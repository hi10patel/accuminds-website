"""Content for the service pages. Edit here, then run:  python tools/build_pages.py

Rules for this file:
- Only state facts we can source. Regulatory facts go in "facts" with a source
  link and are re-checked on the date in REVIEWED. Update REVIEWED when you
  re-check them.
- No invented claims (client numbers, certifications, guarantees, prices).
- "experience" describes the lead's own background (owner-approved, October
  2026): no names, no employer names, no figures. Do not present it as
  Accuminds client results.
- Plain text only; the builder escapes it. Use '|' nowhere special.
"""

REVIEWED = "October 2026"

FTA_VAT_REG = ("FTA: VAT registration", "https://tax.gov.ae/en/services/vat.registration.aspx")
FTA_VAT_TOPIC = ("FTA: Registration for VAT", "https://tax.gov.ae/en/taxes/Vat/vat.topics/registration.for.vat.aspx")
MOF_VAT = ("Ministry of Finance: VAT", "https://mof.gov.ae/en/public-finance/tax/value-added-tax-vat/")
MOF_SBR = ("Ministry of Finance: Small Business Relief extended to 2029",
           "https://mof.gov.ae/en/news/ministry-of-finance-announces-extension-of-small-business-relief-for-corporate-tax-purposes-until-31-december-2029/")
FTA_SBR = ("FTA: Small Business Relief returns",
           "https://tax.gov.ae/en/media.centre/news/fta.confirms.taxable.persons.eligible.for.the.small.business.relief.must.submit.simplified.corporate.tax.returns.within.prescribed.legal.deadline.aspx")
MOF_EINV = ("Ministry of Finance: e-invoicing amendments (2026)",
            "https://mof.gov.ae/en/news/ministry-of-finance-announces-targeted-amendments-to-einvoicing-system-decisions/")
MOF_EINV_GUIDE = ("Ministry of Finance: UAE e-invoicing", "https://mof.gov.ae/en/about-us/initiatives/einvoicing/")
MOF_EINV_OCT = ("Ministry of Finance: e-invoicing amendments (19 October 2026)",
                "https://mof.gov.ae/en/news/ministry-of-finance-amends-electronic-invoicing-regulations-to-ease-the-burden-on-businesses/")
FTA_EINV = ("FTA: UAE e-invoicing", "https://tax.gov.ae/en/content/uae.einvoicing.aspx")
MOF_EINV_GUIDELINES = ("Ministry of Finance: UAE Electronic Invoicing Guidelines v2.0 (26 October 2026)",
                       "https://mof.gov.ae/wp-content/uploads/2026/10/UAE-Electronic-Invoicing-Guidelines_En.pdf")
MOF_EINV_PENALTIES = ("Ministry of Finance: updated e-invoicing penalties (30 October 2026)",
                      "https://mof.gov.ae/en/news/mof-announces-updated-administrative-penalties-related-to-the-uae-einvoicing-system-to-enhance-clarity-and-support-business-compliance/")

SERVICES = [
    # ------------------------------------------------------------------ Core accounting
    {
        "slug": "bookkeeping-accounting-dubai",
        "pillar": "Core Accounting",
        "name": "Bookkeeping & Accounting",
        "title": "Bookkeeping & Accounting Services in Dubai | Accuminds",
        "description": "Bookkeeping, bank reconciliations, month-end close and financial statements for UAE SMEs and free zone companies. Based in Dubai Silicon Oasis.",
        "h1": "Bookkeeping & accounting services in Dubai",
        "lead": "Bookkeeping, reconciliations and month-end close for UAE SMEs and free zone entities, with management accounts you can act on.",
        "card": "Bookkeeping, reconciliations, month-end close and financial statements.",
        "included": [
            ("Bookkeeping", "Sales, purchases and expenses recorded in your accounting system and coded the same way every month."),
            ("Bank & card reconciliations", "Every bank and card account reconciled, so the ledger matches what actually moved."),
            ("Receivables & payables", "Customer and supplier balances kept current, with ageing you can chase from."),
            ("Month-end close", "Accruals, prepayments and fixed assets handled, so each month closes on a consistent basis."),
            ("Financial statements", "Profit and loss, balance sheet and cash flow, prepared for management, your auditor or your bank."),
            ("Chart of accounts set-up & clean-up", "A structure that fits your business and supports VAT, Corporate Tax and management reporting."),
            ("Catch-up bookkeeping", "Months behind? We rebuild and reconcile the backlog before the monthly routine starts."),
        ],
        "who": [
            "SMEs and start-ups without a full-time accountant",
            "Free zone companies that need accounts ready for audit or licence renewal",
            "Businesses whose books have fallen behind or no longer reconcile",
            "Companies preparing for VAT or Corporate Tax registration that need clean records first",
        ],
        "facts": [],
        "faq": [
            ("Do UAE free zone companies need to keep accounts?",
             "Yes. Under UAE Corporate Tax, businesses must keep accounting records and financial statements that support their tax returns, and many free zone authorities also require audited financial statements for licence renewal. The exact requirement depends on your free zone and licence, so we confirm what applies to you at the start."),
            ("Can you catch up on months of unrecorded transactions?",
             "Yes. Catch-up bookkeeping is a common starting point: we gather the bank statements and documents, rebuild the ledger and reconcile it, then move you onto a monthly routine."),
            ("How often will I receive reports?",
             "After each month-end close you receive your financial statements and management accounts. If you need weekly cash or sales reporting, we agree that as part of the scope."),
            ("Do you audit financial statements?",
             "No. We prepare your accounts and financial statements and support your auditor with schedules and explanations. The audit itself must be carried out by an independent licensed audit firm."),
            ("Do I need clean books before registering for VAT or Corporate Tax?",
             "You need records that support every figure you report. Registering is quicker and filing is far safer when the ledger is reconciled first, which is why we usually start there."),
        ],
        "related": ["vat-services-uae", "corporate-tax-uae", "mis-reporting-dubai"],
    },
    # ------------------------------------------------------------------ VAT
    {
        "slug": "vat-services-uae",
        "pillar": "FTA Compliance",
        "name": "VAT Services",
        "title": "VAT Registration, Returns & Refunds in the UAE | Accuminds",
        "description": "UAE VAT registration, quarterly and monthly VAT returns, refunds, voluntary disclosures and deregistration, handled against FTA requirements.",
        "h1": "VAT services in the UAE: registration, returns and refunds",
        "lead": "VAT registration, returns, refunds and corrections for UAE businesses, prepared against Federal Tax Authority requirements and filed on time.",
        "card": "Registration, VAT returns, refunds, voluntary disclosures and deregistration.",
        "tool": ("Supplier verification check", "/supplier-verification-check/"),
        "included": [
            ("VAT registration", "Threshold check, registration through the FTA's EmaraTax portal and set-up of your VAT codes."),
            ("VAT returns", "Quarterly or monthly returns prepared from reconciled books, with workings you can see."),
            ("Input VAT review", "Recoverable VAT checked invoice by invoice, so you claim what you are entitled to and nothing you are not."),
            ("VAT refunds", "Refund applications prepared with the supporting schedules the FTA asks for."),
            ("Voluntary disclosures", "Errors in past returns identified and corrected through the FTA's voluntary disclosure process."),
            ("VAT deregistration", "When your business no longer needs to be registered, we handle the deregistration steps."),
            ("VAT health checks", "A review of past returns and processes to find issues before they become penalties."),
        ],
        "who": [
            "Businesses approaching or above the AED 375,000 mandatory registration threshold",
            "Companies considering voluntary registration",
            "VAT-registered businesses that want returns prepared and reviewed professionally",
            "Anyone who suspects past returns contain errors",
        ],
        "facts": [
            ("Standard rate", "VAT in the UAE is charged at 5% and has applied since 1 January 2018.", MOF_VAT),
            ("Mandatory registration", "Registration is required once taxable supplies and imports exceed AED 375,000 over the previous 12 months, or are expected to within the next 30 days.", FTA_VAT_TOPIC),
            ("Voluntary registration", "Businesses whose taxable supplies and imports, or taxable expenses, exceed AED 187,500 may register voluntarily.", FTA_VAT_TOPIC),
            ("Return deadline", "Each VAT return is due no later than the 28th day after the end of the tax period (the next working day if that falls on a holiday), and must be filed even if no tax is payable.", FTA_VAT_REG),
        ],
        "faq": [
            ("When does a UAE business have to register for VAT?",
             "When its taxable supplies and imports have exceeded AED 375,000 over the previous 12 months, or are expected to exceed it within the next 30 days. Below that, registration is voluntary from AED 187,500."),
            ("How often are VAT returns filed in the UAE?",
             "Most businesses file quarterly; the FTA can assign monthly tax periods. Each return is due by the 28th day after the end of its tax period."),
            ("Do I file a VAT return if I had no sales?",
             "Yes. A registered business must file a return for every tax period, even when no tax is payable."),
            ("Can mistakes in previous VAT returns be fixed?",
             "Yes. Errors are corrected through a voluntary disclosure to the FTA. Correcting them before the FTA finds them is generally the better position, so we review past returns as part of onboarding."),
            ("Can I recover VAT on all my business expenses?",
             "Not always. Some input VAT is blocked from recovery, and recovery depends on having valid tax invoices. We check recoverability as we prepare each return."),
        ],
        "related": ["corporate-tax-uae", "e-invoicing-uae", "bookkeeping-accounting-dubai"],
    },
    # ------------------------------------------------------------------ Corporate Tax
    {
        "slug": "corporate-tax-uae",
        "pillar": "FTA Compliance",
        "name": "Corporate Tax Services",
        "title": "UAE Corporate Tax Registration & Returns | Accuminds",
        "description": "UAE Corporate Tax registration, tax returns, Small Business Relief and free zone qualifying income reviews for SMEs and free zone companies.",
        "h1": "UAE Corporate Tax services: registration, returns and relief",
        "lead": "Corporate Tax registration, returns and planning for UAE SMEs and free zone entities, built on reconciled books and filed within the deadline.",
        "card": "Registration, Corporate Tax returns, Small Business Relief and free zone reviews.",
        "tool": ("Free filing check", "/corporate-tax-check/"),
        "included": [
            ("Corporate Tax registration", "Registration with the FTA and confirmation of your tax period."),
            ("Taxable income computation", "From your financial statements to taxable income, with each adjustment documented."),
            ("Corporate Tax returns", "Returns prepared and submitted within the deadline, with the supporting workings kept on file."),
            ("Small Business Relief", "Eligibility checked each period and the election made in the return where it applies."),
            ("Free zone qualifying income review", "For free zone companies, a review of which income may qualify for the 0% rate and what conditions must be met."),
            ("Planning & structuring", "Advice on how your group, transactions and records should be set up for Corporate Tax."),
        ],
        "who": [
            "Mainland SMEs that must register and file, even with modest profits",
            "Free zone companies assessing qualifying income",
            "Businesses with revenue under AED 3 million considering Small Business Relief",
            "Companies whose first Corporate Tax return is approaching",
        ],
        "facts": [
            ("Rates", "0% on taxable income up to AED 375,000 and 9% on taxable income above that, for financial years starting on or after 1 June 2023.", ("Ministry of Finance: Corporate Tax", "https://mof.gov.ae/en/public-finance/tax/corporate-tax/")),
            ("Return & payment deadline", "Returns are filed and tax paid within nine months of the end of the tax period; for a year ending 31 December 2025 that was 30 September 2026.", FTA_SBR),
            ("Small Business Relief", "Resident businesses with revenue of AED 3 million or less may elect to be treated as having no taxable income, for tax periods ending on or before 31 December 2029. Registration and a return are still required.", MOF_SBR),
            ("Audited statements", "Audited financial statements are required for businesses with revenue above AED 50 million and for Qualifying Free Zone Persons (Ministerial Decision No. 84 of 2025).", ("Ministerial Decision No. 84 of 2025", "https://mof.gov.ae/wp-content/uploads/2025/04/Ministerial-Decision-No.-84-of-2025-on-Audited-Financial-Statements.pdf")),
        ],
        "faq": [
            ("Do I need to register for Corporate Tax if my profit is below AED 375,000?",
             "Yes. The AED 375,000 band is taxed at 0%, but it does not remove the obligation to register and file a return."),
            ("What is Small Business Relief?",
             "An election for resident businesses with revenue of AED 3 million or less to be treated as having no taxable income for the period. It is currently available for tax periods ending on or before 31 December 2029, and it is claimed in the Corporate Tax return, so you still need to register and file."),
            ("When is my Corporate Tax return due?",
             "Within nine months of the end of your tax period. For a financial year ending 31 December, that is 30 September of the following year."),
            ("Are free zone companies exempt from Corporate Tax?",
             "Not automatically. A Qualifying Free Zone Person can apply 0% to qualifying income if it meets the conditions, and pays 9% on other taxable income. We review your activities and income against those conditions."),
            ("Do I need audited financial statements for Corporate Tax?",
             "They are required if your revenue exceeds AED 50 million or you are a Qualifying Free Zone Person. Other businesses still need financial statements that support the return."),
        ],
        "related": ["vat-services-uae", "bookkeeping-accounting-dubai", "cfo-advisory-dubai"],
    },
    # ------------------------------------------------------------------ E-invoicing
    {
        "slug": "e-invoicing-uae",
        "pillar": "FTA Compliance",
        "name": "E-Invoicing Readiness",
        "title": "UAE E-Invoicing Readiness & ASP Onboarding | Accuminds",
        "description": "Get ready for UAE e-invoicing: timelines, accredited service provider onboarding, invoice data mapping and process changes for SMEs.",
        "h1": "E-invoicing in the UAE: readiness and onboarding",
        "lead": "The UAE is moving business invoices onto a mandatory electronic system. We help you work out what changes, appoint a provider and get your data ready in time.",
        "card": "Timelines, accredited service provider onboarding and invoice data readiness.",
        "tool": "Free readiness check",
        "included": [
            ("Readiness assessment", "Which of your invoices are in scope, when your deadlines fall and what your systems produce today."),
            ("Accredited service provider onboarding", "Support choosing and appointing an Accredited Service Provider (ASP) and connecting it to your accounting system."),
            ("Invoice data mapping", "Your invoice and customer data checked against the mandatory e-invoice fields, with the gaps fixed at source."),
            ("Process changes", "Credit notes, timing, approvals and exceptions adapted to how e-invoices are issued and received."),
            ("Testing & go-live", "Test invoices run before your mandatory date, then a supported switch-over."),
            ("Team guidance", "Short, practical guidance for the people who raise and approve invoices."),
        ],
        "who": [
            "Businesses with revenue of AED 50 million or more, which go live on 1 January 2027",
            "Businesses below AED 50 million, which go live on 1 July 2027",
            "Companies whose invoices are raised manually or in spreadsheets today",
            "Finance teams that want to adopt early, voluntarily",
        ],
        "facts": [
            ("Legal basis", "Ministerial Decisions No. 243 and 244 of 2025, amended by Ministerial Decisions No. 66 and No. 197 of 2026. Providers are accredited under Ministerial Decision No. 168 of 2026, and penalties are set by Cabinet Decision No. 173 of 2026.", MOF_EINV_GUIDELINES),
            ("Revenue of AED 50 million or more", "The deadline to appoint an Accredited Service Provider was 30 October 2026; if you have not appointed one, do it now. Implement by 1 January 2027.", MOF_EINV_GUIDELINES),
            ("Revenue below AED 50 million", "Appoint an Accredited Service Provider by 31 March 2027 and implement by 1 July 2027.", MOF_EINV_GUIDELINES),
            ("Government entities", "Appoint an Accredited Service Provider by 31 March 2027 and implement by 1 October 2027.", MOF_EINV_GUIDELINES),
            ("Voluntary adoption", "Businesses may implement e-invoicing voluntarily from 1 July 2026. Business-to-consumer invoices are excluded for now.", FTA_EINV),
            ("Tax group transactions", "Transactions between members of the same Tax Group are excluded from e-invoicing for 24 months from 1 January 2027 (Ministerial Decision No. 197 of 2026).", MOF_EINV_OCT),
            ("Record keeping", "Keep e-invoices, e-credit notes and their data for the period set by the Tax Procedures Law and provide them to the FTA on request. Since 1 October 2026 they no longer have to be stored inside the UAE.", MOF_EINV_OCT),
            ("Penalties", "Cabinet Decision No. 173 of 2026 replaced Cabinet Decision No. 106 of 2025. Not meeting the implementation obligations costs AED 5,000, then AED 5,000 for each month or part of a month it continues, up to AED 50,000 in any 12 consecutive months. There is no longer a penalty for not notifying a system failure, and only one penalty applies where the same business is both issuer and recipient.", MOF_EINV_PENALTIES),
            ("No penalties while voluntary", "E-invoicing penalties do not apply to e-invoices issued voluntarily before your mandatory date.", MOF_EINV_GUIDELINES),
        ],
        "faq": [
            ("When does e-invoicing become mandatory in the UAE?",
             "On 1 January 2027 for businesses with revenue of AED 50 million or more, on 1 July 2027 for businesses below that, and on 1 October 2027 for government entities. Each must appoint an Accredited Service Provider first: by 30 October 2026 for the first group (now passed), and by 31 March 2027 for the others."),
            ("What is an Accredited Service Provider (ASP)?",
             "A provider approved by the authorities to exchange and report e-invoices on your behalf. You appoint one and connect it to the system that raises your invoices."),
            ("Is a PDF invoice sent by email an e-invoice?",
             "No. Under the UAE system an e-invoice is a structured data file exchanged through accredited providers, not a PDF or scanned document."),
            ("Do invoices to individual consumers have to be e-invoices?",
             "Not for now. Business-to-consumer transactions are excluded from the current phase."),
            ("Are transactions within a tax group covered?",
             "Not at first. Ministerial Decision No. 197 of 2026 excludes transactions between members of the same Tax Group from e-invoicing for 24 months from 1 January 2027."),
            ("Do e-invoices have to be stored inside the UAE?",
             "No, not since Ministerial Decision No. 197 of 2026, effective 1 October 2026. You must still keep e-invoices, e-credit notes and their data for the period set by the Tax Procedures Law and provide them to the FTA on request."),
            ("What are the penalties for not implementing e-invoicing?",
             "Under Cabinet Decision No. 173 of 2026: AED 5,000 for the first violation of the implementation obligations, then AED 5,000 for each month or part of a month it continues, up to AED 50,000 in any 12 consecutive months. Penalties do not apply to e-invoices issued voluntarily before your mandatory date."),
            ("What should we do first?",
             "Confirm your revenue band and deadlines, check what your accounting system can export, and shortlist providers. That assessment is our first step with every client."),
        ],
        "related": ["vat-services-uae", "ai-accounting-automation-uae", "bookkeeping-accounting-dubai"],
    },
    # ------------------------------------------------------------------ CFO advisory
    {
        "slug": "cfo-advisory-dubai",
        "pillar": "CFO Advisory",
        "name": "CFO Advisory",
        "title": "Part-Time CFO Services in Dubai for SMEs | Accuminds",
        "description": "Part-time CFO support for UAE SMEs: budgets, rolling forecasts, cash-flow planning, working capital and board-ready reporting.",
        "h1": "Part-time CFO services in Dubai",
        "lead": "Senior finance support (forecasting, cash-flow planning and board-ready reporting) for growing UAE businesses that do not need a full-time CFO yet.",
        "card": "Budgets, forecasts, cash-flow planning and board / investor packs.",
        "included": [
            ("Budgets & rolling forecasts", "An annual budget and a forecast that is updated as the year unfolds."),
            ("Cash-flow planning", "A forward view of cash, so payroll, VAT and Corporate Tax payments never come as a surprise."),
            ("Working capital", "Receivables, payables and inventory managed to free up cash."),
            ("Board & investor packs", "Clear monthly or quarterly packs: results, explanations and the decisions they point to."),
            ("Pricing & margin analysis", "Which products, clients or projects make money, and which do not."),
            ("Structuring", "Advice on group structure and on mainland or free zone set-up as the business grows."),
        ],
        "who": [
            "Owner-managed businesses that have outgrown basic bookkeeping",
            "Companies preparing for a bank facility or investment",
            "Founders who want a finance partner for decisions, not just compliance",
            "Groups with several entities or branches",
        ],
        "facts": [],
        "experience": {
            "title": "Senior finance experience, part-time.",
            "lead": "CFO advisory at Accuminds is led by a qualified Cost and Management Accountant (CMA) with more than 20 years in financial control, business planning and treasury, working across the UAE, Saudi Arabia, Iraq (Kurdistan) and India.",
            "rows": [
                ("Planning and budgeting", "Annual operating plans and budgets, rolling forecasts, mid-term reviews and five-year business plans."),
                ("Cash and treasury", "Cash-flow management, banking facilities and foreign-exchange exposure, including hedging."),
                ("Commercial decisions", "Pricing of new products, business cases for tenders and new product lines, and make-or-buy analysis."),
                ("Controls and audits", "Month-end close, internal controls, and coordination with internal and external auditors."),
                ("Industries", "Oil and gas services, paper trading, automotive, capital markets, and consulting and audit."),
                ("Tools", "Excel financial models, Power BI dashboards and ERP systems."),
            ],
        },
        "faq": [
            ("What does a part-time CFO do?",
             "The same strategic work as a full-time CFO (forecasting, cash planning, reporting to owners or investors, and decision support) for a set number of days or hours each month."),
            ("When does an SME need a CFO?",
             "Typically when cash becomes hard to predict, when owners need numbers for decisions rather than just compliance, or when a bank or investor asks for forecasts."),
            ("How is CFO advisory different from accounting?",
             "Accounting records and reports what happened. CFO advisory uses those numbers to plan what happens next. We do both, so the forecast is built on the same books."),
            ("How is the engagement set up?",
             "We agree the scope and the regular outputs, such as the monthly pack and the forecast cycle, at the start, and review them as the business changes."),
        ],
        "related": ["mis-reporting-dubai", "bookkeeping-accounting-dubai", "corporate-tax-uae"],
    },
    # ------------------------------------------------------------------ MIS & reporting
    {
        "slug": "mis-reporting-dubai",
        "pillar": "MIS & Reporting",
        "name": "MIS & Reporting",
        "title": "MIS & Management Reporting Services in Dubai | Accuminds",
        "description": "Custom MIS and management reporting for UAE businesses: monthly management packs, KPIs, dashboards and budget vs actual analysis.",
        "h1": "MIS and management reporting in Dubai",
        "lead": "Custom MIS and management reporting that turn your ledger into clear, decision-ready numbers every month.",
        "card": "Management packs, KPIs, dashboards and variance analysis.",
        "tool": ("Free MIS template", "/mis-report-template/"),
        "included": [
            ("Monthly management packs", "Results, key ratios and short commentary, ready shortly after month-end."),
            ("KPIs & dashboards", "The handful of measures that matter for your business, tracked consistently."),
            ("Budget vs actual & variance analysis", "Where you are against plan, and why."),
            ("Profitability by segment", "Results by branch, department, project or product line."),
            ("Custom MIS design & set-up", "Cost centres, tracking categories and report layouts set up so the numbers can be produced reliably."),
            ("Automated reporting", "Reports refreshed from your ledger instead of rebuilt by hand in spreadsheets."),
        ],
        "who": [
            "Owners who get financial statements but still lack a clear monthly picture",
            "Businesses with several branches, projects or product lines",
            "Teams spending days each month assembling reports in spreadsheets",
            "Companies reporting to boards, partners or investors",
        ],
        "facts": [],
        "experience": {
            "title": "Built by someone who has produced MIS for 20 years.",
            "lead": "MIS and reporting at Accuminds is led by a qualified Cost and Management Accountant (CMA) with more than 20 years in management reporting, financial control and business planning, working across the UAE, Saudi Arabia, Iraq (Kurdistan) and India.",
            "rows": [
                ("Management reporting", "Monthly MIS packs, and consolidated profit and loss and balance sheet reporting with analysis against budget."),
                ("Variance and profitability", "Budget-versus-actual and quarterly variance reporting, and job, product and segment profitability."),
                ("Numbers you can trust", "Month-end close, accruals and cut-off, reconciliations including inventory, and internal controls behind every report."),
                ("Industries", "Oil and gas services, paper trading, automotive, capital markets, and consulting and audit."),
                ("Tools", "Excel financial models, Power BI dashboards and ERP systems."),
            ],
        },
        "faq": [
            ("What is MIS in accounting?",
             "A management information system: the structure, reports and dashboards that turn accounting data into information managers use to run the business."),
            ("What is in a monthly management pack?",
             "Typically the profit and loss against budget, cash position, receivables and payables, key performance indicators and short commentary on what changed and why."),
            ("How is MIS different from financial statements?",
             "Financial statements follow accounting standards and serve auditors, banks and regulators. MIS is designed around your decisions: by branch, product, project or whatever you manage by."),
            ("Can dashboards update automatically?",
             "Yes, when they are fed from a well-structured ledger. Part of setting up MIS is making sure the accounting data is coded in a way that reports can rely on."),
        ],
        "related": ["cfo-advisory-dubai", "ai-accounting-automation-uae", "bookkeeping-accounting-dubai"],
    },
    # ------------------------------------------------------------------ AI automation
    {
        "slug": "ai-accounting-automation-uae",
        "pillar": "AI Automation",
        "name": "AI Accounting Automation",
        "title": "AI Accounting Automation for UAE Businesses | Accuminds",
        "description": "AI-assisted invoice and receipt capture, reconciliation and approval workflows for UAE SMEs, with every entry reviewed before it is posted.",
        "h1": "AI accounting automation for UAE businesses",
        "lead": "AI-assisted intake and workflow automation that turns invoices and receipts into ledger entries ready for review, so your books stay current with less manual work.",
        "card": "Invoice and receipt capture, reconciliation and approval workflows.",
        "included": [
            ("Invoice & receipt capture", "Supplier invoices and receipts read automatically, in multiple languages."),
            ("Suggested coding", "Each document arrives with a suggested account and VAT treatment for review."),
            ("Reconciliation workflows", "Bank lines matched to documents, with exceptions flagged instead of hunted for."),
            ("Approval workflows", "Bills routed to the right person to approve before payment."),
            ("Accounting software integrations", "Automation connected to the accounting system you use."),
            ("Reporting from the ledger", "Clean, current data that feeds management reports and dashboards."),
        ],
        "who": [
            "Businesses with high volumes of invoices and receipts",
            "Teams still keying documents into the accounting system by hand",
            "Companies whose month-end is slowed by missing paperwork",
            "Businesses preparing for e-invoicing that want cleaner invoice data",
        ],
        "facts": [],
        "faq": [
            ("Does AI replace the accountant?",
             "No. AI handles capture and a first-pass suggestion; every entry is reviewed before it is posted to your ledger."),
            ("What documents can be processed?",
             "Supplier invoices, receipts and other supporting documents, including documents in more than one language."),
            ("Will it work with our accounting software?",
             "Automation is set up around the system you already use. We confirm the connection options during the assessment."),
            ("How does this relate to e-invoicing?",
             "E-invoicing makes invoices structured data, which suits automation well. Cleaning up your invoice data now helps with both."),
        ],
        "related": ["e-invoicing-uae", "mis-reporting-dubai", "bookkeeping-accounting-dubai"],
    },
]
