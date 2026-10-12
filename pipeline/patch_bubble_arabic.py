"""patch_bubble_arabic.py — a full Arabic version of the Client Portfolio Bubble Map
(hub/EH_Client_Bubble_Map_CURRENT.html), 12 Oct 2026.

Until now the page had no Arabic: the hub's shared layer (eh-shared.js) calls ehBubbleLang('ar'|'en') when the hub
switches language, but the page never defined it, so Arabic readers saw the English page. This script adds it.

  • one dictionary, BUB_I18N, holds every word the page shows: the strings the charts write (English exactly as
    before, plus Arabic), the sector and service-family names, the deal-size buckets, the bridge/retention step
    names, the plural forms used with counts, the chart captions, and the Arabic for the static page text (whose
    English stays in the page markup and is read back when switching to English)
  • window.ehBubbleLang(l) swaps all of it, sets <html lang/dir>, remembers the choice in localStorage
    'ehhub.lang' (the hub's key), and redraws the bubble legend, the heatmap and the Executive charts; inside the hub
    the page starts in Arabic straight away when the hub was last left in Arabic
  • Arabic is formal business Arabic in the hub's own words (العملاء، القطاع، الإيرادات، ريال …); company names are
    kept exactly as stored; amounts read «12 مليون ريال» with Western digits; years, amounts and number ranges are
    isolated left-to-right so they never flip
  • right-to-left layout: the legend and the detail panel sit on the inline-end side and the panel slides in from
    there; the ranked charts (client concentration, retention, sector mix) mirror so bars start from the right; time
    and money axes (revenue bridge 2025 → 2026, deal size, depth vs value) stay left to right; the bubble pack is not
    mirrored. Chart SVGs keep a left-to-right base so anchors stay put, and Arabic phrases inside them are wrapped in
    right-to-left isolates so they read correctly
  • English output is unchanged: every English string the code writes is the same text as before

It also removes the hub shell's now-wrong code comment that the bubble chart "is a static English artifact", and adds
one line to pipeline/CHANGES.md under 2026-W42.

Run once:  python3 pipeline/patch_bubble_arabic.py
Restore:   git checkout -- hub/EH_Client_Bubble_Map_CURRENT.html hub/EH_Hub.html pipeline/CHANGES.md
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'EH_Client_Bubble_Map_CURRENT.html')
HUB = os.path.join(HERE, '..', 'hub', 'EH_Hub.html')
CH = os.path.join(HERE, 'CHANGES.md')
if 'id="bub-i18n"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'bub'); load(HUB, 'hub'); load(CH, 'changes')

LRI, RLI, PDI = '⁦', '⁧', '⁩'
def L(s):  # keep a number range or year pair left-to-right inside Arabic
    return LRI + s + PDI

# ---------------------------------------------------------------------------------------------------------------
# The dictionary (one source of truth). ui: [English exactly as the page wrote it, Arabic]; {0} {1} are filled in.
# ---------------------------------------------------------------------------------------------------------------
UI = {
 'proj_line_s':  [' project line', ''],
 'lines_lbl':    ['Lines:', 'عدد البنود:'],
 'unpriced_lbl': ['Service types without a priced amount:', 'أنواع خدمات بلا مبلغ مسعّر:'],
 'no_lines':     ['No lines in this year scope.', 'لا توجد بنود ضمن نطاق هذه السنة.'],
 'png_fail':     ['PNG export failed — please report this.', 'تعذّر تصدير الصورة — يُرجى الإبلاغ عن ذلك.'],
 'k_total':      ['Total book 25+26', 'إجمالي قيمة العقود 2025+2026'],
 'k_rev26':      ['2026 revenue', 'إيرادات 2026'],
 'k_active':     ['Active clients 2026', 'العملاء النشطون في 2026'],
 'k_ret':        ['Client retention', 'نسبة الاحتفاظ بالعملاء'],
 'k_top5':       ['Top-5 client share', 'حصة أكبر 5 عملاء'],
 'k_nrr':        ['Net revenue retention', 'صافي الاحتفاظ بالإيرادات'],
 'k_ws':         ['Whitespace cells', 'خلايا الفرص غير المستغلة'],
 'vs25':         [' vs 2025', ' مقارنة بعام 2025'],
 'kept':         ['{0} of {1} kept', '{0} من أصل {1} مستمرون'],
 'top1':         ['top 1 = {0}%', 'أكبر عميل = ' + L('{0}%')],
 'nrr_note':     ['2026 SAR from 2025 clients ÷ 2025 book', 'إيرادات 2026 من عملاء 2025 ÷ قيمة 2025'],
 'ws_note':      ['cross-sell targets', 'أهداف للبيع المتقاطع'],
 'scope':        ['Showing <b>{0}</b> only — Depth vs Value, Deal-Size and Whitespace are scoped to {0}; the Bridge, Retention and Sector-Shift cards always compare 2025 → 2026. &nbsp;',
                  'يُعرض عام <b>{0}</b> فقط — بطاقات عمق العلاقة مقابل القيمة وتوزيع أحجام الصفقات والفرص غير المستغلة مقصورة على {0}؛ أما بطاقات جسر الإيرادات والاحتفاظ بالعملاء وتحوّل القطاعات فتقارن دائماً ' + L('2025 → 2026') + '. &nbsp;'],
 'q_x':          ['How many jobs the client gives EH → (log scale)', '→ عدد المشاريع التي يُسندها العميل إلى EH (مقياس لوغاريتمي)'],
 'q_y':          ['Contract value with EH → (SAR, log scale)', '→ قيمة العقود مع EH (ريال، مقياس لوغاريتمي)'],
 'median':       ['median', 'الوسيط:'],
 'qS':           ['Strategic accounts', 'حسابات استراتيجية'],
 'qC':           ['Concentrated bets', 'رهانات مركّزة'],
 'qT':           ['Transactional volume', 'حجم المعاملات'],
 'qX':           ['Smaller accounts', 'حسابات أصغر'],
 'show_names':   ['Show all 60 names', 'عرض جميع الأسماء الستين'],
 'hide_names':   ['Hide names', 'إخفاء الأسماء'],
 'deal_note':    ['bars = client count · label % = share of total book value in that bucket', 'الأعمدة = عدد العملاء · النسبة = حصة الفئة من إجمالي قيمة العقود'],
 'of_book':      ['{0}% of book', L('{0}%') + ' من الإجمالي'],
 'ws_client':    ['Client', 'العميل'],
 'ws_value':     ['Value', 'القيمة'],
 'ws_top':       ['Top services (by value)', 'أبرز الخدمات (حسب القيمة)'],
 'ws_missing':   ['Not yet bought (whitespace)', 'لم يشترها بعد (فرص غير مستغلة)'],
 'ws_unclass':   ['project descriptions not classifiable', 'تعذّر تصنيف أوصاف المشاريع'],
 'more':         ['+{0} more', L('+{0}') + ' أخرى'],
 'net':          ['net', 'الصافي'],
 'impact26':     ['impact on 2026 revenue', 'الأثر على إيرادات 2026'],
 'clients_lbl':  ['Clients:', 'عدد العملاء:'],
 'pareto_sub':   ["Top 1 = {0}% · Top 5 = {1}% · Top 10 = {2}% of the two-year book — click a bar for that client's ledger",
                  'أكبر عميل = ' + L('{0}%') + ' · أكبر 5 عملاء = ' + L('{1}%') + ' · أكبر 10 عملاء = ' + L('{2}%') + ' من إجمالي العامين — انقر على أي عمود لعرض سجل ذلك العميل'],
 'cum':          ['{0}% cumulative', 'التراكمي ' + L('{0}%')],
 'share25':      ['2025 share', 'حصة 2025'],
 'share26':      ['2026 share', 'حصة 2026'],
 'pp':           ['pp', ' نقطة'],
 'ws_title':     ['Whitespace: no {0} sales into {1}', 'فرصة غير مستغلة: لا مبيعات من «{0}» لقطاع «{1}»'],
 'cell_n':       ['{0} ln · {1} co', '{0} بند · {1} عميل'],
 'M':            ['M', ' مليون'],
}
SEC = {
 'Power & Utilities': 'الكهرباء والمرافق', 'Government & Municipal': 'الجهات الحكومية والبلدية',
 'Construction & Contracting': 'البناء والمقاولات', 'Transport & Logistics': 'النقل والخدمات اللوجستية',
 'Engineering & Consultancy': 'الهندسة والاستشارات', 'Oil & Gas / Petrochemicals': 'النفط والغاز والبتروكيماويات',
 'Trading & Services': 'التجارة والخدمات', 'Manufacturing & Industrial': 'التصنيع والصناعة',
 'Steel & Metals': 'الحديد والمعادن', 'Cement & Building Materials': 'الأسمنت ومواد البناء',
 'Food & Agriculture': 'الأغذية والزراعة', 'Healthcare & Pharma': 'الرعاية الصحية والأدوية',
 'Other': 'أخرى', 'Oils & Lubricants': 'الزيوت ومواد التشحيم',
}
SVC = {
 'Chemical Waste': 'النفايات الكيميائية', 'Used Oils & Fuel Waste': 'الزيوت المستعملة ومخلفات الوقود',
 'Industrial Wastewater & Sludge': 'مياه الصرف الصناعي والحمأة', 'Soil, Asbestos & Remediation': 'التربة والأسبستوس والمعالجة',
 'Monitoring, Sampling & Analysis': 'الرصد وأخذ العينات والتحليل', 'Env. Studies, Permits & Consulting': 'الدراسات البيئية والتصاريح والاستشارات',
 'Product & Goods Destruction': 'إتلاف المنتجات والبضائع', 'Landfill & Final Disposal': 'الردم والتخلص النهائي',
 'Transport, Handling & Containers': 'النقل والمناولة والحاويات', 'Cleaning & Emergency Response': 'التنظيف والاستجابة للطوارئ',
 'Civil, Marine & EPC Works': 'الأعمال المدنية والبحرية (EPC)', 'Contract Fees & Retainers': 'رسوم العقود والاشتراكات',
 'Industrial & Solid Waste': 'النفايات الصناعية والصلبة', 'Other': 'أخرى',
}
DEAL = {
 '< 25K': 'أقل من 25 ألف', '25–100K': L('25–100') + ' ألف', '100–500K': L('100–500') + ' ألف',
 '0.5–2M': L('0.5–2') + ' مليون', '2–10M': L('2–10') + ' ملايين', '> 10M': 'أكثر من 10 ملايين',
}
STEP = {
 'New clients': 'عملاء جدد', 'Expansion': 'نمو العملاء الحاليين', 'Contraction': 'تراجع العملاء الحاليين',
 'Churn': 'عملاء متوقفون', 'Retained': 'عملاء مستمرون', 'New in 2026': 'جدد في 2026', 'Lost after 2025': 'متوقفون بعد 2025',
 '2026 value': 'قيمة 2026', '2025 value not repeated': 'قيمة 2025 التي لم تتكرر',
}
# Arabic counted nouns: [1, 2, 3–10, 11–99, 100+ / 0]
PL = {
 'client': ['عميل واحد', 'عميلان', 'عملاء', 'عميلاً', 'عميل'],
 'line':   ['بند واحد', 'بندان', 'بنود', 'بنداً', 'بند'],
 'proj':   ['مشروع واحد', 'مشروعان', 'مشاريع', 'مشروعاً', 'مشروع'],
}
CAP = {
 'svgBridge': 'يُقرأ من اليسار إلى اليمين: إجمالي العام الماضي، ثم العملاء الذين أضافوا قيمة أو فقدوها، وصولاً إلى إجمالي هذا العام.',
 'svgPareto': 'يوضح المنحنى أن عدداً قليلاً من العملاء يشكّل معظم القيمة — وكلما كانت بدايته أشد انحداراً زاد اعتماد آفاق البيئة على عدد محدود من الأسماء.',
 'svgRet': 'الأشرطة الخضراء عملاء احتُفظ بهم أو اكتُسبوا بين العامين، والحمراء عملاء فُقدوا — والتوازن بينهما هو الخلاصة.',
 'svgSlope': 'كل خط يمثل قطاعاً: الخطوط الصاعدة نالت حصة أكبر من الإيرادات هذا العام، والهابطة حصة أصغر.',
 'svgQuad': 'أعلى اليمين هو الأفضل — عملاء يشترون خدمات كثيرة وينفقون كثيراً؛ وأسفل اليمين عملاء ينفقون كثيراً لكنهم يشترون خدمة أو خدمتين فقط ويمكنهم شراء المزيد.',
 'svgDeal': 'يقع معظم العملاء في فئات الصفقات الصغيرة على اليسار، بينما تحمل القلة على اليمين حصة كبيرة من القيمة.',
}
QUAD_SUB = ('أعلى 60 عميلاً حسب القيمة. اليمين = يُسند إلى EH <b>مشاريع كثيرة</b>؛ والأعلى = <b>قيمة مالية كبيرة</b>. '
 'الخطان المتقطعان يمثلان وسيط هذه المجموعة ويقسمان العملاء إلى أربع فئات — انقر أو مرّر المؤشر على أي نقطة لعرض الاسم والأرقام.\n'
 '      <div style="margin-top:6px;font-size:11.5px;line-height:1.7">\n'
 '      <span style="color:#1F7A4C;font-weight:700">&#9679; حسابات استراتيجية</span> — مشاريع كثيرة <i>و</i>قيمة كبيرة: حافظوا على هذه العلاقات. &nbsp;\n'
 '      <span style="color:#B8860B;font-weight:700">&#9679; رهانات مركّزة</span> — قيمة كبيرة من مشاريع قليلة: خسارة عقد واحد مؤلمة، فعمّقوا العلاقة. &nbsp;\n'
 '      <span style="color:#1A5FAB;font-weight:700">&#9679; حجم المعاملات</span> — مشاريع صغيرة كثيرة: خدمتها فعّالة، وهي أفضل أهداف البيع المتقاطع. &nbsp;\n'
 '      <span style="color:#8A99A3;font-weight:700">&#9679; حسابات أصغر</span> — مشاريع قليلة وصغيرة.\n'
 '      </div>')
# static page text: [selector, how, Arabic]; the English is read from the page before the first switch
ST = [
 ['document', 'doc', 'محفظة عملاء آفاق البيئة — خريطة الفقاعات'],
 ['header h1', 'html', '<b>آفاق البيئة</b> · خريطة فقاعات محفظة العملاء'],
 ['.kpis>span:nth-child(1)', 'tail', 'الشركات'],
 ['.kpis>span:nth-child(2)', 'tail', 'إجمالي قيمة العقود'],
 ['.kpis>span:nth-child(3)', 'tail', 'بنود المشاريع'],
 ['#viewSeg [data-v=bubbles]', 'text', 'خريطة الفقاعات'],
 ['#viewSeg [data-v=heat]', 'text', 'خريطة حرارية: القطاع × الخدمة'],
 ['#viewSeg [data-v=exec]', 'text', 'الملخص التنفيذي'],
 ['#yearSeg [data-y=both],.ytog [data-y=both]', 'text', 'العامان'],
 ['.ytog', 'aria', 'نطاق السنة'],
 ['#search', 'ph', 'ابحث عن شركة…'],
 ['#reset', 'text', 'إعادة ضبط العرض'],
 ['.toolbar .hint', 'text', 'مرّر للتكبير · اسحب للتنقل · انقر على فقاعة لعرض مشاريعها وخدماتها · انقر على قطاع للتصفية'],
 ['#execYearNote', 'tail', 'الرسوم تفاعلية: مرّر للتكبير · اسحب للتنقل · انقر مرتين لإعادة الضبط · زر PNG ⬇ يصدّر العرض الحالي.'],
 ['.egrid>.ecard:nth-child(1)>.eh2', 'head', 'جسر الإيرادات · ' + L('2025 → 2026') + ' '],
 ['.egrid>.ecard:nth-child(2)>.eh2', 'head', 'تركّز العملاء '],
 ['.egrid>.ecard:nth-child(3)>.eh2', 'head', 'الاحتفاظ بالعملاء · ' + L('2025 → 2026') + ' '],
 ['.egrid>.ecard:nth-child(4)>.eh2', 'head', 'تحوّل مزيج القطاعات · الحصة من الإيرادات '],
 ['.egrid>.ecard:nth-child(5)>.eh2', 'head', 'عمق العلاقة مقابل القيمة '],
 ['.egrid>.ecard:nth-child(6)>.eh2', 'head', 'توزيع أحجام الصفقات '],
 ['.egrid>.ecard:nth-child(7)>.eh2', 'head', 'قائمة الفرص غير المستغلة · أهداف البيع المتقاطع '],
 ['.ecard .png[data-svg]', 'text', 'تصدير PNG'],
 ['.egrid>.ecard:nth-child(1)>.esub', 'text', 'ما الذي أحدث التغيير — انقر على أي عمود لعرض أسماء العملاء خلفه'],
 ['.egrid>.ecard:nth-child(3)>.esub', 'text', 'حركة العملاء بين العامين — انقر على أي شريط لعرض الأسماء'],
 ['.egrid>.ecard:nth-child(4)>.esub', 'text', 'النقطة المفرغة = حصة 2025 · النقطة الممتلئة = حصة 2026 · الأخضر/الأحمر = حصة مكتسبة أو مفقودة'],
 ['.egrid>.ecard:nth-child(5)>.esub', 'html', QUAD_SUB],
 ['.egrid>.ecard:nth-child(6)>.esub', 'text', 'العملاء مصنّفون حسب متوسط حجم الصفقة (إجمالي القيمة ÷ إجمالي المشاريع)'],
 ['.egrid>.ecard:nth-child(7)>.esub', 'html', 'أبرز خدمات كل عميل رئيسي (بالأزرق، مع حصتها من إنفاقه) بجانب خدمات آفاق البيئة التي <b>لم</b> يشترها قط (بالأخضر) — مصنّفة بالكلمات المفتاحية من أوصاف المشاريع'],
 ['#execWrap>.enote', 'text', 'تغطية البيانات: بنود السجل المسعّرة فقط. البنود التي لا تحمل مبلغاً بالريال (خدمات نُفّذت أو حُدّد نطاقها دون تسجيل سعر) مستبعدة من جميع أرقام هذه الصفحة.'],
 ['#heatWrap>.heatnote', 'html', 'لون الخلية = قيمة العقود (مقياس الجذر التربيعي √) · <b>الخلايا المتقطعة فرص غير مستغلة</b>: لا مبيعات مسجّلة لآفاق البيئة من فئة الخدمة هذه في هذا القطاع · انقر على خلية ممتلئة لعرض قائمة العملاء.'],
 ['.zctl', 'aria', 'أدوات التكبير'],
 ['.zctl button:nth-child(1)', 'aria', 'تكبير'],
 ['.zctl button:nth-child(2)', 'aria', 'تصغير'],
 ['.zctl button:nth-child(3)', 'aria', 'إعادة ضبط التكبير'],
 ['.zctl button:nth-child(3)', 'title', 'إعادة ضبط التكبير'],
 ['#legend h3', 'text', 'القطاع'],
 ['footer', 'text', 'مساحة الفقاعة = إجمالي قيمة العقود. البنود المسعّرة فقط (البنود التي لا تحمل مبلغاً بالريال مستبعدة). القطاعات مستنتجة آلياً من أسماء الشركات — ويمكن تعديلها في سكربت البناء عند الحاجة.'],
 ['#pclose', 'title', 'إغلاق'],
 ['.sr-only caption', 'text', 'محفظة العملاء حسب إجمالي قيمة العقود (' + L('2025–2026') + ')'],
 ['.sr-only th:nth-child(1)', 'text', 'العميل'],
 ['.sr-only th:nth-child(2)', 'text', 'الإجمالي (ريال)'],
 ['.sr-only th:nth-child(3)', 'text', 'المشاريع'],
 ['svg[aria-label]', 'aria', 'رسم فقاعي لمحفظة العملاء؛ مساحة كل فقاعة تتناسب مع قيمة العقود، ويليه جدول مرتّب بالبيانات نفسها لقارئات الشاشة.'],
]
DICT = {'ui': UI, 'sec': SEC, 'svc': SVC, 'deal': DEAL, 'step': STEP, 'pl': PL, 'cap': CAP, 'st': ST}
DICT_JS = json.dumps(DICT, ensure_ascii=True, indent=None, separators=(',', ':'))   # \uXXXX escapes: Arabic and isolates survive any re-encoding

I18N = r'''<script id="bub-i18n">
/* Arabic version (patch_bubble_arabic.py, 12 Oct 2026). BUB_I18N is the page's one dictionary:
   ui = [English exactly as the page always wrote it, Arabic] ({0},{1} are filled in), sec/svc/deal/step = names,
   pl = Arabic counted nouns, cap = Arabic chart captions, st = Arabic for the static page text (its English is the
   markup itself, read back when switching to English). window.ehBubbleLang('ar'|'en') is called by eh-shared.js. */
var BUB_LANG='en', BUB_SNAP=[];
const BUB_I18N=__DICT__;
const BUB_RLI='⁧', BUB_LRI='⁦', BUB_FSI='⁨', BUB_PDI='⁩';
function bT(k){ var e=BUB_I18N.ui[k]; return e?e[BUB_LANG==='ar'?1:0]:k; }
function bF(k){ var a=arguments; return bT(k).replace(/\{(\d)\}/g,function(m,i){ return a[+i+1]; }); }
function bMap(m,k){ return (BUB_LANG==='ar'&&BUB_I18N[m][k])||k; }
function bTS(s){ return bMap('sec',s); }
function bTV(s){ return bMap('svc',s); }
function bidiAr(s){ return BUB_LANG==='ar'?BUB_RLI+s+BUB_PDI:s; }      /* Arabic phrase inside a left-to-right chart */
function bidiName(s){ return BUB_LANG==='ar'?BUB_FSI+s+BUB_PDI:s; }   /* a company name, whichever script it is in */
function bCount(n,w){ var f=BUB_I18N.pl[w], m=n%100; if(n===1)return f[0]; if(n===2)return f[1]; return n+' '+(m>=3&&m<=10?f[2]:m>=11?f[3]:f[4]); }
function bubFmtAr(v,sg,cur){ var n,u='';
  if(v>=1e6){ n=(v/1e6).toFixed(v>=1e7?0:1); u='مليون'; } else if(v>=1e3){ n=(v/1e3).toFixed(0); u='ألف'; } else n=v.toFixed(0);
  var w=[u,cur?'ريال':''].filter(Boolean).join(' ');
  return BUB_RLI+BUB_LRI+(sg||'')+n+BUB_PDI+(w?' '+w:'')+BUB_PDI; }
/* amount with optional sign, with or without the currency word; English is the page's original wording */
function bubAmt(v,signed,cur){ var sg=signed?(v>=0?"+":"−"):"";
  if(BUB_LANG==='ar') return bubFmtAr(Math.abs(v),sg,cur);
  var s=fmt(Math.abs(v)); return sg+(cur?s:s.replace("SAR ","")); }
function bPct(n){ return BUB_LANG==='ar'?BUB_LRI+n+'%'+BUB_PDI:n+'%'; }
function bubMTick(v){ var n=(v/1e6).toFixed(0); return BUB_LANG==='ar'?bidiAr(n+bT('M')):n+"M"; }
function bubCap(id){ return (BUB_LANG==='ar'&&BUB_I18N.cap[id])||EH_BUB_CAPS[id]; }
function bubNode(el,m){ var n;
  if(m==='tail'){ for(n=el.lastChild;n;n=n.previousSibling) if(n.nodeType===3&&n.nodeValue.trim()) return n; }
  else for(n=el.firstChild;n;n=n.nextSibling) if(n.nodeType===3&&n.nodeValue.trim()) return n;
  return null; }
function bubGet(el,m){
  if(m==='doc') return document.title; if(m==='html') return el.innerHTML; if(m==='text') return el.textContent;
  if(m==='ph') return el.placeholder; if(m==='aria') return el.getAttribute('aria-label'); if(m==='title') return el.getAttribute('title');
  var n=bubNode(el,m); return n?n.nodeValue:null; }
function bubSet(el,m,v){ if(v==null) return;
  if(m==='doc') document.title=v; else if(m==='html') el.innerHTML=v; else if(m==='text') el.textContent=v;
  else if(m==='ph') el.placeholder=v; else if(m==='aria') el.setAttribute('aria-label',v); else if(m==='title') el.setAttribute('title',v);
  else { var n=bubNode(el,m); if(n) n.nodeValue=v; } }
function bubEls(r){ return r[0]==='document'?[document]:[].slice.call(document.querySelectorAll(r[0])); }
function bubSnap(){ BUB_I18N.st.forEach(function(r,i){ BUB_SNAP[i]=bubEls(r).map(function(el){ return bubGet(el,r[1]); }); }); }
function bubStatic(l){ BUB_I18N.st.forEach(function(r,i){ bubEls(r).forEach(function(el,j){ bubSet(el,r[1],l==='ar'?r[2]:(BUB_SNAP[i]||[])[j]); }); }); }
window.ehBubbleLang=function(l){
  l=(l==='ar')?'ar':'en';
  if(l===BUB_LANG) return;
  if(l==='ar') bubSnap();                      /* read the English page text before anything changes */
  BUB_LANG=l;
  var h=document.documentElement; h.lang=l; h.dir=(l==='ar'?'rtl':'ltr');
  bubStatic(l);
  var ql=document.getElementById('quadList'), qb=document.getElementById('quadListBtn');
  if(ql&&qb) qb.textContent=bT(ql.style.display==='none'?'show_names':'hide_names');
  document.querySelectorAll('.eh-caption[data-for]').forEach(function(c){ c.textContent=bubCap(c.getAttribute('data-for')); });
  try{ localStorage.setItem('ehhub.lang',l); }catch(e){}
  var keep=panelCompany;
  try{ render(); if(viewMode==='heat') renderHeat(); else if(viewMode==='exec') renderExec(); }catch(e){}
  var c=keep&&DATA.find(function(d){ return d.name===keep; });
  if(c&&val(c)>0) showPanel(c); else closePanel();
};
/* inside the hub, start in the hub's language straight away (eh-shared.js also posts it a moment later) */
document.addEventListener('DOMContentLoaded',function(){
  try{ var emb=document.documentElement.classList.contains('inframe')||/[?&]embedded=1/.test(location.search);
    if(emb&&localStorage.getItem('ehhub.lang')==='ar') window.ehBubbleLang('ar'); }catch(e){}
});
</script>
'''.replace('__DICT__', DICT_JS)
RTL_CSS = '''<style id="eh-bub-ar">
/* Arabic / right-to-left (patch_bubble_arabic.py) */
html[dir=rtl] #execWrap svg{direction:ltr}            /* chart anchors stay put; Arabic phrases inside are RTL isolates */
html[dir=rtl] .zctl{right:auto;left:10px}
html[lang=ar] .kcard .kv{font-size:22px}
html[lang=ar] td.hc{width:88px;min-width:88px}
html[lang=ar] td.hc small{white-space:nowrap}
html[dir=rtl] .sv small.meta{text-align:right}
html[dir=rtl] #tip{text-align:right}
html[dir=rtl] #wsList td,html[dir=rtl] #wsList th{text-align:right}
@media(min-width:769px){
  html[lang=ar] #legend{width:300px}
  html[dir=rtl] #panel{right:auto;left:0;transform:translateX(calc(-100% - 32px));box-shadow:10px 0 30px -12px rgba(13,23,54,.35)}
  html[dir=rtl] #panel.open{transform:none}
  html[dir=rtl] body.dark #panel{box-shadow:10px 0 30px -10px rgba(0,0,0,.6)}
}
@media(max-width:820px){
  html[dir=rtl] .ecard .eh2,html[dir=rtl] .ecard .esub,html[dir=rtl] .ecard .heatnote{left:auto;right:0}
  html[lang=ar] .ecard::after{content:"⟷ اسحب الرسم"}
}
</style>
'''

# ---------------- page: dictionary, RTL styles ----------------
rep('bub', '</style>\n</head>', '</style>\n' + RTL_CSS + '</head>', 'arabic', 'RTL styles: panel slides from the inline end, zoom buttons and notes mirror')
rep('bub', '</aside>\n\n<script>\nconst DATA = [', '</aside>\n\n' + I18N + '<script>\nconst DATA = [', 'arabic', 'the dictionary and ehBubbleLang(), before the page script')

# ---------------- page script: every string it writes goes through the dictionary ----------------
rep('bub', '''const fmt = v => {
  if (v >= 1e6)''', '''const fmt = v => {
  if (BUB_LANG === "ar") return bubFmtAr(v, "", true);
  if (v >= 1e6)''', 'arabic', 'amounts in Arabic: «12 مليون ريال», Western digits, isolated')
rep('bub', '''        <div class="s">${d.data.sector}</div>
        <div>${fmt(val(d.data))} · ${proj(d.data)} project line${proj(d.data)>1?"s":""}</div>''',
    '''        <div class="s">${bTS(d.data.sector)}</div>
        <div>${fmt(val(d.data))} · ${BUB_LANG==="ar" ? bCount(proj(d.data),"line") : proj(d.data)+bT("proj_line_s")+(proj(d.data)>1?"s":"")}</div>''',
    'arabic', 'bubble tooltip: sector and line count')
rep('bub', '''` : ""}`;
    })
    .on("mouseleave"''', '''` : ""}`;
      if (BUB_LANG==="ar") tip.style.left = Math.max(8, e.clientX-14-tip.offsetWidth) + "px";
    })
    .on("mouseleave"''', 'arabic', 'tooltip opens to the left of the pointer in Arabic')
rep('bub', 'lgAll.select(".nm").text(d => d[0]);', 'lgAll.select(".nm").text(d => bTS(d[0]));', 'arabic', 'legend sector names')
rep('bub', 'document.getElementById("psec").textContent = comp.sector;', 'document.getElementById("psec").textContent = bTS(comp.sector);', 'arabic', 'detail panel sector')
rep('bub', '''  document.getElementById("ptot").innerHTML =
    `<b>${fmt(d3.sum(priced, l => l.v))}</b> across''', '''  document.getElementById("ptot").innerHTML = BUB_LANG==="ar" ?
    `<b>${fmt(d3.sum(priced, l => l.v))}</b> · ${bT("lines_lbl")} <b>${d3.sum(lines, l => l.n)}</b>` +
    (lines.length > priced.length ? ` · ${bT("unpriced_lbl")} ${lines.length - priced.length}` : "") :
    `<b>${fmt(d3.sum(priced, l => l.v))}</b> across''', 'arabic', 'detail panel total line')
rep('bub', '`<div class="pline"><span class="sv">No lines in this year scope.</span></div>`;',
    '`<div class="pline"><span class="sv">${bT("no_lines")}</span></div>`;', 'arabic', 'detail panel empty state')
rep('bub', 'img.onerror = () => alert("PNG export failed — please report this.");', 'img.onerror = () => alert(bT("png_fail"));', 'arabic', 'PNG export error')
rep('bub', '''    ["Total book 25+26", fmt(tAll), null],
    ["2026 revenue", fmt(t26), (yoy>=0?"▲ ":"▼ ") + Math.round(Math.abs(yoy)*100) + "% vs 2025", yoy>=0],
    ["Active clients 2026", c26.length, (c26.length>=c25.length?"▲ ":"▼ ") + Math.abs(c26.length-c25.length) + " vs 2025", c26.length>=c25.length],
    ["Client retention", Math.round(100*ret.length/c25.length) + "%", ret.length + " of " + c25.length + " kept", true],
    ["Top-5 client share", Math.round(top5*100) + "%", "top 1 = " + Math.round(top1*100) + "%", false],
    ["Net revenue retention", Math.round(100*d3.sum(ret, d=>d.v2026)/t25) + "%", "2026 SAR from 2025 clients ÷ 2025 book", d3.sum(ret,d=>d.v2026)>=t25],
    ["Whitespace cells", ws, "cross-sell targets", true],''',
    '''    [bT("k_total"), fmt(tAll), null],
    [bT("k_rev26"), fmt(t26), (yoy>=0?"▲ ":"▼ ") + Math.round(Math.abs(yoy)*100) + "%" + bT("vs25"), yoy>=0],
    [bT("k_active"), c26.length, (c26.length>=c25.length?"▲ ":"▼ ") + Math.abs(c26.length-c25.length) + bT("vs25"), c26.length>=c25.length],
    [bT("k_ret"), Math.round(100*ret.length/c25.length) + "%", bF("kept", ret.length, c25.length), true],
    [bT("k_top5"), Math.round(top5*100) + "%", bF("top1", Math.round(top1*100)), false],
    [bT("k_nrr"), Math.round(100*d3.sum(ret, d=>d.v2026)/t25) + "%", bT("nrr_note"), d3.sum(ret,d=>d.v2026)>=t25],
    [bT("k_ws"), ws, bT("ws_note"), true],''', 'arabic', 'Executive KPI tiles')
rep('bub', '''    : 'Showing <b>'+yearMode+'</b> only — Depth vs Value, Deal-Size and Whitespace are scoped to '+yearMode+
      '; the Bridge, Retention and Sector-Shift cards always compare 2025 → 2026. &nbsp;';''',
    '''    : bF("scope", yearMode);''', 'arabic', 'Executive year-scope note')
rep('bub', 'const axY=root.select(".qax-y").call(d3.axisLeft(py).ticks(6,"~s").tickSizeOuter(0));',
    'const _fq=py.tickFormat(6,"~s");\n  const axY=root.select(".qax-y").call(BUB_LANG==="ar" ? d3.axisLeft(py).ticks(6).tickFormat(v=>_fq(v)?bubAmt(v,false,false):"").tickSizeOuter(0) : d3.axisLeft(py).ticks(6,"~s").tickSizeOuter(0));',
    'arabic', 'depth vs value: money axis in Arabic units')
rep('bub', 'function t_axis(){return "How many jobs the client gives EH \\u2192 (log scale)";}',
    'function t_axis(){return bidiAr(bT("q_x"));}', 'arabic', 'depth vs value: x-axis title')
rep('bub', '.text("Contract value with EH \\u2192 (SAR, log scale)");', '.text(bidiAr(bT("q_y")));', 'arabic', 'depth vs value: y-axis title')
rep('bub', '.text("median "+medP+" projects")', '.text(BUB_LANG==="ar" ? bidiAr(bT("median")+" "+bCount(medP,"proj")) : "median "+medP+" projects")', 'arabic', 'median guide label (projects)')
rep('bub', '.text("median "+fmt(medV))', '.text(bidiAr(bT("median")+" "+fmt(medV)))', 'arabic', 'median guide label (value)')
rep('bub', '''  const QL=[["Strategic accounts ("+QN.S+")",W-M.r-6,M.t+14,"end","S"],
            ["Concentrated bets ("+QN.C+")",M.l+10,M.t+14,"start","C"],
            ["Transactional volume ("+QN.T+")",W-M.r-6,H-M.b-10,"end","T"],
            ["Smaller accounts ("+QN.X+")",M.l+10,H-M.b-10,"start","X"]];''',
    '''  const QL=[[bidiAr(bT("qS")+" ("+QN.S+")"),W-M.r-6,M.t+14,"end","S"],
            [bidiAr(bT("qC")+" ("+QN.C+")"),M.l+10,M.t+14,"start","C"],
            [bidiAr(bT("qT")+" ("+QN.T+")"),W-M.r-6,H-M.b-10,"end","T"],
            [bidiAr(bT("qX")+" ("+QN.X+")"),M.l+10,H-M.b-10,"start","X"]];''', 'arabic', 'quadrant headings')
rep('bub', 'd3.select(this).select("title").text(d.n+"\\n"+d.p+" projects \\u00b7 "+fmt(d.v));',
    'd3.select(this).select("title").text(d.n+"\\n"+(BUB_LANG==="ar"?bCount(d.p,"proj"):d.p+" projects")+" \\u00b7 "+fmt(d.v));', 'arabic', 'dot hover title')
rep('bub', '''      .attr("fill",TXT).attr("stroke",HALO)
      .text(o=>o.nm)''', '''      .attr("fill",TXT).attr("stroke",HALO)
      .text(o=>bidiName(o.nm))''', 'arabic', 'dot name labels read in their own script')
rep('bub', 'const QTITLE={S:"Strategic accounts",C:"Concentrated bets",T:"Transactional volume",X:"Smaller accounts"};',
    'const QTITLE={S:bT("qS"),C:bT("qC"),T:bT("qT"),X:bT("qX")};', 'arabic', 'full name list headings')
rep('bub', '''<span style="opacity:.65">\\u2014 '+d.p+' jobs \\u00b7 '+fmt(d.v)+'</span>''',
    '''<span style="opacity:.65">\\u2014 '+(BUB_LANG==="ar"?bCount(d.p,"proj"):d.p+' jobs')+' \\u00b7 '+fmt(d.v)+'</span>''', 'arabic', 'full name list counts')
rep('bub', 'b.textContent=show?"Hide names":"Show all 60 names";', 'b.textContent=bT(show?"hide_names":"show_names");', 'arabic', 'show/hide names button')
rep('bub', 'const axX=root.select(".deal-ax-x").call(d3.axisBottom(x).tickSizeOuter(0));',
    'const axX=root.select(".deal-ax-x").call(d3.axisBottom(x).tickSizeOuter(0).tickFormat(k=>BUB_LANG==="ar"?bidiAr(bMap("deal",k)):k));', 'arabic', 'deal-size bucket names')
rep('bub', 'root.select(".deal-note").attr("fill",SUB).text("bars = client count · label % = share of total book value in that bucket");',
    'root.select(".deal-note").attr("fill",SUB).attr("x",BUB_LANG==="ar"?W-M.r:M.l).attr("text-anchor",BUB_LANG==="ar"?"end":null).text(bidiAr(bT("deal_note")));', 'arabic', 'deal-size note (right-aligned in Arabic)')
rep('bub', 'bAll.select("title").text(a=>a.c+" clients · "+fmt(a.val)+" ("+pct(a)+"% of book)");',
    'bAll.select("title").text(a=>(BUB_LANG==="ar"?bCount(a.c,"client"):a.c+" clients")+" · "+fmt(a.val)+" ("+bF("of_book",pct(a))+")");', 'arabic', 'deal-size bar hover')
rep('bub', '''   '<thead><tr style="text-align:left;color:#5F7078"><th style="padding:6px 8px">Client</th><th style="padding:6px 8px">Value</th><th style="padding:6px 8px">Top services (by value)</th><th style="padding:6px 8px">Not yet bought (whitespace)</th></tr></thead><tbody>'+''',
    '''   '<thead><tr style="text-align:start;color:#5F7078"><th style="padding:6px 8px">'+bT("ws_client")+'</th><th style="padding:6px 8px">'+bT("ws_value")+'</th><th style="padding:6px 8px">'+bT("ws_top")+'</th><th style="padding:6px 8px">'+bT("ws_missing")+'</th></tr></thead><tbody>'+''',
    'arabic', 'whitespace table headings (aligned to the start side)')
rep('bub', '''font-style:italic">project descriptions not classifiable</span>')+r.top.map(t=>chip(t[0]+' \\u00b7 '+Math.round(100*t[1]/r.val)+'%',''',
    '''font-style:italic">'+bT("ws_unclass")+'</span>')+r.top.map(t=>chip(bTV(t[0])+' \\u00b7 '+bPct(Math.round(100*t[1]/r.val)),''', 'arabic', 'whitespace top services')
rep('bub', '''r.missing.slice(0,4).map(c=>chip(c,'#EFF6F1','#D5E6DA','#1F7A4C')).join('')+(r.missing.length>4?' <span style="color:#8A99A3">+'+(r.missing.length-4)+' more</span>':'')''',
    '''r.missing.slice(0,4).map(c=>chip(bTV(c),'#EFF6F1','#D5E6DA','#1F7A4C')).join('')+(r.missing.length>4?' <span style="color:#8A99A3">'+bF("more",r.missing.length-4)+'</span>':'')''', 'arabic', 'whitespace services not yet bought')
# revenue bridge (stays left to right: it reads 2025 → 2026)
rep('bub', '''  const svg = svgBase("svgBridge");
  svg.append("g").attr("transform",`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickFormat(v=>(v/1e6).toFixed(0)+"M"))''',
    '''  const svg = svgBase("svgBridge");
  svg.append("g").attr("transform",`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickFormat(bubMTick))''', 'arabic', 'bridge axis: millions')
rep('bub', '''          .map(d => ({name: d.name, meta: p.l==="New clients"?"":`${fmt(d.v2025)} → ${fmt(d.v2026)}`,
                      amt: (p.key(d)>=0?"+":"−") + fmt(Math.abs(p.key(d)))}));
        showListPanel(p.l, `${p.items.length} clients · net ${p.v>=0?"+":"−"}${fmt(Math.abs(p.v))}`, p.c,
          `<b>${p.v>=0?"+":"−"}${fmt(Math.abs(p.v))}</b> impact on 2026 revenue`, its);''',
    '''          .map(d => ({name: d.name, meta: p.l==="New clients"?"":`${fmt(d.v2025)} → ${fmt(d.v2026)}`,
                      amt: bubAmt(p.key(d), true, true)}));
        showListPanel(bMap("step",p.l), BUB_LANG==="ar" ? `${bCount(p.items.length,"client")} · ${bT("net")} ${bubAmt(p.v,true,true)}` : `${p.items.length} clients · net ${p.v>=0?"+":"−"}${fmt(Math.abs(p.v))}`, p.c,
          `<b>${bubAmt(p.v,true,true)}</b> ${bT("impact26")}`, its);''', 'arabic', 'bridge click-through panel')
rep('bub', '''      .text((p.abs?"":(p.v>=0?"+":"−")) + fmt(Math.abs(p.v)).replace("SAR ",""));''',
    '''      .text(bubAmt(p.v, !p.abs, false));''', 'arabic', 'bridge bar values')
rep('bub', '''.attr("text-anchor","middle").attr("font-size","12.5px").attr("fill","#5E6B80").text(p.l);''',
    '''.attr("text-anchor","middle").attr("font-size","12.5px").attr("fill","#5E6B80").text(bidiAr(bMap("step",p.l)));''', 'arabic', 'bridge step names')
# client concentration (Pareto): mirrors in Arabic — largest client on the right, value axis on the right
rep('bub', '''    `Top 1 = ${Math.round(top1*100)}% · Top 5 = ${Math.round(top5*100)}% · Top 10 = ${Math.round(top10*100)}% of the two-year book — click a bar for that client's ledger`;''',
    '''    bF("pareto_sub", Math.round(top1*100), Math.round(top5*100), Math.round(top10*100));''', 'arabic', 'concentration subtitle')
rep('bub', '''  const W=960, H=440, m={t:24,r:60,b:112,l:78};
  const x = d3.scaleBand().domain(top.map(d=>d.name)).range([m.l, W-m.r]).padding(0.25);''',
    '''  const RT=BUB_LANG==="ar", W=960, H=440, m=RT?{t:24,r:78,b:112,l:60}:{t:24,r:60,b:112,l:78};
  const x = d3.scaleBand().domain(top.map(d=>d.name)).range(RT?[W-m.r, m.l]:[m.l, W-m.r]).padding(0.25);''', 'arabic', 'concentration: mirrored order in Arabic')
rep('bub', '''  svg.append("g").attr("transform",`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickFormat(v=>(v/1e6).toFixed(0)+"M"))
     .attr("font-size","12px").attr("color","#5E6B80");
  svg.append("g").attr("transform",`translate(${W-m.r},0)`).call(d3.axisRight(yp).ticks(5).tickFormat(v=>v+"%"))''',
    '''  svg.append("g").attr("transform",`translate(${RT?W-m.r:m.l},0)`).call((RT?d3.axisRight(y):d3.axisLeft(y)).ticks(6).tickFormat(bubMTick))
     .attr("font-size","12px").attr("color","#5E6B80");
  svg.append("g").attr("transform",`translate(${RT?m.l:W-m.r},0)`).call((RT?d3.axisLeft(yp):d3.axisRight(yp)).ticks(5).tickFormat(v=>v+"%"))''', 'arabic', 'concentration: axes swap sides in Arabic')
rep('bub', '''      .attr("transform", `translate(${x(d.name)+x.bandwidth()/2+4},${H-m.b+8}) rotate(34)`)
      .attr("font-size","11px").attr("fill","#46546F").attr("text-anchor","start")
      .text(short.length > 20 ? short.slice(0,19)+"…" : short);''',
    '''      .attr("transform", RT ? `translate(${x(d.name)+x.bandwidth()/2-4},${H-m.b+8}) rotate(-34)` : `translate(${x(d.name)+x.bandwidth()/2+4},${H-m.b+8}) rotate(34)`)
      .attr("font-size","11px").attr("fill","#46546F").attr("text-anchor",RT?"end":"start")
      .text(bidiName(short.length > 20 ? short.slice(0,19)+"…" : short));''', 'arabic', 'concentration: client names slant the other way in Arabic')
rep('bub', '''  svg.append("text").attr("x", x(pts[pts.length-1].name)-10).attr("y", yp(pts[pts.length-1].cum)-10)
     .attr("font-size","12px").attr("fill","#15224D").attr("font-weight","600")
     .text(Math.round(pts[pts.length-1].cum) + "% cumulative");''',
    '''  svg.append("text").attr("x", RT ? x(pts[pts.length-1].name)+x.bandwidth()/2-4 : x(pts[pts.length-1].name)-10).attr("y", yp(pts[pts.length-1].cum)-10)
     .attr("font-size","12px").attr("fill","#15224D").attr("font-weight","600")
     .text(bidiAr(bF("cum", Math.round(pts[pts.length-1].cum))));''', 'arabic', 'concentration: cumulative label')
# retention: horizontal bars start from the right in Arabic
rep('bub', '''  const W=960, H=300, m={t:24,r:220,b:14,l:180};
  const y = d3.scaleBand().domain(rows.map(r=>r.l)).range([m.t, H-m.b]).padding(0.34);
  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>r.v)*1.05]).range([m.l, W-m.r]);''',
    '''  const RT=BUB_LANG==="ar", W=960, H=300, m={t:24,r:220,b:14,l:180}, x0=RT?W-m.l:m.l;
  const y = d3.scaleBand().domain(rows.map(r=>r.l)).range([m.t, H-m.b]).padding(0.34);
  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>r.v)*1.05]).range(RT?[W-m.l, m.r]:[m.l, W-m.r]);
  const bx = r => RT ? Math.min(x(r.v), x0-4) : m.l;''', 'arabic', 'retention: bars start from the right in Arabic')
rep('bub', '''      .attr("x", m.l).attr("y", y(r.l)).attr("height", y.bandwidth())
      .attr("width", Math.max(4, x(r.v)-m.l)).attr("rx",6).attr("fill", r.c)
      .on("click", () => showListPanel(r.l, `${r.n} clients · ${r.note}`, r.c,
          `<b>${fmt(r.v)}</b> across <b>${r.n}</b> clients`,''',
    '''      .attr("x", bx(r)).attr("y", y(r.l)).attr("height", y.bandwidth())
      .attr("width", Math.max(4, Math.abs(x(r.v)-x0))).attr("rx",6).attr("fill", r.c)
      .on("click", () => showListPanel(bMap("step",r.l), BUB_LANG==="ar" ? `${bCount(r.n,"client")} · ${bMap("step",r.note)}` : `${r.n} clients · ${r.note}`, r.c,
          BUB_LANG==="ar" ? `<b>${fmt(r.v)}</b> · ${bT("clients_lbl")} <b>${r.n}</b>` : `<b>${fmt(r.v)}</b> across <b>${r.n}</b> clients`,''', 'arabic', 'retention bars and click-through panel')
rep('bub', '''    svg.append("text").attr("x", m.l-10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("text-anchor","end").attr("font-size","14px").attr("fill","#15224D").attr("font-weight","600").text(r.l);
    svg.append("text").attr("x", Math.max(4, x(r.v))+10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("font-size","12.5px").attr("fill","#5E6B80")
       .text(`${r.n} clients · ${fmt(r.v)}`);''',
    '''    svg.append("text").attr("x", RT ? x0+10 : m.l-10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("text-anchor",RT?"start":"end").attr("font-size","14px").attr("fill","#15224D").attr("font-weight","600").text(bidiAr(bMap("step",r.l)));
    svg.append("text").attr("x", RT ? bx(r)-10 : Math.max(4, x(r.v))+10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("text-anchor",RT?"end":null).attr("font-size","12.5px").attr("fill","#5E6B80")
       .text(BUB_LANG==="ar" ? bidiAr(`${bCount(r.n,"client")} · ${fmt(r.v)}`) : `${r.n} clients · ${fmt(r.v)}`);''', 'arabic', 'retention labels')
# sector mix shift: mirrors in Arabic — sector names on the right, values on the left
rep('bub', '''  const W=960, H=Math.max(360, 64 + rows.length*32), m={t:46,b:30,l:230,r:150};''',
    '''  const RT=BUB_LANG==="ar", W=960, H=Math.max(360, 64 + rows.length*32), m={t:46,b:30,l:230,r:RT?185:150};''', 'arabic', 'sector shift: wider value margin in Arabic')
rep('bub', '''  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>Math.max(r.p25,r.p26))*1.1]).range([m.l, W-m.r]);''',
    '''  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>Math.max(r.p25,r.p26))*1.1]).range(RT?[W-m.l, m.r]:[m.l, W-m.r]);''', 'arabic', 'sector shift: mirrored share axis in Arabic')
rep('bub', '''  svg.append("circle").attr("cx",m.l+4).attr("cy",14).attr("r",5).attr("fill","#fff").attr("stroke","#7D8AA0").attr("stroke-width",2);
  svg.append("text").attr("x",m.l+14).attr("y",18).attr("font-size","11.5px").attr("fill","#5E6B80").text("2025 share");
  svg.append("circle").attr("cx",m.l+110).attr("cy",14).attr("r",5.5).attr("fill","#0072BB");
  svg.append("text").attr("x",m.l+120).attr("y",18).attr("font-size","11.5px").attr("fill","#5E6B80").text("2026 share");''',
    '''  const lx = d => RT ? W-16-d : m.l+d;
  svg.append("circle").attr("cx",lx(4)).attr("cy",14).attr("r",5).attr("fill","#fff").attr("stroke","#7D8AA0").attr("stroke-width",2);
  svg.append("text").attr("x",lx(14)).attr("y",18).attr("text-anchor",RT?"end":null).attr("font-size","11.5px").attr("fill","#5E6B80").text(bidiAr(bT("share25")));
  svg.append("circle").attr("cx",lx(110)).attr("cy",14).attr("r",5.5).attr("fill","#0072BB");
  svg.append("text").attr("x",lx(120)).attr("y",18).attr("text-anchor",RT?"end":null).attr("font-size","11.5px").attr("fill","#5E6B80").text(bidiAr(bT("share26")));''', 'arabic', 'sector shift legend')
rep('bub', '''    const sn = r.s.length > 28 ? r.s.slice(0,27)+"…" : r.s;
    svg.append("text").attr("x", m.l-12).attr("y", cy+4.5).attr("text-anchor","end")
       .attr("font-size","12.5px").attr("fill","#15224D").attr("font-weight","600").text(sn);''',
    '''    const sl = bTS(r.s), sn = sl.length > 28 ? sl.slice(0,27)+"…" : sl;
    svg.append("text").attr("x", RT ? W-m.l+12 : m.l-12).attr("y", cy+4.5).attr("text-anchor",RT?"start":"end")
       .attr("font-size","12.5px").attr("fill","#15224D").attr("font-weight","600").text(bidiAr(sn));''', 'arabic', 'sector shift: sector names')
rep('bub', '''    svg.append("text").attr("x", W-m.r+12).attr("y", cy+4.5)
       .attr("font-size","12px").attr("fill","#46546F")
       .text(`${r.p25.toFixed(1)} → ${r.p26.toFixed(1)}%`);
    svg.append("text").attr("x", W-14).attr("y", cy+4.5).attr("text-anchor","end")
       .attr("font-size","12px").attr("font-weight","700")
       .attr("fill", up ? "#2E7A37" : "#B23F2B")
       .text((up?"+":"−") + Math.abs(d).toFixed(1) + "pp");''',
    '''    svg.append("text").attr("x", RT ? m.r-12 : W-m.r+12).attr("y", cy+4.5).attr("text-anchor",RT?"end":null)
       .attr("font-size","12px").attr("fill","#46546F")
       .text(`${r.p25.toFixed(1)} → ${r.p26.toFixed(1)}%`);
    svg.append("text").attr("x", RT ? 14 : W-14).attr("y", cy+4.5).attr("text-anchor",RT?"start":"end")
       .attr("font-size","12px").attr("font-weight","700")
       .attr("fill", up ? "#2E7A37" : "#B23F2B")
       .text(BUB_LANG==="ar" ? bidiAr(BUB_LRI+(up?"+":"−")+Math.abs(d).toFixed(1)+BUB_PDI+bT("pp")) : (up?"+":"−") + Math.abs(d).toFixed(1) + "pp");''', 'arabic', 'sector shift: values and change')
# heatmap
rep('bub', 'secs.map(s => `<th class="col">${s}</th>`).join("")', 'secs.map(s => `<th class="col">${bTS(s)}</th>`).join("")', 'arabic', 'heatmap sector headings')
rep('bub', 'h += `<tr><th class="row" title="${cat}">${cat}</th>`;', 'h += `<tr><th class="row" title="${bTV(cat)}">${bTV(cat)}</th>`;', 'arabic', 'heatmap service headings')
rep('bub', 'h += `<td class="hc empty" title="Whitespace: no ${cat} sales into ${sec}">–</td>`;',
    'h += `<td class="hc empty" title="${bF("ws_title", bTV(cat), bTS(sec))}">–</td>`;', 'arabic', 'heatmap empty-cell hover')
rep('bub', '''                 title="${sec} × ${cat}">${v>0?fmt(v).replace("SAR ",""):"0"}<small>${n} ln · ${c.co.length} co</small></td>`;''',
    '''                 title="${bTS(sec)} × ${bTV(cat)}">${v>0?bubAmt(v,false,false):"0"}<small>${bF("cell_n", n, c.co.length)}</small></td>`;''', 'arabic', 'heatmap cells')
rep('bub', '''  document.getElementById("pco").textContent = cat;
  document.getElementById("psec").textContent = sec;''', '''  document.getElementById("pco").textContent = bTV(cat);
  document.getElementById("psec").textContent = bTS(sec);''', 'arabic', 'heatmap cell panel title')
rep('bub', '''    `<b>${fmt(hv(c))}</b> across <b>${hn(c)}</b> lines · <b>${cos.length}</b> client${cos.length>1?"s":""}`;''',
    '''    (BUB_LANG==="ar" ? `<b>${fmt(hv(c))}</b> · ${bT("lines_lbl")} <b>${hn(c)}</b> · ${bT("clients_lbl")} <b>${cos.length}</b>` :
    `<b>${fmt(hv(c))}</b> across <b>${hn(c)}</b> lines · <b>${cos.length}</b> client${cos.length>1?"s":""}`);''', 'arabic', 'heatmap cell panel total')
# chart captions follow the language
rep('bub', "cap.textContent=EH_BUB_CAPS[id];", "cap.textContent=bubCap(id);", 'arabic', 'chart captions')

# ---------------- hub shell: the comment is no longer true ----------------
rep('hub', 'bcastLang();\n// note: the bubble chart is a static English artifact and keeps its labels.\n', 'bcastLang();\n',
    'cleanup', 'remove the out-of-date comment: the bubble page now follows the hub language')

# ---------------- CHANGES.md ----------------
LINE = ('clients | major | Clients & Revenue | New: the client portfolio page is now fully in Arabic when the hub is in Arabic — the bubble map, '
        'the sector × service heatmap, every Executive chart, the KPI tiles, hover boxes, the client detail panel and the notes. '
        'Company names stay as recorded, amounts read in riyals with Western digits, and the page reads right to left: the legend and '
        'detail panel sit on the left, and the ranked charts (client concentration, retention, sector mix) start from the right, while '
        'the 2025 → 2026 revenue bridge and the money axes stay left to right. | '
        'جديد: صفحة محفظة العملاء أصبحت بالعربية كاملة عند اختيار العربية في المنصة — خريطة الفقاعات، والخريطة الحرارية للقطاعات والخدمات، '
        'وكل رسوم الملخص التنفيذي، وبطاقات المؤشرات، ونوافذ التمرير، ولوحة تفاصيل العميل، والملاحظات. تبقى أسماء الشركات كما سُجّلت، '
        'وتظهر المبالغ بالريال وبالأرقام الغربية، وتُقرأ الصفحة من اليمين إلى اليسار: المفتاح ولوحة التفاصيل على اليسار، والرسوم المرتّبة '
        '(تركّز العملاء، والاحتفاظ بهم، ومزيج القطاعات) تبدأ من اليمين، بينما يبقى جسر الإيرادات من 2025 إلى 2026 ومحاور المبالغ من اليسار إلى اليمين.')
rep('changes', '\n\n## 2026-W41\n', '\n' + LINE + '\n\n## 2026-W41\n', 'changelog', 'one W42 line for the Arabic client portfolio page')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['bub'])
open(HUB, 'w', encoding='utf-8').write(FILES['hub'])
open(CH, 'w', encoding='utf-8').write(FILES['changes'])
write_change_table(os.path.join(HERE, 'change_table_bubble_arabic'), 'Arabic version — Client Bubble Map')
print('patched: hub/EH_Client_Bubble_Map_CURRENT.html, hub/EH_Hub.html, pipeline/CHANGES.md')
