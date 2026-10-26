# Change table — Organisations view

Generated 2026-10-26 15:21 · 16 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | EH_Hub.html | exact | org-view | Sixth top-level tab after News & Intelligence | 1 | ✓ |
| 2 | EH_Hub.html | exact | org-view | Loading skeleton | 1 | ✓ |
| 3 | EH_Hub.html | exact | org-view | Lazy iframe for the page | 1 | ✓ |
| 4 | EH_Hub.html | exact | org-view | Mobile tab bar button | 1 | ✓ |
| 5 | EH_Hub.html | exact | org-view | Mobile bar grid: five buttons | 1 | ✓ |
| 6 | EH_Hub.html | exact | org-view | Phone bar grid: six buttons | 1 | ✓ |
| 7 | EH_Hub.html | exact | org-view | Footer count (EN) | 1 | ✓ |
| 8 | EH_Hub.html | exact | org-view | Footer count (AR) | 1 | ✓ |
| 9 | EH_Hub.html | exact | org-view | What's New app label | 1 | ✓ |
| 10 | EH_Hub.html | exact | org-view | What's New app → tab | 1 | ✓ |
| 11 | EH_Hub.html | exact | org-view | View aliases for deep links | 1 | ✓ |
| 12 | EH_Hub.html | exact | org-view | Search hits carry an "Open profile" action | 1 | ✓ |
| 13 | EH_Hub.html | exact | org-view | qOrg(): open the Organisations view on a name | 1 | ✓ |
| 14 | update-dashboard.yml | exact | org-view | Pipeline builds and publishes organisations.html | 1 | ✓ |
| 15 | update-dashboard.yml | exact | org-view | Unresolved-names workbook kept with the bid-sync-review artifact | 1 | ✓ |
| 16 | CHANGES.md | exact | org-view | What's New entries for W44 | 1 | ✓ |

## Edit detail

### 1. EH_Hub.html — Sixth top-level tab after News & Intelligence

**Old**
```
data-ar="الأخبار والمستجدات">News &amp; Intelligence</span></button>
  </div></nav>
```
**New**
```
data-ar="الأخبار والمستجدات">News &amp; Intelligence</span></button>
    <button class="tab" role="tab" data-f="orgs" data-t="Organisations" aria-pressed="false" onclick="go(this)" title="One profile per organisation — every tender it asked for, every bid against EH, what EH sells it · ملف لكل منظمة — كل منافسة طرحتها، كل عرض ضد آفاق البيئة، وما تبيعه لها آفاق البيئة"><svg class="ic" aria-hidden="
```

### 2. EH_Hub.html — Loading skeleton

**Old**
```
<div class="skel" id="sk-bubbles">
```
**New**
```
<div class="skel" id="sk-orgs"><div class="in"><div class="spin"></div><span class="tl" data-en="Loading organisations…" data-ar="جارٍ تحميل المنظمات…">Loading organisations…</span></div></div>
  <div class="skel" id="sk-bubbles">
```

### 3. EH_Hub.html — Lazy iframe for the page

**Old**
```
<iframe id="f-bubbles" title="Client portfolio bubble chart" data-src="EH_Client_Bubble_Map_CURRENT.html" loading="lazy"></iframe>
```
**New**
```
<iframe id="f-bubbles" title="Client portfolio bubble chart" data-src="EH_Client_Bubble_Map_CURRENT.html" loading="lazy"></iframe>
  <iframe id="f-orgs" title="Organisations — one profile per client, bidder and competitor" data-src="organisations.html" loading="lazy"></iframe>
```

### 4. EH_Hub.html — Mobile tab bar button

**Old**
```
<span class="tl" data-en="News" data-ar="الأخبار">News</span></button>
</nav>
```
**New**
```
<span class="tl" data-en="News" data-ar="الأخبار">News</span></button>
  <button class="mtab" data-f="orgs" role="tab" onclick="go(document.querySelector('.tab[data-f=orgs]'))"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><p
```

### 5. EH_Hub.html — Mobile bar grid: five buttons

**Old**
```
nav.mtabs{position:sticky;bottom:0;display:grid;grid-template-columns:repeat(4,1fr);
```
**New**
```
nav.mtabs{position:sticky;bottom:0;display:grid;grid-template-columns:repeat(5,1fr);
```

### 6. EH_Hub.html — Phone bar grid: six buttons

**Old**
```
@media(max-width:640px){nav.mtabs{grid-template-columns:repeat(5,1fr)}
```
**New**
```
@media(max-width:640px){nav.mtabs{grid-template-columns:repeat(6,1fr)}
```

### 7. EH_Hub.html — Footer count (EN)

**Old**
```
data-en="Five live views · bids refresh hourly
```
**New**
```
data-en="Six live views · bids refresh hourly
```

### 8. EH_Hub.html — Footer count (AR)

**Old**
```
data-ar="خمس لوحات حيّة · تُحدَّث العطاءات
```
**New**
```
data-ar="ست لوحات حيّة · تُحدَّث العطاءات
```

### 9. EH_Hub.html — What's New app label

**Old**
```
hub:['Hub','المنصة']};
```
**New**
```
hub:['Hub','المنصة'],orgs:['Organisations','المنظمات']};
```

### 10. EH_Hub.html — What's New app → tab

**Old**
```
clients:'bubbles',news:'news',hub:null};
```
**New**
```
clients:'bubbles',news:'news',orgs:'orgs',hub:null};
```

### 11. EH_Hub.html — View aliases for deep links

**Old**
```
'environment fund 2025 report':'ef2025',
```
**New**
```
'environment fund 2025 report':'ef2025','organisations':'orgs','organisation profiles':'orgs','profiles':'orgs','المنظمات':'orgs',
```

### 12. EH_Hub.html — Search hits carry an "Open profile" action

**Old**
```
onclick="qGo(this.getAttribute(\'data-n\'))">'+esc(r.n)+(r.s?'<div style="font-size:10.5px;opacity:.65;margin-top:1px">'+esc(r.s)+'</div>':'')+'</div>';}).join('');
```
**New**
```
onclick="qGo(this.getAttribute(\'data-n\'))">'+esc(r.n)+'<span class="qp" data-n="'+esc(r.n)+'" onclick="event.stopPropagation();qOrg(this.getAttribute(\'data-n\'))" title="'+L('Open the organisation profile','افتح ملف المنظمة')+'" style="float:'+(hubL==='ar'?'left':'right')+';font-size:10.5px;font-weight:600;color:var(--eh-sea,#0072BB);border:1px solid currentColor;border-radius:999px;padding:1px
```

### 13. EH_Hub.html — qOrg(): open the Organisations view on a name

**Old**
```
function qGo(name){
  qHide(); qEl.value=name;
```
**New**
```
function qOrg(name){
  qHide(); qEl.value=name;
  go(document.querySelector('.tab[data-f="orgs"]'));
  var f=document.getElementById('f-orgs'), send=function(){ try{ f.contentWindow.postMessage({ehhub:'open-org',name:name},'*'); }catch(e){} };
  if(f&&f.contentWindow&&f.dataset.ready){ send(); } else if(f){ f.addEventListener('load',function(){ f.dataset.ready='1'; setTimeout(send,250); },{once:tr
```

### 14. update-dashboard.yml — Pipeline builds and publishes organisations.html

**Old**
```
          rm -f pipeline/etimad_data.xlsx pipeline/etimad_tenders.json

```
**New**
```
          rm -f pipeline/etimad_data.xlsx pipeline/etimad_tenders.json

      # ---------- Organisations view: one profile per client / bidder / winner, built after the sync and the Etimad step so the map carries the live bid and Etimad fields (26 Oct 2026) ----------
      - name: Build the Organisations view
        run: |
          python pipeline/build_org_profiles.py --map site/EH_Stakeholder
```

### 15. update-dashboard.yml — Unresolved-names workbook kept with the bid-sync-review artifact

**Old**
```
            pipeline/roster_duplicates.json

```
**New**
```
            pipeline/roster_duplicates.json
            pipeline/org_unresolved_names.xlsx

```

### 16. CHANGES.md — What's New entries for W44

**Old**
```
## 2026-W43

```
**New**
```
## 2026-W44
hub | major | Organisations | New: an Organisations view — one profile per client, bidder and competitor: every tender it asked for (with the full bidder roster and prices), every bid against EH, wins against EH, what EH sells it, licence and Etimad tenders. Search in English or Arabic; the hub search now offers "Profile" on every hit. | جديد: لوحة «المنظمات» — ملف لكل عميل ومتقدم ومنا
```

| EH_Hub.html | org-view | Masthead tagline: "Six live views … organisation profiles" (EN/AR) | manual follow-up to patch_org_view.py |
