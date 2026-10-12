"""patch_design_news.py — EH design system v2 for Corporate & Government News (hub/eh_news_intelligence.html), 12 Oct 2026.

The news page is a hand-maintained page (no pipeline generator writes it), so the design goes straight into the
published HTML, through exact-string edits that stop if an anchor is missing:
  • page skin after eh-shared.css: the page's own colour variables now point at the shared tokens, so light and dark
    both come from one place; the Fraunces serif is gone (headings and KPI numbers in the brand display font,
    Montserrat / Alexandria); labels in sentence case; KPI tiles lose their coloured edges; the fact-check verdicts
    become status words with a shape (dot, ring, square, diamond, dash) as well as a colour
  • standalone masthead: deep navy with EH's contour lines, the logo on a white tile and the land-to-sea line along
    its lower edge (inside the hub the masthead is still removed by eh-shared.css section 2)
  • the old dark-mode block (hard-coded greys and blues) is replaced by token rules; the Arabic report loses the
    coloured bar before its headings and takes the same surfaces as the English view
  • charts: brand palette (land → sea), brand fonts once they have loaded, gridlines and axis text from the tokens in
    both themes, and the horizontal "news category" chart mirrors in Arabic (labels on the right, bars grow leftwards)
  • motion: the fact-check, watch-list and big-picture panels join the shared reveal; switching Cards / Table slides
    the new view in; the slide-out story panel is kept out of the reveal (it flashed open on load before)

Words, numbers, filters and links are unchanged.

Run once:  python3 pipeline/patch_design_news.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'eh_news_intelligence.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'news')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Corporate & Government News skin (patch_design_news.py). Tokens and fonts come from eh-shared.css. */
/* the page's own variables, mapped to the shared tokens (declared on body so body.dark re-resolves them) */
body,body.dark{--eh-green:var(--eh-leaf);--eh-blue:var(--eh-sea);--eh-green-d:var(--eh-leaf-ink);--eh-green-l:var(--eh-good-bg);--eh-blue-d:var(--eh-sea-ink);--eh-blue-l:var(--eh-info-bg);
  --ink:var(--eh-ink);--ink-soft:var(--eh-ink-2);--muted:var(--eh-ink-3);--line:var(--eh-line);--line-2:var(--eh-line);--bg:var(--eh-mist);--card:var(--eh-paper);
  --flag:var(--eh-bad);--flag-bg:var(--eh-bad-bg);--flag-line:var(--eh-line);--amber:var(--eh-warn);--amber-bg:var(--eh-warn-bg);
  --shadow-sm:var(--eh-shadow);--shadow:0 1px 0 rgba(21,34,77,.05),0 12px 26px -14px rgba(21,34,77,.32);--radius:var(--eh-r-panel);--radius-sm:12px;
  background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
h1,h2,h3,h4,.serif{font-family:var(--eh-display);font-weight:600;letter-spacing:0}
a{color:var(--eh-sea)}
/* masthead (standalone; inside the hub eh-shared.css removes it) */
.topbar{display:none}
header.masthead{background:var(--eh-deep);border-bottom:0;color:#fff;position:relative;isolation:isolate}
body.dark header.masthead{background:#0A1230}
header.masthead>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header.masthead::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] header.masthead::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
.mast-inner{padding:34px 0 28px}
header.masthead .logo{height:52px;background:#fff;border-radius:11px;padding:4px 6px;box-shadow:0 2px 10px -4px rgba(0,0,0,.4)}
body.dark header.masthead .logo{filter:none}
.eyebrow{font-size:12.5px;font-weight:600;letter-spacing:0;text-transform:none;color:#A8E3AD}
.mast-titles h1{font:600 26px/1.18 var(--eh-display);color:#fff;margin:3px 0 4px;letter-spacing:-.005em}
.mast-sub{font-size:13.5px;color:rgba(255,255,255,.76)}
.mast-meta{text-align:end;font-size:12.5px;color:rgba(255,255,255,.76)}
.mast-meta .period{color:#fff;font-weight:600;font-size:13.5px}
.btn-print{font:600 12.5px var(--eh-font);color:#fff;background:transparent;border:1px solid rgba(255,255,255,.32);border-radius:var(--eh-r-ctl);padding:6px 12px}
.btn-print:hover{background:rgba(255,255,255,.1)}
#ehLangBar{border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);background:var(--eh-paper);box-shadow:var(--eh-shadow)}
#ehLangBar button,body.dark #ehLangBar button{font:600 12.5px var(--eh-font);background:var(--eh-paper);color:var(--eh-ink-2)}
#ehLangBar button.on,body.dark #ehLangBar button.on{background:var(--eh-sea);color:#fff}
/* KPI tiles: no coloured edges; numbers lead */
.kpis{gap:12px;margin:22px 0 6px}
.kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:16px 16px 15px;box-shadow:var(--eh-shadow)}
.kpi::before{display:none}
.kpi .k-num{font:600 28px/1.08 var(--eh-display);color:var(--eh-ink);font-variant-numeric:tabular-nums lining-nums}
.kpi .k-num small{font:500 14px var(--eh-font);color:var(--eh-ink-3);margin-inline-start:3px}
.kpi .k-lab{font-size:13px;font-weight:600;color:var(--eh-ink);margin-top:8px;line-height:1.35}
.kpi .k-note{font-size:12px;color:var(--eh-ink-3);margin-top:4px;line-height:1.45}
/* section headings */
section{margin:36px 0}
.sec-head{border-bottom:1px solid var(--eh-line);padding-bottom:12px;margin-bottom:16px;align-items:center;flex-wrap:wrap}
.sec-head .num{font:600 13px var(--eh-display);background:var(--eh-tint);color:var(--eh-sea-ink);border-radius:8px;width:28px;height:28px}
.sec-head h2{font:600 22px/1.25 var(--eh-display);color:var(--eh-ink)}
.sec-head .sh-sub{font-size:13px;color:var(--eh-ink-2);margin-left:0;margin-inline-start:auto;line-height:1.45}
#sec-audit .sec-head .sh-sub{flex-basis:100%;margin-inline-start:0;padding-inline-start:40px}
/* chart panels */
.charts{gap:14px}
.chart-card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;box-shadow:var(--eh-shadow)}
.chart-card h3{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);margin-bottom:3px}
.chart-card .c-sub{font-size:13px;color:var(--eh-ink-2);margin-bottom:12px}
.chart-foot{font-size:12px;color:var(--eh-ink-3);line-height:1.5}
/* filter bar */
.filters{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);padding:14px 16px}
.fgroup label{font-size:12.5px;font-weight:600;letter-spacing:0;text-transform:none;color:var(--eh-ink-2)}
.fgroup select,.fgroup input[type=text]{font-size:13px;color:var(--eh-ink);background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl)}
.fgroup select:focus,.fgroup input:focus{border-color:var(--eh-sea);box-shadow:0 0 0 3px var(--eh-info-bg)}
.toggle{font-size:13px;color:var(--eh-ink-2)}
.toggle input{accent-color:var(--eh-bad)}
.view-toggle{border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);margin-left:0;margin-inline-start:auto}
.view-toggle button,body.dark .view-toggle button{font:600 13px var(--eh-font);background:var(--eh-paper);color:var(--eh-ink-2);border:0}
.view-toggle button.active,body.dark .view-toggle button.active{background:var(--eh-sea);color:#fff}
.btn-reset{font:600 13px var(--eh-font);color:var(--eh-sea);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);background:transparent}
.btn-reset:hover{color:var(--eh-sea);border-color:var(--eh-sea);background:var(--eh-info-bg)}
/* scope headers and story cards: blue = company news, green = government (a scope mark, kept on the reading-start edge) */
.scope-bar .dot{border-radius:50%}
.scope-bar.corp .dot{background:var(--eh-sea)}.scope-bar.gov .dot{background:var(--eh-leaf)}
.scope-bar h3{font:600 16px var(--eh-display);color:var(--eh-ink)}
.scope-bar .cnt{font-size:12.5px;color:var(--eh-ink-3);margin-left:0;margin-inline-start:4px}
.scope-bar .legend{font-size:12px;color:var(--eh-ink-3);margin-left:0;margin-inline-start:auto}
.cards{gap:12px}
.card{background:var(--eh-paper);border:1px solid var(--eh-line);border-left-width:1px;border-inline-start:3px solid var(--eh-sea);border-radius:12px;padding:15px 17px;box-shadow:var(--eh-shadow)}
.card.gov{border-left-color:var(--eh-line);border-inline-start-color:var(--eh-leaf)}
.card:hover{box-shadow:0 1px 0 rgba(21,34,77,.05),0 12px 26px -14px rgba(21,34,77,.32);transform:translateY(-1px)}
body.dark .card:hover{box-shadow:0 1px 0 rgba(0,0,0,.25),0 14px 28px -14px rgba(0,0,0,.7)}
.entity{font-weight:700;font-size:14px;color:var(--eh-ink)}
.card .c-group{font-size:12px;color:var(--eh-ink-3);font-weight:500}
.card .c-head{font-size:14px;color:var(--eh-ink-2);line-height:1.5}
.card .c-more{font-size:12.5px;font-weight:600;color:var(--eh-sea)}
.flag-strip{right:auto;inset-inline-end:0;border-top-right-radius:11px;border-color:transparent var(--eh-bad) transparent transparent}
[dir=rtl] .flag-strip{border-width:0 0 22px 22px;border-color:transparent transparent transparent var(--eh-bad);border-top-right-radius:0;border-top-left-radius:11px}
/* chips: soft fills from the token set */
.chip,body.dark .chip{font-size:11.5px;font-weight:600;letter-spacing:0;border-radius:var(--eh-r-chip);border:0}
.chip-cat,body.dark .chip-cat{color:var(--eh-info);background:var(--eh-info-bg)}
.card.gov .chip-cat,body.dark .card.gov .chip-cat{color:var(--eh-good);background:var(--eh-good-bg)}
.chip-date,body.dark .chip-date{color:var(--eh-ink-2);background:var(--eh-tint)}
.chip-flag,body.dark .chip-flag{color:var(--eh-bad);background:var(--eh-bad-bg)}
.chip-conf{font-size:11.5px;display:inline-flex;align-items:center;gap:5px}
.chip-conf::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.conf-High,body.dark .conf-High{color:var(--eh-good);background:var(--eh-good-bg)}.conf-High::before{border-radius:50%}
.conf-Medium,body.dark .conf-Medium{color:var(--eh-warn);background:var(--eh-warn-bg)}.conf-Medium::before{border-radius:1px}
.conf-Low,body.dark .conf-Low{color:var(--eh-muted);background:var(--eh-muted-bg)}.conf-Low::before{height:2px}
.c-svc,body.dark .c-svc{font-size:11.5px;font-weight:600;color:var(--eh-good);background:var(--eh-good-bg)}
.c-svc.muted,body.dark .c-svc.muted{color:var(--eh-muted);background:var(--eh-muted-bg)}
html.eh-floor .c-svc,html.eh-floor .c-svc.muted{font-size:12px}
.svc-chip{font-size:12px;color:var(--eh-good);background:var(--eh-good-bg);border:0;border-radius:var(--eh-r-chip)}
.svc-note{font-size:13px;color:var(--eh-ink-2);background:var(--eh-tint);border-left:0;border-inline-start:3px solid var(--eh-leaf);border-radius:0 8px 8px 0}
[dir=rtl] .svc-note{border-radius:8px 0 0 8px}
.scope-tag,.fr-ent .scope-mini{font-size:11px;font-weight:600;border-radius:var(--eh-r-chip)}
.scope-tag.c,.fr-ent .sm-c{color:var(--eh-info);background:var(--eh-info-bg)}
.scope-tag.g,.fr-ent .sm-g{color:var(--eh-good);background:var(--eh-good-bg)}
.flag-row .fr-ent .scope-mini{margin-left:0;margin-inline-start:6px}
/* table view */
.tbl-wrap{border:1px solid var(--eh-line);border-radius:12px;background:var(--eh-paper);box-shadow:var(--eh-shadow)}
table.dt thead th,body.dark table.dt thead th{text-align:start;font-size:12.5px;letter-spacing:0;text-transform:none;font-weight:600;color:var(--eh-ink-2);background:var(--eh-tint) !important;border-bottom:1px solid var(--eh-line)}
table.dt thead th .arr{margin-left:0;margin-inline-start:3px}
table.dt tbody td,body.dark table.dt tbody td{border-bottom:1px solid var(--eh-line) !important;font-size:13px}
table.dt tbody tr:hover{background:var(--eh-tint)}
table.dt .t-ent{color:var(--eh-ink)}table.dt .t-head{color:var(--eh-ink-2)}
.empty{color:var(--eh-ink-2);background:var(--eh-paper);border-color:var(--eh-line)}
/* items to watch */
.flag-wrap,body.dark .flag-wrap{background:var(--eh-paper) !important;border:1px solid var(--eh-line) !important;border-radius:var(--eh-r-panel)}
.flag-banner,body.dark .flag-banner{background:var(--eh-bad-bg) !important;color:var(--eh-ink) !important;border-bottom:1px solid var(--eh-line) !important;border-inline-start:3px solid var(--eh-bad);font-size:13px;font-weight:500}
@media(min-width:1081px){.flag-row,.flag-head-row{grid-template-columns:minmax(0,1.4fr) minmax(0,2.2fr) minmax(0,.9fr) minmax(0,1.5fr)}.foot-grid{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}}
.flag-row{border-bottom:1px solid var(--eh-line)}
.flag-row:hover{background:var(--eh-tint)}
.flag-row .fr-ent{font-weight:700;font-size:13.5px}
.flag-row .fr-desc{font-size:13px;color:var(--eh-ink-2);line-height:1.5}
.flag-row .fr-val{font:600 13px var(--eh-display);color:var(--eh-bad);font-variant-numeric:tabular-nums}
.flag-row .fr-link{font-size:12px;color:var(--eh-ink-3)}
.flag-head-row,body.dark .flag-head-row{background:var(--eh-tint) !important;color:var(--eh-ink-2) !important;border-color:var(--eh-line) !important;font-size:12.5px;letter-spacing:0;text-transform:none;font-weight:600}
/* the big picture */
.highlights{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);padding:26px 30px}
.highlights .lead{font:500 17px/1.6 var(--eh-display);color:var(--eh-ink);border-bottom:1px solid var(--eh-line)}
.hl-item h4,.hl-item h4.blue,body.dark .hl-item h4.blue{font:600 15px/1.4 var(--eh-display) !important;letter-spacing:0;text-transform:none;color:var(--eh-ink) !important;margin-bottom:6px}
.hl-item p{font-size:14px;color:var(--eh-ink-2)}
/* fact-check */
.audit-wrap,body.dark .audit-wrap{background:var(--eh-paper) !important;border:1px solid var(--eh-line) !important;border-radius:var(--eh-r-panel)}
.audit-banner{background:var(--eh-tint);border-bottom:1px solid var(--eh-line);color:var(--eh-ink-2);font-size:13px}
.audit-banner .big{font:600 19px var(--eh-display);color:var(--eh-ink)}
.audit-row{border-top:1px solid var(--eh-line)}
.a-num{font:600 13px var(--eh-display);color:var(--eh-ink-3)}
.a-claim{font-weight:600;font-size:14px;color:var(--eh-ink)}
.a-note{font-size:13px;color:var(--eh-ink-2);line-height:1.55}
.audit-open,body.dark .audit-open{background:var(--eh-tint) !important;color:var(--eh-ink-2) !important;border-top:1px solid var(--eh-line) !important;font-size:13px}
.audit-open strong,body.dark .audit-open strong{color:var(--eh-ink) !important}
/* verdicts: a word plus a shape, in sentence case */
.verdict,body.dark .verdict{display:inline-flex;align-items:center;gap:6px;font:600 12px var(--eh-font);letter-spacing:0;text-transform:lowercase;border:0 !important;border-radius:var(--eh-r-chip);padding:3px 10px 3px 9px}
.verdict::first-letter{text-transform:uppercase}
.verdict::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.v-conf,body.dark .verdict.v-conf{color:var(--eh-good) !important;background:var(--eh-good-bg) !important}.v-conf::before{border-radius:50%}
.v-upd,body.dark .verdict.v-upd{color:var(--eh-info) !important;background:var(--eh-info-bg) !important}.v-upd::before{background:none;border:1.5px solid currentColor;border-radius:50%}
.v-clar,body.dark .verdict.v-clar{color:var(--eh-warn) !important;background:var(--eh-warn-bg) !important}.v-clar::before{border-radius:1px}
.v-corr,body.dark .verdict.v-corr{color:var(--eh-bad) !important;background:var(--eh-bad-bg) !important}.v-corr::before{border-radius:1px;transform:rotate(45deg)}
.v-open,body.dark .verdict.v-open{color:var(--eh-muted) !important;background:var(--eh-muted-bg) !important}.v-open::before{height:2px}
/* slide-out story panel */
.overlay{background:rgba(13,23,54,.45)}
.panel{background:var(--eh-mist);box-shadow:-12px 0 40px rgba(13,23,54,.22)}
.panel:not(.open){box-shadow:none}
.panel-head{background:var(--eh-paper);border-bottom:1px solid var(--eh-line)}
.panel-head h3{font:600 19px/1.3 var(--eh-display);color:var(--eh-ink)}
.panel-id{font-size:12px;color:var(--eh-ink-3)}
.panel-close,body.dark .panel-close{background:var(--eh-paper) !important;border:1px solid var(--eh-line);color:var(--eh-ink-2) !important;border-radius:var(--eh-r-ctl)}
.panel-close:hover{background:var(--eh-tint) !important}
.pf .pf-lab{font-size:12.5px;letter-spacing:0;text-transform:none;font-weight:600;color:var(--eh-ink-2)}
.pf .pf-lab::before{display:none}
.pf .pf-val{font-size:14px;color:var(--eh-ink-2)}
.pf .pf-val.big{color:var(--eh-ink)}
.giga-box{background:var(--eh-bad-bg);border:0;border-inline-start:3px solid var(--eh-bad);border-radius:10px}
.giga-box .gb-lab{font-size:12.5px;letter-spacing:0;text-transform:none;font-weight:600;color:var(--eh-bad)}
.giga-box .gb-val{font-size:13.5px;color:var(--eh-ink)}
.src-list li{font-size:13px}
.src-list li::before{color:var(--eh-sea)}
/* footer */
footer.foot{border-top:1px solid var(--eh-line)}
.foot h3{font:600 16px var(--eh-display);color:var(--eh-ink)}
.foot p,.foot li{font-size:13px;color:var(--eh-ink-2)}
.foot .small{font-size:12px;color:var(--eh-ink-3)}
.cov-meter{background:var(--eh-tint);height:8px}
.cov-fill{background:var(--eh-sea)}
.tier-legend span{font-size:12px;color:var(--eh-ink-2)}
.tier-dot{border-radius:50%}
html .vlist li,html.eh-floor .vlist li{font-size:12.5px;color:var(--eh-ink-2)}
.vlist li::before{color:var(--eh-leaf-ink);margin-right:0;margin-inline-end:6px}
.note-box{background:var(--eh-info-bg);border:0;border-inline-start:3px solid var(--eh-sea);border-radius:0 10px 10px 0;color:var(--eh-ink-2);font-size:13px;line-height:1.6}
[dir=rtl] .note-box{border-radius:10px 0 0 10px}
.note-box strong{color:var(--eh-ink)}
.disclaimer{font-size:12px;color:var(--eh-ink-3);border-top:1px solid var(--eh-line)}
/* Arabic */
html[dir=rtl] .kpi,html[dir=rtl] .chart-card{text-align:start}
html[dir=rtl] .kpi .k-num{direction:ltr;unicode-bidi:isolate;text-align:right}
html[dir=rtl] .chart-card h3{line-height:1.5}
@media(max-width:768px){
  .kpi .k-num{font-size:23px}
  .sec-head h2{font-size:19px}
  .sec-head .sh-sub{margin-inline-start:0}
  .highlights{padding:18px}
  .card{padding:13px 14px}
  .mast-meta{text-align:start}
}
</style>'''

DARK = r'''<style id="ehDark">
/* dark theme (patch_design_news.py): the shared tokens switch under body.dark; only what tokens cannot express is here */
body.dark{background:var(--eh-mist) !important;color:var(--eh-ink)}
body.dark svg text,body.dark svg tspan{fill:var(--eh-ink-2) !important}
body.dark svg .domain,body.dark svg g.tick line{stroke:var(--eh-line)}
body.dark .muted{color:var(--eh-muted) !important}
'''

AR = r'''#ehArView{display:none;max-width:1040px;margin:0 auto;padding:64px 26px 60px;font-size:15px;line-height:2;color:var(--eh-ink)}
body.ar-mode #ehArView{display:block}
#ehArView h1{font:600 27px/1.6 var(--eh-display);color:var(--eh-ink);margin:6px 0 10px}
#ehArView h2{font:600 21px/1.5 var(--eh-display);margin:34px 0 8px;color:var(--eh-ink)}
#ehArView h3{font:600 16px/1.5 var(--eh-display);margin:20px 0 6px;color:var(--eh-ink)}
#ehArView .avc{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:14px 18px;margin:12px 0;box-shadow:var(--eh-shadow)}
#ehArView .avwarn{background:var(--eh-warn-bg);border:0;border-inline-start:3px solid var(--eh-warn);border-radius:12px;padding:14px 18px;margin:12px 0;color:var(--eh-ink)}
#ehArView .avred{background:var(--eh-bad-bg);border:0;border-inline-start:3px solid var(--eh-bad);border-radius:12px;padding:14px 18px;margin:12px 0;color:var(--eh-ink)}
#ehArView ul{padding-inline-start:22px}
#ehArView li{margin:5px 0}
#ehArView .avmeta{font-size:12.5px;color:var(--eh-ink-3);margin-top:30px;border-top:1px solid var(--eh-line);padding-top:12px}
#ehArView b{color:var(--eh-ink)}
#ehArView .avnote{font-size:13px;color:var(--eh-ink-3)}
'''

# ---------------- skin + masthead
rep('news', '<link rel="stylesheet" href="eh-shared.css">', SKIN, 'design', 'page skin after the shared design system')
rep('news', '<header class="masthead">', '<header class="masthead" data-eh-contour="7">', 'design', 'standalone masthead contour lines')
# ---------------- panels join the shared reveal; the slide-out story panel stays out of it
rep('news', '<div class="audit-wrap">', '<div class="audit-wrap eh-panel">', 'motion', 'fact-check panel joins the reveal')
rep('news', '<div class="flag-wrap">', '<div class="flag-wrap eh-panel">', 'motion', 'watch-list panel joins the reveal')
rep('news', '<div class="highlights">', '<div class="highlights eh-panel">', 'motion', 'big-picture panel joins the reveal')
rep('news', '<aside class="panel" id="panel" aria-hidden="true">', '<aside class="panel" id="panel" aria-hidden="true" data-eh-noreveal>',
    'motion', 'story panel kept out of the reveal (it flashed open on load)')
# Cards / Table switch: the incoming view slides in
rep('news', "document.getElementById('v-card').classList.remove('active'); render();});",
    "document.getElementById('v-card').classList.remove('active'); render(); ehViewSwap();});", 'motion', 'Table view slides in')
rep('news', "document.getElementById('v-table').classList.remove('active'); render();});",
    "document.getElementById('v-table').classList.remove('active'); render(); ehViewSwap();});\n"
    "function ehViewSwap(){ if(window.EH_SHARED&&EH_SHARED.viewIn){ document.querySelectorAll('#sec-corp .scope-block,#sec-gov .scope-block').forEach(function(el){ EH_SHARED.viewIn(el); }); } }",
    'motion', 'Cards view slides in')

# ---------------- charts: brand palette, fonts, token colours, Arabic mirroring
rep('news', "const PALETTE=['#2563eb','#0ea5e9','#06b6d4','#14b8a6','#10b981','#22c55e','#84cc16','#eab308','#f59e0b','#f97316','#ef4444','#f43f5e','#ec4899','#a855f7','#6366f1'];",
    "// EH design system v2: land → sea palette from the logo and the EH profile\n"
    "const PALETTE=['#0072BB','#54AB5D','#3B57B8','#00A0E0','#C98A1B','#8E6BB8','#A6CE39','#B23F2B','#5E9FD6','#7FB685'];",
    'design', 'brand chart palette')
rep('news', "Chart.defaults.font.family=\"'Plus Jakarta Sans',sans-serif\";\nChart.defaults.font.size=11;\nChart.defaults.color='#64748b';",
    "Chart.defaults.font.family=\"'EH Sans','Encode Sans','Segoe UI',Tahoma,Arial,sans-serif\";\nChart.defaults.font.size=12;\nChart.defaults.color='#5E6B80';\n"
    "Chart.defaults.borderColor='#D9E3DF';\nconst EH_RTL=()=>document.documentElement.dir==='rtl';",
    'design', 'chart text in the brand font, axis colour from the tokens')
rep('news', "backgroundColor:PALETTE, borderColor:'#fff', borderWidth:2}]},\n  options:{cutout:'58%', plugins:{legend:{position:'right', labels:{boxWidth:10, padding:8, font:{size:10}}}}}",
    "backgroundColor:PALETTE, borderColor:'#fff', borderWidth:2}]},\n  options:{cutout:'60%', plugins:{legend:{position:'right', labels:{boxWidth:9, boxHeight:9, usePointStyle:true, pointStyle:'circle', padding:9, font:{size:12}}}}}",
    'design', 'sector donut legend readable')
rep('news', "backgroundColor:catData.map((_,i)=>colorFor(i)), borderRadius:5, barThickness:14}]},\n  options:{indexAxis:'y', plugins:{legend:{display:false}},\n    scales:{x:{beginAtZero:true, ticks:{precision:0, stepSize:1}, grid:{color:'#eceff3'}}, y:{grid:{display:false}, ticks:{font:{size:10}}}}}",
    "backgroundColor:catData.map(()=>'#0072BB'), borderRadius:4, barThickness:14}]},\n  options:{indexAxis:'y', plugins:{legend:{display:false}},\n    scales:{x:{beginAtZero:true, reverse:EH_RTL(), ticks:{precision:0, stepSize:1}, grid:{color:'#D9E3DF'}}, y:{position:EH_RTL()?'right':'left', grid:{display:false}, ticks:{font:{size:12}}}}}",
    'design', 'news-category bars in one brand colour; mirrored in Arabic')
rep('news', "backgroundColor:['#2563eb','#06b6d4','#f59e0b'], borderRadius:5, barThickness:30}]},",
    "backgroundColor:['#0072BB','#00A0E0','#C98A1B'], borderRadius:4, barThickness:30}]},", 'design', 'new-money bars in brand colours')
rep('news', "scales:{y:{beginAtZero:true, grid:{color:'#eceff3'}, ticks:{callback:v=>'$'+v+'bn'}}, x:{grid:{display:false}, ticks:{font:{size:10}}}}}",
    "scales:{y:{beginAtZero:true, grid:{color:'#D9E3DF'}, ticks:{callback:v=>'$'+v+'bn'}}, x:{grid:{display:false}, ticks:{font:{size:12}}}}}",
    'design', 'new-money axis readable')
rep('news', "/* ----- init ----- */\nrender();\nrenderFlagged();",
    "/* ----- init ----- */\nrender();\nrenderFlagged();\n"
    "/* EH design system v2: redraw once the brand fonts are in; mirror the horizontal bar chart when the page turns Arabic */\n"
    "(function(){\n"
    "  const all=()=>Object.values(Chart.instances||{});\n"
    "  if(document.fonts&&document.fonts.load){ Promise.all([document.fonts.load(\"500 12px 'EH Sans'\"),document.fonts.load(\"500 12px 'EH Sans'\",'\\u0639\\u0631\\u0628\\u064a')]).then(()=>all().forEach(ch=>{try{ch.update('none');}catch(e){}})).catch(()=>{}); }\n"
    "  function mirror(){ const rtl=EH_RTL(); all().forEach(ch=>{ try{ const o=ch.config.options; if(o.indexAxis!=='y'||!o.scales)return; o.scales.x.reverse=rtl; o.scales.y.position=rtl?'right':'left'; ch.update('none'); }catch(e){} }); }\n"
    "  try{ new MutationObserver(mirror).observe(document.documentElement,{attributes:true,attributeFilter:['dir']}); }catch(e){}\n"
    "})();",
    'rtl', 'brand fonts redraw; horizontal bars mirror in Arabic')

# ---------------- dark theme: tokens instead of hard-coded colours
rep_re('news', r'<style id="ehDark">\nbody\.dark\{--eh-green-l:.*?body\.dark \.blue\{color:#7FB4E8 !important\}\n', lambda m: DARK,
       'dark', 'old dark-mode block replaced by token rules')
rep_re('news', r'#ehLangBar\{position:fixed;top:10px;left:12px;z-index:9999;display:flex;gap:0;border:1px solid rgba\(128,148,160,\.4\);border-radius:8px;overflow:hidden;font-family:inherit\}\n.*?body\.dark #ehLangBar button\.on\{background:#0E5A9E;color:#fff\}\n',
       lambda m: '#ehLangBar{position:fixed;top:10px;left:12px;z-index:9999;display:flex;gap:0;border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);overflow:hidden;font-family:inherit}\n'
                 '#ehLangBar button{border:0;padding:6px 14px;font-size:12.5px;font-weight:600;cursor:pointer;background:var(--eh-paper);color:var(--eh-ink-2)}\n'
                 '#ehLangBar button.on{background:var(--eh-sea);color:#fff}\n',
       'dark', 'language bar from the tokens')
rep_re('news', r'#ehArView\{display:none;max-width:1040px.*?body\.dark #ehArView \.avnote\{color:#93A6B2\}\n', lambda m: AR,
       'design', 'Arabic report: token surfaces, no coloured bar before headings')
# chart theme: axis and grid colours from the tokens; brand series get their dark-theme twins
rep('news', "var c=dark?'#C9D4DB':'#666', g=dark?'#2C3A43':'#E5E5E5';",
    "var cs=getComputedStyle(document.body), c=(cs.getPropertyValue('--eh-ink-3')||'').trim()||(dark?'#9DABC5':'#5E6B80'), g=(cs.getPropertyValue('--eh-line')||'').trim()||(dark?'#2A3A6B':'#D9E3DF');\n"
    "    var DK={'#0072BB':'#4EB0EE','#54AB5D':'#7CCB82','#3B57B8':'#A9B6E8','#00A0E0':'#38C6F4','#C98A1B':'#E8B04A','#8E6BB8':'#B79BDB','#A6CE39':'#C2E06A','#B23F2B':'#F0907D','#5E9FD6':'#8CC0EC','#7FB685':'#A3D3A8','#FFF':'#15214A','#FFFFFF':'#15214A'};",
    'dark', 'chart axis/grid colours from the tokens')
rep('news', "      var p=pl(x); if(!p) return x;",
    "      if(Array.isArray(x)) return x.map(lift);\n"
    "      if(typeof x==='string'&&DK[x.toUpperCase()]) return DK[x.toUpperCase()];\n"
    "      var p=pl(x); if(!p) return x;",
    'dark', 'brand series colours switch to their dark-theme twins (arrays included)')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['news'])
write_change_table(os.path.join(HERE, 'change_table_design_news'), 'Design system v2 — Corporate & Government News')
print('patched: hub/eh_news_intelligence.html')
