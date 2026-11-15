#!/usr/bin/env python3
"""15 Nov 2026 — EH Jeddah head office moved to its real position (Youssef: Hira Street at the Madinah Road intersection).
Old pin 21.5772, 39.1516 was about 4 km south. New position from EH's own business listing (Al Bawadi, Madinah Road x Hira Street, Jeddah 23531)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table

M = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
if '21.6137111' in FILES['map']: sys.exit('Already applied.')
LAT, LNG = '21.6137111', '39.1562528'
EN, AR = 'Madinah Road at the Hira Street intersection, Al Bawadi, Jeddah', 'طريق المدينة المنورة مع تقاطع شارع حراء، حي البوادي، جدة'
ok = [
 rep('map', "'Afaq Al-Biah Co. Ltd (Environmental Horizons)': [21.5772,39.1516,'Hira Street, Jeddah — Head Office','EH (Reference)']",
     "'Afaq Al-Biah Co. Ltd (Environmental Horizons)': [%s,%s,'%s — Head Office','EH (Reference)']" % (LAT, LNG, EN), 'eh-hq', 'GEO_SITES: Jeddah head office position'),
 rep('map', '"lat":21.5772,"lng":39.1516,"a_en":"Hira Street, Jeddah","a_ar":"شارع حراء، جدة"',
     '"lat":%s,"lng":%s,"a_en":"%s","a_ar":"%s"' % (LAT, LNG, EN, AR), 'eh-hq', 'Saudi Map (BETA) data: Jeddah head office position'),
]
if not all(ok): sys.exit('Patch failed — nothing written.')
with open(M, 'w', encoding='utf-8') as f: f.write(FILES['map'])
write_change_table(os.path.join(HERE, 'change_table_eh_jeddah_hq'), 'EH Jeddah head office position')
print('done')
