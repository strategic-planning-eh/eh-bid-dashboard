"""patch_kpi_label_wrap.py — Bid & Tender app: KPI labels no longer spill out of their card.

"Avg participants/tender" had no break opportunity at the slash, and .kc did not clip overflow, so the label ran past the
card edge once the shared 12px text floor enlarged it. Two edits in the generator (the app is rebuilt every run):
  • app.js        label reads "Avg participants / tender" (spaces give the browser a place to wrap), AR unchanged.
  • build_bid_dashboard.py  .kc .l wraps anywhere as a last resort and .kc clips overflow.
Run once: python3 pipeline/patch_kpi_label_wrap.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
A = os.path.join(HERE, 'app.js'); G = os.path.join(HERE, 'build_bid_dashboard.py')
if 'overflow-wrap:anywhere' in open(G, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (A, G): shutil.copy2(p, p + '.pre-kpilbl.bak'); load(p, os.path.basename(p))
rep('app.js', "t('Avg participants/tender','متوسط المشاركين بالمنافسة')", "t('Avg participants / tender','متوسط المشاركين بالمنافسة')", 'kpi-label', 'Label gets a wrap point at the slash')
rep('build_bid_dashboard.py', ".kc{background:#fff;border:1px solid #E3EAE5;border-radius:12px;padding:13px 15px;box-shadow:0 1px 3px rgba(0,0,0,.03)}",
    ".kc{background:#fff;border:1px solid #E3EAE5;border-radius:12px;padding:13px 15px;box-shadow:0 1px 3px rgba(0,0,0,.03);overflow:hidden;min-width:0}", 'kpi-label', 'Card clips its content')
rep('build_bid_dashboard.py', ".kc .l{font-size:10.5px;color:#6B7C86;text-transform:uppercase;letter-spacing:.5px;margin-top:4px;font-weight:600}",
    ".kc .l{font-size:10.5px;color:#6B7C86;text-transform:uppercase;letter-spacing:.5px;margin-top:4px;font-weight:600;overflow-wrap:anywhere;line-height:1.3}", 'kpi-label', 'Label wraps inside the card instead of overflowing')
for p in (A, G): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_kpi_label_wrap'), 'Change table — KPI label wrap (Bid & Tender)')
print('edits:', 3 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
