"""patch_ar_swap_floor.py — Arabic labels on the fiscal page no longer stay in English (12 Oct 2026).

Cause: hub/eh-ar-dashboard.js finds the Arabic twin of each English text block by its exact HTML. The shared 12px
reading floor (eh-shared.js) enlarges very small text by writing an inline font size onto those elements, which changes
their HTML, so blocks such as the key-figure labels, source tags, risk pills and top badges no longer matched and kept
their English. The lookup now also tries the block with inline style attributes removed (on both sides), so a size
change can never hide a translation again. Exact matches still win; nothing else changes.

Run once:  python3 pipeline/patch_ar_swap_floor.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

J = os.path.join(HERE, '..', 'hub', 'eh-ar-dashboard.js')
if 'FULLN' in open(J, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(J, 'ar')
rep('ar', "  var normH=function(h){ return String(h).replace(/\\s+/g,' ').trim(); };\n",
    "  var normH=function(h){ return String(h).replace(/\\s+/g,' ').trim(); };\n"
    "  /* 12 Oct 2026: match a block even when the reading floor has added an inline font size (style attributes ignored) */\n"
    "  var noSt=function(h){ return normH(String(h).replace(/\\s+style=\"[^\"]*\"/g,'')); };\n"
    "  var FULLN=null; if(FULL){ FULLN={}; for(var fk in FULL){ if(fk.indexOf('#text:')!==0) FULLN[noSt(fk)]=FULL[fk]; } }\n",
    'fix', 'style-insensitive lookup table')
rep('ar', "var k=normH(el.innerHTML); var v=FULL[k];",
    "var k=normH(el.innerHTML); var v=FULL[k]; if(v==null&&FULLN) v=FULLN[noSt(el.innerHTML)];",
    'fix', 'fall back to the style-insensitive match')
# chart B's 'Other' spending line had no Arabic label (the news page's dictionary had one, the fiscal one did not)
rep('ar', "'Salaries':'الرواتب',", "'Salaries':'الرواتب','Other':'أخرى',", 'fix', 'Arabic label for Other in chart B')
if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(J, 'w', encoding='utf-8').write(FILES['ar'])
write_change_table(os.path.join(HERE, 'change_table_ar_swap_floor'), 'Arabic swap ignores the reading-floor font size')
print('patched: hub/eh-ar-dashboard.js')
