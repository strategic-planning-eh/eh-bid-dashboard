"""patch_saudi_map_beta.py — Stakeholder Map: the Saudi Map tab becomes "Saudi Map (BETA)" (15 Nov 2026, approved by Youssef).

One interactive Leaflet map showing ONLY:
  1. Bidders — Active Competitors with tracker bids against EH (2025 + 2026 together), each at a real location: a business
     listing, an address EH supplied, or a head office from EH's own records. No estimated positions: a bidder without one
     is listed under "Location not found" beneath the map, never placed on a city or region centre.
  2. Tenders — where each tender was (delivery site named in the title, else the buyer's head office), coloured by result.
  3. Vision 2030 project sites, with SIRC drawn separately as a PIF company.
  4. The four EH sites — always on, on top.
  5. Roads; region boundaries as a faint outline.
Removed from the tab: every non-bidder pin and the position table behind them (LGEO…), the category / tier / minimum-score /
data-confidence filters, the "Has bid against EH only" tick box, the Schematic mode with its code (buildGeoSchematic,
setGeoMode, the mode buttons) and the "estimated position" wording.
Kept: region selector, fullscreen, Export Excel / GeoJSON / CSV (now the layers shown), About box (rewritten), hub print,
language and theme following. Added: region strip, "Location not found" list with its own Excel export, legend.

Data: a new block <script id="SMB" type="application/json"> filled by pipeline/embed_saudi_map_data.py from
pipeline/bidder_locations.csv, tender_sites.json, v2030_sites.json and the Bid & Tender app. This script inserts the block
and fills it once for the stored hub copy; the workflow re-fills it after the bid→map sync on every publish.

Re-runnable: if the map already carries the SMB block the code edits are skipped and only the data block is refreshed.
Run pipeline/apply_bidder_location_review.py first (it writes the three stores).
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, write_change_table, css_min, nfkc
import embed_saudi_map_data as ESM

HUB = os.path.join(os.path.dirname(HERE), 'hub')
M = os.path.join(HUB, 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
BIDS = os.path.join(HUB, 'EH_Bid_Analysis_CURRENT.html')
CAT = 'saudi-map-beta'

def fill_data(html):
    bh = open(BIDS, encoding='utf-8').read() if os.path.exists(BIDS) else None
    payload, summary, warn = ESM.build(html, bh, None, None, None)
    return ESM.embed(html, payload)

if '<script id="SMB" type="application/json">' in FILES['map']:
    open(M, 'w', encoding='utf-8').write(fill_data(FILES['map'])); print('Already applied — data block refreshed.'); sys.exit(0)
for f in ('bidder_locations.csv', 'tender_sites.json', 'v2030_sites.json'):
    if not os.path.exists(os.path.join(HERE, f)): sys.exit(f'pipeline/{f} is missing — run pipeline/apply_bidder_location_review.py first.')
ok = []
def R(pattern, new, note): ok.append(rep_re('map', pattern, (lambda m, _n=nfkc(new): _n), CAT, note))

# ---------------------------------------------------------------- header comment, tab label
ok.append(rep('map', """  EH Stakeholder & Competitive Landscape Map - with interactive Leaflet Saudi Map tab
  SETUP: open this file in any modern browser. No server or build step required.
  The "Saudi Map" tab loads Leaflet 1.9.4 + MarkerCluster from cdnjs and OpenStreetMap tiles,
  so that tab needs an internet connection; every other tab works fully offline.
  DEPLOY: upload this single file to GitHub Pages / Netlify / any static host.
  DATA: stakeholder markers are embedded as GeoJSON in the LSTAKE constant (search "const LSTAKE").
  Each feature carries: n(name) cat typ tier city rg sc(cap+bk score) cf(data confidence)
  bid/bc(bids vs EH) th(threat) own(ownership) act(licence codes) pos(position confidence) src(source).
  To add or edit a company, edit that feature list and reload.
""", """  EH Stakeholder & Competitive Landscape Map - with the interactive "Saudi Map (BETA)" tab
  SETUP: open this file in any modern browser. No server or build step required.
  The "Saudi Map (BETA)" tab loads Leaflet 1.9.4 + MarkerCluster (cdnjs, then the copy in vendor/) and OpenStreetMap tiles,
  so its base map needs an internet connection; every other tab works fully offline.
  DEPLOY: upload this single file to GitHub Pages / Netlify / any static host.
  SAUDI MAP DATA: bidders are read live from the company records (Active Competitors with tracker bids); their positions,
  the tender sites, the Vision 2030 project sites and the bid figures are in the SMB data block, written by
  pipeline/embed_saudi_map_data.py from pipeline/bidder_locations.csv, tender_sites.json and v2030_sites.json.
  To place or move a bidder, edit pipeline/bidder_locations.csv. EH's own sites are in GEO_SITES (search "const GEO_SITES").
""", CAT, 'File header comment describes the new tab and where its data lives'))
ok.append(rep('map', """<div class="tab" id="tabGeo" onclick="switchTab('geo')">Saudi Map</div>""",
              """<div class="tab" id="tabGeo" onclick="switchTab('geo')">Saudi Map (BETA)</div>""", CAT, 'Tab label: Saudi Map (BETA)'))
ok.append(rep('map', " ['Saudi Map','\\u062e\\u0631\\u064a\\u0637\\u0629 \\u0627\\u0644\\u0633\\u0639\\u0648\\u062f\\u064a\\u0629'],",
              " ['Saudi Map (BETA)','\\u062e\\u0631\\u064a\\u0637\\u0629 \\u0627\\u0644\\u0633\\u0639\\u0648\\u062f\\u064a\\u0629 (\\u062a\\u062c\\u0631\\u064a\\u0628\\u064a)'],",
              CAT, 'Tab label in Arabic: خريطة السعودية (تجريبي)'))

# ---------------------------------------------------------------- data block
ok.append(rep('map', '<script id="LIC" type="application/json">', '<script id="SMB" type="application/json">{}</script>\n<script id="LIC" type="application/json">',
              CAT, 'New data block SMB (filled by embed_saudi_map_data.py)'))

# ---------------------------------------------------------------- CSS
CSS = css_min("""<style id="eh-saudi-map-beta">
/* Saudi Map (BETA), 15 Nov 2026 */
#leafBanner b.smb-beta{display:inline-block;background:var(--eh-sea,#0072BB);color:#fff;border-radius:999px;padding:0 8px;margin-inline-end:6px;font-size:10.5px;letter-spacing:.4px}
#smbCount{margin-inline-start:auto;font-size:12px;color:var(--eh-ink-2,#51626D)}
#smbCount b{color:var(--eh-sea,#1A5FAB)}
#smbShow{font-size:12px;color:var(--eh-ink-2,#51626D);margin:0 0 6px}
.smb-b{border-radius:50%;box-sizing:border-box;opacity:.93;cursor:pointer}
.smb-beat{background:#D55E00;border:3px solid #1C2B33}
.smb-under{background:#E69F00;border:2px dashed #1C2B33}
.smb-met{background:#0072B2;border:1.5px solid #fff;box-shadow:0 0 0 1px #0072B2}
.smb-t{width:13px;height:13px;transform:rotate(45deg);box-sizing:border-box;border:2.5px solid;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 0 0 1px rgba(255,255,255,.9)}
.smb-t span{transform:rotate(-45deg);font:700 9px/1 Arial,sans-serif;color:#fff}
.smb-t.smb-hq{background:#fff !important}
.smb-r-w{background:#009E73;border-color:#009E73}.smb-r-l{background:#882255;border-color:#882255}.smb-r-p{background:#332288;border-color:#332288}.smb-r-c{background:#7A7A7A;border-color:#7A7A7A}
.smb-t.smb-hq.smb-r-w span{color:#009E73}.smb-t.smb-hq.smb-r-l span{color:#882255}.smb-t.smb-hq.smb-r-p span{color:#332288}.smb-t.smb-hq.smb-r-c span{color:#7A7A7A}
.smb-v{width:16px;height:16px;box-sizing:border-box;background:#1C2B33;color:#FFD166;border:1.5px solid #FFD166;border-radius:3px;font:700 9.5px/13px Arial,sans-serif;text-align:center;cursor:pointer}
.smb-sirc{height:18px;box-sizing:border-box;background:#FFD166;color:#1C2B33;border:2px solid #1C2B33;border-radius:999px;font:800 9.5px/14px Arial,sans-serif;text-align:center;padding:0 5px;white-space:nowrap;cursor:pointer}
.smb-eh{width:28px;height:28px;box-sizing:border-box;background:#fff;color:#1A5FAB;border:3px solid #3FA34D;border-radius:50%;font:800 11.5px/22px Arial,sans-serif;text-align:center;box-shadow:0 1px 5px rgba(0,0,0,.45);cursor:pointer}
.smb-cl{box-sizing:border-box;background:#fff;color:#1C2B33;font:700 11px/1 Arial,sans-serif;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 4px rgba(0,0,0,.35)}
.smb-cl-b{border-radius:50%;border:3px solid #0072B2}
.smb-cl-b.smb-cl-under{border-color:#E69F00;border-style:dashed}.smb-cl-b.smb-cl-beat{border-color:#D55E00}
.smb-cl-t{border:2.5px solid #332288;transform:rotate(45deg)}.smb-cl-t span{transform:rotate(-45deg)}
.smb-lg{display:flex;align-items:center;gap:7px;margin:4px 0;line-height:1.3}
.smb-lg i{flex:none;display:inline-flex;width:22px;justify-content:center}
.smb-lg .smb-b{width:13px;height:13px;cursor:default}.smb-lg .smb-t,.smb-lg .smb-v,.smb-lg .smb-sirc,.smb-lg .smb-eh{cursor:default}
.smb-lg .smb-eh{width:20px;height:20px;font-size:8.5px;line-height:14px;border-width:2.5px}
.leaflet-popup-content .smb-alt{font-size:11.5px;color:#51626D;margin-top:2px}
.leaflet-popup-content .smb-chip-beat{background:#D55E00}.leaflet-popup-content .smb-chip-under{background:#E69F00;color:#1C2B33}.leaflet-popup-content .smb-chip-met{background:#0072B2}
.leaflet-popup-content .smb-tl{max-height:132px;overflow-y:auto;border-top:1px solid #EEF2F5;margin-top:3px;padding-top:3px;font-size:11.5px}
.leaflet-popup-content .smb-tl div{padding:2px 0;border-bottom:1px dotted #E2E9EE}
.leaflet-popup-content .smb-sub{font-size:10.5px;color:#5A6B76;margin-top:2px}
.leaflet-popup-content .prow .v{text-align:end}
.smb-sec{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:18px 0 6px}
.smb-sec .biz-sec{margin:0}
.smb-note{font-size:12px;color:var(--eh-ink-2,#51626D);margin:0 0 8px;line-height:1.5}
#smbRegions tbody tr,#smbNotFound tbody tr{cursor:pointer}
#smbRegions tr.on td{background:var(--eh-tint,#EAF3FB);font-weight:700}
#smbRegions td.num,#smbRegions th.num,#smbNotFound td.num,#smbNotFound th.num{text-align:center}
#smbNotFoundWrap{max-height:340px;overflow-y:auto;border:1px solid var(--eh-line,#E2E9EE);border-radius:10px}
#smbRegionsWrap{overflow-x:auto;border:1px solid var(--eh-line,#E2E9EE);border-radius:10px}
html.dark .leaflet-popup-content-wrapper,html.dark .leaflet-popup-tip{background:#182126;color:#E6EDF1}
html.dark .leaflet-popup-content .lchip.smb-chip-beat{background:#D55E00;color:#fff}html.dark .leaflet-popup-content .lchip.smb-chip-under{background:#E69F00;color:#1C2B33}html.dark .leaflet-popup-content .lchip.smb-chip-met{background:#0072B2;color:#fff}
html.dark .leaflet-popup-content .lchip.smb-r-w{background:#009E73;color:#fff}html.dark .leaflet-popup-content .lchip.smb-r-l{background:#882255;color:#fff}html.dark .leaflet-popup-content .lchip.smb-r-p{background:#332288;color:#fff}html.dark .leaflet-popup-content .lchip.smb-r-c{background:#7A7A7A;color:#fff}
html.dark #leafSide .smb-beat,html.dark #leafSide .smb-under{border-color:#E6EDF1}
html.dark #smbRegions tr.on td{background:#22313A}
html.dark .leaflet-popup-content .prow{border-color:#2C3A43}html.dark .leaflet-popup-content .prow .k,html.dark .leaflet-popup-content .smb-alt,html.dark .leaflet-popup-content .smb-sub{color:#9FB3BE}
html.dark .leaflet-popup-content .smb-tl,html.dark .leaflet-popup-content .smb-tl div{border-color:#2C3A43}
html[dir=rtl] .leaflet-popup-content{direction:rtl;text-align:right}
html.eh-printing #leafBar .leafbtn,html.eh-printing .smb-sec .leafbtn{display:none}
html.eh-printing #leafMap{height:560px}
html.eh-printing #geoView{position:static !important;height:auto !important;max-height:none !important;overflow:visible !important}
html.eh-printing #smbNotFoundWrap{max-height:none !important;overflow:visible !important}
html.eh-printing #smbRegions tbody tr,html.eh-printing #smbNotFound tbody tr{break-inside:avoid}
@media print{#leafBar .leafbtn,.smb-sec .leafbtn,.leaflet-control-zoom{display:none !important}#leafSide{max-height:none !important;overflow:visible !important}#smbNotFoundWrap{max-height:none !important;overflow:visible !important}.smb-b,.smb-t,.smb-v,.smb-sirc,.smb-eh,.smb-cl{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style></head>""")
ok.append(rep('map', '</head>', CSS, CAT, 'CSS: markers, legend, region strip, not-found list, popup (light, dark, RTL, print)'))

# ---------------------------------------------------------------- JS 1: the schematic mode leaves with its helpers
R(r"let geoV=\{k:1,x:0,y:0\}, geoEl=null, geoDrag=null;\n.*?\n\}\n\nfunction buildList\(\)\{", "function buildList(){",
  'Removed: Schematic (offline) mode — buildGeoSchematic and its zoom/pan helpers (geoV, geoApply, geoZoom, geoReset, geoLayers, geoOutside); nothing else called them')

# ---------------------------------------------------------------- JS 2: positions table out, EH sites + data block in
VS = json.load(open(os.path.join(HERE, 'v2030_sites.json'), encoding='utf-8'))
EH = {s['key']: s for s in VS['sites'] if s['kind'] == 'eh_site'}
def site(key, label): s = EH[key]; return " '%s': [%s,%s,'%s','EH (Reference)']" % (key, round(s['lat'], 6), round(s['lng'], 6), label)
JS_HEAD = r"""/* ===================== SAUDI MAP (BETA) — bidders, tenders, Vision 2030 projects and EH sites (patch_saudi_map_beta.py, 15 Nov 2026) =====================
   One interactive Leaflet map. Bidders = Active Competitors with tracker bids, read live from NODES; a bidder is drawn only
   where SMB.loc holds a reviewed position (business listing, address supplied by EH, or EH's own records) — never at a city
   or region centre. Everything else in SMB is written by pipeline/embed_saudi_map_data.py on every publish. */
let leafMap=null, leafProv=null, leafRoads=null, leafRouteLbls=null, smbGrp={}, smbM=null;
/* ================================================================================
   GEO_SITES — EH's own sites (single point of edit): 'Name': [lat, lng, 'Street / district label', 'EH (Reference)'].
   Always drawn, on top of every other layer. Display names and Arabic text come from pipeline/v2030_sites.json (kind eh_site).
   Coordinates: right-click the spot in Google Maps -> first menu line.
   ================================================================================ */
const GEO_SITES={
__SITES__
};
const SMB=(function(){try{return JSON.parse(document.getElementById('SMB').textContent)||{};}catch(e){return {};}})();
const SMB_BID_CAT='Active Competitors';
const SF={prov:'all',bid:true,ten:true,v:true,roads:true,outline:true};

"""
SITES = ",\n".join([
    site('Afaq Al-Biah Co. Ltd (Environmental Horizons)', 'Hira Street, Jeddah — Head Office'),
    site('EH — Al-Juhfah Waste Management Complex (Rabigh)', 'Al-Juhfah, Rabigh — hazardous-waste treatment & disposal complex'),
    site('EH — Riyadh Branch', 'Al Imam Abdullah Bin Saud Bin Abdulaziz Branch Road, Al Shohda District, Riyadh (street level)'),
    site('Afaaq Environment Training Center', '3822 Madinah Road, As Salamah, Jeddah 23525')])
R(r"/\* =+ SAUDI MAP TAB: interactive Leaflet app \+ schematic fallback =+ \*/\nlet geoMode='leaf'.*?\nfunction posL\(s\)\{[^\n]*\}\n\n",
  JS_HEAD.replace('__SITES__', SITES),
  'Removed: the old position table (LGEO, LGEO_POS, LGEO_SRC, LGEO_RG), region centres (LREGC), leafBuild/leafFeat and the "estimated position" wording. GEO_SITES now holds the four EH sites; SMB data block is read')

# ---------------------------------------------------------------- JS 3: tab shell
JS_SHELL = r"""function smbRing(x,y,r){var c=false;for(var i=0,j=r.length-1;i<r.length;j=i++){var xi=r[i][0],yi=r[i][1],xj=r[j][0],yj=r[j][1];if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c;}return c;}
function smbProvOf(lat,lng){   // which region a point is in: the province polygons (LPROV); a point just off the simplified coastline (within about 35 km) takes the nearest region; anything else is outside the Kingdom
  var best=null,bd=1e9;
  for(var i=0;i<LPROV.features.length;i++){var f=LPROV.features[i],g=f.geometry,polys=g.type==='Polygon'?[g.coordinates]:g.coordinates;
    for(var k=0;k<polys.length;k++){
      if(smbRing(lng,lat,polys[k][0])){var hole=false;for(var q=1;q<polys[k].length;q++)if(smbRing(lng,lat,polys[k][q]))hole=true;if(!hole)return f.properties.n;}
      var r=polys[k][0];for(var p=0;p<r.length;p++){var d=(r[p][0]-lng)*(r[p][0]-lng)+(r[p][1]-lat)*(r[p][1]-lat);if(d<bd){bd=d;best=f.properties.n;}}
    }}
  return bd<0.1225?best:'Outside';
}
function smbProvL(p){return (p==null||p==='Outside')?t('Outside Saudi Arabia','خارج السعودية'):(LNG==='ar'?('منطقة '+(AR_PROV[p]||p)):(p+' Province'));}
function smbModel(){
  var h=SMB.h||{},loc=SMB.loc||{},nl=SMB.nl||{},rost=SMB.rost||{},B=[],T=[],V=[],E=[],tix={};
  NODES.forEach(function(n){
    if(n.cat!==SMB_BID_CAT||!n.bid||n.merged_into)return;
    var a=h[n.n]||null,l=loc[n.n]||null;
    var wins=a?a[1]:((n.h2h&&n.h2h.wins)||0), under=a?a[2]:null, priced=a?a[3]:null;
    var ub=under!=null?under>0:!!(n.h2h&&n.h2h.undercut>0);
    B.push({node:n,name:n.n,bc:n.bc||0,wins:wins||0,under:under,priced:priced,ub:ub,cls:wins>0?'beat':(ub?'under':'met'),
      lat:l?l[0]:null,lng:l?l[1]:null,addr:l?l[2]:'',src:l?l[3]:null,dist:l?l[4]:0,prov:l?smbProvOf(l[0],l[1]):null,why:l?'':(nl[n.n]||'x'),keys:rost[n.n]||null});
  });
  B.sort(function(a,b){return b.bc-a.bc||a.name.localeCompare(b.name);});
  (SMB.t||[]).forEach(function(r){var o={year:r[0],sn:r[1],buyer:r[2],title:r[3],res:r[4],kind:r[5],lat:r[6],lng:r[7],place:r[8],prov:r[6]!=null?smbProvOf(r[6],r[7]):null};T.push(o);tix[r[0]+'-'+r[1]]=o;});
  (SMB.v||[]).forEach(function(s){if(s.k!=='e')V.push({k:s.k,s:s,lat:s.lat,lng:s.lng,prov:s.lat!=null?smbProvOf(s.lat,s.lng):null});});
  Object.keys(GEO_SITES).forEach(function(k){var g=GEO_SITES[k],s=(SMB.v||[]).filter(function(x){return x.k==='e'&&x.key===k;})[0]||{};
    E.push({key:k,s:s,lat:g[0],lng:g[1],label:g[2],prov:smbProvOf(g[0],g[1])});});
  return {B:B,T:T,V:V,E:E,tix:tix,located:B.filter(function(b){return b.lat!=null;}).length,tpinned:T.filter(function(x){return x.lat!=null;}).length};
}
function smbResL(r){return r==='w'?t('Won','فوز'):r==='l'?t('Lost','خسارة'):r==='c'?t('Cancelled','ملغاة'):t('Awaiting result','بانتظار النتيجة');}
function smbResG(r){return r==='w'?'✓':r==='l'?'✕':r==='c'?'–':'…';}
function smbKindL(k){return k===0?t('Delivery site named in the title','موقع التنفيذ المذكور في عنوان المنافسة'):k===1?t('Region named in the title (pinned at the regional capital)','المنطقة المذكورة في العنوان (مثبّتة عند عاصمة المنطقة)'):k===2?t('Buyer’s head office','المقر الرئيسي للجهة المشترية'):t('Not located','غير محدد الموقع');}
function smbClsL(c){return c==='beat'?t('Has beaten EH','فاز على EH'):c==='under'?t('Has priced below EH','سعّر دون EH'):t('Met EH only','واجه EH فقط');}
function smbSrcL(b){var s=[t('business listing','سجل الأعمال على الخرائط'),t('address supplied by EH','عنوان قدّمته EH'),t('own records','سجلات EH')][b.src]||'';return s+(b.dist?t(' · district level',' · على مستوى الحي'):'');}
function smbWhyL(w){return w==='c'?t('City only — the address on record is just a city name','المدينة فقط — العنوان المسجل اسم مدينة لا غير'):w==='a'?t('Awaiting Youssef’s decision','بانتظار قرار يوسف'):w==='n'?t('No listing found','لم يُعثر على سجل'):t('Not yet looked up (new on the bid tracker)','لم يُبحث عنه بعد (جديد في جدول المنافسات)');}
function smbVName(s){return LNG==='ar'?(s.ar||s.en):s.en;}
function buildGeoMap(){
  // tear down any previous Leaflet instance — the container is about to be rebuilt
  if(typeof leafMap!=='undefined'&&leafMap){try{leafMap.remove();}catch(e){} leafMap=null;}
  smbGrp={}; smbM=smbModel();
  var M=smbM,nB=M.B.length,nNo=nB-M.located,fmt=function(v){return v.toLocaleString('en-US');};
  var gv=document.getElementById('geoView');
  var about=LNG==='ar'?
    '<b>ما الذي تعرضه الخريطة.</b> المتقدمون الذين نافسوا EH في المنافسات (2025 و2026 معاً)، ومواقع المنافسات، ومواقع مشاريع رؤية 2030، ومواقع EH الأربعة. لا تظهر هنا أي جهة أخرى من خريطة الأطراف؛ وهي موجودة في بقية التبويبات.<br><br>'+
    '<b>مصادر البيانات.</b> أسماء المتقدمين وعدد المنافسات المشتركة ونتائجها من جدول منافسات EH، ويُحدَّث مع كل نشر. عناوين المتقدمين من سجلات الأعمال على الخرائط التي بُحث عنها في 15 نوفمبر 2026، ومن عناوين قدّمتها EH، ومن سجلات EH. مواقع المشاريع وحالتها من تبويب رؤية 2030. الخريطة الأساسية © مساهمو OpenStreetMap؛ حدود المناطق والطرق من Natural Earth.<br><br>'+
    '<b>ما الذي يُثبَّت وما الذي لا يُثبَّت.</b> يُثبَّت المتقدم فقط عند عنوان حقيقي: سجل أعمال، أو عنوان قدّمته EH، أو مقر في سجلات EH. من لا عنوان له، أو عنوانه اسم مدينة فقط، لا يوضع على الخريطة إطلاقاً ويُدرج في قائمة «الموقع غير موجود» أسفل الخريطة ('+fmt(nNo)+' من '+fmt(nB)+'). تُثبَّت المنافسة عند موقع التنفيذ المذكور في عنوانها، وإلا فعند المقر الرئيسي للجهة المشترية؛ و'+fmt(M.T.length-M.tpinned)+' منافسات لم يُحدَّد لها موقع. بعض مواقع المشاريع الكبرى نقطة تمثيلية داخل الموقع.<br><br>'+
    '<b>نسخة تجريبية.</b> هذه الخريطة قيد المراجعة. إن رأيت موقعاً خاطئاً أو متقدماً ناقصاً فأبلغ فريق تطوير الأعمال ليُصحَّح في المصدر.'
  : '<b>What this map shows.</b> The bidders that have competed against EH in tenders (2025 and 2026 together), where the tenders were, the Vision 2030 project sites, and EH’s four sites. No other organisation from the Stakeholder Map is drawn here; they are in the other tabs.<br><br>'+
    '<b>Data sources.</b> Bidder names, tenders shared and results come from the EH bid tracker and update with every publish. Bidder addresses come from business listings looked up on 15 Nov 2026, from addresses supplied by EH, and from EH’s own records. Project sites and their status come from the Vision 2030 tab. Base map © OpenStreetMap contributors; region boundaries and roads from Natural Earth.<br><br>'+
    '<b>What is and is not pinned.</b> A bidder is pinned only at a real address: a business listing, an address supplied by EH, or a head office in EH’s records. A bidder with no address, or whose address is only a city name, is not placed on the map at all and is listed under “Location not found” below the map ('+fmt(nNo)+' of '+fmt(nB)+'). A tender is pinned at the delivery site named in its title, otherwise at the buyer’s head office; '+fmt(M.T.length-M.tpinned)+' tenders could not be located. Some large project sites are shown by one representative point inside the site.<br><br>'+
    '<b>BETA.</b> This map is under review. If a location looks wrong or a bidder is missing, tell the Business Development team so it is corrected at the source.';
  var h='<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px"><div class="biz-sec" style="margin:0">'+t('Saudi Map (BETA) — bidders, tenders and Vision 2030 projects','خريطة السعودية (تجريبي) — المتقدمون والمنافسات ومشاريع رؤية 2030')+'</div></div>'+
  '<div id="leafBanner"><b class="smb-beta">'+t('BETA','تجريبي')+'</b>'+t('Every bidder is drawn at a real address (a business listing, an address supplied by EH, or EH’s own records). Bidders without one are not drawn; they are listed under the map.','كل متقدم مرسوم عند عنوان حقيقي (سجل أعمال، أو عنوان قدّمته EH، أو سجلات EH). من لا عنوان له لا يُرسم، ويُدرج في القائمة أسفل الخريطة.')+'</div>'+
  '<div id="leafBar"><button class="leafbtn" onclick="leafFull()">'+t('⛶ Fullscreen','⛶ ملء الشاشة')+'</button><button class="leafbtn" onclick="smbExport(\'xlsx\')">⬇ Excel</button><button class="leafbtn" onclick="smbExport(\'geojson\')">⬇ GeoJSON</button><button class="leafbtn" onclick="smbExport(\'csv\')">⬇ CSV</button><button class="leafbtn" onclick="document.getElementById(\'leafModal\').classList.add(\'on\')">'+t('ⓘ About this map','ⓘ حول هذه الخريطة')+'</button>'+
  '<span id="smbCount"><b>'+fmt(M.located)+'</b>'+t(' of ',' من ')+'<b>'+fmt(nB)+'</b>'+t(' bidders located',' متقدماً حُدِّد موقعه')+' · <b>'+fmt(nNo)+'</b>'+t(' not located (listed below)',' بلا موقع (في القائمة أدناه)')+' · <b>'+fmt(M.tpinned)+'</b>'+t(' of ',' من ')+fmt(M.T.length)+t(' tenders pinned',' منافسة مثبّتة')+'</span></div>'+
  '<div id="smbShow"></div>'+
  '<div id="leafWrap"><div id="leafSide"></div><div id="leafMap"></div></div>'+
  '<div class="smb-sec"><div class="biz-sec">'+t('By region','حسب المنطقة')+'</div></div><div class="smb-note">'+t('Counts are for what is pinned on the map. Click a region to zoom to it.','الأعداد لما هو مثبّت على الخريطة. انقر منطقة للتكبير عليها.')+'</div><div id="smbRegionsWrap"><table class="btab" id="smbRegions"></table></div>'+
  '<div class="smb-sec"><div class="biz-sec">'+t('Location not found','الموقع غير موجود')+' — <span id="smbNfHead">'+fmt(M.located)+t(' of ',' من ')+fmt(nB)+t(' bidders located',' متقدماً حُدِّد موقعه')+'</span></div>'+(nNo?'<button class="leafbtn" onclick="smbExportNotFound()">⬇ '+t('Export this list (Excel)','تصدير هذه القائمة (Excel)')+'</button>':'')+'</div>'+
  '<div class="smb-note">'+(nNo?t('These '+fmt(nNo)+' bidders are not on the map because no real address is on record for them. Click a row to open the profile.','هؤلاء المتقدمون ('+fmt(nNo)+') ليسوا على الخريطة لعدم وجود عنوان حقيقي مسجل لهم. انقر صفاً لفتح الملف.'):t('Every bidder is on the map.','كل المتقدمين على الخريطة.'))+'</div>'+
  (nNo?'<div id="smbNotFoundWrap"><table class="btab" id="smbNotFound"></table></div>':'')+
  '<div class="smb-note" id="smbOther" style="margin-top:10px"></div>'+
  '<div id="leafModal" onclick="if(event.target===this)this.classList.remove(\'on\')"><div class="box"><h3 style="margin-top:0">'+t('About this map','حول هذه الخريطة')+'</h3>'+about+
  '<div style="text-align:end;margin-top:10px"><button class="leafbtn" onclick="document.getElementById(\'leafModal\').classList.remove(\'on\')">'+t('Close','إغلاق')+'</button></div></div></div>';
  gv.innerHTML=h;
  var vOff=M.V.filter(function(v){return v.lat==null;}).map(function(v){return smbVName(v.s);}), tOff=M.T.filter(function(x){return x.lat==null;});
  document.getElementById('smbOther').innerHTML=
    (vOff.length?'<b>'+t('Vision 2030 projects not on the map (no site listing found): ','مشاريع رؤية 2030 غير الظاهرة على الخريطة (لم يُعثر على سجل للموقع): ')+'</b>'+vOff.map(esc).join(' \u00b7 ')+'<br>':'')+
    (tOff.length?'<b>'+tOff.length+t(' tenders not on the map (no delivery site in the title and no head office found for the buyer): ',' منافسات غير ظاهرة على الخريطة (لا موقع تنفيذ في العنوان ولم يُعثر على مقر للجهة المشترية): ')+'</b>'+tOff.map(function(x){return '<span dir="auto">'+x.sn+'/'+x.year+' '+esc(x.buyer)+'</span>';}).join(' \u00b7 '):'');
  smbSidebar(); smbRegionTable(); smbNotFoundTable();
  loadLeaflet(smbStart,function(){
    document.getElementById('leafMap').innerHTML='<div style="padding:40px;text-align:center;color:#5A6B76">'+t('Could not load the map library (no internet connection?). The lists below still work.','تعذّر تحميل مكتبة الخريطة (لا يوجد اتصال بالإنترنت؟). القوائم أدناه ما زالت تعمل.')+'</div>';
  });
}
"""
R(r"const LF=\{prov:'all',tiers:null.*?\n(?=function loadLeaflet\(ok,fail\)\{)", JS_SHELL,
  'Tab shell rebuilt: BETA banner, bar (fullscreen, exports, About), located / not-located counts, region strip and "Location not found" list. Removed: LF filter state, setGeoMode, the Interactive / Schematic buttons, the old About text')

# ---------------------------------------------------------------- JS 4: sidebar, layers, markers, popups, tables
JS_MAP = r"""function smbSidebar(){
  var provs=LPROV.features.map(function(f){return f.properties.n;}).sort(function(a,b){return smbProvL(a).localeCompare(smbProvL(b));});
  if(smbM.B.concat(smbM.T,smbM.V).some(function(o){return o.lat!=null&&o.prov==='Outside';}))provs.push('Outside');
  var lg=function(ic,tx){return '<div class="smb-lg"><i>'+ic+'</i><span>'+tx+'</span></div>';};
  var dia=function(r,hq){return '<span class="smb-t smb-r-'+r+(hq?' smb-hq':'')+'"><span>'+smbResG(r)+'</span></span>';};
  var s='<h4>'+t('Region','المنطقة')+'</h4><select id="smbProvSel" onchange="smbRegion(this.value)"><option value="all">'+t('All regions','كل المناطق')+'</option>'+provs.map(function(p){return '<option value="'+esc(p)+'" '+(SF.prov===p?'selected':'')+'>'+esc(smbProvL(p))+'</option>';}).join('')+'</select>';
  s+='<h4>'+t('Layers','الطبقات')+'</h4>'+
    [['bid',t('Bidders','المتقدمون')],['ten',t('Tenders','المنافسات')],['v',t('Vision 2030 projects','مشاريع رؤية 2030')],['roads',t('Roads','الطرق')],['outline',t('Region outline','حدود المناطق')]].map(function(x){
      return '<label><input type="checkbox" '+(SF[x[0]]?'checked':'')+' onchange="smbToggle(\''+x[0]+'\',this.checked)"> '+x[1]+'</label>';}).join('')+
    '<label style="opacity:.75;cursor:default"><input type="checkbox" checked disabled> '+t('EH sites (always on)','مواقع EH (ظاهرة دائماً)')+'</label>';
  s+='<h4>'+t('Bidders','المتقدمون')+'</h4>'+
    lg('<span class="smb-b smb-beat"></span>',t('Has beaten EH — solid dark ring','فاز على EH — حلقة داكنة متصلة'))+
    lg('<span class="smb-b smb-under"></span>',t('Has priced below EH — dashed ring','سعّر دون EH — حلقة متقطعة'))+
    lg('<span class="smb-b smb-met"></span>',t('Met EH only — thin ring','واجه EH فقط — حلقة رفيعة'))+
    '<div style="margin:2px 0 4px;color:#5A6B76">'+t('Circle area = tenders shared with EH. A number in a ring = several bidders close together; zoom in or click it.','مساحة الدائرة = عدد المنافسات المشتركة مع EH. الرقم داخل حلقة = عدة متقدمين متقاربين؛ كبّر أو انقر عليه.')+'</div>';
  s+='<h4>'+t('Tenders','المنافسات')+'</h4>'+
    lg(dia('w'),t('Won','فوز'))+lg(dia('l'),t('Lost','خسارة'))+lg(dia('p'),t('Awaiting result','بانتظار النتيجة'))+lg(dia('c'),t('Cancelled','ملغاة'))+
    lg(dia('p'),t('Filled = delivery site or region named in the title','ممتلئ = موقع التنفيذ أو المنطقة المذكورة في العنوان'))+
    lg(dia('p',1),t('Hollow = buyer’s head office','مفرّغ = المقر الرئيسي للجهة المشترية'));
  s+='<h4>'+t('Vision 2030 and EH','رؤية 2030 و EH')+'</h4>'+
    lg('<span class="smb-v">V</span>',t('Vision 2030 project site','موقع مشروع من رؤية 2030'))+
    lg('<span class="smb-sirc">PIF</span>',t('SIRC — PIF company','سرك — شركة تابعة لصندوق الاستثمارات العامة'))+
    lg('<span class="smb-eh">EH</span>',t('EH site','موقع EH'))+
    lg('<span style="color:#C77B3B;font-weight:800">—</span>',t('Major highway','طريق سريع'))+
    lg('<span style="color:#8FA33F;font-weight:800">- -</span>',t('Region outline','حدود منطقة'));
  document.getElementById('leafSide').innerHTML=s;
}
function smbIn(o){return o.lat!=null&&(SF.prov==='all'||o.prov===SF.prov);}
function smbStart(){
  if(leafMap)return;
  var el=document.getElementById('leafMap'); if(!el)return;
  leafMap=L.map('leafMap',{zoomControl:true,maxZoom:18}).setView([24.2,45.0],5);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© OpenStreetMap contributors'}).addTo(leafMap);
  leafMap.createPane('smbEh').style.zIndex=640;
  leafProv=L.geoJSON(LPROV,{interactive:false,style:{color:'#8FA33F',weight:1.1,opacity:.75,dashArray:'4 4',fill:false}});
  leafRoads=L.geoJSON(LROADS,{interactive:false,style:function(f){return f.properties.t==='exp'?{color:'#C77B3B',weight:2.2,opacity:0.85}:{color:'#B9A97E',weight:1.2,opacity:0.65};}});
  leafRouteLbls=L.layerGroup(LROUTE.map(function(r){return L.marker([r[1],r[2]],{icon:L.divIcon({className:'',html:'<div style="background:#2E7D46;color:#fff;border-radius:5px;padding:1px 6px;font-size:10px;font-weight:800;border:1.5px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.3)">'+r[0]+'</div>',iconSize:null}),interactive:false,keyboard:false});}));
  var clus=function(kind){return L.markerClusterGroup({maxClusterRadius:kind==='b'?34:26,spiderfyOnMaxZoom:true,showCoverageOnHover:false,spiderfyDistanceMultiplier:1.6,
    iconCreateFunction:function(c){var ch=c.getAllChildMarkers(),n=ch.length,d=n<10?26:n<100?32:38,cls='';
      if(kind==='b'){cls=ch.some(function(m){return m.options.smbCls==='beat';})?' smb-cl-beat':ch.some(function(m){return m.options.smbCls==='under';})?' smb-cl-under':'';}
      return L.divIcon({className:'',html:'<div class="smb-cl smb-cl-'+kind+cls+'" style="width:'+d+'px;height:'+d+'px"><span>'+n+'</span></div>',iconSize:[d,d],iconAnchor:[d/2,d/2]});}});};
  smbGrp.ten=clus('t'); smbGrp.bid=clus('b'); smbGrp.v=L.layerGroup(); smbGrp.eh=L.layerGroup();
  smbRefresh();
  document.addEventListener('fullscreenchange',function(){if(leafMap)setTimeout(function(){leafMap.invalidateSize();},220);});
}
function smbRefresh(){
  if(!leafMap||!smbGrp.bid)return;
  var M=smbM,nb=0,nt=0,nv=0;
  ['ten','bid','v','eh'].forEach(function(k){smbGrp[k].clearLayers();});
  M.T.forEach(function(x,i){ if(!smbIn(x))return; nt++;
    var m=L.marker([x.lat,x.lng],{icon:L.divIcon({className:'',html:'<div class="smb-t smb-r-'+x.res+(x.kind===2?' smb-hq':'')+'"><span>'+smbResG(x.res)+'</span></div>',iconSize:[13,13],iconAnchor:[6.5,6.5]}),zIndexOffset:100,keyboard:false});
    m.bindTooltip(t('Tender ','منافسة ')+x.sn+'/'+x.year+' · '+smbResL(x.res),{direction:'top'}); m.bindPopup(function(){return smbTenPopup(x);},{maxWidth:300}); smbGrp.ten.addLayer(m); });
  M.B.forEach(function(b,i){ if(!smbIn(b))return; nb++;
    var d=Math.round(12*Math.sqrt(Math.max(1,b.bc)));
    var m=L.marker([b.lat,b.lng],{icon:L.divIcon({className:'',html:'<div class="smb-b smb-'+b.cls+'" style="width:'+d+'px;height:'+d+'px"></div>',iconSize:[d,d],iconAnchor:[d/2,d/2]}),zIndexOffset:200,smbCls:b.cls,keyboard:false});
    m.bindTooltip(b.name+' · '+b.bc,{direction:'top'}); m.bindPopup(function(){return smbBidPopup(i);},{maxWidth:310}); smbGrp.bid.addLayer(m); });
  M.V.forEach(function(v,i){ if(!smbIn(v))return; if(v.k==='p')nv++;
    var sirc=v.k==='s', m=L.marker([v.lat,v.lng],{icon:L.divIcon({className:'',html:sirc?'<div class="smb-sirc">PIF</div>':'<div class="smb-v">V</div>',iconSize:sirc?[30,18]:[16,16],iconAnchor:sirc?[15,9]:[8,8]}),zIndexOffset:300,keyboard:false});
    m.bindTooltip(smbVName(v.s),{direction:'top'}); m.bindPopup(function(){return smbVPopup(i);},{maxWidth:300}); smbGrp.v.addLayer(m); });
  M.E.forEach(function(e,i){
    var m=L.marker([e.lat,e.lng],{pane:'smbEh',icon:L.divIcon({className:'',html:'<div class="smb-eh">EH</div>',iconSize:[28,28],iconAnchor:[14,14]}),zIndexOffset:1000,keyboard:false});
    m.bindTooltip(smbVName({en:e.s.en||e.key,ar:e.s.ar}),{direction:'top'}); m.bindPopup(function(){return smbEhPopup(i);},{maxWidth:290}); smbGrp.eh.addLayer(m); });
  [['outline',leafProv],['roads',leafRoads],['roads',leafRouteLbls],['ten',smbGrp.ten],['bid',smbGrp.bid],['v',smbGrp.v]].forEach(function(x){
    if(SF[x[0]]){if(!leafMap.hasLayer(x[1]))leafMap.addLayer(x[1]);}else if(leafMap.hasLayer(x[1]))leafMap.removeLayer(x[1]);});
  if(!leafMap.hasLayer(smbGrp.eh))leafMap.addLayer(smbGrp.eh);
  var sh=document.getElementById('smbShow');
  if(sh)sh.innerHTML=(SF.prov==='all'?t('On the map now: ','على الخريطة الآن: '):esc(smbProvL(SF.prov))+': ')+
    [SF.bid?nb+t(' bidders',' متقدماً'):'',SF.ten?nt+t(' tenders',' منافسة'):'',SF.v?nv+t(' Vision 2030 project sites',' موقع مشروع من رؤية 2030'):'',M.E.length+t(' EH sites',' مواقع EH')].filter(Boolean).join(' · ')+
    (SF.prov==='all'?'':' — <a href="#" onclick="smbRegion(\'all\');return false">'+t('show all regions','عرض كل المناطق')+'</a>');
  document.querySelectorAll('#smbRegions tbody tr').forEach(function(tr){tr.classList.toggle('on',tr.getAttribute('data-p')===SF.prov);});
}
function smbToggle(k,on){SF[k]=on;smbRefresh();}
function smbRegion(p){
  SF.prov=p||'all';
  var sel=document.getElementById('smbProvSel'); if(sel)sel.value=SF.prov;
  smbRefresh();
  if(!leafMap)return;
  if(SF.prov==='all'){leafMap.setView([24.2,45.0],5);return;}
  var f=LPROV.features.filter(function(x){return x.properties.n===SF.prov;})[0];
  if(f){try{leafMap.fitBounds(L.geoJSON(f).getBounds(),{padding:[12,12]});}catch(e){}}
  else{var pts=smbM.B.concat(smbM.T,smbM.V).filter(function(o){return o.lat!=null&&o.prov===SF.prov;}).map(function(o){return [o.lat,o.lng];});if(pts.length)leafMap.fitBounds(pts,{padding:[40,40],maxZoom:9});}
  var w=document.getElementById('leafWrap'); if(w&&w.scrollIntoView&&w.getBoundingClientRect().top<0)w.scrollIntoView({block:'start'});
}
function smbRegionI(i){var ps=smbRegionRows();smbRegion(ps[i]?ps[i].p:'all');}
function smbRegionRows(){
  var M=smbM,by={},get=function(p){return by[p]||(by[p]={p:p,b:0,enc:0,ub:0,t:0,v:0,e:0});};
  LPROV.features.forEach(function(f){get(f.properties.n);});
  M.B.forEach(function(b){if(b.lat==null)return;var g=get(b.prov);g.b++;g.enc+=b.bc;if(b.ub)g.ub++;});
  M.T.forEach(function(x){if(x.lat!=null)get(x.prov).t++;});
  M.V.forEach(function(v){if(v.k==='p'&&v.lat!=null)get(v.prov).v++;});
  M.E.forEach(function(e){get(e.prov).e++;});
  return Object.keys(by).map(function(k){return by[k];}).sort(function(a,b){return (a.p==='Outside')-(b.p==='Outside')||b.b-a.b||b.t-a.t||a.p.localeCompare(b.p);});
}
function smbRegionTable(){
  var el=document.getElementById('smbRegions'); if(!el)return;
  var rows=smbRegionRows(),tot={b:0,enc:0,ub:0,t:0,v:0,e:0};
  rows.forEach(function(r){['b','enc','ub','t','v','e'].forEach(function(k){tot[k]+=r[k];});});
  var th=[t('Region','المنطقة'),t('Bidders based there','متقدمون مقرهم فيها'),t('Tenders they shared with EH','منافساتهم المشتركة مع EH'),t('Bidders that priced below EH','متقدمون سعّروا دون EH'),t('Tenders pinned there','منافسات مثبّتة فيها'),t('Vision 2030 project sites','مواقع مشاريع رؤية 2030'),t('EH sites','مواقع EH')];
  var c=function(v){return '<td class="num">'+(v||'–')+'</td>';};
  el.innerHTML='<thead><tr>'+th.map(function(x,i){return '<th'+(i?' class="num"':'')+'>'+x+'</th>';}).join('')+'</tr></thead><tbody>'+
    rows.map(function(r,i){return '<tr data-p="'+esc(r.p)+'" onclick="smbRegionI('+i+')" title="'+t('Zoom to this region','التكبير على هذه المنطقة')+'"><td><b>'+esc(smbProvL(r.p))+'</b></td>'+c(r.b)+c(r.enc)+c(r.ub)+c(r.t)+c(r.v)+c(r.e)+'</tr>';}).join('')+
    '<tr data-p="all" onclick="smbRegion(\'all\')"><td><b>'+t('All regions','كل المناطق')+'</b></td>'+c(tot.b)+c(tot.enc)+c(tot.ub)+c(tot.t)+c(tot.v)+c(tot.e)+'</tr></tbody>';
}
function smbNotFoundRows(){return smbM.B.filter(function(b){return b.lat==null;});}
function smbNotFoundTable(){
  var el=document.getElementById('smbNotFound'); if(!el)return;
  el.innerHTML='<thead><tr><th>'+t('Bidder','المتقدم')+'</th><th class="num">'+t('Tenders shared with EH','المنافسات المشتركة مع EH')+'</th><th>'+t('Why it is not on the map','سبب عدم ظهوره على الخريطة')+'</th></tr></thead><tbody>'+
    smbNotFoundRows().map(function(b){return '<tr onclick="smbProfile(smbM.B['+smbM.B.indexOf(b)+'].name)"><td dir="auto">'+esc(b.name)+'</td><td class="num">'+b.bc+'</td><td>'+smbWhyL(b.why)+'</td></tr>';}).join('')+'</tbody>';
}
function smbAltName(n){   // the same company's name in the other script, when the record holds one
  var re=/Alias \(merged duplicate\):\s*(.+?)(?=\s+Alias \(merged duplicate\):|\s+Tender-roster intelligence|\s+Claimed bidder|\s+Reviewer note|\s+·|$)/g,m,ar=/[\u0600-\u06FF]/.test(n.n);
  while((m=re.exec(n.notes||''))){var a=m[1].trim();if(a&&a.length<=90&&/[\u0600-\u06FF]/.test(a)!==ar)return a;}
  return '';
}
function smbRow(k,v){return v?'<div class="prow"><span class="k">'+k+'</span><span class="v" dir="auto">'+v+'</span></div>':'';}
function smbProfile(name){   // Organisations view through the hub (the route its "Profile" links use); on its own, the map's detail panel
  try{if(window.parent&&window.parent!==window&&typeof window.parent.qOrg==='function'){window.parent.qOrg(name);return;}}catch(e){}
  selByName(name);
}
function smbBidPopup(i){
  var b=smbM.B[i],n=b.node,alt=smbAltName(n),M=smbM;
  var hh='<div><b dir="auto" style="font-size:13px">'+esc(b.name)+'</b>'+(alt?'<div class="smb-alt" dir="auto">'+esc(alt)+'</div>':'')+
    '<div style="margin:5px 0 7px">'+(n.tier?'<span class="lchip" style="background:#51626D">'+esc(tierL(n.tier))+'</span>':'')+'<span class="lchip smb-chip-'+b.cls+'">'+smbClsL(b.cls)+'</span></div>';
  hh+=smbRow(t('Tenders shared with EH','المنافسات المشتركة مع EH'),String(b.bc));
  hh+=smbRow(t('Has beaten EH','فاز على EH'),b.wins>0?t('Yes — ','نعم — ')+b.wins+t(b.wins===1?' tender':' tenders',' منافسة'):t('No','لا'));
  if(b.priced!=null)hh+=smbRow(t('Priced below EH','سعّر دون EH'),b.priced>0?(b.under+t(' of ',' من ')+b.priced+t(' priced comparisons',' مقارنات سعرية')):t('No priced comparison on record','لا مقارنة سعرية مسجلة'));
  else if(n.h2h&&n.h2h.undercut!=null)hh+=smbRow(t('Priced below EH','سعّر دون EH'),n.h2h.undercut+'%'+t(' of priced comparisons',' من المقارنات السعرية'));
  if(b.keys&&b.keys.length){
    hh+='<div class="smb-sub">'+t('Tenders on record (year · buyer · result)','المنافسات المسجلة (السنة · الجهة المشترية · النتيجة)')+(b.keys.length<b.bc?' — '+b.keys.length+t(' of ',' من ')+b.bc+t(' listed',' مدرجة'):'')+'</div><div class="smb-tl">'+
      b.keys.map(function(k){var x=M.tix[k];return '<div>'+(x?(x.year+' · <bdi>'+esc(x.buyer)+'</bdi> · '+smbResL(x.res)):esc(k.split('-')[0]+' · '+t('tender ','منافسة ')+k.split('-')[1]))+'</div>';}).join('')+'</div>';
  }
  hh+=smbRow(t('Address','العنوان'),esc(b.addr));
  hh+=smbRow(t('Address from','مصدر العنوان'),smbSrcL(b));
  hh+=smbRow(t('Region','المنطقة'),esc(smbProvL(b.prov)));
  return hh+'<div style="margin-top:8px;text-align:end"><button class="leafbtn" onclick="smbProfile(smbM.B['+i+'].name)">'+t('Open profile','فتح الملف')+'</button></div></div>';
}
function smbTenPopup(x){
  var hh='<div><b style="font-size:13px">'+t('Tender no. ','المنافسة رقم ')+x.sn+' · '+x.year+'</b><div style="margin:5px 0 7px"><span class="lchip smb-r-'+x.res+'">'+smbResL(x.res)+'</span></div>';
  hh+=smbRow(t('Buyer','الجهة المشترية'),esc(x.buyer));
  hh+=smbRow(t('Title','العنوان'),esc(x.title));
  hh+=smbRow(t('Result','النتيجة'),smbResL(x.res));
  hh+=smbRow(t('Pinned at','مثبّتة عند'),smbKindL(x.kind));
  hh+=smbRow(t('Place','المكان'),esc(x.place));
  return hh+'</div>';
}
function smbVPopup(i){
  var v=smbM.V[i],s=v.s,hh='<div><b dir="auto" style="font-size:13px">'+esc(smbVName(s))+'</b>';
  if(v.k==='s'){
    var n=NODES.find(function(x){return x.n===s.node;});
    hh+='<div style="margin:5px 0 7px"><span class="lchip" style="background:#1C2B33">'+t('PIF company','شركة تابعة لصندوق الاستثمارات العامة')+'</span><span class="lchip" style="background:#2E7D46">'+t('EH client','عميل EH')+'</span></div>';
    hh+=smbRow(t('Tenders shared with EH','المنافسات المشتركة مع EH'),n?String(n.bc||0):'');
    hh+=smbRow(t('Address','العنوان'),esc(s.addr));
    hh+=smbRow(t('Address from','مصدر العنوان'),t('business listing','سجل الأعمال على الخرائط'));
    return hh+'<div class="smb-sub">'+t('Shown with the Vision 2030 projects, not as a bidder.','تظهر مع مشاريع رؤية 2030 لا ضمن المتقدمين.')+'</div><div style="margin-top:8px;text-align:end"><button class="leafbtn" onclick="smbProfile(smbM.V['+i+'].s.node)">'+t('Open profile','فتح الملف')+'</button></div></div>';
  }
  hh+='<div style="margin:5px 0 7px"><span class="lchip" style="background:#1C2B33">'+t('Vision 2030 project','مشروع من رؤية 2030')+'</span></div>';
  hh+=smbRow(t('Part of','جزء من'),esc(LNG==='ar'?(s.pa_ar||s.pa):s.pa));
  hh+='<div class="prow" style="display:block"><span class="k">'+t('Status (as written on the Vision 2030 tab)','الحالة (كما وردت في تبويب رؤية 2030)')+'</span><div dir="auto" style="margin-top:2px">'+esc(LNG==='ar'?(s.s_ar||s.s_en):s.s_en)+'</div></div>';
  return hh+'</div>';
}
function smbEhPopup(i){
  var e=smbM.E[i],s=e.s,hh='<div><b dir="auto" style="font-size:13px">'+esc(smbVName({en:s.en||e.key,ar:s.ar}))+'</b><div style="margin:5px 0 7px"><span class="lchip" style="background:#3FA34D">'+t('EH site','موقع EH')+'</span></div>';
  hh+=smbRow(t('Address','العنوان'),esc(LNG==='ar'?(s.a_ar||e.label):(s.a_en||e.label)));
  if(s.street)hh+=smbRow(t('Precision','الدقة'),t('street level','على مستوى الشارع'));
  return hh+'</div>';
}
function leafFull(){var w=document.getElementById('leafWrap');if(document.fullscreenElement)document.exitFullscreen();else if(w.requestFullscreen)w.requestFullscreen();}
"""
R(r"function leafSidebar\(\)\{.*?\nfunction leafFull\(\)\{[^\n]*\}\n", JS_MAP,
  'Map rebuilt: layer switches (Bidders, Tenders, Vision 2030 projects, Roads, Region outline), bidder circles sized by tenders shared and coloured by worst outcome with a ring cue, tender diamonds by result, Vision 2030 sites, SIRC as PIF company, EH sites on top; popups; region strip; not-found list. Removed: category / tier / minimum-score / data-confidence filters and the "Has bid against EH only" box (leafSidebar, leafPass, leafPopup, leafSel, leafRefresh, leafToggle, leafReset)')

# ---------------------------------------------------------------- JS 5: exports
ok.append(rep('map', """  if(scope==='leaf'&&typeof LSTAKE!=='undefined'){
    var names={}; LSTAKE.features.filter(function(f){return leafPass(f.properties);}).forEach(function(f){names[f.properties.n]=1;});
    rows=NODES.filter(function(n){return names[n.n];});
    filters=[]; if(LF.prov!=='all')filters.push([t('Province','المنطقة الإدارية'),LF.prov]); var onK=function(o){return o?Object.keys(o).filter(function(k){return o[k];}):null;}, offK=function(o){return o?Object.keys(o).filter(function(k){return !o[k];}):[];}; if(LF.tiers&&offK(LF.tiers).length)filters.push([t('Tier','الفئة'),onK(LF.tiers).map(tierL).join(' · ')]); if(LF.cats&&offK(LF.cats).length)filters.push([t('Category','الفئة'),onK(LF.cats).map(catS).join(' · ')]); if(LF.bidOnly)filters.push([t('Bid against EH only','المتقدمون ضد EH فقط'),t('Yes','نعم')]); if(LF.minSc)filters.push([t('Minimum score','الحد الأدنى للدرجة'),LF.minSc]); if(LF.confs&&offK(LF.confs).length)filters.push([t('Confidence','الثقة'),onK(LF.confs).join(' · ')]);
    label=t('Saudi Map tab (geo-located companies only)','تبويب خريطة السعودية (الشركات ذات الموقع فقط)');
  }else{ rows=VIS.slice(); filters=xlsFilters(); label=t('Current filters','المرشّحات الحالية'); }
""", """  rows=VIS.slice(); filters=xlsFilters(); label=t('Current filters','المرشّحات الحالية');   // the Saudi Map (BETA) has its own export (smbExport)
""", CAT, 'exportXlsx: the old Saudi Map branch (all pinned companies with the removed filters) is gone'))
ok.append(rep('map', "function(){ done(); if(scope==='leaf'){leafExport('csv');} else { xlsCsvFallback(rows); } alert(",
              "function(){ done(); xlsCsvFallback(rows); alert(", CAT, 'exportXlsx: CSV fallback no longer calls the removed leafExport'))
JS_EXPORT = r"""function smbExportData(){   // the layers shown (switches + region), EH sites always
  var M=smbM,src=function(b){return ['business listing','address supplied by EH','own records'][b.src]||'';};
  var o={bid:[],ten:[],v:[],eh:[],nf:[]};
  if(SF.bid)M.B.forEach(function(b){if(!smbIn(b))return;o.bid.push({name:b.name,tier:b.node.tier||'',tenders:b.bc,beat:b.wins,under:b.under,priced:b.priced,outcome:smbClsL(b.cls),address:b.addr,address_from:src(b),precision:b.dist?'district level':'',region:smbProvL(b.prov),lat:b.lat,lng:b.lng});});
  if(SF.ten)M.T.forEach(function(x){if(!smbIn(x))return;o.ten.push({no:x.sn,year:x.year,buyer:x.buyer,title:x.title,result:smbResL(x.res),pinned_at:smbKindL(x.kind),place:x.place,region:smbProvL(x.prov),lat:x.lat,lng:x.lng});});
  if(SF.v)M.V.forEach(function(v){if(!smbIn(v))return;o.v.push({name:smbVName(v.s),kind:v.k==='s'?t('PIF company','شركة تابعة لصندوق الاستثمارات العامة'):t('Vision 2030 project','مشروع من رؤية 2030'),part_of:v.k==='s'?'':(LNG==='ar'?(v.s.pa_ar||v.s.pa):v.s.pa),status:v.k==='s'?'':(LNG==='ar'?(v.s.s_ar||v.s.s_en):v.s.s_en),region:smbProvL(v.prov),lat:v.lat,lng:v.lng});});
  M.E.forEach(function(e){o.eh.push({name:smbVName({en:e.s.en||e.key,ar:e.s.ar}),address:LNG==='ar'?(e.s.a_ar||e.label):(e.s.a_en||e.label),region:smbProvL(e.prov),lat:e.lat,lng:e.lng});});
  smbNotFoundRows().forEach(function(b){o.nf.push({name:b.name,tenders:b.bc,reason:smbWhyL(b.why)});});
  return o;
}
function smbCols(k){
  return {bid:[[t('Bidder','المتقدم'),'name'],[t('Tier','الفئة'),'tier'],[t('Tenders shared with EH','المنافسات المشتركة مع EH'),'tenders'],[t('Tenders won against EH','منافسات فاز بها على EH'),'beat'],[t('Times priced below EH','مرات التسعير دون EH'),'under'],[t('Priced comparisons','المقارنات السعرية'),'priced'],[t('Worst outcome for EH','أسوأ نتيجة لـ EH'),'outcome'],[t('Address','العنوان'),'address'],[t('Address from','مصدر العنوان'),'address_from'],[t('Precision','الدقة'),'precision'],[t('Region','المنطقة'),'region'],[t('Latitude','خط العرض'),'lat'],[t('Longitude','خط الطول'),'lng']],
    ten:[[t('Tender no.','رقم المنافسة'),'no'],[t('Year','السنة'),'year'],[t('Buyer','الجهة المشترية'),'buyer'],[t('Title','العنوان'),'title'],[t('Result','النتيجة'),'result'],[t('Pinned at','مثبّتة عند'),'pinned_at'],[t('Place','المكان'),'place'],[t('Region','المنطقة'),'region'],[t('Latitude','خط العرض'),'lat'],[t('Longitude','خط الطول'),'lng']],
    v:[[t('Name','الاسم'),'name'],[t('Kind','النوع'),'kind'],[t('Part of','جزء من'),'part_of'],[t('Status (as written on the Vision 2030 tab)','الحالة (كما وردت في تبويب رؤية 2030)'),'status'],[t('Region','المنطقة'),'region'],[t('Latitude','خط العرض'),'lat'],[t('Longitude','خط الطول'),'lng']],
    eh:[[t('EH site','موقع EH'),'name'],[t('Address','العنوان'),'address'],[t('Region','المنطقة'),'region'],[t('Latitude','خط العرض'),'lat'],[t('Longitude','خط الطول'),'lng']],
    nf:[[t('Bidder','المتقدم'),'name'],[t('Tenders shared with EH','المنافسات المشتركة مع EH'),'tenders'],[t('Why it is not on the map','سبب عدم ظهوره على الخريطة'),'reason']]}[k];
}
function smbSheet(k,rows){
  var cols=smbCols(k),aoa=[cols.map(function(c){return c[0];})].concat(rows.map(function(r){return cols.map(function(c){var v=r[c[1]];return v==null?'':v;});}));
  var ws=XLSX.utils.aoa_to_sheet(aoa); ws['!cols']=cols.map(function(c){return {wch:/name|title|address|status|buyer|reason/.test(c[1])?44:16};}); if(LNG==='ar')ws['!views']=[{rightToLeft:true}];
  return ws;
}
function smbSave(blob,fn){var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=fn;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(a.href);},2000);}
function smbCsv(d){
  var q=function(v){v=(v==null?'':String(v));return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;},out=[['layer','name','detail','result_or_outcome','tenders_shared','address_or_place','region','lat','lng'].join(',')];
  d.bid.forEach(function(r){out.push(['bidder',r.name,r.tier,r.outcome,r.tenders,r.address,r.region,r.lat,r.lng].map(q).join(','));});
  d.ten.forEach(function(r){out.push(['tender',r.no+'/'+r.year+' '+r.buyer,r.title,r.result,'',r.pinned_at+(r.place?' — '+r.place:''),r.region,r.lat,r.lng].map(q).join(','));});
  d.v.forEach(function(r){out.push(['vision2030',r.name,r.kind,r.status,'','',r.region,r.lat,r.lng].map(q).join(','));});
  d.eh.forEach(function(r){out.push(['eh_site',r.name,'','','',r.address,r.region,r.lat,r.lng].map(q).join(','));});
  return String.fromCharCode(0xFEFF)+out.join('\n');
}
function smbExport(kind){
  var d=smbExportData(),name='EH_Saudi_Map_BETA_'+new Date().toISOString().slice(0,10);
  if(kind==='geojson'){
    var F=[],add=function(layer,rows){rows.forEach(function(r){var p={layer:layer};Object.keys(r).forEach(function(k){if(k!=='lat'&&k!=='lng')p[k]=r[k];});F.push({type:'Feature',properties:p,geometry:{type:'Point',coordinates:[r.lng,r.lat]}});});};
    add('bidder',d.bid);add('tender',d.ten);add('vision2030',d.v);add('eh_site',d.eh);
    smbSave(new Blob([JSON.stringify({type:'FeatureCollection',features:F},null,1)],{type:'application/geo+json'}),name+'.geojson');return;
  }
  if(kind==='csv'){smbSave(new Blob([smbCsv(d)],{type:'text/csv;charset=utf-8'}),name+'.csv');return;}
  ldXlsx(function(){ try{
      var wb=XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb,smbSheet('bid',d.bid),t('Bidders','المتقدمون'));
      XLSX.utils.book_append_sheet(wb,smbSheet('ten',d.ten),t('Tenders','المنافسات'));
      XLSX.utils.book_append_sheet(wb,smbSheet('v',d.v),t('Vision 2030','رؤية 2030'));
      XLSX.utils.book_append_sheet(wb,smbSheet('eh',d.eh),t('EH sites','مواقع EH'));
      XLSX.utils.book_append_sheet(wb,smbSheet('nf',d.nf),t('Location not found','الموقع غير موجود'));
      var rd=XLSX.utils.aoa_to_sheet([[t('EH Saudi Map (BETA) — export','خريطة السعودية لآفاق البيئة (تجريبي) — تصدير')],
        [t('The sheets hold the layers that were switched on when the file was made','تحتوي الأوراق على الطبقات التي كانت مفعّلة وقت إنشاء الملف')+(SF.prov==='all'?'':' — '+smbProvL(SF.prov))+'.'],
        [t('Bidders are pinned only at a business listing (looked up 15 Nov 2026), an address supplied by EH, or EH’s own records. Bidders without one are on the last sheet, not on the map.','يُثبَّت المتقدمون فقط عند سجل أعمال (بُحث عنه في 15 نوفمبر 2026) أو عنوان قدّمته EH أو سجلات EH. من لا عنوان له في الورقة الأخيرة، لا على الخريطة.')],
        [t('Exported on ','تاريخ التصدير ')+new Date().toISOString().slice(0,16).replace('T',' ')+' UTC'+(SMB.built?t(' · data built ',' · بُنيت البيانات ')+SMB.built:'')]]);
      rd['!cols']=[{wch:120}]; if(LNG==='ar')rd['!views']=[{rightToLeft:true}];
      XLSX.utils.book_append_sheet(wb,rd,'README');
      XLSX.writeFile(wb,name+'.xlsx');
    }catch(e){ console.error(e); alert(t('Export failed: ','تعذّر التصدير: ')+e.message); } },
    function(){ smbSave(new Blob([smbCsv(d)],{type:'text/csv;charset=utf-8'}),name+'.csv'); alert(t('The Excel library could not be loaded (offline or blocked). A CSV file was downloaded instead.','تعذّر تحميل مكتبة Excel (بلا اتصال أو محجوبة). نُزِّل ملف CSV بدلاً منه.')); });
}
function smbExportNotFound(){
  var rows=smbExportData().nf;
  ldXlsx(function(){ try{ var wb=XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb,smbSheet('nf',rows),t('Location not found','الموقع غير موجود')); XLSX.writeFile(wb,'EH_Bidders_Location_Not_Found.xlsx'); }catch(e){ console.error(e); alert(t('Export failed: ','تعذّر التصدير: ')+e.message); } },
    function(){ var q=function(v){v=String(v==null?'':v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;}; smbSave(new Blob([String.fromCharCode(0xFEFF)+[smbCols('nf').map(function(c){return q(c[0]);}).join(',')].concat(rows.map(function(r){return [r.name,r.tenders,r.reason].map(q).join(',');})).join('\n')],{type:'text/csv;charset=utf-8'}),'EH_Bidders_Location_Not_Found.csv'); alert(t('The Excel library could not be loaded (offline or blocked). A CSV file was downloaded instead.','تعذّر تحميل مكتبة Excel (بلا اتصال أو محجوبة). نُزِّل ملف CSV بدلاً منه.')); });
}

"""
R(r"function leafExport\(kind\)\{.*?\n\}\n\n(?=/\* =+ ASK THE MAP)", JS_EXPORT,
  'Exports rebuilt: Excel (Bidders, Tenders, Vision 2030, EH sites, Location not found, README), GeoJSON and CSV of the layers shown; "Location not found" list exports as EH_Bidders_Location_Not_Found.xlsx')

if not all(ok) or FAILURES:
    write_change_table(os.path.join(HERE, 'change_table_saudi_map_beta'), 'Change table — Saudi Map (BETA) (15 Nov 2026) — FAILED, nothing written')
    sys.exit('ANCHOR MISMATCH: ' + str(ok))
out = fill_data(FILES['map'])
if out is None: sys.exit('SMB block not found after patching')
left = [k for k in ('buildGeoSchematic', 'setGeoMode', 'geoMode', 'LGEO', 'LREGC', 'LSTAKE', 'leafPass', 'leafExport', 'leafSidebar', 'LF.', 'stimated') if k in out[out.find('<script id="LIC"'):]]
if left: sys.exit('dead code still referenced: ' + ', '.join(left))
open(M, 'w', encoding='utf-8').write(out)
write_change_table(os.path.join(HERE, 'change_table_saudi_map_beta'), 'Change table — Saudi Map (BETA): bidders, tenders, Vision 2030 projects and EH sites at real locations (15 Nov 2026)')
print('applied')
