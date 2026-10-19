# Change table — pricing cards SUBMITTED badge

Generated 2026-10-19 13:54 · 2 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | app | exact | px-submitted | Pricing cards: pending tenders EH submitted are badged SUBMITTED (blue), not PENDING | 1 | ✓ |
| 2 | app | exact | px-submitted | Pricing cards: pxSubmitted() helper — tracker submission state per tender | 1 | ✓ |

## Edit detail

### 1. app — Pricing cards: pending tenders EH submitted are badged SUBMITTED (blue), not PENDING

**Old**
```
(r.won==null?'<span style="color:#5F7078;font-weight:700">'+t('PENDING','قيد الدراسة')+'</span>':
```
**New**
```
(r.won==null?(pxSubmitted(r)?'<span class="tag" style="background:#E3EEFA;color:#1A5FAB;border:1px solid #1A5FAB">'+t('SUBMITTED','تم التقديم')+'</span>':'<span style="color:#5F7078;font-weight:700">'+t('PENDING','قيد الدراسة')+'</span>'):
```

### 2. app — Pricing cards: pxSubmitted() helper — tracker submission state per tender

**Old**
```
function renderPricing(){
```
**New**
```
function pxSubmitted(r){const b=BA.bidlist.find(x=>x.year==r.year&&x.sn==r.sn);return b?tSub(b):r.bidders.some(b=>b.eh&&b.price);}   // 19 Oct 2026: tracker submission state (tSub) decides; a priced EH roster row is the fallback
function renderPricing(){
```
