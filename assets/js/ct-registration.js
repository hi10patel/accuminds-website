// UAE Corporate Tax registration deadline finder (/corporate-tax-registration-uae/).
// Deadlines from FTA Decision No. 3 of 2024 (Articles 3 to 5, in force from 1 March 2024);
// penalty and waiver from the FTA's Corporate Tax registration service card.
// Runs in the browser; nothing is sent anywhere. Indicative only: not tax advice.

const form = document.getElementById('cr-form');
const out = document.getElementById('cr-result');

const DAY = 86400000;
const EFFECTIVE = Date.UTC(2024, 2, 1);
// Art. 3.1: resident juridical persons existing before 1 March 2024, by month of licence issue (any year).
const PRE_2024 = ['2024-05-31', '2024-05-31', '2024-06-30', '2024-06-30', '2024-07-31', '2024-08-31',
  '2024-09-30', '2024-10-31', '2024-10-31', '2024-11-30', '2024-11-30', '2024-12-31'];
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

const utc = (s) => (s ? Date.parse(`${s}T00:00:00Z`) : NaN);
const fmt = (t) => { const d = new Date(t); return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`; };

// Same day n months later, or the month's last day when that day does not exist (30 Nov + 3 = 28/29 Feb).
export function addMonths(t, n) {
  const d = new Date(t);
  const y = d.getUTCFullYear(), m = d.getUTCMonth() + n;
  const last = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
  return Date.UTC(y, m, Math.min(d.getUTCDate(), last));
}

export function deadline({ who, inc, fye, year, pe }) {
  if (who === 'uae') {
    const t = utc(inc);
    if (Number.isNaN(t)) return null;
    if (t < EFFECTIVE) {
      const m = new Date(t).getUTCMonth();
      return { at: utc(PRE_2024[m]), basis: `Licence issued in ${MONTHS[m]}: the 2024 deadline for that month (Decision No. 3 of 2024, Art. 3.1).` };
    }
    return { at: addMonths(t, 3), basis: '3 months from incorporation (Decision No. 3 of 2024, Art. 3.3).' };
  }
  if (who === 'foreign') {
    const t = utc(fye);
    if (Number.isNaN(t)) return null;
    return { at: addMonths(t, 3), basis: '3 months from the end of the financial year (Decision No. 3 of 2024, Art. 3.3).' };
  }
  if (who === 'person') {
    const y = Number(String(year ?? '').replace(/\D/g, ''));
    if (!y || y < 1000) return null;
    if (y < 2024) return { early: true };
    return { at: Date.UTC(y + 1, 2, 31), basis: `31 March after the year turnover exceeded AED 1 million (Decision No. 3 of 2024, Art. 5).` };
  }
  if (who === 'pe') {
    const t = utc(pe);
    if (Number.isNaN(t)) return null;
    return t < EFFECTIVE
      ? { at: addMonths(t, 9), basis: '9 months from when the permanent establishment began, as it existed before 1 March 2024 (Art. 4.1).' }
      : { at: addMonths(t, 6), basis: '6 months from when the permanent establishment began (Art. 4.2).' };
  }
  return null;
}

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

function render() {
  const d = new FormData(form);
  const who = d.get('who') || 'uae';
  for (const f of form.querySelectorAll('[data-for]')) f.hidden = f.dataset.for !== who;
  const r = deadline({ who, inc: d.get('inc'), fye: d.get('fye'), year: d.get('year'), pe: d.get('pe') });
  out.replaceChildren();

  const head = (title, ...lines) => {
    out.append(el('p', { class: 'ct-step' }, 'Your deadline'), el('h3', { class: 'ct-question' }, title));
    for (const l of lines) out.append(el('p', { class: 'ct-hint' }, l));
  };
  const list = (items) => out.append(el('ul', { class: 'gr-notes' }, ...items.map((t) => el('li', {}, t))));

  if (!r) {
    head('Enter the date to find your deadline.', who === 'person'
      ? 'Enter the calendar year in which your business turnover first went over AED 1 million.'
      : 'Use the date on your certificate of incorporation or licence.');
    return;
  }
  if (r.early) {
    head('The registration timeline starts with 2024 turnover.', 'FTA Decision No. 3 of 2024 sets the deadline for individuals whose turnover exceeds AED 1 million in 2024 or a later year. Enter that year.');
    return;
  }

  const now = new Date();
  const today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  const days = Math.round((r.at - today) / DAY);
  out.append(el('p', { class: 'ct-step' }, 'Your deadline'), el('p', { class: 'gr-total' }, fmt(r.at)), el('p', { class: 'ct-hint' }, r.basis));

  if (days >= 0) {
    out.append(el('h3', { class: 'ct-question' }, days === 0 ? 'The deadline is today.' : `${days.toLocaleString('en-US')} day${days === 1 ? '' : 's'} left.`));
    list([
      'Register on EmaraTax before the deadline. It is free and takes about 25 minutes.',
      'Have the trade licence, incorporation documents and owner and signatory IDs ready as PDFs.',
      'Missing the deadline carries an AED 10,000 penalty.',
    ]);
  } else {
    out.append(el('h3', { class: 'ct-question' }, 'This deadline has passed. Register now.'));
    list([
      'Late registration carries an AED 10,000 penalty.',
      'The FTA waives it if you file your first tax return within 7 months of the end of your first tax period, and credits it back if you already paid.',
      'The waiver also covers businesses that have not applied yet, so register and plan the first return now.',
    ]);
  }
  out.append(el('p', { class: 'ct-note' }, 'Estimate based on FTA Decision No. 3 of 2024 and the FTA’s registration service. It is not tax advice.'));
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
