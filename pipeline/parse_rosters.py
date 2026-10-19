import openpyxl, json, unicodedata, re, statistics
from namecheck import looks_like_company   # 15 Sep 2026: reasons and tender titles are not bidders

def norm_ar(s):
    s=unicodedata.normalize('NFKC', str(s or '')).lower()
    for a,b in [('أ','ا'),('إ','ا'),('آ','ا'),('ة','ه'),('ى','ي'),('ـ','')]: s=s.replace(a,b)
    return s
def canon(s):
    t=norm_ar(s); t=re.sub(r'[^\w\u0600-\u06FF ]',' ',t); return ' '.join(t.split())
def is_eh(s):
    t=norm_ar(s)
    if 'environmental horizon' in t or 'afaq' in t: return True
    return ('افاق' in t and 'بيئ' in t)
HDR_ROWS=60   # 19 Oct 2026 (bid 87/26): headers below row 12 were missed, so the notes column became the name column
def is_amt(v): return isinstance(v,(int,float)) and 1000<=v<1e11
DQ=['غير مطابق','مستبعد','لم يجتاز','غير متطابق','مستبعده','غير ﻣﻄﺎﺑﻖ']
def is_dq(v): return isinstance(v,str) and any(d in norm_ar(v) or d in str(v) for d in DQ)
HEADERW=['bidder name','اسم المورد','اسم الشركه','supplier','description','rfx','total amount','وصف','رقم','الرقم','remarks','status','date','اسم العارض','المورد','قيمه','الشركات','بيانات','م','no','sn','open','time','response','بند','اجمالي','vat','ضريبه','قائمه الموردين','تاريخ']
def clip_name(v):
    """A name cell over 90 characters (the name pasted twice, or a long legal suffix) is cut to one name (12 Oct 2026)."""
    t=re.sub(r'\s+',' ',str(v)).strip()
    if len(t)<=90: return t
    w=t.split()
    for i in range(2,len(w)-1):
        if w[i:i+2]==w[0:2] or w[i:i+2]==w[1:3]: return ' '.join(w[:i])      # second copy starts here
    out=''
    for x in w:
        if len(out)+len(x)+1>90: break
        out=(out+' '+x).strip()
    return out
LONG_OK=['شركه','مؤسسه','مكتب','مجموعه','مصنع','مركز','معهد','جامعه','company','the']   # a cut name must open like a firm
def is_name(v):
    if not isinstance(v,str): return False
    t=clip_name(v)
    if len(t)<6: return False
    if len(v.strip())>90 and (norm_ar(t).split() or [''])[0] not in LONG_OK: return False   # long titles stay out
    if is_amt(v): return False
    if not looks_like_company(t): return False
    cn=norm_ar(t)
    if cn in HEADERW or cn in ('م','no','sn'): return False
    for ph in ['الشركات الي قدمت','قائمه الموردين','الموردين المتقدمين','الموردين المرسى','المرسى عليه','تقديم خدمات','اعداد دراسه','تنفيذ اعمال','اجراء دراسه','قياس بيئي','عدد الشركات','الشركه الفائزه','تاريخ فتح','رقم المنافسه','تقرير فتح','فتح العروض','الموعد النهائي','تاريخ الترسيه']:
        if ph in cn: return False
    # reject project/service descriptions (start with these words, not company names)
    first=cn.split()[0] if cn.split() else ''
    if first in ['مشروع','خدمات','اعداد','تنفيذ','اجراء','توريد','صيانه','تطوير','دراسه','اعاده','تركيب','تقييم'] and 'شركه' not in cn and 'مؤسسه' not in cn:
        return False
    # must contain letters
    return bool(re.search(r'[A-Za-z\u0600-\u06FF]{3,}',t))

def parse(rs):
    maxr=min(rs.max_row,500); maxc=rs.max_column
    grid=[[rs.cell(r+1,c+1).value for c in range(maxc)] for r in range(maxr)]
    # name column: 1) header match ('Bidder Name'/'اسم المورد')  2) most name-like cells (excl description)
    DESC=['description','وصف','rfx','بيان المنافسه','specification']
    # 12 Oct 2026 (audit bids-07): award-report sheets (Bid#25, Bid#27) carry two bidder-name headers, the award table and the
    # applicant list; the column with the most company names is the roster.
    nc=None; hcols=[]
    for c in range(maxc):
        for r in range(min(HDR_ROWS,maxr)):
            h=norm_ar(grid[r][c])
            if any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','supplier','اسم العارض','المورد']) and not any(d in h for d in DESC):
                hcols.append(c); break
    if hcols:
        nc=max(hcols, key=lambda c:(sum(1 for row in grid if is_name(row[c])), -c))
    if nc is None:
        nscore={c:sum(1 for row in grid if is_name(row[c]) and not any(b in norm_ar(row[c]) for b in ['قيمه','total amount']+DESC)) for c in range(maxc)}
        NOTNAME=['ملاحظات','remarks','notes','رقم العرض','رقم العطاء','رقم المرجع','قيمه العرض','قيمه العطاء','النتيجه الفنيه','التقييم الفني']
        for c in list(nscore):
            for r in range(min(HDR_ROWS,maxr)):
                h=norm_ar(grid[r][c]).strip()
                if h and any(h==k or h.startswith(k) for k in NOTNAME): nscore[c]=0; break   # 19 Oct 2026
        # exclude columns whose header marks them as description
        for c in list(nscore):
            for r in range(min(HDR_ROWS,maxr)):
                if any(d in norm_ar(grid[r][c]) for d in DESC): nscore[c]=0; break
        if not nscore or max(nscore.values())<2: return None
        nc=max(nscore,key=nscore.get)
    # price column = header/spread heuristic (optional)
    cands=[]
    for c in range(maxc):
        hdr=' '.join(norm_ar(grid[r][c]) for r in range(min(HDR_ROWS,maxr)))
        if any(k in hdr for k in ['رقم العرض','رقم العطاء','رقم المرجع']): continue  # offer ID — never a price
        vals=[row[c] for row in grid if is_amt(row[c])]
        if len(vals)>=2:
            cands.append((c,len(vals),max(vals)/max(min(vals),1)))
    pc=None
    if cands:
        def hscore(c):
            for r in range(min(HDR_ROWS,maxr)):
                h=norm_ar(grid[r][c])
                if any(k in h for k in ['قيمه العرض','قيمه الترسيه','total amount','اجمالي','القيمه الماليه','amount','قيمه العطاء']): return 2
                if any(k in h for k in ['رقم','reference','no.','الرقم']): return -3
            return 0
        pc=max(cands, key=lambda x:(hscore(x[0])*10 + (5 if x[2]>1.5 else -2) + min(x[1],50)))[0]
    out=[]; seen=set()
    for row in grid:
        nm=row[nc]
        if not is_name(nm): continue
        nm=clip_name(nm)
        k=canon(nm)[:40]
        if k in seen or not k: continue
        pv=row[pc] if pc is not None else None
        dq=is_dq(pv) if pc is not None else False
        amt=float(pv) if is_amt(pv) else None
        seen.add(k); out.append([str(nm).strip(), amt, dq, is_eh(nm)])
    return out if len(out)>=2 else None

TECHH=['ملاحظات','الملاحظات','remarks','notes','note','النتيجه الفنيه','التقييم الفني','technical']
def tech_scores(rs):
    """Each bidder's technical result from the notes column, e.g. «حاصل على نسبة (87%)» → 87.0 (12 Oct 2026)."""
    maxr=min(rs.max_row,500); maxc=rs.max_column
    grid=[[rs.cell(r+1,c+1).value for c in range(maxc)] for r in range(maxr)]
    nc=tc=None
    for r in range(min(HDR_ROWS,maxr)):
        for c in range(maxc):
            h=norm_ar(grid[r][c]).strip()
            if nc is None and any(k in h for k in ['bidder name','اسم المورد','اسم الشركه','supplier','اسم العارض']): nc=c
            if tc is None and h and any(h==k or h.startswith(k) for k in TECHH): tc=c
    if nc is None or tc is None: return {}
    out={}
    for row in grid:
        nm,nt=row[nc],row[tc]
        if not is_name(nm) or nt is None: continue
        if isinstance(nt,(int,float)) and 0<nt<=1: sc=round(nt*100,1)            # a cell formatted as 87%
        else:
            m=re.search(r'(\d{1,3}(?:[.,]\d+)?)\s*[%٪]',str(nt))
            sc=float(m.group(1).replace(',','.')) if m else None
        if sc is not None and 0<=sc<=100: out[clip_name(nm)]=sc
    return out

if __name__=='__main__':
    allr={}; tech={}
    for f,yr in [('bids2025.xlsx',2025),('bids2026.xlsx',2026)]:
        wb=openpyxl.load_workbook(f, data_only=True)
        for sh in [s for s in wb.sheetnames if __import__('re').match(r'\s*bid\s*#\s*\d+\s*$', s, __import__('re').I)]:
            sn=__import__('re').match(r'\s*bid\s*#\s*(\d+)', sh, __import__('re').I).group(1)
            r=parse(wb[sh])
            if r: allr[f'{yr}-{sn}']=r
            ts=tech_scores(wb[sh])
            if ts: tech[f'{yr}-{sn}']=ts
    # corrections.json "rosters": bidder lists confirmed by the bid team, replacing what the Bid# sheet yields
    # (19 Oct 2026, bid 87/26). Rows: [name, value or null, note]. Enter the same table in the Drive sheet and it becomes a no-op.
    import os
    _cp=os.path.join(os.path.dirname(os.path.abspath(__file__)),'corrections.json')
    if os.path.exists(_cp):
        for key,rows in (json.load(open(_cp,encoding='utf-8')).get('rosters') or {}).items():
            allr[key]=[[clip_name(n), (float(v) if is_amt(v) else None), is_dq(nt), is_eh(n)] for n,v,nt in rows]
            _t={}
            for n,v,nt in rows:
                m=re.search(r'(\d{1,3}(?:[.,]\d+)?)\s*[%٪]',str(nt or ''))
                if m: _t[clip_name(n)]=float(m.group(1).replace(',','.'))
            if _t: tech[key]=_t
            print('corrections.json roster applied:',key,len(rows),'bidders')
    json.dump(allr, open('rosters_all.json','w'), ensure_ascii=False)
    json.dump(tech, open('techscores.json','w'), ensure_ascii=False)   # 12 Oct 2026: technical scores by tender and bidder
    print('Technical scores:', {k: len(v) for k, v in tech.items()} or 'none recorded')
    npriced=sum(1 for v in allr.values() if sum(1 for x in v if x[1]) >=2)
    eh_rosters=sum(1 for v in allr.values() if any(x[3] for x in v))
    print('Total rosters (incl names-only):',len(allr),'| with >=2 prices:',npriced,'| with EH present:',eh_rosters)
