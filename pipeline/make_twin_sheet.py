#!/usr/bin/env python3
"""
make_twin_sheet.py — writes the reviewer workbook from a sync report (bid_sync_report.json) and the map.

  python pipeline/make_twin_sheet.py --report pipeline/bid_sync_report.json --map site/EH_Stakeholder_Map_CURRENT.html \
                                     --out pipeline/possible_twins_review.xlsx

Two review sheets, each with a Decision column (dropdown):
  • "Possible twins" — pairs of map companies that are probably one organisation recorded twice.
        Decision: Merge → keep A | Merge → keep B | Merge (sync picks the side: roster-listed, then higher tier, then higher count) | Keep separate | Unsure
  • "Workbook-only bid flags" — companies flagged as bidders in the workbook but absent from the live tracker rosters.
        Decision: Keep flag | Clear flag | Unsure
How the decisions are used: commit the filled file as pipeline/twin_decisions.xlsx and the sync (run with --decisions) will
  – treat a merged pair's other name as an alias of the kept company (matches, no duplicate node, alias noted),
  – drop "Keep separate" pairs from future twin lists,
  – clear the bid flag (bid=false, count 0) of companies decided "Clear flag".
Rows already decided are carried forward unchanged; new candidates are appended below them.
"""
import argparse, json, re, os, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TWIN_OPTS = ['Merge → keep A', 'Merge → keep B', 'Merge', 'Keep separate', 'Unsure']   # plain 'Merge' = let the sync choose the side
FLAG_OPTS = ['Keep flag', 'Clear flag', 'Unsure']
HDR_FILL = PatternFill('solid', fgColor='1C2B33'); DEC_FILL = PatternFill('solid', fgColor='FFF4D6'); A_FILL = PatternFill('solid', fgColor='EEF6FB'); B_FILL = PatternFill('solid', fgColor='F2F9F0')

def grab(html, sid):
    m = re.search(r'<script id="%s" type="application/json">(.*?)</script>' % sid, html, re.S)
    return json.loads(m.group(1))

def style_header(ws, ncols):
    for c in ws[1]:
        c.font = Font(name='Arial', bold=True, color='FFFFFF', size=10); c.fill = HDR_FILL; c.alignment = Alignment(wrap_text=True, vertical='center')
    ws.row_dimensions[1].height = 32; ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:{get_column_letter(ncols)}{max(ws.max_row, 2)}'

def normalise_decision(d, sheet):
    """Map free-text reviewer wording onto the dropdown values ('merge' → 'Merge' (side chosen by the sync), 'keep' → 'Keep flag' …)."""
    x = d.strip().lower()
    if not x: return ''
    if sheet == 'Possible twins':
        if x.startswith('merge'): return 'Merge → keep A' if 'keep a' in x else 'Merge → keep B' if 'keep b' in x else 'Merge'
        if 'separate' in x or x in ('keep', 'different', 'no'): return 'Keep separate'
        return 'Unsure'
    if x.startswith('clear'): return 'Clear flag'
    if x.startswith('keep'): return 'Keep flag'
    return 'Unsure'

def prior_decisions(path, sheet, keycols):
    """Return {key: (decision, reviewer note)} from a previously filled workbook, if any."""
    out = {}
    if not path or not os.path.exists(path): return out
    try: ws = openpyxl.load_workbook(path, read_only=True)[sheet]
    except Exception: return out
    rows = list(ws.iter_rows(values_only=True)); hdr = [str(h or '') for h in rows[0]]
    try: ki = [hdr.index(k) for k in keycols]; di = hdr.index('Decision'); ni = hdr.index('Reviewer note')
    except ValueError: return out
    for r in rows[1:]:
        key = tuple((r[i] or '').strip() for i in ki)
        if any(key) and (r[di] or r[ni]): out[key] = (normalise_decision(str(r[di] or ''), sheet), (r[ni] or '').strip())
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--report', required=True); ap.add_argument('--map', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--previous', help='earlier filled review workbook (usually pipeline/twin_decisions.xlsx) — its decisions are carried forward')
    a = ap.parse_args()
    R = json.load(open(a.report, encoding='utf-8')); D = grab(open(a.map, encoding='utf-8').read(), 'DATA')
    by = {n['n']: n for n in D['nodes']}
    def f(n, k, d='—'): v = by.get(n, {}).get(k); return d if v in (None, '') else v

    wb = openpyxl.Workbook()
    # ---------------------------------------------------------------- sheet 1: possible twins
    ws = wb.active; ws.title = 'Possible twins'
    hdr = ['#', 'Company A', 'Category A', 'Tier A', 'Region A', 'City A', 'Bid count A', 'Company B', 'Category B', 'Tier B', 'Region B', 'City B', 'Bid count B',
           'Confidence', 'Why flagged', 'Decision', 'Reviewer note']
    ws.append(hdr)
    prev = prior_decisions(a.previous, 'Possible twins', ['Company A', 'Company B'])
    pairs = sorted(R.get('possible_twins', []), key=lambda p: -p['score'])
    for i, p in enumerate(pairs, 1):
        dec, note = prev.get((p['a'], p['b']), prev.get((p['b'], p['a']), ('', '')))
        conf = 'High' if p['score'] >= 0.9 else 'Medium' if p['score'] >= 0.8 else 'Low'
        ws.append([i, p['a'], f(p['a'], 'cat'), f(p['a'], 'tier'), f(p['a'], 'rg'), f(p['a'], 'city'), f(p['a'], 'bc', 0),
                   p['b'], f(p['b'], 'cat'), f(p['b'], 'tier'), f(p['b'], 'rg'), f(p['b'], 'city'), f(p['b'], 'bc', 0), conf, p['reason'], dec, note])
    dv = DataValidation(type='list', formula1='"' + ','.join(TWIN_OPTS) + '"', allow_blank=True, showDropDown=False); ws.add_data_validation(dv)
    dv.add(f'P2:P{max(ws.max_row, 2) + 200}')
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = Font(name='Arial', size=10); c.alignment = Alignment(vertical='top', wrap_text=True)
        for c in row[1:7]: c.fill = A_FILL
        for c in row[7:13]: c.fill = B_FILL
        row[15].fill = DEC_FILL; row[16].fill = DEC_FILL
    for i, w in enumerate([4, 40, 24, 7, 18, 12, 8, 40, 24, 7, 18, 12, 8, 10, 46, 18, 30], 1): ws.column_dimensions[get_column_letter(i)].width = w
    style_header(ws, len(hdr))

    # ---------------------------------------------------------------- sheet 2: workbook-only bid flags
    ws2 = wb.create_sheet('Workbook-only bid flags')
    hdr2 = ['#', 'Company', 'Category', 'Tier', 'Region', 'City', 'Workbook bid count', 'Bid frequency', 'Threat', 'Score', 'Has a possible twin?', 'Decision', 'Reviewer note']
    ws2.append(hdr2)
    prev2 = prior_decisions(a.previous, 'Workbook-only bid flags', ['Company'])
    twin_names = {p['a'] for p in pairs} | {p['b'] for p in pairs}
    names = sorted(R.get('workbook_only_names', []), key=lambda n: (-(by.get(n, {}).get('bc') or 0), n))
    for i, n in enumerate(names, 1):
        dec, note = prev2.get((n,), ('', ''))
        ws2.append([i, n, f(n, 'cat'), f(n, 'tier'), f(n, 'rg'), f(n, 'city'), f(n, 'bc', 0), f(n, 'bf', ''), f(n, 'threat', ''), f(n, 'sc'), 'yes — see Possible twins' if n in twin_names else '', dec, note])
    dv2 = DataValidation(type='list', formula1='"' + ','.join(FLAG_OPTS) + '"', allow_blank=True, showDropDown=False); ws2.add_data_validation(dv2)
    dv2.add(f'L2:L{max(ws2.max_row, 2) + 200}')
    for row in ws2.iter_rows(min_row=2):
        for c in row: c.font = Font(name='Arial', size=10); c.alignment = Alignment(vertical='top', wrap_text=True)
        row[11].fill = DEC_FILL; row[12].fill = DEC_FILL
    for i, w in enumerate([4, 48, 26, 7, 20, 14, 9, 9, 9, 7, 22, 14, 30], 1): ws2.column_dimensions[get_column_letter(i)].width = w
    style_header(ws2, len(hdr2))

    # ---------------------------------------------------------------- sheet 3: how to use
    ws3 = wb.create_sheet('How to use'); ws3.column_dimensions['A'].width = 130
    lines = ['Bid → Stakeholder Map sync — review workbook', '',
             f"Generated {R.get('synced', '')} from the live bid-tracker rosters ({R.get('roster_competitors')} competitors) against the Stakeholder Map ({len(D['nodes'])} companies).",
             '', 'Sheet "Possible twins": two map records that are probably the same organisation (English/Arabic spellings, spelling variants). Fill the yellow Decision cell for each row:',
             '   Merge → keep A / Merge → keep B — the other name becomes an alias of the kept company; the sync matches bids to it and never creates a duplicate.',
             '   Merge (no side) — same, and the sync keeps the record the bid rosters list, else the higher tier, else the higher bid count. Free-text wording (merge / separate / keep / clear) is accepted too.',
             '   Keep separate — they are different companies; the pair is not proposed again.',
             '   Unsure — left for later; proposed again next time.',
             'Sheet "Workbook-only bid flags": companies the workbook marks as bidders against EH but which do not appear in any 2025/2026 tracker roster. Decision: Keep flag / Clear flag / Unsure.',
             '   Clear flag sets bid = no and count = 0 on the map from the next publish.',
             '', 'Saving your decisions: save this file as pipeline/twin_decisions.xlsx in the repo (overwrite the previous one). The workflow passes it to the sync every run.',
             'Decisions you have already made are carried into each newly generated review file, so you only ever review new rows.',
             'The merge itself still belongs in the stakeholder workbook (Alias / merged duplicate) — the sync honours the decision until you do that.',
             '', 'Confidence: High = names essentially identical; Medium = strong name or Arabic/English match; Low = one distinctive word or skeleton in common, both flagged as bidders — check these.']
    for l in lines: ws3.append([l])
    ws3['A1'].font = Font(name='Arial', bold=True, size=12)
    for r in ws3.iter_rows(min_row=2):
        r[0].font = Font(name='Arial', size=10); r[0].alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(a.out)
    print(f'review workbook: {len(pairs)} possible twin pairs, {len(names)} workbook-only flags → {a.out}' + (f' ({len(prev) + len(prev2)} earlier decisions carried forward)' if prev or prev2 else ''))

if __name__ == '__main__':
    main()
