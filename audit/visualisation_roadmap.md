# EH Hub — Visualisation roadmap (Stage C)

**For:** EH senior management and Youssef · **Date:** 08 Sep 2026 · **Follows:** the visual audit (Stage A) and the first upgrade wave (Stage B)
Effort: **S** = under a day · **M** = 2–5 days · **L** = a week or more. Every item says what the reader gains, what data it needs and whether EH already has it.

---

## English

### Where we are after Stage B
The hub now behaves as one product: one header, one set of buttons that reach every page, one font, no page opening on zeros, numbers that count in once, charts that build in once and never re-animate, and a 12-pixel floor on text. Three things from the audit were deliberately **not** done in Stage B because they are content rebuilds rather than fixes, and they lead the "Now" list below.

### NOW — this month
| # | What | What the reader gains | Data needed | Have it? | Effort | Depends on | Risk |
|---|---|---|---|---|---|---|---|
| N1 | **Arabic editions of Fiscal Monitor and News Intelligence become real dashboards** — same cards and charts as English, Arabic labels | An Arabic reader gets the same product, not a text report | none new — the numbers are already on the page | Yes | M | shared layer (done) | Analyst prose stays; charts are added, nothing removed |
| N2 | **Full Arabic layer for the Client Bubble Map** (legend, toolbar, executive tab, tooltips) | The only English-only page joins the rest | none new | Yes | M | string-table pattern from the PIF pages | 60–80 strings; sector names need agreed Arabic |
| N3 | **One-sentence caption under every chart** on the PIF annual-reports page (14) and the Bubble Map executive tab (5) | The takeaway, not just the picture | none new | Yes | S–M | — | Captions must be re-checked when data refreshes |
| N4 | **Bid dashboard: 12 sub-tabs grouped into 4 menus** (Overview · Pipeline & Pricing · Competitors & Clients · Tenders & Notes) | Less to scan; a view is one step away | none | Yes | S | `pipeline/app.js` | Generator change — test on the hourly build |
| N5 | **Apply the hero-tile order to `pipeline/app.js`** so it survives the hourly rebuild | Win rate stays first after the next refresh | `pipeline/app.js` | Yes (repo) | S | — | Untested anchor; script stops safely if it does not match |
| N6 | **Weekly changelog entries** for the Stage B changes | "What's New" tells management what changed | seed file schema | Not seen yet | S | `changelog.seed.json` | — |

### NEXT — next quarter
| # | What | What the reader gains | Data needed | Have it? | Effort | Depends on | Risk |
|---|---|---|---|---|---|---|---|
| X1 | **"What changed this week" view** across all pages: every number that moved since last Monday, with a one-line reason | The Monday question answered in ten seconds | previous-value snapshot per number | Partly — `snapshot.json` covers bids only | L | weekly snapshot for every page | Needs a shared number registry (each figure gets an id) |
| X2 | **Bubble Map executive tab rebuilt as three questions** — "Who pays us most?", "Who is growing?", "Where is the gap?" — one chart each | Three answers instead of five analyst charts | client revenue by year, service mix | Yes (workbook) | M | N2 | Dropping familiar charts — agree first |
| X3 | **Client depth metrics**: net revenue retention, deal-size distribution, ranked whitespace shortlist | Which clients to grow, which sectors we are missing | revenue by client by year; service lines per client | Yes | M | X2 | "Retained" needs one definition |
| X4 | **Slope charts for period-to-period changes** (PIF 2021–25 → 2026–30; bids 2025 → 2026) | Direction of travel in one glance | none new | Yes | S | shared layer | — |
| X5 | **Drill-down from any KPI tile to its rows** (tap "182 tenders" → the 182 rows) | Trust: the number can be checked | row-level data already in the bid JSON; add for stakeholder counts | Mostly | M | shared pattern | Large tables in a frame — paginate |
| X6 | **Giga-project milestone tracker** (the audit found none exists) fed by AR23–AR26 statements | The "Big projects" table stops being a static reconciliation | annual-report milestone extraction each year | Partly (2023–25 by hand) | M | PIF AR 2026 | Manual unless a template is built |
| X7 | **Visual regression test in the workflow** — headless screenshots of every page, diffed on each build; build fails if a page goes blank | Nothing ships broken again | `render.py` from the audit | Yes | M | Actions minutes | Compare with motion off to avoid noise |
| X8 | **Lint step for untranslated strings and internal codes** in visible text ("D3", "AuM", "restated") | Plain language stays plain | list of banned tokens | Yes | S | X7 | — |
| X9 | **Versioned shared files with cache-busting** (`eh-shared.css?v=1.0.0`) | Fixes reach every device without hard refresh | none | Yes | S | — | README already notes the cache problem |

### LATER — 6 to 12 months
| # | What | What the reader gains | Data needed | Have it? | Effort | Depends on | Risk |
|---|---|---|---|---|---|---|---|
| L1 | **Map layer linking hazardous-waste generators to Al-Juhfah**: KAEC, Oxagon, Jubail/Yanbu, RSG sites as generators; distance and licensed route to our site | The commercial case for Al-Juhfah on one map | generator coordinates, waste categories, MWAN licence data | Partly (landfill GIS map: 371 facilities; generators not mapped) | L | MWAN data request; tender mining | Quality of generator waste categories |
| L2 | **Etimad/Furas tender feed into the bid dashboard** (upcoming environmental tenders, not only ours) | We see the market, not only our pipeline | exported tender lists | No | L | portal access and terms | Portal changes break exports |
| L3 | **MWAN licence register refresh on a schedule** into the stakeholder map | Competitor licences stay current; expiries flagged automatically | MWAN register export | Manual today | M | data-request outcome | — |
| L4 | **PIF Annual Report 2026 ingestion** into both PIF pages, with the ecosystem values PIF has promised to report | First quantified view of the six groups | AR 2026 (expected 2027 H1) | Not yet | M | publication | Format may change again |
| L5 | **Guided "read this page" mode** — on request, highlights one element at a time with its one-sentence explanation | A new manager learns a page in two minutes | captions from N3 | After N3 | M | motion layer | Must stay opt-in (moderate motion) |
| L6 | **Comparison mode** — two competitors, two years or two PIF plans side by side | "How does X compare to Y" without exporting | none new | Yes | M | X4 | — |
| L7 | **Board-pack print/PDF layout** for every page (A4 landscape, page breaks, no interactivity) | The hub goes into the board meeting | none | Yes | M | shared layer | Charts must render via headless print |
| L8 | **"Brief mode"** — toggle showing only each page's summary and hero numbers | The two-minute version of the whole hub | captions and hero flags | After N3/N4 | M | — | — |
| L9 | **Style guide page inside the hub** — shared patterns, colours, motion and plain-language rules | Anyone adding a page keeps it consistent | none | Yes | S | — | — |
| L10 | **Bundled EH brand typeface** once supplied (one variable in `eh-shared.css`) | Brand alignment | font files and licence | No | S | brand decision | ~200 KB per page unless subset |

### The three things to do first, and why
1. **N1 — Arabic dashboards for Fiscal and News.** The largest remaining inequality: half the audience gets a text report where the other half gets a dashboard, and the numbers are already on the page.
2. **N3 — captions under every chart.** Cheapest fix with the biggest effect on the ten-second test; it also unlocks L5 and L8.
3. **X7 — visual regression test.** Twice in one week a page shipped with something only a screenshot would have caught. Once this exists every later item is safer.

### Decisions needed before "Now" work starts
- N1: keep the Arabic analyst prose above the charts, or move it below?
- N2: agreed Arabic names for the 14 client sectors.
- N3: rule for captions when hourly data changes the picture ("captions describe the shape, not the number").
- N4: the four menu names for the bid sub-tabs.
- N6: send `changelog.seed.json` (or `notify_and_log.py`).
- X1: every number on every page gets a stable id — a one-off tagging pass.

---

## العربية

### أين نحن بعد المرحلة ب
تتصرف المنصة الآن كمنتج واحد: رأس واحد، أزرار واحدة تصل إلى كل صفحة، خط واحد، لا صفحة تُفتح على أصفار، أرقام تُعَدّ مرة واحدة، رسوم تُبنى مرة واحدة ولا تعيد الحركة، وحد أدنى 12 بكسل للنص. ثلاثة أمور من التدقيق لم تُنفَّذ عن قصد لأنها إعادة بناء للمحتوى لا إصلاحات، وهي تتصدر قائمة «الآن».

### الآن — هذا الشهر
| # | ماذا | ما يكسبه القارئ | البيانات | متوفرة؟ | الجهد |
|---|---|---|---|---|---|
| N1 | النسختان العربيتان لمرصد المالية والاستخبارات الإخبارية تصبحان لوحات حقيقية بالبطاقات والرسوم نفسها | القارئ العربي يحصل على المنتج نفسه لا تقريراً نصياً | لا جديد | نعم | M |
| N2 | طبقة عربية كاملة لخريطة العملاء | الصفحة الوحيدة بالإنجليزية فقط تلحق بالبقية | لا جديد | نعم | M |
| N3 | جملة واحدة تحت كل رسم في صفحة تقارير الصندوق (14) واللوحة التنفيذية لخريطة العملاء (5) | الخلاصة لا الصورة فقط | لا جديد | نعم | S–M |
| N4 | تجميع تبويبات المناقصات الاثني عشر في أربع قوائم | مسح أقل؛ العرض بخطوة واحدة | لا | نعم | S |
| N5 | تطبيق ترتيب البطاقات الرئيسية على `pipeline/app.js` ليبقى بعد إعادة البناء الساعية | تبقى «نسبة الفوز أولاً» بعد التحديث التالي | `app.js` | نعم | S |
| N6 | إدخال تغييرات المرحلة ب في سجل التغييرات الأسبوعي | «ما الجديد» يخبر الإدارة بما تغيّر | ملف البذرة | لم يُرَ بعد | S |

### التالي — الربع القادم
| # | ماذا | ما يكسبه القارئ | الجهد |
|---|---|---|---|
| X1 | عرض «ما الذي تغيّر هذا الأسبوع» عبر كل الصفحات مع سبب من سطر واحد | سؤال الاثنين مُجاب في عشر ثوانٍ | L |
| X2 | إعادة بناء اللوحة التنفيذية لخريطة العملاء كثلاثة أسئلة: من يدفع لنا أكثر؟ من ينمو؟ أين الفجوة؟ | ثلاث إجابات بدل خمسة رسوم تحليلية | M |
| X3 | مقاييس عمق العملاء: الاحتفاظ بالإيراد، توزيع أحجام الصفقات، قائمة الفرص غير المستغلة | أي عميل ننمّيه وأي قطاع نفتقده | M |
| X4 | رسوم الانحدار للتغيرات بين الفترات | اتجاه الحركة بلمحة واحدة | S |
| X5 | النزول من أي بطاقة مؤشر إلى صفوفها | ثقة: الرقم قابل للتحقق | M |
| X6 | متتبّع حقيقي لمعالم المشاريع الكبرى من التقارير السنوية | جدول «المشاريع الكبرى» يتوقف عن كونه مطابقة ثابتة | M |
| X7 | اختبار انحدار بصري في سير العمل: لقطات لكل صفحة تُقارَن مع كل بناء | لا يُنشر شيء مكسور مجدداً | M |
| X8 | فحص للنصوص غير المترجمة والرموز الداخلية | تبقى اللغة بسيطة | S |
| X9 | ملفات مشتركة مرقّمة بإصدار | تصل الإصلاحات إلى كل جهاز دون تحديث قسري | S |

### لاحقاً — 6 إلى 12 شهراً
| # | ماذا | ما يكسبه القارئ | الجهد |
|---|---|---|---|
| L1 | طبقة خريطة تربط مولّدي النفايات الخطرة (مدينة الملك عبدالله الاقتصادية، أوكساجون، الجبيل/ينبع، البحر الأحمر) بالجحفة | القضية التجارية للجحفة على خريطة واحدة | L |
| L2 | تغذية منافسات اعتماد/فرص في لوحة المناقصات | نرى السوق لا محفظتنا فقط | L |
| L3 | تحديث دوري لسجل تراخيص موان | تراخيص المنافسين محدّثة والانتهاءات مُعلَّمة آلياً | M |
| L4 | إدخال التقرير السنوي 2026 للصندوق | أول عرض كمي للمجموعات الست | M |
| L5 | وضع «اقرأ هذه الصفحة» الموجَّه عند الطلب | مدير جديد يتعلم صفحة في دقيقتَين | M |
| L6 | وضع المقارنة جنباً إلى جنب | إجابة «كيف يقارن س بـ ص» دون تصدير | M |
| L7 | تخطيط طباعة/PDF لحزمة مجلس الإدارة | المنصة تدخل اجتماع المجلس | M |
| L8 | «وضع الملخص» | نسخة الدقيقتَين من المنصة كلها | M |
| L9 | صفحة دليل الأسلوب داخل المنصة | كل من يضيف صفحة يحافظ على الاتساق | S |
| L10 | خط العلامة التجارية عند توفيره | مواءمة الهوية | S |

### الأمور الثلاثة الأولى ولماذا
1. **N1** — أكبر تفاوت متبقٍّ: نصف الجمهور يحصل على تقرير نصي والنصف الآخر على لوحة، والأرقام موجودة أصلاً.
2. **N3** — أرخص إصلاح بأكبر أثر على اختبار العشر ثوانٍ، ويفتح الباب لـL5 وL8.
3. **X7** — مرتَين في أسبوع نُشرت صفحة فيها خلل لا تكشفه سوى لقطة شاشة.

### قرارات مطلوبة قبل بدء أعمال «الآن»
- N1: النص التحليلي العربي فوق الرسوم أم تحتها؟
- N2: أسماء عربية متفق عليها لقطاعات العملاء الأربعة عشر.
- N3: قاعدة اعتماد الجُمَل عند تغيّر البيانات.
- N4: أسماء القوائم الأربع لتبويبات المناقصات.
- N6: إرسال `changelog.seed.json` أو `notify_and_log.py`.
- X1: منح كل رقم في كل صفحة معرّفاً ثابتاً.
