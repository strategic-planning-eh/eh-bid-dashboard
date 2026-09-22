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
:root{--bg:#F4F7F5;--card:#fff;--ink:#16333F;--muted:#5F7078;--line:#E3EAE5;--green:#1F7A4C;--blue:#1A5FAB;--red:#C0504D}
@media(prefers-color-scheme:dark){:root{--bg:#0F1519;--card:#151C21;--ink:#E6EDF1;--muted:#9FB3BE;--line:#2C3A43}}
html,body{margin:0;height:100%}body{font-family:"Segoe UI",Tahoma,Arial,sans-serif;background:var(--bg);color:var(--ink);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}
.box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:26px 28px;width:100%;max-width:400px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.box img{height:40px;display:block;margin:0 auto 12px}
h1{font-size:15px;margin:0 0 2px;text-align:center}.ar{text-align:center;font-size:13px;color:var(--muted);margin-bottom:18px}
label{display:block;font-size:12px;color:var(--muted);margin:10px 0 4px}
input[type=password]{width:100%;box-sizing:border-box;font:inherit;font-size:15px;padding:10px 12px;border:1px solid var(--line);border-radius:9px;background:var(--bg);color:var(--ink);direction:ltr}
.row{display:flex;align-items:center;gap:8px;margin:12px 0 14px;font-size:12.5px;color:var(--muted)}
button{width:100%;font:700 14px inherit;padding:11px;border:0;border-radius:9px;background:linear-gradient(90deg,#1A5FAB,#1F7A4C);color:#fff;cursor:pointer}button:disabled{opacity:.6}
.err{color:var(--red);font-size:12.5px;min-height:18px;margin-top:8px;text-align:center}
.foot{font-size:11px;color:var(--muted);text-align:center;margin-top:14px;line-height:1.5}
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
