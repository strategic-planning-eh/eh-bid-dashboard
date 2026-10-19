"""patch_tenders_submitted.py — All Tenders (19 Oct 2026): a pending tender EH has submitted shows SUBMITTED (teal) instead of
PENDING, in the outcome column, the outcome filter, the CSV export and the cross-tab links. Pricing cards use the same colour."""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from patchlib import load, rep, FILES, write_change_table
P=os.path.join(HERE,'app.js'); load(P,'app')
if 'function tOut(' in FILES['app']: sys.exit('Already applied.')
R=[
 ("const DOUT={'Won':'فوز','Lost':'خسارة','Not awarded':'لم تتم الترسية','Cancelled':'ملغاة','Pending':'قيد الدراسة'};",
  "const DOUT={'Won':'فوز','Lost':'خسارة','Not awarded':'لم تتم الترسية','Cancelled':'ملغاة','Pending':'قيد الدراسة','Submitted':'تم التقديم'};\n"
  "function tOut(b){return (b.outcome=='Pending'&&tSub(b))?'Submitted':b.outcome;}   // 19 Oct 2026: shown outcome — a pending tender EH submitted reads Submitted",
  'DOUT + tOut(): Submitted as a displayed outcome'),
 ("const OC={'Won':'#2E7A37','Lost':'#B23F2B','Not awarded':'#C98A1B','Cancelled':'#5E6B80','Pending':'#0072BB'};",
  "const OC={'Won':'#2E7A37','Lost':'#B23F2B','Not awarded':'#C98A1B','Cancelled':'#5E6B80','Pending':'#0072BB','Submitted':'#0B7F76'};",
  'outcome colours: Submitted teal'),
 ("(TF.outcome=='all'||b.outcome==TF.outcome)&&", "(TF.outcome=='all'||tOut(b)==TF.outcome)&&", 'outcome filter matches the shown outcome'),
 ("const outcomes=['Won','Lost','Not awarded','Cancelled','Pending'].filter(o=>BA.bidlist.some(b=>b.outcome==o));",
  "const outcomes=['Won','Lost','Not awarded','Cancelled','Submitted','Pending'].filter(o=>BA.bidlist.some(b=>tOut(b)==o));",
  'outcome filter lists Submitted'),
 ("<td><span class=\"tag\" style=\"background:${OC[b.outcome]}\">${t(b.outcome.toUpperCase(),DOUT[b.outcome]||b.outcome)}</span>",
  "<td><span class=\"tag\" style=\"background:${OC[tOut(b)]}\">${t(tOut(b).toUpperCase(),DOUT[tOut(b)]||tOut(b))}</span>",
  'outcome cell shows SUBMITTED'),
 ("tNeeds(b)?tDaysPast(b):'',b.outcome,b.value||''", "tNeeds(b)?tDaysPast(b):'',tOut(b),b.value||''", 'CSV export shows Submitted'),
 ("+t(b.outcome,(typeof DOUT!=='undefined'&&DOUT[b.outcome])||b.outcome)+'</a>'", "+t(tOut(b),(typeof DOUT!=='undefined'&&DOUT[tOut(b)])||tOut(b))+'</a>'", 'cross-tab links show Submitted'),
 ("'<span class=\"tag\" style=\"background:#E3EEFA;color:#1A5FAB;border:1px solid #1A5FAB\">'+t('SUBMITTED','تم التقديم')+'</span>'",
  "'<span class=\"tag\" style=\"background:#0B7F76\">'+t('SUBMITTED','تم التقديم')+'</span>'", 'pricing cards: same teal SUBMITTED tag'),
]
bad=[d for o,n,d in R if not rep('app',o,n,'tenders-submitted',d)]
if bad: sys.exit('ANCHOR MISMATCH: '+'; '.join(bad))
open(P,'w',encoding='utf-8').write(FILES['app']); write_change_table(os.path.join(HERE,'change_table_tenders_submitted'),'Change table — All Tenders SUBMITTED outcome'); print('applied')
