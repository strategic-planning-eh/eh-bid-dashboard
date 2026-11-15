# Change table — Saudi Map (BETA): bidders, tenders, Vision 2030 projects and EH sites at real locations (15 Nov 2026)

Generated 2026-11-15 15:26 · 12 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | map | exact | saudi-map-beta | File header comment describes the new tab and where its data lives | 1 | ✓ |
| 2 | map | exact | saudi-map-beta | Tab label: Saudi Map (BETA) | 1 | ✓ |
| 3 | map | exact | saudi-map-beta | Tab label in Arabic: خريطة السعودية (تجريبي) | 1 | ✓ |
| 4 | map | exact | saudi-map-beta | New data block SMB (filled by embed_saudi_map_data.py) | 1 | ✓ |
| 5 | map | exact | saudi-map-beta | CSS: markers, legend, region strip, not-found list, popup (light, dark, RTL, print) | 1 | ✓ |
| 6 | map | regex | saudi-map-beta | Removed: Schematic (offline) mode — buildGeoSchematic and its zoom/pan helpers (geoV, geoApply, geoZoom, geoReset, geoLayers, geoOutside); nothing else called them | 1 | ✓ |
| 7 | map | regex | saudi-map-beta | Removed: the old position table (LGEO, LGEO_POS, LGEO_SRC, LGEO_RG), region centres (LREGC), leafBuild/leafFeat and the "estimated position" wording. GEO_SITES now holds the four EH sites; SMB data block is read | 1 | ✓ |
| 8 | map | regex | saudi-map-beta | Tab shell rebuilt: BETA banner, bar (fullscreen, exports, About), located / not-located counts, region strip and "Location not found" list. Removed: LF filter state, setGeoMode, the Interactive / Schematic buttons, the old About text | 1 | ✓ |
| 9 | map | regex | saudi-map-beta | Map rebuilt: layer switches (Bidders, Tenders, Vision 2030 projects, Roads, Region outline), bidder circles sized by tenders shared and coloured by worst outcome with a ring cue, tender diamonds by result, Vision 2030 sites, SIRC as PIF company, EH sites on top; popups; region strip; not-found list. Removed: category / tier / minimum-score / data-confidence filters and the "Has bid against EH only" box (leafSidebar, leafPass, leafPopup, leafSel, leafRefresh, leafToggle, leafReset) | 1 | ✓ |
| 10 | map | exact | saudi-map-beta | exportXlsx: the old Saudi Map branch (all pinned companies with the removed filters) is gone | 1 | ✓ |
| 11 | map | exact | saudi-map-beta | exportXlsx: CSV fallback no longer calls the removed leafExport | 1 | ✓ |
| 12 | map | regex | saudi-map-beta | Exports rebuilt: Excel (Bidders, Tenders, Vision 2030, EH sites, Location not found, README), GeoJSON and CSV of the layers shown; "Location not found" list exports as EH_Bidders_Location_Not_Found.xlsx | 1 | ✓ |

## Edit detail

### 1. map — File header comment describes the new tab and where its data lives

**Old**
```
  EH Stakeholder & Competitive Landscape Map - with interactive Leaflet Saudi Map tab
  SETUP: open this file in any modern browser. No server or build step required.
  The "Saudi Map" tab loads Leaflet 1.9.4 + MarkerCluster from cdnjs and OpenStreetMap tiles,
  so that tab needs an internet connection; every other tab works fully offline.
  DEPLOY: upload this single file to GitHub Pages / Netlif
```
**New**
```
  EH Stakeholder & Competitive Landscape Map - with the interactive "Saudi Map (BETA)" tab
  SETUP: open this file in any modern browser. No server or build step required.
  The "Saudi Map (BETA)" tab loads Leaflet 1.9.4 + MarkerCluster (cdnjs, then the copy in vendor/) and OpenStreetMap tiles,
  so its base map needs an internet connection; every other tab works fully offline.
  DEPLOY: upload th
```

### 2. map — Tab label: Saudi Map (BETA)

**Old**
```
<div class="tab" id="tabGeo" onclick="switchTab('geo')">Saudi Map</div>
```
**New**
```
<div class="tab" id="tabGeo" onclick="switchTab('geo')">Saudi Map (BETA)</div>
```

### 3. map — Tab label in Arabic: خريطة السعودية (تجريبي)

**Old**
```
 ['Saudi Map','\u062e\u0631\u064a\u0637\u0629 \u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629'],
```
**New**
```
 ['Saudi Map (BETA)','\u062e\u0631\u064a\u0637\u0629 \u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629 (\u062a\u062c\u0631\u064a\u0628\u064a)'],
```

### 4. map — New data block SMB (filled by embed_saudi_map_data.py)

**Old**
```
<script id="LIC" type="application/json">
```
**New**
```
<script id="SMB" type="application/json">{}</script>
<script id="LIC" type="application/json">
```

### 5. map — CSS: markers, legend, region strip, not-found list, popup (light, dark, RTL, print)

**Old**
```
</head>
```
**New**
```
<style id="eh-saudi-map-beta">#leafBanner b.smb-beta{display:inline-block;background:var(--eh-sea,#0072BB);color:#fff;border-radius:999px;padding:0 8px;margin-inline-end:6px;font-size:10.5px;letter-spacing:.4px}#smbCount{margin-inline-start:auto;font-size:12px;color:var(--eh-ink-2,#51626D)}#smbCount b{color:var(--eh-sea,#1A5FAB)}#smbShow{font-size:12px;color:var(--eh-ink-2,#51626D);margin:0 0 6px}
```

### 6. map — Removed: Schematic (offline) mode — buildGeoSchematic and its zoom/pan helpers (geoV, geoApply, geoZoom, geoReset, geoLayers, geoOutside); nothing else called them

**Old**
```
let geoV=\{k:1,x:0,y:0\}, geoEl=null, geoDrag=null;\n.*?\n\}\n\nfunction buildList\(\)\{
```
**New**
```
<fn>
```

### 7. map — Removed: the old position table (LGEO, LGEO_POS, LGEO_SRC, LGEO_RG), region centres (LREGC), leafBuild/leafFeat and the "estimated position" wording. GEO_SITES now holds the four EH sites; SMB data block is read

**Old**
```
/\* =+ SAUDI MAP TAB: interactive Leaflet app \+ schematic fallback =+ \*/\nlet geoMode='leaf'.*?\nfunction posL\(s\)\{[^\n]*\}\n\n
```
**New**
```
<fn>
```

### 8. map — Tab shell rebuilt: BETA banner, bar (fullscreen, exports, About), located / not-located counts, region strip and "Location not found" list. Removed: LF filter state, setGeoMode, the Interactive / Schematic buttons, the old About text

**Old**
```
const LF=\{prov:'all',tiers:null.*?\n(?=function loadLeaflet\(ok,fail\)\{)
```
**New**
```
<fn>
```

### 9. map — Map rebuilt: layer switches (Bidders, Tenders, Vision 2030 projects, Roads, Region outline), bidder circles sized by tenders shared and coloured by worst outcome with a ring cue, tender diamonds by result, Vision 2030 sites, SIRC as PIF company, EH sites on top; popups; region strip; not-found list. Removed: category / tier / minimum-score / data-confidence filters and the "Has bid against EH only" box (leafSidebar, leafPass, leafPopup, leafSel, leafRefresh, leafToggle, leafReset)

**Old**
```
function leafSidebar\(\)\{.*?\nfunction leafFull\(\)\{[^\n]*\}\n
```
**New**
```
<fn>
```

### 10. map — exportXlsx: the old Saudi Map branch (all pinned companies with the removed filters) is gone

**Old**
```
  if(scope==='leaf'&&typeof LSTAKE!=='undefined'){
    var names={}; LSTAKE.features.filter(function(f){return leafPass(f.properties);}).forEach(function(f){names[f.properties.n]=1;});
    rows=NODES.filter(function(n){return names[n.n];});
    filters=[]; if(LF.prov!=='all')filters.push([t('Province','المنطقة الإدارية'),LF.prov]); var onK=function(o){return o?Object.keys(o).filter(function(k){ret
```
**New**
```
  rows=VIS.slice(); filters=xlsFilters(); label=t('Current filters','المرشّحات الحالية');   // the Saudi Map (BETA) has its own export (smbExport)

```

### 11. map — exportXlsx: CSV fallback no longer calls the removed leafExport

**Old**
```
function(){ done(); if(scope==='leaf'){leafExport('csv');} else { xlsCsvFallback(rows); } alert(
```
**New**
```
function(){ done(); xlsCsvFallback(rows); alert(
```

### 12. map — Exports rebuilt: Excel (Bidders, Tenders, Vision 2030, EH sites, Location not found, README), GeoJSON and CSV of the layers shown; "Location not found" list exports as EH_Bidders_Location_Not_Found.xlsx

**Old**
```
function leafExport\(kind\)\{.*?\n\}\n\n(?=/\* =+ ASK THE MAP)
```
**New**
```
<fn>
```
