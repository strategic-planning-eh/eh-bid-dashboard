"""patch_bid_appjs.py — companion to patch_visual_upgrade.py. Applies the KPI hero-tile reorder (D-B4) to
pipeline/app.js, which build_bid_dashboard.py inlines into the hourly bid dashboard. app.js was not available in the
build sandbox, so this script is UNTESTED against the real file: it uses the exact rKPI() text found in the served
EH_Bid_Analysis_CURRENT.html. If the anchor is not found it exits with the mismatch shown — do not force it."""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P=os.path.join(HERE,'app.js')
if not os.path.exists(P): sys.exit('pipeline/app.js not found')
load(P,'app')
OLD=("function rKPI(){$('kstrip').innerHTML=\n"
 " kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),'2024–2026')+\n"
 " kc('SAR '+fmtM(k.pipeline),t('Total tendered value','إجمالي قيمة المنافسات'),k.with_value+t(' priced',' مُسعّرة'))+\n"
 " kc('SAR '+fmtM(k.open_pipeline),t('Open pipeline','المحفظة المفتوحة'),k.open_count+t(' pending',' قيد الانتظار'))+\n"
 " kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/'+k.awarded+t(' awarded',' مُرساة'),k.win_rate>=50?'g':'r')+\n")
NEW=("function rKPI(){$('kstrip').innerHTML=\n"
 " kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/'+k.awarded+t(' awarded',' مُرساة'),(k.win_rate>=50?'g':'r')+' hero')+\n"
 " kc('SAR '+fmtM(k.pipeline),t('Total tendered value','إجمالي قيمة المنافسات'),k.with_value+t(' priced',' مُسعّرة'),'hero')+\n"
 " kc('SAR '+fmtM(k.open_pipeline),t('Open pipeline','المحفظة المفتوحة'),k.open_count+t(' pending',' قيد الانتظار'),'hero')+\n"
 " kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),'2024–2026')+\n")
if 'hero' in FILES['app'] and "' hero')" in FILES['app']: sys.exit('Already applied.')
ok=rep('app',OLD,NEW,'ten-second','app.js rKPI(): win rate, total tendered value, open pipeline first, marked hero (D-B4)')
if not ok:
    i=FILES['app'].find('function rKPI()'); print('ANCHOR MISMATCH. Current rKPI() in app.js:\n', FILES['app'][i:i+700]); sys.exit(1)
open(P,'w',encoding='utf-8').write(FILES['app']); write_change_table(os.path.join(HERE,'change_table_bid_appjs'),'Change table — app.js hero tiles'); print('app.js patched')
