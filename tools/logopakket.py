#!/usr/bin/env python3
"""Maakt het logopakket 'logo-licht' (woordmerk donkergrijs, icoon in de logoblauwen, voor witte of lichte achtergrond)
in alle maten, naast het bestaande pakket 'logo-zwarte-achtergrond'. Rasteren gebeurt met Chrome headless (staat op deze pc).

Draaien: python tools/logopakket.py
Uitvoer: static/img/logo/pakket/  (svg, png transparant strak, png 800x267 en 1600x534 met vrije ruimte, jpg op wit, icoon, avatars)
"""
import pathlib, subprocess, shutil, tempfile, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "img" / "logo"
UIT = LOGO / "pakket"
CHROME = next((p for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if pathlib.Path(p).exists()), None)
WOORDMERK = "#3A3F44"   # donkergrijs (Lars, 22-09-2026)

def raster(svg_pad, breedte, uit_png):
    """Rendert een SVG transparant naar PNG op de gevraagde breedte."""
    svg = svg_pad.read_text(encoding="utf-8")
    import re
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg); w, h = float(vb.group(1)), float(vb.group(2))
    hoogte = round(breedte * h / w)
    html = f'<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}svg{{display:block;width:{breedte}px;height:{hoogte}px}}</style></head><body>{svg}</body></html>'
    with tempfile.TemporaryDirectory() as td:
        hp = pathlib.Path(td) / "logo.html"; hp.write_text(html, encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        f"--window-size={breedte},{hoogte}", f"--screenshot={uit_png}", hp.as_uri()], check=True, capture_output=True)

def kader(bron_png, kader_b, kader_h, uit, achtergrond=None):
    """Zet het strakke logo in een vast kader met vrije ruimte (hoogte van de onderregel) rondom."""
    im = Image.open(bron_png).convert("RGBA")
    marge = round(kader_h * 0.16)
    binnen = (kader_b - 2 * marge, kader_h - 2 * marge)
    k = im.copy(); k.thumbnail(binnen, Image.LANCZOS)
    doek = Image.new("RGBA", (kader_b, kader_h), achtergrond or (0, 0, 0, 0))
    doek.alpha_composite(k, ((kader_b - k.width) // 2, (kader_h - k.height) // 2))
    (doek.convert("RGB") if achtergrond else doek).save(uit, optimize=True)

def avatar(icoon_png, uit, achtergrond, maat=1000):
    im = Image.open(icoon_png).convert("RGBA")
    k = im.copy(); k.thumbnail((int(maat * 0.6), int(maat * 0.6)), Image.LANCZOS)
    doek = Image.new("RGBA", (maat, maat), achtergrond)
    doek.alpha_composite(k, ((maat - k.width) // 2, (maat - k.height) // 2))
    doek.convert("RGB").save(uit, optimize=True)

def main():
    if not CHROME: sys.exit("Chrome of Edge niet gevonden; nodig om de SVG te rasteren.")
    UIT.mkdir(exist_ok=True)
    # vectoren: afgeleid van de zwarte-achtergrondvariant, woordmerk donkergrijs
    for bron, doel in [("logo-zwarte-achtergrond.svg", "logo-licht.svg"), ("icoon-zwarte-achtergrond.svg", "icoon-licht.svg")]:
        s = (LOGO / bron).read_text(encoding="utf-8")
        s = s.replace('fill="#FFFFFF"', f'fill="{WOORDMERK}"').replace("Variant voor zwarte achtergrond: alleen op zwart of bijna-zwart gebruiken.",
                      f"Variant voor witte en lichte achtergrond: woordmerk {WOORDMERK}, icoon middenblauw #1B68C0 en lichtblauw #49BFFE. Afgeleid door Claude Code, 22-09-2026.")
        (UIT / doel).write_text(s, encoding="utf-8")
    shutil.copy(LOGO / "logo-zwarte-achtergrond.svg", UIT / "logo-zwarte-achtergrond.svg")
    shutil.copy(LOGO / "icoon-zwarte-achtergrond.svg", UIT / "icoon-zwarte-achtergrond.svg")
    # rasters
    for naam in ("logo-licht", "logo-zwarte-achtergrond"):
        raster(UIT / f"{naam}.svg", 3000, UIT / f"{naam}-3000px.png")
        kader(UIT / f"{naam}-3000px.png", 800, 267, UIT / f"{naam}-800x267.png")
        kader(UIT / f"{naam}-3000px.png", 1600, 534, UIT / f"{naam}-1600x534.png")
    kader(UIT / "logo-licht-3000px.png", 800, 267, UIT / "logo-licht-800x267.jpg", (255, 255, 255, 255))
    kader(UIT / "logo-zwarte-achtergrond-3000px.png", 800, 267, UIT / "logo-zwarte-achtergrond-800x267.jpg", (0, 0, 0, 255))
    for naam in ("icoon-licht", "icoon-zwarte-achtergrond"):
        raster(UIT / f"{naam}.svg", 1500, UIT / f"{naam}-1500px.png")
    avatar(UIT / "icoon-licht-1500px.png", UIT / "avatar-wit.png", (255, 255, 255, 255))
    avatar(UIT / "icoon-zwarte-achtergrond-1500px.png", UIT / "avatar-zwart.png", (17, 17, 17, 255))
    avatar(UIT / "icoon-zwarte-achtergrond-1500px.png", UIT / "avatar-donkerblauw.png", (2, 41, 91, 255))
    (UIT / "LEESMIJ.txt").write_text(f"""WESTENDORP TOEGANGSCONTROLE - LOGOPAKKET
Versie 22-09-2026. Twee varianten, alle maten.

logo-licht                 Voor wit en lichte achtergronden (website-header, briefpapier, e-mail). Woordmerk donkergrijs {WOORDMERK},
                           TOEGANGSCONTROLE lichtblauw #49BFFE, icoon middenblauw #1B68C0 en lichtblauw #49BFFE.
logo-zwarte-achtergrond    Voor zwart en bijna-zwart (tot #1E1E1E): werkkleding, bus op donkere ondergrond, donkere footer.

Per variant:
  <naam>.svg                vector, strak uitgesneden (drukwerk, belettering, borduren, website)
  <naam>-3000px.png         transparant, strak uitgesneden
  <naam>-800x267.png        transparant, vast kader met vrije ruimte (Word, e-mail, social media)
  <naam>-1600x534.png       zelfde kader op dubbele resolutie (retina)
  <naam>-800x267.jpg        op wit (licht) of zwart (zwarte achtergrond), voor platforms zonder PNG
  icoon-<variant>.svg / -1500px.png   los beeldmerk (sleutelgat met W), bijvoorbeeld als favicon
  avatar-wit.png, avatar-zwart.png, avatar-donkerblauw.png   vierkant 1000 x 1000 voor LinkedIn en Google Bedrijfsprofiel

Gebruik: minimale breedte volledig logo 200 px op scherm, 45 mm in druk; vrije ruimte rondom minimaal de hoogte van de onderregel.
Niet uitrekken, niet kantelen, geen schaduw, kleuren niet aanpassen. Lettertype in het logo: Archivo (contouren).
""", encoding="utf-8")
    print("geschreven in", UIT); [print(" ", p.name, p.stat().st_size // 1024, "KB") for p in sorted(UIT.iterdir())]

if __name__ == "__main__":
    main()
