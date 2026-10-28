import json
BAALL=json.load(open('bidanalytics2.json'))
BA=BAALL['both']   # static header bits use the all-years view
CHARTS=open('charts.js').read()
LOGO=open('logo_b64.txt').read().strip()
from datetime import datetime, timezone, timedelta
BUILT=datetime.now(timezone(timedelta(hours=3))).strftime('%d %b %Y, %H:%M')+' (KSA)'
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
.cardhd{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}
.vtog{display:inline-flex;border:1px solid #C9D6DD;border-radius:8px;overflow:hidden;flex:none;background:#fff}
.vtog button{background:transparent;color:#3A4A52;border:none;padding:6px 13px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;transition:.12s}
.vtog button+button{border-inline-start:1px solid #C9D6DD}
.vtog button.on{background:#1A5FAB;color:#fff}
body.dark .vtog{background:#1A242B;border-color:#3A4B55}
body.dark .vtog button{background:transparent;color:#C9D6DD}
body.dark .vtog button.on{background:#4A8FD6;color:#fff}
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
.kc:has(.v.hero){grid-column:span 2;border-top-width:4px}.kc .v.hero{font-size:34px}.kc:has(.v.hero) .l{font-size:12.5px;font-weight:700}@media(max-width:700px){.kc:has(.v.hero){grid-column:span 1}.kc .v.hero{font-size:26px}}
.kc{background:#fff;border:1px solid #E3EAE5;border-radius:12px;padding:13px 15px;box-shadow:0 1px 3px rgba(0,0,0,.03);overflow:hidden;min-width:0}
.kc .v{font-size:25px;font-weight:800;color:#1A5FAB;line-height:1.05}
.kc .v.g{color:#2E7D46}.kc .v.r{color:#C0504D}
.kc .l{font-size:10.5px;color:#6B7C86;text-transform:uppercase;letter-spacing:.5px;margin-top:4px;font-weight:600;overflow-wrap:anywhere;line-height:1.3}
.kc .d{font-size:11px;color:#8A99A3;margin-top:3px}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.g3{grid-template-columns:minmax(0,2fr) minmax(0,1fr)}
@media(max-width:900px){.g2,.g3{grid-template-columns:minmax(0,1fr)}}
.card{background:#fff;border:1px solid #E3EAE5;border-radius:14px;padding:16px 18px;box-shadow:0 1px 3px rgba(0,0,0,.03);margin-bottom:16px}
.card h3{font-size:14px;font-weight:800;color:#1C2B33;margin-bottom:3px}
.card .note{font-size:11.5px;color:#8A99A3;margin-bottom:12px;line-height:1.45}
.sech{font-size:18px;font-weight:800;color:#0F3D2E;margin:6px 0 4px;display:flex;align-items:center;gap:9px}
/* ---- Executive Summary tab ---- */
.exc h3{margin:0}.exh{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:6px}
.png{font:600 11px Segoe UI,Tahoma,Arial,sans-serif;background:#F4F8F5;border:1px solid #DCE8DF;color:#1F7A4C;border-radius:7px;padding:5px 10px;cursor:pointer;white-space:nowrap}.png:hover{background:#E6F2EA}
.exd{display:inline-block;font-size:11px;font-weight:700;margin-inline-start:6px;color:#6B7C86}.exd.up{color:#2E7D46}.exd.down{color:#C0504D}
.excov{font-size:12.5px;font-weight:600;color:#3A4A52;background:#F4F8F5;border:1px solid #E3EAE5;border-inline-start:4px solid #1A5FAB;border-radius:8px;padding:9px 12px;margin:6px 0 12px}
.exfoot{font-size:12px;color:#5F7078;margin-top:8px;line-height:1.5}.exfoot a,.excov a,.exdec a{color:#1A5FAB;cursor:pointer;text-decoration:none}.exfoot a:hover,.excov a:hover,.exdec a:hover{text-decoration:underline}
.exT{font:800 14px Segoe UI,Tahoma,Arial,sans-serif;fill:#0F3D2E}.exS{font:600 10.5px Segoe UI,Tahoma,Arial,sans-serif;fill:#6B7C86}.exq{font:700 10.5px Segoe UI,Tahoma,Arial,sans-serif;fill:#8A99A3}
.exg3{grid-template-columns:minmax(0,3fr) minmax(0,2fr)}@media(max-width:900px){.exg3{grid-template-columns:1fr}}
table.ext th{position:static}table.ext td{padding:6px 8px;font-size:12px}
ol.exdec{margin:6px 0 0;padding-inline-start:22px;font-size:13px;line-height:1.7}ol.exdec li b{font-size:15px;margin-inline-end:4px}
.exw{display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-bottom:1px solid #EFF4F2;font-size:12.5px;line-height:1.5}.exw:last-of-type{border-bottom:0}
.exk .kc .l{font-weight:700;color:#3A4A52}.exk .kc .d{font-size:11.5px;line-height:1.5}
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

HTML=f'''<!DOCTYPE html><html lang="en"><head><script>
/* EH env flags: iOS/iPadOS (incl. iPadOS desktop-mode UA) and iframe context */
(function(){{var ua=navigator.userAgent,c=document.documentElement.classList;
var ios=/iP(hone|od|ad)/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
var inframe=(function(){{try{{return window.self!==window.top;}}catch(e){{return true;}}}})();
if(ios)c.add('ios'); if(inframe)c.add('inframe'); if(ios&&inframe)c.add('iosframe');
if(navigator.maxTouchPoints>0)c.add('touch');}})();
</script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EH Bid & Tender Intelligence</title><script>window.BUILT="{BUILT}";</script><style>{CSS}:focus-visible{{outline:2px solid #027DC3;outline-offset:2px}}
.ntf{{display:inline-block;min-width:15px;padding:1px 6px;margin-inline-start:6px;border-radius:9px;background:#E8862E;color:#fff;font-size:9.5px;font-weight:800;text-align:center;vertical-align:1px}}

body.dark{{background:#0F1519;color:#E6EDF1}}
body.dark .card,body.dark .kcard,body.dark .kc,body.dark .ansbox,body.dark .wli{{background:#151C21;border-color:#2C3A43;color:#E6EDF1}}
body.dark .kc *,body.dark .card h3{{color:#E6EDF1}}
body.dark .kc div{{color:inherit}}
body.dark .png{{background:#1E2830;border-color:#3A4B55;color:#CFE3F2}}body.dark .excov{{background:#1A242B;border-color:#2C3A43;color:#E6EDF1}}body.dark .exT{{fill:#E6EDF1}}body.dark .exS,body.dark .exq{{fill:#9FB3BE}}body.dark .exfoot,body.dark .exw,body.dark ol.exdec{{color:#C9D4DB}}body.dark .exw{{border-color:#2C3A43}}body.dark .exk .kc .l{{color:#C9D4DB}}
body.dark [style*="background:#fff"],body.dark [style*="background:#FFF"]{{background:#151C21 !important;color:#E6EDF1 !important;border-color:#2C3A43 !important}}
body.dark nav{{background:#121A1F;border-color:#2C3A43}}
body.dark .metric{{background:#1A242B !important;border-color:#2C3A43 !important}}
body.dark .ml{{color:#9FB3BE}}
body.dark #nav a.on{{background:#151C21}}
body.dark #nav::after,body.dark #nav::before{{display:none}}
body.dark [style*="background:#F"],body.dark [style*="background:#E"],body.dark [style*="background: #F"],body.dark [style*="background:#F7FAFC"],body.dark [style*="background:#FBFDFB"],body.dark [style*="background:#F5F8FA"],body.dark [style*="background:#EAF2FA"],body.dark [style*="background:#EFF6F1"],body.dark [style*="background:#FFF8EC"],body.dark [style*="background:#FFF6E5"],body.dark [style*="background:#FFF3CD"]{{background:#1A242B !important;color:#D5E0E6 !important;border-color:#2C3A43 !important}}
body.dark #nav{{background:#121A1F;border-color:#2C3A43}}
body.dark #nav a{{color:#9FB3BE}}
body.dark #nav a.on{{color:#E6EDF1;border-color:#2BAE68}}
body.dark table th{{background:#1A242B;color:#CBD8DF}}
body.dark table td{{border-color:#2C3A43}}
body.dark tr:hover td{{background:#1B252C}}
body.dark input,body.dark select,body.dark button:not(.langbtn):not(.png):not(.vtb){{background:#1A242B;border-color:#3A4B55;color:#E6EDF1}}
body.dark svg text{{fill:#C9D4DB}}
body.dark svg .domain,body.dark svg g.tick line{{stroke:#3A4B55}}
body.dark #ntfbar{{background:#2A2416 !important;border-color:#4A4023 !important;color:#D8C68A !important}}
body.dark h3,body.dark h2{{color:#E6EDF1}}
body.dark .sech{{color:#7FD4A3}}
body.dark .secsub,body.dark .note{{color:#9FB3BE}}
body.dark .lgi{{color:#C9D4DB}}
body.dark svg text,body.dark svg tspan{{fill:#C9D4DB !important}}
body.dark a{{color:#7FB4E8}}
body.dark .mv{{color:#7FB4E8 !important}}
body.dark [style*="color:#1C2B33"]{{color:#E6EDF1 !important}}
body.dark [style*="color:#3A4A52"],body.dark [style*="color:#3A4A54"]{{color:#C2D2DB !important}}
body.dark [style*="color:#1A5FAB"]{{color:#7FB4E8 !important}}
body.dark [style*="color:#A03A36"],body.dark [style*="color:#C0504D"]{{color:#E08A85 !important}}
body.dark [style*="color:#5A4A2E"],body.dark [style*="color:#7A5B14"]{{color:#D8C68A !important}}
body.dark [style*="color:#4A5A62"],body.dark [style*="color:#5A6B76"]{{color:#9FB3BE !important}}
body.dark [style*="color:#44525C"]{{color:#D6E0E6 !important}}
body.dark #ehcp{{background:#151C21 !important;color:#E6EDF1}}
body.dark .ehm{{background:#1A242B !important;border-color:#2C3A43 !important;color:#D5E0E6 !important}}
body.dark .ehu{{background:#173049 !important;border-color:#22456A !important;color:#BBD8F2 !important}}
body.dark .ehchip{{background:#1A242B !important;border-color:#3A4B55 !important;color:#8FC1EE !important}}
body.dark .ehcf{{background:#121A1F !important;border-color:#2C3A43 !important}}
body.dark #ehcp input{{background:#1A242B !important;border-color:#3A4B55 !important;color:#E6EDF1 !important}}
body.dark .anst{{color:#E6EDF1 !important}}
body.dark .anst-ar{{color:#9FB3BE !important}}
body.dark .ansrow{{border-color:#2C3A43 !important;color:#D5E0E6}}
body.dark [style*="background:#8A99A3"],body.dark [style*="background:#D4A92E"],body.dark [style*="background:#9AABB5"]{{color:#10171C !important}}

/* ---------- responsive ---------- */
@media(max-width:1024px){{
  .wrap,.hd{{padding-left:14px;padding-right:14px}}
  .g3{{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
}}
@media(max-width:768px){{
  .hd{{flex-wrap:wrap;gap:10px;align-items:flex-start}}
  .hd img{{height:38px}}
  .hd h1{{font-size:17px}}
  .hd .sub{{font-size:11.5px}}
  .hd-right{{margin-inline-start:0;width:100%;justify-content:flex-start;gap:8px}}
  .hd .pill{{font-size:11px;padding:6px 11px;flex:1 1 100%;text-align:start}}
  .g2,.g3{{grid-template-columns:minmax(0,1fr)}}
  /* tab strip: scrollable, snap, edge fade */
  .tabbar,nav.tabs,.tabs{{overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none;scroll-snap-type:x proximity;
    -webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 28px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 28px),transparent)}}
  .tabbar::-webkit-scrollbar,.tabs::-webkit-scrollbar{{display:none}}
  .tabbar .tab,.tabs .tab,.tab{{flex:0 0 auto;white-space:nowrap;scroll-snap-align:start;min-height:44px}}
  .card{{padding:14px 14px}}
  .kpi .v,.k .v{{font-size:24px}}
  /* every table scrolls inside its card */
  .card table{{display:block;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}}
  canvas{{max-width:100% !important}}
}}
@media(max-width:480px){{
  .hd h1{{font-size:15px}}
  .kgrid,.kpis{{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
  .kpi .v,.k .v{{font-size:21px}}
  .card h2,.card .h2{{font-size:14px}}
}}

/* ---- audit 05/09 ---- */
.card{{min-width:0;max-width:100%}}
.card svg{{display:block;width:100%;max-width:100%;height:auto}}
.grid,.g2,.g3{{min-width:0}}
@media(pointer:coarse){{ .hd-right button,.hd-right .seg button,.tab,[role=tab],.pill-btn,.lang{{min-height:44px}} .tab{{padding:10px 14px}} }}
@media(max-width:360px){{ .hd .pill{{font-size:10.5px;padding:5px 9px}} .hd h1{{font-size:14px}} .hd-right{{gap:6px}} }}

@media(max-width:360px){{ body{{overflow-x:hidden}} .hd{{padding:0 10px}} .hd-right{{width:100%;overflow:hidden}} .wrap{{padding:0 10px 40px}} }}

/* ---- iOS / touch hardening (05/09) ---- */
html{{-webkit-text-size-adjust:100%}}
button,[role=button],[role=tab],a,.tab,.chip,.btn,label{{touch-action:manipulation;-webkit-tap-highlight-color:transparent}}
@media(max-width:820px){{ input,select,textarea{{font-size:16px !important}} }}   /* stops iOS focus-zoom */
@media(max-width:768px){{ #ehcbtn,#ehcp{{display:none !important}} }}              /* hub bottom bar owns that corner */
html.iosframe #ehcbtn,html.iosframe #ehcp{{display:none !important}}            /* fixed elements break inside iOS iframes */

@media (orientation:landscape) and (max-height:520px){{
  .hd{{padding:4px 12px;gap:6px}} .hd img{{height:26px}} .hd h1{{font-size:14px}} .hd .sub,.hd .pill{{display:none}}
  .hd-right{{width:auto;margin-inline-start:auto}}
  .tab,[role=tab]{{min-height:34px;padding:5px 10px;font-size:12.5px}}
}}

/* ---- audit 05/09 ---- */
.card{{min-width:0;max-width:100%}}
.card svg{{display:block;width:100%;max-width:100%;height:auto}}
.grid,.g2,.g3{{min-width:0}}
@media(pointer:coarse){{ .hd-right button,.hd-right .seg button,.tab,[role=tab],.pill-btn,.lang{{min-height:44px}} .tab{{padding:10px 14px}} }}
@media(max-width:360px){{ .hd .pill{{font-size:10.5px;padding:5px 9px}} .hd h1{{font-size:14px}} .hd-right{{gap:6px}} }}

@media(max-width:360px){{ body{{overflow-x:hidden}} .hd{{padding:0 10px}} .hd-right{{width:100%;overflow:hidden}} .wrap{{padding:0 10px 40px}} }}

</style><link rel="stylesheet" href="eh-shared.css">
</head>
<body>
<header data-eh-contour="7"><div class="hd"><img src="{LOGO}" alt="EH"><div><h1 id="h-title">Bid &amp; Tender Intelligence</h1><div class="sub" id="h-sub">Environmental Horizons (Afaq Al Beeah) — competitive bid analytics, 2024–2026</div></div>
<div class="hd-right"><div class="langtog" style="margin-inline-end:8px"><button class="langbtn" id="sc-y2025" onclick="setScope('y2025')">2025</button><button class="langbtn" id="sc-y2026" onclick="setScope('y2026')">2026</button><button class="langbtn on" id="sc-both" onclick="setScope('both')">Both</button></div><div class="langtog"><button class="langbtn on" data-l="en" onclick="setLang('en')">EN</button><button class="langbtn" data-l="ar" onclick="setLang('ar')">عربي</button></div>
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
<section id="s-executive"></section>
<section id="s-watchlist"></section>
<section id="s-limitations"></section>
<div class="foot" id="h-foot">Generated for Environmental Horizons · figures reflect the bid-tracking workbooks and are partial where the live trackers are still being filled · self-contained dashboard.</div>
</div>
<script id="BA" type="application/json">{json.dumps(BAALL, ensure_ascii=False).replace('</','<\\/')}</script>
<script>{CHARTS}</script>
<script>__APP__</script>
<script>
function _lblCharts(){{
  document.querySelectorAll('canvas,svg').forEach(function(c){{
    if(c.getAttribute('role'))return;
    c.setAttribute('role','img');
    var h=c.closest('.card'); var tt=h&&h.querySelector('h3');
    c.setAttribute('aria-label',(tt?tt.textContent+' — ':'')+'chart; underlying figures are available in the All Tenders tab table.');
  }});
}}
new MutationObserver(_lblCharts).observe(document.documentElement,{{childList:true,subtree:true}});
window.addEventListener('load',function(){{ _lblCharts();
  document.querySelectorAll('canvas').forEach(function(c){{
    c.setAttribute('role','img');
    if(!c.getAttribute('aria-label')){{
      var h=c.closest('.card'); var tt=h&&h.querySelector('h3');
      c.setAttribute('aria-label',(tt?tt.textContent+' — ':'')+'chart; underlying figures are available in the All Tenders tab table.');
    }}
  }});
}});
</script>
<script src="eh-shared.js" defer></script>
</body></html>'''

APP=open('app.js').read()
HTML=HTML.replace('__APP__', APP)
# EH design system v2 (patch_design_bids.py): the page skin goes after eh-shared.css so tokens resolve
SKIN=r'''
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
HTML=HTML.replace('<link rel="stylesheet" href="eh-shared.css">','<link rel="stylesheet" href="eh-shared.css"><style id="eh-skin">'+SKIN+'</style>',1)
open('EH_Bid_Analysis.html','w',encoding='utf-8').write(HTML)
print('dashboard written:', round(len(HTML)/1024), 'KB')
