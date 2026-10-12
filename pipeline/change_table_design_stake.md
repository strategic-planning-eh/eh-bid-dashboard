# Design system v2 — Stakeholder & Competitive Map

Generated 2026-10-12 10:05 · 29 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | stake | exact | design | page skin after the shared design system | 1 | ✓ |
| 2 | stake | exact | design | standalone masthead contour lines | 1 | ✓ |
| 3 | stake | exact | design | regional-view panels join the shared panel style and reveal | 2 | ✓ |
| 4 | stake | exact | motion | view switch uses the shared view-in motion | 1 | ✓ |
| 5 | stake | exact | design | wheel ring guides on the brand hairline | 1 | ✓ |
| 6 | stake | exact | design | threat-band tints from the brand status set | 1 | ✓ |
| 7 | stake | exact | design | region dividers on the brand hairline | 1 | ✓ |
| 8 | stake | exact | design | wheel region labels in sentence case (were capitals) | 1 | ✓ |
| 9 | stake | exact | design | wheel region labels not forced to capitals | 1 | ✓ |
| 10 | stake | exact | design | label leader ticks on the brand hairline | 1 | ✓ |
| 11 | stake | exact | design | wheel region labels in the brand font, readable size | 1 | ✓ |
| 12 | stake | exact | design | wheel region labels in ink-3 (AA) in both themes | 1 | ✓ |
| 13 | stake | exact | design | EH centre disc on the panel colour | 1 | ✓ |
| 14 | stake | exact | design | EH centre ring in logo green | 1 | ✓ |
| 15 | stake | exact | design | EH centre fallback text in the brand display font | 1 | ✓ |
| 16 | stake | exact | design | EH centre caption in brand font and ink-2 | 1 | ✓ |
| 17 | stake | exact | design | threat ring pills: sentence case, brand status colours readable in both themes | 1 | ✓ |
| 18 | stake | exact | design | ring pills in the brand font | 1 | ✓ |
| 19 | stake | exact | design | ring pill fill on the panel colour | 1 | ✓ |
| 20 | stake | exact | design | zoomed company names in the brand font and ink-2 | 1 | ✓ |
| 21 | stake | exact | design | regulator ring in deep navy, visible in dark mode | 1 | ✓ |
| 22 | stake | exact | design | selected-node ring in brand ink | 1 | ✓ |
| 23 | stake | exact | design | wheel redrawn once the brand fonts have loaded | 1 | ✓ |
| 24 | stake | exact | design | legend wording in sentence case (were capitals) | 1 | ✓ |
| 25 | stake | exact | design | guide: ring names in sentence case to match the wheel | 1 | ✓ |
| 26 | stake | exact | design | guide: ring names in sentence case to match the wheel | 1 | ✓ |
| 27 | stake | exact | design | guide: ring names in sentence case to match the wheel | 1 | ✓ |
| 28 | stake | exact | design | guide: ring names in sentence case to match the wheel | 1 | ✓ |
| 29 | stake | exact | design | schematic map province labels in sentence case | 1 | ✓ |

## Edit detail

### 1. stake — page skin after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css"><style id="eh-skin">
/* EH design system v2 — Stakeholder Map skin (patch_design_stake.py). Tokens and fonts come from eh-shared.css. */
:root,html.dark{--paper:var(--eh-paper);--mist:var(--eh-mist);--ink:var(--eh-ink);--ink-soft:var(--eh-ink-2);--line:var(--eh-line);--eh-blue-d:var(--eh-deep)}
body,html.dark body{background:var(--eh-mist);color:var(--eh
```

### 2. stake — standalone masthead contour lines

**Old**
```
<header>
  <div class="logo">
```
**New**
```
<header data-eh-contour="7">
  <div class="logo">
```

### 3. stake — regional-view panels join the shared panel style and reveal

**Old**
```
<div class="heatwrap">
```
**New**
```
<div class="heatwrap eh-panel">
```

### 4. stake — view switch uses the shared view-in motion

**Old**
```
  if(t==='lic')buildLicenceMap();
}
let listSort=
```
**New**
```
  if(t==='lic')buildLicenceMap();
  if(window.EH_SHARED&&EH_SHARED.viewIn)EH_SHARED.viewIn(document.getElementById(t==='map'?'mapView':t+'View'));   // EH design v2: view change motion
}
let listSort=
```

### 5. stake — wheel ring guides on the brand hairline

**Old**
```
ctx.strokeStyle=(DKM?'#243039':'#E4ECE6');ctx.lineWidth=1;
```
**New**
```
ctx.strokeStyle=(DKM?'#2A3A6B':'#D9E3DF');ctx.lineWidth=1;
```

### 6. stake — threat-band tints from the brand status set

**Old**
```
const BANDS=[[0.155,0.235,'26,95,171',0.045],[0.245,0.475,'214,69,69',0.05],[0.485,0.665,'201,162,39',0.045],[0.675,0.975,'63,163,77',0.035]];
```
**New**
```
const BANDS=[[0.155,0.235,'0,114,187',0.045],[0.245,0.475,'178,63,43',0.05],[0.485,0.665,'201,138,27',0.045],[0.675,0.975,'84,171,93',0.035]];   // EH status set
```

### 7. stake — region dividers on the brand hairline

**Old**
```
ctx.strokeStyle=(DKM?'#202B33':'#EAF1EC');ctx.beginPath();
```
**New**
```
ctx.strokeStyle=(DKM?'#22305E':'#E3EBE7');ctx.beginPath();
```

### 8. stake — wheel region labels in sentence case (were capitals)

**Old**
```
const SHORTRG={'Other Makkah Region':'OTHER MAKKAH','Makkah City':'MAKKAH','Madinah Region':'MADINAH','Qassim Region':'QASSIM','Tabuk Region':'TABUK','Hail Region':'HAIL','Al Jawf Region':'AL JAWF','Northern Borders Region':'N. BORDERS','Eastern Province':'EASTERN','Southern Region':'SOUTHERN','GCC / International':"GCC / INT'L"};
```
**New**
```
const SHORTRG={'Other Makkah Region':'Other Makkah','Makkah City':'Makkah','Madinah Region':'Madinah','Qassim Region':'Qassim','Tabuk Region':'Tabuk','Hail Region':'Hail','Al Jawf Region':'Al Jawf','Northern Borders Region':'N. Borders','Eastern Province':'Eastern','Southern Region':'Southern','GCC / International':"GCC / Int'l"};
```

### 9. stake — wheel region labels not forced to capitals

**Old**
```
const lab=(LNG==='ar'?regL(r):(SHORTRG[r]||r.toUpperCase()));
```
**New**
```
const lab=(LNG==='ar'?regL(r):(SHORTRG[r]||r));
```

### 10. stake — label leader ticks on the brand hairline

**Old**
```
if(tier){ctx.strokeStyle=(DKM?'#22303A':'#E3EAE5');
```
**New**
```
if(tier){ctx.strokeStyle=(DKM?'#2A3A6B':'#D9E3DF');
```

### 11. stake — wheel region labels in the brand font, readable size

**Old**
```
ctx.font=(lab.length>9?'600 8.5px':'600 10px')+' Segoe UI, sans-serif';
```
**New**
```
ctx.font=(lab.length>9?'600 10px':'600 11px')+' "EH Sans","Segoe UI",sans-serif';
```

### 12. stake — wheel region labels in ink-3 (AA) in both themes

**Old**
```
ctx.fillStyle='#8A99A3';ctx.textAlign='center';ctx.fillText(lab,0,0);
```
**New**
```
ctx.fillStyle=(DKM?'#9DABC5':'#5E6B80');ctx.textAlign='center';ctx.fillText(lab,0,0);
```

### 13. stake — EH centre disc on the panel colour

**Old**
```
ctx.fillStyle=(DKM?'#151C21':'#fff');ctx.fill();
```
**New**
```
ctx.fillStyle=(DKM?'#15214A':'#fff');ctx.fill();
```

### 14. stake — EH centre ring in logo green

**Old**
```
ctx.lineWidth=3.5;ctx.strokeStyle='#3FA34D';
```
**New**
```
ctx.lineWidth=3.5;ctx.strokeStyle='#54AB5D';
```

### 15. stake — EH centre fallback text in the brand display font

**Old**
```
ctx.fillStyle=(DKM?'#E6EDF1':'#1C2B33');ctx.font='800 13px Segoe UI,sans-serif';
```
**New**
```
ctx.fillStyle=(DKM?'#E9EEF7':'#15224D');ctx.font='700 13px "EH Display","Segoe UI",sans-serif';
```

### 16. stake — EH centre caption in brand font and ink-2

**Old**
```
ctx.font='600 10px Segoe UI,sans-serif';ctx.fillStyle=(DKM?'#9FB3BE':'#51626D');
```
**New**
```
ctx.font='600 11px "EH Sans","Segoe UI",sans-serif';ctx.fillStyle=(DKM?'#B8C4DA':'#46546F');
```

### 17. stake — threat ring pills: sentence case, brand status colours readable in both themes

**Old**
```
const PILLS=[[0.195,t('REGULATORY','تنظيمي'),'#1A5FAB'],[0.36,t('HIGH THREAT','تهديد مرتفع'),'#B23A3A'],[0.575,t('MEDIUM','متوسط'),'#9A7A1A'],[0.84,t('LOW','منخفض'),'#2E7D3C']];
```
**New**
```
const PILLS=[[0.195,t('Regulatory','تنظيمي'),(DKM?'#7CC3F2':'#0072BB')],[0.36,t('High threat','تهديد مرتفع'),(DKM?'#F0907D':'#B23F2B')],[0.575,t('Medium','متوسط'),(DKM?'#F0C26B':'#8F5C0A')],[0.84,t('Low','منخفض'),(DKM?'#7CCB82':'#2E7A37')]];   // EH status set, sentence case
```

### 18. stake — ring pills in the brand font

**Old**
```
ctx.font='700 10px Segoe UI,sans-serif';ctx.textAlign='center';
```
**New**
```
ctx.font='600 11px "EH Sans","Segoe UI",sans-serif';ctx.textAlign='center';
```

### 19. stake — ring pill fill on the panel colour

**Old**
```
ctx.fillStyle=(DKM?'rgba(15,21,25,0.85)':'rgba(255,255,255,0.88)');ctx.fill();
```
**New**
```
ctx.fillStyle=(DKM?'rgba(21,33,74,0.94)':'rgba(255,255,255,0.94)');ctx.fill();
```

### 20. stake — zoomed company names in the brand font and ink-2

**Old**
```
ctx.font='600 9.5px Segoe UI,sans-serif';ctx.fillStyle=(DKM?'#C2D2DB':'#3A4A54');
```
**New**
```
ctx.font='500 10.5px "EH Sans","Segoe UI",sans-serif';ctx.fillStyle=(DKM?'#B8C4DA':'#46546F');
```

### 21. stake — regulator ring in deep navy, visible in dark mode

**Old**
```
ctx.lineWidth=1.6;ctx.strokeStyle='#0E3B6F';
```
**New**
```
ctx.lineWidth=1.6;ctx.strokeStyle=(document.documentElement.classList.contains('dark')?'#A9B6E8':'#1B2A6E');
```

### 22. stake — selected-node ring in brand ink

**Old**
```
ctx.strokeStyle=(DKM?'#E6EDF1':'#1C2B33');ctx.beginPath();ctx.arc(x,y,r+4
```
**New**
```
ctx.strokeStyle=(DKM?'#E9EEF7':'#15224D');ctx.beginPath();ctx.arc(x,y,r+4
```

### 23. stake — wheel redrawn once the brand fonts have loaded

**Old**
```
window.addEventListener('resize',resize);
resize();recompute();

```
**New**
```
window.addEventListener('resize',resize);
resize();recompute();
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){try{draw();}catch(e){}});   // EH design v2: redraw once the brand fonts are in

```

### 24. stake — legend wording in sentence case (were capitals)

**Old**
```
Rings = competitive threat (HIGH inner → LOW outer)
```
**New**
```
Rings = competitive threat (High inner → Low outer)
```

### 25. stake — guide: ring names in sentence case to match the wheel

**Old**
```
<b style="color:#1A5FAB">REGULATORY</b>
```
**New**
```
<b style="color:#1A5FAB">Regulatory</b>
```

### 26. stake — guide: ring names in sentence case to match the wheel

**Old**
```
<b style="color:#B23A3A">HIGH THREAT</b>
```
**New**
```
<b style="color:#B23A3A">High threat</b>
```

### 27. stake — guide: ring names in sentence case to match the wheel

**Old**
```
<b style="color:#9A7A1A">MEDIUM</b>
```
**New**
```
<b style="color:#9A7A1A">Medium</b>
```

### 28. stake — guide: ring names in sentence case to match the wheel

**Old**
```
<b style="color:#2E7D3C">LOW</b>
```
**New**
```
<b style="color:#2E7D3C">Low</b>
```

### 29. stake — schematic map province labels in sentence case

**Old**
```
font-weight="700" fill="#B3A47C" letter-spacing="1.5" style="text-transform:uppercase;pointer-events:none">'+p.n.toUpperCase()+'</text>
```
**New**
```
font-weight="600" fill="#9A8C66" style="pointer-events:none">'+p.n+'</text>
```
