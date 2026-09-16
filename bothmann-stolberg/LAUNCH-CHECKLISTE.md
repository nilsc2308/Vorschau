# Launch-Checkliste — Vorschau N.J. Bothmann, Stolberg

Stand: 16.09.2026 · Prüfumgebung: Chromium 153.0.8010.12 und WebKit 26.6 über
Playwright, lokaler Server, Prüfskript `_test.js` (liegt nicht im ausgelieferten
Ordner, siehe „Was im Ordner liegt").

Legende: **erledigt** = geprüft und in Ordnung · **offen** = muss der Kunde
liefern oder entscheiden · **vor Livegang** = im Entwurf bewusst anders gelöst.

---

## 1. Zusammenfassung der Messwerte

| Messung | Ergebnis | Ziel |
|---|---|---|
| JS-Fehler, 15 Seiten × 2 Breiten, Chromium | **0** | 0 |
| JS-Fehler, Stichprobe 3 Seiten × 2 Breiten, WebKit | **0** | 0 |
| Horizontaler Überlauf (`scrollWidth > clientWidth`) | **0 von 36 Messungen** | 0 |
| Ladegröße Startseite Desktop (1400 px) bis `load` | **330,6 KB** | < 900 KB |
| Ladegröße Startseite Handy (390 px) bis `load` | **295,5 KB** | < 500 KB |
| Ladegröße Kontaktseite Handy bis `load` | **191,2 KB** | < 500 KB |
| Interne Links geprüft / defekt | **13 / 0** | 0 defekt |
| Kontrastpaare nach WCAG AA geprüft | **12 von 12 bestanden** | alle ≥ 4,5:1 |
| Seiten mit genau einer `h1` | **15 von 15** | alle |
| Bilder ohne `alt`-Attribut | **0** | 0 |
| Formularfelder ohne Label | **0** | 0 |

---

## 2. Datenschutz

- **erledigt** — Eigene Datenschutzseite `datenschutz.html`, im Kopf jeder Seite
  und im Fuß verlinkt, Pflichtangaben nach Art. 12 ff. DSGVO.
- **erledigt** — Verantwortlicher, Rechtsgrundlagen, Speicherdauer, Empfänger und
  alle Betroffenenrechte einschließlich Beschwerderecht sind benannt.
- **erledigt** — Kontaktformular: verarbeitete Felder einzeln aufgeführt,
  Rechtsgrundlage genannt, Honeypot erklärt.
- **erledigt** — Der Abschnitt beschreibt genau die Technik *dieses* Entwurfs,
  nicht eine Mustererklärung.
- **offen — Kunde** — Der Formulardienst ist noch nicht entschieden. Vor dem
  Livegang namentlich nennen und, falls erforderlich, einen Vertrag zur
  Auftragsverarbeitung nach Art. 28 DSGVO schließen.
- **offen — Kunde** — Der endgültige Hoster ist noch nicht entschieden; in der
  Erklärung steht derzeit GitHub Pages als Ablageort der Vorschau.
- **vor Livegang** — Juristische Prüfung durch den Betrieb oder dessen Beratung.
  Dieser Entwurf ist keine Rechtsberatung.

## 3. Impressum

- **erledigt** — `impressum.html` mit Anbieter, Anschrift, Telefon, Telefax,
  E-Mail, Vertretungsberechtigtem, Finanzamt, Steuernummer, USt-IdNr.
  DE183357143, Freistellungsbescheinigung, Handwerksordnung und
  Verbraucherschlichtung.
- **erledigt** — Zwei stille Korrekturen gegenüber der alten Seite, beide im
  Impressum selbst offengelegt: die alte Seite beruft sich auf § 6 TDG und
  § 10 Abs. 3 MDStV (beides aufgehobene Vorschriften, heute § 5 DDG); die
  Postleitzahl der Schlichtungsstelle in Kehl lautet 77694, nicht 77964.
- **offen — Kunde** — **Anschrift widersprüchlich.** Impressum und
  Datenschutzerklärung der alten Seite nennen *Industriestraße 2*, die Seite
  „Karte / Anschrift" und mehrere Verzeichnisse *Werther Straße 2* (beide 52224
  Stolberg). Der Entwurf folgt dem Impressum. **Muss vor Livegang geklärt
  werden** — die Anschrift steht an sechs Stellen (Impressum, Datenschutz,
  Kontakt, Fuß, JSON-LD, Karten-Link).
- **offen — Kunde** — Handwerkskammer: Der Entwurf nennt die Handwerkskammer
  Aachen als zuständige Kammer. Auf der alten Seite steht keine Kammer.
  Bestätigen lassen.

## 4. Cookie-Banner

- **erledigt** — **Kein Banner nötig, weil keine Cookies gesetzt werden.**
  Geprüft: keine `document.cookie`-Zugriffe im Code.
- **erledigt** — Einziger Browser-Speicher: ein Eintrag im `sessionStorage`
  (`njb-intro`), damit die Begrüßungsanimation nicht bei jedem Seitenaufruf
  läuft. Verlässt den Browser nicht, wird mit dem Tab gelöscht, in der
  Datenschutzerklärung beschrieben.
- **erledigt** — Karte lädt erst nach Klick. Automatisiert bestätigt:
  vor dem Klick 0 `iframe`, nach dem Klick 1 `iframe`.

## 5. Mobil

- **erledigt** — Getestet bei 390 × 844 und 1400 × 900, jede Seite komplett
  durchgescrollt. `scrollWidth == clientWidth` auf allen 15 Seiten in beiden
  Breiten.
- **erledigt** — `overflow-x: clip` liegt auf `body`, **nicht** auf `html`.
  Damit bleibt `position: sticky` funktionsfähig.
- **erledigt** — Burger-Menü ab 1020 px, Vollbild-Overlay, Fokus wird im Menü
  gehalten, Escape schließt.
- **erledigt** — Unter 620 px: Wortmarken-Unterzeile ausgeblendet, Telefon-CTA
  nur als Symbol. Ohne diese Regel lief die Kopfleiste bei 390 px über
  (gemessen: 469 px statt 390 px) — behoben.
- **erledigt** — Alle fünf Hero-Blenden laufen bei 390 px; Screenshots in
  `_shots/` an je vier Positionen pro Blende geprüft.
- **erledigt** — Lange Komposita (`Datenschutzerklärung`) brechen per weichem
  Trennzeichen und `hyphens: auto`. Ohne das lief die Seite über
  (gemessen: 1558 px statt 1400 px) — behoben.

## 6. Meta-Angaben

- **erledigt** — Jede Seite hat eigenen `<title>` (alle ≤ 65 Zeichen,
  im Generator per `assert` erzwungen) und eigene `description`
  (alle ≤ 155 Zeichen, ebenfalls per `assert`).
- **erledigt** — `lang="de"`, `charset=utf-8`, `viewport` mit
  `viewport-fit=cover` auf allen Seiten.
- **erledigt** — `theme-color` gesetzt.

## 7. Favicon

- **erledigt** — `favicon.svg` (SVG, skaliert verlustfrei, Leitungsmotiv der
  Marke), `apple-touch-icon.png` 180 × 180, 2,6 KB, aus derselben Quelle
  gerendert.

## 8. Sitemap

- **erledigt** — `sitemap.xml` mit 14 Seiten (die 404-Seite gehört bewusst nicht
  hinein), `lastmod` und `priority`.
- **vor Livegang** — URLs in `sitemap.xml` zeigen auf den Vorschau-Pfad
  `nilsc2308.github.io/Vorschau/bothmann-stolberg/`. Auf die echte Domain
  umstellen. Der Generator hat dafür die Konstante `BASIS` in `_build.py`.

## 9. Robots / Indexierung

- **vor Livegang — WICHTIG** — Auf **jeder** der 15 Seiten steht
  `<meta name="robots" content="noindex, nofollow">`, weil der Betrieb der
  Veröffentlichung noch nicht zugestimmt hat. **Diese Zeile muss vor dem
  Livegang entfernt werden** — im Generator `_build.py`, Funktion `kopf()`.
  Sie ist dort mit einem Kommentar markiert.
- **vor Livegang** — `robots.txt` im Ordner enthält aktuell `Disallow: /`.
  Ebenfalls umstellen.
- **erledigt** — Die Vorschau liegt zusätzlich unter einem Repository, dessen
  Wurzel-`robots.txt` bereits alles sperrt.

## 10. Canonical

- **erledigt** — Jede Seite hat ein `rel="canonical"` auf ihre eigene URL.
- **vor Livegang** — Auf die echte Domain umstellen (dieselbe Konstante `BASIS`).

## 11. 404-Seite

- **erledigt** — `404.html` mit Marke, Navigation, drei Rückwegen und einem
  eigenen SVG-Motiv („unterbrochene Leitung").
- **erledigt** — In `netlify.toml` als Auffangregel eingetragen.
- **vor Livegang** — Auf GitHub Pages greift die 404-Seite eines Unterordners
  nicht. Beim echten Hoster prüfen.

## 12. Defekte Links

- **erledigt** — 13 interne Ziele geprüft, **0 defekt**.
- **offen — nicht abschließend prüfbar** — Der externe Link auf
  `https://www.verbraucher-schlichtung.de` (aus dem Impressum des Betriebs)
  antwortet aus dieser Prüfumgebung mit HTTP 503 beziehungsweise bricht den
  TLS-Handshake ab. Das ist sehr wahrscheinlich eine Sperre gegen automatische
  Zugriffe und kein Fehler der Seite. **Vor Livegang von Hand im Browser
  prüfen.**
- **erledigt** — Externe Links öffnen mit `rel="noopener noreferrer"`.

## 13. Performance

| Seite | eigene Dateien | jsDelivr | gesamt |
|---|---|---|---|
| Startseite, 1400 px | 280,9 KB | 49,7 KB | **330,6 KB** |
| Startseite, 390 px | 245,8 KB | 49,7 KB | **295,5 KB** |
| Kontakt, 390 px | 141,5 KB | 49,7 KB | **191,2 KB** |

- **erledigt** — Alle Fotos als WebP in zwei Größen (400 px und 800 px) mit
  `srcset`, `sizes`, `width`, `height` und `loading="lazy"` außerhalb des ersten
  Viewports. Gesamter Bilderordner: 812 KB für 18 Motive.
- **erledigt** — Schriften lokal, zwei Variable-Fonts, zusammen 64 KB, per
  `preload` und `font-display: swap`.
- **erledigt** — Nur `transform`, `opacity` und `clip-path` werden animiert.
- **vor Livegang, empfohlen** — GSAP und Lenis (zusammen 49,7 KB) lokal
  ausliefern. Spart den Fremdaufruf, vereinfacht die Datenschutzerklärung und
  erlaubt eine strengere Content-Security-Policy.
- **vor Livegang, empfohlen** — `styles.css` (45 KB) und `main.js` (30 KB) beim
  Hoster komprimiert ausliefern (gzip/brotli). Netlify macht das automatisch;
  GitHub Pages auch.

## 14. Barrierefreiheit

- **erledigt** — Kontrast: 12 Farbpaare berechnet, **alle bestehen WCAG AA für
  kleine Schrift**. Niedrigster Wert 5,44:1 (Indigo auf Papier), höchster
  16,88:1.
- **erledigt** — Genau eine `h1` je Seite, keine Sprünge in der
  Überschriftenfolge (geprüft auf allen 15 Seiten).
- **erledigt** — Sprungmarke „Zum Inhalt springen" als erstes fokussierbares
  Element.
- **erledigt** — Sichtbarer Fokusrahmen (3 px, Signalgelb) auf allen
  interaktiven Elementen.
- **erledigt** — Alle interaktiven SVG-Elemente (Verteiler-Module, Ortsknoten,
  Grundriss-Räume) sind per Tab erreichbar und mit Enter/Leertaste bedienbar,
  `role="button"` und `aria-pressed` gesetzt.
- **erledigt** — Vorher/Nachher-Slider mit `role="slider"`, `aria-valuenow` und
  Pfeiltasten-, Pos1- und Ende-Bedienung.
- **erledigt** — `prefers-reduced-motion: reduce` getestet: Der 700vh-Hero
  klappt auf 2104 px zusammen, alle fünf Textblöcke sind statisch sichtbar,
  kein horizontaler Überlauf, 0 JS-Fehler.
- **erledigt** — Ohne JavaScript bleibt die Seite vollständig lesbar und
  bedienbar; der Vorhang wird dann gar nicht erst eingeblendet.
- **offen — empfohlen** — Test mit einem echten Screenreader (NVDA oder
  VoiceOver). Automatisierte Prüfungen ersetzen das nicht.

## 15. Formular

Automatisiert geprüft, alle Punkte bestanden:

- **erledigt** — `?thema=tankschutz` wählt das Thema korrekt vor.
- **erledigt** — Leeres Absenden wird blockiert, 4 Fehlermeldungen erscheinen,
  der Fokus springt auf das erste fehlerhafte Feld.
- **erledigt** — Ungültige E-Mail wird erkannt (`aria-invalid="true"`).
- **erledigt** — Gültige Eingabe leitet auf `danke.html` weiter.
- **erledigt** — Honeypot-Feld `firmen-fax` vorhanden und bei −9768 px
  ausgelagert, `netlify-honeypot` im Formular gesetzt.
- **erledigt** — `data-netlify="true"` und verstecktes `form-name`-Feld für
  Netlify Forms.
- **erledigt** — Pflichtfeld-Kennzeichnung mit \*, Zustimmung zur
  Datenschutzerklärung als Pflichtfeld.
- **offen — Kunde** — Ohne Netlify (zum Beispiel auf GitHub Pages) verschickt
  das Formular nichts. Formulardienst festlegen.

## 16. Alt-Texte

- **erledigt** — **0 Bilder ohne `alt`-Attribut** auf allen 15 Seiten.
- **erledigt** — Inhaltsbilder haben beschreibende Alt-Texte, die sagen, was zu
  sehen ist (zum Beispiel „Monteur bei Rohrleitungsarbeiten in einer
  Heizzentrale").
- **erledigt** — Die 32 leeren `alt=""` auf der Startseite sind die
  Wiederholungen desselben Fotos innerhalb von Lamellen-, Kachel- und
  Streifen-Blenden. Jede Blende trägt den Alt-Text genau einmal; die übrigen
  Ausschnitte sind dekorativ und korrekt leer ausgezeichnet.

## 17. Analytics

- **erledigt** — **Keine Analyse, kein Tracking, keine Werbepixel eingebaut.**
- **offen — Kunde** — Falls Statistik gewünscht: cookiefreie Lösung wählen
  (zum Beispiel serverseitige Auswertung oder ein Dienst ohne
  personenbezogene Daten), sonst wird ein Einwilligungsbanner nötig.

## 18. Open Graph

- **erledigt** — `og:type`, `og:title`, `og:description`, `og:url`,
  `og:site_name`, `og:locale` und `og:image` auf jeder Seite.
- **erledigt** — `og.jpg` 1200 × 630, 59 KB, aus einem echten Foto des Betriebs
  plus Typografie gebaut; trägt sichtbar den Hinweis „Entwurf Nils Cremerius —
  noch nicht freigegeben".
- **erledigt** — `twitter:card = summary_large_image`.
- **vor Livegang** — Den Entwurfs-Hinweis aus `og.jpg` entfernen
  (`_assets.js`, letzte Textzeile) und neu erzeugen.

## 19. Lokale SEO-Daten

- **erledigt** — JSON-LD `Electrician` (Unterart von `LocalBusiness`) auf
  Startseite und Kontaktseite: Name, Anschrift, Telefon, Telefax, E-Mail,
  USt-IdNr., Einsatzgebiete Stolberg, Aachen, Eschweiler, Würselen.
- **erledigt** — JSON-LD `FAQPage` mit allen 12 Fragen auf `faq.html`.
- **erledigt** — JSON-LD `Article` auf allen drei Ratgeber-Beiträgen.
- **bewusst weggelassen** — **Keine `aggregateRating`, keine
  `openingHours`, keine Gründungsjahre.** Öffnungszeiten stehen nicht auf der
  alten Website, und eine belastbare Google-Bewertung war nicht zu belegen
  (nur ProvenExpert 4,70/5 aus 3 Bewertungen). Erfundene strukturierte Daten
  sind ein Verstoß gegen die Google-Richtlinien.
- **offen — Kunde** — Öffnungszeiten, Gründungsjahr, Mitarbeiterzahl und
  Meistertitel erfragen und ergänzen.
- **offen — Kunde** — Google-Unternehmensprofil prüfen und Anschrift,
  Telefonnummer und Website dort mit der Seite abgleichen.

---

## 20. Offene Angaben, die nur der Kunde liefern kann

| Punkt | Warum | Wer |
|---|---|---|
| **Fotorechte** | Alle 18 Fotos stammen aus der Referenz-Galerie der alten Website. Auf drei Aufnahmen sind Personen erkennbar (`montage-rohrleitung`, `ausbau-altkessel`, `team-vor-ort`). Einwilligung nach Art. 6 DSGVO / § 22 KunstUrhG klären. | Betrieb |
| **Fotos in voller Auflösung** | Die Originale sind nur 800 px breit. Auf großen Bildschirmen sind sie weich; der Entwurf kaschiert das mit Korn und Farbauflage. Originaldateien wären deutlich besser. | Betrieb |
| **Richtige Anschrift** | Industriestraße 2 oder Werther Straße 2 — die alte Website nennt beides. | Betrieb |
| **Domain** | Bleibt `bothmann-stolberg.de`? Die Zweitdomain `elektro-bothmann.de` zeigt auf dieselbe Seite und sollte per 301 auf die Hauptdomain zeigen. | Betrieb |
| **Hoster** | Aktuell ohne HTTPS bei einem Anbieter, dessen Baukasten „HomepageFIX 2020" die Seiten erzeugt. Neuer Hoster mit kostenlosem TLS-Zertifikat nötig. | Betrieb / Nils |
| **Formulardienst** | Netlify Forms, ein anderer Dienst oder ein einfacher Mail-Versand? Entscheidet über die Datenschutzerklärung. | Betrieb / Nils |
| **Öffnungszeiten** | Fehlen auf der alten Website, wären für lokale Suche und JSON-LD wertvoll. | Betrieb |
| **Preise / Stundensätze** | Die alte Seite verweist auf „feststehende Stundenverrechnungssätze", nennt sie aber nicht. Der Entwurf nennt deshalb auch keine. | Betrieb |
| **Urlaubshinweis** | Der Entwurf hat die Seite „Urlaubszeit" nicht übernommen, weil sie tagesaktuell gepflegt werden muss. Klären, ob so etwas gewünscht ist. | Betrieb |
| **Logo** | Das alte Logo (985 × 93 px JPG) wurde **nicht** übernommen; die Wortmarke ist typografisch nachgebaut. Original in Vektorform erfragen oder Wortmarke bestätigen lassen. | Betrieb |

---

## 21. Was im Ordner liegt

**Ausgeliefert wird:** die 15 HTML-Seiten, `styles.css`, `main.js`, `fonts/`,
`img/`, `favicon.svg`, `apple-touch-icon.png`, `og.jpg`, `sitemap.xml`,
`robots.txt`, `netlify.toml`.

**Zusätzlich für Nils:** `_build.py` (erzeugt alle HTML-Seiten neu),
`_assets.js` (Icon und OG-Bild), `_img.js` (Bildaufbereitung), `DESIGN.md`,
`LAUNCH-CHECKLISTE.md`, `PITCH.md`, `pitch/` (vier Screenshots),
`img/BILDNACHWEIS.md`.

**Entfernt vor der Ablage:** `node_modules/`, `package.json`,
`package-lock.json`, `_test.js`, `_test-bericht.json`, `_shots/`.
Der Testlauf lässt sich jederzeit neu aufsetzen:
`npm install playwright sharp` und das Prüfskript neu schreiben.

---

## 22. Reihenfolge für den Livegang

1. Einverständnis des Betriebs einholen — ohne das passiert nichts weiter.
2. Anschrift klären und im Generator korrigieren.
3. `BASIS` in `_build.py` auf die echte Domain setzen.
4. `<meta name="robots" content="noindex, nofollow">` aus `kopf()` entfernen.
5. `robots.txt` auf `Allow` umstellen.
6. Entwurfs-Hinweis aus dem Fuß (`fuss()`) und aus `og.jpg` entfernen.
7. Fotorechte klären, nach Möglichkeit Originale in voller Auflösung einsetzen.
8. GSAP und Lenis lokal ausliefern, CSP entsprechend verschärfen.
9. Hoster einrichten, TLS prüfen, alte URLs per 301 weiterleiten
   (Liste liegt in `netlify.toml`).
10. Formulardienst einrichten und mit einer echten Testnachricht prüfen.
11. Datenschutzerklärung an Hoster und Formulardienst anpassen, juristisch
    prüfen lassen.
12. `python3 _build.py` erneut ausführen, Testlauf wiederholen, veröffentlichen.
13. Sitemap im Google-Unternehmensprofil und in der Search Console einreichen.
