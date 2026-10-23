// Supplier verification check (/supplier-verification-check/), based on FTA Decision No. 13 of 2026.
// Runs in the browser; nothing is sent anywhere. Indicative only: not tax advice.

const form = document.getElementById('sv-form');
const out = document.getElementById('sv-result');

const AED = (n) => `AED ${Math.round(n).toLocaleString('en-US')}`;
const num = (v) => {
  const n = Number(String(v ?? '').replace(/[^0-9.]/g, ''));
  return Number.isFinite(n) ? n : 0;
};

// [text, article, required?]
const SUPPLIER = {
  company: [
    ['Incorporation verified on an official database, or a copy of the certificate of incorporation or trade licence; name, address and employees match', 'Art. 3.1b(1)', true],
    ['Emirates ID or passport of the director, agent or employee who represents the supplier', 'Art. 3.1b(2)', true],
  ],
  person: [
    ['Valid Emirates ID or passport of the supplier', 'Art. 3.1a(1)', true],
    ['Record of a meeting with the supplier, in person or virtually, before the supply (with the date)', 'Art. 3.1a(2)', true],
  ],
  all: [
    ['Actual place of business verified electronically or by a site visit, and suitable for the activity (Ejari, utility bill, dated photo or visit note)', 'Art. 3.2', true],
    ['Risk indicators checked: address or key employees changed more than twice in 12 months; transactions out of proportion to the supplier’s size or history', 'Art. 3.3', true],
    ['TRN checked on the FTA portal (dated screenshot) and VAT certificate on file', 'Good practice', false],
  ],
  enhanced: [
    ['Written confirmation from an authorised UAE bank that the supplier holds a bank account, with no reservations (a letter on the supplier’s own letterhead is not enough)', 'Art. 3.4a', true],
    ['Review of clients’ recommendations where available, and public reviews and media from reliable sources; dated and saved', 'Art. 3.4b', true],
  ],
};

const TRANSACTION = [
  ['Commercial reason for the supply: purchase order, contract or accepted quotation', 'Art. 4.1', true],
  ['Payment by electronic means: bank transfer advice matching the supplier', 'Art. 4.2b', true],
  ['Price or margin in line with the market, or the documented reason it differs (e.g. two comparable quotes)', 'Art. 4.3a', true],
  ['Goods or services fall within the supplier’s ordinary or licensed activities', 'Art. 4.3b', true],
  ['Valid tax invoice: supplier TRN, your TRN, invoice number and date, VAT shown separately', 'VAT Law', true],
];

const CONDITIONAL = {
  cash: ['Cash payment: documented commercial reason, within legal limits, easily verifiable', 'Art. 4.2b', true],
  thirdparty: ['Third-party payment or account outside the supplier’s country of incorporation: written commercial explanation', 'Art. 4.2a', true],
  goods: ['Goods: authenticity, origin and the supplier’s right to sell them verified (delivery note or GRN)', 'Art. 4.3c', true],
  imported: ['Imported goods: bill of lading, packing list and customs declaration on file', 'Art. 4.3c', true],
  intermediary: ['Intermediary or agent: clear commercial explanation of the supplier’s role', 'Art. 4.3d', true],
};

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) n.setAttribute(k, v === true ? '' : v);
  }
  for (const k of kids) n.append(k);
  return n;
}

let seq = 0;
function list(items) {
  return el('ul', { class: 'sv-list' }, ...items.map(([text, ref, req]) => {
    const id = `sv-item-${++seq}`;
    return el('li', {},
      el('input', { type: 'checkbox', id }),
      el('label', { for: id }, text, ' ', el('span', { class: `sv-ref${req ? '' : ' sv-ref--rec'}` }, req ? ref : `${ref} (recommended)`)));
  }));
}

function render() {
  const d = new FormData(form);
  const type = d.get('type') || 'company';
  const invoice = num(d.get('invoice'));
  const prev = num(d.get('prev'));
  const next = num(d.get('next'));
  const verified = d.get('verified') === 'yes';
  const flags = new Set(d.getAll('flag'));
  const risks = d.getAll('risk');
  const name = String(d.get('name') || '').trim() || 'Supplier';
  const blank = (k) => !String(d.get(k) ?? '').trim();

  const aggregate = prev > 100000 || next > 100000;
  const enhanced = prev > 375000 || next > 375000;
  const exempt = invoice < 10000 && !aggregate;
  seq = 0;
  out.replaceChildren();

  if (blank('invoice')) {
    out.append(
      el('p', { class: 'ct-step' }, 'Your result'),
      el('h3', { class: 'ct-question' }, 'Enter the invoice amount to see which checks apply.'),
      el('p', { class: 'ct-hint' }, 'Add the totals from this supplier for the previous and next 12 months too: above AED 100,000, every invoice from them is in scope.'),
      el('div', { class: 'ct-actions' },
        el('a', { class: 'btn btn-ghost-light', href: '/assets/downloads/accuminds-supplier-verification-checklist.pdf', download: true }, 'Download the full checklist (PDF)')));
    return;
  }

  const head = el('div', { class: 'sv-head' },
    el('p', { class: 'ct-step' }, 'Your result'),
    el('h3', { class: 'ct-question' }, exempt
      ? 'This supply can be left out of the Decision 13 checks.'
      : enhanced ? 'Full checks, including the enhanced checks.' : 'Full supplier and transaction checks apply.'));
  const why = el('p', { class: 'ct-hint' }, exempt
    ? `The invoice is below AED 10,000 (excluding VAT) and total supplies from this supplier do not exceed AED 100,000 in the previous or next 12 months (Art. 6). Keep the tax invoice as usual.`
    : [
      invoice >= 10000 ? `The invoice is ${AED(invoice)}, so the AED 10,000 exception does not apply.` : '',
      aggregate ? `Supplies from this supplier exceed AED 100,000 in 12 months, so every supply from them is in scope (Art. 6.2).` : '',
      enhanced ? `Above AED 375,000 in 12 months: bank confirmation and reputation review also required (Art. 3.4).` : '',
    ].filter(Boolean).join(' '));
  out.append(head, why);
  if (blank('prev') || blank('next')) {
    out.append(el('p', { class: 'sv-muted sv-small' }, 'A 12-month total left blank is treated as AED 0.'));
  }

  if (!exempt) {
    const print = el('div', { id: 'sv-print', class: 'sv-print' },
      el('div', { class: 'sv-print-head' },
        el('p', { class: 'sv-print-title' }, `Supplier verification record: ${name}`),
        el('p', { class: 'sv-print-meta' },
          `Prepared ${new Date().toISOString().slice(0, 10)} · ${type === 'company' ? 'Company' : 'Individual'} supplier · invoice ${AED(invoice)} · previous 12 months ${AED(prev)} · next 12 months ${AED(next)}`)));
    const supplierItems = verified ? [] : [...SUPPLIER[type], ...SUPPLIER.all, ...(enhanced ? SUPPLIER.enhanced : [])];
    print.append(el('h4', { class: 'sv-h' }, 'Supplier file'),
      verified
        ? el('p', { class: 'sv-muted' }, 'Verified within the last 12 months: no refresh needed now (Art. 5.1). Re-verify when 12 months have passed.')
        : list(supplierItems));
    if (risks.length) {
      print.append(el('p', { class: 'sv-warn' },
        `Risk indicator${risks.length > 1 ? 's' : ''} flagged: ${risks.join('; ')}. Keep a clear, justified written explanation on file and provide it to the FTA on request (Art. 3.3b).`));
    }
    const tx = [...TRANSACTION, ...Object.entries(CONDITIONAL).filter(([k]) => flags.has(k) || (k === 'goods' && flags.has('imported'))).map(([, v]) => v)];
    print.append(el('h4', { class: 'sv-h' }, 'Transaction file (this invoice)'), list(tx));
    print.append(el('div', { class: 'sv-sign' },
      el('span', {}, 'Checked by: ____________________'), el('span', {}, 'Reviewed by: ____________________'), el('span', {}, 'Date: ____________')));
    print.append(el('p', { class: 'sv-muted sv-small' },
      'Keep this record with the supporting documents where the FTA can review them (Art. 5.3). Based on FTA Decision No. 13 of 2026; indicative only, not tax advice. accumindsconsulting.ae'));
    out.append(print);
  }

  out.append(el('div', { class: 'ct-actions' },
    ...(exempt ? [] : [el('button', { type: 'button', class: 'btn btn-gold', onclick: () => window.print() }, 'Print or save as PDF')]),
    el('a', { class: 'btn btn-ghost-light', href: '/assets/downloads/accuminds-supplier-verification-checklist.pdf', download: true }, 'Download the full checklist (PDF)')));
}

// Copies the record to a top-level sheet for printing (see the print rules in main.css),
// keeping the ticks the visitor has made. Runs for the button and for Ctrl+P alike.
function buildPrintSheet() {
  document.getElementById('sv-print-sheet')?.remove();
  const record = document.getElementById('sv-print');
  if (!record) return;
  const sheet = record.cloneNode(true);
  sheet.id = 'sv-print-sheet';
  const ticks = record.querySelectorAll('input');
  sheet.querySelectorAll('input').forEach((box, i) => { box.checked = ticks[i].checked; box.removeAttribute('id'); });
  sheet.querySelectorAll('label').forEach((label) => label.removeAttribute('for'));
  document.body.append(sheet);
}

if (form && out) {
  addEventListener('beforeprint', buildPrintSheet);
  addEventListener('afterprint', () => document.getElementById('sv-print-sheet')?.remove());
  form.addEventListener('input', render);
  form.addEventListener('change', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); out.querySelector('h3')?.focus?.(); });
  render();
}
