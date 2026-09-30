"""patch_plain_fiscal.py — plain-language pass on the Saudi Fiscal Monitor (News & Intelligence, batch 1, 30 Sep 2026).

Rules (agreed with Youssef): agency names in full the first time on the page, then the short form; periods in plain
words (Jan–Jun, not H1/Q2/FY); units in words (million barrels a day, billion); analyst phrasing rewritten; official
quoted phrases kept verbatim; a short "Words used on this page" glossary; the CONFIDENTIAL label removed (the hub is
now passphrase-protected). Same facts and numbers; element ids, classes and chart data untouched.
Text lives in pipeline/plain_text/fiscal_new.py so the before/after is reviewable. Run once.
"""
import os, sys, re, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
spec = importlib.util.spec_from_file_location('fn', os.path.join(HERE, 'plain_text', 'fiscal_new.py')); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
P = os.path.join(ROOT, 'hub', 'saudi_fiscal_monitor_2026.html'); K = 'saudi_fiscal_monitor_2026.html'
src = open(P, encoding='utf-8').read()
if 'Where the Budget Stands at Mid-Year' in src: sys.exit('Already applied — nothing to do.')
shutil.copy2(P, P + '.pre-plain.bak'); load(P, K); N = 0
def block(a, b):  # exact slice of the current file between two markers
    s = FILES[K]; i = s.index(a); j = s.index(b, i + len(a)); return s[i:j]
marks = ['<body>', '<!-- ============ SECTION 1', '<!-- ============ SECTION 2', '<!-- ============ SECTION 3', '<!-- ============ SECTION 4',
         '<!-- ============ SECTION 5', '<!-- ============ SECTION 6', '<!-- ============ SECTION 7', '<script']
keys = ['nav', '1', '2', '3', '4', '5', '6', '7']
olds = [block(marks[i], marks[i + 1]) for i in range(len(keys))]
for k, old in zip(keys, olds):
    rep(K, old, T.SECTIONS[k], 'plain', f'Page text — {"navigation" if k=="nav" else "section " + k}'); N += 1
for name in ('KPIS', 'SCEN', 'SRC'):
    s = FILES[K]; i = s.index(f'const {name} = ['); j = s.index('];', i) + 2
    rep(K, s[i:j], getattr(T, name), 'plain', f'{name} cards in plain words'); N += 1
for a, b in T.JS_STRINGS:
    rep(K, a, b, 'plain', 'Chart wording'); N += 1
for a, b, c in T.JS_MULTI:
    rep(K, a, b, 'plain', 'Chart tooltip wording', count=c); N += 1
old_ar = block('<div id="ehArView"', '<script')
rep(K, old_ar, T.AR_VIEW + '\n', 'plain', 'Arabic view in plain Arabic (confidential label removed)'); N += 1
rep(K, '<title>Saudi Arabia Fiscal Monitor 2026 — v4: H1 Actuals & the Red Sea Front</title>', '<title>Saudi Government Finances 2026 — mid-year position and the Red Sea attacks</title>', 'plain', 'Browser tab title'); N += 1
open(P, 'w', encoding='utf-8').write(FILES[K])
# hub tab label (the page itself is renamed above)
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); shutil.copy2(H, H + '.pre-plain.bak'); load(H, 'EH_Hub.html')
rep('EH_Hub.html', '<span class="tl" data-en="Saudi Fiscal Monitor 2026" data-ar="مرصد المالية السعودية 2026">Saudi Fiscal Monitor 2026</span>',
    '<span class="tl" data-en="Saudi Government Finances 2026" data-ar="مالية الحكومة السعودية 2026">Saudi Government Finances 2026</span>', 'plain', 'Hub tab label'); N += 1
open(H, 'w', encoding='utf-8').write(FILES['EH_Hub.html'])
write_change_table(os.path.join(HERE, 'change_table_plain_fiscal'), 'Change table — plain-language Fiscal Monitor')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note'], f['old'][:120]) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
