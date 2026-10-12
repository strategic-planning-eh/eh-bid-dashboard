# Government Tenders — audit fix shell-20

Generated 2026-10-12 14:24 · 7 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | et | exact | css | shell-20a: own colour pair for open / closed | 1 | ✓ |
| 2 | et | exact | code | shell-20a: stacked bars accept their own colours | 1 | ✓ |
| 3 | et | exact | code | shell-20a: published-per-day chart uses the open / closed pair | 1 | ✓ |
| 4 | et | exact | code | shell-20a: market legend uses the open / closed pair | 1 | ✓ |
| 5 | et | exact | code | shell-20b/c: Region not sortable; text sorts numbers by value | 1 | ✓ |
| 6 | et | exact | code | shell-20b: only sortable headings get a click handler | 1 | ✓ |
| 7 | et | exact | code | shell-20a: by type of work — open / closed colours | 1 | ✓ |

## Edit detail

### 1. et — shell-20a: own colour pair for open / closed

**Old**
```
  --core:var(--eh-c1);--adj:var(--eh-c2);--bar:var(--eh-c1);--bar2:var(--eh-c2);--grid:var(--eh-line);
```
**New**
```
  --core:var(--eh-c1);--adj:var(--eh-c2);--bar:var(--eh-c1);--bar2:var(--eh-c2);--grid:var(--eh-line);
  --open:var(--eh-c5);--closed:var(--eh-grey);   /* audit shell-20: open / closed never reuse the Core / Related colours */
```

### 2. et — shell-20a: stacked bars accept their own colours

**Old**
```
cols=stack?['var(--core)','var(--adj)']:['var(--bar)'];
```
**New**
```
cols=stack?(opt.cols||['var(--core)','var(--adj)']):['var(--bar)'];
```

### 3. et — shell-20a: published-per-day chart uses the open / closed pair

**Old**
```
[{name:L('Still open when checked','مفتوحة عند المراجعة'),color:'var(--core)',vals:DY.map(r=>r.open)},{name:L('Closed','مغلقة'),color:'var(--adj)',vals:DY.map(r=>r.n-r.open)}]
```
**New**
```
[{name:L('Still open when checked','مفتوحة عند المراجعة'),color:'var(--open)',vals:DY.map(r=>r.open)},{name:L('Closed','مغلقة'),color:'var(--closed)',vals:DY.map(r=>r.n-r.open)}]
```

### 4. et — shell-20a: market legend uses the open / closed pair

**Old**
```
<div class="legend"><span><i style="background:var(--core)"></i><span data-en="Still open when checked" data-ar="مفتوحة عند المراجعة">Still open when checked</span></span><span><i style="background:var(--adj)"></i><span data-en="Already closed" data-ar="مغلقة">Already closed</span></span></div>
```
**New**
```
<div class="legend"><span><i style="background:var(--open)"></i><span data-en="Still open when checked" data-ar="مفتوحة عند المراجعة">Still open when checked</span></span><span><i style="background:var(--closed)"></i><span data-en="Already closed" data-ar="مغلقة">Already closed</span></span></div>
```

### 5. et — shell-20b/c: Region not sortable; text sorts numbers by value

**Old**
```
  const k=(C[SORT.k]||C.sub)[1];rows=rows.slice().sort((a,b)=>{const x=k(a),y=k(b);return (x>y?1:x<y?-1:0)*SORT.dir});
  let h=`<table class="t"><thead><tr>${order.map(c=>`<th data-k="${c}" class="${SORT.k===c?'s'+(SORT.dir<0?' up':''):''}">${C[c][0]}</th>`).join('')}</tr></thead><tbody>`;
```
**New**
```
  const k=(C[SORT.k]||C.sub)[1],cmp=(x,y)=>typeof x==='string'&&typeof y==='string'?x.localeCompare(y,LANG==='ar'?'ar':'en',{numeric:true}):(x>y?1:x<y?-1:0);   // audit shell-20c: "No. 8" before "No. 22"
  rows=rows.slice().sort((a,b)=>cmp(k(a),k(b))*SORT.dir);
  let h=`<table class="t"><thead><tr>${order.map(c=>c==='region'?`<th>${C[c][0]}</th>`:`<th data-k="${c}" class="${SORT.k===c?'s'+(SORT.di
```

### 6. et — shell-20b: only sortable headings get a click handler

**Old**
```
  document.querySelectorAll('#list th').forEach(th=>th.onclick=()=>{SORT.dir=(SORT.k===th.dataset.k?-SORT.dir:1);SORT.k=th.dataset.k;render()});
```
**New**
```
  document.querySelectorAll('#list th[data-k]').forEach(th=>th.onclick=()=>{SORT.dir=(SORT.k===th.dataset.k?-SORT.dir:1);SORT.k=th.dataset.k;render()});
```

### 7. et — shell-20a: by type of work — open / closed colours

**Old**
```
{labelW:260});
```
**New**
```
{cols:['var(--open)','var(--closed)'],labelW:260});
```
