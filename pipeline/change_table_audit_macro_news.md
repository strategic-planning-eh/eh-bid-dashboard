# Audit fixes — News Intelligence (macro)

Generated 2026-10-12 14:31 · 28 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | news | exact | copy | macro-02: Aramco pricing story — Brent ~$92 on 24/08, ~$87 close on 25/08 | 1 | ✓ |
| 2 | news | exact | copy | macro-02: Aramco pricing key numbers | 1 | ✓ |
| 3 | news | exact | copy | macro-02/01: regional-security oil path and its own key number | 1 | ✓ |
| 4 | news | exact | copy | macro-02: oil card = 25/08 close (~$87), not "today" | 1 | ✓ |
| 5 | news | exact | copy | macro-02: Arabic Aramco pricing story | 1 | ✓ |
| 6 | news | exact | copy | macro-02: Arabic summary oil figure | 1 | ✓ |
| 7 | news | exact | copy | macro-03: Webuild headline — €3.8bn of contracts, part of $8.4bn cancelled | 1 | ✓ |
| 8 | news | exact | copy | macro-03: Arabic Webuild headline | 1 | ✓ |
| 9 | news | exact | code | macro-15: organisation and theme counts derived from the stories | 1 | ✓ |
| 10 | news | exact | copy | macro-07: Arabic note (watchlist card) | 1 | ✓ |
| 11 | news | exact | copy | macro-15/07: stories card counts organisations and themes from the data (EN + AR) | 1 | ✓ |
| 12 | news | exact | copy | macro-07: Arabic note (watch card) | 1 | ✓ |
| 13 | news | exact | copy | macro-07: Arabic note (new-money card) | 1 | ✓ |
| 14 | news | exact | code | macro-07: Arabic unit under the stories count | 1 | ✓ |
| 15 | news | exact | code | macro-07: KPI notes carry their Arabic twin | 1 | ✓ |
| 16 | news | exact | copy | macro-07: chart note has an Arabic twin | 1 | ✓ |
| 17 | news | exact | copy | macro-15: methodology names the report it re-checks (19 July), not "January–March" | 1 | ✓ |
| 18 | news | exact | copy | macro-15: coverage footer arithmetic adds up (overlap and others named); "Q1 claims" → 19 July report | 1 | ✓ |
| 19 | news | exact | code | macro-15: list count from the list | 1 | ✓ |
| 20 | news | exact | code | macro-16: period options with no stories removed | 1 | ✓ |
| 21 | news | exact | code | macro-17: Date column sorts by dateISO | 1 | ✓ |
| 22 | news | exact | code | macro-01: key number keeps decimals and units | 1 | ✓ |
| 23 | news | exact | code | macro-09: sector and category charts — sorted bars, all labels, height follows bar count | 1 | ✓ |
| 24 | news | exact | code | macro-20: story cards focusable | 1 | ✓ |
| 25 | news | exact | code | macro-20: table rows focusable | 1 | ✓ |
| 26 | news | exact | code | macro-20: Items-to-Watch rows focusable | 1 | ✓ |
| 27 | news | exact | code | macro-20: closed panel is inert (its close button leaves the Tab order) | 1 | ✓ |
| 28 | news | exact | code | macro-20: panel focus in/out; Enter/Space opens a story | 1 | ✓ |

## Edit detail

### 1. news — macro-02: Aramco pricing story — Brent ~$92 on 24/08, ~$87 close on 25/08

**Old**
```
then climbed back to about $90–91 by 25 August when the talks failed."
```
**New**
```
then climbed back to about $92 by 24 August when the talks failed, before closing at about $87 on 25 August."
```

### 2. news — macro-02: Aramco pricing key numbers

**Old**
```
World oil price about $90–91 on 25 August."
```
**New**
```
World oil price about $87 at the close on 25 August (about $92 the day before)."
```

### 3. news — macro-02/01: regional-security oil path and its own key number

**Old**
```
→ about $90–91 (25 August, after talks failed).","partners":"Oman
```
**New**
```
→ about $92 (24 August, after talks failed) → about $87 (25 August close).","keyNumber":"Oil price: about $87 (25 August close)","partners":"Oman
```

### 4. news — macro-02: oil card = 25/08 close (~$87), not "today"

**Old**
```
{accent:'#dc2626', num:'~$91', lab:'Oil price today (Brent, 25/08)', note:'Was ~$80 in early Aug when peace looked close · rose as talks failed and attacks spread'},
```
**New**
```
{accent:'#dc2626', num:'~$87', lab:'Oil price (Brent), close on 25/08', note:'About $92 on 24/08 as talks failed · ~$80 in early Aug when peace looked close', noteAr:'نحو 92 دولارًا في 24/08 مع فشل المحادثات · ونحو 80 دولارًا مطلع أغسطس حين بدا السلام قريبًا'},
```

### 5. news — macro-02: Arabic Aramco pricing story

**Old**
```
ثم عاد إلى 90–91 دولارًا بحلول 25 أغسطس مع فشل المحادثات.
```
**New**
```
ثم عاد إلى نحو 92 دولارًا بحلول 24 أغسطس مع فشل المحادثات، قبل أن يُغلق عند نحو 87 دولارًا في 25 أغسطس.
```

### 6. news — macro-02: Arabic summary oil figure

**Old**
```
نفط برنت اليوم <b>~91$</b> (كان ~80$ مطلع أغسطس حين بدا السلام قريبًا، وارتفع مع انهيار المحادثات واتساع الهجمات).
```
**New**
```
سعر إغلاق برنت في 25/08 <b>~87$</b> (كان ~80$ مطلع أغسطس حين بدا السلام قريبًا، ونحو 92$ في 24/08 مع انهيار المحادثات).
```

### 7. news — macro-03: Webuild headline — €3.8bn of contracts, part of $8.4bn cancelled

**Old**
```
"headline":"NEOM cancelled both contracts with Italy's Webuild — over $8 billion of planned construction gone"
```
**New**
```
"headline":"NEOM cancelled both contracts with Italy's Webuild (about €3.8 billion) — part of more than $8.4 billion of NEOM construction called off"
```

### 8. news — macro-03: Arabic Webuild headline

**Old**
```
نيوم ألغت عقدَي «ويبيلد» الإيطالية كليهما — تبخّر أكثر من 8 مليارات دولار من الإنشاءات المخططة
```
**New**
```
نيوم ألغت عقدَي «ويبيلد» الإيطالية كليهما (نحو 3.8 مليارات يورو) — ضمن أكثر من 8.4 مليارات دولار من إنشاءات نيوم الملغاة
```

### 9. news — macro-15: organisation and theme counts derived from the stories

**Old**
```
const DEAL_FLOW = 6.5; // USD bn, in-window new awards / reported frameworks (see chart foot)
```
**New**
```
const DEAL_FLOW = 6.5; // USD bn, in-window new awards / reported frameworks (see chart foot)
/* audit 12/10 (macro-15): stories about regional themes (not organisations) are told apart by their group */
const THEME_GROUPS = ['Macro & Security','Environment & Marine'];
const themeCount = DATA.filter(d=>THEME_GROUPS.includes(d.group)).length;
const orgCount   = new Set(DATA.filter(d=>!THEME_GROUPS.
```

### 10. news — macro-07: Arabic note (watchlist card)

**Old**
```
{accent:'#2563eb', num:META.monitored_total, lab:'Companies & bodies we track', note:'Our full watchlist of Saudi organisations'},
```
**New**
```
{accent:'#2563eb', num:META.monitored_total, lab:'Companies & bodies we track', note:'Our full watchlist of Saudi organisations', noteAr:'قائمتنا الكاملة للمنظمات السعودية'},
```

### 11. news — macro-15/07: stories card counts organisations and themes from the data (EN + AR)

**Old**
```
{accent:'#14b8a6', num:verifiedItems, sub:' items', lab:'News stories verified', note:META.verified_entity_count+' organisations covered · '+corpItems+' company / '+govItems+' government'},
```
**New**
```
{accent:'#14b8a6', num:verifiedItems, sub:' items', subAr:' خبرًا', lab:'News stories verified', note:orgCount+' organisations and '+themeCount+' regional themes · '+corpItems+' company / '+govItems+' government', noteAr:'الجهات: '+orgCount+' · المحاور الإقليمية: '+themeCount+' · شركات: '+corpItems+' / حكومة: '+govItems},
```

### 12. news — macro-07: Arabic note (watch card)

**Old**
```
{accent:'#ef4444', num:flaggedItems, lab:'🔴 Items to watch', note:'Big projects, infrastructure and security stories'},
```
**New**
```
{accent:'#ef4444', num:flaggedItems, lab:'🔴 Items to watch', note:'Big projects, infrastructure and security stories', noteAr:'مشاريع كبرى وبنية تحتية وأمن'},
```

### 13. news — macro-07: Arabic note (new-money card)

**Old**
```
note:'New deals this period (one $5.3 billion item unconfirmed) · cancellations not counted'},
```
**New**
```
note:'New deals this period (one $5.3 billion item unconfirmed) · cancellations not counted', noteAr:'صفقات جديدة في هذه الفترة (منها بند بقيمة 5.3 مليارات دولار غير مؤكد) · لا تُحتسب الإلغاءات'},
```

### 14. news — macro-07: Arabic unit under the stories count

**Old**
```
<div class="k-num">${k.num}${k.sub?`<small>${k.sub}</small>`:''}</div>
```
**New**
```
<div class="k-num">${k.num}${k.sub?`<small${k.subAr?` data-eh-ar="${k.subAr}"`:''}>${k.sub}</small>`:''}</div>
```

### 15. news — macro-07: KPI notes carry their Arabic twin

**Old**
```
<div class="k-note">${k.note}</div>
```
**New**
```
<div class="k-note"${k.noteAr?` data-eh-ar="${k.noteAr}"`:''}>${k.note}</div>
```

### 16. news — macro-07: chart note has an Arabic twin

**Old**
```
<div class="chart-foot">Note: the $5.3 billion HUMAIN figure
```
**New**
```
<div class="chart-foot" data-eh-ar="ملاحظة: رقم HUMAIN البالغ 5.3 مليارات دولار مصدره تقرير صحفي واحد وغير مؤكد. يحتسب هذا الرسم الصفقات الجديدة المعلنة في الفترة فقط — لا العقود الملغاة ولا البرامج الممتدة ولا نتائج الشركات.">Note: the $5.3 billion HUMAIN figure
```

### 17. news — macro-15: methodology names the report it re-checks (19 July), not "January–March"

**Old**
```
(every material January–March claim re-verified, with per-claim verdicts above)
```
**New**
```
(every material claim from our 19 July report re-verified, with per-claim verdicts above)
```

### 18. news — macro-15: coverage footer arithmetic adds up (overlap and others named); "Q1 claims" → 19 July report

**Old**
```
  const pct = Math.round(META.verified_entity_count/META.monitored_total*100);
  document.getElementById('cov-block').innerHTML = `
    <div style="font-size:12.5px;color:var(--ink-soft);margin-top:4px">
      <strong>${META.verified_entity_count}</strong> priority entities verified of <strong>${META.monitored_total}</strong> monitored
      (<strong>${META.on_watchlist_count}</strong> direct watc
```
**New**
```
  /* audit 12/10 (macro-15): every count from the lists themselves; overlap and others named so the sum adds up */
  const vN = META.verified_entities.length, wl = new Set(META.on_watchlist), nb = new Set(META.national_bodies);
  const inBoth = META.verified_entities.filter(v=>wl.has(v)&&nb.has(v)), others = META.verified_entities.filter(v=>!wl.has(v)&&!nb.has(v));
  const pct = Math.round(vN/META
```

### 19. news — macro-15: list count from the list

**Old**
```
document.getElementById('vsub').textContent = `${META.verified_entity_count} entities
```
**New**
```
document.getElementById('vsub').textContent = `${vN} entities
```

### 20. news — macro-16: period options with no stories removed

**Old**
```
cats.forEach(c=>cSel.insertAdjacentHTML('beforeend',`<option value="${c}">${c}</option>`));
```
**New**
```
cats.forEach(c=>cSel.insertAdjacentHTML('beforeend',`<option value="${c}">${c}</option>`));
/* audit 12/10 (macro-16): drop period options that no story carries ("Policy frame" always returned nothing) */
[...document.getElementById('f-period').options].forEach(o=>{ if(o.value!=='all' && !DATA.some(d=>d.period===o.value)) o.remove(); });
```

### 21. news — macro-17: Date column sorts by dateISO

**Old**
```
    if(k==='flagged'){va=a.flagged?1:0; vb=b.flagged?1:0;}
```
**New**
```
    if(k==='flagged'){va=a.flagged?1:0; vb=b.flagged?1:0;}
    if(k==='date'){va=a.dateISO; vb=b.dateISO;}   // audit 12/10 (macro-17): sort by the date, not its display text
```

### 22. news — macro-01: key number keeps decimals and units

**Old**
```
const val = (d.financials && !/^not /i.test(d.financials)) ? d.financials.split(/[.;(]/)[0].trim() : 'Not disclosed';
```
**New**
```
/* audit 12/10 (macro-01): never cut inside a number ("$5.3"); an item may name its own key number */
    const val = d.keyNumber ? d.keyNumber : (d.financials && !/^not /i.test(d.financials)) ? d.financials.split(/;\s|\s\(|\.(?=\s|$)/)[0].trim() : 'Not disclosed';
```

### 23. news — macro-09: sector and category charts — sorted bars, all labels, height follows bar count

**Old**
```
const secData=countBy('group');
new Chart(document.getElementById('chartSector'),{
  type:'doughnut',
  data:{labels:secData.map(x=>x[0]), datasets:[{data:secData.map(x=>x[1]), backgroundColor:PALETTE, borderColor:'#fff', borderWidth:2}]},
  options:{cutout:'60%', plugins:{legend:{position:'right', labels:{boxWidth:9, boxHeight:9, usePointStyle:true, pointStyle:'circle', padding:9, font:{size:12}}
```
**New**
```
/* audit 12/10 (macro-09): both count charts are sorted horizontal bars with every label shown (long ones on two lines);
   the chart grows with the number of bars (the doughnut's legend was cut off, the bar chart skipped half its labels) */
const ehBarBox=(id,n)=>{ const b=document.getElementById(id).parentElement; b.style.height=Math.max(230, n*28+44)+'px'; };
const ehWrap=s=>{ if(s.length<=22) 
```

### 24. news — macro-20: story cards focusable

**Old**
```
<div class="card ${gov?'gov':''}" data-id="${d.id}">
```
**New**
```
<div class="card ${gov?'gov':''}" data-id="${d.id}" tabindex="0" role="button">
```

### 25. news — macro-20: table rows focusable

**Old**
```
const rows = list.map(d=>`<tr data-id="${d.id}">
```
**New**
```
const rows = list.map(d=>`<tr data-id="${d.id}" tabindex="0">
```

### 26. news — macro-20: Items-to-Watch rows focusable

**Old**
```
return `<div class="flag-row" data-id="${d.id}">
```
**New**
```
return `<div class="flag-row" data-id="${d.id}" tabindex="0" role="button">
```

### 27. news — macro-20: closed panel is inert (its close button leaves the Tab order)

**Old**
```
<aside class="panel" id="panel" aria-hidden="true" data-eh-noreveal>
```
**New**
```
<aside class="panel" id="panel" aria-hidden="true" data-eh-noreveal inert>
```

### 28. news — macro-20: panel focus in/out; Enter/Space opens a story

**Old**
```
  overlay.classList.add('open'); panel.classList.add('open'); panel.setAttribute('aria-hidden','false');
}
function closeDetail(){overlay.classList.remove('open'); panel.classList.remove('open'); panel.setAttribute('aria-hidden','true');}
```
**New**
```
  if(!panel.classList.contains('open')) ehLastFocus=document.activeElement;
  overlay.classList.add('open'); panel.classList.add('open'); panel.setAttribute('aria-hidden','false'); panel.inert=false;
  setTimeout(()=>{ try{ document.getElementById('panel-close').focus({preventScroll:true}); }catch(e){} },0);
}
let ehLastFocus=null;
function closeDetail(){ const was=panel.classList.contains('open')
```
