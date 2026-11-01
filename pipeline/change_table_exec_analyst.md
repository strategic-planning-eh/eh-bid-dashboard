# Change table — Executive Summary analyst cards (1 Nov 2026)

Generated 2026-11-01 14:08 · 6 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | ana | exact | exec-analyst | bid_analytics2: buyer type (government / company) tagged on each tender by issuer name | 1 | ✓ |
| 2 | ana | exact | exec-analyst | bid_analytics2: buyer field written to bidlist | 1 | ✓ |
| 3 | app | exact | exec-analyst | app.js: analyst review cards — exUnknown, exLosePrice, exGapYear, exBuyers, exField, exOpening | 1 | ✓ |
| 4 | app | exact | exec-analyst | Executive Summary: opening lines + "Results still unknown" first in the KPI strip | 1 | ✓ |
| 5 | app | exact | exec-analyst | Executive Summary: card order per the analyst report (price loss → gap → buyers → funnel → where we win → field width → threat → price position → decisions) | 1 | ✓ |
| 6 | app | exact | exec-analyst | Executive Summary subtitle no longer promises exactly five questions | 1 | ✓ |

## Edit detail

### 1. ana — bid_analytics2: buyer type (government / company) tagged on each tender by issuer name

**Old**
```
    bidlist=[]
    for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):
```
**New**
```
    import re as _re
    _GOV=_re.compile(r'هيئة|وزارة|أمانة|أمانه|المركز الوطني|مؤسسة عامة|المؤسسة العامة|بلدية|جامعة|كلية|الحرس|القوات|المديرية|Authority|Ministry|Nat\. Center|National Center|Municipality|University|College|Military|Forces|Corp\b|Organization|Reserve|GAMI|SWCC|NCVC|NCEC|TVTC|ZATCA|Zakat', _re.I)
    def _buyer(name): return 'government' if _GOV.search(str(name or '')) else 'comp
```

### 2. ana — bid_analytics2: buyer field written to bidlist

**Old**
```
            svc=SVCN2.get(b['svcdept'],''), dur=round(b['dur'],1) if b['dur'] else None,
```
**New**
```
            svc=SVCN2.get(b['svcdept'],''), buyer=_buyer(b['client']), dur=round(b['dur'],1) if b['dur'] else None,
```

### 3. app — app.js: analyst review cards — exUnknown, exLosePrice, exGapYear, exBuyers, exField, exOpening

**Old**
```
// ---- PNG export: clone the SVG
```
**New**
```
// ---- analyst review cards (1 Nov 2026): E-12, opening lines, E-1, E-5, E-10, E-2 — see pipeline/analysis/out/map_analyst_report_2026-11.md
function exMedian(a){const s=a.slice().sort((x,y)=>x-y);return s.length?(s.length%2?s[s.length>>1]:(s[s.length/2-1]+s[s.length/2])/2):null;}
function exPct(v){return v==null?'—':Math.round(v)+'%';}
function exBuyer(b){return (b&&b.buyer)||'company';}
functio
```

### 4. app — Executive Summary: opening lines + "Results still unknown" first in the KPI strip

**Old**
```
 <div class="kstrip exk">
  ${kc(d.winRate==null?'—':d.winRate+'%',t('Win rate on decided tenders','نسبة الفوز في المنافسات المحسومة')
```
**New**
```
 ${exOpening(B,d)}
 <div class="kstrip exk">
  ${exUnknown(d)}
  ${kc(d.winRate==null?'—':d.winRate+'%',t('Win rate on decided tenders','نسبة الفوز في المنافسات المحسومة')
```

### 5. app — Executive Summary: card order per the analyst report (price loss → gap → buyers → funnel → where we win → field width → threat → price position → decisions)

**Old**
```
 ${exFunnel(d)}
 ${exWhere(B)}
 ${exThreat(B,d)}
 ${exPrice(B,d)}
 ${exDecisions(B,d)}`;
```
**New**
```
 <div class="grid g2">${exLosePrice(B)}${exGapYear()}</div>
 ${exBuyers(B)}
 ${exFunnel(d)}
 ${exWhere(B)}
 ${exField(B)}
 ${exThreat(B,d)}
 ${exPrice(B,d)}
 ${exDecisions(B,d)}`;
```

### 6. app — Executive Summary subtitle no longer promises exactly five questions

**Old**
```
t('Five questions a director needs answered before the Sunday meeting — computed from the bid tracker on every rebuild','خمسة أسئلة يحتاج المدير إجابتها قبل اجتماع الأحد — تُحسب من جدول العطاءات عند كل إعادة بناء')
```
**New**
```
t('What a director needs to know before the Sunday meeting — computed from the bid tracker on every rebuild','ما يحتاج المدير معرفته قبل اجتماع الأحد — يُحسب من جدول العطاءات عند كل إعادة بناء')
```
