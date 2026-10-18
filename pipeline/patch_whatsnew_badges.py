"""patch_whatsnew_badges.py — What's New shows where the updates are (18 Oct 2026).

  • A count badge on each section tab — Fixes & features, Companies, Bids & Clients, Sources — for the week shown.
  • Fixes & features is grouped under a heading per part of the hub (Hub, Stakeholder Map, Bids, Clients, News), each
    with its count, so you can see at a glance which app changed.
  • Companies: "Added" is split by category (competitors, government, collaborators…) with a count each, category names
    in Arabic when the hub is in Arabic; merged records are counted once (under Merged); every heading carries a badge.
  • Bids & Clients: Won / Lost headings carry counts; the tab badge counts new tenders, new and lapsed clients, wins
    and losses. Sources: the badge counts sources refreshed during the week.
  • The week chip now totals exactly what the three update tabs show (sources excluded).
Run once: python3 pipeline/patch_whatsnew_badges.py
"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P = os.path.join(HERE, '..', 'hub', 'EH_Hub.html')
if 'function wnCounts(' in open(P, encoding='utf-8').read(): sys.exit('Already applied — nothing to do.')
load(P, 'hub')

for k in ('fixes', 'companies', 'bids', 'sources'):
    lbl = {'fixes': ('Fixes &amp; features', 'الإصلاحات والميزات'), 'companies': ('Companies', 'الشركات'),
           'bids': ('Bids &amp; Clients', 'المنافسات والعملاء'), 'sources': ('Sources', 'المصادر')}[k]
    span = f'<span class="tl" data-en="{lbl[0]}" data-ar="{lbl[1]}">{lbl[0]}</span></button>'
    rep('hub', f'onclick="wnTab(\'{k}\')">' + span, f'onclick="wnTab(\'{k}\')">' + span.replace('</button>', f'<span class="wnc" data-c="{k}" dir="ltr" hidden></span></button>'),
        'tabs', f'Count badge on the {k} tab')

rep('hub', ".wntab{color:var(--eh-ink-2)}.wntab[aria-selected=\"true\"]{color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}",
    ".wntab{color:var(--eh-ink-2)}.wntab[aria-selected=\"true\"]{color:var(--eh-ink);box-shadow:inset 0 -3px 0 var(--eh-sea)}\n"
    ".wnc{display:inline-block;min-width:18px;height:18px;line-height:18px;padding:0 5px;border-radius:9px;background:var(--eh-good-bg);color:var(--eh-good);font-size:10.5px;font-weight:800;text-align:center;margin-inline-start:6px;vertical-align:1px;box-sizing:border-box}"
    ".wnc[hidden]{display:none}.wntab[aria-selected=\"true\"] .wnc{background:var(--eh-sea);color:#fff}"
    "body.dark .wnc{background:rgba(43,174,104,.22);color:#8FE0B4}body.dark .wntab[aria-selected=\"true\"] .wnc{background:var(--eh-sea);color:#fff}"
    ".wntab{flex:1 1 auto;white-space:nowrap;padding-inline:8px}.wntabs{overflow-x:auto;scrollbar-width:none}.wnweek .n{padding:0 5px;box-sizing:border-box;min-width:18px;height:18px;line-height:18px}.wnh .wnc{vertical-align:0}.wnh.wnsub{font-size:11.5px;margin:8px 0 2px;font-weight:700}",
    'style', 'Badge style (light and dark), sub-heading style')

rep('hub', "function wnCount(w){var d=w.data||{};return (w.fixes||[]).length+(d.added||[]).length+(d.removed||[]).length+(d.merged||[]).length+(d.confidence_up||[]).length+(d.tier_moves||[]).length+((d.bids||{}).won||[]).length+((d.bids||{}).lost||[]).length;}",
    "function wnCounts(w){var d=w.data||{},b=d.bids||{},c=d.clients||{},num=function(x){return typeof x==='number'?x:(x&&x.length)||0;};\n"
    "  var src=(w.sources||[]).filter(function(s){var r=String(s.refreshed||'').slice(0,10);return r&&r>=w.from&&r<=w.to;}).length;\n"
    "  return {fixes:(w.fixes||[]).length, companies:(d.added||[]).length+(d.removed||[]).filter(function(x){return !(x.reason==='merged');}).length+(d.merged||[]).length+(d.confidence_up||[]).length+(d.tier_moves||[]).length,\n"
    "          bids:num(b.new)+num(c.new)+num(c.lost)+(b.won||[]).length+(b.lost||[]).length, sources:src};}\n"
    "function wnCount(w){var c=wnCounts(w);return c.fixes+c.companies+c.bids;}\n"
    "function wnTabCounts(){var w=WN&&WN.weeks[wnWeek],c=w?wnCounts(w):{};document.querySelectorAll('.wnc[data-c]').forEach(function(s){var n=c[s.dataset.c]||0;s.textContent=n;s.hidden=!n;});}\n"
    "function wnBdg(n){return n?' <span class=\"wnc\" dir=\"ltr\">'+n+'</span>':'';}",
    'counts', 'One count per tab; the week chip totals the three update tabs')

rep('hub', "\n  wnRenderBody(); }\n", "\n  wnTabCounts(); wnRenderBody(); }\n", 'counts', 'Refresh tab badges whenever the week changes')

rep('hub', """    h=(w.fixes||[]).map(function(f,i){return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\\''+wnEsc(f.app)+'\\','+i+')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \\u203a '+wnEsc(viewName(f.view)):'')+'</button><br>'+wnEsc(hubL==='ar'?(f.ar||f.en):(f.en||f.ar))+'</div>';}).join('')""",
    """    var fx=(w.fixes||[]).map(function(f,i){return {f:f,i:i};}), order=['hub','stake','bids','clients','news'], grp={};
    fx.forEach(function(x){var a=APPS[x.f.app]?x.f.app:'hub';(grp[a]=grp[a]||[]).push(x);});
    Object.keys(grp).forEach(function(a){if(order.indexOf(a)<0)order.push(a);});
    h=order.filter(function(a){return grp[a];}).map(function(a){return '<div class="wnh">'+wnEsc(appName(a))+wnBdg(grp[a].length)+'</div>'+grp[a].map(function(x){var f=x.f,i=x.i;return '<div class="wnitem '+wnEsc(f.severity||'')+'"><button class="lnk app" onclick="wnGoApp(\\''+wnEsc(f.app)+'\\','+i+')">'+wnEsc(appName(f.app))+(f.view&&f.view!==f.severity?' \\u203a '+wnEsc(viewName(f.view)):'')+'</button><br>'+wnEsc(hubL==='ar'?(f.ar||f.en):(f.en||f.ar))+'</div>';}).join('');}).join('')""",
    'fixes', 'Fixes grouped by part of the hub, each heading with a count')

rep('hub', """    function sec(title,items,fn){ if(!items||!items.length)return ''; return '<div class="wnh">'+title+' \\u00b7 <span dir="ltr">'+items.length+'</span></div>'+items.map(fn).join(''); }
    h+=sec(L('Added','أُضيفت'),d.added,function(x){return '<div class="wnitem data">'+coLink(x.n)+(x.typ?' \\u00b7 '+wnEsc(x.typ):'')+(x.cat?' \\u00b7 '+wnEsc(x.cat):'')+'</div>';});""",
    """    function sec(title,items,fn,cls){ if(!items||!items.length)return ''; return '<div class="wnh'+(cls?' '+cls:'')+'">'+title+wnBdg(items.length)+'</div>'+items.map(fn).join(''); }
    var CATAR={'Active Competitors':'منافسون نشطون','Direct Competitors':'منافسون مباشرون','Indirect / Adjacent Competitors':'منافسون غير مباشرون / مجاورون','EH Clients':'عملاء آفاق البيئة','Clients / Potential Clients':'عملاء / عملاء محتملون','Government Clients & Institutions':'جهات وعملاء حكوميون','Regulators & Compliance Bodies':'الجهات التنظيمية والرقابية','Potential Collaborators':'شركاء محتملون','Suppliers / Subcontractors':'موردون / مقاولون من الباطن','EH Partners':'شركاء آفاق البيئة','Industry Associations & Academia':'جمعيات صناعية وجهات أكاديمية'};
    var catName=function(k){return hubL==='ar'?(CATAR[k]||k):k;};
    var addRow=function(x){return '<div class="wnitem data">'+coLink(x.n)+(x.typ?' \\u00b7 '+wnEsc(x.typ):'')+'</div>';};
    if((d.added||[]).length){ var byCat={}; d.added.forEach(function(x){var k=x.cat||L('Other','أخرى');(byCat[k]=byCat[k]||[]).push(x);});
      h+='<div class="wnh">'+L('Added','أُضيفت')+wnBdg(d.added.length)+'</div>';
      Object.keys(byCat).sort(function(a,b){var ca=/compet/i.test(a)?0:1,cb=/compet/i.test(b)?0:1;return ca-cb||byCat[b].length-byCat[a].length;}).forEach(function(k){h+=sec(wnEsc(catName(k)),byCat[k],addRow,'wnsub');}); }""",
    'companies', 'Added split by category (competitors first), each with a count')

rep('hub', """    h+=sec(L('Removed','أُزيلت'),d.removed,function(x){""",
    """    var rmFn=function(x){""", 'companies', 'Removed rows rendered by a shared function')
rep('hub', """(x.reason?' \\u00b7 '+wnEsc(x.reason):'')+'</div>';});
    h+=sec(L('Data confidence raised'""",
    """(x.reason&&x.reason!=='merged'?' \\u00b7 '+wnEsc(x.reason):'')+'</div>';};
    var rmM=(d.removed||[]).filter(function(x){return x.reason==='merged'||x.alias;}), rmO=(d.removed||[]).filter(function(x){return !(x.reason==='merged'||x.alias);});
    h+=sec(L('Removed from the map','حُذفت من الخريطة'),rmO,rmFn);
    if(!(d.merged||[]).length) h+=sec(L('Merged into another record','دُمجت في سجل آخر'),rmM,rmFn);
    h+=sec(L('Data confidence raised'""",
    'companies', 'Removed split into merged vs removed, each with a count')

rep('hub', """    if((b.won||[]).length) h+='<div class="wnh">'+L('Won','فاز EH')+'</div>'""",
    """    if((b.won||[]).length) h+='<div class="wnh">'+L('Won','فاز EH')+wnBdg(b.won.length)+'</div>'""", 'bids', 'Won heading count')
rep('hub', """    if((b.lost||[]).length) h+='<div class="wnh">'+L('Lost','خسارة')+'</div>'""",
    """    if((b.lost||[]).length) h+='<div class="wnh">'+L('Lost','خسارة')+wnBdg(b.lost.length)+'</div>'""", 'bids', 'Lost heading count')
rep('hub', """    h=(w.sources||[]).map(function(x){var nt""",
    """    var srcN=wnCounts(w).sources; h=((w.sources||[]).length?'<div class="wnh">'+L('Refreshed this week','حُدّثت هذا الأسبوع')+wnBdg(srcN)+' \\u00b7 '+L('of','من')+' <span dir="ltr">'+w.sources.length+'</span> '+L('sources','مصادر')+'</div>':'')+(w.sources||[]).map(function(x){var nt""",
    'sources', 'Sources heading: how many were refreshed this week')

if not FAILURES:
    shutil.copy2(P, os.path.join(HERE, 'EH_Hub.html.pre-wnbadges.bak'))
    open(P, 'w', encoding='utf-8').write(FILES['hub'])
write_change_table(os.path.join(HERE, 'change_table_whatsnew_badges'), "Change table — hub: What's New count badges per tab and heading")
print('failures:', len(FAILURES)); [print('FAIL', f) for f in FAILURES]; sys.exit(1 if FAILURES else 0)
