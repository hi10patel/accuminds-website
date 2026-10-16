# AccuMinds Consulting FZCO: website

Live at **www.accumindsconsulting.ae**. Static site: plain HTML, CSS and JavaScript.
There is **no build step** and nothing to install to deploy it.

- Design source: the v3 layout and 3D logo, recoloured to the brand tokens (snapshot in `design/`)
- Brand tokens: Deep Navy `#1A2E4A` · Gold `#C9972B` · Teal `#0D8A7F` · Off-white `#F7F5F1`, Plus Jakarta Sans 400/600/800
- Motion: GSAP + ScrollTrigger, Lenis smooth scroll; respects reduced-motion settings

---

## 1. Preview locally

Needs Node 18 or newer (only for the preview server; the site itself has no dependencies).

```bash
npm run serve
```

Then open **http://localhost:4173**.

| Add to the URL | What you see |
|---|---|
| `?todo` | Every placeholder outlined in dashed red, including hidden ones (Numbers section, certifications, client logos, testimonial, licence no., TRN) |
| `?todo&demo` | Same, plus the Numbers count-up running on dummy values so you can judge the motion. Dummy values never appear on the live site |

---

## 2. Before launch: fill in the placeholders

List everything still open:

```bash
npm run check:todo
```

| Placeholder | Where (search `index.html` for…) | Shown on the live site until done? | What to do |
|---|---|---|---|
| Numbers (4 stats) | `data-count="TODO"` | No, section hidden | Replace `TODO` with plain numbers (e.g. `data-count="240"`), remove `data-todo` from those spans and `data-todo-slot` from `<section id="numbers">` |
| Certifications, client logos, testimonial | `class="trust"` | No, hidden | Real items only (logos with permission, testimonials with written consent). Remove `data-todo-slot` when filled; delete what you don't need |
| Trade licence no. and TRN | `footer-legal` | No, hidden | Fill both, remove `data-todo` and `data-todo-slot` |
| Structured data extras | `Structured data. TODO` | n/a | Optionally add `geo`, `openingHoursSpecification`, `sameAs` (LinkedIn etc.) and `taxID` to the JSON-LD in `<head>` |

**Contact form:** delivered by Formspree (form ID `xkjokqyk`, free plan, sends to info@accumindsconsulting.ae). Submissions also appear in the Formspree dashboard. To use a different form, put its ID in **both** `data-formspree="…"` and `action="https://formspree.io/f/…"` on `#contact-form`. The free plan can't restrict the form to this domain; the hidden `_gotcha` honeypot field and Formspree's own spam filtering cover that.

Blocks marked `data-todo-slot` **never render on the live site** until you remove that attribute, so nothing invented can go public by accident.

---

## 3. Deploy

### GitHub Pages (current set-up)

The repo `hi10patel/accuminds-website` is served by GitHub Pages from the root of `main`. `CNAME` maps the custom domain, so keep that file.

1. Push the redesign branch and open a pull request:
   ```bash
   git push -u origin redesign-motion
   ```
2. Review it, then merge into `main` on GitHub.
3. GitHub Pages republishes automatically, usually within a minute or two. No settings change is needed. If you ever need to check them: **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)`**, and keep **Enforce HTTPS** on.

Future edits follow the same pattern: edit, commit, push to `main` (or merge a PR).

### Netlify (alternative)

1. **Add new site → Import an existing project →** pick the GitHub repo.
2. Build command: *(leave empty)*. Publish directory: `.`
3. Add the custom domain under **Domain management**.
4. Forms: either keep Formspree, or switch to Netlify Forms by adding `name="contact" data-netlify="true"` to `#contact-form`, setting `action="/"` and changing `data-formspree` to `"TODO"`.

`404.html`, `robots.txt` and `sitemap.xml` work on both hosts as they are.

---

## 4. Editing copy

All visible text is in **`index.html`**. Each section starts with a comment banner such as `<!-- ================= SERVICES ================= -->`.

| I want to change… | Search `index.html` for… | Notes |
|---|---|---|
| Hero headline, intro, buttons, trust row | `story-final` | The final frame of the hero story; also the whole hero when motion is reduced |
| Hero captions ("Receipts in WhatsApp…", "We untangle it…") | `cap--1`, `cap--2` | |
| The giant words TANGLED / CLARITY | `word--tangled`, `word--clarity` | Each word appears twice (behind and in front of the 3D). Letters marked `is-front` sit in front of the wire; keep both copies identical |
| A service | `svc-card` | Edit the `<h3>`, `<p>` and the `<li>` items. Leave the `<svg>` icons alone |
| Service names in the form | `<select name="service"` | Keep them in step with the card titles and the `data-service="…"` on each card's link |
| How we work steps | `process-step` | Four steps; the animation is timed for four |
| Automation showcase text | `automation-title` | The workbook and dashboard figures come from `tools/gen_showcase.py` (see section 5) |
| Numbers | `class="stat"` | See section 2 |
| About text and fact tiles | `about-text`, `class="fact"` | |
| Phone, email, address, WhatsApp | the old value, e.g. `509867247` | Each appears in the contact section, the footer **and** the JSON-LD in `<head>`; update all of them |
| Page title, description, social preview text | `<title>`, `og:`, `twitter:` | |
| Colours, fonts, spacing | `assets/css/tokens.css` | Change a token once and it applies everywhere |
| Dark page colours (backgrounds, text, lines) | `V2 DARK EDITORIAL THEME` in `assets/css/main.css` | The dark theme remaps the tokens there. The contact form card and the showcase screens keep light colours on purpose |

Rules of thumb:
- Write `&amp;` for **&** inside HTML text.
- Don't remove `data-…` attributes (`data-reveal`, `data-icon`, `data-service`…). The motion and form scripts rely on them.
- After editing, run `npm run serve` and check the page, plus `?todo` if you touched a placeholder.

---

## 4b. Service pages (SEO)

Each service has its own page, so it can rank for its own searches. There are seven, plus a hub at `/services/`:

| Page | URL |
|---|---|
| Bookkeeping & Accounting | `/services/bookkeeping-accounting-dubai/` |
| VAT | `/services/vat-services-uae/` |
| Corporate Tax | `/services/corporate-tax-uae/` |
| E-invoicing | `/services/e-invoicing-uae/` |
| CFO Advisory | `/services/cfo-advisory-dubai/` |
| MIS & Reporting | `/services/mis-reporting-dubai/` |
| AI Automation | `/services/ai-accounting-automation-uae/` |

**Don't edit the generated HTML.** All page copy lives in `tools/pages_content.py`: titles, descriptions, what's included, who it's for, key facts, FAQs and related services. After editing it, run:

```bash
python tools/build_pages.py
```

That rebuilds every service page, `sitemap.xml`, `llms.txt` and the service links in the home footer.

- **Key facts must have an official source** (FTA or Ministry of Finance) and carry the review date in `REVIEWED`. UAE rules change often, so re-check them, update `REVIEWED`, and rebuild.
- **Each page includes structured data** for search engines: Service, BreadcrumbList and FAQPage, plus a reference to the firm. FAQs are written as direct answers so AI assistants can quote them.
- **To add a service,** add an entry to `SERVICES` in `tools/pages_content.py`, rebuild, and add a "Learn more" link to the matching card on the home page.

### Telling search engines about changes

- **Google:** Search Console is verified by the `google-site-verification` meta tag in `index.html`. **Don't remove it.** The sitemap is submitted there.
- **Bing and other IndexNow engines:** the key file `0fb1f254e2294a41940ad768991c5054.txt` at the site root proves the site is ours. It's public by design, so keep it in place.

After a change is live, notify the IndexNow engines. To send every page in the sitemap:

```bash
npm run indexnow
```

To send only the pages you changed:

```bash
npm run indexnow -- https://www.accumindsconsulting.ae/services/vat-services-uae/
```

## 5. Images and generated assets

| Asset | Source | Regenerate with |
|---|---|---|
| Hero logo, header/footer marks, favicons | originals in `design/v3/assets/` | `python tools/optimise_images.py` (needs Pillow) |
| Social preview `assets/img/og-image.jpg` (1200×630) | `tools/og-image.html` | the steps in the comment at the top of that file |
| Automation showcase scene | `tools/gen_showcase.py` | `python tools/gen_showcase.py out.html`, then paste both `<svg>` blocks into `#automation` |

The hero logo is WebP only: lossy AVIF added faint noise to the transparent background, which showed as a dark box on navy.

---

## 6. Motion and accessibility

| Section | Motion | Reduced motion / no JS |
|---|---|---|
| Hero story | Scroll turns a real-time 3D wire ball into the gold spiral while TANGLED becomes CLARITY; the wire weaves through the letters; the headline and CTAs arrive at the end | Static hero: logo image + headline, no 3D downloaded |
| Services | Cards rise in; each icon loops while on screen | Finished icons |
| How we work | Pinned on desktop, line draws as you scroll, steps light up; vertical rail on smaller screens | All steps lit, no pin |
| Automation showcase | Workbook cleans itself up, then becomes the dashboard; Replay button | Before and after side by side |
| Numbers | Count-up once | Final values |
| About, Contact | Gentle staggered reveals | Visible immediately |
| Throughout | Lenis smooth scroll (mouse/trackpad only), magnetic CTAs, gold underline hovers | Native scrolling, no magnetic effect |

- **Pause motion** (in the hero) stops the 3D ball's idle drift and the icon loops. The choice is remembered on that device.
- Smaller screens get fewer network nodes at 30 fps, no pinning, no smooth-scroll library and no magnetic buttons.
- If the scripts fail to load, all content still shows (3-second safety net).
- To switch a feature off, comment out its `init…(motion)` line in `assets/js/main.js`.

Code map:

```
assets/js/main.js            entry point
assets/js/motion/core.js     Lenis + ScrollTrigger, reduced-motion switches, reveals, pause state
assets/js/motion/story.js    hero story: scroll timeline, poster, loads the 3D on demand
assets/js/story/            3D source (three.js): scene.js + wires.js → bundled to assets/js/story.bundle.js
assets/js/motion/icons.js    service icon loops  process.js  pinned timeline
assets/js/motion/showcase.js automation scene    stats.js    count-up
assets/js/ui/nav.js          header + mobile menu
assets/js/ui/magnetic.js     magnetic CTAs       contact.js  form, WhatsApp, floating button
```

Libraries are saved in `assets/vendor/` at pinned versions (checked against the npm registry's sha512 hashes): GSAP 3.15.0 and ScrollTrigger (GSAP standard no-charge licence), Lenis 1.3.27 (MIT). To upgrade, replace the files and update the three `<script>` tags in `<head>`.

---

## 7. Project structure

```
index.html            the page (all copy)
404.html              not-found page
CNAME                 custom domain for GitHub Pages
robots.txt, sitemap.xml, site.webmanifest, favicon.ico, .nojekyll
assets/css/           tokens.css (brand tokens) + main.css (layout and sections)
assets/js/            see the code map above
assets/img/           optimised images (generated, committed)
assets/vendor/        GSAP, ScrollTrigger, Lenis
design/               reference snapshot: v3 design, previous live site, logo animation prototype
tools/                preview server, TODO checker, image/scene generators
```

---

## 7b. The 3D hero

The tangled wire ball is generated in code with three.js 0.186.1 (`assets/js/story/wires.js`); there are no model files. Scrolling blends it into the spiral on the GPU, using a vertex shader, so it costs the CPU almost nothing per frame.

**How it loads (keeps the page fast):**
- First paint shows `assets/img/story-poster.webp`, a still of the ball's first frame, positioned exactly where the 3D ball will render.
- The 3D bundle (`assets/js/story.bundle.js`, about 140 KB gzipped) loads on the visitor's first interaction: a mouse move on desktop, scroll or touch on phones. It then fades in over the poster.
- Without WebGL 2, or with the Save-Data setting, the poster stays.
- With reduced motion, the hero is static and nothing 3D is downloaded.

**After editing `assets/js/story/`:** run `npm install` once, then rebuild the bundle:

```bash
npm run build:3d
```

**If the shape, materials or camera changed,** also regenerate the poster. Start the preview server first (`npm run serve`), then:

```bash
npm run poster:3d
```

```bash
python tools/optimise_images.py
```

## 8. QA results (16 Oct 2026, branch `redesign-motion`)

### Lighthouse 12.8.2 (local server with gzip, as GitHub Pages serves it)

| Run | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|
| Mobile (run 1) | **97** | **100** | 100 | **100** | 1.2 s | 2.0 s | 160 ms | 0 |
| Mobile (run 2) | **97** | **100** | 100 | **100** | 1.2 s | 2.1 s | 120 ms | 0 |
| Desktop | **100** | **100** | 100 | **100** | 0.4 s | 0.8 s | 0 ms | 0.002 |

Targets: Performance ≥ 90, Accessibility ≥ 95, SEO ≥ 95. All met.

With the 3D hero and the dark editorial restyle (branch `redesign-v2`, same set-up):

| Run | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|
| Mobile | **95** | **100** | 100 | **100** | 1.2 s | 2.3 s | 220 ms | 0.004 |
| Desktop | **100** | **100** | 100 | **100** | 0.3 s | 0.6 s | 0 ms | 0.007 |

Lighthouse doesn't interact with the page, so these runs measure the poster first paint; three.js loads on a visitor's first mouse move, scroll or touch.

To re-run, use a quiet machine; Lighthouse's lab TBT jumps when other heavy apps compete for the CPU:

```bash
npx lighthouse http://localhost:4173/ --view
```

```bash
npx lighthouse http://localhost:4173/ --preset=desktop --view
```

Fixes made during QA:
- Fonts load without blocking first paint.
- Below-the-fold set-up runs in idle time, with one ScrollTrigger refresh after set-up and one after fonts load.
- On small screens the hero mark is visible from the first paint (it is the LCP element); desktop keeps the full reveal.
- A cheaper hero shadow, the canvas fade drawn in JS, and header blur only after scrolling.
- Right-sized logo images.
- Upcoming "How we work" steps start hidden rather than dimmed (contrast).
- Footer brand link name fixed.

### Reduced motion (`prefers-reduced-motion: reduce`, desktop and 375px)
- No smooth scroll, no pinning, no looping or scroll-scrubbed animation; the hero background is static and the Pause control is hidden
- After scrolling the whole page every element is visible; icons show their finished frames; all four process steps lit; showcase shows before and after side by side; no clipped hero

### Mobile (375px, touch emulation)
- No horizontal overflow at any scroll position; no text smaller than 12px
- No pinning or smooth-scroll library on touch; hero network at 16 nodes / 30 fps
- Interactive targets ≥ 24px (WCAG 2.2 AA); buttons ≥ 40px

### Contact form (automated)
- "Discuss this" pre-selects the service and tailors the WhatsApp text; empty form blocked by validation
- Without a Formspree ID: email app opens with the message pre-filled, confirmation shown and focused
- With a Formspree ID (stubbed network): JSON request to `formspree.io/f/<id>` with all fields; failure shows the inline error and restores the button; success resets the form
