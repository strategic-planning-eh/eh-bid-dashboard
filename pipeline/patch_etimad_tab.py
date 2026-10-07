"""patch_etimad_tab.py — 7 Oct 2026. Adds the Government Tenders (Etimad) view to the hub.

1. Hub shell: a fifth top-level view «Government Tenders · المنافسات الحكومية» (desktop tab, mobile tab, loading
   skeleton, lazy iframe f-tenders → etimad_tenders.html). Language and theme reach it through the hub's existing
   postMessage broadcast, like every other view.
2. fetch_from_sheets.py also downloads the private Google Sheet EH_Etimad_data (repository variable SHEET_ID_ETIMAD)
   as etimad_data.xlsx. A failure there never stops the bid build: the tab then says no capture is loaded.
3. update-dashboard.yml builds the page at publish time from that sheet (build_etimad.py → build_etimad_page.py) and
   deletes the downloaded sheet; the page is sealed by encrypt_site.py with everything else. No Etimad data is
   committed to the repo, and none goes into an Actions artefact.
4. visual_check.py checks the new page (6 headline cards, the tender table, charts) but skips the pixel comparison
   for it, because its content changes with every Sunday capture.
5. CHANGES.md: one What's New line.

Run once from the repo root: python3 pipeline/patch_etimad_tab.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P = {'hub': os.path.join(ROOT, 'hub', 'EH_Hub.html'), 'fetch': os.path.join(HERE, 'fetch_from_sheets.py'),
     'vis': os.path.join(HERE, 'visual_check.py'), 'chg': os.path.join(HERE, 'CHANGES.md'),
     'wf': os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml')}
if 'data-f="tenders"' in open(P['hub'], encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
for k, p in P.items():
    load(p, k)

ICON = ('<svg class="ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h5"/>'
        '<path d="M14 3v5h5M8 9h3M8 13h5"/><circle cx="16.5" cy="16.5" r="3"/><path d="M18.7 18.7 21 21"/></svg>')

# ---- 1. hub shell
rep('hub', '    <button class="tab" role="tab" data-f="bubbles"',
    '    <button class="tab" role="tab" data-f="tenders" data-t="Government Tenders" aria-pressed="false" onclick="go(this)" '
    'title="Etimad tenders EH can bid for, refreshed every Sunday · منافسات اعتماد التي يمكن لآفاق البيئة التقدم لها، تُحدَّث كل أحد">'
    + ICON + '<span class="tl" data-en="Government Tenders" data-ar="المنافسات الحكومية">Government Tenders</span></button>\n'
    '    <button class="tab" role="tab" data-f="bubbles"', 'hub', 'Desktop tab, between Bid Intelligence and Clients & Revenue')
rep('hub', '  <button class="mtab" data-f="bubbles"',
    '  <button class="mtab" data-f="tenders" role="tab" onclick="go(document.querySelector(\'.tab[data-f=tenders]\'))">'
    + ICON.replace('class="ic" ', '') + '<span class="tl" data-en="Tenders" data-ar="المنافسات">Tenders</span></button>\n'
    '  <button class="mtab" data-f="bubbles"', 'hub', 'Mobile tab')
rep('hub', '  <div class="skel" id="sk-bubbles">',
    '  <div class="skel" id="sk-tenders"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading government tenders…" '
    'data-ar="جارٍ تحميل المنافسات الحكومية…">Loading government tenders…</span></div></div>\n  <div class="skel" id="sk-bubbles">',
    'hub', 'Loading skeleton')
rep('hub', '  <iframe id="f-bubbles" title="Client portfolio bubble chart"',
    '  <iframe id="f-tenders" title="Government tenders on Etimad that EH can bid for" data-src="etimad_tenders.html" loading="lazy"></iframe>\n'
    '  <iframe id="f-bubbles" title="Client portfolio bubble chart"', 'hub', 'Lazy iframe')

rep('hub', '<span dir="ltr">Four live views of EH\'s market — competitors, tenders, clients &amp; Saudi news</span>',
    '<span dir="ltr">Five live views of EH\'s market — competitors, bids, government tenders, clients &amp; Saudi news</span>', 'hub', 'Subtitle: five views')
rep('hub', 'أربع لوحات حيّة: المنافسون والمناقصات والعملاء والأخبار', 'خمس لوحات حيّة: المنافسون والمناقصات والمنافسات الحكومية والعملاء والأخبار',
    'hub', 'Subtitle (Arabic): five views')

# ---- 2. fetch the private sheet
rep('fetch', """    for file_id, out_name in targets.items():
        download(drive, file_id, out_name)
""", """    for file_id, out_name in targets.items():
        download(drive, file_id, out_name)
    # Government Tenders (Etimad): private Google Sheet EH_Etimad_data, shared only with the robot.
    # Never fatal — without it the tab shows that no capture is loaded.
    if os.environ.get('SHEET_ID_ETIMAD'):
        try:
            download(drive, os.environ['SHEET_ID_ETIMAD'], 'etimad_data.xlsx')
        except Exception as e:
            print(f'  WARNING: Etimad sheet not downloaded ({type(e).__name__}: {e}) — the Government Tenders tab will say no capture is loaded')
    else:
        print('  note: SHEET_ID_ETIMAD not set — the Government Tenders tab will say no capture is loaded')
""", 'fetch', 'Download the Etimad sheet (optional)')

# ---- 3. workflow
rep('wf', """          SHEET_ID_2026: ${{ vars.SHEET_ID_2026 }}
        run: python pipeline/run_pipeline.py""", """          SHEET_ID_2026: ${{ vars.SHEET_ID_2026 }}
          SHEET_ID_ETIMAD: ${{ vars.SHEET_ID_ETIMAD }}
        run: python pipeline/run_pipeline.py""", 'workflow', 'Pass the Etimad sheet ID')
rep('wf', """      - name: Keep the bid-sync report, twin review workbook, aliases and feed (Actions → this run → Artifacts)""",
    """      # ---------- Government Tenders (Etimad): built at publish time from the private sheet; never committed, never an artefact ----------
      - name: Build the Government Tenders page
        run: |
          python pipeline/build_etimad.py --sheet pipeline/etimad_data.xlsx --map site/EH_Stakeholder_Map_CURRENT.html \\
            --tracker pipeline/bids2025.xlsx pipeline/bids2026.xlsx --bidraw pipeline/bidraw2.json --out pipeline/etimad_tenders.json
          python pipeline/build_etimad_page.py pipeline/etimad_tenders.json site/etimad_tenders.html
          rm -f pipeline/etimad_data.xlsx pipeline/etimad_tenders.json

      - name: Keep the bid-sync report, twin review workbook, aliases and feed (Actions → this run → Artifacts)""",
    'workflow', 'Build step after the map sync')

# ---- 4. visual check
rep('vis', "    'pif_strategy_2026_2030.html':     dict(kpi=6, tables=4, svgs=1, canvases=2),",
    "    'pif_strategy_2026_2030.html':     dict(kpi=6, tables=4, svgs=1, canvases=2),\n"
    "    'etimad_tenders.html':             dict(kpi=6, tables=0, svgs=0, nodiff=True),   # content changes with each Sunday capture",
    'visual', 'Check the Etimad page')
rep('vis', "                    if have_baseline and os.path.exists(bpath) and not a.update_baseline:",
    "                    if have_baseline and os.path.exists(bpath) and not a.update_baseline and not want.get('nodiff'):",
    'visual', 'No pixel comparison for pages flagged nodiff')

# ---- 5. What's New
rep('chg', "## 2026-W41\n", "## 2026-W41\n"
    "hub | major | Government Tenders | New view: Government Tenders. Every Sunday, public tenders on Etimad are read, sorted by what EH can bid for "
    "(Core, Adjacent or not relevant, by service line), matched to the stakeholder map and the bid tracker, and shown with deadlines, Priority flags, "
    "where the market is going for EH, a count and sector view of every tender published on Etimad (what the Kingdom is buying), the biggest requesters, agencies that are not yet clients, and the bid-tracker row number for tenders EH has studied or bid on. \"Last captured\" turns amber if the data is more than "
    "8 days old. | عرض جديد: المنافسات الحكومية. كل أحد تُقرأ منافسات اعتماد العامة وتُصنَّف حسب ما يمكن لآفاق البيئة التقدم له (أساسي، مجاور، "
    "أو خارج النطاق، حسب خط الخدمة)، وتُربط بخريطة أصحاب المصلحة وجدول متابعة المنافسات، وتُعرض بمواعيدها وأولويتها واتجاه السوق لآفاق، مع عدد كل المنافسات المنشورة في اعتماد وتوزيعها على القطاعات (ما الذي تشتريه المملكة)، وأكبر الجهات "
    "الطارحة والجهات التي ليست عملاء بعد، ورقم الصف في جدول المنافسات لكل منافسة درستها آفاق أو تقدمت لها. يتحول «آخر التقاط» إلى اللون الكهرماني إذا تجاوز عمر البيانات 8 أيام.\n",
    'whatsnew', 'One What\'s New line')

if FAILURES:
    for f in FAILURES:
        print('FAILED:', f)
    sys.exit('Nothing written — fix the failed edits first.')
for k, p in P.items():
    shutil.copy2(p, p + '.pre-etimad.bak')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(FILES[k])
write_change_table(os.path.join(HERE, 'change_table_etimad_tab'))
print('Applied. Files changed:', ', '.join(os.path.relpath(p, ROOT) for p in P.values()))
