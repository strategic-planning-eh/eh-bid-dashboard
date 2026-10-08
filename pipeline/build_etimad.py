"""build_etimad.py — Etimad tenders for the Government Tenders tab.

Reads the raw cards from the private Google Sheet EH_Etimad_data (downloaded by fetch_from_sheets.py as
etimad_data.xlsx; nothing from Etimad is ever committed to the repo), tags each tender against
eh_service_taxonomy.json, applies your decisions and approved agency links from the same sheet, matches
agencies to the published stakeholder map and reference numbers to the bid tracker (canonical), and writes
one JSON for build_etimad_page.py.

CI:    python pipeline/build_etimad.py --sheet pipeline/etimad_data.xlsx --map site/EH_Stakeholder_Map_CURRENT.html \
           --tracker pipeline/bids2025.xlsx pipeline/bids2026.xlsx --bidraw pipeline/bidraw2.json --out pipeline/etimad_tenders.json
Local: python build_etimad.py --raw etimad/raw --map hub/EH_Stakeholder_Map_CURRENT.html --out etimad_tenders.json
"""
import argparse, csv, datetime, glob, json, os, re, sys, unicodedata
from datetime import date

# ---------------------------------------------------------------- normalisation
_DIAC = re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭ]')
_ZW = re.compile(r'[​-‏‪-‮⁦-⁩﻿]')
_MAP = str.maketrans({'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ی': 'ي', 'ک': 'ك', 'ـ': ''})

def norm(s):
    if s is None:
        return ''
    s = unicodedata.normalize('NFKC', str(s))
    s = _ZW.sub('', s)
    s = _DIAC.sub('', s)
    s = s.translate(_MAP)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s

_PREFIX = r'(?:وال|بال|فال|لل|ال|و|ب|ل|ف)?'
_SUFFIX = r'(?:ه|ات|يه)?'

def term_rx(term):
    words = norm(term).split(' ')
    parts = []
    for i, w in enumerate(words):
        core = w[2:] if w.startswith('ال') and len(w) > 4 else w
        tail = _SUFFIX if i == len(words) - 1 else ''
        parts.append(_PREFIX + re.escape(core) + tail)
    return re.compile(r'(?<![\w])' + r'\s+'.join(parts) + r'(?![\w])')

def expand_syn(terms):
    out = []
    for t in terms:
        out.append(t)
        if 'نفايات' in t:
            out.append(t.replace('نفايات', 'مخلفات'))
        elif 'مخلفات' in t:
            out.append(t.replace('مخلفات', 'نفايات'))
    return out

# ---------------------------------------------------------------- raw snapshots
FIELDS = ['ref', 'pub', 'type', 'days', 'sub', 'enq', 'open', 'fee', 'activity', 'agency_raw', 'title', 'queries']

def read_raw(path):
    """Accepts the JSON written by the capture (list of dicts) or the ‖-separated text dump."""
    if path.endswith('.json'):
        return json.load(open(path, encoding='utf-8'))['cards']
    rows = []
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split('‖')]
        if len(parts) != len(FIELDS):
            raise ValueError(f'{path}: expected {len(FIELDS)} fields, got {len(parts)}: {line[:80]}')
        r = dict(zip(FIELDS, parts))
        r['queries'] = [q for q in r['queries'].split('|') if q]
        rows.append(r)
    return rows

def is_block(r):
    return bool(re.fullmatch(r'2000\d{6}', r['ref'])) and bool(re.match(r'\d{8}', r['agency_raw']))

def split_agency(a):
    a = a.strip()
    if is_block_agency(a):
        a = re.sub(r'^\d{8}', '', a)
    head, _, dept = a.partition(' - ')
    return head.strip(), dept.strip()

def is_block_agency(a):
    return bool(re.match(r'\d{8}', a))

def is_open(r):
    return 'إنتهى' not in r['days']

def fee_value(f):
    f = (f or '').strip()
    if f in ('مجانا', 'مجاناً'):
        return 0.0
    try:
        return float(f.replace(',', ''))
    except ValueError:
        return None

# ---------------------------------------------------------------- tagging
class Tagger:
    def __init__(self, tax):
        self.tax = tax
        self.verbs = [term_rx(v) for v in tax['service_verbs']]
        self.supply_starts = [norm(s) for s in tax['supply_starts']]
        self.supply_escape = [term_rx(v) for v in tax['supply_escape_words']]
        self.goods = [norm(g) for g in tax.get('supply_goods_nouns', [])]
        self.excl = [(t, term_rx(t)) for t in expand_syn(tax['exclusions_ar'])]
        self.lines = []
        for L in tax['lines']:
            self.lines.append(dict(L,
                rx=[(t, term_rx(t)) for t in expand_syn(L.get('include_ar', []))],
                weak=[(t, term_rx(t)) for t in L.get('weak_ar', [])],
                ex=[term_rx(t) for t in L.get('exclude_ar', [])],
                qual=[term_rx(t) for t in L.get('requires_qualifier_ar', [])],
                rx_en=[re.compile(r'\b' + re.escape(t.lower()) + r'\b') for t in L.get('include_en', [])]))
        self.waste_rx = term_rx('نفايات'), term_rx('مخلفات')
        self.reg = [norm(a) for a in tax['regulator_agencies_ar']]

    def has_verb(self, t):
        return any(v.search(t) for v in self.verbs)

    def tag(self, title, activity, agency):
        t = norm(title)
        raw_lower = (title or '').lower()
        hits, why = [], []
        starts = [s for s in self.supply_starts if t.startswith(s)]
        supply = bool(starts) and not any(e.search(t) for e in self.supply_escape)
        if starts and not supply:
            rest = t[len(max(starts, key=len)):].strip().split(' ')
            if rest and any(rest[0] in (g, 'ال' + g) for g in self.goods):
                supply = True
        for L in self.lines:
            m = None
            for term, rx in L['rx']:
                if rx.search(t):
                    m = term; break
            if not m:
                for rx in L['rx_en']:
                    if rx.search(raw_lower):
                        m = rx.pattern.strip('\\b'); break
            weak = False
            if not m:
                for term, rx in L['weak']:
                    if rx.search(t):
                        m, weak = term, True; break
            if not m:
                continue
            if any(e.search(t) for e in L['ex']):
                continue
            if L.get('requires_service_verb') and not self.has_verb(t):
                why.append(f'«{m}» but no service verb → supply'); continue
            if L['qual'] and not any(q.search(t) for q in L['qual']):
                why.append(f'«{m}» without a hazardous qualifier'); continue
            hits.append((L['id'], m, weak))
        for L in self.lines:   # 'محطة معالجة' counts only together with an industrial / waste word
            P = L.get('pair_ar')
            if P and L['id'] not in [h[0] for h in hits] and term_rx(P['term']).search(t) and any(term_rx(w).search(t) for w in P['needs_one_of']):
                hits.append((L['id'], P['term'], False))
        excl = [term for term, rx in self.excl if rx.search(t)]
        rel, rule = 'Not EH', 'no EH term'
        review = []
        if hits and not supply:
            strong = [h for h in hits if not h[2]]
            rel = 'Core' if strong else 'Adjacent'
            rule = '; '.join(f'L{h[0]} «{h[1]}»' for h in hits)
            if excl:
                review.append('Core term together with an exclusion term (' + ', '.join(excl) + ')')
            if re.search(r'(تشغيل وصيانه|نظافه)', t):
                rel = 'Adjacent' if rel == 'Core' and not re.search(r'(خطره|طبيه|الرعايه الصحيه|معديه|سموم)', t) else rel
                review.append('Environmental scope bundled into an O&M / cleaning contract (rule A3)')
            if not strong:
                review.append('Only a weak term matched')
        elif hits and supply:
            rel, rule = 'Not EH', 'supply of goods (title starts with a supply word, no service word)'
        else:
            waste = any(r.search(t) for r in self.waste_rx)
            if supply:
                rel, rule = 'Not EH', 'supply of goods'
            elif excl:
                rel, rule = 'Not EH', 'exclusion: ' + ', '.join(excl)
            elif waste and self.has_verb(t):
                rel, rule = 'Adjacent', 'A1 general / municipal waste removal or transfer'
                review.append('General waste work: confirm whether EH would bid')
            elif norm(agency) in self.reg and norm(activity) in (norm('الخدمات البيئية'), norm('أنشطة التدوير وجمع النفايات ومعالجتها وتصريفها واسترجاع المواد')):
                rel, rule = 'Adjacent', 'A2 regulator tender in an environmental activity'
                review.append('Regulator tender: confirm scope')
            elif why:
                rule = why[0]
            if rel == 'Not EH' and (waste or re.search(r'بيئي', t)) and self.has_verb(t) and not supply:
                review.append('Near miss: waste or environmental wording but ruled out (' + rule + ')')
        if (title or '').rstrip().endswith('...') and rel != 'Not EH':
            review.append('Title is cut short on the result card; full title on the Etimad page')
        lines = sorted({h[0] for h in hits}) if rel != 'Not EH' else []
        self.last_terms = [h[1] for h in hits] if rel != 'Not EH' else []
        return rel, lines, rule, review

# ---------------------------------------------------------------- sectors (Etimad activity → plain sector)
SECTORS = [  # (id, EN, AR, activity keywords — first match wins)
    ('env', 'Environment & waste', 'البيئة والنفايات', ['الخدمات البيئيه', 'النفايات', 'التدوير']),
    ('health', 'Healthcare & medical supplies', 'الصحة والمستلزمات الطبية', ['الطبيه', 'الادويه', 'النقاهه', 'المختبريه']),
    ('it', 'IT & telecoms', 'تقنية المعلومات والاتصالات', ['تقنيه المعلومات', 'الاتصالات', 'الحواسيب']),
    ('om', 'Operations, maintenance & cleaning', 'التشغيل والصيانة والنظافة', ['التشغيل والصيانه', 'صيانه', 'تنجيد', 'تنقيه الهواء']),
    ('build', 'Construction & engineering', 'الإنشاءات والهندسة', ['مقاولات', 'مواد البناء', 'الاستشارات الهندسيه', 'انابيب', 'المعادن المشكله']),
    ('utility', 'Utilities, energy & fuel', 'المرافق والطاقة والوقود', ['الكهرباء', 'البترول', 'محطات الوقود']),
    ('supply', 'Spare parts, tools & vehicles', 'قطع الغيار والأدوات والمركبات', ['قطع الغيار', 'الادوات والالات', 'السيارات والمعدات', 'المواد الكيماويه', 'المواد الكيميائيه']),
    ('security', 'Security & safety', 'الأمن والسلامة', ['الامن و السلامه', 'الامن والسلامه']),
    ('consult', 'Consulting & business services', 'الاستشارات وخدمات الأعمال', ['الاستشاريه', 'الاستشارات', 'الخدمات التجاريه', 'التامين', 'التخليص الجمركي', 'العقارات']),
    ('media', 'Media, events & printing', 'الإعلام والفعاليات والطباعة', ['النشر والطباعه', 'المعارض', 'المناسبات']),
    ('transport', 'Transport & logistics', 'النقل والخدمات اللوجستية', ['النقل', 'الموانئ', 'التاجير']),
    ('goods', 'Furniture, clothing & household goods', 'الأثاث والملابس والسلع المنزلية', ['الاثاث', 'الملابس', 'الملبوسات', 'المنسوجات', 'الكماليات', 'الاواني', 'الخياطه']),
    ('food', 'Food, agriculture & hospitality', 'الغذاء والزراعة والضيافة', ['الغذائيه', 'زراعيه', 'الزراعيه', 'المواشي', 'المطاعم', 'الايواء', 'سياحيه']),
    ('edu', 'Education & training', 'التعليم والتدريب', ['التعليم', 'التدريب']),
]
def sector_of(activity):
    a = norm(activity)
    for sid, en, ar, kws in SECTORS:
        if any(norm(k) in a for k in kws):
            return sid
    return 'other'

# ---------------------------------------------------------------- inputs
def read_sheet(path):
    """The private Google Sheet (downloaded by fetch_from_sheets.py as etimad_data.xlsx).
    Returns raw cards, decisions, agency bridge rows and counter rows."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    def cell(v):
        # Google Sheets turns typed dates into real dates; the export then gives datetimes.
        # Keep the text shapes the rest of the build expects: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'.
        if v is None:
            return ''
        if isinstance(v, datetime.datetime):
            return v.strftime('%Y-%m-%d') if (v.hour, v.minute, v.second) == (0, 0, 0) else v.strftime('%Y-%m-%d %H:%M')
        if isinstance(v, datetime.date):
            return v.strftime('%Y-%m-%d')
        if isinstance(v, float) and v.is_integer():
            return str(int(v))
        return str(v).strip()
    def rows(name):
        if name not in wb.sheetnames:
            return []
        it = wb[name].iter_rows(values_only=True)
        head = [str(h or '').strip() for h in next(it, [])]
        out = []
        for r in it:
            if r and any(v not in (None, '') for v in r):
                out.append({h: cell(v) for h, v in zip(head, r)})
        return out
    cards = []
    for r in rows('raw_cards'):
        if not r.get('ref'):
            continue
        cards.append({'capture': r['capture_date'][:10], 'ref': r['ref'].split('.')[0], 'pub': r['published'][:10],
                      'type': r['tender_type'], 'days': r['days_left_as_shown'], 'sub': r['submission_deadline'],
                      'enq': r['enquiry_deadline'][:10], 'open': r['bid_opening'], 'fee': r['document_fee'],
                      'activity': r['activity'], 'agency_raw': r['agency_as_shown'], 'title': r['title_as_shown'],
                      'queries': [q for q in r.get('found_by_search', '').split('|') if q]})
    return cards, rows('decisions'), rows('agency_bridge'), rows('counts'), rows('market'), rows('analyst_notes')

def read_raw_dir(raw_dir):
    """Local / Stage-1 mode: snapshots on disk (etimad/raw/<date>.json or the ‖ text dump)."""
    cards = []
    for f in sorted(glob.glob(os.path.join(raw_dir, '*.json')) + glob.glob(os.path.join(raw_dir, '*.txt'))):
        snap = os.path.basename(f)[:10]
        for r in read_raw(f):
            cards.append(dict(r, capture=snap))
    return cards

def load_map_html(path):
    """Stakeholder map records from the published map page (<script id="DATA">), with the Arabic
    names recorded as merged-duplicate aliases in each record's notes."""
    h = open(path, encoding='utf-8').read()
    m = re.search(r'<script id="DATA" type="application/json">(.*?)</script>', h, re.S)
    if not m:
        sys.exit('map DATA block not found in ' + path)
    nodes = json.loads(m.group(1))['nodes']
    recs = {}
    for n in nodes:
        cl = n.get('cl') or {}
        rec = {'Name': n['n'], 'Tier': n.get('tier'), 'Category': n.get('cat'), 'Region': n.get('rg'),
               'EH Client': 'Yes' if (n.get('cat') == 'EH Clients' or cl) else 'No',
               'Client Value (SAR)': cl.get('value')}
        keys = {norm(n['n'])}
        for al in re.findall(r'Alias \(merged duplicate\):\s*([^.(]+)', n.get('notes') or ''):
            keys.add(norm(al))
        for k in keys:
            if k and k not in recs:
                recs[k] = rec
    return recs

def bridge_from_rows(rows):
    out = {}
    for r in rows:
        st = (r.get('status') or '').strip().lower()
        if st == 'approved' and r.get('etimad_agency') and r.get('map_name'):
            out[norm(r['etimad_agency'])] = (r['map_name'], 'approved')
    return out

def load_tracker_files(paths, bidraw=None):
    """Bid tracker (canonical). Reference numbers are read from the workbooks; the outcome comes from
    bidraw2.json (written by extract_bids2.py) so it matches the Bid & Tender app exactly."""
    import openpyxl
    status = {}
    if bidraw and os.path.exists(bidraw):
        for b in json.load(open(bidraw, encoding='utf-8'))['bids']:
            if b.get('eh_won') is True:
                st = 'Won'
            elif b.get('eh_won') is False:
                st = 'Lost'
            elif b.get('ehsub'):
                st = 'Bid'
            else:
                st = 'Studied'
            status[(b['year'], b['sn'])] = st
    out = {}
    for p in paths:
        if not os.path.exists(p):
            continue
        yr = 2025 if '2025' in os.path.basename(p) else 2026
        ws = openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0]
        hr, rows = None, list(ws.iter_rows(values_only=True))
        for i, r in enumerate(rows[:10]):
            if str(r[0] or '').strip().startswith('SN'):
                hr = i; break
        if hr is None:
            continue
        head = [str(h or '').replace('\n', ' ') for h in rows[hr]]
        rc = next((i for i, h in enumerate(head) if 'Reference No' in h), None)
        if rc is None:
            continue
        sc = next((i for i, h in enumerate(head) if 'Status of submission' in h), None)   # used only when bidraw2.json is absent
        for r in rows[hr + 1:]:
            ref = str(r[rc] or '').strip().split('.')[0]
            try:
                sn = int(float(r[0]))
            except (TypeError, ValueError):
                continue
            if re.fullmatch(r'\d{6,}', ref):
                fallback = 'Bid' if (sc is not None and str(r[sc] or '').strip().lower().startswith('yes')) else 'Studied'
                out[ref] = {'year': yr, 'sn': sn, 'eh_status': status.get((yr, sn), fallback)}
    return out

def load_tracker_simple(path):
    """Stage-1 helper: the 2026 tracker workbook as uploaded (no bidraw2.json)."""
    return load_tracker_files([path])

# ---------------------------------------------------------------- build
def build(cards, tax, recs, bridge, trk, decisions, counts, captured_dates):
    tg = Tagger(tax)
    pri_kw = [norm(x) for x in tax['priority_agencies_ar']]
    tenders = {}
    for r in sorted(cards, key=lambda c: c['capture']):
        t = tenders.setdefault(r['ref'], {'ref': r['ref'], 'first_seen': r['capture'], 'status_history': [], 'queries': []})
        for k in ('pub', 'type', 'days', 'sub', 'enq', 'open', 'fee', 'activity', 'agency_raw', 'title'):
            if r.get(k) not in (None, ''):
                t[k] = r[k]
        for k in ('pub', 'type', 'days', 'sub', 'enq', 'open', 'fee', 'activity', 'agency_raw', 'title'):
            t.setdefault(k, '')
        t['last_seen'] = r['capture']
        st = 'open' if 'إنتهى' not in r['days'] else 'closed'
        if not t['status_history'] or t['status_history'][-1]['status'] != st:
            t['status_history'].append({'date': r['capture'], 'status': st})
        for q in r['queries']:
            if q not in t['queries']:
                t['queries'].append(q)
    dec = {}
    for d in decisions:
        v = (d.get('decision') or d.get('Decision') or '').strip()
        if v in ('Core', 'Adjacent', 'Not EH'):
            dec[str(d.get('ref') or d.get('Reference')).split('.')[0]] = v
    last_capture = max(captured_dates) if captured_dates else None
    for t in tenders.values():
        agency, dept = split_agency(t['agency_raw'])
        t['agency'], t['department'] = agency, dept
        t['block_2000'] = is_block(t)
        rel, lines, rule, review = tg.tag(t['title'], t['activity'], agency)
        t['matched_terms'] = getattr(tg, 'last_terms', [])
        t['rules_said'] = rel
        if t['ref'] in dec:
            rel, review = dec[t['ref']], []
            t['decided_by'] = 'you'
            if rel == 'Not EH':
                lines = []
        t.update(relevance=rel, service_lines=lines, matched_rule=rule, review=review)
        rec, how = match_agency(agency, recs, bridge)
        t['map_match'], t['map'] = how, rec
        tier = (rec or {}).get('Tier'); cat = (rec or {}).get('Category') or ''
        why = []
        if tier in ('Tier 1', 'GOV'):
            why.append('tier')
        if (rec or {}).get('EH Client') == 'Yes':
            why.append('client')
        if cat == 'Regulators & Compliance Bodies' or norm(agency) in tg.reg:
            why.append('regulator')
        if any(k in norm(agency) for k in pri_kw):
            why.append('giga')
        t['priority'], t['priority_why'] = bool(why), why
        tr = trk.get(t['ref'])
        t['eh_status'] = tr['eh_status'] if tr else 'Not studied'
        t['tracker'] = tr
        t['fee_sar'] = fee_value(t['fee'])
        t['is_open'] = 'إنتهى' not in t['days'] and (t['last_seen'] == last_capture)
        t['region'] = None   # only on the tender's own Etimad page; not captured yet
        t['sector'] = sector_of(t['activity'])
    return {'built': date.today().isoformat(), 'last_capture': last_capture, 'captures': sorted(set(captured_dates)),
            'count': len(tenders), 'counts': counts,
            'service_lines': [{'id': L['id'], 'en': L['en'], 'ar': L['ar']} for L in tax['lines']],
            'tenders': sorted(tenders.values(), key=lambda x: x['sub'])}

AGENCY_GROUPS = [  # first match wins
    ('health', ['مستشفي', 'مستشفيات', 'الصحي', 'الصحيه', 'تجمع', 'القلب', 'للعلوم الصحيه']),
    ('water', ['مياه', 'تحليه']),
    ('defence', ['القوات', 'حرس', 'الامن', 'المباحث', 'الدفاع', 'السجون', 'المخدرات', 'العسكري', 'الحرس', 'الصواريخ', 'امن الدوله', 'هيئه الاركان', 'المجاهدين']),
    ('local', ['امانه', 'بلديه', 'اماره', 'الشوون الفنيه']),
    ('edu', ['جامعه', 'كليه', 'التعليم', 'التدريب']),
    ('ministry', ['وزاره']),
]
AGENCY_GROUP_NAMES = {'health': ('Health (hospitals, clusters)', 'الصحة (مستشفيات وتجمعات)'), 'water': ('Water', 'المياه'),
    'defence': ('Defence & security', 'الدفاع والأمن'), 'local': ('Municipalities & regional offices', 'البلديات والجهات المناطقية'),
    'edu': ('Universities & training', 'الجامعات والتدريب'), 'ministry': ('Ministries (central)', 'الوزارات (مركزيًا)'), 'other': ('Other bodies', 'جهات أخرى')}
def agency_group(name):
    a = norm(name)
    for g, kws in AGENCY_GROUPS:
        if any(norm(k) in a for k in kws):
            return g
    return 'other'

def build_market(rows):
    """All Etimad tenders (full-market capture): one block per capture window, with activities grouped into sectors."""
    caps = {}
    for r in rows:
        try:
            k = (r['capture_date'][:10], r['window_from'][:10], r['window_to'][:10])
            caps.setdefault(k, []).append({'dim': r['dimension'], 'key': r['key'], 'n': int(float(r['tenders'])),
                                           'open': int(float(r.get('open_at_capture') or 0)), 'fees': float(r.get('document_fees_sar') or 0)})
        except (KeyError, ValueError):
            continue
    out = []
    for (cap, wf, wt), rr in sorted(caps.items()):
        sec = {}
        for r in rr:
            if r['dim'] == 'activity':
                sid = sector_of(r['key'])
                o = sec.setdefault(sid, {'n': 0, 'open': 0, 'fees': 0.0, 'acts': []})
                o['n'] += r['n']; o['open'] += r['open']; o['fees'] += r['fees']; o['acts'].append([r['key'], r['n']])
        grp = {}
        for r in rr:
            if r['dim'] == 'agency':
                g = agency_group(r['key'])
                o = grp.setdefault(g, {'n': 0, 'fees': 0.0}); o['n'] += r['n']; o['fees'] += r['fees']
        out.append({'capture': cap, 'from': wf, 'to': wt, 'rows': rr, 'sectors': sec, 'agency_groups': grp})
    return {'windows': out, 'group_names': {k: {'en': v[0], 'ar': v[1]} for k, v in AGENCY_GROUP_NAMES.items()}, 'sector_names': {sid: {'en': en, 'ar': ar} for sid, en, ar, _ in SECTORS} | {'other': {'en': 'Other', 'ar': 'أخرى'}}}

def match_agency(agency, recs, bridge):
    a = norm(agency)
    if a in recs:
        return recs[a], 'name'
    if a in bridge:
        r = recs.get(norm(bridge[a][0]))
        if r:
            return r, 'bridge'
    return None, 'unmatched'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sheet', help='etimad_data.xlsx downloaded from the private Google Sheet (CI mode)')
    ap.add_argument('--raw', help='folder of raw snapshots (local mode)')
    ap.add_argument('--taxonomy', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eh_service_taxonomy.json'))
    ap.add_argument('--map', required=True, help='published stakeholder map HTML')
    ap.add_argument('--tracker', nargs='*', default=[], help='bid tracker workbooks (bids2025.xlsx bids2026.xlsx)')
    ap.add_argument('--bidraw', help='bidraw2.json from extract_bids2.py')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    tax = json.load(open(a.taxonomy, encoding='utf-8'))
    if a.sheet and os.path.exists(a.sheet):
        cards, decisions, bridge_rows, counts, market, note_rows = read_sheet(a.sheet)
    elif a.raw:
        cards, decisions, bridge_rows, counts, market, note_rows = read_raw_dir(a.raw), [], [], [], [], []
    else:
        cards, decisions, bridge_rows, counts, market, note_rows = [], [], [], [], [], []
    recs = load_map_html(a.map)
    out = build(cards, tax, recs, bridge_from_rows(bridge_rows), load_tracker_files(a.tracker, a.bidraw),
                decisions, counts, [c['capture'] for c in cards])
    out['market'] = build_market(market)
    # Analyst view: umbrella (committed, no Etimad data) + market windows + tenders + map + notes (private sheet)
    from etimad_analyst import analyst
    out['analyst'] = analyst(market, out['tenders'], a.map, note_rows, bidraw=a.bidraw)
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    rel = sum(1 for t in out['tenders'] if t['relevance'] != 'Not EH')
    print(f"Etimad: {out['count']} tenders ({rel} relevant), last capture {out['last_capture']} → {a.out}")
    an = out.get('analyst') or {}
    print(f"Analyst view: {len(an.get('windows') or [])} market windows, {len(an.get('notes') or [])} notes ({an.get('notes_month')}), reviewed {an.get('reviewed')}")

if __name__ == '__main__':
    main()
