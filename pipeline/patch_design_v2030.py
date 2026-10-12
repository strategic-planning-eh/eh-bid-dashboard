"""patch_design_v2030.py — EH design system v2 for the Vision 2030 projects page (hub/vision2030_dashboard.html),
12 Oct 2026.

Opened on its own, the page's header becomes the navy masthead the hub and the Bid & Tender app use: deep navy from the
shared tokens, EH's bathymetric contour lines drawn once, the logo on its white tile, the title in the brand display
face, and the land-to-sea line (leaf green → EH blue) along its lower edge. Inside the hub that header is not shown
(the hub's own masthead is there) and the two page tabs sit on the page colour as a quiet toolbar.

Everything else moves onto the one quiet surface system of eh-shared.css v2: mist page, white panels with a hairline,
labels in sentence case (no capitals, no tracking), project names, headings and figures in the brand display face, and
the page's own typefaces (Fraunces, Plus Jakarta Sans and, in the Arabic tab, Tajawal) replaced by the brand fonts —
EH Sans and EH Display carry Arabic glyphs themselves, so both tabs read as one product.

Colour: ownership, status, sector and data-confidence colours come from the brand palette (land → sea, amber, brick
for "on hold"); owner and status badges become soft pills (tinted fill, coloured word) instead of white text on strong
colour, so they read in both themes. Charts read their text, gridline and ring colours from the shared tokens each time
they are drawn, and are redrawn when the theme changes, so dark mode has no dark-on-dark legends.

Arabic tab: it is a separate report view (switchTab('arabic')). Its own dashboard mirror now reads right to left
throughout: the sector bar chart starts from the right, the search icon, the toggle switch and the confidence line sit
on the correct side, and the findings, corrections and recommendations use the same panels as the English tab.
Switching tabs slides the incoming view in from the reading-start edge (EH_SHARED.viewIn).

What it changes (exact-string edits; stops if an anchor is missing):
  • page skin inserted after eh-shared.css; it also beats the page's later dark-mode block (#ehDark)
  • masthead gets data-eh-contour; the two side drawers opt out of the scroll reveal (they slide on their own)
  • the Arabic findings and recommendation cards carry the shared panel class
  • palette constants, chart fonts and colours; the theme pass uses the brand dark tokens
  • a small script: redraw charts on theme change, tab change slides in

Run once:  python3 pipeline/patch_design_v2030.py
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import css_min, load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'vision2030_dashboard.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'v2030')

SKIN = r'''
/* EH design system v2 — Vision 2030 skin (patch_design_v2030.py). Tokens and fonts come from eh-shared.css.
   Rules are written as "html body …" (and repeated for body.dark) so they win over the page's later #ehDark block. */
html body,html body.dark{--bg:var(--eh-mist);--surface:var(--eh-paper);--ink:var(--eh-ink);--ink-soft:var(--eh-ink-2);--ink-faint:var(--eh-ink-3);
  --line:var(--eh-line);--line-strong:var(--eh-line);--brand:var(--eh-sea);--brand-deep:var(--eh-deep);--green:var(--eh-leaf);--accent:var(--eh-leaf-ink);
  --shadow:var(--eh-shadow);--shadow-lg:0 2px 0 rgba(21,34,77,.04),0 14px 30px -16px rgba(21,34,77,.32);
  --own-gov:#0072BB;--own-pif:#54AB5D;--own-jv:#00A0E0;--own-mixed:#5E6B80;
  background:var(--eh-mist) !important;color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead (standalone): deep navy, contour lines, land-to-sea line */
header.masthead{background:var(--eh-deep);border-bottom:0;position:relative;isolation:isolate;padding:24px clamp(20px,4vw,56px) 26px}
header.masthead>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header.masthead::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] header.masthead::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
.brand-logo{width:60px;height:60px;border-radius:12px;padding:6px;box-shadow:0 2px 10px -4px rgba(0,0,0,.4)}
html body .masthead h1{font:600 30px/1.2 var(--eh-display);letter-spacing:-.01em;color:#fff !important}
.masthead .kicker{font:600 12.5px var(--eh-font);text-transform:none;letter-spacing:0;color:#A8E3AD;margin-bottom:6px}
.masthead .sub{font-size:14px;line-height:1.55;color:rgba(255,255,255,.78);max-width:62ch}
.masthead .asof{font-size:12.5px;color:rgba(255,255,255,.72);text-align:end;border-left:0;padding-left:0;border-inline-start:1px solid rgba(255,255,255,.2);padding-inline-start:18px}
/* inside the hub the hub's masthead is the masthead: this one goes, the tabs stay on the page colour */
html.eh-embedded header.masthead{display:none}
/* page tabs */
html body .tab-nav{background:var(--eh-mist);border-bottom:1px solid var(--eh-line);padding:0 clamp(20px,4vw,56px)}
html body .tab-btn{font:600 13.5px var(--eh-font);color:var(--eh-ink-2);border-bottom:0;padding:13px 16px;box-shadow:inset 0 -3px 0 transparent;transition:color var(--eh-dur-1) var(--eh-ease),box-shadow var(--eh-dur-2) var(--eh-ease)}
html body .tab-btn:hover{color:var(--eh-ink);background:none}
html body .tab-btn.active{color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}
/* key figures */
.kpi-bar{gap:14px}
html body .kpi,html body .ar-kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;box-shadow:var(--eh-shadow);padding:16px 18px 15px}
html body .kpi .label,html body .ar-kpi .al{font:500 13px/1.4 var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2) !important;margin-bottom:0}
html body .kpi .value,html body .ar-kpi .av{font-family:var(--eh-display) !important;font-weight:600;font-size:28px;line-height:1.15;letter-spacing:-.01em;color:var(--eh-ink);font-variant-numeric:tabular-nums lining-nums;margin-top:6px}
html body .ar-kpi .av[style*="font-size:23px"]{font-size:23px !important}
.kpi .value small{font:500 14px var(--eh-font);color:var(--eh-ink-2)}
html body .kpi .seg,html body .ar-kpi .seg{font-size:12.5px;color:var(--eh-ink-2) !important}
html body .kpi .seg b,html body .ar-kpi .seg b{color:var(--eh-ink);font-weight:600;font-variant-numeric:tabular-nums}
.ar-kpi .asub{font-size:12px;color:var(--eh-ink-3)}
/* panels */
html body .panel,html body .chart-card,html body .ar-finding,html body .ar-rec-card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow)}
.grid{gap:18px}.charts{gap:18px}
/* filters */
html body aside.filters h2{font:600 16px var(--eh-display);text-transform:none;letter-spacing:0;color:var(--eh-ink) !important}
.filters .group>.gl{font:600 12.5px var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2)}
.reset-btn{font:600 12.5px var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-sea);border-radius:var(--eh-r-ctl)}
html body .chip,html body .conf-chip,html body .ar-chip{font:500 12.5px var(--eh-font);background:var(--eh-paper) !important;border:1px solid var(--eh-line) !important;color:var(--eh-ink-2) !important;border-radius:var(--eh-r-chip);transition:background-color var(--eh-dur-1) var(--eh-ease),border-color var(--eh-dur-1) var(--eh-ease),color var(--eh-dur-1) var(--eh-ease)}
html body .chip:hover,html body .conf-chip:hover,html body .ar-chip:hover{border-color:var(--eh-sea) !important;color:var(--eh-sea) !important}
html body .chip.active,html body .conf-chip.active,html body .ar-chip.active{background:#0072BB !important;border-color:#0072BB !important;color:#fff !important}
/* an active ownership chip keeps its owner colour (set inline by the page) */
html body .chip.own.active[style*="rgb(0, 114, 187)"]{background:#0072BB !important;border-color:#0072BB !important}
html body .chip.own.active[style*="rgb(84, 171, 93)"]{background:#2E7A37 !important;border-color:#2E7A37 !important}
html body .chip.own.active[style*="rgb(0, 160, 224)"]{background:#00729F !important;border-color:#00729F !important}
html body .chip.own.active[style*="rgb(94, 107, 128)"]{background:#5E6B80 !important;border-color:#5E6B80 !important}
.search-wrap svg{left:auto;inset-inline-start:11px;color:var(--eh-ink-3)}
html body .search-wrap input,html body .ar-search{background:var(--eh-paper) !important;border:1px solid var(--eh-line) !important;color:var(--eh-ink) !important;border-radius:var(--eh-r-ctl);font-family:var(--eh-font);padding:10px 12px;padding-inline-start:34px}
html body .ar-search{padding-inline-start:12px}
.search-wrap input:focus,.ar-search:focus{border-color:var(--eh-sea) !important}
.toggle-row{font-size:13px;color:var(--eh-ink-2)}
html body .tg-switch{background:var(--eh-line) !important}
html body .tg-knob{background:#fff !important}
html body .toggle-row.on .tg-switch{background:var(--eh-leaf-ink) !important}
.ar-panel .tg-knob{left:auto;right:2px}
.ar-panel .toggle-row.on .tg-knob{transform:translateX(-16px)}
/* charts */
html body .chart-card .ch-title{font:600 16px/1.35 var(--eh-display);text-transform:none;letter-spacing:0;color:var(--eh-ink)}
.chart-card .ch-sub{font-size:13px;color:var(--eh-ink-2)}
.chart-holder{height:240px}
/* toolbar */
.results-count{font-size:13.5px;color:var(--eh-ink-2)}
.results-count b{color:var(--eh-ink);font-variant-numeric:tabular-nums}
html body .view-toggle{background:var(--eh-tint) !important;border:1px solid var(--eh-line) !important;border-radius:var(--eh-r-ctl)}
html body .view-toggle button{font:600 12.5px var(--eh-font);color:var(--eh-ink-2);border-radius:7px}
html body .view-toggle button.active{background:var(--eh-paper) !important;border-color:transparent !important;color:var(--eh-sea) !important;box-shadow:0 1px 2px rgba(21,34,77,.12)}
/* project cards */
.cards,.ar-cards{gap:16px}
html body .card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);transition:transform var(--eh-dur-1) var(--eh-ease),box-shadow var(--eh-dur-1) var(--eh-ease),border-color var(--eh-dur-1) var(--eh-ease)}
html body .card:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg);border-color:var(--eh-line)}
.card .c-name,.ar-card .ac-name{font:600 17px/1.25 var(--eh-display);letter-spacing:-.005em;color:var(--eh-ink)}
.card .desc{font-size:13.5px;line-height:1.6;color:var(--eh-ink-2)}
html body .tag{font:500 12px var(--eh-font);background:var(--eh-tint) !important;color:var(--eh-ink-2) !important;border:0 !important;border-radius:6px;padding:3px 8px}
html body .ds-pill,html body .vf-pill{font:600 12px/1.5 var(--eh-font);text-transform:none;letter-spacing:0;border:0 !important;border-radius:var(--eh-r-chip);padding:2px 9px}
html body .ds-pill{background:var(--eh-bad-bg) !important;color:var(--eh-bad) !important}
html body .vf-pill{background:var(--eh-good-bg) !important;color:var(--eh-good) !important}
.status-pill{font-size:12.5px;color:var(--eh-ink-2)}
.card .c-meta{border-top-color:var(--eh-line)}
.card .figs{text-align:end;font-size:12px;color:var(--eh-ink-3)}
.card .figs b{font:600 15px var(--eh-display);color:var(--eh-ink);font-variant-numeric:tabular-nums lining-nums}
.conf-inline{font-size:12px;color:var(--eh-ink-3)}
.ar-panel .card .figs .conf-inline{justify-content:flex-end !important}
/* owner and status badges: soft pill, coloured word (the page writes the colour inline) */
/* 12px: below that eh-shared.js rewrites the inline style and the colour match below would miss */
html body .badge,html body .mini-badge{font:600 12px/1.5 var(--eh-font);text-transform:none;letter-spacing:0;border-radius:var(--eh-r-chip);padding:2px 10px;border:0 !important;color:#fff}
html body .badge[style*="#0072BB"],html body .mini-badge[style*="#0072BB"],html body .badge[style*="#5E9FD6"]{background:var(--eh-info-bg) !important;color:var(--eh-info) !important}
html body .badge[style*="#54AB5D"],html body .mini-badge[style*="#54AB5D"],html body .badge[style*="#2E7A37"],html body .badge[style*="#7FB685"],html body .badge[style*="#3f8a52"]{background:var(--eh-good-bg) !important;color:var(--eh-good) !important}
html body .badge[style*="#00A0E0"],html body .mini-badge[style*="#00A0E0"]{background:rgba(0,160,224,.14) !important;color:#006E99 !important}
html body.dark .badge[style*="#00A0E0"],html body.dark .mini-badge[style*="#00A0E0"]{color:#7FD6F7 !important}
html body .badge[style*="#5E6B80"],html body .mini-badge[style*="#5E6B80"]{background:var(--eh-muted-bg) !important;color:var(--eh-muted) !important}
html body .badge[style*="#C98A1B"]{background:var(--eh-warn-bg) !important;color:var(--eh-warn) !important}
html body .badge[style*="#B23F2B"],html body .badge[style*="#b5675c"]{background:var(--eh-bad-bg) !important;color:var(--eh-bad) !important}
html body .badge[style*="#3B57B8"]{background:rgba(59,87,184,.13) !important;color:#3B57B8 !important}
html body.dark .badge[style*="#3B57B8"]{color:#A9B6E8 !important}
html body .badge[style*="#8E6BB8"]{background:rgba(142,107,184,.15) !important;color:#6E4E99 !important}
html body.dark .badge[style*="#8E6BB8"]{color:#B79BDB !important}
html body .badge.soft,html body .badge.soft[style]{background:var(--eh-tint) !important;color:var(--eh-ink-2) !important}
/* inline colours the page writes, mapped to the shared tokens */
:root body [style*="color:#3f8a52"],:root body [style*="color:#3f9d57"]{color:var(--eh-good) !important}
:root body [style*="color:#b5675c"],:root body [style*="color:#c2705c"]{color:var(--eh-bad) !important}
:root body [style*="color:#e0a23c"]{color:var(--eh-warn) !important}
/* table */
html body .table-wrap{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow)}
html body thead th{background:var(--eh-tint) !important;color:var(--eh-ink-2);font:600 12.5px var(--eh-font);text-transform:none;letter-spacing:0;text-align:start;border-bottom:1px solid var(--eh-line)}
thead th:hover{color:var(--eh-sea)}
thead th.sorted .arr{color:var(--eh-sea)}
thead th .arr{margin-left:0;margin-inline-start:4px}
html body tbody td{border-bottom:1px solid var(--eh-line);border-color:var(--eh-line) !important;font-size:13px;color:var(--eh-ink)}
tbody tr:hover{background:var(--eh-tint)}
td .tname{font-weight:600;color:var(--eh-ink)}
.empty{color:var(--eh-ink-3)}.empty .big{font:600 19px var(--eh-display);color:var(--eh-ink-2)}
/* drawers */
html body .drawer{background:var(--eh-paper);color:var(--eh-ink)}
.drawer-head{border-bottom-color:var(--eh-line)}
.drawer-head .d-name{font:600 23px/1.2 var(--eh-display);letter-spacing:-.005em;color:var(--eh-ink)}
.drawer-head .d-lead{font-size:13px;color:var(--eh-ink-3);letter-spacing:0}
html body .drawer-head .close{background:var(--eh-tint) !important;color:var(--eh-ink-2) !important}
.d-section h3{font:600 13px var(--eh-font) !important;text-transform:none;letter-spacing:0;color:var(--eh-ink-2)}
.d-desc{font-size:14px;color:var(--eh-ink-2)}
html body .fact{background:var(--eh-tint) !important;border:1px solid transparent !important;border-radius:10px}
html body .fact .fl{font:600 12px var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2) !important}
html body .fact .fv{font-family:var(--eh-display);font-weight:600;color:var(--eh-ink) !important}
html body .fact [style*="font-size:10.5px"]{font-size:12px !important;color:var(--eh-ink-3) !important}
html body .note-box{background:var(--eh-warn-bg) !important;border:0 !important;border-inline-start:3px solid #C98A1B !important;color:var(--eh-ink) !important;border-radius:8px;font-size:13px}
html body .note-box.alert{background:var(--eh-bad-bg) !important;border-inline-start-color:var(--eh-bad) !important}
html body .note-box.alert *{color:var(--eh-ink) !important}
html body .jv-none{background:var(--eh-tint) !important;border:1px solid transparent !important;color:var(--eh-ink-2) !important}
.jv-item .jn,.jv-bar-top .jn{color:var(--eh-ink)}.jv-item .js,.jv-bar-top .js{color:var(--eh-ink-2)}
.jv-track{background:var(--eh-tint)}
.scrim{background:rgba(13,23,54,.45)}
/* methodology note */
html body .disclaimer{background:var(--eh-paper) !important;border:1px dashed var(--eh-line) !important;border-inline-start:3px solid var(--eh-sea) !important;border-radius:10px;font-size:13px;line-height:1.7;color:var(--eh-ink-2) !important}
.disclaimer strong{color:var(--eh-ink)}
/* Arabic tab */
.ar-panel,.ar-panel .filters,.ar-panel .chart-card,.ar-panel .toolbar,.ar-panel .card,.ar-panel table,.ar-drawer,.ar-search,.ar-chip{font-family:var(--eh-font)}
html body .ar-hero{background:var(--eh-deep);border-bottom:0;border-radius:var(--eh-r-panel);position:relative;overflow:hidden;padding:30px 34px 32px}
.ar-hero::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
html body .ar-hero h1{font:600 30px/1.45 var(--eh-display);color:#fff !important}
.ar-hero p{color:rgba(255,255,255,.8);font-size:14.5px}
html body .ar-hero p[style]{font-size:12.5px !important;color:#A8E3AD !important;font-weight:600 !important;margin-bottom:6px !important}
.ar-kpi-bar{gap:14px}
html body .ar-section-title{font:600 21px/1.4 var(--eh-display);text-transform:none;letter-spacing:0;color:var(--eh-ink)}
.ar-section-title::after{background:var(--eh-line)}
html body .ar-finding{border-inline-start:3px solid var(--eh-line);padding:18px 20px}
html body .ar-finding.warn{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;border-inline-start-color:#C98A1B !important}
html body .ar-finding.good{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;border-inline-start-color:var(--eh-leaf) !important}
html body .ar-finding.info{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;border-inline-start-color:var(--eh-sea) !important}
html body .afi{background:none !important;font-size:20px;margin-bottom:8px}
html body .ar-finding h3{font:600 16px/1.5 var(--eh-display) !important;color:var(--eh-ink) !important}
html body .ar-finding p{font-size:14px;line-height:1.75;color:var(--eh-ink-2) !important}
html body .ar-corr{background:var(--eh-warn-bg) !important;border:0 !important;border-inline-start:3px solid #C98A1B !important;border-radius:8px;color:var(--eh-ink) !important;font-size:14px;line-height:1.75}
.ar-corr strong{font-weight:700}
html body .ar-rec-card .rnum{font:600 15px var(--eh-display);background:var(--eh-sea);color:#fff}
html body .ar-rec-card h3{font:600 16px/1.5 var(--eh-display) !important;color:var(--eh-ink)}
.ar-rec-card p{font-size:14px;line-height:1.75;color:var(--eh-ink-2)}
html body .ar-miss-card{background:var(--eh-paper);border:1px dashed var(--eh-line);color:var(--eh-ink-2);font-size:13.5px;line-height:1.7}
.ar-miss-card strong{font:600 15px var(--eh-display);color:var(--eh-ink)}
.ar-panel thead th,.ar-panel tbody td{text-align:start}
.ar-panel .num,.ar-drawer .num{unicode-bidi:isolate}
/* English descriptions inside the Arabic view keep their own direction, so full stops and brackets land where they belong */
.ar-panel .card .desc,.ar-panel .card .figs,.ar-drawer .d-desc,.ar-drawer .drawer-head .d-lead{unicode-bidi:plaintext}
@media(max-width:768px){html body .masthead h1{font-size:21px}html body .kpi .value,html body .ar-kpi .av{font-size:24px}html body .ar-hero{padding:22px 18px 24px}html body .ar-hero h1{font-size:22px}html body .ar-section-title{font-size:18px}}
'''

# every "html body X" rule is also written as "html body.dark X", so it outranks the page's own "body.dark X" rules
def _dark_twin(css):
    def fix(m):
        out = []
        for s_ in re.split(r',(?![^\[(]*[\])])', m.group(1)):   # commas inside [..] or (..) are not selector separators
            out.append(s_)
            t = s_.strip()
            if t.startswith('html body ') and not t.startswith('html body.dark'):
                out.append(s_.replace('html body ', 'html body.dark ', 1))
        return ','.join(out) + '{'
    css = re.sub(r'(?m)^([^{}@/\n][^{}\n]*)\{', fix, css)
    # rules inside one-line @media blocks get the same treatment
    return re.sub(r'(?m)^(@media[^{]*\{)(.*)$', lambda m: m.group(1) + re.sub(r'(?:^|(?<=[{}]))([^{}]+)\{', fix, m.group(2)), css)

rep('v2030', '<link rel="stylesheet" href="eh-shared.css">',
    '<link rel="stylesheet" href="eh-shared.css">\n<style id="eh-skin">' + css_min(_dark_twin(SKIN)) + '</style>', 'design', 'page skin after the shared design system')
rep('v2030', '<header class="masthead">', '<header class="masthead" data-eh-contour="7">', 'design', 'masthead contour lines (standalone)')
rep('v2030', '<aside class="drawer panel ar-drawer" id="arDrawer"', '<aside class="drawer panel ar-drawer" id="arDrawer" data-eh-noreveal', 'motion', 'Arabic drawer slides on its own: no scroll reveal')
rep('v2030', '<aside class="drawer panel" id="drawer"', '<aside class="drawer panel" id="drawer" data-eh-noreveal', 'motion', 'drawer slides on its own: no scroll reveal')
rep('v2030', '<div class="ar-finding ', '<div class="eh-panel ar-finding ', 'motion', 'Arabic findings reveal like the other panels', count=8)
rep('v2030', '<div class="ar-rec-card">', '<div class="eh-panel ar-rec-card">', 'motion', 'Arabic recommendations reveal like the other panels', count=6)

# ---------------- palette constants
rep('v2030', 'const OWN_HEX    = {"Government":"#055a93","PIF":"#4fa85a","Joint Venture":"#0aa6a0","Mixed":"#6b7385"};',
    '/* EH design system v2 (patch_design_v2030.py): brand palette — land → sea, amber, brick for "on hold" */\n'
    'function ehTok(n,f){ try{ var v=getComputedStyle(document.body).getPropertyValue(n).trim(); return v||f; }catch(e){ return f; } }   // shared token, read at draw time\n'
    'const OWN_HEX    = {"Government":"#0072BB","PIF":"#54AB5D","Joint Venture":"#00A0E0","Mixed":"#5E6B80"};',
    'design', 'ownership colours from the brand palette; token reader for charts')
rep('v2030', 'const STATUS_HEX = {"Announced":"#7cc0e8","Planning":"#e0a23c","Under Construction":"#d9c23a","Partially Operational":"#8fce6a","Operational":"#3f9d57","On Hold":"#b5675c","Under Review":"#9a6f9c"};',
    'const STATUS_HEX = {"Announced":"#5E9FD6","Planning":"#C98A1B","Under Construction":"#3B57B8","Partially Operational":"#7FB685","Operational":"#2E7A37","On Hold":"#B23F2B","Under Review":"#8E6BB8"};',
    'design', 'status colours from the brand palette')
rep('v2030', 'const SECTOR_HEX = ["#0070b8","#4fa85a","#e08a3c","#0aa6a0","#8e6fc4","#d9b42a","#5b9bd5","#c0653a","#1d8f74","#d45d79","#6b7385"];',
    'const SECTOR_HEX = ["#0072BB","#54AB5D","#3B57B8","#00A0E0","#C98A1B","#8E6BB8","#A6CE39","#B23F2B","#5E9FD6","#7FB685","#5E6B80"];',
    'design', 'sector colours from the brand palette')
rep('v2030', 'hex:"#3f9d57", desc:"Confirmed', 'hex:"#2E7A37", desc:"Confirmed', 'design', 'confidence colours from the brand status set')
rep('v2030', 'hex:"#e0a23c", desc:"Reported', 'hex:"#C98A1B", desc:"Reported', 'design', 'confidence colours from the brand status set')
rep('v2030', 'hex:"#c2705c", desc:"Indicative', 'hex:"#B23F2B", desc:"Indicative', 'design', 'confidence colours from the brand status set')
# ---------------- charts: brand font, token colours read at draw time
rep('v2030', 'const gridColor="#ececea";\n  Chart.defaults.font.family="\'Plus Jakarta Sans\', sans-serif";\n  Chart.defaults.color="#4a5566";',
    'const gridColor=ehTok("--eh-line","#D9E3DF");\n  Chart.defaults.font.family="\'EH Sans\',\'Encode Sans\',\'Segoe UI\',Tahoma,Arial,sans-serif";\n  Chart.defaults.font.size=12.5;\n  Chart.defaults.color=ehTok("--eh-ink-2","#46546F");',
    'design', 'chart text in the brand font; colours from the shared tokens')
rep('v2030', 'const gridColor="#ececea";\n  const arFont="\'Tajawal\',sans-serif";',
    'const gridColor=ehTok("--eh-line","#D9E3DF");\n  const arFont="\'EH Sans\',\'Segoe UI\',Tahoma,Arial,sans-serif";   // brand font carries the Arabic glyphs\n  Chart.defaults.color=ehTok("--eh-ink-2","#46546F");',
    'design', 'Arabic charts in the brand font')
rep('v2030', 'backgroundColor:"#055a93"', 'backgroundColor:"#15224D"', 'design', 'chart tooltips in the brand ink', count=6)
rep('v2030', 'borderColor:"#fff"', 'borderColor:ehTok("--eh-paper","#fff")', 'design', 'doughnut rings cut in the panel colour (light and dark)', count=4)
rep('v2030', 'pointStyle:"circle",index:i}', 'pointStyle:"circle",fontColor:ehTok("--eh-ink-2","#46546F"),index:i}', 'design', 'doughnut legends readable in dark mode', count=2)
rep('v2030', 'font:{size:12,weight:"500"},padding:14,', 'font:{size:12.5,weight:"500"},padding:14,', 'design', 'English doughnut legend at a readable size')
rep('v2030', 'scales:{x:{beginAtZero:true,ticks:{precision:0,font:{size:11,family:arFont}},grid:{color:gridColor,drawBorder:false}},\n              y:{ticks:{font:{size:11.5,weight:"600",family:arFont}},grid:{display:false,drawBorder:false}}}}});',
    'scales:{x:{beginAtZero:true,reverse:true,ticks:{precision:0,font:{size:11.5,family:arFont}},grid:{color:gridColor,drawBorder:false}},\n              y:{position:"right",ticks:{font:{size:12,weight:"600",family:arFont}},grid:{display:false,drawBorder:false}}}}});',
    'rtl', 'Arabic sector chart reads from the right')
rep('v2030', "var c=dark?'#C9D4DB':'#666', g=dark?'#2C3A43':'#E5E5E5';",
    "var c=dark?'#B8C4DA':'#46546F', g=dark?'#2A3A6B':'#D9E3DF';   // brand ink and hairline (eh-shared.css v2)",
    'design', 'theme pass uses the brand light/dark chart colours')
rep('v2030', "ds.borderColor=dark?lift(ds.__ehO.b):ds.__ehO.b;",
    "ds.borderColor=(dark&&ch.config.type!=='doughnut')?lift(ds.__ehO.b):ds.__ehO.b;   // doughnut rings are cut in the panel colour, not lifted",
    'design', 'doughnut rings keep the panel colour in dark mode')
rep('v2030', '<script src="eh-shared.js" defer></script>',
    "<script>\n/* EH design system v2 (patch_design_v2030.py): charts redraw with the token colours when the theme changes;\n"
    "   switching tabs slides the incoming view in from the reading-start edge. */\n"
    "(function(){\n"
    "  var dark=document.body.classList.contains('dark');\n"
    "  function redraw(){ try{ if(typeof renderCharts==='function'&&typeof filtered==='function') renderCharts(filtered()); }catch(e){}\n"
    "    try{ if(typeof arInited!=='undefined'&&arInited&&typeof arRenderCharts==='function') arRenderCharts(arFiltered()); }catch(e){} }\n"
    "  try{ new MutationObserver(function(){ var d=document.body.classList.contains('dark'); if(d!==dark){ dark=d; redraw(); } }).observe(document.body,{attributes:true,attributeFilter:['class']}); }catch(e){}\n"
    "  if(dark) redraw();\n"
    "  var tab=window.switchTab;\n"
    "  if(typeof tab==='function'){ window.switchTab=function(t){ tab.apply(this,arguments);\n"
    "    var p=document.getElementById(t==='arabic'?'panel-arabic':'panel-dashboard'); if(window.EH_SHARED&&EH_SHARED.viewIn) EH_SHARED.viewIn(p); }; }\n"
    "})();\n</script>\n<script src=\"eh-shared.js\" defer></script>",
    'motion', 'chart redraw on theme change; tab change slides in')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['v2030'])
write_change_table(os.path.join(HERE, 'change_table_design_v2030'), 'Design system v2 — Vision 2030 projects')
print('patched: hub/vision2030_dashboard.html')
