#!/usr/bin/env python3
"""build_etimad_page.py — renders the Government Tenders (Etimad) page from etimad_tenders.json.

CI:    python pipeline/build_etimad_page.py pipeline/etimad_tenders.json site/etimad_tenders.html
The page is generated at publish time only and sealed by encrypt_site.py with every other page;
it is never committed, because it carries the Etimad data. It follows the hub's language and theme
through postMessage, like the Environment Fund page.
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etimad_analyst as AV
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'etimad_tenders.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'site', 'etimad_tenders.html')

if os.path.exists(SRC):
    D = json.load(open(SRC, encoding='utf-8'))
else:
    D = {'last_capture': None, 'captures': [], 'count': 0, 'counts': [], 'service_lines': [], 'tenders': []}

# ------------------------------------------------------------------ "what this means for EH" notes
def notes(D):
    T = [t for t in D['tenders'] if t['relevance'] != 'Not EH']
    out = []
    if not T:
        return out
    SL = {s['id']: s for s in D['service_lines']}
    by_line = collections.Counter(i for t in T for i in t['service_lines'])
    if by_line:
        lid, n = by_line.most_common(1)[0]
        out.append({'en': f"{SL[lid]['en']} is the largest relevant line: {n} of {len(T)} relevant tenders captured.",
                    'ar': f"«{SL[lid]['ar']}» أكبر خط خدمة: {n} من أصل {len(T)} منافسة ذات صلة.",
                    'k': 'line'})
    by_ag = collections.Counter(t['agency'] for t in T)
    ag, n = by_ag.most_common(1)[0]
    if n >= 2:
        t0 = next(t for t in T if t['agency'] == ag)
        cl = (t0.get('map') or {}).get('EH Client') == 'Yes'
        out.append({'en': f"The most frequent requester is {ag} with {n} relevant tenders" + (" — already an EH client." if cl else "."),
                    'ar': f"أكثر الجهات طرحًا: {ag} بعدد {n} منافسات ذات صلة" + (" — وهي عميل حالي لآفاق البيئة." if cl else "."),
                    'k': 'agency'})
    dp = [t for t in T if t['type'].startswith('شراء مباشر')]
    if dp:
        out.append({'en': f"{len(dp)} of {len(T)} relevant tenders ({round(100*len(dp)/len(T))}%) are direct purchases, which often stay open for under two weeks — a weekly capture can miss some of them.",
                    'ar': f"{len(dp)} من {len(T)} منافسة ذات صلة ({round(100*len(dp)/len(T))}%) شراء مباشر، وكثير منها يبقى مفتوحًا أقل من أسبوعين؛ لذا قد يفوت الالتقاط الأسبوعي بعضها.",
                    'k': 'direct'})
    op = [t for t in T if t['is_open']]
    ns = [t for t in op if t['eh_status'] == 'Not studied']
    if op:
        out.append({'en': f"{len(op)} relevant tenders were open at the last capture; {len(ns)} of them are not yet in the bid tracker.",
                    'ar': f"كانت {len(op)} منافسة ذات صلة مفتوحة عند آخر التقاط، منها {len(ns)} غير مسجلة بعد في جدول متابعة المنافسات.",
                    'k': 'open'})
    return out

def market_notes(D):
    W = (D.get('market') or {}).get('windows') or []
    if not W:
        return []
    w = W[-1]; SN = D['market']['sector_names']; GN = D['market']['group_names']
    tot = sum(r['n'] for r in w['rows'] if r['dim'] == 'type')
    if not tot:
        return []
    days = len([r for r in w['rows'] if r['dim'] == 'date' and r['n'] >= 10])
    from datetime import date as _d
    AR_M = ['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر']
    def de(x): d = _d.fromisoformat(x); return f"{d.day} {d.strftime('%b')} {d.year}"
    def da(x): d = _d.fromisoformat(x); return f"{d.day} {AR_M[d.month-1]} {d.year}"
    out = [{'en': f"{tot:,} tenders were published on Etimad between {de(w['from'])} and {de(w['to'])} — about {round(tot/max(days,1))} per working day.",
            'ar': f"نُشرت {tot:,} منافسة في اعتماد بين {da(w['from'])} و{da(w['to'])} — نحو {round(tot/max(days,1))} منافسة في يوم العمل."}]
    sec = sorted(w['sectors'].items(), key=lambda kv: -kv[1]['n'])[:3]
    out.append({'en': 'Biggest sectors by number of tenders: ' + '; '.join(f"{SN[k]['en']} {v['n']} ({round(100*v['n']/tot)}%)" for k, v in sec) + '.',
                'ar': 'أكبر القطاعات بعدد المنافسات: ' + '؛ '.join(f"{SN[k]['ar']} {v['n']} ({round(100*v['n']/tot)}%)" for k, v in sec) + '.'})
    fee_sec = sorted(w['sectors'].items(), key=lambda kv: -kv[1]['fees'])[:2]
    allfees = sum(v['fees'] for v in w['sectors'].values()) or 1
    out.append({'en': 'By document fees — a rough sign of contract size, not contract value — the largest sectors are ' + ' and '.join(f"{SN[k]['en']} ({round(100*v['fees']/allfees)}% of fees, {round(100*v['n']/tot)}% of tenders)" for k, v in fee_sec) + '.',
                'ar': 'بحسب قيمة الكراسات — مؤشر تقريبي لحجم العقد وليست قيمته — أكبر القطاعات ' + ' و'.join(f"{SN[k]['ar']} ({round(100*v['fees']/allfees)}% من القيمة، {round(100*v['n']/tot)}% من المنافسات)" for k, v in fee_sec) + '.'})
    ty = {r['key']: r for r in w['rows'] if r['dim'] == 'type'}
    dp, pt = ty.get('شراء مباشر'), ty.get('منافسة عامة')
    if dp and pt:
        tf = sum(r['fees'] for r in ty.values()) or 1
        out.append({'en': f"Direct purchases are {round(100*dp['n']/tot)}% of tenders but only {round(100*dp['fees']/tf)}% of document fees; public tenders carry {round(100*pt['fees']/tf)}%. Large work still goes through public tenders, where EH has time to prepare.",
                    'ar': f"يمثل الشراء المباشر {round(100*dp['n']/tot)}% من المنافسات و{round(100*dp['fees']/tf)}% فقط من قيمة الكراسات، بينما تحمل المنافسات العامة {round(100*pt['fees']/tf)}%. الأعمال الكبيرة ما زالت تُطرح منافسةً عامة، حيث يتسع الوقت للتحضير."})
    g = sorted(w['agency_groups'].items(), key=lambda kv: -kv[1]['n'])[:3]
    gt = sum(v['n'] for v in w['agency_groups'].values()) or 1
    out.append({'en': 'Who is buying (top agencies, grouped): ' + '; '.join(f"{GN[k]['en']} {round(100*v['n']/gt)}%" for k, v in g) + '.',
                'ar': 'من يشتري (أكبر الجهات مجمّعة): ' + '؛ '.join(f"{GN[k]['ar']} {round(100*v['n']/gt)}%" for k, v in g) + '.'})
    env = w['sectors'].get('env', {'n': 0})
    out.append({'en': f"Environment & waste is listed as the activity on only {env['n']} tenders ({round(100*env['n']/tot,1)}%). Most EH-relevant work sits under other activities — water, health, consulting — which is why the tab tags tenders by their titles, not by Etimad's activity.",
                'ar': f"نشاط «البيئة والنفايات» مسجل في {env['n']} منافسة فقط ({round(100*env['n']/tot,1)}%). معظم الأعمال المناسبة لآفاق تُطرح تحت أنشطة أخرى — المياه والصحة والاستشارات — لذلك تُصنَّف المنافسات في هذه الصفحة بعناوينها لا بنشاط اعتماد."})
    return out

D['notes'] = notes(D)
D['market_notes'] = market_notes(D)
D['generated'] = datetime.now().strftime('%Y-%m-%d')
for t in D['tenders']:   # slim the payload
    for k in ('status_history',):
        t.pop(k, None)
payload = json.dumps(D, ensure_ascii=False, default=str).replace('</', '<\\/')

CSS = r"""
:root{--bg:#F4F7F5;--card:#fff;--ink:#16333F;--muted:#5F7078;--line:#E3EAE5;--green:#1F7A4C;--blue:#1A5FAB;--amber:#E8862E;--red:#C0504D;--chip:#F0F5F2;
--core:#1A5FAB;--adj:#2E7D46;--bar:#1A5FAB;--bar2:#2E7D46;--grid:#E8EEEA}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--eh-font,"Segoe UI",Tahoma,Arial,sans-serif);background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
body.dark{--bg:#0F1519;--card:#151C21;--ink:#E6EDF1;--muted:#9FB3BE;--line:#2C3A43;--chip:#1E2830;--core:#4F8FD6;--adj:#3E9E5C;--bar:#4F8FD6;--bar2:#3E9E5C;--grid:#24313A}
header{background:linear-gradient(120deg,#0F3D2E,#1A5FAB);color:#fff;padding:16px 22px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
header h1{margin:0;font-size:19px;font-weight:800}header .sub{font-size:12px;opacity:.9;margin-top:2px}
header .ctl{margin-inline-start:auto;display:flex;gap:6px}
.tog{display:inline-flex;border:1px solid rgba(255,255,255,.5);border-radius:8px;overflow:hidden}.tog button{background:transparent;color:#fff;border:0;padding:6px 12px;cursor:pointer;font:600 12px inherit}.tog button.on{background:#fff;color:#16333F}
body.embedded header .ctl{display:none}
main{max-width:1440px;margin:0 auto;padding:16px 22px 40px}
.stamp{font-size:12.5px;color:var(--muted);margin:0 0 12px;display:flex;gap:8px 14px;flex-wrap:wrap;align-items:center}
.stamp .cap{font-weight:700;color:var(--ink);background:var(--chip);border:1px solid var(--line);border-radius:7px;padding:3px 9px}
.stamp .cap.stale{background:#FFF1D6;border-color:#E8862E;color:#7A4200}
body.dark .stamp .cap.stale{background:#3A2A12;color:#FFD9A8}
.gapnote{font-size:12px;color:var(--muted);background:var(--card);border:1px solid var(--line);border-inline-start:3px solid var(--amber);border-radius:8px;padding:8px 12px;margin-bottom:14px}
.kstrip{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-bottom:14px}
.klab{font-size:11.5px;font-weight:800;letter-spacing:.3px;color:var(--muted);text-transform:uppercase;margin:0 0 6px}
.kc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;border-top:4px solid var(--blue)}
.kc.warn{border-top-color:var(--amber)}.kc.blue{border-top-color:#2E7D46}.kc.mkt{border-top-color:var(--muted)}
.kc .v{font-size:24px;font-weight:800;line-height:1.1;font-variant-numeric:tabular-nums}.kc .l{font-size:12px;color:var(--muted);margin-top:6px;line-height:1.35}
.filters{position:sticky;top:0;z-index:5;background:var(--bg);padding:8px 0 10px;margin-bottom:6px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.filters select,.filters input{font:12.5px inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:7px;padding:5px 7px;max-width:210px}
.filters label{font-size:12px;color:var(--muted);display:inline-flex;align-items:center;gap:4px}
.filters .reset{font:600 12px inherit;background:var(--chip);border:1px solid var(--line);color:var(--ink);border-radius:7px;padding:5px 10px;cursor:pointer}
.filters .cnt{font-size:12px;color:var(--muted);margin-inline-start:auto}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:16px}
.card h2{margin:0 0 4px;font-size:16px;font-weight:800;display:flex;align-items:center;gap:8px}.card h2::before{content:"";width:4px;height:18px;background:var(--green);border-radius:2px;display:inline-block}
.card .note{font-size:12.5px;color:var(--muted);margin-bottom:10px}
.hd{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:980px){.g2{grid-template-columns:1fr}}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}@media(max-width:1180px){.g3{grid-template-columns:1fr}}
.tw{overflow:auto;max-height:640px;border:1px solid var(--line);border-radius:10px}
table.t{width:100%;border-collapse:collapse;font-size:12.5px}
table.t th{position:sticky;top:0;background:var(--chip);text-align:start;font-size:11px;letter-spacing:.2px;color:var(--muted);padding:7px 8px;border-bottom:1px solid var(--line);cursor:pointer;white-space:nowrap;user-select:none}
table.t th.s::after{content:" ▾"}table.t th.s.up::after{content:" ▴"}
table.t td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
table.t td.num{text-align:end;font-variant-numeric:tabular-nums;white-space:nowrap}
table.t td.ttl{min-width:280px;max-width:460px}table.t td.agc{min-width:190px}
.ar{font-family:var(--eh-font-ar,"Segoe UI",Tahoma,Arial,sans-serif)}
.tag{font-size:10.5px;font-weight:700;border-radius:5px;padding:1px 7px;display:inline-block;white-space:nowrap;cursor:help}
.tag.Core{background:var(--core);color:#fff}.tag.Adjacent{background:var(--adj);color:#fff}.tag.NotEH{background:var(--chip);color:var(--muted);border:1px solid var(--line)}
.st{font-size:11px;font-weight:700;border-radius:5px;padding:1px 7px;display:inline-block;white-space:nowrap;border:1px solid var(--line)}
.st.Won{background:#D7EFE3;color:#14532D;border-color:#9CCDB3}.st.Lost{background:#F6DADA;color:#7A1F1F;border-color:#E3A9A9}.st.Bid{background:#DCE8F7;color:#123E73;border-color:#A9C4E8}.st.Studied{background:var(--chip);color:var(--ink)}.st.Notstudied{background:transparent;color:var(--muted)}
body.dark .st.Won{background:#163A28;color:#BFE8D0}body.dark .st.Lost{background:#3D1E1E;color:#F2C2C2}body.dark .st.Bid{background:#16304F;color:#C4DAF5}
.pri{color:var(--amber);font-weight:800;cursor:help}
.days{font-weight:700;white-space:nowrap}.days.soon{color:var(--red)}.days.mid{color:var(--amber)}.days.closed{color:var(--muted);font-weight:500}
.ref{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;white-space:nowrap}
.copy{font:600 10.5px inherit;margin-inline-start:4px;background:none;border:1px solid var(--line);border-radius:5px;color:var(--muted);cursor:pointer;padding:0 5px}
.empty{font-size:12.5px;color:var(--muted);background:var(--chip);border:1px dashed var(--line);border-radius:8px;padding:12px 14px}
.png{font:600 11px inherit;background:var(--chip);border:1px solid var(--line);color:var(--green);border-radius:7px;padding:5px 10px;cursor:pointer}
.legend{display:flex;gap:14px;font-size:12px;color:var(--muted);margin:2px 0 6px}.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-inline-end:5px;vertical-align:-1px}
svg.ch{width:100%;height:auto;display:block}svg.ch text{font-family:var(--eh-font,"Segoe UI",Tahoma,Arial,sans-serif);fill:var(--muted);font-size:11px}
svg.ch .lbl{fill:var(--ink);font-weight:700}svg.ch .grid{stroke:var(--grid)}svg.ch .hit{fill:transparent;cursor:default}
#tip{position:fixed;pointer-events:none;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:12px;box-shadow:0 4px 14px rgba(0,0,0,.15);display:none;z-index:20;max-width:320px}
.nts li{margin:0 0 6px;font-size:13px}
.foot{font-size:11.5px;color:var(--muted);text-align:center;margin-top:20px;line-height:1.6}
.arrow.up{color:var(--green)}.arrow.down{color:var(--red)}.arrow.flat{color:var(--muted)}
"""

JS = r"""
const D=JSON.parse(document.getElementById('ET').textContent);
let LANG='en';try{LANG=localStorage.getItem('ehhub.lang')||'en'}catch(e){}
const L=(en,ar)=>LANG==='ar'?ar:en, $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const SL={};D.service_lines.forEach(s=>SL[s.id]=s);
const slName=i=>SL[i]?L(SL[i].en,SL[i].ar):'';
const NOW=new Date();
const fmtN=n=>n==null?'—':Number(n).toLocaleString(LANG==='ar'?'ar-SA-u-nu-latn':'en-GB');
const fmtD=s=>{if(!s)return '—';const d=new Date(String(s).slice(0,10)+'T00:00:00');return isNaN(d)?esc(s):d.toLocaleDateString(LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB',{day:'numeric',month:'short',year:'numeric'})};
const fmtDT=s=>{if(!s)return '—';const p=String(s).trim().split(/\s+/);return fmtD(p[0])+(p[1]?`<div style="font-size:11px;color:var(--muted)">${esc(p[1])}</div>`:'')};
function deadline(t){const s=(t.sub||'').trim();if(!s)return null;const d=new Date(s.replace(' ','T')+(s.length>10?':00':'T23:59:00')+'+03:00');return isNaN(d)?null:d}
function daysLeft(t){const d=deadline(t);if(!d)return null;const ms=d-NOW;return ms<0?-1:Math.floor(ms/864e5)}
function isOpen(t){const n=daysLeft(t);return n!=null?n>=0:t.is_open}
const TYPE_EN={'منافسة عامة':'Public tender','شراء مباشر':'Direct purchase','منافسة محدودة':'Limited tender','منافسة إتفاقية إطارية':'Framework agreement','المزايدة العكسية الالكترونية':'Reverse auction','منافسات الشركات الكبرى':'Large companies tender'};
const typeName=s=>LANG==='ar'?s:(TYPE_EN[s]||s);
const CAT={'EH Clients':'عملاء آفاق البيئة','Clients / Potential Clients':'عملاء / عملاء محتملون','Government Clients & Institutions':'جهات حكومية ومؤسسات','Regulators & Compliance Bodies':'جهات تنظيمية ورقابية','Direct Competitors':'منافسون مباشرون','Active Competitors':'منافسون نشطون','Indirect / Adjacent Competitors':'منافسون غير مباشرين','Potential Collaborators':'شركاء محتملون','EH Partners':'شركاء آفاق','Suppliers / Subcontractors':'موردون / مقاولو باطن','Industry Associations & Academia':'جمعيات وجهات أكاديمية'};
const catName=c=>LANG==='ar'?(CAT[c]||c):c;
const STAT={'Won':['Won','فازت'],'Lost':['Lost','خسرت'],'Bid':['Bid submitted','قُدِّم عرض'],'Studied':['Studied','تمت الدراسة'],'Not studied':['Not studied','لم تُدرس']};
const REL={'Core':['Core','أساسي'],'Adjacent':['Adjacent','مجاور'],'Not EH':['Not EH','خارج نطاق آفاق']};
const PRI={'tier':['agency is Tier 1 or Government on the stakeholder map','الجهة من الفئة الأولى أو حكومية في خريطة أصحاب المصلحة'],'client':['agency is an EH client','الجهة عميل لآفاق البيئة'],'regulator':['agency is a regulator','الجهة تنظيمية'],'giga':['giga-project or PIF entity','مشروع كبير أو جهة تابعة لصندوق الاستثمارات العامة']};

// ---------- filters
const F={q:'',rel:'rel',status:'open',line:'',agency:'',tier:'',cat:'',type:'',from:'',to:'',pri:false};
function pass(t){
  if(F.rel==='rel'&&t.relevance==='Not EH')return false;
  if(F.rel==='Core'&&t.relevance!=='Core')return false;
  if(F.rel==='Adjacent'&&t.relevance!=='Adjacent')return false;
  if(F.status==='open'&&!isOpen(t))return false;
  if(F.status==='closed'&&isOpen(t))return false;
  if(F.line&&!t.service_lines.includes(+F.line))return false;
  if(F.agency&&t.agency!==F.agency)return false;
  if(F.tier&&((t.map||{}).Tier||'none')!==F.tier)return false;
  if(F.cat&&((t.map||{}).Category||'none')!==F.cat)return false;
  if(F.type&&t.type!==F.type)return false;
  if(F.from&&(t.pub||'')<F.from)return false;
  if(F.to&&(t.pub||'')>F.to)return false;
  if(F.pri&&!t.priority)return false;
  if(F.q){const q=F.q.toLowerCase();if(!((t.title+' '+t.agency+' '+t.ref+' '+t.department).toLowerCase().includes(q)))return false}
  return true}
// charts and rankings ignore the open/closed filter unless it is set to closed, so they show the market, not just today's list
function passMkt(t){const s=F.status;F.status=(s==='open'?'all':s);const r=pass(t);F.status=s;return r}

function opts(id,vals,label,fmt){const el=$(id),cur=el.value;el.innerHTML=`<option value="">${label}</option>`+vals.map(v=>`<option value="${esc(v)}">${esc(fmt?fmt(v):v)}</option>`).join('');el.value=cur}
function buildFilters(){
  const T=D.tenders;
  $('f-rel').innerHTML=[['rel',L('Relevant (Core + Adjacent)','ذات صلة (أساسي + مجاور)')],['Core',L('Core only','أساسي فقط')],['Adjacent',L('Adjacent only','مجاور فقط')],['all',L('All captured tenders','كل المنافسات الملتقطة')]].map(([v,l])=>`<option value="${v}">${l}</option>`).join('');$('f-rel').value=F.rel;
  $('f-status').innerHTML=[['open',L('Open','مفتوحة')],['closed',L('Closed','مغلقة')],['all',L('Open and closed','المفتوحة والمغلقة')]].map(([v,l])=>`<option value="${v}">${l}</option>`).join('');$('f-status').value=F.status;
  opts('f-line',D.service_lines.map(s=>String(s.id)),L('All service lines','كل خطوط الخدمة'),v=>slName(+v));
  opts('f-agency',[...new Set(T.map(t=>t.agency))].sort((a,b)=>a.localeCompare(b,'ar')),L('All agencies','كل الجهات'));
  opts('f-tier',[...new Set(T.map(t=>(t.map||{}).Tier||'none'))].sort(),L('All tiers','كل الفئات'),v=>v==='none'?L('Not on the map','غير موجودة في الخريطة'):v==='GOV'?L('Government','حكومية'):v);
  opts('f-cat',[...new Set(T.map(t=>(t.map||{}).Category||'none'))].sort(),L('All map categories','كل تصنيفات الخريطة'),v=>v==='none'?L('Not on the map','غير موجودة في الخريطة'):catName(v));
  opts('f-type',[...new Set(T.map(t=>t.type))].sort(),L('All tender types','كل أنواع المنافسات'),typeName);
}

// ---------- tooltip
const tip=$('tip');
function showTip(e,html){tip.innerHTML=html;tip.style.display='block';const x=Math.min(e.clientX+14,innerWidth-tip.offsetWidth-8),y=Math.min(e.clientY+14,innerHeight-tip.offsetHeight-8);tip.style.left=x+'px';tip.style.top=y+'px'}
function hideTip(){tip.style.display='none'}
document.addEventListener('mousemove',e=>{const h=e.target.closest&&e.target.closest('[data-tip]');if(h)showTip(e,h.getAttribute('data-tip'));else hideTip()});

// ---------- charts (plain SVG)
function hbars(id,rows,opt={}){ // rows: [{label, values:[core,adj] | value, tip}]
  const W=560,rowH=24,pad=opt.labelW||210,top=6,H=top+rows.length*rowH+6,stack=rows.length&&Array.isArray(rows[0].values);
  if(!rows.length){$(id).innerHTML=`<div class="empty">${opt.empty||L('Searched, none found for these filters.','تم البحث، ولا توجد نتائج لهذه المرشحات.')}</div>`;return}
  const max=Math.max(1,...rows.map(r=>stack?r.values.reduce((a,b)=>a+b,0):r.value)),sx=v=>(W-pad-46)*v/max;
  let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opt.title||'')}">`;
  rows.forEach((r,i)=>{const y=top+i*rowH;const lab=r.label.length>42?r.label.slice(0,41)+'…':r.label;
    s+=`<text x="${LANG==='ar'?W-4:4}" y="${y+16}" text-anchor="${LANG==='ar'?'end':'start'}" class="${r.ar?'ar':''}">${esc(lab)}</text>`;
    let x=pad;const vals=stack?r.values:[r.value],cols=stack?['var(--core)','var(--adj)']:['var(--bar)'];
    vals.forEach((v,k)=>{if(!v)return;const w=Math.max(2,sx(v)-(k<vals.length-1?2:0));const xx=LANG==='ar'?W-x-w:x;s+=`<rect x="${xx}" y="${y+5}" width="${w}" height="14" rx="3" fill="${cols[k]}"/>`;x+=sx(v)});
    const tot=vals.reduce((a,b)=>a+b,0),tx=LANG==='ar'?W-x-6:x+6;
    s+=`<text x="${tx}" y="${y+16}" class="lbl" text-anchor="${LANG==='ar'?'end':'start'}">${fmtN(tot)}${opt.unit||''}</text>`;
    s+=`<rect class="hit" x="0" y="${y}" width="${W}" height="${rowH}" data-tip="${esc(r.tip||(r.label+': '+fmtN(tot)))}"/>`});
  $(id).innerHTML=s+'</svg>'}
function vbars(id,cats,series,opt={}){ // series: [{name,color,vals[]}] stacked
  if(!cats.length||!series.some(s=>s.vals.some(v=>v))){$(id).innerHTML=`<div class="empty">${opt.empty||L('Searched, none found for these filters.','تم البحث، ولا توجد نتائج لهذه المرشحات.')}</div>`;return}
  const W=560,H=230,pl=38,pb=34,pt=10,iw=W-pl-10,ih=H-pb-pt,tot=cats.map((c,i)=>series.reduce((a,s)=>a+s.vals[i],0)),max=Math.max(1,...tot);
  const raw=max/4,mag=Math.pow(10,Math.floor(Math.log10(raw))),step=Math.max(1,[1,2,5,10].map(m=>m*mag).find(v=>v>=raw)),top=step*4,bw=Math.min(36,iw/cats.length*0.62),gx=i=>pl+iw*(i+0.5)/cats.length;
  let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" direction="ltr" role="img" aria-label="${esc(opt.title||'')}">`;
  for(let k=0;k<=4;k++){const y=pt+ih-ih*k/4;s+=`<line class="grid" x1="${pl}" x2="${W-6}" y1="${y}" y2="${y}"/><text x="${pl-6}" y="${y+4}" text-anchor="end">${step*k}</text>`}
  cats.forEach((c,i)=>{let y=pt+ih;const ord=LANG==='ar'?cats.length-1-i:i,x=gx(ord)-bw/2;
    series.forEach((se,k)=>{const v=se.vals[i];if(!v)return;const h=ih*v/top;s+=`<rect x="${x}" y="${y-h+(k?0:0)}" width="${bw}" height="${Math.max(1,h-2)}" rx="3" fill="${se.color}"/>`;y-=h});
    if(tot[i]&&opt.valueLabels!==false)s+=`<text x="${gx(ord)}" y="${y-4}" text-anchor="middle" class="lbl">${tot[i]}</text>`;
    s+=`<text x="${gx(ord)}" y="${H-14}" text-anchor="middle">${esc(c.label)}</text>`;
    s+=`<rect class="hit" x="${gx(ord)-iw/cats.length/2}" y="${pt}" width="${iw/cats.length}" height="${ih}" data-tip="${esc('<b>'+(c.tip||c.label)+'</b><br>'+series.map((se,k)=>se.name+': '+se.vals[i]).join('<br>')+(series.length>1?'<br>'+L('Total','المجموع')+': '+tot[i]:''))}"/>`});
  const lg=opt.legend&&series.length>1?`<div class="lgd" style="display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:4px">${series.map(se=>`<span style="display:inline-flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:2px;background:${se.color};display:inline-block"></i>${esc(se.name)}</span>`).join('')}</div>`:'';
  $(id).innerHTML=s+'</svg>'+lg}
function exportPNG(id,name){const svg=$(id).querySelector('svg');if(!svg)return;const cs=getComputedStyle(document.body);
  let src=new XMLSerializer().serializeToString(svg);
  ['--core','--adj','--bar','--bar2','--grid','--muted','--ink'].forEach(v=>{src=src.split('var('+v+')').join(cs.getPropertyValue(v).trim())});
  src=src.replace('<svg ','<svg style="font-family:Segoe UI,Tahoma,Arial,sans-serif" ').replace(/class="grid"/g,`stroke="${cs.getPropertyValue('--grid').trim()}"`).replace(/<text /g,`<text fill="${cs.getPropertyValue('--muted').trim()}" font-size="11" `).replace(/class="hit"[^/]*\/>/g,'/>');
  const vb=svg.viewBox.baseVal,img=new Image(),c=document.createElement('canvas');c.width=vb.width*2;c.height=vb.height*2;
  img.onload=()=>{const x=c.getContext('2d');x.fillStyle=cs.getPropertyValue('--card').trim()||'#fff';x.fillRect(0,0,c.width,c.height);x.drawImage(img,0,0,c.width,c.height);const a=document.createElement('a');a.download=name+'.png';a.href=c.toDataURL('image/png');a.click()};
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(src)}

// ---------- sections
let SORT={k:'sub',dir:1};
function stTag(s,t){const tr=t&&t.tracker;return `<span class="st ${s.replace(' ','')}">${L(...STAT[s])}</span>`+(tr?`<div style="font-size:11px;color:var(--muted);margin-top:2px;white-space:nowrap" title="${esc(L('Row number in the bid tracking sheet (EH-WIN-02-F01)','رقم الصف في جدول متابعة المنافسات'))}">${L('Tracker','الجدول')} #${tr.sn} · ${tr.year}</div>`:'')}
function relTag(t){const terms=(t.matched_terms||[]).map(x=>'«'+x+'»').join('، ');
  const why=t.decided_by==='you'?L('Set by your review decision','حُدد بقرار المراجعة'):(t.relevance==='Not EH'?L('No EH service term matched','لم تطابق أي عبارة من خدمات آفاق'):L('Matched: ','طابق: ')+terms);
  return `<span class="tag ${t.relevance.replace(' ','')}" data-tip="${esc(why)}">${L(...REL[t.relevance])}</span>`}
function daysCell(t){const n=daysLeft(t);if(n==null)return '—';if(n<0)return `<span class="days closed">${L('Closed','مغلقة')}</span>`;const c=n<=7?'soon':n<=14?'mid':'';return `<span class="days ${c}">${n===0?L('Today','اليوم'):n+' '+L(n===1?'day':'days',n>=3&&n<=10?'أيام':'يوم')}</span>`}
function priCell(t){return t.priority?`<span class="pri" data-tip="${esc(t.priority_why.map(k=>L(...PRI[k])).join('<br>'))}">★</span>`:''}
function table(rows){
  const C={
   title:[L('Tender (as published on Etimad)','المنافسة (كما نُشرت في اعتماد)'),t=>t.title,t=>`<td class="ttl ar" dir="rtl">${esc(t.title)}</td>`],
   rel:[L('Relevance','الصلة'),t=>t.relevance,t=>`<td>${relTag(t)}</td>`],
   eh:[L('EH status','حالة آفاق'),t=>t.eh_status,t=>`<td>${stTag(t.eh_status,t)}</td>`],
   days:[L('Days left','الأيام المتبقية'),t=>{const n=daysLeft(t);return n==null?9999:n},t=>`<td>${daysCell(t)}</td>`],
   sub:[L('Submission deadline','آخر موعد للتقديم'),t=>t.sub,t=>`<td class="num">${fmtDT(t.sub)}</td>`],
   agency:[L('Agency','الجهة'),t=>t.agency,t=>`<td class="ar agc" dir="rtl">${esc(t.agency)}${t.department?`<div style="font-size:11px;color:var(--muted)">${esc(t.department)}</div>`:''}</td>`],
   line:[L('Service line','خط الخدمة'),t=>slName(t.service_lines[0])||'',t=>`<td>${t.service_lines.map(slName).join('<br>')||'—'}</td>`],
   type:[L('Type','النوع'),t=>t.type,t=>`<td>${esc(typeName(t.type))}</td>`],
   fee:[L('Document fee (SAR)','قيمة الكراسة (ريال)'),t=>t.fee_sar??-1,t=>`<td class="num">${t.fee_sar==null?'—':t.fee_sar===0?L('Free','مجانًا'):fmtN(t.fee_sar)}</td>`],
   enq:[L('Enquiries by','آخر موعد للاستفسارات'),t=>t.enq,t=>`<td class="num">${fmtD(t.enq)}</td>`],
   open:[L('Bid opening','فتح العروض'),t=>t.open,t=>`<td class="num">${fmtDT(t.open)}</td>`],
   region:[L('Region','المنطقة'),t=>'',t=>`<td style="color:var(--muted)" data-tip="${esc(L('Region is shown only on each tender\'s own Etimad page and is not captured yet.','تظهر المنطقة في صفحة المنافسة فقط ولم تُلتقط بعد.'))}">${L('Not captured','غير ملتقطة')}</td>`],
   pri:[L('Priority','أولوية'),t=>t.priority?0:1,t=>`<td style="text-align:center">${priCell(t)}</td>`],
   ref:[L('Etimad reference','الرقم المرجعي'),t=>t.ref,t=>`<td><span class="ref">${esc(t.ref)}</span><button class="copy" data-ref="${esc(t.ref)}" title="${L('Copy the reference to search on Etimad','انسخ الرقم المرجعي للبحث في اعتماد')}">⧉</button></td>`]};
  const order=['title','rel','eh','days','sub','agency','line','type','fee','enq','open','pri','region','ref'];
  const k=(C[SORT.k]||C.sub)[1];rows=rows.slice().sort((a,b)=>{const x=k(a),y=k(b);return (x>y?1:x<y?-1:0)*SORT.dir});
  let h=`<table class="t"><thead><tr>${order.map(c=>`<th data-k="${c}" class="${SORT.k===c?'s'+(SORT.dir<0?' up':''):''}">${C[c][0]}</th>`).join('')}</tr></thead><tbody>`;
  rows.forEach(t=>{h+='<tr>'+order.map(c=>C[c][2](t)).join('')+'</tr>'});
  return h+'</tbody></table>'}

function render(){
  document.documentElement.lang=LANG;document.documentElement.dir=LANG==='ar'?'rtl':'ltr';
  document.querySelectorAll('[data-en]').forEach(e=>e.textContent=L(e.dataset.en,e.dataset.ar));
  document.querySelectorAll('[data-ph-en]').forEach(e=>e.placeholder=L(e.dataset.phEn,e.dataset.phAr));
  buildFilters();
  const T=D.tenders,REL_T=T.filter(t=>t.relevance!=='Not EH');
  // stamp
  const lc=D.last_capture,age=lc?Math.floor((NOW-new Date(lc+'T08:00:00+03:00'))/864e5):null;
  $('cap').className='cap'+(age==null||age>8?' stale':'');
  $('cap').textContent=lc?L('Last captured: ','آخر التقاط: ')+fmtD(lc)+(age>8?L(` — ${age} days ago, not live`,` — قبل ${age} يومًا، غير محدّث`):''):L('No capture loaded yet','لم يُحمَّل أي التقاط بعد');
  // KPIs (always on relevant tenders, independent of the filters, so the strip reads the same for everyone)
  const op=REL_T.filter(isOpen),wk=lc?new Date(new Date(lc)-6*864e5).toISOString().slice(0,10):'';
  const K=[[op.length,L('Open relevant tenders','منافسات ذات صلة مفتوحة'),''],
   [op.filter(t=>daysLeft(t)<=7).length,L('Closing within 7 days','تُغلق خلال 7 أيام'),'warn'],
   [op.filter(t=>daysLeft(t)<=14).length,L('Closing within 14 days','تُغلق خلال 14 يومًا'),'warn'],
   [REL_T.filter(t=>t.first_seen===lc&&(t.pub||'')>=wk).length,L('New relevant this week (published in the 7 days before the last capture)','جديدة ذات صلة هذا الأسبوع (نُشرت خلال 7 أيام قبل آخر التقاط)'),'blue'],
   [op.filter(t=>t.priority).length,L('Priority tenders open','منافسات ذات أولوية مفتوحة'),''],
   [op.filter(t=>t.eh_status==='Not studied').length,L('Open and not yet in the bid tracker','مفتوحة وغير مسجلة في جدول المنافسات'),'warn']];
  const MW=(D.market&&D.market.windows||[]).slice(-1)[0],cntA=(D.counts||[]).filter(c=>/active/i.test(c.counter)).sort((a,b)=>a.capture_date<b.capture_date?1:-1)[0];
  const KM=[];
  if(MW)KM.push([MW.rows.filter(r=>r.dim==='type').reduce((x,r)=>x+r.n,0),L(`All tenders published on Etimad, ${fmtD(MW.from)} – ${fmtD(MW.to)}`,`كل المنافسات المنشورة في اعتماد، ${fmtD(MW.from)} – ${fmtD(MW.to)}`),'mkt']);
  KM.push([cntA?+cntA.value:null,L('Active tenders on Etimad today, all sectors (site counter)','المنافسات النشطة في اعتماد اليوم بكل القطاعات (عدّاد المنصة)'),'mkt']);
  KM.push([T.length,L('Tenders captured by EH searches, any relevance','منافسات التقطتها بحوث آفاق، بكل درجات الصلة'),'mkt']);
  KM.push([REL_T.length,L('Of which relevant to EH (Core + Adjacent)','منها ذات صلة بآفاق (أساسي + مجاور)'),'mkt']);
  $('kpism').innerHTML=KM.map(([v,l,c])=>`<div class="kc ${c}"><div class="v">${fmtN(v)}</div><div class="l">${l}</div></div>`).join('');
  $('kpis').innerHTML=K.map(([v,l,c])=>`<div class="kc ${c}"><div class="v">${fmtN(v)}</div><div class="l">${l}</div></div>`).join('');
  // listing
  const rows=T.filter(pass);
  $('cnt').textContent=L(`${rows.length} of ${T.length} captured tenders shown`,`عرض ${rows.length} من ${T.length} منافسة ملتقطة`);
  $('list').innerHTML=rows.length?table(rows):`<div class="empty">${L('Searched, none found for these filters','تم البحث، ولا توجد نتائج لهذه المرشحات')}${lc?' — '+L('capture of ','التقاط ')+fmtD(lc):''}.</div>`;
  // market
  const M=T.filter(t=>passMkt(t)&&t.relevance!=='Not EH');
  const months=[...new Set(T.map(t=>(t.pub||'').slice(0,7)).filter(Boolean))].sort().slice(-12);
  vbars('ch-month',months.map(m=>({label:new Date(m+'-01T00:00:00').toLocaleDateString(LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB',{month:'short',year:'2-digit'})})),
    [{name:L('Core','أساسي'),color:'var(--core)',vals:months.map(m=>M.filter(t=>t.relevance==='Core'&&t.pub.startsWith(m)).length)},
     {name:L('Adjacent','مجاور'),color:'var(--adj)',vals:months.map(m=>M.filter(t=>t.relevance==='Adjacent'&&t.pub.startsWith(m)).length)}],{title:L('Relevant tenders by month published','المنافسات ذات الصلة حسب شهر النشر')});
  const firstPub=T.reduce((m,t)=>t.pub&&t.pub<m?t.pub:m,'9999');$('mcov').textContent=T.length?L(`Covers what has been captured so far (tenders published from ${fmtD(firstPub)}). Older months fill in with the 3-year history load.`,`يغطي ما التُقط حتى الآن (منافسات منشورة منذ ${fmtD(firstPub)}). تكتمل الأشهر الأقدم بعد تحميل سجل السنوات الثلاث.`):'';
  const lineRows=D.service_lines.map(s=>({label:slName(s.id),values:[M.filter(t=>t.relevance==='Core'&&t.service_lines.includes(s.id)).length,M.filter(t=>t.relevance==='Adjacent'&&t.service_lines.includes(s.id)).length]})).filter(r=>r.values[0]+r.values[1]).sort((a,b)=>(b.values[0]+b.values[1])-(a.values[0]+a.values[1]));
  const unl=M.filter(t=>!t.service_lines.length).length;
  if(unl)lineRows.push({label:L('General waste work (no single line)','أعمال نفايات عامة (دون خط محدد)'),values:[0,unl]});
  hbars('ch-line',lineRows,{labelW:290,title:L('Relevant tenders by service line','حسب خط الخدمة')});
  const types=[...new Set(M.map(t=>t.type))];
  hbars('ch-type',types.map(ty=>({label:typeName(ty),values:[M.filter(t=>t.type===ty&&t.relevance==='Core').length,M.filter(t=>t.type===ty&&t.relevance==='Adjacent').length]})).sort((a,b)=>(b.values[0]+b.values[1])-(a.values[0]+a.values[1])),{labelW:200});
  $('ch-region').innerHTML=`<div class="empty">${L('Region is shown only on each tender\'s own Etimad page, so it is not captured yet. Searched, none found','المنطقة تظهر في صفحة كل منافسة فقط، لذا لم تُلتقط بعد. تم البحث، ولا توجد بيانات')}${lc?' — '+fmtD(lc):''}.</div>`;
  // growth / new lines need history
  const span=D.captures.length?Math.round((new Date(D.tenders.reduce((m,t)=>t.pub>m?t.pub:m,'0000'))-new Date(D.tenders.reduce((m,t)=>t.pub&&t.pub<m?t.pub:m,'9999')))/864e5/30.4):0;
  $('growth').innerHTML=span>=24?growth(M):`<div class="empty">${L(`Growth compares the last 12 months with the 12 before. The data covers about ${span} months so far, so this view fills in once the 3-year history is loaded.`,`يقارن النمو آخر 12 شهرًا بالـ12 التي قبلها. تغطي البيانات نحو ${span} أشهر حتى الآن، وتكتمل هذه النافذة بعد تحميل سجل السنوات الثلاث.`)}</div>`;
  const cnt=(D.counts||[]).filter(c=>/active/i.test(c.counter)).sort((a,b)=>a.capture_date<b.capture_date?1:-1)[0];
  $('share').innerHTML=cnt?L(`At the last capture Etimad listed <b>${fmtN(+cnt.value)}</b> active tenders across all sectors; <b>${op.length}</b> of them are relevant to EH (${(100*op.length/+cnt.value).toFixed(1)}%).`,`عند آخر التقاط أدرجت منصة اعتماد <b>${fmtN(+cnt.value)}</b> منافسة نشطة في كل القطاعات، منها <b>${op.length}</b> ذات صلة بآفاق البيئة (${(100*op.length/+cnt.value).toFixed(1)}%).`):`<span class="empty">${L('Searched, none found: no market counter recorded yet.','تم البحث، ولا يوجد عدّاد سوق مسجل بعد.')}</span>`;
  $('notes').innerHTML=D.notes.length?'<ul class="nts">'+D.notes.map(n=>`<li>${esc(L(n.en,n.ar))}</li>`).join('')+'</ul>'+`<div style="font-size:11.5px;color:var(--muted)">${L('Figures from all captured tenders, not the current filters.','الأرقام من كل المنافسات الملتقطة وليست من المرشحات الحالية.')}</div>`:`<div class="empty">${L('Searched, none found.','تم البحث، ولا توجد نتائج.')}</div>`;
  // requesters
  const byA={};M.forEach(t=>{const a=byA[t.agency]=byA[t.agency]||{n:0,fee:0,rec:t.map,first:t.pub,recent:0,prior:0};a.n++;a.fee+=t.fee_sar||0;if(t.pub<a.first)a.first=t.pub;const age=(NOW-new Date(t.pub))/864e5;if(age<=90)a.recent++;else if(age<=180)a.prior++});
  const AG=Object.entries(byA).sort((a,b)=>b[1].n-a[1].n||b[1].fee-a[1].fee);
  hbars('ch-agency',AG.slice(0,10).map(([k,a])=>({label:k,ar:1,value:a.n,tip:`<b>${esc(k)}</b><br>${L('Relevant tenders','منافسات ذات صلة')}: ${a.n}<br>${L('Document fees (estimate of size, not contract value)','قيمة الكراسات (تقدير للحجم وليست قيمة العقد)')}: ${fmtN(a.fee)} ${L('SAR','ريال')}`})),{labelW:250});
  $('agtable').innerHTML=AG.length?`<table class="t"><thead><tr><th>${L('Agency','الجهة')}</th><th>${L('Relevant tenders','منافسات ذات صلة')}</th><th>${L('Document fees (SAR, size estimate)','قيمة الكراسات (ريال، تقدير)')}</th><th>${L('Trend: last 90 days vs the 90 before','الاتجاه: آخر 90 يومًا مقابل السابقة')}</th><th>${L('Tier','الفئة')}</th><th>${L('Map category','تصنيف الخريطة')}</th><th>${L('EH client','عميل لآفاق')}</th><th>${L('Client value (SAR)','قيمة العميل (ريال)')}</th></tr></thead><tbody>`+AG.map(([k,a])=>{const r=a.rec||{},tr=a.recent>a.prior?['up','▲']:a.recent<a.prior?['down','▼']:['flat','■'];return `<tr><td class="ar" dir="rtl">${esc(k)}</td><td class="num">${a.n}</td><td class="num">${fmtN(a.fee)}</td><td><span class="arrow ${tr[0]}">${tr[1]}</span> ${a.recent} / ${a.prior}</td><td>${r.Tier?esc(r.Tier==='GOV'?L('Government','حكومية'):r.Tier):`<span style="color:var(--muted)">${L('Not on the map','غير موجودة في الخريطة')}</span>`}</td><td>${esc(r.Category?catName(r.Category):'—')}</td><td>${r['EH Client']==='Yes'?L('Yes','نعم'):r.Name?L('No','لا'):'—'}</td><td class="num">${r['Client Value (SAR)']?fmtN(r['Client Value (SAR)']):'—'}</td></tr>`}).join('')+'</tbody></table>':`<div class="empty">${L('Searched, none found for these filters.','تم البحث، ولا توجد نتائج لهذه المرشحات.')}</div>`;
  const sixAgo=new Date(NOW-182*864e5).toISOString().slice(0,10);
  $('newiss').innerHTML=span>=9?(AG.filter(([k,a])=>a.first>=sixAgo).map(([k])=>`<span class="st ar" style="margin:2px">${esc(k)}</span>`).join('')||`<div class="empty">${L('Searched, none found.','تم البحث، ولا توجد نتائج.')}</div>`):`<div class="empty">${L('"New issuer" means no relevant tender before the last 6 months. With about '+span+' months of data every agency would look new, so this list waits for the history load.','«جهة جديدة» تعني عدم وجود منافسة ذات صلة قبل آخر 6 أشهر. ومع نحو '+span+' أشهر من البيانات ستبدو كل الجهات جديدة، لذا تنتظر هذه القائمة تحميل السجل.')}</div>`;
  // priority
  const PR=M.filter(t=>t.priority),po=PR.filter(isOpen),pp=PR.filter(t=>!isOpen(t));
  $('pri-open').innerHTML=po.length?mini(po,true):`<div class="empty">${L('Searched, none found for these filters.','تم البحث، ولا توجد نتائج لهذه المرشحات.')}</div>`;
  $('pri-past').innerHTML=pp.length?mini(pp,false):`<div class="empty">${L('Searched, none found for these filters.','تم البحث، ولا توجد نتائج لهذه المرشحات.')}</div>`;
  // whitespace
  const WS=AG.filter(([k,a])=>a.n>=2&&!(a.rec&&a.rec['EH Client']==='Yes'));
  $('white').innerHTML=WS.length?`<table class="t"><thead><tr><th>${L('Agency','الجهة')}</th><th>${L('Relevant tenders','منافسات ذات صلة')}</th><th>${L('On the map as','في الخريطة بوصفها')}</th></tr></thead><tbody>`+WS.map(([k,a])=>`<tr><td class="ar" dir="rtl">${esc(k)}</td><td class="num">${a.n}</td><td>${a.rec?esc(a.rec.Name+' · '+catName(a.rec.Category||'')):`<span style="color:var(--muted)">${L('Not on the map — candidate to add after review','غير موجودة في الخريطة — مرشحة للإضافة بعد المراجعة')}</span>`}</td></tr>`).join('')+'</tbody></table>':`<div class="empty">${L('Searched, none found: no agency outside the EH client list issued two or more relevant tenders in this view.','تم البحث، ولا توجد جهة من خارج عملاء آفاق طرحت منافستين أو أكثر ذات صلة في هذا العرض.')}</div>`;
  renderMarket();
  if(typeof renderAnalyst==='function')renderAnalyst();
  document.querySelectorAll('#list th').forEach(th=>th.onclick=()=>{SORT.dir=(SORT.k===th.dataset.k?-SORT.dir:1);SORT.k=th.dataset.k;render()});
}
function renderMarket(){
  const MK=D.market||{windows:[]},W=MK.windows||[],w=W[W.length-1];
  const none=`<div class="empty">${L('Searched, none found: the full-market capture has not run yet.','تم البحث، ولا توجد بيانات: لم يُشغَّل التقاط السوق الكامل بعد.')}</div>`;
  if(!w){['mk-sector','mk-group','mk-day','mk-agency','mk-type','mk-trend','mk-notes'].forEach(i=>$(i).innerHTML=none);$('mkt-note').textContent='';return}
  const SN=MK.sector_names,GN=MK.group_names,nm=(o)=>L(o.en,o.ar);
  const tot=w.rows.filter(r=>r.dim==='type').reduce((a,r)=>a+r.n,0);
  $('mkt-note').textContent=L(`Every tender published on Etimad from ${fmtD(w.from)} to ${fmtD(w.to)} (${fmtN(tot)} tenders), whatever its sector — not only what fits EH. Counts only; the filters above do not apply here. Bars split tenders still open at the capture from those already closed.`,`كل منافسة نُشرت في اعتماد من ${fmtD(w.from)} إلى ${fmtD(w.to)} (${fmtN(tot)} منافسة) أيًا كان قطاعها — لا ما يناسب آفاق فقط. أعداد فقط؛ ولا تنطبق المرشحات أعلاه هنا. تفصل الأعمدة المنافسات المفتوحة عند الالتقاط عن المغلقة.`);
  const S=Object.entries(w.sectors).sort((a,b)=>b[1].n-a[1].n);
  hbars('mk-sector',S.map(([k,v])=>({label:nm(SN[k]),values:[v.open,v.n-v.open],tip:`<b>${esc(nm(SN[k]))}</b><br>${L('Tenders','منافسات')}: ${v.n} (${(100*v.n/tot).toFixed(1)}%)<br>${L('Open at capture','مفتوحة عند الالتقاط')}: ${v.open}<br>${L('Document fees (size estimate)','قيمة الكراسات (تقدير للحجم)')}: ${fmtN(v.fees)} ${L('SAR','ريال')}<br><span style="color:var(--muted)">${v.acts.slice(0,4).map(a=>esc(a[0])+' '+a[1]).join('<br>')}</span>`})),{labelW:260});
  const G=Object.entries(w.agency_groups).sort((a,b)=>b[1].n-a[1].n);
  hbars('mk-group',G.map(([k,v])=>({label:nm(GN[k]),value:v.n,tip:`<b>${esc(nm(GN[k]))}</b><br>${L('Tenders','منافسات')}: ${v.n}<br>${L('Document fees (size estimate)','قيمة الكراسات (تقدير للحجم)')}: ${fmtN(v.fees)} ${L('SAR','ريال')}`})),{labelW:240});
  // Per day: every window from the latest capture, joined into one continuous day axis (days with no tenders show as 0).
  const dd={};W.filter(x=>x.capture===w.capture).forEach(x=>x.rows.forEach(r=>{if(r.dim!=='date')return;const k=String(r.key).slice(0,10);if(!/^\d{4}-\d{2}-\d{2}$/.test(k)||k<String(x.from).slice(0,10)||k>String(x.to).slice(0,10))return;dd[k]={n:r.n,open:r.open}}));
  const dk=Object.keys(dd).sort(),DY=[];
  if(dk.length){for(let d=new Date(dk[0]+'T00:00:00Z'),e=new Date(dk[dk.length-1]+'T00:00:00Z');d<=e;d=new Date(+d+864e5)){const k=d.toISOString().slice(0,10);DY.push({key:k,...(dd[k]||{n:0,open:0})})}}
  const thin=DY.length>20?Math.ceil(DY.length/14):1,loc=LANG==='ar'?'ar-SA-u-ca-gregory-nu-latn':'en-GB';let lastM=null;
  vbars('mk-day',DY.map((r,i)=>{const d=new Date(r.key+'T00:00:00'),full=d.toLocaleDateString(loc,{weekday:'short',day:'numeric',month:'short'});
      if(i%thin)return {label:'',tip:full};const m=d.getMonth(),lab=m!==lastM?d.toLocaleDateString(loc,{day:'numeric',month:'short'}):String(d.getDate());lastM=m;return {label:lab,tip:full}}),
    [{name:L('Open at capture','مفتوحة عند الالتقاط'),color:'var(--core)',vals:DY.map(r=>r.open)},{name:L('Closed','مغلقة'),color:'var(--adj)',vals:DY.map(r=>r.n-r.open)}],
    {legend:true,valueLabels:DY.length<=20,title:L('Tenders published per day','المنافسات المنشورة يوميًا')});
  if(DY.length)$('mk-day').insertAdjacentHTML('beforeend',`<div style="font-size:11.5px;color:var(--muted);margin-top:2px">${L(`${fmtD(DY[0].key)} to ${fmtD(DY[DY.length-1].key)}: ${fmtN(DY.reduce((a,r)=>a+r.n,0))} tenders. Fridays and Saturdays are usually empty because agencies publish on working days.`,`من ${fmtD(DY[0].key)} إلى ${fmtD(DY[DY.length-1].key)}: ${fmtN(DY.reduce((a,r)=>a+r.n,0))} منافسة. تكون الجمعة والسبت فارغة غالبًا لأن الجهات تنشر في أيام العمل.`)}</div>`);
  const AG=w.rows.filter(r=>r.dim==='agency').sort((a,b)=>b.n-a.n).slice(0,15);
  hbars('mk-agency',AG.map(r=>({label:r.key,ar:1,value:r.n,tip:`<b>${esc(r.key)}</b><br>${L('Tenders','منافسات')}: ${r.n}<br>${L('Document fees (size estimate)','قيمة الكراسات (تقدير للحجم)')}: ${fmtN(r.fees)} ${L('SAR','ريال')}`})),{labelW:260});
  const TY=w.rows.filter(r=>r.dim==='type').sort((a,b)=>b.n-a.n),tf=TY.reduce((a,r)=>a+r.fees,0)||1;
  $('mk-type').innerHTML=`<table class="t"><thead><tr><th>${L('Tender type','نوع المنافسة')}</th><th>${L('Tenders','منافسات')}</th><th>${L('Share','الحصة')}</th><th>${L('Share of document fees','الحصة من قيمة الكراسات')}</th></tr></thead><tbody>`+TY.map(r=>`<tr><td>${esc(typeName(r.key))}</td><td class="num">${fmtN(r.n)}</td><td class="num">${(100*r.n/tot).toFixed(0)}%</td><td class="num">${(100*r.fees/tf).toFixed(0)}%</td></tr>`).join('')+'</tbody></table>';
  if(W.length>=2){const p=W[W.length-2],pt=p.rows.filter(r=>r.dim==='type').reduce((a,r)=>a+r.n,0)||1;
    const ch=Object.keys(SN).map(k=>({k,now:(w.sectors[k]||{n:0}).n/tot*100,before:(p.sectors[k]||{n:0}).n/pt*100})).map(x=>({...x,d:x.now-x.before})).filter(x=>x.now||x.before).sort((a,b)=>b.d-a.d);
    $('mk-trend').innerHTML=`<table class="t"><thead><tr><th>${L('Sector','القطاع')}</th><th>${L('Share now','الحصة الآن')}</th><th>${L('Share before','الحصة سابقًا')}</th><th>${L('Change (points)','التغير (نقاط)')}</th></tr></thead><tbody>`+ch.map(x=>`<tr><td>${esc(nm(SN[x.k]))}</td><td class="num">${x.now.toFixed(1)}%</td><td class="num">${x.before.toFixed(1)}%</td><td class="num"><span class="arrow ${x.d>0.5?'up':x.d<-0.5?'down':'flat'}">${x.d>0.5?'▲':x.d<-0.5?'▼':'■'}</span> ${x.d>0?'+':''}${x.d.toFixed(1)}</td></tr>`).join('')+`</tbody></table><div style="font-size:11.5px;color:var(--muted);margin-top:4px">${L(`Compares ${fmtD(w.from)}–${fmtD(w.to)} with ${fmtD(p.from)}–${fmtD(p.to)}.`,`مقارنة ${fmtD(w.from)}–${fmtD(w.to)} بـ${fmtD(p.from)}–${fmtD(p.to)}.`)}</div>`}
  else $('mk-trend').innerHTML=`<div class="empty">${L('Expansion is measured as a change in each sector\'s share between capture windows. One window is on file so far; the comparison appears after the next weekly full-market capture.','يُقاس التوسع بتغيّر حصة كل قطاع بين فترات الالتقاط. توجد فترة واحدة حتى الآن؛ وتظهر المقارنة بعد الالتقاط الأسبوعي التالي للسوق الكامل.')}</div>`;
  $('mk-notes').innerHTML=(D.market_notes||[]).length?'<ul class="nts">'+D.market_notes.map(n=>`<li>${esc(L(n.en,n.ar))}</li>`).join('')+'</ul>':none;
}
function growth(M){const y1=new Date(NOW-365*864e5).toISOString().slice(0,10),y2=new Date(NOW-730*864e5).toISOString().slice(0,10);
  const rows=D.service_lines.map(s=>{const a=M.filter(t=>t.service_lines.includes(s.id)&&t.pub>=y1).length,b=M.filter(t=>t.service_lines.includes(s.id)&&t.pub>=y2&&t.pub<y1).length;return {s,a,b,d:a-b}}).filter(r=>r.a||r.b).sort((x,y)=>y.d-x.d);
  if(!rows.length)return `<div class="empty">${L('Searched, none found.','تم البحث، ولا توجد نتائج.')}</div>`;
  return `<table class="t"><thead><tr><th>${L('Service line','خط الخدمة')}</th><th>${L('Last 12 months','آخر 12 شهرًا')}</th><th>${L('12 months before','الـ12 شهرًا السابقة')}</th><th>${L('Change','التغير')}</th></tr></thead><tbody>`+rows.map(r=>`<tr><td>${slName(r.s.id)}${!r.b&&r.a?` <span class="st">${L('New','جديد')}</span>`:''}</td><td class="num">${r.a}</td><td class="num">${r.b}</td><td class="num"><span class="arrow ${r.d>0?'up':r.d<0?'down':'flat'}">${r.d>0?'▲':r.d<0?'▼':'■'}</span> ${r.d>0?'+':''}${r.d}</td></tr>`).join('')+'</tbody></table>'}
function mini(rows,open){rows=rows.slice().sort((a,b)=>open?(a.sub>b.sub?1:-1):(a.sub<b.sub?1:-1));return `<table class="t"><thead><tr><th>${L('Tender','المنافسة')}</th><th>${L('Agency','الجهة')}</th><th>${open?L('Days left','الأيام المتبقية'):L('Closed on','أُغلقت في')}</th><th>${L('EH status','حالة آفاق')}</th><th>${L('Outcome on Etimad','النتيجة في اعتماد')}</th></tr></thead><tbody>`+rows.slice(0,25).map(t=>`<tr><td class="ar" dir="rtl">${esc(t.title)}</td><td class="ar" dir="rtl">${esc(t.agency)}</td><td>${open?daysCell(t):fmtD(t.sub)}</td><td>${stTag(t.eh_status,t)}</td><td style="color:var(--muted)">${open?'—':L('Not captured yet','لم تُلتقط بعد')}</td></tr>`).join('')+'</tbody></table>'+(rows.length>25?`<div style="font-size:11.5px;color:var(--muted);margin-top:6px">${L('Showing 25 of '+rows.length+'; use the filters to narrow.','عرض 25 من '+rows.length+'؛ استخدم المرشحات للتضييق.')}</div>`:'')}

// ---------- wiring
function setLang(l){LANG=l;render();document.querySelectorAll('.tog.lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===l))}
function setDark(d){document.body.classList.toggle('dark',d);document.querySelectorAll('.tog.th button').forEach(b=>b.classList.toggle('on',(b.dataset.t==='dark')===d));render()}
window.addEventListener('message',e=>{const d=e.data||{};if(d.ehhub==='lang'&&(d.lang==='ar'||d.lang==='en'))setLang(d.lang);if(d.ehhub==='theme')setDark(d.theme==='dark')});
if(window!==window.parent||/embedded=1/.test(location.search))document.body.classList.add('embedded');
['f-rel','f-status','f-line','f-agency','f-tier','f-cat','f-type','f-from','f-to'].forEach(id=>$(id).addEventListener('change',e=>{F[{'f-rel':'rel','f-status':'status','f-line':'line','f-agency':'agency','f-tier':'tier','f-cat':'cat','f-type':'type','f-from':'from','f-to':'to'}[id]]=e.target.value;render()}));
$('f-q').addEventListener('input',e=>{F.q=e.target.value.trim();render()});
$('f-pri').addEventListener('change',e=>{F.pri=e.target.checked;render()});
$('f-reset').onclick=()=>{Object.assign(F,{q:'',rel:'rel',status:'open',line:'',agency:'',tier:'',cat:'',type:'',from:'',to:'',pri:false});['f-q','f-from','f-to','f-line','f-agency','f-tier','f-cat','f-type'].forEach(i=>$(i).value='');$('f-pri').checked=false;render()};
document.addEventListener('click',e=>{const b=e.target.closest('.copy');if(b){navigator.clipboard&&navigator.clipboard.writeText(b.dataset.ref);b.textContent='✓';setTimeout(()=>b.textContent='⧉',1200)}const p=e.target.closest('.png');if(p)exportPNG(p.dataset.c,p.dataset.n)});
document.querySelectorAll('.tog.lang button').forEach(b=>b.onclick=()=>setLang(b.dataset.l));
document.querySelectorAll('.tog.th button').forEach(b=>b.onclick=()=>setDark(b.dataset.t==='dark'));
try{if((localStorage.getItem('ehhub.theme')||'light')==='dark'){document.body.classList.add('dark');document.querySelectorAll('.tog.th button').forEach(b=>b.classList.toggle('on',b.dataset.t==='dark'))}}catch(e){}
setLang(LANG);
"""

def T(en, ar, tag='span', cls=''):
    return f'<{tag}{" class=" + chr(34) + cls + chr(34) if cls else ""} data-en="{en}" data-ar="{ar}">{en}</{tag}>'

def png(cid, name):
    return f'<button class="png" data-c="{cid}" data-n="{name}" data-en="Export PNG" data-ar="تصدير PNG">Export PNG</button>'

HTML = f"""<!doctype html>
<html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Government Tenders (Etimad)</title>
<link rel="stylesheet" href="eh-shared.css">
<style>{CSS}{AV.CSS}</style></head>
<body>
<header><div><h1 data-en="Government Tenders (Etimad)" data-ar="المنافسات الحكومية (اعتماد)">Government Tenders (Etimad)</h1>
<div class="sub" data-en="Public tenders on Etimad, sorted by what Environmental Horizons (EH) can bid for, and linked to the stakeholder map and the bid tracker." data-ar="منافسات اعتماد العامة مصنفة حسب ما يمكن لآفاق البيئة التقدم له، ومربوطة بخريطة أصحاب المصلحة وجدول متابعة المنافسات.">Public tenders on Etimad, sorted by what Environmental Horizons (EH) can bid for, and linked to the stakeholder map and the bid tracker.</div></div>
<div class="ctl"><div class="tog lang"><button data-l="en" class="on">EN</button><button data-l="ar">عربي</button></div><div class="tog th"><button data-t="light" class="on">☀</button><button data-t="dark">☾</button></div></div></header>
<main>
<div class="stamp"><span id="cap" class="cap"></span>
{T("Source: Etimad public tender listing, read once a week (Sunday). Titles and agency names are shown exactly as published.","المصدر: قائمة المنافسات العامة في منصة اعتماد، تُقرأ أسبوعيًا (الأحد). العناوين وأسماء الجهات كما نُشرت تمامًا.")}</div>
<div class="gapnote">{T("Known gap: direct purchases can open and close within 3–15 days, between two Sunday captures, so some are missed. Public tenders (usually 14–30 days) are caught with time to study. To open a tender on Etimad, copy its reference number into Etimad's search.","فجوة معروفة: قد يُطرح الشراء المباشر ويُغلق خلال 3–15 يومًا بين التقاطين، فيفوت بعضه. أما المنافسات العامة (14–30 يومًا عادةً) فتُلتقط في وقت يسمح بدراستها. لفتح منافسة في اعتماد انسخ رقمها المرجعي وابحث به في المنصة.")}</div>
<div class="klab" data-en="Etimad market" data-ar="سوق اعتماد">Etimad market</div><div class="kstrip" id="kpism"></div>
<div class="klab" data-en="For EH" data-ar="لآفاق البيئة">For EH</div><div class="kstrip" id="kpis"></div>
<div class="filters">
<input id="f-q" type="search" data-ph-en="Search title, agency or reference" data-ph-ar="ابحث في العنوان أو الجهة أو الرقم المرجعي">
<select id="f-rel"></select><select id="f-status"></select><select id="f-line"></select><select id="f-agency"></select>
<select id="f-tier"></select><select id="f-cat"></select><select id="f-type"></select>
<select disabled title="Region is not captured yet · المنطقة غير ملتقطة بعد"><option data-en="Region: not captured yet" data-ar="المنطقة: غير ملتقطة بعد">Region: not captured yet</option></select>
<label><span data-en="Published from" data-ar="نُشرت من">Published from</span> <input id="f-from" type="date"></label>
<label><span data-en="to" data-ar="إلى">to</span> <input id="f-to" type="date"></label>
<label><input id="f-pri" type="checkbox"> <span data-en="Priority only" data-ar="ذات الأولوية فقط">Priority only</span></label>
<button id="f-reset" class="reset" data-en="Reset" data-ar="إعادة ضبط">Reset</button><span id="cnt" class="cnt"></span></div>

<section class="card"><div class="hd"><h2 data-en="Tenders" data-ar="المنافسات">Tenders</h2></div>
<div class="note" data-en="Default view: relevant tenders that are still open, soonest deadline first. Click a column to sort. Hover a relevance tag to see the term that matched; hover ★ to see why a tender is Priority." data-ar="العرض الافتراضي: المنافسات ذات الصلة المفتوحة، الأقرب موعدًا أولًا. انقر عنوان العمود للترتيب. مرّر المؤشر على وسم الصلة لرؤية العبارة المطابقة، وعلى ★ لمعرفة سبب الأولوية.">Default view: relevant tenders that are still open, soonest deadline first.</div>
<div class="tw" id="list"></div></section>

<section class="card"><h2 data-en="Where the market is going — relevant to EH" data-ar="إلى أين يتجه السوق — ما يخص آفاق البيئة">Where the market is going — relevant to EH</h2>
<div class="note" data-en="Charts follow the filters above but include closed tenders, so they show the market rather than only what is open today." data-ar="تتبع الرسوم المرشحات أعلاه لكنها تشمل المنافسات المغلقة، لتعرض السوق لا ما هو مفتوح اليوم فقط.">Charts follow the filters above but include closed tenders.</div>
<div class="legend"><span><i style="background:var(--core)"></i><span data-en="Core" data-ar="أساسي">Core</span></span><span><i style="background:var(--adj)"></i><span data-en="Adjacent" data-ar="مجاور">Adjacent</span></span></div>
<div class="g2"><div><div class="hd"><b data-en="Relevant tenders by month published" data-ar="المنافسات ذات الصلة حسب شهر النشر">Relevant tenders by month published</b>{png('ch-month','etimad_by_month')}</div><div id="ch-month"></div><div id="mcov" style="font-size:11.5px;color:var(--muted)"></div></div>
<div><div class="hd"><b data-en="By service line" data-ar="حسب خط الخدمة">By service line</b>{png('ch-line','etimad_by_service_line')}</div><div id="ch-line"></div></div>
<div><div class="hd"><b data-en="By tender type" data-ar="حسب نوع المنافسة">By tender type</b>{png('ch-type','etimad_by_type')}</div><div id="ch-type"></div></div>
<div><div class="hd"><b data-en="By region" data-ar="حسب المنطقة">By region</b></div><div id="ch-region"></div></div></div>
<div class="g2" style="margin-top:14px"><div><b data-en="Share of the whole Etimad market" data-ar="الحصة من سوق اعتماد كاملًا">Share of the whole Etimad market</b><p id="share" style="font-size:13px"></p>
<b data-en="Fastest-growing and shrinking service lines" data-ar="أسرع خطوط الخدمة نموًا وتراجعًا">Fastest-growing and shrinking service lines</b><div id="growth" style="margin-top:6px"></div></div>
<div><b data-en="What this means for EH" data-ar="ماذا يعني هذا لآفاق البيئة">What this means for EH</b><div id="notes" style="margin-top:6px"></div></div></div></section>

<section class="card"><h2 data-en="Where the market is going — all Etimad tenders" data-ar="إلى أين يتجه السوق — كل منافسات اعتماد">Where the market is going — all Etimad tenders</h2>
<div class="note" id="mkt-note"></div>
<div class="legend"><span><i style="background:var(--core)"></i><span data-en="Open at capture" data-ar="مفتوحة عند الالتقاط">Open at capture</span></span><span><i style="background:var(--adj)"></i><span data-en="Already closed" data-ar="مغلقة">Already closed</span></span></div>
<div class="g2"><div><div class="hd"><b data-en="By sector (Etimad activity, grouped)" data-ar="حسب القطاع (نشاط اعتماد مجمّعًا)">By sector</b>{png('mk-sector','etimad_market_by_sector')}</div><div id="mk-sector"></div></div>
<div><div class="hd"><b data-en="Who is buying (largest agencies, grouped)" data-ar="من يشتري (أكبر الجهات مجمّعة)">Who is buying</b>{png('mk-group','etimad_market_by_buyer')}</div><div id="mk-group"></div></div>
<div><div class="hd"><b data-en="Tenders published per day" data-ar="المنافسات المنشورة يوميًا">Tenders published per day</b>{png('mk-day','etimad_market_per_day')}</div><div id="mk-day"></div></div>
<div><div class="hd"><b data-en="Top 15 agencies" data-ar="أعلى 15 جهة">Top 15 agencies</b>{png('mk-agency','etimad_market_top_agencies')}</div><div id="mk-agency"></div></div></div>
<div class="g2" style="margin-top:14px"><div><b data-en="By tender type" data-ar="حسب نوع المنافسة">By tender type</b><div id="mk-type" style="margin-top:6px"></div>
<b style="display:block;margin-top:12px" data-en="What the Kingdom is expanding" data-ar="ما الذي تتوسع فيه المملكة">What the Kingdom is expanding</b><div id="mk-trend" style="margin-top:6px"></div></div>
<div><b data-en="What the Kingdom is buying now" data-ar="ما الذي تشتريه المملكة الآن">What the Kingdom is buying now</b><div id="mk-notes" style="margin-top:6px"></div></div></div></section>

<section class="card"><h2 data-en="Biggest requesters" data-ar="أكبر الجهات الطارحة">Biggest requesters</h2>
<div class="note" data-en="Agencies ranked by relevant tenders. Document fees are the price of the tender documents — a rough sign of size, never the contract value." data-ar="الجهات مرتبة حسب المنافسات ذات الصلة. قيمة الكراسة هي ثمن وثائق المنافسة — مؤشر تقريبي للحجم وليست قيمة العقد.">Agencies ranked by relevant tenders.</div>
<div class="g2"><div><div class="hd"><b data-en="Top 10 agencies" data-ar="أعلى 10 جهات">Top 10 agencies</b>{png('ch-agency','etimad_top_agencies')}</div><div id="ch-agency"></div></div>
<div><b data-en="New issuers (last 6 months)" data-ar="جهات جديدة (آخر 6 أشهر)">New issuers (last 6 months)</b><div id="newiss" style="margin-top:6px"></div></div></div>
<div class="tw" id="agtable" style="margin-top:12px;max-height:420px"></div></section>

<section class="card"><h2 data-en="Tenders of value or distinction" data-ar="منافسات ذات قيمة أو تميز">Tenders of value or distinction</h2>
<div class="note" data-en="Priority = the agency is Tier 1 or Government on the stakeholder map, an EH client, a regulator, or a giga-project / PIF entity." data-ar="الأولوية = الجهة من الفئة الأولى أو حكومية في الخريطة، أو عميل لآفاق، أو جهة تنظيمية، أو مشروع كبير / جهة تابعة لصندوق الاستثمارات العامة.">Priority definition</div>
<div class="g2"><div><b data-en="Open Priority tenders" data-ar="منافسات الأولوية المفتوحة">Open Priority tenders</b><div class="tw" id="pri-open" style="margin-top:6px;max-height:420px"></div></div>
<div><b data-en="Past Priority tenders and their outcome" data-ar="منافسات الأولوية السابقة ونتيجتها">Past Priority tenders and their outcome</b><div class="tw" id="pri-past" style="margin-top:6px;max-height:420px"></div></div></div></section>

<section class="card"><h2 data-en="Stakeholder view" data-ar="منظور أصحاب المصلحة">Stakeholder view</h2>
<div class="note" data-en="Agencies that issue relevant tenders but are not EH clients — where EH could grow. Agencies not on the map are listed for review and are never added automatically." data-ar="جهات تطرح منافسات ذات صلة وليست من عملاء آفاق — مجالات نمو محتملة. الجهات غير الموجودة في الخريطة تُعرض للمراجعة ولا تُضاف تلقائيًا.">Whitespace</div>
<div class="tw" id="white" style="max-height:420px"></div>
<div style="margin-top:12px"><b data-en="Winners of awarded tenders" data-ar="الفائزون بالمنافسات المرساة">Winners of awarded tenders</b>
<div class="empty" style="margin-top:6px" data-en="Etimad shows every bidder, their price and the winner on each awarded tender's page. These results are not captured yet, so no competitor is added from this tab; the competitor count stays the bid tracker's." data-ar="تعرض منصة اعتماد في صفحة كل منافسة مرساة جميع المتقدمين وأسعارهم والفائز. لم تُلتقط هذه النتائج بعد، لذا لا يُضاف أي منافس من هذه الصفحة، ويبقى عدد المنافسين كما في جدول المنافسات.">Not captured yet.</div></div></section>

{AV.HTML}
<div class="foot" data-en="Built from the private EH Etimad data sheet. Relevance rules: EH service taxonomy (14 service lines). EH status comes from the bid tracker, which stays the reference whenever the two differ." data-ar="مبنية من ورقة بيانات اعتماد الخاصة بآفاق البيئة. قواعد الصلة: تصنيف خدمات آفاق (14 خط خدمة). حالة آفاق مأخوذة من جدول متابعة المنافسات، وهو المرجع عند أي اختلاف.">Built from the private EH Etimad data sheet.</div>
</main><div id="tip"></div>
<script id="ET" type="application/json">{payload}</script>
<script>{JS}{AV.JS}</script>
</body></html>"""

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(HTML)
print(f'Etimad page → {OUT} ({len(HTML)//1024} KB, {len(D["tenders"])} tenders)')
