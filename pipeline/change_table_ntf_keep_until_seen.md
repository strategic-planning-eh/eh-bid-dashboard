# Notification strip keeps items until marked as seen

Generated 2026-11-18 08:59 · 2 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | app.js | exact | ntf-keep | Snapshot no longer overwritten on every load; one-off 7-day recovery | 1 | ✓ |
| 2 | app.js | exact | ntf-keep | "Mark as seen" button + ntfAck() | 1 | ✓ |

## Edit detail

### 1. app.js — Snapshot no longer overwritten on every load; one-off 7-day recovery

**Old**
```
      else if(old.p[k]!==ph[k]) NTF.px.add(k);
    });
  }
  localStorage.setItem('ehb.snap',JSON.stringify({t:th,p:ph,when:new Date().toISOString().slice(0,10)}));
```
**New**
```
      else if(old.p[k]!==ph[k]) NTF.px.add(k);
    });
    if(!old.v){ /* old-style snapshot (was overwritten on every load): recover tenders launched in the last 7 days, once */
      const cut=new Date(Date.now()-7*864e5).toISOString().slice(0,10);
      const base={t:Object.assign({},old.t||{}),p:Object.assign({},old.p||{}),when:cut,v:2};
      BA.bidlist.forEach(b=>{const k=key(b);
        if(
```

### 2. app.js — "Mark as seen" button + ntfAck()

**Old**
```
  '<button onclick="this.parentElement.style.display=\'none\'" style="border:0;background:none;cursor:pointer;font-weight:800;color:#8A7A44;margin-inline-start:auto">\u2715</button>';
}
```
**New**
```
  '<button onclick="ntfAck()" title="'+t('Clears this strip. Until you press it, these items stay listed every time you open the page.','يمسح هذا الشريط. تبقى هذه العناصر ظاهرة في كل مرة تفتح الصفحة حتى تضغط عليه.')+'" style="border:1px solid #D9C88F;background:#fff;border-radius:7px;padding:3px 10px;cursor:pointer;font-weight:700;color:#5C4A14;margin-inline-start:auto">\u2713 '+t('Mark as seen','
```
