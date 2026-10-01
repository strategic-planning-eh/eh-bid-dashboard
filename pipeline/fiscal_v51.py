# Saudi Government Finances 2026 — version 5.1 (01/10/2026). Text for patch_fiscal_v51.py.
# Sources: MoF Pre-Budget Statement FY2027 (30/09/2026), Budget Statement FY2026, Year-End Budget Performance Report FY2024,
# Quarterly Budget Performance Reports Q1 and Q2 FY2026 — all supplied by Youssef on 01/10/2026.
HISTORY = '''<!-- ============ SECTION 3B — 2022–2029 ============ -->
<section id="history">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 04</span><h2>2022 to 2029: what was planned, what happened, what comes next</h2><span class="upd-chip">Official Ministry of Finance figures</span></div>
    <p class="sec-sub">Every number in this section comes from the Ministry of Finance's own documents: the year-end report for 2024, the 2026 budget statement, the quarterly reports for January–March and April–June 2026, and the 2027 pre-budget statement. "Plan" is the figure in the budget approved at the start of the year; "actual" is what the Ministry later reported. Amounts in SAR billion.</p>
    <div class="tbl-wrap">
      <table class="scen">
        <thead><tr><th>Year</th><th>Income<br>plan → actual</th><th>Spending<br>plan → actual</th><th>Gap<br>plan → actual</th><th>Gap as %<br>of the economy</th><th>Government debt<br>at year-end</th><th>What it tells us</th></tr></thead>
        <tbody>
          <tr class="opt"><td class="sname">2022</td><td>1,268 (actual)</td><td>1,164 (actual)</td><td class="big">+104 surplus</td><td>+2.2%</td><td>990</td><td>The last year the government earned more than it spent: oil prices were high after the war in Ukraine.</td></tr>
          <tr class="base"><td class="sname">2023</td><td>1,212 (actual)</td><td>1,293 (actual)</td><td class="big">−81</td><td>−1.8%</td><td>1,050</td><td>Back to a gap as Saudi Arabia cut its own oil output under the OPEC+ agreement.</td></tr>
          <tr class="base"><td class="sname">2024</td><td>1,172 → 1,259</td><td>1,251 → 1,375 <b>(+9.9%)</b></td><td class="big">−79 → −116</td><td>−2.5%</td><td>1,216</td><td>Income beat the plan, but spending beat it by more — mostly running costs, social support and giga-project payments.</td></tr>
          <tr class="pess"><td class="sname">2025</td><td>1,184 → 1,112</td><td>1,285 → 1,388 <b>(+8.0%)</b></td><td class="big">−101 → −277</td><td>−5.8%</td><td>1,519</td><td>Cheap oil (about $70) cut income while spending again ran 8% over plan. The Ministry's September estimate was −245; the final figure was −277.</td></tr>
          <tr class="pess"><td class="sname">2026</td><td>1,147 → 1,190 <i>(est.)</i></td><td>1,313 → 1,435 <b>(+9.3%)</b> <i>(est.)</i></td><td class="big">−165 → −245 <i>(est.)</i></td><td>−4.9%</td><td>1,685 <i>(end of June)</i></td><td>War year. Income holds up thanks to high prices, but exports fell to about 7.9 million barrels a day (January–August) and spending again runs about 9% over plan.</td></tr>
          <tr class="base"><td class="sname">2027 plan</td><td>1,202</td><td>1,392</td><td class="big">−191</td><td>−3.6%</td><td>"to rise deliberately"</td><td>Spending is planned 3% <b>below</b> what 2026 is expected to cost, and the plan assumes the economy grows 12.8% as exports recover.</td></tr>
          <tr><td class="sname">2028–2029 plan</td><td>1,302 · 1,351</td><td>1,479 · 1,544</td><td class="big">−177 · −192</td><td>−3.1% · −3.3%</td><td>—</td><td>Gaps every year to 2029: the government expects to keep borrowing.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="chart-grid" style="margin-top:16px">
      <div class="card full">
        <div class="chead">
          <div><h3>G · The gap between spending and income: planned vs actual, 2022–2029</h3>
          <p class="csub">Light bars: the gap in the budget approved at the start of each year (2028–2029 are the Ministry's projections). Dark bars: what actually happened (2026 is the Ministry's latest estimate). Above zero = surplus.</p></div>
          <span class="tag off">Official · Ministry of Finance</span>
        </div>
        <div class="chart-box"><canvas id="chartG"></canvas></div>
      </div>
    </div>
    <div class="callout blue" style="margin-top:14px"><b>Four things the history shows.</b>
      <br>1. <b>Spending has ended 8–10% above the budget three years running</b> — 2024 (+9.9%), 2025 (+8.0%) and the 2026 estimate (+9.3%) — in a year of good oil income, a year of weak oil income, and a war year alike.
      <br>2. <b>The September estimate has been too low before.</b> In September 2025 the Ministry expected a 2025 gap of SAR 245 billion; the year ended at SAR 277 billion, 13% more. That is why our 2026 range starts at the Ministry's figure rather than below it.
      <br>3. <b>The 2027 plan asks for a spending cut.</b> SAR 1,392 billion is 3% less than the SAR 1,435 billion 2026 is expected to cost. If 2027 overruns its plan the way the last three years did (8–10%), spending would reach about SAR 1,500–1,530 billion and the gap SAR 300–330 billion unless income beats SAR 1,202 billion (EH arithmetic). To hit the plan, something has to be slowed — and the Ministry says money will go to projects with "economic and social returns". This is where the pressure on Vision 2030 projects in section 07 comes from.
      <br>4. <b>Debt has grown by 70% in three and a half years</b>, from SAR 990 billion (end of 2022) to SAR 1,685 billion (end of June 2026), and interest costs rose 41% in April–June 2026 compared with a year earlier. Savings at the central bank have stayed around SAR 390–400 billion: the gaps are being borrowed, not paid from savings.</div>
    <div class="csrc" style="margin-top:8px"><span class="tag off">Sources</span> Ministry of Finance: Year-End Budget Performance Report FY2024 (2022–2024 actuals, 2024 plan); Budget Statement FY2026 (2025 plan and estimate, 2026 plan); Quarterly Budget Performance Reports Q1 and Q2 FY2026 (2025 actual, January–June 2026, debt); Pre-Budget Statement FY2027 (2026 estimate, 2027–2029 plan, size of the economy). The 2027 overrun case is EH's arithmetic, not a Ministry figure.</div>
  </div>
</section>

'''
V2030 = '''<!-- ============ SECTION 5B — VISION 2030 PROJECTS ============ -->
<section id="v2030impact">
  <div class="wrap">
    <div class="sec-head"><span class="sec-num">SECTION 07</span><h2>Which Vision 2030 projects are likely to be shelved, cut back or delayed</h2><span class="upd-chip warn">EH assessment · 01/10/2026</span></div>
    <p class="sec-sub">The government rarely cancels a project out loud. When money is short it re-phases, shrinks the scope, hands the project to someone else, or lets it go quiet: The Line went from a 170 km city to a first phase of a few kilometres, and Trojena lost the 2029 Asian Winter Games to Almaty without either being formally cancelled. So the useful question is not "which will be cancelled" but "which will be shelved, cut back or delayed". With the 2027 plan asking for a 3% spending cut (section 04) and the war adding cost, we sorted the 31 projects tracked on the hub's Vision 2030 page with three tests.</p>
    <div class="callout" style="margin-bottom:14px"><b>How we decided — three tests.</b>
      <br><b>1 · Is it mostly built?</b> Money already spent protects a project: a half-finished landmark is worse for the government than a late one.
      <br><b>2 · Does it earn money, meet a strategic need, or have a fixed date?</b> Industry that replaces imports, ports and land routes, energy, and anything tied to the 2034 FIFA World Cup or Expo 2030 are hard to stop.
      <br><b>3 · Who pays?</b> A project paid for only by the Public Investment Fund (PIF) can be slowed with one decision. One with private partners, a stock-market listing or bank loans is much harder to drop.
      <br>A project that fails all three tests is the one most at risk. The war is a fourth, separate factor: Red Sea projects also face slower shipping and fewer visitors while Bab el-Mandeb stays closed to Saudi ships.</div>
    <div class="tbl-wrap">
      <table class="scen">
        <thead><tr><th>Project</th><th>1 · Mostly built?</th><th>2 · Earns money / strategic / fixed date?</th><th>3 · Who pays?</th><th>War exposure</th><th>Likely outcome</th><th>Why</th></tr></thead>
        <tbody>
          <tr class="pess"><td class="sname">The Line (NEOM)</td><td>No — first phase only</td><td>None</td><td>PIF</td><td>High</td><td><span class="riskpill high">Shelved in all but name</span></td><td>Fails all three tests. Already on hold, cut to a fraction of the original plan, and left out of PIF's 2026–2030 strategy.</td></tr>
          <tr class="pess"><td class="sname">Trojena (NEOM)</td><td>No</td><td>Lost its fixed date — the 2029 Asian Winter Games moved to Almaty</td><td>PIF</td><td>High</td><td><span class="riskpill high">Shelved, or offered to private investors</span></td><td>On hold and left out of PIF's new strategy. With no event to build for, there is no reason to finish it on schedule.</td></tr>
          <tr class="pess"><td class="sname">New Murabba / Mukaab</td><td>Partly — Mukaab excavation about 86% done when work resumed in August</td><td>No fixed date; finish planned for 2040</td><td>PIF</td><td>Low (Riyadh)</td><td><span class="riskpill high">Heavily downsized and re-phased</span></td><td>The easiest large Riyadh project to slow. The resumed excavation makes a smaller Mukaab and a slower district more likely than a full stop.</td></tr>
          <tr class="pess"><td class="sname">AMAALA and Red Sea Global phase 2</td><td>First resorts built; phase 2 not started</td><td>Luxury tourism only; no fixed date; AMAALA already late</td><td>PIF</td><td>High</td><td><span class="riskpill high">Later phases frozen; open resorts kept</span></td><td>Work on phase 2 was reported paused in February (Red Sea Global denied it), and a war at sea next door hurts bookings.</td></tr>
          <tr class="pess"><td class="sname">NEOM tourism beyond Sindalah's first phase</td><td>Sindalah phase 1 only</td><td>None</td><td>PIF</td><td>High</td><td><span class="riskpill high">Cut back</span></td><td>Same tourism logic as AMAALA, on top of NEOM's general spending freeze.</td></tr>
          <tr class="base"><td class="sname">Oxagon industrial city (NEOM)</td><td>Partly</td><td>Industry is a strategic need; Aramco oversight was reported under discussion in January</td><td>PIF, possibly Aramco</td><td>Medium</td><td><span class="riskpill mod">Shrunk to what industry needs</span></td><td>The "floating city" vision is likely to give way to a smaller industrial zone next to the port.</td></tr>
          <tr class="base"><td class="sname">Saudi Green Initiative headline targets</td><td>Ongoing</td><td>Long-term goals, no hard date</td><td>Government</td><td>Low</td><td><span class="riskpill mod">Stretched quietly</span></td><td>Tree-planting and reserve targets can be slowed with little visible cost.</td></tr>
          <tr class="base"><td class="sname">ROSHN later communities</td><td>SEDRA is delivering homes</td><td>Housing for Saudi families is a priority</td><td>PIF and bank lending</td><td>Low</td><td><span class="riskpill mod">Slowed</span></td><td>Current phases continue; new ones depend on PIF money and mortgage demand.</td></tr>
          <tr class="base"><td class="sname">King Abdullah Economic City and its car plants (Lucid, Ceer, Hyundai)</td><td>Plants built or being built</td><td>Industrial localisation — a core strategic aim</td><td>Listed company, private partners; PIF holds a stake in Lucid</td><td>High — parts from Asia came through Bab el-Mandeb</td><td><span class="riskpill mod">Delayed, not dropped</span></td><td>Passes tests 2 and 3. Expect slower start-ups and parts brought in through Gulf ports or Suez.</td></tr>
          <tr class="base"><td class="sname">NEOM Green Hydrogen Company</td><td>About 90% built</td><td>Export earner</td><td>Joint venture with private partners</td><td>High — exports were meant to sail through the Red Sea</td><td><span class="riskpill mod">Finished; first exports slip</span></td><td>Too far along to stop; the question is when it can ship.</td></tr>
          <tr class="base"><td class="sname">SATORP / Amiral expansion (Jubail)</td><td>Under construction</td><td>Earns money</td><td>Aramco and TotalEnergies</td><td>Medium (Gulf coast)</td><td><span class="riskpill mod">Continues, maybe slower</span></td><td>Paid outside the budget, but Aramco itself is under pressure.</td></tr>
          <tr class="opt"><td class="sname">NEOM Port</td><td>Operating in part</td><td>Strategic: one of the few Red Sea gateways still reachable from Europe while Bab el-Mandeb is closed</td><td>PIF, possibly Aramco</td><td>Medium</td><td><span class="riskpill low">Continues — may gain</span></td><td>The war makes northern Red Sea ports and land routes more valuable, not less.</td></tr>
          <tr class="opt"><td class="sname">Diriyah</td><td>Partly open, visitors coming</td><td>UNESCO heritage; steady contracts</td><td>PIF</td><td>Low</td><td><span class="riskpill low">Continues, perhaps slower</span></td><td>Passes tests 1 and 2.</td></tr>
          <tr class="opt"><td class="sname">Qiddiya and King Salman Park</td><td>Partly open</td><td>Fixed dates — 2034 World Cup, opening commitments</td><td>PIF / Government</td><td>Low</td><td><span class="riskpill low">Continues</span></td><td>Fixed dates protect them when other projects are slowed.</td></tr>
          <tr class="opt"><td class="sname">Jafurah gas, Ma'aden, SABIC, desalination, Jubail and Ras Al-Khair industry</td><td>Operating</td><td>Earn money or keep the country running</td><td>Aramco, listed companies, Government</td><td>Medium (Gulf coast)</td><td><span class="riskpill low">Continues</span></td><td>Jafurah's gas lets Saudi Arabia burn less oil at home and export more, so it gains priority.</td></tr>
          <tr class="opt"><td class="sname">Special Integrated Logistics Zone (Riyadh) and Gulf–Red Sea land routes</td><td>Operating</td><td>Strategic — goods now cross the country by road and rail</td><td>Government</td><td>Low</td><td><span class="riskpill low">Expands</span></td><td>One of the few areas likely to get more work, not less.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout" style="margin-top:14px"><b>What would show a project is about to be cut.</b> It is missing from the 2027 budget statement in December; contract awards stop or contractors are asked to "re-baseline"; its chief executive is replaced; or PIF starts talking about "strategic partners" for it.</div>
  </div>
</section>

'''
EH_CARD2_OLD = 'Shift bidding effort toward the projects in the "Lower" and "May gain" rows: Riyadh projects tied to the World Cup and Expo 2030, Gulf-coast industry (Jubail, Ras Al-Khair, Jafurah), desalination and inland logistics. Treat new bids for the projects in the "Most affected" rows as higher-risk unless payment terms are secure.'
EH_CARD2_NEW = 'Shift bidding effort toward projects marked "Continues" or "Expands" in section 07: Riyadh projects tied to the World Cup and Expo 2030, Gulf-coast industry (Jubail, Ras Al-Khair, Jafurah), desalination, NEOM Port and inland logistics. Treat new bids for projects marked "Shelved", "Downsized", "Frozen" or "Cut back" as high-risk unless payment terms are secure; for "Delayed" projects such as King Abdullah Economic City, keep the relationship but plan for later start dates.'
SRC_ADD = r'''  {bg:'#0A2A43', ini:'HIS', name:'Ministry of Finance \u2014 earlier budget documents', date:'2024 year-end report \u00b7 2026 budget statement \u00b7 Q1/Q2 2026 reports', head:'Spending ended 8\u201310% above plan in 2024, 2025 and (estimate) 2026; debt SAR 990 billion (2022) \u2192 1,685 billion (June 2026).', desc:'Year-End Budget Performance Report FY2024: 2022\u20132024 actuals and the 2024 plan. Budget Statement FY2026: the 2025 plan and the SAR 245 billion estimate for 2025 later revised to 277. Quarterly reports for January\u2013March and April\u2013June 2026: 2025 actual, half-year 2026 figures and debt.'},
'''
AR_V2030 = '''<h2>القسم 07 · أي مشاريع رؤية 2030 مرشحة للتجميد أو التقليص أو التأجيل</h2>
<p>نادرًا ما تُعلن الحكومة إلغاء مشروع؛ فعند شح المال تعيد جدولته أو تقلّص نطاقه أو تنقله إلى جهة أخرى أو تتركه يخفت. تقلّص «ذا لاين» من مدينة بطول 170 كيلومترًا إلى مرحلة أولى ببضعة كيلومترات، وخسرت «تروجينا» دورة الألعاب الآسيوية الشتوية 2029 لصالح ألماتي، دون إلغاء رسمي لأيٍّ منهما. ومع طلب خطة 2027 خفض الإنفاق 3% وتكلفة الحرب، فرزنا المشاريع بثلاثة اختبارات:</p>
<div class="avc"><b>كيف قررنا — ثلاثة اختبارات.</b> <b>1 · هل بُني معظمه؟</b> المال المُنفق يحمي المشروع. <b>2 · هل يدرّ دخلًا أو يلبّي حاجة استراتيجية أو له موعد ثابت؟</b> الصناعة البديلة للاستيراد، والموانئ والطرق البرية، والطاقة، وكل ما يرتبط بكأس العالم 2034 أو إكسبو 2030. <b>3 · من يدفع؟</b> المشروع الذي يموّله صندوق الاستثمارات العامة وحده يمكن إبطاؤه بقرار واحد؛ أما ما له شركاء خاصون أو إدراج في السوق أو قروض بنكية فيصعب التخلي عنه. المشروع الذي يرسب في الاختبارات الثلاثة هو الأكثر عرضة. والحرب عامل رابع منفصل يمسّ مشاريع البحر الأحمر.</div>
<ul>
<li><b>مجمّدة فعليًا:</b> ذا لاين؛ تروجينا (أو عرضها على مستثمرين من القطاع الخاص).</li>
<li><b>تقليص كبير أو تجميد المراحل اللاحقة:</b> المربع الجديد والمكعب (تقليص وإعادة جدولة لا إيقاف كامل، إذ كان الحفر نحو 86% عند استئناف العمل في أغسطس)؛ أمالا والمرحلة الثانية من البحر الأحمر الدولية (تُحفظ المنتجعات المفتوحة)؛ سياحة نيوم بعد المرحلة الأولى من سندالة؛ مدينة أوكساجون الصناعية (تُختصر إلى ما تحتاجه الصناعة).</li>
<li><b>إبطاء أو تأجيل:</b> مستهدفات مبادرة السعودية الخضراء؛ مجتمعات روشن اللاحقة؛ مدينة الملك عبدالله الاقتصادية ومصانع السيارات فيها (تأجيل لا تخلٍّ — تجتاز الاختبارين 2 و3)؛ شركة نيوم للهيدروجين الأخضر (تكتمل ويتأخر التصدير)؛ توسعة ساتورب.</li>
<li><b>تستمر أو تتوسع:</b> ميناء نيوم (قد يستفيد بوصفه بوابة شمالية على البحر الأحمر)؛ الدرعية؛ القدية وحديقة الملك سلمان؛ الجافورة ومعادن وسابك والتحلية وصناعات الجبيل ورأس الخير؛ المنطقة اللوجستية المتكاملة الخاصة والطرق البرية بين الخليج والبحر الأحمر.</li>
</ul>
<p><b>علامات تسبق التقليص:</b> غياب المشروع عن بيان ميزانية 2027 في ديسمبر، أو توقف الترسيات، أو تغيير الرئيس التنفيذي، أو حديث الصندوق عن «شركاء استراتيجيين».</p>
'''
AR_HISTORY = '''<h2>القسم 04 · من 2022 إلى 2029: ما خُطط وما حدث وما هو قادم</h2>
<p>كل الأرقام من وثائق وزارة المالية (مليار ريال؛ الخطة ← الفعلي):</p>
<ul>
<li><b>2022:</b> فائض 104 (+2.2% من الاقتصاد)؛ الدين 990.</li>
<li><b>2023:</b> عجز 81 (−1.8%)؛ الدين 1,050.</li>
<li><b>2024:</b> الإنفاق 1,251 ← 1,375 (+9.9%)؛ العجز 79 ← 116 (−2.5%)؛ الدين 1,216.</li>
<li><b>2025:</b> الدخل 1,184 ← 1,112؛ الإنفاق 1,285 ← 1,388 (+8.0%)؛ العجز 101 ← 277 (−5.8%)؛ الدين 1,519. قدّرت الوزارة في سبتمبر 2025 العجز بـ245 فانتهى عند 277.</li>
<li><b>2026 (تقدير):</b> الدخل 1,147 ← 1,190؛ الإنفاق 1,313 ← 1,435 (+9.3%)؛ العجز 165 ← 245 (−4.9%)؛ الدين 1,685 في نهاية يونيو.</li>
<li><b>خطة 2027:</b> الدخل 1,202؛ الإنفاق 1,392؛ العجز 191 (−3.6%). <b>2028–2029:</b> عجز 177 ثم 192.</li>
</ul>
<div class="avc"><b>أربع دلالات.</b> 1) انتهى الإنفاق أعلى من الميزانية بـ8–10% ثلاث سنوات متتالية. 2) تقدير سبتمبر جاء أقل من الواقع من قبل (245 ← 277). 3) خطة 2027 تطلب إنفاقًا أقل بـ3% مما يُتوقع أن يكلّفه 2026؛ وإن تجاوزت الخطة كالسنوات الثلاث الماضية فسيبلغ الإنفاق نحو 1,500–1,530 مليارًا والعجز 300–330 مليارًا ما لم يتجاوز الدخل 1,202 مليار (حساب آفاق البيئة) — ومن هنا يأتي الضغط على مشاريع رؤية 2030. 4) ارتفع الدين 70% في ثلاث سنوات ونصف، وزادت تكاليف الفوائد 41% في أبريل–يونيو 2026، بينما بقيت المدخرات قرب 390–400 مليار: العجز يُقترض ولا يُسدَّد من المدخرات.</div>
'''
