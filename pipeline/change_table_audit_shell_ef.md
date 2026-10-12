# Environment Fund page — audit fixes shell-01/02/08/09/14/15/17

Generated 2026-10-12 14:52 · 18 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | gen | exact | data | shell-02: compute the EH-with-the-Fund table from the bid data at build time (snapshot fallback) | 1 | ✓ |
| 2 | gen | exact | copy | shell-02: stamp says when the bid tracker was read (or how old the snapshot is) | 1 | ✓ |
| 3 | gen | exact | copy | shell-01: honest table columns and a reading written from the numbers | 1 | ✓ |
| 4 | gen | exact | copy | shell-01: xrefHTML() — columns Logged / Submitted / Open / Declined / Cancelled / No submission; reading from the numbers | 1 | ✓ |
| 5 | gen | exact | css | shell-01: on phones the wider table scrolls inside its panel instead of squeezing names into one-word lines | 1 | ✓ |
| 6 | gen | exact | copy | shell-17: Arabic units (مليون/ألف), Gregorian dates, ledger category names | 1 | ✓ |
| 7 | gen | exact | copy | shell-17: facts ledger shows category names, not codes | 1 | ✓ |
| 8 | gen | exact | copy | shell-17: tonnes read "طن" in Arabic charts | 1 | ✓ |
| 9 | gen | exact | code | shell-09: centres on the left, programmes in the middle, EH lines on the right | 1 | ✓ |
| 10 | gen | exact | copy | shell-09: map title follows the new left-to-right order | 1 | ✓ |
| 11 | gen | exact | code | shell-09: lines run centre → programme and programme → EH line only (no line starts at "the first centre") | 1 | ✓ |
| 12 | json | json | copy | shell-01/02: xref keeps client names and match patterns only — counts, "pending" and the reading are computed | 1 | ✓ |
| 13 | json | json | copy | shell-02: meta.tracker_xref_as_of removed (the date now comes from the bid data) | 1 | ✓ |
| 14 | json | json | copy | shell-08: "123 opportunities" chart split — activity (123, p.83) and investor opportunities by centre (45, p.76); inference dropped | 1 | ✓ |
| 15 | json | json | copy | shell-14: "doubled" → "raised by three-quarters (45 % → 79 %)" | 1 | ✓ |
| 16 | json | json | copy | shell-15: waste chart title names the CO₂ bar and the mixed totals / yearly rate | 1 | ✓ |
| 17 | json | json | copy | shell-15: reach chart title names schools and factories | 1 | ✓ |
| 18 | json | json | copy | shell-15: ledger gains the two headline figures it lacked (p.18, p.20) | 1 | ✓ |

## Edit detail

### 1. gen — shell-02: compute the EH-with-the-Fund table from the bid data at build time (snapshot fallback)

**Old**
```
"""build_ef_page.py — renders hub/environment_fund_2025.html from pipeline/ef_report_2025.json.
Re-run after editing the JSON. The page is self-contained apart from eh-shared.css / eh-shared.js."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'ef_report_2025.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else o
```
**New**
```
"""build_ef_page.py — renders hub/environment_fund_2025.html from pipeline/ef_report_2025.json.
Re-run after editing the JSON. The page is self-contained apart from eh-shared.css / eh-shared.js.

"EH's own record with the Fund" is computed from the Bid & Tender app's data each time the page is built
(patch_audit_shell_ef.py, 12 Oct 2026): --bids FILE, or by default pipeline/bidanalytics2.json then
```

### 2. gen — shell-02: stamp says when the bid tracker was read (or how old the snapshot is)

**Old**
```
 $('stamp').innerHTML=`<span>${L('Source','المصدر')}: <b>${esc(L(m.source_en,m.source_ar))}</b> (${m.pages} ${L('pages','صفحة')})</span><span>·</span><span>${L('extracted','تاريخ الاستخراج')} <b dir="ltr">${m.extracted}</b></span><span>·</span><span>${L('checked against EH\'s bid tracker on','مطابقة جدول العطاءات حتى')} <b dir="ltr">${m.tracker_xref_as_of}</b></span>`;
```
**New**
```
 const XL=EF.xref.live;
 $('stamp').innerHTML=`<span>${L('Source','المصدر')}: <b>${esc(L(m.source_en,m.source_ar))}</b> (${m.pages} ${L('pages','صفحة')})</span><span>·</span><span>${L('extracted','تاريخ الاستخراج')} <b>${fmtDay(m.extracted)}</b></span>${XL?`<span>·</span><span>${XL.source==='live'?L('EH\'s bid tracker read on','قُرئ جدول العطاءات في'):L('EH\'s bid tracker as of','جدول العطاءات حتى
```

### 3. gen — shell-01: honest table columns and a reading written from the numbers

**Old**
```
 // xref
 const x=EF.xref;
 $('xref').innerHTML=`<h2>${L("EH's own record with the Fund and the national centres","سجل آفاق البيئة مع الصندوق والمراكز الوطنية")}</h2><div class="note">${esc(L(x.note_en,x.note_ar))}</div>
 <table class="t xr"><thead><tr><th>${L('Client','الجهة')}</th><th style="text-align:center">${L('Tenders','منافسات')}</th><th style="text-align:center">${L('Value (SAR)','القيمة 
```
**New**
```
 // xref — computed from the bid tracker when the page is built (build_ef_page.py; audit shell-01/02, 12 Oct 2026)
 $('xref').innerHTML=xrefHTML();
```

### 4. gen — shell-01: xrefHTML() — columns Logged / Submitted / Open / Declined / Cancelled / No submission; reading from the numbers

**Old**
```
// EH design system v2 (patch_design_ef.py): brand palette (land → sea) for the colours stored in the report data
```
**New**
```
// "EH's own record with the Fund": a tender logged in the tracker is not an EH bid — the columns say what happened to each
function xrefHTML(){
 const x=EF.xref, X=x.live, h=`<h2>${L("EH's own record with the Fund and the national centres","سجل آفاق البيئة مع الصندوق والمراكز الوطنية")}</h2>`;
 if(!X||!X.rows)return h+`<div class="note">${L('The bid tracker was not available when this page was bu
```

### 5. gen — shell-01: on phones the wider table scrolls inside its panel instead of squeezing names into one-word lines

**Old**
```
.xr td.num{text-align:center;font-variant-numeric:tabular-nums}.xr .zero{color:var(--red);font-weight:700}
```
**New**
```
.xr td.num{text-align:center;font-variant-numeric:tabular-nums}.xr .zero{color:var(--red);font-weight:700}.xr td:first-child{min-width:150px}.xr td:last-child{min-width:260px}
```

### 6. gen — shell-17: Arabic units (مليون/ألف), Gregorian dates, ledger category names

**Old**
```
const fmtM=v=>v>=1e6?(v/1e6).toFixed(1).replace(/\.0$/,'')+' M':v>=1e3?(v/1e3).toFixed(0)+' K':String(v);
```
**New**
```
const fmtM=v=>v>=1e6?(v/1e6).toFixed(1).replace(/\.0$/,'')+L(' M',' مليون'):v>=1e3?(v/1e3).toFixed(0)+L(' K',' ألف'):String(v);
const fmtDay=iso=>{const d=new Date(String(iso||'')+'T12:00:00');return isNaN(d)?String(iso||''):d.toLocaleDateString(LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB',{day:'numeric',month:'short',year:'numeric'});};   // Gregorian in both languages, as across the hub
cons
```

### 7. gen — shell-17: facts ledger shows category names, not codes

**Old**
```
<td style="color:var(--muted);white-space:nowrap">${esc(f.cat)}</td>
```
**New**
```
<td style="color:var(--muted);white-space:nowrap">${esc(L(...(CAT[f.cat]||[f.cat,f.cat])))}</td>
```

### 8. gen — shell-17: tonnes read "طن" in Arabic charts

**Old**
```
${r.v.toLocaleString('en-US')}${c.pct?'%':c.unit==='t'?' t':''}
```
**New**
```
${r.v.toLocaleString('en-US')}${c.pct?'%':c.unit==='t'?L(' t',' طن'):''}
```

### 9. gen — shell-09: centres on the left, programmes in the middle, EH lines on the right

**Old**
```
 const xP=40,xC=W/2-40,xE=W-300, bw=[310,150,200];   // EH design v2: programme and centre boxes wide enough for the longest label (English and Arabic) in the brand font
```
**New**
```
 const xC=40,xP=W/2-155,xE=W-240, bw=[310,150,200];   // audit shell-09: centres | programmes | EH lines — every line is a link the report states, none crosses a box
```

### 10. gen — shell-09: map title follows the new left-to-right order

**Old**
```
 <text x="${xP}" y="24" font-size="15" font-weight="800" fill="var(--eh-ink)">${esc(L("Environment Fund programmes → national centres they touch → EH service lines they concern","برامج الصندوق ← المراكز الوطنية التي تمسّها ← خطوط خدمات آفاق البيئة المعنية"))}</text>
 <text x="${xP}" y="42" font-size="11" fill="var(--eh-ink-3)">
```
**New**
```
 <text x="${xC}" y="24" font-size="15" font-weight="800" fill="var(--eh-ink)">${esc(L("National centres → the Environment Fund programmes that touch them → EH service lines they concern","المراكز الوطنية ← برامج الصندوق التي تمسّها ← خطوط خدمات آفاق البيئة المعنية"))}</text>
 <text x="${xC}" y="42" font-size="11" fill="var(--eh-ink-3)">
```

### 11. gen — shell-09: lines run centre → programme and programme → EH line only (no line starts at "the first centre")

**Old**
```
 prods.forEach((p,i)=>{p.centres.forEach(c=>{const j=cen.findIndex(x=>x[0]===c);if(j<0)return;s+=`<path d="M${xP+bw[0]} ${yP(i)+14} C ${xP+bw[0]+90} ${yP(i)+14}, ${xC-90} ${yC(j)+14}, ${xC} ${yC(j)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});
  p.eh.forEach(e=>{const j=ehl.findIndex(x=>x[0]===e);if(j<0)return;const x0=p.centres.length?xC+bw[1]:xP+bw[0];const y0=p.ce
```
**New**
```
 prods.forEach((p,i)=>{p.centres.forEach(c=>{const j=cen.findIndex(x=>x[0]===c);if(j<0)return;const x0=xC+bw[1],x1=xP;s+=`<path d="M${x0} ${yC(j)+14} C ${x0+80} ${yC(j)+14}, ${x1-80} ${yP(i)+14}, ${x1} ${yP(i)+14}" stroke="${col[p.id]}" stroke-width="2" fill="none" opacity=".55"/>`;});
  p.eh.forEach(e=>{const j=ehl.findIndex(x=>x[0]===e);if(j<0)return;const x0=xP+bw[0];s+=`<path d="M${x0} ${yP(i)
```

### 12. json — shell-01/02: xref keeps client names and match patterns only — counts, "pending" and the reading are computed

**Old**
```
{"note_en": "EH's own record with the Fund and the national centres, from the bid tracker (EH-WIN-02-F01) as of 15 Sep 2026.", "note_ar": "سجل آفاق البيئة مع الصندوق والمراكز الوطنية، من جدول تتبع العطاءات (EH-WIN-02-F01) حتى 15 سبتمبر 2026.", "rows": [{"client_en": "Environment Fund", "client_ar": "صندوق البيئة", "tenders": 1, "value": 0, "pending": 0, "cancelled": 1, "decided": 0, "note_en": "Bi
```
**New**
```
{"how_en": "Counts are computed from the bid tracker each time the page is built (build_ef_page.py); a row matches a tender by the client name pattern in 'match'.", "rows": [{"key": "fund", "client_en": "Environment Fund", "client_ar": "صندوق البيئة", "match": "صندوق البيئة|Environment(al)? Fund", "note_en": "Tender 17/26 — sustainability consulting for the national centres", "note_ar": "المنافسة 
```

### 13. json — shell-02: meta.tracker_xref_as_of removed (the date now comes from the bid data)

**Old**
```
"2026-09-15"
```
**New**
```
null
```

### 14. json — shell-08: "123 opportunities" chart split — activity (123, p.83) and investor opportunities by centre (45, p.76); inference dropped

**Old**
```
{"id": "c-activity", "type": "hbar", "title_en": "Where the 123 opportunities sit — by activity, and by the centre seeking private investors", "title_ar": "أين تقع الفرص الـ123 — حسب النشاط، وحسب المركز الجاذب للمستثمرين", "sub_en": "Waste is two-thirds of the pipeline, yet MWAN lists only 4 opportunities to attract private investors — most waste opportunities sit with other centres or in the Fund
```
**New**
```
[{"id": "c-activity", "type": "hbar", "title_en": "Where the 123 opportunities sit — by activity", "title_ar": "أين تقع الفرص الـ123 — حسب النشاط", "sub_en": "Waste is two-thirds of the 123 investment opportunities the Fund reviewed; the report does not list them", "sub_ar": "النفايات ثلثا الفرص الاستثمارية الـ123 التي استعرضها الصندوق؛ ولا يسرد التقرير هذه الفرص", "pages": [83], "color": "#E8862E
```

### 15. json — shell-14: "doubled" → "raised by three-quarters (45 % → 79 %)"

**Old**
```
["A counterpart that closes procurement in 83 days and doubled its digital score will run the centres' tenders differently from how they ran before", "جهة تُنجز المشتريات في 83 يوماً وضاعفت نتيجتها الرقمية ستدير منافسات المراكز بطريقة مختلفة عمّا سبق"]
```
**New**
```
["A counterpart that closes procurement in 83 days and raised its digital score by three-quarters (45 % → 79 %) will run the centres' tenders differently from how they ran before", "جهة تُنجز المشتريات في 83 يوماً ورفعت نتيجتها الرقمية بنحو ثلاثة أرباع (من 45% إلى 79%) ستدير منافسات المراكز بطريقة مختلفة عمّا سبق"]
```

### 16. json — shell-15: waste chart title names the CO₂ bar and the mixed totals / yearly rate

**Old**
```
["Waste tonnage the Fund's 2025 grants put in motion", "أطنان النفايات التي حرّكتها منح الصندوق في 2025", "Three private projects plus one public initiative; company names not disclosed in the report", "ثلاثة مشاريع خاصة ومبادرة عامة؛ أسماء الشركات غير مذكورة في التقرير"]
```
**New**
```
["What the Fund's 2025 grants put in motion — tonnes of waste, and CO₂ avoided", "ما حرّكته منح الصندوق في 2025 — أطنان النفايات، والانبعاثات المخفَّضة", "Three private projects plus one public initiative; company names not disclosed in the report. Whole-programme totals and a yearly rate are shown together — each label says which", "ثلاثة مشاريع خاصة ومبادرة عامة؛ أسماء الشركات غير مذكورة في التق
```

### 17. json — shell-15: reach chart title names schools and factories

**Old**
```
["Grant programme reach in 2025 — people the Fund's initiatives touched", "مدى وصول برنامج المنح في 2025 — من طالتهم مبادرات الصندوق"]
```
**New**
```
["Grant programme reach in 2025 — people, schools and factories the Fund's initiatives touched", "مدى وصول برنامج المنح في 2025 — الأفراد والمدارس والمصانع التي طالتها مبادرات الصندوق"]
```

### 18. json — shell-15: ledger gains the two headline figures it lacked (p.18, p.20)

**Old**
```
null
```
**New**
```
[{"id": "f51", "page": 18, "cat": "headline", "en": "SAR 362.3 million — Income from investing its cash, financial year 1446/47 (measured to international investment-reporting standards)", "ar": "362.3 مليون ريال — العوائد النقدية الاستثمارية للعام المالي 1446/1447هـ (وفق معايير المعايير الدولية لقياس أداء الاستثمار)"}, {"id": "f52", "page": 20, "cat": "headline", "en": "24 initiatives supported i
```
