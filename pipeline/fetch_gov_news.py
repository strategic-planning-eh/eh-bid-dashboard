#!/usr/bin/env python3
"""fetch_gov_news.py — weekly collector for the Government tab under News & Intelligence.

Reads pipeline/gov_news_sources.json (which bodies, which sources), pulls the latest headlines from each source,
merges them with the previously published feed (rolling window, default 90 days), tags them by keyword, and writes:

    gov_news.json        the feed the page renders (items + per-body source status + freshness)
    gov_news_debug.json  what each adapter saw — sample anchors and errors — so a broken adapter can be fixed from
                         the workflow log without guessing at the site's HTML

Design rules (ways-of-working): "searched, none found" is recorded as such — a source that returns nothing gets
status "empty", a source that fails gets status "error" with the message; neither is ever left blank. Headlines are
kept in the language they were published in; nothing is translated or summarised here.

Usage:
    python3 fetch_gov_news.py [--config gov_news_sources.json] [--prev previous_feed.json] [--out gov_news.json]
                              [--debug gov_news_debug.json] [--no-browser] [--only mwan,ncec]

Sources of type "sharepoint" and "spa" need Playwright + Chromium (the page lists are rendered by JavaScript);
with --no-browser they are skipped and recorded as "skipped". Plain "rss" and "html" sources need only requests.
"""
import argparse, datetime as dt, hashlib, html as htmlmod, json, os, re, sys, time, traceback
from urllib.parse import urljoin, quote

try:
    import requests
except ImportError:  # keep the error readable in the Actions log
    sys.exit('fetch_gov_news.py needs `requests` (pip install requests beautifulsoup4)')
try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit('fetch_gov_news.py needs `beautifulsoup4` (pip install requests beautifulsoup4)')

KSA = dt.timezone(dt.timedelta(hours=3))
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 EH-Hub-gov-news/1.0'
HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ dates
AR_DIGITS = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
MONTHS = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])}
MONTHS.update({m[:3]: i for m, i in list(MONTHS.items())})
MONTHS.update({'sept': 9})
AR_MONTHS = {'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4, 'ابريل': 4, 'إبريل': 4, 'مايو': 5, 'يونيو': 6, 'يوليو': 7, 'أغسطس': 8, 'اغسطس': 8,
             'سبتمبر': 9, 'أكتوبر': 10, 'اكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12}

def parse_date(text):
    """Best-effort Gregorian date from a snippet of AR/EN text. Returns ISO date or None. Hijri-only dates return None."""
    if not text: return None
    t = str(text).translate(AR_DIGITS)
    m = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', t)                       # 2026-09-14
    if m:
        y, mo, d = map(int, m.groups())
        if 2000 <= y <= 2100 and 1 <= mo <= 12 and 1 <= d <= 31: return f'{y:04d}-{mo:02d}-{d:02d}'
    m = re.search(r'(\d{1,2})[/.](\d{1,2})[/.](\d{4})', t)                # 14/09/2026
    if m:
        d, mo, y = map(int, m.groups())
        if 2000 <= y <= 2100 and 1 <= mo <= 12 and 1 <= d <= 31: return f'{y:04d}-{mo:02d}-{d:02d}'
    m = re.search(r'([A-Za-z]{3,9})\.?\s+(\d{1,2}),?\s+(\d{4})', t)         # Dec 21, 2025
    if m and m.group(1).lower() in MONTHS:
        return f'{int(m.group(3)):04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}'
    m = re.search(r'(\d{1,2})\s+([A-Za-z]{3,9})\.?,?\s+(\d{4})', t)         # 21 December 2025
    if m and m.group(2).lower() in MONTHS:
        return f'{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}'
    m = re.search(r'(\d{1,2})\s+(' + '|'.join(AR_MONTHS) + r')\s+(\d{4})', t)  # 14 سبتمبر 2026
    if m: return f'{int(m.group(3)):04d}-{AR_MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}'
    m = re.search(r'([A-Za-z]{3}), (\d{1,2}) ([A-Za-z]{3}) (\d{4})', t)      # RFC-822 style in RSS
    if m and m.group(3).lower() in MONTHS:
        return f'{int(m.group(4)):04d}-{MONTHS[m.group(3).lower()]:02d}-{int(m.group(2)):02d}'
    return None

def clean(s):
    s = htmlmod.unescape(str(s or ''))
    s = re.sub(r'[\u200b\u200c\u200d\ufeff\u0640]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def lang_of(s):
    return 'ar' if re.search(r'[\u0600-\u06FF]', s or '') else 'en'

def item_id(url, title):
    return hashlib.sha1((url or title).encode('utf-8')).hexdigest()[:12]

def norm_title(s):
    return re.sub(r'[^\w]+', ' ', clean(s).lower())[:70].strip()

# ------------------------------------------------------------------ adapters
def http_get(url, timeout=40):
    r = requests.get(url, headers={'User-Agent': UA, 'Accept-Language': 'ar,en;q=0.8'}, timeout=timeout)
    r.raise_for_status()
    return r

def fetch_rss(src, dbg):
    r = http_get(src['url'])
    import xml.etree.ElementTree as ET
    root = ET.fromstring(r.content)
    out = []
    for it in root.iter():
        if it.tag.lower().endswith('item') or it.tag.lower().endswith('entry'):
            def g(*names):
                for n in names:
                    for c in it:
                        if c.tag.lower().split('}')[-1] == n and (c.text or c.attrib.get('href')):
                            return c.text or c.attrib.get('href')
                return ''
            title = clean(re.sub(r'<[^>]+>', ' ', g('title')))
            link = clean(g('link', 'guid'))
            date = parse_date(g('pubdate', 'published', 'updated', 'date')) or parse_date(clean(re.sub(r'<[^>]+>', ' ', g('description'))))
            if title and link: out.append(dict(title=title, url=link, date=date))
    dbg['sample'] = [(o['url'], o['title'][:60]) for o in out[:8]]
    return out

def anchors_from_html(html_text, base, pattern):
    soup = BeautifulSoup(html_text, 'html.parser')
    rx = re.compile(pattern) if pattern else None
    out, seen = [], set()
    for a in soup.find_all('a', href=True):
        href = urljoin(base, a['href'].strip())
        text = clean(a.get_text(' '))
        if rx and not rx.search(href): continue
        if len(text) < 12: continue                       # nav links, "read more"
        key = href.split('#')[0]
        if key in seen: continue
        seen.add(key)
        # a date usually sits in the same card/list item: walk up to 3 ancestors
        ctx, node = '', a
        for _ in range(3):
            node = node.parent
            if node is None: break
            ctx = clean(node.get_text(' '))
            if parse_date(ctx): break
        out.append(dict(title=text, url=key, date=parse_date(ctx)))
    return out, soup

def fetch_html(src, dbg):
    r = http_get(src['url'])
    out, soup = anchors_from_html(r.text, src['url'], src.get('link_pattern'))
    if not out:  # record what the page did contain so the pattern can be corrected
        dbg['sample'] = [(urljoin(src['url'], a['href']), clean(a.get_text(' '))[:60]) for a in soup.find_all('a', href=True)[:25]]
    else:
        dbg['sample'] = [(o['url'], o['title'][:60]) for o in out[:8]]
    return out

_PW = {'pw': None, 'browser': None}
def browser():
    if _PW['browser'] is None:
        from playwright.sync_api import sync_playwright
        _PW['pw'] = sync_playwright().start()
        _PW['browser'] = _PW['pw'].chromium.launch(headless=True)
    return _PW['browser']

def rendered_html(url, wait_for=None, settle_ms=2500):
    page = browser().new_page(user_agent=UA, locale='ar-SA')
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        try:
            page.wait_for_load_state('networkidle', timeout=20000)
        except Exception:
            pass
        if wait_for:
            try: page.wait_for_selector(wait_for, timeout=15000)
            except Exception: pass
        page.wait_for_timeout(settle_ms)
        return page.content()
    finally:
        page.close()

def fetch_sharepoint(src, dbg):
    html_text = rendered_html(src['url'])
    out, soup = anchors_from_html(html_text, src['url'], src.get('link_pattern'))
    if not out:
        dbg['sample'] = [(urljoin(src['url'], a['href']), clean(a.get_text(' '))[:60]) for a in soup.find_all('a', href=True) if 'News' in a['href']][:25]
    else:
        dbg['sample'] = [(o['url'], o['title'][:60]) for o in out[:8]]
    return out

def fetch_spa(src, cfg, dbg):
    spa = cfg['spa']; rx = re.compile(spa['link_pattern'])
    tried = []
    for tmpl in spa['search_urls']:
        url = tmpl.format(lang=src.get('lang', 'ar'), q=quote(src['query']))
        tried.append(url)
        try:
            html_text = rendered_html(url, settle_ms=3500)
        except Exception as e:
            dbg.setdefault('errors', []).append(f'{url}: {e}')
            continue
        soup = BeautifulSoup(html_text, 'html.parser')
        out, seen = [], set()
        for a in soup.find_all('a', href=True):
            href = urljoin(url, a['href'].strip()).split('?')[0]
            if not rx.search(href) or href in seen: continue
            text = clean(a.get_text(' '))
            if len(text) < 20:  # card links often wrap an image; take the card's heading instead
                card = a.find_parent(['article', 'li', 'div'])
                if card:
                    h = card.find(['h1', 'h2', 'h3', 'h4', 'p'])
                    text = clean(h.get_text(' ')) if h else text
            if len(text) < 20: continue
            seen.add(href)
            ctx, node = '', a
            for _ in range(4):
                node = node.parent
                if node is None: break
                ctx = clean(node.get_text(' '))
                if parse_date(ctx): break
            out.append(dict(title=text, url=href, date=parse_date(ctx)))
            if len(out) >= spa.get('max_per_query', 15): break
        if out:
            dbg['url'] = url; dbg['sample'] = [(o['url'], o['title'][:60]) for o in out[:8]]
            return out
        dbg.setdefault('sample_any', []).extend([(urljoin(url, a['href']), clean(a.get_text(' '))[:50]) for a in soup.find_all('a', href=True)[:20]])
    dbg['tried'] = tried
    return []

# ------------------------------------------------------------------ tagging / merge
def tag(title, tags):
    low = title.lower(); out = []
    for name, kws in tags.items():
        if any(k.lower() in low for k in kws): out.append(name)
    return out

def matches_body(title, body):
    low = title.lower()
    return any(a.lower() in low for a in body.get('aliases', []))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default=os.path.join(HERE, 'gov_news_sources.json'))
    ap.add_argument('--prev', default=None, help='previously published gov_news.json (items are carried forward within the retention window)')
    ap.add_argument('--out', default=os.path.join(HERE, 'gov_news.json'))
    ap.add_argument('--debug', default=os.path.join(HERE, 'gov_news_debug.json'))
    ap.add_argument('--no-browser', action='store_true')
    ap.add_argument('--only', default=None, help='comma-separated body ids')
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding='utf-8'))
    now = dt.datetime.now(KSA); today = now.date()
    retention = cfg.get('retention_days', 90)
    cutoff = (today - dt.timedelta(days=retention)).isoformat()
    only = set(a.only.split(',')) if a.only else None

    prev_items = {}
    if a.prev and os.path.exists(a.prev):
        try:
            for it in json.load(open(a.prev, encoding='utf-8')).get('items', []):
                prev_items[it['id']] = it
        except Exception as e:
            print('WARN previous feed unreadable:', e)

    items, bodies_out, debug = dict(prev_items), [], {'run': now.isoformat(timespec='minutes'), 'sources': []}
    for body in cfg['bodies']:
        if only and body['id'] not in only: continue
        statuses = []
        for src in body['sources']:
            dbg = {'body': body['id'], 'type': src['type'], 'lang': src.get('lang')}
            st = {'type': src['type'], 'lang': src.get('lang'), 'url': src.get('url') or ('SPA search: ' + src.get('query', '')), 'fetched': now.isoformat(timespec='minutes'), 'count': 0, 'new': 0, 'status': 'ok', 'note': ''}
            t0 = time.time()
            try:
                if src['type'] == 'rss': found = fetch_rss(src, dbg)
                elif src['type'] == 'html': found = fetch_html(src, dbg)
                elif src['type'] in ('sharepoint', 'spa'):
                    if a.no_browser:
                        found = []; st['status'] = 'skipped'; st['note'] = 'browser-rendered source skipped (--no-browser)'
                    elif src['type'] == 'sharepoint': found = fetch_sharepoint(src, dbg)
                    else: found = fetch_spa(src, cfg, dbg)
                else:
                    found = []; st['status'] = 'error'; st['note'] = 'unknown source type'
            except Exception as e:
                found = []; st['status'] = 'error'; st['note'] = f'{type(e).__name__}: {str(e)[:200]}'
                dbg['trace'] = traceback.format_exc()[-1500:]
            st['seconds'] = round(time.time() - t0, 1)
            for f in found:
                title = clean(f['title']); url = f['url']
                if not title or not url: continue
                iid = item_id(url, title)
                stype = 'spa' if src['type'] == 'spa' else 'official'
                if src['type'] == 'spa' and not matches_body(title, body):
                    # SPA search returns loosely related stories; keep them out unless the body is named in the headline
                    dbg.setdefault('dropped_unmatched', []).append(title[:70]); continue
                if iid in items:
                    if not items[iid].get('date') and f.get('date'): items[iid]['date'] = f['date']
                    continue
                items[iid] = dict(id=iid, body=body['id'], title=title, lang=lang_of(title), date=f.get('date'), url=url, source=stype,
                                  tags=tag(title, cfg['tags']), first_seen=today.isoformat())
                st['new'] += 1
            st['count'] = len(found)
            if st['status'] == 'ok' and not found: st['status'] = 'empty'; st['note'] = st['note'] or 'source reachable, no items found'
            statuses.append(st); debug['sources'].append(dbg)
            print(f"{body['id']:6s} {src['type']:10s} {st['status']:7s} found={st['count']:3d} new={st['new']:3d} {st['seconds']}s {st['note']}")
        bodies_out.append({k: body[k] for k in ('id', 'en', 'ar', 'short', 'site') if k in body} | {'robots_disallow': body.get('robots_disallow', False), 'map_note': body.get('map_note', ''), 'sources': statuses})

    # retention + near-duplicate collapse (same body, same normalised title → keep the official one, else the earlier)
    kept, by_key = [], {}
    for it in items.values():
        d = it.get('date') or it.get('first_seen')
        if d and d < cutoff: continue
        key = (it['body'], norm_title(it['title']))
        if key in by_key:
            old = by_key[key]
            if old['source'] == 'spa' and it['source'] == 'official': by_key[key] = it
            continue
        by_key[key] = it
    kept = sorted(by_key.values(), key=lambda x: (x.get('date') or x['first_seen'], x['first_seen']), reverse=True)

    # feed week (Sunday–Saturday, matching What's New)
    wk_start = today - dt.timedelta(days=(today.weekday() + 1) % 7)
    feed = {'generated': now.isoformat(timespec='minutes'), 'generated_ksa': now.strftime('%d %b %Y, %H:%M (KSA)'),
            'week_from': wk_start.isoformat(), 'week_to': (wk_start + dt.timedelta(days=6)).isoformat(),
            'retention_days': retention, 'bodies': bodies_out, 'items': kept,
            'note_en': 'Headlines are shown in the language they were published in. "Official" = the body\'s own site; "SPA" = Saudi Press Agency coverage. Bodies whose sites disallow automated access are followed through SPA only.',
            'note_ar': 'تُعرض العناوين بلغة نشرها الأصلية. «رسمي» = موقع الجهة نفسها؛ «واس» = تغطية وكالة الأنباء السعودية. الجهات التي تمنع مواقعها الوصول الآلي تُتابَع عبر واس فقط.'}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or '.', exist_ok=True)
    json.dump(feed, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(debug, open(a.debug, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    new_total = sum(s['new'] for b in bodies_out for s in b['sources'])
    print(f'\nfeed: {len(kept)} items kept ({new_total} new this run) across {len(bodies_out)} bodies → {a.out}')
    if _PW['browser'] is not None:
        _PW['browser'].close(); _PW['pw'].stop()

if __name__ == '__main__':
    main()
