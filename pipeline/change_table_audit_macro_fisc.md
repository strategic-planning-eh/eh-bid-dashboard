# Audit fixes — Saudi Government Finances (macro)

Generated 2026-10-12 14:19 · 29 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | fisc | exact | copy | macro-13: KPI "Size of the economy" shows a growth rate — renamed "Economic growth, 2026" | 1 | ✓ |
| 2 | fisc | exact | copy | macro-13: debt KPI cites the report the figure comes from | 1 | ✓ |
| 3 | fisc | exact | copy | macro-13: chart E reference line is EH's proxy, not a Ministry assumption | 1 | ✓ |
| 4 | fisc | exact | data | macro-14: Jan–Jun 2025 income = Ministry figures (oil 301.54, other 263.67, total 565.21) | 1 | ✓ |
| 5 | fisc | exact | copy | macro-14: chart A source cites the published 2025 figures | 1 | ✓ |
| 6 | fisc | exact | code | macro-11: language helper for tooltips and markers | 1 | ✓ |
| 7 | fisc | exact | code | macro-11: markers draw their Arabic label in Arabic | 1 | ✓ |
| 8 | fisc | exact | code | macro-11: chart A tooltip in Arabic | 1 | ✓ |
| 9 | fisc | exact | code | macro-11: chart B tooltip value in Arabic | 1 | ✓ |
| 10 | fisc | exact | code | macro-11: chart B tooltip comparison in Arabic | 1 | ✓ |
| 11 | fisc | exact | code | macro-11: chart C tooltip in Arabic | 1 | ✓ |
| 12 | fisc | exact | code | macro-11: chart D tooltip in Arabic | 1 | ✓ |
| 13 | fisc | exact | code | macro-11: chart E tooltip in Arabic | 1 | ✓ |
| 14 | fisc | exact | code | macro-11: Arabic marker labels; last marker moved left of its line and one row down (no collision) | 1 | ✓ |
| 15 | fisc | exact | code | macro-11: chart F tooltip in Arabic | 1 | ✓ |
| 16 | fisc | exact | code | macro-11: chart G tooltip in Arabic | 1 | ✓ |
| 17 | fisc | dict | copy | macro-13: AR label "Economic growth, 2026" | 1 | ✓ |
| 18 | fisc | dict | copy | macro-13: AR debt source | 1 | ✓ |
| 19 | fisc | dict | copy | macro-14: AR chart A source | 1 | ✓ |
| 20 | fisc | dict | copy | macro-05: AR history cell with the right-to-left arrow | 0 | ✓ |
| 21 | fisc | dict | copy | macro-05: AR history cell with the right-to-left arrow | 0 | ✓ |
| 22 | fisc | dict | copy | macro-05: AR history cell with the right-to-left arrow | 0 | ✓ |
| 23 | fisc | dict | copy | macro-05: AR history cell with the right-to-left arrow | 0 | ✓ |
| 24 | fisc | dict | copy | macro-05: AR history cell with the right-to-left arrow | 0 | ✓ |
| 25 | fisc | dict | copy | macro-05: AR history cell with the right-to-left arrow | 0 | ✓ |
| 26 | fisc | dict | copy | macro-12: AR KPI unit "مليار ريال" | 0 | ✓ |
| 27 | fisc | dict | copy | macro-12: AR KPI unit "مليار ريال" | 0 | ✓ |
| 28 | fisc | dict | copy | macro-12: AR KPI unit "مليار ريال" | 0 | ✓ |
| 29 | fisc | dict | code | macro-12: "~10" kept left to right in Arabic | 1 | ✓ |

## Edit detail

### 1. fisc — macro-13: KPI "Size of the economy" shows a growth rate — renamed "Economic growth, 2026"

**Old**
```
{label:'Size of the economy, 2026', val:'\u22123.6'
```
**New**
```
{label:'Economic growth, 2026', val:'\u22123.6'
```

### 2. fisc — macro-13: debt KPI cites the report the figure comes from

**Old**
```
src:'Ministry of Finance \u00b7 borrowing plan for 2027 due by year-end'}
```
**New**
```
src:'Ministry of Finance \u00b7 budget performance report for April\u2013June 2026 (30/07)'}
```

### 3. fisc — macro-13: chart E reference line is EH's proxy, not a Ministry assumption

**Old**
```
{label:'Price the budget assumed ($69.9, 2025 average)', data:budgetRef
```
**New**
```
{label:'EH reference: 2025 average price ($69.9) \u2014 the Ministry publishes no oil-price assumption', data:budgetRef
```

### 4. fisc — macro-14: Jan–Jun 2025 income = Ministry figures (oil 301.54, other 263.67, total 565.21)

**Old**
```
{label:'Jan–Jun 2025', data:[301.5,264.6,566.1]
```
**New**
```
{label:'Jan–Jun 2025', data:[301.5,263.7,565.2]
```

### 5. fisc — macro-14: chart A source cites the published 2025 figures

**Old**
```
<div class="csrc"><span class="tag off">Source</span> Ministry of Finance — budget performance report for April–June 2026 (30/07/2026). The 2025 figures are worked back from the percentage changes the Ministry published.</div>
```
**New**
```
<div class="csrc"><span class="tag off">Source</span> Ministry of Finance — budget performance reports for April–June 2026 (30/07/2026) and April–June 2025 (January–June 2025 figures).</div>
```

### 6. fisc — macro-11: language helper for tooltips and markers

**Old**
```
/* vertical event-marker plugin (no external dep) */
```
**New**
```
/* audit 12/10 (macro-11): Arabic tooltips and marker labels — the page language decides at draw time */
const EH_AR_TIP=()=>document.documentElement.lang==='ar';
const L=(en,ar)=>EH_AR_TIP()?ar:en;
/* vertical event-marker plugin (no external dep) */
```

### 7. fisc — macro-11: markers draw their Arabic label in Arabic

**Old**
```
ctx.fillText(m.label, xp+(m.align==='right'?-6:6), top+(m.yOff||12));
```
**New**
```
ctx.fillText((EH_AR_TIP()&&m.ar)||m.label, xp+(m.align==='right'?-6:6), top+(m.yOff||12));
```

### 8. fisc — macro-11: chart A tooltip in Arabic

**Old**
```
label:c=>`${c.dataset.label}: SAR ${FMT(c.parsed.y)} billion`,
      afterBody:(items)=>{const ch=['Oil: +9% (Apr–Jun alone: +22%)','Other: +2%','Total: +6%'];return '\nChange on a year earlier → '+ch[items[0].dataIndex];}
```
**New**
```
label:c=>L(`${c.dataset.label}: SAR ${FMT(c.parsed.y)} billion`,`${c.dataset.label}: ${FMT(c.parsed.y)} مليار ريال`),
      afterBody:(items)=>{const ch=L(['Oil: +9% (Apr–Jun alone: +22%)','Other: +2%','Total: +6%'],['النفط: +9% (أبريل–يونيو وحده: +22%)','الدخل الآخر: +2%','الإجمالي: +6%']);return L('\nChange on a year earlier → ','\nالتغير عن العام السابق: ')+ch[items[0].dataIndex];}
```

### 9. fisc — macro-11: chart B tooltip value in Arabic

**Old**
```
label:c=>`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,
      afterBody:(items)=>{const q1=
```
**New**
```
label:c=>L(`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,`${c.dataset.label}: ${FMT(c.parsed.x)} مليار ريال`),
      afterBody:(items)=>{const q1=
```

### 10. fisc — macro-11: chart B tooltip comparison in Arabic

**Old**
```
let s='\nJan–Mar vs a year earlier: '+q1[i];if(q2[i]!==undefined)s+='  ·  Apr–Jun: '+q2[i];return s;}
```
**New**
```
let s=L('\nJan–Mar vs a year earlier: ','\nيناير–مارس مقارنة بالعام السابق: ')+q1[i];if(q2[i]!==undefined)s+=L('  ·  Apr–Jun: ','  ·  أبريل–يونيو: ')+q2[i];return s;}
```

### 11. fisc — macro-11: chart C tooltip in Arabic

**Old**
```
label:c=>`Gap: SAR ${FMT(Math.abs(c.parsed.y))} billion`,
        afterLabel:c=>{const p=['Before the war · oil $75, OPEC+ holding back production','Before the war · normal quarter','War, Jan–Mar · record gap; spending +20%','War, Apr–Jun · higher oil income arrives; spending +11%'];return p[c.dataIndex];}
```
**New**
```
label:c=>L(`Gap: SAR ${FMT(Math.abs(c.parsed.y))} billion`,`الفجوة: ${FMT(Math.abs(c.parsed.y))} مليار ريال`),
        afterLabel:c=>{const p=L(['Before the war · oil $75, OPEC+ holding back production','Before the war · normal quarter','War, Jan–Mar · record gap; spending +20%','War, Apr–Jun · higher oil income arrives; spending +11%'],['قبل الحرب · النفط 75 دولارًا وأوبك+ تقيّد الإنتاج','قبل الح
```

### 12. fisc — macro-11: chart D tooltip in Arabic

**Old**
```
label:c=>`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,
      afterBody:items=>{const i=items[0].dataIndex;return `\nJan–Mar vs a year earlier: ${secYoY[i]}  ·  Jan–Mar used ${secPct[i]} of the year's budget (Ministry of Finance)`;} }}},
```
**New**
```
label:c=>L(`${c.dataset.label}: SAR ${FMT(c.parsed.x)} billion`,`${c.dataset.label}: ${FMT(c.parsed.x)} مليار ريال`),
      afterBody:items=>{const i=items[0].dataIndex;return L(`\nJan–Mar vs a year earlier: ${secYoY[i]}  ·  Jan–Mar used ${secPct[i]} of the year's budget (Ministry of Finance)`,`\nيناير–مارس مقارنة بالعام السابق: ${secYoY[i]}  ·  استُخدم في يناير–مارس ${secPct[i]} من ميزانية السنة 
```

### 13. fisc — macro-11: chart E tooltip in Arabic

**Old**
```
tooltip:{callbacks:{label:c=>c.parsed.y==null?null:`${c.dataset.label}: $${c.parsed.y} a barrel`}},
```
**New**
```
tooltip:{callbacks:{label:c=>c.parsed.y==null?null:L(`${c.dataset.label}: $${c.parsed.y} a barrel`,`${c.dataset.label}: ${c.parsed.y} دولارًا للبرميل`)}},
```

### 14. fisc — macro-11: Arabic marker labels; last marker moved left of its line and one row down (no collision)

**Old**
```
        {x:1.5,label:'War · 28 Feb',color:C.red},
        {x:3.2,label:'Ceasefire · 8 Apr',color:C.greyd,yOff:26},
        {x:4.4,label:'UAE exits OPEC · May',color:C.blued,yOff:12},
        {x:6.2,label:'Fighting restarts · 8 Jul',color:C.red,yOff:26},
        {x:6.8,label:'Red Sea attacks · 25 Jul',color:'#8B0000',yOff:42},
        {x:8.3,label:'Pipeline hit · Houthis take Bab el-Mandeb · 10–11 
```
**New**
```
        {x:1.5,label:'War · 28 Feb',ar:'الحرب · 28 فبراير',color:C.red},
        {x:3.2,label:'Ceasefire · 8 Apr',ar:'وقف إطلاق النار · 8 أبريل',color:C.greyd,yOff:26},
        {x:4.4,label:'UAE exits OPEC · May',ar:'الإمارات تغادر أوبك · مايو',color:C.blued,yOff:12},
        {x:6.2,label:'Fighting restarts · 8 Jul',ar:'استئناف القتال · 8 يوليو',color:C.red,yOff:26},
        {x:6.8,label:'Red Sea 
```

### 15. fisc — macro-11: chart F tooltip in Arabic

**Old**
```
label:c=>c.parsed.y==null?null:`${c.dataset.label}: SAR ${FMT(Math.abs(c.parsed.y))} billion so far this year`,
        footer:items=>{const i=items[0].dataIndex; return i<=1?'Official Ministry of Finance figure':(i===3?'Year-end: Ministry estimate, or the middle of the range for an EH path':'End of September: EH illustration');}
```
**New**
```
label:c=>c.parsed.y==null?null:L(`${c.dataset.label}: SAR ${FMT(Math.abs(c.parsed.y))} billion so far this year`,`${c.dataset.label}: ${FMT(Math.abs(c.parsed.y))} مليار ريال منذ بداية العام`),
        footer:items=>{const i=items[0].dataIndex; return i<=1?L('Official Ministry of Finance figure','رقم رسمي من وزارة المالية'):(i===3?L('Year-end: Ministry estimate, or the middle of the range for an EH
```

### 16. fisc — macro-11: chart G tooltip in Arabic

**Old**
```
tooltip:{callbacks:{label:c=>c.parsed.y==null?null:`${c.dataset.label}: ${c.parsed.y>0?'surplus':'gap'} SAR ${FMT(Math.abs(c.parsed.y))} billion`}} },
```
**New**
```
tooltip:{callbacks:{label:c=>c.parsed.y==null?null:L(`${c.dataset.label}: ${c.parsed.y>0?'surplus':'gap'} SAR ${FMT(Math.abs(c.parsed.y))} billion`,`${c.dataset.label}: ${c.parsed.y>0?'فائض':'فجوة'} ${FMT(Math.abs(c.parsed.y))} مليار ريال`)}} },
```

### 17. fisc — macro-13: AR label "Economic growth, 2026"

**Old**
```
<span class="klabel">Size of the economy, 2026</span>
```
**New**
```
<span class="klabel">Economic growth, 2026</span> => <span class="klabel">النمو الاقتصادي، 2026</span>
```

### 18. fisc — macro-13: AR debt source

**Old**
```
Ministry of Finance · borrowing plan for 2027 due by year-end
```
**New**
```
Ministry of Finance · budget performance report for April–June 2026 (30/07) => وزارة المالية · تقرير أداء الميزانية لشهور أبريل–يونيو 2026 (30/07)
```

### 19. fisc — macro-14: AR chart A source

**Old**
```
<span class="tag off">Source</span> Ministry of Finance — budget performance report for April–June 2026 (30/07/2026). The 2025 figures are worked back from the percentage changes the Ministry published.
```
**New**
```
<span class="tag off">Source</span> Ministry of Finance — budget performance reports for April–June 2026 (30/07/2026) and April–June 2025 (January–June 2025 figures). => <span class="tag off">المصدر</span> وزارة المالية — تقريرا أداء الميزانية لشهور أبريل–يونيو 2026 (30/07/2026) وأبريل–يونيو 2025 (أرقام يناير–يونيو 2025).
```

### 20. fisc — macro-05: AR history cell with the right-to-left arrow

**Old**
```
1,172 → 1,259
```
**New**
```
1,172 ← 1,259
```

### 21. fisc — macro-05: AR history cell with the right-to-left arrow

**Old**
```
1,251 → 1,375 <b>(+9.9%)</b>
```
**New**
```
1,251 ← 1,375 <b>(+9.9%)</b>
```

### 22. fisc — macro-05: AR history cell with the right-to-left arrow

**Old**
```
−79 → −116
```
**New**
```
−79 ← −116
```

### 23. fisc — macro-05: AR history cell with the right-to-left arrow

**Old**
```
1,184 → 1,112
```
**New**
```
1,184 ← 1,112
```

### 24. fisc — macro-05: AR history cell with the right-to-left arrow

**Old**
```
1,285 → 1,388 <b>(+8.0%)</b>
```
**New**
```
1,285 ← 1,388 <b>(+8.0%)</b>
```

### 25. fisc — macro-05: AR history cell with the right-to-left arrow

**Old**
```
−101 → −277
```
**New**
```
−101 ← −277
```

### 26. fisc — macro-12: AR KPI unit "مليار ريال"

**Old**
```
245<span class="kunit">B</span>
```
**New**
```
245<span class="kunit">مليار ريال</span>
```

### 27. fisc — macro-12: AR KPI unit "مليار ريال"

**Old**
```
191<span class="kunit">B</span>
```
**New**
```
191<span class="kunit">مليار ريال</span>
```

### 28. fisc — macro-12: AR KPI unit "مليار ريال"

**Old**
```
1,685<span class="kunit">B</span>
```
**New**
```
1,685<span class="kunit">مليار ريال</span>
```

### 29. fisc — macro-12: "~10" kept left to right in Arabic

**Old**
```
~10<span class="kunit">days shut</span>
```
**New**
```
<bdi dir="ltr">~10</bdi>…
```
