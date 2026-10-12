# Design system v2 — hub shell

Generated 2026-10-12 09:54 · 4 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | hub | exact | design | link the shared design system and add the hub skin | 1 | ✓ |
| 2 | hub | exact | design | masthead contour lines | 1 | ✓ |
| 3 | hub | exact | design | title words split for the light/bold pairing (text unchanged) | 1 | ✓ |
| 4 | hub | exact | design | load the shared motion layer | 1 | ✓ |

## Edit detail

### 1. hub — link the shared design system and add the hub skin

**Old**
```
</style>
</head>
```
**New**
```
</style>
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — hub shell skin (patch_design_hub.py). Tokens come from eh-shared.css. */
body,body.dark{background:var(--eh-mist);color:var(--eh-ink)}
header,body.dark header{background:var(--eh-deep);border-bottom:0;padding:12px 22px 0;color:#fff;position:relative;isolation:isolate;align-items:center}
@media(min-w
```

### 2. hub — masthead contour lines

**Old**
```
<header>
  <img class="logo"
```
**New**
```
<header data-eh-contour="8">
  <img class="logo"
```

### 3. hub — title words split for the light/bold pairing (text unchanged)

**Old**
```
<h1>Strategic Intelligence Hub</h1>
```
**New**
```
<h1>Strategic Intelligence <b>Hub</b></h1>
```

### 4. hub — load the shared motion layer

**Old**
```
</body>
</html>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
</html>
```
