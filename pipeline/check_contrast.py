#!/usr/bin/env python3
"""check_contrast.py — every text/background pair in the EH design tokens must pass WCAG AA (12 Oct 2026).

Reads the light tokens (:root) and dark tokens (html.dark, body.dark, [data-theme=dark]) from hub/eh-shared.css and
checks each pair the pages actually use. Translucent backgrounds are composited over the panel colour first.
Normal text needs 4.5:1; large text (the hub masthead title, KPI numbers) needs 3:1.
Exit 0 = all pass. Exit 1 = at least one pair fails (the list is printed).
Usage: python3 pipeline/check_contrast.py [hub/eh-shared.css]
"""
import re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'hub', 'eh-shared.css')

# (text token, background token, minimum ratio, what it is)
PAIRS = [
    ('eh-ink', 'eh-paper', 4.5, 'body text on panels'), ('eh-ink', 'eh-mist', 4.5, 'body text on the page'),
    ('eh-ink', 'eh-tint', 4.5, 'text on quiet fills'), ('eh-ink-2', 'eh-paper', 4.5, 'secondary text on panels'),
    ('eh-ink-2', 'eh-mist', 4.5, 'secondary text on the page'), ('eh-ink-2', 'eh-tint', 4.5, 'secondary text on quiet fills'),
    ('eh-ink-3', 'eh-paper', 4.5, 'footnotes on panels'), ('eh-ink-3', 'eh-mist', 4.5, 'footnotes on the page'),
    ('eh-sea', 'eh-paper', 4.5, 'links and buttons'), ('eh-sea', 'eh-mist', 4.5, 'links on the page'),
    ('eh-sea-ink', 'eh-tint', 4.5, 'blue text on quiet fills'), ('eh-leaf-ink', 'eh-paper', 4.5, 'green text'),
    ('eh-leaf-ink', 'eh-mist', 4.5, 'green text on the page'),
    ('eh-good', 'eh-good-bg', 4.5, 'won / good chip'), ('eh-bad', 'eh-bad-bg', 4.5, 'lost / bad chip'),
    ('eh-warn', 'eh-warn-bg', 4.5, 'warning chip'), ('eh-info', 'eh-info-bg', 4.5, 'info chip'),
    ('eh-muted', 'eh-muted-bg', 4.5, 'muted chip'),
]
LIGHT_ONLY = [('#FFFFFF', 'eh-sea', 4.5, 'white on a solid blue button'), ('#FFFFFF', 'eh-deep', 4.5, 'white on the navy masthead'),
              ('#FFFFFF', 'eh-leaf-ink', 4.5, 'white on a green badge')]

def tokens(block):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r'--(eh-[\w-]+)\s*:\s*([^;]+);', block)}

def parse(c):
    c = c.strip()
    m = re.match(r'#([0-9a-fA-F]{6})$', c)
    if m: h = m.group(1); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (1.0,)
    m = re.match(r'rgba?\(([^)]+)\)', c)
    if m:
        p = [x.strip() for x in m.group(1).split(',')]
        return (float(p[0]), float(p[1]), float(p[2]), float(p[3]) if len(p) > 3 else 1.0)
    raise ValueError('cannot read colour ' + c)

def over(fg, bg):
    a = fg[3]; return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)

def lum(c):
    def ch(v):
        v /= 255; return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])

def ratio(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

def resolve(T, name):
    v = T.get(name, name)
    for _ in range(4):
        m = re.match(r'var\(--([\w-]+)\)', v)
        if not m: break
        v = T[m.group(1)]
    return parse(v)

def main():
    css = open(CSS, encoding='utf-8').read()
    root = tokens(re.search(r':root\{(.*?)\n\}', css, re.S).group(1))
    dark = dict(root); dark.update(tokens(re.search(r'html\.dark,body\.dark,\[data-theme=dark\]\{(.*?)\n\}', css, re.S).group(1)))
    fails, n = [], 0
    for mode, T in (('light', root), ('dark', dark)):
        panel = resolve(T, 'eh-paper')
        for fg, bg, need, what in PAIRS + (LIGHT_ONLY if mode == 'light' else []):
            f = resolve(T, fg) if fg.startswith('eh-') else parse(fg)
            b = resolve(T, bg); b = over(b, panel) if b[3] < 1 else b
            f = over(f, b) if f[3] < 1 else f
            r = ratio(f, b); n += 1
            line = f'{mode:5} {fg:>12} on {bg:<12} {r:5.2f}:1 (needs {need}) {what}'
            print(('FAIL ' if r < need else 'ok   ') + line)
            if r < need: fails.append(line)
    print(f'\n{n - len(fails)} of {n} pairs pass.')
    if fails:
        print('Contrast failures:'); [print('  ' + f) for f in fails]; sys.exit(1)

if __name__ == '__main__':
    main()
