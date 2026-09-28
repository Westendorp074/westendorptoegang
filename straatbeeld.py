"""Vlakke straatscènes als SVG, getekend in code (geen stock, geen AI-beeld). Vervangt de isometrische
scènes uit isometrie.py (Lars, 28-09-2026, naar het voorbeeld van de dormakaba-havenanimatie): recht
vooraanzicht, zachte schaduwen, wazige stad op de achtergrond en veel klein detail.

Opbouw per scène: lucht en verre stad, dan de panden op de horizonlijn, dan groen en lantaarns, dan de
weg (bewust zonder auto's, dat houdt de kaarten rustig en licht) en vooraan de stoep. Elke scène heeft één entree met paslezer waar iemand
naar binnen loopt (klassen sb-loop, sb-arm, sb-pui-l/r en led-deur, cyclus van 10 s in build.STRAAT_CSS)."""

W, H = 1000, 640
HOR = 436                                   # horizonlijn: onderkant van de panden
WEG_Y = HOR + 40                            # bovenkant van de rijweg (92 hoog), daaronder de stoep

# Palet
NAVY = "#123A6B"; BLAUW = "#2B5BA6"; LICHTBLAUW = "#49BFFE"; ROOD = "#D8342B"
GEVEL3 = "#DDE5EE"                          # schaduwzijde van een lichte gevel
GLAS, GLAS_L, GLAS_D, KOZIJN = "#AFCBE8", "#CBDFF2", "#8FB4DA", "#F4F7FA"
HAZE, HAZE2, HAZE_RAAM = "#DFE8F1", "#D2DEEA", "#EFF4F9"
BAKSTEEN, BAKSTEEN_D, VOEG = "#C9705F", "#A4523F", "#D98E7E"
STAAL, STAAL_D = "#C3CEDA", "#AAB8C6"
GROEN_B = ("#69B586", "#7FC79A", "#5AA377")                       # boomtinten
SCHADUW = "rgba(31,54,84,.14)"; SCHADUW_D = "rgba(20,35,55,.26)"
HUID = ("#F1C9A6", "#E8B48C", "#B57F52", "#7C4F2E")               # huidtinten, per scène afgewisseld
WIEL, VELG = "#242A31", "#B7C1CB"

DEFS = ('<defs>'
        '<linearGradient id="lucht" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCE9F5"/><stop offset=".7" stop-color="#F2F7FB"/><stop offset="1" stop-color="#FAFCFD"/></linearGradient>'
        '<linearGradient id="gevel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FDFEFE"/><stop offset="1" stop-color="#EBF0F5"/></linearGradient>'
        '<linearGradient id="baksteen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D07E6D"/><stop offset="1" stop-color="#C06A58"/></linearGradient>'
        '<linearGradient id="glasband" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C6DCF0"/><stop offset="1" stop-color="#9CBEE0"/></linearGradient>'
        '<linearGradient id="glastoren" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D4E5F4"/><stop offset="1" stop-color="#9FC0E0"/></linearGradient>'
        '<linearGradient id="zand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2EBDC"/><stop offset="1" stop-color="#E2D7C1"/></linearGradient>'
        '<linearGradient id="grond" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9EEF3"/><stop offset="1" stop-color="#DDE4EB"/></linearGradient>'
        '<linearGradient id="asfalt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#75828F"/><stop offset="1" stop-color="#616E7B"/></linearGradient>'
        '</defs>')


class Scene:
    def __init__(self, label, tempo=0):
        self.label = label
        self.tempo = tempo                  # verschuiving (s) van de entree-cyclus, zodat niet elke kaart tegelijk iemand binnenlaat
        self.d = []
        self.laat = []                      # bovenste laag (het entree-poppetje): altijd vóór bomen en lantaarns

    # ---- basisvormen ----
    def r(self, x, y, w, h, f, rx=0, e=""):
        self.d.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{f}" {e}/>')
    def p(self, d, f, e=""):
        self.d.append(f'<path d="{d}" fill="{f}" {e}/>')
    def c(self, cx, cy, r, f, e=""):
        self.d.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{f}" {e}/>')
    def el(self, cx, cy, rx, ry, f):
        self.d.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{f}"/>')
    def tekst(self, x, y, t, grootte=10, kleur=NAVY, spatie=2, e=""):
        self.d.append(f'<text x="{x:.0f}" y="{y:.0f}" font-family="Arial,sans-serif" font-size="{grootte}" font-weight="700" letter-spacing="{spatie}" fill="{kleur}" text-anchor="middle" {e}>{t}</text>')

    # ---- achtergrond ----
    def lucht(self):
        self.r(0, 0, W, HOR, "url(#lucht)")
    def wolken(self, posities=((140, 86, 1.15, .9), (430, 52, .75, .7), (720, 96, 1.3, .85), (920, 60, .6, .6))):
        for i, (x, y, s, op) in enumerate(posities):
            # de animatieklasse op een binnenste groep, anders overschrijft de CSS-transform de plaatsing
            self.d.append(f'<g fill="#fff" opacity="{op}" transform="translate({x} {y}) scale({s})"><g class="sb-wolk sb-wolk-{i % 3}">'
                          '<ellipse cx="0" cy="16" rx="52" ry="13"/><circle cx="-20" cy="7" r="14"/><circle cx="4" cy="-2" r="20"/><circle cx="28" cy="8" r="13"/></g></g>')
    def vogels(self, posities=((250, 70, 1), (268, 80, .8), (600, 46, 1), (820, 150, .9))):
        for x, y, s in posities:
            self.d.append(f'<path d="M{x} {y} q5 -5 10 0 q5 -5 10 0" fill="none" stroke="#93A5B8" stroke-width="{1.6 * s}" stroke-linecap="round" opacity=".8"/>')

    def skyline(self, soort="stad"):
        """Verre bebouwing in nevel; vervaagt onderaan in de lucht."""
        blokken = [(0, 60, 58), (64, 42, 92), (110, 74, 44), (158, 50, 120), (212, 64, 66), (282, 46, 84), (330, 80, 40),
                   (374, 56, 96), (434, 70, 52), (490, 48, 110), (604, 62, 74), (682, 52, 96), (742, 72, 46),
                   (792, 58, 88), (884, 66, 60), (948, 50, 90)]
        if soort == "dorp":
            blokken = [(x, w, max(24, h - 52)) for x, w, h in blokken]
        self.d.append("<g>")
        for x, w, h in blokken:
            self.r(x, HOR - 38 - h, w, h + 38, HAZE)
            if soort == "dorp":                                     # puntdaken
                self.p(f"M{x - 2} {HOR - 38 - h} h{w + 4} l-{w / 2 + 2} -{18 + h * .2} z", HAZE2)
            for wy in range(int(HOR - 30 - h), int(HOR - 44), 14):
                for wx in range(x + 6, x + w - 8, 12):
                    self.r(wx, wy, 5, 6, HAZE_RAAM)
        if soort == "stad":
            self.r(500, HOR - 178, 26, 178, HAZE2); self.p(f"M500 {HOR - 178} l13 -22 l13 22 z", HAZE2)   # kerktoren
        if soort == "industrie":
            for x in (150, 560):                                    # hijskranen in de verte
                self.d.append(f'<g fill="none" stroke="{HAZE2}" stroke-width="5"><path d="M{x} {HOR - 30} V{HOR - 150} M{x - 46} {HOR - 132} H{x + 66}"/><path d="M{x} {HOR - 150} L{x - 46} {HOR - 132} M{x} {HOR - 150} L{x + 66} {HOR - 132}" stroke-width="3"/></g>')
                self.d.append(f'<line x1="{x + 44}" y1="{HOR - 132}" x2="{x + 44}" y2="{HOR - 96}" stroke="{HAZE2}" stroke-width="2.5"/>')
            self.r(830, HOR - 140, 16, 140, HAZE2); self.r(862, HOR - 118, 16, 118, HAZE2)   # schoorstenen
        if soort == "groen":                                        # bosrand in plaats van stad
            for x in range(-20, W + 20, 46):
                self.c(x, HOR - 34, 34, HAZE)
        self.d.append(f'<rect x="0" y="{HOR - 70}" width="{W}" height="70" fill="url(#lucht)" opacity=".45"/></g>')

    def grond(self):
        self.r(0, HOR, W, H - HOR, "url(#grond)")

    def weg(self, streep=True, zebra=None):
        self.r(0, WEG_Y, W, 92, "url(#asfalt)")
        self.r(0, WEG_Y, W, 3, "#8B99A7"); self.r(0, WEG_Y + 89, W, 3, "#55616D")
        if streep:
            for x in range(14, W, 64):
                self.r(x, WEG_Y + 44, 34, 4.5, "#E8EDF2", 2, 'opacity=".85"')
        if zebra is not None:
            for x in range(zebra, zebra + 96, 16):
                self.r(x, WEG_Y + 6, 9, 80, "#E8EDF2", 2, 'opacity=".9"')
        self.r(0, WEG_Y + 96, W, H - WEG_Y - 96, "#E4EAF0"); self.r(0, WEG_Y + 96, W, 4, "#C2CCD7")   # stoep

    def parkeervakken(self, van=60, tot=W, stap=170):
        for x in range(van, tot, stap):
            self.r(x, WEG_Y + 110, 3.5, 52, "#fff", 0, 'opacity=".8"')

    # ---- panden ----
    def pand(self, x, w, h, vul="url(#gevel)", dak=NAVY, schaduwzijde=True):
        """Basisblok op de horizonlijn met dakrand en zachte slagschaduw; geeft de bovenrand (y) terug."""
        y = HOR - h
        self.el(x + w / 2, HOR + 4, w * .62, 7, SCHADUW)
        self.r(x - 6, y - 14, w + 12, 16, dak, 3)
        self.r(x, y, w, h, vul)
        if schaduwzijde:
            self.r(x + w - min(40, w * .14), y, min(40, w * .14), h, GEVEL3)
        return y

    def glasband(self, x, y, w, h=26):
        self.r(x, y, w, h, "url(#glasband)", 2); self.r(x, y, w, h * .27, GLAS_L, 2)
        for wx in range(int(x), int(x + w - 2), 22):
            self.r(wx, y, 1.6, h, KOZIJN)
        self.r(x, y + h, w, 3, "#D3DCE6")

    def ramen(self, x, y, kol, rij, bw=30, bh=22, dx=42, dy=42, kader=None):
        for j in range(rij):
            for i in range(kol):
                wx, wy = x + i * dx, y + j * dy
                if kader:
                    self.r(wx - 2, wy - 2, bw + 4, bh + 4, kader, 2)
                self.r(wx, wy, bw, bh, GLAS, 2); self.r(wx, wy, bw, bh * .3, GLAS_L, 2)
                self.r(wx + bw / 2, wy, 1.5, bh, KOZIJN)

    def dak_installatie(self, x, y):
        self.r(x, y - 26, 84, 26, STAAL, 2); self.r(x + 8, y - 32, 18, 8, STAAL_D)

    def dak_leuning(self, x, w, y):
        for lx in range(int(x), int(x + w), 12):
            self.r(lx, y - 12, 1.5, 12, "#9FB0C2")
        self.r(x, y - 13, w, 2, "#9FB0C2")

    # ---- entree met paslezer en persoon die naar binnen loopt ----
    def entree(self, x, w=108, h=90, luifel=True, bord=None, huid=0, jas=BLAUW):
        """Glazen schuifpui onderin een pand: pui die opengaat, lezer met led en een persoon die badget
        en naar binnen loopt (10s-cyclus, klassen in build.STRAAT_CSS)."""
        y = HOR - h
        if luifel:
            self.r(x - 22, y - 18, w + 44, 9, NAVY, 2)
            self.d.append(f'<rect x="{x - 14}" y="{y - 9}" width="3" height="{h + 9}" fill="#8A9BAD"/><rect x="{x + w + 11}" y="{y - 9}" width="3" height="{h + 9}" fill="#8A9BAD"/>')
        if bord:
            wb = 8.4 * len(bord.replace("&#160;", " ")) + 16
            self.r(x + w / 2 - wb / 2, y - 38, wb, 16, "#FFFFFF", 3, 'opacity=".92"')
            self.tekst(x + w / 2, y - 26, bord, 10, NAVY)
        self.r(x - 4, y, w + 8, h, "#7E97B4", 2)
        self.r(x, y + 4, w, h - 4, GLAS_D)                          # vaste pui
        self.r(x, y + 4, w, 22, GLAS)
        m = x + w / 2
        self.p(f"M{x + 6} {y + h - 2} l22 -52 l6 0 l-20 52 z", "#DFEBF6", 'opacity=".45"')   # glans, vóór hal en deuren
        self.r(m - 26, y + 4, 52, h - 4, "#37536F")                 # donkere hal, zichtbaar als de pui opengaat
        self.d.append(f'<g class="sb-pui-l"><rect x="{m - 26}" y="{y + 4}" width="26" height="{h - 4}" fill="{GLAS_D}" stroke="#E8EEF5" stroke-width="2"/></g>')
        self.d.append(f'<g class="sb-pui-r"><rect x="{m}" y="{y + 4}" width="26" height="{h - 4}" fill="{GLAS_D}" stroke="#E8EEF5" stroke-width="2"/></g>')
        self.r(m - 27, y + 4, 54, h - 4, "none", 0, 'stroke="#5F7A99" stroke-width="1.5"')
        # lezer op zuiltje
        zx = x + w + 26
        self.r(zx + 6, HOR - 32, 5, 32, "#8595A6", 1)
        self.r(zx, HOR - 58, 16, 28, "#FFFFFF", 3, f'stroke="{NAVY}" stroke-width="1.6"')
        self.d.append(f'<circle cx="{zx + 8}" cy="{HOR - 49}" r="3.4" class="led-deur"/>')
        self.r(zx + 4.5, HOR - 42, 7, 8, GLAS, 1)
        # persoon: komt van rechts (desnoods van buiten beeld), badget bij het zuiltje, loopt naar de pui;
        # in de uitgestelde laag zodat hij vóór bomen en lantaarns langsloopt, met de schaduw in de groep mee
        px = zx + 22
        ix = 150 if px + 170 <= W else (W - px) + 70
        self.laat.append(
            f'<g class="sb-loop" style="--ix:{ix}px;--dx:{m - px:.0f}px">'
            f'<ellipse cx="{px}" cy="{HOR + 2}" rx="12" ry="3.5" fill="{SCHADUW}"/>'
            f'<path d="M-6 0 l2 -20 h8 l2 20 h-4 l-2 -13 l-2 13 z" fill="{NAVY}" transform="translate({px} {HOR})"/>'
            f'<rect x="{px - 7}" y="{HOR - 46}" width="14" height="27" rx="6" fill="{jas}"/>'
            f'<g class="sb-arm"><path d="M{px - 6} {HOR - 42} L{px - 21} {HOR - 36}" stroke="{jas}" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="{px - 28}" y="{HOR - 41}" width="10" height="7" rx="1.2" fill="#fff" stroke="{NAVY}" stroke-width="1"/></g>'
            f'<circle cx="{px}" cy="{HOR - 53}" r="6.5" fill="{HUID[huid]}"/>'
            f'<path d="M{px - 6.5} {HOR - 55} a6.5 6.5 0 0 1 13 0 l-2 1.5 a5 5 0 0 0 -9 0 z" fill="#4A3A2C"/></g>')
        return y

    # ---- groen en straatmeubilair ----
    def boom(self, x, s=1.0, tint=0, anim=True):
        k1, k2 = GROEN_B[tint % 3], ("#8CD3A8", "#9BDCB4", "#79BE93")[tint % 3]
        self.el(x, HOR + 30 * s, 20 * s, 5 * s, SCHADUW)
        klas = f'<g class="sb-boom sb-boom-{tint % 3}">' if anim else "<g>"
        self.d.append(f'<g transform="translate({x} {HOR}) scale({s})">{klas}<path d="M-2.5 30 L-1 -6 h2 L3.5 30 z" fill="#7A6250"/>'
                      f'<path d="M0 -8 q4 6 10 8" stroke="#7A6250" stroke-width="2" fill="none"/>'
                      f'<circle cx="0" cy="-22" r="21" fill="{k1}"/><circle cx="-11" cy="-30" r="12" fill="{k2}"/>'
                      f'<circle cx="12" cy="-15" r="11" fill="{k2}"/><circle cx="5" cy="-32" r="9" fill="{k2}" opacity=".8"/></g></g>')

    def heg(self, x, w):
        self.r(x, HOR + 22, w, 13, "#7CC496", 6); self.r(x, HOR + 22, w, 5, "#93D3AA", 6)

    def lantaarn(self, x):
        self.el(x + 2, HOR + 36, 6, 2, SCHADUW)
        self.d.append(f'<rect x="{x}" y="{HOR - 52}" width="3.5" height="88" fill="#8595A6"/>'
                      f'<path d="M{x - 9} {HOR - 52} h21 v5 h-21 z" fill="#8595A6"/><circle cx="{x + 1.7}" cy="{HOR - 44}" r="2.6" fill="#FFF3B0"/>')

    def vlag(self, x, y, hoogte=64, doek=None):
        """Vlaggenmast; doek None = Nederlandse vlag."""
        self.d.append(f'<rect x="{x}" y="{y - hoogte}" width="2.5" height="{hoogte}" fill="#8595A6"/>')
        if doek is None:
            self.d.append(f'<g class="sb-vlag"><rect x="{x + 2.5}" y="{y - hoogte}" width="34" height="7" fill="#AE1C28"/>'
                          f'<rect x="{x + 2.5}" y="{y - hoogte + 7}" width="34" height="7" fill="#fff"/>'
                          f'<rect x="{x + 2.5}" y="{y - hoogte + 14}" width="34" height="7" fill="#21468B"/></g>')
        else:
            self.d.append(f'<g class="sb-vlag"><rect x="{x + 2.5}" y="{y - hoogte}" width="34" height="21" fill="{doek}"/></g>')

    # ---- mensen ----
    def persoon(self, x, y, jas=BLAUW, broek=NAVY, huid=0, haar="#4A3A2C", lopend=False):
        self.el(x, y + 2, 11, 3.5, SCHADUW)
        benen = (f'<path d="M{x - 6} {y} l1 -19 h10 l1 19 h-4 l-2 -12 l-2 12 z" fill="{broek}"/>' if not lopend else
                 f'<path d="M{x - 9} {y} l4 -19 h10 l7 17 -4 2 -6 -13 -2 13 z" fill="{broek}"/>')
        self.d.append(f'<g>{benen}<rect x="{x - 7}" y="{y - 46}" width="14" height="27" rx="6" fill="{jas}"/>'
                      f'<circle cx="{x}" cy="{y - 53}" r="6.5" fill="{HUID[huid]}"/>'
                      f'<path d="M{x - 6.5} {y - 55} a6.5 6.5 0 0 1 13 0 l-2 1.5 a5 5 0 0 0 -9 0 z" fill="{haar}"/></g>')

    def kind(self, x, y, trui=ROOD, huid=0):
        self.el(x, y + 1, 8, 2.5, SCHADUW)
        self.d.append(f'<g><path d="M{x - 4} {y} l1 -12 h6 l1 12 h-3 l-1 -8 -1 8 z" fill="{NAVY}"/>'
                      f'<rect x="{x - 5}" y="{y - 30}" width="10" height="19" rx="4.5" fill="{trui}"/>'
                      f'<circle cx="{x}" cy="{y - 35}" r="5.5" fill="{HUID[huid]}"/>'
                      f'<path d="M{x - 5.5} {y - 36.5} a5.5 5.5 0 0 1 11 0 l-1.5 1.2 a4 4 0 0 0 -8 0 z" fill="#5A4636"/></g>')

    # ---- voertuigen (getekend rond x=0 op de wegas; rijdend=True laat ze over de weg rijden) ----
    def _wiel(self, cx, cy, r):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WIEL}"/><circle cx="{cx}" cy="{cy}" r="{r * .42:.1f}" fill="{VELG}"/><circle cx="{cx}" cy="{cy}" r="{r * .16:.1f}" fill="#7B8792"/>'

    def auto(self, kleur=BLAUW, x=0, rijdend=False, duur=17, wacht=0, terug=False):
        y = WEG_Y + 8 if rijdend else WEG_Y + 102
        lijf = (f'<ellipse cx="67" cy="50" rx="74" ry="6" fill="{SCHADUW_D}"/>'
                f'<path d="M0 34 q1 -13 15 -15 l20 -15 q3 -3 8 -3 h44 q5 0 8 3 l22 15 q16 2 18 15 l1 8 q0 6 -6 6 h-124 q-6 0 -6 -6 z" fill="{kleur}"/>'
                f'<path d="M40 4 h36 q3 0 5 2 l14 11 h-70 l12 -11 q1 -2 3 -2 z" fill="#BFD9F2"/><rect x="57" y="4" width="3" height="13" fill="{kleur}"/>'
                '<path d="M0 34 q1 -13 15 -15 h104 q16 2 18 15 z" fill="#fff" opacity=".08"/>'
                + self._wiel(30, 46, 12) + self._wiel(104, 46, 12) +
                '<rect x="129" y="26" width="6" height="5" rx="2" fill="#FFF3B0"/><rect x="0" y="26" width="5" height="5" rx="2" fill="#E77B72"/>')
        self._plaats(lijf, x, y, rijdend, duur, wacht, terug)

    def bestelbus(self, kleur="#F4F7FA", tekst=None, tekstkleur=NAVY, x=0, rijdend=False, duur=15, wacht=0, terug=False):
        y = WEG_Y - 2 if rijdend else WEG_Y + 92
        lijf = (f'<ellipse cx="82" cy="60" rx="88" ry="7" fill="{SCHADUW_D}"/>'
                f'<path d="M6 -30 h104 q6 0 6 6 v78 h-116 v-78 q0 -6 6 -6 z" fill="{kleur}"/>'
                f'<path d="M116 -24 h26 q8 0 12 7 l9 15 q4 6 4 12 v40 q0 4 -4 4 h-47 z" fill="{kleur}"/>'
                f'<path d="M122 -18 h19 q5 0 8 5 l7 12 h-34 z" fill="{GLAS}"/>'
                f'<rect x="10" y="-24" width="92" height="30" rx="3" fill="{GLAS}" opacity=".25"/>'
                + ((f'<g transform="translate(116 0) scale(-1 1)">' if terug else "<g>") +
                   f'<text x="58" y="14" font-family="Arial,sans-serif" font-size="13" font-weight="800" fill="{tekstkleur}" text-anchor="middle" letter-spacing="1">{tekst}</text></g>' if tekst else "")
                + self._wiel(34, 54, 14) + self._wiel(138, 54, 14) +
                '<rect x="163" y="30" width="6" height="6" rx="2" fill="#FFF3B0"/><rect x="0" y="30" width="5" height="6" rx="2" fill="#E77B72"/>')
        self._plaats(lijf, x, y, rijdend, duur, wacht, terug)

    def _plaats(self, lijf, x, y, rijdend, duur, wacht, terug):
        if rijdend:
            richting = ' transform="scale(-1 1)"' if terug else ""
            klas = "sb-rij-terug" if terug else "sb-rij"
            self.d.append(f'<g class="{klas}" style="--duur:{duur}s;--wacht:{wacht}s"><g transform="translate(0 {y})"><g{richting}>{lijf}</g></g></g>')
        else:
            self.d.append(f'<g transform="translate({x} {y})">{lijf}</g>')

    def vrachtwagen(self, kleur=BLAUW, tekst=None, rijdend=True, duur=22, wacht=0, terug=False, x=0):
        y = WEG_Y - 14 if rijdend else WEG_Y + 80
        lijf = (f'<ellipse cx="120" cy="74" rx="130" ry="8" fill="{SCHADUW_D}"/>'
                f'<rect x="0" y="-28" width="176" height="86" rx="4" fill="#EDF1F6"/>'
                f'<rect x="4" y="-24" width="168" height="66" rx="2" fill="{kleur}" opacity=".12"/>'
                + ((f'<g transform="translate(176 0) scale(-1 1)">' if terug else "<g>") +
                   f'<text x="88" y="18" font-family="Arial,sans-serif" font-size="16" font-weight="800" fill="{kleur}" text-anchor="middle" letter-spacing="1">{tekst}</text></g>' if tekst else "")
                + f'<rect x="182" y="4" width="60" height="54" rx="4" fill="{kleur}"/>'
                f'<path d="M242 12 h14 q7 0 11 7 l7 12 q3 5 3 10 v13 q0 4 -4 4 h-31 z" fill="{kleur}"/>'
                f'<path d="M246 16 h9 q4 0 7 4 l6 11 h-22 z" fill="{GLAS}"/>'
                f'<rect x="186" y="10" width="30" height="20" rx="2" fill="{GLAS}"/>'
                + self._wiel(38, 66, 15) + self._wiel(78, 66, 15) + self._wiel(210, 66, 15) + self._wiel(252, 66, 15) +
                '<rect x="272" y="42" width="6" height="6" rx="2" fill="#FFF3B0"/>')
        self._plaats(lijf, x, y, rijdend, duur, wacht, terug)

    def taxi(self, rijdend=True, duur=16, wacht=0, terug=False, x=0):
        y = WEG_Y + 8 if rijdend else WEG_Y + 102
        lijf = (f'<ellipse cx="67" cy="50" rx="74" ry="6" fill="{SCHADUW_D}"/>'
                '<path d="M0 34 q1 -13 15 -15 l20 -15 q3 -3 8 -3 h44 q5 0 8 3 l22 15 q16 2 18 15 l1 8 q0 6 -6 6 h-124 q-6 0 -6 -6 z" fill="#2B3A4A"/>'
                f'<path d="M40 4 h36 q3 0 5 2 l14 11 h-70 l12 -11 q1 -2 3 -2 z" fill="{GLAS}"/><rect x="57" y="4" width="3" height="13" fill="#2B3A4A"/>'
                '<rect x="48" y="-8" width="26" height="9" rx="2.5" fill="#F7C948"/><text x="61" y="-1" font-family="Arial,sans-serif" font-size="7" font-weight="800" fill="#2B3A4A" text-anchor="middle">TAXI</text>'
                + self._wiel(30, 46, 12) + self._wiel(104, 46, 12) +
                '<rect x="129" y="26" width="6" height="5" rx="2" fill="#FFF3B0"/>')
        self._plaats(lijf, x, y, rijdend, duur, wacht, terug)

    def caravan_combi(self, kleur=NAVY, rijdend=True, duur=24, wacht=0, terug=False, x=0):
        """Auto met caravan, voor recreatie."""
        y = WEG_Y + 8 if rijdend else WEG_Y + 102
        lijf = (f'<ellipse cx="140" cy="50" rx="150" ry="7" fill="{SCHADUW_D}"/>'
                '<path d="M0 26 q0 -18 10 -20 h96 q12 2 12 20 v14 q0 4 -4 4 h-110 q-4 0 -4 -4 z" fill="#F6F8FA"/>'
                '<rect x="10" y="-14" width="96" height="34" rx="10" fill="#E7EDF3"/>'
                f'<rect x="18" y="-8" width="34" height="18" rx="3" fill="{GLAS}"/><rect x="62" y="-8" width="34" height="18" rx="3" fill="{GLAS}"/>'
                f'<rect x="4" y="8" width="108" height="5" fill="{kleur}" opacity=".5"/>'
                + self._wiel(58, 42, 11) +
                '<path d="M112 30 h26" stroke="#5B6B7C" stroke-width="4"/>'
                f'<path d="M138 34 q1 -12 14 -14 l19 -14 q3 -3 8 -3 h28 q5 0 8 3 l21 14 q15 2 17 14 l1 7 q0 6 -6 6 h-105 q-6 0 -6 -6 z" fill="{kleur}"/>'
                f'<path d="M176 6 h24 q3 0 5 2 l13 10 h-56 l11 -10 q1 -2 3 -2 z" fill="{GLAS}"/>'
                + self._wiel(166, 45, 11) + self._wiel(226, 45, 11) +
                '<rect x="248" y="26" width="6" height="5" rx="2" fill="#FFF3B0"/>')
        self._plaats(lijf, x, y, rijdend, duur, wacht, terug)

    def fietser(self, x, y, kleur=NAVY, huid=0):
        """Iemand die met de fiets aan de hand staat (bewust niet rijdend: geen zware doorlopende animatie)."""
        self.el(x + 25, y + 21, 30, 4, SCHADUW_D)
        self.d.append(f'<g transform="translate({x} {y})"><circle cx="0" cy="8" r="13" fill="none" stroke="#3B4650" stroke-width="2.5"/><circle cx="34" cy="8" r="13" fill="none" stroke="#3B4650" stroke-width="2.5"/>'
                      f'<path d="M0 8 L12 -8 h14 L34 8 M12 -8 L18 8 L0 8 M26 -8 l-3 -6 h6 M12 -8 l-2 -7 h-5" stroke="{ROOD}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
                      f'<path d="M44 21 l1.5 -18 h9 l1.5 18 h-4 l-2.5 -12 -2.5 12 z" fill="{NAVY}"/>'
                      f'<rect x="43" y="-24" width="14" height="27" rx="6" fill="{kleur}"/>'
                      f'<path d="M45 -18 L28 -12" stroke="{kleur}" stroke-width="5" stroke-linecap="round"/>'
                      f'<circle cx="50" cy="-31" r="6.5" fill="{HUID[huid]}"/>'
                      f'<path d="M43.5 -33 a6.5 6.5 0 0 1 13 0 l-2 1.5 a5 5 0 0 0 -9 0 z" fill="#6B4A2F"/></g>')

    def fietsenrek(self, x, n=5):
        for i in range(n):
            fx = x + i * 17
            self.d.append(f'<g opacity="{.95 - (i % 2) * .25}"><circle cx="{fx}" cy="{HOR + 26}" r="8" fill="none" stroke="#5B6B7C" stroke-width="1.8"/>'
                          f'<circle cx="{fx + 12}" cy="{HOR + 26}" r="8" fill="none" stroke="#5B6B7C" stroke-width="1.8"/>'
                          f'<path d="M{fx} {HOR + 26} l5 -12 h6 l1 -3 M{fx + 5} {HOR + 14} l7 12" stroke="#5B6B7C" stroke-width="1.8" fill="none"/></g>')

    # ---- uitvoer ----
    def svg(self):
        stijl = f' style="--tempo:-{self.tempo}s"' if self.tempo else ""
        return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{self.label}"{stijl} '
                f'xmlns="http://www.w3.org/2000/svg" class="iso">{DEFS}' + "".join(self.d) + "".join(self.laat) + "</svg>")


def _basis(label, skyline="stad", tempo=0):
    """Standaardopbouw: lucht, wolken, vogels, verre stad, grond."""
    sc = Scene(label, tempo)
    sc.lucht(); sc.wolken(); sc.vogels(); sc.skyline(skyline); sc.grond()
    return sc


# ================= scènes per sector =================

def zorg():
    sc = _basis("Tekening van een ziekenhuis met spoedpost en een hoofdingang met paslezer")
    # hoofdtoren met glasbanden en het rode kruis
    bx, bw, bh = 300, 330, 300; by = sc.pand(bx, bw, bh)
    for rij in range(6):
        sc.glasband(bx + 14, by + 26 + rij * 44, bw - 28)
    sc.r(bx + 128, by - 6, 74, bh + 6, "url(#gevel)"); sc.r(bx + 128, by - 6, 74, bh + 6, "#FFFFFF", 0, 'opacity=".55"')
    sc.d.append(f'<rect x="{bx + 128}" y="{by - 6}" width="74" height="{bh + 6}" fill="none" stroke="#E1E8F0" stroke-width="1.5"/>')
    kx, ky = bx + 165, by + 52
    sc.r(kx - 11, ky - 34, 22, 68, ROOD, 3); sc.r(kx - 34, ky - 11, 68, 22, ROOD, 3)
    sc.tekst(kx, by + 150, "ST&#160;ANTONIUS", 13, NAVY, 3, f'transform="rotate(90 {kx} {by + 150})"')
    sc.dak_installatie(bx + 18, by - 14); sc.dak_installatie(bx + 230, by - 8); sc.dak_leuning(bx + 2, bw - 6, by - 16)
    sc.d.append(f'<line x1="{bx + 306}" y1="{by - 16}" x2="{bx + 306}" y2="{by - 58}" stroke="#8A9BAD" stroke-width="2.5"/>')
    sc.c(bx + 306, by - 60, 3, ROOD)
    # spoedpost met ambulancesluis
    vy = sc.pand(96, 190, 132, schaduwzijde=False)
    sc.ramen(110, vy + 16, 4, 1, 32, 24, 44)
    sc.r(108, vy + 50, 128, 15, ROOD, 2); sc.tekst(172, vy + 61, "SPOEDPOST", 9.5, "#fff", 1)
    sc.r(140, vy + 78, 66, 54, "#B9C7D6", 3)
    for ly in range(int(vy + 82), int(vy + 128), 7):
        sc.r(143, ly, 60, 2.5, "#CBD7E3")
    sc.p(f"M130 {vy + 78} h86 l8 -12 h-102 z", NAVY)
    # entreeblok met hoofdingang
    ey = sc.pand(660, 240, 170); sc.ramen(674, ey + 16, 5, 1, 30, 22, 42)
    sc.tekst(758, ey + 56, "HOOFDINGANG", 10, NAVY)
    sc.entree(704, 108, 90, luifel=True, huid=0)
    # verpleegkundige
    sc.persoon(560, HOR + 26, jas="#FFFFFF", broek="#E8EDF2", huid=1, haar="#26160E", lopend=True)
    sc.d.append(f'<rect x="558" y="{HOR - 14}" width="8" height="5" rx="1" fill="{ROOD}" opacity=".9"/>')
    # groen, lantaarns, weg
    sc.boom(52, 1.05, 0); sc.boom(278, .8, 1); sc.boom(630, .78, 2); sc.boom(956, 1.1, 1)
    sc.heg(212, 72); sc.heg(700, 120); sc.heg(850, 90)
    sc.lantaarn(240); sc.lantaarn(480); sc.lantaarn(900)
    sc.weg()
    # stoep: fietser
    sc.fietser(130, WEG_Y + 132)
    return sc.svg()


def woningcorporatie():
    sc = _basis("Tekening van twee woonblokken van een woningcorporatie met portiekentree, bellentableau en paslezer", "dorp", tempo=3.4)
    # linker woonblok: baksteen met trappenhuis boven de entree
    bx, bw, bh = 110, 300, 248; by = sc.pand(bx, bw, bh, "url(#baksteen)", dak="#5A4038")
    sc.r(bx + bw - 34, by, 34, bh, BAKSTEEN_D)
    sc.r(bx + 118, by, 64, bh, "#B85F4D")                            # trappenhuisstrook
    for j in range(3):                                                # de onderste laag valt achter de entree, dus daar geen raam
        sc.r(bx + 134, by + 26 + j * 56, 32, 34, GLAS, 2, f'stroke="{KOZIJN}" stroke-width="3"'); sc.r(bx + 134, by + 26 + j * 56, 32, 10, GLAS_L, 2)
    sc.ramen(bx + 20, by + 24, 2, 4, 34, 26, 52, 56, kader=KOZIJN)
    sc.ramen(bx + 202, by + 24, 2, 4, 34, 26, 52, 56, kader=KOZIJN)
    for j in range(1, 4):                                             # franse balkons
        for wx in (bx + 20, bx + 72, bx + 202, bx + 254):
            sc.d.append(f'<g fill="none" stroke="#54636F" stroke-width="1.6"><path d="M{wx - 3} {by + 24 + j * 56 + 28} h40"/>' +
                        "".join(f'<path d="M{wx + i * 5} {by + 24 + j * 56 + 14} v14"/>' for i in range(0, 9)) + "</g>")
    sc.entree(bx + 112, 76, 84, luifel=False, huid=2, jas="#C9705F")
    sc.d.append(f'<rect x="{bx + 96}" y="{HOR - 62}" width="12" height="26" rx="2" fill="#EDF1F6" stroke="#8595A6" stroke-width="1.2"/>' +
                "".join(f'<circle cx="{bx + 102}" cy="{HOR - 57 + i * 5}" r="1.6" fill="#8595A6"/>' for i in range(4)))   # bellentableau
    # rechter woonblok, iets lager en lichter
    cx, cw, ch = 560, 330, 200; cy = sc.pand(cx, cw, ch, "url(#gevel)", dak="#5A4038")
    sc.tekst(cx + 165, cy + 24, "DE&#160;SCHAKEL", 11, NAVY, 3)
    sc.ramen(cx + 22, cy + 38, 4, 3, 34, 26, 54, 52, kader="#E2E8EF")
    # kliko's en fietsen bij de flat
    for i, kk in enumerate(("#4E5A66", "#3F7A52", "#4E5A66")):
        kx = 468 + i * 26
        sc.el(kx + 9, HOR + 2, 11, 3, SCHADUW)
        sc.d.append(f'<rect x="{kx}" y="{HOR - 30}" width="19" height="30" rx="3" fill="{kk}"/><rect x="{kx - 1.5}" y="{HOR - 33}" width="22" height="6" rx="2" fill="{kk}"/>')
    sc.fietsenrek(700, 4)
    sc.persoon(650, HOR + 24, jas="#7A8B9C", huid=3, haar="#1E1710", lopend=True)
    sc.d.append(f'<path d="M646 {HOR + 2} l-4 -14 h9 l3 14 z" fill="#C9705F"/>')   # boodschappentas
    sc.boom(60, 1.0, 1); sc.boom(438, .85, 0); sc.boom(925, 1.05, 2)
    sc.heg(548, 120); sc.heg(760, 130)
    sc.lantaarn(430); sc.lantaarn(870)
    sc.weg(zebra=560)
    sc.fietser(760, WEG_Y + 132, "#3F7A52", huid=1)
    return sc.svg()


def overheid():
    sc = _basis("Tekening van een gemeentehuis met klokkentoren, Nederlandse vlag en een entree met paslezer", tempo=6.8)
    # moderne glazen vleugel links
    gy = sc.pand(120, 250, 190, "url(#glastoren)", schaduwzijde=False)
    for j in range(4):
        sc.r(120, gy + 12 + j * 46, 250, 3, "#F2F6FA")
    for i in range(7):
        sc.r(126 + i * 35, gy + 6, 1.6, 184, "#E4EDF5", 0, 'opacity=".7"')
    # klassiek middendeel in zandsteen met klokkentoren
    bx, bw, bh = 400, 280, 240; by = sc.pand(bx, bw, bh, "url(#zand)", dak="#7A6A52")
    sc.r(bx + bw - 36, by, 36, bh, "#D8CCB4")
    sc.ramen(bx + 26, by + 30, 4, 1, 30, 40, 60, 62, kader="#FFFFFF")
    sc.ramen(bx + 26, by + 92, 1, 1, 30, 40, kader="#FFFFFF")         # rij 2 alleen de buitenste ramen: het midden is voor naam en luifel
    sc.ramen(bx + 206, by + 92, 1, 1, 30, 40, kader="#FFFFFF")
    for i in range(4):                                               # sluitstenen boven de ramen
        sc.p(f"M{bx + 22 + i * 60} {by + 28} h38 l-19 -10 z", "#D8CCB4")
    sc.tekst(bx + bw / 2, by + 112, "GEMEENTEHUIS", 12, "#6B5B41", 3)
    # toren met klok en vlag
    tx = bx + bw / 2 - 30
    sc.r(tx, by - 84, 60, 84, "url(#zand)"); sc.r(tx + 44, by - 84, 16, 84, "#D8CCB4")
    sc.p(f"M{tx - 6} {by - 84} h72 l-36 -30 z", "#7A6A52")
    sc.c(tx + 30, by - 46, 17, "#fff", 'stroke="#7A6A52" stroke-width="3"')
    sc.d.append(f'<line x1="{tx + 30}" y1="{by - 46}" x2="{tx + 30}" y2="{by - 57}" stroke="#37536F" stroke-width="2.5" stroke-linecap="round" class="sb-wijzer"/>'
                f'<line x1="{tx + 30}" y1="{by - 46}" x2="{tx + 38}" y2="{by - 46}" stroke="#37536F" stroke-width="2.5" stroke-linecap="round"/>')
    sc.vlag(tx + 33, by - 114, 46)
    # entree met bordes en paslezer in het middendeel
    sc.p(f"M{bx + 92} {HOR} h96 l-8 -10 h-80 z", "#D8CCB4")
    sc.entree(bx + 96, 88, 92, luifel=False, huid=1, jas="#C9705F")
    sc.p(f"M{bx + 88} {by + 130} h104 l-8 -12 h-88 z", "#7A6A52")     # luifeltje boven de deur
    # lage vleugel rechts
    ry = sc.pand(740, 180, 150)
    sc.glasband(752, ry + 22, 156); sc.glasband(752, ry + 74, 156)
    # amsterdammertjes en fietsen
    for px in range(320, 600, 48):
        sc.el(px, HOR + 30, 4, 1.6, SCHADUW)
        sc.d.append(f'<rect x="{px - 3}" y="{HOR + 6}" width="6" height="24" rx="3" fill="#8B2D2D"/><circle cx="{px}" cy="{HOR + 6}" r="3" fill="#8B2D2D"/>')
    sc.fietsenrek(238, 4)
    sc.persoon(330, HOR + 26, jas="#5B4A68", huid=0, lopend=True)
    sc.d.append(f'<rect x="336" y="{HOR - 12}" width="11" height="14" rx="1.5" fill="#C9B78A"/>')   # dossiermap
    sc.boom(80, 1.0, 2); sc.boom(700, .9, 0); sc.boom(950, 1.05, 1)
    sc.heg(126, 110)
    sc.lantaarn(300); sc.lantaarn(690)
    sc.weg(zebra=430)
    return sc.svg()


def onderwijs():
    sc = _basis("Tekening van een basisschool met schoolplein, fietsenrek en een entree met paslezer", "dorp", tempo=1.7)
    # hoofdgebouw: twee lagen baksteen met witte bovenrand
    bx, bw, bh = 330, 360, 190; by = sc.pand(bx, bw, bh, "url(#baksteen)", dak="#5A4038")
    sc.r(bx + bw - 40, by, 40, bh, BAKSTEEN_D)
    sc.r(bx, by, bw, 34, "url(#gevel)")                               # witte band met naam
    sc.tekst(bx + bw / 2, by + 22, "BS&#160;DE&#160;REGENBOOG", 13, NAVY, 2)
    for i, kl in enumerate(("#D8342B", "#E9B93A", "#3DBE7A", "#2B5BA6", "#8A5BA6")):
        sc.r(bx + bw / 2 - 57 + i * 24, by + 28, 16, 5, kl, 2)        # regenboogbalkje
    sc.ramen(bx + 22, by + 52, 7, 1, 36, 30, 46, kader=KOZIJN)
    sc.ramen(bx + 22, by + 114, 3, 1, 36, 30, 46, kader=KOZIJN)       # rij 2 niet achter de entree door
    sc.ramen(bx + 252, by + 114, 2, 1, 36, 30, 46, kader=KOZIJN)
    # kindertekeningen achter een paar ramen
    for wx, wy, kl in ((bx + 26, by + 118, "#E9B93A"), (bx + 118, by + 56, "#3DBE7A"), (bx + 252, by + 118, "#D8342B"), (bx + 302, by + 56, "#8A5BA6")):
        sc.r(wx + 6, wy + 8, 10, 12, kl, 1, 'opacity=".85"'); sc.c(wx + 24, wy + 12, 4, kl, 'opacity=".7"')
    sc.entree(bx + 136, 88, 86, luifel=True, huid=0, jas="#3F7A52")
    # gymzaaltje rechts
    gy = sc.pand(760, 170, 120, "url(#gevel)", dak="#5A4038", schaduwzijde=False)
    sc.glasband(772, gy + 18, 146, 20)
    sc.r(772, gy + 58, 146, 44, "#B9C7D6", 3)
    sc.tekst(845, gy + 50, "GYMZAAL", 8.5, "#6B7C8C", 2)
    # schoolplein links met hek, hinkelpad en kinderen
    sc.r(60, HOR + 8, 250, 26, "#E0D6C8", 3)
    hek = "".join(f'<path d="M{70 + i * 16} {HOR + 8} v-26" />' for i in range(14))
    sc.d.append(f'<g stroke="#3F7A52" stroke-width="2" fill="none">{hek}<path d="M62 {HOR - 18} h232 M62 {HOR - 4} h232"/></g>')   # opening rechts, in lijn met het zebrapad
    for i in range(5):                                                # hinkelpad
        sc.r(120 + (i % 2) * 0 + i * 17, HOR + 14, 14, 12, "none", 1, 'stroke="#fff" stroke-width="1.6"')
    sc.kind(230, HOR + 30, "#E9B93A", huid=2); sc.kind(258, HOR + 30, "#2B5BA6", huid=0)
    sc.persoon(96, HOR + 28, jas="#8A5BA6", huid=1, lopend=False)     # ouder bij het hek
    sc.fietsenrek(600, 6)
    sc.boom(40, .95, 1); sc.boom(330, .8, 0, anim=False); sc.boom(730, .85, 2); sc.boom(960, 1.0, 0)
    sc.weg(zebra=300)
    # ouder met bakfiets rijdt voorbij
    bak = (f'<ellipse cx="30" cy="18" rx="52" ry="5" fill="{SCHADUW_D}"/>'
           '<circle cx="-22" cy="8" r="12" fill="none" stroke="#3B4650" stroke-width="2.5"/><circle cx="34" cy="8" r="13" fill="none" stroke="#3B4650" stroke-width="2.5"/>'
           '<path d="M-24 -14 h44 q4 0 4 4 v14 h-48 q-4 0 -4 -4 v-10 q0 -4 4 -4 z" fill="#3F7A52"/>'
           '<path d="M24 8 L30 -10 h6 M34 8 L28 -10 M30 -10 l-2 -6 h-5" stroke="#2B3A4A" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
           f'<circle cx="-8" cy="-20" r="4.5" fill="{HUID[1]}"/><rect x="-12" y="-16" width="9" height="10" rx="3" fill="#D8342B"/>'
           f'<path d="M30 -22 q4 -10 12 -9 l3 8 -7 10 h-4 z" fill="#37536F"/><circle cx="44" cy="-34" r="5.5" fill="{HUID[0]}"/>'
           '<path d="M38.5 -35.5 a5.5 5.5 0 0 1 11 0 l-1.5 1.5 a4 4 0 0 0 -8 0 z" fill="#6B4A2F"/>')
    sc._plaats(bak, 0, WEG_Y + 42, True, 21, 0, True)
    return sc.svg()


def vve():
    sc = _basis("Tekening van een appartementengebouw van een VvE met balkons, intercom en paslezer bij de entree", tempo=5.1)
    # appartementenblok met balkonraster
    bx, bw, bh = 280, 340, 300; by = sc.pand(bx, bw, bh, "url(#gevel)", dak="#3A4652")
    sc.r(bx + bw - 40, by, 40, bh, GEVEL3)
    for j in range(4):
        wy = by + 24 + j * 56
        for i in range(3):
            if j == 3 and i == 1:                                     # het middelste balkon onderin valt achter entree en luifel
                continue
            wx = bx + 24 + i * 104
            sc.r(wx, wy, 76, 34, GLAS, 2); sc.r(wx, wy, 76, 10, GLAS_L, 2)
            sc.r(wx + 37, wy, 2, 34, KOZIJN)
            sc.r(wx - 5, wy + 34, 86, 5, "#C9D3DE", 1)                # balkonvloer
            sc.d.append(f'<rect x="{wx - 5}" y="{wy + 16}" width="86" height="20" fill="#BFD9F2" opacity=".45"/>'
                        f'<rect x="{wx - 5}" y="{wy + 15}" width="86" height="2.5" fill="#8595A6"/>')
            if (i + j) % 3 == 0:                                      # plantje op het balkon
                sc.c(wx + 66, wy + 22, 6, GROEN_B[(i + j) % 3]); sc.r(wx + 63, wy + 27, 6, 7, "#B0714F", 1)
            if (i + j) % 3 == 1:
                sc.d.append(f'<path d="M{wx + 10} {wy + 30} l6 -14 l6 14 z" fill="#E9B93A"/><rect x="{wx + 15}" y="{wy + 30}" width="2" height="4" fill="#8595A6"/>')  # parasolletje
    # penthouselaag
    sc.r(bx + 40, by - 40, 200, 40, "url(#gevel)"); sc.r(bx + 40, by - 40, 200, 5, "#3A4652")
    sc.glasband(bx + 52, by - 32, 176, 22)
    sc.tekst(bx + 50, by + 268, "PARKZICHT", 9.5, "#54636F", 2)
    # entree met intercom
    sc.entree(bx + 116, 84, 88, luifel=True, huid=1, jas="#5B4A68")
    sc.d.append(f'<rect x="{bx + 98}" y="{HOR - 64}" width="13" height="30" rx="2" fill="#EDF1F6" stroke="#8595A6" stroke-width="1.2"/>' +
                "".join(f'<circle cx="{bx + 104.5}" cy="{HOR - 58 + i * 5.2}" r="1.7" fill="#8595A6"/>' for i in range(5)))
    # buurpand links (lager, baksteen)
    cy = sc.pand(90, 160, 170, "url(#baksteen)", dak="#5A4038", schaduwzijde=False)
    sc.ramen(104, cy + 20, 2, 2, 34, 28, 56, 60, kader=KOZIJN)
    sc.r(104, cy + 136, 122, 4, "#D3DCE6")
    # parkje rechts
    sc.heg(680, 150); sc.heg(860, 110)
    sc.boom(720, 1.05, 0); sc.boom(820, .8, 1); sc.boom(930, 1.1, 2); sc.boom(50, .9, 2)
    sc.d.append(f'<rect x="762" y="{HOR + 12}" width="44" height="5" rx="2" fill="#7A6250"/><rect x="766" y="{HOR + 17}" width="5" height="12" fill="#5F4C3D"/><rect x="797" y="{HOR + 17}" width="5" height="12" fill="#5F4C3D"/>')  # bankje
    sc.persoon(870, HOR + 26, jas="#C9705F", huid=3, haar="#1E1710", lopend=True)
    sc.d.append(f'<g><ellipse cx="898" cy="{HOR + 26}" rx="9" ry="5.5" fill="#8A6B4F"/><circle cx="906" cy="{HOR + 20}" r="4" fill="#8A6B4F"/>'
                f'<path d="M909 {HOR + 17} l4 -3 M890 {HOR + 30} l-3 4 M898 {HOR + 31} l0 4 M905 {HOR + 29} l3 4" stroke="#8A6B4F" stroke-width="2" stroke-linecap="round"/>'
                f'<path d="M884 {HOR - 14} q8 18 13 30" stroke="#54636F" stroke-width="1.4" fill="none"/></g>')   # hondje aan de lijn
    sc.lantaarn(268); sc.lantaarn(660)
    sc.weg()
    sc.fietser(560, WEG_Y + 132, "#37536F", huid=0)
    return sc.svg()


def kantoren():
    sc = _basis("Tekening van een kantoorgebouw met glazen toren, laadpaal en een entree met paslezer", tempo=8.5)
    # glazen toren
    bx, bw, bh = 300, 280, 310; by = sc.pand(bx, bw, bh, "url(#glastoren)")
    for j in range(7):
        sc.r(bx, by + 10 + j * 44, bw, 3.5, "#F2F6FA")                # verdiepingsranden
    for i in range(9):
        sc.r(bx + 8 + i * 33, by + 4, 1.6, bh - 8, "#E4EDF5", 0, 'opacity=".65"')
    sc.r(bx + 104, by - 6, 72, bh + 6, "url(#gevel)")                 # witte kern
    sc.d.append(f'<rect x="{bx + 104}" y="{by - 6}" width="72" height="{bh + 6}" fill="none" stroke="#E1E8F0" stroke-width="1.5"/>')
    sc.tekst(bx + 140, by + 66, "DE&#160;POORT", 13, NAVY, 2)
    sc.dak_leuning(bx + 4, bw - 8, by - 14); sc.dak_installatie(bx + 190, by - 12)
    sc.d.append(f'<line x1="{bx + 30}" y1="{by - 16}" x2="{bx + 30}" y2="{by - 52}" stroke="#8A9BAD" stroke-width="2.5"/><circle cx="{bx + 30}" cy="{by - 54}" r="3" fill="{ROOD}"/>')
    # laag paviljoen met de entree
    ey = sc.pand(650, 230, 150)
    sc.glasband(662, ey + 18, 206)
    sc.entree(692, 100, 88, luifel=True, bord="ONTVANGST", huid=2, jas="#37536F")
    # laadpaal met elektrische auto voor de deur
    lx = 200
    sc.d.append(f'<ellipse cx="{lx + 5}" cy="{HOR + 34}" rx="7" ry="2.2" fill="{SCHADUW}"/><rect x="{lx}" y="{HOR - 4}" width="11" height="38" rx="2.5" fill="#3F9965"/>'
                f'<rect x="{lx + 2.5}" y="{HOR}" width="6" height="8" rx="1" fill="#DFF4E8"/><path d="M{lx + 11} {HOR + 6} q9 0 9 7 q0 7 -7 7 q-6 0 -6 -5" stroke="#2B3A4A" stroke-width="2" fill="none"/>')
    # zakelijke voetgangers
    sc.persoon(232, HOR + 26, jas="#2B3A4A", huid=0, lopend=True)
    sc.d.append(f'<rect x="238" y="{HOR + 6}" width="12" height="9" rx="1.5" fill="#5A4636"/>')       # aktetas
    sc.persoon(630, HOR + 26, jas="#7A8B9C", huid=3, haar="#1E1710")
    sc.boom(70, 1.05, 2); sc.boom(262, .8, 0); sc.boom(915, 1.0, 1)
    sc.heg(90, 100); sc.heg(880, 100)
    sc.lantaarn(126); sc.lantaarn(600)
    sc.weg(zebra=344)
    sc.fietser(420, WEG_Y + 132, "#3F7A52", huid=1)
    return sc.svg()


def industrie():
    sc = _basis("Tekening van een bedrijfshal met roldeur, silo's, heftruck en een kantoor met paslezer", "industrie", tempo=2.6)
    # productiehal met golfplaatprofiel
    bx, bw, bh = 240, 420, 210; by = sc.pand(bx, bw, bh, "url(#gevel)", dak="#54616E")
    sc.p(f"M{bx - 8} {by - 12} h{bw + 16} l-14 -26 h-{bw - 12} z", "#8B99A7")     # flauw hellend dak
    for i in range(int(bw / 22)):
        sc.r(bx + 8 + i * 22, by + 8, 2, bh - 16, "#DDE4EC")
    sc.glasband(bx + 20, by + 22, bw - 40, 18)
    sc.tekst(bx + bw / 2, by + 70, "HAL&#160;3", 15, "#54616E", 5)
    # roldeur die opengaat, met heftruck ernaast
    sc.r(bx + 60, HOR - 110, 96, 110, "#37475A", 2)
    sc.d.append(f'<g class="sb-roldeur"><rect x="{bx + 63}" y="{HOR - 107}" width="90" height="107" fill="#B9C7D6"/>' +
                "".join(f'<rect x="{bx + 63}" y="{HOR - 103 + i * 9}" width="90" height="3" fill="#CBD7E3"/>' for i in range(11)) + "</g>")
    sc.p(f"M{bx + 50} {HOR - 110} h116 l8 -14 h-132 z", "#54616E")
    # heftruck met pallet
    hx = bx + 190
    sc.el(hx + 26, HOR + 3, 40, 5, SCHADUW)
    sc.d.append(f'<g transform="translate({hx} {HOR})"><rect x="0" y="-34" width="34" height="24" rx="3" fill="#E9B93A"/>'
                '<path d="M6 -34 v-16 h20 v16" stroke="#54616E" stroke-width="3" fill="none"/>'
                '<rect x="0" y="-12" width="40" height="8" rx="2" fill="#54616E"/>'
                '<rect x="44" y="-40" width="4" height="40" fill="#54616E"/><rect x="48" y="-4" width="18" height="3" fill="#54616E"/>'
                '<rect x="48" y="-16" width="17" height="11" fill="#B0714F"/><rect x="48" y="-18" width="17" height="3" fill="#8A5A3C"/>'
                + sc._wiel(8, -2, 7) + sc._wiel(34, -2, 7) + "</g>")
    # schoorsteen met rook en silo's
    sx = bx + 28
    sc.r(sx, by - 96, 16, 96, "#8B99A7"); sc.r(sx, by - 96, 16, 8, "#6E7C8A")
    for i in range(3):
        sc.d.append(f'<g transform="translate({sx + 8} {by - 100})"><circle r="9" fill="#DFE8F1" class="sb-rook sb-rook-{i}"/></g>')
    for i, dx in enumerate((0, 46)):
        sc.el(730 + dx + 19, HOR + 3, 24, 4, SCHADUW)
        sc.d.append(f'<rect x="{730 + dx}" y="{HOR - 150}" width="38" height="150" rx="10" fill="#C3CEDA"/>'
                    f'<rect x="{730 + dx}" y="{HOR - 150}" width="12" height="150" rx="6" fill="#D7DFE9"/>'
                    f'<path d="M{730 + dx} {HOR - 142} a19 12 0 0 1 38 0 v6 h-38 z" fill="#AAB8C6"/>'
                    f'<path d="M{730 + dx + 4} {HOR - 40} h30 M{730 + dx + 4} {HOR - 90} h30" stroke="#9AA9B8" stroke-width="2"/>')
    # kantoortje met de entree
    ky = sc.pand(830, 150, 128, schaduwzijde=False)
    sc.glasband(842, ky + 14, 126, 20)
    sc.entree(856, 74, 70, luifel=True, bord=None, huid=1, jas="#E9B93A")
    # hek met poort
    sc.d.append(f'<g stroke="#8595A6" stroke-width="2" fill="none">' +
                "".join(f'<path d="M{x} {HOR + 34} v-24"/>' for x in range(40, 210, 14)) +
                f'<path d="M38 {HOR + 12} H210 M38 {HOR + 26} H210"/></g>')
    sc.d.append(f'<rect x="206" y="{HOR + 4}" width="5" height="32" fill="#54616E"/>')
    sc.d.append(f'<g stroke="#8595A6" stroke-width="2" fill="none">' +
                "".join(f'<path d="M{x} {HOR + 34} v-24"/>' for x in range(968, 1000, 14)) +
                f'<path d="M966 {HOR + 12} H1000 M966 {HOR + 26} H1000"/></g>')   # vervolg van het hek rechts
    sc.lantaarn(226); sc.lantaarn(700)
    sc.weg(streep=True)
    return sc.svg()


def retail():
    sc = _basis("Tekening van een winkelstraat met luifels, winkelend publiek en een personeelsingang met paslezer", tempo=7.7)
    # winkelblok: drie zaken met woningen erboven
    bx, bw, bh = 210, 480, 210; by = sc.pand(bx, bw, bh, "url(#baksteen)", dak="#5A4038")
    sc.r(bx + bw - 38, by, 38, bh, BAKSTEEN_D)
    sc.ramen(bx + 24, by + 22, 5, 1, 34, 28, 92, 0, kader=KOZIJN)
    sc.r(bx, by + 78, bw, 6, "#EDE5D4")                               # kroonlijst tussen wonen en winkel
    winkels = (("BAKKERIJ", "#E9B93A", "#8A5A3C"), ("MODE", "#8A5BA6", "#54636F"), ("BLOEMEN", "#3F7A52", "#C9705F"))
    for i, (naam, kleur, accent) in enumerate(winkels):
        wx = bx + 12 + i * 156
        sc.r(wx, by + 92, 144, 22, "#F6F8FA", 2); sc.tekst(wx + 72, by + 107, naam, 10.5, accent, 2)
        sc.r(wx + 4, by + 118, 136, bh - 210 + 92, GLAS_D, 2)
        sc.r(wx + 4, by + 118, 136, 14, GLAS)
        # luifel met strepen
        sc.d.append(f'<g><path d="M{wx - 2} {by + 114} h148 l10 22 h-168 z" fill="{kleur}"/>' +
                    "".join(f'<path d="M{wx + 4 + k * 21} {by + 114} l{9} 22 h-10 l-9 -22 z" fill="#fff" opacity=".55"/>' for k in range(7)) +
                    f'<path d="M{wx - 12} {by + 136} h168 v5 h-168 z" fill="{kleur}" opacity=".8"/></g>')
        # etalage-inhoud
        if i == 0:
            for k in range(3):
                sc.d.append(f'<ellipse cx="{wx + 30 + k * 24}" cy="{by + 168}" rx="10" ry="6" fill="#D9A05B"/><ellipse cx="{wx + 30 + k * 24}" cy="{by + 165}" rx="10" ry="5" fill="#E8BC80"/>')
            sc.r(wx + 14, by + 176, 116, 5, "#B0714F", 2)
        if i == 1:
            for k, kl in enumerate(("#C9705F", "#37536F")):
                mx = wx + 44 + k * 52
                sc.d.append(f'<rect x="{mx - 9}" y="{by + 138}" width="18" height="30" rx="7" fill="{kl}"/><circle cx="{mx}" cy="{by + 133}" r="5" fill="#D8DFE7"/><rect x="{mx - 1.5}" y="{by + 168}" width="3" height="14" fill="#8595A6"/>')
            sc.r(wx + 14, by + 182, 116, 5, "#B0714F", 2)             # vloertje onder de paspoppen
        if i == 2:
            for k, kl in enumerate(("#E06A8A", "#E9B93A", "#8A5BA6", "#D8342B")):
                fx = wx + 26 + k * 30
                sc.d.append(f'<circle cx="{fx}" cy="{by + 152}" r="6" fill="{kl}"/><circle cx="{fx - 6}" cy="{by + 156}" r="4.5" fill="{kl}" opacity=".8"/><circle cx="{fx + 6}" cy="{by + 156}" r="4.5" fill="{kl}" opacity=".8"/>'
                            f'<path d="M{fx - 4} {by + 160} h8 l3 20 h-14 z" fill="#B9C7D6"/>')
            sc.r(wx + 14, by + 180, 116, 5, "#B0714F", 2)             # schap onder de vazen
    # personeelsingang met paslezer, rechts naast het blok
    py2 = sc.pand(720, 150, 150, schaduwzijde=False)
    sc.ramen(734, py2 + 18, 2, 1, 34, 26, 60)
    sc.entree(742, 70, 74, luifel=False, bord=None, huid=0, jas="#C9705F")
    sc.tekst(777, HOR - 84, "PERSONEEL", 7.5, "#6B7C8C", 1.5)
    # winkelend publiek
    sc.persoon(160, HOR + 26, jas="#C9705F", huid=1, lopend=True)
    sc.d.append(f'<path d="M154 {HOR + 4} l-3 -13 h8 l2 13 z" fill="#E9B93A"/><path d="M170 {HOR + 4} l-2 -11 h7 l2 11 z" fill="#8A5BA6"/>')
    sc.persoon(560, HOR + 24, jas="#37536F", huid=2, lopend=True)
    sc.kind(583, HOR + 26, "#3DBE7A", huid=2)
    sc.boom(60, 1.0, 0); sc.boom(968, .95, 1)
    sc.lantaarn(196); sc.lantaarn(660); sc.fietsenrek(884, 3)
    sc.weg(zebra=88)
    sc.fietser(600, WEG_Y + 132, NAVY, huid=3)
    return sc.svg()


def verenigingen():
    sc = _basis("Tekening van een sportpark met clubhuis, sporthal, lichtmasten en een entree met paslezer", "groen", tempo=4.3)
    # sporthal met boogdak
    bx, bw, bh = 420, 330, 150; by = sc.pand(bx, bw, bh, "url(#gevel)", dak="#3A4652")
    sc.p(f"M{bx - 8} {by - 12} q{bw / 2 + 8} -74 {bw + 16} 0 z", "#54616E")
    sc.glasband(bx + 20, by + 24, bw - 40, 20)
    sc.tekst(bx + bw / 2, by + 76, "SPORTHAL", 12, "#54616E", 4)
    sc.r(bx + 130, HOR - 64, 70, 64, "#B9C7D6", 2)
    # clubhuis met terras en de entree
    cy = sc.pand(120, 240, 120, dak="#3F7A52")
    sc.glasband(134, cy + 16, 56, 20)
    sc.tekst(172, cy + 74, "SV&#160;OOSTRUM", 10, "#3F7A52", 1.5)
    sc.entree(220, 82, 78, luifel=True, huid=3, jas="#3F7A52")
    sc.d.append(f'<rect x="132" y="{HOR - 44}" width="40" height="44" rx="2" fill="{GLAS_D}"/><rect x="132" y="{HOR - 44}" width="40" height="10" fill="{GLAS}"/>')
    # scorebord
    sc.el(923, HOR + 2, 30, 4, SCHADUW)
    sc.d.append(f'<rect x="880" y="{HOR - 118}" width="86" height="54" rx="4" fill="#1E2833"/><rect x="919" y="{HOR - 64}" width="8" height="64" fill="#54616E"/>'
                f'<text x="923" y="{HOR - 96}" font-family="Arial,sans-serif" font-size="15" font-weight="800" fill="#7ADCA5" text-anchor="middle">2&#160;-&#160;1</text>'
                f'<text x="923" y="{HOR - 74}" font-family="Arial,sans-serif" font-size="8" font-weight="700" letter-spacing="2" fill="#8FA3B8" text-anchor="middle">THUIS&#160;&#160;UIT</text>')
    # lichtmasten met gloed
    for lx in (60, 815):
        sc.el(lx + 4, HOR + 4, 8, 2.5, SCHADUW)
        sc.d.append(f'<path d="M{lx + 2} {HOR} L{lx + 4} {HOR - 160} M{lx + 6} {HOR} L{lx + 4} {HOR - 160}" stroke="#8595A6" stroke-width="2.5"/>'
                    f'<rect x="{lx - 8}" y="{HOR - 174}" width="24" height="14" rx="2" fill="#54616E"/>' +
                    "".join(f'<circle cx="{lx - 2 + i * 8}" cy="{HOR - 167}" r="2.6" fill="#FFF3B0" class="sb-lamp"/>' for i in range(3)))
    # veldje voor de hal met twee spelers
    sc.r(470, HOR + 10, 370, 24, "#7CC496", 4); sc.r(470, HOR + 10, 370, 4, "#93D3AA", 4)
    sc.d.append(f'<rect x="488" y="{HOR - 8}" width="46" height="28" fill="none" stroke="#fff" stroke-width="2.5"/><line x1="488" y1="{HOR + 20}" x2="534" y2="{HOR + 20}" stroke="#fff" stroke-width="2.5"/>')
    sc.persoon(640, HOR + 26, jas="#D8342B", broek="#fff", huid=2, lopend=True)
    sc.persoon(680, HOR + 28, jas="#2B5BA6", broek="#fff", huid=0, lopend=True)
    sc.fietsenrek(370, 5)
    sc.boom(508, .85, 1); sc.boom(860, .95, 0)
    sc.weg()
    sc.fietser(180, WEG_Y + 132, "#D8342B", huid=1)
    return sc.svg()


def hotel():
    sc = _basis("Tekening van een hotel met luifel, vlaggen, bagagekar en een entree met keycardlezer", tempo=0.9)
    # hotelgevel in warm wit met vijf verdiepingen
    bx, bw, bh = 330, 320, 320; by = sc.pand(bx, bw, bh, "url(#zand)", dak="#54432F")
    sc.r(bx + bw - 38, by, 38, bh, "#DFD3BC")
    for j in range(4):
        wy = by + 26 + j * 52
        for i in range(5):
            wx = bx + 24 + i * 58
            sc.r(wx, wy, 32, 34, GLAS, 2, f'stroke="#FFFFFF" stroke-width="3"'); sc.r(wx, wy, 32, 10, GLAS_L, 2)
            sc.r(wx - 3, wy + 34, 38, 4, "#C9B98F", 1)
            if (i + j) % 4 == 1:                                     # openslaand raam met balkonnetje
                sc.d.append(f'<g fill="none" stroke="#8A7A5A" stroke-width="1.5"><path d="M{wx - 3} {wy + 30} h38"/>' +
                            "".join(f'<path d="M{wx + 1 + k * 6} {wy + 18} v12"/>' for k in range(6)) + "</g>")
    sc.r(bx + 58, by + 2, 204, 21, "#FFFFFF", 3, 'opacity=".88"')
    sc.tekst(bx + bw / 2, by + 17, "HOTEL&#160;DE&#160;KROON", 12, "#54432F", 3)
    for i, vx in enumerate((bx + 60, bx + 150, bx + 240)):
        sc.vlag(vx, by - 2, 40, ("#8B2D2D", None, "#37536F")[i] if i != 1 else None)
    # luifel over de entree
    sc.entree(bx + 116, 88, 92, luifel=False, huid=1, jas="#54432F")
    sc.d.append(f'<path d="M{bx + 96} {HOR - 92} h128 l14 -22 h-156 z" fill="#8B2D2D"/>'
                f'<path d="M{bx + 96} {HOR - 92} h128 v6 h-128 z" fill="#6E2222"/>' +
                "".join(f'<path d="M{bx + 100 + i * 18} {HOR - 92} l3 6 h-7 l3 -6 z" fill="#F6E7C8"/>' for i in range(8)) +
                f'<text x="{bx + 160}" y="{HOR - 99}" font-family="Arial,sans-serif" font-size="10" font-weight="800" letter-spacing="4" fill="#F6E7C8" text-anchor="middle">HOTEL</text>')
    # portier en bagagekar
    sc.persoon(bx + 100, HOR + 4, jas="#6E2222", broek="#2B3A4A", huid=2)
    kx = bx + 50
    sc.el(kx + 15, HOR + 6, 18, 3, SCHADUW)
    sc.d.append(f'<g><path d="M{kx} {HOR + 2} v-52 q0 -6 6 -6 h20 q6 0 6 6 v52" stroke="#B08D3E" stroke-width="3" fill="none"/>'
                f'<rect x="{kx - 2}" y="{HOR - 4}" width="36" height="5" rx="2" fill="#B08D3E"/>'
                f'<rect x="{kx + 2}" y="{HOR - 26}" width="13" height="20" rx="2" fill="#8A5A3C"/><rect x="{kx + 16}" y="{HOR - 36}" width="12" height="30" rx="2" fill="#37536F"/>'
                f'<circle cx="{kx + 4}" cy="{HOR + 3}" r="4" fill="#54616E"/><circle cx="{kx + 28}" cy="{HOR + 3}" r="4" fill="#54616E"/></g>')
    # laag restaurantdeel links
    ry = sc.pand(130, 170, 130, dak="#54432F", schaduwzijde=False)
    sc.glasband(142, ry + 20, 146, 24)
    sc.tekst(215, ry + 78, "BRASSERIE", 9, "#8A7A5A", 2)
    for tx in (150, 250):                                             # terras met parasols
        sc.d.append(f'<ellipse cx="{tx + 18}" cy="{HOR + 24}" rx="22" ry="3.5" fill="{SCHADUW}"/>'
                    f'<path d="M{tx - 6} {HOR - 12} q24 -18 48 0 z" fill="#8B2D2D"/><path d="M{tx - 6} {HOR - 12} h48 l-5 4 h-38 z" fill="#6E2222"/>'
                    f'<rect x="{tx + 16.5}" y="{HOR - 12}" width="3" height="30" fill="#8595A6"/>'
                    f'<rect x="{tx + 6}" y="{HOR + 8}" width="24" height="4" rx="2" fill="#7A6250"/><rect x="{tx + 16}" y="{HOR + 12}" width="4" height="10" fill="#5F4C3D"/>')
    sc.boom(80, 1.0, 1); sc.boom(700, .9, 0); sc.boom(950, 1.05, 2)
    sc.heg(676, 56); sc.heg(840, 100)
    sc.lantaarn(310); sc.lantaarn(662)
    sc.weg(zebra=740)
    sc.persoon(756, HOR + 26, jas="#8A5BA6", huid=0, lopend=True)
    sc.d.append(f'<rect x="763" y="{HOR + 8}" width="14" height="18" rx="2" fill="#C9705F"/><path d="M766 {HOR + 8} v-6 h8 v6" stroke="#8A4A3C" stroke-width="2" fill="none"/>'
                f'<circle cx="766" cy="{HOR + 28}" r="2" fill="#54616E"/><circle cx="774" cy="{HOR + 28}" r="2" fill="#54616E"/>')  # rolkoffer op de grond
    return sc.svg()


def recreatie():
    sc = _basis("Tekening van een vakantiepark met receptie, chalets, slagboom en een paslezer bij de entree", "groen", tempo=5.9)
    # receptie met rieten kap
    bx, bw, bh = 300, 250, 130; by = sc.pand(bx, bw, bh, dak="#7A6250")
    sc.p(f"M{bx - 16} {by - 12} h{bw + 32} l-52 -58 h-{bw - 72} z", "#8A6B4F")
    sc.p(f"M{bx - 16} {by - 12} h{bw + 32} l-8 -10 h-{bw + 16} z", "#755539")
    sc.tekst(bx + bw / 2, by - 30, "DE&#160;VELUWEHOF", 12, "#F8F1E0", 2)
    sc.glasband(bx + 16, by + 20, 100, 22)
    sc.tekst(bx + 158, by + 36, "RECEPTIE", 9, "#755539", 2)
    sc.entree(bx + 118, 82, 80, luifel=False, huid=0, jas="#3F7A52")
    # chalets
    for i, cx in enumerate((640, 800)):
        ch = 96; cyy = HOR - ch
        sc.el(cx + 55, HOR + 3, 62, 5, SCHADUW)
        sc.r(cx, cyy, 110, ch, "#8A6B4F", 2); sc.r(cx, cyy, 110, 8, "#755539")
        sc.p(f"M{cx - 10} {cyy} h130 l-65 -44 z", "#5F4C3D")
        sc.r(cx + 14, cyy + 26, 30, 26, GLAS, 2, 'stroke="#F4E9D8" stroke-width="2.5"')
        sc.r(cx + 62, cyy + 22, 24, ch - 22, "#5F4C3D", 2); sc.c(cx + 82, cyy + 58, 2, "#C9B98F")
        sc.r(cx - 4, HOR - 4, 118, 6, "#B0917A", 2)
        if i == 0:
            sc.d.append(f'<circle cx="{cx - 12}" cy="{HOR - 10}" r="10" fill="#E8734A"/><circle cx="{cx - 12}" cy="{HOR - 10}" r="5" fill="#F6F8FA"/>')  # zwemband tegen het chalet
    # slagboom bij de inrit
    sx = 130
    sc.el(sx + 6, HOR + 34, 9, 2.5, SCHADUW)
    # de slagboom blijft dicht: er rijdt niets meer het park op, dus opengaan zou nergens op slaan
    sc.d.append(f'<rect x="{sx}" y="{HOR - 6}" width="13" height="40" rx="2" fill="#54616E"/><circle cx="{sx + 6.5}" cy="{HOR - 1}" r="2.5" fill="#D9362B"/>'
                f'<g transform="translate({sx + 11} {HOR + 2})"><rect x="0" y="-4" width="96" height="8" rx="4" fill="#F6F8FA" stroke="#D8342B" stroke-width="1.5"/>' +
                "".join(f'<rect x="{8 + i * 24}" y="-4" width="12" height="8" fill="#D8342B"/>' for i in range(4)) + "</g>")
    sc.r(sx + 100, HOR + 6, 4, 28, "#8595A6", 1)                      # steunpaaltje onder de arm
    sc.r(sx - 60, HOR + 14, 300, 18, "#C9BCA4", 3)                    # zandpad de camping op
    # speelveldje met vlaggenlijn
    # vlaggenlijn hoog gespannen tussen het receptiedak en het eerste chalet
    sc.d.append(f'<path d="M560 296 q46 26 92 2" stroke="#8595A6" stroke-width="1.6" fill="none"/>' +
                "".join(f'<g transform="translate({570 + i * 13} {299 + (3, 7, 10, 12, 12, 10, 6)[i]})"><path d="M0 0 l10 2.5 l-10 4.5 z" fill="{("#D8342B", "#E9B93A", "#3DBE7A", "#2B5BA6")[i % 4]}" class="sb-vlag"/></g>' for i in range(7)))
    sc.kind(560, HOR + 28, "#E9B93A", huid=1); sc.kind(590, HOR + 26, "#2B5BA6", huid=3)
    sc.boom(50, 1.1, 2); sc.boom(255, .9, 1); sc.boom(475, .85, 0); sc.boom(770, .9, 2); sc.boom(945, 1.15, 1)
    sc.heg(390, 80)
    sc.weg(streep=False)
    sc.fietser(800, WEG_Y + 136, "#E9B93A", huid=0)
    return sc.svg()


def anders():
    sc = _basis("Tekening van een straat met verschillende bedrijfspanden en een entree met paslezer", tempo=3.0)
    # kantoorvilla
    by = sc.pand(140, 200, 190, dak="#3A4652")
    sc.ramen(158, by + 22, 3, 2, 34, 30, 60, 58, kader="#E2E8EF")
    sc.tekst(240, by + 152, "KANTOOR", 9, "#6B7C8C", 3)
    # bedrijfspand met de entree
    bx, bw, bh = 420, 300, 240; my = sc.pand(bx, bw, bh)
    for rij in range(3):
        sc.glasband(bx + 16, my + 24 + rij * 46, bw - 32)
    sc.r(bx + 108, my - 6, 66, bh + 6, "url(#gevel)")
    sc.d.append(f'<rect x="{bx + 108}" y="{my - 6}" width="66" height="{bh + 6}" fill="none" stroke="#E1E8F0" stroke-width="1.5"/>')
    sc.tekst(bx + 141, my + 64, "ENTREE", 10, NAVY, 3)
    sc.entree(bx + 96, 90, 88, luifel=True, huid=2, jas=BLAUW)
    sc.dak_leuning(bx + 4, bw - 8, my - 14)
    # werkplaats met kleine roldeur
    wy = sc.pand(790, 160, 130, dak="#5A4038", schaduwzijde=False)
    sc.glasband(802, wy + 18, 136, 18)
    sc.r(818, HOR - 74, 74, 74, "#37475A", 2)
    sc.d.append(f'<g class="sb-roldeur"><rect x="{821}" y="{HOR - 71}" width="68" height="71" fill="#B9C7D6"/>' +
                "".join(f'<rect x="821" y="{HOR - 68 + i * 9}" width="68" height="3" fill="#CBD7E3"/>' for i in range(8)) + "</g>")
    sc.tekst(870, wy + 52, "WERKPLAATS", 8, "#6B7C8C", 1.5)
    sc.heg(120, 110); sc.heg(664, 78)                                 # heggen vóór de personen, anders staan die in het groen
    sc.persoon(770, HOR + 26, jas="#E9B93A", huid=1, lopend=True)
    sc.persoon(180, HOR + 28, jas="#5B4A68", huid=3)
    sc.boom(60, 1.0, 0); sc.boom(390, .85, 2); sc.boom(950, 1.0, 1)
    sc.lantaarn(360); sc.lantaarn(740)
    sc.weg(zebra=200)
    sc.fietser(300, WEG_Y + 132, "#37536F", huid=0)
    return sc.svg()


SECTOREN = {
    "zorg": zorg,
    "woningcorporatie": woningcorporatie,  # was: _nog_niet("Tekening van een woongebouw"),
    "overheid": overheid,  # was: _nog_niet("Tekening van een gemeentehuis"),
    "onderwijs": onderwijs,  # was: _nog_niet("Tekening van een school"),
    "vve": vve,  # was: _nog_niet("Tekening van een appartementengebouw"),
    "kantoren": kantoren,  # was: _nog_niet("Tekening van een kantoorgebouw"),
    "industrie": industrie,  # was: _nog_niet("Tekening van een bedrijfshal"),
    "retail": retail,  # was: _nog_niet("Tekening van een winkelstraat"),
    "verenigingen": verenigingen,  # was: _nog_niet("Tekening van een sportpark"),
    "hotel": hotel,  # was: _nog_niet("Tekening van een hotel"),
    "recreatie": recreatie,  # was: _nog_niet("Tekening van een vakantiepark"),
    "anders": anders,  # was: _nog_niet("Tekening van een straat met verschillende panden"),
}
