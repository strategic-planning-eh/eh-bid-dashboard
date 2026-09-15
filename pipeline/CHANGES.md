# CHANGES.md — human-written fix log for the hub's "What's New" panel

<!--
RULES
 • One fix per line, under a "## <ISO week>" heading (e.g. "## 2026-W36").
 • Format:   app | severity | view | EN | AR          (view is optional — leave the cell empty but keep the pipe)
     app      = stake | bids | clients | news | hub
     severity = major | minor
 • Write for a non-technical colleague: say what they will notice ("Fixed: charts were unreadable on iPhone…").
 • The build parses this file. A malformed line FAILS the build. A fix that is not written here is NOT shipped.
 • Arabic follows English in the same line, same commit. Numbers inside Arabic are fine — the panel isolates them.
 • This file is confidential like the rest of the hub.
-->

## 2026-W38
bids | minor | Data | Fixed: a rejection reason typed into the tracker's winner column ("وجود عطاء مالي مقدم من منافس اخر", bid 81/26) was read as a competitor. Cells that read as a reason or a tender title are now kept out of every competitor list, and the reason is filed as the loss reason. | تصحيح: سبب رفض كُتب في عمود «الشركة الفائزة» («وجود عطاء مالي مقدم من منافس اخر»، المنافسة 81/26) قُرئ كمنافس. الخلايا التي تُقرأ كسبب أو كعنوان منافسة تُستبعد الآن من كل قوائم المنافسين، ويُسجَّل السبب كسبب الخسارة.
bids | major | Executive Summary | New tab between All Tenders and Watchlist: six headline cards, the tender funnel, win rate by deal size and service line, a competitor threat matrix (who actually takes tenders off EH), EH's price position in the field, and a "needs a decision" list — every chart exportable as PNG. | تبويب جديد بين «جميع المنافسات» و«قائمة المتابعة»: ست بطاقات رئيسية، قمع المنافسات، نسبة الفوز حسب حجم الصفقة وخط الخدمة، مصفوفة تهديد المنافسين (من يأخذ المنافسات من EH فعلاً)، موقع سعر EH بين المتنافسين، وقائمة «يحتاج قراراً» — وكل رسم قابل للتصدير كصورة PNG.
clients | minor | Revenue Bridge | Fixed: in the client list that opens from a bridge bar, Arabic names and the "SAR a → SAR b" figures overlapped; the figures now sit on their own line under the name. The panel is also readable in dark mode. | تصحيح: في قائمة العملاء التي تُفتح من أعمدة جسر الإيرادات كانت الأسماء العربية تتداخل مع أرقام «ر.س أ ← ر.س ب»؛ أصبحت الأرقام الآن في سطر مستقل تحت الاسم، وباتت اللوحة مقروءة في الوضع الداكن.

## 2026-W37
hub | major | Data | New rule: the bid tracker (EH-WIN-02-F01) is the single source for who bids against EH. Every app now shows the same stamp — "Competitors N · tracker as of <date>" — and the map's bid flags are recomputed from the tracker on every publish. | قاعدة جديدة: جدول تتبع العطاءات (EH-WIN-02-F01) هو المصدر الوحيد لمن يتقدّم ضد EH. تعرض كل التطبيقات الآن الختم نفسه — «المنافسون N · وفق جدول العطاءات حتى <التاريخ>» — ويُعاد حساب مؤشرات العطاءات في الخريطة من الجدول عند كل نشر.
stake | major | Data | Corrected: about 255 companies were flagged as bidders on workbook research the tracker does not confirm; they no longer count and are marked "Claimed bidder (unverified)" in the company panel. | تصحيح: كانت نحو 255 شركة مُعلَّمة كمتقدّمة ضد EH بناءً على بحث في المصنّف لا يؤكده الجدول؛ لم تعد تُحتسب وتظهر بعلامة «متقدّم مُدّعى (غير مؤكد)» في لوحة الشركة.
stake | minor | Filters | The map now opens on every company that bid against EH (all tiers) instead of Tier 1 only; the Tier 1 view is one click away in Filters. | تفتح الخريطة الآن على كل الشركات التي تقدّمت ضد EH (كل الفئات) بدلاً من الفئة الأولى فقط؛ وعرض الفئة الأولى على بُعد نقرة في الفلاتر.

## 2026-W36
stake | major | Bid View | Fixed: the Bid View and Saudi Map inside the Stakeholder & Competitive Map showed an old copy of the bid data (144 tenders); they now refresh from the live Bid & Tender build on every publish. | إصلاح: كان عرض المنافسات وخريطة السعودية داخل خريطة أصحاب المصلحة يعرضان نسخة قديمة من بيانات المنافسات (144 منافسة)؛ يتحدثان الآن من بناء المنافسات المباشر عند كل نشر.
stake | minor | Regional View | Fixed: the region × company type heat map was always empty. | إصلاح: كانت خريطة الحرارة (المنطقة × نوع الشركة) فارغة دائماً.
stake | major | Methodology | Corrected: the Arabic methodology and the "How is the Total Score calculated?" answer still described the old v1 scoring; both now match the v2 model (Low-confidence rows are floored, never filled). | تصحيح: كانت منهجية التقييم بالعربية وجواب «كيف تُحسب الدرجة الكلية؟» يصفان النموذج القديم؛ أصبحا الآن مطابقَين للإصدار الثاني (الشركات ذات الموثوقية المنخفضة تُحد بحدّ أدنى ولا تُعبّأ بقيم مفترضة).
stake | minor | Header | Corrected: the organization count in the header is now read from the data (it showed an old figure in Arabic). | تصحيح: عدد المنظمات في الترويسة يُقرأ الآن من البيانات (كان يعرض رقماً قديماً بالعربية).
stake | minor | Filters | Renamed "Stakeholder categories" to "Company type" everywhere, and the map hint now tells phone users where the filter drawer is. | أُعيدت تسمية «فئات الأطراف» إلى «نوع الشركة» في كل مكان، وأصبح تلميح الخريطة يوضح لمستخدمي الهاتف مكان درج المرشحات.
hub | major | What's New | New: this What's New panel — weekly fixes, company changes, bid outcomes and data-refresh dates, in English and Arabic, on every device. | جديد: لوحة «ما الجديد» — الإصلاحات الأسبوعية وتغييرات الشركات ونتائج المنافسات وتواريخ تحديث البيانات، بالعربية والإنجليزية وعلى كل الأجهزة.
hub | minor | Header | The "Data refreshed" time now uses one format everywhere (e.g. 30 Aug · 09:00). | أصبح وقت «آخر تحديث للبيانات» بصيغة واحدة في كل مكان (مثل 30 Aug · 09:00).
clients | minor | Executive | Wording: "Total book 25+26" is now "Total contract value 2025–2026"; instructions no longer say "click" or "hover" where you tap. | صياغة: «Total book 25+26» أصبحت «إجمالي قيمة العقود 2025–2026»؛ ولم تعد التعليمات تقول «انقر» أو «مرّر» حيث تلمس الشاشة.

## 2026-W35
stake | major | Scoring | New v2 scoring model rolled out: Total Score now weights how much of EH's own business a company could take (service overlap first). Low-confidence rows are floored at a small-company minimum instead of being filled with averages. | طُبّق نموذج التقييم الجديد (الإصدار الثاني): الدرجة الكلية توزن الآن حجم أعمال EH التي يمكن للشركة أخذها (تداخل الخدمات أولاً). الشركات ذات الموثوقية المنخفضة تُحد بحدّ أدنى بدلاً من تعبئتها بمتوسطات.
stake | major | Data | Research programme applied: data confidence raised for the bid-active rivals researched in phases 1a/1b (official register or two independent sources required). | طُبّق برنامج البحث: رُفعت موثوقية البيانات للمنافسين النشطين في المنافسات الذين بُحثوا في المرحلتَين 1أ/1ب (يُشترط سجل رسمي أو مصدران مستقلان).
stake | minor | Filters | The "Bid Competitor" company type was retired — bidding against EH is shown as a flag and an encounter count, not as a type. | أُلغي نوع الشركة «منافس عطاءات» — يظهر التقدم ضد EH كمؤشر وعدد مواجهات، لا كنوع.
bids | minor | Overview | Tender 2026/#23 (Environmental Emergency Services at Saudi Energy Power Plants, SEC) marked Won. | سُجّلت المنافسة 2026/#23 (خدمات الطوارئ البيئية في محطات الكهرباء، الشركة السعودية للكهرباء) كفوز لـEH.

## 2026-W34
stake | major | Data | Duplicate companies merged: Al Mandariyah Environmental Services (Arabic and English rows), Namaa / GESCO, and 28 pairs with identical names. Each keeps one profile. | دُمجت الشركات المكررة: المندرية للخدمات البيئية (صفّا العربية والإنجليزية)، نماء / جيسكو، و28 زوجاً بأسماء متطابقة. لكل شركة ملف واحد.
hub | major | Mobile | Fixed: phone layout — bottom tab bar, filter drawer, tablet tiers, landscape-phone header. | إصلاح: تخطيط الهاتف — شريط تبويبات سفلي، درج المرشحات، مستويات الجهاز اللوحي، ترويسة الهاتف الأفقي.
clients | major | Executive | Fixed: charts were unreadable on iPhone in the Clients executive view; charts can now be swiped. | إصلاح: كانت الرسوم غير مقروءة على آيفون في العرض التنفيذي للعملاء؛ يمكن الآن تمرير الرسوم بالسحب.
stake | minor | Map | New zoom controls (+ / − / reset) on the bubble and radial maps. | أزرار تكبير جديدة (+ / − / إعادة) على خريطتَي الفقاعات والدائرة.

## 2026-W33
hub | major | iOS | Fixed: on iPhone and iPad the dashboards did not fill the screen inside the hub (Safari iframe sizing). | إصلاح: على آيفون وآيباد لم تكن اللوحات تملأ الشاشة داخل المنصة (مقاس إطار سفاري).
hub | minor | Dark mode | Fixed: remaining light-coloured panels and unreadable text in dark mode across all views. | إصلاح: بقايا اللوحات الفاتحة والنصوص غير المقروءة في الوضع الداكن عبر كل اللوحات.
bids | minor | Executive | New: year toggle (2025 / 2026 / Both) and animated quadrant chart in the executive view. | جديد: مبدّل السنة (2025 / 2026 / الكل) ورسم رباعي متحرك في العرض التنفيذي.
hub | minor | Header | CONFIDENTIAL notice added to the hub header on every device. | أُضيف تنبيه «سرّي» إلى ترويسة المنصة على كل الأجهزة.
