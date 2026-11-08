# -*- coding: utf-8 -*-
"""patch_news_nov2026.py — Corporate & Government News: the "8 November update" edition.

Additive edition (the page keeps every story since April and filters by period):
  • 24 new stories (10 company, 14 government / mega-project) for 26 Aug – 8 Nov 2026, period "Q4-2026"
  • fact-check of all 24 claims of the 26 August edition (AUDIT) + corrections, resolved gaps and declared gaps
  • three existing cards corrected where the fact-check found an error (SABIC loss figure, PIF attribution, Alujain result)
  • header window / generated date, period filter, KPI oil card, "new money" chart re-based on this period
  • Big Picture rewritten (eight reads incl. what to watch); Arabic edition extended with condensed versions of the
    new stories, the verification paragraph, KPI line, big picture and methodology note
Content lives in news_nov2026_content.py; research in pipeline/analysis/news_findings_2026-11.md.

Run once:  python3 pipeline/patch_news_nov2026.py
"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_files, write_change_table, _log
import news_nov2026_content as T

P = os.path.join(HERE, '..', 'hub', 'eh_news_intelligence.html')
if '8 November Update' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'n'); K = 'n'
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

# ---------------------------------------------------------------- title, meta
rep(K, '<title>Environmental Horizons — Saudi Arabia Intelligence Dashboard · April–September 2026 · 26 August Update</title>',
    '<title>Environmental Horizons — Saudi Arabia Intelligence Dashboard · April–November 2026 · 8 November Update</title>', 'edition', 'title')
rep(K, '"generated":"26/08/2026","window":"01/04/2026 – 26/08/2026"}', '"generated":"08/11/2026","window":"01/04/2026 – 08/11/2026"}', 'edition', 'META dates')

# ---------------------------------------------------------------- existing cards: corrections found by the fact-check
rep(K, 'net loss SAR 0.38 billion; volumes down 34% while prices rose 42%.', 'reported net loss SAR 833 million (SAR 0.38 billion after adjustments — corrected 08/11); volumes down 34% while prices rose 42%.', 'correction', 'C03 financials')
rep(K, 'and a net loss of SAR 0.38 billion. The reason:', 'and a reported net loss of SAR 833 million (SAR 0.38 billion on an adjusted basis — our 26 August card gave only the adjusted figure). The reason:', 'correction', 'C03 detail')
rep(K, 'Construction promises cut from $71 billion to $30 billion — the biggest pull-back in the fund\'s history.', 'Construction promises reported cut from $71 billion to $30 billion (press figures — PIF\'s published strategy of 13/08 gives no construction-commitment number).', 'correction', 'G01 financials')
rep(K, 'Construction commitments were cut from $71 billion to $30 billion, on top of an earlier round of cuts.', 'Press reports put the cut in construction commitments at $71 billion to $30 billion, on top of an earlier round; the strategy PIF published on 13 August gives no such figure, so these numbers remain press reporting (corrected 08/11).', 'correction', 'G01 detail')
rep(K, 'January–March profit SAR 12.2m — back from a loss; more than SAR 1.1 billion already invested in the new plant.', 'January–March profit SAR 12.2m; six-month profit SAR 104 million (published 02/08 — added 08/11, the figure was already out when our last edition appeared); more than SAR 1.1 billion already invested in the new plant.', 'correction', 'C05 financials')

# ---------------------------------------------------------------- new stories
new_json = ',\n'.join(J(r) for r in T.NEW_DATA)
i = FILES[K].index('"ehNote":"Security background — no direct work, but it shapes the risk levels our emergency plans prepare for."}\n];')
j = FILES[K].index('}\n];', i) + 1
FILES[K] = FILES[K][:j] + ',\n' + new_json + FILES[K][j:]; _log(K, 'exact', 'DATA ]', f'{len(T.NEW_DATA)} new records', 'edition', 'DATA: 24 new stories', 1, True)
rep(K, '<option value="Q3-2026">July – August (war restart)</option>', '<option value="Q3-2026">July – August (war restart)</option>\n        <option value="Q4-2026">September – early November</option>', 'edition', 'period filter')

# ---------------------------------------------------------------- KPIs and money chart
rep(K, 'const DEAL_FLOW = 6.5; // USD bn, in-window new awards / reported frameworks (see chart foot)',
    'const DEAL_FLOW = 5.1; // USD bn, 26 Aug–8 Nov: Aramco–HUMAIN stake 2.6, SPPC batteries 1.16, MWAN opportunities ≈0.56 (SAR 2.1bn), Qiddiya arena + stadium package ≈0.77 (see chart foot)', 'edition', 'DEAL_FLOW')
rep(K, "note:'New deals this period (one $5.3 billion item unconfirmed) · cancellations not counted', noteAr:'صفقات جديدة في هذه الفترة (منها بند بقيمة 5.3 مليارات دولار غير مؤكد) · لا تُحتسب الإلغاءات'",
    "note:'New deals 26 Aug–8 Nov: HUMAIN stake, batteries, MWAN opportunities, Qiddiya and Expo awards · cancellations not counted', noteAr:'صفقات جديدة 26 أغسطس–8 نوفمبر: حصة هيومين، البطاريات، فرص موان، ترسيات القدية وإكسبو · لا تُحتسب الإلغاءات'", 'edition', 'KPI money note')
rep(K, "{accent:'#dc2626', num:'~$87', lab:'Oil price (Brent), close on 25/08', note:'About $92 on 24/08 as talks failed · ~$80 in early Aug when peace looked close', noteAr:'نحو 92 دولارًا في 24/08 مع فشل المحادثات · ونحو 80 دولارًا مطلع أغسطس حين بدا السلام قريبًا'}",
    "{accent:'#dc2626', num:'~$102', lab:'Oil price (Brent), close on 06/11', note:'October average about $108 · peak $117.6 on 30/10 after a mine strike in Hormuz · easing on US–Iran talks', noteAr:'متوسط أكتوبر نحو 108 دولارات · الذروة 117.6 في 30/10 بعد انفجار لغم في هرمز · تراجع مع المحادثات الأمريكية–الإيرانية'}", 'edition', 'KPI oil card')
rep(K, "const capData=[\n  {t:'AI & Data Centres (reported)', v:5.3},\n  {t:'Water & Desalination', v:0.69},\n  {t:'Tourism & Culture', v:0.49},\n];",
    "const capData=[\n  {t:'AI & Data Centres (Aramco–HUMAIN stake)', v:2.6},\n  {t:'Battery storage (SPPC group 1)', v:1.16},\n  {t:'Sport & Expo construction (Qiddiya, Riyadh)', v:0.77},\n  {t:'Waste facilities (MWAN opportunities)', v:0.56},\n];", 'edition', 'capData')
rep_re(K, r'<div class="chart-foot" data-eh-ar="[^"]*">Note: the \$5\.3 billion HUMAIN figure comes from a single news report and is unconfirmed\. This chart counts only new deals announced in the period — not cancelled contracts, long-running programmes or company results\.</div>',
       '<div class="chart-foot" data-eh-ar="ملاحظة: الرسم يحتسب الصفقات الجديدة المعلنة بين 26 أغسطس و8 نوفمبر فقط — لا العقود الملغاة ولا البرامج الممتدة ولا نتائج الشركات. قيمة صالة القدية تقدير صحفي (500–600 مليون دولار)، وفرص موان محوّلة من 2.1 مليار ريال.">Note: this chart counts only new deals announced between 26 August and 8 November — not cancelled contracts, long-running programmes or company results. The Qiddiya arena value is a trade-press estimate ($500–600 million); MWAN\'s opportunities are converted from SAR 2.1 billion. The $5.3 billion HUMAIN loan reported in May is still unconfirmed and no longer counted.</div>', 'edition', 'chart foot')

# ---------------------------------------------------------------- fact-check section
rep(K, '<span class="sh-sub">We re-checked every major claim from our 19 July report against sources — here are the verdicts, corrections and honest gaps</span>',
    '<span class="sh-sub">We re-checked all 24 claims from our 26 August report against sources — here are the verdicts, corrections, resolved gaps and the gaps we declare</span>', 'edition', 'audit sub')
i = FILES[K].index('const AUDIT = ['); j = FILES[K].index('];', i) + 2
FILES[K] = FILES[K][:i] + 'const AUDIT = [\n' + ',\n'.join(J(a) for a in T.AUDIT) + '\n];' + FILES[K][j:]; _log(K, 'exact', 'AUDIT', '24 verdicts', 'edition', 'AUDIT', 1, True)
i = FILES[K].index('const CORRECTIONS = ['); j = FILES[K].index('];', i) + 2
FILES[K] = FILES[K][:i] + 'const CORRECTIONS = [\n' + ',\n'.join(J(a) for a in T.CORRECTIONS) + '\n];' + FILES[K][j:]; _log(K, 'exact', 'CORRECTIONS', '9 rows', 'edition', 'CORRECTIONS', 1, True)
rep(K, "const VERDICT_CLASS = {'CONFIRMED':'v-conf','UPDATED':'v-upd','CLARIFIED':'v-clar'};\nconst VERDICT_LABEL = {'CONFIRMED':'CONFIRMED','UPDATED':'CONFIRMED · UPDATED','CLARIFIED':'CLARIFIED'};",
    "const VERDICT_CLASS = {'CONFIRMED':'v-conf','UPDATED':'v-upd','CLARIFIED':'v-clar','CONTRADICTED':'v-corr'};\nconst VERDICT_LABEL = {'CONFIRMED':'CONFIRMED','UPDATED':'CONFIRMED · UPDATED','CLARIFIED':'CLARIFIED','CONTRADICTED':'CONTRADICTED'};", 'edition', 'verdict classes')
rep(K, "  const counts = {CONFIRMED:0, UPDATED:0, CLARIFIED:0};\n  AUDIT.forEach(a=>counts[a.v]++);\n  document.getElementById('audit-banner').innerHTML =\n    `<span class=\"big\">${AUDIT.length} / ${AUDIT.length} claims checked out</span>",
    "  const counts = {CONFIRMED:0, UPDATED:0, CLARIFIED:0, CONTRADICTED:0};\n  AUDIT.forEach(a=>counts[a.v]++);\n  document.getElementById('audit-banner').innerHTML =\n    `<span class=\"big\">${AUDIT.length - counts.CONTRADICTED} / ${AUDIT.length} claims checked out</span>", 'edition', 'audit banner count')
rep(K, "     <span><span class=\"verdict v-clar\" style=\"justify-self:start\">${counts.CLARIFIED} CLARIFIED</span></span>\n     <span style=\"font-weight:600\">Nothing withdrawn · every major claim from our last report re-checked on 26 August</span>`;",
    "     <span><span class=\"verdict v-clar\" style=\"justify-self:start\">${counts.CLARIFIED} CLARIFIED</span></span>\n     <span><span class=\"verdict v-corr\" style=\"justify-self:start\">${counts.CONTRADICTED} CONTRADICTED</span></span>\n     <span style=\"font-weight:600\">One claim contradicted by events (Hormuz traffic) · all 24 claims re-checked on 8 November</span>`;", 'edition', 'audit banner text')
rep(K, "<span style=\"font-weight:600\">Verified against primary sources as of 26/08/2026</span>`;", "<span style=\"font-weight:600\">Verified against primary sources as of 08/11/2026</span>`;", 'edition', 'corr banner date')

# ---------------------------------------------------------------- big picture
i = FILES[K].index('<p class="lead">Six weeks of stand-off.'); j = FILES[K].index('    </div>\n  </section>', i)
FILES[K] = FILES[K][:i] + T.BIG_PICTURE_EN.lstrip() + FILES[K][j:]; _log(K, 'exact', 'Big Picture (26 Aug)', 'Big Picture (8 Nov)', 'edition', 'Big Picture', 1, True)
rep(K, '<span class="sh-sub">What it all adds up to — in six short reads</span>', '<span class="sh-sub">What it all adds up to — in eight short reads, including what to watch next</span>', 'edition', 'big picture sub')

# ---------------------------------------------------------------- Arabic edition
rep(K, '<div class="avnote">Environmental Horizons · الاستخبارات الاستراتيجية — نافذة الرصد 01/04/2026 – 26/08/2026 · أُصدر 26/08/2026 · سري — للاستخدام الاستراتيجي الداخلي</div>', T.AR_HEADER, 'ar', 'AR header')
i = FILES[K].index('<div class="avc"><b>مؤشرات هذه الدورة:</b>'); j = FILES[K].index('</div>', i) + 6
FILES[K] = FILES[K][:i] + T.AR_KPI + FILES[K][j:]; _log(K, 'exact', 'AR KPI line', 'v8 Nov', 'ar', 'AR KPI line', 1, True)
i = FILES[K].index('<h2>التحقّق: كيف صمد تقريرنا السابق؟</h2>\n<p>'); i2 = i + len('<h2>التحقّق: كيف صمد تقريرنا السابق؟</h2>\n'); j = FILES[K].index('</p>', i2) + 4
FILES[K] = FILES[K][:i2] + T.AR_AUDIT + FILES[K][j:]; _log(K, 'exact', 'AR audit paragraph', 'v8 Nov', 'ar', 'AR audit paragraph', 1, True)
rep(K, '<h2>أخبار الشركات <span class="avnote">(9 قصص موثّقة — بالنص الكامل)</span></h2>', '<h2>أخبار الشركات <span class="avnote">(19 قصة موثّقة — 9 بالنص الكامل من الدورات السابقة، و10 جديدة بصيغة موجزة)</span></h2>', 'ar', 'AR corp heading')
rep(K, '<h2>أخبار الحكومة والمشاريع العملاقة <span class="avnote">(15 قصة موثّقة — بالنص الكامل)</span></h2>', T.AR_CORP + '\n<h2>أخبار الحكومة والمشاريع العملاقة <span class="avnote">(29 قصة موثّقة — 15 بالنص الكامل من الدورات السابقة، و14 جديدة بصيغة موجزة)</span></h2>', 'ar', 'AR: new company stories + gov heading')
rep(K, '<p class="avnote">«بنود المراقبة» 🔴 — القصص الكبرى مجموعةً في جدول واحد', T.AR_GOV + '\n<p class="avnote">«بنود المراقبة» 🔴 — القصص الكبرى مجموعةً في جدول واحد', 'ar', 'AR: new government stories')
i = FILES[K].index('<h2>الصورة الكبرى — في ستّ قراءات قصيرة</h2>'); j = FILES[K].index('<h2>المنهجية وتغطية التحقق</h2>', i)
FILES[K] = FILES[K][:i] + T.AR_BIG + '\n' + FILES[K][j:]; _log(K, 'exact', 'AR big picture', 'v8 Nov', 'ar', 'AR big picture', 1, True)
i = FILES[K].index('<p>تُزاوج هذه الدورة'); j = FILES[K].index('</p>', i) + 4
FILES[K] = FILES[K][:i] + T.AR_METHOD + FILES[K][j:]; _log(K, 'exact', 'AR methodology', 'v8 Nov', 'ar', 'AR methodology', 1, True)
rep(K, '<b>اكتمل التعريب:</b> جميع القصص الأربع والعشرين مترجمة بنصّها الكامل أعلاه؛ وتبقى البطاقات التفاعلية والرسوم في النسخة الإنجليزية مرجعًا للأرقام.',
    '<b>التعريب:</b> قصص الدورات السابقة (24) مترجمة بنصّها الكامل أعلاه، والقصص الأربع والعشرون الجديدة بصيغة موجزة؛ وتبقى البطاقات التفاعلية والرسوم والمصادر في النسخة الإنجليزية مرجعًا للأرقام.', 'ar', 'AR footer note')

if FAILURES:
    for f in FAILURES: print('FAIL', f['note'], '|', f['old'][:160])
    sys.exit(1)
write_files(os.path.join(HERE, '..', 'hub'))
write_change_table(os.path.join(HERE, 'change_table_news_nov2026'), 'Corporate & Government News — 8 November 2026 update')
print('applied')
