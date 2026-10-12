"""patch_exec_rtl.py — Executive Summary charts read right-to-left in Arabic (12 Oct 2026).

In Arabic the tender funnel and the "where we win" bar charts were drawn left-to-right like the English: labels on the
left, bars growing rightwards, chart titles in the top-left corner. They now mirror, like every other horizontal bar
chart in the hub (charts.js hbar since the v2 design): labels on the right, bars growing leftwards from the right
edge, counts and percentages beyond the bar end, and each chart's title and scope in the top-right corner. English is
unchanged. The exported PNG is the same picture, so it mirrors too.

Run once:  python3 pipeline/patch_exec_rtl.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

J = os.path.join(HERE, 'app.js')
if 'exRTL(' in open(J, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(J, 'app')

# shared helper + titles
rep('app', "function exSvgHead(W,title,sub){ return `<text x=\"14\" y=\"20\" class=\"exT\">${esc(title)}</text>${sub?`<text x=\"14\" y=\"36\" class=\"exS\">${esc(sub)}</text>`:''}`; }",
    "// Arabic: mirror x positions and swap text anchors (12 Oct 2026)\n"
    "function exRTL(W){const R=document.documentElement.dir==='rtl';return {R:R,X:x=>R?W-x:x,A:a=>R?(a==='end'?'start':a==='start'?'end':a):a,B:(x,w)=>R?W-x-w:x};}\n"
    "function exSvgHead(W,title,sub){ const m=exRTL(W); return `<text x=\"${m.X(14)}\" y=\"20\" text-anchor=\"${m.A('start')}\" class=\"exT\">${esc(title)}</text>${sub?`<text x=\"${m.X(14)}\" y=\"36\" text-anchor=\"${m.A('start')}\" class=\"exS\">${esc(sub)}</text>`:''}`; }",
    'rtl', 'chart titles sit top-right in Arabic')

# funnel
rep('app', " let leak=null,leakI=-1;\n let s=`<svg id=\"ex-funnel\"",
    " let leak=null,leakI=-1; const m=exRTL(W);\n let s=`<svg id=\"ex-funnel\"", 'rtl', 'funnel mirror helper')
rep('app', "  s+=`<text x=\"${x0-10}\" y=\"${y+20}\" text-anchor=\"end\" class=\"chl\">${esc(l)}</text><rect x=\"${x0}\" y=\"${y+4}\" width=\"${w.toFixed(1)}\" height=\"26\" rx=\"4\" fill=\"${col}\"",
    "  s+=`<text x=\"${m.X(x0-10)}\" y=\"${y+20}\" text-anchor=\"${m.A('end')}\" class=\"chl\">${esc(l)}</text><rect x=\"${m.B(x0,w).toFixed(1)}\" y=\"${y+4}\" width=\"${w.toFixed(1)}\" height=\"26\" rx=\"4\" fill=\"${col}\"",
    'rtl', 'funnel labels and bars mirror')
rep('app', "  s+=`<text x=\"${x0+w+8}\" y=\"${y+22}\" class=\"chv\">${v}</text>${drop!=null?`<text x=\"${x0+w+8+String(v).length*9+10}\" y=\"${y+22}\" class=\"chs\">−${drop}%</text>`:''}`;});",
    "  s+=`<text x=\"${m.X(x0+w+8)}\" y=\"${y+22}\" text-anchor=\"${m.A('start')}\" class=\"chv\">${v}</text>${drop!=null?`<text x=\"${m.X(x0+w+8+String(v).length*9+10)}\" y=\"${y+22}\" text-anchor=\"${m.A('start')}\" class=\"chs\" direction=\"ltr\">−${drop}%</text>`:''}`;});",
    'rtl', 'funnel counts and drops mirror')

# where-we-win bars
rep('app', " let s=`<svg id=\"${id}\" viewBox=\"0 0 ${W} ${H}\" class=\"ch exsvg\">${exSvgHead(W,title,t('Scope','النطاق')+': '+exScopeLabel())}`;\n rows.forEach((r,i)=>{const y=50+i*rh,",
    " const m=exRTL(W);\n let s=`<svg id=\"${id}\" viewBox=\"0 0 ${W} ${H}\" class=\"ch exsvg\">${exSvgHead(W,title,t('Scope','النطاق')+': '+exScopeLabel())}`;\n rows.forEach((r,i)=>{const y=50+i*rh,",
    'rtl', 'win-bars mirror helper')
rep('app', "  s+=`<text x=\"${x0-10}\" y=\"${y+19}\" text-anchor=\"end\" class=\"chl\">${esc(lab(r))}</text><rect x=\"${x0}\" y=\"${y+5}\" width=\"${wa.toFixed(1)}\"",
    "  s+=`<text x=\"${m.X(x0-10)}\" y=\"${y+19}\" text-anchor=\"${m.A('end')}\" class=\"chl\">${esc(lab(r))}</text><rect x=\"${m.B(x0,wa).toFixed(1)}\" y=\"${y+5}\" width=\"${wa.toFixed(1)}\"",
    'rtl', 'win-bars labels and decided bars mirror')
rep('app', "/><rect x=\"${x0}\" y=\"${y+5}\" width=\"${ww.toFixed(1)}\" height=\"22\" rx=\"3\" fill=\"${r.grey?EXC.grey:EXC.won}\">",
    "/><rect x=\"${m.B(x0,ww).toFixed(1)}\" y=\"${y+5}\" width=\"${ww.toFixed(1)}\" height=\"22\" rx=\"3\" fill=\"${r.grey?EXC.grey:EXC.won}\">",
    'rtl', 'win-bars won bars mirror')
rep('app', "  s+=`<text x=\"${x0+wa+8}\" y=\"${y+21}\" class=\"chv\">${r.won||0}/${r.awarded||0}</text><text x=\"${x0+wa+8+String((r.won||0)+'/'+(r.awarded||0)).length*9+8}\" y=\"${y+21}\" class=\"chs\">",
    "  s+=`<text x=\"${m.X(x0+wa+8)}\" y=\"${y+21}\" text-anchor=\"${m.A('start')}\" class=\"chv\" direction=\"ltr\">${r.won||0}/${r.awarded||0}</text><text x=\"${m.X(x0+wa+8+String((r.won||0)+'/'+(r.awarded||0)).length*9+8)}\" y=\"${y+21}\" text-anchor=\"${m.A('start')}\" class=\"chs\">",
    'rtl', 'win-bars counts mirror')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(J, 'w', encoding='utf-8').write(FILES['app'])
write_change_table(os.path.join(HERE, 'change_table_exec_rtl'), 'Executive Summary charts mirror in Arabic')
print('patched: app.js')
