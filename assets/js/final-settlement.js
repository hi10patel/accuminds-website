// UAE final settlement calculator (/final-settlement-calculator/).
// Federal Decree-Law No. 33 of 2021: Article 43 (notice and the notice allowance), Article 51 (gratuity),
// Article 53 (final dues within 14 days); Cabinet Resolution No. 1 of 2022: Article 19(2) (unused leave
// on basic salary) and Article 29 (deductions from end-of-service pay).
// Runs in the browser; nothing is sent anywhere. Indicative only: not legal advice.

import { gratuity, serviceYears } from './gratuity.js';
import { earned } from './leave.js';

const form = document.getElementById('fs-form');
const out = document.getElementById('fs-result');

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

function render() {
  const d = new FormData(form);
  const who = d.get('who') || 'foreign';
  const notice = d.get('notice') || 'worked';
  for (const f of form.querySelectorAll('[data-for]')) f.hidden = !f.dataset.for.split(' ').includes(notice);
  out.replaceChildren();

  const head = (title, ...lines) => {
    out.append(el('p', { class: 'ct-step' }, 'Your result'), el('h3', { class: 'ct-question' }, title));
    for (const l of lines) out.append(el('p', { class: 'ct-hint' }, l));
  };

  const basic = num(d.get('basic'));
  const total = Math.max(num(d.get('total')), basic);
  const start = d.get('start') ? new Date(`${d.get('start')}T00:00:00Z`) : null;
  const end = d.get('end') ? new Date(`${d.get('end')}T00:00:00Z`) : null;
  if (!basic || !start || !end) {
    head('Enter your salary and your service dates.',
      'Basic salary is the contract wage without allowances: gratuity and unused leave are paid on it. Total salary, with allowances, is used for unpaid salary and notice pay.');
    return;
  }
  if (end < start) {
    head('The last working day is before the start date.', 'Check the two dates.');
    return;
  }

  const rows = [];
  const notes = [];
  let net = 0;
  const add = (label, amount, how) => {
    net += amount;
    rows.push([label, `${amount < 0 ? '− ' : ''}${AED(round2(Math.abs(amount)))}`, how]);
  };

  // Salary still owed for days worked (Article 53), at the full wage.
  const salaryDays = num(d.get('salarydays'));
  if (salaryDays) add('Unpaid salary', (total / 30) * salaryDays, `${fmtDays(salaryDays)} × ${AED(round2(total / 30))} (total salary ÷ 30)`);

  // Gratuity (Article 51): foreign full-time workers with one year or more of continuous service.
  const unpaid = num(d.get('unpaid'));
  const { years } = serviceYears(start, end, unpaid);
  if (who === 'national') {
    notes.push('No gratuity is shown: a UAE national’s end-of-service entitlement follows the pensions and social security law instead (Article 51(1)).');
  } else if (years < 1) {
    notes.push('No gratuity: it starts once one year of continuous service is completed (Article 51(2)).');
  } else {
    const g = gratuity({ basic, years });
    add('Gratuity', g.total, `${years.toFixed(2)} years of service on basic salary${g.capped ? ', capped at two years’ wage' : ''}`);
  }

  // Unused annual leave, paid on basic salary when service ends (Executive Regulation, Article 19(2)).
  // Counted only once the leave taken or the balance is entered, so a blank answer doesn't count every day as unused.
  let balance = 0;
  if (has(d.get('balance'))) {
    balance = num(d.get('balance'));
  } else if (has(d.get('taken'))) {
    const e = earned(start.getTime(), end.getTime());
    balance = Math.max(e.days - num(d.get('taken')), 0);
  } else {
    notes.push('Unused leave is not included yet: enter the leave days you have taken, or your unused balance.');
  }
  if (balance) add('Unused annual leave', balance * (basic / 30), `${fmtDays(round2(balance))} × ${AED(round2(basic / 30))} (basic salary ÷ 30)`);

  // Notice allowance (Article 43(3) and (4)): the wage for the notice period, or the part not served.
  if (notice !== 'worked') {
    const period = num(d.get('noticedays'));
    const left = Math.max(period - num(d.get('served')), 0);
    if (!period) {
      notes.push('Enter the notice period in your contract (30 to 90 days) to include notice pay.');
    } else if (left) {
      const amount = (total / 30) * left;
      if (notice === 'employer') add('Notice pay', amount, `${fmtDays(left)} of notice not served × ${AED(round2(total / 30))}`);
      else add('Notice you did not serve', -amount, `${fmtDays(left)} × ${AED(round2(total / 30))}, owed to the employer (Article 43(3))`);
    }
  }

  const other = num(d.get('other'));
  if (other) add('Other amounts due to you', other, 'From your contract, such as overtime, a bonus or an air ticket');
  const deduct = num(d.get('deduct'));
  if (deduct) add('Deductions', -deduct, 'Loans, advances or overpayments you owe');

  if (!rows.length) {
    head('Nothing to pay on these answers.', 'Add any unpaid salary days, or check the dates and leave figures.');
    if (notes.length) out.append(el('ul', { class: 'gr-notes' }, ...notes.map((t) => el('li', {}, t))));
    return;
  }

  out.append(
    el('p', { class: 'ct-step' }, net < 0 ? 'You owe your employer' : 'Your estimated final settlement'),
    el('p', { class: 'gr-total' }, AED(round2(Math.abs(net)))),
    el('p', { class: 'ct-hint' }, `For ${years.toFixed(2)} years of service, on a basic salary of ${AED(basic)} and a total salary of ${AED(total)} a month.`),
    el('dl', { class: 'gr-rows gr-rows--sum' }, ...rows.map(([t, v, how]) => el('div', {}, el('dt', {}, t, el('small', {}, how)), el('dd', {}, v)))),
  );
  notes.push(
    'Your employer must pay your wages and all final dues within 14 days of the contract ending (Article 53).',
    'The law does not set the daily rate. This uses monthly salary ÷ 30, the common practice; employers who use (salary × 12) ÷ 365 would pay slightly less.',
    'Deductions are limited to amounts such as loans, overpayments and court-ordered debts (Executive Regulation, Article 29).',
  );
  if (notice === 'employer') notes.push('If you and your employer agreed to waive or shorten the notice, you keep your rights for the notice period in your contract (Article 43(2)).');
  out.append(el('ul', { class: 'gr-notes' }, ...notes.map((t) => el('li', {}, t))));
  out.append(el('p', { class: 'ct-note' }, 'Estimate only, based on your answers and the federal Labour Law. It is not legal advice.'));
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
