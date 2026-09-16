/* =========================================================================
   N.J. Bothmann — Vorschau. Interaktion & Scroll-Choreografie.
   Abhängigkeiten: GSAP 3.12.5 + ScrollTrigger, Lenis 1.1.18 (beide per CDN).
   Fällt ohne diese Bibliotheken auf eine statische, voll benutzbare Seite zurück.
   ========================================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.remove('kein-js');

  var willWenig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hatGsap = !!(window.gsap && window.ScrollTrigger);
  var animiert = hatGsap && !willWenig;
  if (!animiert) root.classList.add('reduziert');

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ===================== Lenis + GSAP-Grundlage ===================== */
  var lenis = null;
  if (animiert) {
    gsap.registerPlugin(ScrollTrigger);
    if (window.Lenis) {
      lenis = new Lenis({ duration: 1.1, smoothWheel: true, touchMultiplier: 1.6 });
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    }
    ScrollTrigger.config({ ignoreMobileResize: true });
  }

  function scrolleZu(ziel) {
    if (lenis) lenis.scrollTo(ziel, { offset: -70 });
    else ziel.scrollIntoView({ behavior: 'auto', block: 'start' });
  }

  /* ===================== Brand-Intro (nur erster Besuch) ===================== */
  (function intro() {
    var schirm = $('.intro-schirm');
    if (!schirm) return;
    var gesehen = false;
    try { gesehen = sessionStorage.getItem('njb-intro') === '1'; } catch (e) { gesehen = false; }
    if (gesehen || !animiert) {
      schirm.hidden = true;
      return;
    }
    try { sessionStorage.setItem('njb-intro', '1'); } catch (e) {}
    document.body.style.overflow = 'hidden';
    if (lenis) lenis.stop();
    var tl = gsap.timeline({
      onComplete: function () {
        schirm.hidden = true;
        document.body.style.overflow = '';
        if (lenis) lenis.start();
        ScrollTrigger.refresh();
      }
    });
    tl.to($$('.intro-schirm__marke span'), { opacity: 1, y: 0, duration: .5, stagger: .035, ease: 'power3.out' }, 0)
      .to($('.intro-schirm__zeile'), { opacity: 1, duration: .45 }, .35)
      .to($('.intro-schirm__balken i'), { scaleX: 1, duration: .85, ease: 'power2.inOut' }, .3)
      .to(schirm, { opacity: 0, duration: .55, ease: 'power2.inOut' }, 1.25)
      .set(schirm, { pointerEvents: 'none' });
  })();

  /* ===================== Vorhang-Seitenübergang ===================== */
  (function vorhang() {
    var v = $('.vorhang');
    if (!v) return;
    // Der Vorhang deckt beim Laden die Seite ab. Er MUSS in jedem Fall wieder
    // freigegeben werden — auch wenn GSAP gar nicht geladen wurde. Sonst
    // schluckt er sämtliche Klicks.
    v.classList.remove('ist-zu');
    if (!animiert) { v.style.display = 'none'; return; }
    var latten = $$('.vorhang i');
    gsap.set(latten, { scaleY: 1, transformOrigin: '50% 0%' });
    gsap.to(latten, {
      scaleY: 0, duration: .55, ease: 'power3.inOut', stagger: .05,
      onComplete: function () { v.classList.remove('ist-zu'); }
    });

    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a') : null;
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (a.target === '_blank' || a.hasAttribute('download')) return;
      if (!href || href.charAt(0) === '#' || /^(mailto:|tel:|https?:)/i.test(href)) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      v.classList.add('ist-zu');
      gsap.set(latten, { transformOrigin: '50% 100%' });
      gsap.to(latten, {
        scaleY: 1, duration: .45, ease: 'power3.inOut', stagger: .045,
        onComplete: function () { window.location.href = href; }
      });
    });
  })();

  /* ===================== Kopfleiste, Fortschritt, Sticky-CTA ===================== */
  (function kopfleiste() {
    var kopf = $('.kopf');
    var balken = $('.fortschritt');
    var cta = $('.sticky-cta');
    var letzte = 0;

    function takt() {
      var y = window.scrollY || window.pageYOffset;
      var hoehe = document.documentElement.scrollHeight - window.innerHeight;
      if (kopf) {
        kopf.classList.toggle('ist-gescrollt', y > 24);
        var offen = document.body.classList.contains('menue-offen');
        kopf.classList.toggle('ist-weg', !offen && y > 460 && y > letzte + 6);
      }
      if (balken) balken.style.transform = 'scaleX(' + (hoehe > 0 ? Math.min(y / hoehe, 1) : 0) + ')';
      if (cta) cta.classList.toggle('ist-da', y > 700);
      letzte = y;
    }
    window.addEventListener('scroll', takt, { passive: true });
    takt();
  })();

  /* ===================== Mobiles Menü ===================== */
  (function menue() {
    var knopf = $('.burger');
    var feld = $('.menue');
    if (!knopf || !feld) return;
    var zuletzt = null;

    function setze(offen) {
      knopf.setAttribute('aria-expanded', String(offen));
      feld.classList.toggle('ist-offen', offen);
      feld.setAttribute('aria-hidden', String(!offen));
      document.body.classList.toggle('menue-offen', offen);
      document.body.style.overflow = offen ? 'hidden' : '';
      if (lenis) { offen ? lenis.stop() : lenis.start(); }
      if (offen) {
        zuletzt = document.activeElement;
        var erster = $('a', feld);
        if (erster) erster.focus();
      } else if (zuletzt) {
        zuletzt.focus();
      }
    }
    knopf.addEventListener('click', function () {
      setze(knopf.getAttribute('aria-expanded') !== 'true');
    });
    feld.addEventListener('click', function (e) {
      if (e.target.closest('a')) setze(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && knopf.getAttribute('aria-expanded') === 'true') setze(false);
    });
    // Fokus im offenen Menü halten
    feld.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var ziele = $$('a, button', feld).filter(function (el) { return el.offsetParent !== null; });
      if (!ziele.length) return;
      var erst = ziele[0], letzt = ziele[ziele.length - 1];
      if (e.shiftKey && document.activeElement === erst) { e.preventDefault(); letzt.focus(); }
      else if (!e.shiftKey && document.activeElement === letzt) { e.preventDefault(); erst.focus(); }
    });
    setze(false);
  })();

  /* ===================== Magnetische Buttons + 3D-Tilt ===================== */
  (function mikro() {
    if (!animiert || window.matchMedia('(hover: none)').matches) return;

    $$('[data-magnet]').forEach(function (el) {
      var x = gsap.quickTo(el, 'x', { duration: .5, ease: 'power3.out' });
      var y = gsap.quickTo(el, 'y', { duration: .5, ease: 'power3.out' });
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        x((e.clientX - r.left - r.width / 2) * .3);
        y((e.clientY - r.top - r.height / 2) * .38);
      });
      el.addEventListener('pointerleave', function () { x(0); y(0); });
    });

    $$('[data-tilt]').forEach(function (el) {
      var rx = gsap.quickTo(el, 'rotationX', { duration: .6, ease: 'power3.out' });
      var ry = gsap.quickTo(el, 'rotationY', { duration: .6, ease: 'power3.out' });
      gsap.set(el, { transformPerspective: 800, transformStyle: 'preserve-3d' });
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        ry(((e.clientX - r.left) / r.width - .5) * 11);
        rx((.5 - (e.clientY - r.top) / r.height) * 11);
      });
      el.addEventListener('pointerleave', function () { rx(0); ry(0); });
    });
  })();

  /* ===================== Reveal ===================== */
  (function reveal() {
    if (!animiert) return;
    $$('.auf').forEach(function (el) {
      gsap.to(el, {
        opacity: 1, y: 0, duration: .85, ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true }
      });
    });
  })();

  /* ===================== Leitungslinie zeichnen ===================== */
  (function leitung() {
    $$('.leitung').forEach(function (box) {
      var pfad = $('path', box);
      if (!pfad) return;
      var len = pfad.getTotalLength();
      box.style.setProperty('--laenge', len);
      if (!animiert) { pfad.style.strokeDashoffset = 0; return; }
      gsap.to(pfad, {
        strokeDashoffset: 0, ease: 'none',
        scrollTrigger: { trigger: box, start: 'top 80%', end: 'bottom 30%', scrub: .6 }
      });
      gsap.to($$('circle', box), {
        opacity: 1, scale: 1, duration: .4, stagger: .2, ease: 'back.out(2)',
        scrollTrigger: { trigger: box, start: 'top 70%', end: 'bottom 40%', scrub: .8 }
      });
    });
  })();

  /* ===================== HERO: 700vh Scroll-Through ===================== */
  (function hero() {
    var held = $('.hero');
    if (!held) return;
    var shots = $$('.shot', held);
    var zeilen = $$('.hero__zeile', held);
    var punkte = $$('.hero__punkt i', held);
    var zaehler = $('.hero__zaehler b', held);

    shots.forEach(function (s, i) { s.style.zIndex = String(i + 1); });

    if (!animiert) {
      shots.forEach(function (s) { s.classList.add('shot--aktiv'); });
      return;
    }

    // Startzustände je Blende
    shots.forEach(function (shot) {
      var art = shot.dataset.blende;
      if (art === 'maske') {
        gsap.set($('.maskwort', shot), { scale: 1.08, opacity: 1, backgroundSize: '150%' });
        gsap.set($('.maske__foto', shot), { opacity: 0 });
      } else if (art === 'lamellen') {
        $$('.lamelle', shot).forEach(function (l, i) {
          gsap.set(l, { yPercent: i % 2 === 0 ? -104 : 104 });
        });
      } else if (art === 'kacheln') {
        $$('.kachel', shot).forEach(function (k) {
          gsap.set(k, { scale: .22, opacity: 0, rotation: (Math.random() - .5) * 26 });
        });
      } else if (art === 'iris') {
        gsap.set($('.shot__bild', shot), { clipPath: 'circle(0% at 50% 50%)' });
      } else if (art === 'streifen') {
        $$('.streif', shot).forEach(function (s, i) {
          gsap.set(s, { xPercent: i % 2 === 0 ? -104 : 104 });
        });
      }
      gsap.set(shot, { autoAlpha: 0 });
    });
    gsap.set(zeilen, { autoAlpha: 0 });
    gsap.set($$('.wort', held), { opacity: 0, yPercent: 110, rotateX: -55 });

    var tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: held,
        start: 'top top',
        end: 'bottom bottom',
        scrub: .75,
        invalidateOnRefresh: true,
        onUpdate: function (st) {
          var p = st.progress * shots.length;
          var akt = Math.min(shots.length - 1, Math.floor(p));
          if (zaehler) zaehler.textContent = String(akt + 1).padStart(2, '0');
          punkte.forEach(function (b, i) {
            var v = i < akt ? 1 : (i === akt ? p - akt : 0);
            b.style.transform = 'scaleX(' + v + ')';
          });
        }
      }
    });

    shots.forEach(function (shot, i) {
      var t = i;                 // ein Takt je Aufnahme
      var art = shot.dataset.blende;
      var zeile = zeilen[i];
      var woerter = zeile ? $$('.wort', zeile) : [];
      // Fenster so gewählt, dass auch die längste Zeile (12 Wörter) den
      // Einlauf vollständig abschließt, kurz steht und erst dann ausläuft.
      // Einlauf-Ende  = ein + (n-1)*0.014 + 0.13
      // Auslauf-Ende  = aus + (n-1)*0.012 + 0.11   (muss < t+1.26 bleiben)
      var ein = art === 'maske' ? .42 : .26;
      var aus = art === 'maske' ? .80 : .70;

      tl.set(shot, { autoAlpha: 1 }, t);
      shot.classList.add('shot--aktiv');

      /* --- Blende auf: 0.00 → 0.30 --- */
      if (art === 'maske') {
        // Das Wort setzt sich, zieht dann durch den Betrachter hindurch und
        // übergibt an das volle Foto. Danach erst kommt der Text — so liegt
        // nie Schrift auf Schrift.
        tl.to($('.maskwort', shot), { scale: 1, backgroundSize: '108%', duration: .24 }, t)
          .to($('.maskwort', shot), { scale: 9, opacity: 0, duration: .2, ease: 'power2.in' }, t + .26)
          .to($('.maske__foto', shot), { opacity: 1, duration: .16 }, t + .30);
      } else if (art === 'lamellen') {
        tl.to($$('.lamelle', shot), { yPercent: 0, duration: .3, stagger: { each: .018, from: 'edges' } }, t);
      } else if (art === 'kacheln') {
        tl.to($$('.kachel', shot), {
          scale: 1, opacity: 1, rotation: 0, duration: .3,
          stagger: { each: .012, from: 'random' }
        }, t);
      } else if (art === 'iris') {
        tl.to($('.shot__bild', shot), { clipPath: 'circle(78% at 50% 50%)', duration: .3 }, t)
          .fromTo($('.blitz', shot), { opacity: .85 }, { opacity: 0, duration: .22 }, t + .02);
      } else if (art === 'streifen') {
        tl.to($$('.streif', shot), { xPercent: 0, duration: .3, stagger: { each: .022, from: 'start' } }, t);
      }

      /* --- Text ein: 0.30 → 0.46 (immer NACH der Blende) --- */
      if (zeile) {
        tl.set(zeile, { autoAlpha: 1 }, t + ein);
        tl.to(woerter, {
          opacity: 1, yPercent: 0, rotateX: 0,
          duration: .13, stagger: { each: .014 }, ease: 'power2.out'
        }, t + ein);

        /* --- Halten, dann Text vollständig aus, bevor die nächste Zeile beginnt --- */
        tl.to(woerter, {
          opacity: 0, yPercent: -110,
          duration: .11, stagger: { each: .012 }, ease: 'power2.in'
        }, t + aus);
        tl.set(zeile, { autoAlpha: 0 }, t + aus + .26);
      }

      /* --- leichte Eigenbewegung des Bildes, damit es nicht steht --- */
      var bilder = $$('.shot__bild, .lamelle img, .kachel img, .streif img', shot);
      if (bilder.length && art !== 'maske') {
        tl.fromTo(bilder, { scale: 1.04 }, { scale: 1.12, duration: 1 }, t);
      }
    });

    // Der Timeline-Gesamttakt entspricht der Anzahl Aufnahmen.
    tl.to({}, { duration: .001 }, shots.length);
  })();

  /* ===================== Gewerke-Kacheln: aus dem Raster ===================== */
  (function gewerke() {
    var feld = $('.gewerke');
    if (!feld || !animiert) return;
    var teile = $$('.gewerk', feld);
    gsap.fromTo(teile, {
      yPercent: function (i) { return 16 + i * 7; },
      xPercent: function (i) { return (i % 2 ? 1 : -1) * (8 + i * 2); },
      rotation: function (i) { return (i % 2 ? 1 : -1) * (3 + i); },
      opacity: 0
    }, {
      yPercent: 0, xPercent: 0, rotation: 0, opacity: 1,
      ease: 'power3.out',
      scrollTrigger: { trigger: feld, start: 'top 82%', end: 'top 32%', scrub: .7 }
    });
  })();

  /* ===================== Sticky-Storytelling ===================== */
  (function ablauf() {
    var schritte = $$('.schritt');
    var zahl = $('.ablauf__zahl');
    if (!schritte.length) return;
    if (!animiert) { schritte.forEach(function (s) { s.classList.add('ist-aktiv'); }); return; }
    schritte.forEach(function (s, i) {
      ScrollTrigger.create({
        trigger: s,
        start: 'top 62%',
        end: 'bottom 40%',
        onToggle: function (self) {
          s.classList.toggle('ist-aktiv', self.isActive);
          if (self.isActive && zahl) zahl.textContent = String(i + 1).padStart(2, '0');
        }
      });
    });
    schritte[0].classList.add('ist-aktiv');
  })();

  /* ===================== Vorher / Nachher ===================== */
  (function vorherNachher() {
    var box = $('.vn');
    if (!box) return;
    var knopf = $('.vn__knopf', box);
    var pos = 50;

    function setze(p) {
      pos = Math.max(0, Math.min(100, p));
      box.style.setProperty('--pos', pos + '%');
      if (knopf) knopf.setAttribute('aria-valuenow', Math.round(pos));
    }
    function ausEvent(e) {
      var r = box.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      setze((x / r.width) * 100);
    }
    var zieht = false;
    box.addEventListener('pointerdown', function (e) {
      zieht = true; box.setPointerCapture && box.setPointerCapture(e.pointerId); ausEvent(e);
    });
    box.addEventListener('pointermove', function (e) { if (zieht) ausEvent(e); });
    window.addEventListener('pointerup', function () { zieht = false; });
    if (knopf) {
      knopf.addEventListener('keydown', function (e) {
        var s = e.shiftKey ? 12 : 4;
        if (e.key === 'ArrowLeft')  { setze(pos - s); e.preventDefault(); }
        if (e.key === 'ArrowRight') { setze(pos + s); e.preventDefault(); }
        if (e.key === 'Home')       { setze(0); e.preventDefault(); }
        if (e.key === 'End')        { setze(100); e.preventDefault(); }
      });
    }
    setze(50);
    if (animiert) {
      gsap.fromTo(box, { '--pos': '12%' }, {
        '--pos': '88%', ease: 'none',
        scrollTrigger: { trigger: box, start: 'top 78%', end: 'bottom 22%', scrub: .8 }
      });
      box.addEventListener('pointerdown', function () {
        gsap.killTweensOf(box);
      });
    }
  })();

  /* ===================== Marquee ===================== */
  (function marquee() {
    var spur = $('.marquee__spur');
    if (!spur || !animiert) return;
    var breite = spur.scrollWidth / 2;
    gsap.set(spur, { x: 0 });
    var tw = gsap.to(spur, {
      x: -breite, duration: 26, ease: 'none', repeat: -1,
      modifiers: { x: function (x) { return (parseFloat(x) % breite) + 'px'; } }
    });
    ScrollTrigger.create({
      trigger: spur.parentNode,
      start: 'top bottom', end: 'bottom top',
      onUpdate: function (self) {
        tw.timeScale(self.direction === -1 ? -1.6 : 1.6);
      },
      onLeave: function () { tw.timeScale(1); },
      onLeaveBack: function () { tw.timeScale(1); }
    });
  })();

  /* ===================== 3D-Zitat ===================== */
  (function zitat() {
    var bq = $('.zitat blockquote');
    if (!bq || !animiert) return;
    var zeilen = $$('.zitat__zeile', bq);
    gsap.fromTo(bq, { rotationX: 22, rotationY: -9, y: 40 }, {
      rotationX: -8, rotationY: 5, y: -30, ease: 'none',
      scrollTrigger: { trigger: bq, start: 'top 90%', end: 'bottom 14%', scrub: .9 }
    });
    gsap.fromTo(zeilen, { opacity: 0, yPercent: 65 }, {
      opacity: 1, yPercent: 0, duration: .75, stagger: .1, ease: 'power3.out',
      scrollTrigger: { trigger: bq, start: 'top 78%', once: true }
    });
  })();

  /* ===================== Einsatzgebiet-Karte ===================== */
  (function gebiet() {
    var karte = $('.karte-svg');
    if (!karte) return;
    var anzeige = $('.gebiet__anzeige');
    var titel = anzeige ? $('h3', anzeige) : null;
    var text = anzeige ? $('p', anzeige) : null;
    var orte = $$('.ort', karte);

    function zeige(el) {
      orte.forEach(function (o) { o.classList.toggle('ist-aktiv', o === el); });
      if (titel) titel.textContent = el.dataset.ort || '';
      if (text) text.textContent = el.dataset.info || '';
    }
    orte.forEach(function (o) {
      o.setAttribute('tabindex', '0');
      o.setAttribute('role', 'button');
      o.addEventListener('mouseenter', function () { zeige(o); });
      o.addEventListener('focus', function () { zeige(o); });
      o.addEventListener('click', function () { zeige(o); });
      o.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); zeige(o); }
      });
    });
    var sitz = $('.ort--sitz', karte);
    if (sitz) zeige(sitz);

    var strecke = $('.strecke', karte);
    if (strecke) {
      var l = strecke.getTotalLength();
      karte.style.setProperty('--l', l);
      if (animiert) {
        gsap.to(strecke, {
          strokeDashoffset: 0, ease: 'none',
          scrollTrigger: { trigger: karte, start: 'top 82%', end: 'bottom 45%', scrub: .7 }
        });
      } else {
        strecke.style.strokeDashoffset = 0;
      }
    }
  })();

  /* ===================== Schaltschrank-Explorer ===================== */
  (function schrank() {
    var svg = $('.schrank svg');
    if (!svg) return;
    var feld = $('.schrank__text');
    if (!feld) return;
    var titel = $('h3', feld), text = $('p', feld);
    var module = $$('.modul', svg);
    function waehle(m) {
      module.forEach(function (x) { x.setAttribute('aria-pressed', String(x === m)); });
      if (titel) titel.textContent = m.dataset.titel || '';
      if (text) text.textContent = m.dataset.text || '';
    }
    module.forEach(function (m) {
      m.setAttribute('tabindex', '0');
      m.setAttribute('role', 'button');
      m.setAttribute('aria-pressed', 'false');
      m.addEventListener('click', function () { waehle(m); });
      m.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); waehle(m); }
      });
    });
    if (module.length) waehle(module[0]);
  })();

  /* ===================== Baujahr-Prüfung (Mini-Rechner) ===================== */
  (function pruefer() {
    var box = $('.pruefer');
    if (!box) return;
    var feld = $('input[type="number"]', box);
    var aus = $('.pruefer__ergebnis', box);
    if (!feld || !aus) return;
    var jetzt = new Date().getFullYear();

    function rechne() {
      var j = parseInt(feld.value, 10);
      if (!j || j < 1900 || j > jetzt) {
        aus.innerHTML = '<span class="leise">Bitte ein Baujahr zwischen 1900 und ' + jetzt + ' eintragen.</span>';
        return;
      }
      var alter = jetzt - j;
      var ampel, kopf, satz;
      if (alter >= 30) {
        ampel = 'rot'; kopf = 'Anlage ist ' + alter + ' Jahre alt.';
        satz = 'Für Heizkessel ab 30 Betriebsjahren greift nach § 72 Gebäudeenergiegesetz ein Betriebsverbot. Ausgenommen sind Niedertemperatur- und Brennwertkessel sowie bestimmte selbst genutzte Ein- und Zweifamilienhäuser. Welcher Fall vorliegt, steht auf dem Typenschild — das sehe ich mir vor Ort an.';
      } else if (alter >= 25) {
        ampel = 'gelb'; kopf = 'Anlage ist ' + alter + ' Jahre alt.';
        satz = 'In ' + (30 - alter) + ' Jahr(en) wird die 30-Jahre-Grenze des § 72 Gebäudeenergiegesetz erreicht. Jetzt ist ein guter Zeitpunkt, die Nachfolge zu planen statt sie im Winter entscheiden zu müssen.';
      } else {
        ampel = 'gruen'; kopf = 'Anlage ist ' + alter + ' Jahre alt.';
        satz = 'Die 30-Jahre-Grenze des § 72 Gebäudeenergiegesetz ist noch nicht in Sicht. Sinnvoll bleibt die regelmäßige Wartung — sie hält Verschleißteile im Griff, bevor sie ausfallen.';
      }
      aus.innerHTML = '<p><span class="ampel ampel--' + ampel + '"></span><b>' + kopf + '</b></p><p>' + satz + '</p>' +
        '<p class="leise" style="font-size:.85rem">Grobe Einordnung, keine Rechtsberatung und keine Prüfung des Einzelfalls.</p>';
    }
    feld.addEventListener('input', rechne);
    $$('.chip', box).forEach(function (c) {
      c.addEventListener('click', function () {
        feld.value = c.dataset.jahr;
        $$('.chip', box).forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        rechne();
      });
    });
    rechne();
  })();

  /* ===================== Checkliste mit Ring ===================== */
  (function check() {
    var box = $('.check');
    if (!box) return;
    var knoepfe = $$('.check__liste button', box);
    var fuell = $('.ring .fuell', box);
    var zahl = $('.ring text', box);
    if (!knoepfe.length || !fuell) return;
    var u = 2 * Math.PI * 42;
    fuell.setAttribute('stroke-dasharray', u);

    function mal() {
      var an = knoepfe.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; }).length;
      var q = an / knoepfe.length;
      fuell.setAttribute('stroke-dashoffset', u * (1 - q));
      if (zahl) zahl.textContent = an + '/' + knoepfe.length;
    }
    knoepfe.forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
        mal();
      });
    });
    mal();
  })();

  /* ===================== Zuständigkeits-Umschalter ===================== */
  (function umschalt() {
    var box = $('.umschalt');
    if (!box) return;
    var knoepfe = $$('.umschalt__knoepfe button', box);
    var felder = $$('.umschalt__feld', box);
    knoepfe.forEach(function (b, i) {
      b.addEventListener('click', function () {
        knoepfe.forEach(function (x, j) {
          x.setAttribute('aria-pressed', String(j === i));
          if (felder[j]) felder[j].hidden = j !== i;
        });
      });
    });
    knoepfe.forEach(function (b, i) {
      b.setAttribute('aria-pressed', String(i === 0));
      if (felder[i]) felder[i].hidden = i !== 0;
    });
  })();

  /* ===================== Grundriss (Rauchwarnmelder) ===================== */
  (function grundriss() {
    var svg = $('.grundriss');
    if (!svg) return;
    var aus = $('.grundriss-text');
    var raeume = $$('.raum', svg);
    function zeige(r) {
      raeume.forEach(function (x) { x.classList.toggle('ist-aktiv', x === r); });
      if (aus) aus.textContent = r.dataset.info || '';
    }
    raeume.forEach(function (r) {
      r.setAttribute('tabindex', '0');
      r.setAttribute('role', 'button');
      r.addEventListener('click', function () { zeige(r); });
      r.addEventListener('mouseenter', function () { zeige(r); });
      r.addEventListener('focus', function () { zeige(r); });
      r.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); zeige(r); }
      });
    });
    if (raeume.length) zeige(raeume[0]);
  })();

  /* ===================== FAQ-Suche ===================== */
  (function faq() {
    var feld = $('.faq__suche');
    if (!feld) return;
    var eintraege = $$('.faq details');
    var leer = $('.faq__leer');
    feld.addEventListener('input', function () {
      var q = feld.value.trim().toLowerCase();
      var treffer = 0;
      eintraege.forEach(function (d) {
        var passt = !q || d.textContent.toLowerCase().indexOf(q) !== -1;
        d.hidden = !passt;
        if (passt) treffer++;
        if (q && passt) d.open = true;
      });
      if (leer) leer.hidden = treffer > 0;
    });
  })();

  /* ===================== Kontaktformular ===================== */
  (function formular() {
    var form = $('form[data-form]');
    if (!form) return;

    // ?thema= vorwählen
    var thema = new URLSearchParams(window.location.search).get('thema');
    var wahl = $('#thema', form);
    if (thema && wahl) {
      var da = Array.prototype.some.call(wahl.options, function (o) { return o.value === thema; });
      if (da) wahl.value = thema;
    }

    function fehlerZu(el, text) {
      var box = el.parentNode.querySelector('.fehler');
      if (!box) { box = document.createElement('span'); box.className = 'fehler'; el.parentNode.appendChild(box); }
      box.textContent = text || '';
      el.setAttribute('aria-invalid', text ? 'true' : 'false');
      return !text;
    }

    function pruefe() {
      var ok = true;
      var name = $('#name', form);
      var mail = $('#email', form);
      var text = $('#nachricht', form);
      var zu = $('#zustimmung', form);
      if (name) ok = fehlerZu(name, name.value.trim().length < 2 ? 'Bitte Ihren Namen eintragen.' : '') && ok;
      if (mail) {
        var gut = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim());
        ok = fehlerZu(mail, gut ? '' : 'Bitte eine gültige E-Mail-Adresse eintragen.') && ok;
      }
      if (text) ok = fehlerZu(text, text.value.trim().length < 10 ? 'Bitte kurz beschreiben, worum es geht (mindestens 10 Zeichen).' : '') && ok;
      if (zu) ok = fehlerZu(zu, zu.checked ? '' : 'Ohne Zustimmung zur Datenschutzerklärung kann ich die Anfrage nicht bearbeiten.') && ok;
      return ok;
    }

    form.setAttribute('novalidate', 'novalidate');
    form.addEventListener('submit', function (e) {
      if (!pruefe()) {
        e.preventDefault();
        var erstes = form.querySelector('[aria-invalid="true"]');
        if (erstes) erstes.focus();
      }
    });
    $$('input, textarea, select', form).forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value) pruefe(); });
    });
  })();

  /* ===================== Karte erst auf Klick ===================== */
  (function karteAufKlick() {
    var feld = $('.kartenfeld');
    if (!feld) return;
    var knopf = $('button', feld);
    if (!knopf) return;
    knopf.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.setAttribute('title', 'Karte mit dem Standort Industriestraße 2, 52224 Stolberg, OpenStreetMap');
      f.setAttribute('loading', 'lazy');
      f.setAttribute('referrerpolicy', 'no-referrer');
      f.src = feld.dataset.karte;
      feld.innerHTML = '';
      feld.appendChild(f);
    });
  })();

  /* ===================== Anker sanft ===================== */
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var id = a.getAttribute('href');
    if (!id || id === '#') return;
    var ziel = document.querySelector(id);
    if (!ziel) return;
    e.preventDefault();
    scrolleZu(ziel);
    ziel.setAttribute('tabindex', '-1');
    ziel.focus({ preventScroll: true });
  });

  /* ===================== Nach Laden neu vermessen ===================== */
  if (animiert) {
    window.addEventListener('load', function () { ScrollTrigger.refresh(); });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
    }
  }
})();
