#!/usr/bin/env python3
"""
refresh_map_banalytics.py — rebuilds the BANALYTICS block embedded in the Stakeholder &
Competitive Map from the freshly generated Bid & Tender app, so the map's Bid View and
Saudi Map never show a stale bid snapshot.

  python pipeline/refresh_map_banalytics.py --map site/EH_Stakeholder_Map_CURRENT.html \
                                            --bids site/EH_Bid_Analysis_CURRENT.html

Run AFTER the bid pipeline and BEFORE build_changelog.py. Idempotent.
"""
import argparse, json, re, unicodedata, sys, datetime as dt

REGIONS = ['Jeddah', 'Makkah City', 'Rabigh', 'Other Makkah Region', 'Madinah Region', 'Riyadh', 'Qassim Region',
           'Eastern Province', 'Tabuk Region', 'Hail Region', 'Al Jawf Region', 'Northern Borders Region', 'Southern Region']
# keyword → region (EN + AR); first match wins, longest keys first
KW = {
    'Jeddah': ['jeddah', 'جدة', 'جده', 'king abdulaziz university', 'جامعة الملك عبدالعزيز'],
    'Makkah City': ['makkah', 'mecca', 'مكة', 'مكه'],
    'Rabigh': ['rabigh', 'رابغ', 'petro rabigh', 'بترو رابغ', 'kaec', 'king abdullah economic city', 'مدينة الملك عبدالله الاقتصادية'],
    'Other Makkah Region': ['taif', 'الطائف', 'thuwal', 'ثول', 'kaust', 'كاوست', 'jamoum', 'الجموم', 'khulais', 'خليص'],
    'Madinah Region': ['madinah', 'medina', 'المدينة', 'yanbu', 'ينبع', 'المدينه'],
    'Riyadh': ['riyadh', 'الرياض', 'kharj', 'الخرج', 'diriyah', 'الدرعية', 'qiddiya', 'القدية'],
    'Qassim Region': ['qassim', 'القصيم', 'buraydah', 'بريدة', 'unaizah', 'عنيزة'],
    'Eastern Province': ['jubail', 'الجبيل', 'dammam', 'الدمام', 'dhahran', 'الظهران', 'khobar', 'الخبر', 'ras al-khair', 'ras al khair', 'رأس الخير', 'راس الخير', 'hofuf', 'الهفوف', 'al ahsa', 'الأحساء', 'الاحساء', 'qatif', 'القطيف', 'eastern province', 'المنطقة الشرقية', 'khafji', 'الخفجي', 'abqaiq', 'بقيق'],
    'Tabuk Region': ['tabuk', 'تبوك', 'neom', 'نيوم', 'duba', 'ضباء', 'umluj', 'أملج', 'red sea', 'البحر الأحمر'],
    'Hail Region': ['hail', 'حائل'],
    'Al Jawf Region': ['jawf', 'الجوف', 'sakaka', 'سكاكا'],
    'Northern Borders Region': ['arar', 'عرعر', 'rafha', 'رفحاء', 'northern borders', 'الحدود الشمالية', 'waad al shamal', 'وعد الشمال'],
    'Southern Region': ['jizan', 'jazan', 'جازان', 'جيزان', 'najran', 'نجران', 'abha', 'أبها', 'ابها', 'asir', 'عسير', 'baha', 'الباحة', 'khamis', 'خميس مشيط', 'sharurah', 'شرورة'],
}
COMP_CATS = ('Active Competitors', 'Direct Competitors', 'Indirect / Adjacent Competitors')
CLIENT_CATS = ('EH Clients', 'Clients / Potential Clients', 'Government Clients & Institutions')

def norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200d\ufeff\u064b-\u0652]', '', s)
    s = re.sub(r'[إأآا]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي')
    s = re.sub(r'\b(company|co\.?|ltd\.?|llc|est\.?|establishment|for|the|and|&|شركة|شركه|مؤسسة|مؤسسه|ال)\b', ' ', s.casefold())
    return re.sub(r'[^\w\u0600-\u06FF]+', ' ', s).strip()

def region_of(text):
    t = norm(text).replace(' ', '')
    for rg, keys in KW.items():
        for k in keys:
            if norm(k).replace(' ', '') in t:
                return rg
    return None

def grab(html, sid):
    m = re.search(r'(<script id="%s" type="application/json">)(.*?)(</script>)' % sid, html, re.S)
    return m, json.loads(m.group(2))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--map', required=True); ap.add_argument('--bids', required=True)
    a = ap.parse_args()
    mh = open(a.map, encoding='utf-8').read(); bh = open(a.bids, encoding='utf-8').read()
    _, D = grab(mh, 'DATA'); nodes = D['nodes']
    _, BAALL = grab(bh, 'BA'); B = BAALL['both']
    mban, OLD = grab(mh, 'BANALYTICS')
    names = {norm(n['n']): n for n in nodes}
    def in_map(name):
        k = norm(name)
        if k in names: return True
        return any(k and (k in x or x in k) and len(min(k, x, key=len)) >= max(10, 0.7 * len(max(k, x, key=len))) for x in names)

    kpi = B['kpi']; bl = B['bidlist']
    competitors = [{'name': c['name'], 'in_map': in_map(c['name']), 'appearances': c.get('encounters', 0), 'wins': c.get('wins', 0),
                    'dq': c.get('dq', 0), 'avg_price': c.get('avg_price'), 'undercut_pct': c.get('undercut_pct')} for c in B['competitors']]
    clients = [dict(c, in_map=in_map(c['name']),
                    wr25=(round(100 * c['eh_won'] / c['awarded']) if c.get('awarded') and c.get('bids25') and not c.get('bids26') else None),
                    wr26=None) for c in B['clients']]
    traj = {y: {'bids': v['bids'], 'with_client': v['bids'], 'pipeline_value': v.get('pipeline'), 'awarded': v['awarded'], 'eh_won': v['eh_won'],
                'win_rate': v['win_rate'], 'avg_bidders': v.get('avg_bidders')} for y, v in B['trajectory'].items()}

    # geography: stakeholder base from the map, tender delivery parsed from title + client
    regions = {rg: {'total': 0, 'competitors': 0, 'clients': 0, 'opps': 0, 'opp_value': 0, 'eh_won': 0, 'awarded': 0} for rg in REGIONS}
    gcc = {'total': 0, 'competitors': 0}
    for n in nodes:
        rg = n.get('rg')
        if rg in regions:
            regions[rg]['total'] += 1
            if n.get('cat') in COMP_CATS: regions[rg]['competitors'] += 1
            if n.get('cat') in CLIENT_CATS: regions[rg]['clients'] += 1
        elif rg == 'GCC / International':
            gcc['total'] += 1
            if n.get('cat') in COMP_CATS: gcc['competitors'] += 1
    national = {'opps': 0, 'opp_value': 0, 'eh_won': 0, 'awarded': 0}
    for r in bl:
        rg = region_of((r.get('title') or '') + ' ' + (r.get('client') or ''))
        g = regions[rg] if rg else national
        g['opps'] += 1; g['opp_value'] += r.get('value') or 0
        if str(r.get('outcome')).lower() in ('won', 'lost', 'not awarded'): g['awarded'] += 1
        if str(r.get('outcome')).lower() == 'won': g['eh_won'] += 1

    # licence contest counts (competitors holding each EH licence code)
    LIC = json.loads(re.search(r'<script id="LIC" type="application/json">(.*?)</script>', mh, re.S).group(1))
    eh_codes = []
    for e in D.get('eh', []):
        eh_codes += [c.strip() for c in (e.get('act') or '').split(',') if c.strip()]
    holders = {}
    for n in nodes:
        if n.get('cat') in COMP_CATS:
            for c in (n.get('act') or '').split(','):
                c = c.strip()
                if c: holders[c] = holders.get(c, 0) + 1
    def lbl(c): return LIC.get(c) or LIC.get(re.sub(r'\(.*\)$', '', c)) or c
    eh_portfolio = sorted([[c, holders.get(c, 0), lbl(c)] for c in dict.fromkeys(eh_codes)], key=lambda x: x[1])
    most_crowded = sorted([[c, v, lbl(c)] for c, v in holders.items()], key=lambda x: -x[1])[:10]
    white_space = sorted([[c, v, lbl(c)] for c, v in holders.items() if v <= 1], key=lambda x: x[0])[:12]

    NEW = {'kpi': {'total_bids': kpi['total'], 'total_pipeline': kpi['pipeline'], 'awarded': kpi['awarded'], 'eh_won': kpi['eh_won'],
                   'win_rate': kpi['win_rate'], 'competitors_faced': sum(1 for c in competitors if c['in_map']),
                   'max_bidders': kpi['max_bidders'], 'biggest_client': clients[0]['name'] if clients else None},
           'competitors': competitors, 'clients': clients, 'trajectory': traj,
           'licenses': {'eh_portfolio': eh_portfolio, 'most_crowded': most_crowded, 'white_space': white_space},
           'geo': {'regions': regions, 'national': national, 'gcc': gcc},
           'watchlist': [{'sev': w['sev'], 'kind': w['kind'], 'text': w['text']} for w in B.get('watchlist', [])],
           'refreshed': dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).isoformat(timespec='minutes'),
           'source': 'EH_Bid_Analysis_CURRENT.html (' + str(re.search(r'window\.BUILT_ISO="([^"]+)"', bh).group(1) if re.search(r'window\.BUILT_ISO="([^"]+)"', bh) else '') + ')'}
    payload = json.dumps(NEW, ensure_ascii=False).replace('</', '<\\/')
    out = mh[:mban.start(2)] + payload + mh[mban.end(2):]
    open(a.map, 'w', encoding='utf-8').write(out)
    print(f"BANALYTICS refreshed: {OLD['kpi']['total_bids']} → {NEW['kpi']['total_bids']} tenders, "
          f"{OLD['kpi']['competitors_faced']} → {NEW['kpi']['competitors_faced']} mapped competitors faced, "
          f"national {national['opps']} / regional {sum(g['opps'] for g in regions.values())}")

if __name__ == '__main__':
    main()
