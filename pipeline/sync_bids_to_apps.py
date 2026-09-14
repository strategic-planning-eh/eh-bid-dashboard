#!/usr/bin/env python3
"""
sync_bids_to_apps.py — makes the Stakeholder & Competitive Map reflect the live bid tracker on every publish.

Until now a tender entered in the Google Sheet reached the Bid & Tender app within the hour and nothing else: the map's
per-company bid fields were a frozen workbook export and its Bid View block was refreshed by a script nobody called.

What this does, in order (all idempotent, all on the published copy in site/):
  a. Per-company fields on the map — for every competitor in the live roster build (competitors_rebuilt.json, written by
     build_competitors.py each run) that matches a map company:
         bid=True · bc=encounters (exactly as the Bid & Tender app counts them) · bf=High/Medium/Low from bc (5+ / 3–4 / 1–2)
         h2h={app,wins,dq,undercut%} (feeds the "Head-to-head vs EH" block in the detail panel)
         notes: the "Tender-roster intelligence (Mon YYYY): …" sentence is rewritten with the live figures.
     Matching: exact normalised name → alias recorded in the node's notes ("Alias (merged duplicate): …") → containment
     (≥70% of the longer name, ≥10 chars) → difflib ratio ≥0.90. Arabic is NFKC-normalised, tatweel/diacritics stripped,
     legal-form words (company, est., شركة, مؤسسة …) removed on both sides.
  b. Unmatched roster competitors are ADDED to the map as "Active Competitors" — Tier 4, confidence Low, region '—'
     (drawn in the map's Unknown sector), type guessed from the name, and a note saying they came from the bid tracker and
     are not yet in the workbook. The header count and the What's New "Companies › Added" diff pick them up automatically.
  c. The Bid View / Saudi Map block (BANALYTICS) is refreshed from the live Bid & Tender build via refresh_map_banalytics.py
     (skipped with a warning if the bid app file is not present, e.g. when run locally).

  d. TRACKER IS LAW (decided 13 Sep 2026): bid / bc / bf / h2h on every map company are COMPUTED from the live rosters on each
     run. A company the rosters do not name gets bid=False, bc=0. If the workbook had flagged it as a bidder, the flag is kept
     as `claimed=True` (+ a "Claimed bidder (unverified) …" note) so the research is visible but never counted. Confirmations
     from earlier runs do not persist: a company matched last month but absent from today's rosters is reset the same way.
  e. Name bridging lives in pipeline/aliases.csv (tracker_name, map_name, method, status). Rows with status approved/reviewer/
     auto are applied before any fuzzy matching. Every match this run finds by a non-exact method is appended as status=auto
     for a one-time look; reviewer merges from twin_decisions.xlsx are written there too, so the CSV is the durable store.
  f. One feed for every app: competitors_feed.json + sync_stamp.json next to the map. The stamp ("Competitors: N · tracker as
     of D Mon YYYY") is what the map, the Bid & Tender app, the clients app and the news hub must all print.

Usage (CI):  python pipeline/sync_bids_to_apps.py --map site/EH_Stakeholder_Map_CURRENT.html \
                 --competitors pipeline/competitors_rebuilt.json --bids site/EH_Bid_Analysis_CURRENT.html
Writes a machine-readable report next to the map (bid_sync_report.json) and prints a summary. Exit 0 on success.
"""
import argparse, json, re, sys, os, unicodedata, subprocess, datetime as dt
from difflib import SequenceMatcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twins

HERE = os.path.dirname(os.path.abspath(__file__))
LEGAL = r'\b(company|co|ltd|llc|est|establishment|office|for|the|and|of|general|trading|contracting|شركة|مؤسسة|مكتب|للاستشارات|للخدمات|للمقاولات|للتجارة|المحدودة|ذات|مسؤولية|محدودة|الشخص|الواحد|مهنية|شخص|واحد)\b'

ALIAS_RE = re.compile(r'\s*Alias \(merged duplicate\): [^.]*?(?=\s+[A-Z\u0600-\u06FF]|$)')

def norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200d\ufeff\u064b-\u0652]', '', s)
    s = re.sub(r"[’'ʼ`]", '', s)
    s = re.sub(r'[إأآا]', 'ا', s).replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    s = re.sub(LEGAL, ' ', s.casefold())
    return re.sub(r'[^\w\u0600-\u06FF]+', ' ', s).strip()

def grab(html, sid):
    m = re.search(r'(<script id="%s" type="application/json">)(.*?)(</script>)' % sid, html, re.S)
    if not m: sys.exit(f'block <script id="{sid}"> not found in map')
    return m, json.loads(m.group(2))

def bf_of(bc): return 'High' if bc >= 5 else 'Medium' if bc >= 3 else 'Low' if bc >= 1 else ''

def guess_type(name):
    n = name.casefold()
    if re.search(r'consult|استشار|هندس|engineer', n): return 'Consulting Company'
    if re.search(r'lab|مختبر|فحص|test', n): return 'LAB'
    if re.search(r'transport|نقل|logistic', n): return 'Transport'
    if re.search(r'recycl|تدوير', n): return 'Recycling Company'
    if re.search(r'waste|نفايات|مخلفات', n): return 'Waste Management Company'
    if re.search(r'environ|بيئ', n): return 'Environmental Services'
    return 'Other'

def roster_sentence(c, stamp):
    s = f"Tender-roster intelligence ({stamp}): {c['encounters']} encounter(s) in EH bid rosters"
    if c.get('priced_vs'): s += f", undercut EH in {c.get('undercut', 0)}/{c['priced_vs']} priced head-to-heads"
    if c.get('avg_price'): s += f", avg offer ≈ SAR {c['avg_price']:,.0f}"
    if c.get('wins'): s += f", won {c['wins']} tender(s) against EH"
    return s + '.'

SENT_RE = re.compile(r'Tender-roster intelligence \([^)]*\):[^.]*(?:\.\d[^.]*)*\.')   # sentence may contain "≈ SAR 2,334,347." decimals? keep simple

def fold_bid_app(bids_path, roster_to_record):
    """Tracker is law, but one company = one record: roster spellings that this run resolved to the SAME map record are
    folded inside the Bid & Tender app's embedded BA block (every scope: both / y2025 / y2026), so its competitor
    count and scorecard agree with the map and the stamp whatever the state of aliases.csv. Returns folded count for 'both'."""
    h = open(bids_path, encoding='utf-8').read()
    m = re.search(r'(<script id="BA" type="application/json">)(.*?)(</script>)', h, re.DOTALL)
    if not m: return None
    BA = json.loads(m.group(2)); folded_pairs = []
    for scope, blk in BA.items():
        comps = blk.get('competitors') if isinstance(blk, dict) else None
        if not comps: continue
        by = {}; order = []
        for c in comps:
            key = roster_to_record.get(norm(c['name']), norm(c['name']))
            if key not in by: by[key] = dict(c); order.append(key); continue
            d = by[key]
            if scope == 'both': folded_pairs.append((d['name'], c['name']))
            for f in ('encounters', 'wins', 'dq', 'undercut', 'priced_vs'): d[f] = (d.get(f) or 0) + (c.get(f) or 0)
            w1, w2 = (d.get('encounters') or 0) - (c.get('encounters') or 0), (c.get('encounters') or 0)
            if d.get('avg_price') and c.get('avg_price') and (w1 + w2): d['avg_price'] = round((d['avg_price'] * w1 + c['avg_price'] * w2) / (w1 + w2))
            elif not d.get('avg_price'): d['avg_price'] = c.get('avg_price')
            d['undercut_pct'] = round(100 * d['undercut'] / d['priced_vs']) if d.get('priced_vs') else None
        out = [by[k] for k in order]; out.sort(key=lambda x: (-(x.get('encounters') or 0), -(x.get('wins') or 0)))
        blk['competitors'] = out
        if isinstance(blk.get('kpi'), dict) and 'competitors' in blk['kpi']: blk['kpi']['competitors'] = len(out)
    payload = json.dumps(BA, ensure_ascii=False).replace('</', '<\\/')
    open(bids_path, 'w', encoding='utf-8').write(h[:m.start(2)] + payload + h[m.end(2):])
    return len(BA.get('both', {}).get('competitors', [])) if isinstance(BA.get('both'), dict) else None, folded_pairs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', required=True); ap.add_argument('--competitors', required=True); ap.add_argument('--bids')
    ap.add_argument('--decisions', help='twin review workbook (possible_twins.xlsx) with the Decision column filled in; merges become aliases, "Keep separate" pairs are dropped from future twin lists')
    ap.add_argument('--min-encounters', type=int, default=1, help='ignore roster competitors below this many encounters when ADDING new nodes')
    ap.add_argument('--aliases', default=os.path.join(HERE, 'aliases.csv'), help='tracker_name → map_name bridging table (created if missing)')
    ap.add_argument('--tracker-stamp', default=None, help='date the tracker export was taken, e.g. "13 Sep 2026" (defaults to today, KSA)')
    a = ap.parse_args()

    mh = open(a.map, encoding='utf-8').read()
    mdata, D = grab(mh, 'DATA'); nodes = D['nodes']
    comps = json.load(open(a.competitors, encoding='utf-8'))
    comps = [c for c in comps if c.get('name') and c.get('encounters')]
    stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%b %Y')

    # ---- index the map: normalised names + aliases recorded in notes
    idx = {}
    for n in nodes:
        idx.setdefault(norm(n['n']), n)
        for al in re.findall(r'Alias \(merged duplicate\):\s*([^·\n]+)', n.get('notes') or ''):
            for part in re.split(r'\s*[;,/]\s*|\s+\|\s+', al):
                k = norm(part)
                if k: idx.setdefault(k, n)
    # ---- aliases.csv: approved bridges (AR roster spelling → EN workbook name, etc.) take priority over every fuzzy rule
    import csv
    alias_rows, alias_keys = [], set()
    if os.path.exists(a.aliases):
        with open(a.aliases, encoding='utf-8-sig', newline='') as f: alias_rows = list(csv.DictReader(f))
    for r in alias_rows:
        if str(r.get('status', '')).strip().lower() not in ('approved', 'reviewer', 'auto'): continue
        tgt = idx.get(norm(r['map_name']))
        k = norm(r['tracker_name'])
        if tgt is not None and k: idx[k] = tgt; alias_keys.add(k)
    known_alias_pairs = {(norm(r['tracker_name']), norm(r['map_name'])) for r in alias_rows}
    rejected_pairs = {(norm(r['tracker_name']), norm(r['map_name'])) for r in alias_rows if str(r.get('status', '')).strip().lower() == 'rejected'}
    # status=rejected: the reviewer said these are different companies — no matcher may pair them again
    new_alias_rows = []
    def remember_alias(tracker_name, map_name, method, status):
        pair = (norm(tracker_name), norm(map_name))
        if pair in known_alias_pairs or pair[0] == pair[1]: return
        known_alias_pairs.add(pair)
        new_alias_rows.append({'tracker_name': tracker_name.strip(), 'map_name': map_name.strip(), 'method': method, 'status': status, 'added': stamp})
    # ---- reviewer decisions from the twin sheet: "Merge → keep A/B" makes the other name an alias; "Keep separate" is remembered
    decided_pairs, merges, auto_sides = set(), 0, []
    if a.decisions and os.path.exists(a.decisions):
        import openpyxl
        wsx = openpyxl.load_workbook(a.decisions, read_only=True)['Possible twins']
        rows = list(wsx.iter_rows(values_only=True)); hdr = [str(h or '') for h in rows[0]]
        iA, iB, iD = hdr.index('Company A'), hdr.index('Company B'), hdr.index('Decision')
        roster_keys = {norm(c['name']) for c in comps}
        TIER_RANK = {'Tier 1': 1, 'GOV': 1, 'Tier 2': 2, 'Tier 3': 3, 'Tier 4': 4}
        def pick_keep(A, B):
            # note: aliases recorded by an earlier run of this script are ignored here, so the side chosen is the same
            # on a re-run over an already-synced file as on a fresh one
            """'merge' with no side given: keep the record the live rosters know, else the richer one (higher tier, then higher bid count), else A."""
            na = next((n for n in nodes if norm(n['n']) == norm(A)), None)
            nb = next((n for n in nodes if norm(n['n']) == norm(B)), None)
            if (na is None) != (nb is None): return (A if na is not None else B), 'the one that is a map record (the other is a roster spelling → alias)'
            ra, rb = norm(A) in roster_keys, norm(B) in roster_keys
            if ra != rb: return (A if ra else B), 'the one the bid rosters list'
            ta, tb = TIER_RANK.get((na or {}).get('tier'), 9), TIER_RANK.get((nb or {}).get('tier'), 9)
            if ta != tb: return (A if ta < tb else B), 'the higher-tier record'
            ba, bb = (na or {}).get('bc') or 0, (nb or {}).get('bc') or 0
            if ba != bb: return (A if ba > bb else B), 'the record with the higher bid count'
            return A, 'A (no other difference)'
        auto_sides = []
        for r in rows[1:]:
            A, B, dec = (r[iA] or '').strip(), (r[iB] or '').strip(), str(r[iD] or '').strip()
            if not (A and B and dec): continue
            decided_pairs.add(frozenset((norm(A), norm(B))))
            d = dec.lower()
            keep = None
            if d.startswith('merge'):
                if 'keep a' in d: keep = A
                elif 'keep b' in d: keep = B
                else: keep, why = pick_keep(A, B); auto_sides.append({'a': A, 'b': B, 'kept': keep, 'rule': why})
            if keep:
                lose = B if keep == A else A
                tgt = idx.get(norm(keep))
                if tgt is not None:
                    idx[norm(lose)] = tgt; merges += 1; remember_alias(lose, tgt['n'], 'reviewer merge', 'reviewer')
                    al = tgt.get('notes') or ''
                    if f'Alias (merged duplicate): {lose}' not in al: tgt['notes'] = (al + ' ' if al else '') + f'Alias (merged duplicate): {lose}'
                    loser = next((n for n in nodes if norm(n['n']) == norm(lose) and n is not tgt), None)
                    if loser is not None:   # the duplicate record stops counting as a bidder; the kept record carries the data
                        loser['bid'] = False; loser['bc'] = 0; loser['bf'] = ''; loser.pop('h2h', None); loser['merged_into'] = tgt['n']
                        if 'Merged into' not in (loser.get('notes') or ''): loser['notes'] = ((loser.get('notes') or '') + f' Merged into "{tgt["n"]}" by reviewer decision ({stamp}); remove from the workbook.').strip()
        try:   # sheet 2: flags the reviewer decided to clear
            ws2 = openpyxl.load_workbook(a.decisions, read_only=True)['Workbook-only bid flags']
            rows2 = list(ws2.iter_rows(values_only=True)); h2 = [str(h or '') for h in rows2[0]]
            iN, iD2 = h2.index('Company'), h2.index('Decision')
            clear_flags = {norm(r[iN]) for r in rows2[1:] if r[iN] and str(r[iD2] or '').strip().lower().startswith('clear')}
        except Exception: clear_flags = set()
    else: clear_flags = set()
    keys = list(idx)

    # core key: distinctive tokens only (domain words that almost every name shares are removed)
    STOP = set('environmental environment consulting consultation consultant consultants consultancy services service solutions group international arabia arabian saudi al one person'.split()) | \
           set('البيئية البيئي البيئة بيئية للبيئة الاستشارات استشارات الخدمات خدمات المقاولات مقاولات الهندسية هندسية المهنية مهنية التجارية التجاره الدولية العربية السعودية شركه'.split())
    def core(k):
        toks = [t for t in re.sub(r'\bal ', 'al', k).split() if len(t) > 1 and t not in STOP]
        return tuple(toks)
    cores = {}
    for k, n in idx.items():
        c = core(k)
        if c: cores.setdefault(c, []).append(n)
    core_list = list(cores)

    def find(name):
        k = norm(name)
        if not k: return None, 'skip'
        if k in idx: return idx[k], 'exact'
        c = core(k)
        if c and c in cores and len({id(x) for x in cores[c]}) == 1: return cores[c][0], 'core'
        if c:   # every distinctive token of the shorter name inside the longer one, and exactly one candidate
            cs = set(c); cand = []
            for c2 in core_list:
                s2 = set(c2)
                if cs <= s2 and (len(cs) >= 2 or (len(cs) == 1 and len(c[0]) >= 4)): cand += cores[c2]
                elif s2 <= cs and (len(s2) >= 2 or (len(s2) == 1 and len(c2[0]) >= 4)): cand += cores[c2]
            uniq = {id(x): x for x in cand}
            if len(uniq) == 1: return next(iter(uniq.values())), 'core-subset'
            if len(uniq) > 1:   # several companies share the distinctive tokens: take the one whose full name is clearly closest
                scored = sorted(((SequenceMatcher(None, k, norm(x['n'])).ratio(), x) for x in uniq.values()), key=lambda t: -t[0])
                if scored[0][0] >= 0.72 and scored[0][0] - scored[1][0] >= 0.08: return scored[0][1], f'core-subset+ratio {scored[0][0]:.2f}'
        if c and len(c) >= 2:   # fuzzy on the distinctive-token cores ("quality techno certification" ~ "quality tech certification")
            sc = ' '.join(c); scored = []
            for c2 in core_list:
                s2 = ' '.join(c2)
                if abs(len(s2) - len(sc)) > 0.35 * max(len(s2), len(sc)): continue
                r = SequenceMatcher(None, sc, s2).ratio()
                if r >= 0.88: scored.append((r, c2))
            uniq = {id(x): (r, x) for r, c2 in scored for x in cores[c2]}
            if len(uniq) == 1: r, x = next(iter(uniq.values())); return x, f'core-fuzzy {r:.2f}'
            if len(uniq) > 1:
                best = sorted(uniq.values(), key=lambda t: -t[0])
                if best[0][0] - best[1][0] >= 0.06: return best[0][1], f'core-fuzzy {best[0][0]:.2f}'
        for x in keys:
            if (k in x or x in k) and len(min(k, x, key=len)) >= max(10, 0.7 * len(max(k, x, key=len))):
                return idx[x], 'contains'
        best, bs = None, 0
        for x in keys:
            if abs(len(x) - len(k)) > 0.4 * max(len(x), len(k)): continue
            r = SequenceMatcher(None, k, x).ratio()
            if r > bs: bs, best = r, x
        if bs >= 0.90: return idx[best], f'fuzzy {bs:.2f}'
        return None, 'none'

    # ---- a. update matched nodes
    matched, changed, added, unmatched_low = [], [], [], []
    touched = set()
    for c in comps:
        n, how = find(c['name'])
        if n is not None and (norm(c['name']), norm(n['n'])) in rejected_pairs: n, how = None, None
        if n is not None and how == 'exact' and norm(c['name']) in alias_keys: how = 'alias'
        if n is not None and how not in ('exact', 'alias'): remember_alias(c['name'], n['n'], how, 'auto')
        if n is None:
            if c['encounters'] >= a.min_encounters: added.append(c)
            else: unmatched_low.append(c['name'])
            continue
        if id(n) in touched:   # two roster names collapsed onto one map company — sum them
            n['bc'] += c['encounters']; n['h2h']['app'] += c['encounters']; n['h2h']['wins'] += c.get('wins', 0); n['h2h']['dq'] += c.get('dq', 0)
            n['bf'] = bf_of(n['bc']); matched.append((c['name'], n['n'], how + ' (+merged)')); continue
        touched.add(id(n))
        before = (n.get('bid'), n.get('bc'), n.get('bf'))
        n['bid'] = True; n['bc'] = c['encounters']; n['bf'] = bf_of(c['encounters'])
        n['h2h'] = {'app': c['encounters'], 'wins': c.get('wins', 0), 'dq': c.get('dq', 0), 'undercut': c.get('undercut_pct')}
        notes = n.get('notes') or ''
        sent = roster_sentence(c, stamp)
        notes = SENT_RE.sub(sent, notes, count=1) if SENT_RE.search(notes) else (notes + (' ' if notes else '') + sent)
        n['notes'] = notes
        n['bid_synced'] = stamp
        matched.append((c['name'], n['n'], how))
        if before != (True, c['encounters'], bf_of(c['encounters'])): changed.append((n['n'], before[1], c['encounters']))

    # ---- b. before adding: is this competitor a twin of a company already on the map (English/Arabic, spelling variant)?
    freq = {}
    for n in nodes:
        for kk in set(twins.skeleton(n['n'])): freq[kk] = freq.get(kk, 0) + 1
        for t in set(twins.core(n['n'])): freq['w:' + t] = freq.get('w:' + t, 0) + 1
    still_add, twin_matched = [], []
    for c in added:
        tmp = {'n': c['name'], 'cat': 'Active Competitors', 'bid': True, 'act': '', 'city': '—'}
        best = None
        for n in nodes:
            if n.get('auto_added'): continue
            if (norm(c['name']), norm(n['n'])) in rejected_pairs: continue   # reviewer said: different companies
            r = twins.compare(tmp, n, freq)
            if r and (best is None or r[0] > best[0][0]): best = (r, n)
        if best and best[0][0] >= 0.85 and id(best[1]) not in touched:
            n = best[1]; touched.add(id(n))
            before = (n.get('bid'), n.get('bc'), n.get('bf'))
            n['bid'] = True; n['bc'] = c['encounters']; n['bf'] = bf_of(c['encounters'])
            n['h2h'] = {'app': c['encounters'], 'wins': c.get('wins', 0), 'dq': c.get('dq', 0), 'undercut': c.get('undercut_pct')}
            notes = n.get('notes') or ''; sent = roster_sentence(c, stamp)
            notes = SENT_RE.sub(sent, notes, count=1) if SENT_RE.search(notes) else (notes + (' ' if notes else '') + sent)
            if f'Alias (merged duplicate): {c["name"]}' not in notes: notes += f' Alias (merged duplicate): {c["name"]}'
            n['notes'] = notes; n['bid_synced'] = stamp
            matched.append((c['name'], n['n'], 'twin ' + best[0][1][:60])); twin_matched.append(c['name']); remember_alias(c['name'], n['n'], 'twin', 'auto')
            if before != (True, c['encounters'], bf_of(c['encounters'])): changed.append((n['n'], before[1], c['encounters']))
        else: still_add.append(c)
    added = still_add
    for c in added:
        nodes.append({'n': c['name'].strip(), 'cat': 'Active Competitors', 'rg': '—', 'city': '—', 'reg': '—',
                      'typ': guess_type(c['name']), 'sec': None, 'tier': 'Tier 4', 'bid': True, 'sites': None, 'mn': False, 'mp': False,
                      'act': '', 'bc': c['encounters'], 'bf': bf_of(c['encounters']), 'threat': 'Medium' if c['encounters'] >= 3 else 'Low',
                      'collab': False, 'sc': None, 'cap': None, 'bk': 0, 'cf': 'Low', 'cf_basis': 'EH bid tracker roster (auto-added by sync_bids_to_apps)',
                      'drv': 'bids', 'h2h': {'app': c['encounters'], 'wins': c.get('wins', 0), 'dq': c.get('dq', 0), 'undercut': c.get('undercut_pct')},
                      'notes': f"Added automatically from the EH bid tracker rosters ({stamp}) — met EH in {c['encounters']} tender(s) but not yet in the stakeholder workbook; "
                               f"region and company type unverified. " + roster_sentence(c, stamp),
                      'bid_synced': stamp, 'auto_added': stamp})

    # ---- d. tracker is law: anything the rosters did not confirm THIS run stops counting as a bidder
    claimed, stale_cleared, cleared = [], [], 0
    added_ids = {id(n) for n in nodes if n.get('auto_added') == stamp}
    CLAIM_RE = re.compile(r'\s*Claimed bidder \(unverified\)[^.]*\.')
    for n in nodes:
        if id(n) in touched or id(n) in added_ids: n.pop('claimed', None); n['bid_src'] = 'tracker'; n['notes'] = CLAIM_RE.sub('', n.get('notes') or ''); continue
        if n.get('merged_into'): continue
        if n.get('bid'):
            was_tracker = bool(n.get('bid_synced')) or bool(n.get('auto_added'))
            (stale_cleared if was_tracker else claimed).append(n['n'])
            n['claimed'] = not was_tracker and norm(n['n']) not in clear_flags
            n['bid'] = False; n['bc'] = 0; n['bf'] = ''; n.pop('h2h', None); n.pop('bid_synced', None); n['bid_cleared'] = stamp
            n['bid_src'] = 'claimed' if n['claimed'] else ''
            if n['claimed'] and not CLAIM_RE.search(n.get('notes') or ''):
                n['notes'] = ((n.get('notes') or '') + f' Claimed bidder (unverified): flagged in the stakeholder workbook, no record in the EH bid tracker as of {stamp}.').strip()
            if not n['claimed']: n.pop('claimed', None); cleared += norm(n['n']) in clear_flags
        elif n.get('claimed'): n['bid_src'] = 'claimed'
    workbook_only = claimed   # kept for the report's key names
    # ---- possible twins among workbook-only flags and freshly added nodes, minus pairs the reviewer already decided
    focus = [id(n) for n in nodes if (n.get('bid') and id(n) not in touched) or n.get('auto_added')]
    twin_list = [p for p in twins.find_twins(nodes, focus) if frozenset((norm(p['a']['n']), norm(p['b']['n']))) not in decided_pairs]

    if new_alias_rows or not os.path.exists(a.aliases):
        fields = ['tracker_name', 'map_name', 'method', 'status', 'added']
        with open(a.aliases, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
            for r in alias_rows + new_alias_rows: w.writerow({k: r.get(k, '') for k in fields})
    # ---- one company = one record, on the bid app side too
    roster_to_record = {norm(r): norm(mp) for r, mp, how in matched}
    bid_app_count, bid_app_folded = (None, [])
    if a.bids and os.path.exists(a.bids):
        res = fold_bid_app(a.bids, roster_to_record)
        if res: bid_app_count, bid_app_folded = res
    # ---- f. one feed for every app
    tracker_stamp = a.tracker_stamp or dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%-d %b %Y')
    bidders = [n for n in nodes if n.get('bid') and not n.get('merged_into')]
    n_comp = bid_app_count if bid_app_count is not None else len(bidders)   # the stamp shows the folded count — identical on every app
    feed = {'tracker_as_of': tracker_stamp, 'synced': dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).isoformat(timespec='minutes'),
            'roster_competitors': len(comps), 'competitors': n_comp, 'map_bidders': len(bidders), 'recurring': sum(1 for n in bidders if (n.get('bc') or 0) >= 2),
            'claimed_unverified': len(claimed), 'bid_app_folded_pairs': bid_app_folded, 'stamp': f"Competitors: {n_comp} · tracker as of {tracker_stamp}",
            'competitor_list': sorted(({'name': n['n'], 'cat': n.get('cat'), 'tier': n.get('tier'), 'bc': n.get('bc'), 'bf': n.get('bf'), 'h2h': n.get('h2h')} for n in bidders), key=lambda x: (-(x['bc'] or 0), x['name']))}
    _dir = os.path.dirname(os.path.abspath(a.map))
    json.dump(feed, open(os.path.join(_dir, 'competitors_feed.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({'stamp': feed['stamp'], 'tracker_as_of': tracker_stamp, 'competitors': n_comp, 'synced': feed['synced']}, open(os.path.join(_dir, 'sync_stamp.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    D['sync'] = {'stamp': feed['stamp'], 'tracker_as_of': tracker_stamp, 'competitors': n_comp}
    payload = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
    mh = mh[:mdata.start(2)] + payload + mh[mdata.end(2):]
    open(a.map, 'w', encoding='utf-8').write(mh)

    # ---- c. Bid View / Saudi Map block from the live Bid & Tender build
    ban = 'skipped (no --bids file)'
    if a.bids and os.path.exists(a.bids):
        r = subprocess.run([sys.executable, os.path.join(HERE, 'refresh_map_banalytics.py'), '--map', a.map, '--bids', a.bids], capture_output=True, text=True)
        ban = (r.stdout.strip() or r.stderr.strip()[-300:]) if r.returncode == 0 else 'FAILED: ' + r.stderr.strip()[-400:]
    elif a.bids: ban = f'skipped ({a.bids} not found)'

    report = {'synced': dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).isoformat(timespec='minutes'),
              'roster_competitors': len(comps), 'matched': len(matched), 'counts_changed': len(changed), 'added': [c['name'] for c in added],
              'claimed_unverified': len(claimed), 'claimed_names': claimed, 'stale_tracker_confirmations_reset': stale_cleared,
              'aliases_added': new_alias_rows, 'stamp': feed['stamp'], 'reviewer_merges_applied': merges, 'merge_side_chosen_automatically': auto_sides, 'reviewer_flags_cleared': cleared, 'twin_matched_instead_of_added': twin_matched, 'banalytics': ban,
              'possible_twins': [{'a': p['a']['n'], 'b': p['b']['n'], 'score': round(p['score'], 2), 'reason': p['reason']} for p in twin_list],
              'matches': [{'roster': r, 'map': m, 'how': h} for r, m, h in matched], 'changes': [{'map': m, 'from': f, 'to': t} for m, f, t in changed]}
    json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(a.map)), 'bid_sync_report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"bid sync: {len(comps)} roster competitors → {len(matched)} matched to map companies ({len(changed)} counts changed), "
          f"{len(added)} added to the map ({len(twin_matched)} recognised as twins of existing companies instead), "
          f"{len(claimed)} workbook flags kept as claimed-unverified (not counted), {len(stale_cleared)} stale confirmations reset, "
          f"{len(new_alias_rows)} aliases recorded; {len(bid_app_folded)} spelling pairs folded in the bid app; {len(twin_list)} possible twin pairs listed for review"
          + (f"; {merges} reviewer merges applied" if merges else '') + (f"; {cleared} flags cleared by reviewer" if cleared else '') + '.')
    print('BANALYTICS:', ban); print('STAMP:', feed['stamp'])
    if ban.startswith('FAILED'): sys.exit(2)

if __name__ == '__main__':
    main()
