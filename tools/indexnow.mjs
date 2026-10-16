// Tells IndexNow search engines (Bing, Yandex, Seznam, Naver …) which pages
// have been added or changed, so they re-crawl them straight away.
//
//   npm run indexnow                    every URL in sitemap.xml
//   npm run indexnow -- <url> [<url>]   only the pages you changed
//
// Run it after a change is LIVE (merged and published), not before.
// The key is public by design: the key file at the site root proves the site
// is ours. It is not a secret and is not tied to any account login.
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const HOST = 'www.accumindsconsulting.ae';
const KEY = '0fb1f254e2294a41940ad768991c5054';
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;
const ENDPOINT = 'https://api.indexnow.org/indexnow';

const RESPONSES = {
  200: 'OK: URLs submitted.',
  202: 'Accepted: URLs received; the key is still being validated.',
  400: 'Bad request: the submission was malformed.',
  403: 'Forbidden: the key file was not found or does not match.',
  422: 'Unprocessable: a URL does not belong to this host, or the key does not match.',
  429: 'Too many requests: wait before submitting again.',
};

async function sitemapUrls() {
  const xml = await readFile(fileURLToPath(new URL('../sitemap.xml', import.meta.url)), 'utf8');
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].trim());
}

const urls = process.argv.length > 2 ? process.argv.slice(2) : await sitemapUrls();
const foreign = urls.filter((u) => new URL(u).host !== HOST);
if (foreign.length) {
  console.error(`Not on ${HOST}:`, foreign.join(', '));
  process.exit(1);
}

// The search engines fetch this file to verify ownership, so check it first.
const live = await fetch(KEY_LOCATION).then((r) => (r.ok ? r.text() : '')).catch(() => '');
if (live.trim() !== KEY) {
  console.error(`Key file not live at ${KEY_LOCATION}. Merge and publish the site first.`);
  process.exit(1);
}

const res = await fetch(ENDPOINT, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: KEY_LOCATION, urlList: urls }),
});
console.log(`${res.status} ${RESPONSES[res.status] ?? res.statusText}`);
console.log(`${urls.length} URL(s):\n  ${urls.join('\n  ')}`);
process.exitCode = res.status === 200 || res.status === 202 ? 0 : 1;
