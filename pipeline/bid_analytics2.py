import json, collections, statistics as st
raw=json.load(open('bidraw2.json')); bids=raw['bids']; rosters=raw['rosters']
EH=['افاق البيئة','آفاق البيئة','افاق البيئه','آفاق البيئه','environmental horizon']
def is_eh(s): s=str(s or '').lower(); return any(t in s for t in EH)
def wr(won,aw): return round(100*won/aw) if aw else None

# ---------- KPIs ----------
awarded=[b for b in bids if b['decided']]
val=lambda B:[b['offer'] for b in B if b['offer']]
kpi=dict(
 total=len(bids), with_value=len(val(bids)), pipeline=round(sum(val(bids))),
 awarded=len(awarded), eh_won=sum(1 for b in awarded if b['eh_won']),
 win_rate=wr(sum(1 for b in awarded if b['eh_won']), len(awarded)),
 submitted=sum(1 for b in bids if b['offer']),
 competitors=len(json.load(open('competitors_rebuilt.json'))),
 clients=len(set(b['client'] for b in bids if b['client'])),
 platforms=len(set(b['platform'] for b in bids if b['platform'])),
 avg_bidders=round(st.mean([b['nbid'] for b in bids if b['nbid']]),1),
 max_bidders=int(max((b['nbid'] for b in bids if b['nbid']),default=0)),
 committee_accept=sum(1 for b in bids if 'accept' in b['committee'].lower()),
 committee_total=sum(1 for b in bids if b['committee']),
 avg_value=round(st.mean(val(bids))) if val(bids) else 0,
 median_value=round(st.median(val(bids))) if val(bids) else 0,
 total_guarantee=round(sum(b['bankval'] for b in bids if b['bankval'])),
)

# ---------- TIMELINE (monthly) ----------
months=sorted(set(b['month'] for b in bids if b['month']))
tl=[]
for mo in months:
    mb=[b for b in bids if b['month']==mo]
    maw=[b for b in mb if b['decided']]
    tl.append(dict(month=mo, launched=len(mb), value=round(sum(val(mb))),
        awarded=len(maw), won=sum(1 for b in maw if b['eh_won'])))
# submission months
smonths=sorted(set(b['submonth'] for b in bids if b['submonth']))
sub_tl=[dict(month=mo, submitted=sum(1 for b in bids if b['submonth']==mo)) for mo in smonths]

# ---------- WIN / LOSS / PIPELINE ----------
winloss=dict(
 awarded_eh=sum(1 for b in awarded if b['eh_won']),
 awarded_other=sum(1 for b in awarded if not b['eh_won']),
 not_awarded=sum(1 for b in bids if b['status']=='Not awarded'),
 cancelled=sum(1 for b in bids if b['status']=='Cancelled'),
 in_progress=sum(1 for b in bids if b['status']=='In progress'),
 no_status=sum(1 for b in bids if not b['status']),
)

# ---------- TRAJECTORY 2025 vs 2026 ----------
traj={}
for y in (2025,2026):
    yb=[b for b in bids if b['year']==y]; ya=[b for b in yb if b['decided']]
    traj[y]=dict(bids=len(yb), pipeline=round(sum(val(yb))),
        awarded=len(ya), eh_won=sum(1 for b in ya if b['eh_won']),
        win_rate=wr(sum(1 for b in ya if b['eh_won']),len(ya)),
        avg_bidders=round(st.mean([b['nbid'] for b in yb if b['nbid']]),1) if any(b['nbid'] for b in yb) else 0,
        submitted=sum(1 for b in yb if b['offer']),
        accept=sum(1 for b in yb if 'accept' in b['committee'].lower()),
        committee=sum(1 for b in yb if b['committee']))

# ---------- SERVICE MIX ----------
SVCN={'Env. Study Dep.':'Environmental Studies / EIA','Env. Service Dep.':'Environmental Services','Training Center':'Training'}
svc=collections.defaultdict(lambda:{'count':0,'value':0.0,'won':0,'awarded':0})
for b in bids:
    key=SVCN.get(b['svcdept'], b['svcdept'] or 'Unclassified')
    s=svc[key]; s['count']+=1
    if b['offer']: s['value']+=b['offer']
    if b['decided']: s['awarded']+=1; s['won']+=1 if b['eh_won'] else 0
service_mix=sorted([dict(name=k,count=v['count'],value=round(v['value']),won=v['won'],awarded=v['awarded'],win_rate=wr(v['won'],v['awarded'])) for k,v in svc.items()], key=lambda x:-x['count'])

# ---------- PLATFORM MIX ----------
def platnorm(p):
    pl=p.lower()
    if 'etimad' in pl: return 'Etimad'
    if 'ariba' in pl: return 'SAP Ariba'
    if 'sec' in pl: return 'SEC-SAP'
    if 'email' in pl or 'mail' in pl: return 'Email / direct'
    if not p: return 'Other'
    return 'Other / client portal'
plat=collections.defaultdict(lambda:{'count':0,'value':0.0,'won':0,'awarded':0})
for b in bids:
    if not b['platform']: continue
    p=plat[platnorm(b['platform'])]; p['count']+=1
    if b['offer']: p['value']+=b['offer']
    if b['decided']: p['awarded']+=1; p['won']+=1 if b['eh_won'] else 0
platform_mix=sorted([dict(name=k,count=v['count'],value=round(v['value']),won=v['won'],awarded=v['awarded'],win_rate=wr(v['won'],v['awarded'])) for k,v in plat.items()], key=lambda x:-x['count'])

# ---------- DURATION ----------
durs=[b['dur'] for b in bids if b['dur']]
dur_bands=[('≤3 mo',0,3),('4–6 mo',4,6),('7–12 mo',7,12),('13–24 mo',13,24),('25+ mo',25,999)]
duration=[]
for lbl,lo,hi in dur_bands:
    bb=[b for b in bids if b['dur'] and lo<=b['dur']<=hi]
    duration.append(dict(band=lbl,count=len(bb),value=round(sum(val(bb)))))
dur_stats=dict(median=round(st.median(durs)) if durs else 0, mean=round(st.mean(durs),1) if durs else 0, max=int(max(durs)) if durs else 0)

# ---------- QUALIFICATION FUNNEL (internal dept approvals) ----------
deps=['ceo','fin','tech','bd','pm','admin','legal']
funnel=dict(total=len(bids))
for d in deps: funnel[d]=sum(1 for b in bids if b['appr'][d])
funnel['submitted']=sum(1 for b in bids if b['offer'])
funnel['committee_accept']=kpi['committee_accept']

# ---------- COMMITTEE / DISCOUNT ----------
committee=dict(accept=kpi['committee_accept'], reject=sum(1 for b in bids if 'reject' in b['committee'].lower()))
discount=dict(requested=sum(1 for b in bids if b['discount'].lower() in ('yes','نعم')), not_req=sum(1 for b in bids if b['discount'].lower() in ('no','لا')))

# ---------- VALUE BANDS ----------
vbands=[('< 1M',0,1e6),('1–5M',1e6,5e6),('5–20M',5e6,20e6),('20–50M',20e6,50e6),('50M+',50e6,1e12)]
value_bands=[]
for lbl,lo,hi in vbands:
    bb=[b for b in bids if b['offer'] and lo<=b['offer']<hi]
    aw=[b for b in bb if b['decided']]
    value_bands.append(dict(band=lbl,count=len(bb),value=round(sum(val(bb))),awarded=len(aw),won=sum(1 for b in aw if b['eh_won'])))

# ---------- BIDDER CONCENTRATION ----------
bd_dist=collections.defaultdict(lambda:{'count':0,'won':0,'awarded':0})
for b in bids:
    if not b['nbid']: continue
    n=int(b['nbid']); key=n if n<=10 else 11
    d=bd_dist[key]; d['count']+=1
    if b['decided']: d['awarded']+=1; d['won']+=1 if b['eh_won'] else 0
bidder_dist=[dict(n=('10+' if k==11 else str(k)), count=v['count'], won=v['won'], awarded=v['awarded']) for k,v in sorted(bd_dist.items())]

# ---------- PRICING POSITIONING (full bidder breakdown, robust parser) ----------
rfull=json.load(open('rosters_all.json'))
winner_canon=json.load(open('winner_canon.json'))
competitors_rebuilt=json.load(open('competitors_rebuilt.json'))
from parse_rosters import canon as _canon
import unicodedata as _u
def _na(x):
    t=_u.normalize('NFKC',str(x or '')).lower()
    for a,b in [('أ','ا'),('إ','ا'),('آ','ا'),('ة','ه'),('ى','ي'),('ـ','')]: t=t.replace(a,b)
    return t
price_rows=[]; ranks=[]; gaps=[]; cheapest_cnt=0; eh_priced=0
for key,bidders in rfull.items():
    yr,sn=key.split('-'); yr=int(yr); sn=int(sn)
    # bidders = [name, amt, dq, eh]
    valid=[(n,a,dq,e) for n,a,dq,e in bidders if a is not None and not dq]
    ehrow=next(((n,a) for n,a,dq,e in bidders if e and a is not None and not dq), None)
    if not ehrow or len(valid)<2: continue
    ehp=ehrow[1]; eh_priced+=1
    prices=sorted(a for n,a,dq,e in valid)
    rank=prices.index(ehp)+1; n=len(prices)
    lo=min(prices); hi=max(prices); avg=st.mean(prices)
    gap=round(100*(ehp-lo)/lo,1) if lo else 0
    if rank==1: cheapest_cnt+=1
    ranks.append(rank/n); gaps.append(gap)
    bb=next((b for b in bids if b['year']==yr and b['sn']==sn), None)
    # winner of THIS tender (actual recorded winner, not lowest)
    wc=winner_canon.get(key)   # '__EH__', a canon string, or None (pending)
    def _is_winner(nm,e):
        if wc=='__EH__': return bool(e)
        if wc: return _canon(nm)==wc
        return False
    has_winner = wc is not None
    # build full ranked bidder list (compliant by price asc, then DQ'd)
    comp=sorted(valid, key=lambda x:x[1])
    blist=[]
    for i,(nm,a,dq,e) in enumerate(comp):
        blist.append(dict(name=('Environmental Horizons (EH)' if e else nm), price=round(a), dq=False, eh=bool(e), rank=i+1, lowest=(i==0), won=_is_winner(nm,e)))
    for nm,a,dq,e in [x for x in bidders if x[2]]:  # DQ'd bidders (no price)
        blist.append(dict(name=('Environmental Horizons (EH)' if e else nm), price=None, dq=True, eh=bool(e), rank=None, lowest=False, won=_is_winner(nm,e)))
    price_rows.append(dict(sn=sn,year=yr,eh=round(ehp),low=round(lo),high=round(hi),avg=round(avg),
        rank=rank,n=n,gap=gap,won=(bb['eh_won'] if bb else None), has_winner=has_winner,
        win_price=(round(bb['winval']) if (bb and bb.get('winval')) else None),
        title=(bb['title'] if bb else ''),client=(bb['client'] if bb else ''),
        bidders=blist, dq_count=sum(1 for x in bidders if x[2])))
price_rows.sort(key=lambda x:(x['year'],x['sn']))
pricing=dict(rows=price_rows, summary=dict(
    tenders=eh_priced, cheapest=cheapest_cnt, cheapest_pct=round(100*cheapest_cnt/eh_priced) if eh_priced else 0,
    avg_percentile=round(100*st.mean(ranks)) if ranks else 0, avg_gap=round(st.mean(gaps),1) if gaps else 0,
    median_gap=round(st.median(gaps),1) if gaps else 0,
    total_bidders=sum(len(r['bidders']) for r in price_rows)))

# ---------- CLIENTS (self-contained, with English aliases) ----------
import os as _os
client_aliases=json.load(open('client_aliases.json')) if _os.path.exists('client_aliases.json') else {}
def cl_name(raw): return client_aliases.get(raw.strip(), raw.strip())
cacc=collections.defaultdict(lambda:{'b25':0,'v25':0.0,'b26':0,'v26':0.0,'won':0,'aw':0})
for b in bids:
    if not b['client']: continue
    c=cacc[cl_name(b['client'])]
    if b['year']==2025: c['b25']+=1; c['v25']+=b['offer'] or 0
    else: c['b26']+=1; c['v26']+=b['offer'] or 0
    if b['decided']:
        c['aw']+=1
        if b['eh_won']: c['won']+=1
clients=[]
for nm,c in cacc.items():
    clients.append(dict(name=nm, bids=c['b25']+c['b26'], value=round(c['v25']+c['v26']),
        bids25=c['b25'], value25=round(c['v25']), bids26=c['b26'], value26=round(c['v26']),
        win_rate=(round(100*c['won']/c['aw']) if c['aw'] else None), eh_won=c['won'], awarded=c['aw'],
        lapsed=(c['b25']>0 and c['b26']==0), isnew=(c['b25']==0 and c['b26']>0)))
clients.sort(key=lambda x:-x['value'])

# ---------- WATCHLIST (self-contained, regenerated each run) ----------
watchlist=[]
for c in sorted(competitors_rebuilt, key=lambda x:-x['wins']):
    if c['wins']>0:
        watchlist.append(dict(sev='high', kind='Competitor beating EH', text=f"{c['name']} has won {c['wins']} tender(s) competing against EH across {c['encounters']} encounters."))
if traj[2025]['win_rate'] and traj[2026]['win_rate'] is not None and traj[2026]['win_rate']<traj[2025]['win_rate']:
    watchlist.append(dict(sev='high', kind='Win-rate decline', text=f"EH win rate fell from {traj[2025]['win_rate']}% (2025) to {traj[2026]['win_rate']}% (2026) — investigate pricing/technical scoring."))
for c in sorted(competitors_rebuilt, key=lambda x:-x['priced_vs']):
    if c['undercut_pct']==100 and c['priced_vs']>=3:
        watchlist.append(dict(sev='med', kind='Consistent undercutter', text=f"{c['name']} priced below EH in every shared priced tender ({c['priced_vs']} bids) — persistent price pressure."))
for c in clients:
    if c['lapsed'] and c['value25']>=1000000:
        watchlist.append(dict(sev='med', kind='Lapsed high-value client', text=f"{c['name']} sent tenders in 2025 (SAR {c['value25']:,}) but none in 2026 — re-engage."))
_sev={'high':0,'med':1,'low':2}
watchlist.sort(key=lambda x:_sev.get(x['sev'],3))
watchlist=watchlist[:18]

out=dict(kpi=kpi, timeline=tl, sub_timeline=sub_tl, winloss=winloss, trajectory=traj,
 service_mix=service_mix, platform_mix=platform_mix, duration=duration, dur_stats=dur_stats,
 funnel=funnel, committee=committee, discount=discount, value_bands=value_bands,
 bidder_dist=bidder_dist, pricing=pricing,
 competitors=competitors_rebuilt, clients=clients, watchlist=watchlist)

# ---------- TURNAROUND: launch -> submission deadline window ----------
import datetime as _dt
def _days(a,b):
    try: return (_dt.date.fromisoformat(b)-_dt.date.fromisoformat(a)).days
    except: return None
windows=[]
for b in bids:
    if b['launch'] and b['submit']:
        d=_days(b['launch'],b['submit'])
        if d is not None and 0<=d<=400: windows.append((d,b))
wd_bands=[('≤7 days',0,7),('8–14 days',8,14),('15–30 days',15,30),('31–45 days',31,45),('46+ days',46,400)]
turnaround_bands=[]
for lbl,lo,hi in wd_bands:
    bb=[b for d,b in windows if lo<=d<=hi]
    aw=[b for b in bb if b['decided']]
    turnaround_bands.append(dict(band=lbl,count=len(bb),awarded=len(aw),won=sum(1 for b in aw if b['eh_won'])))
dvals=[d for d,b in windows]
turnaround=dict(bands=turnaround_bands, n=len(windows),
    median=int(st.median(dvals)) if dvals else 0, mean=round(st.mean(dvals),1) if dvals else 0,
    minv=min(dvals) if dvals else 0, maxv=max(dvals) if dvals else 0,
    tight7=sum(1 for d in dvals if d<=7), tight14=sum(1 for d in dvals if d<=14))

# ---------- FULL BID LIST (readable, for list view) ----------
SVCN2={'Env. Study Dep.':'Env. Studies / EIA','Env. Service Dep.':'Env. Services','Training Center':'Training'}
def outcome(b):
    if b['eh_won']: return 'Won'
    if b['decided'] and not b['eh_won']: return 'Lost'
    if b['status']=='Not awarded': return 'Not awarded'
    if b['status']=='Cancelled': return 'Cancelled'
    return 'Pending'
bidlist=[]
for b in sorted(bids, key=lambda x:(x['year'], x['sn'])):
    win='EH' if b['eh_won'] else (b['winner'] if b['winner'] else '')
    bidlist.append(dict(year=b['year'], sn=b['sn'], date=b['launch'] or '',
        title=b['title'], client=b['client'], platform=b['platform'],
        value=round(b['offer']) if b['offer'] else None, nbid=int(b['nbid']) if b['nbid'] else None,
        svc=SVCN2.get(b['svcdept'],''), dur=int(b['dur']) if b['dur'] else None,
        winner=win, outcome=outcome(b),
        window=_days(b['launch'],b['submit']) if (b['launch'] and b['submit']) else None))

out['turnaround']=turnaround
out['bidlist']=bidlist

# ---------- REFUSED BIDS (why declined) ----------
def reason_cat(txt):
    t=txt.lower()
    if any(k in t for k in ['مشع','radioactive','ترخيص','license','licence','لم تحصل','تأهيل','qualif','رخصة']): return 'Missing licence / qualification'
    if any(k in t for k in ['brand','tailored','specific brand','مواصفات','علامة تجارية','sepcified','specified']): return 'Brand-locked specification'
    if any(k in t for k in ['دورات','تدريب','training']): return 'Service not offered / out of scope of company'
    if any(k in t for k in ['يفتقر','النضج','maturity','الميدانية']): return 'Vendor / partner risk'
    if any(k in t for k in ['نطاق','خارج','تخصص','specialization','scope','لا تتوافق','لا يعد','لا يُعد','عضوية','عامه','توظيف']): return 'Outside EH scope'
    return 'Other / not specified'
refused=[]
for b in bids:
    if 'reject' in b['committee'].lower() and b.get('comments'):
        refused.append(dict(year=b['year'], sn=b['sn'], title=b['title'][:75], client=b['client'][:40], reason=b['comments'], cat=reason_cat(b['comments'])))
refused.sort(key=lambda x:(x['year'],x['sn']))
refusal_cats=[{'cat':c,'n':n} for c,n in collections.Counter(r['cat'] for r in refused).most_common()]
out['refused']=refused
out['refusal_cats']=refusal_cats

json.dump(out, open('bidanalytics2.json','w'), ensure_ascii=False, indent=1)

print('KPIs:', {k:kpi[k] for k in ['total','pipeline','win_rate','awarded','eh_won','competitors','avg_bidders','committee_accept','committee_total']})
print('Timeline months:', len(tl), '|', months[0],'→',months[-1])
print('Service mix:', [(s['name'],s['count'],f"{s['win_rate']}%" if s['win_rate'] is not None else '-') for s in service_mix])
print('Platform mix:', [(p['name'],p['count']) for p in platform_mix])
print('Value bands:', [(v['band'],v['count']) for v in value_bands])
print('Pricing summary:', pricing['summary'])
print('Funnel:', funnel)
