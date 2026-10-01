"""patch_ntf_jump.py — "Since your last visit" links go straight to the tenders they mention (02/10/2026).

Before: every link in the strip only switched tab (go('tenders') / go('winloss') / go('pricing')), leaving the reader to
find the flagged rows in a list of hundreds.
After:
  • "N new tender(s)" and "N row update(s)" open All tenders filtered to exactly those tenders, scroll to the first and
    highlight them; a pill above the table says what is shown and "Show all tenders" clears it.
  • Each decision link (#12/26 → Won) opens All tenders on that single tender (its outcome, winner and loss reason are
    in the row), instead of the Win/loss charts, which do not list tenders.
  • "N pricing update(s)" opens Pricing with those tenders expanded and scrolled to.
  • Changing any filter, or Reset, clears the jump filter.
Edits pipeline/app.js only (the Bid & Tender app is rebuilt every pipeline run). Run once.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
A = os.path.join(HERE, 'app.js'); K = 'app.js'
if 'function jumpTo(' in open(A, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(A, A + '.pre-jump.bak'); load(A, K); N = 0
def R(a, b, note):
    global N; N += 1; rep(K, a, b, 'ntf-jump', note)
# links in the strip
R("onclick=\"go(\\'tenders\\')\">'+NTF.nw.size", "onclick=\"jumpTo(\\'tenders\\',\\'nw\\')\">'+NTF.nw.size", 'New tenders → filtered list')
R("onclick=\"go(\\'winloss\\')\">'+lbl(k)", "onclick=\"jumpTo(\\'tenders\\',\\''+k+'\\')\">'+lbl(k)", 'Decision → that tender')
R("onclick=\"go(\\'pricing\\')\">'+NTF.px.size", "onclick=\"jumpTo(\\'pricing\\',\\'px\\')\">'+NTF.px.size", 'Pricing updates → expanded cards')
R("onclick=\"go(\\'tenders\\')\">'+NTF.upd.size", "onclick=\"jumpTo(\\'tenders\\',\\'upd\\')\">'+NTF.upd.size", 'Row updates → filtered list')
# jump function (after go)
R("function go(id){", """function jumpTo(tab,which){
 var keys=(which==='nw'||which==='upd'||which==='px')?Array.from(NTF[which]):[which];
 if(!keys.length){go(tab);return;}
 if(tab==='tenders'){TF.year='all';TF.outcome='all';TF.platform='all';TF.svc='all';TF.q='';TF.only=new Set(keys);renderTenders();}
 if(tab==='pricing'){BA.pricing.rows.forEach(function(r,i){if(keys.indexOf(r.year+'-'+r.sn)>-1)pxExpand[i]=true;});renderPricing();}
 go(tab);
 if(!document.getElementById('bkflashcss')){var st=document.createElement('style');st.id='bkflashcss';st.textContent='@keyframes bkflash{0%,60%{background:#FFF1C9;box-shadow:inset 4px 0 0 #E8862E}100%{background:transparent;box-shadow:none}}.bkflash,.bkflash td{animation:bkflash 2.6s ease-out}';document.head.appendChild(st);}
 setTimeout(function(){var first=null;keys.forEach(function(k){document.querySelectorAll('[data-bk="'+k+'"]').forEach(function(el){if(!first)first=el;el.classList.remove('bkflash');void el.offsetWidth;el.classList.add('bkflash');});});
  if(first)first.scrollIntoView({behavior:'smooth',block:'center'});},120);
}
function go(id){""", 'jumpTo(): filter, switch tab, scroll, highlight')
# tenders list: filter, row anchors, pill
R("(!TF.q||((b.title+' '+b.client+' #'+b.sn).toLowerCase().includes(TF.q.toLowerCase()))));",
  "(!TF.q||((b.title+' '+b.client+' #'+b.sn).toLowerCase().includes(TF.q.toLowerCase())))&&\n   (!TF.only||TF.only.has(b.year+'-'+b.sn)));", 'Tenders list honours the jump filter')
R("const rows=list.map(b=>`<tr>", "const rows=list.map(b=>`<tr data-bk=\"${b.year}-${b.sn}\">", 'Row anchor')
R(" ${ctrls}\n <div class=\"card\" style=\"padding:6px 10px\">",
  " ${ctrls}\n ${TF.only?`<div style=\"display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:-4px 0 12px;background:#FFF8EC;border:1px solid #EAD9B0;border-radius:9px;padding:8px 13px;font-size:12px;color:#5C4A14\"><b>${t('Showing the '+TF.only.size+' tender(s) flagged since '+(NTF.when||'your last visit'),'عرض '+TF.only.size+' منافسة/منافسات مُعلَّمة منذ '+(NTF.when||'آخر زيارة'))}</b><button onclick=\"TF.only=null;renderTenders()\" style=\"margin-inline-start:auto;border:1px solid #D9C48E;background:#fff;color:#8A6D2E;border-radius:7px;padding:5px 11px;font-size:11.5px;font-weight:700;cursor:pointer\">${t('Show all tenders','عرض كل المنافسات')}</button></div>`:''}\n <div class=\"card\" style=\"padding:6px 10px\">", 'Pill: what is shown + Show all')
R("function setTF(kk,v){TF[kk]=v;renderTenders();}", "function setTF(kk,v){TF[kk]=v;TF.only=null;renderTenders();}", 'Any filter change clears the jump filter')
R("TF.year='all';TF.outcome='all';TF.platform='all';TF.svc='all';TF.q='';renderTenders()", "TF.year='all';TF.outcome='all';TF.platform='all';TF.svc='all';TF.q='';TF.only=null;renderTenders()", 'Reset clears it too')
# pricing cards anchor
R("return `<div class=\"card\" style=\"margin-bottom:10px;padding:0;overflow:hidden\">", "return `<div class=\"card\" data-bk=\"${r.year}-${r.sn}\" style=\"margin-bottom:10px;padding:0;overflow:hidden\">", 'Pricing card anchor')
open(A, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_ntf_jump'), 'Change table — strip links jump to the tender')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
