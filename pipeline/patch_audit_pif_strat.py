"""patch_audit_pif_strat.py — audit fixes for the PIF Strategy 2026–2030 page (hub/pif_strategy_2026_2030.html), 12 Oct 2026.

An independent audit checked this page against the strategy document and PIF's 2023–2025 annual reports. What was
wrong, and what changed:

  • "Climate solutions" row cited the 2024 report p.95; the figure is on p.88 (audit pif-05).
  • Jobs (pif-07): the 730,249 "what happened" figure counts direct and indirect jobs since 2018, while the 1.8 million
    promise counts direct, indirect and induced jobs for 2021–25. The row now says so, and the source is p.9 (was
    p.10–11).
  • "How fast it grew" chart (pif-08): the 2026–30 row was an empty bar. It now says "Not published" inside the chart,
    in English or Arabic, as the page's own rule requires.
  • SIRC / waste (pif-09): wherever the page talks about group 05's waste wording or SIRC's role, it now says PIF does
    not say which kinds of waste (openings #1, relevance row 2, risks #1, the sectors paragraph, the SIRC row).
    Relevance row 2 no longer says "this is the company PIF will use for waste" — the plan only names SIRC.
  • Inside the hub, the "Where the numbers come from" button was hidden although the page tells readers to use it
    (pif-10). It now shows; the language and theme buttons stay hidden (the hub has its own).
  • "Then and now" chart (pif-11): the share-abroad target is a ceiling, but its bar looked like a miss. It is now
    drawn as promise ÷ what happened (24 ÷ 20 = 120), labelled "ceiling: lower is better".
  • Arabic (pif-12, pif-21 "Hub2021"): big-project "Before/Now" columns, project names, unit labels, the source lists
    under both charts, every source chip, popover and the sources list are now in Arabic (EH translations, as the page
    already says for its other Arabic). Any English name left is isolated so Arabic does not reorder it.
  • Text glitches (pif-21): merged labels ("…Hub2021", "…Hub.i", "[2018..2020]"), the undefined "S26 p25" chips (now
    "Strategy document p.25"), internal field names ("wasteQuotes") in sources, "three five-year plans" (the first was
    PIF Program 2018–2020, so the column is now "2018–20 plan"), the dangling "§2.9", "?✓" next to a missing number,
    and "all 36 pages" (now "36 PDF pages, 69 printed pages").
  • Sector-shift diagram in Arabic (pif-22): titles and group labels now read right to left, with numbers in place.
  • Keyboard (pif-23): every source chip can be reached with Tab and opened with Enter or Space; the sources box keeps
    the focus inside while open and returns it when closed; Escape closes popovers too.
  • Desktop nav (pif-24): at 1024 px and wider the section links wrap instead of running off the right edge.
  • Qiddiya "48 million tourists" source: 2023 report p.76 (was p.78) (pif-14).

Not changed here: the 2020 share-abroad baseline (30% here vs ~23% from the companion page's pools) is an owner decision
(pif-15).

Exact-string edits; stops if an anchor is missing. Run once:  python3 pipeline/patch_audit_pif_strat.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'pif_strategy_2026_2030.html')
if 'id="auditPif"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'str')
A = 'str'

# ---------------------------------------------------------------- data: sources and wording
rep(A, "src:'figures in the PIF Intelligence Hub[2018..2020] (2021 report p.28)'", "src:'figures in the PIF Intelligence Hub, 2018–2020 (2021 report p.28)'", 'copy', 'pif-21: merged label "Hub[2018..2020]"')
rep(A, "src:'2024 report p.28–29; 2025 report p.28; figures in the PIF Intelligence Hub.i'}", "src:'2024 report p.28–29; 2025 report p.28; figures in the PIF Intelligence Hub'}", 'copy', 'pif-21: merged label "Hub.i"')
rep(A, "p2:{stated:1800000, deliv:730249, delivY:2023, note:['last reported 2023; no 2024/2025 figure','آخر رقم منشور 2023؛ لا رقم لعامَي 2024/2025'], src:'2024 report p.28–29; 2023 report p.10–11; HUB findings f3'}",
    "p2:{stated:1800000, deliv:730249, delivY:2023, note:['last reported 2023; no 2024/2025 figure. Different basis: this counts direct and indirect jobs since 2018; the promise counts direct, indirect and induced jobs for 2021–25','آخر رقم منشور 2023؛ لا رقم لعامَي 2024/2025. أساس مختلف: يعدّ هذا الرقم الوظائف المباشرة وغير المباشرة منذ 2018، بينما يعدّ الوعد الوظائف المباشرة وغير المباشرة والمستحثّة للفترة 2021–2025'], src:'2024 report p.28–29; 2023 report p.9; HUB findings f3'}",
    'copy', 'pif-07: jobs — different basis stated; source p.10–11 → p.9')
rep(A, "src:'figures in the PIF Intelligence Hub2021'}", "src:'figures in the PIF Intelligence Hub, 2021 (2021 report p.5)'}", 'copy', 'pif-21: merged label "Hub2021" (water row)')
rep(A, "src:'PIF Intelligence Hub findings f3 (2024 report p.95)'}", "src:'PIF Intelligence Hub findings f3 (2024 report p.88)'}", 'copy', 'pif-05: climate-solutions share is on 2024 report p.88')
rep(A, "src:'HUB wasteQuotes 2022–2025'}", "src:'HUB section 8 quotes, 2022–2025'}", 'copy', 'pif-21: internal field name in a source label (1)')
rep(A, "src:'HUB wasteQuotes[2021]'}", "src:'HUB section 8 quotes, 2021'}", 'copy', 'pif-21: internal field name in a source label (2)')
rep(A, "src:'HUB wasteQuotes 2022, 2024, 2025'}", "src:'HUB section 8 quotes, 2022, 2024, 2025'}", 'copy', 'pif-21: internal field name in a source label (3)')
rep(A, "p3:{text:['named as one of the three companies in group 05','مسمّاة كإحدى الشركات الثلاث في المجموعة 05']",
    "p3:{text:['named as one of the three companies in group 05; PIF does not say which kinds of waste it will handle','مسمّاة كإحدى الشركات الثلاث في المجموعة 05؛ ولا يحدد الصندوق أي أنواع النفايات ستتولاها']",
    'copy', 'pif-09: SIRC row flags the undefined waste scope')
rep(A, "src:'figures in the PIF Intelligence Hub2021 (2021 report p.5). Mapping to ecosystems is EH analysis (L).'",
    "src:'figures in the PIF Intelligence Hub, 2021 (2021 report p.5). Mapping to ecosystems is EH analysis (L).'", 'copy', 'pif-21: merged label "Hub2021" (sectors)')
rep(A, "j:['This is the company PIF will use for waste. For EH it is both a possible customer and a serious competitor.','هذه الشركة التي سيستخدمها الصندوق للنفايات. بالنسبة لآفاق البيئة هي عميل محتمل ومنافس جدي في الوقت نفسه.']",
    "j:['SIRC is the only recycling company named in group 05; its waste role is not defined (PIF does not say which kinds of waste). For EH it could be a customer, a competitor or both.','سرك هي شركة إعادة التدوير الوحيدة المسمّاة في المجموعة 05؛ ودورها في النفايات غير محدد (لا يحدد الصندوق أي أنواع النفايات). وقد تكون لآفاق البيئة عميلاً أو منافساً أو كليهما.']",
    'copy', 'pif-09: relevance row 2 no longer says PIF will use SIRC for waste')
rep(A, "bsrc:'2023 report p.78'", "bsrc:'2023 report p.76'", 'copy', 'pif-14: Qiddiya 48 million tourists is on 2023 report p.76')
rep(A, "['PIF has written waste management into its plan for the first time (group 05)','كتب الصندوق إدارة النفايات في خطته لأول مرة (المجموعة 05)',",
    "['PIF has written waste management into its plan for the first time (group 05), but does not say which kinds of waste','كتب الصندوق إدارة النفايات في خطته لأول مرة (المجموعة 05)، لكنه لا يحدد أي أنواع النفايات',",
    'copy', 'pif-09: opening #1 flags the undefined waste scope')
rep(A, "['Saudi Investment Recycling Company (SIRC), PIF\\u2019s own recycling company, is the one PIF names for waste — a competitor with PIF behind it','الشركة السعودية الاستثمارية لإعادة التدوير، شركة الصندوق لإعادة التدوير، هي التي يسمّيها الصندوق للنفايات — منافس يقف الصندوق خلفه',",
    "['Saudi Investment Recycling Company (SIRC), PIF\\u2019s own recycling company, is the only recycling company PIF names in group 05 — a possible competitor with PIF behind it (PIF does not say which kinds of waste)','الشركة السعودية الاستثمارية لإعادة التدوير، شركة الصندوق لإعادة التدوير، هي شركة إعادة التدوير الوحيدة التي يسمّيها الصندوق في المجموعة 05 — منافس محتمل يقف الصندوق خلفه (لا يحدد الصندوق أي أنواع النفايات)',",
    'copy', 'pif-09: risk #1 flags the undefined waste scope')
rep(A, "'performance measures for the §2.9 measurement framework'", "'numbers for the measurement framework PIF describes (p.42)'", 'copy', 'pif-21: dangling "§2.9" (EN)')
rep(A, "'مؤشرات إطار القياس (القسم 2.9)'", "'أرقام لإطار القياس الذي يصفه الصندوق (ص42)'", 'copy', 'pif-21: dangling "§2.9" (AR)')

# ---------------------------------------------------------------- I18N wording
rep(A, 'We read all 36 pages.', 'We read the whole document (36 PDF pages, 69 printed pages).', 'copy', 'pif-21: "36 pages" made unambiguous (EN)')
rep(A, 'قرأنا الصفحات الست والثلاثين كلها.', 'قرأنا الوثيقة كلها (36 صفحة PDF، أي 69 صفحة مطبوعة).', 'copy', 'pif-21: "36 pages" made unambiguous (AR)')
rep(A, 'PIF has had three five-year plans.', 'PIF has had three plans: 2018–20, 2021–25 and now 2026–30.', 'copy', 'pif-21: "three five-year plans" (EN)')
rep(A, 'كان للصندوق ثلاث خطط خمسية.', 'كان للصندوق ثلاث خطط: 2018–2020، و2021–2025، والآن 2026–2030.', 'copy', 'pif-21: "three five-year plans" (AR)')
rep(A, '2017–20 plan', '2018–20 plan', 'copy', 'pif-21: the first plan is PIF Program 2018–2020 (EN)', count=2)
rep(A, 'خطة 2017–2020', 'خطة 2018–2020', 'copy', 'pif-21: the first plan is PIF Program 2018–2020 (AR)', count=2)
rep(A, 'There is no bar for 2026–30 because PIF set no fund-wide target — the empty last row is deliberate.',
    'There is no bar for 2026–30 because PIF set no fund-wide target, so that row says \\"Not published\\".', 'copy', 'pif-08: trajectory paragraph (EN)')
rep(A, 'لا عمود ل2026–2030 لأن الصندوق لم يحدد مستهدفاً على مستوى الصندوق — الصف الأخير الفارغ مقصود.',
    'لا عمود ل2026–2030 لأن الصندوق لم يحدد مستهدفاً على مستوى الصندوق، لذا يقول ذلك الصف «غير منشور».', 'copy', 'pif-08: trajectory paragraph (AR)')
rep(A, 'Waste appears for the first time, in group 05\'s focus text.', 'Waste appears for the first time, in group 05\'s focus text (PIF does not say which kinds of waste).', 'copy', 'pif-09: sectors paragraph (EN)')
rep(A, 'وتظهر النفايات لأول مرة في نص تركيز المجموعة 05.', 'وتظهر النفايات لأول مرة في نص تركيز المجموعة 05 (لا يحدد الصندوق أي أنواع النفايات).', 'copy', 'pif-09: sectors paragraph (AR)')
rep(A, 'وحيث يختلفان نعلّم ذلك ونعرض الرقمَين؛ لا نختار أحدهما بصمت أبداً.',
    'وحيث يختلفان نعلّم ذلك ونعرض الرقمَين؛ لا نختار أحدهما بصمت أبداً. النصوص العربية في هذا الجدول ترجمة آفاق البيئة؛ الأصل بالإنجليزية.', 'copy', 'pif-12: big-projects table labelled as EH translation (AR)')
rep(A, 'عندما تختلف خطة 2026–2030 عن تقرير سنوي نستخدم رقم الخطة ونعرض الآخر أيضاً.',
    'عندما تختلف خطة 2026–2030 عن تقرير سنوي نستخدم رقم الخطة ونعرض الآخر أيضاً. أوصاف المصادر بالعربية ترجمة آفاق البيئة.', 'copy', 'pif-12: sources box labelled as EH translation (AR)')

rep(A, '<b>HUB</b> تعني الصفحة المرافقة عن التقارير السنوية', '<b>الصفحة المرافقة</b> تعني صفحة التقارير السنوية للصندوق', 'copy', 'pif-12: Arabic how-to names the companion page as the chips now do (AR)')

# ---------------------------------------------------------------- pif-12: Arabic helpers (after the I18N block)
AR_HELP = r'''let LANG='en',THEME='light';const charts={};
// ---- Arabic for source notes, units and the big-projects table (patch_audit_pif_strat.py, 12 Oct 2026). These are EH translations:
//      PIF published the plan in English only. srcL() turns a source note into Arabic; any English name left is isolated LTR.
const SRC_AR=[
 [/all 36 PDF pages searched: no PIF-level numeric target for 2030/g,'بحثنا في صفحات PDF الست والثلاثين كلها: لا مستهدف رقمي على مستوى الصندوق لعام 2030'],
 [/— no PIF-level numeric 2030 target; pace cannot be computed/g,'— لا مستهدف رقمي على مستوى الصندوق لعام 2030؛ لا يمكن حساب الوتيرة'],
 [/— actual only, no 2030 target/g,'— الرقم الحالي فقط، لا مستهدف لعام 2030'],[/— whole document searched/g,'— بحثنا في الوثيقة كلها'],
 [/absent from Strategy document ecosystem lists/g,'غائبة عن قوائم المنظومات في وثيقة الاستراتيجية'],[/present in (\d{4}) report/g,'موجودة في تقرير $1'],
 [/Mapping to ecosystems is EH analysis \(L\)/g,'ربط القطاعات بالمنظومات تحليل آفاق البيئة (L)'],[/workbook Stakeholders row (\d+)/g,'مصنف أصحاب المصلحة، الصف $1'],
 [/EH_company_profile\.pdf/g,'الملف التعريفي لآفاق البيئة'],[/not in project data/g,'ليس في بيانات المشروع'],[/— not mentioned/g,'— غير مذكور'],[/— absent/g,'— غائب'],[/all pages/g,'كل الصفحات'],
 [/(?:PIF Intelligence Hub|HUB) findings f(\d)/g,'الصفحة المرافقة، الخلاصة f$1'],[/HUB section 8 quotes/g,'الصفحة المرافقة، اقتباسات القسم 8'],
 [/figures in the PIF Intelligence Hub/g,'أرقام الصفحة المرافقة'],[/\bHUB\b/g,'الصفحة المرافقة'],
 [/">\$([\d,.]+) billion"/g,'«أكثر من $1 مليار دولار»'],[/\$([\d,.]+) billion→>\$([\d,.]+) billion/g,'من $1 مليار دولار إلى أكثر من $2 مليار دولار'],
 [/SAR ([\d,.]+)\+ billion/g,'أكثر من $1 مليار ريال'],[/SAR ([\d,.]+) billion/g,'$1 مليار ريال'],[/ new projects /g,' مشاريع جديدة '],
 [/"up to 11%"/g,'«حتى 11%»'],[/"11%\.\.\. by the end of that period"/g,'«11%... بنهاية تلك الفترة»'],[/"more than 220 companies"/g,'«أكثر من 220 شركة»'],[/"six-fold"/g,'«ستة أضعاف»'],
 [/(\d+%) in (\d{4})/g,'$1 في $2'],[/\btarget (?=\d{4} report)/g,'المستهدف: '],[/\bactual (?=\d{4} report)/g,'الفعلي: '],[/ baseline/g,' (خط الأساس)'],
 [/over 2 yrs/g,'خلال سنتين'],[/over (\d+) yrs/g,'خلال $1 سنوات'],
 [/AR(\d\d) p\.?(\d+)/g,'تقرير 20$1 ص$2'],[/(\d{4}) report/g,'تقرير $1'],[/Strategy document/g,'وثيقة الاستراتيجية'],
 [/\bp\.(\d+(?:[–-]\d+)?)/g,'ص$1'],[/, ص/g,'، ص'],[/; /g,'؛ ']];
const srcL=s=>{if(LANG!=='ar'||s==null)return s;let o=String(s);SRC_AR.forEach(([r,v])=>{o=o.replace(r,v)});
  return o.replace(/[>~$]?[\d][\d.,]*(?:\s*→\s*[>~$]?[\d][\d.,]*)+/g,m=>'⁦'+m+'⁩').replace(/[A-Za-z][A-Za-z0-9 .,&'’()_-]*[A-Za-z0-9)]/g,m=>'⁦'+m+'⁩')};
const UNIT_AR={'SAR billion':'مليار ريال','SAR billion/yr':'مليار ريال سنوياً','%':'%','jobs':'وظيفة','million':'مليون','destinations':'وجهة'};
const unitL=u=>LANG==='ar'?(UNIT_AR[u]||u):u;
const GP_AR={'NEOM':'نيوم','Red Sea Global':'البحر الأحمر الدولية','Diriyah':'الدرعية','Qiddiya':'القدية','ROSHN':'روشن','KAFD':'مركز الملك عبدالله المالي','Riyadh Air':'طيران الرياض','KAEC / Lucid':'مدينة الملك عبدالله الاقتصادية / لوسيد'};
const GIGA_AR={
 'NEOM|Scope':['أوكساجون، ذا لاين، تروجينا، ماجنا، الجزر','«موانئ نيوم، ومركز أوكساجون للتصنيع، ومشروع الهيدروجين الأخضر، ومرافق الطاقة النظيفة والذكاء الاصطناعي»'],
 'NEOM|Green hydrogen':['مكتمل بنسبة 90%؛ يبدأ التشغيل في 2026','مسمّى ضمن مجالات التركيز؛ بلا نسبة أو تاريخ'],
 'NEOM|Port terminal 2026':['«في المسار الصحيح لبدء التشغيل في 2026»','لم يُعاد ذكره'],
 'Red Sea Global|Open resorts':['4 (تقرير 2024)؛ ديزرت روك «العقار الخامس» و3 فنادق في جزيرة شُرى (تقرير 2025)','«أربعة عشر منتجعاً مفتوحاً»'],
 'Red Sea Global|AMAALA first guests 2026':['تستعد لاستقبال أول ضيوفها في 2026','لم يُعاد ذكره'],
 'Red Sea Global|2030 GDP / jobs':['—','أكثر من 8 مليارات دولار ناتجاً محلياً؛ أكثر من 170,000 وظيفة مباشرة وغير مباشرة'],
 'Red Sea Global|Local content':['—','\u206656%\u2069؛ نحو 700 مليون دولار لشركات سعودية في 2024'],
 'Diriyah|Visitors 2030':['«أكثر من 47 مليون زائر سنوياً بحلول 2030»','«أكثر من 25 مليون زيارة سنوياً»'],
 'Diriyah|Jobs / residents 2030':['—','أكثر من 125,000 وظيفة مباشرة؛ أكثر من 34,000 ساكن'],
 'Diriyah|Opera House SAR 5.26 billion; Wadi Safar SAR 6 billion; KSU contract "SAR 4,225 billion"':['كما طُبع','لم يُعاد ذكره'],
 'Qiddiya|Six Flags opened 31 Dec 2025; PMBS Stadium SAR 15 billion':['كما طُبع','مسمّاة ضمن المجموعة 01 فقط'],
 'Qiddiya|48 million tourists; 325,000 jobs; 600,000+ residents':['كما طُبع','لم يُعاد ذكره'],
 'ROSHN|Scale metrics':['محفظة تزيد على 200 مليون م²؛ هدف وطني لتملك المساكن 70%','أكثر من 3,000 منزل سُلّمت؛ 11 موقعاً في 3 مناطق؛ 9 إطلاقات بأكثر من 17,000 منزل؛ 13 شراكة؛ 1.4 مليون م²'],
 'KAFD|GDP projection; RHQs':['من 9.39 مليار ريال إلى 32.68 مليار ريال بحلول 2030؛ 20 مقراً إقليمياً','أُعيد ذكر المقرات الإقليمية العشرين؛ وتوقع الناتج لم يُعاد ذكره'],
 'Riyadh Air|2030 targets':['100 وجهة؛ 20 مليار دولار ناتجاً محلياً؛ 200,000 وظيفة','نحو 100 وجهة؛ نحو 20 مليار دولار ناتجاً محلياً؛ الوظائف لم يُعاد ذكرها'],
 'KAEC / Lucid|Automotive cluster':['اعتُمد مجمع الملك سلمان للسيارات؛ هيونداي 50,000 مركبة سنوياً؛ سير، لوسيد','برنامج لوسيد مع أوبر لتشغيل 20,000 سيارة أجرة ذاتية القيادة؛ ومدينة الملك عبدالله الاقتصادية مسمّاة شركةً في المجموعة 03']};
const gigaL=(g,i)=>{if(LANG!=='ar')return i?g.s26:g.base;const a=GIGA_AR[g.p+'|'+g.item[0]];return a?a[i]:srcL(i?g.s26:g.base)};'''
rep(A, "let LANG='en',THEME='light';const charts={};", AR_HELP, 'code', 'pif-12: Arabic source notes, units, project names and big-project texts')

# cite(): Arabic labels/sources, keyboard access, and no ✓ next to "?"
rep(A, "function cite(label,src,g){REG.push({label:String(label).replace(/<[^>]+>/g,''),src,g:g||'H'});return `<span class=\"cite\" data-src=\"${esc(src)}\" data-g=\"${g||'H'}\">${label}<sup>${g==='M'?'≈':g==='L'?'•':'✓'}</sup></span>`}",
    "function cite(label,src,g){const s2=srcL(src);label=String(label);if(label===src||label===esc(src))label=esc(s2);else if(!/[<&]/.test(label))label=srcL(label);"
    "REG.push({label:label.replace(/<[^>]+>/g,''),src:s2,g:g||'H'});return `<span class=\"cite\" tabindex=\"0\" role=\"button\" data-src=\"${esc(s2)}\" data-g=\"${g||'H'}\">${label}<sup>${g==='N'?'':g==='M'?'≈':g==='L'?'•':'✓'}</sup></span>`}",
    'code', 'pif-12/21/23: source chips in Arabic, reachable by keyboard; "?" without a ✓')
rep(A, "${cite('?',p.src,'H')}", "${cite('?',p.src,'N')}", 'code', 'pif-21: no ✓ next to a missing number')
rep(A, "cite('S26 p4, p23','Strategy document p.4, p.23; 2025 report p.30')", "cite('Strategy document p.4, p.23','Strategy document p.4, p.23; 2025 report p.30')", 'copy', 'pif-21: "S26" chip → "Strategy document" (1)')
rep(A, "cite('S26 p5, p22–23','S26 p5, p22–23')", "cite('Strategy document p.5, p.22–23','Strategy document p.5, p.22–23')", 'copy', 'pif-21: "S26" chip → "Strategy document" (2)')
rep(A, "cite('S26 '+e.page,'S26 '+e.page)", "cite('Strategy document p.'+e.page.slice(1),'Strategy document p.'+e.page.slice(1))", 'copy', 'pif-21: "S26" chip → "Strategy document" (3)')
rep(A, "cite('S26','Strategy document — whole document searched')", "cite('Strategy document','Strategy document — whole document searched')", 'copy', 'pif-21: "S26" chip → "Strategy document" (4)')
rep(A, "cite('figures in the PIF Intelligence Hub2021 (2021 report p.5) · Strategy document p.5','figures in the PIF Intelligence Hub2021 (2021 report p.5); Strategy document p.5')",
    "cite('figures in the PIF Intelligence Hub, 2021 (2021 report p.5) · Strategy document p.5','figures in the PIF Intelligence Hub, 2021 (2021 report p.5); Strategy document p.5')", 'copy', 'pif-21: merged label "Hub2021" (diagram source)')
rep(A, "s=`<span class=\"conf\">${t('k_conf')}: ${k.conflict.map(x=>iso(x)).join(' · ')}</span>`;", "s=`<span class=\"conf\">${t('k_conf')}: ${k.conflict.map(x=>LANG==='ar'?srcL(x):iso(x)).join(' · ')}</span>`;", 'code', 'pif-12: KPI conflict sources in Arabic')
rep(A, "s=iso(`$${k.usd} bn`);", "s=LANG==='ar'?(k.usd[0]==='>'?'أكثر من '+iso(k.usd.slice(1)):iso(k.usd))+' مليار دولار':iso(`$${k.usd} bn`);", 'code', 'pif-12: KPI dollar line in Arabic')
rep(A, "${x.unit?`<div class=\"tiny\">${esc(x.unit)}</div>`:''}", "${x.unit?`<div class=\"tiny\">${esc(unitL(x.unit))}</div>`:''}", 'code', 'pif-12: unit labels in Arabic')
rep(A, "S.giga.map(g=>`<tr><td><b>${g.p}</b></td><td>${P(g.item)}</td><td>${esc(g.base)} ${g.bsrc!=='—'?cite('',g.bsrc):''}</td><td>${esc(g.s26)} ${cite('',g.ssrc)}</td>",
    "S.giga.map(g=>`<tr><td><b>${LANG==='ar'?(GP_AR[g.p]||g.p):g.p}</b></td><td>${P(g.item)}</td><td>${esc(gigaL(g,0))} ${g.bsrc!=='—'?cite('',g.bsrc):''}</td><td>${esc(gigaL(g,1))} ${cite('',g.ssrc)}</td>",
    'code', 'pif-12: big-projects "Before/Now" columns and names in Arabic')
rep(A, "document.getElementById('buildline').innerHTML=`pif_strategy_2026_2030.html ${BUILD.version} · ${t('build')} ${iso(BUILD.date)} · ${esc(BUILD.source)}`;",
    "document.getElementById('buildline').innerHTML=`pif_strategy_2026_2030.html ${BUILD.version} · ${t('build')} ${iso(BUILD.date)} · ${esc(L(BUILD.source,'استراتيجية صندوق الاستثمارات العامة 2026–2030 — النسخة العامة (© الصندوق 2026، 69 صفحة)'))}`;",
    'code', 'pif-12: build line in Arabic')
rep(A, "S.sources.map(s=>`<tr><td><b>${s.id}</b></td>", "S.sources.map(s=>`<tr><td><b>${LANG==='ar'?({'WB':'المصنف','FX':'سعر الصرف'}[s.id]||esc(srcL(s.id))):s.id}</b></td>", 'code', 'pif-12: source names in the sources box in Arabic')
rep(A, "<td class=\"tiny\">${esc(r.src)}</td><td class=\"c\">${r.g}</td></tr>`).join('');", "<td class=\"tiny\">${esc(r.src)}</td><td class=\"c\">${r.g==='N'?'?':r.g}</td></tr>`).join('');", 'code', 'pif-21: sources list shows "?" for a missing number')

# ---------------------------------------------------------------- pif-11: ceiling target in the "then and now" chart
rep(A, "mk('cCmp',{type:'bar',data:{labels:numeric.map(x=>P([x.en,x.ar])),datasets:[\n    {label:t('deliv'),data:numeric.map(x=>+(x.p2.deliv/x.p2.stated*100).toFixed(1)),",
    "const ceil=x=>x.id==='intl';   // share abroad is a ceiling: plotted as promise ÷ what happened, so past the line = met (audit pif-11)\n"
    "  mk('cCmp',{type:'bar',data:{labels:numeric.map(x=>P([x.en,x.ar])+(ceil(x)?L(' (ceiling: lower is better)',' (حدٌّ أعلى: الأقل أفضل)'):'')),datasets:[\n    {label:t('deliv'),data:numeric.map(x=>+((ceil(x)?x.p2.stated/x.p2.deliv:x.p2.deliv/x.p2.stated)*100).toFixed(1)),",
    'code', 'pif-11: share-abroad ceiling plotted as promise ÷ what happened')
rep(A, "tooltip:{callbacks:{label:c=>t('deliv')+': '+c.raw+' ('+t('stated')+' = 100)',afterBody:c=>[numeric[c[0].dataIndex].p2.src]}}",
    "tooltip:{callbacks:{label:c=>ceil(numeric[c.dataIndex])?L('Ceiling: promise ÷ what happened × 100 = ','حدٌّ أعلى: الوعد ÷ ما حدث × 100 = ')+c.raw:t('deliv')+': '+c.raw+' ('+t('stated')+' = 100)',afterBody:c=>[srcL(numeric[c[0].dataIndex].p2.src)]}}",
    'code', 'pif-11: chart tooltip explains the ceiling; source in Arabic')
rep(A, "numeric.map(x=>`<b>${P([x.en,x.ar])}</b>: ${fmt(x.p2.deliv)} / ${fmt(x.p2.stated)} ${x.unit} — ${esc(x.p2.src)}`).join('<br>')+`<br>${L('Jobs and non-governmental investment are omitted: no closing actual exists. International share is a ceiling, so below target counts as met.','الوظائف والاستثمار غير الحكومي محذوفان: لا رقم فعلي ختامي. الحصة الدولية حدٌّ أعلى، لذا يُعدّ ما دون المستهدف تحقيقاً.')}`;",
    "numeric.map(x=>`<b>${P([x.en,x.ar])}</b>: ${fmt(x.p2.deliv)} / ${fmt(x.p2.stated)} ${esc(unitL(x.unit))} — ${esc(srcL(x.p2.src))}`).join('<br>')+`<br>${L('Jobs and non-governmental investment are omitted: no closing actual exists. ','الوظائف والاستثمار غير الحكومي محذوفان: لا رقم فعلي ختامي. ')}`"
    "+numeric.filter(ceil).map(x=>L(`Share abroad is a ceiling (lower is better), so its bar shows the promise divided by what happened: ${x.p2.stated} ÷ ${x.p2.deliv} × 100 = ${+(x.p2.stated/x.p2.deliv*100).toFixed(1)}; past the line means met.`,`حصة الخارج حدٌّ أعلى (الأقل أفضل)، لذا يعرض عمودها الوعد مقسوماً على ما حدث: ${iso(x.p2.stated+' ÷ '+x.p2.deliv+' × 100 = '+(+(x.p2.stated/x.p2.deliv*100).toFixed(1)))}؛ وتجاوز الخط يعني التحقق.`)).join('');",
    'code', 'pif-11/12: chart footnote explains the ceiling; units and sources in Arabic')

# ---------------------------------------------------------------- pif-08: "Not published" inside the trajectory chart
rep(A, "tooltip:{callbacks:{label:c=>(c.raw==null?t('k_none'):c.raw+'% p.a.'),afterBody:c=>[TJ[c[0].dataIndex].src]}}}}});",
    "tooltip:{callbacks:{label:c=>(c.raw==null?t('k_none'):c.raw+L('% p.a.','% سنوياً')),afterBody:c=>[srcL(TJ[c[0].dataIndex].src)]}}}},\n"
    "    plugins:[{id:'notPublished',afterDatasetsDraw(ch){const {ctx,scales}=ch,rtl=LANG==='ar';ctx.save();ctx.fillStyle=C.red;ctx.font='600 12px '+Chart.defaults.font.family;ctx.textBaseline='middle';ctx.textAlign=rtl?'right':'left';try{ctx.direction=rtl?'rtl':'ltr'}catch(e){}"
    "TJ.forEach((x,i)=>{if(x.v!=null)return;const y=scales.y.getPixelForValue(i),x0=scales.x.getPixelForValue(0);ctx.fillText(t('k_none')+' — '+L('no fund-wide 2030 target','لا مستهدف للصندوق لعام 2030'),rtl?x0-8:x0+8,y)});ctx.restore();}}]});   // audit pif-08: never a blank row",
    'code', 'pif-08: "Not published" written in the 2026–30 row of the chart')
rep(A, "document.getElementById('trajsrc').innerHTML=TJ.map(x=>`<b>${P([x.en,x.ar])}</b>: ${x.v==null?t('k_none'):iso(x.v+'%')} — ${esc(x.src)}`).join('<br>');",
    "document.getElementById('trajsrc').innerHTML=TJ.map(x=>`<b>${P([x.en,x.ar])}</b>: ${x.v==null?t('k_none'):iso(x.v+'%')} — ${esc(srcL(x.src))}`).join('<br>');",
    'code', 'pif-12: trajectory source list in Arabic')

# ---------------------------------------------------------------- pif-22: Arabic sector-shift diagram reads right to left
rep(A, "const trunc=(str,n)=>str.length>n?str.slice(0,n-1)+'…':str;", "const trunc=(str,n)=>str.length>n?str.slice(0,n-1)+'…':str, TL=rtl?52:44;", 'code', 'pif-22: Arabic group names are not cut short')
rep(A, "${esc(trunc(P([e.en,e.ar]),44))}", "${esc(trunc(P([e.en,e.ar]),TL))}", 'code', 'pif-22: Arabic group names are not cut short (2)')
rep(A, "svg.innerHTML=out;svg.style.direction='ltr';", "if(rtl)out=out.replace(/(class=\"(?:stitle|slab|elab)\") text-anchor=\"end\"/g,'$1 text-anchor=\"start\" direction=\"rtl\"');   // audit pif-22: Arabic titles and labels run right to left, numbers stay in place; company lists stay left to right\n  svg.innerHTML=out;svg.style.direction='ltr';",
    'code', 'pif-22: Arabic diagram text set right to left')

# ---------------------------------------------------------------- pif-23: keyboard for chips and the sources box
rep(A, "const modal=document.getElementById('modal');document.getElementById('bSrc').onclick=()=>{modal.classList.add('on')};document.getElementById('mclose').onclick=()=>modal.classList.remove('on');modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.remove('on')});document.addEventListener('keydown',e=>{if(e.key==='Escape')modal.classList.remove('on')});",
    "const modal=document.getElementById('modal');let mPrev=null;   // audit pif-23: focus moves into the box, stays there, and comes back on close\n"
    "const mOpen=()=>{mPrev=document.activeElement;modal.classList.add('on');modal.setAttribute('role','dialog');modal.setAttribute('aria-modal','true');setTimeout(()=>document.getElementById('mclose').focus(),0)};\n"
    "const mShut=()=>{if(!modal.classList.contains('on'))return;modal.classList.remove('on');if(mPrev&&mPrev.focus)mPrev.focus()};\n"
    "document.getElementById('bSrc').onclick=mOpen;document.getElementById('mclose').onclick=mShut;modal.addEventListener('click',e=>{if(e.target===modal)mShut()});\n"
    "document.addEventListener('keydown',e=>{if(e.key==='Escape'){mShut();pop.style.display='none';return}\n"
    "  if(e.key==='Tab'&&modal.classList.contains('on')){const f=[...modal.querySelectorAll('button,a[href],[tabindex=\"0\"]')].filter(x=>x.offsetParent!==null);if(!f.length)return;const a=f[0],z=f[f.length-1];\n"
    "    if(!modal.contains(document.activeElement)){e.preventDefault();a.focus()}else if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}\n"
    "  if((e.key==='Enter'||e.key===' ')&&e.target&&e.target.classList&&e.target.classList.contains('cite')){e.preventDefault();e.target.click()}});",
    'code', 'pif-23: sources box keeps and returns focus; chips open with Enter/Space; Escape closes popovers')
rep(A, "pop.innerHTML=`<b>${t('src_lbl')}</b> · ${g==='H'?'✓':g==='M'?'≈':'•'} ${g}<br>${esc(c.dataset.src)}`;",
    "pop.innerHTML=`<b>${t('src_lbl')}</b> · ${g==='N'?'?':(g==='H'?'✓':g==='M'?'≈':'•')+' '+g}<br>${esc(c.dataset.src)}`;", 'code', 'pif-21: popover shows "?" (not ✓) for a missing number')

# ---------------------------------------------------------------- pif-10 / pif-24 / focus ring: page styles
CSS = ('<style id="auditPif">'
       # pif-10: inside the hub keep "Where the numbers come from"; the hub has its own language and theme buttons
       'html.eh-embedded.eh-page-strat body header .ctl{display:flex !important}'
       'html.eh-embedded.eh-page-strat body header .ctl #bLang,html.eh-embedded.eh-page-strat body header .ctl #bTheme{display:none !important}'
       'html.eh-embedded.eh-page-strat body header .ctl #bSrc{background:var(--card);color:var(--eh-ink);border:1px solid var(--eh-line)}'
       'html.eh-embedded.eh-page-strat body header .ctl #bSrc:hover{background:var(--soft)}'
       # pif-24: on desktop the section links wrap instead of running off the right edge
       '@media (min-width:1024px){nav{flex-wrap:wrap;overflow-x:visible;white-space:normal}nav a{white-space:nowrap}}'
       # pif-23: visible focus on source chips
       '.cite:focus-visible{outline:2px solid var(--eh-c1,#0072BB);outline-offset:2px;border-radius:3px}'
       '</style>\n</head>')
rep(A, '</head>', CSS, 'design', 'pif-10/23/24: sources button visible in the hub; nav wraps on desktop; chip focus ring')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES[A])
write_change_table(os.path.join(HERE, 'change_table_audit_pif_strat'), 'Audit fixes — PIF Strategy 2026–2030 page (12 Oct 2026)')
print('patched: hub/pif_strategy_2026_2030.html')
