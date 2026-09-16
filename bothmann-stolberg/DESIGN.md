# Design-Kontrakt — N.J. Bothmann, Stolberg

1. **Leitidee:** „Der Technikraum" — das, was im Haus niemand sieht: Kessel, Verteiler, Leitungen. Die Seite macht den Heizungs- und Elektrokeller zur Bühne statt ihn zu verstecken.
2. **Signature-Element:** Eine durchgehende **Leitungslinie** (SVG-Schaltplan-Strecke mit Knoten und 90°-Ecken), die vom Hero bis zum Kontakt-CTA durch alle Sektionen läuft und scrollgebunden gezeichnet wird; an jedem Knoten rastet eine Sektion ein.
3. **Typografie:** Display **Space Grotesk Variable** (technisch, geschnittene Kurven), Fließtext **Archivo Variable**; beide lokal aus `fonts/`, keine Google-Fonts-Aufrufe.
4. **Farbwelt:** Graphit `#101217` als Grundton, Indigo `#4E57C0` (aus dem vorhandenen Logo), Creme `#FFF4BC` (Logo-Verlauf), Signalgelb `#F2B21A` und Signalrot `#C8402E` als Akzente aus den Anlagenfotos.
5. **Navigationstyp:** Fixierte Kopfleiste mit Wortmarke links und Inline-Links rechts; ab 1020px Burger mit Vollbild-Overlay; zusätzlich Scroll-Fortschrittsbalken und Sticky-CTA-Leiste unten.
6. **Baustein 1:** Sticky-Storytelling „Vom Anruf zur Anlage" — vier Schritte pinnen sich, der Text wechselt scrollgebunden.
7. **Baustein 2:** Vorher/Nachher-Slider aus zwei echten Referenzfotos (Ausbau Altkessel ↔ fertige Anlage), Ziehgriff mit Tastaturbedienung.
8. **Baustein 3:** Text-Marquee mit eingestreuten Fotos — Leistungsband, Laufrichtung an die Scrollrichtung gekoppelt.
9. **Baustein 4:** Kacheln, die aus dem Raster fliegen — die fünf Gewerke lösen sich beim Scrollen aus einem Raster und setzen sich wieder zusammen.
10. **Baustein 5:** Interaktive SVG-Karte des Einsatzgebiets (Stolberg und Nachbarorte als Knoten der Leitungslinie), Hover/Fokus zeigt den Ort; echte OpenStreetMap-Karte erst nach Klick auf der Kontaktseite.

**Abgrenzung:** Im Repository existiert bisher kein weiterer Unterordner; dieser Kontrakt ist die erste Handschrift. Merkmale, die künftige Vorschauen *nicht* wiederholen sollen: die durchgehende Leitungslinie als Seitenklammer, die Graphit-Indigo-Creme-Kombination und der Blenden-Katalog Text-Maske / Lamellen / Kachel-Montage / Iris / Streifen-Vorhang in genau dieser Reihenfolge.
