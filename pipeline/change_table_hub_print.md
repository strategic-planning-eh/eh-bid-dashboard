# Change table — Print / save as PDF (9 Nov 2026)

Generated 2026-11-09 16:05 · 7 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | hub | exact | hub-print | Hub toolbar: Print / save as PDF button before Presentation mode | 1 | ✓ |
| 2 | hub | exact | hub-print | hubPrint(): posts {ehhub:print} to the frame on screen; Ctrl/Cmd+P routed to it | 1 | ✓ |
| 3 | js | exact | hub-print | eh-shared.js: ehPrint — open scrollers, hide floating chrome, header, print, restore; Ctrl/Cmd+P | 1 | ✓ |
| 4 | js | exact | hub-print | version | 1 | ✓ |
| 5 | js | exact | hub-print | EH_SHARED exposes print | 1 | ✓ |
| 6 | css | exact | hub-print | eh-shared.css: print page setup, break hints, floating chrome hidden, print header styles | 1 | ✓ |
| 7 | css | exact | hub-print | version | 1 | ✓ |

## Edit detail

### 1. hub — Hub toolbar: Print / save as PDF button before Presentation mode

**Old**
```
  <button onclick="hubFS()" title="Presentation mode (fullscreen)"
```
**New**
```
  <button onclick="hubPrint()" title="Print or save this view as PDF" aria-label="Print or save the current view as PDF" data-tt-en="Print or save this view as PDF" data-tt-ar="طباعة هذه اللوحة أو حفظها PDF" data-al-en="Print or save the current view as PDF" data-al-ar="طباعة اللوحة الحالية أو حفظها PDF" style="padding:7px 11px;border:1px solid var(--line);border-radius:8px;background:#fff;cursor:
```

### 2. hub — hubPrint(): posts {ehhub:print} to the frame on screen; Ctrl/Cmd+P routed to it

**Old**
```
// ---- presentation mode ----
function hubFS(){
```
**New**
```
// ---- print / save as PDF: the frame on screen, prepared for paper by eh-shared.js (9 Nov 2026) ----
function hubCurFrame(){
  var f=document.querySelector('iframe.on');
  if(!f){var w=$('newswrap');if(w&&w.style.display!=='none'){f=Array.prototype.find.call(w.querySelectorAll('iframe'),function(x){return x.style.display!=='none'&&x.src;});}}
  return f;
}
function hubPrint(){
  var f=hubCurFram
```

### 3. js — eh-shared.js: ehPrint — open scrollers, hide floating chrome, header, print, restore; Ctrl/Cmd+P

**Old**
```
    if(d.ehhub==='theme'&&(d.theme==='dark'||d.theme==='light')){ var g=THEME[PAGE]; try{ if(g)g(d.theme); }catch(err){} }
  });
```
**New**
```
    if(d.ehhub==='theme'&&(d.theme==='dark'||d.theme==='light')){ var g=THEME[PAGE]; try{ if(g)g(d.theme); }catch(err){} }
    if(d.ehhub==='print'){ ehPrint(); }
  });

  /* 2b. Print / save as PDF (9 Nov 2026): open every scrolling panel, hide floating chrome, add a header, print, restore. */
  var PRINT_UNDO=[];
  function ehPrintPrepare(){
    if(html.classList.contains('eh-printing'))return;

```

### 4. js — version

**Old**
```
/* eh-shared.js — EH Hub shared behaviour layer · v2.0.0 · 2026-10-12 (v1.1.0 2026-09-08)
```
**New**
```
/* eh-shared.js — EH Hub shared behaviour layer · v2.1.0 · 2026-11-09 (v2.0.0 2026-10-12; v1.1.0 2026-09-08)
   v2.1.0: print / save as PDF of the whole page on {ehhub:'print'}, window.ehPrint() or Ctrl/Cmd+P.
```

### 5. js — EH_SHARED exposes print

**Old**
```
window.EH_SHARED={version:'2.0.0',
```
**New**
```
window.EH_SHARED={version:'2.1.0',print:ehPrint,
```

### 6. css — eh-shared.css: print page setup, break hints, floating chrome hidden, print header styles

**Old**
```
@media print{html,body{background:#fff !important;color:#15224D !important}.eh-contour,.eh-syncstamp{display:none !important}.eh-rv{opacity:1 !important;transform:none !important}}
```
**New**
```
@media print{html,body{background:#fff !important;color:#15224D !important}.eh-contour,.eh-syncstamp{display:none !important}.eh-rv{opacity:1 !important;transform:none !important}
  @page{size:A4 landscape;margin:12mm}
  html.eh-printing *,html.eh-printing *::before,html.eh-printing *::after{animation:none !important;transition:none !important;box-shadow:none !important;text-shadow:none !important
```

### 7. css — version

**Old**
```
/* eh-shared.css — EH Hub design system · v2.0.0 · 2026-10-12
```
**New**
```
/* eh-shared.css — EH Hub design system · v2.1.0 · 2026-11-09 (print rules) · v2.0.0 · 2026-10-12
```
