"""patch_fiscal_v5.py — Saudi Government Finances 2026, version 5 (01/10/2026).

Why: the Ministry of Finance's 2027 pre-budget statement (30/09) gave the first official estimate of the war's cost
(2026 gap SAR 245 billion; economy −3.6% in 2026), and September brought the two events version 4 called the worst
case: the Houthis took the Bab el-Mandeb strait (10–11/09) and the East–West pipeline to Yanbu was shut for about ten
days (10–22/09). Version 5 updates the summary, key figures, charts E and F, the scenarios and the sources; adds two new
sections — how this affects the 31 Vision 2030 projects tracked on the hub, and what EH should do (Business
Development proposals); and updates the Arabic view and the Arabic-mode dictionary. Sections 3 (Jan–Jun actuals) and
the page structure are unchanged. Text lives in plain_text/fiscal_v5.py. Run once.
"""
import os, sys, shutil, importlib.util, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
spec = importlib.util.spec_from_file_location('v5', os.path.join(HERE, 'plain_text', 'fiscal_v5.py')); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
P = os.path.join(ROOT, 'hub', 'saudi_fiscal_monitor_2026.html'); K = 'saudi_fiscal_monitor_2026.html'
A = os.path.join(ROOT, 'hub', 'eh-ar-dashboard.js'); KA = 'eh-ar-dashboard.js'
if 'Version 5 · 01/10/2026' in open(P, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (P, A): shutil.copy2(p, p + '.pre-v5.bak')
load(P, K); load(A, KA); N = 0
def block(a, b):
    s = FILES[K]; i = s.index(a); j = s.index(b, i + len(a)); return s[i:j]
def R(f, a, b, note, **k):
    global N; N += 1; rep(f, a, b, 'v5', note, **k)
R(K, block('<body>', '<!-- ============ SECTION 1'), T.S['nav'], 'Navigation: version tag, two new sections')
R(K, block('<!-- ============ SECTION 1', '<!-- ============ SECTION 2'), T.S['1'], 'Summary rewritten for the pre-budget statement and September events')
R(K, block('<!-- ============ SECTION 2', '<!-- ============ SECTION 3'), T.S['2'], 'Key figures section intro')
R(K, block('<!-- ============ SECTION 4', '<!-- ============ SECTION 5'), T.S['4'], 'Year-end outlook: charts E and F text')
R(K, block('<!-- ============ SECTION 5', '<!-- ============ SECTION 6'), T.S['5'], 'Scenarios + new sections: Vision 2030 projects, What EH should do')
a, b = T.S['6_head']; R(K, a, b, 'Sources intro')
R(K, '<div class="sec-head"><span class="sec-num">SECTION 06</span><h2>Where the figures come from</h2></div>', '<div class="sec-head"><span class="sec-num">SECTION 08</span><h2>Where the figures come from</h2></div>', 'Sources renumbered')
R(K, '      <b>Barrels a day</b> — how much oil is produced or shipped every day; one barrel is about 159 litres.\n',
     '      <b>Barrels a day</b> — how much oil is produced or shipped every day; one barrel is about 159 litres.\n      <b>East–West pipeline</b> — the oil pipeline from the eastern oilfields to Yanbu on the Red Sea, Saudi Arabia\'s way around the Strait of Hormuz.\n      <b>Pre-budget statement</b> — the Ministry of Finance\'s early outline of next year\'s budget, published each September with an updated estimate for the current year.\n', 'Glossary additions')
s = FILES[K]; i = s.index('    <div class="disclaimer">\n      <b>How this page was put together'); j = s.index('</div>', i) + len('</div>\n')
R(K, s[i:j], T.S['6_method'], 'Method note for version 5')
R(K, block('<!-- ============ SECTION 7', '<script'), T.S['7'], 'Footer for version 5')
for name in ('KPIS', 'SCEN'):
    s = FILES[K]; i = s.index(f'const {name} = ['); j = s.index('];', i) + 2
    R(K, s[i:j], getattr(T, name), f'{name} for version 5')
R(K, 'const SRC = [\n', 'const SRC = [\n' + T.SRC_ADD, 'Two new source cards (pre-budget statement; September events)')
for a, b in T.CHART_E: R(K, a, b, 'Chart E')
for a, b in T.CHART_F: R(K, a, b, 'Chart F')
a, b = T.TITLE; R(K, a, b, 'Browser tab title')
R(K, block('<div id="ehArView"', '<script'), T.AR_VIEW + '\n', 'Arabic view, version 5')
# ---- Arabic mode: new sections are English-only on the page (their Arabic lives in the Arabic view); new labels translated
R(KA, "enOnly:['header#overview','#scenarios','#sources',", "enOnly:['header#overview','#scenarios','#v2030impact','#ehplan','#sources',", 'New sections hidden in Arabic mode (Arabic view carries them)')
KPI_AR = {'Expected gap for 2026 (Ministry of Finance)':'الفجوة المتوقعة لعام 2026 (وزارة المالية)','Planned gap for 2027':'الفجوة المخططة لعام 2027','Size of the economy, 2026':'حجم الاقتصاد، 2026','World oil price (Brent) — close on 30/09':'سعر النفط العالمي (برنت) — إغلاق 30/09','Pipeline to Yanbu':'خط الأنابيب إلى ينبع','Bab el-Mandeb strait':'مضيق باب المندب','Gulf oil through Hormuz':'نفط الخليج عبر هرمز'}
LBL_AR = {'Oil price so far (monthly average, approximate)':'سعر النفط حتى الآن (متوسط شهري تقريبي)','Oct–Dec · most likely: Red Sea closed, convoys run ($90–105)':'أكتوبر–ديسمبر · الأرجح: البحر الأحمر مغلق والقوافل مستمرة (90–105 دولارات)','Oct–Dec · worst: convoys stop too (spike above $110)':'أكتوبر–ديسمبر · الأسوأ: توقف القوافل أيضًا (قفزة فوق 110 دولارات)','Oct–Dec · calmer: a deal eases both straits ($75–90)':'أكتوبر–ديسمبر · الأهدأ: اتفاق يهدّئ المضيقين (75–90 دولارًا)','Ministry of Finance year-end estimate (\u2212245, 30/09)':'تقدير وزارة المالية لنهاية العام (\u2212245، 30/09)','Most likely · Red Sea closed, convoys run — year ~262':'الأرجح · البحر الأحمر مغلق والقوافل مستمرة — السنة نحو 262','Worst · convoys stop too — year ~315':'الأسوأ · توقف القوافل أيضًا — السنة نحو 315','Calmer · a deal eases both straits — year ~245':'الأهدأ · اتفاق يهدّئ المضيقين — السنة نحو 245','Pipeline hit · Houthis take Bab el-Mandeb · 10–11 Sep':'ضرب الأنبوب · الحوثيون يسيطرون على باب المندب · 10–11 سبتمبر'}
SEC_AR = {'What could happen in October–December 2026':'ما قد يحدث في أكتوبر–ديسمبر 2026','What this means for Vision 2030 projects':'ماذا يعني هذا لمشاريع رؤية 2030','What EH should do':'ما يجب أن تفعله آفاق البيئة'}
js = lambda d: ','.join("'" + k + "':'" + v + "'" for k, v in d.items())
s = FILES[KA]; fi = s.index('fisc:{')
for key, d in (('kpi:{', KPI_AR), ('lbl:{', LBL_AR), ('sec:{', SEC_AR)):
    i = s.index(key, fi) + len(key); s = s[:i] + js(d) + ',' + s[i:]
FILES[KA] = s; N += 1
open(P, 'w', encoding='utf-8').write(FILES[K]); open(A, 'w', encoding='utf-8').write(FILES[KA])
write_change_table(os.path.join(HERE, 'change_table_fiscal_v5'), 'Change table — Saudi Government Finances 2026, version 5')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note'], f['old'][:120]) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
