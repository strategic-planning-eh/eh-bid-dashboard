#!/usr/bin/env python3
"""
build_changelog.py — weekly "What's New" generator for the EH Strategic Intelligence Hub.

  Data changes are DIFFED mechanically (previous snapshot vs current build).
  Fixes are NEVER inferred: they come only from CHANGES.md (human-written).

Inputs
  --hub DIR            folder holding the 8 published HTML files (site/ or hub/)
  --prev DIR           previous snapshot folder (stakeholders.json, bids.json, clients.json)
  --changes FILE       CHANGES.md   (app | severity | view? | EN | AR, one fix per line under a ## week heading)
  --out FILE           changelog.json to write (existing weeks are kept, 12-week retention)
  --snapshot-out DIR   where to write the new snapshot (uploaded as a workflow artefact)
  --init               allow the very first run with no previous snapshot (writes snapshot, no diff)

Exit codes: 0 ok · 2 previous snapshot missing (build must fail) · 3 CHANGES.md malformed
"""
import argparse, json, re, sys, os, datetime as dt, unicodedata

# ------------------------------------------------------------------ extraction from the built apps
def _grab(html, sid):
    m = re.search(r'<script id="%s" type="application/json">(.*?)</script>' % sid, html, re.S)
    return json.loads(m.group(1)) if m else None

def _norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200d\ufeff]', '', s)
    s = re.sub(r'[إأآا]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي')
    return re.sub(r'\s+', ' ', s).strip().casefold()

def extract(hub):
    out = {}
    p = os.path.join(hub, 'EH_Stakeholder_Map_CURRENT.html')
    d = _grab(open(p, encoding='utf-8').read(), 'DATA') if os.path.exists(p) else None
    if d:
        out['stakeholders'] = {n['n']: {'typ': n.get('typ'), 'cat': n.get('cat'), 'tier': n.get('tier'), 'cf': n.get('cf'),
                                        'bid': bool(n.get('bid')), 'bc': n.get('bc') or 0, 'drv': n.get('drv')} for n in d['nodes']}
    p = os.path.join(hub, 'EH_Bid_Analysis_CURRENT.html')
    b = _grab(open(p, encoding='utf-8').read(), 'BA') if os.path.exists(p) else None
    if b:
        rows = b['both'].get('bidlist', [])
        out['bids'] = {f"{r.get('year')}/{r.get('sn')}": {'title': r.get('title'), 'client': r.get('client'), 'outcome': r.get('outcome'),
                                                          'winner': r.get('winner'), 'value': r.get('value'), 'status': r.get('status')} for r in rows}
        out['clients'] = sorted({r.get('client') for r in rows if r.get('client')})
    p = os.path.join(hub, 'EH_Client_Bubble_Map_CURRENT.html')
    if os.path.exists(p):
        m = re.search(r'const DATA = (\[\{.*?\}\]);', open(p, encoding='utf-8').read(), re.S)
        if m:
            try:
                cl = json.loads(m.group(1))
                out['eh_clients'] = sorted({c.get('name') or c.get('n') or c.get('company') for c in cl if isinstance(c, dict)} - {None})
            except Exception:
                pass
    return out

# ------------------------------------------------------------------ news wing: each report's own version/date → Sources tab
NEWS = [('vision2030_dashboard.html', 'Vision 2030 Dashboard', [r'Last reviewed <strong>([^<]+)</strong>', r'const LAST_REVIEWED = "([^"]+)"']),
        ('saudi_fiscal_monitor_2026.html', 'Saudi Fiscal Monitor 2026', [r'(v\d+ · \d{2}/\d{2}/\d{4})']),
        ('eh_news_intelligence.html', 'Corporate & Government News', [r'<title>[^<]*?·\s*([^<·]+Update)</title>', r'Generated</[^>]+>\s*<[^>]+>([^<]+)<']),
        ('pif_intelligence_hub.html', 'PIF Intelligence Hub', [r'<title>PIF annual reports (\d{4}\u2013\d{4})[^<]*</title>'])]  # coverage years; PIF publishes annually

def _dmy_to_iso(s):
    m = re.match(r'(\d{2})/(\d{2})/(\d{4})', s.strip())
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else None

def news_sources(hub):
    out = []
    for fn, name, pats in NEWS:
        p = os.path.join(hub, fn)
        if not os.path.exists(p): continue
        h = open(p, encoding='utf-8').read(); ver = None
        for pat in pats:
            m = re.search(pat, h)
            if m: ver = m.group(1).strip(); break
        iso = _dmy_to_iso(ver.split('· ')[-1]) if ver and '/' in ver else None
        out.append({'name': name, 'refreshed': iso, 'note': (('covers annual reports ' if 'PIF' in name else 'report version: ') + ver) if ver else 'version not detected — add a marker to the report header'})
    return out

# ------------------------------------------------------------------ diff
def diff(prev, cur):
    data = {'added': [], 'removed': [], 'merged': [], 'confidence_up': [], 'tier_moves': [],
            'bids': {'new': 0, 'won': [], 'lost': []}, 'clients': {'new': 0, 'lost': 0}, 'totals': {}}
    ps, cs = prev.get('stakeholders', {}), cur.get('stakeholders', {})
    pn, cn = {_norm(k): k for k in ps}, {_norm(k): k for k in cs}
    added = [cn[k] for k in cn if k not in pn]
    removed = [pn[k] for k in pn if k not in cn]
    # a removed name whose normalised form is a prefix/suffix twin of a kept name → alias of a merge
    for r in list(removed):
        rn = _norm(r)
        twin = next((cn[k] for k in cn if k != rn and (rn in k or k in rn) and len(min(rn, k, key=len)) >= 8), None)
        if twin:
            # Display-name rule (approved 06/09/2026): the KEPT row is the English registry name, the ALIAS is the
            # Arabic or short name. The build cannot rename rows; it flags a pair that breaks the rule for the analyst.
            rule_ok = bool(re.search(r'[A-Za-z]', twin)) or not re.search(r'[A-Za-z]', r)
            data['merged'].append({'kept': twin, 'alias': r, **({} if rule_ok else {'check': 'kept name is not the English registry name — rename in the workbook'})}); removed.remove(r)
            data['removed'].append({'n': r, 'alias': twin, 'reason': 'merged'})
    data['added'] = [{'n': n, 'typ': cs[n].get('typ'), 'cat': cs[n].get('cat')} for n in sorted(added)]
    data['removed'] += [{'n': n} for n in sorted(removed)]
    rank = {'Low': 0, 'Medium': 1, 'High': 2}
    for k, n in cn.items():
        if k in pn:
            a, b = ps[pn[k]], cs[n]
            if a.get('cf') != b.get('cf') and rank.get(b.get('cf'), -1) > rank.get(a.get('cf'), -1):
                data['confidence_up'].append({'n': n, 'from': a.get('cf') or '—', 'to': b.get('cf'), 'basis': 'research rubric'})
            if a.get('tier') != b.get('tier') and b.get('tier'):
                data['tier_moves'].append({'n': n, 'from': a.get('tier') or '—', 'to': b.get('tier'), 'driver': b.get('drv') or ''})
    pb, cb = prev.get('bids', {}), cur.get('bids', {})
    data['bids']['new'] = len([k for k in cb if k not in pb])
    for k, r in cb.items():
        o = (pb.get(k) or {}).get('outcome')
        if r.get('outcome') != o:
            if str(r.get('outcome')).lower() == 'won':
                data['bids']['won'].append({'title': r.get('title'), 'client': r.get('client'), 'value': r.get('value')})
            elif str(r.get('outcome')).lower() in ('lost', 'not awarded'):
                data['bids']['lost'].append({'title': r.get('title'), 'client': r.get('client'), 'winner': r.get('winner')})
    pc, cc = set(prev.get('clients', [])), set(cur.get('clients', []))
    data['clients'] = {'new': len(cc - pc), 'lost': len(pc - cc)}
    data['totals'] = {'orgs': len(cs), 'tenders': len(cb), 'clients': len(cur.get('eh_clients', [])) or None}
    return data

# ------------------------------------------------------------------ CHANGES.md
LINE = re.compile(r'^\s*(?P<app>stake|bids|clients|news|hub)\s*\|\s*(?P<sev>major|minor)\s*\|\s*(?:(?P<view>[^|]*?)\s*\|\s*)?(?P<en>[^|]+?)\s*\|\s*(?P<ar>[^|]+?)\s*$')

def parse_changes(path, week):
    """Return fixes for `week` (## 2026-W36 heading). Malformed line → exit 3."""
    fixes, cur, bad = [], None, []
    for i, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.rstrip('\n')
        if not line.strip() or line.lstrip().startswith(('#', '<!--', '|--', '| app')) and not line.lstrip().startswith('## '):
            if line.lstrip().startswith('## '):
                cur = line.strip()[3:].strip()
            continue
        if line.lstrip().startswith('## '):
            cur = line.strip()[3:].strip(); continue
        if cur != week:
            continue
        m = LINE.match(line.strip().strip('|'))
        if not m:
            bad.append(f'line {i}: {line[:90]}'); continue
        fixes.append({'app': m['app'], 'severity': m['sev'], 'view': (m['view'] or '').strip() or None,
                      'en': m['en'].strip(), 'ar': m['ar'].strip()})
    if bad:
        print('CHANGES.md malformed (app | severity | [view |] EN | AR):\n  ' + '\n  '.join(bad), file=sys.stderr); sys.exit(3)
    return fixes

# ------------------------------------------------------------------ main
def iso_week(d):
    y, w, _ = d.isocalendar(); mon = d - dt.timedelta(days=d.weekday())
    return f'{y}-W{w:02d}', mon.isoformat(), (mon + dt.timedelta(days=6)).isoformat()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hub', required=True); ap.add_argument('--prev', required=True); ap.add_argument('--changes', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--snapshot-out', required=True)
    ap.add_argument('--init', action='store_true'); ap.add_argument('--sources', default=None, help='JSON list of {name,refreshed}')
    ap.add_argument('--now', default=None)
    a = ap.parse_args()
    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone(dt.timedelta(hours=3)))
    week, wfrom, wto = iso_week(now.date())

    cur = extract(a.hub)
    if not cur.get('stakeholders'):
        print('FATAL: could not read the stakeholder dataset from', a.hub, file=sys.stderr); sys.exit(2)
    prev_file = os.path.join(a.prev, 'snapshot.json')
    if not os.path.exists(prev_file):
        if not a.init:
            print('FATAL: previous snapshot missing at', prev_file, '— refusing to publish an empty week. '
                  'Restore the snapshot artefact or run once with --init.', file=sys.stderr); sys.exit(2)
        prev = {}
        print('INIT run: no previous snapshot; data diff will be empty this week only.')
    else:
        prev = json.load(open(prev_file, encoding='utf-8'))

    fixes = parse_changes(a.changes, week)
    data = diff(prev, cur) if prev else {'added': [], 'removed': [], 'merged': [], 'confidence_up': [], 'tier_moves': [],
                                         'bids': {'new': 0, 'won': [], 'lost': []}, 'clients': {'new': 0, 'lost': 0},
                                         'totals': {'orgs': len(cur['stakeholders']), 'tenders': len(cur.get('bids', {})), 'clients': len(cur.get('eh_clients', [])) or None}}
    sources = json.loads(a.sources) if a.sources else [
        {'name': 'EH stakeholder workbook (EH_Stakeholder_Competitive_Map.xlsx)', 'refreshed': now.isoformat(timespec='minutes')},
        {'name': 'Bid tracker (Google Sheets 2025 / 2026)', 'refreshed': now.isoformat(timespec='minutes')},
        {'name': 'MWAN licence register', 'refreshed': None, 'note': 'refresh date recorded in the workbook'}]
    sources += news_sources(a.hub)
    entry = {'week': week, 'from': wfrom, 'to': wto, 'built': now.isoformat(timespec='minutes'),
             'fixes': fixes, 'data': data, 'sources': sources}

    log = {'weeks': []}
    if os.path.exists(a.out):
        try: log = json.load(open(a.out, encoding='utf-8'))
        except Exception: log = {'weeks': []}
    weeks = [w for w in log.get('weeks', []) if w.get('week') != week]
    # same ISO week rebuilt (hourly workflow): merge data diffs cumulatively, replace fixes with the current CHANGES.md
    old = next((w for w in log.get('weeks', []) if w.get('week') == week), None)
    if old and prev:
        od = old.get('data', {})
        for k in ('added', 'removed', 'merged', 'confidence_up', 'tier_moves'):
            seen = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in data[k]}
            data[k] = data[k] + [x for x in od.get(k, []) if json.dumps(x, sort_keys=True, ensure_ascii=False) not in seen]
        for k in ('won', 'lost'):
            data['bids'][k] += [x for x in od.get('bids', {}).get(k, []) if x not in data['bids'][k]]
        data['bids']['new'] += od.get('bids', {}).get('new', 0)
        data['clients']['new'] += od.get('clients', {}).get('new', 0); data['clients']['lost'] += od.get('clients', {}).get('lost', 0)
    weeks.insert(0, entry)
    weeks.sort(key=lambda w: w['week'], reverse=True)
    log = {'weeks': weeks[:12], 'retention_weeks': 12, 'confidential': True}
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    json.dump(log, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(a.snapshot_out, exist_ok=True)
    json.dump(cur, open(os.path.join(a.snapshot_out, 'snapshot.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'changelog.json written: week {week}, {len(fixes)} fixes, +{len(data["added"])} / -{len(data["removed"])} orgs, '
          f'{len(data["merged"])} merges, {len(data["confidence_up"])} confidence ups, {len(data["tier_moves"])} tier moves')

if __name__ == '__main__':
    main()
