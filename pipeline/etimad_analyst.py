"""etimad_analyst.py — the "Analyst view" at the end of the Government Tenders (Etimad) tab.

Build side   analyst(...)  joins pipeline/vision_umbrella.json (committed, no Etimad data) with the market windows and the
             captured tenders from the private sheet, the published stakeholder map and the analyst notes tab
             ("analyst_notes" in EH_Etimad_data). Called by build_etimad.py; the result goes into etimad_tenders.json,
             which is never committed.
Page side    CSS, HTML and JS strings used by build_etimad_page.py to draw the section.

Rules kept here: the buyer decides the goal (never the title); unmatched buyers stay "Running government"; nothing is
added to the stakeholder map; every figure carries its source and date; where nothing is found the page says so.
"""
import json, os, re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
UMBRELLA = os.path.join(HERE, 'vision_umbrella.json')


def load_umbrella(path=UMBRELLA):
    if not os.path.exists(path):
        return None
    return json.load(open(path, encoding='utf-8'))


def _rules(U):
    return [(r['goal'], re.compile(r['pattern'], re.I)) for r in U['level5_etimad']['buyer_rules'] if r['goal'] != 'govops']


SHOWN = None   # goal ids shown on the page; health, defence and education rules fold into "Running government"


def goal_of(agency, rules):
    a = (agency or '').strip()
    for g, rx in rules:
        if rx.search(a):
            return g if (SHOWN is None or g in SHOWN) else 'govops'
    return 'govops'


def _map_nodes(map_html):
    if not map_html or not os.path.exists(map_html):
        return {}
    h = open(map_html, encoding='utf-8').read()
    m = re.search(r'<script id="DATA" type="application/json">(.*?)</script>', h, re.S)
    return {n['n']: n for n in json.loads(m.group(1))['nodes']} if m else {}


def _windows(market_rows, rules, pif):
    """Full-market windows. Uses the complete agency list (dimension 'agency_all') when the capture wrote it;
    falls back to the top-agency rows and marks the window partial."""
    caps = {}
    for r in market_rows:
        try:
            k = (r['capture_date'][:10], r['window_from'][:10], r['window_to'][:10])
            caps.setdefault(k, []).append((r['dimension'], r['key'], int(float(r['tenders'])), int(float(r.get('open_at_capture') or 0)),
                                           float(r.get('document_fees_sar') or 0)))
        except (KeyError, ValueError):
            continue
    out = []
    for (cap, wf, wt), rr in sorted(caps.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        total = sum(n for d, _, n, _, _ in rr if d == 'type')
        full = [x for x in rr if x[0] == 'agency_all']
        ag = full or [x for x in rr if x[0] == 'agency']
        goals, hits = {}, []
        for _, name, n, op, fee in ag:
            g = goal_of(name, rules)
            o = goals.setdefault(g, {'n': 0, 'open': 0, 'fees': 0.0, 'top': []})
            o['n'] += n; o['open'] += op; o['fees'] += fee; o['top'].append([name, n])
            for label, rx in pif:
                if rx.search(name):
                    hits.append({'pif': label, 'agency': name, 'n': n})
        asum = sum(o['n'] for o in goals.values())
        if not total:   # no tender-type rows: fall back to the agency rows and say so
            print(f"Analyst view WARNING: {wf}..{wt} has no tender-type rows; using the agency rows ({asum}) as the total")
            total = asum
        gap = total - asum if full else 0
        if gap > 0:   # complete agency list is short of the type total: count the rest as unmatched buyers
            print(f"Analyst view WARNING: {wf}..{wt} agency_all rows sum to {asum}, tender types to {total} (gap {gap})")
            goals.setdefault('govops', {'n': 0, 'open': 0, 'fees': 0.0, 'top': []})['n'] += gap
        elif gap < 0:   # agency rows exceed the type total: trust the agency rows
            print(f"Analyst view WARNING: {wf}..{wt} agency_all rows sum to {asum}, more than tender types ({total}); using {asum}")
            total = asum
        for o in goals.values():
            o['top'] = sorted(o['top'], key=lambda x: -x[1])[:6]
        out.append({'capture': cap, 'from': wf, 'to': wt, 'total': total, 'complete': bool(full), 'agencies': len(ag), 'goals': goals, 'pif_hits': hits})
    # one window per (from, to): keep the latest capture of it
    best = {}
    for w in out:
        best[(w['from'], w['to'])] = w
    W = [best[k] for k in sorted(best)]
    if len(W) < 2:
        return W
    now = max(W, key=lambda w: (w['to'], w['from']))   # latest period, then the latest one that ends before it starts
    earlier = [w for w in W if w['to'] < now['from']]
    return ([max(earlier, key=lambda w: w['to'])] if earlier else []) + [now]


def _goal_table(U, W):
    if not W:
        return []
    now = W[-1]; prev = W[-2] if len(W) > 1 else None
    sig = {}
    for e in U['level4_entities']:
        for g in e['goals']:
            s = sig.setdefault(g, {'going_ahead': 0, 'mixed': 0, 'slowing': 0, 'unknown': 0, 'protected': 0, 'delayed': 0, 'cut back': 0, 'shelved': 0, 'not mentioned': 0})
            s[e['signal']] += 1; s[e['outlook']] = s.get(e['outlook'], 0) + 1
    rows = []
    for g in [x['id'] for x in U['level2_goals']] + ['govops']:
        a = (prev or {}).get('goals', {}).get(g, {}).get('n', 0) if prev else None
        b = now['goals'].get(g, {}).get('n', 0)
        sa = 100 * a / prev['total'] if prev and prev['total'] else None
        sb = 100 * b / now['total'] if now['total'] else 0
        d = (sb - sa) if sa is not None else None
        s = sig.get(g, {})
        ahead, slow = s.get('going_ahead', 0), s.get('slowing', 0)
        flag = ''
        small = max(a or 0, b) < 25
        if d is not None and d > 0.5 and slow > ahead:
            flag = 'up_slowing'
        if d is not None and d < -0.5 and ahead > slow and ahead:
            flag = 'down_ahead'
        if flag and small:   # a handful of tenders is not a signal for management
            flag += '_small'
        rows.append({'goal': g, 'prev_n': a, 'now_n': b, 'prev_share': None if sa is None else round(sa, 1), 'now_share': round(sb, 1),
                     'change': None if d is None else round(d, 1), 'small': max(a or 0, b) < 25,
                     'ahead': ahead, 'mixed': s.get('mixed', 0), 'slowing': slow,
                     'continuing': s.get('protected', 0), 'delayed': s.get('delayed', 0), 'cut': s.get('cut back', 0) + s.get('shelved', 0),
                     'flag': flag, 'now_open': now['goals'].get(g, {}).get('open', 0), 'top': now['goals'].get(g, {}).get('top', [])})
    return rows


def _bids(bidraw):
    if not bidraw or not os.path.exists(bidraw):
        return None
    out = []
    for b in json.load(open(bidraw, encoding='utf-8')).get('bids', []):
        st = 'Won' if b.get('eh_won') is True else 'Lost' if b.get('eh_won') is False else 'Cancelled' if b.get('status') == 'Cancelled' \
            else 'Bid' if (b.get('ehsub') or b.get('offer')) else 'Studied'
        if b.get('year'):
            out.append((b.get('year'), str(b.get('client') or ''), st))
    return out


def _watch(U, nodes, bids):
    proj = {e['name']: e for e in U['level4_entities']}
    out = []
    for w in U['watch']:
        rec = None
        if bids is not None:
            rx = re.compile(w['client_pattern'], re.I) if w.get('client_pattern') else None
            rec = {}
            for yr, cl, st in bids:
                if rx and rx.search(cl):
                    y = rec.setdefault(str(yr), {}); y[st] = y.get(st, 0) + 1
        ns = [nodes[n] for n in w['map_names'] if n in nodes]
        val = sum(((n.get('cl') or {}).get('val') or 0) for n in ns)
        client = any(n.get('cat') == 'EH Clients' or (n.get('cl') and 'Competitor' not in (n.get('cat') or '')) for n in ns)
        tiers = [n.get('tier') for n in ns if n.get('tier')]
        p = proj.get(w.get('project') or '')
        out.append({'key': w['key'], 'en': w['en'], 'ar': w['ar'], 'link_en': w['link_en'], 'link_ar': w['link_ar'],
                    'on_map': bool(ns), 'records': len(ns), 'tier': (sorted(tiers)[0] if tiers else None), 'client': client,
                    'value': round(val), 'encounters': sum(int(n.get('bc') or 0) for n in ns),
                    'signal': p['signal'] if p else None, 'outlook': p['outlook'] if p else None, 'bids': rec})
    out.sort(key=lambda x: (-x['value'], -sum(sum(y.values()) for y in (x['bids'] or {}).values()), x['en']))
    return out


def _notes(rows):
    def mk(r):
        return {k: (r.get(k) or '').strip() for k in ('month', 'order', 'kind', 'goal', 'finding_en', 'finding_ar', 'figures_en', 'figures_ar', 'sources',
                                                      'means_for_eh_en', 'means_for_eh_ar', 'next_step_en', 'next_step_ar', 'reviewed_on', 'change_vs_last_month')}
    R = [mk(r) for r in rows if (r.get('finding_en') or '').strip()]
    for r in R:
        r['month'] = r['month'][:7]   # Sheets may turn '2026-10' into a date
    if not R:
        return None, [], [], None
    month = max(r['month'] for r in R)
    cur = [r for r in R if r['month'] == month]
    def order(r):
        try:
            return float(r['order'])
        except ValueError:
            return 99
    notes = sorted([r for r in cur if r['kind'].lower() in ('', 'note')], key=order)
    unknown = sorted([r for r in cur if r['kind'].lower() == 'unknown'], key=order)
    rev = max([r['reviewed_on'][:10] for r in cur if r['reviewed_on']] or [None])
    return month, notes, unknown, rev


def analyst(market_rows, tenders, map_html, note_rows, bidraw=None, umbrella_path=UMBRELLA):
    U = load_umbrella(umbrella_path)
    if not U:
        return None
    global SHOWN
    SHOWN = {g['id'] for g in U['level2_goals']}
    rules = _rules(U)
    pif = [(label, re.compile(rx, re.I)) for label, rx in U['level3_pif']['pif_buyer_names']]
    for t in tenders:
        t['goal'] = goal_of(t.get('agency') or t.get('agency_raw'), rules)
    W = _windows(market_rows, rules, pif)
    month, notes, unknown, rev = _notes(note_rows)
    return {'umbrella': U, 'windows': [{k: v for k, v in w.items()} for w in W[-2:]], 'goal_table': _goal_table(U, W),
            'watch': _watch(U, _map_nodes(map_html), _bids(bidraw)), 'bids_loaded': bool(bidraw and os.path.exists(bidraw)), 'notes_month': month, 'notes': notes, 'unknown': unknown,
            'reviewed': rev or U.get('reviewed'), 'review_every_days': U.get('review_every_days', 35)}


# ====================================================================== page side
CSS = r"""
#av .lede{font-size:12.5px;color:var(--muted);margin:2px 0 10px;max-width:1000px}
#av h3{font-size:14.5px;margin:22px 0 4px;display:flex;align-items:center;gap:8px}
#av h3 .n{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:var(--green);color:#fff;font-size:12px;font-weight:800;flex:none}
#av .brief{background:var(--chip);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0 6px}
#av .brief b.t{display:block;font-size:13px;margin-bottom:4px}#av .brief ol{margin:4px 0 0;padding-inline-start:20px}#av .brief li{font-size:13px;margin:3px 0}
#av .howto{display:flex;gap:8px 18px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:8px 0 2px}
#av .howto span{white-space:nowrap}
#av .sig{font-weight:700}#av .sig.up{color:var(--green)}#av .sig.down{color:var(--red)}#av .sig.mix{color:var(--muted)}
#av .reading{font-style:normal;border-bottom:1px dotted var(--muted);cursor:help}
#av .warnline{font-size:12.5px;background:var(--card);border:1px solid var(--line);border-inline-start:3px solid var(--amber);border-radius:8px;padding:9px 12px;margin:8px 0}
#av .flag{font-weight:700;color:var(--amber)}
#av .chipr{display:inline-block;background:var(--chip);border:1px solid var(--line);border-radius:6px;padding:1px 7px;margin:2px 4px 2px 0;font-size:11.5px;white-space:nowrap}
#av .gcard{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:10px 0;background:var(--card)}
#av .gcard .gt{font-weight:800;font-size:13.5px}#av .gcard .nw{font-size:11.5px;color:var(--muted);margin-inline-start:6px}
#av .gcard ul{margin:6px 0;padding-inline-start:18px;font-size:12.5px}#av .gcard .row{font-size:12.5px;margin-top:4px}
#av .avn{border-inline-start:3px solid var(--core);padding-inline-start:12px;margin:14px 0}
#av .avn .h{font-weight:800;font-size:13.5px}#av .avn .f{font-size:12.5px;margin:4px 0}#av .avn .m{font-size:12.5px}#av .avn .x{font-size:12.5px;font-weight:700;margin-top:2px}
#av .avn .s{font-size:11px;color:var(--muted);margin-top:2px}
#av .src{font-size:11px;color:var(--muted)}#av .src abbr{text-decoration:none;border-bottom:1px dotted var(--muted);cursor:help}
#av details.more summary{cursor:pointer;font-size:12.5px;color:var(--muted);padding:8px 2px}
#av .mini{display:inline-block;height:8px;border-radius:2px;vertical-align:middle}
#av .stamp-rv{font-weight:700;color:var(--ink);background:var(--chip);border:1px solid var(--line);border-radius:7px;padding:3px 9px;font-size:12px}
#av .stamp-rv.stale{background:#FFF1D6;border-color:#E8862E;color:#7A4200}body.dark #av .stamp-rv.stale{background:#3A2A12;color:#FFD9A8}
#av table.t th.num{text-align:end}#av .flowwrap{overflow-x:auto}#av-flow svg{min-width:900px}
@media(max-width:700px){#av .howto span{white-space:normal}}
"""

HTML = r"""
<section class="card" id="av">
<div class="hd"><h2 data-en="Analyst view — how these tenders fit the Kingdom's bigger plan" data-ar="قراءة تحليلية — موقع هذه المنافسات من خطة المملكة الأشمل">Analyst view — how these tenders fit the Kingdom's bigger plan</h2></div>
<div id="av-body"></div>
</section>
"""

JS = r"""
// ================= Analyst view
function renderAnalyst(){
  const A=D.analyst,box=$('av-body');if(!box)return;
  if(!A||!A.umbrella){box.innerHTML=`<div class="empty empty-analyst">${L('Searched, none found: the Vision 2030 umbrella file (pipeline/vision_umbrella.json) was not loaded in this build.','تم البحث، ولا توجد بيانات: لم يُحمَّل ملف مظلة رؤية 2030 في هذا البناء.')}</div>`;return}
  const U=A.umbrella,S=U.sources,G={};U.level2_goals.forEach(g=>G[g.id]=g);G.govops=U.level2_not_linked;
  const P={};U.level1_pillars.forEach(p=>P[p.id]=p);const ECO={};U.level3_pif.ecosystems.forEach(e=>ECO[e.id]=e);
  const LN={};U.level6_eh_lines.forEach(l=>LN[l.line]=l);
  const gname=(g,short)=>{const x=G[g];return x?L(short?x.short_en:x.en,short?x.short_ar:x.ar):g};
  const hasK=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
  const srcs=a=>(a||[]).map(s=>hasK(S,s)?`<abbr data-tip="${esc(L(S[s].en,S[s].ar)+' · '+L('as of ','بتاريخ ')+(/^\d{4}-\d{2}-\d{2}$/.test(S[s].as_of)?fmtD(S[s].as_of):S[s].as_of))}">${esc(s)}</abbr>`:esc(s)).join(', ');
  const srcTxt=a=>(a||[]).map(s=>hasK(S,s)?s+' '+L(S[s].en,S[s].ar)+' ('+(/^\d{4}-\d{2}-\d{2}$/.test(S[s].as_of)?fmtD(S[s].as_of):S[s].as_of)+')':s).join('<br>');
  const SIG={going_ahead:['▲','up',L('going ahead','ماضٍ')],mixed:['■','mix',L('mixed','متباين')],slowing:['▼','down',L('slowing','يتباطأ')],unknown:['?','mix',L('unknown','غير معروف')]};
  const OUT={protected:L('continuing','مستمر'),delayed:L('delayed','مؤجل'),'cut back':L('cut back','مقلّص'),shelved:L('shelved','مجمّد'),'not mentioned':L('not mentioned','غير مذكور')};
  const reading=`<i class="reading" data-tip="${esc(L('Our reading: an EH interpretation, not stated in a source.','قراءتنا: تفسير من آفاق وليس منصوصًا في مصدر.'))}">${L('our reading','قراءتنا')}</i>`;
  const W=A.windows||[],now=W[W.length-1],prev=W.length>1?W[W.length-2]:null;
  const wlab=w=>w?fmtD(w.from)+' – '+fmtD(w.to):'—';
  const wshort=w=>{if(!w)return '—';const o={day:'numeric',month:'short'},loc=LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB';return new Date(w.from+'T00:00:00').toLocaleDateString(loc,o)+'–'+new Date(w.to+'T00:00:00').toLocaleDateString(loc,o)};
  const age=A.reviewed?Math.floor((NOW-new Date(A.reviewed+'T08:00:00+03:00'))/864e5):null,stale=age==null||age>(A.review_every_days||35);
  let h='';
  // ---- stamp, in brief, how to read
  h+=`<div class="stamp" style="margin-top:6px"><span class="stamp-rv${stale?' stale':''}">${L('Last reviewed: ','آخر مراجعة: ')}${A.reviewed?fmtD(A.reviewed):'—'}${stale&&age!=null?L(` — ${age} days ago, due for review`,` — قبل ${age} يومًا، تحتاج مراجعة`):''}</span>`+
     (now?`<span>${L('Tenders compared: ','المنافسات المقارنة: ')}${prev?wlab(prev)+L(' and ',' و')+wlab(now):wlab(now)} (${fmtN((prev?prev.total:0)+now.total)} ${L('tenders','منافسة')})</span>`:'')+`</div>`;
  const N=A.notes||[];
  h+=`<div class="brief"><b class="t">${L('In brief','باختصار')}</b>`+(N.length?`<ol>${N.slice(0,3).map(n=>`<li>${esc(L(n.finding_en,n.finding_ar||n.finding_en))}</li>`).join('')}</ol>`:`<div class="empty">${L('Searched, none found: no analyst notes for this month in the private sheet.','تم البحث، ولا توجد ملاحظات تحليلية لهذا الشهر في الورقة الخاصة.')}</div>`)+
     `<div class="howto"><span>${L('Parts 1–3 describe the whole Etimad market and ignore the filters above; parts 4–5 follow the Relevance filter.','الأجزاء 1–3 تصف سوق اعتماد كاملًا ولا تتأثر بالمرشحات أعلاه؛ والجزءان 4–5 يتبعان مرشح الصلة.')}</span>`+
     `<span><b class="sig up">▲</b> ${L('going ahead','ماضٍ')} · <b class="sig mix">■</b> ${L('mixed','متباين')} · <b class="sig down">▼</b> ${L('slowing','يتباطأ')}</span>`+
     `<span>${L('S1, S2 … = source page; hover for its name and date.','S1 وS2 … = الصفحة المصدرية؛ مرّر المؤشر لرؤية اسمها وتاريخها.')}</span></div></div>`;
  // ---- 1 the plan in one picture
  h+=`<h3><span class="n">1</span>${L('The plan in one picture','الخطة في صورة واحدة')}</h3><div class="hd"><p class="lede" style="margin:0">${L('Read each row from left to right: the Vision 2030 pillar, the goal our sources name, the PIF investment area behind it, the projects that deliver it, how many Etimad tenders its buyers published, and which EH services it calls on. Hover a row for the detail and the sources.','اقرأ كل صف من اليمين إلى اليسار: ركيزة رؤية 2030، والهدف الذي تسميه مصادرنا، ومجال استثمار الصندوق خلفه، والمشاريع التي تنفذه، وعدد منافسات اعتماد التي طرحتها جهاته، وخدمات آفاق التي يحتاجها. مرّر المؤشر على الصف لرؤية التفاصيل والمصادر.')}</p><button class="png" data-c="av-flow" data-n="etimad_analyst_plan">${L('Export PNG','تصدير PNG')}</button></div><div class="flowwrap"><div id="av-flow"></div></div>`;
  h+=`<div class="src" style="margin-top:4px">${L('Pillars: Ministry of Economy and Planning site, added for this section (checked 7 Oct 2026). Goal → pillar, goal → PIF area (except clean energy & water → water and waste, which S3 states), project → goal and buyer → goal are ','الركائز: موقع وزارة الاقتصاد والتخطيط، أضيفت لهذا القسم (تم التحقق في 7 أكتوبر 2026). روابط الهدف بالركيزة وبمجال الصندوق (عدا الطاقة النظيفة والمياه ← المياه والنفايات، المنصوص عليها في S3) والمشروع والجهة بالهدف هي ')}${reading}.</div>`;
  // ---- 2 money moving
  const GT=A.goal_table||[],GTS=GT.slice().sort((x,y)=>(x.goal==='govops')-(y.goal==='govops')||y.now_share-x.now_share);
  h+=`<h3><span class="n">2</span>${L('Where public money is moving, and whether it is real','إلى أين يتجه المال العام، وهل هو حقيقي')}</h3><p class="lede">${L('Each goal\'s share of all Etimad tenders in the earlier and the latest period (the buyer decides the goal), beside what the Vision 2030 page and the government-finance page say about its projects. A warning marks a goal where tenders and projects point in opposite directions — the most useful reading for management.','حصة كل هدف من كل منافسات اعتماد في الفترة السابقة والأحدث (الجهة المشترية تحدد الهدف)، بجانب ما تقوله صفحة رؤية 2030 وصفحة المالية العامة عن مشاريعه. علامة التحذير تبيّن هدفًا تتعاكس فيه المنافسات والمشاريع — وهي أهم قراءة للإدارة.')}</p>`;
  if(!now)h+=`<div class="empty">${L('Searched, none found: no full-market capture on file yet.','تم البحث، ولا توجد بيانات: لا يوجد التقاط للسوق الكامل بعد.')}</div>`;
  else{
    const mx=Math.max(1,...GT.map(r=>Math.abs(r.change||0)));
    h+=`<div class="tw" style="max-height:none"><table class="t"><thead><tr><th>${L('Goal','الهدف')}</th><th class="num">${L('Share','الحصة')} ${prev?wshort(prev):''}</th><th class="num">${L('Share','الحصة')} ${wshort(now)}</th><th class="num">${L('Change (points)','التغير (نقاط)')}</th><th>${L('Projects — Vision 2030 page (S1)','المشاريع — صفحة رؤية 2030 (S1)')}</th><th>${L('Budget view — finance page (S2)','نظرة الميزانية — صفحة المالية (S2)')}</th><th>${L('Reading','القراءة')}</th></tr></thead><tbody>`+
      GTS.map(r=>{const d=r.change,w=d==null?0:Math.round(46*Math.abs(d)/mx),cls=d==null?'mix':d>0.5?'up':d<-0.5?'down':'mix';
        const tipT=`<b>${esc(gname(r.goal))}</b><br>${prev?wlab(prev)+': '+fmtN(r.prev_n)+'<br>':''}${wlab(now)}: ${fmtN(r.now_n)} (${L('open at capture','مفتوحة عند الالتقاط')} ${fmtN(r.now_open)})`+(r.top.length?'<br><span style="color:var(--muted)">'+r.top.slice(0,4).map(x=>esc(x[0])+' '+x[1]).join('<br>')+'</span>':'');
        const proj=(r.ahead+r.mixed+r.slowing)?`<span class="sig up">▲${r.ahead}</span> <span class="sig mix">■${r.mixed}</span> <span class="sig down">▼${r.slowing}</span>`:`<span style="color:var(--muted)">${L('none tracked','لا يوجد')}</span>`;
        const fis=(r.continuing+r.delayed+r.cut)?L(`${r.continuing} continuing · ${r.delayed} delayed · ${r.cut} cut back or shelved`,`${r.continuing} مستمر · ${r.delayed} مؤجل · ${r.cut} مقلّص أو مجمّد`):`<span style="color:var(--muted)">—</span>`;
        const flag=r.flag==='up_slowing_small'?L('Tenders up, projects slowing (few tenders)','المنافسات ترتفع والمشاريع تتباطأ (منافسات قليلة)'):r.flag==='down_ahead_small'?L('Tenders down, projects going ahead (few tenders)','المنافسات تنخفض والمشاريع ماضية (منافسات قليلة)'):r.flag==='up_slowing'?L('⚠ Tenders up, projects slowing','⚠ المنافسات ترتفع والمشاريع تتباطأ'):r.flag==='down_ahead'?L('⚠ Tenders down, projects going ahead','⚠ المنافسات تنخفض والمشاريع ماضية'):'';
        return `<tr data-tip="${esc(tipT)}"><td>${esc(gname(r.goal))}${r.goal==='govops'?` <span class="src">(${L('no programme named','لا برنامج مسمّى')})</span>`:''}</td><td class="num">${r.prev_share==null?'—':r.prev_share.toFixed(1)+'%'}</td><td class="num">${r.now_share.toFixed(1)}%</td>`+
          `<td class="num"><span class="mini" style="width:${w}px;background:${cls==='down'?'var(--red)':cls==='up'?'var(--green)':'var(--muted)'};opacity:.75"></span> <span class="sig ${cls}">${d==null?'':d>0.5?'▲':d<-0.5?'▼':'■'}</span> ${d==null?'—':(d>0?'+':'')+d.toFixed(1)}${r.small?` <span class="src" data-tip="${esc(L('Fewer than 25 tenders: a few tenders move the share a lot.','أقل من 25 منافسة: منافسات قليلة تحرك الحصة كثيرًا.'))}">*</span>`:''}</td><td>${proj}</td><td>${fis}</td><td class="flag">${flag}</td></tr>`}).join('')+`</tbody></table></div>`;
    h+=`<div class="src" style="margin-top:6px">${L(`Sources: S11 (tenders), S1 and S2 (projects); hover a code for its date. Shares are compared rather than counts because the periods differ in length. * fewer than 25 tenders. "Running government" covers health, defence and security, education, justice and other buyers no rule matched.`,`المصادر: S11 (المنافسات)، وS1 وS2 (المشاريع)؛ مرّر المؤشر على الرمز لرؤية تاريخه. تُقارن الحصص لا الأعداد لأن الفترتين مختلفتان في الطول. * أقل من 25 منافسة. «تشغيل الجهات الحكومية» يشمل الصحة والدفاع والأمن والتعليم والعدل والجهات التي لم تطابقها أي قاعدة.`)} ${srcs(['S11','S1','S2'])}</div>`;
    if(!now.complete)h+=`<div class="warnline">${L('This capture saved only the largest agencies, so goal shares are approximate. The next capture writes the full agency list.','حفظ هذا الالتقاط أكبر الجهات فقط، لذا حصص الأهداف تقريبية. يكتب الالتقاط التالي قائمة الجهات كاملة.')}</div>`;
  }
  // ---- 3 PIF lens
  const PF=U.level3_pif,WT=PF.sector_weights_pct,yrs=Object.keys(WT).sort(),secs=Object.keys(WT[yrs[yrs.length-1]]);
  h+=`<h3><span class="n">3</span>${L('The PIF lens','من زاوية صندوق الاستثمارات العامة')}</h3>`;
  const hits=W.flatMap(w=>w.pif_hits||[]);
  h+=`<div class="warnline"><b>${L('Blind spot: ','نقطة عمياء: ')}</b>${esc(L(PF.blind_spot_en,PF.blind_spot_ar))} `+(now?(hits.length?L('PIF names found among Etimad buyers in these periods: ','أسماء من مجموعة الصندوق ظهرت بين جهات اعتماد في هاتين الفترتين: ')+hits.map(x=>`${esc(x.pif)} (${esc(x.agency)}, ${x.n})`).join('; ')+'.':L(`We searched all ${fmtN(W.reduce((a,w)=>a+w.total,0))} tenders (${W.map(wlab).join(L(' and ',' و'))}) for ${PF.pif_buyer_names.length} PIF names (${PF.pif_buyer_names.map(x=>x[0]).join(', ')}): none found.`,`بحثنا في كل المنافسات البالغة ${fmtN(W.reduce((a,w)=>a+w.total,0))} (${W.map(wlab).join(' و')}) عن ${PF.pif_buyer_names.length} اسمًا من مجموعة الصندوق: لم نجد أيًا منها.`)):'')+`</div>`;
  const gshare=gs=>now?gs.reduce((a,g)=>a+((GT.find(r=>r.goal===g)||{}).now_share||0),0):null;
  h+=`<div class="g2"><div><b>${L('PIF sector weights (% of assets)','أوزان القطاعات لدى الصندوق (% من الأصول)')}</b><div class="tw" style="margin-top:6px;max-height:none"><table class="t"><thead><tr><th>${L('Sector','القطاع')}</th>${yrs.map(y=>`<th class="num">${y}</th>`).join('')}<th class="num">${L('Etimad share now, closest goals','حصة اعتماد الآن لأقرب الأهداف')}</th></tr></thead><tbody>`+
    secs.map(s=>{const gs=PF.sector_goal_reading[s]||[],v=gshare(gs);return `<tr><td>${esc(L(s,PF.sector_names[s]||s))}</td>${yrs.map(y=>`<td class="num">${WT[y][s]}%</td>`).join('')}<td class="num" data-tip="${esc(gs.map(g=>gname(g)).join(' + '))}">${v==null?'—':v.toFixed(1)+'%'}</td></tr>`}).join('')+
    `</tbody></table></div><div class="src">${L('PIF weights: ','أوزان الصندوق: ')}${srcs(PF.sector_weights_src)}. ${L('Sector → goal is ','ربط القطاع بالهدف ')}${reading}; ${L('Etimad shows government buyers, not PIF spending.','يعرض اعتماد الجهات الحكومية لا إنفاق الصندوق.')}</div></div>`+
    `<div><b>${L('What the 2026–2030 strategy changes','ما الذي تغيّره استراتيجية 2026–2030')}</b><ul class="nts" style="margin-top:6px;padding-inline-start:18px">${(LANG==='ar'?PF.shifts_ar:PF.shifts_en).map(x=>`<li>${esc(x)}</li>`).join('')}</ul><div class="src">${srcs(['S3','S5'])}</div></div></div>`;
  const WL=A.watch||[],has=x=>x.value||x.client||(x.bids&&Object.keys(x.bids).length),act=WL.filter(has),rest=WL.filter(x=>!has(x));
  const wrow=x=>`<tr><td><b>${esc(L(x.en,x.ar))}</b></td><td>${esc(L(x.link_en,x.link_ar))}</td><td>${x.on_map?esc(x.tier==='GOV'?L('Government','حكومية'):x.tier||'—'):`<span style="color:var(--muted)">${L('Not on the map','غير موجودة في الخريطة')}</span>`}</td><td>${x.client?L('Yes','نعم'):L('No','لا')}</td><td class="num">${x.value?fmtN(x.value):'—'}</td><td>${x.bids==null?'<span style="color:var(--muted)">'+L('tracker not loaded','الجدول غير محمّل')+'</span>':Object.keys(x.bids).length?Object.keys(x.bids).sort().map(y=>y+': '+Object.entries(x.bids[y]).map(([k,v])=>(k==='Cancelled'?L('Cancelled','ملغاة'):L(...STAT[k]))+' '+v).join(L(', ','، '))).join('<br>'):'<span style="color:var(--muted)">—</span>'}</td><td>${x.signal?`<span class="sig ${SIG[x.signal][1]}">${SIG[x.signal][0]}</span> ${SIG[x.signal][2]}${x.outlook?' · '+(OUT[x.outlook]||esc(x.outlook)):''}`:'<span style="color:var(--muted)">—</span>'}</td></tr>`;
  const whead=`<thead><tr><th>${L('Name','الاسم')}</th><th>${L('Link to PIF (as recorded)','الصلة بالصندوق (كما هي مسجلة)')}</th><th>${L('Tier on the map','الفئة في الخريطة')}</th><th>${L('EH client','عميل لآفاق')}</th><th>${L('Client value (SAR)','قيمة العميل (ريال)')}</th><th data-tip="${esc(L(U.watch_note_method.en,U.watch_note_method.ar))}">${L('EH tenders with them (bid tracker)','منافسات آفاق معهم (جدول المتابعة)')}</th><th>${L('Project status (S1 · S2)','حالة المشروع (S1 · S2)')}</th></tr></thead>`;
  h+=`<div style="margin-top:14px"><b>${L('Suggested names to watch','أسماء مقترحة للمتابعة')}</b> <span class="src">— ${esc(L(U.watch_note.en,U.watch_note.ar))} ${srcs(['S9','S10','S1','S2'])}</span>`+
     (WL.length?`<div class="tw" style="margin-top:6px;max-height:none"><table class="t">${whead}<tbody>${act.map(wrow).join('')}</tbody></table></div>`+(rest.length?`<details class="more"><summary>${L(`Show ${rest.length} more on the list with no EH client value or tender record yet`,`عرض ${rest.length} أخرى في القائمة بلا قيمة عميل أو سجل منافسات بعد`)}</summary><div class="tw" style="max-height:none"><table class="t">${whead}<tbody>${rest.map(wrow).join('')}</tbody></table></div></details>`:''):`<div class="empty">${L('Searched, none found.','تم البحث، ولا توجد نتائج.')}</div>`)+`</div>`;
  // ---- 4 newer goals
  const RELT=D.tenders.filter(t=>F.rel==='all'?true:F.rel==='rel'?t.relevance!=='Not EH':t.relevance===F.rel);
  const NG=['water','waste','envcomp','climate','energy','events'].filter(g=>G[g]&&G[g].is_newer);
  h+=`<h3><span class="n">4</span>${L('The newer national goals and EH','الأهداف الوطنية الأحدث وآفاق البيئة')}</h3><p class="lede">${L('Goals announced or reset since 2021 that touch EH\'s services. The tender references follow the Relevance filter above; copy a reference into Etimad\'s search to open it.','أهداف أُعلنت أو حُدّثت منذ 2021 وتمس خدمات آفاق. تتبع أرقام المنافسات مرشح الصلة أعلاه؛ انسخ الرقم وابحث به في اعتماد لفتح المنافسة.')}</p>`;
  NG.forEach(g=>{const x=G[g],ts=RELT.filter(t=>t.goal===g),gr=GT.find(r=>r.goal===g)||{},rec={};ts.forEach(t=>rec[t.eh_status]=(rec[t.eh_status]||0)+1);
    const lines=U.level6_eh_lines.filter(l=>l.goals.includes(g)).map(l=>L(l.short_en,l.short_ar));
    h+=`<div class="gcard"><span class="gt">${esc(L(x.en,x.ar))}</span><span class="nw">${esc(L(x.newer_en,x.newer_ar))}</span>`+
      `<ul>${(LANG==='ar'?x.figures_ar:x.figures_en).map(f=>`<li>${esc(f)}</li>`).join('')}</ul>`+
      `<div class="row"><b>${L('Regulator or fund: ','الجهة التنظيمية أو الصندوق: ')}</b>${esc(L(x.regulator_en,x.regulator_ar))}</div>`+
      `<div class="row"><b>${L('EH services it calls on: ','خدمات آفاق التي يحتاجها: ')}</b>${lines.map(esc).join(L(', ','، '))||'—'} <span class="src">(${reading})</span></div>`+
      `<div class="row"><b>${L('Etimad, all buyers in this goal: ','اعتماد، كل جهات هذا الهدف: ')}</b>${now?L(`${fmtN(gr.now_n||0)} tenders in ${wlab(now)}`,`${fmtN(gr.now_n||0)} منافسة في ${wlab(now)}`)+(prev?L(` (${fmtN(gr.prev_n||0)} in the period before)`,` (${fmtN(gr.prev_n||0)} في الفترة السابقة)`):''):'—'}</div>`+
      `<div class="row"><b>${L('EH-relevant tenders captured: ','المنافسات ذات الصلة الملتقطة: ')}</b>${ts.length?ts.map(t=>`<span class="chipr" data-tip="${esc('<span class=ar dir=rtl>'+esc(t.title)+'</span><br>'+esc(t.agency))}"><span class="ref">${esc(t.ref)}</span> · ${L(...REL[t.relevance])}${t.eh_status!=='Not studied'?' · '+L(...STAT[t.eh_status]):''}</span>`).join(''):`<span style="color:var(--muted)">${L('Searched, none found','تم البحث، ولا توجد نتائج')}${D.last_capture?' — '+L('capture of ','التقاط ')+fmtD(D.last_capture):''}.</span>`}</div>`+
      (ts.length?`<div class="row"><b>${L('EH record on these (bid tracker): ','سجل آفاق فيها (جدول المنافسات): ')}</b>${Object.entries(rec).map(([k,v])=>L(...STAT[k])+' '+v).join(' · ')}</div>`:'')+
      `<div class="src" style="margin-top:4px">${srcs(x.src)}</div></div>`});
  // ---- 5 notes
  h+=`<h3><span class="n">5</span>${L('Analyst notes','ملاحظات تحليلية')}${A.notes_month?' — '+esc(A.notes_month):''}</h3>`;
  h+=N.length?N.map(n=>`<div class="avn"><div class="h">${esc(L(n.finding_en,n.finding_ar||n.finding_en))}</div><div class="f">${esc(L(n.figures_en,n.figures_ar||n.figures_en))}</div><div class="m"><b>${L('What it means for EH: ','ماذا يعني لآفاق: ')}</b>${esc(L(n.means_for_eh_en,n.means_for_eh_ar||n.means_for_eh_en))}</div><div class="x">${L('Next step: ','الخطوة التالية: ')}${esc(L(n.next_step_en,n.next_step_ar||n.next_step_en))}</div>${n.change_vs_last_month?`<div class="s">${L('Since last month: ','منذ الشهر الماضي: ')}${esc(n.change_vs_last_month)}</div>`:''}<div class="s">${srcs(n.sources.split(/[ ,;]+/).filter(Boolean))}</div></div>`).join(''):`<div class="empty empty-notes">${L('Searched, none found: no analyst notes for this month in the private sheet (tab "analyst_notes").','تم البحث، ولا توجد ملاحظات تحليلية لهذا الشهر في الورقة الخاصة (تبويب analyst_notes).')}</div>`;
  // ---- 6 unknowns
  const UK=A.unknown||[];
  h+=`<h3><span class="n">6</span>${L("What we don't know",'ما لا نعرفه')}</h3>`+(UK.length?`<div class="tw" style="max-height:none"><table class="t"><thead><tr><th>${L('Gap','الفجوة')}</th><th>${L('Decision it affects','القرار المتأثر')}</th></tr></thead><tbody>${UK.map(u=>`<tr><td>${esc(L(u.finding_en,u.finding_ar||u.finding_en))}</td><td>${esc(L(u.means_for_eh_en,u.means_for_eh_ar||u.means_for_eh_en))}</td></tr>`).join('')}</tbody></table></div>`:`<div class="empty">${L('Searched, none found.','تم البحث، ولا توجد نتائج.')}</div>`);
  box.innerHTML=h;
  avFlow(U,G,P,ECO,LN,GT,now,prev,wshort,gname,SIG,OUT,srcTxt);
}
function avFlow(U,G,P,ECO,LN,GT,now,prev,wshort,gname,SIG,OUT,srcTxt){
  const el=$('av-flow');if(!el)return;
  const rtl=LANG==='ar',W=1240,rowH=50,top=34;
  const order=['P1','P2','P3'];const goals=[];order.forEach(p=>U.level2_goals.filter(g=>g.pillar===p).forEach(g=>goals.push(g.id)));goals.push('govops');
  const H=top+goals.length*rowH+8;
  const C={pil:[0,118],goal:[126,232],eco:[364,160],proj:[532,250],ten:[790,196],eh:[992,248]};
  const X=(c,off=0)=>rtl?W-C[c][0]-off:C[c][0]+off,anc=rtl?'end':'start';
  const tr=(s,n)=>{s=String(s||'');return s.length>n?s.slice(0,n-1)+'…':s};
  const T=(c,y,s,st,off=6)=>`<text x="${X(c,off)}" y="${y}" text-anchor="${anc}"${st?` style="${st}"`:''}>${esc(s)}</text>`;
  const mx=Math.max(1,...GT.filter(r=>r.goal!=='govops').map(r=>Math.max(r.prev_n||0,r.now_n||0))),CAP=150;
  let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" direction="ltr" role="img" aria-label="${esc(L('The plan in one picture','الخطة في صورة واحدة'))}">`;
  [['pil',L('Vision 2030 pillar','ركيزة رؤية 2030')],['goal',L('Goal','الهدف')],['eco',L('PIF investment area','مجال استثمار الصندوق')],['proj',L('Delivering projects','المشاريع المنفذة')],['ten',L('Etimad tenders (two periods)','منافسات اعتماد (فترتان)')],['eh',L('EH services','خدمات آفاق')]].forEach(([c,t])=>{s+=T(c,18,t,'font-weight:700')});
  s+=`<line class="grid" x1="0" x2="${W}" y1="${top-8}" y2="${top-8}"/>`;
  // pillar bands
  let i0=0;order.concat(['none']).forEach(p=>{const ids=p==='none'?['govops']:goals.filter(g=>g!=='govops'&&G[g].pillar===p);if(!ids.length)return;const y=top+i0*rowH,h=ids.length*rowH-6;
    s+=`<rect x="${rtl?W-C.pil[0]-C.pil[1]:C.pil[0]}" y="${y}" width="${C.pil[1]}" height="${h}" rx="8" fill="${p==='none'?'var(--muted)':'var(--adj)'}" fill-opacity="${p==='none'?0.08:0.12}"/>`;
    const lab=p==='none'?L('Not linked','غير مرتبط'):L(P[p].short_en,P[p].short_ar),ws=lab.split(' ');const mid=y+h/2;
    (ws.length>1&&lab.length>12?[ws.slice(0,Math.ceil(ws.length/2)).join(' '),ws.slice(Math.ceil(ws.length/2)).join(' ')]:[lab]).forEach((ln,k,a)=>{s+=T('pil',mid+4+(k-(a.length-1)/2)*14,ln,'font-weight:700;font-size:12px',10)});
    i0+=ids.length});
  goals.forEach((g,i)=>{const y=top+i*rowH,cy=y+rowH/2-3,r=GT.find(x=>x.goal===g)||{prev_n:0,now_n:0},gov=g==='govops',gd=G[g];
    s+=`<line class="grid" x1="${rtl?0:C.goal[0]}" x2="${rtl?W-C.goal[0]:W}" y1="${y+rowH-3}" y2="${y+rowH-3}"/>`;
    // goal
    s+=T('goal',cy-2,tr(gname(g,true),34),'font-weight:700;font-size:12px');
    s+=T('goal',cy+13,gov?L('no programme named in our sources','لا برنامج مسمّى في مصادرنا'):(gd.src||[]).join(' · '),'font-size:10px');
    // eco
    const ecos=gov?[]:U.level3_pif.ecosystems.filter(e=>e.goals.includes(g)).map(e=>L(e.short_en,e.short_ar));
    if(!ecos.length)s+=T('eco',cy+4,'—');else{s+=T('eco',cy-2,tr(ecos[0],26));if(ecos[1])s+=T('eco',cy+13,tr(ecos.slice(1).join(rtl?'، ':', '),26))}
    // projects
    const ents=gov?[]:U.level4_entities.filter(e=>e.goals.includes(g));
    if(gov)s+=T('proj',cy+4,L('health, defence, education, justice','الصحة، الدفاع، التعليم، العدل'));
    else if(!ents.length)s+=T('proj',cy+4,L('none tracked','لا يوجد'));
    else{const c={going_ahead:0,mixed:0,slowing:0,unknown:0};ents.forEach(e=>c[e.signal]++);
      s+=T('proj',cy-2,`▲ ${c.going_ahead}   ■ ${c.mixed}   ▼ ${c.slowing}`+(c.unknown?`   ? ${c.unknown}`:''),'font-weight:700;font-size:12px');
      s+=T('proj',cy+13,tr(L('e.g. ','مثل ')+ents.slice(0,3).map(e=>L(e.name,e.name_ar)).join(rtl?'، ':', '),40))}
    // tenders: two bars
    const bw=v=>Math.min(CAP,Math.max(v?2:0,Math.round(120*v/mx))),bx=(w)=>rtl?W-C.ten[0]-6-w:C.ten[0]+6;
    if(prev){const w1=bw(r.prev_n||0);s+=`<rect x="${bx(w1)}" y="${cy-12}" width="${w1}" height="9" rx="2" fill="var(--muted)" fill-opacity="0.45"/>`+T('ten',cy-4,fmtN(r.prev_n||0),'font-size:10px',12+w1)}
    const w2=bw(r.now_n||0);s+=`<rect x="${bx(w2)}" y="${cy+1}" width="${w2}" height="9" rx="2" fill="var(--core)"/>`+T('ten',cy+10,fmtN(r.now_n||0),'font-weight:700;font-size:11px',12+w2);
    // EH lines
    const ls=U.level6_eh_lines.filter(l=>l.goals.includes(g)).map(l=>L(l.short_en,l.short_ar));
    if(!ls.length)s+=T('eh',cy+4,'—');else{s+=T('eh',cy-2,tr(ls.slice(0,2).join(rtl?'، ':', '),38));if(ls.length>2)s+=T('eh',cy+13,tr(ls.slice(2,4).join(rtl?'، ':', ')+(ls.length>4?(rtl?' و':' +')+(ls.length-4)+L(' more',' أخرى'):''),38))}
    // hover
    const tip=`<b>${esc(gov?L(G.govops.en,G.govops.ar):L(gd.en,gd.ar))}</b>`+(gov?`<br>${esc(L(G.govops.note_en,G.govops.note_ar))}`:`<br>${L('Pillar','الركيزة')}: ${esc(L(P[gd.pillar].en,P[gd.pillar].ar))} (${L('our reading','قراءتنا')})`)+
      (ecos.length?`<br>${L('PIF area','مجال الصندوق')}: ${esc(U.level3_pif.ecosystems.filter(e=>e.goals.includes(g)).map(e=>L(e.en,e.ar)).join(' · '))}`:'')+
      (ents.length?`<br>${L('Projects','المشاريع')}: ${ents.map(e=>esc(L(e.name,e.name_ar))+' '+SIG[e.signal][0]+(e.outlook?' ('+(OUT[e.outlook]||e.outlook)+')':'')).join('; ')}`:'')+
      `<br>${L('Etimad tenders','منافسات اعتماد')}: ${prev?wshort(prev)+' '+fmtN(r.prev_n||0)+' · ':''}${now?wshort(now)+' '+fmtN(r.now_n||0)+' ('+(r.now_share||0).toFixed(1)+'%)':'—'}`+
      (ls.length?`<br>${L('EH services','خدمات آفاق')}: ${esc(ls.join(rtl?'، ':', '))}`:'')+
      `<br><span style="color:var(--muted)">${srcTxt((gov?[]:gd.src).concat(['S1','S2','S3','S11']).filter((v,k,a)=>a.indexOf(v)===k))}</span>`;
    s+=`<rect class="hit" fill="transparent" x="0" y="${y}" width="${W}" height="${rowH-3}" data-tip="${esc(tip)}"/>`});
  const capped=GT.some(r=>r.goal==='govops'&&Math.max(r.prev_n||0,r.now_n||0)*120/mx>CAP);
  el.innerHTML=s+'</svg>'+`<div class="legend" style="margin-top:4px;flex-wrap:wrap"><span><i style="background:var(--muted);opacity:.45"></i>${prev?wshort(prev):''}</span><span><i style="background:var(--core)"></i>${now?wshort(now):''}</span>${capped?`<span>${L('The "Running government" bars are shortened to fit; the numbers are exact.','أعمدة «تشغيل الجهات الحكومية» مختصرة لتتسع؛ والأرقام دقيقة.')}</span>`:''}</div>`;
}
"""
