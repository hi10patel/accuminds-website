// UAE Corporate Tax return deadline finder (/corporate-tax-return-uae/).
// Federal Decree-Law No. 47 of 2022: Article 53 (return no later than nine months from the end of the
// tax period) and Article 48 (payment within the same nine months).
// Cabinet Decision No. 75 of 2023 as amended: row 7 (late return: AED 500 for each month or part of a
// month for the first twelve months, AED 1,000 from the thirteenth), row 8 (late payment: a monthly
// penalty of 14% per annum on the unpaid tax) and Article 3 (the monthly date in a shorter month).
// Runs in the browser; nothing is sent anywhere. Indicative only: not tax advice.

const form = document.getElementById('cf-form');
const out = document.getElementById('cf-result');

const DAY = 86400000;
const AED = (n) => `AED ${n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const fmt = (d) => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
const num = (v) => {
  const n = Number(String(v ?? '').replace(/[^0-9.]/g, ''));
  return Number.isFinite(n) ? n : 0;
};
const lastDay = (y, m) => new Date(Date.UTC(y, m + 1, 0)).getUTCDate();

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

// n months after a date. A month-end stays a month-end (31 December + 9 months = 30 September);
// any other day keeps its number, or the month's last day if the month is shorter.
export function addMonths(date, n, stickToMonthEnd = true) {
  const y = date.getUTCFullYear();
  const m = date.getUTCMonth() + n;
  const d = date.getUTCDate();
  const end = lastDay(y, m);
  const isMonthEnd = d === lastDay(y, date.getUTCMonth());
  return new Date(Date.UTC(y, m, stickToMonthEnd && isMonthEnd ? end : Math.min(d, end)));
}

// Return and payment are both due nine months after the tax period ends.
export const dueDate = (periodEnd) => addMonths(periodEnd, 9);

// Months, or parts of a month, of lateness: the penalty is imposed on the day after the deadline
// and on the same date each month after that.
export function monthsLate(due, today) {
  if (today <= due) return 0;
  const first = new Date(due.getTime() + DAY);
  let n = 0;
  while (addMonths(first, n, false) <= today) n += 1;
  return n;
}

export const lateFilingPenalty = (months) => Math.min(months, 12) * 500 + Math.max(months - 12, 0) * 1000;
// 14% a year, charged for each month or part of a month, on the tax still unpaid.
export const latePaymentPenalty = (unpaid, months) => Math.round(unpaid * (0.14 / 12) * months * 100) / 100;

function render() {
  const d = new FormData(form);
  out.replaceChildren();
  const end = d.get('end') ? new Date(`${d.get('end')}T00:00:00Z`) : null;
  if (!end || Number.isNaN(end.getTime())) {
    out.append(
      el('p', { class: 'ct-step' }, 'Your result'),
      el('h3', { class: 'ct-question' }, 'Enter the last day of your financial year.'),
      el('p', { class: 'ct-hint' }, 'For most companies that is 31 December. Your tax period is the financial year you prepare accounts for (Article 57).'));
    return;
  }

  const now = new Date();
  const today = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
  const due = dueDate(end);
  const late = monthsLate(due, today);
  const daysLeft = Math.round((due - today) / DAY);
  const unpaid = num(d.get('unpaid'));

  out.append(
    el('p', { class: 'ct-step' }, 'Return and payment due'),
    el('p', { class: 'gr-total' }, fmt(due)),
    el('p', { class: 'ct-hint' }, late
      ? `That date has passed. Counted to today, the return is ${late} month${late === 1 ? '' : 's'} late (a part month counts as a month).`
      : daysLeft === 0 ? 'That is today.' : `${daysLeft.toLocaleString('en-US')} day${daysLeft === 1 ? '' : 's'} from today.`),
  );

  const rows = [
    ['Tax period ends', 'The date you entered', fmt(end)],
    ['Return due', 'Nine months after the period ends (Article 53)', fmt(due)],
    ['Tax due', 'The same date (Article 48)', fmt(due)],
  ];
  if (late) {
    rows.push(['Late filing penalty so far', `If the return is still not filed: ${Math.min(late, 12)} × AED 500${late > 12 ? ` + ${late - 12} × AED 1,000` : ''}`, AED(lateFilingPenalty(late))]);
    if (unpaid) rows.push(['Late payment penalty so far', `${AED(unpaid)} × 14% ÷ 12 × ${late} month${late === 1 ? '' : 's'}`, AED(latePaymentPenalty(unpaid, late))]);
  }
  out.append(el('dl', { class: 'gr-rows gr-rows--sum' },
    ...rows.map(([t, how, v]) => el('div', {}, el('dt', {}, t, el('small', {}, how)), el('dd', {}, v)))));

  const notes = late
    ? [
      'File now: the late filing penalty is AED 500 for each month or part of a month for the first twelve months, then AED 1,000 a month. It is added on the day after the deadline and on the same date each month.',
      'Unpaid tax carries a monthly penalty of 14% a year from the day after the due date. If the return was filed and the tax paid on time, no penalty applies.',
    ]
    : [
      'A return is due even if there is no tax to pay, and also if you elect Small Business Relief.',
      'Filing late costs AED 500 for each month or part of a month for the first twelve months, then AED 1,000 a month. Unpaid tax carries a monthly penalty of 14% a year.',
    ];
  notes.push('The FTA can set another date in specific cases (Article 53). If the date falls on a weekend or public holiday, do not count on extra time: file before it.');
  out.append(el('ul', { class: 'gr-notes' }, ...notes.map((n) => el('li', {}, n))));
  out.append(el('p', { class: 'ct-note' }, 'An estimate only, based on the dates and figures you entered. It is not tax advice.'));
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
