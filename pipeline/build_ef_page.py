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

# EH design system v2 (patch_design_ef.py): page skin, placed after the page CSS so it wins
SKIN = r"""
/* EH design system v2 — Environment Fund skin (patch_design_ef.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);
  --green:var(--eh-leaf-ink);--blue:var(--eh-sea);--amber:var(--eh-warn);--red:var(--eh-bad);--efblue:var(--eh-sea);
  background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead (standalone): deep navy, contour lines, land-to-sea line along the lower edge */
header,body.dark header{background:var(--eh-deep);position:relative;isolation:isolate;padding:20px 22px 22px;gap:12px 16px}
body.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header>div:first-child{min-width:0;flex:1 1 320px}
header h1{font:600 23px/1.25 var(--eh-display);letter-spacing:-.005em}
header .sub{font-size:13.5px;opacity:.8;margin-top:4px;line-height:1.5}
.tog{border-color:rgba(255,255,255,.32);border-radius:var(--eh-r-ctl)}
.tog button{font:600 12.5px var(--eh-font);color:rgba(255,255,255,.85);padding:7px 13px}
.tog button.on{background:#fff;color:var(--eh-deep)}
/* inside the hub the masthead belongs to the hub: this header becomes a quiet toolbar on the page colour */
html.eh-embedded header,html.eh-embedded body.dark header{background:transparent;color:var(--eh-ink);padding:16px 22px 4px}
html.eh-embedded header::after,html.eh-embedded header>.eh-contour{display:none}
html.eh-embedded header h1{font-size:21px}
html.eh-embedded header .sub{color:var(--eh-ink-2);opacity:1}
html.eh-embedded .tog{border-color:var(--eh-line);background:var(--eh-paper)}
html.eh-embedded .tog button{color:var(--eh-ink-2)}
html.eh-embedded .tog button.on{background:var(--eh-sea);color:#fff}
html.eh-embedded body.dark .tog button.on{color:#0D1736}
main{padding:18px 22px 44px}
/* source line and names */
.stamp{font-size:12.5px;color:var(--eh-ink-3);gap:6px 10px}.stamp b{color:var(--eh-ink);font-weight:600}
#names{font-size:12.5px !important;color:var(--eh-ink-2);line-height:1.6;max-width:150ch}#names b{color:var(--eh-ink);font-weight:600}
/* KPI tiles: no coloured edges; numbers lead */
.kstrip{gap:12px;margin-bottom:18px}
.kc,body.dark .kc{background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
.kc .v{font:600 26px/1.12 var(--eh-display);color:var(--eh-ink);unicode-bidi:isolate}
html[dir=rtl] .kc .v{text-align:right}
.kc .l{font-size:13px;color:var(--eh-ink-2);margin-top:7px;line-height:1.45}
/* page references */
.pg{font:600 12px/1.5 var(--eh-font);color:var(--eh-ink-3);background:var(--eh-tint);border:0;border-radius:var(--eh-r-chip);padding:0 7px;unicode-bidi:isolate;font-variant-numeric:tabular-nums}
/* panels and headings */
.card,body.dark .card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;margin-bottom:16px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.card h2{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);gap:8px}
.card h2::before{display:none}
#charts>.card:first-child h2{font-size:21px}
.card .note{font-size:13px;color:var(--eh-ink-2);line-height:1.55;margin:4px 0 12px}
.hd{gap:10px 14px}
/* grid columns may shrink below their widest table (the table then scrolls inside, the page does not) */
.g2>*,.g3>*{min-width:0}
/* opportunity tabs */
.tabs{gap:8px;margin:10px 0 14px}
.tabs button{font:600 13px var(--eh-font);background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink-2);border-radius:var(--eh-r-chip);padding:7px 14px}
.tabs button:hover{border-color:var(--eh-sea);color:var(--eh-ink)}
.tabs button.on,body.dark .tabs button.on{background:var(--eh-sea);border-color:var(--eh-sea);color:#fff}
body.dark .tabs button.on{color:#0D1736}
/* opportunities: when (a word plus a shape), who, page */
.opp{gap:10px 16px;padding:14px 0;border-top-color:var(--eh-line)}
.chips{gap:5px;min-width:104px}
.chip{display:inline-flex;align-items:center;justify-content:center;gap:5px;font:600 12px/1.5 var(--eh-font);border-radius:var(--eh-r-chip);padding:1px 9px;background:var(--eh-muted-bg);color:var(--eh-muted)}
.chip::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.chip.h-Now{background:var(--eh-bad-bg);color:var(--eh-bad)}.chip.h-Now::before{transform:rotate(45deg);width:6px;height:6px}
.chip.h-2026{background:var(--eh-warn-bg);color:var(--eh-warn)}.chip.h-2026::before{border-radius:1px}
.chip.h-2027\+{background:var(--eh-info-bg);color:var(--eh-info)}.chip.h-2027\+::before{background:none;border:1.5px solid currentColor;border-radius:50%}
.chip.o{background:var(--eh-tint);color:var(--eh-ink-2);border:0;font-weight:500}.chip.o::before{display:none}
.chips .pg{align-self:center}
.opp .st{font-size:14px;line-height:1.6;color:var(--eh-ink)}
.opp .ac{font-size:13px;color:var(--eh-ink);background:var(--eh-tint);border-radius:9px;border-inline-start:3px solid var(--eh-leaf);padding:9px 12px;margin-top:8px}
.opp .ac b{color:var(--eh-leaf-ink);font-weight:600}
/* tables */
table.t{font-size:13px;font-variant-numeric:tabular-nums}
table.t th{font:600 12.5px var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2);background:var(--eh-tint);padding:8px 9px;border-bottom:1px solid var(--eh-line)}
table.t td{padding:8px 9px;border-bottom-color:var(--eh-line)}
table.t tbody tr:hover td{background:var(--eh-tint)}
table.t td [style*="color:var(--muted)"],table.t td[style*="color:var(--muted)"]{color:var(--eh-ink-2) !important}
.xr .zero{color:var(--eh-bad);font-weight:700}
.tag{display:inline-flex;align-items:center;gap:5px;font:600 12px/1.5 var(--eh-font);border-radius:var(--eh-r-chip);padding:1px 9px 1px 8px}
.tag::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.tag.add{background:var(--eh-good-bg);color:var(--eh-good)}.tag.add::before{border-radius:50%}
.tag.update{background:var(--eh-info-bg);color:var(--eh-info)}.tag.update::before{background:none;border:1.5px solid currentColor;border-radius:50%}
.tag.identify{background:var(--eh-warn-bg);color:var(--eh-warn)}.tag.identify::before{border-radius:1px}
.read{font-size:13.5px;line-height:1.6;background:var(--eh-warn-bg);color:var(--eh-ink);border-radius:9px;border-inline-start:3px solid var(--eh-amber);padding:11px 14px;margin-top:12px}
/* what we don't know */
.gap{font-size:13.5px;padding:10px 0;border-top-color:var(--eh-line)}.gap .how{font-size:13px;color:var(--eh-ink-2)}
details#facts>summary{font:600 16px var(--eh-display);color:var(--eh-ink)}
/* export buttons */
.png,body.dark .png{font:600 12px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl);padding:6px 11px}
.png:hover{background:var(--eh-info-bg)}
/* charts: brand fonts; titles in the display face */
svg.pm text{font-family:var(--eh-font)}
svg.pm text[font-weight="800"]{font-family:var(--eh-display);font-weight:600}
.foot{font-size:12px;color:var(--eh-ink-3);line-height:1.65;max-width:130ch;margin:24px auto 0}
/* Arabic */
html[dir=rtl] .kc,html[dir=rtl] .card{text-align:start}
html[dir=rtl] .card h2{line-height:1.55}
/* phone: wide tables scroll inside their panel, never the page */
@media(max-width:760px){
  header{padding:16px 16px 18px}header h1{font-size:19px}
  main{padding:14px 12px 36px}
  .card{padding:15px 14px}
  .kc .v{font-size:22px}
  table.t{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .gap{grid-template-columns:1fr}.gap .how{max-width:none;text-align:start}
  .opp{grid-template-columns:1fr}.chips{flex-direction:row;flex-wrap:wrap;min-width:0}
}
"""

JS = r"""
const EF=JSON.parse(document.getElementById('EF').textContent);
let LANG=(localStorage.getItem('ef.lang')||'en'), DARK=false, GROUP='money';
const L=(en,ar)=>LANG==='ar'?ar:en, $=id=>document.getElementById(id), esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const P=p=>`<span class="pg" title="${esc(L('Annual Report 2025, page','التقرير السنوي 2025، صفحة'))} ${p}">${L('p.','ص')} ${p}</span>`;
const fmtM=v=>v>=1e6?(v/1e6).toFixed(1).replace(/\.0$/,'')+' M':v>=1e3?(v/1e3).toFixed(0)+' K':String(v);
const OWN_EN={'BD':'Business Development','Consulting/EIA':'Consulting / environmental studies'};
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
 $('stamp').innerHTML=`<span>${L('Source','المصدر')}: <b>${esc(L(m.source_en,m.source_ar))}</b> (${m.pages} ${L('pages','صفحة')})</span><span>·</span><span>${L('extracted','تاريخ الاستخراج')} <b dir="ltr">${m.extracted}</b></span><span>·</span><span>${L('checked against EH\'s bid tracker on','مطابقة جدول العطاءات حتى')} <b dir="ltr">${m.tracker_xref_as_of}</b></span>`;
 /* NAMES_LINE: every agency in full once per page (agreed 30 Sep 2026), then the short form */
 (function(){let el=document.getElementById('names');if(!el){el=document.createElement('div');el.id='names';el.className='note';el.style.cssText='margin:-4px 0 12px;font-size:12px';$('kstrip').parentNode.insertBefore(el,$('kstrip'));}
  el.innerHTML=L('<b>Names used on this page:</b> NCEC — National Center for Environmental Compliance · MWAN — National Center for Waste Management · NCVC — National Center for Vegetation Cover &amp; Combating Desertification · NCW — National Center for Wildlife · NCM — National Center for Meteorology · MEWA — Ministry of Environment, Water &amp; Agriculture · EXPRO — Expenditure &amp; Projects Efficiency Authority (checks government spending and projects) · Etimad — the government tendering portal · Kafalah — the state loan-guarantee programme for small businesses','<b>الأسماء المستخدمة في هذه الصفحة:</b> المركز الوطني للرقابة على الالتزام البيئي · المركز الوطني لإدارة النفايات (موان) · المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر · المركز الوطني لتنمية الحياة الفطرية · المركز الوطني للأرصاد · وزارة البيئة والمياه والزراعة · هيئة كفاءة الإنفاق والمشروعات الحكومية (إكسبرو) · اعتماد — بوابة المنافسات الحكومية · كفالة — برنامج ضمان تمويل المنشآت الصغيرة');})();
 $('kstrip').innerHTML=EF.headline.map(h=>`<div class="kc"><div class="v" dir="ltr">${esc(L(h.value,h.ar_value))}</div><div class="l">${esc(L(h.en,h.ar))} ${P(h.page)}</div></div>`).join('');
 // xref
 const x=EF.xref;
 $('xref').innerHTML=`<h2>${L("EH's own record with the Fund and the national centres","سجل آفاق البيئة مع الصندوق والمراكز الوطنية")}</h2><div class="note">${esc(L(x.note_en,x.note_ar))}</div>
 <table class="t xr"><thead><tr><th>${L('Client','الجهة')}</th><th style="text-align:center">${L('Tenders','منافسات')}</th><th style="text-align:center">${L('Value (SAR)','القيمة (ريال)')}</th><th style="text-align:center">${L('Pending','قيد الانتظار')}</th><th style="text-align:center">${L('Cancelled','ملغاة')}</th><th style="text-align:center">${L('Decided','محسومة')}</th><th>${L('Note','ملاحظة')}</th></tr></thead><tbody>
 ${x.rows.map(r=>`<tr><td><b>${esc(L(r.client_en,r.client_ar))}</b></td><td class="num">${r.tenders}</td><td class="num" dir="ltr">${r.value?fmtM(r.value):'—'}</td><td class="num">${r.pending}</td><td class="num">${r.cancelled}</td><td class="num ${r.tenders&&!r.decided?'zero':''}">${r.decided}</td><td style="color:var(--muted)">${esc(L(r.note_en,r.note_ar))}</td></tr>`).join('')}</tbody></table>
 <div class="read">${esc(L(x.reading_en,x.reading_ar))} ${P(87)}</div>`;
 // opportunities
 $('h-opp').textContent=L('What it means for EH — grouped by question, with when it matters and who at EH acts','ماذا يعني لآفاق البيئة — مصنَّف بحسب السؤال، ومعلَّم بالأفق والجهة المسؤولة');
 const G=[['money',L('Money EH can access','تمويل يمكن لآفاق البيئة الوصول إليه')],['tenders',L('Tenders EH will see','منافسات ستراها آفاق البيئة')],['rules',L('Rules and costs that shift','قواعد وتكاليف تتغير')],['competitors',L('Competitors and partners the Fund is funding','منافسون وشركاء يموّلهم الصندوق')]];
 $('tabs').innerHTML=G.map(([k,l])=>`<button class="${k===GROUP?'on':''}" onclick="GROUP='${k}';render();window.EH_SHARED&&EH_SHARED.viewIn($('opps'))">${l} <span style="opacity:.7">(${EF.opportunities.filter(o=>o.group===k).length})</span></button>`).join('');
 $('opps').innerHTML=EF.opportunities.filter(o=>o.group===GROUP).map(o=>`<div class="opp"><div class="chips"><span class="chip h-${o.horizon}">${esc(L(o.horizon,HOR[o.horizon]||o.horizon))}</span><span class="chip o">${esc(L(OWN_EN[o.owner]||o.owner,OWN[o.owner]||o.owner))}</span>${P(o.page)}</div><div><div class="st">${esc(L(o.en,o.ar))}</div><div class="ac"><b>${L('Action','الإجراء')}:</b> ${esc(L(o.action_en,o.action_ar))}</div></div></div>`).join('');
 // programme map
 $('pmwrap').innerHTML=mir(programmeMap());
 $('charts').innerHTML=`<div class="card"><h2>${L('The Kingdom by the Fund\'s numbers — what the report quantifies','المملكة بأرقام الصندوق — ما يقيسه التقرير')}</h2><div class="note">${L('Every figure the report gives a number to, charted. It does not itemise the 80 waste opportunities or the 45 feasibility studies — those counts are the most the report discloses (see "What we don\'t know").','كل ما أعطاه التقرير رقماً، مرسوماً. لا يفصّل التقرير فرص النفايات الثمانين ولا دراسات الجدوى الـ45 — تلك الأعداد هي أقصى ما يكشفه (انظر «ما لا نعرفه»).')}</div></div>`+EF.charts.map(c=>`<div class="card"><div class="hd"><h2>${esc(L(c.title_en,c.title_ar))}</h2><button class="png" onclick="exPNG('${c.id}','${c.id.replace('c-','')}')">${L('Export PNG','تصدير PNG')}</button></div><div class="note">${esc(L(c.sub_en,c.sub_ar))} · ${c.pages.map(P).join(' ')}</div>${mir(chart(c))}</div>`).join('');
 // stakeholders + events
 $('stk').innerHTML=`<h2>${L('Stakeholders to add or update in the map','أصحاب مصلحة لإضافتهم أو تحديثهم في الخريطة')}</h2><div class="note">${L('Field values ready to paste into the stakeholder workbook.','قيم الحقول جاهزة للنقل إلى مصنّف أصحاب المصلحة.')}</div>
 <table class="t"><thead><tr><th></th><th>${L('Name','الاسم')}</th><th>${L('Category · Tier','الفئة · المستوى')}</th><th>${L('Role for EH','الدور بالنسبة لآفاق البيئة')}</th><th></th></tr></thead><tbody>
 ${EF.stakeholders.map(s=>`<tr><td><span class="tag ${s.status}">${esc(L({add:'Add',update:'Update',identify:'Identify'}[s.status],{add:'إضافة',update:'تحديث',identify:'تحديد'}[s.status]))}</span></td><td><b dir="auto">${esc(L(s.name_en,s.name_ar))}</b><div style="color:var(--muted);font-size:11.5px" dir="auto">${esc(L(s.name_ar,s.name_en))}</div></td><td style="white-space:nowrap">${esc(s.cat)} · ${esc(s.tier)}</td><td>${esc(L(s.role_en,s.role_ar))}${s.notes_en?`<div style="color:var(--muted);font-size:11.5px;margin-top:3px">${esc(L(s.notes_en,s.notes_ar))}</div>`:''}</td><td>${P(s.page)}</td></tr>`).join('')}</tbody></table>`;
 $('evt').innerHTML=`<h2>${L('Events Business Development should attend','تقويم الفعاليات لحضور تطوير الأعمال')}</h2><div class="note">${L('Where the Fund shows up, and why it matters for EH.','أين يظهر الصندوق، ولماذا يهم آفاق البيئة.')}</div>
 <table class="t"><thead><tr><th>${L('Event','الفعالية')}</th><th>${L('When','التوقيت')}</th><th>${L('Why go','لماذا الحضور')}</th><th></th></tr></thead><tbody>
 ${EF.events.map(e=>`<tr><td><b>${esc(L(e.en,e.ar))}</b></td><td style="white-space:nowrap;color:var(--muted)">${esc(L(e.when_en,e.when_ar))}</td><td>${esc(L(e.why_en,e.why_ar))}</td><td>${P(e.page)}</td></tr>`).join('')}</tbody></table>`;
 $('gaps').innerHTML=`<h2>${L("What we don't know","ما لا نعرفه")}</h2><div class="note">${L('The report does not say — and how to find out.','لا يذكره التقرير — وكيف نعرفه.')}</div>${EF.gaps.map(g=>`<div class="gap"><div>${esc(L(g.en,g.ar))}</div><div class="how">→ ${esc(L(g.how_en,g.how_ar))}</div></div>`).join('')}`;
 // facts ledger (collapsible)
 $('facts').innerHTML=`<summary style="cursor:pointer;font-weight:700">${L('Every figure and the page it comes from','سجل الاستخراج — كل رقم بصفحته')} (${EF.facts.length})</summary><table class="t" style="margin-top:10px"><tbody>${EF.facts.map(f=>`<tr><td style="white-space:nowrap">${P(f.page)}</td><td style="color:var(--muted);white-space:nowrap">${esc(f.cat)}</td><td>${esc(L(f.en,f.ar))}</td></tr>`).join('')}</tbody></table>`;
 $('foot').innerHTML=esc(L(m.method_en,m.method_ar));
}
// EH design system v2 (patch_design_ef.py): brand palette (land → sea) for the colours stored in the report data
const BCM={'#2A3F80':'#3B57B8','#E8862E':'#C98A1B','#1F7A4C':'#54AB5D','#C0504D':'#B23F2B','#1A5FAB':'#0072BB','#2E9E8E':'#00A0E0','#5F7078':'#5E6B80','#7B4FA6':'#8E6BB8','#9AABB5':'#9DABC5'};
const BC=x=>BCM[String(x||'').toUpperCase()]||x;
// one label column for every chart, wide enough for the longest label in the current language
function EF_L0(){let n=0;EF.charts.forEach(c=>c.rows.forEach(r=>{n=Math.max(n,String(L(r.en,r.ar)).length)}));return Math.round(Math.min(560,Math.max(330,n*6.3+26)));}
// Arabic: mirror a drawn chart so labels sit on the right and bars grow leftwards (text is never flipped)
function mir(h){if(LANG!=='ar')return h;const t=document.createElement('template');t.innerHTML=h;
 t.content.querySelectorAll('svg').forEach(svg=>{const W=+(svg.getAttribute('viewBox')||'0 0 0 0').split(/\s+/)[2]||0,num=(e,a)=>+(e.getAttribute(a)||0);
  svg.querySelectorAll('rect').forEach(e=>e.setAttribute('x',(W-num(e,'x')-num(e,'width')).toFixed(1)));
  svg.style.direction='rtl';   // text keeps its logical anchor: in right-to-left, start is the right edge
  svg.querySelectorAll('text').forEach(e=>{e.setAttribute('x',(W-num(e,'x')).toFixed(1));
   if(!/[\u0600-\u06FF]/.test(e.textContent)){e.style.direction='ltr';const a=e.getAttribute('text-anchor')||'start';if(a!=='middle')e.setAttribute('text-anchor',a==='end'?'start':'end');}});   // figures and units read left to right
  svg.querySelectorAll('line').forEach(e=>{e.setAttribute('x1',W-num(e,'x1'));e.setAttribute('x2',W-num(e,'x2'));});
  svg.querySelectorAll('path').forEach(e=>e.setAttribute('d',e.getAttribute('d').replace(/(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)/g,(m,x,y)=>(W-x)+' '+y)));});
 return t.innerHTML;}
// programme-map labels: white or navy, whichever reads better on the box colour
function onFill(hx){const v=[1,3,5].map(i=>{const c=parseInt(hx.substr(i,2),16)/255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)}),l=0.2126*v[0]+0.7152*v[1]+0.0722*v[2];return (1.05/(l+0.05))>=((l+0.05)/0.0686)?'#fff':'#15224D';}
function chart(c){
 const W=1100, rowH=34, L0=EF_L0(), iw=W-L0-190, ink='var(--eh-ink)', mut='var(--eh-ink-3)';   // EH design v2: token colours follow the theme
 c=Object.assign({},c,{color:BC(c.color),colors:(c.colors||[]).map(BC),rows:c.rows.map(r=>r.c?Object.assign({},r,{c:BC(r.c)}):r)});
 const head=`<text x="14" y="22" font-size="14" font-weight="800" fill="${ink}">${esc(L(c.title_en,c.title_ar))}</text><text x="14" y="38" font-size="10.5" fill="${mut}">${esc(L('Source: Environment Fund Annual Report 2025 · p.','المصدر: التقرير السنوي لصندوق البيئة 2025 · ص'))} ${c.pages.join(', ')}</text>`;
 if(c.type==='compare'){
  const H=56+c.rows.length*44+30, max=Math.max(...c.rows.flatMap(r=>[r.a,r.b]));
  let s=`<svg id="${c.id}" class="pm" viewBox="0 0 ${W} ${H}" width="100%" xmlns="http://www.w3.org/2000/svg" dir="ltr">${head}`;
  s+=`<rect x="${W-190}" y="14" width="12" height="12" fill="${c.colors[0]}"/><text x="${W-172}" y="24" font-size="11" fill="${ink}">${c.series[0]}</text><rect x="${W-110}" y="14" width="12" height="12" fill="${c.colors[1]}"/><text x="${W-92}" y="24" font-size="11" fill="${ink}">${c.series[1]}</text>`;
  c.rows.forEach((r,i)=>{const y=56+i*44;const wa=r.a/max*iw,wb=r.b/max*iw;const up=r.b>r.a;const better=/days|الأيام/.test(r.en+r.ar)?!up:up;
   s+=`<text x="${L0-12}" y="${y+22}" text-anchor="end" font-size="12" fill="${ink}">${esc(L(r.en,r.ar))}</text><rect x="${L0}" y="${y+4}" width="${wa}" height="13" rx="2" fill="${c.colors[0]}"/><text x="${L0+wa+6}" y="${y+15}" font-size="11" fill="${mut}">${r.a}</text><rect x="${L0}" y="${y+20}" width="${wb}" height="13" rx="2" fill="${c.colors[1]}"/><text x="${L0+wb+6}" y="${y+31}" font-size="11" font-weight="700" fill="${ink}">${r.b} <tspan fill="${better?'var(--eh-good)':'var(--eh-bad)'}">${up?'▲':'▼'} ${Math.abs(Math.round((r.b-r.a)/r.a*100))}%</tspan></text><text x="${W-40}" y="${y+22}" text-anchor="end" font-size="10" fill="${mut}">${L('p.','ص')} ${r.p}</text>`;});
  return s+'</svg>';
 }
 const H=56+c.rows.length*rowH+16, vals=c.rows.map(r=>r.v), max=c.pct?100:Math.max(...vals);
 const scale=v=>c.log?Math.log10(v+1)/Math.log10(max+1)*iw:v/max*iw;
 let s=`<svg id="${c.id}" class="pm" viewBox="0 0 ${W} ${H}" width="100%" xmlns="http://www.w3.org/2000/svg" dir="ltr">${head}`;
 c.rows.forEach((r,i)=>{const y=56+i*rowH,w=Math.max(scale(r.v),2);const col=r.c||c.color;
  s+=`<text x="${L0-12}" y="${y+19}" text-anchor="end" font-size="12" fill="${ink}">${esc(L(r.en,r.ar))}</text><rect x="${L0}" y="${y+5}" width="${w.toFixed(1)}" height="22" rx="3" fill="${col}"/><text x="${L0+w+8}" y="${y+20}" font-size="12.5" font-weight="700" fill="${ink}">${r.v.toLocaleString('en-US')}${c.pct?'%':c.unit==='t'?' t':''}</text><text x="${W-40}" y="${y+20}" text-anchor="end" font-size="10" fill="${mut}">${L('p.','ص')} ${r.p}</text>`;});
 if(c.log)s+=`<text x="${L0}" y="${H-4}" font-size="10" fill="${mut}">${esc(L('compressed scale so large and small numbers fit — bar lengths are not to scale','مقياس لوغاريتمي — أطوال الأشرطة غير تناسبية'))}</text>`;
 return s+'</svg>';
}
function programmeMap(){
 const pm=EF.programme_map, W=1100, rowH=40, top=56;
 const prods=pm.products, cen=pm.centres, ehl=pm.eh_lines;
 const H=top+Math.max(prods.length,cen.length,ehl.length)*rowH+30;
 const xP=40,xC=W/2-40,xE=W-300, bw=[310,150,200];   // EH design v2: programme and centre boxes wide enough for the longest label (English and Arabic) in the brand font
 const yP=i=>top+i*rowH+ (Math.max(prods.length,cen.length,ehl.length)-prods.length)*rowH/2;
 const yC=i=>top+i*rowH+(Math.max(prods.length,cen.length,ehl.length)-cen.length)*rowH/2;
 const yE=i=>top+i*rowH+(Math.max(prods.length,cen.length,ehl.length)-ehl.length)*rowH/2;
 const col={grants:'#2E7A37',loansup:'#3B57B8',guar:'#0072BB',impact:'#8E6BB8',ppp:'#C98A1B',fees:'#B23F2B',shared:'#5E6B80',carbon:'#00A0E0'};   // EH brand palette
 let s=`<svg id="ex-pm" class="pm" viewBox="0 0 ${W} ${H}" width="100%" xmlns="http://www.w3.org/2000/svg" dir="ltr">
 <text x="${xP}" y="24" font-size="15" font-weight="800" fill="var(--eh-ink)">${esc(L("Environment Fund programmes → national centres they touch → EH service lines they concern","برامج الصندوق ← المراكز الوطنية التي تمسّها ← خطوط خدمات آفاق البيئة المعنية"))}</text>
 <text x="${xP}" y="42" font-size="11" fill="var(--eh-ink-3)">${esc(L('Source: Annual Report 2025, pages cited on each programme · a line means the report links them explicitly','المصدر: التقرير السنوي 2025، الصفحات مذكورة على كل برنامج · الخط يعني أن التقرير يربطهما صراحةً'))}</text>`;
 prods.forEach((p,i)=>{p.centres.forEach(c=>{const j=cen.findIndex(x=>x[0]===c);if(j<0)return;s+=`<path d="M${xP+bw[0]} ${yP(i)+14} C ${xP+bw[0]+90} ${yP(i)+14}, ${xC-90} ${yC(j)+14}, ${xC} ${yC(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});
  p.eh.forEach(e=>{const j=ehl.findIndex(x=>x[0]===e);if(j<0)return;const x0=p.centres.length?xC+bw[1]:xP+bw[0];const y0=p.centres.length?yC(cen.findIndex(x=>x[0]===p.centres[0]))+14:yP(i)+14;s+=`<path d="M${x0} ${y0} C ${x0+90} ${y0}, ${xE-90} ${yE(j)+14}, ${xE} ${yE(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});});
 prods.forEach((p,i)=>{s+=`<rect x="${xP}" y="${yP(i)}" width="${bw[0]}" height="28" rx="6" fill="${col[p.id]}"/><text x="${xP+10}" y="${yP(i)+19}" font-size="12.5" font-weight="700" fill="${onFill(col[p.id])}">${esc(L(p.en,p.ar))}</text><text x="${xP+bw[0]-8}" y="${yP(i)+19}" font-size="10.5" fill="${onFill(col[p.id])}" text-anchor="end" opacity=".85">${L('p.','ص')} ${p.page}</text>`;});
 cen.forEach((c,i)=>{s+=`<rect x="${xC}" y="${yC(i)}" width="${bw[1]}" height="28" rx="6" fill="var(--eh-tint)" stroke="var(--eh-line)"/><text x="${xC+bw[1]/2}" y="${yC(i)+18}" font-size="12" font-weight="700" fill="var(--eh-ink)" text-anchor="middle">${esc(L(c[0],c[1]))}</text>`;});
 ehl.forEach((e,i)=>{s+=`<rect x="${xE}" y="${yE(i)}" width="${bw[2]}" height="28" rx="6" fill="var(--eh-paper)" stroke="var(--eh-leaf-ink)" stroke-width="1.5"/><text x="${xE+10}" y="${yE(i)+18}" font-size="12.5" font-weight="700" fill="var(--eh-leaf-ink)">EH · ${esc(L(e[0],e[1]))}</text>`;});
 s+='</svg>';
 return `<div class="hd"><h2>${L('Programme map — what touches whom','خريطة البرامج — ما يمسّ من')}</h2><button class="png" onclick="exPNG('ex-pm','programme_map')">${L('Export PNG','تصدير PNG')}</button></div><div class="note">${L('Loan support, guarantees and impact investment reach EH directly; grants, partnerships with private companies, fees and shared services reach EH through the centres that license it and that it bids to.','دعم القروض والضمانات واستثمارات الأثر تصل آفاق البيئة مباشرة؛ أما المنح والتخصيص والمقابلات المالية والخدمات المشتركة فتصلها عبر المراكز التي ترخّصها وتتقدم لمنافساتها.')}</div>${s}`;
}
// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)
let EXFONTS=null;
function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);
 const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'],['EH Display','vendor/fonts/montserrat-latin-var.woff2','100 900'],['EH Display','vendor/fonts/alexandria-arabic-var.woff2','100 900']];
 return Promise.all(F.map(f=>fetch(f[1]).then(r=>r.ok?r.blob():null).then(b=>b?new Promise(res=>{const fr=new FileReader();fr.onload=()=>res(`@font-face{font-family:'${f[0]}';src:url(${fr.result}) format('woff2');font-weight:${f[2]}}`);fr.readAsDataURL(b);}):'').catch(()=>''))).then(a=>EXFONTS=a.join(''));}
function exPNG(id,name){ exFonts().then(()=>exPNG2(id,name)); }
function exPNG2(id,name){const svg=$(id);if(!svg)return;const cl=svg.cloneNode(true);const vb=svg.viewBox.baseVal;cl.setAttribute('width',vb.width);cl.setAttribute('height',vb.height);cl.removeAttribute('class');
 // read every colour as the light theme draws it, so the PNG is ink on white in either theme
 const dk=document.body.classList.contains('dark');if(dk)document.body.classList.remove('dark');
 const se=[...svg.querySelectorAll('*')],ce=[...cl.querySelectorAll('*')];
 se.forEach((e,i)=>{const d=ce[i];if(!d||!/^(text|tspan|rect|path|line|circle)$/.test(e.tagName))return;const cs=getComputedStyle(e);d.setAttribute('fill',cs.fill);d.setAttribute('stroke',cs.stroke);
  if(e.tagName==='text'){d.setAttribute('font-family',/EH Display/.test(cs.fontFamily)?"'EH Display','Segoe UI',Tahoma,Arial,sans-serif":"'EH Sans','Segoe UI',Tahoma,Arial,sans-serif");d.setAttribute('font-weight',cs.fontWeight);}d.removeAttribute('class');d.removeAttribute('style');});
 if(dk)document.body.classList.add('dark');
 const fst=document.createElementNS('http://www.w3.org/2000/svg','style');fst.textContent=EXFONTS||'';cl.insertBefore(fst,cl.firstChild);
 const bg=document.createElementNS('http://www.w3.org/2000/svg','rect');bg.setAttribute('width',vb.width);bg.setAttribute('height',vb.height);bg.setAttribute('fill','#fff');cl.insertBefore(bg,cl.firstChild);
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
<style id="eh-skin">{SKIN}</style>
</head>
<body>
<header data-eh-contour="7">
 <div><h1 id="title"></h1><div class="sub" id="sub"></div></div>
 <div class="ctl"><div class="tog" id="lang"><button data-l="en" onclick="setLang('en')">EN</button><button data-l="ar" onclick="setLang('ar')">عربي</button></div></div>
</header>
<main>
 <div class="stamp" id="stamp"></div>
 <div class="kstrip" id="kstrip"></div>
 <div class="card" id="xref"></div>
 <div class="card"><h2 id="h-opp"></h2><div class="tabs" id="tabs"></div><div id="opps"></div></div>
 <div class="card" id="pmwrap"></div>
 <div id="charts"></div>
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
