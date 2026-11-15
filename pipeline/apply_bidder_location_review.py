#!/usr/bin/env python3
"""
apply_bidder_location_review.py — applies Youssef's bidder-location review (returned 15 Nov 2026) for the Saudi Map (BETA).

Inputs (pipeline/sources/saudi_map_beta/, exactly as reviewed — nothing here is estimated):
  bidder_locations_review.csv   one row per bidder: no, name (the map record's name), tenders, status, address, lat, lng, source
  addr_found.tsv                coordinates for the addresses he typed: no|lat|lng|precision|listing|listing address|place_id|note
  review_decisions.json         dups (pairs that resolved to one business listing, with his Merge / Keep separate), merges (typed
                                commands), removes, region_edits
  bidders_index.json            no -> map record name
  tender_sites.tsv, buyers.tsv  where each tender was (place named in the title; buyer head offices)
  v2030_sites.tsv               Vision 2030 project sites, SIRC head office, EH sites

What it does
  1. Merges — the folded record becomes "Alias (merged duplicate): …" on the kept record (the map's existing style), the kept
     record takes the higher tier, bid encounters are added the way the hourly sync adds two spellings of one company, and
     aliases.csv gains an approved row so the bid→map sync folds the spelling on every publish. Alias rows that pointed at the
     folded record are re-pointed at the kept one.
  2. Removals — the record leaves the map; the name goes to removed_names.csv (the sync never adds it back).
  3. Region edit — Naqaa Environmental Consulting Office: city Jeddah, region Jeddah.
  4. Stores — pipeline/bidder_locations.csv (single store of bidder positions: name, lat, lng, address, source, precision,
     status, note), pipeline/tender_sites.json, pipeline/v2030_sites.json. embed_saudi_map_data.py puts them in the map.
     A bidder is pinned only at a business listing, at an address EH supplied, or at a head office from EH's own records.
     An address that is only a city name is NOT pinned (decision: never stack pins on a city centre).
Writes a log (bidder_location_review_log_<date>.json) holding every folded / removed record in full, for reversal.
Re-runnable: a merge or removal already applied is skipped; the three stores are rebuilt from the inputs each time.

Usage:  python3 pipeline/apply_bidder_location_review.py [--dry-run]
"""
import argparse, csv, json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from sync_bids_to_apps import norm, bf_of

MAP = os.path.join(ROOT, 'hub', 'EH_Stakeholder_Map_CURRENT.html')
SRC = os.path.join(HERE, 'sources', 'saudi_map_beta')
V2030 = os.path.join(ROOT, 'hub', 'vision2030_dashboard.html')
METHOD = 'reviewer merge (bidder location review)'
RANK = {'Tier 1': 1, 'GOV': 1, 'Tier 2': 2, 'Tier 3': 3, 'Tier 4': 4}
ALIAS_NOTE = re.compile(r'Alias \(merged duplicate\):\s*([^·\n]+)')
# typed merge commands whose target is named in words (his wording -> the record's exact name)
MERGE_TARGET = {267: 'Strategic Minds', 308: 'United Environmental Services – Waste Transport'}
KEEP_OVERRIDE = {(207, 208): 208}          # SAECO: one company; he asked to keep "Saudi Arabian Engineering Co. (SAECO)"
PINNED_PRECISION = ('company at address', 'building', 'street', 'district')
# EH sites: the two already on the map (own records) + the two confirmed in this review
EH_SITES = [
    {'key': 'Afaq Al-Biah Co. Ltd (Environmental Horizons)', 'en': 'Environmental Horizons — Jeddah head office', 'ar': 'آفاق البيئة — المقر الرئيسي بجدة',
     'lat': 21.6137111, 'lng': 39.1562528, 'addr_en': 'Madinah Road at the Hira Street intersection, Al Bawadi, Jeddah', 'addr_ar': 'طريق المدينة المنورة مع تقاطع شارع حراء، حي البوادي، جدة', 'precision': 'own records'},
    {'key': 'EH — Al-Juhfah Waste Management Complex (Rabigh)', 'en': 'EH — Al-Juhfah Waste Management Complex (Rabigh)', 'ar': 'آفاق البيئة — مجمع الجحفة لإدارة النفايات (رابغ)',
     'lat': 22.7050, 'lng': 39.1460, 'addr_en': 'Al-Juhfah, Rabigh — hazardous-waste treatment and disposal complex', 'addr_ar': 'الجحفة، رابغ — مجمع معالجة النفايات الخطرة والتخلص منها', 'precision': 'own records'},
]
EH_FROM_REVIEW = {   # v2030_sites.tsv name -> map key, names, the address Youssef confirmed
    'Environmental Horizons - Riyadh branch': {'key': 'EH — Riyadh Branch', 'en': 'Environmental Horizons — Riyadh branch', 'ar': 'آفاق البيئة — فرع الرياض',
        'addr_en': 'Al Imam Abdullah Bin Saud Bin Abdulaziz Branch Road, Al Shohda District, Riyadh', 'addr_ar': 'طريق الإمام عبدالله بن سعود بن عبدالعزيز الفرعي، حي الشهداء، الرياض', 'precision': 'street'},
    'Afaaq Environment Training Center (EH training centre)': {'key': 'Afaaq Environment Training Center', 'en': 'Afaaq Environment Training Centre', 'ar': 'مركز آفاق البيئة للتدريب',
        'addr_en': '3822 Madinah Road, As Salamah, Jeddah 23525', 'addr_ar': '3822 طريق المدينة، حي السلامة، جدة 23525', 'precision': 'company at address'},
}
V_DASH = {'The Red Sea': 'Red Sea Global (The Red Sea & AMAALA)', 'AMAALA': 'Red Sea Global (The Red Sea & AMAALA)', 'New Murabba (The Mukaab)': 'New Murabba',
          'ROSHN (Sedra community)': 'ROSHN', 'Ceer (KAEC plant)': 'Ceer'}
V_NAME_AR = {'The Red Sea': 'البحر الأحمر', 'AMAALA': 'أمالا'}     # the dashboard has one Arabic name for the two Red Sea Global sites


def tsv(path, n):
    out = []
    for l in open(path, encoding='utf-8'):
        f = l.rstrip('\n').split('|')
        if len(f) >= 3: out.append([x.strip() for x in f] + [''] * (n - len(f)))
    return out

def clean_addr(a):
    a = re.sub(r'\s*\[\d+(?:\s*,\s*\d+)*\]\s*$', '', str(a or ''))     # trailing "[1, 2]" reference marks pasted with the address
    return re.sub(r'\s+', ' ', a).strip()

def city_only(a):
    a = clean_addr(a)
    return bool(a) and len(a.split()) <= 2 and not re.search(r'\d', a)

def v2030_dashboard():
    """status / completion / Arabic texts as written on the Vision 2030 tab (hub/vision2030_dashboard.html)"""
    out = {'projects': {}, 'ar_status': {}, 'ar_names': {}, 'ar_txt': {}, 'ar_completion': {}}
    if not os.path.exists(V2030): return out
    s = open(V2030, encoding='utf-8').read()
    for nm, st, comp in re.findall(r'\{name:"([^"]+)",sectors:.*?status:"([^"]+)",completion:"([^"]+)"', s):
        out['projects'][nm] = {'status': st, 'completion': comp}
    m = re.search(r'const AR_STATUS\s*=\s*(\{.*?\});', s, re.S)
    if m: out['ar_status'] = json.loads(m.group(1))
    m = re.search(r'const AR_NAMES\s*=\s*(\{.*?\});', s, re.S)
    if m: out['ar_names'] = json.loads(m.group(1))
    m = re.search(r'const AR_COMPLETION\s*=\s*(\{.*?\});', s, re.S)
    if m: out['ar_completion'] = json.loads(m.group(1))
    i = s.find('const AR_TXT = {')
    if i >= 0:
        try: out['ar_txt'] = json.JSONDecoder().raw_decode(s[i + len('const AR_TXT = '):])[0]
        except Exception: pass
    return out


def build_stores(final_name, d_iso, log):
    """final_name: review no -> the surviving map record's name (after merges; None when removed)."""
    rows = list(csv.DictReader(open(os.path.join(SRC, 'bidder_locations_review.csv'), encoding='utf-8-sig', newline='')))
    addr = {int(f[0]): f for f in tsv(os.path.join(SRC, 'addr_found.tsv'), 8)}
    own, cand = {}, {}
    for r in rows:
        no = int(r['no']); st = r['status'].strip(); a = clean_addr(r['address']); rec = None
        if st == 'Located':
            is_own = r['source'].strip().lower().startswith('own')
            rec = {'lat': float(r['lat']), 'lng': float(r['lng']), 'address': a, 'source': 'own records' if is_own else 'business listing',
                   'precision': 'head office' if is_own else 'listing', 'status': 'Located', 'note': ''}
        elif st == 'Address from Youssef':
            f = addr.get(no)
            if f and f[3] in PINNED_PRECISION and f[1] and f[2]:
                rec = {'lat': float(f[1]), 'lng': float(f[2]), 'address': a, 'source': 'address supplied by EH', 'precision': f[3], 'status': 'Located',
                       'note': ('matched to: ' + f[4]) if f[4] else ''}
            elif city_only(a): rec = {'lat': '', 'lng': '', 'address': a, 'source': 'address supplied by EH', 'precision': 'none', 'status': 'Not located', 'note': 'city only'}
            elif f: rec = {'lat': '', 'lng': '', 'address': a, 'source': 'address supplied by EH', 'precision': 'none', 'status': 'Not located', 'note': 'no listing found'}
            else: log['problems'].append(f'no. {no} {r["name"]}: typed address not in the address lookup and not a city name — left unpinned'); \
                  rec = {'lat': '', 'lng': '', 'address': a, 'source': 'address supplied by EH', 'precision': 'none', 'status': 'Not located', 'note': 'no listing found'}
        elif st == 'Awaiting decision':
            rec = {'lat': '', 'lng': '', 'address': '', 'source': '', 'precision': 'none', 'status': 'Awaiting decision', 'note': 'awaiting decision'}
        else:
            rec = {'lat': '', 'lng': '', 'address': '', 'source': '', 'precision': 'none', 'status': 'Not located', 'note': 'no listing found'}
        tgt = final_name.get(no)
        if tgt is None: continue                                   # removed from the map
        rec['name'] = tgt
        (own if tgt == r['name'] else cand).setdefault(tgt, []).append((rec, r['name']))
    out = []
    for tgt in sorted(set(own) | set(cand), key=lambda x: x.casefold()):
        o = own.get(tgt, [None])[0]; rec = o[0] if o else None
        if rec is None or rec['status'] != 'Located':              # merged bidder: the kept record's location, else the folded record's
            alt = next(((c, nm) for c, nm in cand.get(tgt, []) if c['status'] == 'Located'), None)
            if alt:
                rec = dict(alt[0]); rec['note'] = (rec['note'] + '; ' if rec['note'] else '') + 'location from the merged record: ' + alt[1]
            elif rec is None: rec = dict(cand[tgt][0][0])
        out.append(rec)
    fields = ['name', 'lat', 'lng', 'address', 'source', 'precision', 'status', 'note']
    with open(os.path.join(HERE, 'bidder_locations.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows([{k: r[k] for k in fields} for r in out])
    # ---- tenders: delivery sites named in the title + buyer head offices (rule applied at embed time against the live tracker)
    sites = {}
    for f in tsv(os.path.join(SRC, 'tender_sites.tsv'), 9):
        if f[4] and f[5]: sites[f'{f[0]}-{f[1]}'] = {'place': f[2], 'type': f[3], 'lat': float(f[4]), 'lng': float(f[5]), 'listing': f[6], 'place_id': f[7], 'note': f[8]}
    buyers = []
    for f in tsv(os.path.join(SRC, 'buyers.tsv'), 8):
        buyers.append({'client': f[0], 'lat': float(f[1]) if f[1] else None, 'lng': float(f[2]) if f[2] else None, 'grade': f[3], 'listing': f[4], 'address': f[5], 'place_id': f[6], 'note': f[7]})
    json.dump({'looked_up': '2026-11-15', 'rule': "delivery site named in the title if it has coordinates (type region = regional capital); else the buyer's head office when its match is High or Medium; else not pinned and counted",
               'sites': sites, 'buyers': buyers}, open(os.path.join(HERE, 'tender_sites.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # ---- Vision 2030 project sites, SIRC head office, EH sites
    dash = v2030_dashboard(); V = []
    for f in tsv(os.path.join(SRC, 'v2030_sites.tsv'), 11):
        kind, en, ar, parent = f[0], f[1], f[2], f[3]
        lat, lng = (float(f[4]), float(f[5])) if f[4] and f[5] else (None, None)
        if kind == 'eh_site':
            e = dict(EH_FROM_REVIEW[en]); e.update({'kind': 'eh_site', 'lat': lat, 'lng': lng}); V.append(e); continue
        if kind == 'pif_company':
            V.append({'kind': 'pif_company', 'en': 'Saudi Investment Recycling Company (SIRC) — head office', 'ar': ar + ' — المقر الرئيسي', 'node': 'Saudi Investment Recycling Company (SIRC)',
                      'lat': lat, 'lng': lng, 'addr': re.sub(r',?\s*Saudi Arabia$', '', f[7])}); continue
        dn = V_DASH.get(en, en); dp = dash['projects'].get(dn) or {}; at = dash['ar_txt'].get(dn) or {}
        st_ar = ''
        if dp:
            comp_ar = dash['ar_completion'].get(dp['completion'], dp['completion'])
            st_ar = (dash['ar_status'].get(dp['status'], dp['status']) + '؛ الإنجاز ' + comp_ar + ((' — ' + at['desc']) if at.get('desc') else ''))
        V.append({'kind': 'project', 'en': en, 'ar': V_NAME_AR.get(en, ar), 'parent': parent, 'parent_ar': dash['ar_names'].get(parent, '') if parent else '',
                  'dash': dn if dp else '', 'status': dp.get('status', ''), 'completion': dp.get('completion', ''), 'lat': lat, 'lng': lng, 'status_en': f[9], 'status_ar': st_ar, 'site_note': f[10]})
    for e in EH_SITES: V.append(dict(e, kind='eh_site'))
    json.dump({'looked_up': '2026-11-15', 'sites': V}, open(os.path.join(HERE, 'v2030_sites.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out, sites, buyers, V


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true'); a = ap.parse_args()
    d_iso = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y-%m-%d'); d_mon = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%b %Y')
    dec = json.load(open(os.path.join(SRC, 'review_decisions.json'), encoding='utf-8'))
    index = {x['no']: x['name'] for x in json.load(open(os.path.join(SRC, 'bidders_index.json'), encoding='utf-8'))}
    html = open(MAP, encoding='utf-8').read()
    m = re.search(r'(<script id="DATA" type="application/json"[^>]*>)(.*?)(</script>)', html, re.S)
    D = json.loads(m.group(2)); nodes = D['nodes']; by = {n['n']: n for n in nodes}
    log = {'applied': d_iso, 'source': 'bidder location review workbook returned 15 Nov 2026', 'bidders_before': sum(1 for n in nodes if n.get('cat') == 'Active Competitors' and n.get('bid')),
           'merged': [], 'removed': [], 'regions': [], 'already_applied': [], 'problems': []}
    alias_new, removed_new, override_new, drop = [], [], [], set()

    # ---- fold -> keep, by review number
    fold_to = {}
    for k, kn, f, fn, d in dec['dups']:
        if str(d).strip().lower() != 'merge': continue
        keep = KEEP_OVERRIDE.get((k, f), k); fold = f if keep == k else k
        fold_to[fold] = ('no', keep)
    for no, name, bc, cmd, addr in dec['merges']:
        if no in MERGE_TARGET: fold_to[no] = ('name', MERGE_TARGET[no])
    removed_nos = {r[0] for r in dec['removes']}
    def target_name(no):
        seen = set()
        while no in fold_to and no not in seen:
            seen.add(no); kind, v = fold_to[no]
            if kind == 'name': return v
            no = v
        return index[no]
    final_name = {no: (None if no in removed_nos else target_name(no)) for no in index}

    # ---- 1. merges
    alias_rows = list(csv.DictReader(open(os.path.join(HERE, 'aliases.csv'), encoding='utf-8-sig', newline='')))
    for fold_no in sorted(fold_to):
        fold_name, keep_name = index[fold_no], target_name(fold_no)
        kept, n = by.get(keep_name), by.get(fold_name)
        if kept is None: log['problems'].append(f'{fold_name}: merge target "{keep_name}" is not on the map'); continue
        alias_new.append({'tracker_name': fold_name, 'map_name': keep_name, 'method': METHOD, 'status': 'approved', 'added': d_iso})
        for r in alias_rows:                                       # spellings that pointed at the folded record now point at the kept one
            if norm(r.get('map_name')) == norm(fold_name) and str(r.get('status', '')).strip().lower() in ('approved', 'reviewer', 'auto'):
                alias_new.append({'tracker_name': r['tracker_name'], 'map_name': keep_name, 'method': METHOD + ' — re-pointed', 'status': 'approved', 'added': d_iso})
        if n is None or n is kept:
            log['already_applied'].append(fold_name); continue
        note = kept.get('notes') or ''
        carried = [fold_name] + [x.strip() for al in ALIAS_NOTE.findall(n.get('notes') or '') for x in re.split(r'\s*[;,/]\s*|\s+\|\s+', al) if x.strip()]
        for al in carried:
            if f'Alias (merged duplicate): {al}' not in note: note = (note.rstrip() + ' ' if note.strip() else '') + f'Alias (merged duplicate): {al}'
            if al != fold_name: alias_new.append({'tracker_name': al, 'map_name': keep_name, 'method': METHOD + ' — re-pointed', 'status': 'approved', 'added': d_iso})
        before = {k: kept.get(k) for k in ('tier', 'bc', 'bf', 'h2h', 'cat', 'rg', 'city')}
        kept['notes'] = note
        if RANK.get(n.get('tier'), 9) < RANK.get(kept.get('tier'), 9): kept['tier_old'] = kept.get('tier'); kept['tier'] = n['tier']
        if kept.get('cat') in ('Indirect / Adjacent Competitors', 'Direct Competitors'): kept['cat_old'] = kept['cat']; kept['cat'] = 'Active Competitors'
        if kept.get('rg') in ('—', '', None) and n.get('rg') not in ('—', '', None): kept['rg'], kept['reg'], kept['city'] = n['rg'], n.get('reg'), n.get('city') or kept.get('city') or ''
        if not kept.get('mw') and n.get('mw'): kept['mw'] = n['mw']
        if not kept.get('act') and n.get('act'): kept['act'] = n['act']
        # bid figures: added the way the hourly sync adds two spellings of one company (it recomputes them from the live rosters on publish)
        if n.get('bid'):
            kept['bid'] = True; kept['bc'] = (kept.get('bc') or 0) + (n.get('bc') or 0); kept['bf'] = bf_of(kept['bc'])
            hk, hn = kept.get('h2h'), n.get('h2h')
            if hk and hn:
                for f in ('app', 'wins', 'dq'): hk[f] = (hk.get(f) or 0) + (hn.get(f) or 0)
                if hk.get('undercut') is None: hk['undercut'] = hn.get('undercut')
            elif hn: kept['h2h'] = dict(hn)
        drop.add(id(n))
        log['merged'].append({'duplicate': fold_name, 'kept': keep_name, 'kept_before': before, 'kept_after': {k: kept.get(k) for k in before}, 'record': n})

    # ---- 2. removals
    for no, name, bc in dec['removes']:
        n = by.get(index.get(no, name))
        removed_new.append({'name': name, 'reason': 'Remove (bidder location review)', 'decided': d_iso})
        if n is None: log['already_applied'].append(name); continue
        drop.add(id(n)); log['removed'].append({'name': name, 'record': n})

    # ---- 3. region edit: his "Makkah Region" + Jeddah is the map's own Jeddah slice
    for no, city, rg in dec['region_edits']:
        n = by.get(final_name.get(no) or '')
        if n is None: log['problems'].append(f'region edit: record no. {no} not on the map'); continue
        new_rg = {'jeddah': 'Jeddah', 'makkah': 'Makkah City', 'rabigh': 'Rabigh'}.get(city.lower(), 'Other Makkah Region') if rg.lower().startswith('makkah') else rg
        if (n.get('rg'), n.get('city')) != (new_rg, city):
            log['regions'].append({'name': n['n'], 'before': [n.get('rg'), n.get('city'), n.get('reg')], 'region': new_rg, 'city': city})
            n['rg'], n['city'], n['reg'] = new_rg, city, 'Makkah'; n['region_src'] = 'reviewed ' + d_iso
        override_new.append({'map_name': n['n'], 'region': new_rg, 'city': city, 'confidence': 'Reviewer', 'method': 'Reviewer', 'source': 'Bidder location review workbook returned 15 Nov 2026', 'decided': d_iso})

    D['nodes'] = [n for n in nodes if id(n) not in drop]
    after = sum(1 for n in D['nodes'] if n.get('cat') == 'Active Competitors' and n.get('bid')); log['bidders_after'] = after
    names_after = {n['n'] for n in D['nodes']}
    missing = sorted({v for v in final_name.values() if v and v not in names_after})
    if missing: log['problems'].append('reviewed bidders not found on the map after the merges: ' + '; '.join(missing))
    kept_norm = {norm(n['n']) for n in D['nodes']}
    clash = [x['name'] for x in removed_new if norm(x['name']) in kept_norm]
    if clash: log['problems'].append('removed names that normalise to a record still on the map (not blocked in the sync): ' + '; '.join(clash)); removed_new = [x for x in removed_new if x['name'] not in clash]

    print(f"records {len(nodes)} → {len(D['nodes'])} | bidders (Active Competitors with tracker bids) {log['bidders_before']} → {after} | merged {len(log['merged'])} | removed {len(log['removed'])} "
          f"| region edits {len(log['regions'])} | already applied {len(log['already_applied'])}")
    for p in log['problems']: print('  !!', p)
    if a.dry_run: print('DRY RUN — nothing written'); return

    if drop or log['regions']:
        open(MAP, 'w', encoding='utf-8').write(html[:m.start(2)] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + html[m.end(2):])
    def append_csv(path, fields, new, key):
        old = []
        if os.path.exists(path):
            with open(path, encoding='utf-8-sig', newline='') as f: old = list(csv.DictReader(f))
        seen = {tuple(norm(r.get(k, '')) for k in key) for r in old}; add = []
        for r in new:
            k = tuple(norm(r[x]) for x in key)
            if k in seen or (len(key) == 2 and k[0] == k[1]): continue
            seen.add(k); add.append(r)
        if add:
            with open(path, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows([{k: r.get(k, '') for k in fields} for r in old + add])
        return len(add)
    # an earlier "different companies" row for a pair he has now merged would make the sync add the folded spelling back as a
    # new company on every publish: the 15 Nov decision replaces it (kept in the log so it can be reversed)
    ap_ = os.path.join(HERE, 'aliases.csv'); fields_a = ['tracker_name', 'map_name', 'method', 'status', 'added']
    with open(ap_, encoding='utf-8-sig', newline='') as f: cur = list(csv.DictReader(f))
    merged_pairs = {frozenset((norm(x['tracker_name']), norm(x['map_name']))): x for x in alias_new if x['method'] == METHOD}
    superseded = []
    for r in cur:
        if str(r.get('status', '')).strip().lower() != 'rejected': continue
        x = merged_pairs.get(frozenset((norm(r['tracker_name']), norm(r['map_name']))))
        if x is None: continue
        superseded.append(dict(r))
        r.update({'tracker_name': x['tracker_name'], 'map_name': x['map_name'], 'method': METHOD + ' — replaces "different companies" of ' + (r.get('added') or 'an earlier review'), 'status': 'approved', 'added': d_iso})
    if superseded:
        with open(ap_, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields_a); w.writeheader(); w.writerows([{k: r.get(k, '') for k in fields_a} for r in cur])
        print(f'aliases.csv: {len(superseded)} earlier "different companies" row(s) replaced by the merge decision: ' + '; '.join(f"{r['tracker_name']} / {r['map_name']}" for r in superseded))
    log['superseded_rejections'] = superseded
    na = append_csv(ap_, fields_a, alias_new, ('tracker_name', 'map_name'))
    nr = append_csv(os.path.join(HERE, 'removed_names.csv'), ['name', 'reason', 'decided'], removed_new, ('name',))
    no_ = append_csv(os.path.join(HERE, 'region_overrides.csv'), ['map_name', 'region', 'city', 'confidence', 'method', 'source', 'decided'], override_new, ('map_name',))
    locs, sites, buyers, V = build_stores(final_name, d_iso, log)
    c = {}
    for r in locs: c[r['status'] + (' — ' + r['note'] if r['status'] != 'Located' else '')] = c.get(r['status'] + (' — ' + r['note'] if r['status'] != 'Located' else ''), 0) + 1
    log['stores'] = {'bidder_locations.csv': {'rows': len(locs), 'by_status': c}, 'tender_sites.json': {'sites': len(sites), 'buyers': len(buyers)}, 'v2030_sites.json': len(V)}
    lp = os.path.join(HERE, f'bidder_location_review_log_{d_iso}.json')
    if (drop or log['regions']) or not os.path.exists(lp): json.dump(log, open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    elif superseded:                                               # a re-run that only repaired aliases.csv: add that to the existing log
        old = json.load(open(lp, encoding='utf-8')); old['superseded_rejections'] = (old.get('superseded_rejections') or []) + superseded
        json.dump(old, open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'written: map ({"changed" if drop or log["regions"] else "unchanged"}), aliases.csv (+{na}), removed_names.csv (+{nr}), region_overrides.csv (+{no_}), bidder_locations.csv ({len(locs)} rows: {c}), '
          f'tender_sites.json, v2030_sites.json, {os.path.basename(lp)}')
    for p in log['problems']: print('  !!', p)

if __name__ == '__main__':
    main()
