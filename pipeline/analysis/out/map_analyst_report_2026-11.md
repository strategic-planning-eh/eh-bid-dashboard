# Stakeholder Map × Bid Tracker — analyst conclusions and dashboard gaps

**Stage 1 report · 1 Nov 2026 · for Youssef Abdelaal (BD)** · scripts `pipeline/analysis/{profile_map,build_v9_workbook,analyse}.py`, every number traceable to `pipeline/analysis/out/analysis.json` and `map_profile.json`

> **Read this first.** Two data limits shape every number below. (1) The bid data is the extract baked into the repo's bid dashboard — tracker to **Aug 2026, 182 tenders** — because the Drive files are not in the repo; the map's own encounter counts are newer (synced 20 Oct). Pricing and win/loss figures will move when the live tracker is loaded; the direction of each conclusion is unlikely to. (2) **135 of 182 tenders (74 %) have no outcome recorded**, so "never won" below means "no award recorded", and win rates are computed on 29 awarded tenders only. The Etimad capture was not available, so B-11 is blocked.

Part A (data profile) is in `claude/map_analyst_part_a_profile.md`; its twelve findings are assumed here.

---

## Part B — Conclusions the dashboard does not currently state

**B-1. Tiering predicts *whether* a rival shows up, not *whether it beats EH on price*.**
Evidence: of competitor rows outside the override list, Tier 1 = 24 (23 bid-active), Tier 2 = 49 (47), Tier 3 = 87 (86), Tier 4 = 2,938 (196). But the undercut rate — share of priced head-to-heads where the rival priced below EH — is 67 % for Tier 1, 54 % Tier 2, 71 % Tier 3, 54 % Tier 4. 34 Tier 3/4 rivals have priced below EH; one Tier 4 (Kafaat Training) has won against EH. Only one Tier 1 competitor has never met EH in a tender (Marine Operations Environmental Services / SAIL). · Confidence: **High** on bid-activity, **Medium** on undercut (n = 105 priced pairs) · Would change if: live tracker adds Sep–Oct rosters · Lives in: Stakeholder Map KPI strip + E-3.

**B-2. EH is beaten on price almost exclusively in environmental studies, almost always by government buyers, by a cluster of 15 consulting firms — and a third of them are not even flagged as confident in the map.**
Evidence: 21 tenders with EH priced and ≥ 2 priced bidders; 95 below-EH prices recorded, 85 of them in Env. Studies / EIA, 87 from government buyers vs 8 from companies (buyer type per Youssef's 1 Nov rule: ministries, authorities, أمانات, هيئات, national centres, public corporations, universities, military/health bodies = government; state-owned companies such as SEC, SIRC, NWC, ACWA = companies). Priced head-to-heads come almost entirely from Etimad tenders, whose opening reports disclose prices; company buyers rarely do. Top undercutters: البيئة والتنمية (3 of 4), AH Enviro (3/3), Al Emad El Arabi (3/3), GSCES (3/3), Evara (3/3), Imtithal (3/3), then Environmental Integration, ADECO, Al Mandariyah, GECO (2 each). Of the 66 rivals that have ever priced below EH: 15 Tier 1, 17 Tier 2, 16 Tier 3, 18 Tier 4; confidence High 13, Medium 9, Low 13, **blank or not in map 36**. · Confidence: **Medium** (the 21-tender base) · Would change if: 2025 roster prices for the Sep–Oct tenders arrive · Lives in: Bid & Tender Executive Summary (replaces the generic threat-matrix framing) + E-1, E-4.

**B-3. Competitive pressure is wide and shallow — the map is built for a concentration that does not exist.**
Evidence: map — 459 rivals, 745 encounters, 330 seen once, top-10 share 10.5 %, 108 rivals needed to reach half of all encounters; bid extract — 219 rivals, 442 encounters, top-10 share 16 %, 50 rivals for half. Only 69 rivals have ≥ 3 encounters. The map holds 3,110 competitor rows for 459 that have ever appeared. · Confidence: **High** · Would change if: nothing short of a different market · Lives in: Stakeholder Map summary (E-2) and the BD narrative — effort should follow the 69, not the 3,110.

**B-4. When EH loses on price it is not by a little: median gap to the lowest bid is 78 %, and 2025 was far worse than 2026.**
Evidence: 21 priced tenders; gap to lowest median 78 %, mean 283 %, p75 452 %, max 1,476 %; EH was lowest in 5 (won 2, 3 pending). 2025 median 452 % (n 11) vs 2026 median 62 % (n 10). Studies/EIA median 76 % (n 14); government buyers median 130 % (n 15) vs companies 76 % (n 6). Of 7 priced tenders lost with a named winner, 6 carried a price-type reason or none, 1 a technical rejection. The three worst gaps are genuine (e.g. 2025-37: EH SAR 630k vs 67.9k; 2025-61 training: EH 1.38 m vs 217k), not unit errors. · Confidence: **Medium** — n is small, and spot-checks show the extremes are real · Would change if: more priced rosters (the Sep–Oct opening reports) · Lives in: Executive Summary pricing block (E-5) — show the median and the year split, not the mean.

**B-5. Clients and issuers overlap less than assumed, and eight "competitors" are also paying EH clients.**
Evidence: 96 tracker issuers, 87 bridged to the map; 17 of them are EH clients (Aramco e-Marketplace 3 bids, Saudi Energy 3 + 2 + 1 under three labels, Petrorabigh 2, Linxon 2, NEOM, SAL, CEER …) — none of those bids has a recorded loss, and only Saudi Energy and ZATCA have recorded wins. Eight competitor rows carry an EH client revenue block (e.g. شركة أسمنت المدينة SAR 175k, حلول معالجة النفايات الإلكترونية SAR 60k, شبه الجزيرة للمقاولات) — all Tier 4, none bid-active: they are waste generators that hold a collection licence, not rivals. · Confidence: **High** · Would change if: nothing · Lives in: Organisations view flag + Client Bubble Map (E-7).

**B-6. EH competes in Riyadh and from Riyadh, not from its licensed base.**
Evidence: 123 of 182 tenders come from Riyadh-based issuers (18 unknown region); every recorded win (12/13) and 12 of 16 losses are Riyadh. Bid-active rivals: Riyadh 259, Eastern 59, Jeddah 59; Tier 1/2 rivals: Riyadh 36, Jeddah 16, Eastern 12; undercutters: Riyadh 34, Jeddah 15, Eastern 10. Demand side (NCEC permits 2026 YTD, minimum reported): Riyadh 2,600, Eastern 1,600, Makkah 1,200 of ≈ 17,000 national. EH's licensed footprint (Rabigh/Al-Juhfah, Jeddah) sits in the region with the third-largest permit flow and the second-largest rival cluster. · Confidence: **High** on the tracker side, **Medium** on demand (NCEC gives floors, not totals) · Would change if: client regions for the 18 unknown issuers · Lives in: Saudi waste page cross-link + E-6.

**B-7. The Licence Watch is a Tier 4 list: licence expiry is not where EH's competitive opportunity is.**
Evidence: 329 licences expire within 180 days; 4 belong to bid-active rivals (وصل Tier 1, النخبة الخليجية Tier 1, الاداء المتوازن Tier 2, نواقل الدولية Tier 3); 3 licences are already expired, all Tier 4. Within 365 days, 12 Tier 1–3 licences expire, including ESCO, GESCO, البيئة والتنمية and رواد الاستدامة (Tier 1, spring 2027). Hazardous-activity licences expiring ≤ 180 days: 8 rows, 2 of them Tier 1–3. · Confidence: **High** (MWAN snapshot Jul 2026 — the snapshot itself is 3 months old) · Would change if: a fresh MWAN register export · Lives in: Licence Watch (E-8 — filter to Tier 1–3 and bid-active by default).

**B-8. "Direct Competitors" is a licence category, "Active Competitors" is the behaviour category — the names are the wrong way round for a reader.**
Evidence: Direct = 1,063 rows: 973 MWAN-licensed, 68 with a hazardous-waste activity, 19 bid-active, 1 with confirmed services, 89 with no evidence of any kind; 1,044 are Tier 4. Active = 173 rows: 171 bid-active. Meanwhile 173 "Indirect / Adjacent" rows are bid-active and 24 have priced below or beaten EH — the "indirect" label hides a third of the real competition. · Confidence: **High** · Lives in: taxonomy decision (C2) before any category card is built.

**B-9. Tier movement since v2 has been research-driven and floor-driven, not market-driven.**
Evidence: 223 competitor rows changed tier; 62 up, 161 down. Upward moves: 25 bid activity, 23 confidence upgrades (Phase 1 research), 12 floor-rule releases, 2 rescoring. Downward: 119 rescoring (v2 weights), 41 bid-activity-related, 1 research. The Movement Report's "risers" therefore mostly record that EH learned something, not that a rival grew. · Confidence: **High** on the counts, **Medium** on the driver attribution (inferred from flags, not logged) · Lives in: Movement Report wording (E-9).

**B-10. EH's bidding is concentrated on a few government issuers it has not yet won from — and the tracker cannot tell us whether it lost.**
Evidence: Saudi Energy / SEC 23 bids (6 won, 10 awarded); NCVC 17 bids, 0 awarded recorded; SWA 13 (4 won); NCEC 9, 0 awarded recorded; SWCC 4; ZATCA 3 (1 won). Issuers with ≥ 3 bids and no recorded win: NCVC, NCEC, SWCC, Military Industries Corp, Aramco e-Marketplace, Saudi Energy (second label). 9 of 96 issuers are not in the map at all (Armed Forces Medical Services, Royal Saudi Naval Forces, Transport General Authority, Royal Saudi Air Force, National Guard Health Affairs, GAMI, King Khalid Military College, TVTC, Northern Border University) — a military/defence cluster EH bids to but has never mapped. Issuer mix by map tier: GOV 54, Tier 1 20, Tier 2 10, not in map 9. · Confidence: **High** on counts, **Low** on win/loss (74 % no outcome) · Would change if: outcome discipline in the tracker · Lives in: Executive Summary buyer block (E-10) + map additions.

**B-11. Tracker versus the Etimad market — blocked.** No Etimad capture available in this session. Required: the `EH_Etimad_data` sheet.

**B-12. The intelligence pages feed the map only at the entity level — nothing in the map or tracker references a regulatory event, a permit figure, or an Environment Fund product.**
Evidence: 57 map rows carry an intelligence provenance (SWA chart 22, Environment Fund 13, Etimad 12, Organisations review 10). Of 20 Environment Fund stakeholders in `ef_report_2025.json`, 10 are map records; the other 10 are named individuals (board/executives) and three unnamed grant recipients. The NCEC permits file has region figures that no card joins to the map's regions; the two regulatory briefs are text only. · Confidence: **High** · Lives in: E-11 (intelligence-to-target card) and C2.

---

## Part C — Missing-data register

### C1 — Caveats to display with each conclusion

| Conclusion | Gap | How the card should say it |
|---|---|---|
| B-1, B-2, B-4 | Priced rosters exist for 47 tenders, ≥ 2 priced bidders for 21–23 | "Based on 21 priced tenders" in the card subtitle; hide percentages when n < 5 |
| B-2 | 36 of 66 undercutters have blank confidence or no map record | "Confidence unset for N of these rivals" chip |
| B-4 | Gaps are heavy-tailed (mean 283 % vs median 78 %) | Show median, label the mean as skewed, keep the max as a tooltip |
| B-5, B-10 | 74 % of tenders have no outcome | Every win/loss figure carries "n awarded = 29"; "no result recorded" must be its own bar, never folded into "lost" |
| B-6 | 18 issuers without a region; NCEC permits are minimum figures | "≥" prefix on permit numbers; "region unknown" segment shown |
| B-7 | MWAN snapshot Jul 2026 | "Licence data as of Jul 2026" stamp |
| B-9 | Drivers inferred from flags | "Driver inferred" footnote until the sync logs reasons |
| B-12 | Etimad absent | Card shows "no capture loaded" state, as the Etimad tab already does |
| All | Map "High confidence" ≈ MWAN entry | Rename the chip "Registry-verified" (see C2-2) or the rubric is misread everywhere |

### C2 — Data-debt backlog, ranked by what it unlocks

| # | Gap | Unlocks | Source | Owner | Effort | Order |
|---|---|---|---|---|---|---|
| 1 | Tender outcomes: 135 of 182 tenders with no result; winner named on 1 non-EH award | Every win-rate, loss-reason and "never won" figure (B-5, B-10, E-1, E-10) | Tracker discipline — a monthly pass over Etimad award notices for open tenders | Bid committee / Youssef | M (recurring) | 1 |
| 2 | Confidence rubric: 1,726 High rows with 11 bases; rename High → "Registry-verified", reserve "Verified services" for rows with Services Confirmed | Honest confidence chips on all 4 apps; stops "high-confidence competitor" meaning "licensed somewhere" | Wording change in sync + map methodology; no new data | Youssef | S | 2 |
| 3 | Live tracker in the analysis path (Drive 2025/2026 files, or a committed extract each publish) | Recomputes B-1/2/4 on current data; fixes the `hub/` date mismatch (Part A §6) | `run_pipeline.py` writes `pipeline/analysis/out/bid_extract.json` each publish | pipeline | S | 3 |
| 4 | Etimad capture history | B-11; market-share-of-bids card | `EH_Etimad_data` sheet (weekly) | Youssef | S to share, L to accumulate | 4 |
| 5 | Threat field: 62 % blank, 9 High — decide: retire, or derive it (undercut × encounters × tier) and stop hand-editing | Any "threat" card; removes a contradictory column | Decision; derivation is a sync formula | Youssef | S | 5 |
| 6 | Category semantics: Direct (licence) vs Active (behaviour) vs Indirect (173 bid-active) | B-8; category filters that mean what they say | Rename or re-rule in `sync_bids_to_apps.py`; log in Reclassification Log | Youssef | M | 6 |
| 7 | Services Confirmed for Tier 1–2 competitors (73 rows, 25 confirmed anywhere) | Real service-overlap scoring (D) | Web + Wathq, paced per the 200-search rule | Claude + Youssef | M | 7 |
| 8 | Map records for the 9 unmapped issuers (defence/military cluster) | B-10 completeness; Organisations view profiles | Add via the pending-decisions workflow | Youssef | S | 8 |
| 9 | Client label bridges: 13 tracker labels bridged by hand in this analysis (SEC/Saudi Energy/SE, SWCC→SWA, ZATCA, NCVC, NCEC, SIO, SIRC, Luberef, MEWA, Imam Abdulaziz Reserve, MIC) | Issuer joins in every app; the "16 client_aliases labels" open item | Append to `client_aliases.json` | Youssef approves, pipeline | S | 9 |
| 10 | Fresh MWAN register export (snapshot is Jul 2026; 3 licences already expired) | B-7; Licence Watch accuracy; 405 region residue | MWAN data request already sent | MWAN / Youssef | — | 10 |
| 11 | Region for 18 issuers and 408 map rows (3 bid-active) | B-6 completeness | Youssef's manual fill | Youssef | S | 11 |
| 12 | Bid roster prices for the 24 tenders with a roster but no prices | Doubles the pricing base | Etimad opening reports | Youssef | M | 12 |

---

## Part D — Scoring model validation (v2)

Components reverse-engineered from the live data (the workbook stores totals, not components): **services = `cap`**, **bids = flat 15 for any row with ≥ 1 encounter** (152 of 170 rows with 1 encounter, 3 of 3 with 9 — encounters never scale the score), **backing = `bk`** (non-zero on 29 rows), mega flag (52 rows), sites (171 rows). Workforce, footprint and multi could not be isolated. Overrides (12 rows, F1) excluded; 3,098 competitor rows tested.

**Discriminating power** (Spearman ρ against the two outcomes the model should predict):

| Component | ρ · bid-active | ρ · has undercut EH | Lift, top quartile → bid-active |
|---|---|---|---|
| Services (cap) | 0.45 | 0.20 | 2.1× |
| Score ex-bids | 0.47 | 0.19 | 2.1× |
| Score v2 (total) | 0.52 | 0.21 | 2.1× |
| Backing | 0.07 | −0.01 | — |
| Mega flag | 0.13 | 0.02 | — |
| Sites | 0.11 | 0.04 | — |

Reading: the services component carries almost all of the model's predictive weight; backing, mega and footprint add nothing measurable against either outcome. The bids component adds 0.05 of ρ because it is binary — it cannot distinguish a rival met once from one met nine times.

**Floor rule:** 107 Low-confidence bid-active competitors; 55 are floored, 95 sit in Tier 4; 6 have priced below EH, 0 have beaten EH, 9 have ≥ 3 encounters, 140 encounters in total. The rule hides activity but has not yet hidden a winner.

**Sensitivity** (tier distribution of 3,098 competitors; thresholds T1 ≥ 44, T2 ≥ 34, T3 ≥ 23):

| Model | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Rivals with ≥ 3 encounters that move up |
|---|---|---|---|---|---|
| v2 as published | 23 | 41 | 238 | 2,796 | — |
| **Scaled bids** (10 + 5 × min(encounters, 5), floor exempt when bid-active) | 57 | 51 | 200 | 2,790 | 38 |
| v2, floor exempt at ≥ 2 encounters | 23 | 55 | 230 | 2,790 | 6 |

Scaled bids promotes the rivals BD already recognises — AH Enviro (6 encounters), Kayan Al Amthal (6, has beaten EH), Oasis of Excellence (6), Vision Dimensions (6), Fuel Professional (5, Tier 4 → 1), Naqsh, Verde, Renewable Environment (4 each) — without touching Tier 4's size.

**Recommendation:** keep v2's structure and thresholds; replace the binary bids component with the scaled form and exempt bid-active rows from the Low-confidence floor. Deliver as a dry-run script (`pipeline/analysis/rescore_dryrun.py`, to be written at Stage 2) that writes a before/after sheet and changes nothing until approved. Do not re-weight backing/mega/footprint on this evidence — they are too sparse to test, not proven useless.

---

## Part E — Recommended new summary cards and charts

Priority: **Must** = buildable now and changes a decision · **Should** = buildable now, sharpens an existing view · **Could** = blocked or marginal. Sample values are from the current data (map 20 Oct sync; tracker extract to Aug 2026).

### CEO headline (Bid & Tender → Executive Summary, top row)

| ID | Name EN / AR | Question | Type · placement | Data & computation | Sample | Caveat shown | Blocked by | Priority |
|---|---|---|---|---|---|---|---|---|
| E-1 | Where we lose on price / أين نخسر على السعر | In which service line and buyer type does EH get undercut? | Stacked bar (service × buyer type) · first card after the headline numbers | pricing rows with EH price and ≥ 2 priced bidders; count below-EH prices by `svc` × buyer type (issuer-name rule in `bid_analytics2.py`) | Studies/EIA 85 of 95 · government 87 / companies 8 | "21 priced tenders" | — | **Must** — built 1 Nov 2026 |
| E-2 (built 1 Nov 2026) | How wide the field is / اتساع المنافسة | Is competition concentrated or spread? | Pareto curve with a marker at the 50 % point · replaces nothing; sits beside the funnel | encounters per rival, cumulative share; marker = rivals needed for 50 % | 50 rivals for half of 442 encounters; 122 seen once | "Tracker as of <date>" | — | **Must** |
| E-5 (built 1 Nov 2026) | Price gap when we lose / فجوة السعر عند الخسارة | How far above the winner is EH, typically? | Box/strip plot by year with the median labelled · replaces the per-tender "% above lowest" bar (keep that as a drill-down) | `gap` per priced tender; median, p25–p75; split 2025/2026 | median 78 % (2025: 452 %, 2026: 62 %) | median not mean; n per year | — | **Must** |
| E-10 (built 1 Nov 2026) | Buyers we keep bidding to / الجهات التي نكرر التقدم لها | Which issuers take most of our bids, and what came back? | Table: issuer · bids · won · awarded to others · no result · map tier · opens Organisations profile | tracker `clients` list joined to map via client bridges | Saudi Energy 23 / 6 won; NCVC 17 / 0 awarded; SWA 13 / 4; NCEC 9 / 0 | "No result" is its own column | C2-1 for the won/lost split | **Must** |
| E-12 (built 1 Nov 2026) | Results still unknown / نتائج غير مسجّلة | How much of our record is blank? | KPI card + button to the open-tender list · top row | tenders with no outcome ÷ total | 135 of 182 (74 %) | — | — | **Must** |

### Bid committee (Bid & Tender → Executive Summary, second row, and Watchlist)

| ID | Name EN / AR | Question | Type · placement | Data & computation | Sample | Caveat | Blocked by | Priority |
|---|---|---|---|---|---|---|---|---|
| E-3 | Rivals by tier: met vs beat us / المنافسون حسب الفئة | Does our tiering match who actually hurts us? | Grouped bar per tier: bid-active · priced below EH · beaten EH | map tier × rec from bid extract (override rows excluded) | T1 23/9/3 · T2 47/14/1 · T3 86/12/1 · T4 196/14/0 | overrides excluded | — | **Should** |
| E-4 | The undercutter list / قائمة من يقدّمون أقل منا | Who prices below us most often, and do we know them? | Ranked table with confidence chip and "profile" link | below-EH count / priced pairs per rival; map tier & confidence | 6 rivals at 3/3 or 3/4; 36 of 66 with blank confidence | n per rival | — | **Should** |
| E-13 | Lowest and still lost / الأقل سعراً ولم نفز | How often was EH lowest and did not win? | KPI | rank = 1 and has_winner and not won | 0 of 5 so far (3 pending) | small n | C2-1 | Could |

### BD (Stakeholder Map summary strip; Client Bubble Map Executive tab)

| ID | Name EN / AR | Question | Type · placement | Data & computation | Sample | Caveat | Blocked by | Priority |
|---|---|---|---|---|---|---|---|---|
| E-6 | Where the fight is vs where we are / أين المنافسة وأين نحن | Does our footprint match the demand and the rivals? | Map overlay or three-column bar per region: tenders · bid-active rivals · NCEC permits · EH sites | tracker client region, map rival region, `ncec_permits_2026.json`, EH sites | Riyadh 123 / 259 / ≥ 2,600; Jeddah 6 / 59 / — ; Eastern 5 / 59 / ≥ 1,600 | permits are minimums | — | **Should** |
| E-7 | Clients who also hold our licences / عملاء يحملون تراخيصنا | Which paying clients are tagged as competitors? | Small table with a "waste generator, not rival" flag · Client Bubble Map | competitor rows with a client revenue block | 8 rows, all Tier 4, none bid-active, SAR 175k top | — | — | Could |
| E-14 | Client value concentration / تركّز قيمة العملاء | How dependent are we on a few clients? | KPI pair: top-5 share · top-20 share | client revenue blocks | 80 % / 94 % of SAR 184.8 m | 2025–26 only | — | **Should** (the Pareto chart exists; the headline number does not) |

### Intelligence (News & Intelligence hub; Stakeholder Map)

| ID | Name EN / AR | Question | Type · placement | Data & computation | Sample | Caveat | Blocked by | Priority |
|---|---|---|---|---|---|---|---|---|
| E-9 | Why tiers moved / لماذا تغيّرت الفئات | Is a tier change market news or our own research? | Movement Report gets a "driver" column and two totals | tier vs tier_old, driver inferred from flags (research / bid activity / floor / rescoring) | 62 up (25 bid activity, 23 research, 12 floor); 161 down (119 rescoring) | inferred until logged | — | **Should** |
| E-11 | Intelligence that became a target / من الخبر إلى الهدف | Which signals on the intelligence pages have a stakeholder or tender attached? | List: signal · source page · linked map record / tender · "no target yet" | `added_from`, EF stakeholders, reg briefs, permits | 57 map rows sourced from intelligence; EF: 10 of 20 in map; permits: no link | — | partly C2-4 | Could |
| E-8 | Licence Watch, narrowed / مراقبة التراخيص | Which rivals that matter lose a licence soon? | Default filter Tier 1–3 or bid-active; count card | MWAN `days` ≤ 180 / ≤ 365 | 4 bid-active within 180 d; 12 Tier 1–3 within 365 d | MWAN snapshot Jul 2026 | C2-10 | **Should** |

### Data owner (hub shell, small "data health" strip)

| ID | Name EN / AR | Question | Type | Data | Sample | Priority |
|---|---|---|---|---|---|---|
| E-15 | Map evidence coverage / تغطية الأدلة | How much of the map is more than a registry line? | Three meters: registry-verified · services confirmed · bid-evidenced | cf High with MWAN / services_confirmed / bc > 0 ÷ competitor rows | 1,592 / 25 / 459 of 3,110 | **Should** |
| E-16 | Tracker completeness / اكتمال جدول المنافسات | How complete is the record the dashboards run on? | Meters: outcome recorded · value recorded · price roster · submission date | tracker fields ÷ 182 | 26 % · 37 % · 26 % · 36 % | **Should** |
| E-17 | Etimad history / عمق بيانات اعتماد | How many weeks of market capture do we have? | KPI | Etimad sheet | — | Could (blocked) |

### What changes in the Executive Summary — in words

Order, top to bottom: **E-12** results unknown (so every number that follows is read with it) → the existing six headline cards → **E-1** where we lose on price → **E-5** price gap by year → **E-10** buyers we keep bidding to → existing funnel and win-rate charts → **E-2** how wide the field is → threat matrix, re-labelled with the override note → **E-3 / E-4** → watch items.

The summary should open with three sentences, each tied to a conclusion:

1. "Seven in ten of our tenders have no recorded result, so every rate on this page is computed on 29 awards." (B-10, E-12)
2. "When we lose, it is in environmental studies for government buyers, and we are typically 78 % above the lowest bid — half the gap of 2025." (B-2, B-4)
3. "Competition is wide, not deep: 50 firms account for half of all encounters, and the ones that undercut us are as often Tier 3–4 as Tier 1." (B-3, B-1)

---

## Part F — Appendices

**F1 — Analyst-override rows excluded from Parts B–D** (listed without comment; awaiting Youssef's confirmation): Al Emad El Arabi for Environmental Services · Al-Jazeera Environmental Consulting Office · Atwar Environmental Consulting Establishment · Environmental Integration Consulting Office · Evara Co. Ltd (One-Person Co.) · FEAL Arabia Industrial Co. Ltd. · Green Sustainability Environmental Services Co. (GSCES) · Imtithal Al-Beeah Environmental Consulting Office · United Specialized Chemicals Factory · شركة الحلول المتفردة للخدمات البيئية · مؤسسة أرض خضراء لنقل النفايات · مؤسسة ساس المتقدمة للنقليات. (Four of these appear in B-2's undercutter list on the tracker's evidence; they are reported there as facts about pricing, not as a comment on their tier.)

**F2 — Bridge coverage.** Bid-extract competitors: 219, bridged to the map 215 (4 unbridged: مختبر قطرة الحياة, الوطنية للخدمات الجيومكانية, two Green East spellings — the deleted ghost). Issuers: 96, bridged 87 (13 by hand bridges this analysis proposes for `client_aliases.json`, see C2-9), 9 unmapped (C2-8). Map rows flagged "Claimed bidder (unverified)": not present in the live map as a distinct flag — the 286 workbook-only bid flags recorded in `bid_sync_report_preview.json` are not visible on the map as such and should be, or the flag should be retired.

**F3 — Reproducibility.** `pipeline/analysis/profile_map.py` → `out/map_profile.json`; `build_v9_workbook.py` → `out/EH_Stakeholder_Competitive_Map_v9_live.xlsx`; `analyse.py` → `out/analysis.json`. Inputs: `out/map_data_raw.json` and `out/bid_data_raw.json` (data blocks lifted from `hub/EH_Stakeholder_Map_CURRENT.html` and `hub/EH_Bid_Analysis_CURRENT.html` at commit ae8fde0), `pipeline/aliases.csv`, `client_aliases.json`, `ncec_permits_2026.json`, `ef_report_2025.json`, `reg_brief.json`. Re-run order: profile → workbook → analyse.

**F4 — Skills used.** `find-skills` (skills.sh): installed, registry unreachable from the sandbox (allowlist 403) — no external skills used. Built-in: `data:explore-data` (Part A method), `xlsx` (workbook build + recalculation, 48 formulas, 0 errors), `data:statistical-analysis` (medians over means for the gap distribution, Spearman for D, small-n caveats), `data:validate-data` (pre-delivery pass: spot-checked the three largest price gaps against the roster rows — real; verified subtotal 29 awarded = 13 won + 16 awarded elsewhere; confirmed overrides are excluded from D; flagged the 74 % no-outcome share as the governing caveat). Validation verdict: **share with noted caveats** — the caveats are C1.

---

## Status

**Stage 2 (1 Nov 2026):** the five Must cards (E-1, E-2, E-5, E-10, E-12) and the three opening sentences are live on the Bid & Tender Executive Summary in the proposed order, via `pipeline/patch_exec_analyst.py`. Still open: the Should cards (E-3, E-4, E-6, E-8, E-9, E-14, E-15, E-16), the scoring dry-run (Part D), the Etimad sheet for B-11, and the F1 override confirmation.
