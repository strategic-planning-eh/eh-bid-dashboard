# Arabic version — Client Bubble Map

Generated 2026-10-12 11:13 · 55 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | bub | exact | arabic | RTL styles: panel slides from the inline end, zoom buttons and notes mirror | 1 | ✓ |
| 2 | bub | exact | arabic | the dictionary and ehBubbleLang(), before the page script | 1 | ✓ |
| 3 | bub | exact | arabic | amounts in Arabic: «12 مليون ريال», Western digits, isolated | 1 | ✓ |
| 4 | bub | exact | arabic | bubble tooltip: sector and line count | 1 | ✓ |
| 5 | bub | exact | arabic | tooltip opens to the left of the pointer in Arabic | 1 | ✓ |
| 6 | bub | exact | arabic | legend sector names | 1 | ✓ |
| 7 | bub | exact | arabic | detail panel sector | 1 | ✓ |
| 8 | bub | exact | arabic | detail panel total line | 1 | ✓ |
| 9 | bub | exact | arabic | detail panel empty state | 1 | ✓ |
| 10 | bub | exact | arabic | PNG export error | 1 | ✓ |
| 11 | bub | exact | arabic | Executive KPI tiles | 1 | ✓ |
| 12 | bub | exact | arabic | Executive year-scope note | 1 | ✓ |
| 13 | bub | exact | arabic | depth vs value: money axis in Arabic units | 1 | ✓ |
| 14 | bub | exact | arabic | depth vs value: x-axis title | 1 | ✓ |
| 15 | bub | exact | arabic | depth vs value: y-axis title | 1 | ✓ |
| 16 | bub | exact | arabic | median guide label (projects) | 1 | ✓ |
| 17 | bub | exact | arabic | median guide label (value) | 1 | ✓ |
| 18 | bub | exact | arabic | quadrant headings | 1 | ✓ |
| 19 | bub | exact | arabic | dot hover title | 1 | ✓ |
| 20 | bub | exact | arabic | dot name labels read in their own script | 1 | ✓ |
| 21 | bub | exact | arabic | full name list headings | 1 | ✓ |
| 22 | bub | exact | arabic | full name list counts | 1 | ✓ |
| 23 | bub | exact | arabic | show/hide names button | 1 | ✓ |
| 24 | bub | exact | arabic | deal-size bucket names | 1 | ✓ |
| 25 | bub | exact | arabic | deal-size note (right-aligned in Arabic) | 1 | ✓ |
| 26 | bub | exact | arabic | deal-size bar hover | 1 | ✓ |
| 27 | bub | exact | arabic | whitespace table headings (aligned to the start side) | 1 | ✓ |
| 28 | bub | exact | arabic | whitespace top services | 1 | ✓ |
| 29 | bub | exact | arabic | whitespace services not yet bought | 1 | ✓ |
| 30 | bub | exact | arabic | bridge axis: millions | 1 | ✓ |
| 31 | bub | exact | arabic | bridge click-through panel | 1 | ✓ |
| 32 | bub | exact | arabic | bridge bar values | 1 | ✓ |
| 33 | bub | exact | arabic | bridge step names | 1 | ✓ |
| 34 | bub | exact | arabic | concentration subtitle | 1 | ✓ |
| 35 | bub | exact | arabic | concentration: mirrored order in Arabic | 1 | ✓ |
| 36 | bub | exact | arabic | concentration: axes swap sides in Arabic | 1 | ✓ |
| 37 | bub | exact | arabic | concentration: client names slant the other way in Arabic | 1 | ✓ |
| 38 | bub | exact | arabic | concentration: cumulative label | 1 | ✓ |
| 39 | bub | exact | arabic | retention: bars start from the right in Arabic | 1 | ✓ |
| 40 | bub | exact | arabic | retention bars and click-through panel | 1 | ✓ |
| 41 | bub | exact | arabic | retention labels | 1 | ✓ |
| 42 | bub | exact | arabic | sector shift: wider value margin in Arabic | 1 | ✓ |
| 43 | bub | exact | arabic | sector shift: mirrored share axis in Arabic | 1 | ✓ |
| 44 | bub | exact | arabic | sector shift legend | 1 | ✓ |
| 45 | bub | exact | arabic | sector shift: sector names | 1 | ✓ |
| 46 | bub | exact | arabic | sector shift: values and change | 1 | ✓ |
| 47 | bub | exact | arabic | heatmap sector headings | 1 | ✓ |
| 48 | bub | exact | arabic | heatmap service headings | 1 | ✓ |
| 49 | bub | exact | arabic | heatmap empty-cell hover | 1 | ✓ |
| 50 | bub | exact | arabic | heatmap cells | 1 | ✓ |
| 51 | bub | exact | arabic | heatmap cell panel title | 1 | ✓ |
| 52 | bub | exact | arabic | heatmap cell panel total | 1 | ✓ |
| 53 | bub | exact | arabic | chart captions | 1 | ✓ |
| 54 | hub | exact | cleanup | remove the out-of-date comment: the bubble page now follows the hub language | 1 | ✓ |
| 55 | changes | exact | changelog | one W42 line for the Arabic client portfolio page | 1 | ✓ |

## Edit detail

### 1. bub — RTL styles: panel slides from the inline end, zoom buttons and notes mirror

**Old**
```
</style>
</head>
```
**New**
```
</style>
<style id="eh-bub-ar">
/* Arabic / right-to-left (patch_bubble_arabic.py) */
html[dir=rtl] #execWrap svg{direction:ltr}            /* chart anchors stay put; Arabic phrases inside are RTL isolates */
html[dir=rtl] .zctl{right:auto;left:10px}
html[lang=ar] .kcard .kv{font-size:22px}
html[lang=ar] td.hc{width:88px;min-width:88px}
html[lang=ar] td.hc small{white-space:nowrap}
html[dir=rtl] .
```

### 2. bub — the dictionary and ehBubbleLang(), before the page script

**Old**
```
</aside>

<script>
const DATA = [
```
**New**
```
</aside>

<script id="bub-i18n">
/* Arabic version (patch_bubble_arabic.py, 12 Oct 2026). BUB_I18N is the page's one dictionary:
   ui = [English exactly as the page always wrote it, Arabic] ({0},{1} are filled in), sec/svc/deal/step = names,
   pl = Arabic counted nouns, cap = Arabic chart captions, st = Arabic for the static page text (its English is the
   markup itself, read back when switchin
```

### 3. bub — amounts in Arabic: «12 مليون ريال», Western digits, isolated

**Old**
```
const fmt = v => {
  if (v >= 1e6)
```
**New**
```
const fmt = v => {
  if (BUB_LANG === "ar") return bubFmtAr(v, "", true);
  if (v >= 1e6)
```

### 4. bub — bubble tooltip: sector and line count

**Old**
```
        <div class="s">${d.data.sector}</div>
        <div>${fmt(val(d.data))} · ${proj(d.data)} project line${proj(d.data)>1?"s":""}</div>
```
**New**
```
        <div class="s">${bTS(d.data.sector)}</div>
        <div>${fmt(val(d.data))} · ${BUB_LANG==="ar" ? bCount(proj(d.data),"line") : proj(d.data)+bT("proj_line_s")+(proj(d.data)>1?"s":"")}</div>
```

### 5. bub — tooltip opens to the left of the pointer in Arabic

**Old**
```
` : ""}`;
    })
    .on("mouseleave"
```
**New**
```
` : ""}`;
      if (BUB_LANG==="ar") tip.style.left = Math.max(8, e.clientX-14-tip.offsetWidth) + "px";
    })
    .on("mouseleave"
```

### 6. bub — legend sector names

**Old**
```
lgAll.select(".nm").text(d => d[0]);
```
**New**
```
lgAll.select(".nm").text(d => bTS(d[0]));
```

### 7. bub — detail panel sector

**Old**
```
document.getElementById("psec").textContent = comp.sector;
```
**New**
```
document.getElementById("psec").textContent = bTS(comp.sector);
```

### 8. bub — detail panel total line

**Old**
```
  document.getElementById("ptot").innerHTML =
    `<b>${fmt(d3.sum(priced, l => l.v))}</b> across
```
**New**
```
  document.getElementById("ptot").innerHTML = BUB_LANG==="ar" ?
    `<b>${fmt(d3.sum(priced, l => l.v))}</b> · ${bT("lines_lbl")} <b>${d3.sum(lines, l => l.n)}</b>` +
    (lines.length > priced.length ? ` · ${bT("unpriced_lbl")} ${lines.length - priced.length}` : "") :
    `<b>${fmt(d3.sum(priced, l => l.v))}</b> across
```

### 9. bub — detail panel empty state

**Old**
```
`<div class="pline"><span class="sv">No lines in this year scope.</span></div>`;
```
**New**
```
`<div class="pline"><span class="sv">${bT("no_lines")}</span></div>`;
```

### 10. bub — PNG export error

**Old**
```
img.onerror = () => alert("PNG export failed — please report this.");
```
**New**
```
img.onerror = () => alert(bT("png_fail"));
```

### 11. bub — Executive KPI tiles

**Old**
```
    ["Total book 25+26", fmt(tAll), null],
    ["2026 revenue", fmt(t26), (yoy>=0?"▲ ":"▼ ") + Math.round(Math.abs(yoy)*100) + "% vs 2025", yoy>=0],
    ["Active clients 2026", c26.length, (c26.length>=c25.length?"▲ ":"▼ ") + Math.abs(c26.length-c25.length) + " vs 2025", c26.length>=c25.length],
    ["Client retention", Math.round(100*ret.length/c25.length) + "%", ret.length + " of " + c25.length 
```
**New**
```
    [bT("k_total"), fmt(tAll), null],
    [bT("k_rev26"), fmt(t26), (yoy>=0?"▲ ":"▼ ") + Math.round(Math.abs(yoy)*100) + "%" + bT("vs25"), yoy>=0],
    [bT("k_active"), c26.length, (c26.length>=c25.length?"▲ ":"▼ ") + Math.abs(c26.length-c25.length) + bT("vs25"), c26.length>=c25.length],
    [bT("k_ret"), Math.round(100*ret.length/c25.length) + "%", bF("kept", ret.length, c25.length), true],
    [
```

### 12. bub — Executive year-scope note

**Old**
```
    : 'Showing <b>'+yearMode+'</b> only — Depth vs Value, Deal-Size and Whitespace are scoped to '+yearMode+
      '; the Bridge, Retention and Sector-Shift cards always compare 2025 → 2026. &nbsp;';
```
**New**
```
    : bF("scope", yearMode);
```

### 13. bub — depth vs value: money axis in Arabic units

**Old**
```
const axY=root.select(".qax-y").call(d3.axisLeft(py).ticks(6,"~s").tickSizeOuter(0));
```
**New**
```
const _fq=py.tickFormat(6,"~s");
  const axY=root.select(".qax-y").call(BUB_LANG==="ar" ? d3.axisLeft(py).ticks(6).tickFormat(v=>_fq(v)?bubAmt(v,false,false):"").tickSizeOuter(0) : d3.axisLeft(py).ticks(6,"~s").tickSizeOuter(0));
```

### 14. bub — depth vs value: x-axis title

**Old**
```
function t_axis(){return "How many jobs the client gives EH \u2192 (log scale)";}
```
**New**
```
function t_axis(){return bidiAr(bT("q_x"));}
```

### 15. bub — depth vs value: y-axis title

**Old**
```
.text("Contract value with EH \u2192 (SAR, log scale)");
```
**New**
```
.text(bidiAr(bT("q_y")));
```

### 16. bub — median guide label (projects)

**Old**
```
.text("median "+medP+" projects")
```
**New**
```
.text(BUB_LANG==="ar" ? bidiAr(bT("median")+" "+bCount(medP,"proj")) : "median "+medP+" projects")
```

### 17. bub — median guide label (value)

**Old**
```
.text("median "+fmt(medV))
```
**New**
```
.text(bidiAr(bT("median")+" "+fmt(medV)))
```

### 18. bub — quadrant headings

**Old**
```
  const QL=[["Strategic accounts ("+QN.S+")",W-M.r-6,M.t+14,"end","S"],
            ["Concentrated bets ("+QN.C+")",M.l+10,M.t+14,"start","C"],
            ["Transactional volume ("+QN.T+")",W-M.r-6,H-M.b-10,"end","T"],
            ["Smaller accounts ("+QN.X+")",M.l+10,H-M.b-10,"start","X"]];
```
**New**
```
  const QL=[[bidiAr(bT("qS")+" ("+QN.S+")"),W-M.r-6,M.t+14,"end","S"],
            [bidiAr(bT("qC")+" ("+QN.C+")"),M.l+10,M.t+14,"start","C"],
            [bidiAr(bT("qT")+" ("+QN.T+")"),W-M.r-6,H-M.b-10,"end","T"],
            [bidiAr(bT("qX")+" ("+QN.X+")"),M.l+10,H-M.b-10,"start","X"]];
```

### 19. bub — dot hover title

**Old**
```
d3.select(this).select("title").text(d.n+"\n"+d.p+" projects \u00b7 "+fmt(d.v));
```
**New**
```
d3.select(this).select("title").text(d.n+"\n"+(BUB_LANG==="ar"?bCount(d.p,"proj"):d.p+" projects")+" \u00b7 "+fmt(d.v));
```

### 20. bub — dot name labels read in their own script

**Old**
```
      .attr("fill",TXT).attr("stroke",HALO)
      .text(o=>o.nm)
```
**New**
```
      .attr("fill",TXT).attr("stroke",HALO)
      .text(o=>bidiName(o.nm))
```

### 21. bub — full name list headings

**Old**
```
const QTITLE={S:"Strategic accounts",C:"Concentrated bets",T:"Transactional volume",X:"Smaller accounts"};
```
**New**
```
const QTITLE={S:bT("qS"),C:bT("qC"),T:bT("qT"),X:bT("qX")};
```

### 22. bub — full name list counts

**Old**
```
<span style="opacity:.65">\u2014 '+d.p+' jobs \u00b7 '+fmt(d.v)+'</span>
```
**New**
```
<span style="opacity:.65">\u2014 '+(BUB_LANG==="ar"?bCount(d.p,"proj"):d.p+' jobs')+' \u00b7 '+fmt(d.v)+'</span>
```

### 23. bub — show/hide names button

**Old**
```
b.textContent=show?"Hide names":"Show all 60 names";
```
**New**
```
b.textContent=bT(show?"hide_names":"show_names");
```

### 24. bub — deal-size bucket names

**Old**
```
const axX=root.select(".deal-ax-x").call(d3.axisBottom(x).tickSizeOuter(0));
```
**New**
```
const axX=root.select(".deal-ax-x").call(d3.axisBottom(x).tickSizeOuter(0).tickFormat(k=>BUB_LANG==="ar"?bidiAr(bMap("deal",k)):k));
```

### 25. bub — deal-size note (right-aligned in Arabic)

**Old**
```
root.select(".deal-note").attr("fill",SUB).text("bars = client count · label % = share of total book value in that bucket");
```
**New**
```
root.select(".deal-note").attr("fill",SUB).attr("x",BUB_LANG==="ar"?W-M.r:M.l).attr("text-anchor",BUB_LANG==="ar"?"end":null).text(bidiAr(bT("deal_note")));
```

### 26. bub — deal-size bar hover

**Old**
```
bAll.select("title").text(a=>a.c+" clients · "+fmt(a.val)+" ("+pct(a)+"% of book)");
```
**New**
```
bAll.select("title").text(a=>(BUB_LANG==="ar"?bCount(a.c,"client"):a.c+" clients")+" · "+fmt(a.val)+" ("+bF("of_book",pct(a))+")");
```

### 27. bub — whitespace table headings (aligned to the start side)

**Old**
```
   '<thead><tr style="text-align:left;color:#5F7078"><th style="padding:6px 8px">Client</th><th style="padding:6px 8px">Value</th><th style="padding:6px 8px">Top services (by value)</th><th style="padding:6px 8px">Not yet bought (whitespace)</th></tr></thead><tbody>'+
```
**New**
```
   '<thead><tr style="text-align:start;color:#5F7078"><th style="padding:6px 8px">'+bT("ws_client")+'</th><th style="padding:6px 8px">'+bT("ws_value")+'</th><th style="padding:6px 8px">'+bT("ws_top")+'</th><th style="padding:6px 8px">'+bT("ws_missing")+'</th></tr></thead><tbody>'+
```

### 28. bub — whitespace top services

**Old**
```
font-style:italic">project descriptions not classifiable</span>')+r.top.map(t=>chip(t[0]+' \u00b7 '+Math.round(100*t[1]/r.val)+'%',
```
**New**
```
font-style:italic">'+bT("ws_unclass")+'</span>')+r.top.map(t=>chip(bTV(t[0])+' \u00b7 '+bPct(Math.round(100*t[1]/r.val)),
```

### 29. bub — whitespace services not yet bought

**Old**
```
r.missing.slice(0,4).map(c=>chip(c,'#EFF6F1','#D5E6DA','#1F7A4C')).join('')+(r.missing.length>4?' <span style="color:#8A99A3">+'+(r.missing.length-4)+' more</span>':'')
```
**New**
```
r.missing.slice(0,4).map(c=>chip(bTV(c),'#EFF6F1','#D5E6DA','#1F7A4C')).join('')+(r.missing.length>4?' <span style="color:#8A99A3">'+bF("more",r.missing.length-4)+'</span>':'')
```

### 30. bub — bridge axis: millions

**Old**
```
  const svg = svgBase("svgBridge");
  svg.append("g").attr("transform",`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickFormat(v=>(v/1e6).toFixed(0)+"M"))
```
**New**
```
  const svg = svgBase("svgBridge");
  svg.append("g").attr("transform",`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickFormat(bubMTick))
```

### 31. bub — bridge click-through panel

**Old**
```
          .map(d => ({name: d.name, meta: p.l==="New clients"?"":`${fmt(d.v2025)} → ${fmt(d.v2026)}`,
                      amt: (p.key(d)>=0?"+":"−") + fmt(Math.abs(p.key(d)))}));
        showListPanel(p.l, `${p.items.length} clients · net ${p.v>=0?"+":"−"}${fmt(Math.abs(p.v))}`, p.c,
          `<b>${p.v>=0?"+":"−"}${fmt(Math.abs(p.v))}</b> impact on 2026 revenue`, its);
```
**New**
```
          .map(d => ({name: d.name, meta: p.l==="New clients"?"":`${fmt(d.v2025)} → ${fmt(d.v2026)}`,
                      amt: bubAmt(p.key(d), true, true)}));
        showListPanel(bMap("step",p.l), BUB_LANG==="ar" ? `${bCount(p.items.length,"client")} · ${bT("net")} ${bubAmt(p.v,true,true)}` : `${p.items.length} clients · net ${p.v>=0?"+":"−"}${fmt(Math.abs(p.v))}`, p.c,
          `<b>${bubAmt
```

### 32. bub — bridge bar values

**Old**
```
      .text((p.abs?"":(p.v>=0?"+":"−")) + fmt(Math.abs(p.v)).replace("SAR ",""));
```
**New**
```
      .text(bubAmt(p.v, !p.abs, false));
```

### 33. bub — bridge step names

**Old**
```
.attr("text-anchor","middle").attr("font-size","12.5px").attr("fill","#5E6B80").text(p.l);
```
**New**
```
.attr("text-anchor","middle").attr("font-size","12.5px").attr("fill","#5E6B80").text(bidiAr(bMap("step",p.l)));
```

### 34. bub — concentration subtitle

**Old**
```
    `Top 1 = ${Math.round(top1*100)}% · Top 5 = ${Math.round(top5*100)}% · Top 10 = ${Math.round(top10*100)}% of the two-year book — click a bar for that client's ledger`;
```
**New**
```
    bF("pareto_sub", Math.round(top1*100), Math.round(top5*100), Math.round(top10*100));
```

### 35. bub — concentration: mirrored order in Arabic

**Old**
```
  const W=960, H=440, m={t:24,r:60,b:112,l:78};
  const x = d3.scaleBand().domain(top.map(d=>d.name)).range([m.l, W-m.r]).padding(0.25);
```
**New**
```
  const RT=BUB_LANG==="ar", W=960, H=440, m=RT?{t:24,r:78,b:112,l:60}:{t:24,r:60,b:112,l:78};
  const x = d3.scaleBand().domain(top.map(d=>d.name)).range(RT?[W-m.r, m.l]:[m.l, W-m.r]).padding(0.25);
```

### 36. bub — concentration: axes swap sides in Arabic

**Old**
```
  svg.append("g").attr("transform",`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickFormat(v=>(v/1e6).toFixed(0)+"M"))
     .attr("font-size","12px").attr("color","#5E6B80");
  svg.append("g").attr("transform",`translate(${W-m.r},0)`).call(d3.axisRight(yp).ticks(5).tickFormat(v=>v+"%"))
```
**New**
```
  svg.append("g").attr("transform",`translate(${RT?W-m.r:m.l},0)`).call((RT?d3.axisRight(y):d3.axisLeft(y)).ticks(6).tickFormat(bubMTick))
     .attr("font-size","12px").attr("color","#5E6B80");
  svg.append("g").attr("transform",`translate(${RT?m.l:W-m.r},0)`).call((RT?d3.axisLeft(yp):d3.axisRight(yp)).ticks(5).tickFormat(v=>v+"%"))
```

### 37. bub — concentration: client names slant the other way in Arabic

**Old**
```
      .attr("transform", `translate(${x(d.name)+x.bandwidth()/2+4},${H-m.b+8}) rotate(34)`)
      .attr("font-size","11px").attr("fill","#46546F").attr("text-anchor","start")
      .text(short.length > 20 ? short.slice(0,19)+"…" : short);
```
**New**
```
      .attr("transform", RT ? `translate(${x(d.name)+x.bandwidth()/2-4},${H-m.b+8}) rotate(-34)` : `translate(${x(d.name)+x.bandwidth()/2+4},${H-m.b+8}) rotate(34)`)
      .attr("font-size","11px").attr("fill","#46546F").attr("text-anchor",RT?"end":"start")
      .text(bidiName(short.length > 20 ? short.slice(0,19)+"…" : short));
```

### 38. bub — concentration: cumulative label

**Old**
```
  svg.append("text").attr("x", x(pts[pts.length-1].name)-10).attr("y", yp(pts[pts.length-1].cum)-10)
     .attr("font-size","12px").attr("fill","#15224D").attr("font-weight","600")
     .text(Math.round(pts[pts.length-1].cum) + "% cumulative");
```
**New**
```
  svg.append("text").attr("x", RT ? x(pts[pts.length-1].name)+x.bandwidth()/2-4 : x(pts[pts.length-1].name)-10).attr("y", yp(pts[pts.length-1].cum)-10)
     .attr("font-size","12px").attr("fill","#15224D").attr("font-weight","600")
     .text(bidiAr(bF("cum", Math.round(pts[pts.length-1].cum))));
```

### 39. bub — retention: bars start from the right in Arabic

**Old**
```
  const W=960, H=300, m={t:24,r:220,b:14,l:180};
  const y = d3.scaleBand().domain(rows.map(r=>r.l)).range([m.t, H-m.b]).padding(0.34);
  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>r.v)*1.05]).range([m.l, W-m.r]);
```
**New**
```
  const RT=BUB_LANG==="ar", W=960, H=300, m={t:24,r:220,b:14,l:180}, x0=RT?W-m.l:m.l;
  const y = d3.scaleBand().domain(rows.map(r=>r.l)).range([m.t, H-m.b]).padding(0.34);
  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>r.v)*1.05]).range(RT?[W-m.l, m.r]:[m.l, W-m.r]);
  const bx = r => RT ? Math.min(x(r.v), x0-4) : m.l;
```

### 40. bub — retention bars and click-through panel

**Old**
```
      .attr("x", m.l).attr("y", y(r.l)).attr("height", y.bandwidth())
      .attr("width", Math.max(4, x(r.v)-m.l)).attr("rx",6).attr("fill", r.c)
      .on("click", () => showListPanel(r.l, `${r.n} clients · ${r.note}`, r.c,
          `<b>${fmt(r.v)}</b> across <b>${r.n}</b> clients`,
```
**New**
```
      .attr("x", bx(r)).attr("y", y(r.l)).attr("height", y.bandwidth())
      .attr("width", Math.max(4, Math.abs(x(r.v)-x0))).attr("rx",6).attr("fill", r.c)
      .on("click", () => showListPanel(bMap("step",r.l), BUB_LANG==="ar" ? `${bCount(r.n,"client")} · ${bMap("step",r.note)}` : `${r.n} clients · ${r.note}`, r.c,
          BUB_LANG==="ar" ? `<b>${fmt(r.v)}</b> · ${bT("clients_lbl")} <b>${r.n
```

### 41. bub — retention labels

**Old**
```
    svg.append("text").attr("x", m.l-10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("text-anchor","end").attr("font-size","14px").attr("fill","#15224D").attr("font-weight","600").text(r.l);
    svg.append("text").attr("x", Math.max(4, x(r.v))+10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("font-size","12.5px").attr("fill","#5E6B80")
       .text(`${r.n} clients · ${fmt(r.v)}`);
```
**New**
```
    svg.append("text").attr("x", RT ? x0+10 : m.l-10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("text-anchor",RT?"start":"end").attr("font-size","14px").attr("fill","#15224D").attr("font-weight","600").text(bidiAr(bMap("step",r.l)));
    svg.append("text").attr("x", RT ? bx(r)-10 : Math.max(4, x(r.v))+10).attr("y", y(r.l)+y.bandwidth()/2+5)
       .attr("text-anchor",RT?"end":null).attr("fo
```

### 42. bub — sector shift: wider value margin in Arabic

**Old**
```
  const W=960, H=Math.max(360, 64 + rows.length*32), m={t:46,b:30,l:230,r:150};
```
**New**
```
  const RT=BUB_LANG==="ar", W=960, H=Math.max(360, 64 + rows.length*32), m={t:46,b:30,l:230,r:RT?185:150};
```

### 43. bub — sector shift: mirrored share axis in Arabic

**Old**
```
  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>Math.max(r.p25,r.p26))*1.1]).range([m.l, W-m.r]);
```
**New**
```
  const x = d3.scaleLinear().domain([0, d3.max(rows,r=>Math.max(r.p25,r.p26))*1.1]).range(RT?[W-m.l, m.r]:[m.l, W-m.r]);
```

### 44. bub — sector shift legend

**Old**
```
  svg.append("circle").attr("cx",m.l+4).attr("cy",14).attr("r",5).attr("fill","#fff").attr("stroke","#7D8AA0").attr("stroke-width",2);
  svg.append("text").attr("x",m.l+14).attr("y",18).attr("font-size","11.5px").attr("fill","#5E6B80").text("2025 share");
  svg.append("circle").attr("cx",m.l+110).attr("cy",14).attr("r",5.5).attr("fill","#0072BB");
  svg.append("text").attr("x",m.l+120).attr("y",18
```
**New**
```
  const lx = d => RT ? W-16-d : m.l+d;
  svg.append("circle").attr("cx",lx(4)).attr("cy",14).attr("r",5).attr("fill","#fff").attr("stroke","#7D8AA0").attr("stroke-width",2);
  svg.append("text").attr("x",lx(14)).attr("y",18).attr("text-anchor",RT?"end":null).attr("font-size","11.5px").attr("fill","#5E6B80").text(bidiAr(bT("share25")));
  svg.append("circle").attr("cx",lx(110)).attr("cy",14).attr("
```

### 45. bub — sector shift: sector names

**Old**
```
    const sn = r.s.length > 28 ? r.s.slice(0,27)+"…" : r.s;
    svg.append("text").attr("x", m.l-12).attr("y", cy+4.5).attr("text-anchor","end")
       .attr("font-size","12.5px").attr("fill","#15224D").attr("font-weight","600").text(sn);
```
**New**
```
    const sl = bTS(r.s), sn = sl.length > 28 ? sl.slice(0,27)+"…" : sl;
    svg.append("text").attr("x", RT ? W-m.l+12 : m.l-12).attr("y", cy+4.5).attr("text-anchor",RT?"start":"end")
       .attr("font-size","12.5px").attr("fill","#15224D").attr("font-weight","600").text(bidiAr(sn));
```

### 46. bub — sector shift: values and change

**Old**
```
    svg.append("text").attr("x", W-m.r+12).attr("y", cy+4.5)
       .attr("font-size","12px").attr("fill","#46546F")
       .text(`${r.p25.toFixed(1)} → ${r.p26.toFixed(1)}%`);
    svg.append("text").attr("x", W-14).attr("y", cy+4.5).attr("text-anchor","end")
       .attr("font-size","12px").attr("font-weight","700")
       .attr("fill", up ? "#2E7A37" : "#B23F2B")
       .text((up?"+":"−") + Math
```
**New**
```
    svg.append("text").attr("x", RT ? m.r-12 : W-m.r+12).attr("y", cy+4.5).attr("text-anchor",RT?"end":null)
       .attr("font-size","12px").attr("fill","#46546F")
       .text(`${r.p25.toFixed(1)} → ${r.p26.toFixed(1)}%`);
    svg.append("text").attr("x", RT ? 14 : W-14).attr("y", cy+4.5).attr("text-anchor",RT?"start":"end")
       .attr("font-size","12px").attr("font-weight","700")
       .attr
```

### 47. bub — heatmap sector headings

**Old**
```
secs.map(s => `<th class="col">${s}</th>`).join("")
```
**New**
```
secs.map(s => `<th class="col">${bTS(s)}</th>`).join("")
```

### 48. bub — heatmap service headings

**Old**
```
h += `<tr><th class="row" title="${cat}">${cat}</th>`;
```
**New**
```
h += `<tr><th class="row" title="${bTV(cat)}">${bTV(cat)}</th>`;
```

### 49. bub — heatmap empty-cell hover

**Old**
```
h += `<td class="hc empty" title="Whitespace: no ${cat} sales into ${sec}">–</td>`;
```
**New**
```
h += `<td class="hc empty" title="${bF("ws_title", bTV(cat), bTS(sec))}">–</td>`;
```

### 50. bub — heatmap cells

**Old**
```
                 title="${sec} × ${cat}">${v>0?fmt(v).replace("SAR ",""):"0"}<small>${n} ln · ${c.co.length} co</small></td>`;
```
**New**
```
                 title="${bTS(sec)} × ${bTV(cat)}">${v>0?bubAmt(v,false,false):"0"}<small>${bF("cell_n", n, c.co.length)}</small></td>`;
```

### 51. bub — heatmap cell panel title

**Old**
```
  document.getElementById("pco").textContent = cat;
  document.getElementById("psec").textContent = sec;
```
**New**
```
  document.getElementById("pco").textContent = bTV(cat);
  document.getElementById("psec").textContent = bTS(sec);
```

### 52. bub — heatmap cell panel total

**Old**
```
    `<b>${fmt(hv(c))}</b> across <b>${hn(c)}</b> lines · <b>${cos.length}</b> client${cos.length>1?"s":""}`;
```
**New**
```
    (BUB_LANG==="ar" ? `<b>${fmt(hv(c))}</b> · ${bT("lines_lbl")} <b>${hn(c)}</b> · ${bT("clients_lbl")} <b>${cos.length}</b>` :
    `<b>${fmt(hv(c))}</b> across <b>${hn(c)}</b> lines · <b>${cos.length}</b> client${cos.length>1?"s":""}`);
```

### 53. bub — chart captions

**Old**
```
cap.textContent=EH_BUB_CAPS[id];
```
**New**
```
cap.textContent=bubCap(id);
```

### 54. hub — remove the out-of-date comment: the bubble page now follows the hub language

**Old**
```
bcastLang();
// note: the bubble chart is a static English artifact and keeps its labels.

```
**New**
```
bcastLang();

```

### 55. changes — one W42 line for the Arabic client portfolio page

**Old**
```


## 2026-W41

```
**New**
```

clients | major | Clients & Revenue | New: the client portfolio page is now fully in Arabic when the hub is in Arabic — the bubble map, the sector × service heatmap, every Executive chart, the KPI tiles, hover boxes, the client detail panel and the notes. Company names stay as recorded, amounts read in riyals with Western digits, and the page reads right to left: the legend and detail panel sit o
```
