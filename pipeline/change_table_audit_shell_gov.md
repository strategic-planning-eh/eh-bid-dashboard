# Regulatory news — audit fixes shell-03/04/19

Generated 2026-10-12 14:23 · 7 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | gov | exact | code | shell-04/19: Gregorian dates in Arabic; ages counted from the collection date; collection time in the page language | 1 | ✓ |
| 2 | gov | exact | code | shell-04: the September 2026 brief is labelled September 2026 in Arabic, not a Hijri month | 1 | ✓ |
| 3 | gov | exact | copy | shell-04: "Collected" time in Arabic | 1 | ✓ |
| 4 | gov | exact | copy | shell-04: Arabic week range reads right to left | 1 | ✓ |
| 5 | gov | exact | code | shell-03: search box keeps focus while typing | 1 | ✓ |
| 6 | gov | exact | code | shell-03: qRender() restores focus and caret | 1 | ✓ |
| 7 | gov | exact | data | shell-19: stories dated after the collection are treated as undated | 1 | ✓ |

## Edit detail

### 1. gov — shell-04/19: Gregorian dates in Arabic; ages counted from the collection date; collection time in the page language

**Old**
```
const fmtD=iso=>{if(!iso)return L('date n/a','بدون تاريخ');const d=new Date(iso+'T00:00:00');return d.toLocaleDateString(LANG==='ar'?'ar-SA-u-nu-latn':'en-GB',{day:'2-digit',month:'short',year:'numeric'});};
const daysAgo=iso=>iso?Math.floor((Date.now()-new Date(iso+'T00:00:00'))/864e5):null;
```
**New**
```
const LOC=()=>LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB';   // Gregorian in Arabic too, as on every hub page (audit shell-04)
const fmtD=iso=>{if(!iso)return L('date n/a','بدون تاريخ');const d=new Date(iso+'T00:00:00');return d.toLocaleDateString(LOC(),{day:'2-digit',month:'short',year:'numeric'});};
// ages are counted from the collection date, not the reader's clock (audit shell-19)
functi
```

### 2. gov — shell-04: the September 2026 brief is labelled September 2026 in Arabic, not a Hijri month

**Old**
```
const monthName=m=>{const [y,mo]=m.split('-');return new Date(+y,+mo-1,1).toLocaleDateString(LANG==='ar'?'ar-SA-u-nu-latn':'en-GB',{month:'long',year:'numeric'});};
```
**New**
```
const monthName=m=>{const [y,mo]=m.split('-');return new Date(+y,+mo-1,1).toLocaleDateString(LOC(),{month:'long',year:'numeric'});};
```

### 3. gov — shell-04: "Collected" time in Arabic

**Old**
```
<span>${L('Collected','تاريخ الجمع')} <b dir="ltr">${esc(FEED.generated_ksa||FEED.generated)}</b></span>
```
**New**
```
<span>${L('Collected','تاريخ الجمع')} <b>${esc(fmtGen())}</b></span>
```

### 4. gov — shell-04: Arabic week range reads right to left

**Old**
```
<b dir="ltr">${fmtD(FEED.week_from)} – ${fmtD(FEED.week_to)}</b>
```
**New**
```
<b>${fmtD(FEED.week_from)} – ${fmtD(FEED.week_to)}</b>
```

### 5. gov — shell-03: search box keeps focus while typing

**Old**
```
<input placeholder="${L('Search headlines…','ابحث في العناوين…')}" value="${esc(S.q)}" oninput="S.q=this.value;render()">
```
**New**
```
<input id="gq" placeholder="${L('Search headlines…','ابحث في العناوين…')}" value="${esc(S.q)}" oninput="S.q=this.value;qRender(this)">
```

### 6. gov — shell-03: qRender() restores focus and caret

**Old**
```
function render(){
 document.querySelectorAll('#lang button')
```
**New**
```
// redraw the list without losing the search box's cursor (audit shell-03)
function qRender(el){const a=el.selectionStart,b=el.selectionEnd;render();const q=$('gq');if(q){q.focus();try{q.setSelectionRange(a,b);}catch(e){}}}
function render(){
 document.querySelectorAll('#lang button')
```

### 7. gov — shell-19: stories dated after the collection are treated as undated

**Old**
```
fetch('gov_news.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();}).then(j=>{FEED=j;render();})
```
**New**
```
fetch('gov_news.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();}).then(j=>{FEED=j;
  const g=genDay();(FEED.items||[]).forEach(it=>{if(it.date&&FEED.generated&&it.date>g){it.date_after_collection=it.date;it.date=null;}});   // a date after the collection cannot be right: treat as undated (audit shell-19)
  render();})
```
