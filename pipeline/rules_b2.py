import re
EN = [
 (r' ?\((?:D\d+(?:, ?)?)+\)', ''),  # internal decision codes never shown
 # page-specific phrases first
 (r'labelled AR21 to AR25 \(AR24 = the 2024 report\)', 'cited by year (for example, “2024 report”)'),
 (r'full audit of the prior tranche', "full re-check of the previous briefing"),
 (r'HUB D\.[A-Za-z_.]+(\[\d+\])?', 'figures in the PIF Intelligence Hub'),
 (r'\bAR2(\d) p\.? ?(\d+)', r'202\1 report p.\2'), (r'\bAR2(\d)\b', r'202\1 report'),
 (r'\bS26 p\.? ?(\d+)', r'Strategy document p.\1'), (r'\bS26\b', 'Strategy document'),
 (r'since VRP inception', 'since the Vision Realization Program began'), (r'\bVRP\b', 'Vision Realization Program'),
 (r'(?<=[ ,(])p(\d+)\b', r'p.\1'), (r'\bper annum\b', 'per year'), (r'\bAuM\b', 'assets under management'),
 (r'\bEIA/ESIA & Permitting\b', 'Environmental impact studies & permits'), (r'\bEIA/ESIA\b', 'environmental impact studies'),
 (r'\bSustainability & ESG Consultancy\b', 'Sustainability consulting'), (r'\bESG\b', 'sustainability'),
 (r'\bFCF/dividend gap analysis\b', 'free cash flow vs dividend — analysis'), (r'\bFCF\b', 'free cash flow'),
 (r'\b(\w+) OSP\b', r"Aramco's \1 selling price"), (r'\bOSP\b', "Aramco's official selling price"),
 (r'\bIPO/Funding Round\b', 'Stock-market listing / funding round'), (r'\bIPO\b', 'stock-market listing'),
 (r'\bBESS\b', 'battery storage'), (r'(\d[\d,.]*) ?GW\b', r'\1 gigawatts'), (r'(\d[\d,.]*) ?MW\b', r'\1 megawatts'),
 (r'\bJVs\b', 'joint ventures'), (r'\bJV\b', 'joint venture'), (r'\bSEZ\b', 'special economic zone'),
 (r'\bKPIs\b', 'performance measures'), (r'(\d) ?pp\b(?!\.)', r'\1 percentage points'),
 (r'\be\.g\.', 'for example'), (r'\bi\.e\.', 'that is'),
 # money
 (r'\$ ?(\d[\d.,]*) ?bn\b', r'$\1 billion'), (r'SAR ?(\d[\d.,]*) ?bn\b', r'SAR \1 billion'), (r'(\d[\d.,]*) ?bn\b', r'\1 billion'),
 (r'\bUSD bn\b', 'US$ billion'), (r'\bSAR bn\b', 'SAR billion'), (r'\bbn\b', 'billion'),
 (r'\$ ?(\d[\d.,]*) ?mn\b', r'$\1 million'), (r'SAR ?(\d[\d.,]*) ?mn\b', r'SAR \1 million'), (r'(\d[\d.,]*) ?mn\b', r'\1 million'), (r'\bmn\b', 'million'),
 # periods
 (r'\bQ2/Q3 (20\d\d)', r'April–September \1'), (r'\bQ2/Q3\b(?!-\d)', 'April–September'),
 (r'\bQ1 (20\d\d)(?!-)', r'January–March \1'), (r'\bQ2 (20\d\d)(?!-)', r'April–June \1'), (r'\bQ3 (20\d\d)(?!-)', r'July–September \1'), (r'\bQ4 (20\d\d)(?!-)', r'October–December \1'),
 (r'\bQ1\b(?!-\d)', 'January–March'), (r'\bQ2\b(?!-\d)', 'April–June'), (r'\bQ3\b(?!-\d)', 'July–September'), (r'\bQ4\b(?!-\d)', 'October–December'),
 (r'\bH1 (20\d\d)(?!-)', r'January–June \1'), (r'\bH2 (20\d\d)(?!-)', r'July–December \1'), (r'\bH1\b(?!-\d)', 'January–June'), (r'\bH2\b(?!-\d)', 'July–December'),
 (r'\bFY ?(20\d\d)\b', r'\1 financial year'),
 # Regulatory news page
 (r'\bThis feed week\b', 'This week'), (r'\bfeed week\b', 'collection week'), (r'\bFeed week\b', 'Collection week'),
 (r'\bOfficial \+ SPA\b', 'Official sites + Saudi Press Agency'), (r'\bSPA only\b', 'Saudi Press Agency only'), (r'\bvia SPA\b', 'via the Saudi Press Agency'),
 (r'\b90-day window\b', 'last 90 days'),
]
FIRST = [  # expanded once per page, where the full name is not already on the page
 ('PIF', 'Public Investment Fund (PIF)', 'Public Investment Fund'),
 ('GDP', 'GDP (the size of the economy)', 'size of the economy'),
 ('SIRC', 'Saudi Investment Recycling Company (SIRC)', 'Saudi Investment Recycling Company'),
 ('MWAN', 'National Center for Waste Management (MWAN)', 'National Center for Waste Management'),
 ('SWPC', 'Saudi Water Partnership Company (SWPC)', 'Saudi Water Partnership Company'),
 ('SPPC', 'Saudi Power Procurement Company (SPPC)', 'Saudi Power Procurement Company'),
 ('NGHC', 'NEOM Green Hydrogen Company (NGHC)', 'NEOM Green Hydrogen Company'),
 ('RCJY', 'Royal Commission for Jubail & Yanbu (RCJY)', 'Royal Commission for Jubail'),
 ('RCU', 'Royal Commission for AlUla (RCU)', 'Royal Commission for AlUla'),
 ('SGI', 'Saudi Green Initiative (SGI)', 'Saudi Green Initiative'),
 ('KAEC', 'King Abdullah Economic City (KAEC)', 'King Abdullah Economic City'),
 ('SWCC', 'Saline Water Conversion Corporation (SWCC)', 'Saline Water Conversion Corporation'),
 ('IMI', 'International Maritime Industries (IMI)', 'International Maritime Industries'),
 ('SATORP', 'SATORP (the Aramco–TotalEnergies refinery in Jubail)', 'Aramco–TotalEnergies'),
 ('OPEC', 'OPEC (the group of oil-exporting countries)', 'oil-exporting countries'),
 ('SPA', 'Saudi Press Agency (SPA)', 'Saudi Press Agency'),
 ('MODON', 'MODON (Saudi Authority for Industrial Cities)', 'Authority for Industrial Cities'),
]
AR = [(r' ?\((?:D\d+(?:, ?)?)+\)', ''), (r'\bAR2(\d)\b', r'تقرير 202\1'), (r'\bS26\b', 'وثيقة الاستراتيجية'), (r'\bESG\b', 'الاستدامة'), (r'\bGICS\b', 'GICS')]
