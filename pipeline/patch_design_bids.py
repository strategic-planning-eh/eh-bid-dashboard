"""patch_design_bids.py — EH design system v2 for the Bid & Tender app (generated hourly), 12 Oct 2026.

The bid app is rebuilt every hour from pipeline/, so the design goes into the generator, never the published HTML:
  • build_bid_dashboard.py  adds the page skin after eh-shared.css; the standalone header gets the navy masthead
                            with contour lines; inside the hub the header becomes a quiet toolbar on the page colour
  • charts.js               brand chart palette (land → sea), chart text in the brand fonts and a readable size,
                            horizontal bar charts mirror in Arabic (labels on the right, bars grow leftwards)
  • app.js                  outcome colours from the brand status set; chart PNG export embeds the brand fonts and
                            always prints dark ink on white, in either theme

Design rules applied here (from eh-shared.css v2): one quiet surface system (mist page, white panels, hairlines, no
rainbow top borders), labels in sentence case (no capitals), numbers in Montserrat with tabular figures, status
always shown as a word plus a shape, and the inline colours app.js writes mapped to the shared tokens so light and
dark themes both come from one place.

Run once:  python3 pipeline/patch_design_bids.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_change_table

B, CJ, A = (os.path.join(HERE, f) for f in ('build_bid_dashboard.py', 'charts.js', 'app.js'))
if 'eh-skin' in open(B, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(B, 'build'); load(CJ, 'charts'); load(A, 'app')

SKIN = r'''
/* EH design system v2 — Bid & Tender skin (patch_design_bids.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead (standalone) */
header{background:var(--eh-deep);box-shadow:none;position:relative;isolation:isolate;padding:20px 0 22px}
body.dark header{background:#0A1230}
header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
.hd h1{font:600 24px/1.2 var(--eh-display);letter-spacing:-.005em}
.hd h1 b{font-weight:700}
.hd .sub{font-size:13px;opacity:.78}
.hd img{border-radius:11px;box-shadow:0 2px 10px -4px rgba(0,0,0,.4)}
.langtog{border-color:rgba(255,255,255,.32);border-radius:var(--eh-r-ctl)}
.langbtn{font:600 12.5px var(--eh-font);color:rgba(255,255,255,.85)}
.langbtn.on{background:#fff;color:var(--eh-deep)}
.hd .pill{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);border-radius:var(--eh-r-ctl);font-weight:500}
/* inside the hub the masthead belongs to the hub: this header becomes a quiet toolbar on the page colour */
html.inframe header,html.eh-embedded header,html.inframe body.dark header,html.eh-embedded body.dark header{background:transparent;padding:14px 0 6px;color:var(--eh-ink)}
html.inframe header::after,html.eh-embedded header::after,html.inframe header>.eh-contour,html.eh-embedded header>.eh-contour{display:none}
html.inframe .langtog,html.eh-embedded .langtog{border-color:var(--eh-line);background:var(--eh-paper)}
html.inframe .langbtn,html.eh-embedded .langbtn{color:var(--eh-ink-2)}
html.inframe .langbtn.on,html.eh-embedded .langbtn.on{background:var(--eh-sea);color:#fff}
html.inframe .hd .pill,html.eh-embedded .hd .pill{background:var(--eh-paper);border:1px solid var(--eh-line);color:var(--eh-ink-2)}
/* section tabs */
nav,body.dark nav,#nav,body.dark #nav{background:var(--eh-mist);border-bottom:1px solid var(--eh-line);box-shadow:none}
#nav{border-bottom:0}
nav a,#nav a,body.dark #nav a{font:600 13.5px var(--eh-font);color:var(--eh-ink-2);border-bottom:0;padding:13px 15px;box-shadow:inset 0 -3px 0 transparent;transition:color var(--eh-dur-1) var(--eh-ease),box-shadow var(--eh-dur-2) var(--eh-ease)}
nav a:hover{color:var(--eh-ink)}
nav a.on,#nav a.on,body.dark #nav a.on{color:var(--eh-ink);background:none;box-shadow:inset 0 -3px 0 var(--eh-sea);border-color:transparent}
.ntf,.nsub .newb{background:var(--eh-leaf-ink)}
/* headings */
.sech,body.dark .sech{font:600 23px/1.25 var(--eh-display);color:var(--eh-ink);margin:10px 0 6px}
.sech:before{display:none}
.secsub,body.dark .secsub{font-size:14px;color:var(--eh-ink-2);max-width:78ch;line-height:1.6;margin-bottom:18px}
/* KPI tiles: no rainbow edges; numbers lead */
.kstrip{gap:12px}
.kc,body.dark .kc,.kstrip .kc:nth-child(n){background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
.kc .v{font:600 27px/1.08 var(--eh-display);color:var(--eh-ink)}
.kc .v.g{color:var(--eh-good)}.kc .v.r{color:var(--eh-bad)}
.kc .l,body.dark .kc .l{font-size:13px;color:var(--eh-ink-2);text-transform:none;letter-spacing:0;font-weight:500;margin-top:6px;line-height:1.35}
.kc .d,body.dark .kc .d{font-size:12px;color:var(--eh-ink-3);margin-top:4px}
.kc:has(.v.hero){border-top-width:1px}
body.dark .kc *{color:inherit}body.dark .kc .v{color:var(--eh-ink)}body.dark .kc .v.g{color:var(--eh-good)}body.dark .kc .v.r{color:var(--eh-bad)}
/* panels */
.card,body.dark .card,.grid.g2 .card:nth-child(n){background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
.card h3,body.dark .card h3,.grid.g2 .card:nth-child(n) h3{font:600 16px/1.35 var(--eh-display);color:var(--eh-ink);border:0;padding:0;margin-bottom:4px}
.card .note,body.dark .note{font-size:13px;color:var(--eh-ink-2);line-height:1.55}
.metric,body.dark .metric,.metric:nth-child(n){background:var(--eh-tint) !important;border:1px solid transparent !important;border-radius:11px}
.metric .mv,.metric:nth-child(n) .mv,body.dark .mv{font:600 21px var(--eh-display);color:var(--eh-ink) !important}
.metric .ml,body.dark .ml{font-size:12.5px;color:var(--eh-ink-2)}
/* tables */
table.t th,body.dark table th{background:var(--eh-tint);color:var(--eh-ink-2);font-size:12px;text-transform:none;letter-spacing:0;font-weight:600;border-bottom:1px solid var(--eh-line)}
table.t td,body.dark table td{border-bottom:1px solid var(--eh-line);font-size:13px}
table.t tr:hover,body.dark tr:hover td{background:var(--eh-tint)}
/* outcome tags: a word plus a shape, soft fill */
.tag{font:600 11.5px var(--eh-font);border-radius:var(--eh-r-chip);padding:2px 9px 2px 8px;display:inline-flex;align-items:center;gap:5px;text-transform:none}
.tag::before{content:"";width:7px;height:7px;flex:none;background:currentColor;border-radius:50%}
.tag[style*="#2E7A37"]{background:var(--eh-good-bg) !important;color:var(--eh-good) !important}
.tag[style*="#B23F2B"]{background:var(--eh-bad-bg) !important;color:var(--eh-bad) !important}.tag[style*="#B23F2B"]::before{border-radius:1px;transform:rotate(45deg)}
.tag[style*="#C98A1B"]{background:var(--eh-warn-bg) !important;color:var(--eh-warn) !important}.tag[style*="#C98A1B"]::before{border-radius:1px}
.tag[style*="#5E6B80"]{background:var(--eh-muted-bg) !important;color:var(--eh-muted) !important}.tag[style*="#5E6B80"]::before{height:2px;border-radius:0}
.tag[style*="#0072BB"]{background:var(--eh-info-bg) !important;color:var(--eh-info) !important}.tag[style*="#0072BB"]::before{background:none;border:1.5px solid currentColor}
/* watch items, answers, exports */
.wli,body.dark .wli{background:var(--eh-paper);border:1px solid var(--eh-line);border-inline-start-width:3px;border-radius:10px;color:var(--eh-ink)}
.wli.high{border-inline-start-color:var(--eh-bad);background:var(--eh-paper)}.wli.med{border-inline-start-color:var(--eh-warn);background:var(--eh-paper)}.wli.low{border-inline-start-color:var(--eh-leaf);background:var(--eh-paper)}
.wlk{text-transform:none;letter-spacing:0;font-size:11px;border-radius:var(--eh-r-chip)}
.ansbox,body.dark .ansbox{background:var(--eh-tint);border:1px solid var(--eh-line);border-inline-start:3px solid var(--eh-sea);color:var(--eh-ink)}
.anst{color:var(--eh-ink)}.anst-ar,.ansrow{color:var(--eh-ink-2)}
.askbtn{background:var(--eh-paper);border-color:var(--eh-line);color:var(--eh-ink)}.askbtn:hover{border-color:var(--eh-sea);box-shadow:none;transform:none}
.png,body.dark .png{font:600 12px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-sea);border-radius:var(--eh-r-ctl)}
.png:hover{background:var(--eh-info-bg)}
.excov,body.dark .excov{background:var(--eh-tint);border-color:var(--eh-line);border-inline-start-color:var(--eh-sea);color:var(--eh-ink)}
.exT,body.dark .exT{font-family:var(--eh-display);font-weight:600;fill:var(--eh-ink)}.exS,.exq,body.dark .exS,body.dark .exq{font-family:var(--eh-font);fill:var(--eh-ink-3)}
.exfoot{color:var(--eh-ink-2)}.exfoot a,.excov a,.exdec a{color:var(--eh-sea)}
.exw{border-bottom-color:var(--eh-line)}
.foot,body.dark .foot{color:var(--eh-ink-3);border-top-color:var(--eh-line);font-size:12px}
/* chart text */
.cax,.cax2{font-family:var(--eh-font) !important;font-size:11.5px !important;font-weight:500 !important;fill:var(--eh-ink-3)}
.caxt{font-family:var(--eh-font) !important;font-size:12px !important;fill:var(--eh-ink-2)}
.chl{font-family:var(--eh-font) !important;font-size:12.5px !important;font-weight:500 !important;fill:var(--eh-ink-2)}
.chv{font-family:var(--eh-display) !important;font-size:12.5px !important;font-weight:600 !important;fill:var(--eh-ink)}
.chs{font-family:var(--eh-font) !important;font-size:11.5px !important;fill:var(--eh-ink-3)}
.cln{font-family:var(--eh-display) !important;font-size:11px !important}
.lgi,body.dark .lgi{font-size:12.5px;color:var(--eh-ink-2)}.lgi b{color:var(--eh-ink);font-weight:600}
.lgd{border-radius:50%}
body.dark svg text,body.dark svg tspan{fill:var(--eh-ink-2) !important}
/* inputs */
input,select,body.dark input,body.dark select{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;color:var(--eh-ink) !important;border-radius:var(--eh-r-ctl) !important}
/* the colours app.js writes inline, mapped to the shared tokens (one place for light and dark) */
:root body [style*="color:#1A5FAB"]{color:var(--eh-sea) !important}
:root body [style*="color:#1C2B33"],:root body [style*="color:#3A4A52"],:root body [style*="color:#3A4A54"],:root body [style*="color:#44525C"]{color:var(--eh-ink) !important}
:root body [style*="color:#5F7078"],:root body [style*="color:#6B7C86"],:root body [style*="color:#4A5A62"],:root body [style*="color:#5A6B76"],:root body [style*="color:#5A6A72"]{color:var(--eh-ink-2) !important}
:root body [style*="color:#8A99A3"],:root body [style*="color:#77868F"],:root body [style*="color:#7B8A92"],:root body [style*="color:#9AABB5"]{color:var(--eh-ink-3) !important}
:root body [style*="color:#2E7D46"]{color:var(--eh-good) !important}
:root body [style*="color:#C0504D"],:root body [style*="color:#A03A36"],:root body [style*="color:#B23A3A"]{color:var(--eh-bad) !important}
:root body [style*="color:#3E86C8"]{color:var(--eh-info) !important}
:root body [style*="color:#5A4A2E"],:root body [style*="color:#5C4A14"],:root body [style*="color:#8A6D2E"],:root body [style*="color:#8A5A12"],:root body [style*="color:#7A5B14"]{color:var(--eh-warn) !important}
:root body [style*="background:#fff"],:root body [style*="background:#FFF;"],:root body [style*="background: #fff"]{background:var(--eh-paper) !important;color:inherit}
:root body [style*="background:#FFF8EC"],:root body [style*="background:#FFF3DF"],:root body [style*="background:#FFF1C9"]{background:var(--eh-warn-bg) !important;color:var(--eh-ink) !important}
:root body [style*="background:#F4F8F5"],:root body [style*="background:#F7FAFC"],:root body [style*="background:#F5F8FA"],:root body [style*="background:#EEF5FB"],:root body [style*="background:#F2F7FC"]{background:var(--eh-tint) !important}
:root body [style*="border:1px solid #E3EAE5"],:root body [style*="border:1px solid #D5DEE2"],:root body [style*="border:1px solid #CBD6DC"],:root body [style*="border:1px solid #EAD9B0"],:root body [style*="border:1px solid #F0DDB0"]{border-color:var(--eh-line) !important}
:root body [style*="border-left:4px solid #E8862E"]{border-inline-start-color:var(--eh-warn) !important}
/* "Ask the data" */
#ehcbtn{background:var(--eh-deep) !important;box-shadow:0 8px 22px -8px rgba(13,23,54,.6) !important}
.ehch{background:var(--eh-deep) !important}
.ehsend{background:var(--eh-sea) !important}
.ehcb{background:var(--eh-mist) !important}
.ehm{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;color:var(--eh-ink) !important}
.ehu{background:var(--eh-info-bg) !important;border-color:transparent !important;color:var(--eh-ink) !important}
.ehchip{background:var(--eh-paper) !important;border-color:var(--eh-line) !important;color:var(--eh-sea) !important}
.ehcf,#ehcp{background:var(--eh-paper) !important}
/* Arabic: labels sit right, figures stay readable */
html[dir=rtl] .kc,html[dir=rtl] .metric{text-align:start}
html[dir=rtl] .card h3{line-height:1.5}
@media(max-width:768px){.sech{font-size:20px}.kc .v{font-size:23px}}
'''

# ---------------- build_bid_dashboard.py
rep('build', "APP=open('app.js').read()\nHTML=HTML.replace('__APP__', APP)\n",
    "APP=open('app.js').read()\nHTML=HTML.replace('__APP__', APP)\n"
    "# EH design system v2 (patch_design_bids.py): the page skin goes after eh-shared.css so tokens resolve\n"
    "SKIN=r'''" + SKIN + "'''\n"
    "HTML=HTML.replace('<link rel=\"stylesheet\" href=\"eh-shared.css\">','<link rel=\"stylesheet\" href=\"eh-shared.css\"><style id=\"eh-skin\">'+SKIN+'</style>',1)\n",
    'design', 'page skin after the shared design system')
rep('build', '<header><div class="hd"><img src="{LOGO}" alt="EH"><div><h1 id="h-title">Bid &amp; Tender Intelligence</h1>',
    '<header data-eh-contour="7"><div class="hd"><img src="{LOGO}" alt="EH"><div><h1 id="h-title">Bid &amp; Tender Intelligence</h1>',
    'design', 'standalone masthead contour lines')

# ---------------- charts.js
rep('charts', "const C={green:'#3FA34D',blue:'#1A5FAB',ink:'#1C2B33',soft:'#6B7C86',line:'#E3EAE5',mist:'#F4F8F5',\n red:'#C0504D',orange:'#E8862E',teal:'#2A9D8F',purple:'#7B6BA8',gold:'#D4A92E',\n pal:['#1A5FAB','#3FA34D','#E8862E','#7B6BA8','#2A9D8F','#C0504D','#D4A92E','#5A95C8','#8FB339','#B5651D']};",
    "// EH design system v2: land → sea palette from the logo and the EH profile; readable on light and dark panels\n"
    "const C={green:'#54AB5D',blue:'#0072BB',ink:'#15224D',soft:'#5E6B80',line:'#D9E3DF',mist:'#F2F6F4',\n red:'#B23F2B',orange:'#C98A1B',teal:'#00A0E0',purple:'#8E6BB8',gold:'#C98A1B',\n pal:['#0072BB','#54AB5D','#3B57B8','#00A0E0','#C98A1B','#8E6BB8','#A6CE39','#B23F2B','#5E9FD6','#7FB685']};",
    'design', 'brand chart palette')
# horizontal bars mirror in Arabic: labels on the right, bars grow leftwards
rep('charts', "  data.forEach((d,i)=>{const v=o.val(d);const w=Math.max(v/max*iw,1);const y=7+i*o.rh;\n"
              "    s+=`<text x=\"${labw}\" y=\"${y+o.rh/2+1}\" text-anchor=\"end\" class=\"chl\">${esc(String(o.lab(d)).slice(0,o.maxlab))}</text>`;\n"
              "    s+=`<rect x=\"${barx}\" y=\"${y+3}\" width=\"${w.toFixed(1)}\" height=\"${o.rh-9}\" rx=\"2.5\" fill=\"${typeof o.color==='function'?o.color(d):o.color}\"><title>${esc(o.lab(d))}: ${esc(o.fmt(v))}</title></rect>`;\n"
              "    s+=`<text x=\"${barx+w+6}\" y=\"${y+o.rh/2+1}\" class=\"chv\">${esc(o.fmt(v))}${o.sub?'  <tspan class=\"chs\">'+esc(o.sub(d))+'</tspan>':''}</text>`;});",
    "  const RTL=document.documentElement.dir==='rtl', X=x=>RTL?W-x:x, A=a=>RTL?(a==='end'?'start':'end'):a;   // Arabic: mirror the chart\n"
    "  data.forEach((d,i)=>{const v=o.val(d);const w=Math.max(v/max*iw,1);const y=7+i*o.rh;\n"
    "    s+=`<text x=\"${X(labw)}\" y=\"${y+o.rh/2+1}\" text-anchor=\"${A('end')}\" class=\"chl\">${esc(String(o.lab(d)).slice(0,o.maxlab))}</text>`;\n"
    "    s+=`<rect x=\"${(RTL?W-barx-w:barx).toFixed(1)}\" y=\"${y+3}\" width=\"${w.toFixed(1)}\" height=\"${o.rh-9}\" rx=\"2.5\" fill=\"${typeof o.color==='function'?o.color(d):o.color}\"><title>${esc(o.lab(d))}: ${esc(o.fmt(v))}</title></rect>`;\n"
    "    s+=`<text x=\"${X(barx+w+6)}\" y=\"${y+o.rh/2+1}\" text-anchor=\"${A('start')}\" class=\"chv\">${esc(o.fmt(v))}${o.sub?'  <tspan class=\"chs\">'+esc(o.sub(d))+'</tspan>':''}</text>`;});",
    'rtl', 'horizontal bar charts mirror in Arabic')
rep('charts', "style=\"font:800 26px Segoe UI;fill:${C.ink}\">${o.center}</text><text x=\"${cx}\" y=\"${cy+14}\" text-anchor=\"middle\" style=\"font:600 10px Segoe UI;fill:${C.soft};letter-spacing:.5px\">",
    "class=\"eh-dc\" style=\"font-family:var(--eh-display);font-weight:600;font-size:26px;fill:var(--eh-ink)\">${o.center}</text><text x=\"${cx}\" y=\"${cy+15}\" text-anchor=\"middle\" style=\"font-family:var(--eh-font);font-weight:500;font-size:11.5px;fill:var(--eh-ink-3)\">",
    'design', 'donut centre in the brand fonts and token colours')

# ---------------- app.js
rep('app', " const OC={'Won':'#2E7D46','Lost':'#C0504D','Not awarded':'#E8862E','Cancelled':'#5F7078','Pending':'#3E86C8'};",
    " const OC={'Won':'#2E7A37','Lost':'#B23F2B','Not awarded':'#C98A1B','Cancelled':'#5E6B80','Pending':'#0072BB'};   // EH status set (eh-shared.css v2)",
    'design', 'outcome colours from the brand status set')
rep('app', "const EXC={won:'#2E7D46',lost:'#C0504D',pend:'#3E86C8',stale:'#E8862E',grey:'#9AABB5',ink:'#1C2B33'};",
    "const EXC={won:'#2E7A37',lost:'#B23F2B',pend:'#0072BB',stale:'#C98A1B',grey:'#9DABC5',ink:'#15224D'};   // EH status set (eh-shared.css v2)",
    'design', 'executive summary colours from the brand status set')
# PNG export: embed the brand fonts, always dark ink on white
rep('app', " src.forEach((el,i)=>{ if(el.tagName==='text'||el.tagName==='tspan'){const cs=getComputedStyle(el); dst[i].setAttribute('style',`font:${cs.fontWeight} ${cs.fontSize} 'Segoe UI',Tahoma,Arial,sans-serif;fill:${cs.fill}`);} dst[i].removeAttribute('onclick'); });",
    " src.forEach((el,i)=>{ if(el.tagName==='text'||el.tagName==='tspan'){const cs=getComputedStyle(el); const disp=/EH Display/.test(cs.fontFamily); dst[i].setAttribute('style',`font-family:${disp?\"'EH Display'\":\"'EH Sans'\"},'Segoe UI',Tahoma,Arial,sans-serif;font-weight:${cs.fontWeight};font-size:${cs.fontSize};fill:${exInk(cs.fill)}`);} dst[i].removeAttribute('onclick'); });\n"
    " const fst=document.createElementNS('http://www.w3.org/2000/svg','style'); fst.textContent=EXFONTS||''; cl.insertBefore(fst,cl.firstChild);",
    'design', 'chart PNGs carry the brand fonts and stay legible from dark mode')
rep('app', "function exPNG(id,name){\n const svg=document.getElementById(id); if(!svg)return;",
    "// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)\n"
    "let EXFONTS=null;\n"
    "function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);\n"
    " const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'],['EH Display','vendor/fonts/montserrat-latin-var.woff2','100 900'],['EH Display','vendor/fonts/alexandria-arabic-var.woff2','100 900']];\n"
    " return Promise.all(F.map(f=>fetch(f[1]).then(r=>r.ok?r.blob():null).then(b=>b?new Promise(res=>{const fr=new FileReader();fr.onload=()=>res(`@font-face{font-family:'${f[0]}';src:url(${fr.result}) format('woff2');font-weight:${f[2]}}`);fr.readAsDataURL(b);}):'').catch(()=>''))).then(a=>EXFONTS=a.join(''));}\n"
    "// on a white PNG, light text (dark theme) is printed in the brand ink instead\n"
    "function exInk(c){const m=String(c).match(/(\\d+)\\D+(\\d+)\\D+(\\d+)/); if(!m)return c; const l=(0.2126*m[1]+0.7152*m[2]+0.0722*m[3])/255; return l>0.62?'#15224D':c;}\n"
    "function exPNG(id,name){ exFonts().then(()=>exPNG2(id,name)); }\n"
    "function exPNG2(id,name){\n const svg=document.getElementById(id); if(!svg)return;",
    'design', 'PNG export waits for the embedded fonts')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for alias, path in (('build', B), ('charts', CJ), ('app', A)):
    open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_design_bids'), 'Design system v2 — Bid & Tender app')
print('patched: build_bid_dashboard.py, charts.js, app.js')
