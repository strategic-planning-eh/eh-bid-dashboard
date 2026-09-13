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

Workbook bid flags on companies that do NOT appear in the live rosters are left untouched and counted in the report —
they may come from tenders outside the tracker's scope; whether to clear them is an open decision.

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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', required=True); ap.add_argument('--competitors', required=True); ap.add_argument('--bids')
    ap.add_argument('--decisions', help='twin review workbook (possible_twins.xlsx) with the Decision column filled in; merges become aliases, "Keep separate" pairs are dropped from future twin lists')
    ap.add_argument('--min-encounters', type=int, default=1, help='ignore roster competitors below this many encounters when ADDING new nodes')
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
                    idx[norm(lose)] = tgt; merges += 1
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
            matched.append((c['name'], n['n'], 'twin ' + best[0][1][:60])); twin_matched.append(c['name'])
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

    cleared = 0
    for n in nodes:   # reviewer said "Clear flag": the workbook flag goes, unless the live rosters confirmed the company this run
        if norm(n['n']) in clear_flags and id(n) not in touched and n.get('bid'):
            n['bid'] = False; n['bc'] = 0; n['bf'] = ''; n.pop('h2h', None); n['bid_cleared'] = stamp; cleared += 1
    workbook_only = [n['n'] for n in nodes if n.get('bid') and id(n) not in touched and not n.get('auto_added')]
    # ---- possible twins among workbook-only flags and freshly added nodes, minus pairs the reviewer already decided
    focus = [id(n) for n in nodes if (n.get('bid') and id(n) not in touched) or n.get('auto_added')]
    twin_list = [p for p in twins.find_twins(nodes, focus) if frozenset((norm(p['a']['n']), norm(p['b']['n']))) not in decided_pairs]

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
              'workbook_only_bid_flags': len(workbook_only), 'workbook_only_names': workbook_only, 'reviewer_merges_applied': merges, 'merge_side_chosen_automatically': auto_sides, 'reviewer_flags_cleared': cleared, 'twin_matched_instead_of_added': twin_matched, 'banalytics': ban,
              'possible_twins': [{'a': p['a']['n'], 'b': p['b']['n'], 'score': round(p['score'], 2), 'reason': p['reason']} for p in twin_list],
              'matches': [{'roster': r, 'map': m, 'how': h} for r, m, h in matched], 'changes': [{'map': m, 'from': f, 'to': t} for m, f, t in changed]}
    json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(a.map)), 'bid_sync_report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"bid sync: {len(comps)} roster competitors → {len(matched)} matched to map companies ({len(changed)} counts changed), "
          f"{len(added)} added to the map ({len(twin_matched)} recognised as twins of existing companies instead), "
          f"{len(workbook_only)} workbook-only bid flags left as they were; {len(twin_list)} possible twin pairs listed for review"
          + (f"; {merges} reviewer merges applied" if merges else '') + (f"; {cleared} flags cleared by reviewer" if cleared else '') + '.')
    print('BANALYTICS:', ban)
    if ban.startswith('FAILED'): sys.exit(2)

if __name__ == '__main__':
    main()
