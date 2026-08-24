# notify_and_log.py — run AFTER bid_analytics2.py in the workflow.
# Diffs current tender fingerprints against the previously PUBLISHED state (fetched
# from the live site), writes state.json + changelog.json for the site build, and
# optionally emails a summary when SMTP secrets are configured.
# No secrets => silent skip of email; changelog still accumulates.
import json, os, sys, urllib.request, ssl
from datetime import datetime, timezone, timedelta

SITE = os.environ.get("SITE_URL", "https://strategic-planning-eh.github.io/eh-bid-dashboard")
KSA = timezone(timedelta(hours=3))
TODAY = datetime.now(KSA).strftime("%Y-%m-%d")
NOW = datetime.now(KSA).strftime("%Y-%m-%d %H:%M")

def fetch_json(url):
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(url, timeout=20, context=ctx) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None

A = json.load(open("bidanalytics2.json"))
bids = A["both"]["bidlist"]
prow = A["both"]["pricing"]["rows"]
th = {f"{b['year']}-{b['sn']}": "|".join(str(x) for x in [b.get("outcome"), b.get("status") or "", b.get("value") or 0, b.get("nbid") or 0, b.get("winner") or "", b.get("lossreason") or ""]) for b in bids}
ph = {f"{r['year']}-{r['sn']}": "|".join(str(x) for x in [r.get("n_priced"), r.get("rank"), r.get("won"), r.get("undisc_count")]) for r in prow}

prev = fetch_json(SITE + "/state.json") or {}
events = []
lbl = lambda k: "#%s/%s" % (k.split("-")[1], k.split("-")[0][2:])
binfo = {f"{b['year']}-{b['sn']}": b for b in bids}
if prev.get("t"):
    for k, v in th.items():
        b = binfo[k]
        if k not in prev["t"]:
            events.append({"d": TODAY, "type": "new", "ref": lbl(k),
                           "txt": "New tender: %s (%s)%s" % (str(b.get('title'))[:70], str(b.get('client'))[:40],
                                  " — SAR %s" % format(b['value'], ',.0f') if b.get('value') else "")})
        elif prev["t"][k] != v:
            was, now = prev["t"][k].split("|")[0], v.split("|")[0]
            if was != now and now in ("Won", "Lost", "Not awarded", "Cancelled"):
                events.append({"d": TODAY, "type": "decision", "ref": lbl(k),
                               "txt": "%s → %s%s" % (lbl(k), now, " (EH WIN)" if now == "Won" and b.get("eh_won") else "")})
            else:
                events.append({"d": TODAY, "type": "update", "ref": lbl(k), "txt": "%s updated" % lbl(k)})
    for k, v in ph.items():
        if k in th and prev.get("p") and (k not in prev["p"] or prev["p"][k] != v) and not any(e["ref"] == lbl(k) for e in events):
            events.append({"d": TODAY, "type": "pricing", "ref": lbl(k), "txt": "%s pricing/roster updated" % lbl(k)})

json.dump({"t": th, "p": ph, "when": NOW}, open("state.json", "w"), ensure_ascii=False)

log = fetch_json(SITE + "/changelog.json") or {"entries": []}
seen_today = {(e["d"], e["ref"], e["type"]) for e in log["entries"]}
fresh = [e for e in events if (e["d"], e["ref"], e["type"]) not in seen_today]
log["entries"] = (fresh + log["entries"])[:150]
log["updated"] = NOW
json.dump(log, open("changelog.json", "w"), ensure_ascii=False)
print("notify_and_log: %d change(s) detected, %d new logged, changelog=%d entries" % (len(events), len(fresh), len(log["entries"])))

# ---- optional email ----
H, U, P, TO = (os.environ.get(x, "") for x in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS", "MAIL_TO"))
if fresh and H and U and P and TO:
    try:
        import smtplib
        from email.mime.text import MIMEText
        body = "EH Bid Tracker — changes detected (%s KSA):\n\n" % NOW + "\n".join("• " + e["txt"] for e in fresh) + \
               "\n\nDashboard: %s/#bids" % SITE
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = "EH Bids: %d change(s) — %s" % (len(fresh), ", ".join(e["ref"] for e in fresh[:5]))
        msg["From"] = U
        msg["To"] = TO
        port = int(os.environ.get("SMTP_PORT", "587"))
        s = smtplib.SMTP(H, port, timeout=30)
        s.starttls()
        s.login(U, P)
        s.sendmail(U, [t.strip() for t in TO.split(",")], msg.as_string())
        s.quit()
        print("notify_and_log: email sent to", TO)
    except Exception as e:
        print("notify_and_log: email failed (non-fatal):", e)
elif fresh:
    print("notify_and_log: SMTP secrets not configured — email skipped")
