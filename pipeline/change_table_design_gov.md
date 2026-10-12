# Design system v2 — Regulatory news

Generated 2026-10-12 10:35 · 2 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | gov | exact | design | page skin after the shared design system | 1 | ✓ |
| 2 | gov | exact | design | standalone masthead contour lines | 1 | ✓ |

## Edit detail

### 1. gov — page skin after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">html body,html body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);--gov:var(--eh-sea);--blue:var(--eh-sea);--green:var(--eh-leaf);--amber:#C98A1B;--red:var(--eh-bad);background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(
```

### 2. gov — standalone masthead contour lines

**Old**
```
<header>
 <div><h1 id="title"></h1>
```
**New**
```
<header data-eh-contour="6">
 <div><h1 id="title"></h1>
```
