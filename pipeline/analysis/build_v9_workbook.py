"""Rebuild the stakeholder workbook (v9-live) from the live map's embedded data block.

Source : pipeline/analysis/out/map_data_raw.json (extracted from hub/EH_Stakeholder_Map_CURRENT.html)
Output : EH_Stakeholder_Competitive_Map_v9_live.xlsx  (same column order as workbook v4's Stakeholders sheet, plus live-only fields)
"""
import json, os, re, collections, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
raw = json.load(open(os.path.join(OUT, 'map_data_raw.json'), encoding='utf-8'))
nodes = raw['nodes']
BUILT = '2026-11-05'; SYNCED = 'tracker as of 20 Oct 2026 (per map stamp)'

HDR = Font(name='Arial', bold=True, color='FFFFFF'); BODY = Font(name='Arial', size=10)
FILL = PatternFill('solid', fgColor='1F4E5F'); NOTE = Font(name='Arial', size=9, italic=True, color='555555')

def cl_val(n):
    c = n.get('cl')
    if isinstance(c, dict):
        if 'val' in c: return c.get('val')
    return None
def trk_val(n):
    c = n.get('cl')
    return c.get('value') if isinstance(c, dict) and 'bids' in c else None
def cl_kind(n):
    c = n.get('cl')
    if isinstance(c, dict): return 'project revenue' if 'val' in c else 'tracker bids'
    return None
def mw(n, k):
    m = n.get('mw'); return m.get(k) if isinstance(m, dict) else None
def yn(b): return 'Yes' if b else 'No'
def h2h(n, k):
    h = n.get('h2h'); return h.get(k) if isinstance(h, dict) else None

COLS = [  # (header, fn)  — first 28 mirror workbook v4; the rest are live-only fields
    ('Name', lambda n: n['n']), ('Category', lambda n: n['cat']), ('Tier', lambda n: n['tier'] or None), ('Tier (prev)', lambda n: n.get('tier_old')),
    ('Company Type', lambda n: n['typ']), ('Region', lambda n: None if n['rg'] in ('', '—', None) else n['rg']), ('City', lambda n: n['city'] or None), ('Threat', lambda n: n.get('threat') or None),
    ('New Score', lambda n: n.get('sc')), ('Prev Score', lambda n: n.get('sc_old')), ('New Capability', lambda n: n.get('cap')), ('Prev Capability', lambda n: n.get('cap_old')),
    ('Score Driver', lambda n: n.get('drv')), ('Status', lambda n: 'Score floor (Low cf)' if n.get('fl') else ('Analyst score retained' if n.get('pend') else None)),
    ('Confidence', lambda n: n.get('cf') or None), ('Confidence Basis', lambda n: n.get('cf_basis')), ('Services Confirmed', lambda n: n.get('services_confirmed')),
    ('Evidence/Source', lambda n: n.get('evidence')), ('Bids vs EH', lambda n: yn(n.get('bid'))), ('Bid Encounters', lambda n: n.get('bc') or 0),
    ('EH Client', lambda n: yn(n['cat'] == 'EH Clients' or cl_kind(n) == 'project revenue')), ('Client Value (SAR)', cl_val),
    ('Licence Activities', lambda n: n.get('act') or None), ('MWAN Expiry', lambda n: mw(n, 'exp')), ('Days to Expiry', lambda n: mw(n, 'days')),
    ('Licensed Cities', lambda n: ', '.join(mw(n, 'cities') or []) or None), ('Ghost Flag', lambda n: None), ('Notes', lambda n: n.get('notes') or None),
    # live-only
    ('Province', lambda n: n.get('reg') or None), ('Region Basis', lambda n: n.get('region_basis')), ('Bid Flag Basis', lambda n: n.get('bf') or None),
    ('H2H Appearances', lambda n: h2h(n, 'app')), ('H2H Wins vs EH', lambda n: h2h(n, 'wins')), ('H2H Disqualified', lambda n: h2h(n, 'dq')), ('H2H Undercut %', lambda n: h2h(n, 'undercut')),
    ('Client Block Type', cl_kind), ('Tracker Bid Value (SAR)', trk_val), ('Client Years', lambda n: ', '.join(n['cl'].get('years', [])) if isinstance(n.get('cl'), dict) else None),
    ('Client Score', lambda n: n.get('clsc')), ('Client Tier', lambda n: n.get('cltier')), ('Backing', lambda n: n.get('bk')), ('Sector', lambda n: n.get('sec') or None),
    ('Ownership', lambda n: n.get('own')), ('MWAN Licensed', lambda n: yn(n.get('mn'))), ('Mega-project', lambda n: yn(n.get('mp'))), ('Collaborator', lambda n: yn(n.get('collab'))),
    ('Sites', lambda n: n.get('sites')), ('MWAN Vehicles', lambda n: mw(n, 'veh')), ('Licence Titles', lambda n: ' | '.join(mw(n, 'lic') or []) or None),
    ('Last Verified', lambda n: n.get('last_verified')), ('Added (sync)', lambda n: n.get('added')), ('Added From', lambda n: n.get('added_from')), ('Added On', lambda n: n.get('added_on')),
]

wb = Workbook(); ws = wb.active; ws.title = 'Stakeholders'
ws.append([h for h, _ in COLS])
for c in ws[1]: c.font = HDR; c.fill = FILL; c.alignment = Alignment(vertical='center', wrap_text=True)
rows = sorted(nodes, key=lambda n: n['n'].lower())
for n in rows:
    ws.append([f(n) for _, f in COLS])
for r in ws.iter_rows(min_row=2):
    for c in r: c.font = BODY
widths = {'Name': 42, 'Notes': 48, 'Licence Activities': 28, 'Licence Titles': 40, 'Confidence Basis': 36, 'Region Basis': 30, 'Services Confirmed': 30}
for i, (h, _) in enumerate(COLS, 1):
    ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 14)
ws.freeze_panes = 'B2'; ws.auto_filter.ref = ws.dimensions
NR = ws.max_row
C = {h: get_column_letter(i) for i, (h, _) in enumerate(COLS, 1)}
def rng(h): return f"Stakeholders!${C[h]}$2:${C[h]}${NR}"

# ---- Summary (live COUNTIF formulas)
s = wb.create_sheet('Summary')
s['A1'] = f'EH Stakeholder Map — v9-live rebuilt from the published map data block ({BUILT}; {SYNCED})'; s['A1'].font = Font(name='Arial', bold=True, size=12)
s['A2'] = 'All counts are live COUNTIF/COUNTIFS formulas over the Stakeholders sheet.'; s['A2'].font = NOTE
lines = [
    ('Key indicators', None),
    ('Total organisations', f'=COUNTA({rng("Name")})'),
    ('Tier 1', f'=COUNTIF({rng("Tier")},"Tier 1")'), ('Tier 2', f'=COUNTIF({rng("Tier")},"Tier 2")'), ('Tier 3', f'=COUNTIF({rng("Tier")},"Tier 3")'),
    ('Tier 4', f'=COUNTIF({rng("Tier")},"Tier 4")'), ('GOV', f'=COUNTIF({rng("Tier")},"GOV")'), ('No tier (EH Clients)', f'=COUNTBLANK({rng("Tier")})'),
    ('Bid against EH', f'=COUNTIF({rng("Bids vs EH")},"Yes")'), ('Total bid encounters', f'=SUM({rng("Bid Encounters")})'),
    ('Score floor applied', f'=COUNTIF({rng("Status")},"Score floor (Low cf)")'), ('Analyst score retained', f'=COUNTIF({rng("Status")},"Analyst score retained")'),
    ('Score = 0', f'=COUNTIF({rng("New Score")},0)'),
    ('EH clients', f'=COUNTIF({rng("EH Client")},"Yes")'), ('Client value total (SAR)', f'=SUM({rng("Client Value (SAR)")})'),
    ('No region', f'=COUNTBLANK({rng("Region")})'), ('MWAN licence on record', f'=COUNTA({rng("MWAN Expiry")})'),
    ('Licences expiring ≤ 180 days', f'=COUNTIFS({rng("Days to Expiry")},"<=180",{rng("Days to Expiry")},">0")'),
    ('Threat set', f'=COUNTA({rng("Threat")})'), ('Confidence High', f'=COUNTIF({rng("Confidence")},"High")'),
    ('Confidence Medium', f'=COUNTIF({rng("Confidence")},"Medium")'), ('Confidence Low', f'=COUNTIF({rng("Confidence")},"Low")'),
    ('Confidence blank', f'=COUNTBLANK({rng("Confidence")})'),
    ('High confidence with a Confidence Basis', f'=COUNTIFS({rng("Confidence")},"High",{rng("Confidence Basis")},"<>")'),
    ('High confidence with an MWAN licence', f'=COUNTIFS({rng("Confidence")},"High",{rng("MWAN Expiry")},"<>")'),
    (None, None), ('By category', None),
]
for cat in sorted(collections.Counter(n['cat'] for n in nodes)):
    lines.append((cat, f'=COUNTIF({rng("Category")},"{cat}")'))
lines += [(None, None), ('By company type', None)]
for t in sorted(collections.Counter(n['typ'] for n in nodes)):
    lines.append((t, f'=COUNTIF({rng("Company Type")},"{t}")'))
r = 4
for a, b in lines:
    if a: s.cell(r, 1, a).font = Font(name='Arial', bold=(b is None))
    if b: s.cell(r, 2, b).font = BODY
    r += 1
s.column_dimensions['A'].width = 44; s.column_dimensions['B'].width = 16

# ---- Bid Rivals
b = wb.create_sheet('Bid Rivals')
bh = ['Name', 'Category', 'Tier', 'Threat', 'Encounters', 'New Score', 'Prev Score', 'Confidence', 'Score Driver', 'Company Type', 'Region', 'H2H Wins vs EH', 'H2H Undercut %']
b.append(bh)
for n in sorted((n for n in nodes if (n.get('bc') or 0) > 0), key=lambda n: (-(n['bc'] or 0), n['n'])):
    b.append([n['n'], n['cat'], n['tier'], n.get('threat') or None, n['bc'], n.get('sc'), n.get('sc_old'), n.get('cf') or None, n.get('drv'), n['typ'], (None if n['rg'] in ('', '—', None) else n['rg']), h2h(n, 'wins'), h2h(n, 'undercut')])
# ---- Licence Watch (≤ 365 days)
l = wb.create_sheet('Licence Watch')
l.append(['Name', 'Category', 'Tier', 'Bid Encounters', 'MWAN Expiry', 'Days Left', 'Licensed Activities', 'Licensed Cities'])
for n in sorted((n for n in nodes if isinstance(mw(n, 'days'), (int, float)) and mw(n, 'days') <= 365), key=lambda n: mw(n, 'days')):
    l.append([n['n'], n['cat'], n['tier'], n.get('bc') or 0, mw(n, 'exp'), mw(n, 'days'), ' | '.join(mw(n, 'lic') or []), ', '.join(mw(n, 'cities') or [])])
# ---- Analyst override candidates
o = wb.create_sheet('Override Candidates')
o.append(['Name', 'Category', 'Tier', 'New Score', 'Confidence', 'Status', 'Note'])
o.append([None, None, None, None, None, None, 'Competitor rows whose Tier sits above the v2 score band (T1 ≈ 44+, T2 ≈ 34+, T3 ≈ 23+). Listed for confirmation only — excluded from model validation per the prompt.'])
band = {'Tier 1': 40, 'Tier 2': 23, 'Tier 3': 23}
for n in sorted(nodes, key=lambda n: n['n']):
    if 'Competitor' in n['cat'] and n['tier'] in band and (n.get('sc') or 0) < band[n['tier']]:
        o.append([n['n'], n['cat'], n['tier'], n.get('sc'), n.get('cf') or None, 'Analyst score retained' if n.get('pend') else ('Score floor' if n.get('fl') else None), None])
# ---- Possible duplicates
d = wb.create_sheet('Possible Twins')
d.append(['Normalised key', 'Name A', 'Name B', 'Tier A', 'Tier B', 'Category A', 'Category B'])
def norm(x):
    x = x.lower(); x = re.sub(r'[ً-ْـ]', '', x).replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')
    x = re.sub(r'\b(co|company|ltd|limited|est|establishment|llc|for|the|of|and|شركه|شركة|مؤسسه|مؤسسة|المحدوده|المحدودة|فرع)\b', ' ', x)
    x = re.sub(r'[^\w؀-ۿ]+', ' ', x); return re.sub(r'\s+', ' ', x).strip()
g = collections.defaultdict(list)
for n in nodes: g[norm(n['n'])].append(n)
for k, v in g.items():
    if k and len(v) > 1: d.append([k, v[0]['n'], v[1]['n'], v[0]['tier'], v[1]['tier'], v[0]['cat'], v[1]['cat']])
# ---- README
m = wb.create_sheet('README', 0)
for i, t in enumerate([
    'EH Stakeholder & Competitive Map — v9-live (rebuilt)',
    f'Built {BUILT} from the data block embedded in hub/EH_Stakeholder_Map_CURRENT.html (repo strategic-planning-eh/eh-bid-dashboard, commit of 1 Nov 2026 incl. FEAL Arabia Tier 1 + MWAN block).',
    f'Bid fields (Bids vs EH, Bid Encounters, H2H) are as synced into the map: {SYNCED}.',
    'Columns A–AB follow workbook v4\'s Stakeholders layout; columns AC onward are fields that exist only in the live map (province, region basis, head-to-head record, client block, provenance of Oct 2026 additions).',
    'Ghost Flag is empty by design: the two ghost candidates were deleted on 20 Oct 2026.',
    'Status = "Score floor (Low cf)" or "Analyst score retained" reproduces the v4 Status column from the map\'s fl/pend flags.',
    'Client Value (SAR) = the map\'s project-revenue block (val) for EH clients; six rows carry a tracker-bid block instead (see Client Block Type).',
    'Sheets: Stakeholders · Summary (live formulas) · Bid Rivals · Licence Watch (≤ 365 days) · Override Candidates · Possible Twins.',
    'This file is a read-out of the published map, not the master. Changes belong in the pipeline (sync, overrides, aliases) so they survive the next publish.',
], 1):
    m.cell(i, 1, t).font = Font(name='Arial', bold=(i == 1), size=12 if i == 1 else 10)
m.column_dimensions['A'].width = 140
for sh in (b, l, o, d):
    for c in sh[1]: c.font = HDR; c.fill = FILL
    sh.freeze_panes = 'A2'; sh.auto_filter.ref = sh.dimensions
    for col in range(1, sh.max_column + 1): sh.column_dimensions[get_column_letter(col)].width = 18
    sh.column_dimensions['A'].width = 42
path = os.path.join(OUT, 'EH_Stakeholder_Competitive_Map_v9_live.xlsx')
wb.save(path); print(path, 'rows', NR - 1, 'rivals', b.max_row - 1, 'licence', l.max_row - 1, 'overrides', o.max_row - 2, 'twins', d.max_row - 1)
