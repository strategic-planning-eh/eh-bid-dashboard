#!/usr/bin/env python3
"""extract_saudi_waste.py — reads the GASTAT waste tables into pipeline/saudi_waste_data.json for the "Saudi waste" page.

Sources (pipeline/sources/gastat_waste/, GASTAT public releases, English editions):
  env_stats_2024_en.xlsx   Environment Statistics 2024 — CANONICAL. Section 3 waste tables 3-8 … 3-16; 1-22 region area
  env_stats_2023_en.xlsx   2023 edition — 5-1 region population (2022 census) and earlier vintages for the revisions note
  env_stats_2022_en.xlsx   2022 edition — earlier vintages only
  env_stats_2021_en.xlsx   2021 edition — earlier vintages only
  seea_waste_2024_en.xlsx  SEEA Waste accounts 2023 + 2024 (supply by generating sector, use by destination)

Every cell is read by POSITION from the header rows (merged headers and blank cells shift the order of non-blank values).
Wastewater tables 3-1 … 3-7 are left out on purpose (liquid effluent, outside the solid/hazardous scope).
Usage: python3 extract_saudi_waste.py [source_dir] [out.json]"""
import json, os, re, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'sources', 'gastat_waste')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'saudi_waste_data.json')

# ISO 3166-2 codes, matched to the Natural Earth boundaries embedded in the page
REGIONS = [  # code, EN (GASTAT spelling), AR
    ('SA-01', 'Riyadh', 'الرياض'), ('SA-02', 'Makkah', 'مكة المكرمة'), ('SA-03', 'Madinah', 'المدينة المنورة'),
    ('SA-05', 'Qassim', 'القصيم'), ('SA-04', 'Eastern Region', 'المنطقة الشرقية'), ('SA-14', 'Aseer', 'عسير'),
    ('SA-07', 'Tabuk', 'تبوك'), ('SA-06', 'Hail', 'حائل'), ('SA-08', 'Northern Borders', 'الحدود الشمالية'),
    ('SA-09', 'Jazan', 'جازان'), ('SA-10', 'Najran', 'نجران'), ('SA-11', 'Al-Baha', 'الباحة'), ('SA-12', 'Al-Jouf', 'الجوف')]
ALIAS = {'riyadh': 'SA-01', 'makkah': 'SA-02', 'madinah': 'SA-03', 'qassim': 'SA-05', 'al qassim': 'SA-05',
         'eastern region': 'SA-04', 'aseer': 'SA-14', 'tabuk': 'SA-07', 'tabouk': 'SA-07', 'hail': 'SA-06',
         'northern borders': 'SA-08', 'northern border': 'SA-08', 'jazan': 'SA-09', 'najran': 'SA-10', 'najarn': 'SA-10',
         'al-baha': 'SA-11', 'al baha': 'SA-11', 'al bahah': 'SA-11', 'al-jouf': 'SA-12', 'al-jowf': 'SA-12'}

def rcode(s):
    k = re.sub(r'\s+', ' ', str(s or '')).strip().lower()
    return ALIAS.get(k)

def num(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    s = str(v).strip().replace(',', '')
    if s in ('', '-', 'N/A', 'NA', '..'): return None
    try: return float(s)
    except ValueError: return None

def clean(s): return re.sub(r'\s+', ' ', str(s or '').replace('🛈', '')).strip(' .:')

def year_table(ws):
    """Find the header row of years, then return [(labels..., {year: value})] for the rows beneath.
    labels = the text cells left of the first year column; empty label cells inherit the row above (merged cells)."""
    hdr = None
    for r in ws.iter_rows(min_row=1, max_row=15):
        ys = {c.column: int(c.value) for c in r if isinstance(c.value, (int, float)) and 1990 <= c.value <= 2035}
        if len(ys) >= 2: hdr = (r[0].row, ys); break
    if not hdr: raise ValueError(f'{ws.title}: no year header')
    hrow, ycols = hdr; first = min(ycols)
    out, carry = [], {}
    for r in ws.iter_rows(min_row=hrow + 1):
        cells = {c.column: c.value for c in r if not isinstance(c, openpyxl.cell.cell.MergedCell)}
        lab = []
        for col in range(1, first):
            v = cells.get(col)
            if isinstance(v, str) and v.strip() and not re.fullmatch(r'(Ton|Tons|Cubic meters|Percentage|Million.*)', v.strip()):
                carry[col] = clean(v)
                for k in [k for k in carry if k > col]: carry.pop(k)       # a new parent label resets its children
            lab.append(carry.get(col, ''))
        vals = {y: num(cells.get(col)) for col, y in ycols.items()}
        if all(v is None for v in vals.values()): continue
        if any(l.startswith('Source') for l in lab): break
        out.append(([l for l in lab if l], vals))
    return out

def wb(name): return openpyxl.load_workbook(os.path.join(SRC, name), data_only=True)

E24, E23, E22, E21, SE = (wb('env_stats_2024_en.xlsx'), wb('env_stats_2023_en.xlsx'), wb('env_stats_2022_en.xlsx'),
                          wb('env_stats_2021_en.xlsx'), wb('seea_waste_2024_en.xlsx'))
D = {'meta': {'sources': {
        'env2024': 'GASTAT, Environment Statistics 2024 (English edition)',
        'env2023': 'GASTAT, Environment Statistics 2023 (English edition)',
        'env2022': 'GASTAT, Environment Statistics 2022 (English edition)',
        'env2021': 'GASTAT, Environment Statistics 2021 (English edition)',
        'seea': 'GASTAT, SEEA Waste accounts 2024 (English edition)'},
     'regions': [{'code': c, 'en': e, 'ar': a} for c, e, a in REGIONS]}}

def series(rows, *match):
    for lab, vals in rows:
        if all(any(m.lower() in l.lower() for l in lab) for m in match): return {str(k): v for k, v in vals.items()}
    raise KeyError(match)

# ---- municipal: national total (3-8), by region and material (3-9), by region and treatment (3-10)
D['municipal_total'] = {'src': 'env2024:3-8', 'unit': 't', 'v': series(year_table(E24['3-8']), 'municipal')}
MAT = {'paper': 'Paper', 'fabric': 'Fabric', 'plastic': 'Plastic', 'glass': 'Glass', 'metal': 'Metal',
       'other': 'Other non-organic', 'organic': 'Organic', 'total': 'Total'}
def by_region(rows, keymap):
    res = {}
    for lab, vals in rows:
        if len(lab) < 2: continue
        code = rcode(lab[0]) or ('KSA' if lab[0].lower().startswith('total') else None)
        if not code: continue
        k = next((k for k, m in keymap.items() if lab[-1].lower().startswith(m.lower())), None)
        if not k: continue
        res.setdefault(code, {})[k] = {str(y): v for y, v in vals.items()}
    return res
D['municipal_by_material'] = {'src': 'env2024:3-9', 'unit': 't', 'v': by_region(year_table(E24['3-9']), MAT)}
TRT = {'recycling': 'Recycling', 'incineration': 'Pressing', 'landfill': 'Sanitary landfilling', 'total': 'Total'}
rows310 = year_table(E24['3-10'])
# the national block of 3-10 is labelled "Total disposal methods" + method, and a last "Total" row
fix = []
for lab, vals in rows310:
    if lab and lab[0].lower().startswith('total') and len(lab) == 1: lab = ['Total', 'Total']
    fix.append((lab, vals))
D['municipal_by_treatment'] = {'src': 'env2024:3-10', 'unit': 't', 'v': by_region(fix, TRT)}

# ---- industrial waste, Jubail and Yanbu (3-11, 3-12), recycling (3-13, 3-14)
D['jy_total'] = {'src': 'env2024:3-11', 'unit': 't', 'v': series(year_table(E24['3-11']), 'industrial')}
r312 = year_table(E24['3-12'])
D['jy_methods'] = {'src': 'env2024:3-12', 'unit': 't', 'v': {
    'all': {'incineration': series(r312, 'Total waste', 'Incineration'), 'burial': series(r312, 'Total waste', 'Backfilling'),
            'recycling': series(r312, 'Total waste', 'cycling')},
    'hazardous': {'incineration': series(r312, 'Hazardous', 'Incineration'), 'burial': series(r312, 'Hazardous', 'Backfilling'),
                  'recycling': series(r312, 'Hazardous', 'cycling')},
    'nonhazardous': {'burial': series(r312, 'Non-hazardous', 'Backfilling')}}}
r313 = year_table(E24['3-13']); r314 = year_table(E24['3-14'])
D['recycled'] = {'src': 'env2024:3-13', 'unit': 't', 'v': {'jy': series(r313, 'industrial'), 'municipal': series(r313, 'Municipal')}}
D['recycling_rate'] = {'src': 'env2024:3-14', 'unit': 'share', 'v': {'jy': series(r314, 'industrial'), 'municipal': series(r314, 'municipal')}}

# ---- earlier editions, for the revisions note
D['revisions'] = {
    'jy_total': {'env2023': series(year_table(E23['3-11']), 'industrial'), 'env2022': series(year_table(E22['3-10']), 'industrial'),
                 'env2021': series(year_table(E21['3.3.2.c.1']), 'industrial')},
    'municipal_total': {'env2023': series(year_table(E23['3-8']), ''), 'env2022': series(year_table(E22['3-7']), ''),
                        'env2021': {k: (v * 1000 if v is not None else None) for k, v in series(year_table(E21['3.3.2.a.1']), 'municipal').items()}}}

# ---- denominators: population 2022 census (2023 edition 5-1), area (2024 edition 1-22)
pop = {}
for lab, vals in year_table(E23['5-1']):
    c = rcode(lab[0]) if lab else None
    if c: pop[c] = vals[2022]
    elif lab and lab[0].lower().startswith('total'): pop['KSA'] = vals[2022]
D['population_2022'] = {'src': 'env2023:5-1', 'v': pop}
area = {}
for r in E24['1-22'].iter_rows(min_row=5):
    c = rcode(r[1].value)
    if c and num(r[3].value): area[c] = num(r[3].value)
    elif r[1].value and str(r[1].value).strip().lower() == 'total': area['KSA'] = num(r[3].value) or num(r[2].value)
D['area_km2'] = {'src': 'env2024:1-22', 'v': area}

# ---- SEEA accounts (by cell position: see the header rows of 1-1/1-2)
SUP = {'C': 'waste_sector', 'D': 'agriculture', 'E': 'mining', 'F': 'manufacturing', 'G': 'electricity', 'H': 'construction',
       'I': 'other_economic', 'J': 'households', 'K': 'total', 'L': 'imports'}
USE = {'C': 'landfill', 'D': 'specialised_company', 'E': 'other_disposal', 'F': 'recycling_msw', 'G': 'rec_agriculture',
       'H': 'rec_mining', 'I': 'rec_manufacturing', 'J': 'rec_electricity', 'K': 'rec_construction', 'L': 'rec_other_economic',
       'M': 'households', 'N': 'total', 'O': 'exports'}
TYPES = [('paper', 'Paper'), ('plastic', 'Plastic'), ('metal', 'Metal'), ('textiles', 'Textiles'), ('organic', 'Organic'),
         ('construction', 'Construction'), ('wood', 'wood'), ('glass', 'glass'), ('hazardous_medical', 'Hazardous medical'),
         ('hazardous', 'Hazardous waste'), ('ewaste', 'Electronic'), ('sludge', 'Sewage'), ('slaughter', 'Slaughterhouse'),
         ('tyres', 'tires'), ('other', 'Other waste'), ('misc', 'Miscellaneous'), ('fines', 'Fines'), ('total', 'Total')]
def seea(ws, cols):
    out = {}
    for r in ws.iter_rows(min_row=5):
        a = clean(r[0].value)
        if not a: continue
        key = next((k for k, m in TYPES if a.lower().startswith(m.lower())), None)
        if not key or key in out: continue
        cells = {c.column_letter: c.value for c in r if not isinstance(c, openpyxl.cell.cell.MergedCell)}
        out[key] = {name: num(cells.get(col)) for col, name in cols.items()}
    return out
D['seea'] = {'src': 'seea', 'unit': 't',
             'supply': {'2023': seea(SE['1-1'], SUP), '2024': seea(SE['2-1'], SUP)},
             'use': {'2023': seea(SE['1-2'], USE), '2024': seea(SE['2-2'], USE)}, 'summary': {}}
for r in SE['Summary'].iter_rows(min_row=1):
    v = [c.value for c in r]
    if len(v) >= 5 and isinstance(v[1], str) and num(v[3]) is not None:
        D['seea']['summary'][clean(v[1])] = {'unit': clean(v[2]), '2023': num(v[3]), '2024': num(v[4])}

json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', OUT)
