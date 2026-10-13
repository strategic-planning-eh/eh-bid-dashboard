"""patch_saudi_waste_tab.py — adds the "Saudi waste" sub-tab to News & Intelligence (13 Oct 2026).

New files shipped alongside (not patched, just added):
  pipeline/sources/gastat_waste/*.xlsx          GASTAT Environment Statistics 2021–2024 + SEEA Waste 2024 (public releases)
  pipeline/sources/ne_sau_adm1_simplified.geojson  region boundaries (Natural Earth, public domain, simplified)
  pipeline/extract_saudi_waste.py               workbooks → pipeline/saudi_waste_data.json (cells read by position)
  pipeline/build_saudi_waste_page.py            JSON → hub/saudi_waste.html
  hub/saudi_waste.html                          the tab page

Edits made here:
  hub/EH_Hub.html                         sub-tab button, skeleton, lazy iframe, tab switcher list, search aliases
  .github/workflows/update-dashboard.yml  the page is published
Run once: python3 pipeline/patch_saudi_waste_tab.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); W = os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml')
if 'data-n="waste"' in open(H, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (H, W): load(p, os.path.basename(p))

EF_BTN = '<span class="tl" data-en="Environment Fund 2025 Report" data-ar="تقرير صندوق البيئة 2025">Environment Fund 2025 Report</span><span class="newb tl" data-new-until="2026-10-06" data-en="New" data-ar="جديد">New</span></button>'
rep('EH_Hub.html', EF_BTN,
    EF_BTN + '\n      <button class="nsub" data-n="waste" title="Saudi waste — where the Kingdom\'s waste is generated and where it piles up · النفايات في المملكة — أين تتولد وأين تتراكم"><span class="tl" data-en="Saudi waste" data-ar="النفايات في المملكة">Saudi waste</span><span class="newb tl" data-new-until="2026-10-27" data-en="New" data-ar="جديد">New</span></button>',
    'waste-tab', 'Saudi waste sub-tab button after the Environment Fund report')
EF_IF = '<iframe id="f-ef2025" title="Environment Fund 2025 Annual Report — what it means for EH" data-src="environment_fund_2025.html" loading="lazy" style="display:none"></iframe>'
rep('EH_Hub.html', EF_IF,
    EF_IF + '\n      <div class="skel" id="sk-waste"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading Saudi waste…" data-ar="جارٍ تحميل النفايات في المملكة…">Loading Saudi waste…</span></div></div>\n'
    '      <iframe id="f-waste" title="Saudi waste — where the Kingdom\'s waste is generated and where it piles up" data-src="saudi_waste.html" loading="lazy" style="display:none"></iframe>',
    'waste-tab', 'Skeleton + lazy iframe for the tab page')
rep('EH_Hub.html', "['v2030','fiscal','corp','gov','pif','strat','ef2025']", "['v2030','fiscal','corp','gov','pif','strat','ef2025','waste']", 'waste-tab', 'Tab switcher knows the new frame')
rep('EH_Hub.html', "'environment fund 2025 report':'ef2025',", "'environment fund 2025 report':'ef2025','saudi waste':'waste','waste statistics':'waste','hazardous waste':'waste','النفايات في المملكة':'waste',", 'waste-tab', 'Hub search opens the tab by name')
rep('update-dashboard.yml', "          cp hub/government_news.html site/ 2>/dev/null || true\n",
    "          cp hub/government_news.html site/ 2>/dev/null || true\n          cp hub/saudi_waste.html site/ 2>/dev/null || true\n", 'waste-tab', 'Tab page is published')

for p in (H, W): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_saudi_waste_tab'), 'Change table — Saudi waste tab')
print('edits:', 5 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
