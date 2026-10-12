# What's New builder — audit fixes shell-07/10

Generated 2026-10-12 14:26 · 6 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | cl | exact | code | shell-10: subprocess for the workbook date | 1 | ✓ |
| 2 | cl | exact | code | shell-10: sources read their own dates; no developer note; new name; four more sources; Arabic names | 1 | ✓ |
| 3 | cl | exact | copy | shell-10: the workbook is no longer stamped with the build time; Arabic names | 1 | ✓ |
| 4 | cl | exact | code | shell-07: `tenders` is an app code (Government Tenders tab) | 1 | ✓ |
| 5 | cl | exact | copy | shell-07: usage note lists the app codes | 1 | ✓ |
| 6 | cl | exact | copy | shell-07: error message lists the app codes | 1 | ✓ |

## Edit detail

### 1. cl — shell-10: subprocess for the workbook date

**Old**
```
import argparse, json, re, sys, os, datetime as dt, unicodedata
```
**New**
```
import argparse, json, re, sys, os, subprocess, datetime as dt, unicodedata
```

### 2. cl — shell-10: sources read their own dates; no developer note; new name; four more sources; Arabic names

**Old**
```
NEWS = [('vision2030_dashboard.html', 'Vision 2030 Dashboard', [r'Last reviewed <strong>([^<]+)</strong>', r'const LAST_REVIEWED = "([^"]+)"']),
        ('saudi_fiscal_monitor_2026.html', 'Saudi Fiscal Monitor 2026', [r'(v\d+ · \d{2}/\d{2}/\d{4})']),
        ('eh_news_intelligence.html', 'Corporate & Government News', [r'<title>[^<]*?·\s*([^<·]+Update)</title>', r'Generated</[^>]+>\s*<[^>]+>([^<]+
```
**New**
```
# (file, name EN, name AR, version pattern, note prefix EN/AR, date pattern (dd/mm/yyyy or yyyy-mm-dd), fixed note EN/AR)
NEWS = [('vision2030_dashboard.html', 'Vision 2030 Dashboard', 'لوحة رؤية 2030', None, None,
         r'Last reviewed <strong>(\d{2}/\d{2}/\d{4})', ('date of the last review', 'تاريخ آخر مراجعة')),
        ('saudi_fiscal_monitor_2026.html', 'Saudi Government Finances 2026', 'ما
```

### 3. cl — shell-10: the workbook is no longer stamped with the build time; Arabic names

**Old**
```
        {'name': 'EH stakeholder workbook (EH_Stakeholder_Competitive_Map.xlsx)', 'refreshed': now.isoformat(timespec='minutes')},
        {'name': 'Bid tracker (Google Sheets 2025 / 2026)', 'refreshed': now.isoformat(timespec='minutes')},
        {'name': 'MWAN licence register', 'refreshed': None, 'note': 'refresh date recorded in the workbook'}]
```
**New**
```
        workbook_source(now),
        {'name': 'Bid tracker (Google Sheets 2025 / 2026)', 'name_ar': 'جدول تتبع العطاءات (Google Sheets 2025 / 2026)', 'refreshed': now.isoformat(timespec='minutes'),
         'note': 'read every hour', 'note_ar': 'يُقرأ كل ساعة'},
        {'name': 'MWAN licence register', 'name_ar': 'سجل تراخيص المركز الوطني لإدارة النفايات', 'refreshed': None,
         'note': 're
```

### 4. cl — shell-07: `tenders` is an app code (Government Tenders tab)

**Old**
```
LINE = re.compile(r'^\s*(?P<app>stake|bids|clients|news|hub)\s*\|
```
**New**
```
LINE = re.compile(r'^\s*(?P<app>stake|bids|tenders|clients|news|hub)\s*\|
```

### 5. cl — shell-07: usage note lists the app codes

**Old**
```
  --changes FILE       CHANGES.md   (app | severity | view? | EN | AR, one fix per line under a ## week heading)
```
**New**
```
  --changes FILE       CHANGES.md   (app | severity | view? | EN | AR, one fix per line under a ## week heading;
                       app = stake | bids | tenders | clients | news | hub)
```

### 6. cl — shell-07: error message lists the app codes

**Old**
```
print('CHANGES.md malformed (app | severity | [view |] EN | AR):
```
**New**
```
print('CHANGES.md malformed (app | severity | [view |] EN | AR; app = stake|bids|tenders|clients|news|hub):
```
