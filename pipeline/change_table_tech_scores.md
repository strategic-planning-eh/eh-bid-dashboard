# Bid sheets — technical scores (2026 #87)

Generated 2026-10-12 11:20 · 12 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | rost | exact | data | read technical scores from the notes column of each bid sheet | 1 | ✓ |
| 2 | rost | exact | data | collect technical scores per tender | 1 | ✓ |
| 3 | rost | exact | data | technical score store | 1 | ✓ |
| 4 | rost | exact | data | write techscores.json | 1 | ✓ |
| 5 | ana | exact | data | load technical scores | 1 | ✓ |
| 6 | ana | exact | data | attach technical scores to each bidder | 1 | ✓ |
| 7 | ana | exact | data | EH technical score, best score and place per tender | 1 | ✓ |
| 8 | app | exact | feature | Technical column in the tender row | 1 | ✓ |
| 9 | app | exact | feature | technical score helper for bidder lines | 1 | ✓ |
| 10 | app | exact | feature | score beside each priced bidder | 1 | ✓ |
| 11 | app | exact | feature | score beside each bidder whose price was not disclosed | 1 | ✓ |
| 12 | app | exact | feature | score beside a disqualified bidder | 1 | ✓ |

## Edit detail

### 1. rost — read technical scores from the notes column of each bid sheet

**Old**
```
    return out if len(out)>=2 else None

```
**New**
```
    return out if len(out)>=2 else None

TECHH=['ملاحظات','الملاحظات','remarks','notes','note','النتيجه الفنيه','التقييم الفني','technical']
def tech_scores(rs):
    """Each bidder's technical result from the notes column, e.g. «حاصل على نسبة (87%)» → 87.0 (12 Oct 2026)."""
    maxr=min(rs.max_row,500); maxc=rs.max_column
    grid=[[rs.cell(r+1,c+1).value for c in range(maxc)] for r in range(maxr)
```

### 2. rost — collect technical scores per tender

**Old**
```
            r=parse(wb[sh])
            if r: allr[f'{yr}-{sn}']=r

```
**New**
```
            r=parse(wb[sh])
            if r: allr[f'{yr}-{sn}']=r
            ts=tech_scores(wb[sh])
            if ts: tech[f'{yr}-{sn}']=ts

```

### 3. rost — technical score store

**Old**
```
    allr={}
    for f,yr in
```
**New**
```
    allr={}; tech={}
    for f,yr in
```

### 4. rost — write techscores.json

**Old**
```
    json.dump(allr, open('rosters_all.json','w'), ensure_ascii=False)

```
**New**
```
    json.dump(allr, open('rosters_all.json','w'), ensure_ascii=False)
    json.dump(tech, open('techscores.json','w'), ensure_ascii=False)   # 12 Oct 2026: technical scores by tender and bidder
    print('Technical scores:', {k: len(v) for k, v in tech.items()} or 'none recorded')

```

### 5. ana — load technical scores

**Old**
```
_ALLR=json.load(open('rosters_all.json'))

```
**New**
```
_ALLR=json.load(open('rosters_all.json'))
import os as _os2
_TECH=json.load(open('techscores.json')) if _os2.path.exists('techscores.json') else {}   # 12 Oct 2026
def _tcanon(s):
    t=str(s or '').strip().lower()
    for a,b in (('أ','ا'),('إ','ا'),('آ','ا'),('ة','ه'),('ى','ي'),('','')): t=t.replace(a,b)
    return ' '.join(re.sub(r'[^\w\u0600-\u06FF ]',' ',t).split())

```

### 6. ana — attach technical scores to each bidder

**Old**
```
        has_full=(ehp is not None and n_priced>=2)

```
**New**
```
        # technical scores from the bid sheet's notes column (12 Oct 2026); matched by bidder name as written
        _ts={_tcanon(k):v for k,v in (_TECH.get(key) or {}).items()}
        if _ts:
            _rawn=None
            for bl in blist:
                src=next((n for n,a,dq,e in work if (('Environmental Horizons (EH)' if e else n)==bl['name'])),bl['name'])
                bl['tech']=_ts
```

### 7. ana — EH technical score, best score and place per tender

**Old**
```
            bidders=blist,dq_count=len(dqd),undisc_count=len(undisc),level=('full' if has_full else 'partial')))

```
**New**
```
            bidders=blist,dq_count=len(dqd),undisc_count=len(undisc),level=('full' if has_full else 'partial'),
            tech_eh=_eht,tech_best=(max(_sc) if _sc else None),tech_n=len(_sc),
            tech_rank=(1+sum(1 for x in _sc if x>_eht) if _eht is not None else None)))

```

### 8. app — Technical column in the tender row

**Old**
```
       <div style="text-align:center"><div style="font-size:9px;color:#5F7078;text-transform:uppercase">${t('vs Low','مقابل الأدنى')}</div>
```
**New**
```
       ${r.tech_n?`<div style="text-align:center" title="${esc(t('EH technical score and place among the '+r.tech_n+' scored bidders; best score '+r.tech_best+'%','الدرجة الفنية ل EH وترتيبها بين '+r.tech_n+' متقدمين لهم درجة؛ أعلى درجة '+r.tech_best+'%'))}"><div style="font-size:9px;color:#5F7078;text-transform:uppercase">${t('Technical','الفني')}</div><div style="font-weight:700;font-size:12.5px
```

### 9. app — technical score helper for bidder lines

**Old**
```
   const bars=r.bidders.map(b=>{

```
**New**
```
   const tch=b=>b.tech!=null?` <span title="${esc(t('Technical score','الدرجة الفنية'))}" style="font-size:10.5px;font-weight:600;color:${b.tech>=(r.tech_best||101)?'#2E7D46':'#5F7078'};white-space:nowrap">${t('tech ','فني ')}<span dir="ltr">${b.tech}%</span></span>`:'';
   const bars=r.bidders.map(b=>{

```

### 10. app — score beside each priced bidder

**Old**
```
${b.lowest?'\u25bc ':''}${esc(b.name)}</div>
```
**New**
```
${b.lowest?'\u25bc ':''}${esc(b.name)}</div>${b.tech!=null?`<div style="min-width:58px">${tch(b)}</div>`:(r.tech_n?'<div style="min-width:58px"></div>':'')}
```

### 11. app — score beside each bidder whose price was not disclosed

**Old**
```
white-space:nowrap" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(90deg
```
**New**
```
white-space:nowrap" dir="auto">${esc(b.name)}</div>${r.tech_n?`<div style="min-width:58px">${tch(b)}</div>`:''}<div style="flex:1;height:15px;background:repeating-linear-gradient(90deg
```

### 12. app — score beside a disqualified bidder

**Old**
```
text-align:right" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(45deg
```
**New**
```
text-align:right" dir="auto">${esc(b.name)}</div>${r.tech_n?`<div style="min-width:58px">${tch(b)}</div>`:''}<div style="flex:1;height:15px;background:repeating-linear-gradient(45deg
```
