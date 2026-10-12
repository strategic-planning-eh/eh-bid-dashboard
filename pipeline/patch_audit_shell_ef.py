"""patch_audit_shell_ef.py — Environment Fund 2025 page: audit fixes shell-01, 02, 08, 09, 14, 15, 17 (12 Oct 2026).

What was wrong, and what changes (the page is written by build_ef_page.py from ef_report_2025.json, so both are edited
and the page is rebuilt):

  shell-01  "EH's own record with the Fund" called 31 logged tenders "EH's bids", counted them as "pending" and asked
            Business Development to chase 24 of them. The bid tracker shows EH submitted on none of them: several were
            declined by EH's own bid committee, some were cancelled, and the rest have no submission recorded.
            The table now has honest columns — Logged / EH submitted / Open now / Declined by EH / Cancelled /
            No submission recorded — and the reading under it is written from those numbers (English and Arabic).
            "Pending" and "Decided" are gone; the value column counts only offers EH actually submitted.
  shell-02  The table was typed into the JSON on 15 Sep and had gone stale (the Wildlife tender closing 18 Oct showed as
            "No tenders"; MWAN 1 instead of 2; the Meteorology tenders were never matched). build_ef_page.py now
            computes the table from the Bid & Tender app's own data when the page is built (bidanalytics2.json, or
            bidraw2.json, from pipeline/run_pipeline.py), using the app's submission rule (bid_analytics2.substate),
            and keeps the last result in ef_xref_snapshot.json. Built without bid data, the page shows that snapshot
            and says how many days old it is. The Meteorology centre's tenders were never matched ("للأرصاد");
            NCW and NCM now have a row each, so an open tender is named by its own centre.
  shell-08  One chart mixed the 123 opportunities (by activity) with a different list of 45 investor opportunities (by
            centre) and drew a conclusion the report does not make. It is now two charts with their own titles; the
            conclusion is dropped.
  shell-09  The programme map started every centre→EH line at the first centre listed, so MWAN, NCW and NCM looked
            unconnected to EH. The map is now laid out centres → programmes → EH service lines: every line is one
            the report states, and no line passes through a box.
  shell-14  "doubled its digital score" — 45 % → 79 % is a rise of three-quarters. Wording corrected (EN + AR).
  shell-15  "Waste tonnage" chart also holds CO₂; "people" chart also holds schools and factories: titles now say what
            is plotted. The facts ledger ("every figure") gains the two headline figures it lacked (SAR 362.3 M, p.18;
            13 regions, p.20). Page references that disagree between chart and ledger (p.100 vs p.106, p.95 vs p.94)
            are NOT changed — the report PDF is not available here to say which is right.
  shell-17  Arabic: ledger categories shown as raw codes (ppp, grantees …) now have names in both languages; values in
            Arabic read "مليون" / "طن" instead of "M" / "t".

Exact-string edits on build_ef_page.py (fail loudly if an anchor is missing); structured edits on the JSON (written
back with the file's own formatting, indent=1). Change table: change_table_audit_shell_ef.md/.json.

Run once:  python3 pipeline/patch_audit_shell_ef.py   then   python3 pipeline/build_ef_page.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import patchlib
from patchlib import load, rep, FILES, FAILURES, write_change_table

B = os.path.join(HERE, 'build_ef_page.py'); J = os.path.join(HERE, 'ef_report_2025.json')
if 'ef_xref_snapshot.json' in open(B, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(B, 'gen')

# =====================================================================================================================
# 1. build_ef_page.py — arguments and the tracker cross-check computed at build time (shell-01, shell-02)
# =====================================================================================================================
rep('gen', '''"""build_ef_page.py — renders hub/environment_fund_2025.html from pipeline/ef_report_2025.json.
Re-run after editing the JSON. The page is self-contained apart from eh-shared.css / eh-shared.js."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'ef_report_2025.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'hub', 'environment_fund_2025.html')
EF = json.load(open(SRC, encoding='utf-8'))
payload''', '''"""build_ef_page.py — renders hub/environment_fund_2025.html from pipeline/ef_report_2025.json.
Re-run after editing the JSON. The page is self-contained apart from eh-shared.css / eh-shared.js.

"EH's own record with the Fund" is computed from the Bid & Tender app's data each time the page is built
(patch_audit_shell_ef.py, 12 Oct 2026): --bids FILE, or by default pipeline/bidanalytics2.json then pipeline/bidraw2.json
(both written by run_pipeline.py). The result is also saved to ef_xref_snapshot.json; when no bid data is present the
page uses that snapshot and shows its age.
Usage: python3 build_ef_page.py [ef_report_2025.json] [out.html] [--bids FILE] [--asof YYYY-MM-DD]"""
import json, os, sys, re, argparse, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
_ap = argparse.ArgumentParser()
_ap.add_argument('src', nargs='?', default=os.path.join(HERE, 'ef_report_2025.json'))
_ap.add_argument('out', nargs='?', default=os.path.join(HERE, '..', 'hub', 'environment_fund_2025.html'))
_ap.add_argument('--bids', default=None, help='bidanalytics2.json or bidraw2.json (default: whichever exists in pipeline/)')
_ap.add_argument('--asof', default=None, help='date of the bid data (default: today in Riyadh)')
_ap.add_argument('--snapshot', default=os.path.join(HERE, 'ef_xref_snapshot.json'))
_a = _ap.parse_args()
SRC, OUT = _a.src, _a.out
EF = json.load(open(SRC, encoding='utf-8'))

# ---- EH's own record with the Fund and the national centres: from the bid tracker, at build time -------------------
def _sub_raw(b, today):
    """Same order as bid_analytics2.substate(): the tracker's submission columns, then offer evidence, then reasons."""
    if b.get('ehsubdate') or b.get('subdate'): return 'date'
    if b.get('substatus') == 'Yes': return 'yes'
    no = b.get('substatus') == 'No'
    if not no and (b.get('eh_won') is True or b.get('ehsub') or b.get('offer')): return 'yes'
    if re.search(r'reject|رفض', b.get('committee') or '', re.I): return 'rejected'
    if (b.get('status') or '') == 'Cancelled': return 'cancelled'
    if no: return 'no'
    if b.get('submit') and b['submit'] >= today: return 'open'
    return 'none' if b.get('subcol') else 'unrecorded'

def _bid_row(b, today):
    if 'outcome' in b:                                   # bid_analytics2.py bid list (what the Bid app shows)
        out, sub, dl = b.get('outcome') or 'Pending', b.get('sub'), b.get('deadline')
        if sub is None:                                  # older bid data without a submission state
            sub = ('rejected' if re.search(r'reject|رفض', b.get('committee') or '', re.I) else
                   'cancelled' if out == 'Cancelled' else 'open' if dl and dl >= today else 'unrecorded')
    else:                                                # extract_bids2.py raw rows
        st = b.get('status') or ''
        out = 'Won' if b.get('eh_won') is True else 'Lost' if b.get('eh_won') is False else 'Cancelled' if st == 'Cancelled' else 'Pending'
        sub, dl = _sub_raw(b, today), b.get('submit')
    if sub in ('date', 'yes'): state = 'submitted'
    elif sub == 'cancelled' or out == 'Cancelled': state = 'cancelled'
    elif sub == 'rejected': state = 'declined'
    elif sub == 'open': state = 'open'
    else: state = 'nosub'
    return {'year': b.get('year'), 'sn': b.get('sn'), 'client': b.get('client') or '', 'title': b.get('title') or '',
            'deadline': dl, 'state': state, 'outcome': out, 'value': (b.get('value') or 0) if state == 'submitted' else 0}

def _xref(bids, today):
    rows, years = [], sorted({b.get('year') for b in bids if b.get('year')})
    for r in EF['xref']['rows']:
        hit = [_bid_row(b, today) for b in bids if re.search(r['match'], str(b.get('client') or ''), re.I)]
        c = {k: sum(1 for h in hit if h['state'] == k) for k in ('submitted', 'open', 'declined', 'cancelled', 'nosub')}
        rows.append(dict(key=r['key'], tenders=len(hit), value=round(sum(h['value'] for h in hit)), **c,
                         won=sum(1 for h in hit if h['state'] == 'submitted' and h['outcome'] == 'Won'),
                         lost=sum(1 for h in hit if h['state'] == 'submitted' and h['outcome'] in ('Lost', 'Not awarded')),
                         open_list=[{'year': h['year'], 'sn': h['sn'], 'deadline': h['deadline'], 'title': h['title'][:90]}
                                    for h in sorted(hit, key=lambda h: h['deadline'] or '') if h['state'] == 'open']))
    return {'as_of': today, 'years': years, 'rows': rows}

_bids_path = _a.bids or next((p for p in (os.path.join(HERE, 'bidanalytics2.json'), os.path.join(HERE, 'bidraw2.json')) if os.path.exists(p)), None)
_today = _a.asof or dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).date().isoformat()
if _bids_path and os.path.exists(_bids_path):
    _j = json.load(open(_bids_path, encoding='utf-8'))
    _x = _xref(_j['both'].get('bidlist', []) if 'both' in _j else _j.get('bids', []), _today)
    json.dump(_x, open(_a.snapshot, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    EF['xref']['live'] = dict(_x, source='live')
    print('EH record with the Fund: computed from', os.path.basename(_bids_path), 'as of', _today)
elif os.path.exists(_a.snapshot):
    EF['xref']['live'] = dict(json.load(open(_a.snapshot, encoding='utf-8')), source='snapshot')
    print('EH record with the Fund: no bid data found — using the snapshot of', EF['xref']['live']['as_of'])
else:
    EF['xref']['live'] = None
    print('EH record with the Fund: no bid data and no snapshot — the section says so')
payload''', 'data', 'shell-02: compute the EH-with-the-Fund table from the bid data at build time (snapshot fallback)')

# ---- the page: table and reading (shell-01)
rep('gen', ''' $('stamp').innerHTML=`<span>${L('Source','المصدر')}: <b>${esc(L(m.source_en,m.source_ar))}</b> (${m.pages} ${L('pages','صفحة')})</span><span>·</span><span>${L('extracted','تاريخ الاستخراج')} <b dir="ltr">${m.extracted}</b></span><span>·</span><span>${L('checked against EH\\'s bid tracker on','مطابقة جدول العطاءات حتى')} <b dir="ltr">${m.tracker_xref_as_of}</b></span>`;''',
    ''' const XL=EF.xref.live;
 $('stamp').innerHTML=`<span>${L('Source','المصدر')}: <b>${esc(L(m.source_en,m.source_ar))}</b> (${m.pages} ${L('pages','صفحة')})</span><span>·</span><span>${L('extracted','تاريخ الاستخراج')} <b>${fmtDay(m.extracted)}</b></span>${XL?`<span>·</span><span>${XL.source==='live'?L('EH\\'s bid tracker read on','قُرئ جدول العطاءات في'):L('EH\\'s bid tracker as of','جدول العطاءات حتى')} <b>${fmtDay(XL.as_of)}</b></span>`:''}`;''',
    'copy', 'shell-02: stamp says when the bid tracker was read (or how old the snapshot is)')

rep('gen', ''' // xref
 const x=EF.xref;
 $('xref').innerHTML=`<h2>${L("EH's own record with the Fund and the national centres","سجل آفاق البيئة مع الصندوق والمراكز الوطنية")}</h2><div class="note">${esc(L(x.note_en,x.note_ar))}</div>
 <table class="t xr"><thead><tr><th>${L('Client','الجهة')}</th><th style="text-align:center">${L('Tenders','منافسات')}</th><th style="text-align:center">${L('Value (SAR)','القيمة (ريال)')}</th><th style="text-align:center">${L('Pending','قيد الانتظار')}</th><th style="text-align:center">${L('Cancelled','ملغاة')}</th><th style="text-align:center">${L('Decided','محسومة')}</th><th>${L('Note','ملاحظة')}</th></tr></thead><tbody>
 ${x.rows.map(r=>`<tr><td><b>${esc(L(r.client_en,r.client_ar))}</b></td><td class="num">${r.tenders}</td><td class="num" dir="ltr">${r.value?fmtM(r.value):'—'}</td><td class="num">${r.pending}</td><td class="num">${r.cancelled}</td><td class="num ${r.tenders&&!r.decided?'zero':''}">${r.decided}</td><td style="color:var(--muted)">${esc(L(r.note_en,r.note_ar))}</td></tr>`).join('')}</tbody></table>
 <div class="read">${esc(L(x.reading_en,x.reading_ar))} ${P(87)}</div>`;''',
    ''' // xref — computed from the bid tracker when the page is built (build_ef_page.py; audit shell-01/02, 12 Oct 2026)
 $('xref').innerHTML=xrefHTML();''', 'copy', 'shell-01: honest table columns and a reading written from the numbers')

rep('gen', '''// EH design system v2 (patch_design_ef.py): brand palette (land → sea) for the colours stored in the report data''',
    '''// "EH's own record with the Fund": a tender logged in the tracker is not an EH bid — the columns say what happened to each
function xrefHTML(){
 const x=EF.xref, X=x.live, h=`<h2>${L("EH's own record with the Fund and the national centres","سجل آفاق البيئة مع الصندوق والمراكز الوطنية")}</h2>`;
 if(!X||!X.rows)return h+`<div class="note">${L('The bid tracker was not available when this page was built, so this record cannot be shown here. The Bid & Tender tab has every tender.','لم يكن جدول العطاءات متاحاً عند بناء هذه الصفحة، فلا يمكن عرض هذا السجل هنا. تبويب المناقصات والعطاءات يعرض كل المنافسات.')}</div>`;
 const R=X.rows.map(r=>Object.assign({},x.rows.find(d=>d.key===r.key)||{},r)), K=['tenders','submitted','open','declined','cancelled','nosub','value'];
 const T={};K.forEach(k=>T[k]=R.reduce((a,r)=>a+(r[k]||0),0));
 const yrs='\u2066'+((X.years||[]).length>1?X.years[0]+'–'+X.years[X.years.length-1]:String((X.years||[''])[0]))+'\u2069';   // isolated so Arabic keeps 2025–2026 in order
 const age=Math.floor((Date.now()-new Date(X.as_of+'T12:00:00+03:00'))/864e5);
 const when=X.source==='live'?L(`Read from the tracker on ${fmtDay(X.as_of)}.`,`قُرئ من الجدول في ${fmtDay(X.as_of)}.`)
   :L(`Snapshot of the tracker taken on ${fmtDay(X.as_of)}${age>1?` — ${age} days old`:''}.`,`لقطة من الجدول بتاريخ ${fmtDay(X.as_of)}${age>1?` — مضى عليها ${age} يوماً`:''}.`);
 const sn=o=>`${o.sn}/${String(o.year).slice(2)}`;
 const ltr=h=>h.replace(/\u2066(.*?)\u2069/g,'<span dir="ltr">$1</span>');   // Chromium ignores isolate characters in text: use a real LTR span
 const openTxt=o=>L(`${sn(o)} closes ${fmtDay(o.deadline)}`,`رقم ${sn(o)} يُغلق ${fmtDay(o.deadline)}`);
 const note=r=>{const a=[];if(r.submitted)a.push(L(`Submitted: ${[r.won?r.won+' won':'',r.lost?r.lost+' lost':'',r.submitted-r.won-r.lost?(r.submitted-r.won-r.lost)+' awaiting a result':''].filter(Boolean).join(', ')}`,`قُدِّم: ${[r.won?r.won+' فازت':'',r.lost?r.lost+' لم تُرسَ':'',r.submitted-r.won-r.lost?(r.submitted-r.won-r.lost)+' بانتظار النتيجة':''].filter(Boolean).join('، ')}`));
  if(r.open_list&&r.open_list.length)a.push(L('Open: ','مفتوحة: ')+r.open_list.map(openTxt).join(L('; ','؛ ')));
  if(!r.tenders)a.push(L('No tenders logged','لا منافسات مسجَّلة'));else if(r.note_en)a.push(L(r.note_en,r.note_ar));return esc(a.join(L(' · ',' · ')));};
 const th=(en,ar,c)=>`<th${c?' style="text-align:center"':''}>${L(en,ar)}</th>`, td=v=>`<td class="num">${v}</td>`;
 // the reading: every number comes from the table above it
 const was=(n,en1,enN)=>n===1?en1:enN;
 const ow=[];if(T.declined)ow.push(L(`${T.declined} ${was(T.declined,'was','were')} declined by EH's bid committee`,`رفضت لجنة العطاءات في آفاق البيئة ${T.declined}`));
 if(T.cancelled)ow.push(L(`${T.cancelled} ${was(T.cancelled,'was','were')} cancelled`,`أُلغيت ${T.cancelled}`));
 if(T.nosub)ow.push(L(`${T.nosub} passed ${was(T.nosub,'its','their')} deadline with no decision or submission recorded`,`انقضى موعد ${T.nosub} دون تسجيل قرار أو تقديم`));
 const join=a=>a.length<2?(a[0]||''):a.slice(0,-1).join(L(', ','، '))+L(' and ','، و')+a[a.length-1];
 const opens=R.flatMap(r=>(r.open_list||[]).map(o=>L(`${r.client_en} ${openTxt(o)}`,`${r.client_ar} ${openTxt(o)}`)));
 const rd=[L(`${T.tenders} tenders from the Fund and the national centres are logged in EH's bid tracker (${yrs}).`,`${T.tenders} منافسة من الصندوق والمراكز الوطنية مسجَّلة في جدول تتبع العطاءات لآفاق البيئة (${yrs}).`),
  T.submitted?L(`EH submitted an offer on ${T.submitted} of them.`,`قدّمت آفاق البيئة عرضاً في ${T.submitted} منها.`)
   :L('EH submitted an offer on none of them, so there is no EH bid here waiting for a decision.','لم تقدّم آفاق البيئة عرضاً في أيٍّ منها، فلا يوجد هنا عطاء لآفاق البيئة ينتظر قراراً.'),
  ow.length?(s=>s.charAt(0).toUpperCase()+s.slice(1))(join(ow))+L('.','.'):'',
  opens.length?L(`Still open: ${opens.join('; ')}. Decide whether to bid before ${was(opens.length,'it closes','they close')}.`,`ما تزال مفتوحة: ${opens.join('؛ ')}. يلزم تقرير التقدّم من عدمه قبل الإغلاق.`):'',
  T.nosub?L(`Ask the bid team to record the committee decision and the submission status on the ${T.nosub} without one, so this record stays accurate.`,`يُرجى أن يسجّل فريق العطاءات قرار اللجنة وحالة التقديم في ${T.nosub} منافسة ينقصها ذلك، ليبقى هذا السجل دقيقاً.`):''].filter(Boolean).join(' ');
 return h+`<div class="note">${ltr(esc(L(`Every tender from the Fund and the national centres that is logged in EH's bid tracker (EH-WIN-02-F01), ${yrs}. A tender is logged when EH looks at it — that does not mean EH bid. "Submitted" follows the same rule as the Bid & Tender tab.`,`كل منافسة من الصندوق والمراكز الوطنية مسجَّلة في جدول تتبع العطاءات لآفاق البيئة (EH-WIN-02-F01)، ${yrs}. تُسجَّل المنافسة عندما تطّلع عليها آفاق البيئة — ولا يعني ذلك أنها تقدّمت لها. «قُدِّم» وفق القاعدة نفسها في تبويب المناقصات والعطاءات.`)))} ${esc(when)}</div>
 <table class="t xr"><thead><tr>${th('Client','الجهة')}${th('Logged','مسجَّلة',1)}${th('EH submitted','قدّمت آفاق البيئة',1)}${th('Open now','مفتوحة الآن',1)}${th('Declined by EH','رفضتها لجنة آفاق البيئة',1)}${th('Cancelled','ملغاة',1)}${th('No submission recorded','لا تقديم مسجَّل',1)}${th("Value of EH's offers (SAR)",'قيمة عروض آفاق البيئة (ريال)',1)}${th('Note','ملاحظة')}</tr></thead><tbody>
 ${R.map(r=>`<tr><td><b>${esc(L(r.client_en,r.client_ar))}</b></td>${td(r.tenders)}${td(r.submitted)}${td(r.open?`<b>${r.open}</b>`:0)}${td(r.declined)}${td(r.cancelled)}${td(r.nosub)}<td class="num" dir="ltr">${r.value?fmtM(r.value):'—'}</td><td style="color:var(--muted)">${note(r)}</td></tr>`).join('')}
 <tr><td><b>${L('Total','المجموع')}</b></td>${['tenders','submitted','open','declined','cancelled','nosub'].map(k=>td(`<b>${T[k]}</b>`)).join('')}<td class="num" dir="ltr"><b>${T.value?fmtM(T.value):'—'}</b></td><td></td></tr></tbody></table>
 <div class="read">${ltr(esc(rd))}</div>`;
}
// EH design system v2 (patch_design_ef.py): brand palette (land → sea) for the colours stored in the report data''',
    'copy', 'shell-01: xrefHTML() — columns Logged / Submitted / Open / Declined / Cancelled / No submission; reading from the numbers')

rep('gen', """.xr td.num{text-align:center;font-variant-numeric:tabular-nums}.xr .zero{color:var(--red);font-weight:700}""",
    """.xr td.num{text-align:center;font-variant-numeric:tabular-nums}.xr .zero{color:var(--red);font-weight:700}.xr td:first-child{min-width:150px}.xr td:last-child{min-width:260px}""",
    'css', 'shell-01: on phones the wider table scrolls inside its panel instead of squeezing names into one-word lines')

# ---- Arabic units and dates (shell-17)
rep('gen', '''const fmtM=v=>v>=1e6?(v/1e6).toFixed(1).replace(/\\.0$/,'')+' M':v>=1e3?(v/1e3).toFixed(0)+' K':String(v);''',
    '''const fmtM=v=>v>=1e6?(v/1e6).toFixed(1).replace(/\\.0$/,'')+L(' M',' مليون'):v>=1e3?(v/1e3).toFixed(0)+L(' K',' ألف'):String(v);
const fmtDay=iso=>{const d=new Date(String(iso||'')+'T12:00:00');return isNaN(d)?String(iso||''):d.toLocaleDateString(LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB',{day:'numeric',month:'short',year:'numeric'});};   // Gregorian in both languages, as across the hub
const CAT={ppp:['Partnerships & privatisation','الشراكة والتخصيص'],grantees:['Grant recipients','المستفيدون من المنح'],finance:['Finance','المالية'],impact:['Impact investment','استثمارات الأثر'],shared:['Shared services','الخدمات المشتركة'],grants:['Grants','المنح'],portfolio:['Portfolio','المحفظة'],fees:['Fees','المقابل المالي'],carbon:['Carbon','الكربون'],mandate:['Mandate','المهام'],products:['Products','المنتجات'],esg:['Sustainability reporting','تقارير الاستدامة'],people:['People','الموارد البشرية'],strategy:['Strategy','الاستراتيجية'],digital:['Digital','التحول الرقمي'],comms:['Communications','الاتصال'],headline:['Headline figure','رقم رئيسي']};''',
    'copy', 'shell-17: Arabic units (مليون/ألف), Gregorian dates, ledger category names')
rep('gen', '''<td style="color:var(--muted);white-space:nowrap">${esc(f.cat)}</td>''',
    '''<td style="color:var(--muted);white-space:nowrap">${esc(L(...(CAT[f.cat]||[f.cat,f.cat])))}</td>''',
    'copy', 'shell-17: facts ledger shows category names, not codes')
rep('gen', '''${r.v.toLocaleString('en-US')}${c.pct?'%':c.unit==='t'?' t':''}''',
    '''${r.v.toLocaleString('en-US')}${c.pct?'%':c.unit==='t'?L(' t',' طن'):''}''',
    'copy', 'shell-17: tonnes read "طن" in Arabic charts')

# ---- programme map: centres → programmes → EH lines (shell-09)
rep('gen', ''' const xP=40,xC=W/2-40,xE=W-300, bw=[310,150,200];   // EH design v2: programme and centre boxes wide enough for the longest label (English and Arabic) in the brand font''',
    ''' const xC=40,xP=W/2-155,xE=W-240, bw=[310,150,200];   // audit shell-09: centres | programmes | EH lines — every line is a link the report states, none crosses a box''',
    'code', 'shell-09: centres on the left, programmes in the middle, EH lines on the right')
rep('gen', ''' <text x="${xP}" y="24" font-size="15" font-weight="800" fill="var(--eh-ink)">${esc(L("Environment Fund programmes → national centres they touch → EH service lines they concern","برامج الصندوق ← المراكز الوطنية التي تمسّها ← خطوط خدمات آفاق البيئة المعنية"))}</text>
 <text x="${xP}" y="42" font-size="11" fill="var(--eh-ink-3)">''',
    ''' <text x="${xC}" y="24" font-size="15" font-weight="800" fill="var(--eh-ink)">${esc(L("National centres → the Environment Fund programmes that touch them → EH service lines they concern","المراكز الوطنية ← برامج الصندوق التي تمسّها ← خطوط خدمات آفاق البيئة المعنية"))}</text>
 <text x="${xC}" y="42" font-size="11" fill="var(--eh-ink-3)">''', 'copy', 'shell-09: map title follows the new left-to-right order')
rep('gen', ''' prods.forEach((p,i)=>{p.centres.forEach(c=>{const j=cen.findIndex(x=>x[0]===c);if(j<0)return;s+=`<path d="M${xP+bw[0]} ${yP(i)+14} C ${xP+bw[0]+90} ${yP(i)+14}, ${xC-90} ${yC(j)+14}, ${xC} ${yC(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});
  p.eh.forEach(e=>{const j=ehl.findIndex(x=>x[0]===e);if(j<0)return;const x0=p.centres.length?xC+bw[1]:xP+bw[0];const y0=p.centres.length?yC(cen.findIndex(x=>x[0]===p.centres[0]))+14:yP(i)+14;s+=`<path d="M${x0} ${y0} C ${x0+90} ${y0}, ${xE-90} ${yE(j)+14}, ${xE} ${yE(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});});''',
    ''' prods.forEach((p,i)=>{p.centres.forEach(c=>{const j=cen.findIndex(x=>x[0]===c);if(j<0)return;const x0=xC+bw[1],x1=xP;s+=`<path d="M${x0} ${yC(j)+14} C ${x0+80} ${yC(j)+14}, ${x1-80} ${yP(i)+14}, ${x1} ${yP(i)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});
  p.eh.forEach(e=>{const j=ehl.findIndex(x=>x[0]===e);if(j<0)return;const x0=xP+bw[0];s+=`<path d="M${x0} ${yP(i)+14} C ${x0+70} ${yP(i)+14}, ${xE-70} ${yE(j)+14}, ${xE} ${yE(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});});''',
    'code', 'shell-09: lines run centre → programme and programme → EH line only (no line starts at "the first centre")')

# =====================================================================================================================
# 2. ef_report_2025.json — xref rows (match patterns, no typed counts), charts and ledger
# =====================================================================================================================
EF = json.load(open(J, encoding='utf-8')); JLOG = []
def jlog(note, old, new):
    JLOG.append(note); patchlib.CHANGES.append({'file': 'json', 'kind': 'json', 'category': 'copy', 'note': note, 'occurrences': 1,
                                                'ok': True, 'old': json.dumps(old, ensure_ascii=False)[:400], 'new': json.dumps(new, ensure_ascii=False)[:400]})
old_x = EF['xref']
MATCH = [('fund', r'صندوق البيئة|Environment(al)? Fund'), ('ncec', r'المركز الوطني للرقابة|الالتزام البيئي|NCEC'),
         ('ncvc', r'الغطاء النباتي|NCVC'), ('mwan', r'المركز الوطني لإدارة النفايات|موان|MWAN'),
         ('ncw', r'الحياة الفطرية|NCW'), ('ncm', r'[اأ]رصاد|NCM'), ('mewa', r'وزارة البيئة|MEWA')]
NOTES = {'fund': ('Tender 17/26 — sustainability consulting for the national centres', 'المنافسة 17/26 — خدمات استشارية للمعايير البيئية والاجتماعية للمراكز'),
         'mwan': ('Incl. the national digital waste-management platform (29/26)', 'منها المنصة الرقمية الوطنية لإدارة النفايات (29/26)'),
         'ncw': ('', ''), 'ncm': ('', ''), 'mewa': ('', '')}
# the old combined "NCW · NCM" row becomes two rows, so an open tender is named by its own centre
OLD = {'fund': 0, 'ncec': 1, 'ncvc': 2, 'mwan': 3, 'mewa': 5}
NAMES = {'ncw': ('NCW (Wildlife)', 'المركز الوطني لتنمية الحياة الفطرية'), 'ncm': ('NCM (Meteorology)', 'المركز الوطني للأرصاد')}
rows = []
for key, pat in MATCH:
    r = old_x['rows'][OLD[key]] if key in OLD else {'client_en': NAMES[key][0], 'client_ar': NAMES[key][1], 'note_en': '', 'note_ar': ''}
    ne, na = NOTES.get(key, (r['note_en'], r['note_ar']))
    rows.append({'key': key, 'client_en': r['client_en'], 'client_ar': r['client_ar'], 'match': pat, 'note_en': ne, 'note_ar': na})
new_x = {'how_en': "Counts are computed from the bid tracker each time the page is built (build_ef_page.py); a row matches a tender by the client name pattern in 'match'.",
         'rows': rows}
EF['xref'] = new_x
jlog('shell-01/02: xref keeps client names and match patterns only — counts, "pending" and the reading are computed', old_x, new_x)
old = EF['meta'].pop('tracker_xref_as_of'); jlog('shell-02: meta.tracker_xref_as_of removed (the date now comes from the bid data)', old, None)

ch = {c['id']: c for c in EF['charts']}
a = ch['c-activity']; old = dict(a)
inv = {'id': 'c-investors', 'type': 'hbar',
       'title_en': 'Opportunities to attract private investors — by centre',
       'title_ar': 'فرص جذب المستثمرين من القطاع الخاص — حسب المركز',
       'sub_en': '45 opportunities listed by three centres. This is a different list from the 123 above, and the report does not say how the two overlap',
       'sub_ar': '45 فرصة أدرجتها ثلاثة مراكز. هذه قائمة مختلفة عن الفرص الـ123 أعلاه، ولا يذكر التقرير كيف تتداخل القائمتان',
       'pages': [76], 'color': '#1F7A4C',
       'rows': [{'en': 'NCVC (Vegetation Cover)', 'ar': 'المركز الوطني لتنمية الغطاء النباتي', 'v': 25, 'p': 76},
                {'en': 'NCW (Wildlife)', 'ar': 'المركز الوطني لتنمية الحياة الفطرية', 'v': 16, 'p': 76},
                {'en': 'MWAN (Waste Management)', 'ar': 'المركز الوطني لإدارة النفايات', 'v': 4, 'p': 76}]}
a.update({'title_en': 'Where the 123 opportunities sit — by activity', 'title_ar': 'أين تقع الفرص الـ123 — حسب النشاط',
          'sub_en': 'Waste is two-thirds of the 123 investment opportunities the Fund reviewed; the report does not list them',
          'sub_ar': 'النفايات ثلثا الفرص الاستثمارية الـ123 التي استعرضها الصندوق؛ ولا يسرد التقرير هذه الفرص',
          'pages': [83], 'rows': [r for r in a['rows'] if r['p'] == 83]})
EF['charts'].insert(EF['charts'].index(a) + 1, inv)
jlog('shell-08: "123 opportunities" chart split — activity (123, p.83) and investor opportunities by centre (45, p.76); inference dropped', old, [a, inv])

c = ch['c-capability']; old = (c['sub_en'], c['sub_ar'])
assert 'doubled its digital score' in c['sub_en'] and 'وضاعفت نتيجتها الرقمية' in c['sub_ar']
c['sub_en'] = c['sub_en'].replace('doubled its digital score', 'raised its digital score by three-quarters (45 % → 79 %)')
c['sub_ar'] = c['sub_ar'].replace('وضاعفت نتيجتها الرقمية', 'ورفعت نتيجتها الرقمية بنحو ثلاثة أرباع (من 45% إلى 79%)')
jlog('shell-14: "doubled" → "raised by three-quarters (45 % → 79 %)"', old, (c['sub_en'], c['sub_ar']))

w = ch['c-waste']; old = (w['title_en'], w['title_ar'], w['sub_en'], w['sub_ar'])
w['title_en'] = "What the Fund's 2025 grants put in motion — tonnes of waste, and CO₂ avoided"
w['title_ar'] = 'ما حرّكته منح الصندوق في 2025 — أطنان النفايات، والانبعاثات المخفَّضة'
w['sub_en'] = 'Three private projects plus one public initiative; company names not disclosed in the report. Whole-programme totals and a yearly rate are shown together — each label says which'
w['sub_ar'] = 'ثلاثة مشاريع خاصة ومبادرة عامة؛ أسماء الشركات غير مذكورة في التقرير. تُعرض الإجماليات ومعدل سنوي معاً — وكل تسمية توضّح أيّهما'
jlog('shell-15: waste chart title names the CO₂ bar and the mixed totals / yearly rate', old, (w['title_en'], w['title_ar'], w['sub_en'], w['sub_ar']))
g = ch['c-grants']; old = (g['title_en'], g['title_ar'])
g['title_en'] = "Grant programme reach in 2025 — people, schools and factories the Fund's initiatives touched"
g['title_ar'] = 'مدى وصول برنامج المنح في 2025 — الأفراد والمدارس والمصانع التي طالتها مبادرات الصندوق'
jlog('shell-15: reach chart title names schools and factories', old, (g['title_en'], g['title_ar']))

H = {h['id']: h for h in EF['headline']}
add = [{'id': 'f51', 'page': 18, 'cat': 'headline', 'en': 'SAR 362.3 million — ' + H['h1']['en'], 'ar': '362.3 مليون ريال — ' + H['h1']['ar']},
       {'id': 'f52', 'page': 20, 'cat': 'headline', 'en': '24 initiatives supported in 13 regions, SAR 17 million+ in grants', 'ar': '24 مبادرة مدعومة في 13 منطقة، و+17 مليون ريال من المنح'}]
assert not any(f['id'] in ('f51', 'f52') for f in EF['facts'])
EF['facts'] += add
jlog('shell-15: ledger gains the two headline figures it lacked (p.18, p.20)', None, add)

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(B, 'w', encoding='utf-8').write(FILES['gen'])
open(J, 'w', encoding='utf-8').write(json.dumps(EF, ensure_ascii=False, indent=1))
write_change_table(os.path.join(HERE, 'change_table_audit_shell_ef'), 'Environment Fund page — audit fixes shell-01/02/08/09/14/15/17')
print('patched: build_ef_page.py (%d edits), ef_report_2025.json (%d edits)' % (len(patchlib.CHANGES) - len(JLOG), len(JLOG)))
print('next: python3 pipeline/build_ef_page.py   (uses pipeline/bidanalytics2.json or bidraw2.json if present, else ef_xref_snapshot.json)')
