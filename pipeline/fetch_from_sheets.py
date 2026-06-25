"""
Downloads the live Google Sheet(s) as .xlsx so the rest of the pipeline can read them.
Reads configuration from environment variables (set by GitHub Actions):
  SHEET_ID_2025  - the ID of the 2025 bid-tracking Google Sheet
  SHEET_ID_2026  - the ID of the 2026 bid-tracking Google Sheet
  GOOGLE_APPLICATION_CREDENTIALS - path to the service-account JSON key file
The Sheet ID is the long code in the sheet's URL:
  https://docs.google.com/spreadsheets/d/THIS_LONG_CODE_IS_THE_ID/edit
"""
import os, io, sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def main():
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'service_account.json')
    if not os.path.exists(cred_path):
        sys.exit('ERROR: service-account key not found at ' + cred_path)
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    drive = build('drive', 'v3', credentials=creds)

    targets = {}
    if os.environ.get('SHEET_ID_2025'): targets[os.environ['SHEET_ID_2025']] = 'bids2025.xlsx'
    if os.environ.get('SHEET_ID_2026'): targets[os.environ['SHEET_ID_2026']] = 'bids2026.xlsx'
    if not targets:
        sys.exit('ERROR: set SHEET_ID_2025 and/or SHEET_ID_2026 environment variables.')

    for sheet_id, out_name in targets.items():
        req = drive.files().export_media(fileId=sheet_id, mimeType=XLSX)
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
        with open(out_name, 'wb') as f:
            f.write(buf.getvalue())
        print(f'  downloaded {out_name}  ({len(buf.getvalue())//1024} KB)')

if __name__ == '__main__':
    main()
