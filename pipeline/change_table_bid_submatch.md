# Bid tracker — EH submissions matched across all submission columns

Generated 2026-10-11 16:30 · 5 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | extract | exact | data | map the proposal-date, amendment-date and award-date columns | 1 | ✓ |
| 2 | extract | exact | data | carry proposal, amendment and award dates into bidraw2.json | 1 | ✓ |
| 3 | extract | exact | data | derive EH submission date, its source and any gap between the two records | 1 | ✓ |
| 4 | analytics | exact | data | a proposal date counts as a dated submission | 1 | ✓ |
| 5 | analytics | exact | data | bidlist rows carry the submission evidence the All Tenders tab needs | 1 | ✓ |

## Edit detail

### 1. extract — map the proposal-date, amendment-date and award-date columns

**Old**
```
        elif h.startswith('Status of submission') or h.startswith('حالة التقديم'): m['substatus']=c

```
**New**
```
        elif h.startswith('Status of submission') or h.startswith('حالة التقديم'): m['substatus']=c
        elif h.startswith('العرض الفني') or h.startswith('Technical Proposal'): m['techprop']=c
        elif h.startswith('العرض المالي') or h.startswith('Financial Proposal'): m['finprop']=c
        elif h.startswith('Date of Amendment'): m['amenddate']=c
        elif h.startswith('تاريخ الترسية') 
```

### 2. extract — carry proposal, amendment and award dates into bidraw2.json

**Old**
```
            subdate=subdstr(g('subdate')), substatus=substat(g('substatus')), subcol=('subdate' in m or 'substatus' in m),

```
**New**
```
            subdate=subdstr(g('subdate')), substatus=substat(g('substatus')), subcol=('subdate' in m or 'substatus' in m),
            techdate=subdstr(g('techprop')), findate=subdstr(g('finprop')),
            amenddate=subdstr(g('amenddate')), awarddate=subdstr(g('awarddate')),

```

### 3. extract — derive EH submission date, its source and any gap between the two records

**Old**
```
        b['value']=b['winval'] if b['winval'] else b['offer']
        allbids.append(b)

```
**New**
```
        b['value']=b['winval'] if b['winval'] else b['offer']
        # EH submission date: the tracker's own date first, else the earlier proposal date (11 Oct 2026)
        _pd=sorted(x for x in (b['techdate'],b['findate']) if x)
        b['ehsubdate']=b['subdate'] or (_pd[0] if _pd else None)
        b['subsrc']='tracker' if b['subdate'] else ('proposal' if _pd else None)
        b['subgap']=No
```

### 4. analytics — a proposal date counts as a dated submission

**Old**
```
        if b.get('subdate'): return 'date'

```
**New**
```
        if b.get('ehsubdate') or b.get('subdate'): return 'date'

```

### 5. analytics — bidlist rows carry the submission evidence the All Tenders tab needs

**Old**
```
            deadline=b.get('submit') or None, subdate=b.get('subdate') or None, sub=substate(b),

```
**New**
```
            deadline=b.get('submit') or None, subdate=(b.get('ehsubdate') or b.get('subdate') or None), sub=substate(b),
            subsrc=b.get('subsrc'), subgap=b.get('subgap'), awarddate=b.get('awarddate'),
            submitted=substate(b) in ('date','yes'),
            deadline_stale=bool(b.get('submit') and (b.get('ehsubdate') or b.get('subdate')) and (b.get('ehsubdate') or b.get('subdate')
```
