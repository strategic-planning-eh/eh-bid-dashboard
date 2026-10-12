# Audit fixes (J1) — bid pipeline

Generated 2026-10-12 14:35 · 37 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | nc | exact | data | roster labels and sheet titles are not company names (single guard) | 1 | ✓ |
| 2 | rost | exact | data | over-long names are cut to one name instead of dropped | 1 | ✓ |
| 3 | rost | exact | data | pick the applicant list, not the award table | 1 | ✓ |
| 4 | rost | exact | data | store the clipped name | 1 | ✓ |
| 5 | rost | exact | data | technical scores keyed by the same clipped name | 1 | ✓ |
| 6 | comp | exact | data | shared roster fill (VAT basis), same-firm alias and keep-apart list | 1 | ✓ |
| 7 | comp | exact | data | winner key uses the same-firm alias | 1 | ✓ |
| 8 | comp | exact | data | undercut / priced-vs-EH counted on the filled-in rows | 1 | ✓ |
| 9 | comp | exact | data | keep-apart list honoured by the fuzzy merge | 1 | ✓ |
| 10 | ext | exact | data | duration parser: days / weeks / years to months | 1 | ✓ |
| 11 | ext | exact | data | read the text duration column | 1 | ✓ |
| 12 | ext | exact | data | read the offer-with-VAT column | 1 | ✓ |
| 13 | ext | exact | data | duration in months from either duration column | 1 | ✓ |
| 14 | ext | exact | data | offer with VAT | 1 | ✓ |
| 15 | ext | exact | data | override keeps the VAT figure consistent | 1 | ✓ |
| 16 | ext | exact | data | corrections keep the VAT figure consistent | 1 | ✓ |
| 17 | ext | exact | data | fill offer_vat | 1 | ✓ |
| 18 | ana | exact | data | winner list passed in memory | 1 | ✓ |
| 19 | ana | exact | data | win/loss slices no longer double-count losses | 1 | ✓ |
| 20 | ana | exact | data | duration bands accept decimal months | 1 | ✓ |
| 21 | ana | exact | data | duration stats keep one decimal | 1 | ✓ |
| 22 | ana | exact | data | use the winner list built in this run | 1 | ✓ |
| 23 | ana | exact | data | pricing cards use the shared VAT-basis fill | 1 | ✓ |
| 24 | ana | exact | data | rank only with two or more prices | 1 | ✓ |
| 25 | ana | exact | data | gap only with two or more prices | 1 | ✓ |
| 26 | ana | exact | data | bidder rank only with two or more prices | 1 | ✓ |
| 27 | ana | exact | data | 2-point cards on the VAT basis | 1 | ✓ |
| 28 | ana | exact | data | 2-point cards: field size from the tracker or unknown | 1 | ✓ |
| 29 | ana | exact | data | single-price won cards: no invented rank, gap or bidder count | 1 | ✓ |
| 30 | ana | exact | data | single-price lost cards: no invented bidder count | 1 | ✓ |
| 31 | ana | exact | data | text-flagged cards: no invented bidder count | 1 | ✓ |
| 32 | ana | exact | data | VAT basis flag and shared-tender count | 1 | ✓ |
| 33 | ana | exact | data | client value = EH offers only | 1 | ✓ |
| 34 | ana | exact | data | client years from all data | 1 | ✓ |
| 35 | ana | exact | data | new / lapsed flags independent of scope | 1 | ✓ |
| 36 | ana | exact | data | bid list keeps decimal months | 1 | ✓ |
| 37 | ana | exact | data | pass the winner list in memory | 1 | ✓ |

## Edit detail

### 1. nc — roster labels and sheet titles are not company names (single guard)

**Old**
```
def looks_like_company(s):
    t = _n(s)
    return bool(t) and 3 <= len(t) <= 120 and not is_reason_text(t) and not is_tender_title(t) and bool(re.search(r'[a-z\u0600-\u06ff]{3,}', t))

```
**New**
```
# Etimad award-report labels and roster headings that sit in the bidder-name column (12 Oct 2026, audit bids-06 / data-15)
LABEL_PHRASES = ['حالة الترسية', 'مستبعد من الترسية', 'سبب الاستبعاد', 'سبب عدم الترسية', 'تقرير الترسية', 'تقرير الموردين', 'تقرير فتح العروض',
                 'قائمة الموردين', 'عدد الموردين', 'اسم المورد', 'قيمة الترسية', 'نوع الترسية', 'ترسية كاملة', 'ترسية جزئية',
      
```

### 2. rost — over-long names are cut to one name instead of dropped

**Old**
```
def is_name(v):
    if not isinstance(v,str): return False
    t=v.strip()
    if len(t)<6 or len(t)>90: return False

```
**New**
```
def clip_name(v):
    """A name cell over 90 characters (the name pasted twice, or a long legal suffix) is cut to one name (12 Oct 2026)."""
    t=re.sub(r'\s+',' ',str(v)).strip()
    if len(t)<=90: return t
    w=t.split()
    for i in range(2,len(w)-1):
        if w[i:i+2]==w[0:2] or w[i:i+2]==w[1:3]: return ' '.join(w[:i])      # second copy starts here
    out=''
    for x in w:
        if le
```

### 3. rost — pick the applicant list, not the award table

**Old**
```
    nc=None
    for c in range(maxc):
        for r in range(min(12,maxr)):
            h=norm_ar(grid[r][c])
            if any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','supplier','اسم العارض','المورد']) and not any(d in h for d in DESC):
                nc=c; break
        if nc is not None: break

```
**New**
```
    # 12 Oct 2026 (audit bids-07): award-report sheets (Bid#25, Bid#27) carry two bidder-name headers, the award table and the
    # applicant list; the column with the most company names is the roster.
    nc=None; hcols=[]
    for c in range(maxc):
        for r in range(min(12,maxr)):
            h=norm_ar(grid[r][c])
            if any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','
```

### 4. rost — store the clipped name

**Old**
```
        nm=row[nc]
        if not is_name(nm): continue
        k=canon(nm)[:40]

```
**New**
```
        nm=row[nc]
        if not is_name(nm): continue
        nm=clip_name(nm)
        k=canon(nm)[:40]

```

### 5. rost — technical scores keyed by the same clipped name

**Old**
```
        if sc is not None and 0<=sc<=100: out[str(nm).strip()]=sc

```
**New**
```
        if sc is not None and 0<=sc<=100: out[clip_name(nm)]=sc

```

### 6. comp — shared roster fill (VAT basis), same-firm alias and keep-apart list

**Old**
```
from parse_rosters import norm_ar, canon, is_eh

```
**New**
```
from parse_rosters import norm_ar, canon, is_eh

# ---- one firm under two spellings / two firms that look alike (12 Oct 2026, audit bids-19 / data-17) ----
SAME_FIRM={canon('شركة الدكتور على الدهيمان للاستشارات البيئية'): canon('شركة د علي صالح الدهيمان للاستشارات البيئية')}
KEEP_APART=[['رواد الاستدامه','رائدات الاستدامه','رموز الاستدامه']]   # distinct firms: never merged by the fuzzy step
def 
```

### 7. comp — winner key uses the same-firm alias

**Old**
```
        return canon(best) if bestov>=2 else None

```
**New**
```
        return ckey(best) if bestov>=2 else None

```

### 8. comp — undercut / priced-vs-EH counted on the filled-in rows

**Old**
```
        if not any(x[3] for x in bidders): continue   # EH must be present
        ehp=next((a for nm,a,dq,e in bidders if e and a and not dq), None)
        wc=winner_canon.get(key)
        for nm,a,dq,e in bidders:
            if e: continue   # skip EH itself
            c=canon(nm)

```
**New**
```
        if not any(x[3] for x in bidders): continue   # EH must be present
        yr,sn=key.split('-'); b=bidx.get((int(yr),int(sn)))
        wc=winner_canon.get(key)
        work,_=fill_roster(bidders, b, wc)            # same filled-in prices as the pricing cards (12 Oct 2026, audit bids-08)
        ehp=next((a for nm,a,dq,e,ad in work if e and a and not dq), None)
        for nm,a,dq,e,added i
```

### 9. comp — keep-apart list honoured by the fuzzy merge

**Old**
```
            if k2==k or k2 in merged_into: continue
            if sim(dn, dispname(k2))>=0.85:

```
**New**
```
            if k2==k or k2 in merged_into: continue
            _a,_b=_apart(dn),_apart(dispname(k2))
            if _a and _b and _a!=_b: continue      # listed as different firms
            if sim(dn, dispname(k2))>=0.85:

```

### 10. ext — duration parser: days / weeks / years to months

**Old**
```
def mkey(v):

```
**New**
```
def dur_months(v):
    """Project length in months, one decimal (12 Oct 2026, audit data-12). Numbers are months; text such as «10 ايام»,
    «3 اسابيع», «2.5 سنتين ونصف», «شهرين» or «Annual» is converted. None when no length can be read («مرة واحدة»)."""
    if v is None: return None
    if isinstance(v,(int,float)): return round(float(v),1) if (v==v and v>0) else None
    s=unicodedata.normalize
```

### 11. ext — read the text duration column

**Old**
```
        elif 'Project Duration (Month)' in h: m['dur']=c

```
**New**
```
        elif 'Project Duration (Month)' in h: m['dur']=c
        elif h.startswith('Project Duration'): m['dur2']=c          # text duration (col 7), used when col 6 is empty

```

### 12. ext — read the offer-with-VAT column

**Old**
```
        elif 'قيمة العرض المالي المقدم (بدون' in h: m['offer']=c

```
**New**
```
        elif 'قيمة العرض المالي المقدم (بدون' in h: m['offer']=c
        elif 'قيمة العرض المالي المقدم (+' in h: m['offer_vat']=c     # with VAT — the basis of Etimad roster and award prices

```

### 13. ext — duration in months from either duration column

**Old**
```
            dur=num(g('dur')),

```
**New**
```
            dur=(dur_months(g('dur')) if dur_months(g('dur')) is not None else dur_months(g('dur2'))),

```

### 14. ext — offer with VAT

**Old**
```
            offer=num(g('offer')),

```
**New**
```
            offer=num(g('offer')),
            offer_vat=num(g('offer_vat')),

```

### 15. ext — override keeps the VAT figure consistent

**Old**
```
    _o=OVERRIDES.get((_b['year'],_b['sn']))
    if _o: _b.update(_o)

```
**New**
```
    _o=OVERRIDES.get((_b['year'],_b['sn']))
    if _o:
        _b.update(_o)
        if 'offer' in _o and 'offer_vat' not in _o: _b['offer_vat']=None   # re-derived below

```

### 16. ext — corrections keep the VAT figure consistent

**Old**
```
            _b=_byk[_k]; _b.update(_fields); _nu+=1

```
**New**
```
            _b=_byk[_k]; _b.update(_fields); _nu+=1
            if 'offer' in _fields and 'offer_vat' not in _fields: _b['offer_vat']=None   # re-derived below

```

### 17. ext — fill offer_vat

**Old**
```
json.dump({'bids':allbids,'rosters':rosters}, open('bidraw2.json','w'), ensure_ascii=False)

```
**New**
```
# offer with VAT: the tracker's own figure where it is a number, else the pre-VAT offer × 1.15 (12 Oct 2026, audit bids-03)
for _b in allbids:
    if not _b.get('offer'): _b['offer_vat']=None
    elif not _b.get('offer_vat') or _b['offer_vat']<100: _b['offer_vat']=round(_b['offer']*1.15,2)
json.dump({'bids':allbids,'rosters':rosters}, open('bidraw2.json','w'), ensure_ascii=False)

```

### 18. ana — winner list passed in memory

**Old**
```
def compute(bids, rfull, comp):

```
**New**
```
def compute(bids, rfull, comp, wcanon=None):

```

### 19. ana — win/loss slices no longer double-count losses

**Old**
```
     not_awarded=sum(1 for b in bids if b['status']=='Not awarded'),

```
**New**
```
     # «لم تتم الترسية» rows are EH's losses and already sit in awarded_other; only an undecided one is 'not awarded'
     not_awarded=sum(1 for b in bids if b['status']=='Not awarded' and not b['decided']),   # 12 Oct 2026, audit bids-04
     pending=sum(1 for b in bids if not b['decided'] and b['status'] not in ('Cancelled','Not awarded')),

```

### 20. ana — duration bands accept decimal months

**Old**
```
    durs=[b['dur'] for b in bids if b['dur']]
    dur_bands=[('≤3 mo',0,3),('4–6 mo',4,6),('7–12 mo',7,12),('13–24 mo',13,24),('25+ mo',25,999)]
    duration=[]
    for lbl,lo,hi in dur_bands:
        bb=[b for b in bids if b['dur'] and lo<=b['dur']<=hi]

```
**New**
```
    durs=[b['dur'] for b in bids if b['dur']]
    dur_bands=[('≤3 mo',0,3),('4–6 mo',3,6),('7–12 mo',6,12),('13–24 mo',12,24),('25+ mo',24,999)]   # months may be decimal (12 Oct 2026)
    duration=[]
    for lbl,lo,hi in dur_bands:
        bb=[b for b in bids if b['dur'] and lo<b['dur']<=hi]

```

### 21. ana — duration stats keep one decimal

**Old**
```
    dur_stats=dict(median=round(st.median(durs)) if durs else 0, mean=round(st.mean(durs),1) if durs else 0, max=int(max(durs)) if durs else 0)

```
**New**
```
    dur_stats=dict(median=round(st.median(durs),1) if durs else 0, mean=round(st.mean(durs),1) if durs else 0, max=round(max(durs),1) if durs else 0)

```

### 22. ana — use the winner list built in this run

**Old**
```
    winner_canon=json.load(open('winner_canon.json'))

```
**New**
```
    winner_canon=wcanon if wcanon is not None else json.load(open('winner_canon.json'))   # 12 Oct 2026: in memory, never a stale file

```

### 23. ana — pricing cards use the shared VAT-basis fill

**Old**
```
        eh_offer=(bb['offer'] if bb else None)     # قيمة العرض
        award=(bb['winval'] if bb else None)        # قيمة الترسية
        winner=(bb['winner'] if bb else None)
        wc=winner_canon.get(key)                    # '__EH__', canon string, or None
        def _is_w(nm,e,wc=wc):
            if wc=='__EH__': return bool(e)
            if wc: return _canon(nm)==wc
            return Fa
```
**New**
```
        award=(bb['winval'] if bb else None)        # قيمة الترسية (Etimad award value, VAT included)
        wc=winner_canon.get(key)                    # '__EH__', canon string, or None
        # One VAT basis (12 Oct 2026, audit bids-03): roster and award prices include VAT, so EH's tracker offer is taken from
        # the «(+ ضريبة القيمة المضافة)» column. build_competitors.fill_roster is sha
```

### 24. ana — rank only with two or more prices

**Old**
```
        rank=(prices.index(ehp)+1) if ehp is not None else None

```
**New**
```
        rank=(prices.index(ehp)+1) if (ehp is not None and n_priced>=2) else None   # no rank against an unknown field (audit bids-13)

```

### 25. ana — gap only with two or more prices

**Old**
```
        gap=round(100*(ehp-lo)/lo,1) if (ehp is not None and lo) else None

```
**New**
```
        gap=round(100*(ehp-lo)/lo,1) if (ehp is not None and lo and n_priced>=2) else None

```

### 26. ana — bidder rank only with two or more prices

**Old**
```
            blist.append(dict(name=('Environmental Horizons (EH)' if e else n),price=round(a),dq=False,undisclosed=False,eh=bool(e),rank=i2+1,lowest=(i2==0 and n_priced>1),won=_is_w(n,e)))

```
**New**
```
            blist.append(dict(name=('Environmental Horizons (EH)' if e else n),price=round(a),dq=False,undisclosed=False,eh=bool(e),rank=(i2+1 if n_priced>1 else None),lowest=(i2==0 and n_priced>1),won=_is_w(n,e)))

```

### 27. ana — 2-point cards on the VAT basis

**Old**
```
        offer=bb['offer']; wv=bb['winval']; wn=bb['winner']

```
**New**
```
        offer=_BC.eh_price_vat(bb); wv=bb['winval']; wn=bb['winner']     # VAT included, like the award value

```

### 28. ana — 2-point cards: field size from the tracker or unknown

**Old**
```
        price_rows.append(dict(sn=sn2,year=yr2,eh=ehp,low=round(lo),high=round(hi),avg=round(avg),
            rank=rank,n=2,n_priced=2,gap=gap,
```
**New**
```
        price_rows.append(dict(sn=sn2,year=yr2,eh=ehp,low=round(lo),high=round(hi),avg=round(avg),
            rank=rank,n=(int(bb['nbid']) if bb.get('nbid') else None),n_priced=2,gap=gap,
```

### 29. ana — single-price won cards: no invented rank, gap or bidder count

**Old**
```
        if bb.get('eh_won') is True and (bb.get('winval') or bb.get('offer')):
            ehp=round(bb.get('winval') or bb.get('offer'))
            blist=[dict(name='Environmental Horizons (EH)',price=ehp,dq=False,undisclosed=False,eh=True,rank=1,lowest=True,won=True)]
            price_rows.append(dict(sn=sn3,year=yr3,eh=ehp,low=ehp,high=ehp,avg=ehp,
                rank=1,n=(nb or 1),n_priced=
```
**New**
```
        if bb.get('eh_won') is True and (bb.get('winval') or bb.get('offer')):
            ehp=round(_BC.eh_price_vat(bb) or bb.get('winval'))   # EH's offer with VAT; the award value only when no offer
            blist=[dict(name='Environmental Horizons (EH)',price=ehp,dq=False,undisclosed=False,eh=True,rank=None,lowest=False,won=True)]
            price_rows.append(dict(sn=sn3,year=yr3,eh=ehp,l
```

### 30. ana — single-price lost cards: no invented bidder count

**Old**
```
            blist=[dict(name=bb['winner'],price=wvr,dq=False,undisclosed=False,eh=False,rank=1,lowest=True,won=True)]
            price_rows.append(dict(sn=sn3,year=yr3,eh=None,low=wvr,high=wvr,avg=wvr,
                rank=None,n=(nb or 1),
```
**New**
```
            blist=[dict(name=bb['winner'],price=wvr,dq=False,undisclosed=False,eh=False,rank=None,lowest=False,won=True)]
            price_rows.append(dict(sn=sn3,year=yr3,eh=None,low=wvr,high=wvr,avg=wvr,
                rank=None,n=nb,
```

### 31. ana — text-flagged cards: no invented bidder count

**Old**
```
            rank=None,n=(nb4 or 1),n_priced=0,
```
**New**
```
            rank=None,n=nb4,n_priced=0,
```

### 32. ana — VAT basis flag and shared-tender count

**Old**
```
        total_bidders=sum(r['n_priced'] for r in price_rows),

```
**New**
```
        total_bidders=sum(r['n_priced'] for r in price_rows),
        basis='vat_incl',                                                    # every price on the cards includes 15% VAT
        eh_rosters=sum(1 for v in rfull.values() if any(x[3] for x in v)),   # bid sheets that list EH (shared tenders)

```

### 33. ana — client value = EH offers only

**Old**
```
        if b['year']==2025: c['b25']+=1; c['v25']+=b['value'] or 0
        else: c['b26']+=1; c['v26']+=b['value'] or 0

```
**New**
```
        # EH's own offer (pre-VAT tracker column), never the winner's price on a lost tender (12 Oct 2026, audit bids-11)
        if b['year']==2025: c['b25']+=1; c['v25']+=b['offer'] or 0
        else: c['b26']+=1; c['v26']+=b['offer'] or 0

```

### 34. ana — client years from all data

**Old**
```
    clients=[]
    for nm,c in cacc.items():

```
**New**
```
    # new / lapsed are judged across every tracking year, whatever the scope (12 Oct 2026, audit bids-10)
    _cyrs=collections.defaultdict(set)
    for b in _ALLBIDS:
        if b['client']: _cyrs[cl_name(b['client'])].add(b['year'])
    _ylast=max((b['year'] for b in _ALLBIDS), default=None)
    clients=[]
    for nm,c in cacc.items():

```

### 35. ana — new / lapsed flags independent of scope

**Old**
```
            lapsed=(c['b25']>0 and c['b26']==0), isnew=(c['b25']==0 and c['b26']>0)))

```
**New**
```
            lapsed=((_ylast-1) in _cyrs[nm] and _ylast not in _cyrs[nm]), isnew=(_cyrs[nm]=={_ylast})))

```

### 36. ana — bid list keeps decimal months

**Old**
```
            svc=SVCN2.get(b['svcdept'],''), dur=int(b['dur']) if b['dur'] else None,

```
**New**
```
            svc=SVCN2.get(b['svcdept'],''), dur=round(b['dur'],1) if b['dur'] else None,

```

### 37. ana — pass the winner list in memory

**Old**
```
    comp,_wc=_BC.build(B, RF)
    return compute(B, RF, comp)

```
**New**
```
    comp,_wc=_BC.build(B, RF)
    return compute(B, RF, comp, _wc)

```
