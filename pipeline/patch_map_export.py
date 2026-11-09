"""patch_map_export.py — Stakeholder Map: "Export to Excel" of whatever is currently filtered (9 Nov 2026).

Youssef: "in the stakeholder map, can we add an export to xlsx in whatever list of clients or filters added?"

- Header button "Export to Excel" (EN/AR) and a matching button on the List View count line. Both export VIS —
  the rows passing the current filters (category chips, company type, region, tier, licence, bid flag, search …) —
  so the file is exactly what the user sees, in whatever tab.
- The workbook has three sheets: Stakeholders (28 columns: identity, tier/score, confidence, bids, EH client value,
  MWAN licence expiry/activities/cities, flags, notes), Filters (every active filter and its value, row count,
  date, language) and README. Column headers follow the page language.
- The Saudi Map's own export bar gains an Excel option using the same writer on its own filtered features.
- SheetJS (xlsx 0.18.5) is loaded from cdnjs on first use, like Leaflet is; if it cannot load, the button falls
  back to the existing CSV writer and says so.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, write_change_table, css_min

M = os.path.join(os.path.dirname(HERE), 'hub', 'EH_Stakeholder_Map_CURRENT.html'); load(M, 'map')
if 'exportXlsx' in FILES['map']: sys.exit('Already applied.')
ok = []

CSS = css_min("""<style id="eh-map-export">
/* 9 Nov 2026: Export to Excel */
#xlsBtn svg,.lxls svg{width:14px;height:14px;vertical-align:-2px;margin-inline-end:5px}
.lcount .lxls{margin-inline-start:12px;padding:3px 10px;font-size:12px;vertical-align:middle}
#xlsBtn[disabled],.lxls[disabled]{opacity:.55;cursor:progress}
</style></head>""")
ok.append(rep('map', '</head>', CSS, 'map-export', 'CSS: export buttons'))

ICON = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg>'
ok.append(rep('map', '    <button class="btn" onclick="resetFilters()">Reset filters</button>\n    <button class="btn" id="langBtn"',
              '    <button class="btn" onclick="resetFilters()">Reset filters</button>\n    <button class="btn" id="xlsBtn" type="button" onclick="exportXlsx(\'list\')" title="Download the companies currently shown as an Excel workbook">' + ICON + '<span class="tr">Export to Excel</span></button>\n    <button class="btn" id="langBtn"',
              'map-export', 'Header: Export to Excel button'))
ok.append(rep('map', "const STATIC_TR=[", "const STATIC_TR=[['Export to Excel','\\u062a\\u0635\\u062f\\u064a\\u0631 \\u0625\\u0644\\u0649 Excel'],", 'map-export', 'STATIC_TR: Export to Excel'))

# List View count line gets its own button
ok.append(rep('map', "click any row for detail · click a column to re-sort','<b>'+rows.length.toLocaleString()+'</b> شركة معروضة — ",
              "click any row for detail · click a column to re-sort','<b>'+rows.length.toLocaleString()+'</b> شركة معروضة — ", 'map-export', 'anchor check'))
ok.append(rep('map', "  const lv=document.getElementById('listView'); lv.innerHTML=h;",
              "  h=h.replace('</div><table class=\"ltbl\">','<button type=\"button\" class=\"btn lxls\" onclick=\"exportXlsx(\\'list\\')\">" + ICON.replace('"', '\\"') + "'+t('Export to Excel','تصدير إلى Excel')+'</button></div><table class=\"ltbl\">');\n  const lv=document.getElementById('listView'); lv.innerHTML=h;",
              'map-export', 'List View: Export to Excel button on the count line'))

JS = r"""
// ---- Export to Excel (9 Nov 2026): the rows passing the current filters, in whatever tab ----
var XLSX_URL='vendor/xlsx.full.min.js'; /* vendored in hub/vendor (published to site/vendor) like chart.js; cdnjs fallback below */
var XLSX_CDN='https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
function ldXlsx(ok,bad){ if(window.XLSX)return ok(); var s=document.createElement('script'); s.src=XLSX_URL; s.onload=ok; s.onerror=function(){var c=document.createElement('script'); c.src=XLSX_CDN; c.onload=ok; c.onerror=bad; document.head.appendChild(c);}; document.head.appendChild(s); }
function xlsFilters(){
  var f=[]; var S=state;
  if(S.q)f.push([t('Search','بحث'),S.q]);
  if(S.catg&&S.catg.size)f.push([t('Stakeholder category','فئة الطرف'),Array.from(S.catg).map(catS).join(' · ')]);
  var allTyp=(typeof CATS!=='undefined')?CATS.length:0;
  if(S.cats&&S.cats.size&&(!allTyp||S.cats.size<allTyp))f.push([t('Company type','نوع الشركة'),Array.from(S.cats).map(catL).join(' · ')]);
  if(S.regs&&S.regs.size)f.push([t('Region','المنطقة'),Array.from(S.regs).map(regL).join(' · ')]);
  if(S.tiers&&S.tiers.size)f.push([t('Tier','الفئة'),Array.from(S.tiers).map(tierL).join(' · ')]);
  if(S.type)f.push([t('Company type (dropdown)','نوع الشركة (قائمة)'),catL(S.type)]);
  if(S.sector)f.push([t('Sector','القطاع'),S.sector]);
  if(S.lic)f.push([t('Licence activity','نشاط الترخيص'),S.lic]);
  if(S.bid)f.push([t('Bid against EH only','المتقدمون ضد EH فقط'),t('Yes','نعم')]);
  if(S.freqs&&S.freqs.size)f.push([t('Bid frequency','تكرار العطاءات'),Array.from(S.freqs).join(' · ')]);
  if(S.t1)f.push([t('Tier 1 only','الفئة 1 فقط'),t('Yes','نعم')]);
  if(S.sites>0)f.push([t('Minimum sites','الحد الأدنى للمواقع'),S.sites]);
  return f;
}
function xlsCols(){
  var Y=t('Yes','نعم'),N=t('No','لا'), yn=function(b){return b?Y:N;}, j=function(a){return (a&&a.length)?a.join(' | '):'';};
  return [
    [t('Company','الشركة'),function(n){return n.n;}],
    [t('Category','الفئة'),function(n){return catS(n.cat);}],
    [t('Tier','الفئة (م)'),function(n){return tierL(n.tier)||'';}],
    [t('Company type','نوع الشركة'),function(n){return n.typ?catL(n.typ):'';}],
    [t('Region','المنطقة'),function(n){return (n.rg&&n.rg!=='—')?regL(n.rg):'';}],
    [t('City','المدينة'),function(n){return n.city||'';}],
    [t('Score (v2)','الدرجة (v2)'),function(n){return n.sc==null?'':Math.round(n.sc*10)/10;}],
    [t('Capability','القدرة'),function(n){return n.cap==null?'':n.cap;}],
    [t('Strategic backing','الدعم الاستراتيجي'),function(n){return n.bk||0;}],
    [t('Score driver','محرّك الدرجة'),function(n){return n.drv||'';}],
    [t('Score status','حالة الدرجة'),function(n){return n.fl?t('Floored (low confidence)','مُثبَّتة عند الحد الأدنى (ثقة منخفضة)'):(n.pend?t('Analyst score retained','درجة المحلل محفوظة'):'');}],
    [t('Threat','التهديد'),function(n){return n.threat||'';}],
    [t('Confidence','الثقة'),function(n){return n.cf||'';}],
    [t('Confidence basis','أساس الثقة'),function(n){return n.cf_basis||'';}],
    [t('Bid against EH','تقدّم ضد EH'),function(n){return yn(n.bid);}],
    [t('Bid encounters','مواجهات العطاءات'),function(n){return n.bc||0;}],
    [t('Beat EH (count)','فاز على EH (عدد)'),function(n){return n.h2h&&n.h2h.wins!=null?n.h2h.wins:'';}],
    [t('Priced below EH (count)','سعّر دون EH (عدد)'),function(n){return n.h2h&&n.h2h.undercut!=null?n.h2h.undercut:'';}],
    [t('EH client','عميل EH'),function(n){return yn(n.cat==='EH Clients'||(n.cl&&n.cl.val!=null));}],
    [t('Client value (SAR)','قيمة العميل (ريال)'),function(n){return (n.cl&&n.cl.val!=null)?n.cl.val:'';}],
    [t('MWAN licence expiry','انتهاء ترخيص موان'),function(n){return n.mw&&n.mw.exp?n.mw.exp:'';}],
    [t('Days to expiry','أيام حتى الانتهاء'),function(n){return n.mw&&n.mw.days!=null?n.mw.days:'';}],
    [t('Licence activities','أنشطة الترخيص'),function(n){return n.act||'';}],
    [t('Licensed titles','عناوين التراخيص'),function(n){return n.mw?j(n.mw.lic):'';}],
    [t('Licensed cities','المدن المرخّصة'),function(n){return n.mw?j(n.mw.cities):'';}],
    [t('Sites','المواقع'),function(n){return n.sites==null?'':n.sites;}],
    [t('Sector','القطاع'),function(n){return n.sec||'';}],
    [t('Multinational','متعددة الجنسيات'),function(n){return yn(n.mn);}],
    [t('Megaprojects','مشاريع كبرى'),function(n){return yn(n.mp);}],
    [t('Collaboration potential','إمكانية تعاون'),function(n){return yn(n.collab);}],
    [t('Notes','ملاحظات'),function(n){return n.notes||'';}]
  ];
}
function xlsWrite(rows,cols,filters,fn,scopeLabel){
  var hdr=cols.map(function(c){return c[0];});
  var aoa=[hdr].concat(rows.map(function(n){return cols.map(function(c){var v=c[1](n);return v==null?'':v;});}));
  var ws=XLSX.utils.aoa_to_sheet(aoa);
  ws['!cols']=cols.map(function(c){var w=String(c[0]).length+2;return {wch:Math.min(Math.max(w,10),c[0]===t('Company','الشركة')?44:(c[0]===t('Notes','ملاحظات')?60:28))};});
  ws['!autofilter']={ref:XLSX.utils.encode_range({s:{r:0,c:0},e:{r:aoa.length-1,c:hdr.length-1}})};
  ws['!freeze']={xSplit:1,ySplit:1}; if(LNG==='ar')ws['!views']=[{rightToLeft:true}];
  var now=new Date(); var stamp='';try{for(var i=0;i<NODES.length&&!stamp;i++){var mm=/tracker as of ([^)]+)\)/.exec(NODES[i].notes||'');if(mm)stamp=t('bid tracker as of ','جدول المنافسات حتى ')+mm[1];}}catch(e){}
  var fr=[[t('Filter','المرشّح'),t('Value','القيمة')]].concat(filters.length?filters:[[t('(no filters — all rows)','(لا مرشّحات — كل الصفوف)'),'']]);
  fr.push(['','']); fr.push([t('Rows exported','الصفوف المصدَّرة'),rows.length]); fr.push([t('Scope','النطاق'),scopeLabel]);
  fr.push([t('Exported on','تاريخ التصدير'),now.toISOString().slice(0,16).replace('T',' ')+' UTC']); fr.push([t('Language','اللغة'),LNG==='ar'?'العربية':'English']);
  if(stamp)fr.push([t('Data as of','البيانات حتى'),stamp]);
  var wf=XLSX.utils.aoa_to_sheet(fr); wf['!cols']=[{wch:30},{wch:70}]; if(LNG==='ar')wf['!views']=[{rightToLeft:true}];
  var rd=[[t('EH Stakeholder & Competitive Map — export','خريطة أصحاب المصلحة والمنافسة لآفاق البيئة — تصدير')],
          [t('This file holds exactly the companies that were visible on the map when it was exported, with the filters listed on the Filters sheet.','يحتوي هذا الملف على الشركات التي كانت ظاهرة على الخريطة وقت التصدير فقط، مع المرشّحات المذكورة في ورقة المرشّحات.')],
          [t('Score (v2) = capability 0–100 + strategic backing 0–25 + bids-vs-EH +15. Low-confidence rows are floored, never neutral-filled. Bid figures come from the EH bid tracker on each hourly rebuild.','الدرجة (v2) = القدرة 0–100 + الدعم الاستراتيجي 0–25 + التقدّم ضد EH +15. الصفوف منخفضة الثقة مُثبَّتة عند الحد الأدنى. أرقام العطاءات من جدول منافسات EH عند كل إعادة بناء.')],
          [t('The map is the master: edit the source workbook or the pipeline, not this export.','الخريطة هي المرجع: عدّل ملف المصدر أو خط المعالجة لا هذا التصدير.')]];
  var wr=XLSX.utils.aoa_to_sheet(rd); wr['!cols']=[{wch:120}]; if(LNG==='ar')wr['!views']=[{rightToLeft:true}];
  var wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,ws,t('Stakeholders','الأطراف'));
  XLSX.utils.book_append_sheet(wb,wf,t('Filters','المرشّحات'));
  XLSX.utils.book_append_sheet(wb,wr,'README');
  XLSX.writeFile(wb,fn);
}
function exportXlsx(scope){
  var btns=document.querySelectorAll('#xlsBtn,.lxls'); btns.forEach(function(b){b.disabled=true;});
  var done=function(){btns.forEach(function(b){b.disabled=false;});};
  var rows, filters, label;
  if(scope==='leaf'&&typeof LSTAKE!=='undefined'){
    var names={}; LSTAKE.features.filter(function(f){return leafPass(f.properties);}).forEach(function(f){names[f.properties.n]=1;});
    rows=NODES.filter(function(n){return names[n.n];});
    filters=[]; if(LF.prov!=='all')filters.push([t('Province','المنطقة الإدارية'),LF.prov]); var onK=function(o){return o?Object.keys(o).filter(function(k){return o[k];}):null;}, offK=function(o){return o?Object.keys(o).filter(function(k){return !o[k];}):[];}; if(LF.tiers&&offK(LF.tiers).length)filters.push([t('Tier','الفئة'),onK(LF.tiers).map(tierL).join(' · ')]); if(LF.cats&&offK(LF.cats).length)filters.push([t('Category','الفئة'),onK(LF.cats).map(catS).join(' · ')]); if(LF.bidOnly)filters.push([t('Bid against EH only','المتقدمون ضد EH فقط'),t('Yes','نعم')]); if(LF.minSc)filters.push([t('Minimum score','الحد الأدنى للدرجة'),LF.minSc]); if(LF.confs&&offK(LF.confs).length)filters.push([t('Confidence','الثقة'),onK(LF.confs).join(' · ')]);
    label=t('Saudi Map tab (geo-located companies only)','تبويب خريطة السعودية (الشركات ذات الموقع فقط)');
  }else{ rows=VIS.slice(); filters=xlsFilters(); label=t('Current filters','المرشّحات الحالية'); }
  var fn='EH_stakeholders_'+rows.length+'_'+new Date().toISOString().slice(0,10)+'.xlsx';
  ldXlsx(function(){ try{ xlsWrite(rows,xlsCols(),filters,fn,label); }catch(e){ console.error(e); alert(t('Export failed: ','تعذّر التصدير: ')+e.message); } done(); },
         function(){ done(); if(scope==='leaf'){leafExport('csv');} else { xlsCsvFallback(rows); } alert(t('The Excel library could not be loaded (offline or blocked). A CSV file was downloaded instead.','تعذّر تحميل مكتبة Excel (بلا اتصال أو محجوبة). نُزِّل ملف CSV بدلاً منه.')); });
}
function xlsCsvFallback(rows){
  var cols=xlsCols(); var q=function(v){v=(v==null?'':String(v));return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;};
  var out=[cols.map(function(c){return q(c[0]);}).join(',')].concat(rows.map(function(n){return cols.map(function(c){return q(c[1](n));}).join(',');}));
  var blob=new Blob(['﻿'+out.join('\n')],{type:'text/csv;charset=utf-8'}); var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='EH_stakeholders_'+rows.length+'_'+new Date().toISOString().slice(0,10)+'.csv'; a.click(); setTimeout(function(){URL.revokeObjectURL(a.href);},2000);
}
"""
ok.append(rep('map', "function leafExport(kind){", JS.strip('\n') + "\nfunction leafExport(kind){", 'map-export', 'JS: exportXlsx, xlsCols, xlsFilters, xlsWrite, CSV fallback'))

# Saudi Map bar: Excel option
ok.append(rep('map', "<button class=\"leafbtn\" onclick=\"leafExport(\\'geojson\\')\">\\u2b07 GeoJSON</button>",
              "<button class=\"leafbtn\" onclick=\"exportXlsx(\\'leaf\\')\">\\u2b07 Excel</button><button class=\"leafbtn\" onclick=\"leafExport(\\'geojson\\')\">\\u2b07 GeoJSON</button>",
              'map-export', 'Saudi Map bar: Excel export of the geo-filtered set'))

if not all(ok): sys.exit('ANCHOR MISMATCH: ' + str(ok))
open(M, 'w', encoding='utf-8').write(FILES['map'])
write_change_table(os.path.join(HERE, 'change_table_map_export'), 'Change table — Stakeholder Map Export to Excel (9 Nov 2026)'); print('applied')
