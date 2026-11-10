"""patch_org_news.py — Organisations view: 'News & Vision 2030' section in every profile (10 Nov 2026, Youssef).

Adds one card between 'Government tenders (Etimad)' and 'Notes and evidence' with two groups:
  Named in the news   items from News & Intelligence that name the organisation
  Sector context      items about the organisation's sector (tender clients, EH clients and Tier 1–2 only)
Data comes from build_org_news.py (org_news_config.json holds the sector rules); this patch only touches the page
renderer (build_org_page.py), the publish workflow (one new step after the Regulatory news feed is restored) and CHANGES.md.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table

ROOT = os.path.dirname(HERE)
PAGE = os.path.join(HERE, 'build_org_page.py'); WF = os.path.join(ROOT, '.github', 'workflows', 'update-dashboard.yml'); CH = os.path.join(HERE, 'CHANGES.md')
load(PAGE, 'page'); load(WF, 'wf')
if 'newsBlock' in FILES['page']: sys.exit('Already applied.')
ok = []

# ---- 1. styles
ok.append(rep('page', ".notes{white-space:pre-wrap;font-size:13px;color:var(--eh-ink-2);line-height:1.6}",
 ".notes{white-space:pre-wrap;font-size:13px;color:var(--eh-ink-2);line-height:1.6}\n"
 ".nw-g{margin-top:18px}.nw-g:first-child{margin-top:0}\n"
 ".nw-t{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 10px;font-weight:700;font-size:13.5px;color:var(--eh-deep)}html.dark .nw-t{color:var(--eh-ink)}\n"
 ".nw-t .n{font-weight:600;font-size:12px;color:var(--eh-ink-3)}\n"
 ".nw-s{font-size:12.5px;color:var(--eh-ink-2);margin:3px 0 4px;line-height:1.5}\n"
 ".nw{list-style:none;margin:0;padding:0}.nw li{padding:10px 0;border-bottom:1px solid var(--eh-line)}.nw li:last-child{border-bottom:0}\n"
 ".nw .m{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;font-size:11.5px;color:var(--eh-ink-3)}\n"
 ".nw .h{font-weight:600;margin-top:5px;line-height:1.5;font-size:13.5px}.nw .h a{color:inherit;text-decoration:underline;text-decoration-color:var(--eh-line);text-underline-offset:3px}.nw .h a:hover{color:var(--eh-sea)}\n"
 ".nw .w{font-size:12.5px;color:var(--eh-ink-2);margin-top:3px;line-height:1.55}\n"
 ".nw-btn{margin-top:8px}.nw-cap{font-size:11.5px;color:var(--eh-ink-3);margin-top:14px;padding-top:10px;border-top:1px solid var(--eh-line);line-height:1.5}\n"
 "@media print{.nw-more{display:block!important}.nw-btn{display:none!important}}",
 'org-news', 'Styles for the News & Vision 2030 card'))

# ---- 2. labels (EN → AR)
ok.append(rep('page', " 'Tier':'التصنيف','map':'خريطة','SAR':'ريال',",
 " 'News & Vision 2030':'الأخبار ورؤية 2030','Named in the news':'ورد اسمها في الأخبار','Sector context':'سياق القطاع',\n"
 " 'News, regulatory releases, Vision 2030 projects and PIF strategy lines that name this organisation.':'أخبار وإعلانات تنظيمية ومشاريع رؤية 2030 وبنود من استراتيجية صندوق الاستثمارات العامة ورد فيها اسم هذه المنظمة.',\n"
 " 'Not about this organisation by name — news and Vision 2030 projects in its sector:':'ليست عن هذه المنظمة بالاسم — أخبار ومشاريع رؤية 2030 في قطاعها:',\n"
 " 'No item in News & Intelligence names this organisation':'لا يوجد بند في الأخبار والمعلومات يذكر هذه المنظمة بالاسم',\n"
 " 'No sector on record for this organisation, so no sector context is shown':'لا يوجد قطاع مسجّل لهذه المنظمة، لذا لا يُعرض سياق القطاع',\n"
 " 'No news on record for this sector':'لا توجد أخبار مسجّلة لهذا القطاع',\n"
 " 'Sector context is shown for tender clients, EH clients and Tier 1–2 organisations only.':'يُعرض سياق القطاع لعملاء المنافسات وعملاء آفاق البيئة ومنظمات التصنيف الأول والثاني فقط.',\n"
 " 'No news on record':'لا توجد أخبار في السجل','News briefing':'موجز الأخبار','Regulatory news':'الأخبار التنظيمية','Vision 2030 project':'مشروع رؤية 2030','PIF Strategy 2026–2030':'استراتيجية الصندوق 2026–2030',\n"
 " 'Show all':'عرض الكل','Show fewer':'عرض أقل','What it means for EH':'ماذا يعني لآفاق البيئة','named in the detail':'ورد الاسم في التفاصيل','reviewed':'روجع',\n"
 " 'Taken from the News & Intelligence pages as published: the news briefing, Regulatory news, the Vision 2030 dashboard and the PIF Strategy 2026–2030 page. Arabic news headlines are EH translations; regulatory headlines stay in the language of the source.':'مأخوذة من صفحات الأخبار والمعلومات كما نُشرت: موجز الأخبار، والأخبار التنظيمية، ولوحة رؤية 2030، وصفحة استراتيجية الصندوق 2026–2030. عناوين الأخبار بالعربية ترجمة آفاق البيئة؛ وعناوين الأخبار التنظيمية تبقى بلغة المصدر.',\n"
 " 'Tier':'التصنيف','map':'خريطة','SAR':'ريال',",
 'org-news', 'Arabic labels for the News & Vision 2030 card'))

# ---- 3. renderer
NEWS_JS = r'''var NIDX={};(ORG.news_items||[]).forEach(function(x){NIDX[x.id]=x});
var NSRC={news:['News briefing','blue'],reg:['Regulatory news','green'],v2030:['Vision 2030 project','grey'],pif:['PIF Strategy 2026–2030','grey']};
function newsRow(id,p,i){var x=NIDX[id];if(!x)return'';var ar=LANG==='ar',head=ar?(x.ar||x.en):(x.en||x.ar),why=ar?(x.why_ar||''):(x.why_en||''),who=ar?(x.who_ar||x.who||''):(x.who||''),s=NSRC[x.src]||[x.src,'grey'];
  var det=(p.news.primary!=null&&i>=p.news.primary&&i>=0)?'<span>· '+t('named in the detail')+'</span>':'';
  var hd='<bdi dir="auto">'+esc(head)+'</bdi>';if(x.url)hd='<a href="'+esc(x.url)+'" target="_blank" rel="noopener">'+hd+'</a>';
  return'<li><div class="m"><span class="eh-chip '+s[1]+'">'+t(s[0])+'</span>'+(x.date?'<span>'+(x.src==='v2030'?t('reviewed')+' ':'')+d(x.date)+'</span>':'')+(who?'<span>· <bdi dir="auto">'+esc(who)+'</bdi></span>':'')+det+'</div><div class="h">'+hd+'</div>'+
    (why?'<div class="w">'+(x.src==='news'?'<b>'+t('What it means for EH')+':</b> ':'')+'<bdi dir="auto">'+esc(why)+'</bdi></div>':'')+'</li>'}
function newsList(ids,p,key,isM){var N=5,a=ids.slice(0,N).map(function(id,i){return newsRow(id,p,isM?i:-1)}).join(''),b=ids.slice(N).map(function(id,i){return newsRow(id,p,isM?i+N:-1)}).join('');
  return'<ul class="nw">'+a+'</ul>'+(b?'<ul class="nw nw-more" id="nw-'+key+'" style="display:none;border-top:1px solid var(--eh-line)">'+b+'</ul><button class="eh-btn nw-btn" onclick="var u=document.getElementById(\'nw-'+key+'\'),o=u.style.display===\'none\';u.style.display=o?\'\':\'none\';this.textContent=o?t(\'Show fewer\'):t(\'Show all\')+\' ('+ids.length+')\'">'+t('Show all')+' ('+ids.length+')</button>':'')}
function newsBlock(p){var n=p.news;if(!n)return'<span class="none">'+t('No news on record')+'</span>';var TH=ORG.news_themes||{},ar=LANG==='ar';
  var labs=(n.themes||[]).map(function(k){var o=TH[k]||{};return'<span class="eh-chip grey">'+esc(ar?(o.ar||k):(o.en||k))+'</span>'}).join(' ');
  var h='<div class="nw-g"><div class="nw-t">'+t('Named in the news')+' <span class="n">'+n.mentions.length+'</span></div><div class="nw-s">'+t('News, regulatory releases, Vision 2030 projects and PIF strategy lines that name this organisation.')+'</div>'+
    (n.mentions.length?newsList(n.mentions,p,'m',true):'<span class="none">'+t('No item in News & Intelligence names this organisation')+'</span>')+'</div>';
  h+='<div class="nw-g"><div class="nw-t">'+t('Sector context')+' <span class="n">'+n.context.length+'</span></div>';
  if(!n.eligible)h+='<div class="nw-s">'+t('Sector context is shown for tender clients, EH clients and Tier 1–2 organisations only.')+'</div>';
  else if(!n.themes.length)h+='<span class="none">'+t('No sector on record for this organisation, so no sector context is shown')+'</span>';
  else h+='<div class="nw-s">'+t('Not about this organisation by name — news and Vision 2030 projects in its sector:')+' '+labs+'</div>'+(n.context.length?newsList(n.context,p,'c',false):'<span class="none">'+t('No news on record for this sector')+'</span>');
  h+='</div><div class="nw-cap">'+t('Taken from the News & Intelligence pages as published: the news briefing, Regulatory news, the Vision 2030 dashboard and the PIF Strategy 2026–2030 page. Arabic news headlines are EH translations; regulatory headlines stay in the language of the source.')+'</div>';
  return h}
'''
ok.append(rep('page', "function renderProf(){var p=SEL,el=document.getElementById('prof');", NEWS_JS + "function renderProf(){var p=SEL,el=document.getElementById('prof');",
 'org-news', 'newsRow / newsList / newsBlock: renders mentions and sector context, five rows then "Show all"'))

# ---- 4. the card, between Government tenders and Notes and evidence
ok.append(rep('page', "  h+='<div class=\"card\"><h2>'+t('Notes and evidence')+'</h2>'",
 "  h+='<div class=\"card\"><h2>'+t('News & Vision 2030')+(p.news?' <span class=\"n\">'+(p.news.mentions.length+p.news.context.length)+'</span>':'')+'</h2>'+newsBlock(p)+'</div>';\n"
 "  h+='<div class=\"card\"><h2>'+t('Notes and evidence')+'</h2>'",
 'org-news', 'New card placed after Government tenders (Etimad) and before Notes and evidence'))

# ---- 5. module docstring
ok.append(rep('page', "client ledger, licence, Etimad, notes.", "client ledger, licence, Etimad, news & Vision 2030 (from build_org_news.py), notes.",
 'org-news', 'Docstring lists the new section'))

# ---- 6. workflow: run after the Regulatory news feed is in place, then render the page again
ok.append(rep('wf', "      # ---------- What's New: previous dataset snapshot (artefact of the last successful run) ----------",
 "      # ---------- Organisations view: News & Vision 2030 section (10 Nov 2026). Runs here because it needs the Regulatory news feed restored\n"
 "      #            just above; the page built earlier stays in place if this step fails (it then shows \"No news on record\"). ----------\n"
 "      - name: Add News & Vision 2030 to the Organisations view\n"
 "        run: |\n"
 "          if python pipeline/build_org_news.py --profiles pipeline/org_profiles.json --gov site/gov_news.json --report pipeline/org_news_report.json; then\n"
 "            python pipeline/build_org_page.py pipeline/org_profiles.json site/organisations.html\n"
 "          else echo \"::warning::organisation news step failed — the Organisations page is published without the news section\"; fi\n\n"
 "      - name: Keep the organisation-news match report (which item was linked to which organisation, and why)\n"
 "        uses: actions/upload-artifact@v4\n"
 "        continue-on-error: true\n"
 "        with:\n"
 "          name: org-news-report\n"
 "          path: pipeline/org_news_report.json\n"
 "          retention-days: 30\n"
 "          overwrite: true\n\n"
 "      # ---------- What's New: previous dataset snapshot (artefact of the last successful run) ----------",
 'org-news', 'Workflow step: build_org_news.py after the gov-news feed, re-render organisations.html, keep the match report'))

if not all(ok): sys.exit('ANCHOR MISMATCH — nothing written')
for path, alias in ((PAGE, 'page'), (WF, 'wf')): open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_org_news'), 'Change table — Organisations view: News & Vision 2030 section (10 Nov 2026)')
print('applied')
