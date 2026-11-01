# Part A — Data profile (Stage 1 gate)

Stakeholder Map × Bid Tracker analyst review · 1 Nov 2026 · scripts: `pipeline/analysis/profile_map.py` (outputs in `pipeline/analysis/out/`)

## 0. What was profiled, and what is still missing

| Input | Status | Used |
|---|---|---|
| Stakeholder data | **No v9 .xlsx in the repo.** The live map (`hub/EH_Stakeholder_Map_CURRENT.html`, commit of 1 Nov 2026 incl. FEAL Arabia) embeds the full dataset: **4,211 rows**, synced to "tracker as of 20 Oct 2026". Profiled as the v9-live source. | yes |
| Bid tracker extracts | Not in the repo (the hourly build pulls `bids2025.xlsx` / `bids2026.xlsx` from Drive). The only extract on hand is the one baked into `hub/EH_Bid_Analysis_CURRENT.html`: **182 tenders, 2026 up to SN 103 (Aug 2026)** — stale. The 2026 tracker attached to the project is v5 (151 rows, to 9 Sep) — also behind the 20 Oct sync the map carries. | partially (shape only) |
| Etimad capture | Not in the repo (private Google Sheet). | no |
| News & Intelligence data files | `ncec_permits_2026.json`, `reg_brief.json`, `ef_report_2025.json`, `saudi_waste_data.json` present. | not yet needed |
| skills.sh `find-skills` | Installed, but the registry (skills.sh) is blocked by the sandbox allowlist (HTTP 403) — every search returns "no skills found". Built-in skills used instead (`data:explore-data` for this part). Recorded for F4. | — |

**To continue past this gate I need from you:** (1) the current 2025 and 2026 tracker workbooks from Drive (or the v9 .xlsx if you want its Movement/Research sheets profiled too); (2) the `EH_Etimad_data` sheet ID (the Google Sheets connector can read it) or an export; (3) confirmation of the analyst-override list in §5.

## 1. Headline findings (the things that change how every card should be read)

1. **"High confidence" means "has an MWAN register entry".** 1,726 rows are High; 1,592 of them (92 %) carry an MWAN licence block and only 11 have a Confidence Basis, 6 an Evidence/Source, 7 a Services Confirmed. 108 High rows have neither an MWAN block nor a basis (53 of them EH Clients, where High presumably means "we invoice them"). The rubric says High = official registry source — that is exactly what the data shows, but the label is being read on the dashboard as "we know this company", which it is not.
2. **Half the map is effectively unscored.** 1,614 rows score 0, 1,228 are floored for Low confidence, 225 keep an analyst score pending re-scoring: 49 % of all rows, and among the 3,110 competitor rows 1,089 are zero, 1,054 floored, 158 pending. Tier 4 holds 2,938 of 3,110 competitors (94 %) — it is a holding pen, not a tier.
3. **The score is a service-overlap proxy.** Driver = "services" for 3,450 rows (82 %); "bids" for 426. Capability and Score are identical for 1,614 rows (both 0) and within the floor band for most of the rest.
4. **Threat is vestigial.** Blank for 2,609 rows (62 %), 9 "High" in the whole map, blank for 201 of 239 Tier 1 rows and for 88 bid-active rivals. It cannot support a card today.
5. **Client Value is revenue, not a fee schedule — but it is extremely concentrated.** The live map stores a project block per EH client (413 clients, SAR 184.8 m total, 2025 + 2026). The clusters at 4,600 / 3,450 / 4,025 (74 / 25 / 16 clients) are small standard-fee jobs; the top 5 clients are 80 % of value and the top 20 are 94 %. Any "client base" card that counts clients rather than value is misleading by construction.
6. **Bid encounters are flat, not concentrated.** 459 rivals have met EH; 330 of them exactly once. Top-10 rivals account for only 10.5 % of the map's 745 encounters (16 % in the bid dashboard's own 442-encounter extract). The competitive field is wide and shallow — a Pareto card would show the *absence* of concentration, which is itself the finding.
7. **Map and bid dashboard disagree on the basics.** Map: 459 bid-active rivals, 745 encounters (synced 20 Oct). Bid dashboard in the repo: 219 competitors, 442 encounters (built from a tracker ending Aug 2026). The hub copies are at different tracker dates; the stamp rule ("Competitors N · tracker as of <date>") is not holding across files in `hub/`. Needs the live Drive files to resolve.
8. **Tier does track bid activity for competitors — strongly.** Of 30 Tier 1 competitors, 28 have bid against EH; Tier 2: 49 of 51. But Tier 4 holds 244 bid-active rivals, 177 of them Low-confidence and floored. Who beats EH is a Tier 4 question as much as a Tier 1 one.
9. **Licence Watch is mostly non-competitors.** 332 licences expire within 180 days; 4 belong to bid-active rivals; 328 are Tier 4.
10. **Region is now 90 % filled** (408 blank, down from ~1,100): 327 of the blanks are Tier 4, only 3 are bid-active. Region is usable for conclusions; the residue does not affect any competitor finding.
11. **Residual duplicates: 15 normalised-name pairs** (e.g. EFSIM Facilities Management ×2, وادي رم لتدوير المعادن ×2, أريكي للخدمات البيئية ×2). No exact-name duplicates.
12. **Category "Direct Competitors" is MWAN-defined, not behaviour-defined.** 1,063 Direct rows: 973 have an MWAN block, 19 have ever bid against EH, 1 has Services Confirmed, 89 have none of the three. "Active Competitors" (173) is the behaviour category: 171 bid-active.

## 2. Column verdicts — live map, 4,211 rows

Verdict: **U** usable for conclusions · **C** usable with caveat · **N** not usable.

| Column (map key) | Filled | Distinct | Dominant value | Verdict | Note |
|---|---|---|---|---|---|
| Name (`n`) | 100 % | 4,211 | — | U | 0 exact dupes; 15 normalised twins (§1.11) |
| Category (`cat`) | 100 % | 12 | Indirect 1,874 · Direct 1,063 · EH Clients 406 | C | Direct = MWAN-licensed, not "competes with EH" (§1.12) |
| Tier (`tier`) | 92 % | 6 | Tier 4 3,103 · T1 239 · T3 229 · T2 191 · GOV 132 | C | 316 blanks are all EH Clients (no tier scheme for clients); Tier 1 is 186 clients + 30 competitors + 23 others |
| Tier (prev) (`tier_old`) | 33 % | 4 | — | C | Only for rows tiered before v2; fine for movement analysis |
| Company Type (`typ`) | 100 % | 12 | WM Co 1,679 · Other 1,551 | C | "Other" is 37 %; original type survives only in Notes ("Type: Contractor" ×288, Manufacturer ×278, Trader ×231 …) — recoverable |
| Region (`rg`) | 90 % | 18 | Riyadh 1,292 · Eastern 775 · Jeddah 688 | U | 408 blanks, 3 bid-active; mixed granularity (city "Jeddah"/"Rabigh" beside region "Eastern Province") |
| Province (`reg`) | 41 % | 35 | — | C | Derived; partial |
| City (`city`) | 79 % | 327 | Riyadh / الرياض split | C | AR/EN spelling pairs not unified (Riyadh 679 + الرياض 213) |
| Region basis | 15 % | 411 | Reviewer 181 · Google Places ≈380 | U | Audit trail only |
| Threat (`threat`) | 38 % | 3 | Low 1,473 · Med 120 · High 9 | **N** | §1.4 — retire or maintain decision needed |
| Score v2 (`sc`) | 96 % | 107 | 0 ×1,614 · 7 ×799 · 6 ×496 | C | 49 % effectively unscored; competitor bands: T1 ≥ ~44, T2 ~34–73, T3 ~23–33, T4 ≤ 36 (142 Tier 4 rows ≥ 23 — floored) |
| Score prev (`sc_old`) | 37 % | 136 | 24.3 ×523 · 20 ×322 | C | Pre-v2; many were the old "Low-confidence default" 24.3 |
| Capability (`cap`) | 95 % | 69 | mirrors Score | C | Near-redundant with Score below the floor |
| Score driver (`drv`) | 97 % | 6 | services 3,450 · bids 426 · backing 105 | U | Shows what the score is made of (§1.3) |
| Floor flag (`fl`) | 95 % | 2 | 1,228 floored | U | |
| Pending (`pend`) | 5 % | 1 | 225 | U | 158 competitors never re-scored under v2 |
| Confidence (`cf`) | 80 % | 3 | High 1,726 · Low 1,322 · Med 316 | C | 847 blank (333 EH Clients, 206 Potential Clients, 118 Indirect …); High ≈ MWAN entry (§1.1); of 459 bid-active rivals: Low 177, blank 174, Med 54, High 54 |
| Confidence basis | 4 % | 38 | sync auto-add 52 · tracker client 24 · N&I pages 22 | C | Present mostly on rows added by pipelines, not on researched rows |
| Services confirmed | 1 % | 17 | — | **N** for overlap claims | 25 rows |
| Evidence/Source | 1 % | 23 | — | N | 23 rows, one per Phase 1 research target |
| Last verified | 1 % | 1 | 2026-09-03 | N | 24 rows |
| Bids vs EH (`bid`) / Encounters (`bc`) | 100 % | 11 | 0 ×3,752 · 1 ×330 · 2 ×60 · ≥3 ×69 | U | Tracker-synced; flat distribution (§1.6); disagrees with repo bid dashboard (§1.7) |
| Bid flag basis (`bf`) | 10 % | 3 | Low 335 · Med 48 · High 21 | C | Only on 404 of 459 bid-active rows |
| Head-to-head (`h2h`) | 0.3 % | 10 | — | C | 14 rows carry app/wins/dq/undercut — the threat-matrix inputs; everything else must come from the tracker join |
| EH client block (`cl`) | 10 % | 419 | project block 413 · tracker block 6 | U | SAR 184.8 m, top 5 = 80 % (§1.5); 12 non-client rows also carry a block (SIRC-type cases: 4 Direct, 4 Indirect, 4 Potential) |
| Client score / tier (`clsc`,`cltier`) | 2 % | — | — | C | 65 rows; separate scheme |
| Licence activities (`act`) | 34 % | 275 | NH-COLL 141 · ENV-CON(A) 126 | U | Coded; `licenses.json` decodes |
| MWAN block (`mw`) | 38 % | 1,593 | — | U | expiry, days, cities, activities, vehicles; 971 Direct, 618 Indirect, 3 Active; 332 expire ≤ 180 d, 3 expired |
| Sites (`sites`) | 4 % | 14 | — | C | 171 rows |
| MWAN flag (`mn`) / Mega (`mp`) / Collab | 100 % | bool | — | U | |
| Backing (`bk`) | 90 % | 5 | 0 ×3,768 | C | Non-zero for 29 rows only |
| Sector (`sec`) | 16 % | 75 | Construction 130 · Manufacturing 78 | C | Filled mainly for Potential Clients (247) and Indirect (245) |
| Ownership (`own`) | 1 % | 33 | — | N | 37 rows |
| Added / Added from / on | 2 % | — | 101 on 2026-10-20; 57 sourced (SWA 22, EF 13, Etimad 12, Org review 10) | U | Provenance of the Oct additions |
| Notes | 84 % | 547 | MWAN snapshot 1,539 · "Type: …" 1,476 | C | Holds the retired taxonomy and all research excerpts; not machine-readable |

## 3. Bid tracker extract — shape only (stale copy, Aug 2026)

From the repo's bid dashboard data block (182 tenders: 79 in 2025, 103 in 2026 to SN 103):

- Outcome: Pending 135 · Cancelled 18 · Lost 16 · Won 13 (13 of 29 awarded = 45 % win rate on awarded; 7 % of all tenders).
- Value present for 67 of 182 (37 %); 115 blank. Service line blank for 59 (32 %): EIA/Studies 84, Services 31, Training 8.
- Pricing: 47 tenders have a priced roster; **23 have more than one priced bidder** — the entire "% above lowest bid" and undercut evidence base is n = 23. 101 rivals have been priced against; 143 priced head-to-heads in total; 6 rivals have ever won against EH.
- Loss reasons recorded on 10 of 16 lost tenders.
- Submission date present on 65 tenders ("submitted"); the standing rule (match across the tracker's own columns) must be re-run on the live files — this extract predates it.
- Turnaround (launch → deadline) available for 179 tenders: median 18 days; 29 tenders at ≤ 7 days.

These figures are **not** final — they will be recomputed from the Drive files you provide.

## 4. Etimad capture

Not available in the repo. Nothing profiled. Needed for B-11/B-12.

## 5. Analyst overrides — for confirmation only (appendix F1 candidates)

Competitor rows whose recorded Tier sits above the band their v2 score would give. Per §3 of the prompt these are excluded from every test; please confirm the list is complete (or strike any that are formula results):

| Row | Tier | Score | Confidence |
|---|---|---|---|
| FEAL Arabia Industrial Co. Ltd. | Tier 1 | 23.8 | High |
| Al Emad El Arabi for Environmental Services | Tier 1 | 28 | — |
| Green Sustainability Environmental Services | Tier 1 | 32 | — |
| Environmental Integration Consulting Office | Tier 1 | 37 | Medium |
| Evara Co. Ltd (One-Person Co.) | Tier 1 | 2 (pending re-score) | Medium |
| United Specialized Chemicals Factory | Tier 1 | 0 | Low |
| Imtithal Al-Beeah Environmental Consulting | Tier 2 | 0 | Low |
| مؤسسة ساس المتقدمة للنقليات | Tier 2 | 7 | High |
| Al-Jazeera Environmental Consulting Office · Atwar Environmental Consulting Est. | Tier 3 | 0 | Low |
| مؤسسة أرض خضراء لنقل النفايات · شركة الحلول المتفردة للخدمات البيئية | Tier 3 | 12.8 · 10 | High |

Reviva does not appear in the live map under that name — tell me its map name if it should be on this list.

## 6. Two things outside the brief that you should know

- **Repository visibility.** The session's git proxy cloned `strategic-planning-eh/eh-bid-dashboard` anonymously and reported it as a public repository. Your standing rule is that the repo must stay private because the source (and these data blocks) is not encrypted — only the published site is. Please check the repo's visibility setting; if it is public, every stakeholder row, client value and tracker price above is readable without the passphrase.
- **`hub/` files are at different tracker dates** (map 20 Oct; bid dashboard ≈ Aug). The published site rebuilds both hourly so this may be invisible to readers, but any analysis run from the repo copy of the bid dashboard would understate competitors by half.

## Next step

On your reply (files + override confirmation), I proceed to Parts B–D as scripts in `pipeline/analysis/`, then the report. Nothing in the workbook, tracker or hub is touched.
