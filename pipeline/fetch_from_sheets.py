"""Downloads the live bid files from Google Drive as .xlsx (handles uploaded Excel files and native Sheets)."""
import os, io, sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive():
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'service_account.json')
    if not os.path.exists(cred_path):
        sys.exit('ERROR: robot key not found at ' + cred_path)
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def download(drive, file_id, out_name):
    meta = drive.files().get(fileId=file_id, fields='name,mimeType', supportsAllDrives=True).execute()
    mime = meta.get('mimeType', '')
    if mime == 'application/vnd.google-apps.spreadsheet':
        req = drive.files().export_media(fileId=file_id,
            mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        req = drive.files().get_media(fileId=file_id, supportsAllDrives=True)
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = dl.next_chunk()
    with open(out_name, 'wb') as f:
        f.write(buf.getvalue())
    print(f"  downloaded {out_name}  ({len(buf.getvalue())//1024} KB)  [{meta.get('name','')}]")

def main():
    drive = get_drive()
    targets = {}
    if os.environ.get('SHEET_ID_2025'): targets[os.environ['SHEET_ID_2025']] = 'bids2025.xlsx'
    if os.environ.get('SHEET_ID_2026'): targets[os.environ['SHEET_ID_2026']] = 'bids2026.xlsx'
    if not targets:
        sys.exit('ERROR: set SHEET_ID_2025 and/or SHEET_ID_2026 repository variables.')
    for file_id, out_name in targets.items():
        download(drive, file_id, out_name)

if __name__ == '__main__':
    main()
