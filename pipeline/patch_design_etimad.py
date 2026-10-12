"""patch_design_etimad.py — EH design system v2 for the Government Tenders (Etimad) page (generated), 12 Oct 2026.

The page is generated at publish time by pipeline/build_etimad_page.py (see .github/workflows/update-dashboard.yml)
and is never committed, because it carries the Etimad data. So the design goes into the generator only:
    python3 pipeline/patch_design_etimad.py
The next publish builds the page with it.

What it changes (exact-string edits; stops if an anchor is missing):
  • a page skin after the page's own styles and the Analyst view styles (eh-shared.css is still linked first, so
    every token resolves): mist page, white panels with hairlines, no coloured top edges on the KPI tiles and no
    green bars before headings, the two KPI group labels in sentence case (they were in capitals), numbers in the
    display font with tabular figures, and the page's own colour variables mapped to the shared tokens so light and
    dark come from one place
  • status shown as a word plus a shape in the shared status colours: EH status (Won ●, Lost ◆, Bid submitted ○,
    Studied ■, Not studied —) and fit for EH (Core service, Related, Not for EH)
  • charts: Core service / still open in EH blue, Related / closed in leaf green (the brand land → sea pair), grid
    lines and axis text in token colours; the two time charts (by month, per day) now run left to right in Arabic
    too, as time axes do everywhere else in the hub; the horizontal bar charts keep starting from the right, and their
    labels no longer run off the panel in Arabic (the chart inherited right-to-left drawing, which flipped every label)
  • tender titles, buyer names and reference numbers in the brand font (they fell back to Segoe UI / monospace)
  • the standalone header becomes the navy masthead with contour lines and the land-to-sea line; inside the hub it
    becomes a quiet toolbar on the page colour
  • eh-shared.js is now loaded, so the page gets the shared motion (reveal, count-up, first-load rows), the
    readable-size floor and embedded-mode detection like every other page
  • phone: wide tables outside the scrolling lists scroll inside their panel, so the page no longer scrolls sideways
  • PNG export: always light, with the brand fonts embedded

The Analyst view keeps its ids and classes (#av, #av-flow, .avn). No visible words, numbers, links or features change.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

G = os.path.join(HERE, 'build_etimad_page.py')
if 'eh-skin' in open(G, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(G, 'gen')

SKIN = r'''
/* EH design system v2 — Government Tenders skin (patch_design_etimad.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);
  --green:var(--eh-leaf-ink);--blue:var(--eh-sea);--amber:var(--eh-warn);--red:var(--eh-bad);
  --core:var(--eh-c1);--adj:var(--eh-c2);--bar:var(--eh-c1);--bar2:var(--eh-c2);--grid:var(--eh-line);
  background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead (standalone): deep navy, contour lines, land-to-sea line along the lower edge */
header,body.dark header{background:var(--eh-deep);position:relative;isolation:isolate;padding:20px 22px 22px;gap:12px 16px}
body.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
header>div:first-child{min-width:0;flex:1 1 320px}
header h1{font:600 23px/1.25 var(--eh-display);letter-spacing:-.005em}
header .sub{font-size:13.5px;opacity:.8;margin-top:4px;line-height:1.5}
.tog{border-color:rgba(255,255,255,.32);border-radius:var(--eh-r-ctl)}
.tog button{font:600 12.5px var(--eh-font);color:rgba(255,255,255,.85);padding:7px 13px}
.tog button.on{background:#fff;color:var(--eh-deep)}
/* inside the hub the masthead belongs to the hub: this header becomes a quiet toolbar on the page colour */
html.eh-embedded header,body.embedded header,html.eh-embedded body.dark header,body.embedded.dark header{background:transparent;color:var(--eh-ink);padding:16px 22px 4px}
html.eh-embedded header::after,body.embedded header::after,html.eh-embedded header>.eh-contour,body.embedded header>.eh-contour{display:none}
html.eh-embedded header h1,body.embedded header h1{font-size:21px}
html.eh-embedded header .sub,body.embedded header .sub{color:var(--eh-ink-2);opacity:1}
main{padding:18px 22px 44px}
/* source line, notes, glossary */
.stamp{font-size:13px;color:var(--eh-ink-2);gap:8px 14px}
.stamp .cap,#av .stamp-rv{font:600 12.5px var(--eh-font);color:var(--eh-ink);background:var(--eh-tint);border:0;border-radius:var(--eh-r-chip);padding:3px 11px}
.stamp .cap.stale,body.dark .stamp .cap.stale,#av .stamp-rv.stale,body.dark #av .stamp-rv.stale{background:var(--eh-warn-bg);color:var(--eh-warn);border:0}
.gapnote,#av .warnline{font-size:13px;color:var(--eh-ink);background:var(--eh-warn-bg);border:0;border-inline-start:3px solid #C98A1B;border-radius:9px;padding:10px 14px}
.gloss{font-size:13px;background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:10px 14px;box-shadow:var(--eh-shadow)}
.gloss summary{font-weight:600;color:var(--eh-ink)}.glist li{color:var(--eh-ink-2)}.glist b{color:var(--eh-ink);font-weight:600}
/* KPI tiles: no coloured edges; numbers lead; group labels in sentence case */
.klab{font:600 13.5px var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2);margin:4px 0 8px}
.kstrip{gap:12px;margin-bottom:18px}
.kc,body.dark .kc,.kc.warn,.kc.blue,.kc.mkt{background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
.kc.mkt{background:var(--eh-tint);box-shadow:none;border-color:transparent}
.kc .v{font:600 26px/1.12 var(--eh-display);color:var(--eh-ink)}
.kc .l{font-size:13px;color:var(--eh-ink-2);margin-top:7px;line-height:1.45}
/* filter bar: sits on the page colour */
.filters{background:var(--eh-mist);border-bottom:1px solid var(--eh-line);gap:8px;padding:10px 0 12px}
.filters select,.filters input,body.dark .filters select,body.dark .filters input{font:13px var(--eh-font);color:var(--eh-ink);background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);padding:6px 9px}
.filters input[type=checkbox]{accent-color:var(--eh-sea);padding:0}
.filters label{font-size:13px;color:var(--eh-ink-2)}
.filters .reset{font:600 13px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl);padding:6px 12px}
.filters .reset:hover{background:var(--eh-info-bg)}
.filters .cnt{font-size:13px;color:var(--eh-ink-2);font-variant-numeric:tabular-nums}
/* panels and headings */
.card,body.dark .card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;margin-bottom:16px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.card h2{font:600 21px/1.3 var(--eh-display);color:var(--eh-ink);gap:8px}
.card h2::before{display:none}
.card .note,#av .lede{font-size:13.5px;color:var(--eh-ink-2);line-height:1.6;margin-bottom:12px;max-width:110ch}
.card .hd>b,.card .g2 b:not(table b){font:600 15px/1.4 var(--eh-display);color:var(--eh-ink)}
.hd{gap:10px 14px;margin-bottom:4px}
/* grid columns may shrink below their widest table (the table then scrolls inside, the page does not) */
.g2>*,.g3>*{min-width:0}
/* tables */
.tw{border:1px solid var(--eh-line);border-radius:11px}
table.t{font-size:13px;font-variant-numeric:tabular-nums}
table.t th{font:600 12.5px var(--eh-font);letter-spacing:0;text-transform:none;color:var(--eh-ink-2);background:var(--eh-tint);padding:8px 9px;border-bottom:1px solid var(--eh-line)}
table.t th:hover{color:var(--eh-ink)}
table.t td{padding:8px 9px;border-bottom-color:var(--eh-line)}
table.t tbody tr:hover td{background:var(--eh-tint)}
.ar,.ref{font-family:var(--eh-font)}
.ref{font-size:12.5px;font-variant-numeric:tabular-nums;unicode-bidi:isolate;direction:ltr}
.copy{font:600 12px var(--eh-font);color:var(--eh-sea);border-color:var(--eh-line);border-radius:6px;padding:0 6px}
/* fit for EH: a word plus a shape */
.tag{display:inline-flex;align-items:center;gap:5px;font:600 12px/1.5 var(--eh-font);border-radius:var(--eh-r-chip);padding:1px 9px 1px 8px}
.tag::before{content:"";width:7px;height:7px;flex:none;background:currentColor;border-radius:50%}
.tag.Core{background:var(--eh-info-bg);color:var(--eh-info)}
.tag.Adjacent{background:var(--eh-good-bg);color:var(--eh-good)}.tag.Adjacent::before{background:none;border:1.5px solid currentColor}
.tag.NotEH{background:var(--eh-muted-bg);color:var(--eh-muted);border:0}.tag.NotEH::before{height:2px;border-radius:0}
/* EH status: a word plus a shape */
.st,body.dark .st{display:inline-flex;align-items:center;gap:5px;font:600 12px/1.5 var(--eh-font);border:0;border-radius:var(--eh-r-chip);padding:1px 9px 1px 8px;background:var(--eh-muted-bg);color:var(--eh-muted)}
.st::before{content:"";width:7px;height:7px;flex:none;background:currentColor;border-radius:1px}
.st.Won,body.dark .st.Won{background:var(--eh-good-bg);color:var(--eh-good)}.st.Won::before{border-radius:50%}
.st.Lost,body.dark .st.Lost{background:var(--eh-bad-bg);color:var(--eh-bad)}.st.Lost::before{transform:rotate(45deg);width:6px;height:6px}
.st.Bid,body.dark .st.Bid{background:var(--eh-info-bg);color:var(--eh-info)}.st.Bid::before{background:none;border:1.5px solid currentColor;border-radius:50%}
.st.Studied{background:var(--eh-tint);color:var(--eh-ink)}
.st.Notstudied{background:transparent;color:var(--eh-ink-2);box-shadow:inset 0 0 0 1px var(--eh-line)}.st.Notstudied::before{height:2px;border-radius:0}
#newiss .st::before{display:none}
.pri{color:#C98A1B}
.days.soon{color:var(--eh-bad)}.days.mid{color:var(--eh-warn)}.days.closed{color:var(--eh-ink-3)}
.arrow.up{color:var(--eh-good)}.arrow.down{color:var(--eh-bad)}.arrow.flat{color:var(--eh-ink-3)}
.empty,#av .empty{font-size:13px;color:var(--eh-ink-2);background:var(--eh-tint);border:1px dashed var(--eh-line);border-radius:9px;padding:12px 14px}
/* charts */
svg.ch text{font-family:var(--eh-font);fill:var(--eh-ink-3);font-size:11.5px}
svg.ch .lbl{fill:var(--eh-ink);font-family:var(--eh-display);font-weight:600}
svg.ch .grid{stroke:var(--eh-line)}
/* the charts place every label in page coordinates (they mirror themselves in Arabic), so the drawing direction is
   always left to right; without this the horizontal bar labels ran off the panel in Arabic */
svg.ch{direction:ltr}
.legend{font-size:12.5px;color:var(--eh-ink-2);gap:16px}.legend i{border-radius:50%}
.lgd{font-size:12.5px !important;color:var(--eh-ink-2) !important}
.png,body.dark .png{font:600 12px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl);padding:6px 11px}
.png:hover{background:var(--eh-info-bg)}
#tip{background:var(--eh-paper);color:var(--eh-ink);border:1px solid var(--eh-line);border-radius:10px;box-shadow:var(--eh-shadow);font-size:12.5px;line-height:1.5;padding:8px 11px}
.nts li{font-size:13.5px;line-height:1.6;color:var(--eh-ink)}
.foot{font-size:12px;color:var(--eh-ink-3);line-height:1.65;max-width:130ch;margin:24px auto 0}
/* Analyst view (ids and classes kept: #av, #av-flow, .avn) */
#av h3{font:600 17px/1.35 var(--eh-display);color:var(--eh-ink);margin:26px 0 6px}
#av h3 .n{background:var(--eh-deep);color:#fff;font:600 12px var(--eh-display)}
body.dark #av h3 .n{background:var(--eh-sea);color:#0D1736}
#av .brief{background:var(--eh-tint);border:0;border-inline-start:3px solid var(--eh-sea);border-radius:9px;padding:13px 16px}
#av .brief b.t{font:600 14px var(--eh-display);color:var(--eh-ink)}#av .brief li{font-size:13.5px}
#av .howto{font-size:12.5px;color:var(--eh-ink-2)}
#av .gcard{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:14px 16px}
#av .gcard .gt{font:600 15px var(--eh-display);color:var(--eh-ink)}#av .gcard ul,#av .gcard .row{font-size:13px}
#av .avn{border-inline-start:3px solid var(--eh-sea);padding-inline-start:14px}
#av .avn .h{font:600 14.5px var(--eh-display);color:var(--eh-ink)}#av .avn .f,#av .avn .m,#av .avn .x{font-size:13px}
#av .avn .s,#av .src{font-size:12px;color:var(--eh-ink-3)}
#av .chipr{background:var(--eh-tint);border:0;border-radius:var(--eh-r-chip);font-size:12px;padding:1px 9px}
#av .pst{font-size:12px;background:var(--eh-paper);border:1px solid var(--eh-line);border-inline-start-width:3px;border-radius:7px}
#av .pst.good{border-inline-start-color:var(--eh-good)}#av .pst.warn{border-inline-start-color:#C98A1B}#av .pst.bad{border-inline-start-color:var(--eh-bad)}
#av .sig.up{color:var(--eh-good)}#av .sig.down{color:var(--eh-bad)}#av .sig.mix{color:var(--eh-ink-3)}
#av .flag{color:var(--eh-warn)}
#av table.av2 tr.clash td{background:var(--eh-warn-bg)}
#av details.more summary{color:var(--eh-sea)}
#av-flow svg text{fill:var(--eh-ink-2)}
/* Arabic */
html[dir=rtl] .kc,html[dir=rtl] .card{text-align:start}
html[dir=rtl] .card h2,html[dir=rtl] #av h3{line-height:1.55}
/* phone: wide tables outside the scrolling lists scroll inside their panel, never the page */
@media(max-width:760px){
  header{padding:16px 16px 18px}header h1{font-size:19px}
  main{padding:14px 12px 36px}
  .card{padding:15px 14px}.card h2{font-size:18px}
  .kc .v{font-size:22px}
  div:not(.tw)>table.t{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .filters{position:static}
  .filters select,.filters input[type=search]{max-width:100%;flex:1 1 150px}
}
'''

# ---------------- page skin, after the page and Analyst view styles (eh-shared.css stays linked first)
rep('gen', 'CSS = r"""\n:root{--bg:#F4F7F5;',
    '# EH design system v2 (patch_design_etimad.py): page skin, placed after the page CSS so it wins\nSKIN = r"""' + SKIN + '"""\n\nCSS = r"""\n:root{--bg:#F4F7F5;',
    'design', 'page skin (land and sea): tokens, panels, status as word + shape, sentence-case labels')
rep('gen', '<style>{CSS}{AV.CSS}</style></head>',
    '<style>{CSS}{AV.CSS}</style><style id="eh-skin">{SKIN}</style></head>',
    'design', 'skin linked after the page styles')
rep('gen', '<header><div><h1 data-en="Government Tenders (Etimad)"',
    '<header data-eh-contour="7"><div><h1 data-en="Government Tenders (Etimad)"',
    'design', 'standalone masthead contour lines')
rep('gen', '<script>{JS}{AV.JS}</script>\n</body></html>',
    '<script>{JS}{AV.JS}</script>\n<script src="eh-shared.js" defer></script>\n</body></html>',
    'motion', 'shared behaviour layer: motion, text floor, embedded-mode detection')

# ---------------- time axes run left to right in both languages
rep('gen', "const ord=LANG==='ar'?cats.length-1-i:i,x=gx(ord)-bw/2;",
    "const ord=i,x=gx(ord)-bw/2;   // EH design v2: time runs left to right in Arabic too",
    'rtl', 'time charts keep a left-to-right time axis in Arabic')

# ---------------- PNG export: always light, brand fonts embedded
rep('gen', "function exportPNG(id,name){const svg=$(id).querySelector('svg');if(!svg)return;const cs=getComputedStyle(document.body);",
    "// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)\n"
    "let EXFONTS=null;\n"
    "function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);\n"
    " const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'],['EH Display','vendor/fonts/montserrat-latin-var.woff2','100 900'],['EH Display','vendor/fonts/alexandria-arabic-var.woff2','100 900']];\n"
    " return Promise.all(F.map(f=>fetch(f[1]).then(r=>r.ok?r.blob():null).then(b=>b?new Promise(res=>{const fr=new FileReader();fr.onload=()=>res(`@font-face{font-family:'${f[0]}';src:url(${fr.result}) format('woff2');font-weight:${f[2]}}`);fr.readAsDataURL(b);}):'').catch(()=>''))).then(a=>EXFONTS=a.join(''));}\n"
    "function exportPNG(id,name){ exFonts().then(()=>exportPNG2(id,name)); }\n"
    "function exportPNG2(id,name){const svg=$(id).querySelector('svg');if(!svg)return;\n"
    "  // colours as the light theme draws them, so the PNG is ink on white in either theme\n"
    "  const dk=document.body.classList.contains('dark');if(dk)document.body.classList.remove('dark');const lv={},bs=getComputedStyle(document.body);\n"
    "  ['--core','--adj','--bar','--bar2','--grid','--muted','--ink','--card'].forEach(v=>lv[v]=bs.getPropertyValue(v).trim());if(dk)document.body.classList.add('dark');\n"
    "  const cs={getPropertyValue:v=>lv[v]||''};",
    'design', 'PNG export: light colours, waits for the embedded brand fonts')
rep('gen', "src=src.replace('<svg ','<svg style=\"font-family:Segoe UI,Tahoma,Arial,sans-serif\" ')",
    "src=src.replace('<svg ','<svg style=\"font-family:EH Sans,Segoe UI,Tahoma,Arial,sans-serif\" ').replace(/(<svg[^>]*>)/,m=>m+'<style>'+(EXFONTS||'')+'</style>')",
    'design', 'PNG export in the brand font')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(G, 'w', encoding='utf-8').write(FILES['gen'])
write_change_table(os.path.join(HERE, 'change_table_design_etimad'), 'Design system v2 — Government Tenders (Etimad) page (generator)')
print('patched: build_etimad_page.py (the page is built at publish time)')
