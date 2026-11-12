// UAE VAT calculator (/vat-calculator-uae/).
// Federal Decree-Law No. 8 of 2017: Article 3 (standard rate of 5%), Article 34 (value of a supply is the
// consideration less the tax), Article 53 (payable tax = output tax less recoverable input tax);
// Cabinet Resolution No. 52 of 2017, Article 61 (tax may be rounded to the nearest fils).
// Runs in the browser; nothing is sent anywhere. Indicative only: not tax advice.

export const RATE = 0.05;

const AED = (n) => `AED ${n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const round2 = (n) => Math.round((n + Number.EPSILON) * 100) / 100;
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

// Add VAT to a price before VAT. The tax is rounded to the nearest fils.
export function addVat(net) {
  const vat = round2(net * RATE);
  return { net, vat, total: round2(net + vat) };
}

// Take VAT out of a price that includes it: the tax is 5/105 of the total.
export function removeVat(total) {
  const vat = round2((total * RATE) / (1 + RATE));
  return { net: round2(total - vat), vat, total };
}

// VAT for a tax period: output tax on sales less recoverable input tax on purchases.
export function period(sales, purchases) {
  const output = round2(sales * RATE);
  const input = round2(purchases * RATE);
  return { output, input, due: round2(output - input) };
}

const rowsList = (rows) => el('dl', { class: 'gr-rows gr-rows--sum' },
  ...rows.map(([t, how, v]) => el('div', {}, el('dt', {}, t, el('small', {}, how)), el('dd', {}, v))));
const notesList = (notes) => el('ul', { class: 'gr-notes' }, ...notes.map((n) => el('li', {}, n)));
const prompt = (out, title, hint) => out.append(
  el('p', { class: 'ct-step' }, 'Your result'), el('h3', { class: 'ct-question' }, title), el('p', { class: 'ct-hint' }, hint));

function wire(form, out, render) {
  if (!form || !out) return;
  const run = () => { out.replaceChildren(); render(new FormData(form), out); };
  form.addEventListener('input', run);
  form.addEventListener('change', run);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); run(); });
  run();
}

// ---- Add or remove VAT
wire(document.getElementById('vc-form'), document.getElementById('vc-result'), (d, out) => {
  const amount = num(d.get('amount'));
  const add = (d.get('mode') || 'add') === 'add';
  if (!amount) {
    prompt(out, 'Enter an amount.', 'Then choose whether it is the price before VAT or a price that already includes VAT.');
    return;
  }
  const r = add ? addVat(amount) : removeVat(amount);
  out.append(
    el('p', { class: 'ct-step' }, add ? 'Total including VAT' : 'Amount before VAT'),
    el('p', { class: 'gr-total' }, AED(add ? r.total : r.net)),
    el('p', { class: 'ct-hint' }, add
      ? `${AED(r.net)} plus 5% VAT of ${AED(r.vat)}.`
      : `${AED(r.total)} includes 5% VAT of ${AED(r.vat)}.`),
    rowsList([
      ['Amount before VAT', add ? 'The amount you entered' : `${AED(r.total)} − ${AED(r.vat)}`, AED(r.net)],
      ['VAT at 5%', add ? `${AED(r.net)} × 5%` : `${AED(r.total)} × 5 ÷ 105`, AED(r.vat)],
      ['Total including VAT', add ? `${AED(r.net)} + ${AED(r.vat)}` : 'The amount you entered', AED(r.total)],
    ]),
    notesList([
      add
        ? 'To add VAT in one step, multiply the price by 1.05.'
        : 'To take VAT out in one step, divide the price by 1.05. The VAT inside a price is 5/105 of it (about 4.76%), not 5%.',
      'VAT is rounded to the nearest fils, as the Executive Regulation allows (Article 61).',
      'This uses the 5% standard rate. Zero-rated supplies carry 0% VAT and exempt supplies carry none: see the rules below.',
    ]),
    el('p', { class: 'ct-note' }, 'A calculation only, based on your figures. It is not tax advice.'),
  );
});

// ---- VAT for a tax period
wire(document.getElementById('vp-form'), document.getElementById('vp-result'), (d, out) => {
  const sales = num(d.get('sales'));
  const purchases = num(d.get('purchases'));
  if (!sales && !purchases) {
    prompt(out, 'Enter your sales and purchases for the period.', 'Use the amounts before VAT, for sales and purchases charged at 5% only.');
    return;
  }
  const r = period(sales, purchases);
  out.append(
    el('p', { class: 'ct-step' }, r.due < 0 ? 'Estimated VAT recoverable' : 'Estimated VAT to pay'),
    el('p', { class: 'gr-total' }, AED(Math.abs(r.due))),
    el('p', { class: 'ct-hint' }, r.due < 0
      ? 'Your input VAT is more than your output VAT for the period, so the return would show excess recoverable tax.'
      : 'Output VAT on your sales, less the input VAT you can recover on your purchases.'),
    rowsList([
      ['Output VAT on sales', `${AED(sales)} × 5%`, AED(r.output)],
      ['Input VAT on purchases', `${AED(purchases)} × 5%`, `− ${AED(r.input)}`],
    ]),
    notesList([
      'The payable tax for a period is the output tax less the recoverable input tax (Article 53).',
      'Input VAT is recoverable on goods and services used to make taxable supplies (Article 54). Leave out purchases without a valid tax invoice and costs behind exempt sales.',
      'This estimate leaves out imports, reverse-charge purchases, zero-rated and exempt sales, and adjustments from earlier periods.',
    ]),
    el('p', { class: 'ct-note' }, 'An estimate only, based on your figures. It is not tax advice and is not a VAT return.'),
  );
});
