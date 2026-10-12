# Design system v2 — Bid & Tender app

Generated 2026-10-12 09:54 · 9 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | build | exact | design | page skin after the shared design system | 1 | ✓ |
| 2 | build | exact | design | standalone masthead contour lines | 1 | ✓ |
| 3 | charts | exact | design | brand chart palette | 1 | ✓ |
| 4 | charts | exact | rtl | horizontal bar charts mirror in Arabic | 1 | ✓ |
| 5 | charts | exact | design | donut centre in the brand fonts and token colours | 1 | ✓ |
| 6 | app | exact | design | outcome colours from the brand status set | 1 | ✓ |
| 7 | app | exact | design | executive summary colours from the brand status set | 1 | ✓ |
| 8 | app | exact | design | chart PNGs carry the brand fonts and stay legible from dark mode | 1 | ✓ |
| 9 | app | exact | design | PNG export waits for the embedded fonts | 1 | ✓ |

## Edit detail

### 1. build — page skin after the shared design system

**Old**
```
APP=open('app.js').read()
HTML=HTML.replace('__APP__', APP)

```
**New**
```
APP=open('app.js').read()
HTML=HTML.replace('__APP__', APP)
# EH design system v2 (patch_design_bids.py): the page skin goes after eh-shared.css so tokens resolve
SKIN=r'''
/* EH design system v2 — Bid & Tender skin (patch_design_bids.py). Tokens and fonts come from eh-shared.css. */
body,body.dark{background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead
```

### 2. build — standalone masthead contour lines

**Old**
```
<header><div class="hd"><img src="{LOGO}" alt="EH"><div><h1 id="h-title">Bid &amp; Tender Intelligence</h1>
```
**New**
```
<header data-eh-contour="7"><div class="hd"><img src="{LOGO}" alt="EH"><div><h1 id="h-title">Bid &amp; Tender Intelligence</h1>
```

### 3. charts — brand chart palette

**Old**
```
const C={green:'#3FA34D',blue:'#1A5FAB',ink:'#1C2B33',soft:'#6B7C86',line:'#E3EAE5',mist:'#F4F8F5',
 red:'#C0504D',orange:'#E8862E',teal:'#2A9D8F',purple:'#7B6BA8',gold:'#D4A92E',
 pal:['#1A5FAB','#3FA34D','#E8862E','#7B6BA8','#2A9D8F','#C0504D','#D4A92E','#5A95C8','#8FB339','#B5651D']};
```
**New**
```
// EH design system v2: land → sea palette from the logo and the EH profile; readable on light and dark panels
const C={green:'#54AB5D',blue:'#0072BB',ink:'#15224D',soft:'#5E6B80',line:'#D9E3DF',mist:'#F2F6F4',
 red:'#B23F2B',orange:'#C98A1B',teal:'#00A0E0',purple:'#8E6BB8',gold:'#C98A1B',
 pal:['#0072BB','#54AB5D','#3B57B8','#00A0E0','#C98A1B','#8E6BB8','#A6CE39','#B23F2B','#5E9FD6','#7FB685']};
```

### 4. charts — horizontal bar charts mirror in Arabic

**Old**
```
  data.forEach((d,i)=>{const v=o.val(d);const w=Math.max(v/max*iw,1);const y=7+i*o.rh;
    s+=`<text x="${labw}" y="${y+o.rh/2+1}" text-anchor="end" class="chl">${esc(String(o.lab(d)).slice(0,o.maxlab))}</text>`;
    s+=`<rect x="${barx}" y="${y+3}" width="${w.toFixed(1)}" height="${o.rh-9}" rx="2.5" fill="${typeof o.color==='function'?o.color(d):o.color}"><title>${esc(o.lab(d))}: ${esc(o.fmt(v))}
```
**New**
```
  const RTL=document.documentElement.dir==='rtl', X=x=>RTL?W-x:x, A=a=>RTL?(a==='end'?'start':'end'):a;   // Arabic: mirror the chart
  data.forEach((d,i)=>{const v=o.val(d);const w=Math.max(v/max*iw,1);const y=7+i*o.rh;
    s+=`<text x="${X(labw)}" y="${y+o.rh/2+1}" text-anchor="${A('end')}" class="chl">${esc(String(o.lab(d)).slice(0,o.maxlab))}</text>`;
    s+=`<rect x="${(RTL?W-barx-w:barx).toF
```

### 5. charts — donut centre in the brand fonts and token colours

**Old**
```
style="font:800 26px Segoe UI;fill:${C.ink}">${o.center}</text><text x="${cx}" y="${cy+14}" text-anchor="middle" style="font:600 10px Segoe UI;fill:${C.soft};letter-spacing:.5px">
```
**New**
```
class="eh-dc" style="font-family:var(--eh-display);font-weight:600;font-size:26px;fill:var(--eh-ink)">${o.center}</text><text x="${cx}" y="${cy+15}" text-anchor="middle" style="font-family:var(--eh-font);font-weight:500;font-size:11.5px;fill:var(--eh-ink-3)">
```

### 6. app — outcome colours from the brand status set

**Old**
```
 const OC={'Won':'#2E7D46','Lost':'#C0504D','Not awarded':'#E8862E','Cancelled':'#5F7078','Pending':'#3E86C8'};
```
**New**
```
 const OC={'Won':'#2E7A37','Lost':'#B23F2B','Not awarded':'#C98A1B','Cancelled':'#5E6B80','Pending':'#0072BB'};   // EH status set (eh-shared.css v2)
```

### 7. app — executive summary colours from the brand status set

**Old**
```
const EXC={won:'#2E7D46',lost:'#C0504D',pend:'#3E86C8',stale:'#E8862E',grey:'#9AABB5',ink:'#1C2B33'};
```
**New**
```
const EXC={won:'#2E7A37',lost:'#B23F2B',pend:'#0072BB',stale:'#C98A1B',grey:'#9DABC5',ink:'#15224D'};   // EH status set (eh-shared.css v2)
```

### 8. app — chart PNGs carry the brand fonts and stay legible from dark mode

**Old**
```
 src.forEach((el,i)=>{ if(el.tagName==='text'||el.tagName==='tspan'){const cs=getComputedStyle(el); dst[i].setAttribute('style',`font:${cs.fontWeight} ${cs.fontSize} 'Segoe UI',Tahoma,Arial,sans-serif;fill:${cs.fill}`);} dst[i].removeAttribute('onclick'); });
```
**New**
```
 src.forEach((el,i)=>{ if(el.tagName==='text'||el.tagName==='tspan'){const cs=getComputedStyle(el); const disp=/EH Display/.test(cs.fontFamily); dst[i].setAttribute('style',`font-family:${disp?"'EH Display'":"'EH Sans'"},'Segoe UI',Tahoma,Arial,sans-serif;font-weight:${cs.fontWeight};font-size:${cs.fontSize};fill:${exInk(cs.fill)}`);} dst[i].removeAttribute('onclick'); });
 const fst=document.crea
```

### 9. app — PNG export waits for the embedded fonts

**Old**
```
function exPNG(id,name){
 const svg=document.getElementById(id); if(!svg)return;
```
**New**
```
// brand fonts for exported PNGs: fetched once, embedded as data URIs so the image renders them (12 Oct 2026)
let EXFONTS=null;
function exFonts(){ if(EXFONTS!==null)return Promise.resolve(EXFONTS);
 const F=[['EH Sans','vendor/fonts/encode-sans-latin-var.woff2','100 900'],['EH Sans','vendor/fonts/plex-sans-arabic-400.woff2','100 549'],['EH Sans','vendor/fonts/plex-sans-arabic-600.woff2','550 900'
```
