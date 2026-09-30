# Change table — Environment Fund builder wording

Generated 2026-09-30 08:19 · 9 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 2 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 3 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 4 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 5 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 6 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 7 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 8 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |
| 9 | build_ef_page.py | exact | plain | Environment Fund page wording | 1 | ✓ |

## Edit detail

### 1. build_ef_page.py — Environment Fund page wording

**Old**
```
L('bid-tracker cross-reference as of','مطابقة جدول العطاءات حتى')
```
**New**
```
L('checked against EH\'s bid tracker on','مطابقة جدول العطاءات حتى')
```

### 2. build_ef_page.py — Environment Fund page wording

**Old**
```
'What it means for EH — filed by question, tagged by horizon and owner'
```
**New**
```
'What it means for EH — grouped by question, with when it matters and who at EH acts'
```

### 3. build_ef_page.py — Environment Fund page wording

**Old**
```
'Events calendar for BD attendance'
```
**New**
```
'Events Business Development should attend'
```

### 4. build_ef_page.py — Environment Fund page wording

**Old**
```
'log scale — bar lengths are not proportional'
```
**New**
```
'compressed scale so large and small numbers fit — bar lengths are not to scale'
```

### 5. build_ef_page.py — Environment Fund page wording

**Old**
```
'Extraction ledger — every figure with its page'
```
**New**
```
'Every figure and the page it comes from'
```

### 6. build_ef_page.py — Environment Fund page wording

**Old**
```
'Loan support, guarantees and impact investment reach EH directly; grants, PPP, fees and shared services reach EH through the centres it is licensed by and bids to.'
```
**New**
```
'Loan support, guarantees and impact investment reach EH directly; grants, partnerships with private companies, fees and shared services reach EH through the centres that license it and that it bids to.'
```

### 7. build_ef_page.py — Environment Fund page wording

**Old**
```
${esc(L(o.owner,OWN[o.owner]||o.owner))}
```
**New**
```
${esc(L(OWN_EN[o.owner]||o.owner,OWN[o.owner]||o.owner))}
```

### 8. build_ef_page.py — Environment Fund page wording

**Old**
```
const OWN={
```
**New**
```
const OWN_EN={'BD':'Business Development','Consulting/EIA':'Consulting / environmental studies'};
const OWN={
```

### 9. build_ef_page.py — Environment Fund page wording

**Old**
```
$('kstrip').innerHTML=EF.headline.map(
```
**New**
```
/* NAMES_LINE: every agency in full once per page (agreed 30 Sep 2026), then the short form */
 $('stamp').insertAdjacentHTML('afterend','');
 (function(){let el=document.getElementById('names');if(!el){el=document.createElement('div');el.id='names';el.className='note';el.style.cssText='margin:-4px 0 12px;font-size:12px';$('kstrip').parentNode.insertBefore(el,$('kstrip'));}
  el.innerHTML=L('<b>Na
```
