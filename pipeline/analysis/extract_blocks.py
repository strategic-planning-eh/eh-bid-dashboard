"""Step 0 — lift the data blocks the analysis reads from the published hub pages.

Writes out/map_data_raw.json, out/map_lic_raw.json, out/map_banalytics_raw.json (from hub/EH_Stakeholder_Map_CURRENT.html)
and out/bid_data_raw.json (from hub/EH_Bid_Analysis_CURRENT.html). Run before profile_map.py / build_v9_workbook.py / analyse.py.
The raw blocks are not committed: they duplicate hub/ and are regenerated here.
"""
import re, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
def block(html, sid):
    m = re.search(r'<script id="%s" type="application/json"[^>]*>(.*?)</script>' % sid, html, re.S)
    return json.loads(m.group(1))
m = open(os.path.join(ROOT, 'hub', 'EH_Stakeholder_Map_CURRENT.html'), encoding='utf-8').read()
for sid, name in (('DATA', 'map_data_raw'), ('LIC', 'map_lic_raw'), ('BANALYTICS', 'map_banalytics_raw')):
    json.dump(block(m, sid), open(os.path.join(OUT, name + '.json'), 'w'), ensure_ascii=False)
b = open(os.path.join(ROOT, 'hub', 'EH_Bid_Analysis_CURRENT.html'), encoding='utf-8').read()
json.dump(block(b, 'BA'), open(os.path.join(OUT, 'bid_data_raw.json'), 'w'), ensure_ascii=False)
print('blocks written to', OUT)
