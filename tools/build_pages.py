"""Builds the service pages from tools/pages_content.py.

    python tools/build_pages.py

Writes:
  services/index.html                 services hub
  services/<slug>/index.html          one page per service
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

SITE = "https://www.accumindsconsulting.ae"
WA = "971509867247"
TODAY = date.today().isoformat()
BY_SLUG = {s["slug"]: s for s in SERVICES}
ORG_ID = f"{SITE}/#organization"
# Free tool published from the uae-einvoice-checker repo (npm run sync:checker).
CHECKER = {"path": "/e-invoice-checker/", "name": "Free E-Invoice Readiness Checker",
           "card": "Check sample sales invoices against the UAE e-invoicing (PINT AE) mandatory fields in your browser, with a readiness score, gap list and PDF report."}
FONT = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap"

e = lambda t: escape(t, quote=True)  # noqa: E731


def url(slug=None):
    return f"{SITE}/services/{slug}/" if slug else f"{SITE}/services/"


def wa_link(topic):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(f'Hello AccuMinds, I would like to discuss {topic}.')}"


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
  <meta property="og:site_name" content="AccuMinds Consulting FZCO" />
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
      <a class="brand" href="/" aria-label="AccuMinds Consulting, home">
        <img src="/assets/img/mark-3d.webp" width="88" height="32" alt="" />
        <span class="wordmark">AccuMinds</span>
      </a>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
        <ul>
          <li><a class="u-link" href="/services/">Services</a></li>
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
    return "\n            ".join(items)


def footer(current=None):
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      <a class="footer-brand" href="/">
        <img src="/assets/img/mark-3d.webp" width="77" height="28" alt="" loading="lazy" decoding="async" />
        <span class="wordmark-light">AccuMinds Consulting · FZCO</span>
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
        <a class="u-link" href="https://www.linkedin.com/company/accuminds-consulting/" rel="me noopener" target="_blank">LinkedIn</a>
      </address>
      <p class="footer-copy">© <span data-year>{date.today().year}</span> AccuMinds Consulting FZCO. All rights reserved.</p>
    </div>
  </footer>"""


def org_node():
    return {
        "@type": "ProfessionalService", "@id": ORG_ID, "name": "AccuMinds Consulting FZCO", "url": f"{SITE}/",
        "telephone": "+971509867247", "email": "info@accumindsconsulting.ae",
        "sameAs": ["https://www.linkedin.com/company/accuminds-consulting/"],
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
        tool_cta = f"""
          <a class="btn btn-ghost-light" href="{CHECKER["path"]}" data-magnetic>{e(s["tool"])} <span aria-hidden="true">&rarr;</span></a>"""

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
{facts_section}
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
        {"@type": "ItemList", "name": "AccuMinds services", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": url(s["slug"]), "name": s["name"]} for i, s in enumerate(SERVICES)]},
    ]}
    cards = "\n".join(
        f"""          <a class="related-card" href="/services/{s["slug"]}/"><span class="related-pillar">{e(s["pillar"])}</span><span class="related-name">{e(s["name"])}</span><span class="related-desc">{e(s["card"])}</span><span class="related-go" aria-hidden="true">→</span></a>"""
        for s in SERVICES)
    body = f"""{head("Accounting, VAT, Corporate Tax & CFO Services in Dubai | AccuMinds",
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


def sitemap():
    urls = [f"{SITE}/", url()] + [url(s["slug"]) for s in SERVICES] + [f"{SITE}{CHECKER['path']}"]
    rows = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n',
        encoding="utf-8")


def llms_txt():
    lines = [
        "# AccuMinds Consulting FZCO",
        "",
        "> Finance, compliance and automation consultancy for SMEs and free zone companies in the UAE, based in Dubai Silicon Oasis (IFZA).",
        "",
        "AccuMinds provides bookkeeping and accounting, UAE VAT and Corporate Tax compliance, e-invoicing readiness, part-time CFO advisory, MIS and management reporting, and AI-assisted accounting automation.",
        "",
        "Contact: info@accumindsconsulting.ae · +971 50 98 67247 (phone and WhatsApp) · DSO - IFZA, IFZA Properties, Dubai Silicon Oasis, Dubai, UAE",
        "",
        "## Services",
        "",
    ]
    lines += [f"- [{s['name']}]({url(s['slug'])}): {s['card']}" for s in SERVICES]
    lines += ["", "## Free tools", "", f"- [{CHECKER['name']}]({SITE}{CHECKER['path']}): {CHECKER['card']} Runs in the browser; invoice files are not uploaded."]
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
    written = [hub_page()] + [service_page(s) for s in SERVICES]
    sitemap()
    llms_txt()
    refresh_home_footer()
    for w in written:
        print("wrote", w.relative_to(ROOT))
    print("wrote sitemap.xml, llms.txt")
