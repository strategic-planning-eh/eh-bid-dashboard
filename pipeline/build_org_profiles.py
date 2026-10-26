#!/usr/bin/env python3
"""
build_org_profiles.py — one profile per organisation for the Organisations view (26 Oct 2026).

Joins the bid tracker (2025 + 2026, as analysed by bid_analytics2.py) to the Stakeholder Map records so one
lookup answers "what do we know about X": every tender X asked for, every tender X bid on against EH, what X
won, what EH sells X, X's licence, and X's map standing (category, tier, region, confidence).

Inputs
  --map        hub/EH_Stakeholder_Map_CURRENT.html   (the <script id="DATA"> block — map records + aliases in notes)
  --ba         pipeline/bidanalytics2.json OR  a built bid-app HTML (its <script id="BA"> block is read)
  --aliases    pipeline/aliases.csv        (roster spelling → map name; approved / reviewer / auto honoured, rejected blocked)
  --client-aliases pipeline/client_aliases.json (tracker Arabic client → map English name)
  --bidraw     pipeline/bidraw2.json       (optional; adds EH's ex-VAT offer, submission date, deadline, bid bond)
  --proposed   pipeline/org_bridges_proposed.csv (dry run only: bridges Youssef has not yet approved; same columns as aliases.csv,
               status=proposed honoured, status=rejected blocked. Once approved they move into aliases.csv and this file empties.)
Outputs
  --out        org_profiles.json           ({"built", "scope", "orgs":[...], "unresolved":{...}})
  --unresolved EH_Org_Unresolved.xlsx      (optional review workbook: names the tracker uses that match no map record)

Scope (Youssef, 26 Oct 2026): organisations with activity only — tracker clients, roster bidders, winners,
EH clients (cl ledger), licence holders with a bid/client link. Pure map rows with no activity are not profiled.

Name matching mirrors sync_bids_to_apps.py (norm → aliases.csv → core tokens → core-subset → core-fuzzy →
contains → fuzzy ≥0.90). A tracker client is first bridged through client_aliases.json, then client_canon
variants, then the same matcher. Anything still unmatched becomes an "unresolved" profile (shown, flagged,
never counted into a map record) and is listed in the review workbook for Youssef's decision.
"""
import argparse, csv, json, os, re, sys, datetime as dt, unicodedata
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sync_bids_to_apps import norm, grab          # single source of the normaliser
from namecheck import looks_like_company

STOP = set('environmental environment consulting consultation consultant consultants consultancy services service solutions group international arabia arabian saudi al one person'.split()) | \
       set('البيئية البيئي البيئة بيئية للبيئة الاستشارات استشارات الخدمات خدمات المقاولات مقاولات الهندسية هندسية المهنية مهنية التجارية التجاره الدولية العربية السعودية شركه'.split())
# words that never identify an institution on their own (a one-word overlap on these is not a match)
GENERIC = set('وزاره هيئه الهيئه مركز المركز اداره الاداره العامه الوطني الوطنيه القوات مؤسسه جامعه بلديه امانه منطقه ministry authority center centre general national corporation corp agency university municipality'.split())

EH_NAMES = {'__eh__', 'eh', 'environmental horizons', 'environmental horizons (eh)', 'افاق البيئه', 'شركة آفاق البيئة', 'افاق البيئة', 'afaq al-biah', 'afaq albiah', 'afaq al biah (eh)'}
def is_eh(name):
    k = norm(name)
    return k in {norm(x) for x in EH_NAMES} or 'horizons' in k or 'افاق البيئ' in k or ('afaq' in k and 'biah' in k)

class Matcher:
    def __init__(self, nodes, aliases_csv=None, client_aliases=None, client_canon=None, proposed_csv=None):
        self.idx = {}
        for n in nodes:
            self.idx.setdefault(norm(n['n']), n)
            for al in re.findall(r'Alias \(merged duplicate\):\s*([^·\n]+)', n.get('notes') or ''):
                for part in re.split(r'\s*[;,/]\s*|\s+\|\s+', al):
                    k = norm(part)
                    if k: self.idx.setdefault(k, n)
        self.rejected = set(); self.bridged = {}
        for path, ok in ((aliases_csv, ('approved', 'reviewer', 'auto')), (proposed_csv, ('proposed',))):
            if not path or not os.path.exists(path): continue
            with open(path, encoding='utf-8-sig', newline='') as f: rows = list(csv.DictReader(f))
            for r in rows:
                st = str(r.get('status', '')).strip().lower()
                if st == 'rejected': self.rejected.add((norm(r['tracker_name']), norm(r['map_name']))); continue
                if st not in ok: continue
                tgt = self.idx.get(norm(r['map_name'])); k = norm(r['tracker_name'])
                if tgt is None: print('  bridge target not on map:', r['map_name'])
                if tgt is not None and k: self.idx[k] = tgt; self.bridged[k] = st
        # tracker Arabic client → map English record (client_aliases.json), plus client_canon variants
        self.client_map = {}
        if client_aliases:
            for ar, en in client_aliases.items():
                tgt = self.idx.get(norm(en))
                if tgt is not None: self.client_map[norm(ar)] = tgt; self.idx.setdefault(norm(ar), tgt)
        if client_canon:
            for ar, spec in (client_canon.get('clients') or {}).items():
                tgt = self.idx.get(norm(spec.get('en', ''))) or self.idx.get(norm(ar)) or self.client_map.get(norm(ar))
                if tgt is None: continue
                for v in [ar] + list(spec.get('variants') or []):
                    k = norm(v)
                    if k: self.client_map.setdefault(k, tgt); self.idx.setdefault(k, tgt)
        self.keys = list(self.idx)
        self.cores = {}
        for k, n in self.idx.items():
            c = self.core(k)
            if c: self.cores.setdefault(c, []).append(n)
        self.core_list = list(self.cores)
        self.cache = {}

    @staticmethod
    def core(k):
        return tuple(t for t in re.sub(r'\bal ', 'al', k).split() if len(t) > 1 and t not in STOP)

    def find(self, name, client=False):
        key = (norm(name), client)
        if key in self.cache: return self.cache[key]
        r = self._find(name, client)
        if r[0] is not None and (norm(name), norm(r[0]['n'])) in self.rejected: r = (None, 'rejected')
        self.cache[key] = r
        return r

    def _find(self, name, client):
        k = norm(name)
        if not k: return None, 'skip'
        if k in self.bridged: return self.idx[k], 'bridge-' + self.bridged[k]
        if client and k in self.client_map: return self.client_map[k], 'client-alias'
        if k in self.idx: return self.idx[k], 'exact'
        c = self.core(k)
        if c and c in self.cores and len({id(x) for x in self.cores[c]}) == 1: return self.cores[c][0], 'core'
        if c:
            cs = set(c); cand = []
            for c2 in self.core_list:
                s2 = set(c2)
                if cs <= s2 and (len(cs) >= 2 or (len(cs) == 1 and len(c[0]) >= 4 and c[0] not in GENERIC)): cand += self.cores[c2]
                elif s2 <= cs and (len(s2) >= 2 or (len(s2) == 1 and len(c2[0]) >= 4 and c2[0] not in GENERIC)): cand += self.cores[c2]
            uniq = {id(x): x for x in cand}
            if len(uniq) == 1: return next(iter(uniq.values())), 'core-subset'
            if len(uniq) > 1:
                scored = sorted(((SequenceMatcher(None, k, norm(x['n'])).ratio(), x) for x in uniq.values()), key=lambda t: -t[0])
                if scored[0][0] >= 0.72 and scored[0][0] - scored[1][0] >= 0.08: return scored[0][1], f'core-subset+ratio {scored[0][0]:.2f}'
        if c and len(c) >= 2:
            sc = ' '.join(c); scored = []
            for c2 in self.core_list:
                s2 = ' '.join(c2)
                if abs(len(s2) - len(sc)) > 0.35 * max(len(s2), len(sc)): continue
                r = SequenceMatcher(None, sc, s2).ratio()
                if r >= 0.88: scored.append((r, c2))
            uniq = {id(x): (r, x) for r, c2 in scored for x in self.cores[c2]}
            if len(uniq) == 1: r, x = next(iter(uniq.values())); return x, f'core-fuzzy {r:.2f}'
            if len(uniq) > 1:
                best = sorted(uniq.values(), key=lambda t: -t[0])
                if best[0][0] - best[1][0] >= 0.06: return best[0][1], f'core-fuzzy {best[0][0]:.2f}'
        for x in self.keys:
            if (k in x or x in k) and len(min(k, x, key=len)) >= max(10, 0.7 * len(max(k, x, key=len))):
                return self.idx[x], 'contains'
        best, bs = None, 0
        for x in self.keys:
            if abs(len(x) - len(k)) > 0.4 * max(len(x), len(k)): continue
            r = SequenceMatcher(None, k, x).ratio()
            if r > bs: bs, best = r, x
        if bs >= 0.90: return self.idx[best], f'fuzzy {bs:.2f}'
        return None, 'none'

    def suggest(self, name, n=3):
        """closest map names for the review workbook (never applied automatically)"""
        k = norm(name); out = []
        for x in self.keys:
            if abs(len(x) - len(k)) > 0.5 * max(len(x), len(k), 1): continue
            out.append((SequenceMatcher(None, k, x).ratio(), self.idx[x]['n']))
        out.sort(key=lambda t: -t[0]); seen, res = set(), []
        for r, nm in out:
            if nm in seen: continue
            seen.add(nm); res.append((nm, round(r, 2)))
            if len(res) == n: break
        return res


def load_ba(path):
    if path.lower().endswith('.html'):
        html = open(path, encoding='utf-8').read()
        _, ba = grab(html, 'BA')
    else:
        ba = json.load(open(path, encoding='utf-8'))
    return ba['both'] if 'both' in ba else ba


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', required=True); ap.add_argument('--ba', required=True)
    ap.add_argument('--aliases', default=os.path.join(HERE, 'aliases.csv'))
    ap.add_argument('--client-aliases', default=os.path.join(HERE, 'client_aliases.json'))
    ap.add_argument('--client-canon', default=os.path.join(HERE, 'client_canon.json'))
    ap.add_argument('--bidraw', default=None)
    ap.add_argument('--proposed', default=None, help='org_bridges_proposed.csv — dry-run bridges awaiting approval (status=proposed honoured, rejected blocked)')
    ap.add_argument('--out', required=True); ap.add_argument('--unresolved', default=None)
    ap.add_argument('--stamp', default=None)
    a = ap.parse_args()

    mh = open(a.map, encoding='utf-8').read()
    _, D = grab(mh, 'DATA'); nodes = D['nodes']
    ba = load_ba(a.ba)
    cal = json.load(open(a.client_aliases, encoding='utf-8')) if os.path.exists(a.client_aliases) else {}
    canon = json.load(open(a.client_canon, encoding='utf-8')) if os.path.exists(a.client_canon) else {}
    raw = {}
    if a.bidraw and os.path.exists(a.bidraw):
        bj = json.load(open(a.bidraw, encoding='utf-8'))
        for b in (bj.get('bids') if isinstance(bj, dict) else bj): raw[(b['year'], b['sn'])] = b
    M = Matcher(nodes, a.aliases, cal, canon, a.proposed)

    pricing = {(r['year'], r['sn']): r for r in ba.get('pricing', {}).get('rows', [])}
    ba_clients = {c['name']: c for c in ba.get('clients', [])}

    profiles = {}          # id → profile
    roster_dropped = []    # tender titles / reasons found in a roster (escalated, never shown as bidders)
    unresolved = {'clients': {}, 'bidders': {}, 'winners': {}}
    def prof_for(node, name=None, kind=None):
        if node is not None:
            pid = 'map:' + node['n']
            if pid not in profiles:
                profiles[pid] = dict(id=pid, name=node['n'], resolved=True, cat=node.get('cat'), tier=node.get('tier'),
                    typ=node.get('typ'), sec=node.get('sec'), region=node.get('rg'), city=node.get('city'), cf=node.get('cf'),
                    threat=node.get('threat'), score=node.get('sc'), notes=node.get('notes') or '',
                    aliases=sorted({p.strip() for al in re.findall(r'Alias \(merged duplicate\):\s*([^·\n]+)', node.get('notes') or '') for p in re.split(r'\s*[;,/]\s*|\s+\|\s+', al) if p.strip()}),
                    lic=dict(act=node.get('act') or '', exp=(node.get('mw') or {}).get('exp') if isinstance(node.get('mw'), dict) else None, mw=node.get('mw')) if (node.get('act') or node.get('mw')) else None,
                    client=node.get('cl') or None, cltier=node.get('cltier'), etimad=node.get('etimad'),
                    bc=node.get('bc', 0), h2h=node.get('h2h'),
                    tracker_names=[], tenders=[], encounters=[], wins=[], roles=[])
            return profiles[pid]
        pid = 'unresolved:' + norm(name)
        if pid not in profiles:
            profiles[pid] = dict(id=pid, name=name, resolved=False, cat='Not on the map yet', tier='—', typ='', sec='', region='—', city='',
                cf=None, threat='', score=None, notes='', aliases=[], lic=None, client=None, cltier=None, etimad=None, bc=0, h2h=None,
                tracker_names=[], tenders=[], encounters=[], wins=[], roles=[])
        unresolved[kind].setdefault(name, {'n': 0, 'value': 0, 'suggest': M.suggest(name)})
        return profiles[pid]

    def add_name(p, nm):
        if nm and nm not in p['tracker_names'] and norm(nm) != norm(p['name']): p['tracker_names'].append(nm)

    # ---- tenders by client
    for t in ba.get('bidlist', []):
        key = (t['year'], t['sn']); pr = pricing.get(key, {}); rb = raw.get(key, {})
        cname = t.get('client') or ''
        node, how = M.find(cname, client=True) if cname else (None, 'skip')
        p = prof_for(node, cname, 'clients')
        if not node: unresolved['clients'][cname]['n'] += 1; unresolved['clients'][cname]['value'] += (t.get('value') or 0)
        add_name(p, cname)
        bidders = []; dropped = []
        for b in pr.get('bidders', []):
            if not b.get('eh') and not is_eh(b['name']) and not looks_like_company(b['name']): dropped.append(b['name']); continue   # a tender title or a reason in the roster is never a bidder
            bidders.append(dict(name=b['name'], price=b.get('price'), dq=b.get('dq'), eh=b.get('eh') or is_eh(b['name']), rank=b.get('rank'), won=b.get('won'), undisclosed=b.get('undisclosed')))
        if dropped: roster_dropped.append(dict(ref=f"{t['year']}/{t['sn']}", names=dropped))
        # EH submitted = tracker says so, or EH has a price / a submission date / a result (Youssef, Oct 2026: match across columns)
        submitted = bool(t.get('submitted')) or t.get('sub') == 'Yes' or bool(t.get('subdate')) or pr.get('eh') is not None or t.get('outcome') in ('Won', 'Lost') or rb.get('substatus') == 'Yes' or bool(rb.get('subdate'))
        eh_price = pr.get('eh')
        if eh_price is None and t.get('per_unit') and rb.get('offer_vat'): eh_price = rb['offer_vat']   # per-unit rate: the roster has no lump sums to rank, show EH's own rate
        wname = t.get('winner') or ''
        tender = dict(year=t['year'], sn=t['sn'], ref=f"{t['year']}/{t['sn']}", date=t.get('date'), title=t.get('title'), platform=t.get('platform'),
            svc=t.get('svc'), dur=t.get('dur'), value=t.get('value'), eh_price=eh_price, per_unit=bool(t.get('per_unit')), eh_offer_exvat=rb.get('offer'),
            nbid=t.get('nbid'), n_priced=pr.get('n_priced'), low=pr.get('low'), gap=pr.get('gap'), rank=pr.get('rank'),
            winner=wname, win_price=pr.get('win_price') if pr.get('has_winner') else None, outcome=t.get('outcome'), status=t.get('status'),
            committee=t.get('committee'), submitted=submitted,
            subdate=t.get('subdate') or rb.get('subdate'), deadline=t.get('deadline') or rb.get('submit'), lossreason=t.get('lossreason'),
            reason=t.get('reason'), bidders=bidders, how=how)
        p['tenders'].append(tender)
        if 'client' not in p['roles']: p['roles'].append('client')
        # ---- bidders (competitors) on this tender
        for b in bidders:
            if b['eh'] or is_eh(b['name']) or not looks_like_company(b['name']): continue
            n2, how2 = M.find(b['name'])
            q = prof_for(n2, b['name'], 'bidders')
            if not n2: unresolved['bidders'][b['name']]['n'] += 1
            add_name(q, b['name'])
            q['encounters'].append(dict(year=t['year'], sn=t['sn'], ref=tender['ref'], date=t.get('date'), title=t.get('title'), client=cname,
                client_id=p['id'], their_price=b['price'], eh_price=pr.get('eh'), dq=b['dq'], rank=b['rank'], won=b['won'],
                undercut=(b['price'] is not None and pr.get('eh') is not None and b['price'] < pr['eh']), outcome=t.get('outcome'), how=how2))
            if 'competitor' not in q['roles']: q['roles'].append('competitor')
        # ---- winner
        if wname and wname not in ('EH', '__EH__') and not is_eh(wname) and looks_like_company(wname):
            n3, how3 = M.find(wname)
            w = prof_for(n3, wname, 'winners')
            if not n3: unresolved['winners'][wname]['n'] += 1; unresolved['winners'][wname]['value'] += (pr.get('win_price') or t.get('value') or 0)
            add_name(w, wname)
            w['wins'].append(dict(year=t['year'], sn=t['sn'], ref=tender['ref'], title=t.get('title'), client=cname, client_id=p['id'], win_price=pr.get('win_price'), eh_price=pr.get('eh'), how=how3))
            if 'winner' not in w['roles']: w['roles'].append('winner')

    # ---- EH clients with a contracts ledger but no tender (still an organisation people ask about)
    for n in nodes:
        if n.get('cl') or n.get('h2h') or n.get('bid') or n.get('etimad'):
            p = prof_for(n)
            if n.get('cl') and 'eh-client' not in p['roles']: p['roles'].append('eh-client')

    # ---- KPIs per profile
    def kpis(p):
        T = p['tenders']; sub = [t for t in T if t['submitted']]
        won = [t for t in T if t['outcome'] == 'Won']; lost = [t for t in T if t['outcome'] in ('Lost', 'Not awarded')]
        pend = [t for t in T if t['outcome'] == 'Pending']; canc = [t for t in T if t['outcome'] == 'Cancelled']
        decided = len(won) + len(lost)
        E = p['encounters']; priced = [e for e in E if e['their_price'] is not None and e['eh_price'] is not None]
        p['kpi'] = dict(tenders=len(T), submitted=len(sub), won=len(won), lost=len(lost), pending=len(pend), cancelled=len(canc),
            win_rate=round(100 * len(won) / decided) if decided else None,
            value_asked=sum(t['value'] or 0 for t in T), value_won=sum((t['win_price'] or t['value'] or 0) for t in won),
            value_lost=sum((t['win_price'] or t['value'] or 0) for t in lost),
            years=sorted({t['year'] for t in T}),
            encounters=len(E), beat_eh=sum(1 for e in E if e['won']), undercut=sum(1 for e in E if e['undercut']), priced_vs=len(priced),
            undercut_pct=round(100 * sum(1 for e in priced if e['undercut']) / len(priced)) if priced else None,
            dq=sum(1 for e in E if e['dq']), wins_total=len(p['wins']),
            client_value=(p['client'] or {}).get('val'), client_projects=(p['client'] or {}).get('proj'))
        p['tenders'].sort(key=lambda t: (t['year'], t['sn']), reverse=True)
        p['encounters'].sort(key=lambda t: (t['year'], t['sn']), reverse=True)
        # list order: tender and bid activity first (what people ask about), then the client ledger as a tie-breaker
        p['activity'] = 10 * (p['kpi']['tenders'] + p['kpi']['encounters'] + 2 * p['kpi']['wins_total']) + min(p['kpi']['client_projects'] or 0, 9)
    for p in profiles.values(): kpis(p)

    orgs = sorted(profiles.values(), key=lambda p: (-p['activity'], p['name']))
    stamp = a.stamp or dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%-d %b %Y')
    out = dict(built=stamp, scope='organisations with activity (tracker clients, roster bidders, winners, EH clients)',
               years=sorted({t['year'] for p in orgs for t in p['tenders']}),
               counts=dict(orgs=len(orgs), resolved=sum(1 for p in orgs if p['resolved']), unresolved=sum(1 for p in orgs if not p['resolved']),
                           tenders=len(ba.get('bidlist', [])), map_records=len(nodes)),
               unresolved={k: [dict(name=n, **v) for n, v in sorted(d.items(), key=lambda t: -t[1]['n'])] for k, d in unresolved.items()},
               roster_dropped=roster_dropped,
               orgs=orgs)
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    if roster_dropped: print('  roster entries dropped as non-company text:', roster_dropped)
    print(f"org_profiles: {len(orgs)} organisations ({out['counts']['resolved']} on the map, {out['counts']['unresolved']} not yet) from {out['counts']['tenders']} tenders; "
          f"unresolved clients {len(unresolved['clients'])}, bidders {len(unresolved['bidders'])}, winners {len(unresolved['winners'])}")

    if a.unresolved:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.worksheet.datavalidation import DataValidation
        wb = Workbook(); wb.remove(wb.active)
        head = Font(bold=True, color='FFFFFF'); fill = PatternFill('solid', fgColor='1B2A6E')
        def sheet(title, cols, rows, decision_opts):
            ws = wb.create_sheet(title); ws.append(cols)
            for c in ws[1]: c.font = head; c.fill = fill; c.alignment = Alignment(wrap_text=True, vertical='center')
            for r in rows: ws.append(r)
            dv = DataValidation(type='list', formula1='"' + ','.join(decision_opts) + '"', allow_blank=True); ws.add_data_validation(dv)
            dcol = cols.index('Decision') + 1
            for i in range(2, len(rows) + 2): dv.add(ws.cell(row=i, column=dcol))
            for i, w in enumerate([46, 10, 16, 40, 10, 40, 10, 40, 10, 22, 40], 1): ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
            ws.freeze_panes = 'A2'
        for kind, label in (('clients', 'Tracker clients'), ('bidders', 'Roster bidders'), ('winners', 'Winners')):
            rows = []
            for n, v in sorted(unresolved[kind].items(), key=lambda t: -t[1]['n']):
                s = v['suggest'] + [('', '')] * 3
                rows.append([n, v['n'], v['value'] or 0, s[0][0], s[0][1], s[1][0], s[1][1], s[2][0], s[2][1], '', ''])
            sheet(label + ' not on map', ['Tracker name', 'Tenders' if kind != 'bidders' else 'Encounters', 'Value (SAR)', 'Closest map name 1', 'Ratio 1', 'Closest map name 2', 'Ratio 2', 'Closest map name 3', 'Ratio 3', 'Decision', 'Map name to use (if "Link to")'],
                  rows, ['Link to closest 1', 'Link to closest 2', 'Link to closest 3', 'Link to (name in next column)', 'Add as new record', 'Not a company — ignore', 'Unsure'])
        if a.proposed and os.path.exists(a.proposed):
            with open(a.proposed, encoding='utf-8-sig', newline='') as f: prow = [r for r in csv.DictReader(f) if r.get('status') == 'proposed']
            sheet('Proposed bridges', ['Tracker name', 'Tenders' , 'Value (SAR)', 'Closest map name 1', 'Ratio 1', 'Closest map name 2', 'Ratio 2', 'Closest map name 3', 'Ratio 3', 'Decision', 'Map name to use (if "Link to")'],
                  [[r['tracker_name'], '', '', r['map_name'], 'proposed', '', '', '', '', '', ''] for r in prow], ['Approve', 'Reject', 'Link to (name in next column)', 'Unsure'])
        ws = wb.create_sheet('How to use', 0)
        for line in ['EH Organisations view — names the bid tracker uses that match no Stakeholder Map record (' + stamp + ').',
                     'The matcher is the same as the bid→map sync (exact, alias, core tokens, fuzzy ≥0.90); anything here fell below it.',
                     'Fill Decision on each sheet. "Link to…" adds an approved bridge to pipeline/aliases.csv / client_aliases.json; "Add as new record" creates a map record (category by role: client → Clients / Potential Clients Tier 2, bidder → Active Competitors Tier 4).',
                     'Until decided, these organisations still get a profile in the view, marked "Not on the map yet", and nothing is counted into any map record.',
                     '"Proposed bridges" lists the links Claude applied in the dry run (pipeline/org_bridges_proposed.csv, status=proposed). Approve → the row moves to aliases.csv as approved; Reject → it is recorded as rejected and the tracker name becomes "Not on the map yet".']:
            ws.append([line])
        ws.column_dimensions['A'].width = 140
        wb.save(a.unresolved); print('review workbook:', a.unresolved)

if __name__ == '__main__':
    main()
