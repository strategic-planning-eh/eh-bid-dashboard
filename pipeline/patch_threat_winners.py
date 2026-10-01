"""patch_threat_winners.py — threat-matrix table: winners first, and how many times each rival priced below EH (02/10/2026).

Problem (Youssef): the table ranked rivals by "% of shared priced tenders where they bid below EH". Eight rows of 100%
with 0 wins invited the reading that bidding lower doesn't win — or that these are the biggest threats — when the real
threat is the rivals who have actually beaten EH.
Change (Executive Summary → threat matrix, right-hand table):
  • Two groups, labelled: "Have beaten EH" first (ranked by wins vs EH, then times priced below EH, then tenders met),
    then "Priced below EH, no win yet" (ranked by times priced below EH, then share, then tenders met).
  • New column "Priced below EH" as a count ("3 of 3") next to the share, so 100% of 2 and 100% of 10 no longer look alike.
  • Winners are included even if fewer than two of their tenders had prices disclosed.
  • Footer explains that a lower price is not a win: Saudi tenders are scored on technical merit and compliance as well.
Chart unchanged. Edits pipeline/app.js only. Run once.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
A = os.path.join(HERE, 'app.js'); K = 'app.js'
if 'const topW=beatEH' in open(A, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(A, A + '.pre-threat.bak'); load(A, K); N = 0
def R(a, b, note):
    global N; N += 1; rep(K, a, b, 'threat-winners', note)
R(" const ranked=priced.filter(c=>(c.priced_vs||0)>=2).sort((a,b)=>b.undercut_pct-a.undercut_pct||b.encounters-a.encounters||(b.wins||0)-(a.wins||0));\n const top=ranked.slice(0,8);",
  " const nBelow=c=>c.undercut_pct==null?null:Math.round(c.undercut_pct*(c.priced_vs||0)/100);\n"
  " const beatEH=all.filter(c=>(c.wins||0)>0).sort((a,b)=>(b.wins||0)-(a.wins||0)||(nBelow(b)||0)-(nBelow(a)||0)||b.encounters-a.encounters);\n"
  " const cheapNoWin=priced.filter(c=>!(c.wins>0)&&(c.priced_vs||0)>=2).sort((a,b)=>(nBelow(b)||0)-(nBelow(a)||0)||b.undercut_pct-a.undercut_pct||b.encounters-a.encounters);\n"
  " const topW=beatEH.slice(0,6), topC=cheapNoWin.slice(0,Math.max(3,9-topW.length));",
  'Two ranked groups: winners first')
OLD_ROWS = " const rows=top.map((c,i)=>`<tr style=\"cursor:pointer\" onclick=\"exGo('competitors')\"><td style=\"color:#5F7078\">${i+1}</td><td><b dir=\"auto\">${esc(c.name)}</b></td><td style=\"text-align:center\">${c.encounters}</td><td style=\"text-align:center;color:${col(c)};font-weight:700\">${c.undercut_pct}%</td><td style=\"text-align:center;color:#8A99A3\">${c.priced_vs}</td><td style=\"text-align:center\">${c.wins?`<b style=\"color:${EXC.lost}\">${c.wins}</b>`:'0'}</td></tr>`).join('');"
NEW_ROWS = (" const row=(c,i)=>`<tr style=\"cursor:pointer\" onclick=\"exGo('competitors')\"><td style=\"color:#5F7078\">${i+1}</td><td><b dir=\"auto\">${esc(c.name)}</b></td><td style=\"text-align:center\">${c.encounters}</td>"
  "<td style=\"text-align:center\">${c.wins?`<b style=\"color:${EXC.lost}\">${c.wins}</b>`:'<span style=\"color:#8A99A3\">0</span>'}</td>"
  "<td style=\"text-align:center;white-space:nowrap\">${nBelow(c)==null?'<span style=\"color:#8A99A3\">'+t('no price','بلا سعر')+'</span>':`<b>${nBelow(c)}</b> <span style=\"color:#8A99A3\">${t('of','من')} ${c.priced_vs}</span>`}</td>"
  "<td style=\"text-align:center;color:${c.undercut_pct==null?'#8A99A3':col(c)};font-weight:700\">${c.undercut_pct==null?'\\u2014':c.undercut_pct+'%'}</td></tr>`;\n"
  " const grp=(lbl,col2)=>`<tr><td colspan=\"6\" style=\"background:${col2}12;color:${col2};font-size:10.5px;font-weight:800;letter-spacing:.3px;text-transform:uppercase;padding:6px 10px\">${lbl}</td></tr>`;\n"
  " const rows=(topW.length?grp(t('Have beaten EH','تغلّبوا على EH'),EXC.lost)+topW.map(row).join(''):'')+(topC.length?grp(t('Priced below EH, no win yet','سعّروا دون EH ولم يفوزوا بعد'),'#5F7078')+topC.map((c,i)=>row(c,i+topW.length)).join(''):'');")
R(OLD_ROWS, NEW_ROWS, 'Rows: grouped, count of times below EH')
R("<th>${t('Met','مواجهات')}</th><th>${t('Below EH','دون EH')}</th><th>${t('Priced','مُسعَّرة')}</th><th>${t('Won vs EH','فاز على EH')}</th>",
  "<th>${t('Met','مواجهات')}</th><th>${t('Won vs EH','فاز على EH')}</th><th>${t('Priced below EH','سعّر دون EH')}</th><th>${t('Share','النسبة')}</th>",
  'Column order: wins, then times below, then share')
R("${t('Ranked by how often the competitor priced below EH, then by how often we meet — among competitors with at least two priced head-to-heads. Top-right of the chart is where sustained price pressure comes from; a red ring marks a competitor who has actually beaten EH. Click a row for the full record.','مرتَّب حسب تكرار التسعير دون EH ثم تكرار اللقاء — بين المنافسين الذين لهم مواجهتان مُسعَّرتان على الأقل. أعلى يمين الرسم مصدر الضغط السعري المستمر؛ الحلقة الحمراء تعني منافساً تغلّب على EH فعلاً. انقر السطر للسجل الكامل.')}",
  "${t('Rivals who have actually won against EH come first, ranked by wins and then by how many times they priced below us. Below them are rivals who priced below EH but have not won yet. A lower price does not decide a tender on its own: Saudi tenders also score technical merit, compliance and capability, which is why many rivals priced below EH and still lost. \"Priced below EH\" counts only tenders where both prices are known (\"3 of 3\"). Top-right of the chart is where sustained price pressure comes from; a red ring marks a rival who has beaten EH. Click a row for the full record.','يأتي أولاً المنافسون الذين فازوا فعلاً على EH، مرتَّبين حسب عدد مرات الفوز ثم عدد مرات التسعير دوننا. ويليهم من سعّروا دون EH ولم يفوزوا بعد. السعر الأقل لا يحسم المنافسة وحده: تُقيَّم المنافسات السعودية أيضاً على الجدارة الفنية والالتزام والقدرة، ولهذا سعّر كثيرون دون EH وخسروا. «سعّر دون EH» يحتسب فقط المنافسات المعروف فيها السعران («3 من 3»). أعلى يمين الرسم مصدر الضغط السعري المستمر؛ الحلقة الحمراء تعني منافساً تغلّب على EH. انقر السطر للسجل الكامل.')}",
  'Footer: lower price ≠ win')
open(A, 'w', encoding='utf-8').write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_threat_winners'), 'Change table — threat matrix: winners first')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f['note']) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
