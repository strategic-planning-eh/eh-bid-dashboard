"""patch_design_pif.py — EH design system v2 for the PIF annual reports page (hub/pif_intelligence_hub.html), 12 Oct 2026.

The PIF page compares five annual reports in fourteen Chart.js charts, six KPI tiles and five tables. It already loads
eh-shared.css, so this patch maps the page's own colour variables onto the shared tokens and adds a page skin:
  • standalone, the header becomes the navy masthead (contour lines, logo on a white tile, the land-to-sea line along
    its lower edge); inside the hub the logo, title and buttons are hidden by eh-shared.css and the section links that
    stay visible sit on the page colour, not on navy
  • one quiet surface system: mist page, white panels with a hairline and soft shadow, KPI tiles at 12px radius, no
    coloured header rule, section headings in deep-navy ink (not green) set in Montserrat / Alexandria
  • labels in sentence case (the KPI labels were in capitals), numbers with tabular figures, footnotes never below 12px
  • notes and the analysis box use logical borders and corners, so they mirror correctly in Arabic
  • charts: the brand palette (land → sea) read from the shared tokens, so dark mode has its own lighter set; chart
    text in the brand font (Chart.defaults.font.family) with axis text in the footnote ink and hairline gridlines;
    the two horizontal bar charts (industries, PIF's 2021 sector list) start from the right in Arabic; chart text
    is re-measured once the brand fonts finish loading
  • the eight "pools" keep green for listed Saudi companies and purple for PIF-founded companies, because the
    section text names those two colours
  • KPI figures such as "+120%" and "×3.7" are isolated left-to-right so Arabic does not move the sign to the end

Nothing visible changes in wording, numbers, links or behaviour; the chart tooltips (source and page for every
point) and the "?" (not published) cells work as before.

What it changes (exact-string edits; stops if an anchor is missing):
  • page skin <style id="eh-skin"> straight after the eh-shared.css link
  • header gets data-eh-contour; each section gets the shared eh-panel class (for the reveal-on-scroll)
  • pal() and mk(): brand palette, fonts, axis colours, Arabic mirroring of horizontal bars
  • keyword heat map in EH blue; a small script that repaints chart text after the fonts load

Run once:  python3 pipeline/patch_design_pif.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'pif_intelligence_hub.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'pif')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — PIF annual reports skin (patch_design_pif.py). Tokens and fonts come from eh-shared.css. */
/* the page's own colour variables, mapped onto the shared tokens (light and dark both follow eh-shared.css) */
:root,html[data-theme=dark]{--g:var(--eh-c2);--b:var(--eh-c1);--ink:var(--eh-ink);--grey:var(--eh-ink-2);--line:var(--eh-line);--bg:var(--eh-mist);--card:var(--eh-paper);--soft:var(--eh-tint);--noteg:var(--eh-good-bg);--noteb:var(--eh-info-bg);--heat0:var(--eh-tint);--grid:var(--eh-line)}
body{background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead (standalone) */
header{background:var(--eh-deep);border-bottom:0;padding:16px 28px 18px;gap:12px 16px;position:relative;isolation:isolate;color:#fff}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan));pointer-events:none}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header img{height:44px;background:#fff;border-radius:11px;padding:4px 6px;box-shadow:0 2px 10px -4px rgba(0,0,0,.4)}
html:root header h1{font:600 22px/1.25 var(--eh-display);color:#fff;letter-spacing:-.005em}
header p{color:rgba(255,255,255,.74);font-size:13px;margin-top:4px;max-width:96ch;line-height:1.5}
.ctl button{background:transparent;border:1px solid rgba(255,255,255,.3);color:#fff;border-radius:var(--eh-r-ctl);font:600 12.5px var(--eh-font)}
.ctl button:hover{background:rgba(255,255,255,.1)}
nav{gap:6px;padding-top:4px}
nav a{color:rgba(255,255,255,.86);border:1px solid rgba(255,255,255,.24);border-radius:var(--eh-r-chip);font:600 12.5px var(--eh-font);padding:4px 13px}
nav a:hover{background:rgba(255,255,255,.1);color:#fff}
nav a[style]{border-color:rgba(166,206,57,.55) !important;color:#D5EBA0 !important}
/* inside the hub the masthead belongs to the hub: the section links stay, on the page colour */
html.eh-embedded header,html.inframe header{background:var(--eh-mist);color:var(--eh-ink);border-bottom:1px solid var(--eh-line);padding-inline:32px}
html.eh-embedded header::after,html.inframe header::after,html.eh-embedded header>.eh-contour,html.inframe header>.eh-contour{display:none}
html.eh-embedded nav,html.inframe nav{padding-bottom:10px}
html.eh-embedded nav a,html.inframe nav a{color:var(--eh-ink-2);border-color:var(--eh-line);background:var(--eh-paper)}
html.eh-embedded nav a:hover,html.inframe nav a:hover{color:var(--eh-ink);background:var(--eh-tint)}
html.eh-embedded nav a[style],html.inframe nav a[style]{border-color:var(--eh-leaf) !important;color:var(--eh-leaf-ink) !important}
/* how-to-read box and KPI tiles: numbers lead, labels in sentence case */
.gl{display:block;font-size:13px;color:var(--eh-ink-2);background:var(--eh-tint);border:1px solid var(--eh-line);border-radius:12px;padding:11px 15px;line-height:1.6;margin-bottom:16px}
.gl b{color:var(--eh-ink)}
.kpis{gap:12px;margin-bottom:22px}
.kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
.kpi .l,[dir=rtl] .kpi .l{font-size:13px;color:var(--eh-ink-2);text-transform:none;letter-spacing:0;font-weight:500;line-height:1.35}
.kpi .v{font-size:25px;line-height:1.12;color:var(--eh-ink);margin:8px 0 5px;text-wrap:balance}
.kpi .s{font-size:12px;color:var(--eh-ink-3);line-height:1.45}
html[dir=rtl] .kpi .v{direction:ltr;unicode-bidi:isolate;text-align:right}
/* panels and headings */
section{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);padding:22px 24px;margin-bottom:20px}
html:root body h2{color:var(--eh-ink) !important}
section h2{font:600 21px/1.3 var(--eh-display);margin:0 0 6px}
section .sub{font-size:14px;color:var(--eh-ink-2);line-height:1.6;margin-bottom:16px}
h3{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);margin:18px 0 8px}
p{line-height:1.6}
.src{font-size:12px;color:var(--eh-ink-3);line-height:1.5;margin-top:10px}
.src b{color:var(--eh-ink-2)}
.note{border-inline-start:3px solid var(--eh-leaf);background:var(--eh-good-bg);border-radius:0;border-start-end-radius:10px;border-end-end-radius:10px;padding:12px 16px}
[dir=rtl] .note{border-radius:0;border-start-end-radius:10px;border-end-end-radius:10px}
.note.an{border-inline-start-color:var(--eh-sea);background:var(--eh-info-bg)}
/* view switches */
.tog{border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);background:var(--eh-paper)}
.tog button{background:transparent;color:var(--eh-ink-2);font:600 12.5px var(--eh-font);padding:5px 12px}
.tog button:hover:not(.on){background:var(--eh-tint);color:var(--eh-ink)}
html:root .tog button.on{background:#0072BB !important;color:#fff !important}
/* tables */
table{font-size:13px}
th,td{border-bottom:1px solid var(--eh-line);padding:8px 10px}
th{background:var(--eh-tint);color:var(--eh-ink-2);font-weight:600;font-size:12.5px}
table:not(.heat) tr:hover td{background:var(--eh-tint)}
.heat td.c{font-weight:600;border-radius:5px;font-variant-numeric:tabular-nums}
html:root[data-theme=dark] .c{color:var(--eh-ink-2)}
footer{color:var(--eh-ink-3);font-size:12px}
/* phone */
@media(max-width:600px){header{padding:12px 16px 14px}header img{height:34px;border-radius:9px}html:root header h1{font-size:17px}
  html.eh-embedded header,html.inframe header{padding-inline:16px}
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.kpi{padding:12px 13px}.kpi .v{font-size:20px}
  section{padding:16px 14px;border-radius:12px}section h2{font-size:18px}}
</style>'''

rep('pif', '<link rel="stylesheet" href="eh-shared.css">', SKIN, 'design', 'page skin straight after the shared design system')
rep('pif', '<header><img src="data:image/jpeg', '<header data-eh-contour="7"><img src="data:image/jpeg', 'design', 'standalone masthead contour lines')
rep('pif', '<section id="', '<section class="eh-panel" id="', 'motion', 'sections join the shared reveal-on-scroll (eh-panel)', count=10)

# charts: brand palette from the shared tokens (dark mode reads the dark set); pools keep green (index 3) and purple (index 4)
rep('pif', "const pal=()=>({g:getComputedStyle(document.documentElement).getPropertyValue('--g').trim(),b:getComputedStyle(document.documentElement).getPropertyValue('--b').trim(),ink:getComputedStyle(document.documentElement).getPropertyValue('--ink').trim(),grid:getComputedStyle(document.documentElement).getPropertyValue('--grid').trim(),gold:THEME==='dark'?'#E0B865':'#C9A24A',red:THEME==='dark'?'#E0655A':'#C0392B',lightb:THEME==='dark'?'#6FB5E8':'#8FC3E8',pool:['#3AA0E8','#2BAE68','#C9A24A','#1D9E8F','#8B7BFF','#E0655A','#8A94A0','#F28C28']});",
    "// EH design system v2 (patch_design_pif.py): brand palette, land → sea, read from eh-shared.css tokens so dark mode gets its lighter set.\n"
    "// Pools keep green (listed Saudi companies) and purple (PIF-founded companies): section 2's text names those two colours.\n"
    "const pal=()=>{const cs=getComputedStyle(document.documentElement),v=k=>cs.getPropertyValue(k).trim(),dk=THEME==='dark';\n"
    " return {g:v('--eh-c2'),b:v('--eh-c1'),ink:v('--eh-ink-2'),ink3:v('--eh-ink-3'),grid:v('--eh-line'),gold:v('--eh-c5'),red:v('--eh-c8'),lightb:dk?'#A9B6E8':'#5E9FD6',\n"
    "  pool:dk?['#4EB0EE','#E8B04A','#38C6F4','#7CCB82','#B79BDB','#F0907D','#A9B6E8','#C2E06A']:['#0072BB','#C98A1B','#00A0E0','#54AB5D','#8E6BB8','#B23F2B','#3B57B8','#A6CE39']}};",
    'design', 'brand chart palette from the shared tokens')
rep('pif', "function mk(id,cfg){const C=pal();Chart.defaults.color=C.ink;Chart.defaults.borderColor=C.grid;",
    "function mk(id,cfg){const C=pal();Chart.defaults.color=C.ink;Chart.defaults.borderColor=C.grid;Chart.defaults.font.family=getComputedStyle(document.documentElement).getPropertyValue('--eh-font').trim()||Chart.defaults.font.family;",
    'design', 'chart text in the brand font')
rep('pif', "ax.ticks=Object.assign({color:C.ink},ax.ticks||{});if(ax.title)ax.title.color=C.ink;}const ch=new Chart(",
    "ax.ticks=Object.assign({color:C.ink3},ax.ticks||{});if(ax.title)ax.title.color=C.ink;}\n"
    "if(cfg.options.indexAxis==='y'&&cfg.options.scales){const rtl=LANG==='ar';if(cfg.options.scales.x)cfg.options.scales.x.reverse=rtl;if(cfg.options.scales.y)cfg.options.scales.y.position=rtl?'right':'left';}   // Arabic: horizontal bars start from the right\n"
    "const ch=new Chart(",
    'rtl', 'axis text in the footnote ink; horizontal bar charts mirror in Arabic')
rep('pif', "`rgba(2,125,195,${0.15+0.85*q})`", "`rgba(0,114,187,${0.15+0.85*q})`", 'design', 'keyword heat map in EH blue')
rep('pif', '<script src="eh-shared.js" defer></script>',
    "<script>\n"
    "/* EH design system v2 (patch_design_pif.py): chart text is painted on canvas, which cannot swap fonts by itself. When the brand\n"
    "   fonts finish loading (first visit, or the Arabic glyphs after a language switch) the charts re-measure and repaint, without animating. */\n"
    "(function(){ if(!document.fonts||!document.fonts.addEventListener)return; var tm=null;\n"
    "  function repaint(){ clearTimeout(tm); tm=setTimeout(function(){ (typeof CH!=='undefined'?CH:[]).forEach(function(c){ try{ Object.values(c.scales||{}).forEach(function(s){ s._longestTextCache={}; }); c.stop(); c.update('none'); }catch(e){} }); },60); }\n"
    "  document.fonts.addEventListener('loadingdone',repaint); document.fonts.ready.then(repaint); })();\n"
    "</script>\n<script src=\"eh-shared.js\" defer></script>",
    'design', 'repaint chart text once the brand fonts have loaded')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['pif'])
write_change_table(os.path.join(HERE, 'change_table_design_pif'), 'Design system v2 — PIF annual reports')
print('patched: hub/pif_intelligence_hub.html')
