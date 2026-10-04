"""patch_gov_news_spa_meta.py — SPA story dates read from the story page itself (02/10/2026).

The story Youssef checked (https://spa.gov.sa/N2689556, «نائب أمير الشرقية يطّلع على مشاريع ومبادرات وزارة البيئة…»)
was still missing from "This feed week". Opening it shows why the earlier fixes were not enough: SPA's search results do
not carry the story's date reliably, but every SPA story page does — in its description tag, which starts with the
dateline («الدمام 19 ربيع الآخر 1448 هـ الموافق 30 سبتمبر 2026 م واس …»), and its picture is filed under a year-month
folder (…/backend/original/202609/…). The page is plain HTML, so no browser is needed.
Rule now, for every SPA story on file: unless its date already came from its own dateline or its own page, the collector
opens the story page (plain request), reads the date from the description tag, and checks it against the picture's
year-month folder. That date replaces any date guessed from the search results. Up to 120 story pages per run.
Run once, then run the Government news workflow.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
F = os.path.join(HERE, 'fetch_gov_news.py'); K = 'fetch_gov_news.py'
if 'def spa_story_date(' in open(F, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(F, F + '.pre-spameta.bak'); load(F, K); N = 0
def R(a, b, note):
    global N; N += 1; rep(K, a, b, 'spa-meta', note)
R("def spa_consistency(items, log):", r'''def spa_story_date(url):
    """Date of an SPA story from its own page: the dateline at the start of the description tag, checked against the
    picture's year-month folder. Plain HTTP — SPA story pages are server-rendered."""
    html = http_get(url, timeout=25).text
    desc = ''
    for prop in ('og:description', 'description', 'twitter:description'):
        m = re.search(r'<meta[^>]+(?:property|name)="' + re.escape(prop) + r'"[^>]+content="([^"]{0,600})', html) or \
            re.search(r'<meta[^>]+content="([^"]{0,600})"[^>]+(?:property|name)="' + re.escape(prop) + r'"', html)
        if m: desc = htmlmod.unescape(m.group(1)); break
    d = dateline_date(desc[:300])
    img = re.search(r'/backend/original/(20\d\d)(\d\d)/', html)
    if d and img and d[:7] != f'{img.group(1)}-{img.group(2)}':
        # a picture can be filed a day or so later at a month boundary; reject only clear disagreements
        dd = dt.date.fromisoformat(d); im = dt.date(int(img.group(1)), int(img.group(2)), 1)
        if abs((dd.replace(day=1) - im).days) > 40: return None, f'dateline {d} disagrees with picture folder {img.group(1)}-{img.group(2)}'
    return d, ('ok' if d else 'no dateline in description')

def spa_consistency(items, log):''', 'SPA story-page date reader')
R("""        if d: it['date'], it['date_src'] = d, 'dateline'
        if it.get('date_src') in ('dateline', 'article'):""",
  """        if d: it['date'], it['date_src'] = d, 'dateline'
        if it.get('source') == 'spa' and it.get('date_src') not in ('dateline', 'page') and spa_budget > 0:   # SPA: the story page decides
            spa_budget -= 1
            try:
                nd, why = spa_story_date(it['url'])
                if nd:
                    if nd != it.get('date'): redated += 1
                    it['date'], it['date_src'] = nd, 'page'; continue
                debug.setdefault('spa_story_dates', []).append(f"{it['url']}: {why}")
            except Exception as e:
                debug.setdefault('spa_story_dates', []).append(f"{it['url']}: {type(e).__name__}")
        if it.get('date_src') in ('dateline', 'article', 'page'):""", 'Every SPA story not yet dated from its own text: read its page')
R("""    redated, art_budget = 0, int(cfg.get('article_date_lookups', 40))""",
  """    redated, art_budget = 0, int(cfg.get('article_date_lookups', 40))
    spa_budget = int(cfg.get('spa_story_lookups', 120))""", 'Budget for SPA story pages')
open(F, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_gov_news_spa_meta'), 'Change table — SPA story dates from the story page')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
