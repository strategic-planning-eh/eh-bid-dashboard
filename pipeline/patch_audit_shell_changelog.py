"""patch_audit_shell_changelog.py — What's New builder (build_changelog.py): audit fixes shell-07 and shell-10 (12 Oct 2026).

What was wrong, and what changes:
  shell-07  CHANGES.md had no app code for the Government Tenders tab, so its fixes were filed under "Hub" and their
            links went nowhere. The builder now accepts `tenders` as an app code (the hub opens that tab). Existing
            lines are unaffected.
  shell-10  The Sources tab:
            (a) stamped the stakeholder workbook "Refreshed <this hour>" on every hourly run, although the workbook
                only changes when someone updates it. It now shows the date of the last change to the Stakeholder Map
                file when the build has the history to know it, and otherwise says plainly that it updates when the
                workbook does — no invented time;
            (b) showed a developer instruction ("version not detected — add a marker to the report header") under the
                page's old name. The note is gone, the page is called "Saudi Government Finances 2026", and its
                version and "figures as of" date are read from the page;
            (c) had no line for Regulatory news, Government Tenders, PIF Strategy or the Environment Fund report —
                added, each with the date it carries;
            (d) every source name and note now has an Arabic version (name_ar / note_ar), shown by the hub in Arabic.

Exact-string edits; stops if an anchor is missing. Change table: change_table_audit_shell_changelog.md/.json.
Run once:  python3 pipeline/patch_audit_shell_changelog.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from patchlib import load, rep, FILES, FAILURES, write_change_table

C = os.path.join(HERE, 'build_changelog.py')
if 'def workbook_source(' in open(C, encoding='utf-8').read():
    sys.exit('Already applied — nothing to do.')
load(C, 'cl')

rep('cl', '''import argparse, json, re, sys, os, datetime as dt, unicodedata''',
    '''import argparse, json, re, sys, os, subprocess, datetime as dt, unicodedata''', 'code', 'shell-10: subprocess for the workbook date')

rep('cl', '''NEWS = [('vision2030_dashboard.html', 'Vision 2030 Dashboard', [r'Last reviewed <strong>([^<]+)</strong>', r'const LAST_REVIEWED = "([^"]+)"']),
        ('saudi_fiscal_monitor_2026.html', 'Saudi Fiscal Monitor 2026', [r'(v\\d+ · \\d{2}/\\d{2}/\\d{4})']),
        ('eh_news_intelligence.html', 'Corporate & Government News', [r'<title>[^<]*?·\\s*([^<·]+Update)</title>', r'Generated</[^>]+>\\s*<[^>]+>([^<]+)<']),
        ('pif_intelligence_hub.html', 'PIF Intelligence Hub', [r'<title>PIF annual reports (\\d{4}\\u2013\\d{4})[^<]*</title>'])]  # coverage years; PIF publishes annually

def _dmy_to_iso(s):
    m = re.match(r'(\\d{2})/(\\d{2})/(\\d{4})', s.strip())
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else None

def news_sources(hub):
    out = []
    for fn, name, pats in NEWS:
        p = os.path.join(hub, fn)
        if not os.path.exists(p): continue
        h = open(p, encoding='utf-8').read(); ver = None
        for pat in pats:
            m = re.search(pat, h)
            if m: ver = m.group(1).strip(); break
        iso = _dmy_to_iso(ver.split('· ')[-1]) if ver and '/' in ver else None
        out.append({'name': name, 'refreshed': iso, 'note': (('covers annual reports ' if 'PIF' in name else 'report version: ') + ver) if ver else 'version not detected — add a marker to the report header'})
    return out''',
    '''# (file, name EN, name AR, version pattern, note prefix EN/AR, date pattern (dd/mm/yyyy or yyyy-mm-dd), fixed note EN/AR)
NEWS = [('vision2030_dashboard.html', 'Vision 2030 Dashboard', 'لوحة رؤية 2030', None, None,
         r'Last reviewed <strong>(\\d{2}/\\d{2}/\\d{4})', ('date of the last review', 'تاريخ آخر مراجعة')),
        ('saudi_fiscal_monitor_2026.html', 'Saudi Government Finances 2026', 'مالية الحكومة السعودية 2026', r'<title>[^<]*?\\bversion (\\d+)', ('version ', 'الإصدار '),
         r'figures as of (\\d{2}/\\d{2}/\\d{4})', None),
        ('eh_news_intelligence.html', 'Corporate & Government News', 'أخبار الشركات والحكومة', r'<title>[^<]*?·\\s*([^<·]+Update)</title>', ('edition: ', 'الإصدار: '), None, None),
        ('pif_intelligence_hub.html', 'PIF Intelligence Hub', 'مركز استخبارات صندوق الاستثمارات', r'<title>PIF annual reports (\\d{4}\\u2013\\d{4})[^<]*</title>',
         ('covers annual reports ', 'يغطي التقارير السنوية '), None, None),   # coverage years; PIF publishes annually
        ('pif_strategy_2026_2030.html', 'PIF Strategy 2026–2030', 'استراتيجية صندوق الاستثمارات العامة 2026–2030', None, None, None,
         ("PIF's strategy document for 2026–2030", 'وثيقة استراتيجية الصندوق للأعوام 2026–2030')),
        ('environment_fund_2025.html', 'Environment Fund 2025 Annual Report', 'التقرير السنوي لصندوق البيئة 2025', None, None,
         r'"extracted":\\s*"(\\d{4}-\\d{2}-\\d{2})"', ('date the report was read', 'تاريخ قراءة التقرير')),
        ('etimad_tenders.html', 'Government Tenders (Etimad)', 'المنافسات الحكومية (اعتماد)', None, None,
         r'"last_capture":\\s*"(\\d{4}-\\d{2}-\\d{2})"', ('Etimad is checked every Sunday', 'يُفحص اعتماد كل أحد'))]

AR_MONTHS = dict(zip(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                     ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']))

def _dmy_to_iso(s):
    s = s.strip(); m = re.match(r'(\\d{2})/(\\d{2})/(\\d{4})$', s)
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else (s if re.match(r'\\d{4}-\\d{2}-\\d{2}$', s) else None)

def news_sources(hub):
    """One line per report page, with the version and date the page itself carries. Nothing says "not detected":
    a page without a marker simply shows its name (audit shell-10)."""
    out = []
    for fn, name, name_ar, vpat, pre, dpat, fixed in NEWS:
        p = os.path.join(hub, fn)
        if not os.path.exists(p): continue
        h = open(p, encoding='utf-8').read()
        mv = re.search(vpat, h) if vpat else None
        md = re.search(dpat, h) if dpat else None
        note, note_ar = fixed or ((pre[0] + mv.group(1).strip(), pre[1] + mv.group(1).strip()) if mv else (None, None))
        me = re.match(r'(\\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) Update$', mv.group(1).strip() if mv else '')
        if me:   # "26 August Update" -> "26 August update" / "تحديث 26 أغسطس"
            note, note_ar = pre[0] + me.group(1) + ' ' + me.group(2) + ' update', pre[1] + 'تحديث ' + me.group(1) + ' ' + AR_MONTHS[me.group(2)]
        out.append({'name': name, 'name_ar': name_ar, 'refreshed': _dmy_to_iso(md.group(1)) if md else None, 'note': note, 'note_ar': note_ar})
    gp = os.path.join(hub, 'gov_news.json')   # Regulatory news: the weekly feed carries its own collection time
    if os.path.exists(gp):
        try: g = json.load(open(gp, encoding='utf-8')).get('generated') or None
        except Exception: g = None
        out.append({'name': 'Regulatory news', 'name_ar': 'الأخبار التنظيمية', 'refreshed': g,
                    'note': 'collected every Sunday morning' if g else 'not collected yet', 'note_ar': 'تُجمع كل صباح أحد' if g else 'لم تُجمع بعد'})
    return out

def workbook_source(now):
    """The stakeholder workbook changes only when someone updates it. Its date is the last commit of the Stakeholder Map
    file when the checkout has history; a shallow checkout (the hourly workflow) cannot know it, so no time is invented."""
    src = {'name': 'EH stakeholder workbook', 'name_ar': 'مصنّف أصحاب المصلحة لآفاق البيئة', 'refreshed': None,
           'note': 'updates when the workbook is updated, not hourly', 'note_ar': 'يُحدَّث عند تحديث المصنّف، لا كل ساعة'}
    try:
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
        shallow = subprocess.run(['git', 'rev-parse', '--is-shallow-repository'], cwd=root, capture_output=True, text=True, timeout=20).stdout.strip()
        if shallow == 'false':
            d = subprocess.run(['git', 'log', '-1', '--format=%cI', '--', 'hub/EH_Stakeholder_Map_CURRENT.html'], cwd=root,
                               capture_output=True, text=True, timeout=20).stdout.strip()
            if d: src.update(refreshed=d, note='last change to the Stakeholder Map', note_ar='آخر تغيير على خريطة أصحاب المصلحة')
    except Exception:
        pass
    return src''', 'code', 'shell-10: sources read their own dates; no developer note; new name; four more sources; Arabic names')

rep('cl', '''        {'name': 'EH stakeholder workbook (EH_Stakeholder_Competitive_Map.xlsx)', 'refreshed': now.isoformat(timespec='minutes')},
        {'name': 'Bid tracker (Google Sheets 2025 / 2026)', 'refreshed': now.isoformat(timespec='minutes')},
        {'name': 'MWAN licence register', 'refreshed': None, 'note': 'refresh date recorded in the workbook'}]''',
    '''        workbook_source(now),
        {'name': 'Bid tracker (Google Sheets 2025 / 2026)', 'name_ar': 'جدول تتبع العطاءات (Google Sheets 2025 / 2026)', 'refreshed': now.isoformat(timespec='minutes'),
         'note': 'read every hour', 'note_ar': 'يُقرأ كل ساعة'},
        {'name': 'MWAN licence register', 'name_ar': 'سجل تراخيص المركز الوطني لإدارة النفايات', 'refreshed': None,
         'note': 'refresh date recorded in the workbook', 'note_ar': 'تاريخ التحديث مسجَّل في المصنّف'}]''',
    'copy', 'shell-10: the workbook is no longer stamped with the build time; Arabic names')

rep('cl', '''LINE = re.compile(r'^\\s*(?P<app>stake|bids|clients|news|hub)\\s*\\|''', '''LINE = re.compile(r'^\\s*(?P<app>stake|bids|tenders|clients|news|hub)\\s*\\|''',
    'code', 'shell-07: `tenders` is an app code (Government Tenders tab)')
rep('cl', '''  --changes FILE       CHANGES.md   (app | severity | view? | EN | AR, one fix per line under a ## week heading)''',
    '''  --changes FILE       CHANGES.md   (app | severity | view? | EN | AR, one fix per line under a ## week heading;
                       app = stake | bids | tenders | clients | news | hub)''', 'copy', 'shell-07: usage note lists the app codes')
rep('cl', '''print('CHANGES.md malformed (app | severity | [view |] EN | AR):''', '''print('CHANGES.md malformed (app | severity | [view |] EN | AR; app = stake|bids|tenders|clients|news|hub):''',
    'copy', 'shell-07: error message lists the app codes')

if FAILURES:
    for f in FAILURES: print('FAILED:', f)
    sys.exit(1)
open(C, 'w', encoding='utf-8').write(FILES['cl'])
write_change_table(os.path.join(HERE, 'change_table_audit_shell_changelog'), "What's New builder — audit fixes shell-07/10")
print('patched: pipeline/build_changelog.py')
