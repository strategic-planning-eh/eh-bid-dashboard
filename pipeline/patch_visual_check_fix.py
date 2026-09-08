"""patch_visual_check_fix.py — fixes the first workflow run of the visual regression gate (X7), which stopped the build.

Root causes (both confirmed by reading the repo, not guessed):
  1. The workflow publishes the hub shell as site/index.html (update-dashboard.yml line "cp hub/EH_Hub.html site/index.html"),
     but visual_check.py looked for site/EH_Hub.html → "file missing from site/".
  2. Every Chart.js page (news, vision2030, fiscal) loads Chart.js from jsdelivr with an onerror fallback to
     vendor/chart.umd.min.js. The checker blocks CDNs on purpose (deterministic screenshots), so the fallback fires —
     and 404s, because chart.umd.min.js sits at hub/chart.umd.min.js, NOT hub/vendor/, and only hub/vendor/ is published.
     → "Chart is not defined" on all three pages, every chart blank, and Vision 2030's Arabic KPI bar empty (built by the
     same script, after the line that throws). This also means the production fallback was broken: a jsdelivr outage
     would have killed the charts on the live site.

Fixes:
  • hub/vendor/chart.umd.min.js — copied from hub/chart.umd.min.js (Chart.js 4.5.1). Makes the fallback real, in the
    gate and in production. The workflow already publishes hub/vendor/ wholesale, so no workflow change is needed.
  • pipeline/visual_check.py — hub shell looked up as index.html (EH_Hub.html accepted too); an explicit
    "Chart.js did not load" diagnosis instead of five lines of blank chart IDs; optional --allow-cdn switch for debugging.

Lives in pipeline/. Run once from anywhere: python3 pipeline/patch_visual_check_fix.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, CHANGES, write_change_table
REPO = os.path.abspath(os.path.join(HERE, '..')); HUB = os.path.join(REPO, 'hub')
VC = os.path.join(HERE, 'visual_check.py')
SRC_CHART = os.path.join(HUB, 'chart.umd.min.js'); DST_CHART = os.path.join(HUB, 'vendor', 'chart.umd.min.js')

if not os.path.exists(VC): sys.exit('Cannot find pipeline/visual_check.py')
if not os.path.exists(SRC_CHART) and not os.path.exists(DST_CHART): sys.exit('Cannot find hub/chart.umd.min.js to copy into hub/vendor/')
if '--allow-cdn' in open(VC, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
shutil.copy2(VC, VC + '.pre-vcfix.bak'); load(VC, 'vc')

# ---------------------------------------------------------------- 1. vendor fallback made real
if not os.path.exists(DST_CHART):
    shutil.copy2(SRC_CHART, DST_CHART)
    CHANGES.append(dict(file='hub/vendor/chart.umd.min.js', kind='file-copy', category='chart-fallback', old='(absent)',
                        new='copied from hub/chart.umd.min.js (Chart.js 4.5.1, %d bytes)' % os.path.getsize(DST_CHART),
                        note='vendor/chart.umd.min.js fallback referenced by news, vision2030 and fiscal pages now exists', occurrences=1, ok=True))

# ---------------------------------------------------------------- 2. checker: hub shell is published as index.html
rep('vc', "PAGES = {  # file: minimum expectations {canvases painted, kpi cards, tables, svgs}\n    'EH_Hub.html':                     dict(kpi=0, tables=0, svgs=0),",
    "PAGES = {  # file: minimum expectations {canvases painted, kpi cards, tables, svgs}\n    'index.html':                      dict(kpi=0, tables=0, svgs=0),   # hub shell — the workflow publishes hub/EH_Hub.html as site/index.html",
    'gate-fix', 'Hub shell looked up under its published name index.html')
rep('vc', "THRESHOLD = 0.06",
    "ALIASES = {'index.html': 'EH_Hub.html'}   # accepted alternative filename when the primary is absent (local runs against hub/)\nTHRESHOLD = 0.06",
    'gate-fix', 'EH_Hub.html still accepted when checking a folder that was not assembled by the workflow')
rep('vc', "            if not os.path.exists(os.path.join(a.site, page)): report[page] = 'missing'; failures.append(f'{page}: file missing from site/'); continue",
    "            if not os.path.exists(os.path.join(a.site, page)) and ALIASES.get(page) and os.path.exists(os.path.join(a.site, ALIASES[page])): page_file = ALIASES[page]\n"
    "            elif not os.path.exists(os.path.join(a.site, page)): report[page] = 'missing'; failures.append(f'{page}: file missing from site/'); continue\n"
    "            else: page_file = page",
    'gate-fix', 'Resolve the file to open (published name or its alias)')
rep('vc', "pg.goto(base + page + '?embedded=1', wait_until='load', timeout=60000)",
    "pg.goto(base + page_file + '?embedded=1', wait_until='load', timeout=60000)",
    'gate-fix', 'Open the resolved filename')

# ---------------------------------------------------------------- 3. checker: say plainly when Chart.js never loaded
rep('vc', " return {canvases:canv.length,blank,", " return {chartlib:typeof Chart!=='undefined',canvases:canv.length,blank,",
    'gate-fix', 'Report whether Chart.js is present on the page')
rep('vc', "                    if m['blank']: probs.append('blank charts: ' + ', '.join(m['blank']))",
    "                    if want.get('canvases', 0) and not m['chartlib']: probs.append('Chart.js did not load — CDN blocked by this check and vendor/chart.umd.min.js not served (copy hub/chart.umd.min.js into hub/vendor/)')\n"
    "                    elif m['blank']: probs.append('blank charts: ' + ', '.join(m['blank']))",
    'gate-fix', 'One clear line instead of a list of blank chart IDs when the library itself is missing')

# ---------------------------------------------------------------- 4. checker: --allow-cdn for debugging; CDN block explained
rep('vc', "ap.add_argument('--update-baseline', action='store_true'); ap.add_argument('--port', type=int, default=8794)",
    "ap.add_argument('--update-baseline', action='store_true'); ap.add_argument('--port', type=int, default=8794)\n"
    "    ap.add_argument('--allow-cdn', action='store_true', help='let cdnjs/jsdelivr/fonts load (default: blocked, so the gate exercises the vendor/ fallbacks and screenshots stay deterministic)')",
    'gate-fix', 'Optional --allow-cdn switch')
rep('vc', "                pg.route('**/*', lambda r: r.abort() if any(d in r.request.url for d in ('cdnjs', 'jsdelivr', 'googleapis', 'gstatic', 'openstreetmap', 'cartocdn')) else r.continue_())",
    "                # External hosts are blocked by default so (a) the run does not depend on a CDN being up, (b) screenshots are identical build-to-build,\n"
    "                # (c) the vendor/ fallbacks every page carries are exercised on every build. --allow-cdn lifts the block for scripts and fonts only.\n"
    "                blocked = ('openstreetmap', 'cartocdn') if a.allow_cdn else ('cdnjs', 'jsdelivr', 'googleapis', 'gstatic', 'openstreetmap', 'cartocdn')\n"
    "                pg.route('**/*', lambda r, _b=blocked: r.abort() if any(d in r.request.url for d in _b) else r.continue_())",
    'gate-fix', 'CDN block made explicit and switchable')

open(VC, 'w', encoding='utf-8').write(FILES['vc'])
write_change_table(os.path.join(HERE, 'change_table_visual_check_fix'), 'Change table — visual regression gate fix (index.html lookup · Chart.js vendor fallback)')
print('edits:', sum(1 for c in CHANGES if c['ok']), 'failures:', len(FAILURES))
for f in FAILURES: print('FAIL', f)
sys.exit(1 if FAILURES else 0)
