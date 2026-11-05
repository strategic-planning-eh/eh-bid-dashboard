"""patch_map_list_filters.py — Stakeholder Map: List View layout, category filter, clear-all, EMCO note (5 Nov 2026).

Youssef's five-point request:
  1. List View: the empty "Company detail" column is hidden while nothing is selected, so the table takes the width;
     clicking a row brings the panel back (with a close button on desktop too).
  2. Left menu: new "Stakeholder category" chip filter (Active Competitors, Direct Competitors, EH Clients …) —
     the map's Category field, which he calls company type; the existing "Company type" boxes (typ) stay as they are.
  3. EMCO (شركة قياس البيئة المحدودة): note that it is a sister company of EH.
  4. Left menu: "Clear all filters" button at the top (same action as the header's Reset filters).
  5. (workbook rebuilt separately with pipeline/analysis/build_v9_workbook.py)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table, css_min

M = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
if 'catgChips' in FILES['map']: sys.exit('Already applied.')
ok = []

# ---- 1. List View: hide the empty detail column, widen the table
CSS = css_min("""<style id="eh-list-filters">
/* 5 Nov 2026: List View — no empty detail column until a row is clicked */
@media(min-width:1101px){
  .wrap.listmode:has(#detail:not(.has)){grid-template-columns:268px minmax(0,1fr)}
  .wrap.listmode:has(#detail:not(.has)) #detail{display:none}
  .wrap.listmode #detail.has .dclose{display:flex;position:sticky;top:0;margin-inline-start:auto;width:36px;height:36px;align-items:center;justify-content:center;border:0;border-radius:18px;background:var(--eh-tint,var(--mist));color:var(--eh-ink,var(--ink));font-size:22px;cursor:pointer;z-index:2}
}
@media(min-width:1101px) and (max-width:1400px){.wrap.listmode:has(#detail:not(.has)){grid-template-columns:224px minmax(0,1fr)}}
#clearAllWrap{padding:12px 16px 10px;border-bottom:1px solid var(--eh-line,var(--mist))}
#clearAllBtn{width:100%;justify-content:center}
</style></head>""")
ok.append(rep('map', '</head>', CSS, 'list-filters', 'CSS: list mode hides the empty detail column; clear-all button block'))
ok.append(rep('map', "  if(t==='map')resize();\n  if(t==='list')buildList();",
              "  try{document.querySelector('.wrap').classList.toggle('listmode',t==='list');}catch(e){}\n  if(t==='map')resize();\n  if(t==='list')buildList();",
              'list-filters', 'switchTab: .wrap gets .listmode while the List View is open'))

# ---- 4. Clear all filters (top of the left menu) + 2. Stakeholder category chips (above Company type)
ok.append(rep('map', '  <div class="panel side" id="sidePanel">\n    <h3>Search company</h3>',
              '  <div class="panel side" id="sidePanel">\n    <div id="clearAllWrap"><button class="btn" id="clearAllBtn" type="button" onclick="resetFilters()">Clear all filters</button></div>\n    <h3>Search company</h3>',
              'list-filters', 'Side panel: "Clear all filters" button at the top'))
ok.append(rep('map', '    <h3>Company type</h3>\n    <section id="catFilters"></section>',
              '    <h3>Stakeholder category</h3>\n    <section><div class="chips" id="catgChips"></div></section>\n    <h3>Company type</h3>\n    <section id="catFilters"></section>',
              'list-filters', 'Side panel: "Stakeholder category" chip group (Active Competitors, Direct Competitors, EH Clients …)'))
ok.append(rep('map', " ['Company type','\\u0646\\u0648\\u0639 \\u0627\\u0644\\u0634\\u0631\\u0643\\u0629'],",
              " ['Company type','\\u0646\\u0648\\u0639 \\u0627\\u0644\\u0634\\u0631\\u0643\\u0629'],\n ['Stakeholder category','فئة الطرف'],\n ['Clear all filters','مسح كل الفلاتر'],",
              'list-filters', 'STATIC_TR: Arabic for the two new labels'))

# state + filter + chips + badge + reset + language
ok.append(rep('map', "const state = {cats:new Set(), regs:new Set(), tiers:new Set(), freqs:new Set(),",
              "const state = {cats:new Set(), catg:new Set(), regs:new Set(), tiers:new Set(), freqs:new Set(),",
              'list-filters', 'state.catg (selected stakeholder categories)'))
ok.append(rep('map', "  if(!state.cats.has(n.typ||'Other'))return false;\n  if(state.regs.size && !state.regs.has(n.rg))return false;",
              "  if(!state.cats.has(n.typ||'Other'))return false;\n  if(state.catg.size && !state.catg.has(n.cat))return false;\n  if(state.regs.size && !state.regs.has(n.rg))return false;",
              'list-filters', 'visible(): category filter'))
ok.append(rep('map', "ch.textContent=(elId==='regChips'?regL(v):elId==='tierChips'?tierL(v):elId==='freqChips'?freqL(v):v);",
              "ch.textContent=(elId==='regChips'?regL(v):elId==='tierChips'?tierL(v):elId==='freqChips'?freqL(v):elId==='catgChips'?catS(v):v);",
              'list-filters', 'chipGroup: category chips labelled in the current language'))
ok.append(rep('map', "chipGroup('tierChips',TIERS,state.tiers);",
              "chipGroup('tierChips',TIERS,state.tiers);\nconst CATG_LIST=Object.keys(CAT_RING).filter(c=>c!=='EH (Reference)'&&NODES.some(n=>n.cat===c)).sort((a,b)=>CAT_RING[a]-CAT_RING[b]||a.localeCompare(b));\nchipGroup('catgChips',CATG_LIST,state.catg);",
              'list-filters', 'build the category chips (ring order: regulators → competitors → partners → clients → suppliers)'))
ok.append(rep('map', "    ch.textContent=(box==='regChips'?regL(v):box==='tierChips'?tierL(v):box==='freqChips'?freqL(v):v);",
              "    ch.textContent=(box==='regChips'?regL(v):box==='tierChips'?tierL(v):box==='freqChips'?freqL(v):box==='catgChips'?catS(v):v);",
              'list-filters', 'applyLang: category chips re-labelled on language switch'))
ok.append(rep('map', "var n=(state.cats?state.cats.size:0)+(state.regs?state.regs.size:0)",
              "var n=(state.cats?state.cats.size:0)+(state.catg?state.catg.size:0)+(state.regs?state.regs.size:0)",
              'list-filters', 'mobile filter badge counts the category filter'))
ok.append(rep('map', "  state.regs.clear();state.tiers.clear();state.type='';state.sector='';state.lic='';",
              "  state.regs.clear();state.catg.clear();state.tiers.clear();state.type='';state.sector='';state.lic='';",
              'list-filters', 'resetFilters / Clear all filters clears the category filter too'))

# ---- 3. EMCO — sister company of EH
ok.append(rep('map', '"notes": "EH Relationship Score: 47/100, Tier 3 (verified — EMCO environmental lab).',
              '"notes": "Sister company of Environmental Horizons (EH) — EMCO, Environmental Measurement Co. (شركة قياس البيئة المحدودة). EH Relationship Score: 47/100, Tier 3 (verified — EMCO environmental lab).',
              'list-filters', 'EMCO (شركة قياس البيئة المحدودة): note — sister company of EH'))

if not all(ok): sys.exit('ANCHOR MISMATCH: ' + str(ok))
open(M, 'w', encoding='utf-8').write(FILES['map'])
write_change_table(os.path.join(HERE, 'change_table_map_list_filters'), 'Change table — Stakeholder Map list/filters/EMCO (5 Nov 2026)'); print('applied', len(ok), 'edits')
