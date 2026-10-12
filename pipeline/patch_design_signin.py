"""patch_design_signin.py — EH design system v2 for the sign-in card the sealed hub shows first (12 Oct 2026).

encrypt_site.py writes a small unlock page for every sealed file. It is the first thing every reader sees, so it now
opens on the same deep-navy field with EH's bathymetric contour lines as the hub masthead, the logo on its white tile,
the brand fonts (served unsealed from vendor/fonts/), and a solid EH-blue button. Words, fields and behaviour are
unchanged. It follows the device's light/dark preference as before.

Run once:  python3 pipeline/patch_design_signin.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table
P = os.path.join(HERE, 'encrypt_site.py')
if 'EH design system v2' in open(P, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(P, 'enc')
CONTOUR = """%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 800' preserveAspectRatio='none'%3E%3Cg fill='none' stroke='%236FB6EA' stroke-width='1.2'%3E%3Cpath d='M0 84L30 83L60 80L90 77L120 75L150 72L180 71L210 70L240 69L270 69L300 69L330 67L360 65L390 61L420 57L450 52L480 48L510 45L540 43L570 44L600 45L630 48L660 51L690 55L720 58L750 60L780 62L810 62L840 63L870 63L900 64L930 67L960 70L990 73L1020 77L1050 81L1080 84L1110 85L1140 84L1170 82L1200 79' opacity='0.10'/%3E%3Cpath d='M0 150L30 148L60 145L90 141L120 137L150 133L180 131L210 129L240 128L270 128L300 127L330 126L360 125L390 122L420 119L450 116L480 112L510 110L540 109L570 110L600 112L630 116L660 120L690 125L720 129L750 132L780 135L810 136L840 137L870 137L900 138L930 139L960 141L990 144L1020 147L1050 150L1080 152L1110 153L1140 152L1170 149L1200 146' opacity='0.12'/%3E%3Cpath d='M0 213L30 211L60 207L90 203L120 198L150 194L180 190L210 188L240 187L270 186L300 186L330 186L360 186L390 185L420 183L450 181L480 179L510 177L540 177L570 178L600 181L630 185L660 190L690 196L720 201L750 205L780 208L810 209L840 210L870 210L900 210L930 210L960 211L990 213L1020 215L1050 217L1080 218L1110 218L1140 217L1170 215L1200 211' opacity='0.15'/%3E%3Cpath d='M0 275L30 273L60 268L90 264L120 258L150 253L180 250L210 247L240 246L270 246L300 247L330 248L360 249L390 249L420 249L450 248L480 247L510 246L540 247L570 248L600 251L630 256L660 261L690 267L720 273L750 277L780 280L810 282L840 282L870 281L900 280L930 280L960 279L990 280L1020 280L1050 282L1080 282L1110 283L1140 281L1170 279L1200 275' opacity='0.17'/%3E%3Cpath d='M0 335L30 333L60 329L90 324L120 319L150 314L180 310L210 307L240 306L270 307L300 308L330 310L360 313L390 315L420 316L450 316L480 317L510 317L540 318L570 320L600 323L630 327L660 332L690 338L720 343L750 348L780 351L810 353L840 353L870 351L900 349L930 347L960 346L990 345L1020 345L1050 345L1080 345L1110 345L1140 345L1170 343L1200 340' opacity='0.19'/%3E%3Cpath d='M0 395L30 392L60 389L90 384L120 379L150 375L180 371L210 369L240 368L270 369L300 372L330 375L360 379L390 382L420 385L450 387L480 388L510 389L540 390L570 392L600 394L630 398L660 403L690 408L720 413L750 417L780 420L810 421L840 421L870 419L900 416L930 413L960 411L990 409L1020 408L1050 407L1080 408L1110 408L1140 408L1170 406L1200 404' opacity='0.21'/%3E%3Cpath d='M0 454L30 452L60 449L90 445L120 441L150 437L180 434L210 433L240 433L270 434L300 438L330 442L360 446L390 451L420 455L450 458L480 460L510 461L540 462L570 464L600 466L630 469L660 473L690 477L720 481L750 485L780 487L810 488L840 487L870 485L900 482L930 478L960 475L990 472L1020 470L1050 470L1080 470L1110 470L1140 471L1170 471L1200 470' opacity='0.24'/%3E%3Cpath d='M0 513L30 512L60 510L90 508L120 505L150 502L180 500L210 499L240 499L270 501L300 505L330 510L360 515L390 521L420 525L450 529L480 532L510 533L540 534L570 535L600 536L630 538L660 541L690 544L720 547L750 550L780 552L810 553L840 552L870 549L900 546L930 542L960 538L990 535L1020 533L1050 532L1080 533L1110 534L1140 535L1170 537L1200 537' opacity='0.26'/%3E%3Cpath d='M0 573L30 573L60 572L90 571L120 570L150 568L180 567L210 566L240 567L270 570L300 574L330 579L360 585L390 591L420 596L450 600L480 603L510 604L540 605L570 605L600 605L630 606L660 607L690 609L720 611L750 614L780 615L810 616L840 615L870 612L900 609L930 605L960 601L990 598L1020 596L1050 596L1080 597L1110 599L1140 602L1170 604L1200 606' opacity='0.28'/%3E%3Cpath d='M0 635L30 636L60 637L90 637L120 637L150 636L180 636L210 636L240 637L270 640L300 644L330 649L360 655L390 661L420 666L450 670L480 673L510 674L540 674L570 673L600 672L630 671L660 672L690 672L720 674L750 675L780 677L810 677L840 677L870 675L900 672L930 669L960 666L990 663L1020 661L1050 661L1080 663L1110 666L1140 669L1170 673L1200 677' opacity='0.30'/%3E%3Cpath d='M0 698L30 700L60 703L90 704L120 706L150 706L180 706L210 707L240 708L270 710L300 714L330 719L360 724L390 729L420 734L450 738L480 741L510 741L540 741L570 739L600 737L630 736L660 735L690 734L720 735L750 736L780 738L810 738L840 739L870 738L900 736L930 733L960 731L990 729L1020 728L1050 729L1080 731L1110 735L1140 739L1170 744L1200 749' opacity='0.33'/%3E%3C/g%3E%3C/svg%3E"""
OLD_CSS = open(P, encoding='utf-8').read().split(':root{--bg:#F4F7F5',1)[1].split('.quiet .box{display:none}',1)[0]
NEW_CSS = r'''/* EH design system v2 sign-in (patch_design_signin.py) */
@font-face{font-family:"EH Display";src:url("vendor/fonts/montserrat-latin-var.woff2") format("woff2");font-weight:100 900;font-display:swap;unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:"EH Display";src:url("vendor/fonts/alexandria-arabic-var.woff2") format("woff2");font-weight:100 900;font-display:swap;unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFC}
@font-face{font-family:"EH Sans";src:url("vendor/fonts/encode-sans-latin-var.woff2") format("woff2");font-weight:100 900;font-stretch:75% 125%;font-display:swap;unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:"EH Sans";src:url("vendor/fonts/plex-sans-arabic-400.woff2") format("woff2");font-weight:400;font-display:swap;unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFC}
:root{--bg:#1B2A6E;--card:#fff;--ink:#15224D;--muted:#46546F;--line:#D9E3DF;--green:#2E7A37;--blue:#0072BB;--red:#B23F2B;--field:#F2F6F4}
@media(prefers-color-scheme:dark){:root{--bg:#0A1230;--card:#15214A;--ink:#E9EEF7;--muted:#B8C4DA;--line:#2A3A6B;--field:#0D1736}}
html,body{margin:0;height:100%}body{font-family:"EH Sans","Segoe UI",Tahoma,Arial,sans-serif;background:var(--bg) url("data:image/svg+xml,__CONTOUR__") center/cover no-repeat;color:var(--ink);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}
.box{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:28px 30px;width:100%;max-width:410px;box-shadow:0 24px 60px -24px rgba(0,0,0,.55);position:relative;overflow:hidden}
.box::before{content:"";position:absolute;inset-inline:0;top:0;height:3px;background:linear-gradient(90deg,#54AB5D,#0072BB 70%,#00A0E0)}
.box img{height:44px;display:block;margin:0 auto 14px;background:#fff;border-radius:11px;padding:4px 6px}
h1{font:600 17px/1.3 "EH Display","Segoe UI",sans-serif;margin:0 0 3px;text-align:center}.ar{text-align:center;font-size:14px;color:var(--muted);margin-bottom:20px;line-height:1.7}
label{display:block;font-size:13px;color:var(--muted);margin:10px 0 5px}
input[type=password]{width:100%;box-sizing:border-box;font:inherit;font-size:16px;padding:11px 13px;border:1px solid var(--line);border-radius:9px;background:var(--field);color:var(--ink);direction:ltr}
input[type=password]:focus{outline:2px solid #0072BB;outline-offset:1px}
.row{display:flex;align-items:center;gap:8px;margin:12px 0 16px;font-size:13px;color:var(--muted)}
button{width:100%;font:600 15px "EH Sans","Segoe UI",sans-serif;padding:12px;border:0;border-radius:9px;background:#0072BB;color:#fff;cursor:pointer}button:hover{background:#00609E}button:disabled{opacity:.6}
.err{color:var(--red);font-size:13px;min-height:18px;margin-top:8px;text-align:center}
.foot{font-size:12px;color:var(--muted);text-align:center;margin-top:16px;line-height:1.6}
@media (prefers-reduced-motion:no-preference){.box{animation:ehIn .42s cubic-bezier(.2,.7,.2,1) both}@keyframes ehIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}}
'''.replace('__CONTOUR__', CONTOUR)
s = FILES['enc']; a = ':root{--bg:#F4F7F5' + OLD_CSS + '.quiet .box{display:none}'
rep('enc', a, NEW_CSS + '.quiet .box{display:none}', 'design', 'sign-in card in the EH design system')
if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(P, 'w', encoding='utf-8').write(FILES['enc'])
write_change_table(os.path.join(HERE, 'change_table_design_signin'), 'Design system v2 — sign-in card')
print('patched: encrypt_site.py')
