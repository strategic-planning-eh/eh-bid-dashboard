"""patch_design_fisc.py — EH design system v2 for the Saudi Government Finances page
(hub/saudi_fiscal_monitor_2026.html), 12 Oct 2026.

The page keeps its deep-navy opening, because deep navy is one of the three brand things, but it now takes that navy
from the shared tokens, carries EH's bathymetric contour lines when opened on its own (not inside the hub, where the
hub masthead already has them) and ends in the land-to-sea line (leaf green → EH blue) that follows reading direction.
Everything below the opening moves onto the one quiet surface system of eh-shared.css v2: mist page, white panels with
a hairline, no coloured top edges on the key-figure tiles, no gradient washes on table rows, labels in sentence case
(no capitals, no tracking), headings and numbers in the brand display face with tabular figures, and the page's own
typefaces (Plus Jakarta Sans and Fraunces) replaced by the brand fonts everywhere, the charts included.

Charts: series take the brand palette (land → sea, then amber, brick for loss), axis text in the brand ink, gridlines
in the brand hairline colour; the dark-theme pass the page already runs uses the brand dark tokens. In Arabic the two
horizontal bar charts (B and D) read from the right: category labels on the right, bars growing leftwards; the month
and quarter axes stay left to right.

Arabic: the Arabic edition (eh-ar-dashboard.js full mode, saudi_fiscal_monitor_2026.ar.json) swaps text in place, so
the same layout must work right to left: borders, margins and alignment that were hard-coded to the left now use
logical properties, and status pills carry a shape as well as a colour.

What it changes (exact-string edits; stops if an anchor is missing):
  • page skin inserted after eh-shared.css; it also beats the page's later dark-mode block (#ehDark)
  • opening header gets data-eh-contour
  • chart palette, chart fonts and axis colours; dark-theme chart colours from the brand dark tokens
  • a small script that mirrors charts B and D when the page switches to Arabic

Run once:  python3 pipeline/patch_design_fisc.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'saudi_fiscal_monitor_2026.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'fisc')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Saudi Government Finances skin (patch_design_fisc.py). Tokens and fonts come from eh-shared.css.
   Rules are written as "html body …" so they also win over the page's later dark-mode block (#ehDark). */
html body,html body.dark{--navy:var(--eh-deep);--navy2:var(--eh-deep);--blue:var(--eh-sea);--blue-d:var(--eh-sea-ink);--blue-tint:var(--eh-info-bg);
  --green:var(--eh-leaf);--green-d:var(--eh-leaf-ink);--green-tint:var(--eh-good-bg);--rag-red:var(--eh-bad);--rag-amber:#C98A1B;--rag-green:var(--eh-good);
  --red-tint:var(--eh-bad-bg);--amber-tint:var(--eh-warn-bg);--bg:var(--eh-mist);--card:var(--eh-paper);--line:var(--eh-line);
  --t1:var(--eh-ink);--t2:var(--eh-ink-2);--t3:var(--eh-ink-3);--radius:var(--eh-r-panel);--gap:18px;--shadow:var(--eh-shadow);
  background:var(--eh-mist) !important;color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* section bar: navy on its own, a quiet toolbar on the page colour inside the hub */
html body .topnav{background:var(--eh-deep);backdrop-filter:none;border-bottom:1px solid rgba(255,255,255,.1)}
.topnav .wrap{height:auto;min-height:58px;flex-wrap:wrap;row-gap:4px;padding-block:6px}
html:not(.eh-embedded) .topnav .wrap{padding-inline-end:118px}   /* room for the fixed EN/AR switch */
.topnav .brand{font:600 14px var(--eh-font)}
.topnav .brand img{width:30px;height:30px;border-radius:8px;padding:3px}
.topnav .vtag{font:500 11.5px var(--eh-font);letter-spacing:0;background:rgba(255,255,255,.1);color:rgba(255,255,255,.85);border:1px solid rgba(255,255,255,.2);border-radius:var(--eh-r-chip);padding:2px 10px}
.topnav nav{margin-left:0;margin-inline-start:auto}
.topnav nav a{font:600 13px var(--eh-font);color:rgba(255,255,255,.78);border-radius:var(--eh-r-ctl);transition:color var(--eh-dur-1) var(--eh-ease),background-color var(--eh-dur-1) var(--eh-ease)}
.topnav nav a:hover{color:#fff;background:rgba(255,255,255,.1)}
html.eh-embedded body .topnav{background:var(--eh-mist);border-bottom:1px solid var(--eh-line)}
html.eh-embedded .topnav .wrap{height:auto;min-height:52px}
html.eh-embedded .topnav nav{margin-inline-start:0}
html.eh-embedded .topnav nav a{color:var(--eh-ink-2)}
html.eh-embedded .topnav nav a:hover{color:var(--eh-ink);background:var(--eh-tint)}
/* language switch (standalone only) */
html body #ehLangBar{border:1px solid rgba(255,255,255,.3);border-radius:var(--eh-r-ctl);top:12px;left:auto;inset-inline-end:14px;inset-inline-start:auto}
html body #ehLangBar button{font:600 12.5px var(--eh-font);background:var(--eh-deep);color:rgba(255,255,255,.85);min-height:32px}
html body #ehLangBar button.on{background:#fff;color:#1B2A6E}
/* opening: deep navy, contour lines (standalone), land-to-sea line along the lower edge */
html body .hero{background:var(--eh-deep);position:relative;isolation:isolate;padding:40px 0 34px}
.hero>.eh-contour{color:#6FB6EA;opacity:.42;z-index:-1}
html.eh-embedded .hero>.eh-contour{display:none}
.hero::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] .hero::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
html body .hero h1{font:600 32px/1.22 var(--eh-display);color:#fff !important;letter-spacing:-.01em;max-width:1000px;margin-bottom:12px}
.hero .sub{font-size:15.5px;line-height:1.65;color:rgba(255,255,255,.8);font-weight:400;max-width:940px}
.hero .sub b{color:#fff}
.hero .meta{font-size:13px;color:rgba(255,255,255,.66);gap:8px 22px}
.hero .meta b{color:#fff;font-weight:600}
html body .hero .ctx-badge{font:600 11.5px/1.5 var(--eh-font);text-transform:none;letter-spacing:0;background:rgba(255,255,255,.1) !important;color:rgba(255,255,255,.88) !important;border:1px solid rgba(255,255,255,.2) !important;padding:4px 12px;border-radius:var(--eh-r-chip)}
html body .hero .ctx-badge.upd{background:rgba(84,171,93,.2) !important;border-color:rgba(124,203,130,.5) !important;color:#C8EBCB !important}
html body .hero .ctx-badge.war{background:rgba(178,63,43,.32) !important;border-color:rgba(240,144,125,.55) !important;color:#FFD9CF !important}
html body .ctx-note{background:rgba(255,255,255,.06) !important;border:1px solid rgba(255,255,255,.14) !important;border-radius:12px;color:rgba(255,255,255,.84) !important;font-size:14px;line-height:1.7;padding:18px 20px}
html body .ctx-note b{color:#fff !important}
.ctx-note .corr{color:#F0C26B}.ctx-note .rev{color:#F0907D}.ctx-note .good{color:#7CCB82}
.prov-legend{font-size:12.5px;color:rgba(255,255,255,.72)}
.prov-legend>span[style]{color:#fff !important;font-weight:600 !important}
.dot{border-radius:50%}.dot.off{background:var(--eh-leaf)}.dot.an{background:#C98A1B;border-radius:2px}.dot.sc{background:#4EB0EE;border-radius:2px;transform:rotate(45deg) scale(.85)}
/* section headings: sentence case, brand display type */
section{padding:30px 0;scroll-margin-top:100px}
.sec-head{gap:10px 12px;align-items:center}
html body .sec-head h2{font:600 22px/1.3 var(--eh-display);color:var(--eh-ink) !important}
html body .sec-num{font:600 12.5px var(--eh-font);letter-spacing:0;text-transform:lowercase;color:var(--eh-sea-ink) !important;background:var(--eh-info-bg);border-radius:var(--eh-r-chip);padding:2px 10px}
.sec-num::first-letter{text-transform:uppercase}
html body .sec-sub{font-size:14.5px;line-height:1.6;color:var(--eh-ink-2) !important;max-width:80ch}
html body .upd-chip{font:600 12px var(--eh-font);text-transform:none;letter-spacing:0;background:var(--eh-good-bg) !important;color:var(--eh-good) !important;border:1px solid transparent !important;border-radius:var(--eh-r-chip);padding:2px 10px}
html body .upd-chip.warn{background:var(--eh-bad-bg) !important;color:var(--eh-bad) !important}
/* provenance tags: a word plus a shape */
html body .tag{font:600 11.5px/1.5 var(--eh-font);text-transform:none;letter-spacing:0;border-radius:var(--eh-r-chip);padding:2px 9px 2px 8px;display:inline-flex;align-items:center;gap:5px;border:0 !important}
.tag::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
html body .tag.off{background:var(--eh-good-bg) !important;color:var(--eh-good) !important}.tag.off::before{border-radius:50%}
html body .tag.an{background:var(--eh-warn-bg) !important;color:var(--eh-warn) !important}.tag.an::before{border-radius:1px}
html body .tag.sc{background:var(--eh-info-bg) !important;color:var(--eh-info) !important}.tag.sc::before{border-radius:1px;transform:rotate(45deg) scale(.85)}
/* key figures: no coloured top edges; the number leads */
.kpi-grid{gap:14px}
html body .kpi{background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:12px;box-shadow:var(--eh-shadow);padding:16px 17px 14px}
html body .kpi.red,html body .kpi.amber,html body .kpi.green{border-top-color:var(--eh-line)}
/* 11.5px here (and on .ksrc, .csrc, .tag, .riskpill, .ctx-badge) is deliberate: eh-shared.js lifts any text under 12px to
   12px with an inline style before the Arabic twin is swapped in, and the swap matches on that markup — so these keep
   exactly the words they showed before the restyle. They render at 12px. See the report for the shared fix. */
html body .kpi .klabel{font:500 11.5px/1.4 var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2) !important}
html body .kpi .kval{font:600 28px/1.1 var(--eh-display);color:var(--eh-ink) !important;letter-spacing:-.01em;font-variant-numeric:tabular-nums lining-nums}
.kpi .kunit{font:500 13px var(--eh-font);color:var(--eh-ink-3);margin-left:0;margin-inline-start:4px}
.kpi .kdelta{font-size:12.5px;font-weight:600;line-height:1.45;margin-top:8px;display:block}
.kdelta.up{color:var(--eh-good)}.kdelta.down{color:var(--eh-bad)}.kdelta.flat{color:var(--eh-ink-2)}.kdelta.warn{color:var(--eh-warn)}
.kpi .ksrc{font-size:11.5px;color:var(--eh-ink-3);border-top-color:var(--eh-line)}
/* chart panels */
.chart-grid{gap:18px}
html body .card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow);color:var(--eh-ink);padding:20px 22px}
html body .card h3{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink) !important}
.card .csub{font-size:13.5px;line-height:1.55;color:var(--eh-ink-2);max-width:none}
.card .chead{gap:10px 14px}
.chart-box{height:330px}.chart-box.tall{height:390px}
.csrc{font-size:11.5px;color:var(--eh-ink-3);border-top-color:var(--eh-line)}
html body .callout{background:var(--eh-warn-bg) !important;border:0 !important;border-inline-start:3px solid #C98A1B !important;border-radius:0 8px 8px 0;color:var(--eh-ink) !important;font-size:13.5px;line-height:1.6;padding:10px 14px}
[dir=rtl] .callout{border-radius:8px 0 0 8px !important}
html body .callout.blue{background:var(--eh-info-bg) !important;border-inline-start-color:var(--eh-sea) !important}
html body .callout.red{background:var(--eh-bad-bg) !important;border-inline-start-color:var(--eh-bad) !important}
html body .callout.green{background:var(--eh-good-bg) !important;border-inline-start-color:var(--eh-leaf) !important}
html body .callout b,html body .callout strong{color:var(--eh-ink) !important}
/* tables: tinted head, sentence case, scenario rows marked by an edge instead of a colour wash */
html body .tbl-wrap{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow)}
html body table.scen th{background:var(--eh-tint) !important;color:var(--eh-ink-2);text-align:start;font:600 12.5px/1.4 var(--eh-font);text-transform:none;letter-spacing:0;border-bottom:1px solid var(--eh-line)}
html body table.scen td{border-bottom:1px solid var(--eh-line);border-color:var(--eh-line) !important;font-size:13.5px;line-height:1.55;color:var(--eh-ink)}
table.scen tr.opt td,table.scen tr.base td,table.scen tr.pess td{background:none}
table.scen tr td:first-child{border-inline-start:3px solid transparent}
table.scen tr.opt td:first-child{border-inline-start-color:var(--eh-leaf)}
table.scen tr.base td:first-child{border-inline-start-color:#C98A1B}
table.scen tr.pess td:first-child{border-inline-start-color:var(--eh-bad)}
table.scen tbody tr:hover td{background:var(--eh-tint)}
table.scen .sname{font:600 14px/1.4 var(--eh-display)}
table.scen tr.opt .sname{color:var(--eh-good)}table.scen tr.base .sname{color:var(--eh-warn)}table.scen tr.pess .sname{color:var(--eh-bad)}
table.scen .big{font:600 15px var(--eh-display);font-variant-numeric:tabular-nums lining-nums;white-space:nowrap}
.riskpill{font:600 11.5px/1.5 var(--eh-font);border-radius:var(--eh-r-chip);padding:2px 10px 2px 9px;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.riskpill::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.riskpill.low{background:var(--eh-good-bg);color:var(--eh-good)}.riskpill.low::before{border-radius:50%}
.riskpill.mod{background:var(--eh-warn-bg);color:var(--eh-warn)}.riskpill.mod::before{border-radius:1px}
.riskpill.high{background:var(--eh-bad-bg);color:var(--eh-bad)}.riskpill.high::before{border-radius:1px;transform:rotate(45deg)}
.basis{font-size:12px;color:var(--eh-ink-3)}
/* sources */
.src-grid{gap:16px}
html body .src-card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);box-shadow:var(--eh-shadow)}
html body .src-badge{font:600 13px var(--eh-display);border-radius:10px;color:#fff !important;border:0 !important}
html body .src-badge[style*="#0A2A43"]{background:#1B2A6E !important}
html body .src-badge[style*="#7A1F1F"],html body .src-badge[style*="#C0392B"]{background:#B23F2B !important}
html body .src-badge[style*="#0572BC"]{background:#0072BB !important}
html body .src-badge[style*="#54AB5D"]{background:#2E7A37 !important}
html body .src-badge[style*="#1f6f8b"]{background:#3B57B8 !important}
html body .src-badge[style*="#5A6A7A"]{background:#5E6B80 !important}
html body.dark .src-badge[style*="#0A2A43"]{background:#3B57B8 !important}
.src-card .sname2{font:600 14.5px/1.3 var(--eh-display);color:var(--eh-ink)}
.src-card .sdate{font-size:12px;color:var(--eh-ink-3)}
html body .src-card .shead{font-size:13.5px;font-weight:600;color:var(--eh-sea-ink) !important}
.src-card .sdesc{font-size:13px;line-height:1.55;color:var(--eh-ink-2)}
html body .disclaimer{background:var(--eh-paper) !important;border:1px dashed var(--eh-line) !important;border-inline-start:3px solid var(--eh-sea) !important;border-radius:10px;color:var(--eh-ink-2) !important;font-size:13px;line-height:1.7}
html body .disclaimer b{color:var(--eh-ink)}
html body b,html body strong{color:inherit}
html body .card b,html body .sec-sub b{color:var(--eh-ink)}
/* footer on the deep navy */
footer{background:var(--eh-deep);color:rgba(255,255,255,.72);font-size:13px}
footer [style*="Fraunces"]{font-family:var(--eh-display) !important;font-weight:600}
footer ul{font-size:12.5px;color:rgba(255,255,255,.66)}
footer [style*="#9fb6cb"]{color:rgba(255,255,255,.66) !important}
html body footer b{color:#fff}
/* the analyst-written Arabic report (fallback when the full Arabic twin is missing) */
html body #ehArView{color:var(--eh-ink)}
html body #ehArView h1{font:600 26px/1.5 var(--eh-display);color:var(--eh-ink)}
html body #ehArView h2{font:600 20px/1.5 var(--eh-display);color:var(--eh-ink);border-inline-start:3px solid var(--eh-leaf)}
html body #ehArView h3{font:600 16px/1.5 var(--eh-display);color:var(--eh-ink)}
html body #ehArView .avc,html body #ehArView .avwarn,html body #ehArView .avred{background:var(--eh-paper);border:1px solid var(--eh-line);border-inline-start:3px solid var(--eh-sea);color:var(--eh-ink)}
html body #ehArView .avwarn{border-inline-start-color:#C98A1B}html body #ehArView .avred{border-inline-start-color:var(--eh-bad)}
html body #ehArView b{color:var(--eh-ink)}html body #ehArView .avnote,html body #ehArView .avmeta{color:var(--eh-ink-3);border-color:var(--eh-line)}
/* Arabic: labels sit right, figures stay left-to-right */
[dir=rtl] .kpi,[dir=rtl] .card,[dir=rtl] .src-card{text-align:start}
[dir=rtl] .kpi .kval{unicode-bidi:plaintext;text-align:right}
[dir=rtl] .hero h1{line-height:1.45}
[dir=rtl] .card h3{line-height:1.5}
[dir=rtl] table.scen .big{direction:ltr;unicode-bidi:isolate;text-align:start}
@media(max-width:1080px){html body .hero h1{font-size:26px}}
@media(max-width:560px){html.eh-embedded body .topnav{display:none}}   /* inside the hub on a phone the bar would be empty: its links are hidden at this width */
@media(max-width:768px){html body .hero h1{font-size:21px;line-height:1.3}.hero{padding:28px 0 26px}html body .sec-head h2{font-size:19px}html body .kpi .kval{font-size:24px}html body .card{padding:14px}.chart-box{height:300px}.chart-box.tall{height:340px}}
</style>'''

# every "html body X" rule is also written as "html body.dark X", so it outranks the page's own "body.dark X" rules
import re as _re
def _dark_twin(css):
    def fix(m):
        sels = _re.split(r',(?![^\[(]*[\])])', m.group(1))   # commas inside [..] or (..) are not separators
        out = []
        for s_ in sels:
            out.append(s_)
            t = s_.strip()
            if t.startswith('html body ') and not t.startswith('html body.dark'):
                out.append(s_.replace('html body ', 'html body.dark ', 1))
        return ','.join(out) + '{'
    css = _re.sub(r'(?m)^([^{}@/\n][^{}\n]*)\{', fix, css)
    # rules inside one-line @media blocks get the same treatment
    return _re.sub(r'(?m)^(@media[^{]*\{)(.*)$', lambda m: m.group(1) + _re.sub(r'(?:^|(?<=[{}]))([^{}]+)\{', fix, m.group(2)), css)
SKIN = _dark_twin(SKIN)
rep('fisc', '<link rel="stylesheet" href="eh-shared.css">', SKIN, 'design', 'page skin after the shared design system')
rep('fisc', '<header class="hero" id="overview">', '<header class="hero" id="overview" data-eh-contour="7">', 'design', 'contour lines in the opening (standalone only)')

# ---------------- charts: brand palette, fonts and axis colours
rep('fisc', "const C = {\n  blue:'#0572BC', blued:'#045a96', green:'#54AB5D', grey:'#94A3B8', greyd:'#64748b',\n  red:'#D32F2F', amber:'#F9A825', ragGreen:'#388E3C', navy:'#0A2A43'\n};",
    "/* EH design system v2 (patch_design_fisc.py): brand chart palette — land → sea, amber, brick for loss */\n"
    "const C = {\n  blue:'#0072BB', blued:'#00609E', green:'#54AB5D', grey:'#AEB9CE', greyd:'#5E6B80',\n  red:'#B23F2B', amber:'#C98A1B', ragGreen:'#2E7A37', navy:'#1B2A6E'\n};",
    'design', 'brand chart palette')
rep('fisc', "Chart.defaults.font.family = \"'Plus Jakarta Sans', sans-serif\";\nChart.defaults.font.size = 12;\nChart.defaults.color = '#5A6A7A';\nconst GRID = '#eef2f7';",
    "Chart.defaults.font.family = \"'EH Sans','Encode Sans','Segoe UI',Tahoma,Arial,sans-serif\";   // brand font (Arabic glyphs come from the same family)\n"
    "Chart.defaults.font.size = 12.5;\nChart.defaults.color = '#5E6B80';\n"
    "Chart.defaults.plugins.tooltip.backgroundColor = '#15224D'; Chart.defaults.plugins.tooltip.padding = 10; Chart.defaults.plugins.tooltip.cornerRadius = 8;\n"
    "Chart.defaults.plugins.tooltip.titleFont = {weight:'600'};\n"
    "const GRID = '#D9E3DF';",
    'design', 'chart text in the brand font and ink; gridlines in the brand hairline colour')
rep('fisc', "color:'#8a98a8'", "color:'#5E6B80'", 'design', 'axis titles in the brand footnote ink', count=7)
rep('fisc', "font:{size:11,weight:'600'},color:", "font:{size:12,weight:'600'},color:", 'design', 'axis titles at a readable size', count=7)
rep('fisc', "ctx.font='700 10px Plus Jakarta Sans';", "ctx.font=\"600 11px 'EH Sans','Encode Sans',sans-serif\";", 'design', 'event markers in the brand font')
rep('fisc', "ticks:{font:{size:10.5},autoSkip:false}", "ticks:{font:{size:11.5},autoSkip:false}", 'design', 'chart D sector labels at a readable size')
rep('fisc', "backgroundColor:['#c7d2dd','#c7d2dd',C.red,C.green]", "backgroundColor:[C.grey,C.grey,C.red,C.green]", 'design', 'chart C pre-war bars in the brand muted grey')
rep('fisc', "backgroundColor:'rgba(10,42,67,.06)'", "backgroundColor:'rgba(27,42,110,.06)'", 'design', 'chart E fill from the brand navy')
rep('fisc', "backgroundColor:'rgba(5,114,188,.35)'", "backgroundColor:'rgba(0,114,187,.3)'", 'design', 'chart G planned bars from the brand blue')
rep('fisc', "borderColor:'#b8c2cf'", "borderColor:'#AEB9CE'", 'design', 'chart E reference line in the brand muted grey')
rep('fisc', "borderColor:'#94A3B8', borderWidth:1.6", "borderColor:'#5E6B80', borderWidth:1.6", 'design', 'chart F 2025 line in the brand muted ink')
rep('fisc', "var c=dark?'#C9D4DB':'#666', g=dark?'#2C3A43':'#E5E5E5';",
    "var c=dark?'#B8C4DA':'#5E6B80', g=dark?'#2A3A6B':'#D9E3DF';   // brand ink and hairline (eh-shared.css v2)",
    'design', 'theme pass uses the brand light/dark chart colours')
# Arabic: the two horizontal bar charts read from the right
rep('fisc', '<script src="eh-ar-dashboard.js" defer></script>',
    "<script>\n/* EH design system v2 (patch_design_fisc.py): in Arabic the horizontal bar charts (B, D) read from the right —\n"
    "   category labels on the right, bars grow leftwards. Time axes are left as they are. */\n"
    "(function(){\n"
    "  function mirror(){ var rtl=document.documentElement.dir==='rtl';\n"
    "    ['chartB','chartD'].forEach(function(id){ var cv=document.getElementById(id), ch=cv&&window.Chart&&Chart.getChart&&Chart.getChart(cv); if(!ch)return;\n"
    "      var s=ch.config.options.scales; if(!s||!s.x||!s.y)return; if(!!s.x.reverse===rtl&&(s.y.position||'left')===(rtl?'right':'left'))return;\n"
    "      s.x.reverse=rtl; s.y.position=rtl?'right':'left'; try{ ch.update('none'); }catch(e){} }); }\n"
    "  /* value axes: a left-to-right mark before each figure keeps the minus sign in front of negative numbers in Arabic */\n"
    "  function ltrTicks(){ if(!window.Chart||!Chart.getChart)return; [].forEach.call(document.querySelectorAll('canvas'),function(cv){ var ch=Chart.getChart(cv); if(!ch||ch.__ehLtr)return; ch.__ehLtr=1;\n"
    "      var s=ch.config.options.scales||{}; Object.keys(ch.scales||{}).forEach(function(k){ if(ch.scales[k].type!=='linear'||!s[k])return; s[k].ticks=s[k].ticks||{}; var f=s[k].ticks.callback;\n"
    "        s[k].ticks.callback=function(v){ var o=f?f.apply(this,arguments):Chart.Ticks.formatters.numeric.apply(this,arguments); return (typeof o==='string'||typeof o==='number')?'\\u200E'+o:o; }; });\n"
    "      try{ ch.update('none'); }catch(e){} }); }\n"
    "  ltrTicks();\n"
    "  try{ new MutationObserver(mirror).observe(document.documentElement,{attributes:true,attributeFilter:['dir']}); }catch(e){}\n"
    "  mirror();\n"
    "})();\n</script>\n<script src=\"eh-ar-dashboard.js\" defer></script>",
    'rtl', 'horizontal bar charts mirror in Arabic; minus signs stay in front of negative axis figures')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['fisc'])
write_change_table(os.path.join(HERE, 'change_table_design_fisc'), 'Design system v2 — Saudi Government Finances')
print('patched: hub/saudi_fiscal_monitor_2026.html')
