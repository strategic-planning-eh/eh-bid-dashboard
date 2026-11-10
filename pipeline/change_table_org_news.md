# Change table — Organisations view: News & Vision 2030 section (10 Nov 2026)

Generated 2026-11-10 11:06 · 6 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | page | exact | org-news | Styles for the News & Vision 2030 card | 1 | ✓ |
| 2 | page | exact | org-news | Arabic labels for the News & Vision 2030 card | 1 | ✓ |
| 3 | page | exact | org-news | newsRow / newsList / newsBlock: renders mentions and sector context, five rows then "Show all" | 1 | ✓ |
| 4 | page | exact | org-news | New card placed after Government tenders (Etimad) and before Notes and evidence | 1 | ✓ |
| 5 | page | exact | org-news | Docstring lists the new section | 1 | ✓ |
| 6 | wf | exact | org-news | Workflow step: build_org_news.py after the gov-news feed, re-render organisations.html, keep the match report | 1 | ✓ |

## Edit detail

### 1. page — Styles for the News & Vision 2030 card

**Old**
```
.notes{white-space:pre-wrap;font-size:13px;color:var(--eh-ink-2);line-height:1.6}
```
**New**
```
.notes{white-space:pre-wrap;font-size:13px;color:var(--eh-ink-2);line-height:1.6}
.nw-g{margin-top:18px}.nw-g:first-child{margin-top:0}
.nw-t{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 10px;font-weight:700;font-size:13.5px;color:var(--eh-deep)}html.dark .nw-t{color:var(--eh-ink)}
.nw-t .n{font-weight:600;font-size:12px;color:var(--eh-ink-3)}
.nw-s{font-size:12.5px;color:var(--eh-ink-
```

### 2. page — Arabic labels for the News & Vision 2030 card

**Old**
```
 'Tier':'التصنيف','map':'خريطة','SAR':'ريال',
```
**New**
```
 'News & Vision 2030':'الأخبار ورؤية 2030','Named in the news':'ورد اسمها في الأخبار','Sector context':'سياق القطاع',
 'News, regulatory releases, Vision 2030 projects and PIF strategy lines that name this organisation.':'أخبار وإعلانات تنظيمية ومشاريع رؤية 2030 وبنود من استراتيجية صندوق الاستثمارات العامة ورد فيها اسم هذه المنظمة.',
 'Not about this organisation by name — news and Vision 2030 pro
```

### 3. page — newsRow / newsList / newsBlock: renders mentions and sector context, five rows then "Show all"

**Old**
```
function renderProf(){var p=SEL,el=document.getElementById('prof');
```
**New**
```
var NIDX={};(ORG.news_items||[]).forEach(function(x){NIDX[x.id]=x});
var NSRC={news:['News briefing','blue'],reg:['Regulatory news','green'],v2030:['Vision 2030 project','grey'],pif:['PIF Strategy 2026–2030','grey']};
function newsRow(id,p,i){var x=NIDX[id];if(!x)return'';var ar=LANG==='ar',head=ar?(x.ar||x.en):(x.en||x.ar),why=ar?(x.why_ar||''):(x.why_en||''),who=ar?(x.who_ar||x.who||''):(x.who||
```

### 4. page — New card placed after Government tenders (Etimad) and before Notes and evidence

**Old**
```
  h+='<div class="card"><h2>'+t('Notes and evidence')+'</h2>'
```
**New**
```
  h+='<div class="card"><h2>'+t('News & Vision 2030')+(p.news?' <span class="n">'+(p.news.mentions.length+p.news.context.length)+'</span>':'')+'</h2>'+newsBlock(p)+'</div>';
  h+='<div class="card"><h2>'+t('Notes and evidence')+'</h2>'
```

### 5. page — Docstring lists the new section

**Old**
```
client ledger, licence, Etimad, notes.
```
**New**
```
client ledger, licence, Etimad, news & Vision 2030 (from build_org_news.py), notes.
```

### 6. wf — Workflow step: build_org_news.py after the gov-news feed, re-render organisations.html, keep the match report

**Old**
```
      # ---------- What's New: previous dataset snapshot (artefact of the last successful run) ----------
```
**New**
```
      # ---------- Organisations view: News & Vision 2030 section (10 Nov 2026). Runs here because it needs the Regulatory news feed restored
      #            just above; the page built earlier stays in place if this step fails (it then shows "No news on record"). ----------
      - name: Add News & Vision 2030 to the Organisations view
        run: |
          if python pipeline/build_org_news.
```
