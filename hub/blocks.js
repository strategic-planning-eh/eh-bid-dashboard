/* Lists every English text block of a hub page as rendered (used by patch_ar_full.py --check). Needs node + jsdom. */
const {JSDOM}=require('jsdom');const fs=require('fs');
const path=require('path');const full=process.argv[2];const f=path.basename(full);process.chdir(path.dirname(full));
let html=fs.readFileSync(f,'utf8').replace(/<script src="https?:[^"]*"[^>]*><\/script>/g,'').replace(/<script src="eh-[^"]*"[^>]*><\/script>/g,'');
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://example.org/'+f,pretendToBeVisual:true,beforeParse(w){w.Chart=function(){return {destroy(){},update(){},data:{datasets:[]},options:{}}};w.Chart.register=()=>{};w.Chart.defaults={font:{},plugins:{legend:{labels:{}},tooltip:{}},scale:{grid:{}}};w.HTMLCanvasElement.prototype.getContext=()=>null;w.matchMedia=()=>({matches:false,addEventListener(){},addListener(){}});w.ResizeObserver=class{observe(){}unobserve(){}disconnect(){}};w.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}};w.scrollTo=()=>{};}});
setTimeout(()=>{const d=dom.window.document;const INL=new Set(['B','I','SPAN','A','BR','SUP','SUB','SMALL','STRONG','EM','CODE','ABBR','U','MARK']);
 const out=[];const seen=new Set();
 const skip=el=>el.closest('#ehArView,script,style,svg,canvas,noscript');
 const isLeaf=el=>![...el.childNodes].some(n=>n.nodeType===1&&!INL.has(n.tagName));
 d.body.querySelectorAll('*').forEach(el=>{if(skip(el))return;if(INL.has(el.tagName)&&!(el.parentElement&&!isLeaf(el.parentElement)))return;
  const kids=[...el.childNodes];if(!/[A-Za-z]{2}/.test(el.textContent))return;
  if(kids.some(n=>n.nodeType===1&&!INL.has(n.tagName)))return; // only leaf blocks (inline children only)
  const k=el.innerHTML.replace(/\s+/g,' ').trim(); if(!/[A-Za-z]{2}/.test(el.textContent)||seen.has(k))return; seen.add(k); out.push(k);});
 // mixed blocks: text directly inside an element that also has block children
 d.body.querySelectorAll('*').forEach(el=>{if(skip(el))return;[...el.childNodes].forEach(n=>{if(n.nodeType===3&&/[A-Za-z]{3}/.test(n.textContent)&&[...el.childNodes].some(c=>c.nodeType===1&&!INL.has(c.tagName))){const k='#text:'+n.textContent.replace(/\s+/g,' ').trim();if(!seen.has(k)){seen.add(k);out.push(k);}}});});
 process.stdout.write(JSON.stringify(out));process.exit(0)},1500);
