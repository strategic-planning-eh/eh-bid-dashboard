"""patch_gov_news_dates2.py — second date fix for the Regulatory news tab (02/10/2026).

What happened: after the week filter was corrected, this week's story vanished from "This feed week" — because its stored
date was still wrong (an old date), so it no longer counted as this week. The likely source: when a story had no usable
date, the collector opened the article page and took the first "الموافق …" date anywhere on it — which on SPA pages can
belong to a related story in the sidebar.
Fix (fetch_gov_news.py):
  1. On the article page, the date is read only from the dateline that follows the story's own headline (within the first
     600 characters after it), or from the page's publication-date tag. Dates elsewhere on the page are ignored.
  2. Cross-check for SPA stories: SPA story numbers (the N… in the address) only go up over time. Stories whose dates come
     from their own dateline act as reference points; any other date that contradicts them by more than 30 days (a higher
     number with a much earlier date, or a lower number with a much later date) is rejected.
  3. A rejected or missing date is shown as "date n/a" with the day the story was collected — so the story stays in
     "This feed week" rather than disappearing — and the run log lists every rejected date.
Run once, then run the Government news workflow.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
F = os.path.join(HERE, 'fetch_gov_news.py'); K = 'fetch_gov_news.py'
if 'def spa_consistency(' in open(F, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(F, F + '.pre-dates2.bak'); load(F, K); N = 0
def R(a, b, note):
    global N; N += 1; rep(K, a, b, 'gov-dates2', note)
R("""                txt = clean(BeautifulSoup(page, 'html.parser').get_text(' '))
                m = re.search(r'<meta[^>]+(?:article:published_time|datePublished|pubdate)[^>]+content="([^"]+)"', page)
                nd = (sane(parse_date(m.group(1))) if m else None) or dateline_date(txt)""",
  """                txt = clean(BeautifulSoup(page, 'html.parser').get_text(' '))
                m = re.search(r'<meta[^>]+(?:article:published_time|datePublished|pubdate)[^>]+content="([^"]+)"', page)
                head = trim_headline(it['title'])[:40]
                at = txt.find(head) if head else -1
                nd = (sane(parse_date(m.group(1))) if m else None) or (dateline_date(txt[at:at + len(head) + 600]) if at >= 0 else None)""",
  'Article page: only the dateline after the story headline')
R("""def clean(s):""", '''def spa_consistency(items, log):
    """SPA story numbers rise over time. Use stories dated from their own dateline as reference points and reject any
    other date that contradicts them by more than 30 days."""
    def num(u):
        m = re.search(r'/N(\\d{5,})', u or ''); return int(m.group(1)) if m else None
    refs = sorted((num(i['url']), i['date']) for i in items.values() if i.get('source') == 'spa' and i.get('date_src') == 'dateline' and i.get('date') and num(i['url']))
    if not refs: return 0
    bad = 0
    for it in items.values():
        n = num(it.get('url'))
        if it.get('source') != 'spa' or not n or not it.get('date') or it.get('date_src') == 'dateline': continue
        d = dt.date.fromisoformat(it['date'])
        later = [dt.date.fromisoformat(rd) for rn, rd in refs if rn < n]      # published before this story
        earlier = [dt.date.fromisoformat(rd) for rn, rd in refs if rn > n]    # published after this story
        if (later and d < max(later) - dt.timedelta(days=30)) or (earlier and d > min(earlier) + dt.timedelta(days=30)):
            log.append(f"{it['url']}: {it['date']} ({it.get('date_src')}) contradicts SPA numbering — rejected")
            it['date'], it['date_src'] = None, 'unknown'; bad += 1
    return bad

def clean(s):''', 'SPA numbering cross-check')
R("""    print(f'date check: {redated} items dated from their article page;""",
  """    rejected = []; nbad = spa_consistency(items, rejected)
    if rejected: debug['rejected_dates'] = rejected; print('\\n'.join('date rejected: ' + r for r in rejected))
    print(f'date check: {redated} items dated from their article page; {nbad} dates rejected by the SPA numbering check;""",
  'Run the cross-check and log rejections')
open(F, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_gov_news_dates2'), 'Change table — Regulatory news dates, second fix')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
