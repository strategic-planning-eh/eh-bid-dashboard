# Clear all filters shows nothing

Generated 2026-11-16 09:19 · 4 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | map | exact | clear-all | Side panel button calls the new function | 1 | ✓ |
| 2 | map | exact | clear-all | New clearAllFilters(): unticks every company type | 1 | ✓ |
| 3 | map | exact | clear-all | Empty-state message matches the new behaviour | 1 | ✓ |
| 4 | map | exact | clear-all | Arabic for the empty-state message | 1 | ✓ |

## Edit detail

### 1. map — Side panel button calls the new function

**Old**
```
<button class="btn" id="clearAllBtn" type="button" onclick="resetFilters()">Clear all filters</button>
```
**New**
```
<button class="btn" id="clearAllBtn" type="button" onclick="clearAllFilters()">Clear all filters</button>
```

### 2. map — New clearAllFilters(): unticks every company type

**Old**
```

function resetFilters(){

```
**New**
```

function clearAllFilters(){   /* 16 Nov 2026: clear = nothing ticked, nothing shown */
    resetFilters(); state.cats.clear();
    document.querySelectorAll('#catFilters input[type=checkbox]').forEach(function(i){i.checked=false;});
    state.sel=null; recompute();
}
function resetFilters(){

```

### 3. map — Empty-state message matches the new behaviour

**Old**
```
The map opens with <b>no filters selected</b>.<br>Tick company types in the Filters panel to populate it — or<br>
```
**New**
```
<p style="margin:0;font-weight:700;color:#1C2B33">No company types are selected.</p><p style="margin:4px 0 0">Tick company types in the Filters panel to show companies — or</p>
```

### 4. map — Arabic for the empty-state message

**Old**
```
const STATIC_TR=[
```
**New**
```
const STATIC_TR=[['No company types are selected.','لم يُحدَّد أي نوع من الشركات.'],['Tick company types in the Filters panel to show companies — or','حدّد أنواع الشركات من لوحة الفلاتر لعرض الشركات — أو'],['Show everything','عرض الكل'],
```
