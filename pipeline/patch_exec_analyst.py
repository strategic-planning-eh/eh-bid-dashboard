"""patch_exec_analyst.py — Executive Summary, analyst review cards (1 Nov 2026, Stage 2 of claude/map_analyst_report_2026-11.md).

Adds to the Bid & Tender Executive Summary, computed from the live tracker on every rebuild:
  E-12 Results still unknown   (KPI, first card — governs how every rate on the page is read)
  opening lines                (three sentences built from the live numbers, each tied to a card)
  E-1  Where we lose on price  (below-EH prices by service line × buyer type)
  E-5  Price gap when we lose  (median gap to the lowest bid, by year)
  E-10 Buyers we keep bidding to (issuer table with "no result" as its own column)
  E-2  How wide the field is   (Pareto of encounters, rivals needed for half)
and the order the report proposed. bid_analytics2.py tags every tender with a buyer type (government / company) by name.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table, write_files

A = os.path.join(HERE, 'app.js'); load(A, 'app')
P = os.path.join(HERE, 'bid_analytics2.py'); load(P, 'ana')
if 'exUnknown' in FILES['app']: sys.exit('Already applied.')

# ---- 1. bid_analytics2.py: buyer type on every bidlist row
ok1 = rep('ana', "    bidlist=[]\n    for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):",
"""    import re as _re
    _GOV=_re.compile(r'هيئة|وزارة|أمانة|أمانه|المركز الوطني|مؤسسة عامة|المؤسسة العام|بلدية|جامعة|كلية|حرس|قوات|المديرية|تجمع|مستشف|مدينة الملك|محمية|صندوق البيئة|Authority|Ministry|Nat\\. Center|National Center|Municipality|University|College|Military|Forces|Organization|Reserve|GAMI|SWCC|NCVC|NCEC|TVTC|ZATCA|Zakat|Environment Fund', _re.I)   # 1 Nov 2026, Youssef: state-owned companies (SEC, SIRC, NWC, ACWA…) are companies; ministries, authorities, universities, أمانات, هيئات, national centres, public corporations, hospitals and health clusters are government
    def _buyer(name): return 'government' if _GOV.search(str(name or '')) else 'company'
    bidlist=[]
    for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):""", 'exec-analyst', 'bid_analytics2: buyer type (government / company) tagged on each tender by issuer name')
ok2 = rep('ana', "            svc=SVCN2.get(b['svcdept'],''), dur=round(b['dur'],1) if b['dur'] else None,",
"            svc=SVCN2.get(b['svcdept'],''), buyer=_buyer(b['client']), dur=round(b['dur'],1) if b['dur'] else None,", 'exec-analyst', 'bid_analytics2: buyer field written to bidlist')

# ---- 2. app.js: new cards
NEWJS = r"""
// ---- analyst review cards (1 Nov 2026): E-12, opening lines, E-1, E-5, E-10, E-2 — see pipeline/analysis/out/map_analyst_report_2026-11.md
function exMedian(a){const s=a.slice().sort((x,y)=>x-y);return s.length?(s.length%2?s[s.length>>1]:(s[s.length/2-1]+s[s.length/2])/2):null;}
function exPct(v){return v==null?'—':Math.round(v)+'%';}
function exBuyer(b){return (b&&b.buyer)||'company';}
function exBuyerL(k){return k==='government'?t('government buyers','جهات حكومية'):t('companies','شركات');}
// E-12 — results still unknown
function exUnknown(d){
 const n=d.total, un=n-d.decided-(d.lost.length?0:0); const noRes=(BA.bidlist||[]).filter(b=>b.outcome==='Pending').length, canc=(BA.bidlist||[]).filter(b=>b.outcome==='Cancelled').length;
 return kc(n?Math.round(100*noRes/n)+'%':'—',t('Results still unknown','نتائج غير مسجّلة'),`${noRes} ${t('of','من')} ${n} ${t('tenders have no result recorded','منافسة بلا نتيجة مسجّلة')} · ${t('every rate here is computed on','كل نسبة هنا محسوبة على')} ${d.decided} ${t('decided','محسومة')} · <a onclick="exGo('tenders',{outcome:'Pending',year:'all',platform:'all',svc:'all',q:''})">${t('open the list','افتح القائمة')} →</a>`, noRes/n>0.5?'r':'');
}
// E-1 — where we lose on price: below-EH prices by service line × buyer type
function exLoseRows(B){
 const bl=new Map((B.bidlist||[]).map(b=>[b.year+'-'+b.sn,b])); const out={};
 (B.pricing&&B.pricing.rows||[]).filter(r=>r.eh&&r.n_priced>1).forEach(r=>{const b=bl.get(r.year+'-'+r.sn); const svc=(b&&b.svc)||''; const by=exBuyer(b);
  r.bidders.forEach(x=>{ if(!x.price||x.eh||/Environmental Horizons/.test(x.name))return; if(x.price<r.eh){const k=svc||'(unset)'; out[k]=out[k]||{government:0,company:0}; out[k][by]++;} });});
 return Object.keys(out).map(k=>({svc:k,government:out[k].government,company:out[k].company,total:out[k].government+out[k].company})).sort((a,b)=>b.total-a.total);
}
function exLosePrice(B){
 const rows=exLoseRows(B), n=(B.pricing&&B.pricing.rows||[]).filter(r=>r.eh&&r.n_priced>1).length, tot=rows.reduce((s,r)=>s+r.total,0);
 if(!rows.length)return `<div class="card exc"><div class="exh"><h3>${t('Where we lose on price','أين نخسر على السعر')}</h3></div><div class="note">${t('No tender with two or more disclosed prices yet.','لا توجد منافسة فيها سعران مُفصَحان بعد.')}</div></div>`;
 const W=620,rh=36,H=56+rows.length*rh+8,x0=200,iw=W-x0-130,max=Math.max(...rows.map(r=>r.total),1),m=exRTL(W);
 let s=`<svg id="ex-lose" viewBox="0 0 ${W} ${H}" class="ch exsvg">${exSvgHead(W,t('Below-EH prices by service line and buyer','الأسعار الأدنى من EH حسب خط الخدمة والجهة'),t('one count per rival price below EH · dark = government buyers · light = companies','عدّ واحد لكل سعر منافس دون EH · الداكن = جهات حكومية · الفاتح = شركات'))}`;
 rows.forEach((r,i)=>{const y=52+i*rh,wg=r.government/max*iw,wc=r.company/max*iw;
  s+=`<text x="${m.X(x0-10)}" y="${y+19}" text-anchor="${m.A('end')}" class="chl">${esc(r.svc==='(unset)'?t('Unclassified','غير مصنّف'):dv(DSVC,r.svc))}</text><rect x="${m.B(x0,wg).toFixed(1)}" y="${y+5}" width="${Math.max(wg,0).toFixed(1)}" height="22" rx="3" fill="${EXC.lost}"><title>${esc(r.svc)} · ${r.government} ${esc(exBuyerL('government'))}</title></rect><rect x="${m.B(x0+wg,wc).toFixed(1)}" y="${y+5}" width="${Math.max(wc,0).toFixed(1)}" height="22" rx="3" fill="${EXC.lost}" fill-opacity=".4"><title>${esc(r.svc)} · ${r.company} ${esc(exBuyerL('company'))}</title></rect><text x="${m.X(x0+wg+wc+8)}" y="${y+21}" text-anchor="${m.A('start')}" class="chv" direction="ltr">${r.total}</text><text x="${m.X(x0+wg+wc+8+String(r.total).length*9+8)}" y="${y+21}" text-anchor="${m.A('start')}" class="chs" direction="ltr">${r.government} / ${r.company}</text>`;});
 s+='</svg>';
 const top=rows[0]; const share=tot?Math.round(100*top.total/tot):0; const gov=rows.reduce((a,r)=>a+r.government,0);
 return `<div class="card exc"><div class="exh"><h3>${t('Where we lose on price','أين نخسر على السعر')}</h3>${exBtn('ex-lose','where_we_lose_on_price')}</div>
  <div class="excov">${t(`${share}% of the ${tot} prices recorded below EH are in ${top.svc==='(unset)'?'unclassified tenders':dv(DSVC,top.svc)}; ${gov} of ${tot} come from government buyers.`,`${share}% من ${tot} سعراً مسجّلاً دون EH في ${top.svc==='(unset)'?'منافسات غير مصنّفة':dv(DSVC,top.svc)}؛ ${gov} من ${tot} من جهات حكومية.`)}</div>${s}
  <div class="exfoot">${t('Based on','مبني على')} ${n} ${t('priced tenders — only tenders where EH\'s price and at least one rival price are both known. A tender with five rivals below EH counts five times. Buyer type is read from the issuer\'s name.','منافسة مُسعَّرة — فقط المنافسات المعروف فيها سعر EH وسعر منافس واحد على الأقل. المنافسة التي فيها خمسة منافسين دون EH تُعدّ خمس مرات. نوع الجهة مستنتج من اسمها.')}</div></div>`;
}
// E-5 — price gap when we lose: median gap to the lowest bid, by year
function exGapYear(){
 const yrs=['y2025','y2026'].filter(y=>BAD[y]); const data=yrs.map(y=>({y:y.slice(1),g:(BAD[y].pricing&&BAD[y].pricing.rows||[]).filter(r=>r.eh&&r.n_priced>1&&r.gap!=null).map(r=>r.gap)}));
 const all=data.reduce((a,d)=>a.concat(d.g),[]); if(!all.length)return '';
 const W=620,H=200,x0=70,iw=W-x0-30,top=Math.min(Math.max(...all),600),sc=v=>x0+Math.min(v,top)/top*iw,m=exRTL(W);
 let s=`<svg id="ex-gap" viewBox="0 0 ${W} ${H}" class="ch exsvg">${exSvgHead(W,t('How far above the lowest bid EH priced — typical gap by year','كم كان سعر EH فوق أدنى عرض — الفجوة النموذجية حسب العام'),t('each dot is one tender · bar = middle half · line = median · axis capped at 600%','كل نقطة منافسة · الشريط = النصف الأوسط · الخط = الوسيط · المحور يقف عند 600%'))}`;
 [0,100,200,300,400,500,600].filter(v=>v<=top).forEach(v=>{s+=`<line x1="${m.X(sc(v))}" x2="${m.X(sc(v))}" y1="46" y2="${H-20}" stroke="#E3EAE5"/><text x="${m.X(sc(v))}" y="${H-6}" text-anchor="middle" class="chs" direction="ltr">${v}%</text>`;});
 data.forEach((d,i)=>{const y=70+i*55; if(!d.g.length){s+=`<text x="${m.X(x0-8)}" y="${y+5}" text-anchor="${m.A('end')}" class="chl">${d.y}</text><text x="${m.X(x0+6)}" y="${y+5}" text-anchor="${m.A('start')}" class="chs">${esc(t('no priced tender','لا منافسة مُسعَّرة'))}</text>`;return;}
  const sg=d.g.slice().sort((a,b)=>a-b),med=exMedian(sg),q1=sg[Math.floor(sg.length/4)],q3=sg[Math.floor(sg.length*3/4)];
  s+=`<text x="${m.X(x0-8)}" y="${y+5}" text-anchor="${m.A('end')}" class="chl">${d.y}</text><rect x="${m.B(sc(q1),sc(q3)-sc(q1)).toFixed(1)}" y="${y-12}" width="${Math.max(sc(q3)-sc(q1),2).toFixed(1)}" height="24" rx="3" fill="${EXC.lost}" fill-opacity=".18"/>`;
  sg.forEach(v=>{s+=`<circle cx="${m.X(sc(v)).toFixed(1)}" cy="${y}" r="4" fill="${v<=0?EXC.won:EXC.lost}" fill-opacity=".75"><title>${v<=0?esc(t('EH was lowest','EH الأدنى')):Math.round(v)+'% '+esc(t('above lowest','فوق الأدنى'))}</title></circle>`;});
  s+=`<line x1="${m.X(sc(med))}" x2="${m.X(sc(med))}" y1="${y-16}" y2="${y+16}" stroke="${EXC.ink}" stroke-width="2.5"/><text x="${m.X(sc(med)+6)}" y="${y-18}" text-anchor="${m.A('start')}" class="chv" direction="ltr">${t('median','الوسيط')} ${Math.round(med)}% · n=${sg.length}</text>`;});
 s+='</svg>';
 const meds=data.filter(d=>d.g.length).map(d=>[d.y,Math.round(exMedian(d.g))]); const mAll=Math.round(exMedian(all));
 return `<div class="card exc"><div class="exh"><h3>${t('Price gap when we lose','فجوة السعر عند الخسارة')}</h3>${exBtn('ex-gap','price_gap_by_year')}</div>
  <div class="excov">${t(`Typical gap to the lowest bid: ${mAll}% across ${all.length} priced tenders`,`الفجوة النموذجية عن أدنى عرض: ${mAll}% عبر ${all.length} منافسة مُسعَّرة`)}${meds.length>1?' · '+meds.map(x=>x[0]+': '+x[1]+'%').join(' · '):''}</div>${s}
  <div class="exfoot">${t('The median is used, not the average: a few very large gaps would otherwise dominate. Gaps include disqualified low bids where a price was disclosed. 0% = EH was the lowest bidder.','يُستخدم الوسيط لا المتوسط: فجوات قليلة كبيرة جداً كانت ستطغى. تشمل الفجوات العروض المستبعدة إذا أُفصح عن سعرها. 0% = EH الأدنى سعراً.')}</div></div>`;
}
// E-10 — buyers we keep bidding to
function exBuyers(B){
 const bl=B.bidlist||[]; const acc={};
 bl.forEach(b=>{if(!b.client)return;const k=b.client;const a=acc[k]=acc[k]||{client:k,bids:0,won:0,lost:0,none:0,canc:0,value:0};a.bids++;a.value+=b.value||0;if(b.outcome==='Won')a.won++;else if(b.outcome==='Lost')a.lost++;else if(b.outcome==='Cancelled')a.canc++;else a.none++;});
 const rows=Object.values(acc).sort((a,b)=>b.bids-a.bids).slice(0,10);
 const noWin=rows.filter(r=>r.bids>=3&&!r.won);
 const tr=rows.map((r,i)=>`<tr style="cursor:pointer" onclick="exGo('tenders',{outcome:'all',year:'all',platform:'all',svc:'all',q:${JSON.stringify(r.client)}})"><td style="color:#5F7078">${i+1}</td><td><b dir="auto">${esc(r.client)}</b></td><td style="text-align:center">${r.bids}</td><td style="text-align:center">${r.won?`<b class="vt-good">${r.won}</b>`:'<span style="color:#8A99A3">0</span>'}</td><td style="text-align:center">${r.lost?`<b class="vt-bad">${r.lost}</b>`:'<span style="color:#8A99A3">0</span>'}</td><td style="text-align:center;${r.none>=r.bids/2?'font-weight:700;color:#C98A1B':''}">${r.none}</td><td style="text-align:center;color:#8A99A3">${r.canc||0}</td><td style="text-align:end;white-space:nowrap" dir="ltr">${r.value?'SAR '+fmtM(r.value):'—'}</td></tr>`).join('');
 return `<div class="card exc"><div class="exh"><h3>${t('Buyers we keep bidding to','الجهات التي نكرر التقدم لها')}</h3></div>
  <div class="excov">${noWin.length?t(`${noWin.length} buyer${noWin.length>1?'s':''} with three or more bids and no recorded win: ${noWin.map(r=>r.client).join(', ')}.`,`${noWin.length} جهة بثلاثة عروض أو أكثر دون فوز مسجّل: ${noWin.map(r=>r.client).join('، ')}.`):t('Every buyer with three or more bids has at least one recorded win.','لكل جهة بثلاثة عروض أو أكثر فوز مسجّل واحد على الأقل.')}</div>
  <div style="overflow:auto"><table class="ext"><thead><tr><th>#</th><th>${t('Buyer','الجهة')}</th><th>${t('Bids','العروض')}</th><th>${t('Won','فاز EH')}</th><th>${t('Lost','خسر')}</th><th>${t('No result','بلا نتيجة')}</th><th>${t('Cancelled','أُلغيت')}</th><th>${t('Value offered','القيمة المقدَّمة')}</th></tr></thead><tbody>${tr}</tbody></table></div>
  <div class="exfoot">${t('Top ten issuers by number of bids. "No result" is shown on its own and is never folded into "lost" — for most buyers it is the largest column, which is a tracker gap, not a verdict. Click a row to list that buyer\'s tenders.','أكبر عشر جهات بعدد العروض. تُعرض «بلا نتيجة» وحدها ولا تُدمج في «خسر» — وهي لدى أغلب الجهات العمود الأكبر، وهذه فجوة في الملف لا حكم. انقر السطر لعرض منافسات الجهة.')}</div></div>`;
}
// E-2 — how wide the field is (Pareto of encounters)
function exField(B){
 const enc=(B.competitors||[]).map(c=>c.encounters||0).filter(x=>x>0).sort((a,b)=>b-a); const tot=enc.reduce((a,b)=>a+b,0); if(!tot)return '';
 let cum=0,half=null,p10=0,once=enc.filter(x=>x===1).length; const pts=enc.map((v,i)=>{cum+=v;if(half==null&&cum>=tot/2)half=i+1;if(i<10)p10=cum;return cum/tot;});
 const W=wd,H=260,x0=70,y0=44,iw=W-x0-30,ih=H-y0-44,m=exRTL(W),X=i=>x0+(i+1)/enc.length*iw,Y=v=>y0+ih-v*ih;
 let s=`<svg id="ex-field" viewBox="0 0 ${W} ${H}" class="ch exsvg">${exSvgHead(W,t('How wide the field is','اتساع المنافسة'),t('rivals ranked by how often they met EH · line = cumulative share of all encounters','المنافسون مرتَّبون بعدد مواجهاتهم لـ EH · الخط = الحصة التراكمية من كل المواجهات'))}`;
 [0.25,0.5,0.75,1].forEach(v=>{s+=`<line x1="${m.X(x0)}" x2="${m.X(x0+iw)}" y1="${Y(v)}" y2="${Y(v)}" stroke="#E3EAE5"/><text x="${m.X(x0-6)}" y="${Y(v)+4}" text-anchor="${m.A('end')}" class="chs" direction="ltr">${v*100}%</text>`;});
 let path=`M${m.X(x0)},${Y(0)}`; pts.forEach((v,i)=>{path+=` L${m.X(X(i)).toFixed(1)},${Y(v).toFixed(1)}`;});
 s+=`<path d="${path}" fill="none" stroke="${EXC.pend}" stroke-width="2.5"/>`;
 if(half){s+=`<line x1="${m.X(X(half-1))}" x2="${m.X(X(half-1))}" y1="${y0}" y2="${Y(0)}" stroke="${EXC.ink}" stroke-dasharray="4 3"/><text x="${m.X(X(half-1)+6)}" y="${y0+14}" text-anchor="${m.A('start')}" class="chv">${half} ${esc(t('rivals = half of all encounters','منافساً = نصف المواجهات'))}</text>`;}
 s+=`<text x="${m.X(x0)}" y="${H-8}" text-anchor="${m.A('start')}" class="chs">1</text><text x="${m.X(x0+iw)}" y="${H-8}" text-anchor="${m.A('end')}" class="chs" direction="ltr">${enc.length} ${esc(t('rivals','منافساً'))}</text></svg>`;
 return `<div class="card exc"><div class="exh"><h3>${t('How wide the field is','اتساع المنافسة')}</h3>${exBtn('ex-field','field_width')}</div>
  <div class="excov">${t(`${enc.length} rivals, ${tot} encounters: the ten most frequent account for ${Math.round(100*p10/tot)}%, and it takes ${half} rivals to reach half. ${once} were met only once.`,`${enc.length} منافساً و${tot} مواجهة: العشرة الأكثر تكراراً يمثّلون ${Math.round(100*p10/tot)}%، ويلزم ${half} منافساً لبلوغ النصف. ${once} ووجهوا مرة واحدة فقط.`)}</div>${s}
  <div class="exfoot">${t('A steep early curve would mean a few rivals dominate; a straight line means pressure is spread thin. Competitor watch effort should follow the rivals with three or more encounters and the ones that price below EH (see the threat matrix), not the long tail.','منحنى حادّ في البداية يعني أن قلّة تهيمن؛ وخط مستقيم يعني أن الضغط موزَّع. ينبغي أن يتركّز جهد المتابعة على المنافسين بثلاث مواجهات أو أكثر ومن يسعّرون دون EH (انظر مصفوفة التهديد)، لا على الذيل الطويل.')}</div></div>`;
}
// opening lines — three sentences from the live numbers, each tied to a card
function exOpening(B,d){
 const n=d.total, noRes=(B.bidlist||[]).filter(b=>b.outcome==='Pending').length;
 const lose=exLoseRows(B), tot=lose.reduce((a,r)=>a+r.total,0), top=lose[0], gov=lose.reduce((a,r)=>a+r.government,0);
 const gaps=(B.pricing&&B.pricing.rows||[]).filter(r=>r.eh&&r.n_priced>1&&r.gap!=null).map(r=>r.gap), med=gaps.length?Math.round(exMedian(gaps)):null;
 const enc=(B.competitors||[]).map(c=>c.encounters||0).filter(x=>x>0).sort((a,b)=>b-a), et=enc.reduce((a,b)=>a+b,0); let c=0,half=null; enc.forEach((v,i)=>{c+=v;if(half==null&&c>=et/2)half=i+1;});
 const l1=t(`${Math.round(100*noRes/Math.max(n,1))}% of our tenders have no recorded result, so every rate on this page is computed on ${d.decided} decided tenders.`,`${Math.round(100*noRes/Math.max(n,1))}% من منافساتنا بلا نتيجة مسجّلة، فكل نسبة في هذه الصفحة محسوبة على ${d.decided} منافسة محسومة.`);
 const l2=tot&&top?t(`When we lose on price it is in ${top.svc==='(unset)'?'unclassified tenders':dv(DSVC,top.svc)} (${Math.round(100*top.total/tot)}% of below-EH prices) and mostly to government buyers (${gov} of ${tot})${med!=null?`, typically ${med}% above the lowest bid`:''}.`,`عندما نخسر على السعر فذلك في ${top.svc==='(unset)'?'منافسات غير مصنّفة':dv(DSVC,top.svc)} (${Math.round(100*top.total/tot)}% من الأسعار الأدنى من EH) ولدى جهات حكومية غالباً (${gov} من ${tot})${med!=null?`، وعادةً بفارق ${med}% فوق أدنى عرض`:''}.`):'';
 const l3=half?t(`Competition is wide, not deep: ${half} rivals account for half of all ${et} encounters, and the ones that price below us sit in every tier.`,`المنافسة واسعة لا عميقة: ${half} منافساً يمثّلون نصف المواجهات الـ${et}، ومن يسعّرون دوننا موجودون في كل الفئات.`):'';
 return `<div class="excov" style="font-size:13.5px;line-height:1.7"><b>${t('In three sentences','في ثلاث جمل')}</b><br>1. ${esc(l1)}${l2?'<br>2. '+esc(l2):''}${l3?'<br>3. '+esc(l3):''}</div>`;
}
"""
ok3 = rep('app', "// ---- PNG export: clone the SVG", NEWJS.strip('\n') + "\n// ---- PNG export: clone the SVG", 'exec-analyst', 'app.js: analyst review cards — exUnknown, exLosePrice, exGapYear, exBuyers, exField, exOpening')

# ---- 3. rExecutive: new order and the E-12 card first in the strip
OLD_STRIP = """ <div class="kstrip exk">
  ${kc(d.winRate==null?'—':d.winRate+'%',t('Win rate on decided tenders','نسبة الفوز في المنافسات المحسومة')"""
NEW_STRIP = """ ${exOpening(B,d)}
 <div class="kstrip exk">
  ${exUnknown(d)}
  ${kc(d.winRate==null?'—':d.winRate+'%',t('Win rate on decided tenders','نسبة الفوز في المنافسات المحسومة')"""
ok4 = rep('app', OLD_STRIP, NEW_STRIP, 'exec-analyst', 'Executive Summary: opening lines + "Results still unknown" first in the KPI strip')
OLD_ORDER = """ ${exFunnel(d)}
 ${exWhere(B)}
 ${exThreat(B,d)}
 ${exPrice(B,d)}
 ${exDecisions(B,d)}`;"""
NEW_ORDER = """ <div class="grid g2">${exLosePrice(B)}${exGapYear()}</div>
 ${exBuyers(B)}
 ${exFunnel(d)}
 ${exWhere(B)}
 ${exField(B)}
 ${exThreat(B,d)}
 ${exPrice(B,d)}
 ${exDecisions(B,d)}`;"""
ok5 = rep('app', OLD_ORDER, NEW_ORDER, 'exec-analyst', 'Executive Summary: card order per the analyst report (price loss → gap → buyers → funnel → where we win → field width → threat → price position → decisions)')
ok6 = rep('app', "t('Five questions a director needs answered before the Sunday meeting — computed from the bid tracker on every rebuild','خمسة أسئلة يحتاج المدير إجابتها قبل اجتماع الأحد — تُحسب من جدول العطاءات عند كل إعادة بناء')",
          "t('What a director needs to know before the Sunday meeting — computed from the bid tracker on every rebuild','ما يحتاج المدير معرفته قبل اجتماع الأحد — يُحسب من جدول العطاءات عند كل إعادة بناء')", 'exec-analyst', 'Executive Summary subtitle no longer promises exactly five questions')
if not all([ok1, ok2, ok3, ok4, ok5, ok6]): sys.exit('ANCHOR MISMATCH: ' + str([ok1, ok2, ok3, ok4, ok5, ok6]))
open(A, 'w', encoding='utf-8').write(FILES['app']); open(P, 'w', encoding='utf-8').write(FILES['ana'])
write_change_table(os.path.join(HERE, 'change_table_exec_analyst'), 'Change table — Executive Summary analyst cards (1 Nov 2026)'); print('applied')
