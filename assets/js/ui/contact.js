// Contact: form delivery, service pre-selection, WhatsApp shortcuts.
//   Form: Formspree via fetch when data-formspree holds a real form ID;
//         otherwise opens the visitor's email app with the message filled in.
//   "Discuss this" links ([data-service]) pre-select the service and tailor
//   the WhatsApp greeting.
//   Floating WhatsApp button: small screens, shown after the hero, hidden
//   while the contact section itself is on screen.

const EMAIL = 'info@accumindsconsulting.ae';
const DEFAULT_TOPIC = 'my accounting and compliance needs';

export function initContact(motion) {
  const form = document.getElementById('contact-form');
  const waLinks = [...document.querySelectorAll('[data-whatsapp]')];

  const setWhatsAppTopic = (topic) => {
    const text = `Hello AccuMinds, I'd like to discuss ${topic}.`;
    waLinks.forEach((a) => {
      a.href = `https://wa.me/${a.dataset.whatsapp}?text=${encodeURIComponent(text)}`;
    });
  };

  document.addEventListener('click', (e) => {
    const link = e.target.closest('[data-service]');
    if (!link || !form) return;
    form.elements.service.value = link.dataset.service;
    setWhatsAppTopic(link.dataset.service);
  });
  form?.elements.service.addEventListener('change', (e) => {
    setWhatsAppTopic(e.target.value === 'Something else' ? DEFAULT_TOPIC : e.target.value);
  });

  if (form) initForm(form, motion);
  initFloatingButton();
}

function initForm(form, motion) {
  const body = form.querySelector('.form-body');
  const sent = form.querySelector('.sent');
  const title = sent.querySelector('.sent-title');
  const text = sent.querySelector('.sent-text');
  const error = form.querySelector('.form-error');
  const button = form.querySelector('button[type="submit"]');
  const label = button.querySelector('.btn-label');
  const formId = (form.dataset.formspree || '').trim();
  const useFormspree = /^[A-Za-z0-9]{6,}$/.test(formId) && formId !== 'TODO';

  const busy = (on) => {
    button.disabled = on;
    button.setAttribute('aria-busy', String(on));
    label.textContent = on ? 'Sending…' : 'Send inquiry';
  };

  const showSent = (mode) => {
    if (mode === 'mail') {
      title.textContent = 'Your email app should now open.';
      text.innerHTML = `Send the pre-filled message from there. If nothing opened, email us at <a href="mailto:${EMAIL}">${EMAIL}</a>.`;
    } else {
      title.textContent = 'Thanks, we’ll be in touch.';
      text.textContent = 'We’ve received your message.';
    }
    body.hidden = true;
    sent.hidden = false;
    title.focus();
    drawTick(sent, motion);
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    error.hidden = true;
    const data = new FormData(form);
    if (data.get('_gotcha')) return; // honeypot filled: almost certainly a bot

    if (!useFormspree) {
      window.location.href = mailtoFrom(data);
      showSent('mail');
      return;
    }

    busy(true);
    try {
      const res = await fetch(`https://formspree.io/f/${formId}`, {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' },
      });
      if (!res.ok) throw new Error(`Formspree ${res.status}`);
      form.reset();
      showSent('sent');
    } catch {
      error.hidden = false;
    } finally {
      busy(false);
    }
  });

  sent.querySelector('.sent-again').addEventListener('click', () => {
    sent.hidden = true;
    body.hidden = false;
    form.elements.name.focus();
  });
}

function mailtoFrom(data) {
  const lines = [
    `Name: ${data.get('name')}`,
    `Email: ${data.get('email')}`,
    `Service: ${data.get('service')}`,
    '',
    data.get('note') || '',
  ];
  const subject = `Inquiry: ${data.get('service')}`;
  return `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
}

function drawTick(sent, motion) {
  const tick = sent.querySelector('.sent-tick');
  if (!motion.enabled || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  motion.gsap.fromTo(tick, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.7, delay: 0.1, ease: 'power2.out' });
}

function initFloatingButton() {
  const fab = document.querySelector('.wa-float');
  const hero = document.querySelector('.hero');
  const contact = document.getElementById('contact');
  if (!fab || !hero || !contact) return;

  let pastHero = false;
  let atContact = false;
  const update = () => {
    const show = pastHero && !atContact;
    fab.classList.toggle('is-visible', show);
    // Keep it out of the tab order and accessibility tree while hidden.
    if (show) fab.removeAttribute('tabindex'); else fab.setAttribute('tabindex', '-1');
    fab.setAttribute('aria-hidden', String(!show));
  };
  new IntersectionObserver(([entry]) => {
    pastHero = !entry.isIntersecting && entry.boundingClientRect.top < 0;
    update();
  }).observe(hero);
  new IntersectionObserver(([entry]) => {
    atContact = entry.isIntersecting;
    update();
  }, { rootMargin: '0px 0px -30% 0px' }).observe(contact);
  update();
}
