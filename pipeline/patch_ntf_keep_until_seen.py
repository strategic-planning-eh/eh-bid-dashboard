#!/usr/bin/env python3
"""18 Nov 2026 — "Since your last visit" strip keeps its items until the reader marks them as seen (Youssef).
Before: every page load saved a fresh snapshot, so a new tender was announced exactly once — any reload, a second tab,
        or the page reopening after an hourly rebuild silently marked it as seen and it vanished from the strip.
After:  the snapshot only moves forward when the reader presses "Mark as seen" on the strip. Until then new tenders,
        decisions and updates stay listed, on every load.
One-off recovery: a browser still holding an old-style snapshot gets tenders launched in the last 7 days flagged as new
        again, because the old behaviour may have swallowed them.
Edits pipeline/app.js only. Run once."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table
A = os.path.join(HERE, 'app.js'); K = 'app.js'; load(A, K)
if 'function ntfAck(' in FILES[K]: sys.exit('Already applied — nothing to do.')
OLD_SAVE = """      else if(old.p[k]!==ph[k]) NTF.px.add(k);
    });
  }
  localStorage.setItem('ehb.snap',JSON.stringify({t:th,p:ph,when:new Date().toISOString().slice(0,10)}));"""
NEW_SAVE = """      else if(old.p[k]!==ph[k]) NTF.px.add(k);
    });
    if(!old.v){ /* old-style snapshot (was overwritten on every load): recover tenders launched in the last 7 days, once */
      const cut=new Date(Date.now()-7*864e5).toISOString().slice(0,10);
      const base={t:Object.assign({},old.t||{}),p:Object.assign({},old.p||{}),when:cut,v:2};
      BA.bidlist.forEach(b=>{const k=key(b);
        if(String(b.date||'').slice(0,10)>=cut&&base.t.hasOwnProperty(k)){delete base.t[k];delete base.p[k];NTF.nw.add(k);NTF.upd.delete(k);NTF.dec.delete(k);NTF.px.delete(k);}});
      NTF.when=cut;
      localStorage.setItem('ehb.snap',JSON.stringify(base));
    }
  } else {
    localStorage.setItem('ehb.snap',JSON.stringify({t:th,p:ph,when:new Date().toISOString().slice(0,10),v:2}));
  }
  NTF.cur={t:th,p:ph};  /* the snapshot only moves forward in ntfAck() — "Mark as seen" */"""
OLD_BTN = """  '<button onclick="this.parentElement.style.display=\\'none\\'" style="border:0;background:none;cursor:pointer;font-weight:800;color:#8A7A44;margin-inline-start:auto">\\u2715</button>';
}"""
NEW_BTN = """  '<button onclick="ntfAck()" title="'+t('Clears this strip. Until you press it, these items stay listed every time you open the page.','يمسح هذا الشريط. تبقى هذه العناصر ظاهرة في كل مرة تفتح الصفحة حتى تضغط عليه.')+'" style="border:1px solid #D9C88F;background:#fff;border-radius:7px;padding:3px 10px;cursor:pointer;font-weight:700;color:#5C4A14;margin-inline-start:auto">\\u2713 '+t('Mark as seen','تمّت المشاهدة')+'</button>';
}
function ntfAck(){
 /* 18 Nov 2026: the only place the "last visit" snapshot moves forward */
 try{ if(NTF.cur) localStorage.setItem('ehb.snap',JSON.stringify({t:NTF.cur.t,p:NTF.cur.p,when:new Date().toISOString().slice(0,10),v:2})); }catch(e){}
 NTF.nw.clear();NTF.dec.clear();NTF.upd.clear();NTF.px.clear();
 var el=document.getElementById('ntfbar'); if(el) el.style.display='none';
 try{ rNav(); if(typeof TF!=='undefined'&&TF.only){TF.only=null;} if(typeof renderTenders==='function') renderTenders(); }catch(e){}
}"""
ok = [rep(K, OLD_SAVE, NEW_SAVE, 'ntf-keep', 'Snapshot no longer overwritten on every load; one-off 7-day recovery'),
      rep(K, OLD_BTN, NEW_BTN, 'ntf-keep', '"Mark as seen" button + ntfAck()')]
if not all(ok): sys.exit('Patch failed — nothing written.')
with open(A, 'w', encoding='utf-8') as f: f.write(FILES[K])
write_change_table(os.path.join(HERE, 'change_table_ntf_keep_until_seen'), 'Notification strip keeps items until marked as seen')
print('done')
