# Bildnachweis

Alle Fotos auf dieser Vorschau-Website stammen **ausschließlich von der bestehenden
Website des Betriebs**, aus der Referenz-Galerie unter
`http://www.bothmann-stolberg.de/referenzen_pellets.html`.

Es wurden **keine Stock-Fotos, keine KI-Bilder und keine Fremdaufnahmen** verwendet.
Wo ein Foto fehlte, wurde die Lücke mit Typografie, Farbfläche und SVG-Grafik gefüllt.

## Rechtlicher Hinweis — vor dem Livegang klären

Die Bildrechte liegen beim Betrieb bzw. bei der Person, die die Aufnahmen gemacht hat.
Für diese Vorschau wurden die Dateien nur technisch aufbereitet (Zuschnitt auf Breite,
WebP-Konvertierung). Eine **breite Veröffentlichung ist erst nach Einverständnis des
Betriebs zulässig**. Die Vorschau ist mit `noindex, nofollow` ausgeliefert und für das
Gespräch mit dem Betrieb gedacht.

Auf einigen Aufnahmen sind **Personen** erkennbar (Mitarbeiter, Kunden, Umstehende).
Vor einem Livegang ist zu klären, ob für diese Personen eine Einwilligung nach
Art. 6 Abs. 1 DSGVO bzw. § 22 KunstUrhG vorliegt. Betroffen sind die Dateien
`montage-rohrleitung`, `ausbau-altkessel` und `team-vor-ort`.

Ebenfalls zu klären: das **Logo** (`logo.jpg` der alten Website) wurde für die Vorschau
**nicht** übernommen, sondern die Wortmarke typografisch nachgebaut. Die Original-Datei
liegt in dieser Vorschau nicht bei.

## Dateien

| Datei (ohne Größensuffix) | Quelle auf der alten Website | Originalgröße | Motiv laut Aufnahme |
|---|---|---|---|
| `montage-rohrleitung` | `hpfixgal_referenzen_pellets_bild0778_17_10_2008_12_43_04.jpg` | 800×600 | Monteur bei Rohrleitungsarbeiten in der Heizzentrale |
| `verteiler-armaturen` | `hpfixgal_referenzen_pellets_bild0882_31_10_2008_09_53_24.jpg` | 800×600 | Verteilerbalken mit Armaturen und Schaltkasten |
| `pelletkessel-paar` | `hpfixgal_referenzen_pellets_bild0822_20_10_2008_11_33_18.jpg` | 800×600 | Zwei Pelletkessel im Heizraum |
| `firmenfahrzeug` | `hpfixgal_referenzen_pellets_bild0827_20_10_2008_11_51_34.jpg` | 800×600 | Firmenfahrzeug mit Einblasschlauch bei der Pelletanlieferung |
| `heizzentrale-2021` | `hpfixgal_referenzen_pellets_img_6968_20_05_2021_09_45_20.jpg` | 800×600 | Heizzentrale, Aufnahme vom 20.05.2021 |
| `ausbau-altkessel` | `hpfixgal_referenzen_pellets_bild0786_17_10_2008_13_26_26.jpg` | 800×600 | Ausbau eines Altkessels |
| `anlage-fertig` | `hpfixgal_referenzen_pellets_bild0870_31_10_2008_09_50_02.jpg` | 800×600 | Fertige Anlage im selben Referenzprojekt-Zeitraum |
| `team-vor-ort` | `hpfixgal_referenzen_pellets_bild0866_24_10_2008_14_39_32.jpg` | 800×600 | Zwei Personen an der Verteilergruppe |
| `schaltwand-messtechnik` | `hpfixgal_referenzen_pellets_bild0979_13_01_2009_11_01_06.jpg` | 800×600 | Schaltwand mit Messtechnik und Ausdehnungsgefäßen |
| `regelung-display` | `hpfixgal_referenzen_pellets_img_6887_27_04_2021_07_18_24.jpg` | 450×600 | Regelung mit Touch-Display, Aufnahme vom 27.04.2021 |
| `kessel-modern-2021` | `hpfixgal_referenzen_pellets_img_6888_27_04_2021_07_18_28.jpg` | 800×600 | Moderner Kessel mit Ausdehnungsgefäß, 27.04.2021 |
| `rohrbuendel-kupfer` | `hpfixgal_referenzen_pellets_bild0740_16_10_2008_08_40_56.jpg` | 800×600 | Verteiler mit Absperrarmaturen |
| `pelletlager-einblas` | `hpfixgal_referenzen_pellets_bild0756_16_10_2008_13_21_00.jpg` | 800×600 | Einblasstutzen am Pelletlager |
| `altkessel-demontage` | `hpfixgal_referenzen_pellets_bild0774_17_10_2008_12_42_10.jpg` | 800×600 | Demontierter Altkessel |
| `kesselhaus-oel` | `hpfixgal_referenzen_pellets_bild0738_16_10_2008_08_40_26.jpg` | 800×600 | Kesselhaus mit Ölkessel |
| `pumpengruppe` | `hpfixgal_referenzen_pellets_bild0877_31_10_2008_09_52_00.jpg` | 800×600 | Pumpengruppe mit Absperrung |
| `speicher-technikraum` | `hpfixgal_referenzen_pellets_bild1002_13_01_2009_11_06_30.jpg` | 800×600 | Technikraum mit Speicher |
| `aussenleitung-dach` | `hpfixgal_referenzen_pellets_bild0758_16_10_2008_13_21_22.jpg` | 800×600 | Außenliegende Leitungsführung |

## Aufbereitung

- Konvertiert mit **sharp** (libvips 8.18.6), Skript `_img.js`.
- Zwei Größen je Motiv: **800 px** (native Breite der Originale, Qualität 72) und
  **400 px** (Qualität 64), eingebunden über `srcset` mit `width`/`height` und
  `loading="lazy"` außerhalb des ersten Viewports.
- **Nicht hochskaliert.** Die Originale sind 800 px breit; eine größere Variante würde
  Bytes ohne Detail erzeugen. Auf großen Bildschirmen sind die Fotos deshalb weich.
  Das ist im Entwurf bewusst durch Korn- und Duotone-Auflage kaschiert.
  **Für einen Livegang sollten die Originalaufnahmen in voller Auflösung beim Betrieb
  angefragt werden.**

## Grafik ohne Foto

Alle übrigen Bildflächen sind SVG: die Leitungslinie als Seitenklammer, die Karte des
Einsatzgebiets, die Gewerke-Piktogramme, das Favicon und die Diagramme. Sie wurden für
diese Seite gezeichnet und enthalten keine fremden Vorlagen.
