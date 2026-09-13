"""twins.py — finds map companies that are probably the same organisation recorded twice (English/Arabic twins, spelling
variants, "Turbine"/"Turbines"). Used by sync_bids_to_apps.py (report) and make_twin_sheet.py (review workbook).

Three signals, each pair gets the strongest one:
  • same-script name similarity — distinctive-token cores (domain words removed) with difflib ratio ≥ 0.86, or ≥ 3 shared
    distinctive tokens
  • cross-script skeleton — Arabic and Latin names reduced to consonant skeletons (الدهيمان → dhmn, Al-Duhaiman → dhmn);
    a pair matches on ≥ 2 equal token skeletons, or 1 equal skeleton of ≥ 4 consonants
  • fingerprint — identical licence-code set (act) AND same city, for two competitors
Pairs must be in the same family (competitor-type categories together, client-type together) unless the skeleton match
is strong (≥ 2 tokens). Nothing here edits data; it only proposes.
"""
import re, unicodedata
from difflib import SequenceMatcher

COMP = {'Active Competitors', 'Direct Competitors', 'Indirect / Adjacent Competitors', 'Potential Collaborators', 'Suppliers / Subcontractors', 'EH Partners'}
CLIENT = {'EH Clients', 'Clients / Potential Clients', 'Government Clients & Institutions'}
STOP = set('environmental environment consulting consultation consultant consultants consultancy services service solutions group international arabia arabian saudi al one person co company ltd llc est establishment office for the and of general trading contracting engineering'.split()) | \
       set('البيئية البيئي البيئة بيئية للبيئة الاستشارات استشارات الخدمات خدمات المقاولات مقاولات الهندسية هندسية المهنية مهنية التجارية التجاره الدولية العربية السعودية شركه شركة مؤسسة مكتب للاستشارات للخدمات للمقاولات للتجارة المحدودة ذات مسؤولية محدودة الشخص الواحد شخص واحد'.split())
AR = {'ب':'b','ت':'t','ث':'t','ج':'j','ح':'h','خ':'k','د':'d','ذ':'d','ر':'r','ز':'z','س':'s','ش':'s','ص':'s','ض':'d','ط':'t','ظ':'z','ع':'','غ':'g','ف':'f','ق':'k','ك':'k','ل':'l','م':'m','ن':'n','ه':'h','ة':'','و':'','ي':'','ى':'','ا':'','أ':'','إ':'','آ':'','ء':'','ئ':'','ؤ':''}

def is_ar(s): return bool(re.search(r'[\u0600-\u06FF]', s or ''))

def norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200d\ufeff\u064b-\u0652]', '', s)
    s = re.sub(r'[إأآا]', 'ا', s).replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    s = re.sub(r"[’'ʼ`]", '', s)                        # Ma’mar → Mamar
    s = re.sub(r'\(.*?\)', ' ', s)                      # drop bracketed acronyms / "(One-Person Co.)"
    s = s.casefold().replace('-', ' ').replace('&', ' ')
    s = re.sub(r'\bal ', 'al', s)                        # al-harbi / al harbi → alharbi
    return re.sub(r'[^\w\u0600-\u06FF]+', ' ', s).strip()

def core(s):
    return tuple(t for t in norm(s).split() if len(t) > 1 and t not in STOP)

def skel_token(t):
    if is_ar(t):
        t = re.sub(r'^(ال|لل|وال|بال)', '', t)
        return ''.join(AR.get(ch, '') for ch in t)
    t = re.sub(r'^al', '', t)
    for a, b in (('kh','k'),('sh','s'),('th','t'),('dh','d'),('gh','g'),('ph','f'),('ck','k'),('q','k'),('c','k'),('x','ks'),('v','f'),('p','b')): t = t.replace(a, b)
    t = re.sub(r'(.)\1', r'\1', t)                       # double letters
    return re.sub(r'[aeiouyw]', '', t)

def skeleton(s): return [k for k in (skel_token(t) for t in core(s)) if len(k) >= 2]

def family(cat): return 'comp' if cat in COMP else 'client' if cat in CLIENT else 'other'

def compare(a, b, freq=None):
    """Return (score, reason) for two node dicts, or None. freq: skeleton-token frequency over the whole map (rarity)."""
    freq = freq or {}
    na, nb = a['n'], b['n']
    if norm(na) == norm(nb): return (1.0, 'identical name after normalisation')
    ca, cb = core(na), core(nb)
    same_fam = family(a.get('cat')) == family(b.get('cat'))
    both_bid = bool(a.get('bid')) and bool(b.get('bid'))
    if is_ar(na) == is_ar(nb):                           # same script
        if ca and cb:
            sa, sb = ' '.join(ca), ' '.join(cb)
            r = SequenceMatcher(None, sa, sb).ratio()
            shared = len(set(ca) & set(cb))
            single = min(len(ca), len(cb)) == 1
            if r >= 0.86 and same_fam and not single: return (r, f'names {r:.0%} similar ("{sa}" / "{sb}")')
            w = min(ca, cb, key=len)[0]
            if r >= 0.86 and single and (len(w) >= 6 or (len(w) >= 5 and freq.get('w:' + w, 0) <= 3)) and (both_bid or (a.get('city') and a.get('city') == b.get('city'))):
                return (0.7, f'one distinctive word in common ("{w}") + same city or both bid')
            rare_shared = [t for t in set(ca) & set(cb) if freq.get('w:' + t, 0) <= 10]
            if len(rare_shared) >= 3 and same_fam: return (0.8, f'{len(rare_shared)} distinctive words shared ({", ".join(sorted(rare_shared)[:4])})')
            if len(rare_shared) >= 2 and same_fam and both_bid: return (0.7, f'{len(rare_shared)} distinctive words shared ({", ".join(sorted(rare_shared))}), both flagged as bidders')
    else:                                                # Arabic vs Latin: consonant skeletons
        ka, kb = skeleton(na), skeleton(nb)
        elig = lambda ks: [k for k in ks if len(k) >= 3 and freq.get(k, 0) <= 12]
        ea, eb = elig(ka), elig(kb)
        hits = [k for k in ea if k in eb]                 # rare tokens in common
        all_hits = [k for k in ka if k in kb and len(k) >= 3]   # incl. common ones (الانجاز, صالح …) — count them once a rare one anchors the pair
        short = min(len(ea), len(eb)) or 1
        cover = len(hits) / short
        if hits and len(all_hits) >= 2: hits = all_hits
        cover_all = len(all_hits) / (min(len(ka), len(kb)) or 1)
        if not hits and len(all_hits) >= 3 and cover_all >= 0.6 and same_fam and both_bid:
            return (0.75, 'Arabic/English name matches on ' + ', '.join(all_hits))
        if not hits and len(all_hits) >= 2 and cover_all >= 0.8 and same_fam and both_bid:
            return (0.8, 'Arabic/English name matches almost word for word (' + ', '.join(all_hits) + ')')
        if (len(hits) >= 2 and cover >= 0.5) or len(hits) >= 3:
            return (0.75 + 0.05 * min(len(hits), 4), 'Arabic/English skeleton match on ' + ', '.join(hits))
        if len(hits) == 1 and len(hits[0]) >= 4 and cover >= 0.5 and same_fam and both_bid:
            return (0.65, f'Arabic/English skeleton match on "{hits[0]}" (both flagged as bidders)')
        if len(ka) == 1 and len(kb) == 1 and ka == kb and len(ka[0]) >= 2 and same_fam and both_bid and freq.get(ka[0], 0) <= 6:
            return (0.6, f'single-word names with the same consonant skeleton ("{ka[0]}"), both flagged as bidders')
    acta, actb = a.get('act') or '', b.get('act') or ''
    if same_fam and family(a.get('cat')) == 'comp' and acta.count(',') >= 2 and acta == actb and (a.get('city') or '—') == (b.get('city') or '—') and a.get('city') not in (None, '', '—'):
        if ca and cb and SequenceMatcher(None, ' '.join(ca), ' '.join(cb)).ratio() >= 0.5:
            return (0.6, f'same licence codes and city ({a.get("city")})')
    return None

def find_twins(nodes, focus=None, per_node=3):
    """focus: iterable of node ids to look for twins of (default: all). Returns list of dicts sorted by score,
    at most `per_node` candidates per focus node."""
    focus = set(focus) if focus is not None else {id(n) for n in nodes}
    freq = {}
    for n in nodes:
        for k in set(skeleton(n['n'])): freq[k] = freq.get(k, 0) + 1
        for t in set(core(n['n'])): freq['w:' + t] = freq.get('w:' + t, 0) + 1
    out, seen = [], set()
    for a in nodes:
        if id(a) not in focus: continue
        cands = []
        for b in nodes:
            if a is b: continue
            key = frozenset((id(a), id(b)))
            if key in seen: continue
            r = compare(a, b, freq)
            if r: cands.append({'a': a, 'b': b, 'score': r[0], 'reason': r[1], 'key': key})
        for c in sorted(cands, key=lambda x: -x['score'])[:per_node]:
            seen.add(c['key']); out.append(c)
    return sorted(out, key=lambda x: -x['score'])
