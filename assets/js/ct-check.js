// Corporate Tax filing check (/corporate-tax-check/). Runs in the browser; nothing is sent anywhere.
// Rules are summarised from FTA and Ministry of Finance pages (linked on the page) and were
// checked on the date shown there. Indicative only: not tax advice.

const AED = (n) => `AED ${n.toLocaleString('en-US')}`;

const QUESTIONS = {
  who: {
    text: 'Which best describes you?',
    options: [
      { id: 'company', label: 'A company or other legal entity', hint: 'Mainland or free zone: LLC, FZCO, FZE, branch registered in the UAE' },
      { id: 'person', label: 'An individual doing business', hint: 'Sole establishment, freelancer, licensed professional' },
      { id: 'exempt', label: 'A government entity, charity or fund', hint: 'Government or government-controlled entity, public benefit entity, investment or pension fund' },
    ],
  },
  turnover: {
    text: `Did your business turnover in a calendar year (January to December) exceed ${AED(1000000)}?`,
    hint: 'Count business and business-activity income only. Salary, personal investment income and personal real estate investment income are not counted.',
    options: [{ id: 'yes', label: 'Yes' }, { id: 'no', label: 'No' }],
  },
  qfzp: {
    text: 'Are you a free zone company that intends to be a Qualifying Free Zone Person (0% on qualifying income)?',
    options: [{ id: 'yes', label: 'Yes' }, { id: 'no', label: 'No, or not a free zone company' }, { id: 'unsure', label: 'Not sure' }],
  },
  revenue: {
    text: `Was your revenue ${AED(3000000)} or less in this tax period and in every previous tax period?`,
    options: [{ id: 'yes', label: 'Yes' }, { id: 'no', label: 'No' }],
  },
  mne: {
    text: `Are you part of a multinational group with consolidated revenue above ${AED(3150000000)}?`,
    options: [{ id: 'no', label: 'No' }, { id: 'yes', label: 'Yes' }],
  },
};

function next(a) {
  if (!a.who) return 'who';
  if (a.who === 'exempt') return null;
  if (a.who === 'person' && !a.turnover) return 'turnover';
  if (a.who === 'person' && a.turnover === 'no') return null;
  if (a.who === 'company' && !a.qfzp) return 'qfzp';
  if (a.qfzp === 'yes') return null;
  if (!a.revenue) return 'revenue';
  if (a.revenue === 'no') return null;
  if (!a.mne) return 'mne';
  return null;
}

function result(a) {
  const always = [
    'File a Corporate Tax return for every tax period within 9 months of the end of that period, even when no tax is due.',
    `Late registration carries an ${AED(10000)} penalty. The FTA waives it if the first return is filed within 7 months of the end of the first tax period.`,
  ];
  if (a.who === 'exempt') {
    return {
      tone: 'info',
      title: 'It depends on your exempt category.',
      points: [
        'Government entities, and businesses notified to the Ministry of Finance as natural resource businesses, generally do not register unless they carry on taxable business.',
        'Qualifying public benefit entities, and investment funds, pension funds and their subsidiaries approved by the FTA, are generally required to register.',
        'Exempt status has conditions and, for some categories, needs approval. Get it confirmed before relying on it.',
      ],
    };
  }
  if (a.who === 'person' && a.turnover === 'no') {
    return {
      tone: 'good',
      title: 'You do not need to register for Corporate Tax yet.',
      points: [
        `Individuals become subject to Corporate Tax when business turnover in a calendar year exceeds ${AED(1000000)}.`,
        'Keep proper records and check again each year: once you cross the threshold you must register and file.',
      ],
    };
  }
  const points = [
    a.who === 'person'
      ? `Because your business turnover exceeded ${AED(1000000)} in a calendar year, you must register for Corporate Tax.`
      : 'UAE companies, including free zone companies, must register for Corporate Tax, whatever their revenue or profit.',
  ];
  if (a.qfzp === 'yes') {
    points.push(
      'As a Qualifying Free Zone Person, qualifying income is taxed at 0% if you meet all the conditions. You still register and file a return.',
      'Qualifying Free Zone Persons must prepare audited financial statements.',
      'Small Business Relief is not available to Qualifying Free Zone Persons.',
    );
    return { tone: 'act', title: 'Register, file every year, and keep audited accounts.', points: points.concat(always) };
  }
  if (a.qfzp === 'unsure') {
    points.push('Whether you qualify as a Qualifying Free Zone Person depends on your activities, income and substance in the free zone. It is worth confirming before your first return.');
  }
  const sbr = a.revenue === 'yes' && a.mne === 'no';
  if (sbr) {
    points.push(
      `You appear eligible for Small Business Relief: you can elect to be treated as having no taxable income for tax periods ending on or before 31 December 2029. It is claimed in the return, so you still register and file.`,
    );
    return { tone: 'act', title: 'Register and file; you can likely claim Small Business Relief.', points: points.concat(always) };
  }
  points.push(
    a.mne === 'yes'
      ? 'Members of large multinational groups cannot elect Small Business Relief.'
      : `Small Business Relief is not available because revenue exceeded ${AED(3000000)} in this or an earlier tax period.`,
    `Taxable income up to ${AED(375000)} is taxed at 0% and the rest at 9%.`,
  );
  return { tone: 'act', title: 'Register and file a return every tax period.', points: points.concat(always) };
}

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v);
  }
  for (const k of kids) n.append(k);
  return n;
}

function mount(root) {
  const answers = {};
  const history = [];

  const render = (focus = true) => {
    root.replaceChildren();
    const key = next(answers);
    if (key) {
      const q = QUESTIONS[key];
      const step = history.length + 1;
      const legendId = `ct-q-${key}`;
      const group = el('div', { class: 'ct-options', role: 'group', 'aria-labelledby': legendId });
      for (const o of q.options) {
        group.append(el('button', {
          type: 'button', class: 'ct-option',
          onclick: () => { answers[key] = o.id; history.push(key); render(); },
        }, el('span', { class: 'ct-option-label' }, o.label), ...(o.hint ? [el('span', { class: 'ct-option-hint' }, o.hint)] : [])));
      }
      root.append(
        el('p', { class: 'ct-step' }, `Question ${step}`),
        el('h3', { class: 'ct-question', id: legendId, tabindex: '-1' }, q.text),
        ...(q.hint ? [el('p', { class: 'ct-hint' }, q.hint)] : []),
        group,
      );
    } else {
      const r = result(answers);
      root.append(
        el('p', { class: `ct-step ct-tone-${r.tone}` }, 'Your result'),
        el('h3', { class: 'ct-question', tabindex: '-1' }, r.title),
        el('ul', { class: 'ct-points' }, ...r.points.map((p) => el('li', {}, p))),
        el('p', { class: 'ct-note' }, 'Indicative only, based on your answers. It is not tax advice; rules have conditions and exceptions.'),
        el('div', { class: 'ct-actions' },
          el('a', { class: 'btn btn-gold', href: '/#contact' }, 'Get it confirmed'),
          el('a', { class: 'btn btn-ghost-light', href: '/services/corporate-tax-uae/' }, 'Corporate Tax services')),
      );
    }
    if (history.length) {
      root.append(el('div', { class: 'ct-nav' },
        el('button', { type: 'button', class: 'ct-link', onclick: () => { delete answers[history.pop()]; render(); } }, '← Back'),
        el('button', { type: 'button', class: 'ct-link', onclick: () => { for (const k of history.splice(0)) delete answers[k]; render(); } }, 'Start again')));
    }
    if (focus) root.querySelector('.ct-question')?.focus({ preventScroll: true });
  };
  render(false);
}

const root = document.getElementById('ct-check');
if (root) mount(root);
