# Change table — Licence Map white-space section removed (5 Nov 2026)

Generated 2026-11-05 10:10 · 1 edits · 0 failures

| # | File | Kind | Category | Note | Occurrences | OK |
|---|---|---|---|---|---|---|
| 1 | map | regex | licence-map | Licence Map: white-space heading, table and closing sentence removed | 1 | ✓ |

## Edit detail

### 1. map — Licence Map: white-space heading, table and closing sentence removed

**Old**
```
  h\+='<div class=\"biz-sec\">'\+t\('White space — licences almost no one holds \(opportunity\)'.*?\n(  document\.getElementById\('licView'\)\.innerHTML=h;)
```
**New**
```
  /* 5 Nov 2026: 'White space — licences almost no one holds' section removed at Youssef's request (data kept in BA.licenses.white_space) */\n\1
```
