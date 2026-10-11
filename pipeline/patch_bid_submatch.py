"""patch_bid_submatch.py — match EH's bid submissions against every submission column in the bid tracker (11 Oct 2026).

Why: the tracker's "Date of submission" column is often left blank or not updated, and the client's
"Submission Deadline" is often not updated when the client extends it. The tracker (EH-WIN-02-F01) is the
only source of truth, so the submission is now read from all of its submission evidence, not one column:

  "Date of submission / تاريخ التقديم"            date EH recorded as submitted (preferred when present)
  "العرض الفني / Technical Proposal"              date the technical proposal went in
  "العرض المالي / Financial Proposal"             date the financial proposal went in
  "Status of submission / حالة التقديم"           Yes / No
  "Date of Amendment", "تاريخ الترسية"            carried for reference (award date shown where recorded)

Rules (nothing is guessed from a title):
  • EH submission date = "Date of submission" when filled, otherwise the earlier of the two proposal dates.
  • If EH's submission date is later than the recorded deadline, the deadline is treated as extended but not
    updated in the tracker (deadline_stale) — it is NOT shown as a late submission.
  • If "Date of submission" and the proposal dates differ by more than 3 days, the row carries the gap (subgap)
    so the table can show both.
  • "Status of submission = No" on a tender that has an award result is a contradiction (sub_conflict) to fix
    in the tracker.

What it changes (exact-string edits; stops if an anchor is missing):
  • extract_bids2.py   read the proposal-date, amendment-date and award-date columns; derive ehsubdate/subsrc/subgap.
  • bid_analytics2.py  submission state uses ehsubdate; bidlist rows carry subsrc, deadline_stale, subgap,
                       sub_conflict, awarddate and a plain `submitted` flag.

Run once:  python3 pipeline/patch_bid_submatch.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

X, A = (os.path.join(HERE, f) for f in ('extract_bids2.py', 'bid_analytics2.py'))
if 'ehsubdate' in open(X, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(X, 'extract'); load(A, 'analytics')

# ---------------- extract_bids2.py
rep('extract',
    "        elif h.startswith('Status of submission') or h.startswith('حالة التقديم'): m['substatus']=c\n",
    "        elif h.startswith('Status of submission') or h.startswith('حالة التقديم'): m['substatus']=c\n"
    "        elif h.startswith('العرض الفني') or h.startswith('Technical Proposal'): m['techprop']=c\n"
    "        elif h.startswith('العرض المالي') or h.startswith('Financial Proposal'): m['finprop']=c\n"
    "        elif h.startswith('Date of Amendment'): m['amenddate']=c\n"
    "        elif h.startswith('تاريخ الترسية') or h.startswith('Award date'): m['awarddate']=c\n",
    'data', 'map the proposal-date, amendment-date and award-date columns')
rep('extract',
    "            subdate=subdstr(g('subdate')), substatus=substat(g('substatus')), subcol=('subdate' in m or 'substatus' in m),\n",
    "            subdate=subdstr(g('subdate')), substatus=substat(g('substatus')), subcol=('subdate' in m or 'substatus' in m),\n"
    "            techdate=subdstr(g('techprop')), findate=subdstr(g('finprop')),\n"
    "            amenddate=subdstr(g('amenddate')), awarddate=subdstr(g('awarddate')),\n",
    'data', 'carry proposal, amendment and award dates into bidraw2.json')
rep('extract',
    "        b['value']=b['winval'] if b['winval'] else b['offer']\n        allbids.append(b)\n",
    "        b['value']=b['winval'] if b['winval'] else b['offer']\n"
    "        # EH submission date: the tracker's own date first, else the earlier proposal date (11 Oct 2026)\n"
    "        _pd=sorted(x for x in (b['techdate'],b['findate']) if x)\n"
    "        b['ehsubdate']=b['subdate'] or (_pd[0] if _pd else None)\n"
    "        b['subsrc']='tracker' if b['subdate'] else ('proposal' if _pd else None)\n"
    "        b['subgap']=None\n"
    "        if b['subdate'] and _pd:\n"
    "            _g=(datetime.date.fromisoformat(b['subdate'])-datetime.date.fromisoformat(_pd[0])).days\n"
    "            if abs(_g)>3: b['subgap']=dict(proposal=_pd[0], days=_g)\n"
    "        allbids.append(b)\n",
    'data', 'derive EH submission date, its source and any gap between the two records')

# ---------------- bid_analytics2.py
rep('analytics',
    "        if b.get('subdate'): return 'date'\n",
    "        if b.get('ehsubdate') or b.get('subdate'): return 'date'\n",
    'data', 'a proposal date counts as a dated submission')
rep('analytics',
    "            deadline=b.get('submit') or None, subdate=b.get('subdate') or None, sub=substate(b),\n",
    "            deadline=b.get('submit') or None, subdate=(b.get('ehsubdate') or b.get('subdate') or None), sub=substate(b),\n"
    "            subsrc=b.get('subsrc'), subgap=b.get('subgap'), awarddate=b.get('awarddate'),\n"
    "            submitted=substate(b) in ('date','yes'),\n"
    "            deadline_stale=bool(b.get('submit') and (b.get('ehsubdate') or b.get('subdate')) and (b.get('ehsubdate') or b.get('subdate'))>b['submit']),\n"
    "            sub_conflict=bool(b.get('substatus')=='No' and (b.get('decided') or b.get('eh_won'))),\n",
    'data', 'bidlist rows carry the submission evidence the All Tenders tab needs')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for alias, path in (('extract', X), ('analytics', A)):
    open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_bid_submatch'), 'Bid tracker — EH submissions matched across all submission columns')
print('patched: extract_bids2.py, bid_analytics2.py')
