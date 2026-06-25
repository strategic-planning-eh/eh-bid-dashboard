const BA=JSON.parse(document.getElementById('BA').textContent);
const $=id=>document.getElementById(id);
const pct=v=>v==null?'—':v+'%';
const wrCol=v=>v==null?C.soft:(v>=50?C.green:v>=30?C.orange:C.red);
const RCAT={'Outside EH scope':'#E8862E','Service not offered (e.g. training)':'#7B6BA8','Brand-locked specification':'#C0504D','Missing licence / qualification':'#2A9D8F','Vendor / partner risk':'#D4A92E','Other / not specified':'#9AABB5'};

// ---------- NAV ----------
const TABS=[['overview','Overview'],['pipeline','Pipeline & Timeline'],['winloss','Win / Loss'],['pricing','Pricing Intelligence'],['competitors','Competitors'],['clients','Clients'],['service','Service & Platform'],['funnel','Bid Turnaround'],['tenders','All Tenders'],['watchlist','Watchlist'],['limitations','Notes & Limits']];
$('nav').innerHTML=TABS.map(([id,l],i)=>`<a id="t-${id}" class="${i==0?'on':''}" onclick="go('${id}')">${l}</a>`).join('');
function go(id){TABS.forEach(([t])=>{$('t-'+t).classList.toggle('on',t==id);$('s-'+t).classList.toggle('on',t==id);});window.scrollTo(0,0);}

// ---------- KPI STRIP ----------
const k=BA.kpi;
function kc(v,l,d,cls){return `<div class="kc"><div class="v ${cls||''}">${v}</div><div class="l">${l}</div>${d?`<div class="d">${d}</div>`:''}</div>`;}
$('kstrip').innerHTML=
 kc(k.total,'Tenders tracked','2024–2026')+
 kc('SAR '+fmtM(k.pipeline),'Pipeline value',k.with_value+' priced')+
 kc(pct(k.win_rate),'Win rate',k.eh_won+'/'+k.awarded+' awarded',k.win_rate>=50?'g':'r')+
 kc(k.competitors,'Competitors faced','head-to-head')+
 kc(k.avg_bidders,'Avg bidders/tender','max '+k.max_bidders)+
 kc(Math.round(100*k.committee_accept/k.committee_total)+'%','Bid selectivity',k.committee_accept+'/'+k.committee_total+' accepted')+
 kc('SAR '+fmtM(k.median_value),'Median tender','typical size');

// ===================== OVERVIEW =====================
(function(){
 const wl=BA.winloss;
 const segs=[{l:'EH won',v:wl.awarded_eh,c:C.green},{l:'Lost (other won)',v:wl.awarded_other,c:C.red},{l:'Not awarded',v:wl.not_awarded,c:C.orange},{l:'Cancelled',v:wl.cancelled,c:C.soft}];
 const t=BA.trajectory;
 const gb=[{l:'2025',bids:t[2025].bids,won:t[2025].eh_won,wr:t[2025].win_rate,val:t[2025].pipeline},{l:'2026',bids:t[2026].bids,won:t[2026].eh_won,wr:t[2026].win_rate,val:t[2026].pipeline}];
 $('s-overview').innerHTML=
 `<div class="sech">Executive overview</div><div class="secsub">Headline performance across the tender pipeline, win/loss outcome, and the year-on-year trajectory.</div>
 <div style="background:#FFF8EC;border:1px solid #F0DDB0;border-left:4px solid #E8862E;border-radius:9px;padding:11px 14px;margin-bottom:16px;font-size:12.5px;color:#5A4A2E">
 <b>Read this dashboard as directional, not definitive.</b> Win-rate and pricing figures rest on a small recorded sample (only a fraction of the 144 tenders have a recorded outcome; 10 have full pricing), and 2026 is a partial year. See the <a onclick="go('limitations')" style="color:#1A5FAB;cursor:pointer;font-weight:600;text-decoration:underline">Notes &amp; Limits</a> tab for the full caveats.</div>
 <div class="grid g2">
   <div class="card"><h3>Outcome of tracked tenders</h3><div class="note">Of ${k.total} tenders, ${k.awarded} have a recorded award decision. The rest are in progress or pending in the tracker.</div>
     <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;justify-content:center">${donut(segs,{center:pct(k.win_rate),csub:'WIN RATE'})}<div>${legend(segs)}</div></div></div>
   <div class="card"><h3>2025 → 2026 trajectory</h3><div class="note">Tender volume held up but win rate fell sharply — the central competitive concern.</div>
     ${cardRow([['Tenders',t[2025].bids+' → '+t[2026].bids,''],['Win rate',pct(t[2025].win_rate)+' → '+pct(t[2026].win_rate),t[2026].win_rate<t[2025].win_rate?'down':''],['Pipeline','SAR '+fmtM(t[2025].pipeline)+' → '+fmtM(t[2026].pipeline),''],['Avg bidders',t[2025].avg_bidders+' → '+t[2026].avg_bidders,'']])}</div>
 </div>`;
})();
function cardRow(items){return '<div class="cardrow">'+items.map(([l,v,f])=>`<div class="metric"><div class="mv" style="${f=='down'?'color:#C0504D':''}">${v}</div><div class="ml">${l}</div></div>`).join('')+'</div>';}

// ===================== PIPELINE & TIMELINE =====================
(function(){
 const vb=BA.value_bands;
 const wl=BA.winloss;
 const statusSeg=[{l:'Awarded — EH',v:wl.awarded_eh,c:C.green},{l:'Awarded — other',v:wl.awarded_other,c:C.red},{l:'Not awarded',v:wl.not_awarded,c:C.orange},{l:'Cancelled',v:wl.cancelled,c:C.soft},{l:'In progress / pending',v:wl.in_progress+wl.no_status,c:C.blue}];
 $('s-pipeline').innerHTML=
 `<div class="sech">Pipeline &amp; timeline</div><div class="secsub">When tenders arrive, how much value is in play, and what stage they're at.</div>
 <div class="card"><h3>Pipeline value launched per month</h3><div class="note">Sum of EH offer/estimated value for tenders launched each month (partial — only ${k.with_value} of ${k.total} tenders carry a value).</div>
   ${barChart(BA.timeline,{val:d=>d.value,lab:d=>d.month.slice(2),fmt:v=>fmtM(v),color:C.green,h:240})}</div>
 <div class="grid g2">
  <div class="card"><h3>Current status of all tenders</h3><div class="note">Live state across the two tracking years.</div>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;justify-content:center">${donut(statusSeg,{center:k.total,csub:'TENDERS'})}<div>${legend(statusSeg)}</div></div></div>
  <div class="card"><h3>Tenders by value band</h3><div class="note">Distribution of tender sizes (where a value is recorded).</div>
    ${barChart(vb,{val:d=>d.count,lab:d=>d.band,fmt:v=>v,color:d=>C.pal[vb.indexOf(d)%C.pal.length],h:210})}
    <table class="t" style="margin-top:12px"><thead><tr><th>Band</th><th>Tenders</th><th>Total value</th><th>EH win rate</th></tr></thead><tbody>
    ${vb.map(v=>`<tr><td><b>${v.band}</b></td><td>${v.count}</td><td>${fmtSAR(v.value)}</td><td style="color:${wrCol(v.awarded?Math.round(100*v.won/v.awarded):null)};font-weight:700">${v.awarded?Math.round(100*v.won/v.awarded)+'%':'—'}</td></tr>`).join('')}</tbody></table></div>
 </div>`;
})();

// ===================== WIN / LOSS =====================
(function(){
 const byDim=(arr,lab)=>arr.filter(x=>x.awarded>0).map(x=>({l:lab(x),v:Math.round(100*x.won/x.awarded),aw:x.awarded,n:x.count}));
 const svc=byDim(BA.service_mix,x=>x.name);
 const plat=byDim(BA.platform_mix,x=>x.name);
 const vb=byDim(BA.value_bands,x=>x.band);
 const bdr=BA.bidder_dist.filter(x=>x.awarded>0).map(x=>({l:x.n+' bidders',v:Math.round(100*x.won/x.awarded),aw:x.awarded}));
 const wl=BA.winloss;
 const segs=[{l:'EH won',v:wl.awarded_eh,c:C.green},{l:'Competitor won',v:wl.awarded_other,c:C.red}];
 $('s-winloss').innerHTML=
 `<div class="sech">Win / loss performance</div><div class="secsub">Where EH converts and where it doesn't. Win rates are over tenders with a recorded outcome — a small but telling sample (${k.awarded} awarded).</div>
 <div class="grid g2">
  <div class="card"><h3>Head-to-head outcome</h3><div class="note">Among awarded tenders, EH vs the field.</div>
   <div style="display:flex;align-items:center;gap:18px;justify-content:center;flex-wrap:wrap">${donut(segs,{center:pct(k.win_rate),csub:'WIN RATE'})}<div>${legend(segs)}</div></div>
   <div style="margin-top:12px;font-size:12px;color:#6B7C86;text-align:center">EH won <b style="color:#2E7D46">${wl.awarded_eh}</b> · lost <b style="color:#C0504D">${wl.awarded_other}</b> of ${k.awarded} decided tenders.</div></div>
  <div class="card"><h3>Win rate by service line</h3><div class="note">Which capabilities convert best.</div>
   ${hbar(svc,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+' awarded)',color:d=>wrCol(d.v),maxlab:34,rh:44})}</div>
 </div>
 <div class="grid g2">
  <div class="card"><h3>Win rate vs competition intensity</h3><div class="note">Does EH win more when fewer rivals bid? Each bar = win rate at that bidder count.</div>
   ${bdr.length?hbar(bdr,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+')',color:d=>wrCol(d.v),rh:40}):'<div class="note">Not enough awarded tenders with bidder counts.</div>'}</div>
  <div class="card"><h3>Win rate by platform</h3><div class="note">Conversion by procurement channel.</div>
   ${plat.length?hbar(plat,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+'%',sub:d=>'('+d.aw+')',color:d=>wrCol(d.v),rh:44}):'<div class="note">Insufficient data.</div>'}</div>
 </div>`;
})();

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
   const oc=r.won==null?'<span style="color:#9AA8B0;font-weight:700">PENDING</span>':(r.won?'<span class="tag" style="background:#2E7D46">EH WON</span>':'<span class="tag" style="background:#C0504D">LOST</span>');
   // full bidder bars (shown when open)
   const bars=r.bidders.map(b=>{
     if(b.dq){return `<div style="display:flex;align-items:center;gap:8px;margin:3px 0;opacity:.6"><div style="width:230px;font-size:10.5px;color:#8A99A3;text-align:right" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(45deg,#EEE,#EEE 4px,#E0E0E0 4px,#E0E0E0 8px);border-radius:3px;max-width:60px"></div><div style="font-size:10px;color:#B23A3A;font-weight:700">DQ — non-compliant</div></div>`;}
     const w=Math.max(b.price/maxp*100,2);
     const col=b.eh?'#1A5FAB':(b.won?'#2E7D46':'#9AABB5');
     const isWin=b.won;
     return `<div style="display:flex;align-items:center;gap:8px;margin:3px 0">
       <div style="width:230px;font-size:10.5px;color:${b.eh?'#1A5FAB':'#3A4A52'};font-weight:${b.eh?'700':'500'};text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" dir="auto">${b.lowest?'\u25bc ':''}${esc(b.name)}</div>
       <div style="flex:1;max-width:${w}%;height:15px;background:${col};border-radius:3px;min-width:3px"></div>
       <div style="font-size:10.5px;color:#1C2B33;font-weight:${b.eh?'700':'500'};white-space:nowrap">${fmtSAR(b.price)}${isWin?' <span style="color:#2E7D46;font-weight:700">\u2605 won</span>':''}</div></div>`;
   }).join('');
   return `<div class="card" style="margin-bottom:10px;padding:0;overflow:hidden">
     <div onclick="togglePx(${i})" style="cursor:pointer;padding:12px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:${open?'#F7FAFC':'#fff'}">
       <div style="min-width:70px"><b style="font-size:13px">#${r.sn}/${String(r.year).slice(2)}</b><div style="font-size:9px;color:#9AA8B0">${r.n} bidders${r.dq_count?' · '+r.dq_count+' DQ':''}</div></div>
       <div style="flex:1;min-width:200px"><div dir="auto" style="font-size:11.5px;color:#1C2B33;font-weight:600;line-height:1.3">${esc(r.title)||'<span style=\'color:#aaa\'>(untitled tender)</span>'}</div><div dir="auto" style="font-size:10px;color:#9AA8B0;margin-top:1px">${esc(r.client)}</div></div>
       <div style="text-align:right"><div style="font-size:9px;color:#9AA8B0;text-transform:uppercase;letter-spacing:.3px">EH bid</div><div style="font-weight:700;font-size:12.5px;color:#1A5FAB">${fmtSAR(r.eh)}</div></div>
       <div style="text-align:center"><div style="font-size:9px;color:#9AA8B0;text-transform:uppercase">Rank</div><div style="font-weight:700;font-size:12.5px">${r.rank}/${r.n}</div></div>
       <div style="text-align:center"><div style="font-size:9px;color:#9AA8B0;text-transform:uppercase">vs Low</div><div style="font-weight:700;font-size:12.5px;color:${gapcol}">${r.gap>0?'+'+r.gap+'%':r.gap+'%'}</div></div>
       <div style="min-width:78px;text-align:center">${oc}</div>
       <div style="font-size:13px;color:#9AA8B0;transform:rotate(${open?'90':'0'}deg);transition:.15s">\u25b8</div>
     </div>
     ${open?`<div style="padding:10px 16px 14px;border-top:1px solid #EEF2F0;background:#FBFCFD">
       <div style="font-size:10.5px;color:#8A99A3;margin-bottom:8px">All ${r.bidders.length} bids, lowest first \u2014 <span style="color:#1A5FAB;font-weight:700">EH in blue</span>, <span style="color:#2E7D46;font-weight:700">\u25bc lowest</span>${r.win_price?', \u2605 = winning bid':''}.</div>
       ${bars}</div>`:''}</div>`;
 }).join('');
 $('s-pricing').innerHTML=
 `<div class="sech">Pricing intelligence</div><div class="secsub">How EH's bid sits against every competitor, drawn from the ${s.tenders} tenders whose detailed bidder-pricing sheets are filled in (${s.total_bidders} individual bids). Click any tender to see all bids and prices.</div>
 <div class="kstrip">
   ${kc(s.cheapest_pct+'%','Tenders EH was cheapest',s.cheapest+' of '+s.tenders,s.cheapest_pct>=40?'g':'r')}
   ${kc(s.avg_percentile+'th','Avg price percentile','1st=cheapest',s.avg_percentile<=40?'g':'r')}
   ${kc((s.median_gap>0?'+':'')+s.median_gap+'%','Median gap to lowest','typical EH vs cheapest',s.median_gap>20?'r':'g')}
   ${kc(s.tenders,'Tenders priced',s.total_bidders+' total bids')}
 </div>
 <div style="display:flex;gap:8px;margin-bottom:12px"><button onclick="pxAll(true)" style="padding:6px 13px;border:1px solid #1A5FAB;background:#1A5FAB;color:#fff;border-radius:7px;font-size:11.5px;font-weight:600;cursor:pointer">Expand all</button><button onclick="pxAll(false)" style="padding:6px 13px;border:1px solid #D5DEE2;background:#fff;color:#6B7C86;border-radius:7px;font-size:11.5px;font-weight:600;cursor:pointer">Collapse all</button></div>
 ${cards}
 <div style="margin-top:14px;font-size:12px;color:#6B7C86;background:#FCF5F4;border:1px solid #F0D9D6;border-radius:8px;padding:11px 13px">
 <b>Read-out:</b> Across ${s.tenders} priced tenders EH was the outright lowest bidder ${s.cheapest_pct}% of the time and sat at the ${s.avg_percentile}th price percentile on average. The median gap to the cheapest bid is ${s.median_gap}% \u2014 EH is often within a hair of the lowest, but a handful of tenders sit far above it, dragging the average up. Price is clearly one lever, but <b>price is not the whole story</b>: Saudi tenders are scored on technical merit, compliance, delivery capability and incumbency too, and the tracker doesn't capture those factors or the stated reason for each loss \u2014 so we can see where EH priced high, but cannot prove price caused a loss. Capturing the technical score and loss reason per tender is what would close that gap.</div>`;
}
renderPricing();

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
 `<div class="sech">Competitive landscape</div><div class="secsub">Every company that has bid against EH, rebuilt directly from the detailed bidder sheets \u2014 ${all.length} distinct competitors across ${BA.pricing.summary.tenders}+ shared tenders.</div>
 <div class="card"><h3>Most frequent competitors (shared tenders with EH)</h3><div class="note">How many tenders each competitor has bid in alongside EH. Red bars are competitors that have actually beaten EH to an award.</div>
   ${hbar(freq,{val:d=>d.encounters,lab:d=>d.name,fmt:v=>v,sub:d=>d.wins?'\u00b7 '+d.wins+' win vs EH':'',color:d=>d.wins?C.red:C.blue,maxlab:40,rh:24})}</div>
 <div class="card"><h3>Competitor scorecard \u2014 head-to-head vs EH</h3>
   <div class="note">Encounters = shared tenders. Undercut = of the tenders where both were priced, the share where the competitor bid below EH. Won = tenders this competitor actually won.</div>
   <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;padding:10px 13px;background:#F4F8F5;border:1px solid #E3EAE5;border-radius:9px">
     <label style="display:flex;align-items:center;gap:7px;cursor:pointer;font-size:12.5px;font-weight:600;color:#3A4A52"><input type="checkbox" ${showOneOff?'checked':''} onchange="toggleOneOff()" style="width:15px;height:15px;cursor:pointer"> Show one-off bidders</label>
     <span style="font-size:11.5px;color:#8A99A3;flex:1;min-width:240px">${showOneOff?`Showing all <b>${all.length}</b> competitors.`:`Showing <b>${recurring.length}</b> recurring competitors. <b>${oneoff.length}</b> one-off bidders are hidden \u2014 a company that bid against EH only once is noise, not a pattern, and isn't a recurring competitive threat. Tick the box to include them.`}</span>
   </div>
 <table class="t"><thead><tr><th>#</th><th>Competitor</th><th>Encounters</th><th>Won vs field</th><th>Times DQ'd</th><th>Undercut EH</th><th>Avg bid</th></tr></thead><tbody>
 ${shown.map((c,i)=>`<tr><td style="color:#9AA8B0">${i+1}</td><td><b dir="auto">${esc(c.name)}</b></td><td>${c.encounters}</td><td>${c.wins?`<b style="color:#C0504D">${c.wins}</b>`:'0'}</td><td>${c.dq||0}</td><td style="color:${c.undercut_pct>=67?'#C0504D':c.undercut_pct>=34?'#E8862E':'#1C2B33'};font-weight:700">${c.undercut_pct==null?'\u2014':c.undercut_pct+'%'}</td><td>${c.avg_price?fmtSAR(c.avg_price):'\u2014'}</td></tr>`).join('')}
 </tbody></table>
 <div style="font-size:11px;color:#9AA8B0;margin-top:10px">Names are taken verbatim from the bidder sheets (mostly Arabic) and grouped by normalized spelling; very close name variants of the same firm may still appear as separate rows.</div></div>`;
}
renderCompetitors();

// ===================== CLIENTS =====================
(function(){
 const cl=BA.clients;
 const byVal=cl.filter(c=>c.value>0).slice(0,12);
 const totVal=cl.reduce((a,c)=>a+c.value,0);
 const top3=cl.slice(0,3).reduce((a,c)=>a+c.value,0);
 const lapsed=cl.filter(c=>c.lapsed).length, fresh=cl.filter(c=>c.isnew).length;
 $('s-clients').innerHTML=
 `<div class="sech">Client intelligence</div><div class="secsub">Who EH bids to, the value each represents, and how the book is shifting between 2025 and 2026.</div>
 <div class="kstrip">
   ${kc(k.clients,'Distinct clients','sending tenders')}
   ${kc(Math.round(100*top3/totVal)+'%','Top-3 concentration','of tracked value',top3/totVal>0.5?'r':'')}
   ${kc(lapsed,'Lapsed clients','2025 only, no 2026','r')}
   ${kc(fresh,'New in 2026','first appeared','g')}
 </div>
 <div class="card"><h3>Top clients by tracked value</h3><div class="note">Sum of EH offer values per client (partial where the tracker isn't filled). SEC dominates the book.</div>
   ${hbar(byVal,{val:d=>d.value,lab:d=>d.name,fmt:v=>'SAR '+fmtM(v),color:d=>C.pal[byVal.indexOf(d)%C.pal.length],maxlab:38,rh:24})}</div>
 <div class="card"><h3>Client value tiering — 2025 vs 2026</h3><div class="note">Per-client split by year, with status. "Lapsed" = active in 2025 but silent in 2026 (re-engagement targets).</div>
 <table class="t"><thead><tr><th>Client</th><th>'25 tenders</th><th>'25 value</th><th>'26 tenders</th><th>'26 value</th><th>EH win</th><th>Status</th></tr></thead><tbody>
 ${cl.slice(0,20).map(c=>`<tr><td><b dir="auto">${esc(c.name)}</b></td><td>${c.bids25||'—'}</td><td>${c.value25?fmtSAR(c.value25):'—'}</td><td>${c.bids26||'—'}</td><td>${c.value26?fmtSAR(c.value26):'—'}</td><td style="color:${wrCol(c.win_rate)};font-weight:700">${c.win_rate==null?'—':c.win_rate+'%'}</td><td>${c.lapsed?'<span style="color:#C0504D">Lapsed</span>':(c.isnew?'<span style="color:#2E7D46">New 2026</span>':'Active')}</td></tr>`).join('')}
 </tbody></table></div>`;
})();

// ===================== SERVICE & PLATFORM =====================
(function(){
 const sm=BA.service_mix, pm=BA.platform_mix, du=BA.duration, ds=BA.dur_stats;
 const smSeg=sm.map((x,i)=>({l:x.name,v:x.count,c:C.pal[i%C.pal.length]}));
 $('s-service').innerHTML=
 `<div class="sech">Service mix &amp; channels</div><div class="secsub">What kind of work EH bids for, through which platforms, and at what project scale.</div>
 <div class="grid g2">
  <div class="card"><h3>Tenders by service line</h3><div class="note">From the assigned technical department (where recorded).</div>
   <div style="display:flex;align-items:center;gap:16px;justify-content:center;flex-wrap:wrap">${donut(smSeg,{center:sm.reduce((a,x)=>a+x.count,0),csub:'TENDERS'})}<div>${legend(smSeg)}</div></div>
   <table class="t" style="margin-top:12px"><thead><tr><th>Service line</th><th>Tenders</th><th>Value</th><th>Win rate</th></tr></thead><tbody>
   ${sm.map(x=>`<tr><td><b>${esc(x.name)}</b></td><td>${x.count}</td><td>${fmtSAR(x.value)}</td><td style="color:${wrCol(x.win_rate)};font-weight:700">${x.win_rate==null?'—':x.win_rate+'%'}</td></tr>`).join('')}</tbody></table></div>
  <div class="card"><h3>Tenders by platform</h3><div class="note">Procurement channels — Etimad (government) dominates.</div>
   ${hbar(pm,{val:d=>d.count,lab:d=>d.name,fmt:v=>v+' tenders',sub:d=>d.win_rate!=null?'· win '+d.win_rate+'%':'',color:d=>C.pal[pm.indexOf(d)%C.pal.length],maxlab:26,rh:46})}</div>
 </div>
 <div class="card"><h3>Project duration distribution</h3><div class="note">Contract length of tenders (months), where recorded. Median ${ds.median} months · mean ${ds.mean} · longest ${ds.max}.</div>
   ${barChart(du,{val:d=>d.count,lab:d=>d.band,fmt:v=>v,color:C.purple,h:200})}</div>`;
})();

// ===================== TURNAROUND / DECISION DURATION =====================
(function(){
 const t=BA.turnaround, f=BA.funnel, com=BA.committee, k2=BA.kpi;
 // categorize the decision/review window into clear named buckets
 const LBL={'≤7 days':'Under 1 week','8–14 days':'1 – 2 weeks','15–30 days':'2 – 4 weeks','31–45 days':'4 – 6 weeks','46+ days':'Over 6 weeks'};
 const cats=t.bands.map((b,i)=>({l:LBL[b.band]||b.band, v:b.count, i}));
 const comSeg=[{l:'Accepted (decided to bid)',v:com.accept,c:C.green},{l:'Rejected (decided to pass)',v:com.reject,c:C.red}];
 const guarFmt='SAR '+fmtM(k2.total_guarantee);
 $('s-funnel').innerHTML=
 `<div class="sech">Decision &amp; review duration</div><div class="secsub">How long the full stakeholder review runs on each tender \u2014 the elapsed time from the tender being launched to the submission deadline, the window in which BD, the CEO, technical, PM and the bid committee must all weigh in and decide.</div>
 <div class="kstrip">
   ${kc(t.mean+' days','Average review duration','launch \u2192 deadline')}
   ${kc(t.median+' days','Median review duration','typical tender')}
   ${kc(t.minv+'\u2013'+t.maxv,'Range (days)','fastest \u2192 slowest')}
   ${kc(t.n,'Tenders measured','with both dates')}
 </div>
 <div class="card"><h3>How long does the stakeholder decision take?</h3><div class="note">Each tender placed into a duration band by the length of its review window. This is the elapsed calendar time available for all stakeholders to review and reach a decision \u2014 it is <b>not</b> win rate.</div>
   ${hbar(cats,{val:d=>d.v,lab:d=>d.l,fmt:v=>v+' tender'+(v==1?'':'s'),color:d=>[C.red,C.orange,C.green,C.teal,C.blue][d.i]||C.blue,rh:34,maxlab:18})}
   <div style="margin-top:12px;font-size:12px;color:#6B7C86;background:#F2F7FC;border:1px solid #D6E4F2;border-radius:8px;padding:11px 13px">
   <b>Read-out:</b> The stakeholder review runs <b>${t.mean} days on average</b> (median ${t.median}). But the spread is the real story: <b>${t.tight14} of ${t.n}</b> tenders compress the entire BD \u2192 CEO \u2192 technical \u2192 PM \u2192 committee decision into two weeks or less, and ${t.tight7} into a single week \u2014 little time for a considered technical and pricing response. <i>Caveat: the workbook records each department's sign-off as accept/reject but not the date it happened, so this is the overall decision window, not the gap between individual stakeholders. Logging a date at each sign-off would let us pinpoint exactly where tenders stall.</i></div></div>
 <div class="grid g2">
  <div class="card"><h3>The bid / no-bid decision</h3><div class="note">Once reviewed, how often the committee decides to pursue a tender versus pass on it.</div>
   <div style="display:flex;align-items:center;gap:16px;justify-content:center;flex-wrap:wrap">${donut(comSeg,{center:Math.round(100*com.accept/(com.accept+com.reject))+'%',csub:'PURSUED'})}<div>${legend(comSeg)}</div></div></div>
  <div class="card"><h3>Bank-guarantee exposure</h3><div class="note">What "guarantee exposure" means.</div>
   <div style="text-align:center;padding:6px 0 10px"><div style="font-size:34px;font-weight:800;color:#7B6BA8;line-height:1">${guarFmt}</div><div style="font-size:11px;color:#9AA8B0;text-transform:uppercase;letter-spacing:.5px;margin-top:4px">total bid-bond value issued</div></div>
   <div style="font-size:12px;color:#5A4A62;line-height:1.6;background:#F6F3FB;border:1px solid #E0D8F0;border-radius:8px;padding:11px 13px">A <b>bank guarantee</b> (bid bond) is security a bidder must post to enter many government tenders. This figure is the cumulative value of the guarantees EH has issued across the tracked tenders \u2014 i.e. capital tied up as bid security. It is returned when EH is not awarded, or released on contract signing, so it represents committed-but-recoverable exposure, not a sunk cost. Only ${Math.round(100*22/k2.total)>0?'a minority of':'some'} tenders in the tracker record a guarantee value, so the true figure is higher.</div></div>
 </div>
 <div class="card"><h3>Why bids were declined \u2014 ${BA.refused.length} recorded no-bid decisions</h3>
   <div class="note">When the committee decides to pass on a tender, the reason is logged in the comments column. These are the declined bids and exactly why. Capturing this is how EH learns where to stop spending effort \u2014 and the pattern is clear: most declines are work that falls outside EH's scope, needs a licence EH doesn't hold, or is locked to a specific brand.</div>
   <div style="display:flex;flex-wrap:wrap;gap:9px;margin-bottom:15px">
   ${BA.refusal_cats.map(rc=>{const cc=RCAT[rc.cat]||'#9AABB5';return `<div style="display:flex;align-items:center;gap:8px;background:${cc}14;border:1px solid ${cc}55;border-radius:9px;padding:8px 13px"><span style="font-size:17px;font-weight:800;color:${cc}">${rc.n}</span><span style="font-size:11.5px;color:#3A4A52;font-weight:600">${rc.cat}</span></div>`;}).join('')}
   </div>
   <table class="t"><thead><tr><th>Tender</th><th>Project</th><th>Client</th><th>Reason category</th><th>Recorded reason</th></tr></thead><tbody>
   ${BA.refused.map(r=>{const cc=RCAT[r.cat]||'#9AABB5';return `<tr><td><b>#${r.sn}/${String(r.year).slice(2)}</b></td><td dir="auto" style="max-width:180px;font-size:11px;line-height:1.35">${esc(r.title)||'\u2014'}</td><td dir="auto" style="max-width:120px;font-size:10.5px;color:#7B8A92">${esc(r.client)||'\u2014'}</td><td><span class="tag" style="background:${cc};white-space:nowrap">${r.cat}</span></td><td dir="auto" style="max-width:330px;font-size:11px;color:#5A6A72;line-height:1.4">${esc(r.reason)}</td></tr>`;}).join('')}
   </tbody></table></div>`;
})();

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
 const sel=(kk,opts,lab)=>`<div style="display:flex;flex-direction:column;gap:3px"><label style="font-size:10px;color:#8A99A3;text-transform:uppercase;letter-spacing:.4px;font-weight:600">${lab}</label><select onchange="setTF('${kk}',this.value)" style="${ss}">${['all',...opts].map(o=>`<option value="${o}" ${TF[kk]==o?'selected':''}>${o=='all'?'All':o}</option>`).join('')}</select></div>`;
 const outcomes=['Won','Lost','Not awarded','Cancelled','Pending'].filter(o=>BA.bidlist.some(b=>b.outcome==o));
 const ctrls=`<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;margin-bottom:14px;background:#fff;border:1px solid #E3EAE5;border-radius:11px;padding:13px 15px">
   ${sel('year',['2025','2026'],'Year')}
   ${sel('outcome',outcomes,'Outcome')}
   ${sel('platform',uniqVals(b=>platN(b.platform)),'Platform')}
   ${sel('svc',uniqVals(b=>b.svc),'Service line')}
   <div style="display:flex;flex-direction:column;gap:3px;flex:1;min-width:180px"><label style="font-size:10px;color:#8A99A3;text-transform:uppercase;letter-spacing:.4px;font-weight:600">Search title / client / ref</label>
     <input oninput="setTF('q',this.value)" value="${esc(TF.q)}" placeholder="Type to filter\u2026" style="${ss};width:100%;cursor:text"></div>
   <button onclick="TF.year='all';TF.outcome='all';TF.platform='all';TF.svc='all';TF.q='';renderTenders()" style="padding:8px 14px;border:1px solid #D5DEE2;background:#F4F8F5;color:#6B7C86;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer">Reset</button></div>`;
 const rows=list.map(b=>`<tr>
   <td><b>#${b.sn}</b><div style="font-size:9.5px;color:#9AA8B0">${b.year}</div></td>
   <td style="font-size:10.5px;color:#7B8A92;white-space:nowrap">${b.date||'\u2014'}</td>
   <td style="max-width:280px"><div dir="auto" style="font-size:11.5px;line-height:1.35">${esc(b.title)||'<span style="color:#bbb">\u2014</span>'}</div></td>
   <td style="max-width:150px"><div dir="auto" style="font-size:11px;color:#3A4A52">${esc(b.client)||'\u2014'}</div></td>
   <td style="font-size:11px;white-space:nowrap">${esc(platN(b.platform))}</td>
   <td style="font-size:10.5px;color:#6B7C86">${b.svc||'\u2014'}</td>
   <td style="text-align:right;font-size:11px;white-space:nowrap">${b.value?fmtSAR(b.value):'\u2014'}</td>
   <td style="text-align:center">${b.nbid!=null?b.nbid:'\u2014'}</td>
   <td><span class="tag" style="background:${OC[b.outcome]}">${b.outcome.toUpperCase()}</span></td>
   <td style="max-width:130px"><div dir="auto" style="font-size:10.5px;color:#6B7C86">${b.winner=='EH'?'<b style="color:#2E7D46">EH</b>':(esc(b.winner)||'\u2014')}</div></td>
 </tr>`).join('');
 $('s-tenders').innerHTML=
 `<div class="sech">All tracked tenders</div><div class="secsub">Every real tender in the workbooks (empty placeholder rows excluded). Filter by any column or search. <b>${list.length}</b> of ${BA.bidlist.length} shown.</div>
 ${ctrls}
 <div class="card" style="padding:6px 10px">
 <table class="t"><thead><tr><th>Ref</th><th>Launched</th><th>Title</th><th>Client</th><th>Platform</th><th>Service</th><th style="text-align:right">EH value</th><th style="text-align:center">Bidders</th><th>Outcome</th><th>Winner</th></tr></thead>
 <tbody>${rows||'<tr><td colspan="10" style="text-align:center;padding:30px;color:#9AA8B0">No tenders match these filters.</td></tr>'}</tbody></table></div>`;
}
renderTenders();

// ===================== NOTES & LIMITATIONS =====================
(function(){
 const lim=[
  ['Small outcome sample','Only 16 of 144 tenders have a recorded winner and 10 have full competitor pricing. Every win-rate figure — overall and especially the slices by service line, platform, value band and bidder count — is computed off those 16, so most breakdowns rest on one to three tenders. Read them as anecdotes, not statistics.'],
  ['Pricing ≠ full picture','The pricing analysis shows EH\'s losing bids were priced high, but Saudi tenders are scored on technical merit, compliance, delivery capability and incumbency alongside price. Without the technical scores and the stated loss reason, we cannot prove price caused the losses or rule out that EH was competing on larger scope or quality.'],
  ['2025 vs 2026 not comparable','2026 is a partial, in-progress year — many tenders are still pending and outcomes lag launch by months. A near-complete 2025 is being compared against a half-finished 2026 where wins may simply not be recorded yet. The same depresses the most recent months of any time view.'],
  ['Recording is not random','Tenders with a logged outcome or pricing are likely those that progressed furthest or that someone chose to complete. If wins or painful losses get logged more diligently, the recorded win rate is biased in an unknown direction. "Win rate among tenders with an outcome" is not the same as the true win rate.'],
  ['Competitor / client counts undercount','The Arabic↔English name reconciliation matches the major recurring rivals and big clients well, but ~130 one-off Arabic-named SMEs go unmatched. "Competitors faced" counts matched competitors only; the real field is larger, and some small clients may be split across name variants.'],
  ['No market denominator','The dashboard only sees tenders EH tracked — not the tenders EH never bid on or never saw. It therefore cannot measure true market share or bid/no-bid quality. Win rate here is conditional on having bid.'],
  ['Turnaround is a proxy','The workbook records department sign-off as accept/reject but not the date of each review, so true per-stakeholder cycle time can\'t be measured. The launch-to-deadline window is the closest available stand-in.'],
  ['Single self-reported source','All figures come from EH\'s own tracking workbooks, a static snapshot with no cross-check against official Etimad award records. Value fields also mix offered and awarded bases and should be read as proxies.'],
 ];
 $('s-limitations').innerHTML=
 `<div class="sech">Notes &amp; limitations</div><div class="secsub">An honest analyst's read on what this dashboard can and cannot tell you. The analytics are only ever as strong as the completeness of the tracking data behind them.</div>
 <div class="card" style="background:#FFF8EC;border-color:#F0DDB0"><h3 style="color:#8A6D2E">Bottom line</h3><div style="font-size:13px;color:#5A4A2E;line-height:1.6">Use this dashboard to <b>spot patterns and frame questions</b> — where EH may be losing, which clients are slipping, where pricing looks exposed — not to settle them with precision. The headline story (declining win rate, high pricing on losses, SEC concentration) is directionally credible; the exact percentages are not. The single highest-leverage fix is upstream: <b>record an outcome and a loss reason for every closed tender, capture the technical score alongside price, and keep a bid/no-bid log.</b> Do that and most caveats below shrink on their own.</div></div>
 ${lim.map(([h,b])=>`<div class="card"><h3>${h}</h3><div style="font-size:12.5px;color:#4A5A62;line-height:1.6">${b}</div></div>`).join('')}`;
})();

// ===================== WATCHLIST =====================
(function(){
 const SEVC={high:'#B23A3A',med:'#E8862E',low:'#2E7D46'};
 $('s-watchlist').innerHTML=
 `<div class="sech">Watchlist — prioritised alerts</div><div class="secsub">Auto-flagged signals from the bid data that warrant attention, ranked by severity.</div>
 <div class="wl">${BA.watchlist.map(f=>`<div class="wli ${f.sev}"><span class="wlk" style="background:${SEVC[f.sev]}">${esc(f.kind)}</span><span>${esc(f.text)}</span></div>`).join('')}</div>`;
})();

go('overview');
