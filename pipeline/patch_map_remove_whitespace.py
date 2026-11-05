"""patch_map_remove_whitespace.py — Licence Map: remove the "White space — licences almost no one holds" section (5 Nov 2026, Youssef).

Drops the heading, the table and the closing moat/exposed-lines sentence from buildLicenceMap(). The data block
(BA.licenses.white_space) is untouched, so the section can be restored by reverting this patch.
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep_re, FILES, write_change_table

M = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
if 'White space' not in FILES['map']: sys.exit('Already applied.')
ok = rep_re('map',
    r"  h\+='<div class=\"biz-sec\">'\+t\('White space — licences almost no one holds \(opportunity\)'.*?\n(  document\.getElementById\('licView'\)\.innerHTML=h;)",
    r"  /* 5 Nov 2026: 'White space — licences almost no one holds' section removed at Youssef's request (data kept in BA.licenses.white_space) */\n\1",
    'licence-map', 'Licence Map: white-space heading, table and closing sentence removed')
if not ok: sys.exit('ANCHOR MISMATCH')
open(M, 'w', encoding='utf-8').write(FILES['map'])
write_change_table(os.path.join(HERE, 'change_table_map_remove_whitespace'), 'Change table — Licence Map white-space section removed (5 Nov 2026)'); print('applied')
