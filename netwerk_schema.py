# Eigen vectorversie van het virtueel-netwerkoverzicht (Lars, 02-10-2026): plattegrond met één duidelijke
# route in vier genummerde stappen — pas uitgegeven, updates reizen mee, geblokkeerde pas geweigerd,
# alles in één scherm. Zelfde familie als sluitplan_schema.py.
import hashlib
import pathlib
from PIL import ImageFont

_ARIAL = ImageFont.truetype("arialbd.ttf", 23)
def _breedte(t):
    """Gemeten tekstbreedte, zodat de tekst nooit uit zijn blokje loopt."""
    return _ARIAL.getlength(t)

NAVY, BLAUW, LICHT = "#02295B", "#1B68C0", "#49BFFE"
GROEN, ROOD = "#3DBE7A", "#D9362B"
INKT, ZACHT, CHIP = "#14232E", "#5A6570", "#EEF4FB"
MUUR, MUURD, VLOER, KAMER = "#C7D2DD", "#9FB0C0", "#FDFEFE", "#F2F7FB"
F = "Arial,Helvetica,sans-serif"
W, H = 1240, 840
d = []

d.append(f'<defs><filter id="zweef" x="-20%" y="-20%" width="140%" height="150%">'
         f'<feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="{NAVY}" flood-opacity="0.16"/></filter></defs>')
d.append(f'<rect width="{W}" height="{H}" rx="14" fill="#FFFFFF"/>')

# ---- plattegrond ----
PX0, PY0, PX1, PY1 = 150, 70, 1150, 520
d.append(f'<rect x="{PX0}" y="{PY0}" width="{PX1 - PX0}" height="{PY1 - PY0}" rx="6" fill="{VLOER}" stroke="{MUUR}" stroke-width="10" filter="url(#zweef)"/>')
# kamers
d.append(f'<rect x="{PX0 + 5}" y="{PY0 + 5}" width="330" height="245" fill="{KAMER}"/>')          # vergaderruimte
d.append(f'<rect x="870" y="{PY0 + 5}" width="{PX1 - 875}" height="200" fill="{KAMER}"/>')        # kantoor
d.append(f'<rect x="870" y="330" width="{PX1 - 875}" height="{PY1 - 335}" fill="#E8EEF4"/>')      # serverruimte
d.append(f'<rect x="{PX0 + 5}" y="325" width="325" height="{PY1 - 330}" fill="#F6F3EC"/>')        # kantine
# binnenwanden (met gaten voor deuren)
d.append(f'<g fill="{MUUR}">'
         f'<rect x="480" y="{PY0}" width="10" height="126"/><rect x="480" y="264" width="10" height="{PY1 - 264}"/>'
         f'<rect x="{PX0}" y="315" width="200" height="10"/><rect x="420" y="315" width="70" height="10"/>'
         f'<rect x="865" y="{PY0}" width="10" height="130"/><rect x="865" y="270" width="10" height="110"/><rect x="865" y="450" width="10" height="{PY1 - 450}"/>'
         f'<rect x="875" y="270" width="{PX1 - 875}" height="10"/></g>')
# serverracks
for i in range(3):
    d.append(f'<rect x="{905 + i * 78}" y="345" width="52" height="108" rx="4" fill="{NAVY}"/>')
    for j in range(5):
        d.append(f'<rect x="{911 + i * 78}" y="{354 + j * 20}" width="40" height="7" rx="2" fill="{BLAUW}"/>')
# ramen in de buitengevel
for rx0, rb in ((200, 90), (310, 90), (560, 140), (930, 160)):
    d.append(f'<rect x="{rx0}" y="65" width="{rb}" height="10" rx="4" fill="#BEE3FB"/>')
for ry0 in (120, 360):
    d.append(f'<rect x="145" y="{ry0}" width="10" height="70" rx="4" fill="#BEE3FB"/>')
d.append(f'<rect x="1145" y="120" width="10" height="70" rx="4" fill="#BEE3FB"/>')
# meubels, ingetogen
d.append(f'<rect x="195" y="112" width="190" height="130" rx="18" fill="#E9F1F8"/>')
d.append(f'<rect x="215" y="140" width="150" height="70" rx="10" fill="#D9C9B2"/>')
for cx in (245, 300, 355):
    d.append(f'<circle cx="{cx}" cy="124" r="12" fill="{MUURD}"/><circle cx="{cx}" cy="226" r="12" fill="{MUURD}"/>')
d.append(f'<rect x="935" y="100" width="150" height="70" rx="12" fill="#E9F1F8"/>')
d.append(f'<rect x="950" y="110" width="120" height="48" rx="8" fill="#D9C9B2"/><circle cx="1010" cy="92" r="11" fill="{MUURD}"/>')
d.append(f'<rect x="992" y="118" width="36" height="24" rx="3" fill="{NAVY}"/><rect x="1006" y="142" width="8" height="5" fill="{MUURD}"/>')
# kantine linksonder: keukenblok, koffieapparaat en een rond tafeltje met stoelen
d.append(f'<rect x="162" y="345" width="30" height="130" rx="6" fill="#D9C9B2"/>'
         f'<circle cx="177" cy="378" r="9" fill="#FFFFFF" stroke="{MUURD}" stroke-width="3"/>'
         f'<rect x="168" y="432" width="18" height="22" rx="3" fill="{NAVY}"/>'
         f'<rect x="171" y="449" width="12" height="5" rx="2" fill="{LICHT}"/>')
d.append(f'<circle cx="352" cy="408" r="48" fill="#EFE9DE"/><circle cx="352" cy="408" r="26" fill="#D9C9B2"/>')
for hx, hy in ((352, 366), (352, 450), (310, 408), (394, 408)):
    d.append(f'<circle cx="{hx}" cy="{hy}" r="11" fill="{MUURD}"/>')
# deurmat voor de entree
d.append(f'<rect x="596" y="528" width="48" height="13" rx="4" fill="{MUURD}" opacity="0.5"/>')
# ruimtelabels
def label(x, y, t):
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="16" font-weight="700" fill="{ZACHT}" '
            f'letter-spacing="2.5" text-anchor="middle">{t}</text>')
d.append(label(290, 288, "VERGADERRUIMTE"))
d.append(label(300, 499, "KANTINE"))
d.append(label(1010, 246, "KANTOOR"))
d.append(label(1010, 316, "SERVERRUIMTE"))
d.append(label(663, 470, "ENTREE"))
for px_, py_ in ((200, 480), (830, 100), (770, 480)):
    d.append(f'<circle cx="{px_}" cy="{py_}" r="13" fill="#7FC79A"/><circle cx="{px_ - 8}" cy="{py_ + 6}" r="8" fill="#5AA377"/><rect x="{px_ - 6}" y="{py_ + 10}" width="12" height="10" rx="2" fill="#B0714F"/>')

def deur(x, y, richting="h", led=GROEN):
    """Deuropening met blad en lezer; richting h = in een horizontale wand."""
    if richting == "h":
        return (f'<rect x="{x - 34}" y="{y - 7}" width="68" height="14" fill="{VLOER}"/>'
                f'<path d="M{x - 30} {y} A30 30 0 0 1 {x} {y - 30}" fill="none" stroke="{MUURD}" stroke-width="2" stroke-dasharray="4 5"/>'
                f'<rect x="{x - 32}" y="{y - 4}" width="8" height="34" rx="3" fill="{NAVY}"/>'
                f'<rect x="{x + 24}" y="{y - 22}" width="12" height="18" rx="3" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'
                f'<circle cx="{x + 30}" cy="{y - 16}" r="3.5" fill="{led}"/>')
    return (f'<rect x="{x - 7}" y="{y - 34}" width="14" height="68" fill="{VLOER}"/>'
            f'<path d="M{x} {y - 30} A30 30 0 0 1 {x + 30} {y}" fill="none" stroke="{MUURD}" stroke-width="2" stroke-dasharray="4 5"/>'
            f'<rect x="{x - 4}" y="{y - 32}" width="34" height="8" rx="3" fill="{NAVY}"/>'
            f'<rect x="{x - 24}" y="{y + 22}" width="18" height="12" rx="3" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'
            f'<circle cx="{x - 15}" cy="{y + 28}" r="3.5" fill="{led}"/>')

# deuren: entree onderin het open middendeel, binnendeuren, serverruimte (rood)
d.append(deur(620, PY1, "h"))                     # entree in de ondergevel
d.append(deur(385, 320, "h"))                     # lager kamertje links -> gang
d.append(deur(485, 230, "v"))                     # vergaderruimte -> gang
d.append(deur(870, 225, "v"))                     # gang -> kantoor
d.append(deur(870, 415, "v", led=ROOD))           # gang -> serverruimte, geweigerd

# ---- route: van de pas, door de deuren, stoppend bij de geweigerde deur ----
route = (f"M258 648 C 370 614 510 590 616 556 L620 500 "
         f"L620 330 C 620 272 582 240 530 232 L504 230 "
         f"M530 208 C 650 186 760 196 848 220 "
         f"M872 246 C 832 300 828 356 850 404")
d.append(f'<path d="{route}" fill="none" stroke="{LICHT}" stroke-width="8" stroke-linecap="round" stroke-dasharray="0.1 20"/>')
for px_, py_, hoek in ((620, 540, -90), (512, 230, 180), (844, 219, 12), (852, 400, 65)):
    d.append(f'<g transform="translate({px_} {py_}) rotate({hoek})"><path d="M-6 -11 L12 0 L-6 11 Z" fill="{LICHT}"/></g>')
# blokkeerteken bij de geweigerde deur
d.append(f'<g transform="translate(838 444)"><circle r="15" fill="{ROOD}"/>'
         f'<path d="M-7 -7 L7 7 M7 -7 L-7 7" stroke="#fff" stroke-width="4" stroke-linecap="round"/></g>')
# statusverbinding van het pand naar het beheerscherm
d.append(f'<path d="M1000 528 C 1016 548 1036 562 1052 574" fill="none" stroke="{BLAUW}" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/>')

# ---- de pas linksonder, met het eigen sleutelgat-W-logo (zelfde paden als de favicon) ----
LOGO = ['M475.08 219.5A229 229 0 1 0 161.87 457.39L148.59 506.57A17 17 0 0 0 165 528L330 528A17 17 0 0 0 346.41 506.57L325.06 427.5L289.85 427.5L307.8 494L187.2 494L198.76 451.17A17 17 0 0 0 187.57 430.56A195 195 0 1 1 440.83 219.5Z',
        'M363.74 219.5A119 119 0 1 0 224.5 361.76L224.5 326.83A85 85 0 1 1 328.58 219.5ZM57.76 471.15L16.71 609.15A17 17 0 0 0 33 631L462 631A17 17 0 0 0 478.29 609.15L424.25 427.5L388.78 427.5L439.21 597L55.79 597L90.35 480.85Z',
        'M237.5 252.29H279.52L300.01 327.85Q301.05 330.74 301.88 334.78Q302.7 338.82 303.53 342.75Q304.36 346.68 304.98 349.37H306.22Q306.64 347.1 307.15 344.2Q307.67 341.3 308.29 338.3Q308.91 335.3 309.53 332.61Q310.16 329.92 310.57 327.85L329.82 252.29H378.67L398.13 327.85Q398.75 330.54 399.58 334.37Q400.41 338.2 401.23 342.23Q402.06 346.27 402.68 349.37H403.93Q404.34 347.1 404.96 344.3Q405.58 341.51 406.31 338.51Q407.03 335.51 407.65 332.71Q408.27 329.92 408.89 327.85L429.18 252.29H467.89L426.28 394.5H379.71L357.77 311.08Q356.94 307.98 356.01 304.35Q355.07 300.73 354.45 297.21Q353.83 293.69 353.42 291.21H352.18Q351.76 294.11 350.93 297.73Q350.11 301.35 349.28 304.87Q348.45 308.39 347.83 311.08L326.09 394.5H278.9L237.5 252.29Z']
d.append(f'<g transform="translate(168 682) rotate(-8)" filter="url(#zweef)">'
         f'<rect x="-72" y="-100" width="144" height="200" rx="16" fill="#FFFFFF" stroke="{MUUR}" stroke-width="3.5"/>'
         f'<g transform="translate(-37 -88) scale(0.15)">'
         f'<path fill="{LICHT}" d="{LOGO[0]}"/><path fill="{BLAUW}" d="{LOGO[1]}"/><path fill="{NAVY}" d="{LOGO[2]}"/></g>'
         # contactloos-symbool: drie bogen met stip, netjes gecentreerd onder het logo
         f'<g fill="none" stroke="{LICHT}" stroke-width="6.5" stroke-linecap="round">'
         f'<path d="M-8.5 64 A12 12 0 0 1 8.5 64"/>'
         f'<path d="M-15.6 57 A22 22 0 0 1 15.6 57"/>'
         f'<path d="M-22.6 50 A32 32 0 0 1 22.6 50"/></g>'
         f'<circle cx="0" cy="73" r="4.5" fill="{LICHT}"/>'
         f'</g>')
d.append(f'<circle cx="244" cy="592" r="20" fill="{GROEN}"/><path d="M234 592 l7 7 l14 -15" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')

# ---- het scherm rechtsonder ----
d.append(f'<g filter="url(#zweef)"><rect x="940" y="580" width="250" height="168" rx="10" fill="{NAVY}"/>'
         f'<rect x="950" y="590" width="230" height="148" rx="6" fill="#FFFFFF"/>'
         f'<rect x="958" y="598" width="124" height="132" rx="4" fill="{CHIP}"/>'
         f'<path d="M970 700 L1010 700 L1010 650 L1060 650" fill="none" stroke="{LICHT}" stroke-width="5" stroke-dasharray="0.1 11" stroke-linecap="round"/>'
         f'<circle cx="970" cy="700" r="6" fill="{BLAUW}"/><circle cx="1060" cy="650" r="6" fill="{BLAUW}"/>'
         + "".join(f'<circle cx="{1100}" cy="{612 + i * 30}" r="9" fill="{GROEN if i < 3 else ROOD}"/>'
                   f'<rect x="1116" y="{606 + i * 30}" width="56" height="12" rx="6" fill="{CHIP}"/>' for i in range(4))
         + f'<rect x="1040" y="748" width="50" height="22" fill="{MUURD}"/><rect x="1010" y="770" width="110" height="10" rx="5" fill="{MUURD}"/></g>')

# ---- vier genummerde stappen; blokbreedte volgt de gemeten tekst ----
def stap(x, y, n, t, anker="links"):
    b = round(54 + _breedte(t) + 22)
    if anker == "rechts":
        x -= b          # x is dan de rechterrand, bij het element waar het blokje op slaat
    elif anker == "midden":
        x -= b // 2
    return (f'<g><rect x="{x}" y="{y}" width="{b}" height="52" rx="26" fill="{CHIP}"/>'
            f'<circle cx="{x + 28}" cy="{y + 26}" r="17" fill="{BLAUW}"/>'
            f'<text x="{x + 28}" y="{y + 34}" font-family="{F}" font-size="21" font-weight="800" fill="#FFFFFF" text-anchor="middle">{n}</text>'
            f'<text x="{x + 54}" y="{y + 34}" font-family="{F}" font-size="23" font-weight="700" fill="{INKT}">{t}</text></g>')

d.append(stap(268, 742, 1, "Pas uitgegeven"))
d.append(stap(690, 140, 2, "Updates reizen mee van deur naar deur", anker="midden"))
d.append(stap(1142, 462, 3, "Geblokkeerde pas geweigerd", anker="rechts"))
d.append(stap(926, 646, 4, "Alle deuren in één scherm", anker="rechts"))

svg = (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" '
       f'aria-label="Virtueel netwerk: een uitgegeven pas neemt toegangsupdates mee van deur naar deur; een geblokkeerde pas wordt geweigerd en de beheersoftware toont de status van alle deuren">'
       + "".join(d) + "</svg>")
naam = f"virtueel-netwerk-schema-{hashlib.md5(svg.encode()).hexdigest()[:8]}.svg"
map_ = pathlib.Path(__file__).resolve().parent / "static" / "img" / "schema"
map_.mkdir(parents=True, exist_ok=True)
for oud in map_.glob("virtueel-netwerk-schema-*.svg"):
    oud.unlink()
(map_ / naam).write_text(svg, encoding="utf-8")
print(naam)
