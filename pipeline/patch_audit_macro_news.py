"""patch_audit_macro_news.py — audit fixes for the News Intelligence page (hub/eh_news_intelligence.html), 12 Oct 2026,
judge J3, ids macro-01, 02, 03, 07, 09, 15, 16 (empty option only), 17, 20.

What was wrong and what changes:
  • macro-01 — "Items to Watch", Key number column: each item's figure was cut at the first ".", ";" or "(", so decimals
    were lost ("About $5" for $5.3 billion, "about €2" for €2.8 billion) and the oil row showed a 17 July price. The cut
    now happens only at ";", " (" or a full stop that ends a sentence (never between digits), and an item can name its
    own key number — the regional-security item now shows "about $87 (25 August close)".
  • macro-02 — the oil-price card said "Oil price today (Brent, 25/08) ~$91". Brent closed at about $87.1 on 25/08
    (about $92 on 24/08), which is what the Finances page says. The card now reads "Oil price (Brent), close on 25/08
    ~$87"; the Aramco pricing story, the regional-security item and the Arabic report say the same.
  • macro-03 — the Webuild headline gave "over $8 billion" to the two Webuild contracts, which the item itself values at
    about €2.8 billion + €1 billion; the $8.4 billion is all NEOM cancellations. Headline (EN and AR) corrected.
  • macro-07 — Arabic: key-figure notes and the chart note were English; they now carry Arabic twins (data-eh-ar, shown
    by eh-ar-dashboard.js, which also hides the English filter bar and footer in Arabic).
  • macro-09 — charts: the category chart showed only every second label (Chart.js skipped them) and the sector
    doughnut's legend was cut off ("Giga-Project Auth…"). Both are now sorted horizontal bar charts with every label
    shown and a height that grows with the number of bars.
  • macro-15 — counts: "24 organisations covered" counted stories, not organisations (Aramco twice; four or five
    regional themes are not organisations). The card now counts from the stories: organisations and regional themes
    (the "Macro & Security" and "Environment & Marine" groups). The footer said "12 watchlist + 9 national bodies"
    for 24 entities; it now explains the overlap and the others, computed from the lists. "January–March"/"audited Q1
    claims" became "claims from our 19 July report", which is what the fact-check covers.
  • macro-16 — the "Policy frame" period option never matched any story; options with no stories are removed.
    (Whether a story's period follows its start date or its latest update is an owner decision and is unchanged.)
  • macro-17 — the table's Date column sorted the display text; it now sorts by the date behind it.
  • macro-20 — keyboard: story cards, table rows and Items-to-Watch rows can be reached with Tab and opened with Enter
    or Space; the closed story panel is inert, so its hidden close button no longer takes focus. Opening a story moves
    focus to the panel's close button and closing returns it.

Not changed (owner decisions, listed in the report): the $6.5B "new money" figure (macro-10); The Line population and
other cross-page facts (macro-18); the period rule (macro-16).

Exact-string edits; stops if an anchor is missing.   Run once:  python3 pipeline/patch_audit_macro_news.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'eh_news_intelligence.html')
if '"keyNumber"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'news')
R = lambda old, new, cat, note, count=1: rep('news', old, new, cat, note, count)

# ---------------------------------------------------------------- macro-02 oil price
R("then climbed back to about $90–91 by 25 August when the talks failed.\"",
  "then climbed back to about $92 by 24 August when the talks failed, before closing at about $87 on 25 August.\"",
  'copy', 'macro-02: Aramco pricing story — Brent ~$92 on 24/08, ~$87 close on 25/08')
R("World oil price about $90–91 on 25 August.\"", "World oil price about $87 at the close on 25 August (about $92 the day before).\"",
  'copy', 'macro-02: Aramco pricing key numbers')
R("→ about $90–91 (25 August, after talks failed).\",\"partners\":\"Oman",
  "→ about $92 (24 August, after talks failed) → about $87 (25 August close).\",\"keyNumber\":\"Oil price: about $87 (25 August close)\",\"partners\":\"Oman",
  'copy', 'macro-02/01: regional-security oil path and its own key number')
R("{accent:'#dc2626', num:'~$91', lab:'Oil price today (Brent, 25/08)', note:'Was ~$80 in early Aug when peace looked close · rose as talks failed and attacks spread'},",
  "{accent:'#dc2626', num:'~$87', lab:'Oil price (Brent), close on 25/08', note:'About $92 on 24/08 as talks failed · ~$80 in early Aug when peace looked close', "
  "noteAr:'نحو 92 دولارًا في 24/08 مع فشل المحادثات · ونحو 80 دولارًا مطلع أغسطس حين بدا السلام قريبًا'},",
  'copy', 'macro-02: oil card = 25/08 close (~$87), not "today"')
R("ثم عاد إلى 90–91 دولارًا بحلول 25 أغسطس مع فشل المحادثات.",
  "ثم عاد إلى نحو 92 دولارًا بحلول 24 أغسطس مع فشل المحادثات، قبل أن يُغلق عند نحو 87 دولارًا في 25 أغسطس.",
  'copy', 'macro-02: Arabic Aramco pricing story')
R("نفط برنت اليوم <b>~91$</b> (كان ~80$ مطلع أغسطس حين بدا السلام قريبًا، وارتفع مع انهيار المحادثات واتساع الهجمات).",
  "سعر إغلاق برنت في 25/08 <b>~87$</b> (كان ~80$ مطلع أغسطس حين بدا السلام قريبًا، ونحو 92$ في 24/08 مع انهيار المحادثات).",
  'copy', 'macro-02: Arabic summary oil figure')

# ---------------------------------------------------------------- macro-03 Webuild headline
R("\"headline\":\"NEOM cancelled both contracts with Italy's Webuild — over $8 billion of planned construction gone\"",
  "\"headline\":\"NEOM cancelled both contracts with Italy's Webuild (about €3.8 billion) — part of more than $8.4 billion of NEOM construction called off\"",
  'copy', 'macro-03: Webuild headline — €3.8bn of contracts, part of $8.4bn cancelled')
R("نيوم ألغت عقدَي «ويبيلد» الإيطالية كليهما — تبخّر أكثر من 8 مليارات دولار من الإنشاءات المخططة",
  "نيوم ألغت عقدَي «ويبيلد» الإيطالية كليهما (نحو 3.8 مليارات يورو) — ضمن أكثر من 8.4 مليارات دولار من إنشاءات نيوم الملغاة",
  'copy', 'macro-03: Arabic Webuild headline')

# ---------------------------------------------------------------- macro-15 counts + macro-07 Arabic KPI notes
R("const DEAL_FLOW = 6.5; // USD bn, in-window new awards / reported frameworks (see chart foot)",
  "const DEAL_FLOW = 6.5; // USD bn, in-window new awards / reported frameworks (see chart foot)\n"
  "/* audit 12/10 (macro-15): stories about regional themes (not organisations) are told apart by their group */\n"
  "const THEME_GROUPS = ['Macro & Security','Environment & Marine'];\n"
  "const themeCount = DATA.filter(d=>THEME_GROUPS.includes(d.group)).length;\n"
  "const orgCount   = new Set(DATA.filter(d=>!THEME_GROUPS.includes(d.group)).map(d=>d.entity)).size;",
  'code', 'macro-15: organisation and theme counts derived from the stories')
R("{accent:'#2563eb', num:META.monitored_total, lab:'Companies & bodies we track', note:'Our full watchlist of Saudi organisations'},",
  "{accent:'#2563eb', num:META.monitored_total, lab:'Companies & bodies we track', note:'Our full watchlist of Saudi organisations', noteAr:'قائمتنا الكاملة للمنظمات السعودية'},",
  'copy', 'macro-07: Arabic note (watchlist card)')
R("{accent:'#14b8a6', num:verifiedItems, sub:' items', lab:'News stories verified', note:META.verified_entity_count+' organisations covered · '+corpItems+' company / '+govItems+' government'},",
  "{accent:'#14b8a6', num:verifiedItems, sub:' items', subAr:' خبرًا', lab:'News stories verified', note:orgCount+' organisations and '+themeCount+' regional themes · '+corpItems+' company / '+govItems+' government', "
  "noteAr:'الجهات: '+orgCount+' · المحاور الإقليمية: '+themeCount+' · شركات: '+corpItems+' / حكومة: '+govItems},",
  'copy', 'macro-15/07: stories card counts organisations and themes from the data (EN + AR)')
R("{accent:'#ef4444', num:flaggedItems, lab:'🔴 Items to watch', note:'Big projects, infrastructure and security stories'},",
  "{accent:'#ef4444', num:flaggedItems, lab:'🔴 Items to watch', note:'Big projects, infrastructure and security stories', noteAr:'مشاريع كبرى وبنية تحتية وأمن'},",
  'copy', 'macro-07: Arabic note (watch card)')
R("note:'New deals this period (one $5.3 billion item unconfirmed) · cancellations not counted'},",
  "note:'New deals this period (one $5.3 billion item unconfirmed) · cancellations not counted', noteAr:'صفقات جديدة في هذه الفترة (منها بند بقيمة 5.3 مليارات دولار غير مؤكد) · لا تُحتسب الإلغاءات'},",
  'copy', 'macro-07: Arabic note (new-money card)')
R("<div class=\"k-num\">${k.num}${k.sub?`<small>${k.sub}</small>`:''}</div>",
  "<div class=\"k-num\">${k.num}${k.sub?`<small${k.subAr?` data-eh-ar=\"${k.subAr}\"`:''}>${k.sub}</small>`:''}</div>",
  'code', 'macro-07: Arabic unit under the stories count')
R("<div class=\"k-note\">${k.note}</div>",
  "<div class=\"k-note\"${k.noteAr?` data-eh-ar=\"${k.noteAr}\"`:''}>${k.note}</div>",
  'code', 'macro-07: KPI notes carry their Arabic twin')
R("<div class=\"chart-foot\">Note: the $5.3 billion HUMAIN figure",
  "<div class=\"chart-foot\" data-eh-ar=\"ملاحظة: رقم HUMAIN البالغ 5.3 مليارات دولار مصدره تقرير صحفي واحد وغير مؤكد. يحتسب هذا الرسم الصفقات الجديدة المعلنة في الفترة فقط — لا العقود الملغاة ولا البرامج الممتدة ولا نتائج الشركات.\">Note: the $5.3 billion HUMAIN figure",
  'copy', 'macro-07: chart note has an Arabic twin')

# footer
R("(every material January–March claim re-verified, with per-claim verdicts above)",
  "(every material claim from our 19 July report re-verified, with per-claim verdicts above)",
  'copy', 'macro-15: methodology names the report it re-checks (19 July), not "January–March"')
R("""  const pct = Math.round(META.verified_entity_count/META.monitored_total*100);
  document.getElementById('cov-block').innerHTML = `
    <div style="font-size:12.5px;color:var(--ink-soft);margin-top:4px">
      <strong>${META.verified_entity_count}</strong> priority entities verified of <strong>${META.monitored_total}</strong> monitored
      (<strong>${META.on_watchlist_count}</strong> direct watchlist names + ${META.national_bodies.length} governing national bodies & authorities) · ${verifiedItems} developments + ${AUDIT.length} audited Q1 claims + ${CORRECTIONS.length} corrections/resolutions.</div>""",
  """  /* audit 12/10 (macro-15): every count from the lists themselves; overlap and others named so the sum adds up */
  const vN = META.verified_entities.length, wl = new Set(META.on_watchlist), nb = new Set(META.national_bodies);
  const inBoth = META.verified_entities.filter(v=>wl.has(v)&&nb.has(v)), others = META.verified_entities.filter(v=>!wl.has(v)&&!nb.has(v));
  const pct = Math.round(vN/META.monitored_total*100);
  document.getElementById('cov-block').innerHTML = `
    <div style="font-size:12.5px;color:var(--ink-soft);margin-top:4px">
      <strong>${vN}</strong> priority entities verified of <strong>${META.monitored_total}</strong> monitored
      (<strong>${wl.size}</strong> direct watchlist names + ${nb.size} governing national bodies & authorities${inBoth.length?` — ${esc(inBoth.join(', '))} counted in both`:''}${others.length?` — plus ${others.length} others: ${esc(others.join(', '))}`:''}) · ${verifiedItems} developments + ${AUDIT.length} claims from our 19 July report re-checked + ${CORRECTIONS.length} corrections/resolutions.</div>""",
  'copy', 'macro-15: coverage footer arithmetic adds up (overlap and others named); "Q1 claims" → 19 July report')
R("document.getElementById('vsub').textContent = `${META.verified_entity_count} entities",
  "document.getElementById('vsub').textContent = `${vN} entities", 'code', 'macro-15: list count from the list')

# ---------------------------------------------------------------- macro-16 empty period option
R("cats.forEach(c=>cSel.insertAdjacentHTML('beforeend',`<option value=\"${c}\">${c}</option>`));",
  "cats.forEach(c=>cSel.insertAdjacentHTML('beforeend',`<option value=\"${c}\">${c}</option>`));\n"
  "/* audit 12/10 (macro-16): drop period options that no story carries (\"Policy frame\" always returned nothing) */\n"
  "[...document.getElementById('f-period').options].forEach(o=>{ if(o.value!=='all' && !DATA.some(d=>d.period===o.value)) o.remove(); });",
  'code', 'macro-16: period options with no stories removed')

# ---------------------------------------------------------------- macro-17 date sort
R("    if(k==='flagged'){va=a.flagged?1:0; vb=b.flagged?1:0;}",
  "    if(k==='flagged'){va=a.flagged?1:0; vb=b.flagged?1:0;}\n    if(k==='date'){va=a.dateISO; vb=b.dateISO;}   // audit 12/10 (macro-17): sort by the date, not its display text",
  'code', 'macro-17: Date column sorts by dateISO')

# ---------------------------------------------------------------- macro-01 key number
R("const val = (d.financials && !/^not /i.test(d.financials)) ? d.financials.split(/[.;(]/)[0].trim() : 'Not disclosed';",
  "/* audit 12/10 (macro-01): never cut inside a number (\"$5.3\"); an item may name its own key number */\n"
  "    const val = d.keyNumber ? d.keyNumber : (d.financials && !/^not /i.test(d.financials)) ? d.financials.split(/;\\s|\\s\\(|\\.(?=\\s|$)/)[0].trim() : 'Not disclosed';",
  'code', 'macro-01: key number keeps decimals and units')

# ---------------------------------------------------------------- macro-09 charts
R("""const secData=countBy('group');
new Chart(document.getElementById('chartSector'),{
  type:'doughnut',
  data:{labels:secData.map(x=>x[0]), datasets:[{data:secData.map(x=>x[1]), backgroundColor:PALETTE, borderColor:'#fff', borderWidth:2}]},
  options:{cutout:'60%', plugins:{legend:{position:'right', labels:{boxWidth:9, boxHeight:9, usePointStyle:true, pointStyle:'circle', padding:9, font:{size:12}}}}}
});

const catData=countBy('category');
new Chart(document.getElementById('chartCat'),{
  type:'bar',
  data:{labels:catData.map(x=>x[0]), datasets:[{data:catData.map(x=>x[1]), backgroundColor:catData.map(()=>'#0072BB'), borderRadius:4, barThickness:14}]},
  options:{indexAxis:'y', plugins:{legend:{display:false}},
    scales:{x:{beginAtZero:true, reverse:EH_RTL(), ticks:{precision:0, stepSize:1}, grid:{color:'#D9E3DF'}}, y:{position:EH_RTL()?'right':'left', grid:{display:false}, ticks:{font:{size:12}}}}}
});""",
  """/* audit 12/10 (macro-09): both count charts are sorted horizontal bars with every label shown (long ones on two lines);
   the chart grows with the number of bars (the doughnut's legend was cut off, the bar chart skipped half its labels) */
const ehBarBox=(id,n)=>{ const b=document.getElementById(id).parentElement; b.style.height=Math.max(230, n*28+44)+'px'; };
const ehWrap=s=>{ if(s.length<=22) return s; const mid=s.length/2; let k=-1; for(let i=0;i<s.length;i++) if(s[i]===' '&&(k<0||Math.abs(i-mid)<Math.abs(k-mid))) k=i; return k<0?s:[s.slice(0,k),s.slice(k+1)]; };   // long labels on two lines, never cut
const ehCountBar=(id,rows,color)=>{ ehBarBox(id,rows.length); return new Chart(document.getElementById(id),{
  type:'bar',
  data:{labels:rows.map(x=>ehWrap(x[0])), datasets:[{data:rows.map(x=>x[1]), backgroundColor:rows.map(()=>color), borderRadius:4, barThickness:14}]},
  options:{indexAxis:'y', maintainAspectRatio:false, plugins:{legend:{display:false}},
    scales:{x:{beginAtZero:true, reverse:EH_RTL(), ticks:{precision:0, stepSize:1}, grid:{color:'#D9E3DF'}}, y:{position:EH_RTL()?'right':'left', grid:{display:false}, ticks:{autoSkip:false, font:{size:12}}}}}
}); };
const secData=countBy('group');
ehCountBar('chartSector', secData, '#54AB5D');
const catData=countBy('category');
ehCountBar('chartCat', catData, '#0072BB');""",
  'code', 'macro-09: sector and category charts — sorted bars, all labels, height follows bar count')

# ---------------------------------------------------------------- macro-20 keyboard
R("<div class=\"card ${gov?'gov':''}\" data-id=\"${d.id}\">", "<div class=\"card ${gov?'gov':''}\" data-id=\"${d.id}\" tabindex=\"0\" role=\"button\">",
  'code', 'macro-20: story cards focusable')
R("const rows = list.map(d=>`<tr data-id=\"${d.id}\">", "const rows = list.map(d=>`<tr data-id=\"${d.id}\" tabindex=\"0\">",
  'code', 'macro-20: table rows focusable')
R("return `<div class=\"flag-row\" data-id=\"${d.id}\">", "return `<div class=\"flag-row\" data-id=\"${d.id}\" tabindex=\"0\" role=\"button\">",
  'code', 'macro-20: Items-to-Watch rows focusable')
R("<aside class=\"panel\" id=\"panel\" aria-hidden=\"true\" data-eh-noreveal>", "<aside class=\"panel\" id=\"panel\" aria-hidden=\"true\" data-eh-noreveal inert>",
  'code', 'macro-20: closed panel is inert (its close button leaves the Tab order)')
R("  overlay.classList.add('open'); panel.classList.add('open'); panel.setAttribute('aria-hidden','false');\n}\n"
  "function closeDetail(){overlay.classList.remove('open'); panel.classList.remove('open'); panel.setAttribute('aria-hidden','true');}",
  "  if(!panel.classList.contains('open')) ehLastFocus=document.activeElement;\n"
  "  overlay.classList.add('open'); panel.classList.add('open'); panel.setAttribute('aria-hidden','false'); panel.inert=false;\n"
  "  setTimeout(()=>{ try{ document.getElementById('panel-close').focus({preventScroll:true}); }catch(e){} },0);\n}\n"
  "let ehLastFocus=null;\n"
  "function closeDetail(){ const was=panel.classList.contains('open'); overlay.classList.remove('open'); panel.classList.remove('open'); panel.setAttribute('aria-hidden','true'); panel.inert=true;\n"
  "  if(was&&ehLastFocus&&ehLastFocus.isConnected){ try{ ehLastFocus.focus({preventScroll:true}); }catch(e){} } }\n"
  "/* audit 12/10 (macro-20): Enter or Space opens the focused story */\n"
  "document.addEventListener('keydown',e=>{ const t=e.target; if((e.key==='Enter'||e.key===' ')&&t&&t.matches&&t.matches('.card[data-id],table.dt tbody tr[data-id],.flag-row[data-id]')){ e.preventDefault(); openDetail(t.dataset.id); } });",
  'code', 'macro-20: panel focus in/out; Enter/Space opens a story')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['news'])
md, _ = write_change_table(os.path.join(HERE, 'change_table_audit_macro_news'), 'Audit fixes — News Intelligence (macro)')
print('patched news page;', md)
