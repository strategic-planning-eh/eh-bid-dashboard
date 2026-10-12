# Design system v2 — PIF Strategy 2026–2030

Generated 2026-10-12 10:07 · 8 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | strat | exact | design | page skin straight after the shared design system | 1 | ✓ |
| 2 | strat | exact | design | standalone masthead contour lines | 1 | ✓ |
| 3 | strat | exact | motion | sections join the shared reveal-on-scroll (eh-panel) | 10 | ✓ |
| 4 | strat | exact | design | chart red and amber from the shared tokens | 1 | ✓ |
| 5 | strat | exact | design | chart text in the brand font and secondary ink | 1 | ✓ |
| 6 | strat | exact | design | grey "required pace" bar in the shared muted ink | 1 | ✓ |
| 7 | strat | exact | rtl | axis colours; horizontal bar charts mirror in Arabic | 1 | ✓ |
| 8 | strat | exact | design | repaint chart text once the brand fonts have loaded | 1 | ✓ |

## Edit detail

### 1. strat — page skin straight after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — PIF Strategy 2026–2030 skin (patch_design_strat.py). Tokens and fonts come from eh-shared.css. */
/* the page's own colour variables, mapped onto the shared tokens (light and dark both follow eh-shared.css) */
:root,html[data-theme=dark]{--g:var(--eh-c2);--b:var(--eh-c1);--ink:var(--eh-ink);--grey:var(--eh-i
```

### 2. strat — standalone masthead contour lines

**Old**
```
<header><img src="data:image/jpeg
```
**New**
```
<header data-eh-contour="7"><img src="data:image/jpeg
```

### 3. strat — sections join the shared reveal-on-scroll (eh-panel)

**Old**
```
<section id="
```
**New**
```
<section class="eh-panel" id="
```

### 4. strat — chart red and amber from the shared tokens

**Old**
```
red:THEME==='dark'?'#E0655A':'#C0392B',gold:THEME==='dark'?'#E0B865':'#C9A24A'
```
**New**
```
red:g('--eh-c8'),gold:g('--eh-c5')
```

### 5. strat — chart text in the brand font and secondary ink

**Old**
```
Chart.defaults.color=C.ink;Chart.defaults.borderColor=C.grid;Chart.defaults.font.family=getComputedStyle(document.body).fontFamily;
```
**New**
```
Chart.defaults.color=getComputedStyle(document.documentElement).getPropertyValue('--eh-ink-2').trim()||C.ink;Chart.defaults.borderColor=C.grid;Chart.defaults.font.family=getComputedStyle(document.documentElement).getPropertyValue('--eh-font').trim()||getComputedStyle(document.body).fontFamily;
```

### 6. strat — grey "required pace" bar in the shared muted ink

**Old**
```
(THEME==='dark'?'rgba(160,175,185,.35)':'rgba(96,115,125,.25)')
```
**New**
```
(THEME==='dark'?'rgba(157,171,197,.32)':'rgba(94,107,128,.22)')
```

### 7. strat — axis colours; horizontal bar charts mirror in Arabic

**Old**
```
cfg.options=o;charts[id]=new Chart(
```
**New**
```
// EH design system v2 (patch_design_strat.py): axis text in the footnote ink, hairline grid; Arabic: horizontal bars start from the right
  {const cs=getComputedStyle(document.documentElement),tk=cs.getPropertyValue('--eh-ink-3').trim(),ln=cs.getPropertyValue('--eh-line').trim(),rtl=LANG==='ar';
   if(o.scales){for(const ax of Object.values(o.scales)){ax.ticks=Object.assign({color:tk},ax.ticks||{
```

### 8. strat — repaint chart text once the brand fonts have loaded

**Old**
```
<script src="eh-shared.js" defer></script>
```
**New**
```
<script>
/* EH design system v2 (patch_design_strat.py): chart text is painted on canvas, which cannot swap fonts by itself. When the brand
   fonts finish loading (first visit, or the Arabic glyphs after a language switch) the charts re-measure and repaint. */
(function(){ if(!document.fonts||!document.fonts.addEventListener)return; var tm=null;
  function repaint(){ clearTimeout(tm); tm=setTimeo
```
