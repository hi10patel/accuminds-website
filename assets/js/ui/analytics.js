// Visit and enquiry counting with GoatCounter (https://www.goatcounter.com).
//
// No cookies and no personal data: each count is one request holding the page
// path, its title, the referring site, the screen width and a campaign tag if
// the link had one. Nothing a visitor types into a calculator or the contact
// form is ever sent.
//
// This talks to GoatCounter's /count endpoint directly (the same request its
// own count.js makes), so no third-party script runs on the site.
//
// What is counted:
//   page views                 "/gratuity-calculator/"
//   WhatsApp clicks            "whatsapp /gratuity-calculator/"
//   email and phone clicks     "email /…", "phone /…"
//   "Book a consultation"      "consultation /…"        (links to #contact)
//   contact form sent          "form-sent /…"           (from contact.js)
//   file downloads             "download accuminds-monthly-mis-template.xlsx"
//   a tool being used          "tool-used /…"           (first entry in a calculator, once per visit to the page)
//
// Skip your own visits: open any page with #toggle-goatcounter on the end of
// the address, once per browser. Open it again to switch counting back on.
// Check what would be sent without sending it: localStorage.gcdebug = 't'.

// The site code chosen at sign-up: https://CODE.goatcounter.com. Empty = counting off.
const CODE = 'accuminds';
const ENDPOINT = CODE ? `https://${CODE}.goatcounter.com/count` : '';

const store = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch { /* storage unavailable */ } },
  remove(key) { try { localStorage.removeItem(key); } catch { /* storage unavailable */ } },
};

// Requests that should not be counted (same rules as GoatCounter's count.js).
function skipReason() {
  if (document.visibilityState === 'prerender') return 'prerender';
  if (window.location !== window.parent.location) return 'frame'; // the embedded calculator on other sites
  if (/(localhost$|^127\.|^10\.|^172\.(1[6-9]|2[0-9]|3[0-1])\.|^192\.168\.|^0\.0\.0\.0$)/.test(location.hostname)) return 'local';
  if (location.protocol === 'file:') return 'file';
  if (store.get('skipgc') === 't') return 'switched off in this browser';
  return '';
}

// Only campaign tags are passed on, never the rest of the query string.
function campaign() {
  const keep = new URLSearchParams();
  new URLSearchParams(location.search).forEach((value, key) => {
    if (/^(utm_(source|medium|campaign)|ref)$/i.test(key)) keep.set(key, value);
  });
  const q = keep.toString();
  return q ? `?${q}` : '';
}

function count({ path, title, event = false }) {
  const debug = store.get('gcdebug') === 't';
  if (!debug && (!ENDPOINT || skipReason())) return;
  const data = {
    p: path,
    t: title,
    r: event ? '' : document.referrer,
    e: event ? 'true' : '',
    s: window.screen.width,
    b: navigator.webdriver ? 153 : 0,
    q: campaign(),
    rnd: Math.random().toString(36).slice(2, 7),
  };
  const query = Object.entries(data)
    .filter(([, v]) => v !== '' && v !== null && v !== undefined)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
  const url = `${ENDPOINT || 'https://CODE.goatcounter.com/count'}?${query}`;
  if (debug) { console.info('[count]', event ? 'event' : 'view', path, url); return; }
  if (!navigator.sendBeacon?.(url)) new Image().src = url;
}

const page = () => location.pathname;
const countEvent = (name, detail = page()) => count({ path: `${name} ${detail}`, title: `${name}: ${detail}`, event: true });

function eventFor(link) {
  const href = link.getAttribute('href') || '';
  if (/^https:\/\/wa\.me\//.test(href)) return ['whatsapp'];
  if (href.startsWith('mailto:')) return ['email'];
  if (href.startsWith('tel:')) return ['phone'];
  if (link.hasAttribute('download')) return ['download', href.split('/').pop()];
  if (/#contact$/.test(href)) return ['consultation'];
  return null;
}

export function initAnalytics() {
  if (location.hash === '#toggle-goatcounter') {
    const off = store.get('skipgc') === 't';
    if (off) store.remove('skipgc'); else store.set('skipgc', 't');
    window.alert(off ? 'Visits from this browser are counted again.' : 'Visits from this browser are no longer counted.');
  }

  // Page view: once the page is actually on screen (not a background tab that is never looked at).
  const view = () => count({ path: page(), title: document.title });
  if (document.visibilityState === 'visible') view();
  else {
    const onVisible = () => {
      if (document.visibilityState !== 'visible') return;
      document.removeEventListener('visibilitychange', onVisible);
      view();
    };
    document.addEventListener('visibilitychange', onVisible);
  }

  // Enquiry clicks and downloads. auxclick = middle click (opens in a new tab).
  const onClick = (e) => {
    const link = e.target.closest?.('a[href]');
    const found = link && eventFor(link);
    if (found) countEvent(...found);
  };
  document.addEventListener('click', onClick);
  document.addEventListener('auxclick', onClick);

  // A sent contact form (contact.js announces it; the message itself never comes here).
  document.addEventListener('am:lead', (e) => countEvent(e.detail?.kind || 'form-sent'));

  // First entry in a calculator or check, once per page load. Only the fact, not what was entered.
  const onUse = (e) => {
    if (!e.target.closest?.('main form:not(#contact-form)')) return;
    document.removeEventListener('input', onUse);
    countEvent('tool-used');
  };
  document.addEventListener('input', onUse);
}
