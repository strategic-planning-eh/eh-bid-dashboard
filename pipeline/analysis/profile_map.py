"""Part A — column-by-column profile of the live Stakeholder Map dataset.

Input : hub/EH_Stakeholder_Map_CURRENT.html (embedded <script id="DATA"> block, extracted to out/map_data_raw.json)
Output: out/map_profile.json, out/map_profile.md
Run   : python pipeline/analysis/profile_map.py
"""
import json, collections, statistics, re, os, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
raw = json.load(open(os.path.join(OUT, 'map_data_raw.json'), encoding='utf-8'))
nodes = raw['nodes']
N = len(nodes)
TODAY = date(2026, 11, 1)

FIELDS = {  # key: (label, kind)
    'n': ('Name', 'id'), 'cat': ('Category', 'dim'), 'tier': ('Tier', 'dim'), 'tier_old': ('Tier (prev)', 'dim'),
    'typ': ('Company Type', 'dim'), 'rg': ('Region', 'dim'), 'reg': ('Province', 'dim'), 'city': ('City', 'dim'),
    'region_basis': ('Region basis', 'dim'), 'threat': ('Threat', 'dim'), 'sc': ('Score (v2)', 'num'),
    'sc_old': ('Score (prev)', 'num'), 'cap': ('Capability', 'num'), 'cap_old': ('Capability (prev)', 'num'),
    'drv': ('Score driver', 'dim'), 'fl': ('Score floor flag', 'dim'), 'pend': ('Analyst score retained (pending)', 'dim'),
    'cf': ('Confidence', 'dim'), 'cf_basis': ('Confidence basis', 'text'), 'services_confirmed': ('Services confirmed', 'text'),
    'evidence': ('Evidence/Source', 'text'), 'last_verified': ('Last verified', 'date'),
    'bid': ('Bids vs EH', 'bool'), 'bc': ('Bid encounters', 'num'), 'bf': ('Bid flag basis', 'dim'), 'h2h': ('Head-to-head record', 'struct'),
    'cl': ('EH client (value SAR)', 'num'), 'clsc': ('Client score', 'num'), 'cltier': ('Client tier', 'dim'), 'ctier': ('C-tier', 'dim'),
    'act': ('Licence activities', 'text'), 'mw': ('MWAN licence block', 'struct'), 'sites': ('Sites', 'num'),
    'mn': ('MWAN licensed', 'bool'), 'mp': ('Mega-project flag', 'bool'), 'collab': ('Collaborator flag', 'bool'),
    'bk': ('Backing score', 'num'), 'sec': ('Sector', 'dim'), 'own': ('Ownership', 'dim'),
    'added': ('Added (sync)', 'dim'), 'added_from': ('Added from', 'dim'), 'added_on': ('Added on', 'date'),
    'notes': ('Notes', 'text'),
}

def present(v):
    return v not in (None, '', '—', [], {}, False) if not isinstance(v, (int, float)) or isinstance(v, bool) else True

def present_bool(v):
    return v is not None and v != ''

prof = {}
for k, (label, kind) in FIELDS.items():
    vals = [n.get(k) for n in nodes]
    if kind == 'bool':
        filled = sum(1 for v in vals if present_bool(v)); trues = sum(1 for v in vals if v is True)
        prof[k] = dict(label=label, kind=kind, filled=filled, true=trues, true_rate=round(trues / N, 3))
        continue
    nn = [v for v in vals if v not in (None, '', '—', [], {})]
    entry = dict(label=label, kind=kind, filled=len(nn), fill_rate=round(len(nn) / N, 3))
    if kind in ('dim', 'text', 'id', 'date'):
        c = collections.Counter(str(v)[:60] for v in nn)
        entry['distinct'] = len(c); entry['top'] = c.most_common(8)
        if kind == 'id':
            entry['dupes'] = [(a, b) for a, b in c.items() if b > 1]
    elif kind == 'num':
        nums = [float(v) for v in nn if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if nums:
            s = sorted(nums)
            def p(q): return s[min(len(s) - 1, int(q * len(s)))]
            entry.update(min=s[0], p25=p(.25), median=p(.5), p75=p(.75), p95=p(.95), max=s[-1], mean=round(statistics.mean(s), 2),
                         zeros=sum(1 for x in s if x == 0), distinct=len(set(s)))
            entry['top'] = collections.Counter(s).most_common(6)
    elif kind == 'struct':
        entry['distinct'] = len(set(json.dumps(v, sort_keys=True) for v in nn))
        entry['sample'] = nn[0] if nn else None
    prof[k] = entry

# cross-field checks that Part A must answer
def ct(keyfn):
    return collections.Counter(keyfn(n) for n in nodes)

checks = {}
checks['N'] = N
checks['cat'] = ct(lambda n: n['cat'])
checks['tier'] = ct(lambda n: n['tier'])
checks['tier_x_bid'] = ct(lambda n: (n['tier'], n['bid']))
checks['tier_x_bc_gt0'] = ct(lambda n: (n['tier'], (n['bc'] or 0) > 0))
checks['cf'] = ct(lambda n: n.get('cf'))
# confidence vs evidence: does High mean "has MWAN block"?
hi = [n for n in nodes if n.get('cf') == 'High']
checks['high_cf'] = dict(n=len(hi), with_mw=sum(1 for n in hi if n.get('mw')), with_mn=sum(1 for n in hi if n.get('mn')),
                         with_cf_basis=sum(1 for n in hi if n.get('cf_basis')), with_evidence=sum(1 for n in hi if n.get('evidence')),
                         with_services_confirmed=sum(1 for n in hi if n.get('services_confirmed')),
                         neither_mw_nor_basis=sum(1 for n in hi if not n.get('mw') and not n.get('mn') and not n.get('cf_basis')))
checks['high_cf_basis_top'] = collections.Counter(str(n.get('cf_basis'))[:50] for n in hi if n.get('cf_basis')).most_common(10)
# High without MWAN: what are they?
nm = [n for n in hi if not n.get('mw') and not n.get('mn')]
checks['high_no_mwan_by_cat'] = collections.Counter(n['cat'] for n in nm)
checks['high_no_mwan_notes_top'] = collections.Counter(str(n.get('notes'))[:45] for n in nm).most_common(8)
lo = [n for n in nodes if n.get('cf') == 'Low']
checks['low_cf'] = dict(n=len(lo), bid_active=sum(1 for n in lo if (n['bc'] or 0) > 0), floored=sum(1 for n in lo if n.get('fl')),
                        tier=collections.Counter(n['tier'] for n in lo))
# threat
checks['threat'] = ct(lambda n: n.get('threat') or '(blank)')
checks['threat_x_tier'] = ct(lambda n: (n['tier'], n.get('threat') or '(blank)'))
checks['threat_blank_bidactive'] = sum(1 for n in nodes if not n.get('threat') and (n['bc'] or 0) > 0)
# score
checks['sc_zero'] = sum(1 for n in nodes if (n['sc'] in (0,None)))
checks['sc_zero_x_tier'] = collections.Counter(n['tier'] for n in nodes if (n['sc'] in (0,None)))
checks['floor'] = sum(1 for n in nodes if n.get('fl'))
checks['pend'] = sum(1 for n in nodes if n.get('pend'))
checks['pend_x_tier'] = collections.Counter(n['tier'] for n in nodes if n.get('pend'))
checks['drv'] = ct(lambda n: n.get('drv') or '(blank)')
checks['drv_x_tier'] = ct(lambda n: (n['tier'], n.get('drv') or '(blank)'))
checks['unscored_share'] = round(sum(1 for n in nodes if (n['sc'] in (0,None)) or n.get('fl') or n.get('pend')) / N, 3)
# score bands vs tier (tier thresholds reverse-engineered)
bands = collections.defaultdict(list)
for n in nodes:
    if n['tier'] in ('Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'): bands[n['tier']].append(n['sc'] if isinstance(n['sc'],(int,float)) else 0)
checks['score_range_by_tier'] = {t: (min(v), round(statistics.median(v), 1), max(v), len(v)) for t, v in bands.items()}
# analyst overrides candidate: tier higher than score band suggests — leave for appendix only
# client value
cl = [n['cl'] for n in nodes if isinstance(n.get('cl'), (int, float)) and not isinstance(n.get('cl'), bool)]
checks['client_value'] = dict(n=len(cl), total=sum(cl), top_values=collections.Counter(cl).most_common(8),
                              eq4600=sum(1 for v in cl if v == 4600), under10k=sum(1 for v in cl if v < 10000),
                              share_under10k=round(sum(1 for v in cl if v < 10000) / max(1, len(cl)), 3),
                              top5_share=round(sum(sorted(cl)[-5:]) / max(1, sum(cl)), 3))
checks['eh_clients_total'] = sum(1 for n in nodes if n['cat'] == 'EH Clients')
checks['eh_clients_with_value'] = sum(1 for n in nodes if n['cat'] == 'EH Clients' and isinstance(n.get('cl'), (int, float)))
# region
checks['region_blank'] = sum(1 for n in nodes if n['rg'] in ('', '—', None))
checks['region_blank_x_tier'] = collections.Counter(n['tier'] for n in nodes if n['rg'] in ('', '—', None))
checks['region_blank_x_cat'] = collections.Counter(n['cat'] for n in nodes if n['rg'] in ('', '—', None))
checks['region_blank_bidactive'] = sum(1 for n in nodes if n['rg'] in ('', '—', None) and (n['bc'] or 0) > 0)
checks['region_top'] = ct(lambda n: n['rg'] or '(blank)').most_common(16)
# licence
mw = [n for n in nodes if n.get('mw')]
checks['mwan_block'] = len(mw)
checks['mwan_x_cat'] = collections.Counter(n['cat'] for n in mw)
checks['mwan_x_tier'] = collections.Counter(n['tier'] for n in mw)
checks['mwan_sample'] = mw[0]['mw'] if mw else None
# expiry: find expiry date fields in mw blocks
exp = []
for n in mw:
    b = n['mw']
    txt = json.dumps(b)
    for d in re.findall(r'20\d\d-\d\d-\d\d', txt):
        exp.append(d)
checks['mwan_expiry_dates_found'] = len(exp)
# bid encounters
checks['bid_true'] = sum(1 for n in nodes if n['bid'])
checks['bc_gt0'] = sum(1 for n in nodes if (n['bc'] or 0) > 0)
checks['bid_true_bc0'] = sum(1 for n in nodes if n['bid'] and (n['bc'] or 0) == 0)
checks['bf'] = ct(lambda n: n.get('bf') or '(blank)')
checks['bc_dist'] = collections.Counter((n['bc'] or 0) for n in nodes if (n['bc'] or 0) > 0)
bcs = sorted(((n['bc'] or 0) for n in nodes if (n['bc'] or 0) > 0), reverse=True)
tot = sum(bcs)
checks['bc_pareto'] = dict(total_encounters=tot, rivals=len(bcs), top10_share=round(sum(bcs[:10]) / tot, 3),
                           top20_share=round(sum(bcs[:20]) / tot, 3), top50_share=round(sum(bcs[:50]) / tot, 3))
checks['h2h_present'] = sum(1 for n in nodes if n.get('h2h'))
checks['h2h_sample'] = next((n['h2h'] for n in nodes if n.get('h2h')), None)
# category drift
direct = [n for n in nodes if n['cat'] == 'Direct Competitors']
checks['direct'] = dict(n=len(direct), bid_active=sum(1 for n in direct if (n['bc'] or 0) > 0),
                        with_mwan=sum(1 for n in direct if n.get('mw') or n.get('mn')),
                        with_services_confirmed=sum(1 for n in direct if n.get('services_confirmed')),
                        no_mwan_no_bid_no_services=sum(1 for n in direct if not (n.get('mw') or n.get('mn')) and (n['bc'] or 0) == 0 and not n.get('services_confirmed')),
                        tier=collections.Counter(n['tier'] for n in direct))
active = [n for n in nodes if n['cat'] == 'Active Competitors']
checks['active'] = dict(n=len(active), bid_active=sum(1 for n in active if (n['bc'] or 0) > 0), tier=collections.Counter(n['tier'] for n in active))
# duplicates: exact name, and normalised
def norm(s):
    s = s.lower(); s = re.sub(r'[ً-ْـ]', '', s); s = s.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')
    s = re.sub(r'\b(co|company|ltd|limited|est|establishment|llc|for|the|of|and|شركه|شركة|مؤسسه|مؤسسة|المحدوده|المحدودة|فرع)\b', ' ', s)
    s = re.sub(r'[^\w؀-ۿ]+', ' ', s); return re.sub(r'\s+', ' ', s).strip()
nc = collections.Counter(norm(n['n']) for n in nodes)
checks['exact_dupes'] = [(a, b) for a, b in collections.Counter(n['n'] for n in nodes).items() if b > 1]
checks['norm_dupes'] = [(a, b) for a, b in nc.items() if b > 1 and a][:40]
checks['norm_dupes_n'] = sum(1 for a, b in nc.items() if b > 1 and a)
# added by sync
checks['added'] = ct(lambda n: n.get('added') or '')
checks['added_from'] = ct(lambda n: n.get('added_from') or '')
# region_basis
checks['region_basis'] = ct(lambda n: n.get('region_basis') or '')
# tier_old present share, analyst-retained
checks['eh_rows'] = len(raw['eh'])

def fix(o):
    if isinstance(o,dict): return {str(k):fix(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [fix(v) for v in o]
    return o
json.dump(fix(dict(profile=prof, checks=checks)), open(os.path.join(OUT, 'map_profile.json'), 'w'), ensure_ascii=False, indent=1, default=str)
print(json.dumps(fix(checks), ensure_ascii=False, indent=1, default=str))
