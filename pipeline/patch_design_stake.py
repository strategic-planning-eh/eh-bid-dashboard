"""patch_design_stake.py — EH design system v2 for the Stakeholder & Competitive Map (hub/EH_Stakeholder_Map_CURRENT.html), 12 Oct 2026.

The map keeps everything it shows (the radial stakeholder wheel, the Leaflet Saudi map, the licence and regional
views, the list) and takes the shared look from eh-shared.css v2 so it reads as one product with the hub shell and the
Bid & Tender app:
  • standalone, its header becomes the deep-navy masthead with contour lines, the logo on a white tile and the
    land-to-sea line along the bottom; inside the hub the header shrinks to a quiet toolbar on the page colour, so the
    four action buttons sit on mist, not navy
  • KPI tiles, side filters, company detail and every view use the quiet surface system: white panels with a hairline,
    numbers in Montserrat with tabular figures, labels in sentence case (no capitals anywhere — the KPI labels, panel
    headings, table heads and the wheel's ring and region labels were all set in capitals before)
  • tabs become a single underline bar; switching a view slides it in from the reading-start edge (eh-shared.js)
  • the radial map and the Leaflet layers keep their data colours (categories, tiers, bid rings); only their chrome
    changes — the wheel's guides, ring pills, labels and the EH centre now use brand tokens and the brand fonts, and
    read properly in dark mode
  • the page's hard-coded dark theme and the inline colours its scripts write are mapped onto the shared tokens, so
    light and dark both come from eh-shared.css
  • physical left/right in the page CSS that broke Arabic (header actions, counts, table heads, detail values, list
    dots, watch items, popup values, modal close) replaced with logical properties

Data safety: pipeline/sync_bids_to_apps.py and refresh_map_banalytics.py rewrite the
<script id="DATA|LIC|BANALYTICS" type="application/json"> blocks on every publish. Nothing here touches those blocks
or their opening/closing tags; every edit is an exact-string replacement in the CSS, the markup above the data blocks,
or the page script below them, and the script stops if any anchor is missing.

Run once:  python3 pipeline/patch_design_stake.py
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'stake')

def blocks(s):
    return re.findall(r'<script id="(?:DATA|LIC|BANALYTICS)" type="application/json">.*?</script>', s, re.S)
BEFORE = blocks(FILES['stake'])

SKIN = r'''<link rel="stylesheet" href="eh-shared.css"><style id="eh-skin">
/* EH design system v2 — Stakeholder Map skin (patch_design_stake.py). Tokens and fonts come from eh-shared.css. */
:root,html.dark{--paper:var(--eh-paper);--mist:var(--eh-mist);--ink:var(--eh-ink);--ink-soft:var(--eh-ink-2);--line:var(--eh-line);--eh-blue-d:var(--eh-deep)}
body,html.dark body{background:var(--eh-mist);color:var(--eh-ink);font-size:14px;line-height:var(--eh-lh)}
/* masthead (standalone) */
header,html.dark header{background:var(--eh-deep);border-bottom:0;color:#fff;position:relative;isolation:isolate;padding:16px 22px 19px}
html.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan));pointer-events:none}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header .logo img{box-sizing:content-box;background:#fff;border-radius:11px;padding:3px 6px;box-shadow:0 2px 10px -4px rgba(0,0,0,.4)}
.titles h1{font:600 19px/1.25 var(--eh-display);color:#fff;letter-spacing:-.005em}
.titles p{font-size:12.5px;color:rgba(255,255,255,.72);margin-top:3px}
.hd-actions{margin-left:0;margin-inline-start:auto;flex-wrap:wrap}
.btn,html.dark .btn{font:600 13px var(--eh-font);border-radius:var(--eh-r-ctl);padding:7px 14px;background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink)}
.btn:hover,html.dark .btn:hover{background:var(--eh-tint);border-color:var(--eh-sea);color:var(--eh-sea)}
header .btn,html.dark header .btn{background:transparent;border:1px solid rgba(255,255,255,.28);color:#fff}
header .btn:hover,html.dark header .btn:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.5);color:#fff}
html body header .eh-syncstamp{font-size:12px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);color:rgba(255,255,255,.82);border-radius:var(--eh-r-chip)}
html body header .eh-syncstamp b{color:#A8E3AD}
/* inside the hub the masthead belongs to the hub: this header is a quiet toolbar on the page colour */
html.eh-embedded header,html.inframe header,html.eh-embedded.dark header,html.inframe.dark header{background:transparent;color:var(--eh-ink)}
html.eh-embedded.eh-page-stake header,html.inframe.eh-page-stake header,html.eh-embedded.eh-page-stake.dark header{padding:12px 22px 2px !important}
html.eh-embedded header::after,html.inframe header::after,html.eh-embedded header>.eh-contour,html.inframe header>.eh-contour{display:none}
html.eh-embedded .hd-actions,html.inframe .hd-actions{margin-inline-start:0}
html.eh-embedded header .btn,html.inframe header .btn,html.eh-embedded.dark header .btn,html.inframe.dark header .btn{background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink)}
html.eh-embedded header .btn:hover,html.inframe header .btn:hover,html.eh-embedded.dark header .btn:hover,html.inframe.dark header .btn:hover{background:var(--eh-tint);border-color:var(--eh-sea);color:var(--eh-sea)}
html.eh-embedded body header .eh-syncstamp,html.inframe body header .eh-syncstamp{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink-2)}
html.eh-embedded body header .eh-syncstamp b,html.inframe body header .eh-syncstamp b{color:var(--eh-leaf-ink)}
/* KPI tiles: no coloured edges, numbers lead, labels in sentence case */
.kpis{gap:12px;padding:14px 22px}
.kpi,html.dark .kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:14px 16px 13px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.kpi .v{font:600 26px/1.1 var(--eh-display);color:var(--eh-ink)}
.kpi.accent .v{color:var(--eh-leaf-ink)}.kpi.gold .v{color:var(--eh-warn)}.kpi.red .v{color:var(--eh-bad)}.kpi.blue .v{color:var(--eh-sea)}
.kpi .l{font-size:13px;color:var(--eh-ink-2);text-transform:none;letter-spacing:0;font-weight:500;margin-top:6px;line-height:1.35}
/* panels */
.wrap{gap:14px}
.panel,html.dark .panel{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.panel h3{font:600 14px/1.35 var(--eh-display);color:var(--eh-ink);text-transform:none;letter-spacing:0;padding:14px 16px 7px}
.side section{padding:4px 16px 12px;border-bottom:1px solid var(--eh-line)}
.note{font-size:12px;color:var(--eh-ink-3)}
input[type=text],select,html.dark input,html.dark select,html.dark #search{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);color:var(--eh-ink)}
input[type=text]:focus,select:focus{outline:2px solid var(--eh-sea);outline-offset:0;border-color:transparent}
html.dark #search::placeholder,#search::placeholder{color:var(--eh-ink-3)}
.catrow,html.dark .catrow{font-size:13px;color:var(--eh-ink)}
.catrow input,input[type=range],#leafSide input{accent-color:var(--eh-sea)}
.catrow .cnt{margin-left:0;margin-inline-start:auto;color:var(--eh-ink-3);font-size:12px}
html.dark label{color:var(--eh-ink)}
.chip,html.dark .chip{border:1px solid var(--eh-line);border-radius:var(--eh-r-chip);padding:5px 12px;font-size:12.5px;background:var(--eh-paper);color:var(--eh-ink-2);font-weight:500}
.chip:hover,html.dark .chip:hover{background:var(--eh-tint);color:var(--eh-ink)}
.chip.on,html.dark .chip.on{background:var(--eh-sea);border-color:var(--eh-sea);color:var(--eh-paper);font-weight:600}
.range-l{font-size:12px;color:var(--eh-ink-3)}
.matches,html.dark .matches{background:transparent}
.match,html.dark .match{color:var(--eh-ink)}
.match:hover,html.dark .match:hover{background:var(--eh-tint)}
.mfilt{border-color:var(--eh-line) !important;background:var(--eh-paper) !important;color:var(--eh-ink) !important;font-weight:600 !important;border-radius:12px}
.mfilt .mfcnt{background:var(--eh-leaf-ink) !important;color:var(--eh-paper) !important}
/* view tabs: one underline bar */
.tabs,.panel.center .tabs,html.dark .tabs{background:transparent;gap:2px;padding:4px 12px 0;border-bottom:1px solid var(--eh-line)}
.tab,html.dark .tab{font:600 13.5px var(--eh-font);color:var(--eh-ink-2);border:0;border-radius:0;background:none;padding:12px 14px;box-shadow:inset 0 -3px 0 transparent;display:flex;align-items:center;transition:color var(--eh-dur-1) var(--eh-ease),box-shadow var(--eh-dur-2) var(--eh-ease)}
.tab:hover,html.dark .tab:hover{color:var(--eh-ink)}
.tab.on,html.dark .tab.on{background:none;color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}
#mapView,#regView,html.dark #mapView,html.dark #regView{background:transparent;border-radius:0}
#listView,#bidView,#geoView,#licView,html.dark #listView,html.dark #geoView,html.dark #licView,html.dark #bidView{background:var(--eh-paper)}
/* radial map chrome */
.tooltip{background:var(--eh-deep);color:#fff;border-radius:9px;box-shadow:0 8px 22px -10px rgba(13,23,54,.55);font-size:12.5px}
html.dark .tooltip{border:1px solid rgba(255,255,255,.14)}
.zbtn,html.dark .zbtn{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);color:var(--eh-ink);box-shadow:var(--eh-shadow)}
.zbtn:hover,html.dark .zbtn:hover{border-color:var(--eh-sea);color:var(--eh-sea)}
.zoomhint,html.dark .zoomhint{font-size:12px;color:var(--eh-ink-2) !important;background:color-mix(in srgb,var(--eh-paper) 88%,transparent) !important;border-radius:var(--eh-r-chip)}
#emptyHint>div,html.dark #emptyHint>div{background:var(--eh-paper) !important;border:1px solid var(--eh-line) !important;color:var(--eh-ink-2) !important;border-radius:var(--eh-r-panel) !important;box-shadow:var(--eh-shadow) !important}
.legend,html.dark .legend{background:var(--eh-paper);border-top:1px solid var(--eh-line);color:var(--eh-ink-2);font-size:12.5px;gap:8px 16px;padding:11px 16px}
.legend b,html.dark .legend b{color:var(--eh-ink) !important}
.legend [style*="color:#C9A227"],.legend [style*="color:#B8860B"],html.dark .legend [style*="color:#C9A227"],html.dark .legend [style*="color:#B8860B"]{color:var(--eh-warn) !important}
/* company detail */
.detail .empty{color:var(--eh-ink-2);font-size:13px}
.dname{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);padding:4px 16px 2px}
.dbadges{padding:8px 16px 12px}
.bdg{font-size:11.5px;font-weight:600;border-radius:var(--eh-r-chip);padding:3px 10px}
.drow{border-top:1px solid var(--eh-line);font-size:13px;padding:7px 16px}
.drow .k{color:var(--eh-ink-2)}
.drow .v,html[dir=rtl] .drow .v{text-align:end;color:var(--eh-ink)}
.mwblk,html.dark .mwblk{background:var(--eh-tint);border:1px solid var(--eh-line);border-radius:10px}
.mwhdr,.mwblk .mwhdr,html.dark .mwblk .mwhdr,html.dark .mwhdr{color:var(--eh-leaf-ink) !important;text-transform:none;letter-spacing:0;font-size:12.5px}
html.dark .mwblk .k{color:var(--eh-ink-2)}html.dark .mwblk .v{color:var(--eh-ink)}
.lchip,html.dark .lchip{font-size:12px;font-weight:600;background:var(--eh-tint);border:1px solid var(--eh-line);border-radius:6px;color:var(--eh-ink);font-variant-numeric:tabular-nums}
.leaflet-popup-content .lchip,#leafSide .lchip,html.dark .leaflet-popup-content .lchip,html.dark #leafSide .lchip{color:#fff;border:0;border-radius:var(--eh-r-chip);font-size:11.5px;margin-right:0;margin-inline-end:4px}
#detail div[style*="font-size:11px"],#detail div[style*="font-size:11.5px"]{font-size:12.5px !important}
/* regional view */
.heatwrap{padding:16px 18px;margin-bottom:14px}
.heatwrap h4{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);margin-bottom:12px}
.bars .bl{text-align:end;color:var(--eh-ink-2);font-size:12.5px}
.bars .bt{background:var(--eh-leaf);border-radius:3px}
.bars .bv{font-size:12.5px;font-weight:600;color:var(--eh-ink)}
table.heat th{color:var(--eh-ink-2);text-align:start;font-size:12px}
table.heat td{font-size:12px}
/* list view */
.ltbl{font-size:13px}
.ltbl thead th,html.dark .ltbl th,html.dark #listView th{background:var(--eh-tint);color:var(--eh-ink-2);font-size:12.5px;text-transform:none;letter-spacing:0;font-weight:600;border-bottom:1px solid var(--eh-line);text-align:start}
.ltbl thead th:hover{color:var(--eh-sea)}
.ltbl tbody td,html.dark #listView td{border-bottom:1px solid var(--eh-line)}
.ltbl tbody tr:hover td,html.dark #listView tr:hover td{background:var(--eh-tint)}
.ltbl tbody tr:hover{background:none}
.ltbl .tdot{margin-right:0;margin-inline-end:7px}
.lcount,html.dark .lcount{background:var(--eh-paper) !important;color:var(--eh-ink-2) !important;border-color:var(--eh-line) !important;font-size:12.5px}
.lcount b,html.dark .lcount b{color:var(--eh-ink)}
/* bid, licence and Saudi map views */
.biz-sec{font:600 17px/1.35 var(--eh-display);color:var(--eh-ink);border:0;padding:0;margin:22px 0 10px}
.biz-kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;box-shadow:var(--eh-shadow);padding:13px 15px}
.biz-kpi .v{font-family:var(--eh-display) !important;font-weight:600;color:var(--eh-ink)}
.biz-kpi .l{font-size:12.5px;color:var(--eh-ink-2);text-transform:none;letter-spacing:0;margin-top:5px}
.btab{font-size:13px}
.btab th{background:var(--eh-tint);color:var(--eh-ink-2);font-size:12.5px;text-transform:none;letter-spacing:0;font-weight:600;border-bottom:1px solid var(--eh-line);text-align:start}
.btab td{border-bottom:1px solid var(--eh-line)}
.btab tr:hover{background:var(--eh-tint)}
.geo-legend{font-size:12px;color:var(--eh-ink-3);line-height:1.55}
.yoy-card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px}
.yoy-yr{font:600 18px var(--eh-display);color:var(--eh-leaf-ink)}
.wl-item{background:var(--eh-paper);border:1px solid var(--eh-line);border-inline-start-width:3px;border-radius:10px;color:var(--eh-ink);font-size:13px}
.wl-high,html.dark .wl-high{background:var(--eh-paper);border-left-color:var(--eh-line);border-inline-start-color:var(--eh-bad)}
.wl-med,html.dark .wl-med{background:var(--eh-paper);border-left-color:var(--eh-line);border-inline-start-color:var(--eh-warn)}
.wl-low,html.dark .wl-low{background:var(--eh-paper);border-left-color:var(--eh-line);border-inline-start-color:var(--eh-leaf)}
.wl-k,html.dark .wl-k{text-transform:none;letter-spacing:0;font-size:11.5px;border-radius:var(--eh-r-chip);color:#fff}
.sat-row{font-size:12.5px}
.sat-lbl,html.dark .sat-lbl{font:600 12px var(--eh-font);color:var(--eh-sea-ink) !important;font-variant-numeric:tabular-nums}
.sat-bar[style*="#2E7D46"]{background:#2E7A37 !important}.sat-bar[style*="#1A6FB0"]{background:#0072BB !important}.sat-bar[style*="#E8862E"]{background:#C98A1B !important}.sat-bar[style*="#B23A3A"]{background:#B23F2B !important}
#geoSvg{font-family:var(--eh-font)}
#leafBanner,html.dark #leafBanner{background:var(--eh-warn-bg);border:1px solid transparent;color:var(--eh-ink-2);font-size:12.5px;border-radius:var(--eh-r-ctl);padding:8px 12px}
.leafbtn,html.dark .leafbtn{font:600 12.5px var(--eh-font);background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl)}
.leafbtn:hover,html.dark .leafbtn:hover{background:var(--eh-info-bg);border-color:var(--eh-sea)}
.gmode,html.dark .gmode{background:var(--eh-tint);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl)}
.gmode button,html.dark .gmode button{font:600 12.5px var(--eh-font);color:var(--eh-ink-2)}
.gmode button.on,html.dark .gmode button.on{background:var(--eh-sea);color:var(--eh-paper)}
#leafSide,html.dark #leafSide{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;color:var(--eh-ink-2);font-size:12.5px}
#leafSide h4{font:600 12.5px var(--eh-font);color:var(--eh-ink);text-transform:none;letter-spacing:0}
#leafSide div[style*="font-size:10.5px"],.leaflet-popup-content [style*="font-size:10.5px"],.leaflet-popup-content [style*="font-size:9.5px"]{font-size:12px !important}
#leafMap,html.dark #leafMap{border:1px solid var(--eh-line);border-radius:12px;isolation:isolate}   /* Leaflet's panes stay under the page's modals */
#leafCount{color:var(--eh-sea)}
#leafModal{background:rgba(13,23,54,.5)}
#leafModal .box,html.dark #leafModal .box{background:var(--eh-paper);color:var(--eh-ink);border-radius:var(--eh-r-panel)}
html .leaflet-container{font-family:var(--eh-font)}
html .leaflet-popup-content-wrapper,html .leaflet-popup-tip{background:var(--eh-paper);color:var(--eh-ink);box-shadow:0 8px 24px -10px rgba(13,23,54,.45)}
html .leaflet-popup-content-wrapper{border-radius:12px}
html .leaflet-popup-content{font-family:var(--eh-font);font-size:12.5px}
.leaflet-popup-content .prow{border-top:1px solid var(--eh-line)}
.leaflet-popup-content .prow .k{color:var(--eh-ink-2)}
.leaflet-popup-content .prow .v{text-align:end}
html .leaflet-tooltip{font-family:var(--eh-font);font-size:12px}
html.dark .leaflet-tooltip{background:var(--eh-paper);color:var(--eh-ink);border-color:var(--eh-line)}
html.dark .leaflet-bar a{background:var(--eh-paper);color:var(--eh-ink);border-color:var(--eh-line)}
html.dark .leaflet-control-attribution{background:rgba(21,33,74,.85);color:var(--eh-ink-2)}
html.dark .leaflet-control-attribution a{color:var(--eh-sea)}
/* modal */
.modal{background:rgba(13,23,54,.5)}
.modal .card,html.dark .modal .card,html.dark #modalCard{background:var(--eh-paper);color:var(--eh-ink);border-radius:var(--eh-r-panel);box-shadow:0 20px 50px -20px rgba(13,23,54,.5)}
.modal h2{font:600 21px/1.3 var(--eh-display);color:var(--eh-ink)}
.modal h4{font:600 15px/1.4 var(--eh-display);color:var(--eh-ink)}
.modal td,.modal th{border:1px solid var(--eh-line);text-align:start;font-size:12.5px}
.modal th{background:var(--eh-tint);color:var(--eh-ink-2)}
.modal .x{float:inline-end;color:var(--eh-ink-2)}
/* the colours the page scripts write inline, mapped to the shared tokens (one place for light and dark) */
:root body [style*="text-transform:uppercase"]{text-transform:none !important;letter-spacing:0 !important}
:root body [style*="color:#1A5FAB"],:root body [style*="color:#1A6FB0"]{color:var(--eh-sea) !important}
:root body [style*="color:#1C2B33"],:root body [style*="color:#3A4A52"]{color:var(--eh-ink) !important}
:root body [style*="color:#51626D"],:root body [style*="color:#5A6B76"],:root body [style*="color:#14456a"]{color:var(--eh-ink-2) !important}
:root body [style*="color:#8A99A3"],:root body [style*="color:#9A8C66"]{color:var(--eh-ink-3) !important}
:root body [style*="color:#1E6B38"],:root body [style*="color:#2E7D46"],:root body [style*="color:#2E7D3C"]{color:var(--eh-good) !important}
:root body [style*="color:#B23A3A"],:root body [style*="color:#8B1A1A"],:root body [style*="color:#C0392B"]{color:var(--eh-bad) !important}
:root body [style*="color:#8A6D2E"],:root body [style*="color:#9A7A1A"],:root body [style*="color:#7A6A3A"],:root body [style*="color:#B8860B"]{color:var(--eh-warn) !important}
:root body [style*="color:#0B7A99"]{color:var(--eh-info) !important}
:root body [style*="color:#E8862E"]{color:var(--eh-warn) !important}
:root body [style*="background:#F0FAFC"]{background:var(--eh-info-bg) !important}
:root body [style*="background:#FCF5F4"]{background:var(--eh-bad-bg) !important}
:root body [style*="background:#F2FAF4"]{background:var(--eh-good-bg) !important}
:root body [style*="background:#FBF6EC"]{background:var(--eh-warn-bg) !important}
:root body [style*="background:#E7EDF0"]{background:var(--eh-tint) !important}
:root body [style*="border:1px solid #CBE7EE"],:root body [style*="border:1px solid #F0D9D6"],:root body [style*="border:1px solid #CFE8D6"],:root body [style*="border:1px solid #E2E9EE"],:root body [style*="border:1px solid #D5DEE2"]{border-color:var(--eh-line) !important}
:root body [style*="border-top:1px solid #E7EDF0"]{border-top-color:var(--eh-line) !important}
/* "Ask the map" */
#ehcbtn{background:var(--eh-deep) !important;box-shadow:0 8px 22px -8px rgba(13,23,54,.6) !important}
html.dark #ehcbtn{background:var(--eh-sea) !important}
.ehch{background:var(--eh-deep) !important}
html.dark .ehch{background:#0A1230 !important}
.ehsend{background:var(--eh-sea) !important}
html .ehcx{margin-left:0;margin-inline-start:auto}
html .ehcb,html.dark .ehcb{background:var(--eh-mist) !important}
html .ehm,html.dark .ehm{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;color:var(--eh-ink) !important}
html .ehu,html.dark .ehu{background:var(--eh-info-bg) !important;border-color:transparent !important;color:var(--eh-ink) !important}
html .ehchip,html.dark .ehchip{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;color:var(--eh-sea) !important}
html .ehchip:hover,html.dark .ehchip:hover{background:var(--eh-info-bg) !important;border-color:var(--eh-sea) !important}
html .ehcf,html.dark .ehcf,html #ehcp,html.dark #ehcp{background:var(--eh-paper) !important;border-color:var(--eh-line) !important}
html .ehcf input,html.dark .ehcf input{background:var(--eh-paper);color:var(--eh-ink);border-color:var(--eh-line)}
/* dark scrollbars on the shared palette */
html.dark *{scrollbar-color:rgba(184,196,218,.3) transparent}
html.dark ::-webkit-scrollbar-track{background:transparent}
html.dark ::-webkit-scrollbar-thumb{background:#2A3A6B;border-color:var(--eh-paper)}
html.dark ::-webkit-scrollbar-thumb:hover{background:#3A4C80}
/* phones and tablets */
@media(max-width:1100px){.kpis{padding:12px 14px}}
@media(max-width:768px){
  header,html.dark header{padding:10px 12px 13px}
  html.eh-embedded.eh-page-stake header,html.inframe.eh-page-stake header,html.eh-embedded.eh-page-stake.dark header{padding:8px 12px 0 !important}
  .titles h1{font-size:15px}
  .kpis{gap:8px;padding:10px 12px}
  .kpi{padding:9px 10px;border-radius:11px}
  .kpi .v{font-size:19px}
  .kpi .l{font-size:12px;line-height:1.3;margin-top:3px}
  .tab{padding:10px 11px;font-size:13px}
  .legend{font-size:12px}
}
</style>'''

# ---------------- markup and CSS
rep('stake', '<link rel="stylesheet" href="eh-shared.css">', SKIN, 'design', 'page skin after the shared design system')
rep('stake', '<header>\n  <div class="logo">', '<header data-eh-contour="7">\n  <div class="logo">', 'design', 'standalone masthead contour lines')
rep('stake', '<div class="heatwrap">', '<div class="heatwrap eh-panel">', 'design', 'regional-view panels join the shared panel style and reveal', count=2)

# ---------------- tabs: the incoming view slides in from the reading-start edge
rep('stake', "  if(t==='lic')buildLicenceMap();\n}\nlet listSort=",
    "  if(t==='lic')buildLicenceMap();\n"
    "  if(window.EH_SHARED&&EH_SHARED.viewIn)EH_SHARED.viewIn(document.getElementById(t==='map'?'mapView':t+'View'));   // EH design v2: view change motion\n"
    "}\nlet listSort=", 'motion', 'view switch uses the shared view-in motion')

# ---------------- radial map chrome: brand guides, labels, fonts; data colours unchanged
rep('stake', "ctx.strokeStyle=(DKM?'#243039':'#E4ECE6');ctx.lineWidth=1;", "ctx.strokeStyle=(DKM?'#2A3A6B':'#D9E3DF');ctx.lineWidth=1;", 'design', 'wheel ring guides on the brand hairline')
rep('stake', "const BANDS=[[0.155,0.235,'26,95,171',0.045],[0.245,0.475,'214,69,69',0.05],[0.485,0.665,'201,162,39',0.045],[0.675,0.975,'63,163,77',0.035]];",
    "const BANDS=[[0.155,0.235,'0,114,187',0.045],[0.245,0.475,'178,63,43',0.05],[0.485,0.665,'201,138,27',0.045],[0.675,0.975,'84,171,93',0.035]];   // EH status set",
    'design', 'threat-band tints from the brand status set')
rep('stake', "ctx.strokeStyle=(DKM?'#202B33':'#EAF1EC');ctx.beginPath();", "ctx.strokeStyle=(DKM?'#22305E':'#E3EBE7');ctx.beginPath();", 'design', 'region dividers on the brand hairline')
rep('stake', "const SHORTRG={'Other Makkah Region':'OTHER MAKKAH','Makkah City':'MAKKAH','Madinah Region':'MADINAH','Qassim Region':'QASSIM','Tabuk Region':'TABUK','Hail Region':'HAIL','Al Jawf Region':'AL JAWF','Northern Borders Region':'N. BORDERS','Eastern Province':'EASTERN','Southern Region':'SOUTHERN','GCC / International':\"GCC / INT'L\"};",
    "const SHORTRG={'Other Makkah Region':'Other Makkah','Makkah City':'Makkah','Madinah Region':'Madinah','Qassim Region':'Qassim','Tabuk Region':'Tabuk','Hail Region':'Hail','Al Jawf Region':'Al Jawf','Northern Borders Region':'N. Borders','Eastern Province':'Eastern','Southern Region':'Southern','GCC / International':\"GCC / Int'l\"};",
    'design', 'wheel region labels in sentence case (were capitals)')
rep('stake', "const lab=(LNG==='ar'?regL(r):(SHORTRG[r]||r.toUpperCase()));", "const lab=(LNG==='ar'?regL(r):(SHORTRG[r]||r));", 'design', 'wheel region labels not forced to capitals')
rep('stake', "if(tier){ctx.strokeStyle=(DKM?'#22303A':'#E3EAE5');", "if(tier){ctx.strokeStyle=(DKM?'#2A3A6B':'#D9E3DF');", 'design', 'label leader ticks on the brand hairline')
rep('stake', "ctx.font=(lab.length>9?'600 8.5px':'600 10px')+' Segoe UI, sans-serif';", "ctx.font=(lab.length>9?'600 10px':'600 11px')+' \"EH Sans\",\"Segoe UI\",sans-serif';", 'design', 'wheel region labels in the brand font, readable size')
rep('stake', "ctx.fillStyle='#8A99A3';ctx.textAlign='center';ctx.fillText(lab,0,0);", "ctx.fillStyle=(DKM?'#9DABC5':'#5E6B80');ctx.textAlign='center';ctx.fillText(lab,0,0);", 'design', 'wheel region labels in ink-3 (AA) in both themes')
rep('stake', "ctx.fillStyle=(DKM?'#151C21':'#fff');ctx.fill();", "ctx.fillStyle=(DKM?'#15214A':'#fff');ctx.fill();", 'design', 'EH centre disc on the panel colour')
rep('stake', "ctx.lineWidth=3.5;ctx.strokeStyle='#3FA34D';", "ctx.lineWidth=3.5;ctx.strokeStyle='#54AB5D';", 'design', 'EH centre ring in logo green')
rep('stake', "ctx.fillStyle=(DKM?'#E6EDF1':'#1C2B33');ctx.font='800 13px Segoe UI,sans-serif';", "ctx.fillStyle=(DKM?'#E9EEF7':'#15224D');ctx.font='700 13px \"EH Display\",\"Segoe UI\",sans-serif';", 'design', 'EH centre fallback text in the brand display font')
rep('stake', "ctx.font='600 10px Segoe UI,sans-serif';ctx.fillStyle=(DKM?'#9FB3BE':'#51626D');", "ctx.font='600 11px \"EH Sans\",\"Segoe UI\",sans-serif';ctx.fillStyle=(DKM?'#B8C4DA':'#46546F');", 'design', 'EH centre caption in brand font and ink-2')
rep('stake', "const PILLS=[[0.195,t('REGULATORY','تنظيمي'),'#1A5FAB'],[0.36,t('HIGH THREAT','تهديد مرتفع'),'#B23A3A'],[0.575,t('MEDIUM','متوسط'),'#9A7A1A'],[0.84,t('LOW','منخفض'),'#2E7D3C']];",
    "const PILLS=[[0.195,t('Regulatory','تنظيمي'),(DKM?'#7CC3F2':'#0072BB')],[0.36,t('High threat','تهديد مرتفع'),(DKM?'#F0907D':'#B23F2B')],[0.575,t('Medium','متوسط'),(DKM?'#F0C26B':'#8F5C0A')],[0.84,t('Low','منخفض'),(DKM?'#7CCB82':'#2E7A37')]];   // EH status set, sentence case",
    'design', 'threat ring pills: sentence case, brand status colours readable in both themes')
rep('stake', "ctx.font='700 10px Segoe UI,sans-serif';ctx.textAlign='center';", "ctx.font='600 11px \"EH Sans\",\"Segoe UI\",sans-serif';ctx.textAlign='center';", 'design', 'ring pills in the brand font')
rep('stake', "ctx.fillStyle=(DKM?'rgba(15,21,25,0.85)':'rgba(255,255,255,0.88)');ctx.fill();", "ctx.fillStyle=(DKM?'rgba(21,33,74,0.94)':'rgba(255,255,255,0.94)');ctx.fill();", 'design', 'ring pill fill on the panel colour')
rep('stake', "ctx.font='600 9.5px Segoe UI,sans-serif';ctx.fillStyle=(DKM?'#C2D2DB':'#3A4A54');", "ctx.font='500 10.5px \"EH Sans\",\"Segoe UI\",sans-serif';ctx.fillStyle=(DKM?'#B8C4DA':'#46546F');", 'design', 'zoomed company names in the brand font and ink-2')
rep('stake', "ctx.lineWidth=1.6;ctx.strokeStyle='#0E3B6F';", "ctx.lineWidth=1.6;ctx.strokeStyle=(document.documentElement.classList.contains('dark')?'#A9B6E8':'#1B2A6E');", 'design', 'regulator ring in deep navy, visible in dark mode')
rep('stake', "ctx.strokeStyle=(DKM?'#E6EDF1':'#1C2B33');ctx.beginPath();ctx.arc(x,y,r+4", "ctx.strokeStyle=(DKM?'#E9EEF7':'#15224D');ctx.beginPath();ctx.arc(x,y,r+4", 'design', 'selected-node ring in brand ink')
rep('stake', "window.addEventListener('resize',resize);\nresize();recompute();\n",
    "window.addEventListener('resize',resize);\nresize();recompute();\n"
    "if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){try{draw();}catch(e){}});   // EH design v2: redraw once the brand fonts are in\n",
    'design', 'wheel redrawn once the brand fonts have loaded')
rep('stake', "Rings = competitive threat (HIGH inner → LOW outer)", "Rings = competitive threat (High inner → Low outer)", 'design', 'legend wording in sentence case (were capitals)')
rep('stake', '<b style="color:#1A5FAB">REGULATORY</b>', '<b style="color:#1A5FAB">Regulatory</b>', 'design', 'guide: ring names in sentence case to match the wheel')
rep('stake', '<b style="color:#B23A3A">HIGH THREAT</b>', '<b style="color:#B23A3A">High threat</b>', 'design', 'guide: ring names in sentence case to match the wheel')
rep('stake', '<b style="color:#9A7A1A">MEDIUM</b>', '<b style="color:#9A7A1A">Medium</b>', 'design', 'guide: ring names in sentence case to match the wheel')
rep('stake', '<b style="color:#2E7D3C">LOW</b>', '<b style="color:#2E7D3C">Low</b>', 'design', 'guide: ring names in sentence case to match the wheel')
# offline schematic Saudi map: province labels were forced to spaced capitals
rep('stake', """font-weight="700" fill="#B3A47C" letter-spacing="1.5" style="text-transform:uppercase;pointer-events:none">'+p.n.toUpperCase()+'</text>""",
    """font-weight="600" fill="#9A8C66" style="pointer-events:none">'+p.n+'</text>""", 'design', 'schematic map province labels in sentence case')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
if blocks(FILES['stake']) != BEFORE:
    sys.exit('ABORT: a data block changed — nothing written.')
CRLF = b'\r\n' in open(P, 'rb').read(4096)   # the published file uses Windows line endings; keep them so the diff is only the design
open(P, 'w', encoding='utf-8', newline='\r\n' if CRLF else '\n').write(FILES['stake'])
write_change_table(os.path.join(HERE, 'change_table_design_stake'), 'Design system v2 — Stakeholder & Competitive Map')
print('patched: hub/EH_Stakeholder_Map_CURRENT.html')
