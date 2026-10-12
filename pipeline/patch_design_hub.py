"""patch_design_hub.py — EH design system v2 for the hub shell (hub/EH_Hub.html), 12 Oct 2026.

The hub's header becomes the one signature moment of the whole product: a deep-navy masthead with EH's
bathymetric contour lines (drawn once on load), the logo on its own white tile, the title set the way the EH
company profile sets its headings (Montserrat light + bold), and the section tabs cut out of the navy like folder
tabs so the active one runs straight into the page below. A thin land-to-sea line (leaf green → EH blue) runs
along the masthead's lower edge and follows reading direction. Everything else in the shell takes the shared
tokens from eh-shared.css v2, so light/dark and English/Arabic come from one place.

Motion: switching a section slides the incoming view in from the reading-start edge (mirrored in Arabic);
the What's New panel already slides from the inline end; theme and language changes ease via eh-shared.js.

What it changes (exact-string edits; stops if an anchor is missing):
  • links eh-shared.css + adds the page skin after the shell's own styles
  • title words wrapped so the light/bold pairing can be styled (text unchanged)
  • masthead gets data-eh-contour; eh-shared.js loaded at the end of the body

Run once:  python3 pipeline/patch_design_hub.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

H = os.path.join(HERE, '..', 'hub', 'EH_Hub.html')
if 'id="eh-skin"' in open(H, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(H, 'hub')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — hub shell skin (patch_design_hub.py). Tokens come from eh-shared.css. */
body,body.dark{background:var(--eh-mist);color:var(--eh-ink)}
header,body.dark header{background:var(--eh-deep);border-bottom:0;padding:12px 22px 0;color:#fff;position:relative;isolation:isolate;align-items:center}
@media(min-width:821px) and (min-height:521px){
  header{display:grid;grid-template-columns:auto minmax(0,1fr) auto auto auto auto auto auto;column-gap:10px;row-gap:4px;align-items:center}
  header>img.logo{grid-row:1;grid-column:1}
  .brand{grid-row:1;grid-column:2;min-width:0}
  .fresh{grid-row:1;grid-column:3}
  #hsearch{grid-row:1;grid-column:4}
  #wnbtn{grid-row:1;grid-column:5}
  #themebtn{grid-row:1;grid-column:6}
  #langbtn{grid-row:1;grid-column:7}
  header>button[onclick*="hubFS"]{grid-row:1;grid-column:8}
  .tabs{grid-row:2;grid-column:1/-1;margin-inline-start:-6px;justify-content:flex-start}
  .brand .desc{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
}
body.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;z-index:-1;opacity:.55}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan));z-index:1;pointer-events:none}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header>img.logo{height:44px;background:#fff;border-radius:11px;padding:4px 6px;margin-block:2px 12px;box-shadow:0 2px 10px -4px rgba(0,0,0,.4)}
.brand{color:#fff;margin-bottom:10px;line-height:1.3}
@media(min-width:641px){.brand small{display:inline !important;margin-inline-end:10px}}
.brand h1,body.dark .brand h1{font:300 21px/1.2 var(--eh-display);color:#fff;letter-spacing:-.005em;display:block}
.brand h1 b{font-weight:700}
.brand small,body.dark .brand small{color:rgba(255,255,255,.72);font-weight:500;font-size:11.5px;letter-spacing:0}
.brand .desc,body.dark .brand .desc{color:rgba(255,255,255,.7)}
.conf,body.dark .conf{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);color:#FFD9CF;text-transform:none;letter-spacing:0;font-weight:600;font-size:11px;border-radius:999px;padding:2px 10px}
.fresh,body.dark .fresh{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.18);color:rgba(255,255,255,.8);margin-bottom:10px}
.fresh b,body.dark .fresh b{color:#A8E3AD}
header #langbtn,header #wnbtn,header #themebtn,header .hbtn,header button:not(.tab),
body.dark header #langbtn,body.dark header #wnbtn,body.dark header #themebtn,body.dark header button:not(.tab){background:transparent !important;border:1px solid rgba(255,255,255,.28) !important;color:#fff !important;border-radius:var(--eh-r-ctl) !important;margin-bottom:10px}
header button:not(.tab):hover,body.dark header button:not(.tab):hover{background:rgba(255,255,255,.1) !important}
header #q,body.dark header #q{background:rgba(255,255,255,.1) !important;border:1px solid rgba(255,255,255,.26) !important;color:#fff !important;border-radius:var(--eh-r-ctl) !important;margin-bottom:10px}
header #q::placeholder{color:rgba(255,255,255,.66)}
#qdrop{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;color:var(--eh-ink)}
#qdrop .qh{color:var(--eh-ink);border-bottom-color:var(--eh-line) !important}
#qdrop .qh:hover,#qdrop .qh:focus{background:var(--eh-tint) !important}
.tabs{align-self:flex-end;gap:2px}
.tab,body.dark .tab{color:rgba(255,255,255,.78);border:0;border-radius:11px 11px 0 0;box-shadow:none;font:600 13.5px var(--eh-font);padding:11px 18px 12px}
.tab:hover:not(.on),body.dark .tab:hover:not(.on){background:rgba(255,255,255,.09);color:#fff}
.tab.on,body.dark .tab.on{background:var(--eh-mist);color:var(--eh-ink);box-shadow:none}
body.dark header .tab{background:transparent !important;border:0 !important;color:rgba(255,255,255,.78) !important}
body.dark header .tab:hover:not(.on){background:rgba(255,255,255,.09) !important;color:#fff !important}
body.dark header .tab.on{background:var(--eh-mist) !important;color:var(--eh-ink) !important}
.tab.on .ic{color:var(--eh-leaf-ink)}
#kpis{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink-2)}
#kpis b{color:var(--eh-ink)}
iframe,body.dark iframe{background:var(--eh-mist)}
.skel,body.dark .skel{background:var(--eh-mist)}
.skel .in{color:var(--eh-ink-2)}
.spin{border-color:var(--eh-line);border-top-color:var(--eh-sea)}
.foot,body.dark .foot{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink-3)}
#newsbar,body.dark #newsbar{background:var(--eh-mist) !important;border-bottom:1px solid var(--eh-line) !important;padding:10px 16px !important;gap:6px}
.nsub,body.dark .nsub{background:transparent !important;border:1px solid var(--eh-line) !important;color:var(--eh-ink-2) !important;border-radius:var(--eh-r-chip);font:600 12.5px var(--eh-font);padding:7px 14px}
.nsub:hover:not(.on){background:var(--eh-tint) !important;color:var(--eh-ink) !important}
.nsub.on,body.dark .nsub.on{background:var(--eh-sea) !important;border-color:var(--eh-sea) !important;color:#fff !important}
.nsub .newb,.wnbadge{background:var(--eh-leaf-ink)}
nav.mtabs,body.dark .mtabs{background:var(--eh-paper);border-top-color:var(--eh-line)}
.mtab,body.dark .mtab{color:var(--eh-ink-2)}
.mtab.on,body.dark .mtab.on{color:var(--eh-sea);box-shadow:inset 0 3px 0 var(--eh-sea)}
#wnpanel,body.dark #wnpanel{background:var(--eh-paper);color:var(--eh-ink)}
.wnhd,.wnweeks,.wntabs,body.dark .wnhd,body.dark .wnweeks,body.dark .wntabs{border-color:var(--eh-line)}
.wnhd h2,body.dark .wnhd h2{font:600 19px var(--eh-display);color:var(--eh-ink)}
.wnx,body.dark .wnx{background:transparent !important;border-color:var(--eh-line) !important;color:var(--eh-ink-2) !important}
.wnfresh,.wnh,.wntot,.wnempty{color:var(--eh-ink-2)}.wnfresh b{color:var(--eh-leaf-ink)}.wntot b{color:var(--eh-ink)}
.wnh{text-transform:none;letter-spacing:0;font-size:12.5px}
.wnitem,body.dark .wnitem{color:var(--eh-ink);border-inline-start-color:var(--eh-line);font-size:13.5px;line-height:1.6}
.wnitem.major{border-inline-start-color:var(--eh-sea)}.wnitem.minor{border-inline-start-color:var(--eh-leaf)}
.wnitem .app{color:var(--eh-sea-ink);text-transform:none;letter-spacing:0;font-size:11.5px}
.wnitem a,.wnitem button.lnk{color:var(--eh-sea)}
.wnweek,body.dark .wnweek{background:transparent;border-color:var(--eh-line);color:var(--eh-ink-2)}
.wnweek.on,body.dark .wnweek.on{background:var(--eh-sea);border-color:var(--eh-sea);color:#fff}
.wnweek .n{background:var(--eh-good-bg);color:var(--eh-good)}
.wntab{color:var(--eh-ink-2)}.wntab[aria-selected="true"]{color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}
.wnmonth{color:var(--eh-ink-2);text-transform:none;letter-spacing:0}
#wnov{background:rgba(13,23,54,.5)}
@media(max-width:640px){nav.mtabs{grid-template-columns:repeat(5,1fr)}.mtab{font-size:11.5px}.brand h1,body.dark .brand h1{font-size:15px;display:block}header{padding:8px 10px}header>img.logo{height:30px;margin:0;padding:3px 4px;border-radius:8px}.brand{margin:0}.brand h1{font-size:15px}header button,header #q{margin-bottom:0}.tab{border-radius:9px}}
@media (prefers-reduced-motion:no-preference){
  html:not([data-eh-motion="off"]) main>iframe.on,html:not([data-eh-motion="off"]) #newswrap iframe.vis{animation:ehViewIn var(--eh-dur-2) var(--eh-ease) both}
  html:not([data-eh-motion="off"]) .tab{transition:background-color var(--eh-dur-1) var(--eh-ease),color var(--eh-dur-1) var(--eh-ease)}
}
</style>
</head>'''

rep('hub', '</style>\n</head>', '</style>\n' + SKIN, 'design', 'link the shared design system and add the hub skin')
rep('hub', '<header>\n  <img class="logo"', '<header data-eh-contour="8">\n  <img class="logo"', 'design', 'masthead contour lines')
rep('hub', '<h1>Strategic Intelligence Hub</h1>', '<h1>Strategic Intelligence <b>Hub</b></h1>', 'design', 'title words split for the light/bold pairing (text unchanged)')
rep('hub', '</body>\n</html>', '<script src="eh-shared.js" defer></script>\n</body>\n</html>', 'design', 'load the shared motion layer')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(H, 'w', encoding='utf-8').write(FILES['hub'])
write_change_table(os.path.join(HERE, 'change_table_design_hub'), 'Design system v2 — hub shell')
print('patched: hub/EH_Hub.html')
