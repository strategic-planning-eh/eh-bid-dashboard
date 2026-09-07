"""patch_pif_strategy.py — hub insertion for pif_strategy_2026_2030.html (Option A: fifth .nsub sub-tab in the
News & Intelligence view, adjacent to the PIF Intelligence Hub sub-tab; same style, same lazy-iframe behaviour).
Also cross-links pif_intelligence_hub.html -> new dashboard. Run from a directory containing patchlib.py.

Location: pipeline/patch_pif_strategy.py (with pipeline/patchlib.py). Edits hub/EH_Hub.html, hub/pif_intelligence_hub.html and
.github/workflows/update-dashboard.yml in place, after saving pipeline/<name>.pre-pif-strategy.bak backups.
Writes pipeline/change_table_pif_strategy.{md,json}.
Safe to re-run: exits without changes if the sub-tab is already present.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, rep, rep_re, FILES, FAILURES, write_files, write_change_table, nfkc

# Repo layout (strategic-planning-eh/eh-bid-dashboard):
#   hub/                     EH_Hub.html + the dashboards (+ hub/vendor/)      <- files edited here
#   pipeline/                tooling, this script, patchlib.py                 <- this script lives here
#   .github/workflows/update-dashboard.yml   publishes hub/* to site/          <- edited here (adds the new file)
# Run from anywhere:  python3 pipeline/patch_pif_strategy.py
# Edits in place after saving pipeline/<name>.pre-pif-strategy.bak backups; refuses to run twice.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
HUB = os.path.join(REPO, 'hub')
WF = os.path.join(REPO, '.github', 'workflows', 'update-dashboard.yml')
import shutil
for src in (os.path.join(HUB, 'EH_Hub.html'), os.path.join(HUB, 'pif_intelligence_hub.html'), WF):
    if not os.path.exists(src):
        sys.exit(f'Cannot find {src} — this script expects to sit in pipeline/ with hub/ and .github/workflows/ as siblings.')
    shutil.copy2(src, os.path.join(HERE, os.path.basename(src) + '.pre-pif-strategy.bak'))
if 'data-n="strat"' in open(os.path.join(HUB, 'EH_Hub.html'), encoding='utf-8').read():
    sys.exit('EH_Hub.html already contains the PIF Strategy sub-tab — patch already applied, nothing to do.')
if not os.path.exists(os.path.join(HUB, 'pif_strategy_2026_2030.html')):
    print('WARNING: hub/pif_strategy_2026_2030.html is not present yet — copy it in before pushing, or the sub-tab will load an empty frame.')
IN = OUT = HUB
load(f'{IN}/EH_Hub.html', 'hub')
load(f'{IN}/pif_intelligence_hub.html', 'pif')
load(WF, 'wf')

# ------------------------------------------------------------------ EH_Hub.html
# 1. sub-tab button, immediately after the PIF Intelligence Hub sub-tab, with a "New" badge (same visual as .tbadge)
rep('hub',
    '<button class="nsub" data-n="pif"><span class="tl" data-en="PIF Intelligence Hub" data-ar="مركز استخبارات صندوق الاستثمارات">PIF Intelligence Hub</span></button>\n    </div>',
    '<button class="nsub" data-n="pif"><span class="tl" data-en="PIF Intelligence Hub" data-ar="مركز استخبارات صندوق الاستثمارات">PIF Intelligence Hub</span></button>\n'
    '      <button class="nsub" data-n="strat" title="PIF Strategy 2026–2030 — what changed, and what it means for EH · استراتيجية صندوق الاستثمارات العامة 2026–2030 — ما الذي تغيّر وماذا يعني لآفاق البيئة">'
    '<span class="tl" data-en="PIF Strategy 2026–2030" data-ar="استراتيجية صندوق الاستثمارات العامة 2026–2030">PIF Strategy 2026–2030</span>'
    '<span class="newb" aria-label="New">New</span></button>\n    </div>',
    'hub-insert', 'News sub-tab: PIF Strategy 2026–2030 button with New badge, adjacent to PIF Intelligence Hub')

# 2. skeleton loader + lazy iframe, after the PIF ones
rep('hub',
    '<iframe id="f-pif" title="PIF annual reports intelligence" data-src="pif_intelligence_hub.html" loading="lazy" style="display:none"></iframe>',
    '<iframe id="f-pif" title="PIF annual reports intelligence" data-src="pif_intelligence_hub.html" loading="lazy" style="display:none"></iframe>\n'
    '      <div class="skel" id="sk-strat"><div class="in"><div class="spin"></div>Loading PIF Strategy 2026–2030…</div></div>\n'
    '      <iframe id="f-strat" title="PIF Strategy 2026–2030 — what changed, and what it means for EH" data-src="pif_strategy_2026_2030.html" loading="lazy" style="display:none"></iframe>',
    'hub-insert', 'News view: skeleton + lazy iframe for pif_strategy_2026_2030.html')

# 3. the hard-coded sub-tab list in nGo()
rep('hub', "['v2030','fiscal','corp','pif'].forEach(k=>{", "['v2030','fiscal','corp','pif','strat'].forEach(k=>{",
    'hub-insert', "nGo(): register 'strat' in the sub-tab array")

# 4. New-badge style (reuses the hub's orange .tbadge look; hidden once the tab has been opened)
rep('hub', '.nsub.on{background:var(--green);border-color:var(--green);color:#fff}',
    '.nsub.on{background:var(--green);border-color:var(--green);color:#fff}\n'
    '.nsub .newb{display:inline-block;margin-inline-start:6px;padding:1px 6px;border-radius:9px;background:#E8862E;color:#fff;font-size:10px;font-weight:800;vertical-align:middle;letter-spacing:.02em}\n'
    '.nsub.on .newb,.nsub.seen .newb{display:none}',
    'hub-insert', 'CSS: .newb badge on sub-tabs (hidden when active/seen)')

# 5. mark the tab as seen once opened (sub-tab click handler)
rep('hub', "document.querySelectorAll('.nsub').forEach(b=>b.addEventListener('click',()=>nGo(b)));",
    "document.querySelectorAll('.nsub').forEach(b=>b.addEventListener('click',()=>{nGo(b);b.classList.add('seen');}));",
    'hub-insert', 'Sub-tab click: add .seen so the New badge retires after first open')

# 6. footer copy: three integrated views + news wing count is unchanged; hub footer not touched (no stale count there)

# --------------------------------------------------------- pif_intelligence_hub.html
# 7. nav cross-link to the new dashboard (bilingual via I18N key)
rep('pif', '<a href="#findings" data-k="nav_findings">Findings</a></nav>',
    '<a href="#findings" data-k="nav_findings">Findings</a><a href="pif_strategy_2026_2030.html" data-k="nav_strat" style="border-color:var(--g);color:var(--g)">PIF Strategy 2026–2030 →</a></nav>',
    'cross-link', 'Nav: link to pif_strategy_2026_2030.html')
rep('pif', 'const I18N={"title":',
    'const I18N={"nav_strat": ["PIF Strategy 2026–2030 →", "استراتيجية صندوق الاستثمارات العامة 2026–2030 ←"], "title":',
    'cross-link', 'I18N: nav_strat key (EN/AR)')

# 8. findings f4 already mentions the 2026–2030 structure; add a pointer sentence (EN + AR) so readers find the companion
rep('pif', 'and the 2026–2030 structure with its named "Clean Energy, Water and Renewables Infrastructure" ecosystem (2025).</p>',
    'and the 2026–2030 structure with its named "Clean Energy, Water and Renewables Infrastructure" ecosystem (2025). '
    'The strategy document itself, published 2026, is analysed in the companion dashboard <a href="pif_strategy_2026_2030.html">PIF Strategy 2026–2030</a>; '
    'it spells the ecosystem "Clean Energy, Water &amp; Renewable Infrastructure", which is treated as canonical there.</p>',
    'cross-link', 'Findings f4: pointer to the strategy dashboard and the canonical ecosystem spelling (EN)')

# Arabic copy of f4 lives in I18N["f4"][1]; append the same pointer there (exact anchor on the string's tail)
rep('pif', 'والطاقة المتجددة\\" (2025)."]',
    'والطاقة المتجددة\\" (2025). وثيقة الاستراتيجية نفسها (2026) محلَّلة في اللوحة المرافقة <a href=\\"pif_strategy_2026_2030.html\\">استراتيجية صندوق الاستثمارات العامة 2026–2030</a>."]',
    'cross-link', 'Findings f4 (AR): pointer to the strategy dashboard')

# --------------------------------------------- .github/workflows/update-dashboard.yml
# 9. publish the new dashboard alongside the PIF hub (the workflow only copies files it is told to)
rep('wf', "          cp hub/pif_intelligence_hub.html site/ 2>/dev/null || true\n",
    "          cp hub/pif_intelligence_hub.html site/ 2>/dev/null || true\n          cp hub/pif_strategy_2026_2030.html site/ 2>/dev/null || true\n",
    'publish', 'Workflow: copy pif_strategy_2026_2030.html into site/')

# ------------------------------------------------------------------ finish
# nfkc() in patchlib is Arabic-script-only, so it is safe on whole files (m³, …, ² untouched)
# Whole-file Arabic normalisation is NOT applied: the PIF hub uses tatweel deliberately as a prefix connector (لـ"سرك", بـ13).
# Inserted strings are normalised inside patchlib.rep / rep_re.
from patchlib import FILES as _F
wf_txt = _F.pop('wf'); _F.pop('wf.__path')
paths = write_files(OUT)
open(WF, 'w', encoding='utf-8').write(wf_txt); paths.append(WF)
md, js = write_change_table(os.path.join(HERE, 'change_table_pif_strategy'), 'Change table — PIF Strategy 2026–2030 hub insertion')
print('written:', paths)
from patchlib import CHANGES
print('edits:', sum(1 for c in CHANGES if c['ok']), 'failures:', len(FAILURES))
if FAILURES:
    for f in FAILURES: print('FAIL', f)
    sys.exit(1)
