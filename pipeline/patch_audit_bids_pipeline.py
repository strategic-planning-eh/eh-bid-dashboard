"""patch_audit_bids_pipeline.py — bid pipeline fixes from the 12 Oct 2026 audit (judge J1, "bids" fix pass).

What was wrong, and what changes (exact-string edits; the script stops if any anchor is missing):

  namecheck.py        (J1 #6, bids-06/data-15) Etimad award-report labels in the bidder-name column — «حالة الترسية»,
                      «مستبعد من الترسية», «سبب الاستبعاد», «تقرير الترسية», «الاعلى سعرًا», «العرض الثاني وتم استعاده» — and the
                      #82 tender title «منافسة مكتب استشارات بيئية…» were read as competitors. namecheck.py stays the single
                      guard: a new is_label_text() rejects roster labels, and a cell that starts with «منافسة» or «مشروع» is a
                      tender title even when it names an office type. Every reader (rosters, map sync) goes through it.
  parse_rosters.py    (J1 #7, bids-07/data-16) Bid#25 and Bid#27 put the award table left of the applicant list, so the parser
                      took the one-name award column and dropped the roster (39 + 3 bidders). When several columns carry a
                      bidder-name header, the one with the most company names is used. (J1 #20) Names over 90 characters
                      (a name pasted twice, long legal suffixes on Bid#65/#34) were dropped; they are now cut to one name.
  build_competitors.py(J1 #8, bids-08) "Undercut" and "priced against EH" were counted on the raw roster only, so rivals whose
                      winning price is in the tracker showed "no price". The counts now use the same filled-in rows as the
                      pricing cards (fill_roster: EH's offer with VAT, the award value on the winner). (J1 #20, bids-19/
                      data-17) «شركة الدكتور على الدهيمان» is the same firm as «شركة د علي صالح الدهيمان»; «رواد / رائدات / رموز
                      الاستدامة» are three firms and are no longer merged by the fuzzy step. (Esco and Samer pairs: owner decision.)
  extract_bids2.py    (J1 #1) reads the tracker's «قيمة العرض المالي المقدم (+ ضريبة القيمة المضافة)» column as offer_vat (else
                      offer × 1.15). (J1 #40, data-12) durations written in days, weeks or years («10 ايام», «3 اسابيع»,
                      «سنتين ونصف», «Annual») are converted to months with one decimal, and the text duration column is used
                      when the months column is empty.
  bid_analytics2.py   (J1 #1, bids-03/data-03) every price comparison is on one basis, VAT included: Etimad roster and award
                      prices include VAT, so EH's offer is taken from the «+ ضريبة» column (gaps, ranks, medians re-derived).
                      (J1 #3, bids-04) "not awarded" no longer double-counts the 14 lost tenders; a pending count is added so
                      the donut slices add up to the tender total. (J1 #10, bids-10) new / lapsed client flags are computed
                      across all tracking years, not per scope. (J1 #11) client value = EH's own offers (no winners' prices).
                      (J1 #15, bids-13) rank and gap are left empty when fewer than two prices are known, and the bidder
                      count is left empty (not "1") when there is no roster and no tracker count. (J1 #27) counts the
                      rosters that list EH. (J1 #51, data-50) the winner list is passed in memory instead of being re-read
                      from winner_canon.json. Duration bands follow the decimal months.
  winner_canon.json   (J1 #51) regenerated from the v6 tracker (the committed copy held 4 of 14 winners).
  aliases.csv         (J1 #52, data-53) row 52 «مكتب الدعم البيئي للاستشارات البيئية» → «شركة الدعم للخدمات البيئية» merged two
                      different firms (Bid#27/#50 vs Bid#69): status set to rejected. Rows 16, 19, 30 are left for the owner.

Run once:  python3 pipeline/patch_audit_bids_pipeline.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

P = {a: os.path.join(HERE, f) for a, f in (('nc', 'namecheck.py'), ('rost', 'parse_rosters.py'), ('comp', 'build_competitors.py'),
                                          ('ext', 'extract_bids2.py'), ('ana', 'bid_analytics2.py'))}
if 'def is_label_text' in open(P['nc'], encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
for a, p in P.items(): load(p, a)

# ======================================================================= namecheck.py
rep('nc', "def looks_like_company(s):\n    t = _n(s)\n    return bool(t) and 3 <= len(t) <= 120 and not is_reason_text(t) and not is_tender_title(t) and bool(re.search(r'[a-z\\u0600-\\u06ff]{3,}', t))\n",
    "# Etimad award-report labels and roster headings that sit in the bidder-name column (12 Oct 2026, audit bids-06 / data-15)\n"
    "LABEL_PHRASES = ['حالة الترسية', 'مستبعد من الترسية', 'سبب الاستبعاد', 'سبب عدم الترسية', 'تقرير الترسية', 'تقرير الموردين', 'تقرير فتح العروض',\n"
    "                 'قائمة الموردين', 'عدد الموردين', 'اسم المورد', 'قيمة الترسية', 'نوع الترسية', 'ترسية كاملة', 'ترسية جزئية',\n"
    "                 'الاعلى سعرا', 'الادنى سعرا', 'العرض الاول', 'العرض الثاني', 'العرض الثالث', 'رقم المنافسة', 'تاريخ فتح العروض']\n"
    "_LAB = [_n(p) for p in LABEL_PHRASES]\n"
    "_TITLE_ALWAYS = [_n(w) for w in ['منافسة', 'مشروع']]   # «منافسة مكتب استشارات…» is a tender title even though it names an office type\n"
    "\n"
    "def is_label_text(s):\n"
    "    \"\"\"True when the cell is a roster label (award status, exclusion reason, list heading) or a sheet title, not a bidder.\"\"\"\n"
    "    t = _n(s); w = t.split()\n"
    "    return bool(w) and (any(p in t for p in _LAB) or w[0] in _TITLE_ALWAYS)\n"
    "\n"
    "def looks_like_company(s):\n    t = _n(s)\n    return bool(t) and 3 <= len(t) <= 120 and not is_reason_text(t) and not is_tender_title(t) and not is_label_text(t) and bool(re.search(r'[a-z\\u0600-\\u06ff]{3,}', t))\n",
    'data', 'roster labels and sheet titles are not company names (single guard)')

# ======================================================================= parse_rosters.py
rep('rost', "def is_name(v):\n    if not isinstance(v,str): return False\n    t=v.strip()\n    if len(t)<6 or len(t)>90: return False\n",
    "def clip_name(v):\n"
    "    \"\"\"A name cell over 90 characters (the name pasted twice, or a long legal suffix) is cut to one name (12 Oct 2026).\"\"\"\n"
    "    t=re.sub(r'\\s+',' ',str(v)).strip()\n"
    "    if len(t)<=90: return t\n"
    "    w=t.split()\n"
    "    for i in range(2,len(w)-1):\n"
    "        if w[i:i+2]==w[0:2] or w[i:i+2]==w[1:3]: return ' '.join(w[:i])      # second copy starts here\n"
    "    out=''\n"
    "    for x in w:\n"
    "        if len(out)+len(x)+1>90: break\n"
    "        out=(out+' '+x).strip()\n"
    "    return out\n"
    "LONG_OK=['شركه','مؤسسه','مكتب','مجموعه','مصنع','مركز','معهد','جامعه','company','the']   # a cut name must open like a firm\n"
    "def is_name(v):\n    if not isinstance(v,str): return False\n    t=clip_name(v)\n    if len(t)<6: return False\n"
    "    if len(v.strip())>90 and (norm_ar(t).split() or [''])[0] not in LONG_OK: return False   # long titles stay out\n",
    'data', 'over-long names are cut to one name instead of dropped')
rep('rost', "    nc=None\n    for c in range(maxc):\n        for r in range(min(12,maxr)):\n            h=norm_ar(grid[r][c])\n"
    "            if any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','supplier','اسم العارض','المورد']) and not any(d in h for d in DESC):\n"
    "                nc=c; break\n        if nc is not None: break\n",
    "    # 12 Oct 2026 (audit bids-07): award-report sheets (Bid#25, Bid#27) carry two bidder-name headers, the award table and the\n"
    "    # applicant list; the column with the most company names is the roster.\n"
    "    nc=None; hcols=[]\n"
    "    for c in range(maxc):\n        for r in range(min(12,maxr)):\n            h=norm_ar(grid[r][c])\n"
    "            if any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','supplier','اسم العارض','المورد']) and not any(d in h for d in DESC):\n"
    "                hcols.append(c); break\n"
    "    if hcols:\n"
    "        nc=max(hcols, key=lambda c:(sum(1 for row in grid if is_name(row[c])), -c))\n",
    'data', 'pick the applicant list, not the award table')
rep('rost', "        nm=row[nc]\n        if not is_name(nm): continue\n        k=canon(nm)[:40]\n",
    "        nm=row[nc]\n        if not is_name(nm): continue\n        nm=clip_name(nm)\n        k=canon(nm)[:40]\n",
    'data', 'store the clipped name')
rep('rost', "        if sc is not None and 0<=sc<=100: out[str(nm).strip()]=sc\n",
    "        if sc is not None and 0<=sc<=100: out[clip_name(nm)]=sc\n",
    'data', 'technical scores keyed by the same clipped name')

# ======================================================================= build_competitors.py
rep('comp', "from parse_rosters import norm_ar, canon, is_eh\n",
    "from parse_rosters import norm_ar, canon, is_eh\n"
    "\n"
    "# ---- one firm under two spellings / two firms that look alike (12 Oct 2026, audit bids-19 / data-17) ----\n"
    "SAME_FIRM={canon('شركة الدكتور على الدهيمان للاستشارات البيئية'): canon('شركة د علي صالح الدهيمان للاستشارات البيئية')}\n"
    "KEEP_APART=[['رواد الاستدامه','رائدات الاستدامه','رموز الاستدامه']]   # distinct firms: never merged by the fuzzy step\n"
    "def ckey(name):\n"
    "    c=canon(name); return SAME_FIRM.get(c,c)\n"
    "def _apart(name):\n"
    "    c=canon(name)\n"
    "    for gi,grp in enumerate(KEEP_APART):\n"
    "        for j,p in enumerate(grp):\n"
    "            if canon(p) in c: return (gi,j)\n"
    "    return None\n"
    "\n"
    "def eh_price_vat(b):\n"
    "    \"\"\"EH's offer on the Etimad basis, VAT included: the tracker's «(+ ضريبة القيمة المضافة)» column, else offer × 1.15.\n"
    "    Roster prices and award values on Etimad include VAT, so every comparison uses this figure (12 Oct 2026, audit bids-03).\"\"\"\n"
    "    if not b: return None\n"
    "    if b.get('offer_vat'): return b['offer_vat']\n"
    "    return round(b['offer']*1.15,2) if b.get('offer') else None\n"
    "\n"
    "def fill_roster(bidders, b, wc):\n"
    "    \"\"\"The roster with the prices the tracker knows filled in: EH's offer (VAT included) on EH's row, the award value on the\n"
    "    winner's row, and the named winner appended when missing from the roster. Rows: [name, price, dq, is_eh, appended].\n"
    "    Used by the pricing cards (bid_analytics2) and by the competitor undercut counts below, so both agree.\"\"\"\n"
    "    eh_offer=eh_price_vat(b); award=(b or {}).get('winval'); winner=(b or {}).get('winner')\n"
    "    def is_w(nm,e):\n"
    "        if wc=='__EH__': return bool(e)\n"
    "        if wc: return ckey(nm)==wc\n"
    "        return False\n"
    "    work=[[n,a,dq,e,False] for n,a,dq,e in bidders]\n"
    "    for row in work:\n"
    "        if row[3] and row[1] is None and not row[2] and eh_offer: row[1]=eh_offer\n"
    "    present=False\n"
    "    for row in work:\n"
    "        if is_w(row[0],row[3]):\n"
    "            present=True\n"
    "            if row[1] is None and not row[2] and award: row[1]=award\n"
    "    if winner and award and not present and not is_eh(winner):\n"
    "        work.append([winner,award,False,False,True])\n"
    "    return work, is_w\n",
    'data', 'shared roster fill (VAT basis), same-firm alias and keep-apart list')
rep('comp', "        return canon(best) if bestov>=2 else None\n", "        return ckey(best) if bestov>=2 else None\n",
    'data', 'winner key uses the same-firm alias')
rep('comp', "        if not any(x[3] for x in bidders): continue   # EH must be present\n"
    "        ehp=next((a for nm,a,dq,e in bidders if e and a and not dq), None)\n"
    "        wc=winner_canon.get(key)\n"
    "        for nm,a,dq,e in bidders:\n"
    "            if e: continue   # skip EH itself\n"
    "            c=canon(nm)\n",
    "        if not any(x[3] for x in bidders): continue   # EH must be present\n"
    "        yr,sn=key.split('-'); b=bidx.get((int(yr),int(sn)))\n"
    "        wc=winner_canon.get(key)\n"
    "        work,_=fill_roster(bidders, b, wc)            # same filled-in prices as the pricing cards (12 Oct 2026, audit bids-08)\n"
    "        ehp=next((a for nm,a,dq,e,ad in work if e and a and not dq), None)\n"
    "        for nm,a,dq,e,added in work:\n"
    "            if e or added: continue   # skip EH itself; an appended winner is not a roster encounter\n"
    "            c=ckey(nm)\n",
    'data', 'undercut / priced-vs-EH counted on the filled-in rows')
rep('comp', "            if k2==k or k2 in merged_into: continue\n            if sim(dn, dispname(k2))>=0.85:\n",
    "            if k2==k or k2 in merged_into: continue\n"
    "            _a,_b=_apart(dn),_apart(dispname(k2))\n"
    "            if _a and _b and _a!=_b: continue      # listed as different firms\n"
    "            if sim(dn, dispname(k2))>=0.85:\n",
    'data', 'keep-apart list honoured by the fuzzy merge')

# ======================================================================= extract_bids2.py
rep('ext', "def mkey(v):\n",
    "def dur_months(v):\n"
    "    \"\"\"Project length in months, one decimal (12 Oct 2026, audit data-12). Numbers are months; text such as «10 ايام»,\n"
    "    «3 اسابيع», «2.5 سنتين ونصف», «شهرين» or «Annual» is converted. None when no length can be read («مرة واحدة»).\"\"\"\n"
    "    if v is None: return None\n"
    "    if isinstance(v,(int,float)): return round(float(v),1) if (v==v and v>0) else None\n"
    "    s=unicodedata.normalize('NFKC',str(v)).strip().lower().translate(str.maketrans('٠١٢٣٤٥٦٧٨٩٫','0123456789.'))\n"
    "    s=re.sub(r'[\\u0640\\u064b-\\u0652]','',s)\n"
    "    for a,b in (('أ','ا'),('إ','ا'),('آ','ا'),('ة','ه'),('ى','ي')): s=s.replace(a,b)\n"
    "    if not s: return None\n"
    "    m=re.search(r'\\d+(?:[.,]\\d+)?',s); n=float(m.group(0).replace(',','.')) if m else None\n"
    "    tail=s[m.end():m.end()+14] if m else s          # the unit word right after the number decides\n"
    "    def unit(x):\n"
    "        if re.search(r'يوم|ايام|day',x): return 1/30\n"
    "        if re.search(r'اسبوع|اسابيع|week',x): return 7/30\n"
    "        if re.search(r'شهر|اشهر|month',x): return 1\n"
    "        if re.search(r'سنه|سنو|سنين|سنتين|سنوات|عام|اعوام|year|annual',x): return 12\n"
    "        return None\n"
    "    u=unit(tail) or unit(s)\n"
    "    if n is None:\n"
    "        if re.search(r'سنتين|عامين|شهرين|اسبوعين|يومين',s): n=2\n"
    "        elif u: n=1\n"
    "        else: return None\n"
    "    if u is None: u=1                                # a bare number means months\n"
    "    return round(n*u,1) if n>0 else None\n"
    "def mkey(v):\n",
    'data', 'duration parser: days / weeks / years to months')
rep('ext', "        elif 'Project Duration (Month)' in h: m['dur']=c\n",
    "        elif 'Project Duration (Month)' in h: m['dur']=c\n"
    "        elif h.startswith('Project Duration'): m['dur2']=c          # text duration (col 7), used when col 6 is empty\n",
    'data', 'read the text duration column')
rep('ext', "        elif 'قيمة العرض المالي المقدم (بدون' in h: m['offer']=c\n",
    "        elif 'قيمة العرض المالي المقدم (بدون' in h: m['offer']=c\n"
    "        elif 'قيمة العرض المالي المقدم (+' in h: m['offer_vat']=c     # with VAT — the basis of Etimad roster and award prices\n",
    'data', 'read the offer-with-VAT column')
rep('ext', "            dur=num(g('dur')),\n",
    "            dur=(dur_months(g('dur')) if dur_months(g('dur')) is not None else dur_months(g('dur2'))),\n",
    'data', 'duration in months from either duration column')
rep('ext', "            offer=num(g('offer')),\n",
    "            offer=num(g('offer')),\n            offer_vat=num(g('offer_vat')),\n",
    'data', 'offer with VAT')
rep('ext', "    _o=OVERRIDES.get((_b['year'],_b['sn']))\n    if _o: _b.update(_o)\n",
    "    _o=OVERRIDES.get((_b['year'],_b['sn']))\n    if _o:\n        _b.update(_o)\n        if 'offer' in _o and 'offer_vat' not in _o: _b['offer_vat']=None   # re-derived below\n",
    'data', 'override keeps the VAT figure consistent')
rep('ext', "            _b=_byk[_k]; _b.update(_fields); _nu+=1\n",
    "            _b=_byk[_k]; _b.update(_fields); _nu+=1\n"
    "            if 'offer' in _fields and 'offer_vat' not in _fields: _b['offer_vat']=None   # re-derived below\n",
    'data', 'corrections keep the VAT figure consistent')
rep('ext', "json.dump({'bids':allbids,'rosters':rosters}, open('bidraw2.json','w'), ensure_ascii=False)\n",
    "# offer with VAT: the tracker's own figure where it is a number, else the pre-VAT offer × 1.15 (12 Oct 2026, audit bids-03)\n"
    "for _b in allbids:\n"
    "    if not _b.get('offer'): _b['offer_vat']=None\n"
    "    elif not _b.get('offer_vat') or _b['offer_vat']<100: _b['offer_vat']=round(_b['offer']*1.15,2)\n"
    "json.dump({'bids':allbids,'rosters':rosters}, open('bidraw2.json','w'), ensure_ascii=False)\n",
    'data', 'fill offer_vat')

# ======================================================================= bid_analytics2.py
rep('ana', "def compute(bids, rfull, comp):\n",
    "def compute(bids, rfull, comp, wcanon=None):\n", 'data', 'winner list passed in memory')
rep('ana', "     not_awarded=sum(1 for b in bids if b['status']=='Not awarded'),\n",
    "     # «لم تتم الترسية» rows are EH's losses and already sit in awarded_other; only an undecided one is 'not awarded'\n"
    "     not_awarded=sum(1 for b in bids if b['status']=='Not awarded' and not b['decided']),   # 12 Oct 2026, audit bids-04\n"
    "     pending=sum(1 for b in bids if not b['decided'] and b['status'] not in ('Cancelled','Not awarded')),\n",
    'data', 'win/loss slices no longer double-count losses')
rep('ana', "    durs=[b['dur'] for b in bids if b['dur']]\n    dur_bands=[('≤3 mo',0,3),('4–6 mo',4,6),('7–12 mo',7,12),('13–24 mo',13,24),('25+ mo',25,999)]\n"
    "    duration=[]\n    for lbl,lo,hi in dur_bands:\n        bb=[b for b in bids if b['dur'] and lo<=b['dur']<=hi]\n",
    "    durs=[b['dur'] for b in bids if b['dur']]\n    dur_bands=[('≤3 mo',0,3),('4–6 mo',3,6),('7–12 mo',6,12),('13–24 mo',12,24),('25+ mo',24,999)]   # months may be decimal (12 Oct 2026)\n"
    "    duration=[]\n    for lbl,lo,hi in dur_bands:\n        bb=[b for b in bids if b['dur'] and lo<b['dur']<=hi]\n",
    'data', 'duration bands accept decimal months')
rep('ana', "    dur_stats=dict(median=round(st.median(durs)) if durs else 0, mean=round(st.mean(durs),1) if durs else 0, max=int(max(durs)) if durs else 0)\n",
    "    dur_stats=dict(median=round(st.median(durs),1) if durs else 0, mean=round(st.mean(durs),1) if durs else 0, max=round(max(durs),1) if durs else 0)\n",
    'data', 'duration stats keep one decimal')
rep('ana', "    winner_canon=json.load(open('winner_canon.json'))\n",
    "    winner_canon=wcanon if wcanon is not None else json.load(open('winner_canon.json'))   # 12 Oct 2026: in memory, never a stale file\n",
    'data', 'use the winner list built in this run')
rep('ana', "        eh_offer=(bb['offer'] if bb else None)     # قيمة العرض\n"
    "        award=(bb['winval'] if bb else None)        # قيمة الترسية\n"
    "        winner=(bb['winner'] if bb else None)\n"
    "        wc=winner_canon.get(key)                    # '__EH__', canon string, or None\n"
    "        def _is_w(nm,e,wc=wc):\n"
    "            if wc=='__EH__': return bool(e)\n"
    "            if wc: return _canon(nm)==wc\n"
    "            return False\n"
    "        work=[[n,a,dq,e] for n,a,dq,e in bidders]\n"
    "        # fill EH's price from the main table if EH is on the roster but unpriced\n"
    "        for row in work:\n"
    "            if row[3] and row[1] is None and not row[2] and eh_offer: row[1]=eh_offer\n"
    "        # assign the award value to the winner if present & unpriced; note if winner is on the roster\n"
    "        winner_present=False\n"
    "        for row in work:\n"
    "            if _is_w(row[0],row[3]):\n"
    "                winner_present=True\n"
    "                if row[1] is None and not row[2] and award: row[1]=award\n"
    "        # winner named in main table but not on the roster -> add them with the award value\n"
    "        if winner and award and not winner_present and not _is_eh_name(winner):\n"
    "            work.append([winner, award, False, False])\n",
    "        award=(bb['winval'] if bb else None)        # قيمة الترسية (Etimad award value, VAT included)\n"
    "        wc=winner_canon.get(key)                    # '__EH__', canon string, or None\n"
    "        # One VAT basis (12 Oct 2026, audit bids-03): roster and award prices include VAT, so EH's tracker offer is taken from\n"
    "        # the «(+ ضريبة القيمة المضافة)» column. build_competitors.fill_roster is shared with the competitor undercut counts.\n"
    "        _w5,_is_w=_BC.fill_roster(bidders, bb, wc)\n"
    "        work=[[n,a,dq,e] for n,a,dq,e,_ad in _w5]\n",
    'data', 'pricing cards use the shared VAT-basis fill')
rep('ana', "        rank=(prices.index(ehp)+1) if ehp is not None else None\n",
    "        rank=(prices.index(ehp)+1) if (ehp is not None and n_priced>=2) else None   # no rank against an unknown field (audit bids-13)\n",
    'data', 'rank only with two or more prices')
rep('ana', "        gap=round(100*(ehp-lo)/lo,1) if (ehp is not None and lo) else None\n",
    "        gap=round(100*(ehp-lo)/lo,1) if (ehp is not None and lo and n_priced>=2) else None\n",
    'data', 'gap only with two or more prices')
rep('ana', "            blist.append(dict(name=('Environmental Horizons (EH)' if e else n),price=round(a),dq=False,undisclosed=False,eh=bool(e),rank=i2+1,lowest=(i2==0 and n_priced>1),won=_is_w(n,e)))\n",
    "            blist.append(dict(name=('Environmental Horizons (EH)' if e else n),price=round(a),dq=False,undisclosed=False,eh=bool(e),rank=(i2+1 if n_priced>1 else None),lowest=(i2==0 and n_priced>1),won=_is_w(n,e)))\n",
    'data', 'bidder rank only with two or more prices')
rep('ana', "        offer=bb['offer']; wv=bb['winval']; wn=bb['winner']\n",
    "        offer=_BC.eh_price_vat(bb); wv=bb['winval']; wn=bb['winner']     # VAT included, like the award value\n",
    'data', '2-point cards on the VAT basis')
rep('ana', "        price_rows.append(dict(sn=sn2,year=yr2,eh=ehp,low=round(lo),high=round(hi),avg=round(avg),\n            rank=rank,n=2,n_priced=2,gap=gap,",
    "        price_rows.append(dict(sn=sn2,year=yr2,eh=ehp,low=round(lo),high=round(hi),avg=round(avg),\n            rank=rank,n=(int(bb['nbid']) if bb.get('nbid') else None),n_priced=2,gap=gap,",
    'data', '2-point cards: field size from the tracker or unknown')
rep('ana', "        if bb.get('eh_won') is True and (bb.get('winval') or bb.get('offer')):\n            ehp=round(bb.get('winval') or bb.get('offer'))\n"
    "            blist=[dict(name='Environmental Horizons (EH)',price=ehp,dq=False,undisclosed=False,eh=True,rank=1,lowest=True,won=True)]\n"
    "            price_rows.append(dict(sn=sn3,year=yr3,eh=ehp,low=ehp,high=ehp,avg=ehp,\n"
    "                rank=1,n=(nb or 1),n_priced=1,gap=0,won=True,",
    "        if bb.get('eh_won') is True and (bb.get('winval') or bb.get('offer')):\n            ehp=round(_BC.eh_price_vat(bb) or bb.get('winval'))   # EH's offer with VAT; the award value only when no offer\n"
    "            blist=[dict(name='Environmental Horizons (EH)',price=ehp,dq=False,undisclosed=False,eh=True,rank=None,lowest=False,won=True)]\n"
    "            price_rows.append(dict(sn=sn3,year=yr3,eh=ehp,low=ehp,high=ehp,avg=ehp,\n"
    "                rank=None,n=nb,n_priced=1,gap=None,won=True,",
    'data', 'single-price won cards: no invented rank, gap or bidder count')
rep('ana', "            blist=[dict(name=bb['winner'],price=wvr,dq=False,undisclosed=False,eh=False,rank=1,lowest=True,won=True)]\n"
    "            price_rows.append(dict(sn=sn3,year=yr3,eh=None,low=wvr,high=wvr,avg=wvr,\n"
    "                rank=None,n=(nb or 1),",
    "            blist=[dict(name=bb['winner'],price=wvr,dq=False,undisclosed=False,eh=False,rank=None,lowest=False,won=True)]\n"
    "            price_rows.append(dict(sn=sn3,year=yr3,eh=None,low=wvr,high=wvr,avg=wvr,\n"
    "                rank=None,n=nb,",
    'data', 'single-price lost cards: no invented bidder count')
rep('ana', "            rank=None,n=(nb4 or 1),n_priced=0,",
    "            rank=None,n=nb4,n_priced=0,", 'data', 'text-flagged cards: no invented bidder count')
rep('ana', "        total_bidders=sum(r['n_priced'] for r in price_rows),\n",
    "        total_bidders=sum(r['n_priced'] for r in price_rows),\n"
    "        basis='vat_incl',                                                    # every price on the cards includes 15% VAT\n"
    "        eh_rosters=sum(1 for v in rfull.values() if any(x[3] for x in v)),   # bid sheets that list EH (shared tenders)\n",
    'data', 'VAT basis flag and shared-tender count')
rep('ana', "        if b['year']==2025: c['b25']+=1; c['v25']+=b['value'] or 0\n        else: c['b26']+=1; c['v26']+=b['value'] or 0\n",
    "        # EH's own offer (pre-VAT tracker column), never the winner's price on a lost tender (12 Oct 2026, audit bids-11)\n"
    "        if b['year']==2025: c['b25']+=1; c['v25']+=b['offer'] or 0\n        else: c['b26']+=1; c['v26']+=b['offer'] or 0\n",
    'data', 'client value = EH offers only')
rep('ana', "    clients=[]\n    for nm,c in cacc.items():\n",
    "    # new / lapsed are judged across every tracking year, whatever the scope (12 Oct 2026, audit bids-10)\n"
    "    _cyrs=collections.defaultdict(set)\n"
    "    for b in _ALLBIDS:\n"
    "        if b['client']: _cyrs[cl_name(b['client'])].add(b['year'])\n"
    "    _ylast=max((b['year'] for b in _ALLBIDS), default=None)\n"
    "    clients=[]\n    for nm,c in cacc.items():\n",
    'data', 'client years from all data')
rep('ana', "            lapsed=(c['b25']>0 and c['b26']==0), isnew=(c['b25']==0 and c['b26']>0)))\n",
    "            lapsed=((_ylast-1) in _cyrs[nm] and _ylast not in _cyrs[nm]), isnew=(_cyrs[nm]=={_ylast})))\n",
    'data', 'new / lapsed flags independent of scope')
rep('ana', "            svc=SVCN2.get(b['svcdept'],''), dur=int(b['dur']) if b['dur'] else None,\n",
    "            svc=SVCN2.get(b['svcdept'],''), dur=round(b['dur'],1) if b['dur'] else None,\n",
    'data', 'bid list keeps decimal months')
rep('ana', "    comp,_wc=_BC.build(B, RF)\n    return compute(B, RF, comp)\n",
    "    comp,_wc=_BC.build(B, RF)\n    return compute(B, RF, comp, _wc)\n", 'data', 'pass the winner list in memory')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for a, p in P.items():
    open(p, 'w', encoding='utf-8').write(FILES[a])

# ---- aliases.csv (CRLF + BOM: edited byte-for-byte, only row 52 changes)
AP = os.path.join(HERE, 'aliases.csv')
s = open(AP, encoding='utf-8', newline='').read()
old = 'مكتب الدعم البيئي للاستشارات البيئية,شركة الدعم للخدمات البيئية,core-subset,auto,Oct 2026'
if s.count(old) != 1: sys.exit('FAILED: aliases.csv row 52 not found')
open(AP, 'w', encoding='utf-8', newline='').write(s.replace(old, old.replace(',auto,', ',rejected,')))

# ---- winner_canon.json regenerated from tracker v6 (EH-WIN-02-F01 v6, 2026 scope — what build_competitors writes last)
WC = {"2026-2": "شركه السامر العربيه للخدمات البيئيه",
      "2026-13": "شركه الكيان الامثل للتجاره",
      "2026-15": "شركه اسكو المحدوده",
      "2026-16": "__EH__",
      "2026-25": "شركه الاندلس للاستشارات الهندسيه",
      "2026-27": "شركه البيئه والتنميه للاستشارات البيئيه",
      "2026-50": "__EH__",
      "2026-52": "شركه نماء المتقدمه للخدمات البيئيه",
      "2026-68": "شركه العالميه للخدمات البيئيه",
      "2026-81": "شركه العالميه للخدمات البيئيه",
      "2026-83": "__EH__",
      "2026-84": "__EH__",
      "2026-85": "__EH__",
      "2026-88": "__EH__",
      "2026-108": "شركه د علي صالح الدهيمان للاستشارات البيئيه"}
json.dump(WC, open(os.path.join(HERE, 'winner_canon.json'), 'w', encoding='utf-8'), ensure_ascii=False)

write_change_table(os.path.join(HERE, 'change_table_audit_bids_pipeline'), 'Audit fixes (J1) — bid pipeline')
print('patched: namecheck.py, parse_rosters.py, build_competitors.py, extract_bids2.py, bid_analytics2.py, aliases.csv, winner_canon.json')
