"""patch_bid_subdates.py — All Tenders (bid app): show each tender's submission deadline and EH's date of submission (8 Oct 2026).

Source: the bid tracker EH-WIN-02-F01 —
  "Submission Deadline / آجال تقديم العروض"  (already read as `submit`)
  "Date of submission / تاريخ التقديم"        (new: `subdate`; a date, or text such as 11.05.2026; "-" or blank = none)
  "Status of submission / حالة التقديم"       (new: `substatus`; Yes / No / blank)
Where EH did not submit, the table says so in words, with the reason when the tracker gives one
(bid committee said no, tender cancelled, deadline still open). Nothing is guessed from a title.

What it changes (exact-string edits, fails loudly if an anchor is missing):
  • extract_bids2.py   read the two new columns (by header, so either tracker layout works) into bidraw2.json.
  • bid_analytics2.py  add deadline, subdate and a submission state code to every row of bidlist.
  • app.js             two new columns in All Tenders: "Submission deadline" and "EH submitted", EN/AR.

Run once:  python3 pipeline/patch_bid_subdates.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

X, A, J = (os.path.join(HERE, f) for f in ('extract_bids2.py', 'bid_analytics2.py', 'app.js'))
if 'substatus' in open(X, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(X, 'extract'); load(A, 'analytics'); load(J, 'app')

# ---------------- extract_bids2.py
rep('extract', "def mkey(v):\n",
    "def subdstr(v):\n"
    "    \"\"\"EH's date of submission: a real date, or text like 11.05.2026 / 11/05/2026 / 2026-05-11. '-' or blank = none.\"\"\"\n"
    "    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime('%Y-%m-%d')\n"
    "    s=str(v or '').strip()\n"
    "    mm=re.match(r'^(\\d{1,2})[./-](\\d{1,2})[./-](\\d{4})$',s)\n"
    "    if mm:\n"
    "        try: return datetime.date(int(mm.group(3)),int(mm.group(2)),int(mm.group(1))).isoformat()\n"
    "        except ValueError: return None\n"
    "    mm=re.match(r'^(\\d{4})-(\\d{1,2})-(\\d{1,2})',s)\n"
    "    if mm:\n"
    "        try: return datetime.date(int(mm.group(1)),int(mm.group(2)),int(mm.group(3))).isoformat()\n"
    "        except ValueError: return None\n"
    "    return None\n"
    "def substat(v):\n"
    "    s=str(v or '').strip().lower()\n"
    "    if s in ('yes','y','نعم','تم','تم التقديم'): return 'Yes'\n"
    "    if s in ('no','n','لا','لم يتم'): return 'No'\n"
    "    return None\n"
    "def mkey(v):\n",
    'data', 'parse the date and status of submission')
rep('extract', "        if h.startswith('SN#') and 'Year' not in h and 'sn' not in m: m['sn']=c\n",
    "        if h.startswith('SN#') and 'Year' not in h and 'sn' not in m: m['sn']=c\n"
    "        elif h.startswith('Date of submission') or h.startswith('تاريخ التقديم'): m['subdate']=c\n"
    "        elif h.startswith('Status of submission') or h.startswith('حالة التقديم'): m['substatus']=c\n",
    'data', 'map the tracker columns "Date of submission" and "Status of submission"')
rep('extract', "            submit=dstr(g('submit')), submonth=mkey(g('submit')),\n",
    "            submit=dstr(g('submit')), submonth=mkey(g('submit')),\n"
    "            subdate=subdstr(g('subdate')), substatus=substat(g('substatus')), subcol=('subdate' in m or 'substatus' in m),\n",
    'data', 'carry the submission fields into bidraw2.json')

# ---------------- bid_analytics2.py
rep('analytics', "    bidlist=[]\n    for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):\n",
    "    def substate(b):\n"
    "        # Order matters: the tracker's own submission columns first, then the offer evidence, then the reasons.\n"
    "        if b.get('subdate'): return 'date'\n"
    "        if b.get('substatus')=='Yes': return 'yes'\n"
    "        no=b.get('substatus')=='No'\n"
    "        if not no and (b.get('eh_won') is True or b.get('ehsub') or b.get('offer')): return 'yes'\n"
    "        if re.search(r'reject|رفض', b.get('committee') or '', re.I): return 'rejected'\n"
    "        if (b.get('status') or '')=='Cancelled': return 'cancelled'\n"
    "        if no: return 'no'\n"
    "        if b.get('submit') and b['submit']>=_today.isoformat(): return 'open'\n"
    "        return 'none' if b.get('subcol') else 'unrecorded'\n"
    "    bidlist=[]\n    for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):\n",
    'data', 'submission state for each tender')
rep('analytics', "            title=b['title'], client=b['client'], platform=b['platform'],\n",
    "            title=b['title'], client=b['client'], platform=b['platform'],\n"
    "            deadline=b.get('submit') or None, subdate=b.get('subdate') or None, sub=substate(b),\n",
    'data', 'deadline and date of submission in bidlist')
rep('analytics', "import json, collections, statistics as st\n", "import json, collections, re, statistics as st\n", 'data', 'import re')

# ---------------- app.js
rep('app', "function renderTenders(){\n",
    "const SUBW={yes:['Submitted \u2014 date not recorded','\u0642\u064f\u062f\u0651\u0650\u0645 \u0627\u0644\u0639\u0631\u0636 \u2014 \u0627\u0644\u062a\u0627\u0631\u064a\u062e \u063a\u064a\u0631 \u0645\u0633\u062c\u0651\u0644'],\n"
    " no:['EH did not submit','\u0644\u0645 \u062a\u0642\u062f\u0651\u0645 EH \u0639\u0631\u0636\u0627\u064b'],\n"
    " rejected:['EH did not submit \u2014 the bid committee said no','\u0644\u0645 \u062a\u0642\u062f\u0651\u0645 EH \u0639\u0631\u0636\u0627\u064b \u2014 \u0631\u0641\u0636\u062a \u0644\u062c\u0646\u0629 \u0627\u0644\u0645\u0646\u0627\u0641\u0633\u0627\u062a \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629'],\n"
    " cancelled:['EH did not submit \u2014 the tender was cancelled','\u0644\u0645 \u062a\u0642\u062f\u0651\u0645 EH \u0639\u0631\u0636\u0627\u064b \u2014 \u0623\u064f\u0644\u063a\u064a\u062a \u0627\u0644\u0645\u0646\u0627\u0641\u0633\u0629'],\n"
    " open:['Not submitted yet \u2014 the deadline is still open','\u0644\u0645 \u064a\u064f\u0642\u062f\u0651\u064e\u0645 \u0628\u0639\u062f \u2014 \u0627\u0644\u0645\u0648\u0639\u062f \u0645\u0627 \u0632\u0627\u0644 \u0645\u0641\u062a\u0648\u062d\u0627\u064b'],\n"
    " none:['EH did not submit \u2014 no offer recorded','\u0644\u0645 \u062a\u0642\u062f\u0651\u0645 EH \u0639\u0631\u0636\u0627\u064b \u2014 \u0644\u0627 \u0639\u0631\u0636 \u0645\u0633\u062c\u0651\u0644'],\n"
    " unrecorded:['No submission recorded in the tracker','\u0644\u0627 \u062a\u0642\u062f\u064a\u0645 \u0645\u0633\u062c\u0651\u0644 \u0641\u064a \u0645\u0644\u0641 \u0627\u0644\u0645\u062a\u0627\u0628\u0639\u0629']};\n"
    "function subCell(b){if(b.subdate)return `<span style=\"font-size:10.5px;color:#1A5FAB;font-weight:600;white-space:nowrap\">${b.subdate}</span>`;\n"
    " const w=SUBW[b.sub]||SUBW.unrecorded, col=b.sub=='yes'?'#1A5FAB':(b.sub=='open'?'#3E86C8':'#77868F');\n"
    " return `<div dir=\"auto\" style=\"font-size:10px;color:${col};max-width:150px;line-height:1.35;white-space:normal\">${t(w[0],w[1])}</div>`;}\n"
    "function renderTenders(){\n",
    'feature', 'words for each submission state (EN/AR) and the cell renderer')
rep('app', "   <td style=\"font-size:10.5px;color:#7B8A92;white-space:nowrap\">${b.date||'\\u2014'}</td>\n",
    "   <td style=\"font-size:10.5px;color:#7B8A92;white-space:nowrap\">${b.date||'\\u2014'}</td>\n"
    "   <td style=\"font-size:10.5px;color:#3A4A52;white-space:nowrap\">${b.deadline||`<span style=\"color:#77868F;font-size:10px;white-space:normal\">${t('No deadline recorded','\u0644\u0627 \u0645\u0648\u0639\u062f \u0645\u0633\u062c\u0651\u0644')}</span>`}</td>\n"
    "   <td>${subCell(b)}</td>\n",
    'feature', 'two new cells per tender row')
rep('app', "<th>${t('Launched','الطرح')}</th>",
    "<th>${t('Launched','الطرح')}</th><th>${t('Submission deadline','آجال تقديم العروض')}</th><th>${t('EH submitted','تاريخ تقديم EH')}</th>",
    'feature', 'two new column headings')
rep('app', "'<tr><td colspan=\"10\" style=\"text-align:center;padding:30px;color:#5F7078\">'",
    "'<tr><td colspan=\"12\" style=\"text-align:center;padding:30px;color:#5F7078\">'", 'fix', 'empty row spans the new columns')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for alias, path in (('extract', X), ('analytics', A), ('app', J)):
    open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_bid_subdates'), 'All Tenders — submission deadline and EH date of submission')
print('patched: extract_bids2.py, bid_analytics2.py, app.js')
