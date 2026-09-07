"""patchlib.py — exact-string / regex patch framework with an auto-generated change table.

Interface (kept compatible with the pattern used by patch_map.py):
    load(path, alias)                       -> registers a file under alias; FILES[alias] holds its text
    rep(alias, old, new, category, note, count=1)          exact-string replacement; `new` is NFKC-normalised (Arabic script only); fails loudly if count mismatch
    NOTE: whole-file normalisation is deliberately NOT applied — tatweel is used intentionally as a prefix connector (لـ, بـ) in existing copy.
    rep_re(alias, pattern, repl, category, note, count=1)  regex replacement (re.DOTALL); fails loudly if count mismatch
    rep_t(alias, key, en, ar, category, note, count=1)     replaces a t('key','...') bilingual call pair
    nfkc(s)                                 -> NFKC + tatweel / zero-width removal
    write_files(outdir)                     -> writes patched copies (originals untouched)
    write_change_table(stem)                -> stem.md + stem.json
    FAILURES                                -> list of failed edits (must be empty before delivery)

NOTE: the repo's own patchlib.py (strategic-planning-eh/eh-bid-dashboard) was not reachable from the build
sandbox (private repo). This file re-implements the documented interface; diff against the repo copy before
merging and keep whichever is canonical.
"""
import re, json, os, unicodedata, datetime

FILES, ORIG, CHANGES, FAILURES = {}, {}, [], []

def nfkc(s):
    """NFKC applied only to Arabic-script characters (presentation forms FB50–FDFF / FE70–FEFF fold to base letters);
    Latin typography (m³, …, ²) is left untouched. Tatweel and zero-width characters are removed."""
    out = []
    for ch in s:
        o = ord(ch)
        if 0x0600 <= o <= 0x06FF or 0x0750 <= o <= 0x077F or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF:
            out.append(unicodedata.normalize('NFKC', ch))
        else:
            out.append(ch)
    return re.sub('[\u0640\u200b\u200c\u200d\ufeff]', '', ''.join(out))

def load(path, alias):
    with open(path, encoding='utf-8') as f:
        FILES[alias] = ORIG[alias] = f.read()
    FILES[alias + '.__path'] = path

def _log(alias, kind, old, new, category, note, n, ok):
    CHANGES.append({'file': alias, 'kind': kind, 'category': category, 'note': note,
                    'occurrences': n, 'ok': ok, 'old': old[:400], 'new': new[:400]})
    if not ok:
        FAILURES.append({'file': alias, 'note': note, 'old': old[:200]})

def rep(alias, old, new, category, note, count=1):
    s = FILES[alias]; n = s.count(old); new = nfkc(new)   # inserted text is normalised; the rest of the file is not
    ok = (n == count)
    if ok:
        FILES[alias] = s.replace(old, new)
    _log(alias, 'exact', old, new, category, note, n, ok)
    return ok

def rep_re(alias, pattern, repl, category, note, count=1, flags=re.DOTALL):
    s = FILES[alias]; n = len(re.findall(pattern, s, flags))
    ok = (n == count)
    if ok:
        FILES[alias] = re.sub(pattern, repl if callable(repl) else nfkc(repl), s, flags=flags)
    _log(alias, 'regex', pattern, repl if isinstance(repl, str) else '<fn>', category, note, n, ok)
    return ok

def rep_t(alias, key, en, ar, category, note, count=1):
    """Replace every t('key','<anything>') pair with t('en','ar')."""
    pat = r"t\('" + re.escape(key) + r"',\s*'[^']*'\)"
    return rep_re(alias, pat, "t('%s','%s')" % (en, ar), category, note, count)

def write_files(outdir):
    os.makedirs(outdir, exist_ok=True); out = []
    for alias, txt in list(FILES.items()):
        if alias.endswith('.__path'): continue
        p = os.path.join(outdir, os.path.basename(FILES[alias + '.__path']))
        with open(p, 'w', encoding='utf-8') as f: f.write(txt)
        out.append(p)
    return out

def write_change_table(stem, title='Change table'):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(stem + '.json', 'w', encoding='utf-8') as f:
        json.dump({'generated': ts, 'title': title, 'failures': FAILURES, 'changes': CHANGES}, f, ensure_ascii=False, indent=1)
    md = ['# ' + title, '', 'Generated %s · %d edits · %d failures' % (ts, len(CHANGES), len(FAILURES)), '',
          '| # | File | Kind | Category | Note | Occurrences | OK |', '|---|---|---|---|---|---|---|']
    for i, c in enumerate(CHANGES, 1):
        md.append('| %d | %s | %s | %s | %s | %d | %s |' % (i, c['file'], c['kind'], c['category'],
                  c['note'].replace('|', '\\|'), c['occurrences'], '✓' if c['ok'] else '✗ FAIL'))
    md += ['', '## Edit detail', '']
    for i, c in enumerate(CHANGES, 1):
        md += ['### %d. %s — %s' % (i, c['file'], c['note']), '', '**Old**', '```', c['old'], '```', '**New**', '```', c['new'], '```', '']
    with open(stem + '.md', 'w', encoding='utf-8') as f: f.write('\n'.join(md))
    return stem + '.md', stem + '.json'
