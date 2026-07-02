const BA=JSON.parse(document.getElementById('BA').textContent);
const $=id=>document.getElementById(id);
const pct=v=>v==null?'—':v+'%';
const wrCol=v=>v==null?C.soft:(v>=50?C.green:v>=30?C.orange:C.red);
const RCAT={'Out of scope of EH':'#E8862E','Service not offered':'#7B6BA8','Missing licence / qualification':'#2A9D8F','Vendor / partner risk':'#D4A92E','Other / not specified':'#9AABB5'};
// ---------- i18n ----------
let L='en',curTab='overview';
const t=(en,ar)=>L==='ar'?ar:en;
const DOUT={'Won':'فوز','Lost':'خسارة','Not awarded':'لم تتم الترسية','Cancelled':'ملغاة','Pending':'قيد الدراسة'};
const DCAT={'Out of scope of EH':'خارج نطاق عمل EH','Service not offered':'خدمة غير مقدَّمة','Missing licence / qualification':'نقص ترخيص / تأهيل','Vendor / partner risk':'مخاطر مورّد / شريك','Other / not specified':'أخرى / غير محددة'};
const DSVC={'Environmental Studies / EIA':'دراسات بيئية / تقييم الأثر','Unclassified':'غير مصنّف','Environmental Services':'خدمات بيئية','Training':'تدريب','Env. Services':'خدمات بيئية','Env. Studies / EIA':'دراسات بيئية / تقييم الأثر'};
const DPLAT={'Etimad':'اعتماد','SAP Ariba':'ساب أريبا','SEC-SAP':'SEC-SAP','Email / direct':'بريد / مباشر','Other / client portal':'أخرى / بوابة العميل','Email':'بريد','Other':'أخرى'};
const DDUR={'≤3 mo':'≤3 أشهر','4–6 mo':'4–6 أشهر','7–12 mo':'7–12 شهر','13–24 mo':'13–24 شهر','25+ mo':'+25 شهر'};
const dv=(m,v)=>L==='ar'?(m[v]||v):v;

// ---------- NAV ----------
const TABS=[['overview','Overview','نظرة عامة'],['pipeline','Pipeline & Timeline','المنافسات والجدول الزمني'],['winloss','Win / Loss','الفوز / الخسارة'],['pricing','Pricing Intelligence','تحليل الأسعار'],['competitors','Competitors','المنافسون'],['clients','Clients','العملاء'],['service','Service & Platform','الخدمات والمنصات'],['funnel','Bid Turnaround','مدة اتخاذ القرار'],['tenders','All Tenders','جميع المنافسات'],['watchlist','Watchlist','قائمة المتابعة'],['limitations','Notes & Limits','ملاحظات وحدود']];
function rNav(){$('nav').innerHTML=TABS.map(([id,en,ar])=>`<a id="t-${id}" class="${curTab==id?'on':''}" onclick="go('${id}')">${t(en,ar)}</a>`).join('');}
function go(id){curTab=id;TABS.forEach(([tt])=>{$('t-'+tt).classList.toggle('on',tt==id);$('s-'+tt).classList.toggle('on',tt==id);});window.scrollTo(0,0);}

// ---------- KPI STRIP ----------
const k=BA.kpi;
function kc(v,l,d,cls){return `<div class="kc"><div class="v ${cls||''}">${v}</div><div class="l">${l}</div>${d?`<div class="d">${d}</div>`:''}</div>`;}
function rKPI(){$('kstrip').innerHTML=
 kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),'2024–2026')+
 kc('SAR '+fmtM(k.pipeline),t('Pipeline value','قيمة المحفظة'),k.with_value+t(' priced',' مُسعّرة'))+
 kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/'+k.awarded+t(' awarded',' مُرساة'),k.win_rate>=50?'g':'r')+
 kc(k.competitors,t('Competitors faced','المنافسون المواجَهون'),t('head-to-head','مواجهة مباشرة'))+
 kc(k.avg_bidders,t('Avg bidders/tender','متوسط المتقدمين للمنافسة'),t('max ','الأقصى ')+k.max_bidders)+
 kc(Math.round(100*k.committee_accept/k.committee_total)+'%',t('Bid selectivity','انتقائية التقديم'),k.committee_accept+'/'+k.committee_total+t(' accepted',' مقبولة'))+
 kc('SAR '+fmtM(k.median_value),t('Median tender','وسيط قيمة المنافسة'),t('typical size','الحجم النموذجي'));}

// ===================== OVERVIEW =====================
function rOverview(){
 const wl=BA.winloss;
 const t2=BA.trajectory;
 const segs=[{l:t('EH won','فاز EH'),v:wl.awarded_eh,c:C.green},{l:t('Lost (other won)','خسارة (فاز غيره)'),v:wl.awarded_other,c:C.red},{l:t('Not awarded','لم تتم الترسية'),v:wl.not_awarded,c:C.orange},{l:t('Cancelled','ملغاة'),v:wl.cancelled,c:C.soft}];
 $('s-overview').innerHTML=
 `<div class="sech">${t('Executive overview','ملخّص تنفيذي')}</div><div class="secsub">${t('Headline performance across the tender pipeline, win/loss outcome, and the year-on-year trajectory.','الأداء العام عبر محفظة المنافسات، ونتائج الفوز/الخسارة، والمسار السنوي.')}</div>
 <div style="background:#FFF8EC;border:1px solid #F0DDB0;border-left:4px solid #E8862E;border-radius:9px;padding:11px 14px;margin-bottom:16px;font-size:12.5px;color:#5A4A2E">
 <b>${t('Read this dashboard as directional, not definitive.','اقرأ هذه اللوحة كمؤشرات توجيهية لا كأرقام قاطعة.')}</b> ${t('Win-rate and pricing figures rest on a small recorded sample (only a fraction of the '+k.total+' tenders have a recorded outcome; '+BA.pricing.summary.tenders+' have bidder pricing), and 2026 is a partial year. See the ','تعتمد أرقام نسبة الفوز والأسعار على عيّنة صغيرة مُسجّلة (نسبة يسيرة فقط من '+k.total+' منافسة لها نتيجة مُسجّلة؛ '+BA.pricing.summary.tenders+' منها لها أسعار متقدمين)، و2026 سنة جزئية. راجع ')}<a onclick="go('limitations')" style="color:#1A5FAB;cursor:pointer;font-weight:600;text-decoration:underline">${t('Notes & Limits','ملاحظات وحدود')}</a>${t(' tab for the full caveats.',' للاطّلاع على التحفّظات الكاملة.')}</div>
 <div class="grid g2">
   <div class="card"><h3>${t('Outcome of tracked tenders','نتائج المنافسات المتتبَّعة')}</h3><div class="note">${t('Of '+k.total+' tenders, '+k.awarded+' have a recorded award decision. The rest are in progress or pending in the tracker.','من أصل '+k.total+' منافسة، '+k.awarded+' لها قرار ترسية مُسجّل. والباقي قيد التنفيذ أو الانتظار في الجدول.')}</div>
     <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;justify-content:center">${donut(segs,{center:pct(k.win_rate),csub:t('WIN RATE','نسبة الفوز')})}<div>${legend(segs)}</div></div></div>
   <div class="card"><h3>${t('2025 → 2026 trajectory','مسار 2025 → 2026')}</h3><div class="note">${t('Tender volume held up but win rate fell sharply — the central competitive concern.','صمد حجم المنافسات لكن نسبة الفوز انخفضت بحدّة — وهو الشاغل التنافسي الأبرز.')}</div>
     ${cardRow([[t('Tenders','المنافسات'),t2[2025].bids+' → '+t2[2026].bids,''],[t('Win rate','نسبة الفوز'),pct(t2[2025].win_rate)+' → '+pct(t2[2026].win_rate),t2[2026].win_rate<t2[2025].win_rate?'down':''],[t('Pipeline','المحفظة'),'SAR '+fmtM(t2[2025].pipeline)+' → '+fmtM(t2[2026].pipeline),''],[t('Avg bidders','متوسط المتقدمين'),t2[2025].avg_bidders+' → '+t2[2026].avg_bidders,'']])}</div>
 </div>`;
}
function cardRow(items){return '<div class="cardrow">'+items.map(([l,v,f])=>`<div class="metric"><div class="mv" style="${f=='down'?'color:#C0504D':''}">${v}</div><div class="ml">${l}</div></div>`).join('')+'</div>';}

// ===================== PIPELINE & TIMELINE =====================
function rPipeline(){
 const vb=BA.value_bands;
 const wl=BA.winloss;
 const statusSeg=[{l:t('Awarded — EH','مُرساة لـ EH'),v:wl.awarded_eh,c:C.green},{l:t('Awarded — other','مُرساة لغيره'),v:wl.awarded_other,c:C.red},{l:t('Not awarded','لم تتم الترسية'),v:wl.not_awarded,c:C.orange},{l:t('Cancelled','ملغاة'),v:wl.cancelled,c:C.soft},{l:t('In progress / pending','قيد التنفيذ / الانتظار'),v:wl.in_progress+wl.no_status,c:C.blue}];
 $('s-pipeline').innerHTML=
 `<div class="sech">${t('Pipeline & timeline','المنافسات والجدول الزمني')}</div><div class="secsub">${t('When tenders arrive, how much value is in play, and what stage they are at.','متى تصل المنافسات، وحجم القيمة المطروحة، وفي أي مرحلة هي.')}</div>
 <div class="card"><h3>${t('Pipeline value launched per month','قيمة المنافسات المطروحة شهرياً')}</h3><div class="note">${t('Sum of EH offer/estimated value for tenders launched each month (partial — only '+k.with_value+' of '+k.total+' tenders carry a value).','مجموع قيمة عرض/تقدير EH للمنافسات المطروحة كل شهر (جزئي — '+k.with_value+' من '+k.total+' منافسة فقط لها قيمة).')}</div>
   ${barChart(BA.timeline,{val:d=>d.value,lab:d=>d.month.slice(2),fmt:v=>fmtM(v),color:C.green,h:240})}</div>
 <div class="grid g2">
  <div class="card"><h3>${t('Current status of all tenders','الحالة الحالية لجميع المنافسات')}</h3><div class="note">${t('Live state across the two tracking years.','الحالة الآنية عبر سنتَي التتبّع.')}</div>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;justify-content:center">${donut(statusSeg,{center:k.total,csub:t('TENDERS','منافسات')})}<div>${legend(statusSeg)}</div></div></div>
  <div class="card"><h3>${t('Tenders by value band','المنافسات حسب شريحة القيمة')}</h3><div class="note">${t('Distribution of tender sizes (where a value is recorded).','توزيع أحجام المنافسات (حيث سُجّلت قيمة).')}</div>
    ${barChart(vb,{val:d=>d.count,lab:d=>d.band,fmt:v=>v,color:d=>C.pal[vb.indexOf(d)%C.pal.length],h:210})}
    <table class="t" style="margin-top:12px"><thead><tr><th>${t('Band','الشريحة')}</th><th>${t('Tenders','المنافسات')}</th><th>${t('Total value','إجمالي القيمة')}</th><th>${t('EH win rate','نسبة فوز EH')}</th></tr></thead><tbody>
    ${vb.map(v=>`<tr><td><b>${v.band}</b></td><td>${v.count}</td><td>${fmtSAR(v.value)}</td><td style="color:${wrCol(v.awarded?Math.round(100*v.won/v.awarded):null)};font-weight:700">${v.awarded?Math.round(100*v.won/v.awarded)+'%':'—'}</td></tr>`).join('')}</tbody></table></div>
 </div>`;
}

// ===================== WIN / LOSS =====================
function rWinloss(){
 const byDim=(arr,lab)=>arr.filter(x=>x.awarded>0).map(x=>({l:lab(x),v:Math.round(100*x.won/x.awarded),aw:x.awarded,n:x.count}));
 const svc=byDim(BA.service_mix,x=>dv(DSVC,x.name));
 const plat=byDim(BA.platform_mix,x=>dv(DPLAT,x.name));
 const vb=byDim(BA.value_bands,x=>x.band);
 const bdr=BA.bidder_dist.filter(x=>x.awarded>0).map(x=>({l:x.n+t(' bidders',' متقدمين'),v:Math.round(100*x.won/x.awarded),aw:x.awarded}));
 const wl=BA.winloss;
 const segs=[{l:t('EH won','فاز EH'),v:wl.awarded_eh,c:C.green},{l:t('Competitor won','فاز منافس'),v:wl.awarded_other,c:C.red}];
 $('s-winloss').innerHTML=
 `<div class="sech">${t('Win / loss performance','أداء الفوز / الخسارة')}</div><div class="secsub">${t('Where EH converts and where it does not. Win rates are over tenders with a recorded outcome — a small but telling sample ('+k.awarded+' awarded).','أين يفوز EH وأين لا. نِسب الفوز محسوبة على المنافسات ذات النتيجة المُسجّلة — عيّنة صغيرة لكنها دالّة ('+k.awarded+' مُرساة).')}</div>
 <div class="grid g2">
  <div class="card"><h3>${t('Head-to-head outcome','النتيجة المباشرة')}</h3><div class="note">${t('Among decided tenders, EH vs the field.','بين المنافسات المحسومة، EH مقابل المنافسين.')}</div>
   <div style="display:flex;align-items:center;gap:18px;justify-content:center;flex-wrap:wrap">${donut(segs,{center:pct(k.win_rate),csub:t('WIN RATE','نسبة الفوز')})}<div>${legend(segs)}</div></div>
   <div style="margin-top:12px;font-size:12px;color:#6B7C86;text-align:center">${t('EH won ','فاز EH بـ ')}<b style="color:#2E7D46">${wl.awarded_eh}</b>${t(' · lost ',' · وخسر ')}<b style="color:#C0504D">${wl.awarded_other}</b>${t(' of '+k.awarded+' decided tenders.',' من '+k.awarded+' منافسة محسومة.')}</div></div>
  <div class="card"><h3>${t('Win rate vs competition intensity','نسبة الفوز مقابل حدّة المنافسة')}</h3><div class="note">${t('Does EH win more when fewer rivals bid? Each bar = win rate at that bidder count.','هل يفوز EH أكثر عند تقدّم منافسين أقل؟ كل عمود = نسبة الفوز عند ذلك العدد من المتقدمين.')}</div>
   ${bdr.length?hbar(bdr,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+')',color:d=>wrCol(d.v),rh:42}):'<div class="note">'+t('Not enough decided tenders with bidder counts.','لا توجد منافسات محسومة كافية بأعداد المتقدمين.')+'</div>'}</div>
 </div>
 <div class="card"><h3>${t('Win rate by service line','نسبة الفوز حسب مجال الخدمة')}</h3><div class="note">${t('Which capabilities convert best.','أي القدرات تحقّق أعلى معدّل فوز.')}</div>
   ${hbar(svc,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+t(' decided',' محسومة')+')',color:d=>wrCol(d.v),maxlab:38,rh:54})}</div>
 <div class="card"><h3>${t('Win rate by platform','نسبة الفوز حسب المنصة')}</h3><div class="note">${t('Conversion by procurement channel.','معدّل الفوز حسب قناة الشراء.')}</div>
   ${plat.length?hbar(plat,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+t(' decided',' محسومة')+')',color:d=>wrCol(d.v),maxlab:30,rh:54}):'<div class="note">'+t('Insufficient data.','بيانات غير كافية.')+'</div>'}</div>`;
}

// ===================== PRICING =====================
let pxExpand={};
function togglePx(id){pxExpand[id]=!pxExpand[id];renderPricing();}
function pxAll(v){BA.pricing.rows.forEach((r,i)=>pxExpand[i]=v);renderPricing();}
function renderPricing(){
 const p=BA.pricing, s=p.summary, rows=p.rows;
 const cards=rows.map((r,i)=>{
   const open=!!pxExpand[i];
   const maxp=Math.max(...r.bidders.filter(b=>b.price).map(b=>b.price),1);
   const gapcol=r.gap>50?'#C0504D':r.gap>5?'#E8862E':'#2E7D46';
   const oc=r.status=='Cancelled'?'<span class="tag" style="background:#8A99A3">'+t('CANCELLED','ملغاة')+'</span>':(r.won==null?'<span style="color:#9AA8B0;font-weight:700">'+t('PENDING','قيد الدراسة')+'</span>':(r.won?'<span class="tag" style="background:#2E7D46">'+t('EH WON','فاز EH')+'</span>':'<span class="tag" style="background:#C0504D">'+t('LOST','خسارة')+'</span>'));
   // full bidder bars (shown when open)
   const bars=r.bidders.map(b=>{
     if(b.dq){return `<div style="display:flex;align-items:center;gap:8px;margin:3px 0;opacity:.6"><div style="width:230px;font-size:10.5px;color:#8A99A3;text-align:right" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(45deg,#EEE,#EEE 4px,#E0E0E0 4px,#E0E0E0 8px);border-radius:3px;max-width:60px"></div><div style="font-size:10px;color:#B23A3A;font-weight:700">${t('DQ — non-compliant','مستبعد — غير مطابق')}</div></div>`;}
     if(b.undisclosed){return `<div style="display:flex;align-items:center;gap:8px;margin:3px 0;opacity:.85"><div style="width:230px;font-size:10.5px;color:${b.eh?'#1A5FAB':'#5A6A72'};font-weight:${b.eh?'700':'500'};text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(90deg,#EFF2F4,#EFF2F4 6px,#E4E8EB 6px,#E4E8EB 12px);border-radius:3px;max-width:80px"></div><div style="font-size:10px;color:#9AA8B0;font-style:italic;white-space:nowrap">${t('undisclosed value','قيمة غير معلنة')}${b.won?' <span style="color:#2E7D46;font-weight:700;font-style:normal">★ '+t('won','فائز')+'</span>':''}</div></div>`;}
     const w=Math.max(b.price/maxp*100,2);
     const col=b.eh?'#1A5FAB':(b.won?'#2E7D46':'#9AABB5');
     const isWin=b.won;
     return `<div style="display:flex;align-items:center;gap:8px;margin:3px 0">
       <div style="width:230px;font-size:10.5px;color:${b.eh?'#1A5FAB':'#3A4A52'};font-weight:${b.eh?'700':'500'};text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" dir="auto">${b.lowest?'\u25bc ':''}${esc(b.name)}</div>
       <div style="flex:1;max-width:${w}%;height:15px;background:${col};border-radius:3px;min-width:3px"></div>
       <div style="font-size:10.5px;color:#1C2B33;font-weight:${b.eh?'700':'500'};white-space:nowrap">${fmtSAR(b.price)}${isWin?' <span style="color:#2E7D46;font-weight:700">★ '+t('won','فائز')+'</span>':''}</div></div>`;
   }).join('');
   return `<div class="card" style="margin-bottom:10px;padding:0;overflow:hidden">
     <div onclick="togglePx(${i})" style="cursor:pointer;padding:12px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:${open?'#F7FAFC':'#fff'}">
       <div style="min-width:70px"><b style="font-size:13px">#${r.sn}/${String(r.year).slice(2)}</b><div style="font-size:9px;color:#9AA8B0">${r.n} ${t('bidders','متقدمين')}${r.undisc_count?' · '+r.undisc_count+' '+t('undisclosed','غير معلنة'):''}${r.dq_count?' · '+r.dq_count+' '+t('DQ','مستبعد'):''}</div></div>
       <div style="flex:1;min-width:200px"><div dir="auto" style="font-size:11.5px;color:#1C2B33;font-weight:600;line-height:1.3">${esc(r.title)||'<span style=\'color:#aaa\'>'+t('(untitled tender)','(منافسة بلا عنوان)')+'</span>'}</div><div dir="auto" style="font-size:10px;color:#9AA8B0;margin-top:1px">${esc(r.client)}</div></div>
       <div style="text-align:right"><div style="font-size:9px;color:#9AA8B0;text-transform:uppercase;letter-spacing:.3px">${t('EH bid','عرض EH')}</div><div style="font-weight:700;font-size:12.5px;color:#1A5FAB">${r.eh!=null?fmtSAR(r.eh):'<span style="color:#B0B8BD;font-weight:600;font-size:10px">'+t('no EH bid','لا عرض من EH')+'</span>'}</div></div>
       <div style="text-align:center"><div style="font-size:9px;color:#9AA8B0;text-transform:uppercase">${t('Rank','الترتيب')}</div><div style="font-weight:700;font-size:12.5px">${r.rank!=null?r.rank+'/'+r.n_priced:'\u2014'}</div></div>
       <div style="text-align:center"><div style="font-size:9px;color:#9AA8B0;text-transform:uppercase">${t('vs Low','مقابل الأدنى')}</div><div style="font-weight:700;font-size:12.5px;color:${gapcol}">${r.gap!=null?(r.gap>0?'+'+r.gap+'%':r.gap+'%'):'\u2014'}</div></div>
       <div style="min-width:78px;text-align:center">${oc}</div>
       <div style="font-size:13px;color:#9AA8B0;transform:rotate(${open?'90':'0'}deg);transition:.15s">\u25b8</div>
     </div>
     ${open?`<div style="padding:10px 16px 14px;border-top:1px solid #EEF2F0;background:#FBFCFD">
       <div style="font-size:10.5px;color:#8A99A3;margin-bottom:8px">${r.undisc_count?'<span style="color:#B07A2E;font-weight:600">'+t(r.undisc_count+' of '+r.n+' bidders had no disclosed value (shown as undisclosed).',r.undisc_count+' من '+r.n+' متقدمين بلا قيمة معلنة (تظهر كغير معلنة).')+'</span><br>':''}${t(r.n_priced+' priced bid'+(r.n_priced==1?'':'s')+' shown, lowest first — ',r.n_priced+' عرض مُسعّر مرتّبة من الأدنى — ')}<span style="color:#1A5FAB;font-weight:700">${t('EH in blue','EH بالأزرق')}</span>${r.n_priced>1?', <span style="color:#2E7D46;font-weight:700">▼ '+t('lowest','الأدنى')+'</span>':''}${r.win_price?', ★ = '+t('winning bid','العرض الفائز'):''}.</div>
       ${bars}</div>`:''}</div>`;
 }).join('');
 $('s-pricing').innerHTML=
 `<div class="sech">${t('Pricing intelligence','تحليل الأسعار')}</div><div class="secsub">${t('Every tender with a recorded bidder list — '+s.tenders+' in all. '+s.full+' show EH\'s price against the full field (the ranking stats below are drawn from these); the rest list the bidders with prices where disclosed and “undisclosed value” otherwise. '+s.total_bidders+' disclosed bids across '+s.total_names+' bidder entries. Click any tender for the full list.','كل منافسة لها قائمة متقدمين مُسجّلة — '+s.tenders+' إجمالاً. '+s.full+' منها تُظهر سعر EH مقابل كامل المنافسين (وتُشتق إحصاءات الترتيب أدناه منها)؛ والباقي يسرد المتقدمين بالأسعار حيث أُعلنت وبـ«قيمة غير معلنة» فيما عدا ذلك. '+s.total_bidders+' عرضاً مُعلناً عبر '+s.total_names+' مُدخل متقدم. انقر أي منافسة لعرض القائمة الكاملة.')}</div>
 <div class="kstrip">
   ${kc(s.cheapest_pct+'%',t('Tenders EH was cheapest','منافسات كان EH الأرخص فيها'),s.cheapest+t(' of ',' من ')+s.full+t(' full',' كاملة'),s.cheapest_pct>=40?'g':'r')}
   ${kc(s.avg_percentile+t('th',''),t('Avg price percentile','متوسط المئوي السعري'),t('1st=cheapest','1 = الأرخص'),s.avg_percentile<=40?'g':'r')}
   ${kc((s.median_gap>0?'+':'')+s.median_gap+'%',t('Median gap to lowest','وسيط الفارق عن الأدنى'),t('typical EH vs cheapest','EH نموذجياً مقابل الأرخص'),s.median_gap>20?'r':'g')}
   ${kc(s.tenders,t('Tenders with bidders','منافسات بها متقدمون'),s.full+t(' with full pricing',' بتسعير كامل'))}
 </div>
 <div style="display:flex;gap:8px;margin-bottom:12px"><button onclick="pxAll(true)" style="padding:6px 13px;border:1px solid #1A5FAB;background:#1A5FAB;color:#fff;border-radius:7px;font-size:11.5px;font-weight:600;cursor:pointer">${t('Expand all','توسيع الكل')}</button><button onclick="pxAll(false)" style="padding:6px 13px;border:1px solid #D5DEE2;background:#fff;color:#6B7C86;border-radius:7px;font-size:11.5px;font-weight:600;cursor:pointer">${t('Collapse all','طيّ الكل')}</button></div>
 ${cards}
 <div style="margin-top:14px;font-size:12px;color:#6B7C86;background:#FCF5F4;border:1px solid #F0D9D6;border-radius:8px;padding:11px 13px">
 <b>${t('Read-out:','الخلاصة:')}</b> ${t('Across '+s.full+' tenders with full bidder pricing, EH was the outright lowest bidder '+s.cheapest_pct+'% of the time and sat at the '+s.avg_percentile+'th price percentile on average. The median gap to the cheapest bid is '+s.median_gap+'% — on these tenders EH frequently sits well above the lowest bid, sometimes several times higher, so pricing looks like a genuine competitive exposure worth investigating. Price is clearly one lever, but ','عبر '+s.full+' منافسة بتسعير كامل، كان EH صاحب العرض الأدنى صراحةً في '+s.cheapest_pct+'% من الحالات، وجاء عند المئوي السعري '+s.avg_percentile+' في المتوسط. وسيط الفارق عن أرخص عرض هو '+s.median_gap+'% — وكثيراً ما يكون عرض EH في هذه المنافسات أعلى بكثير من الأدنى، وأحياناً أضعافاً، فيبدو التسعير انكشافاً تنافسياً حقيقياً يستحق البحث. السعر رافعة واحدة بوضوح، لكن ')}<b>${t('price is not the whole story','السعر ليس كامل القصة')}</b>${t(': Saudi tenders are scored on technical merit, compliance, delivery capability and incumbency too, and the tracker does not capture those factors or the stated reason for each loss — so we can see where EH priced high, but cannot prove price caused a loss. Capturing the technical score and loss reason per tender is what would close that gap.','؛ فالمنافسات السعودية تُقيَّم كذلك على الجدارة الفنية والامتثال وقدرة التنفيذ وأسبقية التعاقد، والجدول لا يرصد هذه العوامل ولا السبب المُعلن لكل خسارة — فيمكننا رؤية أين سعّر EH مرتفعاً، لكن يتعذّر إثبات أن السعر سبّب الخسارة. ورصد الدرجة الفنية وسبب الخسارة لكل منافسة هو ما يسدّ تلك الفجوة.')}</div>`;
}

// ===================== COMPETITORS =====================
let showOneOff=false;
function toggleOneOff(){showOneOff=!showOneOff;renderCompetitors();}
function renderCompetitors(){
 const all=BA.competitors;
 const recurring=all.filter(c=>c.encounters>=2);
 const oneoff=all.filter(c=>c.encounters<2);
 const shown=showOneOff?all:recurring;
 const freq=recurring.slice().sort((a,b)=>b.encounters-a.encounters).slice(0,14);
 $('s-competitors').innerHTML=
 `<div class="sech">${t('Competitive landscape','المشهد التنافسي')}</div><div class="secsub">${t('Every company that has bid against EH, rebuilt directly from the detailed bidder sheets — '+all.length+' distinct competitors across '+BA.pricing.summary.tenders+'+ shared tenders.','كل شركة تقدّمت بعرض ضد EH، مُعاد بناؤها مباشرة من كشوف المتقدمين التفصيلية — '+all.length+' منافساً متمايزاً عبر '+BA.pricing.summary.tenders+'+ منافسة مشتركة.')}</div>
 <div class="card"><h3>${t('Most frequent competitors (shared tenders with EH)','المنافسون الأكثر تكراراً (منافسات مشتركة مع EH)')}</h3><div class="note">${t('How many tenders each competitor has bid in alongside EH. Red bars are competitors that have actually beaten EH to an award.','عدد المنافسات التي تقدّم فيها كل منافس إلى جانب EH. الأعمدة الحمراء منافسون تغلّبوا فعلاً على EH في الترسية.')}</div>
   ${hbar(freq,{val:d=>d.encounters,lab:d=>d.name,fmt:v=>v,sub:d=>d.wins?'· '+d.wins+t(' win vs EH',' فوز على EH'):'',color:d=>d.wins?C.red:C.blue,maxlab:40,rh:24})}</div>
 <div class="card"><h3>${t('Competitor scorecard — head-to-head vs EH','بطاقة أداء المنافسين — مواجهة مباشرة مع EH')}</h3>
   <div class="note">${t('Encounters = shared tenders. Undercut = of the tenders where both were priced, the share where the competitor bid below EH. Won = tenders this competitor actually won.','المواجهات = المنافسات المشتركة. الخفض = من المنافسات التي سُعّر فيها الطرفان، نسبة تقديم المنافس بأقل من EH. الفوز = المنافسات التي فاز بها هذا المنافس فعلاً.')}</div>
   <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;padding:10px 13px;background:#F4F8F5;border:1px solid #E3EAE5;border-radius:9px">
     <label style="display:flex;align-items:center;gap:7px;cursor:pointer;font-size:12.5px;font-weight:600;color:#3A4A52"><input type="checkbox" ${showOneOff?'checked':''} onchange="toggleOneOff()" style="width:15px;height:15px;cursor:pointer"> ${t('Show one-off bidders','عرض المتقدمين لمرة واحدة')}</label>
     <span style="font-size:11.5px;color:#8A99A3;flex:1;min-width:240px">${showOneOff?`${t('Showing all ','عرض جميع ')}<b>${all.length}</b>${t(' competitors.',' منافساً.')}`:`${t('Showing ','عرض ')}<b>${recurring.length}</b>${t(' recurring competitors. ',' منافساً متكرراً. ')}<b>${oneoff.length}</b>${t(' one-off bidders are hidden — a company that bid against EH only once is noise, not a pattern, and is not a recurring competitive threat. Tick the box to include them.',' متقدماً لمرة واحدة مخفيون — الشركة التي تقدّمت ضد EH مرة واحدة فقط ضجيج لا نمط، وليست تهديداً تنافسياً متكرراً. فعّل الخانة لتضمينهم.')}`}</span>
   </div>
 <table class="t"><thead><tr><th>#</th><th>${t('Competitor','المنافس')}</th><th>${t('Encounters','المواجهات')}</th><th>${t('Won vs field','فاز على الآخرين')}</th><th>${t('Times DQ\'d','مرات الاستبعاد')}</th><th>${t('Undercut EH','خفض عن EH')}</th><th>${t('Avg bid','متوسط العرض')}</th></tr></thead><tbody>
 ${shown.map((c,i)=>`<tr><td style="color:#9AA8B0">${i+1}</td><td><b dir="auto">${esc(c.name)}</b></td><td>${c.encounters}</td><td>${c.wins?`<b style="color:#C0504D">${c.wins}</b>`:'0'}</td><td>${c.dq||0}</td><td style="color:${c.undercut_pct>=67?'#C0504D':c.undercut_pct>=34?'#E8862E':'#1C2B33'};font-weight:700">${c.undercut_pct==null?'\u2014':c.undercut_pct+'%'}</td><td>${c.avg_price?fmtSAR(c.avg_price):'\u2014'}</td></tr>`).join('')}
 </tbody></table>
 <div style="font-size:11px;color:#9AA8B0;margin-top:10px">${t('Names are taken verbatim from the bidder sheets (mostly Arabic) and grouped by normalized spelling; very close name variants of the same firm may still appear as separate rows.','الأسماء مأخوذة حرفياً من كشوف المتقدمين (عربية غالباً) ومجمّعة حسب التهجئة المُوحّدة؛ وقد تظهر تنويعات قريبة جداً لاسم الشركة نفسها كصفوف منفصلة.')}</div></div>`;
}

// ===================== CLIENTS =====================
function rClients(){
 const cl=BA.clients;
 const byVal=cl.filter(c=>c.value>0).slice(0,12);
 const totVal=cl.reduce((a,c)=>a+c.value,0);
 const top3=cl.slice(0,3).reduce((a,c)=>a+c.value,0);
 const lapsed=cl.filter(c=>c.lapsed).length, fresh=cl.filter(c=>c.isnew).length;
 $('s-clients').innerHTML=
 `<div class="sech">${t('Client intelligence','تحليل العملاء')}</div><div class="secsub">${t('Who EH bids to, the value each represents, and how the book is shifting between 2025 and 2026.','لمن يتقدّم EH، وقيمة كل عميل، وكيف تتغيّر المحفظة بين 2025 و2026.')}</div>
 <div class="kstrip">
   ${kc(k.clients,t('Distinct clients','عملاء متمايزون'),t('sending tenders','يطرحون منافسات'))}
   ${kc(Math.round(100*top3/totVal)+'%',t('Top-3 concentration','تركّز أعلى 3'),t('of tracked value','من القيمة المتتبَّعة'),top3/totVal>0.5?'r':'')}
   ${kc(lapsed,t('Lapsed clients','عملاء متوقّفون'),t('2025 only, no 2026','2025 فقط، بلا 2026'),'r')}
   ${kc(fresh,t('New in 2026','جدد في 2026'),t('first appeared','ظهروا حديثاً'),'g')}
 </div>
 <div class="card"><h3>${t('Top clients by tracked value','أبرز العملاء حسب القيمة المتتبَّعة')}</h3><div class="note">${t('Sum of EH offer values per client (partial where the tracker is not filled). SEC dominates the book.','مجموع قيم عروض EH لكل عميل (جزئي حيث لم يُملأ الجدول). SEC يهيمن على المحفظة.')}</div>
   ${hbar(byVal,{val:d=>d.value,lab:d=>d.name,fmt:v=>'SAR '+fmtM(v),color:d=>C.pal[byVal.indexOf(d)%C.pal.length],maxlab:38,rh:24})}</div>
 <div class="card"><h3>${t('Client value tiering — 2025 vs 2026','تدرّج قيمة العملاء — 2025 مقابل 2026')}</h3><div class="note">${t('Per-client split by year, with status. \"Lapsed\" = active in 2025 but silent in 2026 (re-engagement targets).','تقسيم كل عميل حسب السنة مع الحالة. «متوقّف» = نشط في 2025 وصامت في 2026 (أهداف إعادة تفعيل).')}</div>
 <table class="t"><thead><tr><th>${t('Client','العميل')}</th><th>${t('\'25 tenders','منافسات 25')}</th><th>${t('\'25 value','قيمة 25')}</th><th>${t('\'26 tenders','منافسات 26')}</th><th>${t('\'26 value','قيمة 26')}</th><th>${t('EH win','فوز EH')}</th><th>${t('Status','الحالة')}</th></tr></thead><tbody>
 ${cl.slice(0,20).map(c=>`<tr><td><b dir="auto">${esc(c.name)}</b></td><td>${c.bids25||'—'}</td><td>${c.value25?fmtSAR(c.value25):'—'}</td><td>${c.bids26||'—'}</td><td>${c.value26?fmtSAR(c.value26):'—'}</td><td style="color:${wrCol(c.win_rate)};font-weight:700">${c.win_rate==null?'—':c.win_rate+'%'}</td><td>${c.lapsed?'<span style="color:#C0504D">'+t('Lapsed','متوقّف')+'</span>':(c.isnew?'<span style="color:#2E7D46">'+t('New 2026','جديد 2026')+'</span>':t('Active','نشط'))}</td></tr>`).join('')}
 </tbody></table></div>`;
}

// ===================== SERVICE & PLATFORM =====================
function rService(){
 const sm=BA.service_mix, pm=BA.platform_mix, du=BA.duration, ds=BA.dur_stats;
 const smSeg=sm.map((x,i)=>({l:dv(DSVC,x.name),v:x.count,c:C.pal[i%C.pal.length]}));
 $('s-service').innerHTML=
 `<div class="sech">${t('Service mix & channels','مزيج الخدمات والقنوات')}</div><div class="secsub">${t('What kind of work EH bids for, through which platforms, and at what project scale.','نوع الأعمال التي يتقدّم لها EH، وعبر أي منصات، وبأي حجم مشروع.')}</div>
 <div class="card"><h3>${t('Tenders by service line','المنافسات حسب مجال الخدمة')}</h3><div class="note">${t('From the assigned technical department (where recorded).','من الإدارة الفنية المُسندة (حيث سُجّلت).')}</div>
   <div style="display:flex;align-items:center;gap:16px;justify-content:center;flex-wrap:wrap">${donut(smSeg,{center:sm.reduce((a,x)=>a+x.count,0),csub:t('TENDERS','منافسات')})}<div>${legend(smSeg)}</div></div>
   <table class="t" style="margin-top:12px"><thead><tr><th>${t('Service line','مجال الخدمة')}</th><th>${t('Tenders','المنافسات')}</th><th>${t('Value','القيمة')}</th><th>${t('Win rate','نسبة الفوز')}</th></tr></thead><tbody>
   ${sm.map(x=>`<tr><td><b>${esc(dv(DSVC,x.name))}</b></td><td>${x.count}</td><td>${fmtSAR(x.value)}</td><td style="color:${wrCol(x.win_rate)};font-weight:700">${x.win_rate==null?'—':x.win_rate+'%'}</td></tr>`).join('')}</tbody></table></div>
 <div class="card"><h3>${t('Tenders by platform','المنافسات حسب المنصة')}</h3><div class="note">${t('Procurement channels — Etimad (government) dominates.','قنوات الشراء — تهيمن اعتماد (الحكومية).')}</div>
   ${hbar(pm,{val:d=>d.count,lab:d=>dv(DPLAT,d.name),fmt:v=>v+t(' tenders',' منافسة'),sub:d=>d.win_rate!=null?'· '+t('win ','فوز ')+d.win_rate+'%':'',color:d=>C.pal[pm.indexOf(d)%C.pal.length],maxlab:30,rh:56})}</div>
 <div class="card"><h3>${t('Project duration distribution','توزيع مدة المشاريع')}</h3><div class="note">${t('Contract length of tenders (months), where recorded. Median '+ds.median+' months · mean '+ds.mean+' · longest '+ds.max+'.','مدة عقود المنافسات (بالأشهر) حيث سُجّلت. الوسيط '+ds.median+' شهراً · المتوسط '+ds.mean+' · الأطول '+ds.max+'.')}</div>
   ${barChart(du,{val:d=>d.count,lab:d=>dv(DDUR,d.band),fmt:v=>v,color:C.purple,h:200})}</div>`;
}

// ===================== TURNAROUND / DECISION DURATION =====================
function rFunnel(){
 const tu=BA.turnaround, f=BA.funnel, com=BA.committee, k2=BA.kpi;
 // categorize the decision/review window into clear named buckets
 const LBL={'≤7 days':t('Under 1 week','أقل من أسبوع'),'8–14 days':t('1 – 2 weeks','1 – 2 أسبوع'),'15–30 days':t('2 – 4 weeks','2 – 4 أسابيع'),'31–45 days':t('4 – 6 weeks','4 – 6 أسابيع'),'46+ days':t('Over 6 weeks','أكثر من 6 أسابيع')};
 const cats=tu.bands.map((b,i)=>({l:LBL[b.band]||b.band, v:b.count, i}));
 const comSeg=[{l:t('Accepted (decided to bid)','مقبولة (قرار التقديم)'),v:com.accept,c:C.green},{l:t('Rejected (decided to pass)','مرفوضة (قرار الاعتذار)'),v:com.reject,c:C.red}];
 const guarFmt='SAR '+fmtM(k2.total_guarantee);
 $('s-funnel').innerHTML=
 `<div class="sech">${t('Decision & review duration','مدة القرار والمراجعة')}</div><div class="secsub">${t('How long the full EH committee review runs on each tender — the elapsed time from the tender being launched to the submission deadline, the window in which BD, the CEO, technical, PM and the bid committee must all weigh in and decide.','كم تستغرق مراجعة لجنة EH الكاملة لكل منافسة — الزمن المنقضي من طرح المنافسة حتى الموعد النهائي للتقديم، وهي المهلة التي يجب فيها أن يُدلي تطوير الأعمال والرئيس التنفيذي والفني ومدير المشروع ولجنة العطاءات برأيهم ويقرّروا.')}</div>
 <div class="kstrip">
   ${kc(tu.mean+t(' days',' يوم'),t('Average review duration','متوسط مدة المراجعة'),t('launch → deadline','الطرح → الموعد النهائي'))}
   ${kc(tu.median+t(' days',' يوم'),t('Median review duration','وسيط مدة المراجعة'),t('typical tender','منافسة نموذجية'))}
   ${kc(tu.minv+'–'+tu.maxv,t('Range (days)','المدى (أيام)'),t('fastest → slowest','الأسرع → الأبطأ'))}
   ${kc(tu.n,t('Tenders measured','منافسات مقيسة'),t('with both dates','لها التاريخان'))}
 </div>
 <div class="card"><h3>${t('How long does the EH committee take to decide?','كم تستغرق لجنة EH لاتخاذ القرار؟')}</h3><div class="note">${t('Each tender placed into a duration band by the length of its review window. This is the elapsed calendar time available for the EH committee to review and reach a decision — it is ','تُصنَّف كل منافسة في شريحة مدة حسب طول نافذة مراجعتها. هذا هو الزمن التقويمي المتاح للجنة EH للمراجعة والوصول إلى قرار — وهو ')}<b>${t('not','ليس')}</b>${t(' win rate.',' نسبة الفوز.')}</div>
   ${hbar(cats,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+t(' tender'+(v==1?'':'s'),' منافسة'),color:d=>[C.red,C.orange,C.green,C.teal,C.blue][d.i]||C.blue,rh:34,maxlab:18})}
   <div style="margin-top:12px;font-size:12px;color:#6B7C86;background:#F2F7FC;border:1px solid #D6E4F2;border-radius:8px;padding:11px 13px">
   <b>${t('Read-out:','الخلاصة:')}</b> ${t('The EH committee review runs ','تستغرق مراجعة لجنة EH ')}<b>${t(tu.mean+' days on average',tu.mean+' يوماً في المتوسط')}</b>${t(' (median '+tu.median+'). But the spread is the real story: ',' (الوسيط '+tu.median+'). لكن التشتّت هو القصة الحقيقية: ')}<b>${t(tu.tight14+' of '+tu.n,tu.tight14+' من '+tu.n)}</b>${t(' tenders compress the entire BD → CEO → technical → PM → committee decision into two weeks or less, and '+tu.tight7+' into a single week — little time for a considered technical and pricing response. ',' منافسة تضغط كامل قرار تطوير الأعمال → الرئيس التنفيذي → الفني → مدير المشروع → اللجنة في أسبوعين أو أقل، و'+tu.tight7+' في أسبوع واحد — وقت ضئيل لاستجابة فنية وسعرية متأنّية. ')}<i>${t('Caveat: the workbook records each department sign-off as accept/reject but not the date it happened, so this is the overall decision window, not the gap between individual EH departments. Logging a date at each sign-off would let us pinpoint exactly where tenders stall.','تنبيه: يسجّل الملف اعتماد كل إدارة كقبول/رفض دون تاريخ حدوثه، فهذه نافذة القرار الإجمالية لا الفجوة بين إدارات EH منفردة. تسجيل تاريخ عند كل اعتماد سيتيح تحديد أين تتعثّر المنافسات بدقّة.')}</i></div></div>
 <div class="grid g2">
  <div class="card"><h3>${t('The bid / no-bid decision','قرار التقديم / عدم التقديم')}</h3><div class="note">${t('Once reviewed, how often the committee decides to pursue a tender versus pass on it.','بعد المراجعة، كم مرة تقرّر اللجنة متابعة منافسة مقابل الاعتذار عنها.')}</div>
   <div style="display:flex;align-items:center;gap:16px;justify-content:center;flex-wrap:wrap">${donut(comSeg,{center:Math.round(100*com.accept/(com.accept+com.reject))+'%',csub:t('PURSUED','متابعة')})}<div>${legend(comSeg)}</div></div></div>
  <div class="card"><h3>${t('Bank-guarantee exposure','انكشاف الضمان البنكي')}</h3><div class="note">${t('What \"guarantee exposure\" means.','ماذا يعني «انكشاف الضمان».')}</div>
   <div style="text-align:center;padding:6px 0 10px"><div style="font-size:34px;font-weight:800;color:#7B6BA8;line-height:1">${guarFmt}</div><div style="font-size:11px;color:#9AA8B0;text-transform:uppercase;letter-spacing:.5px;margin-top:4px">${t('total bid-bond value issued','إجمالي قيمة سندات العطاء المُصدرة')}</div></div>
   <div style="font-size:12px;color:#5A4A62;line-height:1.6;background:#F6F3FB;border:1px solid #E0D8F0;border-radius:8px;padding:11px 13px">${t('A ','')}<b>${t('bank guarantee','الضمان البنكي')}</b>${t(' (bid bond) is security a bidder must post to enter many government tenders. This figure is the cumulative value of the guarantees EH has issued across the tracked tenders — i.e. capital tied up as bid security. It is returned when EH is not awarded, or released on contract signing, so it represents committed-but-recoverable exposure, not a sunk cost. Only ',' (سند العطاء) تأمين يجب على المتقدّم تقديمه لدخول كثير من المنافسات الحكومية. هذا الرقم هو القيمة التراكمية للضمانات التي أصدرها EH عبر المنافسات المتتبَّعة — أي رأس مال مُجمّد كتأمين عطاء. يُعاد عند عدم ترسية EH، أو يُفرَج عنه عند توقيع العقد، فيمثّل انكشافاً ملتزَماً لكنه قابل للاسترداد لا تكلفة غارقة. فقط ')}${Math.round(100*22/k2.total)>0?t('a minority of','أقلية من'):t('some','بعض')}${t(' tenders in the tracker record a guarantee value, so the true figure is higher.',' منافسات في الجدول تسجّل قيمة ضمان، فالرقم الحقيقي أعلى.')}</div></div>
 </div>
 <div class="card"><h3>${t('Why bids were declined — '+BA.refused.length+' recorded no-bid decisions','لماذا اعتُذر عن المنافسات — '+BA.refused.length+' قرار عدم تقديم مُسجّل')}</h3>
   <div class="note">${t('When the committee decides to pass on a tender, the reason is logged in the comments column. These are the declined bids and exactly why. Capturing this is how EH learns where to stop spending effort — and the pattern is clear: most declines are work that falls outside EH scope, needs a licence EH does not hold, or is locked to a specific brand.','عندما تقرّر اللجنة الاعتذار عن منافسة، يُسجَّل السبب في عمود الملاحظات. هذه هي العروض المرفوضة وأسبابها بدقّة. رصد ذلك هو كيف يتعلّم EH أين يتوقّف عن بذل الجهد — والنمط واضح: معظم الاعتذارات أعمال خارج نطاق EH، أو تتطلّب ترخيصاً لا يملكه EH، أو محصورة بعلامة تجارية محددة.')}</div>
   <div style="display:flex;flex-wrap:wrap;gap:9px;margin-bottom:15px">
   ${BA.refusal_cats.map(rc=>{const cc=RCAT[rc.cat]||'#9AABB5';return `<div style="display:flex;align-items:center;gap:8px;background:${cc}14;border:1px solid ${cc}55;border-radius:9px;padding:8px 13px"><span style="font-size:17px;font-weight:800;color:${cc}">${rc.n}</span><span style="font-size:11.5px;color:#3A4A52;font-weight:600">${dv(DCAT,rc.cat)}</span></div>`;}).join('')}
   </div>
   <table class="t"><thead><tr><th>${t('Tender','المنافسة')}</th><th>${t('Project','المشروع')}</th><th>${t('Client','العميل')}</th><th>${t('Reason category','فئة السبب')}</th><th>${t('Recorded reason','السبب المُسجّل')}</th></tr></thead><tbody>
   ${BA.refused.map(r=>{const cc=RCAT[r.cat]||'#9AABB5';return `<tr><td><b>#${r.sn}/${String(r.year).slice(2)}</b></td><td dir="auto" style="max-width:180px;font-size:11px;line-height:1.35">${esc(r.title)||'\u2014'}</td><td dir="auto" style="max-width:120px;font-size:10.5px;color:#7B8A92">${esc(r.client)||'\u2014'}</td><td><span class="tag" style="background:${cc};white-space:nowrap">${dv(DCAT,r.cat)}</span></td><td dir="auto" style="max-width:330px;font-size:11px;color:#5A6A72;line-height:1.4">${esc(r.reason)}</td></tr>`;}).join('')}
   </tbody></table></div>`;
}

// ===================== ALL TENDERS (list view) =====================
const TF={year:'all',outcome:'all',platform:'all',svc:'all',q:''};
function setTF(kk,v){TF[kk]=v;renderTenders();}
function platN(p){p=(p||'').toLowerCase();if(p.includes('etimad'))return 'Etimad';if(p.includes('ariba'))return 'SAP Ariba';if(p.includes('sec'))return 'SEC-SAP';if(p.includes('mail'))return 'Email';return p?'Other':'\u2014';}
function uniqVals(fn){return [...new Set(BA.bidlist.map(fn).filter(x=>x&&x!=='\u2014'))].sort();}
function renderTenders(){
 const OC={'Won':'#2E7D46','Lost':'#C0504D','Not awarded':'#E8862E','Cancelled':'#9AA8B0','Pending':'#3E86C8'};
 const list=BA.bidlist.filter(b=>
   (TF.year=='all'||b.year==TF.year)&&
   (TF.outcome=='all'||b.outcome==TF.outcome)&&
   (TF.platform=='all'||platN(b.platform)==TF.platform)&&
   (TF.svc=='all'||b.svc==TF.svc)&&
   (!TF.q||((b.title+' '+b.client+' #'+b.sn).toLowerCase().includes(TF.q.toLowerCase()))));
 const ss='padding:7px 10px;border:1px solid #CBD6DC;border-radius:7px;font-size:12px;color:#3A4A52;background:#fff;cursor:pointer';
 const sel=(kk,opts,lab,disp)=>`<div style="display:flex;flex-direction:column;gap:3px"><label style="font-size:10px;color:#8A99A3;text-transform:uppercase;letter-spacing:.4px;font-weight:600">${lab}</label><select onchange="setTF('${kk}',this.value)" style="${ss}">${['all',...opts].map(o=>`<option value="${o}" ${TF[kk]==o?'selected':''}>${o=='all'?t('All','الكل'):(disp?disp(o):o)}</option>`).join('')}</select></div>`;
 const outcomes=['Won','Lost','Not awarded','Cancelled','Pending'].filter(o=>BA.bidlist.some(b=>b.outcome==o));
 const ctrls=`<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;margin-bottom:14px;background:#fff;border:1px solid #E3EAE5;border-radius:11px;padding:13px 15px">
   ${sel('year',['2025','2026'],t('Year','السنة'))}
   ${sel('outcome',outcomes,t('Outcome','النتيجة'),o=>dv(DOUT,o))}
   ${sel('platform',uniqVals(b=>platN(b.platform)),t('Platform','المنصة'),o=>dv(DPLAT,o))}
   ${sel('svc',uniqVals(b=>b.svc),t('Service line','مجال الخدمة'),o=>dv(DSVC,o))}
   <div style="display:flex;flex-direction:column;gap:3px;flex:1;min-width:180px"><label style="font-size:10px;color:#8A99A3;text-transform:uppercase;letter-spacing:.4px;font-weight:600">${t('Search title / client / ref','البحث في العنوان / العميل / المرجع')}</label>
     <input oninput="setTF('q',this.value)" value="${esc(TF.q)}" placeholder="${t('Type to filter…','للتصفية اكتب…')}" style="${ss};width:100%;cursor:text"></div>
   <button onclick="TF.year='all';TF.outcome='all';TF.platform='all';TF.svc='all';TF.q='';renderTenders()" style="padding:8px 14px;border:1px solid #D5DEE2;background:#F4F8F5;color:#6B7C86;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer">${t('Reset','إعادة تعيين')}</button></div>`;
 const rows=list.map(b=>`<tr>
   <td><b>#${b.sn}</b><div style="font-size:9.5px;color:#9AA8B0">${b.year}</div></td>
   <td style="font-size:10.5px;color:#7B8A92;white-space:nowrap">${b.date||'\u2014'}</td>
   <td style="max-width:280px"><div dir="auto" style="font-size:11.5px;line-height:1.35">${esc(b.title)||'<span style="color:#bbb">\u2014</span>'}</div></td>
   <td style="max-width:150px"><div dir="auto" style="font-size:11px;color:#3A4A52">${esc(b.client)||'\u2014'}</div></td>
   <td style="font-size:11px;white-space:nowrap">${esc(dv(DPLAT,platN(b.platform)))}</td>
   <td style="font-size:10.5px;color:#6B7C86">${b.svc?dv(DSVC,b.svc):'\u2014'}</td>
   <td style="text-align:right;font-size:11px;white-space:nowrap">${b.value?fmtSAR(b.value):'\u2014'}</td>
   <td style="text-align:center">${b.nbid!=null?b.nbid:'\u2014'}</td>
   <td><span class="tag" style="background:${OC[b.outcome]}">${t(b.outcome.toUpperCase(),DOUT[b.outcome]||b.outcome)}</span></td>
   <td style="max-width:130px"><div dir="auto" style="font-size:10.5px;color:#6B7C86">${b.winner=='EH'?'<b style="color:#2E7D46">EH</b>':(esc(b.winner)||'\u2014')}</div></td>
 </tr>`).join('');
 $('s-tenders').innerHTML=
 `<div class="sech">${t('All tracked tenders','جميع المنافسات المتتبَّعة')}</div><div class="secsub">${t('Every real tender in the workbooks (empty placeholder rows excluded). Filter by any column or search. ','كل منافسة فعلية في الملفات (بلا صفوف فارغة). صفِّ بأي عمود أو ابحث. ')}<b>${list.length}</b>${t(' of '+BA.bidlist.length+' shown.',' من '+BA.bidlist.length+' معروضة.')}</div>
 ${ctrls}
 <div class="card" style="padding:6px 10px">
 <table class="t"><thead><tr><th>${t('Ref','المرجع')}</th><th>${t('Launched','الطرح')}</th><th>${t('Title','العنوان')}</th><th>${t('Client','العميل')}</th><th>${t('Platform','المنصة')}</th><th>${t('Service','الخدمة')}</th><th style="text-align:right">${t('EH value','قيمة EH')}</th><th style="text-align:center">${t('Bidders','المتقدمون')}</th><th>${t('Outcome','النتيجة')}</th><th>${t('Winner','الفائز')}</th></tr></thead>
 <tbody>${rows||'<tr><td colspan="10" style="text-align:center;padding:30px;color:#9AA8B0">'+t('No tenders match these filters.','لا توجد منافسات مطابقة لهذه الفلاتر.')+'</td></tr>'}</tbody></table></div>`;
}

// ===================== NOTES & LIMITATIONS =====================
function rLimitations(){
 const lim=[
  [t('Small outcome sample','عيّنة نتائج صغيرة'),t('Only 16 of 144 tenders have a recorded winner and 10 have full competitor pricing. Every win-rate figure — overall and especially the slices by service line, platform, value band and bidder count — is computed off those 16, so most breakdowns rest on one to three tenders. Read them as anecdotes, not statistics.','16 فقط من 144 منافسة لها فائز مُسجّل و10 لها تسعير منافسين كامل. كل رقم لنسبة الفوز — إجمالاً وخاصة التقسيمات حسب مجال الخدمة والمنصة وشريحة القيمة وعدد المتقدمين — محسوب من تلك الـ16، فمعظم التفصيلات تستند إلى منافسة أو ثلاث. اقرأها كحكايات لا كإحصاءات.')],
  [t('Pricing ≠ full picture','التسعير ≠ الصورة الكاملة'),t('The pricing analysis shows EH\'s losing bids were priced high, but Saudi tenders are scored on technical merit, compliance, delivery capability and incumbency alongside price. Without the technical scores and the stated loss reason, we cannot prove price caused the losses or rule out that EH was competing on larger scope or quality.','يُظهر تحليل الأسعار أن عروض EH الخاسرة كانت مرتفعة، لكن المنافسات السعودية تُقيَّم على الجدارة الفنية والامتثال وقدرة التنفيذ وأسبقية التعاقد إلى جانب السعر. وبلا الدرجات الفنية وسبب الخسارة المُعلن، يتعذّر إثبات أن السعر سبّب الخسائر أو استبعاد أن EH كان ينافس على نطاق أو جودة أكبر.')],
  [t('2025 vs 2026 not comparable','2025 مقابل 2026 غير قابلة للمقارنة'),t('2026 is a partial, in-progress year — many tenders are still pending and outcomes lag launch by months. A near-complete 2025 is being compared against a half-finished 2026 where wins may simply not be recorded yet. The same depresses the most recent months of any time view.','2026 سنة جزئية جارية — كثير من المنافسات ما زالت معلّقة والنتائج تتأخّر أشهراً عن الطرح. تُقارَن 2025 شبه المكتملة بـ2026 نصف المنجزة حيث قد لا تكون الانتصارات مُسجّلة بعد. والأمر ذاته يخفض أحدث الأشهر في أي عرض زمني.')],
  [t('Recording is not random','التسجيل ليس عشوائياً'),t('Tenders with a logged outcome or pricing are likely those that progressed furthest or that someone chose to complete. If wins or painful losses get logged more diligently, the recorded win rate is biased in an unknown direction. "Win rate among tenders with an outcome" is not the same as the true win rate.','المنافسات ذات النتيجة أو التسعير المُسجّل غالباً هي التي تقدّمت أكثر أو اختار أحدهم إكمالها. وإذا سُجّلت الانتصارات أو الخسائر المؤلمة بعناية أكبر، فنسبة الفوز المُسجّلة منحازة باتجاه مجهول. «نسبة الفوز بين المنافسات ذات النتيجة» ليست كنسبة الفوز الحقيقية.')],
  [t('Competitor / client counts undercount','أعداد المنافسين / العملاء أقل من الحقيقة'),t('The Arabic↔English name reconciliation matches the major recurring rivals and big clients well, but ~130 one-off Arabic-named SMEs go unmatched. "Competitors faced" counts matched competitors only; the real field is larger, and some small clients may be split across name variants.','مطابقة الأسماء عربي↔إنجليزي تُطابق المنافسين المتكررين الكبار والعملاء الكبار جيداً، لكن ~130 منشأة صغيرة بأسماء عربية لمرة واحدة تبقى دون مطابقة. «المنافسون المواجَهون» يعدّ المطابقين فقط؛ فالميدان الحقيقي أكبر، وقد ينقسم بعض العملاء الصغار عبر تنويعات الاسم.')],
  [t('No market denominator','لا مقام سوقي'),t('The dashboard only sees tenders EH tracked — not the tenders EH never bid on or never saw. It therefore cannot measure true market share or bid/no-bid quality. Win rate here is conditional on having bid.','ترى اللوحة فقط المنافسات التي تتبّعها EH — لا التي لم يتقدّم لها EH أو لم يرها قط. لذا يتعذّر قياس الحصة السوقية الحقيقية أو جودة قرار التقديم. ونسبة الفوز هنا مشروطة بالتقديم.')],
  [t('Turnaround is a proxy','مدة القرار مؤشر تقريبي'),t('The workbook records department sign-off as accept/reject but not the date of each review, so true per-department cycle time cannot be measured. The launch-to-deadline window is the closest available stand-in.','يسجّل الملف اعتماد الإدارة كقبول/رفض دون تاريخ كل مراجعة، فيتعذّر قياس زمن الدورة الحقيقي لكل إدارة. ونافذة الطرح-إلى-الموعد النهائي أقرب بديل متاح.')],
  [t('Single self-reported source','مصدر واحد ذاتي التقرير'),t('All figures come from EH\'s own tracking workbooks, a static snapshot with no cross-check against official Etimad award records. Value fields also mix offered and awarded bases and should be read as proxies.','كل الأرقام من ملفات تتبّع EH الخاصة، وهي لقطة ثابتة دون مطابقة مع سجلات ترسية اعتماد الرسمية. كما تخلط حقول القيمة بين أسس العرض والترسية وينبغي قراءتها كمؤشرات تقريبية.')],
 ];
 $('s-limitations').innerHTML=
 `<div class="sech">${t('Notes & limitations','ملاحظات وحدود')}</div><div class="secsub">${t('An honest analyst read on what this dashboard can and cannot tell you. The analytics are only ever as strong as the completeness of the tracking data behind them.','قراءة محلّل صادقة لما تستطيع هذه اللوحة إخبارك به وما لا تستطيع. فالتحليلات قوية بقدر اكتمال بيانات التتبّع خلفها فقط.')}</div>
 <div class="card" style="background:#FFF8EC;border-color:#F0DDB0"><h3 style="color:#8A6D2E">${t('Bottom line','الخلاصة')}</h3><div style="font-size:13px;color:#5A4A2E;line-height:1.6">${t('Use this dashboard to ','استخدم هذه اللوحة لـ')}<b>${t('spot patterns and frame questions','رصد الأنماط وصياغة الأسئلة')}</b>${t(' — where EH may be losing, which clients are slipping, where pricing looks exposed — not to settle them with precision. The headline story (declining win rate, high pricing on losses, SEC concentration) is directionally credible; the exact percentages are not. The single highest-leverage fix is upstream: ',' — أين قد يخسر EH، وأي العملاء يتراجعون، وأين يبدو التسعير مكشوفاً — لا لحسمها بدقّة. القصة الرئيسية (تراجع نسبة الفوز، ارتفاع التسعير في الخسائر، تركّز SEC) موثوقة توجيهياً؛ أما النسب الدقيقة فلا. وأعلى إصلاح أثراً يقع في المنبع: ')}<b>${t('record an outcome and a loss reason for every closed tender, capture the technical score alongside price, and keep a bid/no-bid log.','سجّل نتيجة وسبب خسارة لكل منافسة مُغلقة، والتقط الدرجة الفنية إلى جانب السعر، واحتفظ بسجل تقديم/عدم تقديم.')}</b>${t(' Do that and most caveats below shrink on their own.',' افعل ذلك وستتقلّص معظم التحفّظات أدناه تلقائياً.')}</div></div>
 ${lim.map(([h,b])=>`<div class="card"><h3>${h}</h3><div style="font-size:12.5px;color:#4A5A62;line-height:1.6">${b}</div></div>`).join('')}`;
}

// ===================== WATCHLIST =====================
function rWatchlist(){
 const SEVC={high:'#B23A3A',med:'#E8862E',low:'#2E7D46'};
 $('s-watchlist').innerHTML=
 `<div class="sech">${t('Watchlist — prioritised alerts','قائمة المتابعة — تنبيهات مُرتّبة')}</div><div class="secsub">${t('Auto-flagged signals from the bid data that warrant attention, ranked by severity.','إشارات مُبرزة تلقائياً من بيانات المنافسات تستحق الانتباه، مُرتّبة حسب الأهمية.')}</div>
 <div class="wl">${BA.watchlist.map(f=>`<div class="wli ${f.sev}"><span class="wlk" style="background:${SEVC[f.sev]}">${esc(L==='ar'?(f.kind_ar||f.kind):f.kind)}</span><span>${esc(L==='ar'?(f.text_ar||f.text):f.text)}</span></div>`).join('')}</div>`;
}

function rChrome(){var el;
 if(el=$('h-title'))el.textContent=t('Bid & Tender Intelligence','تحليلات المنافسات والعطاءات');
 if(el=$('h-sub'))el.textContent=t('Environmental Horizons (Afaq Al Beeah) — competitive bid analytics, 2024–2026','آفاق البيئة (Afaq Al Beeah) — تحليلات تنافسية للمنافسات، 2024–2026');
 if(el=$('h-pill'))el.innerHTML=t(k.total+' tenders tracked<br>SAR '+Math.round(k.pipeline/1e6)+'M pipeline',k.total+' منافسة متتبَّعة<br>محفظة بقيمة '+Math.round(k.pipeline/1e6)+' مليون ريال');
 if(el=$('h-foot'))el.textContent=t('Generated for Environmental Horizons · figures reflect the bid-tracking workbooks and are partial where the live trackers are still being filled · self-contained dashboard.','أُعدّت لصالح آفاق البيئة · تعكس الأرقام جداول تتبّع المنافسات وهي جزئية حيثما لا تزال قيد التعبئة · لوحة مستقلة.');}
function renderAll(){rKPI();rOverview();rPipeline();rWinloss();renderPricing();renderCompetitors();rClients();rService();rFunnel();renderTenders();rLimitations();rWatchlist();rChrome();}
function setLang(l){L=l;document.documentElement.setAttribute('dir',l==='ar'?'rtl':'ltr');document.documentElement.lang=l;document.body.classList.toggle('ar',l==='ar');document.querySelectorAll('.langbtn').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-l')===l);});rNav();renderAll();go(curTab);}
rNav();renderAll();go('overview');

// ===== Ask the data (guided Q&A panel) =====
const OUT_AR={Won:'فوز لصالح EH',Lost:'خسارة',"Not awarded":'لم تتم الترسية',Cancelled:'ملغاة',Pending:'قيد الانتظار','Not awarded ':'لم تتم الترسية'};
function ansBox(tEN,tAR,body){return `<div class="ansbox"><div class="anst">${tEN}</div><div class="anst-ar" dir="rtl">${tAR}</div><div class="ansbody">${body}</div></div>`;}
function listAns(tEN,tAR,items){return `<div class="ansbox"><div class="anst">${tEN}</div><div class="anst-ar" dir="rtl">${tAR}</div><div style="margin-top:8px">${items.map((it,i)=>`<div class="ansrow"><div dir="auto" style="flex:1;min-width:0">${i+1}. ${esc(it.name)}${it.sub?` <span style="color:#9AA8B0;font-size:11px">— ${esc(it.sub)}</span>`:''}</div><div style="font-weight:700;color:#1A5FAB;white-space:nowrap">${esc(it.val)}</div></div>`).join('')}</div></div>`;}
function _tender(){var S=document.querySelectorAll('.ehc-sn'),Y=document.querySelectorAll('.ehc-yr');var s=S[S.length-1],y=Y[Y.length-1];var yr=+((y||{}).value),sn=+((s||{}).value);return {yr,sn,t:BA.bidlist.find(x=>x.year==yr&&x.sn==sn)};}
const ANSF={
 freq(){const c=[...BA.competitors].sort((a,b)=>b.encounters-a.encounters).slice(0,7);return listAns('Who competes against EH the most — by tenders faced','من ينافس EH أكثر — حسب عدد المنافسات',c.map(x=>({name:x.name,val:x.encounters+' tenders',sub:x.wins?x.wins+' beat EH':''})));},
 beatEH(){const c=[...BA.competitors].filter(x=>x.wins>0).sort((a,b)=>b.wins-a.wins).slice(0,7);if(!c.length)return ansBox('No single competitor has a recorded win over EH','لا يوجد منافس بعينه تغلّب على EH','In the tracked outcomes, EH losses are not concentrated on one named competitor.');return listAns('Who beats EH the most — recorded wins over EH','من يتغلب على EH أكثر',c.map(x=>({name:x.name,val:x.wins+(x.wins>1?' wins':' win'),sub:'faced '+x.encounters+'x'})));},
 losing(){const s=[...BA.service_mix].filter(x=>x.awarded>0).sort((a,b)=>a.win_rate-b.win_rate);return listAns('Where EH loses most — service lines by win rate (decided tenders)','أين تخسر EH أكثر — حسب مجال الخدمة',s.map(x=>({name:x.name,val:x.win_rate+'% win rate',sub:x.won+' of '+x.awarded+' won'})));},
 biggest(){const c=[...BA.competitors].sort((a,b)=>(b.wins-a.wins)||(b.encounters-a.encounters)).slice(0,7);return listAns(`EH's biggest competitors — wins over EH, then frequency`,'أبرز منافسي EH',c.map(x=>({name:x.name,val:(x.wins?x.wins+' beat EH · ':'')+x.encounters+' faced',sub:x.undercut_pct!=null?'undercut EH '+x.undercut_pct+'% of priced meets':''})));},
 pricing(){const s=BA.pricing.summary;const hi=s.median_gap>50;return ansBox(hi?'EH pricing looks high versus the field':'EH pricing is broadly competitive',hi?'أسعار EH مرتفعة مقارنة بالمنافسين':'أسعار EH تنافسية إجمالاً',`Across the <b>${s.full}</b> tenders with full bidder pricing, EH was the outright cheapest bidder <b>${s.cheapest_pct}%</b> of the time and sat at the <b>${s.avg_percentile}th</b> price percentile on average (1st = cheapest). Median gap to the lowest bid: <b>${s.median_gap>0?'+':''}${s.median_gap}%</b>. ${hi?'On many tenders EH bid well above the lowest — a real competitive exposure worth reviewing.':'EH is generally close to the lowest bid.'}<br><span style="color:#9AA8B0">Price is only one factor — technical score, compliance and delivery also decide Saudi tenders, and those are not captured here.</span>`);},
 time(){const t=BA.turnaround;const rushed=t.tight14/t.n;return ansBox('Time the committee allows to prepare a proposal','الوقت الذي تتيحه اللجنة لإعداد العرض',`The full review window (launch to submission deadline) runs <b>${t.mean} days on average</b> (median ${t.median}). But <b>${t.tight14} of ${t.n}</b> tenders compress the whole decision into two weeks or less, and <b>${t.tight7}</b> into a single week — little time for a considered technical and pricing response. ${rushed>=0.3?'A meaningful share are rushed, which can push EH toward weaker or higher-priced bids.':'Most tenders have a reasonable window.'}`);},
 status(){const {yr,sn,t}=_tender();if(!yr||!sn)return ansBox('Enter a tender number and year first','أدخل رقم المنافسة والسنة أولاً','Use the two boxes at the top of this tab, then tap the question again.');if(!t)return ansBox('Tender not found','المنافسة غير موجودة',`No tender #${sn} for ${yr} is in the tracker.`);return ansBox(`Tender #${sn}/${yr} — ${t.outcome}`,`المنافسة رقم ${sn}/${yr} — ${OUT_AR[t.outcome]||t.outcome}`,`<b dir="auto">${esc(t.title)||'(untitled)'}</b><br>Client: ${esc(t.client)||'—'} · Platform: ${t.platform||'—'}<br>Outcome: <b>${t.outcome}</b>${t.winner?' · Winner: <span dir="auto">'+esc(t.winner)+'</span>':''}${t.value?' · Value: '+fmtSAR(t.value):''}${t.nbid?' · '+t.nbid+' bidders':''}${t.date?' · Launched '+t.date:''}`);},
 why(){const {yr,sn,t}=_tender();if(!yr||!sn)return ansBox('Enter a tender number and year first','أدخل رقم المنافسة والسنة أولاً','Use the two boxes at the top of this tab, then tap the question again.');if(!t)return ansBox('Tender not found','المنافسة غير موجودة',`No tender #${sn} for ${yr} is in the tracker.`);let b=`<b dir="auto">${esc(t.title)||'(untitled)'}</b><br>`;if(t.committee)b+=`Bid-committee decision: <b dir="auto">${esc(t.committee)}</b><br>`;if(t.reason)b+=`Recorded note / reason: <span dir="auto">${esc(t.reason)}</span><br>`;if(!t.committee&&!t.reason)b+='No committee decision or reason is recorded for this tender in the tracker.';return ansBox(`Why tender #${sn}/${yr}?`,`لماذا المنافسة ${sn}/${yr}؟`,b);},
 service(){const s=[...BA.service_mix].sort((a,b)=>b.count-a.count);return listAns('Most-requested service lines — by tender count','الخدمات الأكثر طلباً — حسب عدد المنافسات',s.map(x=>({name:x.name,val:x.count+' tenders',sub:fmtSAR(x.value)+' total'})));},
};
const ASKQS=[['freq','Who competes against EH the most?','من ينافس EH أكثر؟'],['beatEH','Who beats EH the most?','من يتغلب على EH أكثر؟'],['losing','Where is EH losing in the competition?','أين تخسر EH في المنافسة؟'],['biggest',"Who are EH's biggest competitors?",'من أبرز منافسي EH؟'],['pricing',"Is EH's pricing competitive?",'هل أسعار EH تنافسية؟'],['time','Does the committee allow enough time to bid?','هل تمنح لجنة EH وقتاً كافياً للتقديم؟'],['status','What is the status of a specific tender?','ما حالة منافسة محددة؟'],['why','Why was a specific tender approved / rejected?','لماذا تمت الموافقة/الرفض على منافسة؟'],['service','Which service is requested the most?','ما الخدمة الأكثر طلباً؟']];
const QKW={
 freq:['compete','competes','competitor','competitors','bids against','bid against','against eh','against us','who bids','who else bids','faced','face','often','frequent','ينافس','منافسين','ضد','مواجهه','يتقدم','يقدمون'],
 beatEH:['beat','beats','win against','wins against','who wins','who beats','defeat','defeats','lose to','losing to','beating us','يفوز','يتغلب','يغلب','يهزم','يفوز علينا'],
 losing:['losing','lose','lost','weak','worst','underperform','poor performance','where are we losing','ضعف','تخسر','نخسر','خساره','اخسر','اين نخسر','نقاط الضعف'],
 biggest:['biggest','main','major','rivals','strongest','key competitor','top competitor','ابرز','اكبر','رئيسي','اهم','اقوى','منافس رئيسي'],
 pricing:['pricing','price','prices','cost','costs','cheap','expensive','competitive','overbid','underbid','too high','رخيص','غالي','سعر','اسعار','تسعير','تكلفه','تنافسي','مرتفع'],
 time:['time','committee','decision','enough time','prepare','preparation','deadline','window','rush','rushed','turnaround','وقت','لجنه','قرار','كافي','تحضير','اعداد','موعد','مهله','ضيق الوقت'],
 status:['status','state','result','outcome','stage','what happened','حاله','وضع','نتيجه','مصير','ماذا حدث'],
 why:['why','reason','reasons','approved','approve','rejected','reject','declined','decline','refused','accepted','لماذا','سبب','موافقه','رفض','مرفوض','قبول'],
 service:['service','services','requested','request','most requested','popular','demand','category','type of work','خدمه','خدمات','طلب','مطلوب','فئه','نوع العمل','الاكثر طلبا'],
};
function _norm(t){t=(t||'').toLowerCase();['أ','إ','آ'].forEach(a=>t=t.split(a).join('ا'));return t.split('ة').join('ه').split('ى').join('ي').replace(/[\u064B-\u0652]/g,'');}
function matchQ(text){const q=_norm(text);if(!q.trim())return[];return ASKQS.map(function(x){var id=x[0],s=0;(QKW[id]||[]).forEach(function(k){if(q.indexOf(_norm(k))>=0)s++;});return [id,s];}).filter(function(a){return a[1]>0;}).sort(function(a,b){return b[1]-a[1];}).slice(0,4).map(function(a){return a[0];});}

(function(){
 var css='#ehcbtn{position:fixed;bottom:22px;right:22px;width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#33A85B,#1A5FAB);box-shadow:0 6px 20px rgba(26,95,171,.35);cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:99999;border:none;transition:transform .15s}#ehcbtn:hover{transform:scale(1.06)}#ehcbtn svg{width:27px;height:27px;fill:#fff}#ehcp{position:fixed;bottom:92px;right:22px;width:374px;max-width:calc(100vw - 28px);height:544px;max-height:calc(100vh - 128px);background:#fff;border-radius:16px;box-shadow:0 14px 44px rgba(0,0,0,.24);z-index:99999;display:none;flex-direction:column;overflow:hidden}#ehcp.open{display:flex}.ehch{background:linear-gradient(135deg,#2E9E5B,#1A5FAB);color:#fff;padding:13px 16px;display:flex;align-items:center;gap:8px}.ehch b{font-size:14.5px}.ehch .s{font-size:10.5px;opacity:.9}.ehcx{margin-left:auto;cursor:pointer;font-size:19px;opacity:.9;line-height:1}.ehcb{flex:1;overflow-y:auto;padding:13px;background:#F5F8FA;display:flex;flex-direction:column;gap:9px}.ehm{background:#fff;border:1px solid #E7EDF0;border-radius:12px;border-top-left-radius:3px;padding:10px 12px;font-size:12.5px;color:#3A4A52;line-height:1.5;max-width:92%}.ehu{background:#E7F1FB;border:1px solid #CFE3F5;border-radius:12px;border-bottom-right-radius:3px;padding:9px 12px;font-size:12.5px;color:#14456a;align-self:flex-end;max-width:85%}.ehchip{display:block;width:100%;text-align:left;background:#fff;border:1px solid #CFE0EC;border-radius:10px;padding:9px 11px;margin-top:6px;cursor:pointer;font-size:12.5px;color:#1A5FAB;font-weight:600}.ehchip:hover{background:#EAF3FB;border-color:#1A5FAB}.ehchip .ar{display:block;color:#8494A0;font-weight:500;font-size:11.5px;margin-top:2px}.ehcf{border-top:1px solid #E7EDF0;padding:9px;display:flex;gap:7px;background:#fff}.ehcf input{flex:1;border:1px solid #D5DEE2;border-radius:20px;padding:9px 14px;font-size:13px;outline:none}.ehcf input:focus{border-color:#1A5FAB}.ehsend{background:linear-gradient(135deg,#2E9E5B,#1A5FAB);border:none;color:#fff;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:15px;flex:none}.ehcb .ansbox{max-width:100%}';
 var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
 var w=document.createElement('div');
 w.innerHTML='<button id="ehcbtn" aria-label="Ask the data"><svg viewBox="0 0 24 24"><path d="M12 3C6.5 3 2 6.6 2 11c0 2.3 1.2 4.4 3.3 5.9-.2 1-.8 2.3-1.6 3.3 1.5-.2 3-.8 4.3-1.6 1.2.4 2.5.6 3.7.6 5.5 0 10-3.6 10-8s-4.5-8-10-8z"/></svg></button><div id="ehcp"><div class="ehch"><div><b>Ask the data</b><div class="s">\u0627\u0633\u0623\u0644 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u00b7 runs in your browser</div></div><div class="ehcx">\u2715</div></div><div class="ehcb" id="ehcb"></div><div class="ehcf"><input id="ehci" placeholder="Type your question\u2026 \u0627\u0643\u062a\u0628 \u0633\u0624\u0627\u0644\u0643"><button class="ehsend">\u279c</button></div></div>';
 document.body.appendChild(w);
 window.ehChat={
  open:false,
  toggle:function(){this.open=!this.open;document.getElementById('ehcp').classList.toggle('open',this.open);if(this.open&&!this._g){this._g=1;this.greet();document.getElementById('ehci').focus();}},
  add:function(h){var b=document.getElementById('ehcb');var d=document.createElement('div');d.style.display='contents';d.innerHTML=h;b.appendChild(d);b.scrollTop=b.scrollHeight;},
  greet:function(){this.add('<div class="ehm">Hi \ud83d\udc4b Ask about EH\u2019s competitors, pricing, win rate, service mix, or a specific tender \u2014 type a question and press Enter.<br><span dir="rtl" style="color:#8494A0">\u0645\u0631\u062d\u0628\u0627\u064b! \u0627\u0633\u0623\u0644\u0646\u064a \u0639\u0646 \u0645\u0646\u0627\u0641\u0633\u064a EH \u0623\u0648 \u0627\u0644\u0623\u0633\u0639\u0627\u0631 \u0623\u0648 \u0646\u0633\u0628\u0629 \u0627\u0644\u0641\u0648\u0632 \u0623\u0648 \u0645\u0646\u0627\u0641\u0633\u0629 \u0645\u062d\u062f\u062f\u0629.</span></div>');this.chips(['freq','pricing','service'],'Popular \u00b7 \u0623\u0633\u0626\u0644\u0629 \u0634\u0627\u0626\u0639\u0629:');},
  chips:function(ids,label){var h='<div class="ehm">'+label;ids.forEach(function(id){var q=ASKQS.find(function(x){return x[0]===id;});h+='<button class="ehchip" data-q="'+id+'">'+q[1]+'<span class="ar" dir="rtl">'+q[2]+'</span></button>';});h+='</div>';this.add(h);},
  submit:function(){var inp=document.getElementById('ehci');var t=inp.value.trim();if(!t)return;this.add('<div class="ehu">'+esc(t)+'</div>');inp.value='';var ids=matchQ(t);if(ids.length)this.chips(ids,'Closest to your question \u2014 tap one \u00b7 \u0627\u0644\u0623\u0642\u0631\u0628 \u0644\u0633\u0624\u0627\u0644\u0643:');else this.chips(ASKQS.map(function(x){return x[0];}).slice(0,6),'I couldn\u2019t match that \u2014 try one of these \u00b7 \u062c\u0631\u0651\u0628:');},
  answer:function(id){var q=ASKQS.find(function(x){return x[0]===id;});this.add('<div class="ehu">'+q[1]+'</div>');if(id==='status'||id==='why'){this.tform(id);return;}this.add(ANSF[id]());},
  tform:function(id){this.add('<div class="ehm">Which tender? \u00b7 \u0623\u064a \u0645\u0646\u0627\u0641\u0633\u0629\u061f<div style="display:flex;gap:6px;margin-top:7px;align-items:center;flex-wrap:wrap"><input class="ehc-sn" type="number" placeholder="13" style="width:66px;padding:6px 8px;border:1px solid #D5DEE2;border-radius:6px;font-size:13px"><select class="ehc-yr" style="padding:6px;border:1px solid #D5DEE2;border-radius:6px;font-size:13px"><option>2026</option><option>2025</option></select><button class="ehchip" style="width:auto;margin:0;padding:7px 14px" data-go="'+id+'">Look up \u00b7 \u0639\u0631\u0636</button></div></div>');},
 };
 document.getElementById('ehcbtn').onclick=function(){ehChat.toggle();};
 w.querySelector('.ehcx').onclick=function(){ehChat.toggle();};
 w.querySelector('.ehsend').onclick=function(){ehChat.submit();};
 document.getElementById('ehci').addEventListener('keydown',function(e){if(e.key==='Enter')ehChat.submit();});
 document.getElementById('ehcb').addEventListener('click',function(e){var c=e.target.closest('[data-q]');if(c){ehChat.answer(c.getAttribute('data-q'));return;}var g=e.target.closest('[data-go]');if(g){ehChat.add(ANSF[g.getAttribute('data-go')]());}});
})();
