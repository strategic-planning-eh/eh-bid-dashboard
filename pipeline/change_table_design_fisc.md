# Design system v2 — Saudi Government Finances

Generated 2026-10-12 10:19 · 15 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | fisc | exact | design | page skin after the shared design system | 1 | ✓ |
| 2 | fisc | exact | design | contour lines in the opening (standalone only) | 1 | ✓ |
| 3 | fisc | exact | design | brand chart palette | 1 | ✓ |
| 4 | fisc | exact | design | chart text in the brand font and ink; gridlines in the brand hairline colour | 1 | ✓ |
| 5 | fisc | exact | design | axis titles in the brand footnote ink | 7 | ✓ |
| 6 | fisc | exact | design | axis titles at a readable size | 7 | ✓ |
| 7 | fisc | exact | design | event markers in the brand font | 1 | ✓ |
| 8 | fisc | exact | design | chart D sector labels at a readable size | 1 | ✓ |
| 9 | fisc | exact | design | chart C pre-war bars in the brand muted grey | 1 | ✓ |
| 10 | fisc | exact | design | chart E fill from the brand navy | 1 | ✓ |
| 11 | fisc | exact | design | chart G planned bars from the brand blue | 1 | ✓ |
| 12 | fisc | exact | design | chart E reference line in the brand muted grey | 1 | ✓ |
| 13 | fisc | exact | design | chart F 2025 line in the brand muted ink | 1 | ✓ |
| 14 | fisc | exact | design | theme pass uses the brand light/dark chart colours | 1 | ✓ |
| 15 | fisc | exact | rtl | horizontal bar charts mirror in Arabic; minus signs stay in front of negative axis figures | 1 | ✓ |

## Edit detail

### 1. fisc — page skin after the shared design system

**Old**
```
<link rel="stylesheet" href="eh-shared.css">
```
**New**
```
<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Saudi Government Finances skin (patch_design_fisc.py). Tokens and fonts come from eh-shared.css.
   Rules are written as "html body …" so they also win over the page's later dark-mode block (#ehDark). */
html body,html body.dark{--navy:var(--eh-deep);--navy2:var(--eh-deep);--blue:var(--eh-sea);--blue-d:var(-
```

### 2. fisc — contour lines in the opening (standalone only)

**Old**
```
<header class="hero" id="overview">
```
**New**
```
<header class="hero" id="overview" data-eh-contour="7">
```

### 3. fisc — brand chart palette

**Old**
```
const C = {
  blue:'#0572BC', blued:'#045a96', green:'#54AB5D', grey:'#94A3B8', greyd:'#64748b',
  red:'#D32F2F', amber:'#F9A825', ragGreen:'#388E3C', navy:'#0A2A43'
};
```
**New**
```
/* EH design system v2 (patch_design_fisc.py): brand chart palette — land → sea, amber, brick for loss */
const C = {
  blue:'#0072BB', blued:'#00609E', green:'#54AB5D', grey:'#AEB9CE', greyd:'#5E6B80',
  red:'#B23F2B', amber:'#C98A1B', ragGreen:'#2E7A37', navy:'#1B2A6E'
};
```

### 4. fisc — chart text in the brand font and ink; gridlines in the brand hairline colour

**Old**
```
Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#5A6A7A';
const GRID = '#eef2f7';
```
**New**
```
Chart.defaults.font.family = "'EH Sans','Encode Sans','Segoe UI',Tahoma,Arial,sans-serif";   // brand font (Arabic glyphs come from the same family)
Chart.defaults.font.size = 12.5;
Chart.defaults.color = '#5E6B80';
Chart.defaults.plugins.tooltip.backgroundColor = '#15224D'; Chart.defaults.plugins.tooltip.padding = 10; Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip
```

### 5. fisc — axis titles in the brand footnote ink

**Old**
```
color:'#8a98a8'
```
**New**
```
color:'#5E6B80'
```

### 6. fisc — axis titles at a readable size

**Old**
```
font:{size:11,weight:'600'},color:
```
**New**
```
font:{size:12,weight:'600'},color:
```

### 7. fisc — event markers in the brand font

**Old**
```
ctx.font='700 10px Plus Jakarta Sans';
```
**New**
```
ctx.font="600 11px 'EH Sans','Encode Sans',sans-serif";
```

### 8. fisc — chart D sector labels at a readable size

**Old**
```
ticks:{font:{size:10.5},autoSkip:false}
```
**New**
```
ticks:{font:{size:11.5},autoSkip:false}
```

### 9. fisc — chart C pre-war bars in the brand muted grey

**Old**
```
backgroundColor:['#c7d2dd','#c7d2dd',C.red,C.green]
```
**New**
```
backgroundColor:[C.grey,C.grey,C.red,C.green]
```

### 10. fisc — chart E fill from the brand navy

**Old**
```
backgroundColor:'rgba(10,42,67,.06)'
```
**New**
```
backgroundColor:'rgba(27,42,110,.06)'
```

### 11. fisc — chart G planned bars from the brand blue

**Old**
```
backgroundColor:'rgba(5,114,188,.35)'
```
**New**
```
backgroundColor:'rgba(0,114,187,.3)'
```

### 12. fisc — chart E reference line in the brand muted grey

**Old**
```
borderColor:'#b8c2cf'
```
**New**
```
borderColor:'#AEB9CE'
```

### 13. fisc — chart F 2025 line in the brand muted ink

**Old**
```
borderColor:'#94A3B8', borderWidth:1.6
```
**New**
```
borderColor:'#5E6B80', borderWidth:1.6
```

### 14. fisc — theme pass uses the brand light/dark chart colours

**Old**
```
var c=dark?'#C9D4DB':'#666', g=dark?'#2C3A43':'#E5E5E5';
```
**New**
```
var c=dark?'#B8C4DA':'#5E6B80', g=dark?'#2A3A6B':'#D9E3DF';   // brand ink and hairline (eh-shared.css v2)
```

### 15. fisc — horizontal bar charts mirror in Arabic; minus signs stay in front of negative axis figures

**Old**
```
<script src="eh-ar-dashboard.js" defer></script>
```
**New**
```
<script>
/* EH design system v2 (patch_design_fisc.py): in Arabic the horizontal bar charts (B, D) read from the right —
   category labels on the right, bars grow leftwards. Time axes are left as they are. */
(function(){
  function mirror(){ var rtl=document.documentElement.dir==='rtl';
    ['chartB','chartD'].forEach(function(id){ var cv=document.getElementById(id), ch=cv&&window.Chart&&Chart.g
```
