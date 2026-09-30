"""patch_plain_ef.py — plain-language pass on the Environment Fund 2025 page (News & Intelligence, batch 1, 30 Sep 2026).

The page is built by build_ef_page.py from ef_report_2025.json, so the source files are edited and the page rebuilt.
  • ef_report_2025.json — every displayed string goes through the term map below (English and Arabic). Keys the page
    uses as codes (id, cat, status, tier, group, horizon, owner, centres, eh, file, page) are never touched.
  • build_ef_page.py — a few labels, owner names shown in words, and a "Names used on this page" line under the title
    giving every agency its full name once (agreed rule: full name once per page, then the short form).
Numbers are unchanged. "Tier" is kept: it is the stakeholder map's own scale, used across the hub.
A change table lists every string before and after. Run once.
"""
import os, sys, re, json, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
import patchlib
J = os.path.join(HERE, 'ef_report_2025.json'); B = os.path.join(HERE, 'build_ef_page.py')
if 'NAMES_LINE' in open(B, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(J, J + '.pre-plain.bak'); shutil.copy2(B, B + '.pre-plain.bak')

EN = [  # (regex, replacement) — order matters: specific before general
 (r"From studies to privatisation — the Fund's opportunity pipeline in 2025", "From studies to handing projects to private companies — the Fund's opportunities in 2025"),
 (r'Feasibility studies \(41 revenue \+ 4 sector\)', 'Studies of whether projects can work (41 money-making + 4 sector-wide)'),
 (r'^Incentive-package models$', 'Incentive packages prepared'),
 (r'Privatisation projects \(9 advanced \+ 8 preparing\)', 'Services being handed to private operators (9 well advanced + 8 being prepared)'),
 (r'the demand driver for permitting and EIA work', 'which will raise demand for help with permits and environmental impact studies'),
 (r'MWAN lists only 4 attraction opportunities', 'MWAN lists only 4 opportunities to attract private investors'),
 (r'attraction opportunities at', 'opportunities to attract private investors at'),
 (r'by centre attracting private investors', 'by the centre seeking private investors'),
 (r'\(t, programme total\)', '(tonnes, whole programme)'), (r'\(t / year\)', '(tonnes a year)'), (r'\(t\)', '(tonnes)'),
 (r'Al-Kharj ABVRS plant', 'Al-Kharj plant'), (r'\(UAT\)', '(being tested)'),
 (r'Procurement cycle, days \(EXPRO target 130\)', 'Days from tender to contract (EXPRO target: 130)'),
 (r'Shared-services centralisation — how far along', "Moving the centres' back-office work under the Fund — how far along"),
 (r'Peer-group average, financial entities & funds \(%\)', 'Average for similar government financial bodies (%)'),
 (r'2026 budget documentation readiness', '2026 budget paperwork ready'),
 (r'Medium-term financial plan to 2030', 'Financial plan to 2030'),
 (r'^Waste activity$', 'Waste'), (r'^Eco-tourism activity$', 'Eco-tourism'), (r'^Environmental compliance activity$', 'Environmental compliance'),
 (r'Cash investment returns FY 1446/47 \(GIPS-measured\)', 'Income from investing its cash, financial year 1446/47 (measured to international investment-reporting standards)'),
 (r'\bFY 1446/47\b', 'financial year 1446/47'),
 (r'Feasibility studies for PPP opportunities with the private sector', 'Studies of projects the government could run together with private companies'),
 (r'Privatisation projects at advanced stages \+ in preparation', 'Government services being handed to private operators: well advanced + being prepared'),
 (r'Bank framework agreements for the loan-guarantee product', 'Banks signed up to offer loans the Fund guarantees'),
 (r'RFQ \(request for qualification\) issued for the environmental-inspection PPP under the national privatisation framework',
  'a call for companies to pre-qualify has been issued for environmental inspection to be run with a private partner, under the national privatisation framework'),
 (r'RFP completed for the wildlife-shops monitoring and inspection PPP', 'full tender documents are ready for private partners to monitor and inspect wildlife shops'),
 (r'has an RFQ already issued', 'already has a call for companies to pre-qualify'),
 (r'obtain the RFQ', 'obtain the pre-qualification documents'),
 (r'before the RFP stage', 'before the full tender is issued'),
 (r'RFP dates', 'full-tender dates'),
 (r'\bPPP timelines\b', 'Timelines for projects with private partners'),
 (r'45 feasibility studies for PPP opportunities across sectors; 54 incentive-package models for investment opportunities',
  '45 studies of projects the government could run with private companies; 54 packages of incentives prepared for investors'),
 (r'\bPPP pipeline owner\b', 'owner of the list of projects to run with private partners'),
 (r'a PPP of this size', 'a partnership project of this size'),
 (r'\bthe environmental-inspection PPP\b', 'the environmental-inspection project with a private partner'),
 (r'\bPPP\b', 'public–private partnership'),
 (r'3 projects added to the privatisation radar', '3 projects added to the list of services the government plans to hand to private operators'),
 (r'\bprivatisation radar\b', 'list of services planned for private operators'),
 (r'\b54 incentive-package models\b', '54 incentive packages'),
 (r'\bEXPRO approvals obtained\b', 'Approval from EXPRO (the government body that checks spending and projects) obtained'),
 (r'\b21 KPIs\b', '21 performance measures'), (r'\bKPIs\b', 'performance measures'),
 (r'\b18 MoUs/agreements\b', '18 cooperation agreements'), (r'\bMoUs\b', 'cooperation agreements'),
 (r'\bMoU signings\b', 'agreement signings'), (r'\bMoU announcements\b', 'agreement announcements'),
 (r'\bMoU counterparties\b', 'partners in cooperation agreements'), (r'\bMoU with\b', 'Cooperation agreement with'),
 (r'\ban MoU\b', 'a cooperation agreement'), (r'\bMoU\b', 'cooperation agreement'),
 (r'\bSMEs\b', 'small and medium businesses'),
 (r'\bwith LPs and GPs\b', 'with investors and investment-fund managers'),
 (r'\bSLAs signed\b', 'Service agreements signed'), (r'\bSLAs\b', 'service agreements'), (r'\bSLA\b', 'service agreement'),
 (r'\(UAT stage\)', '(being tested by users)'),
 (r'Oracle ERP support', 'Support for the Oracle finance-and-operations system'), (r'Oracle ERP', 'the Oracle finance-and-operations system'),
 (r'EPM budgeting system', 'budget-planning system'),
 (r'\bKABI recruitment system\b', 'KABI recruitment system'),
 (r'ESG programme', 'Sustainability programme (environmental, social and governance standards)'),
 (r'2024 ESG report, ESG library, GRI-based data collection, ESG handbook for SMEs, ESG scorecards',
  '2024 sustainability report, sustainability library, data collected to the international GRI reporting standard, sustainability handbook for small businesses, sustainability scorecards'),
 (r'\bESG consulting\b', 'sustainability consulting'), (r'\bESG scope\b', 'sustainability work'), (r'\bESG\b', 'sustainability'),
 (r'national CDM committee', 'national carbon-credit committee'), (r'National CDM committee', 'National carbon-credit committee'),
 (r'\bGCOM nature-based initiatives\b', 'nature-based projects of the Global Covenant of Mayors'),
 (r'carbon-credit MRV \(measurement, reporting, verification\)', 'measuring, reporting and independently checking carbon credits'),
 (r'using ABVRS thermal drying', 'using a heat-drying process'), (r'\bABVRS animal-waste\b', 'animal-waste'),
 (r'\bput one named capex project against it\b', 'name one specific building or equipment project to use it for'),
 (r'\beligible capex\b', 'which equipment and building costs qualify'), (r'\bcapex\b', 'building and equipment spending'),
 (r'\(ceiling, tenor, coverage %\)', '(maximum amount, repayment period, share of the loan covered)'),
 (r'ceiling, tenor, coverage %', 'maximum amount, repayment period, share covered'),
 (r'\bMorgan Stanley SMA, Q1 2026\b', 'managed by Morgan Stanley, from January–March 2026'),
 (r'via a separately managed account', 'through an account run only for the Fund'),
 (r'\bQ1 2026\b', 'January–March 2026'),
 (r'\bEIA support\b', 'environmental impact assessment support'),
 (r'\bpre-qualified vendors\b', 'approved suppliers'), (r'\bpre-qualification calendar\b', 'supplier-approval calendar'),
 (r'infrastructure baselines completed for all national centres per EXPRO methodology', 'starting assessments of infrastructure completed for all national centres, using EXPRO\'s method'),
 (r'EXPRO-methodology baselines', 'starting assessments done with EXPRO\'s method'),
 (r'now has completed baselines', 'now has completed starting assessments'),
 (r'against an EXPRO target of 130', 'against a target of 130 set by EXPRO'),
 (r'against an EXPRO ceiling of 130', 'against a maximum of 130 set by EXPRO'),
 (r'\bcapital-project pipeline\b', 'list of building and equipment projects'),
 (r'with the non-oil revenue centre', 'with the Non-Oil Revenue Development Center'),
 (r'to the non-oil revenue centre', 'to the Non-Oil Revenue Development Center'),
 (r'\bby 2050, referred to a board task force\b', 'to 2050, passed to a board working group'),
 (r'\(\+12 pts\)', '(up 12 points)'),
 (r'\bas a Tier 1 contact\b', 'as a top-priority contact'),
 (r'Tier GOV, empty notes', 'listed as a government body, no notes yet'),
 (r'\bdecide the consortium role \(inspection operator vs\. technical sub-contractor\)', 'decide EH\'s role in a group bid (running the inspections, or specialist sub-contractor)'),
 (r'will be won by a consortium, not a single consultancy', 'will be won by a group of companies bidding together, not by one consultancy'),
 (r'\bSaudi Venture Capital \(SVC\)', 'Saudi Venture Capital (SVC, the state fund that invests in start-ups)'),
 (r'\bstated thesis of\b', 'stated focus on'),
 (r'\bGRI\b', 'GRI (international sustainability-reporting standard)'),
 (r'\bISO/IEC 27001:2022 \(information security\), ISO 22301 \(business continuity\), ISO 31000 renewed \(risk\), ISO 27701 \(privacy\)',
  'International quality certificates: information security (ISO/IEC 27001:2022), keeping services running in a crisis (ISO 22301), risk management (ISO 31000, renewed), privacy (ISO 27701)'),
 (r'(\d[\d,.]*) t/yr\b', r'\1 tonnes a year'), (r'(\d[\d,.]*) t\b', r'\1 tonnes'),
 (r'1 M m²', '1 million m²'),
 (r'\bSAR ([\d.,]+) M\+', r'SAR \1 million+'), (r'\bSAR ([\d.,]+) M\b', r'SAR \1 million'),
 (r'\bMoF approval\b', 'Ministry of Finance approval'),
 (r'\bEF grantee\b', 'Fund grant recipient'), (r'\bEF indirect-financing\b', 'Fund indirect-financing'), (r'\bEF loan guarantees\b', 'Fund loan guarantees'),
 (r'\bEF carbon-credit\b', 'Fund carbon-credit'), (r'\bMoU with EF\b', 'Cooperation agreement with the Fund'), (r'\bwith EF\b', 'with the Fund'),
 (r'^EF — ', 'Environment Fund — '),
 (r'\bBD to\b', 'Business Development to'),
 (r'\bxref\b', 'cross-check'),
]
AR = [
 (r'\bESG\b', 'الاستدامة'), (r'\bGIPS\b', 'المعايير الدولية لقياس أداء الاستثمار'), (r'\bSLA\b', 'اتفاقية مستوى خدمة'),
 (r'\bUAT\b', 'مرحلة اختبار المستخدمين'), (r'\bABVRS\b', 'التجفيف الحراري'), (r'\bGCOM\b', 'الميثاق العالمي لرؤساء البلديات'),
 (r'\bERP\b', 'نظام تخطيط الموارد'), (r'\bEPM\b', 'نظام تخطيط الميزانية'),
]
SKIP = {'id', 'cat', 'status', 'tier', 'group', 'horizon', 'owner', 'centres', 'eh', 'file', 'page', 'pages', 'extracted', 'tracker_xref_as_of', 'value', 'ar_value', 'when', 'kind'}
d = json.load(open(J, encoding='utf-8')); rows = []
def fix(s, rules):
    o = s
    for a, b in rules: s = re.sub(a, b, s)
    return s
def walk(o, key=None, path=''):
    if isinstance(o, dict): return {k: walk(v, k, path + '.' + k) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, key, f'{path}[{i}]') for i, v in enumerate(o)]
    if isinstance(o, str) and key not in SKIP:
        n = fix(o, AR if re.search(r'[\u0600-\u06FF]', o) else EN)
        if n != o: rows.append((path, o, n))
        return n
    if isinstance(o, str) and key == 'unit' and o == 't':
        rows.append((path, o, 'tonnes')); return 'tonnes'
    if isinstance(o, str) and key in ('value',):  # headline figures: units in words
        n = fix(o, [(r'\bSAR ([\d.,]+) M\+', r'SAR \1 million+'), (r'\bSAR ([\d.,]+) M\b', r'SAR \1 million')])
        if n != o: rows.append((path, o, n))
        return n
    return o
d2 = walk(d)
json.dump(d2, open(J, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- builder
load(B, 'build_ef_page.py'); K = 'build_ef_page.py'; n = 0
for a, b in [
  ("L('bid-tracker cross-reference as of','مطابقة جدول العطاءات حتى')", "L('checked against EH\\'s bid tracker on','مطابقة جدول العطاءات حتى')"),
  ("'What it means for EH — filed by question, tagged by horizon and owner'", "'What it means for EH — grouped by question, with when it matters and who at EH acts'"),
  ("'Events calendar for BD attendance'", "'Events Business Development should attend'"),
  ("'log scale — bar lengths are not proportional'", "'compressed scale so large and small numbers fit — bar lengths are not to scale'"),
  ("'Extraction ledger — every figure with its page'", "'Every figure and the page it comes from'"),
  ("'Loan support, guarantees and impact investment reach EH directly; grants, PPP, fees and shared services reach EH through the centres it is licensed by and bids to.'",
   "'Loan support, guarantees and impact investment reach EH directly; grants, partnerships with private companies, fees and shared services reach EH through the centres that license it and that it bids to.'"),
  ("${esc(L(o.owner,OWN[o.owner]||o.owner))}", "${esc(L(OWN_EN[o.owner]||o.owner,OWN[o.owner]||o.owner))}"),
  ("const OWN={", "const OWN_EN={'BD':'Business Development','Consulting/EIA':'Consulting / environmental studies'};\nconst OWN={"),
  ("$('kstrip').innerHTML=EF.headline.map(",
   "/* NAMES_LINE: every agency in full once per page (agreed 30 Sep 2026), then the short form */\n"
   " (function(){let el=document.getElementById('names');if(!el){el=document.createElement('div');el.id='names';el.className='note';el.style.cssText='margin:-4px 0 12px;font-size:12px';$('kstrip').parentNode.insertBefore(el,$('kstrip'));}\n"
   "  el.innerHTML=L('<b>Names used on this page:</b> NCEC — National Center for Environmental Compliance · MWAN — National Center for Waste Management · NCVC — National Center for Vegetation Cover &amp; Combating Desertification · NCW — National Center for Wildlife · NCM — National Center for Meteorology · MEWA — Ministry of Environment, Water &amp; Agriculture · EXPRO — Expenditure &amp; Projects Efficiency Authority (checks government spending and projects) · Etimad — the government tendering portal · Kafalah — the state loan-guarantee programme for small businesses',"
   "'<b>الأسماء المستخدمة في هذه الصفحة:</b> المركز الوطني للرقابة على الالتزام البيئي · المركز الوطني لإدارة النفايات (موان) · المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر · المركز الوطني لتنمية الحياة الفطرية · المركز الوطني للأرصاد · وزارة البيئة والمياه والزراعة · هيئة كفاءة الإنفاق والمشروعات الحكومية (إكسبرو) · اعتماد — بوابة المنافسات الحكومية · كفالة — برنامج ضمان تمويل المنشآت الصغيرة');})();\n"
   " $('kstrip').innerHTML=EF.headline.map("),
]:
    rep(K, a, b, 'plain', 'Environment Fund page wording'); n += 1
open(B, 'w', encoding='utf-8').write(FILES[K])
for p, o, nn in rows: patchlib.CHANGE_LOG.append({'file': 'ef_report_2025.json', 'tag': 'plain', 'note': p, 'old': o, 'new': nn}) if hasattr(patchlib, 'CHANGE_LOG') else None
# change table for the data strings (patchlib covers the builder edits)
with open(os.path.join(HERE, 'change_table_plain_ef_data.md'), 'w', encoding='utf-8') as f:
    f.write('# Change table — Environment Fund data strings (plain-language pass)\n\n| Field | Before | After |\n|---|---|---|\n')
    for p, o, nn in rows: f.write(f"| `{p}` | {o.replace('|','/')} | {nn.replace('|','/')} |\n")
write_change_table(os.path.join(HERE, 'change_table_plain_ef'), 'Change table — Environment Fund builder wording')
print('data strings changed:', len(rows), '· builder edits:', n - len(FAILURES), 'of', n, '· failures:', len(FAILURES)); [print('FAIL', f['note'], f['old'][:100]) for f in FAILURES]
if FAILURES: sys.exit(1)
subprocess.run([sys.executable, B], cwd=HERE, check=True)
