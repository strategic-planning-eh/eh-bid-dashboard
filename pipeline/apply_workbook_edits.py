"""apply_workbook_edits.py — apply Youssef's manual edits from a returned v9-live/v10 workbook to the live map data block.

Usage:  python3 pipeline/apply_workbook_edits.py <workbook_as_generated.xlsx> <workbook_returned.xlsx> [--dry-run]

Diffs the Stakeholders sheet row by row (keyed on Name; a renamed row is detected when exactly one name
disappears and one appears) and writes the changed editable fields into hub/EH_Stakeholder_Map_CURRENT.html:
    Name → n · Category → cat · Tier → tier · Company Type → typ · Region → rg · City → city · Sector → sec · Notes → notes
Computed fields (scores, bids, h2h, licences) are never taken from the workbook. Every applied change is logged to
pipeline/workbook_edits_log.json so the merge is reversible (5 Nov 2026).
"""
import sys, os, re, json, datetime as dt
from openpyxl import load_workbook
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
MAP = os.path.join(ROOT, 'hub', 'EH_Stakeholder_Map_CURRENT.html')
FIELDS = {'Name': 'n', 'Category': 'cat', 'Tier': 'tier', 'Company Type': 'typ', 'Region': 'rg', 'City': 'city', 'Sector': 'sec', 'Notes': 'notes'}

def sheet(p):
    ws = load_workbook(p, read_only=True)['Stakeholders']; rows = list(ws.iter_rows(values_only=True))
    h = list(rows[0]); i = h.index('Name')
    return h, {r[i]: r for r in rows[1:] if r[i]}

a_path, b_path = sys.argv[1], sys.argv[2]; dry = '--dry-run' in sys.argv
h, A = sheet(a_path); _, B = sheet(b_path)
added = [n for n in B if n not in A]; removed = [n for n in A if n not in B]
renames = {}
if len(added) == 1 and len(removed) == 1: renames[removed[0]] = added[0]
elif added or removed: sys.exit('Rows added/removed — handle by hand: added=%s removed=%s' % (added, removed))

edits = []   # (old_name, field_key, old, new)
for old_name, row_a in A.items():
    row_b = B.get(renames.get(old_name, old_name))
    for col, key in FIELDS.items():
        i = h.index(col); x, y = row_a[i], row_b[i]
        if (x or '') == (y or ''): continue
        if col == 'Name' and old_name not in renames: continue
        edits.append((old_name, key, x, y))

html = open(MAP, encoding='utf-8').read()
m = re.search(r'(<script id="DATA" type="application/json"[^>]*>)(.*?)(</script>)', html, re.S)
data = json.loads(m.group(2)); by = {n['n']: n for n in data['nodes']}
log = []
for old_name, key, x, y in edits:
    n = by.get(old_name)
    if n is None: print('!! not in map:', old_name); continue
    cur = n.get(key)
    if key == 'rg' and y in (None, ''): y = '—'
    newv = y if y is not None else ''
    log.append({'name': old_name, 'field': key, 'map_before': cur, 'workbook_before': x, 'after': newv})
    print('%-55s %-6s %r -> %r' % (old_name[:55], key, cur, newv))
    if not dry: n[key] = newv
if not dry and log:
    html = html[:m.start(2)] + json.dumps(data, ensure_ascii=False) + html[m.end(2):]
    open(MAP, 'w', encoding='utf-8').write(html)
    lp = os.path.join(HERE, 'workbook_edits_log.json')
    prev = json.load(open(lp, encoding='utf-8')) if os.path.exists(lp) else []
    prev.append({'applied': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'source': os.path.basename(b_path), 'edits': log})
    json.dump(prev, open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(('DRY RUN — ' if dry else 'applied ') + '%d edits' % len(log))
