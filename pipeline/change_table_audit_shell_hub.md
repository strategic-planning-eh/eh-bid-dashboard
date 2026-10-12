# Hub shell — audit fixes shell-06/07/11/12/13/17/18/21

Generated 2026-10-12 14:46 · 31 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | hub | exact | css | shell-06/17/18/21: News area above the phone bar; one-language chip; tablet header; active search result | 1 | ✓ |
| 2 | hub | exact | copy | shell-17: hub title in Arabic (same name as the sign-in page) | 1 | ✓ |
| 3 | hub | exact | copy | shell-17: Protected chip tooltip in Arabic | 1 | ✓ |
| 4 | hub | exact | a11y | shell-17/21: search box is a combobox with a bilingual label | 1 | ✓ |
| 5 | hub | exact | a11y | shell-21: result list is a listbox | 1 | ✓ |
| 6 | hub | exact | copy | shell-17: What's New tooltip | 1 | ✓ |
| 7 | hub | exact | copy | shell-17: theme button tooltip and label in Arabic | 1 | ✓ |
| 8 | hub | exact | copy | shell-17: language button tooltip | 1 | ✓ |
| 9 | hub | exact | copy | shell-17: full-screen button tooltip and label | 1 | ✓ |
| 10 | hub | exact | a11y | shell-17: close button label | 1 | ✓ |
| 11 | hub | exact | copy | shell-17: "New" badge in Arabic (Regulatory news) | 1 | ✓ |
| 12 | hub | exact | copy | shell-17: "New" badges in Arabic (PIF Strategy, EF report) | 2 | ✓ |
| 13 | hub | exact | copy | shell-17: the refresh time reads in Arabic order (it is now written in Arabic) | 1 | ✓ |
| 14 | hub | exact | copy | shell-17: same in the What's New panel | 1 | ✓ |
| 15 | hub | exact | copy | shell-11: footer counts five views and is translated | 1 | ✓ |
| 16 | hub | exact | code | shell-12/13/17: News sub-tab chosen after the skeleton reset; title follows the language | 1 | ✓ |
| 17 | hub | exact | copy | shell-17: error message in Arabic | 1 | ✓ |
| 18 | hub | exact | code | shell-13: deep links to News sub-tabs, remembered sub-tab, address-bar changes | 1 | ✓ |
| 19 | hub | exact | a11y | shell-21: one place closes the list | 1 | ✓ |
| 20 | hub | exact | a11y | shell-21: combobox keyboard pattern | 1 | ✓ |
| 21 | hub | exact | copy | shell-17: Arabic month names for What's New | 1 | ✓ |
| 22 | hub | exact | code | shell-07: tenders app; view names resolve to a tab or News sub-tab | 1 | ✓ |
| 23 | hub | exact | copy | shell-17: dates and times in Arabic | 1 | ✓ |
| 24 | hub | exact | copy | shell-17: month chips in Arabic | 1 | ✓ |
| 25 | hub | exact | copy | shell-17: week chips in Arabic | 1 | ✓ |
| 26 | hub | exact | code | shell-07: a fix link opens the view it names | 1 | ✓ |
| 27 | hub | exact | code | shell-07/17: fix links carry their view; view names in Arabic | 1 | ✓ |
| 28 | hub | exact | copy | shell-10/17: source names and notes in Arabic; no "Refreshed —" line without a date | 1 | ✓ |
| 29 | hub | exact | copy | shell-17: build time reads in Arabic order | 1 | ✓ |
| 30 | hub | exact | code | shell-12/13: spinner visible while a sub-page loads; sub-tab in the address and remembered | 1 | ✓ |
| 31 | hub | exact | copy | shell-17: tooltips, labels, tab title and refresh time follow the language | 1 | ✓ |

## Edit detail

### 1. hub — shell-06/17/18/21: News area above the phone bar; one-language chip; tablet header; active search result

**Old**
```
  html:not([data-eh-motion="off"]) .tab{transition:background-color var(--eh-dur-1) var(--eh-ease),color var(--eh-dur-1) var(--eh-ease)}
}
</style>
```
**New**
```
  html:not([data-eh-motion="off"]) .tab{transition:background-color var(--eh-dur-1) var(--eh-ease),color var(--eh-dur-1) var(--eh-ease)}
}
/* audit shell-06: on portrait phones the News area ends above the fixed bottom tab bar */
@media(max-width:640px) and (min-height:521px){#newswrap{bottom:calc(56px + env(safe-area-inset-bottom)) !important}}
/* audit shell-17: the Protected chip and the descri
```

### 2. hub — shell-17: hub title in Arabic (same name as the sign-in page)

**Old**
```
<div class="brand"><h1>Strategic Intelligence <b>Hub</b></h1>
```
**New**
```
<div class="brand"><h1><span class="tl" data-en="Strategic Intelligence &lt;b&gt;Hub&lt;/b&gt;" data-ar="منصة &lt;b&gt;الاستخبارات الاستراتيجية&lt;/b&gt;">Strategic Intelligence <b>Hub</b></span></h1>
```

### 3. hub — shell-17: Protected chip tooltip in Arabic

**Old**
```
<span class="conf" role="note" title="Restricted — access authorised by EH management only">
```
**New**
```
<span class="conf" role="note" title="Restricted — access authorised by EH management only" data-tt-en="Restricted — access authorised by EH management only" data-tt-ar="مقيّد — الوصول بإذن إدارة آفاق البيئة فقط">
```

### 4. hub — shell-17/21: search box is a combobox with a bilingual label

**Old**
```
<input id="q" type="search" placeholder="Find a company… / ابحث عن شركة" autocomplete="off" aria-label="Global company search"
```
**New**
```
<input id="q" type="search" placeholder="Find a company… / ابحث عن شركة" autocomplete="off" aria-label="Global company search" data-al-en="Find a company across the hub" data-al-ar="ابحث عن شركة في المنصة" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="qdrop"
```

### 5. hub — shell-21: result list is a listbox

**Old**
```
<div id="qdrop" style="display:none;
```
**New**
```
<div id="qdrop" role="listbox" aria-label="Companies" style="display:none;
```

### 6. hub — shell-17: What's New tooltip

**Old**
```
title="What's New" style="position:relative">
```
**New**
```
title="What's New" data-tt-en="What's New" data-tt-ar="ما الجديد" style="position:relative">
```

### 7. hub — shell-17: theme button tooltip and label in Arabic

**Old**
```
<button id="themebtn" class="hbtn" onclick="hubTheme()" title="Toggle dark theme across all views" aria-label="Toggle dark theme">
```
**New**
```
<button id="themebtn" class="hbtn" onclick="hubTheme()" title="Toggle dark theme across all views" aria-label="Toggle dark theme" data-tt-en="Switch every view between light and dark" data-tt-ar="التبديل بين الوضع الفاتح والداكن في كل اللوحات" data-al-en="Switch light or dark theme" data-al-ar="تبديل الوضع الفاتح أو الداكن">
```

### 8. hub — shell-17: language button tooltip

**Old**
```
<button id="langbtn" onclick="hubLang()" title="Switch language across all views"
```
**New**
```
<button id="langbtn" onclick="hubLang()" title="Switch language across all views" data-tt-en="Switch every view to Arabic" data-tt-ar="تحويل كل اللوحات إلى الإنجليزية"
```

### 9. hub — shell-17: full-screen button tooltip and label

**Old**
```
<button onclick="hubFS()" title="Presentation mode (fullscreen)" aria-label="Fullscreen current view"
```
**New**
```
<button onclick="hubFS()" title="Presentation mode (fullscreen)" aria-label="Fullscreen current view" data-tt-en="Presentation mode (full screen)" data-tt-ar="وضع العرض (ملء الشاشة)" data-al-en="Show the current view full screen" data-al-ar="عرض اللوحة الحالية بملء الشاشة"
```

### 10. hub — shell-17: close button label

**Old**
```
<button class="wnx" onclick="wnClose()" aria-label="Close What's New">
```
**New**
```
<button class="wnx" onclick="wnClose()" aria-label="Close What's New" data-al-en="Close What's New" data-al-ar="إغلاق ما الجديد">
```

### 11. hub — shell-17: "New" badge in Arabic (Regulatory news)

**Old**
```
<span class="newb" data-new-until="2026-10-13" aria-label="New">New</span>
```
**New**
```
<span class="newb tl" data-new-until="2026-10-13" data-en="New" data-ar="جديد">New</span>
```

### 12. hub — shell-17: "New" badges in Arabic (PIF Strategy, EF report)

**Old**
```
<span class="newb" data-new-until="2026-10-06" aria-label="New">New</span>
```
**New**
```
<span class="newb tl" data-new-until="2026-10-06" data-en="New" data-ar="جديد">New</span>
```

### 13. hub — shell-17: the refresh time reads in Arabic order (it is now written in Arabic)

**Old**
```
<b dir="ltr" id="freshv"></b>
```
**New**
```
<b id="freshv"></b>
```

### 14. hub — shell-17: same in the What's New panel

**Old**
```
L('Data refreshed','آخر تحديث للبيانات')+' <b dir="ltr">'+fmtFresh(FRESH_ISO)+'</b>'
```
**New**
```
L('Data refreshed','آخر تحديث للبيانات')+' <b>'+fmtFresh(FRESH_ISO)+'</b>'
```

### 15. hub — shell-11: footer counts five views and is translated

**Old**
```
<div class="foot">One link · three integrated views · bid data auto-refreshes hourly from the live tracker · stakeholder &amp; client data rebuilt from source workbooks on commit</div>
```
**New**
```
<div class="foot"><span class="tl" data-en="Five live views · bids refresh hourly from the live tracker · stakeholder and client data update when their source workbooks do" data-ar="خمس لوحات حيّة · تُحدَّث العطاءات كل ساعة من جدول التتبع · وتُحدَّث بيانات أصحاب المصلحة والعملاء عند تحديث مصنّفاتها">Five live views · bids refresh hourly from the live tracker · stakeholder and client data update wh
```

### 16. hub — shell-12/13/17: News sub-tab chosen after the skeleton reset; title follows the language

**Old**
```
  if(isNews) nGo(document.querySelector('.nsub.on')||document.querySelector('.nsub'));
  document.querySelectorAll('.skel').forEach(s=>s.style.zIndex=(s.id==='sk-'+btn.dataset.f)?4:-1);
  document.title='EH Hub — '+btn.dataset.t;
  try{history.replaceState(null,'','#'+btn.dataset.f);localStorage.setItem('ehhub.tab',btn.dataset.f);}catch(e){}
}
```
**New**
```
  document.querySelectorAll('.skel').forEach(s=>s.style.zIndex=(s.id==='sk-'+btn.dataset.f)?4:-1);
  hubTitle();
  try{history.replaceState(null,'','#'+btn.dataset.f);localStorage.setItem('ehhub.tab',btn.dataset.f);}catch(e){}
  if(isNews) nGo(document.querySelector('.nsub.on')||document.querySelector('.nsub'));   // after the skeleton reset, so the sub-tab spinner stays on top
}
// browser-tab ti
```

### 17. hub — shell-17: error message in Arabic

**Old**
```
  d.textContent='This view failed to load — check that its file is published in the site build.';
```
**New**
```
  d.textContent=L('This view failed to load — check that its file is published in the site build.','تعذّر تحميل هذه اللوحة — تأكّد من نشر ملفها في بناء الموقع.');
```

### 18. hub — shell-13: deep links to News sub-tabs, remembered sub-tab, address-bar changes

**Old**
```
(function(){
  var want=(location.hash||'').replace('#','')||null;
  try{ want=want||localStorage.getItem('ehhub.tab'); }catch(e){}
  if(want&&want!=='stake'){ var b=document.querySelector('.tab[data-f="'+want+'"]'); if(b) go(b); }
})();
```
**New**
```
// #bids, #news, #news/<sub-tab> or a bare sub-tab id such as #gov or #ef2025 (audit shell-13)
function hubRoute(h){
  h=String(h||'').replace(/^#/,''); if(!h) return false;
  var p=h.split('/'), sub=document.querySelector('.nsub[data-n="'+(p[1]||p[0])+'"]');
  if(sub){ document.querySelectorAll('.nsub').forEach(function(x){x.classList.toggle('on',x===sub);}); go(document.querySelector('.tab[data-
```

### 19. hub — shell-21: one place closes the list

**Old**
```
  if(!v||!QN){ qD.style.display='none'; return; }
```
**New**
```
  if(!v||!QN){ qHide(); return; }
```

### 20. hub — shell-21: combobox keyboard pattern

**Old**
```
  if(!hits.length){ qD.style.display='none'; return; }
  qD.innerHTML=hits.map(function(n){return '<div class="qh" tabindex="0" onkeydown="if(event.keyCode===13){this.click()}" style="padding:8px 12px;cursor:pointer;font-size:12.5px;border-bottom:1px solid #F0F4F7" onclick="qGo(this.textContent)">'+n.replace(/</g,'&lt;')+'</div>';}).join('');
  qD.style.display='block';
});
document.addEventListen
```
**New**
```
  if(!hits.length){ qHide(); return; }
  qD.innerHTML=hits.map(function(n,i){return '<div class="qh" id="qopt'+i+'" role="option" aria-selected="false" tabindex="-1" style="padding:8px 12px;cursor:pointer;font-size:12.5px;border-bottom:1px solid #F0F4F7" onclick="qGo(this.textContent)">'+n.replace(/</g,'&lt;')+'</div>';}).join('');
  qD.style.display='block'; qEl.setAttribute('aria-expanded','true
```

### 21. hub — shell-17: Arabic month names for What's New

**Old**
```
var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
```
**New**
```
var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], MONAR=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
function mon(i){return hubL==='ar'?MONAR[i]:MON[i];}
```

### 22. hub — shell-07: tenders app; view names resolve to a tab or News sub-tab

**Old**
```
var APPTAB={stake:'stake',map:'stake',bids:'bids',clients:'bubbles',news:'news',hub:null};
```
**New**
```
var APPTAB={stake:'stake',map:'stake',bids:'bids',tenders:'tenders',clients:'bubbles',news:'news',hub:null};
APPS.tenders=['Government Tenders','المنافسات الحكومية'];
// a What's New "view" names a top tab or a News sub-tab by its English label (older names kept as aliases) — audit shell-07
var VIEWALIAS={'saudi fiscal monitor 2026':'fiscal','fiscal monitor':'fiscal','saudi government finances':'f
```

### 23. hub — shell-17: dates and times in Arabic

**Old**
```
function fmtFresh(iso){var d=new Date(iso);if(isNaN(d))return String(iso||'').slice(0,16);var _r=fmtFresh0(d);return _r?_r+' KSA':_r;}
function fmtFresh0(d){var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Riyadh',day:'numeric',month:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(d),o={};f.forEach(function(x){o[x.type]=x.value;});return (+o.day)+' '+MON[+o.month-1]+' \
```
**New**
```
function fmtFresh(iso){var d=new Date(iso);if(isNaN(d))return String(iso||'').slice(0,16);var _r=fmtFresh0(d);return _r?_r+L(' KSA',' بتوقيت السعودية'):_r;}
function fmtFresh0(d){var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Riyadh',day:'numeric',month:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(d),o={};f.forEach(function(x){o[x.type]=x.value;});return (+o.day)+'
```

### 24. hub — shell-17: month chips in Arabic

**Old**
```
<span dir="ltr">'+MON[mi]+' '+y+'</span>
```
**New**
```
<span>'+mon(mi)+' <span dir="ltr">'+y+'</span></span>
```

### 25. hub — shell-17: week chips in Arabic

**Old**
```
<span dir="ltr">'+wnEsc(w.week)+'</span> \u00b7 <span dir="ltr">'+wnEsc(fmtD(w.from))+'\u2013'+wnEsc(fmtD(w.to))+'</span>
```
**New**
```
<span>'+wnEsc(wkName(w.week))+'</span> \u00b7 <span>'+wnEsc(fmtD(w.from))+' \u2013 '+wnEsc(fmtD(w.to))+'</span>
```

### 26. hub — shell-07: a fix link opens the view it names

**Old**
```
function wnGoApp(a){ wnClose(); var t=APPTAB[a]; if(t) go(document.querySelector('.tab[data-f="'+t+'"]')); }
```
**New**
```
function wnGoApp(a,i){ wnClose(); var f=(i!=null&&WN&&WN.weeks[wnWeek])?(WN.weeks[wnWeek].fixes||[])[i]:null, b=f&&f.view?wnView(f.view):null;
  if(b&&b.classList.contains('nsub')){ hubRoute('news/'+b.dataset.n); return; }
  if(b){ go(b); return; }
  var t=APPTAB[a]; if(t) go(document.querySelector('.tab[data-f="'+t+'"]')); }
```

### 27. hub — shell-07/17: fix links carry their view; view names in Arabic

**Old**
```
h=(w.fixes||[]).map(function(f){return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\''+wnEsc(f.app)+'\')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \u203a '+wnEsc(f.view):'')+'</button>
```
**New**
```
h=(w.fixes||[]).map(function(f,i){return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\''+wnEsc(f.app)+'\','+i+')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \u203a '+wnEsc(viewName(f.view)):'')+'</button>
```

### 28. hub — shell-10/17: source names and notes in Arabic; no "Refreshed —" line without a date

**Old**
```
h=(w.sources||[]).map(function(x){return '<div class="wnitem"><b>'+wnEsc(x.name)+'</b><br>'+L('Refreshed','آخر تحديث')+' <span dir="ltr">'+wnEsc(x.refreshed?fmtFresh(x.refreshed):'\u2014')+'</span>'+(x.note?' \u00b7 '+wnEsc(x.note):'')+'</div>';}).join('')
```
**New**
```
h=(w.sources||[]).map(function(x){var nt=L(x.note,x.note_ar||x.note);return '<div class="wnitem"><b>'+wnEsc(L(x.name,x.name_ar||x.name))+'</b><br>'+(x.refreshed?L('Refreshed','آخر تحديث')+' <span>'+wnEsc(/^\d{4}-\d{2}-\d{2}$/.test(x.refreshed)?fmtD(x.refreshed):fmtFresh(x.refreshed))+'</span>':'')+(nt?(x.refreshed?' \u00b7 ':'')+wnEsc(nt):'')+'</div>';}).join('')
```

### 29. hub — shell-17: build time reads in Arabic order

**Old**
```
+L('Built','بُني')+' <span dir="ltr">'+wnEsc(w.built?fmtFresh(w.built):'')+'</span></div>';
```
**New**
```
+L('Built','بُني')+' <span>'+wnEsc(w.built?fmtFresh(w.built):'')+'</span></div>';
```

### 30. hub — shell-12/13: spinner visible while a sub-page loads; sub-tab in the address and remembered

**Old**
```
  const id=btn.dataset.n;
  ['v2030','fiscal','corp','gov','pif','strat','ef2025'].forEach(k=>{
    const f=$('f-'+k);
    const on=k===id;
    if(on&&!f.src&&f.dataset.src){f.src=f.dataset.src;$('sk-'+k).classList.add('on');
```
**New**
```
  const id=btn.dataset.n;
  try{history.replaceState(null,'','#news/'+id);localStorage.setItem('ehhub.sub',id);}catch(e){}   // audit shell-13: shareable link, remembered on this device
  ['v2030','fiscal','corp','gov','pif','strat','ef2025'].forEach(k=>{
    const f=$('f-'+k);
    const on=k===id;
    const sk=$('sk-'+k); if(sk) sk.style.zIndex=on?4:-1;   // audit shell-12: the loading spinner si
```

### 31. hub — shell-17: tooltips, labels, tab title and refresh time follow the language

**Old**
```
  document.querySelectorAll('.tl').forEach(el=>{
    el.innerHTML=hubL==='ar'?el.dataset.ar:el.dataset.en;
  });
```
**New**
```
  document.querySelectorAll('.tl').forEach(el=>{
    el.innerHTML=hubL==='ar'?el.dataset.ar:el.dataset.en;
  });
  document.querySelectorAll('[data-tt-en]').forEach(el=>{el.title=hubL==='ar'?el.dataset.ttAr:el.dataset.ttEn;});      // tooltips (audit shell-17)
  document.querySelectorAll('[data-al-en]').forEach(el=>{el.setAttribute('aria-label',hubL==='ar'?el.dataset.alAr:el.dataset.alEn);});
  if
```
