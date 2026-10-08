"""patch_etimad_analyst.py — adds the "Analyst view" to the end of the Government Tenders (Etimad) tab (Stage 2, approved 7 Oct 2026).

What it changes (exact-string edits, fails loudly if an anchor is missing):
  • build_etimad.py      read the "analyst_notes" tab from the private sheet; call etimad_analyst.analyst() to join
                         pipeline/vision_umbrella.json with the market windows, the captured tenders, the stakeholder map
                         and the notes; store the result as "analyst" in etimad_tenders.json (never committed).
  • build_etimad_page.py add the section's CSS, HTML (after the Stakeholder view card) and JS; render it on every render().
  • visual_check.py      the Etimad page must show the analyst picture and at least one note, or its empty state.
New files (not patched): etimad_analyst.py, vision_umbrella.json.

Run once:  python3 pipeline/patch_etimad_analyst.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

B, P, V = (os.path.join(HERE, f) for f in ('build_etimad.py', 'build_etimad_page.py', 'visual_check.py'))
if 'etimad_analyst' in open(B, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(B, 'build'); load(P, 'page'); load(V, 'vcheck')

# ---------------- build_etimad.py
rep('build', "    return cards, rows('decisions'), rows('agency_bridge'), rows('counts'), rows('market')\n",
    "    return cards, rows('decisions'), rows('agency_bridge'), rows('counts'), rows('market'), rows('analyst_notes')\n",
    'data', 'read_sheet also returns the analyst_notes tab')
rep('build', "        cards, decisions, bridge_rows, counts, market = read_sheet(a.sheet)\n",
    "        cards, decisions, bridge_rows, counts, market, note_rows = read_sheet(a.sheet)\n", 'data', 'unpack notes rows')
rep('build', "        cards, decisions, bridge_rows, counts, market = read_raw_dir(a.raw), [], [], [], []\n",
    "        cards, decisions, bridge_rows, counts, market, note_rows = read_raw_dir(a.raw), [], [], [], [], []\n", 'data', 'local mode: no notes')
rep('build', "        cards, decisions, bridge_rows, counts, market = [], [], [], [], []\n",
    "        cards, decisions, bridge_rows, counts, market, note_rows = [], [], [], [], [], []\n", 'data', 'no input: no notes')
rep('build', "    out['market'] = build_market(market)\n",
    "    out['market'] = build_market(market)\n"
    "    # Analyst view: umbrella (committed, no Etimad data) + market windows + tenders + map + notes (private sheet)\n"
    "    from etimad_analyst import analyst\n"
    "    out['analyst'] = analyst(market, out['tenders'], a.map, note_rows, bidraw=a.bidraw)\n",
    'feature', 'join the Analyst view')
rep('build', "    print(f\"Etimad: {out['count']} tenders ({rel} relevant), last capture {out['last_capture']} → {a.out}\")\n",
    "    print(f\"Etimad: {out['count']} tenders ({rel} relevant), last capture {out['last_capture']} → {a.out}\")\n"
    "    an = out.get('analyst') or {}\n"
    "    print(f\"Analyst view: {len(an.get('windows') or [])} market windows, {len(an.get('notes') or [])} notes ({an.get('notes_month')}), reviewed {an.get('reviewed')}\")\n",
    'log', 'log the analyst join')

# ---------------- build_etimad_page.py
rep('page', "import json, os, sys, collections\n",
    "import json, os, sys, collections\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport etimad_analyst as AV\n",
    'feature', 'import the analyst section')
rep('page', "<style>{CSS}</style></head>", "<style>{CSS}{AV.CSS}</style></head>", 'feature', 'analyst CSS')
rep('page', """<div class="foot" data-en="Built from the private EH Etimad data sheet.""",
    """{AV.HTML}\n<div class="foot" data-en="Built from the private EH Etimad data sheet.""", 'feature', 'analyst card after the Stakeholder view')
rep('page', "<script>{JS}</script>", "<script>{JS}{AV.JS}</script>", 'feature', 'analyst JS')
rep('page', "  renderMarket();\n  document.querySelectorAll('#list th')",
    "  renderMarket();\n  if(typeof renderAnalyst==='function')renderAnalyst();\n  document.querySelectorAll('#list th')", 'feature', 'render the analyst view with the page')

# ---------------- visual_check.py
rep('vcheck', "    'etimad_tenders.html':             dict(kpi=6, tables=0, svgs=0, nodiff=True),   # content changes with each Sunday capture\n",
    "    'etimad_tenders.html':             dict(kpi=6, tables=0, svgs=0, nodiff=True, analyst=True),   # content changes with each Sunday capture\n",
    'check', 'Etimad page: require the analyst section')
rep('vcheck', "                    if m['words'] < 60: probs.append(f\"page nearly empty ({m['words']} words)\")\n",
    "                    if m['words'] < 60: probs.append(f\"page nearly empty ({m['words']} words)\")\n"
    "                    if want.get('analyst'):   # Analyst view: its picture and at least one note, or its stated empty state\n"
    "                        av = pg.evaluate(\"(()=>({flow:!!document.querySelector('#av-flow svg'),notes:document.querySelectorAll('#av .avn').length,\"\n"
    "                                         \"empty:!!document.querySelector('#av .empty-analyst,#av .empty-notes')}))()\")\n"
    "                        m['analyst'] = av\n"
    "                        if not ((av['flow'] and av['notes'] >= 1) or av['empty']):\n"
    "                            probs.append(f\"analyst view incomplete (picture {av['flow']}, notes {av['notes']})\")\n",
    'check', 'analyst view render check')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
for alias, path in (('build', B), ('page', P), ('vcheck', V)):
    open(path, 'w', encoding='utf-8').write(FILES[alias])
write_change_table(os.path.join(HERE, 'change_table_etimad_analyst'), 'Government Tenders — Analyst view (Stage 2)')
print('patched: build_etimad.py, build_etimad_page.py, visual_check.py')
