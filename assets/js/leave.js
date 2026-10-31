// UAE annual leave salary calculator (/leave-salary-calculator/).
// Federal Decree-Law No. 33 of 2021, Article 29 (entitlement, full pay during leave), and
// Cabinet Resolution No. 1 of 2022, Article 19(2) (unused leave paid on basic salary when service ends).
// Runs in the browser; nothing is sent anywhere. Indicative only: not legal advice.

const form = document.getElementById('lv-form');
const out = document.getElementById('lv-result');

const DAY = 86400000;
const AED = (n) => `AED ${n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const round2 = (n) => Math.round(n * 100) / 100;
const fmtDays = (n) => `${Number(n.toFixed(2)).toLocaleString('en-US')} day${n === 1 ? '' : 's'}`;
const num = (v) => {
  const n = Number(String(v ?? '').replace(/[^0-9.]/g, ''));
  return Number.isFinite(n) ? n : 0;
};
const has = (v) => String(v ?? '').trim() !== '';

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

const plusMonths = (t, n) => {
  const d = new Date(t);
  const y = d.getUTCFullYear(), m = d.getUTCMonth() + n;
  return Date.UTC(y, m, Math.min(d.getUTCDate(), new Date(Date.UTC(y, m + 1, 0)).getUTCDate()));
};

// Article 29(1): 30 days a year after one year (part of the last year pro rata, 29(1)(c));
// 2 days for each month when service is more than six months and less than one year.
export function earned(start, end) {
  const endEx = end + DAY; // both dates count as worked
  let years = 0;
  while (plusMonths(start, 12 * (years + 1)) <= endEx) years += 1;
  if (years >= 1) {
    const rest = Math.round((endEx - plusMonths(start, 12 * years)) / DAY);
    return { days: 30 * (years + rest / 365), years: years + rest / 365, basis: 'year' };
  }
  let months = 0;
  while (plusMonths(start, months + 1) <= endEx) months += 1;
  if (endEx > plusMonths(start, 6)) return { days: 2 * months, months, basis: 'month' };
  return { days: 0, months, basis: 'none' };
}

function render() {
  const d = new FormData(form);
  const mode = d.get('mode') || 'exit';
  for (const f of form.querySelectorAll('[data-for]')) f.hidden = f.dataset.for !== mode;
  out.replaceChildren();

  const basic = num(d.get('basic'));
  const head = (title, ...lines) => {
    out.append(el('p', { class: 'ct-step' }, 'Your result'), el('h3', { class: 'ct-question' }, title));
    for (const l of lines) out.append(el('p', { class: 'ct-hint' }, l));
  };
  const rowsOut = (rows) => out.append(el('dl', { class: 'gr-rows' }, ...rows.map(([t, v]) => el('div', {}, el('dt', {}, t), el('dd', {}, v)))));
  const notes = (items) => out.append(el('ul', { class: 'gr-notes' }, ...items.map((t) => el('li', {}, t))));
  const disclaimer = () => out.append(el('p', { class: 'ct-note' }, 'Estimate only, based on your answers and the federal Labour Law. It is not legal advice.'));

  if (mode === 'take') {
    const total = num(d.get('total'));
    const days = num(d.get('days'));
    if (!(total || basic) || !days) {
      head('Enter your salary and the days of leave.', 'You are paid your full wage while on annual leave: basic salary plus allowances (Article 29).');
      return;
    }
    const monthly = total || basic;
    const pay = (monthly / 30) * days;
    out.append(el('p', { class: 'ct-step' }, 'Your leave salary'), el('p', { class: 'gr-total' }, AED(round2(pay))));
    out.append(el('p', { class: 'ct-hint' }, `For ${fmtDays(days)} of annual leave at full pay.`));
    rowsOut([['Daily wage', `${AED(monthly)} ÷ 30 = ${AED(round2(monthly / 30))}`], ['Leave days', `${fmtDays(days)} × ${AED(round2(monthly / 30))}`]]);
    notes([
      ...(total ? [] : ['You entered basic salary only. Full pay during leave includes your cash allowances, so add your total salary for the right figure.']),
      `Employers who use (monthly salary × 12) ÷ 365 per day would pay ${AED(round2((monthly * 12 / 365) * days))}.`,
      'On a monthly salary, this is your usual full pay for the leave period.',
    ]);
    disclaimer();
    return;
  }

  const start = d.get('start') ? Date.parse(`${d.get('start')}T00:00:00Z`) : NaN;
  const end = d.get('end') ? Date.parse(`${d.get('end')}T00:00:00Z`) : NaN;
  const known = has(d.get('balance'));
  if (!basic || (!known && (Number.isNaN(start) || Number.isNaN(end)))) {
    head('Enter your basic salary and your dates.', 'Unused leave is paid out on your basic salary, without allowances (Executive Regulation, Article 19(2)). Or enter your unused balance if you know it.');
    return;
  }
  if (!known && end < start) {
    head('The last working day is before the start date.', 'Check the two dates.');
    return;
  }

  const daily = basic / 30;
  let balance;
  const rows = [['Daily basic wage', `${AED(basic)} ÷ 30 = ${AED(round2(daily))}`]];
  if (known) {
    balance = num(d.get('balance'));
    rows.push(['Unused leave (your balance)', fmtDays(balance)]);
  } else {
    const e = earned(start, end);
    const taken = num(d.get('taken'));
    if (e.basis === 'none') {
      head('No annual leave earned yet.', `Service counted: ${e.months} complete month${e.months === 1 ? '' : 's'}. Leave starts at 2 days a month once service is more than six months (Article 29(1)(b)).`);
      disclaimer();
      return;
    }
    balance = Math.max(e.days - taken, 0);
    rows.push(e.basis === 'year'
      ? ['Leave earned', `${e.years.toFixed(2)} years × 30 days = ${fmtDays(round2(e.days))}`]
      : ['Leave earned', `${e.months} months × 2 days = ${fmtDays(e.days)}`]);
    rows.push(['Already taken', fmtDays(taken)], ['Unused leave', fmtDays(round2(balance))]);
  }
  const pay = balance * daily;
  out.append(el('p', { class: 'ct-step' }, 'Unused leave pay'), el('p', { class: 'gr-total' }, AED(round2(pay))));
  out.append(el('p', { class: 'ct-hint' }, `For ${fmtDays(round2(balance))} of unused annual leave, on a basic salary of ${AED(basic)} a month.`));
  rowsOut(rows);
  notes([
    `The law does not set the daily rate. This uses basic ÷ 30; employers who use (basic × 12) ÷ 365 would pay ${AED(round2(balance * basic * 12 / 365))}.`,
    'It is paid with your final dues, together with your gratuity if you have completed a year.',
    'Leave already carried forward, or paid in cash by agreement, reduces the balance: enter your actual balance if your payslip or HR system shows it.',
  ]);
  disclaimer();
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
