"""Runs the whole rebuild: fetch live data -> analyse -> produce EH_Bid_Analysis.html"""
import subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
STEPS = [
    ('Fetching latest data from Google Sheets', 'fetch_from_sheets.py'),
    ('Reading bids',                            'extract_bids2.py'),
    ('Parsing bidder rosters',                  'parse_rosters.py'),
    ('Analysing competitors',                   'build_competitors.py'),
    ('Computing analytics',                     'bid_analytics2.py'),
    ('Building the dashboard',                  'build_bid_dashboard.py'),
]
for label, script in STEPS:
    print(f'-> {label} ...')
    if subprocess.run([sys.executable, script]).returncode != 0:
        sys.exit(f'FAILED at {script}')
print('Done. EH_Bid_Analysis.html has been rebuilt.')
