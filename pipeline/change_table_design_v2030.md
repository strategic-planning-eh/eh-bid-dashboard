# Design system v2 — Vision 2030 projects

Generated 2026-10-12 10:35 · 22 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | v2030 | exact | design | page skin after the shared design system | 1 | ✓ |
| 2 | v2030 | exact | design | masthead contour lines (standalone) | 1 | ✓ |
| 3 | v2030 | exact | motion | Arabic drawer slides on its own: no scroll reveal | 1 | ✓ |
| 4 | v2030 | exact | motion | drawer slides on its own: no scroll reveal | 1 | ✓ |
| 5 | v2030 | exact | motion | Arabic findings reveal like the other panels | 8 | ✓ |
| 6 | v2030 | exact | motion | Arabic recommendations reveal like the other panels | 6 | ✓ |
| 7 | v2030 | exact | design | ownership colours from the brand palette; token reader for charts | 1 | ✓ |
| 8 | v2030 | exact | design | status colours from the brand palette | 1 | ✓ |
| 9 | v2030 | exact | design | sector colours from the brand palette | 1 | ✓ |
| 10 | v2030 | exact | design | confidence colours from the brand status set | 1 | ✓ |
| 11 | v2030 | exact | design | confidence colours from the brand status set | 1 | ✓ |
| 12 | v2030 | exact | design | confidence colours from the brand status set | 1 | ✓ |
| 13 | v2030 | exact | design | chart text in the brand font; colours from the shared tokens | 1 | ✓ |
| 14 | v2030 | exact | design | Arabic charts in the brand font | 1 | ✓ |
| 15 | v2030 | exact | design | chart tooltips in the brand ink | 6 | ✓ |
| 16 | v2030 | exact | design | doughnut rings cut in the panel colour (light and dark) | 4 | ✓ |
| 17 | v2030 | exact | design | doughnut legends readable in dark mode | 2 | ✓ |
| 18 | v2030 | exact | design | English doughnut legend at a readable size | 1 | ✓ |
| 19 | v2030 | exact | rtl | Arabic sector chart reads from the right | 1 | ✓ |
| 20 | v2030 | exact | design | theme pass uses the brand light/dark chart colours | 1 | ✓ |
| 21 | v2030 | exact | design | doughnut rings keep the panel colour in dark mode | 1 | ✓ |
| 22 | v2030 | exact | motion | chart redraw on theme change; tab change slides in | 1 | ✓ |

## Edit detail

### 1. v2030 — page skin after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">html body,html body.dark{--bg:var(--eh-mist);--surface:var(--eh-paper);--ink:var(--eh-ink);--ink-soft:var(--eh-ink-2);--ink-faint:var(--eh-ink-3);--line:var(--eh-line);--line-strong:var(--eh-line);--brand:var(--eh-sea);--brand-deep:var(--eh-deep);--green:var(--eh-leaf);--accent:var(--eh-leaf-ink);--shadow:var(--eh-shadow);--shadow-lg
```

### 2. v2030 — masthead contour lines (standalone)

**Old**
```
<header class="masthead">
```
**New**
```
<header class="masthead" data-eh-contour="7">
```

### 3. v2030 — Arabic drawer slides on its own: no scroll reveal

**Old**
```
<aside class="drawer panel ar-drawer" id="arDrawer"
```
**New**
```
<aside class="drawer panel ar-drawer" id="arDrawer" data-eh-noreveal
```

### 4. v2030 — drawer slides on its own: no scroll reveal

**Old**
```
<aside class="drawer panel" id="drawer"
```
**New**
```
<aside class="drawer panel" id="drawer" data-eh-noreveal
```

### 5. v2030 — Arabic findings reveal like the other panels

**Old**
```
<div class="ar-finding 
```
**New**
```
<div class="eh-panel ar-finding 
```

### 6. v2030 — Arabic recommendations reveal like the other panels

**Old**
```
<div class="ar-rec-card">
```
**New**
```
<div class="eh-panel ar-rec-card">
```

### 7. v2030 — ownership colours from the brand palette; token reader for charts

**Old**
```
const OWN_HEX    = {"Government":"#055a93","PIF":"#4fa85a","Joint Venture":"#0aa6a0","Mixed":"#6b7385"};
```
**New**
```
/* EH design system v2 (patch_design_v2030.py): brand palette — land → sea, amber, brick for "on hold" */
function ehTok(n,f){ try{ var v=getComputedStyle(document.body).getPropertyValue(n).trim(); return v||f; }catch(e){ return f; } }   // shared token, read at draw time
const OWN_HEX    = {"Government":"#0072BB","PIF":"#54AB5D","Joint Venture":"#00A0E0","Mixed":"#5E6B80"};
```

### 8. v2030 — status colours from the brand palette

**Old**
```
const STATUS_HEX = {"Announced":"#7cc0e8","Planning":"#e0a23c","Under Construction":"#d9c23a","Partially Operational":"#8fce6a","Operational":"#3f9d57","On Hold":"#b5675c","Under Review":"#9a6f9c"};
```
**New**
```
const STATUS_HEX = {"Announced":"#5E9FD6","Planning":"#C98A1B","Under Construction":"#3B57B8","Partially Operational":"#7FB685","Operational":"#2E7A37","On Hold":"#B23F2B","Under Review":"#8E6BB8"};
```

### 9. v2030 — sector colours from the brand palette

**Old**
```
const SECTOR_HEX = ["#0070b8","#4fa85a","#e08a3c","#0aa6a0","#8e6fc4","#d9b42a","#5b9bd5","#c0653a","#1d8f74","#d45d79","#6b7385"];
```
**New**
```
const SECTOR_HEX = ["#0072BB","#54AB5D","#3B57B8","#00A0E0","#C98A1B","#8E6BB8","#A6CE39","#B23F2B","#5E9FD6","#7FB685","#5E6B80"];
```

### 10. v2030 — confidence colours from the brand status set

**Old**
```
hex:"#3f9d57", desc:"Confirmed
```
**New**
```
hex:"#2E7A37", desc:"Confirmed
```

### 11. v2030 — confidence colours from the brand status set

**Old**
```
hex:"#e0a23c", desc:"Reported
```
**New**
```
hex:"#C98A1B", desc:"Reported
```

### 12. v2030 — confidence colours from the brand status set

**Old**
```
hex:"#c2705c", desc:"Indicative
```
**New**
```
hex:"#B23F2B", desc:"Indicative
```

### 13. v2030 — chart text in the brand font; colours from the shared tokens

**Old**
```
const gridColor="#ececea";
  Chart.defaults.font.family="'Plus Jakarta Sans', sans-serif";
  Chart.defaults.color="#4a5566";
```
**New**
```
const gridColor=ehTok("--eh-line","#D9E3DF");
  Chart.defaults.font.family="'EH Sans','Encode Sans','Segoe UI',Tahoma,Arial,sans-serif";
  Chart.defaults.font.size=12.5;
  Chart.defaults.color=ehTok("--eh-ink-2","#46546F");
```

### 14. v2030 — Arabic charts in the brand font

**Old**
```
const gridColor="#ececea";
  const arFont="'Tajawal',sans-serif";
```
**New**
```
const gridColor=ehTok("--eh-line","#D9E3DF");
  const arFont="'EH Sans','Segoe UI',Tahoma,Arial,sans-serif";   // brand font carries the Arabic glyphs
  Chart.defaults.color=ehTok("--eh-ink-2","#46546F");
```

### 15. v2030 — chart tooltips in the brand ink

**Old**
```
backgroundColor:"#055a93"
```
**New**
```
backgroundColor:"#15224D"
```

### 16. v2030 — doughnut rings cut in the panel colour (light and dark)

**Old**
```
borderColor:"#fff"
```
**New**
```
borderColor:ehTok("--eh-paper","#fff")
```

### 17. v2030 — doughnut legends readable in dark mode

**Old**
```
pointStyle:"circle",index:i}
```
**New**
```
pointStyle:"circle",fontColor:ehTok("--eh-ink-2","#46546F"),index:i}
```

### 18. v2030 — English doughnut legend at a readable size

**Old**
```
font:{size:12,weight:"500"},padding:14,
```
**New**
```
font:{size:12.5,weight:"500"},padding:14,
```

### 19. v2030 — Arabic sector chart reads from the right

**Old**
```
scales:{x:{beginAtZero:true,ticks:{precision:0,font:{size:11,family:arFont}},grid:{color:gridColor,drawBorder:false}},
              y:{ticks:{font:{size:11.5,weight:"600",family:arFont}},grid:{display:false,drawBorder:false}}}}});
```
**New**
```
scales:{x:{beginAtZero:true,reverse:true,ticks:{precision:0,font:{size:11.5,family:arFont}},grid:{color:gridColor,drawBorder:false}},
              y:{position:"right",ticks:{font:{size:12,weight:"600",family:arFont}},grid:{display:false,drawBorder:false}}}}});
```

### 20. v2030 — theme pass uses the brand light/dark chart colours

**Old**
```
var c=dark?'#C9D4DB':'#666', g=dark?'#2C3A43':'#E5E5E5';
```
**New**
```
var c=dark?'#B8C4DA':'#46546F', g=dark?'#2A3A6B':'#D9E3DF';   // brand ink and hairline (eh-shared.css v2)
```

### 21. v2030 — doughnut rings keep the panel colour in dark mode

**Old**
```
ds.borderColor=dark?lift(ds.__ehO.b):ds.__ehO.b;
```
**New**
```
ds.borderColor=(dark&&ch.config.type!=='doughnut')?lift(ds.__ehO.b):ds.__ehO.b;   // doughnut rings are cut in the panel colour, not lifted
```

### 22. v2030 — chart redraw on theme change; tab change slides in

**Old**
```
<script src="eh-shared.js" defer></script>
```
**New**
```
<script>
/* EH design system v2 (patch_design_v2030.py): charts redraw with the token colours when the theme changes;
   switching tabs slides the incoming view in from the reading-start edge. */
(function(){
  var dark=document.body.classList.contains('dark');
  function redraw(){ try{ if(typeof renderCharts==='function'&&typeof filtered==='function') renderCharts(filtered()); }catch(e){}
    try
```
