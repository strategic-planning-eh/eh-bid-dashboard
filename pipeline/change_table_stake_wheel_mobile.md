# Stakeholder Map — round wheel on phones and tablets

Generated 2026-10-12 11:05 · 5 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | stake | exact | layout | phones/tablets: square, centred wheel canvas in the page flow; note above the wheel, not over it | 1 | ✓ |
| 2 | stake | exact | bug | wheel drawing sized from the canvas box, not the 560px map box (root cause of the ellipse and mis-aimed taps) | 1 | ✓ |
| 3 | stake | exact | bug | wheel redrawn whenever the canvas box changes size | 1 | ✓ |
| 4 | stake | exact | layout | square canvas keeps a proportional margin so the outer region labels are not cut off at 768px; desktop radius unchanged | 1 | ✓ |
| 5 | stake | exact | bug | selected-company ring no longer throws "DKM is not defined" (tap-to-select redraws again) | 1 | ✓ |

## Edit detail

### 1. stake — phones/tablets: square, centred wheel canvas in the page flow; note above the wheel, not over it

**Old**
```
</head>
```
**New**
```
<style id="eh-wheel-mobile">@media(max-width:1100px){.viewbox:not(:has(>#mapView[style*="none"])){min-height:0}#mapView{position:relative;inset:auto;padding-bottom:34px}#mapView:not([style*="none"]){display:flex !important;flex-direction:column}#cv{width:min(100%,78vh) !important;height:auto !important;aspect-ratio:1/1;max-height:none !important;margin-inline:auto;flex:none}#tier1Note{order:-1;pos
```

### 2. stake — wheel drawing sized from the canvas box, not the 560px map box (root cause of the ellipse and mis-aimed taps)

**Old**
```
  const box=document.getElementById('mapView').getBoundingClientRect();

```
**New**
```
  const box=cv.getBoundingClientRect();   // size the drawing to the canvas's own box so the wheel stays round (phones show it as a square)

```

### 3. stake — wheel redrawn whenever the canvas box changes size

**Old**
```
window.addEventListener('resize',resize);

```
**New**
```
window.addEventListener('resize',resize);
if(window.ResizeObserver){let _cw=0,_ch=0;new ResizeObserver(function(){const b=cv.getBoundingClientRect(),w=Math.round(b.width),h=Math.round(b.height);if(w&&(w!==_cw||h!==_ch)){_cw=w;_ch=h;resize();}}).observe(cv);}   // redraw when the canvas box itself changes size

```

### 4. stake — square canvas keeps a proportional margin so the outer region labels are not cut off at 768px; desktop radius unchanged

**Old**
```
CX=W/2;CY=H/2;R=Math.max(20,Math.min(W,H)/2-34);draw();
```
**New**
```
CX=W/2;CY=H/2;R=Math.max(20,Math.min(W,H)/2-(W<H*1.1?Math.max(34,Math.min(W,H)*0.1):34));draw();   // square canvas (phones/tablets): leave room for the region labels
```

### 5. stake — selected-company ring no longer throws "DKM is not defined" (tap-to-select redraws again)

**Old**
```
ctx.lineWidth=2.2;ctx.strokeStyle=(DKM?'#E9EEF7':'#15224D');
```
**New**
```
ctx.lineWidth=2.2;ctx.strokeStyle=(document.documentElement.classList.contains('dark')?'#E9EEF7':'#15224D');
```
