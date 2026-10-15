"""patch_ef_etimad_stakeholders.py — stakeholders of the Environment Fund 2025 report and the buyers behind relevant Etimad
tenders, on the Stakeholder Map (15 Oct 2026).

  • 25 new records: 13 named in the Environment Fund annual report 2025 (ministries, EXPRO, the Non-Oil Revenue
    Development Center, the guarantee banks, Kafalah, Modon, Saudi Venture Capital, Morgan Stanley) and 12 government
    buyers that published tenders EH could bid for on Etimad (health clusters, hospitals, universities, the Red Crescent,
    the King Fahd Causeway, two municipalities). Category Government Clients & Institutions (tier GOV) or Potential
    Collaborators (banks / investors); confidence Medium (official source).
  • Existing records get a dated, page-referenced note from the report (Environment Fund, MEWA, the five centres, Saudi
    Energy, National Water Company, Soudah, Ma'aden, Social Development Bank, Agricultural Development Fund) and their
    Arabic Etimad name as an alias, so the Government Tenders tab links their tenders to the map.
  • "Enviromental Fund" (a misspelt duplicate of the Environment Fund) is merged.
  • Etimad tender detail is NOT written here: Etimad data never goes into the repo. build_etimad.py adds each buyer's
    relevant tenders to its note on the published map at every publish, from the private sheet.
Board members and departments of the Fund are recorded in the Fund's note (the map holds organisations, not people).

Run once: python3 pipeline/patch_ef_etimad_stakeholders.py [--workbook IN.xlsx --out OUT.xlsx [--etimad-json FILE]]
"""
import argparse, json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MARK = 'Environment Fund annual report 2025'
EF = 'Environment Fund annual report 2025'
ETI = ('Buys services EH offers on Etimad (government tenders platform); the relevant tenders are listed in this note at each '
       'publish and in the Government Tenders tab.')

def al(*names): return ' '.join(f'Alias (merged duplicate): {x}.' for x in names)

# ---------------------------------------------------------------- new records
NEW = [
 # name, cat, tier, typ, sec, region, city, note, aliases
 ('Ministry of Finance', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', '', 'Riyadh', 'Riyadh',
  f'{EF}: the Minister of Finance approved the Fund issuing direct and indirect loan guarantees (p. 55); represented on the Fund\'s board by Haitham Al-Turaif (p. 27).', ['وزارة المالية']),
 ('Ministry of Economy & Planning', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', '', 'Riyadh', 'Riyadh',
  f'{EF}: represented on the Fund\'s board by Hajar Al-Qusayyir (p. 27).', ['وزارة الاقتصاد والتخطيط']),
 ('Expenditure & Projects Efficiency Authority (EXPRO)', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', '', 'Riyadh', 'Riyadh',
  f'{EF}: approved the Fund\'s air, water and soil monitoring projects and its environmental emergency-response project for execution (p. 79); sets the 130-day ceiling the Fund\'s procurement is measured against (p. 96); 35+ workshops with the Fund on the financial plan to 2030 (p. 42). EH angle: monitoring and emergency response are EH service lines.', ['هيئة كفاءة الإنفاق والمشروعات الحكومية', 'EXPRO']),
 ('Non-Oil Revenue Development Center', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', '', 'Riyadh', 'Riyadh',
  f'{EF}: approving the new fee schedules of NCEC (14 licences, 34 services, 4 clearances) and NCW (12 licences, 8 permits) (p. 78). EH angle: paid licensing raises demand for permits done right first time.', ['مركز تنمية الإيرادات غير النفطية']),
 ('Kafalah Programme', 'Potential Collaborators', 'Tier 2', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  f'{EF}: framework agreement for the Fund\'s loan-guarantee product; the Fund\'s first indirect-financing opportunity was approved with Kafalah (p. 14, 55). EH angle: guaranteed, subsidised credit for environmental infrastructure such as a facility expansion.', ['برنامج كفالة']),
 ('Riyad Bank', 'Potential Collaborators', 'Tier 2', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  f'{EF}: one of four framework agreements for the Fund\'s loan-guarantee product (p. 55).', ['بنك الرياض']),
 ('Saudi Awwal Bank (SAB)', 'Potential Collaborators', 'Tier 2', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  f'{EF}: one of four framework agreements for the Fund\'s loan-guarantee product (p. 55).', ['البنك السعودي الأول', 'SAB']),
 ('Alinma Bank', 'Potential Collaborators', 'Tier 2', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  f'{EF}: one of four framework agreements for the Fund\'s loan-guarantee product (p. 55).', ['مصرف الإنماء']),
 ('Saudi National Bank (SNB)', 'Potential Collaborators', 'Tier 3', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  f'{EF}: cooperation agreement with the Fund to widen the reach of its loan-guarantee product (p. 55).', ['البنك الأهلي السعودي']),
 ('Bank AlJazira', 'Potential Collaborators', 'Tier 3', 'Other', 'Finance', 'Jeddah', 'Jeddah',
  f'{EF}: cooperation agreement with the Fund to widen the reach of its loan-guarantee product (p. 55).', ['بنك الجزيرة']),
 ('Saudi Authority for Industrial Cities & Technology Zones (Modon)', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Industrial', 'Riyadh', 'Riyadh',
  f'{EF}: cooperation agreement with the Fund to widen the reach of its loan-guarantee product (p. 55). EH angle: Modon runs the industrial cities, home to many hazardous-waste generators.', ['الهيئة السعودية للمدن الصناعية ومناطق التقنية', 'مدن', 'MODON']),
 ('Saudi Venture Capital (SVC)', 'Potential Collaborators', 'Tier 2', 'Other', 'Finance', 'Riyadh', 'Riyadh',
  f'{EF}: cooperation agreement with the Fund on environmental venture investment, signed under the Minister\'s patronage (p. 46).', ['الشركة السعودية للاستثمار الجريء']),
 ('Morgan Stanley (Environment Fund impact portfolio)', 'Potential Collaborators', 'Tier 3', 'Other', 'Finance', 'GCC / International', '',
  f'{EF}: investment manager of the Fund\'s impact-investment portfolio from January–March 2026, through an account run only for the Fund; its fee is tied to bringing international companies to the Kingdom as well as impact and return (p. 46). EH angle: EH is the kind of local operating partner such investments need.', []),
 # Etimad buyers (Core / Related tenders) not on the map before
 ('Makkah Health Cluster', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Makkah City', 'Makkah', ETI, ['التجمع الصحي بمكة المكرمة']),
 ('Jazan Health Cluster', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Southern Region', 'Jazan', ETI, ['تجمع جازان الصحي']),
 ('Aseer Health Cluster', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Southern Region', 'Abha', ETI, ['تجمع عسير الصحي']),
 ('Madinah Hospital (مستشفى المدينة المنورة)', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Madinah Region', 'Madinah', ETI, ['مستشفى المدينة المنورة']),
 ('Security Forces Hospital, Makkah', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Makkah City', 'Makkah', ETI + ' Part of the Ministry of Interior\'s Security Forces hospitals.', ['مستشفى قوى الأمن بمنطقة مكة المكرمة']),
 ('National Guard Health Affairs', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Riyadh', 'Riyadh', ETI + ' Health arm of the Ministry of National Guard; buys separately from the ministry.', ['الشؤون الصحیة بوزارة الحرس الوطني', 'الشؤون الصحية بوزارة الحرس الوطني']),
 ('Saudi Red Crescent Authority', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Healthcare', 'Riyadh', 'Riyadh', ETI, ['هيئة الهلال الأحمر السعودي']),
 ('Imam Mohammad Ibn Saud Islamic University', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Education', 'Riyadh', 'Riyadh', ETI, ['جامعة الامام محمد بن سعود', 'جامعة الإمام محمد بن سعود الإسلامية']),
 ('Majmaah University', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Education', 'Riyadh', 'Al Majmaah', ETI, ['جامعة المجمعة']),
 ('King Fahd Causeway Authority', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Transport', 'Eastern Province', 'Al Khobar', ETI, ['المؤسسة العامة لجسر الملك فهد']),
 ('Sarat Abidah Governorate Municipality', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Municipalities', 'Southern Region', 'Sarat Abidah', ETI, ['بلدية محافظة سراة عبيدة']),
 ('Qaryat Al-Ulya Governorate Municipality', 'Government Clients & Institutions', 'GOV', 'GOV-ENTITY', 'Municipalities', 'Eastern Province', 'Qaryat Al-Ulya', ETI, ['بلدية محافظة قرية العليا']),
]

# ---------------------------------------------------------------- notes on existing records (exact map names)
UPD = {
 'Environment Fund': (f'{EF} (financial year 1446/47): financing arm of EH\'s regulators — funds the approved budgets of the five national centres (NCEC, MWAN, NCW, NCVC, NCM), runs grants, loan support and direct and indirect loan guarantees (p. 30–31, 55), an impact-investment portfolio managed by Morgan Stanley from January–March 2026 (p. 46), and the list of projects to hand to private partners — 45 studies, 80 waste investment opportunities (p. 76, 83). Procurement for the five centres is being centralised under its shared-services programme: 12 of 33 services live (p. 86–87); its own tender-to-contract time was 83 days in 2025 (p. 96). '
                      'Board: Eng. Abdulrahman Al-Fadhli (Minister of Environment, Water & Agriculture, chair), Dr Osama Faqeeha (vice-chair, MEWA), Haitham Al-Turaif (Ministry of Finance), Hajar Al-Qusayyir (Ministry of Economy & Planning), Abdulrahman Addas, Dr Mohammed Al-Zahrani; acting CEO Munir Al-Sahli (p. 15, 26–27). '
                      'Departments that matter to EH: Incentives & Grants (guarantees, loan support, grants portal), Economic Affairs (investment-opportunity studies), Impact Investments, Shared Services — Procurement & Contracts (p. 87, 92). '
                      'Three private waste projects received Fund grants in 2025 — lead-acid battery recycling (50,000 t), smart recycling stations in Riyadh, an animal-waste plant in Al-Kharj — the report does not name the companies (p. 70–71). EH\'s one tender to the Fund (bid 17/26, sustainability consulting for the national centres) was cancelled.',
                      ['صندوق البيئة', 'Enviromental Fund']),
 'Ministry of Environment, Water and Agricultural': (f'{EF}: the Minister, Eng. Abdulrahman Al-Fadhli, chairs the Fund\'s board and Deputy Minister for Environment Dr Osama Faqeeha is vice-chair (p. 26); the Fund\'s carbon-investment strategy was widened to MEWA\'s water and agriculture sectors (p. 47); Sedrah hackathon run with MEWA\'s Research & Innovation Agency (p. 60); MEWA\'s Environment Week is where the Fund launches initiatives (p. 58).', ['وزارة البيئة والمياه والزراعة']),
 'National Waste Management Center (MWAN)': (f'{EF}: one of the five national centres the Fund finances (p. 30); 4 private-sector attraction opportunities listed at MWAN (p. 76); joint beach protection and treatment initiative in Jeddah under the Governor\'s patronage (p. 61).', ['المركز الوطني لإدارة النفايات']),
 'National Center for Environmental Compliance Monitoring (NCEC Monitoring)': (f'{EF}: fee schedules for 14 licences, 34 services and 4 clearances in progress with the Non-Oil Revenue Development Center (p. 78); Green Factory initiative with the Fund — 100 factories and 300 staff trained on compliance (p. 66); environmental inspection to be run with a private partner, pre-qualification call issued (p. 79).', ['المركز الوطني للرقابة على الالتزام البيئي']),
 'National Center for Wildlife Development': (f'{EF}: one of the five centres the Fund finances; 16 private-sector attraction opportunities (p. 76); fee documents for 12 licences and 8 permits (p. 78); carbon-credit pilot service agreement with the Fund in review (p. 47).', ['المركز الوطني لتنمية الحياة الفطرية']),
 'National Center for Vegetation Cover Development & Combating Desertification (NCVC)': (f'{EF}: one of the five centres the Fund finances; 25 private-sector attraction opportunities (p. 76); building a carbon-credit business model with Saudi Energy and the Fund (p. 50); carbon pilot service agreement in review (p. 47).', ['المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر']),
 'National Center for Meteorology': (f'{EF}: one of the five national centres the Fund finances; its recruitment runs on the Fund\'s shared services (p. 87).', ['المركز الوطني للأرصاد']),
 'Social Development Bank (SDB)': (f'{EF}: cooperation agreement with the Fund to widen the reach of its loan-guarantee product (p. 55).', ['بنك التنمية الاجتماعية']),
 "Saudi Arabian Mining Company (Ma'aden)": (f'{EF}: cooperation agreement with the Fund to widen the reach of its loan-guarantee product (p. 55).', []),
 'SOUDAH': (f'{EF}: carbon-credit cooperation agreement with the Fund being prepared (p. 50).', ['شركة السودة للتطوير']),
 'Saudi Energy (formerly SEC)': (f'{EF}: assessing a carbon-credit business model with NCVC and the Fund (p. 50) — EH is not in that conversation, and it is adjacent to EH\'s landfill-gas and organic-waste work.', []),
 'National Water Company': (f'{EF}: coordinating with the Fund on water-sector carbon credits (p. 50).', []),
 'Agricultural Development Fund': (f'{EF}: farm-to-credit carbon study covering 300 farms with the Environment Fund (p. 51).', ['صندوق التنمية الزراعية']),
 # Etimad buyers already on the map: Arabic Etimad name as alias so the Government Tenders tab links them
 'Saudi Water Authority': ('', ['الهيئة السعودية للمياه']),
 'Holy Makkah Municipality': ('', ['أمانة العاصمة المقدسة']),
 'Saudi Geological Survey': ('', ['هيئة المساحة الجيولوجية السعودية']),
 'King Abdulaziz City for Science and Technology (KACST)': ('', ['مدينة الملك عبدالعزيز للعلوم والتقنية']),
 'Ministry of National Guard (SANG)': ('', ['وزارة الحرس الوطني']),
 'Royal Saudi Navy': ('', ['القوات البحرية']),
 'Hail Region Municipality': ('', ['أمانة منطقة حائل']),
}
DUP = ('Enviromental Fund', 'Environment Fund')

ap = argparse.ArgumentParser(); ap.add_argument('--map', default=os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html'))
ap.add_argument('--workbook'); ap.add_argument('--out'); ap.add_argument('--etimad-json', help='etimad_tenders.json (local, never committed) — adds tender detail to the workbook notes only')
a = ap.parse_args()
today = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y-%m-%d')

def note_for(base, aliases, existing=''):
    parts = [existing.strip()] if existing.strip() else []
    if base and MARK not in existing and base not in existing: parts.append(base)
    for x in aliases:
        if f'Alias (merged duplicate): {x}.' not in existing: parts.append(f'Alias (merged duplicate): {x}.')
    return ' '.join(parts).strip()

# ---------------------------------------------------------------- map
h = open(a.map, encoding='utf-8').read()
m = re.search(r'(<script id="DATA" type="application/json">)(.*?)(</script>)', h, re.S)
D = json.loads(m.group(2)); nodes = D['nodes']; by = {n['n']: n for n in nodes}
log = []
if DUP[0] in by and DUP[1] in by:
    nodes.remove(by[DUP[0]]); log.append(('merged', DUP[0], f'into {DUP[1]} (misspelt duplicate)'))
for name, (base, aliases) in UPD.items():
    n = by.get(name)
    if n is None: sys.exit(f'map record not found: {name}')
    new = note_for(base, aliases, n.get('notes') or '')
    if new != (n.get('notes') or ''): n['notes'] = new; log.append(('noted', name, 'report note' if base else 'Etimad alias'))
added = 0
for name, cat, tier, typ, sec, rg, city, note, aliases in NEW:
    if name in by: continue
    src = 'Environment Fund annual report 2025' if note.startswith(EF) else 'Etimad (government tenders platform)'
    nodes.append({'n': name, 'cat': cat, 'rg': rg, 'city': city, 'reg': '', 'typ': typ, 'sec': sec, 'tier': tier, 'bid': False,
                  'sites': None, 'mn': False, 'mp': False, 'act': '', 'notes': note_for(note, aliases), 'bc': 0, 'bf': '', 'threat': '',
                  'collab': cat == 'Potential Collaborators', 'sc': None, 'cap': None, 'bk': 0, 'cf': 'Medium', 'cf_basis': src,
                  'drv': '', 'added_from': src, 'added_on': today})
    added += 1; log.append(('added', name, src))
payload = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
h = h[:m.start(2)] + payload + h[m.end(2):]
if DUP[0] in h: h = re.sub(r'"Enviromental Fund":\[[^\]]*\],', '', h).replace('"Enviromental Fund"', '"Environment Fund"')
# display: the machine marker "Alias (merged duplicate): X." reads as "Also known as: X." in the detail panel
OLDJS = "if(n.notes)rows.push([t('Notes','\\u0645\\u0644\\u0627\\u062d\\u0638\\u0627\\u062a'),n.notes]);"
NEWJS = ("if(n.notes)rows.push([t('Notes','\\u0645\\u0644\\u0627\\u062d\\u0638\\u0627\\u062a'),"
         "String(n.notes).replace(/Alias \\(merged duplicate\\): ([^.]*)\\./g,t('Also known as: $1.','\\u064a\\u064f\\u0639\\u0631\\u0641 \\u0623\\u064a\\u0636\\u0627\\u064b \\u0628\\u0627\\u0633\\u0645: $1.'))]);")
if OLDJS in h: h = h.replace(OLDJS, NEWJS); log.append(('display', 'detail panel', 'aliases shown as "Also known as"'))
elif 'Also known as' not in h: print('WARNING: notes display line not found; alias wording left as is')
open(a.map, 'w', encoding='utf-8').write(h)
print(f'map: {added} records added, {sum(1 for x in log if x[0]=="noted")} records annotated, {sum(1 for x in log if x[0]=="merged")} duplicate merged')

# ---------------------------------------------------------------- workbook
if a.workbook:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    ET = {}
    if a.etimad_json and os.path.exists(a.etimad_json):
        o = json.load(open(a.etimad_json, encoding='utf-8')); SL = {s['id']: s['en'] for s in o.get('service_lines', [])}
        for t in o['tenders']:
            if t['relevance'] == 'Not EH': continue
            ET.setdefault(t['agency'], []).append(t)
    def etimad_text(aliases):
        ts = [t for x in aliases for t in ET.get(x, [])]
        if not ts: return ''
        ts.sort(key=lambda t: t['sub'] or '', reverse=True)
        items = [f"«{t['title'].strip()}» (ref {t['ref']}, {'core service' if t['relevance']=='Core' else 'related'}"
                 + (f": {', '.join(SL.get(i, str(i)) for i in t['service_lines'])}" if t['service_lines'] else '')
                 + f", published {t['pub']}, submission {t['sub'][:10]})" for t in ts]
        return f'Etimad, relevant tenders captured to {o.get("last_capture")}: {len(ts)} — ' + '; '.join(items) + '.'
    wb = openpyxl.load_workbook(a.workbook); ws = wb['Stakeholders']
    hdr = {str(c.value or ''): i + 1 for i, c in enumerate(ws[1])}
    rows = {str(ws.cell(i, hdr['Name']).value or '').strip(): i for i in range(2, ws.max_row + 1)}
    if DUP[0] in rows and DUP[1] in rows:
        ws.delete_rows(rows[DUP[0]], 1); rows = {str(ws.cell(i, hdr['Name']).value or '').strip(): i for i in range(2, ws.max_row + 1)}
    for name, (base, aliases) in UPD.items():
        r = rows.get(name)
        if not r: print('workbook: not found', name); continue
        c = ws.cell(r, hdr['Notes']); txt = note_for(base, aliases, str(c.value or ''))
        et = etimad_text(aliases)
        if et and 'Etimad, relevant tenders' not in txt: txt += ' ' + et
        c.value = txt
    for name, cat, tier, typ, sec, rg, city, note, aliases in NEW:
        if name in rows: continue
        src = 'Environment Fund annual report 2025' if note.startswith(EF) else 'Etimad (government tenders platform)'
        txt = note_for(note, aliases); et = etimad_text(aliases)
        if et: txt += ' ' + et
        vals = {'Name': name, 'Category': cat, 'Tier': tier, 'Company Type': typ, 'Region': rg, 'City': city, 'Status': 'Added ' + today,
                'Confidence': 'Medium', 'Confidence Basis': src, 'Evidence/Source': src, 'Bids vs EH': 'No', 'Bid Encounters': 0,
                'EH Client': 'No', 'Notes': txt}
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
    wb.save(a.out or a.workbook); print('workbook saved:', a.out or a.workbook, '| rows', ws.max_row - 1)
