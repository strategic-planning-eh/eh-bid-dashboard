"""patch_audit_shell_hub.py — hub shell (hub/EH_Hub.html): audit fixes shell-06, 07, 11, 12, 13, 17, 18, 21 (12 Oct 2026).

What was wrong, and what changes:
  shell-06  Phones: every News sub-page ran 57 px under the bottom tab bar, so its last lines could not be read.
            The News area now stops above the bar (portrait phones; landscape phones have no bar).
  shell-07  What's New: "Hub › Government Tenders" did nothing, and News links ("… › Environment Fund 2025 Report")
            opened Vision 2030. A link now opens the view it names — top tab or News sub-tab — and view names show in
            Arabic when the hub is in Arabic.
  shell-11  Footer said "three integrated views" (there are five) and stayed English in Arabic. Corrected and
            translated.
  shell-12  The "Loading …" spinners of the News sub-tabs sat behind the blank page and never showed. They now show
            while a sub-page loads.
  shell-13  Links such as #gov or #ef2025 opened the Stakeholder Map, the hub forgot the News sub-tab on reload, and
            changing the address did nothing. Now #<sub-tab> and #news/<sub-tab> open the right page, the last
            sub-tab is remembered on this device, and the address bar can switch views.
  shell-17  Arabic: hub title, "New" badges, footer, browser-tab title, button tooltips and screen-reader labels,
            What's New months/weeks/times, view and source names, the error message — all now follow the language.
            The Protected chip and the description show one language at a time (the mixed line read out of order).
  shell-18  Tablet (821–1100 px): the brand block wrapped to five lines. The subtitle and description are hidden at
            that width and the footer stays on one line, giving the views back about 90 px.
  shell-21  Company search: arrow keys now move through the results, Enter opens one, Escape closes the list; the
            list is announced as a list of options (combobox pattern).

Design system v2 (eh-shared.css tokens) is unchanged. Exact-string edits; stops if an anchor is missing.
Change table: change_table_audit_shell_hub.md/.json.   Run once:  python3 pipeline/patch_audit_shell_hub.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

H = os.path.join(HERE, '..', 'hub', 'EH_Hub.html')
if 'function hubRoute(' in open(H, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(H, 'hub')

# ---------------------------------------------------------------- CSS (end of the v2 skin)
rep('hub', '''  html:not([data-eh-motion="off"]) .tab{transition:background-color var(--eh-dur-1) var(--eh-ease),color var(--eh-dur-1) var(--eh-ease)}
}
</style>''', '''  html:not([data-eh-motion="off"]) .tab{transition:background-color var(--eh-dur-1) var(--eh-ease),color var(--eh-dur-1) var(--eh-ease)}
}
/* audit shell-06: on portrait phones the News area ends above the fixed bottom tab bar */
@media(max-width:640px) and (min-height:521px){#newswrap{bottom:calc(56px + env(safe-area-inset-bottom)) !important}}
/* audit shell-17: the Protected chip and the description show the hub's language only (mixed runs read out of order) */
html:not([lang=ar]) .conf [lang=ar],html:not([lang=ar]) .desc [lang=ar],.conf .dsep,.desc .dsep{display:none !important}
html[lang=ar] .conf [dir=ltr],html[lang=ar] .desc [dir=ltr]{display:none !important}
html[lang=ar] .conf span[lang=ar]{display:inline}
/* audit shell-18: tablets — one-line brand block and footer so the views keep their height */
@media(min-width:821px) and (max-width:1100px){.brand small,.brand .desc{display:none !important}.brand h1,body.dark .brand h1{font-size:17px}.foot{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
/* audit shell-21: the result picked with the arrow keys */
#qdrop .qh.act{background:var(--eh-tint) !important}
</style>''', 'css', 'shell-06/17/18/21: News area above the phone bar; one-language chip; tablet header; active search result')

# ---------------------------------------------------------------- header and labels (shell-17)
rep('hub', '<div class="brand"><h1>Strategic Intelligence <b>Hub</b></h1>',
    '<div class="brand"><h1><span class="tl" data-en="Strategic Intelligence &lt;b&gt;Hub&lt;/b&gt;" data-ar="منصة &lt;b&gt;الاستخبارات الاستراتيجية&lt;/b&gt;">Strategic Intelligence <b>Hub</b></span></h1>',
    'copy', 'shell-17: hub title in Arabic (same name as the sign-in page)')
rep('hub', '<span class="conf" role="note" title="Restricted — access authorised by EH management only">',
    '<span class="conf" role="note" title="Restricted — access authorised by EH management only" data-tt-en="Restricted — access authorised by EH management only" data-tt-ar="مقيّد — الوصول بإذن إدارة آفاق البيئة فقط">',
    'copy', 'shell-17: Protected chip tooltip in Arabic')
rep('hub', '''<input id="q" type="search" placeholder="Find a company… / ابحث عن شركة" autocomplete="off" aria-label="Global company search"''',
    '''<input id="q" type="search" placeholder="Find a company… / ابحث عن شركة" autocomplete="off" aria-label="Global company search" data-al-en="Find a company across the hub" data-al-ar="ابحث عن شركة في المنصة" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="qdrop"''',
    'a11y', 'shell-17/21: search box is a combobox with a bilingual label')
rep('hub', '''<div id="qdrop" style="display:none;''', '''<div id="qdrop" role="listbox" aria-label="Companies" style="display:none;''', 'a11y', 'shell-21: result list is a listbox')
rep('hub', '''title="What's New" style="position:relative">''', '''title="What's New" data-tt-en="What's New" data-tt-ar="ما الجديد" style="position:relative">''', 'copy', 'shell-17: What\'s New tooltip')
rep('hub', '''<button id="themebtn" class="hbtn" onclick="hubTheme()" title="Toggle dark theme across all views" aria-label="Toggle dark theme">''',
    '''<button id="themebtn" class="hbtn" onclick="hubTheme()" title="Toggle dark theme across all views" aria-label="Toggle dark theme" data-tt-en="Switch every view between light and dark" data-tt-ar="التبديل بين الوضع الفاتح والداكن في كل اللوحات" data-al-en="Switch light or dark theme" data-al-ar="تبديل الوضع الفاتح أو الداكن">''',
    'copy', 'shell-17: theme button tooltip and label in Arabic')
rep('hub', '''<button id="langbtn" onclick="hubLang()" title="Switch language across all views"''',
    '''<button id="langbtn" onclick="hubLang()" title="Switch language across all views" data-tt-en="Switch every view to Arabic" data-tt-ar="تحويل كل اللوحات إلى الإنجليزية"''', 'copy', 'shell-17: language button tooltip')
rep('hub', '''<button onclick="hubFS()" title="Presentation mode (fullscreen)" aria-label="Fullscreen current view"''',
    '''<button onclick="hubFS()" title="Presentation mode (fullscreen)" aria-label="Fullscreen current view" data-tt-en="Presentation mode (full screen)" data-tt-ar="وضع العرض (ملء الشاشة)" data-al-en="Show the current view full screen" data-al-ar="عرض اللوحة الحالية بملء الشاشة"''',
    'copy', 'shell-17: full-screen button tooltip and label')
rep('hub', '''<button class="wnx" onclick="wnClose()" aria-label="Close What's New">''',
    '''<button class="wnx" onclick="wnClose()" aria-label="Close What's New" data-al-en="Close What's New" data-al-ar="إغلاق ما الجديد">''', 'a11y', 'shell-17: close button label')
rep('hub', '<span class="newb" data-new-until="2026-10-13" aria-label="New">New</span>',
    '<span class="newb tl" data-new-until="2026-10-13" data-en="New" data-ar="جديد">New</span>', 'copy', 'shell-17: "New" badge in Arabic (Regulatory news)')
rep('hub', '<span class="newb" data-new-until="2026-10-06" aria-label="New">New</span>',
    '<span class="newb tl" data-new-until="2026-10-06" data-en="New" data-ar="جديد">New</span>', 'copy', 'shell-17: "New" badges in Arabic (PIF Strategy, EF report)', count=2)

rep('hub', '<b dir="ltr" id="freshv"></b>', '<b id="freshv"></b>', 'copy', 'shell-17: the refresh time reads in Arabic order (it is now written in Arabic)')
rep('hub', """L('Data refreshed','آخر تحديث للبيانات')+' <b dir="ltr">'+fmtFresh(FRESH_ISO)+'</b>'""", """L('Data refreshed','آخر تحديث للبيانات')+' <b>'+fmtFresh(FRESH_ISO)+'</b>'""",
    'copy', 'shell-17: same in the What\'s New panel')

# ---------------------------------------------------------------- footer (shell-11, 17, 18)
rep('hub', '<div class="foot">One link · three integrated views · bid data auto-refreshes hourly from the live tracker · stakeholder &amp; client data rebuilt from source workbooks on commit</div>',
    '<div class="foot"><span class="tl" data-en="Five live views · bids refresh hourly from the live tracker · stakeholder and client data update when their source workbooks do" '
    'data-ar="خمس لوحات حيّة · تُحدَّث العطاءات كل ساعة من جدول التتبع · وتُحدَّث بيانات أصحاب المصلحة والعملاء عند تحديث مصنّفاتها">'
    'Five live views · bids refresh hourly from the live tracker · stakeholder and client data update when their source workbooks do</span></div>',
    'copy', 'shell-11: footer counts five views and is translated')

# ---------------------------------------------------------------- go(): title, skeletons, News sub-tab last (shell-12, 13, 17)
rep('hub', '''  if(isNews) nGo(document.querySelector('.nsub.on')||document.querySelector('.nsub'));
  document.querySelectorAll('.skel').forEach(s=>s.style.zIndex=(s.id==='sk-'+btn.dataset.f)?4:-1);
  document.title='EH Hub — '+btn.dataset.t;
  try{history.replaceState(null,'','#'+btn.dataset.f);localStorage.setItem('ehhub.tab',btn.dataset.f);}catch(e){}
}''', '''  document.querySelectorAll('.skel').forEach(s=>s.style.zIndex=(s.id==='sk-'+btn.dataset.f)?4:-1);
  hubTitle();
  try{history.replaceState(null,'','#'+btn.dataset.f);localStorage.setItem('ehhub.tab',btn.dataset.f);}catch(e){}
  if(isNews) nGo(document.querySelector('.nsub.on')||document.querySelector('.nsub'));   // after the skeleton reset, so the sub-tab spinner stays on top
}
// browser-tab title in the hub's language (audit shell-17)
function hubTitle(){var b=document.querySelector('.tab.on'),t=b&&b.querySelector('.tl');document.title=L('EH Hub — ','منصة آفاق البيئة — ')+(t?(hubL==='ar'?t.dataset.ar:t.dataset.en):'');}''',
    'code', 'shell-12/13/17: News sub-tab chosen after the skeleton reset; title follows the language')
rep('hub', '''  d.textContent='This view failed to load — check that its file is published in the site build.';''',
    '''  d.textContent=L('This view failed to load — check that its file is published in the site build.','تعذّر تحميل هذه اللوحة — تأكّد من نشر ملفها في بناء الموقع.');''', 'copy', 'shell-17: error message in Arabic')

# ---------------------------------------------------------------- deep links (shell-13)
rep('hub', '''(function(){
  var want=(location.hash||'').replace('#','')||null;
  try{ want=want||localStorage.getItem('ehhub.tab'); }catch(e){}
  if(want&&want!=='stake'){ var b=document.querySelector('.tab[data-f="'+want+'"]'); if(b) go(b); }
})();''', '''// #bids, #news, #news/<sub-tab> or a bare sub-tab id such as #gov or #ef2025 (audit shell-13)
function hubRoute(h){
  h=String(h||'').replace(/^#/,''); if(!h) return false;
  var p=h.split('/'), sub=document.querySelector('.nsub[data-n="'+(p[1]||p[0])+'"]');
  if(sub){ document.querySelectorAll('.nsub').forEach(function(x){x.classList.toggle('on',x===sub);}); go(document.querySelector('.tab[data-f="news"]')); return true; }
  var b=document.querySelector('.tab[data-f="'+p[0]+'"]'); if(b){ go(b); return true; } return false;
}
(function(){
  var want=(location.hash||'').replace('#','')||null, st=null, ss=null;
  try{ st=localStorage.getItem('ehhub.tab'); ss=localStorage.getItem('ehhub.sub'); }catch(e){}
  if(!want&&st) want=(st==='news'&&ss)?'news/'+ss:st;
  if(want&&want!=='stake') hubRoute(want);
})();
window.addEventListener('hashchange',function(){ hubRoute(location.hash); });''', 'code', 'shell-13: deep links to News sub-tabs, remembered sub-tab, address-bar changes')

# ---------------------------------------------------------------- search keyboard (shell-21)
rep('hub', '''  if(!v||!QN){ qD.style.display='none'; return; }''', '''  if(!v||!QN){ qHide(); return; }''', 'a11y', 'shell-21: one place closes the list')
rep('hub', '''  if(!hits.length){ qD.style.display='none'; return; }
  qD.innerHTML=hits.map(function(n){return '<div class="qh" tabindex="0" onkeydown="if(event.keyCode===13){this.click()}" style="padding:8px 12px;cursor:pointer;font-size:12.5px;border-bottom:1px solid #F0F4F7" onclick="qGo(this.textContent)">'+n.replace(/</g,'&lt;')+'</div>';}).join('');
  qD.style.display='block';
});
document.addEventListener('click',function(e){ if(!e.target.closest('#hsearch')) qD.style.display='none'; });
function qGo(name){
  qD.style.display='none'; qEl.value=name;''', '''  if(!hits.length){ qHide(); return; }
  qD.innerHTML=hits.map(function(n,i){return '<div class="qh" id="qopt'+i+'" role="option" aria-selected="false" tabindex="-1" style="padding:8px 12px;cursor:pointer;font-size:12.5px;border-bottom:1px solid #F0F4F7" onclick="qGo(this.textContent)">'+n.replace(/</g,'&lt;')+'</div>';}).join('');
  qD.style.display='block'; qEl.setAttribute('aria-expanded','true'); qIdx=-1; qEl.removeAttribute('aria-activedescendant');
});
// combobox keys: Up/Down move through the results, Enter opens one, Escape closes the list (audit shell-21)
var qIdx=-1;
function qHide(){ qD.style.display='none'; qEl.setAttribute('aria-expanded','false'); qEl.removeAttribute('aria-activedescendant'); qIdx=-1; }
function qSet(i){ var o=qD.querySelectorAll('.qh'); if(!o.length) return; qIdx=(i+o.length)%o.length;
  o.forEach(function(x,j){ x.classList.toggle('act',j===qIdx); x.setAttribute('aria-selected',j===qIdx?'true':'false'); });
  qEl.setAttribute('aria-activedescendant',o[qIdx].id); if(o[qIdx].scrollIntoView) o[qIdx].scrollIntoView({block:'nearest'}); }
qEl.addEventListener('keydown',function(e){ var open=qD.style.display==='block';
  if(e.key==='ArrowDown'&&open){ qSet(qIdx+1); e.preventDefault(); }
  else if(e.key==='ArrowUp'&&open){ qSet(qIdx<0?-1:qIdx-1); e.preventDefault(); }
  else if(e.key==='Enter'&&open&&qIdx>-1){ qGo(qD.querySelectorAll('.qh')[qIdx].textContent); e.preventDefault(); }
  else if(e.key==='Escape'&&open){ qHide(); e.preventDefault(); } });
document.addEventListener('click',function(e){ if(!e.target.closest('#hsearch')) qHide(); });
function qGo(name){
  qHide(); qEl.value=name;''', 'a11y', 'shell-21: combobox keyboard pattern')

# ---------------------------------------------------------------- What's New: links, Arabic months/times/views/sources (shell-07, 17)
rep('hub', '''var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];''',
    '''var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], MONAR=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
function mon(i){return hubL==='ar'?MONAR[i]:MON[i];}''', 'copy', 'shell-17: Arabic month names for What\'s New')
rep('hub', '''var APPTAB={stake:'stake',map:'stake',bids:'bids',clients:'bubbles',news:'news',hub:null};''',
    '''var APPTAB={stake:'stake',map:'stake',bids:'bids',tenders:'tenders',clients:'bubbles',news:'news',hub:null};
APPS.tenders=['Government Tenders','المنافسات الحكومية'];
// a What's New "view" names a top tab or a News sub-tab by its English label (older names kept as aliases) — audit shell-07
var VIEWALIAS={'saudi fiscal monitor 2026':'fiscal','fiscal monitor':'fiscal','saudi government finances':'fiscal','government news':'gov','regulatory news':'gov','corporate news':'corp','pif strategy':'strat','pif hub':'pif','environment fund':'ef2025','environment fund 2025 report':'ef2025','etimad':'tenders','government tenders':'tenders','vision 2030':'v2030','client bubble map':'bubbles','clients':'bubbles','stakeholder map':'stake','bid intelligence':'bids'};
function wnView(v){ v=String(v||'').trim().toLowerCase(); if(!v) return null; var hit=null;
  document.querySelectorAll('.nsub,nav[aria-label] .tab').forEach(function(b){ var t=b.querySelector('.tl'); if(!hit&&t&&t.dataset.en.toLowerCase()===v) hit=b; });
  if(!hit){ var k=Object.keys(VIEWALIAS).find(function(a){return v===a||v.indexOf(a)===0;}); if(k) hit=document.querySelector('.nsub[data-n="'+VIEWALIAS[k]+'"]')||document.querySelector('nav[aria-label] .tab[data-f="'+VIEWALIAS[k]+'"]'); }
  return hit; }
// view names inside an app, in the words each app already uses in Arabic
var VIEWAR={'executive summary':'الملخّص التنفيذي','executive':'الملخّص التنفيذي','pricing intelligence':'تحليل الأسعار','bid turnaround':'مدة اتخاذ القرار','all tenders':'جميع المنافسات','overview':'نظرة عامة','regional view':'العرض الإقليمي','methodology':'المنهجية','data':'البيانات','header':'رأس الصفحة','filters':'المرشحات',"what's new":'ما الجديد','all views':'كل اللوحات','ios':'أجهزة iOS','mobile':'الهاتف','dark mode':'الوضع الداكن','scoring':'التقييم','revenue bridge':'جسر الإيرادات','bid view':'عرض العطاءات','map':'الخريطة','bid & tender':'المناقصات والعطاءات'};
function viewName(v){ var b=wnView(v), t=b&&b.querySelector('.tl'); if(t) return hubL==='ar'?t.dataset.ar:t.dataset.en; return hubL==='ar'?(VIEWAR[String(v).trim().toLowerCase()]||v):v; }''',
    'code', 'shell-07: tenders app; view names resolve to a tab or News sub-tab')
rep('hub', '''function fmtFresh(iso){var d=new Date(iso);if(isNaN(d))return String(iso||'').slice(0,16);var _r=fmtFresh0(d);return _r?_r+' KSA':_r;}
function fmtFresh0(d){var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Riyadh',day:'numeric',month:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(d),o={};f.forEach(function(x){o[x.type]=x.value;});return (+o.day)+' '+MON[+o.month-1]+' \\u00b7 '+o.hour+':'+o.minute;}
function fmtD(x){var d=new Date(x+'T12:00:00');return isNaN(d)?x:d.getUTCDate()+' '+MON[d.getUTCMonth()];}''',
    '''function fmtFresh(iso){var d=new Date(iso);if(isNaN(d))return String(iso||'').slice(0,16);var _r=fmtFresh0(d);return _r?_r+L(' KSA',' بتوقيت السعودية'):_r;}
function fmtFresh0(d){var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Riyadh',day:'numeric',month:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(d),o={};f.forEach(function(x){o[x.type]=x.value;});return (+o.day)+' '+mon(+o.month-1)+' \\u00b7 '+o.hour+':'+o.minute;}
function fmtD(x){var d=new Date(x+'T12:00:00');return isNaN(d)?x:d.getUTCDate()+' '+mon(d.getUTCMonth());}
function wkName(w){return hubL==='ar'?'الأسبوع '+(+String(w).split('-W')[1]||w):w;}''', 'copy', 'shell-17: dates and times in Arabic')
rep('hub', '''<span dir="ltr">'+MON[mi]+' '+y+'</span>''', '''<span>'+mon(mi)+' <span dir="ltr">'+y+'</span></span>''', 'copy', 'shell-17: month chips in Arabic')
rep('hub', '''<span dir="ltr">'+wnEsc(w.week)+'</span> \\u00b7 <span dir="ltr">'+wnEsc(fmtD(w.from))+'\\u2013'+wnEsc(fmtD(w.to))+'</span>''',
    '''<span>'+wnEsc(wkName(w.week))+'</span> \\u00b7 <span>'+wnEsc(fmtD(w.from))+' \\u2013 '+wnEsc(fmtD(w.to))+'</span>''', 'copy', 'shell-17: week chips in Arabic')
rep('hub', '''function wnGoApp(a){ wnClose(); var t=APPTAB[a]; if(t) go(document.querySelector('.tab[data-f="'+t+'"]')); }''',
    '''function wnGoApp(a,i){ wnClose(); var f=(i!=null&&WN&&WN.weeks[wnWeek])?(WN.weeks[wnWeek].fixes||[])[i]:null, b=f&&f.view?wnView(f.view):null;
  if(b&&b.classList.contains('nsub')){ hubRoute('news/'+b.dataset.n); return; }
  if(b){ go(b); return; }
  var t=APPTAB[a]; if(t) go(document.querySelector('.tab[data-f="'+t+'"]')); }''', 'code', 'shell-07: a fix link opens the view it names')
rep('hub', '''h=(w.fixes||[]).map(function(f){return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\\''+wnEsc(f.app)+'\\')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \\u203a '+wnEsc(f.view):'')+'</button>''',
    '''h=(w.fixes||[]).map(function(f,i){return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\\''+wnEsc(f.app)+'\\','+i+')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \\u203a '+wnEsc(viewName(f.view)):'')+'</button>''',
    'code', 'shell-07/17: fix links carry their view; view names in Arabic')
rep('hub', '''h=(w.sources||[]).map(function(x){return '<div class="wnitem"><b>'+wnEsc(x.name)+'</b><br>'+L('Refreshed','آخر تحديث')+' <span dir="ltr">'+wnEsc(x.refreshed?fmtFresh(x.refreshed):'\\u2014')+'</span>'+(x.note?' \\u00b7 '+wnEsc(x.note):'')+'</div>';}).join('')''',
    '''h=(w.sources||[]).map(function(x){var nt=L(x.note,x.note_ar||x.note);return '<div class="wnitem"><b>'+wnEsc(L(x.name,x.name_ar||x.name))+'</b><br>'+(x.refreshed?L('Refreshed','آخر تحديث')+' <span>'+wnEsc(/^\\d{4}-\\d{2}-\\d{2}$/.test(x.refreshed)?fmtD(x.refreshed):fmtFresh(x.refreshed))+'</span>':'')+(nt?(x.refreshed?' \\u00b7 ':'')+wnEsc(nt):'')+'</div>';}).join('')''',
    'copy', 'shell-10/17: source names and notes in Arabic; no "Refreshed —" line without a date')
rep('hub', '''+L('Built','بُني')+' <span dir="ltr">'+wnEsc(w.built?fmtFresh(w.built):'')+'</span></div>';''',
    '''+L('Built','بُني')+' <span>'+wnEsc(w.built?fmtFresh(w.built):'')+'</span></div>';''', 'copy', 'shell-17: build time reads in Arabic order')

# ---------------------------------------------------------------- News sub-tabs: spinner, memory (shell-12, 13)
rep('hub', '''  const id=btn.dataset.n;
  ['v2030','fiscal','corp','gov','pif','strat','ef2025'].forEach(k=>{
    const f=$('f-'+k);
    const on=k===id;
    if(on&&!f.src&&f.dataset.src){f.src=f.dataset.src;$('sk-'+k).classList.add('on');''', '''  const id=btn.dataset.n;
  try{history.replaceState(null,'','#news/'+id);localStorage.setItem('ehhub.sub',id);}catch(e){}   // audit shell-13: shareable link, remembered on this device
  ['v2030','fiscal','corp','gov','pif','strat','ef2025'].forEach(k=>{
    const f=$('f-'+k);
    const on=k===id;
    const sk=$('sk-'+k); if(sk) sk.style.zIndex=on?4:-1;   // audit shell-12: the loading spinner sits above the blank page
    if(on&&!f.src&&f.dataset.src){f.src=f.dataset.src;$('sk-'+k).classList.add('on');''', 'code', 'shell-12/13: spinner visible while a sub-page loads; sub-tab in the address and remembered')

# ---------------------------------------------------------------- relabel(): attributes, title, freshness (shell-17)
rep('hub', '''  document.querySelectorAll('.tl').forEach(el=>{
    el.innerHTML=hubL==='ar'?el.dataset.ar:el.dataset.en;
  });''', '''  document.querySelectorAll('.tl').forEach(el=>{
    el.innerHTML=hubL==='ar'?el.dataset.ar:el.dataset.en;
  });
  document.querySelectorAll('[data-tt-en]').forEach(el=>{el.title=hubL==='ar'?el.dataset.ttAr:el.dataset.ttEn;});      // tooltips (audit shell-17)
  document.querySelectorAll('[data-al-en]').forEach(el=>{el.setAttribute('aria-label',hubL==='ar'?el.dataset.alAr:el.dataset.alEn);});
  if(typeof hubTitle==='function'&&document.querySelector('.tab.on')) hubTitle();
  if(typeof FRESH_ISO!=='undefined'&&FRESH_ISO&&$('freshv')) $('freshv').textContent=fmtFresh(FRESH_ISO);''', 'copy', 'shell-17: tooltips, labels, tab title and refresh time follow the language')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(H, 'w', encoding='utf-8').write(FILES['hub'])
write_change_table(os.path.join(HERE, 'change_table_audit_shell_hub'), 'Hub shell — audit fixes shell-06/07/11/12/13/17/18/21')
print('patched: hub/EH_Hub.html')
