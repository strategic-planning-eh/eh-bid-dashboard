# Audit fixes — Vision 2030 (macro)

Generated 2026-10-12 14:24 · 35 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | v | exact | copy | macro-04: KAP review note — 30th in the 2023 index, not "world's most efficient (2024)" | 1 | ✓ |
| 2 | v | exact | copy | macro-04: KAP description | 1 | ✓ |
| 3 | v | exact | copy | macro-06: Arabic descriptions, review notes, lead entities, partner names, completion values (31 projects) | 1 | ✓ |
| 4 | v | exact | code | macro-06: Arabic card description and completion | 1 | ✓ |
| 5 | v | exact | code | macro-06: Arabic table lead entity and completion | 1 | ✓ |
| 6 | v | exact | code | macro-06: Arabic investment unit | 1 | ✓ |
| 7 | v | exact | code | macro-06: Arabic drawer lead entity | 1 | ✓ |
| 8 | v | exact | code | macro-06: Arabic drawer review note | 1 | ✓ |
| 9 | v | exact | code | macro-06: Arabic drawer description | 1 | ✓ |
| 10 | v | exact | code | macro-06: Arabic drawer completion | 1 | ✓ |
| 11 | v | exact | code | macro-06: first tab label can switch language | 1 | ✓ |
| 12 | v | exact | copy | macro-06: Arabic tab name made grammatical | 1 | ✓ |
| 13 | v | exact | code | macro-06: first tab label in Arabic while the Arabic tab is open | 1 | ✓ |
| 14 | v | exact | code | macro-08/19c: remainder-slice and review-month helpers | 1 | ✓ |
| 15 | v | exact | code | macro-08: EN legend lists the remainder | 1 | ✓ |
| 16 | v | exact | code | macro-08: EN doughnut draws the remainder | 1 | ✓ |
| 17 | v | exact | code | macro-08/06: AR legend lists the remainder, partner names in Arabic | 1 | ✓ |
| 18 | v | exact | code | macro-06: AR partner names (undisclosed stakes) | 1 | ✓ |
| 19 | v | exact | code | macro-08: AR doughnut draws the remainder | 1 | ✓ |
| 20 | v | exact | code | macro-19b: EN status chips only for statuses in use | 1 | ✓ |
| 21 | v | exact | code | macro-19b: EN confidence chips only for levels in use | 1 | ✓ |
| 22 | v | exact | code | macro-19b: AR status chips only for statuses in use | 1 | ✓ |
| 23 | v | exact | code | macro-19b: AR confidence chips only for levels in use | 1 | ✓ |
| 24 | v | exact | code | macro-19c: EN last-reviewed month per project | 1 | ✓ |
| 25 | v | exact | code | macro-19c: AR last-reviewed month per project | 1 | ✓ |
| 26 | v | exact | code | macro-20: EN cards focusable | 1 | ✓ |
| 27 | v | exact | code | macro-20: EN rows focusable | 1 | ✓ |
| 28 | v | exact | code | macro-20: AR cards focusable | 1 | ✓ |
| 29 | v | exact | code | macro-20: AR rows focusable | 1 | ✓ |
| 30 | v | exact | code | macro-20: closed AR drawer inert | 1 | ✓ |
| 31 | v | exact | code | macro-20: closed EN drawer inert | 1 | ✓ |
| 32 | v | exact | code | macro-20: EN drawer focus in | 1 | ✓ |
| 33 | v | exact | code | macro-20: EN drawer focus out; Enter/Space opens the focused card or row | 1 | ✓ |
| 34 | v | exact | code | macro-20: AR drawer focus in | 1 | ✓ |
| 35 | v | exact | code | macro-20: AR drawer focus out | 1 | ✓ |

## Edit detail

### 1. v — macro-04: KAP review note — 30th in the 2023 index, not "world's most efficient (2024)"

**Old**
```
Handled 2.93 million shipping containers in 2023. Ranked world's most efficient container port (World Bank port-efficiency ranking, 2024).
```
**New**
```
Handled 2.93 million shipping containers in 2023. Once ranked the world's most efficient container port by the World Bank; 30th in the World Bank's container port performance index for 2023 (published 2024).
```

### 2. v — macro-04: KAP description

**Old**
```
desc:"The Kingdom's first fully privately developed port — now the world's most efficient container port in the World Bank's ranking (2024). Phase 2 targets capacity of ~6 million containers a year."
```
**New**
```
desc:"The Kingdom's first fully privately developed port. The World Bank once ranked it the world's most efficient container port; in the 2023 index (published 2024) it ranked 30th. Phase 2 targets capacity of ~6 million containers a year."
```

### 3. v — macro-06: Arabic descriptions, review notes, lead entities, partner names, completion values (31 projects)

**Old**
```
function arName(p){ return AR_NAMES[p.name]||p.name; }
```
**New**
```
function arName(p){ return AR_NAMES[p.name]||p.name; }
/* audit 12/10 (macro-06): Arabic texts for every project (EH translations) — description, review note, lead entity;
   partner names and completion values. English stays in PROJECTS; the Arabic tab reads from here. */
const AR_TXT = {
"NEOM": {
"lead": "شركة نيوم",
"desc": "المنطقة الرائدة لصندوق الاستثمارات العامة في منطقة تبوك، ويُعاد النظر
```

### 4. v — macro-06: Arabic card description and completion

**Old**
```
<div class="desc">${p.desc}</div>
      <div class="c-meta">
        <span class="status-pill"><span class="dot" style="background:${STATUS_HEX[p.status]}"></span>${AR_STATUS[p.status]}</span>
        <div class="figs"><b>${arFmtInv(p.investment)}</b>${p.completion}
```
**New**
```
<div class="desc">${arTxt(p,'desc')}</div>
      <div class="c-meta">
        <span class="status-pill"><span class="dot" style="background:${STATUS_HEX[p.status]}"></span>${AR_STATUS[p.status]}</span>
        <div class="figs"><b>${arFmtInv(p.investment)}</b>${arCompletion(p.completion)}
```

### 5. v — macro-06: Arabic table lead entity and completion

**Old**
```
      <td style="color:var(--ink-soft)">${p.lead}</td>
      <td><span class="mini-dot"><span class="dot" style="background:${STATUS_HEX[p.status]}"></span>${AR_STATUS[p.status]}</span></td>
      <td class="num">${p.completion}</td>
```
**New**
```
      <td style="color:var(--ink-soft)">${arTxt(p,'lead')}</td>
      <td><span class="mini-dot"><span class="dot" style="background:${STATUS_HEX[p.status]}"></span>${AR_STATUS[p.status]}</span></td>
      <td class="num">${arCompletion(p.completion)}</td>
```

### 6. v — macro-06: Arabic investment unit

**Old**
```
function arFmtInv(v){ return v==null?"—":"$"+(Number.isInteger(v)?v:v.toFixed(1))+"B"; }
```
**New**
```
function arFmtInv(v){ return v==null?"—":(Number.isInteger(v)?v:v.toFixed(1))+" مليار $"; }   // audit 12/10 (macro-06): Arabic unit, as in the KPI
```

### 7. v — macro-06: Arabic drawer lead entity

**Old**
```
document.getElementById("arDLead").textContent=p.lead;
```
**New**
```
document.getElementById("arDLead").textContent=arTxt(p,'lead');
```

### 8. v — macro-06: Arabic drawer review note

**Old**
```
<div><strong>ملاحظة المراجعة:</strong> ${p.note}</div>
```
**New**
```
<div><strong>ملاحظة المراجعة:</strong> ${arTxt(p,'note')}</div>
```

### 9. v — macro-06: Arabic drawer description

**Old**
```
    <div class="d-section"><div class="d-desc">${p.desc}</div></div>
    ${noteHtml}
    <div class="d-section"><h3>الحقائق الأساسية</h3>
```
**New**
```
    <div class="d-section"><div class="d-desc">${arTxt(p,'desc')}</div></div>
    ${noteHtml}
    <div class="d-section"><h3>الحقائق الأساسية</h3>
```

### 10. v — macro-06: Arabic drawer completion

**Old**
```
<div class="fact"><div class="fl">الاكتمال المتوقع</div><div class="fv num">${p.completion}</div></div>
```
**New**
```
<div class="fact"><div class="fl">الاكتمال المتوقع</div><div class="fv num">${arCompletion(p.completion)}</div></div>
```

### 11. v — macro-06: first tab label can switch language

**Old**
```
      Strategic Dashboard
    </button>
```
**New**
```
      <span id="tabDashLbl">Strategic Dashboard</span>
    </button>
```

### 12. v — macro-06: Arabic tab name made grammatical

**Old**
```
      التقرير التحقق — عربي

```
**New**
```
      تقرير التحقق — عربي

```

### 13. v — macro-06: first tab label in Arabic while the Arabic tab is open

**Old**
```
function switchTab(tab){document.documentElement.lang=(tab==='arabic'?'ar':'en');
```
**New**
```
function switchTab(tab){document.documentElement.lang=(tab==='arabic'?'ar':'en');
  { const l=document.getElementById('tabDashLbl'); if(l) l.textContent=(tab==='arabic'?'اللوحة الاستراتيجية (بالإنجليزية)':'Strategic Dashboard'); }   // audit 12/10 (macro-06)
```

### 14. v — macro-08/19c: remainder-slice and review-month helpers

**Old**
```
function confOf(p){ return CONF[p.confidence || CONF_OVERRIDE[p.name] || "Medium"]; }
```
**New**
```
function confOf(p){ return CONF[p.confidence || CONF_OVERRIDE[p.name] || "Medium"]; }
/* audit 12/10 (macro-08): when disclosed stakes add up to less than 100%, the rest is its own grey slice */
const OTHER_HEX = "#AEB9CE";
function stakeParts(p){ const sum=p.partners.reduce((a,pt)=>a+(pt.s||0),0); const parts=p.partners.map((pt,i)=>({n:pt.n,s:pt.s,c:SECTOR_HEX[i%SECTOR_HEX.length]}));
  if(sum<99
```

### 15. v — macro-08: EN legend lists the remainder

**Old**
```
        <div class="jv-legend">${p.partners.map((pt,i)=>`
          <div class="jv-item"><span class="dot" style="background:${SECTOR_HEX[i%SECTOR_HEX.length]}"></span>
          <span class="jn">${pt.n}</span><span class="js">${pt.s}%</span></div>`).join("")}</div>
```
**New**
```
        <div class="jv-legend">${stakeParts(p).map(pt=>`
          <div class="jv-item"><span class="dot" style="background:${pt.c}"></span>
          <span class="jn">${pt.n}</span><span class="js">${pt.s}%</span></div>`).join("")}</div>
```

### 16. v — macro-08: EN doughnut draws the remainder

**Old**
```
      data:{labels:p.partners.map(pt=>pt.n),datasets:[{data:p.partners.map(pt=>pt.s),backgroundColor:p.partners.map((_,i)=>SECTOR_HEX[i%SECTOR_HEX.length]),borderColor:ehTok("--eh-paper","#fff"),borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"60%",
        plugins:
```
**New**
```
      data:{labels:stakeParts(p).map(pt=>pt.n),datasets:[{data:stakeParts(p).map(pt=>pt.s),backgroundColor:stakeParts(p).map(pt=>pt.c),borderColor:ehTok("--eh-paper","#fff"),borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"60%",
        plugins:
```

### 17. v — macro-08/06: AR legend lists the remainder, partner names in Arabic

**Old**
```
<div class="jv-legend">${p.partners.map((pt,i)=>`<div class="jv-item"><span class="dot" style="background:${SECTOR_HEX[i%SECTOR_HEX.length]}"></span><span class="jn">${pt.n}</span><span class="js">${pt.s}%</span></div>`).join("")}</div></div>`;
```
**New**
```
<div class="jv-legend">${stakeParts(p).map(pt=>`<div class="jv-item"><span class="dot" style="background:${pt.c}"></span><span class="jn">${arPartner(pt.n)}</span><span class="js">${pt.s}%</span></div>`).join("")}</div></div>`;
```

### 18. v — macro-06: AR partner names (undisclosed stakes)

**Old**
```
<div class="jv-bar-top"><span class="jn">${pt.n}</span><span class="js">${pt.s!=null?pt.s+"%":"غير معلن"}</span>
```
**New**
```
<div class="jv-bar-top"><span class="jn">${arPartner(pt.n)}</span><span class="js">${pt.s!=null?pt.s+"%":"غير معلن"}</span>
```

### 19. v — macro-08: AR doughnut draws the remainder

**Old**
```
      data:{labels:p.partners.map(pt=>pt.n),datasets:[{data:p.partners.map(pt=>pt.s),backgroundColor:p.partners.map((_,i)=>SECTOR_HEX[i%SECTOR_HEX.length]),borderColor:ehTok("--eh-paper","#fff"),borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"60%",plugins:
```
**New**
```
      data:{labels:stakeParts(p).map(pt=>arPartner(pt.n)),datasets:[{data:stakeParts(p).map(pt=>pt.s),backgroundColor:stakeParts(p).map(pt=>pt.c),borderColor:ehTok("--eh-paper","#fff"),borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"60%",plugins:
```

### 20. v — macro-19b: EN status chips only for statuses in use

**Old**
```
makeChips(document.getElementById("statusChips"),ALL_STATUS,state.status,false);
```
**New**
```
makeChips(document.getElementById("statusChips"),ALL_STATUS.filter(s=>PROJECTS.some(p=>p.status===s)),state.status,false);   // audit 12/10 (macro-19b): no chips that match nothing
```

### 21. v — macro-19b: EN confidence chips only for levels in use

**Old**
```
  ["High","Medium","Low"].forEach(level=>{
    const c=document.createElement("button");
    c.className="conf-chip";
    c.innerHTML=`<span class="cdot" style="background:${CONF[level].hex}"></span>${level}`;
```
**New**
```
  ["High","Medium","Low"].filter(l=>PROJECTS.some(p=>confOf(p).label===l)).forEach(level=>{
    const c=document.createElement("button");
    c.className="conf-chip";
    c.innerHTML=`<span class="cdot" style="background:${CONF[level].hex}"></span>${level}`;
```

### 22. v — macro-19b: AR status chips only for statuses in use

**Old**
```
arMakeChips(document.getElementById("arStatusChipsF"),ALL_STATUS,arState.status,'status');
```
**New**
```
arMakeChips(document.getElementById("arStatusChipsF"),ALL_STATUS.filter(s=>PROJECTS.some(p=>p.status===s)),arState.status,'status');
```

### 23. v — macro-19b: AR confidence chips only for levels in use

**Old**
```
  ["High","Medium","Low"].forEach(level=>{
    const c=document.createElement("button");
    c.className="conf-chip";
    c.innerHTML=`<span class="cdot" style="background:${CONF[level].hex}"></span>${AR_CONF[level]}`;
```
**New**
```
  ["High","Medium","Low"].filter(l=>PROJECTS.some(p=>confOf(p).label===l)).forEach(level=>{
    const c=document.createElement("button");
    c.className="conf-chip";
    c.innerHTML=`<span class="cdot" style="background:${CONF[level].hex}"></span>${AR_CONF[level]}`;
```

### 24. v — macro-19c: EN last-reviewed month per project

**Old**
```
<div class="fact"><div class="fl">Last Reviewed</div><div class="fv" style="font-size:13px">${LAST_REVIEWED}</div></div>
```
**New**
```
<div class="fact"><div class="fl">Last Reviewed</div><div class="fv" style="font-size:13px">${reviewedOf(p,false)}</div></div>
```

### 25. v — macro-19c: AR last-reviewed month per project

**Old**
```
<div class="fact"><div class="fl">آخر مراجعة</div><div class="fv" style="font-size:13px">أغسطس 2026</div></div>
```
**New**
```
<div class="fact"><div class="fl">آخر مراجعة</div><div class="fv" style="font-size:13px">${reviewedOf(p,true)}</div></div>
```

### 26. v — macro-20: EN cards focusable

**Old**
```
    return `<div class="card" data-idx="${idx}">
      <div class="c-top">
        <div class="c-name">${p.name}</div>
```
**New**
```
    return `<div class="card" data-idx="${idx}" tabindex="0" role="button">
      <div class="c-top">
        <div class="c-name">${p.name}</div>
```

### 27. v — macro-20: EN rows focusable

**Old**
```
    return `<tr data-idx="${idx}">
      <td><span class="tname">${p.name}</span>
```
**New**
```
    return `<tr data-idx="${idx}" tabindex="0">
      <td><span class="tname">${p.name}</span>
```

### 28. v — macro-20: AR cards focusable

**Old**
```
    return `<div class="card" data-idx="${idx}">
      <div class="c-top"><div class="c-name">${arName(p)}</div>
```
**New**
```
    return `<div class="card" data-idx="${idx}" tabindex="0" role="button">
      <div class="c-top"><div class="c-name">${arName(p)}</div>
```

### 29. v — macro-20: AR rows focusable

**Old**
```
    return `<tr data-idx="${idx}">
      <td><span class="tname">${arName(p)}</span>
```
**New**
```
    return `<tr data-idx="${idx}" tabindex="0">
      <td><span class="tname">${arName(p)}</span>
```

### 30. v — macro-20: closed AR drawer inert

**Old**
```
<aside class="drawer panel ar-drawer" id="arDrawer" data-eh-noreveal dir="rtl" aria-hidden="true">
```
**New**
```
<aside class="drawer panel ar-drawer" id="arDrawer" data-eh-noreveal dir="rtl" aria-hidden="true" inert>
```

### 31. v — macro-20: closed EN drawer inert

**Old**
```
<aside class="drawer panel" id="drawer" data-eh-noreveal aria-hidden="true">
```
**New**
```
<aside class="drawer panel" id="drawer" data-eh-noreveal aria-hidden="true" inert>
```

### 32. v — macro-20: EN drawer focus in

**Old**
```
  document.getElementById("scrim").classList.add("open");
  document.getElementById("drawer").classList.add("open");
  document.getElementById("drawer").setAttribute("aria-hidden","false");
```
**New**
```
  ehDrawerOpen("drawer","drawerClose");
  document.getElementById("scrim").classList.add("open");
  document.getElementById("drawer").classList.add("open");
  document.getElementById("drawer").setAttribute("aria-hidden","false");
```

### 33. v — macro-20: EN drawer focus out; Enter/Space opens the focused card or row

**Old**
```
function closeDrawer(){
  document.getElementById("scrim").classList.remove("open");
```
**New**
```
/* audit 12/10 (macro-20): drawers are inert while closed; focus moves to the close button and back to the card */
let ehLastFocus=null;
function ehDrawerOpen(id,closeId){ const d=document.getElementById(id); if(!d.classList.contains("open")) ehLastFocus=document.activeElement; d.inert=false;
  setTimeout(()=>{ try{ document.getElementById(closeId).focus({preventScroll:true}); }catch(e){} },0); }

```

### 34. v — macro-20: AR drawer focus in

**Old**
```
  document.getElementById("arScrim").classList.add("open");
  document.getElementById("arDrawer").classList.add("open");
```
**New**
```
  ehDrawerOpen("arDrawer","arDrawerClose");
  document.getElementById("arScrim").classList.add("open");
  document.getElementById("arDrawer").classList.add("open");
```

### 35. v — macro-20: AR drawer focus out

**Old**
```
function arCloseDrawer(){
  document.getElementById("arScrim").classList.remove("open");
```
**New**
```
function arCloseDrawer(){
  ehDrawerClosed("arDrawer");
  document.getElementById("arScrim").classList.remove("open");
```
