# Design system v2 — Government Tenders (Etimad) page (generator)

Generated 2026-10-12 10:12 · 7 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | gen | exact | design | page skin (land and sea): tokens, panels, status as word + shape, sentence-case labels | 1 | ✓ |
| 2 | gen | exact | design | skin linked after the page styles | 1 | ✓ |
| 3 | gen | exact | design | standalone masthead contour lines | 1 | ✓ |
| 4 | gen | exact | motion | shared behaviour layer: motion, text floor, embedded-mode detection | 1 | ✓ |
| 5 | gen | exact | rtl | time charts keep a left-to-right time axis in Arabic | 1 | ✓ |
| 6 | gen | exact | design | PNG export: light colours, waits for the embedded brand fonts | 1 | ✓ |
| 7 | gen | exact | design | PNG export in the brand font | 1 | ✓ |

## Edit detail

### 1. gen — page skin (land and sea): tokens, panels, status as word + shape, sentence-case labels

**Old**
```
CSS = r"""
:root{--bg:#F4F7F5;
```
**New**
```
# EH design system v2 (patch_design_etimad.py): page skin, placed after the page CSS so it wins
SKIN = r"""
/* EH design system v2 — Government Tenders skin (patch_design_etimad.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);
  --green:var(--eh-leaf-i
```

### 2. gen — skin linked after the page styles

**Old**
```
<style>{CSS}{AV.CSS}</style></head>
```
**New**
```
<style>{CSS}{AV.CSS}</style><style id="eh-skin">{SKIN}</style></head>
```

### 3. gen — standalone masthead contour lines

**Old**
```
<header><div><h1 data-en="Government Tenders (Etimad)"
```
**New**
```
<header data-eh-contour="7"><div><h1 data-en="Government Tenders (Etimad)"
```

### 4. gen — shared behaviour layer: motion, text floor, embedded-mode detection

**Old**
```
<script>{JS}{AV.JS}</script>
</body></html>
```
**New**
```
<script>{JS}{AV.JS}</script>
<script src="eh-shared.js" defer></script>
</body></html>
```

### 5. gen — time charts keep a left-to-right time axis in Arabic

**Old**
```
const ord=LANG==='ar'?cats.length-1-i:i,x=gx(ord)-bw/2;
```
**New**
```
const ord=i,x=gx(ord)-bw/2;   // EH design v2: time runs left to right in Arabic too
```

### 6. gen — PNG export: light colours, waits for the embedded brand fonts

**Old**
```
function exportPNG(id,name){const svg=$(id).querySelector('svg');if(!svg)return;const cs=getComputedStyle(document.body);
```
**New**
```
// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)
let EXFONTS=null;
function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);
 const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'
```

### 7. gen — PNG export in the brand font

**Old**
```
src=src.replace('<svg ','<svg style="font-family:Segoe UI,Tahoma,Arial,sans-serif" ')
```
**New**
```
src=src.replace('<svg ','<svg style="font-family:EH Sans,Segoe UI,Tahoma,Arial,sans-serif" ').replace(/(<svg[^>]*>)/,m=>m+'<style>'+(EXFONTS||'')+'</style>')
```
