"""Builds the service pages from tools/pages_content.py.

    python tools/build_pages.py

Writes:
  services/index.html                 services hub
  services/<slug>/index.html          one page per service
  guides/index.html                   e-invoicing software guides hub (tools/guides_content.py)
  mis-report-template/index.html      free MIS pack download (file: tools/build_mis_template.py)
  corporate-tax-check/index.html      Corporate Tax filing check (logic: assets/js/ct-check.js)
  supplier-verification-check/        FTA Decision 13 supplier checks (logic: assets/js/supplier-check.js)
  gratuity-calculator/                UAE end-of-service gratuity (logic: assets/js/gratuity.js)
  guides/<slug>/index.html            one page per guide
  pint-ae-rules/                      PINT AE rules hub and topic pages (tools/pint_rules_content.py)
  sitemap.xml, llms.txt               regenerated from the same content
  index.html                          refreshes the footer service links
                                      (between the SERVICE-LINKS markers)
  CSS/JS version tags                 on every page, via tools/asset_versions.py
The pages share the home page's CSS/JS, header and footer. Paths are
root-absolute (/assets/...), which works on the custom domain and in
`npm run serve`.
"""
import json
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from pages_content import FTA_VAT_REG, FTA_VAT_TOPIC, REVIEWED, SERVICES  # noqa: E402
from guides_content import CHECKED, CHECKLIST, DEADLINES, GUIDES, MOF_ASP, PINT_AE, PINT_AE_RULES  # noqa: E402
from asset_versions import stamp_all  # noqa: E402
from pint_rules_content import BY_ID as PINT_BY_ID, HUB as PINT_HUB, SPEC_AS_OF, TOPICS as PINT_TOPICS  # noqa: E402

SITE = "https://www.accumindsconsulting.ae"
WA = "971509867247"
TODAY = date.today().isoformat()
BY_SLUG = {s["slug"]: s for s in SERVICES}
ORG_ID = f"{SITE}/#organization"
# Free resources on this site.
MIS_TEMPLATE = {"path": "/mis-report-template/", "file": "/assets/downloads/accuminds-monthly-mis-template.xlsx",
                "name": "Free Monthly MIS Report Template",
                "card": "An Excel MIS pack for SMEs: P&L against budget, KPIs, working-capital days, a three-month cash outlook and commentary prompts."}
CT_CHECK = {"path": "/corporate-tax-check/", "name": "Corporate Tax Filing Check",
            "card": "Answer up to five questions to see whether you must register and file for UAE Corporate Tax, and whether Small Business Relief may apply."}
CT_CHECKED = "22 October 2026"
SV_CHECK = {"path": "/supplier-verification-check/", "name": "Supplier Verification Check (VAT)",
            "pdf": "/assets/downloads/accuminds-supplier-verification-checklist.pdf",
            "card": "Which FTA Decision 13 of 2026 checks apply before you claim input VAT on a supplier's invoice, with a printable checklist."}
FTA_DEC13 = ("FTA Decision No. 13 of 2026 (unofficial English translation)",
             "https://tax.gov.ae/Datafolder/Files/Legislation/2026/FTA%20Decision%20No.%2013%20of%202026%20on%20Measures%2018%2008%202026.pdf")
TRN_CHECK = {"path": "/trn-verification-uae/", "name": "TRN Verification and Format Check",
             "card": "Check that a UAE TRN has the right format, then confirm it on the FTA website: the steps, and when a TRN must be on a tax invoice."}
TRN_CHECKED = "31 October 2026"
FTA_HOME = ("FTA website: TRN/TIN verification", "https://tax.gov.ae/en/default.aspx")
VAT_EXEC_REG = ("UAE Legislation: Cabinet Resolution No. 52 of 2017", "https://uaelegislation.gov.ae/en/legislations/1226")
VAT_REG = {"path": "/vat-registration-uae/", "name": "VAT Registration Check",
           "card": "Do you have to register for UAE VAT, or can you choose to? Check the AED 375,000 and AED 187,500 thresholds, then see the documents and EmaraTax steps."}
VAT_REG_CHECKED = "31 October 2026"
CT_REG = {"path": "/corporate-tax-registration-uae/", "name": "Corporate Tax Registration Deadline",
          "card": "Find your UAE Corporate Tax registration deadline under FTA Decision No. 3 of 2024, then see the documents, EmaraTax steps and the late registration penalty waiver."}
CT_REG_CHECKED = "31 October 2026"
FTA_CT_REG = ("FTA: Corporate Tax registration service", "https://tax.gov.ae/en/services/corporate.tax.registration.aspx")
FTA_DEC3 = ("FTA Decision No. 3 of 2024 (unofficial translation)",
            "https://tax.gov.ae/Datafolder/Files/Legislation/FTA%20Decision%20No.%203%20of%202024%20on%20Registration%20Timeline%20for%20Corporate%20Tax%20-%20For%20publishing.pdf")
FTA_PENALTIES = ("FTA: Cabinet Decision No. 40 of 2017 as amended (unofficial translation)",
                 "https://tax.gov.ae/Datafolder/Files/Legislation/2025/Cabinet%20Decision%20No.%2040%20of%202017%20and%20its%20amendments%20-%20publishing%2011%202025.pdf")
# Free tool published from the uae-einvoice-checker repo (npm run sync:checker).
GRATUITY = {"path": "/gratuity-calculator/", "name": "UAE Gratuity Calculator",
            "card": "End-of-service gratuity under the federal Labour Law: 21 and 30 days' basic wage, part years, part-time work and the cap."}
GRATUITY_CHECKED = "28 October 2026"
LABOUR_LAW = ("UAE Legislation: Federal Decree-Law No. 33 of 2021", "https://uaelegislation.gov.ae/en/legislations/1541")
EXEC_REG = ("UAE Legislation: Cabinet Resolution No. 1 of 2022", "https://uaelegislation.gov.ae/en/legislations/1547")
PINT_RULES = {"path": "/pint-ae-rules/", "name": "PINT AE Rules Explained",
              "card": "The PINT AE rules UAE e-invoices are validated against, grouped by topic, with official rule numbers and fixes."}
CHECKER = {"path": "/e-invoice-checker/", "name": "Free E-Invoice Readiness Checker",
           "card": "Check sample sales invoices against the UAE e-invoicing (PINT AE) mandatory fields in your browser, with a readiness score, gap list and PDF report."}
FONT = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap"

e = lambda t: escape(t, quote=True)  # noqa: E731


def url(slug=None):
    return f"{SITE}/services/{slug}/" if slug else f"{SITE}/services/"


def guide_url(slug=None):
    return f"{SITE}/guides/{slug}/" if slug else f"{SITE}/guides/"


def pint_url(slug=None):
    return f"{SITE}{PINT_RULES['path']}{slug + '/' if slug else ''}"


def wa_link(topic):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(f'Hello Accuminds, I would like to discuss {topic}.')}"


SPRITE = """  <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
    <defs>
      <symbol id="i-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3.5a8.5 8.5 0 0 0-7.3 12.8L3.5 20.5l4.3-1.1A8.5 8.5 0 1 0 12 3.5z" />
        <path d="M9.3 8.4c.4-.5 1-.4 1.2.1l.6 1.4c.1.3 0 .6-.2.8l-.5.5a6 6 0 0 0 2.6 2.6l.5-.5c.2-.2.5-.3.8-.2l1.4.6c.5.2.6.8.1 1.2-.8.6-1.8.8-2.8.3a8.3 8.3 0 0 1-3.9-3.9c-.5-1-.3-2.1.2-2.9z" fill="currentColor" stroke="none" />
      </symbol>
      <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5" /></symbol>
      <symbol id="i-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14" /></symbol>
    </defs>
  </svg>"""


def head(title, description, canonical, ld):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <meta name="theme-color" content="#1A2E4A" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Accuminds Consulting FZCO" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(description)}" />
  <meta property="og:image" content="{SITE}/assets/img/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/png" href="/assets/img/favicon-32.png" sizes="32x32" />
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
  <script>
    (function (h) {{
      h.classList.add('js');
      if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {{
        h.classList.add('js-motion');
        setTimeout(function () {{ if (!window.__amMotion) h.classList.remove('js-motion'); }}, 3000);
      }}
    }})(document.documentElement);
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="{FONT}" />
  <link rel="stylesheet" href="{FONT}" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="{FONT}" /></noscript>
  <link rel="stylesheet" href="/assets/css/tokens.css" />
  <link rel="stylesheet" href="/assets/css/main.css" />
  <script defer src="/assets/vendor/gsap-3.15.0.min.js"></script>
  <script defer src="/assets/vendor/ScrollTrigger-3.15.0.min.js"></script>
  <script defer src="/assets/vendor/lenis-1.3.27.min.js"></script>
  <script type="module" src="/assets/js/main.js"></script>
</head>"""


HEADER = """  <header class="site-header" id="site-header">
    <div class="container header-inner">
      <a class="brand" href="/" aria-label="Accuminds Consulting, home">
        <img src="/assets/img/mark-3d.webp" width="88" height="32" alt="" />
        <span class="wordmark">Accuminds</span>
      </a>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
        <ul>
          <li><a class="u-link" href="/services/">Services</a></li>
          <li><a class="u-link" href="/guides/">Guides</a></li>
          <li><a class="u-link" href="/#process">How we work</a></li>
          <li><a class="u-link" href="/#about">About</a></li>
          <li><a class="u-link" href="/#contact">Contact</a></li>
        </ul>
        <a class="btn btn-gold nav-cta" href="/#contact">Book a consultation</a>
      </nav>
      <a class="btn btn-gold btn-sm header-cta" href="/#contact" data-magnetic>Book a consultation</a>
      <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false">
        <span class="sr-only">Open menu</span>
        <span class="nav-toggle__bars" aria-hidden="true"></span>
      </button>
    </div>
  </header>"""


def footer_columns(current=None, base="/services/"):
    """Footer links in three labelled columns: services, free tools, guides.
    Labels are short because the column heading carries "Free"; the pages keep their full names."""
    def li(href, name, cur=False):
        attr = ' aria-current="page"' if cur else ""
        return f'<li><a class="u-link" href="{href}"{attr}>{e(name)}</a></li>'

    cols = [
        ("Services", [li(f'{base}{s["slug"]}/', s["name"], s["slug"] == current) for s in SERVICES]),
        ("Free tools", [
            li(CHECKER["path"], "E-Invoice Readiness Checker"),
            li(CT_CHECK["path"], "Corporate Tax Filing Check"),
            li(SV_CHECK["path"], "Supplier Verification Check (VAT)"),
            li(VAT_REG["path"], "VAT Registration Check"),
            li(CT_REG["path"], "Corporate Tax Registration Deadline"),
            li(TRN_CHECK["path"], "TRN Verification"),
            li(MIS_TEMPLATE["path"], "MIS Report Template"),
            li(GRATUITY["path"], "Gratuity Calculator"),
        ]),
        ("Guides", [
            li("/guides/", "E-Invoicing Software Guides"),
            li(PINT_RULES["path"], "PINT AE Rules Explained"),
        ]),
    ]
    out = []
    for title, items in cols:
        links = "\n            ".join(items)
        out.append(f"""        <nav class="footer-col" aria-label="{title}">
          <p class="footer-col__title">{title}</p>
          <ul class="footer-links">
            {links}
          </ul>
        </nav>""")
    return '      <div class="footer-cols">\n' + "\n".join(out) + "\n      </div>"


def footer(current=None):
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      <a class="footer-brand" href="/">
        <img src="/assets/img/mark-3d.webp" width="77" height="28" alt="" loading="lazy" decoding="async" />
        <span class="wordmark-light">Accuminds Consulting · FZCO</span>
      </a>
{footer_columns(current)}
      <address class="footer-meta">
        DSO – IFZA, IFZA Properties, Dubai Silicon Oasis, Dubai, UAE ·
        <a class="u-link" href="mailto:info@accumindsconsulting.ae">info@accumindsconsulting.ae</a> ·
        <a class="u-link" href="tel:+971509867247">+971 50 98 67247</a> ·
        <a class="u-link" href="https://www.linkedin.com/company/accuminds-consulting/" rel="me noopener" target="_blank">LinkedIn</a> ·
        <a class="u-link" href="https://www.google.com/maps?cid=9046261605626005493" rel="noopener" target="_blank">Google Maps</a>
      </address>
      <p class="footer-copy">© <span data-year>{date.today().year}</span> Accuminds Consulting FZCO. All rights reserved.</p>
    </div>
  </footer>"""


def org_node():
    return {
        "@type": "ProfessionalService", "@id": ORG_ID, "name": "Accuminds Consulting FZCO", "url": f"{SITE}/",
        "telephone": "+971509867247", "email": "info@accumindsconsulting.ae",
        "sameAs": ["https://www.linkedin.com/company/accuminds-consulting/", "https://www.google.com/maps?cid=9046261605626005493"],
        "hasMap": "https://www.google.com/maps?cid=9046261605626005493",
        "address": {"@type": "PostalAddress", "streetAddress": "DSO - IFZA, IFZA Properties, Dubai Silicon Oasis",
                    "addressLocality": "Dubai", "addressRegion": "Dubai", "addressCountry": "AE"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "09:00", "closes": "19:00"}],
    }


def breadcrumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]}


def breadcrumbs_html(trail):
    parts = []
    for i, (name, link) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<li aria-current="page">{e(name)}</li>')
        else:
            parts.append(f'<li><a class="u-link" href="{link.replace(SITE, "") or "/"}">{e(name)}</a></li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def cta_band(topic):
    return f"""    <section class="section section--dark cta-band">
      <div class="container cta-inner">
        <h2 data-reveal="mask">Let&rsquo;s talk about {e(topic)}.</h2>
        <p class="lead" data-reveal>Tell us where things stand. We reply within two business days.</p>
        <div class="hero-ctas" data-reveal-stagger>
          <a class="btn btn-gold" href="/#contact" data-magnetic>Book a consultation</a>
          <a class="btn btn-whatsapp" href="{e(wa_link(topic))}" target="_blank" rel="noopener" data-magnetic>
            <svg class="icon" aria-hidden="true"><use href="#i-whatsapp" /></svg> Chat on WhatsApp<span class="sr-only"> (opens WhatsApp)</span>
          </a>
        </div>
      </div>
    </section>"""


def service_page(s):
    canonical = url(s["slug"])
    trail = [("Home", f"{SITE}/"), ("Services", url()), (s["name"], canonical)]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "Service", "@id": f"{canonical}#service", "name": s["name"], "serviceType": s["name"],
         "description": s["description"], "url": canonical, "provider": {"@id": ORG_ID},
         "areaServed": {"@type": "Country", "name": "United Arab Emirates"},
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["name"], "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}} for n, d in s["included"]]}},
        breadcrumbs_ld(trail),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]},
    ]}

    included = "\n".join(
        f'          <li class="incl"><h3>{e(n)}</h3><p>{e(d)}</p></li>' for n, d in s["included"])
    who = "\n".join(
        f'          <li><svg class="icon" aria-hidden="true"><use href="#i-check" /></svg>{e(w)}</li>' for w in s["who"])
    faq = "\n".join(
        f"""          <details class="faq-item">
            <summary><h3>{e(q)}</h3><svg class="icon" aria-hidden="true"><use href="#i-plus" /></svg></summary>
            <p>{e(a)}</p>
          </details>""" for q, a in s["faq"])
    related = "\n".join(
        f"""          <a class="related-card" href="/services/{r}/"><span class="related-name">{e(BY_SLUG[r]["name"])}</span><span class="related-desc">{e(BY_SLUG[r]["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""
        for r in s["related"])

    experience_section = ""
    if s.get("experience"):
        x = s["experience"]
        rows = "\n".join(f'          <div class="fact-row"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for t, d in x["rows"])
        experience_section = f"""
    <section class="section" aria-labelledby="experience-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Experience behind the service</p>
          <h2 id="experience-title" data-reveal="mask">{e(x["title"])}</h2>
          <p class="lead" data-reveal>{e(x["lead"])}</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{rows}
        </dl>
      </div>
    </section>"""

    facts_section = ""
    if s["facts"]:
        rows = "\n".join(
            f"""          <div class="fact-row"><dt>{e(t)}</dt><dd>{e(d)} <a class="fact-src u-link" href="{e(src[1])}" target="_blank" rel="noopener">{e(src[0])}<span class="sr-only"> (opens in a new tab)</span></a></dd></div>"""
            for t, d, src in s["facts"])
        facts_section = f"""
    <section class="section" aria-labelledby="facts-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Key facts</p>
          <h2 id="facts-title" data-reveal="mask">The rules, in brief.</h2>
          <p class="lead" data-reveal>From official UAE sources, last reviewed {e(REVIEWED)}. Rules change, so we confirm what applies to your business before acting.</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{rows}
        </dl>
      </div>
    </section>"""

    tool_cta = ""
    if s.get("tool"):
        label, path = s["tool"] if isinstance(s["tool"], tuple) else (s["tool"], CHECKER["path"])
        tool_cta = f"""
          <a class="btn btn-ghost-light" href="{path}" data-magnetic>{e(label)} <span aria-hidden="true">&rarr;</span></a>"""

    body = f"""{head(s["title"], s["description"], canonical, ld)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{HEADER}

  <main id="main">
    <section class="page-hero on-dark" aria-labelledby="page-title">
      <div class="container">
        {breadcrumbs_html(trail)}
        <p class="eyebrow" data-reveal>{e(s["pillar"])}</p>
        <h1 id="page-title" data-reveal="mask">{e(s["h1"])}</h1>
        <p class="lead" data-reveal>{e(s["lead"])}</p>
        <div class="hero-ctas" data-reveal-stagger>
          <a class="btn btn-gold" href="/#contact" data-magnetic>Book a consultation</a>
          <a class="btn btn-ghost-light" href="{e(wa_link(s["name"]))}" target="_blank" rel="noopener" data-magnetic>
            <svg class="icon" aria-hidden="true"><use href="#i-whatsapp" /></svg> WhatsApp us<span class="sr-only"> (opens WhatsApp)</span>
          </a>{tool_cta}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="included-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>What&rsquo;s included</p>
          <h2 id="included-title" data-reveal="mask">What we handle for you.</h2>
        </div>
        <ul class="incl-grid" data-reveal-stagger>
{included}
        </ul>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="who-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Who it&rsquo;s for</p>
          <h2 id="who-title" data-reveal="mask">Built for businesses like yours.</h2>
        </div>
        <ul class="who-list" data-reveal-stagger>
{who}
        </ul>
      </div>
    </section>
{experience_section}{facts_section}
    <section class="section section--white" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="related-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Related</p>
          <h2 id="related-title" data-reveal="mask">Often handled together.</h2>
        </div>
        <div class="related-grid" data-reveal-stagger>
{related}
        </div>
      </div>
    </section>

{cta_band(s["name"])}
  </main>

{footer(s["slug"])}
</body>
</html>
"""
    out = ROOT / "services" / s["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def hub_page():
    canonical = url()
    trail = [("Home", f"{SITE}/"), ("Services", canonical)]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(), breadcrumbs_ld(trail),
        {"@type": "ItemList", "name": "Accuminds services", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": url(s["slug"]), "name": s["name"]} for i, s in enumerate(SERVICES)]},
    ]}
    cards = "\n".join(
        f"""          <a class="related-card" href="/services/{s["slug"]}/"><span class="related-pillar">{e(s["pillar"])}</span><span class="related-name">{e(s["name"])}</span><span class="related-desc">{e(s["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""
        for s in SERVICES)
    body = f"""{head("Accounting, Tax & CFO Services in Dubai | Accuminds",
                 "Accounting, VAT, Corporate Tax, e-invoicing, CFO advisory, MIS reporting and AI automation for UAE SMEs and free zone companies.",
                 canonical, ld)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{HEADER}

  <main id="main">
    <section class="page-hero on-dark" aria-labelledby="page-title">
      <div class="container">
        {breadcrumbs_html(trail)}
        <p class="eyebrow" data-reveal>Our services</p>
        <h1 id="page-title" data-reveal="mask">Finance, tax and automation for UAE businesses.</h1>
        <p class="lead" data-reveal>Five disciplines, one accountable firm. Choose a service to see what is included, who it is for and the rules that apply.</p>
      </div>
    </section>

    <section class="section" aria-label="All services">
      <div class="container">
        <div class="related-grid related-grid--all" data-reveal-stagger>
{cards}
        </div>
      </div>
    </section>

{cta_band("your books")}
  </main>

{footer()}
</body>
</html>
"""
    out = ROOT / "services" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def fact_rows(rows):
    return "\n".join(
        f"""          <div class="fact-row"><dt>{e(t)}</dt><dd>{e(d)} <a class="fact-src u-link" href="{e(src[1])}" target="_blank" rel="noopener">{e(src[0])}<span class="sr-only"> (opens in a new tab)</span></a></dd></div>"""
        for t, d, src in rows)


def guide_page(g):
    canonical = guide_url(g["slug"])
    trail = [("Home", f"{SITE}/"), ("Guides", guide_url()), (g["software"], canonical)]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "Article", "@id": f"{canonical}#article", "headline": g["h1"], "description": g["description"],
         "url": canonical, "inLanguage": "en", "dateModified": TODAY, "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
         "about": [{"@type": "Thing", "name": "UAE e-invoicing"}, {"@type": "SoftwareApplication", "name": g["software"]}]},
        breadcrumbs_ld(trail),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]},
    ]}
    steps = "\n".join(f'          <li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in g["steps"])
    questions = "\n".join(f'          <li class="incl"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in g["questions"])
    checklist = "\n".join(
        f'          <div class="fact-row"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for t, d in CHECKLIST)
    faq = "\n".join(
        f"""          <details class="faq-item">
            <summary><h3>{e(q)}</h3><svg class="icon" aria-hidden="true"><use href="#i-plus" /></svg></summary>
            <p>{e(a)}</p>
          </details>""" for q, a in g["faq"])
    others = [x for x in GUIDES if x["slug"] != g["slug"]]
    related = "\n".join(
        [f"""          <a class="related-card" href="/guides/{x["slug"]}/"><span class="related-pillar">Guide</span><span class="related-name">{e(x["software"])} and UAE e-invoicing</span><span class="related-desc">{e(x["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>""" for x in others]
        + [f"""          <a class="related-card" href="/services/e-invoicing-uae/"><span class="related-pillar">Service</span><span class="related-name">{e(BY_SLUG["e-invoicing-uae"]["name"])}</span><span class="related-desc">{e(BY_SLUG["e-invoicing-uae"]["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""])

    body = f"""{head(g["title"], g["description"], canonical, ld)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{HEADER}

  <main id="main">
    <section class="page-hero on-dark" aria-labelledby="page-title">
      <div class="container">
        {breadcrumbs_html(trail)}
        <p class="eyebrow" data-reveal>Guide · UAE e-invoicing</p>
        <h1 id="page-title" data-reveal="mask">{e(g["h1"])}</h1>
        <p class="lead" data-reveal>{e(g["lead"])}</p>
        <div class="hero-ctas" data-reveal-stagger>
          <a class="btn btn-gold" href="{CHECKER["path"]}" data-magnetic>Free readiness check <span aria-hidden="true">&rarr;</span></a>
          <a class="btn btn-ghost-light" href="/#contact" data-magnetic>Book a consultation</a>
        </div>
        <p class="guide-meta" data-reveal>Facts checked {e(CHECKED)} against the Ministry of Finance list and official specifications.</p>
      </div>
    </section>

    <section class="section" aria-labelledby="answer-title">
      <div class="container">
        <div class="answer-box" data-reveal>
          <h2 id="answer-title">The short answer</h2>
          <p>{e(g["answer"])}</p>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="status-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Where {e(g["software"])} stands</p>
          <h2 id="status-title" data-reveal="mask">The facts, with sources.</h2>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{fact_rows(g["status"])}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Step by step</p>
          <h2 id="steps-title" data-reveal="mask">{e(g["steps_title"])}</h2>
        </div>
        <ol class="guide-steps" data-reveal-stagger>
{steps}
        </ol>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="questions-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Before you go live</p>
          <h2 id="questions-title" data-reveal="mask">{e(g["questions_title"])}</h2>
        </div>
        <ul class="incl-grid" data-reveal-stagger>
{questions}
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="data-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Data checklist</p>
          <h2 id="data-title" data-reveal="mask">What every e-invoice must carry.</h2>
          <p class="lead" data-reveal>From the UAE e-invoicing specification, PINT AE. These apply whatever software you use. <a class="u-link" href="{e(PINT_AE_RULES[1])}" target="_blank" rel="noopener">{e(PINT_AE_RULES[0])}<span class="sr-only"> (opens in a new tab)</span></a></p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{checklist}
        </dl>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="dates-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Deadlines</p>
          <h2 id="dates-title" data-reveal="mask">When you need to be ready.</h2>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{fact_rows(DEADLINES)}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq}
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="related-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Related</p>
          <h2 id="related-title" data-reveal="mask">Keep reading.</h2>
        </div>
        <div class="related-grid" data-reveal-stagger>
{related}
        </div>
      </div>
    </section>

{cta_band(g["software"] + " e-invoicing")}
  </main>

{footer()}
</body>
</html>
"""
    out = ROOT / "guides" / g["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def guides_hub():
    canonical = guide_url()
    trail = [("Home", f"{SITE}/"), ("Guides", canonical)]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(), breadcrumbs_ld(trail),
        {"@type": "ItemList", "name": "UAE e-invoicing software guides", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": guide_url(g["slug"]), "name": g["h1"]} for i, g in enumerate(GUIDES)]},
    ]}
    cards = "\n".join(
        f"""          <a class="related-card" href="/guides/{g["slug"]}/"><span class="related-pillar">Guide</span><span class="related-name">{e(g["software"])} and UAE e-invoicing</span><span class="related-desc">{e(g["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""
        for g in GUIDES)
    body = f"""{head("E-Invoicing Guides: QuickBooks, Zoho, Tally, Odoo | Accuminds",
                 "Practical UAE e-invoicing guides for QuickBooks, Zoho Books, TallyPrime and Odoo users: Accredited Service Providers, setup steps, data checklists and deadlines.",
                 canonical, ld)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{HEADER}

  <main id="main">
    <section class="page-hero on-dark" aria-labelledby="page-title">
      <div class="container">
        {breadcrumbs_html(trail)}
        <p class="eyebrow" data-reveal>Guides</p>
        <h1 id="page-title" data-reveal="mask">UAE e-invoicing, by accounting software.</h1>
        <p class="lead" data-reveal>How to meet the e-invoicing mandate with the software you already use: whether it is an Accredited Service Provider, the setup steps, and the data to fix first.</p>
        <div class="hero-ctas" data-reveal-stagger>
          <a class="btn btn-gold" href="{CHECKER["path"]}" data-magnetic>Free readiness check <span aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </section>

    <section class="section" aria-label="All guides">
      <div class="container">
        <div class="related-grid related-grid--all" data-reveal-stagger>
{cards}
        </div>
      </div>
    </section>

{cta_band("e-invoicing")}
  </main>

{footer()}
</body>
</html>
"""
    out = ROOT / "guides" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def nowrap_hyphenated(text):
    """Keeps hyphenated words such as "end-of-service" on one line in headings (escaped text in, HTML out)."""
    return re.sub(r"\b(\w+(?:-\w+)+)\b", r'<span class="nowrap">\1</span>', text)


def resource_shell(title, description, canonical, ld, eyebrow, h1, lead, ctas, inner, topic):
    trail = [("Home", f"{SITE}/"), (h1, canonical)]
    return f"""{head(title, description, canonical, ld)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{HEADER}

  <main id="main">
    <section class="page-hero on-dark" aria-labelledby="page-title">
      <div class="container">
        {breadcrumbs_html(trail)}
        <p class="eyebrow" data-reveal>{e(eyebrow)}</p>
        <h1 id="page-title" data-reveal="mask">{nowrap_hyphenated(e(h1))}</h1>
        <p class="lead" data-reveal>{e(lead)}</p>
        <div class="hero-ctas" data-reveal-stagger>
{ctas}
        </div>
      </div>
    </section>
{inner}
{cta_band(topic)}
  </main>

{footer()}
</body>
</html>
"""


def faq_html(items):
    return "\n".join(
        f"""          <details class="faq-item">
            <summary><h3>{e(q)}</h3><svg class="icon" aria-hidden="true"><use href="#i-plus" /></svg></summary>
            <p>{e(a)}</p>
          </details>""" for q, a in items)


def mis_template_page():
    canonical = f"{SITE}{MIS_TEMPLATE['path']}"
    sheets = [
        ("Settings", "Company name, reporting month and the minimum cash buffer: the pack follows the month you choose."),
        ("Actuals and Budget", "Monthly figures by line: revenue, cost of sales, operating expenses, and month-end cash, receivables, inventory and payables."),
        ("P&L vs Budget", "The month and year to date against budget, with variances coloured by whether they help or hurt."),
        ("KPIs", "Gross and EBITDA margin, cost ratios, receivable, inventory and payable days and the cash conversion cycle, with charts."),
        ("Cash outlook", "Three months of expected receipts and payments, closing cash, and a warning when cash falls below your buffer."),
        ("Commentary", "Prompts for what changed, why, and the decisions needed: the part that turns numbers into a management pack."),
    ]
    faq = [
        ("What is a monthly MIS report?", "A management information pack: profit and loss against budget, cash and working capital, key performance indicators and short commentary, prepared every month so owners can make decisions."),
        ("What should a monthly MIS report format include?", "At least the month and year to date against budget, the main KPIs (margins, cost ratios, receivable, inventory and payable days), a short cash outlook and commentary on what changed and what needs a decision. This template has a sheet for each."),
        ("Is the template free?", "Yes. Download it, replace the fictitious example figures with your own and use it as you like."),
        ("Does it work with my accounting software?", "Yes. Export monthly totals from QuickBooks, Zoho Books, Tally, Odoo or any other system and enter them in the Actuals sheet. We can also build packs that refresh from your ledger automatically."),
        ("Which version of Excel do I need?", "Any recent version of Microsoft Excel. It also opens in Google Sheets and LibreOffice, though charts may look slightly different."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "CreativeWork", "@id": f"{canonical}#template", "name": "Monthly MIS report template (Excel)",
         "description": MIS_TEMPLATE["card"], "url": canonical, "encodingFormat": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
         "isAccessibleForFree": True, "inLanguage": "en", "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
         "associatedMedia": {"@type": "MediaObject", "contentUrl": f"{SITE}{MIS_TEMPLATE['file']}",
                             "encodingFormat": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("Monthly MIS report template", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    cards = "\n".join(f'          <li class="incl"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in sheets)
    ctas = f"""          <a class="btn btn-gold" href="{MIS_TEMPLATE["file"]}" download data-magnetic>Download free (Excel) <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="/services/mis-reporting-dubai/" data-magnetic>MIS &amp; reporting service</a>"""
    inner = f"""
    <section class="section" aria-labelledby="inside-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>What is inside</p>
          <h2 id="inside-title" data-reveal="mask">Everything in one monthly pack.</h2>
          <p class="lead" data-reveal>Blue cells are inputs and yellow cells are where you start. Everything else is a formula, so the pack updates as you enter your numbers. All example figures are fictitious.</p>
        </div>
        <ul class="incl-grid" data-reveal-stagger>
{cards}
        </ul>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="use-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>How to use it</p>
          <h2 id="use-title" data-reveal="mask">Four steps each month.</h2>
        </div>
        <ol class="guide-steps" data-reveal-stagger>
          <li><h3>Close the month</h3><p>Post all invoices, bills and bank entries, and reconcile the bank, so the numbers are complete.</p></li>
          <li><h3>Enter the totals</h3><p>Copy monthly totals by line from your accounting system into the Actuals sheet, and set the reporting month.</p></li>
          <li><h3>Read the variances</h3><p>Start with the biggest variances against budget and the change in receivable and inventory days.</p></li>
          <li><h3>Write the commentary</h3><p>Two or three lines on what changed and why, and the decisions needed. Share the pack within a week of month-end.</p></li>
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
"""
    body = resource_shell(
        "Monthly MIS Report Format in Excel: Free Download | Accuminds",
        "Free download: a monthly MIS report format in Excel for SMEs, with P&L against budget, KPIs, working-capital days, a cash outlook and commentary prompts.",
        canonical, ld, "Free Excel download", "Monthly MIS report format in Excel",
        "A ready-to-use Excel management pack for SMEs: P&L against budget, KPIs, working-capital days, a three-month cash outlook and commentary prompts.",
        ctas, inner, "your monthly reporting")
    out = ROOT / "mis-report-template" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def ct_check_page():
    canonical = f"{SITE}{CT_CHECK['path']}"
    sources = [
        ("FTA: Corporate Tax registration", "https://tax.gov.ae/en/services/corporate.tax.registration.aspx"),
        ("FTA: natural persons", "https://tax.gov.ae/en/taxes/corporate.tax/corporate.tax.topics/basis.of.taxation.natural.person.aspx"),
        ("FTA: Small Business Relief", "https://tax.gov.ae/en/taxes/corporate.tax/corporate.tax.topics/small.business.relief.23.aspx"),
        ("FTA: exempt persons", "https://tax.gov.ae/en/taxes/corporate.tax/corporate.tax.topics/exempt.person.aspx"),
        ("Ministry of Finance: Corporate Tax", "https://mof.gov.ae/en/public-finance/tax/corporate-tax/"),
        ("Ministry of Finance: Small Business Relief extended to 2029",
         "https://mof.gov.ae/en/news/ministry-of-finance-announces-extension-of-small-business-relief-for-corporate-tax-purposes-until-31-december-2029/"),
    ]
    rules = [
        ("Companies", "UAE companies, including free zone companies, must register for Corporate Tax and file a return, whatever their revenue or profit."),
        ("Individuals", "An individual doing business must register when business turnover in a calendar year exceeds AED 1 million. Salary, personal investment income and personal real estate investment income are not counted."),
        ("Small Business Relief", "Resident businesses with revenue of AED 3 million or less in the current and every previous tax period can elect it, for tax periods ending on or before 31 December 2029. Qualifying Free Zone Persons and members of multinational groups with revenue above AED 3.15 billion cannot."),
        ("Rates", "0% on taxable income up to AED 375,000 and 9% above that."),
        ("Deadlines and penalty", "Returns are due within 9 months of the end of each tax period. Late registration carries an AED 10,000 penalty, waived if the first return is filed within 7 months of the end of the first tax period."),
    ]
    faq = [
        ("Do I need to file a Corporate Tax return if I made no profit?", "Yes, if you are required to register. Companies file a return for every tax period even when no tax is due."),
        ("Do free zone companies pay Corporate Tax?", "Free zone companies must register and file. A Qualifying Free Zone Person pays 0% on qualifying income if it meets the conditions, and must keep audited financial statements."),
        ("Does a freelancer need to register for Corporate Tax?", "Only once business turnover in a calendar year exceeds AED 1 million. Below that, keep records and check again each year."),
        ("What is Small Business Relief?", "An election for resident businesses with revenue of AED 3 million or less to be treated as having no taxable income for the period. It is claimed in the return, so you still register and file."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "WebApplication", "@id": f"{canonical}#app", "name": "UAE Corporate Tax filing check", "url": canonical,
         "description": CT_CHECK["card"], "applicationCategory": "BusinessApplication", "operatingSystem": "Any (runs in a web browser)",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"}, "provider": {"@id": ORG_ID}},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("Corporate Tax filing check", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    rule_rows = "\n".join(f'          <div class="fact-row"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for t, d in rules)
    src_links = " · ".join(
        f'<a class="u-link" href="{e(u)}" target="_blank" rel="noopener">{e(n)}<span class="sr-only"> (opens in a new tab)</span></a>' for n, u in sources)
    ctas = """          <a class="btn btn-gold" href="#check" data-magnetic>Start the check <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="/services/corporate-tax-uae/" data-magnetic>Corporate Tax services</a>"""
    inner = f"""
    <section class="section" id="check" aria-labelledby="check-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The check</p>
          <h2 id="check-title" data-reveal="mask">Five questions at most.</h2>
          <p class="lead" data-reveal>Your answers stay in your browser. Nothing is sent or stored.</p>
        </div>
        <div class="ct-card" id="ct-check" aria-live="polite">
          <noscript><p>This check needs JavaScript. The rules it applies are summarised below.</p></noscript>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="rules-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The rules it applies</p>
          <h2 id="rules-title" data-reveal="mask">In brief, with sources.</h2>
          <p class="lead" data-reveal>Checked {e(CT_CHECKED)} against FTA and Ministry of Finance pages: {src_links}</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{rule_rows}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
    <script type="module" src="/assets/js/ct-check.js"></script>
"""
    body = resource_shell(
        "Do I Need to File UAE Corporate Tax? Free Check | Accuminds",
        "A free check for UAE companies, free zone companies and individuals: must you register and file for Corporate Tax, and can you claim Small Business Relief?",
        canonical, ld, "Free tool", "Do I need to register and file for Corporate Tax?",
        "Answer up to five questions to see whether you must register and file for UAE Corporate Tax, and whether Small Business Relief may apply.",
        ctas, inner, "Corporate Tax")
    out = ROOT / "corporate-tax-check" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def supplier_check_page():
    canonical = f"{SITE}{SV_CHECK['path']}"
    rules = [
        ("Who and when", "VAT-registered businesses, for supplies received from 1 October 2026, before deducting input tax (Art. 2, 7). If a supply is connected to tax evasion and the business knew or should have known, the FTA may deny the input tax (Article 54(bis), VAT Law)."),
        ("Below AED 10,000", "A supply under AED 10,000 excluding VAT can be left out of the checks, unless total supplies from that supplier exceed AED 100,000 in the previous 12 months or are expected to in the next 12 (Art. 6)."),
        ("Supplier checks", "Companies: incorporation verified and the representative's ID. Individuals: valid ID and a meeting, in person or virtually, before the supply. All: actual place of business and risk indicators (Art. 3.1 to 3.3)."),
        ("Above AED 375,000", "A written confirmation from an authorised UAE bank that the supplier has a bank account, and a review of clients' recommendations, public reviews and media (Art. 3.4)."),
        ("Supply checks", "Genuine commercial reason, electronic payment (cash only with a documented reason), explanations for third-party or foreign-account payments, market price, licence-activity match, origin and ownership of goods, and intermediary rationale (Art. 4)."),
        ("Procedures", "Verify a new supplier, and again after 12 months; check every supply in scope; document the steps and keep the records; keep a written policy naming who implements, reviews and supervises (Art. 5)."),
    ]
    faq = [
        ("Does every supplier need to be verified from 1 October 2026?", "Every supplier whose supplies are in scope. Supplies under AED 10,000 excluding VAT can be left out, unless total supplies from that supplier exceed AED 100,000 in the previous or next 12 months."),
        ("Is a letter from the supplier confirming its bank account enough?", "No. Above AED 375,000, the Decision asks for a written confirmation issued by an authorised bank in the UAE, without reservations or conditions. It does not have to be addressed to you."),
        ("How often must suppliers be re-verified?", "When you first deal with them, and again on recurring dealings if they have not been verified in the previous 12 months."),
        ("What happens if I do not verify?", "If a supply turns out to be connected to tax evasion and you knew or should have known, the FTA may deny your input tax deduction under Article 54(bis) of the VAT Law."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "WebApplication", "@id": f"{canonical}#app", "name": "Supplier verification check (FTA Decision 13 of 2026)", "url": canonical,
         "description": SV_CHECK["card"], "applicationCategory": "BusinessApplication", "operatingSystem": "Any (runs in a web browser)",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"}, "provider": {"@id": ORG_ID}},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("Supplier verification check", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    rule_rows = "\n".join(f'          <div class="fact-row"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for t, d in rules)
    ctas = f"""          <a class="btn btn-gold" href="#check" data-magnetic>Check a supplier <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="{SV_CHECK["pdf"]}" download data-magnetic>Download the checklist (PDF)</a>"""
    inner = f"""
    <section class="section" id="check" aria-labelledby="check-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The check</p>
          <h2 id="check-title" data-reveal="mask">Which checks apply to this supplier?</h2>
          <p class="lead" data-reveal>Amounts exclude VAT. Your answers stay in your browser; nothing is sent or stored.</p>
        </div>
        <div class="sv-grid">
          <form class="ct-card sv-form" id="sv-form" novalidate>
            <label class="sv-field"><span>Supplier name (for your record)</span><input name="name" type="text" autocomplete="off" placeholder="e.g. Example Supplies LLC" /></label>
            <fieldset class="sv-field"><legend>Supplier type</legend>
              <label class="sv-pill"><input type="radio" name="type" value="company" checked /> Company</label>
              <label class="sv-pill"><input type="radio" name="type" value="person" /> Individual</label>
            </fieldset>
            <label class="sv-field"><span>This invoice (AED, excl. VAT)</span><input name="invoice" inputmode="decimal" placeholder="e.g. 8,500" /></label>
            <label class="sv-field"><span>Total from this supplier, previous 12 months (AED)</span><input name="prev" inputmode="decimal" placeholder="e.g. 60,000" /></label>
            <label class="sv-field"><span>Expected total, next 12 months (AED)</span><input name="next" inputmode="decimal" placeholder="e.g. 90,000" /></label>
            <fieldset class="sv-field"><legend>Verified this supplier in the last 12 months?</legend>
              <label class="sv-pill"><input type="radio" name="verified" value="no" checked /> No</label>
              <label class="sv-pill"><input type="radio" name="verified" value="yes" /> Yes</label>
            </fieldset>
            <fieldset class="sv-field"><legend>This supply involves</legend>
              <label class="sv-check"><input type="checkbox" name="flag" value="goods" /> Goods</label>
              <label class="sv-check"><input type="checkbox" name="flag" value="imported" /> Imported goods</label>
              <label class="sv-check"><input type="checkbox" name="flag" value="cash" /> Cash payment</label>
              <label class="sv-check"><input type="checkbox" name="flag" value="thirdparty" /> Payment via a third party, or to an account outside the supplier's country</label>
              <label class="sv-check"><input type="checkbox" name="flag" value="intermediary" /> Supplier is an agent or intermediary</label>
            </fieldset>
            <fieldset class="sv-field"><legend>Risk indicators (Art. 3.3)</legend>
              <label class="sv-check"><input type="checkbox" name="risk" value="address changed more than twice in 12 months" /> Address changed more than twice in 12 months</label>
              <label class="sv-check"><input type="checkbox" name="risk" value="key employees changed more than twice in 12 months" /> Key employees changed more than twice in 12 months</label>
              <label class="sv-check"><input type="checkbox" name="risk" value="transactions out of proportion to the supplier's size or history" /> Transactions out of proportion to the supplier's size or history</label>
            </fieldset>
          </form>
          <div class="ct-card sv-out" id="sv-result" aria-live="polite">
            <noscript><p>This check needs JavaScript. Download the PDF checklist instead.</p></noscript>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="rules-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The rule</p>
          <h2 id="rules-title" data-reveal="mask">FTA Decision No. 13 of 2026, in brief.</h2>
          <p class="lead" data-reveal>Issued 22 July 2026, effective 1 October 2026. Source: <a class="u-link" href="{e(FTA_DEC13[1])}" target="_blank" rel="noopener">{e(FTA_DEC13[0])}<span class="sr-only"> (opens in a new tab)</span></a></p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{rule_rows}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
    <script type="module" src="/assets/js/supplier-check.js"></script>
"""
    body = resource_shell(
        "Supplier Verification for Input VAT: Free Check | Accuminds",
        "Free check: which supplier and transaction checks FTA Decision No. 13 of 2026 requires before you claim input VAT, with a printable checklist.",
        canonical, ld, "Free tool · VAT", "Supplier verification check",
        "From 1 October 2026 you must verify suppliers and supplies before claiming input VAT. Enter a supplier's amounts to see exactly which checks apply, then print the checklist.",
        ctas, inner, "supplier checks")
    out = ROOT / "supplier-verification-check" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def trn_page():
    canonical = f"{SITE}{TRN_CHECK['path']}"
    rules = [
        ("What a TRN is", "A unique number the FTA assigns to each person registered for tax (Article 1).", VAT_EXEC_REG),
        ("Format", "15 digits. On UAE e-invoices a VAT TRN must start with 1 and end with 03, with no spaces, dashes or prefix (rule IBR-132-AE).", PINT_AE_RULES),
        ("Full tax invoice", "Shows the supplier's name, address and TRN, and the recipient's name, address and TRN if the recipient is VAT registered (Article 59(1)).", VAT_EXEC_REG),
        ("Simplified tax invoice", "Shows the supplier's TRN only. Allowed when the recipient is not VAT registered, or is registered and the supply is AED 10,000 or less, and reverse charge does not apply (Article 59(2) and (5)).", VAT_EXEC_REG),
        ("Where to verify", "The TRN/TIN verification on the FTA website: a 15-digit TRN or a 10-digit TIN, plus a security code. No login is needed.", FTA_HOME),
    ]
    faq = [
        ("How do I verify a TRN number in the UAE?", "On the FTA website (tax.gov.ae), open TRN/TIN verification at the top of the page, choose TRN, enter the 15 digits and the security code, and submit. Check that the result matches the business named on the invoice."),
        ("How many digits is a UAE TRN?", "15. On UAE e-invoices a VAT TRN must start with 1 and end with 03 (PINT AE rule IBR-132-AE)."),
        ("Can I check a TRN without logging in to EmaraTax?", "Yes. The TRN/TIN verification on the FTA website is open to anyone and needs only the number and the security code."),
        ("What is the difference between a TRN and a TIN?", "A TRN has 15 digits; a TIN has 10. The FTA's verification accepts either: choose TRN or TIN before you enter the number."),
        ("Must my customer's TRN be on my tax invoice?", "Yes, if the customer is VAT registered and you issue a full tax invoice (Article 59(1)). A simplified tax invoice shows only your own TRN."),
        ("What if the TRN is not found or the name does not match?", "Ask the supplier for its VAT registration certificate and a corrected invoice before you claim the input VAT. A tax invoice must show the supplier's TRN (Article 59(1))."),
        ("Does this tool check the FTA register?", "No. It checks the format only, in your browser, and nothing is sent. Only the FTA's own verification confirms that a TRN is registered."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "WebApplication", "@id": f"{canonical}#app", "name": "UAE TRN format check", "url": canonical,
         "description": TRN_CHECK["card"], "applicationCategory": "BusinessApplication", "operatingSystem": "Any (runs in a web browser)",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"}, "provider": {"@id": ORG_ID}},
        {"@type": "HowTo", "@id": f"{canonical}#howto", "name": "How to verify a TRN on the FTA website",
         "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t} for i, (n, t) in enumerate([
             ("Open the FTA website", "Go to tax.gov.ae and open TRN/TIN verification at the top of the page."),
             ("Enter the number", "Choose TRN and enter the 15 digits, or choose TIN for a 10-digit number."),
             ("Enter the security code", "Type the code shown in the image and submit."),
             ("Compare the result", "Check that the result matches the business named on the invoice."),
         ], 1)]},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("TRN verification", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    ctas = f"""          <a class="btn btn-gold" href="#check" data-magnetic>Check a TRN <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="{SV_CHECK["path"]}" data-magnetic>Supplier verification check</a>"""
    inner = f"""
    <section class="section" id="check" aria-labelledby="check-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Format check</p>
          <h2 id="check-title" data-reveal="mask">Is this TRN in the right format?</h2>
          <p class="lead" data-reveal>Catches typos and wrong numbers before you look the TRN up. It runs in your browser; nothing is sent or stored.</p>
        </div>
        <div class="sv-grid">
          <form class="ct-card sv-form" id="trn-form" novalidate>
            <label class="sv-field"><span>TRN or TIN</span><input name="trn" inputmode="numeric" autocomplete="off" spellcheck="false" placeholder="15 digits, e.g. 1XXXXXXXXXXXX03" /></label>
            <p class="ct-note">Spaces, dashes and a "TRN" label are ignored.</p>
          </form>
          <div class="ct-card sv-out" id="trn-result" aria-live="polite">
            <noscript><p>The format check needs JavaScript. A UAE VAT TRN has 15 digits, starting with 1 and ending with 03.</p></noscript>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>On the FTA website</p>
          <h2 id="steps-title" data-reveal="mask">Confirm the TRN is registered.</h2>
          <p class="lead" data-reveal>Only the FTA's own verification confirms that a TRN is registered. It is open to anyone, with no EmaraTax login. <a class="u-link" href="{e(FTA_HOME[1])}" target="_blank" rel="noopener">Open tax.gov.ae<span class="sr-only"> (opens in a new tab)</span></a></p>
        </div>
        <ol class="guide-steps" data-reveal-stagger>
          <li><h3>Open TRN/TIN verification</h3><p>On tax.gov.ae, it is at the top of the page.</p></li>
          <li><h3>Enter the number</h3><p>Choose TRN and enter the 15 digits, or choose TIN for a 10-digit number.</p></li>
          <li><h3>Enter the security code</h3><p>Type the code shown in the image and submit.</p></li>
          <li><h3>Compare the result</h3><p>It should match the business named on the invoice. If it is not found or the name differs, ask the supplier for its VAT registration certificate before you claim the input VAT.</p></li>
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="rules-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The rules</p>
          <h2 id="rules-title" data-reveal="mask">When a TRN must be on an invoice.</h2>
          <p class="lead" data-reveal>Cabinet Resolution No. 52 of 2017 (the VAT Executive Regulation, as amended) and the PINT AE specification. Checked {e(TRN_CHECKED)}.</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{fact_rows(rules)}
        </dl>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="supplier-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Before you claim input VAT</p>
          <h2 id="supplier-title" data-reveal="mask">A valid TRN is only the first check.</h2>
          <p class="lead" data-reveal>From 1 October 2026, FTA Decision No. 13 of 2026 also asks you to verify the supplier and the supply before you claim input VAT. See which checks apply in the <a class="u-link" href="{SV_CHECK["path"]}">Supplier Verification Check</a>.</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
    <script type="module" src="/assets/js/trn-check.js"></script>
"""
    body = resource_shell(
        "TRN Verification UAE: Check a TRN Number | Accuminds",
        "How to verify a UAE TRN on the FTA website, with a free format check: 15 digits, starting with 1 and ending with 03. Plus when a TRN must be on a tax invoice.",
        canonical, ld, "Free tool · VAT", "TRN verification in the UAE",
        "Check that a TRN has the right format, then confirm it on the FTA website in four steps. Plus when a TRN must appear on a tax invoice.",
        ctas, inner, "VAT and supplier checks")
    out = ROOT / TRN_CHECK["path"].strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def vat_registration_page():
    canonical = f"{SITE}{VAT_REG['path']}"
    rules = [
        ("Must register", "A UAE business whose taxable supplies and imports exceeded AED 375,000 over the previous 12 months, or are expected to exceed it in the next 30 days.", FTA_VAT_TOPIC),
        ("May register", "Below that, a business may register voluntarily once its taxable supplies and imports, or its taxable expenses, exceed AED 187,500 over the previous 12 months or are expected to in the next 30 days.", FTA_VAT_TOPIC),
        ("Non-resident businesses", "No threshold: registration is mandatory for taxable supplies in the UAE unless someone else in the UAE is responsible for the VAT on them.", FTA_VAT_REG),
        ("Deadline", "Apply within 30 days of becoming required to register. The rules apply to anyone doing business in the UAE, even without a trade licence.", FTA_VAT_REG),
        ("Late registration penalty", "AED 10,000 for not applying within the time the law allows.", FTA_PENALTIES),
        ("Fee and timing", "Registration is free. The application takes about 45 minutes, and the FTA aims to decide within 20 business days of receiving a complete application.", FTA_VAT_REG),
        ("Branches and sole establishments", "One TRN covers all branches of a company. All sole establishments of the same owner share one TRN, and their turnover is added together for the threshold.", FTA_VAT_REG),
    ]
    docs = [
        ("Company documents", "Certificate of incorporation, memorandum of association or partnership agreement, and the trade licence with any branch licences."),
        ("Owners and signatories", "Emirates ID and passport copies of the owners and authorised signatories, and a power of attorney if the manager is not named in the memorandum."),
        ("Turnover declaration", "A signed and stamped letter stating taxable supplies and monthly sales since the business started. The FTA publishes a template."),
        ("Evidence", "Invoices, purchase orders, contracts or leases that support the turnover. Registering on expenses needs at least five VAT invoices; expected revenue needs signed purchase orders or contracts."),
        ("Optional and if applicable", "A bank letter in the company's name, and customs details if you import or export."),
    ]
    steps = [
        ("Create an EmaraTax account", "Sign up on the FTA website and activate the account."),
        ("Add a taxable person", "From the dashboard, create a new taxable person profile for the business and open it."),
        ("Register for VAT", "Click Register under Value Added Tax, complete the form and upload the documents as PDFs (up to 15 MB each)."),
        ("Get your TRN", "Once approved, the VAT registration certificate with your TRN appears in your EmaraTax dashboard."),
    ]
    faq = [
        ("What is the VAT registration threshold in the UAE?", "AED 375,000 of taxable supplies and imports for mandatory registration, and AED 187,500 of taxable supplies and imports or taxable expenses for voluntary registration."),
        ("How long does VAT registration take?", "About 45 minutes to submit online. The FTA aims to decide within 20 business days of receiving a complete application."),
        ("Is there a fee to register for VAT?", "No. VAT registration through EmaraTax is free."),
        ("What is the penalty for late VAT registration?", "AED 10,000 if you do not apply within 30 days of becoming required to register."),
        ("Can I register for VAT on expenses alone?", "Yes, voluntarily, if taxable expenses exceed AED 187,500. The FTA asks for at least five VAT invoices as evidence."),
        ("Does each branch need its own TRN?", "No. All branches register under the company's single TRN and file one VAT return."),
        ("Do free zone companies need to register for VAT?", "The same thresholds apply. For a business in a designated zone trading goods, it depends on its activities and supplies, and the FTA may ask for a business flow showing how goods move."),
        ("What happens after I register?", "You receive a TRN, charge VAT on taxable supplies, issue tax invoices and file VAT returns for each tax period."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "WebApplication", "@id": f"{canonical}#app", "name": "UAE VAT registration check", "url": canonical,
         "description": VAT_REG["card"], "applicationCategory": "BusinessApplication", "operatingSystem": "Any (runs in a web browser)",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"}, "provider": {"@id": ORG_ID}},
        {"@type": "HowTo", "@id": f"{canonical}#howto", "name": "How to register for VAT in the UAE",
         "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t} for i, (n, t) in enumerate(steps, 1)]},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("VAT registration", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    doc_cards = "\n".join(f'          <li class="incl"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in docs)
    step_items = "\n".join(f"          <li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in steps)
    ctas = """          <a class="btn btn-gold" href="#check" data-magnetic>Check if you must register <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="/services/vat-services-uae/" data-magnetic>VAT registration service</a>"""
    inner = f"""
    <section class="section" id="check" aria-labelledby="check-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The check</p>
          <h2 id="check-title" data-reveal="mask">Do you have to register?</h2>
          <p class="lead" data-reveal>Amounts in AED, excluding VAT. Your answers stay in your browser; nothing is sent or stored.</p>
        </div>
        <div class="sv-grid">
          <form class="ct-card sv-form" id="vr-form" novalidate>
            <fieldset class="sv-field"><legend>Where is the business established?</legend>
              <label class="sv-pill"><input type="radio" name="where" value="uae" checked /> In the UAE</label>
              <label class="sv-pill"><input type="radio" name="where" value="foreign" /> Outside the UAE</label>
            </fieldset>
            <div id="vr-amounts">
              <label class="sv-field"><span>Taxable supplies and imports, last 12 months</span><input name="past" inputmode="decimal" placeholder="e.g. 320,000" /></label>
              <label class="sv-field"><span>Expected taxable supplies and imports, next 30 days</span><input name="next" inputmode="decimal" placeholder="e.g. 40,000" /></label>
              <label class="sv-field"><span>Taxable expenses, last 12 months (optional)</span><input name="exp" inputmode="decimal" placeholder="e.g. 150,000" /></label>
              <label class="sv-field"><span>Expected taxable expenses, next 30 days (optional)</span><input name="expnext" inputmode="decimal" placeholder="e.g. 10,000" /></label>
              <p class="ct-note">Taxable supplies are sales charged at 5% or 0%; exempt sales do not count.</p>
            </div>
          </form>
          <div class="ct-card sv-out" id="vr-result" aria-live="polite">
            <noscript><p>This check needs JavaScript. The thresholds it applies are set out below.</p></noscript>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="rules-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The rules</p>
          <h2 id="rules-title" data-reveal="mask">Thresholds, deadline and penalty.</h2>
          <p class="lead" data-reveal>From the FTA's VAT registration pages and its published table of administrative penalties. Checked {e(VAT_REG_CHECKED)}.</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{fact_rows(rules)}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="docs-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Documents</p>
          <h2 id="docs-title" data-reveal="mask">What to have ready.</h2>
          <p class="lead" data-reveal>The FTA's list for a company; it varies by legal form. Upload each as a PDF.</p>
        </div>
        <ul class="incl-grid" data-reveal-stagger>
{doc_cards}
        </ul>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>On EmaraTax</p>
          <h2 id="steps-title" data-reveal="mask">Four steps to a TRN.</h2>
          <p class="lead" data-reveal>Once you have it, customers can confirm it with a <a class="u-link" href="{TRN_CHECK["path"]}">TRN verification</a>.</p>
        </div>
        <ol class="guide-steps" data-reveal-stagger>
{step_items}
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
    <script type="module" src="/assets/js/vat-registration.js"></script>
"""
    body = resource_shell(
        "VAT Registration in UAE: Threshold, Documents & Steps | Accuminds",
        "Do you have to register for UAE VAT? Free check against the AED 375,000 and AED 187,500 thresholds, plus the documents, EmaraTax steps, deadline and penalty.",
        canonical, ld, "Free tool · VAT", "VAT registration in the UAE",
        "Check whether you must register for VAT, or can choose to, then see the documents the FTA asks for and the four steps on EmaraTax.",
        ctas, inner, "VAT registration")
    out = ROOT / VAT_REG["path"].strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def ct_registration_page():
    canonical = f"{SITE}{CT_REG['path']}"
    rules = [
        ("UAE companies, from 1 March 2024", "Including free zone companies: within 3 months of incorporation, establishment or recognition (Art. 3.3).", FTA_DEC3),
        ("UAE companies, before 1 March 2024", "By a deadline in 2024 set by the month the licence was issued, whatever the year; all of these have passed. With more than one licence, the earliest counts (Art. 3.1 and 3.2).", FTA_DEC3),
        ("Foreign companies managed in the UAE", "Within 3 months of the end of the company's financial year (Art. 3.3).", FTA_DEC3),
        ("Individuals", "Once business turnover in a calendar year exceeds AED 1 million, by 31 March of the following year. Salary, personal investment income and real estate investment income do not count (Art. 5).", FTA_DEC3),
        ("Non-resident companies", "With a permanent establishment in the UAE: 6 months from when it began, or 9 months if it existed before 1 March 2024. With a nexus: 3 months (Art. 4).", FTA_DEC3),
        ("Penalty and waiver", "AED 10,000 for late registration, waived if the first tax return is filed within 7 months of the end of the first tax period. A penalty already paid is credited back.", FTA_CT_REG),
        ("Fee and timing", "Registration is free. The application takes about 25 minutes, and the FTA aims to decide within 20 business days of receiving a complete application.", FTA_CT_REG),
        ("Branches", "UAE branches of a UAE company are part of it and do not register or file separately.", FTA_CT_REG),
    ]
    docs = [
        ("Company documents", "Certificate of incorporation, memorandum of association or partnership agreement, and the commercial registration or another document from the licensing authority."),
        ("Trade licence", "A valid trade licence, with branch licences if there are any."),
        ("Owners and signatories", "Emirates ID and passport of each owner with more than 25%, and of the authorised signatories, with proof of the signatory's authority."),
    ]
    steps = [
        ("Sign in to EmaraTax", "Create and activate an EmaraTax account on the FTA website, or use the one you have for VAT."),
        ("Open the taxable person", "Create a new taxable person profile, or open the existing one with View."),
        ("Register for Corporate Tax", "In the Action menu under Corporate Tax, click Register, complete the application and upload the documents as PDFs (up to 15 MB each)."),
        ("Get your registration number", "Once approved, the FTA issues the Corporate Tax registration number. Then note your first tax period and return deadline."),
    ]
    faq = [
        ("When must a new company register for Corporate Tax?", "Within 3 months of incorporation, for UAE companies incorporated on or after 1 March 2024, including free zone companies (FTA Decision No. 3 of 2024)."),
        ("My company was set up before March 2024 and has not registered. What now?", "The 2024 deadline has passed, so register now. The AED 10,000 penalty is waived if the first tax return is filed within 7 months of the end of the first tax period."),
        ("Is there a fee to register for Corporate Tax?", "No. Registration through EmaraTax is free."),
        ("Do I need to register if my profit is below AED 375,000?", "Yes. Profit up to AED 375,000 is taxed at 0%, but companies still register and file a return."),
        ("Does a freelancer need to register for Corporate Tax?", "Only once business turnover in a calendar year exceeds AED 1 million, and then by 31 March of the following year."),
        ("Do branches need a separate Corporate Tax registration?", "No. UAE branches of a UAE company are covered by the company's registration and return."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "WebApplication", "@id": f"{canonical}#app", "name": "UAE Corporate Tax registration deadline finder", "url": canonical,
         "description": CT_REG["card"], "applicationCategory": "BusinessApplication", "operatingSystem": "Any (runs in a web browser)",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"}, "provider": {"@id": ORG_ID}},
        {"@type": "HowTo", "@id": f"{canonical}#howto", "name": "How to register for Corporate Tax in the UAE",
         "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t} for i, (n, t) in enumerate(steps, 1)]},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("Corporate Tax registration", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    doc_cards = "\n".join(f'          <li class="incl"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in docs)
    step_items = "\n".join(f"          <li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in steps)
    ctas = """          <a class="btn btn-gold" href="#check" data-magnetic>Find your deadline <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="/services/corporate-tax-uae/" data-magnetic>Corporate Tax services</a>"""
    inner = f"""
    <section class="section" id="check" aria-labelledby="check-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Deadline finder</p>
          <h2 id="check-title" data-reveal="mask">When must you register?</h2>
          <p class="lead" data-reveal>Not sure you need to register at all? Start with the <a class="u-link" href="{CT_CHECK["path"]}">Corporate Tax filing check</a>. Your answers stay in your browser; nothing is sent or stored.</p>
        </div>
        <div class="sv-grid">
          <form class="ct-card sv-form" id="cr-form" novalidate>
            <label class="sv-field"><span>Who is registering?</span>
              <select name="who">
                <option value="uae">UAE company, incl. free zone</option>
                <option value="foreign">Foreign company managed in the UAE</option>
                <option value="person">Individual or freelancer</option>
                <option value="pe">Foreign company with a UAE branch</option>
              </select>
            </label>
            <label class="sv-field" data-for="uae"><span>Date of incorporation (or of the earliest licence, if before March 2024)</span><input name="inc" type="date" /></label>
            <label class="sv-field" data-for="foreign" hidden><span>End of the company's financial year</span><input name="fye" type="date" /></label>
            <label class="sv-field" data-for="person" hidden><span>Calendar year in which business turnover first exceeded AED 1 million</span><input name="year" inputmode="numeric" placeholder="e.g. 2026" /></label>
            <label class="sv-field" data-for="pe" hidden><span>Date the permanent establishment began</span><input name="pe" type="date" /></label>
          </form>
          <div class="ct-card sv-out" id="cr-result" aria-live="polite">
            <noscript><p>The deadline finder needs JavaScript. The deadlines it applies are set out below.</p></noscript>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="rules-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The rules</p>
          <h2 id="rules-title" data-reveal="mask">Deadlines, penalty and waiver.</h2>
          <p class="lead" data-reveal>FTA Decision No. 3 of 2024 (in force from 1 March 2024) and the FTA's Corporate Tax registration service. Checked {e(CT_REG_CHECKED)}.</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{fact_rows(rules)}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="docs-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Documents</p>
          <h2 id="docs-title" data-reveal="mask">What to have ready.</h2>
          <p class="lead" data-reveal>The FTA's list for a company. Government entities and qualifying public benefit entities also attach their decree or Cabinet decision.</p>
        </div>
        <ul class="incl-grid" data-reveal-stagger>
{doc_cards}
        </ul>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>On EmaraTax</p>
          <h2 id="steps-title" data-reveal="mask">Four steps to register.</h2>
          <p class="lead" data-reveal>Registering for VAT as well? See <a class="u-link" href="{VAT_REG["path"]}">VAT registration in the UAE</a>.</p>
        </div>
        <ol class="guide-steps" data-reveal-stagger>
{step_items}
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
    <script type="module" src="/assets/js/ct-registration.js"></script>
"""
    body = resource_shell(
        "Corporate Tax Registration UAE: Deadline & Steps | Accuminds",
        "Find your UAE Corporate Tax registration deadline under FTA Decision No. 3 of 2024, with the documents, EmaraTax steps and the AED 10,000 penalty waiver.",
        canonical, ld, "Free tool · Corporate Tax", "Corporate Tax registration in the UAE",
        "Find your registration deadline in a few clicks, then see the documents the FTA asks for, the steps on EmaraTax and how the late registration penalty waiver works.",
        ctas, inner, "Corporate Tax registration")
    out = ROOT / CT_REG["path"].strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


GRATUITY_EMBED = "/embed/gratuity-calculator/"
# What other sites paste. The plain link under the iframe is the credit (and the backlink);
# the script line resizes the iframe from the height the embed page posts.
GRATUITY_EMBED_CODE = (
    f'<iframe src="{SITE}{GRATUITY_EMBED}" title="UAE end-of-service gratuity calculator" '
    'width="100%" height="900" loading="lazy" style="border:0;max-width:980px;display:block"></iframe>\n'
    f'<p style="font-size:13px;margin:6px 0 0">UAE <a href="{SITE}{GRATUITY["path"]}">gratuity calculator</a> by Accuminds Consulting</p>\n'
    '<script>addEventListener("message",function(e){if(e.origin==="' + SITE + '"&&e.data&&e.data.type==="accuminds-embed-height")'
    '{document.querySelectorAll("iframe").forEach(function(f){if(f.contentWindow===e.source)f.style.height=e.data.height+"px"})}})</script>'
)


def gratuity_calculator(noscript_tail):
    """The form and result panel, shared by the calculator page and the embed (logic: assets/js/gratuity.js)."""
    return f"""        <div class="sv-grid">
          <form class="ct-card sv-form" id="gr-form" novalidate>
            <fieldset class="sv-field"><legend>Employee</legend>
              <label class="sv-pill"><input type="radio" name="who" value="foreign" checked /> Expatriate</label>
              <label class="sv-pill"><input type="radio" name="who" value="national" /> UAE national</label>
            </fieldset>
            <fieldset class="sv-field"><legend>Work model</legend>
              <label class="sv-pill"><input type="radio" name="kind" value="full" checked /> Full-time</label>
              <label class="sv-pill"><input type="radio" name="kind" value="part" /> Part-time</label>
              <label class="sv-pill"><input type="radio" name="kind" value="temp" /> Temporary</label>
            </fieldset>
            <label class="sv-field"><span>Last monthly basic salary (AED, without allowances)</span><input name="basic" inputmode="decimal" placeholder="e.g. 8,000" /></label>
            <label class="sv-field"><span>Start date</span><input name="start" type="date" /></label>
            <label class="sv-field"><span>Last working day</span><input name="end" type="date" /></label>
            <label class="sv-field"><span>Unpaid leave or absence (days, if any)</span><input name="unpaid" inputmode="numeric" placeholder="0" /></label>
            <div id="gr-part" class="gr-part" hidden>
              <label class="sv-field"><span>Your contracted hours per week</span><input name="parthours" inputmode="decimal" placeholder="e.g. 24" /></label>
              <label class="sv-field"><span>Full-time hours per week at your employer</span><input name="fullhours" inputmode="decimal" placeholder="48" /></label>
            </div>
          </form>
          <div class="ct-card sv-out" id="gr-result" aria-live="polite">
            <noscript><p>The calculator needs JavaScript. {noscript_tail}</p></noscript>
          </div>
        </div>"""


def gratuity_embed_page():
    """Bare calculator for other sites to iframe. noindex, with the canonical on the full page,
    so it never competes with /gratuity-calculator/ in search."""
    full = f"{SITE}{GRATUITY['path']}"
    body = f"""<!DOCTYPE html>
<html lang="en" class="js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>UAE Gratuity Calculator | Accuminds</title>
  <meta name="description" content="{e(GRATUITY['card'])}" />
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="{full}" />
  <link rel="icon" type="image/png" href="/assets/img/favicon-32.png" sizes="32x32" />
  <link rel="stylesheet" href="{FONT}" />
  <link rel="stylesheet" href="/assets/css/tokens.css" />
  <link rel="stylesheet" href="/assets/css/main.css" />
</head>
<body class="embed">
  <main class="embed-main">
{gratuity_calculator('See <a href="' + full + '" target="_blank" rel="noopener">the full calculator</a>.')}
    <p class="embed-credit">
      <a href="{full}" target="_blank" rel="noopener">Gratuity calculator by <b>Accuminds Consulting</b></a>
      <span>Federal Decree-Law No. 33 of 2021 · Estimate only, not legal advice</span>
    </p>
  </main>
  <script type="module" src="/assets/js/gratuity.js"></script>
  <script>
    // Tell the host page how tall the calculator is, so its iframe can fit it without scrolling.
    (function () {{
      if (window.parent === window) return;
      var last = 0;
      function post(force) {{
        var h = Math.ceil(document.body.getBoundingClientRect().height);
        if (force === true || h !== last) {{ last = h; parent.postMessage({{ type: 'accuminds-embed-height', height: h }}, '*'); }}
      }}
      new ResizeObserver(post).observe(document.body);
      // Repeat early on, in case the host page's listener was not ready for the first message.
      addEventListener('load', function () {{ [0, 400, 1500, 4000].forEach(function (ms) {{ setTimeout(post, ms, true); }}); }});
    }})();
  </script>
</body>
</html>
"""
    out = ROOT / GRATUITY_EMBED.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def gratuity_page():
    canonical = f"{SITE}{GRATUITY['path']}"
    rules = [
        ("Who is entitled", "Foreign full-time workers who have completed one or more years of continuous service (Article 51(2)). UAE nationals are covered by the pensions and social security law instead (Article 51(1)).", LABOUR_LAW),
        ("The rate", "The basic wage of 21 days for each of the first five years of service, and of 30 days for each year after that (Article 51(2)).", LABOUR_LAW),
        ("Which wage", "The last basic wage received: the wage in the contract, without allowances or benefits in kind (Article 51(5) and Article 1).", LABOUR_LAW),
        ("Part years and absence", "Parts of a year are paid in proportion once one year of continuous service is completed, and days of unpaid absence do not count as service (Article 51(3) and (4)).", LABOUR_LAW),
        ("The cap", "The total gratuity may not exceed two years' wage (Article 51(6)).", LABOUR_LAW),
        ("Part-time work", "A share of the full-time gratuity: contracted annual hours divided by full-time annual hours. No gratuity under the temporary work model or for service under a year (Article 30).", EXEC_REG),
        ("Deductions", "Only amounts due by law or a court judgment, such as loans, overpayments or approved penalties, under the conditions in Article 29.", EXEC_REG),
        ("When it is paid", "Within 14 days of the end of the contract, together with wages and other final dues (Article 53).", LABOUR_LAW),
    ]
    faq = [
        ("Is UAE gratuity calculated on basic salary or total salary?", "On the last basic salary. The Labour Law defines basic wage as the wage in the contract without allowances or benefits in kind, so housing and transport allowances are left out."),
        ("Do I get gratuity if I resign?", "Yes, once you have completed one year of continuous service. Article 51 of the current Labour Law gives the same formula whether the contract ends by resignation or termination."),
        ("What if I worked less than one year?", "Full-time foreign workers become entitled after one year of continuous service, so there is no gratuity for less. After that, part years are paid in proportion."),
        ("When must my employer pay my gratuity?", "Within 14 days of the end of the contract, with your other final dues (Article 53)."),
        ("Does this apply in free zones?", "It follows the federal Labour Law. DIFC and ADGM have their own employment laws, and domestic workers have a separate law, so the calculation can differ there."),
        ("What if my employer enrolled me in the savings scheme?", "Article 51(8) lets the Cabinet approve alternatives to gratuity, such as the voluntary end-of-service savings scheme. While you are enrolled, the scheme's contributions replace gratuity for that period."),
        ("Should employers set aside gratuity every month?", "Yes. Gratuity builds up as people work, so accruing it monthly keeps the liability in your accounts and avoids a large one-off cost when someone leaves."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "WebApplication", "@id": f"{canonical}#app", "name": "UAE end-of-service gratuity calculator", "url": canonical,
         "description": GRATUITY["card"], "applicationCategory": "BusinessApplication", "operatingSystem": "Any (runs in a web browser)",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"}, "provider": {"@id": ORG_ID}},
        breadcrumbs_ld([("Home", f"{SITE}/"), ("Gratuity calculator", canonical)]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    ctas = """          <a class="btn btn-gold" href="#calculate" data-magnetic>Calculate gratuity <span aria-hidden="true">&darr;</span></a>
          <a class="btn btn-ghost-light" href="/services/bookkeeping-accounting-dubai/" data-magnetic>Payroll and accounting help</a>"""
    inner = f"""
    <section class="section" id="calculate" aria-labelledby="calc-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The calculator</p>
          <h2 id="calc-title" data-reveal="mask">Your <span class="nowrap">end-of-service</span> gratuity.</h2>
          <p class="lead" data-reveal>Your answers stay in your browser; nothing is sent or stored.</p>
        </div>
{gratuity_calculator("The rules it follows are set out below.")}
      </div>
    </section>

    <section class="section section--white" id="embed" aria-labelledby="embed-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>For HR teams and websites</p>
          <h2 id="embed-title" data-reveal="mask">Add this calculator to your website.</h2>
          <p class="lead" data-reveal>Free to use on your HR portal, blog or intranet. Paste this code where you want the calculator to appear. It runs in your visitors' browsers, and nothing they enter is sent anywhere.</p>
        </div>
        <div class="ct-card gr-embed">
          <label class="sv-field"><span>Embed code</span><textarea id="gr-embed-code" rows="6" readonly spellcheck="false">{e(GRATUITY_EMBED_CODE)}</textarea></label>
          <p class="gr-embed__row"><button class="btn btn-gold btn-sm" type="button" id="gr-embed-copy">Copy code</button> <span class="ct-hint" id="gr-embed-status" aria-live="polite"></span></p>
          <p class="ct-note">The last line keeps the calculator the right height; if your site does not allow scripts, leave it out and the calculator scrolls instead. Please keep the credit link.</p>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="rules-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The law</p>
          <h2 id="rules-title" data-reveal="mask">How gratuity is worked out.</h2>
          <p class="lead" data-reveal>Federal Decree-Law No. 33 of 2021 on labour relations and its Executive Regulation, Cabinet Resolution No. 1 of 2022. Checked {e(GRATUITY_CHECKED)} on the UAE Legislation portal.</p>
        </div>
        <dl class="facts-list" data-reveal-stagger>
{fact_rows(rules)}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="example-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Worked example</p>
          <h2 id="example-title" data-reveal="mask">Seven years on AED 8,000 basic.</h2>
        </div>
        <ol class="guide-steps" data-reveal-stagger>
          <li><h3>Daily basic wage</h3><p>AED 8,000 &divide; 30 = AED 266.67.</p></li>
          <li><h3>First five years</h3><p>5 &times; 21 days &times; AED 266.67 = AED 28,000.</p></li>
          <li><h3>Years six and seven</h3><p>2 &times; 30 days &times; AED 266.67 = AED 16,000.</p></li>
          <li><h3>Total gratuity</h3><p>AED 44,000, well under the cap of two years' wage.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(faq)}
        </div>
      </div>
    </section>
    <script type="module" src="/assets/js/gratuity.js"></script>
"""
    body = resource_shell(
        "UAE Gratuity Calculator: End of Service Benefits | Accuminds",
        "Free UAE end-of-service gratuity calculator under the federal Labour Law: 21 and 30 days' basic wage, part years, part-time work and the cap.",
        canonical, ld, "Free tool · Labour Law", "UAE end-of-service gratuity calculator",
        "Work out the gratuity due at the end of employment under the federal Labour Law: 21 days' basic wage a year for the first five years, 30 days after that.",
        ctas, inner, "payroll and gratuity")
    out = ROOT / "gratuity-calculator" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


# ---------------------------------------------------------------- PINT AE rule pages
PINT_ID = re.compile(r"\b(?:IBR-(?:CO-|SR-|CL-)?\d+(?:-AE)?|IBT-\d+(?:-\d+)?|BTAE-\d+|IBG-\d+|ALIGNED-IBRP-[A-Z]+-\d+(?:-AE)?)\b")


def pint_ids(topic):
    """Official PINT AE rule and field numbers a topic covers, in order of first mention."""
    text = topic["answer"] + " " + " ".join(PINT_BY_ID[r]["source_reference"] for r in topic["rules"])
    return list(dict.fromkeys(PINT_ID.findall(text)))


def applies_to(rule):
    w = rule["applies_when"]
    if not w:
        return "All invoices"
    if w["field"] == "transaction_type":
        return "B2B and B2G invoices"
    if w["field"] == "invoice_type_code":
        return "Credit notes (type codes " + " and ".join(w["in"]) + ")"
    if w["field"] == "currency_code" and "not_in" in w:
        return "Invoices not in " + ", ".join(w["not_in"])
    return "Some invoices"


def rule_card(rule):
    sev = rule["severity"]
    rows = [("Official references", rule["source_reference"]), ("Applies to", applies_to(rule)), ("How to fix", rule["fix_hint"])]
    if rule.get("verify_note"):
        rows.append(("Note", rule["verify_note"]))
    meta = "\n".join(f"              <div><dt>{e(t)}</dt><dd>{keep_together(e(d))}</dd></div>" for t, d in rows)
    return f"""          <article class="rule-card">
            <div class="rule-head"><span class="rule-sev rule-sev--{sev}">{e(sev.capitalize())}</span><span class="rule-check">Checker rule {e(rule["id"])}</span></div>
            <h3>{e(rule["description"])}</h3>
            <dl class="rule-meta">
{meta}
            </dl>
          </article>"""


def keep_together(text):
    """Stops lines breaking inside "e-invoices" or a rule number such as IBR-132-AE (escaped text in, HTML out)."""
    text = re.sub(r"\b(e-invoic\w*)", r'<span class="nowrap">\1</span>', text)
    return PINT_ID.sub(lambda m: f'<span class="nowrap">{m.group(0)}</span>', text)


def pint_shell(title, description, canonical, ld, trail, eyebrow, h1, lead, inner):
    return f"""{head(title, description, canonical, ld)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{HEADER}

  <main id="main">
    <section class="page-hero on-dark" aria-labelledby="page-title">
      <div class="container">
        {breadcrumbs_html(trail)}
        <p class="eyebrow" data-reveal>{e(eyebrow)}</p>
        <h1 id="page-title" data-reveal="mask">{keep_together(e(h1))}</h1>
        <p class="lead" data-reveal>{e(lead)}</p>
        <div class="hero-ctas" data-reveal-stagger>
          <a class="btn btn-gold" href="{CHECKER["path"]}" data-magnetic>Check your invoices free <span aria-hidden="true">&rarr;</span></a>
          <a class="btn btn-ghost-light" href="/services/e-invoicing-uae/" data-magnetic>E-invoicing readiness service</a>
        </div>
        <p class="guide-meta" data-reveal>Plain-English summary of the published specification, checked against {e(SPEC_AS_OF)}. The specification itself is authoritative.</p>
      </div>
    </section>
{inner}
{cta_band("e-invoicing")}
  </main>

{footer()}
</body>
</html>
"""


def pint_topic_page(t):
    canonical = pint_url(t["slug"])
    trail = [("Home", f"{SITE}/"), ("PINT AE rules", pint_url()), (t["name"], canonical)]
    ids = pint_ids(t)
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(),
        {"@type": "TechArticle", "@id": f"{canonical}#article", "headline": t["h1"], "description": t["description"],
         "url": canonical, "inLanguage": "en", "dateModified": TODAY, "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
         "keywords": ", ".join(ids), "about": [{"@type": "Thing", "name": "PINT AE"}, {"@type": "Thing", "name": "UAE e-invoicing"}]},
        breadcrumbs_ld(trail),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]}
    chips = "\n".join(f"            <li>{e(i)}</li>" for i in ids)
    cards = "\n".join(rule_card(PINT_BY_ID[r]) for r in t["rules"])
    others = [x for x in PINT_TOPICS if x["slug"] != t["slug"]]
    related = "\n".join(
        f"""          <a class="related-card" href="{PINT_RULES["path"]}{x["slug"]}/"><span class="related-pillar">PINT AE</span><span class="related-name">{e(x["name"])}</span><span class="related-desc">{e(x["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""
        for x in others)
    inner = f"""
    <section class="section" aria-labelledby="answer-title">
      <div class="container">
        <div class="answer-box" data-reveal>
          <h2 id="answer-title">The short answer</h2>
          <p>{keep_together(e(t["answer"]))}</p>
          <ul class="rule-ids" aria-label="Rule and field numbers on this page">
{chips}
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="checks-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>The checks</p>
          <h2 id="checks-title" data-reveal="mask">What we check, and how to fix it.</h2>
          <p class="lead" data-reveal>Each check below runs in our free e-invoice readiness checker. Critical checks count towards the readiness score; warnings are listed but carry no weight.</p>
        </div>
        <div class="rule-list" data-reveal-stagger>
{cards}
        </div>
        <p class="guide-meta"><a class="u-link" href="{e(PINT_AE_RULES[1])}" target="_blank" rel="noopener">{e(PINT_AE_RULES[0])}<span class="sr-only"> (opens in a new tab)</span></a> · <a class="u-link" href="{e(PINT_AE[1])}" target="_blank" rel="noopener">{e(PINT_AE[0])}<span class="sr-only"> (opens in a new tab)</span></a></p>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(t["faq"])}
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="more-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>More PINT AE rules</p>
          <h2 id="more-title" data-reveal="mask">The other topics.</h2>
        </div>
        <div class="related-grid related-grid--all" data-reveal-stagger>
{related}
        </div>
      </div>
    </section>
"""
    body = pint_shell(t["title"], t["description"], canonical, ld, trail, "PINT AE rules · UAE e-invoicing", t["h1"], t["card"], inner)
    out = ROOT / "pint-ae-rules" / t["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


PINT_KINDS = ("IBR", "ALIGNED", "IBT", "IBG", "BTAE")


def pint_sort_key(i):
    kind = i.split("-")[0]
    num = (re.findall(r"\d+", i) or ["0"])[0]
    return (PINT_KINDS.index(kind) if kind in PINT_KINDS else len(PINT_KINDS), i.replace(num, num.zfill(4), 1))


def pint_hub_page():
    canonical = pint_url()
    trail = [("Home", f"{SITE}/"), ("PINT AE rules", canonical)]
    ld = {"@context": "https://schema.org", "@graph": [
        org_node(), breadcrumbs_ld(trail),
        {"@type": "ItemList", "name": "PINT AE rules by topic", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": pint_url(t["slug"]), "name": t["h1"]} for i, t in enumerate(PINT_TOPICS)]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PINT_HUB["faq"]]},
    ]}
    cards = "\n".join(
        f"""          <a class="related-card" href="{PINT_RULES["path"]}{t["slug"]}/"><span class="related-pillar">PINT AE</span><span class="related-name">{e(t["name"])}</span><span class="related-desc">{e(t["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""
        for t in PINT_TOPICS)
    index = {}
    for t in PINT_TOPICS:
        for i in pint_ids(t):
            index.setdefault(i, [])
            if t not in index[i]:
                index[i].append(t)
    rows = "\n".join(
        f"""            <tr><td>{e(i)}</td><td>{", ".join(f'<a class="u-link" href="{PINT_RULES["path"]}{t["slug"]}/">{e(t["name"])}</a>' for t in ts)}</td></tr>"""
        for i, ts in sorted(index.items(), key=lambda kv: pint_sort_key(kv[0])))
    inner = f"""
    <section class="section" aria-label="Topics">
      <div class="container">
        <div class="related-grid related-grid--all" data-reveal-stagger>
{cards}
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="index-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Index</p>
          <h2 id="index-title" data-reveal="mask">Find a rule or field number.</h2>
          <p class="lead" data-reveal>Every PINT AE rule (IBR), field (IBT, BTAE) and group (IBG) number these pages cover, and where it is explained.</p>
        </div>
        <table class="rule-index">
          <thead><tr><th scope="col">Rule or field</th><th scope="col">Explained in</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow" data-reveal>Questions</p>
          <h2 id="faq-title" data-reveal="mask">Common questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal-stagger>
{faq_html(PINT_HUB["faq"])}
        </div>
      </div>
    </section>
"""
    body = pint_shell(PINT_HUB["title"], PINT_HUB["description"], canonical, ld, trail, "PINT AE rules · UAE e-invoicing",
                      PINT_HUB["h1"], PINT_HUB["lead"], inner)
    out = ROOT / "pint-ae-rules" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out


def sitemap():
    urls = ([f"{SITE}/", url()] + [url(s["slug"]) for s in SERVICES] + [f"{SITE}{CHECKER['path']}"]
            + [guide_url()] + [guide_url(g["slug"]) for g in GUIDES]
            + [f"{SITE}{CT_CHECK['path']}", f"{SITE}{MIS_TEMPLATE['path']}", f"{SITE}{SV_CHECK['path']}", f"{SITE}{TRN_CHECK['path']}", f"{SITE}{VAT_REG['path']}", f"{SITE}{CT_REG['path']}"]
            + [f"{SITE}{GRATUITY['path']}"]
            + [pint_url()] + [pint_url(t["slug"]) for t in PINT_TOPICS])
    rows = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n',
        encoding="utf-8")


def llms_txt():
    lines = [
        "# Accuminds Consulting FZCO",
        "",
        "> Finance, compliance and automation consultancy for SMEs and free zone companies in the UAE, based in Dubai Silicon Oasis (IFZA).",
        "",
        "Accuminds provides bookkeeping and accounting, UAE VAT and Corporate Tax compliance, e-invoicing readiness, part-time CFO advisory, MIS and management reporting, and AI-assisted accounting automation.",
        "",
        "Contact: info@accumindsconsulting.ae · +971 50 98 67247 (phone and WhatsApp) · DSO - IFZA, IFZA Properties, Dubai Silicon Oasis, Dubai, UAE",
        "",
        "## Services",
        "",
    ]
    lines += [f"- [{s['name']}]({url(s['slug'])}): {s['card']}" for s in SERVICES]
    lines += ["", "## Free tools", "", f"- [{CHECKER['name']}]({SITE}{CHECKER['path']}): {CHECKER['card']} Runs in the browser; invoice files are not uploaded."]
    lines += ["", "## Free tools and templates", "",
              f"- [{CT_CHECK['name']}]({SITE}{CT_CHECK['path']}): {CT_CHECK['card']}",
              f"- [{MIS_TEMPLATE['name']}]({SITE}{MIS_TEMPLATE['path']}): {MIS_TEMPLATE['card']}",
              f"- [{SV_CHECK['name']}]({SITE}{SV_CHECK['path']}): {SV_CHECK['card']}",
              f"- [{VAT_REG['name']}]({SITE}{VAT_REG['path']}): {VAT_REG['card']} Runs in the browser; nothing is sent.",
              f"- [{CT_REG['name']}]({SITE}{CT_REG['path']}): {CT_REG['card']} Runs in the browser; nothing is sent.",
              f"- [{TRN_CHECK['name']}]({SITE}{TRN_CHECK['path']}): {TRN_CHECK['card']} The format check runs in the browser; nothing is sent.",
              f"- [{GRATUITY['name']}]({SITE}{GRATUITY['path']}): {GRATUITY['card']} Runs in the browser; nothing is sent."]
    lines += ["", "## Guides", ""] + [f"- [{g['h1']}]({guide_url(g['slug'])}): {g['card']}" for g in GUIDES]
    lines += ["", "## PINT AE rules (UAE e-invoicing)", "", f"- [{PINT_HUB['h1']}]({pint_url()}): {PINT_RULES['card']}"]
    lines += [f"- [{t['h1']}]({pint_url(t['slug'])}): {t['card']}" for t in PINT_TOPICS]
    lines += ["", "## Pages", "", f"- [Home]({SITE}/): overview, how we work, contact form", f"- [All services]({url()})", ""]
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def refresh_home_footer():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    start, end = "<!-- SERVICE-LINKS:START -->", "<!-- SERVICE-LINKS:END -->"
    if start not in s:
        print("index.html: SERVICE-LINKS markers not found, footer links not refreshed")
        return
    a, b = s.index(start) + len(start), s.index(end)
    block = f"\n{footer_columns()}\n      "
    p.write_text(s[:a] + block + s[b:], encoding="utf-8")


if __name__ == "__main__":
    written = [hub_page()] + [service_page(s) for s in SERVICES] + [guides_hub()] + [guide_page(g) for g in GUIDES]
    written += [mis_template_page(), ct_check_page(), supplier_check_page(), trn_page(), vat_registration_page(), ct_registration_page()]
    written += [gratuity_page(), gratuity_embed_page()]
    written += [pint_hub_page()] + [pint_topic_page(t) for t in PINT_TOPICS]
    sitemap()
    llms_txt()
    refresh_home_footer()
    for w in written:
        print("wrote", w.relative_to(ROOT))
    print("wrote sitemap.xml, llms.txt")
    # Last, so the tags match the CSS/JS on disk now.
    print("versioned assets on", len(stamp_all()), "pages")
