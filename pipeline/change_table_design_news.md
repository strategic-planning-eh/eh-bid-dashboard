# Design system v2 — Corporate & Government News

Generated 2026-10-12 10:07 · 20 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | news | exact | design | page skin after the shared design system | 1 | ✓ |
| 2 | news | exact | design | standalone masthead contour lines | 1 | ✓ |
| 3 | news | exact | motion | fact-check panel joins the reveal | 1 | ✓ |
| 4 | news | exact | motion | watch-list panel joins the reveal | 1 | ✓ |
| 5 | news | exact | motion | big-picture panel joins the reveal | 1 | ✓ |
| 6 | news | exact | motion | story panel kept out of the reveal (it flashed open on load) | 1 | ✓ |
| 7 | news | exact | motion | Table view slides in | 1 | ✓ |
| 8 | news | exact | motion | Cards view slides in | 1 | ✓ |
| 9 | news | exact | design | brand chart palette | 1 | ✓ |
| 10 | news | exact | design | chart text in the brand font, axis colour from the tokens | 1 | ✓ |
| 11 | news | exact | design | sector donut legend readable | 1 | ✓ |
| 12 | news | exact | design | news-category bars in one brand colour; mirrored in Arabic | 1 | ✓ |
| 13 | news | exact | design | new-money bars in brand colours | 1 | ✓ |
| 14 | news | exact | design | new-money axis readable | 1 | ✓ |
| 15 | news | exact | rtl | brand fonts redraw; horizontal bars mirror in Arabic | 1 | ✓ |
| 16 | news | regex | dark | old dark-mode block replaced by token rules | 1 | ✓ |
| 17 | news | regex | dark | language bar from the tokens | 1 | ✓ |
| 18 | news | regex | design | Arabic report: token surfaces, no coloured bar before headings | 1 | ✓ |
| 19 | news | exact | dark | chart axis/grid colours from the tokens | 1 | ✓ |
| 20 | news | exact | dark | brand series colours switch to their dark-theme twins (arrays included) | 1 | ✓ |

## Edit detail

### 1. news — page skin after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Corporate & Government News skin (patch_design_news.py). Tokens and fonts come from eh-shared.css. */
/* the page's own variables, mapped to the shared tokens (declared on body so body.dark re-resolves them) */
body,body.dark{--eh-green:var(--eh-leaf);--eh-blue:var(--eh-sea);--eh-green-d:var(--eh-leaf-ink);-
```

### 2. news — standalone masthead contour lines

**Old**
```
<header class="masthead">
```
**New**
```
<header class="masthead" data-eh-contour="7">
```

### 3. news — fact-check panel joins the reveal

**Old**
```
<div class="audit-wrap">
```
**New**
```
<div class="audit-wrap eh-panel">
```

### 4. news — watch-list panel joins the reveal

**Old**
```
<div class="flag-wrap">
```
**New**
```
<div class="flag-wrap eh-panel">
```

### 5. news — big-picture panel joins the reveal

**Old**
```
<div class="highlights">
```
**New**
```
<div class="highlights eh-panel">
```

### 6. news — story panel kept out of the reveal (it flashed open on load)

**Old**
```
<aside class="panel" id="panel" aria-hidden="true">
```
**New**
```
<aside class="panel" id="panel" aria-hidden="true" data-eh-noreveal>
```

### 7. news — Table view slides in

**Old**
```
document.getElementById('v-card').classList.remove('active'); render();});
```
**New**
```
document.getElementById('v-card').classList.remove('active'); render(); ehViewSwap();});
```

### 8. news — Cards view slides in

**Old**
```
document.getElementById('v-table').classList.remove('active'); render();});
```
**New**
```
document.getElementById('v-table').classList.remove('active'); render(); ehViewSwap();});
function ehViewSwap(){ if(window.EH_SHARED&&EH_SHARED.viewIn){ document.querySelectorAll('#sec-corp .scope-block,#sec-gov .scope-block').forEach(function(el){ EH_SHARED.viewIn(el); }); } }
```

### 9. news — brand chart palette

**Old**
```
const PALETTE=['#2563eb','#0ea5e9','#06b6d4','#14b8a6','#10b981','#22c55e','#84cc16','#eab308','#f59e0b','#f97316','#ef4444','#f43f5e','#ec4899','#a855f7','#6366f1'];
```
**New**
```
// EH design system v2: land → sea palette from the logo and the EH profile
const PALETTE=['#0072BB','#54AB5D','#3B57B8','#00A0E0','#C98A1B','#8E6BB8','#A6CE39','#B23F2B','#5E9FD6','#7FB685'];
```

### 10. news — chart text in the brand font, axis colour from the tokens

**Old**
```
Chart.defaults.font.family="'Plus Jakarta Sans',sans-serif";
Chart.defaults.font.size=11;
Chart.defaults.color='#64748b';
```
**New**
```
Chart.defaults.font.family="'EH Sans','Encode Sans','Segoe UI',Tahoma,Arial,sans-serif";
Chart.defaults.font.size=12;
Chart.defaults.color='#5E6B80';
Chart.defaults.borderColor='#D9E3DF';
const EH_RTL=()=>document.documentElement.dir==='rtl';
```

### 11. news — sector donut legend readable

**Old**
```
backgroundColor:PALETTE, borderColor:'#fff', borderWidth:2}]},
  options:{cutout:'58%', plugins:{legend:{position:'right', labels:{boxWidth:10, padding:8, font:{size:10}}}}}
```
**New**
```
backgroundColor:PALETTE, borderColor:'#fff', borderWidth:2}]},
  options:{cutout:'60%', plugins:{legend:{position:'right', labels:{boxWidth:9, boxHeight:9, usePointStyle:true, pointStyle:'circle', padding:9, font:{size:12}}}}}
```

### 12. news — news-category bars in one brand colour; mirrored in Arabic

**Old**
```
backgroundColor:catData.map((_,i)=>colorFor(i)), borderRadius:5, barThickness:14}]},
  options:{indexAxis:'y', plugins:{legend:{display:false}},
    scales:{x:{beginAtZero:true, ticks:{precision:0, stepSize:1}, grid:{color:'#eceff3'}}, y:{grid:{display:false}, ticks:{font:{size:10}}}}}
```
**New**
```
backgroundColor:catData.map(()=>'#0072BB'), borderRadius:4, barThickness:14}]},
  options:{indexAxis:'y', plugins:{legend:{display:false}},
    scales:{x:{beginAtZero:true, reverse:EH_RTL(), ticks:{precision:0, stepSize:1}, grid:{color:'#D9E3DF'}}, y:{position:EH_RTL()?'right':'left', grid:{display:false}, ticks:{font:{size:12}}}}}
```

### 13. news — new-money bars in brand colours

**Old**
```
backgroundColor:['#2563eb','#06b6d4','#f59e0b'], borderRadius:5, barThickness:30}]},
```
**New**
```
backgroundColor:['#0072BB','#00A0E0','#C98A1B'], borderRadius:4, barThickness:30}]},
```

### 14. news — new-money axis readable

**Old**
```
scales:{y:{beginAtZero:true, grid:{color:'#eceff3'}, ticks:{callback:v=>'$'+v+'bn'}}, x:{grid:{display:false}, ticks:{font:{size:10}}}}}
```
**New**
```
scales:{y:{beginAtZero:true, grid:{color:'#D9E3DF'}, ticks:{callback:v=>'$'+v+'bn'}}, x:{grid:{display:false}, ticks:{font:{size:12}}}}}
```

### 15. news — brand fonts redraw; horizontal bars mirror in Arabic

**Old**
```
/* ----- init ----- */
render();
renderFlagged();
```
**New**
```
/* ----- init ----- */
render();
renderFlagged();
/* EH design system v2: redraw once the brand fonts are in; mirror the horizontal bar chart when the page turns Arabic */
(function(){
  const all=()=>Object.values(Chart.instances||{});
  if(document.fonts&&document.fonts.load){ Promise.all([document.fonts.load("500 12px 'EH Sans'"),document.fonts.load("500 12px 'EH Sans'",'\u0639\u0631\u0628\u064
```

### 16. news — old dark-mode block replaced by token rules

**Old**
```
<style id="ehDark">\nbody\.dark\{--eh-green-l:.*?body\.dark \.blue\{color:#7FB4E8 !important\}\n
```
**New**
```
<fn>
```

### 17. news — language bar from the tokens

**Old**
```
#ehLangBar\{position:fixed;top:10px;left:12px;z-index:9999;display:flex;gap:0;border:1px solid rgba\(128,148,160,\.4\);border-radius:8px;overflow:hidden;font-family:inherit\}\n.*?body\.dark #ehLangBar button\.on\{background:#0E5A9E;color:#fff\}\n
```
**New**
```
<fn>
```

### 18. news — Arabic report: token surfaces, no coloured bar before headings

**Old**
```
#ehArView\{display:none;max-width:1040px.*?body\.dark #ehArView \.avnote\{color:#93A6B2\}\n
```
**New**
```
<fn>
```

### 19. news — chart axis/grid colours from the tokens

**Old**
```
var c=dark?'#C9D4DB':'#666', g=dark?'#2C3A43':'#E5E5E5';
```
**New**
```
var cs=getComputedStyle(document.body), c=(cs.getPropertyValue('--eh-ink-3')||'').trim()||(dark?'#9DABC5':'#5E6B80'), g=(cs.getPropertyValue('--eh-line')||'').trim()||(dark?'#2A3A6B':'#D9E3DF');
    var DK={'#0072BB':'#4EB0EE','#54AB5D':'#7CCB82','#3B57B8':'#A9B6E8','#00A0E0':'#38C6F4','#C98A1B':'#E8B04A','#8E6BB8':'#B79BDB','#A6CE39':'#C2E06A','#B23F2B':'#F0907D','#5E9FD6':'#8CC0EC','#7FB685':'#A
```

### 20. news — brand series colours switch to their dark-theme twins (arrays included)

**Old**
```
      var p=pl(x); if(!p) return x;
```
**New**
```
      if(Array.isArray(x)) return x.map(lift);
      if(typeof x==='string'&&DK[x.toUpperCase()]) return DK[x.toUpperCase()];
      var p=pl(x); if(!p) return x;
```
