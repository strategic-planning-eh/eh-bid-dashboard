#!/usr/bin/env python3
"""
build_changelog.py — weekly "What's New" generator for the EH Strategic Intelligence Hub.

  Data changes are DIFFED mechanically (previous snapshot vs current build).
  Fixes are NEVER inferred: they come only from CHANGES.md (human-written).

Inputs
  --hub DIR            folder holding the 8 published HTML files (site/ or hub/)
  --prev DIR           previous snapshot folder (stakeholders.json, bids.json, clients.json)
  --changes FILE       CHANGES.md   (app | severity | view? | EN | AR, one fix per line under a ## week heading;
                       app = stake | bids | tenders | clients | news | hub)
  --out FILE           changelog.json to write (existing weeks are kept, 12-week retention)
  --snapshot-out DIR   where to write the new snapshot (uploaded as a workflow artefact)
  --init               allow the very first run with no previous snapshot (writes snapshot, no diff)

Exit codes: 0 ok · 2 previous snapshot missing (build must fail) · 3 CHANGES.md malformed
"""
import argparse, json, re, sys, os, subprocess, datetime as dt, unicodedata

# ------------------------------------------------------------------ extraction from the built apps
def _grab(html, sid):
    m = re.search(r'<script id="%s" type="application/json">(.*?)</script>' % sid, html, re.S)
    return json.loads(m.group(1)) if m else None

def _norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200d\ufeff]', '', s)
    s = re.sub(r'[إأآا]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي')
    return re.sub(r'\s+', ' ', s).strip().casefold()

def extract(hub):
    out = {}
    p = os.path.join(hub, 'EH_Stakeholder_Map_CURRENT.html')
    d = _grab(open(p, encoding='utf-8').read(), 'DATA') if os.path.exists(p) else None
    if d:
        out['stakeholders'] = {n['n']: {'typ': n.get('typ'), 'cat': n.get('cat'), 'tier': n.get('tier'), 'cf': n.get('cf'),
                                        'bid': bool(n.get('bid')), 'bc': n.get('bc') or 0, 'drv': n.get('drv')} for n in d['nodes']}
    p = os.path.join(hub, 'EH_Bid_Analysis_CURRENT.html')
    b = _grab(open(p, encoding='utf-8').read(), 'BA') if os.path.exists(p) else None
    if b:
        rows = b['both'].get('bidlist', [])
        out['bids'] = {f"{r.get('year')}/{r.get('sn')}": {'title': r.get('title'), 'client': r.get('client'), 'outcome': r.get('outcome'),
                                                          'winner': r.get('winner'), 'value': r.get('value'), 'status': r.get('status')} for r in rows}
        out['clients'] = sorted({r.get('client') for r in rows if r.get('client')})
    p = os.path.join(hub, 'EH_Client_Bubble_Map_CURRENT.html')
    if os.path.exists(p):
        m = re.search(r'const DATA = (\[\{.*?\}\]);', open(p, encoding='utf-8').read(), re.S)
        if m:
            try:
                cl = json.loads(m.group(1))
                out['eh_clients'] = sorted({c.get('name') or c.get('n') or c.get('company') for c in cl if isinstance(c, dict)} - {None})
            except Exception:
                pass
    return out

# ------------------------------------------------------------------ news wing: each report's own version/date → Sources tab
# (file, name EN, name AR, version pattern, note prefix EN/AR, date pattern (dd/mm/yyyy or yyyy-mm-dd), fixed note EN/AR)
NEWS = [('vision2030_dashboard.html', 'Vision 2030 Dashboard', 'لوحة رؤية 2030', None, None,
         r'Last reviewed <strong>(\d{2}/\d{2}/\d{4})', ('date of the last review', 'تاريخ آخر مراجعة')),
        ('saudi_fiscal_monitor_2026.html', 'Saudi Government Finances 2026', 'مالية الحكومة السعودية 2026', r'<title>[^<]*?\bversion (\d+)', ('version ', 'الإصدار '),
         r'figures as of (\d{2}/\d{2}/\d{4})', None),
        ('eh_news_intelligence.html', 'Corporate & Government News', 'أخبار الشركات والحكومة', r'<title>[^<]*?·\s*([^<·]+Update)</title>', ('edition: ', 'الإصدار: '), None, None),
        ('pif_intelligence_hub.html', 'PIF Intelligence Hub', 'مركز استخبارات صندوق الاستثمارات', r'<title>PIF annual reports (\d{4}\u2013\d{4})[^<]*</title>',
         ('covers annual reports ', 'يغطي التقارير السنوية '), None, None),   # coverage years; PIF publishes annually
        ('pif_strategy_2026_2030.html', 'PIF Strategy 2026–2030', 'استراتيجية صندوق الاستثمارات العامة 2026–2030', None, None, None,
         ("PIF's strategy document for 2026–2030", 'وثيقة استراتيجية الصندوق للأعوام 2026–2030')),
        ('environment_fund_2025.html', 'Environment Fund 2025 Annual Report', 'التقرير السنوي لصندوق البيئة 2025', None, None,
         r'"extracted":\s*"(\d{4}-\d{2}-\d{2})"', ('date the report was read', 'تاريخ قراءة التقرير')),
        ('etimad_tenders.html', 'Government Tenders (Etimad)', 'المنافسات الحكومية (اعتماد)', None, None,
         r'"last_capture":\s*"(\d{4}-\d{2}-\d{2})"', ('Etimad is checked every Sunday', 'يُفحص اعتماد كل أحد'))]

AR_MONTHS = dict(zip(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                     ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']))

def _dmy_to_iso(s):
    s = s.strip(); m = re.match(r'(\d{2})/(\d{2})/(\d{4})$', s)
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else (s if re.match(r'\d{4}-\d{2}-\d{2}$', s) else None)

def news_sources(hub):
    """One line per report page, with the version and date the page itself carries. Nothing says "not detected":
    a page without a marker simply shows its name (audit shell-10)."""
    out = []
    for fn, name, name_ar, vpat, pre, dpat, fixed in NEWS:
        p = os.path.join(hub, fn)
        if not os.path.exists(p): continue
        h = open(p, encoding='utf-8').read()
        mv = re.search(vpat, h) if vpat else None
        md = re.search(dpat, h) if dpat else None
        note, note_ar = fixed or ((pre[0] + mv.group(1).strip(), pre[1] + mv.group(1).strip()) if mv else (None, None))
        me = re.match(r'(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) Update$', mv.group(1).strip() if mv else '')
        if me:   # "26 August Update" -> "26 August update" / "تحديث 26 أغسطس"
            note, note_ar = pre[0] + me.group(1) + ' ' + me.group(2) + ' update', pre[1] + 'تحديث ' + me.group(1) + ' ' + AR_MONTHS[me.group(2)]
        out.append({'name': name, 'name_ar': name_ar, 'refreshed': _dmy_to_iso(md.group(1)) if md else None, 'note': note, 'note_ar': note_ar})
    gp = os.path.join(hub, 'gov_news.json')   # Regulatory news: the weekly feed carries its own collection time
    if os.path.exists(gp):
        try: g = json.load(open(gp, encoding='utf-8')).get('generated') or None
        except Exception: g = None
        out.append({'name': 'Regulatory news', 'name_ar': 'الأخبار التنظيمية', 'refreshed': g,
                    'note': 'collected every Sunday morning' if g else 'not collected yet', 'note_ar': 'تُجمع كل صباح أحد' if g else 'لم تُجمع بعد'})
    return out

def workbook_source(now):
    """The stakeholder workbook changes only when someone updates it. Its date is the last commit of the Stakeholder Map
    file when the checkout has history; a shallow checkout (the hourly workflow) cannot know it, so no time is invented."""
    src = {'name': 'EH stakeholder workbook', 'name_ar': 'مصنّف أصحاب المصلحة لآفاق البيئة', 'refreshed': None,
           'note': 'updates when the workbook is updated, not hourly', 'note_ar': 'يُحدَّث عند تحديث المصنّف، لا كل ساعة'}
    try:
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
        shallow = subprocess.run(['git', 'rev-parse', '--is-shallow-repository'], cwd=root, capture_output=True, text=True, timeout=20).stdout.strip()
        if shallow == 'false':
            d = subprocess.run(['git', 'log', '-1', '--format=%cI', '--', 'hub/EH_Stakeholder_Map_CURRENT.html'], cwd=root,
                               capture_output=True, text=True, timeout=20).stdout.strip()
            if d: src.update(refreshed=d, note='last change to the Stakeholder Map', note_ar='آخر تغيير على خريطة أصحاب المصلحة')
    except Exception:
        pass
    return src

# ------------------------------------------------------------------ diff
def diff(prev, cur):
    data = {'added': [], 'removed': [], 'merged': [], 'confidence_up': [], 'tier_moves': [],
            'bids': {'new': 0, 'won': [], 'lost': []}, 'clients': {'new': 0, 'lost': 0}, 'totals': {}}
    ps, cs = prev.get('stakeholders', {}), cur.get('stakeholders', {})
    pn, cn = {_norm(k): k for k in ps}, {_norm(k): k for k in cs}
    added = [cn[k] for k in cn if k not in pn]
    removed = [pn[k] for k in pn if k not in cn]
    # a removed name whose normalised form is a prefix/suffix twin of a kept name → alias of a merge
    for r in list(removed):
        rn = _norm(r)
        twin = next((cn[k] for k in cn if k != rn and (rn in k or k in rn) and len(min(rn, k, key=len)) >= 8), None)
        if twin:
            # Display-name rule (approved 06/09/2026): the KEPT row is the English registry name, the ALIAS is the
            # Arabic or short name. The build cannot rename rows; it flags a pair that breaks the rule for the analyst.
            rule_ok = bool(re.search(r'[A-Za-z]', twin)) or not re.search(r'[A-Za-z]', r)
            data['merged'].append({'kept': twin, 'alias': r, **({} if rule_ok else {'check': 'kept name is not the English registry name — rename in the workbook'})}); removed.remove(r)
            data['removed'].append({'n': r, 'alias': twin, 'reason': 'merged'})
    data['added'] = [{'n': n, 'typ': cs[n].get('typ'), 'cat': cs[n].get('cat')} for n in sorted(added)]
    data['removed'] += [{'n': n} for n in sorted(removed)]
    rank = {'Low': 0, 'Medium': 1, 'High': 2}
    for k, n in cn.items():
        if k in pn:
            a, b = ps[pn[k]], cs[n]
            if a.get('cf') != b.get('cf') and rank.get(b.get('cf'), -1) > rank.get(a.get('cf'), -1):
                data['confidence_up'].append({'n': n, 'from': a.get('cf') or '—', 'to': b.get('cf'), 'basis': 'research rubric'})
            if a.get('tier') != b.get('tier') and b.get('tier'):
                data['tier_moves'].append({'n': n, 'from': a.get('tier') or '—', 'to': b.get('tier'), 'driver': b.get('drv') or ''})
    pb, cb = prev.get('bids', {}), cur.get('bids', {})
    data['bids']['new'] = len([k for k in cb if k not in pb])
    for k, r in cb.items():
        o = (pb.get(k) or {}).get('outcome')
        if r.get('outcome') != o:
            if str(r.get('outcome')).lower() == 'won':
                data['bids']['won'].append({'title': r.get('title'), 'client': r.get('client'), 'value': r.get('value')})
            elif str(r.get('outcome')).lower() in ('lost', 'not awarded'):
                data['bids']['lost'].append({'title': r.get('title'), 'client': r.get('client'), 'winner': r.get('winner')})
    pc, cc = set(prev.get('clients', [])), set(cur.get('clients', []))
    data['clients'] = {'new': len(cc - pc), 'lost': len(pc - cc)}
    data['totals'] = {'orgs': len(cs), 'tenders': len(cb), 'clients': len(cur.get('eh_clients', [])) or None}
    return data

# ------------------------------------------------------------------ CHANGES.md
LINE = re.compile(r'^\s*(?P<app>stake|bids|tenders|clients|news|hub)\s*\|\s*(?P<sev>major|minor)\s*\|\s*(?:(?P<view>[^|]*?)\s*\|\s*)?(?P<en>[^|]+?)\s*\|\s*(?P<ar>[^|]+?)\s*$')

def parse_changes(path, week):
    """Return fixes for `week` (## 2026-W36 heading). Malformed line → exit 3."""
    fixes, cur, bad = [], None, []
    for i, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.rstrip('\n')
        if not line.strip() or line.lstrip().startswith(('#', '<!--', '|--', '| app')) and not line.lstrip().startswith('## '):
            if line.lstrip().startswith('## '):
                cur = line.strip()[3:].strip()
            continue
        if line.lstrip().startswith('## '):
            cur = line.strip()[3:].strip(); continue
        if cur != week:
            continue
        m = LINE.match(line.strip().strip('|'))
        if not m:
            bad.append(f'line {i}: {line[:90]}'); continue
        fixes.append({'app': m['app'], 'severity': m['sev'], 'view': (m['view'] or '').strip() or None,
                      'en': m['en'].strip(), 'ar': m['ar'].strip()})
    if bad:
        print('CHANGES.md malformed (app | severity | [view |] EN | AR; app = stake|bids|tenders|clients|news|hub):\n  ' + '\n  '.join(bad), file=sys.stderr); sys.exit(3)
    return fixes

# ------------------------------------------------------------------ main
def iso_week(d):
    """Sunday–Saturday week (Saudi working week). Label = ISO week of the Monday inside it, so Mon–Sat dates keep their
    old label and a Sunday heads the week that follows it."""
    sun = d - dt.timedelta(days=(d.weekday() + 1) % 7); mon = sun + dt.timedelta(days=1)
    y, w, _ = mon.isocalendar()
    return f'{y}-W{w:02d}', sun.isoformat(), (sun + dt.timedelta(days=6)).isoformat()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hub', required=True); ap.add_argument('--prev', required=True); ap.add_argument('--changes', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--snapshot-out', required=True)
    ap.add_argument('--init', action='store_true'); ap.add_argument('--sources', default=None, help='JSON list of {name,refreshed}')
    ap.add_argument('--now', default=None)
    a = ap.parse_args()
    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone(dt.timedelta(hours=3)))
    week, wfrom, wto = iso_week(now.date())

    cur = extract(a.hub)
    if not cur.get('stakeholders'):
        print('FATAL: could not read the stakeholder dataset from', a.hub, file=sys.stderr); sys.exit(2)
    prev_file = os.path.join(a.prev, 'snapshot.json')
    if not os.path.exists(prev_file):
        if not a.init:
            print('FATAL: previous snapshot missing at', prev_file, '— refusing to publish an empty week. '
                  'Restore the snapshot artefact or run once with --init.', file=sys.stderr); sys.exit(2)
        prev = {}
        print('INIT run: no previous snapshot; data diff will be empty this week only.')
    else:
        prev = json.load(open(prev_file, encoding='utf-8'))

    fixes = parse_changes(a.changes, week)
    data = diff(prev, cur) if prev else {'added': [], 'removed': [], 'merged': [], 'confidence_up': [], 'tier_moves': [],
                                         'bids': {'new': 0, 'won': [], 'lost': []}, 'clients': {'new': 0, 'lost': 0},
                                         'totals': {'orgs': len(cur['stakeholders']), 'tenders': len(cur.get('bids', {})), 'clients': len(cur.get('eh_clients', [])) or None}}
    sources = json.loads(a.sources) if a.sources else [
        workbook_source(now),
        {'name': 'Bid tracker (Google Sheets 2025 / 2026)', 'name_ar': 'جدول تتبع العطاءات (Google Sheets 2025 / 2026)', 'refreshed': now.isoformat(timespec='minutes'),
         'note': 'read every hour', 'note_ar': 'يُقرأ كل ساعة'},
        {'name': 'MWAN licence register', 'name_ar': 'سجل تراخيص المركز الوطني لإدارة النفايات', 'refreshed': None,
         'note': 'refresh date recorded in the workbook', 'note_ar': 'تاريخ التحديث مسجَّل في المصنّف'}]
    sources += news_sources(a.hub)
    entry = {'week': week, 'from': wfrom, 'to': wto, 'built': now.isoformat(timespec='minutes'),
             'fixes': fixes, 'data': data, 'sources': sources}

    log = {'weeks': []}
    if os.path.exists(a.out):
        try: log = json.load(open(a.out, encoding='utf-8'))
        except Exception: log = {'weeks': []}
    weeks = [w for w in log.get('weeks', []) if w.get('week') != week]
    # same ISO week rebuilt (hourly workflow): merge data diffs cumulatively, replace fixes with the current CHANGES.md
    old = next((w for w in log.get('weeks', []) if w.get('week') == week), None)
    if old and prev:
        od = old.get('data', {})
        for k in ('added', 'removed', 'merged', 'confidence_up', 'tier_moves'):
            seen = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in data[k]}
            data[k] = data[k] + [x for x in od.get(k, []) if json.dumps(x, sort_keys=True, ensure_ascii=False) not in seen]
        for k in ('won', 'lost'):
            data['bids'][k] += [x for x in od.get('bids', {}).get(k, []) if x not in data['bids'][k]]
        data['bids']['new'] += od.get('bids', {}).get('new', 0)
        data['clients']['new'] += od.get('clients', {}).get('new', 0); data['clients']['lost'] += od.get('clients', {}).get('lost', 0)
    weeks.insert(0, entry)
    weeks.sort(key=lambda w: w['week'], reverse=True)
    log = {'weeks': weeks[:12], 'retention_weeks': 12, 'confidential': True}
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    json.dump(log, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(a.snapshot_out, exist_ok=True)
    json.dump(cur, open(os.path.join(a.snapshot_out, 'snapshot.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'changelog.json written: week {week}, {len(fixes)} fixes, +{len(data["added"])} / -{len(data["removed"])} orgs, '
          f'{len(data["merged"])} merges, {len(data["confidence_up"])} confidence ups, {len(data["tier_moves"])} tier moves')

if __name__ == '__main__':
    main()
