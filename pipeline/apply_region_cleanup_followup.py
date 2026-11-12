#!/usr/bin/env python3
"""apply_region_cleanup_followup.py — Youssef's three answers after the 12 Nov region clean-up.
  1. Clients app untouched (nothing to do).
  2. The two EDCO records are one company: the Arabic MWAN-register record is merged into the English one, which keeps the
     higher tier, the licence block, the stronger confidence and score, and the combined bid encounters (the sync recomputes them).
  3. Fifteen records carried region names the map's wheel does not draw ("Makkah Region", "Asir Region", "Jazan Region",
     "Najran Region"): filed under the map's own slices by city (KAEC → Rabigh, the governorate it lies in).
Usage: python3 pipeline/apply_region_cleanup_followup.py [--dry-run]"""
import csv, json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); MAP = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html')
dry = '--dry-run' in sys.argv; d_iso = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y-%m-%d')
KEPT = 'Environment & Development Environmental Consulting Co. (One-Person Co.) (EDCO)'; DUP = 'شركة البيئة والتنمية للاستشارات البيئية'
html = open(MAP, encoding='utf-8').read()
m = re.search(r'(<script id="DATA" type="application/json"[^>]*>)(.*?)(</script>)', html, re.S)
D = json.loads(m.group(2)); nodes = D['nodes']; by = {n['n']: n for n in nodes}
log = {'applied': d_iso, 'merged': [], 'regions': []}
k, d = by.get(KEPT), by.get(DUP)
if k and d:
    log['merged'].append({'duplicate': DUP, 'kept': KEPT, 'record': dict(d), 'kept_before': dict(k)})
    k['tier_old'] = k.get('tier'); k['tier'] = d['tier']; k['mw'] = d.get('mw'); k['cf'] = d.get('cf') or k.get('cf')
    if (d.get('sc') or 0) > (k.get('sc') or 0): k['sc_old'], k['cap_old'] = k.get('sc'), k.get('cap'); k['sc'], k['cap'] = d['sc'], d['cap']
    k['bc'] = (k.get('bc') or 0) + (d.get('bc') or 0); k['bf'] = 'High' if k['bc'] >= 5 else 'Medium' if k['bc'] >= 3 else 'Low'
    extra = 'MWAN licence register entry (Jul 2026 snapshot).'
    k['notes'] = ' '.join(x for x in [extra, (k.get('notes') or '').strip(), f'Alias (merged duplicate): {DUP}'] if x)
    D['nodes'] = nodes = [n for n in nodes if n is not d]
elif not k: sys.exit('EDCO record not found')
FIX = {'Makkah Region': {'Jeddah': 'Jeddah', 'Rabigh': 'Rabigh', 'Makkah': 'Makkah City', 'KAEC': 'Rabigh'}}
ADMIN = {'Asir Region': 'Asir', 'Jazan Region': 'Jazan', 'Najran Region': 'Najran'}
for n in nodes:
    rg = n.get('rg')
    if rg == 'Makkah Region': new, reg = FIX[rg].get(n.get('city'), 'Other Makkah Region'), 'Makkah'
    elif rg in ADMIN: new, reg = 'Southern Region', ADMIN[rg]
    else: continue
    log['regions'].append({'name': n['n'], 'before': rg, 'city': n.get('city'), 'region': new}); n['rg'] = new; n['reg'] = n.get('reg') or reg
print(f"merged {len(log['merged'])} | regions normalised {len(log['regions'])} | records {len(nodes)}")
for r in log['regions']: print('  ', r['name'][:55], '|', r['before'], '/', r['city'], '→', r['region'])
if dry: sys.exit('DRY RUN')
open(MAP, 'w', encoding='utf-8').write(html[:m.start(2)] + json.dumps(D, ensure_ascii=False) + html[m.end(2):])
if log['merged']:
    with open(os.path.join(HERE, 'aliases.csv'), 'a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow([DUP, KEPT, 'reviewer merge (region cleanup)', 'approved', d_iso])
json.dump(log, open(os.path.join(HERE, f'region_cleanup_followup_log_{d_iso}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
