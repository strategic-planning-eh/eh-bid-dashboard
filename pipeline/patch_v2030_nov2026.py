# -*- coding: utf-8 -*-
"""patch_v2030_nov2026.py — Vision 2030 Dashboard: November 2026 review pass (26 Aug → 8 Nov 2026).

Every one of the 31 project records gets a "Verified (Nov 2026)" review note (EN in PROJECTS, AR in AR_TXT).
Records with a development in the window get a fresh note; records with nothing new keep their earlier note
body behind an explicit "checked, no new development found" line — an absent result is stated, never implied.
Field changes (only where evidenced — see pipeline/analysis/v2030_findings_2026-11.md for sources):
  • NEOM Green Hydrogen Co.: construction complete, commissioning; investment $8.4bn → $8.5bn; completion "2027 (commissioning)"
  • King Salman Park: completion 2026 → "2026–27 (phased opening)"; investment $9.4bn → $13.3bn (SAR 50bn public realm)
  • Lucid AMP-2: completion 2026 → 2027; confidence High → Medium
  • Oxagon: confidence Medium → High · New Murabba: confidence High → Medium
Header/review stamps move to 08/11/2026 (EN + AR); the methodology box gains a November paragraph.

Run once:  python3 pipeline/patch_v2030_nov2026.py
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_files, write_change_table

P = os.path.join(HERE, '..', 'hub', 'vision2030_dashboard.html')
if 'Verified (Nov 2026)' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'v')

NOCHANGE_EN = 'Verified (Nov 2026): checked 26 Aug–8 Nov 2026 — no new development found; the earlier findings stand. '
NOCHANGE_AR = 'تحقّق (نوفمبر 2026): فُحص بين 26 أغسطس و8 نوفمبر 2026 ولم يُرصد تطور جديد؛ النتائج السابقة قائمة. '

# ---------------------------------------------------------------- fresh notes (EN, AR) for records with a development
NEW = {
 'NEOM': (
  "Verified (Nov 2026): Reuters reported on 4 Oct 2026 that the planned NEOM World Cup stadium inside The Line (about $2.5 billion) has been shelved indefinitely; NEOM did not comment. Trade press (MEED, 1 Oct) describes NEOM as recalibrating rather than retreating, with Oxagon now the flagship and money steered to assets that earn a return. The Ministry of Finance's 2027 pre-budget statement (30 Sep) cuts 2027 spending about 3% but pledges to keep \"priority projects\" on track. No new headline budget or official status for NEOM as a whole was published in the window. Earlier: PIF's 2026–30 strategy (Aug 2026) emphasises private capital and returns; NEOM budgets cut by up to 60% on some projects; total spend to early 2026 estimated at $40–60 billion against the $500 billion headline.",
  "تحقّق (نوفمبر 2026): أفادت رويترز في 4 أكتوبر 2026 بأن استاد نيوم المخطط لكأس العالم داخل ذا لاين (نحو 2.5 مليار دولار) جُمّد إلى أجل غير مسمى، ولم تعلّق نيوم. وتصف الصحافة المتخصصة (MEED، 1 أكتوبر) نيوم بأنها تعيد المعايرة لا تتراجع، وأن أوكساغون أصبح المشروع الرائد مع توجيه الأموال إلى الأصول ذات العائد. ويقلّص بيان الميزانية المبدئي لعام 2027 (30 سبتمبر) إنفاق 2027 نحو 3% مع التعهد بإبقاء «المشاريع ذات الأولوية» على مسارها. ولم تُنشر ميزانية جديدة أو حالة رسمية لنيوم ككل خلال الفترة. سابقاً: استراتيجية الصندوق 2026–2030 (أغسطس 2026) تركّز على رأس المال الخاص والعوائد؛ وخُفضت ميزانيات نيوم حتى 60% في بعض المشاريع؛ ويُقدَّر الإنفاق حتى مطلع 2026 بنحو 40–60 مليار دولار مقابل الرقم المعلن 500 مليار."),
 'The Line': (
  "Verified (Nov 2026): still on hold. Reuters (4 Oct 2026) reported that the elevated stadium planned inside The Line has been shelved indefinitely, with no completion date, and recalled the PIF governor's April 2026 statement that The Line is no longer a priority before 2030. Nothing points to a restart. Earlier: omitted from PIF's 2026–30 strategy; construction suspended Sept 2025; only about 2.4 km of 170 km built; resident target cut from 1.5 million to under 300,000.",
  "تحقّق (نوفمبر 2026): ما يزال متوقفاً. أفادت رويترز (4 أكتوبر 2026) بأن الاستاد المرتفع المخطط داخل ذا لاين جُمّد إلى أجل غير مسمى دون موعد إنجاز، واستذكرت تصريح محافظ الصندوق في أبريل 2026 بأن ذا لاين لم يعد أولوية قبل 2030. ولا شيء يشير إلى استئناف. سابقاً: استُبعد من استراتيجية الصندوق 2026–2030؛ عُلّق الإنشاء في سبتمبر 2025؛ لم يُبنَ سوى نحو 2.4 كم من 170 كم؛ وخُفض مستهدف السكان من 1.5 مليون إلى أقل من 300 ألف."),
 'Oxagon': (
  "Verified (Nov 2026): now NEOM's flagship, with several corroborated milestones. HUMAIN and DataVolt started building the first 100 MW of a 360 MW AI data-centre phase (reported 1 Sep 2026; service from 2028; $5 billion programme) and on 22 Oct signed Nebius as anchor customer for up to 50 MW from late 2027. NEOM tendered the concept design of a 400 km+ freight rail link from Port of NEOM to the national network (bids due 29 Oct) and an interim industrial wastewater plant of 35,000 m³/day (bids due 25 Oct; Veolia among the reported bidders). The Red Sea war has strengthened Oxagon's case as a gateway outside the Strait of Hormuz. Confidence raised to High.",
  "تحقّق (نوفمبر 2026): أصبح أوكساغون المشروع الرائد لنيوم، مع عدة إنجازات مؤكدة من أكثر من مصدر. بدأت هيومين وداتافولت بناء أول 100 ميغاواط من مرحلة مراكز بيانات ذكاء اصطناعي بقدرة 360 ميغاواط (أُفيد في 1 سبتمبر 2026؛ التشغيل من 2028؛ برنامج بقيمة 5 مليارات دولار)، ووقّعتا في 22 أكتوبر مع نيبيوس عميلاً رئيساً لما يصل إلى 50 ميغاواط من أواخر 2027. وطرحت نيوم تصميم خط شحن حديدي يتجاوز 400 كم من ميناء نيوم إلى الشبكة الوطنية (العطاءات حتى 29 أكتوبر) ومحطة مؤقتة لمعالجة مياه الصرف الصناعي بقدرة 35,000 م³/يوم (العطاءات حتى 25 أكتوبر؛ فيوليا من المتقدمين المذكورين). وعزّزت حرب البحر الأحمر مكانة أوكساغون بوصفه بوابة خارج مضيق هرمز. رُفعت درجة الثقة إلى عالية."),
 'NEOM Green Hydrogen Company': (
  "Verified (Nov 2026): construction is complete and the plant is in commissioning — confirmed by ACWA Power on its first-half results call (reported 14 Aug 2026) — with commercial operation targeted for 2027; trade press (MEED, 1 Oct) calls the $8.5 billion plant NEOM's most significant completion to date. Capacity unchanged: up to 600 tonnes of hydrogen a day shipped as about 1.2 million tonnes a year of green ammonia, all bought by Air Products for 30 years; powered by about 4 GW of solar and wind. Equal one-third stakes confirmed in Air Products' US stock-market filing (May 2023); $6.1 billion in project loans from 23 banks.",
  "تحقّق (نوفمبر 2026): اكتمل الإنشاء ودخلت المحطة مرحلة التشغيل التجريبي — أكدت ذلك أكوا باور في مؤتمر نتائج النصف الأول (أُفيد في 14 أغسطس 2026) — والتشغيل التجاري مستهدف في 2027؛ وتصف الصحافة المتخصصة (MEED، 1 أكتوبر) المحطة البالغة 8.5 مليارات دولار بأنها أهم ما أُنجز في نيوم حتى الآن. القدرة دون تغيير: حتى 600 طن هيدروجين يومياً تُشحن بوصفها نحو 1.2 مليون طن سنوياً من الأمونيا الخضراء تشتريها إير برودكتس كاملةً لثلاثين عاماً؛ وتعمل بنحو 4 غيغاواط من الطاقة الشمسية والرياح. الحصص المتساوية (الثلث لكل شريك) مؤكدة في إفصاح إير برودكتس لسوق الأسهم الأمريكية (مايو 2023)؛ وقروض المشروع 6.1 مليارات دولار من 23 بنكاً."),
 'NEOM Port (Oxagon Port)': (
  "Verified (Nov 2026): the automated container terminal has slipped again — NEOM's own site now says it launches \"from 2027 onwards\" (previously 2025, then 2026), while a spokesperson told AGBI the port would open by end-2026 with capacity ramping up in 2027. Today the port handles about 0.3% of Saudi imports, mostly vehicles and construction bulk. NEOM has tendered the design of a 400 km+ freight rail link to the national network (bids due 29 Oct 2026), the port's first rail connection; the 1.5 million container target for 2030 still stands in trade reporting. Earlier: about 68% complete (Nov 2025); first fully automated cranes in the Kingdom.",
  "تحقّق (نوفمبر 2026): تأخّرت محطة الحاويات المؤتمتة مجدداً — يذكر موقع نيوم الآن أنها تنطلق «من 2027 فصاعداً» (كان 2025 ثم 2026)، بينما قال متحدث لـAGBI إن الميناء سيفتح بنهاية 2026 مع رفع القدرة تدريجياً في 2027. يتعامل الميناء اليوم مع نحو 0.3% من واردات المملكة، معظمها مركبات ومواد بناء. وطرحت نيوم تصميم خط شحن حديدي يتجاوز 400 كم إلى الشبكة الوطنية (العطاءات حتى 29 أكتوبر 2026)، وهو أول ربط حديدي للميناء؛ وما يزال مستهدف 1.5 مليون حاوية بحلول 2030 قائماً في التقارير المتخصصة. سابقاً: نسبة الإنجاز نحو 68% (نوفمبر 2025)؛ أول رافعات مؤتمتة بالكامل في المملكة."),
 'Diriyah': (
  "Verified (Nov 2026): contracts awarded to date have reached about SAR 130 billion (around $35 billion), with some 74,000 workers on site daily — Diriyah's president at a MEED conference on 28 Sep 2026. The Ministry of Culture has moved into its new headquarters on site and the first homes are being handed over; assets will open gradually. A SAR 2 billion loan with Arab National Bank (17 Aug 2026) funds branded residences in Diriyah and Wadi Safar. On track for 2030 and Expo. Earlier: At-Turaif, Bujairi Terrace and the Bab Samhan hotel open; Diriyah Square under construction.",
  "تحقّق (نوفمبر 2026): بلغت العقود المُرساة حتى الآن نحو 130 مليار ريال (قرابة 35 مليار دولار)، مع نحو 74 ألف عامل في الموقع يومياً — وفق رئيس شركة الدرعية في مؤتمر MEED يوم 28 سبتمبر 2026. وانتقلت وزارة الثقافة إلى مقرها الجديد في الموقع، ويجري تسليم أول المساكن؛ وستُفتح الأصول تدريجياً. ويموّل قرض بقيمة 2 مليار ريال من البنك العربي الوطني (17 أغسطس 2026) مساكن ذات علامات تجارية في الدرعية ووادي صفار. على المسار نحو 2030 وإكسبو. سابقاً: حي الطريف ومطل البجيري وفندق باب سمحان مفتوحة، وساحة الدرعية قيد الإنشاء."),
 'Qiddiya': (
  "Verified (Nov 2026): procurement continues at Qiddiya City — a contract of roughly $500–600 million for the 5,100-seat e-games arena was reported awarded in Sep 2026, and a third infrastructure package for District 0 (17.4 km of roads, 1.4 km of bridges) was tendered with bids due 14 Oct. Separately, a single report (Semafor, 14 Oct 2026, no PIF comment) said PIF intends to drop the planned Qiddiya Coast stadium near Jeddah from the 2034 World Cup plan; this concerns the coastal offshoot, not Qiddiya City, where the Prince Mohammed bin Salman Stadium is reported to be proceeding. Earlier: Six Flags Qiddiya City opened 31 Dec 2025.",
  "تحقّق (نوفمبر 2026): تستمر الترسيات في مدينة القدية — أُفيد في سبتمبر 2026 بإرساء عقد يقارب 500–600 مليون دولار لصالة الألعاب الإلكترونية بسعة 5,100 مقعد، وطُرحت حزمة ثالثة للبنية التحتية في المنطقة صفر (17.4 كم من الطرق و1.4 كم من الجسور) بعطاءات حتى 14 أكتوبر. وعلى صعيد منفصل، ذكر تقرير منفرد (سيمافور، 14 أكتوبر 2026، دون تعليق من الصندوق) أن الصندوق يعتزم إسقاط استاد ساحل القدية المخطط قرب جدة من خطة كأس العالم 2034؛ ويتعلق ذلك بالامتداد الساحلي لا بمدينة القدية التي يُفاد بأن استاد الأمير محمد بن سلمان فيها يمضي قُدماً. سابقاً: افتُتحت سيكس فلاغز القدية في 31 ديسمبر 2025."),
 'Red Sea Global (The Red Sea & AMAALA)': (
  "Verified (Nov 2026): operations keep expanding despite the war at sea. Red Sea Global opened the 430-key Grand Hyatt on Shura Island on 31 Oct 2026, bringing The Red Sea to 12 operating resorts; a hospital opened in late September and more Shura Island hotels are due before year-end. Phase 1 is described as nearing completion. On 27 Sep the company launched a yacht network linking the AMAALA (119 berths) and Shura (159 berths) marinas from winter 2026; AMAALA's Rosewood opened in late August after Four Seasons in June. No war damage to RSG assets is reported, but the Houthi blockade on Saudi-linked shipping (from 20 Jul) and reduced Bab el-Mandeb traffic are a live exposure for a destination sold on sea access.",
  "تحقّق (نوفمبر 2026): يتواصل توسع العمليات رغم الحرب في البحر. افتتحت البحر الأحمر الدولية فندق غراند حياة بسعة 430 مفتاحاً في جزيرة شورى يوم 31 أكتوبر 2026، ليصل عدد المنتجعات العاملة في وجهة البحر الأحمر إلى 12؛ وافتُتح مستشفى في أواخر سبتمبر، ومن المقرر افتتاح مزيد من فنادق شورى قبل نهاية العام. وتوصف المرحلة الأولى بأنها تقارب الاكتمال. وفي 27 سبتمبر أطلقت الشركة شبكة يخوت تربط مرسى أمالا (119 مرسى) ومرسى شورى (159 مرسى) من شتاء 2026؛ وافتُتح روزوود أمالا في أواخر أغسطس بعد فور سيزونز في يونيو. لم تُسجَّل أضرار حرب على أصول الشركة، لكن الحصار الحوثي على السفن المرتبطة بالسعودية (منذ 20 يوليو) وتراجع حركة باب المندب يمثلان تعرضاً فعلياً لوجهة تُسوَّق على الوصول البحري."),
 'King Salman Park': (
  "Verified (Nov 2026): nothing has opened yet, but a phased soft opening is being prepared — the acting CEO told a MEED conference on 28 Sep 2026 that some landscaped areas could open immediately, with the plan going to the board that week and announcements due in the coming months. Phases 1–2 have 95% of contracts awarded and irrigation installed; phase 3 is being re-planned, with the golf course replaced to allow commercial use. The public realm is about SAR 50 billion ($13.3 billion), replacing the older $9.4 billion figure; a further SAR 150 billion of private assets is planned, about SAR 20 billion awarded. Completion shown as 2026–27 (phased). Ownership: Royal Commission for Riyadh City / King Salman Park Foundation (government, not PIF).",
  "تحقّق (نوفمبر 2026): لم يُفتح شيء بعد، لكن يجري الإعداد لافتتاح تدريجي مبدئي — قال الرئيس التنفيذي بالإنابة في مؤتمر MEED يوم 28 سبتمبر 2026 إن بعض المساحات المنسّقة يمكن فتحها فوراً، وأن الخطة تُعرض على مجلس الإدارة في ذلك الأسبوع مع إعلانات خلال الأشهر المقبلة. أُرسي 95% من عقود المرحلتين 1–2 ورُكّب الريّ؛ ويُعاد تخطيط المرحلة 3 مع الاستعاضة عن ملعب الغولف لإتاحة الاستخدام التجاري. يبلغ المجال العام نحو 50 مليار ريال (13.3 مليار دولار) بدلاً من الرقم السابق 9.4 مليارات دولار؛ ويُخطط لأصول خاصة إضافية بقيمة 150 مليار ريال أُرسي منها نحو 20 ملياراً. يُعرض الإنجاز الآن 2026–2027 (تدريجي). الملكية: الهيئة الملكية لمدينة الرياض / مؤسسة حديقة الملك سلمان (جهة حكومية، لا الصندوق)."),
 'New Murabba': (
  "Verified (Nov 2026): no confirmed new development found 26 Aug–8 Nov 2026, and the \"resumed\" status is now provisional. Bids for the Mukaab's main foundations were due 20 Oct 2026 but no award has been reported; a single report (Semafor, 14 Oct, no PIF comment) listed the New Murabba stadium among five 2034 World Cup venues PIF intends to drop; and Reuters (4 Oct) again referred to its January report that Mukaab construction was suspended pending a financing review. Confidence lowered to Medium until an award is published. Earlier: foundation works resumed in Aug 2026 with excavation about 86% done; district phased to 2040.",
  "تحقّق (نوفمبر 2026): لم يُرصد تطور جديد مؤكد بين 26 أغسطس و8 نوفمبر 2026، وأصبحت حالة «الاستئناف» مؤقتة. كان موعد عطاءات الأساسات الرئيسة للمكعب 20 أكتوبر 2026 ولم يُفاد بأي ترسية؛ وأدرج تقرير منفرد (سيمافور، 14 أكتوبر، دون تعليق من الصندوق) استاد المربع الجديد بين خمسة ملاعب لكأس العالم 2034 يعتزم الصندوق إسقاطها؛ وأشارت رويترز (4 أكتوبر) مجدداً إلى تقريرها في يناير بأن إنشاء المكعب عُلّق بانتظار مراجعة التمويل. خُفضت درجة الثقة إلى متوسطة حتى نشر الترسية. سابقاً: استُؤنفت أعمال الأساسات في أغسطس 2026 مع إنجاز الحفر بنحو 86%؛ والحي مرحليٌّ حتى 2040."),
 'ROSHN': (
  "Verified (Nov 2026): ROSHN opened remote sales to eligible non-Saudi buyers in three zones under the new foreign-ownership rules, reporting thousands of registrations (company release, 22 Sep 2026); SEDRA has delivered more than 3,000 homes, with ALAROUS (Jeddah) and ALMANAR (Makkah) next. A single report (Semafor, 14 Oct) listed the ROSHN stadium in Riyadh among 2034 World Cup venues PIF may drop; no company statement. No financing or leadership change found. Earlier: SEDRA delivered early — the first giga-project to hand homes to customers; target 400,000 homes.",
  "تحقّق (نوفمبر 2026): فتحت روشن البيع عن بُعد للمشترين غير السعوديين المؤهلين في ثلاث مناطق بموجب قواعد التملك الأجنبي الجديدة، وأفادت بآلاف التسجيلات (بيان الشركة، 22 سبتمبر 2026)؛ وسلّمت سدرة أكثر من 3,000 مسكن، ويلي ذلك العروس (جدة) والمنار (مكة المكرمة). وأدرج تقرير منفرد (سيمافور، 14 أكتوبر) استاد روشن في الرياض بين ملاعب كأس العالم 2034 التي قد يسقطها الصندوق؛ دون بيان من الشركة. ولم يُرصد تغيير في التمويل أو القيادة. سابقاً: سُلّمت سدرة قبل موعدها — أول مشروع كبير يسلّم منازل للعملاء؛ والمستهدف 400 ألف مسكن."),
 'SABIC': (
  "Verified (Nov 2026): back in profit. Third-quarter results (25 Oct 2026): revenue SAR 28.2 billion (+14% on the previous quarter) and adjusted net income SAR 840 million, against a SAR 380 million loss in the second quarter; the transformation programme has delivered SAR 3.56 billion of a SAR 11.3 billion recurring-earnings target by 2030. Portfolio moves: the $450 million sale of the engineering-thermoplastics business completed; SABIC Agri-Nutrients took the final investment decision on a new 1.2 million t/yr ammonia and 2.6 million t/yr urea complex (reversing the early-2026 pull-back); feedstock allocated for a 1.8 million t/yr methanol plant in Jubail. Aramco's 70% stake unchanged.",
  "تحقّق (نوفمبر 2026): عادت إلى الربحية. نتائج الربع الثالث (25 أكتوبر 2026): إيرادات 28.2 مليار ريال (+14% عن الربع السابق) وصافي دخل معدَّل 840 مليون ريال مقابل خسارة 380 مليوناً في الربع الثاني؛ وحقّق برنامج التحول 3.56 مليارات ريال من مستهدف 11.3 مليار ريال من الأرباح المتكررة بحلول 2030. تحركات المحفظة: أُنجز بيع أعمال اللدائن الهندسية بقيمة 450 مليون دولار؛ واتخذت سابك للمغذيات الزراعية قرار الاستثمار النهائي لمجمع جديد ينتج 1.2 مليون طن أمونيا و2.6 مليون طن يوريا سنوياً (عكس التراجع في مطلع 2026)؛ وخُصص لقيم لمصنع ميثانول بقدرة 1.8 مليون طن سنوياً في الجبيل. حصة أرامكو 70% دون تغيير."),
 'Saudi Aramco Jafurah Gas Field': (
  "Verified (Nov 2026): Aramco's third-quarter results (3 Nov 2026) list Jafurah phase two as on track for 2027, alongside the Fadhili expansion; adjusted net income $31.2 billion, base dividend $21.9 billion. The CEO cited attacks on key energy facilities and said Aramco is exploring new export routes and overseas storage; the East–West pipeline, hit by a drone on 10 Sep, \"continued to provide export flexibility\". No change to the 2 billion cubic feet a day target by 2030. Earlier: phase 1 producing since Dec 2025 at 450 million cubic feet a day.",
  "تحقّق (نوفمبر 2026): تُدرج نتائج أرامكو للربع الثالث (3 نوفمبر 2026) المرحلة الثانية من الجافورة على المسار نحو 2027، إلى جانب توسعة الفاضلي؛ صافي الدخل المعدَّل 31.2 مليار دولار والتوزيعات الأساسية 21.9 مليار دولار. وأشار الرئيس التنفيذي إلى هجمات على منشآت طاقة رئيسة وقال إن أرامكو تدرس مسارات تصدير جديدة وتخزيناً خارجياً؛ وظل خط الأنابيب شرق–غرب، الذي أصابته طائرة مسيّرة في 10 سبتمبر، «يوفر مرونة للتصدير». لا تغيير في مستهدف 2 مليار قدم مكعبة يومياً بحلول 2030. سابقاً: تنتج المرحلة الأولى منذ ديسمبر 2025 بمعدل 450 مليون قدم مكعبة يومياً."),
 'King Salman Energy Park (SPARK)': (
  "Verified (Nov 2026): SPARK signed a 25-year lease with China's Dalipal Holdings on 14 Oct 2026 for a $2.1 billion energy-equipment manufacturing base (first phase about $600 million, 1.03 million m²) making seamless oil, gas and hydrogen pipes — one of the largest single tenant commitments to date. No updated factory count was published in the window. Earlier: 7 factories operating and 14 under construction (2025); phase 1 complete 2021.",
  "تحقّق (نوفمبر 2026): وقّعت سبارك في 14 أكتوبر 2026 عقد إيجار لمدة 25 عاماً مع شركة داليبال الصينية لقاعدة تصنيع معدات طاقة بقيمة 2.1 مليار دولار (المرحلة الأولى نحو 600 مليون دولار على 1.03 مليون م²) لإنتاج أنابيب غير ملحومة للنفط والغاز والهيدروجين — من أكبر التزامات المستأجرين المنفردة حتى الآن. ولم يُنشر عدد محدَّث للمصانع خلال الفترة. سابقاً: 7 مصانع عاملة و14 قيد الإنشاء (2025)؛ واكتملت المرحلة الأولى في 2021."),
 'International Maritime Industries (IMI)': (
  "Verified (Nov 2026): IMI and founding shareholder Lamprell signed an offshore fabrication agreement on 8 Oct 2026 under which the Ras Al-Khair yard will build a production platform and jackets for a Lamprell project — the first time the yard fabricates such structures, described by the CEO as a step beyond shipbuilding. Value and timeline undisclosed; shareholding unchanged (Aramco 50.1%, Lamprell 20%, Bahri 19.9%, Hyundai Heavy 10%).",
  "تحقّق (نوفمبر 2026): وقّعت IMI والمساهم المؤسس لامبريل في 8 أكتوبر 2026 اتفاقية تصنيع بحري يبني بموجبها حوض رأس الخير منصة إنتاج وقواعد (جاكيتات) لمشروع تابع للامبريل — وهي المرة الأولى التي يصنّع فيها الحوض مثل هذه الهياكل، ووصفها الرئيس التنفيذي بخطوة تتجاوز بناء السفن. القيمة والجدول الزمني غير معلنَين؛ والمساهمة دون تغيير (أرامكو 50.1%، لامبريل 20%، البحري 19.9%، هيونداي للصناعات الثقيلة 10%)."),
 'King Abdullah Port': (
  "Verified (Nov 2026): no port-specific statement or volume release found 26 Aug–8 Nov 2026, but the exposure is now direct: the Houthis declared a blockade on Saudi-linked shipping on 20 Jul 2026, struck a cargo ship in August, and Bab el-Mandeb traffic more than halved in September; most container lines still divert round Africa, so a transshipment-dependent port is the most exposed in the Kingdom. Offsetting this, the pre-budget statement reports the Red Sea ports' share of non-oil exports rose from 19% to 41% during the Hormuz crisis. No physical damage reported. Earlier: the Kingdom's first fully privately owned and operated commercial port; 2.93 million containers in 2023.",
  "تحقّق (نوفمبر 2026): لم يُرصد بيان خاص بالميناء أو إعلان أحجام بين 26 أغسطس و8 نوفمبر 2026، لكن التعرض أصبح مباشراً: أعلن الحوثيون حصاراً على السفن المرتبطة بالسعودية في 20 يوليو 2026، وضربوا سفينة شحن في أغسطس، وتراجعت حركة باب المندب إلى أقل من النصف في سبتمبر؛ وما تزال معظم خطوط الحاويات تلتف حول أفريقيا، ما يجعل ميناءً يعتمد على إعادة الشحن الأكثر تعرضاً في المملكة. وفي المقابل، يذكر بيان الميزانية المبدئي أن حصة موانئ البحر الأحمر من الصادرات غير النفطية ارتفعت من 19% إلى 41% خلال أزمة هرمز. ولم تُسجَّل أضرار مادية. سابقاً: أول ميناء تجاري في المملكة مملوك ومُشغَّل بالكامل من القطاع الخاص؛ 2.93 مليون حاوية في 2023."),
 'Ceer': (
  "Verified (Nov 2026): the Crown Prince launched Ceer's first two vehicles — the Exobot electric sedan and SUV (up to 670 km range) — on 21 Sep 2026 (PIF release). Both are to be built at the KAEC plant; Ceer still targets production start in October–December 2026 and first Saudi deliveries before year-end, with seven models planned by 2030. Headcount about 2,300 (80% Saudi). No confirmation of production start had been published by 8 Nov 2026 — the status moves to Partially Operational only when it is. Earlier: $1.3 billion plant, 240,000 m², at KAEC.",
  "تحقّق (نوفمبر 2026): أطلق ولي العهد أول مركبتَين لشركة سير — سيدان ودفع رباعي كهربائيتان باسم إكزوبوت (مدى يصل إلى 670 كم) — في 21 سبتمبر 2026 (بيان الصندوق). ستُصنَّع كلتاهما في مصنع مدينة الملك عبدالله الاقتصادية؛ وما تزال سير تستهدف بدء الإنتاج في أكتوبر–ديسمبر 2026 وأول تسليمات في السعودية قبل نهاية العام، مع سبعة طرازات مخططة بحلول 2030. عدد الموظفين نحو 2,300 (80% سعوديون). ولم يُنشر تأكيد لبدء الإنتاج حتى 8 نوفمبر 2026 — ولا تنتقل الحالة إلى «يعمل جزئياً» إلا عند تأكيده. سابقاً: مصنع بقيمة 1.3 مليار دولار على 240,000 م² في المدينة الاقتصادية."),
 'Lucid Manufacturing (AMP-2, KAEC)': (
  "Verified (Nov 2026): no new AMP-2 development found 26 Aug–8 Nov 2026, but the most recent reporting (July 2026, single trade source) is material: the new CEO cut about 18% of staff on top of an earlier 12%, suspended full-year guidance, and management said AMP-2 will not meaningfully contribute to 2026 volumes; PIF injected a further $750 million in June 2026 (over $9 billion since 2018). AMP-2 is still slated to launch the sub-$50,000 Cosmos ahead of Arizona, and the Saudi government order stands at up to 100,000 vehicles. The 2026 date for the full 155,000-unit factory is no longer credible — shown as 2027, confidence Medium, pending Lucid's third-quarter filing. Naming: this is AMP-2; AMP-1 is Arizona.",
  "تحقّق (نوفمبر 2026): لم يُرصد تطور جديد في AMP-2 بين 26 أغسطس و8 نوفمبر 2026، لكن أحدث التقارير (يوليو 2026، مصدر متخصص منفرد) جوهرية: خفّض الرئيس التنفيذي الجديد نحو 18% من الموظفين فوق 12% سابقة، وعلّق توقعات العام الكامل، وقالت الإدارة إن AMP-2 لن يسهم إسهاماً ذا معنى في أحجام 2026؛ وضخّ الصندوق 750 مليون دولار إضافية في يونيو 2026 (أكثر من 9 مليارات دولار منذ 2018). وما يزال مقرراً أن يطلق AMP-2 طراز كوزموس (دون 50 ألف دولار) قبل أريزونا، ويظل طلب الحكومة السعودية قائماً حتى 100 ألف مركبة. لم يعد موعد 2026 للمصنع الكامل بقدرة 155 ألف وحدة قابلاً للتصديق — يُعرض 2027 بثقة متوسطة بانتظار إفصاح لوسيد للربع الثالث. التسمية: هذا مصنع AMP-2، أما AMP-1 فهو في أريزونا."),
 'King Abdullah Economic City (KAEC)': (
  None,  # no-change prefix + earlier body + one line
  None),
}
# one-line additions for "no new development" records where the window still produced relevant context
ADD = {
 'King Abdullah Economic City (KAEC)': (
  " A single report (Semafor, 14 Oct 2026, no company statement) listed the KAEC stadium among five 2034 World Cup venues PIF may drop; Ceer's production start at KAEC (due Oct–Dec 2026) is the next milestone.",
  " وأدرج تقرير منفرد (سيمافور، 14 أكتوبر 2026، دون بيان من الشركة) استاد المدينة الاقتصادية بين خمسة ملاعب لكأس العالم 2034 قد يسقطها الصندوق؛ وبدء إنتاج سير في المدينة (المقرر في أكتوبر–ديسمبر 2026) هو المحطة التالية."),
 'Jubail Industrial City II': (
  " Related: SABIC Agri-Nutrients' final investment decision on a new ammonia and urea complex and feedstock for a 1.8 million t/yr methanol plant in Jubail (SABIC results, 25 Oct 2026) add to the Jubail pipeline.",
  " وعلى صلة: قرار الاستثمار النهائي لسابك للمغذيات الزراعية لمجمع أمونيا ويوريا جديد، وتخصيص لقيم لمصنع ميثانول بقدرة 1.8 مليون طن سنوياً في الجبيل (نتائج سابك، 25 أكتوبر 2026) يضيفان إلى قائمة مشاريع الجبيل."),
 'Ma\'aden Mining Expansion': (
  " Latest confirmed (first-half results, Aug 2026): profit +13%, the $110 billion ten-year capital programme maintained despite Hormuz disruption and a sulphur shortage; Phosphate 3 phase one was described as on track for end-2026 — third-quarter results were not yet out by 8 Nov.",
  " أحدث المؤكد (نتائج النصف الأول، أغسطس 2026): الربح +13%، وبرنامج الإنفاق الرأسمالي البالغ 110 مليارات دولار لعشر سنوات مستمر رغم اضطراب هرمز ونقص الكبريت؛ ووُصفت المرحلة الأولى من الفوسفات 3 بأنها على المسار لنهاية 2026 — ولم تصدر نتائج الربع الثالث حتى 8 نوفمبر."),
 'Hyundai-PIF Vehicle Plant (HMMME)': (
  " The last official position (Oct 2025) remains a start-up in October–December 2026; no start-of-production announcement by 8 Nov 2026 — if none arrives by December, completion slips to 2027 at the next review.",
  " يبقى الموقف الرسمي الأخير (أكتوبر 2025) بدء التشغيل في أكتوبر–ديسمبر 2026؛ ولم يصدر إعلان بدء إنتاج حتى 8 نوفمبر 2026 — وإن لم يصدر بحلول ديسمبر يُؤجَّل الإنجاز إلى 2027 في المراجعة التالية."),
 'Special Integrated Logistics Zone (SILZ)': (
  " The Lenovo/Alat plant was due to start production in 2026 but no opening had been announced by 8 Nov 2026.",
  " كان مقرراً أن يبدأ مصنع لينوفو/علاط الإنتاج في 2026، لكن لم يُعلن افتتاحه حتى 8 نوفمبر 2026."),
 'Saudi Water Authority (SWA) Desalination': (
  " Context: national desalination capacity passed 16 million m³/day at end-2025 (a figure that includes private plants), and trade press flags a sharp slowdown in water-sector contract awards in 2026.",
  " للسياق: تجاوزت قدرة التحلية الوطنية 16 مليون م³/يوم بنهاية 2025 (رقم يشمل المحطات الخاصة)، وتشير الصحافة المتخصصة إلى تباطؤ حاد في ترسيات قطاع المياه في 2026."),
}

# ---------------------------------------------------------------- helpers
def _js_str(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

def en_note_of(name):
    m = re.search(r'\{name:"' + re.escape(name) + r'",.*?note:"((?:[^"\\]|\\.)*)"', FILES['v'], re.S)
    return m.group(1) if m else None

def ar_block_note(name):
    m = re.search(r'"' + re.escape(name) + r'": \{.*?"note": "((?:[^"\\]|\\.)*)"', FILES['v'], re.S)
    return m.group(1) if m else None

def strip_prefix_en(t):  return re.sub(r'^Verified \((?:Jun|Aug) 2026\):\s*', '', t)
def strip_prefix_ar(t):  return re.sub(r'^تحقّق \((?:يونيو|أغسطس) 2026\):\s*', '', t)

names = re.findall(r'\{name:"((?:[^"\\]|\\.)*)",sectors', FILES['v'])
assert len(names) == 31, len(names)
for n in names:
    old_en, old_ar = en_note_of(n), ar_block_note(n)
    if old_en is None or old_ar is None:
        FAILURES.append({'file': 'v', 'note': 'note not found', 'old': n}); continue
    if n in NEW and NEW[n][0]:
        new_en, new_ar = NEW[n]
    else:
        new_en = NOCHANGE_EN + strip_prefix_en(old_en) + ADD.get(n, ('', ''))[0]
        new_ar = NOCHANGE_AR + strip_prefix_ar(old_ar) + ADD.get(n, ('', ''))[1]
    rep('v', 'note:"' + old_en + '"', 'note:"' + _js_str(new_en) + '"', 'review', f'EN note: {n}')
    rep('v', '"note": "' + old_ar + '"', '"note": "' + _js_str(new_ar) + '"', 'review', f'AR note: {n}')

# ---------------------------------------------------------------- field changes
rep('v', 'partners:[{n:"NEOM",s:33.3},{n:"ACWA Power",s:33.3},{n:"Air Products",s:33.3}],status:"Under Construction",completion:"2027",investment:8.4,',
    'partners:[{n:"NEOM",s:33.3},{n:"ACWA Power",s:33.3},{n:"Air Products",s:33.3}],status:"Under Construction",completion:"2027 (commissioning)",investment:8.5,',
    'field', 'NGHC: completion "2027 (commissioning)", investment $8.5bn')
rep('v', 'desc:"A US$8.4 billion green hydrogen facility at Oxagon',
    'desc:"A US$8.5 billion green hydrogen facility at Oxagon', 'field', 'NGHC: description figure')
rep_re('v', r'(desc:"A US\$8\.5 billion green hydrogen facility at Oxagon[^"]*?)Production now targeted for 2027\."',
       r'\1Construction complete and in commissioning (Aug 2026); production targeted for 2027."', 'field', 'NGHC: description status')
rep('v', 'partners:[{n:"Ajdan Real Estate",s:null},{n:"SEDCO Capital",s:null}],status:"Under Construction",completion:"2026",investment:9.4,',
    'partners:[{n:"Ajdan Real Estate",s:null},{n:"SEDCO Capital",s:null}],status:"Under Construction",completion:"2026–27 (phased opening)",investment:13.3,',
    'field', 'King Salman Park: completion phased, investment $13.3bn (SAR 50bn public realm)')
rep_re('v', r'(\{name:"Lucid Manufacturing \(AMP-2, KAEC\)",[^\n]*?completion:")2026(")', r'\g<1>2027\2', 'field', 'Lucid: completion 2027')
rep_re('v', r'(\{name:"Lucid Manufacturing \(AMP-2, KAEC\)",[^\n]*?confidence:")High(")', r'\1Medium\2', 'field', 'Lucid: confidence Medium')
rep_re('v', r'(\{name:"Oxagon",[^\n]*?confidence:")Medium(")', r'\1High\2', 'field', 'Oxagon: confidence High')
rep_re('v', r'(\{name:"New Murabba",[^\n]*?confidence:")High(")', r'\1Medium\2', 'field', 'New Murabba: confidence Medium')
rep('v', 'const AR_COMPLETION = {"2030+ (revised)": "بعد 2030 (معدَّل)", "Post-2030": "بعد 2030", "Ongoing": "مستمر"};',
    'const AR_COMPLETION = {"2030+ (revised)": "بعد 2030 (معدَّل)", "Post-2030": "بعد 2030", "Ongoing": "مستمر", "2027 (commissioning)": "2027 (تشغيل تجريبي)", "2026–27 (phased opening)": "2026–2027 (افتتاح تدريجي)"};',
    'field', 'AR completion labels for the two new values')

# ---------------------------------------------------------------- review stamps and methodology
rep('v', 'Data as of <strong>Aug 2026</strong><br>\n      Last reviewed <strong>26/08/2026</strong><br>',
    'Data as of <strong>Nov 2026</strong><br>\n      Last reviewed <strong>08/11/2026</strong><br>', 'stamp', 'EN header dates')
rep('v', 'const LAST_REVIEWED = "August 2026";', 'const LAST_REVIEWED = "November 2026";', 'stamp', 'LAST_REVIEWED')
rep('v', 'if(!m) return ar?"أغسطس 2026":LAST_REVIEWED;', 'if(!m) return ar?"نوفمبر 2026":LAST_REVIEWED;', 'stamp', 'AR fallback month')
rep('v', 'نتائج مراجعة مصادر 31 مشروعاً كبيراً &middot; آخر تحديث: 26/08/2026', 'نتائج مراجعة مصادر 31 مشروعاً كبيراً &middot; آخر تحديث: 08/11/2026', 'stamp', 'AR header date')
rep('v', '<strong>Full research verification — June 2026; update pass 26/08/2026.</strong>',
    '<strong>Update pass 08/11/2026.</strong> All 31 records were re-checked for developments between 26 August and 8 November 2026 (Reuters, MEED, AGBI, Argaam, company and PIF releases). What moved: NEOM Green Hydrogen finished construction and is commissioning ($8.5 billion, operations 2027); Oxagon\'s $5 billion AI data-centre campus broke ground and signed its anchor tenant, with a freight-rail link and a wastewater plant out to tender; Red Sea Global reached 12 operating resorts; Diriyah\'s awards passed SAR 130 billion; SABIC returned to profit; SPARK signed a $2.1 billion tenant; Aramco kept Jafurah phase two on track. On the other side, Reuters confirmed the NEOM stadium inside The Line is shelved indefinitely; a single uncorroborated report says five 2034 World Cup stadiums will be dropped (NEOM, KAEC, Qiddiya Coast, ROSHN, New Murabba); the Mukaab foundation award due in October has not surfaced; Lucid\'s KAEC plant will not add 2026 volume; NEOM\'s container terminal slipped to 2027. Twelve records had nothing new in the window and say so. Field changes: NGHC (status, $8.5 billion), King Salman Park (phased 2026–27, SAR 50 billion public realm), Lucid (2027, confidence Medium), Oxagon (confidence High), New Murabba (confidence Medium). The Red Sea war is now a live operating risk for King Abdullah Port, Port of NEOM and Red Sea Global.<br><br>\n    <strong>Full research verification — June 2026; update pass 26/08/2026.</strong>',
    'method', 'EN methodology: November paragraph')

if FAILURES:
    for f in FAILURES: print('FAIL', f['note'], f['old'][:120])
    sys.exit(1)
write_files(os.path.join(HERE, '..', 'hub'))
write_change_table(os.path.join(HERE, 'change_table_v2030_nov2026'), 'Vision 2030 Dashboard — November 2026 review')
print('applied')
