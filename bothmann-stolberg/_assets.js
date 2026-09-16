/* Erzeugt apple-touch-icon.png (180x180) und og.jpg (1200x630).
   Aufruf: node _assets.js   (benötigt sharp)

   Ebenen von unten nach oben:
     1) Farbverlauf als Grundfläche
     2) Foto rechts
     3) Verlauf, der das Foto nach links ausblendet
     4) Typografie (transparentes SVG)
*/
const sharp = require('sharp');
const fs = require('fs');

const W = 1200, H = 630, FOTO_B = 560;

(async () => {
  // --- Touch-Icon ---
  await sharp(fs.readFileSync('favicon.svg'), { density: 400 })
    .resize(180, 180).png({ compressionLevel: 9 })
    .toFile('apple-touch-icon.png');

  // --- 1) Grundfläche ---
  const grund = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1B1F29"/><stop offset="1" stop-color="#0D0F14"/>
    </linearGradient></defs>
    <rect width="${W}" height="${H}" fill="url(#g)"/>
  </svg>`);

  // --- 2) Foto ---
  const foto = await sharp('img/pelletkessel-paar-800.webp')
    .resize({ width: FOTO_B, height: H, fit: 'cover', position: 'centre' })
    .modulate({ brightness: 1.05, saturation: 1.1 })
    .toBuffer();

  // --- 3) Weiche Kante über dem Foto ---
  const kante = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${FOTO_B}" height="${H}">
    <defs>
      <linearGradient id="f" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0"   stop-color="#0D0F14" stop-opacity="1"/>
        <stop offset=".42" stop-color="#0D0F14" stop-opacity=".25"/>
        <stop offset="1"   stop-color="#0D0F14" stop-opacity=".05"/>
      </linearGradient>
      <linearGradient id="i" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#4E57C0" stop-opacity=".34"/>
        <stop offset="1" stop-color="#F2B21A" stop-opacity=".14"/>
      </linearGradient>
    </defs>
    <rect width="${FOTO_B}" height="${H}" fill="url(#i)"/>
    <rect width="${FOTO_B}" height="${H}" fill="url(#f)"/>
  </svg>`);

  // --- 4) Typografie, transparenter Hintergrund ---
  const text = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <path d="M72 96 v92 h44 v92 h-44 v150" fill="none" stroke="#4E57C0" stroke-width="3"/>
    <circle cx="72" cy="188" r="7" fill="#F2B21A"/>
    <circle cx="116" cy="280" r="7" fill="#FFF4BC"/>
    <text x="150" y="150" font-family="DejaVu Sans" font-size="21"
          letter-spacing="5" fill="#9AA1EC" font-weight="bold">STOLBERG · STÄDTEREGION AACHEN</text>
    <text x="150" y="255" font-family="DejaVu Sans" font-size="66"
          fill="#EDEEF2" font-weight="bold">N.J. Bothmann</text>
    <text x="150" y="330" font-family="DejaVu Sans" font-size="38"
          fill="#FFF4BC">Elektro · Heizung · Tankschutz</text>
    <rect x="150" y="372" width="70" height="3" fill="#F2B21A"/>
    <text x="150" y="438" font-family="DejaVu Sans" font-size="27"
          fill="#B4BAC8">Fünf Gewerke, ein Ansprechpartner.</text>
    <text x="150" y="480" font-family="DejaVu Sans" font-size="27"
          fill="#B4BAC8">Telefon 02402 20864</text>
    <text x="150" y="562" font-family="DejaVu Sans" font-size="19"
          fill="#666D7E">Entwurf Nils Cremerius — noch nicht freigegeben</text>
  </svg>`);

  await sharp({ create: { width: W, height: H, channels: 3, background: '#0D0F14' } })
    .composite([
      { input: grund, left: 0, top: 0 },
      { input: foto,  left: W - FOTO_B, top: 0 },
      { input: kante, left: W - FOTO_B, top: 0 },
      { input: text,  left: 0, top: 0 }
    ])
    .jpeg({ quality: 82, progressive: true })
    .toFile('og.jpg');

  for (const f of ['apple-touch-icon.png', 'og.jpg']) {
    console.log(f, (fs.statSync(f).size / 1024).toFixed(1), 'KB');
  }
})();
