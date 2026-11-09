# Change table — Stakeholder Map Export to Excel (9 Nov 2026)

Generated 2026-11-09 16:00 · 7 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | map | exact | map-export | CSS: export buttons | 1 | ✓ |
| 2 | map | exact | map-export | Header: Export to Excel button | 1 | ✓ |
| 3 | map | exact | map-export | STATIC_TR: Export to Excel | 1 | ✓ |
| 4 | map | exact | map-export | anchor check | 1 | ✓ |
| 5 | map | exact | map-export | List View: Export to Excel button on the count line | 1 | ✓ |
| 6 | map | exact | map-export | JS: exportXlsx, xlsCols, xlsFilters, xlsWrite, CSV fallback | 1 | ✓ |
| 7 | map | exact | map-export | Saudi Map bar: Excel export of the geo-filtered set | 1 | ✓ |

## Edit detail

### 1. map — CSS: export buttons

**Old**
```
</head>
```
**New**
```
<style id="eh-map-export">#xlsBtn svg,.lxls svg{width:14px;height:14px;vertical-align:-2px;margin-inline-end:5px}.lcount .lxls{margin-inline-start:12px;padding:3px 10px;font-size:12px;vertical-align:middle}#xlsBtn[disabled],.lxls[disabled]{opacity:.55;cursor:progress}</style></head>
```

### 2. map — Header: Export to Excel button

**Old**
```
    <button class="btn" onclick="resetFilters()">Reset filters</button>
    <button class="btn" id="langBtn"
```
**New**
```
    <button class="btn" onclick="resetFilters()">Reset filters</button>
    <button class="btn" id="xlsBtn" type="button" onclick="exportXlsx('list')" title="Download the companies currently shown as an Excel workbook"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17
```

### 3. map — STATIC_TR: Export to Excel

**Old**
```
const STATIC_TR=[
```
**New**
```
const STATIC_TR=[['Export to Excel','\u062a\u0635\u062f\u064a\u0631 \u0625\u0644\u0649 Excel'],
```

### 4. map — anchor check

**Old**
```
click any row for detail · click a column to re-sort','<b>'+rows.length.toLocaleString()+'</b> شركة معروضة — 
```
**New**
```
click any row for detail · click a column to re-sort','<b>'+rows.length.toLocaleString()+'</b> شركة معروضة — 
```

### 5. map — List View: Export to Excel button on the count line

**Old**
```
  const lv=document.getElementById('listView'); lv.innerHTML=h;
```
**New**
```
  h=h.replace('</div><table class="ltbl">','<button type="button" class="btn lxls" onclick="exportXlsx(\'list\')"><svg aria-hidden=\"true\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2\"/></svg>'+t('Export to Excel','تصدير إلى Excel')+'</butt
```

### 6. map — JS: exportXlsx, xlsCols, xlsFilters, xlsWrite, CSV fallback

**Old**
```
function leafExport(kind){
```
**New**
```
// ---- Export to Excel (9 Nov 2026): the rows passing the current filters, in whatever tab ----
var XLSX_URL='https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
function ldXlsx(ok,bad){ if(window.XLSX)return ok(); var s=document.createElement('script'); s.src=XLSX_URL; s.onload=ok; s.onerror=bad; document.head.appendChild(s); }
function xlsFilters(){
  var f=[]; var S=state;
  
```

### 7. map — Saudi Map bar: Excel export of the geo-filtered set

**Old**
```
<button class="leafbtn" onclick="leafExport(\'geojson\')">\u2b07 GeoJSON</button>
```
**New**
```
<button class="leafbtn" onclick="exportXlsx(\'leaf\')">\u2b07 Excel</button><button class="leafbtn" onclick="leafExport(\'geojson\')">\u2b07 GeoJSON</button>
```
