"""patch_org_view.py — Organisations view, Stage 2 (26 Oct 2026).

Applies Youssef's decisions from EH_Org_Unresolved_Names.xlsx and wires the view into the hub.

Edits made here (all logged to change_table_org_view.*):
  pipeline/aliases.csv                    17 approved bridges (the dry-run proposals), 3 "Link to" decisions, 1 PDC bridge, 4 rejected guards
  pipeline/org_bridges_proposed.csv       emptied — every row moved into aliases.csv
  hub/EH_Stakeholder_Map_CURRENT.html     10 new records ("Add as new record" decisions + Project Development Company (PDC), which Youssef
                                          confirmed is a different company from Saudi Energy)
  hub/EH_Hub.html                         sixth top-level tab "Organisations" (nav, skeleton, lazy iframe, mobile bar, footer, APPS/APPTAB,
                                          hub search: every hit gets an "Open profile" action)
  .github/workflows/update-dashboard.yml  build_org_profiles.py + build_org_page.py run after the bid→map sync and the Etimad step; page published
  pipeline/CHANGES.md                     What's New entry (2026-W44)
Run once: python3 pipeline/patch_org_view.py
"""
import os, sys, json, csv, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
H = os.path.join(ROOT, 'hub', 'EH_Hub.html'); W = os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml')
M = os.path.join(ROOT, 'hub', 'EH_Stakeholder_Map_CURRENT.html'); C = os.path.join(HERE, 'CHANGES.md')
if 'data-f="orgs"' in open(H, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
for p in (H, W, C): load(p, os.path.basename(p))
ADDED = 'Oct 2026'; SRC = 'bid tracker — Organisations view review (26 Oct 2026)'

# ---------- 1. bridges → aliases.csv ----------
approved = [  # tracker name, map name  (proposed in the dry run; Youssef returned the workbook 26 Oct 2026 — see note in the reply)
 ('هيئة الزكاة والضريبة والجمارك', 'Zakat, Tax and Customs Authorities'),
 ('المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر', 'National Center for Vegetation Cover Development & Combating Desertification (NCVC)'),
 ('المركز الوطني للرقابة على الالتزام البيئي', 'National Center for Environmental Compliance Monitoring (NCEC Monitoring)'),
 ('المركز الوطني للرقابة على الإلتزام البيئي', 'National Center for Environmental Compliance Monitoring (NCEC Monitoring)'),
 ('المركز الوطني للرقابةعلى الالتزام البيئي', 'National Center for Environmental Compliance Monitoring (NCEC Monitoring)'),
 ('المؤسسة العامة للصناعات العسكرية', 'Military Industries Corporation'),
 ('القوات البحرية', 'Royal Saudi Navy'),
 ('وزارة البيئة والزراعة والمياه', 'Ministry of Environment, Water and Agricultural'),
 ('وزارة البيئة والمياه والزراعة', 'Ministry of Environment, Water and Agricultural'),
 ('محمية الإمام عبدالعزيز بن محمد', 'Imam Abdulaziz bin Muhammad Royal Reserve'),
 ('jeddahairports (Jedco)', 'Jeddah Airports'),
 ('ACWA', 'ACWA Power'), ('Acwa', 'ACWA Power'),
 ('SAR', 'Saudi Arabia Railways (SAR)'),
 ('SAL Saudi Logistics Services', 'شركة سال السعودية للخدمات اللوجستية (SAL)'),
 ('Jabal Said Company', 'Jabal Sayid / Barrick-Ma’aden Copper'),
 ('شركة اسكو المحدودة', 'ESCO Environmental Consulting Co. (One-Person Co.)'),
 # "Link to" decisions in the workbook
 ('جامعة الحدود الشمالية', 'Northern Borders Region Municipality'),
 ('Aloula', 'Royal Commission for AlUla (RCU)'),
 ('شركة رمز العمران للمقاولات', 'Ramz Professional Consulting Group'),
 # Saudi Energy and PDC are two different companies officially (Youssef, 26 Oct 2026)
 ('Saudi Energy\nProject Development Company (PDC)\nالشركة السعودية للكهرباء', 'Project Development Company (PDC)'),
 # SWCC merged into the Saudi Water Authority (confirmed 26 Oct 2026) — recorded so the fold no longer depends on fuzzy tokens
 ('المؤسسة العامة لتحلية المياه المالحة', 'Saudi Water Authority'),
]
rejected = [
 ('الادارة العامة للخدمات الطبية للقوات المسلحة - وزارة الدفاع', 'Ministry of Commerce'),
 ('SAL Saudi Logistics Services', 'Owal Arabia Logistics Co.'),
 ('Aloula', 'Al-Oula Al-Mukhtassa General Contracting Est.'),
 ('Saudi Energy\nProject Development Company (PDC)\nالشركة السعودية للكهرباء', 'Saudi Energy (formerly SEC)'),
]
# tracker names with "Add as new record" that are the same body as an existing new record
same_as_new = [('الادارة العامة للخدمات الطبية للقوات المسلحة - وزارة الدفاع', 'الإدارة العامة للخدمات الطبية للقوات المسلحة')]
A = os.path.join(HERE, 'aliases.csv')
with open(A, encoding='utf-8-sig', newline='') as f: rows = list(csv.DictReader(f)); fields = list(rows[0].keys())
have = {(r['tracker_name'], r['map_name']) for r in rows}
new_rows = [dict(tracker_name=t, map_name=m, method='org-view review', status='approved', added=ADDED) for t, m in approved + same_as_new if (t, m) not in have] + \
           [dict(tracker_name=t, map_name=m, method='org-view guard', status='rejected', added=ADDED) for t, m in rejected if (t, m) not in have]
with open(A, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); [w.writerow(r) for r in rows + new_rows]
print('aliases.csv: +%d rows' % len(new_rows))
P = os.path.join(HERE, 'org_bridges_proposed.csv')
open(P, 'w', encoding='utf-8-sig', newline='').write('tracker_name,map_name,method,status,added\n')

# ---------- 2. new map records ----------
def rec(n, cat, tier, typ='GOV-ENTITY', rg='—', city='', note='', cf='Low'):
    return dict(n=n, cat=cat, rg=rg, city=city, reg='', typ=typ, sec='', tier=tier, bid=False, sites=None, mn=False, mp=False, act='',
                notes=(note + ' ' if note else '') + 'Added from the bid tracker (Organisations view review, 26 Oct 2026).',
                bc=0, bf='', threat='', collab=False, sc=None, cap=None, bk=0, cf=cf, cf_basis='bid tracker client / bidder',
                drv='', added_from=SRC, added_on=ADDED)
CL, GOV = 'Clients / Potential Clients', 'Government Clients & Institutions'
NEW = [
 rec('الهيئة العامة للنقل', GOV, 'GOV', note='Transport General Authority (TGA).'),
 rec('القوات الجوية', GOV, 'GOV', note='Royal Saudi Air Force.'),
 rec('الإدارة العامة للخدمات الطبية للقوات المسلحة', GOV, 'GOV', note='Armed Forces Medical Services, Ministry of Defense. Alias (merged duplicate): الادارة العامة للخدمات الطبية للقوات المسلحة - وزارة الدفاع.'),
 rec('المؤسسة العامة للتدريب التقني والمهني', GOV, 'GOV', note='Technical and Vocational Training Corporation (TVTC).'),
 rec('SAFE Entreprise', CL, 'Tier 2', typ='Other'),
 rec('Catrion', CL, 'Tier 2', typ='Other', note='Catering company (formerly Saudi Airlines Catering).'),
 rec('مستشفيات الهدا والأمير سلطان والأمير منصور ومركز التأهيل', GOV, 'GOV', note='Armed Forces hospitals cluster, Taif.'),
 rec('Project Development Company (PDC)', CL, 'Tier 2', typ='Other', note='Saudi Electricity Project Development Company — a different company from Saudi Energy (Youssef, 26 Oct 2026).'),
 rec('شركة ساس الرقمية', 'Active Competitors', 'Tier 4', typ='Other', note='Roster bidder.'),
 rec('شركة مور سيف للمقاولات', 'Active Competitors', 'Tier 4', typ='Other', note='Roster bidder.'),
]
mh = open(M, encoding='utf-8').read()
mm = re.search(r'(<script id="DATA" type="application/json">)(.*?)(</script>)', mh, re.S); D = json.loads(mm.group(2))
names = {n['n'] for n in D['nodes']}; added = [r for r in NEW if r['n'] not in names]
D['nodes'] += added
mh = mh[:mm.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + mh[mm.end(2):]
open(M, 'w', encoding='utf-8').write(mh); print('map: +%d records' % len(added))

# ---------- 3. hub shell ----------
ICON = '<svg class="ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M5.5 17c.4-2 1.9-3 3.5-3s3.1 1 3.5 3M14 9h4M14 13h4"/></svg>'
NEWS_BTN_END = 'data-ar="الأخبار والمستجدات">News &amp; Intelligence</span></button>\n  </div></nav>'
rep('EH_Hub.html', NEWS_BTN_END,
    'data-ar="الأخبار والمستجدات">News &amp; Intelligence</span></button>\n'
    '    <button class="tab" role="tab" data-f="orgs" data-t="Organisations" aria-pressed="false" onclick="go(this)" title="One profile per organisation — every tender it asked for, every bid against EH, what EH sells it · ملف لكل منظمة — كل منافسة طرحتها، كل عرض ضد آفاق البيئة، وما تبيعه لها آفاق البيئة">'
    + ICON + '<span class="tl" data-en="Organisations" data-ar="المنظمات">Organisations</span></button>\n  </div></nav>',
    'org-view', 'Sixth top-level tab after News & Intelligence')
SK = '<div class="skel" id="sk-bubbles">'
rep('EH_Hub.html', SK,
    '<div class="skel" id="sk-orgs"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading organisations…" data-ar="جارٍ تحميل المنظمات…">Loading organisations…</span></div></div>\n  ' + SK,
    'org-view', 'Loading skeleton')
IF = '<iframe id="f-bubbles" title="Client portfolio bubble chart" data-src="EH_Client_Bubble_Map_CURRENT.html" loading="lazy"></iframe>'
rep('EH_Hub.html', IF, IF + '\n  <iframe id="f-orgs" title="Organisations — one profile per client, bidder and competitor" data-src="organisations.html" loading="lazy"></iframe>',
    'org-view', 'Lazy iframe for the page')
MT = '<span class="tl" data-en="News" data-ar="الأخبار">News</span></button>\n</nav>'
rep('EH_Hub.html', MT,
    '<span class="tl" data-en="News" data-ar="الأخبار">News</span></button>\n'
    '  <button class="mtab" data-f="orgs" role="tab" onclick="go(document.querySelector(\'.tab[data-f=orgs]\'))">' + ICON.replace('class="ic" ', '') + '<span class="tl" data-en="Profiles" data-ar="الملفات">Profiles</span></button>\n</nav>',
    'org-view', 'Mobile tab bar button')
rep('EH_Hub.html', 'nav.mtabs{position:sticky;bottom:0;display:grid;grid-template-columns:repeat(4,1fr);', 'nav.mtabs{position:sticky;bottom:0;display:grid;grid-template-columns:repeat(5,1fr);', 'org-view', 'Mobile bar grid: five buttons')
rep('EH_Hub.html', '@media(max-width:640px){nav.mtabs{grid-template-columns:repeat(5,1fr)}', '@media(max-width:640px){nav.mtabs{grid-template-columns:repeat(6,1fr)}', 'org-view', 'Phone bar grid: six buttons')
rep('EH_Hub.html', 'data-en="Five live views · bids refresh hourly', 'data-en="Six live views · bids refresh hourly', 'org-view', 'Footer count (EN)')
rep('EH_Hub.html', 'data-ar="خمس لوحات حيّة · تُحدَّث العطاءات', 'data-ar="ست لوحات حيّة · تُحدَّث العطاءات', 'org-view', 'Footer count (AR)')
rep('EH_Hub.html', "hub:['Hub','المنصة']};", "hub:['Hub','المنصة'],orgs:['Organisations','المنظمات']};", 'org-view', 'What\'s New app label')
rep('EH_Hub.html', "clients:'bubbles',news:'news',hub:null};", "clients:'bubbles',news:'news',orgs:'orgs',hub:null};", 'org-view', 'What\'s New app → tab')
rep('EH_Hub.html', "'environment fund 2025 report':'ef2025',", "'environment fund 2025 report':'ef2025','organisations':'orgs','organisation profiles':'orgs','profiles':'orgs','المنظمات':'orgs',", 'org-view', 'View aliases for deep links')
# hub search: an "Open profile" action on every hit, routed to the Organisations view
HIT = """onclick="qGo(this.getAttribute(\\'data-n\\'))">'+esc(r.n)+(r.s?'<div style="font-size:10.5px;opacity:.65;margin-top:1px">'+esc(r.s)+'</div>':'')+'</div>';}).join('');"""
rep('EH_Hub.html', HIT,
    """onclick="qGo(this.getAttribute(\\'data-n\\'))">'+esc(r.n)+'<span class="qp" data-n="'+esc(r.n)+'" onclick="event.stopPropagation();qOrg(this.getAttribute(\\'data-n\\'))" title="'+L('Open the organisation profile','افتح ملف المنظمة')+'" style="float:'+(hubL==='ar'?'left':'right')+';font-size:10.5px;font-weight:600;color:var(--eh-sea,#0072BB);border:1px solid currentColor;border-radius:999px;padding:1px 8px;margin-inline-start:8px">'+L('Profile','الملف')+'</span>'+(r.s?'<div style="font-size:10.5px;opacity:.65;margin-top:1px">'+esc(r.s)+'</div>':'')+'</div>';}).join('');""",
    'org-view', 'Search hits carry an "Open profile" action')
QGO = "function qGo(name){\n  qHide(); qEl.value=name;"
rep('EH_Hub.html', QGO,
    "function qOrg(name){\n  qHide(); qEl.value=name;\n  go(document.querySelector('.tab[data-f=\"orgs\"]'));\n"
    "  var f=document.getElementById('f-orgs'), send=function(){ try{ f.contentWindow.postMessage({ehhub:'open-org',name:name},'*'); }catch(e){} };\n"
    "  if(f&&f.contentWindow&&f.dataset.ready){ send(); } else if(f){ f.addEventListener('load',function(){ f.dataset.ready='1'; setTimeout(send,250); },{once:true}); setTimeout(send,1200); }\n}\n" + QGO,
    'org-view', 'qOrg(): open the Organisations view on a name')

# ---------- 4. workflow ----------
ET = "          rm -f pipeline/etimad_data.xlsx pipeline/etimad_tenders.json\n"
rep('update-dashboard.yml', ET, ET +
    "\n      # ---------- Organisations view: one profile per client / bidder / winner, built after the sync and the Etimad step so the map carries the live bid and Etimad fields (26 Oct 2026) ----------\n"
    "      - name: Build the Organisations view\n        run: |\n"
    "          python pipeline/build_org_profiles.py --map site/EH_Stakeholder_Map_CURRENT.html --ba pipeline/bidanalytics2.json --bidraw pipeline/bidraw2.json \\\n"
    "            --aliases pipeline/aliases.csv --out pipeline/org_profiles.json --unresolved pipeline/org_unresolved_names.xlsx --stamp \"$(TZ='Asia/Riyadh' date +'%-d %b %Y')\"\n"
    "          python pipeline/build_org_page.py pipeline/org_profiles.json site/organisations.html\n",
    'org-view', 'Pipeline builds and publishes organisations.html')
ART = "            pipeline/roster_duplicates.json\n"
rep('update-dashboard.yml', ART, ART + "            pipeline/org_unresolved_names.xlsx\n", 'org-view', 'Unresolved-names workbook kept with the bid-sync-review artifact')

# ---------- 5. What's New ----------
ENTRY = ("## 2026-W44\n"
 "hub | major | Organisations | New: an Organisations view — one profile per client, bidder and competitor: every tender it asked for (with the full bidder roster and prices), every bid against EH, wins against EH, what EH sells it, licence and Etimad tenders. Search in English or Arabic; the hub search now offers \"Profile\" on every hit. | "
 "جديد: لوحة «المنظمات» — ملف لكل عميل ومتقدم ومنافس: كل منافسة طرحتها (مع قائمة المتقدمين والأسعار)، وكل عرض ضد آفاق البيئة، والفوز على آفاق البيئة، وما تبيعه لها آفاق البيئة، والترخيص ومنافسات اعتماد. البحث بالعربية أو الإنجليزية؛ ويعرض بحث المنصة الآن زر «الملف» على كل نتيجة.\n"
 "stake | minor | Data | 12 organisations the bid tracker names were added to the map (Transport General Authority, Royal Saudi Air Force, Armed Forces Medical Services, TVTC, Catrion, SAFE, PDC and others) and 22 tracker spellings linked to their map records, so ZATCA, NCVC, NCEC, MEWA, ACWA Power and SAL now carry their bid history. | "
 "أُضيفت إلى الخريطة 12 منظمة يذكرها جدول التتبع (الهيئة العامة للنقل، القوات الجوية، الخدمات الطبية للقوات المسلحة، التدريب التقني، كاتريون، سيف، شركة تطوير المشاريع وغيرها) ورُبطت 22 تسمية من الجدول بسجلاتها، فصار لهيئة الزكاة والغطاء النباتي والالتزام البيئي ووزارة البيئة وأكوا باور وسال تاريخ منافساتها.\n"
 "bids | minor | Data | Fixed: a per-unit price (bid 88/26, ZATCA framework) was treated as a typo and dropped; per-unit prices are now kept and flagged, and left out of value totals. | "
 "إصلاح: كان سعر الوحدة (منافسة 88/26، إطار هيئة الزكاة) يُعامل كخطأ ويُحذف؛ تُحفظ أسعار الوحدة الآن مع تمييزها وتُستبعد من مجاميع القيمة.\n\n")
rep('CHANGES.md', '## 2026-W43\n', ENTRY + '## 2026-W43\n', 'org-view', 'What\'s New entries for W44')

for p in (H, W, C): open(p, 'w', encoding='utf-8').write(FILES[os.path.basename(p)])
write_change_table(os.path.join(HERE, 'change_table_org_view'), 'Change table — Organisations view')
print('edits:', 17 - len(FAILURES), 'failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
