"""merge_feal_arabia.py — Youssef's 1 Nov 2026 decision: FEAL Arabia moves to Tier 1 and its Arabic twin is merged into it.

Why (evidence on file):
  • MWAN licence register, screenshots supplied by Youssef on 1 Nov 2026 — eight licences: hazardous-waste treatment
    (Jeddah, 800 t/day), two final-disposal licences with evaporation ponds at Rabigh–Al-Juhfah (4 × 29,400 m³ and
    3 × 60,000 m³), hazardous-waste storage (504 t), used-oil recycling (Jeddah, 200 t/day), healthcare-waste collection
    (two licences) and a hazardous-waste collection licence for chemicals, sludge, used oil, electronic waste, batteries,
    marine-vessel waste and asbestos with 87 vehicles.
  • Saudi ports tab: "AH Group" in the IMO register is Feal Arabian Industrial Co. — the only company Saudi Arabia declares to
    the IMO as receiving ship waste at the Red Sea ports (Jeddah, both Yanbu ports, Jizan, Duba).
  • Al-Juhfah is EH's own complex.

What changes (same mechanics as merge_water_twins.py):
  – the English record FEAL Arabia Industrial Co. Ltd. is kept; the Arabic record شركة فيل العربية الصناعية المحدوده becomes an alias
    and its licence block is replaced by the full eight-licence block from the screenshots;
  – tier Tier 4 → Tier 1 as an influence-based assignment (like Reviva); confidence Low → High (official MWAN registry);
  – the score stays a pure formula result: only what the licences evidence (hazardous final disposal 6 + treatment 6 +
    storage 6 + transport & containers 2.75 + hazardous-specialisation bonus 3 = 23.75 → 23.8). Workforce, site footprint
    and backing are not evidenced, so they stay at zero rather than being guessed;
  – the two other names MWAN licenses the group under are added as aliases (شركة فيل العربية, شركة مصنع فيل العربية الصناعية);
  – decision written to pipeline/twin_decisions.xlsx and pipeline/aliases.csv so the hourly sync honours it.

Run once: python3 pipeline/merge_feal_arabia.py [--map hub/EH_Stakeholder_Map_CURRENT.html] [--workbook IN.xlsx --out OUT.xlsx]
"""
import argparse, csv, json, os, re, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
KEPT = 'FEAL Arabia Industrial Co. Ltd.'
LOSER = 'شركة فيل العربية الصناعية المحدوده'
EXTRA_NAMES = ['شركة فيل العربية', 'شركة مصنع فيل العربية الصناعية']      # other MWAN licence-holder names of the same group
WHY = ('Same company: FEAL Arabian Industrial Co. (AH Group), Jeddah and Rabigh–Al-Juhfah — eight MWAN licences incl. hazardous '
       'final disposal and treatment; the declared Red Sea ship-waste receiver. Tier 1 by influence. Decided 1 Nov 2026.')
TODAY = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).date()
TR = {'Tier 1': 1, 'GOV': 1, 'Tier 2': 2, 'Tier 3': 3, 'Tier 4': 4}

# (basic activity, sub-activity in Arabic, valid until)  — from the MWAN register screenshots
LIC = [
 ('Treatment of Hazardous Waste', 'معالجة النفايات الخطرة', '2029-10-07'),
 ('Final Disposal of Hazardous Waste', 'إنشاء مردم هندسي للنفايات الخطرة', '2027-07-16'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل نفايات الرعاية الصحية الخطرة', '2029-06-04'),
 ('Establishment of Recycling Facilities', 'إعادة تدوير الزيوت', '2028-10-21'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل نفايات الرعاية الصحية الخطرة', '2028-09-30'),
 ('Final Disposal of Hazardous Waste', 'إنشاء مردم هندسي للنفايات الخطرة', '2028-08-21'),
 ('Storage of Hazardous Waste', 'التخزين المؤقت للنفايات الخطرة', '2028-08-14'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل النفايات الكيميائية', '2028-08-06'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل الحمأة', '2028-08-06'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل نفايات الزيوت المستعملة', '2028-08-06'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل النفايات الإلكترونية والكهربائية', '2028-08-06'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل نفايات البطاريات', '2028-08-06'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل نفايات الوسائط البحرية', '2028-08-06'),
 ('Collection and Transportation of Hazardous Waste', 'جمع ونقل نفايات الإسبستوس', '2028-08-06'),
]
TECH = ['معالجة النفايات الخطرة', 'التخلص من المخلفات الخطرة', 'معالجة والتخلص من المخلفات الخطرة', 'جمع ونقل النفايات الطبية',
        'إعادة تدوير للزيوت المستعملة', 'تخزين الزيوت المستعملة']
CAP = ['معالجة النفايات الخطرة: 800 طن/يوم (جدة)',
       'مردم هندسي (رابغ – الجحفة): 4 برك تبخير بسعة 29,400 متر مكعب لكل بركة؛ الكمية المتوقع استقبالها سنوياً 45,000 متر مكعب',
       'مردم هندسي (رابغ – الجحفة): بركة تبخير رقم 1 و2 و3 بسعة 60,000 متر مكعب لكل بركة',
       'إعادة تدوير الزيوت المستعملة: 200 طن/يوم (جدة)',
       'تخزين مؤقت للزيوت المستعملة: السعة القصوى 504 طن',
       'ترخيصا نقل نفايات الرعاية الصحية: مركبتان وثلاث مركبات']
ACT = 'H-COLL, H-COLL-CHEM, H-COLL-MED, H-COLL-EW, H-COLL-BATT, H-COLL-ASY, NH-COLL-SLUDGE, NH-COLL-OILS, MAR-COLL, H-TREAT, H-DISP, H-LANDFILL, H-STORE'
NOTE_ADD = ('Subsidiary of AH Group of companies (MWAN contact e-mail domain ahgroup-ksa.com). Tier 1 by influence (decision 1 Nov 2026), as for Reviva: '
            'it is the only company Saudi Arabia has declared to the IMO as receiving ship waste at the Red Sea ports (Jeddah, both Yanbu ports, Jizan, Duba — see the Saudi ports tab), '
            'and it holds hazardous-waste final-disposal ponds at Rabigh–Al-Juhfah, the same complex as EH. '
            'The score stays the formula result from MWAN-evidenced services only; workforce, site footprint and backing are not yet evidenced. '
            'MWAN also licenses the group as شركة فيل العربية (Jeddah, treatment 800 t/day) and شركة مصنع فيل العربية الصناعية (Jeddah, used-oil recycling 200 t/day). '
            'Licences read from the MWAN register screenshots supplied 1 Nov 2026.')

ap = argparse.ArgumentParser(); ap.add_argument('--map', default=os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html'))
ap.add_argument('--workbook'); ap.add_argument('--out'); a = ap.parse_args()

exp = min(x[2] for x in LIC); days = (dt.date.fromisoformat(exp) - TODAY).days
MW = {'days': days, 'exp': exp, 'cities': ['جدة', 'رابغ - الجحفة'], 'lic': [f'{b} — {s}' for b, s, _ in LIC], 'tech': TECH, 'cap': CAP, 'veh': 87}

h = open(a.map, encoding='utf-8').read()
m = re.search(r'(<script id="DATA" type="application/json">)(.*?)(</script>)', h, re.S)
D = json.loads(m.group(2)); nodes = D['nodes']; by = {n['n']: n for n in nodes}
kn, ln = by.get(KEPT), by.get(LOSER)
if kn is None: raise SystemExit(f'kept record missing: {KEPT}')
if kn.get('tier') == 'Tier 1' and ln is None and kn.get('mw', {}).get('exp') == exp: raise SystemExit('Already applied — nothing to do.')
before = {k: kn.get(k) for k in ('tier', 'cf', 'sc', 'cap', 'act', 'notes')}
kn['tier_old'] = kn.get('tier') if kn.get('tier') != 'Tier 1' else kn.get('tier_old')
kn['tier'] = 'Tier 1'
kn['cf'] = 'High'; kn['cf_basis'] = 'MWAN licence register (8 licences, read from screenshots 1 Nov 2026)'
kn['sc'] = kn['cap'] = 23.8; kn['bk'] = 0; kn['fl'] = 0; kn['drv'] = 'services'
kn['cap_old2'] = before['cap'] if before['cap'] is not None else 0.0; kn['sc_old2'] = before['sc'] if before['sc'] is not None else 0.0
kn['own'] = 'AH Group of companies'
kn['act'] = ACT; kn['mw'] = MW
kn['city'] = kn.get('city') or 'Rabigh'
kn['notes'] = NOTE_ADD + f' Alias (merged duplicate): {LOSER}.'
if ln is not None:
    if (ln.get('bc') or 0) > (kn.get('bc') or 0): kn['bid'] = True; kn['bc'] = ln['bc']; kn['bf'] = ln.get('bf')
    nodes.remove(ln)
payload = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
h = h[:m.start(2)] + payload + h[m.end(2):]
ml = re.search(r'"' + re.escape(LOSER) + r'":\[([^\]]*)\],?', h)          # the duplicate's map pin goes; FEAL keeps its Rabigh pin
if ml: h = h.replace(ml.group(0), '')
open(a.map, 'w', encoding='utf-8').write(h)
print('map: FEAL', before['tier'], '→ Tier 1; confidence', before['cf'], '→ High; score', before['sc'], '→ 23.8; mw licences', len(MW['lic']), '| nodes now', len(nodes))

# ---- reviewer decision for the sync, and the alias bridges
import openpyxl
wb = openpyxl.load_workbook(os.path.join(HERE, 'twin_decisions.xlsx')); ws = wb['Possible twins']
hdr = [str(c.value or '') for c in ws[1]]; have = {(str(r[1] or '').strip(), str(r[7] or '').strip()) for r in ws.iter_rows(min_row=2, values_only=True)}
if (KEPT, LOSER) not in have and (LOSER, KEPT) not in have:
    r = [None] * len(hdr); r[0] = ws.max_row; r[1] = KEPT; r[7] = LOSER; r[13] = 'High'
    r[14] = 'same company in English and Arabic (MWAN register + ahgroup-ksa.com contact, Nov 2026)'; r[15] = 'Merge → keep A'; r[16] = WHY
    ws.append(r)
wb.save(os.path.join(HERE, 'twin_decisions.xlsx'))
p = os.path.join(HERE, 'aliases.csv'); rows = list(csv.DictReader(open(p, encoding='utf-8-sig')))
known = {(r['tracker_name'], r['map_name']) for r in rows}
for name in [LOSER] + EXTRA_NAMES:
    if (name, KEPT) not in known: rows.append({'tracker_name': name, 'map_name': KEPT, 'method': 'reviewer merge', 'status': 'approved', 'added': TODAY.isoformat()})
with open(p, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['tracker_name', 'map_name', 'method', 'status', 'added']); w.writeheader(); w.writerows(rows)
print('twin_decisions.xlsx and aliases.csv updated')

# ---- workbook (optional)
if a.workbook:
    wb = openpyxl.load_workbook(a.workbook); ws = wb['Stakeholders']
    wc = {str(c.value or ''): i + 1 for i, c in enumerate(ws[1])}
    rows = {str(ws.cell(i, wc['Name']).value or '').strip(): i for i in range(2, ws.max_row + 1)}
    kr, lr = rows.get(KEPT), rows.get(LOSER)
    if kr is None: raise SystemExit('workbook: kept row missing')
    def put(col, v):
        if col in wc: ws.cell(kr, wc[col]).value = v
    put('Tier (prev)', ws.cell(kr, wc['Tier']).value); put('Tier', 'Tier 1'); put('Confidence', 'High')
    put('Confidence Basis', 'MWAN licence register (8 licences, screenshots 1 Nov 2026)')
    put('New Score', 23.8); put('New Capability', 23.8); put('Score Driver', 'services'); put('Status', 'Influence-based Tier 1 (1 Nov 2026)')
    put('Licence Activities', ACT); put('MWAN Expiry', exp); put('Days to Expiry', days); put('Licensed Cities', 'جدة، رابغ - الجحفة')
    put('Notes', NOTE_ADD + f' Alias (merged duplicate): {LOSER}.')
    if lr is not None: ws.delete_rows(lr, 1)
    lg = wb['Additions Log'] if 'Additions Log' in wb.sheetnames else wb.create_sheet('Additions Log')
    lg.append([TODAY.isoformat(), 'merged + Tier 1', f'{LOSER} → {KEPT}', WHY])
    if 'Licence Watch' in wb.sheetnames:
        lw = wb['Licence Watch']
        for i in range(2, lw.max_row + 1):
            if str(lw.cell(i, 1).value or '').strip() == LOSER: lw.cell(i, 1).value = KEPT
    wb.save(a.out or a.workbook); print('workbook saved:', a.out or a.workbook, '| rows', ws.max_row - 1)
