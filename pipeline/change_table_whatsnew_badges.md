# Change table — hub: What's New count badges per tab and heading

Generated 2026-10-18 09:19 · 14 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | hub | exact | tabs | Count badge on the fixes tab | 1 | ✓ |
| 2 | hub | exact | tabs | Count badge on the companies tab | 1 | ✓ |
| 3 | hub | exact | tabs | Count badge on the bids tab | 1 | ✓ |
| 4 | hub | exact | tabs | Count badge on the sources tab | 1 | ✓ |
| 5 | hub | exact | style | Badge style (light and dark), sub-heading style | 1 | ✓ |
| 6 | hub | exact | counts | One count per tab; the week chip totals the three update tabs | 1 | ✓ |
| 7 | hub | exact | counts | Refresh tab badges whenever the week changes | 1 | ✓ |
| 8 | hub | exact | fixes | Fixes grouped by part of the hub, each heading with a count | 1 | ✓ |
| 9 | hub | exact | companies | Added split by category (competitors first), each with a count | 1 | ✓ |
| 10 | hub | exact | companies | Removed rows rendered by a shared function | 1 | ✓ |
| 11 | hub | exact | companies | Removed split into merged vs removed, each with a count | 1 | ✓ |
| 12 | hub | exact | bids | Won heading count | 1 | ✓ |
| 13 | hub | exact | bids | Lost heading count | 1 | ✓ |
| 14 | hub | exact | sources | Sources heading: how many were refreshed this week | 1 | ✓ |

## Edit detail

### 1. hub — Count badge on the fixes tab

**Old**
```
onclick="wnTab('fixes')"><span class="tl" data-en="Fixes &amp; features" data-ar="الإصلاحات والميزات">Fixes &amp; features</span></button>
```
**New**
```
onclick="wnTab('fixes')"><span class="tl" data-en="Fixes &amp; features" data-ar="الإصلاحات والميزات">Fixes &amp; features</span><span class="wnc" data-c="fixes" dir="ltr" hidden></span></button>
```

### 2. hub — Count badge on the companies tab

**Old**
```
onclick="wnTab('companies')"><span class="tl" data-en="Companies" data-ar="الشركات">Companies</span></button>
```
**New**
```
onclick="wnTab('companies')"><span class="tl" data-en="Companies" data-ar="الشركات">Companies</span><span class="wnc" data-c="companies" dir="ltr" hidden></span></button>
```

### 3. hub — Count badge on the bids tab

**Old**
```
onclick="wnTab('bids')"><span class="tl" data-en="Bids &amp; Clients" data-ar="المنافسات والعملاء">Bids &amp; Clients</span></button>
```
**New**
```
onclick="wnTab('bids')"><span class="tl" data-en="Bids &amp; Clients" data-ar="المنافسات والعملاء">Bids &amp; Clients</span><span class="wnc" data-c="bids" dir="ltr" hidden></span></button>
```

### 4. hub — Count badge on the sources tab

**Old**
```
onclick="wnTab('sources')"><span class="tl" data-en="Sources" data-ar="المصادر">Sources</span></button>
```
**New**
```
onclick="wnTab('sources')"><span class="tl" data-en="Sources" data-ar="المصادر">Sources</span><span class="wnc" data-c="sources" dir="ltr" hidden></span></button>
```

### 5. hub — Badge style (light and dark), sub-heading style

**Old**
```
.wntab{color:var(--eh-ink-2)}.wntab[aria-selected="true"]{color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}
```
**New**
```
.wntab{color:var(--eh-ink-2)}.wntab[aria-selected="true"]{color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}
.wnc{display:inline-block;min-width:18px;height:18px;line-height:18px;padding:0 5px;border-radius:9px;background:var(--eh-good-bg);color:var(--eh-good);font-size:10.5px;font-weight:800;text-align:center;margin-inline-start:6px;vertical-align:1px;box-sizing:border-box}.wnc[hidden]{
```

### 6. hub — One count per tab; the week chip totals the three update tabs

**Old**
```
function wnCount(w){var d=w.data||{};return (w.fixes||[]).length+(d.added||[]).length+(d.removed||[]).length+(d.merged||[]).length+(d.confidence_up||[]).length+(d.tier_moves||[]).length+((d.bids||{}).won||[]).length+((d.bids||{}).lost||[]).length;}
```
**New**
```
function wnCounts(w){var d=w.data||{},b=d.bids||{},c=d.clients||{},num=function(x){return typeof x==='number'?x:(x&&x.length)||0;};
  var src=(w.sources||[]).filter(function(s){var r=String(s.refreshed||'').slice(0,10);return r&&r>=w.from&&r<=w.to;}).length;
  return {fixes:(w.fixes||[]).length, companies:(d.added||[]).length+(d.removed||[]).filter(function(x){return !(x.reason==='merged');}).leng
```

### 7. hub — Refresh tab badges whenever the week changes

**Old**
```

  wnRenderBody(); }

```
**New**
```

  wnTabCounts(); wnRenderBody(); }

```

### 8. hub — Fixes grouped by part of the hub, each heading with a count

**Old**
```
    h=(w.fixes||[]).map(function(f,i){return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\''+wnEsc(f.app)+'\','+i+')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \u203a '+wnEsc(viewName(f.view)):'')+'</button><br>'+wnEsc(hubL==='ar'?(f.ar||f.en):(f.en||f.ar))+'</div>';}).join('')
```
**New**
```
    var fx=(w.fixes||[]).map(function(f,i){return {f:f,i:i};}), order=['hub','stake','bids','clients','news'], grp={};
    fx.forEach(function(x){var a=APPS[x.f.app]?x.f.app:'hub';(grp[a]=grp[a]||[]).push(x);});
    Object.keys(grp).forEach(function(a){if(order.indexOf(a)<0)order.push(a);});
    h=order.filter(function(a){return grp[a];}).map(function(a){return '<div class="wnh">'+wnEsc(appName(a)
```

### 9. hub — Added split by category (competitors first), each with a count

**Old**
```
    function sec(title,items,fn){ if(!items||!items.length)return ''; return '<div class="wnh">'+title+' \u00b7 <span dir="ltr">'+items.length+'</span></div>'+items.map(fn).join(''); }
    h+=sec(L('Added','أُضيفت'),d.added,function(x){return '<div class="wnitem data">'+coLink(x.n)+(x.typ?' \u00b7 '+wnEsc(x.typ):'')+(x.cat?' \u00b7 '+wnEsc(x.cat):'')+'</div>';});
```
**New**
```
    function sec(title,items,fn,cls){ if(!items||!items.length)return ''; return '<div class="wnh'+(cls?' '+cls:'')+'">'+title+wnBdg(items.length)+'</div>'+items.map(fn).join(''); }
    var CATAR={'Active Competitors':'منافسون نشطون','Direct Competitors':'منافسون مباشرون','Indirect / Adjacent Competitors':'منافسون غير مباشرون / مجاورون','EH Clients':'عملاء آفاق البيئة','Clients / Potential Clients
```

### 10. hub — Removed rows rendered by a shared function

**Old**
```
    h+=sec(L('Removed','أُزيلت'),d.removed,function(x){
```
**New**
```
    var rmFn=function(x){
```

### 11. hub — Removed split into merged vs removed, each with a count

**Old**
```
(x.reason?' \u00b7 '+wnEsc(x.reason):'')+'</div>';});
    h+=sec(L('Data confidence raised'
```
**New**
```
(x.reason&&x.reason!=='merged'?' \u00b7 '+wnEsc(x.reason):'')+'</div>';};
    var rmM=(d.removed||[]).filter(function(x){return x.reason==='merged'||x.alias;}), rmO=(d.removed||[]).filter(function(x){return !(x.reason==='merged'||x.alias);});
    h+=sec(L('Removed from the map','حُذفت من الخريطة'),rmO,rmFn);
    if(!(d.merged||[]).length) h+=sec(L('Merged into another record','دُمجت في سجل آخر'),r
```

### 12. hub — Won heading count

**Old**
```
    if((b.won||[]).length) h+='<div class="wnh">'+L('Won','فاز EH')+'</div>'
```
**New**
```
    if((b.won||[]).length) h+='<div class="wnh">'+L('Won','فاز EH')+wnBdg(b.won.length)+'</div>'
```

### 13. hub — Lost heading count

**Old**
```
    if((b.lost||[]).length) h+='<div class="wnh">'+L('Lost','خسارة')+'</div>'
```
**New**
```
    if((b.lost||[]).length) h+='<div class="wnh">'+L('Lost','خسارة')+wnBdg(b.lost.length)+'</div>'
```

### 14. hub — Sources heading: how many were refreshed this week

**Old**
```
    h=(w.sources||[]).map(function(x){var nt
```
**New**
```
    var srcN=wnCounts(w).sources; h=((w.sources||[]).length?'<div class="wnh">'+L('Refreshed this week','حُدّثت هذا الأسبوع')+wnBdg(srcN)+' \u00b7 '+L('of','من')+' <span dir="ltr">'+w.sources.length+'</span> '+L('sources','مصادر')+'</div>':'')+(w.sources||[]).map(function(x){var nt
```
