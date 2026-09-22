"""patch_hub_passphrase.py — three decisions from 22 Sep 2026, applied together.

1. Passphrase protection (replaces the CONFIDENTIAL banner)
   New file pipeline/encrypt_site.py seals every HTML/JSON in site/ as the last publish step. Edits here:
     .github/workflows/update-dashboard.yml   seal step before "Package the page"; the two curl-restores of published
                                              JSON (changelog, gov news) are decrypted with the same secret
     .github/workflows/gov-news.yml           the previous feed restored from the site is decrypted too
     requirements.txt                         cryptography
     hub/EH_Hub.html                          banner → small "Protected · Lock this device" control; What's New footer
                                              loses "confidential" line
2. "New" badges that never clear
     hub/EH_Hub.html   badges carry data-new-until (auto-retire) and the seen state is remembered in localStorage
3. Government tab UI
     hub/government_news.html   status dot classes renamed (they collided with the .empty box style), a body whose
                                only finds were older than the window shows amber with the reason, KPI tiles follow the
                                body filter
Run once: python3 pipeline/patch_hub_passphrase.py

Follow-up (22 Sep 2026, after the first sealed publish broke the hub layout): delivery moved to a service worker
(eh-sw.js written by encrypt_site.py) so pages load untouched; the lock control became ehLock(), which clears the key
from the worker store and from session/local storage. Those two edits were applied directly to hub/EH_Hub.html.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); G = os.path.join(ROOT, 'hub', 'government_news.html')
W = os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml'); WG = os.path.join(ROOT, '.github', 'workflows', 'gov-news.yml')
R = os.path.join(ROOT, 'requirements.txt')
if 'ehHubLock' in open(H, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (H, G, W, WG, R): shutil.copy2(p, p + '.pre-pass.bak'); load(p, os.path.basename(p))
N = 0
def R_(f, a, b, t, w, **k):
    global N; N += 1; rep(f, a, b, t, w, **k)

# ---------------------------------------------------------------- 1. hub: banner → lock control
R_('EH_Hub.html',
   '<span dir="ltr">CONFIDENTIAL — authorised EH management access only</span><span class="dsep"> · </span><span dir="rtl" lang="ar">سرّي — الوصول مصرّح به لإدارة آفاق البيئة فقط</span></span>',
   '<span dir="ltr">Protected</span><span class="dsep"> · </span><span dir="rtl" lang="ar">محمي</span>'
   '<a href="#" class="lockbtn" onclick="if(window.ehHubLock){ehHubLock();}return false;" title="Sign out on this device — the passphrase will be asked again · تسجيل الخروج من هذا الجهاز">'
   '<span dir="ltr">Lock this device</span><span class="dsep"> · </span><span dir="rtl" lang="ar">قفل هذا الجهاز</span></a></span>',
   'passphrase', 'CONFIDENTIAL banner replaced by a Protected note and a lock control')
R_('EH_Hub.html', '.nsub.on .newb,.nsub.seen .newb{display:none}',
   '.nsub.on .newb,.nsub.seen .newb{display:none} .conf .lockbtn{margin-inline-start:10px;color:inherit;text-decoration:underline;text-underline-offset:2px;opacity:.85} .conf .lockbtn:hover{opacity:1}',
   'passphrase', 'Lock control style')
R_('EH_Hub.html',
   "</span> \\u00b7 '+L('This log is confidential, like the rest of the hub.','هذا السجل سرّي كباقي المنصة.')+'</div>';",
   "</span></div>';",
   'passphrase', "What's New footer no longer says the log is confidential")

# ---------------------------------------------------------------- 2. hub: New badges remember and expire
R_('EH_Hub.html',
   'data-ar="استراتيجية صندوق الاستثمارات العامة 2026–2030">PIF Strategy 2026–2030</span><span class="newb" aria-label="New">New</span>',
   'data-ar="استراتيجية صندوق الاستثمارات العامة 2026–2030">PIF Strategy 2026–2030</span><span class="newb" data-new-until="2026-10-06" aria-label="New">New</span>',
   'new-badge', 'PIF Strategy badge retires on 6 Oct')
R_('EH_Hub.html',
   'data-ar="تقرير صندوق البيئة 2025">Environment Fund 2025 Report</span><span class="newb" aria-label="New">New</span>',
   'data-ar="تقرير صندوق البيئة 2025">Environment Fund 2025 Report</span><span class="newb" data-new-until="2026-10-06" aria-label="New">New</span>',
   'new-badge', 'Environment Fund badge retires on 6 Oct')
R_('EH_Hub.html',
   'data-ar="الحكومة">Government</span><span class="newb" aria-label="New">New</span>',
   'data-ar="الحكومة">Government</span><span class="newb" data-new-until="2026-10-13" aria-label="New">New</span>',
   'new-badge', 'Government badge retires on 13 Oct')
R_('EH_Hub.html',
   "document.querySelectorAll('.nsub').forEach(b=>b.addEventListener('click',()=>{nGo(b);b.classList.add('seen');}));",
   "document.querySelectorAll('.nsub').forEach(b=>b.addEventListener('click',()=>{nGo(b);b.classList.add('seen');try{localStorage.setItem('ehhub.seen.'+b.dataset.n,'1');}catch(e){}}));\n"
   "// New badges: hidden once the tab has been opened on this device, and retired automatically after data-new-until\n"
   "document.querySelectorAll('.nsub .newb').forEach(nb=>{const b=nb.closest('.nsub');let seen=false;try{seen=!!localStorage.getItem('ehhub.seen.'+b.dataset.n);}catch(e){}\n"
   "  const until=nb.dataset.newUntil;if(seen||(until&&new Date(until+'T23:59:59+03:00')<new Date()))b.classList.add('seen');});",
   'new-badge', 'Seen state kept in localStorage; badges expire on their date')

# ---------------------------------------------------------------- 3. Government tab
R_('government_news.html',
   '.dot{width:9px;height:9px;border-radius:50%;display:inline-block;background:var(--muted)}.dot.ok{background:var(--green)}.dot.empty{background:var(--amber)}.dot.error{background:var(--red)}.dot.skipped,.dot.robots{background:#9AABB5}',
   '.dot{width:9px;height:9px;border-radius:50%;display:inline-block;background:var(--muted);flex:none}.dot.st-ok{background:var(--green)}.dot.st-empty,.dot.st-stale{background:var(--amber)}.dot.st-error{background:var(--red)}.dot.st-skipped,.dot.st-robots{background:#9AABB5}',
   'gov-ui', 'Status dots use st-* classes so they no longer inherit the .empty box style')
R_('government_news.html',
   "const STL={ok:['Fetched','تم الجلب'],empty:['Reachable, nothing found','متاح، لا عناصر'],error:['Fetch failed','فشل الجلب'],skipped:['Skipped','تم التخطي'],robots:['Site blocks robots — via SPA','الموقع يمنع الروبوتات — عبر واس']};",
   "const STL={ok:['Fetched','تم الجلب'],empty:['Reachable, nothing found','متاح، لا عناصر'],stale:['Found only items older than the window','وُجدت عناصر أقدم من النافذة فقط'],error:['Fetch failed','فشل الجلب'],skipped:['Skipped','تم التخطي'],robots:['Site blocks robots — via SPA','الموقع يمنع الروبوتات — عبر واس']};",
   'gov-ui', 'Stale state label')
R_('government_news.html',
   "function bodyState(b){ // worst-case across sources, but \"ok\" if any source delivered\n const ss=b.sources||[];if(!ss.length)return 'skipped';\n if(ss.some(s=>s.status==='ok'))return 'ok';",
   "function bodyState(b,cnt){ // \"ok\" only if a source delivered AND something is on file; finds that all fell outside the window are \"stale\"\n const ss=b.sources||[];if(!ss.length)return 'skipped';\n if(ss.some(s=>s.status==='ok'))return cnt>0?'ok':'stale';",
   'gov-ui', 'A body with finds but nothing within 90 days shows amber, not green')
R_('government_news.html',
   "return `<div class=\"bd ${S.body===b.id?'on':''}\" onclick=\"S.body=S.body==='${b.id}'?'all':'${b.id}';render()\"><div class=\"n\">${esc(L(b.en,b.ar))}</div><div class=\"m\"><span class=\"dot ${b.robots_disallow&&st!=='ok'?'robots':st}\" title=\"${esc(L(...(STL[b.robots_disallow&&st!=='ok'?'robots':st]||[st,st])))}\"></span>",
   "const sk=b.robots_disallow&&(st==='skipped'||st==='error')?'robots':st;return `<div class=\"bd ${S.body===b.id?'on':''}\" onclick=\"S.body=S.body==='${b.id}'?'all':'${b.id}';render()\"><div class=\"n\">${esc(L(b.en,b.ar))}</div><div class=\"m\"><span class=\"dot st-${sk}\" title=\"${esc(L(...(STL[sk]||[sk,sk])))}\"></span>",
   'gov-ui', 'Dot markup uses the new classes')
R_('government_news.html', "const st=bodyState(b);const last=items.filter(it=>it.body===b.id).map(it=>it.date||it.first_seen).sort().pop();const cnt=items.filter(it=>it.body===b.id).length;",
   "const cnt=items.filter(it=>it.body===b.id).length;const st=bodyState(b,cnt);const last=items.filter(it=>it.body===b.id).map(it=>it.date||it.first_seen).sort().pop();",
   'gov-ui', 'Count computed before the state')
R_('government_news.html',
   "${L('Green: the last run fetched items. Amber: reachable but nothing found. Red: fetch failed. Grey: followed through SPA only because the site blocks robots.','أخضر: آخر تشغيل جلب عناصر. كهرماني: متاح دون عناصر. أحمر: فشل الجلب. رمادي: يُتابَع عبر واس فقط لأن الموقع يمنع الروبوتات.')}",
   "${L('Green: items on file from the last run. Amber: sources reachable but nothing within the 90-day window. Red: a fetch failed. Grey: not fetched yet.','أخضر: عناصر على السجل من آخر تشغيل. كهرماني: المصادر متاحة لكن لا شيء ضمن نافذة 90 يوماً. أحمر: فشل جلب. رمادي: لم يُجلب بعد.')}",
   'gov-ui', 'Legend matches the states')
R_('government_news.html',
   " const items=FEED.items||[], wk=items.filter(",
   " const all=FEED.items||[], items=S.body==='all'?all:all.filter(it=>it.body===S.body), wk=items.filter(",
   'gov-ui', 'KPI tiles follow the selected body')
R_('government_news.html',
   " const bodies=FEED.bodies||[], reporting=bodies.filter(b=>items.some(it=>it.body===b.id)).length,",
   " const bodies=FEED.bodies||[], reporting=bodies.filter(b=>all.some(it=>it.body===b.id)).length,",
   'gov-ui', 'Bodies-reporting tile stays feed-wide')
R_('government_news.html',
   "const cnt=items.filter(it=>it.body===b.id).length;const st=bodyState(b,cnt);const last=items.filter(it=>it.body===b.id).map(",
   "const cnt=all.filter(it=>it.body===b.id).length;const st=bodyState(b,cnt);const last=all.filter(it=>it.body===b.id).map(",
   'gov-ui', 'Body cards count from the whole feed, not the filtered view')
R_('government_news.html', "$('kstrip').innerHTML=[[wk.length,L('Announcements this feed week','إعلانات في أسبوع التغذية')]",
   "$('kstrip').innerHTML=[[wk.length,L('Announcements this feed week','إعلانات في أسبوع التغذية')+(S.body!=='all'?' — '+esc(bodyOf(S.body).short):'')]",
   'gov-ui', 'Tile says which body it is counting')
R_('government_news.html', "const tags=[...new Set(items.flatMap(it=>it.tags||[]))];", "const tags=[...new Set(all.flatMap(it=>it.tags||[]))];", 'gov-ui', 'Topic list built from the whole feed')

# ---------------------------------------------------------------- workflows + requirements
R_('requirements.txt', "google-auth>=2.23\n", "google-auth>=2.23\ncryptography>=42\n", 'passphrase', 'cryptography for encrypt_site.py')
R_('update-dashboard.yml',
   "          curl -fsSL \"$SITE_URL/changelog.json\" -o pipeline/changelog_prev.json && cp pipeline/changelog_prev.json site/changelog.json || cp pipeline/changelog.seed.json site/changelog.json 2>/dev/null || echo \"no published changelog yet\"\n        env:\n          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n",
   "          if curl -fsSL \"$SITE_URL/changelog.json\" -o pipeline/changelog_prev.json && python pipeline/encrypt_site.py --decrypt pipeline/changelog_prev.json; then cp pipeline/changelog_prev.json site/changelog.json;\n"
   "          else cp pipeline/changelog.seed.json site/changelog.json 2>/dev/null || echo \"no published changelog yet\"; fi\n        env:\n          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n          HUB_PASSPHRASE: ${{ secrets.HUB_PASSPHRASE }}\n",
   'passphrase', 'Published changelog is decrypted before reuse')
R_('update-dashboard.yml',
   "          elif curl -fsSL \"$SITE_URL/gov_news.json\" -o site/gov_news.json; then echo \"gov news: kept the previously published feed\";\n"
   "          else cp pipeline/gov_news.seed.json site/gov_news.json; echo \"gov news: seed (no run yet)\"; fi\n        env:\n          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n",
   "          elif curl -fsSL \"$SITE_URL/gov_news.json\" -o site/gov_news.json && python pipeline/encrypt_site.py --decrypt site/gov_news.json; then echo \"gov news: kept the previously published feed\";\n"
   "          else cp pipeline/gov_news.seed.json site/gov_news.json; echo \"gov news: seed (no run yet)\"; fi\n        env:\n          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n          HUB_PASSPHRASE: ${{ secrets.HUB_PASSPHRASE }}\n",
   'passphrase', 'Published gov feed is decrypted before reuse')
R_('update-dashboard.yml',
   "      - name: Package the page\n        uses: actions/upload-pages-artifact@v3\n",
   "      # ---------- Passphrase protection: every page and data file is sealed; the build FAILS if the secret is missing ----------\n"
   "      - name: Seal the site with the hub passphrase\n"
   "        env:\n          HUB_PASSPHRASE: ${{ secrets.HUB_PASSPHRASE }}\n"
   "        run: python pipeline/encrypt_site.py --site site\n\n"
   "      - name: Package the page\n        uses: actions/upload-pages-artifact@v3\n",
   'passphrase', 'Seal step runs after the visual check, right before packaging')
R_('gov-news.yml',
   "          pip install -q requests beautifulsoup4 playwright\n",
   "          pip install -q requests beautifulsoup4 playwright cryptography\n",
   'passphrase', 'cryptography for the decrypt helper')
R_('gov-news.yml',
   "          curl -fsSL \"$SITE_URL/gov_news.json\" -o pipeline/gov_news_prev.json || echo \"no published feed yet — starting from the seed\"\n        env:\n          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n",
   "          if curl -fsSL \"$SITE_URL/gov_news.json\" -o pipeline/gov_news_prev.json; then python pipeline/encrypt_site.py --decrypt pipeline/gov_news_prev.json || rm -f pipeline/gov_news_prev.json; else echo \"no published feed yet — starting from the seed\"; fi\n        env:\n          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n          HUB_PASSPHRASE: ${{ secrets.HUB_PASSPHRASE }}\n",
   'passphrase', 'Previous feed is decrypted before merging')

for p in (H, G, W, WG, R): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_hub_passphrase'), 'Change table — passphrase, banner, New badges, Government tab UI')
print('edits:', N - len(FAILURES), 'of', N, 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
