"""patch_regulatory_news.py — 22 Sep 2026.

1. The tab is renamed "Regulatory news" (EN) / "الأخبار التنظيمية" (AR) everywhere it is visible: hub button, loading
   skeleton, iframe title, page title and heading, and the two What's New lines that name it.
2. Why only NCEC had items: SPA search ranks by relevance, not date, so the stories it returned for MWAN, RCMC and RCU
   were older than the 90-day window and were dropped — correct per the rule, useless for the reader. New rule: the
   window still governs, but every body keeps at least its five most recent stories on file regardless of age, and the
   page marks anything older than the window as "archive". SPA queries also fetch deeper (30 instead of 15) and are
   ordered by SPA's own story number, which rises over time, so the newest stories come first.

Run once: python3 pipeline/patch_regulatory_news.py
"""
import os, sys, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); G = os.path.join(ROOT, 'hub', 'government_news.html')
F = os.path.join(HERE, 'fetch_gov_news.py'); C = os.path.join(HERE, 'CHANGES.md'); S = os.path.join(HERE, 'gov_news_sources.json')
if 'Regulatory news' in open(H, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (H, G, F, C): shutil.copy2(p, p + '.pre-reg.bak'); load(p, os.path.basename(p))

# ---- 1. rename
rep('EH_Hub.html', '<span class="tl" data-en="Government" data-ar="الحكومة">Government</span>',
    '<span class="tl" data-en="Regulatory news" data-ar="الأخبار التنظيمية">Regulatory news</span>', 'rename', 'Hub tab label')
rep('EH_Hub.html', 'data-en="Loading Government news…" data-ar="جارٍ تحميل أخبار الجهات الحكومية…">Loading Government news…',
    'data-en="Loading Regulatory news…" data-ar="جارٍ تحميل الأخبار التنظيمية…">Loading Regulatory news…', 'rename', 'Skeleton text')
rep('EH_Hub.html', 'title="Government news — regulators EH answers to, refreshed weekly"',
    'title="Regulatory news — regulators EH answers to, refreshed weekly"', 'rename', 'Iframe title')
rep('government_news.html', '<title>Government news — regulators EH answers to, refreshed weekly</title>',
    '<title>Regulatory news — regulators EH answers to, refreshed weekly</title>', 'rename', 'Page title')
rep('government_news.html', "$('title').textContent=L('Government — what the regulators announced','الحكومة — ما أعلنته الجهات التنظيمية');",
    "$('title').textContent=L('Regulatory news — what the regulators announced','الأخبار التنظيمية — ما أعلنته الجهات التنظيمية');", 'rename', 'Page heading')
rep('CHANGES.md', 'news | major | Government | New tab under News & Intelligence:', 'news | major | Regulatory news | New tab under News & Intelligence:', 'rename', "What's New")
rep('CHANGES.md', 'news | minor | Government | Fixed: oversized amber blocks', 'news | minor | Regulatory news | Fixed: oversized amber blocks', 'rename', "What's New")
rep('CHANGES.md', "## 2026-W39\n", "## 2026-W39\nnews | minor | Regulatory news | Renamed from \"Government\". Each body now keeps its five most recent stories on file even when they are older than 90 days (SPA search ranks by relevance, so for some bodies that is all it returns); such stories are marked \"archive\" and appear under \"Everything on file\". | أُعيدت التسمية من «الحكومة». تحتفظ كل جهة الآن بأحدث خمس قصص لها حتى وإن كانت أقدم من 90 يوماً (بحث واس يرتّب بالصلة لا بالتاريخ، فهذا كل ما يعيده لبعض الجهات)؛ تُعلَّم هذه القصص «أرشيف» وتظهر تحت «كل السجل».\n", 'rename', "What's New line for the rename and the archive rule")

# ---- 2. page: archive chip + legend wording
rep('government_news.html', "${(it.tags||[]).map(t=>`<span class=\"chip tag\">${esc(L(...(TAGL[t]||[t,t])))}</span>`).join('')}</div></div></div>`).join('')",
    "${(it.tags||[]).map(t=>`<span class=\"chip tag\">${esc(L(...(TAGL[t]||[t,t])))}</span>`).join('')}${(()=>{const n=daysAgo(it.date||it.first_seen);return n!=null&&n>FEED.retention_days?`<span class=\"chip lang\" title=\"${esc(L('Kept because it is one of this body\\'s newest stories on file','محفوظة لأنها من أحدث قصص هذه الجهة على السجل'))}\">${L('archive','أرشيف')}</span>`:'';})()}</div></div></div>`).join('')",
    'archive', 'Stories older than the window carry an archive chip')
rep('government_news.html', "${L('Green: items on file from the last run. Amber: sources reachable but nothing within the 90-day window. Red: a fetch failed. Grey: not fetched yet.','أخضر: عناصر على السجل من آخر تشغيل. كهرماني: المصادر متاحة لكن لا شيء ضمن نافذة 90 يوماً. أحمر: فشل جلب. رمادي: لم يُجلب بعد.')}",
    "${L('Green: items on file. Amber: sources reachable but nothing found. Red: a fetch failed. Grey: not fetched yet. Stories older than 90 days are kept only as each body\\'s newest five and marked \"archive\".','أخضر: عناصر على السجل. كهرماني: المصادر متاحة دون عناصر. أحمر: فشل جلب. رمادي: لم يُجلب بعد. تُحفظ القصص الأقدم من 90 يوماً كأحدث خمس لكل جهة فقط وتُعلَّم «أرشيف».')}",
    'archive', 'Legend explains the archive rule')

# ---- 3. fetcher: retention keeps each body's newest five; SPA fetches deeper and newest-first
rep('fetch_gov_news.py',
    "    kept, by_key = [], {}\n    for it in items.values():\n        d = it.get('date') or it.get('first_seen')\n        if d and d < cutoff: continue\n        key = (it['body'], norm_title(it['title']))",
    "    KEEP_MIN = cfg.get('keep_min_per_body', 5)\n    def story_no(u):\n        m = re.search(r'/N(\\d{5,})', u or ''); return int(m.group(1)) if m else 0\n"
    "    # SPA search ranks by relevance, not date: a body may only ever surface old stories. Each body therefore keeps its\n"
    "    # newest KEEP_MIN stories on file regardless of age; the page marks anything outside the window as archive.\n"
    "    by_body = {}\n    for it in items.values(): by_body.setdefault(it['body'], []).append(it)\n    protected = set()\n"
    "    for bid, lst in by_body.items():\n        lst.sort(key=lambda x: (x.get('date') or '', story_no(x.get('url')), x['first_seen']), reverse=True)\n"
    "        protected.update(x['id'] for x in lst[:KEEP_MIN])\n"
    "    kept, by_key = [], {}\n    for it in items.values():\n        d = it.get('date') or it.get('first_seen')\n        if d and d < cutoff and it['id'] not in protected: continue\n        key = (it['body'], norm_title(it['title']))",
    'archive', 'Retention keeps the newest five per body')
rep('fetch_gov_news.py',
    "        if out:\n            dbg['url'] = url; dbg['sample'] = [(o['url'], o['title'][:60]) for o in out[:8]]\n            return out",
    "        if out:\n            out.sort(key=lambda o: int(re.search(r'/N(\\d+)', o['url']).group(1)) if re.search(r'/N(\\d+)', o['url']) else 0, reverse=True)  # SPA story numbers rise over time\n"
    "            dbg['url'] = url; dbg['sample'] = [(o['url'], o['title'][:60]) for o in out[:8]]\n            return out",
    'archive', 'SPA results ordered newest-first')

for p in (H, G, F, C): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
cfg = json.load(open(S, encoding='utf-8')); cfg['spa']['max_per_query'] = 30; cfg['keep_min_per_body'] = 5
json.dump(cfg, open(S, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
write_change_table(os.path.join(HERE, 'change_table_regulatory_news'), 'Change table — Regulatory news rename + archive rule')
print('edits:', 13 - len(FAILURES), 'of 13, failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
