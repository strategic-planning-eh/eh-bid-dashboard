"""patch_audit_shell_gov.py — Regulatory news (hub/government_news.html): audit fixes shell-03, 04, 19 (12 Oct 2026).

What was wrong, and what changes:
  shell-03  The headline search box lost the cursor after the first letter (the list redraws on every key and the box
            was redrawn with it), so typing "beta" left "b". The box now keeps the cursor and its position while the
            list updates.
  shell-04  In Arabic the page showed Hijri (Umm al-Qura) dates — and labelled the September 2026 brief "ربيع الأول
            1448 هـ" — while every other hub page uses Gregorian dates; the "Collected" time stayed in English.
            Dates and month names are now Gregorian in Arabic too (Arabic month names, Latin digits), and the
            collection time is written in the page language.
  shell-19  "In the last 30 days" was measured from the reader's clock while "this collection week" is measured from
            the feed, and a story dated after the collection counted as recent. Both now count from the collection
            date; a story dated after the collection is treated as undated (shown with the day it was first seen).

Exact-string edits; stops if an anchor is missing. Change table: change_table_audit_shell_gov.md/.json.
Run once:  python3 pipeline/patch_audit_shell_gov.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

G = os.path.join(HERE, '..', 'hub', 'government_news.html')
if 'function genDay(' in open(G, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(G, 'gov')

rep('gov', '''const fmtD=iso=>{if(!iso)return L('date n/a','بدون تاريخ');const d=new Date(iso+'T00:00:00');return d.toLocaleDateString(LANG==='ar'?'ar-SA-u-nu-latn':'en-GB',{day:'2-digit',month:'short',year:'numeric'});};
const daysAgo=iso=>iso?Math.floor((Date.now()-new Date(iso+'T00:00:00'))/864e5):null;''',
    '''const LOC=()=>LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB';   // Gregorian in Arabic too, as on every hub page (audit shell-04)
const fmtD=iso=>{if(!iso)return L('date n/a','بدون تاريخ');const d=new Date(iso+'T00:00:00');return d.toLocaleDateString(LOC(),{day:'2-digit',month:'short',year:'numeric'});};
// ages are counted from the collection date, not the reader's clock (audit shell-19)
function genDay(){return FEED&&/^\\d{4}-\\d{2}-\\d{2}/.test(FEED.generated||'')?FEED.generated.slice(0,10):new Date().toISOString().slice(0,10);}
const daysAgo=iso=>iso?Math.floor((new Date(genDay()+'T00:00:00')-new Date(iso+'T00:00:00'))/864e5):null;
function fmtGen(){const g=FEED.generated||'';const d=new Date(g);if(!g||isNaN(d))return FEED.generated_ksa==='not yet run'?L('not yet run','لم يُشغَّل بعد'):(FEED.generated_ksa||g);
 return d.toLocaleString(LOC(),{timeZone:'Asia/Riyadh',day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit',hour12:false})+L(' (KSA)',' بتوقيت السعودية');}''',
    'code', 'shell-04/19: Gregorian dates in Arabic; ages counted from the collection date; collection time in the page language')
rep('gov', '''const monthName=m=>{const [y,mo]=m.split('-');return new Date(+y,+mo-1,1).toLocaleDateString(LANG==='ar'?'ar-SA-u-nu-latn':'en-GB',{month:'long',year:'numeric'});};''',
    '''const monthName=m=>{const [y,mo]=m.split('-');return new Date(+y,+mo-1,1).toLocaleDateString(LOC(),{month:'long',year:'numeric'});};''',
    'code', 'shell-04: the September 2026 brief is labelled September 2026 in Arabic, not a Hijri month')
rep('gov', '''<span>${L('Collected','تاريخ الجمع')} <b dir="ltr">${esc(FEED.generated_ksa||FEED.generated)}</b></span>''',
    '''<span>${L('Collected','تاريخ الجمع')} <b>${esc(fmtGen())}</b></span>''', 'copy', 'shell-04: "Collected" time in Arabic')
rep('gov', '''<b dir="ltr">${fmtD(FEED.week_from)} – ${fmtD(FEED.week_to)}</b>''', '''<b>${fmtD(FEED.week_from)} – ${fmtD(FEED.week_to)}</b>''',
    'copy', 'shell-04: Arabic week range reads right to left')
rep('gov', '''<input placeholder="${L('Search headlines…','ابحث في العناوين…')}" value="${esc(S.q)}" oninput="S.q=this.value;render()">''',
    '''<input id="gq" placeholder="${L('Search headlines…','ابحث في العناوين…')}" value="${esc(S.q)}" oninput="S.q=this.value;qRender(this)">''',
    'code', 'shell-03: search box keeps focus while typing')
rep('gov', '''function render(){
 document.querySelectorAll('#lang button')''', '''// redraw the list without losing the search box's cursor (audit shell-03)
function qRender(el){const a=el.selectionStart,b=el.selectionEnd;render();const q=$('gq');if(q){q.focus();try{q.setSelectionRange(a,b);}catch(e){}}}
function render(){
 document.querySelectorAll('#lang button')''', 'code', 'shell-03: qRender() restores focus and caret')
rep('gov', '''fetch('gov_news.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();}).then(j=>{FEED=j;render();})''',
    '''fetch('gov_news.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();}).then(j=>{FEED=j;
  const g=genDay();(FEED.items||[]).forEach(it=>{if(it.date&&FEED.generated&&it.date>g){it.date_after_collection=it.date;it.date=null;}});   // a date after the collection cannot be right: treat as undated (audit shell-19)
  render();})''', 'data', 'shell-19: stories dated after the collection are treated as undated')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(G, 'w', encoding='utf-8').write(FILES['gov'])
write_change_table(os.path.join(HERE, 'change_table_audit_shell_gov'), 'Regulatory news — audit fixes shell-03/04/19')
print('patched: hub/government_news.html')
