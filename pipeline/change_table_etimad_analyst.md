# Government Tenders — Analyst view (Stage 2)

Generated 2026-10-07 16:08 · 13 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | build | exact | data | read_sheet also returns the analyst_notes tab | 1 | ✓ |
| 2 | build | exact | data | unpack notes rows | 1 | ✓ |
| 3 | build | exact | data | local mode: no notes | 1 | ✓ |
| 4 | build | exact | data | no input: no notes | 1 | ✓ |
| 5 | build | exact | feature | join the Analyst view | 1 | ✓ |
| 6 | build | exact | log | log the analyst join | 1 | ✓ |
| 7 | page | exact | feature | import the analyst section | 1 | ✓ |
| 8 | page | exact | feature | analyst CSS | 1 | ✓ |
| 9 | page | exact | feature | analyst card after the Stakeholder view | 1 | ✓ |
| 10 | page | exact | feature | analyst JS | 1 | ✓ |
| 11 | page | exact | feature | render the analyst view with the page | 1 | ✓ |
| 12 | vcheck | exact | check | Etimad page: require the analyst section | 1 | ✓ |
| 13 | vcheck | exact | check | analyst view render check | 1 | ✓ |

## Edit detail

### 1. build — read_sheet also returns the analyst_notes tab

**Old**
```
    return cards, rows('decisions'), rows('agency_bridge'), rows('counts'), rows('market')

```
**New**
```
    return cards, rows('decisions'), rows('agency_bridge'), rows('counts'), rows('market'), rows('analyst_notes')

```

### 2. build — unpack notes rows

**Old**
```
        cards, decisions, bridge_rows, counts, market = read_sheet(a.sheet)

```
**New**
```
        cards, decisions, bridge_rows, counts, market, note_rows = read_sheet(a.sheet)

```

### 3. build — local mode: no notes

**Old**
```
        cards, decisions, bridge_rows, counts, market = read_raw_dir(a.raw), [], [], [], []

```
**New**
```
        cards, decisions, bridge_rows, counts, market, note_rows = read_raw_dir(a.raw), [], [], [], [], []

```

### 4. build — no input: no notes

**Old**
```
        cards, decisions, bridge_rows, counts, market = [], [], [], [], []

```
**New**
```
        cards, decisions, bridge_rows, counts, market, note_rows = [], [], [], [], [], []

```

### 5. build — join the Analyst view

**Old**
```
    out['market'] = build_market(market)

```
**New**
```
    out['market'] = build_market(market)
    # Analyst view: umbrella (committed, no Etimad data) + market windows + tenders + map + notes (private sheet)
    from etimad_analyst import analyst
    out['analyst'] = analyst(market, out['tenders'], a.map, note_rows, bidraw=a.bidraw)

```

### 6. build — log the analyst join

**Old**
```
    print(f"Etimad: {out['count']} tenders ({rel} relevant), last capture {out['last_capture']} → {a.out}")

```
**New**
```
    print(f"Etimad: {out['count']} tenders ({rel} relevant), last capture {out['last_capture']} → {a.out}")
    an = out.get('analyst') or {}
    print(f"Analyst view: {len(an.get('windows') or [])} market windows, {len(an.get('notes') or [])} notes ({an.get('notes_month')}), reviewed {an.get('reviewed')}")

```

### 7. page — import the analyst section

**Old**
```
import json, os, sys, collections

```
**New**
```
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etimad_analyst as AV

```

### 8. page — analyst CSS

**Old**
```
<style>{CSS}</style></head>
```
**New**
```
<style>{CSS}{AV.CSS}</style></head>
```

### 9. page — analyst card after the Stakeholder view

**Old**
```
<div class="foot" data-en="Built from the private EH Etimad data sheet.
```
**New**
```
{AV.HTML}
<div class="foot" data-en="Built from the private EH Etimad data sheet.
```

### 10. page — analyst JS

**Old**
```
<script>{JS}</script>
```
**New**
```
<script>{JS}{AV.JS}</script>
```

### 11. page — render the analyst view with the page

**Old**
```
  renderMarket();
  document.querySelectorAll('#list th')
```
**New**
```
  renderMarket();
  if(typeof renderAnalyst==='function')renderAnalyst();
  document.querySelectorAll('#list th')
```

### 12. vcheck — Etimad page: require the analyst section

**Old**
```
    'etimad_tenders.html':             dict(kpi=6, tables=0, svgs=0, nodiff=True),   # content changes with each Sunday capture

```
**New**
```
    'etimad_tenders.html':             dict(kpi=6, tables=0, svgs=0, nodiff=True, analyst=True),   # content changes with each Sunday capture

```

### 13. vcheck — analyst view render check

**Old**
```
                    if m['words'] < 60: probs.append(f"page nearly empty ({m['words']} words)")

```
**New**
```
                    if m['words'] < 60: probs.append(f"page nearly empty ({m['words']} words)")
                    if want.get('analyst'):   # Analyst view: its picture and at least one note, or its stated empty state
                        av = pg.evaluate("(()=>({flow:!!document.querySelector('#av-flow svg'),notes:document.querySelectorAll('#av .avn').length,"
                                 
```
