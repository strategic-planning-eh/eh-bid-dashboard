# Change table — Saudi ports tab

Generated 2026-11-01 10:06 · 5 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | EH_Hub.html | exact | ports-tab | Saudi ports sub-tab button after Saudi waste | 1 | ✓ |
| 2 | EH_Hub.html | exact | ports-tab | Skeleton + lazy iframe for the tab page | 1 | ✓ |
| 3 | EH_Hub.html | exact | ports-tab | Tab switcher knows the new frame | 1 | ✓ |
| 4 | EH_Hub.html | exact | ports-tab | Hub search opens the tab by name | 1 | ✓ |
| 5 | update-dashboard.yml | exact | ports-tab | Tab page is published | 1 | ✓ |

## Edit detail

### 1. EH_Hub.html — Saudi ports sub-tab button after Saudi waste

**Old**
```
<span class="newb tl" data-new-until="2026-10-27" data-en="New" data-ar="جديد">New</span></button>
```
**New**
```
<span class="newb tl" data-new-until="2026-10-27" data-en="New" data-ar="جديد">New</span></button>
      <button class="nsub" data-n="ports" title="Saudi ports — operators, capacities, waste reception and EH's position at each port · الموانئ السعودية — المشغّلون والطاقات واستقبال النفايات وموقع آفاق البيئة في كل ميناء"><span class="tl" data-en="Saudi ports" data-ar="الموانئ السعودية">Saudi ports</
```

### 2. EH_Hub.html — Skeleton + lazy iframe for the tab page

**Old**
```
<iframe id="f-waste" title="Saudi waste — where the Kingdom's waste is generated and where it piles up" data-src="saudi_waste.html" loading="lazy" style="display:none"></iframe>
```
**New**
```
<iframe id="f-waste" title="Saudi waste — where the Kingdom's waste is generated and where it piles up" data-src="saudi_waste.html" loading="lazy" style="display:none"></iframe>
      <div class="skel" id="sk-ports"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading Saudi ports…" data-ar="جارٍ تحميل الموانئ السعودية…">Loading Saudi ports…</span></div></div>
      <iframe id=
```

### 3. EH_Hub.html — Tab switcher knows the new frame

**Old**
```
['v2030','fiscal','corp','gov','pif','strat','ef2025','waste']
```
**New**
```
['v2030','fiscal','corp','gov','pif','strat','ef2025','waste','ports']
```

### 4. EH_Hub.html — Hub search opens the tab by name

**Old**
```
'saudi waste':'waste',
```
**New**
```
'saudi waste':'waste','saudi ports':'ports','ports map':'ports','saudi ports intelligence map':'ports','الموانئ السعودية':'ports',
```

### 5. update-dashboard.yml — Tab page is published

**Old**
```
          cp hub/saudi_waste.html site/ 2>/dev/null || true

```
**New**
```
          cp hub/saudi_waste.html site/ 2>/dev/null || true
          cp hub/saudi_ports_map.html site/ 2>/dev/null || true

```
