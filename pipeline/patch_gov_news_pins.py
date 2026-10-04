"""patch_gov_news_pins.py — pinned stories and a per-body run summary (02/10/2026).

The 30 September MEWA story (https://spa.gov.sa/N2689556) still did not appear after the date fixes. The most likely
reason: it is no longer in the feed at all — it was dropped when an earlier run started from the empty seed, and SPA's
search ranks by relevance, so the weekly search does not necessarily bring it back.
  1. pipeline/gov_news_pins.json — stories to keep even if the search misses them. The collector opens each page (plain
     request), reads the headline and the date from the story's own description tag, and keeps it like any other story,
     exempt from the 90-day clean-out while pinned. Pre-filled with N2689556 for MEWA.
  2. The run log now ends with a summary per body (stories on file, stories this week) and a line for each pinned story,
     so "is it in the feed, and with what date?" can be read straight from the Actions log.
  3. Feed week fixed: the scheduled Sunday-morning run now reports the Sunday–Saturday week that has just ended. Before,
     it opened a new, empty week a few hours old — which is why the 30 September story could not be in "This feed week"
     after the Sunday 4 October run. (Applied directly to fetch_gov_news.py: wk_start is computed from yesterday.)
Run once, then run the Government news workflow.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
F = os.path.join(HERE, 'fetch_gov_news.py'); K = 'fetch_gov_news.py'
if 'gov_news_pins.json' in open(F, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(F, F + '.pre-pins.bak'); load(F, K); N = 0
def R(a, b, note):
    global N; N += 1; rep(K, a, b, 'pins', note)
R("    # ---- date check for every item on file (fixes items carried over from earlier runs)\n",
  """    # ---- pinned stories (pipeline/gov_news_pins.json): kept even when the weekly search misses them
    pinned_ids = set(); pin_log = []
    pin_path = os.path.join(HERE, 'gov_news_pins.json')
    if os.path.exists(pin_path):
        for p in json.load(open(pin_path, encoding='utf-8')).get('pins', []):
            url = (p.get('url') or '').strip(); bid = p.get('body')
            if not url or not bid: continue
            iid = item_id(url, '')
            if iid not in items:
                try:
                    html = http_get(url, timeout=25).text
                    m = re.search(r'<meta[^>]+(?:property|name)="og:title"[^>]+content="([^"]+)"', html) or re.search(r'<title>([^<]+)</title>', html)
                    title = trim_headline(htmlmod.unescape(m.group(1))) if m else url
                    d = None
                    if 'spa.gov.sa' in url:
                        try: d, _ = spa_story_date(url)
                        except Exception: d = None
                    items[iid] = dict(id=iid, body=bid, title=title, lang=lang_of(title), date=d, date_src='page' if d else 'unknown', url=url,
                                      source='spa' if 'spa.gov.sa' in url else 'official', tags=tag(title, cfg['tags']), first_seen=today.isoformat())
                except Exception as e:
                    pin_log.append(f'pinned {url}: could not be opened ({type(e).__name__})'); continue
            items[iid]['pinned'] = True; pinned_ids.add(iid)

    # ---- date check for every item on file (fixes items carried over from earlier runs)
""", 'Pinned stories')
R("        protected.update(x['id'] for x in lst[:KEEP_MIN])\n",
  "        protected.update(x['id'] for x in lst[:KEEP_MIN])\n    protected |= pinned_ids\n", 'Pinned stories are never cleaned out')
R("    print(f'\\nfeed: {len(kept)} items kept ({new_total} new this run) across {len(bodies_out)} bodies → {a.out}')",
  """    print(f'\\nfeed: {len(kept)} items kept ({new_total} new this run) across {len(bodies_out)} bodies → {a.out}')
    wk_to = (wk_start + dt.timedelta(days=6)).isoformat(); wk_from = wk_start.isoformat()
    in_wk = lambda i: (wk_from <= i['date'] <= wk_to) if i.get('date') else i['first_seen'] >= wk_from
    print(f'summary for the week {wk_from} to {wk_to}:')
    for b in bodies_out:
        mine = [i for i in kept if i['body'] == b['id']]
        print(f"  {b['id']:6s} on file {len(mine):3d} · this week {sum(1 for i in mine if in_wk(i)):2d}")
    for i in kept:
        if i.get('pinned'): print(f"  pinned  {i['url']} · {i['body']} · date {i.get('date') or 'unknown'} ({i.get('date_src')}) · this week: {'yes' if in_wk(i) else 'no'}")
    for l in pin_log: print('  ' + l)""", 'Per-body summary and pinned-story lines in the run log')
open(F, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_gov_news_pins'), 'Change table — pinned stories and run summary')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
