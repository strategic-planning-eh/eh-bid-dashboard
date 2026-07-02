# Auto-updating Bid Dashboard — Setup Guide

This kit makes your **EH Bid Analysis dashboard rebuild itself every hour** from your live
Google Sheets and publish to a web link. Once it's set up, you never touch it again — whenever
someone adds or edits a bid in the sheet, the dashboard catches up within the hour.

You do **not** need to know any coding. You'll mostly be clicking buttons and copying-and-pasting
a few codes. Set aside about **45 minutes** for the one-time setup. After that it's automatic and free.

---

## How it works (the 30-second version)

The dashboard is built by a small program (already written for you, in the `pipeline` folder).
We're going to put that program on a free service called **GitHub**, which will:

1. **Every hour**, quietly open your Google Sheets,
2. Re-run all the analysis (competitors, pricing, win/loss, refused bids, everything), and
3. Publish a fresh dashboard to a fixed web address.

Three things have to be arranged once: (A) give the program permission to read your sheets,
(B) put the program on GitHub, (C) tell it which sheets to read. Then (D) switch it on.

---

## Before you start — two free accounts

- A **Google account** (the one that owns the bid sheets).
- A **GitHub account** — make one free at https://github.com/signup if you don't have one.

---

## PART A — Give the program permission to read your sheets

Google won't let a program open your sheets without a special "robot account". You make one here.
(This is the fiddliest part. Go slowly; it's just clicking.)

1. Go to **https://console.cloud.google.com/** and sign in with your Google account.
2. At the very top, click the project dropdown → **New Project** → name it `EH Bid Dashboard` → **Create**.
   Wait a few seconds, then make sure that new project is selected in the top bar.
3. In the search bar at the top, type **Google Drive API**, click it, then click **Enable**.
   (The dashboard reads your sheets through the Drive service.)
4. In the search bar, type **Service Accounts** and open it. Click **+ Create Service Account**.
   - Name it `dashboard-robot` → **Create and Continue** → skip the optional steps → **Done**.
5. You'll see your new robot in the list, with an email like
   `dashboard-robot@eh-bid-dashboard.iam.gserviceaccount.com`. **Copy that email — you'll need it twice.**
6. Click the robot's email → the **Keys** tab → **Add Key → Create new key → JSON → Create**.
   A file downloads to your computer (something like `eh-bid-dashboard-xxxx.json`).
   **Keep this file safe — it's the robot's password. Don't email it or post it anywhere.**
7. Now **share your sheets with the robot**, exactly like sharing with a colleague:
   - Open your **2025** bid Google Sheet → click **Share** (top right) → paste the robot's email
     from step 5 → set it to **Viewer** → untick "Notify people" → **Share**.
   - Do the same for your **2026** sheet.

✅ Done with Google. The robot can now read those two sheets, and nothing else.

---

## PART B — Put the project on GitHub

1. Sign in at **https://github.com**. Click the **+** (top right) → **New repository**.
2. Name it `eh-bid-dashboard`. Choose **Private** (recommended — see the Privacy note at the end).
   Leave everything else as-is → **Create repository**.
3. On the new repo page, click **uploading an existing file** (the link in the middle).
4. Drag in **everything from this kit**: the `pipeline` folder, the `.github` folder, and
   `requirements.txt`. (If your computer hides the `.github` folder because of the dot, you can also
   create it via "Add file → Create new file" and type `.github/workflows/update-dashboard.yml`
   as the name, then paste the file's contents.)
5. Click **Commit changes** at the bottom.

✅ The program is now on GitHub.

---

## PART C — Tell it which sheets to read, and hand over the key

We give GitHub two harmless settings (the sheet IDs) and one secret (the robot's key file).

**Find your two Sheet IDs first.** Open each Google Sheet and look at its web address:
`https://docs.google.com/spreadsheets/d/`**`THIS_LONG_CODE`**`/edit` — the bold part is the ID.
Copy the ID from the 2025 sheet and the 2026 sheet.

1. In your GitHub repo, click **Settings** (top menu) → in the left sidebar,
   **Secrets and variables → Actions**.
2. Open the **Variables** tab → **New repository variable**:
   - Name: `SHEET_ID_2025`  → Value: paste the 2025 sheet's ID → **Add variable**.
   - **New repository variable** again → Name: `SHEET_ID_2026` → Value: the 2026 ID → **Add variable**.
3. Now the **Secrets** tab → **New repository secret**:
   - Name: `GOOGLE_CREDENTIALS`
   - Value: open the JSON key file you downloaded in Part A step 6 in **Notepad** (or TextEdit),
     select **all** the text, copy it, and paste the whole thing here → **Add secret**.

✅ It now knows what to read and how to log in.

---

## PART D — Switch it on

1. In the repo, click **Settings → Pages** (left sidebar). Under **Build and deployment → Source**,
   choose **GitHub Actions**. (This lets it publish the dashboard to a web link.)
2. Click the **Actions** tab (top menu). If it asks you to enable workflows, click the green button.
3. You'll see **"Update Bid Dashboard"** in the left list. Click it → **Run workflow → Run workflow**
   (this runs it once now instead of waiting for the next hour).
4. Wait ~1–2 minutes. A green tick means it worked. Click into the run → the **publish** step shows
   your dashboard's **web address**. Open it — that's your live dashboard. **Bookmark it and share it.**

🎉 **That's it.** From now on it refreshes every hour automatically. To check it's alive, the Actions
tab shows a new green tick every hour.

---

## How to know it's working / make changes

- **See it ran:** the **Actions** tab lists every hourly run with a green tick (or red if something broke).
- **Force an immediate refresh:** Actions tab → Update Bid Dashboard → **Run workflow**.
- **A new client shows in Arabic instead of English?** That's expected for clients not yet translated.
  Open `pipeline/client_aliases.json` in the repo, click the pencil ✏️ to edit, add a line like
  `"<arabic name>": "<English name>",` and commit. It'll use the English name on the next run.
  (Or just send me the new names and I'll add them.)

---

## ⚠️ Privacy note — please read

By default, GitHub Pages makes the dashboard a **public web link** (anyone who has the URL can open it),
even from a private repo. The URL is long and unlisted, so it won't show up in Google searches — but
it is technically reachable. Given the dashboard contains competitor pricing, decide what's acceptable:

- **Fine with an unlisted public link?** You're done — nothing to change.
- **Needs to be truly internal (login required)?** That needs a paid **GitHub Team/Enterprise** plan,
  which can restrict Pages to logged-in members of your organisation. Tell me and I'll adjust the setup,
  or your IT team can enable it.

---

## "I'd rather not do this myself"

Totally fine — this kit is self-contained, so you can hand the whole folder plus this guide to whoever
manages IT/systems at Environmental Horizons, and they can do Parts A–D in 30 minutes. Everything they
need is here. If you'd prefer a different host than GitHub (for example a more click-driven service, or
running it on a company server), tell me your preference and I'll provide that version instead.

---

## If something goes red (quick fixes)

- **Red X on the "Rebuild" step, mentions `service_account`** → the `GOOGLE_CREDENTIALS` secret wasn't
  pasted in full. Redo Part C step 3, pasting the entire JSON file contents.
- **Red X mentioning permission / 403** → the robot wasn't given access to a sheet. Redo Part A step 7
  (share both sheets with the robot's email as Viewer).
- **Runs green but numbers look stale** → make sure `SHEET_ID_2025` / `SHEET_ID_2026` point at the
  sheets you're actually editing (Part C).
- **Anything else** → send me the red error text from the Actions tab and I'll tell you the fix.
