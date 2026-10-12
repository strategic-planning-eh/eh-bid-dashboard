# Executive Summary charts mirror in Arabic

Generated 2026-10-12 11:21 · 8 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | app | exact | rtl | chart titles sit top-right in Arabic | 1 | ✓ |
| 2 | app | exact | rtl | funnel mirror helper | 1 | ✓ |
| 3 | app | exact | rtl | funnel labels and bars mirror | 1 | ✓ |
| 4 | app | exact | rtl | funnel counts and drops mirror | 1 | ✓ |
| 5 | app | exact | rtl | win-bars mirror helper | 1 | ✓ |
| 6 | app | exact | rtl | win-bars labels and decided bars mirror | 1 | ✓ |
| 7 | app | exact | rtl | win-bars won bars mirror | 1 | ✓ |
| 8 | app | exact | rtl | win-bars counts mirror | 1 | ✓ |

## Edit detail

### 1. app — chart titles sit top-right in Arabic

**Old**
```
function exSvgHead(W,title,sub){ return `<text x="14" y="20" class="exT">${esc(title)}</text>${sub?`<text x="14" y="36" class="exS">${esc(sub)}</text>`:''}`; }
```
**New**
```
// Arabic: mirror x positions and swap text anchors (12 Oct 2026)
function exRTL(W){const R=document.documentElement.dir==='rtl';return {R:R,X:x=>R?W-x:x,A:a=>R?(a==='end'?'start':a==='start'?'end':a):a,B:(x,w)=>R?W-x-w:x};}
function exSvgHead(W,title,sub){ const m=exRTL(W); return `<text x="${m.X(14)}" y="20" text-anchor="${m.A('start')}" class="exT">${esc(title)}</text>${sub?`<text x="${m.X(14)}
```

### 2. app — funnel mirror helper

**Old**
```
 let leak=null,leakI=-1;
 let s=`<svg id="ex-funnel"
```
**New**
```
 let leak=null,leakI=-1; const m=exRTL(W);
 let s=`<svg id="ex-funnel"
```

### 3. app — funnel labels and bars mirror

**Old**
```
  s+=`<text x="${x0-10}" y="${y+20}" text-anchor="end" class="chl">${esc(l)}</text><rect x="${x0}" y="${y+4}" width="${w.toFixed(1)}" height="26" rx="4" fill="${col}"
```
**New**
```
  s+=`<text x="${m.X(x0-10)}" y="${y+20}" text-anchor="${m.A('end')}" class="chl">${esc(l)}</text><rect x="${m.B(x0,w).toFixed(1)}" y="${y+4}" width="${w.toFixed(1)}" height="26" rx="4" fill="${col}"
```

### 4. app — funnel counts and drops mirror

**Old**
```
  s+=`<text x="${x0+w+8}" y="${y+22}" class="chv">${v}</text>${drop!=null?`<text x="${x0+w+8+String(v).length*9+10}" y="${y+22}" class="chs">−${drop}%</text>`:''}`;});
```
**New**
```
  s+=`<text x="${m.X(x0+w+8)}" y="${y+22}" text-anchor="${m.A('start')}" class="chv">${v}</text>${drop!=null?`<text x="${m.X(x0+w+8+String(v).length*9+10)}" y="${y+22}" text-anchor="${m.A('start')}" class="chs" direction="ltr">−${drop}%</text>`:''}`;});
```

### 5. app — win-bars mirror helper

**Old**
```
 let s=`<svg id="${id}" viewBox="0 0 ${W} ${H}" class="ch exsvg">${exSvgHead(W,title,t('Scope','النطاق')+': '+exScopeLabel())}`;
 rows.forEach((r,i)=>{const y=50+i*rh,
```
**New**
```
 const m=exRTL(W);
 let s=`<svg id="${id}" viewBox="0 0 ${W} ${H}" class="ch exsvg">${exSvgHead(W,title,t('Scope','النطاق')+': '+exScopeLabel())}`;
 rows.forEach((r,i)=>{const y=50+i*rh,
```

### 6. app — win-bars labels and decided bars mirror

**Old**
```
  s+=`<text x="${x0-10}" y="${y+19}" text-anchor="end" class="chl">${esc(lab(r))}</text><rect x="${x0}" y="${y+5}" width="${wa.toFixed(1)}"
```
**New**
```
  s+=`<text x="${m.X(x0-10)}" y="${y+19}" text-anchor="${m.A('end')}" class="chl">${esc(lab(r))}</text><rect x="${m.B(x0,wa).toFixed(1)}" y="${y+5}" width="${wa.toFixed(1)}"
```

### 7. app — win-bars won bars mirror

**Old**
```
/><rect x="${x0}" y="${y+5}" width="${ww.toFixed(1)}" height="22" rx="3" fill="${r.grey?EXC.grey:EXC.won}">
```
**New**
```
/><rect x="${m.B(x0,ww).toFixed(1)}" y="${y+5}" width="${ww.toFixed(1)}" height="22" rx="3" fill="${r.grey?EXC.grey:EXC.won}">
```

### 8. app — win-bars counts mirror

**Old**
```
  s+=`<text x="${x0+wa+8}" y="${y+21}" class="chv">${r.won||0}/${r.awarded||0}</text><text x="${x0+wa+8+String((r.won||0)+'/'+(r.awarded||0)).length*9+8}" y="${y+21}" class="chs">
```
**New**
```
  s+=`<text x="${m.X(x0+wa+8)}" y="${y+21}" text-anchor="${m.A('start')}" class="chv" direction="ltr">${r.won||0}/${r.awarded||0}</text><text x="${m.X(x0+wa+8+String((r.won||0)+'/'+(r.awarded||0)).length*9+8)}" y="${y+21}" text-anchor="${m.A('start')}" class="chs">
```
