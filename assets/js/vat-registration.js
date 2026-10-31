// UAE VAT registration check (/vat-registration-uae/).
// Thresholds from the FTA's "Registration for VAT" topic and VAT registration service card;
// late registration penalty from Cabinet Decision No. 40 of 2017 as amended (FTA publication).
// Runs in the browser; nothing is sent anywhere. Indicative only: not tax advice.

const form = document.getElementById('vr-form');
const out = document.getElementById('vr-result');

const MANDATORY = 375000;
const VOLUNTARY = 187500;
const PENALTY = 10000;

const AED = (n) => `AED ${Math.round(n).toLocaleString('en-US')}`;
const num = (v) => {
  const n = Number(String(v ?? '').replace(/[^0-9.]/g, ''));
  return Number.isFinite(n) ? n : 0;
};

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

const below = (gap, which) => {
  const limit = which === 'mandatory' ? 'AED 375,000' : 'AED 187,500';
  return gap > 0
    ? `You are ${AED(gap)} below the ${which} threshold of ${limit}.`
    : `You are exactly at the ${which} threshold of ${limit}: any further taxable ${which === 'mandatory' ? 'sale' : 'sale or expense'} takes you over it.`;
};

// "Exceeds" in the law: strictly more than the threshold.
export function assess({ where = 'uae', past = 0, next = 0, exp = 0, expnext = 0 }) {
  if (where === 'foreign') return { kind: 'foreign' };
  if (past > MANDATORY || next > MANDATORY) return { kind: 'must', byPast: past > MANDATORY, byNext: next > MANDATORY };
  const bySupplies = past > VOLUNTARY || next > VOLUNTARY;
  const byExpenses = exp > VOLUNTARY || expnext > VOLUNTARY;
  if (bySupplies || byExpenses) return { kind: 'may', bySupplies, byExpenses, gap: MANDATORY - Math.max(past, next) };
  return { kind: 'no', gap: MANDATORY - Math.max(past, next), vgap: VOLUNTARY - Math.max(past, next, exp, expnext) };
}

function render() {
  const d = new FormData(form);
  const where = d.get('where') || 'uae';
  form.querySelector('#vr-amounts').hidden = where === 'foreign';
  const input = { where, past: num(d.get('past')), next: num(d.get('next')), exp: num(d.get('exp')), expnext: num(d.get('expnext')) };
  const r = assess(input);
  out.replaceChildren();

  const head = (step, title, ...lines) => {
    out.append(el('p', { class: 'ct-step' }, step), el('h3', { class: 'ct-question' }, title));
    for (const l of lines) out.append(el('p', { class: 'ct-hint' }, l));
  };
  const list = (items) => out.append(el('ul', { class: 'gr-notes' }, ...items.map((t) => el('li', {}, t))));

  if (r.kind === 'foreign') {
    head('Your result', 'No threshold applies to non-resident businesses.',
      'A business established outside the UAE must register if it makes taxable supplies in the UAE, whatever their value, unless someone else in the UAE is responsible for the VAT on them.');
  } else if (!input.past && !input.next && !input.exp && !input.expnext) {
    head('Your result', 'Enter your taxable supplies and imports.',
      'Add up sales charged at 5% or 0% and imports over the last 12 months. Leave out exempt sales.');
    return;
  } else if (r.kind === 'must') {
    const why = r.byPast ? 'exceeded AED 375,000 over the last 12 months' : 'are expected to exceed AED 375,000 in the next 30 days';
    head('Your result', 'You must register for VAT.',
      `Your taxable supplies and imports ${why}.`);
    list([
      'Apply on EmaraTax within 30 days of becoming required to register.',
      `Missing the deadline carries a late registration penalty of ${AED(PENALTY)}.`,
      'Have the documents below ready, including a signed turnover declaration.',
    ]);
  } else if (r.kind === 'may') {
    const basis = r.bySupplies && r.byExpenses ? 'taxable supplies, imports and expenses' : r.bySupplies ? 'taxable supplies and imports' : 'taxable expenses';
    head('Your result', 'You can choose to register voluntarily.',
      `Your ${basis} exceed AED 187,500, but supplies and imports are not over AED 375,000.`);
    list([
      `${below(r.gap, 'mandatory')} Check the 12-month total every month: you must apply within 30 days of crossing it.`,
      'Registering lets you recover VAT on business costs, but you then charge VAT, keep VAT records and file returns.',
      ...(r.byExpenses && !r.bySupplies ? ['To register on expenses, the FTA asks for at least five VAT invoices as evidence.'] : []),
    ]);
  } else {
    head('Your result', 'You do not need to register yet.',
      `Your figures do not exceed either threshold. ${below(r.gap, 'mandatory')} ${below(r.vgap, 'voluntary')}`);
    list([
      'Recalculate the last 12 months every month, and check expected sales for the next 30 days.',
      'Apply within 30 days of crossing AED 375,000 to avoid the late registration penalty.',
    ]);
  }
  out.append(el('p', { class: 'ct-note' }, 'Estimate based on your figures and the FTA’s published thresholds. It is not tax advice.'));
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
