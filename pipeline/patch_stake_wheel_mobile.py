"""patch_stake_wheel_mobile.py — keep the Stakeholder Map wheel round on phones and tablets (hub/EH_Stakeholder_Map_CURRENT.html), 12 Oct 2026.

What was wrong
  On screens up to 1100px wide the page's own CSS shows the wheel canvas as a square (width 100%, aspect-ratio 1/1,
  capped at 70vh / 78vh), but the script's resize() sized the drawing from the box of #mapView, which stays 560px tall
  (the .viewbox minimum). So a 360 x 560 drawing was squeezed into a 360 x 360 box: the wheel came out as a flattened
  ellipse, a large empty band sat under it, and taps landed on the wrong company because the tap position was read in
  the squeezed box but matched against the unsqueezed drawing. On a 768 tablet the 70vh cap also made the box itself
  slightly off-square (738 x 717). The "Showing companies that bid against EH only…" note is placed with absolute
  position over the top of the map, so on a narrow screen it covered the upper part of the wheel.
  Separately, the selected-company ring in dot() read a colour flag (DKM) that only exists inside draw(), so selecting
  a company threw "DKM is not defined" and stopped the redraw half-way.

What this patch does
  • resize() now sizes the drawing from the canvas's own box, so the drawing always has the shape it is shown at.
    On desktop the canvas fills #mapView exactly as before, so nothing changes there.
  • on a square canvas the wheel leaves a margin of a tenth of its width (at least the old 34px) so the outer region
    labels are not cut off on a tablet; the wide desktop canvas keeps its old radius.
  • a ResizeObserver redraws the wheel whenever the canvas box itself changes size (not only on window resize).
  • up to 1100px wide: the canvas is a true square, min(100%, 78vh) wide (70vh on phones up to 768px; the full height
    minus the toolbar in short landscape), centred; the map view sits in the page flow instead of being pinned to the
    560px box, so there is no empty band under the wheel; and the note sits above the wheel in the flow (same words,
    same hide button), clear of the zoom buttons, and the zoom hint sits under the wheel rather than on it.
  • the selected-company ring works out light/dark itself, so tap-to-select draws again.
  Pan, pinch, wheel zoom, double-click zoom, hover tooltips and tap-to-select are unchanged — they already worked in
  the canvas's own pixels, which now match the drawing.

Data safety: pipeline/sync_bids_to_apps.py and refresh_map_banalytics.py rewrite the
<script id="DATA|LIC|BANALYTICS" type="application/json"> blocks on every publish. Nothing here touches those blocks or
their tags; every edit is an exact-string replacement in the page script or a new <style> before </head>, and the
script stops if any anchor is missing or a data block changes. Windows line endings (CRLF) are kept.

Run once:  python3 pipeline/patch_stake_wheel_mobile.py
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table, css_min

P = os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html')
if 'id="eh-wheel-mobile"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'stake')

def blocks(s):
    return re.findall(r'<script id="(?:DATA|LIC|BANALYTICS)" type="application/json">.*?</script>', s, re.S)
BEFORE = blocks(FILES['stake'])

WHEEL_CSS = css_min(r'''<style id="eh-wheel-mobile">
/* Stakeholder Map wheel on phones and tablets (patch_stake_wheel_mobile.py): a true square canvas, centred, in the
   page flow; the "bid against EH only" note sits above it instead of over it. Desktop (over 1100px) is unchanged. */
@media(max-width:1100px){
  .viewbox:not(:has(>#mapView[style*="none"])){min-height:0}
  #mapView{position:relative;inset:auto;padding-bottom:34px}   /* room for the zoom hint under the wheel */
  #mapView:not([style*="none"]){display:flex !important;flex-direction:column}
  #cv{width:min(100%,78vh) !important;height:auto !important;aspect-ratio:1/1;max-height:none !important;margin-inline:auto;flex:none}
  #tier1Note{order:-1;position:relative !important;top:auto !important;left:auto !important;right:auto !important;margin:10px 64px 8px 12px}
}
@media(max-width:768px){
  #cv{width:min(100%,70vh) !important}
}
@media (orientation:landscape) and (max-height:520px) and (max-width:1100px){
  #cv{width:min(100%,calc(100vh - 120px)) !important}
}
</style>''')

rep('stake', '</head>', WHEEL_CSS + '</head>', 'layout',
    'phones/tablets: square, centred wheel canvas in the page flow; note above the wheel, not over it')
rep('stake', "  const box=document.getElementById('mapView').getBoundingClientRect();\n",
    "  const box=cv.getBoundingClientRect();   // size the drawing to the canvas's own box so the wheel stays round (phones show it as a square)\n",
    'bug', 'wheel drawing sized from the canvas box, not the 560px map box (root cause of the ellipse and mis-aimed taps)')
rep('stake', "window.addEventListener('resize',resize);\n",
    "window.addEventListener('resize',resize);\n"
    "if(window.ResizeObserver){let _cw=0,_ch=0;new ResizeObserver(function(){const b=cv.getBoundingClientRect(),w=Math.round(b.width),h=Math.round(b.height);if(w&&(w!==_cw||h!==_ch)){_cw=w;_ch=h;resize();}}).observe(cv);}   // redraw when the canvas box itself changes size\n",
    'bug', 'wheel redrawn whenever the canvas box changes size')
rep('stake', "CX=W/2;CY=H/2;R=Math.max(20,Math.min(W,H)/2-34);draw();",
    "CX=W/2;CY=H/2;R=Math.max(20,Math.min(W,H)/2-(W<H*1.1?Math.max(34,Math.min(W,H)*0.1):34));draw();   // square canvas (phones/tablets): leave room for the region labels",
    'layout', 'square canvas keeps a proportional margin so the outer region labels are not cut off at 768px; desktop radius unchanged')
rep('stake', "ctx.lineWidth=2.2;ctx.strokeStyle=(DKM?'#E9EEF7':'#15224D');",
    "ctx.lineWidth=2.2;ctx.strokeStyle=(document.documentElement.classList.contains('dark')?'#E9EEF7':'#15224D');",
    'bug', 'selected-company ring no longer throws "DKM is not defined" (tap-to-select redraws again)')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
if blocks(FILES['stake']) != BEFORE:
    sys.exit('ABORT: a data block changed — nothing written.')
CRLF = b'\r\n' in open(P, 'rb').read(4096)   # the published file uses Windows line endings; keep them
open(P, 'w', encoding='utf-8', newline='\r\n' if CRLF else '\n').write(FILES['stake'])
write_change_table(os.path.join(HERE, 'change_table_stake_wheel_mobile'), 'Stakeholder Map — round wheel on phones and tablets')
print('patched: hub/EH_Stakeholder_Map_CURRENT.html')
