/* eh-shared.js — EH Hub shared behaviour layer · v1.1.0 · 2026-09-08
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
  /* 3d. Bid dashboard transitions (moderate motion, transform-based so they hold at any width).
     - Year toggle (2025 / 2026 / Both): cards FLIP to their new positions, KPI numbers count from the OLD value to the
       NEW one, SVG bars/arcs morph from their previous geometry when the chart shape is unchanged (else they build in),
       horizontal bar divs grow from the start edge.
     - Pricing intelligence: the tender card you tap slides open, its bidder bars grow in one after another, and the
       cards below glide down instead of jumping. Works for "expand all" too.
     Everything wraps the page's own functions; nothing in the page is changed. */
  var BAR_SEL='div[style*="height:15px"],div[style*="height:14px"],div[style*="height:12px"],.bar>i,.bar>span';
  function snapRects(root){ var out=[]; root.querySelectorAll('.card').forEach(function(el){ var r=el.getBoundingClientRect(); out.push({el:el,top:r.top,left:r.left,w:r.width}); }); return out; }
  function flipCards(before,root){
    if(!motion)return; var after=snapRects(root); var byIdx=Math.min(before.length,after.length);
    for(var i=0;i<byIdx;i++){ var b=before[i],a=after[i]; if(!a.el.isConnected||a.el.getBoundingClientRect().height===0)continue; var dy=b.top-a.top, dx=b.left-a.left;
      if(Math.abs(dy)<1&&Math.abs(dx)<1)continue; var el=a.el; el.style.transition='none'; el.style.transform='translate('+dx+'px,'+dy+'px)'; el.style.willChange='transform';
      (function(el){ requestAnimationFrame(function(){ el.style.transition='transform 420ms cubic-bezier(.2,.7,.2,1)'; el.style.transform=''; setTimeout(function(){ el.style.transition='';el.style.willChange=''; },460); }); })(el); }
  }
  function snapSvg(root){ var m={}; root.querySelectorAll('svg').forEach(function(svg,si){ m[si]=[].map.call(svg.querySelectorAll('rect,circle,path'),function(n){ return {tag:n.tagName,x:+n.getAttribute('x')||0,y:+n.getAttribute('y')||0,w:+n.getAttribute('width')||0,h:+n.getAttribute('height')||0,r:+n.getAttribute('r')||0,cx:+n.getAttribute('cx')||0,cy:+n.getAttribute('cy')||0,d:n.getAttribute('d')||''}; }); }); return m; }
  function morphSvg(before,root){
    if(!motion)return; root.querySelectorAll('svg').forEach(function(svg,si){ var old=before[si]; var nodes=svg.querySelectorAll('rect,circle,path'); var same=old&&old.length===nodes.length;
      nodes.forEach(function(n,i){ var tag=n.tagName; var o=same?old[i]:null;
        if(tag==='rect'&&o&&o.tag==='rect'){ var tx=+n.getAttribute('x')||0,ty=+n.getAttribute('y')||0,tw=+n.getAttribute('width')||0,th=+n.getAttribute('height')||0; if(o.x===tx&&o.y===ty&&o.w===tw&&o.h===th)return; var st=performance.now();
          (function step(t){ var k=Math.min(1,(t-st)/520); k=1-Math.pow(1-k,3); n.setAttribute('x',o.x+(tx-o.x)*k); n.setAttribute('y',o.y+(ty-o.y)*k); n.setAttribute('width',Math.max(0,o.w+(tw-o.w)*k)); n.setAttribute('height',Math.max(0,o.h+(th-o.h)*k)); if(k<1)requestAnimationFrame(step); })(st); }
        else if(tag==='circle'&&o&&o.tag==='circle'){ var tr=+n.getAttribute('r')||0; if(o.r===tr)return; var st2=performance.now(); (function step(t){ var k=Math.min(1,(t-st2)/520); n.setAttribute('r',o.r+(tr-o.r)*k); if(k<1)requestAnimationFrame(step); })(st2); }
        else if(tag==='path'&&o&&o.tag==='path'&&o.d!==n.getAttribute('d')){ /* arc paths: cross-fade */ n.style.opacity='0'; n.style.transition='opacity 360ms ease-out'; requestAnimationFrame(function(){ n.style.opacity=''; }); }
        else if(!same){ /* shape changed: build in from baseline */ n.style.transformBox='fill-box'; n.style.transformOrigin=(tag==='rect'&&(+n.getAttribute('width')>+n.getAttribute('height')))?'left center':'center bottom'; n.style.transform=(tag==='rect'&&(+n.getAttribute('width')>+n.getAttribute('height')))?'scaleX(0)':'scaleY(0)'; n.style.transition='none'; requestAnimationFrame(function(){ n.style.transition='transform 480ms cubic-bezier(.2,.7,.2,1)'; n.style.transform=''; }); }
      }); });
  }
  function growBars(root,delayStep){ if(!motion)return; var i=0; root.querySelectorAll(BAR_SEL).forEach(function(b){ if(b.getBoundingClientRect().width===0)return; b.classList.remove('eh-grow'); void b.offsetWidth; b.style.animationDelay=Math.min(i*30,300)+'ms'; b.classList.add('eh-grow'); i++; }); }
  function snapNums(root){ return [].map.call(root.querySelectorAll(KPI_SEL),function(el){ return el.textContent.trim(); }); }
  function countFrom(oldVals,root){ if(!motion)return; var els=root.querySelectorAll(KPI_SEL); els.forEach(function(el,i){ if(el.children.length)return; var raw=el.textContent.trim(), p=parseNum(raw), q=oldVals[i]?parseNum(oldVals[i]):null; if(!p||raw.length>18)return; var from=(q&&q.pre===p.pre&&q.post===p.post)?q.n:0; if(from===p.n)return; var start=performance.now(),dur=560; function step(t){ var k=Math.min(1,(t-start)/dur); k=1-Math.pow(1-k,3); el.textContent=p.pre+fmt(from+(p.n-from)*k,p)+p.post; if(k<1)requestAnimationFrame(step); else el.textContent=raw; } requestAnimationFrame(step); }); }
  function animateCards(root){ if(!motion)return; root=root||document; var i=0; root.querySelectorAll('.card,.kc').forEach(function(el){ if(el.getBoundingClientRect().height===0)return; el.classList.remove('eh-fade-in'); void el.offsetWidth; el.style.animationDelay=Math.min(i*35,280)+'ms'; el.classList.add('eh-fade-in'); i++; }); }
  function wrapBids(){
    if(PAGE!=='bids')return;
    /* year / scope toggle */
    if(typeof window.setScope==='function'&&!window.setScope.__eh){ var os=window.setScope; window.setScope=function(){ var root=document; var rects=snapRects(root), svgs=snapSvg(root), nums=snapNums(root); var r=os.apply(this,arguments);
        requestAnimationFrame(function(){ flipCards(rects,root); morphSvg(svgs,root); growBars(root); countFrom(nums,root); }); return r; }; window.setScope.__eh=true; }
    /* tab change */
    if(typeof window.go==='function'&&!window.go.__eh){ var og=window.go; window.go=function(id){ var r=og.apply(this,arguments); var sec=document.getElementById('s-'+id); setTimeout(function(){ animateCards(sec||document); growBars(sec||document); },20); return r; }; window.go.__eh=true; }
    /* pricing intelligence: expand / collapse one tender, or all */
    function wrapPx(name){ if(typeof window[name]!=='function'||window[name].__eh)return; var of=window[name]; window[name]=function(){ var sec=document.getElementById('s-pricing')||document; var rects=snapRects(sec); var wasOpen={}; sec.querySelectorAll('.card').forEach(function(c,i){ wasOpen[i]=c.getBoundingClientRect().height; }); var r=of.apply(this,arguments);
        requestAnimationFrame(function(){ flipCards(rects,sec); sec.querySelectorAll('.card').forEach(function(c,i){ var h=c.getBoundingClientRect().height; if(wasOpen[i]!=null&&h>wasOpen[i]+20){ var body=c.children[1]||c; body.classList.add('eh-expand'); growBars(c); } }); }); return r; }; window[name].__eh=true; }
    wrapPx('togglePx'); wrapPx('pxAll');
  }
  function ready(fn){ if(document.readyState==='complete')setTimeout(fn,60); else window.addEventListener('load',function(){setTimeout(fn,60);}); }
  ready(function(){ stagger(); countUp(); floorText(); wrapBids(); setTimeout(floorText,1500); });
  window.EH_SHARED={version:'1.1.0',page:PAGE,embedded:embedded,motion:motion,floorText:floorText};
})();
