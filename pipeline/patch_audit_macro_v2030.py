"""patch_audit_macro_v2030.py — audit fixes for the Vision 2030 page (hub/vision2030_dashboard.html), 12 Oct 2026,
judge J3, ids macro-04, macro-06, macro-08, macro-19 (b, c) and macro-20.

What was wrong and what changes:
  • macro-04 — King Abdullah Port was described as "now the world's most efficient container port in the World Bank's
    ranking (2024)". In the World Bank's container port performance index for 2023 (published 2024) it ranked 30th.
    The card, table drawer and review note now say it was once ranked the most efficient and was 30th in the 2023
    index. (No other new claim is added.) EN and AR.
  • macro-06 — the Arabic tab ("تقرير التحقق") printed every project's description, review note, lead entity, partner
    names, completion value and investment unit in English. Each of the 31 projects now has an Arabic description,
    review note and lead entity (EH translations, formal Arabic); partner names, completion values ("Ongoing",
    "Post-2030", "2030+ (revised)") and "$…B" have Arabic forms. The tab label was ungrammatical ("التقرير التحقق") —
    now "تقرير التحقق"; the first tab reads "اللوحة الاستراتيجية (بالإنجليزية)" while the Arabic tab is open.
  • macro-08 — ownership doughnut in the project drawer: with a single disclosed stake (Lucid: PIF 60%; KAEC: PIF 55.5%)
    the ring was drawn full, as if PIF owned everything. When the disclosed stakes add up to less than 100%, the rest is
    now drawn as a grey "Other shareholders / public float" slice and listed under the chart. EN and AR.
  • macro-19 (b) — the status chips "Announced" and "Planning" and the confidence chip "Low" never matched a project;
    chips that match no project are no longer shown. (c) — the drawer showed "Last Reviewed: August 2026" for every
    project from one constant, while the methodology promises a per-project date; each drawer now shows the month in
    the project's own review note ("Verified (Jun 2026)" → June 2026), falling back to August 2026.
    (macro-19 (a), whether the investment total should include NEOM's sub-projects, is an owner decision — unchanged.)
  • macro-20 — keyboard: project cards and table rows can be reached with Tab and opened with Enter or Space; closed
    drawers are inert, so their hidden close buttons no longer take focus. Opening moves focus to the close button and
    closing returns it to the card.

Exact-string edits; stops if an anchor is missing.   Run once:  python3 pipeline/patch_audit_macro_v2030.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'vision2030_dashboard.html')
if 'AR_TXT' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'v')
R = lambda old, new, cat, note, count=1: rep('v', old, new, cat, note, count)

# ---------------------------------------------------------------- macro-04 King Abdullah Port (English)
R("Handled 2.93 million shipping containers in 2023. Ranked world's most efficient container port (World Bank port-efficiency ranking, 2024).",
  "Handled 2.93 million shipping containers in 2023. Once ranked the world's most efficient container port by the World Bank; 30th in the World Bank's container port performance index for 2023 (published 2024).",
  'copy', 'macro-04: KAP review note — 30th in the 2023 index, not "world\'s most efficient (2024)"')
R("desc:\"The Kingdom's first fully privately developed port — now the world's most efficient container port in the World Bank's ranking (2024). Phase 2 targets capacity of ~6 million containers a year.\"",
  "desc:\"The Kingdom's first fully privately developed port. The World Bank once ranked it the world's most efficient container port; in the 2023 index (published 2024) it ranked 30th. Phase 2 targets capacity of ~6 million containers a year.\"",
  'copy', 'macro-04: KAP description')

# ---------------------------------------------------------------- macro-06 Arabic project texts (EH translations)
V = 'تحقّق ({m} 2026): '
J, A = 'يونيو', 'أغسطس'
AR_TXT = {
 "NEOM": {"lead": "شركة نيوم",
  "desc": "المنطقة الرائدة لصندوق الاستثمارات العامة في منطقة تبوك، ويُعاد النظر فيها جذرياً: تتحول من مفهوم المدينة المستقبلية إلى البنية التحتية للذكاء الاصطناعي ومراكز البيانات والاستخدامات الصناعية، بعد تجاوز التكاليف والضغوط المالية.",
  "note": V.format(m=A) + "تركّز استراتيجية صندوق الاستثمارات العامة الجديدة للفترة 2026–2030 (أغسطس 2026) على رأس المال الخاص والعوائد؛ وخُفّضت ميزانيات نيوم بنسبة تصل إلى 60% في بعض المشاريع، ويُتوقع أن ينخفض إجمالي الإنفاق الرأسمالي للصندوق بنحو 15% في 2026. ويُقدَّر ما أُنفق على نيوم حتى مطلع 2026 بنحو 40–60 مليار دولار مقابل الرقم المعلن البالغ 500 مليار دولار. وسجّل الصندوق خسارة في القيمة بنحو 8 مليارات دولار على المشاريع الكبرى في تقريره السنوي لعام 2024، ولم تعد هذه المشاريع تمثل سوى 6% من إجمالي أصوله. ويجري التحول نحو الذكاء الاصطناعي ومراكز البيانات والاستخدام الصناعي."},
 "The Line": {"lead": "شركة نيوم",
  "desc": "صُمّمت في الأصل مدينةً ذكية خطية بطول 170 كم لتسعة ملايين نسمة. عُلّق الإنشاء في سبتمبر 2025 ولم يُنجز سوى نحو 2.4 كم، وتأجّل التسليم النهائي إلى ما بعد 2030 بكثير.",
  "note": V.format(m=A) + "استُبعدت كلياً من وثيقة استراتيجية صندوق الاستثمارات العامة 2026–2030 (أغسطس 2026). عُلّق الإنشاء في 16 سبتمبر 2025 وتوقف حتى ما بعد 2030 على الأقل (سيمافور، مايو 2026)؛ وخُفّضت القوى العاملة 35% منذ أبريل 2025 ونُقل أكثر من 1,000 موظف إلى الرياض. ولم يُنجز سوى نحو 2.4 كم من أصل 170 كم، وخُفّض المستهدف السكاني من 1.5 مليون إلى أقل من 300,000 نسمة."},
 "Oxagon": {"lead": "شركة نيوم / أوكساغون",
  "desc": "المجمّع الصناعي والمينائي العائم في نيوم، وقد أصبح العقدة ذات الأولوية في البرنامج مع التركيز على مراكز بيانات الذكاء الاصطناعي والتصنيع المتقدم والخدمات اللوجستية في البحر الأحمر. والعمليات المينائية جارية.",
  "note": V.format(m=A) + "تعهّدت نيوم بتخصيص 3 مليارات دولار لأوكساغون (يونيو 2026)، ويُتوقع أن يبدأ إنشاء حرم داتافولت لمراكز بيانات الذكاء الاصطناعي بقيمة 5 مليارات دولار خلال أشهر (أغسطس 2026). وتعزّز دوره الاستراتيجي مع اضطراب الملاحة في مضيق هرمز، إذ يُتوقع أن يؤسس لطرق تجارة جديدة عبر البحر الأحمر. وبُسّط التصميم من مفهوم المثمّن العائم الأصلي إلى منطقة صناعية ساحلية تقليدية. وبلغت نسبة إنجاز الميناء نحو 68%، ويستهدف طاقة استيعابية تبلغ 1.5 مليون حاوية سنوياً بحلول 2030."},
 "Trojena": {"lead": "شركة نيوم",
  "desc": "وجهة مخططة للسياحة الجبلية والتزلج ضمن نيوم. فقدت حق استضافة دورة الألعاب الآسيوية الشتوية 2029 (مُنحت لألماتي في فبراير 2026)، وتأجّلت إلى ما بعد 2030 بكثير.",
  "note": V.format(m=A) + "أنهت نيوم ثلاثة عقود رئيسة في تروجينا تتجاوز قيمتها 6 مليارات دولار في مارس 2026، وتروجينا مستبعدة من استراتيجية صندوق الاستثمارات العامة 2026–2030 (أغسطس 2026). وفقدت دورة الألعاب الآسيوية الشتوية 2029، إذ أجّلها المجلس الأولمبي الآسيوي في 24 يناير 2026 وسُمّيت ألماتي مستضيفةً في 2 فبراير 2026. والجدول الزمني الجديد غير واضح، وربما يكون نحو 2033."},
 "Sindalah Island": {"lead": "شركة نيوم / البحر الأحمر العالمية",
  "desc": "منتجع جزيرة في البحر الأحمر تابع لنيوم، افتُتح رسمياً في أكتوبر 2024 لكنه لا يعمل في معظمه. وتشير تجاوزات التكلفة (نحو ثلاثة أضعاف الميزانية) ونقل الإدارة إلى البحر الأحمر العالمية إلى صعوبات في التنفيذ.",
  "note": V.format(m=J) + "افتتاح رسمي في أكتوبر 2024، لكن المرسى والفنادق لم تُفتتح في معظمها؛ وتفيد التقارير بأن التكلفة بلغت نحو ثلاثة أضعاف التقدير الأولي (نحو 4 مليارات دولار). وتفيد التقارير كذلك بنقل الإدارة من نيوم إلى البحر الأحمر العالمية (فايننشال تايمز، سبتمبر 2025)، ويُقرأ ذلك مؤشراً على تراجع الثقة. ويُتوقع افتتاح فندق فور سيزونز نحو 2028."},
 "NEOM Green Hydrogen Company": {"lead": "شركة نيوم للهيدروجين الأخضر",
  "desc": "منشأة للهيدروجين الأخضر بقيمة 8.4 مليارات دولار في أوكساغون، على نطاق عالمي، مملوكة بالتساوي لنيوم وأكوا باور وإير برودكتس، والتزمت إير برودكتس بشراء كامل الإنتاج لمدة 30 عاماً. والإنتاج مستهدف الآن في 2027.",
  "note": V.format(m=A) + "تأخّر مستهدف الإنتاج إلى 2027 (بدلاً من نهاية 2026) وفق تقارير منتصف 2026، ويظل أكثر مكونات نيوم تقدماً. وتأكدت الحصص المتساوية (الثلث لكل شريك) في إفصاح إير برودكتس الرسمي لدى هيئة الأوراق المالية الأمريكية (مايو 2023)؛ وحصل المشروع على قروض بقيمة 6.1 مليارات دولار من 23 مصرفاً؛ ووافقت إير برودكتس على شراء كامل الإنتاج لمدة 30 عاماً (نحو 600 طن من الهيدروجين يومياً، يُشحن على هيئة أمونيا خضراء)."},
 "NEOM Port (Oxagon Port)": {"lead": "ميناء نيوم / أوكساغون",
  "desc": "ميناء مؤتمت في المياه العميقة بأوكساغون، وهو الأول في المملكة برافعات مؤتمتة بالكامل يُتحكم بها عن بُعد، ويستهدف طاقة استيعابية تبلغ 1.5 مليون حاوية سنوياً بحلول 2030.",
  "note": V.format(m=J) + "نسبة الإنجاز نحو 68% (نوفمبر 2025)، ويستهدف محطة حاويات مؤتمتة بالكامل بحلول 2026. وفيه أول رافعات مؤتمتة بالكامل يُتحكم بها عن بُعد في المملكة. ويستهدف طاقة استيعابية تبلغ 1.5 مليون حاوية سنوياً بحلول 2030. وتكلفة المرحلة الأولى نحو 7.5 مليارات ريال (نحو 2 مليار دولار)."},
 "Diriyah": {"lead": "شركة الدرعية",
  "desc": "حيّ للثقافة ونمط الحياة حول موقع الطريف المسجّل في قائمة اليونسكو قرب الرياض، وهو من أفضل مشاريع رؤية 2030 الرائدة تقدماً، وقد افتُتحت فيه عدة مرافق، ويُقدَّر البرنامج بنحو 63 مليار دولار.",
  "note": V.format(m=J) + "من أفضل المشاريع الكبرى تقدماً. حي الطريف ومطل البجيري وفندق باب سمحان مفتوحة، وساحة الدرعية قيد الإنشاء. وتأخّر الإنجاز من 2027 إلى 2030. وتقدّر شركة الاستشارات العقارية نايت فرانك البرنامج الكامل بـ63 مليار دولار، منها نحو 14.5 مليار دولار متعاقد عليها فعلياً حتى الآن. وتجاوزت العقود المرساة منذ بدء المشروع 100 مليار ريال (نحو 27 مليار دولار)."},
 "Qiddiya": {"lead": "شركة القدية للاستثمار",
  "desc": "مدينة للترفيه والرياضة والثقافة جنوب غرب الرياض. افتُتحت مدينة سيكس فلاغز القدية في ديسمبر 2025، إيذاناً ببدء افتتاح مرحلي لنحو 70 منشأة، منها ملعب كأس العالم 2034.",
  "note": V.format(m=J) + "افتُتحت مدينة سيكس فلاغز القدية (وفيها أسرع قطار أفعواني وأطوله في العالم، «فالكونز فلايت») في 31 ديسمبر 2025، وهي الأولى من نحو 70 منشأة مخططة. ولا يزال استاد الأمير محمد بن سلمان (أحد ملاعب كأس العالم 2034) ومركز الفنون الأدائية وحلبة السرعة قيد الإنشاء. ويُقدَّر البرنامج بنحو 40 مليار دولار."},
 "Red Sea Global (The Red Sea & AMAALA)": {"lead": "البحر الأحمر العالمية",
  "desc": "وجهة سياحية فاخرة على الساحل الغربي للمملكة. تعمل وجهة البحر الأحمر منذ 2023، وأعلنت أمالا (مكوّن العافية فائق الفخامة) افتتاحها في نوفمبر 2025.",
  "note": V.format(m=J) + "تستقبل وجهة البحر الأحمر الضيوف منذ 2023 (نحو 9 فنادق)، وافتُتح منتجع ثول الخاص في 2024، وأُعلن افتتاح «الخلجان الثلاثة» في أمالا في نوفمبر 2025 (نحو 13.6 مليار دولار مستثمرة في المرحلة الأولى، وتأمين تمويل جديد بقيمة 1.73 مليار دولار في أكتوبر 2025). وأُعيد تصنيفها ضمن السياحة والترفيه فقط، فالتوجه التجديدي سمة للمشروع لا قطاع."},
 "King Salman Park": {"lead": "مؤسسة حديقة الملك سلمان",
  "desc": "أكبر حديقة حضرية في العالم (16.6 كم²) في الرياض، تحت مظلة الهيئة الملكية لمدينة الرياض. مشروع حكومي (لا يتبع صندوق الاستثمارات العامة)، والمرحلة الأولى مستهدفة في 2026.",
  "note": V.format(m=J) + "تصحيح الملكية: تتبع الهيئة الملكية لمدينة الرياض / مؤسسة حديقة الملك سلمان (جهة حكومية، لا صندوق الاستثمارات العامة). وافتتاح المرحلة الأولى مستهدف في 2026 (بعد أن كان مقرراً في 2025). وأُسس صندوق استثمار خاص بقيمة 3.8 مليارات ريال (نحو مليار دولار) في نوفمبر 2025 مع أجدان العقارية وسدكو كابيتال. وستكون أكبر حديقة حضرية في العالم (16.6 كم²)."},
 "New Murabba": {"lead": "شركة تطوير المربع الجديد",
  "desc": "وسط مدينة جديد للرياض يتمحور حول مبنى المكعب. بعد توقف في يناير 2026 استُؤنفت أعمال أساسات المكعب بحلول أغسطس 2026، ويُسلَّم الحي على مراحل حتى 2040، والمرحلة الأولى مستهدفة لإكسبو 2030.",
  "note": V.format(m=A) + "استُؤنفت أعمال المكعب: أعمال الأساسات جارية (شركة HSSG لمقاولات الأساسات) ونسبة الحفر نحو 86% (أُزيل أكثر من 10 ملايين متر مكعب من التربة)، وموعد تقديم العطاءات للأساسات الخرسانية الرئيسة 20 أكتوبر 2026 (ميد، 20 أغسطس 2026). ويأتي ذلك بعد التعليق الذي أوردته رويترز في يناير 2026 بانتظار مراجعة التمويل. ويُنفَّذ الحي على مراحل حتى 2040: المرحلة الأولى بحلول 2030 لإكسبو، ومراحل لاحقة مرتبطة بكأس العالم 2034، ثم 2035 و2040."},
 "ROSHN": {"lead": "مجموعة روشن",
  "desc": "المطوّر الوطني للمجتمعات السكنية التابع لصندوق الاستثمارات العامة. سُلّم مشروع سدرة في الرياض قبل موعده، ما جعل روشن من المشاريع الكبرى القليلة التي حققت إنجازاً رئيساً مبكراً.",
  "note": V.format(m=J) + "سُلّم مشروع سدرة (مجتمع سكني بمساحة 20 مليون م² في الرياض) قبل موعده، وهو أول مشروع كبير يسلّم منازل للعملاء. والمستهدف 400,000 منزل بحلول 2030، وتملك المجموعة أكثر من 200 مليون م² من الأراضي للبناء مستقبلاً. وجرى ترتيب تسهيل ائتماني بقيمة 10 مليارات ريال (نحو 2.7 مليار دولار). والرئيس التنفيذي ديفيد غروفر."},
 "Ma'aden Mining Expansion": {"lead": "شركة التعدين العربية السعودية (معادن)",
  "desc": "بطل التعدين الوطني في المملكة، ومن أقوى المشاريع أداءً في رؤية 2030، إذ ارتفع صافي ربحه 91% في 2025. وتوسعة الفوسفات 3 على المسار لعام 2027.",
  "note": V.format(m=J) + "توسع قوي: بلغت نسبة إنجاز توسعة الفوسفات 3 نحو 50% وهي على الجدول لبدء الإنتاج في 2027. وارتفع صافي الربح 91% في الأشهر التسعة الأولى من 2025. وتُقدَّم بوصفها «الركيزة الثالثة» للاقتصاد السعودي، ومن أبرز المتفوقين في محفظة رؤية 2030."},
 "Ma'aden Aluminium": {"lead": "معادن (تملك 100% منذ يوليو 2025)",
  "desc": "مجمّع متكامل من البوكسيت إلى الألومنيوم في رأس الخير. كان مشروعاً مشتركاً بين معادن وألكوا، وخرجت ألكوا بالكامل في يوليو 2025، فباتت معادن تملكه بنسبة 100%.",
  "note": V.format(m=J) + "تصحيح رئيس: خرجت ألكوا بالكامل في 1 يوليو 2025 ببيع حصتها البالغة 25.1% لمعادن مقابل 1.35 مليار دولار (150 مليون دولار نقداً إضافةً إلى أسهم في معادن)، وتأكد ذلك في إفصاحات ألكوا الرسمية لدى هيئة الأوراق المالية الأمريكية. لم يعد مشروعاً مشتركاً، وأُعيد تصنيفه من مشروع مشترك إلى مختلط (شركة مدرجة)، وحُذفت بيانات المشروع المشترك."},
 "SABIC": {"lead": "الشركة السعودية للصناعات الأساسية (سابك)",
  "desc": "شركة عالمية عملاقة للبتروكيماويات، مملوكة لأرامكو السعودية بنسبة 70%. وهي ركيزة أساسية في محور التصنيع ضمن رؤية 2030، وتحقق إيرادات كبيرة غير نفطية.",
  "note": V.format(m=J) + "تملك أرامكو 70%، وتُتداول الـ30% المتبقية في السوق المالية السعودية (استحوذت أرامكو على الحصة من صندوق الاستثمارات العامة مقابل 259.125 مليار ريال / 69.1 مليار دولار في 2020، وتسدد للصندوق على أقساط حتى 2028). وقلّصت ذراع الأسمدة في سابك خطط مصنع أمونيا منخفضة الكربون مطلع 2026."},
 "SATORP / Amiral Expansion": {"lead": "ساتورب",
  "desc": "مجمّع أميرال للبتروكيماويات المتكامل مع مصفاة ساتورب في الجبيل (مصفاة أرامكو وتوتال إنرجيز): أرامكو (62.5%) / توتال إنرجيز (37.5%). على المسار لعام 2027، وسيكون أكبر منتج للإيثيلين في الخليج، وهو مادة أساسية في صناعة البلاستيك.",
  "note": V.format(m=J) + "أُرسيت عقود الإنشاء الرئيسة في يونيو 2023، والتشغيل التجاري مستهدف في 2027. وتأكدت قيمة 11 مليار دولار (إفصاح مباشر من توتال إنرجيز). وسينتج 1.65 مليون طن سنوياً من الإيثيلين (مادة أساسية في صناعة البلاستيك)، وهو أكبر مصنع من نوعه في الخليج، إضافةً إلى وحدتين للبلاستيك بطاقة 500,000 طن لكل منهما. وهو على المسار وفق التقارير المشتركة لأرامكو وتوتال إنرجيز."},
 "Saudi Aramco Jafurah Gas Field": {"lead": "أرامكو السعودية",
  "desc": "بدأ إنتاج المرحلة الأولى من أكبر مشروع للغاز الصخري خارج الولايات المتحدة في ديسمبر 2025. ويستهدف ملياري قدم مكعبة من الغاز يومياً بحلول 2030، وهو محوري في استراتيجية أرامكو لنمو الغاز.",
  "note": V.format(m=J) + "بدأ إنتاج المرحلة الأولى في ديسمبر 2025 بمعدل 450 مليون قدم مكعبة من الغاز يومياً، وأكدت ذلك وزارة المالية في بيان ميزانية 2026. والمستهدف ملياري قدم مكعبة يومياً بحلول 2030. وجمعت أرامكو 11 مليار دولار في 2025 بتأجير معامل معالجة الغاز لمجموعة مستثمرين بقيادة بلاك روك، وهو ترتيب تمويلي تحتفظ فيه أرامكو بالملكية. وتتجاوز قيمة دورة حياة المشروع 100 مليار دولار."},
 "King Salman Energy Park (SPARK)": {"lead": "أرامكو السعودية (سبارك)",
  "desc": "مدينة صناعية للطاقة قرب الدمام، مملوكة بالكامل لأرامكو السعودية. اكتملت المرحلة الأولى وهي تعمل بسبعة مصانع، والمستهدف أكثر من 300 منشأة عند اكتمالها (نحو 2035).",
  "note": V.format(m=J) + "7 مصانع عاملة و14 قيد الإنشاء حتى 2025. واكتملت المرحلة الأولى في 2021، وهي أول مدينة صناعية تنال شهادة LEED الفضية الدولية للمباني الخضراء. والمخطط أكثر من 300 منشأة عند الاكتمال (نحو 2035). وتُدار محطة حاويات برية بالشراكة مع هتشيسون بورتس. ويُتوقع أن تضيف نحو 6 مليارات دولار سنوياً إلى الاقتصاد عند اكتمالها."},
 "Saudi Water Authority (SWA) Desalination": {"lead": "الهيئة السعودية للمياه (المؤسسة العامة لتحلية المياه المالحة سابقاً)",
  "desc": "أكبر منتج للمياه المحلاة في العالم، وتديره الهيئة السعودية للمياه التي حلّت رسمياً محل المؤسسة العامة لتحلية المياه المالحة في 2024. وتتنامى الطاقة الإنتاجية عبر عقود طويلة الأجل مع شركات المياه الخاصة.",
  "note": V.format(m=J) + "تصحيح اسم الجهة: أصبحت المؤسسة العامة لتحلية المياه المالحة الهيئةَ السعودية للمياه في 2024. وتنتج نحو 11.5 مليون متر مكعب من مياه الشرب يومياً، وهو الأكبر بين جميع الجهات في العالم. وتُبنى المحطات الجديدة وتُشغَّل بواسطة شركات خاصة (مثل أكوا باور) بموجب عقود حكومية طويلة الأجل."},
 "MODON Industrial Cities": {"lead": "الهيئة السعودية للمدن الصناعية ومناطق التقنية (مدن)",
  "desc": "شبكة وطنية تضم أكثر من 35 مدينة صناعية توفّر أراضي مطوَّرة لنحو 6,500 مصنع و517,000 عامل، وتدعم توطين التصنيع في رؤية 2030.",
  "note": V.format(m=J) + "نحو 35–36 مدينة صناعية (منها 6 واحات صناعية) تحتضن نحو 6,500 مصنع ونحو 517,000 موظف. وأُرسيت عقود جديدة بقيمة 266 مليون ريال في 2024. وتعمل تحت مظلة وزارة الصناعة والثروة المعدنية."},
 "Ras Al-Khair Industrial City": {"lead": "الهيئة الملكية للجبيل وينبع",
  "desc": "مركز للتعدين والصناعات البحرية والصناعة على ساحل الخليج تديره الهيئة الملكية للجبيل وينبع. ويضم حوض الصناعات البحرية الدولية ومجمّع معادن للألومنيوم ومحطة تحلية الهيئة السعودية للمياه. ويتجاوز إجمالي الاستثمار 165 مليار ريال (نحو 44 مليار دولار).",
  "note": V.format(m=J) + "تجاوز إجمالي الاستثمار 165 مليار ريال (نحو 44 مليار دولار) بنهاية 2025، أكثر من 90% منه من شركات خاصة (واس/عرب نيوز، مايو 2026). ويضم حوض الصناعات البحرية الدولية ومصهر معادن للألومنيوم ومحطة تحلية الهيئة السعودية للمياه. واستقطبت منطقته الاقتصادية الخاصة نحو 27 مليار ريال من الاستثمارات (منها 12 مليار ريال من مستثمرين أجانب) بنهاية 2025. وتديره الهيئة الملكية للجبيل وينبع، لا هيئة «مدن»."},
 "International Maritime Industries (IMI)": {"lead": "الصناعات البحرية الدولية",
  "desc": "أكبر حوض بحري متكامل الخدمات في الخليج، في رأس الخير. يبني منصات الحفر البحرية والسفن ويصونها، ويشمل أول عقد كبير لبناء السفن في المملكة ست سفن شحن لصالح البحري (التسليم 2028–2029).",
  "note": V.format(m=J) + "الحصص وفق التقرير السنوي للبحري لعام 2018 والإعلان التأسيسي (رويترز/أرامكو): أرامكو 50.1%، ولامبريل 20%، والبحري 19.9%، وهيونداي للصناعات الثقيلة 10% (تذكر بعض المصادر الثانوية أرامكو 40% وهيونداي 20%، واعتُمد إفصاح البحري مصدراً أساسياً). وأول طلبية كبيرة لبناء السفن في المملكة: ست سفن شحن كبيرة للبحري (762 مليون ريال، التسليم 2028–2029). وضمنت أرامكو والبحري أعمالاً بنحو 10 مليارات دولار على مدى 10 سنوات."},
 "King Abdullah Economic City (KAEC)": {"lead": "إعمار المدينة الاقتصادية",
  "desc": "مدينة اقتصادية على البحر الأحمر أُعيد تنشيطها منطقةً اقتصادية خاصة ومركزاً لتصنيع السيارات. ويملك صندوق الاستثمارات العامة حصة أغلبية بنسبة 55.5% في إعمار المدينة الاقتصادية، المدرجة في السوق المالية السعودية.",
  "note": V.format(m=J) + "يملك صندوق الاستثمارات العامة الآن حصة أغلبية بنسبة 55.5% (ارتفعت من نحو 25% بتحويل قروض مستحقة له بقيمة 2.8 مليار ريال إلى أسهم). وأُعيد تنشيطها منطقةً اقتصادية خاصة وتجمّعاً للسيارات باسم «تجمّع الملك سلمان للسيارات» يضم مصانع سير ولوسيد AMP-2 وهيونداي HMMME. ولا تزال إعمار المدينة الاقتصادية مدرجة في السوق المالية السعودية."},
 "King Abdullah Port": {"lead": "شركة تطوير الموانئ",
  "desc": "أول ميناء في المملكة يطوّره القطاع الخاص بالكامل. صنّفه البنك الدولي سابقاً أكفأ ميناء حاويات في العالم، وجاء في المرتبة 30 في مؤشر 2023 (المنشور في 2024). وتستهدف المرحلة الثانية طاقة استيعابية تبلغ نحو 6 ملايين حاوية سنوياً.",
  "note": V.format(m=J) + "أول ميناء تجاري في المملكة مملوك ومطوَّر ومُشغَّل بالكامل من القطاع الخاص. تعامل مع 2.93 مليون حاوية في 2023. صنّفه البنك الدولي سابقاً أكفأ ميناء حاويات في العالم، وجاء في المرتبة 30 في مؤشر البنك الدولي لأداء موانئ الحاويات لعام 2023 (المنشور في 2024). وتستهدف المرحلة الثانية نحو 6 ملايين حاوية سنوياً. والتوزيع الدقيق للحصص بين شركاء شركة تطوير الموانئ غير معلن."},
 "Jubail Industrial City II": {"lead": "الهيئة الملكية للجبيل وينبع",
  "desc": "توسعة المدينة الصناعية الرائدة للبتروكيماويات في المملكة على ساحل الخليج. وتضاعف الهيئة الملكية مساحة الجبيل بحلول 2030 بالتزام قدره 67.5 مليار ريال (نحو 18 مليار دولار).",
  "note": V.format(m=J) + "خُصص 67.5 مليار ريال (نحو 18 مليار دولار) لمضاعفة مساحة الجبيل بحلول 2030. وأُضيفت مصانع كيميائية جديدة لشركة إنيوس البريطانية (نحو 7 مليارات ريال) في 2024. وتدير شركة بكتل الأمريكية للهندسة برنامج التوسعة البالغ نحو 6 مليارات دولار. وتحتضن المدينة مجمّع أميرال (ساتورب)، والجامعة مخططة نحو 2026."},
 "Ceer": {"lead": "سير موتورز",
  "desc": "أول علامة سعودية للسيارات الكهربائية، وهي مشروع مشترك بين صندوق الاستثمارات العامة وفوكسكون بتقنية BMW. وأولى المركبات مستهدفة في أكتوبر–ديسمبر 2026 من مصنع مدينة الملك عبدالله الاقتصادية بقيمة 1.3 مليار دولار، والطاقة الكاملة 240,000 مركبة سنوياً.",
  "note": V.format(m=J) + "الإنتاج في أكتوبر–ديسمبر 2026 (بعد أن كان مقرراً في 2025). مصنع بقيمة 1.3 مليار دولار في مدينة الملك عبدالله الاقتصادية (240,000 مركبة سنوياً بالطاقة الكاملة). ويستخدم تقنية BMW المرخّصة، وستورّد هيونداي ترانسيس أنظمة الدفع (صفقة بقيمة 8.2 مليارات ريال). وتوزيع الملكية بين الصندوق وفوكسكون غير معلن. ويستهدف تصنيع 45% من القطع محلياً وإضافة 8 مليارات دولار إلى الاقتصاد بحلول 2034."},
 "Lucid Manufacturing (AMP-2, KAEC)": {"lead": "مجموعة لوسيد (يملك صندوق الاستثمارات العامة نحو 60%)",
  "desc": "مصنع لوسيد AMP-2 في مدينة الملك عبدالله الاقتصادية، أول مصنع سيارات في المملكة، افتُتح في سبتمبر 2023. ويملك صندوق الاستثمارات العامة نحو 60% من مجموعة لوسيد. ويُبنى حالياً مصنع سيارات متكامل بجوار مصنع التجميع.",
  "note": V.format(m=J) + "تصحيح الاسم: هذا مصنع لوسيد AMP-2، أما AMP-1 فهو منشأة لوسيد في أريزونا (الولايات المتحدة). افتُتح AMP-2 في سبتمبر 2023 بوصفه أول مصنع سيارات في المملكة. وتجمّع المرحلة الأولى نحو 5,000 سيارة سنوياً من مجموعات قطع تُشحن من الولايات المتحدة، ويُبنى مصنع متكامل بجواره (155,000 سيارة سنوياً عند اكتماله). والتزم الصندوق والصناديق التابعة له بنحو 9.5 مليارات دولار للوسيد منذ 2018."},
 "Hyundai-PIF Vehicle Plant (HMMME)": {"lead": "هيونداي موتور للتصنيع في الشرق الأوسط (HMMME)",
  "desc": "أول مصنع لهيونداي في الشرق الأوسط، وهو مشروع مشترك بين صندوق الاستثمارات العامة (70%) وهيونداي موتور (30%). وُضع حجر الأساس في مايو 2025 في مدينة الملك عبدالله الاقتصادية، وأول مركبة مستهدفة في أكتوبر–ديسمبر 2026.",
  "note": V.format(m=J) + "حصص الصندوق 70% وهيونداي 30% مؤكدة في البيانات الرسمية للصندوق وهيونداي. وُضع حجر الأساس في 14 مايو 2025 في تجمّع الملك سلمان للسيارات بمدينة الملك عبدالله الاقتصادية. وأول مركبة في أكتوبر–ديسمبر 2026، وسينتج المصنع 50,000 مركبة سنوياً (بنزين وكهرباء)، والاستثمار يتجاوز 500 مليون دولار."},
 "Saudi Green Initiative (SGI)": {"lead": "اللجنة العليا لمبادرة السعودية الخضراء / وزارة البيئة والمياه والزراعة / المركز الوطني لتنمية الغطاء النباتي",
  "desc": "برنامج وطني يستهدف الحياد الصفري بحلول 2060 وزراعة 10 مليارات شجرة. أُعلن عن استثمارات تتجاوز 186 مليار دولار، وزُرعت نحو 159 مليون شجرة حتى مطلع 2026، وتتسارع مستهدفات الطاقة المتجددة.",
  "note": V.format(m=J) + "استثمارات معلنة تتجاوز 186–188 مليار دولار (705 مليارات ريال) وفق الموقع الرسمي للمبادرة. وزُرعت نحو 159 مليون شجرة حتى مطلع 2026، والمستهدف الوطني 10 مليارات شجرة، وأُعيد تأهيل أكثر من مليون هكتار من الأراضي. والمستهدف المرحلي أكثر من 600 مليون شجرة بحلول 2030، والالتزام بالحياد الصفري بحلول 2060."},
 "Special Integrated Logistics Zone (SILZ)": {"lead": "شركة المنطقة اللوجستية المتكاملة الخاصة (بإشراف الهيئة العامة للطيران المدني)",
  "desc": "منطقة جمركية خاصة في مطار الرياض، تخزّن فيها الشركات العالمية البضائع وتعالجها وتعيد تصديرها بإجراءات جمركية مبسطة، وتعمل منذ 2022. ومن أبرز المستأجرين أبل ولينوفو (مصنع بمساحة 200,000 م² يُفتتح في 2026) والمركز الإقليمي لشركة DHL.",
  "note": V.format(m=J) + "أُطلقت في أكتوبر 2022، وهي تعمل وتتوسع. ومن المستأجرين المؤكدين: أبل (أول شاغل)، ولينوفو (وضع حجر الأساس 2025، منشأة بمساحة 200,000 م²، والإنتاج 2026)، وDHL (مركز إقليمي بقيمة 130 مليون يورو، نوفمبر 2025)، ونوكيا، وشلهوب، وشي إن، وآلات/سافاير."},
}
AR_PARTNER = {"NEOM": "نيوم", "ACWA Power": "أكوا باور", "Air Products": "إير برودكتس", "Ajdan Real Estate": "أجدان العقارية",
  "SEDCO Capital": "سدكو كابيتال", "Saudi Aramco": "أرامكو السعودية", "Public float": "أسهم متداولة للعموم", "TotalEnergies": "توتال إنرجيز",
  "GIP/BlackRock consortium (midstream financing)": "تحالف GIP / بلاك روك (تمويل مرافق المعالجة والنقل)",
  "Hutchison Ports (inland cargo terminal)": "هتشيسون بورتس (محطة الحاويات البرية)", "Lamprell": "لامبريل", "Bahri": "البحري",
  "Hyundai Heavy Industries": "هيونداي للصناعات الثقيلة", "PIF (majority shareholder)": "صندوق الاستثمارات العامة (مساهم أغلبية)",
  "Emaar, The Economic City": "إعمار المدينة الاقتصادية", "Huta Marine (Binladin Group)": "هوتا مارين (مجموعة بن لادن)",
  "PIF": "صندوق الاستثمارات العامة", "Foxconn (Hon Hai)": "فوكسكون (هون هاي)",
  "PIF (parent stake in Lucid Group)": "صندوق الاستثمارات العامة (حصة في الشركة الأم، مجموعة لوسيد)", "Hyundai Motor": "هيونداي موتور",
  "Other shareholders / public float": "مساهمون آخرون / أسهم متداولة"}
AR_COMPLETION = {"2030+ (revised)": "بعد 2030 (معدَّل)", "Post-2030": "بعد 2030", "Ongoing": "مستمر"}

# every project and partner must be covered — fail loudly otherwise
import re
src = FILES['v']
names = re.findall(r'^\s*\{name:"([^"]+)"', src[src.index('const PROJECTS = ['):src.index('/* ====', src.index('const PROJECTS = ['))], re.M)
partners = set(re.findall(r'\{n:"([^"]+)",s:', src))
missing = [n for n in names if n not in AR_TXT] + [p for p in partners if p not in AR_PARTNER]
if len(names) != 31 or missing:
    FAILURES.append({'file': 'v', 'note': 'Arabic texts incomplete', 'old': '%d projects; missing %s' % (len(names), missing)})

BLOCK = ("\n/* audit 12/10 (macro-06): Arabic texts for every project (EH translations) — description, review note, lead entity;\n"
         "   partner names and completion values. English stays in PROJECTS; the Arabic tab reads from here. */\n"
         "const AR_TXT = " + json.dumps(AR_TXT, ensure_ascii=False, indent=0) + ";\n"
         "const AR_PARTNER = " + json.dumps(AR_PARTNER, ensure_ascii=False) + ";\n"
         "const AR_COMPLETION = " + json.dumps(AR_COMPLETION, ensure_ascii=False) + ";\n"
         "function arTxt(p,k){ const t=AR_TXT[p.name]; return (t&&t[k])||p[k]; }\n"
         "function arPartner(n){ return AR_PARTNER[n]||n; }\n"
         "function arCompletion(c){ return AR_COMPLETION[c]||c; }\n")
R("function arName(p){ return AR_NAMES[p.name]||p.name; }", "function arName(p){ return AR_NAMES[p.name]||p.name; }" + BLOCK,
  'copy', 'macro-06: Arabic descriptions, review notes, lead entities, partner names, completion values (31 projects)')
R("<div class=\"desc\">${p.desc}</div>\n      <div class=\"c-meta\">\n        <span class=\"status-pill\"><span class=\"dot\" style=\"background:${STATUS_HEX[p.status]}\"></span>${AR_STATUS[p.status]}</span>\n        <div class=\"figs\"><b>${arFmtInv(p.investment)}</b>${p.completion}",
  "<div class=\"desc\">${arTxt(p,'desc')}</div>\n      <div class=\"c-meta\">\n        <span class=\"status-pill\"><span class=\"dot\" style=\"background:${STATUS_HEX[p.status]}\"></span>${AR_STATUS[p.status]}</span>\n        <div class=\"figs\"><b>${arFmtInv(p.investment)}</b>${arCompletion(p.completion)}",
  'code', 'macro-06: Arabic card description and completion')
R("      <td style=\"color:var(--ink-soft)\">${p.lead}</td>\n      <td><span class=\"mini-dot\"><span class=\"dot\" style=\"background:${STATUS_HEX[p.status]}\"></span>${AR_STATUS[p.status]}</span></td>\n      <td class=\"num\">${p.completion}</td>",
  "      <td style=\"color:var(--ink-soft)\">${arTxt(p,'lead')}</td>\n      <td><span class=\"mini-dot\"><span class=\"dot\" style=\"background:${STATUS_HEX[p.status]}\"></span>${AR_STATUS[p.status]}</span></td>\n      <td class=\"num\">${arCompletion(p.completion)}</td>",
  'code', 'macro-06: Arabic table lead entity and completion')
R("function arFmtInv(v){ return v==null?\"—\":\"$\"+(Number.isInteger(v)?v:v.toFixed(1))+\"B\"; }",
  "function arFmtInv(v){ return v==null?\"—\":(Number.isInteger(v)?v:v.toFixed(1))+\" مليار $\"; }   // audit 12/10 (macro-06): Arabic unit, as in the KPI",
  'code', 'macro-06: Arabic investment unit')
R("document.getElementById(\"arDLead\").textContent=p.lead;", "document.getElementById(\"arDLead\").textContent=arTxt(p,'lead');",
  'code', 'macro-06: Arabic drawer lead entity')
R("<div><strong>ملاحظة المراجعة:</strong> ${p.note}</div>", "<div><strong>ملاحظة المراجعة:</strong> ${arTxt(p,'note')}</div>",
  'code', 'macro-06: Arabic drawer review note')
R("    <div class=\"d-section\"><div class=\"d-desc\">${p.desc}</div></div>\n    ${noteHtml}\n    <div class=\"d-section\"><h3>الحقائق الأساسية</h3>",
  "    <div class=\"d-section\"><div class=\"d-desc\">${arTxt(p,'desc')}</div></div>\n    ${noteHtml}\n    <div class=\"d-section\"><h3>الحقائق الأساسية</h3>",
  'code', 'macro-06: Arabic drawer description')
R("<div class=\"fact\"><div class=\"fl\">الاكتمال المتوقع</div><div class=\"fv num\">${p.completion}</div></div>",
  "<div class=\"fact\"><div class=\"fl\">الاكتمال المتوقع</div><div class=\"fv num\">${arCompletion(p.completion)}</div></div>",
  'code', 'macro-06: Arabic drawer completion')
# tab labels
R("      Strategic Dashboard\n    </button>", "      <span id=\"tabDashLbl\">Strategic Dashboard</span>\n    </button>",
  'code', 'macro-06: first tab label can switch language')
R("      التقرير التحقق — عربي\n", "      تقرير التحقق — عربي\n", 'copy', 'macro-06: Arabic tab name made grammatical')
R("function switchTab(tab){document.documentElement.lang=(tab==='arabic'?'ar':'en');",
  "function switchTab(tab){document.documentElement.lang=(tab==='arabic'?'ar':'en');\n"
  "  { const l=document.getElementById('tabDashLbl'); if(l) l.textContent=(tab==='arabic'?'اللوحة الاستراتيجية (بالإنجليزية)':'Strategic Dashboard'); }   // audit 12/10 (macro-06)",
  'code', 'macro-06: first tab label in Arabic while the Arabic tab is open')

# ---------------------------------------------------------------- macro-08 remainder slice
R("function confOf(p){ return CONF[p.confidence || CONF_OVERRIDE[p.name] || \"Medium\"]; }",
  "function confOf(p){ return CONF[p.confidence || CONF_OVERRIDE[p.name] || \"Medium\"]; }\n"
  "/* audit 12/10 (macro-08): when disclosed stakes add up to less than 100%, the rest is its own grey slice */\n"
  "const OTHER_HEX = \"#AEB9CE\";\n"
  "function stakeParts(p){ const sum=p.partners.reduce((a,pt)=>a+(pt.s||0),0); const parts=p.partners.map((pt,i)=>({n:pt.n,s:pt.s,c:SECTOR_HEX[i%SECTOR_HEX.length]}));\n"
  "  if(sum<99.5) parts.push({n:\"Other shareholders / public float\",s:+(100-sum).toFixed(1),c:OTHER_HEX,other:true}); return parts; }\n"
  "/* audit 12/10 (macro-19c): the review month comes from each project's own note */\n"
  "const MONTHS = {Jan:\"January\",Feb:\"February\",Mar:\"March\",Apr:\"April\",May:\"May\",Jun:\"June\",Jul:\"July\",Aug:\"August\",Sep:\"September\",Oct:\"October\",Nov:\"November\",Dec:\"December\"};\n"
  "const AR_MONTHS = {Jan:\"يناير\",Feb:\"فبراير\",Mar:\"مارس\",Apr:\"أبريل\",May:\"مايو\",Jun:\"يونيو\",Jul:\"يوليو\",Aug:\"أغسطس\",Sep:\"سبتمبر\",Oct:\"أكتوبر\",Nov:\"نوفمبر\",Dec:\"ديسمبر\"};\n"
  "function reviewedOf(p,ar){ const m=/^Verified \\((\\w{3}) (\\d{4})\\)/.exec(p.note||\"\"); if(!m) return ar?\"أغسطس 2026\":LAST_REVIEWED; return (ar?AR_MONTHS[m[1]]:MONTHS[m[1]])+\" \"+m[2]; }",
  'code', 'macro-08/19c: remainder-slice and review-month helpers')
R("""        <div class="jv-legend">${p.partners.map((pt,i)=>`
          <div class="jv-item"><span class="dot" style="background:${SECTOR_HEX[i%SECTOR_HEX.length]}"></span>
          <span class="jn">${pt.n}</span><span class="js">${pt.s}%</span></div>`).join("")}</div>""",
  """        <div class="jv-legend">${stakeParts(p).map(pt=>`
          <div class="jv-item"><span class="dot" style="background:${pt.c}"></span>
          <span class="jn">${pt.n}</span><span class="js">${pt.s}%</span></div>`).join("")}</div>""",
  'code', 'macro-08: EN legend lists the remainder')
R("""      data:{labels:p.partners.map(pt=>pt.n),datasets:[{data:p.partners.map(pt=>pt.s),backgroundColor:p.partners.map((_,i)=>SECTOR_HEX[i%SECTOR_HEX.length]),borderColor:ehTok("--eh-paper","#fff"),borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"60%",
        plugins:""",
  """      data:{labels:stakeParts(p).map(pt=>pt.n),datasets:[{data:stakeParts(p).map(pt=>pt.s),backgroundColor:stakeParts(p).map(pt=>pt.c),borderColor:ehTok("--eh-paper","#fff"),borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"60%",
        plugins:""",
  'code', 'macro-08: EN doughnut draws the remainder')
R("<div class=\"jv-legend\">${p.partners.map((pt,i)=>`<div class=\"jv-item\"><span class=\"dot\" style=\"background:${SECTOR_HEX[i%SECTOR_HEX.length]}\"></span><span class=\"jn\">${pt.n}</span><span class=\"js\">${pt.s}%</span></div>`).join(\"\")}</div></div>`;",
  "<div class=\"jv-legend\">${stakeParts(p).map(pt=>`<div class=\"jv-item\"><span class=\"dot\" style=\"background:${pt.c}\"></span><span class=\"jn\">${arPartner(pt.n)}</span><span class=\"js\">${pt.s}%</span></div>`).join(\"\")}</div></div>`;",
  'code', 'macro-08/06: AR legend lists the remainder, partner names in Arabic')
R("<div class=\"jv-bar-top\"><span class=\"jn\">${pt.n}</span><span class=\"js\">${pt.s!=null?pt.s+\"%\":\"غير معلن\"}</span>",
  "<div class=\"jv-bar-top\"><span class=\"jn\">${arPartner(pt.n)}</span><span class=\"js\">${pt.s!=null?pt.s+\"%\":\"غير معلن\"}</span>",
  'code', 'macro-06: AR partner names (undisclosed stakes)')
R("      data:{labels:p.partners.map(pt=>pt.n),datasets:[{data:p.partners.map(pt=>pt.s),backgroundColor:p.partners.map((_,i)=>SECTOR_HEX[i%SECTOR_HEX.length]),borderColor:ehTok(\"--eh-paper\",\"#fff\"),borderWidth:3}]},\n      options:{responsive:true,maintainAspectRatio:false,cutout:\"60%\",plugins:",
  "      data:{labels:stakeParts(p).map(pt=>arPartner(pt.n)),datasets:[{data:stakeParts(p).map(pt=>pt.s),backgroundColor:stakeParts(p).map(pt=>pt.c),borderColor:ehTok(\"--eh-paper\",\"#fff\"),borderWidth:3}]},\n      options:{responsive:true,maintainAspectRatio:false,cutout:\"60%\",plugins:",
  'code', 'macro-08: AR doughnut draws the remainder')

# ---------------------------------------------------------------- macro-19 (b, c)
R("makeChips(document.getElementById(\"statusChips\"),ALL_STATUS,state.status,false);",
  "makeChips(document.getElementById(\"statusChips\"),ALL_STATUS.filter(s=>PROJECTS.some(p=>p.status===s)),state.status,false);   // audit 12/10 (macro-19b): no chips that match nothing",
  'code', 'macro-19b: EN status chips only for statuses in use')
R("  [\"High\",\"Medium\",\"Low\"].forEach(level=>{\n    const c=document.createElement(\"button\");\n    c.className=\"conf-chip\";\n    c.innerHTML=`<span class=\"cdot\" style=\"background:${CONF[level].hex}\"></span>${level}`;",
  "  [\"High\",\"Medium\",\"Low\"].filter(l=>PROJECTS.some(p=>confOf(p).label===l)).forEach(level=>{\n    const c=document.createElement(\"button\");\n    c.className=\"conf-chip\";\n    c.innerHTML=`<span class=\"cdot\" style=\"background:${CONF[level].hex}\"></span>${level}`;",
  'code', 'macro-19b: EN confidence chips only for levels in use')
R("arMakeChips(document.getElementById(\"arStatusChipsF\"),ALL_STATUS,arState.status,'status');",
  "arMakeChips(document.getElementById(\"arStatusChipsF\"),ALL_STATUS.filter(s=>PROJECTS.some(p=>p.status===s)),arState.status,'status');",
  'code', 'macro-19b: AR status chips only for statuses in use')
R("  [\"High\",\"Medium\",\"Low\"].forEach(level=>{\n    const c=document.createElement(\"button\");\n    c.className=\"conf-chip\";\n    c.innerHTML=`<span class=\"cdot\" style=\"background:${CONF[level].hex}\"></span>${AR_CONF[level]}`;",
  "  [\"High\",\"Medium\",\"Low\"].filter(l=>PROJECTS.some(p=>confOf(p).label===l)).forEach(level=>{\n    const c=document.createElement(\"button\");\n    c.className=\"conf-chip\";\n    c.innerHTML=`<span class=\"cdot\" style=\"background:${CONF[level].hex}\"></span>${AR_CONF[level]}`;",
  'code', 'macro-19b: AR confidence chips only for levels in use')
R("<div class=\"fact\"><div class=\"fl\">Last Reviewed</div><div class=\"fv\" style=\"font-size:13px\">${LAST_REVIEWED}</div></div>",
  "<div class=\"fact\"><div class=\"fl\">Last Reviewed</div><div class=\"fv\" style=\"font-size:13px\">${reviewedOf(p,false)}</div></div>",
  'code', 'macro-19c: EN last-reviewed month per project')
R("<div class=\"fact\"><div class=\"fl\">آخر مراجعة</div><div class=\"fv\" style=\"font-size:13px\">أغسطس 2026</div></div>",
  "<div class=\"fact\"><div class=\"fl\">آخر مراجعة</div><div class=\"fv\" style=\"font-size:13px\">${reviewedOf(p,true)}</div></div>",
  'code', 'macro-19c: AR last-reviewed month per project')

# ---------------------------------------------------------------- macro-20 keyboard
R("    return `<div class=\"card\" data-idx=\"${idx}\">\n      <div class=\"c-top\">\n        <div class=\"c-name\">${p.name}</div>",
  "    return `<div class=\"card\" data-idx=\"${idx}\" tabindex=\"0\" role=\"button\">\n      <div class=\"c-top\">\n        <div class=\"c-name\">${p.name}</div>",
  'code', 'macro-20: EN cards focusable')
R("    return `<tr data-idx=\"${idx}\">\n      <td><span class=\"tname\">${p.name}</span>",
  "    return `<tr data-idx=\"${idx}\" tabindex=\"0\">\n      <td><span class=\"tname\">${p.name}</span>", 'code', 'macro-20: EN rows focusable')
R("    return `<div class=\"card\" data-idx=\"${idx}\">\n      <div class=\"c-top\"><div class=\"c-name\">${arName(p)}</div>",
  "    return `<div class=\"card\" data-idx=\"${idx}\" tabindex=\"0\" role=\"button\">\n      <div class=\"c-top\"><div class=\"c-name\">${arName(p)}</div>",
  'code', 'macro-20: AR cards focusable')
R("    return `<tr data-idx=\"${idx}\">\n      <td><span class=\"tname\">${arName(p)}</span>",
  "    return `<tr data-idx=\"${idx}\" tabindex=\"0\">\n      <td><span class=\"tname\">${arName(p)}</span>", 'code', 'macro-20: AR rows focusable')
R("<aside class=\"drawer panel ar-drawer\" id=\"arDrawer\" data-eh-noreveal dir=\"rtl\" aria-hidden=\"true\">",
  "<aside class=\"drawer panel ar-drawer\" id=\"arDrawer\" data-eh-noreveal dir=\"rtl\" aria-hidden=\"true\" inert>", 'code', 'macro-20: closed AR drawer inert')
R("<aside class=\"drawer panel\" id=\"drawer\" data-eh-noreveal aria-hidden=\"true\">",
  "<aside class=\"drawer panel\" id=\"drawer\" data-eh-noreveal aria-hidden=\"true\" inert>", 'code', 'macro-20: closed EN drawer inert')
R("  document.getElementById(\"scrim\").classList.add(\"open\");\n  document.getElementById(\"drawer\").classList.add(\"open\");\n  document.getElementById(\"drawer\").setAttribute(\"aria-hidden\",\"false\");",
  "  ehDrawerOpen(\"drawer\",\"drawerClose\");\n  document.getElementById(\"scrim\").classList.add(\"open\");\n  document.getElementById(\"drawer\").classList.add(\"open\");\n  document.getElementById(\"drawer\").setAttribute(\"aria-hidden\",\"false\");",
  'code', 'macro-20: EN drawer focus in')
R("function closeDrawer(){\n  document.getElementById(\"scrim\").classList.remove(\"open\");",
  "/* audit 12/10 (macro-20): drawers are inert while closed; focus moves to the close button and back to the card */\n"
  "let ehLastFocus=null;\n"
  "function ehDrawerOpen(id,closeId){ const d=document.getElementById(id); if(!d.classList.contains(\"open\")) ehLastFocus=document.activeElement; d.inert=false;\n"
  "  setTimeout(()=>{ try{ document.getElementById(closeId).focus({preventScroll:true}); }catch(e){} },0); }\n"
  "function ehDrawerClosed(id){ const d=document.getElementById(id); const was=d.classList.contains(\"open\"); d.inert=true;\n"
  "  if(was&&ehLastFocus&&ehLastFocus.isConnected){ try{ ehLastFocus.focus({preventScroll:true}); }catch(e){} } }\n"
  "document.addEventListener(\"keydown\",e=>{ const t=e.target; if((e.key===\"Enter\"||e.key===\" \")&&t&&t.matches&&t.matches(\".card[data-idx],tbody tr[data-idx]\")){ e.preventDefault(); t.click(); } });\n"
  "function closeDrawer(){\n  ehDrawerClosed(\"drawer\");\n  document.getElementById(\"scrim\").classList.remove(\"open\");",
  'code', 'macro-20: EN drawer focus out; Enter/Space opens the focused card or row')
R("  document.getElementById(\"arScrim\").classList.add(\"open\");\n  document.getElementById(\"arDrawer\").classList.add(\"open\");",
  "  ehDrawerOpen(\"arDrawer\",\"arDrawerClose\");\n  document.getElementById(\"arScrim\").classList.add(\"open\");\n  document.getElementById(\"arDrawer\").classList.add(\"open\");",
  'code', 'macro-20: AR drawer focus in')
R("function arCloseDrawer(){\n  document.getElementById(\"arScrim\").classList.remove(\"open\");",
  "function arCloseDrawer(){\n  ehDrawerClosed(\"arDrawer\");\n  document.getElementById(\"arScrim\").classList.remove(\"open\");",
  'code', 'macro-20: AR drawer focus out')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['v'])
md, _ = write_change_table(os.path.join(HERE, 'change_table_audit_macro_v2030'), 'Audit fixes — Vision 2030 (macro)')
print('patched Vision 2030 page;', md)
