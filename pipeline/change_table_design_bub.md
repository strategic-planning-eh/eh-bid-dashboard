# Design system v2 — Client Bubble Map

Generated 2026-10-12 10:06 · 30 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | bub | exact | design | page skin right after the shared design system | 1 | ✓ |
| 2 | bub | exact | design | standalone masthead contour lines | 1 | ✓ |
| 3 | bub | exact | motion | Executive chart panels revealed by eh-shared.js | 6 | ✓ |
| 4 | bub | exact | motion | whitespace panel revealed by eh-shared.js | 1 | ✓ |
| 5 | bub | exact | motion | bubble chart panel revealed by eh-shared.js | 1 | ✓ |
| 6 | bub | exact | design | brand-led sector palette in its one constant (hue families kept) | 1 | ✓ |
| 7 | bub | exact | design | heatmap: single-hue sea-blue ramp readable in both themes | 1 | ✓ |
| 8 | bub | exact | design | chart text in the brand font | 1 | ✓ |
| 9 | bub | exact | design | PNG export asks for the brand font first | 1 | ✓ |
| 10 | bub | exact | design | revenue bridge in the brand status set | 1 | ✓ |
| 11 | bub | exact | design | retention: kept clients in leaf green | 1 | ✓ |
| 12 | bub | exact | design | retention: new clients in EH blue | 1 | ✓ |
| 13 | bub | exact | design | retention: lost clients in brick | 1 | ✓ |
| 14 | bub | exact | design | sector shift gains/losses in the brand status colours | 2 | ✓ |
| 15 | bub | exact | design | sector shift 2025 hollow dots in the brand slate | 2 | ✓ |
| 16 | bub | exact | design | sector shift legend dot in EH blue | 1 | ✓ |
| 17 | bub | exact | design | chart ink: brand navy text | 6 | ✓ |
| 18 | bub | exact | design | chart axes and secondary labels in ink-3 | 8 | ✓ |
| 19 | bub | exact | design | chart tertiary labels in ink-2 | 2 | ✓ |
| 20 | bub | exact | design | gridlines in the hairline colour | 1 | ✓ |
| 21 | bub | exact | design | bridge connector lines | 1 | ✓ |
| 22 | bub | exact | design | depth vs value: halo, labels and median guides from the tokens | 1 | ✓ |
| 23 | bub | exact | design | depth vs value: quadrant colours from the brand status set | 1 | ✓ |
| 24 | bub | exact | design | depth vs value: axes in ink-3 / hairline | 1 | ✓ |
| 25 | bub | exact | design | deal-size bars and text from the tokens | 1 | ✓ |
| 26 | bub | exact | motion | view change slides in via EH_SHARED.viewIn | 1 | ✓ |
| 27 | bub | exact | design | dark-mode extension: hard-coded colours replaced by tokens | 1 | ✓ |
| 28 | bub | exact | design | swipe hint chip in EH blue, logical position | 1 | ✓ |
| 29 | bub | exact | design | zoom buttons on the token surfaces | 1 | ✓ |
| 30 | bub | exact | design | dark panel colours now come from the tokens in the skin | 1 | ✓ |

## Edit detail

### 1. bub — page skin right after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Client Bubble Map skin (patch_design_bub.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* heatmap ramp ends: one sea-blue scale, re-themed here (renderHeat mixes between them) */
body{--bub-heat-lo:#E4
```

### 2. bub — standalone masthead contour lines

**Old**
```
<body>
<header>
  <h1>
```
**New**
```
<body>
<header data-eh-contour="7">
  <h1>
```

### 3. bub — Executive chart panels revealed by eh-shared.js

**Old**
```
<div class="ecard">
```
**New**
```
<div class="ecard eh-panel">
```

### 4. bub — whitespace panel revealed by eh-shared.js

**Old**
```
<div class="ecard" style="grid-column:1/-1">
```
**New**
```
<div class="ecard eh-panel" style="grid-column:1/-1">
```

### 5. bub — bubble chart panel revealed by eh-shared.js

**Old**
```
<div id="wrap">
```
**New**
```
<div id="wrap" class="eh-panel">
```

### 6. bub — brand-led sector palette in its one constant (hue families kept)

**Old**
```
const PALETTE = {
  "Power & Utilities":        "#027DC3",
  "Government & Municipal":   "#2BAE68",
  "Construction & Contracting":"#E8A33D",
  "Transport & Logistics":    "#1FA8A0",
  "Engineering & Consultancy":"#45B39D",
  "Oil & Gas / Petrochemicals":"#7D5BA6",
  "Trading & Services":       "#8FBF4D",
  "Manufacturing & Industrial":"#5D7793",
  "Steel & Metals":           "#8A9BA8",
  "Cement 
```
**New**
```
// EH design system v2: brand-led sector palette (land → sea). Each sector keeps its hue family from v1
// (blue, green, amber, teal, purple, lime, slate …) so the picture readers know is unchanged; white labels stay legible.
const PALETTE = {
  "Power & Utilities":        "#0072BB",
  "Government & Municipal":   "#54AB5D",
  "Construction & Contracting":"#C98A1B",
  "Transport & Logistics":    "#
```

### 7. bub — heatmap: single-hue sea-blue ramp readable in both themes

**Old**
```
  const cellBg = v => {
    if (v <= 0) return null;
    const t = Math.sqrt(v/vmax);                       // sqrt scale
    const light = 96 - t*58;                           // 96% -> 38%
    return `hsl(203 ${Math.round(30+t*68)}% ${Math.round(light)}%)`;
  };
  const cellFg = v => Math.sqrt(v/vmax) > .42 ? "#fff" : "#16333F";
```
**New**
```
  // EH design system v2: one sea-blue sequential ramp (pale → EH blue), √ scale; the two ends are CSS custom
  // properties (--bub-heat-lo / --bub-heat-hi, set in the skin) so light and dark themes need no redraw
  const cellBg = v => {
    if (v <= 0) return null;
    const t = Math.sqrt(v/vmax);                       // sqrt scale
    return `color-mix(in srgb, var(--bub-heat-hi) ${Math.round(
```

### 8. bub — chart text in the brand font

**Old**
```
svg.attr("font-family","Segoe UI, Tahoma, Arial, sans-serif");
```
**New**
```
svg.attr("font-family","'EH Sans','Encode Sans','Segoe UI',Tahoma,Arial,sans-serif");
```

### 9. bub — PNG export asks for the brand font first

**Old**
```
cl.setAttribute("font-family", "'Segoe UI', system-ui, Arial, sans-serif");
```
**New**
```
cl.setAttribute("font-family", "'EH Sans','Encode Sans','Segoe UI', system-ui, Arial, sans-serif");
```

### 10. bub — revenue bridge in the brand status set

**Old**
```
    {l:"2025", v:t25, abs:true, c:"#5D7793"},
    {l:"New clients", v:vNew, c:"#2BAE68", items: neu, key:d=>d.v2026},
    {l:"Expansion", v:vExp, c:"#57C785", items: ret.filter(d=>d.v2026>d.v2025), key:d=>d.v2026-d.v2025},
    {l:"Contraction", v:vCon, c:"#E0A48A", items: ret.filter(d=>d.v2025>d.v2026), key:d=>d.v2026-d.v2025},
    {l:"Churn", v:vChn, c:"#C0563F", items: los, key:d=>-d.v2025},
   
```
**New**
```
    {l:"2025", v:t25, abs:true, c:"#5E9FD6"},
    {l:"New clients", v:vNew, c:"#54AB5D", items: neu, key:d=>d.v2026},
    {l:"Expansion", v:vExp, c:"#7FB685", items: ret.filter(d=>d.v2026>d.v2025), key:d=>d.v2026-d.v2025},
    {l:"Contraction", v:vCon, c:"#D9917F", items: ret.filter(d=>d.v2025>d.v2026), key:d=>d.v2026-d.v2025},
    {l:"Churn", v:vChn, c:"#B23F2B", items: los, key:d=>-d.v2025},
   
```

### 11. bub — retention: kept clients in leaf green

**Old**
```
    {l:"Retained", n:ret.length, v:d3.sum(ret,d=>d.v2026), c:"#2BAE68",
```
**New**
```
    {l:"Retained", n:ret.length, v:d3.sum(ret,d=>d.v2026), c:"#54AB5D",
```

### 12. bub — retention: new clients in EH blue

**Old**
```
    {l:"New in 2026", n:neu.length, v:d3.sum(neu,d=>d.v2026), c:"#027DC3",
```
**New**
```
    {l:"New in 2026", n:neu.length, v:d3.sum(neu,d=>d.v2026), c:"#0072BB",
```

### 13. bub — retention: lost clients in brick

**Old**
```
    {l:"Lost after 2025", n:los.length, v:d3.sum(los,d=>d.v2025), c:"#C0563F",
```
**New**
```
    {l:"Lost after 2025", n:los.length, v:d3.sum(los,d=>d.v2025), c:"#B23F2B",
```

### 14. bub — sector shift gains/losses in the brand status colours

**Old**
```
up ? "#2BAE68" : "#C0563F"
```
**New**
```
up ? "#2E7A37" : "#B23F2B"
```

### 15. bub — sector shift 2025 hollow dots in the brand slate

**Old**
```
"#8A9BA8"
```
**New**
```
"#7D8AA0"
```

### 16. bub — sector shift legend dot in EH blue

**Old**
```
.attr("r",5.5).attr("fill","#027DC3");
```
**New**
```
.attr("r",5.5).attr("fill","#0072BB");
```

### 17. bub — chart ink: brand navy text

**Old**
```
"#16333F"
```
**New**
```
"#15224D"
```

### 18. bub — chart axes and secondary labels in ink-3

**Old**
```
"#6B7F88"
```
**New**
```
"#5E6B80"
```

### 19. bub — chart tertiary labels in ink-2

**Old**
```
"#4A5E67"
```
**New**
```
"#46546F"
```

### 20. bub — gridlines in the hairline colour

**Old**
```
"#E8EFED"
```
**New**
```
"#D9E3DF"
```

### 21. bub — bridge connector lines

**Old**
```
"#B9C6C3"
```
**New**
```
"#B8C4D0"
```

### 22. bub — depth vs value: halo, labels and median guides from the tokens

**Old**
```
  const HALO=DKQ?"#151C21":"#fff", TXT=DKQ?"#D5E0E6":"#37474F", MED=DKQ?"#4A5A64":"#B9C6CE", MEDT=DKQ?"#8FA3AE":"#8A99A3";
```
**New**
```
  const HALO=DKQ?"#15214A":"#fff", TXT=DKQ?"#E9EEF7":"#15224D", MED=DKQ?"#4A5C8C":"#B8C4D0", MEDT=DKQ?"#9DABC5":"#5E6B80";   // EH tokens
```

### 23. bub — depth vs value: quadrant colours from the brand status set

**Old**
```
  const QCOL=DKQ?{S:"#5FC98E",C:"#E3C36B",T:"#7FB4E8",X:"#93A4AF"}:{S:"#1F7A4C",C:"#B8860B",T:"#1A5FAB",X:"#8A99A3"};
```
**New**
```
  const QCOL=DKQ?{S:"#7CCB82",C:"#E8B04A",T:"#4EB0EE",X:"#9DABC5"}:{S:"#2E7A37",C:"#C98A1B",T:"#0072BB",X:"#7D8AA0"};   // EH status set
```

### 24. bub — depth vs value: axes in ink-3 / hairline

**Old**
```
  const AXL=DKQ?"#5A6B76":"#C3CED5", AXT=DKQ?"#9FB3BE":"#6B7C86";
```
**New**
```
  const AXL=DKQ?"#3A4A78":"#C9D3DE", AXT=DKQ?"#9DABC5":"#5E6B80";
```

### 25. bub — deal-size bars and text from the tokens

**Old**
```
  const BAR=DK?"#4FB0E8":"#027DC3", TXT=DK?"#E6EEF2":"#1C2B33", SUB=DK?"#9FB3BE":"#5F7078", AX=DK?"#9FB3BE":"#6B7C86", AXL=DK?"#5A6B76":"#C3CED5";
```
**New**
```
  const BAR=DK?"#4EB0EE":"#0072BB", TXT=DK?"#E9EEF7":"#15224D", SUB=DK?"#B8C4DA":"#46546F", AX=DK?"#9DABC5":"#5E6B80", AXL=DK?"#3A4A78":"#C9D3DE";   // EH tokens
```

### 26. bub — view change slides in via EH_SHARED.viewIn

**Old**
```
  closePanel();
  if (v === "heat") renderHeat(); else if (v === "exec") renderExec(); else render();
}
```
**New**
```
  closePanel();
  if (v === "heat") renderHeat(); else if (v === "exec") renderExec(); else render();
  if (window.EH_SHARED && EH_SHARED.viewIn) EH_SHARED.viewIn(document.getElementById(v === "heat" ? "heatWrap" : v === "exec" ? "execWrap" : "wrap"));
}
```

### 27. bub — dark-mode extension: hard-coded colours replaced by tokens

**Old**
```
body.dark{background:#0F1519;color:#E6EDF1}
body.dark header,body.dark .hdr,body.dark .topbar{background:#121A1F !important;border-color:#2C3A43 !important;color:#E6EDF1}
body.dark header *{color:#C9D4DB}
body.dark .ecard,body.dark .kcard{background:#151C21;border-color:#2C3A43;color:#E6EDF1}
body.dark .eh2{color:#E6EDF1}
body.dark .esub,body.dark .enote,body.dark .heatnote{color:#9FB3BE}
body.dar
```
**New**
```
/* dark mode: colours come from the eh-shared.css tokens (patch_design_bub.py) */
body.dark{background:var(--eh-mist);color:var(--eh-ink)}
body.dark header,body.dark .hdr,body.dark .topbar{border-color:var(--eh-line) !important}
body.dark .ecard,body.dark .kcard{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink)}
body.dark .eh2{color:var(--eh-ink)}
body.dark .esub,body.dark
```

### 28. bub — swipe hint chip in EH blue, logical position

**Old**
```
  .ecard::after{content:"⟷ swipe chart";position:absolute;right:10px;bottom:8px;font-size:10px;font-weight:700;color:#fff;background:#1F7A4C;padding:2px 7px;border-radius:9px;opacity:.9;pointer-events:none}
```
**New**
```
  .ecard::after{content:"⟷ swipe chart";position:absolute;inset-inline-end:10px;bottom:8px;font-size:11px;font-weight:600;color:#fff;background:#0072BB;padding:2px 8px;border-radius:999px;opacity:.92;pointer-events:none}
```

### 29. bub — zoom buttons on the token surfaces

**Old**
```
.zctl button{width:44px;height:44px;border-radius:12px;border:1px solid var(--line);background:rgba(255,255,255,.94);color:#1F2A37;font:700 20px/1 Arial,sans-serif;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.12);touch-action:manipulation}
```
**New**
```
.zctl button{width:44px;height:44px;border-radius:var(--eh-r-ctl);border:1px solid var(--eh-line);background:var(--eh-paper);color:var(--eh-ink);font:500 20px/1 var(--eh-font);cursor:pointer;box-shadow:var(--eh-shadow);touch-action:manipulation}
.zctl button:hover{border-color:var(--eh-sea);color:var(--eh-sea)}
```

### 30. bub — dark panel colours now come from the tokens in the skin

**Old**
```
body.dark .zctl button{background:rgba(24,33,38,.94);color:#E6EDF1;border-color:#3A4B55}
body.dark #panel{background:#151C21;border-color:#2C3A43;color:#E6EDF1;box-shadow:-8px 0 24px rgba(0,0,0,.45)}
body.dark .ph{border-color:#2C3A43} body.dark #pco{color:#E6EDF1}
body.dark .pline{border-color:#2C3A43;color:#E6EDF1} body.dark .pline:hover{background:#1E2830}
body.dark .sv .nm{color:#E6EDF1} body.
```
**New**
```
body.dark #panel{box-shadow:-10px 0 30px -10px rgba(0,0,0,.6)}
```
