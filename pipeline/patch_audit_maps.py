"""patch_audit_maps.py — audit fixes for the Stakeholder Map and the Client Bubble Map (12 Oct 2026, audit round 2, "maps").

Every item below was CONFIRMED by the judge (audit2/JUDGE_J2.md). Items the judge marked DECISION (maps-03 threat rule,
maps-04/05 score and tier source, maps-25 "revenue" wording) or OWNER DATA (maps-06 twins, maps-20 GESCO) are NOT changed.

STAKEHOLDER MAP (hub/EH_Stakeholder_Map_CURRENT.html)
  maps-01  The Saudi Map (Leaflet) read its own frozen copy of 2,808 companies (const LSTAKE, from an old workbook export):
           tiers, scores, bid flags and bid counts disagreed with the rest of the page, and it never saw the bid sync.
           Now the pins are built from NODES — the same DATA block that sync_bids_to_apps.py rewrites at publish — so every
           filter, popup and export agrees with the page KPIs. Only the map position of each company is kept (LGEO:
           name -> longitude, latitude, position type, source). A company with no stored position is placed at its region
           centre and marked Estimated; companies with no region (or abroad without a position) are counted and named as
           not pinned. "Open full profile" opens the company's own record.
  maps-02  Phone: the company sheet lost its close button the moment it opened (showDetail replaced the panel's HTML).
           The close button is now part of every detail render.
  maps-07  Companies with no recorded region were counted in the KPIs but never drawn. They now have their own
           "Region not recorded" slice on the wheel, bar and row in the Regional View, and region chip. Methodology no
           longer says there is no such group; it states the live count. (No region is invented.)
  maps-08  The wheel legend listed company-type colours, but the dots are coloured by stakeholder category. The legend
           now shows the category colours, in Arabic too.
  maps-09  "Total Score = capability + backing (+ bids 15)" was printed even when the parts did not add up. The breakdown
           is now shown only when it reconciles; otherwise the page says the recorded parts do not add up to the total.
  maps-10  "As a client (from bid tracker)" read fields that the ledger record does not have, so every client showed 0/0.
           It now reads the bid tracker's own client figures (BANALYTICS clients) and is shown only when the client is
           there; labels are bilingual. The ledger box calls its count "ledger lines" (maps-22).
  maps-11  Header said "1,951 verified organisations" in Arabic (and in English after a language switch). It now counts
           the companies in the map and drops "verified". The "see all 4,195" note counts live too.
  maps-12  "Ask the map": the score answer described the retired Proposal B with neutral-fill; EH's "honest score 70"
           (it is 62.7); a regional conclusion its own table contradicted; non-competitors in "top direct competitors";
           stale Methodology challengers. All rewritten from the live data, in the page language. The Arabic
           Methodology no longer says missing data is neutral-filled.
  maps-13  Reset filters ticked every type box but emptied the type filter (empty map). Reset now shows everything.
  maps-14  Arabic: top region, side panel labels, Dark/Light, zoom hint, Regional View, Licence Map, List View sentence,
           detail Category/Company type, wheel tooltip, Leaflet (categories, popups, About), schematic map and the chat now
           follow the page language. (Licence meanings come from the English licence dictionary and stay English.)
  maps-15a "104 of 144 tenders come from national bodies" was typed in; it is now computed from the map's tender split.
  maps-16  Leaflet title said "Tier 1/2" over pins of every tier, and the tier filter had only Tier 1/2. Title and About
           are now computed from the data; the tier filter lists every tier present.
  maps-17  Licence Map bars were squeezed by long labels (481 drew shorter than it should against 280). Bars are now
           proportional; the "most exposed" sentence is computed (ENV-CON(TYPEA) 159 was missing).
  maps-18  Escape now closes the modals and the Leaflet About box; the close mark is a real button.
  maps-19  390 px: header buttons and KPI labels wrap instead of overflowing or being cut ("إعادة ضبط ا…").
  Also:    the "Collaboration potential" badge was given to competitors whose region is unknown (the code checked for
           'Unknown' while the data says '—'); unknown region no longer counts as "outside EH's home regions".

CLIENT BUBBLE MAP (hub/EH_Client_Bubble_Map_CURRENT.html — a static page; its data is not rebuilt by the pipeline)
  maps-21/23  DATA had merged 28 branch / project rows into their parent client, but DETAIL (the company panel) and HEAT
           (the heatmap) had not: Alfanar's panel said SAR 504K under a SAR 1.02M bubble, and branch names sat in the
           heatmap under their own sector. The same 28 branches are now merged into the parent in DETAIL and HEAT
           (checked: every client's panel now equals its bubble for both years, and every sector's heatmap total equals
           the bubble legend).
  maps-22  Two different counts were both called "lines": projects (DATA p, header/tooltip/quadrant) and ledger lines
           (DETAIL/HEAT n, panel/heatmap). They are now "projects" and "ledger lines" everywhere, EN and AR.
  maps-24  With the year set to 2025/2026 the Executive said its cards were scoped to that year while their own toggles
           stayed on "Both"; header KPIs froze outside the Bubble view. The year now sets the three card toggles and the
           header updates in every view.
  maps-26  Hiding a sector in the legend now updates the header KPIs.
  maps-27  "Show all 60 names" no longer triggers the PNG export handler (JavaScript error on every click).
  maps-28  Quadrant caption: "only one or two jobs" -> "fewer projects than the middle of the group" (EN+AR).
  maps-29  Footer no longer shows the developer note "override in the build script as needed" (EN+AR).

Safety: the Stakeholder Map keeps its CRLF line endings (read/written with newline='') and its
<script id="DATA|LIC|BANALYTICS"> blocks byte-identical (checked before writing). Every edit is an exact string (or a block
between two exact anchors) and the script stops if any anchor is missing or found more than once.

Run once from a clean checkout of the two files:  python3 pipeline/patch_audit_maps.py
"""
import os, sys, re, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import patchlib
from patchlib import _log, FAILURES, write_change_table, css_min

MAP = os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html')
BUB = os.path.join(HERE, '..', 'hub', 'EH_Client_Bubble_Map_CURRENT.html')
rd = lambda p: open(p, encoding='utf-8', newline='').read()
MARK = 'patch_audit_maps.py'
if MARK in rd(MAP) or MARK in rd(BUB):
    sys.exit('Already applied — nothing to do.')

TXT = {'stake': rd(MAP), 'bub': rd(BUB)}
NL = {'stake': '\r\n', 'bub': '\n'}

def fix_nl(alias, s):
    return s.replace('\r\n', '\n').replace('\n', NL[alias])

def rep(alias, old, new, category, note, count=1):
    """exact-string edit; fails loudly if the anchor count differs"""
    s = TXT[alias]; n = s.count(old); ok = n == count
    if ok: TXT[alias] = s.replace(old, new)
    _log(alias, 'exact', old, new, category, note, n, ok); return ok

def block(alias, start, end, new, category, note, keep_end=True):
    """replace the text from `start` (inclusive) up to `end` (exclusive when keep_end) — both anchors must be unique"""
    s = TXT[alias]; a, b = s.count(start), s.count(end)
    i = s.find(start); j = s.find(end, i + 1) if i >= 0 else -1
    ok = a == 1 and b == 1 and i >= 0 and j > i
    if ok:
        TXT[alias] = s[:i] + new + (s[j:] if keep_end else s[j + len(end):])
    _log(alias, 'block', start[:120] + ' … ' + end[:60], new[:300], category, note, min(a, b), ok); return ok

def data_blocks(s):
    return re.findall(r'<script id="(?:DATA|LIC|BANALYTICS)" type="application/json">.*?</script>', s, re.S)
BLOCKS_BEFORE = data_blocks(TXT['stake'])

# =====================================================================================================================
# STAKEHOLDER MAP
# =====================================================================================================================
S = 'stake'

# ---- CSS (maps-17 bars, maps-18 close button, maps-19 phone wrapping)
CSS = css_min(r'''<style id="eh-audit-maps">
/* patch_audit_maps.py (12 Oct 2026) */
.sat-lbl{flex:none}.sat-bar{flex:none;max-width:calc(100% - 150px)}.sat-txt{flex:1 1 0;min-width:0}
.modal button.x{background:none;border:0;font:inherit;font-size:20px;line-height:1;padding:6px 10px;min-width:44px;min-height:44px;cursor:pointer;color:var(--eh-ink-2)}
.modal button.x:hover{color:var(--eh-sea)}
@media(max-width:480px){
  .hd-actions .btn{white-space:normal !important;overflow:visible !important;text-overflow:clip !important;line-height:1.15;font-size:11px;padding:4px 3px;overflow-wrap:anywhere;hyphens:auto}
  .kpi .l{overflow-wrap:anywhere;hyphens:auto}
}
</style>''')
rep(S, '</head>', CSS + '</head>', 'layout', 'maps-17/18/19: proportional licence bars, button close mark, phone wrapping')

# ---- maps-11 header markup
rep(S, '<p>Afaq Al Beeah · 4,195 verified organizations across KSA &amp; GCC · HQ Jeddah · Branch Rabigh · v2.7 — full regional granularity</p>',
       '<p>Afaq Al Beeah · 4,195 organisations across KSA &amp; GCC · HQ Jeddah · Branch Rabigh · v2.7 — full regional granularity</p>',
    'copy', 'maps-11: header no longer calls the records "verified" (the count is set live at load)')

# ---- maps-14 side-panel markup: wrap label text so the language sweep can reach it
rep(S, '<span id="mfiltLbl">Filters &amp; search</span>', '<span id="mfiltLbl" class="tr">Filters &amp; search</span>', 'i18n', 'maps-14: "Filters & search" follows the language')
rep(S, '<input type="checkbox" id="fBid"> Bid against EH only</label>', '<input type="checkbox" id="fBid"> <span class="tr">Bid against EH only</span></label>', 'i18n', 'maps-14: "Bid against EH only"')
rep(S, '<input type="checkbox" id="fT1"> Tier 1 only</label>', '<input type="checkbox" id="fT1"> <span class="tr">Tier 1 only</span></label>', 'i18n', 'maps-14: "Tier 1 only"')
rep(S, '<label style="font-size:11.5px;color:var(--ink-soft)">Minimum number of sites: <b id="siteVal">Any</b></label>',
       '<label style="font-size:11.5px;color:var(--ink-soft)"><span class="tr">Minimum number of sites:</span> <b id="siteVal">Any</b></label>', 'i18n', 'maps-14: "Minimum number of sites"')
rep(S, '<div class="range-l"><span>Any</span><span>10+</span></div>', '<div class="range-l"><span class="tr">Any</span><span>10+</span></div>', 'i18n', 'maps-14: range "Any"')

NEW_TR = r"""
 ['Filters & search','الفلاتر والبحث'],
 ['Holds licence','يحمل ترخيصاً'],
 ['Any licence','أي ترخيص'],
 ['Bid against EH only','من تقدّم ضد EH فقط'],
 ['Tier 1 only','الفئة 1 فقط'],
 ['Minimum number of sites:','الحد الأدنى لعدد المواقع:'],
 ['Any','أي عدد'],
 ['High = 5+ bids · Medium = 3–4 · Low = 1–2. Threat weights frequency, so single-job bidders are not High threat.','مرتفع = 5 عطاءات فأكثر · متوسط = 3–4 · منخفض = 1–2. يراعي التهديد تكرار التقدّم، لذا لا يُصنَّف من تقدّم لعمل واحد بتهديد مرتفع.'],
 ['Scroll to zoom · drag to pan','مرّر للتكبير · اسحب للتنقل'],
 ['Stakeholder density by region','كثافة الأطراف حسب المنطقة'],
 ['Heat map — region × company type','خريطة حرارية — المنطقة × نوع الشركة'],
];"""
rep(S, "\r\n];\r\nwindow.addEventListener('message',function(e){\r\n  var d=e.data||{};\r\n  if(d.ehhub==='lang'",
       fix_nl(S, NEW_TR) + "\r\nwindow.addEventListener('message',function(e){\r\n  var d=e.data||{};\r\n  if(d.ehhub==='lang'",
    'i18n', 'maps-14: Arabic for the side panel, zoom hint and Regional View headings')
rep(S, "document.querySelectorAll('h1,h3,p,.btn,.tab,.kpi .l,label,option,.empty,.note').forEach(",
       "document.querySelectorAll('h1,h3,p,.btn,.tab,.kpi .l,label,option,.empty,.note,.tr,.zoomhint,#regView h4').forEach(",
    'i18n', 'maps-14: language sweep also covers wrapped labels, zoom hint and Regional View headings')

# ---- maps-11 header text computed; maps-14 extra relabels on language change
OLD_HP_START = "  var hp=document.querySelector('header .titles p'); if(hp)hp.textContent=t('Afaq Al Beeah \\u00b7 1,951 verified"
i = TXT[S].find(OLD_HP_START); j = TXT[S].find('\r\n', i)
if i < 0:
    _log(S, 'block', OLD_HP_START, '', 'copy', 'maps-11 header (applyLang)', 0, False)
else:
    TXT[S] = TXT[S][:i] + "  var hp=document.querySelector('header .titles p'); if(hp)hp.textContent=hdrText();" + TXT[S][j:]
    _log(S, 'block', TXT[S][i:i + 120], 'hdrText()', 'copy', 'maps-11: header count computed from the map (was 1,951 "verified" in Arabic and after AR→EN)', 1, True)
rep(S, "  // dynamic re-labels\r\n  document.querySelectorAll('#catFilters .catlbl')",
       fix_nl(S, r"""  var _sv=document.getElementById('siteVal'); if(_sv)_sv.textContent=(typeof state!=='undefined'&&state.sites)||t('Any','أي عدد');
  var _db=document.getElementById('darkBtn'); if(_db){var _on=root.classList.contains('dark'),_ic=_db.querySelector('svg');_db.innerHTML=(_ic?_ic.outerHTML:'')+(_on?t('Light','فاتح'):t('Dark','داكن'));}
  document.querySelectorAll('#fType option[data-typ]').forEach(function(o){o.textContent=catL(o.value);});
  // dynamic re-labels
  document.querySelectorAll('#catFilters .catlbl')"""),
    'i18n', 'maps-14: sites value, Dark/Light button and company-type options follow the language')
rep(S, "  if(curTab==='geo')buildGeoMap();\r\n  if(window.__cursel)showDetail(window.__cursel);",
       "  if(curTab==='geo')buildGeoMap();\r\n  if(curTab==='lic')buildLicenceMap();\r\n  if(window.__cursel)showDetail(window.__cursel);",
    'i18n', 'maps-14: Licence Map redrawn on language change')

# ---- helpers: header text, region / category labels
rep(S, "function regL(r){return LNG==='ar'?(AR_REG[r]||r):r;}",
       "function regL(r){if(r==='\\u2014'||r==='')return t('Region not recorded','\\u0627\\u0644\\u0645\\u0646\\u0637\\u0642\\u0629 \\u063a\\u064a\\u0631 \\u0645\\u0633\\u062c\\u0644\\u0629');return LNG==='ar'?(AR_REG[r]||r):r;}\r\n"
       "function hdrText(){var c=NODES.length.toLocaleString('en-US');return t('Afaq Al Beeah \\u00b7 '+c+' organisations across KSA & GCC \\u00b7 HQ Jeddah \\u00b7 Branch Rabigh \\u00b7 v2.7 \\u2014 full regional granularity','\\u0622\\u0641\\u0627\\u0642 \\u0627\\u0644\\u0628\\u064a\\u0626\\u0629 \\u00b7 '+c+' \\u0645\\u0646\\u0638\\u0645\\u0629 \\u0641\\u064a \\u0627\\u0644\\u0633\\u0639\\u0648\\u062f\\u064a\\u0629 \\u0648\\u0627\\u0644\\u062e\\u0644\\u064a\\u062c \\u00b7 \\u0627\\u0644\\u0645\\u0642\\u0631 \\u062c\\u062f\\u0629 \\u00b7 \\u0641\\u0631\\u0639 \\u0631\\u0627\\u0628\\u063a \\u00b7 v2.7');}   // patch_audit_maps.py: counted, not typed",
    'copy', 'maps-07/11: "Region not recorded" label; header text counted from the map')

# ---- maps-07 region-not-recorded slice
rep(S, "const REGIONS = ['Jeddah','Makkah City','Rabigh','Other Makkah Region','Madinah Region','Riyadh','Qassim Region','Eastern Province','Tabuk Region','Hail Region','Al Jawf Region','Northern Borders Region','Southern Region','GCC / International'];",
       "const REGIONS = ['Jeddah','Makkah City','Rabigh','Other Makkah Region','Madinah Region','Riyadh','Qassim Region','Eastern Province','Tabuk Region','Hail Region','Al Jawf Region','Northern Borders Region','Southern Region','GCC / International','\\u2014'];   // '\\u2014' = region not recorded: its own slice, never hidden (patch_audit_maps.py)",
    'bug', 'maps-07: companies with no recorded region get their own wheel slice / Regional View bar / region chip')
rep(S, "'Eastern Province':'Eastern','Southern Region':'Southern','GCC / International':\"GCC / Int'l\"};",
       "'Eastern Province':'Eastern','Southern Region':'Southern','GCC / International':\"GCC / Int'l\",'\\u2014':'Region not recorded'};",
    'copy', 'maps-07: wheel rim label for the new slice')
rep(S, "&&!['Jeddah','Makkah City','Rabigh','Other Makkah Region','Riyadh','Unknown'].includes(n.rg));",
       "&&!['Jeddah','Makkah City','Rabigh','Other Makkah Region','Riyadh','Unknown','\\u2014'].includes(n.rg));",
    'bug', 'collaboration badge no longer given because the region is unknown (data says "—", code checked "Unknown")')

# ---- maps-14 KPI top region
rep(S, "document.getElementById('kTop').textContent=top?top[0]:'—';", "document.getElementById('kTop').textContent=top?regL(top[0]):'—';",
    'i18n', 'maps-14: "Top region" KPI in Arabic')

# ---- maps-14 wheel tooltip
rep(S, "tip.innerHTML='<b dir=\"auto\">'+esc(n.n)+'</b><br>'+(n.cat)+' · '+(n.rg)+(n.tier?' · '+n.tier:'')+(n.bc>0?' · '+n.bc+'× bid'+(n.threat?' · '+n.threat+' threat':''):'');",
       "tip.innerHTML='<b dir=\"auto\">'+esc(n.n)+'</b><br>'+esc(catS(n.cat))+' · '+esc(regL(n.rg))+(n.tier?' · '+esc(tierL(n.tier)):'')+(n.bc>0?' · '+n.bc+t('× bid',' عطاء')+(n.threat?' · '+thrL(n.threat)+t(' threat',' تهديد'):''):'');",
    'i18n', 'maps-14: wheel hover label in Arabic')

# ---- maps-22 (stake side): ledger record count is ledger lines, not projects
rep(S, "'<div class=\"drow\"><span class=\"k\">'+t('Projects','\\u0627\\u0644\\u0645\\u0634\\u0627\\u0631\\u064a\\u0639')+'</span><span class=\"v\">'+c.proj+'</span></div>'+",
       "'<div class=\"drow\"><span class=\"k\">'+t('Ledger lines','\\u0628\\u0646\\u0648\\u062f \\u0627\\u0644\\u0633\\u062c\\u0644')+'</span><span class=\"v\">'+c.proj+'</span></div>'+",
    'copy', 'maps-22: the ledger count is called "ledger lines" (it was labelled "Projects")')

# ---- maps-09 score reconcile helpers (used by the detail panel and the Leaflet popup)
SCORE_FN = r"""
/* patch_audit_maps.py (maps-09): the breakdown is printed only when capability + backing (+15 for a bidder) equals the total */
function scoreText(n,noCf){
  var cap=Math.round((n.cap||0)*10)/10, bk=n.bk||0, bd=n.bid?15:0, sc=Math.round(n.sc*10)/10, s=String(sc);
  if(Math.abs(Math.round((cap+bk+bd)*10)/10-sc)<0.15) s+=t('  =  capability ','  =  القدرة ')+cap+t(' + backing ',' + الإسناد ')+bk+(bd?t(' + bids 15',' + العطاءات 15'):'');
  else s+=t(' — the recorded parts (capability '+cap+', backing '+bk+(n.bid?', bids 15':'')+') do not add up to this total, so no breakdown is shown',
            ' — مكوّنات الدرجة المسجّلة (القدرة '+cap+'، الإسناد '+bk+(n.bid?'، العطاءات 15':'')+') لا يساوي مجموعها هذه الدرجة، لذا لا يُعرض تفصيلها');
  return noCf?s:s+t('  ·  data confidence: ','  ·  موثوقية البيانات: ')+thrL(n.cf||'—');
}
function showDetail(n){window.__cursel=n;"""
rep(S, "function showDetail(n){window.__cursel=n;", fix_nl(S, SCORE_FN.lstrip('\n')), 'bug', 'maps-09: score breakdown only when it adds up')
OLD_TS = TXT[S][TXT[S].find("  else rows.push([t('Total Score','\\u0627\\u0644\\u062f\\u0631\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0644\\u064a\\u0629'),n.sc!=null?"):]
OLD_TS = OLD_TS[:OLD_TS.find('\r\n')]
rep(S, OLD_TS, "  else rows.push([t('Total Score','\\u0627\\u0644\\u062f\\u0631\\u062c\\u0629 \\u0627\\u0644\\u0643\\u0644\\u064a\\u0629'),n.sc!=null?scoreText(n):t('Not scored','\\u063a\\u064a\\u0631 \\u0645\\u064f\\u0642\\u064a\\u0651\\u0645')]);",
    'bug', 'maps-09: detail panel uses the reconciling score text')
# maps-14 detail category / company type
rep(S, "const rows=[[t('Category','\\u0627\\u0644\\u0641\\u0626\\u0629'),catL(n.cat)]];", "const rows=[[t('Category','\\u0627\\u0644\\u0641\\u0626\\u0629'),catS(n.cat)]];",
    'i18n', 'maps-14: detail Category in Arabic (category names, not company-type names)')
rep(S, "rows.push([t('Company type','\\u0646\\u0648\\u0639 \\u0627\\u0644\\u0634\\u0631\\u0643\\u0629'),n.typ||'\\u2014']);",
       "rows.push([t('Company type','\\u0646\\u0648\\u0639 \\u0627\\u0644\\u0634\\u0631\\u0643\\u0629'),n.typ?catL(n.typ):'\\u2014']);",
    'i18n', 'maps-14: detail Company type in Arabic')
# maps-02 close button re-rendered
rep(S, "  document.getElementById('detail').innerHTML='<h3>'+t('Company detail','\\u062a\\u0641\\u0627\\u0635\\u064a\\u0644 \\u0627\\u0644\\u0634\\u0631\\u0643\\u0629')+'</h3>'+",
       "  document.getElementById('detail').innerHTML='<button class=\"dclose\" type=\"button\" aria-label=\"'+t('Close details','\\u0625\\u063a\\u0644\\u0627\\u0642 \\u0627\\u0644\\u062a\\u0641\\u0627\\u0635\\u064a\\u0644')+'\" onclick=\"document.getElementById(\\'detail\\').classList.remove(\\'has\\')\">&times;</button>'+   // maps-02: the phone sheet keeps its close button\r\n    '<h3>'+t('Company detail','\\u062a\\u0641\\u0627\\u0635\\u064a\\u0644 \\u0627\\u0644\\u0634\\u0631\\u0643\\u0629')+'</h3>'+",
    'bug', 'maps-02: phone detail sheet keeps its close button after a company is opened')

# ---- maps-10 client block reads the bid tracker's client figures
OLD_CL_START = "  if(n.cl){const d=n.cl;\r\n    h+='<div style=\"margin:10px 14px 2px;padding:9px 11px;background:#F2FAF4"
NEW_CL = r"""  const bc=clientBA(n);   // maps-10: the bid tracker's own figures for this client (BANALYTICS), not the ledger record
  if(bc){
    h+='<div style="margin:10px 14px 2px;padding:9px 11px;background:#F2FAF4;border:1px solid #CFE8D6;border-radius:8px">'+
      '<div class="k" style="font-size:11px;color:#1E6B38;font-weight:700;text-transform:uppercase;letter-spacing:.4px;margin-bottom:5px">'+t('As a client (from bid tracker)','كعميل (من متتبع العطاءات)')+'</div>'+
      '<div class="drow"><span class="k">'+t('Tenders 2025','منافسات 2025')+'</span><span class="v">'+(bc.bids25||0)+(bc.value25?' · '+fmtSAR(bc.value25):'')+'</span></div>'+
      '<div class="drow"><span class="k">'+t('Tenders 2026','منافسات 2026')+'</span><span class="v">'+(bc.bids26||0)+(bc.value26?' · '+fmtSAR(bc.value26):'')+'</span></div>'+
      '<div class="drow"><span class="k">'+t('EH win rate','نسبة فوز EH')+'</span><span class="v">'+(bc.win_rate==null?'—':bc.win_rate+'%')+'</span></div>'+
      (bc.lapsed?'<div class="drow"><span class="k">'+t('Status','الحالة')+'</span><span class="v" style="color:#B23A3A">'+t('Lapsed — no 2026 tenders','متوقف — لا منافسات في 2026')+'</span></div>':'')+'</div>';
  }
  return h;
}
function _clnorm(s){return String(s||'').toLowerCase().replace(/[\u064b-\u0652\u0640]/g,'').replace(/[إأآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/[^0-9a-z\u0600-\u06ff]+/g,' ').trim();}
function clientBA(n){if(!BA||!BA.clients)return null;var k=_clnorm(n.n);return BA.clients.find(function(c){return _clnorm(c.name)===k;})||null;}
"""
block(S, OLD_CL_START, "function licBlock(n){", fix_nl(S, NEW_CL), 'bug',
      'maps-10: "As a client" reads the tracker client record by name (was always 0/0), bilingual')

# ---- maps-14 company-type options carry their value
rep(S, "types.forEach(t=>document.getElementById('fType').insertAdjacentHTML('beforeend','<option>'+esc(t)+'</option>'));",
       "types.forEach(ty=>document.getElementById('fType').insertAdjacentHTML('beforeend','<option value=\"'+esc(ty)+'\" data-typ=\"1\">'+esc(catL(ty))+'</option>'));",
    'i18n', 'maps-14: company-type options can be shown in Arabic')
rep(S, "document.getElementById('siteVal').textContent=state.sites||'Any';recompute()};",
       "document.getElementById('siteVal').textContent=state.sites||t('Any','أي عدد');recompute()};", 'i18n', 'maps-14: sites value')

# ---- maps-13 reset
rep(S, "  state.cats=new Set();document.querySelectorAll('#catFilters input').forEach(i=>i.checked=false);state.regs.clear();",
       "  state.cats=new Set(CATS.map(c=>c.id));   // maps-13: reset shows everything (every type box is ticked below)\r\n  state.regs.clear();",
    'bug', 'maps-13: Reset filters shows every company type (boxes ticked and filter agree)')
rep(S, "  document.getElementById('fSites').value=0;document.getElementById('siteVal').textContent='Any';",
       "  document.getElementById('fSites').value=0;document.getElementById('siteVal').textContent=t('Any','أي عدد');",
    'i18n', 'maps-14: sites value after reset')

# ---- maps-08 legend
NEW_LEG = r"""function buildLegendBar(){
/* patch_audit_maps.py (maps-08): the dots are filled by stakeholder category (CAT_COL), so the legend lists those colours */
const present=Object.keys(CAT_COL).filter(c=>NODES.some(n=>n.cat===c));
document.getElementById('legend').innerHTML =
  '<b style="color:#1C2B33">'+t('Legend:','الدليل:')+'</b>'+
  present.map(c=>'<span class="it"><span class="dot" style="background:'+CAT_COL[c]+'"></span>'+esc(catS(c))+'</span>').join('')+
"""
block(S, "function buildLegendBar(){", "  '<span class=\"it\"><span class=\"star\">", fix_nl(S, NEW_LEG), 'bug',
      'maps-08: wheel legend shows the stakeholder-category colours the dots use (Arabic labels too)')

# ---- maps-07/14 regional view
NEW_REGV = r"""function buildRegional(){
  /* patch_audit_maps.py: includes the "Region not recorded" bar (maps-07); labels follow the language (maps-14) */
  const rc={};VIS.forEach(n=>rc[n.rg]=(rc[n.rg]||0)+1);
  const ordered=REGIONS.filter(r=>rc[r]);
  const mx=Math.max(1,...ordered.map(r=>rc[r]));
  document.getElementById('regBars').innerHTML=ordered.map(r=>
    '<div class="brow"><div class="bl">'+esc(regL(r))+'</div><div class="bt" style="width:'+(rc[r]/mx*78)+'%"></div><div class="bv">'+rc[r]+'</div></div>').join('');
  // heat
  let html='<tr><th>'+t('Region','المنطقة')+'</th>'+CATS.map(c=>'<th class="rot">'+esc(LNG==='ar'?catL(c.id):c.s)+'</th>').join('')+'<th>'+t('Total','الإجمالي')+'</th></tr>';
  let hmax=1; const grid={};
  ordered.forEach(r=>{grid[r]={};CATS.forEach(c=>{const v=VIS.filter(n=>n.rg===r&&(n.typ||'Other')===c.id).length;grid[r][c.id]=v;if(v>hmax)hmax=v})});
  ordered.forEach(r=>{
    html+='<tr><th>'+esc(regL(r))+'</th>'+CATS.map(c=>{const v=grid[r][c.id];const f=v/hmax;
      const bg=v?'rgba(63,163,77,'+(0.10+f*0.78)+')':'transparent';
      const col=f>0.55?'#fff':'#1C2B33';
      return '<td style="background:'+bg+';color:'+col+'">'+(v||'·')+'</td>'}).join('')+'<td><b>'+rc[r]+'</b></td></tr>';
  });
  document.getElementById('heat').innerHTML=html;
}

"""
block(S, "function buildRegional(){", "// ---------- tabs & modal", fix_nl(S, NEW_REGV), 'i18n',
      'maps-07/14: Regional View shows the "Region not recorded" bar and follows the language')

# ---- maps-17/14 licence map
NEW_LIC = r"""function buildLicenceMap(){
  /* patch_audit_maps.py: bars proportional to the largest count shown (maps-17); sentences computed; language-aware (maps-14) */
  const L=BA.licenses, all=L.eh_portfolio.concat(L.most_crowded), maxComp=Math.max(1,...all.map(r=>r[1]));
  const bar=(n,col)=>'<div class="sat-bar" style="width:calc((100% - 150px) * '+(0.6*n/maxComp).toFixed(4)+');background:'+col+'"></div>';
  const cw=n=>n===1?t(' competitor',' منافس'):t(' competitors',' منافس');
  let h='<div class="biz-sec">'+t('EH licence portfolio — how contested is each capability?','محفظة تراخيص EH — ما مدى التنافس على كل قدرة؟')+'</div>';
  h+='<div class="geo-legend" style="margin-bottom:8px">'+t('Each bar = number of <b>competitors</b> in the map holding the same licence. Short bar = defensible / few rivals. Long bar = commoditised.','كل شريط = عدد <b>المنافسين</b> في الخريطة الذين يحملون الترخيص نفسه. الشريط القصير = قدرة محمية ومنافسون قليلون. الشريط الطويل = خدمة شائعة كثيرة المنافسين.')+'</div>';
  L.eh_portfolio.forEach(([c,n,m])=>{
    const col = n<=2?'#2E7D46':n<=15?'#1A6FB0':n<=60?'#E8862E':'#B23A3A';
    h+='<div class="sat-row"><span class="sat-lbl" title="'+esc(m)+'">'+c+'</span>'+bar(n,col)+'<span class="sat-txt" style="font-size:11.5px"><b>'+n+'</b>'+cw(n)+' &nbsp;<span style="color:var(--ink-soft)">'+esc(m)+'</span></span></div>';
  });
  h+='<div class="biz-sec">'+t('Most crowded licences in the market (avoid price wars)','أكثر التراخيص ازدحاماً في السوق (تجنّب حروب الأسعار)')+'</div>';
  L.most_crowded.forEach(([c,n,m])=>{
    h+='<div class="sat-row"><span class="sat-lbl">'+c+'</span>'+bar(n,'#B23A3A')+'<span class="sat-txt" style="font-size:11.5px"><b>'+n+'</b> &nbsp;<span style="color:var(--ink-soft)">'+esc(m)+'</span></span></div>';
  });
  h+='<div class="biz-sec">'+t('White space — licences almost no one holds (opportunity)','فرص غير مستغلة — تراخيص لا يكاد يحملها أحد (فرصة)')+'</div>';
  h+='<table class="btab"><thead><tr><th>'+t('Licence','الترخيص')+'</th><th>'+t('Competitors holding','عدد المنافسين الحاملين')+'</th><th>'+t('Meaning','المعنى')+'</th></tr></thead><tbody>';
  L.white_space.forEach(([c,n,m])=>{ h+='<tr><td style="font-family:monospace;font-weight:700;color:#2E7D46">'+c+'</td><td><b>'+n+'</b></td><td>'+esc(m)+'</td></tr>'; });
  const port=L.eh_portfolio.slice().sort((a,b)=>a[1]-b[1]), moat=port[0], ex=port.slice(-2).reverse();
  const exEn=ex.map(r=>r[0]+' ('+r[1]+' competitors)').join(' and '), exAr=ex.map(r=>r[0]+' ('+r[1]+' منافس)').join(' و');
  h+='</tbody></table><div class="geo-legend">'+(moat?t('EH\u2019s clearest moat is '+moat[0]+' ('+esc(moat[2])+'), held by only '+moat[1]+' competitor'+(moat[1]===1?'':'s')+'. EH\u2019s most exposed lines are '+exEn+'. White-space licences may warrant pursuit if client demand exists.',
     'أوضح ميزة تنافسية لـ EH هي '+moat[0]+'، إذ لا يحمله سوى '+moat[1]+' منافس. وأكثر خطوط EH عرضة للمنافسة: '+exAr+'. وقد تستحق تراخيص الفرص غير المستغلة السعي إليها إذا وُجد طلب من العملاء.'):'')+'</div>';
  document.getElementById('licView').innerHTML=h;
}

"""
block(S, "function buildLicenceMap(){", "function selByName(", fix_nl(S, NEW_LIC), 'bug',
      'maps-17/14: Licence Map bars proportional, "most exposed" sentence computed, Arabic')

# ---- maps-14 / maps-15a schematic map
rep(S, "PROV.forEach(function(p){ inner+='<path d=\"'+p.d+'\" fill=\"#F6F1E2\" stroke=\"#C9B98E\" stroke-width=\"1.4\"><title>'+p.n+' Province</title></path>'; });",
       "PROV.forEach(function(p){ inner+='<path d=\"'+p.d+'\" fill=\"#F6F1E2\" stroke=\"#C9B98E\" stroke-width=\"1.4\"><title>'+t(p.n+' Province','منطقة '+provL(p.n))+'</title></path>'; });",
    'i18n', 'maps-14: schematic province tooltips')
rep(S, "font-weight=\"600\" fill=\"#9A8C66\" style=\"pointer-events:none\">'+p.n+'</text>'; });",
       "font-weight=\"600\" fill=\"#9A8C66\" style=\"pointer-events:none\">'+provL(p.n)+'</text>'; });", 'i18n', 'maps-14: schematic province labels')
rep(S, "fill=\"#8A7A50\" style=\"pointer-events:none\">'+c+'</text>'; });", "fill=\"#8A7A50\" style=\"pointer-events:none\">'+cityL(c)+'</text>'; });",
    'i18n', 'maps-14: schematic city labels')
rep(S, "font-size=\"10.5\" fill=\"#9A8C66\">'+rg+' · 0</text>'; return; }", "font-size=\"10.5\" fill=\"#9A8C66\">'+regL(rg)+' · 0</text>'; return; }",
    'i18n', 'maps-14: schematic empty-region labels')
rep(S, "<title>'+rg+' — '+g.opps+' tender(s) delivered here'+(g.opp_value?', SAR '+Math.round(g.opp_value).toLocaleString():'')+(wr!=null?'; EH win rate '+wr+'%':'')+'\\n('+g.competitors+' competitors, '+g.clients+' clients based in region)</title>",
       "<title>'+regL(rg)+' — '+t(g.opps+' tender(s) delivered here'+(g.opp_value?', SAR '+Math.round(g.opp_value).toLocaleString():'')+(wr!=null?'; EH win rate '+wr+'%':'')+'\\n('+g.competitors+' competitors, '+g.clients+' clients based in region)',g.opps+' منافسة تُنفَّذ هنا'+(g.opp_value?'، '+Math.round(g.opp_value).toLocaleString()+' ريال':'')+(wr!=null?'؛ نسبة فوز EH '+wr+'%':'')+'\\n('+g.competitors+' منافساً و'+g.clients+' عميلاً مقرهم في المنطقة)')+'</title>",
    'i18n', 'maps-14: schematic bubble tooltips')
rep(S, "font-weight=\"700\" fill=\"#2A3A45\">'+rg+'</text></g>';", "font-weight=\"700\" fill=\"#2A3A45\">'+regL(rg)+'</text></g>';", 'i18n', 'maps-14: schematic bubble labels')
rep(S, "  inner+=ehMark(39.0,22.75,'Rabigh','EH branch');\r\n  inner+=ehMark(39.18,21.5,'Jeddah','EH headquarters');\r\n  inner+=ehMark(46.72,24.63,'Riyadh','EH admin office');",
       "  inner+=ehMark(39.0,22.75,cityL('Rabigh'),t('EH branch','فرع EH'));\r\n  inner+=ehMark(39.18,21.5,cityL('Jeddah'),t('EH headquarters','المقر الرئيسي لـ EH'));\r\n  inner+=ehMark(46.72,24.63,cityL('Riyadh'),t('EH admin office','المكتب الإداري لـ EH'));",
    'i18n', 'maps-14: schematic EH markers')
rep(S, "<title>'+esc(n.n)+' \\u2014 '+n.tier+(n.sc!=null?' \\u00b7 score '+(Math.round(n.sc*10)/10):'')+(n.typ?' \\u00b7 '+esc(n.typ):'')+'\\n'+(L.approx?'Region-level position (city not recorded): '+esc(n.rg):'HQ: '+esc(k))+(n.bid?'\\nBids against EH':'')+'</title>",
       "<title>'+esc(n.n)+' \\u2014 '+tierL(n.tier)+(n.sc!=null?t(' \\u00b7 score ',' \\u00b7 الدرجة ')+(Math.round(n.sc*10)/10):'')+(n.typ?' \\u00b7 '+esc(catL(n.typ)):'')+'\\n'+(L.approx?t('Region-level position (city not recorded): ','موقع على مستوى المنطقة (المدينة غير مسجلة): ')+esc(regL(n.rg)):t('HQ: ','المقر: ')+esc(cityL(k)))+(n.bid?t('\\nBids against EH','\\nتقدّم ضد EH'):'')+'</title>",
    'i18n', 'maps-14: schematic HQ pin tooltips')
rep(S, "    if(ok2.length) geoOutside=ok2.map(function(k){return k+' '+outs[k];}).join(' \\u00b7 ');",
       "    if(ok2.length) geoOutside=ok2.map(function(k){return regL(cityL(k))+' '+outs[k];}).join(' \\u00b7 ');", 'i18n', 'maps-14: schematic "outside map" list')

NEW_GEO_H = r"""  /* patch_audit_maps.py: the national-vs-regional sentence is computed from this split (maps-15a); text follows the language (maps-14) */
  const natwr=NAT.awarded?Math.round(100*NAT.eh_won/NAT.awarded):null, regOpps=Object.values(R).reduce((a,g)=>a+g.opps,0), allOpps=NAT.opps+regOpps;
  let h='<div class="biz-sec">'+t('Saudi map — tender delivery + Tier 1/2 headquarters','خريطة السعودية — مواقع تنفيذ المنافسات ومقار شركات الفئتين 1 و2')+'</div>';
  // National + GCC summary cards
  h+='<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px">'+
    '<div class="biz-kpi" style="flex:1;min-width:220px"><div class="v" style="font-size:18px">'+NAT.opps+t(' tenders · SAR ',' منافسة · ')+fmtM(NAT.opp_value)+t('',' ريال')+'</div><div class="l">'+t('National / multi-site contracts (no single delivery location)','عقود وطنية أو متعددة المواقع (بلا موقع تنفيذ واحد)')+(natwr!=null?t(' · EH win ',' · فوز EH ')+natwr+'%':'')+'</div></div>'+
    '<div class="biz-kpi" style="flex:1;min-width:160px"><div class="v" style="font-size:18px">'+regOpps+t(' tenders',' منافسة')+'</div><div class="l">'+t('Localised to a specific region (shown on map)','مرتبطة بمنطقة محددة (معروضة على الخريطة)')+'</div></div>'+
  '</div>';
  h+='<div style="display:flex;gap:16px;align-items:center;margin:2px 0 8px;font-size:12px;color:#51626D;flex-wrap:wrap"><label style="cursor:pointer"><input type="checkbox" '+(geoLayers.tenders?'checked':'')+' onchange="geoLayers.tenders=this.checked;buildGeoMap()"> '+t('Tender delivery bubbles','فقاعات مواقع تنفيذ المنافسات')+'</label><label style="cursor:pointer"><input type="checkbox" '+(geoLayers.hq?'checked':'')+' onchange="geoLayers.hq=this.checked;buildGeoMap()"> '+t('Tier 1/2 HQ pins','دبابيس مقار الفئتين 1 و2')+'</label><span style="margin-inline-start:auto"><span style="color:#D4A017;font-weight:800">\u25cf</span> '+tierL('Tier 1')+' \u00b7 <span style="color:#5A95C8;font-weight:800">\u25cf</span> '+tierL('Tier 2')+' \u00b7 <span style="color:#C0392B;font-weight:800">\u25cb</span> '+t('red ring = bids vs EH','الحلقة الحمراء = تقدّم ضد EH')+'</span></div>';
  h+='<div style="position:relative">'+svg+
    '<div style="position:absolute;top:8px;right:8px;display:flex;flex-direction:column;gap:5px">'+
    '<button class="zbtn" onclick="geoZoom(1.4)">+</button><button class="zbtn" onclick="geoZoom(1/1.4)">&minus;</button><button class="zbtn" onclick="geoReset()">&#10227;</button></div></div>';
  h+='<div class="geo-legend">'+t('Bubble size = number of tenders <b>delivered</b> in that region (parsed from client &amp; project titles). Colour = EH win rate there (green ≥50%, red &lt;50%, blue = no recorded outcome). '+NAT.opps+' of '+allOpps+' tenders have no single delivery site (national or multi-site contracts, e.g. SEC, NCVC, ministries) — summarised in the card above rather than pinned to Riyadh. Scroll to zoom, drag to pan.',
      'حجم الفقاعة = عدد المنافسات <b>المنفَّذة</b> في تلك المنطقة (مستخرج من أسماء العملاء والمشاريع). اللون = نسبة فوز EH فيها (أخضر ≥50%، أحمر &lt;50%، أزرق = لا نتيجة مسجلة). '+NAT.opps+' من أصل '+allOpps+' منافسة بلا موقع تنفيذ واحد (عقود وطنية أو متعددة المواقع، مثل الشركة السعودية للكهرباء والمركز الوطني لتنمية الغطاء النباتي والوزارات) — ملخصة في البطاقة أعلاه بدلاً من تثبيتها على الرياض. مرّر للتكبير واسحب للتنقل.')+
    (geoLayers.hq?t(' HQ pins: gold = Tier 1, blue = Tier 2; red ring = has bid against EH; pins cluster in a spiral around each city \u2014 click any pin to open the company profile. Companies without a recorded city sit at their region centre.',' دبابيس المقار: الذهبي = الفئة 1، الأزرق = الفئة 2؛ الحلقة الحمراء = تقدّم ضد EH؛ تتجمع الدبابيس حلزونياً حول كل مدينة — انقر أي دبوس لفتح ملف الشركة. الشركات التي لا تُسجَّل مدينتها توضع في مركز منطقتها.'):'')+'</div>'+
    (geoOutside?'<div style="font-size:11px;color:#5A6B76;margin-top:4px">'+t('Outside map extent: ','خارج حدود الخريطة: ')+geoOutside+'</div>':'');
  // region table (tenders + stakeholder context)
  h+='<div class="biz-sec">'+t('Regional breakdown — tenders delivered & stakeholder base','التوزيع الإقليمي — المنافسات المنفَّذة وقاعدة الأطراف')+'</div><table class="btab"><thead><tr><th>'+t('Region','المنطقة')+'</th><th>'+t('Tenders delivered','المنافسات المنفَّذة')+'</th><th>'+t('Tender value','قيمة المنافسات')+'</th><th>'+t('EH win rate','نسبة فوز EH')+'</th><th>'+t('Competitors based','منافسون مقرهم فيها')+'</th><th>'+t('Clients based','عملاء مقرهم فيها')+'</th></tr></thead><tbody>';
  const order=['Jeddah','Makkah City','Rabigh','Other Makkah Region','Madinah Region','Riyadh','Qassim Region','Eastern Province','Tabuk Region','Hail Region','Al Jawf Region','Northern Borders Region','Southern Region'];
  order.forEach(rg=>{const g=R[rg]; if(!g)return; const wr=g.awarded?Math.round(100*g.eh_won/g.awarded)+'%':'—';
    h+='<tr><td><b>'+esc(regL(rg))+'</b></td><td>'+g.opps+'</td><td>'+(g.opp_value?fmtSAR(g.opp_value):'—')+'</td><td>'+wr+'</td><td>'+g.competitors+'</td><td>'+g.clients+'</td></tr>';});
  h+='<tr style="background:#FBF6EC"><td><b>'+t('National / multi-site','وطنية / متعددة المواقع')+'</b></td><td>'+NAT.opps+'</td><td>'+(NAT.opp_value?fmtSAR(NAT.opp_value):'—')+'</td><td>'+(natwr!=null?natwr+'%':'—')+'</td><td colspan="2" style="color:var(--ink-soft)">'+t('delivered Kingdom-wide','تُنفَّذ على مستوى المملكة')+'</td></tr>';
  h+='<tr style="color:var(--ink-soft)"><td>'+t('GCC / International (context)','الخليج / دولي (للسياق)')+'</td><td>—</td><td>—</td><td>—</td><td>'+GCC.competitors+'</td><td colspan="1">'+(GCC.total-GCC.competitors)+'</td></tr>';
  h+='</tbody></table>';
"""
block(S, "  let h='<div class=\"biz-sec\">Saudi map — tender delivery + Tier 1/2 headquarters</div>';",
      "  document.getElementById('geoModeWrap').innerHTML=h;", fix_nl(S, NEW_GEO_H), 'copy',
      'maps-15a/14: schematic map — "N of M tenders" computed from the split; cards, legend and table in Arabic')
GEO_L10N = r"""const AR_PROV={'Eastern':'الشرقية','Northern Borders':'الحدود الشمالية','Al-Jowf':'الجوف','Najran':'نجران',"'Asir":'عسير','Jazan':'جازان','Tabuk':'تبوك','Al Madinah':'المدينة المنورة','Makkah':'مكة المكرمة','Riyadh':'الرياض','Al-Qassim':'القصيم',"Ha'il":'حائل','Al-Baha':'الباحة'};
const AR_CITY={'Riyadh':'الرياض','Jeddah':'جدة','Dammam':'الدمام','Jubail':'الجبيل','Khobar':'الخبر','Al-Khobar':'الخبر','Dhahran':'الظهران','Makkah':'مكة المكرمة','Madinah':'المدينة المنورة','Yanbu':'ينبع','Rabigh':'رابغ','Tabuk':'تبوك','Buraydah':'بريدة','Al Kharj':'الخرج','Jazan':'جازان','Abha':'أبها','Hafr Al Batin':'حفر الباطن','Al Ahsa':'الأحساء','NEOM':'نيوم','Neom':'نيوم','Dubai':'دبي','Abu Dhabi':'أبوظبي','Manama':'المنامة','Bahrain':'البحرين','Sharjah':'الشارقة','Al Qassim':'القصيم','Unaizah':'عنيزة','Al Qatif':'القطيف','Khamis Mushait':'خميس مشيط'};
function provL(p){return LNG==='ar'?(AR_PROV[p]||p):p;}
function cityL(c){return LNG==='ar'?(AR_CITY[c]||c):c;}
let geoV={k:1,x:0,y:0}, geoEl=null, geoDrag=null;"""
rep(S, "let geoV={k:1,x:0,y:0}, geoEl=null, geoDrag=null;", fix_nl(S, GEO_L10N), 'i18n', 'maps-14: Arabic province and city names for the schematic map')

# ---- List View count sentence (maps-14) + type column
OLD_LC = "let h='<div class=\"lcount\"><b>'+rows.length.toLocaleString()+'</b> companies shown — ranked by <b>Total Score (v2)</b> = capability 0–100 + strategic backing 0–25 + bids-vs-EH +15; for EH Clients the Score column shows the <b>EH Relationship Score</b> instead (“—” = not a scored/licensed company; low-confidence rows are floored, never neutral-filled) · click any row for detail · click a column to re-sort</div>';"
NEW_LC = "let h='<div class=\"lcount\">'+t('<b>'+rows.length.toLocaleString()+'</b> companies shown — ranked by <b>Total Score (v2)</b> = capability 0–100 + strategic backing 0–25 + bids-vs-EH +15; for EH Clients the Score column shows the <b>EH Relationship Score</b> instead (“—” = not a scored/licensed company; low-confidence rows are floored, never neutral-filled) · click any row for detail · click a column to re-sort','<b>'+rows.length.toLocaleString()+'</b> شركة معروضة — مرتبة حسب <b>الدرجة الكلية (الإصدار الثاني)</b> = القدرة 0–100 + الإسناد الاستراتيجي 0–25 + التقدّم ضد EH ‎+15؛ ولعملاء EH يعرض عمود الدرجة <b>درجة علاقة EH</b> بدلاً منها («—» = شركة غير مُقيّمة أو غير مرخّصة؛ الصفوف منخفضة الموثوقية توضع عند الحد الأدنى ولا تُملأ بقيم محايدة) · انقر أي صف للتفاصيل · انقر عنوان العمود لإعادة الترتيب')+'</div>';"
rep(S, OLD_LC, NEW_LC, 'i18n', 'maps-14: List View count sentence in Arabic')
rep(S, "     '<td>'+esc(n.typ||'—')+'</td>'+", "     '<td>'+esc(n.typ?catL(n.typ):'—')+'</td>'+", 'i18n', 'maps-14: List View company type in Arabic')

# ---- maps-18 modal close as a button + Escape; maps-07/12 methodology / guide text
rep(S, '<span class="x" onclick="closeModal()">✕</span>', '<button type="button" class="x" onclick="closeModal()" aria-label="Close / إغلاق">✕</button>', 'a11y',
    'maps-18: modal close mark is a keyboard-reachable button', count=5)
rep(S, "covering all Saudi administrative regions where stakeholders are present — Jeddah, Makkah City, Rabigh, Other Makkah, Madinah, Riyadh, Qassim, Eastern Province, Tabuk, Hail, Al Jawf, Northern Borders and Southern regions — plus GCC/International.",
       "covering all Saudi administrative regions where stakeholders are present — Jeddah, Makkah City, Rabigh, Other Makkah, Madinah, Riyadh, Qassim, Eastern Province, Tabuk, Hail, Al Jawf, Northern Borders and Southern regions — plus GCC/International, and a <b>Region not recorded</b> slice for companies whose region is not yet known.",
    'copy', 'maps-07: guide mentions the "Region not recorded" slice')
rep(S, "<p>كل شريحة منطقة سعودية (أو الخليج/دولي).", "<p>كل شريحة منطقة سعودية (أو الخليج/دولي)، وهناك شريحة «المنطقة غير مسجلة» للشركات التي لم تُعرف منطقتها بعد.",
    'copy', 'maps-07: Arabic guide mentions the "Region not recorded" slice')
rep(S, "Companies whose category could not be identified, and companies whose location could not be verified, were <b>removed from the map</b> (226 records,",
       "In an earlier clean-up, companies whose category could not be identified, and companies whose location could not be verified, were <b>removed from the map</b> (226 records,",
    'copy', 'maps-07: the 226-record removal is described as an earlier clean-up')
rep(S, "National government bodies without a recorded location were assigned to Riyadh (federal headquarters convention). The map contains no \"Unknown\" region group. Duplicated company records were merged.",
       "National government bodies without a recorded location were assigned to Riyadh (federal headquarters convention). Companies that remain without a recorded region are kept: they count in every total and are drawn in their own <b>“Region not recorded”</b> slice of the wheel and bar of the Regional View (<span data-live=\"norg\"></span> companies at present). Duplicated company records were merged.",
    'copy', 'maps-07: Methodology no longer claims there is no unknown-region group; states the live count')
rep(S, "Bid counts were derived from the EH bid log; the top challengers are Evara Earth (10), Environmental Experts Contracting and ESCO (7 each).",
       "Bid counts come from the EH bid tracker and are refreshed at each publish; the most frequent challengers at present are <span data-live=\"topch\"></span>.",
    'copy', 'maps-12: Methodology names the current top challengers from the data')
rep(S, "<br><b>القدرة:</b> اتساع الخدمات حتى 30 · القوى العاملة 0–25 · المواقع 0–25 · المشاريع الكبرى +10 · متعددة الجنسيات +10، بسقف 100.",
       "<br><b>القدرة (الإصدار الثاني، سبتمبر 2026):</b> تداخل الخدمات مع خدمات EH 35 · مرات المواجهة مع EH في العطاءات 25 · الإسناد الاستراتيجي 15 · فئة القوى العاملة 10 · المشاريع الكبرى 7 · المواقع 5 · العمليات متعددة الجنسيات 3، بسقف 100.",
    'copy', 'maps-12: Arabic Methodology describes the current (v2) capability weights')
rep(S, "البيانات المفقودة تُملأ بقيم محايدة مع مؤشر موثوقية (مرتفع/متوسط/منخفض).",
       "لا تُملأ البيانات المفقودة بقيم محايدة: حين تكون موثوقية البيانات منخفضة لا يُحتسب إلا ما ثبت بالدليل (مرات المواجهة في العطاءات وسجلات التراخيص)، ويبقى الباقي عند الحد الأدنى للشركات الصغيرة. ويظهر مؤشر الموثوقية (مرتفع/متوسط/منخفض) في كل ملف.",
    'copy', 'maps-12: Arabic Methodology no longer says missing data is neutral-filled')
rep(S, "تصنيف <b>منافس نشط</b> يشترط ترخيصاً واحداً مشتركاً على الأقل مع EH.</p>",
       "تصنيف <b>منافس نشط</b> يشترط ترخيصاً واحداً مشتركاً على الأقل مع EH.</p><h4>المناطق وأكثر المنافسين تكراراً</h4><p>تبقى الشركات التي لا تُسجَّل لها منطقة ضمن الخريطة: تُحتسب في جميع المجاميع وتظهر في شريحة خاصة باسم «المنطقة غير مسجلة» في العجلة وفي العرض الإقليمي (<span data-live=\"norg\"></span> شركة حالياً). وتُستمد أعداد العطاءات من متتبع عطاءات EH وتُحدَّث عند كل نشر؛ وأكثر المنافسين تقدّماً حالياً: <span data-live=\"topch\"></span>.</p>",
    'copy', 'maps-07/12: Arabic Methodology states the region-not-recorded count and current top challengers')
NEW_MODAL = r"""function liveFill(el){   // patch_audit_maps.py: numbers in the Methodology are counted from the map, not typed
  el.querySelectorAll('[data-live]').forEach(function(s){var k=s.getAttribute('data-live');
    if(k==='norg')s.textContent=NODES.filter(function(n){return n.rg==='\u2014';}).length.toLocaleString('en-US');
    if(k==='topch'){var a=NODES.filter(function(n){return n.bc>0;}).sort(function(x,y){return y.bc-x.bc;}).slice(0,3);
      s.textContent=a.length?a.map(function(n){return n.n+' ('+n.bc+')';}).join(t(', ','، ')):t('none recorded','لا يوجد');}
  });
}
function openModal(k){var c=document.getElementById('modalCard');c.innerHTML=k==='guide'?(LNG==='ar'?GUIDE_AR:GUIDE):(k==='method'?(LNG==='ar'?METHOD_AR:METHOD):licGlossary());liveFill(c);document.getElementById('modal').style.display='flex';var x=c.querySelector('button.x');if(x)try{x.focus();}catch(e){}}
function closeModal(){document.getElementById('modal').style.display='none'}
document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;var m=document.getElementById('modal');if(m&&m.style.display==='flex')closeModal();var lm=document.getElementById('leafModal');if(lm)lm.classList.remove('on');});   // maps-18"""
block(S, "function openModal(k){", "\r\ndocument.getElementById('modal').addEventListener('click'", fix_nl(S, NEW_MODAL), 'a11y',
      'maps-18/07/12: Escape closes modals; live counts filled into the Methodology')

# ---- maps-14 dark button label
rep(S, "</svg>Light':'<svg style=\"width:14px;height:14px;vertical-align:-2px;margin-inline-end:5px\" aria-hidden=\"true\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M21 12.8A8.5 8.5 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z\"/></svg>Dark';",
       "</svg>'+t('Light','فاتح'):'<svg style=\"width:14px;height:14px;vertical-align:-2px;margin-inline-end:5px\" aria-hidden=\"true\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M21 12.8A8.5 8.5 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z\"/></svg>'+t('Dark','داكن');",
    'i18n', 'maps-14: Dark/Light button in Arabic')
rep(S, "resize();recompute();\r\nif(document.fonts",
       "resize();recompute();\r\ntry{var _hp=document.querySelector('header .titles p');if(_hp)_hp.textContent=hdrText();}catch(e){}   // maps-11: counted at load (the sync step can add companies)\r\nif(document.fonts",
    'copy', 'maps-11: header count set from the data at load')

# ---- maps-01 / 14 / 16 Leaflet: pins built from NODES
src_line_i = TXT[S].find('const LSTAKE={"type":"FeatureCollection"'); src_line_j = TXT[S].find('\r\n', src_line_i)
LST = json.loads(TXT[S][src_line_i + len('const LSTAKE='):src_line_j].rstrip(';'))
POS, SRC, RGS, LGEO = [], [], [], {}
def ix(lst, v):
    if v not in lst: lst.append(v)
    return lst.index(v)
for f in LST['features']:
    p = f['properties']; lng, lat = f['geometry']['coordinates']
    LGEO[p['n']] = [lng, lat, ix(POS, p['pos']), ix(SRC, p.get('src') or ''), ix(RGS, p.get('rg') or '')]
LGEO_JS = ('/* Saudi Map positions (patch_audit_maps.py, maps-01). Everything else on the map is read live from NODES. '
           'LGEO: company name -> [longitude, latitude, position type (LGEO_POS), source (LGEO_SRC), region when the position was set (LGEO_RG)]. */\r\n'
           'const LGEO_POS=' + json.dumps(POS, ensure_ascii=False) + ', LGEO_SRC=' + json.dumps(SRC, ensure_ascii=False) + ', LGEO_RG=' + json.dumps(RGS, ensure_ascii=False) + ';\r\n'
           'const LGEO=' + json.dumps(LGEO, ensure_ascii=False, separators=(',', ':')) + ';')
if src_line_i < 0:
    _log(S, 'block', 'const LSTAKE=', '', 'data', 'maps-01: LSTAKE', 0, False)
else:
    TXT[S] = TXT[S][:src_line_i] + LGEO_JS + TXT[S][src_line_j:]
    _log(S, 'block', 'const LSTAKE={… 2,808 frozen features, %d bytes}' % (src_line_j - src_line_i), 'const LGEO={… positions only, %d bytes}' % len(LGEO_JS),
         'data', 'maps-01: the frozen Leaflet company copy is replaced by a position lookup (%d names)' % len(LGEO), 1, True)

NEW_BUILD = r"""const LREGC={'Jeddah':[39.2,21.5],'Makkah City':[39.86,21.42],'Rabigh':[39.0,22.75],'Other Makkah Region':[41.3,20.4],'Madinah Region':[39.6,24.6],'Riyadh':[46.7,24.7],'Qassim Region':[43.97,26.33],'Eastern Province':[49.9,26.4],'Tabuk Region':[36.6,28.4],'Hail Region':[41.7,27.5],'Al Jawf Region':[40.0,29.9],'Northern Borders Region':[41.5,30.6],'Southern Region':[42.6,18.4]};   // region centres [lng,lat]
let LSTAKE={type:'FeatureCollection',features:[]}, LNODE=[], LUNPLACED=0;
function leafFeat(n,ll,pos,src,site){
  return {type:'Feature',properties:{n:n.n,cat:n.cat,typ:n.typ||'',tier:n.tier||'',city:n.city||'',rg:n.rg||'',sc:n.sc==null?null:n.sc,cap:n.cap==null?null:n.cap,bk:n.bk||0,cf:n.cf||'\u2014',bid:!!n.bid,bc:n.bc||0,th:n.threat||'',own:n.own||'',act:n.act||'',pos:pos,src:src||'',site:site||''},geometry:{type:'Point',coordinates:[ll[0],ll[1]]}};
}
function leafBuild(){   // maps-01: one pin per map company, from the live data; position from LGEO, else the region centre
  var F=[],NN=[],un=0,at={};
  NODES.forEach(function(n){
    var g=LGEO[n.n],ll=null,pos='',src='';
    if(g){pos=LGEO_POS[g[2]];src=LGEO_SRC[g[3]];
      if(pos.indexOf('Estimated')===0&&LGEO_RG[g[4]]!==n.rg&&LREGC[n.rg]){ll=LREGC[n.rg];pos='Estimated (region centroid)';}   // region changed since the estimate
      else ll=[g[0],g[1]];}
    else if(LREGC[n.rg]){ll=LREGC[n.rg];pos='Estimated (region centroid)';src='EH stakeholder data (no position recorded)';}
    if(!ll){un++;return;}
    at[n.n]=F.length;F.push(leafFeat(n,ll,pos,src));NN.push(n);
  });
  Object.keys(GEO_SITES).forEach(function(nm){var g=GEO_SITES[nm];
    if(at[nm]!=null){var p=F[at[nm]];p.geometry.coordinates=[g[1],g[0]];p.properties.pos='Verified site';p.properties.site=g[2]||'';return;}
    var n=NODES.find(function(x){return x.n===nm;});
    if(n){if(un>0&&!LREGC[n.rg]&&!LGEO[n.n])un--;F.push(leafFeat(n,[g[1],g[0]],'Verified site','GEO_SITES',g[2]));NN.push(n);return;}
    F.push(leafFeat({n:nm,cat:g[3]||'Clients / Potential Clients',city:(g[2]||'').split('\u2014')[0].trim(),cf:'High'},[g[1],g[0]],'Verified site','GEO_SITES',g[2]));NN.push(null);
  });
  LSTAKE={type:'FeatureCollection',features:F}; LNODE=NN; LUNPLACED=un;
}
function posL(s){s=s||'';if(LNG!=='ar')return s;if(/^City/.test(s))return 'على مستوى المدينة';if(/^Estimated/.test(s))return 'موقع تقديري';if(/^HQ/.test(s))return 'مقر رئيسي (تحقق بحثي)';if(/^Verified/.test(s))return 'موقع مؤكد';return s;}

"""
block(S, "(function(){\r\n  var byName={}; LSTAKE.features.forEach(", "const LPROV=", fix_nl(S, NEW_BUILD), 'bug',
      'maps-01: Leaflet features built from NODES at runtime (GEO_SITES still corrects positions)')
rep(S, "const LF={prov:'all',t1:true,t2:true,cats:null,bidOnly:false,minSc:0,confs:null};",
       "const LF={prov:'all',tiers:null,cats:null,bidOnly:false,minSc:0,confs:null};   // tiers: every tier present (maps-16)",
    'bug', 'maps-16: Leaflet tier filter covers every tier')
rep(S, "t('Saudi map \\u2014 Tier 1/2 stakeholders, roads & regions','خريطة السعودية — أطراف الفئتين 1/2، الطرق والمناطق')",
       "t('Saudi map \\u2014 stakeholders, roads & regions','خريطة السعودية — الأطراف والطرق والمناطق')",
    'copy', 'maps-16: Leaflet title no longer says "Tier 1/2" (all tiers are pinned)')

NEW_SHELL = r"""function leafShell(){
  leafBuild();   // maps-01: same live data as the rest of the page
  var FS=LSTAKE.features, nTot=FS.length, cnt=function(re){return FS.filter(function(f){return re.test(f.properties.pos);}).length;};
  var nHQ=cnt(/^(HQ|Verified)/), nCity=cnt(/^City/), nEst=cnt(/^Estimated/), fmt=function(v){return v.toLocaleString('en-US');};
  var w=document.getElementById('geoModeWrap');
  var about=LNG==='ar'?
    '<b>مصادر البيانات.</b> الأسماء والفئات والمستويات والدرجات وسجلات العطاءات في هذه الخريطة تُقرأ من بيانات الأطراف الحية نفسها التي تستخدمها بقية التبويبات، وتُحدَّث من متتبع العطاءات عند كل نشر. مواقع الدبابيس مأخوذة من قاعدة بيانات الأطراف لدى EH ومن جولات البحث عن المواقع (2026). تتبع الدرجات نموذج الإصدار الثاني الموضح في المنهجية (القدرة 0–100 + الإسناد الاستراتيجي 0–25 + التعرض للعطاءات ‎+15). الخريطة الأساسية © مساهمو OpenStreetMap. حدود المناطق ومحاور الطرق السريعة: Natural Earth 10m (ملكية عامة).<br><br>'+
    '<b>دقة المواقع.</b> '+fmt(nHQ)+' دبوساً في مقر رئيسي تم التحقق منه بحثياً أو موقع مؤكد؛ و'+fmt(nCity)+' على مستوى المدينة؛ و'+fmt(nEst)+' بموقع تقديري (لا عنوان مسجلاً — موضوعة في مركز مدينتها أو منطقتها) وتظهر باهتة بعلامة «تقديري». و'+fmt(LUNPLACED)+' شركة بلا منطقة مسجلة، أو مقرها خارج السعودية دون موقع على الخريطة، فلا تُثبَّت هنا وتبقى في عرض القائمة.<br><br>'+
    '<b>فجوات معروفة.</b> بيانات الطرق من Natural Earth لا تحمل أرقام الطرق في هذه المنطقة — الأرقام المعروضة مواضع تقريبية لمنتصف المحاور؛ ويظهر الترقيم الدقيق والطرق الدائرية للمدن على خريطة OSM الأساسية عند التكبير. وتُعلَّم فجوات بيانات الموظفين والمواقع لكل شركة بموثوقية بيانات منخفضة أو متوسطة.<br><br>'+
    '<b>الخطوات التالية.</b> التحقق الميداني من عناوين المقار للمواقع التقديرية ('+fmt(nEst)+')؛ ومطابقة نطاق التراخيص مع سجل المركز الوطني لإدارة النفايات.<br><br>'+
    '<b>النشر.</b> يعمل هذا الملف على أي استضافة ثابتة. يحتاج تبويب خريطة السعودية إلى الإنترنت لبلاطات OSM ومكتبة Leaflet؛ وبقية التبويبات تعمل دون اتصال.'
  : '<b>Data sources.</b> Names, categories, tiers, scores and bid records on this map are read from the same live stakeholder data as every other tab, refreshed from the bid tracker at each publish. Pin positions come from the EH stakeholder database and the 2026 location research passes. Scores follow the v2 model described in Methodology (capability 0\u2013100 + strategic backing 0\u201325 + bid exposure +15). Base map \u00a9 OpenStreetMap contributors. Province boundaries and highway corridors: Natural Earth 10m (public domain).<br><br>'+
    '<b>Position confidence.</b> '+fmt(nHQ)+' pins are at a researched head office or verified site; '+fmt(nCity)+' are at city level; '+fmt(nEst)+' have an estimated position (no address recorded \u2014 placed at their city or region centre), drawn faded and marked <i>Estimated</i>. '+fmt(LUNPLACED)+' companies have no recorded region, or are based outside Saudi Arabia without a mapped location, and are not pinned; they remain in the List View.<br><br>'+
    '<b>Known gaps.</b> Natural Earth road geometry carries no route numbers in this region \u2014 the numbered labels shown are approximate corridor midpoints; exact numbering and city ring roads are visible on the OSM base map at closer zoom. Employee/site data gaps are flagged per company as data confidence Low/Medium.<br><br>'+
    '<b>Next steps.</b> Ground-truth head-office addresses for the '+fmt(nEst)+' estimated positions; verify licence footprints against the MWAN registry.<br><br>'+
    '<b>Deploy.</b> This single HTML file runs on any static host (GitHub Pages, Netlify). The Saudi Map tab needs internet for OSM tiles and the Leaflet library; all other tabs are fully offline.';
  w.innerHTML='<div id="leafBanner">'+t('<b>Disclaimer:</b> stakeholder data is compiled from the EH stakeholder database and publicly available sources as of 2026. Coordinates are city-level (or region-estimated where marked), and scores, ownership and operational details may be approximate or outdated. Verify critical data with official Saudi regulatory bodies (MEWA, NCEC, MWAN) before making operational decisions.','<b>تنويه:</b> بيانات الأطراف مجمعة من قاعدة بيانات EH ومصادر عامة حتى 2026. الإحداثيات على مستوى المدينة (أو تقدير المنطقة حيث يُذكر)، وقد تكون الدرجات والملكية والتفاصيل تقريبية أو قديمة. تحقق من البيانات الحرجة لدى الجهات الرسمية (وزارة البيئة، المركز الوطني للرقابة، مركز إدارة النفايات) قبل اتخاذ قرارات تشغيلية.')+'</div>'+
  '<div id="leafBar"><button class="leafbtn" onclick="leafFull()">'+t('\u26f6 Fullscreen','⛶ ملء الشاشة')+'</button><button class="leafbtn" onclick="leafExport(\'geojson\')">\u2b07 GeoJSON</button><button class="leafbtn" onclick="leafExport(\'csv\')">\u2b07 CSV</button><button class="leafbtn" onclick="document.getElementById(\'leafModal\').classList.add(\'on\')">'+t('\u24d8 About & data notes','ⓘ حول وملاحظات البيانات')+'</button><span style="margin-inline-start:auto;font-size:12px;color:#51626D"><span id="leafCount">\u2014</span>'+t(' of '+fmt(nTot)+' pinned companies shown',' من '+fmt(nTot)+' شركة مثبّتة على الخريطة')+'</span></div>'+
  (LUNPLACED?'<div class="geo-legend" style="margin:0 0 6px">'+t(fmt(LUNPLACED)+' companies have no recorded region, or are based outside Saudi Arabia without a mapped location, so they are not pinned here; they are in the List View.',fmt(LUNPLACED)+' شركة بلا منطقة مسجلة، أو مقرها خارج السعودية دون موقع على الخريطة، لذا لا تُثبَّت هنا؛ وهي موجودة في عرض القائمة.')+'</div>':'')+
  '<div id="leafWrap"><div id="leafSide"></div><div id="leafMap"></div></div>'+
  '<div id="leafModal" onclick="if(event.target===this)this.classList.remove(\'on\')"><div class="box"><h3 style="margin-top:0">'+t('About this map','حول هذه الخريطة')+'</h3>'+about+
  '<div style="text-align:end;margin-top:10px"><button class="leafbtn" onclick="document.getElementById(\'leafModal\').classList.remove(\'on\')">'+t('Close','إغلاق')+'</button></div></div></div>';
  leafSidebar();
  loadLeaflet(leafStart,function(){
    document.getElementById('leafMap').innerHTML='<div style="padding:40px;text-align:center;color:#5A6B76">'+t('Could not load the map library (no internet connection?).','تعذّر تحميل مكتبة الخريطة (لا يوجد اتصال بالإنترنت؟).')+'<br><br><button class="leafbtn" onclick="setGeoMode(\'svg\')">'+t('Open the offline schematic map instead','افتح الخريطة التخطيطية دون اتصال بدلاً منها')+'</button></div>';
  });
}
"""
block(S, "function leafShell(){", "function loadLeaflet(ok,fail){", fix_nl(S, NEW_SHELL), 'copy',
      'maps-01/16/14: Leaflet header, unpinned count and About computed from the live data; Arabic About')

NEW_SIDE = r"""function leafSidebar(){
  var provs={},cats={},tiers={};LSTAKE.features.forEach(function(f){var p=f.properties;provs[p.rg||'\u2014']=1;cats[p.cat]=1;tiers[p.tier||'']=1;});
  if(!LF.cats){LF.cats={};Object.keys(cats).forEach(function(c){LF.cats[c]=true;});}
  if(!LF.confs){LF.confs={'High':true,'Medium':true,'Low':true,'\u2014':true};}
  if(!LF.tiers){LF.tiers={};Object.keys(tiers).forEach(function(k){LF.tiers[k]=true;});}
  var TORD=['Tier 1','Tier 2','Tier 3','Tier 4','GOV','EH',''];
  var s='<div style="font-size:10.5px;color:#51626D;margin:2px 0 8px;line-height:1.8"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#1A5FAB;vertical-align:-1px"></span> '+t('Verified site / head office','موقع مؤكد / مقر رئيسي')+' &nbsp; <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#1A5FAB;opacity:.55;vertical-align:-1px"></span> '+t('Estimated position','موقع تقديري')+'</div>'+'<h4>'+t('Region / province','المنطقة')+'</h4><select onchange="LF.prov=this.value;leafRefresh()"><option value="all">'+t('All regions','كل المناطق')+'</option>'+Object.keys(provs).sort().map(function(p){return '<option value="'+esc(p)+'" '+(LF.prov===p?'selected':'')+'>'+esc(regL(p))+'</option>';}).join('')+'</select>';
  s+='<h4>'+t('Tier','الفئة')+'</h4>'+TORD.filter(function(k){return tiers[k];}).map(function(k){return '<label><input type="checkbox" '+(LF.tiers[k]!==false?'checked':'')+' onchange="LF.tiers[\''+k+'\']=this.checked;leafRefresh()"> '+(k?esc(tierL(k)):t('No tier recorded','بلا فئة مسجلة'))+'</label>';}).join('');
  s+='<h4>'+t('Category','الفئة (التصنيف)')+'</h4>'+Object.keys(cats).sort().map(function(c){return '<label><input type="checkbox" '+(LF.cats[c]?'checked':'')+' onchange="LF.cats[\''+c.replace(/'/g,"\\'")+'\']=this.checked;leafRefresh()"><span style="width:9px;height:9px;border-radius:50%;background:'+(CAT_COL[c]||'#7A8A99')+';display:inline-block"></span> '+esc(catS(c))+'</label>';}).join('');
  s+='<h4>'+t('Competitive','تنافسي')+'</h4><label><input type="checkbox" '+(LF.bidOnly?'checked':'')+' onchange="LF.bidOnly=this.checked;leafRefresh()">'+t(' Has bid against EH only',' من تقدم ضد EH فقط')+'</label>';
  s+='<h4>'+t('Min Total Score: ','الحد الأدنى للدرجة: ')+'<span id="leafScV">'+LF.minSc+'</span></h4><input type="range" min="0" max="120" step="5" value="'+LF.minSc+'" oninput="LF.minSc=+this.value;document.getElementById(\'leafScV\').textContent=this.value;leafRefresh()">';
  s+='<h4>'+t('Data confidence','موثوقية البيانات')+'</h4>'+['High','Medium','Low','\u2014'].map(function(c){return '<label><input type="checkbox" '+(LF.confs[c]?'checked':'')+' onchange="LF.confs[\''+c+'\']=this.checked;leafRefresh()"> '+(c==='\u2014'?t('Not scored','غير مُقيّم'):thrL(c))+'</label>';}).join('');
  s+='<h4>'+t('Layers','الطبقات')+'</h4><label><input type="checkbox" checked onchange="leafToggle(\'prov\',this.checked)">'+t(' Provincial boundaries',' حدود المناطق')+'</label><label><input type="checkbox" checked onchange="leafToggle(\'roads\',this.checked)">'+t(' Highway network',' شبكة الطرق السريعة')+'</label>';
  s+='<div style="margin-top:10px"><button class="leafbtn" onclick="leafReset()">'+t('Reset filters','إعادة ضبط المرشحات')+'</button></div>';
  s+='<h4>'+t('Legend','الدليل')+'</h4><div style="line-height:1.9">'+Object.keys(cats).sort().map(function(c){return '<span class="lchip" style="background:'+(CAT_COL[c]||'#7A8A99')+'">'+esc(catS(c))+'</span>';}).join('')+'<br>'+t('\u25cf large = Tier 1 \u00b7 \u25cf small = other tiers','\u25cf كبيرة = الفئة 1 \u00b7 \u25cf صغيرة = بقية الفئات')+'<br><span style="color:#C0392B;font-weight:800">\u25cb '+t('red ring','حلقة حمراء')+'</span> = '+t('bids against EH','تقدّم ضد EH')+'<br><span style="color:#C77B3B;font-weight:800">\u2014</span> '+t('expressway','طريق سريع')+' \u00b7 <span style="color:#B9A97E;font-weight:800">\u2014</span> '+t('primary road','طريق رئيسي')+'<br><span style="color:#8FA33F">\u25a1</span> '+t('province boundary','حدود منطقة')+'<br>'+t('Faded marker = estimated position','العلامة الباهتة = موقع تقديري')+'</div>';
  document.getElementById('leafSide').innerHTML=s;
}
function leafPass(p){
  if(LF.prov!=='all'&&(p.rg||'\u2014')!==LF.prov)return false;
  if(LF.tiers&&LF.tiers[p.tier||'']===false)return false;
  if(!LF.cats[p.cat])return false;
  if(LF.bidOnly&&!p.bid)return false;
  if((p.sc||0)<LF.minSc)return false;
  if(!LF.confs[p.cf])return false;
  return true;
}
function leafPopup(p,i){
  var n=LNODE[i], conf=p.cf==='\u2014'?t('Not scored','غير مُقيّم'):thrL(p.cf);
  var hh='<div><b dir="auto" style="font-size:13px">'+esc(p.n)+'</b><div style="margin:5px 0 7px"><span class="lchip" style="background:'+(CAT_COL[p.cat]||'#7A8A99')+'">'+esc(catS(p.cat))+'</span>'+(p.tier?'<span class="lchip" style="background:'+(p.tier==='Tier 1'?'#D4A017':'#5A95C8')+'">'+esc(tierL(p.tier))+'</span>':'')+(p.bid?'<span class="lchip" style="background:#C0392B">'+t('bids vs EH','تقدّم ضد EH')+(p.bc?' \u00d7'+p.bc:'')+'</span>':'')+'</div>';
  if(p.site){hh+='<div dir="auto" style="font-size:10.5px;color:#2E7D46;margin:-2px 0 7px">\ud83d\udccd '+esc(p.site)+' <span style="color:#8A99A3;font-size:9.5px">('+esc(posL(p.pos))+')</span></div>';}
  function row(k,v){return v?'<div class="prow"><span class="k">'+k+'</span><span class="v" dir="auto">'+v+'</span></div>':'';}
  hh+=row(t('Type','النوع'),esc(p.typ?catL(p.typ):''));
  hh+=row(t('City / province','المدينة / المنطقة'),esc(p.city)+' \u00b7 '+esc(regL(p.rg)));
  hh+=row(t('Coordinates','الإحداثيات'),(+p.lat).toFixed(4)+', '+(+p.lng).toFixed(4));
  hh+=row(t('Total Score','الدرجة الكلية'),n&&n.sc!=null?esc(scoreText(n,true)):t('Not scored','غير مُقيّم'));
  hh+=row(t('Threat to EH','التهديد على EH'),esc(p.th?thrL(p.th):''));
  hh+=row(t('Licence codes','رموز التراخيص'),esc((p.act||'').split(',').slice(0,4).join(', ')+((p.act||'').split(',').length>4?'\u2026':'')));
  hh+=row(t('Operator / ownership','المشغل / الملكية'),esc(p.own));
  hh+=row(t('Position','الموقع'),esc(posL(p.pos)));
  hh+=row(t('Data confidence','موثوقية البيانات'),conf);
  hh+=row(t('Source','المصدر'),esc(p.src));
  if(n)hh+='<div style="margin-top:8px;text-align:end"><button class="leafbtn" onclick="leafSel('+i+')">'+t('Open full profile','فتح الملف الكامل')+'</button></div>';
  return hh+'</div>';
}
function leafSel(i){var n=LNODE[i];if(n){state.sel=n;showDetail(n);}}   // maps-01: opens this exact company
"""
block(S, "function leafSidebar(){", "function leafStart(){", fix_nl(S, NEW_SIDE), 'bug',
      'maps-01/14/16: Leaflet filters, legend and popups use the live company record, category colours, all tiers, Arabic')
rep(S, "    var m=L.circleMarker([p.lat,p.lng],{radius:p.tier==='Tier 1'?9:7,fillColor:CMAP[p.cat]?CMAP[p.cat].c:'#999',fillOpacity:est?0.55:0.92,color:p.bid?'#C0392B':'#fff',weight:p.bid?2.5:1.5,opacity:1});\r\n    m.bindTooltip(p.n+(est?' (approx.)':''),{direction:'top'});",
       "    var m=L.circleMarker([p.lat,p.lng],{radius:p.tier==='Tier 1'?9:7,fillColor:CAT_COL[p.cat]||'#7A8A99',fillOpacity:est?0.55:0.92,color:p.bid?'#C0392B':'#fff',weight:p.bid?2.5:1.5,opacity:1});\r\n    m.bindTooltip(p.n+(est?t(' (approx.)',' (تقريبي)'):''),{direction:'top'});",
    'bug', 'maps-01/08: Leaflet markers coloured by stakeholder category (CMAP is keyed by company type, so every pin was grey)')
rep(S, "  var c=document.getElementById('leafCount'); if(c)c.textContent=shown;", "  var c=document.getElementById('leafCount'); if(c)c.textContent=shown.toLocaleString('en-US');",
    'copy', 'Leaflet shown-count formatted like the total')
rep(S, "function leafReset(){LF.prov='all';LF.t1=LF.t2=true;LF.cats=null;", "function leafReset(){LF.prov='all';LF.tiers=null;LF.cats=null;",
    'bug', 'maps-16: Leaflet reset restores every tier')

# ---- maps-12/14 chat (rewritten: computed answers, page language)
NEW_CHAT = r"""/* ===================== ASK THE MAP — guided chat (in-browser, no API) =====================
   patch_audit_maps.py (12 Oct 2026, maps-12/14): every answer is computed from the live map data and is written in the
   page language. */
const ASKQS=[
 ['topdirect','Who are the top direct competitors?','من أبرز المنافسين المباشرين؟'],
 ['topenv','Top environmental companies in KSA?','أبرز الشركات البيئية في السعودية؟'],
 ['score','How is the Total Score calculated?','كيف تُحسب الدرجة الكلية؟'],
 ['threat','Which companies are high-threat?','ما الشركات عالية التهديد؟'],
 ['region','Where are competitors concentrated?','أين يتركّز المنافسون؟'],
 ['tiers','Who are the Tier 1 key players?','من اللاعبون الرئيسيون في الفئة 1؟'],
 ['collab','Who could EH partner with?','مع من يمكن أن تتعاون EH؟'],
 ['find','Tell me about a specific company','أخبرني عن شركة محددة'],  ['expiry','Which competitor licences expire soon?','أي تراخيص المنافسين تنتهي قريباً؟'],  ['dual','Which companies are both client and bid rival?','أي الشركات عميلة ومنافسة في آن؟'],  ['hithreat','Who are the high-threat bid rivals?','من المنافسون الأعلى تهديداً في المنافسات؟']];
const QKW={
 topdirect:['direct competitor','top competitor','biggest','main rival','rivals','strongest','who competes','bids against','منافس','منافسين','مباشر','ابرز','اكبر','اقوى'],
 topenv:['environmental companies','env companies','top environmental','best environmental','leading environmental','شركات بيئيه','بيئيه','افضل','رائده'],
 score:['score','total score','points','ranking','rank','calculated','how is','formula','weight','درجه','نقاط','تصنيف','حساب','كيف'],
 threat:['threat','dangerous','risk','high threat','worry','worried','خطر','خطوره','تهديد','عاليه'],
 region:['region','regions','where','city','cities','geography','concentrated','location','منطقه','مناطق','اين','مدينه','تركز','جغرافيا'],
 tiers:['tier','tier 1','key player','key players','important','مستوى','رئيسي','لاعبون','مهم'],
 collab:['partner','partners','partnership','collaborat','ally','allies','joint','together','شريك','شركاء','تعاون','تحالف'],
 find:['specific','about company','tell me about','profile','detail','details','lookup','look up','search','معلومات','شركه محدده','بحث','ملف','تفاصيل']};
function _cnorm(s){s=(s||'').toLowerCase();['أ','إ','آ'].forEach(function(a){s=s.split(a).join('ا');});return s.split('ة').join('ه').split('ى').join('ي').replace(/[\u064B-\u0652]/g,'');}
function matchQ(text){var q=_cnorm(text);if(!q.trim())return[];return ASKQS.map(function(x){var id=x[0],sc=0;(QKW[id]||[]).forEach(function(k){if(q.indexOf(_cnorm(k))>=0)sc++;});return [id,sc];}).filter(function(a){return a[1]>0;}).sort(function(a,b){return b[1]-a[1];}).slice(0,4).map(function(a){return a[0];});}
const _scf=function(v){return v==null?'—':String(Math.round(v*10)/10);};
const _isComp=function(n){return n.cat==='Active Competitors'||n.cat==='Direct Competitors';};
function _rk(list,extra){var hh='<ol style="margin:8px 0 2px 18px;padding:0;display:flex;flex-direction:column;gap:5px">';list.forEach(function(n){hh+='<li style="font-size:12.5px"><a data-sel="'+esc(n.n)+'" style="color:#1A5FAB;font-weight:700;cursor:pointer;text-decoration:underline" dir="auto">'+esc(n.n)+'</a> <span style="background:#EAF3EC;color:#1E6B38;border-radius:8px;padding:1px 7px;font-weight:700;font-size:11px">'+_scf(n.sc)+'</span> <span style="color:#5A6B76;font-size:11px">'+(n.tier?esc(tierL(n.tier)):'—')+' · '+esc(regL(n.rg))+(extra?extra(n):'')+'</span></li>';});return hh+'</ol>';}
function _bids(n){return n.bc?' · '+n.bc+t(n.bc>1?' bids':' bid',' عطاء'):'';}
const ANSF={
  expiry:function(){
    var rows=NODES.filter(function(n){return n.mw&&n.mw.exp&&n.cat!=='EH (Reference)';})
      .map(function(n){return {n:n.n,d:mwDaysLeft(n.mw)};})
      .filter(function(x){return x.d!=null&&x.d>=0&&x.d<180;})
      .sort(function(a,b){return a.d-b.d;});
    var top=rows.slice(0,6).map(function(x){return '<li dir="auto">'+esc(x.n.slice(0,52))+' — <b>'+x.d+'</b>'+t(' days',' يوماً')+'</li>';}).join('');
    return '<div class="ehm"><b>'+rows.length+'</b>'+t(' competitor licences expire within 180 days. Soonest:',' ترخيصاً تنتهي خلال 180 يوماً. الأقرب انتهاءً:')+'<ul style="margin:6px 0 0 16px;padding:0">'+top+'</ul>'+t('A good moment for business outreach.','فرصة مناسبة للتواصل التجاري.')+'</div>';
  },
  dual:function(){
    var rows=NODES.filter(function(n){return n.cat==='EH Clients'&&n.bid;}).sort(function(a,b){return (b.bc||0)-(a.bc||0);}).slice(0,8);
    var lis=rows.map(function(n){return '<li dir="auto">'+esc(n.n.slice(0,50))+' — '+(n.bc||0)+t(' bid encounter(s)',' مواجهة في العطاءات')+'</li>';}).join('');
    return '<div class="ehm">'+t('Companies that are EH clients <i>and</i> appear in tender rosters against EH:','شركات هي عملاء لدى EH <i>و</i>تظهر في قوائم المتقدمين ضد EH:')+'<ul style="margin:6px 0 0 16px;padding:0">'+(lis||'<li>'+t('none at present','لا يوجد حالياً')+'</li>')+'</ul>'+t('These relationships need careful handling.','تتطلب هذه العلاقات إدارة دقيقة.')+'</div>';
  },
  hithreat:function(){
    var all=NODES.filter(function(n){return n.bid&&n.threat==='High';}), rows=all.slice().sort(function(a,b){return (b.bc||0)-(a.bc||0);}).slice(0,8);
    var lis=rows.map(function(n){return '<li dir="auto">'+esc(n.n.slice(0,50))+' — '+(n.bc||0)+t(' encounters',' مواجهة')+'</li>';}).join('');
    return '<div class="ehm"><b>'+all.length+'</b>'+t(' bid rivals carry a High threat rating (wins against EH and/or heavy presence). Top:',' منافساً في المنافسات يحمل تصنيف تهديد مرتفع (فوز على EH و/أو حضور كثيف). الأبرز:')+'<ul style="margin:6px 0 0 16px;padding:0">'+lis+'</ul>'+t('Watch them in every tender.','راقبهم في كل منافسة.')+'</div>';
  },
 topdirect:function(){   // maps-12: only Active and Direct competitors (ACWA Power and other clients are excluded)
  var all=NODES.filter(function(n){return n.bid&&_isComp(n)&&n.sc!=null;}), a=all.slice().sort(function(x,y){return y.sc-x.sc;}).slice(0,10);
  return '<div class="ehm ansbox"><b>'+t('Top direct competitors','أبرز المنافسين المباشرين')+'</b> — '+t('Active and Direct competitors that have bid against EH, ranked by Total Score ('+all.length+' such companies; '+NODES.filter(function(n){return n.bid;}).length+' companies of every kind have bid against EH):','المنافسون النشطون والمباشرون الذين تقدّموا ضد EH، مرتبون حسب الدرجة الكلية ('+all.length+' شركة؛ وعدد كل الشركات التي تقدّمت ضد EH '+NODES.filter(function(n){return n.bid;}).length+'):')+_rk(a,_bids)+'<div style="color:#5A6B76;font-size:11px;margin-top:6px">'+t('Click a name to open its full profile.','انقر الاسم لفتح الملف الكامل.')+'</div></div>';},
 topenv:function(){var a=NODES.filter(function(n){return n.typ==='Environmental Services'&&n.sc!=null&&n.cat!=='EH (Reference)';}).sort(function(x,y){return y.sc-x.sc;}).slice(0,10);
  var eh=NODES.find(function(n){return n.cat==='EH (Reference)';}), ehs=eh&&eh.sc!=null?_scf(eh.sc):'—', tot=NODES.filter(function(n){return n.typ==='Environmental Services';}).length;
  return '<div class="ehm ansbox"><b>'+t('Top environmental companies','أبرز الشركات البيئية')+'</b> — '+t('ranked by Total Score among '+tot+' companies typed “Environmental Services”:','مرتبة حسب الدرجة الكلية بين '+tot+' شركة من نوع «خدمات بيئية»:')+_rk(a)+'<div style="color:#5A6B76;font-size:11px;margin-top:6px">'+t('EH itself appears on the map as the EH (Reference) entry — capability benchmark score '+ehs+' (see Methodology) — and is excluded from this competitor ranking. Broader waste/recycling players like Al-Qaryan and SIRC are typed separately.','تظهر EH نفسها على الخريطة بوصفها المرجع — درجة القدرة المرجعية '+ehs+' (انظر المنهجية) — وهي مستبعدة من ترتيب المنافسين هذا. وتُصنَّف شركات النفايات وإعادة التدوير الأوسع مثل القريان وسرك بنوع مختلف.')+'</div></div>';},
 score:function(){   // maps-12: describes the current v2 model (Methodology), not the retired Proposal B
  var r=function(a,b,p){return '<tr><td style="padding:3px 0;border-top:1px solid #E7EDF0">'+t(a,b)+'</td><td style="text-align:end;border-top:1px solid #E7EDF0">'+p+'</td></tr>';};
  return '<div class="ehm ansbox"><b>'+t('Total Score (v2 model, Sep 2026)','الدرجة الكلية (الإصدار الثاني، سبتمبر 2026)')+'</b> = '+t('Capability (0–100) + Strategic backing (0–25) + Bid exposure (+15 for a company that has bid against EH), maximum 140.','القدرة (0–100) + الإسناد الاستراتيجي (0–25) + التعرض للعطاءات (‎+15 لمن تقدّم ضد EH)، بحد أقصى 140.')+
  '<table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:12px"><tr style="color:#5A6B76"><td style="padding:3px 0">'+t('Capability (0–100)','القدرة (0–100)')+'</td><td style="text-align:end">'+t('Points','النقاط')+'</td></tr>'+
  r('Service overlap with EH’s own services','تداخل الخدمات مع خدمات EH','35')+r('Bid encounters with EH','مرات المواجهة مع EH في العطاءات','25')+r('Strategic backing','الإسناد الاستراتيجي','15')+r('Workforce band','فئة القوى العاملة','10')+r('Megaproject involvement','المشاركة في المشاريع الكبرى','7')+r('Site footprint','انتشار المواقع','5')+r('Multinational operations','العمليات متعددة الجنسيات','3')+'</table>'+
  t('<b>Missing data is never neutral-filled.</b> Where data confidence is Low, only evidenced facts (bid encounters, licence records) score; everything else sits at a small-company floor. Each profile shows its data confidence. Clients, government bodies and regulators are not scored on this model. Full detail: Methodology.','<b>لا تُملأ البيانات المفقودة بقيم محايدة أبداً.</b> حين تكون موثوقية البيانات منخفضة لا يُحتسب إلا ما ثبت بالدليل (مرات المواجهة في العطاءات وسجلات التراخيص)، ويبقى الباقي عند الحد الأدنى للشركات الصغيرة. ويظهر مؤشر الموثوقية في كل ملف. ولا يُقيَّم العملاء والجهات الحكومية والتنظيمية بهذا النموذج. التفاصيل الكاملة في المنهجية.')+'</div>';},
 threat:function(){var a=NODES.filter(function(n){return n.threat==='High';}).sort(function(x,y){return (y.sc||0)-(x.sc||0);});
  return '<div class="ehm ansbox"><b>'+a.length+t(' companies are flagged High threat',' شركة مصنّفة بتهديد مرتفع')+'</b> — '+t('frequent challengers with real competitive overlap. The strongest by score:','منافسون متكررون بتداخل تنافسي فعلي. الأقوى حسب الدرجة:')+_rk(a.slice(0,10),_bids)+'</div>';},
 region:function(){   // maps-12: the conclusion is computed from the same table (no fixed sentence)
  var c={};NODES.forEach(function(n){if(_isComp(n)){c[n.rg]=(c[n.rg]||0)+1;}});
  var a=Object.keys(c).map(function(k){return [k,c[k]];}).sort(function(x,y){return y[1]-x[1];});var tot=a.reduce(function(s,x){return s+x[1];},0);
  var hh='<div class="ehm ansbox"><b>'+t('Where the '+tot+' active + direct competitors sit:','أين يتمركز '+tot+' منافساً نشطاً ومباشراً:')+'</b><table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:12px">';
  a.slice(0,9).forEach(function(x){var p=Math.round(100*x[1]/Math.max(1,tot));hh+='<tr><td style="padding:2px 0">'+esc(regL(x[0]))+'</td><td style="width:46%"><div style="background:#E7EDF0;border-radius:4px;height:9px"><div style="width:'+p+'%;background:#D64545;height:9px;border-radius:4px"></div></div></td><td style="text-align:end;font-weight:700;padding-inline-start:6px">'+x[1]+'</td></tr>';});
  var known=a.filter(function(x){return x[0]!=='\u2014';}).slice(0,3), none=c['\u2014']||0;
  var lst=known.map(function(x){return regL(x[0])+' ('+x[1]+')';}).join(t(', ','، '));
  return hh+'</table>'+t('With a recorded region, most sit in '+lst+'.'+(none?' '+none+' have no recorded region yet.':''),'ومن الشركات ذات المنطقة المسجلة، يتركّز أغلبها في: '+lst+'.'+(none?' و'+none+' شركة لم تُسجَّل منطقتها بعد.':''))+'</div>';},
 tiers:function(){var t1=NODES.filter(function(n){return n.tier==='Tier 1';}).sort(function(x,y){return (y.sc||0)-(x.sc||0);});
  var cnt={};NODES.forEach(function(n){var k=n.tier||'Unclassified';cnt[k]=(cnt[k]||0)+1;});
  var order=['Tier 1','Tier 2','Tier 3','Tier 4','Tier 5','Tier 6','GOV','Unclassified'];
  return '<div class="ehm ansbox"><b>'+t1.length+t(' Tier 1 key players',' لاعباً رئيسياً في الفئة 1')+'</b> '+t('(gold-ring companies). Tier counts: ','(الشركات ذات الحلقة الذهبية). أعداد الفئات: ')+order.filter(function(k){return cnt[k];}).map(function(k){return (k==='Unclassified'?t('Unclassified','غير مصنّفة'):tierL(k))+': <b>'+cnt[k]+'</b>';}).join(' · ')+'.<br>'+t('Highest-scoring Tier 1:','الأعلى درجة في الفئة 1:')+_rk(t1.slice(0,10))+'</div>';},
 collab:function(){var a=NODES.filter(function(n){return (n.collab||n.cat==='Potential Collaborators')&&n.sc!=null;}).sort(function(x,y){return y.sc-x.sc;}).slice(0,10);
  return '<div class="ehm ansbox"><b>'+t('Strongest collaboration candidates','أقوى المرشحين للتعاون')+'</b> — '+t('flagged collaborators and capable regional players outside EH’s core turf:','شركاء محتملون مصنّفون وشركات إقليمية قادرة خارج نطاق EH الأساسي:')+_rk(a)+'<div style="color:#5A6B76;font-size:11px;margin-top:6px">'+t('A high-score company that rarely meets EH in tenders is a partner prospect, not a threat.','الشركة عالية الدرجة التي نادراً ما تواجه EH في المنافسات شريك محتمل لا تهديد.')+'</div></div>';},
};
(function(){
 var css='#ehcbtn{position:fixed;bottom:22px;right:22px;width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#33A85B,#1A5FAB);box-shadow:0 6px 20px rgba(26,95,171,.35);cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:99999;border:none;transition:transform .15s}#ehcbtn:hover{transform:scale(1.06)}#ehcbtn svg{width:27px;height:27px;fill:#fff}#ehcp{position:fixed;bottom:92px;right:22px;width:374px;max-width:calc(100vw - 28px);height:544px;max-height:calc(100vh - 128px);background:#fff;border-radius:16px;box-shadow:0 14px 44px rgba(0,0,0,.24);z-index:99999;display:none;flex-direction:column;overflow:hidden}#ehcp.open{display:flex}.ehch{background:linear-gradient(135deg,#2E9E5B,#1A5FAB);color:#fff;padding:13px 16px;display:flex;align-items:center;gap:8px}.ehch b{font-size:14.5px}.ehch .s{font-size:10.5px;opacity:.9}.ehcx{margin-left:auto;cursor:pointer;font-size:19px;opacity:.9;line-height:1}.ehcb{flex:1;overflow-y:auto;padding:13px;background:#F5F8FA;display:flex;flex-direction:column;gap:9px}.ehm{background:#fff;border:1px solid #E7EDF0;border-radius:12px;border-top-left-radius:3px;padding:10px 12px;font-size:12.5px;color:#3A4A52;line-height:1.5;max-width:92%}.ehu{background:#E7F1FB;border:1px solid #CFE3F5;border-radius:12px;border-bottom-right-radius:3px;padding:9px 12px;font-size:12.5px;color:#14456a;align-self:flex-end;max-width:85%}.ehchip{display:block;width:100%;text-align:start;background:#fff;border:1px solid #CFE0EC;border-radius:10px;padding:9px 11px;margin-top:6px;cursor:pointer;font-size:12.5px;color:#1A5FAB;font-weight:600}.ehchip:hover{background:#EAF3FB;border-color:#1A5FAB}.ehchip .ar{display:block;color:#5A6B76;font-weight:500;font-size:11.5px;margin-top:2px}.ehcf{border-top:1px solid #E7EDF0;padding:9px;display:flex;gap:7px;background:#fff}.ehcf input{flex:1;border:1px solid #D5DEE2;border-radius:20px;padding:9px 14px;font-size:13px;outline:none}.ehcf input:focus{border-color:#1A5FAB}.ehsend{background:linear-gradient(135deg,#2E9E5B,#1A5FAB);border:none;color:#fff;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:15px;flex:none}.ehcb .ansbox{max-width:100%}html[dir=rtl] .ehcx{margin-left:0;margin-right:auto}';
 var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
 var w=document.createElement('div');
 w.innerHTML='<button id="ehcbtn" aria-label="Ask the map"><svg viewBox="0 0 24 24"><path d="M12 3C6.5 3 2 6.6 2 11c0 2.3 1.2 4.4 3.3 5.9-.2 1-.8 2.3-1.6 3.3 1.5-.2 3-.8 4.3-1.6 1.2.4 2.5.6 3.7.6 5.5 0 10-3.6 10-8s-4.5-8-10-8z"/></svg></button><div id="ehcp"><div class="ehch"><div><b id="ehct">Ask the map</b><div class="s" id="ehcs">runs in your browser</div></div><div class="ehcx">✕</div></div><div class="ehcb" id="ehcb"></div><div class="ehcf"><input id="ehci" placeholder="Type your question…"><button class="ehsend" aria-label="Send">➜</button></div></div>';
 document.body.appendChild(w);
 window.ehChat={
  open:false,
  relang:function(){var e;if((e=document.getElementById('ehct')))e.textContent=t('Ask the map','اسأل الخريطة');if((e=document.getElementById('ehcs')))e.textContent=t('runs in your browser','يعمل داخل متصفحك');if((e=document.getElementById('ehci')))e.placeholder=t('Type your question…','اكتب سؤالك…');if((e=document.getElementById('ehcbtn')))e.setAttribute('aria-label',t('Ask the map','اسأل الخريطة'));if((e=document.getElementById('ehcb')))e.dir=LNG==='ar'?'rtl':'ltr';},
  toggle:function(){this.open=!this.open;document.getElementById('ehcp').classList.toggle('open',this.open);if(this.open&&!this._g){this._g=1;this.relang();this.greet();document.getElementById('ehci').focus();}},
  add:function(hh){var b=document.getElementById('ehcb');var dd=document.createElement('div');dd.style.display='contents';dd.innerHTML=hh;b.appendChild(dd);b.scrollTop=b.scrollHeight;},
  greet:function(){this.add('<div class="ehm">'+t('Hi 👋 Ask about EH’s competitors, top environmental companies, the Total Score, threats, regions, or a specific company — type a question and press Enter.','مرحباً 👋 اسأل عن منافسي EH، أو أبرز الشركات البيئية، أو الدرجة الكلية، أو التهديدات، أو المناطق، أو شركة محددة — اكتب سؤالك واضغط Enter.')+'</div>');this.chips(['topdirect','topenv','score','expiry','dual','hithreat'],t('Popular questions:','أسئلة شائعة:'));},
  chips:function(ids,label){var hh='<div class="ehm">'+label;ids.forEach(function(id){var q=ASKQS.find(function(x){return x[0]===id;});hh+='<button class="ehchip" data-q="'+id+'">'+(LNG==='ar'?q[2]:q[1])+'</button>';});hh+='</div>';this.add(hh);},
  submit:function(){var inp=document.getElementById('ehci');var q=inp.value.trim();if(!q)return;this.add('<div class="ehu" dir="auto">'+esc(q)+'</div>');inp.value='';var ids=matchQ(q);if(ids.length){this.chips(ids,t('Closest to your question — tap one:','الأقرب إلى سؤالك — اختر واحداً:'));return;}if(this.searchCo(q)){return;}this.chips(ASKQS.map(function(x){return x[0];}),t('I couldn’t match that — try a question below, or type part of a company name:','لم أجد تطابقاً — جرّب أحد الأسئلة أدناه، أو اكتب جزءاً من اسم شركة:'));},
  answer:function(id){var q=ASKQS.find(function(x){return x[0]===id;});this.add('<div class="ehu">'+(LNG==='ar'?q[2]:q[1])+'</div>');if(id==='find'){this.findForm();return;}this.add(ANSF[id]());},
  findForm:function(){this.add('<div class="ehm">'+t('Which company? Type part of the name','أي شركة؟ اكتب جزءاً من الاسم')+'<div style="display:flex;gap:6px;margin-top:7px"><input class="ehc-nm" placeholder="'+t('e.g. Kayan','مثال: كيان')+'" style="flex:1;padding:6px 9px;border:1px solid #D5DEE2;border-radius:6px;font-size:13px"><button class="ehchip" style="width:auto;margin:0;padding:7px 14px" data-go="find">'+t('Search','بحث')+'</button></div></div>');},
  searchCo:function(text){var q=_cnorm(text);if(q.length<3)return false;var hitsArr=NODES.filter(function(n){return _cnorm(n.n).indexOf(q)>=0;}).sort(function(a,b){return (b.sc||0)-(a.sc||0);});if(!hitsArr.length)return false;if(hitsArr.length===1){this.showCo(hitsArr[0]);return true;}var hh='<div class="ehm">'+hitsArr.length+t(' matches (highest score first) — pick one:',' نتيجة (الأعلى درجة أولاً) — اختر واحدة:');hitsArr.slice(0,6).forEach(function(n){hh+='<button class="ehchip" data-sel="'+esc(n.n)+'" dir="auto">'+esc(n.n)+'<span class="ar">'+(n.tier?esc(tierL(n.tier)):'—')+' · '+_scf(n.sc)+t(' pts',' نقطة')+' · '+esc(regL(n.rg))+'</span></button>';});if(hitsArr.length>6)hh+='<div style="color:#5A6B76;font-size:11px;margin-top:5px">'+t('Showing top 6 of '+hitsArr.length+' — type more letters to narrow.','أعلى 6 من '+hitsArr.length+' — اكتب أحرفاً أكثر للتضييق.')+'</div>';hh+='</div>';this.add(hh);return true;},
  showCo:function(n){selByName(n.n);var f=[];if(n.tier==='Tier 1')f.push('⭐ '+tierL('Tier 1'));if(n.bid)f.push('🔴 '+t('bids vs EH','تقدّم ضد EH')+' ('+(n.bc||'?')+')');if(n.threat)f.push('⚔ '+thrL(n.threat)+t(' threat',' تهديد'));if(n.mp)f.push('🏗 '+t('Megaprojects','مشاريع كبرى'));if(n.mn)f.push('🌍 '+t('Multinational','متعددة الجنسيات'));
   this.add('<div class="ehm ansbox"><b dir="auto">'+esc(n.n)+'</b><br><span style="color:#5A6B76;font-size:11.5px">'+esc(catS(n.cat))+' · '+esc(n.typ?catL(n.typ):'—')+' · '+esc(regL(n.rg))+'</span><br>'+t('Total Score: ','الدرجة الكلية: ')+'<b style="color:#1E6B38">'+_scf(n.sc)+'</b>'+(f.length?' · '+f.join(' · '):'')+'<br><span style="color:#5A6B76;font-size:11px">'+t('Full profile opened in the detail panel','فُتح الملف الكامل في لوحة التفاصيل')+'</span></div>');},
 };
 document.getElementById('ehcbtn').onclick=function(){ehChat.toggle();};
 w.querySelector('.ehcx').onclick=function(){ehChat.toggle();};
 w.querySelector('.ehsend').onclick=function(){ehChat.submit();};
 document.getElementById('ehci').addEventListener('keydown',function(e){if(e.key==='Enter')ehChat.submit();});
 document.getElementById('ehcb').addEventListener('click',function(e){var c=e.target.closest('[data-q]');if(c){ehChat.answer(c.getAttribute('data-q'));return;}var g=e.target.closest('[data-go]');if(g){var inp=document.querySelector('#ehcb .ehc-nm');var q=inp?inp.value.trim():'';if(q&&!ehChat.searchCo(q))ehChat.add('<div class="ehm">'+t('No company matches “'+esc(q)+'” — try fewer letters.','لا توجد شركة تطابق «'+esc(q)+'» — جرّب أحرفاً أقل.')+'</div>');return;}var sl=e.target.closest('[data-sel]');if(sl){var nm=sl.getAttribute('data-sel');var nn=NODES.find(function(x){return x.n===nm;});if(nn)ehChat.showCo(nn);}});
})();
"""
block(S, "/* ===================== ASK THE MAP", "</script>\r\n<script>/* default view", fix_nl(S, NEW_CHAT), 'copy',
      'maps-12/14: "Ask the map" answers computed from the live data (v2 score, EH score, region conclusion, competitors only) and in the page language')

# ---- maps-11 note count; maps-13 comment
rep(S, "ألغِ خيار «تقدّم ضد EH فقط» في الفلاتر لعرض الجميع (4,195 جهة).",
       "ألغِ خيار «تقدّم ضد EH فقط» في الفلاتر لعرض الجميع ('+NODES.length.toLocaleString('en-US')+' جهة).", 'copy', 'maps-11: note counts the map (AR)')
rep(S, "Untick “Bid against EH only” in Filters to see all 4,195.", "Untick “Bid against EH only” in Filters to see all '+NODES.length.toLocaleString('en-US')+'.",
    'copy', 'maps-11: note counts the map (EN)')
rep(S, "<script>/* default view (visual upgrade 07/09): Tier 1 shown on open, with a note; Reset filters shows the old empty gate */",
       "<script>/* default view (visual upgrade 07/09): bidders shown on open, with a note; Reset filters shows every company (patch_audit_maps.py, maps-13) */",
    'copy', 'maps-13: comment matches the new reset behaviour')

if data_blocks(TXT[S]) != BLOCKS_BEFORE:
    FAILURES.append({'file': S, 'note': 'a DATA/LIC/BANALYTICS block changed — refusing to write', 'old': ''})

# =====================================================================================================================
# CLIENT BUBBLE MAP
# =====================================================================================================================
B = 'bub'
dec = json.JSONDecoder()
def grab_const(name):
    s = TXT[B]; i = s.find('const ' + name + ' = '); j = i + len('const ' + name + ' = ')
    obj, k = dec.raw_decode(s, j)
    return i, j, k, obj
_, _, _, DATA = grab_const('DATA')
di, dj, dk, DETAIL = grab_const('DETAIL')
assert json.dumps(DETAIL, ensure_ascii=False) == TXT[B][dj:dk], 'DETAIL format not reproducible — refusing'
hi, hj, hk, HEAT = grab_const('HEAT')
assert json.dumps(HEAT, ensure_ascii=False) == TXT[B][hj:hk], 'HEAT format not reproducible — refusing'
names = {d['name']: d for d in DATA}

# maps-21/23: the branch → parent pairs DATA already merged (identified by name; the totals check below proves each one)
RULES = [('سامرف', '( SAUDI ARAMCO ) Saudi Arabian Oil Company'), ('الفنار', 'شركة الفنار مساهمة مقفلة'),
         ('البابطين للمقاولات', 'شركة البابطين للمقاولات'), ('البحر الابيض المتوسط', 'شركة البحر الابيض المتوسط للملاحة السعودية'),
         ('دايفرسي', 'مستودع شركة دايفرسي العربية السعودية المحدودة -الرياض'), ('الكابلات السعودية', 'شركة الكابلات السعودية'),
         ('رايسي', 'شركة رايسي للتجارة والمقاولات المحدودة - محطة نجران'),
         ('الشريف وكي اي سي', 'شركة مجموعة الشريف وكي اي سي المحدودة - مشروع انشاء خطوط هوائية بين محطة ينبع ورابغ'),
         ('الخرسانة جاهزة الصب', 'شركة الخرسانة جاهزة الصب المحدودة - مكة المكرمة'), ('كنداسة', 'مصنع شركة كنداسة لخدمات المياه-مشروع جدة الاسلامي'),
         ('الزايدي', 'مصنع شركة مجموعة الزايدي للانترلوك والبردورات'), ('سواكو', 'شركة سواكو لتحلية المياه (SAWACO Desalination)')]
BRANCH_OF = {}
for k in DETAIL:
    if k in names: continue
    hits = [p for sub, p in RULES if sub in k]
    if len(hits) != 1 or hits[0] not in names:
        FAILURES.append({'file': B, 'note': 'branch with no single parent: ' + k, 'old': ''}); continue
    BRANCH_OF[k] = hits[0]

def r2(x): return round(x, 2)
# DETAIL: branch lines join the parent
for br, par in BRANCH_OF.items():
    DETAIL[par] = DETAIL.get(par, []) + DETAIL.pop(br)
# HEAT: each branch entry moves to the parent's sector cell. The per-year line split of an entry is recovered exactly by
# assigning the branch's DETAIL lines to its cells so every cell's 2025 value, 2026 value and line count match.
def split_lines(br, cells):
    lines = DETAIL_ORIG[br]
    sols = set()
    for assign in itertools.product(range(len(cells)), repeat=len(lines)):
        acc = [[0.0, 0.0, 0, 0, 0] for _ in cells]
        for l, c in zip(lines, assign):
            a = acc[c]; v = l['v'] or 0
            if l['y'] == 2025: a[0] += v; a[3] += l['n']
            else: a[1] += v; a[4] += l['n']
            a[2] += l['n']
        if all(abs(a[0] - e['v25']) < 0.01 and abs(a[1] - e['v26']) < 0.01 and a[2] == e['n'] for a, (k, e) in zip(acc, cells)):
            sols.add(tuple((a[3], a[4]) for a in acc))
    return sols
DETAIL_ORIG = json.loads(TXT[B][dj:dk])
moves = []
for key, cell in list(HEAT.items()):
    for e in cell['co']:
        if e['name'] in BRANCH_OF: moves.append((key, e))
by_branch = {}
for key, e in moves: by_branch.setdefault(e['name'], []).append((key, e))
for br, cells in by_branch.items():
    sols = split_lines(br, cells)
    if len(sols) != 1:
        FAILURES.append({'file': B, 'note': 'cannot split %s lines by year exactly (%d solutions)' % (br, len(sols)), 'old': ''}); continue
    split = next(iter(sols)); par = BRANCH_OF[br]; psec = names[par]['sector']
    for (key, e), (n25, n26) in zip(cells, split):
        src = HEAT[key]; cat = key.split('|')[1]
        src['co'] = [x for x in src['co'] if x is not e]
        src['v25'] = r2(src['v25'] - e['v25']); src['v26'] = r2(src['v26'] - e['v26']); src['n25'] -= n25; src['n26'] -= n26
        if not src['co']: del HEAT[key]
        dst = HEAT.setdefault(psec + '|' + cat, {'v25': 0.0, 'v26': 0.0, 'n25': 0, 'n26': 0, 'co': []})
        dst['v25'] = r2(dst['v25'] + e['v25']); dst['v26'] = r2(dst['v26'] + e['v26']); dst['n25'] += n25; dst['n26'] += n26
        pe = next((x for x in dst['co'] if x['name'] == par), None)
        if pe is None: dst['co'].append({'name': par, 'v25': e['v25'], 'v26': e['v26'], 'n': e['n']})
        else: pe['v25'] = r2(pe['v25'] + e['v25']); pe['v26'] = r2(pe['v26'] + e['v26']); pe['n'] += e['n']
# checks: every client's panel equals its bubble (both years); every sector's heatmap equals the legend; nothing lost
for d in DATA:
    L = DETAIL.get(d['name'], [])
    for y in (2025, 2026):
        s = sum(l['v'] or 0 for l in L if l['y'] == y)
        if abs(s - d['v%d' % y]) > 1: FAILURES.append({'file': B, 'note': 'DETAIL≠DATA after merge: %s %d (%s vs %s)' % (d['name'], y, s, d['v%d' % y]), 'old': ''})
sec_h, sec_d = {}, {}
for k, c in HEAT.items():
    s = k.split('|')[0]; sec_h[s] = sec_h.get(s, 0) + c['v25'] + c['v26']
    if abs(sum(e['v25'] for e in c['co']) - c['v25']) > 1 or c['n25'] + c['n26'] != sum(e['n'] for e in c['co']):
        FAILURES.append({'file': B, 'note': 'HEAT cell does not add up after merge: ' + k, 'old': ''})
    for e in c['co']:
        if e['name'] not in names: FAILURES.append({'file': B, 'note': 'HEAT still lists a non-client name: ' + e['name'], 'old': ''})
for d in DATA: sec_d[d['sector']] = sec_d.get(d['sector'], 0) + d['v2025'] + d['v2026']
for s in set(sec_h) | set(sec_d):
    if abs(sec_h.get(s, 0) - sec_d.get(s, 0)) > 1: FAILURES.append({'file': B, 'note': 'sector total differs after merge: ' + s, 'old': ''})
HEAT_ORIG = json.loads(TXT[B][hj:hk])
for f in ('v25', 'v26', 'n25', 'n26'):
    if abs(sum(c[f] for c in HEAT.values()) - sum(c[f] for c in HEAT_ORIG.values())) > 1:
        FAILURES.append({'file': B, 'note': 'HEAT grand total %s changed' % f, 'old': ''})
if sum(len(v) for v in DETAIL.values()) != sum(len(v) for v in DETAIL_ORIG.values()):
    FAILURES.append({'file': B, 'note': 'DETAIL line count changed', 'old': ''})
new_detail = json.dumps(DETAIL, ensure_ascii=False); new_heat = json.dumps(HEAT, ensure_ascii=False)
TXT[B] = TXT[B][:hj] + new_heat + TXT[B][hk:]          # HEAT comes after DETAIL: replace it first
TXT[B] = TXT[B][:dj] + new_detail + TXT[B][dk:]
_log(B, 'data', 'DETAIL / HEAT with %d branch keys' % len(BRANCH_OF), 'branches merged into %d parents' % len(set(BRANCH_OF.values())),
     'data', 'maps-21/23: the %d branch / project rows DATA already merged are merged in DETAIL and HEAT too (panel = bubble, heatmap sector = legend)' % len(BRANCH_OF), 1, True)

# ---- BUB_I18N dictionary edits (maps-22/28/29)
bi = TXT[B].find('const BUB_I18N='); bj = TXT[B].find('\n', bi)
raw = TXT[B][bi + len('const BUB_I18N='):bj]; semi = raw.endswith(';'); raw = raw[:-1] if semi else raw
I18 = json.loads(raw)
fmt_i18 = lambda o: json.dumps(o, separators=(',', ':'))
if fmt_i18(I18) != raw:
    fmt_i18 = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
assert fmt_i18(I18) == raw, 'BUB_I18N format not reproducible — refusing'
I18['ui']['lines_lbl'] = ['Ledger lines:', 'بنود السجل:']
I18['ui']['q_x'] = ['How many projects the client gives EH → (log scale)', I18['ui']['q_x'][1]]
for r in I18['st']:
    if r[0] == '.kpis>span:nth-child(3)': r[2] = 'المشاريع'
    if r[0] == 'footer': r[2] = 'مساحة الفقاعة = إجمالي قيمة العقود. البنود المسعّرة فقط (البنود التي لا تحمل مبلغاً بالريال مستبعدة). القطاعات مستنتجة آلياً من أسماء الشركات.'
I18['cap']['svgQuad'] = ('أعلى اليمين هو الأفضل — عملاء يُسندون إلى آفاق البيئة مشاريع كثيرة وينفقون كثيراً؛ وأعلى اليسار عملاء ينفقون كثيراً لكنهم '
                         'يُسندون إليها مشاريع أقل من وسيط المجموعة ويمكنهم شراء المزيد؛ وأسفل اليمين عملاء يُسندون إليها مشاريع صغيرة كثيرة.')
TXT[B] = TXT[B][:bi] + 'const BUB_I18N=' + fmt_i18(I18) + (';' if semi else '') + TXT[B][bj:]
_log(B, 'data', 'BUB_I18N', 'lines_lbl / q_x / kpis / footer / svgQuad caption', 'copy',
     'maps-22/28/29 (AR): "ledger lines" vs "projects"; quadrant caption; footer developer note removed', 1, True)

# ---- maps-22 English wording
rep(B, '<span><b id="kProj">–</b>project lines</span>', '<span><b id="kProj">–</b>projects</span>', 'copy', 'maps-22: header counts projects (DATA p)')
rep(B, '${BUB_LANG==="ar" ? bCount(proj(d.data),"line") : proj(d.data)+bT("proj_line_s")+(proj(d.data)>1?"s":"")}',
       '${BUB_LANG==="ar" ? bCount(proj(d.data),"proj") : proj(d.data)+" project"+(proj(d.data)>1?"s":"")}', 'copy', 'maps-22: bubble tooltip says projects')
rep(B, '`<b>${fmt(d3.sum(priced, l => l.v))}</b> across <b>${d3.sum(lines, l => l.n)}</b> line${d3.sum(lines,l=>l.n)>1?"s":""}`',
       '`<b>${fmt(d3.sum(priced, l => l.v))}</b> across <b>${d3.sum(lines, l => l.n)}</b> ledger line${d3.sum(lines,l=>l.n)>1?"s":""}`', 'copy', 'maps-22: company panel says ledger lines')
rep(B, '`<b>${fmt(hv(c))}</b> across <b>${hn(c)}</b> lines · <b>${cos.length}</b> client${cos.length>1?"s":""}`',
       '`<b>${fmt(hv(c))}</b> across <b>${hn(c)}</b> ledger lines · <b>${cos.length}</b> client${cos.length>1?"s":""}`', 'copy', 'maps-22: heatmap cell panel says ledger lines')
rep(B, "(BUB_LANG===\"ar\"?bCount(d.p,\"proj\"):d.p+' jobs')", "(BUB_LANG===\"ar\"?bCount(d.p,\"proj\"):d.p+' projects')", 'copy', 'maps-22: quadrant name list says projects')
rep(B, 'Right = gives EH <b>many jobs</b>;', 'Right = gives EH <b>many projects</b>;', 'copy', 'maps-22: quadrant intro says projects')
rep(B, '</span> — many jobs <i>and</i> big money: protect these relationships.', '</span> — many projects <i>and</i> big money: protect these relationships.', 'copy', 'maps-22: quadrant legend')
rep(B, '</span> — big money from only a few jobs: one lost contract hurts, deepen the relationship.', '</span> — big money from only a few projects: one lost contract hurts, deepen the relationship.', 'copy', 'maps-22: quadrant legend')
rep(B, '</span> — many small jobs: efficient to serve, best cross-sell targets.', '</span> — many small projects: efficient to serve, best cross-sell targets.', 'copy', 'maps-22: quadrant legend')
rep(B, '</span> — few small jobs.', '</span> — few small projects.', 'copy', 'maps-22: quadrant legend')
# maps-28 caption (EN)
rep(B, '"svgQuad": "Top right is the ideal — clients who give EH many jobs and spend a lot; top left are big spenders who give EH only one or two jobs and could buy more; bottom right give EH many small jobs."',
       '"svgQuad": "Top right is the ideal — clients who give EH many projects and spend a lot; top left are big spenders who give EH fewer projects than the middle of the group and could buy more; bottom right give EH many small projects."',
    'copy', 'maps-28: caption no longer says "only one or two jobs" (the group has 1–4 projects, below the median)')
# maps-29 footer (EN)
rep(B, '  Sectors auto-derived from company names — override in the build script as needed.\n', '  Sectors auto-derived from company names.\n', 'copy', 'maps-29: developer note removed from the footer')
# maps-24/26 header KPIs + year propagation
rep(B, '  document.getElementById("kComp").textContent = rows.length;\n  document.getElementById("kVal").textContent  = fmt(d3.sum(rows, val));\n  document.getElementById("kProj").textContent = d3.sum(rows, proj);\n',
       '  updHeader();\n', 'bug', 'maps-26: header KPIs computed by updHeader() (from the bubbles shown)')
rep(B, 'function render(){\n',
       '/* patch_audit_maps.py (maps-24/26): header KPIs follow the year in every view, and the sectors shown in the Bubble view */\n'
       'function updHeader(){\n'
       '  const rows = DATA.filter(d => val(d) > 0);\n'
       '  const base = (typeof viewMode === "undefined" || viewMode === "bubbles") ? rows.filter(d => !hidden.has(d.sector)) : rows;\n'
       '  document.getElementById("kComp").textContent = base.length;\n'
       '  document.getElementById("kVal").textContent  = fmt(d3.sum(base, val));\n'
       '  document.getElementById("kProj").textContent = d3.sum(base, proj);\n'
       '}\n'
       'function render(){\n', 'bug', 'maps-24/26: updHeader()')
rep(B, '    yearMode = b.dataset.y;\n    if (viewMode === "heat") renderHeat();',
       '    yearMode = b.dataset.y;\n'
       '    quadYear = dealYear = wsYear = yearMode;   // maps-24: the Executive cards follow the page year (their own toggles still work)\n'
       '    ["ytogQuad","ytogDeal","ytogWs"].forEach(id => { const el = document.getElementById(id); if (el) el.querySelectorAll("button").forEach(x => x.classList.toggle("on", x.dataset.y === yearMode)); });\n'
       '    updHeader();\n'
       '    if (viewMode === "heat") renderHeat();', 'bug', 'maps-24: the year sets the Executive card toggles and the header in every view')
rep(B, '  closePanel();\n  if (v === "heat") renderHeat();', '  closePanel();\n  updHeader();\n  if (v === "heat") renderHeat();', 'bug', 'maps-26: header follows the view (sector hiding applies to the Bubble view)')
# maps-27
rep(B, 'document.querySelectorAll(".ecard .png").forEach(b =>\n  b.addEventListener("click", () => dlPNG(b.dataset.svg)));',
       'document.querySelectorAll(".ecard .png[data-svg]").forEach(b =>   // maps-27: "Show all 60 names" is not an export button\n  b.addEventListener("click", () => dlPNG(b.dataset.svg)));',
    'bug', 'maps-27: "Show all 60 names" no longer calls the PNG export (JS error per click)')
rep(B, '<title>EH Client Portfolio — Packed Bubble Map</title>', '<title>EH Client Portfolio — Packed Bubble Map</title><!-- ' + MARK + ' -->', 'meta', 'applied marker')

# =====================================================================================================================
if FAILURES:
    for f in FAILURES: print('FAILED:', f['file'], '—', f['note'], '|', f['old'][:160].replace('\r', '\\r').replace('\n', '\\n'))
    sys.exit(1)
open(MAP, 'w', encoding='utf-8', newline='').write(TXT['stake'])
open(BUB, 'w', encoding='utf-8', newline='').write(TXT['bub'])
md, js = write_change_table(os.path.join(HERE, 'change_table_audit_maps'), 'Audit round 2 — Stakeholder Map and Client Bubble Map fixes')
print('patched %d edits; change table %s' % (len(patchlib.CHANGES), md))
