# Working prompt — "Saudi waste" page for the Strategic Intelligence Hub

## Role and goal
You are the analyst for Environmental Horizons (EH), a Saudi hazardous-waste company licensed by MWAN with its facility at the Al-Juhfah complex near Rabigh (Makkah region). Read the waste statistics the General Authority for Statistics (GASTAT) publishes. Produce a direct analysis of where waste is generated and where it accumulates across the Kingdom's 13 administrative regions, with particular attention to **hazardous** and **industrial** waste. Deliver it as a new page called **"Saudi waste"** («النفايات في المملكة») in the Strategic Intelligence Hub. Senior management must be able to read it without a statistician beside them.

## Sources (the only inputs)
| File | Use |
|---|---|
| Environment Statistics 2024 (EN) | **Canonical** for every series it carries. Section 3 only, and only the waste tables: 3-8 to 3-16 |
| Environment Statistics 2023, 2022, 2021 (EN) | Earlier editions. Use them only to show where GASTAT revised a figure (for example, Jubail–Yanbu 2018–2021), and never to override the 2024 edition |
| SEEA Waste 2024 (EN) | Whole file. National waste accounts for 2023–2024 by waste type, by the sector that produced it, and by destination |
| Region population (2022 census, 2022/2023 editions, table 5-1) and region area (2024 edition, table 1-22) | Denominators only |

Leave out everything that isn't waste: climate, air, water resources, biodiversity and so on. Wastewater tables 3-1 to 3-7 are liquid effluent rather than solid or hazardous waste, so they stay out of scope and the page says so in one line. Sewage sludge stays in, because the SEEA counts it as waste.

## Rules
1. **No invented numbers.** Every figure on the page traces to a file, sheet and row. Hover or tap shows the source as "GASTAT Environment Statistics 2024, table 3-9".
2. **A missing breakdown is stated, never estimated.** These files publish no regional split for hazardous waste or for industrial waste outside Jubail and Yanbu, and the page says this plainly. Do not allocate national hazardous tonnes to regions by population, GDP or any other key. Jubail (Eastern region) and Yanbu (Madinah region) are the only places with published industrial and hazardous tonnages, and the map shows them as such.
3. **Read spreadsheets by cell position.** Merged headers and blank cells shift columns, so map each column from the header rows and never from the order of non-blank values.
4. **Contradictions are shown, not resolved silently.** Known cases:
   - Tables 3-15 and 3-16 are both titled "Waste imports by type". For trade, use the clearly labelled SEEA import and export columns and record the duplicate title in the data notes.
   - Municipal waste treated (3-10) and collected (3-9) do not total the same for some years.
   - The SEEA municipal share does not equal the Ministry of Municipalities and Housing collected tonnage.
5. **Per-person rates** use 2022 census population, the latest regional count in the files, and are labelled that way.
6. **Plain language** (UK spelling), with full English and Arabic versions. Name each agency in full once on the page, then use the short form. Mark anything that is EH's reading rather than GASTAT's data as "EH analysis".

## Analysis to run
A. **National picture (SEEA 2023→2024).** Cover:
   - total waste and its growth;
   - tonnes by waste type;
   - tonnes by generating sector;
   - destination: landfill, specialised waste companies, other disposal including open dumping, and recycling within each sector;
   - imports and exports by type.

B. **Hazardous waste.**
   - Tonnage 2023 and 2024, plus hazardous medical waste.
   - Which sectors generate it.
   - Where it goes: the share handled by specialised waste companies is EH's addressable market.
   - Recycling share.
   - The jump in hazardous waste imports.
   - Jubail and Yanbu's hazardous tonnage as a share of the national total, which shows how much of the national total has no published location.

C. **Industrial waste (Jubail and Yanbu, 2010–2024).**
   - Tonnage trend and compound growth rate.
   - Disposal methods (incineration, burial, recycling).
   - Hazardous versus non-hazardous split from 2021.
   - Recycling rate.
   - Revisions between editions.

D. **Regional municipal waste (13 regions, 2017–2024).** Cover:
   - collected tonnage and rank;
   - kg per person per day;
   - tonnes per km²;
   - growth 2017→2024 and 2021→2024;
   - what it's made of (organic, plastic, paper, metal, glass, fabric, other);
   - how it is treated (landfill, recycling, incineration);
   - **accumulation**: tonnes landfilled each year and cumulatively 2017–2024 — "where waste is piling up";
   - recycling rate by region;
   - outliers and data breaks, such as Madinah's 2020 drop and Eastern region's 2022 spike in "other" waste.

E. **What it means for EH (EH analysis).** Cover:
   - where the hazardous and industrial volume sits (or cannot be placed);
   - the size of the specialised-company hazardous market;
   - EH's home region (Makkah) against the others;
   - the data EH should formally request from MWAN / the National Center for Waste Management (regional hazardous generation by type), tied to the existing MWAN data-request route.

## Page specification
- **Page:** `hub/saudi_waste.html`, generated by `pipeline/build_saudi_waste_page.py` from `pipeline/saudi_waste_data.json`. That JSON is written by `pipeline/extract_saudi_waste.py` from the source workbooks, which are kept in `pipeline/sources/gastat_waste/`.
- **Hub wiring:** a new News & Intelligence sub-tab "Saudi waste" (`data-n="waste"`, iframe `f-waste`) with a skeleton loader, search aliases and a "New" badge. Add a publisher copy step and a `pipeline/CHANGES.md` line so it shows in What's New.
- **Design:** EH design system (`eh-shared.css` / `eh-shared.js`, EH fonts and colours). Follows the hub's language (EN/AR, RTL) and theme (light/dark) through the hub bridge. Works on a phone. Every chart can be saved as a PNG.
- **Map:** a choropleth of the 13 regions drawn with the hub's bundled D3, using public-domain Natural Earth boundaries embedded in the page (no outside requests). A metric switch covers collected tonnage, per person, per km², landfilled, landfilled cumulatively 2017–2024, recycling rate and growth, with a year slider for 2017–2024. Overlay points for Jubail and Yanbu carry the industrial and hazardous figures. A third point marks EH's Al-Juhfah site for reference. A legend shows the colour scale, and the region detail panel opens on click or tap.
- **Sections in order:**
  1. Headline cards
  2. Regional map and ranking table
  3. Hazardous waste
  4. Industrial waste (Jubail and Yanbu)
  5. National picture
  6. Municipal trend and the fall in recycling
  7. What it means for EH
  8. Data notes and gaps, including revisions and the duplicate title
- **Checks before publishing:**
  - Recompute the headline figures from the workbooks with a separate script and compare them with the page.
  - Screenshot EN/AR × light/dark and phone width, and fix any overflow.
  - Confirm the hub tab loads the page.

## Known data problems (found 13 Oct 2026 — check again whenever GASTAT publishes a new edition)
1. **No regional figures for hazardous or industrial waste** (changes conclusions). Hazardous waste (6.91 Mt, 2024) is published only as a national total by producing sector. Industrial waste is published only for Jubail and Yanbu combined (Royal Commission), and nothing for MODON industrial cities. Only 10% of 2024 hazardous waste has a published location.
2. **2024 national accounts are mostly 2023 scaled up, not new measurements** (changes conclusions). In the SEEA tables, almost every 2024 value equals the 2023 value times one growth factor per sector: mining, manufacturing and utilities ×1.2099 (all waste types), agriculture ×1.3278, other activities ×1.0822, households ×1.0963. Hazardous waste in all four industry sectors ×1.2084, and hazardous waste sent to waste companies ×1.2084.
3. **Sector split is apportioned with fixed ratios** (changes conclusions). For 8 waste types, manufacturing is exactly 2.364 × mining and utilities exactly 0.052 × mining, in both years. Identical tonnages repeat across types: paper = 'other' = mixed waste in the industry sectors (361,371 / 854,150 / 18,773 t in 2023); slaughterhouse = 'other' in agriculture (1,059,734 t).
4. **'Specialised waste company' includes informal operators and unsafe disposal** (changes conclusions). GASTAT's footnote defines this column as companies collecting waste for disposal 'whether licensed official companies or informal ones', including selling, open dumping and 'safe and unsafe burial'. The 3.77 Mt of hazardous waste in this column is not all licensed treatment.
5. **Municipal waste treated does not match waste collected** (changes conclusions). Kingdom 2021: treated 19.73 Mt vs collected 23.34 Mt; 2024: treated 26.50 Mt vs collected 25.17 Mt. 17 region-years differ by more than 10%; the worst are Northern Borders 2021 (-51%); Makkah 2024 (+51%); Aseer 2021 (-48%).
6. **Early treatment data looks filled in as "all landfilled"** (use with care). Landfill equals collected exactly, with zero recycling, in 5 regions in 2017, 3 in 2018 and 4 in 2019. Recycling is recorded as 0 in 17 region-years, e.g. Tabuk 2017–2020, Hail and Al-Jouf 2017–2019, Madinah 2023–2024 — more likely missing than zero.
7. **Copied values** (use with care). Madinah 2022 landfill and recycling are identical to 2021 to the gram (925,450.318 t and 41,167 t). Hazardous waste exports are exactly 151,300 t in both 2023 and 2024.
8. **Waste composition by region jumps implausibly** (use with care). 48 cases where one material in one region changes threefold or more in a single year — e.g. Eastern region 'other' 0.42 → 3.02 Mt (2021→22), Eastern plastic 34 kt → 733 kt (2022→23), Riyadh paper 444 → 111 → 614 kt (2021→23), Madinah organic 883 → 186 kt (2019→20). Madinah is now 91% 'other non-organic'.
9. **Outlier regional values** (use with care). Al-Baha: 8.1 kg per person per day (Kingdom 2.1); its collection more than doubled 2019→2020. Riyadh recycling: 23 kt in 2020, 13 t in 2021, 160 kt in 2022.
10. **Early national series is modelled** (use with care). Municipal waste 2010–2014 grows a near-constant 4.22%–4.27% a year, then jumps +32% and +29%. Recycled municipal waste is exactly 15.0% of collected in every year 2010–2015.
11. **GASTAT revised earlier figures between editions** (use with care). Municipal 2023: 19.79 Mt (2023 edition) → 23.98 Mt (2024 edition). Municipal 2017: 25.91 Mt (2021 edition) → 24.21 Mt. Jubail–Yanbu 2018–2021 raised 8–11% between the 2022 and 2023 editions.
12. **Jubail–Yanbu 2024 does not add up** (use with care). Hazardous + non-hazardous = 750,011 t against a total of 766,656 t (16,645 t unassigned). The published recycling rate is 69.3%, but recycled ÷ total = 67.8%. Several values end in thirds (e.g. 891,079.9128333 t), suggesting averaged figures.
13. **Waste trade figures conflict** (use with care). Tables 3-15 and 3-16 carry the same title, 'Waste imports by type'. SEEA trade does not match them (2024 metal waste imports 1.51 Mt vs about 0.17 Mt of metal scrap in 3-15; glass 486 kt vs 3 kt). Tyre exports 1.72 Mt exceed the 234 kt of tyres generated. Hazardous imports went from 64 kt to 1.34 Mt.
14. **Three different 'municipal' totals** (minor). Ministry collection 25.17 Mt; SEEA 'municipal share' 19.2% of total = 25.95 Mt; SEEA household waste 20.54 Mt.
15. **Per-person rates use 2022 population** (minor). The files carry regional population only for the 2022 census. GASTAT's own 2024 national figure is 2.02 kg/day; ours is 2.14.
16. **Labels, spellings and blanks** (minor). Typos and inconsistent terms ('Incineration mothed', 'cycling method', 'Backfilling' for landfill; 'Healthy burial' in 2022 vs 'Sanitary landfilling'); region names vary across editions (Tabouk, Najarn, Al Bahah, Northern Border); the SEEA contents sheet is headed 'SEEA Waste 2023'; the household column of the use table is empty and some cells are blank where others are 0; SEEA 2023 supply and use totals differ by 6 t.
17. **Out of scope** (minor). Wastewater tables 3-1 to 3-7 are excluded (liquid effluent); 3-1 in the 2024 edition still only gives 2021.

### Rules that follow from them
- Never present 2024 SEEA growth (total, hazardous, waste-company tonnage) as measured; it is 2023 scaled by sector factors.
- Present waste-company tonnage as the **upper bound** of EH's market; GASTAT's definition includes informal operators and unsafe burial.
- Read the producing-sector split as GASTAT's allocation, not industry data.
- Do not compare regional recycling for 2017–2019 with later years, or draw material trends by region.
- Do not use the 2010–2015 15% recycling rate as a measured baseline.
- Re-run `pipeline/build_saudi_waste_page.py`: the register on the page is rebuilt from the data, so new editions are re-checked automatically for the rule-based items (treated vs collected, zero recycling, threefold swings, scaling factors, exports above generation).
