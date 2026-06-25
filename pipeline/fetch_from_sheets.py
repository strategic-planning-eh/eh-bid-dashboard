"""
Downloads the live Google Sheet(s) as .xlsx using their PUBLIC share links.
"""
import os, sys, urllib.request

def export_url(sheet_id):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

def download(sheet_id, out_name):
    url = export_url(sheet_id)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    if data[:2] != b'PK':
        sys.exit(f"ERROR: '{out_name}' did not download as a spreadsheet. Check the sheet is 'Anyone with the link can view' and the ID is correct.")
    with open(out_name, 'wb') as f:
        f.write(data)
    print(f"  downloaded {out_name}  ({len(data)//1024} KB)")

def main():
    targets = {}
    if os.environ.get('SHEET_ID_2025'): targets[os.environ['SHEET_ID_2025']] = 'bids2025.xlsx'
    if os.environ.get('SHEET_ID_2026'): targets[os.environ['SHEET_ID_2026']] = 'bids2026.xlsx'
    if not targets:
        sys.exit('ERROR: set SHEET_ID_2025 and/or SHEET_ID_2026 repository variables.')
    for sheet_id, out_name in targets.items():
        download(sheet_id, out_name)

if __name__ == '__main__':
    main()
