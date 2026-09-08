"""patch_visual_upgrade.py — Stage B visual upgrade (audit of 07 Sep 2026).
Lives in pipeline/ next to patchlib.py. Edits in place with .pre-visual.bak backups; refuses to run twice.

What it does
  * every hub/*.html page: loads hub/eh-shared.css + hub/eh-shared.js (font stack, embedded-mode header collapse,
    hub bridge gaps, KPI count-up, chart build-in once, 12px text floor, reduced-motion guard)
  * Vision 2030 / Fiscal / News: removes the Google Fonts links (blocked on corporate networks; one font stack for all)
  * Stakeholder map: opens on Tier 1 with a visible note instead of seven zeros and an empty map (D-B6)
  * Bubble map: "hover any dot" → "tap or hover any dot"
  * PIF annual-reports page: plain words for the remaining analyst labels
  * Bid dashboard (served copy): win rate, total tendered value and open pipeline become the three hero tiles (D-B4)
  * Hub shell: bilingual skeleton text; 180 ms cross-fade when a tab or sub-tab is shown
  * Generator: build_bid_dashboard.py emits the shared css/js links so the hourly rebuild keeps the upgrade
  * Workflow: publishes eh-shared.css and eh-shared.js
The matching edit for pipeline/app.js (KPI order) is in patch_bid_appjs.py because app.js was not available here.
"""
import os, sys, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, rep_re, FILES, FAILURES, CHANGES, write_change_table, nfkc
REPO = os.path.abspath(os.path.join(HERE, '..')); HUB = os.path.join(REPO, 'hub')
WF = os.path.join(REPO, '.github', 'workflows', 'update-dashboard.yml'); GEN = os.path.join(HERE, 'build_bid_dashboard.py')
PAGES = {'stake':'EH_Stakeholder_Map_CURRENT.html','bids':'EH_Bid_Analysis_CURRENT.html','bub':'EH_Client_Bubble_Map_CURRENT.html',
         'news':'eh_news_intelligence.html','v2030':'vision2030_dashboard.html','fisc':'saudi_fiscal_monitor_2026.html',
         'pif':'pif_intelligence_hub.html','strat':'pif_strategy_2026_2030.html'}
targets = {k: os.path.join(HUB, v) for k, v in PAGES.items()}; targets['hub'] = os.path.join(HUB, 'EH_Hub.html'); targets['wf'] = WF; targets['gen'] = GEN
for k, p in targets.items():
    if not os.path.exists(p): sys.exit(f'Cannot find {p}')
    shutil.copy2(p, os.path.join(HERE, os.path.basename(p) + '.pre-visual.bak'))
for f in ('eh-shared.css', 'eh-shared.js'):
    if not os.path.exists(os.path.join(HUB, f)): sys.exit(f'hub/{f} is missing — copy it in first.')
if 'eh-shared.js' in open(targets['strat'], encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for k, p in targets.items(): load(p, k)

SHARED_HEAD = '<link rel="stylesheet" href="eh-shared.css">\n</head>'
SHARED_BODY = '<script src="eh-shared.js" defer></script>\n</body>'
for k in PAGES:
    rep(k, '</head>', SHARED_HEAD, 'shared-layer', f'{PAGES[k]}: load eh-shared.css')
    rep(k, '</body>', SHARED_BODY, 'shared-layer', f'{PAGES[k]}: load eh-shared.js')
for k in ('v2030', 'fisc', 'news'):
    rep_re(k, r'\s*<link[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>', '', 'fonts', f'{PAGES[k]}: remove Google Fonts links (D-B5)', count=3)

# ---- Stakeholder map: open on Tier 1 with a note (D-B6)
rep('stake', '<script src="eh-shared.js" defer></script>\n</body>',
    '<script>/* default view (visual upgrade 07/09): Tier 1 shown on open, with a note; Reset filters shows the old empty gate */\n'
    "setTimeout(function(){try{if(!state.cats.size&&!state.tiers.size){CATS.forEach(function(c){state.cats.add(c.id);});document.querySelectorAll('#catFilters input').forEach(function(i){i.checked=true;});state.tiers.add('Tier 1');chipGroup('tierChips',TIERS,state.tiers);recompute();draw();"
    "var h=document.getElementById('emptyHint');if(h)h.style.display='none';var mv=document.getElementById('mapView');if(mv&&!document.getElementById('tier1Note')){var n=document.createElement('div');n.id='tier1Note';n.className='eh-note eh-fade-in';n.style.cssText='position:absolute;top:10px;left:12px;right:12px;z-index:6;pointer-events:auto';"
    "n.innerHTML=(typeof LNG!=='undefined'&&LNG==='ar')?'يُعرض الآن أصحاب المصلحة من <b>الفئة الأولى</b> فقط. أزل شريحة «الفئة الأولى» في الفلاتر لعرض الجميع (4,195 جهة). <a href=\\'#\\' onclick=\\'this.parentNode.remove();return false\\' style=\\'float:left\\'>إخفاء</a>':'Showing <b>Tier 1</b> organisations only. Remove the Tier 1 chip in Filters to see all 4,195. <a href=\\'#\\' onclick=\\'this.parentNode.remove();return false\\' style=\\'float:right\\'>hide</a>';mv.appendChild(n);}}}catch(e){}},250);</script>\n"
    '<script src="eh-shared.js" defer></script>\n</body>', 'ten-second', 'Stakeholder map: default Tier 1 view + note instead of zeros and an empty map')

# ---- Bubble map: hover copy
rep('bub', 'hover any dot for the name and numbers.', 'tap or hover any dot for the name and numbers.', 'plain-language', 'Bubble map: tap is the first verb (lesson #7)')

# ---- PIF annual-reports page: remaining analyst labels
rep('pif', 'PIF uses a standard international industry list (called GICS)', 'PIF uses a standard international industry list', 'plain-language', 'PIF hub: drop the GICS acronym from the reader-facing sentence', count=2)

# ---- Bid dashboard (served copy): hero tiles first (D-B4)
OLD_KPI = ("function rKPI(){$('kstrip').innerHTML=\n"
 " kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),'2024–2026')+\n"
 " kc('SAR '+fmtM(k.pipeline),t('Total tendered value','إجمالي قيمة المنافسات'),k.with_value+t(' priced',' مُسعّرة'))+\n"
 " kc('SAR '+fmtM(k.open_pipeline),t('Open pipeline','المحفظة المفتوحة'),k.open_count+t(' pending',' قيد الانتظار'))+\n"
 " kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/'+k.awarded+t(' awarded',' مُرساة'),k.win_rate>=50?'g':'r')+\n")
NEW_KPI = ("function rKPI(){$('kstrip').innerHTML=\n"
 " kc(pct(k.win_rate),t('Win rate','نسبة الفوز'),k.eh_won+'/'+k.awarded+t(' awarded',' مُرساة'),(k.win_rate>=50?'g':'r')+' hero')+\n"
 " kc('SAR '+fmtM(k.pipeline),t('Total tendered value','إجمالي قيمة المنافسات'),k.with_value+t(' priced',' مُسعّرة'),'hero')+\n"
 " kc('SAR '+fmtM(k.open_pipeline),t('Open pipeline','المحفظة المفتوحة'),k.open_count+t(' pending',' قيد الانتظار'),'hero')+\n"
 " kc(k.total,t('Tenders tracked','المنافسات المتتبَّعة'),'2024–2026')+\n")
rep('bids', OLD_KPI, NEW_KPI, 'ten-second', 'Bid KPI strip: win rate, total tendered value, open pipeline first and marked hero (D-B4)')
rep('bids', ".kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}",
    ".kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}\n"
    ".kc:has(.v.hero){grid-column:span 2;border-top-width:4px}.kc .v.hero{font-size:34px}.kc:has(.v.hero) .l{font-size:12.5px;font-weight:700}@media(max-width:700px){.kc:has(.v.hero){grid-column:span 1}.kc .v.hero{font-size:26px}}",
    'ten-second', 'Bid KPI strip: hero tile styling (served copy)')

# ---- Hub shell
for en, ar in [('Loading the stakeholder map…','جارٍ تحميل خريطة أصحاب المصلحة…'),('Loading bid intelligence…','جارٍ تحميل استخبارات المناقصات…'),('Loading the client portfolio…','جارٍ تحميل محفظة العملاء…'),
               ('Loading Vision 2030…','جارٍ تحميل رؤية 2030…'),('Loading Fiscal Monitor…','جارٍ تحميل مرصد المالية…'),('Loading News…','جارٍ تحميل الأخبار…'),('Loading PIF Hub…','جارٍ تحميل مركز الصندوق…'),('Loading PIF Strategy 2026–2030…','جارٍ تحميل استراتيجية الصندوق 2026–2030…')]:
    rep('hub', '<div class="spin"></div>'+en, '<div class="spin"></div><span class="tl" data-en="'+en+'" data-ar="'+ar+'">'+en+'</span>', 'bilingual', f'Hub skeleton text bilingual: {en}')
rep('hub', '.nsub.on{background:var(--green);border-color:var(--green);color:#fff}',
    '.nsub.on{background:var(--green);border-color:var(--green);color:#fff}\n'
    '@media (prefers-reduced-motion:no-preference){@keyframes ehIn{from{opacity:0}to{opacity:1}} main>iframe.on,#newswrap iframe.vis{animation:ehIn 180ms ease-out}}',
    'motion', 'Hub: 180 ms cross-fade when a frame is shown (reduced-motion safe)')
rep('hub', "    f.style.display=on?'block':'none';", "    f.style.display=on?'block':'none';f.classList.toggle('vis',on);",
    'motion', 'Hub nGo(): mark the visible News frame so the cross-fade can run')

# ---- Generator: keep the upgrade through the hourly rebuild
rep('gen', '</head>', SHARED_HEAD, 'shared-layer', 'build_bid_dashboard.py: emit eh-shared.css link')
rep('gen', '</body>', SHARED_BODY, 'shared-layer', 'build_bid_dashboard.py: emit eh-shared.js script')
rep('gen', ".kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}",
    ".kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0}\n"
    ".kc:has(.v.hero){grid-column:span 2;border-top-width:4px}.kc .v.hero{font-size:34px}.kc:has(.v.hero) .l{font-size:12.5px;font-weight:700}@media(max-width:700px){.kc:has(.v.hero){grid-column:span 1}.kc .v.hero{font-size:26px}}",
    'ten-second', 'build_bid_dashboard.py: hero tile CSS (this CSS block is a plain string in the generator)')

# ---- Workflow
rep('wf', "          cp hub/pif_strategy_2026_2030.html site/ 2>/dev/null || true\n",
    "          cp hub/pif_strategy_2026_2030.html site/ 2>/dev/null || true\n          cp hub/eh-shared.css hub/eh-shared.js site/ 2>/dev/null || true\n",
    'publish', 'Workflow: publish eh-shared.css and eh-shared.js')

# ---- write
for k, p in targets.items():
    with open(p, 'w', encoding='utf-8') as f: f.write(FILES[k])
md, js = write_change_table(os.path.join(HERE, 'change_table_visual_upgrade'), 'Change table — Stage B visual upgrade')
print('edits:', sum(1 for c in CHANGES if c['ok']), 'failures:', len(FAILURES))
for f in FAILURES: print('FAIL', f)
sys.exit(1 if FAILURES else 0)
