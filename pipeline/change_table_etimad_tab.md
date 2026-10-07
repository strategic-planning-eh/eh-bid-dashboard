# Change table

Generated 2026-10-07 10:58 · 12 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | hub | exact | hub | Desktop tab, between Bid Intelligence and Clients & Revenue | 1 | ✓ |
| 2 | hub | exact | hub | Mobile tab | 1 | ✓ |
| 3 | hub | exact | hub | Loading skeleton | 1 | ✓ |
| 4 | hub | exact | hub | Lazy iframe | 1 | ✓ |
| 5 | hub | exact | hub | Subtitle: five views | 1 | ✓ |
| 6 | hub | exact | hub | Subtitle (Arabic): five views | 1 | ✓ |
| 7 | fetch | exact | fetch | Download the Etimad sheet (optional) | 1 | ✓ |
| 8 | wf | exact | workflow | Pass the Etimad sheet ID | 1 | ✓ |
| 9 | wf | exact | workflow | Build step after the map sync | 1 | ✓ |
| 10 | vis | exact | visual | Check the Etimad page | 1 | ✓ |
| 11 | vis | exact | visual | No pixel comparison for pages flagged nodiff | 1 | ✓ |
| 12 | chg | exact | whatsnew | One What's New line | 1 | ✓ |

## Edit detail

### 1. hub — Desktop tab, between Bid Intelligence and Clients & Revenue

**Old**
```
    <button class="tab" role="tab" data-f="bubbles"
```
**New**
```
    <button class="tab" role="tab" data-f="tenders" data-t="Government Tenders" aria-pressed="false" onclick="go(this)" title="Etimad tenders EH can bid for, refreshed every Sunday · منافسات اعتماد التي يمكن لآفاق البيئة التقدم لها، تُحدَّث كل أحد"><svg class="ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round
```

### 2. hub — Mobile tab

**Old**
```
  <button class="mtab" data-f="bubbles"
```
**New**
```
  <button class="mtab" data-f="tenders" role="tab" onclick="go(document.querySelector('.tab[data-f=tenders]'))"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h5"/><path d="M14 3v5h5M8 9h3M8 13h5"/><circle cx="16.5" cy="16.5" r="3"/><path d="M18.7 18.7 21 21
```

### 3. hub — Loading skeleton

**Old**
```
  <div class="skel" id="sk-bubbles">
```
**New**
```
  <div class="skel" id="sk-tenders"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading government tenders…" data-ar="جارٍ تحميل المنافسات الحكومية…">Loading government tenders…</span></div></div>
  <div class="skel" id="sk-bubbles">
```

### 4. hub — Lazy iframe

**Old**
```
  <iframe id="f-bubbles" title="Client portfolio bubble chart"
```
**New**
```
  <iframe id="f-tenders" title="Government tenders on Etimad that EH can bid for" data-src="etimad_tenders.html" loading="lazy"></iframe>
  <iframe id="f-bubbles" title="Client portfolio bubble chart"
```

### 5. hub — Subtitle: five views

**Old**
```
<span dir="ltr">Four live views of EH's market — competitors, tenders, clients &amp; Saudi news</span>
```
**New**
```
<span dir="ltr">Five live views of EH's market — competitors, bids, government tenders, clients &amp; Saudi news</span>
```

### 6. hub — Subtitle (Arabic): five views

**Old**
```
أربع لوحات حيّة: المنافسون والمناقصات والعملاء والأخبار
```
**New**
```
خمس لوحات حيّة: المنافسون والمناقصات والمنافسات الحكومية والعملاء والأخبار
```

### 7. fetch — Download the Etimad sheet (optional)

**Old**
```
    for file_id, out_name in targets.items():
        download(drive, file_id, out_name)

```
**New**
```
    for file_id, out_name in targets.items():
        download(drive, file_id, out_name)
    # Government Tenders (Etimad): private Google Sheet EH_Etimad_data, shared only with the robot.
    # Never fatal — without it the tab shows that no capture is loaded.
    if os.environ.get('SHEET_ID_ETIMAD'):
        try:
            download(drive, os.environ['SHEET_ID_ETIMAD'], 'etimad_data.xlsx')
     
```

### 8. wf — Pass the Etimad sheet ID

**Old**
```
          SHEET_ID_2026: ${{ vars.SHEET_ID_2026 }}
        run: python pipeline/run_pipeline.py
```
**New**
```
          SHEET_ID_2026: ${{ vars.SHEET_ID_2026 }}
          SHEET_ID_ETIMAD: ${{ vars.SHEET_ID_ETIMAD }}
        run: python pipeline/run_pipeline.py
```

### 9. wf — Build step after the map sync

**Old**
```
      - name: Keep the bid-sync report, twin review workbook, aliases and feed (Actions → this run → Artifacts)
```
**New**
```
      # ---------- Government Tenders (Etimad): built at publish time from the private sheet; never committed, never an artefact ----------
      - name: Build the Government Tenders page
        run: |
          python pipeline/build_etimad.py --sheet pipeline/etimad_data.xlsx --map site/EH_Stakeholder_Map_CURRENT.html \
            --tracker pipeline/bids2025.xlsx pipeline/bids2026.xlsx --bidraw
```

### 10. vis — Check the Etimad page

**Old**
```
    'pif_strategy_2026_2030.html':     dict(kpi=6, tables=4, svgs=1, canvases=2),
```
**New**
```
    'pif_strategy_2026_2030.html':     dict(kpi=6, tables=4, svgs=1, canvases=2),
    'etimad_tenders.html':             dict(kpi=6, tables=0, svgs=0, nodiff=True),   # content changes with each Sunday capture
```

### 11. vis — No pixel comparison for pages flagged nodiff

**Old**
```
                    if have_baseline and os.path.exists(bpath) and not a.update_baseline:
```
**New**
```
                    if have_baseline and os.path.exists(bpath) and not a.update_baseline and not want.get('nodiff'):
```

### 12. chg — One What's New line

**Old**
```
## 2026-W41

```
**New**
```
## 2026-W41
hub | major | Government Tenders | New view: Government Tenders. Every Sunday, public tenders on Etimad are read, sorted by what EH can bid for (Core, Adjacent or not relevant, by service line), matched to the stakeholder map and the bid tracker, and shown with deadlines, Priority flags, where the market is going, the biggest requesters and agencies that are not yet clients. "Last capt
```
