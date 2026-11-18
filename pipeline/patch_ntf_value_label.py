#!/usr/bin/env python3
"""18 Nov 2026 — "Since your last visit" strip: the SAR figure says how many of the new tenders it covers (Youssef).
Before: "3 new tender(s) (SAR 109,000)" read as if all three were worth SAR 109,000, when only one had a value.
After:  "3 new tenders (1 with a value: SAR 109,000 · 2 with no value yet)"; "(SAR x in total)" when all have a value;
        "(no value recorded yet)" when none has. A price under SAR 100 is a per-unit rate and is not added to the total.
Edits pipeline/app.js only (the Bid & Tender app is rebuilt every pipeline run). Run once."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table
A = os.path.join(HERE, 'app.js'); K = 'app.js'; load(A, K)
if 'function ntfNewLabel(' in FILES[K]: sys.exit('Already applied — nothing to do.')
OLD = """   const val=BA.bidlist.filter(b=>NTF.nw.has(b.year+'-'+b.sn)).reduce((a,b)=>a+(b.value||0),0);
   parts.push('<a style="'+lk+'" onclick="jumpTo(\\'tenders\\',\\'nw\\')">'+NTF.nw.size+t(' new tender(s)',' منافسة/منافسات جديدة')+(val?' ('+fmtSAR(val)+')':'')+'</a>');"""
NEW = """   parts.push('<a style="'+lk+'" onclick="jumpTo(\\'tenders\\',\\'nw\\')">'+ntfNewLabel()+'</a>');"""
FN = """function ntfNewLabel(){
 /* 18 Nov 2026: say how many of the new tenders the SAR figure covers; a price under SAR 100 is a per-unit rate, not a total */
 var n=NTF.nw.size, rows=BA.bidlist.filter(function(b){return NTF.nw.has(b.year+'-'+b.sn);});
 var withV=rows.filter(function(b){return (b.value||0)>=100;}), val=withV.reduce(function(a,b){return a+b.value;},0), k=withV.length, z=n-k;
 var head=n===1?t('1 new tender','منافسة جديدة واحدة'):n+t(' new tenders',' منافسات جديدة');
 if(!k) return head+t(' (no value recorded yet)',' (لم تُسجَّل قيمة بعد)');
 if(n===1) return head+' ('+fmtSAR(val)+')';
 if(!z) return head+' ('+fmtSAR(val)+t(' in total',' إجمالاً')+')';
 return head+' ('+k+t(' with a value: ',' بقيمة مسجّلة: ')+fmtSAR(val)+' \\u00b7 '+z+t(' with no value yet',' بلا قيمة بعد')+')';
}
function rNtf(){"""
ok = [rep(K, OLD, NEW, 'ntf-value', 'Strip uses the new label'),
      rep(K, 'function rNtf(){', FN, 'ntf-value', 'ntfNewLabel(): count of valued tenders beside the SAR figure')]
if not all(ok): sys.exit('Patch failed — nothing written.')
with open(A, 'w', encoding='utf-8') as f: f.write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_ntf_value_label'), 'New-tender strip value label')
print('done')
