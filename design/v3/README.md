# Accuminds Consulting — Website

This is the production website for **Accuminds Consulting - FZCO**, generated from the Accuminds Design System.

Live at **www.accumindsconsulting.ae**.

---

## What's here

```
site/
├── index.html          ← everything: HTML + inlined CSS + inlined JS
└── assets/
    ├── logo-mark-blue-transparent.png   (header logo)
    ├── logo-mark-white.png              (hero + footer logo)
    └── logo-square-blue.png             (favicon + social preview)
```

That's it. No build step, no npm, no framework.

---

## How to deploy (GitHub Pages)

Your repo is `hi10patel/accuminds-website`, served by GitHub Pages.

### Option 1 — Replace the whole site (cleanest)

1. Clone your repo:
   ```bash
   git clone https://github.com/hi10patel/accuminds-website.git
   cd accuminds-website
   ```
2. Delete the old `index.html` and `AM logo.png`.
3. Copy the **contents of this `site/` folder** into the repo root:
   ```
   accuminds-website/
   ├── CNAME              ← keep (this is what maps www.accumindsconsulting.ae)
   ├── index.html         ← from site/
   └── assets/            ← from site/
   ```
4. Commit and push:
   ```bash
   git add -A
   git commit -m "Rebrand: new design system, AI services, navy palette"
   git push
   ```
5. GitHub Pages will publish automatically within ~1 minute. Your URL stays the same.

### Option 2 — Preview locally first

Open `site/index.html` in any browser. That's all — no server needed. Fonts and icons load from CDNs (Google Fonts, Lucide), so you need an internet connection to see them styled correctly.

---

## Customization cheatsheet

All edits are in `index.html`.

| I want to change… | Search for… |
|---|---|
| Colors (navy / gold / teal) | `:root {` near the top |
| Fonts | `<link href="https://fonts.googleapis.com/css2?` |
| Hero headline | `<h1>Accurate books.` |
| Service cards | `<article class="svc-card">` |
| Phone / email / address | `contact-list` |
| Social preview image | `<meta property="og:image"` |

---

## Notes & caveats

- **Mailto form:** the contact form uses `mailto:info@accumindsconsulting.ae` — it opens the visitor's email client. For a real form backend (instant inbox, no client required), we can wire Formspree, Getform, or Basin later (5-minute swap).
- **Favicon:** uses `assets/logo-square-blue.png`. If you want a proper `.ico` with crisper 16×16 / 32×32 renders, say the word.
- **Fonts:** Plus Jakarta Sans (Google Fonts) stands in for Canva Sans Bold. No licence needed.
- **Icons:** Lucide icon set, loaded from unpkg CDN.

---

## Want to change something?

Just ask. I can rewrite any section, swap colors, add pages (Services detail, Team, Case studies), wire up a form backend, or build an Arabic/bilingual version.
