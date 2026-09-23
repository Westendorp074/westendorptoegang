"""Isometrische illustraties als SVG, getekend in code (geen stock, geen AI-beeld).
Kleuren uit het logopakket. Elke scène is een functie die een <svg> teruggeeft; build.py schrijft ze als los bestand.
Projectie: x loopt naar rechtsonder, y naar linksonder, z omhoog.

Tekenvolgorde: elk object heeft een doos (x0,y0,z0,x1,y1,z1). Twee objecten die elkaar op het scherm overlappen worden
gesorteerd met de scheidingsregel (A staat achter B als A helemaal links, achter of onder B ligt); daaruit volgt een
topologische volgorde. Dat is de gangbare methode voor isometrische scènes en voorkomt dat een vlag achter een pand
verdwijnt of een rijdende auto over een gebouw heen tekent. Rijdende objecten krijgen een doos over hun hele rijpad.
"""
import math

# Palet
DONKER, MIDDEN, LICHT = "#02295B", "#1B68C0", "#49BFFE"
DONKER2, MIDDEN2, LICHT2 = "#0B3A78", "#3A84D6", "#8AD6FF"   # lichtere varianten voor bovenvlakken
GLAS, GLAS2 = "#BFE6FF", "#E3F4FF"
GROEN, GROEN2, GROENDONKER = "#3DBE7A", "#7ADCA5", "#177A42"
GROND, GROND2, WEG, STREEP = "#EEF1F4", "#E2E7EC", "#D5DBE1", "#FFFFFF"
FIETSPAD = "#D9A9A0"                                            # rood asfalt van een Nederlands fietspad
STAM = "#6B5B4A"
WIT_T, WIT_L, WIT_R = "#F4F7FA", "#DDE5EE", "#C3CFDC"        # wit gebouw (zorg)
GRIJS_T, GRIJS_L, GRIJS_R = "#DDE2E7", "#B8C0C8", "#98A2AC"   # staal (industrie)
ZAND_T, ZAND_L, ZAND_R = "#F1E9DA", "#D9CDB5", "#BFB093"      # zandsteen (overheid)
ROOD_T, ROOD_L, ROOD_R = "#E8A79A", "#C9705F", "#A4523F"      # baksteen (school, woningen)
DAK_T, DAK_L, DAK_R = "#8C6F63", "#6E534A", "#513A33"         # dakpannen
KRUIS_T, KRUIS_L, KRUIS_R = "#F05A4E", "#D9362B", "#A8271E"   # rood kruis (ziekenhuis)
GEEL_T, GEEL_L, GEEL_R = "#F7D774", "#E9B93A", "#C4951C"      # ambulance
NL_ROOD, NL_BLAUW = "#AE1C28", "#21468B"                      # Nederlandse vlag
WIEL = "#1F2428"
PAAL = "#6B7680"
SCHADUW = "#14232E"                                             # slagschaduw (met lage dekking)
KOZIJN, KOZIJN2 = "#8FA9BE", "#A9BFD0"                          # raamkozijnen op het linker- en rechtervlak
STOEPRAND = "#C3CBD3"

CX, CY = math.cos(math.radians(30)), math.sin(math.radians(30))
EPS = 1e-6

# Rijpad van bewegende groepen in wereldeenheden (moet kloppen met de keyframes in build.ISO_CSS bij s=19):
# rijden: ±62 px in schermbreedte = ±3.8 in x; rijden-y: ±58 px = ±3.6 in y; heftruck: 26 px naar linksonder = 1.6 in y.
REK = {"anim-auto": (3.8, 0, 3.8, 0), "anim-auto-2": (3.8, 0, 3.8, 0), "anim-fiets": (3.8, 0, 3.8, 0),
       "anim-auto-y": (0, 3.6, 0, 3.6), "anim-auto-y-terug": (0, 3.6, 0, 3.6), "anim-heftruck": (0, 0, 0, 1.7), "anim-bal": (0, 0, 1.2, 0.2)}

def _tint(kleur, f):
    """Zelfde kleur, iets donkerder (f < 1) of lichter (f > 1)."""
    r, g, b = int(kleur[1:3], 16), int(kleur[3:5], 16), int(kleur[5:7], 16)
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c * f))) for c in (r, g, b))

def _p(x, y, z, s):
    return (x - y) * CX * s, (x + y) * CY * s - z * s

def _poly(punten, fill, extra=""):
    d = " ".join(f"{px:.0f},{py:.0f}" for px, py in punten)
    return f'<polygon points="{d}" fill="{fill}"{extra}/>'

class Scene:
    def __init__(self, s=22, ox=0, oy=0):
        self.s, self.ox, self.oy, self.delen = s, ox, oy, []   # delen: [doos, svg, grond, pad]
        self._bomen = 0
    def P(self, x, y, z):
        px, py = _p(x, y, z, self.s); return px + self.ox, py + self.oy
    def voeg(self, doos, svg, grond=False, pad=(0, 0, 0, 0)):
        self.delen.append([doos, svg, grond, pad])

    # ---------- grondvlak ----------
    def vlak(self, x, y, w, d, kleur, z=0):
        """Plat vlak op de grond (weg, gras, plein). z alleen als laagvolgorde binnen het grondvlak. Gras en bestrating krijgen een fijne textuur."""
        fill = {GROEN2: "url(#p-gras)", GROND2: "url(#p-tegels)", WEG: "url(#p-asfalt)"}.get(kleur, kleur)
        self.voeg((x, y, z, x + w, y + d, z), _poly([self.P(x, y, 0), self.P(x + w, y, 0), self.P(x + w, y + d, 0), self.P(x, y + d, 0)], fill), grond=True)
    def zebra(self, x, y, w, d, n=5):
        for i in range(n):
            self.vlak(x + w * i / n + w / n * 0.15, y, w / n * 0.5, d, STREEP, 0.01)
    def grond_g(self, binnen, klas=""):
        """<g> met de isometrische grondvlak-matrix: alles erin tekent in (x*s, y*s)-coordinaten van het grondvlak."""
        k = f' class="{klas}"' if klas else ""
        return f'<g transform="matrix({CX:.4f},{CY:.4f},{-CX:.4f},{CY:.4f},{self.ox},{self.oy})"{k}>{binnen}</g>'
    def ellips(self, x, y, rx, ry, kleur, rand=None, dikte=1.5, z=0.01):
        e = f'<ellipse cx="{x*self.s:.1f}" cy="{y*self.s:.1f}" rx="{rx*self.s:.1f}" ry="{ry*self.s:.1f}" fill="{kleur}"' + (f' stroke="{rand}" stroke-width="{dikte}"' if rand else "") + "/>"
        self.voeg((x - rx, y - ry, z, x + rx, y + ry, z), self.grond_g(e), grond=True)
    def rondje(self, x, y, r, kleur, z=0.02):
        self.voeg((x - r, y - r, z, x + r, y + r, z), self.grond_g(f'<circle cx="{x*self.s:.1f}" cy="{y*self.s:.1f}" r="{r*self.s:.1f}" fill="{kleur}"/>'), grond=True)
    def lijn_grond(self, x1, y1, x2, y2, kleur=STREEP, dikte=1.5, z=0.02):
        self.voeg((min(x1, x2), min(y1, y2), z, max(x1, x2), max(y1, y2), z),
                  self.grond_g(f'<line x1="{x1*self.s:.1f}" y1="{y1*self.s:.1f}" x2="{x2*self.s:.1f}" y2="{y2*self.s:.1f}" stroke="{kleur}" stroke-width="{dikte}"/>'), grond=True)
    def rechthoek_grond(self, x, y, w, d, kleur=STREEP, dikte=1.2, z=0.02):
        self.voeg((x, y, z, x + w, y + d, z), self.grond_g(f'<rect x="{x*self.s:.1f}" y="{y*self.s:.1f}" width="{w*self.s:.1f}" height="{d*self.s:.1f}" fill="none" stroke="{kleur}" stroke-width="{dikte}"/>'), grond=True)
    def draaiend(self, cx, cy, binnen, klas, z=0.03):
        """Groep die in het grondvlak om (cx, cy) draait (CSS-animatie op klas)."""
        self.voeg((cx - 2, cy - 2, z, cx + 2, cy + 2, z), self.grond_g(f'<g class="{klas}" style="transform-origin:{cx*self.s:.1f}px {cy*self.s:.1f}px">{binnen}</g>'), grond=True)
    def dak_cirkel(self, x, y, z, r, kleur, rand=None, tekst=None):
        """Cirkel op een dak (helikopterplatform), getekend in het grondvlak en omhoog verschoven."""
        s = self.s
        binnen = f'<circle cx="{x*s:.1f}" cy="{y*s:.1f}" r="{r*s:.1f}" fill="{kleur}"' + (f' stroke="{rand}" stroke-width="1.6"' if rand else "") + "/>"
        if tekst: binnen += f'<text x="{x*s:.1f}" y="{y*s + r*s*0.42:.1f}" font-size="{r*s*1.25:.0f}" font-weight="700" fill="{rand or STREEP}" text-anchor="middle" font-family="Arial,sans-serif">{tekst}</text>'
        self.voeg((x - r, y - r, z, x + r, y + r, z), f'<g transform="translate(0,{-z*s:.1f})">' + self.grond_g(binnen) + "</g>")

    # ---------- gebouwen ----------
    def blok(self, x, y, z, w, d, h, top, links, rechts, ramen=None, deur=None, lichtjes=False, deur_anim=False, dak=None):
        """Gebouwblok: drie vlakken. ramen=(rijen, kolommen) tekent glas op beide zijvlakken; deur=(dx, breedte, hoogte) met lezer."""
        P = self.P; uit = []
        if z == 0 and h >= 0.3:                                                                                   # zachte slagschaduw op de grond, naar rechtsvoor
            sx, sy = min(0.9, 0.22 * h), min(0.35, 0.07 * h)
            self.voeg((x, y, 0.003, x + w + sx, y + d + sy, 0.003), _poly([P(x + sx, y + sy, 0), P(x + w + sx, y + sy, 0), P(x + w + sx, y + d + sy, 0), P(x + sx, y + d + sy, 0)], SCHADUW, ' opacity=".09"'), grond=True)
        uit.append(_poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], links))    # linkervlak (y=d)
        uit.append(_poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)], rechts))   # rechtervlak (x=w)
        mat = {ROOD_L: "steen", ZAND_L: "natuursteen", WIT_L: "plaat", GRIJS_L: "plaat"}.get(links)
        if mat and z == 0 and h >= 1.0 and w >= 0.8 and d >= 0.8:                                                # gevelstructuur, alleen op gebouwen
            uit.append(_poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], f"url(#p-{mat}-l)"))
            uit.append(_poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)], f"url(#p-{mat}-r)"))
        uit.append(_poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)], top, f' stroke="{rechts}" stroke-width=".6" stroke-opacity=".45"'))   # bovenvlak met dakrand
        if h >= 1.0 and w >= 0.8 and d >= 0.8:                                                                  # dak: binnenvlak met grind achter de dakrand
            i = min(0.18, w * 0.12, d * 0.12)
            uit.append(_poly([P(x + i, y + i, z + h), P(x + w - i, y + i, z + h), P(x + w - i, y + d - i, z + h), P(x + i, y + d - i, z + h)], _tint(top, 0.965)))
            uit.append(_poly([P(x + i, y + i, z + h), P(x + w - i, y + i, z + h), P(x + w - i, y + d - i, z + h), P(x + i, y + d - i, z + h)], "url(#p-grind)"))
        if dak is None and z == 0 and w >= 1.8 and d >= 1.8 and h >= 1.4: dak = ("zon", "licht", "kast")[int((x * 7 + y * 13) * 10) % 3]
        if dak == "zon":                                                                                          # zonnepanelen in rijen
            i = 0.35; kol = int((w - 2 * i) / 0.55); rij = int((d - 2 * i) / 0.45)
            for r in range(rij):
                for k in range(kol):
                    px, py = x + i + k * 0.55, y + i + r * 0.45
                    uit.append(_poly([P(px, py, z + h + 0.03), P(px + 0.45, py, z + h + 0.03), P(px + 0.45, py + 0.34, z + h + 0.12), P(px, py + 0.34, z + h + 0.12)], "#1F3A5F", ' stroke="#4A6C96" stroke-width=".4"'))
        elif dak == "licht":                                                                                      # lichtstraten
            for k in range(int((w - 0.6) / 0.9)):
                px = x + 0.4 + k * 0.9
                uit.append(_poly([P(px, y + 0.35, z + h + 0.01), P(px + 0.45, y + 0.35, z + h + 0.01), P(px + 0.45, y + d - 0.35, z + h + 0.01), P(px, y + d - 0.35, z + h + 0.01)], GLAS, f' stroke="{KOZIJN}" stroke-width=".5"'))
        if z == 0 and w >= 1.4 and d >= 1.4 and h >= 1.0:                                                        # ontluchtingspijp
            vx, vy = x + w - 0.35, y + 0.3; v0, v1 = P(vx, vy, z + h), P(vx, vy, z + h + 0.3)
            uit.append(f'<line x1="{v0[0]:.1f}" y1="{v0[1]:.1f}" x2="{v1[0]:.1f}" y2="{v1[1]:.1f}" stroke="{GRIJS_R}" stroke-width="2.2"/><ellipse cx="{v1[0]:.1f}" cy="{v1[1]:.1f}" rx="1.3" ry=".7" fill="{GRIJS_T}"/>')
        if z == 0 and h >= 1.0:                                                                                   # plint onderaan beide gevels
            uit.append(_poly([P(x, y + d, 0), P(x + w, y + d, 0), P(x + w, y + d, 0.12), P(x, y + d, 0.12)], _tint(links, 0.86)))
            uit.append(_poly([P(x + w, y, 0), P(x + w, y + d, 0), P(x + w, y + d, 0.12), P(x + w, y, 0.12)], _tint(rechts, 0.86)))
        h0, h1 = P(x + w, y + d, z), P(x + w, y + d, z + h)                                                       # hoekkant
        uit.append(f'<line x1="{h0[0]:.1f}" y1="{h0[1]:.1f}" x2="{h1[0]:.1f}" y2="{h1[1]:.1f}" stroke="{_tint(rechts, 0.75)}" stroke-width=".6"/>')
        if ramen:
            rijen, kol = ramen
            for r in range(1, rijen):                                                                             # verdiepingslijnen
                zz = z + h * r / rijen
                a0, a1, b0, b1 = P(x, y + d, zz), P(x + w, y + d, zz), P(x + w, y, zz), P(x + w, y + d, zz)
                uit.append(f'<line x1="{a0[0]:.0f}" y1="{a0[1]:.0f}" x2="{a1[0]:.0f}" y2="{a1[1]:.0f}" stroke="{_tint(links, 0.8)}" stroke-width=".5" stroke-opacity=".55"/>'
                           f'<line x1="{b0[0]:.0f}" y1="{b0[1]:.0f}" x2="{b1[0]:.0f}" y2="{b1[1]:.0f}" stroke="{_tint(rechts, 0.8)}" stroke-width=".5" stroke-opacity=".55"/>')
            for r in range(rijen):
                zz = z + h * (r + 0.55) / rijen; hh = h / rijen * 0.45
                for k in range(kol):
                    xx = x + w * (k + 0.2) / kol; ww = w / kol * 0.6
                    lk = f' class="anim-licht anim-licht-{(r * 3 + k) % 4}"' if lichtjes and (r * 7 + k * 3) % 5 == 0 else ""
                    uit.append(_poly([P(xx, y + d, zz), P(xx + ww, y + d, zz), P(xx + ww, y + d, zz + hh), P(xx, y + d, zz + hh)], GLAS, lk + f' stroke="{KOZIJN}" stroke-width=".5"'))
                    m0, m1 = P(xx + ww / 2, y + d, zz), P(xx + ww / 2, y + d, zz + hh)                                # tussenstijl
                    uit.append(f'<line x1="{m0[0]:.0f}" y1="{m0[1]:.0f}" x2="{m1[0]:.0f}" y2="{m1[1]:.0f}" stroke="{KOZIJN}" stroke-width=".5"/>')
                    v0, v1 = P(xx - 0.04, y + d, zz - 0.02), P(xx + ww + 0.04, y + d, zz - 0.02)                        # vensterbank
                    uit.append(f'<line x1="{v0[0]:.1f}" y1="{v0[1]:.1f}" x2="{v1[0]:.1f}" y2="{v1[1]:.1f}" stroke="{_tint(links, 0.8)}" stroke-width=".9"/>')
                    yy = y + d * (k + 0.2) / kol; dd = d / kol * 0.6
                    uit.append(_poly([P(x + w, yy, zz), P(x + w, yy + dd, zz), P(x + w, yy + dd, zz + hh), P(x + w, yy, zz + hh)], GLAS2, f' stroke="{KOZIJN2}" stroke-width=".5"'))
                    m0, m1 = P(x + w, yy + dd / 2, zz), P(x + w, yy + dd / 2, zz + hh)
                    uit.append(f'<line x1="{m0[0]:.0f}" y1="{m0[1]:.0f}" x2="{m1[0]:.0f}" y2="{m1[1]:.0f}" stroke="{KOZIJN2}" stroke-width=".5"/>')
        if deur:
            dx, dw, dh = deur
            if deur_anim: dw, dh = max(dw, 0.8), max(dh, 1.3)                                                     # de deur met animatie moet goed zichtbaar zijn
            uit.append(_poly([P(x + dx, y + d, z), P(x + dx + dw, y + d, z), P(x + dx + dw, y + d, z + dh), P(x + dx, y + d, z + dh)], KOZIJN, f' stroke="{KOZIJN}" stroke-width=".6"') if deur_anim else "")   # deuropening (zichtbaar als de deur open is)
            deurvlak = _poly([P(x + dx, y + d, z), P(x + dx + dw, y + d, z), P(x + dx + dw, y + d, z + dh), P(x + dx, y + d, z + dh)], DONKER, f' stroke="{KOZIJN}" stroke-width=".6"')
            kx, ky = P(x + dx + dw * 0.8, y + d, z + dh * 0.5)                                                        # deurklink
            deurvlak += f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="1" fill="{LICHT}"/>'
            if deur_anim:
                sx, sy = P(x + dx, y + d, z)                                                                          # scharnierkant
                uit.append(f'<g class="anim-deur" style="transform-origin:{sx:.1f}px {sy:.1f}px">{deurvlak}</g>')
            else: uit.append(deurvlak)
            lx, ly = P(x + dx + dw + 0.35, y + d, z + dh * 0.55)
            uit.append(f'<rect x="{lx-3:.1f}" y="{ly-6:.1f}" width="6" height="12" rx="1" fill="#FFFFFF" stroke="{DONKER}" stroke-width="0.6"/>'
                       f'<circle class="{"led-deur" if deur_anim else "led"}" cx="{lx:.1f}" cy="{ly-2:.1f}" r="1.6" fill="{GROEN}"/>')
        self.voeg((x, y, z, x + w, y + d, z + h), "".join(uit))
        if deur and deur_anim:                                                                                    # persoon voor de lezer, houdt de pas ertegen
            self.persoon(x + dx + dw + 0.35, y + d + 0.55, MIDDEN, pas=(lx, ly), schaal=1.3)
    def dak(self, x, y, z, w, d, hoog, nok="y", kl=(DAK_T, DAK_L, DAK_R)):
        """Zadeldak. nok 'y': nok loopt in de y-richting (schuine vlakken links en rechts); nok 'x': nok in de x-richting."""
        P = self.P; t, l, r = kl
        pan = f' stroke="{_tint(r, 0.8)}" stroke-width=".45"'
        if nok == "y":
            n0, n1 = P(x + w / 2, y, z + hoog), P(x + w / 2, y + d, z + hoog)
            svg = (_poly([n0, P(x, y, z), P(x, y + d, z), n1], t)            # achterste schuine vlak (soms net zichtbaar)
                   + _poly([n0, P(x + w, y, z), P(x + w, y + d, z), n1], r)  # voorste schuine vlak
                   + _poly([P(x, y + d, z), P(x + w, y + d, z), n1], l))     # topgevel
            for f in (0.25, 0.5, 0.75):                                                                               # pannenlijnen op het voorste vlak
                a, b = P(x + w / 2 + (w / 2) * f, y, z + hoog * (1 - f)), P(x + w / 2 + (w / 2) * f, y + d, z + hoog * (1 - f))
                svg += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"{pan}/>'
            g0, g1 = P(x + w + 0.03, y, z - 0.02), P(x + w + 0.03, y + d, z - 0.02)                                     # dakgoot
        else:
            n0, n1 = P(x, y + d / 2, z + hoog), P(x + w, y + d / 2, z + hoog)
            svg = (_poly([n0, P(x, y, z), P(x + w, y, z), n1], t)
                   + _poly([n0, P(x, y + d, z), P(x + w, y + d, z), n1], l)
                   + _poly([P(x + w, y, z), P(x + w, y + d, z), n1], r))
            for f in (0.25, 0.5, 0.75):
                a, b = P(x, y + d / 2 + (d / 2) * f, z + hoog * (1 - f)), P(x + w, y + d / 2 + (d / 2) * f, z + hoog * (1 - f))
                svg += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"{pan}/>'
            g0, g1 = P(x, y + d + 0.03, z - 0.02), P(x + w, y + d + 0.03, z - 0.02)
        svg += (f'<line x1="{n0[0]:.1f}" y1="{n0[1]:.1f}" x2="{n1[0]:.1f}" y2="{n1[1]:.1f}" stroke="{_tint(r, 0.7)}" stroke-width="1"/>'          # nok
                f'<line x1="{g0[0]:.1f}" y1="{g0[1]:.1f}" x2="{g1[0]:.1f}" y2="{g1[1]:.1f}" stroke="{GRIJS_R}" stroke-width="1.2"/>')            # dakgoot
        self.voeg((x, y, z, x + w, y + d, z + hoog), svg)
    def spits(self, x, y, z, w, d, hoog, kl=(DONKER2, DONKER, MIDDEN)):
        """Piramidedak (torenspits)."""
        P = self.P; a, b, c, dd = P(x, y, z), P(x + w, y, z), P(x + w, y + d, z), P(x, y + d, z); t = P(x + w / 2, y + d / 2, z + hoog)
        self.voeg((x, y, z, x + w, y + d, z + hoog), _poly([a, b, t], kl[0]) + _poly([dd, a, t], kl[0]) + _poly([b, c, t], kl[2]) + _poly([c, dd, t], kl[1]))
    def huis(self, x, y, w, d, h, kl, dakhoog=0.6, nok="y", deur=None, ramen=(1, 1), schoorsteen=False):
        self.blok(x, y, 0, w, d, h, *kl, ramen=ramen, deur=deur)
        self.dak(x, y, h, w, d, dakhoog, nok)
        if schoorsteen: self.blok(x + w * 0.7, y + d * 0.35, h + dakhoog * 0.5, 0.18, 0.18, 0.45, GRIJS_T, GRIJS_L, GRIJS_R)
    def kruis_gevel(self, x, y, z, b, h, kleur, zijde="links", klas=None):
        """Plat kruis op een gevel. zijde 'links': gevelvlak y=const (geef y van de gevel), 'rechts': gevelvlak x=const. (x,y,z) is het midden."""
        P = self.P; dik = b * 0.32
        if zijde == "links":
            R = lambda x0, z0, x1, z1: _poly([P(x0, y, z0), P(x1, y, z0), P(x1, y, z1), P(x0, y, z1)], kleur)
            svg = R(x - b / 2, z - dik / 2, x + b / 2, z + dik / 2) + R(x - dik / 2, z - h / 2, x + dik / 2, z + h / 2)
            doos = (x - b / 2, y, z - h / 2, x + b / 2, y, z + h / 2)
        else:
            R = lambda y0, z0, y1, z1: _poly([P(x, y0, z0), P(x, y1, z0), P(x, y1, z1), P(x, y0, z1)], kleur)
            svg = R(y - b / 2, z - dik / 2, y + b / 2, z + dik / 2) + R(y - dik / 2, z - h / 2, y + dik / 2, z + h / 2)
            doos = (x, y - b / 2, z - h / 2, x, y + b / 2, z + h / 2)
        self.voeg(doos, f'<g class="{klas}">{svg}</g>' if klas else svg)
    def klok(self, x, y, z, r=4.5):
        """Klok op een gevel (x, y op het gevelvlak)."""
        cx, cy = self.P(x, y, z)
        self.voeg((x, y, z - 0.2, x, y, z + 0.2), f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#FFFFFF" stroke="{DONKER}" stroke-width="1"/>'
                  f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{cy-r*0.7:.1f}" stroke="{DONKER}" stroke-width="1"/><line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx+r*0.55:.1f}" y2="{cy+r*0.2:.1f}" stroke="{DONKER}" stroke-width="1"/>', pad=(r, r, r, r))
    def zuilen(self, x, y, n, h, kl=ZAND_T, afstand=0.75, dik=0.22):
        for i in range(n): self.blok(x + i * afstand, y, 0, dik, dik, h, kl, kl, ZAND_L)
    def balkons(self, x, y, z0, n_verd, n_per, w, stap, kleur=LICHT):
        """Balkons op het linkervlak (gevel y=const): plaat plus reling."""
        for v in range(n_verd):
            for k in range(n_per):
                bx = x + k * (w + 0.25) + 0.2; z = z0 + v * stap
                self.blok(bx, y, z, w, 0.35, 0.06, LICHT2, kleur, kleur)
                self.blok(bx, y + 0.33, z + 0.06, w, 0.02, 0.32, GLAS, GLAS, GLAS)
    def cilinder(self, x, y, r, h, top, zij):
        s = self.s; cx, cy = self.P(x, y, 0); rx, ry = 1.22 * r * s, 0.71 * r * s
        self.voeg((x - r, y - r, 0, x + r, y + r, h), f'<rect x="{cx-rx:.1f}" y="{cy-h*s:.1f}" width="{2*rx:.1f}" height="{h*s:.1f}" fill="{zij}"/>'
                  f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{zij}"/><ellipse cx="{cx:.1f}" cy="{cy-h*s:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{top}"/>')
    def hek(self, x, y, w, d, h=0.45, kleur=PAAL):
        """Laag hek langs de rand van een rechthoek (alleen de twee zichtbare zijden)."""
        P = self.P; uit = []
        for (a, b) in [((x, y + d), (x + w, y + d)), ((x + w, y), (x + w, y + d))]:
            a0, a1 = P(*a, 0), P(*a, h); b0, b1 = P(*b, 0), P(*b, h)
            uit.append(f'<line x1="{a1[0]:.0f}" y1="{a1[1]:.0f}" x2="{b1[0]:.0f}" y2="{b1[1]:.0f}" stroke="{kleur}" stroke-width="1"/>')
            n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.6))
            for i in range(n + 1):
                px, py = a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n
                p0, p1 = P(px, py, 0), P(px, py, h)
                uit.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="{kleur}" stroke-width="1"/>')
        self.voeg((x, y + d, 0, x + w, y + d, h), uit[0] + "".join(uit[1:1 + n + 1]))
        self.voeg((x + w, y, 0, x + w, y + d, h), "".join(uit[1 + n + 1:]))

    # ---------- straatmeubilair ----------
    def boom(self, x, y, r=0.55, h=1.4, wind=True):
        r = r * (1 + 0.12 * ((self._bomen % 3) - 1)); h = h * (1 + 0.08 * ((self._bomen % 2) - 0.5))            # geen twee bomen precies gelijk
        P = self.P; bx, by = P(x, y, 0); tx, ty = P(x, y, h); rs = r * self.s
        self.voeg((x, y, 0.003, x + r, y + r, 0.003), self.grond_g(f'<ellipse cx="{(x + 0.3 * r) * self.s:.1f}" cy="{(y + 0.15 * r) * self.s:.1f}" rx="{r * self.s * 0.9:.1f}" ry="{r * self.s * 0.6:.1f}" fill="{SCHADUW}" opacity=".1"/>'), grond=True)
        svg = (f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{STAM}" stroke-width="2.4"/>'
               f'<circle cx="{tx:.1f}" cy="{ty - rs * 0.5:.1f}" r="{rs:.1f}" fill="{GROEN}"/>'
               f'<circle cx="{tx + rs * 0.22:.1f}" cy="{ty - rs * 0.3:.1f}" r="{rs * 0.62:.1f}" fill="{GROENDONKER}" opacity=".28"/>'
               f'<circle cx="{tx - rs * 0.3:.1f}" cy="{ty - rs * 0.7:.1f}" r="{rs * 0.55:.1f}" fill="{GROEN2}"/>')
        if wind:
            svg = f'<g class="anim-boom anim-boom-{self._bomen % 3}" style="transform-origin:{bx:.1f}px {by:.1f}px">{svg}</g>'; self._bomen += 1
        self.voeg((x - r, y - r, 0, x + r, y + r, h + 1.3 * r), svg, pad=(4, 2, 4, 2))
    def persoon(self, x, y, kleur=MIDDEN, pas=None, schaal=1.0):
        """Figuur: schaduw, benen, lijf, arm, hoofd met haar. pas=(lx, ly): de persoon houdt een pas in de hand en brengt die met de arm
        naar de lezer op (lx, ly); de arm draait om de schouder, dus de pas blijft altijd in de hand."""
        k = schaal; bx, by = self.P(x, y, 0)
        huid, haar, broek = "#F1C9A6", "#5A4636", DONKER
        self.voeg((x, y, 0.003, x + 0.2, y + 0.1, 0.003), self.grond_g(f'<ellipse cx="{x*self.s:.1f}" cy="{y*self.s:.1f}" rx="{3*k:.1f}" ry="{2*k:.1f}" fill="{SCHADUW}" opacity=".16"/>'), grond=True)
        lijf = (f'<line x1="{bx-1*k:.1f}" y1="{by-3*k:.1f}" x2="{bx-1*k:.1f}" y2="{by:.1f}" stroke="{broek}" stroke-width="{1.4*k:.1f}" stroke-linecap="round"/>'
                f'<line x1="{bx+1*k:.1f}" y1="{by-3*k:.1f}" x2="{bx+1*k:.1f}" y2="{by:.1f}" stroke="{broek}" stroke-width="{1.4*k:.1f}" stroke-linecap="round"/>'
                f'<rect x="{bx-2.4*k:.1f}" y="{by-11.5*k:.1f}" width="{4.8*k:.1f}" height="{9*k:.1f}" rx="{2*k:.1f}" fill="{kleur}"/>'
                f'<circle cx="{bx:.1f}" cy="{by-13.8*k:.1f}" r="{2.5*k:.1f}" fill="{huid}"/>'
                f'<path d="M{bx-2.5*k:.1f},{by-14*k:.1f} a{2.5*k:.1f},{2.5*k:.1f} 0 0 1 {5*k:.1f},0 z" fill="{haar}"/>')
        arm = ""
        if pas:
            sx, sy = bx + 1.8 * k, by - 10.2 * k                                                                    # schouder
            dx, dy = pas[0] - sx, pas[1] - sy; L = math.hypot(dx, dy); hoek = math.degrees(math.atan2(dy, dx))
            rust = 90 - hoek                                                                                         # arm langs het lijf
            hx, hy = sx + dx, sy + dy
            arm = (f'<g class="anim-arm" style="transform-origin:{sx:.1f}px {sy:.1f}px;--rust:{rust:.1f}deg">'
                   f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{kleur}" stroke-width="{1.7*k:.1f}" stroke-linecap="round"/>'
                   f'<rect x="{hx-2.6:.1f}" y="{hy-2:.1f}" width="5.2" height="3.4" rx=".6" fill="#FFFFFF" stroke="{DONKER}" stroke-width=".6"/>'
                   f'<rect x="{hx-2.6:.1f}" y="{hy-2:.1f}" width="5.2" height="1.1" rx=".4" fill="{MIDDEN}"/>'
                   f'<circle cx="{hx:.1f}" cy="{hy+1.2:.1f}" r="{1.1*k:.1f}" fill="{huid}"/></g>')
        self.voeg((x - 0.12, y - 0.12, 0, x + 0.12, y + 0.12, 0.85 * k), lijf + arm, pad=(8, 20, 30, 3))
    def struik(self, x, y, r=0.32):
        cx, cy = self.P(x, y, 0.12); rs = r * self.s
        self.voeg((x - r, y - r, 0.003, x + r, y + r, 0.003), self.grond_g(f'<ellipse cx="{(x+0.1)*self.s:.1f}" cy="{(y+0.05)*self.s:.1f}" rx="{rs*0.9:.1f}" ry="{rs*0.6:.1f}" fill="{SCHADUW}" opacity=".1"/>'), grond=True)
        self.voeg((x - r, y - r, 0, x + r, y + r, 0.5), f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rs:.1f}" fill="{GROEN}"/><circle cx="{cx+rs*0.25:.1f}" cy="{cy+rs*0.15:.1f}" r="{rs*0.6:.1f}" fill="{GROENDONKER}" opacity=".3"/><circle cx="{cx-rs*0.3:.1f}" cy="{cy-rs*0.3:.1f}" r="{rs*0.5:.1f}" fill="{GROEN2}"/>', pad=(2, 2, 2, 2))
    def lantaarn(self, x, y, h=1.6):
        P = self.P; bx, by = P(x, y, 0); tx, ty = P(x, y, h)
        self.voeg((x, y, 0.003, x + 0.3 * h, y + 0.1 * h, 0.003), self.grond_g(f'<line x1="{x*self.s:.1f}" y1="{y*self.s:.1f}" x2="{(x+0.3*h)*self.s:.1f}" y2="{(y+0.1*h)*self.s:.1f}" stroke="{SCHADUW}" stroke-width="1.2" opacity=".12"/>'), grond=True)
        self.voeg((x, y, 0, x, y, h), f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="6" fill="#FFE9A0" opacity=".18"/><line x1="{bx:.0f}" y1="{by:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{PAAL}" stroke-width="1.5"/><circle cx="{tx:.0f}" cy="{ty:.0f}" r="2.2" fill="#FFF3B0" stroke="{PAAL}" stroke-width="0.6"/>', pad=(7, 7, 7, 7))
    def lichtmast(self, x, y, h=4.2):
        """Lichtmast van een sportveld: hoge paal met lampenbak."""
        P = self.P; bx, by = P(x, y, 0); tx, ty = P(x, y, h)
        self.voeg((x, y, 0, x, y, h), f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{PAAL}" stroke-width="1.6"/>'
                  f'<rect x="{tx-5:.0f}" y="{ty-4:.0f}" width="10" height="5" rx="1" fill="{GRIJS_R}"/><circle cx="{tx-2.5:.0f}" cy="{ty-1.5:.0f}" r="1.1" fill="#FFF3B0"/><circle cx="{tx+2.5:.0f}" cy="{ty-1.5:.0f}" r="1.1" fill="#FFF3B0"/>', pad=(6, 6, 6, 2))
    def dakkast(self, x, y, z):
        self.blok(x, y, z, 0.5, 0.4, 0.3, GRIJS_T, GRIJS_L, GRIJS_R)
    def bord(self, x, y, tekst, kleur=MIDDEN, h=1.3):
        """Bordje op een paal met een letter (H voor ziekenhuis, P voor parkeren)."""
        P = self.P; bx, by = P(x, y, 0); tx, ty = P(x, y, h)
        self.voeg((x, y, 0, x, y, h), f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{PAAL}" stroke-width="1.5"/>'
                  f'<rect x="{tx-6:.0f}" y="{ty-13:.0f}" width="12" height="12" rx="1" fill="{kleur}"/><text x="{tx:.0f}" y="{ty-3:.0f}" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle" font-family="Arial,sans-serif">{tekst}</text>', pad=(7, 14, 7, 2))
    def vlag(self, x, y, h=2.8, kleur=None, nl=False):
        """Vlaggenmast op de grond; de vlag wappert zijwaarts (scaleX vanuit de mast). nl=True: rood-wit-blauw."""
        P = self.P; fx, fy = P(x, y, 0); tx, ty = P(x, y, h)
        if nl: doek = "".join(f'<rect x="{tx:.1f}" y="{ty + i * 4:.1f}" width="22" height="4" fill="{k}"/>' for i, k in enumerate((NL_ROOD, "#FFFFFF", NL_BLAUW)))
        else: doek = f'<rect x="{tx:.1f}" y="{ty:.1f}" width="22" height="12" fill="{kleur or LICHT}"/>'
        svg = (f'<line x1="{fx:.1f}" y1="{fy:.1f}" x2="{tx:.1f}" y2="{ty - 1:.1f}" stroke="{DONKER}" stroke-width="1.8"/><circle cx="{tx:.1f}" cy="{ty - 1.5:.1f}" r="1.4" fill="{DONKER}"/>'
               f'<g class="anim-vlag" style="transform-origin:{tx:.1f}px {ty:.1f}px">{doek}</g>')
        self.voeg((x, y, 0, x, y, h), svg, pad=(2, 3, 24, 2))
    def slagboom(self, x, y, lengte=1.6):
        """Slagboom: kastje met een rood-witte arm die omhoog draait (richting +x)."""
        P = self.P; self.blok(x, y, 0, 0.3, 0.3, 0.7, GRIJS_T, GRIJS_L, GRIJS_R)
        a = P(x + 0.3, y + 0.15, 0.62); b = P(x + 0.3 + lengte, y + 0.15, 0.62)
        arm = f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{KRUIS_L}" stroke-width="2.4"/><line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#FFFFFF" stroke-width="2.4" stroke-dasharray="5 5"/>'
        self.voeg((x + 0.3, y, 0.6, x + 0.3 + lengte, y + 0.3, 0.7), f'<g class="anim-slagboom" style="transform-origin:{a[0]:.1f}px {a[1]:.1f}px">{arm}</g>', pad=(2, 30, 2, 2))
    def fiets(self, x, y, kleur=DONKER):
        """Fiets, van opzij gezien, staand langs de x-as."""
        P = self.P; r = 0.15 * self.s; a = P(x, y, 0.15); b = P(x + 0.5, y, 0.15); z = P(x + 0.28, y, 0.5)
        self.voeg((x, y, 0, x + 0.5, y, 0.55), f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="{r:.1f}" fill="none" stroke="{kleur}" stroke-width="1.2"/><circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="{r:.1f}" fill="none" stroke="{kleur}" stroke-width="1.2"/>'
                  f'<polyline points="{a[0]:.1f},{a[1]:.1f} {z[0]:.1f},{z[1]:.1f} {b[0]:.1f},{b[1]:.1f}" fill="none" stroke="{kleur}" stroke-width="1.2"/>', pad=(3, 3, 3, 3))
    def doel(self, x, y, breedte, richting="x"):
        """Voetbaldoel: twee palen en een lat, wit."""
        P = self.P
        p = [(x, y), (x + breedte, y)] if richting == "x" else [(x, y), (x, y + breedte)]
        a0, a1, b0, b1 = P(*p[0], 0), P(*p[0], 0.55), P(*p[1], 0), P(*p[1], 0.55)
        self.voeg((x, y, 0, p[1][0], p[1][1], 0.55), f'<polyline points="{a0[0]:.0f},{a0[1]:.0f} {a1[0]:.0f},{a1[1]:.0f} {b1[0]:.0f},{b1[1]:.0f} {b0[0]:.0f},{b0[1]:.0f}" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>')
    def net(self, x, y, lengte, richting="x"):
        if richting == "x": self.blok(x, y, 0, lengte, 0.03, 0.3, GRIJS_R, GRIJS_R, GRIJS_R)
        else: self.blok(x, y, 0, 0.03, lengte, 0.3, GRIJS_R, GRIJS_R, GRIJS_R)
    def basket(self, x, y):
        P = self.P; b0, b1 = P(x, y, 0), P(x, y, 1.1)
        self.voeg((x, y, 0, x, y, 1.15), f'<line x1="{b0[0]:.0f}" y1="{b0[1]:.0f}" x2="{b1[0]:.0f}" y2="{b1[1]:.0f}" stroke="{PAAL}" stroke-width="1.4"/><rect x="{b1[0]-5:.0f}" y="{b1[1]-6:.0f}" width="10" height="7" fill="#FFFFFF" stroke="{PAAL}" stroke-width="0.6"/><circle cx="{b1[0]:.0f}" cy="{b1[1]+1:.0f}" r="1.8" fill="none" stroke="{KRUIS_L}" stroke-width="1"/>', pad=(6, 8, 6, 2))
    def schommel(self, x, y):
        self.blok(x, y, 0, 0.12, 0.12, 1.0, LICHT, LICHT, MIDDEN); self.blok(x + 1.2, y, 0, 0.12, 0.12, 1.0, LICHT, LICHT, MIDDEN)
        self.blok(x, y, 1.0, 1.32, 0.12, 0.08, GROEN2, GROEN, GROENDONKER)
        self.blok(x + 0.5, y, 0.35, 0.3, 0.12, 0.05, DONKER, DONKER, DONKER)
    def glijbaan(self, x, y):
        self.blok(x, y, 0, 0.35, 0.35, 0.9, LICHT2, LICHT, MIDDEN)
        P = self.P; self.voeg((x + 0.35, y, 0, x + 1.3, y + 0.35, 0.9), _poly([P(x + 0.35, y, 0.9), P(x + 0.35, y + 0.35, 0.9), P(x + 1.3, y + 0.35, 0.05), P(x + 1.3, y, 0.05)], LICHT))

    # ---------- voertuigen ----------
    def _wielen(self, x, y, lang, d=0.7, richting="x"):
        """Twee wielen op het zichtbare zijvlak en een koplamp op het voorvlak. Rijrichting +x (naar rechtsonder) of +y (naar linksonder)."""
        P = self.P; r = 0.14 * self.s; uit = []
        if richting == "x":
            for wx in (x + 0.32, x + lang - 0.32):
                cx, cy = P(wx, y + d, 0.14)
                uit.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.1f}" ry="{r*0.85:.1f}" fill="{WIEL}"/><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*0.45:.1f}" ry="{r*0.4:.1f}" fill="#9AA3AB"/>')
            lx, ly = P(x + lang, y + d * 0.3, 0.22)
        else:
            for wy in (y + 0.32, y + lang - 0.32):
                cx, cy = P(x + d, wy, 0.14)
                uit.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.1f}" ry="{r*0.85:.1f}" fill="{WIEL}"/><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*0.45:.1f}" ry="{r*0.4:.1f}" fill="#9AA3AB"/>')
            lx, ly = P(x + d * 0.7, y + lang, 0.22)
        if richting == "-y":   # rijdt van de kijker af: het zichtbare y-vlak is de achterkant, dus twee achterlichten
            for ax in (x + d * 0.2, x + d * 0.7):
                lx, ly = P(ax, y + lang, 0.2); uit.append(f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="1.3" fill="{KRUIS_L}"/>')
        else:
            uit.append(f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="1.6" fill="#FFF3B0"/>')
        doos = (x, y, 0, x + lang, y + d, 0.3) if richting == "x" else (x, y, 0, x + d, y + lang, 0.3)
        self.voeg(doos, "".join(uit))
    def auto(self, x, y, kleur=MIDDEN, klas=None, lang=1.4, richting="x"):
        """Personenauto (lang 1.4), bestelbus (1.8) of vrachtwagen (>= 2.2: laadbak met de cabine vóór).
        richting 'x': rijdt naar rechtsonder (klasse anim-auto); 'y': rijdt naar linksonder (klasse anim-auto-y);
        '-y': rijdt naar rechtsboven, van de kijker af (klasse anim-auto-y-terug), met achterlichten."""
        def teken():
            if richting == "x":
                if lang >= 2.2:
                    self.blok(x, y, 0.15, lang - 0.9, 0.7, 0.95, WIT_T, WIT_L, WIT_R)                  # laadbak (achter)
                    self.blok(x + lang - 0.8, y + 0.02, 0, 0.8, 0.66, 0.8, kleur, kleur, kleur)         # cabine (vóór)
                    self.blok(x + lang - 0.62, y + 0.02, 0.45, 0.5, 0.66, 0.32, GLAS, GLAS, kleur)      # cabineraam
                else:
                    self.blok(x, y, 0, lang, 0.7, 0.3, kleur, kleur, kleur)
                    self.blok(x + 0.3, y + 0.05, 0.3, min(0.85, lang * 0.55), 0.6, 0.28, kleur, GLAS, GLAS)
            else:
                if lang >= 2.2:
                    self.blok(x, y, 0.15, 0.7, lang - 0.9, 0.95, WIT_T, WIT_L, WIT_R)
                    self.blok(x + 0.02, y + lang - 0.8, 0, 0.66, 0.8, 0.8, kleur, kleur, kleur)
                    self.blok(x + 0.02, y + lang - 0.62, 0.45, 0.66, 0.5, 0.32, GLAS, kleur, GLAS)
                else:
                    self.blok(x, y, 0, 0.7, lang, 0.3, kleur, kleur, kleur)
                    self.blok(x + 0.05, y + 0.3, 0.3, 0.6, min(0.85, lang * 0.55), 0.28, kleur, GLAS, GLAS)
            self._wielen(x, y, lang, 0.7, richting)
        self.groep(klas, teken)
    def ambulance(self, x, y):
        """Nederlandse ambulance: geel met blauwe streep, rood kruis op de zijkant, zwaailicht; cabine vóór, rijdt naar rechtsonder."""
        def teken():
            self.blok(x, y, 0, 1.75, 0.8, 0.45, GEEL_T, GEEL_L, GEEL_R)                                 # onderbak
            self.blok(x, y, 0.45, 1.05, 0.8, 0.5, GEEL_T, GEEL_L, GEEL_R)                               # opbouw (achter)
            self.blok(x + 1.1, y + 0.05, 0.45, 0.62, 0.7, 0.32, GEEL_T, GLAS, GLAS)                      # cabine met ruiten (vóór)
            self.blok(x, y + 0.79, 0.28, 1.75, 0.01, 0.1, MIDDEN, MIDDEN, MIDDEN)                       # blauwe streep over de zijkant
            self.kruis_gevel(x + 0.52, y + 0.8, 0.72, 0.36, 0.36, KRUIS_L)                              # rood kruis op de zijkant
            lx, ly = self.P(x + 0.5, y + 0.4, 0.95)
            self.voeg((x + 0.4, y + 0.3, 0.95, x + 0.6, y + 0.5, 1.05), f'<rect class="anim-zwaailicht" x="{lx-3:.1f}" y="{ly-3:.1f}" width="6" height="3" rx="1" fill="{LICHT}"/>')
            self._wielen(x, y, 1.75, 0.8, "x")
        self.groep("anim-auto", teken)
    def heftruck(self, x, y):
        def teken():
            self.blok(x, y, 0, 0.6, 0.8, 0.35, GEEL_T, GEEL_L, GEEL_R)
            self.blok(x + 0.05, y + 0.1, 0.35, 0.5, 0.4, 0.45, GEEL_T, GLAS, GLAS)
            self.blok(x + 0.15, y + 0.8, 0, 0.3, 0.05, 0.9, GRIJS_R, GRIJS_R, GRIJS_R)                    # mast
            self.blok(x + 0.1, y + 0.85, 0.12, 0.4, 0.35, 0.05, GRIJS_L, GRIJS_L, GRIJS_R)                # vork
            self._wielen(x, y, 0.8, 0.6, "y")
        self.groep("anim-heftruck", teken)
    def fietser(self, x, y):
        """Fietser op het fietspad, rijdt in de x-richting."""
        def teken():
            self.fiets(x, y, DONKER)
            self.blok(x + 0.2, y - 0.08, 0.5, 0.16, 0.16, 0.42, MIDDEN, MIDDEN, MIDDEN)
            cx, cy = self.P(x + 0.28, y, 1.0); self.voeg((x + 0.2, y - 0.1, 0.95, x + 0.36, y + 0.1, 1.1), f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.2" fill="#F1C9A6"/>')
        self.groep("anim-fiets", teken)

    # ---------- groepen en sortering ----------
    def groep(self, klas, fn, style=None, rek=None):
        """Voert fn uit en bundelt wat het toevoegt in één <g> (voor CSS-animatie). De doos van de groep is de omhullende doos
        van de delen, bij bewegende klassen uitgerekt over het hele rijpad (REK), zodat de tekenvolgorde op elk moment klopt."""
        n = len(self.delen); fn()
        nieuw = self.delen[n:]; del self.delen[n:]
        if not nieuw: return
        doos = [min(d[0][0] for d in nieuw), min(d[0][1] for d in nieuw), min(d[0][2] for d in nieuw),
                max(d[0][3] for d in nieuw), max(d[0][4] for d in nieuw), max(d[0][5] for d in nieuw)]
        r = rek or REK.get(klas)
        if r: doos = [doos[0] - r[0], doos[1] - r[1], doos[2], doos[3] + r[2], doos[4] + r[3], doos[5]]
        pad = tuple(max(d[3][i] for d in nieuw) for i in range(4))
        # de delen binnen de groep in de juiste volgorde
        binnen = "".join(d[1] for d in self._volgorde(nieuw))
        kl = f' class="{klas}"' if klas else ""; st = f' style="{style}"' if style else ""
        self.voeg(tuple(doos), f'<g{kl}{st}>{binnen}</g>', grond=all(d[2] for d in nieuw), pad=pad)
    def _schermdoos(self, deel):
        (x0, y0, z0, x1, y1, z1), _, _, (pl, pt, pr, pb) = deel; s = self.s
        return ((x0 - y1) * CX * s + self.ox - pl, (x0 + y0) * CY * s - z1 * s + self.oy - pt,
                (x1 - y0) * CX * s + self.ox + pr, (x1 + y1) * CY * s - z0 * s + self.oy + pb)
    @staticmethod
    def _achter(a, b):
        """A staat achter B als A helemaal links van, achter of onder B ligt (scheidingsregel)."""
        return a[3] <= b[0] + EPS or a[4] <= b[1] + EPS or a[5] <= b[2] + EPS
    def _volgorde(self, delen):
        grond = sorted([d for d in delen if d[2]], key=lambda d: d[0][2])
        ruim = [d for d in delen if not d[2]]
        n = len(ruim); sd = [self._schermdoos(d) for d in ruim]
        eerst = [[] for _ in range(n)]   # eerst[i]: delen die vóór i getekend moeten worden
        for i in range(n):
            for j in range(i + 1, n):
                a, b = sd[i], sd[j]
                if a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1]: continue   # geen overlap op het scherm
                da, db = ruim[i][0], ruim[j][0]
                ab, ba = self._achter(da, db), self._achter(db, da)
                if ab and not ba: eerst[j].append(i)
                elif ba and not ab: eerst[i].append(j)
                elif ab and ba:
                    if da[0] + da[1] + da[2] <= db[0] + db[1] + db[2]: eerst[j].append(i)
                    else: eerst[i].append(j)
        volg, staat = [], [0] * n
        def bezoek(i):
            if staat[i]: return
            staat[i] = 1
            for k in eerst[i]: bezoek(k)
            staat[i] = 2; volg.append(i)
        for i in range(n): bezoek(i)
        return grond + [ruim[i] for i in volg]
    def svg(self, breedte, hoogte, label):
        iso = f'patternTransform="matrix({CX:.4f},{CY:.4f},{-CX:.4f},{CY:.4f},{self.ox},{self.oy})"'
        t = 0.5 * self.s                                                                                            # tegel van een halve eenheid
        defs = (f'<defs><pattern id="p-gras" width="{t:.1f}" height="{t:.1f}" patternUnits="userSpaceOnUse" {iso}><rect width="{t:.1f}" height="{t:.1f}" fill="{GROEN2}"/>'
                f'<path d="M2,7 l1,-3 l1,3 M6,4 l1,-3 l1,3" fill="none" stroke="#62CC92" stroke-width=".7"/></pattern>'
                f'<pattern id="p-tegels" width="{t:.1f}" height="{t:.1f}" patternUnits="userSpaceOnUse" {iso}><rect width="{t:.1f}" height="{t:.1f}" fill="{GROND2}"/>'
                f'<path d="M0,{t:.1f} H{t:.1f} V0" fill="none" stroke="#D3D9DF" stroke-width=".7"/></pattern>'
                f'<pattern id="p-asfalt" width="7" height="7" patternUnits="userSpaceOnUse"><rect width="7" height="7" fill="{WEG}"/>'
                f'<circle cx="2" cy="2" r=".55" fill="#CBD2D9"/><circle cx="5.5" cy="5" r=".55" fill="#CBD2D9"/></pattern>'
                f'<pattern id="p-grind" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r=".5" fill="#000" opacity=".07"/><circle cx="4.5" cy="4" r=".5" fill="#FFF" opacity=".25"/></pattern>'
                + "".join(f'<pattern id="p-{naam}-{kant}" width="{bw}" height="{bh}" patternUnits="userSpaceOnUse" patternTransform="skewY({hoek})">{inhoud}</pattern>'
                          for kant, hoek in (("l", 30), ("r", -30))
                          for naam, bw, bh, inhoud in (
                              ("steen", 7, 3.2, f'<path d="M0,0 H7 M0,1.6 H7 M0,0 V1.6 M3.5,1.6 V3.2" fill="none" stroke="#6E2F22" stroke-width=".35" opacity=".35"/>'),       # metselwerk halfsteens
                              ("natuursteen", 14, 6, f'<path d="M0,0 H14 M0,3 H14 M0,0 V3 M7,3 V6" fill="none" stroke="#8C7B5E" stroke-width=".4" opacity=".4"/>'),    # grote blokken
                              ("plaat", 9, 20, f'<path d="M0,0 V20 M0,10 H9" fill="none" stroke="#7D8C9B" stroke-width=".35" opacity=".35"/>')))                    # gevelplaten
                + '</defs>')
        return (f'<svg viewBox="0 0 {breedte} {hoogte}" width="{breedte}" height="{hoogte}" role="img" aria-label="{label}" '
                f'xmlns="http://www.w3.org/2000/svg" class="iso">' + defs + "".join(d[1] for d in self._volgorde(self.delen)) + "</svg>")

# ---------- gedeelde bouwstenen ----------
G = 12.2   # grondvlak 12.2 x 12.2

def _nieuw():
    return Scene(19, 222, 116)

def _weg_x(sc, y, b=1.0, x0=0, x1=G, streep=True):
    sc.vlak(x0, y, x1 - x0, b, WEG)
    for k in (y + 0.02, y + b - 0.02): sc.lijn_grond(x0, k, x1, k, STOEPRAND, 0.6, z=0.012)                    # stoepranden
    for f in (0.28, 0.74): sc.ellips(x0 + (x1 - x0) * f, y + b * 0.7, 0.13, 0.13, "#C4CBD2", "#B3BBC3", 0.6, z=0.013)   # putdeksels
    if streep: sc.lijn_grond(x0 + 0.3, y + b / 2, x1 - 0.3, y + b / 2, "#FFFFFF", 0.8)

def _weg_y(sc, x, b=1.0, y0=0, y1=G, streep=True):
    sc.vlak(x, y0, b, y1 - y0, WEG)
    for k in (x + 0.02, x + b - 0.02): sc.lijn_grond(k, y0, k, y1, STOEPRAND, 0.6, z=0.012)
    for f in (0.3, 0.72): sc.ellips(x + b * 0.3, y0 + (y1 - y0) * f, 0.13, 0.13, "#C4CBD2", "#B3BBC3", 0.6, z=0.013)
    if streep: sc.lijn_grond(x + b / 2, y0 + 0.3, x + b / 2, y1 - 0.3, "#FFFFFF", 0.8)

def _stad(sc):
    """Stadsraster: twee wegen in elke richting met zebra's en lantaarns (kantoren)."""
    sc.vlak(0, 0, G, G, GROND)
    for k in (3.4, 7.8): _weg_x(sc, k); _weg_y(sc, k)
    for k in (3.4, 7.8):
        for m in (1.4, 5.8, 10.2): sc.zebra(m, k, 1.2, 1.0, 4); sc.zebra(k, m, 1.0, 1.2, 4)
    for k in (3.3, 7.7):
        for m in (0.6, 5.0, 9.4, 11.8): sc.lantaarn(m, k); sc.lantaarn(k, m)

def _aansluiting(sc, y_weg):
    """Verbindt de doorgaande weg (breedte 1.0, kleur WEG, op y_weg) met de linker- en rechterrand van het beeld op de hoogte van de
    zijpunten van het eilandje, zodat de weg in de sectorrij van kaart naar kaart doorloopt (Lars, 23-09-2026).
    Het verbindingsstuk loopt eerst recht in de richting van de weg het eiland in en uit (zelfde breedte en kleur, dus geen naad)
    en bocht daarna naar de rand. Grondlaag: onder alle gebouwen."""
    rand_y = sc.oy + G * CY * sc.s; yc = y_weg + 0.5
    breedte = 2 * CX * sc.s * CY                             # (x-richting: afstand tussen de randen y en y+1)
    bi, bu = sc.P(1.0, yc, 0), sc.P(-1.1, yc, 0)              # inrit: binnen en buiten het eiland
    ui, uu = sc.P(G - 1.0, yc, 0), sc.P(G + 0.8, yc, 0)       # uitrit
    inrit = f"M0,{rand_y:.1f} C{bu[0]*0.4:.1f},{rand_y:.1f} {bu[0]-34:.1f},{bu[1]-19.6:.1f} {bu[0]:.1f},{bu[1]:.1f} L{bi[0]:.1f},{bi[1]:.1f}"
    uitrit = f"M{ui[0]:.1f},{ui[1]:.1f} L{uu[0]:.1f},{uu[1]:.1f} C{uu[0]+30:.1f},{uu[1]+17:.1f} {444-(444-uu[0])*0.5:.1f},{rand_y:.1f} 444,{rand_y:.1f}"
    for d in (inrit, uitrit):
        sc.voeg((-9, -9, 0.004, -8, -8, 0.004), f'<path d="{d}" fill="none" stroke="{WEG}" stroke-width="{breedte:.1f}"/>'
                f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="0.8"/>', grond=True)

def _bomen(sc, punten, r=0.5, h=1.3):
    for x, y in punten: sc.boom(x, y, r, h)

# ---------- de acht sectoren ----------
def kantoor():
    """Kantoren: zakendistrict met kantoortorens van glas, zendmast met knipperlicht, plein met fontein; ramen lichten om de beurt op, één auto rijdt."""
    sc = _nieuw(); _stad(sc); _aansluiting(sc, 7.8)
    sc.blok(0.3, 0.3, 0, 2.8, 2.8, 5.8, LICHT2, MIDDEN, DONKER, ramen=(6, 3), lichtjes=True)                 # hoogste toren
    sc.blok(1.5, 1.5, 5.8, 0.14, 0.14, 0.7, GRIJS_T, GRIJS_L, GRIJS_R)                                        # zendmast
    mx, my = sc.P(1.57, 1.57, 6.55); sc.voeg((1.5, 1.5, 6.5, 1.64, 1.64, 6.6), f'<circle class="anim-knipper" cx="{mx:.1f}" cy="{my:.1f}" r="2" fill="{KRUIS_L}"/>', pad=(3, 3, 3, 3))
    sc.dakkast(0.6, 2.2, 5.8); sc.dakkast(2.3, 0.6, 5.8)
    sc.blok(4.7, 0.4, 0, 2.8, 2.6, 4.0, WIT_T, WIT_L, WIT_R, ramen=(4, 3), deur=(0.5, 0.7, 1.2), lichtjes=True, deur_anim=True)   # hoofdkantoor met entree
    sc.dakkast(5.0, 0.7, 4.0); sc.dakkast(6.6, 2.2, 4.0)
    sc.blok(9.1, 0.3, 0, 2.8, 2.8, 5.0, LICHT2, MIDDEN2, DONKER2, ramen=(5, 3), lichtjes=True)                 # tweede toren
    sc.blok(9.1, 0.3, 5.0, 1.4, 1.4, 0.5, LICHT2, MIDDEN2, DONKER2)                                            # dakopbouw
    sc.vlak(0.4, 4.6, 3.0, 3.0, GROND2)                                                                        # plein
    sc.ellips(1.9, 6.1, 0.8, 0.8, LICHT); sc.groep("anim-water", lambda: sc.ellips(1.9, 6.1, 0.55, 0.55, GLAS2, z=0.02))   # fontein
    for bx, by in [(0.7, 5.0), (2.8, 4.9), (0.7, 7.0)]: sc.blok(bx, by, 0, 0.6, 0.18, 0.22, DAK_T, DAK_L, DAK_R)   # bankjes
    _bomen(sc, [(3.0, 6.9), (0.8, 6.1)], 0.42, 1.1)
    sc.blok(4.7, 4.7, 0, 2.8, 2.6, 3.4, MIDDEN2, MIDDEN, DONKER, ramen=(3, 3), deur=(1.0, 0.6, 1.1), lichtjes=True)  # kantoor
    sc.blok(9.0, 4.6, 0, 3.0, 3.0, 1.6, GRIJS_T, GRIJS_L, GRIJS_R, ramen=(1, 3)); sc.bord(8.8, 4.5, "P")        # parkeergarage
    sc.vlak(0.4, 9.0, 11.4, 3.0, GROEN2)                                                                         # park vooraan; in- en uitrit blijven vrij
    sc.blok(4.4, 9.0, 0, 3.4, 2.8, 4.4, LICHT2, MIDDEN2, DONKER2, ramen=(4, 3), lichtjes=True)                  # toren vooraan (midden)
    _bomen(sc, [(1.6, 9.8), (2.8, 11.2), (1.2, 11.8), (9.4, 9.8), (11.0, 10.6), (9.8, 11.8)])
    sc.auto(8.0, 7.95, DONKER, klas="anim-auto")
    sc.persoon(2.5, 5.2); sc.persoon(1.2, 6.9, DONKER); sc.persoon(6.0, 10.6, GROENDONKER); sc.struik(3.1, 4.9); sc.struik(3.1, 5.6); sc.struik(0.7, 5.5)
    return sc.svg(444, 350, "Isometrische tekening van een zakendistrict met kantoortorens van glas, een plein met fontein en een parkeergarage")

def zorg():
    """Zorg: ziekenhuis met rood kruis op de gevel en helikopterplatform, spoedeisende hulp, apotheek met groen kruis, jeugdinstelling met speelplein, huisartsenpost; de ambulance rijdt (cabine vooruit)."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    _weg_x(sc, 6.6); _weg_y(sc, 6.0, y0=0, y1=6.6); sc.zebra(6.0, 4.0, 1.0, 1.0, 4); sc.zebra(2.2, 6.6, 1.2, 1.0, 4); _aansluiting(sc, 6.6)
    for m in (0.5, 4.0, 8.5, 11.8): sc.lantaarn(m, 6.5)
    sc.blok(0.4, 0.4, 0, 4.6, 3.4, 4.0, WIT_T, WIT_L, WIT_R, ramen=(4, 5))                                     # ziekenhuis, hoofdgebouw
    sc.kruis_gevel(2.7, 3.8, 3.05, 1.6, 1.6, KRUIS_L, "links", klas="anim-gloed")                               # rood kruis, plat op de voorgevel
    sc.dak_cirkel(2.7, 2.1, 4.0, 0.9, GRIJS_L, "#FFFFFF", "H")                                                 # helikopterplatform
    sc.blok(0.4, 3.8, 0, 4.6, 1.9, 2.0, WIT_T, WIT_L, WIT_R, ramen=(1, 5), deur=(0.4, 1.3, 1.5), deur_anim=True)   # spoedeisende hulp met brede ingang
    sc.kruis_gevel(3.6, 5.7, 1.5, 0.5, 0.5, KRUIS_L)
    sc.bord(5.4, 5.9, "H", KRUIS_L)
    sc.blok(7.4, 0.4, 0, 2.6, 2.4, 1.8, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(0.4, 0.6, 1.1))               # apotheek
    sc.kruis_gevel(8.9, 2.8, 1.25, 0.6, 0.6, GROEN, "links", klas="anim-gloed")                                 # groen kruis
    sc.blok(10.4, 0.4, 0, 1.6, 2.4, 2.6, LICHT2, MIDDEN2, DONKER2, ramen=(2, 2))                                # polikliniek
    sc.blok(9.6, 3.6, 0, 2.4, 2.4, 1.6, LICHT2, MIDDEN2, DONKER2, ramen=(1, 3), deur=(0.9, 0.6, 1.0))           # jeugdinstelling
    sc.vlak(7.2, 3.4, 2.2, 2.8, GROEN2); sc.schommel(7.6, 4.6); sc.ellips(8.6, 3.9, 0.35, 0.35, ZAND_T)          # speelplein met schommel en zandbak
    sc.ambulance(0.2, 6.75)                                                                                    # de enige auto
    sc.vlak(0.4, 8.0, 11.4, 3.8, GROEN2)                                                                         # park vooraan; in- en uitrit blijven vrij
    sc.blok(3.4, 8.0, 0, 3.2, 2.4, 1.8, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(1.3, 0.6, 1.1))               # huisartsenpost
    sc.blok(6.9, 8.0, 0, 3.1, 2.6, 2.2, MIDDEN2, MIDDEN, DONKER, ramen=(2, 3), deur=(1.3, 0.6, 1.1))            # verpleeghuis
    _bomen(sc, [(1.8, 8.8), (2.6, 10.6), (1.4, 11.7), (11.0, 8.9), (11.5, 10.6), (10.6, 11.7), (11.6, 3.0)])
    sc.persoon(1.4, 9.6); sc.persoon(2.2, 9.0, DONKER); sc.persoon(5.3, 6.2, KRUIS_L); sc.struik(5.4, 4.2); sc.struik(5.4, 4.9); sc.struik(10.6, 8.6)
    return sc.svg(444, 350, "Isometrische tekening van een ziekenhuis met rood kruis en helikopterplatform, apotheek, jeugdinstelling en ambulance")

def onderwijs():
    """Onderwijs: bakstenen basisschool met klok, schoolplein met hinkelbaan, klimrek, glijbaan en zandbak, fietsenrekken vol fietsen, gymzaal, kinderopvang; bal stuitert, schoolvlag wappert, een fietser rijdt over het fietspad."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    _weg_x(sc, 8.2); _aansluiting(sc, 8.2)                                                                    # straat langs de school
    sc.vlak(0, 9.35, G, 0.6, FIETSPAD)                                                                           # rood fietspad naast de straat
    sc.blok(0.4, 0.4, 0, 5.0, 2.6, 2.2, ROOD_T, ROOD_L, ROOD_R, ramen=(1, 5), deur=(2.2, 0.8, 1.3), deur_anim=True)   # school, begane grond
    sc.blok(0.4, 0.4, 2.2, 2.4, 2.6, 1.6, ROOD_T, ROOD_L, ROOD_R, ramen=(1, 2))                                  # verdieping
    sc.klok(4.4, 3.0, 1.75)                                                                                    # klok op de gevel
    sc.vlak(0.4, 3.2, 5.0, 4.4, GROND2); sc.hek(0.4, 3.2, 5.0, 4.4)                                             # schoolplein met hek
    for i in range(4): sc.rechthoek_grond(0.9, 3.7 + i * 0.55, 0.55, 0.55)                                     # hinkelbaan
    sc.rechthoek_grond(0.9, 5.9, 0.55, 0.55); sc.rechthoek_grond(1.45, 5.9, 0.55, 0.55)
    sc.schommel(2.4, 3.8); sc.glijbaan(3.8, 3.8); sc.ellips(2.6, 6.2, 0.6, 0.45, ZAND_T)                      # schommel, glijbaan, zandbak
    for i in range(4): sc.blok(2.0 + i * 0.6, 5.3, 0, 0.5, 0.06, 0.6, LICHT, LICHT, MIDDEN)                     # klimrek
    sc.blok(2.0, 5.3, 0.6, 2.3, 0.06, 0.05, LICHT, LICHT, MIDDEN)
    bx, by = sc.P(4.2, 6.2, 0.15)
    sc.groep("anim-bal", lambda: sc.voeg((4.1, 6.1, 0, 4.3, 6.3, 0.3), f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3" fill="{LICHT}" stroke="{DONKER}" stroke-width="0.6"/>', pad=(3, 3, 3, 3)))
    sc.vlag(5.0, 7.2, 2.6, LICHT)                                                                              # schoolvlag op de hoek van het plein
    for i in range(6): sc.fiets(0.6 + i * 0.6, 7.75, DONKER if i % 2 else MIDDEN)                              # fietsenrek vol
    sc.blok(6.6, 0.4, 0, 5.2, 3.0, 2.6, ROOD_T, ROOD_L, ROOD_R, ramen=(1, 4))                                   # gymzaal
    sc.blok(6.6, 4.2, 0, 5.2, 2.6, 1.6, WIT_T, WIT_L, WIT_R, ramen=(1, 4), deur=(2.2, 0.6, 1.0))               # kinderopvang
    sc.vlak(6.6, 6.9, 5.2, 0.9, GROEN2); _bomen(sc, [(7.2, 7.3), (9.4, 7.3), (11.4, 7.3)], 0.4, 1.0)
    sc.fietser(4.0, 9.55)
    sc.vlak(0, 10.0, G, 2.2, GROEN2)
    _bomen(sc, [(3.0, 10.2), (5.4, 9.9), (7.6, 11.0), (9.6, 9.9), (11.4, 11.2), (4.2, 11.6)])
    sc.persoon(1.6, 6.8); sc.persoon(3.4, 6.6, KRUIS_L); sc.persoon(6.0, 10.6, DONKER); sc.struik(6.0, 3.2); sc.struik(6.0, 3.8)
    return sc.svg(444, 350, "Isometrische tekening van een basisschool met schoolplein, hinkelbaan, speeltoestellen, fietsenrek, gymzaal en fietspad")

def vve():
    """VvE en vastgoed: woonstraat met appartementencomplex met balkons, rijtjeshuizen met puntdaken en voortuinen, garageboxen en twee-onder-een-kapwoningen; een schoorsteen rookt, één auto rijdt."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    sc.vlak(0, 4.4, G, 1.0, GROND2); sc.vlak(0, 6.4, G, 0.8, GROND2)                                           # stoepen
    _weg_x(sc, 5.4); sc.zebra(5.6, 5.4, 1.2, 1.0, 4); _aansluiting(sc, 5.4)
    for m in (1.0, 5.0, 9.0): sc.lantaarn(m, 4.5); sc.lantaarn(m + 2.0, 6.6)
    sc.blok(0.4, 0.4, 0, 4.4, 3.0, 4.2, MIDDEN2, MIDDEN, DONKER, ramen=(4, 3), deur=(1.8, 0.7, 1.2), deur_anim=True)   # appartementencomplex
    sc.balkons(0.4, 3.4, 1.3, 3, 3, 1.0, 1.05)
    sc.vlak(0.4, 3.5, 4.4, 0.9, GROEN2); _bomen(sc, [(1.0, 3.9), (4.2, 3.9)], 0.35, 0.9)
    for i in range(5):                                                                                          # rijtjeshuizen met voortuin en heg
        hx = 5.6 + i * 1.25; kl = (ROOD_T, ROOD_L, ROOD_R) if i % 2 == 0 else (WIT_T, WIT_L, WIT_R)
        sc.huis(hx, 0.8, 1.15, 2.2, 1.7, kl, 0.6, "y", deur=(0.15, 0.4, 0.9), ramen=(2, 1), schoorsteen=(i == 1))
        sc.vlak(hx, 3.0, 1.15, 1.4, GROEN2); sc.blok(hx, 4.2, 0, 1.15, 0.12, 0.35, GROEN2, GROEN, GROENDONKER)
    rx, ry = sc.P(6.85 + 1.25 * 0.7 + 0.09, 0.8 + 0.77 + 0.09, 2.75)
    sc.voeg((7.6, 1.5, 2.8, 8.0, 1.9, 3.6), f'<g class="anim-rook"><circle cx="{rx:.1f}" cy="{ry-4:.1f}" r="3.5" fill="#D5DBE1" opacity=".8"/><circle cx="{rx+3:.1f}" cy="{ry-10:.1f}" r="2.8" fill="#D5DBE1" opacity=".6"/></g>', pad=(4, 14, 8, 2))
    sc.vlak(0.4, 7.2, 3.8, 3.2, GROEN2); sc.schommel(2.4, 8.6); sc.ellips(3.4, 7.9, 0.4, 0.4, ZAND_T)                  # speelveldje links vooraan (inrit blijft vrij)
    for i in range(4): sc.blok(8.6 + i * 0.85, 7.8, 0, 0.8, 1.6, 0.9, GRIJS_T, GRIJS_L, GRIJS_R, deur=(0.1, 0.6, 0.7))   # garageboxen rechts (laag, uitrit blijft vrij)
    for i in range(2):                                                                                          # twee-onder-een-kap in het midden
        hx = 4.6 + i * 1.7
        sc.vlak(hx, 7.2, 1.6, 0.8, GROEN2); sc.blok(hx, 7.25, 0, 1.6, 0.1, 0.3, GROEN2, GROEN, GROENDONKER)
        sc.huis(hx, 8.0, 1.6, 2.2, 1.9, (ROOD_T, ROOD_L, ROOD_R) if i else (ZAND_T, ZAND_L, ZAND_R), 0.7, "y", deur=(0.3, 0.45, 0.95), ramen=(2, 2))
    sc.vlak(0.4, 10.4, 11.4, 1.6, GROEN2)
    _bomen(sc, [(3.2, 11.2), (7.4, 11.3), (10.4, 11.0), (11.8, 6.9)], 0.45, 1.2)
    sc.auto(2.6, 5.55, LICHT, klas="anim-auto")
    sc.persoon(3.0, 4.8); sc.persoon(9.0, 6.7, DONKER); sc.struik(0.8, 4.7); sc.struik(5.2, 6.7)
    return sc.svg(444, 350, "Isometrische tekening van een woonstraat met appartementencomplex met balkons, rijtjeshuizen met puntdaken, garageboxen en twee-onder-een-kapwoningen")

def verenigingen():
    """Verenigingen: sportpark met voetbalveld met doelen en lichtmasten, atletiekbaan, tennisbanen met net, basketbalveld, tribune, clubhuis met terras en clubvlag, sporthal; loper rondt de baan, bal rolt, vlag wappert."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROEN2)
    _weg_x(sc, 8.0); sc.vlak(6.6, 0, 0.6, 8.0, GROND2); _aansluiting(sc, 8.0)                                # toegangsweg en pad
    sc.vlak(0.4, 0.4, 5.6, 3.6, GROEN); sc.rechthoek_grond(0.5, 0.5, 5.4, 3.4); sc.lijn_grond(3.2, 0.5, 3.2, 3.9)   # voetbalveld
    sc.ellips(3.2, 2.2, 0.5, 0.5, "none", STREEP); sc.rechthoek_grond(0.5, 1.4, 0.8, 1.6); sc.rechthoek_grond(5.1, 1.4, 0.8, 1.6)
    sc.doel(0.42, 1.65, 1.1, "y"); sc.doel(5.9, 1.65, 1.1, "y")
    sc.groep("anim-bal", lambda: sc.rondje(1.8, 2.6, 0.11, "#FFFFFF"))
    for lx, ly in [(0.35, 0.35), (6.05, 0.35), (0.35, 4.05), (6.05, 4.05)]: sc.lichtmast(lx, ly)
    sc.blok(0.6, 4.3, 0, 5.2, 0.5, 0.5, GRIJS_T, GRIJS_L, GRIJS_R); sc.blok(0.6, 4.3, 0.5, 5.2, 0.25, 0.4, GRIJS_T, GRIJS_L, GRIJS_R)   # tribune
    sc.ellips(9.6, 2.3, 2.3, 1.7, "#D9865E"); sc.ellips(9.6, 2.3, 1.5, 0.95, GROEN)                              # atletiekbaan
    for r in (1.7, 1.9, 2.1): sc.ellips(9.6, 2.3, r, r * 0.74, "none", "#FFFFFF", 0.6)
    sc.draaiend(9.6, 2.3, f'<circle cx="{(9.6+1.9)*19:.1f}" cy="{2.3*19:.1f}" r="2.6" fill="{DONKER}"/>', "anim-loper")
    for k in (0.4, 2.2):                                                                                        # tennisbanen met net
        sc.vlak(k, 5.2, 1.6, 2.6, "#D9865E"); sc.rechthoek_grond(k + 0.15, 5.35, 1.3, 2.3, "#FFFFFF", 0.7); sc.net(k + 0.1, 6.5, 1.4, "x")
    sc.vlak(4.2, 5.2, 2.2, 2.6, "#C9CED0"); sc.rechthoek_grond(4.3, 5.3, 2.0, 2.4, "#FFFFFF", 0.7)               # basketbalveld
    sc.ellips(5.3, 6.5, 0.4, 0.4, "none", "#FFFFFF", 0.7); sc.basket(5.3, 5.25); sc.basket(5.3, 7.75)
    sc.blok(7.6, 5.0, 0, 3.4, 2.4, 1.6, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(1.2, 0.6, 1.0), deur_anim=True)   # clubhuis
    sc.vlak(7.6, 7.4, 3.4, 0.6, ZAND_T); sc.vlag(11.5, 7.6, 2.4, LICHT)                                        # terras en clubvlag
    for i in range(5): sc.fiets(0.8 + i * 0.6, 9.4, DONKER)                                                    # fietsen langs het pad
    sc.blok(3.6, 9.0, 0, 5.2, 2.8, 2.6, WIT_T, WIT_L, WIT_R, ramen=(1, 4), deur=(2.2, 0.7, 1.1))               # sporthal in het midden (in- en uitrit vrij)
    _bomen(sc, [(2.2, 10.2), (1.4, 11.6), (10.0, 9.6), (11.4, 10.8), (10.2, 11.7), (11.8, 4.6), (6.9, 4.6)], 0.5, 1.3)
    sc.persoon(4.0, 7.6); sc.persoon(9.0, 4.6, DONKER); sc.persoon(8.6, 7.8, KRUIS_L); sc.struik(11.4, 7.6); sc.struik(6.4, 4.6)
    return sc.svg(444, 350, "Isometrische tekening van een sportpark met voetbalveld, lichtmasten, atletiekbaan, tennisbanen, basketbalveld, clubhuis en sporthal")

def recreatie():
    """Recreatiepark in het bos: veel kleine huisjes met puntdak, luxe bungalows aan het water, meer met steiger, zwembad, speeltuin, receptie met slagboom; water beweegt, bomen wuiven, één auto rijdt het park op en de slagboom gaat open."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROEN2)
    sc.vlak(8.6, 0, 0.9, G, GROND2); _weg_x(sc, 5.0); sc.vlak(4.2, 0, 0.6, 5.0, GROND2); _aansluiting(sc, 5.0)   # lanen
    sc.ellips(2.6, 8.9, 2.3, 1.9, LICHT); sc.groep("anim-water", lambda: sc.ellips(2.6, 8.9, 2.0, 1.6, GLAS2, z=0.02))   # meer
    for i in range(5): sc.blok(4.6 + i * 0.3, 8.7, 0, 0.28, 0.5, 0.15, ZAND_T, ZAND_L, ZAND_R)                  # steiger
    sc.ellips(1.4, 9.8, 0.35, 0.18, "#FFFFFF", DAK_L, 0.8, z=0.03)                                              # roeiboot
    def huisje(x, y, w=0.95, d=0.85, h=0.75, kl=(ZAND_T, ZAND_L, ZAND_R)):
        sc.huis(x, y, w, d, h, kl, 0.5, "x", ramen=(1, 1))
    for x, y in [(0.6, 0.6), (2.0, 0.6), (0.6, 2.0), (2.0, 2.0), (0.6, 3.4), (2.0, 3.4), (5.4, 0.6), (6.9, 0.6), (5.4, 2.0), (6.9, 2.0), (5.4, 3.4), (6.9, 3.4)]: huisje(x, y)
    for x, y in [(10.0, 0.6), (10.0, 2.4)]:                                                                      # bungalows aan de laan
        sc.huis(x, y, 1.6, 1.3, 1.0, (WIT_T, WIT_L, WIT_R), 0.45, "x", ramen=(1, 2)); sc.vlak(x, y + 1.3, 1.6, 0.5, ZAND_T)
    for x, y in [(6.2, 6.4), (6.2, 8.6)]:                                                                         # luxe bungalows aan het water, met terras en bubbelbad
        sc.huis(x, y, 2.0, 1.5, 1.1, (WIT_T, WIT_L, WIT_R), 0.4, "y", ramen=(1, 2)); sc.vlak(x - 0.9, y, 0.9, 1.5, ZAND_T); sc.ellips(x - 0.45, y + 0.75, 0.25, 0.25, GLAS2, LICHT, 1.2, z=0.03)
    sc.vlak(9.8, 6.4, 2.0, 2.4, LICHT); sc.groep("anim-water", lambda: sc.vlak(10.0, 6.6, 1.6, 2.0, GLAS2, 0.02))   # zwembad
    sc.schommel(9.9, 9.5); sc.glijbaan(10.6, 10.3)                                                              # speeltuin
    sc.blok(6.0, 10.4, 0, 2.4, 1.4, 1.2, WIT_T, WIT_L, WIT_R, ramen=(1, 2), deur=(0.4, 0.5, 0.85), deur_anim=True)   # receptie bij de ingang
    sc.slagboom(8.4, 10.6, 1.4)
    sc.auto(8.75, 8.6, DONKER, klas="anim-auto-y-terug", lang=1.3, richting="-y")
    _bomen(sc, [(3.6, 0.5), (3.6, 1.9), (3.6, 3.3), (0.5, 4.5), (8.0, 0.5), (8.0, 1.9), (8.0, 3.4), (11.9, 1.5), (11.9, 3.5), (10.6, 4.4), (3.4, 6.5), (0.6, 11.6), (5.2, 11.7), (11.7, 5.9), (4.6, 6.0), (9.4, 9.2), (11.8, 8.9)], 0.5, 1.4)
    sc.persoon(9.2, 6.2); sc.persoon(5.4, 11.2, DONKER); sc.persoon(4.6, 8.2, KRUIS_L); sc.struik(5.0, 8.4); sc.struik(4.8, 11.0); sc.struik(9.6, 5.4)
    return sc.svg(444, 350, "Isometrische tekening van een recreatiepark met vakantiehuisjes, bungalows aan het water, zwembad, speeltuin en receptie met slagboom")

def woningcorporatie():
    """Woningcorporaties: galerijflat met trappenhuis, portiekflat waar een huurder met een pas binnengaat, rij bergingen, wijkkantoor
    en de bus van de onderhoudsdienst; ondergrondse afvalcontainers. Eén auto rijdt."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    _weg_x(sc, 7.8); sc.zebra(5.4, 7.8, 1.2, 1.0, 4); _aansluiting(sc, 7.8)
    for m in (1.0, 4.5, 8.0, 11.5): sc.lantaarn(m, 7.7)
    sc.blok(0.4, 0.4, 0, 5.4, 2.2, 4.2, ROOD_T, ROOD_L, ROOD_R, ramen=(4, 5), dak="zon")                          # galerijflat
    for v in range(1, 4):                                                                                        # galerijen met borstwering
        sc.blok(0.4, 2.6, v * 1.05, 5.4, 0.45, 0.07, GRIJS_T, GRIJS_L, GRIJS_R)
        sc.blok(0.4, 3.02, v * 1.05 + 0.07, 5.4, 0.03, 0.34, WIT_T, WIT_L, WIT_R)
    sc.blok(5.8, 0.8, 0, 1.0, 1.6, 4.8, GRIJS_T, GRIJS_L, GRIJS_R, ramen=(5, 1))                                 # trappenhuis
    sc.blok(7.4, 0.4, 0, 4.4, 2.6, 3.2, WIT_T, WIT_L, WIT_R, ramen=(3, 4), deur=(1.6, 0.8, 1.3), deur_anim=True)   # portiekflat
    sc.vlak(0.4, 3.6, 5.4, 0.6, GROND2); sc.vlak(7.4, 3.2, 4.4, 2.2, GROND2)                                      # stoep en voorplein portiekflat
    sc.blok(0.4, 4.4, 0, 4.6, 2.4, 1.9, MIDDEN2, MIDDEN, DONKER, ramen=(1, 4), deur=(1.8, 0.7, 1.2))                 # wijkkantoor
    for i in range(5): sc.blok(7.5 + i * 0.85, 5.8, 0, 0.8, 1.1, 0.9, ZAND_T, ZAND_L, ZAND_R, deur=(0.15, 0.5, 0.75))  # bergingen (laag, voor de portiek langs)
    sc.auto(5.7, 4.3, MIDDEN, lang=1.8, richting="y")                                                               # bus onderhoudsdienst (geparkeerd)
    sc.vlak(0.4, 9.0, 3.6, 3.0, GROEN2); sc.vlak(8.4, 9.0, 3.6, 3.0, GROEN2)                                        # groen aan beide kanten (in- en uitrit vrij)
    sc.vlak(4.4, 9.0, 3.6, 3.0, GROND2)                                                                             # plein met ondergrondse containers
    for i in range(3): sc.cilinder(5.0 + i * 0.8, 10.0, 0.16, 0.38, GRIJS_T, GRIJS_R)                              # inworpzuilen ondergrondse containers
    sc.schommel(1.2, 10.2)
    _bomen(sc, [(3.2, 9.6), (2.4, 11.4), (9.2, 9.8), (11.0, 10.6), (9.6, 11.6)], 0.5, 1.3)
    sc.persoon(4.8, 9.4, KRUIS_L); sc.persoon(7.0, 11.2, DONKER); sc.struik(6.8, 3.9); sc.struik(7.2, 6.4)
    sc.auto(1.2, 7.95, LICHT, klas="anim-auto")
    return sc.svg(444, 350, "Isometrische tekening van een woonwijk van een woningcorporatie met galerijflat, portiekflat, bergingen, wijkkantoor en een bus van de onderhoudsdienst")

def industrie():
    """Industrie en logistiek: bedrijvenpark met productiehal met sheddak, silo's, schoorsteen, distributiecentrum met laaddocks, containerterrein, hekwerk met slagboom en portier; één vrachtwagen rijdt, heftruck pendelt, schoorsteen rookt."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    _weg_y(sc, 5.6, 1.2); _weg_x(sc, 8.0, 1.0); sc.zebra(5.6, 8.0, 1.2, 1.0, 4); _aansluiting(sc, 8.0)
    for m in (1.0, 4.0, 8.0, 11.0): sc.lantaarn(m, 7.9)
    sc.blok(0.4, 0.4, 0, 4.6, 3.4, 2.2, GRIJS_T, GRIJS_L, GRIJS_R, deur=(0.4, 1.4, 1.6))                        # productiehal
    for i in range(4):                                                                                           # sheddak
        P = sc.P; x = 0.4 + i * 1.15; a, b, c, d = P(x, 0.4, 2.2), P(x + 1.15, 0.4, 2.2), P(x + 1.15, 3.8, 2.2), P(x, 3.8, 2.2)
        t1, t2 = P(x + 0.3, 0.4, 2.7), P(x + 0.3, 3.8, 2.7)
        sc.voeg((x, 0.4, 2.2, x + 1.15, 3.8, 2.7), _poly([a, t1, t2, d], GLAS) + _poly([t1, b, c, t2], GRIJS_T))
    sc.blok(3.6, 3.9, 0, 0.5, 0.5, 4.6, GRIJS_T, GRIJS_L, GRIJS_R)                                              # schoorsteen
    rx, ry = sc.P(3.85, 4.15, 4.6)
    sc.voeg((3.6, 3.9, 4.6, 4.1, 4.4, 5.6), f'<g class="anim-rook"><circle cx="{rx:.1f}" cy="{ry-6:.1f}" r="5" fill="#D5DBE1" opacity=".8"/><circle cx="{rx+4:.1f}" cy="{ry-14:.1f}" r="4" fill="#D5DBE1" opacity=".6"/></g>', pad=(6, 22, 12, 2))
    sc.cilinder(1.2, 4.6, 0.42, 3.0, GRIJS_T, GRIJS_L); sc.cilinder(2.3, 4.6, 0.42, 3.0, GRIJS_T, GRIJS_L)        # silo's
    sc.blok(0.4, 5.4, 0, 3.0, 2.0, 1.4, WIT_T, WIT_L, WIT_R, ramen=(1, 3), deur=(0.4, 0.6, 1.0), deur_anim=True)   # kantoor
    sc.blok(7.2, 0.4, 0, 4.6, 3.4, 2.8, MIDDEN2, MIDDEN, DONKER, ramen=(1, 4))                                  # distributiecentrum
    for i in range(3): sc.blok(7.6 + i * 1.3, 3.8, 0, 0.9, 0.05, 1.1, DONKER, DONKER, DONKER)                    # laaddocks
    for i in range(3): sc.blok(7.7 + i * 1.3, 3.95, 0, 0.7, 0.5, 0.35, ZAND_T, ZAND_L, ZAND_R)                   # pallets
    sc.blok(7.2, 5.0, 0, 4.6, 2.4, 1.6, GRIJS_T, GRIJS_L, GRIJS_R, ramen=(1, 4))                                # opslaghal
    sc.hek(7.0, 0.2, 5.0, 7.5, 0.5); sc.hek(0.2, 0.2, 5.2, 7.5, 0.5)                                            # hekwerk
    sc.blok(6.9, 7.0, 0, 0.7, 0.7, 0.9, WIT_T, WIT_L, WIT_R, deur=(0.1, 0.3, 0.7)); sc.slagboom(5.4, 7.15, 1.4)   # portier en slagboom bij de inrit
    sc.vlak(0.4, 9.4, 4.6, 2.4, GROND2)                                                                          # containerterrein
    for i in range(3): sc.blok(2.3 + i * 0.95, 9.6, 0, 0.85, 0.85, 0.8, MIDDEN2, MIDDEN, DONKER)
    sc.blok(2.3, 9.6, 0.8, 0.85, 0.85, 0.8, LICHT2, LICHT, MIDDEN); sc.blok(3.25, 9.6, 0.8, 0.85, 0.85, 0.8, ROOD_T, ROOD_L, ROOD_R)
    sc.blok(2.3, 10.8, 0, 0.85, 0.85, 0.8, ROOD_T, ROOD_L, ROOD_R)
    sc.heftruck(1.2, 9.7)
    sc.blok(5.6, 9.4, 0, 4.0, 2.4, 1.6, WIT_T, WIT_L, WIT_R, ramen=(1, 4), deur=(0.5, 0.6, 1.0))                # expeditie (midden, uitrit blijft vrij)
    sc.auto(1.6, 8.05, GRIJS_R, klas="anim-auto", lang=2.6)                                                     # de enige vrachtwagen
    _bomen(sc, [(10.4, 9.8), (11.6, 11.0), (10.6, 11.8), (5.2, 4.9)], 0.45, 1.2)
    sc.persoon(7.9, 7.7, GEEL_L); sc.persoon(1.0, 11.2, DONKER); sc.struik(10.4, 10.6); sc.struik(4.6, 7.8)
    return sc.svg(444, 350, "Isometrische tekening van een bedrijvenpark met productiehal, silo's, distributiecentrum met laaddocks, containers, heftruck, vrachtwagen en slagboom")

def overheid():
    """Overheid: gemeentehuis met zuilen en klokkentoren, plein met drie Nederlandse vlaggen en fontein, Binnenhof-achtig gebouw met twee spitse torens en hofvijver, rechtbank en provinciehuis; vlaggen wapperen, één auto rijdt."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    _weg_x(sc, 7.8); _weg_y(sc, 6.2, y0=0, y1=7.8); sc.zebra(2.2, 7.8, 1.2, 1.0, 4); sc.zebra(6.2, 6.4, 1.0, 1.0, 4); _aansluiting(sc, 7.8)
    for m in (0.5, 4.0, 9.0, 11.8): sc.lantaarn(m, 7.7)
    sc.blok(0.4, 0.4, 0, 5.2, 3.0, 2.8, ZAND_T, ZAND_L, ZAND_R, ramen=(2, 5), deur=(2.3, 0.7, 1.4), deur_anim=True)   # gemeentehuis
    sc.zuilen(0.7, 3.4, 6, 2.8, afstand=0.85); sc.blok(0.4, 3.4, 2.8, 5.2, 0.5, 0.25, ZAND_T, ZAND_L, ZAND_R)     # zuilengalerij met fries
    sc.blok(2.5, 1.4, 2.8, 1.0, 1.0, 1.6, ZAND_T, ZAND_L, ZAND_R); sc.klok(3.0, 2.4, 3.9); sc.spits(2.5, 1.4, 4.4, 1.0, 1.0, 0.9)   # klokkentoren
    sc.vlak(0.4, 3.9, 5.2, 3.5, GROND2)                                                                          # plein
    sc.ellips(1.6, 5.4, 0.7, 0.7, LICHT); sc.groep("anim-water", lambda: sc.ellips(1.6, 5.4, 0.48, 0.48, GLAS2, z=0.02))   # fontein
    for fx in (3.2, 4.2, 5.2): sc.vlag(fx, 6.6, 2.6, nl=True)                                                    # drie Nederlandse vlaggen op het plein
    sc.blok(7.4, 0.4, 0, 4.4, 2.8, 2.3, ROOD_T, ROOD_L, ROOD_R, ramen=(2, 4), deur=(1.9, 0.7, 1.3))             # regeringsgebouw (Binnenhof-stijl)
    sc.dak(7.4, 0.4, 2.3, 4.4, 2.8, 0.7, "x", (DAK_T, DAK_L, DAK_R))
    for tx in (7.2, 11.2):                                                                                       # twee spitse torens
        sc.blok(tx, 2.6, 0, 0.75, 0.75, 3.6, ROOD_T, ROOD_L, ROOD_R, ramen=(3, 1)); sc.spits(tx, 2.6, 3.6, 0.75, 0.75, 1.3)
    sc.ellips(9.6, 5.3, 2.2, 1.2, LICHT); sc.groep("anim-water", lambda: sc.ellips(9.6, 5.3, 1.9, 0.95, GLAS2, z=0.02))   # hofvijver
    _bomen(sc, [(7.5, 6.9), (11.7, 6.9), (11.8, 3.9)], 0.4, 1.1)
    sc.vlak(0.4, 9.0, 3.4, 3.0, GROEN2); _bomen(sc, [(2.4, 9.6), (3.2, 11.0), (2.0, 11.7)])                    # park links vooraan (inrit blijft vrij)
    sc.blok(4.2, 9.0, 0, 4.0, 2.8, 2.4, WIT_T, WIT_L, WIT_R, ramen=(2, 4), deur=(1.6, 0.6, 1.2)); sc.zuilen(4.5, 11.8, 4, 2.4, WIT_T, 1.0)   # rechtbank (midden)
    sc.vlak(8.6, 9.0, 3.4, 3.0, GROEN2); _bomen(sc, [(9.6, 9.6), (11.0, 10.6), (9.8, 11.7)])                    # park rechts vooraan (uitrit blijft vrij)
    sc.auto(8.4, 7.95, DONKER, klas="anim-auto")
    sc.persoon(2.6, 4.6); sc.persoon(4.6, 5.8, DONKER); sc.persoon(7.0, 8.5, GROENDONKER); sc.struik(0.7, 4.2); sc.struik(0.7, 4.9); sc.struik(5.3, 4.2)
    return sc.svg(444, 350, "Isometrische tekening van een gemeentehuis met klokkentoren en Nederlandse vlaggen, regeringsgebouw met torens en hofvijver, rechtbank en provinciehuis")

def retail():
    """Retail: winkelstraat met vier winkels met gekleurde luifels en etalages, supermarkt met parkeerplaats en winkelwagentjes, bloemenkraam; een bestelbus rijdt."""
    sc = _nieuw(); sc.vlak(0, 0, G, G, GROND)
    sc.vlak(0, 3.6, G, 1.4, GROND2); sc.vlak(0, 6.0, G, 1.0, GROND2)                                           # brede stoep (winkelstraat)
    _weg_x(sc, 5.0); sc.zebra(5.4, 5.0, 1.2, 1.0, 4); _aansluiting(sc, 5.0)
    for m in (1.5, 5.0, 8.5, 11.5): sc.lantaarn(m, 4.9)
    def winkel(x, w, kl, luifel, ramen=(1, 2), deur=(0.3, 0.55, 1.1)):
        sc.blok(x, 0.6, 0, w, 3.0, 2.4, *kl, ramen=ramen)                                                        # winkel met woning erboven
        P = sc.P; R = lambda x0, z0, x1, z1: _poly([P(x0, 3.6, z0), P(x1, 3.6, z0), P(x1, 3.6, z1), P(x0, 3.6, z1)], GLAS)
        sc.voeg((x + 0.2, 3.6, 0.1, x + w - 0.2, 3.6, 1.05), R(x + deur[0] + deur[1] + 0.15, 0.1, x + w - 0.2, 1.05))   # etalage
        sc.voeg((x + deur[0], 3.6, 0, x + deur[0] + deur[1], 3.6, deur[2]), _poly([P(x + deur[0], 3.6, 0), P(x + deur[0] + deur[1], 3.6, 0), P(x + deur[0] + deur[1], 3.6, deur[2]), P(x + deur[0], 3.6, deur[2])], DONKER))
        lx, ly = P(x + deur[0] + deur[1] + 0.3, 3.6, 0.65)
        sc.voeg((x + deur[0] + deur[1] + 0.3, 3.6, 0.5, x + deur[0] + deur[1] + 0.3, 3.6, 0.8), f'<rect x="{lx-3:.1f}" y="{ly-6:.1f}" width="6" height="12" rx="1" fill="#FFFFFF" stroke="{DONKER}" stroke-width="0.6"/><circle class="led" cx="{lx:.1f}" cy="{ly-2:.1f}" r="1.6" fill="{GROEN}"/>')
        sc.blok(x + 0.1, 3.6, 1.15, w - 0.2, 0.55, 0.07, *luifel)                                                # luifel
    winkel(0.4, 2.8, (ROOD_T, ROOD_L, ROOD_R), (KRUIS_T, KRUIS_L, KRUIS_R))
    winkel(3.3, 2.8, (WIT_T, WIT_L, WIT_R), (LICHT2, LICHT, MIDDEN))
    winkel(6.2, 2.8, (ZAND_T, ZAND_L, ZAND_R), (GROEN2, GROEN, GROENDONKER))
    winkel(9.1, 2.7, (ROOD_T, ROOD_L, ROOD_R), (GEEL_T, GEEL_L, GEEL_R))
    sc.blok(3.6, 4.0, 0, 0.9, 0.5, 0.5, GROEN2, GROEN, GROENDONKER); sc.blok(3.7, 4.05, 0.5, 0.7, 0.4, 0.2, KRUIS_T, GEEL_L, LICHT)   # bloemenkraam op de stoep
    sc.vlak(0.4, 7.4, 3.4, 3.4, GROND2)                                                                          # parkeerplaats links vooraan (inrit blijft vrij)
    for i in range(5): sc.lijn_grond(0.6 + i * 0.75, 7.6, 0.6 + i * 0.75, 9.2, "#FFFFFF", 0.8)
    sc.bord(3.6, 7.5, "P")
    for i in range(3): sc.blok(0.8 + i * 0.5, 9.9, 0.15, 0.35, 0.5, 0.35, GRIJS_T, GRIJS_L, GRIJS_R)             # winkelwagentjes
    sc.blok(4.2, 7.4, 0, 5.4, 3.2, 2.2, MIDDEN2, MIDDEN, DONKER, ramen=(1, 5), deur=(0.6, 1.2, 1.4), deur_anim=True)   # supermarkt (midden, uitrit blijft vrij)
    sc.blok(4.2, 7.4, 2.2, 5.4, 0.5, 0.45, LICHT2, LICHT, MIDDEN)                                                # naambord op de gevelrand
    sc.vlak(10.0, 7.4, 2.0, 3.4, GROEN2)
    sc.auto(0.4, 5.15, DONKER, klas="anim-auto", lang=1.8)                                                       # bestelbus
    _bomen(sc, [(2.0, 11.4), (10.6, 8.2), (11.4, 10.0), (10.4, 11.4), (0.6, 6.7)], 0.45, 1.2)
    sc.persoon(2.0, 4.3); sc.persoon(5.2, 4.4, DONKER); sc.persoon(8.6, 4.2, KRUIS_L); sc.persoon(1.6, 6.5, GROENDONKER); sc.struik(10.4, 4.3); sc.struik(0.8, 4.4)
    return sc.svg(444, 350, "Isometrische tekening van een winkelstraat met luifels en etalages, een supermarkt met parkeerplaats en winkelwagentjes en een bestelbus")

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
            "recreatie": recreatie, "industrie": industrie, "overheid": overheid, "retail": retail, "woningcorporatie": woningcorporatie}
