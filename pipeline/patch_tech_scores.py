"""patch_tech_scores.py — read each bidder's technical score from the bid sheets (12 Oct 2026, raised on 2026 bid #87).

The bid-opening sheets (Bid#N tabs of EH-WIN-02-F01) now carry a notes column «ملاحظات» with each bidder's technical
result, e.g. «حاصل على نسبة (87%)». Until now the dashboard ignored that column, so tenders such as 2026 #87 showed only
names and "undisclosed" prices. (The column «رقم العرض» on that sheet holds Etimad's offer numbers — 2230604, 2243963 …
rising in submission order — not prices, and stays excluded as before.)

What it changes (exact-string edits; stops if an anchor is missing):
  • parse_rosters.py   finds the notes column by its header (ملاحظات / remarks / notes) and reads the first percentage
                       in each bidder's note (0–100) into techscores.json — {"2026-87": {"<bidder>": 87.0, …}}.
                       The roster format itself is unchanged, so every other reader of rosters_all.json is unaffected.
  • bid_analytics2.py  attaches the score to each bidder on the Pricing Intelligence card and adds per tender:
                       EH's score, the best score, and EH's place among the scored bidders.
  • app.js             Pricing Intelligence: a "Technical" column in the tender row (EH's score and place) and each
                       bidder's score beside their name when the card is opened. Nothing shows where no score exists.

Run once:  python3 pipeline/patch_tech_scores.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

R, A, J = (os.path.join(HERE, f) for f in ('parse_rosters.py', 'bid_analytics2.py', 'app.js'))
if 'techscores.json' in open(R, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(R, 'rost'); load(A, 'ana'); load(J, 'app')

# ---------------- parse_rosters.py
rep('rost', "    return out if len(out)>=2 else None\n",
    "    return out if len(out)>=2 else None\n\n"
    "TECHH=['ملاحظات','الملاحظات','remarks','notes','note','النتيجه الفنيه','التقييم الفني','technical']\n"
    "def tech_scores(rs):\n"
    "    \"\"\"Each bidder's technical result from the notes column, e.g. «حاصل على نسبة (87%)» → 87.0 (12 Oct 2026).\"\"\"\n"
    "    maxr=min(rs.max_row,500); maxc=rs.max_column\n"
    "    grid=[[rs.cell(r+1,c+1).value for c in range(maxc)] for r in range(maxr)]\n"
    "    nc=tc=None\n"
    "    for r in range(min(15,maxr)):\n"
    "        for c in range(maxc):\n"
    "            h=norm_ar(grid[r][c]).strip()\n"
    "            if nc is None and any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','supplier','اسم العارض']): nc=c\n"
    "            if tc is None and h and any(h==k or h.startswith(k) for k in TECHH): tc=c\n"
    "    if nc is None or tc is None: return {}\n"
    "    out={}\n"
    "    for row in grid:\n"
    "        nm,nt=row[nc],row[tc]\n"
    "        if not is_name(nm) or nt is None: continue\n"
    "        if isinstance(nt,(int,float)) and 0<nt<=1: sc=round(nt*100,1)            # a cell formatted as 87%\n"
    "        else:\n"
    "            m=re.search(r'(\\d{1,3}(?:[.,]\\d+)?)\\s*[%٪]',str(nt))\n"
    "            sc=float(m.group(1).replace(',','.')) if m else None\n"
    "        if sc is not None and 0<=sc<=100: out[str(nm).strip()]=sc\n"
    "    return out\n",
    'data', 'read technical scores from the notes column of each bid sheet')
rep('rost', "            r=parse(wb[sh])\n            if r: allr[f'{yr}-{sn}']=r\n",
    "            r=parse(wb[sh])\n            if r: allr[f'{yr}-{sn}']=r\n"
    "            ts=tech_scores(wb[sh])\n            if ts: tech[f'{yr}-{sn}']=ts\n",
    'data', 'collect technical scores per tender')
rep('rost', "    allr={}\n    for f,yr in", "    allr={}; tech={}\n    for f,yr in", 'data', 'technical score store')
rep('rost', "    json.dump(allr, open('rosters_all.json','w'), ensure_ascii=False)\n",
    "    json.dump(allr, open('rosters_all.json','w'), ensure_ascii=False)\n"
    "    json.dump(tech, open('techscores.json','w'), ensure_ascii=False)   # 12 Oct 2026: technical scores by tender and bidder\n"
    "    print('Technical scores:', {k: len(v) for k, v in tech.items()} or 'none recorded')\n",
    'data', 'write techscores.json')

# ---------------- bid_analytics2.py
rep('ana', "_ALLR=json.load(open('rosters_all.json'))\n",
    "_ALLR=json.load(open('rosters_all.json'))\n"
    "import os as _os2\n"
    "_TECH=json.load(open('techscores.json')) if _os2.path.exists('techscores.json') else {}   # 12 Oct 2026\n"
    "def _tcanon(s):\n"
    "    t=str(s or '').strip().lower()\n"
    "    for a,b in (('أ','ا'),('إ','ا'),('آ','ا'),('ة','ه'),('ى','ي'),('ـ','')): t=t.replace(a,b)\n"
    "    return ' '.join(re.sub(r'[^\\w\\u0600-\\u06FF ]',' ',t).split())\n",
    'data', 'load technical scores')
rep('ana', "        has_full=(ehp is not None and n_priced>=2)\n",
    "        # technical scores from the bid sheet's notes column (12 Oct 2026); matched by bidder name as written\n"
    "        _ts={_tcanon(k):v for k,v in (_TECH.get(key) or {}).items()}\n"
    "        if _ts:\n"
    "            _rawn=None\n"
    "            for bl in blist:\n"
    "                src=next((n for n,a,dq,e in work if (('Environmental Horizons (EH)' if e else n)==bl['name'])),bl['name'])\n"
    "                bl['tech']=_ts.get(_tcanon(src))\n"
    "        _sc=[bl['tech'] for bl in blist if bl.get('tech') is not None]\n"
    "        _eht=next((bl['tech'] for bl in blist if bl['eh'] and bl.get('tech') is not None),None)\n"
    "        has_full=(ehp is not None and n_priced>=2)\n",
    'data', 'attach technical scores to each bidder')
rep('ana', "            bidders=blist,dq_count=len(dqd),undisc_count=len(undisc),level=('full' if has_full else 'partial')))\n",
    "            bidders=blist,dq_count=len(dqd),undisc_count=len(undisc),level=('full' if has_full else 'partial'),\n"
    "            tech_eh=_eht,tech_best=(max(_sc) if _sc else None),tech_n=len(_sc),\n"
    "            tech_rank=(1+sum(1 for x in _sc if x>_eht) if _eht is not None else None)))\n",
    'data', 'EH technical score, best score and place per tender')

# ---------------- app.js (Pricing Intelligence)
rep('app', "       <div style=\"text-align:center\"><div style=\"font-size:9px;color:#5F7078;text-transform:uppercase\">${t('vs Low','مقابل الأدنى')}</div>",
    "       ${r.tech_n?`<div style=\"text-align:center\" title=\"${esc(t('EH technical score and place among the '+r.tech_n+' scored bidders; best score '+r.tech_best+'%','الدرجة الفنية لـ EH وترتيبها بين '+r.tech_n+' متقدمين لهم درجة؛ أعلى درجة '+r.tech_best+'%'))}\"><div style=\"font-size:9px;color:#5F7078;text-transform:uppercase\">${t('Technical','الفني')}</div><div style=\"font-weight:700;font-size:12.5px\">${r.tech_eh!=null?'<span dir=\"ltr\">'+r.tech_eh+'%</span>':'\\u2014'}${r.tech_rank!=null?` <span style=\"font-weight:500;color:#5F7078\">· ${r.tech_rank}/${r.tech_n}</span>`:''}</div></div>`:''}\n"
    "       <div style=\"text-align:center\"><div style=\"font-size:9px;color:#5F7078;text-transform:uppercase\">${t('vs Low','مقابل الأدنى')}</div>",
    'feature', 'Technical column in the tender row')
rep('app', "   const bars=r.bidders.map(b=>{\n",
    "   const tch=b=>b.tech!=null?` <span title=\"${esc(t('Technical score','الدرجة الفنية'))}\" style=\"font-size:10.5px;font-weight:600;color:${b.tech>=(r.tech_best||101)?'#2E7D46':'#5F7078'};white-space:nowrap\">${t('tech ','فني ')}<span dir=\"ltr\">${b.tech}%</span></span>`:'';\n"
    "   const bars=r.bidders.map(b=>{\n",
    'feature', 'technical score helper for bidder lines')
# show the score next to the bidder's name in all three bidder line types (priced, undisclosed, disqualified)
rep('app', "${b.lowest?'\\u25bc ':''}${esc(b.name)}</div>",
    "${b.lowest?'\\u25bc ':''}${esc(b.name)}</div>${b.tech!=null?`<div style=\"min-width:58px\">${tch(b)}</div>`:(r.tech_n?'<div style=\"min-width:58px\"></div>':'')}",
    'feature', 'score beside each priced bidder')
rep('app', 'white-space:nowrap" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(90deg',
    'white-space:nowrap" dir="auto">${esc(b.name)}</div>${r.tech_n?`<div style="min-width:58px">${tch(b)}</div>`:\'\'}<div style="flex:1;height:15px;background:repeating-linear-gradient(90deg',
    'feature', 'score beside each bidder whose price was not disclosed')
rep('app', 'text-align:right" dir="auto">${esc(b.name)}</div><div style="flex:1;height:15px;background:repeating-linear-gradient(45deg',
    'text-align:right" dir="auto">${esc(b.name)}</div>${r.tech_n?`<div style="min-width:58px">${tch(b)}</div>`:\'\'}<div style="flex:1;height:15px;background:repeating-linear-gradient(45deg',
    'feature', 'score beside a disqualified bidder')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for alias, path in (('rost', R), ('ana', A), ('app', J)):
    open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_tech_scores'), 'Bid sheets — technical scores (2026 #87)')
print('patched: parse_rosters.py, bid_analytics2.py, app.js')
