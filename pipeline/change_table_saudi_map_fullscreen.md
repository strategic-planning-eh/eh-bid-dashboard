# Saudi Map (BETA) fullscreen fix

Generated 2026-11-16 08:51 · 3 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | map | exact | smb-fullscreen | CSS: map and side panel fill the screen in fullscreen | 1 | ✓ |
| 2 | map | exact | smb-fullscreen | Refit the view on entering/leaving fullscreen | 1 | ✓ |
| 3 | map | exact | smb-fullscreen | Fullscreen button: Safari fallback | 1 | ✓ |

## Edit detail

### 1. map — CSS: map and side panel fill the screen in fullscreen

**Old**
```
</head>
```
**New**
```
<style id="eh-smb-fullscreen">#leafWrap:fullscreen{width:100vw;height:100vh;box-sizing:border-box;padding:10px;background:#F4F7F9;align-items:stretch}html.dark #leafWrap:fullscreen{background:#0E1418}#leafWrap:fullscreen #leafMap{height:auto !important;min-height:0;align-self:stretch}#leafWrap:fullscreen #leafSide{max-height:none !important;height:auto;overflow-y:auto !important;align-self:stretch
```

### 2. map — Refit the view on entering/leaving fullscreen

**Old**
```
document.addEventListener('fullscreenchange',function(){if(leafMap)setTimeout(function(){leafMap.invalidateSize();},220);});
```
**New**
```
function smbFsFit(){if(!leafMap)return;leafMap.invalidateSize();try{var f=(typeof SF!=='undefined'&&SF.prov!=='all')?LPROV.features.filter(function(x){return x.properties.n===SF.prov;})[0]:null;if(f)leafMap.fitBounds(L.geoJSON(f).getBounds(),{padding:[12,12]});else leafMap.fitBounds([[16.2,34.4],[32.3,55.8]],{padding:[8,8]});}catch(e){}}['fullscreenchange','webkitfullscreenchange'].forEach(functio
```

### 3. map — Fullscreen button: Safari fallback

**Old**
```
function leafFull(){var w=document.getElementById('leafWrap');if(document.fullscreenElement)document.exitFullscreen();else if(w.requestFullscreen)w.requestFullscreen();}
```
**New**
```
function leafFull(){var w=document.getElementById('leafWrap');var cur=document.fullscreenElement||document.webkitFullscreenElement;if(cur){(document.exitFullscreen||document.webkitExitFullscreen).call(document);}else{var rq=w.requestFullscreen||w.webkitRequestFullscreen;if(rq)rq.call(w);}}
```
