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
    def blok(self, x, y, z, w, d, h, top, links, rechts, ramen=None, deur=None, lichtjes=False):
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
                    lk = f' class="anim-licht anim-licht-{(r * 3 + k) % 4}"' if lichtjes and (r * 7 + k * 3) % 5 == 0 else ""
                    uit.append(_poly([P(xx, y + d, zz), P(xx + ww, y + d, zz), P(xx + ww, y + d, zz + hh), P(xx, y + d, zz + hh)], GLAS, lk))
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
    def grond_g(self, binnen, klas=""):
        """<g> met de isometrische grondvlak-matrix: alles erin tekent in (x*s, y*s)-coordinaten van het grondvlak."""
        k = f' class="{klas}"' if klas else ""
        return f'<g transform="matrix({CX:.4f},{CY:.4f},{-CX:.4f},{CY:.4f},{self.ox},{self.oy})"{k}>{binnen}</g>'
    def ellips(self, x, y, rx, ry, kleur, rand=None, dikte=1.5, diepte=-90):
        e = f'<ellipse cx="{x*self.s:.1f}" cy="{y*self.s:.1f}" rx="{rx*self.s:.1f}" ry="{ry*self.s:.1f}" fill="{kleur}"' + (f' stroke="{rand}" stroke-width="{dikte}"' if rand else "") + "/>"
        self.delen.append((diepte, self.grond_g(e)))
    def rondje(self, x, y, r, kleur, diepte=-89):
        self.delen.append((diepte, self.grond_g(f'<circle cx="{x*self.s:.1f}" cy="{y*self.s:.1f}" r="{r*self.s:.1f}" fill="{kleur}"/>')))
    def lijn_grond(self, x1, y1, x2, y2, kleur=STREEP, dikte=1.5, diepte=-89):
        self.delen.append((diepte, self.grond_g(f'<line x1="{x1*self.s:.1f}" y1="{y1*self.s:.1f}" x2="{x2*self.s:.1f}" y2="{y2*self.s:.1f}" stroke="{kleur}" stroke-width="{dikte}"/>')))
    def draaiend(self, cx, cy, binnen, klas, diepte=-88):
        """Groep die in het grondvlak om (cx, cy) draait (CSS-animatie op klas)."""
        self.delen.append((diepte, self.grond_g(f'<g class="{klas}" style="transform-origin:{cx*self.s:.1f}px {cy*self.s:.1f}px">{binnen}</g>')))
    def svg(self, breedte, hoogte, label):
        return (f'<svg viewBox="0 0 {breedte} {hoogte}" width="{breedte}" height="{hoogte}" role="img" aria-label="{label}" '
                f'xmlns="http://www.w3.org/2000/svg" class="iso">' + "".join(d for _, d in sorted(self.delen, key=lambda t: t[0])) + "</svg>")

def _basis(sc, w=9, d=9):
    sc.vlak(0, 0, w, d, GROND)
    sc.vlak(0, d * 0.42, w, 1.2, WEG); sc.zebra(w * 0.15, d * 0.42, 1.6, 1.2)
    sc.vlak(w * 0.42, 0, 1.2, d, WEG)

def kantoor():
    """Kantoren: kantoortorens en flatgebouwen; lichten in de ramen gaan rustig aan en uit, een auto rijdt."""
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 2.6, 2.6, 6.0, LICHT2, MIDDEN, DONKER, ramen=(6, 3), lichtjes=True)
    sc.blok(3.3, 1.2, 0, 1.6, 2.0, 3.6, LICHT2, MIDDEN2, DONKER2, ramen=(4, 2), lichtjes=True)
    sc.blok(5.4, 0.6, 0, 3.2, 2.8, 4.4, WIT_T, WIT_L, WIT_R, ramen=(4, 3), deur=(0.5, 0.7, 1.2), lichtjes=True)
    sc.blok(0.8, 5.6, 0, 3.2, 2.8, 2.6, LICHT2, MIDDEN, DONKER, ramen=(2, 3), lichtjes=True)
    sc.blok(5.6, 5.8, 0, 2.6, 2.6, 5.0, LICHT2, MIDDEN2, DONKER2, ramen=(5, 2), lichtjes=True)
    for x, y in [(4.3, 6.4), (4.6, 8.2), (8.5, 5.0)]: sc.boom(x, y)
    sc.auto(4.6, 4.1, DONKER, klas="anim-auto"); sc.auto(1.2, 4.1, LICHT)
    return sc.svg(420, 320, "Isometrische tekening van kantoortorens en flatgebouwen met toegangscontrole")

def zorg():
    """Zorg: ziekenhuis met groen kruis, apotheek, jeugdinstelling met speelplein; ambulance rijdt, kruis pulseert."""
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.5, 3.4, 4.2, WIT_T, WIT_L, WIT_R, ramen=(4, 3), deur=(1.4, 0.8, 1.2))
    sc.groep("anim-gloed", lambda: (sc.blok(1.55, 1.95, 4.2, 1.4, 0.4, 0.35, GROEN2, GROEN, GROENDONKER), sc.blok(2.05, 1.45, 4.2, 0.4, 1.4, 0.35, GROEN2, GROEN, GROENDONKER)))
    sc.blok(5.5, 0.7, 0, 2.8, 2.6, 1.8, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(0.4, 0.6, 1.1))
    sc.groep("anim-gloed", lambda: (sc.blok(6.5, 3.15, 1.0, 0.7, 0.16, 0.16, GROEN2, GROEN, GROENDONKER), sc.blok(6.75, 3.15, 0.75, 0.2, 0.16, 0.66, GROEN2, GROEN, GROENDONKER)))
    sc.blok(0.8, 5.7, 0, 3.0, 2.6, 1.6, LICHT2, MIDDEN2, DONKER2, ramen=(1, 3), deur=(1.2, 0.6, 1.0))
    sc.vlak(5.6, 5.8, 2.8, 2.6, GROEN2)
    sc.blok(6.2, 6.4, 0, 0.2, 0.2, 1.0, LICHT, LICHT, MIDDEN); sc.blok(7.2, 6.4, 0, 0.2, 0.2, 1.0, LICHT, LICHT, MIDDEN); sc.blok(6.2, 6.4, 1.0, 1.2, 0.2, 0.1, GROEN2, GROEN, GROENDONKER)
    for x, y in [(4.4, 6.6), (4.7, 8.3), (8.6, 4.9)]: sc.boom(x, y)
    sc.ambulance(4.4, 4.1)
    return sc.svg(420, 320, "Isometrische tekening van een ziekenhuis, apotheek en jeugdinstelling met toegangscontrole")

def onderwijs():
    """Onderwijs: basisschool van baksteen met schoolplein, klimrek, glijbaan en fietsenrek; bal stuitert, vlag wappert."""
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.6, 3.2, 2.2, ROOD_T, ROOD_L, ROOD_R, ramen=(1, 4), deur=(1.5, 0.7, 1.2))
    sc.blok(0.5, 0.5, 2.2, 1.6, 3.2, 1.6, ROOD_T, ROOD_L, ROOD_R, ramen=(1, 2))
    sc.vlak(0.8, 5.6, 3.4, 3.0, GROND2)
    for i in range(4): sc.lijn_grond(1.0, 5.9 + i * 0.6, 4.0, 5.9 + i * 0.6, "#FFFFFF", 1)
    sc.blok(1.4, 6.4, 0, 0.2, 0.2, 1.1, LICHT, LICHT, MIDDEN); sc.blok(2.6, 6.4, 0, 0.2, 0.2, 1.1, LICHT, LICHT, MIDDEN); sc.blok(1.4, 6.4, 1.1, 1.4, 0.2, 0.1, GROEN2, GROEN, GROENDONKER)
    sc.blok(3.2, 7.4, 0, 0.9, 0.3, 0.9, LICHT2, LICHT, MIDDEN)
    for i in range(5): sc.blok(5.7 + i * 0.35, 6.0, 0, 0.1, 0.5, 0.4, GRIJS_T, GRIJS_L, GRIJS_R)
    sc.vlag(4.5, 5.8)
    bx, by = sc.P(2.2, 7.0, 0.15)
    sc.groep("anim-bal", lambda: sc.delen.append((2.2 + 7.0, f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3" fill="{LICHT}" stroke="{DONKER}" stroke-width="0.6"/>')))
    sc.blok(5.4, 0.7, 0, 3.0, 2.6, 2.0, ROOD_T, ROOD_L, ROOD_R, ramen=(1, 3))
    for x, y in [(8.5, 7.0), (7.4, 8.2), (5.2, 8.4)]: sc.boom(x, y, 0.5, 1.2)
    return sc.svg(420, 320, "Isometrische tekening van een basisschool met schoolplein en toegangscontrole")

def vve():
    """VvE en vastgoed: verschillende gebouwen door elkaar (flat, rijtjeshuizen, winkel met luifel, kantoortje); een bouwkraan draait langzaam."""
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 2.4, 2.8, 5.0, LICHT2, MIDDEN, DONKER, ramen=(5, 2))
    for i in range(5): sc.blok(2.9, 0.8, 0.8 + i * 0.85, 0.2, 2.2, 0.08, LICHT, LICHT, LICHT2)
    for i in range(3):
        kl = (ROOD_T, ROOD_L, ROOD_R) if i % 2 else (WIT_T, WIT_L, WIT_R)
        sc.blok(3.6 + i * 1.1, 1.0, 0, 1.0, 2.2, 2.0, *kl, ramen=(2, 1))
    sc.blok(6.9, 0.8, 0, 1.6, 2.6, 2.6, ZAND_T, ZAND_L, ZAND_R, ramen=(2, 2), deur=(0.5, 0.6, 1.0))
    sc.blok(0.8, 5.6, 0, 3.0, 2.8, 1.6, WIT_T, WIT_L, WIT_R, ramen=(1, 3))
    sc.blok(0.8, 8.35, 1.1, 3.0, 0.5, 0.08, LICHT, LICHT, MIDDEN)
    sc.blok(5.4, 5.8, 0, 2.0, 2.4, 3.2, MIDDEN2, MIDDEN, DONKER, ramen=(3, 2))
    sc.blok(7.9, 6.6, 0, 0.3, 0.3, 5.2, LICHT2, LICHT, MIDDEN)
    kx, ky = 8.05, 6.75
    arm = (f'<line x1="{kx*24:.1f}" y1="{ky*24:.1f}" x2="{(kx-2.6)*24:.1f}" y2="{ky*24:.1f}" stroke="{DONKER}" stroke-width="2"/>'
           f'<line x1="{kx*24:.1f}" y1="{ky*24:.1f}" x2="{(kx+0.9)*24:.1f}" y2="{ky*24:.1f}" stroke="{DONKER}" stroke-width="3"/>')
    sc.delen.append((100, f'<g transform="translate(0,{-5.2*24:.1f})">' + sc.grond_g(f'<g class="anim-kraan" style="transform-origin:{kx*24:.1f}px {ky*24:.1f}px">{arm}</g>') + "</g>"))
    for x, y in [(4.4, 6.6), (4.7, 8.3)]: sc.boom(x, y)
    return sc.svg(420, 320, "Isometrische tekening van gemengd vastgoed: flat, rijtjeshuizen, winkel en kantoor met toegangscontrole")

def verenigingen():
    """Verenigingen: sportpark met voetbalveld, tennisbaan, basketbalveld en atletiekbaan; bal rolt, loper rondt de baan."""
    sc = Scene(24, 210, 140)
    sc.vlak(0, 0, 9, 9, GROEN2); sc.vlak(0, 4.2, 9, 0.6, WEG); sc.vlak(4.2, 0, 0.6, 9, WEG)
    sc.vlak(0.4, 0.4, 3.6, 3.4, GROEN); sc.lijn_grond(0.4, 2.1, 4.0, 2.1); sc.ellips(2.2, 2.1, 0.5, 0.5, "none", STREEP)
    sc.lijn_grond(0.4, 0.4, 4.0, 0.4); sc.lijn_grond(0.4, 3.8, 4.0, 3.8); sc.lijn_grond(0.4, 0.4, 0.4, 3.8); sc.lijn_grond(4.0, 0.4, 4.0, 3.8)
    sc.groep("anim-bal", lambda: sc.rondje(1.4, 1.4, 0.12, "#FFFFFF", diepte=-50))
    sc.vlak(5.2, 0.4, 3.4, 1.7, "#D9865E"); sc.lijn_grond(6.9, 0.4, 6.9, 2.1, "#FFFFFF", 1); sc.lijn_grond(5.2, 1.25, 8.6, 1.25, "#FFFFFF", 1)
    sc.lijn_grond(5.2, 0.4, 8.6, 0.4, "#FFFFFF", 1); sc.lijn_grond(5.2, 2.1, 8.6, 2.1, "#FFFFFF", 1)
    sc.vlak(5.2, 2.5, 3.4, 1.5, "#C9CED0"); sc.ellips(6.9, 3.25, 0.4, 0.4, "none", "#FFFFFF", 1); sc.lijn_grond(6.9, 2.5, 6.9, 4.0, "#FFFFFF", 1)
    sc.blok(5.25, 3.2, 0, 0.08, 0.08, 1.2, DONKER, DONKER, DONKER); sc.blok(8.5, 3.2, 0, 0.08, 0.08, 1.2, DONKER, DONKER, DONKER)
    sc.ellips(2.6, 6.9, 2.3, 1.7, "#D9865E"); sc.ellips(2.6, 6.9, 1.6, 1.0, GROEN)
    for r in (1.8, 2.05): sc.ellips(2.6, 6.9, r, r * 0.74, "none", "#FFFFFF", 0.8)
    sc.draaiend(2.6, 6.9, f'<circle cx="{(2.6+1.95)*24:.1f}" cy="{6.9*24:.1f}" r="3.2" fill="{DONKER}"/>', "anim-loper")
    sc.blok(6.0, 5.6, 0, 2.6, 2.2, 1.5, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(1.0, 0.6, 1.0))
    for x, y in [(8.6, 8.3), (5.6, 8.6)]: sc.boom(x, y, 0.5, 1.3)
    return sc.svg(420, 320, "Isometrische tekening van een sportpark met voetbalveld, tennisbaan, basketbalveld en atletiekbaan")

def recreatie():
    """Recreatiepark: veel kleine huisjes, enkele luxe bungalows met terras, zwembad en receptie; water beweegt, een auto rijdt het park op."""
    sc = Scene(24, 210, 140); sc.vlak(0, 0, 9, 9, GROEN2); sc.vlak(0, 4.1, 9, 0.8, WEG); sc.vlak(4.1, 0, 0.8, 9, WEG)
    def huisje(x, y, w=1.0, d=0.9, h=0.8, top=LICHT2, l=MIDDEN2, r=DONKER2):
        sc.blok(x, y, 0, w, d, h, top, l, r, ramen=(1, 1))
        P = sc.P; a, b, c, dd = P(x, y, h), P(x + w, y, h), P(x + w, y + d, h), P(x, y + d, h); t = P(x + w / 2, y + d / 2, h + 0.55)
        sc.delen.append((x + w + y + d + 0.02, _poly([a, b, t], ROOD_R) + _poly([b, c, t], ROOD_L) + _poly([c, dd, t], ROOD_T)))
    for x, y in [(0.4, 0.4), (1.7, 0.6), (3.0, 0.4), (0.5, 1.9), (1.9, 2.1), (3.1, 1.9), (0.6, 3.1), (2.2, 3.2)]: huisje(x, y)
    for x, y in [(5.4, 0.6), (7.2, 0.8), (5.4, 2.4), (7.2, 2.6)]:
        huisje(x, y, 1.5, 1.3, 1.1, WIT_T, WIT_L, WIT_R); sc.vlak(x, y + 1.3, 1.5, 0.5, ZAND_T)
    sc.blok(0.6, 5.5, 0, 3.0, 2.4, 1.4, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(1.2, 0.6, 1.0))
    sc.vlak(5.4, 5.6, 3.0, 2.8, LICHT); sc.groep("anim-water", lambda: sc.vlak(5.6, 5.8, 2.6, 2.4, GLAS2, 0.01))
    for x, y in [(4.0, 6.6), (2.0, 8.5), (8.7, 4.7), (3.6, 3.9)]: sc.boom(x, y, 0.6, 1.6)
    sc.auto(4.15, 4.2, DONKER, klas="anim-auto")
    return sc.svg(420, 320, "Isometrische tekening van een recreatiepark met huisjes, bungalows en zwembad met toegangscontrole")

def industrie():
    """Industrie en logistiek: bedrijvenpark met grote hallen, laaddocks, vrachtwagens en een heftruck; meerdere voertuigen rijden, de schoorsteen rookt."""
    sc = Scene(24, 210, 140); sc.vlak(0, 0, 9, 9, GROND); sc.vlak(0, 4.0, 9, 1.2, WEG); sc.vlak(4.0, 0, 1.2, 9, WEG); sc.zebra(1.2, 4.0, 1.4, 1.2)
    sc.blok(0.4, 0.4, 0, 3.4, 3.2, 2.0, GRIJS_T, GRIJS_L, GRIJS_R, deur=(0.4, 1.4, 1.5))
    for i in range(3):
        P = sc.P; x = 0.4 + i * 1.133; a, b, c, d = P(x, 0.4, 2.0), P(x + 1.133, 0.4, 2.0), P(x + 1.133, 3.6, 2.0), P(x, 3.6, 2.0)
        t1, t2 = P(x + 0.3, 0.4, 2.55), P(x + 0.3, 3.6, 2.55)
        sc.delen.append((x + 1.133 + 3.6 + 0.03, _poly([a, t1, t2, d], GLAS) + _poly([t1, b, c, t2], GRIJS_T)))
    sc.blok(5.5, 0.4, 0, 3.2, 3.2, 2.6, MIDDEN2, MIDDEN, DONKER, ramen=(1, 4))
    for i in range(3): sc.blok(5.7 + i * 1.0, 3.6, 0, 0.7, 0.05, 1.1, DONKER, DONKER, DONKER)
    sc.blok(0.4, 5.6, 0, 3.4, 3.0, 1.6, GRIJS_T, GRIJS_L, GRIJS_R)
    sc.blok(3.4, 8.2, 0, 0.5, 0.5, 4.2, GRIJS_T, GRIJS_L, GRIJS_R)
    rx, ry = sc.P(3.65, 8.45, 4.2)
    sc.groep("anim-rook", lambda: sc.delen.append((3.65 + 8.45 + 0.1, f'<circle cx="{rx:.1f}" cy="{ry-6:.1f}" r="5" fill="#D5DBE1" opacity=".8"/><circle cx="{rx+4:.1f}" cy="{ry-14:.1f}" r="4" fill="#D5DBE1" opacity=".6"/>')))
    sc.blok(5.5, 5.6, 0, 3.2, 3.0, 1.2, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(0.5, 0.6, 1.0))
    sc.auto(4.4, 4.2, GRIJS_R, klas="anim-auto", lang=2.4)
    sc.auto(4.2, 4.25, DONKER, klas="anim-auto-2")
    sc.auto(6.2, 4.9, GROENDONKER, klas="anim-heftruck", lang=0.9)
    return sc.svg(420, 320, "Isometrische tekening van een bedrijvenpark met hallen, laaddocks en vrachtwagens met toegangscontrole")

def overheid():
    """Overheid: gemeentehuis met zuilen en een Haags regeringsgebouw met torens; vlaggen wapperen, de vijver beweegt."""
    sc = Scene(24, 210, 140); _basis(sc)
    sc.blok(0.5, 0.5, 0, 3.6, 3.4, 3.0, ZAND_T, ZAND_L, ZAND_R, ramen=(3, 4), deur=(1.5, 0.8, 1.3))
    for i in range(4): sc.blok(0.7 + i * 0.85, 3.9, 0, 0.3, 0.3, 3.0, ZAND_T, ZAND_T, ZAND_L)
    sc.blok(1.6, 1.6, 3.0, 1.4, 1.4, 0.8, ZAND_T, ZAND_L, ZAND_R)
    sc.vlag(2.3, 2.3, h=5.2, kleur=DONKER)
    sc.blok(5.4, 0.6, 0, 3.2, 3.0, 2.6, ROOD_T, ROOD_L, ROOD_R, ramen=(2, 4), deur=(1.3, 0.7, 1.4))
    for tx in (5.4, 7.9):
        sc.blok(tx, 0.6, 0, 0.7, 0.7, 4.2, ROOD_T, ROOD_L, ROOD_R, ramen=(3, 1))
        P = sc.P; a, b, c, d = P(tx, 0.6, 4.2), P(tx + 0.7, 0.6, 4.2), P(tx + 0.7, 1.3, 4.2), P(tx, 1.3, 4.2); t = P(tx + 0.35, 0.95, 5.6)
        sc.delen.append((tx + 0.7 + 1.3 + 0.05, _poly([a, b, t], DONKER) + _poly([b, c, t], DONKER2) + _poly([c, d, t], MIDDEN)))
    sc.vlag(7.05, 0.75, h=4.8, kleur=LICHT)
    sc.vlak(0.9, 5.7, 3.2, 2.8, GROND2); sc.zebra(1.2, 5.9, 2.6, 0.4, 3)
    sc.ellips(2.5, 7.4, 0.7, 0.7, LICHT); sc.groep("anim-water", lambda: sc.ellips(2.5, 7.4, 0.5, 0.5, GLAS2, diepte=-89))
    sc.blok(5.6, 5.8, 0, 3.0, 2.6, 1.8, WIT_T, WIT_L, WIT_R, ramen=(1, 3))
    for x, y in [(4.5, 7.9), (8.6, 8.4), (4.6, 5.9)]: sc.boom(x, y)
    return sc.svg(420, 320, "Isometrische tekening van een gemeentehuis en een regeringsgebouw met toegangscontrole")

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
