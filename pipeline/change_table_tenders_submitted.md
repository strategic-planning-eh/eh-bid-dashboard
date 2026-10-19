# Change table — All Tenders SUBMITTED outcome

Generated 2026-10-19 14:01 · 8 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | app | exact | tenders-submitted | DOUT + tOut(): Submitted as a displayed outcome | 1 | ✓ |
| 2 | app | exact | tenders-submitted | outcome colours: Submitted teal | 1 | ✓ |
| 3 | app | exact | tenders-submitted | outcome filter matches the shown outcome | 1 | ✓ |
| 4 | app | exact | tenders-submitted | outcome filter lists Submitted | 1 | ✓ |
| 5 | app | exact | tenders-submitted | outcome cell shows SUBMITTED | 1 | ✓ |
| 6 | app | exact | tenders-submitted | CSV export shows Submitted | 1 | ✓ |
| 7 | app | exact | tenders-submitted | cross-tab links show Submitted | 1 | ✓ |
| 8 | app | exact | tenders-submitted | pricing cards: same teal SUBMITTED tag | 1 | ✓ |

## Edit detail

### 1. app — DOUT + tOut(): Submitted as a displayed outcome

**Old**
```
const DOUT={'Won':'فوز','Lost':'خسارة','Not awarded':'لم تتم الترسية','Cancelled':'ملغاة','Pending':'قيد الدراسة'};
```
**New**
```
const DOUT={'Won':'فوز','Lost':'خسارة','Not awarded':'لم تتم الترسية','Cancelled':'ملغاة','Pending':'قيد الدراسة','Submitted':'تم التقديم'};
function tOut(b){return (b.outcome=='Pending'&&tSub(b))?'Submitted':b.outcome;}   // 19 Oct 2026: shown outcome — a pending tender EH submitted reads Submitted
```

### 2. app — outcome colours: Submitted teal

**Old**
```
const OC={'Won':'#2E7A37','Lost':'#B23F2B','Not awarded':'#C98A1B','Cancelled':'#5E6B80','Pending':'#0072BB'};
```
**New**
```
const OC={'Won':'#2E7A37','Lost':'#B23F2B','Not awarded':'#C98A1B','Cancelled':'#5E6B80','Pending':'#0072BB','Submitted':'#0B7F76'};
```

### 3. app — outcome filter matches the shown outcome

**Old**
```
(TF.outcome=='all'||b.outcome==TF.outcome)&&
```
**New**
```
(TF.outcome=='all'||tOut(b)==TF.outcome)&&
```

### 4. app — outcome filter lists Submitted

**Old**
```
const outcomes=['Won','Lost','Not awarded','Cancelled','Pending'].filter(o=>BA.bidlist.some(b=>b.outcome==o));
```
**New**
```
const outcomes=['Won','Lost','Not awarded','Cancelled','Submitted','Pending'].filter(o=>BA.bidlist.some(b=>tOut(b)==o));
```

### 5. app — outcome cell shows SUBMITTED

**Old**
```
<td><span class="tag" style="background:${OC[b.outcome]}">${t(b.outcome.toUpperCase(),DOUT[b.outcome]||b.outcome)}</span>
```
**New**
```
<td><span class="tag" style="background:${OC[tOut(b)]}">${t(tOut(b).toUpperCase(),DOUT[tOut(b)]||tOut(b))}</span>
```

### 6. app — CSV export shows Submitted

**Old**
```
tNeeds(b)?tDaysPast(b):'',b.outcome,b.value||''
```
**New**
```
tNeeds(b)?tDaysPast(b):'',tOut(b),b.value||''
```

### 7. app — cross-tab links show Submitted

**Old**
```
+t(b.outcome,(typeof DOUT!=='undefined'&&DOUT[b.outcome])||b.outcome)+'</a>'
```
**New**
```
+t(tOut(b),(typeof DOUT!=='undefined'&&DOUT[tOut(b)])||tOut(b))+'</a>'
```

### 8. app — pricing cards: same teal SUBMITTED tag

**Old**
```
'<span class="tag" style="background:#E3EEFA;color:#1A5FAB;border:1px solid #1A5FAB">'+t('SUBMITTED','تم التقديم')+'</span>'
```
**New**
```
'<span class="tag" style="background:#0B7F76">'+t('SUBMITTED','تم التقديم')+'</span>'
```
