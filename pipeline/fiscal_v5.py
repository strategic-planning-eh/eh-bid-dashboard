# Saudi Government Finances 2026 — version 5 (01/10/2026). Text for patch_fiscal_v5.py. Plain language, same page structure.
S = {}
S['nav'] = '''<body>

<!-- ============ STICKY NAV ============ -->
<div class="topnav">
  <div class="wrap">
    <div class="brand"><img id="navlogo" alt="EH"><span>EH&nbsp;·&nbsp;Strategic Planning</span><span class="vtag">Version 5 · 01/10/2026 · after the 2027 pre-budget statement</span></div>
    <nav>
      <a href="#overview">Summary</a>
      <a href="#kpis">Key figures</a>
      <a href="#compare">Plan vs actual</a>
      <a href="#projection">Year-end outlook</a>
      <a href="#scenarios">What could happen</a>
      <a href="#v2030impact">Vision 2030 projects</a>
      <a href="#ehplan">What EH should do</a>
      <a href="#sources">Sources</a>
    </nav>
  </div>
</div>

'''
S['1'] = '''<!-- ============ SECTION 1 — HEADER ============ -->
<header class="hero" id="overview">
  <div class="wrap">
    <div class="badge-row">
      <span class="ctx-badge">Saudi government finances · 2026</span>
      <span class="ctx-badge upd">New: the Ministry of Finance now expects a SAR 245 billion gap for 2026</span>
      <span class="ctx-badge war">Bab el-Mandeb in Houthi hands since 11/09 · pipeline to Yanbu shut 11–22/09</span>
    </div>
    <h1>Saudi Government Finances 2026: the Red Sea Route Is Cut — What It Means for the Budget and Vision 2030</h1>
    <p class="sub">Version 5. September brought the two events version 4 called the worst case. The Houthis took Yemen's whole Red Sea coast and the Bab el-Mandeb strait (10–11/09) and say the strait is closed to Saudi ships. Drones then knocked out the pipeline that carries Saudi oil from the east of the country to Yanbu on the Red Sea, shutting it for about ten days. Saudi oil still got out — mostly back through the Strait of Hormuz, now crossed in convoys escorted by the US Navy. On 30/09 the Ministry of Finance published its first official view of the damage: it now expects the government to spend <b>SAR 245 billion</b> more than it earns in 2026, against the SAR 165.4 billion planned, and the economy to <b>shrink by 3.6%</b> this year.</p>
    <div class="meta">
      <span>Figures as of <b>30/09/2026</b></span>
      <span>Amounts in <b>billions of Saudi riyals</b> unless stated</span>
      <span>Main sources: <b>Ministry of Finance (2027 pre-budget statement) · Reuters · shipping-data firms</b></span>
      <span>Replaces: <b>version 4 of 26/08/2026</b></span>
    </div>

    <div class="ctx-note">
      <b>What the Ministry of Finance said on 30/09.</b> In its pre-budget statement for 2027 the Ministry estimates that 2026 will end with a gap of <b>SAR 245 billion</b> between spending and income — 48% more than the SAR 165.4 billion in this year's budget. It expects the economy to <b>shrink by 3.6% in 2026</b> and then grow by <b>12.8% in 2027</b> as oil exports recover. For 2027 it plans spending of <b>SAR 1,392 billion</b> and income of <b>SAR 1,202 billion</b>: a gap of about <b>SAR 190 billion (3.6% of the size of the economy)</b>, to be covered by borrowing. Spending is planned to keep rising to SAR 1,544 billion by 2029, so the government is not cutting back overall — it is choosing which projects get the money.
      <br><br><span class="rev">▼ What happened in September.</span> On 10–11/09 drones hit the East–West pipeline, which carries Saudi oil 1,200 km from the eastern oilfields to Yanbu. Saudi and Iraqi officials say they were launched from southern Iraq. Before the attack the pipeline moved about 5.5 million barrels a day, most of it for export from Yanbu. It was shut completely by 13/09 and restarted at a low rate on <b>22/09</b>; satellite images show tankers loading at Yanbu again by 27/09. In the same days the Houthis took the port of Mokha, Perim island in the middle of the Bab el-Mandeb strait and the rest of Yemen's Red Sea coast, and said the strait is open to everyone except Saudi Arabia. Saudi-linked tankers now avoid the southern Red Sea: oil loaded at Yanbu goes north through the Suez Canal or the SUMED pipeline across Egypt, or round Africa. The world oil price (Brent) jumped to <b>$107.6 on 10/09</b> and peaked at $108.8 on 15/09, then eased to <b>$97.5 on 30/09</b> as convoys through Hormuz brought Gulf exports back close to pre-war levels.
      <br><br><span class="corr">⚠ How our estimate changes.</span> Version 4 expected about SAR 290–330 billion for the year. Two things pull that down: oil prices in September were about $100 instead of the $85–95 we assumed, and exports did not collapse because the Hormuz convoys took over when the Yanbu route failed. Our middle estimate is now <b>SAR 245–280 billion (about 5.0–5.7% of the size of the economy)</b>, with the Ministry's own figure at the bottom of the range. We do not go lower than the Ministry because last September it also estimated SAR 245 billion for 2025, and the year finally ended at SAR 276.6 billion — 13% higher.
    </div>

    <div class="prov-legend">
      <span style="font-weight:700;color:#e7f0f8">Where each figure comes from:</span>
      <span class="item"><span class="dot off"></span>Official — Ministry of Finance, Ministry of Energy, National Debt Management Center</span>
      <span class="item"><span class="dot an"></span>Analysts, markets and news agencies — named</span>
      <span class="item"><span class="dot sc"></span>EH's own estimate — built on official figures</span>
    </div>
  </div>
</header>

'''
S['2'] = '''<!-- ============ SECTION 2 — KPI CARDS ============ -->
<section id="kpis">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 02</span><h2>Key figures</h2><span class="upd-chip">Ministry of Finance 30/09 · market figures to 30/09</span></div>
    <p class="sec-sub">The 2027 pre-budget statement (30/09) is the newest official data. The oil and shipping cards show the position at the end of September 2026.</p>
    <div class="kpi-grid" id="kpiGrid"></div>
  </div>
</section>

'''
S['4'] = '''<!-- ============ SECTION 4 — PROJECTION ============ -->
<section id="projection">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 04</span><h2>How 2026 could end</h2><span class="upd-chip warn">Ministry of Finance year-end estimate added · Red Sea route cut</span></div>
    <p class="sec-sub">The Ministry's new year-end estimate (SAR 245 billion) now sits alongside the two official half-year figures. Three paths for October–December: the Red Sea stays closed to Saudi ships while the Hormuz convoys keep running (most likely); a deal calms both straits; or the convoys stop while the Red Sea is still closed — the case in which Saudi Arabia has no safe way left to export oil by sea.</p>
    <div class="chart-grid">

      <div class="card full">
        <div class="chead">
          <div><h3>E · World oil price (Brent) — 2026 so far and three paths for October–December</h3>
          <p class="csub">Monthly average price, approximate. September averaged about $100: the pipeline attack pushed it to $107.6 on 10/09 and $108.8 on 15/09, then it settled at $97.5 on 30/09 as Gulf oil flowed again through Hormuz under US escort.</p></div>
          <div style="display:flex;gap:6px"><span class="tag an">Market prices</span><span class="tag sc">EH paths · Oct–Dec</span></div>
        </div>
        <div class="chart-box tall"><canvas id="chartE"></canvas></div>
        <div class="callout">The price now reacts less to Saudi news than in the spring, because the world is getting Gulf oil again through the Hormuz convoys. For the budget, what matters is no longer the price alone but whether Saudi barrels can reach buyers: through Hormuz under escort, or from Yanbu northwards through Suez. Both routes are working today; both depend on things Riyadh does not control.</div>
        <div class="csrc"><span class="tag an">Sources</span> Brent closing prices from Investing.com (September 2026). The OPEC+ group (OPEC producers plus Russia and others) kept production limits unchanged for October at its meeting on 06/09; it meets again on 04/10. The October–December lines are EH's own.</div>
      </div>

      <div class="card full">
        <div class="chead">
          <div><h3>F · The 2026 gap between spending and income — three possible paths</h3>
          <p class="csub">Two official figures (end of March: SAR 125.7 billion; end of June: SAR 160.0 billion), the Ministry of Finance's year-end estimate (SAR 245 billion, published 30/09), and three EH paths. The end-of-September points are EH's illustration; the year-end points are the middle of each path's range.</p></div>
          <div style="display:flex;gap:6px"><span class="tag off">Official figures + Ministry estimate</span><span class="tag sc">EH paths</span></div>
        </div>
        <div class="chart-box"><canvas id="chartF"></canvas></div>
        <div class="callout blue"><b>How we got our estimate:</b> January–June = SAR 160.0 billion (official). The Ministry's SAR 245 billion means it expects only about SAR 85 billion more in July–December — half of what the same months cost in 2025 (SAR 183.9 billion). That is possible with oil near $100 and exports restored, but it leaves no room for the usual end-of-year rush of payments, for war spending, or for another pipeline outage. Last year the Ministry's September estimate was 13% too low. Our most likely range is therefore <b>SAR 245–280 billion</b>; a calmer path would land close to the Ministry's figure; losing both export routes at once would push the year above SAR 290 billion.</div>
        <div class="csrc"><span class="tag off">Official figures</span> End of March, end of June, the 2025 result and the 2026 plan: Ministry of Finance budget reports. Year-end estimate: Ministry of Finance, 2027 pre-budget statement (30/09/2026). <span class="tag sc">Paths</span> EH's own.</div>
      </div>

    </div>
  </div>
</section>

'''
S['5'] = '''<!-- ============ SECTION 5 — SCENARIO TABLE ============ -->
<section id="scenarios">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 05</span><h2>What could happen in October–December 2026</h2><span class="upd-chip warn">Fifth update · two export routes, both under threat</span></div>
    <p class="sec-sub">Percentages are of the size of the Saudi economy in 2026, taken as about SAR 4.9 trillion (EH's approximation: the pre-war SAR 5.0 trillion adjusted for the Ministry's expected 3.6% fall in output and higher oil prices). Every row is EH's own estimate, built on the official January–June figure and the Ministry's year-end estimate.</p>
    <div class="tbl-wrap">
      <table class="scen">
        <thead>
          <tr>
            <th>What happens</th><th>Oil price (Oct–Dec)</th><th>Gap for the year<br>(SAR billion)</th><th>Gap as % of<br>the economy</th><th>Risk to Vision 2030<br>building projects</th><th>What we assume</th><th>Likelihood<br>(EH estimate)</th>
          </tr>
        </thead>
        <tbody id="scenBody"></tbody>
      </table>
    </div>
    <div class="callout red" style="margin-top:16px"><b>Both of Saudi Arabia's sea exits are now in play.</b> The Houthis took Mokha (10/09), then Perim island in the middle of the Bab el-Mandeb strait and the rest of Yemen's Red Sea coast (11/09); Yemeni government forces say they won back some ground near the strait on 13/09. The Houthis say ships of every country except Saudi Arabia may pass. Meanwhile the East–West pipeline to Yanbu was attacked 10–11/09 and shut for about ten days, and the Houthis said they also targeted Aramco sites at Yanbu on 16/09 and 19/09. While the pipeline was down, Saudi oil went out through Hormuz in US-escorted convoys — which shows the convoys now matter as much to the Saudi budget as the Red Sea route.</div>
    <div class="callout blue" style="margin-top:10px"><b>What would make us change this view.</b> A US–Iran agreement on Hormuz, or a Saudi–Houthi truce, moves us to the calmer path. The convoys stopping, or another long pipeline outage while the Red Sea is still closed, moves us to the worst path. Dates to watch: <b>OPEC+ meeting on 04/10</b>, the <b>Ministry of Finance's July–September report (around the end of October)</b>, the <b>2027 budget (December)</b>, and the 2027 borrowing plan the Ministry will publish by year-end.</div>
  </div>
</section>

<!-- ============ SECTION 5B — VISION 2030 PROJECTS ============ -->
<section id="v2030impact">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 06</span><h2>What this means for Vision 2030 projects</h2><span class="upd-chip warn">EH assessment · 01/10/2026</span></div>
    <p class="sec-sub">The war hits Vision 2030 projects in three ways. <b>Money:</b> a SAR 245 billion gap this year and borrowing again next year mean the government and the Public Investment Fund (PIF) pay for fewer things at once — and the Ministry says spending will go to projects with "economic and social returns". <b>Shipping:</b> with Bab el-Mandeb closed to Saudi ships, building materials and equipment coming from Asia can no longer sail straight into Red Sea ports such as Jeddah, King Abdullah Port and NEOM; they come round through Suez or land at Gulf ports and cross the country by road and rail, which adds weeks and cost. <b>Safety:</b> projects on the Red Sea coast are now near a war zone, which hurts tourism demand and raises insurance costs. The table ranks the 31 projects tracked on the hub's Vision 2030 page by how much these three things hurt them. The ranking is EH's judgement, not an official list.</p>
    <div class="tbl-wrap">
      <table class="scen">
        <thead><tr><th>Project</th><th>Where</th><th>Money</th><th>Shipping</th><th>Safety</th><th>Overall risk</th><th>Why</th></tr></thead>
        <tbody>
          <tr class="pess"><td class="sname">NEOM — Oxagon, NEOM Port, Sindalah</td><td>Red Sea coast, Tabuk</td><td>High</td><td>High</td><td>High</td><td><span class="riskpill high">Most affected</span></td><td>The Line and Trojena were already on hold and spending frozen for review. What was still moving — the port, Oxagon's industry, Sindalah's resort — depends on ships reaching the northern Red Sea and on visitors feeling safe there.</td></tr>
          <tr class="pess"><td class="sname">NEOM Green Hydrogen Company</td><td>Red Sea coast, Tabuk</td><td>Medium</td><td>High</td><td>High</td><td><span class="riskpill high">Most affected</span></td><td>About 90% built, with first exports aimed for late 2026 to 2027. Its ammonia was meant to leave by sea through the Red Sea; buyers in Asia are now cut off by Bab el-Mandeb, so start-up or sales are likely to slip.</td></tr>
          <tr class="pess"><td class="sname">Red Sea Global (The Red Sea and AMAALA)</td><td>Red Sea coast, Tabuk</td><td>High</td><td>Medium</td><td>High</td><td><span class="riskpill high">Most affected</span></td><td>Luxury tourism on a coast next to a war at sea. Work on phase 2 was already reported paused in February; open resorts face cancellations and new openings are likely to be pushed back.</td></tr>
          <tr class="pess"><td class="sname">King Abdullah Economic City, King Abdullah Port, and the car plants there (Lucid, Ceer, Hyundai)</td><td>Red Sea coast, Rabigh</td><td>Medium</td><td>High</td><td>Medium</td><td><span class="riskpill high">High</span></td><td>The car plants need parts shipped from Asia through Bab el-Mandeb, and King Abdullah Port lives on Red Sea traffic. Expect slower start-ups in 2026–2027 and parts brought in through Gulf ports instead.</td></tr>
          <tr class="base"><td class="sname">New Murabba (Mukaab)</td><td>Riyadh</td><td>High</td><td>Low</td><td>Low</td><td><span class="riskpill mod">Medium–high</span></td><td>Safe from the Red Sea, but it is a PIF-funded project with a 2040 finish and no fixed event deadline, which makes it one of the easiest to slow when money is tight.</td></tr>
          <tr class="base"><td class="sname">ROSHN and SEDRA housing</td><td>Riyadh and other cities</td><td>Medium</td><td>Low</td><td>Low</td><td><span class="riskpill mod">Medium</span></td><td>Housing for Saudi families is a political priority and SEDRA is delivering homes, but new phases depend on PIF money and bank lending.</td></tr>
          <tr class="base"><td class="sname">SATORP / Amiral expansion (Jubail)</td><td>Gulf coast</td><td>Medium</td><td>Medium</td><td>Medium</td><td><span class="riskpill mod">Medium</span></td><td>Paid for by Aramco and TotalEnergies rather than the budget, but Aramco is under pressure, and the Gulf coast is within reach of Iranian attacks.</td></tr>
          <tr class="base"><td class="sname">Saudi Green Initiative (tree planting, nature reserves)</td><td>Nationwide</td><td>Medium</td><td>Low</td><td>Low</td><td><span class="riskpill mod">Medium</span></td><td>Long-term government programme that can be slowed without anyone noticing quickly — a typical place to save money in a bad year.</td></tr>
          <tr class="base"><td class="sname">Industrial cities on the Red Sea (Yanbu, Jeddah, Rabigh)</td><td>Red Sea coast</td><td>Low</td><td>High</td><td>High</td><td><span class="riskpill mod">Medium</span></td><td>Refineries and chemical plants keep running, but Yanbu has been targeted three times in September and imports by sea now take longer.</td></tr>
          <tr class="opt"><td class="sname">Diriyah</td><td>Riyadh</td><td>Medium</td><td>Low</td><td>Low</td><td><span class="riskpill low">Lower</span></td><td>Heritage site with steady contract awards and visitors already coming; likely to keep going, possibly more slowly.</td></tr>
          <tr class="opt"><td class="sname">Qiddiya and King Salman Park</td><td>Riyadh</td><td>Medium</td><td>Low</td><td>Low</td><td><span class="riskpill low">Lower</span></td><td>Tied to fixed dates — the 2034 FIFA World Cup and opening commitments — which protects them when other projects are slowed.</td></tr>
          <tr class="opt"><td class="sname">Jafurah gas field, Ma'aden, SABIC, desalination plants, Jubail and Ras Al-Khair industry</td><td>Mostly Gulf coast and inland</td><td>Low</td><td>Medium</td><td>Medium</td><td><span class="riskpill low">Lower</span></td><td>These earn money or keep the country running. Jafurah's gas lets Saudi Arabia burn less oil at home and export more, so it gains priority.</td></tr>
          <tr class="opt"><td class="sname">Special Integrated Logistics Zone (Riyadh) and land routes between the Gulf and the Red Sea</td><td>Riyadh, inland</td><td>Low</td><td>Low</td><td>Low</td><td><span class="riskpill low">May gain</span></td><td>When ships cannot use Bab el-Mandeb, goods cross Saudi Arabia by road and rail instead. Inland logistics is one of the few areas likely to get more work, not less.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout" style="margin-top:14px"><b>The pattern.</b> The projects most likely to be slowed share three features: they sit on the Red Sea coast, they depend on PIF money rather than earning their own, and they have no fixed event date. Projects in Riyadh tied to the World Cup or Expo 2030, and projects that earn money or save oil, are the most protected. This matches what the government had already started doing before the war — PIF's 2026–2030 strategy moved money toward AI, mining and logistics — and the war speeds it up.</div>
  </div>
</section>

<!-- ============ SECTION 5C — WHAT EH SHOULD DO ============ -->
<section id="ehplan">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 07</span><h2>What EH should do</h2><span class="upd-chip">Business Development proposal · for management discussion</span></div>
    <p class="sec-sub">These are Business Development's proposals for EH, based on the analysis above. They are recommendations for discussion, not decisions.</p>
    <div class="chart-grid">
      <div class="card"><div class="chead"><div><h3>1 · Protect cash</h3></div></div>
        <div class="callout red">A government running a SAR 245–280 billion gap tends to pay its suppliers later. Review money owed to EH by government bodies and PIF projects, ask for advance or milestone payments on new contracts with Red Sea tourism and NEOM projects, and give priority to clients that earn their own revenue — Aramco and its joint ventures, SABIC, Ma'aden, the refineries.</div></div>
      <div class="card"><div class="chead"><div><h3>2 · Move the bid pipeline</h3></div></div>
        <div class="callout blue">Shift bidding effort toward the projects in the "Lower" and "May gain" rows: Riyadh projects tied to the World Cup and Expo 2030, Gulf-coast industry (Jubail, Ras Al-Khair, Jafurah), desalination and inland logistics. Treat new bids for the projects in the "Most affected" rows as higher-risk unless payment terms are secure.</div></div>
      <div class="card"><div class="chead"><div><h3>3 · Be ready for spills and clean-up on the Red Sea coast</h3></div></div>
        <div class="callout green">Attacks on tankers near Yanbu and on the pipeline raise the risk of oil spills and contaminated ground — work EH can do. Confirm EH is on the response lists of Aramco, the Saudi Ports Authority (Mawani) and the National Center for Environmental Compliance (NCEC) for the Yanbu–Jeddah–Rabigh coast, and check equipment and crews are ready to move.</div></div>
      <div class="card"><div class="chead"><div><h3>4 · Secure EH's own supplies</h3></div></div>
        <div class="callout">Drums, protective equipment, chemicals and spare parts shipped from Asia to Jeddah now take longer and cost more. Hold more stock of critical items, look for Saudi-made alternatives, and use Dammam or Jubail with a road leg to the west when Red Sea ports are slow.</div></div>
    </div>
  </div>
</section>

'''
S['6_head'] = ('<p class="sec-sub">Every figure comes from one of the organisations below. Official government data counts most; figures from analysts, markets and EH\'s own estimates are labelled as such throughout.</p>',
 '<p class="sec-sub">Every figure comes from one of the organisations below. Official government data counts most; figures from analysts, markets and EH\'s own estimates are labelled as such throughout. Version 5 adds the Ministry of Finance\'s 2027 pre-budget statement (30/09) and September\'s reporting on the pipeline attack and the Houthi advance.</p>')
S['6_method'] = '''    <div class="disclaimer">
      <b>How this page was put together (version 5).</b> The January–June figures are official Ministry of Finance data from its April–June budget report (30/07/2026). The 2026 year-end estimate (SAR 245 billion), the 2027 plan, and the 2026 and 2027 growth figures are official Ministry of Finance estimates from the 2027 pre-budget statement (30/09/2026), as reported by Arab News, Saudi Gazette, Zawya (Reuters) and Arabian Business; the full statement document should be checked when it is posted on the Ministry's website. The 2026 ranges (most likely SAR 245–280 billion) are <b>EH's own estimates</b>: the official January–June figure plus a July–December path, compared with July–December 2025 (SAR 183.9 billion) and with the gap between the Ministry's September 2025 estimate for 2025 (SAR 245 billion) and the final 2025 result (SAR 276.6 billion). The size of the economy used for percentages (about SAR 4.9 trillion) is EH's approximation. Dates for the pipeline attack differ slightly between sources (attacks on 10–11/09; full shutdown by 13/09; restart 22/09). Who launched the drones is disputed: Saudi and Iraqi authorities point to southern Iraq; the group named denies it. September oil prices are futures closing prices; the September average (about $100) is approximate because closes for 01–08/09 were estimated. The Vision 2030 risk ranking and the recommendations for EH are Business Development's judgement and should be read as such. The war is moving fast: figures dated 30/09/2026 may be out of date quickly.
    </div>
'''
S['7'] = '''<!-- ============ SECTION 7 — FOOTER ============ -->
<footer>
  <div class="wrap">
    <div class="frow">
      <div style="max-width:620px">
        <div style="font-family:'Fraunces',serif;font-size:17px;color:#fff;margin-bottom:8px">Saudi Government Finances 2026 — version 5</div>
        <div>Prepared for <b>EH management</b></div>
        <div style="margin-top:10px;color:#9fb6cb">Version 5 prepared on 01/10/2026 · replaces version 4 (26/08/2026), version 3 (19/07/2026), version 2 (07/07/2026) and version 1 (28/06/2026) · Environmental Horizons — Strategic Planning, Business Development.<br>Official budget figures are from the Ministry of Finance (April–June report of 30/07 and 2027 pre-budget statement of 30/09); oil and shipping figures as of 30/09/2026. The next update comes with the Ministry's July–September report (around the end of October), the 2027 budget in December, a Hormuz or Red Sea agreement, or another major attack on Saudi export routes — whichever comes first.</div>
      </div>
      <div>
        <div style="color:#fff;font-weight:700;margin-bottom:8px">Main sources</div>
        <ul>
          <li>Saudi Ministry of Finance — 2027 pre-budget statement (30/09/2026) and April–June 2026 budget report (30/07/2026)</li>
          <li>Saudi Ministry of Energy — statement on the East–West pipeline attack (September 2026)</li>
          <li>Reuters, Seatrade Maritime, OilPrice.com, Rigzone — pipeline shutdown, restart and Yanbu loadings</li>
          <li>Euronews, Al Jazeera, FDD's Long War Journal, CBS News — the Houthi advance on Bab el-Mandeb</li>
          <li>CNBC — Gulf oil flows through Hormuz under US escort (30/09/2026)</li>
          <li>OPEC — statement of 06/09/2026 · Investing.com — Brent prices</li>
          <li>AFP, AGBI, MEED — earlier reporting on NEOM and Red Sea Global spending</li>
        </ul>
      </div>
    </div>
  </div>
</footer>


'''
KPIS = r'''const KPIS = [
  {label:'Expected gap for 2026 (Ministry of Finance)', val:'245', unit:'B', cls:'red', delta:'48% above the SAR 165.4 billion plan · EH most likely: 245–280', dcls:'down', src:'Ministry of Finance · 2027 pre-budget statement (30/09)'},
  {label:'Planned gap for 2027', val:'~190', unit:'B', cls:'amber', delta:'3.6% of the economy · spending 1,392 · income 1,202 · to be borrowed', dcls:'warn', src:'Ministry of Finance · 2027 pre-budget statement (30/09)'},
  {label:'Size of the economy, 2026', val:'\u22123.6', unit:'%', cls:'red', delta:'Ministry expects a 12.8% rebound in 2027 if exports recover', dcls:'down', src:'Ministry of Finance · preliminary estimate (30/09)'},
  {label:'World oil price (Brent) — close on 30/09', val:'97.5', unit:'$/barrel', cls:'amber', delta:'September average about $100 · peak $108.8 on 15/09', dcls:'warn', src:'Investing.com · Brent futures'},
  {label:'Pipeline to Yanbu', val:'~10', unit:'days shut', cls:'red', delta:'Attacked 10\u201311/09 · restarted 22/09 at a low rate · Yanbu loading again by 27/09', dcls:'down', src:'Saudi Ministry of Energy; Reuters; Seatrade Maritime'},
  {label:'Bab el-Mandeb strait', val:'Closed', unit:'to Saudi ships', cls:'red', delta:'Houthis hold Yemen\u2019s whole Red Sea coast and Perim island since 11/09', dcls:'down', src:'Euronews, Al Jazeera, FDD Long War Journal'},
  {label:'Gulf oil through Hormuz', val:'Near pre-war', unit:'', cls:'amber', delta:'Moving in US-escorted convoys \u2014 tankers still come under fire', dcls:'warn', src:'CNBC (30/09)'},
  {label:'Government debt (end of June)', val:'1,685', unit:'B', cls:'amber', delta:'More borrowing to come: the 2027 gap will also be borrowed', dcls:'warn', src:'Ministry of Finance \u00b7 borrowing plan for 2027 due by year-end'}
];'''
SCEN = r'''const SCEN = [
  {cls:'base', name:'Most likely \u2014 Red Sea closed to Saudi ships, Hormuz convoys keep running', oil:'$90\u2013105', def:'~245\u2013280', pct:'~5.0\u20135.7%', risk:['high','High on the Red Sea coast'], assum:'Yanbu loads again but its tankers go north through Suez or round Africa; most exports leave through Hormuz under US escort; the pipeline suffers short interruptions but no long outage; the usual end-of-year spending peak happens. The Ministry\u2019s SAR 245 billion is the bottom of the range.', prob:'55%', basis:'EH estimate \u00b7 official Jan\u2013Jun figure, Ministry year-end estimate, and the 13% overrun of the Ministry\u2019s 2025 estimate'},
  {cls:'opt', name:'Calmer \u2014 a deal eases Hormuz and the Red Sea', oil:'$75\u201390', def:'~235\u2013255', pct:'~4.8\u20135.2%', risk:['mod','Medium'], assum:'A US\u2013Iran agreement or a Saudi\u2013Houthi truce lets tankers move without escort; prices fall but more barrels are sold; war spending eases. The year ends close to the Ministry\u2019s estimate.', prob:'20%', basis:'EH estimate \u00b7 talks continuing in late September'},
  {cls:'pess', name:'Worst \u2014 convoys stop while the Red Sea stays closed', oil:'above $110 spike*', def:'~290\u2013340', pct:'~5.9\u20136.9%', risk:['high','Severe'], assum:'The Hormuz convoys are halted or the pipeline is knocked out again for weeks while Bab el-Mandeb remains closed. Prices jump but Saudi oil cannot reach buyers \u2014 income falls while spending rises. *High price, very little oil sold.', prob:'25%', basis:'EH estimate \u00b7 based on the September pipeline outage and the Houthi hold on the strait'}
];'''
SRC_ADD = r'''  {bg:'#7A1F1F', ini:'SEP', name:'September 2026 \u2014 pipeline attack and Houthi advance', date:'10/09 \u2013 30/09/2026', head:'East\u2013West pipeline shut about ten days; Houthis hold Bab el-Mandeb; Yanbu loading again by 27/09.', desc:'Saudi Ministry of Energy: the pipeline was attacked on the morning of 10/09 and shut as a precaution. Reuters: restarted on 22/09 at a low rate. Seatrade Maritime: about 10 million barrels seen loading at Yanbu and Al Muajjiz on 27/09; Saudi-linked tankers avoid the southern Red Sea. Euronews / Al Jazeera / FDD: Houthis took Mokha (10/09) and Perim island (11/09). CNBC (30/09): Gulf crude flows through Hormuz near pre-war levels under US escort.'},
  {bg:'#0A2A43', ini:'PBS', name:'Ministry of Finance \u2014 2027 pre-budget statement', date:'30/09/2026', head:'2026 gap now expected at SAR 245 billion; economy \u22123.6% in 2026, +12.8% in 2027; 2027 gap about SAR 190 billion.', desc:'Spending SAR 1,392 billion and income SAR 1,202 billion in 2027, rising to SAR 1,544 billion and SAR 1,351 billion by 2029. The 2027 gap will be borrowed under the medium-term debt plan, with details by year-end. As reported by Arab News, Saudi Gazette, Zawya (Reuters) and Arabian Business.'},
'''
CHART_E = [
 ("const actual=[73,71,85,105,92,82,85,92,null,null,null,null];\nconst baseS=[null,null,null,null,null,null,null,92,88,86,85,84];\nconst escS =[null,null,null,null,null,null,null,92,105,115,112,108];\nconst deeS =[null,null,null,null,null,null,null,92,82,77,74,72];",
  "const actual=[73,71,85,105,92,82,85,92,100,null,null,null];\n/* Sep \u2248 $100: futures closes 09\u201330/09 (101.2 \u2192 107.6 on 10/09 \u2192 108.8 on 15/09 \u2192 97.5 on 30/09); 01\u201308/09 approximate. */\nconst baseS=[null,null,null,null,null,null,null,null,100,98,96,94];\nconst escS =[null,null,null,null,null,null,null,null,100,112,118,112];\nconst deeS =[null,null,null,null,null,null,null,null,100,90,84,80];"),
 ("label:'Oil price so far (approx.; August = average to 25/08)'", "label:'Oil price so far (monthly average, approximate)'"),
 ("label:'Jul–Dec · most likely: long war ($85–95)'", "label:'Oct–Dec · most likely: Red Sea closed, convoys run ($90–105)'"),
 ("label:'Jul–Dec · worst: Yanbu route cut (spike above $110)'", "label:'Oct–Dec · worst: convoys stop too (spike above $110)'"),
 ("label:'Jul–Dec · calmer: Hormuz deal ($72–80)'", "label:'Oct–Dec · calmer: a deal eases both straits ($75–90)'"),
 ("        {x:6.8,label:'Red Sea attacks · 25 Jul',color:'#8B0000',yOff:42}\n", "        {x:6.8,label:'Red Sea attacks · 25 Jul',color:'#8B0000',yOff:42},\n        {x:8.3,label:'Pipeline hit · Houthis take Bab el-Mandeb · 10–11 Sep',color:'#8B0000',yOff:12}\n"),
]
CHART_F = [
 ("const fActual=[-125.7,-160.0,null,null];\n/* Q3 waypoints are EH-illustrative; year-ends are scenario range midpoints. */\nconst fBase=[-125.7,-160.0,-222,-310];\nconst fEsc =[-125.7,-160.0,-238,-355];\nconst fDee =[-125.7,-160.0,-212,-275];",
  "const fActual=[-125.7,-160.0,null,null];\n/* v5: end-of-September points are EH-illustrative; year-ends are the middle of each path's range; MoF = 2027 pre-budget statement estimate (30/09). */\nconst fBase=[-125.7,-160.0,-200,-262];\nconst fEsc =[-125.7,-160.0,-212,-315];\nconst fDee =[-125.7,-160.0,-195,-245];\nconst fMoF=[null,null,null,-245];"),
 ("    {label:'Most likely · long war — year ~310', data:fBase,", "    {label:'Ministry of Finance year-end estimate (\\u2212245, 30/09)', data:fMoF, borderColor:C.navy, backgroundColor:'#fff', borderWidth:3, pointRadius:7, pointHoverRadius:8, pointStyle:'circle', showLine:false},\n    {label:'Most likely · Red Sea closed, convoys run — year ~262', data:fBase,"),
 ("{label:'Worst · Yanbu route cut — year ~355', data:fEsc,", "{label:'Worst · convoys stop too — year ~315', data:fEsc,"),
 ("{label:'Calmer · Hormuz deal — year ~275', data:fDee,", "{label:'Calmer · a deal eases both straits — year ~245', data:fDee,"),
 ("footer:items=>{const i=items[0].dataIndex; return i<=1?'Official Ministry of Finance figure':(i===3?'Year-end = middle of the range for this path':'End of September: EH illustration');}",
  "footer:items=>{const i=items[0].dataIndex; return i<=1?'Official Ministry of Finance figure':(i===3?'Year-end: Ministry estimate, or the middle of the range for an EH path':'End of September: EH illustration');}"),
]
TITLE = ('<title>Saudi Government Finances 2026 — mid-year position and the Red Sea attacks</title>', '<title>Saudi Government Finances 2026 — version 5: the Red Sea route cut, the budget and Vision 2030</title>')
AR_VIEW = '''<div id="ehArView" dir="rtl" lang="ar">
<div class="avnote">آفاق البيئة · التخطيط الاستراتيجي — الإصدار الخامس · 01/10/2026 · بعد بيان ميزانية 2027 المبدئي</div>
<h1>مالية الحكومة السعودية 2026: انقطاع طريق البحر الأحمر — ماذا يعني للميزانية ولرؤية 2030</h1>
<p><b>الإصدار الخامس.</b> حمل سبتمبر الحدثين اللذين وصفهما الإصدار الرابع بأسوأ الاحتمالات. سيطر الحوثيون على كامل ساحل اليمن على البحر الأحمر وعلى مضيق باب المندب (10–11/09) وأعلنوا إغلاقه أمام السفن السعودية. ثم عطّلت طائرات مسيّرة خط الأنابيب الذي ينقل النفط السعودي من شرق المملكة إلى ينبع على البحر الأحمر، فتوقّف نحو عشرة أيام. ومع ذلك استمر خروج النفط السعودي — في معظمه عبر مضيق هرمز، الذي تعبره الناقلات الآن في قوافل ترافقها البحرية الأمريكية. وفي 30/09 نشرت وزارة المالية أول تقدير رسمي للأثر: تتوقع الآن أن تنفق الحكومة <b>245 مليار ريال</b> أكثر مما تجني في 2026، مقابل 165.4 مليارًا في الخطة، وأن <b>ينكمش الاقتصاد 3.6%</b> هذا العام.</p>
<div class="avc"><b>ما قالته وزارة المالية في 30/09.</b> في البيان المبدئي لميزانية 2027 تقدّر الوزارة أن ينتهي 2026 بفجوة <b>245 مليار ريال</b> بين الإنفاق والدخل — أعلى بـ48% من خطة العام. وتتوقع انكماش الاقتصاد <b>3.6% في 2026</b> ثم نموه <b>12.8% في 2027</b> مع تعافي الصادرات. وتخطط لعام 2027 لإنفاق <b>1,392 مليار ريال</b> ودخل <b>1,202 مليار</b>، أي فجوة نحو <b>190 مليار ريال (3.6% من حجم الاقتصاد)</b> تُغطّى بالاقتراض. ويرتفع الإنفاق المخطط إلى 1,544 مليارًا بحلول 2029؛ فالحكومة لا تقلّص الإنفاق إجمالًا، بل تختار المشاريع التي تحصل على المال.</div>
<div class="avred"><b>▼ ما حدث في سبتمبر.</b> في 10–11/09 ضربت طائرات مسيّرة خط شرق–غرب الذي ينقل النفط 1,200 كيلومتر من حقول الشرق إلى ينبع؛ ويقول مسؤولون سعوديون وعراقيون إنها أُطلقت من جنوب العراق. كان الخط ينقل قبل الهجوم نحو 5.5 مليون برميل يوميًا معظمها للتصدير من ينبع. أُوقف كليًا بحلول 13/09 وأُعيد تشغيله بمعدل منخفض في <b>22/09</b>، وتُظهر صور الأقمار الصناعية تحميل الناقلات في ينبع من جديد بحلول 27/09. وفي الأيام نفسها أخذ الحوثيون ميناء المخا وجزيرة ميون في وسط باب المندب وبقية الساحل، وقالوا إن المضيق مفتوح للجميع إلا السعودية. صارت الناقلات المرتبطة بالسعودية تتجنب جنوب البحر الأحمر: يتجه نفط ينبع شمالًا عبر قناة السويس أو خط سوميد في مصر، أو يلتف حول أفريقيا. قفز سعر النفط العالمي (برنت) إلى <b>107.6 دولارًا في 10/09</b> وبلغ ذروته 108.8 في 15/09، ثم تراجع إلى <b>97.5 دولارًا في 30/09</b> مع عودة صادرات الخليج قرب مستويات ما قبل الحرب عبر قوافل هرمز.</div>
<div class="avwarn"><b>⚠ كيف يتغيّر تقديرنا.</b> توقّع الإصدار الرابع نحو 290–330 مليار ريال للعام. أمران يخفّضان ذلك: كان سعر النفط في سبتمبر نحو 100 دولار لا 85–95 كما افترضنا، ولم تنهَر الصادرات لأن قوافل هرمز حلّت محلّ طريق ينبع حين تعطّل. تقديرنا الأوسط الآن <b>245–280 مليار ريال (نحو 5.0–5.7% من حجم الاقتصاد)</b>، ورقم الوزارة عند الحد الأدنى. ولا ننزل عن رقم الوزارة لأنها قدّرت في سبتمبر الماضي أيضًا 245 مليارًا لعام 2025، فانتهى العام عند 276.6 مليارًا — أعلى بـ13%.</div>
<h2>القسم 02 · الأرقام الرئيسية</h2>
<p>البيان المبدئي لميزانية 2027 (30/09) هو أحدث بيانات رسمية. بطاقات النفط والشحن تعكس الوضع في نهاية سبتمبر 2026. <span class="avnote">(البطاقات والرسوم مشتركة بين النسختين — الأرقام واحدة.)</span></p>
<h2>القسم 03 · خطة الميزانية مقابل ما حدث فعلًا، يناير–يونيو 2026</h2>
<p>الرسمان A وC يعرضان أرقام يناير–يونيو الرسمية، وB وD يعرضان يناير–مارس لأن الوزارة تقدّم لهذا الربع أدقّ تفصيل.</p>
<h3>A · مصادر دخل الحكومة — يناير–يونيو 2026 مقابل 2025</h3>
<p>ارتفع الدخل في يناير–يونيو 6% إلى <b>599.8 مليار ريال</b>: دخل النفط +9% والدخل الآخر +2%. قفز دخل النفط في أبريل–يونيو 22% إلى 185.1 مليارًا.</p>
<h3>B · قفزة الإنفاق في يناير–مارس — وتباطؤها في أبريل–يونيو</h3>
<p>تباطأ الإنفاق في كل البنود في أبريل–يونيو، إلا <b>الفوائد وتكاليف الاقتراض التي زادت 41%</b> — وستزيد أكثر مع اقتراض 2026 و2027.</p>
<h3>C · الفجوة بين الإنفاق والدخل، ربعًا بعد ربع</h3>
<p>فجوة يناير–يونيو 2026: <b>160.0 مليار ريال</b>، أي 97% من الفجوة المخططة للعام كله.</p>
<h3>D · الإنفاق حسب القطاع — الفعلي في يناير–مارس مقابل ربع الميزانية السنوية</h3>
<p>ما أنفقه كل قطاع في يناير–مارس 2026 بجانب ربع ميزانيته السنوية؛ القسمة على أربعة مقارنة مبسّطة من آفاق البيئة.</p>
<h2>القسم 04 · كيف قد ينتهي عام 2026</h2>
<p>يقف تقدير الوزارة الجديد لنهاية العام (245 مليار ريال) الآن بجانب الرقمين الرسميين لنصف العام. ولشهور أكتوبر–ديسمبر ثلاثة مسارات: يبقى البحر الأحمر مغلقًا أمام السفن السعودية وتستمر قوافل هرمز (الأرجح)؛ أو اتفاق يهدّئ المضيقين؛ أو تتوقف القوافل والبحر الأحمر لا يزال مغلقًا — فلا يبقى للسعودية طريق بحري آمن لتصدير نفطها.</p>
<h3>E · سعر النفط العالمي (برنت) — 2026 حتى الآن وثلاثة مسارات لأكتوبر–ديسمبر</h3>
<p>بلغ متوسط سبتمبر نحو 100 دولار: دفع هجوم خط الأنابيب السعر إلى 107.6 دولارًا في 10/09 و108.8 في 15/09، ثم استقر عند 97.5 في 30/09 مع عودة نفط الخليج عبر هرمز بحماية أمريكية. المهم للميزانية لم يعد السعر وحده، بل قدرة البراميل السعودية على الوصول إلى المشترين.</p>
<h3>F · فجوة 2026 بين الإنفاق والدخل — ثلاثة مسارات محتملة</h3>
<p>رقمان رسميان (نهاية مارس 125.7 مليارًا، نهاية يونيو 160.0 مليارًا)، وتقدير الوزارة لنهاية العام (245 مليارًا)، وثلاثة مسارات من آفاق البيئة. يعني رقم الوزارة أنها تتوقع نحو 85 مليارًا فقط في يوليو–ديسمبر، أي نصف ما كلّفته الأشهر نفسها في 2025 (183.9 مليارًا) — ممكن مع نفط قرب 100 دولار وصادرات مستعادة، لكنه لا يترك مجالًا لذروة دفعات نهاية العام أو لتعطّل جديد للأنبوب.</p>
<h2>القسم 05 · ما قد يحدث في أكتوبر–ديسمبر 2026</h2>
<p>النِّسب من حجم الاقتصاد في 2026، مقدّرًا بنحو <b>4.9 تريليونات ريال</b> (تقريب من آفاق البيئة). <b>الأرجح (55%)</b> — البحر الأحمر مغلق أمام السفن السعودية وقوافل هرمز مستمرة، نفط 90–105 دولارات: <b>245–280 مليار ريال (5.0–5.7%)</b>. <b>الأهدأ (20%)</b> — اتفاق يخفف التوتر في المضيقين، نفط 75–90 دولارًا: <b>235–255 مليارًا</b>. <b>الأسوأ (25%)</b> — توقف القوافل أو تعطّل الأنبوب أسابيع والبحر الأحمر مغلق: <b>290–340 مليارًا</b>.</p>
<div class="avc"><b>ما الذي قد يغيّر تقديرنا؟</b> اجتماع أوبك+ في <b>04/10</b>، وتقرير وزارة المالية لشهور يوليو–سبتمبر (<b>نحو نهاية أكتوبر</b>)، وميزانية 2027 في <b>ديسمبر</b>، وخطة الاقتراض لعام 2027 قبل نهاية العام.</div>
<h2>القسم 06 · ماذا يعني هذا لمشاريع رؤية 2030</h2>
<p>تؤثر الحرب في المشاريع بثلاث طرق: <b>المال</b> — فجوة 245 مليارًا هذا العام واقتراض في العام المقبل يعنيان أن الحكومة وصندوق الاستثمارات العامة يموّلان أشياء أقل في وقت واحد؛ <b>الشحن</b> — مع إغلاق باب المندب أمام السفن السعودية لم تعد مواد البناء والمعدات القادمة من آسيا تصل مباشرة إلى موانئ البحر الأحمر، بل تلتف عبر السويس أو تصل إلى موانئ الخليج وتعبر البلاد برًّا؛ <b>الأمان</b> — مشاريع ساحل البحر الأحمر قريبة الآن من منطقة حرب. هذا ترتيب آفاق البيئة لا قائمة رسمية.</p>
<ul>
<li><b>الأكثر تأثرًا:</b> نيوم (أوكساجون وميناء نيوم وسندالة)؛ شركة نيوم للهيدروجين الأخضر — كان يُفترض أن تصدّر عبر البحر الأحمر؛ البحر الأحمر الدولية (البحر الأحمر وأمالا) — سياحة فاخرة بجوار حرب بحرية؛ مدينة الملك عبدالله الاقتصادية وميناء الملك عبدالله ومصانع السيارات فيها.</li>
<li><b>تأثر متوسط:</b> المربع الجديد (المكعب) — آمن من البحر الأحمر لكنه بلا موعد ثابت ويسهل إبطاؤه؛ روشن وسدرة؛ توسعة ساتورب في الجبيل؛ مبادرة السعودية الخضراء؛ المدن الصناعية على البحر الأحمر (ينبع وجدة ورابغ).</li>
<li><b>الأقل تأثرًا أو المستفيد:</b> الدرعية؛ القدية وحديقة الملك سلمان المرتبطتان بكأس العالم 2034؛ حقل الجافورة ومعادن وسابك ومحطات التحلية وصناعات الجبيل ورأس الخير؛ المنطقة اللوجستية المتكاملة الخاصة في الرياض والطرق البرية بين الخليج والبحر الأحمر.</li>
</ul>
<h2>القسم 07 · ما يجب أن تفعله آفاق البيئة</h2>
<p>مقترحات إدارة تطوير الأعمال للنقاش، وليست قرارات:</p>
<ul>
<li><b>حماية السيولة:</b> مراجعة المستحقات لدى الجهات الحكومية ومشاريع الصندوق، وطلب دفعات مقدمة أو مرحلية في العقود الجديدة مع مشاريع سياحة البحر الأحمر ونيوم، وتقديم العملاء ذوي الدخل الذاتي (أرامكو ومشاريعها المشتركة، سابك، معادن، المصافي).</li>
<li><b>تحويل خط العطاءات</b> نحو مشاريع الرياض المرتبطة بكأس العالم وإكسبو 2030، وصناعات ساحل الخليج، والتحلية، واللوجستيات الداخلية.</li>
<li><b>الجاهزية لانسكابات النفط والتنظيف على ساحل البحر الأحمر:</b> التأكد من وجود آفاق البيئة في قوائم الاستجابة لدى أرامكو والهيئة العامة للموانئ (موانئ) والمركز الوطني للرقابة على الالتزام البيئي لساحل ينبع–جدة–رابغ.</li>
<li><b>تأمين الإمدادات:</b> زيادة مخزون البنود الحرجة (البراميل، معدات الوقاية، المواد الكيميائية، قطع الغيار)، والبحث عن بدائل سعودية، واستخدام الدمام أو الجبيل مع النقل البري غربًا عند بطء موانئ البحر الأحمر.</li>
</ul>
<h2>القسم 08 · من أين تأتي الأرقام</h2>
<p>كل رقم يأتي من إحدى الجهات أدناه. البيانات الحكومية الرسمية هي الأهم؛ وأرقام المحللين والأسواق وتقديرات آفاق البيئة موسومة بذلك في كل موضع — <b>وتقديرات آفاق البيئة ليست توقعات منقولة عن جهات أخرى.</b></p>
<p><b>كلمات مستخدمة في هذه الصفحة:</b> <b>العجز / الفجوة</b> — ما تنفقه الحكومة زيادةً على دخلها، ويُغطّى بالاقتراض أو المدخرات. <b>برنت</b> — سعر النفط العالمي الرئيسي بالدولار للبرميل. <b>أوبك / أوبك+</b> — مجموعة الدول المصدّرة للنفط بقيادة السعودية، وأوبك+ تضم روسيا ومنتجين آخرين. <b>مضيق هرمز / باب المندب</b> — الممرّان البحريان عند طرفي الجزيرة العربية. <b>خط شرق–غرب</b> — أنبوب النفط من حقول المنطقة الشرقية إلى ينبع. <b>برميل يوميًا</b> — كمية النفط المنتجة أو المشحونة كل يوم؛ البرميل نحو 159 لترًا.</p>
<ul>
<li>وزارة المالية — البيان المبدئي لميزانية 2027 (30/09/2026) وتقرير أبريل–يونيو 2026 (30/07/2026)</li>
<li>وزارة الطاقة — بيان الهجوم على خط شرق–غرب (سبتمبر 2026)</li>
<li>رويترز · Seatrade Maritime · OilPrice.com · Rigzone — إيقاف الخط وإعادة تشغيله والتحميل في ينبع</li>
<li>يورونيوز · الجزيرة · Long War Journal · CBS — تقدّم الحوثيين نحو باب المندب</li>
<li>CNBC — تدفق نفط الخليج عبر هرمز بحماية أمريكية (30/09/2026)</li>
<li>أوبك — بيان 06/09/2026 · Investing.com — أسعار برنت</li>
</ul>
<div class="avmeta">مالية الحكومة السعودية 2026 — الإصدار الخامس · أُعدّ لإدارة آفاق البيئة — التخطيط الاستراتيجي، إدارة تطوير الأعمال · بتاريخ 01/10/2026 ويحلّ محل الإصدارات 4 (26/08) و3 (19/07) و2 (07/07) و1 (28/06) · التواريخ بصيغة يوم/شهر/سنة · المبالغ بمليارات الريالات ما لم يُذكر غير ذلك · محتوى تحليلي لأغراض داخلية وليس نصيحة استثمارية أو قانونية.</div>
</div>
'''
