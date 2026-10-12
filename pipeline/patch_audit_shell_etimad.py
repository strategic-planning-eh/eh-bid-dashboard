"""patch_audit_shell_etimad.py — Government Tenders page (build_etimad_page.py): audit fix shell-20 (12 Oct 2026).

What was wrong, and what changes:
  (a) "What the Kingdom is buying" coloured Still open / Closed with the same blue and green that meant Core service /
      Related one section earlier. Open and closed now have their own pair (gold for still open, grey for closed) in
      the legend, the "by type of work" bars and the "published per day" chart.
  (b) The Region column could be clicked to sort but every row says "Not available", so nothing happened. It is no
      longer offered as a sort.
  (c) Sorting by title put "… No. 22" before "… No. 8". Text columns now sort numbers inside the text by value.

The page is written by build_etimad_page.py at publish time, so only the generator changes.
Exact-string edits; stops if an anchor is missing. Change table: change_table_audit_shell_etimad.md/.json.
Run once:  python3 pipeline/patch_audit_shell_etimad.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import patchlib
from patchlib import load, rep, FILES, FAILURES, write_change_table

E = os.path.join(HERE, 'build_etimad_page.py')
if '--open:var(--eh-c5)' in open(E, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(E, 'et')

rep('et', '''  --core:var(--eh-c1);--adj:var(--eh-c2);--bar:var(--eh-c1);--bar2:var(--eh-c2);--grid:var(--eh-line);''',
    '''  --core:var(--eh-c1);--adj:var(--eh-c2);--bar:var(--eh-c1);--bar2:var(--eh-c2);--grid:var(--eh-line);
  --open:var(--eh-c5);--closed:var(--eh-grey);   /* audit shell-20: open / closed never reuse the Core / Related colours */''',
    'css', 'shell-20a: own colour pair for open / closed')
rep('et', '''cols=stack?['var(--core)','var(--adj)']:['var(--bar)'];''', '''cols=stack?(opt.cols||['var(--core)','var(--adj)']):['var(--bar)'];''',
    'code', 'shell-20a: stacked bars accept their own colours')
rep('et', '''[{name:L('Still open when checked','مفتوحة عند المراجعة'),color:'var(--core)',vals:DY.map(r=>r.open)},{name:L('Closed','مغلقة'),color:'var(--adj)',vals:DY.map(r=>r.n-r.open)}]''',
    '''[{name:L('Still open when checked','مفتوحة عند المراجعة'),color:'var(--open)',vals:DY.map(r=>r.open)},{name:L('Closed','مغلقة'),color:'var(--closed)',vals:DY.map(r=>r.n-r.open)}]''',
    'code', 'shell-20a: published-per-day chart uses the open / closed pair')
rep('et', '''<div class="legend"><span><i style="background:var(--core)"></i><span data-en="Still open when checked" data-ar="مفتوحة عند المراجعة">Still open when checked</span></span><span><i style="background:var(--adj)"></i><span data-en="Already closed" data-ar="مغلقة">Already closed</span></span></div>''',
    '''<div class="legend"><span><i style="background:var(--open)"></i><span data-en="Still open when checked" data-ar="مفتوحة عند المراجعة">Still open when checked</span></span><span><i style="background:var(--closed)"></i><span data-en="Already closed" data-ar="مغلقة">Already closed</span></span></div>''',
    'code', 'shell-20a: market legend uses the open / closed pair')
rep('et', '''  const k=(C[SORT.k]||C.sub)[1];rows=rows.slice().sort((a,b)=>{const x=k(a),y=k(b);return (x>y?1:x<y?-1:0)*SORT.dir});
  let h=`<table class="t"><thead><tr>${order.map(c=>`<th data-k="${c}" class="${SORT.k===c?'s'+(SORT.dir<0?' up':''):''}">${C[c][0]}</th>`).join('')}</tr></thead><tbody>`;''',
    '''  const k=(C[SORT.k]||C.sub)[1],cmp=(x,y)=>typeof x==='string'&&typeof y==='string'?x.localeCompare(y,LANG==='ar'?'ar':'en',{numeric:true}):(x>y?1:x<y?-1:0);   // audit shell-20c: "No. 8" before "No. 22"
  rows=rows.slice().sort((a,b)=>cmp(k(a),k(b))*SORT.dir);
  let h=`<table class="t"><thead><tr>${order.map(c=>c==='region'?`<th>${C[c][0]}</th>`:`<th data-k="${c}" class="${SORT.k===c?'s'+(SORT.dir<0?' up':''):''}">${C[c][0]}</th>`).join('')}</tr></thead><tbody>`;''',
    'code', 'shell-20b/c: Region not sortable; text sorts numbers by value')
rep('et', '''  document.querySelectorAll('#list th').forEach(th=>th.onclick=()=>{SORT.dir=(SORT.k===th.dataset.k?-SORT.dir:1);SORT.k=th.dataset.k;render()});''',
    '''  document.querySelectorAll('#list th[data-k]').forEach(th=>th.onclick=()=>{SORT.dir=(SORT.k===th.dataset.k?-SORT.dir:1);SORT.k=th.dataset.k;render()});''',
    'code', 'shell-20b: only sortable headings get a click handler')

# the "by type of work" chart: the only call that passes {labelW:260} right after the market rows
i = FILES['et'].find("hbars('mk-sector',"); j = FILES['et'].find('\n', i)
if i > 0 and FILES['et'][i:j].endswith("})),{labelW:260});"):
    FILES['et'] = FILES['et'][:j - len("{labelW:260});")] + "{cols:['var(--open)','var(--closed)'],labelW:260});" + FILES['et'][j:]
    patchlib.CHANGES.append({'file': 'et', 'kind': 'exact', 'category': 'code', 'note': 'shell-20a: by type of work — open / closed colours',
                             'occurrences': 1, 'ok': True, 'old': '{labelW:260});', 'new': "{cols:['var(--open)','var(--closed)'],labelW:260});"})
else:
    FAILURES.append({'file': 'et', 'note': 'mk-sector options anchor', 'old': FILES['et'][i:j][-120:]})

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(E, 'w', encoding='utf-8').write(FILES['et'])
write_change_table(os.path.join(HERE, 'change_table_audit_shell_etimad'), 'Government Tenders — audit fix shell-20')
print('patched: pipeline/build_etimad_page.py')
