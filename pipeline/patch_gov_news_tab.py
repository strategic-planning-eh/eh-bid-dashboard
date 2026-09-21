"""patch_gov_news_tab.py — wires the new Government news tab into the hub and moves What's New to Sunday-start weeks.

New files shipped alongside (not patched, just added):
  pipeline/gov_news_sources.json   bodies + sources followed
  pipeline/fetch_gov_news.py       weekly collector
  pipeline/gov_news.seed.json      honest empty feed shown until the first Sunday run
  hub/government_news.html         the tab page (reads gov_news.json at runtime)
  .github/workflows/gov-news.yml   Sunday 06:00 KSA collector → `gov-news` artefact

Edits made here:
  hub/EH_Hub.html                       "Government" sub-tab after "Corporate & Government News" (button, skeleton, iframe, nGo list)
  pipeline/build_changelog.py           What's New weeks run Sunday–Saturday (a Sunday release heads its own week)
  .github/workflows/update-dashboard.yml  copies the tab page, restores the gov-news artefact, publishes site/gov_news.json
                                          (fallback: the previously published copy, then the seed)
Run once: python3 pipeline/patch_gov_news_tab.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); C = os.path.join(HERE, 'build_changelog.py'); W = os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml')
if 'data-n="gov"' in open(H, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (H, C, W): shutil.copy2(p, p + '.pre-govnews.bak'); load(p, os.path.basename(p))

# ---- hub: sub-tab
rep('EH_Hub.html',
    '<button class="nsub" data-n="corp"><span class="tl" data-en="Corporate &amp; Government News" data-ar="أخبار الشركات والحكومة">Corporate &amp; Government News</span></button>',
    '<button class="nsub" data-n="corp"><span class="tl" data-en="Corporate &amp; Government News" data-ar="أخبار الشركات والحكومة">Corporate &amp; Government News</span></button>\n'
    '      <button class="nsub" data-n="gov" title="Weekly official releases from MEWA, MWAN, NCEC, the Royal Commissions and the Ministry of Municipalities · إعلانات الجهات التنظيمية الأسبوعية"><span class="tl" data-en="Government" data-ar="الحكومة">Government</span><span class="newb" aria-label="New">New</span></button>',
    'gov-tab', 'Government sub-tab button after the corporate & government briefing')
rep('EH_Hub.html',
    '<iframe id="f-corp" title="Corporate and government news" data-src="eh_news_intelligence.html" loading="lazy" style="display:none"></iframe>',
    '<iframe id="f-corp" title="Corporate and government news" data-src="eh_news_intelligence.html" loading="lazy" style="display:none"></iframe>\n'
    '      <div class="skel" id="sk-gov"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading Government news…" data-ar="جارٍ تحميل أخبار الجهات الحكومية…">Loading Government news…</span></div></div>\n'
    '      <iframe id="f-gov" title="Government news — regulators EH answers to, refreshed weekly" data-src="government_news.html" loading="lazy" style="display:none"></iframe>',
    'gov-tab', 'Skeleton + lazy iframe for the tab page')
rep('EH_Hub.html', "['v2030','fiscal','corp','pif','strat','ef2025']", "['v2030','fiscal','corp','gov','pif','strat','ef2025']", 'gov-tab', 'Tab switcher knows the new frame')

# ---- What's New: Sunday–Saturday weeks. Label stays YYYY-Www: the ISO week of the Monday inside the week, so a
#      Monday–Saturday release keeps the label it had; only Sunday releases move forward to the week they open.
rep('build_changelog.py',
    "def iso_week(d):\n    y, w, _ = d.isocalendar(); mon = d - dt.timedelta(days=d.weekday())\n    return f'{y}-W{w:02d}', mon.isoformat(), (mon + dt.timedelta(days=6)).isoformat()",
    "def iso_week(d):\n    \"\"\"Sunday–Saturday week (Saudi working week). Label = ISO week of the Monday inside it, so Mon–Sat dates keep their\n"
    "    old label and a Sunday heads the week that follows it.\"\"\"\n"
    "    sun = d - dt.timedelta(days=(d.weekday() + 1) % 7); mon = sun + dt.timedelta(days=1)\n"
    "    y, w, _ = mon.isocalendar()\n"
    "    return f'{y}-W{w:02d}', sun.isoformat(), (sun + dt.timedelta(days=6)).isoformat()",
    'sunday-week', "What's New weeks start on Sunday")

# ---- publisher: copy the page, restore the weekly artefact, publish the feed
rep('update-dashboard.yml',
    "          cp hub/environment_fund_2025.html site/ 2>/dev/null || true\n",
    "          cp hub/environment_fund_2025.html site/ 2>/dev/null || true\n          cp hub/government_news.html site/ 2>/dev/null || true\n",
    'gov-feed', 'Tab page is published')
rep('update-dashboard.yml',
    "      # ---------- What's New: previous dataset snapshot (artefact of the last successful run) ----------\n",
    "      # ---------- Government news: weekly feed collected by gov-news.yml (Sunday 06:00 KSA) ----------\n"
    "      - name: Restore the weekly Government news feed\n"
    "        uses: dawidd6/action-download-artifact@v6\n"
    "        continue-on-error: true\n"
    "        with:\n"
    "          workflow: gov-news.yml\n"
    "          workflow_conclusion: success\n"
    "          name: gov-news\n"
    "          path: pipeline/gov_news_in\n"
    "          search_artifacts: true\n\n"
    "      - name: Publish the feed (artefact → last published copy → seed)\n"
    "        run: |\n"
    "          if [ -f pipeline/gov_news_in/gov_news.json ]; then cp pipeline/gov_news_in/gov_news.json site/gov_news.json; echo \"gov news: weekly artefact\";\n"
    "          elif curl -fsSL \"$SITE_URL/gov_news.json\" -o site/gov_news.json; then echo \"gov news: kept the previously published feed\";\n"
    "          else cp pipeline/gov_news.seed.json site/gov_news.json; echo \"gov news: seed (no run yet)\"; fi\n"
    "        env:\n"
    "          SITE_URL: https://strategic-planning-eh.github.io/eh-bid-dashboard\n\n"
    "      # ---------- What's New: previous dataset snapshot (artefact of the last successful run) ----------\n",
    'gov-feed', 'Feed hand-off from the weekly workflow into the published site')

for p in (H, C, W): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_gov_news_tab'), 'Change table — Government news tab + Sunday weeks')
print('edits:', 6 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
