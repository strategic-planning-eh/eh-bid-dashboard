# Saudi waste — data problems register

Found by checking every GASTAT table against itself, against the other tables and against earlier editions (Environment Statistics 2021–2024, SEEA Waste 2024). Every figure below is computed from the workbooks by `pipeline/build_saudi_waste_page.py`; the same list is shown at the end of the hub page.

## 1. No regional figures for hazardous or industrial waste — *Changes conclusions*

Hazardous waste (6.91 Mt, 2024) is published only as a national total by producing sector. Industrial waste is published only for Jubail and Yanbu combined (Royal Commission), and nothing for MODON industrial cities. Only 10% of 2024 hazardous waste has a published location.

**On the page:** The map shades municipal waste only; Jubail and Yanbu are shown as points. Nothing is estimated by region. Ask MWAN for regional data.

## 2. 2024 national accounts are mostly 2023 scaled up, not new measurements — *Changes conclusions*

In the SEEA tables, almost every 2024 value equals the 2023 value times one growth factor per sector: mining, manufacturing and utilities ×1.2099 (all waste types), agriculture ×1.3278, other activities ×1.0822, households ×1.0963. Hazardous waste in all four industry sectors ×1.2084, and hazardous waste sent to waste companies ×1.2084.

**On the page:** The +21% rises for total, hazardous and waste-company tonnage are shown as GASTAT projections, not measured market growth.

## 3. Sector split is apportioned with fixed ratios — *Changes conclusions*

For 8 waste types, manufacturing is exactly 2.364 × mining and utilities exactly 0.052 × mining, in both years. Identical tonnages repeat across types: paper = 'other' = mixed waste in the industry sectors (361,371 / 854,150 / 18,773 t in 2023); slaughterhouse = 'other' in agriculture (1,059,734 t).

**On the page:** Producing-sector charts are read as GASTAT's allocation, not as measured tonnage by industry.

## 4. 'Specialised waste company' includes informal operators and unsafe disposal — *Changes conclusions*

GASTAT's footnote defines this column as companies collecting waste for disposal 'whether licensed official companies or informal ones', including selling, open dumping and 'safe and unsafe burial'. The 3.77 Mt of hazardous waste in this column is not all licensed treatment.

**On the page:** EH's market figure is presented as an upper bound, not the licensed market.

## 5. Municipal waste treated does not match waste collected — *Changes conclusions*

Kingdom 2021: treated 19.73 Mt vs collected 23.34 Mt; 2024: treated 26.50 Mt vs collected 25.17 Mt. 17 region-years differ by more than 10%; the worst are Northern Borders 2021 (-51%); Makkah 2024 (+51%); Aseer 2021 (-48%).

**On the page:** Flagged ⚠ per region and year on the map and table; landfill and recycling measures use table 3-10 as published.

## 6. Early treatment data looks filled in as "all landfilled" — *Use with care*

Landfill equals collected exactly, with zero recycling, in 5 regions in 2017, 3 in 2018 and 4 in 2019. Recycling is recorded as 0 in 17 region-years, e.g. Tabuk 2017–2020, Hail and Al-Jouf 2017–2019, Madinah 2023–2024 — more likely missing than zero.

**On the page:** Regional recycling rates for those years are shown but should not be compared with later years.

## 7. Copied values — *Use with care*

Madinah 2022 landfill and recycling are identical to 2021 to the gram (925,450.318 t and 41,167 t). Hazardous waste exports are exactly 151,300 t in both 2023 and 2024.

**On the page:** Shown as published; treated as carried-forward values.

## 8. Waste composition by region jumps implausibly — *Use with care*

48 cases where one material in one region changes threefold or more in a single year — e.g. Eastern region 'other' 0.42 → 3.02 Mt (2021→22), Eastern plastic 34 kt → 733 kt (2022→23), Riyadh paper 444 → 111 → 614 kt (2021→23), Madinah organic 883 → 186 kt (2019→20). Madinah is now 91% 'other non-organic'.

**On the page:** Composition is shown for 2024 only, with Madinah flagged; no material trends by region are drawn.

## 9. Outlier regional values — *Use with care*

Al-Baha: 8.1 kg per person per day (Kingdom 2.1); its collection more than doubled 2019→2020. Riyadh recycling: 23 kt in 2020, 13 t in 2021, 160 kt in 2022.

**On the page:** Flagged on the region panel.

## 10. Early national series is modelled — *Use with care*

Municipal waste 2010–2014 grows a near-constant 4.22%–4.27% a year, then jumps +32% and +29%. Recycled municipal waste is exactly 15.0% of collected in every year 2010–2015.

**On the page:** The '15% to 3.5%' fall compares an assumed rate with measured ones; the page says so.

## 11. GASTAT revised earlier figures between editions — *Use with care*

Municipal 2023: 19.79 Mt (2023 edition) → 23.98 Mt (2024 edition). Municipal 2017: 25.91 Mt (2021 edition) → 24.21 Mt. Jubail–Yanbu 2018–2021 raised 8–11% between the 2022 and 2023 editions.

**On the page:** The 2024 edition is used throughout; older figures quoted elsewhere may differ.

## 12. Jubail–Yanbu 2024 does not add up — *Use with care*

Hazardous + non-hazardous = 750,011 t against a total of 766,656 t (16,645 t unassigned). The published recycling rate is 69.3%, but recycled ÷ total = 67.8%. Several values end in thirds (e.g. 891,079.9128333 t), suggesting averaged figures.

**On the page:** The published rate is shown; the hazardous share uses the published hazardous rows.

## 13. Waste trade figures conflict — *Use with care*

Tables 3-15 and 3-16 carry the same title, 'Waste imports by type'. SEEA trade does not match them (2024 metal waste imports 1.51 Mt vs about 0.17 Mt of metal scrap in 3-15; glass 486 kt vs 3 kt). Tyre exports 1.72 Mt exceed the 234 kt of tyres generated. Hazardous imports went from 64 kt to 1.34 Mt.

**On the page:** Trade is quoted from SEEA only, as a watch item, not as a finding.

## 14. Three different 'municipal' totals — *Minor*

Ministry collection 25.17 Mt; SEEA 'municipal share' 19.2% of total = 25.95 Mt; SEEA household waste 20.54 Mt.

**On the page:** The page uses the Ministry's collection figure for municipal waste.

## 15. Per-person rates use 2022 population — *Minor*

The files carry regional population only for the 2022 census. GASTAT's own 2024 national figure is 2.02 kg/day; ours is 2.14.

**On the page:** Labelled on the map; used for comparing regions, not as an absolute rate.

## 16. Labels, spellings and blanks — *Minor*

Typos and inconsistent terms ('Incineration mothed', 'cycling method', 'Backfilling' for landfill; 'Healthy burial' in 2022 vs 'Sanitary landfilling'); region names vary across editions (Tabouk, Najarn, Al Bahah, Northern Border); the SEEA contents sheet is headed 'SEEA Waste 2023'; the household column of the use table is empty and some cells are blank where others are 0; SEEA 2023 supply and use totals differ by 6 t.

**On the page:** Handled in extraction (names matched to region codes, cells read by position).

## 17. Out of scope — *Minor*

Wastewater tables 3-1 to 3-7 are excluded (liquid effluent); 3-1 in the 2024 edition still only gives 2021.

**On the page:** Sewage sludge is kept, as GASTAT counts it as waste.
