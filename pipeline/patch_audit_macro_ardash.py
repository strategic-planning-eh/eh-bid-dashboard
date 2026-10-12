"""patch_audit_macro_ardash.py — audit fixes in hub/eh-ar-dashboard.js, the Arabic layer shared by the Saudi Government
Finances page and the News Intelligence page (12 Oct 2026, judge J3, ids macro-02, macro-05, macro-07, macro-12, macro-13).

What was wrong and what changes:
  • macro-05 / macro-12 — Finances page, Arabic: the in-place Arabic swap skipped any block without two Latin letters
    in a row, so number-only cells ("1,172 → 1,259", "245B") could never be given an Arabic version, however the
    dictionary was written. A block is now also swapped when the dictionary holds a different Arabic version of it.
    (The dictionary entries themselves are added by patch_audit_macro_fisc.py.)
  • macro-13 — the renamed Finances labels ("Economic growth, 2026"; chart E's "EH reference: 2025 average price …")
    get their Arabic names in the chart/label dictionaries.
  • macro-02 — News: the oil-price card is relabelled "Oil price (Brent), close on 25/08" (it was "today"); its Arabic
    name follows.
  • macro-07 — News, Arabic: the English filter bar (it filters only the English sections, which are hidden in Arabic)
    and the English methodology/coverage footer stayed on screen. Both are now hidden in Arabic — the Arabic report
    carries its own methodology note. Any element that carries an Arabic twin in a data-eh-ar attribute (the key-figure
    notes and the chart note on the News page) now shows it in Arabic and returns to English when switched back.

Exact-string edits; stops if an anchor is missing.   Run once:  python3 pipeline/patch_audit_macro_ardash.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'eh-ar-dashboard.js')
if 'data-eh-ar' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'ard')

rep('ard', "if(v!=null&&/[A-Za-z]{2}/.test(el.textContent)){",
    "if(v!=null&&(/[A-Za-z]{2}/.test(el.textContent)||v!==el.innerHTML)){",
    'code', 'macro-05/12: number-only blocks are swapped when the dictionary has an Arabic version')
rep('ard', "'Size of the economy, 2026':'حجم الاقتصاد، 2026',",
    "'Size of the economy, 2026':'حجم الاقتصاد، 2026','Economic growth, 2026':'النمو الاقتصادي، 2026',",
    'copy', 'macro-13: Arabic for the renamed growth card')
rep('ard', "'Price the budget assumed ($69.9, 2025 average)':'السعر المفترض في الميزانية (69.9 دولارًا، متوسط 2025)',",
    "'Price the budget assumed ($69.9, 2025 average)':'السعر المفترض في الميزانية (69.9 دولارًا، متوسط 2025)',"
    "'EH reference: 2025 average price ($69.9) — the Ministry publishes no oil-price assumption':"
    "'مرجع آفاق البيئة: متوسط سعر 2025 (69.9 دولارًا) — لا تنشر الوزارة سعرًا مفترضًا للنفط',",
    'copy', 'macro-13: Arabic for the renamed chart E reference line')
rep('ard', "'Oil price today (Brent, 25/08)':'سعر النفط اليوم (برنت، 25/08)'}",
    "'Oil price today (Brent, 25/08)':'سعر النفط اليوم (برنت، 25/08)','Oil price (Brent), close on 25/08':'سعر النفط (برنت)، إغلاق 25/08'}",
    'copy', 'macro-02: Arabic for the relabelled oil-price card')
rep('ard', "enOnly:['#sec-audit','#sec-corp','#sec-gov','#sec-flag','#sec-hl','aside.panel'],",
    "enOnly:['#sec-audit','#sec-corp','#sec-gov','#sec-flag','#sec-hl','aside.panel','#filterbar','footer.foot'],",
    'code', 'macro-07: English filter bar and methodology footer hidden in Arabic')
rep('ard', "    relabelCharts(ar);\n    if(window.EH_SHARED&&EH_SHARED.floorText) setTimeout(EH_SHARED.floorText,50);\n  }",
    "    /* audit 12/10 (macro-07): elements with an Arabic twin in data-eh-ar */\n"
    "    $$('[data-eh-ar]').forEach(function(el){ if(el.dataset.ehEn==null) el.dataset.ehEn=el.innerHTML; el.innerHTML=ar?el.getAttribute('data-eh-ar'):el.dataset.ehEn; });\n"
    "    relabelCharts(ar);\n    if(window.EH_SHARED&&EH_SHARED.floorText) setTimeout(EH_SHARED.floorText,50);\n  }",
    'code', 'macro-07: data-eh-ar twins (KPI notes, chart note) shown in Arabic')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['ard'])
md, _ = write_change_table(os.path.join(HERE, 'change_table_audit_macro_ardash'), 'Audit fixes — Arabic dashboard layer (macro)')
print('patched eh-ar-dashboard.js;', md)
