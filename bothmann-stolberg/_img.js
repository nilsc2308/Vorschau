const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const SRC = '/tmp/claude-0/-home-user-Vorschau/2f6fe71f-3150-5ab9-97a4-6df19ca6a319/scratchpad/probe/fotos';
const OUT = '/home/user/Vorschau/bothmann-stolberg/img';
const P = 'hpfixgal_referenzen_pellets_';
// name -> quelldatei
const MAP = {
  'montage-rohrleitung':      P+'bild0778_17_10_2008_12_43_04.jpg',
  'verteiler-armaturen':      P+'bild0882_31_10_2008_09_53_24.jpg',
  'pelletkessel-paar':        P+'bild0822_20_10_2008_11_33_18.jpg',
  'firmenfahrzeug':           P+'bild0827_20_10_2008_11_51_34.jpg',
  'heizzentrale-2021':        P+'img_6968_20_05_2021_09_45_20.jpg',
  'ausbau-altkessel':         P+'bild0786_17_10_2008_13_26_26.jpg',
  'anlage-fertig':            P+'bild0870_31_10_2008_09_50_02.jpg',
  'team-vor-ort':             P+'bild0866_24_10_2008_14_39_32.jpg',
  'schaltwand-messtechnik':   P+'bild0979_13_01_2009_11_01_06.jpg',
  'regelung-display':         P+'img_6887_27_04_2021_07_18_24.jpg',
  'kessel-modern-2021':       P+'img_6888_27_04_2021_07_18_28.jpg',
  'rohrbuendel-kupfer':       P+'bild0740_16_10_2008_08_40_56.jpg',
  'pelletlager-einblas':      P+'bild0756_16_10_2008_13_21_00.jpg',
  'altkessel-demontage':      P+'bild0774_17_10_2008_12_42_10.jpg',
  'kesselhaus-oel':           P+'bild0738_16_10_2008_08_40_26.jpg',
  'pumpengruppe':             P+'bild0877_31_10_2008_09_52_00.jpg',
  'speicher-technikraum':     P+'bild1002_13_01_2009_11_06_30.jpg',
  'aussenleitung-dach':       P+'bild0758_16_10_2008_13_21_22.jpg',
};
(async () => {
  const meta = [];
  for (const [name, file] of Object.entries(MAP)) {
    const src = path.join(SRC, file);
    if (!fs.existsSync(src)) { console.error('FEHLT', file); continue; }
    const im = sharp(src);
    const m = await im.metadata();
    for (const w of [400, 800]) {
      const out = path.join(OUT, `${name}-${w}.webp`);
      const info = await sharp(src).resize({ width: w, withoutEnlargement: true })
        .webp({ quality: w === 800 ? 72 : 64, effort: 6 }).toFile(out);
      if (w === 800) meta.push({ name, file, w: info.width, h: info.height, src: m.width + 'x' + m.height });
    }
  }
  console.log(JSON.stringify(meta, null, 1));
  const total = fs.readdirSync(OUT).filter(f=>f.endsWith('.webp'))
    .reduce((a,f)=>a+fs.statSync(path.join(OUT,f)).size,0);
  console.log('WEBP gesamt:', (total/1024).toFixed(0), 'KB in', fs.readdirSync(OUT).filter(f=>f.endsWith('.webp')).length, 'Dateien');
})();
