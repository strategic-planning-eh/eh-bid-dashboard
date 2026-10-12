# Arabic swap ignores the reading-floor font size

Generated 2026-10-12 11:23 · 3 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | ar | exact | fix | style-insensitive lookup table | 1 | ✓ |
| 2 | ar | exact | fix | fall back to the style-insensitive match | 1 | ✓ |
| 3 | ar | exact | fix | Arabic label for Other in chart B | 1 | ✓ |

## Edit detail

### 1. ar — style-insensitive lookup table

**Old**
```
  var normH=function(h){ return String(h).replace(/\s+/g,' ').trim(); };

```
**New**
```
  var normH=function(h){ return String(h).replace(/\s+/g,' ').trim(); };
  /* 12 Oct 2026: match a block even when the reading floor has added an inline font size (style attributes ignored) */
  var noSt=function(h){ return normH(String(h).replace(/\s+style="[^"]*"/g,'')); };
  var FULLN=null; if(FULL){ FULLN={}; for(var fk in FULL){ if(fk.indexOf('#text:')!==0) FULLN[noSt(fk)]=FULL[fk]; } }

```

### 2. ar — fall back to the style-insensitive match

**Old**
```
var k=normH(el.innerHTML); var v=FULL[k];
```
**New**
```
var k=normH(el.innerHTML); var v=FULL[k]; if(v==null&&FULLN) v=FULLN[noSt(el.innerHTML)];
```

### 3. ar — Arabic label for Other in chart B

**Old**
```
'Salaries':'الرواتب',
```
**New**
```
'Salaries':'الرواتب','Other':'أخرى',
```
