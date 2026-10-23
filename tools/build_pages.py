"""Builds the service pages from tools/pages_content.py.

    python tools/build_pages.py

Writes:
  services/index.html                 services hub
  services/<slug>/index.html          one page per service
  guides/index.html                   e-invoicing software guides hub (tools/guides_content.py)
  mis-report-template/index.html      free MIS pack download (file: tools/build_mis_template.py)
  corporate-tax-check/index.html      Corporate Tax filing check (logic: assets/js/ct-check.js)
  supplier-verification-check/        FTA Decision 13 supplier checks (logic: assets/js/supplier-check.js)
  guides/<slug>/index.html            one page per guide
  sitemap.xml, llms.txt               regenerated from the same content
  index.html                          refreshes the footer service links
                                      (between the SERVICE-LINKS markers)
The pages share the home page's CSS/JS, header and footer. Paths are
root-absolute (/assets/...), which works on the custom domain and in
`npm run serve`.
"""
import json
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from pages_content import REVIEWED, SERVICES  # noqa: E402
from guides_content import CHECKED, CHECKLIST, DEADLINES, GUIDES, MOF_ASP, PINT_AE, PINT_AE_RULES  # noqa: E402

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
# Free tool published from the uae-einvoice-checker repo (npm run sync:checker).
CHECKER = {"path": "/e-invoice-checker/", "name": "Free E-Invoice Readiness Checker",
           "card": "Check sample sales invoices against the UAE e-invoicing (PINT AE) mandatory fields in your browser, with a readiness score, gap list and PDF report."}
FONT = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap"

e = lambda t: escape(t, quote=True)  # noqa: E731


def url(slug=None):
    return f"{SITE}/services/{slug}/" if slug else f"{SITE}/services/"


def guide_url(slug=None):
    return f"{SITE}/guides/{slug}/" if slug else f"{SITE}/guides/"


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


def service_links(current=None, base="/services/"):
    items = []
    for s in SERVICES:
        cur = ' aria-current="page"' if s["slug"] == current else ""
        items.append(f'<li><a class="u-link" href="{base}{s["slug"]}/"{cur}>{e(s["name"])}</a></li>')
    items.append(f'<li><a class="u-link" href="{CHECKER["path"]}">{e(CHECKER["name"])}</a></li>')
    items.append('<li><a class="u-link" href="/guides/">E-Invoicing Software Guides</a></li>')
    items.append(f'<li><a class="u-link" href="{CT_CHECK["path"]}">{e(CT_CHECK["name"])}</a></li>')
    items.append(f'<li><a class="u-link" href="{SV_CHECK["path"]}">{e(SV_CHECK["name"])}</a></li>')
    items.append(f'<li><a class="u-link" href="{MIS_TEMPLATE["path"]}">{e(MIS_TEMPLATE["name"])}</a></li>')
    return "\n            ".join(items)


def footer(current=None):
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      <a class="footer-brand" href="/">
        <img src="/assets/img/mark-3d.webp" width="77" height="28" alt="" loading="lazy" decoding="async" />
        <span class="wordmark-light">Accuminds Consulting · FZCO</span>
      </a>
      <nav aria-label="Services">
        <ul class="footer-nav footer-services">
            {service_links(current)}
        </ul>
      </nav>
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
                 "Practical UAE e-invoicing guides for QuickBooks, Zoho Books and TallyPrime users: Accredited Service Providers, setup steps, data checklists and deadlines.",
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
        <h1 id="page-title" data-reveal="mask">{e(h1)}</h1>
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
    ctas = f"""          <a class="btn btn-gold" href="{MIS_TEMPLATE["file"]}" download data-magnetic>Download the template (Excel) <span aria-hidden="true">&darr;</span></a>
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
        "Free Monthly MIS Report Template for SMEs (Excel) | Accuminds",
        "Download a free Excel MIS report template: P&L against budget, KPIs, working-capital days, a three-month cash outlook and management commentary prompts.",
        canonical, ld, "Free template", "Monthly MIS report template",
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


def sitemap():
    urls = ([f"{SITE}/", url()] + [url(s["slug"]) for s in SERVICES] + [f"{SITE}{CHECKER['path']}"]
            + [guide_url()] + [guide_url(g["slug"]) for g in GUIDES]
            + [f"{SITE}{CT_CHECK['path']}", f"{SITE}{MIS_TEMPLATE['path']}", f"{SITE}{SV_CHECK['path']}"])
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
              f"- [{SV_CHECK['name']}]({SITE}{SV_CHECK['path']}): {SV_CHECK['card']}"]
    lines += ["", "## Guides", ""] + [f"- [{g['h1']}]({guide_url(g['slug'])}): {g['card']}" for g in GUIDES]
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
    block = f"""
      <nav aria-label="Services">
        <ul class="footer-nav footer-services">
            {service_links()}
        </ul>
      </nav>
      """
    p.write_text(s[:a] + block + s[b:], encoding="utf-8")


if __name__ == "__main__":
    written = [hub_page()] + [service_page(s) for s in SERVICES] + [guides_hub()] + [guide_page(g) for g in GUIDES]
    written += [mis_template_page(), ct_check_page(), supplier_check_page()]
    sitemap()
    llms_txt()
    refresh_home_footer()
    for w in written:
        print("wrote", w.relative_to(ROOT))
    print("wrote sitemap.xml, llms.txt")
