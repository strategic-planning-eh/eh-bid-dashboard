#!/usr/bin/env python3
"""write_workbook_bidcols.py — makes the stakeholder workbook's bid columns pipeline-owned.

Rewrites, on the Stakeholders sheet, from competitors_feed.json + bid_sync_report.json (both written by sync_bids_to_apps.py):
    Bids vs EH        ← Yes only for companies the live tracker rosters name (else No)
    Bid Encounters    ← the roster count (else 0)
    Claimed bidder (unverified)  ← Yes for companies the workbook had flagged but the tracker does not name (new column, appended)
Every other cell, formula and sheet is left exactly as it was. Run after every sync, before the workbook is used as a build input.

Usage: python pipeline/write_workbook_bidcols.py --workbook EH_Stakeholder_Competitive_Map.xlsx --feed site/competitors_feed.json \
           --report site/bid_sync_report.json --out EH_Stakeholder_Competitive_Map.xlsx
"""
import argparse, json, re, unicodedata, datetime as dt, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

def norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = re.sub(r'[\u0640\u200b-\u200d\ufeff\u064b-\u0652]', '', s)
    s = re.sub(r'[إأآا]', 'ا', s).replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub(r'\s+', ' ', s).strip().casefold()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workbook', required=True); ap.add_argument('--feed', required=True); ap.add_argument('--report', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--sheet', default='Stakeholders')
    a = ap.parse_args()
    feed = json.load(open(a.feed, encoding='utf-8')); rep = json.load(open(a.report, encoding='utf-8'))
    bc = {norm(c['name']): c['bc'] for c in feed['competitors']}
    claimed = {norm(n) for n in rep.get('claimed_names', [])}
    wb = openpyxl.load_workbook(a.workbook); ws = wb[a.sheet]
    hdr = {str(c.value).strip(): c.column for c in ws[1] if c.value}
    cB, cE = hdr['Bids vs EH'], hdr['Bid Encounters']
    cC = hdr.get('Claimed bidder (unverified)')
    if not cC:
        cC = ws.max_column + 1; h = ws.cell(1, cC, 'Claimed bidder (unverified)')
        ref = ws.cell(1, cB); h.font = Font(name=ref.font.name, bold=ref.font.b, size=ref.font.sz, color=ref.font.color)
        h.fill = PatternFill(fill_type=ref.fill.fill_type, fgColor=ref.fill.fgColor) if ref.fill and ref.fill.fill_type else h.fill
        h.alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[h.column_letter].width = 14
    n_yes = n_claimed = n_changed = 0
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name: continue
        k = norm(name); before = (ws.cell(r, cB).value, ws.cell(r, cE).value)
        if k in bc:
            ws.cell(r, cB).value = 'Yes'; ws.cell(r, cE).value = bc[k]; ws.cell(r, cC).value = None; n_yes += 1
        else:
            ws.cell(r, cB).value = 'No'; ws.cell(r, cE).value = 0
            ws.cell(r, cC).value = 'Yes' if k in claimed else None; n_claimed += k in claimed
        if before != (ws.cell(r, cB).value, ws.cell(r, cE).value): n_changed += 1
    if 'Reclassification Log' in wb.sheetnames:
        lg = wb['Reclassification Log']; row = lg.max_row + 2
        lg.cell(row, 1, f"PIPELINE-OWNED BID COLUMNS ({dt.date.today():%d/%m/%Y})").font = Font(bold=True)
        lg.cell(row + 1, 1, f"Bids vs EH / Bid Encounters rewritten from the live bid tracker ({feed['stamp']}); {n_yes} bidders, {n_changed} rows changed. "
                            f"{n_claimed} former workbook flags moved to 'Claimed bidder (unverified)'. Do not edit these three columns by hand — write_workbook_bidcols.py regenerates them after every sync.")
    wb.save(a.out)
    print(f"{a.out}: {n_yes} tracker bidders, {n_claimed} claimed-unverified, {n_changed} rows changed · {feed['stamp']}")

if __name__ == '__main__': main()
