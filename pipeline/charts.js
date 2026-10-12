// ===== Lightweight self-contained SVG chart library (theme-aware) =====
// EH design system v2: land → sea palette from the logo and the EH profile; readable on light and dark panels
const C={green:'#54AB5D',blue:'#0072BB',ink:'#15224D',soft:'#5E6B80',line:'#D9E3DF',mist:'#F2F6F4',
 red:'#B23F2B',orange:'#C98A1B',teal:'#00A0E0',purple:'#8E6BB8',gold:'#C98A1B',
 pal:['#0072BB','#54AB5D','#3B57B8','#00A0E0','#C98A1B','#8E6BB8','#A6CE39','#B23F2B','#5E9FD6','#7FB685']};
const fmtM=v=>v==null?'—':(Math.abs(v)>=1e6?(v/1e6).toFixed(1)+'M':Math.abs(v)>=1e3?(v/1e3).toFixed(0)+'K':Math.round(v));
const fmtSAR=v=>v==null?'—':'SAR '+Math.round(v).toLocaleString();
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const wd=900; // virtual width

// vertical bars with optional overlay line (combo)
function barChart(data, o={}){
  o=Object.assign({h:230,pad:{t:18,r:16,b:46,l:46},color:C.blue,val:d=>d.v,lab:d=>d.l,fmt:v=>v,line:null,lineFmt:v=>v,lineColor:C.red,unit:''},o);
  const W=wd,H=o.h,P=o.pad, iw=W-P.l-P.r, ih=H-P.t-P.b;
  const max=Math.max(...data.map(o.val),1)*1.12;
  const bw=iw/data.length;
  let s=`<svg viewBox="0 0 ${W} ${H}" class="ch">`;
  for(let g=0;g<=4;g++){const y=P.t+ih*g/4;const v=max*(1-g/4);s+=`<line x1="${P.l}" y1="${y}" x2="${W-P.r}" y2="${y}" stroke="${C.line}"/>`;s+=`<text x="${P.l-6}" y="${y+3}" text-anchor="end" class="cax">${o.fmt(Math.round(v))}</text>`;}
  data.forEach((d,i)=>{const v=o.val(d);const bh=v/max*ih;const x=P.l+i*bw+bw*0.16;const w=bw*0.68;const y=P.t+ih-bh;
    s+=`<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${Math.max(bh,0).toFixed(1)}" rx="2.5" fill="${typeof o.color==='function'?o.color(d):o.color}"><title>${esc(o.lab(d))}: ${esc(o.fmt(v))}</title></rect>`;
    if(bw>22||data.length<=14)s+=`<text x="${(P.l+i*bw+bw/2).toFixed(1)}" y="${H-P.b+15}" text-anchor="middle" class="cax2" transform="rotate(${data.length>10?'35':'0'} ${(P.l+i*bw+bw/2).toFixed(1)} ${H-P.b+15})">${esc(o.lab(d))}</text>`;});
  if(o.line){const lmax=Math.max(...data.map(o.line).filter(v=>v!=null),1)*1.15;
    let pts=data.map((d,i)=>{const v=o.line(d);if(v==null)return null;return[P.l+i*bw+bw/2,P.t+ih-v/lmax*ih];}).filter(Boolean);
    s+=`<polyline points="${pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' ')}" fill="none" stroke="${o.lineColor}" stroke-width="2.5"/>`;
    pts.forEach(p=>s+=`<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3.2" fill="#fff" stroke="${o.lineColor}" stroke-width="2"/>`);
    data.forEach((d,i)=>{const v=o.line(d);if(v==null)return;const y=P.t+ih-v/lmax*ih;s+=`<text x="${(P.l+i*bw+bw/2).toFixed(1)}" y="${(y-7).toFixed(1)}" text-anchor="middle" class="cln" fill="${o.lineColor}">${o.lineFmt(v)}</text>`;});}
  return s+'</svg>';
}

// horizontal bars (ranked) with value label
function hbar(data, o={}){
  o=Object.assign({val:d=>d.v,lab:d=>d.l,sub:null,fmt:v=>v,color:C.blue,rh:26,maxlab:30},o);
  const W=o.W||wd, n=data.length, H=n*o.rh+14, labw=o.labw||240, barx=labw+8, iw=W-barx-(o.vr||90);   // o.W / o.labw / o.vr (room for the value label): half-width cards keep readable labels
  const max=Math.max(...data.map(o.val),1);
  let s=`<svg viewBox="0 0 ${W} ${H}" class="ch">`;
  const RTL=document.documentElement.dir==='rtl', X=x=>RTL?W-x:x, A=a=>RTL?(a==='end'?'start':'end'):a;   // Arabic: mirror the chart
  data.forEach((d,i)=>{const v=o.val(d);const w=Math.max(v/max*iw,1);const y=7+i*o.rh;
    s+=`<text x="${X(labw)}" y="${y+o.rh/2+1}" text-anchor="${A('end')}" class="chl">${esc(String(o.lab(d)).slice(0,o.maxlab))}</text>`;
    s+=`<rect x="${(RTL?W-barx-w:barx).toFixed(1)}" y="${y+3}" width="${w.toFixed(1)}" height="${o.rh-9}" rx="2.5" fill="${typeof o.color==='function'?o.color(d):o.color}"><title>${esc(o.lab(d))}: ${esc(o.fmt(v))}</title></rect>`;
    s+=`<text x="${X(barx+w+6)}" y="${y+o.rh/2+1}" text-anchor="${A('start')}" class="chv">${esc(o.fmt(v))}${o.sub?'  <tspan class="chs">'+esc(o.sub(d))+'</tspan>':''}</text>`;});
  return s+'</svg>';
}

// donut
function donut(segs, o={}){
  o=Object.assign({size:200,thick:34,center:''},o);
  const R=o.size/2, r=R-o.thick, cx=R, cy=R, tot=segs.reduce((a,s)=>a+s.v,0)||1;
  let ang=-Math.PI/2, s=`<svg viewBox="0 0 ${o.size} ${o.size}" style="width:${o.size}px;height:${o.size}px">`;
  segs.forEach((g,i)=>{const a2=ang+g.v/tot*2*Math.PI;const x1=cx+R*Math.cos(ang),y1=cy+R*Math.sin(ang),x2=cx+R*Math.cos(a2),y2=cy+R*Math.sin(a2);
    const xi2=cx+r*Math.cos(a2),yi2=cy+r*Math.sin(a2),xi1=cx+r*Math.cos(ang),yi1=cy+r*Math.sin(ang);
    const big=(a2-ang)>Math.PI?1:0;const col=g.c||C.pal[i%C.pal.length];
    if(g.v>0)s+=`<path d="M${x1.toFixed(1)} ${y1.toFixed(1)} A${R} ${R} 0 ${big} 1 ${x2.toFixed(1)} ${y2.toFixed(1)} L${xi2.toFixed(1)} ${yi2.toFixed(1)} A${r} ${r} 0 ${big} 0 ${xi1.toFixed(1)} ${yi1.toFixed(1)} Z" fill="${col}"><title>${esc(g.l)}: ${g.v}</title></path>`;
    ang=a2;});
  if(o.center)s+=`<text x="${cx}" y="${cy-4}" text-anchor="middle" class="eh-dc" style="font-family:var(--eh-display);font-weight:600;font-size:26px;fill:var(--eh-ink)">${o.center}</text><text x="${cx}" y="${cy+15}" text-anchor="middle" style="font-family:var(--eh-font);font-weight:500;font-size:11.5px;fill:var(--eh-ink-3)">${esc(o.csub||'')}</text>`;
  return s+'</svg>';
}
function legend(segs){return '<div class="leg">'+segs.map((g,i)=>`<span class="lgi"><span class="lgd" style="background:${g.c||C.pal[i%C.pal.length]}"></span>${esc(g.l)} <b>${g.v}</b></span>`).join('')+'</div>';}

// grouped bars (e.g., 2025 vs 2026 across metrics)
function groupBar(groups, series, o={}){
  o=Object.assign({h:230,pad:{t:18,r:16,b:42,l:46},fmt:v=>v},o);
  const W=wd,H=o.h,P=o.pad,iw=W-P.l-P.r,ih=H-P.t-P.b;
  const max=Math.max(...groups.flatMap(g=>series.map(s=>g[s.k])),1)*1.14;
  const gw=iw/groups.length, bw=gw*0.7/series.length;
  let s=`<svg viewBox="0 0 ${W} ${H}" class="ch">`;
  for(let i=0;i<=4;i++){const y=P.t+ih*i/4;s+=`<line x1="${P.l}" y1="${y}" x2="${W-P.r}" y2="${y}" stroke="${C.line}"/><text x="${P.l-6}" y="${y+3}" text-anchor="end" class="cax">${o.fmt(Math.round(max*(1-i/4)))}</text>`;}
  groups.forEach((g,gi)=>{series.forEach((se,si)=>{const v=g[se.k]||0;const bh=v/max*ih;const x=P.l+gi*gw+gw*0.15+si*bw;const y=P.t+ih-bh;
    s+=`<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${(bw*0.9).toFixed(1)}" height="${Math.max(bh,0).toFixed(1)}" rx="2" fill="${se.c}"><title>${esc(g.l)} · ${esc(se.l)}: ${esc(o.fmt(v))}</title></rect>`;});
    s+=`<text x="${(P.l+gi*gw+gw/2).toFixed(1)}" y="${H-P.b+16}" text-anchor="middle" class="cax2">${esc(g.l)}</text>`;});
  return s+'</svg>';
}

// scatter (x,y) e.g. value vs duration
function scatter(pts, o={}){
  o=Object.assign({h:260,pad:{t:18,r:18,b:42,l:54},xf:v=>v,yf:v=>v,xl:'',yl:'',color:C.blue},o);
  const W=wd,H=o.h,P=o.pad,iw=W-P.l-P.r,ih=H-P.t-P.b;
  const xmax=Math.max(...pts.map(p=>p.x),1)*1.1, ymax=Math.max(...pts.map(p=>p.y),1)*1.1;
  let s=`<svg viewBox="0 0 ${W} ${H}" class="ch">`;
  for(let i=0;i<=4;i++){const y=P.t+ih*i/4;s+=`<line x1="${P.l}" y1="${y}" x2="${W-P.r}" y2="${y}" stroke="${C.line}"/><text x="${P.l-6}" y="${y+3}" text-anchor="end" class="cax">${o.yf(Math.round(ymax*(1-i/4)))}</text>`;}
  for(let i=0;i<=4;i++){const x=P.l+iw*i/4;s+=`<text x="${x}" y="${H-P.b+16}" text-anchor="middle" class="cax2">${o.xf(Math.round(xmax*i/4))}</text>`;}
  pts.forEach(p=>{const x=P.l+p.x/xmax*iw,y=P.t+ih-p.y/ymax*ih;s+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${p.r||5}" fill="${p.c||o.color}" fill-opacity="0.62" stroke="#fff"><title>${esc(p.t||'')}</title></circle>`;});
  s+=`<text x="${P.l+iw/2}" y="${H-4}" text-anchor="middle" class="caxt">${esc(o.xl)}</text>`;
  return s+'</svg>';
}
