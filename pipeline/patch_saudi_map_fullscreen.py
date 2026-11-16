#!/usr/bin/env python3
"""16 Nov 2026 — Saudi Map (BETA) fullscreen fix (reported by Youssef).
In fullscreen the map kept its normal fixed height, so it filled only the top of the screen (black below) and stayed zoomed out.
Now the map and its side panel fill the whole screen and the view is refitted to the Kingdom (or the chosen region) on entering and leaving."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table, css_min

M = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
if 'eh-smb-fullscreen' in FILES['map']: sys.exit('Already applied.')
CSS = css_min("""<style id="eh-smb-fullscreen">
/* 16 Nov 2026: Saudi Map (BETA) fullscreen fills the screen */
#leafWrap:fullscreen{width:100vw;height:100vh;box-sizing:border-box;padding:10px;background:#F4F7F9;align-items:stretch}
html.dark #leafWrap:fullscreen{background:#0E1418}
#leafWrap:fullscreen #leafMap{height:auto !important;min-height:0;align-self:stretch}
#leafWrap:fullscreen #leafSide{max-height:none !important;height:auto;overflow-y:auto !important;align-self:stretch}
#leafWrap:-webkit-full-screen{width:100vw;height:100vh;box-sizing:border-box;padding:10px;background:#F4F7F9;align-items:stretch}
#leafWrap:-webkit-full-screen #leafMap{height:auto !important;min-height:0;align-self:stretch}
#leafWrap:-webkit-full-screen #leafSide{max-height:none !important;height:auto;overflow-y:auto !important;align-self:stretch}
@media (max-width:900px){#leafWrap:fullscreen #leafSide{max-height:32vh !important;flex:none}#leafWrap:fullscreen #leafMap{flex:1}}
</style></head>""")
OLD = "document.addEventListener('fullscreenchange',function(){if(leafMap)setTimeout(function(){leafMap.invalidateSize();},220);});"
NEW = ("function smbFsFit(){if(!leafMap)return;leafMap.invalidateSize();try{var f=(typeof SF!=='undefined'&&SF.prov!=='all')?LPROV.features.filter(function(x){return x.properties.n===SF.prov;})[0]:null;"
       "if(f)leafMap.fitBounds(L.geoJSON(f).getBounds(),{padding:[12,12]});else leafMap.fitBounds([[16.2,34.4],[32.3,55.8]],{padding:[8,8]});}catch(e){}}"
       "['fullscreenchange','webkitfullscreenchange'].forEach(function(ev){document.addEventListener(ev,function(){setTimeout(smbFsFit,120);setTimeout(smbFsFit,450);});});")
OLDF = "function leafFull(){var w=document.getElementById('leafWrap');if(document.fullscreenElement)document.exitFullscreen();else if(w.requestFullscreen)w.requestFullscreen();}"
NEWF = ("function leafFull(){var w=document.getElementById('leafWrap');var cur=document.fullscreenElement||document.webkitFullscreenElement;"
        "if(cur){(document.exitFullscreen||document.webkitExitFullscreen).call(document);}else{var rq=w.requestFullscreen||w.webkitRequestFullscreen;if(rq)rq.call(w);}}")
ok = [rep('map', '</head>', CSS, 'smb-fullscreen', 'CSS: map and side panel fill the screen in fullscreen'),
      rep('map', OLD, NEW, 'smb-fullscreen', 'Refit the view on entering/leaving fullscreen'),
      rep('map', OLDF, NEWF, 'smb-fullscreen', 'Fullscreen button: Safari fallback')]
if not all(ok): sys.exit('Patch failed — nothing written.')
with open(M, 'w', encoding='utf-8') as f: f.write(FILES['map'])
write_change_table(os.path.join(HERE, 'change_table_saudi_map_fullscreen'), 'Saudi Map (BETA) fullscreen fix')
print('done')
