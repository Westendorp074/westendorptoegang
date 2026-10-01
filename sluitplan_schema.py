# Eigen sluitplan-schema als SVG in de huisstijl (Lars, 01-10-2026): hoofdsleutel -> groepssleutels ->
# individuele sleutels -> cilinders -> deuren. Vector, dus op elk scherm haarscherp.
import hashlib
import pathlib

NAVY, BLAUW, LICHT = "#02295B", "#1B68C0", "#49BFFE"
INKT, ZACHT, LIJN, CHIP = "#14232E", "#5A6570", "#E4DFD7", "#EEF4FB"
F = "Arial,Helvetica,sans-serif"
W, H = 1240, 840
d = []

d.append(f'<rect width="{W}" height="{H}" rx="14" fill="#FFFFFF"/>')


def sleutel(x, y, s, kop, blad="#9AA7B4", rand="#6E7C8A"):
    """Platte sleutel: ronde kop met oog, blad met tanden."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="0" r="30" fill="{kop}"/><circle cx="0" cy="-8" r="8" fill="#FFFFFF"/>'
            f'<rect x="22" y="-7" width="64" height="14" rx="4" fill="{blad}"/>'
            f'<path d="M62 7 v9 h8 v-9 M76 7 v13 h8 v-13" fill="{blad}"/>'
            f'<rect x="22" y="-7" width="64" height="5" rx="2.5" fill="#FFFFFF" opacity=".35"/>'
            f'<circle cx="0" cy="0" r="30" fill="none" stroke="{rand}" stroke-width="2"/></g>')

def cilinder(x, y, s=1.0):
    """Europrofielcilinder van voren: cirkel met voetje en sleutelgat."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-16 8 h32 v22 a6 6 0 0 1 -6 6 h-20 a6 6 0 0 1 -6 -6 z" fill="#C7D0D9"/>'
            f'<circle cx="0" cy="0" r="22" fill="#DDE4EB" stroke="#9AA7B4" stroke-width="2"/>'
            f'<circle cx="0" cy="0" r="9" fill="#FFFFFF" stroke="#9AA7B4" stroke-width="1.5"/>'
            f'<rect x="-2" y="-2" width="4" height="12" rx="2" fill="{NAVY}"/><circle cx="0" cy="-3" r="3" fill="{NAVY}"/></g>')

def deur(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="0" r="30" fill="{CHIP}"/>'
            f'<path d="M-12 -20 L10 -24 V20 L-12 24 Z" fill="{NAVY}"/>'
            f'<rect x="10" y="-24" width="4" height="44" fill="{BLAUW}"/>'
            f'<circle cx="5" cy="1" r="2.5" fill="#FFFFFF"/></g>')

def chip(x, y, t, b=None, fs=15, fw="700", kleur=INKT):
    b = b or (len(t) * (fs * .62) + 26)
    return (f'<rect x="{x - b / 2:.0f}" y="{y - fs - 6}" width="{b:.0f}" height="{fs + 14}" rx="{(fs + 14) / 2:.0f}" fill="{CHIP}"/>'
            f'<text x="{x}" y="{y}" font-family="{F}" font-size="{fs}" font-weight="{fw}" fill="{kleur}" text-anchor="middle">{t}</text>')

def pijl(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1} {y1} H{mx} V{y2} H{x2 - 12}" fill="none" stroke="{LICHT}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{x2 - 12} {y2 - 7} L{x2 + 2} {y2} L{x2 - 12} {y2 + 7} Z" fill="{LICHT}"/>')

def lijntje(x1, y, x2):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{LIJN}" stroke-width="3"/>'

# kolommen
HX, GX, IX, CX, DX = 150, 420, 680, 920, 1120
rijen = [168, 268, 368, 528, 628, 728]
GA, GB = 268, 628

# hoofdsleutel (zilver, groot)
d.append(sleutel(HX, 420, 1.5, "#C7CFD8", blad="#AFB9C4", rand="#8A97A4"))
d.append(chip(HX, 540, "Hoofdsleutel", fs=19))
d.append(f'<text x="{HX}" y="572" font-family="{F}" font-size="14" fill="{ZACHT}" text-anchor="middle">Opent alle deuren</text>')
d.append(f'<text x="{HX}" y="592" font-family="{F}" font-size="14" fill="{ZACHT}" text-anchor="middle">in het systeem</text>')

# groepssleutels (navy)
for gy, naam in ((GA, "Groepssleutel A"), (GB, "Groepssleutel B")):
    d.append(pijl(HX + 110, 420, GX - 58, gy))
    d.append(sleutel(GX, gy, 1.0, NAVY, blad="#7E97B4", rand=NAVY))
    d.append(chip(GX, gy + 78, naam, fs=16))
    d.append(f'<text x="{GX}" y="{gy + 104}" font-family="{F}" font-size="13.5" fill="{ZACHT}" text-anchor="middle">Opent een groep deuren</text>')

# individuele sleutels, cilinders en deuren
d.append(chip(DX, 96, "Toegang per deur", fs=15))
for i, ry in enumerate(rijen):
    bron_y = GA if i < 3 else GB
    d.append(pijl(GX + 92, bron_y, IX - 46, ry))
    d.append(sleutel(IX, ry, .62, BLAUW, blad="#9FC6EC", rand=BLAUW))
    d.append(pijl(IX + 62, ry, CX - 32, ry))
    d.append(cilinder(CX, ry, .9))
    d.append(lijntje(CX + 30, ry, DX - 36))
    d.append(deur(DX, ry, .9))
d.append(chip(IX, 462, "Individuele sleutels", fs=14, fw="600", kleur=ZACHT))

svg = (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" '
       f'aria-label="Voorbeeld van een sluitplan: de hoofdsleutel opent alle deuren, groepssleutels openen een groep deuren en individuele sleutels één cilinder">'
       + "".join(d) + "</svg>")
naam = f"sluitplan-schema-{hashlib.md5(svg.encode()).hexdigest()[:8]}.svg"
map_ = pathlib.Path(__file__).resolve().parent / "static" / "img" / "schema"
map_.mkdir(parents=True, exist_ok=True)
for oud in map_.glob("sluitplan-schema-*.svg"):
    oud.unlink()
(map_ / naam).write_text(svg, encoding="utf-8")
print(naam)
