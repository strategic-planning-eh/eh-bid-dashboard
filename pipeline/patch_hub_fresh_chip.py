"""patch_hub_fresh_chip.py — "Data refreshed <date, time>" back beside the hub title.

The chip (#fresh) has been in the header all along, but the What's New rework changed how it is shown: setFresh() only
removes the `hidden` attribute, while the base rule `.fresh{…display:none}` still wins — so on desktop the chip never
appeared, and on tablets/phones two media queries hide it outright. Now:
  • base rule shows it (inline-flex, beside the brand block); `.fresh[hidden]` hides it until build_info.json loads
  • tablet (≤820px) keeps it; only phones (≤640px) hide it, where the header is already a packed grid
  • the chip reads "Data refreshed 13 Sep, 14:05 KSA" (time zone made explicit — the value is already Riyadh time)
Run once: python3 pipeline/patch_hub_fresh_chip.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P = os.path.join(HERE, '..', 'hub', 'EH_Hub.html')
if '.fresh[hidden]' in open(P, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(P, os.path.join(HERE, 'EH_Hub.html.pre-fresh.bak')); load(P, 'hub')
rep('hub', ".fresh{font-size:10.5px;color:var(--mut);background:#F0F5F2;border:1px solid #DCE8DF;border-radius:20px;padding:4px 12px;display:none}",
    ".fresh{font-size:11px;color:var(--mut);background:#F0F5F2;border:1px solid #DCE8DF;border-radius:20px;padding:4px 12px;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;align-self:center}\n.fresh[hidden]{display:none}\nbody.dark .fresh{background:rgba(31,122,76,.18);border-color:rgba(31,122,76,.4)}",
    'fresh-chip', 'Chip is visible by default; hidden only until the build stamp loads; dark-mode colours')
rep('hub', "  #q{order:9;flex:1 1 100%;min-width:0;max-width:none;width:auto !important}\n  .fresh{display:none !important}\n",
    "  #q{order:9;flex:1 1 100%;min-width:0;max-width:none;width:auto !important}\n", 'fresh-chip', 'Tablet width keeps the chip')
rep('hub', "function fmtFresh(iso){var d=new Date(iso);if(isNaN(d))return String(iso||'').slice(0,16);",
    "function fmtFresh(iso){var d=new Date(iso);if(isNaN(d))return String(iso||'').slice(0,16);var _r=fmtFresh0(d);return _r?_r+' KSA':_r;}\nfunction fmtFresh0(d){", 'fresh-chip', 'Time zone shown explicitly (KSA)')
open(P, 'w', encoding='utf-8').write(FILES['hub'])
write_change_table(os.path.join(HERE, 'change_table_hub_fresh_chip'), 'Change table — hub: Data refreshed chip beside the title')
print('edits:', 3 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
