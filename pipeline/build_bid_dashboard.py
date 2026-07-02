import json
BA=json.load(open('bidanalytics2.json'))
CHARTS=open('charts.js').read()
LOGO=open('logo_b64.txt').read().strip()
LIC=json.load(open('licenses.json'))

CSS=r'''
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;color:#1C2B33;background:#EEF2F1;font-size:14px;line-height:1.5}
.wrap{max-width:1340px;margin:0 auto;padding:0 18px 60px}
header{background:linear-gradient(120deg,#0F3D2E,#1A5FAB);color:#fff;padding:18px 0;margin-bottom:0;box-shadow:0 2px 14px rgba(0,0,0,.12)}
.hd{max-width:1340px;margin:0 auto;padding:0 18px;display:flex;align-items:center;gap:16px}
.hd img{height:48px;background:#fff;border-radius:10px;padding:6px 8px;box-shadow:0 1px 4px rgba(0,0,0,.10)}
.hd h1{font-size:21px;font-weight:800;letter-spacing:.2px}
.hd .sub{font-size:12.5px;opacity:.9;margin-top:2px}
.hd .pill{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);border-radius:20px;padding:7px 15px;font-size:12px;font-weight:600;text-align:center;line-height:1.35}
.hd-right{margin-inline-start:auto;display:flex;align-items:center;gap:13px;flex-wrap:wrap;justify-content:flex-end}
.langtog{display:flex;border:1px solid rgba(255,255,255,.45);border-radius:8px;overflow:hidden;flex:none}
.langbtn{background:transparent;color:rgba(255,255,255,.9);border:none;padding:6px 14px;font-size:12.5px;font-weight:800;cursor:pointer;font-family:inherit;transition:.12s}
.langbtn.on{background:#fff;color:#1A5FAB}
html[dir=rtl] body,html[dir=rtl] .note,html[dir=rtl] .secsub,html[dir=rtl] .sech,html[dir=rtl] h3,html[dir=rtl] .foot{text-align:right}
html[dir=rtl] .foot{text-align:center}
html[dir=rtl] .kc,html[dir=rtl] .metric{text-align:center}
html[dir=rtl] #ehcp{right:auto;left:22px}
html[dir=rtl] #ehcbtn{right:auto;left:22px}
html[dir=rtl] .ehu{align-self:flex-start}
html[dir=rtl] .ehchip{text-align:right}
nav{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid #DCE5DF;box-shadow:0 2px 8px rgba(0,0,0,.04);overflow-x:auto;white-space:nowrap}
.navin{max-width:1340px;margin:0 auto;padding:0 10px;display:flex}
nav a{display:inline-block;padding:13px 16px;font-size:13px;font-weight:600;color:#6B7C86;cursor:pointer;border-bottom:3px solid transparent;text-decoration:none}
nav a.on{color:#1A5FAB;border-bottom-color:#3FA34D}
nav a:hover{color:#1C2B33}
section{display:none;padding-top:20px}
section.on{display:block}
.askbtn{text-align:left;background:#fff;border:1px solid #E3EAE6;border-radius:10px;padding:12px 14px;cursor:pointer;transition:.15s}
.askbtn:hover{border-color:#1A5FAB;box-shadow:0 2px 8px rgba(26,95,171,.12);transform:translateY(-1px)}
.ansbox{background:#F7FAFC;border:1px solid #E3EAE6;border-left:3px solid #1A5FAB;border-radius:8px;padding:14px 16px}
.anst{font-weight:700;font-size:14px;color:#1C2B33}
.anst-ar{font-size:12.5px;color:#6B7C86;margin-top:2px}
.ansbody{font-size:12.5px;color:#3A4A52;line-height:1.65;margin-top:8px}
.ansrow{display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px solid #EEF2F0;font-size:12.5px;color:#3A4A52}
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}
.kc{background:#fff;border:1px solid #E3EAE5;border-radius:12px;padding:13px 15px;box-shadow:0 1px 3px rgba(0,0,0,.03)}
.kc .v{font-size:25px;font-weight:800;color:#1A5FAB;line-height:1.05}
.kc .v.g{color:#2E7D46}.kc .v.r{color:#C0504D}
.kc .l{font-size:10.5px;color:#6B7C86;text-transform:uppercase;letter-spacing:.5px;margin-top:4px;font-weight:600}
.kc .d{font-size:11px;color:#8A99A3;margin-top:3px}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:1fr 1fr}.g3{grid-template-columns:2fr 1fr}
@media(max-width:900px){.g2,.g3{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid #E3EAE5;border-radius:14px;padding:16px 18px;box-shadow:0 1px 3px rgba(0,0,0,.03);margin-bottom:16px}
.card h3{font-size:14px;font-weight:800;color:#1C2B33;margin-bottom:3px}
.card .note{font-size:11.5px;color:#8A99A3;margin-bottom:12px;line-height:1.45}
.sech{font-size:18px;font-weight:800;color:#0F3D2E;margin:6px 0 4px;display:flex;align-items:center;gap:9px}
.sech:before{content:'';width:5px;height:20px;background:#3FA34D;border-radius:3px}
.secsub{font-size:12.5px;color:#6B7C86;margin-bottom:16px}
.ch{width:100%;height:auto;display:block;overflow:visible;direction:ltr}
.cax{font:600 10px Segoe UI;fill:#9AA8B0}.cax2{font:600 10px Segoe UI;fill:#7B8A92}.caxt{font:700 11px Segoe UI;fill:#6B7C86}
.chl{font:600 11.5px Segoe UI;fill:#3A4A52}.chv{font:700 11.5px Segoe UI;fill:#1C2B33}.chs{font:600 10.5px Segoe UI;fill:#9AA8B0}
.cln{font:700 10px Segoe UI}
.leg{display:flex;flex-wrap:wrap;gap:7px 16px;margin-top:12px;justify-content:center}
.lgi{font-size:11.5px;color:#3A4A52;display:flex;align-items:center;gap:6px}
.lgd{width:11px;height:11px;border-radius:3px;display:inline-block}
table.t{width:100%;border-collapse:collapse;font-size:12px}
table.t th{background:#F4F8F5;text-align:left;padding:8px 10px;font-size:10px;text-transform:uppercase;letter-spacing:.4px;color:#6B7C86;border-bottom:2px solid #E3EAE5;position:sticky;top:46px}
table.t td{padding:7px 10px;border-bottom:1px solid #F0F4F1}
table.t tr:hover{background:#F8FBF9}
.tag{font-weight:700;font-size:10px;padding:2px 7px;border-radius:5px;color:#fff;display:inline-block}
.miniband{display:flex;align-items:center;gap:8px;margin:7px 0}
.miniband .bar{height:18px;border-radius:4px;display:flex;align-items:center;justify-content:flex-end;padding-right:5px;color:#fff;font-size:10px;font-weight:700;min-width:24px}
.cardrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.metric{border:1px solid #E3EAE5;border-radius:10px;padding:12px}
.metric .mv{font-size:22px;font-weight:800;color:#1A5FAB}
.metric .ml{font-size:11px;color:#6B7C86;margin-top:3px}
.wl{display:flex;flex-direction:column;gap:8px}
.wli{display:flex;gap:10px;align-items:flex-start;border:1px solid #E3EAE5;border-left-width:4px;border-radius:9px;padding:10px 13px;font-size:12.5px;background:#fff}
.wli.high{border-left-color:#B23A3A;background:#FCF5F4}.wli.med{border-left-color:#E8862E;background:#FEF9F3}.wli.low{border-left-color:#2E7D46;background:#F4FBF6}
.wlk{font-weight:700;font-size:9.5px;text-transform:uppercase;letter-spacing:.4px;padding:3px 7px;border-radius:5px;color:#fff;white-space:nowrap}
.pbar{position:relative;height:22px;background:#EEF3F0;border-radius:5px;overflow:visible}
.pbar .seg{position:absolute;height:100%;border-radius:5px}
.foot{text-align:center;color:#9AA8B0;font-size:11px;margin-top:30px;padding-top:16px;border-top:1px solid #DCE5DF}
/* ===== colour accents throughout ===== */
.kc{border-top:3px solid #1A5FAB}
.kstrip .kc:nth-child(7n+1){border-top-color:#1A5FAB}
.kstrip .kc:nth-child(7n+2){border-top-color:#2A9D8F}
.kstrip .kc:nth-child(7n+3){border-top-color:#E8862E}
.kstrip .kc:nth-child(7n+4){border-top-color:#7B6BA8}
.kstrip .kc:nth-child(7n+5){border-top-color:#3FA34D}
.kstrip .kc:nth-child(7n+6){border-top-color:#D4A92E}
.kstrip .kc:nth-child(7n+7){border-top-color:#C0504D}
.card{border-top:3px solid #E3EAE5}
.grid.g2 .card:nth-child(odd){border-top-color:#1A5FAB}
.grid.g2 .card:nth-child(even){border-top-color:#3FA34D}
.card h3{padding-left:11px;border-left:3px solid #3FA34D;line-height:1.1}
.grid.g2 .card:nth-child(odd) h3{border-left-color:#1A5FAB}
.metric{border-top:2px solid #E3EAE5}
.metric:nth-child(5n+1){background:#F2F7FC;border-color:#D3E3F2;border-top-color:#1A5FAB}
.metric:nth-child(5n+2){background:#F1FAF4;border-color:#CFE8D6;border-top-color:#2A9D8F}
.metric:nth-child(5n+3){background:#FEF7EE;border-color:#F2DFC4;border-top-color:#E8862E}
.metric:nth-child(5n+4){background:#F6F3FB;border-color:#E0D8F0;border-top-color:#7B6BA8}
.metric:nth-child(5n+5){background:#FBF3F3;border-color:#F0D6D4;border-top-color:#C0504D}
.metric .mv{color:#1C2B33}
.metric:nth-child(5n+1) .mv{color:#1A5FAB}.metric:nth-child(5n+2) .mv{color:#1F8276}.metric:nth-child(5n+3) .mv{color:#CC7320}.metric:nth-child(5n+4) .mv{color:#6A5A98}.metric:nth-child(5n+5) .mv{color:#B0453F}
table.t th{background:linear-gradient(180deg,#EFF6F1,#E8F1EC)}
nav a.on{background:linear-gradient(180deg,#fff,#F1FBF4)}
'''

HTML=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EH Bid & Tender Intelligence</title><style>{CSS}</style></head>
<body>
<header><div class="hd"><img src="{LOGO}" alt="EH"><div><h1 id="h-title">Bid &amp; Tender Intelligence</h1><div class="sub" id="h-sub">Environmental Horizons (Afaq Al Beeah) — competitive bid analytics, 2024–2026</div></div>
<div class="hd-right"><div class="langtog"><button class="langbtn on" data-l="en" onclick="setLang('en')">EN</button><button class="langbtn" data-l="ar" onclick="setLang('ar')">عربي</button></div>
<div class="pill" id="h-pill">{BA['kpi']['total']} tenders tracked<br>SAR {round(BA['kpi']['pipeline']/1e6)}M pipeline</div></div></div></header>
<nav><div class="navin" id="nav"></div></nav>
<div class="wrap">
<div id="kstrip" class="kstrip"></div>
<section id="s-overview"></section>
<section id="s-pipeline"></section>
<section id="s-winloss"></section>
<section id="s-pricing"></section>
<section id="s-competitors"></section>
<section id="s-clients"></section>
<section id="s-service"></section>
<section id="s-funnel"></section>
<section id="s-tenders"></section>
<section id="s-watchlist"></section>
<section id="s-limitations"></section>
<div class="foot" id="h-foot">Generated for Environmental Horizons · figures reflect the bid-tracking workbooks and are partial where the live trackers are still being filled · self-contained dashboard.</div>
</div>
<script id="BA" type="application/json">{json.dumps(BA, ensure_ascii=False).replace('</','<\\/')}</script>
<script>{CHARTS}</script>
<script>__APP__</script>
</body></html>'''

APP=open('app.js').read()
HTML=HTML.replace('__APP__', APP)
open('EH_Bid_Analysis.html','w',encoding='utf-8').write(HTML)
print('dashboard written:', round(len(HTML)/1024), 'KB')
