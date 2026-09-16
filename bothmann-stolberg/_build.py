#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator für die Vorschau-Website N.J. Bothmann, Stolberg.

Aufruf:  python3 _build.py
Erzeugt alle .html-Dateien sowie sitemap.xml im selben Ordner.
styles.css, main.js, fonts/ und img/ werden NICHT erzeugt, sondern gepflegt.

Grundsatz: Alle Inhalte stammen von der bestehenden Website des Betriebs
(http://www.bothmann-stolberg.de) oder aus benannten Rechtsquellen.
Nichts ist erfunden. Unbekanntes steht als "unbekannt" oder fehlt.
"""

import html
import os
import re

HIER = os.path.dirname(os.path.abspath(__file__))
V = "1"                       # Versionsnummer für styles.css / main.js
BASIS = "https://nilsc2308.github.io/Vorschau/bothmann-stolberg/"

# --------------------------------------------------------------------------
# Betriebsdaten — ausschließlich aus Impressum und Seiten des Betriebs
# --------------------------------------------------------------------------
B = {
    "name":      "N.J. Bothmann",
    "zusatz":    "Elektro · Heizung · Tankschutz",
    "inhaber":   "Norbert John Bothmann",
    "strasse":   "Industriestraße 2",
    "plz":       "52224",
    "ort":       "Stolberg",
    "tel":       "02402 20864",
    "tel_link":  "+492402208 64".replace(" ", ""),
    "fax":       "02402 20838",
    "mail":      "info@bothmann-stolberg.de",
    "ustid":     "DE183357143",
    "steuernr":  "202 / 5036 / 2022",
    "finanzamt": "Aachen-Kreis",
    "freistell": "00040442",
    "alt_url":   "http://www.bothmann-stolberg.de",
}

NAV = [
    ("leistung-elektrotechnik.html", "Elektrotechnik", "01"),
    ("leistung-heizungstechnik.html", "Heizungstechnik", "02"),
    ("leistung-tankschutz.html", "Tankschutz", "03"),
    ("ueber-uns.html", "Über den Betrieb", "04"),
    ("ratgeber.html", "Ratgeber", "05"),
    ("faq.html", "Fragen", "06"),
    ("kontakt.html", "Kontakt", "07"),
]

RECHT = [
    ("impressum.html", "Impressum"),
    ("datenschutz.html", "Datenschutz"),
]


def e(s):
    return html.escape(str(s), quote=True)


def woerter(text):
    """Zerlegt einen Satz in Wort-Spans. Leerzeichen bleiben im Span (white-space:pre),
    damit beim Einlaufen nie zwei Wörter aufeinander liegen."""
    teile = text.split(" ")
    out = []
    for i, w in enumerate(teile):
        raum = "" if i == len(teile) - 1 else " "
        out.append('<span class="wort">%s%s</span>' % (e(w), raum))
    return "".join(out)


def bild(name, alt, klasse="", groesse="(max-width: 700px) 100vw, 800px",
         lazy=True, w=800, h=600):
    return (
        '<img src="img/%s-800.webp" '
        'srcset="img/%s-400.webp 400w, img/%s-800.webp 800w" sizes="%s" '
        'width="%d" height="%d" alt="%s"%s decoding="async"%s>'
        % (name, name, name, e(groesse), w, h, e(alt),
           ' loading="lazy"' if lazy else '',
           ' class="%s"' % klasse if klasse else '')
    )


# --------------------------------------------------------------------------
# Gerüst
# --------------------------------------------------------------------------
def kopf(datei, titel, beschreibung, jsonld=None, vorlade=None, og_typ="website"):
    assert len(titel) <= 65, "Titel zu lang (%d): %s" % (len(titel), titel)
    assert len(beschreibung) <= 155, "Description zu lang (%d): %s" % (len(beschreibung), beschreibung)

    nav_html = "".join(
        '<a href="%s"%s>%s</a>' % (z, ' aria-current="page"' if z == datei else '', e(t))
        for z, t, _ in NAV
    )
    menue_html = "".join(
        '<a href="%s"%s>%s<em>%s</em></a>' % (z, ' aria-current="page"' if z == datei else '', e(t), n)
        for z, t, n in NAV
    )
    recht_html = " ".join('<a href="%s">%s</a>' % (z, e(t)) for z, t in RECHT)

    vor = ""
    if vorlade:
        vor = '<link rel="preload" as="image" href="%s" fetchpriority="high">' % vorlade

    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">%s</script>' % jsonld

    return f"""<!DOCTYPE html>
<html lang="de" class="kein-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<!-- VORSCHAU: Der Betrieb hat der Veröffentlichung noch nicht zugestimmt.
     Diese Zeile vor dem Livegang entfernen. -->
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{BASIS}{datei}">
<meta property="og:type" content="{og_typ}">
<meta property="og:site_name" content="{e(B['name'])} — {e(B['zusatz'])}">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:url" content="{BASIS}{datei}">
<meta property="og:image" content="{BASIS}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="de_DE">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#101217">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="fonts/space-grotesk-latin-wght-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/archivo-latin-wght-normal.woff2" crossorigin>
{vor}
<link rel="stylesheet" href="styles.css?v={V}">
{ld}
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="vorhang" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<div class="fortschritt" aria-hidden="true"></div>

<header class="kopf">
  <a class="wortmarke" href="index.html">
    <b>{e(B['name'])}</b>
    <span>{e(B['zusatz'])}</span>
  </a>
  <nav class="nav" aria-label="Hauptnavigation">{nav_html}</nav>
  <a class="kopf-cta" href="tel:{B['tel_link']}" data-magnet>
    <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>
    <span class="kopf-cta__nr">{e(B['tel'])}</span>
    <span class="sr-only">anrufen</span>
  </a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="hauptmenue">
    <span class="sr-only">Menü öffnen</span><i></i><i></i><i></i>
  </button>
</header>

<nav class="menue" id="hauptmenue" aria-label="Menü" aria-hidden="true">
  {menue_html}
  <div class="menue-fuss">
    <a href="tel:{B['tel_link']}">{e(B['tel'])}</a>
    <a href="mailto:{B['mail']}">{e(B['mail'])}</a>
    {recht_html}
  </div>
</nav>
"""


def intro_schirm():
    buchstaben = "".join(
        '<span>%s</span>' % (e(c) if c != " " else "&nbsp;")
        for c in "N.J. BOTHMANN"
    )
    return f"""<div class="intro-schirm" role="status" aria-label="Seite wird geladen">
  <div>
    <p class="intro-schirm__marke">{buchstaben}</p>
    <p class="intro-schirm__zeile">Elektro · Heizung · Tankschutz · Stolberg</p>
    <div class="intro-schirm__balken"><i></i></div>
  </div>
</div>
"""


def fuss(mit_sticky=True):
    leist = "".join('<li><a href="%s">%s</a></li>' % (z, e(t)) for z, t, _ in NAV[:3])
    seiten = "".join('<li><a href="%s">%s</a></li>' % (z, e(t)) for z, t, _ in NAV[3:])
    recht = "".join('<li><a href="%s">%s</a></li>' % (z, e(t)) for z, t in RECHT)

    sticky = ""
    if mit_sticky:
        sticky = f"""<div class="sticky-cta" aria-hidden="false">
  <p><strong>Störung oder Frage?</strong>{e(B['name'])}, {e(B['ort'])}</p>
  <div class="sticky-cta__zeile">
    <a class="btn btn--voll" href="tel:{B['tel_link']}">Anrufen</a>
    <a class="btn btn--linie" href="kontakt.html">Schreiben</a>
  </div>
</div>"""

    return f"""
<footer class="fuss">
  <div class="wrap">
    <div class="fuss__gitter">
      <div>
        <h2>Betrieb</h2>
        <p class="leise" style="margin:0">
          {e(B['name'])}<br>{e(B['zusatz'])}<br>
          {e(B['strasse'])}<br>{e(B['plz'])} {e(B['ort'])}
        </p>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul>
          <li><a href="tel:{B['tel_link']}">Telefon {e(B['tel'])}</a></li>
          <li><span class="leise">Fax {e(B['fax'])}</span></li>
          <li><a href="mailto:{B['mail']}">{e(B['mail'])}</a></li>
        </ul>
      </div>
      <div><h2>Leistungen</h2><ul>{leist}</ul></div>
      <div><h2>Seiten</h2><ul>{seiten}</ul></div>
      <div><h2>Rechtliches</h2><ul>{recht}</ul></div>
    </div>
    <p class="fuss__vorschau">
      <strong>Hinweis:</strong> Dies ist ein unverbindlicher Gestaltungsentwurf von
      Nils Cremerius für {e(B['name'])}. Der Betrieb hat der Veröffentlichung noch
      nicht zugestimmt. Inhalte, Kontaktdaten und Fotos stammen von
      <span class="leise">{e(B['alt_url'])}</span>. Die Seite ist auf
      <span class="leise">noindex</span> gesetzt und nicht über Suchmaschinen zu finden.
    </p>
    <div class="fuss__unten">
      <span>© {e(B['inhaber'])}, {e(B['ort'])}</span>
      <span>Entwurf: Nils Cremerius, Aachen</span>
    </div>
  </div>
</footer>
{sticky}
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js" defer></script>
<script src="main.js?v={V}" defer></script>
</body>
</html>
"""


def schreibe(datei, inhalt):
    pfad = os.path.join(HIER, datei)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(inhalt)
    return len(inhalt)


# --------------------------------------------------------------------------
# Wiederverwendbare Bausteine
# --------------------------------------------------------------------------
def leitung(hoehe=1200, knoten=4):
    """SVG-Leitungslinie: das Signature-Element der Seite."""
    schritt = hoehe / (knoten + 1)
    d = "M 20 0"
    kreise = []
    x = 20
    for i in range(knoten):
        y = schritt * (i + 1)
        neu = 4 if x == 20 else 20
        d += " L %d %d L %d %d" % (x, y - 26, neu, y - 26)
        d += " L %d %d" % (neu, y)
        kreise.append('<circle cx="%d" cy="%d" r="3.5"/>' % (neu, y))
        x = neu
    d += " L %d %d" % (x, hoehe)
    return ('<div class="leitung" aria-hidden="true">'
            '<svg viewBox="0 0 24 %d" preserveAspectRatio="none">'
            '<path d="%s"/>%s</svg></div>' % (hoehe, d, "".join(kreise)))


def cta_block(ueberschrift, text):
    return f"""<section class="abschnitt cta" id="cta">
  <div class="wrap">
    <p class="marke" style="color:rgba(255,255,255,.75)">Nächster Schritt</p>
    <h2 class="auf">{ueberschrift}</h2>
    <p class="auf">{text}</p>
    <div class="cta__zeile auf">
      <a class="btn btn--voll" href="tel:{B['tel_link']}" data-magnet>Telefon {e(B['tel'])}</a>
      <a class="btn btn--linie" href="kontakt.html" data-magnet>Anfrage schreiben</a>
    </div>
  </div>
</section>"""


def seitenkopf(typ, krume, titel, intro, extra=""):
    krume_html = ""
    if krume:
        teile = ['<a href="index.html">Start</a>']
        for z, t in krume:
            teile.append('<a href="%s">%s</a>' % (z, e(t)) if z else "<span>%s</span>" % e(t))
        krume_html = '<p class="krume">%s</p>' % '<span>/</span>'.join(teile)

    if typ == "geteilt":
        return f"""<header class="seitenkopf kopf--geteilt"><div class="wrap">{krume_html}
  <div class="kopf__gitter"><h1>{titel}</h1><div><p class="intro">{intro}</p>{extra}</div></div>
</div></header>"""
    if typ == "stapel":
        return f"""<header class="seitenkopf kopf--stapel"><div class="wrap">{krume_html}
  <h1>{titel}</h1><p class="intro">{intro}</p>{extra}
</div></header>"""
    if typ == "index":
        return f"""<header class="seitenkopf kopf--index"><div class="wrap">{krume_html}
  <p class="kopf__zahl" aria-hidden="true">{extra}</p><h1>{titel}</h1><p class="intro">{intro}</p>
</div></header>"""
    if typ == "artikel":
        return f"""<header class="seitenkopf kopf--artikel"><div class="wrap">{krume_html}
  <p class="kopf__meta">{extra}</p><h1>{titel}</h1><p class="intro">{intro}</p>
</div></header>"""
    if typ == "mitte":
        return f"""<header class="seitenkopf kopf--mitte"><div class="wrap">{krume_html}
  <h1>{titel}</h1><p class="intro">{intro}</p>{extra}
</div></header>"""
    return f"""<header class="seitenkopf kopf--knapp"><div class="wrap">{krume_html}
  <h1>{titel}</h1><p class="intro">{intro}</p>{extra}
</div></header>"""


# --------------------------------------------------------------------------
# HERO — 700vh-Scroll-Through mit fünf Blenden
# --------------------------------------------------------------------------
HERO_TEXTE = [
    ("Elektro, Heizung und Tankschutz aus einer Hand.",
     "N.J. Bothmann, Industriestraße 2 in Stolberg.", "unten"),
    ("Fünf Gewerke, ein Ansprechpartner.",
     "Elektrotechnik, Heizung, Sanitär, Klima, Tankschutz.", "mitte"),
    ("Wartung ohne Festpreis.",
     "Sie zahlen, was Ihre Anlage wirklich braucht.", "oben"),
    ("Stördienst auch für Kunden anderer Betriebe.",
     "Weil nicht jeder Betrieb einen eigenen unterhält.", "unten"),
    ("Fachbetrieb für Tankschutz.",
     "Montage, Überprüfung, Abnahme und Dichtheitsprüfung.", "mitte"),
]


def shot_maske(name, alt_text):
    return (
        '<div class="shot shot--maske" data-blende="maske" '
        'style="--maskbild:url(img/%s-800.webp)">'
        '<div class="maske__foto">%s<span class="korn"></span></div>'
        '<p class="maskwort" aria-hidden="true"><span>BOTH</span><span>MANN</span></p>'
        '</div>' % (name, bild(name, alt_text, klasse="shot__bild",
                               groesse="100vw", lazy=False, w=800, h=600))
    )


def shot_lamellen(name, alt, n=8):
    inner = "".join(
        '<div class="lamelle" style="--i:%d">%s</div>'
        % (i, bild(name, alt if i == 0 else "", groesse="100vw", w=800, h=600))
        for i in range(n)
    )
    return ('<div class="shot shot--lamellen" data-blende="lamellen">'
            '<div class="lamellen" style="--n:%d">%s</div>'
            '<span class="korn"></span></div>' % (n, inner))


def shot_kacheln(name, alt, sp=4, zl=3):
    inner = []
    for y in range(zl):
        for x in range(sp):
            erste = (x == 0 and y == 0)
            inner.append('<div class="kachel" style="--x:%d;--y:%d">%s</div>'
                         % (x, y, bild(name, alt if erste else "", groesse="100vw", w=800, h=600)))
    return ('<div class="shot shot--kacheln" data-blende="kacheln">'
            '<div class="kacheln" style="--sp:%d;--zl:%d">%s</div>'
            '<span class="korn"></span></div>' % (sp, zl, "".join(inner)))


def shot_iris(name, alt):
    return ('<div class="shot shot--iris" data-blende="iris">'
            '%s<span class="blitz"></span><span class="korn"></span></div>'
            % bild(name, alt, klasse="shot__bild", groesse="100vw", w=800, h=600))


def shot_streifen(name, alt, n=7):
    inner = "".join(
        '<div class="streif" style="--i:%d">%s</div>'
        % (i, bild(name, alt if i == 0 else "", groesse="100vw", w=800, h=600))
        for i in range(n)
    )
    return ('<div class="shot shot--streifen" data-blende="streifen">'
            '<div class="streifen" style="--n:%d">%s</div>'
            '<span class="korn"></span></div>' % (n, inner))


def hero():
    shots = "".join([
        shot_maske("montage-rohrleitung",
                   "Monteur bei Rohrleitungsarbeiten in einer Heizzentrale"),
        shot_lamellen("verteiler-armaturen", "Verteilerbalken mit Absperrarmaturen in einer Heizzentrale"),
        shot_kacheln("pelletkessel-paar", "Zwei Pelletkessel im Heizraum eines Referenzprojekts"),
        shot_iris("firmenfahrzeug", "Firmenfahrzeug von N.J. Bothmann mit Einblasschlauch bei der Pelletanlieferung"),
        shot_streifen("heizzentrale-2021", "Heizzentrale, Aufnahme aus dem Jahr 2021"),
    ])

    zeilen = "".join(
        '<p class="hero__zeile hero__zeile--%s" data-cap="%d">'
        '<span class="gross">%s</span><span class="klein">%s</span></p>'
        % (lage, i, woerter(gross), woerter(klein))
        for i, (gross, klein, lage) in enumerate(HERO_TEXTE)
    )

    punkte = "".join('<span class="hero__punkt"><i></i></span>' for _ in HERO_TEXTE)

    lese = " ".join("%s %s" % (a, b) for a, b, _ in HERO_TEXTE)

    return f"""<section class="hero" id="inhalt" aria-label="Bildstrecke aus dem Betrieb">
  <h1 class="sr-only">N.J. Bothmann — Elektro, Heizung und Tankschutz in Stolberg</h1>
  <p class="sr-only">{e(lese)}</p>
  <div class="hero__sticky">
    <div class="hero__buehne">{shots}</div>
    <div class="hero__texte" aria-hidden="true">{zeilen}</div>
    <div class="hero__kopf" aria-hidden="true">
      <p>Stolberg · Städteregion Aachen</p>
      <p class="hero__zaehler"><b>01</b> / 0{len(HERO_TEXTE)}</p>
    </div>
    <div class="hero__fuss" aria-hidden="true">{punkte}</div>
    <p class="hero__hinweis" aria-hidden="true"><i></i>Scrollen</p>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Sektionen der Startseite
# --------------------------------------------------------------------------
GEWERKE = [
    ("01", "Elektrotechnik", "leistung-elektrotechnik.html",
     "Von der Steckdose bis zur Gebäudetechnik: Zählerschrank, Unterverteilung, "
     "Beleuchtung, Jalousiesteuerung, Sprech- und Antennenanlagen.",
     '<path d="M13 2 4 15h7l-1 7 9-13h-7z"/>'),
    ("02", "Heizungstechnik", "leistung-heizungstechnik.html",
     "Gas, Öl, Holz, Solar und Wärmepumpe — dazu Hydraulik, Regelung und "
     "Wartungsverträge, die nach Aufwand statt nach Festpreis abrechnen.",
     '<path d="M12 22c4 0 7-3 7-7 0-4-5-6-4-13-4 2-6 5-6 8 0 2 1 3 1 4 0 1-1 2-2 2-1 0-2-1-2-3-2 2-1 9 6 9z"/>'),
    ("03", "Sanitärtechnik", "leistung-heizungstechnik.html#sanitaer",
     "Bad und Trinkwasser, gemeinsam mit Richter + Frenzel in Aachen als Partner "
     "für Planung und Ausstellung.",
     '<path d="M4 12h16M6 12v4a6 6 0 0 0 12 0v-4M9 12V5a2 2 0 0 1 4 0"/>'),
    ("04", "Klimatechnik", "leistung-heizungstechnik.html#klima",
     "Kühlen und Lüften als eigener Bereich des Betriebs, aufgeführt auf der "
     "bestehenden Website.",
     '<path d="M12 3v18M3 12h18M6 6l12 12M18 6 6 18"/>'),
    ("05", "Tankschutz", "leistung-tankschutz.html",
     "Fachbetrieb nach Wasserrecht: Montage, Überprüfung und Abnahme von "
     "Tankanlagen, Dichtheitsprüfung, Rückhaltewannen.",
     '<rect x="4" y="7" width="16" height="12" rx="2"/><path d="M8 7V5h8v2M8 13h8"/>'),
]


def s_gewerke():
    karten = "".join(
        f"""<a class="gewerk" href="{z}" data-tilt>
  <span class="gewerk__nr">{n}</span>
  <h3>{e(t)}</h3>
  <p>{e(txt)}</p>
  <svg class="gewerk__pikto" viewBox="0 0 24 24" aria-hidden="true">{p}</svg>
  <span class="gewerk__mehr">Ansehen →</span>
</a>"""
        for n, t, z, txt, p in GEWERKE
    )
    return f"""<section class="abschnitt" id="leistungen">
  {leitung(1100, 4)}
  <div class="wrap">
    <p class="marke">Was der Betrieb macht</p>
    <h2 class="auf" style="font-size:var(--fs-xxl);max-width:18ch">Fünf Gewerke, die im Haus ohnehin zusammengehören.</h2>
    <p class="auf leise" style="max-width:52ch;margin-top:1.2rem">
      Strom, Wärme, Wasser und der Öltank hängen im Keller am selben Punkt zusammen.
      Auf der bestehenden Website führt der Betrieb genau diese fünf Bereiche.
    </p>
    <div class="gewerke">{karten}</div>
  </div>
</section>"""


ABLAUF = [
    ("Schritt 01", "Sie rufen an",
     "Ein Anruf unter " + B["tel"] + " oder eine Nachricht über das Formular. "
     "Beschreiben Sie, was nicht funktioniert oder was geplant ist."),
    ("Schritt 02", "Wir sehen uns die Anlage an",
     "Vor Ort wird geprüft, was die Anlage wirklich braucht. Auf der bestehenden "
     "Website steht dazu: die Erfordernisse der Anlage zu erkennen und zu erfragen, "
     "gehört zur ersten Aufgabe."),
    ("Schritt 03", "Angebot oder direkte Ausführung",
     "Kleine Kundendienst-Einsätze werden direkt erledigt. Bei Montagen über "
     "500 Euro Angebotssumme wird eine Acontozahlung von 30 Prozent angefordert, "
     "danach wird der Auftrag ausgeführt."),
    ("Schritt 04", "Wartung oder Servicevertrag",
     "Auf Wunsch ein Servicevertrag ohne Festpreis. Ab zwei Jahren Laufzeit und "
     "zehn Tagen Zahlungsziel gibt der Betrieb einen Dauernachlass von fünf Prozent "
     "auf alle Arbeiten."),
]


def s_ablauf():
    schritte = "".join(
        f"""<div class="schritt">
  <span class="schritt__marke">{e(m)}</span>
  <h3>{e(t)}</h3><p>{e(txt)}</p>
</div>"""
        for m, t, txt in ABLAUF
    )
    return f"""<section class="abschnitt ablauf" id="ablauf">
  <div class="wrap">
    <div class="ablauf__gitter">
      <div class="ablauf__fix">
        <p class="marke">Ablauf</p>
        <h2 style="font-size:var(--fs-xl);max-width:14ch">Vom Anruf zur fertigen Anlage.</h2>
        <p class="ablauf__zahl" aria-hidden="true">01</p>
        <p class="leise" style="max-width:34ch">
          Alle Angaben in diesem Ablauf stehen so auf der bestehenden Website des
          Betriebs. Preise nennt diese Vorschau bewusst keine.
        </p>
      </div>
      <div class="ablauf__schritte">{schritte}</div>
    </div>
  </div>
</section>"""


def s_vorher_nachher():
    return f"""<section class="abschnitt" id="referenz">
  <div class="wrap">
    <p class="marke">Referenz aus der Galerie des Betriebs</p>
    <h2 class="auf" style="font-size:var(--fs-xl);max-width:20ch">Der Kessel, der raus musste. Und was danach da stand.</h2>
    <div class="vn" role="group" aria-label="Vergleich: Ausbau der Altanlage und fertige Anlage">
      {bild("anlage-fertig", "Fertige Heizungsanlage mit zwei Kesseln", groesse="(max-width: 900px) 100vw, 900px")}
      <div class="vn__oben">{bild("ausbau-altkessel", "Ausbau eines Altkessels im Heizraum", groesse="(max-width: 900px) 100vw, 900px")}</div>
      <span class="vn__schild vn__schild--l">Ausbau</span>
      <span class="vn__schild vn__schild--r">Fertig</span>
      <span class="vn__griff" aria-hidden="true"></span>
      <button class="vn__knopf" type="button" role="slider" aria-label="Vergleich verschieben"
              aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
        <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6-6 6 6 6M15 6l6 6-6 6"/></svg>
      </button>
    </div>
    <p class="leise" style="font-size:.85rem;margin-top:.9rem;max-width:64ch">
      Beide Aufnahmen stammen aus der Referenz-Galerie der bestehenden Website
      (Oktober 2008). Ziehen Sie den Griff oder nutzen Sie die Pfeiltasten.
    </p>
  </div>
</section>"""


MARQUEE = ["Zählerschrank", "Unterverteilung", "Rauchwarnmelder", "Brennwertkessel",
           "Pelletanlage", "Wärmepumpe", "Solarthermie", "Dichtheitsprüfung",
           "Rückhaltewanne", "Stördienst", "Blitzschutz", "Trinkwasserhygiene"]
MARQUEE_BILDER = ["rohrbuendel-kupfer", "schaltwand-messtechnik", "pumpengruppe",
                  "speicher-technikraum", "pelletlager-einblas"]


def s_marquee():
    teile = []
    for i, w in enumerate(MARQUEE):
        klasse = "marquee__wort marquee__wort--voll" if i % 3 == 0 else "marquee__wort"
        teile.append('<span class="%s">%s</span>' % (klasse, e(w)))
        if i % 3 == 2:
            n = MARQUEE_BILDER[(i // 3) % len(MARQUEE_BILDER)]
            teile.append(bild(n, "", klasse="marquee__bild", groesse="16rem"))
    spur = "".join(teile)
    return f"""<section class="marquee" aria-label="Leistungsband">
  <div class="marquee__spur" aria-hidden="true">{spur}{spur}</div>
</section>"""


def s_zitat():
    zeilen = [
        "„Warum soll ein Kunde mit einer",
        "modernen, einfach zu pflegenden",
        "Anlage die gleichen Kosten tragen",
        "wie der, der seine 30 Jahre alte",
        "Anlage am Leben erhalten will?“",
    ]
    inner = "".join('<span class="zitat__zeile">%s</span>' % e(z) for z in zeilen)
    return f"""<section class="abschnitt zitat">
  <div class="wrap zitat__buehne">
    <p class="marke">Aus der eigenen Website</p>
    <figure style="margin:0">
      <blockquote>{inner}</blockquote>
      <figcaption>
        <b>{e(B['inhaber'])}</b> — sinngemäß zitiert von der Seite „Leistungen“
        auf {e(B['alt_url'])}. Deshalb rechnet der Betrieb Wartungen nach Aufwand
        ab und nicht nach Festpreis.
      </figcaption>
    </figure>
  </div>
</section>"""


ORTE = [
    ("Stolberg", 150, 120, "sitz",
     "Sitz des Betriebs: Industriestraße 2, 52224 Stolberg. Hier laufen Anfragen, Kundendienst und Stördienst zusammen."),
    ("Aachen", 62, 96, "",
     "Die bestehende Website nennt Aachen ausdrücklich: der Betrieb ist Servicebetrieb der Firma Golling für die Region Aachen."),
    ("Eschweiler", 196, 60, "",
     "Nachbarstadt im Osten der Städteregion. Von Stolberg aus in wenigen Minuten erreichbar."),
    ("Würselen", 108, 44, "",
     "Nördliche Nachbarstadt in der Städteregion Aachen."),
    ("Mausbach", 214, 148, "",
     "Ortsteil von Stolberg. Unter der Werther Straße führen mehrere Verzeichnisse einen zweiten Eintrag des Betriebs."),
    ("Kornelimünster", 96, 178, "",
     "Südlicher Teil der Städteregion, im Tal der Inde."),
    ("Breinig", 176, 200, "",
     "Ortsteil von Stolberg im Süden des Stadtgebiets."),
]


def s_gebiet():
    punkte = []
    for name, x, y, art, info in ORTE:
        k = "ort ort--sitz" if art == "sitz" else "ort"
        r = 9 if art == "sitz" else 6
        anker = "middle"
        punkte.append(
            '<g class="%s" data-ort="%s" data-info="%s" aria-label="%s">'
            '<circle cx="%d" cy="%d" r="%d"/>'
            '<text x="%d" y="%d" text-anchor="%s">%s</text></g>'
            % (k, e(name), e(info), e(name), x, y, r, x, y + r + 14, anker, e(name))
        )
    strecke = "M 62 96 L 108 44 L 150 120 L 214 148 L 196 60 M 150 120 L 96 178 L 176 200"
    netz = "".join(
        '<path class="netz" d="M 0 %d H 280"/><path class="netz" d="M %d 0 V 250"/>' % (i * 50, i * 56)
        for i in range(1, 5)
    )
    return f"""<section class="abschnitt gebiet" id="gebiet">
  <div class="wrap">
    <div class="gebiet__gitter">
      <div>
        <p class="marke">Einsatzgebiet</p>
        <h2 class="auf" style="font-size:var(--fs-xl);max-width:16ch">Stolberg und die Städteregion Aachen.</h2>
        <svg class="karte-svg" viewBox="0 0 280 250" role="img"
             aria-label="Schematische Karte des Einsatzgebiets rund um Stolberg">
          <g aria-hidden="true">{netz}</g>
          <path class="strecke" d="{strecke}"/>
          {"".join(punkte)}
        </svg>
        <p class="leise" style="font-size:.82rem;margin-top:.8rem">
          Schematische Darstellung, keine maßstabsgetreue Karte. Die echte Karte
          öffnet sich auf der Kontaktseite erst nach einem Klick.
        </p>
      </div>
      <div class="gebiet__anzeige auf">
        <p class="marke" style="margin-bottom:.8rem">Ausgewählt</p>
        <h3>Stolberg</h3>
        <p></p>
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Startseite
# --------------------------------------------------------------------------
def ld_betrieb():
    return """{
 "@context": "https://schema.org",
 "@type": "Electrician",
 "@id": "%sindex.html#betrieb",
 "name": "N.J. Bothmann — Elektro · Heizung · Tankschutz",
 "alternateName": "Norbert John Bothmann",
 "url": "%sindex.html",
 "image": "%sog.jpg",
 "telephone": "+49 2402 20864",
 "faxNumber": "+49 2402 20838",
 "email": "info@bothmann-stolberg.de",
 "vatID": "DE183357143",
 "address": {
  "@type": "PostalAddress",
  "streetAddress": "Industriestraße 2",
  "postalCode": "52224",
  "addressLocality": "Stolberg",
  "addressRegion": "Nordrhein-Westfalen",
  "addressCountry": "DE"
 },
 "areaServed": [
  {"@type": "City", "name": "Stolberg"},
  {"@type": "City", "name": "Aachen"},
  {"@type": "City", "name": "Eschweiler"},
  {"@type": "City", "name": "Würselen"}
 ],
 "knowsAbout": ["Elektrotechnik", "Heizungstechnik", "Sanitärtechnik", "Klimatechnik", "Tankschutz"]
}""" % (BASIS, BASIS, BASIS)


def seite_index():
    kern = "".join([
        intro_schirm(),
        hero(),
        s_gewerke(),
        s_ablauf(),
        s_vorher_nachher(),
        s_marquee(),
        s_zitat(),
        s_gebiet(),
        cta_block(
            "Eine Anlage, ein Ansprechpartner.",
            "Rufen Sie an oder schreiben Sie kurz, worum es geht. "
            "Ein Rückruf ist meist schneller als jedes Formular."),
    ])
    return kopf(
        "index.html",
        "N.J. Bothmann — Elektro, Heizung und Tankschutz in Stolberg",
        "Elektrotechnik, Heizung, Sanitär, Klima und Tankschutz aus einer Hand. "
        "N.J. Bothmann, Industriestraße 2 in Stolberg. Telefon 02402 20864.",
        jsonld=ld_betrieb(),
        vorlade="img/montage-rohrleitung-800.webp",
    ) + kern + fuss()


# --------------------------------------------------------------------------
# Leistung 1 — Elektrotechnik (interaktiv: Schaltschrank-Explorer)
# --------------------------------------------------------------------------
MODULE = [
    ("Zählerschrank", "Hier kommt der Strom ins Haus. Zähler, Vorzählerbereich und "
     "Hauptleitungsabzweigklemmen gehören zu den Teilen, die nur ein eingetragener "
     "Elektrofachbetrieb anfassen darf."),
    ("Unterverteilung", "Von hier laufen die einzelnen Stromkreise ab: Licht, "
     "Steckdosen, Herd, Außenbeleuchtung. Die bestehende Website nennt "
     "Unterverteilungen ausdrücklich als Arbeitsbereich."),
    ("Sicherung", "Leitungsschutzschalter und Fehlerstromschutzschalter. "
     "„Einbaugeräte, Sicherungen, Schütze“ stehen so auf der Elektrotechnik-Seite "
     "des Betriebs."),
    ("Steuergerät", "Zeitsteuerung für Licht, Jalousien und Rollos. Auf der "
     "bestehenden Website: „Steuergeräte für fast alle Anwendungen“."),
    ("Blitzschutz", "Ein oft vernachlässigter Bereich. Der Betrieb hilft bei der "
     "Installationstechnik und holt für größere Anlagen einen spezialisierten "
     "Partner dazu."),
]


def schaltschrank_svg():
    reihen = []
    for i, (titel, text) in enumerate(MODULE):
        y = 22 + i * 46
        reihen.append(
            f"""<g class="modul" data-titel="{e(titel)}" data-text="{e(text)}" aria-label="{e(titel)}">
  <rect class="koerper" x="14" y="{y}" width="192" height="36" rx="2"/>
  <rect class="hebel" x="24" y="{y + 10}" width="10" height="16" rx="1"/>
  <text x="44" y="{y + 22}">{e(titel.upper())}</text>
</g>"""
        )
    return (
        '<svg viewBox="0 0 220 %d" role="group" aria-label="Schematischer Verteiler, '
        'Module zum Anklicken">'
        '<rect x="6" y="8" width="208" height="%d" rx="3" fill="none" stroke="#2C3342"/>'
        '%s</svg>' % (24 + len(MODULE) * 46 + 14, len(MODULE) * 46 + 10, "".join(reihen))
    )


def seite_elektro():
    inhalt = f"""{seitenkopf("geteilt",
        [(None, "Elektrotechnik")],
        "Elektrotechnik",
        "Von der Steckdose bis zur Gebäudetechnik. Die Texte auf dieser Seite folgen "
        "der bestehenden Website des Betriebs.",
        '<a class="btn btn--voll" href="kontakt.html?thema=elektrotechnik" data-magnet>Elektro-Anfrage</a>')}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  {leitung(900, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>Im Haus fängt es bei der einfachen Installation zur Stromversorgung an:
      Schalter, Steckdosen, Telefon, Fernsehen, Klingel. Man denkt über die Technik
      dahinter nicht nach, solange sie funktioniert.</p>

      <h2>Bei moderner Gebäudetechnik sieht das anders aus</h2>
      <p>Licht nach Zeitvorgabe oder nach Raumnutzung steuern. Energie nur dort
      einsetzen, wo sie gebraucht wird. Jalousien und Rollos automatisch fahren
      lassen. Türsprechanlage, Telefonanlage und mehrere Computer miteinander
      verbinden. Satellitenanlage oder Kabelanschluss in alle wichtigen Räume
      legen. Das eigene Eigentum absichern. Maschinen im Betrieb sicher mit Strom
      versorgen. Eine Außenbeleuchtung, die funktional ist und trotzdem wenig
      verbraucht.</p>
      <p><strong>Das funktioniert nicht mehr ganz so einfach — aber es funktioniert.</strong></p>
    </div>

    <h2 style="font-size:var(--fs-xl);margin-top:3.4rem">Was im Verteiler steckt</h2>
    <p class="leise" style="max-width:52ch">Klicken oder mit der Tastatur auswählen —
    jedes Modul erklärt sich selbst.</p>
    <div class="schrank">
      <div>{schaltschrank_svg()}</div>
      <div class="schrank__text" aria-live="polite">
        <p class="marke" style="margin-bottom:.8rem">Ausgewählt</p>
        <h3></h3><p></p>
      </div>
    </div>

    <div class="prosa" style="margin-top:3.4rem">
      <h2>Sicherheitstechnik</h2>
      <p>Videoüberwachung, Einbruchmeldeanlage, Brandmeldeanlage: im kleinen Bereich
      hilft der Betrieb selbst weiter. Größere Anlagen oder solche, die eine
      Zertifizierung verlangen, werden über einen Partner erstellt. Das steht so
      auf der bestehenden Website und ist in der Vorschau unverändert übernommen.</p>

      <h2>Rauchwarnmelder</h2>
      <p>Der Betrieb weist ein Zertifikat als Fachkraft für Rauchwarnmelder aus und
      unterstützt bei Auswahl, Montageort, Montage und Wartung — auch für einzelne
      Melder. Welche Pflichten in Nordrhein-Westfalen gelten, steht im
      <a href="ratgeber-rauchwarnmelder-nrw.html">Ratgeber-Beitrag zur
      Rauchwarnmelderpflicht</a>.</p>

      <h2>Blitzschutz</h2>
      <p>Nicht die Steckdosenleiste aus dem Baumarkt, sondern der Blitzschutz, der
      funktioniert. Bei der Installationstechnik hilft der Betrieb direkt; wo mehr
      nötig ist, kommt ein auf diesen Bereich spezialisierter Partner dazu.</p>

      <div class="hinweis">
        <b>Herstellerpartner laut bestehender Website:</b> Siemens, Gira, Berker,
        OBO, Hensel, Dehn, Tehalit, Ritto, Triax und Brumberg. Der Betrieb nutzt
        deren Schulungen und Fortbildungen.
      </div>
    </div>

    <div class="figur">
      {bild("schaltwand-messtechnik", "Schaltwand mit Messtechnik und Ausdehnungsgefäßen in einer Heizzentrale", groesse="(max-width: 900px) 100vw, 800px")}
      <figcaption>Schaltwand mit Messtechnik — Aufnahme aus der Referenz-Galerie des Betriebs.</figcaption>
    </div>
  </div>
</section>
{cta_block("Strom im Haus neu ordnen?",
           "Ob Zählerschrank, neue Stromkreise oder eine Steuerung für Licht und Jalousien — "
           "ein Anruf klärt schneller, was sinnvoll ist, als jede Beschreibung.")}
</main>"""
    return kopf(
        "leistung-elektrotechnik.html",
        "Elektrotechnik in Stolberg — N.J. Bothmann",
        "Zählerschrank, Unterverteilung, Steuerungen, Sprech- und Antennenanlagen, "
        "Rauchwarnmelder und Blitzschutz. Elektrofachbetrieb in Stolberg.",
    ) + inhalt + fuss()


# --------------------------------------------------------------------------
# Leistung 2 — Heizungstechnik (interaktiv: Baujahr-Prüfung)
# --------------------------------------------------------------------------
def pruefer_block(ueberschrift="Wie alt ist Ihre Heizung?"):
    jahre = [1988, 1995, 2002, 2012]
    chips = "".join(
        '<button type="button" class="chip" data-jahr="%d" aria-pressed="false">%d</button>' % (j, j)
        for j in jahre
    )
    return f"""<div class="pruefer">
  <h3 style="font-size:var(--fs-l);margin-bottom:.9rem">{e(ueberschrift)}</h3>
  <label for="baujahr">Baujahr des Wärmeerzeugers eintragen</label>
  <div class="pruefer__eingabe">
    <input type="number" id="baujahr" name="baujahr" min="1900" max="2026" step="1"
           inputmode="numeric" placeholder="1995" value="1995">
    <span class="leise">Steht meist auf dem Typenschild am Kessel.</span>
  </div>
  <div class="pruefer__schnell">{chips}</div>
  <div class="pruefer__ergebnis" aria-live="polite"></div>
</div>"""


def seite_heizung():
    inhalt = f"""{seitenkopf("stapel",
        [(None, "Heizungstechnik")],
        "Heizungstechnik, Sanitär und Klima",
        "Gas, Öl, Holz, Solar und Wärmepumpe. Dazu Hydraulik, Regelung und ein "
        "Wartungsvertrag, der nach Aufwand abrechnet statt nach Festpreis.",
        '<div class="kopf__meta"><span>Brennwert</span><span>Pellet</span>'
        '<span>Solarthermie</span><span>Wärmepumpe</span><span>Hydraulik</span></div>')}

<main id="inhalt">
<section class="abschnitt" style="padding-top:clamp(2.6rem,6vw,4rem)">
  {leitung(1000, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>Heizungstechnik ist ein Begriff, der frösteln lässt: früher wegen der
      schweren Kessel und Heizkörper, dann weil alles komplizierter wurde, und
      heute wegen der Kosten. Der Betrieb unterstützt bei der Suche nach einem
      geeigneten System — die Entscheidung nimmt er niemandem ab.</p>

      <h2>Zwei Punkte, die seit Jahren Fragen auslösen</h2>
      <ul class="aufzaehlung">
        <li>Die Austauschpflicht für Anlagen, die älter als 30 Jahre sind.</li>
        <li>Die ErP-Vorgabe zum Wegfall der klassischen Niedertemperaturkessel
        und die Verpflichtung zur Brennwerttechnik.</li>
      </ul>
      <p>Beides steht so auf der bestehenden Website des Betriebs. Ob es Ihre
      Anlage betrifft, hängt vom Typenschild ab — hier eine erste Einordnung:</p>
    </div>

    {pruefer_block()}

    <div class="prosa">
      <h2>Hydraulik geht auch einfach</h2>
      <p>Eines der größten Einsparpotenziale in Heizungsanlagen liegt in der
      Hydraulik. Pumpen, Regler und Dämmungen sind die eine Seite, das
      Nutzerverhalten die andere. Schon kleine Änderungen sparen spürbar — das ist
      die Kernaussage der bestehenden Heizungsseite.</p>

      <h2>Wartung ohne Festpreis</h2>
      <p>Ein üblicher Wartungsvertrag listet Tätigkeiten auf, die bei jeder Wartung
      zu erfolgen haben — auch wenn sie nicht immer erforderlich sind. Der Betrieb
      macht das anders: Die Serviceverträge enthalten eine Aufstellung der
      auszuführenden Arbeiten, aber <strong>keine Festpreise</strong>. Abgerechnet
      wird nach den feststehenden Stundenverrechnungssätzen zuzüglich Material und
      Nebenkosten.</p>

      <div class="fakten">
        <div class="fakt"><dt>Servicevertrag</dt><dd>ohne Festpreis</dd></div>
        <div class="fakt"><dt>Ab 2 Jahren Laufzeit</dt><dd>5 % Dauernachlass</dd></div>
        <div class="fakt"><dt>Voraussetzung</dt><dd>10 Tage Zahlungsziel</dd></div>
        <div class="fakt"><dt>Stördienst</dt><dd>auch für Fremdkunden</dd></div>
      </div>
      <p class="leise" style="font-size:.85rem">Alle vier Angaben stehen wörtlich auf
      der Seite „Leistungen“ der bestehenden Website. Konkrete Stundensätze nennt
      diese Vorschau nicht, weil sie dort nicht veröffentlicht sind.</p>
    </div>

    <div class="bildband" style="margin:3rem 0">
      {bild("kessel-modern-2021", "Moderner Heizkessel mit rotem Ausdehnungsgefäß, Aufnahme 2021")}
      {bild("pumpengruppe", "Pumpengruppe mit Absperrarmaturen")}
      {bild("speicher-technikraum", "Technikraum mit Pufferspeicher")}
      {bild("regelung-display", "Regelung mit Touch-Display", w=800, h=1067)}
    </div>

    <div class="prosa" id="sanitaer">
      <h2>Sanitärtechnik</h2>
      <p>Für das Bad arbeitet der Betrieb mit <strong>Richter + Frenzel in
      Aachen</strong> zusammen. Ein Termin vor Ort ist möglich — dort gibt es nicht
      nur Beratung, sondern auch Ideen, wie ein Badezimmer aussehen kann. Und
      meistens eine Tasse Kaffee.</p>
      <p>Für Betreiber von Trinkwasseranlagen weist der Betrieb ein Zertifikat zur
      Trinkwasserhygiene aus und empfiehlt die regelmäßige Untersuchung der
      Anlagen.</p>

      <h2 id="klima">Klimatechnik</h2>
      <p>Klimatechnik führt der Betrieb auf seiner Startseite als eigenen Bereich.
      Eine ausführliche Leistungsbeschreibung steht dort nicht — deshalb steht hier
      auch keine. Was konkret möglich ist, klärt am schnellsten ein Anruf.</p>

      <div class="hinweis">
        <b>Ehrlich bleiben:</b> Diese Vorschau erfindet keine Leistungen. Wo die
        bestehende Website schweigt, schweigt auch der Entwurf. Alles Weitere
        gehört in ein Gespräch mit dem Betrieb.
      </div>
    </div>
  </div>
</section>
{cta_block("Anlage prüfen lassen?",
           "Ein Blick auf das Typenschild und die Hydraulik sagt mehr als jede Ferndiagnose. "
           "Rufen Sie an — oder schreiben Sie kurz, welcher Kessel bei Ihnen steht.")}
</main>"""
    return kopf(
        "leistung-heizungstechnik.html",
        "Heizung, Sanitär und Klima in Stolberg — N.J. Bothmann",
        "Brennwert, Pellet, Solar und Wärmepumpe. Wartungsvertrag ohne Festpreis, "
        "5 % Dauernachlass ab zwei Jahren Laufzeit. Betrieb in Stolberg.",
    ) + inhalt + fuss()


# --------------------------------------------------------------------------
# Leistung 3 — Tankschutz (interaktiv: Checkliste mit Ring)
# --------------------------------------------------------------------------
CHECK_TANK = [
    "Der Tank steht in einer Auffangwanne oder einem abgemauerten Lagerraum.",
    "Das Grenzwertgeber-Kabel ist vorhanden und unbeschädigt.",
    "Am Tank sind keine feuchten Stellen, kein Ölgeruch im Raum.",
    "Die Sicherheitseinrichtungen und Armaturen wurden zuletzt geprüft.",
    "Für die Versorgungsleitungen liegt eine Dichtheitsprüfung vor.",
    "Die Prüfbescheinigung ist auffindbar und nicht abgelaufen.",
]


def seite_tankschutz():
    punkte = "".join(
        '<li><button type="button" aria-pressed="false">%s</button></li>' % e(t)
        for t in CHECK_TANK
    )
    inhalt = f"""{seitenkopf("index",
        [(None, "Tankschutz")],
        "Tankschutz",
        "Fachbetrieb nach Wasserrecht. Montage, Überprüfung und Abnahme von "
        "Tankanlagen, Dichtheitsprüfung von Versorgungsleitungen.",
        extra="03")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  {leitung(820, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>Ein Öltank ist der Teil der Anlage, der jahrzehntelang nichts tut — bis er
      etwas tut. Deshalb hängt am Tankschutz eine eigene Fachbetriebspflicht.</p>

      <h2>Was der Betrieb als Fachbetrieb anbietet</h2>
      <ul class="aufzaehlung">
        <li>Montage, Überprüfung und Abnahme von Tankanlagen</li>
        <li>Dichtheitsprüfung von Versorgungsleitungen</li>
        <li>Erstellung von Rückhaltewannen und Abmauerungen</li>
        <li>Schutzanstrich für gemauerte Lagerräume</li>
        <li>Überprüfung und Montage von Armaturen und Sicherheitseinrichtungen</li>
      </ul>
      <p>Diese Liste steht wörtlich auf der Seite „Leistungen“ der bestehenden
      Website. Dort ist die Fachbetriebseigenschaft mit <em>WHG § 19 l</em>
      angegeben — einer Vorschrift in der alten Zählung des Wasserhaushaltsgesetzes.
      Heute steht die Fachbetriebspflicht in § 62 WHG zusammen mit § 45 der
      Verordnung über Anlagen zum Umgang mit wassergefährdenden Stoffen (AwSV).
      Inhaltlich meint beides dasselbe; die Angabe gehört bei einem Livegang
      aktualisiert.</p>
    </div>

    <h2 style="font-size:var(--fs-xl);margin-top:3.2rem">Kurze Selbstprüfung am Tank</h2>
    <p class="leise" style="max-width:56ch">Haken Sie ab, was bei Ihnen zutrifft.
    Bleibt ein Punkt offen, lohnt der Anruf. Ersetzt keine Prüfung durch einen
    Fachbetrieb.</p>
    <div class="check">
      <ul class="check__liste">{punkte}</ul>
      <div>
        <svg class="ring" viewBox="0 0 100 100" role="img" aria-label="Fortschritt der Selbstprüfung">
          <circle class="bahn" cx="50" cy="50" r="42"/>
          <circle class="fuell" cx="50" cy="50" r="42" stroke-dashoffset="264"/>
          <text x="50" y="50">0/{len(CHECK_TANK)}</text>
        </svg>
      </div>
    </div>

    <div class="figur">
      {bild("kesselhaus-oel", "Kesselhaus mit Ölkessel und Lagerbehältern", groesse="(max-width: 900px) 100vw, 800px")}
      <figcaption>Kesselhaus aus der Referenz-Galerie des Betriebs.</figcaption>
    </div>

    <div class="prosa">
      <div class="hinweis">
        <b>Zum Weiterlesen:</b> Was die Fachbetriebspflicht praktisch bedeutet,
        steht im <a href="ratgeber-tankschutz-fachbetrieb.html">Ratgeber-Beitrag
        zum Tankschutz</a>.
      </div>
    </div>
  </div>
</section>
{cta_block("Prüfung fällig oder Unterlagen verschwunden?",
           "Der Betrieb ist Fachbetrieb für Tankanlagen. Ein Anruf klärt, was bei Ihrer Anlage ansteht.")}
</main>"""
    return kopf(
        "leistung-tankschutz.html",
        "Tankschutz in Stolberg — Fachbetrieb N.J. Bothmann",
        "Montage, Überprüfung und Abnahme von Tankanlagen, Dichtheitsprüfung, "
        "Rückhaltewannen und Armaturen. Fachbetrieb nach Wasserrecht in Stolberg.",
    ) + inhalt + fuss()


# --------------------------------------------------------------------------
# Über den Betrieb (interaktiv: Zuständigkeits-Umschalter)
# --------------------------------------------------------------------------
def seite_ueber():
    selbst = """<ul class="aufzaehlung">
      <li>Elektroinstallation im Haus: Schalter, Steckdosen, Stromkreise</li>
      <li>Zählerschrank, Unterverteilung, Einbaugeräte, Sicherungen, Schütze</li>
      <li>Steuergeräte für Licht, Jalousien und Rollos</li>
      <li>Rauchwarnmelder: Auswahl, Montageort, Montage, Wartung</li>
      <li>Heizungstechnik von Gas und Öl über Holz und Solar bis Wärmepumpe</li>
      <li>Tankschutz als Fachbetrieb nach Wasserrecht</li>
      <li>Stördienst — auch für Kunden, deren Betrieb keinen eigenen unterhält</li>
    </ul>"""
    partner = """<ul class="aufzaehlung">
      <li>Größere Sicherheitsanlagen und alles, was eine Zertifizierung verlangt</li>
      <li>Blitzschutz über die reine Installationstechnik hinaus</li>
      <li>Badplanung und Ausstellung: Richter + Frenzel in Aachen</li>
      <li>Service für Geräte der Firma Golling in der Region Aachen</li>
      <li>Vertretung im Urlaub: der Betrieb benennt dafür einen Ansprechpartner</li>
    </ul>
    <p class="leise" style="font-size:.88rem">So steht es auf der bestehenden
    Website. Der Betrieb sagt dort offen, wo er selbst arbeitet und wo er einen
    Partner dazu holt — das ist in diesem Entwurf unverändert übernommen.</p>"""

    inhalt = f"""{seitenkopf("geteilt",
        [(None, "Über den Betrieb")],
        "Ein Betrieb, der „ich“ sagt.",
        "Auf der bestehenden Website spricht nicht ein „Wir“ aus der Marketingabteilung, "
        "sondern durchgehend eine Person: Norbert John Bothmann.")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  {leitung(900, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>„Ich stehe Ihnen bei Planung, Ausführung und Wartung gerne zur Seite.“ —
      „Ich kann Ihnen keine Entscheidung abnehmen.“ — „Ich weise meine Kunden
      ausdrücklich darauf hin.“ Wer die bestehende Seiten des Betriebs liest,
      merkt schnell, dass hier jemand selbst schreibt und selbst haftet.</p>

      <h2>Was das praktisch heißt</h2>
      <p>Der Betrieb führt fünf Bereiche: Elektrotechnik, Heizungstechnik,
      Sanitärtechnik, Klimatechnik und Tankschutz. Er sagt dabei klar, wo er
      selbst arbeitet und wo er einen Partner hinzuzieht.</p>
    </div>

    <div class="umschalt">
      <div class="umschalt__knoepfe" role="group" aria-label="Zuständigkeit umschalten">
        <button type="button" class="chip" aria-pressed="true">Macht der Betrieb selbst</button>
        <button type="button" class="chip" aria-pressed="false">Macht ein Partner</button>
      </div>
      <div class="umschalt__feld"><h3>Im eigenen Haus</h3>{selbst}</div>
      <div class="umschalt__feld" hidden><h3>Mit Partnern</h3>{partner}</div>
    </div>

    <div class="prosa">
      <h2>Fortbildung statt Prospektwissen</h2>
      <p>Für die Gebäudetechnik arbeitet der Betrieb seit Jahren mit einem
      Hersteller zusammen, der eine wachsende Produktpalette abdeckt, und nutzt
      dessen Schulungen und Fortbildungen regelmäßig, um bei Technik und
      Neuerungen auf dem Laufenden zu bleiben.</p>

      <h2>Material vom Fachhandwerker</h2>
      <p>Zu billigem Material aus dem Internet schreibt der Betrieb offen: Nicht
      alles, was dort angeboten wird, ist schlecht — aber Garantie, Gewährleistung
      und Kulanz greifen bei den meisten Herstellern nur, wenn derselbe
      Handwerker geliefert und eingebaut hat und die Belege vorlegen kann. Manche
      Artikel sind für den deutschen Markt gar nicht zugelassen.</p>

      <h2>Auch die Urlaubszeit ist geregelt</h2>
      <p>Der Betrieb veröffentlicht, wann er nicht erreichbar ist, und benennt für
      diese Zeit einen Ansprechpartner — für Heizungsstörungen, Rohrbrüche,
      Probleme mit der Elektroinstallation und Schwierigkeiten mit der Öltankanlage.</p>
    </div>

    <div class="figur">
      {bild("team-vor-ort", "Zwei Personen an einer Verteilergruppe in der Heizzentrale", groesse="(max-width: 900px) 100vw, 800px")}
      <figcaption>Aufnahme aus der Referenz-Galerie der bestehenden Website.</figcaption>
    </div>

    <div class="prosa">
      <div class="hinweis">
        <b>Was diese Vorschau nicht weiß:</b> Gründungsjahr, Mitarbeiterzahl,
        Öffnungszeiten und Meistertitel sind auf der bestehenden Website nicht
        angegeben. Sie stehen deshalb hier auch nicht — erfundene Betriebsgeschichte
        gibt es in diesem Entwurf nicht.
      </div>
    </div>
  </div>
</section>
{cta_block("Lieber direkt fragen?",
           "Der kürzeste Weg zu einer Antwort ist ein Anruf. Wenn es warten kann, tut es auch das Formular.")}
</main>"""
    return kopf(
        "ueber-uns.html",
        "Über den Betrieb — N.J. Bothmann, Stolberg",
        "Ein Betrieb mit fünf Gewerken und einem Ansprechpartner. Was er selbst "
        "macht, wo er Partner hinzuzieht — ohne erfundene Betriebsgeschichte.",
    ) + inhalt + fuss()


# --------------------------------------------------------------------------
# Ratgeber
# --------------------------------------------------------------------------
ARTIKEL = [
    ("ratgeber-rauchwarnmelder-nrw.html", "Rauchwarnmelder in NRW",
     "Seit wann die Pflicht gilt, wer sie erfüllen muss und was bei der Wartung zählt.",
     "Elektrotechnik", "grundriss-rauchwarnmelder"),
    ("ratgeber-heizung-austauschpflicht.html", "Heizung über 30 Jahre",
     "Was das Gebäudeenergiegesetz verlangt — und welche Anlagen ausgenommen sind.",
     "Heizungstechnik", "baujahr-pruefung"),
    ("ratgeber-tankschutz-fachbetrieb.html", "Fachbetriebspflicht beim Öltank",
     "Warum an der Tankanlage nicht jeder arbeiten darf und welche Fristen laufen.",
     "Tankschutz", "fristen-liste"),
]


def seite_ratgeber():
    karten = "".join(
        f"""<a class="karte" href="{z}" data-tilt>
  <span class="karte__marke">{e(kat)}</span>
  <h3>{e(t)}</h3><p>{e(txt)}</p>
  <span class="gewerk__mehr" style="margin-top:auto">Lesen →</span>
</a>"""
        for z, t, txt, kat, _ in ARTIKEL
    )
    inhalt = f"""{seitenkopf("index",
        [(None, "Ratgeber")],
        "Ratgeber",
        "Drei Themen, die in Stolberg regelmäßig für Rückfragen sorgen. "
        "Sachlich, mit Angabe der Rechtsgrundlage — und ohne Verkaufsdruck.",
        extra="05")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  <div class="wrap">
    <h2 style="font-size:var(--fs-xl);max-width:20ch;margin-bottom:1.8rem">Drei Beiträge</h2>
    <div class="karten">{karten}</div>
    <div class="prosa" style="margin-top:3rem">
      <div class="hinweis">
        <b>Zum Charakter dieser Texte:</b> Sie geben den Stand der genannten
        Vorschriften im September 2026 allgemein wieder. Sie sind keine
        Rechtsberatung und ersetzen keine Prüfung des Einzelfalls. Verbindlich ist
        immer der Gesetzestext und das, was ein Fachbetrieb vor Ort feststellt.
      </div>
    </div>
  </div>
</section>
{cta_block("Frage zu einem der Themen?",
           "Kurz anrufen ist meist schneller als lange lesen. Die Nummer steht oben rechts.")}
</main>"""
    return kopf(
        "ratgeber.html",
        "Ratgeber — Rauchmelder, Heizung, Tankschutz | N.J. Bothmann",
        "Rauchwarnmelderpflicht in NRW, die 30-Jahre-Grenze für Heizkessel und die "
        "Fachbetriebspflicht beim Öltank — kurz erklärt, mit Rechtsgrundlage.",
    ) + inhalt + fuss()


def ld_artikel(datei, titel, beschreibung, datum="2026-09-16"):
    return """{
 "@context": "https://schema.org",
 "@type": "Article",
 "headline": "%s",
 "description": "%s",
 "datePublished": "%s",
 "dateModified": "%s",
 "inLanguage": "de-DE",
 "mainEntityOfPage": {"@type": "WebPage", "@id": "%s%s"},
 "author": {"@type": "Organization", "name": "N.J. Bothmann — Elektro · Heizung · Tankschutz"},
 "publisher": {"@id": "%sindex.html#betrieb"}
}""" % (titel.replace('"', "'"), beschreibung.replace('"', "'"), datum, datum, BASIS, datei, BASIS)


RAEUME = [
    ("Schlafzimmer", 12, 12, 78, 58, "Pflicht: In Schlafräumen schreibt § 47 der Landesbauordnung NRW mindestens einen Rauchwarnmelder vor."),
    ("Kinderzimmer", 98, 12, 78, 58, "Pflicht: Kinderzimmer sind Schlafräume im Sinne der Vorschrift — auch hier ist ein Melder vorgeschrieben."),
    ("Flur", 12, 78, 164, 34, "Pflicht: Flure, über die Rettungswege aus Aufenthaltsräumen führen, brauchen einen Melder."),
    ("Wohnzimmer", 12, 126, 100, 58, "Nicht vorgeschrieben, aber sinnvoll: Wohnräume fallen nicht unter die Pflicht. Viele Brände entstehen trotzdem hier."),
    ("Küche", 120, 126, 56, 58, "Kein Rauchwarnmelder: In Küchen lösen Kochdämpfe Fehlalarme aus. Wer dort absichern will, nimmt einen Hitzemelder."),
]


def grundriss_svg():
    teile = []
    for name, x, y, w, h, info in RAEUME:
        melder = ""
        if "Pflicht:" in info:
            melder = ('<g class="melder"><circle cx="%d" cy="%d" r="5"/>'
                      '<circle cx="%d" cy="%d" r="9" fill="none" stroke="#F2B21A" stroke-width="1.2" opacity=".55"/></g>'
                      % (x + w / 2, y + h / 2 - 8, x + w / 2, y + h / 2 - 8))
        teile.append(
            '<g class="raum" data-info="%s" aria-label="%s">'
            '<rect x="%d" y="%d" width="%d" height="%d" rx="2"/>'
            '<text x="%d" y="%d" text-anchor="middle">%s</text>%s</g>'
            % (e(info), e(name), x, y, w, h, x + w / 2, y + h - 10, e(name), melder)
        )
    return ('<svg class="grundriss" viewBox="0 0 188 196" role="group" '
            'aria-label="Schematischer Grundriss, Räume zum Anklicken">%s</svg>'
            % "".join(teile))


def seite_art_rauchmelder():
    datei = "ratgeber-rauchwarnmelder-nrw.html"
    titel = "Rauchwarnmelder in NRW: Pflicht, Räume, Wartung"
    besch = ("Seit 2013 gilt in Nordrhein-Westfalen die Rauchwarnmelderpflicht. "
             "Welche Räume betroffen sind und wer für die Wartung zuständig ist.")
    inhalt = f"""{seitenkopf("artikel",
        [("ratgeber.html", "Ratgeber"), (None, "Rauchwarnmelder")],
        "Rauchwarnmelder in NRW",
        "Zwei Fristen, drei Raumarten und eine Frage, die regelmäßig für Streit "
        "zwischen Mietern und Eigentümern sorgt.",
        extra="<span>Elektrotechnik</span><span>Lesezeit 4 Minuten</span><span>Stand September 2026</span>")}

<main id="inhalt">
<article class="abschnitt" style="padding-top:0">
  {leitung(760, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>Seit dem 1. April 2013 gilt auch in Nordrhein-Westfalen die
      Rauchwarnmelderpflicht. Für Neubau, Sanierung und Modernisierung galt sie
      sofort; bestehende Gebäude mussten bis spätestens 31. Dezember 2016
      nachgerüstet sein. Beide Daten nennt der Betrieb auf seiner eigenen Seite zum
      Thema — die Grundlage steht in § 47 der Landesbauordnung NRW.</p>

      <h2>Welche Räume betroffen sind</h2>
      <p>Die Pflicht trifft Schlafräume, Kinderzimmer und die Flure, über die
      Rettungswege aus Aufenthaltsräumen führen. Wohnzimmer und Küchen sind nicht
      erfasst. Klicken Sie im Grundriss auf einen Raum:</p>
    </div>

    {grundriss_svg()}
    <p class="grundriss-text leise" aria-live="polite" style="margin-top:.9rem;max-width:60ch"></p>

    <div class="prosa">
      <h2>Wer montiert, wer wartet</h2>
      <p>Für den Einbau ist in NRW der Eigentümer zuständig. Die Betriebsbereitschaft
      — also im Wesentlichen die Wartung — obliegt dem unmittelbaren Besitzer, meist
      also der Mieterin oder dem Mieter, sofern der Eigentümer diese Aufgabe nicht
      selbst übernommen hat. Genau an dieser Zweiteilung entstehen die meisten
      Rückfragen.</p>

      <h2>Warum ein Fachbetrieb</h2>
      <p>Der Betrieb weist ein <strong>Zertifikat als Fachkraft für
      Rauchwarnmelder</strong> aus und hilft bei der Auswahl geeigneter Geräte, der
      Festlegung der Montageorte und der Montage selbst. Auch die Wartung einzelner
      Melder übernimmt er.</p>

      <div class="hinweis">
        <b>Ein Hinweis, der Geld sparen kann:</b> Manche Gebäudeversicherungen
        machen eigene Vorgaben zu Meldern. Der Nachweis fachgerecht eingebauter und
        gewarteter Geräte kann sich positiv auf Beitrag oder Versicherungsschutz
        auswirken. Das steht so auf der bestehenden Website des Betriebs — was für
        Ihren Vertrag gilt, sagt Ihnen Ihre Versicherung.
      </div>

      <h2>Kurz zusammengefasst</h2>
      <ul class="aufzaehlung">
        <li>Pflicht seit 1. April 2013 für Neubau, Sanierung, Modernisierung</li>
        <li>Bestandsgebäude: nachzurüsten bis spätestens 31. Dezember 2016</li>
        <li>Betroffen: Schlafräume, Kinderzimmer, Rettungsweg-Flure</li>
        <li>Einbau: Eigentümer — Betriebsbereitschaft: unmittelbarer Besitzer</li>
        <li>Küche: kein Rauchwarnmelder, sondern gegebenenfalls ein Hitzemelder</li>
      </ul>
      <p class="leise" style="font-size:.85rem">Allgemeine Information nach dem
      Stand vom September 2026, keine Rechtsberatung. Maßgeblich ist der
      Gesetzestext.</p>
    </div>
  </div>
</article>
{cta_block("Melder montieren oder prüfen lassen?",
           "Der Betrieb übernimmt Auswahl, Montageort, Montage und Wartung — auch für einzelne Melder.")}
</main>"""
    return kopf(datei, titel, besch, jsonld=ld_artikel(datei, titel, besch),
                og_typ="article") + inhalt + fuss()


def seite_art_heizung():
    datei = "ratgeber-heizung-austauschpflicht.html"
    titel = "Heizung über 30 Jahre: Was das Gesetz verlangt"
    besch = ("Die 30-Jahre-Grenze nach § 72 Gebäudeenergiegesetz, die Ausnahmen für "
             "Brennwert- und Niedertemperaturkessel und was auf dem Typenschild steht.")
    inhalt = f"""{seitenkopf("artikel",
        [("ratgeber.html", "Ratgeber"), (None, "Heizung über 30 Jahre")],
        "Heizung über 30 Jahre",
        "Eine Zahl, die viele kennen — und drei Ausnahmen, die kaum jemand kennt.",
        extra="<span>Heizungstechnik</span><span>Lesezeit 5 Minuten</span><span>Stand September 2026</span>")}

<main id="inhalt">
<article class="abschnitt" style="padding-top:0">
  {leitung(820, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>„Heizungen, die älter als 30 Jahre sind, müssen raus.“ Der Satz stimmt in
      der Grundtendenz und ist in den Einzelheiten falsch. Die Regel steht in
      § 72 des Gebäudeenergiegesetzes (GEG) — und sie hat Ausnahmen, die für viele
      Häuser in Stolberg genau den Unterschied machen.</p>

      <h2>Die Regel</h2>
      <p>Heizkessel, die mit flüssigem oder gasförmigem Brennstoff beschickt werden
      und älter als 30 Jahre sind, dürfen nicht mehr betrieben werden. Gerechnet
      wird ab dem Einbau- beziehungsweise Aufstellungsjahr.</p>

      <h2>Die Ausnahmen</h2>
      <ul class="aufzaehlung">
        <li><strong>Brennwertkessel</strong> sind von der Regel ausgenommen.</li>
        <li><strong>Niedertemperaturkessel</strong> mit besonders hohem
        Wirkungsgrad sind ebenfalls ausgenommen.</li>
        <li>Für <strong>selbst genutzte Ein- und Zweifamilienhäuser</strong> gilt
        eine eigene Regelung, wenn die Eigentümerin oder der Eigentümer das Haus
        bereits am 1. Februar 2002 selbst bewohnt hat. Bei einem Eigentümerwechsel
        läuft dann eine eigene Frist.</li>
      </ul>
      <p>Welcher Kesseltyp bei Ihnen steht, verrät das Typenschild. Genau deshalb
      ist die Frage nicht aus der Ferne zu beantworten.</p>
    </div>

    {pruefer_block("Grobe Einordnung nach Baujahr")}

    <div class="prosa">
      <h2>Was der Betrieb dazu sagt</h2>
      <p>Auf der bestehenden Website nennt der Betrieb seit Jahren zwei Punkte mit
      zusätzlichem Informationsbedarf: die Austauschpflicht für Anlagen über
      30 Jahre und die ErP-Vorgabe, nach der klassische Niedertemperaturkessel
      entfallen und Brennwerttechnik einzusetzen ist — bei Neuanlagen ebenso wie
      beim Austausch bestehender Anlagen. Ausnahmen seien im Einzelfall zu prüfen.</p>

      <h2>Der unterschätzte Hebel: Hydraulik</h2>
      <p>Eines der größten Einsparpotenziale liegt nicht im Kessel, sondern in der
      Hydraulik: Pumpen, Regler, Dämmung — und das Nutzerverhalten. Schon kleine
      Änderungen sparen spürbar. Wer ohnehin über einen Austausch nachdenkt, sollte
      diesen Teil mitplanen statt ihn später nachzuschieben.</p>

      <div class="hinweis">
        <b>Vorsicht bei Zahlen aus dem Netz:</b> Einsparungen in Prozent hängen vom
        Haus, der Dämmung, dem Nutzerverhalten und dem Brennstoffpreis ab. Diese
        Seite nennt deshalb keine. Wer Ihnen eine exakte Zahl nennt, ohne Ihre
        Anlage gesehen zu haben, rät.
      </div>
      <p class="leise" style="font-size:.85rem">Allgemeine Information nach dem
      Stand vom September 2026, keine Rechtsberatung und keine Prüfung des
      Einzelfalls.</p>
    </div>
  </div>
</article>
{cta_block("Typenschild fotografieren und anrufen.",
           "Mit Kesseltyp und Baujahr lässt sich in zwei Minuten sagen, ob § 72 GEG Sie überhaupt betrifft.")}
</main>"""
    return kopf(datei, titel, besch, jsonld=ld_artikel(datei, titel, besch),
                og_typ="article") + inhalt + fuss()


FRISTEN = [
    ("Beim Einbau", "Anlagen zum Umgang mit wassergefährdenden Stoffen dürfen nur von Fachbetrieben errichtet, innen gereinigt, instand gehalten, instand gesetzt und stillgelegt werden."),
    ("Vor Inbetriebnahme", "Prüfpflichtige Anlagen werden vor der Inbetriebnahme durch einen Sachverständigen geprüft."),
    ("Wiederkehrend", "Je nach Größe, Gefährdungsstufe und Standort gelten wiederkehrende Prüfintervalle. Welche für Ihre Anlage gelten, hängt vom Einzelfall ab."),
    ("Bei Änderung", "Wesentliche Änderungen an der Anlage lösen eine erneute Prüfpflicht aus."),
    ("Bei Stilllegung", "Auch die Stilllegung gehört zu den Tätigkeiten, die dem Fachbetrieb vorbehalten sind."),
]


def seite_art_tank():
    datei = "ratgeber-tankschutz-fachbetrieb.html"
    titel = "Fachbetriebspflicht beim Öltank — kurz erklärt"
    besch = ("Warum an einer Öltankanlage nicht jeder arbeiten darf: § 62 WHG, "
             "§ 45 AwSV und was das für Hauseigentümer praktisch bedeutet.")
    liste = "".join(
        f"""<details><summary>{e(t)}</summary><div>{e(txt)}</div></details>"""
        for t, txt in FRISTEN
    )
    inhalt = f"""{seitenkopf("artikel",
        [("ratgeber.html", "Ratgeber"), (None, "Fachbetriebspflicht")],
        "Fachbetriebspflicht beim Öltank",
        "Ein Öltank ist rechtlich kein Behälter, sondern eine Anlage zum Umgang mit "
        "wassergefährdenden Stoffen. Das ändert alles.",
        extra="<span>Tankschutz</span><span>Lesezeit 4 Minuten</span><span>Stand September 2026</span>")}

<main id="inhalt">
<article class="abschnitt" style="padding-top:0">
  {leitung(760, 3)}
  <div class="wrap">
    <div class="prosa">
      <p>Heizöl ist wassergefährdend. Deshalb steht eine Öltankanlage nicht unter
      dem Heizungsrecht, sondern unter dem Wasserrecht — und dort gilt eine
      Fachbetriebspflicht. Geregelt ist sie in § 62 des Wasserhaushaltsgesetzes
      (WHG) zusammen mit § 45 der Verordnung über Anlagen zum Umgang mit
      wassergefährdenden Stoffen (AwSV).</p>

      <h2>Was das heißt</h2>
      <p>Errichten, innen reinigen, instand halten, instand setzen und stilllegen
      darf solche Anlagen nur ein zugelassener Fachbetrieb. Ein Heimwerker, ein
      Hausmeisterdienst oder ein Betrieb ohne diese Zulassung darf es nicht — auch
      dann nicht, wenn er es technisch könnte.</p>

      <h2>Wann etwas ansteht</h2>
      <p class="leise">Die Punkte aufklappen für die Einzelheiten.</p>
    </div>

    <div class="faq" style="margin-top:1.4rem">{liste}</div>

    <div class="prosa">
      <h2>Der Betrieb ist Fachbetrieb</h2>
      <p>N.J. Bothmann führt den Tankschutz als eigenen Bereich und bietet Montage,
      Überprüfung und Abnahme von Tankanlagen, die Dichtheitsprüfung von
      Versorgungsleitungen, die Erstellung von Rückhaltewannen und Abmauerungen,
      Schutzanstriche für gemauerte Lagerräume sowie die Überprüfung und Montage
      von Armaturen und Sicherheitseinrichtungen an.</p>

      <div class="hinweis">
        <b>Zur Zählung der Paragrafen:</b> Die bestehende Website nennt
        „Fachbetrieb nach WHG § 19 l“. Das ist die alte Nummerierung des
        Wasserhaushaltsgesetzes. Inhaltlich entspricht sie der heutigen Regelung in
        § 62 WHG und § 45 AwSV. Für einen Livegang gehört die Angabe aktualisiert —
        an der Fachbetriebseigenschaft selbst ändert das nichts.
      </div>

      <p>Zusätzlich hat der Betrieb auf die Änderungen zur Heizöllagerung und zur
      Fachbetriebspflicht hingewiesen, die ab August 2017 gelten.</p>
      <p class="leise" style="font-size:.85rem">Allgemeine Information nach dem
      Stand vom September 2026, keine Rechtsberatung. Welche Pflichten und
      Intervalle für Ihre Anlage konkret gelten, hängt von Größe, Gefährdungsstufe
      und Standort ab.</p>
    </div>

    <div class="figur">
      {bild("pelletlager-einblas", "Einblasstutzen und Leitungen am Lagerraum", groesse="(max-width: 900px) 100vw, 800px")}
      <figcaption>Lageranbindung aus der Referenz-Galerie des Betriebs.</figcaption>
    </div>
  </div>
</article>
{cta_block("Unklar, was bei Ihrer Anlage dran ist?",
           "Der Betrieb ist Fachbetrieb für Tankanlagen und sagt Ihnen, welche Prüfung ansteht.")}
</main>"""
    return kopf(datei, titel, besch, jsonld=ld_artikel(datei, titel, besch),
                og_typ="article") + inhalt + fuss()


# --------------------------------------------------------------------------
# FAQ
# --------------------------------------------------------------------------
FRAGEN = [
    ("Welche Gewerke deckt der Betrieb ab?",
     "Elektrotechnik, Heizungstechnik, Sanitärtechnik, Klimatechnik und Tankschutz. "
     "Diese fünf Bereiche führt der Betrieb auf seiner Startseite."),
    ("Gibt es einen Stördienst?",
     "Ja. Der Stördienst soll zunächst Kunden mit Servicevertrag eine kurzfristige "
     "Beseitigung von Notfällen sichern. Da nicht alle Betriebe aus Heizung, Sanitär "
     "und Elektro einen eigenen Stördienst unterhalten, steht das Angebot aber allen "
     "Kunden offen."),
    ("Wie wird der Stördienst abgerechnet?",
     "Eigene Servicekunden zahlen nach Rechnungsstellung durch den Betrieb. Kunden, "
     "die nachweislich bei einem Partnerbetrieb geführt werden, erhalten ihre "
     "Rechnung von dort. Fremdkunden zahlen nach Beendigung des Einsatzes vor Ort."),
    ("Was kostet ein Wartungsvertrag?",
     "Einen Festpreis gibt es bewusst nicht. Die Serviceverträge enthalten eine "
     "Aufstellung der auszuführenden Arbeiten, abgerechnet wird nach den "
     "feststehenden Stundenverrechnungssätzen zuzüglich Material und Nebenkosten. "
     "Die Sätze selbst sind nicht veröffentlicht — danach fragen Sie am besten direkt."),
    ("Gibt es einen Nachlass bei längerer Laufzeit?",
     "Ja. Bei einem Servicevertrag mit mindestens zwei Jahren Laufzeit und einem "
     "Zahlungsziel von zehn Tagen gewährt der Betrieb einen Dauernachlass von "
     "fünf Prozent auf alle Arbeiten."),
    ("Wie läuft die Abrechnung bei einer Montage?",
     "Montagearbeiten werden nach Aufwand und Materialeinsatz abgerechnet. "
     "Übersteigt die Rechnungssumme im Angebot 500 Euro, wird eine Acontozahlung "
     "von 30 Prozent der Auftragssumme angefordert; nach Zahlungseingang wird der "
     "Auftrag ausgeführt. Zahlungsziel: acht Tage nach Rechnungsstellung."),
    ("Und beim Kundendienst?",
     "Kundendiensteinsätze werden, soweit nicht anders vereinbart, vor Ort "
     "abgerechnet. Übersteigt der Auftragswert 250 Euro, wird nach Montagebericht "
     "eine Rechnung erstellt, fällig innerhalb von acht Tagen."),
    ("Kann ich Material selbst im Internet kaufen?",
     "Sie können — der Betrieb rät aber ausdrücklich ab. Garantie, Gewährleistung "
     "und Kulanz erfüllen die meisten Hersteller nur, wenn derselbe Handwerker "
     "geliefert und eingebaut hat und die Belege vorlegen kann. Manche Artikel sind "
     "für den deutschen Markt nicht zugelassen oder entsprechen als Re-Import nicht "
     "den hier geltenden Vorschriften."),
    ("Montiert der Betrieb auch einzelne Rauchwarnmelder?",
     "Ja. Der Betrieb weist ein Zertifikat als Fachkraft für Rauchwarnmelder aus und "
     "hilft bei Auswahl, Montageort und Montage — und übernimmt auch die Wartung "
     "einzelner Melder."),
    ("Macht der Betrieb große Alarmanlagen?",
     "Im kleinen Bereich hilft er selbst weiter. Größere Anlagen oder solche, die "
     "eine Zertifizierung erfordern, werden durch einen zuverlässigen Partner "
     "erstellt. Das sagt der Betrieb auf seiner Elektrotechnik-Seite selbst."),
    ("Wer ist im Urlaub erreichbar?",
     "Der Betrieb veröffentlicht, wann er nicht erreichbar ist, und benennt für "
     "diese Zeit einen Ansprechpartner — für Heizungsstörungen, Rohrbrüche, "
     "Probleme mit der Elektroinstallation und Öltankanlagen."),
    ("Welche Anschrift stimmt?",
     "Impressum und Datenschutzerklärung nennen die Industriestraße 2 in 52224 "
     "Stolberg. Die Seite „Karte / Anschrift“ und mehrere Branchenverzeichnisse "
     "nennen die Werther Straße 2. Diese Vorschau verwendet die Impressums-Anschrift. "
     "Welche die richtige ist, klärt am besten ein Anruf."),
]


def ld_faq():
    eintraege = ",\n".join(
        '  {"@type": "Question", "name": %s, "acceptedAnswer": {"@type": "Answer", "text": %s}}'
        % (json_str(f), json_str(a)) for f, a in FRAGEN
    )
    return '{\n "@context": "https://schema.org",\n "@type": "FAQPage",\n "mainEntity": [\n%s\n ]\n}' % eintraege


def json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def seite_faq():
    liste = "".join(
        f"""<details><summary>{e(f)}</summary><div>{e(a)}</div></details>"""
        for f, a in FRAGEN
    )
    inhalt = f"""{seitenkopf("mitte",
        [(None, "Fragen")],
        "Häufige Fragen",
        "Alle Antworten stammen von der bestehenden Website des Betriebs. Was dort "
        "nicht steht, steht auch hier nicht.")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  <div class="wrap">
    <div class="faq">
      <label class="sr-only" for="faq-suche">Fragen durchsuchen</label>
      <input class="faq__suche" type="search" id="faq-suche"
             placeholder="Suchen, zum Beispiel: Wartung, Stördienst, Rauchmelder">
      {liste}
      <p class="faq__leer" hidden>Dazu steht hier nichts. Rufen Sie an —
      {e(B['tel'])} — oder schreiben Sie über das <a href="kontakt.html">Formular</a>.</p>
    </div>
  </div>
</section>
{cta_block("Frage nicht dabei?",
           "Kein Formular der Welt ersetzt zwei Minuten am Telefon. Die Nummer steht oben.")}
</main>"""
    return kopf(
        "faq.html",
        "Häufige Fragen — N.J. Bothmann, Stolberg",
        "Stördienst, Wartungsvertrag, Abrechnung, Rauchwarnmelder: die häufigsten "
        "Fragen an den Betrieb, beantwortet mit seinen eigenen Angaben.",
        jsonld=ld_faq(),
    ) + inhalt + fuss()


# --------------------------------------------------------------------------
# Kontakt
# --------------------------------------------------------------------------
THEMEN = [
    ("stoerung", "Störung — es funktioniert etwas nicht"),
    ("elektrotechnik", "Elektrotechnik"),
    ("heizungstechnik", "Heizung, Sanitär oder Klima"),
    ("tankschutz", "Tankschutz / Öltank"),
    ("rauchwarnmelder", "Rauchwarnmelder"),
    ("wartung", "Wartung oder Servicevertrag"),
    ("sonstiges", "Etwas anderes"),
]

KARTE_URL = ("https://www.openstreetmap.org/export/embed.html"
             "?bbox=6.2100%2C50.7620%2C6.2600%2C50.7880&amp;layer=mapnik")


def seite_kontakt():
    optionen = "".join('<option value="%s">%s</option>' % (w, e(t)) for w, t in THEMEN)
    inhalt = f"""{seitenkopf("geteilt",
        [(None, "Kontakt")],
        "Kontakt",
        "Für eine Störung ist der Anruf der schnellste Weg. Alles, was warten kann, "
        "geht auch über das Formular.",
        f'<a class="btn btn--voll" href="tel:{B["tel_link"]}" data-magnet>Jetzt anrufen: {e(B["tel"])}</a>')}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  <div class="wrap">
    <div class="ablauf__gitter" style="align-items:start">
      <div>
        <h2 style="font-size:var(--fs-xl)">Anfrage schreiben</h2>
        <p class="leise" style="max-width:44ch">Je genauer die Beschreibung, desto
        kürzer der Rückruf. Pflichtfelder sind mit * gekennzeichnet.</p>

        <form class="form" data-form name="anfrage" method="POST"
              data-netlify="true" netlify-honeypot="firmen-fax" action="danke.html">
          <input type="hidden" name="form-name" value="anfrage">
          <p class="honig" aria-hidden="true">
            <label>Bitte dieses Feld frei lassen
              <input name="firmen-fax" tabindex="-1" autocomplete="off"></label>
          </p>

          <div class="feld--doppel">
            <div class="feld">
              <label for="name">Name *</label>
              <input type="text" id="name" name="name" autocomplete="name" required>
            </div>
            <div class="feld">
              <label for="telefon">Telefon</label>
              <input type="tel" id="telefon" name="telefon" autocomplete="tel">
              <span class="tipp">Für einen Rückruf — freiwillig.</span>
            </div>
          </div>

          <div class="feld">
            <label for="email">E-Mail *</label>
            <input type="email" id="email" name="email" autocomplete="email" required>
          </div>

          <div class="feld">
            <label for="thema">Worum geht es?</label>
            <select id="thema" name="thema">{optionen}</select>
          </div>

          <div class="feld">
            <label for="nachricht">Ihre Nachricht *</label>
            <textarea id="nachricht" name="nachricht" required
              placeholder="Zum Beispiel: Ölkessel Baujahr 1994, Brenner startet nicht mehr zuverlässig. Haus in Stolberg-Büsbach."></textarea>
          </div>

          <div class="feld">
            <label class="zustimmung" for="zustimmung">
              <input type="checkbox" id="zustimmung" name="zustimmung" required>
              <span>Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a>
              gelesen und bin damit einverstanden, dass meine Angaben zur Bearbeitung
              der Anfrage verarbeitet werden. *</span>
            </label>
          </div>

          <div>
            <button class="btn btn--voll" type="submit" data-magnet>Anfrage senden</button>
          </div>
        </form>
      </div>

      <div>
        <h2 style="font-size:var(--fs-xl)">Direkt</h2>
        <dl class="fakten" style="grid-template-columns:1fr">
          <div class="fakt"><dt>Telefon</dt><dd><a href="tel:{B['tel_link']}" style="text-decoration:none">{e(B['tel'])}</a></dd></div>
          <div class="fakt"><dt>Telefax</dt><dd>{e(B['fax'])}</dd></div>
          <div class="fakt"><dt>E-Mail</dt><dd><a href="mailto:{B['mail']}" style="text-decoration:none;word-break:break-all">{e(B['mail'])}</a></dd></div>
          <div class="fakt"><dt>Anschrift</dt><dd style="font-size:.98rem;line-height:1.4">{e(B['name'])}<br>{e(B['strasse'])}<br>{e(B['plz'])} {e(B['ort'])}</dd></div>
        </dl>

        <h3 style="font-size:var(--fs-l);margin-top:2.4rem">Anfahrt</h3>
        <p class="leise" style="font-size:.9rem">Die Karte wird erst geladen, wenn Sie
        sie anfordern. Vorher geht keine Verbindung zu OpenStreetMap — deshalb braucht
        diese Seite auch kein Cookie-Banner.</p>
        <div class="kartenfeld" data-karte="{KARTE_URL}">
          <div class="kartenfeld__text">
            <p><strong>Karte von OpenStreetMap</strong></p>
            <p>Beim Laden wird Ihre IP-Adresse an OpenStreetMap übertragen.</p>
            <button class="btn btn--linie" type="button">Karte laden</button>
          </div>
        </div>

        <div class="hinweis" style="margin-top:2rem">
          <b>Zur Anschrift:</b> Das Impressum der bestehenden Website nennt die
          Industriestraße 2, die Seite „Karte / Anschrift“ dort die Werther Straße 2.
          Diese Vorschau folgt dem Impressum. Vor einem Livegang ist zu klären,
          welche Anschrift gilt.
        </div>
      </div>
    </div>
  </div>
</section>
</main>"""
    return kopf(
        "kontakt.html",
        "Kontakt — N.J. Bothmann, Stolberg | Telefon 02402 20864",
        "Anruf, E-Mail oder Formular. N.J. Bothmann, Industriestraße 2, 52224 "
        "Stolberg. Karte wird erst auf Klick geladen.",
        jsonld=ld_betrieb(),
    ) + inhalt + fuss(mit_sticky=False)


def seite_danke():
    inhalt = f"""{seitenkopf("mitte",
        [("kontakt.html", "Kontakt"), (None, "Danke")],
        "Angekommen.",
        "Ihre Nachricht ist raus. Eine Antwort kommt, sobald der Betrieb aus dem "
        "Keller wieder ans Telefon kommt.")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:0">
  <div class="wrap" style="text-align:center">
    <svg viewBox="0 0 120 120" width="120" height="120" style="margin:0 auto 2rem"
         role="img" aria-label="Häkchen">
      <circle cx="60" cy="60" r="52" fill="none" stroke="#2C3342" stroke-width="2"/>
      <path d="M38 62l15 15 30-34" fill="none" stroke="#F2B21A" stroke-width="4"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <p class="leise" style="max-width:46ch;margin-inline:auto">
      Falls es eilt: Der direkte Weg bleibt das Telefon unter
      <a href="tel:{B['tel_link']}" style="color:var(--gelb)">{e(B['tel'])}</a>.
    </p>
    <div class="cta__zeile" style="justify-content:center">
      <a class="btn btn--linie" href="index.html" data-magnet>Zur Startseite</a>
      <a class="btn btn--linie" href="ratgeber.html" data-magnet>In den Ratgeber</a>
    </div>
  </div>
</section>
</main>"""
    return kopf(
        "danke.html",
        "Danke — Ihre Anfrage ist angekommen | N.J. Bothmann",
        "Ihre Nachricht an N.J. Bothmann in Stolberg wurde übermittelt.",
    ) + inhalt + fuss(mit_sticky=False)


def seite_404():
    inhalt = f"""<main id="inhalt">
<section class="abschnitt vier">
  <div class="wrap">
    <p class="vier__zahl" aria-hidden="true">404</p>
    <h1 style="font-size:var(--fs-xl)">Diese Leitung endet im Nichts.</h1>
    <svg class="bruch" viewBox="0 0 320 60" role="img" aria-label="Unterbrochene Leitung">
      <path d="M0 30 H 120"/>
      <path class="live" d="M120 30 H 200"/>
      <path d="M200 30 H 320"/>
      <circle class="funke" cx="160" cy="30" r="4"/>
      <circle class="funke" cx="146" cy="22" r="2"/>
      <circle class="funke" cx="176" cy="39" r="2"/>
    </svg>
    <p class="leise" style="max-width:42ch;margin-inline:auto">
      Die Seite, die Sie gesucht haben, gibt es hier nicht (mehr).
      Die folgenden Wege führen zurück:
    </p>
    <div class="cta__zeile" style="justify-content:center">
      <a class="btn btn--voll" href="index.html" data-magnet>Startseite</a>
      <a class="btn btn--linie" href="kontakt.html" data-magnet>Kontakt</a>
      <a class="btn btn--linie" href="faq.html" data-magnet>Häufige Fragen</a>
    </div>
  </div>
</section>
</main>"""
    return kopf(
        "404.html",
        "Seite nicht gefunden — N.J. Bothmann, Stolberg",
        "Diese Seite gibt es nicht. Zurück zur Startseite, zum Kontakt oder zu den "
        "häufigen Fragen.",
    ) + inhalt + fuss(mit_sticky=False)


# --------------------------------------------------------------------------
# Impressum
# --------------------------------------------------------------------------
def seite_impressum():
    inhalt = f"""{seitenkopf("stapel",
        [(None, "Impressum")],
        "Impressum",
        "Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG), übernommen vom Impressum "
        "der bestehenden Website des Betriebs.")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:clamp(2.2rem,5vw,3.4rem)">
  <div class="wrap">
    <div class="prosa">
      <h2>Anbieter</h2>
      <p>{e(B['name'])}<br>
      {e(B['zusatz'])}<br>
      {e(B['strasse'])}<br>
      {e(B['plz'])} {e(B['ort'])}</p>

      <h2>Kontakt</h2>
      <p>Telefon: {e(B['tel'])}<br>
      Telefax: {e(B['fax'])}<br>
      E-Mail: <a href="mailto:{B['mail']}">{e(B['mail'])}</a></p>

      <h2>Vertretungsberechtigt und inhaltlich verantwortlich</h2>
      <p>{e(B['inhaber'])}<br>
      Elektrotechnik – Heizungstechnik – Tankschutz<br>
      {e(B['strasse'])}, {e(B['plz'])} {e(B['ort'])}</p>

      <h2>Steuerliche Angaben</h2>
      <p>Finanzamt: {e(B['finanzamt'])}<br>
      Steuernummer: {e(B['steuernr'])}<br>
      Umsatzsteuer-Identifikationsnummer: {e(B['ustid'])}</p>
      <p>Die Freistellungsbescheinigung nach § 48 Abs. 1 EStG ist unter der
      Sicherheitsnummer {e(B['freistell'])} nachzuprüfen.</p>

      <h2>Berufsrechtliche Regelungen</h2>
      <p>Handwerksordnung (Bundesgesetzblatt I, Seite 3074, in der Fassung vom
      24. September 1998) in der jeweils geltenden Fassung.<br>
      Zuständige Kammer: Handwerkskammer Aachen.</p>

      <h2>Verbraucherstreitbeilegung</h2>
      <p>Der Betrieb erklärt sich bei rechtlichen Konflikten mit Verbrauchern
      (§ 13 BGB) bereit, an Verbraucherschlichtungsverfahren nach dem
      Verbraucherstreitbeilegungsgesetz teilzunehmen. Zuständig ist die
      Allgemeine Verbraucherschlichtungsstelle des Zentrums für Schlichtung e. V.,
      Straßburger Straße 8, 77694 Kehl am Rhein,
      Telefon 07851 795 79 40, Telefax 07851 795 79 41,
      E-Mail mail@verbraucher-schlichtung.de,
      <a href="https://www.verbraucher-schlichtung.de" rel="noopener noreferrer"
         target="_blank">www.verbraucher-schlichtung.de</a>.</p>

      <h2>Haftung für Inhalte und Links</h2>
      <p>Als Diensteanbieter ist der Betrieb für eigene Inhalte auf diesen Seiten
      nach den allgemeinen Gesetzen verantwortlich. Für Inhalte externer Links sind
      ausschließlich deren Betreiber verantwortlich. Zum Zeitpunkt der Verlinkung
      waren keine Rechtsverstöße erkennbar. Bei Bekanntwerden von Rechtsverletzungen
      werden entsprechende Links entfernt.</p>

      <h2>Urheberrecht</h2>
      <p>Die auf diesen Seiten verwendeten Fotos stammen vom Betrieb selbst
      (Referenz-Galerie der bestehenden Website). Inhalte und Werke unterliegen dem
      deutschen Urheberrecht.</p>

      <div class="hinweis">
        <b>Hinweis zu diesem Entwurf.</b> Diese Seite ist eine unverbindliche
        Vorschau, erstellt von Nils Cremerius, Aachen, für {e(B['name'])}. Der Betrieb
        hat der Veröffentlichung noch nicht zugestimmt. Die Angaben oben sind
        wörtlich dem Impressum von {e(B['alt_url'])} entnommen, mit zwei
        Aktualisierungen: Die dortigen Verweise auf § 6 Teledienstegesetz und
        § 10 Abs. 3 Mediendienste-Staatsvertrag beziehen sich auf aufgehobene
        Vorschriften; maßgeblich ist heute § 5 DDG. Außerdem ist die Postleitzahl
        der Schlichtungsstelle in Kehl korrigiert (77694 statt 77964).
        <strong>Vor einem Livegang sind alle Angaben vom Betrieb zu bestätigen.</strong>
      </div>
    </div>
  </div>
</section>
</main>"""
    return kopf(
        "impressum.html",
        "Impressum — N.J. Bothmann, Stolberg",
        "Anbieterkennzeichnung nach § 5 DDG für N.J. Bothmann, Elektro, Heizung und "
        "Tankschutz, Industriestraße 2, 52224 Stolberg.",
    ) + inhalt + fuss(mit_sticky=False)


# --------------------------------------------------------------------------
# Datenschutz
# --------------------------------------------------------------------------
def seite_datenschutz():
    inhalt = f"""{seitenkopf("stapel",
        [(None, "Datenschutz")],
        "Daten&shy;schutz&shy;erklärung",
        "Informationen nach Art. 12 ff. DSGVO. Grundlage ist die "
        "Datenschutzerklärung der bestehenden Website, ergänzt um die Technik "
        "dieses Entwurfs.")}

<main id="inhalt">
<section class="abschnitt" style="padding-top:clamp(2.2rem,5vw,3.4rem)">
  <div class="wrap">
    <div class="prosa">
      <h2>Verantwortlicher</h2>
      <p>{e(B['inhaber'])}<br>{e(B['strasse'])}<br>{e(B['plz'])} {e(B['ort'])}<br>
      Telefon {e(B['tel'])} · <a href="mailto:{B['mail']}">{e(B['mail'])}</a></p>
      <p>Weitere Angaben stehen im <a href="impressum.html">Impressum</a>.</p>

      <h2>Welche Daten verarbeitet werden</h2>
      <p>Daten, die Sie übermitteln, werden grundsätzlich nur für die Zwecke
      verarbeitet, für die sie erhoben wurden. Eine Verarbeitung zu anderen Zwecken
      kommt nur in Betracht, wenn die Vorgaben des Art. 6 Abs. 4 DSGVO vorliegen.</p>

      <h2>Rechtsgrundlagen</h2>
      <ul class="aufzaehlung">
        <li>Einwilligung — Art. 6 Abs. 1 lit. a DSGVO</li>
        <li>Erfüllung eines Vertrags — Art. 6 Abs. 1 lit. b DSGVO</li>
        <li>Rechtliche Verpflichtung — Art. 6 Abs. 1 lit. c DSGVO</li>
        <li>Berechtigtes Interesse nach Abwägung — Art. 6 Abs. 1 lit. f DSGVO</li>
      </ul>
      <p>Eine Einwilligung können Sie jederzeit mit Wirkung für die Zukunft
      widerrufen. Gegen eine Verarbeitung auf Grundlage einer Interessenabwägung
      können Sie nach Art. 21 DSGVO Widerspruch einlegen.</p>

      <h2>Kontaktformular</h2>
      <p>Wenn Sie das Formular nutzen, werden die dort eingetragenen Angaben
      (Name, E-Mail-Adresse, optional Telefonnummer, Thema und Nachricht) zur
      Bearbeitung Ihrer Anfrage verarbeitet. Rechtsgrundlage ist Art. 6 Abs. 1
      lit. b beziehungsweise lit. f DSGVO. Das Formular enthält ein für Menschen
      unsichtbares Feld zur Spam-Abwehr; wird es ausgefüllt, wird die Übermittlung
      als automatisiert verworfen.</p>
      <p><strong>Noch offen:</strong> Über welchen Dienst die Formularnachrichten
      zugestellt werden, steht im Livebetrieb noch nicht fest. Dieser Entwurf ist
      für den Formulardienst des Hosters Netlify vorbereitet. Vor dem Livegang ist
      der Dienst hier namentlich zu nennen und, falls erforderlich, ein Vertrag zur
      Auftragsverarbeitung nach Art. 28 DSGVO zu schließen.</p>

      <h2>Server-Protokolle</h2>
      <p>Beim Abruf der Seiten verarbeitet der Hoster technisch notwendige Daten
      (unter anderem IP-Adresse, Zeitpunkt, abgerufene Datei, übertragene Menge,
      Browsertyp). Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Diese Vorschau
      liegt auf GitHub Pages; im Livebetrieb ist der tatsächliche Hoster zu nennen.</p>

      <h2>Cookies, Analyse, Tracking</h2>
      <p>Diese Website setzt <strong>keine Cookies</strong>, bindet keine
      Analysewerkzeuge ein und überträgt keine Daten an Werbenetzwerke. Deshalb gibt
      es auch kein Einwilligungsbanner.</p>
      <p>Ein Wert wird lokal in Ihrem Browser abgelegt: Der Sitzungsspeicher merkt
      sich, dass Sie die Begrüßungsanimation bereits gesehen haben, damit sie nicht
      bei jedem Seitenaufruf erneut läuft. Dieser Wert verlässt Ihren Browser nicht
      und wird mit dem Schließen des Tabs gelöscht.</p>

      <h2>Schriften und Skripte</h2>
      <p>Die verwendeten Schriften liegen auf demselben Server wie die Website; es
      wird keine Verbindung zu Google Fonts aufgebaut. Für die Bewegungsabläufe
      werden zwei Programmbibliotheken (GSAP und Lenis) über das Content Delivery
      Network jsDelivr geladen. Dabei wird Ihre IP-Adresse technisch bedingt an
      jsDelivr übertragen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.
      <strong>Vor einem Livegang empfohlen:</strong> beide Bibliotheken ebenfalls
      lokal ausliefern, dann entfällt auch diese Übertragung.</p>

      <h2>Karte</h2>
      <p>Die Karte auf der Kontaktseite wird <strong>erst nach einem Klick</strong>
      geladen. Vorher besteht keine Verbindung zu OpenStreetMap. Mit dem Klick
      willigen Sie nach Art. 6 Abs. 1 lit. a DSGVO in die Übertragung Ihrer
      IP-Adresse an die OpenStreetMap Foundation ein.</p>

      <h2>Speicherdauer</h2>
      <p>Daten werden verarbeitet, solange dies für den jeweiligen Zweck
      erforderlich ist. Bestehen gesetzliche Aufbewahrungspflichten aus Handels-
      oder Steuerrecht, werden die Daten für deren Dauer gespeichert und danach auf
      weitere Erforderlichkeit geprüft.</p>

      <h2>Empfänger</h2>
      <p>Eine Weitergabe an Dritte findet grundsätzlich nur statt, wenn dies zur
      Durchführung des Vertrags erforderlich ist, auf einer Interessenabwägung nach
      Art. 6 Abs. 1 lit. f DSGVO beruht, eine rechtliche Verpflichtung besteht oder
      Sie eingewilligt haben.</p>

      <h2>Ihre Rechte</h2>
      <ul class="aufzaehlung">
        <li>Auskunft über die zu Ihrer Person verarbeiteten Daten (Art. 15 DSGVO)</li>
        <li>Berichtigung (Art. 16 DSGVO)</li>
        <li>Löschung (Art. 17 DSGVO)</li>
        <li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
        <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
        <li>Widerspruch, insbesondere gegen Direktwerbung (Art. 21 DSGVO)</li>
        <li>Beschwerde bei einer Datenschutz-Aufsichtsbehörde (Art. 77 DSGVO)</li>
      </ul>
      <p>Es werden keine Verfahren eingesetzt, die auf einer automatisierten
      Entscheidungsfindung einschließlich Profiling im Sinne des Art. 22 DSGVO
      beruhen.</p>

      <div class="hinweis">
        <b>Hinweis zu diesem Entwurf.</b> Diese Datenschutzerklärung beschreibt die
        Technik <em>dieses Entwurfs</em>. Sie ist keine Rechtsberatung. Vor einem
        Livegang gehört sie an den tatsächlichen Hoster, den Formulardienst und die
        endgültige Einbindung der Bibliotheken angepasst und juristisch geprüft.
      </div>
    </div>
  </div>
</section>
</main>"""
    return kopf(
        "datenschutz.html",
        "Datenschutzerklärung — N.J. Bothmann, Stolberg",
        "Keine Cookies, kein Tracking, Schriften lokal, Karte erst auf Klick. "
        "Informationen nach Art. 12 ff. DSGVO.",
    ) + inhalt + fuss(mit_sticky=False)


# --------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------
SEITEN = [
    ("index.html", "1.0", seite_index),
    ("leistung-elektrotechnik.html", "0.9", seite_elektro),
    ("leistung-heizungstechnik.html", "0.9", seite_heizung),
    ("leistung-tankschutz.html", "0.9", seite_tankschutz),
    ("ueber-uns.html", "0.7", seite_ueber),
    ("ratgeber.html", "0.7", seite_ratgeber),
    ("ratgeber-rauchwarnmelder-nrw.html", "0.6", seite_art_rauchmelder),
    ("ratgeber-heizung-austauschpflicht.html", "0.6", seite_art_heizung),
    ("ratgeber-tankschutz-fachbetrieb.html", "0.6", seite_art_tank),
    ("faq.html", "0.6", seite_faq),
    ("kontakt.html", "0.9", seite_kontakt),
    ("danke.html", "0.1", seite_danke),
    ("404.html", None, seite_404),
    ("impressum.html", "0.3", seite_impressum),
    ("datenschutz.html", "0.3", seite_datenschutz),
]


def sitemap():
    heute = "2026-09-16"
    eintraege = "".join(
        "  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n"
        % (BASIS, d, heute, p)
        for d, p, _ in SEITEN if p
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '%s</urlset>\n' % eintraege)


def robots():
    return ("# Vorschau — der Betrieb hat der Veröffentlichung noch nicht zugestimmt.\n"
            "# Vor dem Livegang auf Allow umstellen.\n"
            "User-agent: *\n"
            "Disallow: /\n\n"
            "Sitemap: %ssitemap.xml\n" % BASIS)


# --------------------------------------------------------------------------
def main():
    gesamt = 0
    for datei, _prio, bauer in SEITEN:
        n = schreibe(datei, bauer())
        gesamt += n
        print("  %-42s %7.1f KB" % (datei, n / 1024))
    schreibe("sitemap.xml", sitemap())
    schreibe("robots.txt", robots())
    print("  %-42s %7.1f KB" % ("sitemap.xml + robots.txt", 0))
    print("\n  %d Seiten, %.1f KB HTML gesamt" % (len(SEITEN), gesamt / 1024))


if __name__ == "__main__":
    main()
