# Design system v2 — PIF annual reports

Generated 2026-10-12 10:04 · 8 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | pif | exact | design | page skin straight after the shared design system | 1 | ✓ |
| 2 | pif | exact | design | standalone masthead contour lines | 1 | ✓ |
| 3 | pif | exact | motion | sections join the shared reveal-on-scroll (eh-panel) | 10 | ✓ |
| 4 | pif | exact | design | brand chart palette from the shared tokens | 1 | ✓ |
| 5 | pif | exact | design | chart text in the brand font | 1 | ✓ |
| 6 | pif | exact | rtl | axis text in the footnote ink; horizontal bar charts mirror in Arabic | 1 | ✓ |
| 7 | pif | exact | design | keyword heat map in EH blue | 1 | ✓ |
| 8 | pif | exact | design | repaint chart text once the brand fonts have loaded | 1 | ✓ |

## Edit detail

### 1. pif — page skin straight after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — PIF annual reports skin (patch_design_pif.py). Tokens and fonts come from eh-shared.css. */
/* the page's own colour variables, mapped onto the shared tokens (light and dark both follow eh-shared.css) */
:root,html[data-theme=dark]{--g:var(--eh-c2);--b:var(--eh-c1);--ink:var(--eh-ink);--grey:var(--eh-ink-2);
```

### 2. pif — standalone masthead contour lines

**Old**
```
<header><img src="data:image/jpeg
```
**New**
```
<header data-eh-contour="7"><img src="data:image/jpeg
```

### 3. pif — sections join the shared reveal-on-scroll (eh-panel)

**Old**
```
<section id="
```
**New**
```
<section class="eh-panel" id="
```

### 4. pif — brand chart palette from the shared tokens

**Old**
```
const pal=()=>({g:getComputedStyle(document.documentElement).getPropertyValue('--g').trim(),b:getComputedStyle(document.documentElement).getPropertyValue('--b').trim(),ink:getComputedStyle(document.documentElement).getPropertyValue('--ink').trim(),grid:getComputedStyle(document.documentElement).getPropertyValue('--grid').trim(),gold:THEME==='dark'?'#E0B865':'#C9A24A',red:THEME==='dark'?'#E0655A':'
```
**New**
```
// EH design system v2 (patch_design_pif.py): brand palette, land → sea, read from eh-shared.css tokens so dark mode gets its lighter set.
// Pools keep green (listed Saudi companies) and purple (PIF-founded companies): section 2's text names those two colours.
const pal=()=>{const cs=getComputedStyle(document.documentElement),v=k=>cs.getPropertyValue(k).trim(),dk=THEME==='dark';
 return {g:v('--e
```

### 5. pif — chart text in the brand font

**Old**
```
function mk(id,cfg){const C=pal();Chart.defaults.color=C.ink;Chart.defaults.borderColor=C.grid;
```
**New**
```
function mk(id,cfg){const C=pal();Chart.defaults.color=C.ink;Chart.defaults.borderColor=C.grid;Chart.defaults.font.family=getComputedStyle(document.documentElement).getPropertyValue('--eh-font').trim()||Chart.defaults.font.family;
```

### 6. pif — axis text in the footnote ink; horizontal bar charts mirror in Arabic

**Old**
```
ax.ticks=Object.assign({color:C.ink},ax.ticks||{});if(ax.title)ax.title.color=C.ink;}const ch=new Chart(
```
**New**
```
ax.ticks=Object.assign({color:C.ink3},ax.ticks||{});if(ax.title)ax.title.color=C.ink;}
if(cfg.options.indexAxis==='y'&&cfg.options.scales){const rtl=LANG==='ar';if(cfg.options.scales.x)cfg.options.scales.x.reverse=rtl;if(cfg.options.scales.y)cfg.options.scales.y.position=rtl?'right':'left';}   // Arabic: horizontal bars start from the right
const ch=new Chart(
```

### 7. pif — keyword heat map in EH blue

**Old**
```
`rgba(2,125,195,${0.15+0.85*q})`
```
**New**
```
`rgba(0,114,187,${0.15+0.85*q})`
```

### 8. pif — repaint chart text once the brand fonts have loaded

**Old**
```
<script src="eh-shared.js" defer></script>
```
**New**
```
<script>
/* EH design system v2 (patch_design_pif.py): chart text is painted on canvas, which cannot swap fonts by itself. When the brand
   fonts finish loading (first visit, or the Arabic glyphs after a language switch) the charts re-measure and repaint, without animating. */
(function(){ if(!document.fonts||!document.fonts.addEventListener)return; var tm=null;
  function repaint(){ clearTimeout
```
