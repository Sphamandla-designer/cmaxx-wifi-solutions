  // Form delivery endpoint. Leave empty until CMAXX confirms the recipient,
  // storage and privacy notice (brief launch gates H02/H05, Part 10). While
  // empty, a valid submission tells the visitor it was NOT sent and offers
  // phone/WhatsApp instead; it never shows a false success message.
  FORM_ENDPOINT = '';

  componentDidMount() {
    this.routes = __ROUTES__;
    const saved = (function () { try { return localStorage.getItem('cmaxx-site-page'); } catch (e) { return null; } })();
    const initial = this.parseHref(decodeURIComponent(location.hash.slice(1) || ''));
    const initialPage = (initial && this.routes[initial.path]) || (saved && this.routes[saved]) || '/wifi-network-solutions/';
    this.show(initialPage, false, initial && initial.frag);

    document.addEventListener('click', (e) => this.onClick(e));
    document.addEventListener('submit', (e) => this.onSubmit(e), true);
    document.addEventListener('input', (e) => this.clearFieldError(e.target));
    document.addEventListener('change', (e) => this.clearFieldError(e.target));
    document.addEventListener('error', (e) => this.onImageError(e), true);
    window.addEventListener('load', () => this.checkImages());
    setTimeout(() => this.checkImages(), 4000);

    window.addEventListener('hashchange', () => {
      const r = this.parseHref(decodeURIComponent(location.hash.slice(1)));
      const t = r && this.routes[r.path];
      if (t) this.show(t, false, r.frag);
    });

    this.prepareForms();
    this.watchEnquiries();
  }

  // '/smart-home/#ecosystems' -> { path: '/smart-home/', frag: 'ecosystems' }
  parseHref(href) {
    if (!href || href.charAt(0) !== '/') return null;
    const i = href.indexOf('#');
    return i < 0 ? { path: href, frag: '' } : { path: href.slice(0, i), frag: href.slice(i + 1) };
  }

  activePage() {
    return document.querySelector('[data-page][data-active]');
  }

  onClick(e) {
    const a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href) return;

    if (a.hasAttribute('data-contact')) this.track('contact_click', { channel: a.getAttribute('data-contact') });

    // In-page anchors resolve inside the visible page only, so the route in
    // the address bar is preserved and ids shared by two pages still work.
    if (href.charAt(0) === '#' && href.length > 1) {
      const target = this.findInPage(this.activePage(), href.slice(1));
      if (!target) return;
      e.preventDefault();
      this.applyService(a);
      this.scrollToEl(target);
      return;
    }

    if (href.charAt(0) !== '/') return;
    e.preventDefault();
    const r = this.parseHref(href);
    const page = this.routes[r.path];
    if (page) {
      this.show(page, true, r.frag);
      this.applyService(a);
      return;
    }
    // Pages that live outside this file (Contact, Areas We Serve, Industries,
    // Public & Guest WiFi, Privacy, Case Studies): go to this page's enquiry.
    const active = this.activePage();
    const contact = active && (active.querySelector('[data-enquiry]') || active.querySelector('[id$="-contact"]'));
    if (contact) this.scrollToEl(contact);
  }

  findInPage(page, id) {
    if (!page || !id) return null;
    try { return page.querySelector('#' + CSS.escape(id)); } catch (err) { return null; }
  }

  scrollToEl(el) {
    const top = el.getBoundingClientRect().top + window.scrollY - 96;
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: Math.max(0, top), behavior: reduce ? 'auto' : 'smooth' });
    const focusable = /^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY)$/.test(el.tagName);
    if (!focusable && !el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
    try { el.focus({ preventScroll: true }); } catch (err) {}
  }

  // Links carrying data-service preselect the enquiry form's service without
  // clearing anything the visitor has already typed.
  applyService(a) {
    const svc = a.getAttribute('data-service');
    if (!svc) return;
    const page = this.activePage();
    const sel = page && page.querySelector('form[data-cx-form] select[name="service"]');
    if (sel && Array.from(sel.options).some((o) => o.value === svc)) sel.value = svc;
  }

  show(page, scrollTop, frag) {
    const sections = document.querySelectorAll('[data-page]');
    let found = null;
    sections.forEach((s) => {
      const match = s.getAttribute('data-page') === page;
      s.style.display = match ? 'block' : 'none';
      if (match) { s.setAttribute('data-active', ''); found = s; } else { s.removeAttribute('data-active'); }
    });
    if (!found && sections.length) {
      found = sections[0];
      found.style.display = 'block';
      found.setAttribute('data-active', '');
      page = found.getAttribute('data-page');
    }
    if (found) {
      const title = found.getAttribute('data-title');
      if (title) document.title = title;
      const desc = found.getAttribute('data-description');
      const meta = document.querySelector('meta[name="description"]');
      if (desc && meta) meta.setAttribute('content', desc);
    }
    try { localStorage.setItem('cmaxx-site-page', page); } catch (e) {}
    if (location.hash.slice(1) !== page) history.replaceState(null, '', '#' + page);
    const target = frag && this.findInPage(found, frag);
    if (target) {
      requestAnimationFrame(() => this.scrollToEl(target));
    } else if (scrollTop) {
      window.scrollTo({ top: 0, behavior: 'auto' });
    }
    if (this.updateSticky) this.updateSticky();
  }

  // ---- images: graceful fallback when a web image cannot load ----
  onImageError(e) {
    const img = e.target;
    if (!img || img.tagName !== 'IMG') return;
    const box = img.closest('.cx-fig, .cx-cardimg');
    if (box) box.classList.add('cx-img-failed');
  }

  checkImages() {
    document.querySelectorAll('.cx-fig img, .cx-cardimg img').forEach((img) => {
      if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) {
        const box = img.closest('.cx-fig, .cx-cardimg');
        if (box) box.classList.add('cx-img-failed');
      }
    });
  }

  // ---- sticky bar hides while the page's enquiry form is in view ----
  watchEnquiries() {
    const visible = new Set();
    this.updateSticky = () => {
      const page = this.activePage();
      if (!page) return;
      const bar = page.querySelector('[data-sticky]');
      if (!bar) return;
      const enquiry = page.querySelector('[data-enquiry]');
      if (enquiry && visible.has(enquiry)) bar.setAttribute('data-hidden', '');
      else bar.removeAttribute('data-hidden');
    };
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) visible.add(en.target); else visible.delete(en.target); });
      this.updateSticky();
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('[data-enquiry]').forEach((el) => io.observe(el));
  }

  // ---- enquiry forms ----
  prepareForms() {
    document.querySelectorAll('form[data-cx-form] select[defaultValue], form[data-cx-form] select[defaultvalue]').forEach((sel) => {
      const v = sel.getAttribute('defaultValue') || sel.getAttribute('defaultvalue');
      if (v) sel.value = v;
    });
  }

  clearFieldError(el) {
    if (!el || !el.closest || !el.closest('form[data-cx-form]')) return;
    if (el.getAttribute('aria-invalid') === 'true') el.removeAttribute('aria-invalid');
    const holder = el.closest('.cx-field, .cx-fieldset');
    const err = holder && holder.querySelector('.cx-err');
    if (err) err.textContent = '';
    if (el.name === 'contact_method') {
      el.form.querySelectorAll('input[name="contact_method"]').forEach((r) => r.removeAttribute('aria-invalid'));
    }
  }

  validPhone(v) {
    const digits = v.replace(/[\s()+\-.]/g, '');
    return /^\+?[\d\s()\-.]+$/.test(v) && /^\d{9,15}$/.test(digits);
  }

  validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  }

  validate(form) {
    const kind = form.getAttribute('data-cx-form');
    const val = (n) => { const el = form.elements[n]; return el && el.value ? el.value.trim() : ''; };
    const errors = [];
    const fail = (name, msg) => {
      const el = name === 'contact_method' ? form.querySelector('input[name="contact_method"]') : form.elements[name];
      if (!el) return;
      errors.push({ el, msg });
      if (name === 'contact_method') {
        form.querySelectorAll('input[name="contact_method"]').forEach((r) => r.setAttribute('aria-invalid', 'true'));
      } else {
        el.setAttribute('aria-invalid', 'true');
      }
      const holder = el.closest('.cx-field, .cx-fieldset');
      const err = holder && holder.querySelector('.cx-err');
      if (err) err.textContent = msg;
    };

    if (kind === 'network') {
      if (!val('full_name')) fail('full_name', 'Please enter your name.');
      if (!val('property_type')) fail('property_type', 'Please choose the type of property or organisation.');
      if (!val('suburb')) fail('suburb', 'Please enter the suburb or town.');
      if (!val('message')) fail('message', 'Please tell us briefly what you need help with.');
      const methodEl = form.querySelector('input[name="contact_method"]:checked');
      const method = methodEl ? methodEl.value : '';
      if (!method) fail('contact_method', 'Please choose how we should contact you.');
      const email = val('email');
      if ((method === 'email' && !email) || (email && !this.validEmail(email))) {
        fail('email', 'Please enter a valid email address for an email response.');
      }
      const phone = val('phone');
      if (((method === 'phone' || method === 'whatsapp') && !phone) || (phone && !this.validPhone(phone))) {
        fail('phone', 'Please enter a valid contact number for your chosen response method.');
      }
    } else {
      ['full_name', 'suburb', 'service', 'message'].forEach((n) => { if (!val(n)) fail(n, 'Please complete this field.'); });
      const phone = val('phone');
      if (!phone || !this.validPhone(phone)) fail('phone', 'Please enter a contact number we can use to reach you.');
      const email = val('email');
      if (email && !this.validEmail(email)) fail('email', 'Please enter a valid email address, or leave this optional field blank.');
    }
    return errors;
  }

  formMessages(kind) {
    return kind === 'network'
      ? {
          summary: 'Please check the highlighted fields and try again.',
          sending: 'Sending your enquiry...',
          successTitle: 'Thank you - your enquiry has been received.',
          successBody: 'We will review the information and use your selected contact method to discuss the next step. Any assessment scope, fees and appointment time will be confirmed separately.',
          failure: 'Your enquiry could not be submitted. Please try again, or contact CMAXX by phone or WhatsApp. Your appointment has not been booked.'
        }
      : {
          summary: 'Please check the highlighted fields and try again.',
          sending: 'Sending your enquiry...',
          successTitle: 'Thank you.',
          successBody: 'Your enquiry has been sent to CMAXX WiFi Solutions. We will contact you to discuss the requirements and next steps. This does not confirm an appointment or final quotation.',
          failure: 'Your enquiry could not be sent. Please try again, or call or WhatsApp CMAXX using the contact options below.'
        };
  }

  setStatus(form, tone, title, body) {
    const box = form.querySelector('[data-status]');
    if (!box) return;
    box.className = 'cx-status' + (tone === 'warn' ? ' cx-status--warn' : '');
    box.innerHTML = '';
    if (title) { const h = document.createElement('h4'); h.textContent = title; box.appendChild(h); }
    if (body) { const p = document.createElement('p'); p.textContent = body; box.appendChild(p); }
  }

  onSubmit(e) {
    const form = e.target;
    if (!form || !form.matches || !form.matches('form[data-cx-form]')) return;
    e.preventDefault();
    const kind = form.getAttribute('data-cx-form');
    const msgs = this.formMessages(kind);
    const summary = form.querySelector('[data-summary]');
    summary.innerHTML = '';
    this.setStatus(form, '', '', '');

    const errors = this.validate(form);
    if (errors.length) {
      const h = document.createElement('h4');
      h.textContent = msgs.summary;
      const ul = document.createElement('ul');
      errors.forEach((er) => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = '#' + er.el.id;
        link.textContent = er.msg;
        li.appendChild(link);
        ul.appendChild(li);
      });
      summary.appendChild(h);
      summary.appendChild(ul);
      summary.focus();
      this.track('form_error', { form_id: form.id, error_count: errors.length });
      return;
    }

    const data = {};
    new FormData(form).forEach((v, k) => { data[k] = String(v).slice(0, 3000); });
    data.page = (this.activePage() || {}).getAttribute ? this.activePage().getAttribute('data-page') : '';
    data.form_context = form.getAttribute('data-context');

    if (!this.FORM_ENDPOINT) {
      this.setStatus(form, 'warn', 'Online enquiries are not connected yet',
        'Your enquiry has not been sent. Please call CMAXX on 010 140 3660 or use WhatsApp. Your details remain in the form, and no appointment has been booked.');
      return;
    }

    const btn = form.querySelector('button[type="submit"]');
    const label = btn.textContent;
    btn.disabled = true;
    btn.textContent = msgs.sending;
    fetch(this.FORM_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data)
    }).then((res) => {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      this.setStatus(form, '', msgs.successTitle, msgs.successBody);
      this.track('generate_lead', {
        form_id: form.id,
        page_type: data.page,
        service_interest: data.service || data.property_type || data.form_context,
        preferred_contact_channel: data.contact_method || 'phone'
      });
      form.reset();
    }).catch(() => {
      this.setStatus(form, 'warn', '', msgs.failure);
    }).finally(() => {
      btn.disabled = false;
      btn.textContent = label;
    });
  }

  // Analytics hook: no names, numbers, emails or message text are ever sent.
  track(event, params) {
    try {
      const page = this.activePage();
      const payload = Object.assign({ event, page_type: page ? page.getAttribute('data-page') : '' }, params || {});
      if (window.dataLayer && typeof window.dataLayer.push === 'function') window.dataLayer.push(payload);
    } catch (err) {}
  }

