# EH Bid Dashboard — Auto-update Kit

This folder makes the **EH Bid Analysis dashboard refresh itself every hour** from your live
Google Sheets, with no manual work.

## 👉 Start here: open **SETUP_GUIDE.md** and follow Parts A–D once (~45 min).

## What's in this folder
- **SETUP_GUIDE.md** — the step-by-step instructions (read this first).
- **pipeline/** — the program that builds the dashboard:
  - `fetch_from_sheets.py` — downloads your live Google Sheets.
  - `extract_bids2.py`, `parse_rosters.py`, `build_competitors.py`, `bid_analytics2.py` — the analysis.
  - `build_bid_dashboard.py`, `app.js`, `charts.js` — builds the HTML dashboard.
  - `client_aliases.json` — Arabic→English client name translations (you can add to this).
  - `licenses.json`, `logo_b64.txt` — supporting data and the EH logo.
  - `run_pipeline.py` — runs all of the above in order.
- **requirements.txt** — the libraries GitHub installs automatically.
- **.github/workflows/update-dashboard.yml** — the hourly schedule + publishing (runs on GitHub, free).

## What it does NOT change
Your Google Sheets are only ever **read**, never written to. The dashboard is rebuilt from a copy.

## Run it on your own computer (optional, for testing)
If you ever want to build it manually on a PC with Python installed:
```
pip install -r requirements.txt
cd pipeline
python run_pipeline.py
```
That produces `EH_Bid_Analysis.html` in the `pipeline` folder. (Needs the Google key set up as in the guide.)
