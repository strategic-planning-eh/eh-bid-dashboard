"""patch_design_strat.py — EH design system v2 for the PIF Strategy 2026–2030 page (hub/pif_strategy_2026_2030.html), 12 Oct 2026.

The strategy page sets PIF's 2026–2030 plan against the annual reports: ten sections, eight KPI tiles, 146 tap-to-cite
figures (tap one to see the document and page it came from), a sector-shift diagram drawn in SVG, two Chart.js bar
charts, and "Not published" wherever PIF gives no number. It already loads eh-shared.css; this patch maps the page's
own colour variables onto the shared tokens and adds a page skin, matching the companion annual-reports page:
  • standalone, the header becomes the navy masthead (contour lines, logo on a white tile, land-to-sea line); inside
    the hub only the section links stay, on the page colour
  • mist page, white panels with a hairline, 12px KPI tiles, headings in deep-navy ink set in Montserrat / Alexandria,
    no coloured header rule; the six ecosystem cards are quiet white cards, with EH's own ecosystem (05) picked out
    by a leaf-green outline
  • labels in sentence case (KPI labels and the ecosystem card labels were in capitals); footnotes at 12px or more
  • status chips, relevance and exposure cells, the SIRC tag and the warning flags take the shared status colours,
    each still shown with its word; the "Not published" badge keeps its dashed outline
  • the source popover becomes a white card with a blue edge; the tap-to-cite underline stays EH blue
  • sector-shift diagram in brand colours and fonts; arrows in "From … → to …" point the reading way in Arabic
  • charts: chart text in the brand font with axis text in the footnote ink, colours from the shared tokens (green =
    did it, red = fell short, as the legend says); both charts are horizontal bars and start from the right in Arabic

Nothing visible changes in wording, numbers, links or behaviour.

What it changes (exact-string edits; stops if an anchor is missing):
  • page skin <style id="eh-skin"> straight after the eh-shared.css link
  • header gets data-eh-contour; each section gets the shared eh-panel class (for the reveal-on-scroll)
  • pal(), drawAll()'s chart defaults and mk(): token colours, axis colours, Arabic mirroring of horizontal bars
  • a small script that repaints chart text after the brand fonts load

Run once:  python3 pipeline/patch_design_strat.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'pif_strategy_2026_2030.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'strat')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — PIF Strategy 2026–2030 skin (patch_design_strat.py). Tokens and fonts come from eh-shared.css. */
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
nav a.xl{border-color:rgba(166,206,57,.55);color:#D5EBA0}
/* inside the hub the masthead belongs to the hub: the section links stay, on the page colour */
html.eh-embedded header,html.inframe header{background:var(--eh-mist);color:var(--eh-ink);border-bottom:1px solid var(--eh-line);padding-inline:32px}
html.eh-embedded header::after,html.inframe header::after,html.eh-embedded header>.eh-contour,html.inframe header>.eh-contour{display:none}
html.eh-embedded nav,html.inframe nav{padding-bottom:10px}
html.eh-embedded nav a,html.inframe nav a{color:var(--eh-ink-2);border-color:var(--eh-line);background:var(--eh-paper)}
html.eh-embedded nav a:hover,html.inframe nav a:hover{color:var(--eh-ink);background:var(--eh-tint)}
html.eh-embedded nav a.xl,html.inframe nav a.xl{border-color:var(--eh-leaf);color:var(--eh-leaf-ink)}
/* how-to-read box, the "no fund-wide target" note, KPI tiles */
.gl{display:block;font-size:13px;color:var(--eh-ink-2);background:var(--eh-tint);border:1px solid var(--eh-line);border-radius:12px;padding:11px 15px;line-height:1.6;margin-bottom:16px}
.gl b{color:var(--eh-ink)}
.kpis{gap:12px;margin-bottom:22px}
.kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
.kpi .l,[dir=rtl] .kpi .l{font-size:13px;color:var(--eh-ink-2);text-transform:none;letter-spacing:0;font-weight:500;line-height:1.35}
.kpi .v{font-size:24px;line-height:1.15;color:var(--eh-ink);margin:8px 0 5px;text-wrap:balance}
.kpi.kn .v{font-size:16px}
html[dir=rtl] .kpi .v{line-height:1.32}
.kpi .s{font-size:12px;color:var(--eh-ink-3);line-height:1.45}
.kpi .conf,[data-theme=dark] .kpi .conf{color:var(--eh-warn);font-size:12px}
/* panels and headings */
section{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);padding:22px 24px;margin-bottom:20px}
html:root body h2{color:var(--eh-ink) !important}
section h2{font:600 21px/1.3 var(--eh-display);margin:0 0 6px}
section .sub{font-size:14px;color:var(--eh-ink-2);line-height:1.6;margin-bottom:16px}
h3{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);margin:18px 0 8px}
p{line-height:1.6}
.src{font-size:12px;color:var(--eh-ink-3);line-height:1.55;margin-top:10px}
.src b{color:var(--eh-ink-2)}
.note{border-inline-start:3px solid var(--eh-leaf);background:var(--eh-good-bg);border-radius:0;border-start-end-radius:10px;border-end-end-radius:10px;padding:12px 16px}
[dir=rtl] .note{border-radius:0;border-start-end-radius:10px;border-end-end-radius:10px}
.note.an,.note.d3{border-inline-start-color:var(--eh-sea);background:var(--eh-info-bg)}
.note.d3{font-size:14.5px;line-height:1.6;margin-bottom:18px}
/* tap-to-cite figures and their source popover; "Not published" keeps its dashed outline */
.cite{border-bottom:1px dotted var(--eh-sea)}
.cite sup{color:var(--eh-sea);font-size:10px}
.pop{background:var(--eh-paper);color:var(--eh-ink);border:1px solid var(--eh-line);border-inline-start:3px solid var(--eh-sea);border-radius:10px;padding:10px 14px;font-size:13px;line-height:1.5;box-shadow:0 14px 34px -14px rgba(13,23,54,.38)}
.none{border:1.5px dashed var(--eh-ink-3);color:var(--eh-ink-2);border-radius:6px;font-weight:600}
.nf{background:var(--eh-tint);border:1px dashed var(--eh-ink-3);border-radius:var(--eh-r-chip);color:var(--eh-ink-2);font-size:12.5px;padding:3px 11px}
/* status chips: the word plus the shared status colours */
.chip{font-size:11.5px;border-radius:var(--eh-r-chip);padding:2px 9px;line-height:1.5}
.chip.grey{background:var(--eh-muted-bg);color:var(--eh-muted);border-color:transparent}
.chip.blue{background:var(--eh-info-bg);color:var(--eh-info)}
.chip.green{background:var(--eh-good-bg);color:var(--eh-good)}
.chip.red,[data-theme=dark] .chip.red{background:var(--eh-bad-bg);color:var(--eh-bad)}
.chip.gold,[data-theme=dark] .chip.gold{background:var(--eh-warn-bg);color:var(--eh-warn)}
/* the plan in brief */
.shift{font-size:14px;border-bottom-color:var(--eh-line)}
.shift .arr{color:var(--eh-leaf-ink)}
[dir=rtl] .shift .arr{display:inline-block;transform:scaleX(-1)}
.shift b{color:var(--eh-sea)}
#obj li{font-size:13.5px;border-bottom-color:var(--eh-line)}
#obj .num{color:var(--eh-leaf-ink);font-family:var(--eh-display);font-weight:600;font-variant-numeric:tabular-nums}
.port{border-bottom-color:var(--eh-line)}
.port b{color:var(--eh-sea);font-family:var(--eh-display);font-weight:600}
.port p{font-size:13px;color:var(--eh-ink-2)}
/* ecosystem cards */
.ecogrid{gap:14px}
.eco{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:16px}
.eco.eco5{border-color:var(--eh-leaf);box-shadow:inset 0 0 0 1px var(--eh-leaf)}
.ehead .en{font-family:var(--eh-display);font-weight:600;font-size:22px;color:var(--eh-leaf-ink);font-variant-numeric:tabular-nums}
.ehead b{color:var(--eh-ink);font-family:var(--eh-display);font-weight:600;font-size:15px;line-height:1.35}
.ehead .tag{font-size:12.5px;color:var(--eh-ink-2)}
.ef{font-size:13px;line-height:1.55}
.ef .lbl,[dir=rtl] .ef .lbl{font-size:12px;text-transform:none;letter-spacing:0;color:var(--eh-ink-3);font-weight:600}
.ef.hook{color:var(--eh-sea-ink)}
.co{background:var(--eh-tint);border-radius:var(--eh-r-chip);padding:2px 9px;font-size:12px;margin:2px 0;margin-inline-end:4px}
.co.sirc,[data-theme=dark] .co.sirc{background:var(--eh-bad-bg);color:var(--eh-bad)}
.flag{background:var(--eh-warn-bg);border-inline-start:3px solid var(--eh-amber);border-radius:0;border-start-end-radius:8px;border-end-end-radius:8px;color:var(--eh-ink);font-size:12.5px}
[dir=rtl] .flag{border-radius:0;border-start-end-radius:8px;border-end-end-radius:8px}
/* relevance and exposure: word in the cell, colour from the shared set */
.rel,.exp{font-size:11.5px;font-weight:600;border-radius:var(--eh-r-chip);padding:2px 9px;white-space:nowrap}
.relH,.cellH{background:#2E7A37 !important;color:#fff !important}
.relM,.cellM{background:rgba(84,171,93,.32) !important;color:var(--eh-ink) !important}
.relL,.cellL{background:var(--eh-good-bg) !important;color:var(--eh-ink) !important}
.relN,.cellN{background:var(--eh-muted-bg) !important;color:var(--eh-muted) !important}
.cellxup{background:#0072BB !important;color:#fff !important}
.cellxheld{background:var(--eh-tint) !important}
.cellxdown{background:#B23F2B !important;color:#fff !important}
.cellxnew{background:var(--eh-warn-bg) !important;color:var(--eh-warn) !important}
.tiny{font-size:12px;color:var(--eh-ink-3)}.grey{color:var(--eh-ink-2)}
/* sector-shift diagram */
#shiftsvg text{font-family:var(--eh-font)}
.stitle{font-size:12.5px;fill:var(--eh-ink-2);font-weight:600}
.sbox{fill:var(--eh-tint);stroke:var(--eh-line)}
.sbar{fill:rgba(0,114,187,.26)}[data-theme=dark] .sbar{fill:rgba(78,176,238,.3)}
.slab{font-size:12px;fill:var(--eh-ink)}
.ebox{fill:var(--eh-paper);stroke:var(--eh-sea);stroke-width:1.25}.ebox5{stroke:var(--eh-leaf);stroke-width:2.5}
.elab{font-size:12.5px;font-weight:600;fill:var(--eh-ink)}
.etag{font-size:11px;fill:var(--eh-ink-3)}
.lnk{stroke:var(--eh-sea);stroke-opacity:.28}.lnk5{stroke:var(--eh-leaf);stroke-opacity:.8}
ol.to li{font-size:13.5px;border-bottom-color:var(--eh-line)}
/* tables */
table{font-size:13px}
th,td{border-bottom:1px solid var(--eh-line);padding:8px 10px}
th{background:var(--eh-tint);color:var(--eh-ink-2);font-weight:600;font-size:12.5px}
table:not(.heat) tr:hover td{background:var(--eh-tint)}
html:root[data-theme=dark] .c{color:var(--eh-ink-2)}
/* sources window */
.modal{background:rgba(13,23,54,.55)}
.mbox{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow)}
.mhead h2{font:600 19px/1.3 var(--eh-display)}
.mhead button{background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl);font:600 13px var(--eh-font)}
.mhead button:hover{background:var(--eh-info-bg)}
footer{color:var(--eh-ink-3);font-size:12px}
/* phone */
@media(max-width:600px){header{padding:12px 16px 14px}header img{height:34px;border-radius:9px}html:root header h1{font-size:17px}
  html.eh-embedded header,html.inframe header{padding-inline:16px}
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.kpi{padding:12px 13px}.kpi .v{font-size:19px}
  section{padding:16px 14px;border-radius:12px}section h2{font-size:18px}.eco{padding:13px}}
</style>'''

rep('strat', '<link rel="stylesheet" href="eh-shared.css">', SKIN, 'design', 'page skin straight after the shared design system')
rep('strat', '<header><img src="data:image/jpeg', '<header data-eh-contour="7"><img src="data:image/jpeg', 'design', 'standalone masthead contour lines')
rep('strat', '<section id="', '<section class="eh-panel" id="', 'motion', 'sections join the shared reveal-on-scroll (eh-panel)', count=10)

# charts: colours from the shared tokens (green = did it, red = fell short), brand font, axis text in the footnote ink
rep('strat', "red:THEME==='dark'?'#E0655A':'#C0392B',gold:THEME==='dark'?'#E0B865':'#C9A24A'",
    "red:g('--eh-c8'),gold:g('--eh-c5')", 'design', 'chart red and amber from the shared tokens')
rep('strat', "Chart.defaults.color=C.ink;Chart.defaults.borderColor=C.grid;Chart.defaults.font.family=getComputedStyle(document.body).fontFamily;",
    "Chart.defaults.color=getComputedStyle(document.documentElement).getPropertyValue('--eh-ink-2').trim()||C.ink;Chart.defaults.borderColor=C.grid;Chart.defaults.font.family=getComputedStyle(document.documentElement).getPropertyValue('--eh-font').trim()||getComputedStyle(document.body).fontFamily;",
    'design', 'chart text in the brand font and secondary ink')
rep('strat', "(THEME==='dark'?'rgba(160,175,185,.35)':'rgba(96,115,125,.25)')",
    "(THEME==='dark'?'rgba(157,171,197,.32)':'rgba(94,107,128,.22)')", 'design', 'grey "required pace" bar in the shared muted ink')
rep('strat', "cfg.options=o;charts[id]=new Chart(",
    "// EH design system v2 (patch_design_strat.py): axis text in the footnote ink, hairline grid; Arabic: horizontal bars start from the right\n"
    "  {const cs=getComputedStyle(document.documentElement),tk=cs.getPropertyValue('--eh-ink-3').trim(),ln=cs.getPropertyValue('--eh-line').trim(),rtl=LANG==='ar';\n"
    "   if(o.scales){for(const ax of Object.values(o.scales)){ax.ticks=Object.assign({color:tk},ax.ticks||{});ax.grid=Object.assign({color:ln},ax.grid||{});}\n"
    "     if(o.indexAxis==='y'){if(o.scales.x)o.scales.x.reverse=rtl;if(o.scales.y)o.scales.y.position=rtl?'right':'left';}}}\n"
    "  cfg.options=o;charts[id]=new Chart(",
    'rtl', 'axis colours; horizontal bar charts mirror in Arabic')
rep('strat', '<script src="eh-shared.js" defer></script>',
    "<script>\n"
    "/* EH design system v2 (patch_design_strat.py): chart text is painted on canvas, which cannot swap fonts by itself. When the brand\n"
    "   fonts finish loading (first visit, or the Arabic glyphs after a language switch) the charts re-measure and repaint. */\n"
    "(function(){ if(!document.fonts||!document.fonts.addEventListener)return; var tm=null;\n"
    "  function repaint(){ clearTimeout(tm); tm=setTimeout(function(){ Object.values(typeof charts!=='undefined'?charts:{}).forEach(function(c){ try{ Object.values(c.scales||{}).forEach(function(s){ s._longestTextCache={}; }); c.stop(); c.update('none'); }catch(e){} }); },60); }\n"
    "  document.fonts.addEventListener('loadingdone',repaint); document.fonts.ready.then(repaint); })();\n"
    "</script>\n<script src=\"eh-shared.js\" defer></script>",
    'design', 'repaint chart text once the brand fonts have loaded')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['strat'])
write_change_table(os.path.join(HERE, 'change_table_design_strat'), 'Design system v2 — PIF Strategy 2026–2030')
print('patched: hub/pif_strategy_2026_2030.html')
