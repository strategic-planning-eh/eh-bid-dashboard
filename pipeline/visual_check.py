#!/usr/bin/env python3
"""visual_check.py — visual regression gate for the EH Hub (roadmap X7). Runs in the workflow after site/ is assembled.

For every page in site/ (hub shell + dashboards), in English and Arabic, at 1440×900 (motion off):
  * page loads with no JavaScript errors
  * every visible <canvas> has actually painted (a blank chart fails)
  * the page has the minimum number of KPI cards / tables / SVGs expected for it
  * a full-page screenshot is compared with the baseline from the last good build; if more than THRESHOLD of pixels
    changed (or the page height changed by more than 35 %), the page is flagged
Exit 0 = pass. Exit 1 = a regression was found (the build must stop). Exit 2 = the checker itself could not run.

Usage:  python3 pipeline/visual_check.py --site site [--baseline pipeline/visual_baseline] [--out pipeline/visual_out]
        --update-baseline   write the current screenshots as the new baseline (done automatically when there is none)
Baseline lives outside the repo as a workflow artefact ("visual-baseline"), restored before this runs.
"""
import argparse, json, os, sys, threading, http.server, socketserver, time
try:
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageChops
except ImportError as e:
    print('visual_check: missing dependency', e, '— pip install playwright pillow && playwright install --with-deps chromium'); sys.exit(2)

PAGES = {  # file: minimum expectations {canvases painted, kpi cards, tables, svgs}
    'index.html':                      dict(kpi=0, tables=0, svgs=0),   # hub shell — the workflow publishes hub/EH_Hub.html as site/index.html
    'EH_Stakeholder_Map_CURRENT.html': dict(kpi=5, tables=0, svgs=0),
    'EH_Bid_Analysis_CURRENT.html':    dict(kpi=6, tables=0, svgs=1),
    'EH_Client_Bubble_Map_CURRENT.html': dict(kpi=0, tables=0, svgs=1),
    'eh_news_intelligence.html':       dict(kpi=4, tables=0, svgs=0, canvases=3),
    'vision2030_dashboard.html':       dict(kpi=3, tables=0, svgs=0, canvases=2),
    'saudi_fiscal_monitor_2026.html':  dict(kpi=6, tables=0, svgs=0, canvases=6),
    'pif_intelligence_hub.html':       dict(kpi=5, tables=3, svgs=0, canvases=12),
    'pif_strategy_2026_2030.html':     dict(kpi=6, tables=4, svgs=1, canvases=2),
}
ALIASES = {'index.html': 'EH_Hub.html'}   # accepted alternative filename when the primary is absent (local runs against hub/)
THRESHOLD = 0.06   # 6 % of pixels changed vs the last good build → flag (charts with live data move a little every hour)
CHECK_JS = r"""(()=>{const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'};
 const canv=[...document.querySelectorAll('canvas')].filter(vis);
 const blank=canv.filter(c=>{try{const x=c.getContext('2d');if(!x||!c.width)return true;const d=x.getImageData(0,0,c.width,c.height).data;for(let i=3;i<d.length;i+=4*97){if(d[i]>0)return false;}return true;}catch(e){return false;}}).map(c=>c.id||'(no id)');
 return {chartlib:typeof Chart!=='undefined',canvases:canv.length,blank,kpi:[...document.querySelectorAll('.kpi,.kc,.metric,[class*=kpi]')].filter(vis).length,
  tables:[...document.querySelectorAll('table')].filter(vis).length,svgs:[...document.querySelectorAll('svg')].filter(vis).filter(s=>s.getBoundingClientRect().height>60).length,
  height:document.documentElement.scrollHeight,words:(document.body.innerText||'').split(/\s+/).length};})()"""

def serve(root, port):
    class Q(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=root, **k)
        def log_message(self, *a): pass
    srv = socketserver.TCPServer(('127.0.0.1', port), Q); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv

def diff_ratio(a_path, b_path):
    a, b = Image.open(a_path).convert('RGB'), Image.open(b_path).convert('RGB')
    h_ratio = abs(a.height - b.height) / max(a.height, b.height, 1)
    h = min(a.height, b.height); a, b = a.crop((0, 0, a.width, h)), b.crop((0, 0, b.width, h))
    if a.size != b.size: b = b.resize(a.size)
    d = ImageChops.difference(a, b).convert('L').point(lambda p: 255 if p > 40 else 0)
    hist = d.histogram(); changed = (hist[255] if len(hist) > 255 else 0) / max(1, d.width * d.height)
    return changed, h_ratio

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--site', required=True); ap.add_argument('--baseline', default='pipeline/visual_baseline')
    ap.add_argument('--out', default='pipeline/visual_out'); ap.add_argument('--update-baseline', action='store_true'); ap.add_argument('--port', type=int, default=8794)
    ap.add_argument('--allow-cdn', action='store_true', help='let cdnjs/jsdelivr/fonts load (default: blocked, so the gate exercises the vendor/ fallbacks and screenshots stay deterministic)')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(a.baseline, exist_ok=True)
    have_baseline = any(f.endswith('.png') for f in os.listdir(a.baseline))
    srv = serve(os.path.abspath(a.site), a.port); base = f'http://127.0.0.1:{a.port}/'
    failures, report = [], {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        for page, want in PAGES.items():
            if not os.path.exists(os.path.join(a.site, page)) and ALIASES.get(page) and os.path.exists(os.path.join(a.site, ALIASES[page])): page_file = ALIASES[page]
            elif not os.path.exists(os.path.join(a.site, page)): report[page] = 'missing'; failures.append(f'{page}: file missing from site/'); continue
            else: page_file = page
            for lang in ('en', 'ar'):
                ctx = br.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
                # External hosts are blocked by default so (a) the run does not depend on a CDN being up, (b) screenshots are identical build-to-build,
                # (c) the vendor/ fallbacks every page carries are exercised on every build. --allow-cdn lifts the block for scripts and fonts only.
                blocked = ('openstreetmap', 'cartocdn') if a.allow_cdn else ('cdnjs', 'jsdelivr', 'googleapis', 'gstatic', 'openstreetmap', 'cartocdn')
                def _route(route, request, _b=blocked):   # Playwright calls the handler as handler(route, request)
                    (route.abort() if any(d in request.url for d in _b) else route.continue_())
                pg.route('**/*', _route)
                try:
                    pg.add_init_script(f"try{{localStorage.setItem('ehhub.lang','{lang}');}}catch(e){{}}")
                    pg.goto(base + page_file + '?embedded=1', wait_until='load', timeout=60000); pg.wait_for_timeout(2500)
                    pg.evaluate(f"window.postMessage({{ehhub:'lang',lang:'{lang}'}},'*')"); pg.wait_for_timeout(1500)
                    m = pg.evaluate(CHECK_JS); key = f'{page}__{lang}'; shot = os.path.join(a.out, key + '.png'); pg.screenshot(path=shot, full_page=True)
                    probs = []
                    if errs: probs.append('script errors: ' + '; '.join(errs[:2]))
                    if want.get('canvases', 0) and not m['chartlib']: probs.append('Chart.js did not load — CDN blocked by this check and vendor/chart.umd.min.js not served (copy hub/chart.umd.min.js into hub/vendor/)')
                    elif m['blank']: probs.append('blank charts: ' + ', '.join(m['blank']))
                    if want.get('canvases', 0) and m['canvases'] < want['canvases']: probs.append(f"canvases {m['canvases']} < {want['canvases']}")
                    for k in ('kpi', 'tables', 'svgs'):
                        if m[k] < want.get(k, 0): probs.append(f"{k} {m[k]} < {want[k]}")
                    if m['words'] < 60: probs.append(f"page nearly empty ({m['words']} words)")
                    bpath = os.path.join(a.baseline, key + '.png')
                    if have_baseline and os.path.exists(bpath) and not a.update_baseline:
                        ch, hr = diff_ratio(shot, bpath); m['diff'] = round(ch, 4); m['height_change'] = round(hr, 3)
                        if ch > THRESHOLD: probs.append(f'{ch:.1%} of pixels changed vs last good build')
                        if hr > 0.35: probs.append(f'page height changed {hr:.0%}')
                    report[key] = dict(m, problems=probs)
                    if probs: failures.append(f'{key}: ' + ' | '.join(probs))
                except Exception as e:
                    report[f'{page}__{lang}'] = {'error': str(e)[:200]}; failures.append(f'{page}__{lang}: {str(e)[:120]}')
                ctx.close()
        br.close()
    srv.shutdown()
    json.dump(report, open(os.path.join(a.out, 'visual_report.json'), 'w'), indent=1)
    if not failures and (a.update_baseline or not have_baseline):
        for f in os.listdir(a.out):
            if f.endswith('.png'): os.replace(os.path.join(a.out, f), os.path.join(a.baseline, f))
        print('visual_check: baseline written to', a.baseline)
    elif not failures:
        for f in os.listdir(a.out):   # pass → the current build becomes the reference for the next one
            if f.endswith('.png'): os.replace(os.path.join(a.out, f), os.path.join(a.baseline, f))
    if failures:
        print('VISUAL REGRESSION — build stopped:'); [print('  -', f) for f in failures]; sys.exit(1)
    print(f'visual_check: {len(report)} page states OK')

if __name__ == '__main__':
    main()
