/* eh-shared.js — EH Hub shared behaviour layer · v1.0.0 · 2026-09-07
   Include with <script src="eh-shared.js" defer></script> after the page's own scripts.
   1. Embedded mode: adds html.eh-embedded (+ html.eh-page-<id>) when the page is inside the hub.
   2. Hub bridge: one listener for {ehhub:'lang'|'theme'} that calls whatever the page exposes,
      so every page follows the hub's buttons (D-B2).
   3. Motion (moderate, D-B7): KPI numbers count up once per session; Chart.js animates on first
      paint only; card grids stagger in. All off under prefers-reduced-motion or data-eh-motion="off".
   4. Text floor: nothing readable below 12px (adds html.eh-floor; CSS does the rest). */
(function(){
  'use strict';
  var html=document.documentElement;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var motion=!reduce&&html.getAttribute('data-eh-motion')!=='off';
  var file=(location.pathname.split('/').pop()||'').toLowerCase();
  var PAGE=/stakeholder/.test(file)?'stake':/bid_analysis/.test(file)?'bids':/bubble/.test(file)?'bub':/news_intelligence/.test(file)?'news':/vision2030/.test(file)?'v2030':/fiscal/.test(file)?'fisc':/pif_strategy/.test(file)?'strat':/pif_intelligence/.test(file)?'pif':'other';
  html.classList.add('eh-page-'+PAGE,'eh-floor');

  /* 1. embedded mode (D-B1) */
  var embedded=false; try{embedded=(window.parent!==window)||/[?&]embedded=1/.test(location.search);}catch(e){embedded=true;}
  if(embedded) html.classList.add('eh-embedded');

  /* 2. hub bridge — page-specific adapters. Each returns true if it handled the request. */
  /* Only the gaps are adapted here. Stakeholder, Bid and both PIF pages already listen for the hub's
     language message themselves; adapting them again would toggle twice. */
  var LANG={
    news:function(l){ if(typeof ehSetLang==='function'){ehSetLang(l);return true;} },
    fisc:function(l){ if(typeof ehSetLang==='function'){ehSetLang(l);return true;} },
    v2030:function(l){ if(typeof switchTab==='function'){switchTab(l==='ar'?'arabic':'dashboard');return true;} },
    bub:function(l){ if(typeof ehBubbleLang==='function'){ehBubbleLang(l);return true;} return false; }
  };
  var THEME={
    stake:function(t){ var dark=html.classList.contains('dark')||document.body.classList.contains('dark')||html.dataset.theme==='dark'; if((t==='dark')!==dark){ if(typeof toggleDark==='function'){toggleDark();return true;} } return true; }
  };
  function applyLangDir(l){ /* pages that swap content but forget direction (news, fisc) */
    if(PAGE==='news'||PAGE==='fisc'||PAGE==='v2030'){ html.lang=l; html.dir=(l==='ar'?'rtl':'ltr'); }
  }
  window.addEventListener('message',function(e){
    var d=e.data||{}; if(!d.ehhub)return;
    if(d.ehhub==='lang'&&(d.lang==='ar'||d.lang==='en')){ var f=LANG[PAGE]; try{ if(f)f(d.lang); }catch(err){} applyLangDir(d.lang); setTimeout(floorText,50); }
    if(d.ehhub==='theme'&&(d.theme==='dark'||d.theme==='light')){ var g=THEME[PAGE]; try{ if(g)g(d.theme); }catch(err){} }
  });
  /* when embedded, adopt the hub's current language and theme on load without waiting for a click */
  if(embedded){ try{ var hl=localStorage.getItem('ehhub.lang'), ht=localStorage.getItem('ehhub.theme');
    if(hl){ setTimeout(function(){ window.postMessage({ehhub:'lang',lang:hl},'*'); },300); }
    if(ht){ setTimeout(function(){ window.postMessage({ehhub:'theme',theme:ht},'*'); },300); } }catch(e){} }

  /* 3a. Chart.js: animate on first paint only, never on redraw/resize/theme (lesson #1) */
  function chartGuard(){
    if(!window.Chart||!Chart.defaults)return;
    if(!motion){ Chart.defaults.animation=false; return; }
    Chart.defaults.animation={duration:480,easing:'easeOutQuart'};
    Chart.defaults.responsive=true;
    if('transitions' in Chart.defaults){ Chart.defaults.transitions.resize={animation:{duration:0}}; }
    setTimeout(function(){ Chart.defaults.animation=false; },1600); /* after first paint, redraws are instant */
  }
  chartGuard(); window.addEventListener('load',chartGuard);

  /* 3b. KPI count-up, once per page per session */
  var KPI_SEL='.kpi .v,.kc .v,.metric .mv,.kval,.k-num,.a-num,.rnum,.value.num,.biz-kpi .v,.kpis .v,.kpi .val';
  function parseNum(s){ var m=s.replace(/[\u2066\u2069]/g,'').match(/^([^\d\-]*)(-?\d[\d,]*\.?\d*)(.*)$/); if(!m)return null; var n=parseFloat(m[2].replace(/,/g,'')); if(isNaN(n))return null; return {pre:m[1],n:n,post:m[3],dec:(m[2].split('.')[1]||'').length,comma:/,/.test(m[2])}; }
  function fmt(n,p){ var s=n.toFixed(p.dec); if(p.comma){ var parts=s.split('.'); parts[0]=parts[0].replace(/\B(?=(\d{3})+(?!\d))/g,','); s=parts.join('.'); } return s; }
  function countUp(){
    if(!motion)return; var key='eh.counted.'+PAGE; try{ if(sessionStorage.getItem(key))return; sessionStorage.setItem(key,'1'); }catch(e){}
    var els=[].slice.call(document.querySelectorAll(KPI_SEL)).slice(0,24);
    els.forEach(function(el){
      if(el.querySelector('*')&&el.children.length>1)return; var raw=el.textContent.trim(); var p=parseNum(raw); if(!p||p.n===0||raw.length>18)return;
      var final=raw, start=performance.now(), dur=520; el.setAttribute('aria-label',final);
      function step(t){ var k=Math.min(1,(t-start)/dur); k=1-Math.pow(1-k,3); var txt=p.pre+fmt(p.n*k,p)+p.post; if(el.children.length===0)el.textContent=txt; if(k<1)requestAnimationFrame(step); else if(el.children.length===0)el.textContent=final; }
      requestAnimationFrame(step);
    });
  }
  /* 3c. stagger card grids on first paint */
  function stagger(){ if(!motion)return; ['.kpis','.kgrid','.kpi-grid','.kpi-bar','.ecogrid','.metrics','.cards','.grid.cards'].forEach(function(sel){ var g=document.querySelector(sel); if(g&&!g.classList.contains('eh-stagger')&&g.children.length>1&&g.children.length<=16) g.classList.add('eh-stagger'); }); }

  /* 4. text floor: bump computed sizes below 12px on text-bearing elements (once, and after language switch) */
  function floorText(){
    var n=0; var els=document.querySelectorAll('p,td,th,li,span,div,small,label,a,button,caption,dt,dd');
    for(var i=0;i<els.length&&n<400;i++){ var el=els[i]; if(!el.childNodes.length||el.closest('svg,canvas'))continue; var hasText=false; for(var c=0;c<el.childNodes.length;c++){ if(el.childNodes[c].nodeType===3&&el.childNodes[c].textContent.trim().length>2){hasText=true;break;} } if(!hasText)continue; var fs=parseFloat(getComputedStyle(el).fontSize); if(fs&&fs<12){ el.style.fontSize='12px'; n++; } }
  }
  function ready(fn){ if(document.readyState==='complete')setTimeout(fn,60); else window.addEventListener('load',function(){setTimeout(fn,60);}); }
  ready(function(){ stagger(); countUp(); floorText(); setTimeout(floorText,1500); });
  window.EH_SHARED={version:'1.0.0',page:PAGE,embedded:embedded,motion:motion,floorText:floorText};
})();
