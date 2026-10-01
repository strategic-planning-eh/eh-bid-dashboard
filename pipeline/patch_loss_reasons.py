"""patch_loss_reasons.py — group recorded loss reasons by meaning (02/10/2026, Youssef's rule).

The Executive Summary listed every loss reason as typed, so the same reason appeared several times in different words.
Grouping (lossCat() in app.js; the wording in the workbook is never changed):
  • Technical — any reason mentioning the technical offer or technical non-compliance
    (رفض العرض الفني · تم رفض العرض الفني · غير مطابق فنيا …) → shown as «تم رفض العرض الفني» / "Technical offer rejected".
  • Price — any reason about price or the financial offer
    (وجود عرض سعر أقل · غير مقبول ماليا · العرض الأنسب والأقل سعرا · الاعلى سعرًا · أقل العروض … سعراً · عطاء مالي …)
    → shown as «رُفض بسبب السعر» / "Rejected on price".
  • Anything else stays as written ("Rejected", "has been awarded to other bidder", «العرض الثاني وتم استبعاده»).
Each grouped row lists the original wordings underneath in small grey text, so nothing is hidden.
Technical is tested first, so a reason mentioning both is counted as technical. Run once.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
A = os.path.join(HERE, 'app.js'); K = 'app.js'
if 'function lossCat(' in open(A, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(A, A + '.pre-loss.bak'); load(A, K); N = 0
def R(a, b, note):
    global N; N += 1; rep(K, a, b, 'loss-reasons', note)
R("function exThreat(B,d){", r"""// Loss reasons grouped by meaning (rule set by Youssef, 02/10/2026). The recorded wording is never altered.
function lossNorm(s){return String(s||'').toLowerCase().replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/\s+/g,' ').trim();}
function lossCat(r){const s=lossNorm(r); if(!s)return null;
 if(/فني|technical/.test(s)||/غير مطابق/.test(s)&&!/سعر|مالي/.test(s))return {k:'tech',en:'Technical offer rejected',ar:'تم رفض العرض الفني'};
 if(/سعر|مالي|اقل|الاعلي|اعلي|ارخص|price|financial|cheaper|lower bid|higher bid/.test(s))return {k:'price',en:'Rejected on price',ar:'رُفض بسبب السعر'};
 return {k:'raw:'+String(r).trim(),en:String(r).trim(),ar:String(r).trim()};}
function exThreat(B,d){""", 'Shared classifier')
R(" const reasons={}; d.lost.forEach(b=>{const r=(b.lossreason||'').trim();if(r)reasons[r]=(reasons[r]||0)+1;});\n const rr=Object.entries(reasons).sort((a,b)=>b[1]-a[1]).map(([r,n])=>`<tr><td dir=\"auto\">${esc(r)}</td><td style=\"text-align:end\"><b>${n}</b></td></tr>`).join('')",
  " const reasons={}; d.lost.forEach(b=>{const r=(b.lossreason||'').trim();const c=lossCat(r);if(!c)return;const g=reasons[c.k]||(reasons[c.k]={c,n:0,w:{}});g.n++;g.w[r]=(g.w[r]||0)+1;});\n"
  " const rr=Object.values(reasons).sort((a,b)=>b.n-a.n).map(g=>{const grouped=g.c.k==='tech'||g.c.k==='price';const words=Object.keys(g.w);"
  "return `<tr><td dir=\"auto\">${grouped?`<b>${esc(t(g.c.en,g.c.ar))}</b>`:esc(g.c.en)}${grouped&&(words.length>1||words[0]!==g.c.ar)?`<div dir=\"auto\" style=\"font-size:10.5px;color:#8A99A3;line-height:1.45;margin-top:3px\">${words.map(w=>esc(w)+(g.w[w]>1?' ×'+g.w[w]:'')).join(' · ')}</div>`:''}</td><td style=\"text-align:end;vertical-align:top\"><b>${g.n}</b></td></tr>`;}).join('')",
  'Loss reasons grouped, original wordings kept underneath')
open(A, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_loss_reasons'), 'Change table — loss reasons grouped by meaning')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
