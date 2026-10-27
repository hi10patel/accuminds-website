"""Content for the e-invoicing software guides (/guides/...). Edit here, then run:
    python tools/build_pages.py

Same rules as pages_content.py: only state facts we can source, no invented
claims. Vendor and ASP statuses change: re-check them against the Ministry of
Finance list and the vendors' own pages on the date in CHECKED, and update it.
"""
from pages_content import MOF_EINV, MOF_EINV_GUIDE, MOF_EINV_OCT

CHECKED = "22 October 2026"

MOF_ASP = ("Ministry of Finance: eInvoicing Accredited Service Providers",
           "https://mof.gov.ae/en/about-us/initiatives/einvoicing/pre-approved-einvoicing-service-providers/")
PINT_AE = ("Peppol: PINT AE billing specification", "https://docs.peppol.eu/poac/ae/pint-ae/")
PINT_AE_RULES = ("Peppol: PINT AE specific rules",
                 "https://docs.peppol.eu/poac/ae/pint-ae/trn-invoice/rule/PINT-jurisdiction-aligned-rules/")
ZOHO_EINV = ("Zoho Books UAE: eInvoicing", "https://www.zoho.com/ae/books/e-invoicing/")
TALLY_MENA = ("TallyPrime Middle East", "https://tallysolutions.com/mena/")
QB_AE = ("QuickBooks UAE", "https://quickbooks.intuit.com/ae/")
ODOO_UAE = ("Odoo documentation: United Arab Emirates localization",
            "https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/united_arab_emirates.html")
ODOO_EDI = ("Odoo documentation: electronic invoicing (Peppol)",
            "https://www.odoo.com/documentation/19.0/applications/finance/accounting/customer_invoices/electronic_invoicing.html")

# Shared by every guide: the dates and the PINT AE data checks.
DEADLINES = [
    ("Revenue of AED 50 million or more", "Deadline to appoint an Accredited Service Provider: 30 October 2026 (if it has passed, appoint one now). E-invoicing applies from 1 January 2027.", MOF_EINV),
    ("Revenue below AED 50 million", "Appoint an Accredited Service Provider by 31 March 2027; e-invoicing applies from 1 July 2027.", MOF_EINV_GUIDE),
    ("Tax group transactions", "Transactions between members of the same Tax Group are excluded from e-invoicing for 24 months from 1 January 2027 (Ministerial Decision No. 197 of 2026).", MOF_EINV_OCT),
]

CHECKLIST = [
    ("Your TRN", "15 digits, starting with 1 and ending with 03, exactly as on your VAT certificate (IBR-132-AE)."),
    ("Customer TRNs", "Stored for VAT-registered customers; mandatory when an invoice line is VAT reverse charge (IBR-103-AE)."),
    ("VAT category per line", "Each line needs a category: S standard, Z zero rated, E exempt, O out of scope, AE reverse charge or N standard rate additional VAT (IBR-139-AE, IBR-145-AE)."),
    ("Document types", "Tax invoices (380), invoices out of scope of tax (480), credit notes (381) and credit notes for goods or services (81). Credit notes must reference the original invoice (IBR-055-AE)."),
    ("Item name and description", "Every line needs both (IBR-025, IBR-125-AE), so short codes alone are not enough."),
    ("Foreign-currency invoices", "Show the VAT total in AED and the exchange rate when the invoice is not in AED (IBR-159-AE, IBR-175-AE)."),
    ("Addresses", "Seller and buyer addresses need address line 1, city and emirate code: AUH, DXB, SHJ, UAQ, FUJ, AJM or RAK (IBR-128-AE, IBR-143-AE, IBR-144-AE)."),
    ("Line VAT amounts", "VAT is carried per line, and is zero on reverse charge and zero-rated lines (IBR-162-AE, IBR-165-AE)."),
]

GUIDES = [
    {
        "slug": "quickbooks-e-invoicing-uae",
        "software": "QuickBooks",
        "title": "QuickBooks UAE E-Invoicing: Connecting to an ASP | Accuminds",
        "description": "How QuickBooks users in the UAE meet the e-invoicing mandate: choosing an Accredited Service Provider, the data to fix first, and the deadlines.",
        "h1": "QuickBooks and UAE e-invoicing: connecting to an ASP",
        "lead": "QuickBooks is not a UAE Accredited Service Provider, so QuickBooks users exchange e-invoices through a separate accredited provider. Here is how to choose one, connect it and get your data ready.",
        "card": "QuickBooks is not an accredited provider: how to connect through one, and what to ask before you sign.",
        "answer": "QuickBooks Online is sold in the UAE, but Intuit is not on the Ministry of Finance list of eInvoicing Accredited Service Providers, and QuickBooks' UAE pages do not describe built-in e-invoicing. To comply, choose an Accredited Service Provider (ASP) that can take your invoices from QuickBooks, appoint it in EmaraTax, and clean your QuickBooks data so every invoice carries the fields the UAE format (PINT AE) requires.",
        "status": [
            ("Is QuickBooks an accredited provider?", "No. Intuit and QuickBooks do not appear on the Ministry of Finance list of eInvoicing Accredited Service Providers (checked " + CHECKED + ").", MOF_ASP),
            ("Does QuickBooks have built-in UAE e-invoicing?", "Not stated on QuickBooks' UAE website, which describes VAT tracking and invoicing but not Peppol or PINT AE e-invoicing (checked " + CHECKED + ").", QB_AE),
            ("What this means", "Your ASP sends and receives the e-invoices. QuickBooks stays your accounting system, connected to the ASP by an integration or a data export, depending on what the ASP offers.", MOF_ASP),
        ],
        "steps_title": "From QuickBooks to compliant e-invoices",
        "steps": [
            ("Check your invoice data", "Export a few recent invoices and credit notes and test them against the PINT AE fields below, or run them through our free readiness checker."),
            ("Shortlist ASPs that support QuickBooks", "Pick providers from the Ministry of Finance list and ask each one the questions below. Integration support differs between providers, so get the answers in writing."),
            ("Agree the contract, then appoint in EmaraTax", "You appoint your chosen ASP in EmaraTax. The ASP then onboards you and sets up your Peppol participant ID, which for UAE businesses is 0235 followed by your 10-digit TIN."),
            ("Fix data at the source", "Update customer TRNs, VAT categories, item descriptions and addresses in QuickBooks itself, so every new invoice is right first time."),
            ("Test, then go live", "Send test invoices and credit notes through the ASP, check what they reject, and confirm how incoming supplier e-invoices reach QuickBooks."),
        ],
        "questions_title": "Questions to ask an ASP before you sign",
        "questions": [
            ("How do you connect to QuickBooks?", "A direct integration with QuickBooks Online, an upload of exported files, or manual entry in your portal? Which QuickBooks plans are supported?"),
            ("Where do the PINT AE fields come from?", "How are TRNs, VAT category codes (including reverse charge), emirate codes and item descriptions mapped from QuickBooks?"),
            ("Credit notes and foreign currency", "Do credit notes keep the link to the original invoice, and do non-AED invoices carry the VAT total in AED?"),
            ("Incoming e-invoices", "How do supplier e-invoices you receive get into QuickBooks as bills?"),
            ("Pricing and support", "What is the price per invoice or per month, what does onboarding include, and who fixes rejected invoices?"),
        ],
        "faq": [
            ("Do I have to leave QuickBooks for UAE e-invoicing?", "No. You can keep QuickBooks and send e-invoices through an Accredited Service Provider that connects to it. Some businesses move to an accounting system with built-in e-invoicing instead; that is a choice, not a requirement."),
            ("Is QuickBooks an Accredited Service Provider in the UAE?", "No. Intuit and QuickBooks are not on the Ministry of Finance list of eInvoicing Accredited Service Providers as checked on " + CHECKED + "."),
            ("Is there a QuickBooks Peppol or PINT AE integration for the UAE?", "Not from QuickBooks itself: its UAE website does not describe Peppol or PINT AE e-invoicing (checked " + CHECKED + "). The integration comes from your Accredited Service Provider, which connects to QuickBooks or takes an export of your invoices and sends them in the PINT AE format over Peppol. Ask each provider how it connects to QuickBooks before you sign."),
            ("What is my Peppol ID?", "Once your ASP onboards you, your Peppol participant ID is 0235 followed by your 10-digit TIN."),
            ("When must my business appoint an ASP?", "The deadline is 30 October 2026 if your revenue is AED 50 million or more, and 31 March 2027 if it is below that. If your deadline has passed, appoint one as soon as possible."),
            ("Do e-invoices have to be stored inside the UAE?", "No, not since Ministerial Decision No. 197 of 2026, effective 1 October 2026. You must still keep them, with their data, for the period set by the Tax Procedures Law and provide them to the FTA on request."),
        ],
    },
    {
        "slug": "zoho-books-e-invoicing-uae",
        "software": "Zoho Books",
        "title": "Zoho Books UAE E-Invoicing: Setup & Checklist | Accuminds",
        "description": "Zoho is a UAE Accredited Service Provider. How Zoho Books users set up e-invoicing, appoint Zoho in EmaraTax, what it costs, and the data to fix before go-live.",
        "h1": "Zoho Books UAE e-invoicing: setup and data checklist",
        "lead": "Zoho is on the Ministry of Finance list of Accredited Service Providers and e-invoicing is built into Zoho Books, so most of the work is setup and data quality. Here is the order to do it in.",
        "card": "Zoho is an accredited provider with e-invoicing built in: the setup steps and the data to fix first.",
        "answer": "Zoho Software Trading LLC is a Ministry of Finance accredited eInvoicing Service Provider, and Zoho Books UAE creates, sends and receives e-invoices inside the product. You enter your tax IDs in Zoho Books' eInvoicing settings, appoint Zoho Software Trading LLC as your ASP in EmaraTax, and complete the setup in Zoho Books to connect to the Peppol network. The part that still needs care is your data: TRNs, VAT categories, item descriptions and addresses must meet the UAE format (PINT AE).",
        "status": [
            ("Is Zoho an accredited provider?", "Yes. Zoho Software Trading LLC is on the Ministry of Finance list, accreditation number 121988 (checked " + CHECKED + ").", MOF_ASP),
            ("Is e-invoicing built into Zoho Books?", "Yes. Zoho says e-invoices are created, exchanged and managed directly in Zoho Books.", ZOHO_EINV),
            ("What it costs, per Zoho", "Zoho states that the first 100 e-invoicing transactions are free on Professional and higher paid plans, with further packs from AED 41 per 100 transactions (checked " + CHECKED + ").", ZOHO_EINV),
        ],
        "steps_title": "Setting up e-invoicing in Zoho Books",
        "steps": [
            ("Check your plan", "Zoho's included e-invoicing transactions apply to Professional and higher paid plans, so confirm which plan you are on."),
            ("Enter your tax IDs", "Add the required tax IDs in Zoho Books' eInvoicing settings for your organisation."),
            ("Appoint Zoho in EmaraTax", "Log in to EmaraTax and select Zoho Software Trading LLC as your Accredited Service Provider."),
            ("Connect to Peppol", "Complete the eInvoicing setup in Zoho Books to connect your organisation to the Peppol network. Your Peppol participant ID is 0235 followed by your 10-digit TIN."),
            ("Clean your data and test", "Fix customer TRNs, VAT categories, item descriptions and addresses, then send test invoices and credit notes before your go-live date."),
        ],
        "questions_title": "What to check in your Zoho Books setup",
        "questions": [
            ("Customer records", "Every VAT-registered customer has a correct 15-digit TRN and a full address with the emirate."),
            ("Items", "Each item has a clear name and description, not just a short code."),
            ("Tax rates and categories", "Zero-rated, exempt, out-of-scope and reverse charge supplies use the right tax treatment, not a 0% standard rate."),
            ("Credit notes", "Credit notes are raised against the original invoice so the reference carries through."),
            ("Foreign currency", "Non-AED invoices show the VAT total in AED and the exchange rate."),
        ],
        "faq": [
            ("Is Zoho an Accredited Service Provider in the UAE?", "Yes. Zoho Software Trading LLC is on the Ministry of Finance list of eInvoicing Accredited Service Providers, accreditation number 121988, as checked on " + CHECKED + "."),
            ("Do I need a separate e-invoicing provider if I use Zoho Books?", "No. Zoho can act as your Accredited Service Provider, appointed in EmaraTax. You may still choose another accredited provider if you prefer."),
            ("How much does e-invoicing cost in Zoho Books?", "Zoho states that the first 100 e-invoicing transactions are free on Professional and higher paid plans, with packs from AED 41 per 100 transactions after that. Check Zoho's pricing page for current terms."),
            ("When must my business appoint an ASP?", "The deadline is 30 October 2026 if your revenue is AED 50 million or more, and 31 March 2027 if it is below that. If your deadline has passed, appoint one as soon as possible."),
            ("Do e-invoices have to be stored inside the UAE?", "No, not since Ministerial Decision No. 197 of 2026, effective 1 October 2026. You must still keep them, with their data, for the period set by the Tax Procedures Law and provide them to the FTA on request."),
        ],
    },
    {
        "slug": "tally-e-invoicing-uae",
        "software": "TallyPrime",
        "title": "TallyPrime UAE E-Invoicing: Setup & Checklist | Accuminds",
        "description": "Tally is a UAE Accredited Service Provider. How TallyPrime users prepare for e-invoicing, appoint Tally in EmaraTax and fix their masters first.",
        "h1": "TallyPrime UAE e-invoicing: ASP setup and data checklist",
        "lead": "Tally Software Solutions FZCO is on the Ministry of Finance list of Accredited Service Providers, and Tally says e-invoices are exchanged directly within TallyPrime. Here is how to prepare your company and masters.",
        "card": "Tally is an accredited provider: preparing your TallyPrime masters and appointing Tally in EmaraTax.",
        "answer": "Tally Software Solutions FZCO is a Ministry of Finance accredited eInvoicing Service Provider, and Tally says TallyPrime lets you exchange e-invoices directly within the product. To get ready, keep TallyPrime up to date, appoint Tally Software Solutions FZCO (or another accredited provider) in EmaraTax, and make sure your party and stock item masters hold what the UAE format (PINT AE) needs: TRNs, VAT categories, item descriptions and full addresses.",
        "status": [
            ("Is Tally an accredited provider?", "Yes. Tally Software Solutions FZCO is on the Ministry of Finance list, accreditation number 162503 (checked " + CHECKED + ").", MOF_ASP),
            ("Is e-invoicing built into TallyPrime?", "Tally says e-invoices are exchanged directly within TallyPrime, with unlimited e-invoices at no extra cost (checked " + CHECKED + ").", TALLY_MENA),
            ("What Tally does not publish", "Tally's Middle East website does not set out UAE-specific setup steps or a minimum release number, so confirm both with Tally or your Tally partner.", TALLY_MENA),
        ],
        "steps_title": "Preparing TallyPrime for UAE e-invoicing",
        "steps": [
            ("Update TallyPrime", "Move to the latest TallyPrime release and confirm with Tally or your Tally partner which release supports UAE e-invoicing."),
            ("Clean your party masters", "Each VAT-registered customer needs a correct 15-digit TRN and a full address with the emirate."),
            ("Clean your stock item masters", "Each item needs a clear name and description and the right VAT treatment: standard, zero rated, exempt, out of scope or reverse charge."),
            ("Appoint your ASP in EmaraTax", "Select Tally Software Solutions FZCO, or another accredited provider, in EmaraTax. Your Peppol participant ID is 0235 followed by your 10-digit TIN."),
            ("Test, then go live", "Send test invoices and credit notes, check rejections, and confirm how incoming supplier e-invoices are recorded in TallyPrime."),
        ],
        "questions_title": "What to check in your TallyPrime company",
        "questions": [
            ("VAT classifications", "Zero-rated, exempt, out-of-scope and reverse charge supplies are classified correctly, not entered as 0% standard."),
            ("Credit notes", "Credit notes reference the original invoice number."),
            ("Foreign currency", "Non-AED invoices show the VAT total in AED and the exchange rate."),
            ("Multiple companies", "If you run several companies in TallyPrime, or are part of a VAT group, confirm with your ASP how each legal entity is onboarded and identified."),
            ("Who supports you", "Agree who fixes rejected invoices: Tally, your Tally partner or your accountant."),
        ],
        "faq": [
            ("Is Tally an Accredited Service Provider in the UAE?", "Yes. Tally Software Solutions FZCO is on the Ministry of Finance list of eInvoicing Accredited Service Providers, accreditation number 162503, as checked on " + CHECKED + "."),
            ("Do I need a separate e-invoicing provider if I use TallyPrime?", "Not necessarily. You can appoint Tally Software Solutions FZCO as your Accredited Service Provider in EmaraTax, or choose another accredited provider."),
            ("Which TallyPrime release do I need?", "Tally's Middle East website does not state a minimum release for UAE e-invoicing. Update to the latest release and confirm with Tally or your Tally partner."),
            ("When must my business appoint an ASP?", "The deadline is 30 October 2026 if your revenue is AED 50 million or more, and 31 March 2027 if it is below that. If your deadline has passed, appoint one as soon as possible."),
            ("Do e-invoices have to be stored inside the UAE?", "No, not since Ministerial Decision No. 197 of 2026, effective 1 October 2026. You must still keep them, with their data, for the period set by the Tax Procedures Law and provide them to the FTA on request."),
        ],
    },
    {
        "slug": "odoo-e-invoicing-uae",
        "software": "Odoo",
        "title": "Odoo UAE E-Invoicing: ASP Connectors & Checklist | Accuminds",
        "description": "Odoo is not a UAE Accredited Service Provider. How Odoo users connect through an accredited provider for e-invoicing, and the data to fix first.",
        "h1": "Odoo and UAE e-invoicing: connectors and ASPs",
        "lead": "Odoo is not on the Ministry of Finance list of Accredited Service Providers, and its official UAE documentation does not cover e-invoicing. Odoo users connect through an accredited provider, usually with a connector module. Here is how to choose well.",
        "card": "Odoo is not an accredited provider: connector modules, choosing an ASP, and the data to fix first.",
        "answer": "Odoo S.A. is not on the Ministry of Finance list of eInvoicing Accredited Service Providers, and Odoo's official UAE localization documentation does not describe UAE e-invoicing (PINT AE). Odoo's own Peppol access point is documented for European countries, not the UAE. To comply, Odoo users appoint an Accredited Service Provider (ASP) in EmaraTax and connect Odoo to it, usually through a connector module, then make sure invoices carry the fields PINT AE requires.",
        "status": [
            ("Is Odoo an accredited provider?", "No. Odoo does not appear on the Ministry of Finance list of eInvoicing Accredited Service Providers (checked " + CHECKED + ").", MOF_ASP),
            ("Does Odoo's UAE localization cover e-invoicing?", "Not stated. Odoo's official UAE localization documentation covers VAT and invoice language but does not mention UAE e-invoicing, PINT AE or Peppol endpoint 0235 (checked " + CHECKED + ").", ODOO_UAE),
            ("Does Odoo's Peppol access point serve the UAE?", "Not as documented. Odoo's electronic invoicing documentation lists European countries for its Peppol access point; the UAE is not among them (checked " + CHECKED + ").", ODOO_EDI),
        ],
        "steps_title": "From Odoo to compliant e-invoices",
        "steps": [
            ("Note your Odoo version and hosting", "Odoo Online, Odoo.sh or on-premise, and which version. Connector modules differ by version and hosting, and some cannot be installed on Odoo Online."),
            ("Shortlist ASPs, then connectors", "Start from accredited providers on the Ministry of Finance list, then ask how each connects to Odoo. Several third-party connector modules exist; confirm the provider behind any module is on the official list."),
            ("Agree the contract, then appoint in EmaraTax", "You appoint your chosen ASP in EmaraTax. The ASP onboards you and sets up your Peppol participant ID, which for UAE businesses is 0235 followed by your 10-digit TIN."),
            ("Fix data at the source", "Update customer TRNs, taxes mapped to VAT categories, product descriptions and addresses with the emirate in Odoo, so every new invoice is right first time."),
            ("Test, then go live", "Send test invoices and credit notes through the ASP, check rejections, and confirm how incoming supplier e-invoices become vendor bills in Odoo."),
        ],
        "questions_title": "Questions to ask before you choose a connector",
        "questions": [
            ("Which ASP is behind it?", "Is the provider on the Ministry of Finance list today, and who supports you when an invoice is rejected: the module author or the ASP?"),
            ("Which Odoo versions and hosting?", "Does it support your exact version and Odoo Online, Odoo.sh or on-premise? What happens when you upgrade Odoo?"),
            ("How are PINT AE fields mapped?", "Where do VAT category codes (including reverse charge), emirate codes, item descriptions and AED totals for foreign-currency invoices come from?"),
            ("Credit notes and incoming invoices", "Do credit notes keep the link to the original invoice, and do received e-invoices arrive as draft vendor bills?"),
            ("Total cost", "Module licence, ASP fees per invoice or per month, implementation and annual support."),
        ],
        "faq": [
            ("Is Odoo an Accredited Service Provider in the UAE?", "No. Odoo is not on the Ministry of Finance list of eInvoicing Accredited Service Providers as checked on " + CHECKED + "."),
            ("Can I keep Odoo for UAE e-invoicing?", "Yes. Odoo can stay your accounting system; e-invoices are exchanged through an Accredited Service Provider, usually connected to Odoo with a connector module."),
            ("Does Odoo's own Peppol access point work in the UAE?", "Odoo's documentation lists European countries for its Peppol access point and does not include the UAE, so plan on an accredited UAE provider."),
            ("When must my business appoint an ASP?", "The deadline is 30 October 2026 if your revenue is AED 50 million or more, and 31 March 2027 if it is below that. If your deadline has passed, appoint one as soon as possible."),
            ("Do e-invoices have to be stored inside the UAE?", "No, not since Ministerial Decision No. 197 of 2026, effective 1 October 2026. You must still keep them, with their data, for the period set by the Tax Procedures Law and provide them to the FTA on request."),
        ],
    },
]
