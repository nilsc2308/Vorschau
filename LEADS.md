# LEADS

Protokoll der Akquise-Läufe. Eine Firma wird **nur dann nicht erneut bearbeitet**,
wenn sie im Abschnitt **„Bearbeitet"** steht (= Vorschau-Website wurde gebaut).

Firmen im Abschnitt **„Kandidatenpool (unbewertet)"** sind **weiterhin offen** und
sollen in einem späteren Lauf bewertet und bearbeitet werden.

---

## Bearbeitet

_(noch keine)_

---

## Lauf 2026-09-16 (Mittwoch) — Elektriker, Stolberg — ABGEBROCHEN

**Ergebnis: keine Website gebaut. Grund: technische Sperre, kein inhaltlicher Grund.**

Die Ausführungsumgebung dieses Laufs lässt über ihre Netzwerk-Richtlinie (Egress-Proxy)
**keinen Zugriff auf externe Websites** zu. Geprüft und jeweils vom Proxy mit 403
abgewiesen wurden u. a.:

| Ziel | Status |
|---|---|
| Firmen-Websites (bothmann-stolberg.de, petgmbh.de, elektro-swoboda.de, eotek.de, elektro-klakow.com, evosell.de, egreen-elektro.de, elektroeckstein.de) | blockiert (403) |
| Branchenverzeichnisse (gelbeseiten.de, dasoertliche.de, 11880.com, elektriker.org) | blockiert (403) |
| Innung / Handwerk (dashandwerk.de, kh-aachen.de, elektroinnung-aachen.de) | blockiert (403) |
| CDNs (cdn.jsdelivr.net, unpkg.com) | blockiert (403) |
| OpenStreetMap (nominatim, tile) | blockiert (403) |
| https://nilsc2308.github.io/ | blockiert (403) |

Erreichbar waren nur: Websuche (nur Trefferlisten und Snippets, keine Seiteninhalte),
npm-Registry, PyPI, api.github.com und der Git-Push zu GitHub.

**Warum das den Auftrag blockiert:** Die Bewertung nach Schritt 2 (viewport-Meta,
HTTPS, Impressum/Datenschutz, Baukasten-Fußzeile, Copyright-Jahr, Fotobestand)
setzt das Öffnen jeder Website voraus. Schritt 3 verlangt Inhalte, Kontaktdaten,
Impressum, Farben, Logo und **mindestens 3 bzw. für den Startseiten-Scroll 5 echte
Fotos von der alten Website**. Ohne Seitenabruf ist beides nicht möglich. Erfinden
ist laut Auftrag ausgeschlossen (keine Stock-Fotos, keine KI-Bilder, keine erfundenen
Angaben), deshalb wurde **bewusst keine Website gebaut**, statt eine mit erfundenen
Inhalten für einen echten Betrieb zu veröffentlichen.

### Kandidatenpool (unbewertet) — Elektriker Stolberg + 30 km

Aus Suchmaschinen-Trefferlisten und -Snippets zusammengetragen. **Keine Punktevergabe**,
da keine Website geöffnet werden konnte. Alle Angaben unbestätigt; nicht aus dem
Impressum gelesen. „unbekannt" heißt: liegt nicht vor.

| # | Firma | Ort | Telefon | Website | Punkte |
|---|---|---|---|---|---|
| 1 | Heinz Huberty Elektroinstallationen | 52223 Stolberg | unbekannt | unbekannt | nicht bewertet |
| 2 | SGT GmbH | 52222 Stolberg | unbekannt | unbekannt | nicht bewertet |
| 3 | Uwe Weißhoff Elektroinstallation | 52222 Stolberg | unbekannt | unbekannt | nicht bewertet |
| 4 | Elektrotechnik Schell GmbH (Markus Schell) | Rothe Gasse 8, 52224 Stolberg | unbekannt | unbekannt | nicht bewertet |
| 5 | Herbert Cönzer Elektromeisterbetrieb | Stolberg | unbekannt | unbekannt | nicht bewertet |
| 6 | Frank Theißen Elektrohandel | Stolberg | unbekannt | unbekannt | nicht bewertet |
| 7 | Elektro Schlösser | Stolberg | unbekannt | unbekannt | nicht bewertet |
| 8 | N. J. Bothmann Elektro | Werther Str. 2, 52224 Stolberg-Mausbach | unbekannt | bothmann-stolberg.de | nicht bewertet |
| 9 | P-E-T Elektroanlagenbau GmbH | Leimberg 5, 52222 Stolberg | unbekannt | petgmbh.de | nicht bewertet |
| 10 | Elektro Gassert (seit 1946, 3. Generation) | Amaliastr. 33, 52223 Stolberg | 02402 21600 | unbekannt | nicht bewertet |
| 11 | Fernseh Lieber Meisterbetrieb (Frank Lieber) | Sebastianusstr. 86a, 52222 Stolberg | unbekannt | unbekannt | nicht bewertet |
| 12 | Elektro Swoboda e. K. (e-masters), Inh. Stephan Hamacher | Stolberg/Aachen (unklar) | unbekannt | elektro-swoboda.de | nicht bewertet |
| 13 | eGreen Meisterbetrieb Elektrotechnik | unbekannt | unbekannt | egreen-elektro.de | nicht bewertet |
| 14 | Elektro Ohligschläger GmbH & Co. KG | Würselen | unbekannt | eotek.de | nicht bewertet |
| 15 | Elektro Klakow Meisterbetrieb | Würselen | unbekannt | elektro-klakow.com | nicht bewertet |
| 16 | Albapol Elektrotechnik Meisterbetrieb | Eschweiler | unbekannt | unbekannt | nicht bewertet |
| 17 | EvoSell GmbH | Eschweiler | unbekannt | evosell.de | nicht bewertet |
| 18 | Elektro Palm (Turgay Kesgin) | Feldstr. 23a, Eschweiler | unbekannt | unbekannt | nicht bewertet |
| 19 | Elektro Eckstein GmbH & Co. KG | Aachen | unbekannt | elektroeckstein.de | nicht bewertet |
| 20 | Elektrotechnik Ell e. K. | Region Aachen | unbekannt | unbekannt | nicht bewertet |
| 21 | Elektro Kreutzer GmbH | Region Aachen | unbekannt | unbekannt | nicht bewertet |
| 22 | Elektro Anton Beckers GmbH | Region Aachen | unbekannt | unbekannt | nicht bewertet |

Erste Anlaufstellen für den nächsten Lauf (eigene Domain vorhanden, daher sofort
bewertbar): 8, 9, 12, 13, 14, 15, 17, 19.

### Damit der nächste Lauf durchläuft

In der Netzwerk-Richtlinie der Umgebung müssen freigeschaltet werden:

- beliebige Firmen-Domains (HTTP/HTTPS) — ohne das ist keine Bewertung und keine
  Foto-/Inhaltsübernahme möglich
- Branchenverzeichnisse: gelbeseiten.de, dasoertliche.de, 11880.com, elektriker.org
- cdn.jsdelivr.net — für die Fontsource-Schriftdateien beim Bauen
  (die GSAP-/Lenis-Einbindung im ausgelieferten HTML ist davon nicht betroffen,
  die lädt erst im Browser des Besuchers)
- nilsc2308.github.io — für die Abschlussprüfung auf HTTP 200
