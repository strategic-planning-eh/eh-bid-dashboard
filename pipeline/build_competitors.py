import json, collections
from parse_rosters import norm_ar, canon, is_eh

def build(bids, rosters):
    bidx={(b['year'],b['sn']):b for b in bids}

    def toks(s): return set(t for t in canon(s).split() if len(t)>2)
    def match_winner(winner, bidders):
        """match master winner name to a roster bidder; return canon of matched bidder or None"""
        wt=toks(winner)
        if not wt: return None
        best=None; bestov=0
        for nm,a,dq,e in bidders:
            ov=len(wt & toks(nm))
            if ov>bestov: bestov=ov; best=nm
        return canon(best) if bestov>=2 else None

    # ----- winner per tender (ACTUAL winner, not lowest) -----
    winner_canon={}   # key -> canon of winning bidder (or 'EH')
    for key,bidders in rosters.items():
        yr,sn=key.split('-'); b=bidx.get((int(yr),int(sn)))
        if not b: continue
        if b['eh_won'] is True:        # status تمت الترسية OR winner column = EH
            winner_canon[key]='__EH__'
        elif b['winner']:              # a competitor's name recorded
            wc=match_winner(b['winner'], bidders)
            if wc: winner_canon[key]=wc
    json.dump(winner_canon, open('winner_canon.json','w'), ensure_ascii=False)

    # ----- competitor encounters (all rosters where EH present) -----
    comp=collections.defaultdict(lambda:{'enc':0,'wins':0,'dq':0,'under':0,'priced_vs':0,'prices':[],'names':collections.Counter()})
    for key,bidders in rosters.items():
        if not any(x[3] for x in bidders): continue   # EH must be present
        ehp=next((a for nm,a,dq,e in bidders if e and a and not dq), None)
        wc=winner_canon.get(key)
        for nm,a,dq,e in bidders:
            if e: continue   # skip EH itself
            c=canon(nm)
            if not c: continue
            d=comp[c]; d['enc']+=1; d['names'][nm.strip()]+=1
            if dq: d['dq']+=1
            if a: d['prices'].append(a)
            if wc and wc!='__EH__' and c==wc: d['wins']+=1
            if ehp and a and not dq:
                d['priced_vs']+=1
                if a<ehp: d['under']+=1
    import statistics as st
    from difflib import SequenceMatcher
    # ----- DEDUP: merge companies with >=85% similar names -----
    keys=sorted(comp.keys(), key=lambda k:-comp[k]['enc'])
    def dispname(k): return comp[k]['names'].most_common(1)[0][0]
    # strip leading org words + trailing generic boilerplate -> distinctive CORE
    GEN=set('شركه شرکه مؤسسه مكتب معهد مختبر للاستشارات الاستشارات البيئيه الهندسيه المهنيه للخدمات الخدمات للمقاولات المقاولات المحدوده محدوده شخص واحد التجاريه للتجاره العامه الفنيه والمقاولات والاستشارات المتخصصه الوطنيه السعوديه للتدريب ذات مسؤوليه شركه و للاتصالات الاتصالات تقنيه المعلومات الرقميه رقميه نظم حلول تقنيات وتقنيه والاتصالات for environmental consulting services engineering company co ltd est the and communications technology information digital solutions systems'.split())
    def core(name):
        t=canon(name)
        toks=[w for w in t.split() if w not in GEN and len(w)>1]
        return ' '.join(toks)
    def sim(a,b):
        ca,cb=core(a),core(b)
        if len(ca)<2 or len(cb)<2: return 0
        # require token overlap of distinctive words AND high string similarity of cores
        ta,tb=set(ca.split()),set(cb.split())
        if not (ta & tb): return 0
        return SequenceMatcher(None, ca, cb).ratio()
    merged_into={}
    groups=[]
    for k in keys:
        if k in merged_into: continue
        grp=[k]; dn=dispname(k)
        for k2 in keys:
            if k2==k or k2 in merged_into: continue
            if sim(dn, dispname(k2))>=0.85:
                merged_into[k2]=k; grp.append(k2)
        groups.append(grp)
    # ----- ALIAS FOLD (tracker is law, 14 Sep 2026): two roster spellings that pipeline/aliases.csv bridges to the same
    #       stakeholder-map record are one company. Folding them here keeps the Bid & Tender count, the map count and the
    #       stamp identical; the pairs are written to roster_duplicates.json so the spelling can be corrected in the sheet.
    import csv, os, re, unicodedata
    def _anorm(s):
        s=unicodedata.normalize('NFKC', str(s or '')); s=re.sub(r'[\u0640\u200b-\u200d\ufeff\u064b-\u0652]', '', s)
        s=re.sub(r'[إأآا]', 'ا', s).replace('ى','ي').replace('ة','ه').replace('ؤ','و').replace('ئ','ي')
        return re.sub(r'\s+',' ', s).strip().casefold()
    _alias={}
    _ap=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aliases.csv')
    if os.path.exists(_ap):
        for r in csv.DictReader(open(_ap, encoding='utf-8-sig', newline='')):
            if str(r.get('status','')).strip().lower() in ('approved','reviewer'): _alias[_anorm(r['tracker_name'])]=_anorm(r['map_name'])
    def _target(grp):
        for k in grp:                                   # any spelling in the group with an approved bridge decides the target
            n=_anorm(dispname(k))
            if n in _alias: return _alias[n]
        return _anorm(dispname(grp[0]))
    _by_target=collections.OrderedDict(); roster_dups=[]
    for grp in groups:                                  # groups are in encounter order, so the most-seen spelling stays the base
        t=_target(grp)
        if t in _by_target:
            prev=_by_target[t]
            if _anorm(dispname(grp[0]))==t and _anorm(dispname(prev[0]))!=t: prev, grp = list(grp), prev   # the spelling that IS the record name is kept
            roster_dups.append({'kept': dispname(prev[0]), 'folded': [dispname(k) for k in grp], 'via_alias_target': t})
            _by_target[t]=prev+grp
        else: _by_target[t]=list(grp)
    groups=list(_by_target.values())
    json.dump(roster_dups, open('roster_duplicates.json','w'), ensure_ascii=False, indent=1)
    print('Alias-folded roster duplicates:', len(roster_dups))
    for d in roster_dups[:15]: print('  KEEP:', d['kept'][:40], '<- folded:', [x[:34] for x in d['folded']])
    mergelog=[]
    final={}
    for grp in groups:
        base=grp[0]; acc={'enc':0,'wins':0,'dq':0,'under':0,'priced_vs':0,'prices':[],'names':collections.Counter()}
        for k in grp:
            d=comp[k]
            acc['enc']+=d['enc']; acc['wins']+=d['wins']; acc['dq']+=d['dq']
            acc['under']+=d['under']; acc['priced_vs']+=d['priced_vs']; acc['prices']+=d['prices']
            acc['names'].update(d['names'])
        if len(grp)>1: mergelog.append([acc['names'].most_common(1)[0][0], [dispname(k) for k in grp[1:]]])
        acc['canons']=list(grp)          # every canon spelling folded into this competitor — used by bid_analytics2 to join winner_canon → value
        final[base]=acc
    print('Merged duplicate groups:', len(mergelog))
    for m in mergelog[:15]: print('  KEEP:', m[0][:40], '<- merged:', [x[:34] for x in m[1]])

    competitors=[]
    for c,d in final.items():
        disp=d['names'].most_common(1)[0][0]
        competitors.append(dict(
            name=disp, encounters=d['enc'], wins=d['wins'], dq=d['dq'],
            undercut=d['under'], priced_vs=d['priced_vs'],
            undercut_pct=round(100*d['under']/d['priced_vs']) if d['priced_vs'] else None,
            avg_price=round(st.mean(d['prices'])) if d['prices'] else None, canons=d.get('canons',[c])))
    competitors.sort(key=lambda x:(-x['encounters'],-x['wins']))
    return competitors, winner_canon

if __name__=='__main__':
    rosters=json.load(open('rosters_all.json'))
    raw=json.load(open('bidraw2.json')); bids=raw['bids']
    competitors, winner_canon = build(bids, rosters)
    json.dump(competitors, open('competitors_rebuilt.json','w'), ensure_ascii=False)

    print('Winners matched to roster bidder:', sum(1 for v in winner_canon.values() if v!='__EH__'), '| EH wins:', sum(1 for v in winner_canon.values() if v=='__EH__'))
    print('Total distinct competitors (all SMEs):', len(competitors))
    print('  recurring (>=2 encounters):', sum(1 for c in competitors if c['encounters']>=2))
    print('  one-off (1 encounter):', sum(1 for c in competitors if c['encounters']==1))
    print('\nTop 12 by encounters:')
    for c in competitors[:12]: print(f"  {c['encounters']}x enc, {c['wins']}w, undercut {c['undercut_pct']}% : {c['name'][:45]}")
    print('\nSample matched winners:')
    for k,v in list(winner_canon.items())[:8]:
        if v!='__EH__': print(f'  {k}: {v[:40]}')
