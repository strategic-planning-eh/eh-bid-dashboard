"""patch_gov_week_filter.py — "This feed week" shows only stories published that week (02/10/2026).

After the date fix, one story still looked wrong under "This feed week": its date was now correct (an older story), but
the week filter and the "Announcements this feed week" tile also admitted any story *collected* this week, whatever its
real date. SPA search returns older stories, so a 2023 story collected on Sunday showed up as this week's news.
Rule now: a story belongs to the week if its own date falls in the week; the day it was collected is used only for a
story with no known date. The same rule drives the tile. Edits hub/government_news.html. Run once.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P = os.path.join(ROOT, 'hub', 'government_news.html'); K = 'government_news.html'
if 'function inWeek(' in open(P, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(P, P + '.pre-week.bak'); load(P, K)
rep(K, "function inPeriod(it){const d=it.date||it.first_seen;if(S.period==='all')return true;const n=daysAgo(d);if(n==null)return S.period!=='week';return S.period==='week'?(d>=FEED.week_from&&d<=FEED.week_to)||it.first_seen>=FEED.week_from:n<=30;}",
    "function inWeek(it){return it.date?(it.date>=FEED.week_from&&it.date<=FEED.week_to):(it.first_seen>=FEED.week_from);} // own date decides; collection day only when the date is unknown\n"
    "function inPeriod(it){if(S.period==='all')return true;if(S.period==='week')return inWeek(it);const n=daysAgo(it.date||it.first_seen);return n!=null&&n<=30;}",
    'week-filter', 'Week view: published this week, not merely collected this week')
rep(K, "wk=items.filter(it=>(it.date&&it.date>=FEED.week_from&&it.date<=FEED.week_to)||it.first_seen>=FEED.week_from);",
    "wk=items.filter(inWeek);", 'week-filter', 'Tile uses the same rule')
open(P, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_gov_week_filter'), 'Change table — Regulatory news week filter')
print('failures:', len(FAILURES)); sys.exit(1 if FAILURES else 0)
