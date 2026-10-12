"""patch_design_bub.py — EH design system v2 for the Client Portfolio Bubble Map
(hub/EH_Client_Bubble_Map_CURRENT.html), 12 Oct 2026.

The bubble map is a hand-maintained page (no generator in pipeline/ writes it; earlier patch scripts edit the
published HTML directly), so this script patches the HTML itself. It brings the page onto the shared tokens in
eh-shared.css v2 so it reads as one product with the hub shell and the Bid & Tender app:

  • standalone, the header becomes the navy masthead (contour lines, land-to-sea line along the bottom, KPI figures
    in Montserrat); inside the hub the title is already hidden by eh-shared.css and the KPI strip becomes a quiet
    row on the page colour
  • one quiet surface system: mist page, white panels with a hairline, 14px panel corners, 12px KPI tiles, no
    page-local greys; the bubble chart, heatmap and every Executive chart sit on a panel
  • the sector palette is re-mapped in its one constant (PALETTE) to a brand-led categorical set — each sector keeps
    its hue family (Power stays blue, Government green, Construction amber, Oil & Gas purple …), so nothing a reader
    has learned changes meaning
  • the heatmap ramp becomes a single sea-blue sequential scale (pale → EH blue) built with color-mix() from two CSS
    custom properties, so it re-themes with light/dark without redrawing; cell text switches to white only where the
    blue is dark enough to read
  • Executive charts take the brand status set (won/gain #2E7A37, lost/loss #B23F2B, 2026 #0072BB) and the brand
    inks; the dark-mode extension's hard-coded colours become tokens, and SVG text keeps its meaning colour in dark
  • labels in sentence case (no capitals), numbers with tabular figures, panels carry .eh-panel so eh-shared.js
    reveals them, and switching view (Bubble map / Heatmap / Executive) slides the new view in via EH_SHARED.viewIn
  • the detail panel slides with transform instead of animating `right`

No visible words, numbers, filters or features change. The page has no Arabic text of its own (ehBubbleLang is not
defined), so the Arabic view is the English page; the skin uses logical properties so it is ready for one.

Run once:  python3 pipeline/patch_design_bub.py   (restore with git checkout -- hub/EH_Client_Bubble_Map_CURRENT.html)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'EH_Client_Bubble_Map_CURRENT.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'bub')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Client Bubble Map skin (patch_design_bub.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* heatmap ramp ends: one sea-blue scale, re-themed here (renderHeat mixes between them) */
body{--bub-heat-lo:#E4EFF8;--bub-heat-hi:#0072BB}
body.dark{--bub-heat-lo:#1E3264;--bub-heat-hi:#0072BB}
/* masthead (standalone) */
header,body.dark header{background:var(--eh-deep);border-bottom:0;color:#fff;position:relative;isolation:isolate;padding:18px 22px 20px;gap:18px}
body.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan));pointer-events:none}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header h1,body.dark header h1{font:300 21px/1.25 var(--eh-display);color:#fff;letter-spacing:-.005em}
header h1 b,body.dark header h1 b{font-weight:700;color:#fff}
.kpis,body.dark .kpis{margin-left:0;margin-inline-start:auto;gap:26px;font-size:13px;color:rgba(255,255,255,.74)}
.kpis span,body.dark header .kpis span{color:rgba(255,255,255,.74)}
.kpis span b,body.dark header .kpis span b{font:600 21px/1.15 var(--eh-display);color:#fff;font-variant-numeric:tabular-nums lining-nums;letter-spacing:-.01em;margin-bottom:2px}
/* inside the hub the masthead belongs to the hub: the KPI strip sits quietly on the page colour */
html.inframe header,html.eh-embedded header,html.inframe body.dark header,html.eh-embedded body.dark header{background:transparent;color:var(--eh-ink);padding:14px 22px 2px}
html.inframe header::after,html.eh-embedded header::after,html.inframe header>.eh-contour,html.eh-embedded header>.eh-contour{display:none}
html.inframe .kpis span,html.eh-embedded .kpis span,html.inframe body.dark header .kpis span,html.eh-embedded body.dark header .kpis span{color:var(--eh-ink-2)}
html.inframe .kpis span b,html.eh-embedded .kpis span b,html.inframe body.dark header .kpis span b,html.eh-embedded body.dark header .kpis span b{color:var(--eh-ink)}
html.inframe header h1,html.inframe header h1 b{color:var(--eh-ink)}
/* toolbar: segmented view switch (ink), year scope (EH blue), search and reset */
.toolbar{padding:12px 22px;gap:10px}
.seg,body.dark .seg{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);box-shadow:none}
.seg button,body.dark .seg button{font:600 13px var(--eh-font);color:var(--eh-ink-2);background:transparent;border:0;padding:7px 15px}
.seg button:hover:not(.on){background:var(--eh-tint);color:var(--eh-ink)}
.btn,body.dark .btn{font:600 13px var(--eh-font);background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink);border-radius:var(--eh-r-ctl);padding:7px 14px}
.btn:hover,body.dark .btn:hover{border-color:var(--eh-sea);color:var(--eh-sea)}
#search,body.dark #search{background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink);border-radius:var(--eh-r-ctl);font:400 13.5px var(--eh-font)}
#search::placeholder{color:var(--eh-ink-3)}
#search:focus{outline:2px solid var(--eh-sea);outline-offset:1px;border-color:var(--eh-sea)}
.hint{font-size:12.5px}
/* bubble chart and legend share one panel */
#wrap{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);margin:2px 22px 0;overflow:hidden}
#chart svg text{font-family:var(--eh-font)}
circle.bub{stroke:var(--eh-paper)}
circle.bub:hover,circle.flash{stroke:var(--eh-ink)}
:root body.dark #chart text.lbl{fill:#fff}
:root body.dark #chart text.val{fill:rgba(255,255,255,.86)}
#legend{width:272px;padding:12px 16px 16px;border-inline-start:1px solid var(--eh-line);align-self:stretch}
#legend h3{font-size:14px;font-weight:600;color:var(--eh-ink);text-transform:none;letter-spacing:0;margin:4px 8px 8px}
.lg{font-size:13px;padding:6px 8px;border-radius:8px;color:var(--eh-ink)}
.lg:hover{background:var(--eh-tint)}
.lg .sw{width:12px;height:12px}
.lg .amt{margin-left:0;margin-inline-start:auto;padding-inline-start:8px;white-space:nowrap;color:var(--eh-ink-3);font-size:12px;font-variant-numeric:tabular-nums}
footer{padding:12px 22px 20px;font-size:12.5px;color:var(--eh-ink-3);line-height:1.55}
/* tooltip and zoom buttons */
#tip{background:rgba(13,23,54,.95);border-radius:10px;font-size:13px;box-shadow:0 10px 24px -12px rgba(0,0,0,.5)}
#tip .t{font-family:var(--eh-display);font-weight:600}
#tip .s{color:#A8E3AD}
/* detail panel: slides with transform (desktop), bottom sheet on phones is kept */
#panel,body.dark #panel{background:var(--eh-paper);color:var(--eh-ink);border-left:0;border-inline-start:1px solid var(--eh-line);box-shadow:-10px 0 30px -12px rgba(13,23,54,.35)}
@media(min-width:769px){
  #panel{right:0;inset-inline-end:0;transform:translateX(calc(100% + 32px));transition:transform var(--eh-dur-2) var(--eh-ease)}
  #panel.open{right:0;transform:none}
}
#panel .ph,body.dark #panel .ph{border-bottom:1px solid var(--eh-line);padding:18px 20px 14px}
#panel .ph .co,body.dark #pco{font:600 16px/1.4 var(--eh-display);color:var(--eh-ink);padding-inline-end:28px}
#panel .ph .sec,body.dark #psec{color:var(--eh-ink-2);font-size:12.5px}
#panel .ph .tot{color:var(--eh-ink-2);font-size:13px}
#panel .ph .tot b{color:var(--eh-ink);font-variant-numeric:tabular-nums}
#panel .px,body.dark #panel .px{right:auto;inset-inline-end:12px;color:var(--eh-ink-2);background:transparent;border:0}
#panel .px:hover{color:var(--eh-ink)}
.pline,body.dark .pline{border-bottom:1px solid var(--eh-line);font-size:13px;color:var(--eh-ink);padding:9px 20px}
.pline:hover,body.dark .pline:hover{background:var(--eh-tint)}
.pline .yr{font-size:11.5px;border-radius:6px;padding:1px 7px;font-variant-numeric:tabular-nums}
.pline .yr.y25{background:#5E6B80}
.pline .yr.y26{background:#0072BB}
.pline .sv small,body.dark .sv small{color:var(--eh-ink-3)}
.pline .amt,body.dark .amt{color:var(--eh-ink);font-variant-numeric:tabular-nums}
.pline .amt.na,body.dark .amt.na{color:var(--eh-ink-3)}
body.dark .sv .nm{color:var(--eh-ink)}
/* heatmap */
#heatWrap{padding:2px 22px 18px}
#heatTbl{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);padding:14px 16px;overflow-x:auto;max-width:100%}
#heatWrap th,body.dark #heatWrap th{font-size:12px;color:var(--eh-ink-2);font-weight:600;text-align:start}
#heatWrap th.col{height:150px}
#heatWrap th.row{padding-right:0;padding-inline-end:10px;color:var(--eh-ink)}
td.hc{border-radius:6px;font-size:12px;font-variant-numeric:tabular-nums;transition:none}
td.hc small{font-size:11px;opacity:.8}
td.hc:hover{outline:2px solid var(--eh-ink);outline-offset:-1px}
td.hc.empty,body.dark td.hc.empty{border:1.5px dashed color-mix(in srgb,var(--eh-ink-3) 45%,transparent);color:var(--eh-ink-3) !important;background:transparent}
.heatnote,body.dark .heatnote{font-size:13px;color:var(--eh-ink-2);padding:4px 0 10px}
.heatnote b{color:var(--eh-ink)}
/* Executive: KPI tiles, chart panels */
#execWrap{padding:6px 22px 28px}
.kband{gap:12px;margin-bottom:16px}
.kcard,body.dark .kcard{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.kcard .kv{font:600 26px/1.1 var(--eh-display);color:var(--eh-ink);font-variant-numeric:tabular-nums lining-nums;letter-spacing:-.01em}
.kcard .kl{font-size:13px;color:var(--eh-ink-2);font-weight:500;margin-top:6px;line-height:1.35}
.kcard .kd{font-size:12.5px;margin-top:4px;font-weight:600}
.kd.up{color:var(--eh-good)}.kd.dn{color:var(--eh-bad)}
.egrid{gap:16px}
.ecard,body.dark .ecard{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.ecard .eh2,body.dark .eh2{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);gap:6px;flex-wrap:wrap;margin-bottom:4px}
.ecard .esub,body.dark .esub{font-size:13px;color:var(--eh-ink-2);line-height:1.55;margin-bottom:10px}
.ecard .esub b{color:var(--eh-ink)}
.enote,body.dark .enote{font-size:12.5px;color:var(--eh-ink-3);margin-top:12px}
.ecard .eh2 .png,body.dark .png{font:600 12px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl);padding:5px 11px;margin-left:0}
.ecard .eh2 .png[data-svg]{margin-inline-start:auto}
.ecard .eh2 .png:hover{background:var(--eh-info-bg);border-color:var(--eh-sea);color:var(--eh-sea)}
#execWrap svg text{font-family:var(--eh-font)}
.ytog,body.dark .ytog{border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);background:var(--eh-paper)}
.ytog button,body.dark .ytog button{background:transparent;color:var(--eh-ink-2);font:600 12px var(--eh-font)}
.ytog button+button,body.dark .ytog button+button{border-inline-start-color:var(--eh-line)}
.ytog button.on,body.dark .ytog button.on{background:#0072BB;color:#fff}
.ytog button:hover:not(.on),body.dark .ytog button:hover:not(.on){background:var(--eh-tint);color:var(--eh-ink)}
#wsList table td,#wsList table th{font-size:13px}
#wsList th{font-weight:600;font-size:12.5px}
/* the colours the page writes inline, mapped to the shared tokens (one place for light and dark) */
:root body [style*="color:#1F7A4C"],:root body [style*="color:#2E7A37"]{color:var(--eh-good) !important}
:root body [style*="color:#B8860B"],:root body [style*="color:#C98A1B"]{color:var(--eh-warn) !important}
:root body [style*="color:#1A5FAB"],:root body [style*="color:#0072BB"]{color:var(--eh-info) !important}
:root body [style*="color:#8A99A3"],:root body [style*="color:#7D8AA0"]{color:var(--eh-ink-3) !important}
:root body [style*="color:#5F7078"]{color:var(--eh-ink-2) !important}
:root body [style*="background:#EAF2FA"]{background:var(--eh-info-bg) !important}
:root body [style*="background:#EFF6F1"]{background:var(--eh-good-bg) !important}
:root body [style*="border:1px solid #CCE0F0"],:root body [style*="border:1px solid #D5E6DA"]{border-color:transparent !important}
:root body [style*="border-top:1px solid #EEF2F5"]{border-top-color:var(--eh-line) !important}
/* quadrant headings in amber read in the darker warning ink */
.qquads text[fill="#C98A1B"]{fill:var(--eh-warn)}
/* Arabic-ready: labels sit at the start edge, figures stay left-to-right */
html[dir=rtl] .kcard{text-align:start}
html[dir=rtl] .kpis span b,html[dir=rtl] .lg .amt,html[dir=rtl] .pline .amt{direction:ltr;unicode-bidi:isolate}
@media(max-width:1024px){#wrap{margin-inline:14px}#heatWrap,#execWrap{padding-inline:14px}}
@media(max-width:768px){
  header,body.dark header{padding:12px 14px 14px}
  header h1,body.dark header h1{font-size:16px}
  .kpis,body.dark .kpis{margin-inline-start:0;gap:18px}
  .kpis span b,body.dark header .kpis span b{font-size:18px}
  html.inframe header,html.eh-embedded header{padding:10px 12px 0}
  #wrap{margin-inline:12px}
  #legend{width:100%;border-inline-start:0;border-top:1px solid var(--eh-line);padding:12px}
  #legend h3{flex:1 1 100%;margin:0 0 4px}
  .lg .amt{padding-inline-start:4px}
  #heatWrap,#execWrap{padding-inline:12px}
  .ecard{padding:14px}
  .kcard .kv{font-size:22px}
}
</style>
</head>'''

# ---------------- head: shared design system + skin right after it
rep('bub', '<link rel="stylesheet" href="eh-shared.css">\n</head>', SKIN, 'design', 'page skin right after the shared design system')

# ---------------- markup: masthead contours, panels revealed by eh-shared.js
rep('bub', '<body>\n<header>\n  <h1>', '<body>\n<header data-eh-contour="7">\n  <h1>', 'design', 'standalone masthead contour lines')
rep('bub', '<div class="ecard">', '<div class="ecard eh-panel">', 'motion', 'Executive chart panels revealed by eh-shared.js', count=6)
rep('bub', '<div class="ecard" style="grid-column:1/-1">', '<div class="ecard eh-panel" style="grid-column:1/-1">', 'motion', 'whitespace panel revealed by eh-shared.js')
rep('bub', '<div id="wrap">', '<div id="wrap" class="eh-panel">', 'motion', 'bubble chart panel revealed by eh-shared.js')

# ---------------- sector palette: one constant, brand-led, each sector keeps its hue family
rep('bub', '''const PALETTE = {
  "Power & Utilities":        "#027DC3",
  "Government & Municipal":   "#2BAE68",
  "Construction & Contracting":"#E8A33D",
  "Transport & Logistics":    "#1FA8A0",
  "Engineering & Consultancy":"#45B39D",
  "Oil & Gas / Petrochemicals":"#7D5BA6",
  "Trading & Services":       "#8FBF4D",
  "Manufacturing & Industrial":"#5D7793",
  "Steel & Metals":           "#8A9BA8",
  "Cement & Building Materials":"#C2A878",
  "Food & Agriculture":       "#D2B33A",
  "Healthcare & Pharma":      "#DE7C9A",
  "Other":                    "#AEB9BF",
  "Oils & Lubricants":        "#9C7A55"
};''', '''// EH design system v2: brand-led sector palette (land → sea). Each sector keeps its hue family from v1
// (blue, green, amber, teal, purple, lime, slate …) so the picture readers know is unchanged; white labels stay legible.
const PALETTE = {
  "Power & Utilities":        "#0072BB",
  "Government & Municipal":   "#54AB5D",
  "Construction & Contracting":"#C98A1B",
  "Transport & Logistics":    "#00A0E0",
  "Engineering & Consultancy":"#2E9C8F",
  "Oil & Gas / Petrochemicals":"#8E6BB8",
  "Trading & Services":       "#8DB83A",
  "Manufacturing & Industrial":"#3B57B8",
  "Steel & Metals":           "#7D8AA0",
  "Cement & Building Materials":"#B89A6B",
  "Food & Agriculture":       "#D0A72C",
  "Healthcare & Pharma":      "#C9708E",
  "Other":                    "#A7B1C2",
  "Oils & Lubricants":        "#94704C"
};''', 'design', 'brand-led sector palette in its one constant (hue families kept)')

# ---------------- heatmap: single sea-blue sequential ramp, re-themed by CSS custom properties
rep('bub', '''  const cellBg = v => {
    if (v <= 0) return null;
    const t = Math.sqrt(v/vmax);                       // sqrt scale
    const light = 96 - t*58;                           // 96% -> 38%
    return `hsl(203 ${Math.round(30+t*68)}% ${Math.round(light)}%)`;
  };
  const cellFg = v => Math.sqrt(v/vmax) > .42 ? "#fff" : "#16333F";''',
'''  // EH design system v2: one sea-blue sequential ramp (pale → EH blue), √ scale; the two ends are CSS custom
  // properties (--bub-heat-lo / --bub-heat-hi, set in the skin) so light and dark themes need no redraw
  const cellBg = v => {
    if (v <= 0) return null;
    const t = Math.sqrt(v/vmax);                       // sqrt scale
    return `color-mix(in srgb, var(--bub-heat-hi) ${Math.round(8+t*92)}%, var(--bub-heat-lo))`;
  };
  const cellFg = v => Math.sqrt(v/vmax) > .7 ? "#fff" : "var(--eh-ink)";''', 'design', 'heatmap: single-hue sea-blue ramp readable in both themes')

# ---------------- Executive charts: brand fonts, inks and status colours
rep('bub', 'svg.attr("font-family","Segoe UI, Tahoma, Arial, sans-serif");',
    'svg.attr("font-family","\'EH Sans\',\'Encode Sans\',\'Segoe UI\',Tahoma,Arial,sans-serif");', 'design', 'chart text in the brand font')
rep('bub', 'cl.setAttribute("font-family", "\'Segoe UI\', system-ui, Arial, sans-serif");',
    'cl.setAttribute("font-family", "\'EH Sans\',\'Encode Sans\',\'Segoe UI\', system-ui, Arial, sans-serif");', 'design', 'PNG export asks for the brand font first')
rep('bub', '''    {l:"2025", v:t25, abs:true, c:"#5D7793"},
    {l:"New clients", v:vNew, c:"#2BAE68", items: neu, key:d=>d.v2026},
    {l:"Expansion", v:vExp, c:"#57C785", items: ret.filter(d=>d.v2026>d.v2025), key:d=>d.v2026-d.v2025},
    {l:"Contraction", v:vCon, c:"#E0A48A", items: ret.filter(d=>d.v2025>d.v2026), key:d=>d.v2026-d.v2025},
    {l:"Churn", v:vChn, c:"#C0563F", items: los, key:d=>-d.v2025},
    {l:"2026", v:t26, abs:true, c:"#027DC3"},''',
'''    {l:"2025", v:t25, abs:true, c:"#5E9FD6"},
    {l:"New clients", v:vNew, c:"#54AB5D", items: neu, key:d=>d.v2026},
    {l:"Expansion", v:vExp, c:"#7FB685", items: ret.filter(d=>d.v2026>d.v2025), key:d=>d.v2026-d.v2025},
    {l:"Contraction", v:vCon, c:"#D9917F", items: ret.filter(d=>d.v2025>d.v2026), key:d=>d.v2026-d.v2025},
    {l:"Churn", v:vChn, c:"#B23F2B", items: los, key:d=>-d.v2025},
    {l:"2026", v:t26, abs:true, c:"#0072BB"},''', 'design', 'revenue bridge in the brand status set')
rep('bub', '''    {l:"Retained", n:ret.length, v:d3.sum(ret,d=>d.v2026), c:"#2BAE68",''',
    '''    {l:"Retained", n:ret.length, v:d3.sum(ret,d=>d.v2026), c:"#54AB5D",''', 'design', 'retention: kept clients in leaf green')
rep('bub', '''    {l:"New in 2026", n:neu.length, v:d3.sum(neu,d=>d.v2026), c:"#027DC3",''',
    '''    {l:"New in 2026", n:neu.length, v:d3.sum(neu,d=>d.v2026), c:"#0072BB",''', 'design', 'retention: new clients in EH blue')
rep('bub', '''    {l:"Lost after 2025", n:los.length, v:d3.sum(los,d=>d.v2025), c:"#C0563F",''',
    '''    {l:"Lost after 2025", n:los.length, v:d3.sum(los,d=>d.v2025), c:"#B23F2B",''', 'design', 'retention: lost clients in brick')
rep('bub', 'up ? "#2BAE68" : "#C0563F"', 'up ? "#2E7A37" : "#B23F2B"', 'design', 'sector shift gains/losses in the brand status colours', count=2)
rep('bub', '"#8A9BA8"', '"#7D8AA0"', 'design', 'sector shift 2025 hollow dots in the brand slate', count=2)
rep('bub', '.attr("r",5.5).attr("fill","#027DC3");', '.attr("r",5.5).attr("fill","#0072BB");', 'design', 'sector shift legend dot in EH blue')
rep('bub', '"#16333F"', '"#15224D"', 'design', 'chart ink: brand navy text', count=6)
rep('bub', '"#6B7F88"', '"#5E6B80"', 'design', 'chart axes and secondary labels in ink-3', count=8)
rep('bub', '"#4A5E67"', '"#46546F"', 'design', 'chart tertiary labels in ink-2', count=2)
rep('bub', '"#E8EFED"', '"#D9E3DF"', 'design', 'gridlines in the hairline colour')
rep('bub', '"#B9C6C3"', '"#B8C4D0"', 'design', 'bridge connector lines')
rep('bub', '''  const HALO=DKQ?"#151C21":"#fff", TXT=DKQ?"#D5E0E6":"#37474F", MED=DKQ?"#4A5A64":"#B9C6CE", MEDT=DKQ?"#8FA3AE":"#8A99A3";''',
    '''  const HALO=DKQ?"#15214A":"#fff", TXT=DKQ?"#E9EEF7":"#15224D", MED=DKQ?"#4A5C8C":"#B8C4D0", MEDT=DKQ?"#9DABC5":"#5E6B80";   // EH tokens''',
    'design', 'depth vs value: halo, labels and median guides from the tokens')
rep('bub', '''  const QCOL=DKQ?{S:"#5FC98E",C:"#E3C36B",T:"#7FB4E8",X:"#93A4AF"}:{S:"#1F7A4C",C:"#B8860B",T:"#1A5FAB",X:"#8A99A3"};''',
    '''  const QCOL=DKQ?{S:"#7CCB82",C:"#E8B04A",T:"#4EB0EE",X:"#9DABC5"}:{S:"#2E7A37",C:"#C98A1B",T:"#0072BB",X:"#7D8AA0"};   // EH status set''',
    'design', 'depth vs value: quadrant colours from the brand status set')
rep('bub', '''  const AXL=DKQ?"#5A6B76":"#C3CED5", AXT=DKQ?"#9FB3BE":"#6B7C86";''',
    '''  const AXL=DKQ?"#3A4A78":"#C9D3DE", AXT=DKQ?"#9DABC5":"#5E6B80";''', 'design', 'depth vs value: axes in ink-3 / hairline')
rep('bub', '''  const BAR=DK?"#4FB0E8":"#027DC3", TXT=DK?"#E6EEF2":"#1C2B33", SUB=DK?"#9FB3BE":"#5F7078", AX=DK?"#9FB3BE":"#6B7C86", AXL=DK?"#5A6B76":"#C3CED5";''',
    '''  const BAR=DK?"#4EB0EE":"#0072BB", TXT=DK?"#E9EEF7":"#15224D", SUB=DK?"#B8C4DA":"#46546F", AX=DK?"#9DABC5":"#5E6B80", AXL=DK?"#3A4A78":"#C9D3DE";   // EH tokens''',
    'design', 'deal-size bars and text from the tokens')

# ---------------- view switch: the incoming view slides in from the reading-start edge
rep('bub', '''  closePanel();
  if (v === "heat") renderHeat(); else if (v === "exec") renderExec(); else render();
}''', '''  closePanel();
  if (v === "heat") renderHeat(); else if (v === "exec") renderExec(); else render();
  if (window.EH_SHARED && EH_SHARED.viewIn) EH_SHARED.viewIn(document.getElementById(v === "heat" ? "heatWrap" : v === "exec" ? "execWrap" : "wrap"));
}''', 'motion', 'view change slides in via EH_SHARED.viewIn')

# ---------------- dark-mode extension: hard-coded colours become tokens
rep('bub', '''body.dark{background:#0F1519;color:#E6EDF1}
body.dark header,body.dark .hdr,body.dark .topbar{background:#121A1F !important;border-color:#2C3A43 !important;color:#E6EDF1}
body.dark header *{color:#C9D4DB}
body.dark .ecard,body.dark .kcard{background:#151C21;border-color:#2C3A43;color:#E6EDF1}
body.dark .eh2{color:#E6EDF1}
body.dark .esub,body.dark .enote,body.dark .heatnote{color:#9FB3BE}
body.dark svg text{fill:#C9D4DB}
body.dark svg .domain,body.dark svg g.tick line{stroke:#3A4B55}
body.dark table th{color:#CBD8DF}
body.dark table td,body.dark table tr{border-color:#2C3A43 !important}
body.dark input,body.dark select,body.dark button:not(.png){background:#1A242B;border-color:#3A4B55;color:#E6EDF1}
body.dark .png{background:#1E2830;border-color:#3A4B55;color:#CFE3F2}
body.dark .seg button.on{background:var(--eh-blue) !important;color:#fff !important}
body.dark .vw.on{background:var(--eh-green,#2BAE68) !important;color:#fff !important}
body.dark .seg{background:#151C21}
body.dark .hc{text-shadow:0 1px 2px rgba(0,0,0,.6)}
body.dark .hc:not([style*="background"]){color:#8FA3AE !important}
body.dark [style*="color:#1A5FAB"]{color:#7FB4E8 !important}

/* a11y audit fixes */

.vw,.seg button{min-height:44px}
.png{min-height:36px}
.vw.on{background:#1F7A4C !important;border-color:#1F7A4C !important}
.seg button.on{background:#0E5A9E !important}
body.dark .vw.on{background:#1F7A4C !important;border-color:#1F7A4C !important}
body.dark .seg button.on{background:#0E5A9E !important}
.hint{color:#5A6A74}
body.dark .hint{color:#AFC3CE !important}
header small, .esub{color:#44525C}''',
'''/* dark mode: colours come from the eh-shared.css tokens (patch_design_bub.py) */
body.dark{background:var(--eh-mist);color:var(--eh-ink)}
body.dark header,body.dark .hdr,body.dark .topbar{border-color:var(--eh-line) !important}
body.dark .ecard,body.dark .kcard{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink)}
body.dark .eh2{color:var(--eh-ink)}
body.dark .esub,body.dark .enote,body.dark .heatnote{color:var(--eh-ink-2)}
/* SVG text keeps the meaning of the colour the chart gave it */
body.dark #execWrap svg text:not([fill]),body.dark #heatWrap svg text{fill:var(--eh-ink-2)}
body.dark #execWrap svg text[fill="#15224D"]{fill:var(--eh-ink)}
body.dark #execWrap svg text[fill="#46546F"]{fill:var(--eh-ink-2)}
body.dark #execWrap svg text[fill="#5E6B80"],body.dark #execWrap svg text[fill="currentColor"]{fill:var(--eh-ink-3)}
body.dark #execWrap svg text[fill="#2E7A37"]{fill:var(--eh-good)}
body.dark #execWrap svg text[fill="#B23F2B"]{fill:var(--eh-bad)}
body.dark #execWrap svg g[color="#5E6B80"]{color:var(--eh-ink-3)}
body.dark #execWrap svg line[stroke="#2E7A37"]{stroke:var(--eh-good)}
body.dark #execWrap svg line[stroke="#B23F2B"]{stroke:var(--eh-bad)}
body.dark #svgPareto path[stroke="#15224D"]{stroke:var(--eh-ink)}
body.dark #svgPareto circle[fill="#15224D"]{fill:var(--eh-ink)}
body.dark #svgSlope circle[fill="#fff"]{fill:var(--eh-paper)}
body.dark #execWrap svg line[stroke="#B8C4D0"]{stroke:#4A5C8C}
body.dark svg .domain,body.dark svg g.tick line{stroke:var(--eh-line)}
body.dark table th{color:var(--eh-ink-2)}
body.dark table td,body.dark table tr{border-color:var(--eh-line) !important}
body.dark input,body.dark select{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink)}
body.dark .seg{background:var(--eh-paper)}
body.dark .hc:not([style*="background"]){color:var(--eh-ink-3) !important}

/* a11y audit fixes */

.vw,.seg button{min-height:44px}
.png{min-height:36px}
/* active view = ink, active year = EH blue (white text passes AA on both, in either theme) */
#viewSeg button.on{background:var(--eh-ink) !important;border-color:var(--eh-ink) !important;color:var(--eh-paper) !important}
#yearSeg button.on{background:#0072BB !important;border-color:#0072BB !important;color:#fff !important}
.hint,body.dark .hint{color:var(--eh-ink-2)}
header small, .esub{color:var(--eh-ink-2)}''', 'design', 'dark-mode extension: hard-coded colours replaced by tokens')
rep('bub', '''  .ecard::after{content:"⟷ swipe chart";position:absolute;right:10px;bottom:8px;font-size:10px;font-weight:700;color:#fff;background:#1F7A4C;padding:2px 7px;border-radius:9px;opacity:.9;pointer-events:none}''',
    '''  .ecard::after{content:"⟷ swipe chart";position:absolute;inset-inline-end:10px;bottom:8px;font-size:11px;font-weight:600;color:#fff;background:#0072BB;padding:2px 8px;border-radius:999px;opacity:.92;pointer-events:none}''',
    'design', 'swipe hint chip in EH blue, logical position')
rep('bub', '''.zctl button{width:44px;height:44px;border-radius:12px;border:1px solid var(--line);background:rgba(255,255,255,.94);color:#1F2A37;font:700 20px/1 Arial,sans-serif;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.12);touch-action:manipulation}''',
    '''.zctl button{width:44px;height:44px;border-radius:var(--eh-r-ctl);border:1px solid var(--eh-line);background:var(--eh-paper);color:var(--eh-ink);font:500 20px/1 var(--eh-font);cursor:pointer;box-shadow:var(--eh-shadow);touch-action:manipulation}
.zctl button:hover{border-color:var(--eh-sea);color:var(--eh-sea)}''', 'design', 'zoom buttons on the token surfaces')
rep('bub', '''body.dark .zctl button{background:rgba(24,33,38,.94);color:#E6EDF1;border-color:#3A4B55}
body.dark #panel{background:#151C21;border-color:#2C3A43;color:#E6EDF1;box-shadow:-8px 0 24px rgba(0,0,0,.45)}
body.dark .ph{border-color:#2C3A43} body.dark #pco{color:#E6EDF1}
body.dark .pline{border-color:#2C3A43;color:#E6EDF1} body.dark .pline:hover{background:#1E2830}
body.dark .sv .nm{color:#E6EDF1} body.dark .sv small,body.dark #psec,body.dark .amt.na{color:#9FB3BE}
body.dark .amt{color:#E6EDF1}''',
'''body.dark #panel{box-shadow:-10px 0 30px -10px rgba(0,0,0,.6)}''', 'design', 'dark panel colours now come from the tokens in the skin')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['bub'])
write_change_table(os.path.join(HERE, 'change_table_design_bub'), 'Design system v2 — Client Bubble Map')
print('patched: hub/EH_Client_Bubble_Map_CURRENT.html')
