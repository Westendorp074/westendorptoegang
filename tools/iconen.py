#!/usr/bin/env python3
"""Maakt favicon.ico, apple-touch-icon.png en og-standaard.png uit het logopakket.

Pillow kan geen SVG rasteren, dus wij gebruiken de PNG's uit het pakket (variant zwarte achtergrond, transparant)
en zetten de kleuren om naar de lichte variant volgens LEESMIJ: wit → donkerblauw, lichtblauw → middenblauw,
middenblauw → donkerblauw. Zodra icoon-kleur.png / logo-kleur.png worden aangeleverd: die hier neerzetten en dit
script opnieuw draaien. Draaien: python tools/iconen.py <map met logopakket-PNG's>
"""
import sys, pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
UIT = ROOT / "static" / "img"
DONKER, MIDDEN, LICHT, WIT = (2, 41, 91), (27, 104, 192), (73, 191, 254), (255, 255, 255)
ZWART = (28, 28, 28)

def dichtstbij(px):
    r, g, b = px
    kand = {WIT: DONKER, LICHT: MIDDEN, MIDDEN: DONKER}
    return min(kand, key=lambda k: (k[0]-r)**2 + (k[1]-g)**2 + (k[2]-b)**2)

def herkleur(im):
    im = im.convert("RGBA")
    px = im.load()
    kand = {WIT: DONKER, LICHT: MIDDEN, MIDDEN: DONKER}
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0: continue
            px[x, y] = kand[dichtstbij((r, g, b))] + (a,)
    return im

def main(bron):
    bron = pathlib.Path(bron)
    icoon_bron = next((p for p in [bron / "icoon-zwarte-achtergrond-1500px.png"] if p.exists()), None)
    logo_bron = next((p for p in [bron / "logo-zwarte-achtergrond-3000px.png"] if p.exists()), None)
    if not icoon_bron or not logo_bron:
        sys.exit("icoon- of logo-PNG niet gevonden in " + str(bron))
    # Site is zwart in header, hero en footer: de zwarte-achtergrondvariant gaat ongewijzigd op #111111.
    icoon = Image.open(icoon_bron).convert("RGBA")
    logo = Image.open(logo_bron).convert("RGBA")

    def vierkant(im, maat, achtergrond, marge):
        doek = Image.new("RGBA", (maat, maat), achtergrond)
        binnen = maat - 2 * marge
        k = im.copy(); k.thumbnail((binnen, binnen), Image.LANCZOS)
        doek.alpha_composite(k, ((maat - k.width) // 2, (maat - k.height) // 2))
        return doek

    # favicon.ico: 16, 32, 48 op transparant
    lagen = [vierkant(icoon, m, ZWART + (255,), max(1, m // 16)) for m in (16, 32, 48)]
    lagen[0].save(ROOT / "static" / "img" / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=lagen[1:])
    # apple-touch-icon: 180 px, opaak
    vierkant(icoon, 180, ZWART + (255,), 24).convert("RGB").save(UIT / "apple-touch-icon.png", optimize=True)
    # og-standaard: 1200×630, logo op --vlak
    og = Image.new("RGBA", (1200, 630), ZWART + (255,))
    k = logo.copy(); k.thumbnail((880, 300), Image.LANCZOS)
    og.alpha_composite(k, ((1200 - k.width) // 2, (630 - k.height) // 2))
    og.convert("RGB").save(UIT / "og-standaard.png", optimize=True)
    print("geschreven: favicon.ico, apple-touch-icon.png, og-standaard.png")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "static" / "img" / "logo")
