# All Tenders — submission deadline and EH date of submission

Generated 2026-10-08 14:16 · 10 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | extract | exact | data | parse the date and status of submission | 1 | ✓ |
| 2 | extract | exact | data | map the tracker columns "Date of submission" and "Status of submission" | 1 | ✓ |
| 3 | extract | exact | data | carry the submission fields into bidraw2.json | 1 | ✓ |
| 4 | analytics | exact | data | submission state for each tender | 1 | ✓ |
| 5 | analytics | exact | data | deadline and date of submission in bidlist | 1 | ✓ |
| 6 | analytics | exact | data | import re | 1 | ✓ |
| 7 | app | exact | feature | words for each submission state (EN/AR) and the cell renderer | 1 | ✓ |
| 8 | app | exact | feature | two new cells per tender row | 1 | ✓ |
| 9 | app | exact | feature | two new column headings | 1 | ✓ |
| 10 | app | exact | fix | empty row spans the new columns | 1 | ✓ |

## Edit detail

### 1. extract — parse the date and status of submission

**Old**
```
def mkey(v):

```
**New**
```
def subdstr(v):
    """EH's date of submission: a real date, or text like 11.05.2026 / 11/05/2026 / 2026-05-11. '-' or blank = none."""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime('%Y-%m-%d')
    s=str(v or '').strip()
    mm=re.match(r'^(\d{1,2})[./-](\d{1,2})[./-](\d{4})$',s)
    if mm:
        try: return datetime.date(int(mm.group(3)),int(mm.group(2)),int(mm.group
```

### 2. extract — map the tracker columns "Date of submission" and "Status of submission"

**Old**
```
        if h.startswith('SN#') and 'Year' not in h and 'sn' not in m: m['sn']=c

```
**New**
```
        if h.startswith('SN#') and 'Year' not in h and 'sn' not in m: m['sn']=c
        elif h.startswith('Date of submission') or h.startswith('تاريخ التقديم'): m['subdate']=c
        elif h.startswith('Status of submission') or h.startswith('حالة التقديم'): m['substatus']=c

```

### 3. extract — carry the submission fields into bidraw2.json

**Old**
```
            submit=dstr(g('submit')), submonth=mkey(g('submit')),

```
**New**
```
            submit=dstr(g('submit')), submonth=mkey(g('submit')),
            subdate=subdstr(g('subdate')), substatus=substat(g('substatus')), subcol=('subdate' in m or 'substatus' in m),

```

### 4. analytics — submission state for each tender

**Old**
```
    bidlist=[]
    for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):

```
**New**
```
    def substate(b):
        # Order matters: the tracker's own submission columns first, then the offer evidence, then the reasons.
        if b.get('subdate'): return 'date'
        if b.get('substatus')=='Yes': return 'yes'
        no=b.get('substatus')=='No'
        if not no and (b.get('eh_won') is True or b.get('ehsub') or b.get('offer')): return 'yes'
        if re.search(r'reject|رفض', b.g
```

### 5. analytics — deadline and date of submission in bidlist

**Old**
```
            title=b['title'], client=b['client'], platform=b['platform'],

```
**New**
```
            title=b['title'], client=b['client'], platform=b['platform'],
            deadline=b.get('submit') or None, subdate=b.get('subdate') or None, sub=substate(b),

```

### 6. analytics — import re

**Old**
```
import json, collections, statistics as st

```
**New**
```
import json, collections, re, statistics as st

```

### 7. app — words for each submission state (EN/AR) and the cell renderer

**Old**
```
function renderTenders(){

```
**New**
```
const SUBW={yes:['Submitted — date not recorded','قُدِّم العرض — التاريخ غير مسجّل'],
 no:['EH did not submit','لم تقدّم EH عرضاً'],
 rejected:['EH did not submit — the bid committee said no','لم تقدّم EH عرضاً — رفضت لجنة المنافسات المشاركة'],
 cancelled:['EH did not submit — the tender was cancelled','لم تقدّم EH عرضاً — أُلغيت المنافسة'],
 open:['Not submitted yet — the deadline is still open',
```

### 8. app — two new cells per tender row

**Old**
```
   <td style="font-size:10.5px;color:#7B8A92;white-space:nowrap">${b.date||'\u2014'}</td>

```
**New**
```
   <td style="font-size:10.5px;color:#7B8A92;white-space:nowrap">${b.date||'\u2014'}</td>
   <td style="font-size:10.5px;color:#3A4A52;white-space:nowrap">${b.deadline||`<span style="color:#77868F;font-size:10px;white-space:normal">${t('No deadline recorded','لا موعد مسجّل')}</span>`}</td>
   <td>${subCell(b)}</td>

```

### 9. app — two new column headings

**Old**
```
<th>${t('Launched','الطرح')}</th>
```
**New**
```
<th>${t('Launched','الطرح')}</th><th>${t('Submission deadline','آجال تقديم العروض')}</th><th>${t('EH submitted','تاريخ تقديم EH')}</th>
```

### 10. app — empty row spans the new columns

**Old**
```
'<tr><td colspan="10" style="text-align:center;padding:30px;color:#5F7078">'
```
**New**
```
'<tr><td colspan="12" style="text-align:center;padding:30px;color:#5F7078">'
```
