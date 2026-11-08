"""patch_gov_blocked.py — Regulatory news tab: show a source that was refused by an access wall as "blocked",
not as "reachable, nothing found" (8 Nov 2026).

Background: on 8 Nov 2026 every Saudi Press Agency (SPA) search came back as a Cloudflare "Attention Required"
page for the GitHub Actions runner, and the tab reported it as "Reachable, nothing found" for 11 bodies.
fetch_gov_news.py now records that case as status `blocked`; this patch teaches the page the new status:
  • a label for it (EN/AR), a red dot, and body-level state "blocked" when every source of a body is blocked
  • the header problem count includes blocked sources

Run once:  python3 pipeline/patch_gov_blocked.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_files, write_change_table

P = os.path.join(HERE, '..', 'hub', 'government_news.html')
if "blocked:['" in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'gov')

rep('gov',
    "error:['Fetch failed','فشل الجلب'],",
    "error:['Fetch failed','فشل الجلب'],blocked:['Refused by the site (access wall) — not a result','رفضه الموقع (حاجز وصول) — ليست نتيجة'],",
    'status', 'label for the new blocked status')

rep('gov',
    ".dot.st-error{background:var(--red)}.dot.st-skipped",
    ".dot.st-error,.dot.st-blocked{background:var(--red)}.dot.st-skipped",
    'status', 'red dot for blocked (base CSS)')

rep('gov',
    "body .dot.st-error{background:var(--eh-bad);border-radius:1px;transform:rotate(45deg)}",
    "body .dot.st-error{background:var(--eh-bad);border-radius:1px;transform:rotate(45deg)}body .dot.st-blocked{background:var(--eh-bad);border-radius:1px}",
    'status', 'red dot for blocked (EH skin)')

rep('gov',
    " if(b.robots_disallow&&ss.every(s=>s.type==='spa'&&s.status!=='ok'))return ss.some(s=>s.status==='error')?'error':'empty';\n if(ss.some(s=>s.status==='empty'))return 'empty';",
    " if(ss.every(s=>s.status==='blocked'))return 'blocked';\n if(b.robots_disallow&&ss.every(s=>s.type==='spa'&&s.status!=='ok'))return ss.some(s=>s.status==='error')?'error':ss.some(s=>s.status==='blocked')?'blocked':'empty';\n if(ss.some(s=>s.status==='empty'))return 'empty';",
    'status', 'body state: blocked when its sources were refused')

rep('gov',
    "problems=bodies.reduce((n,b)=>n+(b.sources||[]).filter(s=>s.status==='error').length,0);",
    "problems=bodies.reduce((n,b)=>n+(b.sources||[]).filter(s=>s.status==='error'||s.status==='blocked').length,0);",
    'status', 'problem count includes blocked sources')

if FAILURES:
    print('FAILURES', FAILURES); sys.exit(1)
write_files(os.path.join(HERE, '..', 'hub'))
write_change_table(os.path.join(HERE, 'change_table_gov_blocked'), 'Regulatory news — blocked status (8 Nov 2026)')
print('applied')
