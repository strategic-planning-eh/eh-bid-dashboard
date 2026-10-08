"""patch_etimad_plain.py — plain-language pass on the Government Tenders (Etimad) tab (feedback 8 Oct 2026:
"the page is full of jargon").

Every replacement swaps wording only; logic and data are untouched. Terms changed across the tab:
  capture → update / check · agency → buyer · Core / Adjacent → Core service / Related ·
  Priority → key buyer · document fee → price of the tender documents · sector → type of work ·
  requester / issuer → buyer · "relevant" → "EH can bid for".
A collapsible "Words used on this page" box is added under the known-gap note.

Run once:  python3 pipeline/patch_etimad_plain.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, 'build_etimad_page.py')
if 'Words used on this page' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'page')

def R(old, new, note='plain language'):
    n = FILES['page'].count(old)
    if n == 0:
        FAILURES.append({'file': 'page', 'note': note, 'old': old[:120]})
        return
    rep('page', old, new, 'plain', note, count=n)

PAIRS = [
 # ---- stamp, source line, known gap
 ("L('Last captured: ','آخر التقاط: ')", "L('Updated from Etimad: ','آخر تحديث من اعتماد: ')"),
 ("L('No capture loaded yet','لم يُحمَّل أي التقاط بعد')", "L('No Etimad data loaded yet','لم تُحمَّل بيانات من اعتماد بعد')"),
 ('"Source: Etimad public tender listing, read once a week (Sunday). Titles and agency names are shown exactly as published."',
  '"Where this comes from: the public list of tenders on Etimad, the government tendering website, checked every Sunday. Tender titles and buyer names are shown exactly as Etimad publishes them."'),
 ('"المصدر: قائمة المنافسات العامة في منصة اعتماد، تُقرأ أسبوعيًا (الأحد). العناوين وأسماء الجهات كما نُشرت تمامًا."',
  '"المصدر: قائمة المنافسات العامة في منصة اعتماد للمنافسات الحكومية، نراجعها كل أحد. عناوين المنافسات وأسماء الجهات كما ينشرها اعتماد تمامًا."'),
 ('"Known gap: direct purchases can open and close within 3–15 days, between two Sunday captures, so some are missed. Public tenders (usually 14–30 days) are caught with time to study. To open a tender on Etimad, copy its reference number into Etimad\'s search."',
  '"Please note: direct purchases (small orders placed without a full tender) can open and close within 3–15 days, between two Sunday checks, so some are missed. Public tenders usually stay open 14–30 days, so we see them in time to study them. To open a tender on Etimad, copy its number into Etimad\'s search box."'),
 ('"فجوة معروفة: قد يُطرح الشراء المباشر ويُغلق خلال 3–15 يومًا بين التقاطين، فيفوت بعضه. أما المنافسات العامة (14–30 يومًا عادةً) فتُلتقط في وقت يسمح بدراستها. لفتح منافسة في اعتماد انسخ رقمها المرجعي وابحث به في المنصة."',
  '"تنبيه: قد يُطرح الشراء المباشر (طلبات صغيرة دون منافسة كاملة) ويُغلق خلال 3–15 يومًا بين مراجعتين، فيفوتنا بعضه. أما المنافسات العامة فتبقى مفتوحة عادةً 14–30 يومًا، فنراها في وقت يسمح بدراستها. لفتح منافسة في اعتماد انسخ رقمها وابحث به في المنصة."'),
 # ---- KPI strips
 ('data-en="Etimad market" data-ar="سوق اعتماد">Etimad market<', 'data-en="All government tenders on Etimad" data-ar="كل المنافسات الحكومية في اعتماد">All government tenders on Etimad<'),
 ('data-en="For EH" data-ar="لآفاق البيئة">For EH<', 'data-en="Tenders EH can bid for" data-ar="منافسات يمكن لآفاق التقدم لها">Tenders EH can bid for<'),
 ("L('Active tenders on Etimad today, all sectors (site counter)','المنافسات النشطة في اعتماد اليوم بكل القطاعات (عدّاد المنصة)')",
  "L('Tenders open on Etimad today, all types of work (Etimad’s own count)','المنافسات المفتوحة في اعتماد اليوم بكل أنواع العمل (عدّاد المنصة)')"),
 ("L('Tenders captured by EH searches, any relevance','منافسات التقطتها بحوث آفاق، بكل درجات الصلة')", "L('Tenders found by EH’s searches','منافسات وجدتها بحوث آفاق')"),
 ("L('Of which relevant to EH (Core + Adjacent)','منها ذات صلة بآفاق (أساسي + مجاور)')", "L('Of these, ones EH can bid for','منها ما يمكن لآفاق التقدم له')"),
 ("L('Open relevant tenders','منافسات ذات صلة مفتوحة')", "L('Open now','مفتوحة الآن')"),
 ("L('New relevant this week (published in the 7 days before the last capture)','جديدة ذات صلة هذا الأسبوع (نُشرت خلال 7 أيام قبل آخر التقاط)')",
  "L('New this week (published in the 7 days before the last update)','جديدة هذا الأسبوع (نُشرت خلال 7 أيام قبل آخر تحديث)')"),
 ("L('Priority tenders open','منافسات ذات أولوية مفتوحة')", "L('Open, from key buyers ★','مفتوحة من جهات مهمة ★')"),
 ("L('Open and not yet in the bid tracker','مفتوحة وغير مسجلة في جدول المنافسات')", "L('Open, not yet logged in the bid tracker','مفتوحة وغير مسجلة بعد في جدول المنافسات')"),
 # ---- labels used everywhere
 ("const REL={'Core':['Core','أساسي'],'Adjacent':['Adjacent','مجاور'],'Not EH':['Not EH','خارج نطاق آفاق']};",
  "const REL={'Core':['Core service','خدمة أساسية'],'Adjacent':['Related','ذات صلة'],'Not EH':['Not for EH','خارج نطاق آفاق']};"),
 ("L('Core','أساسي')", "L('Core service','خدمة أساسية')"),
 ("L('Adjacent','مجاور')", "L('Related','ذات صلة')"),
 ('data-en="Core" data-ar="أساسي">Core<', 'data-en="Core service" data-ar="خدمة أساسية">Core service<'),
 ('data-en="Adjacent" data-ar="مجاور">Adjacent<', 'data-en="Related" data-ar="ذات صلة">Related<'),
 ("const PRI={'tier':['agency is Tier 1 or Government on the stakeholder map','الجهة من الفئة الأولى أو حكومية في خريطة أصحاب المصلحة'],'client':['agency is an EH client','الجهة عميل لآفاق البيئة'],'regulator':['agency is a regulator','الجهة تنظيمية'],'giga':['giga-project or PIF entity','مشروع كبير أو جهة تابعة لصندوق الاستثمارات العامة']};",
  "const PRI={'tier':['the buyer is Tier 1 or a government body on the stakeholder map','الجهة من الفئة الأولى أو جهة حكومية في خريطة أصحاب المصلحة'],'client':['the buyer is an EH client','الجهة عميل لآفاق البيئة'],'regulator':['the buyer is a regulator','الجهة تنظيمية'],'giga':['a giga-project or a company owned by the Public Investment Fund (PIF)','مشروع كبير أو شركة مملوكة لصندوق الاستثمارات العامة']};"),
 # ---- filters
 ("['rel',L('Relevant (Core + Adjacent)','ذات صلة (أساسي + مجاور)')],['Core',L('Core only','أساسي فقط')],['Adjacent',L('Adjacent only','مجاور فقط')],['all',L('All captured tenders','كل المنافسات الملتقطة')]",
  "['rel',L('EH can bid for (core + related)','يمكن لآفاق التقدم لها (أساسية + ذات صلة)')],['Core',L('Core services only','الخدمات الأساسية فقط')],['Adjacent',L('Related only','ذات الصلة فقط')],['all',L('All tenders found','كل المنافسات التي وُجدت')]"),
 ("L('All agencies','كل الجهات')", "L('All buyers','كل الجهات')"),
 ("L('All tiers','كل الفئات')", "L('All stakeholder-map tiers','كل فئات خريطة أصحاب المصلحة')"),
 ("L('Not on the map','غير موجودة في الخريطة')", "L('Not on the stakeholder map','غير موجودة في خريطة أصحاب المصلحة')"),
 ("L('All map categories','كل تصنيفات الخريطة')", "L('All stakeholder-map categories','كل تصنيفات خريطة أصحاب المصلحة')"),
 ('title="Region is not captured yet · المنطقة غير ملتقطة بعد"><option data-en="Region: not captured yet" data-ar="المنطقة: غير ملتقطة بعد">Region: not captured yet<',
  'title="Region is not available yet · المنطقة غير متاحة بعد"><option data-en="Region: not available yet" data-ar="المنطقة: غير متاحة بعد">Region: not available yet<'),
 ('data-en="Priority only" data-ar="ذات الأولوية فقط">Priority only<', 'data-en="Key buyers only ★" data-ar="الجهات المهمة فقط ★">Key buyers only ★<'),
 ("L(`${rows.length} of ${T.length} captured tenders shown`,`عرض ${rows.length} من ${T.length} منافسة ملتقطة`)", "L(`Showing ${rows.length} of ${T.length} tenders found`,`عرض ${rows.length} من ${T.length} منافسة`)"),
 ("L('capture of ','التقاط ')", "L('update of ','تحديث ')"),
 # ---- tender list
 ('data-en="Default view: relevant tenders that are still open, soonest deadline first. Click a column to sort. Hover a relevance tag to see the term that matched; hover ★ to see why a tender is Priority." data-ar="العرض الافتراضي: المنافسات ذات الصلة المفتوحة، الأقرب موعدًا أولًا. انقر عنوان العمود للترتيب. مرّر المؤشر على وسم الصلة لرؤية العبارة المطابقة، وعلى ★ لمعرفة سبب الأولوية.">Default view: relevant tenders that are still open, soonest deadline first.<',
  'data-en="Shown first: open tenders EH can bid for, nearest deadline first. Click a column heading to sort. Point at a Core service or Related tag to see the words that matched; point at ★ to see why the buyer is a key buyer." data-ar="يظهر أولًا: المنافسات المفتوحة التي يمكن لآفاق التقدم لها، الأقرب موعدًا أولًا. انقر عنوان العمود للترتيب. مرّر المؤشر على وسم «خدمة أساسية» أو «ذات صلة» لرؤية الكلمات المطابقة، وعلى ★ لمعرفة سبب اعتبار الجهة مهمة.">Shown first: open tenders EH can bid for, nearest deadline first.<'),
 ("L('Relevance','الصلة')", "L('Fit for EH','الملاءمة لآفاق')"),
 ("L('Agency','الجهة')", "L('Buyer','الجهة')"),
 ("L('Service line','خط الخدمة')", "L('EH service','خدمة آفاق')"),
 ("L('Document fee (SAR)','قيمة الكراسة (ريال)')", "L('Price of tender documents (SAR)','ثمن وثائق المنافسة (ريال)')"),
 ("L('Enquiries by','آخر موعد للاستفسارات')", "L('Questions accepted until','آخر موعد للاستفسارات')"),
 ("L('Bid opening','فتح العروض')", "L('Bids opened on','فتح العروض')"),
 ("L('Priority','أولوية')", "L('Key buyer','جهة مهمة')"),
 ("L('Etimad reference','الرقم المرجعي')", "L('Etimad number','رقم المنافسة في اعتماد')"),
 ("L('Not captured','غير ملتقطة')", "L('Not available','غير متاحة')"),
 ("L('Region is shown only on each tender\\'s own Etimad page and is not captured yet.','تظهر المنطقة في صفحة المنافسة فقط ولم تُلتقط بعد.')",
  "L('Etimad shows the region only on each tender’s own page, which we do not read yet.','يعرض اعتماد المنطقة في صفحة كل منافسة فقط، ولا نقرؤها بعد.')"),
 ("${L('Tracker','الجدول')} #${tr.sn} · ${tr.year}", "${L('Bid tracker row','صف جدول المنافسات')} ${tr.sn} (${tr.year})"),
 ("L('No EH service term matched','لم تطابق أي عبارة من خدمات آفاق')", "L('No EH service words found in the title','لم تُوجد في العنوان كلمات من خدمات آفاق')"),
 ("L('Matched: ','طابق: ')", "L('Words found: ','الكلمات المطابقة: ')"),
 # ---- trends for EH
 ('data-en="Where the market is going — relevant to EH" data-ar="إلى أين يتجه السوق — ما يخص آفاق البيئة">Where the market is going — relevant to EH<',
  'data-en="Trends in tenders EH can bid for" data-ar="اتجاهات المنافسات التي يمكن لآفاق التقدم لها">Trends in tenders EH can bid for<'),
 ('data-en="Charts follow the filters above but include closed tenders, so they show the market rather than only what is open today." data-ar="تتبع الرسوم المرشحات أعلاه لكنها تشمل المنافسات المغلقة، لتعرض السوق لا ما هو مفتوح اليوم فقط.">Charts follow the filters above but include closed tenders.<',
  'data-en="These charts follow the filters above but also count closed tenders, so they show the trend, not just what is open today." data-ar="تتبع هذه الرسوم المرشحات أعلاه لكنها تحتسب المنافسات المغلقة أيضًا، لتعرض الاتجاه لا ما هو مفتوح اليوم فقط.">These charts follow the filters above but also count closed tenders.<'),
 ('data-en="Relevant tenders by month published" data-ar="المنافسات ذات الصلة حسب شهر النشر">Relevant tenders by month published<',
  'data-en="Tenders EH can bid for, by month published" data-ar="المنافسات المناسبة لآفاق حسب شهر النشر">Tenders EH can bid for, by month published<'),
 ("L('Relevant tenders by month published','المنافسات ذات الصلة حسب شهر النشر')", "L('Tenders EH can bid for, by month published','المنافسات المناسبة لآفاق حسب شهر النشر')"),
 ("L(`Covers what has been captured so far (tenders published from ${fmtD(firstPub)}). Older months fill in with the 3-year history load.`,`يغطي ما التُقط حتى الآن (منافسات منشورة منذ ${fmtD(firstPub)}). تكتمل الأشهر الأقدم بعد تحميل سجل السنوات الثلاث.`)",
  "L(`Covers tenders found so far (published from ${fmtD(firstPub)}). Earlier months appear once three years of history are loaded.`,`يغطي المنافسات التي وُجدت حتى الآن (منشورة منذ ${fmtD(firstPub)}). تظهر الأشهر الأقدم بعد تحميل سجل السنوات الثلاث.`)"),
 ('data-en="By service line" data-ar="حسب خط الخدمة">By service line<', 'data-en="By EH service" data-ar="حسب خدمة آفاق">By EH service<'),
 ("L('Relevant tenders by service line','حسب خط الخدمة')", "L('Tenders EH can bid for, by EH service','حسب خدمة آفاق')"),
 ("L('General waste work (no single line)','أعمال نفايات عامة (دون خط محدد)')", "L('General waste work (no single EH service)','أعمال نفايات عامة (دون خدمة محددة)')"),
 ("L('Region is shown only on each tender\\'s own Etimad page, so it is not captured yet. Searched, none found','المنطقة تظهر في صفحة كل منافسة فقط، لذا لم تُلتقط بعد. تم البحث، ولا توجد بيانات')",
  "L('Etimad shows the region only on each tender’s own page, which we do not read yet, so there is nothing to show','يعرض اعتماد المنطقة في صفحة كل منافسة فقط، ولا نقرؤها بعد، لذا لا توجد بيانات')"),
 ('data-en="Share of the whole Etimad market" data-ar="الحصة من سوق اعتماد كاملًا">Share of the whole Etimad market<',
  'data-en="How much of Etimad fits EH" data-ar="كم من منافسات اعتماد يناسب آفاق">How much of Etimad fits EH<'),
 ("L(`At the last capture Etimad listed <b>${fmtN(+cnt.value)}</b> active tenders across all sectors; <b>${op.length}</b> of them are relevant to EH (${(100*op.length/+cnt.value).toFixed(1)}%).`,`عند آخر التقاط أدرجت منصة اعتماد <b>${fmtN(+cnt.value)}</b> منافسة نشطة في كل القطاعات، منها <b>${op.length}</b> ذات صلة بآفاق البيئة (${(100*op.length/+cnt.value).toFixed(1)}%).`)",
  "L(`On the last update Etimad listed <b>${fmtN(+cnt.value)}</b> open tenders of every kind; <b>${op.length}</b> of them are ones EH can bid for (${(100*op.length/+cnt.value).toFixed(1)}%).`,`عند آخر تحديث أدرجت منصة اعتماد <b>${fmtN(+cnt.value)}</b> منافسة مفتوحة من كل الأنواع، منها <b>${op.length}</b> يمكن لآفاق التقدم لها (${(100*op.length/+cnt.value).toFixed(1)}%).`)"),
 ("L('Searched, none found: no market counter recorded yet.','تم البحث، ولا يوجد عدّاد سوق مسجل بعد.')", "L('Searched, none found: Etimad’s count of open tenders has not been recorded yet.','تم البحث، ولم يُسجَّل عدّاد المنافسات المفتوحة في اعتماد بعد.')"),
 ('data-en="Fastest-growing and shrinking service lines" data-ar="أسرع خطوط الخدمة نموًا وتراجعًا">Fastest-growing and shrinking service lines<',
  'data-en="EH services growing and shrinking fastest" data-ar="أسرع خدمات آفاق نموًا وتراجعًا">EH services growing and shrinking fastest<'),
 ("L('Figures from all captured tenders, not the current filters.','الأرقام من كل المنافسات الملتقطة وليست من المرشحات الحالية.')", "L('These figures cover every tender found, not just the current filters.','تشمل هذه الأرقام كل المنافسات التي وُجدت، لا المرشحات الحالية فقط.')"),
 # ---- python notes()
 ('f"{SL[lid][\'en\']} is the largest relevant line: {n} of {len(T)} relevant tenders captured."', 'f"{SL[lid][\'en\']} is the EH service with the most tenders: {n} of the {len(T)} tenders EH can bid for."'),
 ('f"«{SL[lid][\'ar\']}» أكبر خط خدمة: {n} من أصل {len(T)} منافسة ذات صلة."', 'f"«{SL[lid][\'ar\']}» أكثر خدمات آفاق طلبًا: {n} من أصل {len(T)} منافسة يمكن لآفاق التقدم لها."'),
 ('f"The most frequent requester is {ag} with {n} relevant tenders"', 'f"The buyer with the most tenders EH can bid for is {ag}, with {n}"'),
 ('f"{len(dp)} of {len(T)} relevant tenders ({round(100*len(dp)/len(T))}%) are direct purchases, which often stay open for under two weeks — a weekly capture can miss some of them."',
  'f"{len(dp)} of the {len(T)} tenders EH can bid for ({round(100*len(dp)/len(T))}%) are direct purchases (small, quick orders). They often stay open for under two weeks, so a weekly check can miss some."'),
 ('قد يفوت الالتقاط الأسبوعي بعضها', 'قد تفوت المراجعة الأسبوعية بعضها'),
 ('f"{len(op)} relevant tenders were open at the last capture; {len(ns)} of them are not yet in the bid tracker."', 'f"{len(op)} tenders EH can bid for were open at the last update; {len(ns)} of them are not yet logged in the bid tracker."'),
 ('كانت {len(op)} منافسة ذات صلة مفتوحة عند آخر التقاط', 'كانت {len(op)} منافسة يمكن لآفاق التقدم لها مفتوحة عند آخر تحديث'),
 # ---- whole market
 ('data-en="Where the market is going — all Etimad tenders" data-ar="إلى أين يتجه السوق — كل منافسات اعتماد">Where the market is going — all Etimad tenders<',
  'data-en="What the Kingdom is buying — every tender on Etimad" data-ar="ما الذي تشتريه المملكة — كل منافسات اعتماد">What the Kingdom is buying — every tender on Etimad<'),
 ("whatever its sector — not only what fits EH. Counts only; the filters above do not apply here. Bars split tenders still open at the capture from those already closed.`",
  "in every type of work, not only what fits EH. Only counts are shown, and the filters above do not apply here. In each bar, blue is tenders still open when we checked and green is tenders already closed.`"),
 ("أيًا كان قطاعها — لا ما يناسب آفاق فقط. أعداد فقط؛ ولا تنطبق المرشحات أعلاه هنا. تفصل الأعمدة المنافسات المفتوحة عند الالتقاط عن المغلقة.`",
  "في كل أنواع العمل، لا ما يناسب آفاق فقط. تُعرض الأعداد فقط، ولا تنطبق المرشحات أعلاه هنا. في كل عمود: الأزرق منافسات كانت مفتوحة عند المراجعة، والأخضر منافسات أُغلقت.`"),
 ("L('Open at capture','مفتوحة عند الالتقاط')", "L('Still open when checked','مفتوحة عند المراجعة')"),
 ('data-en="Open at capture" data-ar="مفتوحة عند الالتقاط">Open at capture<', 'data-en="Still open when checked" data-ar="مفتوحة عند المراجعة">Still open when checked<'),
 ("L('Searched, none found: the full-market capture has not run yet.','تم البحث، ولا توجد بيانات: لم يُشغَّل التقاط السوق الكامل بعد.')",
  "L('Searched, none found: the weekly read of all Etimad tenders has not run yet.','تم البحث، ولا توجد بيانات: لم تُشغَّل القراءة الأسبوعية لكل منافسات اعتماد بعد.')"),
 ('data-en="By sector (Etimad activity, grouped)" data-ar="حسب القطاع (نشاط اعتماد مجمّعًا)">By sector<', 'data-en="By type of work" data-ar="حسب نوع العمل">By type of work<'),
 ('data-en="Who is buying (largest agencies, grouped)" data-ar="من يشتري (أكبر الجهات مجمّعة)">Who is buying<', 'data-en="Who is buying (buyers grouped by kind)" data-ar="من يشتري (الجهات مجمّعة حسب نوعها)">Who is buying<'),
 ('data-en="Top 15 agencies" data-ar="أعلى 15 جهة">Top 15 agencies<', 'data-en="15 biggest buyers" data-ar="أكبر 15 جهة مشترية">15 biggest buyers<'),
 ("L('Document fees (size estimate)','قيمة الكراسات (تقدير للحجم)')", "L('Price of tender documents (rough sign of size)','ثمن وثائق المنافسات (مؤشر تقريبي للحجم)')"),
 ("L('Share of document fees','الحصة من قيمة الكراسات')", "L('Share of document prices (rough size)','الحصة من ثمن الوثائق (حجم تقريبي)')"),
 ("L('Share now','الحصة الآن')", "L('Share, latest period','الحصة، الفترة الأحدث')"),
 ("L('Share before','الحصة سابقًا')", "L('Share, earlier period','الحصة، الفترة السابقة')"),
 ("L('Change (points)','التغير (نقاط)')", "L('Change (percentage points)','التغير (نقاط مئوية)')"),
 ("L('Sector','القطاع')", "L('Type of work','نوع العمل')"),
 ("Expansion is measured as a change in each sector\\'s share between capture windows. One window is on file so far; the comparison appears after the next weekly full-market capture.",
  "Growth is measured as the change in each type of work’s share between two periods. Only one period is on file so far; the comparison appears after the next weekly read of all Etimad tenders."),
 ("يُقاس التوسع بتغيّر حصة كل قطاع بين فترات الالتقاط. توجد فترة واحدة حتى الآن؛ وتظهر المقارنة بعد الالتقاط الأسبوعي التالي للسوق الكامل.",
  "يُقاس التوسع بتغيّر حصة كل نوع عمل بين فترتين. توجد فترة واحدة حتى الآن؛ وتظهر المقارنة بعد القراءة الأسبوعية التالية لكل منافسات اعتماد."),
 # ---- python market_notes()
 ("'Biggest sectors by number of tenders: '", "'Biggest types of work by number of tenders: '"),
 ("'أكبر القطاعات بعدد المنافسات: '", "'أكبر أنواع العمل بعدد المنافسات: '"),
 ("'By document fees — a rough sign of contract size, not contract value — the largest sectors are '", "'By the price of tender documents (a rough sign of contract size, not the contract value), the biggest types of work are '"),
 ("'بحسب قيمة الكراسات — مؤشر تقريبي لحجم العقد وليست قيمته — أكبر القطاعات '", "'بحسب ثمن وثائق المنافسة (مؤشر تقريبي لحجم العقد وليس قيمته) أكبر أنواع العمل '"),
 ("of fees, ", "of document prices, "),
 ("'Who is buying (top agencies, grouped): '", "'Who is buying: '"),
 ("'من يشتري (أكبر الجهات مجمّعة): '", "'من يشتري: '"),
 ('f"Environment & waste is listed as the activity on only {env[\'n\']} tenders ({round(100*env[\'n\']/tot,1)}%). Most EH-relevant work sits under other activities — water, health, consulting — which is why the tab tags tenders by their titles, not by Etimad\'s activity."',
  'f"Only {env[\'n\']} tenders ({round(100*env[\'n\']/tot,1)}%) are listed under “Environment & waste”. Most work EH can do is listed under other headings, such as water, health and consulting, so this tab sorts tenders by their titles rather than by Etimad\'s heading."'),
 ('Direct purchases are {round(100*dp[\'n\']/tot)}% of tenders but only {round(100*dp[\'fees\']/tf)}% of document fees; public tenders carry {round(100*pt[\'fees\']/tf)}%.',
  'Direct purchases (small, quick orders) are {round(100*dp[\'n\']/tot)}% of tenders but only {round(100*dp[\'fees\']/tf)}% of document prices; public tenders carry {round(100*pt[\'fees\']/tf)}%.'),
 # ---- biggest buyers
 ('data-en="Biggest requesters" data-ar="أكبر الجهات الطارحة">Biggest requesters<', 'data-en="Biggest buyers" data-ar="أكبر الجهات المشترية">Biggest buyers<'),
 ('data-en="Agencies ranked by relevant tenders. Document fees are the price of the tender documents — a rough sign of size, never the contract value." data-ar="الجهات مرتبة حسب المنافسات ذات الصلة. قيمة الكراسة هي ثمن وثائق المنافسة — مؤشر تقريبي للحجم وليست قيمة العقد.">Agencies ranked by relevant tenders.<',
  'data-en="Buyers ranked by the number of tenders EH can bid for. The document price is what a bidder pays for the tender papers: a rough sign of size, never the contract value." data-ar="الجهات مرتبة حسب عدد المنافسات التي يمكن لآفاق التقدم لها. ثمن الوثائق هو ما يدفعه المتقدم لشراء وثائق المنافسة: مؤشر تقريبي للحجم وليس قيمة العقد.">Buyers ranked by the number of tenders EH can bid for.<'),
 ('data-en="Top 10 agencies" data-ar="أعلى 10 جهات">Top 10 agencies<', 'data-en="10 biggest buyers" data-ar="أكبر 10 جهات">10 biggest buyers<'),
 ('data-en="New issuers (last 6 months)" data-ar="جهات جديدة (آخر 6 أشهر)">New issuers (last 6 months)<', 'data-en="New buyers (last 6 months)" data-ar="جهات جديدة (آخر 6 أشهر)">New buyers (last 6 months)<'),
 ("L('\"New issuer\" means no relevant tender before the last 6 months. With about '+span+' months of data every agency would look new, so this list waits for the history load.'",
  "L('“New buyer” means a buyer with no tender EH could bid for before the last 6 months. With only about '+span+' months of data every buyer would look new, so this list waits until three years of history are loaded.'"),
 ("L('Relevant tenders','منافسات ذات صلة')", "L('Tenders EH can bid for','منافسات يمكن لآفاق التقدم لها')"),
 ("L('Document fees (SAR, size estimate)','قيمة الكراسات (ريال، تقدير)')", "L('Document prices (SAR, rough size)','ثمن الوثائق (ريال، حجم تقريبي)')"),
 ("L('Document fees (estimate of size, not contract value)','قيمة الكراسات (تقدير للحجم وليست قيمة العقد)')", "L('Price of tender documents (rough size, not the contract value)','ثمن وثائق المنافسات (حجم تقريبي وليس قيمة العقد)')"),
 ("L('Tier','الفئة')", "L('Stakeholder-map tier','الفئة في الخريطة')"),
 ("L('Map category','تصنيف الخريطة')", "L('Stakeholder-map category','التصنيف في الخريطة')"),
 # ---- key buyers
 ('data-en="Tenders of value or distinction" data-ar="منافسات ذات قيمة أو تميز">Tenders of value or distinction<', 'data-en="Tenders from key buyers ★" data-ar="منافسات من جهات مهمة ★">Tenders from key buyers ★<'),
 ('data-en="Priority = the agency is Tier 1 or Government on the stakeholder map, an EH client, a regulator, or a giga-project / PIF entity." data-ar="الأولوية = الجهة من الفئة الأولى أو حكومية في الخريطة، أو عميل لآفاق، أو جهة تنظيمية، أو مشروع كبير / جهة تابعة لصندوق الاستثمارات العامة.">Priority definition<',
  'data-en="A key buyer is Tier 1 or a government body on the stakeholder map, an EH client, a regulator, or a giga-project or company owned by the Public Investment Fund (PIF)." data-ar="الجهة المهمة هي جهة من الفئة الأولى أو جهة حكومية في الخريطة، أو عميل لآفاق، أو جهة تنظيمية، أو مشروع كبير أو شركة مملوكة لصندوق الاستثمارات العامة.">A key buyer is Tier 1 or a government body on the stakeholder map, an EH client, a regulator, or a PIF company.<'),
 ('data-en="Open Priority tenders" data-ar="منافسات الأولوية المفتوحة">Open Priority tenders<', 'data-en="Open now" data-ar="مفتوحة الآن">Open now<'),
 ('data-en="Past Priority tenders and their outcome" data-ar="منافسات الأولوية السابقة ونتيجتها">Past Priority tenders and their outcome<', 'data-en="Closed, and how they ended" data-ar="مغلقة، وكيف انتهت">Closed, and how they ended<'),
 ("L('Outcome on Etimad','النتيجة في اعتماد')", "L('Result on Etimad','النتيجة في اعتماد')"),
 ("L('Not captured yet','لم تُلتقط بعد')", "L('Not read yet','لم تُقرأ بعد')"),
 # ---- not yet clients, winners, footer
 ('data-en="Stakeholder view" data-ar="منظور أصحاب المصلحة">Stakeholder view<', 'data-en="Buyers who are not EH clients yet" data-ar="جهات ليست من عملاء آفاق بعد">Buyers who are not EH clients yet<'),
 ('data-en="Agencies that issue relevant tenders but are not EH clients — where EH could grow. Agencies not on the map are listed for review and are never added automatically." data-ar="جهات تطرح منافسات ذات صلة وليست من عملاء آفاق — مجالات نمو محتملة. الجهات غير الموجودة في الخريطة تُعرض للمراجعة ولا تُضاف تلقائيًا.">Whitespace<',
  'data-en="Buyers that publish tenders EH can bid for but are not EH clients yet: room to grow. Buyers missing from the stakeholder map are listed for review and are never added automatically." data-ar="جهات تطرح منافسات يمكن لآفاق التقدم لها وليست من عملائها بعد: مجال للنمو. الجهات غير الموجودة في خريطة أصحاب المصلحة تُعرض للمراجعة ولا تُضاف تلقائيًا.">Buyers that publish tenders EH can bid for but are not EH clients yet.<'),
 ("L('On the map as','في الخريطة بوصفها')", "L('On the stakeholder map as','في خريطة أصحاب المصلحة بوصفها')"),
 ("L('Not on the map — candidate to add after review','غير موجودة في الخريطة — مرشحة للإضافة بعد المراجعة')", "L('Not on the stakeholder map — suggested for review','غير موجودة في خريطة أصحاب المصلحة — مقترحة للمراجعة')"),
 ("issued two or more relevant tenders in this view.','تم البحث، ولا توجد جهة من خارج عملاء آفاق طرحت منافستين أو أكثر ذات صلة في هذا العرض.')",
  "published two or more tenders EH can bid for in this view.','تم البحث، ولا توجد جهة من خارج عملاء آفاق طرحت منافستين أو أكثر يمكن لآفاق التقدم لها في هذا العرض.')"),
 ('data-en="Winners of awarded tenders" data-ar="الفائزون بالمنافسات المرساة">Winners of awarded tenders<', 'data-en="Who won finished tenders" data-ar="من فاز بالمنافسات المرساة">Who won finished tenders<'),
 ('These results are not captured yet, so no competitor is added from this tab; the competitor count stays the bid tracker\'s." data-ar="تعرض منصة اعتماد في صفحة كل منافسة مرساة جميع المتقدمين وأسعارهم والفائز. لم تُلتقط هذه النتائج بعد، لذا لا يُضاف أي منافس من هذه الصفحة، ويبقى عدد المنافسين كما في جدول المنافسات.">Not captured yet.<',
  'We do not read these results yet, so this tab adds no competitors; competitor counts still come from the bid tracker." data-ar="تعرض منصة اعتماد في صفحة كل منافسة مرساة جميع المتقدمين وأسعارهم والفائز. لا نقرأ هذه النتائج بعد، لذا لا تضيف هذه الصفحة أي منافس، وتبقى أعداد المنافسين من جدول المنافسات.">We do not read these results yet.<'),
 ('data-en="Built from the private EH Etimad data sheet. Relevance rules: EH service taxonomy (14 service lines). EH status comes from the bid tracker, which stays the reference whenever the two differ." data-ar="مبنية من ورقة بيانات اعتماد الخاصة بآفاق البيئة. قواعد الصلة: تصنيف خدمات آفاق (14 خط خدمة). حالة آفاق مأخوذة من جدول متابعة المنافسات، وهو المرجع عند أي اختلاف.">Built from the private EH Etimad data sheet.<',
  'data-en="Built from EH\'s private Etimad data sheet. Whether a tender fits EH is decided from EH\'s list of 14 services. EH status comes from the bid tracker, which wins whenever the two disagree." data-ar="مبنية من ورقة بيانات اعتماد الخاصة بآفاق البيئة. تُحدد ملاءمة المنافسة لآفاق من قائمة خدماتها الأربع عشرة. حالة آفاق مأخوذة من جدول متابعة المنافسات، وهو المرجع عند أي اختلاف.">Built from EH\'s private Etimad data sheet.<'),
 ("L('All service lines','كل خطوط الخدمة')", "L('All EH services','كل خدمات آفاق')"),
 ('data-ph-en="Search title, agency or reference" data-ph-ar="ابحث في العنوان أو الجهة أو الرقم المرجعي"', 'data-ph-en="Search by title, buyer or tender number" data-ph-ar="ابحث بالعنوان أو الجهة أو رقم المنافسة"'),
 ("['rel',L('EH can bid for (core + related)','يمكن لآفاق التقدم لها (أساسية + ذات صلة)')]", "['rel',L('EH can bid for','يمكن لآفاق التقدم لها')]"),
]
for old, new in PAIRS:
    R(old, new)

# ---- "Words used on this page" box, under the known-gap note
GLOSS_EN = [("Core service", "the tender asks for one of EH's 14 services."), ("Related", "the tender is close to EH's work (for example general waste or site services) but not a core service."),
    ("Key buyer ★", "Tier 1 or a government body on the stakeholder map, an EH client, a regulator, or a giga-project or PIF company."),
    ("Direct purchase", "a small, quick order placed without a full tender; often open for less than two weeks."), ("Public tender", "an open competition anyone qualified can bid for; usually open 14–30 days."),
    ("Price of tender documents", "what a bidder pays Etimad for the tender papers; a rough sign of size, never the contract value."),
    ("Stakeholder-map tier", "how important the buyer is to EH, as recorded on the stakeholder map (Tier 1 = most important)."),
    ("Bid tracker", "EH's own sheet of tenders studied and bid for (EH-WIN-02-F01)."), ("PIF", "the Public Investment Fund, which owns NEOM, Red Sea Global, ROSHN and many other companies."),
    ("Giga-project", "one of the very large Vision 2030 developments, such as NEOM, Qiddiya or Diriyah.")]
GLOSS_AR = [("خدمة أساسية", "تطلب المنافسة إحدى خدمات آفاق الأربع عشرة."), ("ذات صلة", "قريبة من عمل آفاق (مثل النفايات العامة أو خدمات المواقع) لكنها ليست خدمة أساسية."),
    ("جهة مهمة ★", "جهة من الفئة الأولى أو حكومية في خريطة أصحاب المصلحة، أو عميل لآفاق، أو جهة تنظيمية، أو مشروع كبير أو شركة للصندوق."),
    ("شراء مباشر", "طلب صغير وسريع دون منافسة كاملة؛ يبقى مفتوحًا غالبًا أقل من أسبوعين."), ("منافسة عامة", "منافسة مفتوحة لكل مؤهل؛ تبقى مفتوحة عادةً 14–30 يومًا."),
    ("ثمن وثائق المنافسة", "ما يدفعه المتقدم لاعتماد مقابل وثائق المنافسة؛ مؤشر تقريبي للحجم وليس قيمة العقد."),
    ("الفئة في الخريطة", "أهمية الجهة لآفاق كما هي مسجلة في خريطة أصحاب المصلحة (الفئة الأولى = الأهم)."),
    ("جدول المنافسات", "جدول آفاق للمنافسات التي درستها أو تقدمت لها (EH-WIN-02-F01)."), ("الصندوق", "صندوق الاستثمارات العامة، مالك نيوم والبحر الأحمر الدولية وروشن وشركات كثيرة أخرى."),
    ("مشروع كبير", "أحد مشاريع رؤية 2030 الضخمة مثل نيوم والقدية والدرعية.")]
gl_en = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in GLOSS_EN).replace('"', '&quot;')
gl_ar = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in GLOSS_AR).replace('"', '&quot;')
anchor = '<div class="klab" data-en="All government tenders on Etimad"'
box = ('<details class="gloss"><summary data-en="Words used on this page" data-ar="كلمات مستخدمة في هذه الصفحة">Words used on this page</summary>'
       f'<ul class="glist" data-html-en="{gl_en}" data-html-ar="{gl_ar}"></ul></details>\n')
rep('page', anchor, box + anchor, 'plain', 'glossary box')
rep('page', "  document.querySelectorAll('[data-ph-en]').forEach(e=>e.placeholder=L(e.dataset.phEn,e.dataset.phAr));\n",
    "  document.querySelectorAll('[data-ph-en]').forEach(e=>e.placeholder=L(e.dataset.phEn,e.dataset.phAr));\n"
    "  document.querySelectorAll('[data-html-en]').forEach(e=>e.innerHTML=L(e.dataset.htmlEn,e.dataset.htmlAr));\n", 'plain', 'glossary language switch')
rep('page', ".arrow.up{color:var(--green)}",
    ".gloss{font-size:12.5px;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:-6px 0 14px}.gloss summary{cursor:pointer;font-weight:700;color:var(--ink)}"
    ".glist{margin:8px 0 2px;padding-inline-start:18px;columns:2;column-gap:28px}.glist li{margin:0 0 5px;break-inside:avoid}@media(max-width:780px){.glist{columns:1}}\n.arrow.up{color:var(--green)}",
    'plain', 'glossary style')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['page'])
write_change_table(os.path.join(HERE, 'change_table_etimad_plain'), 'Government Tenders — plain-language pass')
print('patched build_etimad_page.py')
