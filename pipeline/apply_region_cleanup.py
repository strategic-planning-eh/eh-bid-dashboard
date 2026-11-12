#!/usr/bin/env python3
"""
apply_region_cleanup.py — applies Youssef's returned "Region not recorded" workbook (12 Nov 2026) to the Stakeholder Map.

The workbook (EH_Map_Region_Not_Recorded_2026-11-10.xlsx) lists every map company without a region: the 408 stored in
hub/EH_Stakeholder_Map_CURRENT.html and the 35 that exist only on the published map because the hourly sync adds unmatched
roster bidders there. His rule for the Notes column: an action word is a command (remove / merge / apply), anything else is
a note about the company.

What it does
  1. Regions — Region / City as he filled them, normalised to the map's own region list (e.g. "Makkah Region" + Jeddah →
     Jeddah, "Eastern Region" → Eastern Province). A row with a city and no region takes the city's region.
  2. Stored records for the 35 roster-only bidders that he kept — written into the map file so they are no longer
     re-created without a region on every publish (the sync then matches them by exact name and refreshes bid figures).
  3. Merges — the duplicate becomes "Alias (merged duplicate): …" on the kept record plus an approved row in aliases.csv.
  4. Removals — the record leaves the map; the name goes to pipeline/removed_names.csv, which sync_bids_to_apps.py reads so a
     removed roster name is never added back. Full removed records are kept in the log for reversal.
     A name he extended with a short form in brackets ("… (CCL)") is applied as a rename.
  5. Notes — appended to the record's notes as "Reviewer note (12 Nov 2026): …".
Writes: the map, aliases.csv, region_overrides.csv, removed_names.csv, region_cleanup_log_<date>.json.

Usage:  python3 pipeline/apply_region_cleanup.py --review <returned.xlsx> [--dry-run]
"""
import argparse, csv, json, os, re, sys, warnings, datetime as dt
import openpyxl
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from sync_bids_to_apps import norm, guess_type, bf_of
warnings.simplefilter('ignore')

MAP = os.path.join(ROOT, 'hub', 'EH_Stakeholder_Map_CURRENT.html')
REGIONS = ['Jeddah', 'Makkah City', 'Rabigh', 'Other Makkah Region', 'Madinah Region', 'Riyadh', 'Qassim Region', 'Eastern Province',
           'Tabuk Region', 'Hail Region', 'Al Jawf Region', 'Northern Borders Region', 'Southern Region', 'GCC / International']
CITY_FIX = {'buraydiah': 'Buraydah', 'buraydah city': 'Buraydah', 'ahsa': 'Al-Ahsa'}
CITY_REGION = {'najran': ('Southern Region', 'Najran'), 'hail': ('Hail Region', 'Hail'), 'buraydah': ('Qassim Region', 'Qassim')}
# merge targets resolved against the map (his wording → the record's exact name)
MERGE_TARGET = {
    'شركة المستشار البيئي': 'Environmental Consultant Office',
    'شركة البيئة والتنمية للاسشارات': 'Environment & Development Environmental Consulting Co. (One-Person Co.) (EDCO)',
    'Engineering Principles': 'Fouad Fahad Al-Saleh & Khalid Al-Duwailah Environmental & Engineering Consulting (FKEC) (Engineering Principles)',
    'لاسكو العربية': 'LASCO Saudi Engineering Consulting Co. (One Person Co.)',
    'يورو قروب': 'Euro Group Engineering Consultancy',
    'شركة القيم الاربعة التجارية شخص واحد': 'Nineti Co.',
}
# "Apply" = take the suggestion printed in the Check column
APPLY = {'جامعة الملك خالد': ('Southern Region', 'Abha', 'Asir')}
CITY_DEFAULT = {'جامعة الملك فهد للبترول والمعادن - معهد البحوث': 'Dhahran'}

def region_of(rg, city):
    """his Region + City → (map region, admin region, city) or None when nothing usable was given"""
    rg = str(rg or '').strip(); city = str(city or '').strip()
    city = CITY_FIX.get(city.lower(), city); r, c = rg.lower(), city.lower()
    if not rg:
        if c in CITY_REGION: return CITY_REGION[c][0], CITY_REGION[c][1], city
        return None
    if r in ('makkah region', 'makkah'):
        m = {'jeddah': 'Jeddah', 'makkah': 'Makkah City', 'rabigh': 'Rabigh'}.get(c, 'Other Makkah Region')
        return m, 'Makkah', city
    if r in ('eastern region', 'eastern province'): return 'Eastern Province', 'Eastern Province', city
    if r == 'riyadh': return 'Riyadh', 'Riyadh', city
    if r in ('madinah region', 'madinah'): return 'Madinah Region', 'Madinah', city
    if r in ('qassim region', 'qassim'): return 'Qassim Region', 'Qassim', city
    if r in ('tabuk region', 'tabuk'): return 'Tabuk Region', 'Tabuk', city
    if r in ('hail region', 'hail'): return 'Hail Region', 'Hail', city
    if r == 'northern borders region': return 'Northern Borders Region', 'Northern Borders', city
    if r == 'al jawf region': return 'Al Jawf Region', 'Al Jawf', city
    if r in ('asir region', 'jazan region', 'najran region', 'southern region'):
        return 'Southern Region', {'asir region': 'Asir', 'jazan region': 'Jazan', 'najran region': 'Najran'}.get(r, ''), city
    if r == 'gcc / international':
        return 'GCC / International', {'dubai': 'UAE', 'cairo': 'Egypt', 'kuwait': 'Kuwait'}.get(c, ''), city
    raise SystemExit(f'region not understood: {rg!r} / {city!r}')

def action_of(note):
    s = str(note or '').strip(); l = s.lower()
    if not s: return 'none'
    if l.startswith('remove'): return 'remove'
    if 'merge' in l: return 'merge'
    if l == 'apply': return 'apply'
    return 'note'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--review', required=True); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))); d_iso, d_txt, d_mon = today.strftime('%Y-%m-%d'), today.strftime('%-d %b %Y'), today.strftime('%b %Y')
    wb = openpyxl.load_workbook(a.review, data_only=True)
    rows = {}
    for sh in ('All not recorded (443)', 'Missed (35)'):          # the Missed sheet is where he filled the 35, so it wins
        for r in wb[sh].iter_rows(min_row=2, values_only=True):
            r = list(r) + [None] * 13
            if not r[1]: continue
            name = str(r[1]).strip()
            if name in rows and not (r[10] or r[11] or r[12]): continue
            rows[name] = {'name': name, 'cat': r[2], 'typ': r[4], 'bc': r[6] or 0, 'stored': r[7] == 'Yes', 'rg': r[10], 'city': r[11], 'note': r[12]}

    html = open(MAP, encoding='utf-8').read()
    m = re.search(r'(<script id="DATA" type="application/json"[^>]*>)(.*?)(</script>)', html, re.S)
    D = json.loads(m.group(2)); nodes = D['nodes']; by = {n['n'].strip(): n for n in nodes}
    log = {'applied': d_iso, 'source': os.path.basename(a.review), 'regions': [], 'added': [], 'merged': [], 'removed': [], 'notes': [], 'renamed': [], 'problems': []}
    alias_new, override_new, removed_new, drop = [], [], [], set()

    def add_note(n, text):
        tag = f'Reviewer note ({d_txt}): {text.strip()}'
        if tag not in (n.get('notes') or ''): n['notes'] = ((n.get('notes') or '').rstrip() + ' ' + tag).strip()

    for name, r in rows.items():
        act = action_of(r['note']); n = by.get(name)
        if n is None and r['stored']:                                # he added a short name in brackets to the record's name → a rename
            base = re.sub(r'\s*\([^()]*\)\s*$', '', name).strip()
            if base != name and base in by:
                n = by[base]; n['n'] = name; by[name] = n; log['renamed'].append({'before': base, 'after': name})
                alias_new.append({'tracker_name': base, 'map_name': name, 'method': 'reviewer rename (region cleanup)', 'status': 'approved', 'added': d_iso})
        if r['stored'] and n is None: log['problems'].append(f'{name}: listed as stored but not in the map file'); continue
        if act == 'remove':
            keep_clients = 'keep in database' in str(r['note']).lower()
            if n is not None: drop.add(id(n))
            removed_new.append({'name': name, 'reason': str(r['note']).strip(), 'decided': d_iso})
            log['removed'].append({'name': name, 'instruction': str(r['note']).strip(), 'kept_in_client_app': keep_clients, 'record': n})
            continue
        if act == 'merge':
            kept = by.get(MERGE_TARGET.get(name, ''))
            if kept is None: log['problems'].append(f'{name}: merge target not resolved ({r["note"]})'); continue
            al = f'Alias (merged duplicate): {name}'
            if al not in (kept.get('notes') or ''): kept['notes'] = ((kept.get('notes') or '').rstrip() + ' ' + al).strip()
            if kept.get('rg') in ('—', '', None):
                reg = region_of(r['rg'], r['city'])
                if reg: kept['rg'], kept['reg'], kept['city'] = reg[0], reg[1], reg[2] or kept.get('city') or ''
            if kept['cat'] in ('Indirect / Adjacent Competitors', 'Direct Competitors'):      # 5 Nov 2026 rule: a tracker bidder is an Active Competitor
                kept['cat_old'] = kept['cat']; kept['cat'] = 'Active Competitors'
            if n is not None:
                rank = {'Tier 1': 1, 'GOV': 1, 'Tier 2': 2, 'Tier 3': 3, 'Tier 4': 4}
                if rank.get(n.get('tier'), 9) < rank.get(kept.get('tier'), 9): kept['tier_old'] = kept.get('tier'); kept['tier'] = n['tier']
                drop.add(id(n))
            alias_new.append({'tracker_name': name, 'map_name': kept['n'], 'method': 'reviewer merge (region cleanup)', 'status': 'approved', 'added': d_iso})
            log['merged'].append({'duplicate': name, 'kept': kept['n'], 'instruction': str(r['note']).strip(), 'record': n})
            continue
        # ---- region
        reg = None
        if act == 'apply' and name in APPLY: reg = (APPLY[name][0], APPLY[name][2], APPLY[name][1])
        else: reg = region_of(r['rg'], r['city'])
        if reg and not reg[2] and name in CITY_DEFAULT: reg = (reg[0], reg[1], CITY_DEFAULT[name])
        if n is None:                                                # roster-only bidder he kept → becomes a stored record
            if reg is None: log['problems'].append(f'{name}: roster-only bidder with no region and no instruction — left to the sync'); continue
            bc = int(r['bc'] or 0)
            n = {'n': name, 'cat': 'Active Competitors', 'rg': reg[0], 'city': reg[2], 'reg': reg[1], 'typ': r['typ'] or guess_type(name), 'sec': None,
                 'tier': 'Tier 4', 'bid': True, 'sites': None, 'mn': False, 'mp': False, 'act': '', 'bc': bc, 'bf': bf_of(bc), 'threat': 'Medium' if bc >= 3 else 'Low',
                 'collab': False, 'sc': None, 'cap': None, 'bk': 0, 'cf': 'Low', 'cf_basis': 'EH bid tracker roster; region set by reviewer ' + d_txt, 'drv': 'bids',
                 'notes': f'Added from the EH bid tracker rosters ({d_mon}); region set by reviewer {d_txt}. Tender-roster intelligence ({d_mon}): {bc} encounter(s) in EH bid rosters.',
                 'bid_synced': d_mon, 'bid_src': 'tracker', 'region_src': 'reviewed ' + d_iso}
            nodes.append(n); by[name] = n; log['added'].append({'name': name, 'region': reg[0], 'city': reg[2]})
        elif reg:
            log['regions'].append({'name': name, 'before': n.get('rg'), 'region': reg[0], 'city': reg[2], 'typed': [r['rg'], r['city']]})
            n['rg'], n['reg'] = reg[0], reg[1]
            if reg[2]: n['city'] = reg[2]
            n['region_src'] = 'reviewed ' + d_iso
        else:
            log['problems'].append(f'{name}: no region given and no instruction — still not recorded')
        if reg: override_new.append({'map_name': name, 'region': reg[0], 'city': reg[2], 'confidence': 'Reviewer', 'method': 'Reviewer', 'source': 'Region-not-recorded workbook returned ' + d_txt, 'decided': d_iso})
        if act == 'note': add_note(n, str(r['note'])); log['notes'].append({'name': name, 'note': str(r['note']).strip()})

    D['nodes'] = [n for n in nodes if id(n) not in drop]
    left = [n['n'] for n in D['nodes'] if n.get('rg') in ('—', '', None)]
    kept_norm = {norm(n['n']) for n in D['nodes']}
    clash = [x['name'] for x in removed_new if norm(x['name']) in kept_norm]
    if clash: log['problems'].append('removed names that normalise to a record still on the map (not blocked in the sync): ' + '; '.join(clash))
    removed_new = [x for x in removed_new if x['name'] not in clash]
    print(f"records {len(nodes)} → {len(D['nodes'])} | regions set {len(log['regions'])} | stored records added {len(log['added'])} | merged {len(log['merged'])} "
          f"| removed {len(log['removed'])} | notes {len(log['notes'])} | still without region {len(left)}")
    for p in log['problems']: print('  !!', p)
    for x in left: print('  still —:', x)
    if a.dry_run: print('DRY RUN — nothing written'); return

    open(MAP, 'w', encoding='utf-8').write(html[:m.start(2)] + json.dumps(D, ensure_ascii=False) + html[m.end(2):])
    def append_csv(path, fields, new, key):
        old = []
        if os.path.exists(path):
            with open(path, encoding='utf-8-sig', newline='') as f: old = list(csv.DictReader(f))
        seen = {tuple(norm(r.get(k, '')) for k in key) for r in old}
        add = [r for r in new if tuple(norm(r[k]) for k in key) not in seen]
        with open(path, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(old + add)
        return len(add)
    na = append_csv(os.path.join(HERE, 'aliases.csv'), ['tracker_name', 'map_name', 'method', 'status', 'added'], alias_new, ('tracker_name', 'map_name'))
    no = append_csv(os.path.join(HERE, 'region_overrides.csv'), ['map_name', 'region', 'city', 'confidence', 'method', 'source', 'decided'], override_new, ('map_name',))
    nr = append_csv(os.path.join(HERE, 'removed_names.csv'), ['name', 'reason', 'decided'], removed_new, ('name',))
    json.dump(log, open(os.path.join(HERE, f'region_cleanup_log_{d_iso}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'written: map, aliases.csv (+{na}), region_overrides.csv (+{no}), removed_names.csv (+{nr}), region_cleanup_log_{d_iso}.json')

if __name__ == '__main__':
    main()
