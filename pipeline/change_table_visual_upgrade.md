# Change table — Stage B visual upgrade

Generated 2026-09-07 12:47 · 38 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | stake | exact | shared-layer | EH_Stakeholder_Map_CURRENT.html: load eh-shared.css | 1 | ✓ |
| 2 | stake | exact | shared-layer | EH_Stakeholder_Map_CURRENT.html: load eh-shared.js | 1 | ✓ |
| 3 | bids | exact | shared-layer | EH_Bid_Analysis_CURRENT.html: load eh-shared.css | 1 | ✓ |
| 4 | bids | exact | shared-layer | EH_Bid_Analysis_CURRENT.html: load eh-shared.js | 1 | ✓ |
| 5 | bub | exact | shared-layer | EH_Client_Bubble_Map_CURRENT.html: load eh-shared.css | 1 | ✓ |
| 6 | bub | exact | shared-layer | EH_Client_Bubble_Map_CURRENT.html: load eh-shared.js | 1 | ✓ |
| 7 | news | exact | shared-layer | eh_news_intelligence.html: load eh-shared.css | 1 | ✓ |
| 8 | news | exact | shared-layer | eh_news_intelligence.html: load eh-shared.js | 1 | ✓ |
| 9 | v2030 | exact | shared-layer | vision2030_dashboard.html: load eh-shared.css | 1 | ✓ |
| 10 | v2030 | exact | shared-layer | vision2030_dashboard.html: load eh-shared.js | 1 | ✓ |
| 11 | fisc | exact | shared-layer | saudi_fiscal_monitor_2026.html: load eh-shared.css | 1 | ✓ |
| 12 | fisc | exact | shared-layer | saudi_fiscal_monitor_2026.html: load eh-shared.js | 1 | ✓ |
| 13 | pif | exact | shared-layer | pif_intelligence_hub.html: load eh-shared.css | 1 | ✓ |
| 14 | pif | exact | shared-layer | pif_intelligence_hub.html: load eh-shared.js | 1 | ✓ |
| 15 | strat | exact | shared-layer | pif_strategy_2026_2030.html: load eh-shared.css | 1 | ✓ |
| 16 | strat | exact | shared-layer | pif_strategy_2026_2030.html: load eh-shared.js | 1 | ✓ |
| 17 | v2030 | regex | fonts | vision2030_dashboard.html: remove Google Fonts links (D-B5) | 3 | ✓ |
| 18 | fisc | regex | fonts | saudi_fiscal_monitor_2026.html: remove Google Fonts links (D-B5) | 3 | ✓ |
| 19 | news | regex | fonts | eh_news_intelligence.html: remove Google Fonts links (D-B5) | 3 | ✓ |
| 20 | stake | exact | ten-second | Stakeholder map: default Tier 1 view + note instead of zeros and an empty map | 1 | ✓ |
| 21 | bub | exact | plain-language | Bubble map: tap is the first verb (lesson #7) | 1 | ✓ |
| 22 | pif | exact | plain-language | PIF hub: drop the GICS acronym from the reader-facing sentence | 2 | ✓ |
| 23 | bids | exact | ten-second | Bid KPI strip: win rate, total tendered value, open pipeline first and marked hero (D-B4) | 1 | ✓ |
| 24 | bids | exact | ten-second | Bid KPI strip: hero tile styling (served copy) | 1 | ✓ |
| 25 | hub | exact | bilingual | Hub skeleton text bilingual: Loading the stakeholder map… | 1 | ✓ |
| 26 | hub | exact | bilingual | Hub skeleton text bilingual: Loading bid intelligence… | 1 | ✓ |
| 27 | hub | exact | bilingual | Hub skeleton text bilingual: Loading the client portfolio… | 1 | ✓ |
| 28 | hub | exact | bilingual | Hub skeleton text bilingual: Loading Vision 2030… | 1 | ✓ |
| 29 | hub | exact | bilingual | Hub skeleton text bilingual: Loading Fiscal Monitor… | 1 | ✓ |
| 30 | hub | exact | bilingual | Hub skeleton text bilingual: Loading News… | 1 | ✓ |
| 31 | hub | exact | bilingual | Hub skeleton text bilingual: Loading PIF Hub… | 1 | ✓ |
| 32 | hub | exact | bilingual | Hub skeleton text bilingual: Loading PIF Strategy 2026–2030… | 1 | ✓ |
| 33 | hub | exact | motion | Hub: 180 ms cross-fade when a frame is shown (reduced-motion safe) | 1 | ✓ |
| 34 | hub | exact | motion | Hub nGo(): mark the visible News frame so the cross-fade can run | 1 | ✓ |
| 35 | gen | exact | shared-layer | build_bid_dashboard.py: emit eh-shared.css link | 1 | ✓ |
| 36 | gen | exact | shared-layer | build_bid_dashboard.py: emit eh-shared.js script | 1 | ✓ |
| 37 | gen | exact | ten-second | build_bid_dashboard.py: hero tile CSS (this CSS block is a plain string in the generator) | 1 | ✓ |
| 38 | wf | exact | publish | Workflow: publish eh-shared.css and eh-shared.js | 1 | ✓ |

## Edit detail

### 1. stake — EH_Stakeholder_Map_CURRENT.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 2. stake — EH_Stakeholder_Map_CURRENT.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 3. bids — EH_Bid_Analysis_CURRENT.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 4. bids — EH_Bid_Analysis_CURRENT.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 5. bub — EH_Client_Bubble_Map_CURRENT.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 6. bub — EH_Client_Bubble_Map_CURRENT.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 7. news — eh_news_intelligence.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 8. news — eh_news_intelligence.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 9. v2030 — vision2030_dashboard.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 10. v2030 — vision2030_dashboard.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 11. fisc — saudi_fiscal_monitor_2026.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 12. fisc — saudi_fiscal_monitor_2026.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 13. pif — pif_intelligence_hub.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 14. pif — pif_intelligence_hub.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 15. strat — pif_strategy_2026_2030.html: load eh-shared.css

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 16. strat — pif_strategy_2026_2030.html: load eh-shared.js

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 17. v2030 — vision2030_dashboard.html: remove Google Fonts links (D-B5)

**Old**
```
\s*<link[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>
```
**New**
```

```

### 18. fisc — saudi_fiscal_monitor_2026.html: remove Google Fonts links (D-B5)

**Old**
```
\s*<link[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>
```
**New**
```

```

### 19. news — eh_news_intelligence.html: remove Google Fonts links (D-B5)

**Old**
```
\s*<link[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>
```
**New**
```

```

### 20. stake — Stakeholder map: default Tier 1 view + note instead of zeros and an empty map

**Old**
```
<script src="eh-shared.js" defer></script>
</body>
```
**New**
```
<script>/* default view (visual upgrade 07/09): Tier 1 shown on open, with a note; Reset filters shows the old empty gate */
setTimeout(function(){try{if(!state.cats.size&&!state.tiers.size){CATS.forEach(function(c){state.cats.add(c.id);});document.querySelectorAll('#catFilters input').forEach(function(i){i.checked=true;});state.tiers.add('Tier 1');chipGroup('tierChips',TIERS,state.tiers);recomput
```

### 21. bub — Bubble map: tap is the first verb (lesson #7)

**Old**
```
hover any dot for the name and numbers.
```
**New**
```
tap or hover any dot for the name and numbers.
```

### 22. pif — PIF hub: drop the GICS acronym from the reader-facing sentence

**Old**
```
PIF uses a standard international industry list (called GICS)
```
**New**
```
PIF uses a standard international industry list
```

### 23. bids — Bid KPI strip: win rate, total tendered value, open pipeline first and marked hero (D-B4)

**Old**
```
function rKPI(){$('kstrip').innerHTML=
 kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),'2024–2026')+
 kc('SAR '+fmtM(k.pipeline),t('Total tendered value','إجمالي قيمة المنافسات'),k.with_value+t(' priced',' مُسعّرة'))+
 kc('SAR '+fmtM(k.open_pipeline),t('Open pipeline','المحفظة المفتوحة'),k.open_count+t(' pending',' قيد الانتظار'))+
 kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/
```
**New**
```
function rKPI(){$('kstrip').innerHTML=
 kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/'+k.awarded+t(' awarded',' مُرساة'),(k.win_rate>=50?'g':'r')+' hero')+
 kc('SAR '+fmtM(k.pipeline),t('Total tendered value','إجمالي قيمة المنافسات'),k.with_value+t(' priced',' مُسعّرة'),'hero')+
 kc('SAR '+fmtM(k.open_pipeline),t('Open pipeline','المحفظة المفتوحة'),k.open_count+t(' pending',' قيد الانت
```

### 24. bids — Bid KPI strip: hero tile styling (served copy)

**Old**
```
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}
```
**New**
```
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}
.kc:has(.v.hero){grid-column:span 2;border-top-width:4px}.kc .v.hero{font-size:34px}.kc:has(.v.hero) .l{font-size:12.5px;font-weight:700}@media(max-width:700px){.kc:has(.v.hero){grid-column:span 1}.kc .v.hero{font-size:26px}}
```

### 25. hub — Hub skeleton text bilingual: Loading the stakeholder map…

**Old**
```
<div class="spin"></div>Loading the stakeholder map…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading the stakeholder map…" data-ar="جارٍ تحميل خريطة أصحاب المصلحة…">Loading the stakeholder map…</span>
```

### 26. hub — Hub skeleton text bilingual: Loading bid intelligence…

**Old**
```
<div class="spin"></div>Loading bid intelligence…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading bid intelligence…" data-ar="جارٍ تحميل استخبارات المناقصات…">Loading bid intelligence…</span>
```

### 27. hub — Hub skeleton text bilingual: Loading the client portfolio…

**Old**
```
<div class="spin"></div>Loading the client portfolio…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading the client portfolio…" data-ar="جارٍ تحميل محفظة العملاء…">Loading the client portfolio…</span>
```

### 28. hub — Hub skeleton text bilingual: Loading Vision 2030…

**Old**
```
<div class="spin"></div>Loading Vision 2030…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading Vision 2030…" data-ar="جارٍ تحميل رؤية 2030…">Loading Vision 2030…</span>
```

### 29. hub — Hub skeleton text bilingual: Loading Fiscal Monitor…

**Old**
```
<div class="spin"></div>Loading Fiscal Monitor…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading Fiscal Monitor…" data-ar="جارٍ تحميل مرصد المالية…">Loading Fiscal Monitor…</span>
```

### 30. hub — Hub skeleton text bilingual: Loading News…

**Old**
```
<div class="spin"></div>Loading News…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading News…" data-ar="جارٍ تحميل الأخبار…">Loading News…</span>
```

### 31. hub — Hub skeleton text bilingual: Loading PIF Hub…

**Old**
```
<div class="spin"></div>Loading PIF Hub…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading PIF Hub…" data-ar="جارٍ تحميل مركز الصندوق…">Loading PIF Hub…</span>
```

### 32. hub — Hub skeleton text bilingual: Loading PIF Strategy 2026–2030…

**Old**
```
<div class="spin"></div>Loading PIF Strategy 2026–2030…
```
**New**
```
<div class="spin"></div><span class="tl" data-en="Loading PIF Strategy 2026–2030…" data-ar="جارٍ تحميل استراتيجية الصندوق 2026–2030…">Loading PIF Strategy 2026–2030…</span>
```

### 33. hub — Hub: 180 ms cross-fade when a frame is shown (reduced-motion safe)

**Old**
```
.nsub.on{background:var(--green);border-color:var(--green);color:#fff}
```
**New**
```
.nsub.on{background:var(--green);border-color:var(--green);color:#fff}
@media (prefers-reduced-motion:no-preference){@keyframes ehIn{from{opacity:0}to{opacity:1}} main>iframe.on,#newswrap iframe.vis{animation:ehIn 180ms ease-out}}
```

### 34. hub — Hub nGo(): mark the visible News frame so the cross-fade can run

**Old**
```
    f.style.display=on?'block':'none';
```
**New**
```
    f.style.display=on?'block':'none';f.classList.toggle('vis',on);
```

### 35. gen — build_bid_dashboard.py: emit eh-shared.css link

**Old**
```
</head>
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
</head>
```

### 36. gen — build_bid_dashboard.py: emit eh-shared.js script

**Old**
```
</body>
```
**New**
```
<script src="eh-shared.js" defer></script>
</body>
```

### 37. gen — build_bid_dashboard.py: hero tile CSS (this CSS block is a plain string in the generator)

**Old**
```
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}
```
**New**
```
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}
.kc:has(.v.hero){grid-column:span 2;border-top-width:4px}.kc .v.hero{font-size:34px}.kc:has(.v.hero) .l{font-size:12.5px;font-weight:700}@media(max-width:700px){.kc:has(.v.hero){grid-column:span 1}.kc .v.hero{font-size:26px}}
```

### 38. wf — Workflow: publish eh-shared.css and eh-shared.js

**Old**
```
          cp hub/pif_strategy_2026_2030.html site/ 2>/dev/null || true

```
**New**
```
          cp hub/pif_strategy_2026_2030.html site/ 2>/dev/null || true
          cp hub/eh-shared.css hub/eh-shared.js site/ 2>/dev/null || true

```
