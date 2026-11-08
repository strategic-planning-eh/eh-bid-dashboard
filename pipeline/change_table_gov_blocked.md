# Regulatory news — blocked status (8 Nov 2026)

Generated 2026-11-08 13:58 · 5 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | gov | exact | status | label for the new blocked status | 1 | ✓ |
| 2 | gov | exact | status | red dot for blocked (base CSS) | 1 | ✓ |
| 3 | gov | exact | status | red dot for blocked (EH skin) | 1 | ✓ |
| 4 | gov | exact | status | body state: blocked when its sources were refused | 1 | ✓ |
| 5 | gov | exact | status | problem count includes blocked sources | 1 | ✓ |

## Edit detail

### 1. gov — label for the new blocked status

**Old**
```
error:['Fetch failed','فشل الجلب'],
```
**New**
```
error:['Fetch failed','فشل الجلب'],blocked:['Refused by the site (access wall) — not a result','رفضه الموقع (حاجز وصول) — ليست نتيجة'],
```

### 2. gov — red dot for blocked (base CSS)

**Old**
```
.dot.st-error{background:var(--red)}.dot.st-skipped
```
**New**
```
.dot.st-error,.dot.st-blocked{background:var(--red)}.dot.st-skipped
```

### 3. gov — red dot for blocked (EH skin)

**Old**
```
body .dot.st-error{background:var(--eh-bad);border-radius:1px;transform:rotate(45deg)}
```
**New**
```
body .dot.st-error{background:var(--eh-bad);border-radius:1px;transform:rotate(45deg)}body .dot.st-blocked{background:var(--eh-bad);border-radius:1px}
```

### 4. gov — body state: blocked when its sources were refused

**Old**
```
 if(b.robots_disallow&&ss.every(s=>s.type==='spa'&&s.status!=='ok'))return ss.some(s=>s.status==='error')?'error':'empty';
 if(ss.some(s=>s.status==='empty'))return 'empty';
```
**New**
```
 if(ss.every(s=>s.status==='blocked'))return 'blocked';
 if(b.robots_disallow&&ss.every(s=>s.type==='spa'&&s.status!=='ok'))return ss.some(s=>s.status==='error')?'error':ss.some(s=>s.status==='blocked')?'blocked':'empty';
 if(ss.some(s=>s.status==='empty'))return 'empty';
```

### 5. gov — problem count includes blocked sources

**Old**
```
problems=bodies.reduce((n,b)=>n+(b.sources||[]).filter(s=>s.status==='error').length,0);
```
**New**
```
problems=bodies.reduce((n,b)=>n+(b.sources||[]).filter(s=>s.status==='error'||s.status==='blocked').length,0);
```
