"""Content for the PINT AE rule pages (/pint-ae-rules/...). Edit here, then run:
    python tools/build_pages.py

The checks themselves (descriptions, official references, fixes, notes) come from
tools/data/pint-ae-rules.json, the e-invoice checker's verified rule set, copied in by
`npm run sync:checker`. The text below only groups and explains them: every statement
must be traceable to that file or to the PINT AE specification it cites.
"""
import json
from pathlib import Path

RULES = json.loads((Path(__file__).parent / "data" / "pint-ae-rules.json").read_text(encoding="utf-8"))
SPEC_AS_OF = RULES["ruleset"]["spec_as_of"]  # e.g. "19 October 2026 (PINT AE Billing 1.0.4)"
BY_ID = {r["id"]: r for r in RULES["rules"]}

TOPICS = [
    {
        "slug": "seller-trn",
        "name": "Seller TRN",
        "title": "Seller TRN on UAE E-Invoices (IBR-132-AE) | Accuminds",
        "description": "How PINT AE checks the seller's TRN on a UAE e-invoice: the 15-digit format (IBR-132-AE), when it is required (IBR-134-AE) and how to fix errors.",
        "h1": "Seller TRN on UAE e-invoices (IBR-132-AE)",
        "card": "The 15-digit TRN format, and when PINT AE requires it.",
        "answer": "Your TRN goes in IBT-031, the seller VAT identifier. It must be 15 digits, starting with 1 and ending with 03 (IBR-132-AE). "
                  "It is required on tax invoices; PINT AE does not require it on invoice types 480 and 81 (IBR-134-AE), and a seller without a TRN may give a TIN in IBT-032 instead (IBR-177-AE).",
        "rules": ["AE-001"],
        "faq": [
            ("What format is a UAE TRN on a PINT AE e-invoice?", "15 digits, starting with 1 and ending with 03, with no spaces, dashes or prefix (IBR-132-AE)."),
            ("Is the seller TRN required on every invoice type?", "No. It is not required on invoice types 480 (out of scope of tax) and 81 (IBR-134-AE). A seller without a TRN may give a TIN in IBT-032 instead (IBR-177-AE)."),
        ],
    },
    {
        "slug": "buyer-trn",
        "name": "Buyer TRN",
        "title": "Buyer TRN on UAE E-Invoices (IBR-103-AE) | Accuminds",
        "description": "When the buyer's TRN is required on a UAE e-invoice under PINT AE, its format, the reverse charge rule (IBR-103-AE) and how to fix gaps.",
        "h1": "Buyer TRN on UAE e-invoices (IBT-048)",
        "card": "Optional for buyers without a TRN, required on reverse charge lines.",
        "answer": "The buyer's TRN goes in IBT-048, the buyer VAT identifier. PINT AE treats it as optional for buyers without a TRN, but when it is given it must follow the TRN format "
                  "(IBR-132-AE: 15 digits, starting with 1 and ending with 03), and it is required when any line is VAT reverse charge (IBR-103-AE). "
                  "Under UAE VAT law, a tax invoice to a VAT-registered buyer shows the buyer's TRN.",
        "rules": ["AE-002"],
        "faq": [
            ("Is the buyer TRN mandatory in PINT AE?", "Not for buyers without a TRN, but it is required when any invoice line is VAT reverse charge (IBR-103-AE). A tax invoice to a VAT-registered buyer should show the buyer's TRN under UAE VAT law."),
            ("Where should the buyer TRN be stored?", "In the customer master of your accounting system, so it prints on every invoice to that customer without retyping."),
        ],
    },
    {
        "slug": "peppol-participant-id",
        "name": "Peppol Participant ID",
        "title": "Peppol Participant ID for UAE E-Invoicing (0235) | Accuminds",
        "description": "The seller and buyer Peppol electronic addresses in PINT AE (IBT-034, IBT-049), the UAE 0235 scheme and TIN format, and who sets them up.",
        "h1": "Peppol Participant ID for UAE e-invoicing (0235)",
        "card": "IBT-034 and IBT-049, the 0235 scheme and the 10-digit TIN.",
        "answer": "Every e-invoice carries a Peppol electronic address for the seller (IBT-034) and the buyer (IBT-049), each with a scheme (IBT-034-1, IBT-049-1). "
                  "UAE identifiers use the 0235 scheme: for the seller it is the 10-digit TIN, 1XXXXXXXXX (IBR-148-AE); for the buyer it is the TIN or a predefined identifier, 9XXXXXXXXX (IBR-135-AE, IBR-149-AE). "
                  "Both are mandatory in PINT AE, and your Accredited Service Provider usually registers them during onboarding.",
        "rules": ["AE-003", "AE-004"],
        "faq": [
            ("What does a UAE Peppol Participant ID look like?", "The scheme 0235 followed by the identifier, written 0235:<TIN>. For a seller the identifier is the 10-digit TIN starting with 1 (IBR-148-AE)."),
            ("Who sets up my Peppol Participant ID?", "It is registered during onboarding with your Accredited Service Provider. Keep it in your accounting system's company profile in the format 0235:<TIN>."),
            ("Where do I find my TIN?", "It is the first 10 digits of your 15-digit TRN, according to the Ministry of Finance e-invoicing guidelines (version 2.0). In a tax group, use your own TRN, not the representative's."),
        ],
    },
    {
        "slug": "invoice-number-and-date",
        "name": "Invoice number and date",
        "title": "Invoice Number and Issue Date in PINT AE | Accuminds",
        "description": "PINT AE rules for the invoice number (IBT-001, IBR-002) and issue date (IBT-002, IBR-003) on UAE e-invoices, and the data errors to fix first.",
        "h1": "Invoice number and issue date in PINT AE",
        "card": "IBT-001 and IBT-002: unique numbers and valid dates.",
        "answer": "Every invoice and credit note needs an invoice number (IBT-001, IBR-002) that identifies it uniquely, and an issue date (IBT-002, IBR-003) recorded as a valid date. "
                  "Our checker also flags issue dates in the future, which are usually typing mistakes; that is a data-quality check, not a PINT AE business rule.",
        "rules": ["AE-005", "AE-006", "AE-007", "AE-008"],
        "faq": [
            ("Can two e-invoices share the same number?", "No. The invoice number (IBT-001) is defined as a unique identification of the invoice, so fix the numbering series in your system if a number repeats."),
            ("What date format should the issue date use?", "A real date rather than free text. Your Accredited Service Provider converts it to the format the e-invoice needs; an export with DD/MM/YYYY or YYYY-MM-DD dates is fine for checking."),
        ],
    },
    {
        "slug": "invoice-type-codes-and-credit-notes",
        "name": "Invoice type codes and credit notes",
        "title": "PINT AE Invoice Type Codes: 380, 480, 381, 81 | Accuminds",
        "description": "The four UAE e-invoice type codes in PINT AE (IBT-003) and the credit note rule (IBR-055-AE) that requires a reference to the original invoice.",
        "h1": "PINT AE invoice type codes: 380, 480, 381 and 81",
        "card": "Which code each document uses, and linking credit notes to invoices.",
        "answer": "Each document needs a type code (IBT-003, IBR-004). PINT AE uses 380 for a tax invoice, 480 for an invoice out of scope of tax, 381 for a credit note and 81 for a credit note related to goods or services. "
                  "Credit notes (381 and 81) must reference the original invoice (IBT-025, IBR-055-AE) unless the credit note reason code is VD.",
        "rules": ["AE-009", "AE-010"],
        "faq": [
            ("What is invoice type code 480 in the UAE?", "An invoice out of scope of tax. A tax invoice uses 380."),
            ("Does a UAE e-credit note need the original invoice number?", "Yes, for type codes 381 and 81, unless the credit note reason code is VD (IBR-055-AE)."),
        ],
    },
    {
        "slug": "currency-and-aed-vat",
        "name": "Currency and AED VAT",
        "title": "Foreign-Currency E-Invoices: AED VAT (IBR-175-AE) | Accuminds",
        "description": "PINT AE rules for the invoice currency (IBT-005) and for non-AED invoices: VAT total in AED (IBR-175-AE), exchange rate (IBR-159-AE) and AED totals.",
        "h1": "Foreign-currency e-invoices and the AED VAT total",
        "card": "ISO currency codes, and the AED figures a non-AED invoice needs.",
        "answer": "Every invoice needs an ISO 4217 currency code (IBT-005). The tax accounting currency is AED (IBR-140-AE), so an invoice in another currency must also show the VAT total in AED (IBR-175-AE), "
                  "the exchange rate (BTAE-04, IBR-159-AE) and the total with VAT in AED (BTAE-20).",
        "rules": ["AE-011", "AE-012"],
        "faq": [
            ("Can a UAE e-invoice be issued in US dollars?", "Yes. The invoice currency can be another ISO 4217 code, but the VAT total must also be shown in AED (IBR-175-AE), with the exchange rate (IBR-159-AE) and the total with VAT in AED (BTAE-20)."),
        ],
    },
    {
        "slug": "vat-category-codes",
        "name": "VAT category codes",
        "title": "PINT AE VAT Category Codes: S, Z, E, O, AE, N | Accuminds",
        "description": "The UAE e-invoice VAT category codes per line (IBT-151) and the matching VAT rates in PINT AE, including the 5.00 standard rate rule (IBR-190-AE).",
        "h1": "PINT AE VAT category codes: S, Z, E, O, AE and N",
        "card": "Mapping your tax codes to the six categories, with the right rates.",
        "answer": "Every invoice line needs a VAT category code (IBT-151): S standard rated, Z zero rated, E exempt, O out of scope, AE reverse charge and N standard rate additional VAT (IBR-145-AE, IBR-139-AE). "
                  "The line VAT rate (IBT-152) must match: 5.00 for the standard rate (IBR-190-AE), 0 for zero rated, no rate for exempt and out of scope, a rate for reverse charge, and a non-zero rate for additional VAT (IBR-111-AE).",
        "rules": ["AE-017", "AE-018"],
        "faq": [
            ("What does VAT category code AE mean on a UAE e-invoice?", "Reverse charge. Lines with category AE carry a VAT rate, a zero VAT amount (IBR-162-AE) and require the buyer's TRN (IBR-103-AE)."),
            ("What is the difference between Z, E and O?", "Z is zero rated (rate 0), E is exempt and O is out of scope; exempt and out-of-scope lines carry no VAT rate."),
        ],
    },
    {
        "slug": "invoice-lines",
        "name": "Invoice lines",
        "title": "Invoice Line Rules in PINT AE (IBR-147-AE) | Accuminds",
        "description": "What every UAE e-invoice line needs in PINT AE: item name and description, quantity, net price, line net amount (IBR-147-AE) and line VAT amount.",
        "h1": "Invoice line rules in PINT AE",
        "card": "Item names, quantities, prices, line totals and line VAT.",
        "answer": "Each line needs an item name (IBT-153, IBR-025) and description (IBT-154, IBR-125-AE), a quantity (IBT-129, IBR-022), a net price (IBT-146) and a line net amount (IBT-131, IBR-024). "
                  "The line net amount must equal quantity times net price (per base quantity), plus line charges, minus line allowances (IBR-147-AE). Each line also carries its VAT amount (BTAE-08), "
                  "which is zero on reverse charge and zero-rated lines (IBR-162-AE, IBR-165-AE).",
        "rules": ["AE-013", "AE-014", "AE-015", "AE-016", "AE-019", "AE-020"],
        "faq": [
            ("Is a short item code enough as the line description?", "No. PINT AE carries an item name (IBR-025) and an item description (IBR-125-AE), so each line needs a readable description of the goods or services."),
            ("Why does the line net amount not match quantity times price?", "Usually because prices are stored with VAT included, a line discount is missing, or the amount is not rounded to 2 decimals (IBR-147-AE)."),
        ],
    },
    {
        "slug": "invoice-totals",
        "name": "Invoice totals",
        "title": "Invoice Totals in PINT AE (IBR-CO-10 to CO-15) | Accuminds",
        "description": "How the totals on a UAE e-invoice must add up under PINT AE: line net sum, total excluding VAT, VAT total and total including VAT.",
        "h1": "Invoice totals in PINT AE",
        "card": "Why totals must add up exactly, and the usual causes when they don't.",
        "answer": "The sum of line net amounts (IBT-106, IBR-CO-10) feeds the total excluding VAT (IBT-109, IBR-CO-13); the VAT total (IBT-110) must equal the sum of the VAT breakdown amounts (IBR-CO-14); "
                  "and the total including VAT (IBT-112) must equal the total excluding VAT plus the VAT total (IBR-CO-15). Header-level discounts, rounding lines and a different VAT rounding method (per line or per invoice) are the usual causes of a mismatch.",
        "rules": ["AE-021", "AE-022", "AE-023"],
        "faq": [
            ("Why is my e-invoice VAT total off by a few fils?", "Usually the system rounds VAT per invoice while the lines are rounded individually, or the other way round. Align the rounding method so the VAT total equals the sum of line VAT amounts."),
        ],
    },
    {
        "slug": "seller-and-buyer-details",
        "name": "Seller and buyer details",
        "title": "Seller and Buyer Name and Address in PINT AE | Accuminds",
        "description": "PINT AE rules for seller and buyer legal names and addresses on UAE e-invoices, including the emirate codes AUH, DXB, SHJ, UAQ, FUJ, AJM and RAK.",
        "h1": "Seller and buyer names and addresses in PINT AE",
        "card": "Legal names, address lines, cities and emirate codes.",
        "answer": "The seller's legal name (IBT-027, IBR-006) and postal address (IBG-05) are required, with address line 1, city and emirate (IBR-143-AE). "
                  "The buyer's name (IBT-044, IBR-007) and postal address (IBG-08) follow the same pattern (IBR-144-AE). Emirates use the codes AUH, DXB, SHJ, UAQ, FUJ, AJM and RAK.",
        "rules": ["AE-024", "AE-025", "AE-026", "AE-027"],
        "faq": [
            ("What are the emirate codes on a UAE e-invoice?", "AUH (Abu Dhabi), DXB (Dubai), SHJ (Sharjah), UAQ (Umm Al Quwain), FUJ (Fujairah), AJM (Ajman) and RAK (Ras Al Khaimah)."),
            ("Which name should appear as the seller name?", "Your legal name exactly as on your trade licence and TRN certificate."),
        ],
    },
]

HUB = {
    "title": "UAE PINT AE E-Invoice Rules, Explained | Accuminds",
    "description": "Plain-English guide to the PINT AE rules UAE e-invoices are checked against: TRNs, Peppol IDs, type codes, VAT categories, lines and totals.",
    "h1": "UAE PINT AE e-invoice rules, explained",
    "lead": "The rules behind UAE e-invoices, grouped by topic, with the official rule numbers, what each one means and how to fix the usual data problems.",
    "faq": [
        ("What is PINT AE?", "The UAE's version of the Peppol International (PINT) billing specification: the data model and business rules every UAE e-invoice is validated against. These pages follow PINT AE Billing 1.0.4."),
        ("Who applies these rules to my invoices?", "Your Accredited Service Provider validates each e-invoice before it is exchanged, so data that breaks a rule has to be fixed in your accounting system first."),
        ("How can I check my invoices against these rules?", "Export a few recent invoices from your accounting system and run them through our free e-invoice readiness checker. It reads the file in your browser and lists the gaps, rule by rule."),
    ],
}

for _t in TOPICS:
    assert all(r in BY_ID for r in _t["rules"]), _t["slug"]
assert sorted(r for t in TOPICS for r in t["rules"]) == sorted(BY_ID), "every checker rule belongs to one topic"
