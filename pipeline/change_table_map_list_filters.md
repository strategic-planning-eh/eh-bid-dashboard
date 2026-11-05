# Change table — Stakeholder Map list/filters/EMCO (5 Nov 2026)

Generated 2026-11-05 09:52 · 13 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | map | exact | list-filters | CSS: list mode hides the empty detail column; clear-all button block | 1 | ✓ |
| 2 | map | exact | list-filters | switchTab: .wrap gets .listmode while the List View is open | 1 | ✓ |
| 3 | map | exact | list-filters | Side panel: "Clear all filters" button at the top | 1 | ✓ |
| 4 | map | exact | list-filters | Side panel: "Stakeholder category" chip group (Active Competitors, Direct Competitors, EH Clients …) | 1 | ✓ |
| 5 | map | exact | list-filters | STATIC_TR: Arabic for the two new labels | 1 | ✓ |
| 6 | map | exact | list-filters | state.catg (selected stakeholder categories) | 1 | ✓ |
| 7 | map | exact | list-filters | visible(): category filter | 1 | ✓ |
| 8 | map | exact | list-filters | chipGroup: category chips labelled in the current language | 1 | ✓ |
| 9 | map | exact | list-filters | build the category chips (ring order: regulators → competitors → partners → clients → suppliers) | 1 | ✓ |
| 10 | map | exact | list-filters | applyLang: category chips re-labelled on language switch | 1 | ✓ |
| 11 | map | exact | list-filters | mobile filter badge counts the category filter | 1 | ✓ |
| 12 | map | exact | list-filters | resetFilters / Clear all filters clears the category filter too | 1 | ✓ |
| 13 | map | exact | list-filters | EMCO (شركة قياس البيئة المحدودة): note — sister company of EH | 1 | ✓ |

## Edit detail

### 1. map — CSS: list mode hides the empty detail column; clear-all button block

**Old**
```
</head>
```
**New**
```
<style id="eh-list-filters">@media(min-width:1101px){.wrap.listmode:has(#detail:not(.has)){grid-template-columns:268px minmax(0,1fr)}.wrap.listmode:has(#detail:not(.has)) #detail{display:none}.wrap.listmode #detail.has .dclose{display:flex;position:sticky;top:0;margin-inline-start:auto;width:36px;height:36px;align-items:center;justify-content:center;border:0;border-radius:18px;background:var(--eh-
```

### 2. map — switchTab: .wrap gets .listmode while the List View is open

**Old**
```
  if(t==='map')resize();
  if(t==='list')buildList();
```
**New**
```
  try{document.querySelector('.wrap').classList.toggle('listmode',t==='list');}catch(e){}
  if(t==='map')resize();
  if(t==='list')buildList();
```

### 3. map — Side panel: "Clear all filters" button at the top

**Old**
```
  <div class="panel side" id="sidePanel">
    <h3>Search company</h3>
```
**New**
```
  <div class="panel side" id="sidePanel">
    <div id="clearAllWrap"><button class="btn" id="clearAllBtn" type="button" onclick="resetFilters()">Clear all filters</button></div>
    <h3>Search company</h3>
```

### 4. map — Side panel: "Stakeholder category" chip group (Active Competitors, Direct Competitors, EH Clients …)

**Old**
```
    <h3>Company type</h3>
    <section id="catFilters"></section>
```
**New**
```
    <h3>Stakeholder category</h3>
    <section><div class="chips" id="catgChips"></div></section>
    <h3>Company type</h3>
    <section id="catFilters"></section>
```

### 5. map — STATIC_TR: Arabic for the two new labels

**Old**
```
 ['Company type','\u0646\u0648\u0639 \u0627\u0644\u0634\u0631\u0643\u0629'],
```
**New**
```
 ['Company type','\u0646\u0648\u0639 \u0627\u0644\u0634\u0631\u0643\u0629'],
 ['Stakeholder category','فئة الطرف'],
 ['Clear all filters','مسح كل الفلاتر'],
```

### 6. map — state.catg (selected stakeholder categories)

**Old**
```
const state = {cats:new Set(), regs:new Set(), tiers:new Set(), freqs:new Set(),
```
**New**
```
const state = {cats:new Set(), catg:new Set(), regs:new Set(), tiers:new Set(), freqs:new Set(),
```

### 7. map — visible(): category filter

**Old**
```
  if(!state.cats.has(n.typ||'Other'))return false;
  if(state.regs.size && !state.regs.has(n.rg))return false;
```
**New**
```
  if(!state.cats.has(n.typ||'Other'))return false;
  if(state.catg.size && !state.catg.has(n.cat))return false;
  if(state.regs.size && !state.regs.has(n.rg))return false;
```

### 8. map — chipGroup: category chips labelled in the current language

**Old**
```
ch.textContent=(elId==='regChips'?regL(v):elId==='tierChips'?tierL(v):elId==='freqChips'?freqL(v):v);
```
**New**
```
ch.textContent=(elId==='regChips'?regL(v):elId==='tierChips'?tierL(v):elId==='freqChips'?freqL(v):elId==='catgChips'?catS(v):v);
```

### 9. map — build the category chips (ring order: regulators → competitors → partners → clients → suppliers)

**Old**
```
chipGroup('tierChips',TIERS,state.tiers);
```
**New**
```
chipGroup('tierChips',TIERS,state.tiers);
const CATG_LIST=Object.keys(CAT_RING).filter(c=>c!=='EH (Reference)'&&NODES.some(n=>n.cat===c)).sort((a,b)=>CAT_RING[a]-CAT_RING[b]||a.localeCompare(b));
chipGroup('catgChips',CATG_LIST,state.catg);
```

### 10. map — applyLang: category chips re-labelled on language switch

**Old**
```
    ch.textContent=(box==='regChips'?regL(v):box==='tierChips'?tierL(v):box==='freqChips'?freqL(v):v);
```
**New**
```
    ch.textContent=(box==='regChips'?regL(v):box==='tierChips'?tierL(v):box==='freqChips'?freqL(v):box==='catgChips'?catS(v):v);
```

### 11. map — mobile filter badge counts the category filter

**Old**
```
var n=(state.cats?state.cats.size:0)+(state.regs?state.regs.size:0)
```
**New**
```
var n=(state.cats?state.cats.size:0)+(state.catg?state.catg.size:0)+(state.regs?state.regs.size:0)
```

### 12. map — resetFilters / Clear all filters clears the category filter too

**Old**
```
  state.regs.clear();state.tiers.clear();state.type='';state.sector='';state.lic='';
```
**New**
```
  state.regs.clear();state.catg.clear();state.tiers.clear();state.type='';state.sector='';state.lic='';
```

### 13. map — EMCO (شركة قياس البيئة المحدودة): note — sister company of EH

**Old**
```
"notes": "EH Relationship Score: 47/100, Tier 3 (verified — EMCO environmental lab).
```
**New**
```
"notes": "Sister company of Environmental Horizons (EH) — EMCO, Environmental Measurement Co. (شركة قياس البيئة المحدودة). EH Relationship Score: 47/100, Tier 3 (verified — EMCO environmental lab).
```
