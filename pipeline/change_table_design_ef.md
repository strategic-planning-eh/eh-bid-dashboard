# Design system v2 — Environment Fund 2025 page (generator)

Generated 2026-10-12 10:17 · 19 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | gen | exact | design | page skin (land and sea): tokens, panels, chips with word + shape, sentence-case labels | 1 | ✓ |
| 2 | gen | exact | design | skin linked after the page styles | 1 | ✓ |
| 3 | gen | exact | design | standalone masthead contour lines | 1 | ✓ |
| 4 | gen | exact | design | chart text in token colours, series in the brand palette, label column fits the longest label | 1 | ✓ |
| 5 | gen | exact | design | better / worse marks in the shared status colours | 1 | ✓ |
| 6 | gen | exact | rtl | helpers: palette map, shared label column, Arabic mirroring, label contrast | 1 | ✓ |
| 7 | gen | exact | rtl | charts mirrored in Arabic | 1 | ✓ |
| 8 | gen | exact | rtl | programme map mirrored in Arabic (reads right to left, like its Arabic title) | 1 | ✓ |
| 9 | gen | exact | design | programme map in the brand palette | 1 | ✓ |
| 10 | gen | exact | design | programme map title in the token ink | 1 | ✓ |
| 11 | gen | exact | design | programme map source line in the token footnote colour | 1 | ✓ |
| 12 | gen | exact | design | programme labels readable on every box colour | 1 | ✓ |
| 13 | gen | exact | design | centre boxes in token colours | 1 | ✓ |
| 14 | gen | exact | design | EH service boxes in token colours | 1 | ✓ |
| 15 | gen | exact | design | programme boxes fit their longest label | 1 | ✓ |
| 16 | gen | exact | design | PNG export waits for the embedded brand fonts | 1 | ✓ |
| 17 | gen | exact | design | PNG export: light colours and brand fonts | 1 | ✓ |
| 18 | gen | exact | design | PNG export background always white | 1 | ✓ |
| 19 | gen | exact | motion | opportunity tabs use the shared view transition | 1 | ✓ |

## Edit detail

### 1. gen — page skin (land and sea): tokens, panels, chips with word + shape, sentence-case labels

**Old**
```
"""

JS = r"""

```
**New**
```
"""

# EH design system v2 (patch_design_ef.py): page skin, placed after the page CSS so it wins
SKIN = r"""
/* EH design system v2 — Environment Fund skin (patch_design_ef.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);
  --green:var(--eh-leaf-ink);-
```

### 2. gen — skin linked after the page styles

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
<style>{CSS}</style>

```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style>{CSS}</style>
<style id="eh-skin">{SKIN}</style>

```

### 3. gen — standalone masthead contour lines

**Old**
```
<header>
 <div><h1 id="title"></h1>
```
**New**
```
<header data-eh-contour="7">
 <div><h1 id="title"></h1>
```

### 4. gen — chart text in token colours, series in the brand palette, label column fits the longest label

**Old**
```
 const W=1100, rowH=34, L0=430, iw=W-L0-190, ink=DARK?'#E6EDF1':'#16333F', mut='#6B7C86';

```
**New**
```
 const W=1100, rowH=34, L0=EF_L0(), iw=W-L0-190, ink='var(--eh-ink)', mut='var(--eh-ink-3)';   // EH design v2: token colours follow the theme
 c=Object.assign({},c,{color:BC(c.color),colors:(c.colors||[]).map(BC),rows:c.rows.map(r=>r.c?Object.assign({},r,{c:BC(r.c)}):r)});

```

### 5. gen — better / worse marks in the shared status colours

**Old**
```
<tspan fill="${better?'#1F7A4C':'#C0504D'}">
```
**New**
```
<tspan fill="${better?'var(--eh-good)':'var(--eh-bad)'}">
```

### 6. gen — helpers: palette map, shared label column, Arabic mirroring, label contrast

**Old**
```
function chart(c){

```
**New**
```
// EH design system v2 (patch_design_ef.py): brand palette (land → sea) for the colours stored in the report data
const BCM={'#2A3F80':'#3B57B8','#E8862E':'#C98A1B','#1F7A4C':'#54AB5D','#C0504D':'#B23F2B','#1A5FAB':'#0072BB','#2E9E8E':'#00A0E0','#5F7078':'#5E6B80','#7B4FA6':'#8E6BB8','#9AABB5':'#9DABC5'};
const BC=x=>BCM[String(x||'').toUpperCase()]||x;
// one label column for every chart, wide en
```

### 7. gen — charts mirrored in Arabic

**Old**
```
${chart(c)}</div>`).join('');
```
**New**
```
${mir(chart(c))}</div>`).join('');
```

### 8. gen — programme map mirrored in Arabic (reads right to left, like its Arabic title)

**Old**
```
 $('pmwrap').innerHTML=programmeMap();
```
**New**
```
 $('pmwrap').innerHTML=mir(programmeMap());
```

### 9. gen — programme map in the brand palette

**Old**
```
 const col={grants:'#1F7A4C',loansup:'#2A3F80',guar:'#1A5FAB',impact:'#7B4FA6',ppp:'#E8862E',fees:'#C0504D',shared:'#5F7078',carbon:'#2E9E8E'};
```
**New**
```
 const col={grants:'#2E7A37',loansup:'#3B57B8',guar:'#0072BB',impact:'#8E6BB8',ppp:'#C98A1B',fees:'#B23F2B',shared:'#5E6B80',carbon:'#00A0E0'};   // EH brand palette
```

### 10. gen — programme map title in the token ink

**Old**
```
<text x="${xP}" y="24" font-size="15" font-weight="800" fill="${DARK?'#E6EDF1':'#16333F'}">
```
**New**
```
<text x="${xP}" y="24" font-size="15" font-weight="800" fill="var(--eh-ink)">
```

### 11. gen — programme map source line in the token footnote colour

**Old**
```
<text x="${xP}" y="42" font-size="11" fill="#6B7C86">
```
**New**
```
<text x="${xP}" y="42" font-size="11" fill="var(--eh-ink-3)">
```

### 12. gen — programme labels readable on every box colour

**Old**
```
font-size="12.5" font-weight="700" fill="#fff">${esc(L(p.en,p.ar))}</text><text x="${xP+bw[0]-8}" y="${yP(i)+19}" font-size="10" fill="#fff"
```
**New**
```
font-size="12.5" font-weight="700" fill="${onFill(col[p.id])}">${esc(L(p.en,p.ar))}</text><text x="${xP+bw[0]-8}" y="${yP(i)+19}" font-size="10.5" fill="${onFill(col[p.id])}"
```

### 13. gen — centre boxes in token colours

**Old**
```
fill="${DARK?'#1E2830':'#F0F5F2'}" stroke="${DARK?'#3A4B55':'#DCE8DF'}"/><text x="${xC+bw[1]/2}" y="${yC(i)+18}" font-size="12" font-weight="700" fill="${DARK?'#E6EDF1':'#16333F'}"
```
**New**
```
fill="var(--eh-tint)" stroke="var(--eh-line)"/><text x="${xC+bw[1]/2}" y="${yC(i)+18}" font-size="12" font-weight="700" fill="var(--eh-ink)"
```

### 14. gen — EH service boxes in token colours

**Old**
```
fill="${DARK?'#1E2830':'#fff'}" stroke="#1F7A4C" stroke-width="1.5"/><text x="${xE+10}" y="${yE(i)+18}" font-size="12.5" font-weight="700" fill="${DARK?'#E6EDF1':'#1F7A4C'}">
```
**New**
```
fill="var(--eh-paper)" stroke="var(--eh-leaf-ink)" stroke-width="1.5"/><text x="${xE+10}" y="${yE(i)+18}" font-size="12.5" font-weight="700" fill="var(--eh-leaf-ink)">
```

### 15. gen — programme boxes fit their longest label

**Old**
```
const xP=40,xC=W/2-40,xE=W-300, bw=[250,120,200];
```
**New**
```
const xP=40,xC=W/2-40,xE=W-300, bw=[310,150,200];   // EH design v2: programme and centre boxes wide enough for the longest label (English and Arabic) in the brand font
```

### 16. gen — PNG export waits for the embedded brand fonts

**Old**
```
function exPNG(id,name){const svg=$(id);if(!svg)return;
```
**New**
```
// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)
let EXFONTS=null;
function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);
 const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'
```

### 17. gen — PNG export: light colours and brand fonts

**Old**
```
 cl.querySelectorAll('text').forEach(t=>t.setAttribute('font-family',"'Segoe UI',Tahoma,Arial,sans-serif"));

```
**New**
```
 // read every colour as the light theme draws it, so the PNG is ink on white in either theme
 const dk=document.body.classList.contains('dark');if(dk)document.body.classList.remove('dark');
 const se=[...svg.querySelectorAll('*')],ce=[...cl.querySelectorAll('*')];
 se.forEach((e,i)=>{const d=ce[i];if(!d||!/^(text|tspan|rect|path|line|circle)$/.test(e.tagName))return;const cs=getComputedStyle(e);d
```

### 18. gen — PNG export background always white

**Old**
```
bg.setAttribute('fill',DARK?'#151C21':'#fff');
```
**New**
```
bg.setAttribute('fill','#fff');
```

### 19. gen — opportunity tabs use the shared view transition

**Old**
```
onclick="GROUP='${k}';render()"
```
**New**
```
onclick="GROUP='${k}';render();window.EH_SHARED&&EH_SHARED.viewIn($('opps'))"
```
