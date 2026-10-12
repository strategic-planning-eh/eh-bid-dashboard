"""patch_design_gov.py — EH design system v2 for Regulatory news (hub/government_news.html), 12 Oct 2026.

The regulatory news page is a hand-maintained shell that reads gov_news.json and reg_brief.json when it opens; no
pipeline generator writes the HTML, so the design goes straight into it through exact-string edits that stop if an
anchor is missing:
  • page skin after eh-shared.css: the page's own colour variables now point at the shared tokens (light and dark
    from one place); the green-to-blue header band becomes the deep-navy masthead with EH's contour lines and the
    land-to-sea line, and inside the hub that header turns into a quiet title bar on the page colour
  • KPI tiles lose their blue top edge and the numbers move to the brand display font in ink; section headings lose
    the coloured bar in front of them; labels and table headings in sentence case
  • chips become soft token fills; the monthly-brief verdicts (Risk, Opportunity …) and the source-status dots each
    get a shape as well as a colour (circle, square, diamond, dash), so colour is never the only signal
  • numbers and dates keep their left-to-right isolation in Arabic; small print raised to 12px

Words, numbers, filters and links are unchanged.

Run once:  python3 pipeline/patch_design_gov.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import css_min, load, rep, FILES, FAILURES, write_change_table

P = os.path.join(HERE, '..', 'hub', 'government_news.html')
if 'id="eh-skin"' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'gov')

SKIN = r'''<link rel="stylesheet" href="eh-shared.css">
<style id="eh-skin">
/* EH design system v2 — Regulatory news skin (patch_design_gov.py). Tokens and fonts come from eh-shared.css.
   The page's own <style> follows this block, so its variables are remapped on body (wins over :root) and
   body.dark (more specific than the page's own body.dark). Component rules use a body prefix for the same reason. */
html body,html body.dark{--bg:var(--eh-mist);--card:var(--eh-paper);--ink:var(--eh-ink);--muted:var(--eh-ink-2);--line:var(--eh-line);--chip:var(--eh-tint);
  --gov:var(--eh-sea);--blue:var(--eh-sea);--green:var(--eh-leaf);--amber:#C98A1B;--red:var(--eh-bad);
  background:var(--eh-mist);color:var(--eh-ink);font-size:14.5px;line-height:var(--eh-lh)}
/* masthead (standalone) */
body header{background:var(--eh-deep);color:#fff;padding:20px 24px 22px;position:relative;isolation:isolate}
body.dark header{background:#0A1230}
body header>.eh-contour{color:#6FB6EA;opacity:.5;z-index:-1}
body header::after{content:"";position:absolute;inset-inline:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
[dir=rtl] body header::after{background:linear-gradient(270deg,var(--eh-leaf),var(--eh-sea) 70%,var(--eh-cyan))}
body header h1{font:600 22px/1.25 var(--eh-display);letter-spacing:-.005em;color:#fff}
body header .sub{font-size:13px;opacity:1;color:rgba(255,255,255,.76);margin-top:4px;max-width:90ch}
body .tog{border:1px solid rgba(255,255,255,.32);border-radius:var(--eh-r-ctl)}
body .tog button{font:600 12.5px var(--eh-font);color:rgba(255,255,255,.85);padding:6px 13px}
body .tog button.on{background:#fff;color:var(--eh-deep)}
/* inside the hub the masthead belongs to the hub: this header becomes a quiet title bar on the page colour */
html.eh-embedded body header,html.eh-embedded body.dark header{background:transparent;color:var(--eh-ink);padding:18px 22px 2px;max-width:1380px;margin:0 auto}
html.eh-embedded body header::after,html.eh-embedded body header>.eh-contour{display:none}
html.eh-embedded body header h1{color:var(--eh-ink);font-size:21px}
html.eh-embedded body header .sub{color:var(--eh-ink-2)}
html.eh-embedded body .tog{border-color:var(--eh-line);background:var(--eh-paper)}
html.eh-embedded body .tog button{color:var(--eh-ink-2)}
html.eh-embedded body .tog button.on{background:var(--eh-sea);color:#fff}
/* stamp + KPI tiles: no coloured edges; numbers lead */
body .stamp{font-size:12.5px;color:var(--eh-ink-3);margin:2px 0 14px}
body .stamp b{color:var(--eh-ink);font-weight:600;unicode-bidi:isolate}
body .kstrip{gap:12px;margin-bottom:18px}
body .kc{background:var(--eh-paper);border:1px solid var(--eh-line);border-top:1px solid var(--eh-line);border-radius:12px;padding:15px 16px 14px;box-shadow:var(--eh-shadow)}
body .kc .v{font:600 27px/1.08 var(--eh-display);color:var(--eh-ink);unicode-bidi:isolate}
[dir=rtl] body .kc .v{text-align:right}
body .kc .l{font-size:13px;color:var(--eh-ink-2);margin-top:7px;line-height:1.4}
/* panels */
body .card{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:var(--eh-r-panel);padding:18px 20px;margin-bottom:16px;box-shadow:var(--eh-shadow);color:var(--eh-ink)}
body .card h2{font:600 18px/1.35 var(--eh-display);color:var(--eh-ink);margin-bottom:4px}
body .card h2::before{display:none}
body .card .note{font-size:13px;color:var(--eh-ink-2);line-height:1.55;margin-bottom:12px}
body details.card summary{font:600 15px var(--eh-display);color:var(--eh-ink)}
/* monthly brief */
body .bsum{font-size:15px;line-height:1.7;color:var(--eh-ink)}
body .bgrid h3{font:600 13px var(--eh-font) !important;letter-spacing:0;text-transform:none;color:var(--eh-ink-2);margin:8px 0 6px}
body .bb{font-size:13.5px;line-height:1.65;color:var(--eh-ink-2);border-top:1px solid var(--eh-line)}
body .bmeta{font-size:12px;color:var(--eh-ink-3)}
body .warn{font-size:13px;background:var(--eh-warn-bg);color:var(--eh-ink);border-inline-start:3px solid var(--eh-warn);border-radius:0 8px 8px 0;padding:10px 13px}
[dir=rtl] body .warn{border-radius:8px 0 0 8px}
body .ref{min-width:18px;height:18px;line-height:18px;font:600 11px var(--eh-font);border-radius:5px;background:var(--eh-tint);color:var(--eh-sea-ink);border:0;unicode-bidi:isolate}
body .ref:hover{background:var(--eh-info-bg)}
body .ref.miss{color:var(--eh-ink-3)}
/* month tabs and period tabs */
body .tabs button{font:600 13px var(--eh-font);background:transparent;border:1px solid var(--eh-line);color:var(--eh-ink-2);border-radius:var(--eh-r-chip);padding:6px 14px}
body .tabs button:hover:not(.on){background:var(--eh-tint);color:var(--eh-ink)}
body .tabs button.on{background:var(--eh-sea);border-color:var(--eh-sea);color:#fff}
/* chips: soft fills from the token set */
body .chip{font-size:11.5px;font-weight:600;border-radius:var(--eh-r-chip);padding:2px 9px;color:var(--eh-ink-2);background:var(--eh-muted-bg);border:0}
body .chip.body{background:var(--eh-info-bg);color:var(--eh-info)}
body .chip.src-official{background:var(--eh-good-bg);color:var(--eh-good)}
body .chip.src-spa{background:var(--eh-muted-bg);color:var(--eh-muted)}
body .chip.tag{background:var(--eh-tint);color:var(--eh-ink-2);border:0}
body .chip.lang{background:transparent;color:var(--eh-ink-3);border:1px solid var(--eh-line)}
body button.chip.body{background:var(--eh-sea);color:#fff}
/* brief verdicts: a word plus a shape */
body .chip[class*="kind-"]{display:inline-flex;align-items:center;gap:5px;vertical-align:1px}
body .chip[class*="kind-"]::before{content:"";width:7px;height:7px;flex:none;background:currentColor}
body .chip.kind-risk{background:var(--eh-bad-bg);color:var(--eh-bad)}body .chip.kind-risk::before{border-radius:1px;transform:rotate(45deg)}
body .chip.kind-opportunity{background:var(--eh-good-bg);color:var(--eh-good)}body .chip.kind-opportunity::before{border-radius:50%}
body .chip.kind-licensing{background:var(--eh-info-bg);color:var(--eh-info)}body .chip.kind-licensing::before{background:none;border:1.5px solid currentColor;border-radius:50%}
body .chip.kind-tender{background:var(--eh-warn-bg);color:var(--eh-warn)}body .chip.kind-tender::before{border-radius:1px}
body .chip.kind-watch{background:var(--eh-muted-bg);color:var(--eh-muted)}body .chip.kind-watch::before{height:2px}
/* bodies followed: source status as a shape as well as a colour */
body .bodies{gap:10px}
body .bd{background:var(--eh-paper);border:1px solid var(--eh-line);border-radius:12px;padding:11px 13px;transition:border-color var(--eh-dur-1) var(--eh-ease),background-color var(--eh-dur-1) var(--eh-ease)}
body .bd:hover{border-color:var(--eh-sea)}
body .bd.on{outline:0;border-color:var(--eh-sea);box-shadow:inset 0 0 0 1px var(--eh-sea);background:var(--eh-info-bg)}
body .bd .n{font-weight:600;font-size:13.5px;color:var(--eh-ink)}
body .bd .m{font-size:12px;color:var(--eh-ink-3)}
body .dot{width:8px;height:8px;background:var(--eh-ink-3)}
body .dot.st-ok{background:var(--eh-good);border-radius:50%}
body .dot.st-empty,body .dot.st-stale{background:#C98A1B;border-radius:1px}
body .dot.st-error{background:var(--eh-bad);border-radius:1px;transform:rotate(45deg)}
body .dot.st-skipped,body .dot.st-robots{background:var(--eh-ink-3);height:2.5px;border-radius:0}
/* filters */
body .fl select,body .fl input{font:13px var(--eh-font);padding:7px 10px;border:1px solid var(--eh-line);border-radius:var(--eh-r-ctl);background:var(--eh-paper);color:var(--eh-ink)}
body .fl select:focus,body .fl input:focus{border-color:var(--eh-sea);box-shadow:0 0 0 3px var(--eh-info-bg);outline:0}
/* announcements */
body .it{border-top:1px solid var(--eh-line);padding:12px 0}
body .it .d{font-size:12.5px;color:var(--eh-ink-3)}
body .it .d small{font-size:12px}
body .it .t{font-size:14px;line-height:1.55}
body .it .t a{color:var(--eh-ink);font-weight:600}
body .it .t a:hover{color:var(--eh-sea)}
body .empty{background:var(--eh-tint);color:var(--eh-ink-2);border-radius:12px}
/* source status table */
body table.t{font-size:13px}
body table.t th{font-size:12.5px;font-weight:600;letter-spacing:0;text-transform:none;color:var(--eh-ink-2);background:var(--eh-tint);border-bottom:1px solid var(--eh-line);padding:8px 9px}
body table.t td{border-bottom:1px solid var(--eh-line);padding:8px 9px}
body .foot{font-size:12px;color:var(--eh-ink-3)}
@media(max-width:640px){
  body header{padding:14px 16px 16px}
  body header h1{font-size:18px}
  main{padding:14px 16px 36px}
  body .kstrip{grid-template-columns:repeat(2,minmax(0,1fr))}
  body .kc .v{font-size:23px}
  body .fl input{min-width:0;flex:1 1 100%}
  body .card{padding:14px 15px}
}
</style>'''
SKIN = css_min(SKIN)   # keep page growth small

rep('gov', '<link rel="stylesheet" href="eh-shared.css">', SKIN, 'design', 'page skin after the shared design system')
rep('gov', '<header>\n <div><h1 id="title"></h1>', '<header data-eh-contour="6">\n <div><h1 id="title"></h1>', 'design', 'standalone masthead contour lines')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['gov'])
write_change_table(os.path.join(HERE, 'change_table_design_gov'), 'Design system v2 — Regulatory news')
print('patched: hub/government_news.html')
