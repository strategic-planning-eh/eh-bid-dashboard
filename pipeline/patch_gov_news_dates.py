"""patch_gov_news_dates.py — correct dates on the Regulatory news tab (02/10/2026).

Fault Youssef found: an SPA story datelined «الدمام 19 ربيع الآخر 1448 هـ الموافق 30 سبتمبر 2026 م» was shown as
06 Nov 2023. Two causes:
  1. To find a story's date the collector walked up the page from the link (up to 4 levels). On SPA's search page that
     can reach the container holding the whole results list, and the first date found there belonged to another story.
  2. The Arabic dateline was not trimmed off the headline (the trim expected a one-word Hijri month; «ربيع الآخر» has
     two), so the real date stayed buried in the title instead of being used.
Fix (fetch_gov_news.py):
  • Date order of trust: the dateline inside the story text («الموافق 30 سبتمبر 2026 م» / "Riyadh, September 30, 2026")
    → the story's own card (an ancestor that holds only this story's link, never a list) → the date in the page address
    (SharePoint) → the article page itself (opened only when nothing else gave a date) → unknown.
  • A date in the future, or before 2015, is rejected as a misread.
  • Arabic datelines with any Hijri month are trimmed off headlines, and section prefixes such as «بيئي /» removed.
  • Every item records where its date came from (date_src). Items carried over from earlier runs are re-dated the same
    way on the next run, so the 06 Nov 2023 entry corrects itself; nothing has to be deleted by hand.
Run once, then run the Government news workflow.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
F = os.path.join(HERE, 'fetch_gov_news.py'); K = 'fetch_gov_news.py'
if 'def dateline_date(' in open(F, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(F, F + '.pre-dates.bak'); load(F, K); N = 0
def R(a, b, note, **k):
    global N; N += 1; rep(K, a, b, 'gov-dates', note, **k)

R("def clean(s):", r'''AR_HIJRI = r'(?:محرم|صفر|ربيع الأول|ربيع الاول|ربيع الآخر|ربيع الاخر|ربيع الثاني|جمادى الأولى|جمادى الاولى|جمادى الآخرة|جمادى الاخرة|جمادى الثانية|رجب|شعبان|رمضان|شوال|ذو القعدة|ذو الحجة)'
def sane(d):
    """Reject impossible dates: in the future (more than a day ahead) or before 2015."""
    if not d: return None
    try:
        x = dt.date.fromisoformat(d)
    except Exception:
        return None
    today = dt.datetime.now(KSA).date()
    return d if dt.date(2015, 1, 1) <= x <= today + dt.timedelta(days=1) else None

def dateline_date(text):
    """The date written inside the story itself — the most reliable source.
    Arabic SPA: «المدينة 19 ربيع الآخر 1448 هـ الموافق 30 سبتمبر 2026 م»; English SPA: "Riyadh, September 30, 2026, SPA"."""
    t = clean(text)
    m = re.search(r'الموافق\s+([0-9٠-٩]{1,2}\s+\S+\s+[0-9٠-٩]{4})', t)
    if m: return sane(parse_date(m.group(1)))
    m = re.search(r'\b[A-Z][A-Za-z-]+,\s+((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})', t)
    if m: return sane(parse_date(m.group(1)))
    return None

def trim_headline(text):
    """Remove the dateline and anything after it, and a leading section label such as «بيئي /»."""
    t = clean(text)
    t = re.split(r'\s+\S+\s+[0-9٠-٩]{1,2}\s+' + AR_HIJRI + r'\s+[0-9٠-٩]{4}\s*هـ', t)[0]
    t = re.split(r'\s+\S+\s+[0-9٠-٩]{1,2}\s+\S+\s+[0-9٠-٩]{4}\s*هـ', t)[0]
    t = re.split(r'\s+(?:[A-Z][A-Za-z-]+),\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d', t)[0]
    t = re.sub(r'^[\u0600-\u06FF]{2,12}\s*/\s*', '', t)
    return t.strip()

def card_date(a, link_rx):
    """Date from the story's own card: walk up only while the ancestor holds this one story link."""
    node = a
    for _ in range(4):
        node = node.parent
        if node is None: return None
        links = {x['href'].split('#')[0] for x in node.find_all('a', href=True) if link_rx is None or link_rx.search(x['href'])}
        if len(links) > 1: return None          # reached a list of stories: any date here may belong to another one
        d = sane(parse_date(clean(node.get_text(' '))))
        if d: return d
    return None

def clean(s):''', 'Date helpers: dateline first, card only, sanity check, headline trim')

# official lists
R("""        # a date usually sits in the same card/list item: walk up to 3 ancestors
        ctx, node = '', a
        for _ in range(3):
            node = node.parent
            if node is None: break
            ctx = clean(node.get_text(' '))
            if parse_date(ctx): break
        out.append(dict(title=text, url=key, date=parse_date(ctx) or date_from_url(key)))""",
  """        d, src = dateline_date(text), 'dateline'
        if not d: d, src = card_date(a, rx), 'card'
        if not d: d, src = sane(date_from_url(key)), 'address'
        out.append(dict(title=trim_headline(text), url=key, date=d, date_src=src if d else 'unknown'))""",
  'Official lists: trusted date order')
# SPA
R("""            # SPA cards end with a dateline ("… Riyadh, September 21, 2026, SPA --"); keep the headline only
            text = re.split""", """            raw_text = text
            # SPA cards end with a dateline ("… Riyadh, September 21, 2026, SPA --"); keep the headline only
            text = re.split""", 'Keep the untrimmed card text for its dateline')
R("""            seen.add(href)
            ctx, node = '', a
            for _ in range(4):
                node = node.parent
                if node is None: break
                ctx = clean(node.get_text(' '))
                if parse_date(ctx): break
            out.append(dict(title=text, url=href, date=parse_date(ctx)))""",
  """            seen.add(href)
            d, dsrc = dateline_date(raw_text), 'dateline'
            if not d: d, dsrc = card_date(a, rx), 'card'
            out.append(dict(title=trim_headline(text), url=href, date=d, date_src=dsrc if d else 'unknown'))""",
  'SPA: dateline, then own card only')
# merge: new items carry date_src; existing items re-dated
R("""                if iid in items:
                    if not items[iid].get('date') and f.get('date'): items[iid]['date'] = f['date']
                    continue
                items[iid] = dict(id=iid, body=body['id'], title=title, lang=lang_of(title), date=f.get('date'), url=url, source=stype,
                                  tags=tag(title, cfg['tags']), first_seen=today.isoformat())""",
  """                if iid in items:
                    old = items[iid]
                    if f.get('date') and (old.get('date_src') in (None, 'unknown', 'card', 'address') or not old.get('date')) and f.get('date_src') in ('dateline', 'card', 'address'):
                        old['date'], old['date_src'] = f['date'], f['date_src']
                    continue
                items[iid] = dict(id=iid, body=body['id'], title=trim_headline(title), lang=lang_of(title), date=f.get('date'), date_src=f.get('date_src', 'unknown'), url=url, source=stype,
                                  tags=tag(title, cfg['tags']), first_seen=today.isoformat())""",
  'Merge keeps the most trusted date')
# re-date pass + article fallback before retention
R("""    # retention + near-duplicate collapse""",
  """    # ---- date check for every item on file (fixes items carried over from earlier runs)
    redated, art_budget = 0, int(cfg.get('article_date_lookups', 40))
    for it in items.values():
        d = dateline_date(it['title'])               # older titles still carry the dateline: use it, then trim it off
        it['title'] = trim_headline(it['title']) or it['title']
        if d: it['date'], it['date_src'] = d, 'dateline'
        if it.get('date_src') in ('dateline', 'article'):
            it['date'] = sane(it.get('date')); continue
        if it.get('date') and not sane(it['date']): it['date'] = None
        if it.get('date_src') is None:               # written before 02/10/2026: date may come from a neighbouring story
            it['date'], it['date_src'] = None, 'unknown'
        if not it.get('date'):
            ad = sane(date_from_url(it.get('url')))
            if ad: it['date'], it['date_src'] = ad, 'address'
        if not it.get('date') and art_budget > 0 and not a.no_browser:
            art_budget -= 1
            try:
                page = rendered_html(it['url'], settle_ms=1500)
                txt = clean(BeautifulSoup(page, 'html.parser').get_text(' '))
                m = re.search(r'<meta[^>]+(?:article:published_time|datePublished|pubdate)[^>]+content="([^"]+)"', page)
                nd = (sane(parse_date(m.group(1))) if m else None) or dateline_date(txt)
                if nd: it['date'], it['date_src'] = nd, 'article'; redated += 1
            except Exception as e:
                debug.setdefault('article_date_errors', []).append(f"{it['url']}: {type(e).__name__}")
    print(f'date check: {redated} items dated from their article page; {sum(1 for i in items.values() if not i.get("date"))} still without a date')

    # retention + near-duplicate collapse""", 'Re-date pass with article-page fallback')
open(F, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_gov_news_dates'), 'Change table — Regulatory news dates')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
