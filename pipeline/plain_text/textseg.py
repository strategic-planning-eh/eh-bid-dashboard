"""Find human-visible text segments in a hub page: HTML text nodes and attribute text (title/placeholder/aria-label/data-en/data-ar)
outside <script>/<style>, and string literals with 3+ words inside inline app scripts (library scripts skipped)."""
import re
LIB = re.compile(r'Chart\.js v|\(c\) 20\d\d Chart\.js|Leaflet|d3js\.org|@license|sourceMappingURL|!function\(t,e\)\{"object"==typeof exports|jQuery v')
def segments(s):
    out = []  # (start, end) spans of editable text
    for m in re.finditer(r'<script\b[^>]*>(.*?)</script>|<style\b[^>]*>.*?</style>', s, re.S):
        pass
    # mark script/style regions
    regions = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r'<(script|style)\b[^>]*>.*?</\1>', s, re.S)]
    pos = 0
    for a, b, blk in regions + [(len(s), len(s), '')]:
        html = s[pos:a]
        for t in re.finditer(r'>([^<>]+)<', html):
            if re.search(r'[A-Za-z\u0600-\u06FF]', t.group(1)): out.append((pos + t.start(1), pos + t.end(1)))
        for t in re.finditer(r'\b(?:title|placeholder|aria-label|data-en|data-ar|alt)="([^"]*)"', html):
            out.append((pos + t.start(1), pos + t.end(1)))
        if blk.startswith('<script') and not LIB.search(blk[:4000]) and len(blk) < 400000:
            body_off = a + blk.find('>') + 1
            code = blk[blk.find('>') + 1:]
            for t in re.finditer(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`", code):
                g = 1 if t.group(1) is not None else 2 if t.group(2) is not None else 3
                txt = t.group(g)
                if g == 3:
                    # template literal: take only the literal text between ${...} and outside tags
                    base = body_off + t.start(3); i = 0
                    for part in re.finditer(r'\$\{(?:[^{}]|\{[^{}]*\})*\}', txt):
                        seg = txt[i:part.start()]
                        for tt in re.finditer(r'>([^<>]+)<|^([^<>="]+)$', seg):
                            gg = tt.group(1) or tt.group(2)
                            if gg and len(re.findall(r'[A-Za-z\u0600-\u06FF]{2,}', gg)) >= 3:
                                k = tt.start(1) if tt.group(1) else tt.start(2)
                                out.append((base + i + k, base + i + k + len(gg)))
                        i = part.end()
                    continue
                if len(re.findall(r'[A-Za-z\u0600-\u06FF]{2,}', txt)) >= 3 and not re.search(r'^\s*(function|return|var |const |let )|[{};]\s*$', txt):
                    out.append((body_off + t.start(g), body_off + t.end(g)))
        pos = b
    return out
def apply(s, rules_en, rules_ar):
    spans = segments(s); spans.sort(); res = []; last = 0; changed = []
    for a, b in spans:
        if a < last: continue
        seg = s[a:b]; new = seg
        for rx, rp in (rules_ar if re.search(r'[\u0600-\u06FF]', seg) else rules_en):
            new = re.sub(rx, rp, new)
        res.append(s[last:a]); res.append(new); last = b
        if new != seg: changed.append((seg, new))
    res.append(s[last:])
    return ''.join(res), changed

QUOTE = re.compile(r'(“[^”]*”|&quot;.*?&quot;|\\"[^"\\]*\\"|"[^"]{3,}")')
def apply2(s, rules_en, rules_ar, first=()):
    """Like apply(), but leaves quoted wording untouched and expands FIRST terms once per page."""
    spans = sorted(segments(s)); res = []; last = 0; changed = []; done = set()
    full_page = s
    for a, b in spans:
        if a < last: continue
        seg = s[a:b]
        ar = bool(re.search(r'[\u0600-\u06FF]', seg))
        parts = QUOTE.split(seg) if not ar else [seg]
        out = []
        for i, p in enumerate(parts):
            if i % 2 == 1 and not ar: out.append(p); continue
            for rx, rp in (rules_ar if ar else rules_en): p = re.sub(rx, rp, p)
            if not ar:
                for ab, full, probe in first:
                    if ab in done: continue
                    if probe in full_page: done.add(ab); continue
                    if len(re.findall(r'[A-Za-z]{2,}', p)) < 12: continue  # sentences only, never labels or titles
                    m = re.search(r'(?<![A-Za-z(])' + re.escape(ab) + r'(?![A-Za-z)\-])', p)
                    if m: p = p[:m.start()] + full + p[m.end():]; done.add(ab)
            out.append(p)
        new = ''.join(out)
        res.append(s[last:a]); res.append(new); last = b
        if new != seg: changed.append((seg, new))
    res.append(s[last:])
    return ''.join(res), changed
