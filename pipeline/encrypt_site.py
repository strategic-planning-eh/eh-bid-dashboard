#!/usr/bin/env python3
"""encrypt_site.py — passphrase protection for the published hub (decided 22 Sep 2026).

Runs as the LAST step before the site is packaged. Every HTML page and every JSON data file in site/ is replaced by
an encrypted copy: HTML pages become a small bilingual unlock page carrying the ciphertext; JSON files become a
one-line "EHENC1:" envelope. The browser derives the key from the passphrase (PBKDF2-SHA256, 600 000 rounds) and
decrypts with AES-256-GCM. Nothing readable is ever on the public URL.

  • The passphrase comes from the HUB_PASSPHRASE environment variable (a GitHub Secret). Missing → exit 2 and the
    build fails: an unprotected publish is never made by accident.
  • One salt per build, so one derived key opens every file; each file has its own random IV.
  • Delivery: a service worker (site/eh-sw.js, written by this script, never sealed) holds the key in IndexedDB and
    decrypts every page and data file on the way in, so the hub, its iframes and its JSON load exactly as built —
    nothing is rewritten in the page. "Remember this device" keeps the key; otherwise it expires after 12 hours.
    Browsers without service-worker support fall back to in-page decryption (document.write + a fetch shim).
  • Rotation: change the secret → next hourly build re-encrypts → tell the seven holders. Old keys remembered on
    devices simply stop working.

Usage:
    python3 encrypt_site.py --site site                       # encrypt in place (HUB_PASSPHRASE in env)
    python3 encrypt_site.py --decrypt in.json --out out.json  # workflow helper: read a published, encrypted JSON

Plain CSS/JS/vendor files and images are left as they are — they contain no data.
"""
import argparse, base64, json, os, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = 600_000
MARK = 'EHENC1:'
b64 = lambda b: base64.b64encode(b).decode('ascii')
ub64 = lambda s: base64.b64decode(s)

def derive(passphrase, salt):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ROUNDS).derive(passphrase.encode('utf-8'))

def seal(key, data: bytes):
    iv = secrets.token_bytes(12)
    return iv, AESGCM(key).encrypt(iv, data, None)

def envelope(salt, iv, ct):
    return MARK + b64(salt) + '.' + b64(iv) + '.' + b64(ct)

def open_envelope(text, passphrase):
    if not text.startswith(MARK): return text
    s, i, c = text[len(MARK):].split('.')
    key = derive(passphrase, ub64(s))
    return AESGCM(key).decrypt(ub64(i), ub64(c), None).decode('utf-8')

# ------------------------------------------------------------------ unlock page
def logo():
    p = os.path.join(HERE, 'logo_b64.txt')
    return open(p).read().strip() if os.path.exists(p) else ''

SW = r"""/* eh-sw.js — decrypts the sealed hub for browsers that hold the key (issued by the sign-in card). Never caches. */
const MARK='EHENC1:', DB='eh-hub', STORE='k';
let _db=null;function idb(){if(_db)return Promise.resolve(_db);return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>r.result.createObjectStore(STORE);r.onsuccess=()=>{_db=r.result;res(_db);};r.onerror=()=>rej(r.error);});}
async function getKey(){try{const db=await idb();return await new Promise((res,rej)=>{const t=db.transaction(STORE,'readonly').objectStore(STORE).get('key');t.onsuccess=()=>res(t.result||null);t.onerror=()=>rej(t.error);});}catch(e){return null;}}
const u=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
async function open(rec){const raw=await getKey();if(!raw)throw new Error('locked');if(raw.until&&Date.now()>raw.until)throw new Error('expired');
 const key=await crypto.subtle.importKey('raw',raw.k,'AES-GCM',false,['decrypt']);const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:u(rec.iv)},key,u(rec.ct));return new TextDecoder().decode(pt);}
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('message',e=>{if(e.data&&e.data.type==='eh-lock')e.waitUntil(idb().then(db=>new Promise(r=>{const t=db.transaction(STORE,'readwrite').objectStore(STORE).delete('key');t.onsuccess=r;t.onerror=r;})));});
self.addEventListener('fetch',e=>{const url=new URL(e.request.url);if(url.origin!==location.origin||e.request.method!=='GET')return;
 if(!/\.(html|json)(\?|$)/.test(url.pathname)&&!url.pathname.endsWith('/')&&e.request.mode!=='navigate')return;
 e.respondWith((async()=>{const r=await fetch(e.request.url,{cache:'no-store',credentials:'same-origin'});if(!r.ok)return r;const ct=r.headers.get('content-type')||'';const text=await r.clone().text();
  try{
   if(text.startsWith(MARK)){const p=text.slice(MARK.length).split('.');const pt=await open({iv:p[1],ct:p[2]});return new Response(pt,{status:200,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'}});}
   if(text.startsWith('<!--EHENC1-->')){const m=text.match(/<script id="enc" type="application\/json">([\s\S]*?)<\/script>/);if(!m)return r;const rec=JSON.parse(m[1].replace(/<\\\//g,'</'));
    const html=await open(rec);return new Response(html,{status:200,headers:{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'}});}
  }catch(err){/* no key, wrong key or rotated passphrase → hand back the sign-in card */}
  return r;})());});
"""

UNLOCK = r"""<!--EHENC1--><!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>__TITLE__</title>
<style>
/* EH design system v2 sign-in (patch_design_signin.py) */
@font-face{font-family:"EH Display";src:url("vendor/fonts/montserrat-latin-var.woff2") format("woff2");font-weight:100 900;font-display:swap;unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:"EH Display";src:url("vendor/fonts/alexandria-arabic-var.woff2") format("woff2");font-weight:100 900;font-display:swap;unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFC}
@font-face{font-family:"EH Sans";src:url("vendor/fonts/encode-sans-latin-var.woff2") format("woff2");font-weight:100 900;font-stretch:75% 125%;font-display:swap;unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:"EH Sans";src:url("vendor/fonts/plex-sans-arabic-400.woff2") format("woff2");font-weight:400;font-display:swap;unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFC}
:root{--bg:#1B2A6E;--card:#fff;--ink:#15224D;--muted:#46546F;--line:#D9E3DF;--green:#2E7A37;--blue:#0072BB;--red:#B23F2B;--field:#F2F6F4}
@media(prefers-color-scheme:dark){:root{--bg:#0A1230;--card:#15214A;--ink:#E9EEF7;--muted:#B8C4DA;--line:#2A3A6B;--field:#0D1736}}
html,body{margin:0;height:100%}body{font-family:"EH Sans","Segoe UI",Tahoma,Arial,sans-serif;background:var(--bg) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 800' preserveAspectRatio='none'%3E%3Cg fill='none' stroke='%236FB6EA' stroke-width='1.2'%3E%3Cpath d='M0 84L30 83L60 80L90 77L120 75L150 72L180 71L210 70L240 69L270 69L300 69L330 67L360 65L390 61L420 57L450 52L480 48L510 45L540 43L570 44L600 45L630 48L660 51L690 55L720 58L750 60L780 62L810 62L840 63L870 63L900 64L930 67L960 70L990 73L1020 77L1050 81L1080 84L1110 85L1140 84L1170 82L1200 79' opacity='0.10'/%3E%3Cpath d='M0 150L30 148L60 145L90 141L120 137L150 133L180 131L210 129L240 128L270 128L300 127L330 126L360 125L390 122L420 119L450 116L480 112L510 110L540 109L570 110L600 112L630 116L660 120L690 125L720 129L750 132L780 135L810 136L840 137L870 137L900 138L930 139L960 141L990 144L1020 147L1050 150L1080 152L1110 153L1140 152L1170 149L1200 146' opacity='0.12'/%3E%3Cpath d='M0 213L30 211L60 207L90 203L120 198L150 194L180 190L210 188L240 187L270 186L300 186L330 186L360 186L390 185L420 183L450 181L480 179L510 177L540 177L570 178L600 181L630 185L660 190L690 196L720 201L750 205L780 208L810 209L840 210L870 210L900 210L930 210L960 211L990 213L1020 215L1050 217L1080 218L1110 218L1140 217L1170 215L1200 211' opacity='0.15'/%3E%3Cpath d='M0 275L30 273L60 268L90 264L120 258L150 253L180 250L210 247L240 246L270 246L300 247L330 248L360 249L390 249L420 249L450 248L480 247L510 246L540 247L570 248L600 251L630 256L660 261L690 267L720 273L750 277L780 280L810 282L840 282L870 281L900 280L930 280L960 279L990 280L1020 280L1050 282L1080 282L1110 283L1140 281L1170 279L1200 275' opacity='0.17'/%3E%3Cpath d='M0 335L30 333L60 329L90 324L120 319L150 314L180 310L210 307L240 306L270 307L300 308L330 310L360 313L390 315L420 316L450 316L480 317L510 317L540 318L570 320L600 323L630 327L660 332L690 338L720 343L750 348L780 351L810 353L840 353L870 351L900 349L930 347L960 346L990 345L1020 345L1050 345L1080 345L1110 345L1140 345L1170 343L1200 340' opacity='0.19'/%3E%3Cpath d='M0 395L30 392L60 389L90 384L120 379L150 375L180 371L210 369L240 368L270 369L300 372L330 375L360 379L390 382L420 385L450 387L480 388L510 389L540 390L570 392L600 394L630 398L660 403L690 408L720 413L750 417L780 420L810 421L840 421L870 419L900 416L930 413L960 411L990 409L1020 408L1050 407L1080 408L1110 408L1140 408L1170 406L1200 404' opacity='0.21'/%3E%3Cpath d='M0 454L30 452L60 449L90 445L120 441L150 437L180 434L210 433L240 433L270 434L300 438L330 442L360 446L390 451L420 455L450 458L480 460L510 461L540 462L570 464L600 466L630 469L660 473L690 477L720 481L750 485L780 487L810 488L840 487L870 485L900 482L930 478L960 475L990 472L1020 470L1050 470L1080 470L1110 470L1140 471L1170 471L1200 470' opacity='0.24'/%3E%3Cpath d='M0 513L30 512L60 510L90 508L120 505L150 502L180 500L210 499L240 499L270 501L300 505L330 510L360 515L390 521L420 525L450 529L480 532L510 533L540 534L570 535L600 536L630 538L660 541L690 544L720 547L750 550L780 552L810 553L840 552L870 549L900 546L930 542L960 538L990 535L1020 533L1050 532L1080 533L1110 534L1140 535L1170 537L1200 537' opacity='0.26'/%3E%3Cpath d='M0 573L30 573L60 572L90 571L120 570L150 568L180 567L210 566L240 567L270 570L300 574L330 579L360 585L390 591L420 596L450 600L480 603L510 604L540 605L570 605L600 605L630 606L660 607L690 609L720 611L750 614L780 615L810 616L840 615L870 612L900 609L930 605L960 601L990 598L1020 596L1050 596L1080 597L1110 599L1140 602L1170 604L1200 606' opacity='0.28'/%3E%3Cpath d='M0 635L30 636L60 637L90 637L120 637L150 636L180 636L210 636L240 637L270 640L300 644L330 649L360 655L390 661L420 666L450 670L480 673L510 674L540 674L570 673L600 672L630 671L660 672L690 672L720 674L750 675L780 677L810 677L840 677L870 675L900 672L930 669L960 666L990 663L1020 661L1050 661L1080 663L1110 666L1140 669L1170 673L1200 677' opacity='0.30'/%3E%3Cpath d='M0 698L30 700L60 703L90 704L120 706L150 706L180 706L210 707L240 708L270 710L300 714L330 719L360 724L390 729L420 734L450 738L480 741L510 741L540 741L570 739L600 737L630 736L660 735L690 734L720 735L750 736L780 738L810 738L840 739L870 738L900 736L930 733L960 731L990 729L1020 728L1050 729L1080 731L1110 735L1140 739L1170 744L1200 749' opacity='0.33'/%3E%3C/g%3E%3C/svg%3E") center/cover no-repeat;color:var(--ink);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}
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
.quiet .box{display:none}
</style></head><body class="quiet">
<form class="box" id="f" autocomplete="off">
 __LOGO__
 <h1>EH Strategic Intelligence Hub</h1><div class="ar" dir="rtl" lang="ar">منصة الاستخبارات الاستراتيجية — آفاق البيئة</div>
 <label for="p">Passphrase · <span dir="rtl" lang="ar">عبارة المرور</span></label>
 <input id="p" type="password" autofocus autocomplete="current-password" spellcheck="false">
 <div class="row"><input id="r" type="checkbox" checked><label for="r" style="margin:0">Remember this device · <span dir="rtl" lang="ar">تذكّر هذا الجهاز</span></label></div>
 <button id="b" type="submit">Open · فتح</button>
 <div class="err" id="e"></div>
 <div class="foot">Access is limited to EH management. The passphrase is issued by Business Development.<br><span dir="rtl" lang="ar">الوصول مقصور على إدارة آفاق البيئة. تُصدر عبارة المرور من إدارة تطوير الأعمال.</span></div>
</form>
<script id="enc" type="application/json">__ENC__</script>
<script>
(function(){
/* Two ways in. Preferred: a service worker (eh-sw.js) holds the key and decrypts every page and data file on the way
   in, so the hub loads exactly as it was built — no rewriting of the document. Fallback (no service-worker support):
   decrypt here and rewrite the document in place. */
const E=JSON.parse(document.getElementById('enc').textContent), SK='eh.hub.k', DB='eh-hub', STORE='k', enc=new TextEncoder(), dec=new TextDecoder();
const u=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0)), b=a=>btoa(String.fromCharCode(...new Uint8Array(a)));
const SESSION_MS=12*3600*1000;
function idb(){return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>r.result.createObjectStore(STORE);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
async function idbPut(rec){const db=await idb();return new Promise((res,rej)=>{const t=db.transaction(STORE,'readwrite').objectStore(STORE).put(rec,'key');t.onsuccess=res;t.onerror=()=>rej(t.error);});}
async function idbDel(){try{const db=await idb();await new Promise(res=>{const t=db.transaction(STORE,'readwrite').objectStore(STORE).delete('key');t.onsuccess=res;t.onerror=res;});}catch(e){}}
async function derive(pass){const km=await crypto.subtle.importKey('raw',enc.encode(pass),'PBKDF2',false,['deriveBits']);
 return crypto.subtle.deriveBits({name:'PBKDF2',salt:u(E.salt),iterations:E.rounds,hash:'SHA-256'},km,256);}
async function tryRaw(raw){const key=await crypto.subtle.importKey('raw',raw,'AES-GCM',false,['decrypt']);
 const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:u(E.iv)},key,u(E.ct));return dec.decode(pt);}
const swOK=('serviceWorker' in navigator)&&window.isSecureContext;
async function sw(){try{const reg=await navigator.serviceWorker.register('eh-sw.js',{scope:'./'});await navigator.serviceWorker.ready;return reg;}catch(e){return null;}}
/* ---- fallback path (no service worker) ---- */
function stored(){try{return sessionStorage.getItem(SK)||localStorage.getItem(SK);}catch(e){return null;}}
function keep(raw,remember){try{sessionStorage.setItem(SK,b(raw));if(remember)localStorage.setItem(SK,b(raw));else localStorage.removeItem(SK);}catch(e){}}
function forget(){try{sessionStorage.removeItem(SK);localStorage.removeItem(SK);}catch(e){}}
const PRELUDE='<script>(function(){var SK="eh.hub.k",MARK="EHENC1:";function u(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)})}'+
 'async function dec(t){var p=t.slice(MARK.length).split(".");var raw=sessionStorage.getItem(SK)||localStorage.getItem(SK);if(!raw)throw new Error("locked");'+
 'var key=await crypto.subtle.importKey("raw",u(raw),"AES-GCM",false,["decrypt"]);var pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:u(p[1])},key,u(p[2]));return new TextDecoder().decode(pt)}'+
 'var of=window.fetch.bind(window);window.fetch=async function(i,o){var r=await of(i,o);try{var url=new URL(typeof i==="string"?i:i.url,location.href);'+
 'if(url.origin!==location.origin||!r.ok)return r;var t=await r.clone().text();if(t.indexOf(MARK)!==0)return r;var pt=await dec(t);'+
 'return new Response(pt,{status:200,headers:{"Content-Type":"application/json"}})}catch(e){return r}};window.ehHubLock=function(){sessionStorage.removeItem(SK);localStorage.removeItem(SK);location.reload()}})();<\/script>';
function render(html){const i=html.search(/<head[^>]*>/i);const at=i>=0?html.indexOf('>',i)+1:0;document.open();document.write(html.slice(0,at)+PRELUDE+html.slice(at));document.close();}
/* ---- boot ---- */
async function boot(){
 if(swOK){const reg=await sw();
  if(reg&&navigator.serviceWorker.controller===null){ /* first visit: the worker is now installed but did not serve this load; if a key is already on this device, reload through it */
   try{const db=await idb();const rec=await new Promise(res=>{const t=db.transaction(STORE,'readonly').objectStore(STORE).get('key');t.onsuccess=()=>res(t.result||null);t.onerror=()=>res(null);});
    if(rec&&!(rec.until&&Date.now()>rec.until)){location.reload();return;}}catch(e){}}
 }else{const s=stored();if(s){try{render(await tryRaw(u(s)));return;}catch(e){forget();}}}
 document.body.classList.remove('quiet');document.getElementById('p').focus();}
document.getElementById('f').addEventListener('submit',async ev=>{ev.preventDefault();const p=document.getElementById('p'),btn=document.getElementById('b'),err=document.getElementById('e'),remember=document.getElementById('r').checked;
 if(!p.value)return;btn.disabled=true;err.textContent='';
 try{const raw=await derive(p.value);const html=await tryRaw(raw);   /* proves the passphrase before anything is stored */
  if(swOK&&(await sw())){await idbPut({k:new Uint8Array(raw),until:remember?0:Date.now()+SESSION_MS});location.reload();return;}
  keep(raw,remember);render(html);}
 catch(e){err.textContent='Incorrect passphrase · عبارة المرور غير صحيحة';btn.disabled=false;p.select();}});
boot();
})();
</script></body></html>"""

def encrypt_site(site, passphrase):
    salt = secrets.token_bytes(16); key = derive(passphrase, salt); n = 0
    open(os.path.join(site, 'eh-sw.js'), 'w', encoding='utf-8').write(SW)
    lg = logo(); logo_tag = f'<img src="{lg}" alt="EH">' if lg else ''
    for root, dirs, files in os.walk(site):
        if os.path.basename(root) == 'vendor': dirs[:] = []; continue
        for fn in files:
            p = os.path.join(root, fn); low = fn.lower()
            if low.endswith('.html'):
                raw = open(p, 'rb').read()
                if raw.startswith(b'<!--EHENC1-->'): continue   # already sealed
                iv, ct = seal(key, raw)
                title = 'EH Hub — sign in'
                try:
                    import re
                    m = re.search(rb'<title>(.*?)</title>', raw, re.S | re.I)
                    if m: title = m.group(1).decode('utf-8', 'ignore').strip()[:90] + ' — sign in'
                except Exception: pass
                enc = json.dumps({'v': 1, 'rounds': ROUNDS, 'salt': b64(salt), 'iv': b64(iv), 'ct': b64(ct)})
                page = UNLOCK.replace('__TITLE__', title.replace('<', '&lt;')).replace('__LOGO__', logo_tag).replace('__ENC__', enc.replace('</', '<\\/'))
                open(p, 'w', encoding='utf-8').write(page); n += 1
            elif low.endswith('.json'):
                txt = open(p, 'r', encoding='utf-8').read()
                if txt.startswith(MARK): continue
                iv, ct = seal(key, txt.encode('utf-8'))
                open(p, 'w', encoding='utf-8').write(envelope(salt, iv, ct)); n += 1
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', default=None); ap.add_argument('--decrypt', default=None); ap.add_argument('--out', default=None)
    a = ap.parse_args()
    pw = os.environ.get('HUB_PASSPHRASE', '')
    if not pw.strip():
        print('FATAL: HUB_PASSPHRASE is not set — refusing to publish the hub unprotected. Add the secret in Settings → Secrets and variables → Actions.', file=sys.stderr); sys.exit(2)
    if len(pw) < 16:
        print('FATAL: HUB_PASSPHRASE is shorter than 16 characters — choose a longer passphrase.', file=sys.stderr); sys.exit(2)
    if a.decrypt:
        txt = open(a.decrypt, encoding='utf-8').read()
        try: out = open_envelope(txt, pw)
        except Exception as e:
            print('decrypt failed (different passphrase than the one it was published with?):', type(e).__name__, file=sys.stderr); sys.exit(3)
        open(a.out or a.decrypt, 'w', encoding='utf-8').write(out); print('decrypted', a.decrypt); return
    if not a.site: sys.exit('give --site DIR or --decrypt FILE')
    n = encrypt_site(a.site, pw)
    print(f'sealed {n} files in {a.site} (AES-256-GCM, PBKDF2 {ROUNDS:,} rounds)')

if __name__ == '__main__':
    main()
