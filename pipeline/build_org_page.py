#!/usr/bin/env python3
"""
build_org_page.py — renders the Organisations view (hub/organisations.html) from org_profiles.json (26 Oct 2026).

    python pipeline/build_org_page.py pipeline/org_profiles.json site/organisations.html

The page is a standalone bilingual (EN/AR) hub app: a searchable list of every organisation with activity on the
left, one profile on the right — map standing, bid history as client, head-to-heads as a bidder, wins against EH,
client ledger, licence, Etimad, notes. It follows the hub's language/theme via the {ehhub:'lang'|'theme'} messages,
uses eh-shared.css/js, and embeds its data in <script id="ORG" type="application/json">.
"""
import json, sys, html

TEMPLATE = r'''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EH · Organisations</title>
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
*{box-sizing:border-box}
body{margin:0;overflow-x:hidden;background:var(--eh-mist);color:var(--eh-ink);font:var(--eh-fs-m)/var(--eh-lh) var(--eh-font)}
a{color:var(--eh-sea)}
.hd{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:14px 20px 10px;border-bottom:1px solid var(--eh-line);background:var(--eh-paper)}
.hd h1{margin:0;font-size:var(--eh-fs-h2);color:var(--eh-deep)}
.hd .sub{color:var(--eh-ink-2);font-size:var(--eh-fs-s)}
.hd .sp{flex:1}
html.eh-embedded .hd .chrome{display:none}
.wrap{display:grid;grid-template-columns:340px 1fr;gap:var(--eh-gap);padding:var(--eh-gap);min-height:calc(100vh - 70px)}
@media (max-width:900px){.wrap{grid-template-columns:1fr}.list{position:static;max-height:46vh}}
.list{display:flex;flex-direction:column;min-height:0;position:sticky;top:var(--eh-gap);max-height:calc(100vh - 2*var(--eh-gap));align-self:start}
.q{position:relative;margin-bottom:10px}
.q input{width:100%;padding:11px 14px 11px 38px;border:1.5px solid var(--eh-line);border-radius:var(--eh-r-ctl);background:var(--eh-paper);color:var(--eh-ink);font:inherit;font-size:15px}
[dir=rtl] .q input{padding:11px 38px 11px 14px}
.q input:focus{outline:none;border-color:var(--eh-sea);box-shadow:0 0 0 3px var(--eh-info-bg)}
.q svg{position:absolute;top:13px;inset-inline-start:12px;width:17px;height:17px;color:var(--eh-ink-3)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.chip{font:600 12px/1.5 var(--eh-font);padding:4px 11px;border-radius:var(--eh-r-chip);border:1px solid var(--eh-line);background:var(--eh-paper);color:var(--eh-ink-2);cursor:pointer;transition:all var(--eh-dur-1) var(--eh-ease)}
.chip.on{background:var(--eh-deep);border-color:var(--eh-deep);color:#fff}
html.dark .chip.on{background:var(--eh-sea);border-color:var(--eh-sea);color:#0D1736}
.cnt{font-size:var(--eh-fs-xs);color:var(--eh-ink-3);margin:0 2px 8px}
.rows{overflow:auto;flex:1;border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);background:var(--eh-paper);box-shadow:var(--eh-shadow)}
.row{display:block;width:100%;text-align:start;padding:10px 14px;border:0;border-bottom:1px solid var(--eh-line);background:transparent;color:inherit;font:inherit;cursor:pointer;transition:background var(--eh-dur-1)}
.row:hover{background:var(--eh-tint)}.row.on{background:var(--eh-info-bg);box-shadow:inset 3px 0 0 var(--eh-sea)}
[dir=rtl] .row.on{box-shadow:inset -3px 0 0 var(--eh-sea)}
.row .nm{font-weight:600;font-size:14px;line-height:1.35}
.row .mt{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:3px;font-size:12px;color:var(--eh-ink-2)}
.row .mt b{color:var(--eh-ink);font-weight:600}
.prof{min-width:0}
.card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);padding:16px 18px;margin-bottom:var(--eh-gap)}
.card h2{margin:0 0 10px;font-size:var(--eh-fs-h3);color:var(--eh-deep);display:flex;align-items:center;gap:8px}
.card h2 .n{font-size:12px;color:var(--eh-ink-3);font-weight:500;font-family:var(--eh-font)!important}
.ph{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap}
.ph h1{margin:0;font-size:var(--eh-fs-h1);line-height:1.15;color:var(--eh-deep);font-weight:700}
.ph .als{color:var(--eh-ink-2);font-size:13px;margin-top:4px}
.ph .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px 18px;margin-top:14px;padding-top:12px;border-top:1px solid var(--eh-line)}
.facts .k{font-size:11.5px;color:var(--eh-ink-3);text-transform:uppercase;letter-spacing:.04em}
[dir=rtl] .facts .k{text-transform:none}
.facts .v{font-weight:600;margin-top:2px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:10px;margin-bottom:var(--eh-gap)}
.kc{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:12px 14px;box-shadow:var(--eh-shadow);min-width:0;overflow:hidden}
.kc.m .v{font-size:21px;padding-top:4px}
.kc .l{font-size:11.5px;color:var(--eh-ink-2);font-weight:500}
.kc .v{font-size:var(--eh-fs-kpi);line-height:1.1;margin-top:4px;color:var(--eh-deep)}
.kc .s{font-size:11.5px;color:var(--eh-ink-3);margin-top:3px}
.kc.good .v{color:var(--eh-good)}
html.dark .kc .v,html.dark .ph h1,html.dark .card h2,html.dark .hd h1,html.dark .empty h2{color:var(--eh-ink)}
html.dark .kc.good .v{color:var(--eh-good)}html.dark .kc.bad .v{color:var(--eh-bad)}html.dark .kc.info .v{color:var(--eh-sea)}.kc.bad .v{color:var(--eh-bad)}.kc.info .v{color:var(--eh-sea-ink)}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:start;font-size:11.5px;color:var(--eh-ink-2);font-weight:600;padding:8px 8px;border-bottom:1px solid var(--eh-line);background:var(--eh-tint);white-space:nowrap}
td{padding:8px 8px;border-bottom:1px solid var(--eh-line);vertical-align:top}
tr.t{cursor:pointer}tr.t:hover td{background:var(--eh-tint)}
td.num,th.num{text-align:end;white-space:nowrap;font-variant-numeric:tabular-nums}
td.ttl{min-width:220px}td.ttl .s{display:block;font-size:11.5px;color:var(--eh-ink-3);margin-top:2px}
tr.x td{background:var(--eh-mist);padding:10px 14px}
.bd{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px}
.bd span{padding:3px 9px;border-radius:8px;background:var(--eh-paper);border:1px solid var(--eh-line)}
.bd span.eh{border-color:var(--eh-leaf);font-weight:600}.bd span.w{border-color:var(--eh-good);background:var(--eh-good-bg)}
.bd span.dq{text-decoration:line-through;color:var(--eh-ink-3)}
.bd span b{font-weight:500;color:var(--eh-ink-2);margin-inline-start:6px}
.none{display:block;padding:14px;text-align:center;color:var(--eh-ink-2);border:1.5px dashed var(--eh-line);border-radius:10px;font-size:13px}
.svcs{display:flex;flex-wrap:wrap;gap:6px}
.notes{white-space:pre-wrap;font-size:13px;color:var(--eh-ink-2);line-height:1.6}
.empty{display:flex;align-items:center;justify-content:center;min-height:50vh;color:var(--eh-ink-2);text-align:center;padding:30px}
.empty h2{color:var(--eh-deep);margin:0 0 8px}
.warn{display:inline-flex;align-items:center;gap:6px;padding:6px 10px;border-radius:8px;background:var(--eh-warn-bg);color:var(--eh-warn);font-size:12.5px;font-weight:600;margin-top:10px}
.ft{padding:10px 20px 24px;font-size:12px;color:var(--eh-ink-3)}
@media print{.list,.hd .chrome,.q,.chips,.cnt{display:none!important}.wrap{display:block;padding:0}.card{break-inside:avoid;box-shadow:none}body{background:#fff}}
</style>
</head>
<body>
<header class="hd">
  <div><h1 data-en="Organisations" data-ar="المنظمات">Organisations</h1>
  <div class="sub" id="stamp"></div></div>
  <div class="sp"></div>
  <button class="eh-btn chrome" id="langBtn" onclick="setLang(LANG==='en'?'ar':'en')">عربي</button>
  <button class="eh-btn chrome" id="darkBtn" onclick="toggleDark()">Dark</button>
  <button class="eh-btn" onclick="window.print()" data-en="Export / print" data-ar="تصدير / طباعة">Export / print</button>
</header>
<div class="wrap">
  <aside class="list">
    <div class="q"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" autocomplete="off" data-ph-en="Find an organisation (English or Arabic)…" data-ph-ar="ابحث عن منظمة (عربي أو إنجليزي)…" placeholder="Find an organisation (English or Arabic)…"></div>
    <div class="chips" id="chips"></div>
    <div class="cnt" id="cnt"></div>
    <div class="rows" id="rows"></div>
  </aside>
  <main class="prof" id="prof"></main>
</div>
<div class="ft" data-en="Figures come from the bid tracker (2025 and 2026) and the Stakeholder Map on the date shown. A tender awaiting a result shows SUBMITTED when EH has submitted its bid and PENDING when it has not. Prices are EH's submitted price including VAT, as in the Bid &amp; Tender app." data-ar="الأرقام من جدول تتبع المنافسات (2025 و2026) وخريطة الأطراف المعنية بتاريخ النشر المبيّن. المنافسة التي تنتظر نتيجة تظهر «تم التقديم» إذا قدّمت آفاق البيئة عرضها و«بانتظار التقديم» إن لم تقدّم. الأسعار هي سعر عرض آفاق البيئة شاملاً الضريبة كما في تطبيق المنافسات.">Figures come from the bid tracker (2025 and 2026) and the Stakeholder Map on the date shown.</div>
<script id="ORG" type="application/json">__DATA__</script>
<script>
var ORG=JSON.parse(document.getElementById('ORG').textContent), ORGS=ORG.orgs;
var LANG='en', ROLE='all', Q='', SEL=null;
var T={
 'All':'الكل','Clients':'عملاء المنافسات','Competitors':'منافسون','Beat EH':'تغلّبوا على آفاق البيئة','EH clients':'عملاء آفاق البيئة','Not on the map yet':'ليست على الخريطة بعد',
 'organisations':'منظمة','tenders':'منافسات','encounters':'مواجهات','client value':'قيمة العميل','Tracker spellings':'التسميات في جدول التتبع','Also known as':'تُعرف أيضاً بـ',
 'Category':'الفئة','Tier':'الفئة التصنيفية','Region':'المنطقة','City':'المدينة','Confidence':'درجة الثقة','Threat':'التهديد','Map score':'درجة الخريطة',
 'Tenders asked':'منافسات طرحتها','EH submitted':'قدّمت آفاق البيئة','Won':'فوز','Lost':'خسارة','Pending':'بانتظار النتيجة','Win rate':'نسبة الفوز','Value won':'قيمة الفوز','Value lost':'قيمة الخسارة',
 'Head-to-heads':'مواجهات مع آفاق البيئة','Beat EH (times)':'تغلّب على آفاق البيئة (مرات)','Priced below EH':'سعّر أقل من آفاق البيئة','Client value (SAR)':'قيمة العميل (ريال)','Projects':'مشاريع',
 'Tenders where this organisation was the client':'المنافسات التي طرحتها هذه المنظمة','Tenders where this organisation bid against EH':'المنافسات التي نافست فيها آفاق البيئة','Tenders this organisation won against EH':'المنافسات التي فازت بها على آفاق البيئة',
 'What EH sells this client':'ما تبيعه آفاق البيئة لهذا العميل','Licence':'الترخيص','Government tenders (Etimad)':'منافسات حكومية (اعتماد)','Notes and evidence':'ملاحظات وأدلة',
 'Ref':'المرجع','Date':'التاريخ','Title':'العنوان','Platform':'المنصة','EH price':'سعر آفاق البيئة','Bidders':'المتقدمون','Winner':'الفائز','Winning price':'سعر الفائز','Gap to lowest':'الفرق عن الأقل','Result':'النتيجة','Reason':'السبب',
 'Client':'العميل','Their price':'سعرهم','per unit':'سعر الوحدة','Price vs EH':'السعر مقابل آفاق البيئة','Lost to EH':'خسر أمام آفاق البيئة','Lost to another bidder':'خسر أمام متقدم آخر','of':'من','Rank':'الترتيب','Outcome':'النتيجة',
 'SUBMITTED':'تم التقديم','PENDING':'بانتظار التقديم','CANCELLED':'ملغاة','WON':'فوز','LOST':'خسارة','NOT AWARDED':'لم تتم الترسية',
 'none on record':'لا يوجد في السجل','No tenders on record':'لا توجد منافسات في السجل','No head-to-heads on record':'لا توجد مواجهات في السجل','No wins against EH on record':'لا يوجد فوز على آفاق البيئة في السجل',
 'No EH contracts on record':'لا توجد عقود لآفاق البيئة في السجل','No licence on record':'لا يوجد ترخيص في السجل','No Etimad tenders on record':'لا توجد منافسات اعتماد في السجل','No notes on record':'لا توجد ملاحظات في السجل',
 'Not on the Stakeholder Map yet — this name comes from the bid tracker and waits for a decision (link to an existing record or add a new one). Nothing here is counted into any map record.':'ليست على خريطة الأطراف المعنية بعد — هذا الاسم من جدول تتبع المنافسات وينتظر قراراً (ربطه بسجل قائم أو إضافة سجل جديد). لا يُحتسب شيء هنا في أي سجل على الخريطة.',
 'Pick an organisation':'اختر منظمة','Search by name, alias or any spelling the bid tracker uses. Every organisation with a tender, a bid against EH, a win, or an EH contract is here.':'ابحث بالاسم أو الاسم البديل أو أي تسمية يستخدمها جدول التتبع. كل منظمة لها منافسة أو عرض ضد آفاق البيئة أو فوز أو عقد مع آفاق البيئة موجودة هنا.',
 'Services':'الخدمات','Years':'السنوات','Activities':'الأنشطة','Expiry':'الانتهاء','Tenders on Etimad':'منافسات على اعتماد','Open':'مفتوحة','Last capture':'آخر التقاط','undisclosed':'غير معلن','DQ':'مستبعد','EH':'آفاق البيئة',
 'Tier':'التصنيف','map':'خريطة','SAR':'ريال','asked':'طُرحت','vs EH':'ضد آفاق البيئة','Beaten by':'خسرت أمام','below':'أقل','above':'أعلى','lowest':'الأقل'
};
function t(s){return LANG==='ar'&&T[s]!==undefined?T[s]:s}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function money(v){if(v==null||isNaN(v))return'<span class="eh-none">'+t('none on record')+'</span>';return'<bdi class="eh-ltr">'+Math.round(v).toLocaleString('en-US')+'</bdi>'}
function pct(v){return v==null?'<span class="eh-none">—</span>':'<bdi class="eh-ltr">'+v+'%</bdi>'}
function d(s){return s?'<bdi class="eh-ltr">'+esc(s)+'</bdi>':'—'}
function st(tn){var o=tn.outcome;if(o==='Won')return'<span class="eh-st won">'+t('WON')+'</span>';if(o==='Lost')return'<span class="eh-st lost">'+t('LOST')+'</span>';if(o==='Not awarded')return'<span class="eh-st off">'+t('NOT AWARDED')+'</span>';if(o==='Cancelled')return'<span class="eh-st off">'+t('CANCELLED')+'</span>';return tn.submitted?'<span class="eh-st wait" style="color:var(--eh-sea);background:var(--eh-info-bg)">'+t('SUBMITTED')+'</span>':'<span class="eh-st off">'+t('PENDING')+'</span>'}
function tierChip(p){if(!p.resolved)return'<span class="eh-chip amber" style="background:var(--eh-warn-bg);color:var(--eh-warn)">'+t('Not on the map yet')+'</span>';var c=p.tier==='Tier 1'?'green':p.tier==='GOV'?'blue':'grey';return(p.tier&&p.tier!=='—'?'<span class="eh-chip '+c+'">'+esc(p.tier)+'</span>':'')+(p.cat?'<span class="eh-chip grey">'+esc(p.cat)+'</span>':'')}
function hasRole(p,r){return p.roles.indexOf(r)>=0}
var ROLES=[['all','All'],['client','Clients'],['competitor','Competitors'],['beat','Beat EH'],['eh-client','EH clients'],['unresolved','Not on the map yet']];
function normq(s){return String(s||'').normalize('NFKC').toLowerCase().replace(/[\u0640\u200b-\u200f\u064b-\u0652]/g,'').replace(/[إأآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/[^\w\u0600-\u06FF]+/g,' ').trim()}
ORGS.forEach(function(p){p._k=normq([p.name].concat(p.aliases,p.tracker_names).join(' | '))})
function filtered(){var q=normq(Q).split(' ').filter(Boolean);return ORGS.filter(function(p){
  if(ROLE==='beat'){if(!(p.kpi.beat_eh>0||p.wins.length>0))return false}
  else if(ROLE==='unresolved'){if(p.resolved)return false}
  else if(ROLE!=='all'&&!hasRole(p,ROLE))return false;
  return q.every(function(w){return p._k.indexOf(w)>=0})})}
function renderChips(){document.getElementById('chips').innerHTML=ROLES.map(function(r){return'<button class="chip'+(ROLE===r[0]?' on':'')+'" onclick="ROLE=\''+r[0]+'\';renderChips();renderList()">'+t(r[1])+'</button>'}).join('')}
function renderList(){var L=filtered();document.getElementById('cnt').textContent=L.length+' '+t('organisations');
  document.getElementById('rows').innerHTML=L.slice(0,400).map(function(p){var k=p.kpi,m=[];
    if(k.tenders)m.push('<b>'+k.tenders+'</b> '+t('tenders'));if(k.encounters)m.push('<b>'+k.encounters+'</b> '+t('encounters'));if(k.wins_total)m.push('<b>'+k.wins_total+'</b> '+t('vs EH'));if(k.client_value)m.push('<b>'+Math.round(k.client_value/1e6*10)/10+'M</b> '+t('client value'));
    return'<button class="row'+(SEL&&SEL.id===p.id?' on':'')+'" onclick="pick(\''+esc(p.id).replace(/'/g,"\\'")+'\')"><div class="nm">'+esc(p.name)+(p.resolved?'':' <span class="eh-chip" style="background:var(--eh-warn-bg);color:var(--eh-warn)">'+t('Not on the map yet')+'</span>')+'</div><div class="mt">'+(p.tier&&p.tier!=='—'?'<span>'+esc(p.tier)+'</span>':'')+m.map(function(x){return'<span>'+x+'</span>'}).join('')+'</div></button>'}).join('')}
function pick(id){SEL=ORGS.filter(function(p){return p.id===id})[0]||null;try{location.hash='#org='+encodeURIComponent(id)}catch(e){}renderList();renderProf();if(window.innerWidth<900){document.getElementById('prof').scrollIntoView({behavior:'smooth',block:'start'})}else{window.scrollTo({top:0,behavior:'smooth'})}}
function kc(l,v,cls,s){return'<div class="kc'+(cls?' '+cls:'')+'"><div class="l">'+t(l)+'</div><div class="v">'+v+'</div>'+(s?'<div class="s">'+s+'</div>':'')+'</div>'}
function bidders(tn){if(!tn.bidders||!tn.bidders.length)return'<span class="eh-none">'+t('none on record')+'</span>';return'<div class="bd">'+tn.bidders.map(function(b){var c=b.eh?' eh':'';if(b.won)c+=' w';if(b.dq)c+=' dq';return'<span class="'+c+'">'+(b.eh?t('EH'):esc(b.name))+(b.price!=null?'<b>'+money(b.price)+'</b>':'<b>'+t('undisclosed')+'</b>')+(b.dq?' · '+t('DQ'):'')+'</span>'}).join('')+'</div>'}
function gap(tn){if(tn.gap==null||tn.eh_price==null)return'—';if(tn.gap===0)return'<span class="eh-chip green">'+t('lowest')+'</span>';return'<bdi class="eh-ltr">+'+tn.gap+'%</bdi>'}
function tendersTable(p){if(!p.tenders.length)return'<span class="none">'+t('No tenders on record')+'</span>';
  return'<div style="overflow:auto"><table><thead><tr><th>'+t('Ref')+'</th><th>'+t('Date')+'</th><th>'+t('Title')+'</th><th>'+t('Platform')+'</th><th class="num">'+t('EH price')+'</th><th class="num">'+t('Bidders')+'</th><th>'+t('Winner')+'</th><th class="num">'+t('Winning price')+'</th><th class="num">'+t('Gap to lowest')+'</th><th>'+t('Result')+'</th></tr></thead><tbody>'+
  p.tenders.map(function(tn,i){var w=tn.winner==='EH'?'<b>'+t('EH')+'</b>':tn.winner?esc(tn.winner):'—';
    return'<tr class="t" onclick="var x=document.getElementById(\'x'+i+'\');x.style.display=x.style.display===\'none\'?\'\':\'none\'"><td><bdi class="eh-ltr">'+esc(tn.ref)+'</bdi></td><td>'+d(tn.date)+'</td><td class="ttl">'+esc(tn.title)+(tn.lossreason||tn.reason?'<span class="s">'+esc(tn.lossreason||tn.reason)+'</span>':'')+'</td><td>'+esc(tn.platform||'—')+'</td><td class="num">'+(tn.eh_price!=null?money(tn.eh_price)+(tn.per_unit?'<div style="font-size:10.5px;color:var(--eh-ink-3)">'+t('per unit')+'</div>':''):'<span class="eh-none">—</span>')+'</td><td class="num">'+(tn.nbid!=null?tn.nbid:'—')+'</td><td>'+w+'</td><td class="num">'+(tn.win_price!=null?money(tn.win_price):'—')+'</td><td class="num">'+gap(tn)+'</td><td>'+st(tn)+'</td></tr>'+
    '<tr class="x" id="x'+i+'" style="display:none"><td colspan="10">'+bidders(tn)+'</td></tr>'}).join('')+'</tbody></table></div>'}
function encTable(p){if(!p.encounters.length)return'<span class="none">'+t('No head-to-heads on record')+'</span>';
  return'<div style="overflow:auto"><table><thead><tr><th>'+t('Ref')+'</th><th>'+t('Date')+'</th><th>'+t('Title')+'</th><th>'+t('Client')+'</th><th class="num">'+t('Their price')+'</th><th class="num">'+t('EH price')+'</th><th>'+t('Price vs EH')+'</th><th>'+t('Outcome')+'</th></tr></thead><tbody>'+
  p.encounters.map(function(e){var o=e.won?'<span class="eh-st won">'+t('Won')+'</span>':e.dq?'<span class="eh-st off">'+t('DQ')+'</span>':e.outcome==='Won'?'<span class="eh-st lost">'+t('Lost to EH')+'</span>':e.outcome==='Lost'?'<span class="eh-st off">'+t('Lost to another bidder')+'</span>':e.outcome==='Cancelled'?'<span class="eh-st off">'+t('CANCELLED')+'</span>':e.outcome==='Not awarded'?'<span class="eh-st off">'+t('NOT AWARDED')+'</span>':'<span class="eh-st wait">'+t('Pending')+'</span>';
    var pv=e.their_price!=null&&e.eh_price!=null?(e.undercut?'<span class="eh-chip red">'+t('below')+' '+t('EH')+'</span>':'<span class="eh-chip grey">'+t('above')+' '+t('EH')+'</span>'):'<span class="eh-chip grey">'+t('undisclosed')+'</span>';
    return'<tr><td><bdi class="eh-ltr">'+esc(e.ref)+'</bdi></td><td>'+d(e.date)+'</td><td class="ttl">'+esc(e.title)+'</td><td><a href="#" onclick="pick(\''+esc(e.client_id).replace(/'/g,"\\'")+'\');return false">'+esc(e.client)+'</a></td><td class="num">'+(e.their_price!=null?money(e.their_price):'<span class="eh-none">'+t('undisclosed')+'</span>')+'</td><td class="num">'+(e.eh_price!=null?money(e.eh_price):'—')+'</td><td>'+pv+'</td><td>'+o+'</td></tr>'}).join('')+'</tbody></table></div>'}
function winsTable(p){if(!p.wins.length)return'<span class="none">'+t('No wins against EH on record')+'</span>';
  return'<div style="overflow:auto"><table><thead><tr><th>'+t('Ref')+'</th><th>'+t('Title')+'</th><th>'+t('Client')+'</th><th class="num">'+t('Winning price')+'</th><th class="num">'+t('EH price')+'</th></tr></thead><tbody>'+p.wins.map(function(w){return'<tr><td><bdi class="eh-ltr">'+esc(w.ref)+'</bdi></td><td class="ttl">'+esc(w.title)+'</td><td><a href="#" onclick="pick(\''+esc(w.client_id).replace(/'/g,"\\'")+'\');return false">'+esc(w.client)+'</a></td><td class="num">'+(w.win_price!=null?money(w.win_price):'—')+'</td><td class="num">'+(w.eh_price!=null?money(w.eh_price):'—')+'</td></tr>'}).join('')+'</tbody></table></div>'}
function clientBlock(p){var c=p.client;if(!c)return'<span class="none">'+t('No EH contracts on record')+'</span>';
  return'<div class="facts" style="border:0;padding:0;margin:0"><div><div class="k">'+t('Projects')+'</div><div class="v">'+(c.proj!=null?c.proj:'—')+'</div></div><div><div class="k">'+t('Client value (SAR)')+'</div><div class="v">'+money(c.val)+'</div></div><div><div class="k">'+t('Years')+'</div><div class="v"><bdi class="eh-ltr">'+esc((c.years||[]).join(', ')||'—')+'</bdi></div></div></div>'+
  (c.svcs&&c.svcs.length?'<div style="margin-top:10px"><div class="k eh-label">'+t('Services')+'</div><div class="svcs" style="margin-top:6px">'+c.svcs.map(function(s){return'<span class="eh-chip blue">'+esc(s)+'</span>'}).join('')+'</div></div>':'')}
function licBlock(p){var l=p.lic;if(!l||(!l.act&&!l.mw))return'<span class="none">'+t('No licence on record')+'</span>';var mw=l.mw&&typeof l.mw==='object'?l.mw:{};
  return'<div class="facts" style="border:0;padding:0;margin:0"><div><div class="k">'+t('Activities')+'</div><div class="v"><bdi class="eh-ltr">'+esc(l.act||'—')+'</bdi></div></div>'+(mw.exp?'<div><div class="k">'+t('Expiry')+'</div><div class="v">'+d(mw.exp)+'</div></div>':'')+(mw.cities?'<div><div class="k">'+t('City')+'</div><div class="v">'+esc(Array.isArray(mw.cities)?mw.cities.join(', '):mw.cities)+'</div></div>':'')+'</div>'}
function etimadBlock(p){var e=p.etimad;if(!e)return'<span class="none">'+t('No Etimad tenders on record')+'</span>';
  return'<div class="facts" style="border:0;padding:0;margin:0"><div><div class="k">'+t('Tenders on Etimad')+'</div><div class="v">'+(e.tenders!=null?e.tenders:'—')+'</div></div><div><div class="k">'+t('Open')+'</div><div class="v">'+(e.open!=null?e.open:'—')+'</div></div><div><div class="k">'+t('Last capture')+'</div><div class="v">'+d(e.last_capture)+'</div></div></div>'}
function renderProf(){var p=SEL,el=document.getElementById('prof');
  if(!p){el.innerHTML='<div class="card empty"><div><h2>'+t('Pick an organisation')+'</h2><div>'+t('Search by name, alias or any spelling the bid tracker uses. Every organisation with a tender, a bid against EH, a win, or an EH contract is here.')+'</div></div></div>';return}
  var k=p.kpi,aka=p.aliases.concat(p.tracker_names.filter(function(x){return p.aliases.indexOf(x)<0}));
  var h='<div class="card"><div class="ph"><div style="flex:1;min-width:240px"><h1>'+esc(p.name)+'</h1>'+(aka.length?'<div class="als">'+t('Also known as')+': '+aka.map(esc).join(' · ')+'</div>':'')+
    '<div class="tags">'+tierChip(p)+p.roles.map(function(r){return'<span class="eh-chip blue">'+t({client:'Clients',competitor:'Competitors',winner:'Beat EH','eh-client':'EH clients'}[r]||r)+'</span>'}).join('')+'</div>'+
    (p.resolved?'':'<div class="warn">⚠ '+t('Not on the Stakeholder Map yet — this name comes from the bid tracker and waits for a decision (link to an existing record or add a new one). Nothing here is counted into any map record.')+'</div>')+'</div></div>';
  if(p.resolved)h+='<div class="facts"><div><div class="k">'+t('Category')+'</div><div class="v">'+esc(p.cat||'—')+'</div></div><div><div class="k">'+t('Region')+'</div><div class="v">'+esc(p.region||'—')+(p.city&&p.city!==p.region?' · '+esc(p.city):'')+'</div></div><div><div class="k">'+t('Confidence')+'</div><div class="v">'+esc(p.cf||'—')+'</div></div>'+(p.threat?'<div><div class="k">'+t('Threat')+'</div><div class="v">'+esc(p.threat)+'</div></div>':'')+(p.score!=null?'<div><div class="k">'+t('Map score')+'</div><div class="v"><bdi class="eh-ltr">'+Math.round(p.score)+'/100</bdi></div></div>':'')+(p.typ?'<div><div class="k">Type</div><div class="v">'+esc(p.typ)+(p.sec?' · '+esc(p.sec):'')+'</div></div>':'')+'</div>';
  h+='</div>';
  var K=[];
  if(hasRole(p,'client')){K.push(kc('Tenders asked',k.tenders,'',k.years.length?'<bdi class="eh-ltr">'+k.years.join(' · ')+'</bdi>':''));K.push(kc('EH submitted',k.submitted,'info'));K.push(kc('Won',k.won,'good',money(k.value_won)+' '+t('SAR')));K.push(kc('Lost',k.lost,k.lost?'bad':'',money(k.value_lost)+' '+t('SAR')));K.push(kc('Pending',k.pending));K.push(kc('Win rate',pct(k.win_rate)))}
  if(hasRole(p,'competitor')||hasRole(p,'winner')){K.push(kc('Head-to-heads',k.encounters,'info'));K.push(kc('Beat EH (times)',k.beat_eh,k.beat_eh?'bad':''));K.push(kc('Priced below EH',k.undercut,'',k.priced_vs?pct(k.undercut_pct)+' '+t('of')+' '+k.priced_vs:''))}
  if(p.client){K.push(kc('Client value (SAR)',money(p.client.val),'good m',p.client.proj+' '+t('Projects')))}
  h+='<div class="kpis">'+K.join('')+'</div>';
  h+='<div class="card"><h2>'+t('Tenders where this organisation was the client')+' <span class="n">'+p.tenders.length+'</span></h2>'+tendersTable(p)+'</div>';
  h+='<div class="card"><h2>'+t('Tenders where this organisation bid against EH')+' <span class="n">'+p.encounters.length+'</span></h2>'+encTable(p)+'</div>';
  if(p.wins.length)h+='<div class="card"><h2>'+t('Tenders this organisation won against EH')+' <span class="n">'+p.wins.length+'</span></h2>'+winsTable(p)+'</div>';
  h+='<div class="card"><h2>'+t('What EH sells this client')+'</h2>'+clientBlock(p)+'</div>';
  h+='<div class="card"><h2>'+t('Licence')+'</h2>'+licBlock(p)+'</div>';
  h+='<div class="card"><h2>'+t('Government tenders (Etimad)')+'</h2>'+etimadBlock(p)+'</div>';
  h+='<div class="card"><h2>'+t('Notes and evidence')+'</h2>'+(p.notes?'<div class="notes">'+esc(p.notes)+'</div>':'<span class="none">'+t('No notes on record')+'</span>')+'</div>';
  el.innerHTML=h;if(window.ehMotion&&ehMotion.animateCards)try{ehMotion.animateCards(el)}catch(e){}}
function relabel(){document.querySelectorAll('[data-en]').forEach(function(e){e.innerHTML=LANG==='ar'?e.getAttribute('data-ar'):e.getAttribute('data-en')});var q=document.getElementById('q');q.placeholder=LANG==='ar'?q.getAttribute('data-ph-ar'):q.getAttribute('data-ph-en');document.getElementById('langBtn').textContent=LANG==='ar'?'English':'عربي'}
function setLang(l){LANG=l;document.documentElement.lang=l;document.documentElement.dir=l==='ar'?'rtl':'ltr';relabel();renderChips();renderList();renderProf();document.getElementById('stamp').textContent=(LANG==='ar'?'جدول التتبع بتاريخ ':'Tracker as of ')+ORG.built+' · '+ORG.counts.orgs+' '+t('organisations')}
function toggleDark(){var on=document.documentElement.classList.toggle('dark');document.getElementById('darkBtn').textContent=on?(LANG==='ar'?'فاتح':'Light'):(LANG==='ar'?'داكن':'Dark');try{localStorage.setItem('ehhub.theme',on?'dark':'light')}catch(e){}}
window.addEventListener('message',function(e){var m=e.data||{};if(m.ehhub==='lang'&&(m.lang==='ar'||m.lang==='en')&&m.lang!==LANG)setLang(m.lang);if(m.ehhub==='theme'&&(m.theme==='dark'||m.theme==='light')){if((m.theme==='dark')!==document.documentElement.classList.contains('dark'))toggleDark()}
  if(m.ehhub==='open-org'&&m.name){var p=ORGS.filter(function(x){return normq(x.name)===normq(m.name)||x._k.indexOf(normq(m.name))>=0})[0];if(p)pick(p.id)}});
try{if(localStorage.getItem('ehhub.theme')==='dark')toggleDark();var hl=localStorage.getItem('ehhub.lang');if(hl==='ar')LANG='ar'}catch(e){}
document.getElementById('q').addEventListener('input',function(){Q=this.value;renderList()});
setLang(LANG);
(function(){var m=/org=([^&]+)/.exec(location.hash||'');if(m){var id=decodeURIComponent(m[1]);if(ORGS.some(function(p){return p.id===id}))pick(id)}})();
</script>
<script src="eh-shared.js"></script>
</body>
</html>
'''

def main():
    src, out = sys.argv[1], sys.argv[2]
    data = json.load(open(src, encoding='utf-8'))
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html_out = TEMPLATE.replace('__DATA__', blob)
    open(out, 'w', encoding='utf-8').write(html_out)
    print(f'organisations page: {out} ({len(html_out)//1024} KB, {len(data["orgs"])} organisations)')

if __name__ == '__main__':
    main()
