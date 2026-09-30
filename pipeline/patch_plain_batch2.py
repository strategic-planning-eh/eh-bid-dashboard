"""patch_plain_batch2.py — plain-language pass, batch 2 (30 Sep 2026): Vision 2030, Corporate & Government News,
Regulatory news, PIF Intelligence Hub, PIF Strategy 2026–2030. Same agreed rules as batch 1.

How it works (text only — ids, classes, data values used as keys and chart numbers are never touched):
  1. plain_text/textseg.py finds the text people read: HTML text and tooltips, and sentences (3+ words) inside the
     page scripts; library code is skipped. Quoted wording ("…") is left exactly as published.
  2. plain_text/rules_b2.py rewrites periods (Q2 → April–June), units (bn → billion), abbreviations, and source codes
     (AR25 p10 → 2025 report p.10, S26 → Strategy document); organisations are named in full once per page, in a sentence.
  3. Short display strings the step-1 filter skips (source citations, unit suffixes, period labels) get targeted edits.
  4. eh-ar-dashboard.js — the Arabic mode looks labels up by their English text, so every renamed label (batch 1's
     Fiscal Monitor and this batch's news page) gets its Arabic entry under the new English key.
A before/after table per page is written to change_table_plain_batch2.md. Run once.
"""
import os, sys, re, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'plain_text')); import textseg, rules_b2 as R
PAGES = ['vision2030_dashboard.html', 'eh_news_intelligence.html', 'government_news.html', 'pif_intelligence_hub.html', 'pif_strategy_2026_2030.html']
CITE_EN = [(r'\bAR2(\d) p\.? ?(\d+)', r'202\1 report p.\2'), (r'\bAR2(\d)\b', r'202\1 report'), (r'\bS26 p\.? ?(\d+)', r'Strategy document p.\1'),
           (r'\bS26 pN\b', 'Strategy document'), (r'\bS26\b', 'Strategy document'), (r'HUB findings', 'PIF Intelligence Hub findings'),
           (r'HUB D\.[A-Za-z_.]+(\[\d+\])?', 'figures in the PIF Intelligence Hub'), (r'(?<=[ ,(])p(\d+)\b', r'p.\1')]
MONEY = [r for r in R.EN if 'bn' in r[0] or 'mn' in r[0]]
PERIOD = [r for r in R.EN if re.search(r'Q\d|H\d', r[0])]
QSTR = re.compile(r"""(?<=[:,(\[ ])(['"])((?:(?!\1)[^\\\n]|\\.){1,160})\1|>([^<>]{1,160})<""")
log = []
def sub_quoted(s, pred, rules):
    def f(m):
        txt = m.group(2) if m.group(2) is not None else m.group(3)
        if not pred(txt): return m.group(0)
        new = txt
        for a, b in rules: new = re.sub(a, b, new)
        if new == txt: return m.group(0)
        log.append((txt, new))
        return m.group(0).replace(txt, new, 1)
    return QSTR.sub(f, s)
if 'Strategy document p.' in open(os.path.join(ROOT, 'hub', 'pif_strategy_2026_2030.html'), encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
report = ['# Change table — plain-language batch 2\n']
for f in PAGES:
    p = os.path.join(ROOT, 'hub', f); s = open(p, encoding='utf-8').read(); shutil.copy2(p, p + '.pre-plain.bak'); log.clear()
    s, ch = textseg.apply2(s, R.EN, R.AR, R.FIRST); log.extend(ch)
    s = sub_quoted(s, lambda t: bool(re.match(r'\s*(AR2\d|S26|HUB )', t)), CITE_EN)                              # source citations
    s = re.sub(r"\b(src|bsrc|ssrc):'S26'", r"\1:'Strategy document'", s)
    s = sub_quoted(s, lambda t: bool(re.search(r'(^|\s|\d)bn\b|\bmn\b', t)) and len(t) < 60, MONEY)            # unit suffixes
    s = re.sub(r"\bunit:'bn'", "unit:'billion'", s)
    s = sub_quoted(s, lambda t: bool(re.search(r'\b(Q[1-4]|H[12])\b(?!-\d)', t)) and bool(re.search(r'—|results|report|\(|·|profit', t)), PERIOD)  # periods in source lists
    if f == 'eh_news_intelligence.html':
        a = "const periodLabel = p => p==='Q2-2026'?'Q2 2026':(p==='Q3-2026'?'Q3 2026 · war restart':"
        assert a in s; s = s.replace(a, "const periodLabel = p => p==='Q2-2026'?'April–June 2026':(p==='Q3-2026'?'July–September 2026 · fighting restarts':"); log.append((a, 'period labels in words'))
    if f == 'vision2030_dashboard.html':
        n = s.count(".replace('Joint Venture','JV')"); assert n == 2; s = s.replace(".replace('Joint Venture','JV')", ".replace('Joint Venture','Joint venture')"); log.append(("'JV' badge", "'Joint venture'"))
    open(p, 'w', encoding='utf-8').write(s)
    report.append(f'\n## {f} — {len(log)} changes\n\n| Before | After |\n|---|---|\n')
    for o, n in log: report.append(f"| {o[:400].replace('|','/').replace(chr(10),' ')} | {n[:400].replace('|','/').replace(chr(10),' ')} |\n")
    print(f, len(log), 'changes')

# ---- Arabic mode dictionaries
A = os.path.join(ROOT, 'hub', 'eh-ar-dashboard.js'); a = open(A, encoding='utf-8').read(); shutil.copy2(A, A + '.pre-plain.bak')
FISC_KPI = {'Gap between spending and income, Jan–Jun 2026 (official)':'الفجوة بين الإنفاق والدخل، يناير–يونيو 2026 (رسمي)','Gap between spending and income, Apr–Jun 2026':'الفجوة بين الإنفاق والدخل، أبريل–يونيو 2026','World oil price (Brent) — close on 25/08':'سعر النفط العالمي (برنت) — إغلاق 25/08','Share of oil exports leaving through Yanbu':'حصة صادرات النفط الخارجة عبر ينبع','Saudi oil exports (June)':'صادرات النفط السعودي (يونيو)','Ships passing through Hormuz':'السفن العابرة لهرمز','Government debt (end of June)':'الدين الحكومي (نهاية يونيو)','Government savings at the central bank (end of June)':'مدخرات الحكومة لدى البنك المركزي (نهاية يونيو)'}
FISC_LBL = {'Jan–Jun 2025':'يناير–يونيو 2025','Jan–Jun 2026':'يناير–يونيو 2026','Jan–Mar 2025':'يناير–مارس 2025','Jan–Mar 2026':'يناير–مارس 2026','Apr–Jun 2025':'أبريل–يونيو 2025','Apr–Jun 2026':'أبريل–يونيو 2026','Oil income':'دخل النفط','Other income':'الدخل الآخر','Total income':'إجمالي الدخل','Salaries':'الرواتب','Building & equipment':'المباني والمعدات','Interest & borrowing costs':'الفوائد وتكاليف الاقتراض','Military & security':'العسكري والأمن','Health & social development':'الصحة والتنمية الاجتماعية','General spending':'إنفاق عام','Regional government':'الإدارة الإقليمية','Economy & natural resources':'الاقتصاد والموارد الطبيعية','Municipal services':'الخدمات البلدية','Government administration':'الإدارة الحكومية','Infrastructure & transport':'البنية التحتية والنقل','Gap (SAR billion)':'الفجوة (مليار ريال)','2026 budget ÷ 4 (a quarter of the year)':'ميزانية 2026 ÷ 4 (ربع السنة)','Jan–Mar 2026 actual':'يناير–مارس 2026 الفعلي','Oil price so far (approx.; August = average to 25/08)':'سعر النفط حتى الآن (تقريبي؛ أغسطس = المتوسط حتى 25/08)','Jul–Dec · most likely: long war ($85–95)':'يوليو–ديسمبر · الأرجح: حرب طويلة (85–95 دولارًا)','Jul–Dec · worst: Yanbu route cut (spike above $110)':'يوليو–ديسمبر · الأسوأ: انقطاع طريق ينبع (قفزة فوق 110 دولارات)','Jul–Dec · calmer: Hormuz deal ($72–80)':'يوليو–ديسمبر · الأهدأ: اتفاق هرمز (72–80 دولارًا)','Price the budget assumed ($69.9, 2025 average)':'السعر المفترض في الميزانية (69.9 دولارًا، متوسط 2025)','Official figures (end of March, end of June)':'الأرقام الرسمية (نهاية مارس، نهاية يونيو)','Most likely · long war — year ~310':'الأرجح · حرب طويلة — السنة نحو 310','Worst · Yanbu route cut — year ~355':'الأسوأ · انقطاع طريق ينبع — السنة نحو 355','Calmer · Hormuz deal — year ~275':'الأهدأ · اتفاق هرمز — السنة نحو 275','2026 plan (\u2212165.4)':'خطة 2026 (\u2212165.4)','2025 result (\u2212276.6)':'نتيجة 2025 (\u2212276.6)','Fighting restarts · 8 Jul':'استئناف القتال · 8 يوليو','Red Sea attacks · 25 Jul':'هجمات البحر الأحمر · 25 يوليو','Oil price, US$ per barrel':'سعر النفط، دولار للبرميل','Gap so far this year (SAR billion)':'الفجوة منذ بداية العام (مليار ريال)','SAR billion (gap in the quarter)':'مليار ريال (فجوة الربع)','SAR billion (six months)':'مليار ريال (ستة أشهر)','End of March (actual)':'نهاية مارس (فعلي)','End of June (actual)':'نهاية يونيو (فعلي)','End of September':'نهاية سبتمبر','End of December':'نهاية ديسمبر'}
FISC_SEC = {'Key figures':'الأرقام الرئيسية','The budget plan vs what happened, January–June 2026':'خطة الميزانية مقابل ما حدث فعلًا، يناير–يونيو 2026','How 2026 could end':'كيف قد ينتهي عام 2026','What could happen in July–December 2026':'ما قد يحدث في يوليو–ديسمبر 2026','Where the figures come from':'من أين تأتي الأرقام'}
js = lambda d: ','.join(json.dumps(k, ensure_ascii=False).replace('"', "'", 1)[:-1] + "':" + "'" + v + "'" for k, v in d.items())
def add(block_start, d):
    global a
    i = a.index(block_start); j = i + len(block_start)
    a = a[:j] + js(d) + ',' + a[j:]
fi = a.index('fisc:{')
for name, d in (('kpi:{', FISC_KPI), ('lbl:{', FISC_LBL), ('sec:{', FISC_SEC)):
    i = a.index(name, fi); j = i + len(name); a = a[:j] + js(d) + ',' + a[j:]
# news: every English key that batch 2 would rename gets a twin under its new text
ni = a.index('news:{'); ne = a.index('}[PAGE]', ni); block = a[ni:ne]
def plain(k):
    for x, y in R.EN: k = re.sub(x, y, k)
    return k
extra = {}
for m in re.finditer(r"'([^'\\]+)':'([^'\\]+)'", block):
    k, v = m.group(1), m.group(2)
    if len(re.findall(r'[A-Za-z]{2,}', k)) >= 3 and plain(k) != k: extra[plain(k)] = v
for name in ('kpi:{', 'lbl:{', 'chart:{'):
    if extra:
        i = a.index(name, a.index('news:{')); j = i + len(name); a = a[:j] + js(extra) + ',' + a[j:]
open(A, 'w', encoding='utf-8').write(a)
report.append(f'\n## eh-ar-dashboard.js\n\nArabic entries added for {len(FISC_KPI)+len(FISC_LBL)+len(FISC_SEC)} renamed Fiscal Monitor labels and {len(extra)} renamed news labels: {", ".join(extra)}\n')
open(os.path.join(HERE, 'change_table_plain_batch2.md'), 'w', encoding='utf-8').write(''.join(report))
print('Arabic dictionary entries added:', len(FISC_KPI) + len(FISC_LBL) + len(FISC_SEC), '+', len(extra))
