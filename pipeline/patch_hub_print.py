"""patch_hub_print.py — Print / save any hub tab as PDF (9 Nov 2026).

Youssef: "add a feature in the competition tab or any tab of the bids/tender, government tenders, news and
intelligence etc. to export/print the whole tab page."

How it works
- Hub shell: a 🖨 button beside Presentation mode ("Print / save as PDF" EN·AR) and Ctrl/Cmd+P both call hubPrint(),
  which finds the frame currently on screen (top-level tab, or the News & Intelligence sub-tab) and posts
  {ehhub:'print'} to it. The browser's print dialog opens for that page alone — the reader picks a printer or
  "Save as PDF". Pages without the shared layer (Saudi ports map) are printed directly.
- eh-shared.js (every app): on {ehhub:'print'} or window.ehPrint(), the page is prepared for paper — every
  scrolling panel is opened to its full height so nothing below the fold is lost, fixed/sticky chrome
  (floating buttons, language bars, side drawers) is hidden, a header is added (app title · EH · date · language),
  then window.print(); everything is restored on afterprint.
- eh-shared.css: the @media print block gets the generic page rules (A4 landscape by default, white background,
  no animation, page-break hints for cards and tables).
Standalone use: any app page also answers Ctrl/Cmd+P the same way.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table

HUB = os.path.dirname(HERE) + '/hub'
load(HUB + '/EH_Hub.html', 'hub'); load(HUB + '/eh-shared.js', 'js'); load(HUB + '/eh-shared.css', 'css')
if 'hubPrint' in FILES['hub']: sys.exit('Already applied.')
ok = []

# ---- 1. hub shell: button + keyboard
BTN = ('  <button onclick="hubPrint()" title="Print or save this view as PDF" aria-label="Print or save the current view as PDF" data-tt-en="Print or save this view as PDF" data-tt-ar="طباعة هذه اللوحة أو حفظها PDF" data-al-en="Print or save the current view as PDF" data-al-ar="طباعة اللوحة الحالية أو حفظها PDF" style="padding:7px 11px;border:1px solid var(--line);border-radius:8px;background:#fff;cursor:pointer;font-size:13px;line-height:1">'
       '<svg class="ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;vertical-align:-3px"><path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/></svg></button>\n'
       '  <button onclick="hubFS()" title="Presentation mode (fullscreen)"')
ok.append(rep('hub', '  <button onclick="hubFS()" title="Presentation mode (fullscreen)"', BTN, 'hub-print', 'Hub toolbar: Print / save as PDF button before Presentation mode'))
ok.append(rep('hub', "// ---- presentation mode ----\nfunction hubFS(){",
"""// ---- print / save as PDF: the frame on screen, prepared for paper by eh-shared.js (9 Nov 2026) ----
function hubCurFrame(){
  var f=document.querySelector('iframe.on');
  if(!f){var w=$('newswrap');if(w&&w.style.display!=='none'){f=Array.prototype.find.call(w.querySelectorAll('iframe'),function(x){return x.style.display!=='none'&&x.src;});}}
  return f;
}
function hubPrint(){
  var f=hubCurFrame(); if(!f||!f.contentWindow)return;
  var w=f.contentWindow, shared=false; try{ shared=!!(w.EH_SHARED&&w.ehPrint); }catch(e){}
  if(shared){ try{ w.postMessage({ehhub:'print',lang:hubL},'*'); return; }catch(e){} }
  try{ w.focus(); w.print(); }catch(e){ window.print(); }
}
document.addEventListener('keydown',function(e){ if((e.ctrlKey||e.metaKey)&&!e.shiftKey&&!e.altKey&&(e.key==='p'||e.key==='P')){ e.preventDefault(); hubPrint(); } });
// ---- presentation mode ----
function hubFS(){""", 'hub-print', 'hubPrint(): posts {ehhub:print} to the frame on screen; Ctrl/Cmd+P routed to it'))

# ---- 2. eh-shared.js: print preparation
ok.append(rep('js', "    if(d.ehhub==='theme'&&(d.theme==='dark'||d.theme==='light')){ var g=THEME[PAGE]; try{ if(g)g(d.theme); }catch(err){} }\n  });",
"""    if(d.ehhub==='theme'&&(d.theme==='dark'||d.theme==='light')){ var g=THEME[PAGE]; try{ if(g)g(d.theme); }catch(err){} }
    if(d.ehhub==='print'){ ehPrint(); }
  });

  /* 2b. Print / save as PDF (9 Nov 2026): open every scrolling panel, hide floating chrome, add a header, print, restore. */
  var PRINT_UNDO=[];
  function ehPrintPrepare(){
    if(html.classList.contains('eh-printing'))return;
    html.classList.add('eh-printing');
    var all=document.body.querySelectorAll('*'), vw=window.innerWidth;
    for(var i=0;i<all.length;i++){ var el=all[i]; if(el.tagName==='SVG'||el.tagName==='CANVAS'||el.closest('svg'))continue; var cs; try{cs=getComputedStyle(el);}catch(e){continue;}
      var scroller=(/(auto|scroll)/.test(cs.overflowY)||/(auto|scroll)/.test(cs.overflow))&&el.scrollHeight>el.clientHeight+4;
      var fixed=cs.position==='fixed'&&el.offsetWidth<vw*0.9&&el.id!=='ehPrintHead';
      var sticky=cs.position==='sticky';
      if(scroller||fixed||sticky){ PRINT_UNDO.push([el,el.getAttribute('style')]);
        if(scroller){ el.style.setProperty('height','auto','important'); el.style.setProperty('max-height','none','important'); el.style.setProperty('overflow','visible','important'); el.style.setProperty('flex','none','important'); }
        if(fixed){ el.style.setProperty('display','none','important'); }
        if(sticky){ el.style.setProperty('position','static','important'); } } }
    /* page-level scroll containers that size to the viewport */
    [document.documentElement,document.body].forEach(function(el){ PRINT_UNDO.push([el,el.getAttribute('style')]); el.style.setProperty('height','auto','important'); el.style.setProperty('overflow','visible','important'); });
    var ar=/^ar/i.test(html.lang||'')||html.dir==='rtl';
    var h=document.createElement('div'); h.id='ehPrintHead'; h.dir=ar?'rtl':'ltr';
    var title=(document.querySelector('header h1, h1')||{}).textContent||document.title;
    var d=new Date(), ds=new Intl.DateTimeFormat(ar?'ar-SA-u-nu-latn':'en-GB',{timeZone:'Asia/Riyadh',day:'numeric',month:'long',year:'numeric',hour:'2-digit',minute:'2-digit'}).format(d);
    h.innerHTML='<div class="ehph-t">'+String(title).replace(/[<>]/g,'')+'</div><div class="ehph-s">'+(ar?'آفاق البيئة — منصة الاستخبارات الاستراتيجية · طُبعت ':'Environmental Horizons — Strategic Intelligence Hub · printed ')+ds+(ar?' (بتوقيت السعودية) · سرّي':' (KSA) · Confidential')+'</div>';
    document.body.insertBefore(h,document.body.firstChild);
    try{ window.dispatchEvent(new Event('resize')); }catch(e){}
  }
  function ehPrintRestore(){
    if(!html.classList.contains('eh-printing'))return;
    html.classList.remove('eh-printing');
    PRINT_UNDO.forEach(function(p){ if(p[1]==null)p[0].removeAttribute('style'); else p[0].setAttribute('style',p[1]); }); PRINT_UNDO=[];
    var h=document.getElementById('ehPrintHead'); if(h)h.parentNode.removeChild(h);
    try{ window.dispatchEvent(new Event('resize')); }catch(e){}
  }
  function ehPrint(){ ehPrintPrepare(); setTimeout(function(){ try{ window.focus(); window.print(); }catch(e){ ehPrintRestore(); } },350); }
  window.addEventListener('afterprint',function(){ setTimeout(ehPrintRestore,100); });
  window.ehPrint=ehPrint; window.ehPrintPrepare=ehPrintPrepare; window.ehPrintRestore=ehPrintRestore;
  document.addEventListener('keydown',function(e){ if((e.ctrlKey||e.metaKey)&&!e.shiftKey&&!e.altKey&&(e.key==='p'||e.key==='P')){ e.preventDefault(); ehPrint(); } });""",
'hub-print', 'eh-shared.js: ehPrint — open scrollers, hide floating chrome, header, print, restore; Ctrl/Cmd+P'))
ok.append(rep('js', "/* eh-shared.js — EH Hub shared behaviour layer · v2.0.0 · 2026-10-12 (v1.1.0 2026-09-08)",
              "/* eh-shared.js — EH Hub shared behaviour layer · v2.1.0 · 2026-11-09 (v2.0.0 2026-10-12; v1.1.0 2026-09-08)\n   v2.1.0: print / save as PDF of the whole page on {ehhub:'print'}, window.ehPrint() or Ctrl/Cmd+P.", 'hub-print', 'version'))
ok.append(rep('js', "window.EH_SHARED={version:'2.0.0',", "window.EH_SHARED={version:'2.1.0',print:ehPrint,", 'hub-print', 'EH_SHARED exposes print'))

# ---- 3. eh-shared.css: print rules
ok.append(rep('css', "@media print{html,body{background:#fff !important;color:#15224D !important}.eh-contour,.eh-syncstamp{display:none !important}.eh-rv{opacity:1 !important;transform:none !important}}",
"""@media print{html,body{background:#fff !important;color:#15224D !important}.eh-contour,.eh-syncstamp{display:none !important}.eh-rv{opacity:1 !important;transform:none !important}
  @page{size:A4 landscape;margin:12mm}
  html.eh-printing *,html.eh-printing *::before,html.eh-printing *::after{animation:none !important;transition:none !important;box-shadow:none !important;text-shadow:none !important}
  html.eh-printing body{width:auto !important;min-width:0 !important}
  html.eh-printing .card,html.eh-printing .kc,html.eh-printing .panel,html.eh-printing table,html.eh-printing figure,html.eh-printing .exc{break-inside:avoid;page-break-inside:avoid}
  html.eh-printing tr,html.eh-printing .kpi{break-inside:avoid}
  html.eh-printing h2,html.eh-printing h3{break-after:avoid}
  html.eh-printing [role="dialog"],html.eh-printing .modal,html.eh-printing .overlay,html.eh-printing .tooltip,html.eh-printing #ehcbtn,html.eh-printing #ehLangBar,html.eh-printing .mfilt,html.eh-printing button:not(.tab):not(.nsub){display:none !important}
  html.eh-printing a{text-decoration:none;color:inherit}
}
#ehPrintHead{display:none}
html.eh-printing #ehPrintHead{display:block;padding:0 0 10px;margin:0 0 14px;border-bottom:2px solid #15224D;font-family:inherit}
#ehPrintHead .ehph-t{font-size:18px;font-weight:800;color:#15224D}
#ehPrintHead .ehph-s{font-size:11px;color:#5F7078;margin-top:3px}""",
'hub-print', 'eh-shared.css: print page setup, break hints, floating chrome hidden, print header styles'))
ok.append(rep('css', "/* eh-shared.css — EH Hub design system · v2.0.0 · 2026-10-12", "/* eh-shared.css — EH Hub design system · v2.1.0 · 2026-11-09 (print rules) · v2.0.0 · 2026-10-12", 'hub-print', 'version'))

if not all(ok): sys.exit('ANCHOR MISMATCH: ' + str(ok))
for k, p in (('hub', '/EH_Hub.html'), ('js', '/eh-shared.js'), ('css', '/eh-shared.css')): open(HUB + p, 'w', encoding='utf-8').write(FILES[k])
write_change_table(os.path.join(HERE, 'change_table_hub_print'), 'Change table — Print / save as PDF (9 Nov 2026)'); print('applied')
