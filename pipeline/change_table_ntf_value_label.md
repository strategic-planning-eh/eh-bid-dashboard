# New-tender strip value label

Generated 2026-11-18 08:51 · 2 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | app.js | exact | ntf-value | Strip uses the new label | 1 | ✓ |
| 2 | app.js | exact | ntf-value | ntfNewLabel(): count of valued tenders beside the SAR figure | 1 | ✓ |

## Edit detail

### 1. app.js — Strip uses the new label

**Old**
```
   const val=BA.bidlist.filter(b=>NTF.nw.has(b.year+'-'+b.sn)).reduce((a,b)=>a+(b.value||0),0);
   parts.push('<a style="'+lk+'" onclick="jumpTo(\'tenders\',\'nw\')">'+NTF.nw.size+t(' new tender(s)',' منافسة/منافسات جديدة')+(val?' ('+fmtSAR(val)+')':'')+'</a>');
```
**New**
```
   parts.push('<a style="'+lk+'" onclick="jumpTo(\'tenders\',\'nw\')">'+ntfNewLabel()+'</a>');
```

### 2. app.js — ntfNewLabel(): count of valued tenders beside the SAR figure

**Old**
```
function rNtf(){
```
**New**
```
function ntfNewLabel(){
 /* 18 Nov 2026: say how many of the new tenders the SAR figure covers; a price under SAR 100 is a per-unit rate, not a total */
 var n=NTF.nw.size, rows=BA.bidlist.filter(function(b){return NTF.nw.has(b.year+'-'+b.sn);});
 var withV=rows.filter(function(b){return (b.value||0)>=100;}), val=withV.reduce(function(a,b){return a+b.value;},0), k=withV.length, z=n-k;
 var head=n=
```
