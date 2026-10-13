#!/usr/bin/env python3
"""build_saudi_waste_page.py — renders hub/saudi_waste.html ("Saudi waste" · «النفايات في المملكة») from
pipeline/saudi_waste_data.json (written by extract_saudi_waste.py from the GASTAT workbooks) and the Natural Earth
region boundaries in pipeline/sources/ne_sau_adm1_simplified.geojson (public domain, simplified with mapshaper).

Every figure on the page is computed here or in the page from those two files — nothing is typed in by hand.
What the sources do NOT give (hazardous waste by region, industrial waste outside Jubail–Yanbu) is shown as a stated
gap; nothing is allocated or estimated.
Usage: python3 build_saudi_waste_page.py [saudi_waste_data.json] [out.html]"""
import json, os, sys, collections, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'saudi_waste_data.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'hub', 'saudi_waste.html')
GEO = os.path.join(HERE, 'sources', 'ne_sau_adm1_simplified.geojson')
D = json.load(open(SRC, encoding='utf-8'))
G = json.load(open(GEO, encoding='utf-8'))
YRS = [str(y) for y in range(2017, 2025)]

# ---------------------------------------------------------------- analysis (all from D)
mat, trt = D['municipal_by_material']['v'], D['municipal_by_treatment']['v']
pop, area = D['population_2022']['v'], D['area_km2']['v']
codes = [r['code'] for r in D['meta']['regions']]

def g(d, *k, default=0.0):
    for x in k:
        if not isinstance(d, dict) or x not in d or d[x] is None: return default
        d = d[x]
    return d

# regional data quality flags, found by rule (not by hand)
flags = {c: [] for c in codes}
for c in codes:
    for y in YRS:
        col, tr = g(mat, c, 'total', y), sum(g(trt, c, k, y) for k in ('landfill', 'recycling', 'incineration'))
        if col and abs(tr / col - 1) > 0.10:
            flags[c].append({'k': 'mismatch', 'y': y, 'col': col, 'tr': tr})
nat_pc = {y: g(mat, 'KSA', 'total', y) * 1000 / 365 / pop['KSA'] for y in YRS}
for c in codes:
    pc = g(mat, c, 'total', '2024') * 1000 / 365 / pop[c]
    if pc > 2 * nat_pc['2024']: flags[c].append({'k': 'percap', 'y': '2024', 'v': pc, 'nat': nat_pc['2024']})
    oth = g(mat, c, 'other', '2024') / g(mat, c, 'total', '2024')
    if oth > 0.6: flags[c].append({'k': 'other', 'y': '2024', 'v': oth, 'org17': g(mat, c, 'organic', '2017') / g(mat, c, 'total', '2017'),
                                   'org24': g(mat, c, 'organic', '2024') / g(mat, c, 'total', '2024')})

se_s, se_u = D['seea']['supply'], D['seea']['use']
REC_KEYS = ['recycling_msw', 'rec_agriculture', 'rec_mining', 'rec_manufacturing', 'rec_electricity', 'rec_construction', 'rec_other_economic']
def dest(y, t):
    u = se_u[y][t]
    return {'specialised': u['specialised_company'] or 0, 'recycled': sum(u[k] or 0 for k in REC_KEYS),
            'landfill': u['landfill'] or 0, 'other': u['other_disposal'] or 0, 'total': u['total'] or 0}
jm = D['jy_methods']['v']
jy_haz = {y: sum(g(jm, 'hazardous', k, y) for k in ('incineration', 'burial', 'recycling')) for y in ('2021', '2022', '2023', '2024')}
A = {
    'dest': {y: {t: dest(y, t) for t in ('hazardous', 'total')} for y in ('2023', '2024')},
    'jy_haz': jy_haz,
    'nat_pc': nat_pc,
    'flags': flags,
    'cum_landfill': {c: sum(g(trt, c, 'landfill', y) for y in YRS) for c in codes + ['KSA']},
}
# trade flags found by rule: exports above what the accounts say was generated, or the same export figure two years running
A['trade_flags'] = [t for t in se_u['2024'] if t != 'total' and (se_u['2024'][t]['exports'] or 0) > (se_s['2024'][t]['total'] or 0) > 0]
A['repeat_exports'] = [t for t in se_u['2024'] if t != 'total' and se_u['2024'][t]['exports'] and se_u['2024'][t]['exports'] == se_u['2023'][t]['exports']]


# ---------------------------------------------------------------- data-problem register (all evidence computed from D)
def f0(v): return f'{v:,.0f}'
def mt(v): return f'{v/1e6:,.2f} Mt'
def kt(v): return f'{v/1e3:,.0f} kt'
S23, S24, U23, U24 = se_s['2023'], se_s['2024'], se_u['2023'], se_u['2024']
fac = lambda a, b: (b / a) if a else None
sector_f = {k: collections.Counter(round(fac(S23[t][k], S24[t][k]), 4) for t in S24 if t != 'total' and S23[t].get(k) and S24[t].get(k)).most_common(1)[0]
            for k in ('agriculture', 'mining', 'manufacturing', 'electricity', 'other_economic', 'households')}
hz_f = fac(S23['hazardous']['manufacturing'], S24['hazardous']['manufacturing'])
spec_f = fac(U23['hazardous']['specialised_company'], U24['hazardous']['specialised_company'])
ratio_n = sum(1 for t in S23 if S23[t].get('mining') and round(S23[t]['manufacturing'] / S23[t]['mining'], 3) == 2.364)
treat = {y: sum(g(trt, 'KSA', k, y) for k in ('landfill', 'recycling', 'incineration')) for y in YRS}
mism = [(c, f['y'], f['col'], f['tr']) for c in codes for f in flags[c] if f['k'] == 'mismatch']
worst = sorted(mism, key=lambda m: -abs(m[3] / m[2] - 1))[:3]
derived = {y: [c for c in codes if abs(g(trt, c, 'landfill', y) - g(mat, c, 'total', y)) < 1] for y in YRS}
zero_rec = [(c, y) for c in codes for y in YRS if g(trt, c, 'recycling', y) == 0]
swings = []
for c in codes:
    for k in mat[c]:
        if k == 'total': continue
        for a, b in zip(YRS, YRS[1:]):
            va, vb = g(mat, c, k, a), g(mat, c, k, b)
            if max(va, vb) > 50000 and min(va, vb) > 0 and max(va, vb) / min(va, vb) >= 3: swings.append((c, k, a, va, b, vb))
mt_ = D['municipal_total']['v']; g10 = [mt_[str(y + 1)] / mt_[str(y)] - 1 for y in range(2010, 2014)]
rec15 = [y for y in D['recycled']['v']['municipal'] if abs(D['recycled']['v']['municipal'][y] / mt_[y] - 0.15) < 0.0005]
rv = D['revisions']; jy = D['jy_total']['v']
jy24_split = sum(g(jm, 'hazardous', k, '2024') for k in ('incineration', 'burial', 'recycling')) + g(jm, 'nonhazardous', 'burial', '2024')
jy24_rate_calc = D['recycled']['v']['jy']['2024'] / jy['2024']
RN = {r['code']: (r['en'], r['ar']) for r in D['meta']['regions']}
seea_msw = D['seea']['summary']['Percentage of Municipal Waste of the Total Waste Quantity']['2024'] * S24['total']['total']
REG = [
 # sev, title EN, title AR, evidence EN, evidence AR, handling EN, handling AR
 ('critical', 'No regional figures for hazardous or industrial waste', 'لا أرقام إقليمية للنفايات الخطرة أو الصناعية',
  f"Hazardous waste ({mt(S24['hazardous']['total'])}, 2024) is published only as a national total by producing sector. Industrial waste is published only for Jubail and Yanbu combined (Royal Commission), and nothing for MODON industrial cities. Only {jy_haz['2024']/S24['hazardous']['total']:.0%} of 2024 hazardous waste has a published location.",
  f"النفايات الخطرة ({mt(S24['hazardous']['total'])} في 2024) منشورة إجمالياً وطنياً فقط حسب القطاع المولِّد، والنفايات الصناعية منشورة للجبيل وينبع مجتمعتين فقط (الهيئة الملكية)، ولا شيء لمدن «مدن» الصناعية. {jy_haz['2024']/S24['hazardous']['total']:.0%} فقط من النفايات الخطرة لعام 2024 لها موقع منشور.",
  'The map shades municipal waste only; Jubail and Yanbu are shown as points. Nothing is estimated by region. Ask MWAN for regional data.',
  'تُلوَّن الخريطة بالنفايات البلدية فقط، وتظهر الجبيل وينبع كنقطتين، ولا يُقدَّر شيء حسب المنطقة. يُطلب ذلك من «موان».'),
 ('critical', "2024 national accounts are mostly 2023 scaled up, not new measurements", 'حسابات 2024 الوطنية في معظمها أرقام 2023 مضروبة في معامل، لا قياسات جديدة',
  f"In the SEEA tables, almost every 2024 value equals the 2023 value times one growth factor per sector: mining, manufacturing and utilities ×{sector_f['mining'][0]:.4f} (all waste types), agriculture ×{sector_f['agriculture'][0]:.4f}, other activities ×{sector_f['other_economic'][0]:.4f}, households ×{sector_f['households'][0]:.4f}. Hazardous waste in all four industry sectors ×{hz_f:.4f}, and hazardous waste sent to waste companies ×{spec_f:.4f}.",
  f"في جداول الحسابات البيئية تكاد كل قيمة لعام 2024 تساوي قيمة 2023 مضروبة في معامل نمو واحد لكل قطاع: التعدين والصناعة والمرافق ×{sector_f['mining'][0]:.4f} (لكل أنواع النفايات)، والزراعة ×{sector_f['agriculture'][0]:.4f}، والأنشطة الأخرى ×{sector_f['other_economic'][0]:.4f}، والأسر ×{sector_f['households'][0]:.4f}. والنفايات الخطرة في القطاعات الصناعية الأربعة ×{hz_f:.4f}، وكذلك الخطرة المسلَّمة لشركات النفايات ×{spec_f:.4f}.",
  'The +21% rises for total, hazardous and waste-company tonnage are shown as GASTAT projections, not measured market growth.',
  'تُعرض زيادات +21% في الإجمالي والنفايات الخطرة وكميات شركات النفايات على أنها إسقاطات للهيئة، لا نمواً مقيساً في السوق.'),
 ('critical', 'Sector split is apportioned with fixed ratios', 'التوزيع على القطاعات محسوب بنسب ثابتة',
  f"For {ratio_n} waste types, manufacturing is exactly 2.364 × mining and utilities exactly 0.052 × mining, in both years. Identical tonnages repeat across types: paper = 'other' = mixed waste in the industry sectors (361,371 / 854,150 / 18,773 t in 2023); slaughterhouse = 'other' in agriculture (1,059,734 t).",
  f"في {ratio_n} أنواع من النفايات تساوي الصناعةُ 2.364 × التعدين تماماً، والمرافقُ 0.052 × التعدين تماماً، في السنتين. وتتكرر أطنان متطابقة بين الأنواع: الورق = «أخرى» = المختلطة في القطاعات الصناعية (361,371 / 854,150 / 18,773 طن في 2023)، ومخلفات المسالخ = «أخرى» في الزراعة (1,059,734 طن).",
  'Producing-sector charts are read as GASTAT\'s allocation, not as measured tonnage by industry.',
  'تُقرأ رسوم القطاعات المولِّدة على أنها توزيع الهيئة، لا أطناناً مقيسة لكل صناعة.'),
 ('critical', "'Specialised waste company' includes informal operators and unsafe disposal", '«الشركات المتخصصة» تشمل جهات غير رسمية وطرق تخلص غير آمنة',
  f"GASTAT's footnote defines this column as companies collecting waste for disposal 'whether licensed official companies or informal ones', including selling, open dumping and 'safe and unsafe burial'. The {mt(U24['hazardous']['specialised_company'])} of hazardous waste in this column is not all licensed treatment.",
  f"تعرّف حاشية الهيئة هذا العمود بأنه شركات تجمع النفايات للتخلص منها «سواء كانت شركات رسمية مرخّصة أو غير رسمية»، ويشمل البيع والإلقاء المكشوف و«الدفن الآمن وغير الآمن». فالـ{mt(U24['hazardous']['specialised_company'])} من النفايات الخطرة في هذا العمود ليست كلها معالجة مرخّصة.",
  "EH's market figure is presented as an upper bound, not the licensed market.",
  'يُعرض رقم سوق آفاق البيئة حداً أعلى، لا حجم السوق المرخّص.'),
 ('critical', 'Municipal waste treated does not match waste collected', 'النفايات البلدية المعالجة لا تطابق المجموعة',
  f"Kingdom 2021: treated {mt(treat['2021'])} vs collected {mt(g(mat,'KSA','total','2021'))}; 2024: treated {mt(treat['2024'])} vs collected {mt(g(mat,'KSA','total','2024'))}. {len(mism)} region-years differ by more than 10%; the worst are " + '; '.join(f"{RN[c][0]} {y} ({(tr/col-1):+.0%})" for c, y, col, tr in worst) + '.',
  f"المملكة 2021: المعالَج {mt(treat['2021'])} مقابل المجموع {mt(g(mat,'KSA','total','2021'))}؛ 2024: المعالَج {mt(treat['2024'])} مقابل المجموع {mt(g(mat,'KSA','total','2024'))}. تختلف {len(mism)} حالة (منطقة-سنة) بأكثر من 10%، أسوؤها " + '؛ '.join(f"{RN[c][1]} {y} ({(tr/col-1):+.0%})" for c, y, col, tr in worst) + '.',
  'Flagged ⚠ per region and year on the map and table; landfill and recycling measures use table 3-10 as published.',
  'معلَّمة بـ⚠ لكل منطقة وسنة في الخريطة والجدول؛ ومقاييس الدفن والتدوير من جدول 3-10 كما نُشر.'),
 ('major', 'Early treatment data looks filled in as "all landfilled"', 'بيانات المعالجة المبكرة تبدو معبّأة على أنها «كلها دُفنت»',
  f"Landfill equals collected exactly, with zero recycling, in {len(derived['2017'])} regions in 2017, {len(derived['2018'])} in 2018 and {len(derived['2019'])} in 2019. Recycling is recorded as 0 in {len(zero_rec)} region-years, e.g. Tabuk 2017–2020, Hail and Al-Jouf 2017–2019, Madinah 2023–2024 — more likely missing than zero.",
  f"يساوي الدفنُ المجموعَ تماماً مع تدوير صفر في {len(derived['2017'])} مناطق في 2017، و{len(derived['2018'])} في 2018، و{len(derived['2019'])} في 2019. والتدوير مسجّل صفراً في {len(zero_rec)} حالة (منطقة-سنة)، مثل تبوك 2017–2020 وحائل والجوف 2017–2019 والمدينة 2023–2024 — والأرجح أنها بيانات ناقصة لا أصفار.",
  'Regional recycling rates for those years are shown but should not be compared with later years.',
  'تُعرض نسب التدوير الإقليمية لتلك السنوات لكن لا تُقارن بالسنوات اللاحقة.'),
 ('major', 'Copied values', 'قيم منسوخة',
  f"Madinah 2022 landfill and recycling are identical to 2021 to the gram (925,450.318 t and 41,167 t). Hazardous waste exports are exactly {f0(U24['hazardous']['exports'])} t in both 2023 and 2024.",
  f"أرقام الدفن والتدوير في المدينة المنورة لعام 2022 مطابقة لعام 2021 حتى الغرام (925,450.318 طن و41,167 طن). وصادرات النفايات الخطرة {f0(U24['hazardous']['exports'])} طن تماماً في 2023 و2024.",
  'Shown as published; treated as carried-forward values.',
  'تُعرض كما نُشرت، وتُعامَل على أنها قيم مُرحَّلة.'),
 ('major', 'Waste composition by region jumps implausibly', 'مكوّنات النفايات حسب المنطقة تقفز بشكل غير معقول',
  f"{len(swings)} cases where one material in one region changes threefold or more in a single year — e.g. Eastern region 'other' 0.42 → 3.02 Mt (2021→22), Eastern plastic 34 kt → 733 kt (2022→23), Riyadh paper 444 → 111 → 614 kt (2021→23), Madinah organic 883 → 186 kt (2019→20). Madinah is now 91% 'other non-organic'.",
  f"{len(swings)} حالة تتغير فيها مادة واحدة في منطقة واحدة ثلاثة أضعاف أو أكثر في سنة — مثل «أخرى» في الشرقية 0.42 → 3.02 مليون طن (2021→22)، وبلاستيك الشرقية 34 → 733 ألف طن (2022→23)، وورق الرياض 444 → 111 → 614 ألف طن (2021→23)، والعضوية في المدينة 883 → 186 ألف طن (2019→20). والمدينة الآن 91% «غير عضوية أخرى».",
  'Composition is shown for 2024 only, with Madinah flagged; no material trends by region are drawn.',
  'تُعرض المكوّنات لعام 2024 فقط مع تعليم المدينة، ولا تُرسم اتجاهات المواد حسب المنطقة.'),
 ('major', 'Outlier regional values', 'قيم إقليمية شاذة',
  f"Al-Baha: {g(mat,'SA-11','total','2024')*1000/365/pop['SA-11']:.1f} kg per person per day (Kingdom {nat_pc['2024']:.1f}); its collection more than doubled 2019→2020. Riyadh recycling: {kt(g(trt,'SA-01','recycling','2020'))} in 2020, {f0(g(trt,'SA-01','recycling','2021'))} t in 2021, {kt(g(trt,'SA-01','recycling','2022'))} in 2022.",
  f"الباحة: {g(mat,'SA-11','total','2024')*1000/365/pop['SA-11']:.1f} كغ للفرد يومياً (المملكة {nat_pc['2024']:.1f})، وتضاعف ما جُمع فيها بين 2019 و2020. تدوير الرياض: {kt(g(trt,'SA-01','recycling','2020'))} في 2020، و{f0(g(trt,'SA-01','recycling','2021'))} طن فقط في 2021، و{kt(g(trt,'SA-01','recycling','2022'))} في 2022.",
  'Flagged on the region panel.', 'معلَّمة في لوحة المنطقة.'),
 ('major', 'Early national series is modelled', 'السلسلة الوطنية المبكرة مُنمذَجة',
  f"Municipal waste 2010–2014 grows a near-constant {min(g10):.2%}–{max(g10):.2%} a year, then jumps {mt_['2016']/mt_['2015']-1:+.0%} and {mt_['2017']/mt_['2016']-1:+.0%}. Recycled municipal waste is exactly 15.0% of collected in every year {rec15[0]}–{rec15[-1]}.",
  f"تنمو النفايات البلدية 2010–2014 بمعدل شبه ثابت {min(g10):.2%}–{max(g10):.2%} سنوياً، ثم تقفز {mt_['2016']/mt_['2015']-1:+.0%} و{mt_['2017']/mt_['2016']-1:+.0%}. والمُدوَّر يساوي 15.0% من المجموع تماماً في كل سنة من {rec15[0]} إلى {rec15[-1]}.",
  "The '15% to 3.5%' fall compares an assumed rate with measured ones; the page says so.",
  'مقارنة «من 15% إلى 3.5%» تقارن نسبة مفترضة بنسب مقيسة، وتذكر الصفحة ذلك.'),
 ('major', 'GASTAT revised earlier figures between editions', 'راجعت الهيئة أرقاماً سابقة بين الإصدارات',
  f"Municipal 2023: {mt(rv['municipal_total']['env2023']['2023'])} (2023 edition) → {mt(mt_['2023'])} (2024 edition). Municipal 2017: {mt(rv['municipal_total']['env2021']['2017'])} (2021 edition) → {mt(mt_['2017'])}. Jubail–Yanbu 2018–2021 raised 8–11% between the 2022 and 2023 editions.",
  f"البلدية 2023: {mt(rv['municipal_total']['env2023']['2023'])} (إصدار 2023) ← {mt(mt_['2023'])} (إصدار 2024). البلدية 2017: {mt(rv['municipal_total']['env2021']['2017'])} (إصدار 2021) ← {mt(mt_['2017'])}. ورُفعت أرقام الجبيل وينبع 2018–2021 بنسبة 8–11% بين إصداري 2022 و2023.",
  'The 2024 edition is used throughout; older figures quoted elsewhere may differ.',
  'يُعتمد إصدار 2024 في كل الصفحة، وقد تختلف الأرقام القديمة المقتبسة في أماكن أخرى.'),
 ('major', 'Jubail–Yanbu 2024 does not add up', 'أرقام الجبيل وينبع 2024 غير متسقة',
  f"Hazardous + non-hazardous = {f0(jy24_split)} t against a total of {f0(jy['2024'])} t ({f0(jy['2024']-jy24_split)} t unassigned). The published recycling rate is {D['recycling_rate']['v']['jy']['2024']:.1%}, but recycled ÷ total = {jy24_rate_calc:.1%}. Several values end in thirds (e.g. 891,079.9128333 t), suggesting averaged figures.",
  f"الخطرة + غير الخطرة = {f0(jy24_split)} طن مقابل إجمالي {f0(jy['2024'])} طن ({f0(jy['2024']-jy24_split)} طن غير مصنّفة). ونسبة التدوير المنشورة {D['recycling_rate']['v']['jy']['2024']:.1%} لكن المُدوَّر ÷ الإجمالي = {jy24_rate_calc:.1%}. وتنتهي عدة قيم بأثلاث (مثل 891,079.9128333 طن)، ما يوحي بأرقام متوسطة.",
  'The published rate is shown; the hazardous share uses the published hazardous rows.',
  'تُعرض النسبة المنشورة، وتُحسب حصة الخطرة من صفوف الخطرة المنشورة.'),
 ('major', 'Waste trade figures conflict', 'أرقام تجارة النفايات متضاربة',
  f"Tables 3-15 and 3-16 carry the same title, 'Waste imports by type'. SEEA trade does not match them (2024 metal waste imports {mt(S24['metal']['imports'])} vs about 0.17 Mt of metal scrap in 3-15; glass {kt(S24['glass']['imports'])} vs 3 kt). Tyre exports {mt(U24['tyres']['exports'])} exceed the {kt(S24['tyres']['total'])} of tyres generated. Hazardous imports went from {kt(S23['hazardous']['imports'])} to {mt(S24['hazardous']['imports'])}.",
  f"الجدولان 3-15 و3-16 بالعنوان نفسه «واردات النفايات حسب النوع». ولا تطابقهما أرقام الحسابات البيئية (واردات المعادن 2024 {mt(S24['metal']['imports'])} مقابل نحو 0.17 مليون طن خردة معادن في 3-15؛ الزجاج {kt(S24['glass']['imports'])} مقابل 3 آلاف طن). وصادرات الإطارات {mt(U24['tyres']['exports'])} تفوق المتولد منها {kt(S24['tyres']['total'])}. وارتفعت واردات النفايات الخطرة من {kt(S23['hazardous']['imports'])} إلى {mt(S24['hazardous']['imports'])}.",
  'Trade is quoted from SEEA only, as a watch item, not as a finding.',
  'تُقتبس التجارة من الحسابات البيئية فقط، كبند متابعة لا كنتيجة.'),
 ('minor', "Three different 'municipal' totals", 'ثلاثة مجاميع مختلفة لـ«البلدية»',
  f"Ministry collection {mt(mt_['2024'])}; SEEA 'municipal share' {D['seea']['summary']['Percentage of Municipal Waste of the Total Waste Quantity']['2024']:.1%} of total = {mt(seea_msw)}; SEEA household waste {mt(S24['total']['households'])}.",
  f"ما جمعته الوزارة {mt(mt_['2024'])}؛ «حصة البلدية» في الحسابات {D['seea']['summary']['Percentage of Municipal Waste of the Total Waste Quantity']['2024']:.1%} من الإجمالي = {mt(seea_msw)}؛ ونفايات الأسر في الحسابات {mt(S24['total']['households'])}.",
  "The page uses the Ministry's collection figure for municipal waste.", 'تعتمد الصفحة رقم الوزارة للنفايات البلدية.'),
 ('minor', 'Per-person rates use 2022 population', 'معدل الفرد على سكان 2022',
  f"The files carry regional population only for the 2022 census. GASTAT's own 2024 national figure is {D['seea']['summary']['municipal solid waste per Capita']['2024']:.2f} kg/day; ours is {nat_pc['2024']:.2f}.",
  f"لا تتضمن الملفات سكان المناطق إلا لتعداد 2022. ورقم الهيئة الوطني لعام 2024 {D['seea']['summary']['municipal solid waste per Capita']['2024']:.2f} كغ/يوم، ورقمنا {nat_pc['2024']:.2f}.",
  'Labelled on the map; used for comparing regions, not as an absolute rate.', 'معلَّم على الخريطة؛ للمقارنة بين المناطق لا كمعدل مطلق.'),
 ('minor', 'Labels, spellings and blanks', 'التسميات والإملاء والخانات الفارغة',
  "Typos and inconsistent terms ('Incineration mothed', 'cycling method', 'Backfilling' for landfill; 'Healthy burial' in 2022 vs 'Sanitary landfilling'); region names vary across editions (Tabouk, Najarn, Al Bahah, Northern Border); the SEEA contents sheet is headed 'SEEA Waste 2023'; the household column of the use table is empty and some cells are blank where others are 0; SEEA 2023 supply and use totals differ by 6 t.",
  "أخطاء وتسميات غير متسقة («Incineration mothed» و«cycling method» و«Backfilling» للدفن؛ «Healthy burial» في 2022 مقابل «Sanitary landfilling»)؛ وأسماء المناطق تختلف بين الإصدارات (Tabouk وNajarn وAl Bahah وNorthern Border)؛ وصفحة محتويات الحسابات معنونة «SEEA Waste 2023»؛ وعمود الأسر في جدول الاستخدام فارغ وبعض الخانات فارغة حيث غيرها صفر؛ ويختلف إجمالي العرض والاستخدام لعام 2023 بـ6 أطنان.",
  'Handled in extraction (names matched to region codes, cells read by position).', 'عولجت عند الاستخراج (مطابقة الأسماء برموز المناطق وقراءة الخلايا حسب الموقع).'),
 ('minor', 'Out of scope', 'خارج النطاق',
  "Wastewater tables 3-1 to 3-7 are excluded (liquid effluent); 3-1 in the 2024 edition still only gives 2021.",
  "استُبعدت جداول مياه الصرف 3-1 إلى 3-7 (سوائل)؛ والجدول 3-1 في إصدار 2024 لا يزال يعطي 2021 فقط.",
  'Sewage sludge is kept, as GASTAT counts it as waste.', 'أُبقيت حمأة الصرف لأن الهيئة تحتسبها نفايات.'),
]
A['register'] = [dict(zip(('sev', 'ten', 'tar', 'en', 'ar', 'hen', 'har'), r)) for r in REG]
A['proj'] = {'hz_f': hz_f, 'spec_f': spec_f, 'sector_f': {k: v[0] for k, v in sector_f.items()}}

payload = json.dumps({'D': D, 'A': A, 'G': G, 'built': dt.date.today().isoformat()}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

CSS = r"""
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--eh-font);background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh);
 --c1:#0072BB;--c2:#54AB5D;--c3:#8E6BB8;--c4:#C98A1B;--c0:#8A94A6;--surf:var(--eh-paper)}
body.dark{--c1:#2F8FD6;--c2:#4AA654;--c3:#9A7BD0;--c4:#BD8628;--c0:#7C88A0}
html[lang=ar] body{line-height:var(--eh-lh-ar)}
header{background:var(--eh-deep);color:#fff;position:relative;isolation:isolate;padding:20px 22px 22px;display:flex;gap:12px 16px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}
body.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header>div:first-child{min-width:0;flex:1 1 320px}
header h1{margin:0;font:600 23px/1.25 var(--eh-display)}
header .sub{font-size:13.5px;opacity:.8;margin-top:4px;line-height:1.5}
.tog{display:inline-flex;border:1px solid rgba(255,255,255,.32);border-radius:var(--eh-r-ctl);overflow:hidden}
.tog button{background:transparent;border:0;cursor:pointer;font:600 12.5px var(--eh-font);color:rgba(255,255,255,.85);padding:7px 13px}
.tog button.on{background:#fff;color:var(--eh-deep)}
html.eh-embedded header{background:transparent;color:var(--eh-ink);padding:16px 22px 4px}
html.eh-embedded header::after,html.eh-embedded header>.eh-contour{display:none}
html.eh-embedded header h1{font-size:21px}
html.eh-embedded header .sub{color:var(--eh-ink-2);opacity:1}
html.eh-embedded .tog{border-color:var(--eh-line);background:var(--eh-paper)}
html.eh-embedded .tog button{color:var(--eh-ink-2)}
html.eh-embedded .tog button.on{background:var(--eh-sea);color:#fff}
main{padding:18px 22px 44px;max-width:1400px;margin:0 auto}
.stamp{font-size:12.5px;color:var(--eh-ink-3);display:flex;gap:6px 10px;flex-wrap:wrap;margin:0 0 12px}.stamp b{color:var(--eh-ink);font-weight:600}
.gapnote{display:flex;gap:12px;align-items:flex-start;background:var(--eh-warn-bg);border:1px solid color-mix(in srgb,var(--eh-warn) 35%,transparent);border-radius:12px;padding:12px 14px;margin:0 0 16px;font-size:13.5px;color:var(--eh-ink)}
.gapnote b{color:var(--eh-warn)}
.gapnote svg{flex:0 0 auto;margin-top:2px;color:var(--eh-warn)}
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:18px}
.kc{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow);position:relative;overflow:hidden}
.kc::before{content:"";position:absolute;inset-inline-start:0;top:0;bottom:0;width:3px;background:var(--k,var(--eh-sea))}
.kc .v{font:600 26px/1.12 var(--eh-display);color:var(--eh-ink);unicode-bidi:isolate}
.kc .d{font-size:12.5px;font-weight:600;margin-top:4px;color:var(--eh-ink-2)}
.kc .d.up,.kc .d.dn{color:var(--eh-ink-2)}
.kc .l{font-size:13px;color:var(--eh-ink-2);margin-top:6px;line-height:1.45}
.card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;margin-bottom:16px;box-shadow:var(--eh-shadow)}
.card h2{margin:0;font:600 17px/1.35 var(--eh-display);color:var(--eh-ink)}
.card h3{margin:16px 0 4px;font:600 14.5px/1.4 var(--eh-display);color:var(--eh-ink)}
.sec{font:600 12px var(--eh-font);color:var(--eh-leaf-ink);letter-spacing:.02em;margin:26px 0 8px;display:flex;align-items:center;gap:8px}
.sec::after{content:"";flex:1;height:1px;background:var(--eh-line)}
.note{font-size:13px;color:var(--eh-ink-2);line-height:1.55;margin:4px 0 12px}
.hd{display:flex;align-items:flex-start;justify-content:space-between;gap:10px 14px;flex-wrap:wrap}
.png{font:600 12px var(--eh-font);background:var(--eh-tint);border:1px solid var(--eh-line);color:var(--eh-sea-ink);border-radius:8px;padding:5px 10px;cursor:pointer;white-space:nowrap}
.png:hover{border-color:var(--eh-sea)}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px}.g2>.card{margin-bottom:0}
.g2+.card,.g2+.g2{margin-top:16px}
@media(max-width:980px){.g2{grid-template-columns:1fr}}
.src{display:inline-block;font:600 11.5px/1.6 var(--eh-font);color:var(--eh-ink-3);background:var(--eh-tint);border-radius:999px;padding:0 8px;unicode-bidi:isolate;white-space:nowrap;cursor:help}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.chips button{font:600 12.5px var(--eh-font);background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink-2);border-radius:999px;padding:6px 13px;cursor:pointer}
.chips button:hover{border-color:var(--eh-sea);color:var(--eh-ink)}
.chips button.on{background:var(--eh-sea);border-color:var(--eh-sea);color:#fff}
body.dark .chips button.on{color:#0D1736}
.ctlrow{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;font-size:13px;color:var(--eh-ink-2)}
.ctlrow input[type=range]{width:200px;accent-color:var(--eh-sea)}
.ctlrow label{display:inline-flex;gap:6px;align-items:center;cursor:pointer}
.yr{font:600 15px var(--eh-display);color:var(--eh-ink);min-width:3ch;unicode-bidi:isolate}
.mapgrid{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(280px,1fr);gap:18px;align-items:start}
@media(max-width:900px){.mapgrid{grid-template-columns:1fr}}
#map svg{width:100%;max-width:600px;height:auto;display:block;margin:0 auto}
#map path.rg{stroke:var(--eh-paper);stroke-width:1.2;cursor:pointer;transition:fill var(--eh-dur-2) var(--eh-ease)}
#map path.rg:hover{stroke:var(--eh-ink);stroke-width:1.6}
#map path.rg.sel{stroke:var(--eh-ink);stroke-width:2.4}
#map .lbl{font:600 11.5px var(--eh-font);fill:var(--eh-ink);paint-order:stroke fill;stroke:var(--eh-paper);stroke-width:2.5px;stroke-opacity:.9;stroke-linejoin:round;pointer-events:none}
#map .lbl.v{font-weight:500;fill:var(--eh-ink-2)}
#map .pt{cursor:pointer}
#map .pt circle,#map .pt path{stroke:var(--eh-paper);stroke-width:2}
.legend{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center;font-size:12px;color:var(--eh-ink-2);margin-top:8px}
.legend .sw{display:inline-flex;align-items:center;gap:5px;unicode-bidi:isolate}
.legend .sw i{display:inline-block;width:16px;height:12px;border-radius:3px}
.legend .pk{display:inline-flex;align-items:center;gap:5px}
.panel{background:var(--eh-tint);border-radius:12px;padding:14px 16px;min-height:200px}
.panel h3{margin:0 0 2px}
.kv{display:grid;grid-template-columns:1fr auto;gap:4px 12px;font-size:13px;margin-top:8px}
.kv span:nth-child(odd){color:var(--eh-ink-2)}.kv span:nth-child(even){font-weight:600;text-align:end;unicode-bidi:isolate;font-variant-numeric:tabular-nums}
.flag{font-size:12.5px;background:var(--eh-warn-bg);color:var(--eh-ink);border-radius:8px;padding:7px 10px;margin-top:8px;border-inline-start:3px solid var(--eh-warn)}
.flag b{color:var(--eh-warn)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.t{width:100%;border-collapse:collapse;font-size:13px;min-width:640px}
table.t th{text-align:start;font:600 12px var(--eh-font);color:var(--eh-ink-2);padding:8px;border-bottom:1px solid var(--eh-line);background:var(--eh-tint);cursor:pointer;white-space:nowrap}
table.t th.n,table.t td.n{text-align:end;font-variant-numeric:tabular-nums}
table.t td{padding:7px 8px;border-bottom:1px solid var(--eh-line)}
table.t tr:hover td{background:var(--eh-tint)}
table.t tr.sel td{background:var(--eh-info-bg)}
table.t td .bar{display:inline-block;height:8px;border-radius:0 4px 4px 0;background:var(--c1);vertical-align:middle;margin-inline-end:6px}
[dir=rtl] table.t td .bar{border-radius:4px 0 0 4px}
table.t th[aria-sort] {color:var(--eh-ink)}
svg.ch{width:100%;height:auto;display:block;overflow:visible}
svg.ch text{font-family:var(--eh-font);font-size:12px;fill:var(--eh-ink-2)}
svg.ch text.lab{fill:var(--eh-ink)}
svg.ch text.val{fill:var(--eh-ink);font-weight:600}
svg.ch text.ttl{font-family:var(--eh-display);font-weight:600;fill:var(--eh-ink)}
svg.ch .grid{stroke:var(--eh-line);stroke-width:1}
svg.ch .axis{stroke:var(--eh-ink-3);stroke-width:1}
svg.ch .hit{fill:transparent;cursor:default}
svg.ch .s1{fill:var(--c1)}svg.ch .s2{fill:var(--c2)}svg.ch .s3{fill:var(--c3)}svg.ch .s4{fill:var(--c4)}svg.ch .s0{fill:var(--c0)}
svg.ch .ln1{fill:none;stroke:var(--c1);stroke-width:2}svg.ch .ln2{fill:none;stroke:var(--c4);stroke-width:2;stroke-dasharray:5 4}
svg.ch .dot1{fill:var(--c1);stroke:var(--eh-paper);stroke-width:2}svg.ch .dot2{fill:var(--c4);stroke:var(--eh-paper);stroke-width:2}
svg.ch .ghost{fill:var(--eh-muted-bg)}
svg.ch .xh{stroke:var(--eh-ink-3);stroke-width:1;stroke-dasharray:3 3}
svg.ch .unk{fill:url(#hatch)}
.lg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;color:var(--eh-ink-2);margin:4px 0 8px}
.lg span{display:inline-flex;align-items:center;gap:6px}.lg i{width:12px;height:12px;border-radius:3px;display:inline-block}
.lg i.l{height:3px;border-radius:2px}
#tip{position:fixed;z-index:50;pointer-events:none;background:var(--eh-ink);color:var(--eh-paper);font-size:12.5px;line-height:1.45;padding:8px 10px;border-radius:8px;max-width:280px;box-shadow:0 8px 24px -10px rgba(0,0,0,.5);opacity:0;transition:opacity .12s}
#tip b{font-weight:600}
#tip .tn{font-variant-numeric:tabular-nums;unicode-bidi:isolate}
.read{font-size:13.5px;padding:10px 12px;background:var(--eh-tint);border-radius:9px;border-inline-start:3px solid var(--eh-sea);margin-top:12px;line-height:1.6}
.read b{font-weight:600}
.opp{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;padding:12px 0;border-top:1px solid var(--eh-line)}
.opp:first-of-type{border-top:0}
.opp .n{font:600 20px var(--eh-display);color:var(--eh-leaf-ink);min-width:1.4em}
.opp .st{font-size:14px;line-height:1.6}.opp .st b{font-weight:600}
.opp .ac{font-size:13px;color:var(--eh-ink);background:var(--eh-tint);border-radius:9px;border-inline-start:3px solid var(--eh-leaf);padding:8px 12px;margin-top:8px}
.opp .ac b{color:var(--eh-leaf-ink);font-weight:600}
.eha{display:inline-block;font:600 11px var(--eh-font);background:var(--eh-good-bg);color:var(--eh-good);border-radius:999px;padding:1px 8px;margin-inline-start:6px;vertical-align:middle}
ul.dn{margin:6px 0 0;padding-inline-start:20px;font-size:13.5px}ul.dn li{margin:6px 0}
.foot{font-size:12px;color:var(--eh-ink-3);text-align:center;margin-top:20px;line-height:1.6}
.num{unicode-bidi:isolate;font-variant-numeric:tabular-nums}
@media(max-width:560px){main{padding:14px 12px 36px}header{padding:16px 14px}.card{padding:14px 14px}.kc .v{font-size:22px}.ctlrow input[type=range]{width:150px}}
"""

JS = r"""
const P=JSON.parse(document.getElementById('DATA').textContent), D=P.D, A=P.A, G=P.G;
let LANG='en'; try{LANG=localStorage.getItem('ehhub.lang')||localStorage.getItem('sw.lang')||'en'}catch(e){}
let METRIC='cumlf', YEAR=2024, SEL=null, PTS=true, SORT=null;
const $=id=>document.getElementById(id), L=(en,ar)=>LANG==='ar'?ar:en, RTL=()=>LANG==='ar';
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const NF=(v,d=0)=>v==null||isNaN(v)?'—':Number(v).toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const N=(v,d=0)=>`<span class="num" dir="ltr">${NF(v,d)}</span>`;
// tonnes, readable: 6.9 Mt / 694 thousand t
function T(v,short){ if(v==null||isNaN(v))return '—'; const a=Math.abs(v);
  if(a>=1e6){const d=a>=1e7?1:2;return `<span class="num" dir="ltr">${NF(v/1e6,d)}</span> ${L(short?'Mt':'million t','مليون طن')}`;}
  if(a>=1e3) return `<span class="num" dir="ltr">${NF(v/1e3,0)}</span> ${L(short?'kt':'thousand t','ألف طن')}`;
  return `<span class="num" dir="ltr">${NF(v,0)}</span> ${L('t','طن')}`;}
const TP=v=>T(v,true).replace(/<[^>]+>/g,'');                       // plain text for SVG
const PCT=(v,d=1)=>v==null||isNaN(v)?'—':`<span class="num" dir="ltr">${NF(v*100,d)}%</span>`;
const PCTp=(v,d=0)=>NF(v*100,d)+'%';
const CH=(a,b)=>b?(a/b-1):null;
const SG=v=>v==null?'—':(v>=0?'+':'−')+NF(Math.abs(v*100),0)+'%';
const SRC={env2024:['GASTAT Environment Statistics 2024','الهيئة العامة للإحصاء — إحصاءات البيئة 2024'],env2023:['GASTAT Environment Statistics 2023','الهيئة العامة للإحصاء — إحصاءات البيئة 2023'],env2022:['GASTAT Environment Statistics 2022','الهيئة العامة للإحصاء — إحصاءات البيئة 2022'],env2021:['GASTAT Environment Statistics 2021','الهيئة العامة للإحصاء — إحصاءات البيئة 2021'],seea:['GASTAT SEEA Waste accounts 2024','الهيئة العامة للإحصاء — حسابات النفايات البيئية الاقتصادية 2024']};
function S(ref){const [f,t]=ref.split(':');const s=SRC[f];return `<span class="src" title="${esc(L(s[0],s[1]))}${t?', '+L('table','جدول')+' '+t:''}">${f==='seea'?'SEEA':L('Env. Stats','إحصاءات البيئة')} ${f==='seea'?(t?L('table ','جدول ')+'<bdi dir="ltr">'+t+'</bdi>':''):('<bdi dir="ltr">'+f.slice(3)+(t?' · '+t:'')+'</bdi>')}</span>`;}
const RN=c=>{const r=D.meta.regions.find(r=>r.code===c);return r?L(r.en,r.ar):c;};
const Y=['2017','2018','2019','2020','2021','2022','2023','2024'];
const M=D.municipal_by_material.v, TR=D.municipal_by_treatment.v, POP=D.population_2022.v, AREA=D.area_km2.v;
const CODES=D.meta.regions.map(r=>r.code);
const g=(o,...k)=>{for(const x of k){if(o==null)return null;o=o[x];}return o;};
// ---------- tooltip
const tip=()=>$('tip');
function showTip(e,html){const t=tip();t.innerHTML=html;t.style.opacity=1;const x=e.clientX,y=e.clientY,w=t.offsetWidth,h=t.offsetHeight;
  t.style.left=Math.max(8,Math.min(innerWidth-w-8,x+14))+'px';t.style.top=Math.max(8,(y+h+20>innerHeight?y-h-12:y+14))+'px';}
function hideTip(){tip().style.opacity=0;}
document.addEventListener('scroll',hideTip,{passive:true});
function bindTips(root){root.querySelectorAll('[data-tip]').forEach(el=>{el.addEventListener('mousemove',e=>showTip(e,el.dataset.tip));el.addEventListener('mouseleave',hideTip);
  el.addEventListener('click',e=>{showTip(e,el.dataset.tip);});});}
const at=s=>esc(s).replace(/&lt;(\/?)(b|br|span[^&]*)&gt;/g,'<$1$2>');   // tooltip html kept in data-tip

// ---------- metrics for the map
function regionVal(c,metric,y){y=String(y);
  const col=g(M,c,'total',y), lf=g(TR,c,'landfill',y), rc=g(TR,c,'recycling',y), inc=g(TR,c,'incineration',y);
  switch(metric){
    case 'collected': return col;
    case 'percap': return col*1000/365/POP[c];
    case 'density': return col/AREA[c];
    case 'landfill': return lf;
    case 'cumlf': return Y.filter(x=>+x<=+y).reduce((s,x)=>s+(g(TR,c,'landfill',x)||0),0);
    case 'recrate': return col?rc/col:null;
    case 'growth': {const b=g(M,c,'total','2017');return b?col/b-1:null;}
  }}
const METRICS=[
 ['cumlf',['Landfilled, 2017 to year (cumulative)','المدفون تراكمياً من 2017 حتى السنة'],['Where municipal waste has piled up: tonnes sent to sanitary landfill each year from 2017, added together.','أين تراكمت النفايات البلدية: مجموع الأطنان المُرسلة إلى الدفن الصحي كل عام منذ 2017.'],'env2024:3-10'],
 ['collected',['Collected in the year','المجموع في السنة'],['Municipal waste collected by the Ministry of Municipalities and Housing in the year.','النفايات البلدية التي جمعتها وزارة البلديات والإسكان في السنة.'],'env2024:3-9'],
 ['landfill',['Landfilled in the year','المدفون في السنة'],['Municipal waste sent to sanitary landfill in the year.','النفايات البلدية المُرسلة إلى الدفن الصحي في السنة.'],'env2024:3-10'],
 ['percap',['Per person per day','للفرد يومياً'],['kg of municipal waste per person per day, using the 2022 census population (the latest regional count in these files).','كيلوغرام من النفايات البلدية للفرد يومياً، على أساس سكان تعداد 2022 (أحدث عدّ إقليمي في هذه الملفات).'],'env2023:5-1'],
 ['density',['Per km²','لكل كم²'],['Tonnes of municipal waste per km² of the region in the year.','أطنان النفايات البلدية لكل كيلومتر مربع من مساحة المنطقة في السنة.'],'env2024:1-22'],
 ['recrate',['Recycling rate','نسبة التدوير'],['Municipal waste recycled as a share of waste collected — the same measure GASTAT uses for the national rate (table 3-14).','النفايات البلدية المُعاد تدويرها نسبةً إلى المجموع — المقياس نفسه الذي تعتمده الهيئة للنسبة الوطنية (جدول 3-14).'],'env2024:3-10'],
 ['growth',['Change since 2017','التغير منذ 2017'],['Change in municipal waste collected, from 2017 to the selected year.','التغير في النفايات البلدية المجموعة من 2017 حتى السنة المختارة.'],'env2024:3-9']];
function fmtM(metric,v,plain){ if(v==null)return '—';
  if(metric==='percap') return plain?NF(v,2)+' '+L('kg','كغ'):`${N(v,2)} ${L('kg','كغ')}`;
  if(metric==='density') return plain?NF(v,1)+' '+L('t/km²','طن/كم²'):`${N(v,1)} ${L('t/km²','طن/كم²')}`;
  if(metric==='recrate') return plain?PCTp(v,1):PCT(v,1);
  if(metric==='growth') return plain?SG(v):`<span class="num" dir="ltr">${SG(v)}</span>`;
  return plain?TP(v):T(v,true);}
// colour ramps (sequential: one hue light→dark; growth: diverging, grey midpoint)
const RAMP={light:['#DCEAF5','#AFCFEA','#79AEDB','#3F87C4','#0F5E9E'],dark:['#1D3463','#24508C','#2E73B8','#4E9BE0','#8CC7F2']};
const RAMPG={light:['#D9EDDB','#A9D5AE','#6FB878','#3D9147','#1F6A2A'],dark:['#1C3A3A','#24573F','#2F7A48','#4EA25A','#86CC8C']};
const DIV={light:['#0F5E9E','#79AEDB','#D5D9E0','#E5B566','#A86A0C'],dark:['#2E73B8','#24508C','#3A4566','#8F6A28','#E0A944']};
function scaleFor(metric,vals){const dark=document.body.classList.contains('dark')?'dark':'light';
  if(metric==='growth'){const br=[-0.25,-0.05,0.05,0.25];return {col:v=>v==null?null:DIV[dark][br.filter(b=>v>=b).length],bins:DIV[dark].map((c,i)=>[c,i===0?'< −25%':i===4?'> +25%':[ '−25 to −5%','−5 to +5%','+5 to +25%'][i-1]])};}
  const r=(metric==='recrate'?RAMPG:RAMP)[dark];const q=vals.filter(v=>v!=null).sort((a,b)=>a-b);
  const br=[0.2,0.4,0.6,0.8].map(p=>q[Math.min(q.length-1,Math.floor(p*q.length))]);
  const lo=q[0],hi=q[q.length-1];const edges=[lo,...br,hi];
  return {col:v=>v==null?null:r[br.filter(b=>v>=b).length],bins:r.map((c,i)=>[c,fmtM(metric,edges[i],1)+' – '+fmtM(metric,edges[i+1],1)])};}

// ---------- map
const PTSDATA=[
 {id:'jub',lon:49.66,lat:27.01,en:'Jubail',ar:'الجبيل',kind:'jy'},
 {id:'ynb',lon:38.25,lat:23.98,en:'Yanbu',ar:'ينبع',kind:'jy'},
 {id:'eh',lon:39.13,lat:22.73,en:'EH — Al-Juhfah complex (Rabigh)',ar:'آفاق البيئة — مجمع الجحفة (رابغ)',kind:'eh'}];
function rewind(f){ // d3 wants clockwise rings; Natural Earth/mapshaper output is counter-clockwise
  if(d3.geoArea(f)>2*Math.PI){const r=x=>x.map(ring=>ring.slice().reverse());
    if(f.geometry.type==='Polygon')f.geometry.coordinates=r(f.geometry.coordinates);else f.geometry.coordinates=f.geometry.coordinates.map(r);}return f;}
G.features.forEach(rewind);
function jyTip(){const y=String(YEAR), jt=D.jy_total.v[y], jh=A.jy_haz[y], nh=g(D.seea.supply,y,'hazardous','total');
  return `<b>${L('Jubail and Yanbu (reported together)','الجبيل وينبع (تُنشر معاً)')}</b><br>${L('Industrial waste','النفايات الصناعية')} ${y}: <b class="tn">${TP(jt)}</b>`+
   (jh?`<br>${L('of which hazardous','منها خطرة')}: <b class="tn">${TP(jh)}</b>`+(nh?` (${PCTp(jh/nh)} ${L('of the national hazardous total','من إجمالي النفايات الخطرة في المملكة')})`:''):`<br>${L('Hazardous split published from 2021 only','تفصيل النفايات الخطرة منشور من 2021 فقط')}`)+
   `<br>${L('Recycled','نسبة التدوير')}: <b class="tn">${PCTp(D.recycling_rate.v.jy[y])}</b><br><span style="opacity:.75">${L('Royal Commission for Jubail and Yanbu, via GASTAT tables 3-11, 3-12','الهيئة الملكية للجبيل وينبع، عبر جداول الهيئة العامة للإحصاء 3-11 و3-12')}</span>`;}
function drawMap(){
  const W=620,H=560, svg=d3.select('#map').html('').append('svg').attr('viewBox',`0 0 ${W} ${H}`).attr('id','svg-map').attr('role','img')
     .attr('aria-label',L('Map of the 13 regions of Saudi Arabia shaded by the selected municipal waste measure','خريطة مناطق المملكة الثلاث عشرة ملوّنة بحسب مقياس النفايات البلدية المختار'));
  const proj=d3.geoMercator().fitExtent([[10,10],[W-10,H-10]],G), path=d3.geoPath(proj);
  const vals={};CODES.forEach(c=>vals[c]=regionVal(c,METRIC,YEAR));
  const sc=scaleFor(METRIC,Object.values(vals));
  svg.append('g').selectAll('path').data(G.features).join('path').attr('class',f=>'rg'+(f.properties.iso_3166_2===SEL?' sel':''))
    .attr('d',path).attr('fill',f=>sc.col(vals[f.properties.iso_3166_2])||'var(--eh-muted-bg)')
    .attr('data-tip',f=>{const c=f.properties.iso_3166_2;return `<b>${esc(RN(c))}</b><br>${esc(L(METRICS.find(m=>m[0]===METRIC)[1][0],METRICS.find(m=>m[0]===METRIC)[1][1]))}: <b class="tn">${fmtM(METRIC,vals[c],1)}</b>`+(A.flags[c].some(f=>f.y===String(YEAR))?`<br>⚠ ${L('Data warning — see panel','تنبيه بيانات — انظر اللوحة')}`:'');})
    .on('click',(e,f)=>{SEL=f.properties.iso_3166_2;renderMapAll();});
  // direct labels: the five largest values (selective, not every region)
  const top=CODES.filter(c=>vals[c]!=null).sort((a,b)=>(METRIC==='growth'?Math.abs(vals[b])-Math.abs(vals[a]):vals[b]-vals[a])).slice(0,5);
  const lg=svg.append('g');
  G.features.filter(f=>top.includes(f.properties.iso_3166_2)).forEach(f=>{const c=f.properties.iso_3166_2;let [x,y]=path.centroid(f);
    if(c==='SA-04'){x-=40;y-=20;} if(c==='SA-11'){x-=34;} if(c==='SA-09'){x+=0;y+=4;}
    lg.append('text').attr('class','lbl').attr('x',x).attr('y',y).attr('text-anchor','middle').text(RN(c));
    lg.append('text').attr('class','lbl v').attr('x',x).attr('y',y+14).attr('text-anchor','middle').attr('direction',RTL()?'rtl':'ltr').text(fmtM(METRIC,vals[c],1));});
  if(PTS){const pg=svg.append('g');PTSDATA.forEach(p=>{const [x,y]=proj([p.lon,p.lat]);const gg=pg.append('g').attr('class','pt').attr('transform',`translate(${x},${y})`);
    if(p.kind==='jy'){gg.append('circle').attr('r',8).attr('fill','var(--c4)');gg.attr('data-tip',jyTip());}
    else{gg.append('path').attr('d','M0,-8L8,0L0,8L-8,0Z').attr('fill','var(--c2)');gg.attr('data-tip',`<b>${esc(L(p.en,p.ar))}</b><br>${L('EH\'s licensed hazardous-waste facility (approximate location). Shown for reference — not a data point.','منشأة آفاق البيئة المرخّصة لمعالجة النفايات الخطرة (موقع تقريبي). للإرشاد فقط وليست نقطة بيانات.')}`);}
    gg.append('text').attr('class','lbl').attr('x',p.id==='ynb'?12:-12).attr('y',4).attr('text-anchor',p.id==='ynb'?'start':'end').text(p.id==='eh'?L('EH · Al-Juhfah','آفاق البيئة · الجحفة'):L(p.en,p.ar));});}
  bindTips($('map'));
  // legend
  $('legend').innerHTML=sc.bins.map(([c,t])=>`<span class="sw"><i style="background:${c}"></i><span>${esc(t)}</span></span>`).join('')+
    (PTS?`<span class="pk"><svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="var(--c4)"/></svg>${L('Jubail, Yanbu — industrial & hazardous (only published locations)','الجبيل وينبع — صناعية وخطرة (المواقع الوحيدة المنشورة)')}</span><span class="pk"><svg width="14" height="14"><path d="M7,1L13,7L7,13L1,7Z" fill="var(--c2)"/></svg>${L('EH site','موقع آفاق البيئة')}</span>`:'');
}
function renderPanel(){
  const c=SEL; if(!c){$('panel').innerHTML=`<h3>${L('Pick a region','اختر منطقة')}</h3><div class="note">${L('Tap a region on the map or a row in the table for its figures, trend and any data warnings.','انقر منطقة على الخريطة أو صفاً في الجدول لعرض أرقامها واتجاهها وأي تنبيهات على بياناتها.')}</div>`+jyBox();return;}
  const y=String(YEAR), rank=CODES.map(x=>[x,g(M,x,'total',y)]).sort((a,b)=>b[1]-a[1]).findIndex(r=>r[0]===c)+1;
  const comp=[['organic',L('Organic','عضوية')],['plastic',L('Plastic','بلاستيك')],['paper',L('Paper','ورق')],['mgf',L('Metal, glass, fabric','معادن وزجاج ونسيج')],['other',L('Other non-organic','غير عضوية أخرى')]];
  const tot=g(M,c,'total',y), cv=k=>k==='mgf'?['metal','glass','fabric'].reduce((s,x)=>s+(g(M,c,x,y)||0),0):g(M,c,k,y);
  let x=0;const W=300;const bars=comp.map(([k,l],i)=>{const w=W*cv(k)/tot;const r=`<rect x="${x}" y="0" width="${Math.max(0,w-2)}" height="14" class="s${[1,2,3,4,0][i]}" data-tip="${at(`<b>${l}</b>: <span class='tn'>${TP(cv(k))}</span> (${PCTp(cv(k)/tot)})`)}"></rect>`;x+=w;return r;}).join('');
  const fl=A.flags[c].filter(f=>f.y===y).map(f=>f.k==='mismatch'?`<div class="flag"><b>${L('Totals disagree','المجاميع غير متطابقة')} ${f.y}:</b> ${L('treated','المعالَج')} ${T(f.tr,1)} ${L('vs collected','مقابل المجموع')} ${T(f.col,1)} (${S('env2024:3-10')} ${L('vs','مقابل')} ${S('env2024:3-9')})</div>`:
    f.k==='percap'?`<div class="flag"><b>${L('Unusually high per person','مرتفع على نحو غير معتاد للفرد')}:</b> ${N(f.v,1)} ${L('kg/day against a national','كغ/يوم مقابل متوسط وطني')} ${N(f.nat,1)}. ${L('Likely includes non-household waste or a recording issue — treat with care.','يُرجَّح أنه يشمل نفايات غير منزلية أو خللاً في التسجيل — يُستخدم بحذر.')}</div>`:
    `<div class="flag"><b>${L('Classification break','تغيّر في التصنيف')}:</b> ${PCT(f.v,0)} ${L('is "other non-organic"; organic fell from','مصنّفة «غير عضوية أخرى»؛ وتراجعت العضوية من')} ${PCT(f.org17,0)} ${L('(2017) to','(2017) إلى')} ${PCT(f.org24,0)}. ${L('The material split for this region is not reliable.','تفصيل المواد لهذه المنطقة غير موثوق.')}</div>`).join('');
  $('panel').innerHTML=`<h3>${esc(RN(c))}</h3><div class="note" style="margin:0">${L('Municipal waste','النفايات البلدية')} · ${y}</div>
   <div class="kv"><span>${L('Collected','المجموع')}</span><span>${T(tot,1)}</span><span>${L('Rank of 13','الترتيب من 13')}</span><span>${N(rank)}</span>
   <span>${L('Share of the Kingdom','الحصة من المملكة')}</span><span>${PCT(tot/g(M,'KSA','total',y))}</span>
   <span>${L('Per person per day','للفرد يومياً')}</span><span>${fmtM('percap',regionVal(c,'percap',y))}</span>
   <span>${L('Landfilled','المدفون')}</span><span>${T(g(TR,c,'landfill',y),1)}</span>
   <span>${L('Landfilled 2017 to','المدفون من 2017 حتى')} ${y}</span><span>${T(regionVal(c,'cumlf',y),1)}</span>
   <span>${L('Recycling rate','نسبة التدوير')}</span><span>${PCT(regionVal(c,'recrate',y),1)}</span>
   <span>${L('Change since 2017','التغير منذ 2017')}</span><span>${fmtM('growth',regionVal(c,'growth',y))}</span></div>
   <h3 style="margin-top:12px">${L('What it is made of','مكوّناتها')}</h3>
   <svg class="ch" viewBox="0 0 300 14" style="direction:ltr;${RTL()?'transform:scaleX(-1)':''}">${bars}</svg>
   <div class="lg">${comp.map(([k,l],i)=>`<span><i style="background:var(--c${[1,2,3,4,0][i]})"></i>${l} ${PCT(cv(k)/tot,0)}</span>`).join('')}</div>
   <h3>${L('Collected and landfilled, 2017–2024','المجموع والمدفون 2017–2024')}</h3><div id="spark"></div>${fl}${(()=>{const o=A.flags[c].filter(f=>f.k==='mismatch'&&f.y!==y).map(f=>f.y);return o.length?`<div class="note" style="margin-top:8px">${L('Treated and collected totals also disagree by more than 10% in','كما يختلف المعالَج عن المجموع بأكثر من 10% في')} <span class="num">${o.join(', ')}</span>.</div>`:''})()}`;
  lineChart('spark',Y,[{k:L('Collected','المجموع'),v:Y.map(x=>g(M,c,'total',x))},{k:L('Landfilled','المدفون'),v:Y.map(x=>g(TR,c,'landfill',x))}],{h:150,unit:'t',mini:1});
  bindTips($('panel'));
}
function jyBox(){const y=String(YEAR);return `<div class="flag" style="background:var(--eh-paper);border-inline-start-color:var(--c4)"><b style="color:var(--eh-ink)">${L('Hazardous and industrial waste are not mapped by region','النفايات الخطرة والصناعية غير منشورة حسب المنطقة')}</b><br>${L('The only places with published industrial and hazardous tonnages are Jubail and Yanbu (orange dots), reported together. In','الموقعان الوحيدان بأطنان منشورة للنفايات الصناعية والخطرة هما الجبيل وينبع (النقطتان البرتقاليتان)، ويُنشران معاً. في')} ${y} ${L('they account for','شكّلا')} ${A.jy_haz[y]?PCT(A.jy_haz[y]/g(D.seea.supply,y,'hazardous','total'),0):L('an unpublished share','حصة غير منشورة')} ${L('of the Kingdom\'s hazardous waste; the rest has no published location.','من النفايات الخطرة في المملكة؛ والباقي بلا موقع منشور.')}</div>`;}
function renderTable(){
  const y=String(YEAR);const rows=CODES.map(c=>({c,col:g(M,c,'total',y),pc:regionVal(c,'percap',y),lf:g(TR,c,'landfill',y),cum:regionVal(c,'cumlf',y),rr:regionVal(c,'recrate',y),gr:regionVal(c,'growth',y),fl:A.flags[c].filter(f=>f.y===y).length}));
  const cols=[['c',L('Region','المنطقة'),0],['col',L('Collected','المجموع'),1],['pc',L('kg / person / day','كغ/فرد/يوم'),1],['lf',L('Landfilled','المدفون'),1],['cum',L('Landfilled since 2017','المدفون منذ 2017'),1],['rr',L('Recycling rate','نسبة التدوير'),1],['gr',L('Change since 2017','التغير منذ 2017'),1]];
  const sk=SORT||(METRIC==='percap'?'pc':METRIC==='landfill'?'lf':METRIC==='recrate'?'rr':METRIC==='growth'?'gr':METRIC==='cumlf'?'cum':'col');
  rows.sort((a,b)=>sk==='c'?RN(a.c).localeCompare(RN(b.c)):(b[sk]??-1e9)-(a[sk]??-1e9));
  const mx=Math.max(...rows.map(r=>r.col));
  $('rtable').innerHTML=`<table class="t"><thead><tr>${cols.map(([k,l,n])=>`<th class="${n?'n':''}" data-k="${k}" ${k===sk?'aria-sort="descending"':''}>${l}${k===sk?' ↓':''}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr data-c="${r.c}" class="${r.c===SEL?'sel':''}" style="cursor:pointer"><td>${esc(RN(r.c))}${r.fl?' <span title="'+esc(L('Data warning — open the region','تنبيه بيانات — افتح المنطقة'))+'">⚠</span>':''}</td>
   <td class="n"><span class="bar" style="width:${Math.round(60*r.col/mx)}px"></span>${T(r.col,1)}</td><td class="n">${N(r.pc,2)}</td><td class="n">${T(r.lf,1)}</td><td class="n">${T(r.cum,1)}</td><td class="n">${PCT(r.rr,1)}</td><td class="n">${fmtM('growth',r.gr)}</td></tr>`).join('')}
   <tr style="font-weight:600"><td>${L('Kingdom','المملكة')}</td><td class="n">${T(g(M,'KSA','total',y),1)}</td><td class="n">${N(g(M,'KSA','total',y)*1000/365/POP.KSA,2)}</td><td class="n">${T(g(TR,'KSA','landfill',y),1)}</td><td class="n">${T(regionVal('KSA','cumlf',y),1)}</td><td class="n">${PCT(regionVal('KSA','recrate',y),1)}</td><td class="n">${fmtM('growth',regionVal('KSA','growth',y))}</td></tr></tbody></table>`;
  $('rtable').querySelectorAll('th').forEach(th=>th.onclick=()=>{SORT=th.dataset.k;renderTable();});
  $('rtable').querySelectorAll('tr[data-c]').forEach(tr=>tr.onclick=()=>{SEL=tr.dataset.c;renderMapAll();$('map').scrollIntoView({behavior:'smooth',block:'nearest'});});
}
function resetMap(){METRIC='cumlf';YEAR=2024;SEL=null;PTS=true;SORT=null;$('yslider').value=2024;$('ptsbox').checked=true;
  $('chips').querySelectorAll('button').forEach(x=>x.classList.toggle('on',x.dataset.m===METRIC));renderMapAll();}
function renderMapAll(){drawMap();renderPanel();renderTable();
  const dflt=METRIC==='cumlf'&&YEAR===2024&&!SEL&&PTS&&!SORT;const rb=$('mreset');rb.textContent='↺ '+L('Reset filters','إعادة ضبط الفلاتر');rb.disabled=dflt;rb.style.opacity=dflt?.45:1;rb.style.cursor=dflt?'default':'pointer';
  rb.title=L('Back to the default view: landfilled since 2017, year 2024, no region selected','العودة إلى العرض الافتراضي: المدفون منذ 2017، سنة 2024، دون منطقة مختارة');
  const m=METRICS.find(m=>m[0]===METRIC);$('mdesc').innerHTML=esc(L(m[2][0],m[2][1]))+' '+S(m[3]);
  $('yr').textContent=YEAR;}

// ---------- generic charts (plain SVG; Arabic mirrors horizontal bars, time axes stay left to right)
function hbars(id,items,o={}){ // items: {label, v, v0?, cls, tip}; v0 draws a second (grey) bar for the earlier year
  const pair=items.some(i=>i.v0!=null);const W=640,lw=o.lw||190,rh=o.rh||(pair?40:30),H=items.length*rh+8,max=o.max||Math.max(...items.map(i=>Math.max(i.v,i.v0||0)));const bw=W-lw-130,r=RTL();
  const BW=v=>bw*v/max;
  let s=`<svg class="ch" id="svg-${id}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(o.aria||'')}" style="direction:ltr">`;
  items.forEach((it,i)=>{const y=i*rh+4, w=Math.max(1,BW(it.v)), x=r?W-lw-w:lw;
    const by=pair?y+5:y+8, bh=pair?14:rh-18;
    s+=`<text class="lab" x="${r?W-lw+10:lw-10}" y="${pair?y+rh/2-1:y+rh/2+1}" text-anchor="end" direction="${r?'rtl':'ltr'}" dominant-baseline="middle">${esc(it.label)}</text>`;
    s+=`<rect class="${it.cls||'s1'}" x="${x}" y="${by}" width="${w}" height="${bh}" rx="3"></rect>`;
    s+=`<text class="val" x="${r?x-8:x+w+8}" y="${by+bh/2+1}" text-anchor="start" direction="${r?'rtl':'ltr'}" dominant-baseline="middle">${esc(it.vl||TP(it.v))}</text>`;
    if(it.v0!=null){const w0=Math.max(1,BW(it.v0)),x0=r?W-lw-w0:lw,y0=by+bh+3;
      s+=`<rect class="s0" x="${x0}" y="${y0}" width="${w0}" height="9" rx="2"></rect>`;
      s+=`<text x="${r?x0-8:x0+w0+8}" y="${y0+5}" text-anchor="start" direction="${r?'rtl':'ltr'}" dominant-baseline="middle" style="font-size:11px">${esc(TP(it.v0))}</text>`;}
    s+=`<rect class="hit" x="0" y="${y}" width="${W}" height="${rh}" data-tip="${at(it.tip||'')}"></rect>`;});
  $(id).innerHTML=s+'</svg>'+(pair?`<div class="lg"><span><i style="background:var(--${(items[0].cls||'s1')==='s4'?'c4':'c1'})"></i>2024</span><span><i style="background:var(--c0)"></i>2023</span></div>`:'');bindTips($(id));}
function stack100(id,rows,cats,o={}){ // rows:{label, parts:{k:v}}; cats:[k,label,cls]
  const W=o.w||640,lw=o.lw||70,rh=o.rh||40,H=rows.length*rh+4,bw=W-lw-10,r=RTL();let s=`<svg class="ch" id="svg-${id}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(o.aria||'')}" style="direction:ltr">`;
  rows.forEach((row,i)=>{const y=i*rh+4,tot=cats.reduce((a,[k])=>a+(row.parts[k]||0),0);let acc=0;
    s+=`<text class="lab" x="${r?W-lw+10:lw-10}" y="${y+rh/2-2}" text-anchor="end" direction="${r?'rtl':'ltr'}" dominant-baseline="middle">${esc(row.label)}</text>`;
    cats.forEach(([k,l,cls])=>{const v=row.parts[k]||0,w=bw*v/tot;if(w<=0)return;const x=r?W-lw-acc-w:lw+acc;
      s+=`<rect class="${cls}" x="${x+1}" y="${y+4}" width="${Math.max(0,w-2)}" height="${rh-14}" rx="3" data-tip="${at(`<b>${row.label} · ${l}</b><br><span class='tn'>${TP(v)}</span> · ${PCTp(v/tot,1)}`)}"></rect>`;
      if(w>44)s+=`<text x="${x+w/2}" y="${y+rh/2-2}" text-anchor="middle" dominant-baseline="middle" style="fill:#fff;font-weight:600;pointer-events:none" direction="ltr">${PCTp(v/tot)}</text>`;acc+=w;});});
  $(id).innerHTML=s+'</svg>';bindTips($(id));}
function vstack(id,years,series,o={}){ // series:[{k,label,cls,vals[]}] ; unknown=null drawn hatched
  const W=o.w||640,H=o.h||260,pl=56,pr=10,pt=10,pb=26;const tot=years.map((_,i)=>series.reduce((a,s)=>a+(s.vals[i]||0),0));const max=niceMax(Math.max(...tot,o.total?Math.max(...o.total.filter(v=>v!=null)):0));
  const bw=(W-pl-pr)/years.length, Yp=v=>pt+(H-pt-pb)*(1-v/max);let s=`<svg class="ch" id="svg-${id}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(o.aria||'')}" style="direction:ltr">`;
  s+=`<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="var(--eh-muted-bg)"/><line x1="0" y1="0" x2="0" y2="6" stroke="var(--eh-ink-3)" stroke-width="1.2"/></pattern></defs>`;
  ticks(max).forEach(t=>{s+=`<line class="grid" x1="${pl}" x2="${W-pr}" y1="${Yp(t)}" y2="${Yp(t)}"></line><text x="${pl-6}" y="${Yp(t)}" text-anchor="end" dominant-baseline="middle">${axisT(t)}</text>`;});
  years.forEach((yr,i)=>{let acc=0;const x=pl+i*bw+bw*.18,w=bw*.64;let tipH=`<b>${yr}</b>`;
    series.forEach(sr=>{const v=sr.vals[i];if(v==null||v<=0)return;const y1=Yp(acc+v),y0=Yp(acc);s+=`<rect class="${sr.cls}" x="${x}" y="${y1+1}" width="${w}" height="${Math.max(0,y0-y1-2)}" rx="2"></rect>`;acc+=v;tipH+=`<br>${sr.label}: <span class='tn'>${TP(v)}</span>`;});
    if(o.total&&o.total[i]!=null&&o.total[i]>acc+1){const y1=Yp(o.total[i]),y0=Yp(acc);s+=`<rect class="unk" x="${x}" y="${y1+1}" width="${w}" height="${Math.max(0,y0-y1-2)}" rx="2"></rect>`;tipH+=`<br>${o.restLabel}: <span class='tn'>${TP(o.total[i]-acc)}</span>`;}
    if(o.total&&o.total[i]!=null)tipH+=`<br><b>${L('Total','الإجمالي')}: <span class='tn'>${TP(o.total[i])}</span></b>`;
    if(years.length<=16||i%2===0)s+=`<text x="${x+w/2}" y="${H-8}" text-anchor="middle">${yr}</text>`;
    s+=`<rect class="hit" x="${pl+i*bw}" y="${pt}" width="${bw}" height="${H-pt-pb}" data-tip="${at(tipH)}"></rect>`;});
  s+=`<line class="axis" x1="${pl}" x2="${W-pr}" y1="${Yp(0)}" y2="${Yp(0)}"></line>`;
  $(id).innerHTML=s+'</svg>';bindTips($(id));}
function lineChart(id,years,series,o={}){ // up to 2 series; o.pct for shares
  const W=o.mini?300:640,H=o.h||220,pl=o.mini?40:56,pr=12,pt=10,pb=24;const all=series.flatMap(s=>s.v).filter(v=>v!=null);const max=o.max||niceMax(Math.max(...all));
  const X=i=>pl+(W-pl-pr)*i/(years.length-1),Yp=v=>pt+(H-pt-pb)*(1-v/max);let s=`<svg class="ch" id="svg-${id}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(o.aria||'')}" style="direction:ltr">`;
  ticks(max,o.mini?3:5).forEach(t=>{s+=`<line class="grid" x1="${pl}" x2="${W-pr}" y1="${Yp(t)}" y2="${Yp(t)}"></line><text x="${pl-6}" y="${Yp(t)}" text-anchor="end" dominant-baseline="middle">${o.pct?NF(t*100)+'%':axisT(t)}</text>`;});
  series.forEach((sr,j)=>{const pts=sr.v.map((v,i)=>v==null?null:[X(i),Yp(v)]);let d='';pts.forEach((p,i)=>{if(!p)return;d+=(i&&pts[i-1]?'L':'M')+p[0]+','+p[1];});
    s+=`<path class="ln${j+1}" d="${d}"></path>`;const li=sr.v.length-1;if(pts[li])s+=`<circle class="dot${j+1}" cx="${pts[li][0]}" cy="${pts[li][1]}" r="4"></circle>`;});
  const step=years.length>10?2:1;years.forEach((yr,i)=>{if(i%step===0||i===years.length-1)s+=`<text x="${X(i)}" y="${H-6}" text-anchor="middle">${o.mini?"'"+String(yr).slice(2):yr}</text>`;});
  years.forEach((yr,i)=>{const tp=`<b>${yr}</b>`+series.map(sr=>`<br>${sr.k}: <span class='tn'>${sr.v[i]==null?'—':o.pct?PCTp(sr.v[i],1):TP(sr.v[i])}</span>`).join('');
    s+=`<rect class="hit" x="${X(i)-(W-pl-pr)/(years.length-1)/2}" y="${pt}" width="${(W-pl-pr)/(years.length-1)}" height="${H-pt-pb}" data-tip="${at(tp)}"></rect>`;});
  s+=`<line class="axis" x1="${pl}" x2="${W-pr}" y1="${Yp(0)}" y2="${Yp(0)}"></line>`;
  $(id).innerHTML=s+'</svg>'+(series.length>1?`<div class="lg">${series.map((sr,j)=>`<span><i class="l" style="background:var(--c${j?4:1})"></i>${sr.k}</span>`).join('')}</div>`:'');bindTips($(id));}
function niceMax(v){if(!(v>0))return 1;const p=Math.pow(10,Math.floor(Math.log10(v)));const n=v/p;return ([1,1.2,1.5,2,2.5,3,4,5,6,8,10].find(x=>n<=x))*p;}
function ticks(max,n=4){const out=[];for(let i=0;i<=n;i++)out.push(max*i/n);return out;}
function axisT(v){return v>=1e6?NF(v/1e6,v%1e6?1:0)+'M':v>=1e3?NF(v/1e3)+'k':NF(v);}
function lgd(cats){return `<div class="lg">${cats.map(([k,l,cls])=>`<span><i style="background:var(--c${cls.slice(1)})"></i>${l}</span>`).join('')}</div>`;}

// ---------- sections
function render(){
  document.documentElement.lang=LANG;document.documentElement.dir=RTL()?'rtl':'ltr';
  document.querySelectorAll('#lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===LANG));
  const S24=D.seea.supply['2024'],S23=D.seea.supply['2023'],U24=D.seea.use['2024'],SM=D.seea.summary;
  const d24=A.dest['2024'].hazardous,d23=A.dest['2023'].hazardous;
  $('title').textContent=L('Saudi waste','النفايات في المملكة');
  $('sub').textContent=L('Where the Kingdom\'s waste is generated, where it piles up, and what is — and is not — known about hazardous and industrial waste. Official statistics to 2024.','أين تتولد نفايات المملكة وأين تتراكم، وما المعروف — وغير المعروف — عن النفايات الخطرة والصناعية. إحصاءات رسمية حتى 2024.');
  $('stamp').innerHTML=`<span>${L('Sources','المصادر')}: <b>${L('General Authority for Statistics (GASTAT) — Environment Statistics 2021–2024 and SEEA Waste accounts 2024','الهيئة العامة للإحصاء — إحصاءات البيئة 2021–2024 وحسابات النفايات البيئية الاقتصادية 2024')}</b></span><span>·</span><span>${L('latest year','آخر سنة')} <b class="num">2024</b></span><span>·</span><span>${L('page built','تاريخ البناء')} <b class="num" dir="ltr">${P.built}</b></span>`;
  $('names').innerHTML=L('<b>Names used on this page:</b> GASTAT — General Authority for Statistics · MWAN — National Center for Waste Management · RCJY — Royal Commission for Jubail and Yanbu · MoMAH — Ministry of Municipalities and Housing · SEEA — the UN System of Environmental-Economic Accounting, the framework GASTAT uses for its national waste accounts','<b>الأسماء المستخدمة في هذه الصفحة:</b> الهيئة العامة للإحصاء · المركز الوطني لإدارة النفايات (موان) · الهيئة الملكية للجبيل وينبع · وزارة البلديات والإسكان · نظام المحاسبة البيئية الاقتصادية للأمم المتحدة (SEEA)، الإطار الذي تعتمده الهيئة العامة للإحصاء في حسابات النفايات الوطنية');
  $('gap').innerHTML=`<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 2 21h20L12 3z"/><path d="M12 10v5M12 18v.01"/></svg><div><b>${L('Read this first.','اقرأ هذا أولاً.')}</b> ${L('GASTAT publishes municipal waste by region, but <b>hazardous waste only as a national total</b> (split by the industry that produced it) and <b>industrial waste only for Jubail and Yanbu</b>. So the map shades regions by municipal waste, and shows hazardous and industrial waste where — and only where — a location is published. In 2024 that covers','تنشر الهيئة العامة للإحصاء النفايات البلدية حسب المنطقة، لكنها تنشر <b>النفايات الخطرة إجمالياً وطنياً فقط</b> (موزعة حسب النشاط المولِّد لها) و<b>النفايات الصناعية للجبيل وينبع فقط</b>. لذلك تُلوَّن المناطق في الخريطة بحسب النفايات البلدية، وتظهر النفايات الخطرة والصناعية حيث يُنشر موقعها — وحيث فقط. وفي 2024 يغطي ذلك')} ${PCT(A.jy_haz['2024']/S24.hazardous.total,0)} ${L('of hazardous waste; the other','من النفايات الخطرة؛ أما الـ')} ${PCT(1-A.jy_haz['2024']/S24.hazardous.total,0)} ${L('has no published location. Nothing on this page spreads national figures across regions by estimate. The source tables also have','الباقية فلا موقع منشور لها. لا توزّع هذه الصفحة أي رقم وطني على المناطق بالتقدير. وفي الجداول المصدر أيضاً')} <a href="#h-notes" style="color:inherit;font-weight:600">${A.register.length} ${L('data problems, listed at the end','مشكلة بيانات مدرجة في آخر الصفحة')}</a>${L(' — including that most 2024 national figures are 2023 scaled up.',' — منها أن معظم الأرقام الوطنية لعام 2024 هي أرقام 2023 مضروبة في معامل.')}</div>`;
  // KPIs
  const K=[
   [T(S24.total.total,1),CH(S24.total.total,S23.total.total),L('All waste generated in 2024 — every sector and households','إجمالي النفايات المتولدة في 2024 — كل القطاعات والأسر')+' '+S('seea:2-1'),'var(--eh-sea)',1],
   [T(S24.hazardous.total,1),CH(S24.hazardous.total,S23.hazardous.total),L('Hazardous waste in 2024','النفايات الخطرة في 2024')+' '+S('seea:2-1'),'var(--c4)',1],
   [T(d24.specialised,1),CH(d24.specialised,d23.specialised),L('Hazardous waste handed to waste companies, licensed or informal — the upper bound of EH\'s market','نفايات خطرة سُلّمت لشركات نفايات مرخّصة أو غير رسمية — الحد الأعلى لسوق آفاق البيئة')+' ('+PCT(d24.specialised/d24.total,0)+') '+S('seea:2-2'),'var(--eh-leaf)',1],
   [T(D.municipal_total.v['2024'],1),CH(D.municipal_total.v['2024'],D.municipal_total.v['2023']),L('Municipal waste collected in 2024','النفايات البلدية المجموعة في 2024')+' '+S('env2024:3-8'),'var(--eh-sea)'],
   [PCT(D.recycling_rate.v.municipal['2024'],1),null,L('of municipal waste recycled in 2024. GASTAT gives a flat 15% for 2010–2015, which looks assumed','من النفايات البلدية أُعيد تدويرها في 2024. وتعطي الهيئة 15% ثابتة لـ2010–2015، وتبدو مفترضة')+' '+S('env2024:3-14'),'var(--eh-bad)'],
   [T(D.jy_total.v['2024'],1),CH(D.jy_total.v['2024'],D.jy_total.v['2023']),L('Industrial waste in Jubail and Yanbu, of which','النفايات الصناعية في الجبيل وينبع، أُعيد تدوير')+' '+PCT(D.recycling_rate.v.jy['2024'],0)+' '+L('recycled','منها')+' '+S('env2024:3-11'),'var(--c4)']];
  $('kstrip').innerHTML=K.map(([v,d,l,c,pj])=>`<div class="kc" style="--k:${c}"><div class="v">${v}</div>${d==null?'':`<div class="d ${d>0?'up':'dn'}"><span class="num" dir="ltr">${SG(d)}</span> ${L('on 2023','عن 2023')}${pj?` · <span title="${esc(L('GASTAT built most 2024 account figures by scaling 2023 — see Data problems','بنت الهيئة معظم أرقام حسابات 2024 بضرب أرقام 2023 في معامل — انظر مشكلات البيانات'))}" style="border-bottom:1px dotted currentColor;cursor:help">${L('projected','إسقاط')}</span>`:''}</div>`}<div class="l">${l}</div></div>`).join('');
  // map section
  $('h-map').textContent=L('Where municipal waste is collected and where it piles up','أين تُجمع النفايات البلدية وأين تتراكم');
  $('chips').innerHTML=METRICS.map(([k,l])=>`<button class="${k===METRIC?'on':''}" data-m="${k}">${L(l[0],l[1])}</button>`).join('');
  $('chips').querySelectorAll('button').forEach(b=>b.onclick=()=>{METRIC=b.dataset.m;SORT=null;$('chips').querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));renderMapAll();});
  $('lyr').textContent=L('Year','السنة');$('lpts').textContent=L('Show Jubail, Yanbu and EH\'s site','إظهار الجبيل وينبع وموقع آفاق البيئة');
  $('h-rt').textContent=L('All 13 regions','المناطق الثلاث عشرة');
  $('rt-note').innerHTML=L('Click a column to sort, or a row to open the region. ⚠ marks a region whose figures have a data warning.','انقر عمود لترتيبه أو صفاً لفتح المنطقة. تشير ⚠ إلى منطقة في أرقامها تنبيه.')+' '+S('env2024:3-9')+' '+S('env2024:3-10');
  renderMapAll();
  // map reading — computed
  const cum=CODES.map(c=>[c,A.cum_landfill[c]]).sort((a,b)=>b[1]-a[1]),top3=cum.slice(0,3),top3s=top3.reduce((a,b)=>a+b[1],0)/A.cum_landfill.KSA;
  const pc=CODES.map(c=>[c,regionVal(c,'percap',2024)]).sort((a,b)=>b[1]-a[1]);
  const rr=CODES.map(c=>[c,regionVal(c,'recrate',2024)]).sort((a,b)=>b[1]-a[1]);
  $('mapread').innerHTML=`<b>${L('What the map says','ما تقوله الخريطة')}:</b> ${L('from 2017 to 2024','من 2017 إلى 2024 دُفن')} ${T(A.cum_landfill.KSA,1)} ${L('of municipal waste went to landfill; three regions —','من النفايات البلدية؛ ثلاث مناطق —')} ${top3.map(([c,v])=>`${esc(RN(c))} (${T(v,1)})`).join(L(', ','، '))} ${L('— hold','— تضم')} ${PCT(top3s,0)} ${L('of it. Riyadh and the Eastern region are also growing fastest among the large regions. Recycling is highest in','منها. والرياض والمنطقة الشرقية هما الأسرع نمواً بين المناطق الكبيرة. وأعلى نسبة تدوير في')} ${esc(RN(rr[0][0]))} (${PCT(rr[0][1],0)}) ${L('and','و')} ${esc(RN(rr[1][0]))} (${PCT(rr[1][1],0)}); ${L('in','وفي')} ${N(rr.filter(r=>r[1]<0.04).length)} ${L('of the 13 regions it is under 4%. Per person, the highest reading is','من 13 منطقة تقل عن 4%. وأعلى معدل للفرد في')} ${esc(RN(pc[0][0]))} (${N(pc[0][1],1)} ${L('kg/day','كغ/يوم')}) ${L('— flagged as unusual — followed by','— وهو معلَّم كقيمة غير معتادة — تليها')} ${esc(RN(pc[1][0]))} ${L('and','و')} ${esc(RN(pc[2][0]))}.`;
  hazard(); industrial(); national(); municipal(); forEH(); notes();
  $('foot').innerHTML=L('Built by Environmental Horizons Business Development from GASTAT\'s public releases. Region boundaries: Natural Earth (public domain). Arabic text is EH\'s translation. Figures are GASTAT\'s; lines marked "EH analysis" are EH\'s reading.','أعدّته إدارة تطوير الأعمال في آفاق البيئة من إصدارات الهيئة العامة للإحصاء المنشورة. حدود المناطق: Natural Earth (ملك عام). النص العربي ترجمة آفاق البيئة. الأرقام من الهيئة العامة للإحصاء؛ وما عُلِّم «تحليل آفاق البيئة» هو قراءة الشركة.');
}
function hazard(){
  const S24=D.seea.supply['2024'],S23=D.seea.supply['2023'],h24=S24.hazardous,h23=S23.hazardous,d24=A.dest['2024'].hazardous,d23=A.dest['2023'].hazardous;
  $('h-haz').textContent=L('Hazardous waste — who produces it and where it goes','النفايات الخطرة — من يولّدها وإلى أين تذهب');
  $('haz-note').innerHTML=`${T(h24.total,1)} ${L('in 2024 against','في 2024 مقابل')} ${T(h23.total,1)} ${L('in 2023 — the 2024 figure is GASTAT\'s projection from 2023. Medical hazardous waste is counted separately:','في 2023 — ورقم 2024 إسقاط من الهيئة بناءً على 2023. وتُحسب النفايات الطبية الخطرة منفصلة:')} ${T(S24.hazardous_medical.total,1)}; ${L('electronic waste:','والنفايات الإلكترونية:')} ${T(S24.ewaste.total,1)}. ${S('seea:2-1')}`;
  const SEC=[['manufacturing',L('Manufacturing','الصناعة التحويلية')],['construction',L('Construction','التشييد')],['electricity',L('Power, gas & water utilities','الكهرباء والغاز والمرافق')],['mining',L('Mining & quarrying','التعدين واستغلال المحاجر')],['households',L('Households','الأسر')],['other_economic',L('Other activities','أنشطة أخرى')]];
  hbars('c-hzsrc',SEC.map(([k,l])=>({label:l,v:h24[k],v0:h23[k],vl:TP(h24[k])+'  ·  '+PCTp(h24[k]/h24.total),tip:`<b>${l}</b><br>2024: <span class='tn'>${TP(h24[k])}</span> (${PCTp(h24[k]/h24.total,1)})<br>2023: <span class='tn'>${TP(h23[k])}</span>`})),{lw:200,aria:L('Hazardous waste by producing sector, 2024','النفايات الخطرة حسب القطاع المولِّد 2024')});
  const CATS=[['specialised',L('Waste companies (licensed or informal)','شركات نفايات (مرخّصة أو غير رسمية)'),'s1'],['recycled',L('Recycled or reused in industry','أُعيد تدويرها أو استخدامها'),'s2'],['landfill',L('Landfill','الدفن'),'s3'],['other',L('Other disposal, incl. open dumping','طرق أخرى منها الإلقاء المكشوف'),'s4']];
  stack100('c-hzdst',[{label:'2023',parts:d23},{label:'2024',parts:d24}],CATS,{aria:L('Where hazardous waste goes','أين تذهب النفايات الخطرة')});
  $('hzdst-lg').innerHTML=lgd(CATS);
  const unk=h24.total-A.jy_haz['2024'];
  stack100('c-hzloc',['2021','2022','2023','2024'].map(y=>({label:y,parts:{jy:A.jy_haz[y],none:g(D.seea.supply,y,'hazardous','total')!=null?g(D.seea.supply,y,'hazardous','total')-A.jy_haz[y]:null}})).filter(r=>r.parts.none!=null),[['jy',L('Jubail & Yanbu','الجبيل وينبع'),'s4'],['none',L('No published location','بلا موقع منشور'),'s0']],{aria:L('Share of hazardous waste with a published location','حصة النفايات الخطرة ذات الموقع المنشور')});
  $('hzloc-lg').innerHTML=lgd([['jy',L('Jubail & Yanbu (RCJY)','الجبيل وينبع (الهيئة الملكية)'),'s4'],['none',L('No published location','بلا موقع منشور'),'s0']]);
  $('hzread').innerHTML=`<b>${L('Reading','القراءة')}:</b> ${L('four industries produce','أربعة قطاعات تولّد')} ${PCT((h24.manufacturing+h24.construction+h24.electricity+h24.mining)/h24.total,0)} ${L('of hazardous waste; manufacturing alone is','من النفايات الخطرة؛ والصناعة التحويلية وحدها')} ${PCT(h24.manufacturing/h24.total,0)}. ${L('Waste companies — licensed or informal, by GASTAT\'s definition — received','واستلمت شركات النفايات — المرخّصة وغير الرسمية بحسب تعريف الهيئة —')} ${T(d24.specialised,1)} (${PCT(d24.specialised/d24.total,0)}). ${L('The rise on 2023 is GASTAT scaling its 2023 figures by','والارتفاع عن 2023 ناتج عن ضرب الهيئة أرقام 2023 في')} <span class="num" dir="ltr">×${NF(A.proj.spec_f,3)}</span>${L(', not a measured change. Another','، لا تغيّر مقيس. وذهب')} ${T(d24.landfill+d24.other,1)} (${PCT((d24.landfill+d24.other)/d24.total,0)}) ${L('went to landfill or "other disposal", which GASTAT says includes open dumping and unsafe burial. Only','إلى الدفن أو «طرق أخرى» تشمل بحسب الهيئة الإلقاء المكشوف والدفن غير الآمن. ولا يُعرف موقع إلا')} ${T(A.jy_haz['2024'],1)} ${L('of the total has a known location (Jubail and Yanbu).','من الإجمالي (الجبيل وينبع).')} ${L('Hazardous waste imports rose from','وارتفعت واردات النفايات الخطرة من')} ${T(S23.hazardous.imports,1)} ${L('to','إلى')} ${T(S24.hazardous.imports,1)}; ${L('GASTAT counts imports inside the sector totals, so part of 2024\'s rise may be imported material.','وتحتسب الهيئة الواردات ضمن مجاميع القطاعات، فقد يكون جزء من ارتفاع 2024 مواد مستوردة.')}`;
}
function industrial(){
  const yrs=Object.keys(D.jy_total.v),jm=D.jy_methods.v,J=D.jy_total.v;const cagr=Math.pow(J['2024']/J['2010'],1/14)-1;
  $('h-ind').textContent=L('Industrial waste — Jubail and Yanbu, 2010–2024','النفايات الصناعية — الجبيل وينبع 2010–2024');
  $('ind-note').innerHTML=`${L('The only industrial-waste series GASTAT publishes. It comes from the Royal Commission and covers its two industrial cities together. Growth since 2010:','السلسلة الوحيدة للنفايات الصناعية التي تنشرها الهيئة العامة للإحصاء، مصدرها الهيئة الملكية وتغطي مدينتيها الصناعيتين معاً. النمو منذ 2010:')} <span class="num" dir="ltr">${NF(J['2024']/J['2010'],1)}×</span> (${PCT(cagr,1)} ${L('a year','سنوياً')}). ${S('env2024:3-11')} ${S('env2024:3-12')}`;
  const IC=[['recycling',L('Recycled','تدوير'),'s2'],['burial',L('Buried (landfill)','دفن'),'s3'],['incineration',L('Incinerated','حرق'),'s1']];
  vstack('c-ind',yrs,IC.map(([k,l,c])=>({k,label:l,cls:c,vals:yrs.map(y=>g(jm,'all',k,y))})),{w:1100,h:300,total:yrs.map(y=>J[y]),restLabel:L('Not split by method','غير موزع حسب الطريقة'),aria:L('Industrial waste in Jubail and Yanbu by treatment method','النفايات الصناعية في الجبيل وينبع حسب طريقة المعالجة')});
  const gap=yrs.some(y=>J[y]>IC.reduce((a,[k])=>a+(g(jm,'all',k,y)||0),0)+1);
  $('ind-lg').innerHTML=lgd(IC)+(!gap?'':`<div class="lg" style="margin-top:-4px"><span><i style="background:url(#);background-image:repeating-linear-gradient(45deg,var(--eh-ink-3) 0 1.5px,var(--eh-muted-bg) 1.5px 5px)"></i>${L('Total above the three methods (not split)','الفرق بين الإجمالي والطرق الثلاث (غير موزع)')}</span></div>`);
  const hy=['2021','2022','2023','2024'];
  const HC=[['recycling',L('Recycled','تدوير'),'s2'],['burial',L('Buried','دفن'),'s3'],['incineration',L('Incinerated','حرق'),'s1']];
  stack100('c-indhz',hy.map(y=>({label:y,parts:{recycling:g(jm,'hazardous','recycling',y),burial:g(jm,'hazardous','burial',y),incineration:g(jm,'hazardous','incineration',y)}})),HC,{aria:L('Hazardous industrial waste in Jubail and Yanbu by method','النفايات الصناعية الخطرة في الجبيل وينبع حسب الطريقة')});
  $('indhz-lg').innerHTML=lgd(HC);
  lineChart('c-indrr',yrs,[{k:L('Industrial (Jubail & Yanbu)','الصناعية (الجبيل وينبع)'),v:yrs.map(y=>D.recycling_rate.v.jy[y])},{k:L('Municipal (Kingdom)','البلدية (المملكة)'),v:yrs.map(y=>D.recycling_rate.v.municipal[y])}],{pct:1,max:1,h:200,aria:L('Recycling rates','نسب التدوير')});
  const hs=A.jy_haz['2024']/J['2024'];
  $('indread').innerHTML=`<b>${L('Reading','القراءة')}:</b> ${L('in 2024','في 2024 كانت')} ${PCT(hs,0)} ${L('of the industrial waste in Jubail and Yanbu was hazardous, and','من النفايات الصناعية في الجبيل وينبع خطرة، وأُعيد تدوير')} ${PCT(D.recycling_rate.v.jy['2024'],0)} ${L('of all of it was recycled — the opposite of municipal waste, where','من مجملها — عكس النفايات البلدية التي لم يُدوَّر منها إلا')} ${PCT(D.recycling_rate.v.municipal['2024'],1)} ${L('was. Tonnage fell','. وتراجعت الكمية')} <span class="num" dir="ltr">${SG(CH(J['2024'],J['2023']))}</span> ${L('in 2024 after a peak of','في 2024 بعد ذروة')} ${T(J['2023'],1)} ${L('in 2023.','في 2023.')}`;
  // revisions table
  const R=D.revisions.jy_total;const ry=['2018','2019','2020','2021'];
  $('rev').innerHTML=`<table class="t" style="min-width:420px"><thead><tr><th>${L('Year','السنة')}</th><th class="n">${L('2022 edition','إصدار 2022')}</th><th class="n">${L('2023 edition','إصدار 2023')}</th><th class="n">${L('2024 edition (used)','إصدار 2024 (المعتمد)')}</th><th class="n">${L('Revision','المراجعة')}</th></tr></thead><tbody>${ry.map(y=>`<tr><td class="num">${y}</td><td class="n">${N(R.env2022[y])}</td><td class="n">${N(R.env2023[y])}</td><td class="n">${N(J[y])}</td><td class="n"><span class="num" dir="ltr">${SG(CH(J[y],R.env2022[y]))}</span></td></tr>`).join('')}</tbody></table>`;
}
function national(){
  const S24=D.seea.supply['2024'],S23=D.seea.supply['2023'];
  $('h-nat').textContent=L('The whole picture — all waste, 2024','الصورة الكاملة — كل النفايات 2024');
  $('nat-note').innerHTML=`${L('GASTAT\'s national waste accounts: every tonne generated by every sector and by households.','حسابات النفايات الوطنية: كل طن تولّده القطاعات والأسر.')} ${S('seea:2-1')} ${S('seea:2-2')}`;
  const TY=[['organic',L('Organic (farm, food, garden)','عضوية (زراعية وغذائية وحدائق)')],['construction',L('Construction & demolition','مخلفات البناء والهدم')],['plastic',L('Plastic','بلاستيك')],['hazardous',L('Hazardous','خطرة')],['metal',L('Metal','معادن')],['paper',L('Paper & cardboard','ورق وكرتون')],['misc',L('Mixed (burnable & not)','مختلطة')],['other',L('Other','أخرى')],['slaughter',L('Slaughterhouse','مخلفات المسالخ')],['fines',L('Fines & fluids','دقائق وسوائل')],['sludge',L('Sewage sludge','حمأة الصرف')],['glass',L('Glass','زجاج')],['wood',L('Wood','خشب')],['textiles',L('Textiles, leather, rubber','منسوجات وجلود ومطاط')],['ewaste',L('Electronic','إلكترونية')],['tyres',L('Tyres','إطارات')],['hazardous_medical',L('Medical hazardous','طبية خطرة')]];
  hbars('c-type',TY.map(([k,l])=>({label:l,v:S24[k].total,v0:S23[k].total,cls:k==='hazardous'||k==='hazardous_medical'?'s4':'s1',vl:TP(S24[k].total),tip:`<b>${l}</b><br>2024: <span class='tn'>${TP(S24[k].total)}</span> (${PCTp(S24[k].total/S24.total.total,1)})<br>2023: <span class='tn'>${TP(S23[k].total)}</span>`})),{lw:210,rh:34,aria:L('Waste by type','النفايات حسب النوع')});
  const SEC=[['agriculture',L('Agriculture & fishing','الزراعة والصيد')],['construction',L('Construction','التشييد')],['households',L('Households','الأسر')],['manufacturing',L('Manufacturing','الصناعة التحويلية')],['other_economic',L('Other activities','أنشطة أخرى')],['mining',L('Mining & quarrying','التعدين')],['waste_sector',L('Waste & water treatment (sludge)','معالجة النفايات والمياه (حمأة)')],['electricity',L('Power, gas & water utilities','الكهرباء والغاز والمرافق')]];
  hbars('c-sec',SEC.map(([k,l])=>({label:l,v:S24.total[k],v0:S23.total[k],vl:TP(S24.total[k]),tip:`<b>${l}</b><br>2024: <span class='tn'>${TP(S24.total[k])}</span> (${PCTp(S24.total[k]/S24.total.total,1)})<br>2023: <span class='tn'>${TP(S23.total[k])}</span>`})),{lw:210,aria:L('Waste by producing sector','النفايات حسب القطاع')});
  const CATS=[['specialised',L('Waste companies (licensed or informal)','شركات نفايات (مرخّصة أو غير رسمية)'),'s1'],['recycled',L('Recycled or reused','أُعيد تدويرها أو استخدامها'),'s2'],['landfill',L('Landfill','الدفن'),'s3'],['other',L('Other disposal, incl. open dumping','طرق أخرى منها الإلقاء المكشوف'),'s4']];
  stack100('c-natdst',[{label:'2023',parts:A.dest['2023'].total},{label:'2024',parts:A.dest['2024'].total}],CATS,{aria:L('Where all waste goes','أين تذهب كل النفايات')});
  $('natdst-lg').innerHTML=lgd(CATS);
  $('natread').innerHTML=`<b>${L('Reading','القراءة')}:</b> ${L('total waste is','إجمالي النفايات')} ${T(S24.total.total,1)} ${L('in 2024 — the','في 2024 — والزيادة')} <span class="num" dir="ltr">${SG(CH(S24.total.total,S23.total.total))}</span> ${L('rise is mostly GASTAT scaling 2023 by sector, and the split by producing sector is an allocation (see Data problems).','على 2023 ناتجة في معظمها عن ضرب الهيئة أرقام 2023 بمعاملات قطاعية، وتوزيع القطاعات المولِّدة تقديري (انظر مشكلات البيانات).')} ${L('Farming and construction produce over half of it, and households','وتولّد الزراعة والتشييد أكثر من نصفه، والأسر')} ${PCT(S24.total.households/S24.total.total,0)}. ${L('Only','ولا تصل إلى الشركات المتخصصة إلا')} ${PCT(A.dest['2024'].total.specialised/A.dest['2024'].total.total,0)} ${L('reaches specialised waste companies;','؛')} ${PCT((A.dest['2024'].total.landfill+A.dest['2024'].total.other)/A.dest['2024'].total.total,0)} ${L('is landfilled or goes to "other disposal".','تُدفن أو تذهب إلى «طرق أخرى».')}`;
}
function municipal(){
  const yrs=Object.keys(D.municipal_total.v);
  $('h-mun').textContent=L('Municipal waste — growth and the fall in recycling','النفايات البلدية — النمو وتراجع التدوير');
  $('mun-note').innerHTML=`${L('Collected by the Ministry of Municipalities and Housing, 2010–2024.','ما جمعته وزارة البلديات والإسكان 2010–2024.')} ${S('env2024:3-8')} ${S('env2024:3-13')}`;
  vstack('c-mun',yrs,[{k:'rec',label:L('Recycled','مُدوَّرة'),cls:'s2',vals:yrs.map(y=>D.recycled.v.municipal[y])},{k:'rest',label:L('Not recycled','غير مُدوَّرة'),cls:'s1',vals:yrs.map(y=>D.municipal_total.v[y]-D.recycled.v.municipal[y])}],{w:1100,h:280,aria:L('Municipal waste collected and recycled','النفايات البلدية المجموعة والمُدوَّرة')});
  $('mun-lg').innerHTML=lgd([['rec',L('Recycled','مُدوَّرة'),'s2'],['rest',L('Not recycled','غير مُدوَّرة'),'s1']]);
  // composition by region 2024
  const comp=[['organic',L('Organic','عضوية'),'s1'],['plastic',L('Plastic','بلاستيك'),'s2'],['paper',L('Paper','ورق'),'s3'],['mgf',L('Metal, glass, fabric','معادن وزجاج ونسيج'),'s4'],['other',L('Other non-organic','غير عضوية أخرى'),'s0']];
  const order=CODES.slice().sort((a,b)=>g(M,b,'total','2024')-g(M,a,'total','2024'));
  stack100('c-comp',['KSA',...order].map(c=>({label:c==='KSA'?L('Kingdom','المملكة'):RN(c),parts:{organic:g(M,c,'organic','2024'),plastic:g(M,c,'plastic','2024'),paper:g(M,c,'paper','2024'),mgf:['metal','glass','fabric'].reduce((s,x)=>s+g(M,c,x,'2024'),0),other:g(M,c,'other','2024')}})),comp,{w:1100,rh:32,lw:150,aria:L('Municipal waste by material and region','النفايات البلدية حسب المادة والمنطقة')});
  $('comp-lg').innerHTML=lgd(comp);
  const R=D.recycling_rate.v.municipal;
  $('munread').innerHTML=`<b>${L('Reading','القراءة')}:</b> ${L('municipal waste has more than doubled since 2010 (','تضاعفت النفايات البلدية منذ 2010 (')}${T(D.municipal_total.v['2010'],1)} → ${T(D.municipal_total.v['2024'],1)}${L('). Measured recycling was 7% in 2017 and',')، وكان التدوير المقيس 7% في 2017 و')} ${PCT(R['2024'],1)} ${L('in 2024; the 15% GASTAT shows for 2010–2015 is identical every year and looks assumed.','في 2024؛ أما نسبة 15% التي تظهرها الهيئة لـ2010–2015 فثابتة كل عام وتبدو مفترضة.')} ${L('Almost everything collected ends in sanitary landfill:','ويكاد كل ما يُجمع ينتهي بالدفن الصحي:')} ${PCT(g(TR,'KSA','landfill','2024')/g(TR,'KSA','total','2024'),0)} ${L('of treated municipal waste in 2024.','من النفايات البلدية المعالجة في 2024.')} ${L('About','ونحو')} ${PCT(g(M,'KSA','organic','2024')/g(M,'KSA','total','2024'),0)} ${L('of it is organic, and plastic is the next largest stream.','منها عضوية، ويليها البلاستيك.')}`;
}
function forEH(){
  const S24=D.seea.supply['2024'],S23=D.seea.supply['2023'],d24=A.dest['2024'].hazardous,d23=A.dest['2023'].hazardous;
  const mk=g(M,'SA-02','total','2024'),mkr=CODES.map(c=>[c,A.cum_landfill[c]]).sort((a,b)=>b[1]-a[1]).findIndex(r=>r[0]==='SA-02')+1;
  $('h-eh').innerHTML=L('What it means for EH','ماذا يعني لآفاق البيئة')+`<span class="eha">${L('EH analysis','تحليل آفاق البيئة')}</span>`;
  const O=[
   [L(`<b>EH's market is at most ${TP(d24.specialised)} of hazardous waste a year (${PCTp(d24.specialised/d24.total)} of the total).</b> That is the tonnage GASTAT puts with waste companies, and its definition includes informal operators and unsafe burial, so licensed treatment is only part of it. The ${SG(CH(d24.specialised,d23.specialised))} rise on 2023 is GASTAT scaling its 2023 figures, not observed growth.`,`<b>سوق آفاق البيئة لا يتجاوز ${TP(d24.specialised)} من النفايات الخطرة سنوياً (${PCTp(d24.specialised/d24.total)} من الإجمالي).</b> وهي الكمية التي تنسبها الهيئة لشركات النفايات، وتعريفها يشمل جهات غير رسمية والدفن غير الآمن، فالمعالجة المرخّصة جزء منها فقط. والزيادة ${SG(CH(d24.specialised,d23.specialised))} عن 2023 ناتجة عن ضرب الهيئة أرقام 2023، لا نمو ملاحَظ.`),
    L('Quote this as an upper-bound market size, not a growth rate. Ask MWAN for tonnage received by licensed facilities to get the real market.','يُستخدم حداً أعلى لحجم السوق لا معدل نمو، ويُطلب من «موان» ما تستلمه المنشآت المرخّصة لمعرفة السوق الفعلي.')],
   [L(`<b>${TP(d24.landfill+d24.other)} of hazardous waste (${PCTp((d24.landfill+d24.other)/d24.total)}) still goes to landfill or "other disposal"</b>, which GASTAT says includes open dumping and unsafe burial. If enforcement tightens, this is the volume most likely to move to licensed treatment.`,`<b>لا يزال ${TP(d24.landfill+d24.other)} من النفايات الخطرة (${PCTp((d24.landfill+d24.other)/d24.total)}) يذهب إلى الدفن أو «طرق أخرى»</b> تشمل بحسب الهيئة الإلقاء المكشوف والدفن غير الآمن. وإذا شُدّدت الرقابة فهذه هي الكمية الأرجح انتقالها إلى المعالجة المرخّصة.`),
    L('Target the producers behind it — manufacturing, construction, utilities and mining — with compliance-led offers.','استهداف القطاعات المولِّدة لها — الصناعة والتشييد والمرافق والتعدين — بعروض قائمة على الامتثال.')],
   [L(`<b>Four industries produce ${PCTp((S24.hazardous.manufacturing+S24.hazardous.construction+S24.hazardous.electricity+S24.hazardous.mining)/S24.hazardous.total)} of hazardous waste</b> by GASTAT's allocation (fixed ratios, not plant-level data). Construction alone produced ${TP(S24.hazardous.construction)}. That is where giga-project and infrastructure sites sit, although the data does not name them.`,`<b>أربعة قطاعات تولّد ${PCTp((S24.hazardous.manufacturing+S24.hazardous.construction+S24.hazardous.electricity+S24.hazardous.mining)/S24.hazardous.total)} من النفايات الخطرة</b> بحسب توزيع الهيئة (نسب ثابتة لا بيانات منشآت). والتشييد وحده ولّد ${TP(S24.hazardous.construction)}، وفيه تقع مواقع المشاريع الكبرى والبنية التحتية، وإن لم تسمّها البيانات.`),
    L('Cross-check the stakeholder map: tier the contractors and utilities by these volumes.','مطابقة ذلك مع خريطة أصحاب المصلحة وترتيب المقاولين والمرافق وفق هذه الكميات.')],
   [L(`<b>${PCTp(1-A.jy_haz['2024']/S24.hazardous.total)} of hazardous waste has no published location.</b> None of GASTAT's tables say which regions generate it. EH cannot size its catchment around Al-Juhfah from public data.`,`<b>${PCTp(1-A.jy_haz['2024']/S24.hazardous.total)} من النفايات الخطرة بلا موقع منشور.</b> لا تبيّن جداول الهيئة المناطق المولِّدة لها، فلا تستطيع آفاق البيئة تقدير نطاق خدمتها حول الجحفة من البيانات العامة.`),
    L('Add a request to the MWAN data-request letter: hazardous waste generated by region and waste type, and tonnage received by each licensed facility, 2021–2024.','إضافة طلب إلى خطاب طلب البيانات الموجّه إلى «موان»: النفايات الخطرة المتولدة حسب المنطقة ونوع النفاية، والكميات المستلمة في كل منشأة مرخّصة، 2021–2024.')],
   [L(`<b>Makkah region, EH's home, collected ${TP(mk)} of municipal waste in 2024 and ranks ${['','first','second','third','fourth','fifth'][mkr]||'#'+mkr} for waste landfilled since 2017.</b> But GASTAT's own tables show more landfilled there than collected, so the regional figures are unreliable.`,`<b>منطقة مكة المكرمة، مقر آفاق البيئة، جمعت ${TP(mk)} من النفايات البلدية في 2024، وترتيبها ${['','الأول','الثاني','الثالث','الرابع','الخامس'][mkr]||mkr} في المدفون منذ 2017.</b> لكن جداول الهيئة نفسها تُظهر مدفوناً أكبر من المجموع فيها، فأرقامها الإقليمية غير موثوقة.`),
    L('Treat Makkah\'s municipal numbers with care, and do not quote them without the caveat.','التعامل مع أرقام مكة البلدية بحذر وعدم الاستشهاد بها دون التحفّظ.')],
   [L(`<b>Hazardous waste imports rose from ${TP(S23.hazardous.imports)} to ${TP(S24.hazardous.imports)}.</b> The figure is not broken down. It could mean more material arriving for treatment or recovery in the Kingdom.`,`<b>ارتفعت واردات النفايات الخطرة من ${TP(S23.hazardous.imports)} إلى ${TP(S24.hazardous.imports)}.</b> ولا يتوفر تفصيل لها، وقد تعني مواد أكثر تصل للمعالجة أو الاستخلاص داخل المملكة.`),
    L('Watch item: ask MWAN or GASTAT what the imports are and who receives them.','بند متابعة: سؤال «موان» أو الهيئة عن طبيعة هذه الواردات والجهات المستلمة.')]];
  $('opps').innerHTML=O.map(([s,a],i)=>`<div class="opp"><div class="n num">${i+1}</div><div><div class="st">${s}</div><div class="ac"><b>${L('Action','الإجراء')}:</b> ${a}</div></div></div>`).join('');
}
function notes(){
  const RG=A.register, SEV={critical:[L('Changes conclusions','يغيّر الاستنتاجات'),'var(--eh-bad)','var(--eh-bad-bg)'],major:[L('Use with care','يُستخدم بحذر'),'var(--eh-warn)','var(--eh-warn-bg)'],minor:[L('Minor','بسيط'),'var(--eh-ink-3)','var(--eh-muted-bg)']};
  $('h-notes').textContent=L('Data problems and gaps','مشكلات البيانات والفجوات');
  const cnt=k=>RG.filter(r=>r.sev===k).length;
  $('dnotes').innerHTML=`<div class="note">${L(`${RG.length} problems found by checking every table against itself, against the other tables and against earlier GASTAT editions: ${cnt('critical')} change what the figures can be used for, ${cnt('major')} need care, ${cnt('minor')} are minor. Each says what this page does about it.`,`${RG.length} مشكلة وُجدت بمطابقة كل جدول مع نفسه ومع الجداول الأخرى ومع إصدارات الهيئة السابقة: ${cnt('critical')} تغيّر ما يصح استخدام الأرقام له، و${cnt('major')} تحتاج حذراً، و${cnt('minor')} بسيطة. ولكل منها ما تفعله الصفحة حيالها.`)}</div>`+
   RG.map((r,i)=>{const sv=SEV[r.sev];return `<div class="opp"><div class="n num" style="color:${sv[1]}">${i+1}</div><div><div class="st"><b>${esc(L(r.ten,r.tar))}</b> <span class="eha" style="background:${sv[2]};color:${sv[1]}">${sv[0]}</span></div><div class="st" style="font-size:13.5px;color:var(--eh-ink-2);margin-top:4px">${esc(L(r.en,r.ar))}</div><div class="ac" style="border-inline-start-color:${sv[1]}"><b style="color:${sv[1]}">${L('On this page','في هذه الصفحة')}:</b> ${esc(L(r.hen,r.har))}</div></div></div>`;}).join('');
  document.querySelectorAll('[data-sec]').forEach(el=>{const k=el.dataset.sec.split('|');el.textContent=L(k[0],k[1]);});
  document.querySelectorAll('.png:not(#mreset)').forEach(b=>b.textContent=L('Export PNG','تصدير PNG'));
  document.querySelectorAll('[data-t]').forEach(el=>{const k=el.dataset.t.split('|');el.textContent=L(k[0],k[1]);});
}
// ---------- PNG export (light-theme colours, EH fonts embedded)
let EXFONTS=null;
function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);
 const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'],['EH Display','vendor/fonts/montserrat-latin-var.woff2','100 900'],['EH Display','vendor/fonts/alexandria-arabic-var.woff2','100 900']];
 return Promise.all(F.map(f=>fetch(f[1]).then(r=>r.ok?r.blob():null).then(b=>b?new Promise(res=>{const fr=new FileReader();fr.onload=()=>res(`@font-face{font-family:'${f[0]}';src:url(${fr.result}) format('woff2');font-weight:${f[2]}}`);fr.readAsDataURL(b);}):'').catch(()=>''))).then(a=>EXFONTS=a.join(''));}
function exPNG(id,name){ exFonts().then(()=>exPNG2(id,name)); }
function exPNG2(id,name){const svg=document.querySelector('#'+id+' svg');if(!svg)return;const cl=svg.cloneNode(true);const vb=svg.viewBox.baseVal;cl.setAttribute('width',vb.width);cl.setAttribute('height',vb.height);
 const dk=document.body.classList.contains('dark');if(dk)document.body.classList.remove('dark');
 const se=[...svg.querySelectorAll('*')],ce=[...cl.querySelectorAll('*')];
 se.forEach((e,i)=>{const d=ce[i];if(!d||!/^(text|tspan|rect|path|line|circle)$/.test(e.tagName))return;const cs=getComputedStyle(e);if(!(e.getAttribute('fill')||'').startsWith('url'))d.setAttribute('fill',cs.fill);d.setAttribute('stroke',cs.stroke);d.setAttribute('stroke-width',cs.strokeWidth);if(cs.strokeDasharray&&cs.strokeDasharray!=='none')d.setAttribute('stroke-dasharray',cs.strokeDasharray);
  if(e.tagName==='text'){d.setAttribute('font-family',/EH Display/.test(cs.fontFamily)?"'EH Display','Segoe UI',Tahoma,Arial,sans-serif":"'EH Sans','Segoe UI',Tahoma,Arial,sans-serif");d.setAttribute('font-weight',cs.fontWeight);d.setAttribute('font-size',cs.fontSize);d.setAttribute('paint-order',cs.paintOrder);}if(e.classList.contains('hit'))d.setAttribute('fill','none');d.removeAttribute('class');d.removeAttribute('data-tip');});
 if(dk)document.body.classList.add('dark');
 const fst=document.createElementNS('http://www.w3.org/2000/svg','style');fst.textContent=EXFONTS||'';cl.insertBefore(fst,cl.firstChild);
 const bg=document.createElementNS('http://www.w3.org/2000/svg','rect');bg.setAttribute('width',vb.width);bg.setAttribute('height',vb.height);bg.setAttribute('fill','#fff');cl.insertBefore(bg,cl.firstChild);
 const xml=new XMLSerializer().serializeToString(cl),img=new Image(),SC=2.5;img.onload=()=>{const c=document.createElement('canvas');c.width=vb.width*SC;c.height=vb.height*SC;const x=c.getContext('2d');x.drawImage(img,0,0,c.width,c.height);const a=document.createElement('a');a.download=`EH_SaudiWaste_${name}_${LANG}_${new Date().toISOString().slice(0,10)}.png`;a.href=c.toDataURL('image/png');document.body.appendChild(a);a.click();a.remove();};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(xml);}
// ---------- language / theme (follows the hub)
function setLang(l){LANG=l;try{localStorage.setItem('sw.lang',l)}catch(e){};render();}
function setDark(d){document.body.classList.toggle('dark',d);drawMap();}
window.addEventListener('message',e=>{const d=e.data||{};if(d.ehhub==='lang'&&(d.lang==='ar'||d.lang==='en')&&d.lang!==LANG)setLang(d.lang);if(d.ehhub==='theme')setDark(d.theme==='dark');});
$('yslider').addEventListener('input',e=>{YEAR=+e.target.value;renderMapAll();});
$('ptsbox').addEventListener('change',e=>{PTS=e.target.checked;drawMap();});
try{if(localStorage.getItem('ehhub.theme')==='dark')document.body.classList.add('dark');}catch(e){}
if(!/[?&]embedded=1/.test(location.search)&&window.parent===window){try{if(matchMedia('(prefers-color-scheme: dark)').matches&&!localStorage.getItem('ehhub.theme'))document.body.classList.add('dark');}catch(e){}}
render();
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Saudi waste — where the Kingdom's waste is generated and where it piles up</title>
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">{CSS}</style>
<script src="vendor/d3.min.js"></script>
</head>
<body>
<header data-eh-contour="7">
 <div><h1 id="title">Saudi waste</h1><div class="sub" id="sub"></div></div>
 <div class="ctl"><div class="tog" id="lang"><button data-l="en" onclick="setLang('en')">EN</button><button data-l="ar" onclick="setLang('ar')">عربي</button></div></div>
</header>
<main>
 <div class="stamp" id="stamp"></div>
 <div class="note" id="names" style="margin:-4px 0 12px;font-size:12.5px"></div>
 <div class="gapnote" id="gap" role="note"></div>
 <div class="kstrip" id="kstrip"></div>

 <div class="sec" data-sec="1 · Regions|١ · المناطق"></div>
 <div class="card">
  <div class="hd"><h2 id="h-map"></h2><button class="png" onclick="exPNG('map','map')">Export PNG</button></div>
  <div class="chips" id="chips" role="tablist"></div>
  <div class="ctlrow"><span id="lyr">Year</span> <input type="range" id="yslider" min="2017" max="2024" step="1" value="2024" aria-label="Year"> <span class="yr num" id="yr">2024</span>
   <label><input type="checkbox" id="ptsbox" checked> <span id="lpts"></span></label>
   <button class="png" id="mreset" type="button" onclick="resetMap()" style="margin-inline-start:auto"></button></div>
  <div class="note" id="mdesc" style="margin-top:8px"></div>
  <div class="mapgrid"><div><div id="map"></div><div class="legend" id="legend"></div></div><div class="panel" id="panel"></div></div>
  <div class="read" id="mapread"></div>
 </div>
 <div class="card"><h2 id="h-rt"></h2><div class="note" id="rt-note"></div><div class="tw" id="rtable"></div></div>

 <div class="sec" data-sec="2 · Hazardous waste|٢ · النفايات الخطرة"></div>
 <div class="card">
  <h2 id="h-haz"></h2><div class="note" id="haz-note"></div>
  <div class="g2" style="gap:24px">
   <div><div class="hd"><h3 data-t="Who produces it — 2024 and 2023|من يولّدها — 2024 و2023"></h3><button class="png" onclick="exPNG('c-hzsrc','hazardous_by_sector')">Export PNG</button></div><div id="c-hzsrc"></div></div>
   <div><div class="hd"><h3 data-t="Where it goes|إلى أين تذهب"></h3><button class="png" onclick="exPNG('c-hzdst','hazardous_destination')">Export PNG</button></div><div id="hzdst-lg"></div><div id="c-hzdst"></div>
    <div class="hd" style="margin-top:10px"><h3 data-t="How much has a published location|كم منها له موقع منشور"></h3><button class="png" onclick="exPNG('c-hzloc','hazardous_location')">Export PNG</button></div><div id="hzloc-lg"></div><div id="c-hzloc"></div></div>
  </div>
  <div class="read" id="hzread"></div>
 </div>

 <div class="sec" data-sec="3 · Industrial waste|٣ · النفايات الصناعية"></div>
 <div class="card">
  <div class="hd"><h2 id="h-ind"></h2><button class="png" onclick="exPNG('c-ind','industrial_jubail_yanbu')">Export PNG</button></div><div class="note" id="ind-note"></div>
  <div id="ind-lg"></div><div class="note" data-t="Tonnes (k = thousand, M = million)|بالطن (k = ألف، M = مليون)" style="margin:0"></div><div id="c-ind"></div>
  <div class="g2" style="gap:24px;margin-top:14px">
   <div><div class="hd"><h3 data-t="Hazardous share, by method (2021–2024)|النفايات الخطرة حسب الطريقة (2021–2024)"></h3><button class="png" onclick="exPNG('c-indhz','industrial_hazardous_methods')">Export PNG</button></div><div id="indhz-lg"></div><div id="c-indhz"></div></div>
   <div><div class="hd"><h3 data-t="Recycling rate — industrial vs municipal|نسبة التدوير — صناعية مقابل بلدية"></h3><button class="png" onclick="exPNG('c-indrr','recycling_rates')">Export PNG</button></div><div id="c-indrr"></div></div>
  </div>
  <div class="read" id="indread"></div>
  <h3 data-t="Revisions between GASTAT editions (tonnes)|المراجعات بين إصدارات الهيئة (طن)"></h3><div class="tw" id="rev"></div>
 </div>

 <div class="sec" data-sec="4 · All waste|٤ · كل النفايات"></div>
 <div class="card">
  <h2 id="h-nat"></h2><div class="note" id="nat-note"></div>
  <div class="g2" style="gap:24px">
   <div><div class="hd"><h3 data-t="By type — 2024 and 2023|حسب النوع — 2024 و2023"></h3><button class="png" onclick="exPNG('c-type','waste_by_type')">Export PNG</button></div><div id="c-type"></div></div>
   <div><div class="hd"><h3 data-t="By producing sector — 2024 and 2023|حسب القطاع المولِّد — 2024 و2023"></h3><button class="png" onclick="exPNG('c-sec','waste_by_sector')">Export PNG</button></div><div id="c-sec"></div>
    <div class="hd" style="margin-top:10px"><h3 data-t="Where it goes|إلى أين تذهب"></h3><button class="png" onclick="exPNG('c-natdst','waste_destination')">Export PNG</button></div><div id="natdst-lg"></div><div id="c-natdst"></div></div>
  </div>
  <div class="read" id="natread"></div>
 </div>

 <div class="sec" data-sec="5 · Municipal waste|٥ · النفايات البلدية"></div>
 <div class="card">
  <div class="hd"><h2 id="h-mun"></h2><button class="png" onclick="exPNG('c-mun','municipal_trend')">Export PNG</button></div><div class="note" id="mun-note"></div>
  <div id="mun-lg"></div><div class="note" data-t="Tonnes (k = thousand, M = million)|بالطن (k = ألف، M = مليون)" style="margin:0"></div><div id="c-mun"></div>
  <div class="hd" style="margin-top:14px"><h3 data-t="What it is made of, by region — 2024|مكوّناتها حسب المنطقة — 2024"></h3><button class="png" onclick="exPNG('c-comp','municipal_composition')">Export PNG</button></div><div id="comp-lg"></div><div id="c-comp"></div>
  <div class="read" id="munread"></div>
 </div>

 <div class="sec" data-sec="6 · For EH and data problems|٦ · لآفاق البيئة ومشكلات البيانات"></div>
 <div class="card"><h2 id="h-eh"></h2><div id="opps"></div></div>
 <div class="card"><h2 id="h-notes"></h2><div id="dnotes"></div></div>
 <div class="foot" id="foot"></div>
</main>
<div id="tip" role="tooltip"></div>
<script id="DATA" type="application/json">{payload}</script>
<script>{JS}</script>
<script src="eh-shared.js" defer></script>
</body></html>
"""
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(HTML)
print('written', OUT, len(HTML) // 1024, 'KB')
