// UAE end-of-service gratuity calculator (/gratuity-calculator/).
// Federal Decree-Law No. 33 of 2021, Article 51, and Cabinet Resolution No. 1 of 2022, Article 30.
// Runs in the browser; nothing is sent anywhere. Indicative only: not legal advice.

const form = document.getElementById('gr-form');
const out = document.getElementById('gr-result');

const DAY = 86400000;
const AED = (n) => `AED ${n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const num = (v) => {
  const n = Number(String(v ?? '').replace(/[^0-9.]/g, ''));
  return Number.isFinite(n) ? n : 0;
};
const round2 = (n) => Math.round(n * 100) / 100;

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

// Article 51: 21 days' basic wage for each of the first 5 years, 30 days for each year after,
// fractions of a year pro rata once one year is completed, capped at two years' wage.
export function gratuity({ basic, years, daily = basic / 30, share = 1 }) {
  const first = Math.min(years, 5) * 21 * daily;
  const after = Math.max(years - 5, 0) * 30 * daily;
  const uncapped = first + after;
  const cap = 24 * basic; // two years' wage, taken here as two years' basic wage (the stricter reading)
  const full = Math.min(uncapped, cap);
  return { daily, first, after, uncapped, cap, capped: uncapped > cap, full, total: full * share };
}

function render() {
  const d = new FormData(form);
  const who = d.get('who') || 'foreign';
  const kind = d.get('kind') || 'full';
  const basic = num(d.get('basic'));
  const start = d.get('start') ? new Date(`${d.get('start')}T00:00:00Z`) : null;
  const end = d.get('end') ? new Date(`${d.get('end')}T00:00:00Z`) : null;
  const unpaid = num(d.get('unpaid'));
  const partHours = num(d.get('parthours'));
  const fullHours = num(d.get('fullhours')) || 48;
  form.querySelector('#gr-part').hidden = kind !== 'part';
  out.replaceChildren();

  const head = (title, ...lines) => {
    out.append(el('p', { class: 'ct-step' }, 'Your result'), el('h3', { class: 'ct-question' }, title));
    for (const l of lines) out.append(el('p', { class: 'ct-hint' }, l));
  };

  if (who === 'national') {
    head('UAE nationals are covered by the pension law instead.',
      'A national worker’s end-of-service entitlement follows the legislation on pensions and social security, not this gratuity formula (Article 51(1)).');
    return;
  }
  if (kind === 'temp') {
    head('No gratuity under a temporary work model.', 'End-of-service pay does not apply to the temporary work model (Cabinet Resolution No. 1 of 2022, Article 30(2)).');
    return;
  }
  if (!basic || !start || !end) {
    head('Enter your basic salary and your service dates.',
      'Use the monthly basic salary from your contract, without housing, transport or other allowances: gratuity is calculated on the last basic wage (Article 51(5)).');
    return;
  }
  if (kind === 'part' && !partHours) {
    head('Enter your contracted hours per week.',
      'Part-time gratuity is a share of the full-time amount: your contracted hours divided by full-time hours (Cabinet Resolution No. 1 of 2022, Article 30).');
    return;
  }
  if (end < start) {
    head('The last working day is before the start date.', 'Check the two dates.');
    return;
  }

  // Whole years by anniversary, then the remaining days pro rata (Article 51(3)); both dates count as worked.
  const endEx = new Date(end.getTime() + DAY);
  const anniversary = (n) => new Date(Date.UTC(start.getUTCFullYear() + n, start.getUTCMonth(), start.getUTCDate()));
  let whole = 0;
  while (anniversary(whole + 1) <= endEx) whole += 1;
  const days = Math.round((endEx - start) / DAY) - unpaid;
  const years = whole + (Math.round((endEx - anniversary(whole)) / DAY) - unpaid) / 365;
  if (years < 1) {
    head('No gratuity yet: less than one year of continuous service.',
      `Service counted: ${Math.max(days, 0).toLocaleString('en-US')} days. Gratuity starts once one year of continuous service is completed (Article 51(2)); unpaid absence days do not count (Article 51(4)).`);
    return;
  }

  const share = kind === 'part' && partHours > 0 ? Math.min(partHours / fullHours, 1) : 1;
  const g = gratuity({ basic, years, share });
  const alt = gratuity({ basic, years, daily: (basic * 12) / 365, share });

  out.append(
    el('p', { class: 'ct-step' }, 'Your estimated gratuity'),
    el('p', { class: 'gr-total' }, AED(round2(g.total))),
    el('p', { class: 'ct-hint' }, `For ${years.toFixed(2)} years of service (${days.toLocaleString('en-US')} days${unpaid ? `, after ${unpaid.toLocaleString('en-US')} unpaid days` : ''}) on a basic salary of ${AED(basic)} a month.`),
  );

  const rows = [
    ['Daily basic wage', `${AED(basic)} ÷ 30 = ${AED(round2(g.daily))}`],
    ['First 5 years', `${Math.min(years, 5).toFixed(2)} years × 21 days = ${AED(round2(g.first))}`],
  ];
  if (years > 5) rows.push(['After 5 years', `${(years - 5).toFixed(2)} years × 30 days = ${AED(round2(g.after))}`]);
  if (g.capped) rows.push(['Cap: two years’ wage', `Reduced from ${AED(round2(g.uncapped))} to ${AED(round2(g.cap))} (Article 51(6))`]);
  if (share < 1) rows.push(['Part-time share', `${partHours} ÷ ${fullHours} hours = ${(share * 100).toFixed(1)}% of ${AED(round2(g.full))}`]);
  out.append(el('dl', { class: 'gr-rows' }, ...rows.map(([t, v]) => el('div', {}, el('dt', {}, t), el('dd', {}, v)))));

  const notes = [
    `The law sets the rate in days of wage but not how a day is worked out. This estimate uses monthly basic ÷ 30, the common practice; employers who use (monthly basic × 12) ÷ 365 would pay ${AED(round2(alt.total))}.`,
    'Resigning does not reduce gratuity under the current law. Your employer must pay it, with your other final dues, within 14 days of the contract ending (Article 53).',
    'The employer may deduct amounts you owe, such as loans or overpayments, under Article 29 of Cabinet Resolution No. 1 of 2022.',
  ];
  if (g.capped) notes.push('The law caps gratuity at two years’ wage. This estimate applies the cap to basic wage, the stricter reading; if allowances count towards the cap, the limit is higher.');
  out.append(el('ul', { class: 'gr-notes' }, ...notes.map((n) => el('li', {}, n))));
  out.append(el('p', { class: 'ct-note' }, 'Estimate only, based on your answers and the federal Labour Law. It is not legal advice.'));
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
