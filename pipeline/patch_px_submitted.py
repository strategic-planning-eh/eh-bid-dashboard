"""patch_px_submitted.py — Pricing intelligence cards (19 Oct 2026): a pending tender that EH has submitted reads
SUBMITTED (blue accent) instead of PENDING; PENDING stays for tenders EH has not (yet) submitted."""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from patchlib import load, rep, FILES, write_change_table
P=os.path.join(HERE,'app.js'); load(P,'app')
OLD="(r.won==null?'<span style=\"color:#5F7078;font-weight:700\">'+t('PENDING','قيد الدراسة')+'</span>':"
NEW=("(r.won==null?(pxSubmitted(r)?'<span class=\"tag\" style=\"background:#E3EEFA;color:#1A5FAB;border:1px solid #1A5FAB\">'+t('SUBMITTED','تم التقديم')+'</span>'"
     ":'<span style=\"color:#5F7078;font-weight:700\">'+t('PENDING','قيد الدراسة')+'</span>'):")
if 'pxSubmitted' in FILES['app']: sys.exit('Already applied.')
ok=rep('app',OLD,NEW,'px-submitted','Pricing cards: pending tenders EH submitted are badged SUBMITTED (blue), not PENDING')
OLD2="function renderPricing(){"
NEW2=("function pxSubmitted(r){const b=BA.bidlist.find(x=>x.year==r.year&&x.sn==r.sn);return b?tSub(b):r.bidders.some(b=>b.eh&&b.price);}   // 19 Oct 2026: tracker submission state (tSub) decides; a priced EH roster row is the fallback\n"
      "function renderPricing(){")
ok2=rep('app',OLD2,NEW2,'px-submitted','Pricing cards: pxSubmitted() helper — tracker submission state per tender')
if not (ok and ok2): sys.exit('ANCHOR MISMATCH')
open(P,'w',encoding='utf-8').write(FILES['app']); write_change_table(os.path.join(HERE,'change_table_px_submitted'),'Change table — pricing cards SUBMITTED badge'); print('applied')
