# Change table — hub: company search shows up to 20 results and matches every typed word

Generated 2026-10-13 10:15 · 4 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | hub | exact | search | Index normalised name, subtitle (tier · region) and a normalised blob incl. region bucket | 1 | ✓ |
| 2 | hub | exact | search | All-words matching, Arabic/Latin normalisation, Arabic names searchable in Latin letters, 20 results ranked starts-with › in name › elsewhere, subtitle per row | 1 | ✓ |
| 3 | hub | exact | search | Enter opens the selected row by its data-n (row now carries a subtitle) | 1 | ✓ |
| 4 | hub | exact | search | Taller, slightly wider list so 20 rows are usable; never wider than the phone screen | 1 | ✓ |

## Edit detail

### 1. hub — Index normalised name, subtitle (tier · region) and a normalised blob incl. region bucket

**Old**
```
    QN=mw.EHX.N.map(function(n){
      return {n:n.n, b:(n.n+' '+(n.typ||'')+' '+(n.sec||'')+' '+(n.reg||'')+' '+(n.city||'')+' '+(n.notes||'')).toLowerCase()};
    });
```
**New**
```
    QN=mw.EHX.N.map(function(n){
      var k=qNorm(n.n), b=qNorm(n.n+' '+(n.typ||'')+' '+(n.sec||'')+' '+(n.reg||'')+' '+(n.rg||'')+' '+(n.city||'')+' '+(n.notes||''));
      return {n:n.n, k:k, kc:qCollapse(k+' '+qRoman(k)), s:[n.tier,n.rg].filter(function(x){return x&&x!=='—';}).join(' · '),
              b:b, bc:qCollapse(b+' '+qRoman(b))};
    });
```

### 2. hub — All-words matching, Arabic/Latin normalisation, Arabic names searchable in Latin letters, 20 results ranked starts-with › in name › elsewhere, subtitle per row

**Old**
```
qEl.addEventListener('input',function(){
  var v=qEl.value.trim().toLowerCase();
  if(!v||!QN){ qHide(); return; }
  var hits=[], rest=[], i;
  for(i=0;i<QN.length;i++){
    if(QN[i].n.toLowerCase().indexOf(v)>-1){ if(hits.length<8) hits.push(QN[i].n); }
    else if(QN[i].b.indexOf(v)>-1){ if(rest.length<8) rest.push(QN[i].n); }
    if(hits.length>=8) break;
  }
  hits=hits.concat(rest).slice(0,8)
```
**New**
```
// Same normalisation as the pipeline: NFKC, Arabic alef/taa/yaa variants unified, tatweel and diacritics dropped, case folded.
function qNorm(s){ s=String(s||''); try{ s=s.normalize('NFKC'); }catch(e){}
  return s.toLowerCase().replace(/[\u0640\u200b-\u200f\u064b-\u0652]/g,'').replace(/[\u0622\u0623\u0625]/g,'\u0627').replace(/\u0629/g,'\u0647').replace(/\u0649/g,'\u064a').replace(/\u0624/g,'\u06
```

### 3. hub — Enter opens the selected row by its data-n (row now carries a subtitle)

**Old**
```
  else if(e.key==='Enter'&&open&&qIdx>-1){ qGo(qD.querySelectorAll('.qh')[qIdx].textContent); e.preventDefault(); }
```
**New**
```
  else if(e.key==='Enter'&&open&&qIdx>-1){ qGo(qD.querySelectorAll('.qh')[qIdx].getAttribute('data-n')); e.preventDefault(); }
```

### 4. hub — Taller, slightly wider list so 20 rows are usable; never wider than the phone screen

**Old**
```
id="qdrop" role="listbox" aria-label="Companies" style="display:none;position:absolute;top:36px;left:0;width:320px;max-height:300px;
```
**New**
```
id="qdrop" role="listbox" aria-label="Companies" style="display:none;position:absolute;top:36px;left:0;width:360px;max-width:92vw;max-height:min(60vh,520px);
```
