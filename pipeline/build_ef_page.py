#!/usr/bin/env python3
"""build_ef_page.py — renders hub/environment_fund_2025.html from pipeline/ef_report_2025.json.
Re-run after editing the JSON. The page is self-contained apart from eh-shared.css / eh-shared.js."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'ef_report_2025.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'hub', 'environment_fund_2025.html')
EF = json.load(open(SRC, encoding='utf-8'))
payload = json.dumps(EF, ensure_ascii=False).replace('</', '<\\/')

CSS = r"""
:root{--bg:#F4F7F5;--card:#fff;--ink:#16333F;--muted:#5F7078;--line:#E3EAE5;--green:#1F7A4C;--blue:#1A5FAB;--amber:#E8862E;--red:#C0504D;--chip:#F0F5F2;--efblue:#2A3F80}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--eh-font,"Segoe UI",Tahoma,Arial,sans-serif);background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
body.dark{--bg:#0F1519;--card:#151C21;--ink:#E6EDF1;--muted:#9FB3BE;--line:#2C3A43;--chip:#1E2830;--efblue:#8FA6E6}
header{background:linear-gradient(90deg,#2A3F80,#1F7A4C);color:#fff;padding:16px 22px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
header h1{margin:0;font-size:19px;font-weight:800}header .sub{font-size:12px;opacity:.9;margin-top:2px}
header .ctl{margin-inline-start:auto;display:flex;gap:6px}
.tog{display:inline-flex;border:1px solid rgba(255,255,255,.5);border-radius:8px;overflow:hidden}.tog button{background:transparent;color:#fff;border:0;padding:6px 12px;cursor:pointer;font:600 12px inherit}.tog button.on{background:#fff;color:#1F3A5F}
main{max-width:1380px;margin:0 auto;padding:16px 22px 40px}
.stamp{font-size:12px;color:var(--muted);margin:0 0 12px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}.stamp b{color:var(--ink)}
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin-bottom:16px}
.kc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;border-top:4px solid var(--efblue)}
.kc .v{font-size:24px;font-weight:800;color:var(--efblue);line-height:1.1}.kc .l{font-size:12px;color:var(--muted);margin-top:6px;line-height:1.4}
.pg{display:inline-block;font-size:10.5px;font-weight:700;color:var(--muted);background:var(--chip);border:1px solid var(--line);border-radius:5px;padding:1px 6px;white-space:nowrap;cursor:help}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:16px}
.card h2{margin:0 0 4px;font-size:16px;font-weight:800;color:var(--ink);display:flex;align-items:center;gap:8px}.card h2::before{content:"";width:4px;height:18px;background:var(--green);border-radius:2px;display:inline-block}
.card .note{font-size:12.5px;color:var(--muted);margin-bottom:10px}
.hd{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 12px}.tabs button{background:var(--chip);border:1px solid var(--line);color:var(--ink);border-radius:20px;padding:6px 14px;cursor:pointer;font:600 12.5px inherit}.tabs button.on{background:var(--efblue);border-color:var(--efblue);color:#fff}
.opp{display:grid;grid-template-columns:auto 1fr;gap:10px 14px;padding:12px 0;border-top:1px solid var(--line)}.opp:first-of-type{border-top:0}
.chips{display:flex;flex-direction:column;gap:4px;min-width:96px}
.chip{font-size:10.5px;font-weight:700;border-radius:6px;padding:2px 8px;text-align:center;color:#fff;background:var(--muted)}
.chip.h-Now{background:var(--red)}.chip.h-2026{background:var(--amber)}.chip.h-2027\+{background:var(--blue)}.chip.o{background:var(--chip);color:var(--ink);border:1px solid var(--line)}
.opp .st{font-size:13.5px;line-height:1.55}.opp .ac{font-size:12.5px;color:var(--ink);margin-top:6px;padding:8px 10px;background:var(--chip);border-radius:8px;border-inline-start:3px solid var(--green)}.opp .ac b{color:var(--green)}
table.t{width:100%;border-collapse:collapse;font-size:12.5px}table.t th{text-align:start;font-size:11px;letter-spacing:.3px;color:var(--muted);text-transform:uppercase;padding:6px 8px;border-bottom:1px solid var(--line)}table.t td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}table.t tr:last-child td{border-bottom:0}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:960px){.g2{grid-template-columns:1fr}}
.tag{font-size:10px;font-weight:700;border-radius:5px;padding:2px 6px;color:#fff;display:inline-block}.tag.add{background:var(--green)}.tag.update{background:var(--blue)}.tag.identify{background:var(--amber)}
.gap{display:grid;grid-template-columns:1fr auto;gap:8px 14px;padding:8px 0;border-top:1px solid var(--line);font-size:12.5px}.gap:first-of-type{border-top:0}.gap .how{color:var(--muted);font-size:12px;max-width:340px;text-align:end}
.png{font:600 11px inherit;background:var(--chip);border:1px solid var(--line);color:var(--green);border-radius:7px;padding:5px 10px;cursor:pointer}
svg.pm text{font-family:var(--eh-font,"Segoe UI",Tahoma,Arial,sans-serif)}
.foot{font-size:11.5px;color:var(--muted);text-align:center;margin-top:20px;line-height:1.6}
.xr td.num{text-align:center;font-variant-numeric:tabular-nums}.xr .zero{color:var(--red);font-weight:700}
.read{font-size:13px;padding:10px 12px;background:var(--chip);border-radius:8px;border-inline-start:3px solid var(--amber);margin-top:10px}
[dir=rtl] .gap .how{text-align:start}
"""

JS = r"""
const EF=JSON.parse(document.getElementById('EF').textContent);
let LANG=(localStorage.getItem('ef.lang')||'en'), DARK=false, GROUP='money';
const L=(en,ar)=>LANG==='ar'?ar:en, $=id=>document.getElementById(id), esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const P=p=>`<span class="pg" title="${esc(L('Annual Report 2025, page','التقرير السنوي 2025، صفحة'))} ${p}">${L('p.','ص')} ${p}</span>`;
const fmtM=v=>v>=1e6?(v/1e6).toFixed(1).replace(/\.0$/,'')+' M':v>=1e3?(v/1e3).toFixed(0)+' K':String(v);
const OWN={'BD':'تطوير الأعمال','Finance':'المالية','Operations':'العمليات','Consulting/EIA':'الاستشارات/دراسات الأثر','Training':'التدريب'};
const HOR={'Now':'الآن','2026':'2026','2027+':'2027+'};
function setLang(l){LANG=l;try{localStorage.setItem('ef.lang',l)}catch(e){};document.documentElement.lang=l;document.documentElement.dir=l==='ar'?'rtl':'ltr';render();}
function setDark(d){DARK=d;document.body.classList.toggle('dark',d);}
window.addEventListener('message',e=>{const d=e.data||{};if(d.ehhub==='lang'&&(d.lang==='ar'||d.lang==='en'))setLang(d.lang);if(d.ehhub==='theme')setDark(d.theme==='dark');});
function render(){
 const m=EF.meta;
 $('title').textContent=L('Environment Fund — 2025 Annual Report: what it means for EH','صندوق البيئة — التقرير السنوي 2025: ماذا يعني لآفاق البيئة');
 $('sub').textContent=L(m.source_en,m.source_ar)+' · '+L('read as a map of where EH\'s clients\' money, rules and tenders will come from in 2026–2030','قراءةٌ لمصادر تمويل عملاء آفاق البيئة وقواعدهم ومنافساتهم في 2026–2030');
 document.querySelectorAll('#lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===LANG));
 $('stamp').innerHTML=`<span>${L('Source','المصدر')}: <b>${esc(L(m.source_en,m.source_ar))}</b> (${m.pages} ${L('pages','صفحة')})</span><span>·</span><span>${L('extracted','تاريخ الاستخراج')} <b dir="ltr">${m.extracted}</b></span><span>·</span><span>${L('bid-tracker cross-reference as of','مطابقة جدول العطاءات حتى')} <b dir="ltr">${m.tracker_xref_as_of}</b></span>`;
 $('kstrip').innerHTML=EF.headline.map(h=>`<div class="kc"><div class="v" dir="ltr">${esc(L(h.value,h.ar_value))}</div><div class="l">${esc(L(h.en,h.ar))} ${P(h.page)}</div></div>`).join('');
 // xref
 const x=EF.xref;
 $('xref').innerHTML=`<h2>${L("EH's own record with the Fund and the national centres","سجل آفاق البيئة مع الصندوق والمراكز الوطنية")}</h2><div class="note">${esc(L(x.note_en,x.note_ar))}</div>
 <table class="t xr"><thead><tr><th>${L('Client','الجهة')}</th><th style="text-align:center">${L('Tenders','منافسات')}</th><th style="text-align:center">${L('Value (SAR)','القيمة (ريال)')}</th><th style="text-align:center">${L('Pending','قيد الانتظار')}</th><th style="text-align:center">${L('Cancelled','ملغاة')}</th><th style="text-align:center">${L('Decided','محسومة')}</th><th>${L('Note','ملاحظة')}</th></tr></thead><tbody>
 ${x.rows.map(r=>`<tr><td><b>${esc(L(r.client_en,r.client_ar))}</b></td><td class="num">${r.tenders}</td><td class="num" dir="ltr">${r.value?fmtM(r.value):'—'}</td><td class="num">${r.pending}</td><td class="num">${r.cancelled}</td><td class="num ${r.tenders&&!r.decided?'zero':''}">${r.decided}</td><td style="color:var(--muted)">${esc(L(r.note_en,r.note_ar))}</td></tr>`).join('')}</tbody></table>
 <div class="read">${esc(L(x.reading_en,x.reading_ar))} ${P(87)}</div>`;
 // opportunities
 $('h-opp').textContent=L('What it means for EH — filed by question, tagged by horizon and owner','ماذا يعني لآفاق البيئة — مصنَّف بحسب السؤال، ومعلَّم بالأفق والجهة المسؤولة');
 const G=[['money',L('Money EH can access','تمويل يمكن لآفاق البيئة الوصول إليه')],['tenders',L('Tenders EH will see','منافسات ستراها آفاق البيئة')],['rules',L('Rules and costs that shift','قواعد وتكاليف تتغير')],['competitors',L('Competitors and partners the Fund is funding','منافسون وشركاء يموّلهم الصندوق')]];
 $('tabs').innerHTML=G.map(([k,l])=>`<button class="${k===GROUP?'on':''}" onclick="GROUP='${k}';render()">${l} <span style="opacity:.7">(${EF.opportunities.filter(o=>o.group===k).length})</span></button>`).join('');
 $('opps').innerHTML=EF.opportunities.filter(o=>o.group===GROUP).map(o=>`<div class="opp"><div class="chips"><span class="chip h-${o.horizon}">${esc(L(o.horizon,HOR[o.horizon]||o.horizon))}</span><span class="chip o">${esc(L(o.owner,OWN[o.owner]||o.owner))}</span>${P(o.page)}</div><div><div class="st">${esc(L(o.en,o.ar))}</div><div class="ac"><b>${L('Action','الإجراء')}:</b> ${esc(L(o.action_en,o.action_ar))}</div></div></div>`).join('');
 // programme map
 $('pmwrap').innerHTML=programmeMap();
 // stakeholders + events
 $('stk').innerHTML=`<h2>${L('Stakeholders to add or update in the map','أصحاب مصلحة لإضافتهم أو تحديثهم في الخريطة')}</h2><div class="note">${L('Field values ready to paste into the stakeholder workbook.','قيم الحقول جاهزة للنقل إلى مصنّف أصحاب المصلحة.')}</div>
 <table class="t"><thead><tr><th></th><th>${L('Name','الاسم')}</th><th>${L('Category · Tier','الفئة · المستوى')}</th><th>${L('Role for EH','الدور بالنسبة لآفاق البيئة')}</th><th></th></tr></thead><tbody>
 ${EF.stakeholders.map(s=>`<tr><td><span class="tag ${s.status}">${esc(L({add:'Add',update:'Update',identify:'Identify'}[s.status],{add:'إضافة',update:'تحديث',identify:'تحديد'}[s.status]))}</span></td><td><b dir="auto">${esc(L(s.name_en,s.name_ar))}</b><div style="color:var(--muted);font-size:11.5px" dir="auto">${esc(L(s.name_ar,s.name_en))}</div></td><td style="white-space:nowrap">${esc(s.cat)} · ${esc(s.tier)}</td><td>${esc(L(s.role_en,s.role_ar))}${s.notes_en?`<div style="color:var(--muted);font-size:11.5px;margin-top:3px">${esc(L(s.notes_en,s.notes_ar))}</div>`:''}</td><td>${P(s.page)}</td></tr>`).join('')}</tbody></table>`;
 $('evt').innerHTML=`<h2>${L('Events calendar for BD attendance','تقويم الفعاليات لحضور تطوير الأعمال')}</h2><div class="note">${L('Where the Fund shows up, and why it matters for EH.','أين يظهر الصندوق، ولماذا يهم آفاق البيئة.')}</div>
 <table class="t"><thead><tr><th>${L('Event','الفعالية')}</th><th>${L('When','التوقيت')}</th><th>${L('Why go','لماذا الحضور')}</th><th></th></tr></thead><tbody>
 ${EF.events.map(e=>`<tr><td><b>${esc(L(e.en,e.ar))}</b></td><td style="white-space:nowrap;color:var(--muted)">${esc(L(e.when_en,e.when_ar))}</td><td>${esc(L(e.why_en,e.why_ar))}</td><td>${P(e.page)}</td></tr>`).join('')}</tbody></table>`;
 $('gaps').innerHTML=`<h2>${L("What we don't know","ما لا نعرفه")}</h2><div class="note">${L('The report does not say — and how to find out.','لا يذكره التقرير — وكيف نعرفه.')}</div>${EF.gaps.map(g=>`<div class="gap"><div>${esc(L(g.en,g.ar))}</div><div class="how">→ ${esc(L(g.how_en,g.how_ar))}</div></div>`).join('')}`;
 // facts ledger (collapsible)
 $('facts').innerHTML=`<summary style="cursor:pointer;font-weight:700">${L('Extraction ledger — every figure with its page','سجل الاستخراج — كل رقم بصفحته')} (${EF.facts.length})</summary><table class="t" style="margin-top:10px"><tbody>${EF.facts.map(f=>`<tr><td style="white-space:nowrap">${P(f.page)}</td><td style="color:var(--muted);white-space:nowrap">${esc(f.cat)}</td><td>${esc(L(f.en,f.ar))}</td></tr>`).join('')}</tbody></table>`;
 $('foot').innerHTML=esc(L(m.method_en,m.method_ar));
}
function programmeMap(){
 const pm=EF.programme_map, W=1100, rowH=40, top=56;
 const prods=pm.products, cen=pm.centres, ehl=pm.eh_lines;
 const H=top+Math.max(prods.length,cen.length,ehl.length)*rowH+30;
 const xP=40,xC=W/2-40,xE=W-300, bw=[250,120,200];
 const yP=i=>top+i*rowH+ (Math.max(prods.length,cen.length,ehl.length)-prods.length)*rowH/2;
 const yC=i=>top+i*rowH+(Math.max(prods.length,cen.length,ehl.length)-cen.length)*rowH/2;
 const yE=i=>top+i*rowH+(Math.max(prods.length,cen.length,ehl.length)-ehl.length)*rowH/2;
 const col={grants:'#1F7A4C',loansup:'#2A3F80',guar:'#1A5FAB',impact:'#7B4FA6',ppp:'#E8862E',fees:'#C0504D',shared:'#5F7078',carbon:'#2E9E8E'};
 let s=`<svg id="ex-pm" class="pm" viewBox="0 0 ${W} ${H}" width="100%" xmlns="http://www.w3.org/2000/svg" dir="ltr">
 <text x="${xP}" y="24" font-size="15" font-weight="800" fill="${DARK?'#E6EDF1':'#16333F'}">${esc(L("Environment Fund programmes → national centres they touch → EH service lines they concern","برامج الصندوق ← المراكز الوطنية التي تمسّها ← خطوط خدمات آفاق البيئة المعنية"))}</text>
 <text x="${xP}" y="42" font-size="11" fill="#6B7C86">${esc(L('Source: Annual Report 2025, pages cited on each programme · a line means the report links them explicitly','المصدر: التقرير السنوي 2025، الصفحات مذكورة على كل برنامج · الخط يعني أن التقرير يربطهما صراحةً'))}</text>`;
 prods.forEach((p,i)=>{p.centres.forEach(c=>{const j=cen.findIndex(x=>x[0]===c);if(j<0)return;s+=`<path d="M${xP+bw[0]} ${yP(i)+14} C ${xP+bw[0]+90} ${yP(i)+14}, ${xC-90} ${yC(j)+14}, ${xC} ${yC(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});
  p.eh.forEach(e=>{const j=ehl.findIndex(x=>x[0]===e);if(j<0)return;const x0=p.centres.length?xC+bw[1]:xP+bw[0];const y0=p.centres.length?yC(cen.findIndex(x=>x[0]===p.centres[0]))+14:yP(i)+14;s+=`<path d="M${x0} ${y0} C ${x0+90} ${y0}, ${xE-90} ${yE(j)+14}, ${xE} ${yE(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});});
 prods.forEach((p,i)=>{s+=`<rect x="${xP}" y="${yP(i)}" width="${bw[0]}" height="28" rx="6" fill="${col[p.id]}"/><text x="${xP+10}" y="${yP(i)+19}" font-size="12.5" font-weight="700" fill="#fff">${esc(L(p.en,p.ar))}</text><text x="${xP+bw[0]-8}" y="${yP(i)+19}" font-size="10" fill="#fff" text-anchor="end" opacity=".85">${L('p.','ص')} ${p.page}</text>`;});
 cen.forEach((c,i)=>{s+=`<rect x="${xC}" y="${yC(i)}" width="${bw[1]}" height="28" rx="6" fill="${DARK?'#1E2830':'#F0F5F2'}" stroke="${DARK?'#3A4B55':'#DCE8DF'}"/><text x="${xC+bw[1]/2}" y="${yC(i)+18}" font-size="12" font-weight="700" fill="${DARK?'#E6EDF1':'#16333F'}" text-anchor="middle">${esc(L(c[0],c[1]))}</text>`;});
 ehl.forEach((e,i)=>{s+=`<rect x="${xE}" y="${yE(i)}" width="${bw[2]}" height="28" rx="6" fill="${DARK?'#1E2830':'#fff'}" stroke="#1F7A4C" stroke-width="1.5"/><text x="${xE+10}" y="${yE(i)+18}" font-size="12.5" font-weight="700" fill="${DARK?'#E6EDF1':'#1F7A4C'}">EH · ${esc(L(e[0],e[1]))}</text>`;});
 s+='</svg>';
 return `<div class="hd"><h2>${L('Programme map — what touches whom','خريطة البرامج — ما يمسّ من')}</h2><button class="png" onclick="exPNG('ex-pm','programme_map')">${L('Export PNG','تصدير PNG')}</button></div><div class="note">${L('Loan support, guarantees and impact investment reach EH directly; grants, PPP, fees and shared services reach EH through the centres it is licensed by and bids to.','دعم القروض والضمانات واستثمارات الأثر تصل آفاق البيئة مباشرة؛ أما المنح والتخصيص والمقابلات المالية والخدمات المشتركة فتصلها عبر المراكز التي ترخّصها وتتقدم لمنافساتها.')}</div>${s}`;
}
function exPNG(id,name){const svg=$(id);if(!svg)return;const cl=svg.cloneNode(true);const vb=svg.viewBox.baseVal;cl.setAttribute('width',vb.width);cl.setAttribute('height',vb.height);cl.removeAttribute('class');
 cl.querySelectorAll('text').forEach(t=>t.setAttribute('font-family',"'Segoe UI',Tahoma,Arial,sans-serif"));
 const bg=document.createElementNS('http://www.w3.org/2000/svg','rect');bg.setAttribute('width',vb.width);bg.setAttribute('height',vb.height);bg.setAttribute('fill',DARK?'#151C21':'#fff');cl.insertBefore(bg,cl.firstChild);
 const xml=new XMLSerializer().serializeToString(cl),img=new Image(),S=2.5;img.onload=()=>{const c=document.createElement('canvas');c.width=vb.width*S;c.height=vb.height*S;const x=c.getContext('2d');x.drawImage(img,0,0,c.width,c.height);const a=document.createElement('a');a.download=`EH_EnvFund2025_${name}_${LANG}_${new Date().toISOString().slice(0,10)}.png`;a.href=c.toDataURL('image/png');document.body.appendChild(a);a.click();a.remove();};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(xml);}
document.documentElement.lang=LANG;document.documentElement.dir=LANG==='ar'?'rtl':'ltr';render();
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Environment Fund — 2025 Annual Report · what it means for EH</title>
<link rel="stylesheet" href="eh-shared.css">
<style>{CSS}</style>
</head>
<body>
<header>
 <div><h1 id="title"></h1><div class="sub" id="sub"></div></div>
 <div class="ctl"><div class="tog" id="lang"><button data-l="en" onclick="setLang('en')">EN</button><button data-l="ar" onclick="setLang('ar')">عربي</button></div></div>
</header>
<main>
 <div class="stamp" id="stamp"></div>
 <div class="kstrip" id="kstrip"></div>
 <div class="card" id="xref"></div>
 <div class="card"><h2 id="h-opp"></h2><div class="tabs" id="tabs"></div><div id="opps"></div></div>
 <div class="card" id="pmwrap"></div>
 <div class="g2"><div class="card" id="stk"></div><div class="card" id="evt"></div></div>
 <div class="card" id="gaps"></div>
 <details class="card" id="facts"></details>
 <div class="foot" id="foot"></div>
</main>
<script id="EF" type="application/json">{payload}</script>
<script>{JS}</script>
<script src="eh-shared.js" defer></script>
</body></html>
"""
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(HTML)
print('written', OUT, len(HTML)//1024, 'KB')
