"""patch_audit_macro_fisc.py — audit fixes for the Saudi Government Finances page (12 Oct 2026, judge J3, ids macro-05,
macro-11, macro-12, macro-13, macro-14).

What was wrong and what changes:
  • macro-05 — Arabic, section 04 table: the 2024 and 2025 "plan → actual" cells kept the English arrow "→". In a
    right-to-left line that arrow points from the actual figure back to the plan, so those rows read backwards against
    the column heading "الخطة ← الفعلي" (the 2026 row was already right). The six cells now have Arabic versions with
    "←". (They hold no letters, so eh-ar-dashboard.js is also taught to swap such cells — see patch_audit_macro_ardash.py.)
  • macro-11 — Arabic, chart E and the chart tooltips: the event markers on the oil-price chart ("War · 28 Feb" …) and
    the tooltip lines ("SAR … billion", "Change on a year earlier", "Official Ministry of Finance figure" …) stayed in
    English. Each marker and tooltip now has an Arabic version used when the page is in Arabic. The last marker
    ("Pipeline hit · …") ran into the worst-case line and the right edge; it now sits to the left of its line, one row
    lower, so it no longer collides with the other labels.
  • macro-12 — Arabic key-figure cards showed "245B", "191B", "1,685B"; they now read "مليار ريال". "~10" no longer
    flips to "10~" (it is isolated left to right).
  • macro-13 — three labels: the debt card cited the "borrowing plan for 2027" although the SAR 1,685 billion comes
    from the Ministry's April–June 2026 budget performance report (30/07); the card "Size of the economy, 2026" shows
    the growth rate (−3.6%), so it is now "Economic growth, 2026"; the chart E reference line said "Price the budget
    assumed" although the Ministry publishes no oil-price assumption — it is now named as EH's reference (the 2025
    average Brent price, $69.9). EN and AR. (The fourth sub-point, "we do not go lower than the Ministry", was not
    reproduced by the judge and is unchanged.)
  • macro-14 — chart A: the January–June 2025 bars were worked back from percentages (other income 264.6, total
    566.1). The Ministry published the actual figures: total 565.21, oil 301.54, other 263.67 (SAR billion). The bars
    now use them; the rounded % changes are unchanged (+9%, +2%, +6%). The source line now cites both reports.

The Arabic dictionary lives twice — embedded in the page (<script id="ehArFull">) and in saudi_fiscal_monitor_2026.ar.json —
and both are rewritten from the same dict in their existing formats, so they stay identical.

Exact-string edits; stops if an anchor is missing.   Run once:  python3 pipeline/patch_audit_macro_fisc.py
"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table, _log

HUB = os.path.join(HERE, '..', 'hub')
P = os.path.join(HUB, 'saudi_fiscal_monitor_2026.html')
J = os.path.join(HUB, 'saudi_fiscal_monitor_2026.ar.json')
if 'EH_AR_TIP' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'fisc')

# ---------------------------------------------------------------- macro-13: KPI labels and source
rep('fisc', "{label:'Size of the economy, 2026', val:'\\u22123.6'", "{label:'Economic growth, 2026', val:'\\u22123.6'",
    'copy', 'macro-13: KPI "Size of the economy" shows a growth rate — renamed "Economic growth, 2026"')
rep('fisc', "src:'Ministry of Finance \\u00b7 borrowing plan for 2027 due by year-end'}",
    "src:'Ministry of Finance \\u00b7 budget performance report for April\\u2013June 2026 (30/07)'}",
    'copy', 'macro-13: debt KPI cites the report the figure comes from')
OLD_REF = "{label:'Price the budget assumed ($69.9, 2025 average)', data:budgetRef"
NEW_REF = "{label:'EH reference: 2025 average price ($69.9) \\u2014 the Ministry publishes no oil-price assumption', data:budgetRef"
rep('fisc', OLD_REF, NEW_REF, 'copy', 'macro-13: chart E reference line is EH\'s proxy, not a Ministry assumption')

# ---------------------------------------------------------------- macro-14: chart A 2025 base
rep('fisc', "{label:'Jan–Jun 2025', data:[301.5,264.6,566.1]", "{label:'Jan–Jun 2025', data:[301.5,263.7,565.2]",
    'data', 'macro-14: Jan–Jun 2025 income = Ministry figures (oil 301.54, other 263.67, total 565.21)')
OLD_SRC = ('<div class="csrc"><span class="tag off">Source</span> Ministry of Finance — budget performance report for '
           'April–June 2026 (30/07/2026). The 2025 figures are worked back from the percentage changes the Ministry published.</div>')
NEW_SRC = ('<div class="csrc"><span class="tag off">Source</span> Ministry of Finance — budget performance reports for '
           'April–June 2026 (30/07/2026) and April–June 2025 (January–June 2025 figures).</div>')
rep('fisc', OLD_SRC, NEW_SRC, 'copy', 'macro-14: chart A source cites the published 2025 figures')

# ---------------------------------------------------------------- macro-11: Arabic tooltips and markers
rep('fisc', "/* vertical event-marker plugin (no external dep) */",
    "/* audit 12/10 (macro-11): Arabic tooltips and marker labels — the page language decides at draw time */\n"
    "const EH_AR_TIP=()=>document.documentElement.lang==='ar';\n"
    "const L=(en,ar)=>EH_AR_TIP()?ar:en;\n"
    "/* vertical event-marker plugin (no external dep) */",
    'code', 'macro-11: language helper for tooltips and markers')
rep('fisc', "ctx.fillText(m.label, xp+(m.align==='right'?-6:6), top+(m.yOff||12));",
    "ctx.fillText((EH_AR_TIP()&&m.ar)||m.label, xp+(m.align==='right'?-6:6), top+(m.yOff||12));",
    'code', 'macro-11: markers draw their Arabic label in Arabic')
# chart A
rep('fisc', "label:c=>`${c.dataset.label}: SAR ${FMT(c.parsed.y)} billion`,\n      afterBody:(items)=>{const ch=['Oil: +9% (Apr–Jun alone: +22%)','Other: +2%','Total: +6%'];return '\\nChange on a year earlier → '+ch[items[0].dataIndex];}",
    "label:c=>L(`${c.dataset.label}: SAR ${FMT(c.parsed.y)} billion`,`${c.dataset.label}: ${FMT(c.parsed.y)} مليار ريال`),\n"
    "      afterBody:(items)=>{const ch=L(['Oil: +9% (Apr–Jun alone: +22%)','Other: +2%','Total: +6%'],['النفط: +9% (أبريل–يونيو وحده: +22%)','الدخل الآخر: +2%','الإجمالي: +6%']);return L('\\nChange on a year earlier → ','\\nالتغير عن العام السابق: ')+ch[items[0].dataIndex];}",
    'code', 'macro-11: chart A tooltip in Arabic')
# chart B
rep('fisc', "label:c=>`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,\n      afterBody:(items)=>{const q1=",
    "label:c=>L(`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,`${c.dataset.label}: ${FMT(c.parsed.x)} مليار ريال`),\n      afterBody:(items)=>{const q1=",
    'code', 'macro-11: chart B tooltip value in Arabic')
rep('fisc', "let s='\\nJan–Mar vs a year earlier: '+q1[i];if(q2[i]!==undefined)s+='  ·  Apr–Jun: '+q2[i];return s;}",
    "let s=L('\\nJan–Mar vs a year earlier: ','\\nيناير–مارس مقارنة بالعام السابق: ')+q1[i];if(q2[i]!==undefined)s+=L('  ·  Apr–Jun: ','  ·  أبريل–يونيو: ')+q2[i];return s;}",
    'code', 'macro-11: chart B tooltip comparison in Arabic')
# chart C
rep('fisc', "label:c=>`Gap: SAR ${FMT(Math.abs(c.parsed.y))} billion`,\n        afterLabel:c=>{const p=['Before the war · oil $75, OPEC+ holding back production','Before the war · normal quarter','War, Jan–Mar · record gap; spending +20%','War, Apr–Jun · higher oil income arrives; spending +11%'];return p[c.dataIndex];}",
    "label:c=>L(`Gap: SAR ${FMT(Math.abs(c.parsed.y))} billion`,`الفجوة: ${FMT(Math.abs(c.parsed.y))} مليار ريال`),\n"
    "        afterLabel:c=>{const p=L(['Before the war · oil $75, OPEC+ holding back production','Before the war · normal quarter','War, Jan–Mar · record gap; spending +20%','War, Apr–Jun · higher oil income arrives; spending +11%'],"
    "['قبل الحرب · النفط 75 دولارًا وأوبك+ تقيّد الإنتاج','قبل الحرب · ربع اعتيادي','الحرب، يناير–مارس · فجوة قياسية؛ الإنفاق +20%','الحرب، أبريل–يونيو · وصول دخل نفطي أعلى؛ الإنفاق +11%']);return p[c.dataIndex];}",
    'code', 'macro-11: chart C tooltip in Arabic')
# chart D
rep('fisc', "label:c=>`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,\n      afterBody:items=>{const i=items[0].dataIndex;return `\\nJan–Mar vs a year earlier: ${secYoY[i]}  ·  Jan–Mar used ${secPct[i]} of the year's budget (Ministry of Finance)`;} }}},",
    "label:c=>L(`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,`${c.dataset.label}: ${FMT(c.parsed.x)} مليار ريال`),\n"
    "      afterBody:items=>{const i=items[0].dataIndex;return L(`\\nJan–Mar vs a year earlier: ${secYoY[i]}  ·  Jan–Mar used ${secPct[i]} of the year's budget (Ministry of Finance)`,`\\nيناير–مارس مقارنة بالعام السابق: ${secYoY[i]}  ·  استُخدم في يناير–مارس ${secPct[i]} من ميزانية السنة (وزارة المالية)`);} }}},",
    'code', 'macro-11: chart D tooltip in Arabic')
# chart E
rep('fisc', "tooltip:{callbacks:{label:c=>c.parsed.y==null?null:`${c.dataset.label}: $${c.parsed.y} a barrel`}},",
    "tooltip:{callbacks:{label:c=>c.parsed.y==null?null:L(`${c.dataset.label}: $${c.parsed.y} a barrel`,`${c.dataset.label}: ${c.parsed.y} دولارًا للبرميل`)}},",
    'code', 'macro-11: chart E tooltip in Arabic')
OLD_MK = """        {x:1.5,label:'War · 28 Feb',color:C.red},
        {x:3.2,label:'Ceasefire · 8 Apr',color:C.greyd,yOff:26},
        {x:4.4,label:'UAE exits OPEC · May',color:C.blued,yOff:12},
        {x:6.2,label:'Fighting restarts · 8 Jul',color:C.red,yOff:26},
        {x:6.8,label:'Red Sea attacks · 25 Jul',color:'#8B0000',yOff:42},
        {x:8.3,label:'Pipeline hit · Houthis take Bab el-Mandeb · 10–11 Sep',color:'#8B0000',yOff:12}"""
NEW_MK = """        {x:1.5,label:'War · 28 Feb',ar:'الحرب · 28 فبراير',color:C.red},
        {x:3.2,label:'Ceasefire · 8 Apr',ar:'وقف إطلاق النار · 8 أبريل',color:C.greyd,yOff:26},
        {x:4.4,label:'UAE exits OPEC · May',ar:'الإمارات تغادر أوبك · مايو',color:C.blued,yOff:12},
        {x:6.2,label:'Fighting restarts · 8 Jul',ar:'استئناف القتال · 8 يوليو',color:C.red,yOff:26},
        {x:6.8,label:'Red Sea attacks · 25 Jul',ar:'هجمات البحر الأحمر · 25 يوليو',color:'#8B0000',yOff:42},
        {x:8.3,label:'Pipeline hit · Houthis take Bab el-Mandeb · 10–11 Sep',ar:'ضرب خط الأنابيب · الحوثيون يسيطرون على باب المندب · 10–11 سبتمبر',color:'#8B0000',yOff:58,align:'right'}"""
rep('fisc', OLD_MK, NEW_MK, 'code', 'macro-11: Arabic marker labels; last marker moved left of its line and one row down (no collision)')
# chart F
rep('fisc', "label:c=>c.parsed.y==null?null:`${c.dataset.label}: SAR ${FMT(Math.abs(c.parsed.y))} billion so far this year`,\n        footer:items=>{const i=items[0].dataIndex; return i<=1?'Official Ministry of Finance figure':(i===3?'Year-end: Ministry estimate, or the middle of the range for an EH path':'End of September: EH illustration');}",
    "label:c=>c.parsed.y==null?null:L(`${c.dataset.label}: SAR ${FMT(Math.abs(c.parsed.y))} billion so far this year`,`${c.dataset.label}: ${FMT(Math.abs(c.parsed.y))} مليار ريال منذ بداية العام`),\n"
    "        footer:items=>{const i=items[0].dataIndex; return i<=1?L('Official Ministry of Finance figure','رقم رسمي من وزارة المالية'):(i===3?L('Year-end: Ministry estimate, or the middle of the range for an EH path','نهاية العام: تقدير الوزارة، أو منتصف النطاق لمسار آفاق البيئة'):L('End of September: EH illustration','نهاية سبتمبر: توضيح من آفاق البيئة'));}",
    'code', 'macro-11: chart F tooltip in Arabic')
# chart G
rep('fisc', "tooltip:{callbacks:{label:c=>c.parsed.y==null?null:`${c.dataset.label}: ${c.parsed.y>0?'surplus':'gap'} SAR ${FMT(Math.abs(c.parsed.y))} billion`}} },",
    "tooltip:{callbacks:{label:c=>c.parsed.y==null?null:L(`${c.dataset.label}: ${c.parsed.y>0?'surplus':'gap'} SAR ${FMT(Math.abs(c.parsed.y))} billion`,`${c.dataset.label}: ${c.parsed.y>0?'فائض':'فجوة'} ${FMT(Math.abs(c.parsed.y))} مليار ريال`)}} },",
    'code', 'macro-11: chart G tooltip in Arabic')

# ---------------------------------------------------------------- Arabic dictionary (embedded + .ar.json)
m = re.search(r'(<script type="application/json" id="ehArFull">)(.*?)(</script>)', FILES['fisc'], re.S)
raw = m.group(2); emb = json.loads(raw)
emb_fmt = lambda d: json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
assert emb_fmt(emb) == raw, 'embedded dictionary format changed — refusing to rewrite'
jtxt = open(J, encoding='utf-8').read(); js = json.loads(jtxt)
assert js == emb, 'ar.json and the embedded dictionary differ — refusing to rewrite'
assert json.dumps(js, ensure_ascii=False, indent=0) == jtxt, 'ar.json format changed — refusing to rewrite'

def rename(d, old, new_key, new_val, note):
    ok = old in d and new_key not in d
    if ok:
        items = [(new_key, new_val) if k == old else (k, v) for k, v in d.items()]
        d.clear(); d.update(items)
    _log('fisc', 'dict', old, new_key + ' => ' + new_val, 'copy', note, int(old in d or ok), ok)
def add(d, key, val, note):
    ok = key not in d
    if ok: d[key] = val
    _log('fisc', 'dict', key, val, 'copy', note, 0 if ok else 1, ok)

d = emb
rename(d, '<span class="klabel">Size of the economy, 2026</span>', '<span class="klabel">Economic growth, 2026</span>',
       '<span class="klabel">النمو الاقتصادي، 2026</span>', 'macro-13: AR label "Economic growth, 2026"')
rename(d, 'Ministry of Finance · borrowing plan for 2027 due by year-end',
       'Ministry of Finance · budget performance report for April–June 2026 (30/07)',
       'وزارة المالية · تقرير أداء الميزانية لشهور أبريل–يونيو 2026 (30/07)', 'macro-13: AR debt source')
rename(d, OLD_SRC[len('<div class="csrc">'):-len('</div>')], NEW_SRC[len('<div class="csrc">'):-len('</div>')],
       '<span class="tag off">المصدر</span> وزارة المالية — تقريرا أداء الميزانية لشهور أبريل–يونيو 2026 (30/07/2026) '
       'وأبريل–يونيو 2025 (أرقام يناير–يونيو 2025).', 'macro-14: AR chart A source')
for en, ar in [('1,172 → 1,259', '1,172 ← 1,259'), ('1,251 → 1,375 <b>(+9.9%)</b>', '1,251 ← 1,375 <b>(+9.9%)</b>'),
               ('−79 → −116', '−79 ← −116'), ('1,184 → 1,112', '1,184 ← 1,112'),
               ('1,285 → 1,388 <b>(+8.0%)</b>', '1,285 ← 1,388 <b>(+8.0%)</b>'), ('−101 → −277', '−101 ← −277')]:
    if en not in FILES['fisc']:
        FAILURES.append({'file': 'fisc', 'note': 'macro-05 cell not on page', 'old': en})
    add(d, en, ar, 'macro-05: AR history cell with the right-to-left arrow')
for v in ('245', '191', '1,685'):
    add(d, v + '<span class="kunit">B</span>', v + '<span class="kunit">مليار ريال</span>', 'macro-12: AR KPI unit "مليار ريال"')
d['~10<span class="kunit">days shut</span>'] = '<bdi dir="ltr">~10</bdi><span class="kunit">أيام توقف</span>'
_log('fisc', 'dict', '~10<span class="kunit">days shut</span>', '<bdi dir="ltr">~10</bdi>…', 'code', 'macro-12: "~10" kept left to right in Arabic', 1, True)

new_raw = emb_fmt(d)
FILES['fisc'] = FILES['fisc'][:m.start(2)] + new_raw + FILES['fisc'][m.end(2):]

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['fisc'])
open(J, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=0))
md, _ = write_change_table(os.path.join(HERE, 'change_table_audit_macro_fisc'), 'Audit fixes — Saudi Government Finances (macro)')
print('patched fiscal page and ar.json;', md)
