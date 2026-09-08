/* eh-ar-dashboard.js — v1.0.0 · 2026-09-08
   Makes the Arabic edition of the Fiscal Monitor and the News Intelligence page a dashboard, not a text report (roadmap N1).
   In Arabic mode the KPI cards and charts stay on screen with Arabic labels; the English prose is hidden; the analyst-written
   Arabic report (#ehArView) is split so each chart explainer sits directly under its chart and the rest follows the charts.
   Chart datasets are relabelled through ch.data / ch.config.options (never ch.options — Chart.js v4 proxy lesson).
   Switching back to English restores everything. Loaded after the page's own scripts. */
(function(){
  'use strict';
  var file=(location.pathname.split('/').pop()||'').toLowerCase();
  var PAGE=/fiscal/.test(file)?'fisc':/news_intelligence/.test(file)?'news':null; if(!PAGE)return;
  var $=function(s,r){return (r||document).querySelector(s);}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};

  /* ---------------- dictionaries (EH translations) ---------------- */
  var D={
    fisc:{
      kpi:{'H1 2026 Deficit (official)':'عجز النصف الأول 2026 (رسمي)','Q2 2026 Deficit':'عجز الربع الثاني 2026','Brent — settle 25/08':'برنت — تسوية 25/08','Yanbu Export Share':'حصة ينبع من الصادرات','Saudi Crude Exports (Jun)':'صادرات الخام السعودي (يونيو)','Hormuz Transits':'عبور هرمز','Public Debt (end-H1)':'الدين العام (نهاية النصف الأول)','Reserves (end-June)':'الاحتياطيات (نهاية يونيو)'},
      lbl:{'H1 2025':'النصف الأول 2025','H1 2026':'النصف الأول 2026','Q1 2025':'الربع الأول 2025','Q1 2026':'الربع الأول 2026','FY2026 budget ÷4 (pro-rata quarter)':'موازنة 2026 ÷ 4 (ربع نسبي)','Q1 2026 actual':'الربع الأول 2026 الفعلي','Brent actual (approx., Aug = MTD avg)':'برنت الفعلي (تقريبي، أغسطس = متوسط الشهر حتى تاريخه)','H2 — Base · grinding war ($85–95)':'النصف الثاني — الأساس · حرب مستنزفة (85–95 دولاراً)','H2 — Corridor breach (>$110 spike)':'النصف الثاني — اختراق الممر (قفزة فوق 110 دولارات)','H2 — De-escalation · Hormuz deal ($72–80)':'النصف الثاني — تهدئة · اتفاق هرمز (72–80 دولاراً)','Budget reference ($69.9, FY25 avg)':'مرجع الموازنة (69.9 دولاراً، متوسط 2025)','Official actuals (Q1, H1)':'الفعلي الرسمي (الربع الأول، النصف الأول)','Base · grinding war — FY ~310':'الأساس · حرب مستنزفة — السنة نحو 310','Corridor breach — FY ~355':'اختراق الممر — السنة نحو 355','De-escalation — FY ~275':'تهدئة — السنة نحو 275','Budget target (\u2212165.4)':'مستهدف الموازنة (\u2212165.4)','FY2025 outturn (\u2212276.6)':'نتيجة 2025 (\u2212276.6)','Deficit (SAR bn)':'العجز (مليار ريال)','Ceasefire · 8 Apr':'وقف إطلاق النار · 8 أبريل',
           'Goods & services':'سلع وخدمات','Compensation':'تعويضات العاملين','Capex':'نفقات رأسمالية','Social benefits':'منافع اجتماعية','Subsidies':'دعم','Financing':'تمويل','Grants':'منح','Military & Security':'العسكري والأمن','Health & Social Dev':'الصحة والتنمية الاجتماعية','General Items':'بنود عامة','Education':'التعليم','Regional Admin':'الإدارة الإقليمية','Economic Resources':'الموارد الاقتصادية','Municipal Services':'الخدمات البلدية','Public Admin':'الإدارة العامة','Infra. & Transport':'البنية التحتية والنقل','Q2 2025':'الربع الثاني 2025','Q2 2026':'الربع الثاني 2026','Q1 2026\u2002(actual)':'الربع الأول 2026 (فعلي)','Q2 / H1\u2002(actual)':'الربع الثاني / النصف الأول (فعلي)','Q4 (year-end)':'الربع الرابع (نهاية السنة)','Brent USD / barrel':'برنت — دولار / برميل','Cumulative deficit (SAR billion)':'العجز التراكمي (مليار ريال)','SAR billion (quarter)':'مليار ريال (ربع سنة)','SAR billion (quarterly deficit)':'مليار ريال (عجز فصلي)','SAR billion (half-year)':'مليار ريال (نصف سنة)','Oil revenue':'الإيراد النفطي','Non-oil revenue':'الإيراد غير النفطي','Total revenue':'إجمالي الإيراد','Expenditure':'الإنفاق','Revenue':'الإيراد','Deficit':'العجز','Q1':'الربع الأول','Q2':'الربع الثاني','Q3':'الربع الثالث','Q4':'الربع الرابع','Jan':'يناير','Feb':'فبراير','Mar':'مارس','Apr':'أبريل','May':'مايو','Jun':'يونيو','Jul':'يوليو','Aug':'أغسطس','Sep':'سبتمبر','Oct':'أكتوبر','Nov':'نوفمبر','Dec':'ديسمبر'},
      sec:{'Headline metrics':'المؤشرات الرئيسة','Budget vs. H1 2026 actuals':'الموازنة مقابل النتائج الفعلية للنصف الأول 2026','Full-year 2026 projection':'إسقاط العام الكامل 2026','Scenario analysis — H2 2026 (v4)':'تحليل السيناريوهات — النصف الثاني 2026','Source attribution':'إسناد المصادر','SECTION 02':'القسم 02','SECTION 03':'القسم 03','SECTION 04':'القسم 04','SECTION 05':'القسم 05','SECTION 06':'القسم 06'},
      enOnly:['header#overview','#scenarios','#sources','#kpis .sec-sub','#compare .sec-sub','#projection .sec-sub','#kpis .upd-chip','#compare .upd-chip','#projection .upd-chip','#compare p','#projection p','#compare ul','#projection ul'],
      keepArHead:/^(القسم 0[56])/ , chartPrefix:/^([A-F])\s*·/, chartOf:function(letter){return $('#chart'+letter);},
      after:'#projection'
    },
    news:{
      kpi:{'Companies & bodies we track':'الشركات والجهات التي نتابعها','News stories verified':'أخبار موثّقة','🔴 Items to watch':'🔴 بنود تحت المراقبة','New money announced':'أموال جديدة مُعلنة','Oil price today (Brent, 25/08)':'سعر النفط اليوم (برنت، 25/08)'},
      lbl:{'National Body':'جهة وطنية','Giga-Project Authority':'هيئة مشروع كبير','Petrochemicals':'البتروكيماويات','Macro & Security':'الاقتصاد الكلي والأمن','Energy':'الطاقة','Environment & Marine':'البيئة والبحار','Energy / Utilities (Water)':'الطاقة / المرافق (المياه)','Mining & Minerals':'التعدين والمعادن','Technology / AI':'التقنية / الذكاء الاصطناعي','Environmental Services':'الخدمات البيئية','Security/Disruption Impact':'أثر أمني / تعطّل','Giga-Project Update':'تحديث مشروع كبير','Other':'أخرى','Expansion/Capacity Increase':'توسّع / زيادة طاقة','Contract Award':'ترسية عقد','Policy/Regulatory Change':'تغيير سياسة / تنظيم','Strategic MOU':'مذكرة تفاهم استراتيجية','IPO/Funding Round':'طرح عام / جولة تمويل','New Tender/Procurement':'منافسة / شراء جديد','Environmental Regulation':'تنظيم بيئي','AI & Data Centres (reported)':'الذكاء الاصطناعي ومراكز البيانات (مُبلَّغ)','Water & Desalination':'المياه والتحلية','Tourism & Culture':'السياحة والثقافة','Items':'بنود','Count':'العدد','USD bn':'مليار دولار'},
      chart:{'Verified items by sector':'البنود الموثّقة بحسب القطاع','Verified items by news category':'البنود الموثّقة بحسب فئة الخبر','New money announced, by theme':'الأموال الجديدة المُعلنة بحسب المحور','Distribution of source-verified developments':'توزيع التطورات الموثّقة من المصادر','Across corporate & government':'عبر الشركات والحكومة','In billions of US dollars · new deals announced this period':'بمليارات الدولارات · صفقات جديدة أُعلنت هذه الفترة'},
      sec:{}, enOnly:['#sec-audit','#sec-corp','#sec-gov','#sec-flag','#sec-hl','aside.panel'],
      keepArHead:/./, chartPrefix:null, chartOf:null,
      after:function(){ var c=$('.charts'); return c?c.closest('section'):null; }
    }
  }[PAGE];
  var tr=function(map,s){ if(s==null)return s; if(Array.isArray(s))s=s.join(' '); var k=String(s).replace(/&amp;/g,'&').replace(/\s+/g,' ').trim(); if(map[k]!=null)return map[k]; var k2=k.replace(/\u2212/g,'-'); for(var key in map){ if(key.replace(/\u2212/g,'-')===k2)return map[key]; } return null; };

  /* ---------------- one-time preparation ---------------- */
  var prepared=false, moved=[];
  function prepare(){
    if(prepared)return; prepared=true;
    D.enOnly.forEach(function(sel){ $$(sel).forEach(function(el){ el.classList.add('eh-en-only'); }); });
    /* remember English texts */
    $$('.klabel,.k-lab,.sec-head h2,.sec-num,.chart-card h3,.chart-card .c-sub,.card .chead h3,.card .chead .csub').forEach(function(el){ if(!el.dataset.en)el.dataset.en=el.innerHTML; });
    /* split the Arabic report into blocks and move chart explainers under their charts */
    var ar=$('#ehArView'); if(!ar)return;
    var kids=[].slice.call(ar.children), blocks=[], cur=null;
    kids.forEach(function(k){ if(/^H[23]$/.test(k.tagName)){ cur={head:k,items:[]}; blocks.push(cur); } else if(cur){ cur.items.push(k); } });
    if(D.chartPrefix){
      blocks.forEach(function(b){ var m=b.head.textContent.trim().match(D.chartPrefix); if(!m)return; var cv=D.chartOf(m[1]); if(!cv)return; var card=cv.closest('.chart-card,.card,.cc,.chart')||cv.parentElement.parentElement; $$('.csub,.callout,p',card).forEach(function(x){ if(!x.closest('.eh-ar-cap')) x.classList.add('eh-en-only'); });
        var wrap=document.createElement('div'); wrap.className='eh-ar-cap'; wrap.dir='rtl'; wrap.lang='ar';
        
        b.items.forEach(function(it){ wrap.appendChild(it); }); b.head.remove(); card.appendChild(wrap); moved.push(wrap);
        var t=$('h3',card); if(t){ t.dataset.ar=b.head.textContent.trim(); } var first=$('p',wrap); if(first&&first.textContent.trim().length>400) wrap.classList.add('eh-ar-long'); });
    }
    /* the rest of the report follows the charts */
    var anchor=typeof D.after==='function'?D.after():$(D.after); if(anchor&&anchor.parentNode){ anchor.parentNode.insertBefore(ar,anchor.nextSibling); ar.classList.add('eh-ar-rest'); }
  }

  /* ---------------- chart relabelling ---------------- */
  var chartMemo=[];
  function charts(){ if(!window.Chart||!Chart.getChart)return []; return $$('canvas').map(function(c){return Chart.getChart(c);}).filter(Boolean); }
  function relabelCharts(ar){
    charts().forEach(function(ch){
      var memo=chartMemo.filter(function(m){return m.ch===ch;})[0];
      if(ar){ if(!memo){ memo={ch:ch,labels:ch.data.labels?ch.data.labels.slice():null,ds:ch.data.datasets.map(function(d){return d.label;}),ax:{}}; try{ var sc=ch.config.options.scales||{}; Object.keys(sc).forEach(function(k){ if(sc[k]&&sc[k].title&&sc[k].title.text) memo.ax[k]=sc[k].title.text; }); }catch(e){} chartMemo.push(memo); }
        try{ var sc1=ch.config.options.scales||{}; Object.keys(memo.ax).forEach(function(k){ var t=tr(D.lbl,memo.ax[k]); if(t!=null&&sc1[k]&&sc1[k].title) sc1[k].title.text=t; }); }catch(e){}
        if(ch.data.labels) ch.data.labels=memo.labels.map(function(l){ var t=tr(D.lbl,l); return t!=null?t:l; });
        ch.data.datasets.forEach(function(d,i){ var t=tr(D.lbl,memo.ds[i]); if(t!=null)d.label=t; });
        try{ var o=ch.config.options; if(o&&o.plugins&&o.plugins.legend){ o.plugins.legend.rtl=true; o.plugins.legend.textDirection='rtl'; } }catch(e){}
      } else if(memo){ if(memo.labels) ch.data.labels=memo.labels.slice(); ch.data.datasets.forEach(function(d,i){ d.label=memo.ds[i]; }); try{ var sc2=ch.config.options.scales||{}; Object.keys(memo.ax).forEach(function(k){ if(sc2[k]&&sc2[k].title) sc2[k].title.text=memo.ax[k]; }); }catch(e){} try{ var o2=ch.config.options; if(o2&&o2.plugins&&o2.plugins.legend){ o2.plugins.legend.rtl=false; o2.plugins.legend.textDirection='ltr'; } }catch(e){} }
      try{ ch.update('none'); }catch(e){}
    });
  }

  /* ---------------- apply / restore ---------------- */
  function apply(ar){
    prepare();
    document.documentElement.lang=ar?'ar':'en'; document.documentElement.dir=ar?'rtl':'ltr';
    document.body.classList.toggle('eh-ar-dash',ar);
    $$('.klabel,.k-lab').forEach(function(el){ var t=tr(D.kpi,el.dataset.en); el.innerHTML=ar&&t?t:el.dataset.en; });
    $$('.sec-head h2').forEach(function(el){ var t=tr(D.sec,el.dataset.en.replace(/<[^>]+>/g,'')); el.innerHTML=ar&&t?t:el.dataset.en; });
    $$('.sec-num').forEach(function(el){ var t=tr(D.sec,el.dataset.en); el.innerHTML=ar&&t?t:el.dataset.en; });
    $$('.chart-card h3,.card .chead h3').forEach(function(el){ var t=el.dataset.ar||tr(D.chart||{},el.dataset.en); if(el.dataset.en!=null) el.innerHTML=ar&&t?t:el.dataset.en; });
    $$('.card .chead .csub').forEach(function(el){ if(el.dataset.en!=null) el.innerHTML=el.dataset.en; });
    $$('.chart-card .c-sub').forEach(function(el){ var t=tr(D.chart||{},el.dataset.en); el.innerHTML=ar&&t?t:el.dataset.en; });
    relabelCharts(ar);
    if(window.EH_SHARED&&EH_SHARED.floorText) setTimeout(EH_SHARED.floorText,50);
  }

  /* hook the page's own switch */
  var orig=window.ehSetLang;
  if(typeof orig==='function'){ window.ehSetLang=function(l){ orig.apply(this,arguments); apply(l==='ar'); }; }
  function init(){ if(document.body.classList.contains('ar-mode')) apply(true); }
  if(document.readyState==='complete') setTimeout(init,120); else window.addEventListener('load',function(){ setTimeout(init,120); });
  window.EH_AR_DASH={version:'1.0.0',page:PAGE,apply:apply};
})();
