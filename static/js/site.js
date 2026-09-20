// site.js — westendorptoegang.nl. Geen frameworks. Drie taken: toestemming en meting,
// het menu, en het formulier. Alles werkt ook zonder dit bestand (FAQ is <details>).
(function () {
  'use strict';
  var d = document;
  var C = window.WT_CONFIG || {};   // uit build.py: {tagActief, web3formsKey, adsLabelForm, adsLabelTel}

  // ---------- Toestemming (Consent Mode v2) ----------
  // De Google-tag staat alleen in de pagina als er een ID in CONFIG staat. Zonder tag: geen balk, niets meten.
  var heeftTag = typeof window.gtag === 'function';
  var balk = d.getElementById('consent');
  function lees() { try { return localStorage.getItem('consent'); } catch (e) { return null; } }
  function bewaar(v) { try { localStorage.setItem('consent', v); } catch (e) {} }
  function zetConsent(v) {
    if (!heeftTag) return;
    var s = v === 'granted' ? 'granted' : 'denied';
    gtag('consent', 'update', { ad_storage: s, ad_user_data: s, ad_personalization: s, analytics_storage: s });
  }
  function toonBalk() { if (balk) { balk.hidden = false; } }
  function verbergBalk() { if (balk) { balk.hidden = true; } }
  if (heeftTag && balk) {
    var keuze = lees();
    if (keuze === 'granted') zetConsent('granted');
    if (!keuze) toonBalk();
    balk.querySelectorAll('[data-consent]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-consent');
        bewaar(v); zetConsent(v); verbergBalk();
      });
    });
    d.querySelectorAll('[data-consent-open]').forEach(function (b) { b.addEventListener('click', toonBalk); });
  }
  function mag() { return heeftTag && lees() === 'granted'; }
  function meet(naam, params) { if (mag()) { try { gtag('event', naam, params || {}); } catch (e) {} } }

  // ---------- Conversie op de bedanktpagina, één keer per bezoek ----------
  if (/^\/bedankt\/?$/.test(location.pathname)) {
    var al = false;
    try { al = sessionStorage.getItem('form_submit') === '1'; sessionStorage.setItem('form_submit', '1'); } catch (e) {}
    if (!al) {
      meet('form_submit', { page_path: location.pathname });
      if (C.adsLabelForm && mag()) { try { gtag('event', 'conversion', { send_to: C.adsLabelForm }); } catch (e) {} }
    }
  }

  // ---------- Klikmeting: bellen, WhatsApp, CTA ----------
  d.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) {
      meet('tel_click', { page_path: location.pathname });
      if (C.adsLabelTel && mag()) { try { gtag('event', 'conversion', { send_to: C.adsLabelTel }); } catch (er) {} }
    } else if (href.indexOf('https://wa.me/') === 0) {
      meet('whatsapp_click', { page_path: location.pathname });
    } else if (a.hasAttribute('data-cta')) {
      meet('cta_click', { page_path: location.pathname, cta: a.getAttribute('data-cta') });
    }
  });

  // ---------- Video op klik: nooit autoplay, pas laden na de klik ----------
  d.querySelectorAll('[data-video]').forEach(function (fig) {
    var start = fig.querySelector('.video__start'), vid = fig.querySelector('video');
    if (!start || !vid) return;
    start.addEventListener('click', function () {
      start.hidden = true; vid.hidden = false; vid.load();
      var p = vid.play(); if (p && p.catch) p.catch(function () {});
      vid.focus();
    });
  });

  // ---------- Menu ----------
  var knop = d.getElementById('menu-knop'), nav = d.getElementById('nav');
  if (knop && nav) {
    knop.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      knop.setAttribute('aria-expanded', open ? 'true' : 'false');
      knop.querySelector('span').textContent = open ? 'Sluiten' : 'Menu';
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { knop.click(); knop.focus(); }
    });
  }

  // ---------- Formulier (Web3Forms, honeypot, tijdscheck, echte foutmeldingen) ----------
  d.querySelectorAll('form[data-aanvraag]').forEach(function (f) {
    var start = Date.now();
    var status = f.querySelector('.form-status');
    var teksten = {
      naam: 'Vul uw naam in.',
      plaats: 'Vul de plaats van het pand in.',
      contact: 'Vul een telefoonnummer of e-mailadres in, dan kunnen wij u bereiken.',
      email: 'Dit e-mailadres lijkt niet te kloppen. Controleer het @-teken en de punt.'
    };
    function zetFout(veld, tekst) {
      var wrap = veld.closest('.veld'); if (!wrap) return;
      var m = wrap.querySelector('.melding');
      if (tekst) { wrap.classList.add('fout'); if (m) m.textContent = tekst; veld.setAttribute('aria-invalid', 'true'); }
      else { wrap.classList.remove('fout'); veld.removeAttribute('aria-invalid'); }
    }
    function controleer() {
      var ok = true, eerste = null;
      var naam = f.elements.naam, tel = f.elements.telefoon, mail = f.elements.email, plaats = f.elements.plaats;
      zetFout(naam, ''); zetFout(tel, ''); zetFout(mail, ''); zetFout(plaats, '');
      if (!naam.value.trim()) { zetFout(naam, teksten.naam); ok = false; eerste = eerste || naam; }
      if (!tel.value.trim() && !mail.value.trim()) { zetFout(tel, teksten.contact); ok = false; eerste = eerste || tel; }
      if (mail.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim())) { zetFout(mail, teksten.email); ok = false; eerste = eerste || mail; }
      if (!plaats.value.trim()) { zetFout(plaats, teksten.plaats); ok = false; eerste = eerste || plaats; }
      if (eerste) eerste.focus();
      return ok;
    }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (status) { status.textContent = ''; status.className = 'form-status'; }
      if (!controleer()) return;
      if (f.elements.website && f.elements.website.value) return;            // honeypot: stil negeren
      if (Date.now() - start < 3000) {                                        // tijdscheck: sneller dan een mens
        if (status) { status.textContent = 'Controleer uw gegevens en verstuur opnieuw.'; status.className = 'form-status mis'; }
        return;
      }
      if (!C.web3formsKey || C.web3formsKey.indexOf('[[') === 0) {
        if (status) { status.textContent = 'Het formulier is nog niet gekoppeld. Bel ons of mail naar ' + (C.mail || 'ons e-mailadres') + '.'; status.className = 'form-status mis'; }
        return;
      }
      var knopje = f.querySelector('button[type="submit"]');
      if (knopje) { knopje.disabled = true; knopje.textContent = 'Versturen…'; }
      var data = new FormData(f);
      data.append('access_key', C.web3formsKey);
      data.append('subject', 'Inventarisatie-aanvraag via westendorptoegang.nl');
      data.append('from_name', 'westendorptoegang.nl');
      data.append('pagina', location.pathname);
      fetch('https://api.web3forms.com/submit', { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (r) {
          if (r && r.success) { location.href = '/bedankt/'; }
          else { throw new Error('mislukt'); }
        })
        .catch(function () {
          if (status) { status.textContent = 'Versturen is niet gelukt. Bel ons of probeer het later opnieuw.'; status.className = 'form-status mis'; }
          if (knopje) { knopje.disabled = false; knopje.textContent = C.cta || 'Verstuur aanvraag'; }
        });
    });
  });
})();
