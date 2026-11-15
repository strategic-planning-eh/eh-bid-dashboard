#!/usr/bin/env python3
"""
embed_saudi_map_data.py — fills the Saudi Map (BETA) data block (<script id="SMB">) in the Stakeholder Map.

Runs after sync_bids_to_apps.py on every publish (and once from patch_saudi_map_beta.py for the stored hub copy), because
the sync rewrites the map's company records and the bid figures change with the live tracker. Nothing here is estimated:

  loc      reviewed bidder positions from pipeline/bidder_locations.csv, re-keyed to the CURRENT map record name through the
           same alias folding the sync uses (exact name → "Alias (merged duplicate)" notes → aliases.csv). A tracker bidder
           with no row gets no position — the page lists it under "Location not found" (reason: not yet looked up).
  nl       reviewed bidders that are not pinned, with the reason (city only / no listing found / awaiting decision)
  h        per bidder, from the live Bid & Tender app (BA.both.competitors, folded per map record exactly as the sync folds
           them): [encounters, wins against EH, times priced below EH, priced comparisons]
  rost     per bidder, the tenders it shared with EH — from the per-tender rosters (pipeline/rosters_all.json, present at
           publish) or, when that file is not there, from the priced rosters inside the Bid & Tender app (partial; the page
           then shows "k of n listed"). Never a made-up list.
  t        every tender in the live tracker with its result (won / lost / awaiting / cancelled — read at build time, not
           frozen) and where it is pinned: delivery site named in the title → region named in the title → buyer's head
           office (High/Medium match) → not pinned and counted. Sites and buyers come from pipeline/tender_sites.json.
  v        Vision 2030 project sites, SIRC head office (PIF company) and the EH sites from pipeline/v2030_sites.json.

Usage (CI):  python pipeline/embed_saudi_map_data.py --map site/EH_Stakeholder_Map_CURRENT.html --bids site/EH_Bid_Analysis_CURRENT.html \
                 [--sync-report site/bid_sync_report.json] [--rosters pipeline/rosters_all.json] [--competitors pipeline/competitors_rebuilt.json]
Idempotent. Exit 0 on success; exit 2 if the map has no SMB block (patch_saudi_map_beta.py not applied).
"""
import argparse, csv, json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sync_bids_to_apps import norm

BLOCK = re.compile(r'(<script id="SMB" type="application/json">)(.*?)(</script>)', re.S)
SRC_CODE = {'business listing': 0, 'address supplied by EH': 1, 'own records': 2}
WHY_CODE = {'city only': 'c', 'no listing found': 'n', 'awaiting decision': 'a'}
BIDDER_CAT = 'Active Competitors'

def grab(html, sid):
    m = re.search(r'<script id="%s" type="application/json">(.*?)</script>' % sid, html, re.S)
    return json.loads(m.group(1)) if m else None

def node_index(nodes, aliases_path):
    """normalised spelling -> map record, the way sync_bids_to_apps.py indexes the map"""
    idx = {}
    for n in nodes:
        idx.setdefault(norm(n['n']), n)
        for al in re.findall(r'Alias \(merged duplicate\):\s*([^·\n]+)', n.get('notes') or ''):
            for part in re.split(r'\s*[;,/]\s*|\s+\|\s+', al):
                k = norm(part)
                if k: idx.setdefault(k, n)
    if aliases_path and os.path.exists(aliases_path):
        with open(aliases_path, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                if str(r.get('status', '')).strip().lower() not in ('approved', 'reviewer', 'auto'): continue
                tgt = idx.get(norm(r.get('map_name'))); k = norm(r.get('tracker_name'))
                if tgt is not None and k: idx[k] = tgt
    return idx

def result_of(r):
    o = str(r.get('outcome') or '').strip().lower(); s = str(r.get('status') or '').strip().lower()
    if o == 'won' or (not o and s == 'awarded' and str(r.get('winner') or '').strip().upper() == 'EH'): return 'w'
    if o in ('lost', 'not awarded') or (not o and s == 'not awarded'): return 'l'
    if o == 'cancelled' or s == 'cancelled': return 'c'
    return 'p'          # pending / submitted / no result recorded = awaiting result

def build(map_html, bids_html=None, sync_report=None, rosters=None, competitors=None, aliases=os.path.join(HERE, 'aliases.csv'), quiet=False):
    D = grab(map_html, 'DATA'); nodes = [n for n in D['nodes'] if not n.get('merged_into')]
    idx = node_index(nodes, aliases); warn = []
    bidders = [n for n in nodes if n.get('cat') == BIDDER_CAT and n.get('bid')]
    bidder_names = {n['n'] for n in bidders}

    # ---- bidder positions (reviewed rows survive every publish; keyed by the current record name)
    loc, nl = {}, {}
    with open(os.path.join(HERE, 'bidder_locations.csv'), encoding='utf-8-sig', newline='') as f: rows = list(csv.DictReader(f))
    exact = {n['n']: n for n in nodes}
    for r in rows:
        n = exact.get(r['name']) or idx.get(norm(r['name']))      # the record of that exact name first; else the record its spelling now folds into
        if n is None: continue                                    # no longer on the map (removed, or renamed without an alias)
        nm = n['n']
        if r['status'] == 'Located' and r['lat'] and r['lng']:
            if nm in loc: continue
            loc[nm] = [round(float(r['lat']), 6), round(float(r['lng']), 6), r['address'], SRC_CODE.get(r['source'], 0), 1 if r['precision'] == 'district' else 0]
            nl.pop(nm, None)
        elif nm not in loc:
            nl.setdefault(nm, WHY_CODE.get(r['note'], 'n'))

    # ---- live figures from the Bid & Tender app, folded per map record
    h, rost, rost_src, tenders, stamp = {}, {}, 'none', [], ''
    BA = grab(bids_html, 'BA') if bids_html else None
    both = (BA or {}).get('both') or {}
    roster_to_map = {}
    if sync_report:
        for mt in sync_report.get('matches', []): roster_to_map[norm(mt['roster'])] = mt['map']
    by_name = {n['n']: n for n in nodes}
    def to_node(name):
        k = norm(name)
        if k in roster_to_map and roster_to_map[k] in by_name: return by_name[roster_to_map[k]]
        return idx.get(k)
    for c in both.get('competitors') or []:
        n = to_node(c.get('name'))
        if n is None: continue
        a = h.setdefault(n['n'], [0, 0, 0, 0])
        a[0] += c.get('encounters') or 0; a[1] += c.get('wins') or 0; a[2] += c.get('undercut') or 0; a[3] += c.get('priced_vs') or 0
    # per-tender lists
    if rosters:
        rost_src = 'rosters'
        canon_to_disp = {}
        if competitors:
            from parse_rosters import canon as _canon
            for c in competitors:
                for cn in c.get('canons') or []: canon_to_disp[cn] = c['name']
        else: _canon = None
        for key, bl in rosters.items():
            if not any(x[3] for x in bl): continue                # EH must be on the roster
            for x in bl:
                if x[3]: continue
                n = to_node(x[0])
                if n is None and _canon:
                    d = canon_to_disp.get(_canon(x[0]))
                    if d: n = to_node(d)
                if n is not None and key not in rost.setdefault(n['n'], []): rost[n['n']].append(key)
    elif both.get('pricing', {}).get('rows'):
        rost_src = 'priced'
        for r in both['pricing']['rows']:
            key = f"{r['year']}-{r['sn']}"
            for b in r.get('bidders') or []:
                if b.get('eh'): continue
                n = to_node(b.get('name'))
                if n is not None and key not in rost.setdefault(n['n'], []): rost[n['n']].append(key)
    rost = {k: sorted(v, key=lambda s: tuple(int(x) for x in s.split('-'))) for k, v in rost.items() if k in bidder_names or by_name[k]['n'].startswith('Saudi Investment Recycling')}

    # ---- tenders: live result + where pinned
    TS = json.load(open(os.path.join(HERE, 'tender_sites.json'), encoding='utf-8'))
    buy = {re.sub(r'\s+', ' ', b['client'].replace(' / ', ' ')).strip(): b for b in TS['buyers']}
    counts = {'site': 0, 'region': 0, 'buyer': 0, 'none': 0}
    for r in both.get('bidlist') or []:
        cl = re.sub(r'\s+', ' ', r.get('client') or '').strip(); key = f"{r['year']}-{r['sn']}"
        s = TS['sites'].get(key); b = buy.get(cl); kind, lat, lng, place = 3, None, None, ''
        if s: kind = 1 if s.get('type') == 'region' else 0; lat, lng, place = s['lat'], s['lng'], s.get('place') or s.get('listing') or ''
        elif b and b.get('lat') is not None and b.get('grade') in ('High', 'Medium'): kind, lat, lng, place = 2, b['lat'], b['lng'], re.sub(r',?\s*Saudi Arabia$', '', b.get('address') or b.get('listing') or '')
        counts[('site', 'region', 'buyer', 'none')[kind]] += 1
        tenders.append([r['year'], r['sn'], cl, re.sub(r'\s+', ' ', r.get('title') or '').strip(), result_of(r), kind,
                        round(lat, 6) if lat is not None else None, round(lng, 6) if lng is not None else None, place])
    m = re.search(r'window\.BUILT_ISO="([^"]+)"', bids_html or '')
    if m: stamp = m.group(1)

    # ---- Vision 2030 project sites, SIRC, EH sites
    VS = json.load(open(os.path.join(HERE, 'v2030_sites.json'), encoding='utf-8'))
    v = []
    for s in VS['sites']:
        if s['kind'] == 'project':
            v.append({'k': 'p', 'en': s['en'], 'ar': s.get('ar') or '', 'pa': s.get('parent') or '', 'pa_ar': s.get('parent_ar') or '', 'lat': s.get('lat'), 'lng': s.get('lng'),
                      'st': s.get('status') or '', 's_en': s.get('status_en') or '', 's_ar': s.get('status_ar') or ''})
        elif s['kind'] == 'pif_company':
            v.append({'k': 's', 'en': s['en'], 'ar': s.get('ar') or '', 'node': s.get('node') or '', 'lat': s.get('lat'), 'lng': s.get('lng'), 'addr': s.get('addr') or ''})
        elif s['kind'] == 'eh_site':
            v.append({'k': 'e', 'key': s['key'], 'en': s['en'], 'ar': s.get('ar') or '', 'lat': s.get('lat'), 'lng': s.get('lng'), 'a_en': s.get('addr_en') or '', 'a_ar': s.get('addr_ar') or '',
                      'street': 1 if s.get('precision') == 'street' else 0})

    # ---- reconciliation (printed; the page itself reads the sync's per-company count)
    mism = [(n['n'], n.get('bc'), h[n['n']][0]) for n in bidders if n['n'] in h and h[n['n']][0] != (n.get('bc') or 0)]
    noapp = [n['n'] for n in bidders if n['n'] not in h]
    if BA and mism: warn.append(f"{len(mism)} bidder(s) whose map encounter count differs from the Bid & Tender app (expected 0 after the sync): " + '; '.join(f'{a} map {b} / app {c}' for a, b, c in mism[:6]))
    if BA and noapp: warn.append(f"{len(noapp)} map bidder(s) not found among the Bid & Tender app's competitors (expected 0 after the sync)")
    dup_tenders = [(k, (by_name[k].get('bc') or 0), len(vv)) for k, vv in rost.items() if rost_src == 'rosters' and k in bidder_names and len(vv) < (by_name[k].get('bc') or 0)]
    if dup_tenders: warn.append(f"{len(dup_tenders)} bidder(s) appear under two spellings in the same tender (encounters > distinct tenders): " + '; '.join(f'{a} {b}>{c}' for a, b, c in dup_tenders[:6]))
    payload = {'built': dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%-d %b %Y'), 'looked_up': '15 Nov 2026', 'bid_built': stamp,
               'loc': {k: loc[k] for k in sorted(loc) if k in bidder_names}, 'nl': {k: nl[k] for k in sorted(nl) if k in bidder_names},
               'h': {k: h[k] for k in sorted(h) if k in bidder_names or k in rost}, 'rost': rost, 'rost_src': rost_src, 't': tenders, 'tn': counts, 'v': v}
    located = sum(1 for n in bidders if n['n'] in payload['loc'])
    summary = (f"Saudi Map data: {len(bidders)} bidders, {located} located, {len(bidders) - located} not located "
               f"({sum(1 for n in bidders if n['n'] not in payload['loc'] and n['n'] not in payload['nl'])} not yet looked up); "
               f"{len(tenders)} tenders (delivery site {counts['site']}, region {counts['region']}, buyer head office {counts['buyer']}, not located {counts['none']}); "
               f"tender lists from {rost_src} for {sum(1 for k in rost if k in bidder_names)} bidders; {sum(1 for x in v if x['k'] == 'p' and x['lat'] is not None)} project sites")
    if not quiet:
        print(summary)
        for w in warn: print('  note:', w)
    return payload, summary, warn

def embed(map_html, payload):
    if not BLOCK.search(map_html): return None
    txt = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return BLOCK.sub(lambda m: m.group(1) + txt + m.group(3), map_html, count=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', required=True); ap.add_argument('--bids'); ap.add_argument('--sync-report')
    ap.add_argument('--rosters', default=os.path.join(HERE, 'rosters_all.json')); ap.add_argument('--competitors', default=os.path.join(HERE, 'competitors_rebuilt.json'))
    ap.add_argument('--aliases', default=os.path.join(HERE, 'aliases.csv')); ap.add_argument('--no-rosters', action='store_true', help='ignore rosters_all.json even if present')
    a = ap.parse_args()
    mh = open(a.map, encoding='utf-8').read()
    if not BLOCK.search(mh): print('embed_saudi_map_data: the map has no SMB block — run pipeline/patch_saudi_map_beta.py first'); sys.exit(2)
    bh = open(a.bids, encoding='utf-8').read() if a.bids and os.path.exists(a.bids) else None
    if a.bids and bh is None: print(f'  note: {a.bids} not found — tenders and bid figures left empty')
    rep = json.load(open(a.sync_report, encoding='utf-8')) if a.sync_report and os.path.exists(a.sync_report) else None
    ros = json.load(open(a.rosters, encoding='utf-8')) if (not a.no_rosters and a.rosters and os.path.exists(a.rosters)) else None
    comp = json.load(open(a.competitors, encoding='utf-8')) if a.competitors and os.path.exists(a.competitors) else None
    payload, _, _ = build(mh, bh, rep, ros, comp, a.aliases)
    open(a.map, 'w', encoding='utf-8').write(embed(mh, payload))

if __name__ == '__main__':
    main()
