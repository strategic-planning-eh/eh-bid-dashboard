"""patch_n1_n3_x7.py — roadmap items N1 (Arabic dashboards for Fiscal Monitor and News Intelligence),
N3 (one-sentence caption under every chart on the PIF annual-reports page and the Clients executive tab) and
X7 (visual regression gate in the workflow). Lives in pipeline/. Run after patch_visual_upgrade.py and patch_whats_new.py.
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, CHANGES, write_change_table
REPO = os.path.abspath(os.path.join(HERE, '..')); HUB = os.path.join(REPO, 'hub')
F = {'fisc': os.path.join(HUB, 'saudi_fiscal_monitor_2026.html'), 'news': os.path.join(HUB, 'eh_news_intelligence.html'),
     'pif': os.path.join(HUB, 'pif_intelligence_hub.html'), 'bub': os.path.join(HUB, 'EH_Client_Bubble_Map_CURRENT.html'),
     'css': os.path.join(HUB, 'eh-shared.css'), 'wf': os.path.join(REPO, '.github', 'workflows', 'update-dashboard.yml')}
for k, p in F.items():
    if not os.path.exists(p): sys.exit(f'Cannot find {p}')
if not os.path.exists(os.path.join(HUB, 'eh-ar-dashboard.js')): sys.exit('hub/eh-ar-dashboard.js is missing — copy it in first.')
if not os.path.exists(os.path.join(HERE, 'visual_check.py')): sys.exit('pipeline/visual_check.py is missing — copy it in first.')
if 'eh-ar-dashboard.js' in open(F['fisc'], encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for k, p in F.items(): shutil.copy2(p, os.path.join(HERE, os.path.basename(p) + '.pre-n1n3x7.bak')); load(p, k)

# ------------------------------------------------------------------ N1: Arabic dashboards
OLD_HIDE = '.ar-mode > *:not(#ehArView):not(#ehLangBar):not(script):not(style){display:none !important}'
for k in ('fisc', 'news'):
    rep(k, OLD_HIDE, '.ar-mode .eh-en-only{display:none !important}', 'arabic-dashboard', f'{os.path.basename(F[k])}: Arabic mode no longer hides the whole dashboard — only English prose')
    rep(k, '<script src="eh-shared.js" defer></script>\n</body>', '<script src="eh-ar-dashboard.js" defer></script>\n<script src="eh-shared.js" defer></script>\n</body>', 'arabic-dashboard', f'{os.path.basename(F[k])}: load eh-ar-dashboard.js')
rep('css', '/* ---------- 3. Shared patterns ---------- */', '''/* ---------- 2b. Arabic dashboards (N1): explainer blocks moved under their charts; the rest of the Arabic report follows the charts ---------- */
.eh-ar-cap{display:none;margin-top:12px;padding-top:10px;border-top:1px dashed rgba(95,112,120,.35);font-size:13px;line-height:1.65}
body.ar-mode .eh-ar-cap{display:block}.eh-ar-title{font-weight:800;margin-bottom:4px;color:var(--eh-blue)}
body.ar-mode #ehArView.eh-ar-rest{display:block}body:not(.ar-mode) #ehArView.eh-ar-rest{display:none !important}
body.ar-mode .kpi .kdelta,body.ar-mode .kpi .ksrc,body.ar-mode .kpi .k-note{direction:ltr;text-align:start;unicode-bidi:plaintext}

/* ---------- 3. Shared patterns ---------- */''', 'arabic-dashboard', 'eh-shared.css: styles for moved Arabic explainers')

# ------------------------------------------------------------------ N3: captions (shape, not number — so they stay true when data refreshes)
PIF_CAPS = {
 'cAum':   ["The fund grew every year until 2025, when the line dips for the first time.", "نما الصندوق كل عام حتى 2025، حين ينخفض الخط لأول مرة."],
 'cPool':  ["Most of the money sits in a few large pools; the giga-projects pool is the one growing fastest.", "معظم الأموال في بضع مجموعات كبيرة؛ ومجموعة المشاريع الكبرى هي الأسرع نمواً."],
 'cSplit': ["Roughly four riyals in five stay inside Saudi Arabia; the share held abroad has been shrinking.", "نحو أربعة ريالات من كل خمسة تبقى داخل المملكة؛ وحصة الخارج تتقلص."],
 'cIntl':  ["Money abroad has stayed roughly flat in riyals while the whole fund grew — so its share fell.", "بقيت أموال الخارج ثابتة تقريباً بالريال بينما نما الصندوق كله — فانخفضت حصتها."],
 'cGics':  ["Three industries — technology and telecom, property, and finance — take most of the money; environment is not a category here.", "ثلاث صناعات — التقنية والاتصالات، والعقار، والمال — تأخذ معظم الأموال؛ والبيئة ليست فئة هنا."],
 'cStrat': ["PIF's own 2021 list ranked utilities and renewables fourth; that is where water sat before it got its own group.", "قائمة الصندوق لعام 2021 وضعت المرافق والطاقة المتجددة رابعاً؛ هناك كانت المياه قبل أن تحصل على مجموعتها."],
 'cEnergy':["Energy and utilities is a steady slice of the fund, not a growing one — the industry that matters most to EH is holding, not expanding.", "الطاقة والمرافق حصة ثابتة من الصندوق لا متنامية — القطاع الأهم لآفاق البيئة يحافظ على مكانه ولا يتوسع."],
 'cBal':   ["What PIF owns rises faster than what it owes; the gap between the two bars is the fund's net worth.", "ما يملكه الصندوق يرتفع أسرع مما يدين به؛ والفجوة بين العمودَين هي صافي ثروته."],
 'cPnl':   ["Profit swings from year to year far more than the fund's size does — a reminder that returns are lumpy.", "يتقلب الربح من عام لآخر أكثر بكثير من حجم الصندوق — تذكير بأن العوائد متذبذبة."],
 'cCf':    ["Cash going out to investments exceeds cash coming in most years; borrowing fills the gap.", "النقد الخارج للاستثمارات يتجاوز الداخل في معظم السنوات؛ والاقتراض يسدّ الفجوة."],
 'cRev':   ["Total income climbs steadily; cash in hand moves in steps, rising when PIF borrows or sells.", "يتصاعد الدخل الكلي باطراد؛ والنقد المتاح يتحرك على درجات، يرتفع عند الاقتراض أو البيع."],
 'cGreen': ["Green bond money raised has roughly quadrupled since 2022; pollution control and water are among the eligible uses.", "تضاعفت أموال السندات الخضراء نحو أربع مرات منذ 2022؛ ومكافحة التلوث والمياه من الاستخدامات المؤهلة."],
 'cTsr':   ["The yearly return since 2017 has drifted down every year — the fund is bigger but earning less per riyal.", "انحدر العائد السنوي منذ 2017 كل عام — الصندوق أكبر لكنه يكسب أقل لكل ريال."],
 'cStaff': ["Headcount has more than doubled in four years; PIF is building its own capacity to run assets, not only to fund them.", "تضاعف عدد الموظفين أكثر من مرتَين في أربع سنوات؛ يبني الصندوق قدرته على إدارة الأصول لا تمويلها فقط."],
}
caps_js = "const EH_CAPS=" + __import__('json').dumps(PIF_CAPS, ensure_ascii=False) + ";\n" + r'''
(function(){ /* one-sentence caption under every chart (N3) — follows the page language */
  function place(){ Object.keys(EH_CAPS).forEach(function(id){ var c=document.getElementById(id); if(!c)return; var box=c.closest('.cw')||c.parentElement; var cap=box.parentElement.querySelector('.eh-caption[data-for="'+id+'"]'); if(!cap){ cap=document.createElement('p'); cap.className='eh-caption'; cap.setAttribute('data-for',id); box.insertAdjacentElement('afterend',cap); } cap.textContent=EH_CAPS[id][(typeof LANG!=='undefined'&&LANG==='ar')?1:0]; }); }
  var oa=window.applyLang; if(typeof oa==='function'){ window.applyLang=function(){ var r=oa.apply(this,arguments); setTimeout(place,80); return r; }; }
  var od=window.drawAll; if(typeof od==='function'){ window.drawAll=function(){ var r=od.apply(this,arguments); place(); return r; }; }
  if(document.readyState==='complete') place(); else window.addEventListener('load',place);
})();
'''
rep('pif', '<script src="eh-shared.js" defer></script>\n</body>', '<script>\n' + caps_js + '</script>\n<script src="eh-shared.js" defer></script>\n</body>', 'captions', 'PIF annual-reports page: 14 chart captions (EN/AR), inserted after each chart and refreshed on language change')

BUB_CAPS = {
 'svgBridge': "Reads left to right: last year's total, then each client that added or lost value, ending at this year's total.",
 'svgPareto': "The curve shows how few clients make up most of the value — the steeper the start, the more EH depends on a handful of names.",
 'svgRet':    "Green bars are clients kept or gained between the two years; red bars are clients lost — the balance between them is the story.",
 'svgSlope':  "Each line is a sector: rising lines took a bigger share of revenue this year, falling lines a smaller one.",
 'svgQuad':   "Top right is the ideal — clients who buy many services and spend a lot; bottom right are big spenders who buy only one or two services and could buy more.",
 'svgDeal':   "Most clients sit in the small-deal buckets on the left; the few on the right carry a large share of the value.",
}
bub_js = "const EH_BUB_CAPS=" + __import__('json').dumps(BUB_CAPS, ensure_ascii=False) + r''';
(function(){ function place(){ Object.keys(EH_BUB_CAPS).forEach(function(id){ var s=document.getElementById(id); if(!s||s.parentElement.querySelector('.eh-caption[data-for="'+id+'"]'))return; var cap=document.createElement('div'); cap.className='eh-caption'; cap.setAttribute('data-for',id); cap.textContent=EH_BUB_CAPS[id]; s.insertAdjacentElement('afterend',cap); }); }
  if(document.readyState==='complete') place(); else window.addEventListener('load',place); setTimeout(place,1500); document.addEventListener('click',function(){ setTimeout(place,300); });
})();
'''
rep('bub', '<script src="eh-shared.js" defer></script>\n</body>', '<script>\n' + bub_js + '</script>\n<script src="eh-shared.js" defer></script>\n</body>', 'captions', 'Clients executive tab: 6 chart captions (English; Arabic layer is roadmap N2)')

# ------------------------------------------------------------------ X7: visual regression gate
rep('wf', "      - name: Package the page\n", """      # ---------- Visual regression gate (roadmap X7): every page, EN + AR, must render with painted charts and no script errors,
      #            and must not have changed by more than 6 % of pixels since the last good build (baseline = artefact) ----------
      - name: Restore visual baseline
        uses: dawidd6/action-download-artifact@v6
        continue-on-error: true
        with:
          workflow: update-dashboard.yml
          workflow_conclusion: success
          name: visual-baseline
          path: pipeline/visual_baseline
          search_artifacts: true

      - name: Visual regression check
        run: |
          pip install playwright pillow >/dev/null
          python -m playwright install --with-deps chromium >/dev/null
          python pipeline/visual_check.py --site site --baseline pipeline/visual_baseline --out pipeline/visual_out

      - name: Keep screenshots (always) and the new baseline (on pass)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: visual-screens
          path: |
            pipeline/visual_out
            pipeline/visual_baseline
          retention-days: 30
      - name: Update visual baseline artefact
        uses: actions/upload-artifact@v4
        with:
          name: visual-baseline
          path: pipeline/visual_baseline
          retention-days: 90
          overwrite: true

      - name: Package the page
""", 'visual-regression', 'Workflow: visual regression gate before publishing (X7)')
rep('wf', "          cp hub/eh-shared.css hub/eh-shared.js site/ 2>/dev/null || true\n", "          cp hub/eh-shared.css hub/eh-shared.js hub/eh-ar-dashboard.js site/ 2>/dev/null || true\n", 'arabic-dashboard', 'Workflow: publish eh-ar-dashboard.js')

for k, p in F.items(): open(p, 'w', encoding='utf-8').write(FILES[k])
write_change_table(os.path.join(HERE, 'change_table_n1_n3_x7'), 'Change table — N1 Arabic dashboards · N3 captions · X7 visual gate')
print('edits:', sum(1 for c in CHANGES if c['ok']), 'failures:', len(FAILURES))
for f in FAILURES: print('FAIL', f)
sys.exit(1 if FAILURES else 0)
