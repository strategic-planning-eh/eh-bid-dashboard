# EH Hub — deploy package (06/09/2026)

## Contents
- `hub/` — the 8 app files (EH_Hub.html + 7 dashboards) and `hub/vendor/` (Chart.js, D3, Leaflet — local fallbacks when cdnjs is blocked).
- `update-dashboard.yml` — GitHub Actions workflow: publishes `hub/EH_Hub.html` as `site/index.html` and copies every dashboard alongside it.

## Deploy
1. Copy `hub/` into the repo root (replace the existing folder entirely — files were removed as well as changed).
2. Copy `update-dashboard.yml` into `.github/workflows/` (overwrite).
3. Commit & push. The workflow builds `site/` and publishes to GitHub Pages.
4. Hard-refresh on each device (Ctrl/Cmd+Shift+R; on iPhone: Safari → aA → Website Settings → clear, or open in a private tab). Files are served by plain filename with no cache-busting, so a normal refresh can show the old build.

## What this build contains
Company-type filter · v2 scoring + Phase 1a/1b research applied · 4,195 organizations (Al Mandariyah + Namaa/GESCO twins merged) · CONFIDENTIAL notice · bid 2026/#23 marked Won · exec year toggles + animated quadrant chart · full dark-mode fixes · mobile/tablet layout (bottom bar, filter drawer, tablet tiers) · iOS-in-iframe strategy · landscape-phone layout · bubble-map zoom controls.

## Not in this package (kept separate, confidential data)
`EH_Stakeholder_Competitive_Map.xlsx` and the research/audit reports live outside the public Pages repo.

## ⚠ Bid & Tender dashboard — two things the workflow does differently
1. **It does not publish `hub/EH_Bid_Analysis_CURRENT.html`.** Line 48 of the workflow publishes `pipeline/EH_Bid_Analysis.html`, which the pipeline regenerates every hour from the Google Sheets. Any fix made only to the HTML file is overwritten on the next run. This package therefore includes `pipeline/build_bid_dashboard.py` with every UI layer ported into the generator (dark-mode repairs, responsive/tablet/landscape rules, grid hardening, touch targets, iOS handling). **Copy it over `pipeline/build_bid_dashboard.py` in the repo.** The `hub/EH_Bid_Analysis_CURRENT.html` in this package is the same build and is safe to keep as the local fallback.
2. **Bid 2026 #23 ("Environmental Emergency Services at Saudi Energy Power Plants", SEC, SAR 15.34M) was marked Won in the HTML only.** The pipeline recomputes every KPI from the sheets, so on the next run it will revert to *Pending* unless the **source sheet row is updated** (outcome = Won, winner = Afaq Al-Biah / EH). Please make that edit in the 2026 sheet before or with this deploy.
