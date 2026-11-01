"""patch_saudi_ports_tab.py — adds the "Saudi ports" sub-tab to News & Intelligence (1 Nov 2026).

New file shipped alongside (not patched, just added):
  hub/saudi_ports_map.html   the Saudi Ports Intelligence Map (Youssef's 22 Oct build, v3): local fonts instead of
                             Google Fonts, and it follows the hub's language and theme buttons.

Edits made here:
  hub/EH_Hub.html                         sub-tab button, skeleton, lazy iframe, tab switcher list, search aliases
  .github/workflows/update-dashboard.yml  the page is published
Run once: python3 pipeline/patch_saudi_ports_tab.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); W = os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml')
if 'data-n="ports"' in open(H, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (H, W): load(p, os.path.basename(p))

WASTE_BTN = '<span class="newb tl" data-new-until="2026-10-27" data-en="New" data-ar="جديد">New</span></button>'
rep('EH_Hub.html', WASTE_BTN,
    WASTE_BTN + '\n      <button class="nsub" data-n="ports" title="Saudi ports — operators, capacities, waste reception and EH\'s position at each port · الموانئ السعودية — المشغّلون والطاقات واستقبال النفايات وموقع آفاق البيئة في كل ميناء"><span class="tl" data-en="Saudi ports" data-ar="الموانئ السعودية">Saudi ports</span><span class="newb tl" data-new-until="2026-11-15" data-en="New" data-ar="جديد">New</span></button>',
    'ports-tab', 'Saudi ports sub-tab button after Saudi waste')
WASTE_IF = '<iframe id="f-waste" title="Saudi waste — where the Kingdom\'s waste is generated and where it piles up" data-src="saudi_waste.html" loading="lazy" style="display:none"></iframe>'
rep('EH_Hub.html', WASTE_IF,
    WASTE_IF + '\n      <div class="skel" id="sk-ports"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading Saudi ports…" data-ar="جارٍ تحميل الموانئ السعودية…">Loading Saudi ports…</span></div></div>\n'
    '      <iframe id="f-ports" title="Saudi Ports Intelligence Map" data-src="saudi_ports_map.html" loading="lazy" style="display:none"></iframe>',
    'ports-tab', 'Skeleton + lazy iframe for the tab page')
rep('EH_Hub.html', "['v2030','fiscal','corp','gov','pif','strat','ef2025','waste']", "['v2030','fiscal','corp','gov','pif','strat','ef2025','waste','ports']", 'ports-tab', 'Tab switcher knows the new frame')
rep('EH_Hub.html', "'saudi waste':'waste',", "'saudi waste':'waste','saudi ports':'ports','ports map':'ports','saudi ports intelligence map':'ports','الموانئ السعودية':'ports',", 'ports-tab', 'Hub search opens the tab by name')
rep('update-dashboard.yml', "          cp hub/saudi_waste.html site/ 2>/dev/null || true\n",
    "          cp hub/saudi_waste.html site/ 2>/dev/null || true\n          cp hub/saudi_ports_map.html site/ 2>/dev/null || true\n", 'ports-tab', 'Tab page is published')

for p in (H, W): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_saudi_ports_tab'), 'Change table — Saudi ports tab')
print('edits:', 5 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
