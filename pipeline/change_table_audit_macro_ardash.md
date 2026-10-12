# Audit fixes — Arabic dashboard layer (macro)

Generated 2026-10-12 14:20 · 6 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | ard | exact | code | macro-05/12: number-only blocks are swapped when the dictionary has an Arabic version | 1 | ✓ |
| 2 | ard | exact | copy | macro-13: Arabic for the renamed growth card | 1 | ✓ |
| 3 | ard | exact | copy | macro-13: Arabic for the renamed chart E reference line | 1 | ✓ |
| 4 | ard | exact | copy | macro-02: Arabic for the relabelled oil-price card | 1 | ✓ |
| 5 | ard | exact | code | macro-07: English filter bar and methodology footer hidden in Arabic | 1 | ✓ |
| 6 | ard | exact | code | macro-07: data-eh-ar twins (KPI notes, chart note) shown in Arabic | 1 | ✓ |

## Edit detail

### 1. ard — macro-05/12: number-only blocks are swapped when the dictionary has an Arabic version

**Old**
```
if(v!=null&&/[A-Za-z]{2}/.test(el.textContent)){
```
**New**
```
if(v!=null&&(/[A-Za-z]{2}/.test(el.textContent)||v!==el.innerHTML)){
```

### 2. ard — macro-13: Arabic for the renamed growth card

**Old**
```
'Size of the economy, 2026':'حجم الاقتصاد، 2026',
```
**New**
```
'Size of the economy, 2026':'حجم الاقتصاد، 2026','Economic growth, 2026':'النمو الاقتصادي، 2026',
```

### 3. ard — macro-13: Arabic for the renamed chart E reference line

**Old**
```
'Price the budget assumed ($69.9, 2025 average)':'السعر المفترض في الميزانية (69.9 دولارًا، متوسط 2025)',
```
**New**
```
'Price the budget assumed ($69.9, 2025 average)':'السعر المفترض في الميزانية (69.9 دولارًا، متوسط 2025)','EH reference: 2025 average price ($69.9) — the Ministry publishes no oil-price assumption':'مرجع آفاق البيئة: متوسط سعر 2025 (69.9 دولارًا) — لا تنشر الوزارة سعرًا مفترضًا للنفط',
```

### 4. ard — macro-02: Arabic for the relabelled oil-price card

**Old**
```
'Oil price today (Brent, 25/08)':'سعر النفط اليوم (برنت، 25/08)'}
```
**New**
```
'Oil price today (Brent, 25/08)':'سعر النفط اليوم (برنت، 25/08)','Oil price (Brent), close on 25/08':'سعر النفط (برنت)، إغلاق 25/08'}
```

### 5. ard — macro-07: English filter bar and methodology footer hidden in Arabic

**Old**
```
enOnly:['#sec-audit','#sec-corp','#sec-gov','#sec-flag','#sec-hl','aside.panel'],
```
**New**
```
enOnly:['#sec-audit','#sec-corp','#sec-gov','#sec-flag','#sec-hl','aside.panel','#filterbar','footer.foot'],
```

### 6. ard — macro-07: data-eh-ar twins (KPI notes, chart note) shown in Arabic

**Old**
```
    relabelCharts(ar);
    if(window.EH_SHARED&&EH_SHARED.floorText) setTimeout(EH_SHARED.floorText,50);
  }
```
**New**
```
    /* audit 12/10 (macro-07): elements with an Arabic twin in data-eh-ar */
    $$('[data-eh-ar]').forEach(function(el){ if(el.dataset.ehEn==null) el.dataset.ehEn=el.innerHTML; el.innerHTML=ar?el.getAttribute('data-eh-ar'):el.dataset.ehEn; });
    relabelCharts(ar);
    if(window.EH_SHARED&&EH_SHARED.floorText) setTimeout(EH_SHARED.floorText,50);
  }
```
