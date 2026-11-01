"""Parts B–D — conclusions, missing-data register inputs, scoring validation.

Inputs : out/map_data_raw.json (live map), out/bid_data_raw.json (bid dashboard extract, tracker to Aug 2026 — STALE),
         pipeline/aliases.csv, client_aliases.json, ncec_permits_2026.json, ef_report_2025.json, reg_brief.json
Output : out/analysis.json (every number in the report traces here)
"""
import json, os, re, csv, collections, statistics, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out'); PIPE = os.path.dirname(HERE)
N = json.load(open(os.path.join(OUT, 'map_data_raw.json'), encoding='utf-8'))['nodes']
BA = json.load(open(os.path.join(OUT, 'bid_data_raw.json'), encoding='utf-8'))
C = collections.Counter
R = {}

# ---------- name bridging (mirrors sync_bids_to_apps: exact norm → aliases.csv → notes alias → core containment)
def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    s = re.sub(r'[ً-ْـ​-‏]', '', s).replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')
    s = re.sub(r'[^\w؀-ۿ]+', ' ', s); return re.sub(r'\s+', ' ', s).strip()
STOP = {'co', 'company', 'ltd', 'limited', 'est', 'establishment', 'llc', 'for', 'the', 'of', 'and', 'شركه', 'مؤسسه', 'المحدوده', 'فرع', 'مكتب', 'office'}
def core(s): return ' '.join(w for w in norm(s).split() if w not in STOP)
idx = {}
for n in N:
    idx.setdefault(norm(n['n']), n)
    for m in re.findall(r'Alias \(merged duplicate\):\s*([^·|\n]+)', n.get('notes') or ''):
        idx.setdefault(norm(m), n)
with open(os.path.join(PIPE, 'aliases.csv'), encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        if str(r.get('status', '')).lower() in ('approved', 'reviewer', 'auto') and norm(r['map_name']) in idx:
            idx.setdefault(norm(r['tracker_name']), idx[norm(r['map_name'])])
cores = collections.defaultdict(list)
for n in N: cores[core(n['n'])].append(n)
def find(name):
    k = norm(name)
    if k in idx: return idx[k], 'exact/alias'
    c = core(name)
    if c in cores and len(cores[c]) == 1: return cores[c][0], 'core'
    for ck, v in cores.items():
        if len(v) == 1 and len(c) > 12 and (c in ck or ck in c): return v[0], 'containment'
    return None, None
CLIENT_AL = json.load(open(os.path.join(PIPE, 'client_aliases.json'), encoding='utf-8'))
# acronym index: "(NCVC)" in a map name → that record
acr = {}
for n in N:
    for a in re.findall(r'\(([A-Z][A-Z&+ .-]{1,14})\)', n['n']): acr.setdefault(a.strip().upper(), n)
# analyst bridges for tracker labels with no map twin (entity rules from the project; proposed for client_aliases.json — see F2)
HAND = {'Saudi Electricity Company (SEC)': 'Saudi Energy (formerly SEC)', 'Saudi Energy': 'Saudi Energy (formerly SEC)', 'SE': 'Saudi Energy (formerly SEC)',
        'Saline Water Conversion Corp (SWCC)': 'Saudi Water Authority', 'Zakat, Tax & Customs (ZATCA)': 'Zakat, Tax and Customs Authorities',
        'Nat. Center for Vegetation Cover (NCVC)': 'National Center for Vegetation Cover Development & Combating Desertification (NCVC)',
        'Nat. Center for Environmental Compliance (NCEC)': 'National Center for Environmental Compliance Monitoring (NCEC Monitoring)',
        'General Irrigation Corp': 'Saudi Irrigation Organization (SIO)', 'SIRC': 'Saudi Investment Recycling Company (SIRC)', 'Luberef': 'Luberef (Saudi ARAMCO Base Oil Company)',
        'Ministry of Environment, Water & Agriculture': 'Ministry of Environment, Water and Agricultural', 'Imam Abdulaziz Royal Reserve': 'Imam Abdulaziz bin Muhammad Royal Reserve',
        'Gen. Authority for Military Industries (GAMI)': None, 'Military Industries Corp': 'Military Industries Corporation'}
def find_client(name):
    if name in HAND:
        if HAND[name] is None: return None, None
        n, _ = find(HAND[name]); 
        if n: return n, 'hand bridge'
    en = CLIENT_AL.get(name)
    if en:
        n, how = find(en)
        if n: return n, 'client_alias'
    m = re.search(r'\(([A-Z][A-Z&+ .-]{1,14})\)', name)
    if m and m.group(1).strip().upper() in acr: return acr[m.group(1).strip().upper()], 'acronym'
    return find(name)

# ---------- competitors bridge
comp_map = {}
unmatched = []
for c in BA['both']['competitors']:
    n, how = find(c['name'])
    if n: comp_map[c['name']] = n
    else: unmatched.append(c['name'])
R['bridge'] = dict(bid_competitors=len(BA['both']['competitors']), matched=len(comp_map), unmatched=len(unmatched), unmatched_names=unmatched[:40])

# ---------- overrides (excluded from model tests) — band thresholds from observed competitor bands
BAND = {'Tier 1': 40, 'Tier 2': 23, 'Tier 3': 23}
is_comp = lambda n: 'Competitor' in n['cat']
override = {n['n'] for n in N if is_comp(n) and n['tier'] in BAND and (n.get('sc') or 0) < BAND[n['tier']]}
R['overrides'] = sorted(override)
comps = [n for n in N if is_comp(n) and n['n'] not in override]
bc = lambda n: n.get('bc') or 0

# ---------- per-rival record from bid dashboard (stale) joined to map
rec = {}  # map name -> aggregated
for c in BA['both']['competitors']:
    n = comp_map.get(c['name'])
    key = n['n'] if n else c['name']
    r = rec.setdefault(key, dict(map=n is not None, tier=n['tier'] if n else None, cat=n['cat'] if n else None, cf=(n.get('cf') if n else None), rg=(n['rg'] if n else None),
                                 enc=0, wins=0, dq=0, undercut=0, priced_vs=0, names=[]))
    r['enc'] += c['encounters']; r['wins'] += c['wins']; r['dq'] += c['dq']; r['undercut'] += c['undercut'] or 0; r['priced_vs'] += c['priced_vs'] or 0; r['names'].append(c['name'])

# ---------- B1 tier × bid behaviour (map bc = 20 Oct sync; wins/undercut from stale extract)
b1 = {}
for t in ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4']:
    g = [n for n in comps if n['tier'] == t]
    rr = [rec[n['n']] for n in g if n['n'] in rec]
    b1[t] = dict(n=len(g), bid_active=sum(1 for n in g if bc(n) > 0), encounters=sum(bc(n) for n in g),
                 priced_vs=sum(r['priced_vs'] for r in rr), undercut=sum(r['undercut'] for r in rr), has_undercut=sum(1 for r in rr if r['undercut']),
                 beaten_eh=sum(1 for r in rr if r['wins']), low_cf=sum(1 for n in g if n.get('cf') == 'Low'), floored=sum(1 for n in g if n.get('fl')))
R['B1_tier_x_bid'] = b1
R['B1_tier1_never_bid'] = [n['n'] for n in comps if n['tier'] == 'Tier 1' and bc(n) == 0]
R['B1_tier34_beat_or_undercut'] = sorted([(k, r['tier'], r['enc'], r['undercut'], r['priced_vs'], r['wins'], r['cf']) for k, r in rec.items() if r['tier'] in ('Tier 3', 'Tier 4') and (r['wins'] or r['undercut'])], key=lambda x: (-x[5], -x[3]))
R['B1_undercut_by_tier_rate'] = {t: (round(b1[t]['undercut'] / b1[t]['priced_vs'], 2) if b1[t]['priced_vs'] else None) for t in b1}

# ---------- B2 who beats EH: from pricing rows (n_priced>1)
bidlist = {(b['year'], b['sn']): b for b in BA['both']['bidlist']}
prow = [r for r in BA['both']['pricing']['rows'] if r['n_priced'] and r['n_priced'] > 1 and r['eh']]
def gov_type(client):
    n, _ = find_client(client)
    if n:
        if n['cat'] in ('Government Clients & Institutions', 'Regulators & Compliance Bodies') or n['tier'] == 'GOV': return 'government'
        if n.get('mp'): return 'PIF / giga'
        return 'company'
    if re.search(r'هيئة|وزارة|أمانة|المركز الوطني|مؤسسة عامة|بلدية|جامعة|الهيئة|المديرية', client): return 'government'
    return 'company'
under = collections.defaultdict(lambda: dict(below=0, priced=0, tenders=[], svc=C(), ctype=C()))
for r in prow:
    b = bidlist.get((r['year'], r['sn'])); svc = (b['svc'] if b else '') or '(unset)'; ct = gov_type(r['client'])
    for bd in r['bidders']:
        if not bd.get('price') or 'Environmental Horizons' in bd['name']: continue
        n, _ = find(bd['name']); key = n['n'] if n else bd['name']
        u = under[key]; u['priced'] += 1
        if bd['price'] < r['eh']: u['below'] += 1; u['svc'][svc] += 1; u['ctype'][ct] += 1; u['tenders'].append(f"{r['year']}-{r['sn']}")
top = sorted(under.items(), key=lambda kv: (-kv[1]['below'], -kv[1]['priced']))[:15]
R['B2_priced_tenders'] = len(prow)
R['B2_top_undercutters'] = [(k, v['below'], v['priced'], dict(v['svc']), dict(v['ctype']), (find(k)[0] or {}).get('tier'), (find(k)[0] or {}).get('cf')) for k, v in top]
R['B2_svc_of_losses'] = dict(sum((v['svc'] for v in under.values()), C()))
R['B2_ctype_of_losses'] = dict(sum((v['ctype'] for v in under.values()), C()))
R['B2_undercutters_tier'] = dict(C((find(k)[0] or {}).get('tier') or 'not in map' for k, v in under.items() if v['below']))
R['B2_undercutters_cf'] = dict(C((find(k)[0] or {}).get('cf') or 'blank/not in map' for k, v in under.items() if v['below']))

# ---------- B3 concentration
def pareto(vals):
    s = sorted(vals, reverse=True); t = sum(s)
    return dict(total=t, rivals=len(s), once=sum(1 for v in s if v == 1), top10=round(sum(s[:10]) / t, 3), top20=round(sum(s[:20]) / t, 3), top50=round(sum(s[:50]) / t, 3),
                rivals_for_50pct=next(i + 1 for i in range(len(s)) if sum(s[:i + 1]) >= t / 2))
R['B3_map_bc'] = pareto([bc(n) for n in N if bc(n) > 0])
R['B3_bidext'] = pareto([c['encounters'] for c in BA['both']['competitors']])
R['B3_map_rows_vs_rivals'] = dict(map_rows=len(N), competitor_rows=sum(1 for n in N if is_comp(n)), bid_active=sum(1 for n in N if bc(n) > 0), bid_active_3plus=sum(1 for n in N if bc(n) >= 3))

# ---------- B4 price gap
gaps = [r for r in prow if r['gap'] is not None]
def dist(v):
    s = sorted(v); return dict(n=len(s), median=round(statistics.median(s), 1), mean=round(statistics.mean(s), 1), p25=round(s[len(s) // 4], 1), p75=round(s[3 * len(s) // 4], 1), max=round(s[-1], 1), zero_or_lowest=sum(1 for x in s if x <= 0)) if s else dict(n=0)
R['B4_gap_all'] = dist([r['gap'] for r in gaps])
R['B4_gap_by_year'] = {y: dist([r['gap'] for r in gaps if r['year'] == y]) for y in (2025, 2026)}
R['B4_gap_by_svc'] = {s: dist([r['gap'] for r in gaps if ((bidlist.get((r['year'], r['sn'])) or {}).get('svc') or '(unset)') == s]) for s in set(((bidlist.get((r['year'], r['sn'])) or {}).get('svc') or '(unset)') for r in gaps)}
R['B4_gap_by_ctype'] = {s: dist([r['gap'] for r in gaps if gov_type(r['client']) == s]) for s in set(gov_type(r['client']) for r in gaps)}
def band(v): return '<1M' if v < 1e6 else '1–5M' if v < 5e6 else '5–20M' if v < 20e6 else '20M+'
R['B4_gap_by_band'] = {s: dist([r['gap'] for r in gaps if r['eh'] and band(r['eh']) == s]) for s in set(band(r['eh']) for r in gaps if r['eh'])}
R['B4_rank_dist'] = dict(C(r['rank'] for r in gaps))
R['B4_won_when_lowest'] = dict(lowest=sum(1 for r in gaps if r['rank'] == 1), won=sum(1 for r in gaps if r['rank'] == 1 and r['won']), lowest_lost=[f"{r['year']}-{r['sn']}" for r in gaps if r['rank'] == 1 and r['has_winner'] and not r['won']])
R['B4_lost_not_lowest'] = [(f"{r['year']}-{r['sn']}", r['gap'], r['rank'], r['n_priced'], (r['reason'] or '')[:40]) for r in gaps if r['has_winner'] and not r['won']]
R['B4_tenders_with_outcome_and_price'] = sum(1 for r in gaps if r['has_winner'])

# ---------- B5 client × competitor overlap
clients = {c['name']: c for c in BA['both']['clients']}
lost_by_client = C(b['client'] for b in BA['both']['bidlist'] if b['outcome'] == 'Lost')
bids_by_client = C(b['client'] for b in BA['both']['bidlist'])
won_by_client = C(b['client'] for b in BA['both']['bidlist'] if b['outcome'] == 'Won')
eh_client_issuers = []
for cl in clients:
    n, _ = find_client(cl)
    if n and (n['cat'] == 'EH Clients' or isinstance(n.get('cl'), dict)):
        eh_client_issuers.append((cl, n['n'], bids_by_client[cl], won_by_client[cl], lost_by_client[cl]))
R['B5_issuers_that_are_eh_clients'] = sorted(eh_client_issuers, key=lambda x: -x[2])
R['B5_issuers_matched_to_map'] = sum(1 for cl in clients if find_client(cl)[0])
R['B5_issuers_total'] = len(clients)
R['B5_competitors_that_are_clients'] = [(n['n'], n['cat'], n['tier'], (n['cl'].get('val') if isinstance(n.get('cl'), dict) else None), bc(n)) for n in N if is_comp(n) and isinstance(n.get('cl'), dict)]

# ---------- B6 regional exposure
def client_region(cl):
    n, _ = find_client(cl); return (n['rg'] if n and n['rg'] not in ('', '—') else 'unknown')
R['B6_tenders_by_client_region'] = dict(C(client_region(b['client']) for b in BA['both']['bidlist']).most_common())
R['B6_lost_by_client_region'] = dict(C(client_region(b['client']) for b in BA['both']['bidlist'] if b['outcome'] == 'Lost'))
R['B6_won_by_client_region'] = dict(C(client_region(b['client']) for b in BA['both']['bidlist'] if b['outcome'] == 'Won'))
R['B6_rivals_by_region_tier12'] = dict(C(n['rg'] or 'unknown' for n in comps if n['tier'] in ('Tier 1', 'Tier 2')).most_common())
R['B6_bidactive_rivals_by_region'] = dict(C(n['rg'] or 'unknown' for n in N if bc(n) > 0).most_common())
R['B6_undercutters_by_region'] = dict(C((find(k)[0] or {}).get('rg') or 'unknown' for k, v in under.items() if v['below']))
perm = json.load(open(os.path.join(PIPE, 'ncec_permits_2026.json'), encoding='utf-8'))
R['B6_ncec_permits'] = dict(national=perm.get('national'), regions=perm.get('regions_ytd_2026_min'))

# ---------- B7 licence window
mw = [n for n in N if isinstance(n.get('mw'), dict) and isinstance(n['mw'].get('days'), (int, float))]
R['B7'] = dict(expiring_180=sum(1 for n in mw if 0 < n['mw']['days'] <= 180), expiring_180_bidactive=[(n['n'], n['tier'], bc(n), n['mw']['exp']) for n in mw if 0 < n['mw']['days'] <= 180 and bc(n) > 0],
               expiring_365_tier123=[(n['n'], n['tier'], n['mw']['exp']) for n in mw if 0 < n['mw']['days'] <= 365 and n['tier'] in ('Tier 1', 'Tier 2', 'Tier 3')],
               expired=[(n['n'], n['tier'], n['mw']['exp']) for n in mw if n['mw']['days'] <= 0],
               haz_expiring_180=[(n['n'], n['tier'], n['mw']['exp']) for n in mw if 0 < n['mw']['days'] <= 180 and re.search(r'H-COLL|H-TREAT|H-DISP|HAZ|الخطرة', (n.get('act') or '') + ' '.join(n['mw'].get('lic') or []))])

# ---------- B8 category drift
direct = [n for n in N if n['cat'] == 'Direct Competitors']
act = [n for n in N if n['cat'] == 'Active Competitors']
R['B8'] = dict(direct=len(direct), direct_bidactive=sum(1 for n in direct if bc(n) > 0), direct_mwan=sum(1 for n in direct if n.get('mw') or n.get('mn')),
               direct_haz=sum(1 for n in direct if re.search(r'H-COLL|H-TREAT|H-DISP|H-STOR|HAZ', n.get('act') or '')), direct_no_evidence=sum(1 for n in direct if not (n.get('mw') or n.get('mn')) and bc(n) == 0 and not n.get('services_confirmed')),
               direct_tier=dict(C(n['tier'] for n in direct)), active=len(act), active_bidactive=sum(1 for n in act if bc(n) > 0), active_tier=dict(C(n['tier'] for n in act)),
               indirect_bidactive=sum(1 for n in N if n['cat'] == 'Indirect / Adjacent Competitors' and bc(n) > 0), indirect_beat_or_undercut=sum(1 for k, r in rec.items() if r['cat'] == 'Indirect / Adjacent Competitors' and (r['wins'] or r['undercut'])))

# ---------- B9 movement
mv = [n for n in comps if n.get('tier_old') and n['tier'] != n['tier_old']]
def tier_rank(t): return {'Tier 1': 1, 'Tier 2': 2, 'Tier 3': 3, 'Tier 4': 4}.get(t, 9)
up = [n for n in mv if tier_rank(n['tier']) < tier_rank(n['tier_old'])]; down = [n for n in mv if tier_rank(n['tier']) > tier_rank(n['tier_old'])]
def driver(n):
    if n.get('cf_basis') or n.get('evidence'): return 'research (confidence upgrade)'
    if n.get('fl'): return 'floor rule'
    if bc(n) > 0: return 'bid activity'
    return 'rescoring'
R['B9'] = dict(changed=len(mv), up=len(up), down=len(down), up_driver=dict(C(driver(n) for n in up)), down_driver=dict(C(driver(n) for n in down)),
               up_list=[(n['n'], n['tier_old'], n['tier'], driver(n)) for n in up][:25])

# ---------- B10 buyer side
issuers = []
for cl, c in clients.items():
    n, how = find_client(cl)
    issuers.append(dict(client=cl, map=n['n'] if n else None, cat=n['cat'] if n else None, tier=n['tier'] if n else None, bids=c['bids'], value=c['value'], won=c['eh_won'], awarded=c['awarded'], lost=lost_by_client[cl]))
issuers.sort(key=lambda x: -x['bids'])
R['B10_top_issuers'] = issuers[:15]
R['B10_issuer_tier'] = dict(C(i['tier'] or ('not in map' if not i['map'] else 'no tier') for i in issuers))
R['B10_issuer_cat'] = dict(C(i['cat'] or 'not in map' for i in issuers))
R['B10_never_won_3plus'] = [(i['client'], i['bids'], i['lost'], i['tier']) for i in issuers if i['bids'] >= 3 and i['won'] == 0]
R['B10_issuers_not_in_map'] = [i['client'] for i in issuers if not i['map']]

# ---------- B12 intelligence linkage
ef = json.load(open(os.path.join(PIPE, 'ef_report_2025.json'), encoding='utf-8'))
ef_st = ef.get('stakeholders') or []
def ef_name(s): return s.get('name_en') or s.get('name') or s.get('en') or json.dumps(s, ensure_ascii=False)[:40]
ef_link = [(ef_name(s), bool(find(ef_name(s))[0])) for s in ef_st] if isinstance(ef_st, list) else []
R['B12_ef_stakeholders'] = dict(n=len(ef_link), in_map=sum(1 for _, b in ef_link if b), missing=[a for a, b in ef_link if not b])
R['B12_added_from'] = dict(C(n.get('added_from') for n in N if n.get('added_from')))
rb = json.load(open(os.path.join(PIPE, 'reg_brief.json'), encoding='utf-8'))
R['B12_reg_briefs'] = len(rb.get('briefs', []))
R['B12_ncec_permits_in_map'] = 'permits-by-region figures exist in ncec_permits_2026.json; no map or tracker field references them'

# ---------- D scoring validation (components reverse-engineered: services=cap, bids=flat 15 if bc>0, backing=bk)
def spearman(x, y):
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]: j += 1
            for k in range(i, j + 1): r[s[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y); mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** .5
    return round(num / den, 3) if den else None
test = [n for n in comps if isinstance(n.get('sc'), (int, float))]
y_bid = [1 if bc(n) > 0 else 0 for n in test]
undercut_set = {k for k, v in under.items() if v['below']}
y_under = [1 if n['n'] in undercut_set else 0 for n in test]
comp_fields = {'services (cap)': [n.get('cap') or 0 for n in test], 'backing (bk)': [n.get('bk') or 0 for n in test], 'mega flag': [1 if n.get('mp') else 0 for n in test],
               'sites': [n.get('sites') or 0 for n in test], 'score ex-bids': [(n.get('sc') or 0) - (15 if bc(n) > 0 and not n.get('fl') else 0) for n in test], 'score v2': [n.get('sc') or 0 for n in test]}
R['D_component_vs_outcome'] = {k: dict(rho_bid_active=spearman(v, y_bid), rho_undercut=spearman(v, y_under)) for k, v in comp_fields.items()}
# lift: P(bid-active | top quartile of component) / base rate
base = statistics.mean(y_bid)
def lift(v):
    thr = sorted(v)[int(len(v) * .75)]; top = [y for x, y in zip(v, y_bid) if x >= thr and thr > 0]
    return round(statistics.mean(top) / base, 2) if top else None
R['D_lift_top_quartile'] = {k: lift(v) for k, v in comp_fields.items()}
R['D_bids_component_flat'] = 'bids component = 15 for any bc ≥ 1 (152/170 rows with bc=1 … 3/3 with bc=9); encounters do not scale the score'
# floor rule
low_bid = [n for n in comps if n.get('cf') == 'Low' and bc(n) > 0]
R['D_floor'] = dict(low_cf_bidactive=len(low_bid), floored=sum(1 for n in low_bid if n.get('fl')), in_tier4=sum(1 for n in low_bid if n['tier'] == 'Tier 4'),
                    undercut_eh=sum(1 for n in low_bid if n['n'] in undercut_set), beat_eh=sum(1 for n in low_bid if rec.get(n['n'], {}).get('wins')),
                    encounters=sum(bc(n) for n in low_bid), bc3plus=sum(1 for n in low_bid if bc(n) >= 3))
# sensitivity: alt A = v2; alt B = bids scaled 10 + 5*min(bc,5) ex floor; alt C = v2 but floor exempts bc>=2
def tier_of(s): return 'Tier 1' if s >= 44 else 'Tier 2' if s >= 34 else 'Tier 3' if s >= 23 else 'Tier 4'
def alt(n, mode):
    cap = n.get('cap') or 0; bk = n.get('bk') or 0; b = bc(n)
    if mode == 'v2': return n.get('sc') or 0
    bids = (15 if b else 0) if mode != 'scaled' else (0 if not b else 10 + 5 * min(b, 5))
    s = cap + bk + bids + (7 if n.get('mp') else 0)
    if mode == 'floor_exempt_bc2' and n.get('fl') and b < 2: return n.get('sc') or 0
    if mode == 'scaled' and n.get('fl') and b == 0: return n.get('sc') or 0
    return s
R['D_sensitivity'] = {m: dict(C(tier_of(alt(n, m)) for n in comps)) for m in ('v2', 'scaled', 'floor_exempt_bc2')}
R['D_sensitivity_moves_up'] = {m: [(n['n'], n['tier'], tier_of(alt(n, m)), bc(n), rec.get(n['n'], {}).get('wins', 0)) for n in comps if tier_rank(tier_of(alt(n, m))) < tier_rank(n['tier']) and bc(n) >= 3][:25] for m in ('scaled', 'floor_exempt_bc2')}
R['D_sensitivity_n_up_bc3'] = {m: sum(1 for n in comps if tier_rank(tier_of(alt(n, m))) < tier_rank(n['tier']) and bc(n) >= 3) for m in ('scaled', 'floor_exempt_bc2')}

json.dump(R, open(os.path.join(OUT, 'analysis.json'), 'w'), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
