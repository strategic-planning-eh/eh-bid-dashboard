"""namecheck.py — one place that decides whether a tracker cell is a company name or a sentence about the tender.

Why: on 15 Sep 2026 the reason text "وجود عطاء مالي مقدم من منافس اخر" (typed into the winner column of bid 81/26)
was ingested as a competitor. Every path that turns a cell into a competitor name goes through is_reason_text():
extract_bids2.py (winner column), parse_rosters.py (roster tabs) and sync_bids_to_apps.py (adding companies to the map).
"""
import re, unicodedata

def _n(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200f\u064b-\u0652]', '', s)
    s = re.sub(r'[إأآ]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub(r'\s+', ' ', s).strip().lower()

# phrases that only occur in an award/rejection statement, never in a company name
REASON_PHRASES = [
    'وجود عطاء', 'عطاء مالي', 'عرض مالي', 'عرض سعر', 'سعر اقل', 'اقل سعر', 'اقل من العرض', 'اعلي من', 'منافس اخر', 'مقدم من منافس',
    'غير مقبول', 'غير مطابق', 'غير مستوف', 'عدم مطابق', 'عدم استيفاء', 'عدم وجود', 'عدم تقديم', 'لا يوجد', 'لم يتم', 'لم تتم', 'لم يستوف',
    'تم استبعاد', 'تم الاستبعاد', 'استبعاد العرض', 'تم رفض', 'رفض العرض', 'رفض عرض', 'سبب عدم', 'بسبب', 'نتيجه', 'تم الغاء', 'الغاء المنافسه',
    'التاهيل', 'الخبرات السابقه', 'شروط المنافسه', 'كراسه الشروط', 'التقييم الفني', 'التقييم المالي', 'النقاط', 'المستندات المطلوبه', 'انسحاب',
    'lowest price', 'lower price', 'lowest bid', 'not compliant', 'non-compliant', 'disqualified', 'rejected', 'another bidder', 'another competitor', 'not awarded',
]
COMPANY_MARKERS = ['شركه', 'مؤسسه', 'مكتب', 'معهد', 'مركز', 'مصنع', 'مجموعه', 'مختبر', 'مستودع', 'تحالف', 'فرع',
                   ' co', 'co.', 'ltd', 'llc', 'l.l.c', 'est', 'company', 'group', 'consult', 'inc', 'corp', 'engineering', 'services', 'solutions', 'trading', 'contracting']

_PHR = [_n(p) for p in REASON_PHRASES]
_MRK = [_n(m) if not m.startswith(' ') else ' ' + _n(m) for m in COMPANY_MARKERS]
# function words that carry a sentence, not a name: Arabic particles / English verbs and connectors
_FUNC = [_n(w) for w in ['من', 'في', 'علي', 'الي', 'ان', 'تم', 'لم', 'لا', 'غير', 'عدم', 'بسبب', 'هو', 'هي', 'كان', 'يوجد', 'حيث', 'الذي', 'التي', 'اذا', 'حتي', 'بعد', 'قبل']] + \
        ['is', 'was', 'were', 'has', 'have', 'due to', 'because', 'since', 'submitted', 'offer', 'bid', 'price', 'than', 'not']

def is_reason_text(s):
    """True when the cell reads like a statement about the tender (a reason, a verdict) rather than a company name."""
    t = _n(s)
    if not t: return False
    if any(p in t for p in _PHR): return True
    words = t.split()
    has_marker = any(m in t for m in _MRK)
    func = sum(1 for w in words if w in _FUNC)
    if len(words) >= 6 and not has_marker and func >= 2: return True    # long, no company word, carried by particles/verbs → a sentence
    return False

_TITLE_STARTS = [_n(w) for w in ['مشروع', 'اتفاقيه', 'عقد', 'منافسه', 'خدمات', 'خدمه', 'اعداد', 'تنفيذ', 'اجراء', 'توريد', 'صيانه', 'دراسه', 'تقييم', 'تشغيل', 'تاهيل', 'انشاء', 'تطوير', 'تركيب', 'ازاله', 'نقل', 'معالجه', 'التخلص', 'استخراج', 'تجديد', 'اصدار']]

def is_tender_title(s):
    """True when the cell is a scope/tender title (starts with a work noun and names no company)."""
    t = _n(s); w = t.split()
    return bool(w) and w[0] in _TITLE_STARTS and not any(m in t for m in _MRK)

def looks_like_company(s):
    t = _n(s)
    return bool(t) and 3 <= len(t) <= 120 and not is_reason_text(t) and not is_tender_title(t) and bool(re.search(r'[a-z\u0600-\u06ff]{3,}', t))
