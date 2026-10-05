"""patch_ar_full.py — full Arabic edition with the same layout and charts as the English page (04/10/2026).

Youssef: the Arabic of Saudi Government Finances 2026 and Corporate & Government News did not have the same charts,
details and layout as the English. Cause: Arabic mode hid most English sections and showed a shorter, separately written
Arabic report (#ehArView) instead.
New approach ("full mode"): every block of text on the page (headings, paragraphs, table cells, cards, KPI labels, source
cards, notes) has an Arabic twin stored in the page as <script type="application/json" id="ehArFull">. In Arabic mode
eh-ar-dashboard.js swaps each block's content for its twin in place — same sections, same tables, same charts, same order,
right-to-left — and swaps back for English. Chart labels keep using the existing Arabic dictionary. The short Arabic
report is no longer shown on pages that have a full edition.
Translations live in pipeline/ar_full/<page>.ar.json, keyed by the English block. A block whose English changes later and
has no matching Arabic stays in English, and `--check` lists such blocks (run it after every English update).
Usage:  python3 pipeline/patch_ar_full.py            embed translations into the pages that have a file in ar_full/
        python3 pipeline/patch_ar_full.py --check    report untranslated blocks (needs node + jsdom)
"""
import os, sys, json, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
A = os.path.join(ROOT, 'hub', 'eh-ar-dashboard.js')
RUNTIME = r"""
  /* ---------------- full mode (04/10/2026): Arabic twin of every text block, same layout and charts ---------------- */
  var FULL=null; try{ var fe=document.getElementById('ehArFull'); if(fe) FULL=JSON.parse(fe.textContent); }catch(e){ FULL=null; }
  var INL={B:1,I:1,SPAN:1,A:1,BR:1,SUP:1,SUB:1,SMALL:1,STRONG:1,EM:1,CODE:1,ABBR:1,U:1,MARK:1}, swapped=[];
  var normH=function(h){ return String(h).replace(/\s+/g,' ').trim(); };
  function skipEl(el){ return el.closest('#ehArView,script,style,svg,canvas,noscript,#ehLangBar'); }
  var obs=null, busy=false;
  function fullSwap(ar,root){
    if(!ar){ if(obs){ obs.disconnect(); obs=null; } swapped.forEach(function(s){ if(s.t) s.node.textContent=s.en; else { s.node.innerHTML=s.en; s.node.__ehAr=0; } }); swapped=[]; return; }
    if(!root&&swapped.length) return;
    busy=true; scan(root||document.body); busy=false;
    /* content the page draws later (expanded cards, filtered lists) is translated as it appears */
    if(!obs&&window.MutationObserver){ obs=new MutationObserver(function(ms){ if(busy)return; busy=true; ms.forEach(function(m){ [].forEach.call(m.addedNodes,function(n){ if(n.nodeType===1&&n.isConnected) scan(n.parentElement||n); }); }); busy=false; }); obs.observe(document.body,{childList:true,subtree:true}); }
  }
  function scan(root){
    var els=[root].concat([].slice.call(root.querySelectorAll('*')));
    var isLeaf=function(e){ for(var q=0;q<e.childNodes.length;q++){ var c=e.childNodes[q]; if(c.nodeType===1&&!INL[c.tagName]) return false; } return true; };
    for(var i=0;i<els.length;i++){ var el=els[i]; if(skipEl(el)) continue; if(INL[el.tagName]&&!(el.parentElement&&!isLeaf(el.parentElement))) continue;
      var kids=el.childNodes, leaf=true, j;
      for(j=0;j<kids.length;j++){ if(kids[j].nodeType===1&&!INL[kids[j].tagName]){ leaf=false; break; } }
      if(leaf){ if(el.__ehAr) continue; var k=normH(el.innerHTML); var v=FULL[k]; if(v!=null&&/[A-Za-z]{2}/.test(el.textContent)){ el.__ehAr=1; swapped.push({node:el,en:el.innerHTML}); el.innerHTML=v; } continue; }
      for(j=0;j<kids.length;j++){ var n=kids[j]; if(n.nodeType!==3||!/[A-Za-z]{3}/.test(n.textContent)) continue;
        var v2=FULL['#text:'+normH(n.textContent)]; if(v2!=null){ swapped.push({node:n,en:n.textContent,t:1}); n.textContent=' '+v2+' '; } }
    }
  }
  if(FULL){ var st=document.createElement('style'); st.textContent='body.eh-ar-full #ehArView{display:none !important}body.eh-ar-full .eh-en-only{display:revert !important}'; document.head.appendChild(st); }
"""
APPLY_OLD = "  function apply(ar){\n    prepare();"
APPLY_NEW = ("  function apply(ar){\n"
             "    if(FULL){ document.documentElement.lang=ar?'ar':'en'; document.documentElement.dir=ar?'rtl':'ltr'; document.body.classList.toggle('eh-ar-full',ar);\n"
             "      fullSwap(ar); relabelCharts(ar); if(window.EH_SHARED&&EH_SHARED.floorText) setTimeout(EH_SHARED.floorText,50); return; }\n"
             "    prepare();")

def patch_runtime():
    s = open(A, encoding='utf-8').read()
    if 'function fullSwap(' in s: return 'runtime already present'
    anchor = "  /* ---------------- one-time preparation ---------------- */"
    assert s.count(anchor) == 1 and s.count(APPLY_OLD) == 1, 'eh-ar-dashboard.js anchors not found'
    shutil.copy2(A, A + '.pre-full.bak')
    s = s.replace(anchor, RUNTIME + "\n" + anchor).replace(APPLY_OLD, APPLY_NEW)
    s = s.replace("window.EH_AR_DASH={version:'1.0.0'", "window.EH_AR_DASH={version:'2.0.0',full:!!FULL")
    open(A, 'w', encoding='utf-8').write(s); return 'runtime added'

def embed(page, mapping):
    p = os.path.join(ROOT, 'hub', page); s = open(p, encoding='utf-8').read()
    blob = '<script type="application/json" id="ehArFull">' + json.dumps(mapping, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    if 'id="ehArFull"' in s:
        s = re.sub(r'<script type="application/json" id="ehArFull">.*?</script>\n', lambda m: blob, s, count=1, flags=re.S)
    else:
        tag = '<script src="eh-ar-dashboard.js" defer></script>'
        assert s.count(tag) == 1, page + ': eh-ar-dashboard.js tag not found'
        s = s.replace(tag, blob + tag)
    open(p, 'w', encoding='utf-8').write(s)
    return len(mapping)

if __name__ == '__main__':
    if '--check' in sys.argv:
        for f in sorted(x for x in os.listdir(os.path.join(HERE, 'ar_full')) if x.endswith('.ar.json')):
            page = f.replace('.ar.json', '.html'); m = json.load(open(os.path.join(HERE, 'ar_full', f), encoding='utf-8'))
            out = subprocess.run(['node', os.path.join(HERE, 'ar_full', 'blocks.js'), os.path.join(ROOT, 'hub', page)], capture_output=True, text=True)
            blocks = json.loads(out.stdout or '[]'); miss = [b for b in blocks if b not in m and not re.fullmatch(r'[A-Z]{2,3}|EN', re.sub('<[^>]+>', '', b).strip())]
            print(f'{page}: {len(blocks)} blocks, {len(miss)} without Arabic'); [print('   ', b[:120]) for b in miss[:40]]
        sys.exit(0)
    print(patch_runtime())
    for f in sorted(os.listdir(os.path.join(HERE, 'ar_full'))):
        if not f.endswith('.ar.json'): continue
        n = embed(f.replace('.ar.json', '.html'), json.load(open(os.path.join(HERE, 'ar_full', f), encoding='utf-8')))
        print(f'{f}: {n} Arabic blocks embedded')
