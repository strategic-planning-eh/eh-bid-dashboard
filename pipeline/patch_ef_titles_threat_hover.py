"""patch_ef_titles_threat_hover.py — two UI fixes reported 17 Sep 2026.

1. Environment Fund page: every chart showed its title twice — once as the card heading, once again inside the SVG
   (kept there so the exported PNG carries a title). The SVG head is now cropped out of view on the page
   (viewBox starts at y=44) and restored at export time, so the page shows one title and the PNG still has one.
     • build_ef_page.py  chart(): both chart <svg> viewBoxes start at y=44 (rows begin at y=56).
     • build_ef_page.py  exPNG(): clone gets the full viewBox back before rasterising.
   Then re-run build_ef_page.py so hub/environment_fund_2025.html is regenerated.

2. Bid & Tender app, Executive Summary → threat matrix: hovering a dot showed nothing until the browser's slow native
   tooltip appeared, so the only way to learn who a dot was was to click through to the Competitors tab. Dots now show
   an instant tooltip (name, encounters, share below EH, wins vs EH) on hover; click still opens Competitors.
     • app.js                        <title> on the dots replaced by data-tip + hover handlers; exTip helpers added.
     • build_bid_dashboard.py        .extip CSS (light + dark).
   The app is rebuilt every pipeline run, so no HTML edit is needed here.

Run once: python3 pipeline/patch_ef_titles_threat_hover.py
"""
import os, sys, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
E = os.path.join(HERE, 'build_ef_page.py'); A = os.path.join(HERE, 'app.js'); G = os.path.join(HERE, 'build_bid_dashboard.py')
if 'exTip(' in open(A, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (E, A, G): shutil.copy2(p, p + '.pre-eftitles.bak'); load(p, os.path.basename(p))

# ---- 1. Environment Fund: one title per chart on the page, title kept in the PNG
rep('build_ef_page.py',
    '<svg id="${c.id}" class="pm" viewBox="0 0 ${W} ${H}" width="100%"',
    '<svg id="${c.id}" class="pm" viewBox="0 44 ${W} ${H-44}" width="100%"',
    'ef-titles', 'Chart SVGs start below the in-SVG title, so the card heading is the only visible title', count=2)
rep('build_ef_page.py',
    "const cl=svg.cloneNode(true);const vb=svg.viewBox.baseVal;cl.setAttribute('width',vb.width);cl.setAttribute('height',vb.height);",
    "const cl=svg.cloneNode(true);const b=svg.viewBox.baseVal,vb={width:b.width,height:b.y+b.height};cl.setAttribute('viewBox',`0 0 ${vb.width} ${vb.height}`);cl.setAttribute('width',vb.width);cl.setAttribute('height',vb.height);",
    'ef-titles', 'Export restores the full viewBox so the PNG keeps its title and source line')
rep('build_ef_page.py',
    '''s+=`<rect x="${W-190}" y="14" width="12" height="12" fill="${c.colors[0]}"/><text x="${W-172}" y="24" font-size="11" fill="${ink}">${c.series[0]}</text><rect x="${W-110}" y="14" width="12" height="12" fill="${c.colors[1]}"/><text x="${W-92}" y="24" font-size="11" fill="${ink}">${c.series[1]}</text>`;''',
    '''s+=`<rect x="${W-190}" y="44" width="12" height="12" fill="${c.colors[0]}"/><text x="${W-172}" y="54" font-size="11" fill="${ink}">${c.series[0]}</text><rect x="${W-110}" y="44" width="12" height="12" fill="${c.colors[1]}"/><text x="${W-92}" y="54" font-size="11" fill="${ink}">${c.series[1]}</text>`;''',
    'ef-titles', '2024/2025 legend on the compare chart moves below the crop line so it stays visible on the page')

# ---- 2. Bid & Tender: instant hover tooltip on threat-matrix dots
OLD_DOT = ('style="cursor:pointer" onclick="exGo(\'competitors\')"><title>${esc(c.name)} · ${c.encounters} ${esc(t(\'encounters\',\'مواجهة\'))} · '
           '${esc(t(\'below EH in\',\'دون EH في\'))} ${c.undercut_pct}% ${esc(t(\'of\',\'من\'))} ${c.priced_vs} ${esc(t(\'priced\',\'مُسعَّرة\'))} · '
           '${c.wins||0} ${esc(t(\'wins vs EH\',\'فوز على EH\'))}</title></circle>`;});')
NEW_DOT = ('style="cursor:pointer" onclick="exGo(\'competitors\')" onmouseenter="exTip(event,this)" onmousemove="exTipMove(event)" onmouseleave="exTipHide()" '
           'data-tip="<b dir=&quot;auto&quot;>${esc(c.name)}</b><br>${c.encounters} ${esc(t(\'shared tenders\',\'منافسة مشتركة\'))} · '
           '${esc(t(\'below EH in\',\'دون EH في\'))} ${c.undercut_pct}% ${esc(t(\'of\',\'من\'))} ${c.priced_vs} ${esc(t(\'priced\',\'مُسعَّرة\'))}<br>'
           '${c.wins||0} ${esc(t(\'wins vs EH\',\'فوز على EH\'))} · <span style=&quot;opacity:.75&quot;>${esc(t(\'click for the full record\',\'انقر للسجل الكامل\'))}</span>"></circle>`;});')
rep('app.js', OLD_DOT, NEW_DOT, 'threat-hover', 'Dots carry a data-tip and hover handlers instead of a native <title>')
rep('app.js',
    "function exBtn(id,name){",
    "function exTipEl(){let e=document.getElementById('extip');if(!e){e=document.createElement('div');e.id='extip';e.className='extip';document.body.appendChild(e);}return e;}\n"
    "function exTip(ev,el){const e=exTipEl();e.innerHTML=el.getAttribute('data-tip')||'';e.style.display='block';exTipMove(ev);}\n"
    "function exTipMove(ev){const e=exTipEl();const w=e.offsetWidth,h=e.offsetHeight;let x=ev.clientX+14,y=ev.clientY+14;if(x+w>window.innerWidth-8)x=ev.clientX-w-14;if(y+h>window.innerHeight-8)y=ev.clientY-h-14;e.style.left=x+'px';e.style.top=y+'px';}\n"
    "function exTipHide(){const e=document.getElementById('extip');if(e)e.style.display='none';}\n"
    "function exBtn(id,name){",
    'threat-hover', 'Shared fixed-position tooltip helpers for Executive Summary charts')
rep('build_bid_dashboard.py',
    ".exq{font:700 10.5px Segoe UI,Tahoma,Arial,sans-serif;fill:#8A99A3}",
    ".exq{font:700 10.5px Segoe UI,Tahoma,Arial,sans-serif;fill:#8A99A3}\n"
    ".extip{position:fixed;z-index:9999;display:none;pointer-events:none;max-width:300px;background:#16333F;color:#fff;font:500 12px Segoe UI,Tahoma,Arial,sans-serif;line-height:1.5;padding:8px 11px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.22)}.extip b{font-weight:800}",
    'threat-hover', 'Tooltip style (light)')
rep('build_bid_dashboard.py',
    "body.dark .png{{background:#1E2830;border-color:#3A4B55;color:#CFE3F2}}",
    "body.dark .png{{background:#1E2830;border-color:#3A4B55;color:#CFE3F2}}body.dark .extip{{background:#E6EDF1;color:#16333F}}",
    'threat-hover', 'Tooltip style (dark)')

for p in (E, A, G): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_ef_titles_threat_hover'), 'Change table — EF chart titles + threat-matrix hover')
print('edits:', 7 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]
if FAILURES: sys.exit(1)
subprocess.run([sys.executable, E], cwd=HERE, check=True)
print('hub/environment_fund_2025.html regenerated')
