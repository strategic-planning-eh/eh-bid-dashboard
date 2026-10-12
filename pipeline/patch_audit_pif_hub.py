"""patch_audit_pif_hub.py — audit fixes for the PIF annual reports page (hub/pif_intelligence_hub.html), 12 Oct 2026.

An independent audit checked every figure on this page against PIF's 2023, 2024 and 2025 annual reports. The numbers were
right; several sentences about them were not, and some source pages pointed to the wrong place. What was wrong, and what
changed:

  • Chart captions said the opposite of their own charts (audit pif-01, 02, 03, 04, 13, 25a). The one-line captions are
    now worked out from the data the page already holds, in English and Arabic, so they cannot drift from the charts:
      - industries: Energy is the largest slice every year (23% → 32% → 28%), then real estate — not "technology,
        property and finance take most of the money";
      - return: it rose to 8.7% in 2023, then fell two years running to 5.8% — not "fell every year" (also fixed in
        sections 7 and 10 and the analysis box);
      - accounts: what PIF owes grew faster than what it owns (debts ×2.4, borrowing ×3.7, assets ×2.2), and the
        green line is what is left after debts — not "owns rises faster" and not "two bars";
      - abroad: the share fell from 29% to 17% by 2024, then rose to 20% in 2025, and money abroad rose in riyals
        every year (512 → 663 bn) — not "shrinking" and "roughly flat";
      - pools: listed Saudi stakes and PIF-founded companies hold most of the money; giga-projects grew fastest only
        from a tiny 2020 base and dipped after 2023; energy rose from 23% to 28–32% — not "steady";
      - income: risen in most years, with a dip in 2022 — not "climbs steadily".
  • 2024 waste row (pif-05): "full reuse of wastewater" is Qiddiya in the 2024 report (p.71), not NEOM; the other four
    2024 page numbers in that row are corrected (p.89, p.88, p.85, p.69). English and Arabic.
  • Green bonds (pif-06): the 2025 report's 146 is "projects with eligible spending identified", not projects funded.
    The chart now draws the 2025 point hollow (dashed join) with that label, and the table header, findings,
    note, analysis and "changed numbers" row no longer claim the fall from 49.4 to 4 million m³ is "a change of
    definition": PIF does not say whether the 2025 figures cover the SAR 33.75 bn allocated or the SAR 67.5 bn
    identified.
  • Wrong source pages in tooltips (pif-14): green bonds 2024 p.90 → p.86; Saudi staff 2024 p.92 → p.20; new hires
    2023 p.102 → p.100; "200-plus" companies p.12 → p.14; money abroad 2023 p.43 → p.14; fund size 2022 "2025 report
    p.46" → 2024 report p.42 (the 2025 report does not print it).
  • Arabic (pif-16): tooltips, KPI tiles and table cells now say "مليار ريال" / "مليار دولار" instead of "SAR … bn";
    tooltip sources read "تقرير 2024 ص86" etc.; the 2024 column header is translated.
  • "Improved every year" heading listed rising borrowing → "Rose every year" (pif-17).
  • "Sevenfold" sustainability mentions used raw counts; per 10,000 words it is just over threefold (pif-18).
  • "AI" mentions recounted for 2023–2025 as the whole word "AI" or "artificial intelligence": 7 / 63 / 55 (were
    5 / 30 / 38); the footnote says how AI and SIRC are counted (pif-19). SIRC counts already match "SIRC or the full
    company name", so they are unchanged.
  • Local supplier figures 53%, 57%, 62 and 207 are printed in the 2025 report (p.104): marked ✓, not ≈ (pif-20).
  • Findings f4: dropped the cash-flow claim (the 2021 report already had one); the English now has the sentence
    pointing to the strategy page that the Arabic already had (pif-25b, c).

Not changed here (owner decisions): the "+120%" KPI basis (pif-25d) and the 2020 share-abroad baseline (pif-15).

Exact-string edits; stops if an anchor is missing. Run once:  python3 pipeline/patch_audit_pif_hub.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table, nfkc, _log

P = os.path.join(HERE, '..', 'hub', 'pif_intelligence_hub.html')
if 'EH_CAPS_LIVE' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'pif')
A = 'pif'
jx = lambda s: json.dumps(s, ensure_ascii=False)[1:-1]          # how the I18N block stores a string

def i18n(key, en_old, en_new, ar_old, ar_new, note, cat='copy', body_too=True):
    """Replace one part of an I18N value (English and/or Arabic), matched exactly as stored in the script. The English
    text is also written into the page body (what shows before the script runs), so it is replaced there too."""
    k = FILES[A].index('const I18N=')
    body, script = FILES[A][:k], FILES[A][k:]
    pairs = []
    if en_old is not None: pairs.append(('EN', en_old, en_new, body_too))
    if ar_old is not None: pairs.append(('AR', ar_old, ar_new, False))
    for lang, old, new, in_body in pairs:
        n = script.count(jx(old)); ok = n == 1
        if ok: script = script.replace(jx(old), nfkc(jx(new)))
        _log(A, 'exact', jx(old), jx(new), cat, note + ' (%s, script)' % lang, n, ok)
        if in_body:
            n = body.count(old); ok = n == 1
            if ok: body = body.replace(old, new)
            _log(A, 'exact', old, new, cat, note + ' (%s, page body)' % lang, n, ok)
    FILES[A] = body + script

# ---------------------------------------------------------------- pif-01/02/03/04/13/25a: captions from the data
LIVE = r'''
/* EH_CAPS_LIVE (patch_audit_pif_hub.py, 12 Oct 2026): the captions below are worked out from D, so they always say what the
   chart shows. Arabic number runs are isolated (U+2066…U+2069) so ranges and "×" keep their order. */
(function(){try{
  var I=function(x){return '⁦'+x+'⁩'}, r=Math.round, f1=function(x){return (Math.round(x*10)/10).toFixed(1)};
  /* industries */
  var gy=[2023,2024,2025], en=gy.map(function(y){return r(D.gics[y].v[0])}), re=gy.map(function(y){return D.gics[y].v[1]});
  var top=gy.every(function(y){var v=D.gics[y].v.slice(0,11);return v[0]===Math.max.apply(null,v)});
  if(top) EH_CAPS.cGics=['Energy is the largest slice every year ('+en.join('% → ')+'%), then real estate ('+r(Math.min.apply(null,re))+'–'+r(Math.max.apply(null,re))+'%); there is no environmental-services category.',
    'الطاقة هي الشريحة الأكبر كل عام ('+en.join('% ثم ')+'%)، تليها العقارات ('+I(r(Math.min.apply(null,re))+'–'+r(Math.max.apply(null,re))+'%')+')؛ ولا توجد فئة للخدمات البيئية.'];
  /* energy and utilities */
  var ut=gy.map(function(y){return D.gics[y].v[5]}), later=en.slice(1);
  EH_CAPS.cEnergy=['Energy rose from '+en[0]+'% (2023) to '+Math.min.apply(null,later)+'–'+Math.max.apply(null,later)+'% in the next two years; utilities stayed at '+r(Math.min.apply(null,ut))+'–'+r(Math.max.apply(null,ut))+'%.',
    'ارتفعت حصة الطاقة من '+en[0]+'% (2023) إلى '+I(Math.min.apply(null,later)+'–'+Math.max.apply(null,later)+'%')+' في العامين التاليين؛ وبقيت المرافق عند '+I(r(Math.min.apply(null,ut))+'–'+r(Math.max.apply(null,ut))+'%')+'.'];
  /* return: rise to a peak, then n falls */
  var ty=[2022,2023,2024,2025], tv=ty.map(function(y){return D.tsr[y].v}), pk=tv.indexOf(Math.max.apply(null,tv)), n=tv.length-1-pk;
  if(pk>0&&n>0){var wEn={1:'in 2025',2:'two years running',3:'three years running'}[n], wAr={1:'في العام التالي',2:'عامين متتاليين',3:'ثلاثة أعوام متتالية'}[n];
    EH_CAPS.cTsr=['The average yearly return since 2017 rose from '+tv[0]+'% to '+tv[pk]+'% in '+ty[pk]+', then fell '+wEn+' to '+tv[tv.length-1]+'%.',
      'ارتفع متوسط العائد السنوي منذ 2017 من '+tv[0]+'% إلى '+tv[pk]+'% في '+ty[pk]+'، ثم انخفض '+wAr+' إلى '+tv[tv.length-1]+'%.'];}
  /* balance sheet */
  var F=D.fs, ast=F.totalAssets[2025]/F.totalAssets[2020], liab=(F.totalAssets[2025]-F.equity[2025])/(F.totalAssets[2020]-F.equity[2020]), ln=F.loans[2025]/F.loans[2020];
  if(liab>ast) EH_CAPS.cBal=['What PIF owes grew faster than what it owns since 2020: all debts ×'+f1(liab)+', borrowing ×'+f1(ln)+', everything owned ×'+f1(ast)+'. The green line is what is left after all debts.',
    'نما ما يدين به الصندوق أسرع مما يملكه منذ 2020: كل الديون '+I('×'+f1(liab))+'، والاقتراض '+I('×'+f1(ln))+'، وكل ما يملكه '+I('×'+f1(ast))+'. والخط الأخضر هو ما يتبقى بعد كل الديون.'];
  else EH_CAPS.cBal=['Since 2020 everything owned grew ×'+f1(ast)+' and borrowing ×'+f1(ln)+'. The green line is what is left after all debts.','منذ 2020 نما كل ما يملكه الصندوق '+I('×'+f1(ast))+' والاقتراض '+I('×'+f1(ln))+'. والخط الأخضر هو ما يتبقى بعد كل الديون.'];
  /* share abroad */
  var sy=[2021,2022,2023,2024,2025], si=sy.map(function(y){return D.split[y].i}), mn=Math.min.apply(null,si), my=sy[si.indexOf(mn)], last=si[si.length-1];
  if(my!==2025&&last>mn) EH_CAPS.cSplit=['Roughly four riyals in five stay inside Saudi Arabia; the share held abroad fell from '+si[0]+'% (2021) to '+mn+'% ('+my+'), then rose to '+last+'% in 2025.',
    'نحو أربعة ريالات من كل خمسة تبقى داخل المملكة؛ وانخفضت حصة الخارج من '+si[0]+'% (2021) إلى '+mn+'% ('+my+')، ثم ارتفعت إلى '+last+'% في 2025.'];
  /* money abroad in riyals */
  var iy=[2022,2023,2024,2025], iv=iy.map(function(y){return D.splitSAR[y].i}), up=iv.every(function(v,k){return !k||v>iv[k-1]}), g=r((iv[3]/iv[2]-1)*100), shr=D.aum.own[2025]<D.aum.own[2024];
  if(up&&shr) EH_CAPS.cIntl=['Money invested abroad rose in riyals every year, from SAR '+iv[0]+' bn (2022) to SAR '+iv[3]+' bn (2025); in 2025 it grew '+g+'% while the whole fund shrank, so its share went back up.',
    'ارتفعت الأموال المستثمرة في الخارج بالريال كل عام، من '+iv[0]+' مليار ريال (2022) إلى '+iv[3]+' مليار ريال (2025)؛ وفي 2025 نمت '+g+'% بينما انكمش الصندوق كله، فعادت حصتها إلى الارتفاع.'];
  /* pools */
  var pv=D.pools[2025].v, tot=pv.reduce(function(a,b){return a+b},0), big=r((pv[3]+pv[4])/tot*100), gg=[2020,2021,2022,2023,2024,2025].map(function(y){return D.pools[y].v[6]}),
      gpk=Math.max.apply(null,gg), gpy=2020+gg.indexOf(gpk), fast=D.pools[2025].v.every(function(v,k){return k===7||k===6||v/D.pools[2020].v[k]<=gg[5]/gg[0]});
  if(fast&&gpy<2025) EH_CAPS.cPool=['Listed Saudi stakes and PIF-founded companies hold most of the money ('+big+'% in 2025); the giga-projects pool grew fastest from a tiny 2020 base (SAR '+gg[0]+' bn), then dipped after '+gpy+' (SAR '+gpk+' bn → '+gg[5]+' bn).',
    'تضم حصص الشركات السعودية المدرجة والشركات التي أسسها الصندوق معظم الأموال ('+big+'% في 2025)؛ ونمت مجموعة المشاريع الكبرى الأسرع من قاعدة صغيرة جداً في 2020 ('+gg[0]+' مليار ريال)، ثم تراجعت بعد '+gpy+' (من '+gpk+' إلى '+gg[5]+' مليار ريال).'];
  /* income */
  var yy=[2020,2021,2022,2023,2024,2025], dips=yy.filter(function(y,k){return k&&F.revenue[y]<F.revenue[yy[k-1]]});
  if(dips.length&&dips.length<3) EH_CAPS.cRev=['Total income has risen in most years (it dipped in '+dips.join(' and ')+'); cash in hand moves in steps, rising when PIF borrows or sells.',
    'ارتفع الدخل الكلي في معظم السنوات (مع تراجع في '+dips.join(' و')+')؛ والنقد المتاح يتحرك على درجات، يرتفع عند الاقتراض أو البيع.'];
}catch(e){}})();
'''
rep(A, '"cStaff": ["Headcount has more than doubled in four years; PIF is building its own capacity to run assets, not only to fund them.", "تضاعف عدد الموظفين أكثر من مرتَين في أربع سنوات؛ يبني الصندوق قدرته على إدارة الأصول لا تمويلها فقط."]};\n',
    '"cStaff": ["Headcount has more than doubled in four years; PIF is building its own capacity to run assets, not only to fund them.", "تضاعف عدد الموظفين أكثر من مرتَين في أربع سنوات؛ يبني الصندوق قدرته على إدارة الأصول لا تمويلها فقط."]};' + LIVE,
    'copy', 'pif-01/02/03/04/13/25a: chart captions worked out from the page data (EN+AR)')

# ---------------------------------------------------------------- pif-02: return "fell every year"
i18n('p7', 'It has fallen every year on that measure.',
     'On that measure it rose from 8% (2022) to 8.7% (2023), then fell two years running to 5.8% (2025).',
     'وقد انخفض كل عام بهذا المقياس.',
     'وبهذا المقياس ارتفع من 8% (2022) إلى 8.7% (2023)، ثم انخفض عامين متتاليين إلى 5.8% (2025).',
     'pif-02: section 7 return sentence')
i18n('f2', 'The average yearly return since 2017 has gone down every year it has been reported the same way: 8% (2022), 8.7% (2023), 7.2% (2024), 5.8% (2025).',
     'The average yearly return since 2017 fell for a second year running, to 5.8% (7.2% in 2024; it had risen from 8% to 8.7% in 2023).',
     'تراجع متوسط العائد السنوي منذ 2017 في كل سنة أُبلغ عنها بالطريقة نفسها: 8% (2022)، 8.7% (2023)، 7.2% (2024)، 5.8% (2025).',
     'وانخفض متوسط العائد السنوي منذ 2017 للعام الثاني على التوالي إلى 5.8% (7.2% في 2024؛ وكان قد ارتفع من 8% إلى 8.7% في 2023).',
     'pif-02: findings f2 return sentence')
i18n('an1', 'Its return has been falling since the reports first measured it consistently.',
     'Its average return rose to 8.7% in 2023 and has fallen in both years since, to 5.8%.',
     'وعائده في تراجع منذ أن بدأت التقارير قياسه بطريقة متسقة.',
     'وارتفع متوسط عائده إلى 8.7% في 2023 ثم انخفض في العامين التاليين إلى 5.8%.',
     'pif-02: analysis an1 return sentence')

# ---------------------------------------------------------------- pif-05: 2024 waste row
rep(A, 'SIRC installed 70 reverse vending machines in Riyadh; 1.25 million bottles, 30,000 cans, 15,000 users (2024 report p.96). SIRC listed among companies making up the ~2% of assets under management in climate solutions (2024 report p.95). PIF audited water and waste at its own properties and drafted a waste reduction strategy (2024 report p.89). Red Sea Global: \\"sustainable waste management\\" (2024 report p.70). NEOM: \\"full reuse of wastewater\\" (2024 report p.72).',
    'SIRC installed 70 reverse vending machines in Riyadh; 1.25 million bottles, 30,000 cans, 15,000 users (2024 report p.89). SIRC listed among companies making up the ~2% of assets under management in climate solutions (2024 report p.88). PIF audited energy, water and waste at its own properties and drafted a waste reduction strategy (2024 report p.85). Red Sea Global: \\"sustainable waste management\\" (2024 report p.69). Qiddiya: \\"full reuse of wastewater\\" (2024 report p.71).',
    'copy', 'pif-05: 2024 waste row — wastewater reuse is Qiddiya; four page numbers corrected (EN)')
rep(A, '(تقرير 2024 ص96). \\"سرك\\" مدرجة ضمن الشركات التي تشكل نحو 2% من الأصول في الحلول المناخية (تقرير 2024 ص95). راجع الصندوق المياه والنفايات في منشآته الخاصة ووضع مسودة استراتيجية لتقليل النفايات (تقرير 2024 ص89). البحر الأحمر الدولية: \\"إدارة مستدامة للنفايات\\" (تقرير 2024 ص70). نيوم: \\"إعادة استخدام كامل لمياه الصرف\\" (تقرير 2024 ص72).',
    '(تقرير 2024 ص89). \\"سرك\\" مدرجة ضمن الشركات التي تشكل نحو 2% من الأصول في الحلول المناخية (تقرير 2024 ص88). راجع الصندوق الطاقة والمياه والنفايات في منشآته الخاصة ووضع مسودة استراتيجية لتقليل النفايات (تقرير 2024 ص85). البحر الأحمر الدولية: \\"إدارة مستدامة للنفايات\\" (تقرير 2024 ص69). القدية: \\"إعادة استخدام كامل لمياه الصرف\\" (تقرير 2024 ص71).',
    'copy', 'pif-05: 2024 waste row — wastewater reuse is Qiddiya; four page numbers corrected (AR)')

# ---------------------------------------------------------------- pif-06: green bonds 2025 = identified, not funded
rep(A, 'projects:{2023:{v:35,src:"2023 report p.98"},2024:{v:91,src:"2024 report p.90"},2025:{v:146,src:"2025 report p.92"}}',
    'projects:{2023:{v:35,src:"2023 report p.98"},2024:{v:91,src:"2024 report p.86"},2025:{v:146,kind:"identified",note:"projects with eligible spending identified, not projects funded",src:"2025 report p.92"}}',
    'data', 'pif-06 + pif-14: 2025 project count marked "identified"; 2024 page p.90 → p.86')
rep(A, 'co2:{2023:{v:10.6,note:"expected, eligible pipeline, Mt CO2e",src:"2023 report p.98"},2025:{v:5.1,note:"expected, allocated projects, Mt CO2",src:"2025 report p.92"}}',
    'co2:{2023:{v:10.6,note:"expected, eligible pipeline, Mt CO2e",src:"2023 report p.98"},2025:{v:5.1,note:"expected from these investments (allocated or identified: PIF does not say), Mt CO2",src:"2025 report p.92"}}',
    'data', 'pif-06: 2025 CO2 note no longer says "allocated projects"')
rep(A, 'wastewater:{2023:{v:49.4,note:"expected, eligible pipeline, million m3",src:"2023 report p.98"},2025:{v:4,note:"expected, allocated projects, million m3",src:"2025 report p.92"}}',
    'wastewater:{2023:{v:49.4,note:"expected, eligible pipeline, million m3",src:"2023 report p.98"},2025:{v:4,note:"expected from these investments (allocated or identified: PIF does not say), million m3",src:"2025 report p.92"}}',
    'data', 'pif-06: 2025 wastewater note no longer says "allocated projects"')
rep(A, "{type:'line',label:t('c_proj'),data:gr.map(y=>gv(G.projects,y)),borderColor:C.gold,backgroundColor:C.gold,yAxisID:'y2',pointRadius:5}",
    "{type:'line',label:t('c_proj'),data:gr.map(y=>gv(G.projects,y)),borderColor:C.gold,backgroundColor:C.gold,pointBackgroundColor:gr.map(y=>G.projects[y]&&G.projects[y].kind==='identified'?'transparent':C.gold),pointBorderWidth:gr.map(y=>G.projects[y]&&G.projects[y].kind==='identified'?2:1),segment:{borderDash:s=>{const o=G.projects[gr[s.p1DataIndex]];return o&&o.kind==='identified'?[5,4]:undefined}},yAxisID:'y2',pointRadius:5}",
    'code', 'pif-06: 2025 project point drawn hollow with a dashed join (a different measure)')
rep(A, '"c_proj": ["Projects funded", "المشاريع الممولة"]', '"c_proj": ["Projects funded (hollow point: only identified)", "المشاريع الممولة (النقطة المفرغة: محددة فقط)"]',
    'copy', 'pif-06: chart legend explains the hollow point')
i18n('p6', 'Line: the number of projects funded.', 'Line: the number of projects funded; the 2025 point is hollow because it counts projects with eligible spending identified, not projects funded.',
     'الخط: عدد المشاريع الممولة.', 'الخط: عدد المشاريع الممولة؛ ونقطة 2025 مفرغة لأنها تعدّ المشاريع التي حُدد لها إنفاق مؤهل، لا المشاريع الممولة.',
     'pif-06: section 6 text explains the hollow point')
i18n('t6_c3', '2025 report (funded projects, 2025)', '2025 report (146 projects with eligible spending identified)',
     'تقرير 2025 (المشاريع الممولة، 2025)', 'تقرير 2025 (146 مشروعاً حُدد لها إنفاق مؤهل)', 'pif-06: impact table header (drawn by the script only)', body_too=False)
i18n('f1', 'and the number of green projects funded (35, then 91, then 146).',
     'and the number of green projects funded (35, then 91; the 2025 report counts something different: 146 projects with eligible spending identified).',
     'وعدد المشاريع الخضراء الممولة (35 ثم 91 ثم 146).',
     'وعدد المشاريع الخضراء الممولة (35 ثم 91؛ ويعدّ تقرير 2025 شيئاً مختلفاً: 146 مشروعاً حُدد لها إنفاق مؤهل).',
     'pif-06: findings f1 project count')
i18n('s6b', 'The 2023 numbers describe every project that could qualify; the 2025 numbers describe only the projects that have been given money. They measure different things, so the drop from 49.4 to 4 million cubic metres is not a fall in activity.',
     'The 2023 figures describe every project that could qualify (USD 11.7 billion of eligible spending). The 2025 report says its figures come from "these investments": SAR 33.75 billion already allocated and SAR 67.5 billion of eligible spending identified across 146 projects. It does not say which of the two, so the drop from 49.4 to 4 million cubic metres cannot be called a change of definition; it may be a real fall in the wastewater the bonds are expected to treat.',
     'أرقام 2023 تصف كل مشروع يمكن أن يكون مؤهلاً؛ وأرقام 2025 تصف فقط المشاريع التي أُعطيت أموالاً. إنها تقيس أشياء مختلفة، لذا فإن الانخفاض من 49.4 إلى 4 ملايين متر مكعب ليس تراجعاً في النشاط.',
     'تصف أرقام 2023 كل مشروع يمكن أن يكون مؤهلاً (11.7 مليار دولار من الإنفاق المؤهل). ويقول تقرير 2025 إن أرقامه تأتي من «هذه الاستثمارات»: 33.75 مليار ريال خُصصت فعلاً، و67.5 مليار ريال من الإنفاق المؤهل حُددت عبر 146 مشروعاً. ولا يحدد أيهما يقصد، لذا لا يمكن وصف الانخفاض من 49.4 إلى 4 ملايين متر مكعب بأنه تغيير في التعريف؛ فقد يكون تراجعاً حقيقياً في مياه الصرف المتوقع أن تعالجها السندات.',
     'pif-06: green bond note')
i18n('an5', 'Second, the green bond impact figures changed what they measure between 2023 and 2025; the drop from 49.4 to 4 million cubic metres of wastewater is a change of definition, not of activity.',
     'Second, PIF does not say which investments the 2025 green bond impact figures cover (SAR 33.75 billion allocated or SAR 67.5 billion identified across 146 projects), so the drop from 49.4 to 4 million cubic metres of wastewater cannot be put down to a change of definition; it may be a real fall.',
     'ثانياً، غيّرت أرقام أثر السندات الخضراء ما تقيسه بين 2023 و2025؛ فالانخفاض من 49.4 إلى 4 ملايين متر مكعب من مياه الصرف تغيير في التعريف لا في النشاط.',
     'ثانياً، لا يحدد الصندوق الاستثمارات التي تشملها أرقام أثر السندات الخضراء لعام 2025 (33.75 مليار ريال مخصصة أم 67.5 مليار ريال محددة عبر 146 مشروعاً)، لذا لا يمكن عزو الانخفاض من 49.4 إلى 4 ملايين متر مكعب من مياه الصرف إلى تغيير في التعريف؛ فقد يكون تراجعاً حقيقياً.',
     'pif-06: analysis an5')
rep(A, '"4 million m³, funded projects only (2025 report p.92)","Different measures; shown in a table, not as a trend."',
    '"4 million m³, from \\"these investments\\": SAR 33.75 billion allocated and SAR 67.5 billion identified across 146 projects; PIF does not say which (2025 report p.92)","PIF does not say what the 2025 figure covers, so the fall cannot be put down to a change of definition; shown in a table, not as a trend."',
    'copy', 'pif-06: changed-numbers row (EN)')
rep(A, '"4 ملايين م³، المشاريع الممولة فقط (تقرير 2025 ص92)","مقياسان مختلفان؛ يُعرضان في جدول لا كاتجاه."',
    '"4 ملايين م³، من «هذه الاستثمارات»: 33.75 مليار ريال مخصصة و67.5 مليار ريال محددة عبر 146 مشروعاً؛ ولا يحدد الصندوق أيهما (تقرير 2025 ص92)","لا يحدد الصندوق ما يشمله رقم 2025، لذا لا يمكن عزو الانخفاض إلى تغيير في التعريف؛ يُعرض الرقمان في جدول لا كاتجاه."',
    'copy', 'pif-06: changed-numbers row (AR)')

# ---------------------------------------------------------------- pif-14: wrong source pages
rep(A, '2024:{v:9,src:"2024 report p.90"}', '2024:{v:9,src:"2024 report p.86"}', 'data', 'pif-14: green bonds raised 2024 p.90 → p.86')
rep(A, '2024:{v:5.2,note:"as of 30 Jun 2024",src:"2024 report p.90"}', '2024:{v:5.2,note:"as of 30 Jun 2024",src:"2024 report p.86"}', 'data', 'pif-14: green bonds allocated 2024 p.90 → p.86')
rep(A, '2024:{v:19.4,src:"2024 report p.90"}', '2024:{v:19.4,src:"2024 report p.86"}', 'data', 'pif-14: green eligible spending 2024 p.90 → p.86')
i18n('s6', '2024 report p.90', '2024 report p.86', 'تقرير 2024 ص90', 'تقرير 2024 ص86', 'pif-14: green bonds source line', 'data')
rep(A, '2024:{v:84.5,src:"2024 report p.92"}', '2024:{v:84.5,src:"2024 report p.20"}', 'data', 'pif-14: Saudi staff 2024 p.92 → p.20')
rep(A, '2023:{v:812,src:"2023 report p.102"}', '2023:{v:812,src:"2023 report p.100"}', 'data', 'pif-14: new hires 2023 p.102 → p.100')
rep(A, 'src:"2023 report p.12 (\\"200-plus\\")"', 'src:"2023 report p.14 (\\"200-plus\\")"', 'data', 'pif-14: "200-plus" companies p.12 → p.14')
rep(A, '2023:{i:586,l:2194,t:72, src:"2023 report p.43"}', '2023:{i:586,l:2194,t:72, src:"2023 report p.14 (abroad), p.43 (cash)"}', 'data', 'pif-14: money abroad 2023 is on p.14')
i18n('s3b', '2023 report p.43 ·', '2023 report p.14 (abroad), p.43 (cash) ·', 'تقرير 2023 ص43 ·', 'تقرير 2023 ص14 (الخارج)، ص43 (النقد) ·', 'pif-14: Saudi/abroad source line', 'data')
rep(A, '2022:"2025 report p.46", 2023:"2025 report p.46"', '2022:"2024 report p.42 (also 2023 report p.42)", 2023:"2025 report p.46"', 'data', 'pif-14: fund size 2022 is not in the 2025 report; 2024 report p.42')

# ---------------------------------------------------------------- pif-16: Arabic units and sources
SRC = r'''const usd=v=>LANG==='ar'?'≈'+(v/FX).toFixed(v<100?1:0)+' مليار دولار':'≈$'+(v/FX).toFixed(v<100?1:0)+' bn';const fmt=n=>n==null?'?':n.toLocaleString('en-US');
// Arabic (patch_audit_pif_hub.py, 12 Oct 2026): amounts in words, and source notes in Arabic ("تقرير 2024 ص86"); any English left is isolated LTR.
const sarbn=v=>LANG==='ar'?fmt(v)+' مليار ريال':'SAR '+fmt(v)+' bn';
const usdB=x=>LANG==='ar'?x+' مليار دولار':'$'+x+' billion';
const sarB=x=>LANG==='ar'?(/\+$/.test(x)?'أكثر من '+x.slice(0,-1):x)+' مليار ريال':'SAR '+x+' billion';
const plusL=x=>LANG==='ar'?'أكثر من '+x.slice(0,-1):x;
const SRC_AR=[[/2021 single-year return \(2021 report p\.28\) - not the since-Vision Realization Program measure used from 2022/g,'عائد عام 2021 وحده (تقرير 2021 ص28)، وليس مقياس «منذ بدء برنامج تحقيق الرؤية» المستخدم منذ 2022'],
 [/since the Vision Realization Program began \(30 Sep 2017\), per year/g,'متوسط سنوي منذ بدء برنامج تحقيق الرؤية (30 سبتمبر 2017)'],[/since the Vision Realization Program began, per year/g,'متوسط سنوي منذ بدء برنامج تحقيق الرؤية'],
 [/latest report to show (\d{4})/g,'آخر تقرير يعرض $1'],[/(\d{4}) report gives no pool values/g,'تقرير $1 لا يذكر قيم المجموعات'],[/had ([\d,]+) for listed shares and bonds/g,'ذكر $1 للأسهم والسندات المدرجة'],
 [/had ([\d,]+) and ([\d,]+) for two Saudi buckets/g,'ذكر $1 و$2 لمجموعتين سعوديتين'],[/unchanged from/g,'دون تغيير عن'],[/originally printed/g,'طبع في الأصل'],[/ said /g,' ذكر '],[/\(also /g,'(وكذلك '],
 [/treasury not separated/g,'النقد غير مفصول'],[/only report showing 2020/g,'التقرير الوحيد الذي يعرض 2020'],[/previous-year column/g,'عمود السنة السابقة'],[/cash flows revised from/g,'تدفقات نقدية معدّلة عن'],
 [/cash in hand from/g,'النقد المتاح من'],[/opening balance/g,'الرصيد الافتتاحي'],[/\(abroad\)/g,'(الخارج)'],[/\(cash\)/g,'(النقد)'],[/"200-plus"/g,'«أكثر من 200»'],[/: ([\d,.]+) of ([\d,.]+)/g,': $1 من $2'],
 [/SAR ([\d.,]+) billion \/ 3\.75/g,'$1 مليار ريال ÷ 3.75'],[/as of 30 Jun (\d{4})/g,'حتى 30 يونيو $1'],[/projects with eligible spending identified, not projects funded/g,'مشاريع حُدد لها إنفاق مؤهل، لا مشاريع ممولة'],
 [/expected, eligible pipeline/g,'متوقع، كل المشاريع المؤهلة'],[/expected from these investments \(allocated or identified: PIF does not say\)/g,'متوقع من «هذه الاستثمارات» (المخصصة أم المحددة: لا يحدد الصندوق)'],
 [/Mt CO2e?/g,'مليون طن CO₂'],[/million m3/g,'مليون م³'],[/AR(\d\d) p\.?(\d+)/g,'تقرير 20$1 ص$2'],[/(\d{4}) report p\.(\d+(?:[-–]\d+)?)/g,'تقرير $1 ص$2'],[/(\d{4}) report/g,'تقرير $1'],[/ p\.(\d+)/g,' ص$1'],[/ - /g,' — '],[/; /g,'؛ '],[/, /g,'، ']];
const srcL=s=>{if(LANG!=='ar'||!s)return s;let o=String(s);SRC_AR.forEach(([r,v])=>{o=o.replace(r,v)});return o.replace(/[A-Za-z][A-Za-z0-9 .,'’-]*[A-Za-z0-9]/g,m=>'⁦'+m+'⁩')};'''
rep(A, "const usd=v=>'≈$'+(v/FX).toFixed(v<100?1:0)+' bn';const fmt=n=>n==null?'?':n.toLocaleString('en-US');", SRC,
    'code', 'pif-16: Arabic amounts ("مليار ريال") and Arabic source notes for tooltips')
rep(A, "if(unit==='sarbn')s+='SAR '+fmt(v)+' bn ('+usd(v)+')'", "if(unit==='sarbn')s+=sarbn(v)+' ('+usd(v)+')'", 'code', 'pif-16: tooltip amounts in Arabic')
rep(A, "afterLabel:c=>srcFn?srcFn(c):''", "afterLabel:c=>srcFn?srcL(srcFn(c)):''", 'code', 'pif-16: tooltip sources in Arabic')
rep(A, "[t('k1'),'SAR '+fmt(A[2025])+' bn',", "[t('k1'),sarbn(A[2025]),", 'code', 'pif-16: KPI fund size in Arabic')
rep(A, "[t('k3'),'SAR 4,000 billion',", "[t('k3'),sarB(fmt(D.aum.target)),", 'code', 'pif-16: KPI target in Arabic')
rep(A, "return c.dataset.label+': '+(c.datasetIndex<2?'$'+o.v+' bn':o.v)+' '+glyph(o.g)+(o.note?' · '+o.note:'')},afterLabel:c=>{const o=[G.raised,G.allocated,G.projects][c.datasetIndex][gr[c.dataIndex]];return o?o.src:''}",
    "return c.dataset.label+': '+(c.datasetIndex<2?(LANG==='ar'?o.v+' مليار دولار':'$'+o.v+' bn'):o.v)+' '+glyph(o.g)+(o.note?' · '+srcL(o.note):'')},afterLabel:c=>{const o=[G.raised,G.allocated,G.projects][c.datasetIndex][gr[c.dataIndex]];return o?srcL(o.src):''}",
    'code', 'pif-16: green bond tooltip amounts, notes and sources in Arabic')
rep(A, '<td class="n">$11.7 billion</td><td class="n">$19.4 billion</td><td class="n">≈$18.0 billion (SAR 67.5 billion)</td>',
    '<td class="n">${usdB(\'11.7\')}</td><td class="n">${usdB(\'19.4\')}</td><td class="n">≈${usdB(\'18.0\')} (${sarB(\'67.5\')})</td>', 'code', 'pif-16: impact table amounts in Arabic')
rep(A, '<td class="n">SAR 40+ billion ✓</td>', '<td class="n">${sarB(\'40+\')} ✓</td>', 'code', 'pif-16: Private Sector Hub amounts in Arabic (1)')
rep(A, '<td class="n">20 (SAR 6.1 billion) ✓</td>', '<td class="n">20 (${sarB(\'6.1\')}) ✓</td>', 'code', 'pif-16: Private Sector Hub amounts in Arabic (2)')
rep(A, '<td class="n">30 (SAR 11+ billion) ✓</td>', '<td class="n">30 (${sarB(\'11+\')}) ✓</td>', 'code', 'pif-16: Private Sector Hub amounts in Arabic (3)')
rep(A, '<td class="n">140+ (SAR 15+ billion) ✓</td>', '<td class="n">${plusL(\'140+\')} (${sarB(\'15+\')}) ✓</td>', 'code', 'pif-16: Private Sector Hub amounts in Arabic (4)')
rep(A, '"t6_c2": ["2024 report", "2024 report"]', '"t6_c2": ["2024 report", "تقرير 2024"]', 'copy', 'pif-16: 2024 column header in Arabic')

# ---------------------------------------------------------------- pif-17 / 18 / 19 / 20 / 25b-c
i18n('f1h', 'Improved every year', 'Rose every year', 'تحسّن كل عام', 'ارتفع كل عام', 'pif-17: neutral heading — borrowing rising is not an improvement')
i18n('an3', 'The sustainability sections have grown more than sevenfold since 2021 (\"sustainab-\" appears 21 times in the 2021 report and 158 times in 2025)',
     'The sustainability sections have more than tripled since 2021 when measured per 10,000 words (\"sustainab-\" goes from 17 to 56 mentions per 10,000 words; 21 to 158 raw mentions, partly because the reports grew longer)',
     'نمت أقسام الاستدامة أكثر من سبعة أضعاف منذ 2021 (كلمة \"sustainab-\" تظهر 21 مرة في تقرير 2021 و158 مرة في 2025)',
     'تضاعفت أقسام الاستدامة أكثر من ثلاث مرات منذ 2021 مقيسةً لكل 10,000 كلمة (من 17 إلى 56 ذكراً لكلمة \"sustainab-\" لكل 10,000 كلمة؛ ومن 21 إلى 158 مرة في العدّ الخام، جزئياً لأن التقارير صارت أطول)',
     'pif-18: sustainability growth measured per 10,000 words')
rep(A, '2023:[1,0,0,4,0,1,2,6,5,2,25,2,63,7,8],', '2023:[1,0,0,4,0,1,2,6,7,2,25,2,63,7,8],', 'data', 'pif-19: AI mentions 2023 recounted 5 → 7')
rep(A, '2024:[5,1,4,11,0,1,3,12,30,0,35,3,126,10,18],', '2024:[5,1,4,11,0,1,3,12,63,0,35,3,126,10,18],', 'data', 'pif-19: AI mentions 2024 recounted 30 → 63')
rep(A, '2025:[7,5,1,8,2,2,4,6,38,3,33,53,158,8,18]}', '2025:[7,5,1,8,2,2,4,6,55,3,33,53,158,8,18]}', 'data', 'pif-19: AI mentions 2025 recounted 38 → 55')
rep(A, 'mentions: { // whole-text keyword counts per report (case-insensitive substring match on pdftotext output).',
    'mentions: { // whole-text keyword counts per report (case-insensitive substring match on pdftotext output; AI 2023-2025 = whole word "AI" or "artificial intelligence", once when both appear together, recounted 12 Oct 2026; SIRC = short or full name).',
    'data', 'pif-19: counting rule noted in the data comment')
i18n('s8', '\"AI\" is under-counted where it appears as \"A.I.\" or inside compound words.',
     '\"AI\" for 2023–2025 counts the word \"AI\" or \"artificial intelligence\" (once where both appear together); 2021–2022 use the earlier, simpler count, which can miss some mentions. \"SIRC\" counts the short name or the full company name.',
     'كلمة \"AI\" مُحصاة بأقل من الواقع حيث ترد \"A.I.\" أو داخل كلمات مركبة.',
     'تشمل \"AI\" في 2023–2025 كلمة \"AI\" أو عبارة \"artificial intelligence\" (مرة واحدة حين تردان معاً)؛ وتعتمد 2021–2022 العدّ الأبسط السابق، وقد يفوته بعض المرات. وتشمل \"SIRC\" الاسم المختصر أو الاسم الكامل للشركة.',
     'pif-19: heat map footnote says how AI and SIRC are counted (drawn by the script only)', body_too=False)
rep(A, '<td class="n">53% ≈</td><td class="n">57% ≈</td>', '<td class="n">53% ✓</td><td class="n">57% ✓</td>', 'copy', 'pif-20: local content score is printed (2025 report p.104) — ✓ not ≈')
rep(A, '<td class="n">62 ≈</td>', '<td class="n">62 ✓</td>', 'copy', 'pif-20: local spend 2020 is printed — ✓ not ≈')
rep(A, '<td class="n">207 ≈</td>', '<td class="n">207 ✓</td>', 'copy', 'pif-20: local spend 2024 is printed — ✓ not ≈')
i18n('s7c', 'The local supplier figures appear only in the 2025 report, looking back, hence ≈.', 'The local supplier figures appear only in the 2025 report (p.104), looking back; they are printed there, hence ✓.',
     'أرقام الموردين المحليين تظهر فقط في تقرير 2025 بأثر رجعي، ومن هنا علامة ≈.', 'أرقام الموردين المحليين تظهر فقط في تقرير 2025 (ص104) بأثر رجعي، وهي مطبوعة فيه، ومن هنا علامة ✓.',
     'pif-20: local supplier note')
i18n('f4', 'a cash-flow table (from 2023), ', '', 'وجدول التدفقات النقدية (منذ 2023)، ', '', 'pif-25b: f4 no longer says the cash-flow table started in 2023')
i18n('f4', 'Renewables Infrastructure\" ecosystem (2025).',
     'Renewables Infrastructure\" ecosystem (2025). The strategy document itself, published 2026, is analysed in the companion dashboard <a href=\"pif_strategy_2026_2030.html\">PIF Strategy 2026–2030</a>; it spells the ecosystem \"Clean Energy, Water & Renewable Infrastructure\", which is treated as canonical there.',
     None, None, 'pif-25c: English f4 gets the strategy-page sentence the Arabic (and the page body) already had', body_too=False)

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES[A])
write_change_table(os.path.join(HERE, 'change_table_audit_pif_hub'), 'Audit fixes — PIF annual reports page (12 Oct 2026)')
print('patched: hub/pif_intelligence_hub.html')
