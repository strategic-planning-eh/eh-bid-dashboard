"""patch_audit_bids.py — Bid & Tender page fixes from the 12 Oct 2026 audit (judge J1, "bids" fix pass).

Run AFTER patch_audit_bids_pipeline.py (the page reads the new fields it adds: winloss.pending, pricing.summary.basis /
eh_rosters). Every edit is an exact-string (or anchored regex) replacement that stops the script if the anchor is missing.

What was wrong → what the page does now:
  #1  bids-03   Prices were compared on two VAT bases. The Pricing subtitle, the Executive price chart and the chat now say
                that all prices include VAT (the pipeline puts every price on that basis).
  #2  bids-02   Executive "Price position — we win on technical, not on price" was a typed verdict the chart contradicted.
                Title and summary are computed: wins where EH was / was not the lowest bidder (decided tenders only), and
                the "typically EH priced X% above" figure is the median of the bars actually drawn.
  #3  bids-04   Overview and Pipeline donuts counted the 14 lost tenders twice. One slice per tender: won / lost /
                cancelled / pending (a "closed, nobody awarded" slice only if such tenders exist).
  #4  bids-01   Chat "open pipeline" listed won tenders: it now lists tenders with no result only.
  #5  bids-05   All Tenders search lost focus after one letter: focus and caret are restored after each re-render.
  #15 bids-13   Pricing cards: "bidder count unknown" instead of an invented "1 bidders"; rank/gap stay "—" with one price.
  #16 bids-14   Bid Turnaround called the client's launch→deadline window "how long the EH committee takes to decide":
                retitled "Time the client allows to bid", committee wording removed (tab, read-out, chat).
  #17 bids-16   Pricing read-out, chat and Notes gave opposite verdicts from one number and said loss reasons are not
                recorded. One verdict from the median gap (single 20% threshold) everywhere; the caveat counts the
                recorded loss reasons and technical scores.
  #18 bids-17   Chat "latest decisions" was empty: lists won/lost tenders by award date.
  #21 bids-20   Arabic Executive charts: price and threat charts are mirrored and their Arabic text runs right-to-left.
  #22 bids-21   "Environmental Studies / EIA" translated; chat answers in Arabic; colloquial «مين بيكسب علينا» matches.
  #23 bids-15   "show EH's price against the full field" → "have EH's price and at least one rival's".
  #24 bids-22   Executive win-rate change is grey and marked "not significant" when the likely ranges overlap.
  #25 bids-23   Year labels follow the selected scope (header, KPI strip, Pipeline status card).
  #26 bids-24   Funnel note no longer says stage names are clickable.
  #27 bids-25   Competitors subtitle counts the bid sheets that list EH (not "37+").
  #28 bids-26   Pricing card: keyboard focus returns to the card after Enter.
  #29 bids-27   Win/Loss: bars with fewer than 10 decided tenders are grey and say "too few to rate" (All Tenders' rule);
                the competition-intensity chart is drawn at a readable size.
  #30 bids-28   "Why bids were declined": the typed "locked to a specific brand" claim is replaced by the two most common
                recorded categories; the hard-coded 22 is replaced by the number of guarantees recorded.
  #31 bids-31   Coloured values (win %, gaps, undercut %, "older than 90 days") use the EH status tokens (≥4.5:1 in light
                and dark); the grey CANCELLED tag uses dark text.
  #8  bids-08   Threat cover line: "never disclosed a price" → "no price known against EH's".

Run once:  python3 pipeline/patch_audit_bids.py
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_change_table

J, CH = os.path.join(HERE, 'app.js'), os.path.join(HERE, 'charts.js')
if 'function pxVerdict' in open(J, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(J, 'app'); load(CH, 'charts')

# ---------------------------------------------------------------- charts.js: hbar can be drawn at a smaller virtual width
rep('charts', "  const W=wd, n=data.length, H=n*o.rh+14, labw=240, barx=labw+8, iw=W-barx-90;\n",
    "  const W=o.W||wd, n=data.length, H=n*o.rh+14, labw=o.labw||240, barx=labw+8, iw=W-barx-(o.vr||90);   // o.W / o.labw / o.vr (room for the value label): half-width cards keep readable labels\n",
    'ui', 'hbar: optional virtual width and label column (#29)')

# ---------------------------------------------------------------- labels, colours, scope
rep('app', "const DSVC={'Environmental Studies / EIA (impact assessment)':'دراسات بيئية / تقييم الأثر البيئي',",
    "const DSVC={'Environmental Studies / EIA (impact assessment)':'دراسات بيئية / تقييم الأثر البيئي','Environmental Studies / EIA':'دراسات بيئية / تقييم الأثر البيئي',",
    'copy', '#22 Arabic name for the EIA service line')
rep('app', "['funnel','Bid Turnaround','مدة اتخاذ القرار']", "['funnel','Bid Turnaround','مهلة التقديم']",
    'copy', '#16 Arabic tab name no longer says "decision time"')
rep('app', "const wrCol=v=>v==null?C.soft:(v>=50?C.green:v>=30?C.orange:C.red);\n",
    "const wrCol=v=>v==null?C.soft:(v>=50?C.green:v>=30?C.orange:C.red);\n"
    "const wrCls=v=>v==null?'':(v>=50?'vt-good':v>=30?'vt-warn':'vt-bad');   // text colour classes: EH status tokens, AA in both themes (#31)\n",
    'ui', '#31 text colour classes')
rep('app', "body.dark .tctl{background:#151C21!important;border-color:#2C3A43!important}</style>');}catch(e){}})();",
    "body.dark .tctl{background:#151C21!important;border-color:#2C3A43!important}.vt-good{color:var(--eh-good)!important}.vt-warn{color:var(--eh-warn)!important}.vt-bad{color:var(--eh-bad)!important}</style>');}catch(e){}})();",
    'ui', '#31 colour classes use the contrast-checked status tokens')
rep('app', "kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),YRS)+",
    "kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),exScopeLabel())+", 'copy', '#25 KPI year label follows the scope')
rep('app', "'Environmental Horizons (Afaq Al-Biah) — competitive bid analytics, tracking years '+YRS,'آفاق البيئة (Afaq Al-Biah) — تحليلات تنافسية للمنافسات، سنوات التتبّع \\u2066'+YRS+'\\u2069'",
    "'Environmental Horizons (Afaq Al-Biah) — competitive bid analytics, '+(SCOPE==='both'?'tracking years ':'tracking year ')+exScopeLabel(),'آفاق البيئة (Afaq Al-Biah) — تحليلات تنافسية للمنافسات، '+(SCOPE==='both'?'سنوات التتبّع':'سنة التتبّع')+' \\u2066'+exScopeLabel()+'\\u2069'",
    'copy', '#25 header year label follows the scope')

# ---------------------------------------------------------------- #3 donuts: one tender, one slice
rep('app', "// ===================== OVERVIEW =====================\n",
    "// one tender, one slice (12 Oct 2026, audit bids-04): «لم تتم الترسية» rows are EH's losses, so they are not counted again\n"
    "function wlSegs(wl){const pend=wl.pending!=null?wl.pending:(wl.in_progress||0)+(wl.no_status||0);\n"
    " return [{l:t('EH won','فاز EH'),v:wl.awarded_eh,c:C.green},{l:t('Lost','خسارة'),v:wl.awarded_other,c:C.red}]\n"
    "  .concat(wl.pending!=null&&wl.not_awarded?[{l:t('Closed, nobody awarded','أُغلقت دون ترسية'),v:wl.not_awarded,c:C.orange}]:[])\n"
    "  .concat([{l:t('Cancelled','ملغاة'),v:wl.cancelled,c:C.soft},{l:t('Pending / in progress','قيد الانتظار / التنفيذ'),v:pend,c:C.blue}]);}\n"
    "// ===================== OVERVIEW =====================\n",
    'data', '#3 shared donut slices')
rep('app', " const segs=[{l:t('EH won','فاز EH'),v:wl.awarded_eh,c:C.green},{l:t('Lost (other won)','خسارة (فاز غيره)'),v:wl.awarded_other,c:C.red},{l:t('Not awarded','لم تتم الترسية'),v:wl.not_awarded,c:C.orange},{l:t('Cancelled','ملغاة'),v:wl.cancelled,c:C.soft}];\n",
    " const segs=wlSegs(wl);\n", 'data', '#3 Overview donut')
rep('app', " const statusSeg=[{l:t('Awarded — EH','مُرساة ل EH'),v:wl.awarded_eh,c:C.green},{l:t('Awarded — other','مُرساة لغيره'),v:wl.awarded_other,c:C.red},{l:t('Not awarded','لم تتم الترسية'),v:wl.not_awarded,c:C.orange},{l:t('Cancelled','ملغاة'),v:wl.cancelled,c:C.soft},{l:t('In progress / pending','قيد التنفيذ / الانتظار'),v:wl.in_progress+wl.no_status,c:C.blue}];\n",
    " const statusSeg=wlSegs(wl);\n", 'data', '#3 Pipeline donut')
rep('app', "${t('Live state across the two tracking years.','الحالة الآنية عبر سنتَي التتبّع.')}",
    "${SCOPE==='both'?t('Live state across the tracking years '+exScopeLabel()+'. Each tender is counted once.','الحالة الآنية عبر سنوات التتبّع '+exScopeLabel()+'. تُحتسب كل منافسة مرة واحدة.'):t('Live state of the '+exScopeLabel()+' tenders. Each tender is counted once.','الحالة الآنية لمنافسات '+exScopeLabel()+'. تُحتسب كل منافسة مرة واحدة.')}",
    'copy', '#25 #3 Pipeline donut note')

# ---------------------------------------------------------------- #29 Win/Loss small samples, readable intensity chart
rep('app', " const byDim=(arr,lab)=>arr.filter(x=>x.awarded>0).map(x=>({l:lab(x),v:Math.round(100*x.won/x.awarded),aw:x.awarded,n:x.count}));\n",
    " const WR_MIN=10;   // same rule as All Tenders: fewer than 10 decided tenders is too few to give a rate (audit bids-27)\n"
    " const byDim=(arr,lab)=>arr.filter(x=>x.awarded>0).map(x=>({l:lab(x),v:Math.round(100*x.won/x.awarded),aw:x.awarded,n:x.count,few:x.awarded<WR_MIN}));\n"
    " const few=t(' · too few to rate',' · عدد أقل من أن يُعطي نسبة'), grey='#B9C4CB';\n",
    'ui', '#29 small-sample flag')
rep('app', "v:Math.round(100*x.won/x.awarded),aw:x.awarded}));\n const wl=BA.winloss;\n const segs=[{l:t('EH won','فاز EH'),v:wl.awarded_eh,c:C.green},{l:t('Competitor won','فاز منافس'),v:wl.awarded_other,c:C.red}];\n",
    "v:Math.round(100*x.won/x.awarded),aw:x.awarded,few:x.awarded<WR_MIN}));\n const wl=BA.winloss;\n const segs=[{l:t('EH won','فاز EH'),v:wl.awarded_eh,c:C.green},{l:t('Competitor won','فاز منافس'),v:wl.awarded_other,c:C.red}];\n",
    'ui', '#29 small-sample flag (rivals)')
rep('app', "${bdr.length?hbar(bdr,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+')',color:d=>wrCol(d.v),rh:42})",
    "${bdr.length?hbar(bdr,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+(d.few?few:'')+')',color:d=>d.few?grey:wrCol(d.v),rh:34,W:520,labw:110,vr:190})",
    'ui', '#29 intensity chart: grey small samples, readable labels')
rep('app', "${hbar(svc,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+t(' decided',' محسومة')+')',color:d=>wrCol(d.v),maxlab:38,rh:54})}",
    "${hbar(svc,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+t(' decided',' محسومة')+(d.few?few:'')+')',color:d=>d.few?grey:wrCol(d.v),maxlab:38,rh:54})}",
    'ui', '#29 service bars')
rep('app', "${plat.length?hbar(plat,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+t(' decided',' محسومة')+')',color:d=>wrCol(d.v),",
    "${plat.length?hbar(plat,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+t(' decided',' محسومة')+(d.few?few:'')+')',color:d=>d.few?grey:wrCol(d.v),",
    'ui', '#29 platform bars')
rep('app', "Each bar = win rate among decided tenders in that band.','عدد المنافسين لا يشمل EH — عدد الشركات في الجدول يشمل EH، لذا حدّة المنافسة = عدد المتقدمين − 1، مجمّعة في نطاقات. كل عمود = نسبة الفوز بين المنافسات المحسومة في ذلك النطاق.')}",
    "Each bar = win rate among decided tenders in that band; grey bars rest on fewer than '+WR_MIN+' decided tenders, too few to give a rate.','عدد المنافسين لا يشمل EH — عدد الشركات في الجدول يشمل EH، لذا حدّة المنافسة = عدد المتقدمين − 1، مجمّعة في نطاقات. كل عمود = نسبة الفوز بين المنافسات المحسومة في ذلك النطاق؛ والأعمدة الرمادية تستند إلى أقل من '+WR_MIN+' منافسات محسومة، وهو عدد أقل من أن يُعطي نسبة.')}",
    'copy', '#29 intensity note explains the grey bars')

# ---------------------------------------------------------------- pricing: one verdict, VAT basis, honest counts
rep('app', "let pxExpand={};\nfunction togglePx(id){pxExpand[id]=!pxExpand[id];renderPricing();}\n",
    "// one verdict on EH's price for the read-out, the chat and the Notes (12 Oct 2026, audit bids-16): a single 20% threshold,\n"
    "// the same one that colours the \"Median gap to lowest\" figure. Prices include VAT (audit bids-03).\n"
    "const PX_HIGH=20;\n"
    "function pxVerdict(s){const hi=(s.median_gap||0)>PX_HIGH;\n"
    " return {hi:hi,en:hi?'EH usually prices well above the lowest bid, a pricing exposure worth reviewing':'EH usually prices close to the lowest bid',\n"
    "  ar:hi?'يسعّر EH عادةً أعلى بكثير من أدنى عرض، وهو انكشاف سعري يستحق المراجعة':'يسعّر EH عادةً قريباً من أدنى عرض'};}\n"
    "function pxCaveat(){const lost=(BA.bidlist||[]).filter(b=>b.outcome=='Lost'), why=lost.filter(b=>(b.lossreason||'').trim()).length, tn=(BA.pricing.rows||[]).filter(r=>r.tech_n).length;\n"
    " return t('Price is one lever, not the whole story: Saudi tenders also score technical merit, compliance and delivery capability, so a high price alone does not prove why a tender was lost. The tracker records a reason for '+why+' of '+lost.length+' lost tenders (grouped on the Executive Summary)'+(tn?', and bid sheets give technical scores for '+tn+' tender'+(tn==1?'':'s'):'; the bid sheets do not yet give technical scores')+'.',\n"
    "  'السعر عامل واحد وليس القصة كلها: تُقيَّم المنافسات السعودية أيضاً على الجدارة الفنية والامتثال وقدرة التنفيذ، فالسعر المرتفع وحده لا يثبت سبب الخسارة. يسجّل الملف سبب الخسارة في '+why+' من '+lost.length+' منافسة خاسرة (مجمّعة في الملخّص التنفيذي)'+(tn?'، وتذكر كشوف المتقدمين درجات فنية في '+tn+' منافسة':'؛ ولا تذكر كشوف المتقدمين درجات فنية بعد')+'.');}\n"
    "function pxGap(s){return (s.median_gap>0?'+':'')+s.median_gap+'%';}\n"
    "function pxReadout(s){const v=pxVerdict(s);\n"
    " return t('Across the '+s.full+' tenders where EH and at least one rival are priced (all prices include VAT), EH was the lowest bidder '+s.cheapest_pct+'% of the time and sat at the '+s.avg_percentile+'th price percentile on average. The median gap to the cheapest bid is '+pxGap(s)+': '+v.en+'. ',\n"
    "  'عبر '+s.full+' منافسة فيها سعر EH وسعر منافس واحد على الأقل (الأسعار كلها شاملة الضريبة)، كان EH صاحب العرض الأدنى في '+s.cheapest_pct+'% من الحالات، وجاء عند المئوي السعري '+s.avg_percentile+' في المتوسط. وسيط الفارق عن أرخص عرض '+pxGap(s)+': '+v.ar+'. ')+pxCaveat();}\n"
    "function pxNote(){const s=BA.pricing.summary, v=pxVerdict(s);\n"
    " return t('On the '+s.full+' tenders where EH and at least one rival are priced (prices include VAT), the median gap to the lowest bid is '+pxGap(s)+': '+v.en+'. ','على '+s.full+' منافسة فيها سعر EH وسعر منافس واحد على الأقل (الأسعار شاملة الضريبة)، وسيط الفارق عن أدنى عرض '+pxGap(s)+': '+v.ar+'. ')+pxCaveat();}\n"
    "let pxExpand={};\n"
    "function togglePx(id){pxExpand[id]=!pxExpand[id];renderPricing();const el=document.querySelector('[onclick=\"togglePx('+id+')\"]');if(el)el.focus();}   // keyboard focus stays on the card (#28)\n",
    'copy', '#17 #28 single pricing verdict and caveat; focus kept on toggle')
rep('app', "   const gapcol=r.gap>50?'#C0504D':r.gap>5?'#E8862E':'#2E7D46';\n",
    "   const gapcls=r.gap>50?'vt-bad':r.gap>5?'vt-warn':'vt-good';\n", 'ui', '#31 gap colour class')
rep('app', "<div style=\"font-weight:700;font-size:12.5px;color:${gapcol}\">${r.gap!=null?",
    "<div class=\"${r.gap!=null?gapcls:''}\" style=\"font-weight:700;font-size:12.5px\">${r.gap!=null?", 'ui', '#31 gap value')
rep('app', "'<span class=\"tag\" style=\"background:#8A99A3\">'+t('CANCELLED','ملغاة')+'</span>'",
    "'<span class=\"tag\" style=\"background:#8A99A3;color:#10171C\">'+t('CANCELLED','ملغاة')+'</span>'", 'ui', '#31 dark text on the grey tag')
rep('app', "${r.n} ${t('bidders','متقدمين')}${r.undisc_count?",
    "${r.n!=null?r.n+' '+t('bidders','متقدمين'):t('bidder count unknown','عدد المتقدمين غير معروف')}${r.undisc_count?",
    'copy', '#15 no invented bidder count')
rep('app', "t(r.undisc_count+' of '+r.n+' bidders had no disclosed value (shown as undisclosed).',r.undisc_count+' من '+r.n+' متقدمين بلا قيمة معلنة (تظهر كغير معلنة).')",
    "t(r.undisc_count+' of '+(r.n!=null?r.n:r.bidders.length)+' bidders had no disclosed value (shown as undisclosed).',r.undisc_count+' من '+(r.n!=null?r.n:r.bidders.length)+' متقدمين بلا قيمة معلنة (تظهر كغير معلنة).')",
    'copy', '#15 undisclosed note with an unknown field size')
rep_re('app', r"\$\{t\('Every tender with a recorded bidder list — '\+s\.tenders\+' in all\. '\+s\.full\+' show EH\\'s price against the full field.*?اختر أي منافسة لعرض القائمة الكاملة\.'\)\}",
    "${t('Every tender with a recorded bidder list — '+s.tenders+' in all. '+s.full+' have EH\\'s price and at least one rival\\'s (the ranking figures below are drawn from these, so they compare EH with the rivals whose price is known, not always the whole field); the rest list the bidders with prices where disclosed and “undisclosed value” otherwise. All prices include 15% VAT, as published on Etimad; EH\\'s own offer is taken from the tracker\\'s with-VAT column. '+s.total_bidders+' disclosed bids across '+s.total_names+' bidder entries. Select any tender for the full list.','كل منافسة لها قائمة متقدمين مُسجّلة — '+s.tenders+' إجمالاً. '+s.full+' منها فيها سعر EH وسعر منافس واحد على الأقل (وتُشتق أرقام الترتيب أدناه منها، فهي تقارن EH بالمنافسين المعروفة أسعارهم لا بكامل المتقدمين دائماً)؛ والباقي يسرد المتقدمين بالأسعار حيث أُعلنت وب«قيمة غير معلنة» فيما عدا ذلك. الأسعار كلها شاملة ضريبة القيمة المضافة 15% كما تُنشر في اعتماد، ويُؤخذ عرض EH من عمود السعر شاملاً الضريبة في ملف المتابعة. '+s.total_bidders+' عرضاً مُعلناً عبر '+s.total_names+' مُدخل متقدم. اختر أي منافسة لعرض القائمة الكاملة.')}",
    'copy', '#23 #1 Pricing subtitle: rival-priced wording and VAT basis')
rep('app', "s.cheapest+t(' of ',' من ')+s.full+t(' full',' كاملة')", "s.cheapest+t(' of ',' من ')+s.full+t(' with a rival priced',' فيها سعر منافس')",
    'copy', '#23 KPI sub-label')
rep('app', "s.full+t(' with full pricing',' بتسعير كامل')", "s.full+t(' with a rival priced',' فيها سعر منافس')", 'copy', '#23 KPI sub-label')
rep_re('app', r"<b>\$\{t\('Read-out:','الخلاصة:'\)\}</b> \$\{t\('Across '\+s\.full\+' tenders with full bidder pricing.*?ورصد الدرجة الفنية وسبب الخسارة لكل منافسة هو ما يسدّ تلك الفجوة\.'\)\}</div>",
    "<b>${t('Read-out:','الخلاصة:')}</b> ${pxReadout(s)}</div>", 'copy', '#17 Pricing read-out computed')

# ---------------------------------------------------------------- competitors / clients / service colour + #27
rep('app', "'+all.length+' distinct competitors across '+BA.pricing.summary.tenders+'+ shared tenders.','كل شركة تقدّمت بعرض ضد EH، مُعاد بناؤها مباشرة من كشوف المتقدمين التفصيلية — '+all.length+' منافساً متمايزاً عبر '+BA.pricing.summary.tenders+'+ منافسة مشتركة.')",
    "'+all.length+' distinct competitors across the '+(BA.pricing.summary.eh_rosters!=null?BA.pricing.summary.eh_rosters:BA.pricing.summary.tenders)+' bid sheets that list EH.','كل شركة تقدّمت بعرض ضد EH، مُعاد بناؤها مباشرة من كشوف المتقدمين التفصيلية — '+all.length+' منافساً متمايزاً عبر '+(BA.pricing.summary.eh_rosters!=null?BA.pricing.summary.eh_rosters:BA.pricing.summary.tenders)+' كشف متقدمين يرد فيه EH.')",
    'copy', '#27 shared-tender count')
rep('app', "<td style=\"color:${c.undercut_pct>=67?'#C0504D':c.undercut_pct>=34?'#E8862E':'#1C2B33'};font-weight:700\">",
    "<td class=\"${c.undercut_pct>=67?'vt-bad':c.undercut_pct>=34?'vt-warn':''}\" style=\"font-weight:700\">", 'ui', '#31 undercut colour')
rep('app', "<td style=\"color:${wrCol(v.awarded?Math.round(100*v.won/v.awarded):null)};font-weight:700\">",
    "<td class=\"${wrCls(v.awarded?Math.round(100*v.won/v.awarded):null)}\" style=\"font-weight:700\">", 'ui', '#31 value-band win rate')
rep('app', "<td style=\"color:${wrCol(c.win_rate)};font-weight:700\">", "<td class=\"${wrCls(c.win_rate)}\" style=\"font-weight:700\">", 'ui', '#31 client win rate')
rep('app', "<td style=\"color:${wrCol(x.win_rate)};font-weight:700\">", "<td class=\"${wrCls(x.win_rate)}\" style=\"font-weight:700\">", 'ui', '#31 service win rate')

# ---------------------------------------------------------------- #16 Bid Turnaround = the client's window
rep_re('app', r"`<div class=\"sech\">\$\{t\('Decision & review duration','مدة القرار والمراجعة'\)\}</div><div class=\"secsub\">\$\{t\('How long the full EH committee review runs.*?برأيهم ويقرّروا\.'\)\}</div>",
    "`<div class=\"sech\">${t('Time allowed to bid','مهلة التقديم')}</div><div class=\"secsub\">${t('How long clients give bidders to respond — the time from a tender being launched to its submission deadline. The client sets this window; EH\\'s committee review, pricing and proposal all have to fit inside it.','المهلة التي يمنحها العملاء للمتقدمين — الزمن من طرح المنافسة حتى الموعد النهائي للتقديم. يحدّد العميل هذه المهلة، ويجب أن تتّسع لمراجعة لجنة EH والتسعير وإعداد العرض.')}</div>",
    'copy', '#16 Turnaround heading and subtitle')
rep('app', "t('Average review duration','متوسط مدة المراجعة')", "t('Average time to bid','متوسط مهلة التقديم')", 'copy', '#16 KPI')
rep('app', "t('Median review duration','وسيط مدة المراجعة')", "t('Median time to bid','وسيط مهلة التقديم')", 'copy', '#16 KPI')
rep_re('app', r"<h3>\$\{t\('How long does the EH committee take to decide\?','كم تستغرق لجنة EH لاتخاذ القرار؟'\)\}</h3><div class=\"note\">.*?\$\{t\(' win rate\.',' نسبة الفوز\.'\)\}</div>",
    "<h3>${t('Time the client allows to bid (launch → deadline)','المهلة التي يتيحها العميل للتقديم (الطرح ← الموعد النهائي)')}</h3><div class=\"note\">${t('Each tender placed into a band by the length of the window from launch to submission deadline. The client sets this window: it is not a measure of how fast EH works, and it is not win rate.','تُصنَّف كل منافسة في شريحة حسب طول المهلة من الطرح حتى الموعد النهائي للتقديم. يحدّد العميل هذه المهلة: فهي ليست مقياساً لسرعة عمل EH، وليست نسبة الفوز.')}</div>",
    'copy', '#16 chart title and note')
rep_re('app', r"<b>\$\{t\('Read-out:','الخلاصة:'\)\}</b> \$\{t\('The EH committee review runs ','تستغرق مراجعة لجنة EH '\)\}.*?تحديد أين تتعثّر المنافسات بدقّة\.'\)\}</i></div></div>",
    "<b>${t('Read-out:','الخلاصة:')}</b> ${t('Clients allow ','يمنح العملاء ')}<b>${t(tu.mean+' days on average',tu.mean+' يوماً في المتوسط')}</b>${t(' from launch to deadline (median '+tu.median+'). The spread matters more: ',' من الطرح حتى الموعد النهائي (الوسيط '+tu.median+'). والتشتّت أهم: ')}<b>${t(tu.tight14+' of '+tu.n,tu.tight14+' من '+tu.n)}</b>${t(' tenders leave two weeks or less, and '+tu.tight7+' a week or less, for EH\\'s committee review and a considered technical and pricing response. ',' منافسة تترك أسبوعين أو أقل، و'+tu.tight7+' أسبوعاً أو أقل، لمراجعة لجنة EH ولاستجابة فنية وسعرية متأنّية. ')}<i>${t('Caveat: windows use the deadline recorded in the tracker; where the client extended the deadline, the real window was longer.','تنبيه: تُحسب المهل من الموعد المسجّل في الملف؛ وحيث مدّد العميل الموعد كانت المهلة الفعلية أطول.')}</i></div></div>",
    'copy', '#16 read-out without the committee wording')
rep('app', "${Math.round(100*22/k2.total)>0?t('a minority of','أقلية من'):t('some','بعض')}",
    "${(k2.guarantee_n||0)<k2.total/2?t('a minority of','أقلية من'):t('some','بعض')}", 'copy', '#30 guarantee share from the data, not 22')
rep_re('app', r"<div class=\"note\">\$\{t\('When the committee decides to pass on a tender, the reason is logged in the comments column\..*?محصورة بعلامة تجارية محددة\.'\)\}</div>",
    "<div class=\"note\">${t('When the committee decides to pass on a tender, the reason is logged in the comments column. These are the declined bids and exactly why; capturing this is how EH learns where to stop spending effort. ','عندما تقرّر اللجنة الاعتذار عن منافسة، يُسجَّل السبب في عمود الملاحظات. هذه هي العروض المرفوضة وأسبابها بدقّة؛ ورصد ذلك هو كيف يتعلّم EH أين يتوقّف عن بذل الجهد. ')}${(function(){const rc=BA.refusal_cats||[], n=(BA.refused||[]).length, top=rc.slice(0,2);if(!top.length)return '';\n"
    "   return t('The most common recorded reasons: '+top.map(c=>c.cat+' ('+c.n+')').join(' and ')+', of '+n+' declines.','أكثر الأسباب المسجّلة: '+top.map(c=>dv(DCAT,c.cat)+' ('+c.n+')').join(' و')+'، من أصل '+n+' اعتذاراً.');})()}</div>",
    'copy', '#30 declined-bids sentence computed from the categories')

# ---------------------------------------------------------------- #5 search keeps focus
rep('app', "function renderTenders(){\n",
    "function renderTenders(){\n const _q=(document.activeElement&&document.activeElement.id==='tq')?[document.activeElement.selectionStart,document.activeElement.selectionEnd]:null;   // keep typing in the search box (audit bids-05)\n",
    'ui', '#5 remember the caret')
rep('app', "<input oninput=\"setTF('q',this.value)\"", "<input id=\"tq\" oninput=\"setTF('q',this.value)\"", 'ui', '#5 search box id')
rep('app', "</tbody></table></div>`;\n}\n// ---- submission timing",
    "</tbody></table></div>`;\n if(_q){const i=$('tq');if(i){i.focus();try{i.setSelectionRange(_q[0],_q[1]);}catch(e){}}}\n}\n// ---- submission timing",
    'ui', '#5 restore focus and caret')

# ---------------------------------------------------------------- Notes
rep('app', " have a recorded decision and '+BA.pricing.summary.full+' have full competitor pricing.",
    " have a recorded decision and '+BA.pricing.summary.full+' have EH\\'s price and at least one rival\\'s.", 'copy', '#23 Notes wording')
rep('app', "' منافسة في هذا النطاق لها قرار مُسجّل و'+BA.pricing.summary.full+' لها تسعير منافسين كامل.",
    "' منافسة في هذا النطاق لها قرار مُسجّل و'+BA.pricing.summary.full+' فيها سعر EH وسعر منافس واحد على الأقل.", 'copy', '#23 Notes wording (AR)')
rep_re('app', r"\[t\('Pricing ≠ full picture','التسعير ≠ الصورة الكاملة'\),t\('The pricing analysis shows EH\\'s losing bids were priced high.*?كان ينافس على نطاق أو جودة أكبر\.'\)\],",
    "[t('Pricing ≠ full picture','التسعير ≠ الصورة الكاملة'),pxNote()],", 'copy', '#17 Notes pricing card uses the single verdict')

# ---------------------------------------------------------------- Executive
rep('app', "function exScopeLabel(){",
    "function exTA(m,a){return m.R?`text-anchor=\"${a}\" direction=\"rtl\"`:`text-anchor=\"${a}\"`;}   // Arabic SVG text: right-to-left run; the anchor is read in that direction (audit bids-20)\n"
    "function exScopeLabel(){", 'ui', '#21 RTL text helper')
rep('app', "function exSvgHead(W,title,sub){ const m=exRTL(W); return `<text x=\"${m.X(14)}\" y=\"20\" text-anchor=\"${m.A('start')}\" class=\"exT\">${esc(title)}</text>${sub?`<text x=\"${m.X(14)}\" y=\"36\" text-anchor=\"${m.A('start')}\" class=\"exS\">${esc(sub)}</text>`:''}`; }",
    "function exSvgHead(W,title,sub){ const m=exRTL(W); return `<text x=\"${m.X(14)}\" y=\"20\" ${exTA(m,'start')} class=\"exT\">${esc(title)}</text>${sub?`<text x=\"${m.X(14)}\" y=\"36\" ${exTA(m,'start')} class=\"exS\">${esc(sub)}</text>`:''}`; }",
    'ui', '#21 chart titles run right-to-left in Arabic')
rep('app', "function exDelta(cur,prev,unit,goodUp){",
    "// win-rate change: grey and \"not significant\" when the likely ranges of the two years overlap (12 Oct 2026, audit bids-22)\n"
    "function exDeltaWR(cur,prev){ if(!cur||!prev||cur.winRate==null||prev.winRate==null)return ''; const a=wilson(cur.wonN,cur.decided), b=wilson(prev.wonN,prev.decided);\n"
    " if(a&&b&&(a[1]<b[0]||b[1]<a[0]))return exDelta(cur.winRate,prev.winRate,'pt',true); const dd=cur.winRate-prev.winRate; if(!dd)return exDelta(0,0,'pt',true);\n"
    " return `<span class=\"exd\">${dd>0?'▲':'▼'} ${Math.abs(dd)} ${t('pts vs prior year · not significant','نقطة عن العام السابق · فرق غير دالّ')}</span>`; }\n"
    "function exDelta(cur,prev,unit,goodUp){", 'ui', '#24 significance-aware win-rate delta')
rep('app', "${delta(x=>x.winRate,null,'pt',true)}", "${other&&cur?exDeltaWR(cur,other):''}", 'ui', '#24 use it on the win-rate KPI')
rep('app', "<span style=\"color:${EXC.stale};font-weight:700\">SAR ${fmtM(d.stale90V)}", "<span class=\"vt-warn\" style=\"font-weight:700\">SAR ${fmtM(d.stale90V)}",
    'ui', '#31 "older than 90 days" colour')
rep('app', "'Each stage shows the count and the share lost from the stage before. Click a stage name to open those tenders.','كل مرحلة تُظهر العدد ونسبة المفقود من المرحلة السابقة. انقر اسم المرحلة لفتح منافساتها.'",
    "'Each stage shows the count and the share lost from the stage before.','كل مرحلة تُظهر العدد ونسبة المفقود من المرحلة السابقة.'", 'copy', '#26 no clickable-stage claim')

# threat matrix: mirrored in Arabic, Arabic text RTL (#21); cover wording (#8); colours (#31)
rep('app', " const xm=P.l+iw*0.5, ym=P.t+ih*0.5;\n", " const xm=P.l+iw*0.5, ym=P.t+ih*0.5, m=exRTL(W);\n", 'ui', '#21 threat: mirror helper')
rep('app', "s+=`<rect x=\"${xm}\" y=\"${P.t}\" width=\"${iw/2}\" height=\"${ih/2}\" fill=\"${EXC.lost}\" fill-opacity=\".06\"/><line x1=\"${xm}\" y1=\"${P.t}\" x2=\"${xm}\" y2=\"${P.t+ih}\" stroke=\"${C.line}\" stroke-dasharray=\"4 4\"/><line x1=\"${P.l}\" y1=\"${ym}\" x2=\"${W-P.r}\" y2=\"${ym}\"",
    "s+=`<rect x=\"${m.B(xm,iw/2)}\" y=\"${P.t}\" width=\"${iw/2}\" height=\"${ih/2}\" fill=\"${EXC.lost}\" fill-opacity=\".06\"/><line x1=\"${m.X(xm)}\" y1=\"${P.t}\" x2=\"${m.X(xm)}\" y2=\"${P.t+ih}\" stroke=\"${C.line}\" stroke-dasharray=\"4 4\"/><line x1=\"${m.X(P.l)}\" y1=\"${ym}\" x2=\"${m.X(W-P.r)}\" y2=\"${ym}\"",
    'ui', '#21 threat: mirrored quadrant')
rep('app', "<text x=\"${W-P.r-6}\" y=\"${P.t+ih*0.5-6}\" text-anchor=\"end\" class=\"exq\">", "<text x=\"${m.X(W-P.r-6)}\" y=\"${P.t+ih*0.5-6}\" ${exTA(m,'end')} class=\"exq\">", 'ui', '#21 threat: quadrant label')
rep('app', "<text x=\"${P.l+6}\" y=\"${P.t+ih*0.5-6}\" class=\"exq\">", "<text x=\"${m.X(P.l+6)}\" y=\"${P.t+ih*0.5-6}\" ${exTA(m,'start')} class=\"exq\">", 'ui', '#21 threat: quadrant label')
rep('app', "<text x=\"${W-P.r-6}\" y=\"${P.t+ih-8}\" text-anchor=\"end\" class=\"exq\">", "<text x=\"${m.X(W-P.r-6)}\" y=\"${P.t+ih-8}\" ${exTA(m,'end')} class=\"exq\">", 'ui', '#21 threat: quadrant label')
rep('app', "s+=`<line x1=\"${P.l}\" y1=\"${y}\" x2=\"${W-P.r}\" y2=\"${y}\" stroke=\"${C.line}\" stroke-opacity=\".6\"/><text x=\"${P.l-8}\" y=\"${y+3}\" text-anchor=\"end\" class=\"cax\">",
    "s+=`<line x1=\"${m.X(P.l)}\" y1=\"${y}\" x2=\"${m.X(W-P.r)}\" y2=\"${y}\" stroke=\"${C.line}\" stroke-opacity=\".6\"/><text x=\"${m.X(P.l-8)}\" y=\"${y+3}\" text-anchor=\"${m.A('end')}\" class=\"cax\">",
    'ui', '#21 threat: y axis')
rep('app', "const x=P.l+i/xmax*iw;s+=`<text x=\"${x}\" y=\"${H-P.b+16}\"", "const x=m.X(P.l+i/xmax*iw);s+=`<text x=\"${x}\" y=\"${H-P.b+16}\"", 'ui', '#21 threat: x ticks')
rep('app', "return [P.l+c.encounters/xmax*iw+j,P.t+ih-c.undercut_pct/YS*ih];};", "return [m.X(P.l+c.encounters/xmax*iw+j),P.t+ih-c.undercut_pct/YS*ih];};", 'ui', '#21 threat: points mirrored')
rep('app', "text-anchor=\"middle\" class=\"chs\">${esc(String(c.name).slice(0,26))}</text>", "${exTA(m,'middle')} class=\"chs\">${esc(String(c.name).slice(0,26))}</text>", 'ui', '#21 threat: name labels RTL')
rep('app', "s+=`<text x=\"${P.l+iw/2}\" y=\"${H-4}\" text-anchor=\"middle\" class=\"caxt\">${esc(t('Shared tenders with EH','منافسات مشتركة مع EH'))}",
    "s+=`<text x=\"${m.X(P.l+iw/2)}\" y=\"${H-4}\" ${exTA(m,'middle')} class=\"caxt\">${esc(t('Shared tenders with EH','منافسات مشتركة مع EH'))}", 'ui', '#21 threat: axis title RTL')
rep('app', "${c.wins?`<b style=\"color:${EXC.lost}\">${c.wins}</b>`:", "${c.wins?`<b class=\"vt-bad\">${c.wins}</b>`:", 'ui', '#31 wins colour')
rep('app', "<td style=\"text-align:center;color:${c.undercut_pct==null?'#8A99A3':col(c)};font-weight:700\">",
    "<td class=\"${c.undercut_pct==null?'':c.undercut_pct>=67?'vt-bad':c.undercut_pct>=34?'vt-warn':''}\" style=\"text-align:center;${c.undercut_pct==null?'color:#8A99A3;':''}font-weight:700\">", 'ui', '#31 share colour')
rep('app', " const grp=(lbl,col2)=>`<tr><td colspan=\"6\" style=\"background:${col2}12;color:${col2};",
    " const grp=(lbl,col2)=>`<tr><td colspan=\"6\" class=\"${col2===EXC.lost?'vt-bad':''}\" style=\"background:${col2}12;color:${col2};", 'ui', '#31 "Have beaten EH" label readable in dark mode')
rep('app', "competitors have at least one tender priced against EH (${unpriced} never disclosed a price) ·", "competitors have at least one tender priced against EH (${unpriced} with no price known against EH's) ·",
    'copy', '#8 cover wording')
rep('app', "منافساً لديهم منافسة واحدة على الأقل مُسعَّرة مقابل EH (${unpriced} لم يُفصحوا عن سعر) ·", "منافساً لديهم منافسة واحدة على الأقل مُسعَّرة مقابل EH (${unpriced} بلا سعر معروف مقابل سعر EH) ·",
    'copy', '#8 cover wording (AR)')

# price position: computed verdict, VAT note, mirrored in Arabic (#2 #1 #21)
_m = re.search(r"\n( const reasons=\{\}; d\.lost\.forEach.*?\n)( const rr=.*?\n)", FILES['app'], re.S)
if not _m: FAILURES.append({'file': 'app', 'note': 'exPrice reasons block not found', 'old': ''}); _keep = ''
else: _keep = _m.group(1) + _m.group(2)
NEW_EXPRICE = (
 "function exPrice(B,d){\n"
 " const rows=(B.pricing&&B.pricing.rows||[]).filter(r=>r.eh&&r.n_priced>1&&r.gap!=null).sort((a,b)=>a.gap-b.gap);\n"
 " const sm=B.pricing&&B.pricing.summary||{};\n"
 " // computed verdict (12 Oct 2026, audit bids-02): wins where EH was / was not the lowest priced bidder, decided tenders only\n"
 " const dec=r=>r.won===true||r.won===false, low=rows.filter(r=>r.rank===1&&dec(r)), notLow=rows.filter(r=>r.rank!==1&&dec(r));\n"
 " const lowest=rows.filter(r=>r.rank===1).length, lowWon=low.filter(r=>r.won).length, notLowWon=notLow.filter(r=>r.won).length;\n"
 " const gs=rows.map(r=>r.gap).sort((a,b)=>a-b), medGap=gs.length?(gs.length%2?gs[gs.length>>1]:(gs[gs.length/2-1]+gs[gs.length/2])/2):null;   // median of the bars drawn\n"
 " const CAP=300, W=wd, bh=14, H=64+rows.length*bh+34, x0=64, iw=W-x0-90, m=exRTL(W);\n"
 " let s=`<svg id=\"ex-price\" viewBox=\"0 0 ${W} ${H}\" class=\"ch exsvg\">${exSvgHead(W,t('How far above the lowest bid EH priced, tender by tender','كم كان سعر EH فوق أدنى عرض، منافسة بمنافسة'),t('one bar per tender with two or more disclosed prices · prices include VAT · 0% = EH was the lowest bidder · green = EH won','شريط لكل منافسة فيها سعران مُفصَحان أو أكثر · الأسعار شاملة الضريبة · 0% = EH الأدنى سعراً · الأخضر = فاز EH'))}`;\n"
 " [0,50,100,150,200,250,300].forEach(v=>{const x=m.X(x0+iw*v/CAP);s+=`<line x1=\"${x}\" y1=\"${52}\" x2=\"${x}\" y2=\"${56+rows.length*bh}\" stroke=\"${C.line}\"/><text x=\"${x}\" y=\"${56+rows.length*bh+14}\" text-anchor=\"middle\" class=\"cax2\" direction=\"ltr\">${v===CAP?'≥':''}${v}%</text>`;});\n"
 " rows.forEach((r,i)=>{const y=54+i*bh, g=Math.max(0,r.gap), w=Math.max(2,Math.min(g,CAP)/CAP*iw);const c=r.won?EXC.won:(r.status==='Awarded'||r.has_winner)?EXC.lost:EXC.pend;\n"
 "  s+=`<text x=\"${m.X(x0-6)}\" y=\"${y+10}\" text-anchor=\"${m.A('end')}\" class=\"cax\" direction=\"ltr\">#${r.sn}/${String(r.year).slice(2)}</text><rect x=\"${m.B(x0,w).toFixed(1)}\" y=\"${y+2}\" width=\"${w.toFixed(1)}\" height=\"${bh-4}\" rx=\"2\" fill=\"${c}\" fill-opacity=\"${r.level==='full'?0.9:0.45}\"><title>#${r.sn}/${String(r.year).slice(2)} ${esc(r.title||'')} · EH +${Math.round(g)}% ${esc(t('above the lowest bid','فوق أدنى عرض'))} · ${r.rank}/${r.n_priced} ${esc(t('by price','بالسعر'))}${r.won?' · '+esc(t('EH won','فاز EH')):''}</title></rect>`;\n"
 "  s+=`<text x=\"${m.X(x0+w+5).toFixed(1)}\" y=\"${y+10}\" text-anchor=\"${m.A('start')}\" class=\"chs\" direction=\"ltr\">+${Math.round(g)}%${r.won?' ✓':''}</text>`;});\n"
 " s+=`<text x=\"${m.X(x0)}\" y=\"${H-6}\" ${exTA(m,'start')} class=\"chs\">${esc(t('Faded bar = only part of the field disclosed a price','الشريط الباهت = جزء من المتنافسين فقط أفصح عن سعره'))}</text></svg>`;\n"
 " const mg=medGap!=null?Math.round(medGap):'—', mw=sm.median_win_gap!=null?Math.round(sm.median_win_gap):'—';\n"
 " const head=t(`Of ${sm.tenders||rows.length} tenders with price data, ${rows.length} have two or more disclosed prices (all prices include VAT). EH was the lowest bidder in ${lowest} of them. Where the result is known, EH won ${lowWon} of the ${low.length} tenders in which it was the lowest bidder and ${notLowWon} of the ${notLow.length} in which it was not. Typically EH priced ${mg}% above the lowest bid (median of the bars below); where EH lost to a known winner, its price was a median ${mw}% above the winning bid (n = ${sm.win_gap_n||0}).`,"
 "`من ${sm.tenders||rows.length} منافسة ببيانات أسعار، ${rows.length} فيها سعران مُفصَحان أو أكثر (الأسعار كلها شاملة الضريبة). كان EH الأدنى سعراً في ${lowest} منها. وحيث عُرفت النتيجة، فاز EH ب ${lowWon} من ${low.length} منافسة كان فيها الأدنى سعراً، و${notLowWon} من ${notLow.length} لم يكن فيها الأدنى. عادةً سعّر EH ${mg}% فوق أدنى عرض (وسيط الأشرطة أدناه)؛ وحيث خسر EH أمام فائز معروف كان سعره بوسيط ${mw}% فوق العرض الفائز (ن = ${sm.win_gap_n||0}).`);\n"
 + _keep +
 " return `<div class=\"card exc\"><div class=\"exh\"><h3>${t('Price position — EH won '+lowWon+' of '+low.length+' decided tenders where it was the lowest bidder, '+notLowWon+' of '+notLow.length+' where it was not','موقع السعر — فاز EH ب '+lowWon+' من '+low.length+' منافسة محسومة كان فيها الأدنى سعراً، و'+notLowWon+' من '+notLow.length+' لم يكن فيها الأدنى')}</h3>${exBtn('ex-price','price_position')}</div>\n"
 "  <div class=\"excov\">${head}</div>\n"
 "  <div class=\"grid g3 exg3\"><div>${s}</div><div><div class=\"note\" style=\"margin-bottom:6px\"><b>${t('Recorded loss reasons','أسباب الخسارة المُسجَّلة')}</b> · ${d.lostN} ${t('lost','مفقودة')}</div><table class=\"t ext\"><tbody>${rr}</tbody></table></div></div></div>`;\n"
 "}\n")
rep_re('app', r"function exPrice\(B,d\)\{\n.*?\n\}\n(?=// ---- 6\. decisions \+ watchlist)", lambda mm: NEW_EXPRICE, 'copy', '#2 #1 #21 price position: computed verdict, VAT basis, Arabic mirrored')

# ---------------------------------------------------------------- chat (#4 #16 #17 #18 #22)
rep('app', "  open(){\n    const P=BA.bidlist.filter(x=>!x.decided&&(x.status||'')!=='Cancelled');\n",
    "  open(){\n    const P=BA.bidlist.filter(x=>x.outcome==='Pending');   // tenders with no result yet (audit bids-01: the bid list has no 'decided' field)\n",
    'data', '#4 open pipeline lists pending tenders only')
rep('app', "    return listAns('Open pipeline — SAR '+fmtM2(BA.kpi.open_pipeline)+' across '+BA.kpi.open_count+' open tenders",
    "    return listAns('Open pipeline — SAR '+fmtM2(BA.kpi.open_pipeline)+' across '+P.length+' open tenders", 'data', '#4 count from the same list')
rep('app', "'المنافسات المفتوحة — '+fmtM2(BA.kpi.open_pipeline)+' ريال عبر '+BA.kpi.open_count+' منافسة؛",
    "'المنافسات المفتوحة — '+fmtM2(BA.kpi.open_pipeline)+' ريال عبر '+P.length+' منافسة؛", 'data', '#4 count from the same list (AR)')
rep_re('app', r"  recent\(\)\{\n    const d=BA\.bidlist\.filter\(x=>x\.decided\).*?\n  \},\n",
    "  recent(){\n"
    "    const d=BA.bidlist.filter(x=>x.outcome==='Won'||x.outcome==='Lost').sort((a,b)=>(b.awarddate||'').localeCompare(a.awarddate||'')||(b.year-a.year)||(b.sn-a.sn)).slice(0,6);   // audit bids-17\n"
    "    return listAns('Latest recorded award decisions, newest award date first (results without an award date follow)','أحدث قرارات الترسية المسجّلة، الأحدث تاريخ ترسية أولاً (تليها النتائج بلا تاريخ ترسية)',\n"
    "      d.map(x=>({name:'#'+x.sn+'/'+String(x.year).slice(2),sub:(x.title||'').slice(0,44)+(x.awarddate?' · '+x.awarddate:''),val:t(x.outcome==='Won'?'EH won':'Lost',DOUT[x.outcome]||x.outcome)})));\n"
    "  },\n",
    'data', '#18 latest decisions from outcomes and award dates')
rep_re('app', r" freq\(\)\{.*?\n service\(\)\{[^\n]*\n",
    " freq(){const c=[...BA.competitors].sort((a,b)=>b.encounters-a.encounters).slice(0,7);return listAns('Who competes against EH the most — by tenders faced','من ينافس EH أكثر — حسب عدد المنافسات',c.map(x=>({name:x.name,val:x.encounters+t(' tenders',' منافسة'),sub:x.wins?x.wins+t(' beat EH',' فوز على EH'):''})));},\n"
    " beatEH(){const c=[...BA.competitors].filter(x=>x.wins>0).sort((a,b)=>b.wins-a.wins).slice(0,7);if(!c.length)return ansBox('No single competitor has a recorded win over EH','لا يوجد منافس بعينه تغلّب على EH',t('In the tracked outcomes, EH losses are not concentrated on one named competitor.','في النتائج المتتبَّعة، لا تتركّز خسائر EH على منافس مسمّى واحد.'));return listAns('Who beats EH the most — recorded wins over EH','من يتغلب على EH أكثر',c.map(x=>({name:x.name,val:x.wins+t(x.wins>1?' wins':' win',' فوز'),sub:t('faced '+x.encounters+'x','واجهه '+x.encounters+' مرة')})));},\n"
    " losing(){const s=[...BA.service_mix].filter(x=>x.awarded>0).sort((a,b)=>a.win_rate-b.win_rate);return listAns('Where EH loses most — service lines by win rate (decided tenders)','أين تخسر EH أكثر — حسب مجال الخدمة',s.map(x=>({name:dv(DSVC,x.name),val:x.win_rate+t('% win rate','% نسبة الفوز'),sub:t(x.won+' of '+x.awarded+' won',x.won+' فوز من '+x.awarded)})));},\n"
    " biggest(){const c=[...BA.competitors].sort((a,b)=>(b.wins-a.wins)||(b.encounters-a.encounters)).slice(0,7);return listAns(`EH's biggest competitors — wins over EH, then frequency`,'أبرز منافسي EH',c.map(x=>({name:x.name,val:(x.wins?x.wins+t(' beat EH · ',' فوز على EH · '):'')+x.encounters+t(' faced',' مواجهة'),sub:x.undercut_pct!=null?t('undercut EH '+x.undercut_pct+'% of priced meets','سعّر دون EH في '+x.undercut_pct+'% من المواجهات المسعّرة'):''})));},\n"
    " pricing(){const s=BA.pricing.summary, v=pxVerdict(s);return ansBox(v.hi?'EH pricing looks high versus the lowest bids':'EH pricing is close to the lowest bids',v.hi?'أسعار EH مرتفعة مقارنة بأدنى العروض':'أسعار EH قريبة من أدنى العروض',\n"
    "  t(`Across the <b>${s.full}</b> tenders where EH and at least one rival are priced (all prices include VAT), EH was the outright cheapest bidder <b>${s.cheapest_pct}%</b> of the time and sat at the <b>${s.avg_percentile}th</b> price percentile on average (1st = cheapest). Median gap to the lowest bid: <b>${pxGap(s)}</b>: ${v.en}.`,`عبر <b>${s.full}</b> منافسة فيها سعر EH وسعر منافس واحد على الأقل (الأسعار كلها شاملة الضريبة)، كان EH الأرخص صراحةً في <b>${s.cheapest_pct}%</b> من الحالات، وجاء عند المئوي السعري <b>${s.avg_percentile}</b> في المتوسط (1 = الأرخص). وسيط الفارق عن أدنى عرض: <b>${pxGap(s)}</b>: ${v.ar}.`)+`<br><span style=\"color:#5F7078\">${pxCaveat()}</span>`);},\n"
    " time(){const tu=BA.turnaround;const rushed=tu.tight14/tu.n;return ansBox('Time clients allow to bid (launch → deadline)','المهلة التي يتيحها العملاء للتقديم (الطرح ← الموعد النهائي)',\n"
    "  t(`Clients allow <b>${tu.mean} days on average</b> from launch to submission deadline (median ${tu.median}). <b>${tu.tight14} of ${tu.n}</b> tenders leave two weeks or less, and <b>${tu.tight7}</b> a week or less, for EH's committee review and a considered technical and pricing response. ${rushed>=0.3?'A meaningful share are rushed, which can push EH toward weaker or higher-priced bids.':'Most tenders leave a reasonable window.'}`,\n"
    "    `يمنح العملاء <b>${tu.mean} يوماً في المتوسط</b> من الطرح حتى الموعد النهائي للتقديم (الوسيط ${tu.median}). <b>${tu.tight14} من ${tu.n}</b> منافسة تترك أسبوعين أو أقل، و<b>${tu.tight7}</b> أسبوعاً أو أقل، لمراجعة لجنة EH ولاستجابة فنية وسعرية متأنّية. ${rushed>=0.3?'نسبة معتبرة منها مستعجلة، وهذا قد يدفع EH إلى عروض أضعف أو أعلى سعراً.':'معظم المنافسات تترك مهلة معقولة.'}`));},\n"
    " status(){const {yr,sn,t:b}=_tender();if(!yr||!sn)return ansBox('Enter a tender number and year first','أدخل رقم المنافسة والسنة أولاً',t('Use the two boxes at the top of this tab, then tap the question again.','استخدم الخانتين أعلاه ثم اضغط السؤال مرة أخرى.'));if(!b)return ansBox('Tender not found','المنافسة غير موجودة',t(`No tender #${sn} for ${yr} is in the tracker.`,`لا توجد المنافسة رقم ${sn} لعام ${yr} في ملف المتابعة.`));const oc=t(b.outcome,DOUT[b.outcome]||b.outcome);return ansBox(`Tender #${sn}/${yr} — ${b.outcome}`,`المنافسة رقم ${sn}/${yr} — ${OUT_AR[b.outcome]||b.outcome}`,`<b dir=\"auto\">${esc(b.title)||t('(untitled)','(بلا عنوان)')}</b><br>${t('Client','العميل')}: <span dir=\"auto\">${esc(b.client)||'—'}</span> · ${t('Platform','المنصة')}: ${esc(dv(DPLAT,platN(b.platform)))}<br>${t('Outcome','النتيجة')}: <b>${oc}</b>${b.winner?' · '+t('Winner','الفائز')+': <span dir=\"auto\">'+esc(b.winner)+'</span>':''}${b.value?' · '+t('Value','القيمة')+': '+fmtSAR(b.value):''}${b.nbid?' · '+b.nbid+t(' bidders',' متقدمين'):''}${b.date?' · '+t('Launched ','طُرحت ')+b.date:''}`);},\n"
    " why(){const {yr,sn,t:b}=_tender();if(!yr||!sn)return ansBox('Enter a tender number and year first','أدخل رقم المنافسة والسنة أولاً',t('Use the two boxes at the top of this tab, then tap the question again.','استخدم الخانتين أعلاه ثم اضغط السؤال مرة أخرى.'));if(!b)return ansBox('Tender not found','المنافسة غير موجودة',t(`No tender #${sn} for ${yr} is in the tracker.`,`لا توجد المنافسة رقم ${sn} لعام ${yr} في ملف المتابعة.`));let h=`<b dir=\"auto\">${esc(b.title)||t('(untitled)','(بلا عنوان)')}</b><br>`;if(b.committee)h+=`${t('Bid-committee decision','قرار لجنة المنافسات')}: <b dir=\"auto\">${esc(b.committee)}</b><br>`;if(b.reason)h+=`${t('Recorded note / reason','الملاحظة / السبب المسجّل')}: <span dir=\"auto\">${esc(b.reason)}</span><br>`;if(!b.committee&&!b.reason)h+=t('No committee decision or reason is recorded for this tender in the tracker.','لا قرار لجنة ولا سبب مسجّلاً لهذه المنافسة في ملف المتابعة.');return ansBox(`Why tender #${sn}/${yr}?`,`لماذا المنافسة ${sn}/${yr}؟`,h);},\n"
    " service(){const s=[...BA.service_mix].sort((a,b)=>b.count-a.count);return listAns('Most-requested service lines — by tender count','الخدمات الأكثر طلباً — حسب عدد المنافسات',s.map(x=>({name:dv(DSVC,x.name),val:x.count+t(' tenders',' منافسة'),sub:fmtSAR(x.value)+t(' total',' إجمالاً')})));},\n",
    'copy', '#16 #17 #22 chat answers: Arabic bodies, one pricing verdict, client window wording')
rep('app', "['time','Does the committee allow enough time to bid?','هل تمنح لجنة EH وقتاً كافياً للتقديم؟']",
    "['time','Do clients allow enough time to bid?','هل يمنح العملاء وقتاً كافياً للتقديم؟']", 'copy', '#16 chat question')
rep('app', "'يفوز','يتغلب','يغلب','يهزم','يفوز علينا'],", "'يفوز','يتغلب','يغلب','يهزم','يفوز علينا','يكسب','بيكسب','علينا','يغلبنا'],",
    'copy', '#22 colloquial Arabic keywords')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(J, 'w', encoding='utf-8').write(FILES['app'])
open(CH, 'w', encoding='utf-8').write(FILES['charts'])
write_change_table(os.path.join(HERE, 'change_table_audit_bids'), 'Audit fixes (J1) — Bid & Tender page')
print('patched: app.js, charts.js')
