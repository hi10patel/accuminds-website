// UAE TRN format check (/trn-verification-uae/).
// Format per PINT AE rule IBR-132-AE: 15 digits, starting with 1 and ending with 03.
// The TIN is the TRN's first 10 digits (MoF UAE Electronic Invoicing Guidelines v2.0, Highlights).
// Runs in the browser; nothing is sent anywhere. It checks the format only: whether a TRN
// is registered can only be confirmed with the FTA's own TRN/TIN verification.

const form = document.getElementById('trn-form');
const out = document.getElementById('trn-result');
const FTA = 'https://tax.gov.ae/en/default.aspx';

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

const ftaLink = () => el('a', { class: 'u-link', href: FTA, target: '_blank', rel: 'noopener' }, 'TRN/TIN verification on tax.gov.ae');

// Drop a leading "TRN" or "TIN" label and the spaces, dashes and dots people type or copy in.
export function clean(raw) {
  return String(raw ?? '').trim().replace(/^(trn|tin)\s*(no\.?|number)?\s*[:#-]?\s*/i, '').replace(/[\s.\-–]/g, '');
}

export function check(raw) {
  const n = clean(raw);
  if (!n) return { kind: 'empty' };
  if (/\D/.test(n)) return { kind: 'chars', n };
  if (n.length === 10) return { kind: 'tin', n };
  if (n.length !== 15) return { kind: 'length', n };
  const starts = n[0] === '1';
  const ends = n.endsWith('03');
  return { kind: starts && ends ? 'ok' : 'pattern', n, starts, ends };
}

function render() {
  const r = check(new FormData(form).get('trn'));
  out.replaceChildren();
  const head = (title, ...lines) => {
    out.append(el('p', { class: 'ct-step' }, 'Format check'), el('h3', { class: 'ct-question' }, title));
    for (const l of lines) out.append(el('p', { class: 'ct-hint' }, ...[].concat(l)));
  };

  if (r.kind === 'empty') {
    head('Enter a TRN to check its format.', 'Copy it from the invoice or the supplier’s VAT registration certificate.');
    return;
  }
  if (r.kind === 'chars') {
    head('A TRN has digits only.', `Remove the letters or symbols: “${r.n.replace(/\d/g, '')}”.`);
    return;
  }
  if (r.kind === 'tin') {
    head('This looks like a 10-digit TIN, not a TRN.',
      'A TIN is the first 10 digits of a TRN.',
      ['The FTA’s verification accepts a TIN too: choose TIN instead of TRN on the ', ftaLink(), '.'],
      'If you need the supplier’s VAT number for a tax invoice, ask for the 15-digit TRN.');
    return;
  }
  if (r.kind === 'length') {
    head(`This has ${r.n.length} digits; a TRN has 15.`, 'Check for a missing or extra digit against the invoice or the VAT registration certificate.');
    return;
  }

  out.append(
    el('p', { class: 'ct-step' }, 'Format check'),
    el('h3', { class: 'ct-question' }, r.kind === 'ok' ? 'The format is right.' : 'This is not the format of a UAE VAT TRN.'),
    el('p', { class: 'gr-total trn-num' }, r.n),
  );
  const mark = (pass) => (pass ? '✓ Yes' : '✗ No');
  const rows = [['15 digits', '✓ Yes'], ['Starts with 1', mark(r.starts)], ['Ends with 03', mark(r.ends)]];
  if (r.kind === 'ok') rows.push(['TIN (first 10 digits)', r.n.slice(0, 10)]);
  out.append(el('dl', { class: 'gr-rows' }, ...rows.map(([t, v]) => el('div', {}, el('dt', {}, t), el('dd', {}, v)))));

  if (r.kind === 'ok') {
    out.append(el('p', { class: 'ct-hint' }, 'The format does not show that the TRN is registered. Confirm it on the ', ftaLink(), ', and check that the name matches the invoice.'));
    const btn = el('button', { class: 'btn btn-gold btn-sm', type: 'button' }, 'Copy number');
    const status = el('span', { class: 'ct-hint', 'aria-live': 'polite' });
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(r.n);
        status.textContent = ' Copied. Paste it into the FTA verification.';
      } catch {
        status.textContent = ' Select the number above and copy it.';
      }
    });
    out.append(el('p', { class: 'gr-embed__row trn-copy' }, btn, status));
  } else {
    out.append(el('p', { class: 'ct-hint' }, 'A UAE VAT TRN starts with 1 and ends with 03 (PINT AE rule IBR-132-AE). Check the number against the supplier’s VAT registration certificate before you rely on the invoice.'));
  }
  out.append(el('p', { class: 'ct-note' }, 'Format check only. It does not look anything up, and nothing you enter is sent.'));
}

if (form && out) {
  form.addEventListener('input', render);
  form.addEventListener('submit', (ev) => { ev.preventDefault(); render(); });
  render();
}
