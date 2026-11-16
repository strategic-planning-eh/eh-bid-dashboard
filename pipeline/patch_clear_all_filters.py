#!/usr/bin/env python3
"""16 Nov 2026 — Stakeholder Map: "Clear all filters" now clears everything (Youssef).
Before: it reset to every company type ticked, so all companies were shown.
Now: every filter is cleared AND every "Company type" box is unticked, so nothing is shown until a type is chosen.
The header "Reset filters" button is unchanged (still returns to all companies)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table

M = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
if 'No company types are selected.' in FILES['map']: sys.exit('Already applied.')
DONE1 = 'function clearAllFilters' in FILES['map']
ok = [] if DONE1 else [
 rep('map', '<button class="btn" id="clearAllBtn" type="button" onclick="resetFilters()">Clear all filters</button>',
     '<button class="btn" id="clearAllBtn" type="button" onclick="clearAllFilters()">Clear all filters</button>', 'clear-all', 'Side panel button calls the new function'),
 rep('map', '\nfunction resetFilters(){\n',
     "\nfunction clearAllFilters(){   /* 16 Nov 2026: clear = nothing ticked, nothing shown */\n"
     "    resetFilters(); state.cats.clear();\n"
     "    document.querySelectorAll('#catFilters input[type=checkbox]').forEach(function(i){i.checked=false;});\n"
     "    state.sel=null; recompute();\n"
     "}\n"
     "function resetFilters(){\n", 'clear-all', 'New clearAllFilters(): unticks every company type'),
]
ok += [
 rep('map', 'The map opens with <b>no filters selected</b>.<br>Tick company types in the Filters panel to populate it — or<br>',
     '<p style="margin:0;font-weight:700;color:#1C2B33">No company types are selected.</p><p style="margin:4px 0 0">Tick company types in the Filters panel to show companies — or</p>', 'clear-all', 'Empty-state message matches the new behaviour'),
 rep('map', "const STATIC_TR=[", "const STATIC_TR=[['No company types are selected.','لم يُحدَّد أي نوع من الشركات.'],['Tick company types in the Filters panel to show companies — or','حدّد أنواع الشركات من لوحة الفلاتر لعرض الشركات — أو'],['Show everything','عرض الكل'],",
     'clear-all', 'Arabic for the empty-state message'),
]
if not all(ok): sys.exit('Patch failed — nothing written.')
with open(M, 'w', encoding='utf-8') as f: f.write(FILES['map'])
write_change_table(os.path.join(HERE, 'change_table_clear_all_filters'), 'Clear all filters shows nothing')
print('done')
