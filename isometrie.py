"""Isometrische illustraties als SVG, getekend in code (geen stock, geen AI-beeld).
Kleuren uit het logopakket. Elke scène is een functie die een <svg> teruggeeft; build.py zet ze inline in de pagina.
Projectie: x loopt naar rechtsonder, y naar linksonder, z omhoog."""
import math

# Palet
DONKER, MIDDEN, LICHT = "#02295B", "#1B68C0", "#49BFFE"
DONKER2, MIDDEN2, LICHT2 = "#0B3A78", "#3A84D6", "#8AD6FF"   # lichtere varianten voor bovenvlakken
GLAS, GLAS2 = "#BFE6FF", "#E3F4FF"
GROEN, GROEN2, GROENDONKER = "#3DBE7A", "#7ADCA5", "#177A42"
GROND, GROND2, WEG, STREEP = "#EEF1F4", "#E2E7EC", "#D5DBE1", "#FFFFFF"
STAM = "#6B5B4A"
WIT_T, WIT_L, WIT_R = "#F4F7FA", "#DDE5EE", "#C3CFDC"        # wit gebouw (zorg)
GRIJS_T, GRIJS_L, GRIJS_R = "#DDE2E7", "#B8C0C8", "#98A2AC"   # staal (industrie)
ZAND_T, ZAND_L, ZAND_R = "#F1E9DA", "#D9CDB5", "#BFB093"      # zandsteen (overheid, kerk)
ROOD_T, ROOD_L, ROOD_R = "#E8A79A", "#C9705F", "#A4523F"      # baksteen (school, kerk)

CX, CY = math.cos(math.radians(30)), math.sin(math.radians(30))

def _p(x, y, z, s):
    return (x - y) * CX * s, (x + y) * CY * s - z * s

def _poly(punten, fill, extra=""):
    d = " ".join(f"{px:.1f},{py:.1f}" for px, py in punten)
    return f'<polygon points="{d}" fill="{fill}"{extra}/>'

class Scene:
    def __init__(self, s=22, ox=0, oy=0):
        self.s, self.ox, self.oy, self.delen = s, ox, oy, []   # delen: (diepte, svg)
    def P(self, x, y, z):
        px, py = _p(x, y, z, self.s); return px + self.ox, py + self.oy
    def vlak(self, x, y, w, d, kleur, z=0):
        """Plat vlak op de grond (weg, gras, plein)."""
        self.delen.append((-100 + z, _poly([self.P(x, y, z), self.P(x + w, y, z), self.P(x + w, y + d, z), self.P(x, y + d, z)], kleur)))
    def blok(self, x, y, z, w, d, h, top, links, rechts, ramen=None, deur=None):
        """Gebouwblok: drie vlakken. ramen=(rijen, kolommen) tekent glas op beide zijvlakken."""
        P = self.P; diepte = x + w + y + d + z * 0.01
        uit = []
        uit.append(_poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], links))    # linkervlak (y=d)
        uit.append(_poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)], rechts))   # rechtervlak (x=w)
        uit.append(_poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)], top))       # bovenvlak
        if ramen:
            rijen, kol = ramen
            for r in range(rijen):
                zz = z + h * (r + 0.55) / rijen
                hh = h / rijen * 0.45
                for k in range(kol):
                    xx = x + w * (k + 0.2) / kol; ww = w / kol * 0.6
                    uit.append(_poly([P(xx, y + d, zz), P(xx + ww, y + d, zz), P(xx + ww, y + d, zz + hh), P(xx, y + d, zz + hh)], GLAS))
                    yy = y + d * (k + 0.2) / kol; dd = d / kol * 0.6
                    uit.append(_poly([P(x + w, yy, zz), P(x + w, yy + dd, zz), P(x + w, yy + dd, zz + hh), P(x + w, yy, zz + hh)], GLAS2))
        if deur:
            # deur op het linkervlak, met lezer ernaast; de lezer-led krijgt een class voor de animatie
            dx, dw, dh = deur
            uit.append(_poly([P(x + dx, y + d, z), P(x + dx + dw, y + d, z), P(x + dx + dw, y + d, z + dh), P(x + dx, y + d, z + dh)], DONKER))
            lx, ly = P(x + dx + dw + 0.35, y + d, z + dh * 0.55)
            uit.append(f'<rect x="{lx-3:.1f}" y="{ly-6:.1f}" width="6" height="12" rx="1" fill="#FFFFFF" stroke="{DONKER}" stroke-width="0.6"/>'
                       f'<circle class="led" cx="{lx:.1f}" cy="{ly-2:.1f}" r="1.6" fill="{GROEN}"/>')
        self.delen.append((diepte, "".join(uit)))
    def boom(self, x, y, r=0.55, h=1.4):
        P = self.P
        bx, by = P(x, y, 0); tx, ty = P(x, y, h)
        self.delen.append((x + y, f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{STAM}" stroke-width="2"/>'
                          f'<circle cx="{tx:.1f}" cy="{ty - r * self.s * 0.5:.1f}" r="{r * self.s:.1f}" fill="{GROEN}"/>'
                          f'<circle cx="{tx - r * self.s * 0.3:.1f}" cy="{ty - r * self.s * 0.7:.1f}" r="{r * self.s * 0.6:.1f}" fill="{GROEN2}"/>'))
    def zebra(self, x, y, w, d, n=5):
        for i in range(n):
            self.vlak(x + w * i / n + w / n * 0.15, y, w / n * 0.5, d, STREEP, 0.01)
    def auto(self, x, y, kleur=MIDDEN, klas=None, lang=1.4):
        def teken():
            self.blok(x, y, 0, lang, 0.7, 0.35, kleur, kleur, kleur)
            self.blok(x + 0.3, y, 0.35, min(0.8, lang * 0.5), 0.7, 0.3, GLAS, kleur, kleur)
        self.groep(klas, teken) if klas else teken()
    def ambulance(self, x, y):
        def teken():
            self.blok(x, y, 0, 1.6, 0.8, 0.55, WIT_T, WIT_L, WIT_R)
            self.blok(x + 0.55, y + 0.25, 0.55, 0.5, 0.12, 0.28, GROEN2, GROEN, GROENDONKER); self.blok(x + 0.68, y + 0.13, 0.55, 0.28, 0.36, 0.28, GROEN2, GROEN, GROENDONKER)
        self.groep("anim-auto", teken)
    def groep(self, klas, fn):
        """Voert fn uit en bundelt wat het toevoegt in één <g class=...> (voor CSS-animatie)."""
        n = len(self.delen); fn()
        nieuw = self.delen[n:]; del self.delen[n:]
        if nieuw:
            self.delen.append((min(d for d, _ in nieuw), f'<g class="{klas}">' + "".join(x for _, x in nieuw) + "</g>"))
    def vlag(self, x, y, h=3.2, kleur=None):
        P = self.P; fx, fy = P(x, y, 0); tx, ty = P(x, y, h)
        self.delen.append((x + y, f'<line x1="{fx:.1f}" y1="{fy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{DONKER}" stroke-width="2"/>'))
        self.groep("anim-vlag", lambda: self.delen.append((x + y + 0.01,
            f'<polygon points="{tx:.1f},{ty:.1f} {tx+24:.1f},{ty+6:.1f} {tx:.1f},{ty+13:.1f}" fill="{kleur or LICHT}" style="transform-origin:{tx:.1f}px {ty:.1f}px"/>')))
    def svg(self, breedte, hoogte, label):
        return (f'<svg viewBox="0 0 {breedte} {hoogte}" width="{breedte}" height="{hoogte}" role="img" aria-label="{label}" '
                f'xmlns="http://www.w3.org/2000/svg" class="iso">' + "".join(d for _, d in sorted(self.delen, key=lambda t: t[0])) + "</svg>")

def _basis(sc, w=9, d=9):
    sc.vlak(0, 0, w, d, GROND)
    sc.vlak(0, d * 0.42, w, 1.2, WEG); sc.zebra(w * 0.15, d * 0.42, 1.6, 1.2)
    sc.vlak(w * 0.42, 0, 1.2, d, WEG)

def kantoor():
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3, 3, 5.5, LICHT2, MIDDEN, DONKER, ramen=(5, 3))
    sc.blok(5.2, 0.8, 0, 3.2, 2.6, 3.2, LICHT2, MIDDEN2, DONKER2, ramen=(3, 3), deur=(0.4, 0.7, 1.2))
    sc.blok(0.8, 5.5, 0, 2.6, 2.6, 2.2, LICHT2, MIDDEN, DONKER, ramen=(2, 2))
    for x, y in [(4.2, 6.5), (6.5, 6.2), (7.8, 7.6), (5.3, 8.2)]: sc.boom(x, y)
    sc.auto(4.6, 4.1, DONKER, klas="anim-auto"); sc.auto(1.4, 4.1, LICHT)
    return sc.svg(420, 320, "Isometrische tekening van een kantoorpand met toegangscontrole")

def zorg():
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.4, 3.4, 4.2, WIT_T, WIT_L, WIT_R, ramen=(4, 3), deur=(1.3, 0.8, 1.2))
    # groot groen kruis op het dak, pulserend
    sc.groep("anim-gloed", lambda: (sc.blok(1.5, 1.95, 4.2, 1.4, 0.4, 0.35, GROEN2, GROEN, GROENDONKER), sc.blok(2.0, 1.45, 4.2, 0.4, 1.4, 0.35, GROEN2, GROEN, GROENDONKER)))
    sc.blok(5.4, 0.6, 0, 3, 2.8, 2.4, WIT_T, WIT_L, WIT_R, ramen=(2, 3))
    sc.blok(0.8, 5.6, 0, 3, 2.8, 1.8, LICHT2, MIDDEN2, DONKER2, ramen=(1, 3))
    for x, y in [(5.6, 6.6), (7.2, 7.4), (8.2, 5.9)]: sc.boom(x, y)
    sc.ambulance(5.4, 4.1)
    return sc.svg(420, 320, "Isometrische tekening van een zorginstelling met toegangscontrole")

def onderwijs():
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.4, 3.2, 2.6, ROOD_T, ROOD_L, ROOD_R, ramen=(2, 4), deur=(1.4, 0.7, 1.2))
    sc.blok(5.3, 0.6, 0, 3.2, 2.8, 2.6, ROOD_T, ROOD_L, ROOD_R, ramen=(2, 4))
    sc.vlak(0.8, 5.6, 3.2, 3.0, GROEN2)                      # schoolplein/gras
    sc.vlak(5.6, 5.8, 2.8, 2.6, GROND2)
    sc.vlag(4.6, 5.9)
    # speeltoestel en schoolbus
    sc.blok(1.6, 6.4, 0, 0.25, 0.25, 1.2, LICHT, LICHT, MIDDEN); sc.blok(2.6, 6.4, 0, 0.25, 0.25, 1.2, LICHT, LICHT, MIDDEN); sc.blok(1.6, 6.4, 1.2, 1.25, 0.25, 0.12, GROEN2, GROEN, GROENDONKER)
    sc.auto(5.2, 4.1, LICHT, klas="anim-auto", lang=2.2)
    for x, y in [(1.4, 7.9), (3.4, 6.2), (7.8, 7.6), (6.3, 6.4)]: sc.boom(x, y, 0.5, 1.2)
    return sc.svg(420, 320, "Isometrische tekening van een school met toegangscontrole")

def vve():
    sc = Scene(24, 210, 140); _basis(sc)
    for i in range(3):
        sc.blok(0.5 + i * 1.25, 0.6, 0, 1.15, 3.0, 3.0 + (i % 2) * 0.4, LICHT2, MIDDEN2 if i % 2 else MIDDEN, DONKER2 if i % 2 else DONKER, ramen=(3, 1), deur=(0.3, 0.5, 1.0) if i == 1 else None)
    sc.blok(5.4, 0.6, 0, 3.0, 2.8, 5.2, LICHT2, MIDDEN, DONKER, ramen=(5, 3))
    for i in range(3):
        sc.blok(0.5 + i * 1.25, 5.8, 0, 1.15, 2.6, 2.6, LICHT2, MIDDEN2, DONKER2, ramen=(2, 1))
    for i in range(5):   # balkons op de flat
        sc.blok(5.2, 1.0, 0.9 + i * 0.85, 0.2, 2.0, 0.08, LICHT, LICHT, LICHT2)
    for x, y in [(5.8, 6.4), (7.4, 7.6), (8.3, 5.9)]: sc.boom(x, y)
    sc.auto(5.6, 4.1, MIDDEN, klas="anim-auto")
    return sc.svg(420, 320, "Isometrische tekening van een appartementencomplex met toegangscontrole")

def verenigingen():
    sc = Scene(24, 210, 140); _basis(sc)
    # kerk: schip + toren
    sc.blok(0.6, 0.8, 0, 3.4, 2.4, 2.4, ZAND_T, ZAND_L, ZAND_R, ramen=(1, 4), deur=(1.4, 0.7, 1.4))
    sc.blok(0.6, 0.8, 0, 1.0, 1.0, 5.0, ZAND_T, ZAND_L, ZAND_R, ramen=(4, 1))
    # dak toren (piramide als driehoeken)
    P = sc.P; a, b, c, d = P(0.6, 0.8, 5), P(1.6, 0.8, 5), P(1.6, 1.8, 5), P(0.6, 1.8, 5); top = P(1.1, 1.3, 6.4)
    sc.delen.append((0.6 + 1.0 + 0.8 + 1.0 + 0.06, _poly([a, b, top], DONKER) + _poly([b, c, top], DONKER2) + _poly([c, d, top], MIDDEN)))
    # dorpshuis en sportveld
    sc.blok(5.4, 0.7, 0, 3.0, 2.6, 1.8, LICHT2, MIDDEN, DONKER, ramen=(1, 3), deur=(0.4, 0.6, 1.1))
    sc.vlak(0.8, 5.7, 3.4, 2.8, GROEN); sc.vlak(1.0, 5.9, 3.0, 2.4, GROEN2); sc.vlak(2.45, 5.9, 0.1, 2.4, STREEP, 0.01)   # sportveld met middenlijn
    sc.groep("anim-bal", lambda: sc.delen.append((2.0 + 6.9, f'<circle cx="{sc.P(2.0, 6.9, 0.15)[0]:.1f}" cy="{sc.P(2.0, 6.9, 0.15)[1]:.1f}" r="3" fill="#FFFFFF" stroke="{DONKER}" stroke-width="0.6"/>')))
    for x, y in [(5.8, 6.5), (7.6, 7.4), (8.3, 6.0)]: sc.boom(x, y)
    return sc.svg(420, 320, "Isometrische tekening van een kerk en dorpshuis met toegangscontrole")

def recreatie():
    sc = Scene(24, 210, 140); sc.vlak(0, 0, 9, 9, GROEN2); sc.vlak(0, 3.8, 9, 1.0, WEG); sc.vlak(4.0, 0, 1.0, 9, WEG)
    for x, y in [(0.6, 0.6), (2.3, 0.9), (0.8, 2.2), (5.6, 0.7), (7.3, 1.2), (5.8, 2.4)]:
        sc.blok(x, y, 0, 1.2, 1.0, 0.9, LICHT2, MIDDEN2, DONKER2, ramen=(1, 1))
        P = sc.P; a, b, c, d = P(x, y, 0.9), P(x + 1.2, y, 0.9), P(x + 1.2, y + 1.0, 0.9), P(x, y + 1.0, 0.9); top = P(x + 0.6, y + 0.5, 1.5)
        sc.delen.append((x + 1.2 + y + 1.0 + 0.02, _poly([a, b, top], DONKER) + _poly([b, c, top], DONKER2) + _poly([c, d, top], MIDDEN)))
    sc.blok(0.8, 5.6, 0, 3.2, 2.6, 1.6, LICHT2, MIDDEN, DONKER, ramen=(1, 3), deur=(1.3, 0.6, 1.1))   # receptie
    sc.vlak(5.6, 5.6, 2.8, 2.8, LICHT); sc.groep("anim-water", lambda: sc.vlak(5.8, 5.8, 2.4, 2.4, GLAS2, 0.01))   # zwembad met bewegend water
    for x, y in [(3.6, 1.6), (1.9, 3.2), (7.3, 3.2), (4.8, 7.8), (8.5, 4.6)]: sc.boom(x, y, 0.6, 1.6)
    return sc.svg(420, 320, "Isometrische tekening van een recreatiepark met toegangscontrole")

def industrie():
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.5, 3.4, 2.2, GRIJS_T, GRIJS_L, GRIJS_R, ramen=(1, 4), deur=(0.4, 1.2, 1.5))
    for i in range(3):   # sheddak
        P = sc.P; x = 0.5 + i * 1.17; a, b, c, d = P(x, 0.5, 2.2), P(x + 1.17, 0.5, 2.2), P(x + 1.17, 3.9, 2.2), P(x, 3.9, 2.2)
        t1, t2 = P(x + 0.3, 0.5, 2.8), P(x + 0.3, 3.9, 2.8)
        sc.delen.append((x + 1.17 + 3.9 + 0.03, _poly([a, t1, t2, d], GLAS) + _poly([t1, b, c, t2], LICHT2)))
    sc.blok(5.3, 0.7, 0, 3.2, 3.0, 1.6, MIDDEN2, MIDDEN, DONKER)                                     # magazijn (blauw: het bedrijf)
    sc.blok(6.0, 5.8, 0, 0.5, 0.5, 4.0, GRIJS_T, GRIJS_L, GRIJS_R)                                    # schoorsteen
    rx, ry = sc.P(6.25, 6.05, 4.0)
    sc.groep("anim-rook", lambda: sc.delen.append((6.25 + 6.05 + 0.1, f'<circle cx="{rx:.1f}" cy="{ry-6:.1f}" r="5" fill="#D5DBE1" opacity=".8"/><circle cx="{rx+4:.1f}" cy="{ry-14:.1f}" r="4" fill="#D5DBE1" opacity=".6"/>')))
    sc.blok(0.8, 5.7, 0, 1.4, 1.4, 1.4, GROND2, "#B8C0C8", "#98A2AC"); sc.blok(2.5, 5.7, 0, 1.4, 1.4, 1.4, GROND2, "#B8C0C8", "#98A2AC")  # tanks/containers
    sc.auto(4.6, 4.1, GRIJS_R, klas="anim-auto", lang=2.4)                                            # vrachtwagen rijdt
    for x, y in [(8.2, 7.6), (7.2, 8.2)]: sc.boom(x, y)
    return sc.svg(420, 320, "Isometrische tekening van een industrieterrein met toegangscontrole")

def overheid():
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.6, 3.4, 3.0, ZAND_T, ZAND_L, ZAND_R, ramen=(3, 4), deur=(1.5, 0.8, 1.3))
    for i in range(4):   # zuilen
        sc.blok(0.7 + i * 0.85, 3.9, 0, 0.3, 0.3, 3.0, ZAND_T, ZAND_T, ZAND_L)
    sc.blok(1.6, 1.6, 3.0, 1.4, 1.4, 0.9, ZAND_T, ZAND_L, ZAND_R)   # koepel-blok
    sc.vlag(2.3, 2.3, h=5.4, kleur=DONKER)
    sc.vlak(0.9, 5.7, 3.2, 2.8, GROND2); sc.zebra(1.2, 5.9, 2.6, 0.4, 3)   # plein
    sc.blok(5.4, 0.7, 0, 3.0, 2.6, 2.0, LICHT2, MIDDEN, DONKER, ramen=(2, 3))
    for x, y in [(5.8, 6.4), (7.4, 7.6), (8.3, 5.9), (4.6, 7.9)]: sc.boom(x, y)
    return sc.svg(420, 320, "Isometrische tekening van een gemeentehuis met toegangscontrole")

def hero_scene():
    """Grote scène voor de hero: bedrijfspand met entree, lezer en groene led."""
    sc = Scene(30, 300, 205)
    sc.vlak(0, 0, 10, 10, GROND); sc.vlak(0, 4.4, 10, 1.3, WEG); sc.zebra(1.2, 4.4, 1.8, 1.3); sc.vlak(4.4, 0, 1.3, 10, WEG)
    sc.blok(0.5, 0.5, 0, 3.6, 3.6, 6.0, LICHT2, MIDDEN, DONKER, ramen=(6, 3))
    sc.blok(6.0, 0.6, 0, 3.4, 3.4, 3.4, LICHT2, MIDDEN2, DONKER2, ramen=(3, 3), deur=(0.7, 0.9, 1.5))
    sc.blok(0.7, 6.0, 0, 3.4, 3.2, 2.0, LICHT2, MIDDEN, DONKER, ramen=(1, 3))
    sc.vlak(6.2, 6.0, 3.2, 3.2, GROEN2)
    for x, y in [(6.6, 6.5), (8.6, 7.0), (7.4, 8.6), (4.2, 8.8)]: sc.boom(x, y, 0.65, 1.7)
    sc.auto(6.4, 4.6); sc.auto(2.0, 4.6, DONKER)
    return sc.svg(600, 470, "Isometrische tekening van een bedrijfspand met een deur met elektronische lezer")

SECTOREN = {"kantoren": kantoor, "zorg": zorg, "onderwijs": onderwijs, "vve": vve, "verenigingen": verenigingen,
            "recreatie": recreatie, "industrie": industrie, "overheid": overheid}
