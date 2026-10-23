// Publishes the UAE E-Invoice Readiness Checker at /e-invoice-checker/.
//
//   npm run sync:checker -- <path to a checkout of hi10patel/uae-einvoice-checker>
//
// The checker is a separate React (Vite) app with its own repo and tests. This
// script builds it with the /e-invoice-checker/ base path, replaces the
// e-invoice-checker/ folder here with the build, and adds what the page needs on
// this site: SEO tags, structured data, a static summary for crawlers, and the
// checker's Content-Security-Policy as a <meta> tag (GitHub Pages cannot send
// response headers). Run the checker's own `npm ci` and `npm test` first; then
// commit the folder and open a PR.
import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE = 'https://www.accumindsconsulting.ae';
const BASE = '/e-invoice-checker/';
const URL_ = `${SITE}${BASE}`;
const OUT = fileURLToPath(new URL(`..${BASE}`, import.meta.url));

// Same policy as the checker's public/_headers, minus frame-ancestors (ignored in a meta tag).
const CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; font-src 'self'; "
  + "connect-src 'self'; worker-src 'self' blob:; object-src 'none'; base-uri 'self'; form-action 'none'";

const TITLE = 'Free UAE E-Invoice Readiness Checker (PINT AE) | Accuminds';
const DESCRIPTION = 'Check your sales invoices against UAE e-invoicing (PINT AE) mandatory fields. '
  + 'Free readiness score, gap list and PDF report. Your file stays in your browser.';

// Shown inside #root until the app mounts (React replaces it), so crawlers that do not
// run JavaScript still see what the page is. Classes must exist in the checker's CSS.
const STATIC_BODY = `<main class="mx-auto max-w-3xl px-4 py-10 text-slate-700">
        <h1 class="text-3xl font-bold text-brand-navy">UAE E-Invoice Readiness Checker (PINT AE)</h1>
        <p class="mt-4">Check a sample of your sales invoices against the PINT AE fields used for UAE e-invoicing. Upload an Excel, CSV or PDF export, match your columns, and get a readiness score, the gaps rule by rule and a PDF report.</p>
        <ul class="mt-4 list-disc pl-5">
          <li>27 PINT AE 1.0.4 rules: 25 critical and 2 warnings.</li>
          <li>Column presets for TallyPrime, Zoho Books, QuickBooks Online, Odoo and SAP Business One.</li>
          <li>Your file is read inside your browser. Nothing is uploaded, stored or sent.</li>
        </ul>
        <p class="mt-4 text-sm">The checker needs JavaScript. See also <a href="/services/e-invoicing-uae/">UAE e-invoicing readiness</a> and the <a href="/guides/">e-invoicing software guides</a>.</p>
      </main>`;

const repo = process.argv[2] && resolve(process.argv[2]);
if (!repo || !existsSync(join(repo, 'src', 'rules', 'pint-ae-rules.json'))) {
  console.error('Usage: npm run sync:checker -- <path to the uae-einvoice-checker repo>');
  process.exit(1);
}

// 1. Build into a temp folder with this site's base path.
const tmp = mkdtempSync(join(tmpdir(), 'checker-'));
const vite = join(repo, 'node_modules', 'vite', 'bin', 'vite.js');
execFileSync(process.execPath, [vite, 'build', '--base', BASE, '--outDir', tmp, '--emptyOutDir'], { cwd: repo, stdio: 'inherit' });

// 2. Replace the published folder. Hosting files for Cloudflare/Vercel do not apply here.
rmSync(OUT, { recursive: true, force: true });
cpSync(tmp, OUT, { recursive: true, filter: (src) => !/[\\/](_headers|_redirects)$/.test(src) });
rmSync(tmp, { recursive: true, force: true });

// 3. Page head: SEO, social, structured data and the security policy.
const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
const ld = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'WebApplication',
      '@id': `${URL_}#app`,
      name: 'UAE E-Invoice Readiness Checker',
      url: URL_,
      description: DESCRIPTION,
      applicationCategory: 'BusinessApplication',
      operatingSystem: 'Any (runs in a web browser)',
      isAccessibleForFree: true,
      offers: { '@type': 'Offer', price: '0', priceCurrency: 'AED' },
      provider: { '@id': `${SITE}/#organization` },
      inLanguage: 'en',
    },
    {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE}/` },
        { '@type': 'ListItem', position: 2, name: 'E-Invoicing Readiness', item: `${SITE}/services/e-invoicing-uae/` },
        { '@type': 'ListItem', position: 3, name: 'E-Invoice Readiness Checker', item: URL_ },
      ],
    },
  ],
};
const tags = `
    <meta http-equiv="Content-Security-Policy" content="${CSP}" />
    <meta name="referrer" content="no-referrer" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#1A2E4A" />
    <link rel="canonical" href="${URL_}" />
    <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Accuminds Consulting FZCO" />
    <meta property="og:title" content="${esc(TITLE)}" />
    <meta property="og:description" content="${esc(DESCRIPTION)}" />
    <meta property="og:url" content="${URL_}" />
    <meta property="og:image" content="${SITE}/assets/img/og-image.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <script type="application/ld+json">${JSON.stringify(ld)}</script>`;

const page = join(OUT, 'index.html');
let html = readFileSync(page, 'utf8');
const set = (re, value, what) => {
  if (!re.test(html)) throw new Error(`checker index.html: ${what} not found`);
  html = html.replace(re, value);
};
set(/<title>[^<]*<\/title>/, `<title>${esc(TITLE)}</title>`, '<title>');
set(/<meta name="description" content="[^"]*"\s*\/?>/, `<meta name="description" content="${esc(DESCRIPTION)}" />`, 'meta description');
set(/<meta charset="UTF-8"\s*\/?>/i, (m) => m + tags, 'meta charset');
set(/<div id="root"><\/div>/, `<div id="root">\n      ${STATIC_BODY}\n    </div>`, '<div id="root">');
writeFileSync(page, html);

console.log(`Published the checker to ${BASE} (${URL_})`);
