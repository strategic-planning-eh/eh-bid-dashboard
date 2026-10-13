# Change table — Saudi waste tab

Generated 2026-10-13 15:07 · 5 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | EH_Hub.html | exact | waste-tab | Saudi waste sub-tab button after the Environment Fund report | 1 | ✓ |
| 2 | EH_Hub.html | exact | waste-tab | Skeleton + lazy iframe for the tab page | 1 | ✓ |
| 3 | EH_Hub.html | exact | waste-tab | Tab switcher knows the new frame | 1 | ✓ |
| 4 | EH_Hub.html | exact | waste-tab | Hub search opens the tab by name | 1 | ✓ |
| 5 | update-dashboard.yml | exact | waste-tab | Tab page is published | 1 | ✓ |

## Edit detail

### 1. EH_Hub.html — Saudi waste sub-tab button after the Environment Fund report

**Old**
```
<span class="tl" data-en="Environment Fund 2025 Report" data-ar="تقرير صندوق البيئة 2025">Environment Fund 2025 Report</span><span class="newb tl" data-new-until="2026-10-06" data-en="New" data-ar="جديد">New</span></button>
```
**New**
```
<span class="tl" data-en="Environment Fund 2025 Report" data-ar="تقرير صندوق البيئة 2025">Environment Fund 2025 Report</span><span class="newb tl" data-new-until="2026-10-06" data-en="New" data-ar="جديد">New</span></button>
      <button class="nsub" data-n="waste" title="Saudi waste — where the Kingdom's waste is generated and where it piles up · النفايات في المملكة — أين تتولد وأين تتراكم"><span
```

### 2. EH_Hub.html — Skeleton + lazy iframe for the tab page

**Old**
```
<iframe id="f-ef2025" title="Environment Fund 2025 Annual Report — what it means for EH" data-src="environment_fund_2025.html" loading="lazy" style="display:none"></iframe>
```
**New**
```
<iframe id="f-ef2025" title="Environment Fund 2025 Annual Report — what it means for EH" data-src="environment_fund_2025.html" loading="lazy" style="display:none"></iframe>
      <div class="skel" id="sk-waste"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading Saudi waste…" data-ar="جارٍ تحميل النفايات في المملكة…">Loading Saudi waste…</span></div></div>
      <iframe id="f
```

### 3. EH_Hub.html — Tab switcher knows the new frame

**Old**
```
['v2030','fiscal','corp','gov','pif','strat','ef2025']
```
**New**
```
['v2030','fiscal','corp','gov','pif','strat','ef2025','waste']
```

### 4. EH_Hub.html — Hub search opens the tab by name

**Old**
```
'environment fund 2025 report':'ef2025',
```
**New**
```
'environment fund 2025 report':'ef2025','saudi waste':'waste','waste statistics':'waste','hazardous waste':'waste','النفايات في المملكة':'waste',
```

### 5. update-dashboard.yml — Tab page is published

**Old**
```
          cp hub/government_news.html site/ 2>/dev/null || true

```
**New**
```
          cp hub/government_news.html site/ 2>/dev/null || true
          cp hub/saudi_waste.html site/ 2>/dev/null || true

```
