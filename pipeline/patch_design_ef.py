"""patch_design_ef.py — EH design system v2 for the Environment Fund 2025 page (generated), 12 Oct 2026.

The page hub/environment_fund_2025.html is written by pipeline/build_ef_page.py from ef_report_2025.json, so the
design goes into the generator, never the published HTML. After patching, re-run the generator:
    python3 pipeline/patch_design_ef.py
    python3 pipeline/build_ef_page.py

What it changes (exact-string edits; stops if an anchor is missing):
  • a page skin after the page's own styles (it must come after them to win; eh-shared.css is still linked first,
    so every token resolves): mist page, white panels with hairlines, no coloured top edges on the KPI tiles and
    no green bars before headings, labels in sentence case (table headings were in capitals), numbers in the
    display font with tabular figures, status chips that carry a word and a shape (Now / 2026 / 2027+, Add /
    Update / Identify) in the shared status colours, and the page's own colour variables mapped to the shared
    tokens so the dark theme comes from one place
  • the standalone header becomes the navy masthead with contour lines and the land-to-sea line; inside the hub it
    becomes a quiet toolbar on the page colour
  • phone: wide tables scroll inside their panel, so the page itself no longer scrolls sideways at 390px
  • charts: series colours from the brand palette (land → sea), text in token colours (readable in both themes
    without a redraw), one label column wide enough for the longest label (no clipped labels); in Arabic every
    chart and the programme map are mirrored, so labels sit on the right and bars grow leftwards
  • programme map: boxes in the brand palette, label colour chosen for contrast on each box
  • PNG export: always light, with the brand fonts embedded
  • the opportunity tabs slide the new list in (EH_SHARED.viewIn), like every other in-page tab

No visible words, numbers, links or features change.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

G = os.path.join(HERE, 'build_ef_page.py')
if 'eh-skin' in open(G, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(G, 'gen')

SKIN = r'''
/* EH design system v2 — Environment Fund skin (patch_design_ef.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);
  --green:var(--eh-leaf-ink);--blue:var(--eh-sea);--amber:var(--eh-warn);--red:var(--eh-bad);--efblue:var(--eh-sea);
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
html.eh-embedded header,html.eh-embedded body.dark header{background:transparent;color:var(--eh-ink);padding:16px 22px 4px}
html.eh-embedded header::after,html.eh-embedded header>.eh-contour{display:none}
html.eh-embedded header h1{font-size:21px}
html.eh-embedded header .sub{color:var(--eh-ink-2);opacity:1}
html.eh-embedded .tog{border-color:var(--eh-line);background:var(--eh-paper)}
html.eh-embedded .tog button{color:var(--eh-ink-2)}
html.eh-embedded .tog button.on{background:var(--eh-sea);color:#fff}
html.eh-embedded body.dark .tog button.on{color:#0D1736}
main{padding:18px 22px 44px}
/* source line and names */
.stamp{font-size:12.5px;color:var(--eh-ink-3);gap:6px 10px}.stamp b{color:var(--eh-ink);font-weight:600}
#names{font-size:12.5px !important;color:var(--eh-ink-2);line-height:1.6;max-width:150ch}#names b{color:var(--eh-ink);font-weight:600}
/* KPI tiles: no coloured edges; numbers lead */
.kstrip{gap:12px;margin-bottom:18px}
.kc,body.dark .kc{background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
.kc .v{font:600 26px/1.12 var(--eh-display);color:var(--eh-ink);unicode-bidi:isolate}
html[dir=rtl] .kc .v{text-align:right}
.kc .l{font-size:13px;color:var(--eh-ink-2);margin-top:7px;line-height:1.45}
/* page references */
.pg{font:600 12px/1.5 var(--eh-font);color:var(--eh-ink-3);background:var(--eh-tint);border:0;border-radius:var(--eh-r-chip);padding:0 7px;unicode-bidi:isolate;font-variant-numeric:tabular-nums}
/* panels and headings */
.card,body.dark .card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;margin-bottom:16px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.card h2{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);gap:8px}
.card h2::before{display:none}
#charts>.card:first-child h2{font-size:21px}
.card .note{font-size:13px;color:var(--eh-ink-2);line-height:1.55;margin:4px 0 12px}
.hd{gap:10px 14px}
/* grid columns may shrink below their widest table (the table then scrolls inside, the page does not) */
.g2>*,.g3>*{min-width:0}
/* opportunity tabs */
.tabs{gap:8px;margin:10px 0 14px}
.tabs button{font:600 13px var(--eh-font);background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink-2);border-radius:var(--eh-r-chip);padding:7px 14px}
.tabs button:hover{border-color:var(--eh-sea);color:var(--eh-ink)}
.tabs button.on,body.dark .tabs button.on{background:var(--eh-sea);border-color:var(--eh-sea);color:#fff}
body.dark .tabs button.on{color:#0D1736}
/* opportunities: when (a word plus a shape), who, page */
.opp{gap:10px 16px;padding:14px 0;border-top-color:var(--eh-line)}
.chips{gap:5px;min-width:104px}
.chip{display:inline-flex;align-items:center;justify-content:center;gap:5px;font:600 12px/1.5 var(--eh-font);border-radius:var(--eh-r-chip);padding:1px 9px;background:var(--eh-muted-bg);color:var(--eh-muted)}
.chip::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.chip.h-Now{background:var(--eh-bad-bg);color:var(--eh-bad)}.chip.h-Now::before{transform:rotate(45deg);width:6px;height:6px}
.chip.h-2026{background:var(--eh-warn-bg);color:var(--eh-warn)}.chip.h-2026::before{border-radius:1px}
.chip.h-2027\+{background:var(--eh-info-bg);color:var(--eh-info)}.chip.h-2027\+::before{background:none;border:1.5px solid currentColor;border-radius:50%}
.chip.o{background:var(--eh-tint);color:var(--eh-ink-2);border:0;font-weight:500}.chip.o::before{display:none}
.chips .pg{align-self:center}
.opp .st{font-size:14px;line-height:1.6;color:var(--eh-ink)}
.opp .ac{font-size:13px;color:var(--eh-ink);background:var(--eh-tint);border-radius:9px;border-inline-start:3px solid var(--eh-leaf);padding:9px 12px;margin-top:8px}
.opp .ac b{color:var(--eh-leaf-ink);font-weight:600}
/* tables */
table.t{font-size:13px;font-variant-numeric:tabular-nums}
table.t th{font:600 12.5px var(--eh-font);text-transform:none;letter-spacing:0;color:var(--eh-ink-2);background:var(--eh-tint);padding:8px 9px;border-bottom:1px solid var(--eh-line)}
table.t td{padding:8px 9px;border-bottom-color:var(--eh-line)}
table.t tbody tr:hover td{background:var(--eh-tint)}
table.t td [style*="color:var(--muted)"],table.t td[style*="color:var(--muted)"]{color:var(--eh-ink-2) !important}
.xr .zero{color:var(--eh-bad);font-weight:700}
.tag{display:inline-flex;align-items:center;gap:5px;font:600 12px/1.5 var(--eh-font);border-radius:var(--eh-r-chip);padding:1px 9px 1px 8px}
.tag::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
.tag.add{background:var(--eh-good-bg);color:var(--eh-good)}.tag.add::before{border-radius:50%}
.tag.update{background:var(--eh-info-bg);color:var(--eh-info)}.tag.update::before{background:none;border:1.5px solid currentColor;border-radius:50%}
.tag.identify{background:var(--eh-warn-bg);color:var(--eh-warn)}.tag.identify::before{border-radius:1px}
.read{font-size:13.5px;line-height:1.6;background:var(--eh-warn-bg);color:var(--eh-ink);border-radius:9px;border-inline-start:3px solid var(--eh-amber);padding:11px 14px;margin-top:12px}
/* what we don't know */
.gap{font-size:13.5px;padding:10px 0;border-top-color:var(--eh-line)}.gap .how{font-size:13px;color:var(--eh-ink-2)}
details#facts>summary{font:600 16px var(--eh-display);color:var(--eh-ink)}
/* export buttons */
.png,body.dark .png{font:600 12px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl);padding:6px 11px}
.png:hover{background:var(--eh-info-bg)}
/* charts: brand fonts; titles in the display face */
svg.pm text{font-family:var(--eh-font)}
svg.pm text[font-weight="800"]{font-family:var(--eh-display);font-weight:600}
.foot{font-size:12px;color:var(--eh-ink-3);line-height:1.65;max-width:130ch;margin:24px auto 0}
/* Arabic */
html[dir=rtl] .kc,html[dir=rtl] .card{text-align:start}
html[dir=rtl] .card h2{line-height:1.55}
/* phone: wide tables scroll inside their panel, never the page */
@media(max-width:760px){
  header{padding:16px 16px 18px}header h1{font-size:19px}
  main{padding:14px 12px 36px}
  .card{padding:15px 14px}
  .kc .v{font-size:22px}
  table.t{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .gap{grid-template-columns:1fr}.gap .how{max-width:none;text-align:start}
  .opp{grid-template-columns:1fr}.chips{flex-direction:row;flex-wrap:wrap;min-width:0}
}
'''

# ---------------- page skin, after the page's own styles (eh-shared.css stays linked first so tokens resolve)
rep('gen', '"""\n\nJS = r"""\n',
    '"""\n\n# EH design system v2 (patch_design_ef.py): page skin, placed after the page CSS so it wins\nSKIN = r"""' + SKIN + '"""\n\nJS = r"""\n',
    'design', 'page skin (land and sea): tokens, panels, chips with word + shape, sentence-case labels')
rep('gen', '<link rel="stylesheet" href="eh-shared.css">\n<style>{CSS}</style>\n',
    '<link rel="stylesheet" href="eh-shared.css">\n<style>{CSS}</style>\n<style id="eh-skin">{SKIN}</style>\n',
    'design', 'skin linked after the page styles')
rep('gen', '<header>\n <div><h1 id="title"></h1>',
    '<header data-eh-contour="7">\n <div><h1 id="title"></h1>',
    'design', 'standalone masthead contour lines')

# ---------------- charts: brand palette, token text colours, shared label column, Arabic mirroring
rep('gen', " const W=1100, rowH=34, L0=430, iw=W-L0-190, ink=DARK?'#E6EDF1':'#16333F', mut='#6B7C86';\n",
    " const W=1100, rowH=34, L0=EF_L0(), iw=W-L0-190, ink='var(--eh-ink)', mut='var(--eh-ink-3)';   // EH design v2: token colours follow the theme\n"
    " c=Object.assign({},c,{color:BC(c.color),colors:(c.colors||[]).map(BC),rows:c.rows.map(r=>r.c?Object.assign({},r,{c:BC(r.c)}):r)});\n",
    'design', 'chart text in token colours, series in the brand palette, label column fits the longest label')
rep('gen', "<tspan fill=\"${better?'#1F7A4C':'#C0504D'}\">",
    "<tspan fill=\"${better?'var(--eh-good)':'var(--eh-bad)'}\">",
    'design', 'better / worse marks in the shared status colours')
rep('gen', "function chart(c){\n",
    "// EH design system v2 (patch_design_ef.py): brand palette (land → sea) for the colours stored in the report data\n"
    "const BCM={'#2A3F80':'#3B57B8','#E8862E':'#C98A1B','#1F7A4C':'#54AB5D','#C0504D':'#B23F2B','#1A5FAB':'#0072BB','#2E9E8E':'#00A0E0','#5F7078':'#5E6B80','#7B4FA6':'#8E6BB8','#9AABB5':'#9DABC5'};\n"
    "const BC=x=>BCM[String(x||'').toUpperCase()]||x;\n"
    "// one label column for every chart, wide enough for the longest label in the current language\n"
    "function EF_L0(){let n=0;EF.charts.forEach(c=>c.rows.forEach(r=>{n=Math.max(n,String(L(r.en,r.ar)).length)}));return Math.round(Math.min(560,Math.max(330,n*6.3+26)));}\n"
    "// Arabic: mirror a drawn chart so labels sit on the right and bars grow leftwards (text is never flipped)\n"
    "function mir(h){if(LANG!=='ar')return h;const t=document.createElement('template');t.innerHTML=h;\n"
    " t.content.querySelectorAll('svg').forEach(svg=>{const W=+(svg.getAttribute('viewBox')||'0 0 0 0').split(/\\s+/)[2]||0,num=(e,a)=>+(e.getAttribute(a)||0);\n"
    "  svg.querySelectorAll('rect').forEach(e=>e.setAttribute('x',(W-num(e,'x')-num(e,'width')).toFixed(1)));\n"
    "  svg.style.direction='rtl';   // text keeps its logical anchor: in right-to-left, start is the right edge\n"
    "  svg.querySelectorAll('text').forEach(e=>{e.setAttribute('x',(W-num(e,'x')).toFixed(1));\n"
    "   if(!/[\\u0600-\\u06FF]/.test(e.textContent)){e.style.direction='ltr';const a=e.getAttribute('text-anchor')||'start';if(a!=='middle')e.setAttribute('text-anchor',a==='end'?'start':'end');}});   // figures and units read left to right\n"
    "  svg.querySelectorAll('line').forEach(e=>{e.setAttribute('x1',W-num(e,'x1'));e.setAttribute('x2',W-num(e,'x2'));});\n"
    "  svg.querySelectorAll('path').forEach(e=>e.setAttribute('d',e.getAttribute('d').replace(/(-?\\d+(?:\\.\\d+)?)\\s+(-?\\d+(?:\\.\\d+)?)/g,(m,x,y)=>(W-x)+' '+y)));});\n"
    " return t.innerHTML;}\n"
    "// programme-map labels: white or navy, whichever reads better on the box colour\n"
    "function onFill(hx){const v=[1,3,5].map(i=>{const c=parseInt(hx.substr(i,2),16)/255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)}),l=0.2126*v[0]+0.7152*v[1]+0.0722*v[2];return (1.05/(l+0.05))>=((l+0.05)/0.0686)?'#fff':'#15224D';}\n"
    "function chart(c){\n",
    'rtl', 'helpers: palette map, shared label column, Arabic mirroring, label contrast')
rep('gen', "${chart(c)}</div>`).join('');",
    "${mir(chart(c))}</div>`).join('');",
    'rtl', 'charts mirrored in Arabic')
rep('gen', " $('pmwrap').innerHTML=programmeMap();",
    " $('pmwrap').innerHTML=mir(programmeMap());",
    'rtl', 'programme map mirrored in Arabic (reads right to left, like its Arabic title)')
rep('gen', " const col={grants:'#1F7A4C',loansup:'#2A3F80',guar:'#1A5FAB',impact:'#7B4FA6',ppp:'#E8862E',fees:'#C0504D',shared:'#5F7078',carbon:'#2E9E8E'};",
    " const col={grants:'#2E7A37',loansup:'#3B57B8',guar:'#0072BB',impact:'#8E6BB8',ppp:'#C98A1B',fees:'#B23F2B',shared:'#5E6B80',carbon:'#00A0E0'};   // EH brand palette",
    'design', 'programme map in the brand palette')
rep('gen', "<text x=\"${xP}\" y=\"24\" font-size=\"15\" font-weight=\"800\" fill=\"${DARK?'#E6EDF1':'#16333F'}\">",
    "<text x=\"${xP}\" y=\"24\" font-size=\"15\" font-weight=\"800\" fill=\"var(--eh-ink)\">",
    'design', 'programme map title in the token ink')
rep('gen', "<text x=\"${xP}\" y=\"42\" font-size=\"11\" fill=\"#6B7C86\">",
    "<text x=\"${xP}\" y=\"42\" font-size=\"11\" fill=\"var(--eh-ink-3)\">",
    'design', 'programme map source line in the token footnote colour')
rep('gen', "font-size=\"12.5\" font-weight=\"700\" fill=\"#fff\">${esc(L(p.en,p.ar))}</text><text x=\"${xP+bw[0]-8}\" y=\"${yP(i)+19}\" font-size=\"10\" fill=\"#fff\"",
    "font-size=\"12.5\" font-weight=\"700\" fill=\"${onFill(col[p.id])}\">${esc(L(p.en,p.ar))}</text><text x=\"${xP+bw[0]-8}\" y=\"${yP(i)+19}\" font-size=\"10.5\" fill=\"${onFill(col[p.id])}\"",
    'design', 'programme labels readable on every box colour')
rep('gen', "fill=\"${DARK?'#1E2830':'#F0F5F2'}\" stroke=\"${DARK?'#3A4B55':'#DCE8DF'}\"/><text x=\"${xC+bw[1]/2}\" y=\"${yC(i)+18}\" font-size=\"12\" font-weight=\"700\" fill=\"${DARK?'#E6EDF1':'#16333F'}\"",
    "fill=\"var(--eh-tint)\" stroke=\"var(--eh-line)\"/><text x=\"${xC+bw[1]/2}\" y=\"${yC(i)+18}\" font-size=\"12\" font-weight=\"700\" fill=\"var(--eh-ink)\"",
    'design', 'centre boxes in token colours')
rep('gen', "fill=\"${DARK?'#1E2830':'#fff'}\" stroke=\"#1F7A4C\" stroke-width=\"1.5\"/><text x=\"${xE+10}\" y=\"${yE(i)+18}\" font-size=\"12.5\" font-weight=\"700\" fill=\"${DARK?'#E6EDF1':'#1F7A4C'}\">",
    "fill=\"var(--eh-paper)\" stroke=\"var(--eh-leaf-ink)\" stroke-width=\"1.5\"/><text x=\"${xE+10}\" y=\"${yE(i)+18}\" font-size=\"12.5\" font-weight=\"700\" fill=\"var(--eh-leaf-ink)\">",
    'design', 'EH service boxes in token colours')

rep('gen', "const xP=40,xC=W/2-40,xE=W-300, bw=[250,120,200];",
    "const xP=40,xC=W/2-40,xE=W-300, bw=[310,150,200];   // EH design v2: programme and centre boxes wide enough for the longest label (English and Arabic) in the brand font",
    'design', 'programme boxes fit their longest label')

# ---------------- PNG export: always light, brand fonts embedded
rep('gen', "function exPNG(id,name){const svg=$(id);if(!svg)return;",
    "// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)\n"
    "let EXFONTS=null;\n"
    "function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);\n"
    " const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'],['EH Display','vendor/fonts/montserrat-latin-var.woff2','100 900'],['EH Display','vendor/fonts/alexandria-arabic-var.woff2','100 900']];\n"
    " return Promise.all(F.map(f=>fetch(f[1]).then(r=>r.ok?r.blob():null).then(b=>b?new Promise(res=>{const fr=new FileReader();fr.onload=()=>res(`@font-face{font-family:'${f[0]}';src:url(${fr.result}) format('woff2');font-weight:${f[2]}}`);fr.readAsDataURL(b);}):'').catch(()=>''))).then(a=>EXFONTS=a.join(''));}\n"
    "function exPNG(id,name){ exFonts().then(()=>exPNG2(id,name)); }\n"
    "function exPNG2(id,name){const svg=$(id);if(!svg)return;",
    'design', 'PNG export waits for the embedded brand fonts')
rep('gen', " cl.querySelectorAll('text').forEach(t=>t.setAttribute('font-family',\"'Segoe UI',Tahoma,Arial,sans-serif\"));\n",
    " // read every colour as the light theme draws it, so the PNG is ink on white in either theme\n"
    " const dk=document.body.classList.contains('dark');if(dk)document.body.classList.remove('dark');\n"
    " const se=[...svg.querySelectorAll('*')],ce=[...cl.querySelectorAll('*')];\n"
    " se.forEach((e,i)=>{const d=ce[i];if(!d||!/^(text|tspan|rect|path|line|circle)$/.test(e.tagName))return;const cs=getComputedStyle(e);d.setAttribute('fill',cs.fill);d.setAttribute('stroke',cs.stroke);\n"
    "  if(e.tagName==='text'){d.setAttribute('font-family',/EH Display/.test(cs.fontFamily)?\"'EH Display','Segoe UI',Tahoma,Arial,sans-serif\":\"'EH Sans','Segoe UI',Tahoma,Arial,sans-serif\");d.setAttribute('font-weight',cs.fontWeight);}d.removeAttribute('class');d.removeAttribute('style');});\n"
    " if(dk)document.body.classList.add('dark');\n"
    " const fst=document.createElementNS('http://www.w3.org/2000/svg','style');fst.textContent=EXFONTS||'';cl.insertBefore(fst,cl.firstChild);\n",
    'design', 'PNG export: light colours and brand fonts')
rep('gen', "bg.setAttribute('fill',DARK?'#151C21':'#fff');",
    "bg.setAttribute('fill','#fff');",
    'design', 'PNG export background always white')

# ---------------- motion: the opportunity tabs slide the new list in, like every other in-page tab
rep('gen', "onclick=\"GROUP='${k}';render()\"",
    "onclick=\"GROUP='${k}';render();window.EH_SHARED&&EH_SHARED.viewIn($('opps'))\"",
    'motion', 'opportunity tabs use the shared view transition')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(G, 'w', encoding='utf-8').write(FILES['gen'])
write_change_table(os.path.join(HERE, 'change_table_design_ef'), 'Design system v2 — Environment Fund 2025 page (generator)')
print('patched: build_ef_page.py — now run: python3 pipeline/build_ef_page.py')
