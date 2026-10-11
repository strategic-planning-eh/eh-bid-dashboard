# All Tenders — live analytics, honest sentences and data checks

Generated 2026-10-11 16:30 · 9 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | app | regex | feature | All Tenders rebuilt with live analytics, filters, checks and export | 1 | ✓ |
| 2 | app | exact | fix | Overview: typed "win rate fell sharply" (contradicted by the data) replaced by a live sentence | 1 | ✓ |
| 3 | app | exact | fix | Notes & Limits: typed headline story replaced by live figures | 1 | ✓ |
| 4 | app | regex | fix | Notes & Limits: open-pipeline card built from the submission match | 1 | ✓ |
| 5 | app | regex | fix | Notes & Limits: "near-complete 2025" (untrue) replaced by live counts | 1 | ✓ |
| 6 | app | exact | feature | render the submission-timing card | 1 | ✓ |
| 7 | analytics | exact | fix | "EH was cheapest" counted only lost tenders, so it always read 0 | 1 | ✓ |
| 8 | analytics | exact | fix | win-rate helper for the watch item | 1 | ✓ |
| 9 | analytics | exact | fix | "Win-rate decline" only when the fall is clear, not noise | 1 | ✓ |

## Edit detail

### 1. app — All Tenders rebuilt with live analytics, filters, checks and export

**Old**
```
//\ =====================\ ALL\ TENDERS\ \(list\ view\)\ =====================\
.*?(?=// ===================== NOTES & LIMITATIONS =====================\n)
```
**New**
```
<fn>
```

### 2. app — Overview: typed "win rate fell sharply" (contradicted by the data) replaced by a live sentence

**Old**
```
${t('Tender volume held up but win rate fell sharply — the central competitive concern.','صمد حجم المنافسات لكن نسبة الفوز انخفضت بحدّة — وهو الشاغل التنافسي الأبرز.')}
```
**New**
```
${tTrend()}
```

### 3. app — Notes & Limits: typed headline story replaced by live figures

**Old**
```
${t(' — where EH may be losing, which clients are slipping, where pricing looks exposed — not to settle them with precision. The headline story (declining win rate, high pricing on losses, SEC concentration) is directionally credible; the exact percentages are not. The single highest-leverage fix is upstream: ',' — أين قد يخسر EH، وأي العملاء يتراجعون، وأين يبدو التسعير مكشوفاً — لا لحسمها بدقّة. 
```
**New**
```
${t(' — where EH may be losing, which clients are slipping, where pricing looks exposed — not to settle them with precision. ',' — أين قد يخسر EH، وأي العملاء يتراجعون، وأين يبدو التسعير مكشوفاً — لا لحسمها بدقّة. ')}${tHeadline()}${t('Treat the exact percentages as indicative. The single highest-leverage fix is upstream: ','تعامل مع النسب الدقيقة كمؤشرات. وأعلى إصلاح أثراً يقع في المنبع: ')}
```

### 4. app — Notes & Limits: open-pipeline card built from the submission match

**Old**
```
\[t\('Open pipeline is an upper bound'.*?'\)\],\n
```
**New**
```
<fn>
```

### 5. app — Notes & Limits: "near-complete 2025" (untrue) replaced by live counts

**Old**
```
\[t\('2025 vs 2026 not comparable'.*?'\)\],\n
```
**New**
```
<fn>
```

### 6. app — render the submission-timing card

**Old**
```
rFunnel();renderTenders();
```
**New**
```
rFunnel();rTiming();renderTenders();
```

### 7. analytics — "EH was cheapest" counted only lost tenders, so it always read 0

**Old**
```
            wgaps.append(round(100*(ehp-award)/award,1))
            if rank==1: cheapest_cnt+=1

```
**New**
```
            wgaps.append(round(100*(ehp-award)/award,1))
        if has_full and rank==1: cheapest_cnt+=1   # 11 Oct 2026: count every fully priced tender where EH was lowest

```

### 8. analytics — win-rate helper for the watch item

**Old**
```
    # ---------- WATCHLIST (self-contained, regenerated each run) ----------

```
**New**
```
    def _wilson(k,n,z=1.959964):
        if not n: return None
        p=k/n; den=1+z*z/n; c=(p+z*z/(2*n))/den; h=z*((p*(1-p)/n+z*z/(4*n*n))**.5)/den
        return (c-h, c+h)
    def _wr_clear(a,b):
        # a real change only when both years have 10+ results and the likely ranges do not overlap
        if (a.get('awarded') or 0)<10 or (b.get('awarded') or 0)<10: return False
        x=_wilson(a
```

### 9. analytics — "Win-rate decline" only when the fall is clear, not noise

**Old**
```
traj[2026]['win_rate']<traj[2025]['win_rate']:

```
**New**
```
traj[2026]['win_rate']<traj[2025]['win_rate'] and _wr_clear(traj[2025],traj[2026]):

```
