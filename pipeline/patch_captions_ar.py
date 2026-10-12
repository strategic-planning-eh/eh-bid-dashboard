"""patch_captions_ar.py — two small text fixes found while building the Arabic Clients page (12 Oct 2026).

1. Clients & Revenue → Executive → "Client Depth vs Value": the caption under the chart said the bottom-right corner
   holds "big spenders who buy only one or two services". On this chart right = many jobs and up = more money, so big
   spenders with only one or two jobs sit top-LEFT ("Concentrated bets"), and bottom-right is many small jobs
   ("Transactional volume"). The English and Arabic captions now describe the corners correctly, matching the legend
   above the chart.
2. Stakeholder Map → the note "Showing companies that bid against EH only…" was written once, about a quarter of a
   second after the page opened — before the hub had told the page its language — so in Arabic it stayed in English.
   It now rewrites itself whenever the page language changes (both texts already existed; neither is changed).

Exact-string edits; stops if an anchor is missing. The Stakeholder Map keeps its mixed line endings byte-for-byte
(read and written without newline translation) and its data blocks are checked unchanged.

Run once:  python3 pipeline/patch_captions_ar.py
"""
import os, sys, json, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
BUB = os.path.join(HERE, '..', 'hub', 'EH_Client_Bubble_Map_CURRENT.html')
MAP = os.path.join(HERE, '..', 'hub', 'EH_Stakeholder_Map_CURRENT.html')
rd = lambda p: open(p, encoding='utf-8', newline='').read()
if 'ehT1Note' in rd(MAP):
    sys.exit('Already applied — nothing to do.')
changes, fails = [], []
def rep(text, old, new, note):
    n = text.count(old)
    if n != 1: fails.append(f'{note}: anchor found {n} times'); return text
    changes.append(note); return text.replace(old, new)

# ---- 1. bubble map caption (English constant and the Arabic dictionary, which is stored JSON-escaped)
OLD_EN = "Top right is the ideal — clients who buy many services and spend a lot; bottom right are big spenders who buy only one or two services and could buy more."
NEW_EN = ("Top right is the ideal — clients who give EH many jobs and spend a lot; top left are big spenders who give EH "
          "only one or two jobs and could buy more; bottom right give EH many small jobs.")
OLD_AR = "أعلى اليمين هو الأفضل — عملاء يشترون خدمات كثيرة وينفقون كثيراً؛ وأسفل اليمين عملاء ينفقون كثيراً لكنهم يشترون خدمة أو خدمتين فقط ويمكنهم شراء المزيد."
NEW_AR = ("أعلى اليمين هو الأفضل — عملاء يمنحون آفاق البيئة أعمالاً كثيرة وينفقون كثيراً؛ وأعلى اليسار عملاء ينفقون كثيراً "
          "لكنهم يمنحونها عملاً أو عملين فقط ويمكنهم شراء المزيد؛ وأسفل اليمين عملاء يمنحونها أعمالاً صغيرة كثيرة.")
b = rd(BUB)
b = rep(b, OLD_EN, NEW_EN, 'Clients: depth-vs-value caption (English) names the right corners')
esc = lambda s: json.dumps(s)[1:-1]          # how the Arabic dictionary stores text (\\uXXXX)
if esc(OLD_AR) in b: b = rep(b, esc(OLD_AR), esc(NEW_AR), 'Clients: depth-vs-value caption (Arabic) names the right corners')
else:                b = rep(b, OLD_AR, NEW_AR, 'Clients: depth-vs-value caption (Arabic) names the right corners')

# ---- 2. stakeholder note follows the language
m = rd(MAP)
blocks_before = re.findall(r'<script id="(?:DATA|LIC|BANALYTICS)"[^>]*>.*?</script>', m, re.S)
i = m.find("n.innerHTML=(typeof LNG!=='undefined'&&LNG==='ar')?")
j = m.find("mv.appendChild(n);", i)
if i < 0 or j < 0:
    fails.append('Stakeholder note: anchor not found')
else:
    expr = m[i + len("n.innerHTML="):j].rstrip(';')
    new = ("window.ehT1Note=function(){return " + expr + ";};n.innerHTML=ehT1Note();mv.appendChild(n);"
           "try{new MutationObserver(function(){var e=document.getElementById('tier1Note');if(e)e.innerHTML=ehT1Note();})"
           ".observe(document.documentElement,{attributes:true,attributeFilter:['lang']});}catch(e){}")
    m = m[:i] + new + m[j + len("mv.appendChild(n);"):]
    changes.append('Stakeholder Map: bid-against-EH note rewrites itself on language change')
if re.findall(r'<script id="(?:DATA|LIC|BANALYTICS)"[^>]*>.*?</script>', m, re.S) != blocks_before:
    fails.append('Stakeholder Map: a data block changed — refusing to write')

if fails:
    for f in fails: print('FAILED:', f)
    sys.exit(1)
open(BUB, 'w', encoding='utf-8', newline='').write(b)
open(MAP, 'w', encoding='utf-8', newline='').write(m)
stem = os.path.join(HERE, 'change_table_captions_ar')
json.dump({'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'title': 'Caption and note fixes', 'failures': [], 'changes': changes},
          open(stem + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(stem + '.md', 'w', encoding='utf-8').write('# Caption and note fixes\n\n' + '\n'.join('- ' + c for c in changes) + '\n')
print('patched:', '; '.join(changes))
