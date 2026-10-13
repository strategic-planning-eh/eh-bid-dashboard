"""patch_hub_search.py — the hub's "Find a company" box shows more results and finds more companies (13 Oct 2026).

Before: the list stopped at 8 names, matched only a plain substring of the typed text, and treated Arabic spelling
variants (أ/إ/آ vs ا, ة vs ه, ى vs ي, tatweel) as different letters — so "adaa" showed two names and an Arabic search
missed records written with a different alef.
Now:
  • up to 20 results in a scrollable list (was 8), with the company's tier and region under each name
  • every typed word must appear somewhere (name, type, sector, region, city, notes or merged-duplicate aliases), in any
    order — "adaa contracting", "adaa jeddah" and "contracting adaa" all find the same company
  • Arabic and Latin text are normalised the same way the pipeline does it before matching
  • names that START with the text come first, then names containing it, then matches found elsewhere in the record
  • Arabic names are also searchable in Latin letters: each Arabic name is romanised letter by letter (الاداء → aladaa),
    and doubled letters are collapsed on both sides, so "adaa" finds شركة الاداء المتوازن للمقاولات as well as
    "Al Adaa El Motawazen Contracting Co" — the English and Arabic records of one company appear together
Run once: python3 pipeline/patch_hub_search.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P = os.path.join(HERE, '..', 'hub', 'EH_Hub.html')
if 'function qNorm(' in open(P, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(P, os.path.join(HERE, 'EH_Hub.html.pre-search.bak')); load(P, 'hub')

OLD_INIT = """    QN=mw.EHX.N.map(function(n){
      return {n:n.n, b:(n.n+' '+(n.typ||'')+' '+(n.sec||'')+' '+(n.reg||'')+' '+(n.city||'')+' '+(n.notes||'')).toLowerCase()};
    });"""
NEW_INIT = """    QN=mw.EHX.N.map(function(n){
      var k=qNorm(n.n), b=qNorm(n.n+' '+(n.typ||'')+' '+(n.sec||'')+' '+(n.reg||'')+' '+(n.rg||'')+' '+(n.city||'')+' '+(n.notes||''));
      return {n:n.n, k:k, kc:qCollapse(k+' '+qRoman(k)), s:[n.tier,n.rg].filter(function(x){return x&&x!=='—';}).join(' · '),
              b:b, bc:qCollapse(b+' '+qRoman(b))};
    });"""
OLD_INPUT = """qEl.addEventListener('input',function(){
  var v=qEl.value.trim().toLowerCase();
  if(!v||!QN){ qHide(); return; }
  var hits=[], rest=[], i;
  for(i=0;i<QN.length;i++){
    if(QN[i].n.toLowerCase().indexOf(v)>-1){ if(hits.length<8) hits.push(QN[i].n); }
    else if(QN[i].b.indexOf(v)>-1){ if(rest.length<8) rest.push(QN[i].n); }
    if(hits.length>=8) break;
  }
  hits=hits.concat(rest).slice(0,8);
  if(!hits.length){ qHide(); return; }
  qD.innerHTML=hits.map(function(n,i){return '<div class="qh" id="qopt'+i+'" role="option" aria-selected="false" tabindex="-1" style="padding:8px 12px;cursor:pointer;font-size:12.5px;border-bottom:1px solid #F0F4F7" onclick="qGo(this.textContent)">'+n.replace(/</g,'&lt;')+'</div>';}).join('');
  qD.style.display='block'; qEl.setAttribute('aria-expanded','true'); qIdx=-1; qEl.removeAttribute('aria-activedescendant');
});"""
NEW_INPUT = """// Same normalisation as the pipeline: NFKC, Arabic alef/taa/yaa variants unified, tatweel and diacritics dropped, case folded.
function qNorm(s){ s=String(s||''); try{ s=s.normalize('NFKC'); }catch(e){}
  return s.toLowerCase().replace(/[\\u0640\\u200b-\\u200f\\u064b-\\u0652]/g,'').replace(/[\\u0622\\u0623\\u0625]/g,'\\u0627').replace(/\\u0629/g,'\\u0647').replace(/\\u0649/g,'\\u064a').replace(/\\u0624/g,'\\u0648').replace(/\\u0626/g,'\\u064a').replace(/[’'ʼ`]/g,'').replace(/\\s+/g,' ').trim(); }
// Letter-by-letter romanisation of Arabic (الاداء → aladaa) so a Latin search also finds Arabic records; the reverse is not attempted.
var Q_AR={'ا':'a','ب':'b','ت':'t','ث':'th','ج':'j','ح':'h','خ':'kh','د':'d','ذ':'dh','ر':'r','ز':'z','س':'s','ش':'sh','ص':'s','ض':'d','ط':'t','ظ':'z','ع':'a','غ':'gh','ف':'f','ق':'q','ك':'k','ل':'l','م':'m','ن':'n','ه':'h','و':'w','ي':'y','ء':'a','ة':'h','ى':'a'};
function qRoman(s){ return String(s).replace(/[\u0621-\u064a]/g,function(c){ return Q_AR[c]||''; }); }
function qCollapse(s){ return String(s).replace(/(.)\1+/g,'$1'); }
var Q_MAX=20;
qEl.addEventListener('input',function(){
  var v=qNorm(qEl.value);
  if(!v||!QN){ qHide(); return; }
  var words=v.split(' ').filter(Boolean), wc=words.map(qCollapse), i, j, r, ok, starts=[], inName=[], elsewhere=[];
  for(i=0;i<QN.length;i++){
    r=QN[i]; ok=true;
    for(j=0;j<words.length;j++){ if(r.b.indexOf(words[j])<0&&r.bc.indexOf(wc[j])<0){ ok=false; break; } }
    if(!ok) continue;
    if(r.k.indexOf(v)===0) starts.push(r); else if(r.k.indexOf(v)>-1) inName.push(r);
    else { ok=true; for(j=0;j<words.length;j++){ if(r.k.indexOf(words[j])<0&&r.kc.indexOf(wc[j])<0){ ok=false; break; } } (ok?inName:elsewhere).push(r); }
    if(starts.length>=Q_MAX) break;
  }
  var hits=starts.concat(inName,elsewhere).slice(0,Q_MAX);
  if(!hits.length){ qHide(); return; }
  var esc=function(t){ return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'); };
  qD.innerHTML=hits.map(function(r,i){return '<div class="qh" id="qopt'+i+'" role="option" aria-selected="false" tabindex="-1" data-n="'+esc(r.n)+'" style="padding:7px 12px;cursor:pointer;font-size:12.5px;border-bottom:1px solid #F0F4F7" onclick="qGo(this.getAttribute(\\'data-n\\'))">'+esc(r.n)+(r.s?'<div style="font-size:10.5px;opacity:.65;margin-top:1px">'+esc(r.s)+'</div>':'')+'</div>';}).join('');
  qD.style.display='block'; qEl.setAttribute('aria-expanded','true'); qIdx=-1; qEl.removeAttribute('aria-activedescendant');
});"""
OLD_ENTER = """  else if(e.key==='Enter'&&open&&qIdx>-1){ qGo(qD.querySelectorAll('.qh')[qIdx].textContent); e.preventDefault(); }"""
NEW_ENTER = """  else if(e.key==='Enter'&&open&&qIdx>-1){ qGo(qD.querySelectorAll('.qh')[qIdx].getAttribute('data-n')); e.preventDefault(); }"""
OLD_DROP = 'id="qdrop" role="listbox" aria-label="Companies" style="display:none;position:absolute;top:36px;left:0;width:320px;max-height:300px;'
NEW_DROP = 'id="qdrop" role="listbox" aria-label="Companies" style="display:none;position:absolute;top:36px;left:0;width:360px;max-width:92vw;max-height:min(60vh,520px);'

rep('hub', OLD_INIT, NEW_INIT, 'search', 'Index normalised name, subtitle (tier · region) and a normalised blob incl. region bucket')
rep('hub', OLD_INPUT, NEW_INPUT, 'search', 'All-words matching, Arabic/Latin normalisation, Arabic names searchable in Latin letters, 20 results ranked starts-with › in name › elsewhere, subtitle per row')
rep('hub', OLD_ENTER, NEW_ENTER, 'search', 'Enter opens the selected row by its data-n (row now carries a subtitle)')
rep('hub', OLD_DROP, NEW_DROP, 'search', 'Taller, slightly wider list so 20 rows are usable; never wider than the phone screen')
open(P, 'w', encoding='utf-8').write(FILES['hub'])
write_change_table(os.path.join(HERE, 'change_table_hub_search'), 'Change table — hub: company search shows up to 20 results and matches every typed word')
print('edits:', 4 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
