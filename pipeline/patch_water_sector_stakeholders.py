"""patch_water_sector_stakeholders.py — the Saudi water sector's operators on the Stakeholder Map (20 Oct 2026).

Source: "The water sector in the Kingdom of Saudi Arabia — who governs, who regulates, who operates" (Rafa, Oct 2026),
compiled from the Saudi Water Authority's register of licensed facilities and public announcements. Every organisation
the chart names is checked against the map:

  • 24 new records — SWPC and the Saudi Irrigation Organization (Government Clients & Institutions, tier GOV); the SWA-group
    operators WTTCO and Water Solutions Co.; Marafiq's Tawreed and JWAP; the eleven IWPP/IWP producers selling to SWPC
    (Shuaibah ×4, Rabigh ×2, Shuqaiq, Jazlah, Jubail International, Yanbu International, Taif); and the seven ISTP
    developers (Metito, Mowah, Orascom, Gulf Amwal, Acciona, Tawzea, Tamasuk). Potential clients: desalination and
    sewage plants generate brine, sludge, spent membranes and treatment-chemical waste — EH service lines.
    Confidence Medium (official register via a secondary compilation; CR/LEI not yet checked).
  • Existing records get a dated sector-role note and the chart's name as an alias: MEWA, SWA, NWC, Neom, Marafiq (Arabic
    record), Shuqaiq Third Water Co. (Arabic client record, region filled: Southern Region / Al Shuqaiq), Kindasa, SAWACO,
    Red Sea Utilities (Consortium), Veolia Middle East.
  • Nothing is merged here. Two possible twins are left for Youssef's review workbook: "Red Sea Utilities Consortium" ↔
    "شركة مرافق البحر الاحمر المشتركة للطاقة" and "Veolia Middle East Environmental Services" ↔ "فيوليا ميديل ايست للخدمات البيئية".

Run once: python3 pipeline/patch_water_sector_stakeholders.py [--map hub/EH_Stakeholder_Map_CURRENT.html]
                                                              [--workbook IN.xlsx --out OUT.xlsx]
"""
import argparse, json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SRC = 'SWA water-sector structure chart (Oct 2026)'
MARK = SRC
EHA = 'EH angle: brine, sludge, spent membranes and treatment-chemical waste streams.'
IWPP = f'{SRC}: independent water (and power) producer selling to SWPC under a long-term purchase agreement; licensed by SWA. {EHA}'
ISTP = (f'{SRC}: developer in an independent sewage treatment plant (ISTP) consortium — build-own-operate-transfer contracts '
        'tendered by SWPC with the National Water Company as offtaker. ')
CLI, GOVC = 'Clients / Potential Clients', 'Government Clients & Institutions'
UW = 'Utilities & Water'

def al(*names): return ' '.join(f'Alias (merged duplicate): {x}.' for x in names)

# ---------------------------------------------------------------- new records
NEW = [
 # name, cat, tier, typ, sec, region, city, note, aliases
 ('Saudi Water Partnership Company (SWPC)', GOVC, 'GOV', 'GOV-ENTITY', UW, 'Riyadh', 'Riyadh',
  f'{SRC}: owned by the Ministry of Finance; the principal offtaker buying water and wastewater services from producers, and the body that tenders IWPP, IWP, independent-reservoir and ISTP contracts. EH angle: SWPC project companies are the plant owners EH would serve; SWPC tender documents set the environmental obligations of each plant.',
  ['الشركة السعودية لشراكات المياه', 'SWPC']),
 ('Saudi Irrigation Organization (SIO)', GOVC, 'GOV', 'GOV-ENTITY', UW, 'Riyadh', 'Riyadh',
  f'{SRC}: transports, distributes and sells treated water for reuse (regulated by MEWA and SWA). EH angle: reuse networks and irrigation reservoirs generate sludge and monitoring work.',
  ['المؤسسة العامة للري', 'SIO']),
 ('Water Transmission & Technologies Co. (WTTCO)', CLI, 'Tier 2', 'Other', UW, 'Riyadh', 'Riyadh',
  f'{SRC}: operates the Kingdom\'s main water transmission lines and strategic storage (SWA group), regulated by SWA with SWPC as offtaker. EH angle: pipeline and reservoir maintenance waste, tank cleaning sludge, Kingdom-wide sites.',
  ['الشركة السعودية لنقل وتقنيات المياه', 'WTTCO']),
 ('Water Solutions Co. (WSM)', CLI, 'Tier 2', 'Other', UW, 'Riyadh', 'Riyadh',
  f'{SRC}: PIF-owned; manages desalination and purification plants. {EHA}',
  ['شركة حلول المياه', 'WSM']),
 ('Tawreed (Marafiq distribution arm)', CLI, 'Tier 2', 'Other', UW, 'Eastern Province', 'Jubail',
  f'{SRC}: water distribution in Jubail and Yanbu under Marafiq (see شركه مرافق الكهرباء والمياه بالجبيل وينبع, an EH client). EH angle: network maintenance waste in the two industrial cities.',
  ['توريد']),
 ('Jubail Water & Power Co. (JWAP)', CLI, 'Tier 2', 'Other', UW, 'Eastern Province', 'Jubail',
  f'{SRC}: independent water and power producer in Jubail, Marafiq group. {EHA}',
  ['شركة الجبيل للمياه والطاقة', 'JWAP']),
 ('Shuaibah Water & Electricity Co.', CLI, 'Tier 2', 'Other', UW, 'Other Makkah Region', 'Shuaibah', IWPP, ['شركة الشعيبة للمياه والكهرباء', 'SWEC']),
 ('Shuaibah Expansion Project Co.', CLI, 'Tier 2', 'Other', UW, 'Other Makkah Region', 'Shuaibah', IWPP, ['شركة مشروع توسعة الشعيبة']),
 ('Shuaibah Second Water Development Co.', CLI, 'Tier 2', 'Other', UW, 'Other Makkah Region', 'Shuaibah', IWPP, ['شركة مشروع تطوير مياه الشعيبة الثانية']),
 ('Shuaibah Three Water Desalination Co.', CLI, 'Tier 2', 'Other', UW, 'Other Makkah Region', 'Shuaibah', IWPP, ['شركة الشعيبة الثالثة لتحلية المياه']),
 ('Rabigh Arabian Water & Electricity Co.', CLI, 'Tier 2', 'Other', UW, 'Rabigh', 'Rabigh',
  IWPP + ' Sits in EH\'s home industrial cluster beside the Al-Juhfah complex.', ['الشركة العربية للمياه والكهرباء برابغ', 'RAWEC']),
 ('Rabigh Third Co.', CLI, 'Tier 2', 'Other', UW, 'Rabigh', 'Rabigh',
  IWPP + ' Sits in EH\'s home industrial cluster beside the Al-Juhfah complex.', ['شركة رابغ الثالثة']),
 ('Shuqaiq Water & Electricity Co.', CLI, 'Tier 2', 'Other', UW, 'Southern Region', 'Al Shuqaiq', IWPP, ['شركة الشقيق للمياه والكهرباء', 'SqWEC']),
 ('Jazlah Water Desalination Co.', CLI, 'Tier 2', 'Other', UW, 'Eastern Province', 'Jubail', IWPP, ['شركة جزلة لتحلية المياه']),
 ('Jubail International Co.', CLI, 'Tier 2', 'Other', UW, 'Eastern Province', 'Jubail', IWPP, ['شركة الجبيل الدولية']),
 ('Yanbu International Water Co.', CLI, 'Tier 2', 'Other', UW, 'Madinah Region', 'Yanbu', IWPP, ['شركة ينبع الدولية للمياه']),
 ('Taif Independent Water Plant Co.', CLI, 'Tier 2', 'Other', UW, 'Other Makkah Region', 'Taif', IWPP, ['شركة الطائف المستقلة لمحطة المياه']),
 # ISTP developers
 ('Metito', CLI, 'Tier 3', 'Other', UW, 'GCC / International', 'Dubai',
  ISTP + 'Dammam West ISTP with Mowah and Orascom. International water-treatment contractor and operator (HQ Dubai) with a Saudi arm.', ['ميتيتو']),
 ('Mowah', CLI, 'Tier 3', 'Other', UW, 'Riyadh', 'Riyadh',
  ISTP + 'Dammam West ISTP with Metito and Orascom. Saudi water-infrastructure developer and operator.', ['مواه', 'شركة مواه']),
 ('Orascom Construction', CLI, 'Tier 3', 'Other', UW, 'GCC / International', 'Cairo',
  ISTP + 'Dammam West ISTP with Metito and Mowah. Egyptian engineering and construction group.', ['أوراسكوم', 'Orascom']),
 ('Gulf Amwal (أموال الخليج)', CLI, 'Tier 3', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  ISTP + 'Jeddah Airport 2 ISTP with Marafiq and Veolia. Saudi investor in the consortium.', ['أموال الخليج']),
 ('Acciona', CLI, 'Tier 3', 'Other', UW, 'GCC / International', 'Madrid',
  ISTP + 'Madinah 3, Buraydah 2 and Tabuk 2 ISTPs with Tawzea and Tamasuk. Spanish infrastructure and water group; also a desalination EPC contractor in the Kingdom.', ['أكسيونا']),
 ('Tawzea (International Water Distribution Co.)', CLI, 'Tier 3', 'Other', UW, 'Riyadh', 'Riyadh',
  ISTP + 'Madinah 3, Buraydah 2 and Tabuk 2 ISTPs with Acciona and Tamasuk. Saudi water distribution and treatment operator.', ['توزيع', 'الشركة الدولية لتوزيع المياه']),
 ('Tamasuk', CLI, 'Tier 3', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  ISTP + 'Madinah 3, Buraydah 2 and Tabuk 2 ISTPs with Acciona and Tawzea. Saudi infrastructure investor and developer.', ['تماسك']),
]

# ---------------------------------------------------------------- notes on existing records (exact map names) → (note, aliases, field updates)
UPD = {
 'Ministry of Environment, Water and Agricultural': (f'{SRC}: umbrella ministry of the water sector — policy, strategy and legislation; the Minister chairs the boards of the Saudi Water Authority and the National Water Company.', ['MEWA'], {}),
 'Saudi Water Authority': (f'{SRC}: the sector regulator (formerly the Saline Water Conversion Corporation) — licensing, standards and planning for every stage from production to reuse; its Production Arm operates the government desalination plants. EH angle: SWA licensing conditions drive the environmental obligations of every plant on the map.', ['SWA', 'المؤسسة العامة لتحلية المياه المالحة'], {}),
 'National Water Company': (f'{SRC}: PIF-owned; distributes urban water through six regional clusters, runs the Kingdom\'s sewer networks and treatment plants, holds a strategic-storage licence in its regions, sells treated water from its plants, and is the offtaker of the ISTP contracts.', ['NWC', 'شركة المياه الوطنية'], {}),
 'Neom': (f'{SRC}: licensed desalination producer and water distributor within NEOM.', [], {}),
 'شركه مرافق الكهرباء والمياه بالجبيل وينبع': (f'{SRC}: Marafiq — power and water utility of Jubail and Yanbu: desalination producer (through JWAP), distributor (through Tawreed) and operator of the two cities\' industrial and municipal sewerage; partner in the Jeddah Airport 2 ISTP with Veolia and Gulf Amwal.', ['Marafiq', 'Power & Water Utility Co. for Jubail & Yanbu'], {}),
 'شركه الشقيق الثالثه للمياه': (f'{SRC}: Shuqaiq Third Water Co. — independent water producer (IWP) at Al Shuqaiq, Jazan, selling to SWPC; already an EH client (oil-spill response, support services). {EHA}', ['Shuqaiq Third Water Co.', 'Shuqaiq 3'], {'rg': 'Southern Region', 'city': 'Al Shuqaiq', 'sec': UW}),
 'شركة كنداسة لخدمات المياه (Kindasa Water Services)': (f'{SRC}: private desalination producer licensed by SWA.', ['Kindasa'], {}),
 'شركة سواكو لتحلية المياه (SAWACO Desalination)': (f'{SRC}: private desalination producer licensed by SWA.', ['SAWACO'], {}),
 'Red Sea Utilities Consortium': (f'{SRC}: Red Sea Utilities Co. — private desalination producer licensed by SWA, serving the Red Sea destination. Possible twin of the MWAN-licensed record «شركة مرافق البحر الاحمر المشتركة للطاقة» (Umluj) — left for the twin review.', ['Red Sea Utilities Co.'], {}),
 'Veolia Middle East Environmental Services': (f'{SRC}: Veolia is a partner in the Jeddah Airport 2 ISTP consortium with Marafiq and Gulf Amwal. Possible twin of the MWAN-licensed record «فيوليا ميديل ايست للخدمات البيئية» (Jubail) — left for the twin review.', [], {}),
}

ap = argparse.ArgumentParser(); ap.add_argument('--map', default=os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html'))
ap.add_argument('--workbook'); ap.add_argument('--out')
a = ap.parse_args()
today = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y-%m-%d')

def note_for(base, aliases, existing=''):
    parts = [existing.strip()] if existing.strip() else []
    if base and MARK not in existing: parts.append(base)
    for x in aliases:
        if f'Alias (merged duplicate): {x}.' not in existing: parts.append(f'Alias (merged duplicate): {x}.')
    return ' '.join(parts).strip()

# ---------------------------------------------------------------- map
h = open(a.map, encoding='utf-8').read()
m = re.search(r'(<script id="DATA" type="application/json">)(.*?)(</script>)', h, re.S)
D = json.loads(m.group(2)); nodes = D['nodes']; by = {n['n']: n for n in nodes}
log = []
for name, (base, aliases, fields) in UPD.items():
    n = by.get(name)
    if n is None: sys.exit(f'map record not found: {name}')
    new = note_for(base, aliases, n.get('notes') or '')
    changed = new != (n.get('notes') or '')
    if changed: n['notes'] = new
    for k, v in fields.items():
        if (n.get(k) or '') in ('', '—'): n[k] = v; changed = True
    if changed: log.append(('noted', name, 'sector role' + (' + region' if fields else '')))
added = 0
for name, cat, tier, typ, sec, rg, city, note, aliases in NEW:
    if name in by: continue
    nodes.append({'n': name, 'cat': cat, 'rg': rg, 'city': city, 'reg': '', 'typ': typ, 'sec': sec, 'tier': tier, 'bid': False,
                  'sites': None, 'mn': False, 'mp': False, 'act': '', 'notes': note_for(note, aliases), 'bc': 0, 'bf': '', 'threat': '',
                  'collab': False, 'sc': None, 'cap': None, 'bk': 0, 'cf': 'Medium', 'cf_basis': SRC,
                  'drv': '', 'added_from': SRC, 'added_on': today})
    added += 1; log.append(('added', name, SRC))
payload = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
h = h[:m.start(2)] + payload + h[m.end(2):]
open(a.map, 'w', encoding='utf-8').write(h)
print(f'map: {added} records added, {sum(1 for x in log if x[0]=="noted")} records annotated; nodes now {len(nodes)}')

# ---------------------------------------------------------------- workbook
if a.workbook:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.load_workbook(a.workbook); ws = wb['Stakeholders']
    hdr = {str(c.value or ''): i + 1 for i, c in enumerate(ws[1])}
    rows = {str(ws.cell(i, hdr['Name']).value or '').strip(): i for i in range(2, ws.max_row + 1)}
    WB_FIELD = {'rg': 'Region', 'city': 'City'}
    for name, (base, aliases, fields) in UPD.items():
        r = rows.get(name)
        if not r: print('workbook: not found', name); continue
        c = ws.cell(r, hdr['Notes']); c.value = note_for(base, aliases, str(c.value or ''))
        for k, v in fields.items():
            col = WB_FIELD.get(k)
            if col and col in hdr and not ws.cell(r, hdr[col]).value: ws.cell(r, hdr[col]).value = v
    for name, cat, tier, typ, sec, rg, city, note, aliases in NEW:
        if name in rows: continue
        vals = {'Name': name, 'Category': cat, 'Tier': tier, 'Company Type': typ, 'Region': rg, 'City': city, 'Status': 'Added ' + today,
                'Confidence': 'Medium', 'Confidence Basis': SRC + ' — SWA licensed-facilities register via secondary compilation; CR/LEI not yet checked',
                'Evidence/Source': SRC, 'Bids vs EH': 'No', 'Bid Encounters': 0, 'EH Client': 'No', 'Notes': note_for(note, aliases)}
        r = ws.max_row + 1
        for k, v in vals.items():
            if k in hdr: ws.cell(r, hdr[k]).value = v
    last = ws.max_row
    ws.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(ws.max_column)}{last}"
    if 'Summary' in wb.sheetnames:
        for row in wb['Summary'].iter_rows():
            for x in row:
                if isinstance(x.value, str) and x.value.startswith('='): x.value = re.sub(r'\$(\d{4})\b', lambda mm: f'${last}' if int(mm.group(1)) >= 4000 else mm.group(0), x.value)
    lg = wb['Additions Log'] if 'Additions Log' in wb.sheetnames else wb.create_sheet('Additions Log')
    if lg.max_row == 1 and lg.cell(1, 1).value is None:
        lg.append(['Date', 'Action', 'Record', 'Source / detail'])
        for x in lg[1]: x.font = Font(bold=True, color='FFFFFF'); x.fill = PatternFill('solid', fgColor='1F4E5F')
        for col, w in zip('ABCD', (11, 10, 60, 70)): lg.column_dimensions[col].width = w
    for act, name, src in log: lg.append([today, act, name, src])
    lg.append([today, 'review', 'Red Sea Utilities Consortium ↔ شركة مرافق البحر الاحمر المشتركة للطاقة', 'possible twin — not merged, for twin review'])
    lg.append([today, 'review', 'Veolia Middle East Environmental Services ↔ فيوليا ميديل ايست للخدمات البيئية', 'possible twin — not merged, for twin review'])
    wb.save(a.out or a.workbook); print('workbook saved:', a.out or a.workbook, '| rows', ws.max_row - 1)
