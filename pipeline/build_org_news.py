#!/usr/bin/env python3
"""build_org_news.py — adds the 'News & Vision 2030' section to every organisation profile (Youssef, 10 Nov 2026).

Reads org_profiles.json (from build_org_profiles.py) and four News & Intelligence sources, and writes the same file back with
  news_items   one record per news item / project / strategy line (stored once, referenced by id)
  news_themes  the sector labels (EN/AR)
  p['news']    per organisation: mentions[] (the item names the organisation), context[] (the item is about its sector),
               themes[] (its sectors), eligible (clients and Tier 1–2 get sector context; everyone gets mentions)

Sources (nothing is fetched from the web — only what the hub already publishes):
  --news   hub/eh_news_intelligence.html      curated corporate & government briefing (const DATA)
  --gov    site/gov_news.json                 Regulatory news weekly feed   (--gov-manual pipeline/gov_news_manual.json as a fallback)
  --brief  pipeline/reg_brief.json            Regulatory news monthly brief
  --v2030  hub/vision2030_dashboard.html      Vision 2030 projects   } read through org_news_extract.js (needs node);
  --pif    hub/pif_strategy_2026_2030.html    PIF Strategy 2026–2030 } if node is missing these two are skipped and the report says so
Rules live in org_news_config.json (sectors, extra search names, blocked matches). A match report is written with --report.
"""
import argparse, json, os, re, subprocess, sys, unicodedata, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- text helpers
def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    s = re.sub(r'[ـ​-‏ً-ْ]', '', s)
    s = re.sub(r'[إأآ]', 'ا', s).replace('ى', 'ي').replace('ة', 'ه')
    s = s.replace('’', "'").replace('‘', "'")
    s = re.sub(r"[^\w؀-ۿ']+", ' ', s)
    return ' ' + s.strip() + ' '

LEGAL = (r"\b(co|company|ltd|limited|llc|est|establishment|corporation|corp|inc|jsc|holding|group|one person|one-person|branch|office|ksa|the)\b"
         r"|شركه|مؤسسه|المحدوده|ذات مسؤوليه محدوده|شخص واحد|القابضه|مجموعه|فرع|مهنيه|مساهمه سعوديه|مساهمه")
GENERIC = set('saudi arabia arabian national environment environmental services service consulting consultant consultants office company gulf green '
              'vision energy water power general international united advanced contracting engineering trading industrial industry factory '
              'السعوديه العربيه الوطنيه البيئه البيئيه للخدمات للاستشارات مكتب الخليج الخضراء للمقاولات الهندسيه للتجاره للصناعه مصنع العالميه المتحده المتقدمه'.split())

def variants(p, extra, never):
    """Search names for one organisation → (cores, acronyms). Cores are matched case-insensitively on word boundaries,
    acronyms case-sensitively. Deliberately conservative: a name that is one generic word is never used."""
    never_n = {norm(x).strip() for x in never}; never_raw = set(never)
    names = [p['name']] + [a for a in (p.get('aliases') or []) if len(a) <= 70] + list(p.get('tracker_names') or []) + list(extra or [])
    cores, acr = set(), set()
    for raw in names:
        raw = str(raw or '').replace('\n', ' ')
        for par in re.findall(r'\(([^)]{2,40})\)', raw):
            par = par.strip()
            if re.fullmatch(r'[A-Z][A-Za-z&\-]{1,9}', par) and sum(c.isupper() for c in par) >= 2 and par not in never_raw: acr.add(par)
            elif re.search(r'[؀-ۿ]', par) or len(par.split()) >= 2: names.append(par) if par not in names and not re.search(r'formerly|One-Person|شخص', par) else None
        base = re.sub(r'\([^)]*\)', ' ', raw)
        if re.fullmatch(r'\s*[A-Z][A-Z&\-]{1,9}\s*', base):                                   # the whole name is an acronym (CEER, NEOM, ARAMCO)
            if base.strip() not in never_raw: acr.add(base.strip())
            if len(base.strip()) < 5: continue
        n = re.sub(LEGAL, ' ', norm(base)); n = re.sub(r'\s+', ' ', n).strip()
        if not n or n in never_n: continue
        toks = n.split(); spec = [t for t in toks if t not in GENERIC and len(t) > 1]
        if len(toks) == 1:
            if len(n) >= 5 and n not in GENERIC: cores.add(n)
        elif spec and len(n) >= 9:                                                              # at least one word that is not generic
            cores.add(n)
    for x in (extra or []):                                                                    # names added by hand are always used as written
        if re.fullmatch(r'[A-Z][A-Za-z&\-]{1,9}', x) and sum(c.isupper() for c in x) >= 2: acr.add(x)
        else: cores.add(re.sub(r'\s+', ' ', norm(x)).strip())
    return {c for c in cores if c and c not in never_n}, acr

def find_in(cores, acr, text_norm, text_raw):
    for c in cores:
        if (' ' + c + ' ') in text_norm: return c
    for a in acr:
        if re.search(r'(?<![A-Za-z0-9])' + re.escape(a) + r'(?![A-Za-z0-9])', text_raw): return a
    return None

AR_MONTHS = {'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4, 'ابريل': 4, 'مايو': 5, 'يونيو': 6, 'يوليو': 7, 'أغسطس': 8, 'اغسطس': 8, 'سبتمبر': 9, 'أكتوبر': 10, 'اكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12}
EN_MONTHS = {m: i for i, m in enumerate('january february march april may june july august september october november december'.split(), 1)}
def ar_date(s):
    m = re.search(r'(\d{1,2})\s+(\S+)\s+(\d{4})', s or '')
    return f"{int(m.group(3)):04d}-{AR_MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}" if m and m.group(2) in AR_MONTHS else None

def text_themes(text, rules):
    out = []
    for pat, th in rules:
        if re.search(pat, text, re.I):
            out += [t for t in th if t not in out]
    return out

# ---------------------------------------------------------------- sources → items
def load_news(path, cfg, ar):
    html = open(path, encoding='utf-8').read()
    i = html.find('const DATA = ['); j = html.find('\n];', i)
    if i < 0 or j < 0: raise ValueError('const DATA not found in ' + path)
    items = []
    for d in json.loads(html[i + len('const DATA = '):j + 2]):
        th = cfg['news_item_themes'].get(d['id'])
        if th is None: th = text_themes(' '.join([d.get('entity', ''), d.get('group', ''), d.get('giga', ''), d.get('headline', '')]), cfg['news_text_rules'])
        url = next((s.get('url') for s in d.get('sources', []) if s.get('url')), '')
        items.append(dict(id='news:' + d['id'], src='news', date=d.get('dateISO') or '', en=d.get('headline', ''), ar=ar.get(d['id'], ''),
                          why_en=d.get('relevance', ''), why_ar='', who=d.get('entity', ''), url=url, themes=th,
                          _subject=' '.join([d.get('entity', ''), d.get('headline', '')]),
                          _body=' '.join([d.get('partners', ''), d.get('detail', ''), d.get('giga', ''), d.get('implications', '')])))
    return items

def load_gov(feed_path, manual_path, sources_path, brief_path, cfg):
    items, note = [], ''
    bodies = {}
    if sources_path and os.path.exists(sources_path):
        bodies = {b['id']: b for b in json.load(open(sources_path, encoding='utf-8'))['bodies']}
    feed = None
    if feed_path and os.path.exists(feed_path):
        try:
            feed = json.load(open(feed_path, encoding='utf-8'))
            if not feed.get('items'): feed = None
        except Exception: feed = None                                # sealed or unreadable feed → fall back to the manual captures
    if feed:
        for it in feed['items']:
            items.append(dict(id='reg:' + str(it['id']), src='reg', date=it.get('date') or '', en=it['title'] if it.get('lang') == 'en' else '',
                              ar=it['title'] if it.get('lang') != 'en' else '', why_en='', why_ar='', who=it.get('body', ''), url=it.get('url', ''),
                              themes=list(cfg['gov_bodies'].get(it.get('body'), {}).get('themes', [])), body=it.get('body'), _subject=it['title'], _body=''))
        note = f"weekly feed ({len(items)} stories)"
    elif manual_path and os.path.exists(manual_path):
        seen = set()
        for cap in json.load(open(manual_path, encoding='utf-8')).get('captures', []):
            for bid, rows in cap.get('bodies', {}).items():
                al = [norm(a.strip('"«»')).strip() for a in bodies.get(bid, {}).get('aliases', [])]
                for r in rows:
                    title = re.sub(r'^\s*\S+\s*/\s*', '', r.get('title') or '').strip()         # drop the SPA desk prefix ("اقتصادي / …")
                    tn = norm(title)
                    if al and not any((' ' + a + ' ') in tn or a in tn for a in al if a): continue   # collector's rule: the body is named in the headline
                    key = (bid, r.get('n'))
                    if key in seen: continue
                    seen.add(key)
                    items.append(dict(id=f"reg:spa{r.get('n')}", src='reg', date=ar_date(r.get('date_ar')) or cap.get('date', ''), en='', ar=title, why_en='', why_ar='',
                                      who=bid, url=f"https://spa.gov.sa/N{r.get('n')}", themes=list(cfg['gov_bodies'].get(bid, {}).get('themes', [])), body=bid, _subject=title, _body=''))
        note = f"manual captures only ({len(items)} stories) — the weekly feed was not available to this build"
    else:
        note = 'not available to this build'
    for it in items:
        b = bodies.get(it['body'], {}); it['who'] = b.get('short') or b.get('en') or it['body']; it['who_ar'] = b.get('ar', '')
    if brief_path and os.path.exists(brief_path):
        for br in json.load(open(brief_path, encoding='utf-8')).get('briefs', []):
            for bb in br.get('by_body', []):
                b = bodies.get(bb['body'], {})
                items.append(dict(id=f"reg:brief-{br['month']}-{bb['body']}", src='reg', date=br.get('written') or br['month'] + '-28', en=bb.get('en', ''), ar=bb.get('ar', ''),
                                  why_en='', why_ar='', who=(b.get('short') or bb['body']) + ' · monthly brief ' + br['month'], who_ar=(b.get('ar') or bb['body']) + ' · الموجز الشهري ' + br['month'],
                                  url='', themes=list(cfg['gov_bodies'].get(bb['body'], {}).get('themes', [])), body=bb['body'], brief=True, _subject=bb.get('en', ''), _body=''))
    return items, note

def load_js(v_path, p_path, cfg):
    try:
        r = subprocess.run(['node', os.path.join(HERE, 'org_news_extract.js'), v_path, p_path], capture_output=True, text=True, timeout=60)
        d = json.loads(r.stdout)
    except Exception as e:
        return [], [], f'not read ({e.__class__.__name__}: node could not run the extractor)'
    v_items, p_items = [], []
    V = d.get('v2030')
    if V:
        m = re.match(r'(\w+)\s+(\d{4})', V.get('reviewed') or ''); vdate = f"{m.group(2)}-{EN_MONTHS.get(m.group(1).lower(), 1):02d}" if m else ''
        for pr in V['projects']:
            th = cfg['v2030_project_themes'].get(pr['name'])
            if th is None:
                th = []
                for s in pr.get('sectors', []): th += [t for t in cfg['v2030_sector_map'].get(s, []) if t not in th]
            art = V['ar_txt'].get(pr['name'], {}); arn = V['ar_names'].get(pr['name'], pr['name'])
            st_en = pr.get('status', ''); st_ar = V['ar_status'].get(st_en, st_en)
            partners = ' '.join(x.get('n', '') for x in pr.get('partners', []))
            v_items.append(dict(id='v2030:' + pr['name'], src='v2030', date=vdate, en=f"{pr['name']} — {st_en}" + (f", completion {pr['completion']}" if pr.get('completion') else ''),
                                ar=f"{arn} — {st_ar}", why_en=pr.get('desc', ''), why_ar=art.get('desc', ''), who=pr.get('lead', ''), who_ar=art.get('lead', ''), url='', themes=th,
                                _subject=' '.join([pr['name'], pr.get('lead', '')]), _body=partners + ' ' + pr.get('note', '')))
    P = d.get('pif')
    if P:
        pdate = (P.get('build') or {}).get('date', '')
        for e in P.get('ecosystems', []):
            p_items.append(dict(id=f"pif:eco{e['n']}", src='pif', date=pdate, en=f"PIF investment group {e['n']:02d}: {e['en']}", ar=f"مجموعة استثمارات الصندوق {e['n']:02d}: {e['ar']}",
                                why_en=e['focus'][0], why_ar=e['focus'][1], who='PIF Strategy 2026–2030, ' + e.get('page', ''), who_ar='استراتيجية الصندوق 2026–2030',
                                url='', themes=cfg['pif_ecosystem_themes'].get(str(e['n']), []), _subject=e['en'] + ' ' + ' '.join(e.get('cos', [])), _body=e['focus'][0]))
        for k, g in enumerate(P.get('relevance', [])):
            if g.get('rel') not in ('H', 'M'): continue
            txt = g['en'] + ' ' + g['j'][0]
            p_items.append(dict(id=f"pif:rel{k}", src='pif', date=pdate, en=g['en'], ar=g.get('ar', ''), why_en=g['j'][0], why_ar=g['j'][1], who=g.get('src', ''), who_ar='استراتيجية الصندوق 2026–2030',
                                url='', themes=[], _subject=txt, _body='', _mention_only=True))
        for k, g in enumerate(P.get('giga', [])):
            p_items.append(dict(id=f"pif:giga{k}", src='pif', date=pdate, en=f"{g['p']} — {g['item'][0]}: {g['d'][0]}", ar=f"{g['p']} — {g['item'][1]}: {g['d'][1]}",
                                why_en='', why_ar='', who=g.get('ssrc', ''), who_ar='استراتيجية الصندوق 2026–2030', url='', themes=[], _subject=g['p'], _body='', _mention_only=True))
    return v_items, p_items, '; '.join(d.get('errors') or [])

# ---------------------------------------------------------------- organisations → themes
def org_themes(p, cfg):
    """Sector themes for one organisation, and how they were decided (shown in the report, never guessed silently)."""
    if p['name'] in cfg['overrides']: return list(cfg['overrides'][p['name']]), 'override'
    roles = p.get('roles') or []; cat = p.get('cat') or ''
    is_client = 'client' in roles or 'eh-client' in roles
    if not is_client and ('competitor' in roles or 'winner' in roles or 'Competitor' in cat):
        return ['waste'], 'competitor'                               # a rival in EH's own market: the waste / environmental-regulation theme, whatever sector the map shows
    th, how = [], ''
    sec = (p.get('sec') or '').strip()
    if sec and sec in cfg['sector_map']: th += cfg['sector_map'][sec]; how = 'map sector'
    if not th:
        hay = ' | '.join([p['name']] + list(p.get('tracker_names') or []) + [a for a in (p.get('aliases') or []) if len(a) <= 70])
        for pat, t in cfg['name_rules']:
            if re.search(pat, hay, re.I): th += [x for x in t if x not in th]
        if th: how = 'name'
    if p.get('tier') == 'GOV' or p.get('typ') == 'GOV-ENTITY' or cat.startswith('Government') or cat.startswith('Regulators'):
        if 'public' not in th: th.append('public')
        how = how or 'government body'
    return th, how

def eligible(p):
    roles = p.get('roles') or []
    return 'client' in roles or 'eh-client' in roles or p.get('tier') in ('Tier 1', 'Tier 2')

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--profiles', required=True); ap.add_argument('--out', default=None)
    ap.add_argument('--news', default=os.path.join(HERE, '..', 'hub', 'eh_news_intelligence.html'))
    ap.add_argument('--v2030', default=os.path.join(HERE, '..', 'hub', 'vision2030_dashboard.html'))
    ap.add_argument('--pif', default=os.path.join(HERE, '..', 'hub', 'pif_strategy_2026_2030.html'))
    ap.add_argument('--gov', default=None); ap.add_argument('--gov-manual', default=os.path.join(HERE, 'gov_news_manual.json'))
    ap.add_argument('--gov-sources', default=os.path.join(HERE, 'gov_news_sources.json')); ap.add_argument('--brief', default=os.path.join(HERE, 'reg_brief.json'))
    ap.add_argument('--config', default=os.path.join(HERE, 'org_news_config.json')); ap.add_argument('--ar', default=os.path.join(HERE, 'org_news_ar.json'))
    ap.add_argument('--report', default=None)
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding='utf-8'))
    ar = json.load(open(a.ar, encoding='utf-8')).get('headlines', {}) if os.path.exists(a.ar) else {}
    data = json.load(open(a.profiles, encoding='utf-8')); orgs = data['orgs']

    status = {}
    try: news = load_news(a.news, cfg, ar); status['news'] = f'{len(news)} items'
    except Exception as e: news = []; status['news'] = f'not read ({e})'
    gov, status['reg'] = load_gov(a.gov, a.gov_manual, a.gov_sources, a.brief, cfg)
    v2030, pif, err = load_js(a.v2030, a.pif, cfg)
    status['v2030'] = f'{len(v2030)} projects' if v2030 else 'not read' + (f' ({err})' if err else '')
    status['pif'] = f'{len(pif)} lines' if pif else 'not read' + (f' ({err})' if err else '')
    items = news + gov + v2030 + pif
    for it in items:
        it['_sn'] = norm(it['_subject']); it['_bn'] = norm(it['_body']); it['_raw'] = it['_subject'] + ' ' + it['_body']

    blocked = {(o, i) for o, i in cfg.get('block', [])}
    body_orgs = {}
    for bid, b in cfg['gov_bodies'].items():
        for o in b['orgs']: body_orgs.setdefault(o, set()).add(bid)
    by_name = {p['name'] for p in orgs}
    cap = int(cfg.get('gov_context_cap', 8))
    used = set(); report = dict(sources=status, orgs=[], no_sector=[], untranslated=[], bodies_without_profile=[])
    for bid, b in cfg['gov_bodies'].items():
        if not any(o in by_name for o in b['orgs']): report['bodies_without_profile'].append(bid)

    for p in orgs:
        cores, acr = variants(p, cfg['extra_names'].get(p['name']), cfg['never_names'])
        mentions = []
        for it in items:
            if (p['name'], it['id']) in blocked: continue
            hit = None; level = None
            if it['src'] == 'reg' and it.get('body') in body_orgs.get(p['name'], ()): hit, level = 'followed body', 1
            else:
                h = find_in(cores, acr, it['_sn'], it['_subject'])
                if h: hit, level = h, 1
                else:
                    h = find_in(cores, acr, it['_bn'], it['_body'])
                    if h: hit, level = h, 2
            if hit: mentions.append((level, it, hit))
        mentions.sort(key=lambda t: t[1]['date'] or '0000', reverse=True)
        mentions.sort(key=lambda t: t[0])                           # named in the headline first, then named in the detail; newest first inside each
        m_ids = [it['id'] for _, it, _ in mentions]
        el = eligible(p); themes, how = (org_themes(p, cfg) if el else ([], ''))
        ctx = []
        if themes:
            c = [it for it in items if it['id'] not in m_ids and not it.get('_mention_only') and (p['name'], it['id']) not in blocked and set(it['themes']) & set(themes)]
            c.sort(key=lambda it: it['date'] or '0000', reverse=True)
            n_reg = 0
            for it in c:
                if it['src'] == 'reg':
                    if n_reg >= cap: continue
                    n_reg += 1
                ctx.append(it['id'])
        p['news'] = dict(mentions=m_ids, primary=sum(1 for l, _, _ in mentions if l == 1), context=ctx, themes=themes, eligible=el)
        used.update(m_ids); used.update(ctx)
        if el and not themes: report['no_sector'].append(dict(name=p['name'], cat=p.get('cat'), tier=p.get('tier')))
        if m_ids or themes:
            report['orgs'].append(dict(name=p['name'], cat=p.get('cat'), tier=p.get('tier'), themes=themes, themes_from=how,
                                       mentions=[dict(id=it['id'], matched_on=hit, where='headline' if l == 1 else 'detail', title=(it['en'] or it['ar'])[:110]) for l, it, hit in mentions],
                                       context=len(ctx)))

    pub = []
    for it in items:
        if it['id'] not in used: continue
        o = {k: v for k, v in it.items() if not k.startswith('_') and k not in ('body',) and v not in ('', None, [])}
        o.setdefault('en', ''); o.setdefault('ar', ''); pub.append(o)
        if it['src'] == 'news' and not it['ar']: report['untranslated'].append(it['id'])
    data['news_items'] = pub
    data['news_themes'] = cfg['themes']
    data['news_sources'] = status
    json.dump(data, open(a.out or a.profiles, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    n_m = sum(1 for p in orgs if p['news']['mentions']); n_c = sum(1 for p in orgs if p['news']['context'])
    print(f"org news: {len(pub)} items linked · {n_m} organisations named in the news · {n_c} with sector context · "
          f"{len(report['no_sector'])} clients / Tier 1–2 with no sector on record")
    for k, v in status.items(): print(f'  source {k}: {v}')
    if report['bodies_without_profile']: print('  followed bodies with no organisation profile:', ', '.join(report['bodies_without_profile']))
    if report['untranslated']: print('  news headlines with no Arabic yet (shown in English):', ', '.join(report['untranslated']))
    if a.report:
        report['built'] = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).strftime('%Y-%m-%d %H:%M KSA')
        json.dump(report, open(a.report, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
