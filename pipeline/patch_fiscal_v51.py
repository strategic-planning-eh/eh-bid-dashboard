"""patch_fiscal_v51.py — Saudi Government Finances 2026, version 5.1 (01/10/2026).

1. New section 04 "2022 to 2029": plan vs actual for income, spending, gap and debt, from the Ministry of Finance's own
   documents (2024 year-end report, 2026 budget statement, Q1/Q2 2026 reports, 2027 pre-budget statement), chart G, and
   four conclusions — notably that spending ended 8–10% above plan three years running and that the 2027 plan asks for a
   3% cut on 2026's expected level, which is where the pressure on Vision 2030 projects comes from.
2. Vision 2030 section rebuilt around the three tests (mostly built? earns money / strategic / fixed date? who pays?) with a
   "likely outcome" column (shelved / downsized / frozen / cut back / delayed / continues / expands), following Youssef's
   review: KAEC delayed not dropped; NEOM Port separated from Oxagon; The Line, Trojena, New Murabba and AMAALA at the top.
3. Corrections from the pre-budget statement itself: 2026 gap = 4.9% of the economy (nominal GDP SAR 4,978 billion, not
   EH's earlier 4.9 trillion approximation), 2027 gap SAR 191 billion; scenario percentages recomputed; 2026 income and
   spending estimates and January–August oil supply (7.9 vs 9.2 million barrels a day) added.
4. Sections renumbered (04 history, 05 outlook, 06 scenarios, 07 projects, 08 EH, 09 sources); Arabic view and Arabic-mode
   dictionary updated. Text lives in plain_text/fiscal_v51.py. Run once.
"""
import os, sys, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
spec = importlib.util.spec_from_file_location('v51', os.path.join(HERE, 'plain_text', 'fiscal_v51.py')); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
P = os.path.join(ROOT, 'hub', 'saudi_fiscal_monitor_2026.html'); K = 'saudi_fiscal_monitor_2026.html'
A = os.path.join(ROOT, 'hub', 'eh-ar-dashboard.js'); KA = 'eh-ar-dashboard.js'
if 'id="history"' in open(P, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (P, A): shutil.copy2(p, p + '.pre-v51.bak')
load(P, K); load(A, KA); N = 0
def R(f, a, b, note, **k):
    global N; N += 1; rep(f, a, b, 'v5.1', note, **k)
def block(a, b):
    s = FILES[K]; i = s.index(a); j = s.index(b, i + len(a)); return s[i:j]
# --- navigation, version tag
R(K, '<span class="vtag">Version 5 · 01/10/2026 · after the 2027 pre-budget statement</span>', '<span class="vtag">Version 5.1 · 01/10/2026 · with 2022–2029 history</span>', 'Version tag')
R(K, '      <a href="#compare">Plan vs actual</a>\n', '      <a href="#compare">Plan vs actual</a>\n      <a href="#history">2022–2029</a>\n', 'Nav link to the history section')
# --- renumber (highest first so labels never collide)
R(K, '<span class="sec-num">SECTION 08</span><h2>Where the figures come from', '<span class="sec-num">SECTION 09</span><h2>Where the figures come from', 'Renumber sources')
R(K, '<span class="sec-num">SECTION 07</span><h2>What EH should do', '<span class="sec-num">SECTION 08</span><h2>What EH should do', 'Renumber EH section')
R(K, '<span class="sec-num">SECTION 05</span><h2>What could happen', '<span class="sec-num">SECTION 06</span><h2>What could happen', 'Renumber scenarios')
R(K, '<span class="sec-num">SECTION 04</span><h2>How 2026 could end', '<span class="sec-num">SECTION 05</span><h2>How 2026 could end', 'Renumber outlook')
R(K, '(section 5)', '(section 6)', 'Cross-reference', ) if '(section 5)' in FILES[K] else None
# --- new history section, chart G
R(K, '<!-- ============ SECTION 4 — PROJECTION ============ -->', T.HISTORY + '<!-- ============ SECTION 4 — PROJECTION ============ -->', 'New section 04: 2022–2029 plan vs actual')
s = FILES[K]; i = s.index("document.getElementById('chartF')"); j = s.index("\n});\n</script>", i) + len("\n});\n")
CHART_G = r"""
/* ---- Chart G: plan vs actual gap 2022–2029 (v5.1, official MoF figures) ---- */
new Chart(document.getElementById('chartG'),{
  type:'bar',
  data:{ labels:['2022','2023','2024','2025','2026','2027','2028','2029'], datasets:[
    {label:'Planned in the budget', data:[null,null,-79,-101,-165.4,-191,-177,-192], backgroundColor:'rgba(5,114,188,.35)', borderColor:C.blue, borderWidth:1.2, borderRadius:4},
    {label:'Actual (2026 = Ministry estimate)', data:[104,-81,-116,-276.6,-245,null,null,null], backgroundColor:C.navy, borderRadius:4}
  ]},
  options:{ responsive:true, maintainAspectRatio:false,
    plugins:{ ...legendTop, tooltip:{callbacks:{label:c=>c.parsed.y==null?null:`${c.dataset.label}: ${c.parsed.y>0?'surplus':'gap'} SAR ${FMT(Math.abs(c.parsed.y))} billion`}} },
    scales:{ y:{title:{display:true,text:'SAR billion (above zero = surplus)',font:{size:11,weight:'600'},color:'#8a98a8'},grid:{color:GRID}}, x:{grid:{display:false}} } }
});
"""
R(K, s[i:j], s[i:j] + CHART_G, 'Chart G drawing code')
# --- Vision 2030 section rebuilt around the three tests
R(K, block('<!-- ============ SECTION 5B', '<!-- ============ SECTION 5C'), T.V2030, 'Vision 2030 section: three tests + likely outcome')
R(K, T.EH_CARD2_OLD, T.EH_CARD2_NEW, 'EH bid advice follows the new outcome labels')
R(K, 'This is where the pressure on Vision 2030 projects in section 07', 'This is where the pressure on Vision 2030 projects in section 07', 'noop') if False else None
# --- corrections from the pre-budget statement
R(K, '<b>SAR 245–280 billion (about 5.0–5.7% of the size of the economy)</b>', '<b>SAR 245–280 billion (about 4.9–5.6% of the size of the economy)</b>', 'Percentages on the Ministry\'s own GDP (SAR 4,978 billion)')
R(K, 'as oil exports recover. For 2027 it plans', 'as oil exports recover. Its estimate puts 2026 income at <b>SAR 1,190 billion</b> and spending at <b>SAR 1,435 billion</b> — 9% above this year\'s plan. It also reports that Saudi crude supply averaged <b>7.9 million barrels a day in January–August</b>, against 9.2 million a year earlier, while Brent averaged $87. For 2027 it plans', 'Pre-budget detail: 2026 income/spending, oil supply')
R(K, 'a gap of about <b>SAR 190 billion (3.6% of the size of the economy)</b>', 'a gap of about <b>SAR 191 billion (3.6% of the size of the economy)</b>', '2027 gap per the statement table') if 'a gap of about <b>SAR 190 billion (3.6% of the size of the economy)</b>' in FILES[K] else None
R(K, 'Percentages are of the size of the Saudi economy in 2026, taken as about SAR 4.9 trillion (EH\'s approximation: the pre-war SAR 5.0 trillion adjusted for the Ministry\'s expected 3.6% fall in output and higher oil prices).',
     'Percentages are of the size of the Saudi economy in 2026 as estimated by the Ministry of Finance: SAR 4,978 billion (pre-budget statement, 30/09).', 'Scenario base: Ministry GDP')
R(K, 'The size of the economy used for percentages (about SAR 4.9 trillion) is EH\'s approximation.', 'Percentages use the Ministry\'s own estimate of the 2026 economy (SAR 4,978 billion) and, for 2022–2025, the Ministry\'s published ratios.', 'Method note: GDP source')
R(K, r"pct:'~5.0\u20135.7%'", r"pct:'~4.9\u20135.6%'", 'Scenario %')
R(K, r"pct:'~4.8\u20135.2%'", r"pct:'~4.7\u20135.1%'", 'Scenario %')
R(K, r"pct:'~5.9\u20136.9%'", r"pct:'~5.8\u20136.8%'", 'Scenario %')
R(K, "val:'~190'", "val:'191'", 'KPI: 2027 gap')
R(K, "delta:'48% above the SAR 165.4 billion plan · EH most likely: 245–280'", "delta:'4.9% of the economy · 48% above the SAR 165.4 billion plan · EH most likely: 245–280'", 'KPI: 2026 gap as % of economy') if "delta:'48% above the SAR 165.4 billion plan · EH most likely: 245–280'" in FILES[K] else None
R(K, "2027 gap about SAR 190 billion.", "2027 gap about SAR 191 billion.", 'Source card: 2027 gap')
R(K, 'const SRC = [\n', 'const SRC = [\n' + T.SRC_ADD, 'Source card: earlier Ministry documents')
# --- Arabic view
R(K, '<h2>القسم 08 · من أين تأتي الأرقام</h2>', '<h2>القسم 09 · من أين تأتي الأرقام</h2>', 'AR renumber')
R(K, '<h2>القسم 07 · ما يجب أن تفعله آفاق البيئة</h2>', '<h2>القسم 08 · ما يجب أن تفعله آفاق البيئة</h2>', 'AR renumber')
R(K, block('<h2>القسم 06 · ماذا يعني هذا لمشاريع رؤية 2030</h2>', '<h2>القسم 08 · ما يجب'), T.AR_V2030, 'AR: projects with three tests')
R(K, '<h2>القسم 05 · ما قد يحدث في أكتوبر–ديسمبر 2026</h2>', '<h2>القسم 06 · ما قد يحدث في أكتوبر–ديسمبر 2026</h2>', 'AR renumber')
R(K, '<h2>القسم 04 · كيف قد ينتهي عام 2026</h2>', T.AR_HISTORY + '<h2>القسم 05 · كيف قد ينتهي عام 2026</h2>', 'AR: history section + renumber')
R(K, '<b>245–280 مليار ريال (نحو 5.0–5.7% من حجم الاقتصاد)</b>', '<b>245–280 مليار ريال (نحو 4.9–5.6% من حجم الاقتصاد)</b>', 'AR %')
R(K, '<b>245–280 مليار ريال (5.0–5.7%)</b>', '<b>245–280 مليار ريال (4.9–5.6%)</b>', 'AR %')
R(K, 'مقدّرًا بنحو <b>4.9 تريليونات ريال</b> (تقريب من آفاق البيئة)', 'وفق تقدير وزارة المالية: <b>4,978 مليار ريال</b>', 'AR GDP base')
R(K, 'فجوة نحو <b>190 مليار ريال (3.6% من حجم الاقتصاد)</b>', 'فجوة نحو <b>191 مليار ريال (3.6% من حجم الاقتصاد)</b>', 'AR 2027 gap') if 'فجوة نحو <b>190 مليار ريال' in FILES[K] else None
R(K, '<div class="avnote">آفاق البيئة · التخطيط الاستراتيجي — الإصدار الخامس · 01/10/2026 · بعد بيان ميزانية 2027 المبدئي</div>', '<div class="avnote">آفاق البيئة · التخطيط الاستراتيجي — الإصدار 5.1 · 01/10/2026 · مع مقارنة 2022–2029</div>', 'AR version tag')
# --- Arabic mode dictionary
R(KA, "enOnly:['header#overview','#scenarios','#v2030impact','#ehplan','#sources',", "enOnly:['header#overview','#history','#scenarios','#v2030impact','#ehplan','#sources',", 'History section is English-only on the page; Arabic view carries it')
s = FILES[KA]; fi = s.index('fisc:{'); i = s.index('sec:{', fi) + len('sec:{')
add = "'2022 to 2029: what was planned, what happened, what comes next':'من 2022 إلى 2029: ما خُطط وما حدث وما هو قادم','Which Vision 2030 projects are likely to be shelved, cut back or delayed':'أي مشاريع رؤية 2030 مرشحة للتجميد أو التقليص أو التأجيل','SECTION 07':'القسم 07','SECTION 08':'القسم 08','SECTION 09':'القسم 09',"
FILES[KA] = s[:i] + add + s[i:]; N += 1
i = FILES[KA].index('lbl:{', fi) + len('lbl:{')
FILES[KA] = FILES[KA][:i] + "'Planned in the budget':'المخطط في الميزانية','Actual (2026 = Ministry estimate)':'الفعلي (2026 = تقدير الوزارة)','SAR billion (above zero = surplus)':'مليار ريال (فوق الصفر = فائض)'," + FILES[KA][i:]; N += 1
open(P, 'w', encoding='utf-8').write(FILES[K]); open(A, 'w', encoding='utf-8').write(FILES[KA])
write_change_table(os.path.join(HERE, 'change_table_fiscal_v51'), 'Change table — Saudi Government Finances 2026, version 5.1')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note'], f['old'][:140]) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
