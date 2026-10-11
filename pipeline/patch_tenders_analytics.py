"""patch_tenders_analytics.py — All Tenders: live analytics, honest sentences and data checks (11 Oct 2026).

Reviewed before build in an agent arena (three independent Claude analysts → cross-review → separate judge) against
tracker v6. Run AFTER patch_bid_submatch.py (it uses the submission fields that patch adds).

What it changes (exact-string edits; stops if an anchor is missing):
  app.js
   • All Tenders rebuilt: a "Show" filter (Needs a result · Deadline still open · Accepted, no submission recorded ·
     Data gaps to fix · Deadline probably extended), a filter-aware summary strip (count, results, win rate with its
     likely range — hidden under 10 results — indicative value, median bidders, needs-a-result count), live
     "What this view says" sentences, a deadline cell that says "closes in N days" / "N days, no result" /
     "probably extended", data-check chips per row (red = contradiction, amber = missing, grey = rule, not error),
     winner-price values greyed and left out of totals, very-large tenders (≥20% of the shown total) marked with an
     option to leave them out of the value total, and "Export this list (CSV)".
   • Overview: the typed "win rate fell sharply" sentence is replaced by a live year-on-year sentence that says
     "no clear change" when the likely ranges overlap.
   • Notes & Limits: the typed headline story and the "Open pipeline" and "2025 vs 2026" cards become live text.
   • Bid Turnaround: new card "How close to the deadline EH submits".
  bid_analytics2.py
   • "Tenders where EH was cheapest" now counts every fully priced tender where EH was lowest (it only counted
     tenders EH lost, so it always read 0).
   • The "Win-rate decline" watch item fires only when the two years' likely ranges do not overlap.

Run once:  python3 pipeline/patch_tenders_analytics.py
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_change_table

J, A = (os.path.join(HERE, f) for f in ('app.js', 'bid_analytics2.py'))
if 'function tNeeds(' in open(J, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
if 'ehsubdate' not in open(A, encoding='utf-8').read():
    sys.exit('Run patch_bid_submatch.py first.')
load(J, 'app'); load(A, 'analytics')

BLOCK = r'''// ===================== TENDER ANALYTICS (11 Oct 2026 — every rule below was challenged in the agent arena) =====================
// Everything is computed live from BA.bidlist; no figure on the page is typed in.
const TODAY=new Date(Date.now()+3*36e5).toISOString().slice(0,10);   // today in KSA
function dDays(a,b){return Math.round((Date.parse(b)-Date.parse(a))/864e5);}
function wilson(k,n){if(!n)return null;const z=1.959964,p=k/n,den=1+z*z/n,c=(p+z*z/(2*n))/den,h=z*Math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den;return [Math.max(0,Math.round(100*(c-h))),Math.min(100,Math.round(100*(c+h)))];}
function tMed(a){a=a.filter(x=>x!=null).sort((x,y)=>x-y);if(!a.length)return null;const m=a.length>>1;return a.length%2?a[m]:Math.round((a[m-1]+a[m])/2);}
function tSub(b){return b.submitted!=null?!!b.submitted:(b.sub=='date'||b.sub=='yes');}
function tRej(b){return /reject|رفض/i.test(b.committee||'');}
function tAcc(b){return /accept|موافق/i.test(b.committee||'');}
// the day a result could first be expected: the deadline, or EH's submission date when the client extended the deadline
function tRef(b){return (b.subdate&&b.deadline&&b.subdate>b.deadline)?b.subdate:b.deadline;}
function tDaysPast(b){return b.deadline?dDays(tRef(b),TODAY):null;}
// Needs a result = pending, EH submitted, not declined by the committee, past the deadline
function tNeeds(b){const d=tDaysPast(b);return b.outcome=='Pending'&&tSub(b)&&!tRej(b)&&d!=null&&d>0;}
function tAhead(b){return b.outcome=='Pending'&&!!b.deadline&&b.deadline>=TODAY&&!tRej(b);}
function tAccNoSub(b){return tAcc(b)&&(b.sub=='none'||b.sub=='no')&&b.outcome=='Pending'&&(tDaysPast(b)||0)>0;}
function tLostNoBid(b){return b.outcome=='Lost'&&(['no','none','rejected'].indexOf(b.sub)>=0||!!b.sub_conflict);}
// on a lost tender with a named winner the tracker's value is the winner's price, not EH's offer
function tWinPrice(b){return b.outcome=='Lost'&&!!b.winner&&b.winner!='EH'&&!!b.value;}
function tRate(Lst){const d=Lst.filter(b=>b.outcome=='Won'||b.outcome=='Lost');const w=d.filter(b=>b.outcome=='Won').length;
 return {w:w,n:d.length,p:d.length?Math.round(100*w/d.length):null,ci:d.length>=10?wilson(w,d.length):null,nobid:d.filter(tLostNoBid)};}
function tYearsWith(f){const s={};(BAD.both.bidlist||[]).forEach(b=>{if(b[f])s[b.year]=1;});return s;}
const YR_AWD=tYearsWith('awarddate'), YR_SUBD=tYearsWith('subdate');
function tUnknownYrs(Lst){return [...new Set(Lst.filter(b=>!YR_SUBD[b.year]).map(b=>b.year))].sort();}
function tBadges(b){const B=[];const add=(l,en,ar)=>B.push({l:l,en:en,ar:ar});
 if(tLostNoBid(b))add('r','Counted as lost, but EH did not submit','محسوبة خسارة رغم أن EH لم تقدّم');
 if(b.deadline&&b.date&&b.deadline<b.date)add('r','Deadline is before the launch date','الموعد النهائي قبل تاريخ الطرح');
 if(b.subgap&&Math.abs(b.subgap.days)>=30)add('r','Submission dates disagree ('+Math.abs(b.subgap.days)+' days apart)','تواريخ التقديم متعارضة (فارق '+Math.abs(b.subgap.days)+' يوماً)');
 if(tSub(b)&&!b.subdate&&YR_SUBD[b.year]&&b.outcome!='Cancelled')add('a','Submitted, no date recorded','قُدِّم دون تاريخ مسجّل');
 if(b.outcome=='Lost'&&!b.winner&&!tLostNoBid(b)&&(lossCat(b.lossreason)||{}).k!=='tech')add('a','Lost, no winner recorded','خسارة دون فائز مسجّل');
 if((b.outcome=='Won'||b.outcome=='Lost')&&!b.awarddate&&YR_AWD[b.year]&&!tLostNoBid(b))add('a','Result, no award date','نتيجة دون تاريخ ترسية');
 if((b.outcome=='Won'||b.outcome=='Lost')&&b.nbid==null&&!tLostNoBid(b))add('a','Result, no bidder count','نتيجة دون عدد المتقدمين');
 if(tAccNoSub(b))add('a','Committee accepted, no submission recorded','قبلتها اللجنة دون تقديم مسجّل');
 if(b.deadline_stale)add('g','Deadline probably extended — tracker shows the original','الموعد مُدّد على الأرجح — الملف يُظهر الأصلي');
 return B;}
function tGap(b){return tBadges(b).some(x=>x.l!='g');}
function tChips(b){return tBadges(b).map(x=>`<span class="tchip tc-${x.l}" title="${esc(t(x.en,x.ar))}">${esc(t(x.en,x.ar))}</span>`).join('');}
// tracked value for a set of rows: EH offers and EH wins only (winner prices left out); very large = ≥20% of the total
function tValue(Lst,dropBig){const rows=Lst.filter(b=>b.value&&!tWinPrice(b));const tot=rows.reduce((a,b)=>a+b.value,0);
 const big=new Set(rows.length>=3?rows.filter(b=>b.value>=0.2*tot).map(b=>b.year+'-'+b.sn):[]);
 const kept=dropBig?rows.filter(b=>!big.has(b.year+'-'+b.sn)):rows;
 return {total:kept.reduce((a,b)=>a+b.value,0),n:kept.length,all:rows.length,big:big,dropped:dropBig?big.size:0};}
function tRateTxt(r){if(!r.n)return t('no tender with a result','لا منافسة لها نتيجة');
 if(!r.ci)return t(r.w+' won of '+r.n+' with a result — too few to give a rate',r.w+' فوز من '+r.n+' لها نتيجة — عدد أقل من أن يُعطي نسبة');
 return t(r.p+'% ('+r.w+' of '+r.n+'; likely between '+r.ci[0]+'% and '+r.ci[1]+'%)',r.p+'% ('+r.w+' من '+r.n+'؛ على الأرجح بين '+r.ci[0]+'% و'+r.ci[1]+'%)');}
// year-on-year sentence — replaces the typed "win rate fell sharply"
function tTrend(){const Lst=BAD.both.bidlist||[];const ys=[...new Set(Lst.map(b=>b.year))].sort();if(ys.length<2)return '';
 const y0=ys[ys.length-2],y1=ys[ys.length-1];const A=Lst.filter(b=>b.year==y0),B=Lst.filter(b=>b.year==y1);
 const r0=tRate(A),r1=tRate(B);const md=TODAY.slice(5);
 const sameA=A.filter(b=>b.date&&b.date.slice(5)<=md).length;
 let s=t(B.length+' tenders tracked in '+y1+' so far, against '+sameA+' by the same date in '+y0+' ('+A.length+' in the whole year) — part of any rise may be fuller tracking. ',
   B.length+' منافسة متتبَّعة في '+y1+' حتى الآن، مقابل '+sameA+' حتى التاريخ نفسه في '+y0+' ('+A.length+' في العام كاملاً) — وقد يعود جزء من أي ارتفاع إلى تتبّع أكمل. ');
 if(!r0.ci||!r1.ci)return s+t('Too few tenders have a result to compare win rates.','عدد المنافسات ذات النتيجة أقل من أن تُقارن نسب الفوز.');
 const ov=r0.ci[0]<=r1.ci[1]&&r1.ci[0]<=r0.ci[1];
 if(ov)return s+t('Win rate '+r0.p+'% → '+r1.p+'%, but with only '+r0.n+' and '+r1.n+' results the likely ranges ('+r0.ci[0]+'–'+r0.ci[1]+'% and '+r1.ci[0]+'–'+r1.ci[1]+'%) overlap, so there is no clear change.',
   'نسبة الفوز '+r0.p+'% ← '+r1.p+'%، لكن مع '+r0.n+' و'+r1.n+' نتيجة فقط تتداخل النطاقات المرجّحة ('+r0.ci[0]+'–'+r0.ci[1]+'% و'+r1.ci[0]+'–'+r1.ci[1]+'%)، فلا تغيّر واضح.');
 const up=r1.p>r0.p;return s+t('Win rate '+r0.p+'% → '+r1.p+'% — clearly '+(up?'higher':'lower')+' (likely ranges '+r0.ci[0]+'–'+r0.ci[1]+'% and '+r1.ci[0]+'–'+r1.ci[1]+'% do not overlap).',
   'نسبة الفوز '+r0.p+'% ← '+r1.p+'% — '+(up?'أعلى':'أدنى')+' بوضوح (النطاقان '+r0.ci[0]+'–'+r0.ci[1]+'% و'+r1.ci[0]+'–'+r1.ci[1]+'% لا يتداخلان).');}
function tLossSplit(Lst){const L2=Lst.filter(b=>b.outcome=='Lost'&&!tLostNoBid(b));let p=0,te=0,o=0;L2.forEach(b=>{const c=lossCat(b.lossreason);if(c&&c.k=='price')p++;else if(c&&c.k=='tech')te++;else o++;});return {n:L2.length,price:p,tech:te,other:o};}
function tTopClient(Lst){const W=Lst.filter(b=>b.outcome=='Won'&&b.value);const tot=W.reduce((a,b)=>a+b.value,0);if(W.length<3||!tot)return null;
 const g={};W.forEach(b=>{const k=(b.client||'').split('\n').pop().trim()||'—';g[k]=(g[k]||0)+b.value;});
 const top=Object.entries(g).sort((a,b)=>b[1]-a[1])[0];const nT=Lst.filter(b=>(b.client||'').indexOf(top[0])>=0).length;
 const big=W.slice().sort((a,b)=>b.value-a.value)[0];
 return {name:top[0],share:Math.round(100*top[1]/tot),ntend:nT,nall:Lst.length,big:big.year+'-'+big.sn,bigshare:Math.round(100*big.value/tot)};}
function tAwardLag(Lst){const d=Lst.filter(b=>b.awarddate&&b.deadline&&(b.outcome=='Won'||b.outcome=='Lost')).map(b=>dDays(tRef(b),b.awarddate)).filter(x=>x>=0);return {n:d.length,m:tMed(d)};}
function tHeadline(){const Lst=BA.bidlist||[];const ls=tLossSplit(Lst),tc=tTopClient(Lst),r=tRate(Lst);const parts=[];
 parts.push(t('win rate '+tRateTxt(r),'نسبة الفوز '+tRateTxt(r)));
 if(ls.n)parts.push(t(ls.price+' of '+ls.n+' lost bids were lost on price and '+ls.tech+' on technical rejection',ls.price+' من '+ls.n+' عرضاً خاسراً خسرت بسبب السعر و'+ls.tech+' برفض فني'));
 if(tc)parts.push(t('<bdi>'+esc(tc.name)+'</bdi> accounts for '+tc.share+'% of won value','<bdi>'+esc(tc.name)+'</bdi> يمثّل '+tc.share+'% من قيمة ما فاز به EH'));
 return t('On today\'s data: ','على بيانات اليوم: ')+parts.join(t('; ','؛ '))+t('. ','. ');}

const TF={year:'all',outcome:'all',platform:'all',svc:'all',q:'',flag:'all',bigx:false};
function setTF(kk,v){TF[kk]=v;TF.only=null;renderTenders();}
function platN(p){p=(p||'').toLowerCase();if(p.includes('etimad'))return 'Etimad';if(p.includes('ariba')||p.includes('sec')||p.includes('sap'))return 'SEC-SAP / SAP Ariba';if(p.includes('mail'))return 'Email';return p?'Other':'—';}
function uniqVals(fn){return [...new Set(BA.bidlist.map(fn).filter(x=>x&&x!=='—'))].sort();}
const SUBW={yes:['Submitted — date not recorded','قُدِّم العرض — التاريخ غير مسجّل'],
 no:['EH did not submit','لم تقدّم EH عرضاً'],
 rejected:['EH did not submit — the bid committee said no','لم تقدّم EH عرضاً — رفضت لجنة المنافسات المشاركة'],
 cancelled:['EH did not submit — the tender was cancelled','لم تقدّم EH عرضاً — أُلغيت المنافسة'],
 open:['Not submitted yet — the deadline is still open','لم يُقدَّم بعد — الموعد ما زال مفتوحاً'],
 none:['EH did not submit — no offer recorded','لم تقدّم EH عرضاً — لا عرض مسجّل'],
 unrecorded:['No submission recorded in the tracker','لا تقديم مسجّل في ملف المتابعة']};
function subCell(b){if(b.subdate)return `<span style="font-size:10.5px;color:#1A5FAB;font-weight:600;white-space:nowrap">${b.subdate}</span>${b.subsrc=='proposal'?`<div class="tnote">${t('from the proposal dates','من تواريخ العرضين')}</div>`:''}${b.subgap?`<div class="tnote">${t('proposals dated '+b.subgap.proposal,'العرضان بتاريخ '+b.subgap.proposal)}</div>`:''}`;
 const w=SUBW[b.sub]||SUBW.unrecorded, col=b.sub=='yes'?'#1A5FAB':(b.sub=='open'?'#3E86C8':'#77868F');
 return `<div dir="auto" style="font-size:10px;color:${col};max-width:150px;line-height:1.35;white-space:normal">${t(w[0],w[1])}</div>`;}
function dlCell(b){if(!b.deadline)return `<span style="color:#77868F;font-size:10px;white-space:normal">${t('No deadline recorded','لا موعد مسجّل')}</span>`;
 let s=`<span style="white-space:nowrap">${b.deadline}</span>`;
 if(tAhead(b)){const d=dDays(TODAY,b.deadline);const hot=d<=3&&!tSub(b);s+=`<div class="tnote" style="color:${hot?'#A03A36':'#3E86C8'};font-weight:${hot?700:600}">${d==0?t('closes today','يُغلق اليوم'):t('closes in '+d+' day'+(d==1?'':'s'),'يُغلق خلال '+d+' يوم')}</div>`;}
 else if(tNeeds(b)){const d=tDaysPast(b);const c=d>90?'#A03A36':(d>60?'#B5651D':'#6B7C86');s+=`<div class="tnote" style="color:${c};font-weight:${d>60?700:500}">${t(d+' days, no result',d+' يوماً دون نتيجة')}</div>`;}
 if(b.deadline_stale)s+=`<div class="tnote">${t('probably extended','مُدّد على الأرجح')}</div>`;
 return s;}
function tCSV(list){const H=['Ref','Year','Title','Client','Platform','Submission deadline','EH submitted','Days past deadline, no result','Outcome','Value (SAR, indicative)','Value note','Checks'];
 const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""').replace(/\s+/g,' ').trim()+'"';
 const rows=list.map(b=>[b.year+'-'+b.sn,b.year,b.title,b.client,platN(b.platform),b.deadline||'',b.subdate||(tSub(b)?'submitted, no date':''),tNeeds(b)?tDaysPast(b):'',b.outcome,b.value||'',tWinPrice(b)?"winner's price, not EH's offer":'',tBadges(b).map(x=>x.en).join('; ')].map(q).join(','));
 const blob=new Blob(['﻿'+[H.map(q).join(',')].concat(rows).join('\r\n')],{type:'text/csv;charset=utf-8'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='EH_tenders_'+(TF.flag=='all'?'list':TF.flag)+'_'+TODAY+'.csv';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);}
let _tLast=[];
function tFlagOK(b){switch(TF.flag){case 'needs':return tNeeds(b);case 'ahead':return tAhead(b);case 'accnosub':return tAccNoSub(b);case 'gaps':return tGap(b);case 'stale':return !!b.deadline_stale;default:return true;}}
function renderTenders(){
 const OC={'Won':'#2E7D46','Lost':'#C0504D','Not awarded':'#E8862E','Cancelled':'#5F7078','Pending':'#3E86C8'};
 const list=BA.bidlist.filter(b=>
   (TF.year=='all'||b.year==TF.year)&&
   (TF.outcome=='all'||b.outcome==TF.outcome)&&
   (TF.platform=='all'||platN(b.platform)==TF.platform)&&
   (TF.svc=='all'||b.svc==TF.svc)&&
   (!TF.q||((b.title+' '+b.client+' #'+b.sn).toLowerCase().includes(TF.q.toLowerCase())))&&
   tFlagOK(b)&&
   (!TF.only||TF.only.has(b.year+'-'+b.sn)));
 _tLast=list;
 const ss='padding:7px 10px;border:1px solid #CBD6DC;border-radius:7px;font-size:12px;color:#3A4A52;background:#fff;cursor:pointer';
 const sel=(kk,opts,lab,disp)=>`<div style="display:flex;flex-direction:column;gap:3px"><label style="font-size:10px;color:#8A99A3;text-transform:uppercase;letter-spacing:.4px;font-weight:600">${lab}</label><select onchange="setTF('${kk}',this.value)" style="${ss}">${['all',...opts].map(o=>`<option value="${o}" ${TF[kk]==o?'selected':''}>${o=='all'?t('All','الكل'):(disp?disp(o):o)}</option>`).join('')}</select></div>`;
 const outcomes=['Won','Lost','Not awarded','Cancelled','Pending'].filter(o=>BA.bidlist.some(b=>b.outcome==o));
 const FL={needs:[t('Needs a result','بانتظار نتيجة'),BA.bidlist.filter(tNeeds).length],ahead:[t('Deadline still open','الموعد ما زال مفتوحاً'),BA.bidlist.filter(tAhead).length],accnosub:[t('Accepted, no submission recorded','مقبولة دون تقديم مسجّل'),BA.bidlist.filter(tAccNoSub).length],gaps:[t('Data gaps to fix','ثغرات بيانات للتصحيح'),BA.bidlist.filter(tGap).length],stale:[t('Deadline probably extended','الموعد مُدّد على الأرجح'),BA.bidlist.filter(b=>b.deadline_stale).length]};
 const years=[...new Set(BA.bidlist.map(b=>String(b.year)))].sort();
 const ctrls=`<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;margin-bottom:14px;background:#fff;border:1px solid #E3EAE5;border-radius:11px;padding:13px 15px" class="tctl">
   ${sel('year',years,t('Year','السنة'))}
   ${sel('outcome',outcomes,t('Outcome','النتيجة'),o=>dv(DOUT,o))}
   ${sel('platform',uniqVals(b=>platN(b.platform)),t('Platform','المنصة'),o=>dv(DPLAT,o))}
   ${sel('svc',uniqVals(b=>b.svc),t('Service line','مجال الخدمة'),o=>dv(DSVC,o))}
   ${sel('flag',Object.keys(FL).filter(k=>FL[k][1]>0||TF.flag==k),t('Show','عرض'),o=>FL[o][0]+' ('+FL[o][1]+')')}
   <div style="display:flex;flex-direction:column;gap:3px;flex:1;min-width:180px"><label style="font-size:10px;color:#8A99A3;text-transform:uppercase;letter-spacing:.4px;font-weight:600">${t('Search title / client / ref','البحث في العنوان / العميل / المرجع')}</label>
     <input oninput="setTF('q',this.value)" value="${esc(TF.q)}" placeholder="${t('Type to filter…','للتصفية اكتب…')}" style="${ss};width:100%;cursor:text"></div>
   <button onclick="TF.year='all';TF.outcome='all';TF.platform='all';TF.svc='all';TF.q='';TF.flag='all';TF.bigx=false;TF.only=null;renderTenders()" style="padding:8px 14px;border:1px solid #D5DEE2;background:#F4F8F5;color:#6B7C86;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer">${t('Reset','إعادة تعيين')}</button>
   <button onclick="tCSV(_tLast)" title="${t('Download the rows shown as a CSV file (opens in Excel)','تنزيل الصفوف المعروضة كملف CSV (يُفتح في Excel)')}" style="padding:8px 14px;border:1px solid #BFD3E6;background:#EEF5FB;color:#1A5FAB;border-radius:7px;font-size:12px;font-weight:700;cursor:pointer">${t('Export this list (CSV)','تصدير هذه القائمة (CSV)')}</button></div>`;
 // ---- summary strip for the rows shown
 const r=tRate(list), V=tValue(list,TF.bigx), nb=list.filter(b=>b.nbid!=null), need=list.filter(tNeeds), n90=need.filter(b=>tDaysPast(b)>90).length;
 const strip=`<div class="kstrip tstrip">
   ${kc(list.length,t('Tenders shown','المنافسات المعروضة'),t('of '+BA.bidlist.length,'من '+BA.bidlist.length))}
   ${kc(r.n,t('With a result','لها نتيجة'),t(r.w+' won · '+(r.n-r.w)+' lost',r.w+' فوز · '+(r.n-r.w)+' خسارة'))}
   ${kc(r.ci?r.p+'%':'—',t('Win rate','نسبة الفوز'),r.ci?t('likely '+r.ci[0]+'–'+r.ci[1]+'%','على الأرجح '+r.ci[0]+'–'+r.ci[1]+'%'):t(r.n?'too few results ('+r.n+')':'no results','نتائج أقل من الكافي ('+r.n+')'))}
   ${kc('SAR '+fmtM(V.total),t('Tracked value (indicative)','القيمة المتتبَّعة (تقريبية)'),t(V.n+' of '+list.length+' have a value'+(V.dropped?' · very large left out':''),V.n+' من '+list.length+' لها قيمة'+(V.dropped?' · دون الكبيرة جداً':'')))}
   ${kc(nb.length?tMed(nb.map(b=>b.nbid)):'—',t('Typical bidders','المتقدمون عادةً'),t('median of '+nb.length+' with a count','الوسيط من '+nb.length+' لها عدد'))}
   ${kc(need.length,t('Needs a result','بانتظار نتيجة'),n90?t(n90+' over 90 days',n90+' تجاوزت 90 يوماً'):t('submitted, past deadline','مقدَّمة وتجاوزت الموعد'),need.length?'r':'')}
 </div>`;
 // ---- what this view says (live sentences)
const ls=tLossSplit(list), tc=tTopClient(list), lag=tAwardLag(list);
 const S=[];
 if(r.n)S.push(t('EH won ','فاز EH ب')+'<b>'+tRateTxt(r)+'</b>'+(r.nobid.length?t(' — includes '+r.nobid.map(b=>b.year+'-'+b.sn).join(', ')+', counted as lost although EH did not submit; correct it in the tracker',' — يشمل '+r.nobid.map(b=>b.year+'-'+b.sn).join('، ')+' المحسوبة خسارة رغم عدم التقديم؛ صحّحها في الملف'):'')+'.');
 const KL=list.filter(b=>YR_SUBD[b.year]), uk=tUnknownYrs(list);
 if(TF.flag!='needs'&&KL.some(tSub)){const sb=KL.filter(tSub), ns=KL.filter(b=>b.outcome=='Pending'&&!tSub(b)&&!tAhead(b)).length, op=KL.filter(b=>b.outcome=='Pending'&&!tSub(b)&&tAhead(b)).length;
  S.push(t('Of the <b>'+sb.length+'</b> bids EH submitted, '+sb.filter(b=>b.outcome=='Won').length+' were won, '+sb.filter(b=>b.outcome=='Lost').length+' lost, '+sb.filter(b=>b.outcome=='Pending').length+' are awaiting a result and '+sb.filter(b=>b.outcome=='Cancelled').length+' were cancelled.'+(ns?' '+ns+' more pending tenders were not submitted, so no result will come for them.':'')+(op?' '+op+' are still open and not yet submitted.':'')+(uk.length?' (No submission records for '+uk.join(', ')+'.)':''),
   'من <b>'+sb.length+'</b> عرضاً قدّمه EH: '+sb.filter(b=>b.outcome=='Won').length+' فوز، و'+sb.filter(b=>b.outcome=='Lost').length+' خسارة، و'+sb.filter(b=>b.outcome=='Pending').length+' بانتظار النتيجة، و'+sb.filter(b=>b.outcome=='Cancelled').length+' ملغاة.'+(ns?' و'+ns+' منافسة معلّقة أخرى لم تُقدَّم، فلن تأتي لها نتيجة.':'')+(op?' و'+op+' ما زالت مفتوحة ولم تُقدَّم بعد.':'')+(uk.length?' (لا سجلات تقديم لعام '+uk.join('، ')+'.)':'')));}
 if(need.length)S.push(t('<b>'+need.length+'</b> submitted bids are past their deadline with no result recorded'+(n90?'; <b>'+n90+'</b> of them by more than 90 days':'')+(lag.n>=10?'. Results usually arrive about '+lag.m+' days after the deadline (median of '+lag.n+')':'')+'. Use <i>Show → Needs a result</i> to list them.',
   '<b>'+need.length+'</b> عرضاً مقدَّماً تجاوز موعده دون نتيجة مسجّلة'+(n90?'؛ منها <b>'+n90+'</b> تجاوزت 90 يوماً':'')+(lag.n>=10?'. تصل النتائج عادةً بعد نحو '+lag.m+' يوماً من الموعد (الوسيط من '+lag.n+')':'')+'. استخدم <i>عرض ← بانتظار نتيجة</i> لإظهارها.'));
 if(ls.n)S.push(t('Of '+ls.n+' lost bids, '+ls.price+' were lost on price and '+ls.tech+' on technical rejection; '+ls.other+' give no clear reason.','من '+ls.n+' عرضاً خاسراً، '+ls.price+' بسبب السعر و'+ls.tech+' برفض فني؛ و'+ls.other+' بلا سبب واضح.'));
 if(tc)S.push(t('<bdi>'+esc(tc.name)+'</bdi> is '+tc.ntend+' of the '+tc.nall+' tenders shown but '+tc.share+'% of won value; the largest single win ('+tc.big+') alone is '+tc.bigshare+'%.','<bdi>'+esc(tc.name)+'</bdi> يمثّل '+tc.ntend+' من '+tc.nall+' منافسة معروضة لكن '+tc.share+'% من قيمة ما فاز به EH؛ وأكبر فوز منفرد ('+tc.big+') وحده '+tc.bigshare+'%.'));
 const says=S.length?`<div class="card tsays"><h3>${t('What this view says','ما تقوله هذه القائمة')}</h3><ul>${S.map(x=>'<li>'+x+'</li>').join('')}</ul>
   <div class="tnote" style="margin-top:6px">${t('Values are indicative: on lost tenders with a named winner the tracker holds the winner\'s price, so those are left out of totals; some values include VAT. ','القيم تقريبية: في المنافسات الخاسرة ذات الفائز المسمّى يحمل الملف سعر الفائز، فتُستبعد من المجاميع؛ وبعض القيم تشمل الضريبة. ')}
   ${V.big.size?`<label style="cursor:pointer;white-space:nowrap"><input type="checkbox" ${TF.bigx?'checked':''} onchange="TF.bigx=this.checked;renderTenders()"> ${t('Leave very large tenders ('+[...V.big].join(', ')+') out of the value total','استبعاد المنافسات الكبيرة جداً ('+[...V.big].join('، ')+') من مجموع القيمة')}</label>`:''}</div></div>`:'';
 const rows=list.map(b=>`<tr data-bk="${b.year}-${b.sn}">
   <td><b>#${b.sn}</b>${ntfChip(b.year+"-"+b.sn)}<div style="font-size:9.5px;color:#5F7078">${b.year}</div>${tChips(b)}</td>
   <td style="font-size:10.5px;color:#7B8A92;white-space:nowrap">${b.date||'—'}</td>
   <td style="font-size:10.5px;color:#3A4A52">${dlCell(b)}</td>
   <td>${subCell(b)}</td>
   <td style="max-width:280px"><div dir="auto" style="font-size:11.5px;line-height:1.35">${esc(b.title)||'<span style="color:#bbb">—</span>'}</div></td>
   <td style="max-width:150px"><div dir="auto" style="font-size:11px;color:#3A4A52">${esc(b.client)||'—'}</div></td>
   <td style="font-size:11px;white-space:nowrap">${esc(dv(DPLAT,platN(b.platform)))}</td>
   <td style="font-size:10.5px;color:#6B7C86">${b.svc?dv(DSVC,b.svc):'—'}</td>
   <td style="text-align:right;font-size:11px;white-space:nowrap">${b.value?(tWinPrice(b)?`<span style="color:#8A99A3">${fmtSAR(b.value)}</span><div class="tnote">${t('winner\'s price','سعر الفائز')}</div>`:fmtSAR(b.value)+(V.big.has(b.year+'-'+b.sn)?`<div class="tnote" style="color:#8A5A12;font-weight:700">${t('very large','كبيرة جداً')}</div>`:'')):'—'}</td>
   <td style="text-align:center">${b.nbid!=null?b.nbid:'—'}</td>
   <td><span class="tag" style="background:${OC[b.outcome]}">${t(b.outcome.toUpperCase(),DOUT[b.outcome]||b.outcome)}</span>${b.lossreason&&b.outcome!='Won'?`<div dir="auto" style="font-size:9.5px;color:${b.outcome=='Cancelled'?'#77868F':'#A03A36'};margin-top:3px;max-width:175px;line-height:1.35">${esc(b.lossreason)}</div>`:''}</td>
   <td style="max-width:130px"><div dir="auto" style="font-size:10.5px;color:#6B7C86">${b.winner=='EH'?'<b style="color:#2E7D46">EH</b>':(esc(b.winner)||'—')}</div></td>
 </tr>`).join('');
 $('s-tenders').innerHTML=
 `<div class="sech">${t('All tracked tenders','جميع المنافسات المتتبَّعة')}</div><div class="secsub">${t('Every real tender in the workbooks (empty placeholder rows excluded). Filter by any column or search; the figures and sentences below follow the filters. ','كل منافسة فعلية في الملفات (بلا صفوف فارغة). صفِّ بأي عمود أو ابحث؛ الأرقام والجمل أدناه تتبع التصفية. ')}<b>${list.length}</b>${t(' of '+BA.bidlist.length+' shown.',' من '+BA.bidlist.length+' معروضة.')}</div>
 ${ctrls}
 ${TF.only?`<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:-4px 0 12px;background:#FFF8EC;border:1px solid #EAD9B0;border-radius:9px;padding:8px 13px;font-size:12px;color:#5C4A14"><b>${t('Showing the '+TF.only.size+' tender(s) flagged since '+(NTF.when||'your last visit'),'عرض '+TF.only.size+' منافسة/منافسات مُعلَّمة منذ '+(NTF.when||'آخر زيارة'))}</b><button onclick="TF.only=null;renderTenders()" style="margin-inline-start:auto;border:1px solid #D9C48E;background:#fff;color:#8A6D2E;border-radius:7px;padding:5px 11px;font-size:11.5px;font-weight:700;cursor:pointer">${t('Show all tenders','عرض كل المنافسات')}</button></div>`:''}
 ${strip}
 ${says}
 <div class="card" style="padding:6px 10px">
 <table class="t"><thead><tr><th>${t('Ref','المرجع')}</th><th>${t('Launched','الطرح')}</th><th>${t('Submission deadline','آجال تقديم العروض')}</th><th>${t('EH submitted','تاريخ تقديم EH')}</th><th>${t('Title','العنوان')}</th><th>${t('Client','العميل')}</th><th>${t('Platform','المنصة')}</th><th>${t('Service','الخدمة')}</th><th style="text-align:right">${t('Value (SAR, indicative)','القيمة (ريال، تقريبية)')}</th><th style="text-align:center">${t('Bidders','المتقدمون')}</th><th>${t('Outcome','النتيجة')}</th><th>${t('Winner','الفائز')}</th></tr></thead>
 <tbody>${rows||'<tr><td colspan="12" style="text-align:center;padding:30px;color:#5F7078">'+t('No tenders match these filters.','لا توجد منافسات مطابقة لهذه الفلاتر.')+'</td></tr>'}</tbody></table></div>`;
}
// ---- submission timing (shown on the Bid Turnaround tab)
function rTiming(){const el=$('s-funnel');if(!el)return;
 const R=(BA.bidlist||[]).filter(b=>b.subdate&&b.deadline&&!b.deadline_stale&&!b.sub_conflict&&!(b.subgap&&b.subgap.days<0)).map(b=>dDays(b.subdate,b.deadline)).filter(d=>d>=0);
 if(R.length<10)return;
 const bk=[[t('Deadline day','يوم الموعد'),d=>d==0],[t('1 day before','قبل يوم'),d=>d==1],[t('2–3 days before','قبل 2–3 أيام'),d=>d>=2&&d<=3],[t('4–7 days before','قبل 4–7 أيام'),d=>d>=4&&d<=7],[t('More than 7 days before','قبل أكثر من 7 أيام'),d=>d>7]].map(([l,f])=>({l:l,v:R.filter(f).length}));
 const close=R.filter(d=>d<=1).length, stale=(BA.bidlist||[]).filter(b=>b.deadline_stale).length;
 el.insertAdjacentHTML('beforeend',`<div class="card"><h3>${t('How close to the deadline EH submits','مدى قرب تقديم EH من الموعد النهائي')}</h3><div class="note">${t('EH submits a median of '+tMed(R)+(tMed(R)==1?' day':' days')+' before the deadline; '+close+' of '+R.length+' bids went in on the deadline day or the day before. Bids where the client extended the deadline without the tracker being updated are left out ('+stale+'). This shows timing only — it says nothing about whether late submissions win or lose.','يقدّم EH بوسيط '+tMed(R)+' يوم قبل الموعد؛ '+close+' من '+R.length+' عرضاً قُدّمت يوم الموعد أو قبله بيوم. تُستبعد العروض التي مدّد العميل موعدها دون تحديث الملف ('+stale+'). يُظهر هذا التوقيت فقط ولا يقول شيئاً عن أثره في الفوز أو الخسارة.')}</div>
 ${hbar(bk,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+t(' bids',' عرض'),color:d=>d===bk[0]||d===bk[1]?C.orange:C.blue,maxlab:30,rh:40})}</div>`);}
(function(){try{document.head.insertAdjacentHTML('beforeend','<style>.tchip{display:inline-block;font-size:9.5px;font-weight:700;padding:1px 6px;border-radius:9px;margin:3px 3px 0 0;line-height:1.4;max-width:170px;white-space:normal}.tc-r{background:#FBE9E8;color:#A03A36}.tc-a{background:#FFF3DF;color:#8A5A12}.tc-g{background:#EEF2F4;color:#5F7078}.tnote{font-size:9.5px;color:#77868F;line-height:1.35;margin-top:2px;white-space:normal}.tsays ul{margin:6px 0 0;padding-inline-start:18px;font-size:12.5px;line-height:1.6;color:#3A4A52}.tsays li{margin-bottom:3px}.tstrip{margin-bottom:12px}body.dark .tc-r{background:#3A2223;color:#F2B8B5}body.dark .tc-a{background:#3A3020;color:#F0D19A}body.dark .tc-g{background:#24303A;color:#B7C5CE}body.dark .tsays ul{color:#DCE5EA}body.dark .tnote{color:#9FB3BE}body.dark .tctl{background:#151C21!important;border-color:#2C3A43!important}</style>');}catch(e){}})();
// ---- live text for two Notes & Limits cards (replace typed text, 11 Oct 2026)
function tPipeNote(){const Lst=(BA.bidlist||[]).filter(b=>YR_SUBD[b.year]);const uk=tUnknownYrs(BA.bidlist||[]);if(!Lst.length)return t('The tracker has no submission records yet, so pending tenders cannot be split into submitted and not submitted.','لا سجلات تقديم في الملف بعد، فيتعذّر فصل المعلّقة إلى مقدَّمة وغير مقدَّمة.');const P=Lst.filter(b=>b.outcome=='Pending');const s=P.filter(tSub);const need=Lst.filter(tNeeds);const n90=need.filter(b=>tDaysPast(b)>90).length;const lag=tAwardLag(Lst);
 return t('Of the '+P.length+' tenders still marked pending, EH submitted '+s.length+'. The other '+(P.length-s.length)+' were declined by the bid committee, have no submission recorded or are not yet due, so most will never produce a result. Of the submitted ones, '+need.length+' are past their deadline with no result recorded ('+n90+' by more than 90 days) — the "Needs a result" view on All Tenders lists them for chasing.'+(lag.n>=10?' Results usually arrive about '+lag.m+' days after the deadline (median of '+lag.n+' tenders with an award date).':'')+' Open value counts only what EH actually offered.'+(uk.length?' '+uk.join(', ')+' has no submission records, so it is left out of these counts.':''),
  'من '+P.length+' منافسة ما زالت معلّقة، قدّم EH عروضاً في '+s.length+'. أما الـ'+(P.length-s.length)+' الأخرى فرفضتها لجنة المنافسات أو لا تقديم مسجّل لها أو لم يحن موعدها، فمعظمها لن تأتي له نتيجة. ومن المقدَّمة، '+need.length+' تجاوزت موعدها دون نتيجة مسجّلة ('+n90+' تجاوزت 90 يوماً) — وتعرضها قائمة «بانتظار نتيجة» في «جميع المنافسات» للمتابعة.'+(lag.n>=10?' تصل النتائج عادةً بعد نحو '+lag.m+' يوماً من الموعد (الوسيط من '+lag.n+' منافسة لها تاريخ ترسية).':'')+' والقيمة المفتوحة تحسب ما عرضه EH فعلاً فقط.'+(uk.length?' لا سجلات تقديم لعام '+uk.join('، ')+'، فاستُبعد من هذه الأعداد.':''));}
function tYearNote(){const Lst=BAD.both.bidlist||[];const ys=[...new Set(Lst.map(b=>b.year))].sort();
 const per=ys.map(y=>{const A=Lst.filter(b=>b.year==y);return {y:y,n:A.length,r:A.filter(b=>b.outcome=='Won'||b.outcome=='Lost').length};});
 const lst=per.map(p=>p.r+t(' of ',' من ')+p.n+t(' in ',' في ')+p.y).join(t(' and ',' و'));
 return t('Both years are mostly without a recorded result: '+lst+' have one. The current year is still running and outcomes lag the deadline by weeks to months, so recent months look emptier than they will. '+tTrend(),'معظم منافسات العامين بلا نتيجة مسجّلة: '+lst+' لها نتيجة. والعام الحالي ما زال جارياً وتتأخّر النتائج عن الموعد أسابيع إلى أشهر، فتبدو الأشهر الأخيرة أقل مما ستكون. '+tTrend());}
'''

# ---------------- app.js
HDR = "// ===================== ALL TENDERS (list view) =====================\n"
rep_re('app', re.escape(HDR) + r".*?(?=// ===================== NOTES & LIMITATIONS =====================\n)",
       lambda m: HDR + BLOCK + "\n", 'feature', 'All Tenders rebuilt with live analytics, filters, checks and export')
rep('app', "${t('Tender volume held up but win rate fell sharply — the central competitive concern.','صمد حجم المنافسات لكن نسبة الفوز انخفضت بحدّة — وهو الشاغل التنافسي الأبرز.')}",
    "${tTrend()}", 'fix', 'Overview: typed "win rate fell sharply" (contradicted by the data) replaced by a live sentence')
rep('app', "${t(' — where EH may be losing, which clients are slipping, where pricing looks exposed — not to settle them with precision. The headline story (declining win rate, high pricing on losses, SEC concentration) is directionally credible; the exact percentages are not. The single highest-leverage fix is upstream: ',' — أين قد يخسر EH، وأي العملاء يتراجعون، وأين يبدو التسعير مكشوفاً — لا لحسمها بدقّة. القصة الرئيسية (تراجع نسبة الفوز، ارتفاع التسعير في الخسائر، تركّز SEC) موثوقة توجيهياً؛ أما النسب الدقيقة فلا. وأعلى إصلاح أثراً يقع في المنبع: ')}",
    "${t(' — where EH may be losing, which clients are slipping, where pricing looks exposed — not to settle them with precision. ',' — أين قد يخسر EH، وأي العملاء يتراجعون، وأين يبدو التسعير مكشوفاً — لا لحسمها بدقّة. ')}${tHeadline()}${t('Treat the exact percentages as indicative. The single highest-leverage fix is upstream: ','تعامل مع النسب الدقيقة كمؤشرات. وأعلى إصلاح أثراً يقع في المنبع: ')}",
    'fix', 'Notes & Limits: typed headline story replaced by live figures')
rep_re('app', r"\[t\('Open pipeline is an upper bound'.*?'\)\],\n",
       lambda m: "[t('Open pipeline is mostly not live','معظم المنافسات المفتوحة ليست قائمة فعلاً'),tPipeNote()],\n",
       'fix', 'Notes & Limits: open-pipeline card built from the submission match')
rep_re('app', r"\[t\('2025 vs 2026 not comparable'.*?'\)\],\n",
       lambda m: "[t('Year-on-year comparisons are fragile','المقارنات السنوية هشّة'),tYearNote()],\n",
       'fix', 'Notes & Limits: "near-complete 2025" (untrue) replaced by live counts')
rep('app', "rFunnel();renderTenders();", "rFunnel();rTiming();renderTenders();", 'feature', 'render the submission-timing card')

# ---------------- bid_analytics2.py
rep('analytics', "            wgaps.append(round(100*(ehp-award)/award,1))\n            if rank==1: cheapest_cnt+=1\n",
    "            wgaps.append(round(100*(ehp-award)/award,1))\n        if has_full and rank==1: cheapest_cnt+=1   # 11 Oct 2026: count every fully priced tender where EH was lowest\n",
    'fix', '"EH was cheapest" counted only lost tenders, so it always read 0')
rep('analytics', "    # ---------- WATCHLIST (self-contained, regenerated each run) ----------\n",
    "    def _wilson(k,n,z=1.959964):\n"
    "        if not n: return None\n"
    "        p=k/n; den=1+z*z/n; c=(p+z*z/(2*n))/den; h=z*((p*(1-p)/n+z*z/(4*n*n))**.5)/den\n"
    "        return (c-h, c+h)\n"
    "    def _wr_clear(a,b):\n"
    "        # a real change only when both years have 10+ results and the likely ranges do not overlap\n"
    "        if (a.get('awarded') or 0)<10 or (b.get('awarded') or 0)<10: return False\n"
    "        x=_wilson(a['eh_won'],a['awarded']); y=_wilson(b['eh_won'],b['awarded'])\n"
    "        return x[1]<y[0] or y[1]<x[0]\n"
    "    # ---------- WATCHLIST (self-contained, regenerated each run) ----------\n",
    'fix', 'win-rate helper for the watch item')
rep('analytics', "traj[2026]['win_rate']<traj[2025]['win_rate']:\n",
    "traj[2026]['win_rate']<traj[2025]['win_rate'] and _wr_clear(traj[2025],traj[2026]):\n",
    'fix', '"Win-rate decline" only when the fall is clear, not noise')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for alias, path in (('app', J), ('analytics', A)):
    open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_tenders_analytics'), 'All Tenders — live analytics, honest sentences and data checks')
print('patched: app.js, bid_analytics2.py')
