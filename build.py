#!/usr/bin/env python3
"""westendorptoegang.nl — statische site-generator.

Werkwijze: feiten uit INPUT.md staan in het CONFIG-blok hieronder; pagina's staan als data in content/;
`python build.py` schrijft alles naar dist/. HTML in dist/ nooit met de hand bewerken.

Regels (CLAUDE.md §1): een veld [[INVULLEN: ...]] blijft letterlijk staan tot Lars het invult.
check.py faalt zolang zo'n veld in dist/ voorkomt; die pagina gaat niet live.
"""
import sys, re, json, html, shutil, hashlib, pathlib, datetime, importlib
import isometrie   # isometrische illustraties in code (richting Salto, Lars 22-09-2026)
sys.dont_write_bytecode = True
# Contentmodules doen `from build import *`; zo krijgen ze deze draaiende module, niet een tweede kopie.
sys.modules.setdefault("build", sys.modules[__name__])

# ============================================================
# CONFIG — alle feiten uit INPUT.md. Nergens anders hardcoded.
# ============================================================
def INV(wat): return f"[[INVULLEN: {wat}]]"

SITE          = "https://westendorptoegang.nl"
NAAM          = "Westendorp Toegangscontrole"                       # INPUT §A1, overal identiek
RECHTSPERSOON = "Westendorp Groep VOF"                              # alleen schema, footer, privacy
KVK           = "91885124"                                          # INPUT §A1 (aanname, controleren)
VESTIGINGSNR  = ""                                                  # INPUT §A1: voorlopig weglaten (Lars, 20-09-2026)
BTW           = "NL865804990B01"                                    # INPUT §A1 (Lars, 20-09-2026)
MOEDER        = "Westendorp Slotenspecialist"                       # zusterbedrijf; alleen genoemd op /over-ons/ (Lars, 20-09-2026)
MOEDER_URL    = "https://www.westendorpslotenspecialist.nl/"
MOEDER_SINDS  = "1985"                                              # INPUT §C3: Twents familiebedrijf sinds 1985 (Lars, 20-09-2026)
# Lars, chat 20-09-2026: het woord "slotenmaker" komt op deze site niet voor (check.py bewaakt dat); hoofdmerk is EVVA,
# Salto plaatsen wij niet, maar onderhouden en breiden wij wel uit; klanten komen niet langs, wij komen op locatie.
# Westendorp Toegangscontrole is onderdeel van Westendorp Groep VOF (niet van Slotenspecialist). Particulieren en
# autosleutels worden nergens genoemd, behalve één zin op /over-ons/ over de verhouding tot het zusterbedrijf.

STRAAT        = "Wesseler-Nering 33"                                # INPUT §A2 (Lars, 20-09-2026)
POSTCODE      = "7544 JC"                                           # INPUT §A2
KVK_ADRES     = "Wesseler-Nering 32, 7544 JC Enschede"              # inschrijfadres KvK van de VOF (Lars, 21-09-2026); vestiging 33 mag gebruikt worden
PLAATS        = "Enschede"
REGIO         = "Overijssel"
LAT, LON      = 52.192259, 6.882859                                 # INPUT §A2 (Lars, 20-09-2026)
TEL_TONEN     = "053 478 42 45"                                     # INPUT §A2, Lars chat 20-09-2026 (zelfde nummer als de hoofdsite)
TEL_LINK      = "+31534784245"
MAIL          = "info@westendorpgroep.nl"                           # INPUT §A2 (Lars, 20-09-2026; in kleine letters geschreven)
OPENING_TEKST = "dag en nacht, 7 dagen per week voor storingen; kantoor maandag tot en met vrijdag 08:00–17:00"   # Bedrijfsprofiel staat op 24/7 (Lars, 20-09-2026)
KANTOORTIJD   = "maandag tot en met vrijdag 08:00–17:00"            # aanname INPUT §A2
OPENING_SCHEMA = [(d, "00:00", "23:59") for d in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")]   # gelijk aan het Bedrijfsprofiel: 24/7
STORING_BUITEN_KANTOORTIJD = "dag en nacht bereikbaar, 7 dagen per week"   # INPUT §A2 (Lars, 20-09-2026)
BEZOEKADRES   = "alleen op afspraak"                                # INPUT §A2 (Lars, 20-09-2026); inventarisatie altijd op locatie bij de klant

GOOGLE_PROFIEL = "https://share.google/lRJgjHKFPBrgrWkop"           # INPUT §A3: deellink Google Bedrijfsprofiel (Lars, 21-09-2026)
LINKEDIN       = "https://www.linkedin.com/company/westendorp-toegangscontrole/"   # INPUT §A3 (Lars, 21-09-2026)
ANDERE_PROFIELEN = []                                                # INPUT §A3 optioneel

# Aanbod (INPUT §B1). Diensten zonder ja/nee staan als placeholder in de tekst waar ze genoemd worden.
DIENSTEN_ONBEVESTIGD = {
    "wandlezers": "ja",                                   # Lars, 21-09-2026
    "beheer": "beide",                                    # wij doen het of leren het de klant
    "onderhoud": "ja",
    "storingsdienst": "ja",
    "overnemen": "ja",
    "koppelingen": "in overleg",
}

# Werkgebied (INPUT §B3): plaats, regio, rijtijd in minuten (None = placeholder), eigen pagina (pad of None).
WERKGEBIED = [
    ("Enschede",   "Twente",    5,    None),
    ("Hengelo",    "Twente",    None, None),
    ("Almelo",     "Twente",    None, None),
    ("Oldenzaal",  "Twente",    None, None),
    ("Haaksbergen","Twente",    None, None),
    ("Borne",      "Twente",    None, None),
    ("Deventer",   "Salland",   None, None),
    ("Zwolle",     "Vechtdal",  None, None),
    ("Zutphen",    "Achterhoek",None, None),
    ("Doetinchem", "Achterhoek",None, None),
    ("Apeldoorn",  "Veluwe",    None, None),
]
WERKGEBIED_REGEL = "tot 60 minuten rijden vanaf Enschede"
# Rijtijd per plaats: bewust niet op de site (Lars, 21-09-2026).

# Merken (INPUT §B4)
MERKEN = {
    "salto": {"naam": "Salto", "lijnen": "", "partner": "", "logo_ok": ""},   # chat 20-09-2026: niet plaatsen, wel onderhoud en uitbreiding van bestaande Salto-systemen
    "xesar": {"naam": "EVVA Xesar", "lijnen": "de complete Xesar-lijn", "partner": "EVVA Partner", "logo_ok": "ja"},
    "emzy":  {"naam": "EVVA EMZY", "lijnen": "motorcilinder", "partner": "EVVA Partner", "logo_ok": "ja"},
    "mechanisch": {"naam": "EVVA 4KS+ en EVVA EPS, ABUS S6+ en ABUS Magtec (eigen profiel), ASSA ABLOY", "lijnen": "", "partner": "", "logo_ok": "ja"},
    "assa": {"naam": "ASSA ABLOY", "lijnen": "mechanisch en elektronisch", "partner": "officieel partner", "logo_ok": "ja"},
    "abus": {"naam": "ABUS", "lijnen": "mechanisch: S6+ en Magtec, eigen profiel", "partner": "officieel partner", "logo_ok": "ja"},
}
AIRKEY = "ja"                                                        # Lars, 21-09-2026: AirKey-startpakket vanaf € 487
PARTNERS = ["EVVA", "ASSA ABLOY", "ABUS"]                              # officieel partner van alle drie (Lars, 20-09-2026)
PARTNER_TEKST = "officieel partner van EVVA, ASSA ABLOY en ABUS"
# Eigen sleutelprofielen (Lars, 20-09-2026): cilinders op naam, voorraad in huis, dus snel leveren in plaats van weken wachten.
EIGEN_PROFIEL = "EVVA 4KS+, EVVA EPS, ABUS S6+ en ABUS Magtec"
EVVA_PROFIEL = "EVVA 4KS+ en EVVA EPS"
EVVA_PROJECTEN = True   # EVVA schakelt Westendorp in voor bepaalde projecten (Lars, 20-09-2026)

# Richtprijzen (INPUT §B5), excl. btw. Zonder ingevulde waarden gaat /kosten/ niet live.
# Vanaf-prijzen (Lars, 21-09-2026). Sleutel: (omschrijving, vanaf in euro als tekst of None, eenheid). None = regel weglaten.
# Aanname: excl. btw (B2B); Lars bevestigt.
PRIJZEN = {
    "slot":            ("Elektronisch slot (smart lock), geplaatst", "123", "per deur"),
    "airkey_start":    ("EVVA AirKey startpakket", "487", "per pakket"),
    "cilinder_xesar":  ("Elektronische cilinder EVVA Xesar, geplaatst", None, "per deur"),
    "beslag":          ("Elektronisch beslag, geplaatst", None, "per deur"),
    "emzy":            ("Motorcilinder EVVA EMZY, geplaatst", None, "per deur"),
    "wandlezer":       ("Wandlezer met elektrische sluitplaat", None, "per deur"),
    "infrezen":        ("Infrezen houten deur", None, "per deur"),
    "mech_cilinder":   ("Mechanische cilinder in eigen profiel", None, "per cilinder"),
    "servicecontract": ("Servicecontract", None, "per jaar"),
}
REKENVOORBEELDEN = []                                                # optioneel; leeg = blok weglaten
INVENTARISATIE_GRATIS = True                                         # INPUT §B5 aanname
PRIJS_DISCLAIMER = "Richtprijs, definitieve prijs na inventarisatie."
BTW_TEKST = "excl. btw"

def prijs(sleutel, eenheid=True):
    """'vanaf € 123 per deur' of, zonder bekende prijs, 'op aanvraag'."""
    oms, v, een = PRIJZEN[sleutel]
    if not v: return "op aanvraag"
    return f"vanaf € {v}" + (f" {een}" if eenheid else "")

# Proces en beloftes (INPUT §B6)
# Lars, 21-09-2026: alleen deze twee beloftes; doorlooptijd, uren per deur, garantie en contractvormen zijn per project en staan niet op de site.
REACTIE_AANVRAAG   = "1 werkdag"
OFFERTE_BINNEN     = "zo snel mogelijk, afhankelijk van de omvang"
REACTIE_STORING    = "binnen 4 tot 12 uur, dag en nacht, 365 dagen per jaar"

SECTOREN = ["kantoren", "zorg", "onderwijs"]                          # INPUT §B7 aanname; pagina's pas in fase 2
CERTIFICATEN = "officieel partner van EVVA, ASSA ABLOY en ABUS; monteurs PKVW-gecertificeerd (Politiekeurmerk Veilig Wonen); getraind door EVVA en door GU voor deurdrangers en deurautomaten"   # INPUT §B9 (Lars, 20/21-09-2026)
PKVW = "Onze monteurs zijn PKVW-gecertificeerd (Politiekeurmerk Veilig Wonen) en gespecialiseerd in het vernieuwen van oudere panden met toegangscontrole, zonder de bestaande deuren te vervangen."
DEURDRANGERS = "GU"                                                  # INPUT §B1: deurdrangers en deurautomaten van GU (Lars, 20-09-2026)

# Feiten in het kort (INPUT §C3)
TOEGANG_SINDS   = "1995"                                             # Lars, 21-09-2026
# Aantal deuren en monteurs: bewust niet op de site (Lars, 21-09-2026).
WERKPLAATS      = "Enschede en Hengelo"                              # Lars, 21-09-2026: werkplaats en uitrijbasis in beide; Hengelo is de servicevestiging met kantoor
VESTIGINGEN_MOEDER = "Enschede (winkel, Wesselernering 32) en Hengelo (Oldenzaalsestraat 553)"

# Adviseur (INPUT §C4): staat op elke pagina naast het formulier.
ADVISEURS = [  # Lars, 21-09-2026: twee adviseurs, zelfde nummer
    {"naam": "Lars", "functie": "adviseur toegangscontrole", "foto": "adviseur-lars.jpg", "tel_tonen": "053 478 42 45", "tel_link": "+31534784245"},
    {"naam": "Nick", "functie": "adviseur toegangscontrole", "foto": "adviseur-nick.jpg", "tel_tonen": "053 478 42 45", "tel_link": "+31534784245"},
]
ADVISEUR = ADVISEURS[0]
ADVISEUR_NAMEN = " of ".join(a["naam"] for a in ADVISEURS)          # "Lars of Nick"

# Conversie (INPUT §E)
# Duurzaamheid (Lars, 22-09-2026): ABUS Magtec in eigen profiel; cijfers van ABUS/ClimatePartner, met bron op /duurzaamheid/.
DUURZAAM = [
    ("46 procent minder CO₂", "De ABUS Magtec-cilinder veroorzaakt 46 procent minder broeikasgasemissies dan een conventionele profielcilinder, berekend door ClimatePartner over de levenscyclus (gebruiksfase niet meegerekend)."),
    ("Loodvrij geproduceerd", "Bij de productie van Magtec-cilinders wordt geen lood gebruikt; het verschil in uitstoot zit vooral in grondstoffen en productie."),
    ("SKG*** en uit voorraad", "Hoogste niveau op DIN EN 1303 en SKG***-gecertificeerd. Wij voeren Magtec in ons eigen profiel en leveren uit voorraad."),
]
CTA            = "Plan een gratis inventarisatie"                     # INPUT §E1 aanname
WHATSAPP       = ""                                                   # INPUT §E1 optioneel; leeg = geen WhatsApp
WEB3FORMS_KEY  = "50c899f1-e3b2-4bbe-b1b3-5dbd7c00ac7c"              # INPUT §E2 (Lars, 21-09-2026, incognito aangemaakt op info@); 3d5d8a2f… en 2fa6ec12… gingen naar autosleutel@
FORM_MAILBOX   = MAIL                                               # INPUT §E2: aanname, zelfde als het algemene adres
BEDANKT_TEKST  = ("Uw aanvraag is binnen. U ontvangt direct een bevestiging per e-mail. Lars of Nick belt u binnen 1 werkdag om uw situatie door te nemen "
                  "en de inventarisatie op locatie in te plannen. Daarna ontvangt u zo snel mogelijk een offerte met een vaste prijs per deur.")   # voorstel Claude, 21-09-2026
GOOGLE_TAG_ID  = "AW-17596975114"                                   # INPUT §E3 (Lars, 21-09-2026), gedeeld met andere sites; conversielabels volgen
ADS_LABEL_FORM = ""                                                   # INPUT §E3, "AW-xxx/label"; leeg = geen Ads-conversie
ADS_LABEL_TEL  = ""
SC_VERIFICATIE = "cP27EjU-ymEGxRVvGIe0oJR3uFC-TVVEizK6w0S-oP0"      # INPUT §E3 Search Console (Lars, 21-09-2026)
BING_VERIFICATIE = ""                                                 # INPUT §E3 optioneel
UET_TAG        = ""                                                   # INPUT §E3 optioneel

TAG_ACTIEF = "[[" not in GOOGLE_TAG_ID
VANDAAG = datetime.date.today()

# ============================================================
# Paden en hulpfuncties
# ============================================================
ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
STATIC = ROOT / "static"
BRON = STATIC / "img" / "bron"

def placeholder(s):
    return isinstance(s, str) and "[[" in s

def esc(s):
    return html.escape(str(s), quote=True)

def datum_nl(d):
    return d.strftime("%d-%m-%Y")

def versie(pad):
    return hashlib.md5(pad.read_bytes()).hexdigest()[:8]

def tel(tonen=None, link=None, klas="tel"):
    tonen, link = tonen or TEL_TONEN, link or TEL_LINK
    return f'<a class="{klas}" href="tel:{esc(link)}">{esc(tonen)}</a>'

def cta_knop(tekst=None, href="#aanvraag", cta_id="primair", klas="knop"):
    return f'<a class="{klas}" href="{href}" data-cta="{cta_id}">{esc(tekst or CTA)}</a>'

def acties(tekst=None, href="#aanvraag"):
    return f'<p class="acties" data-gedeeld>{cta_knop(tekst, href)}<span>of bel {tel()}</span></p>'

def p(*alineas):
    return "".join(f"<p>{a}</p>" for a in alineas)

def lijst(items, tag="ul", klas=""):
    kl = f' class="{klas}"' if klas else ""
    return f"<{tag}{kl}>" + "".join(f"<li>{i}</li>" for i in items) + f"</{tag}>"

def tabel(rijen, kop=None, bijschrift=None, rijkop=True):
    """Specificatiestrook: echte <table>. rijen = [(label, waarde), ...] of [(c1, c2, c3), ...] met kop."""
    uit = ['<div class="tabel-scroll"><table>']
    if bijschrift: uit.append(f"<caption class=\"visueel-verborgen\">{esc(bijschrift)}</caption>")
    if kop: uit.append("<thead><tr>" + "".join(f"<th scope=\"col\">{esc(k)}</th>" for k in kop) + "</tr></thead>")
    uit.append("<tbody>")
    for r in rijen:
        cellen = list(r)
        if rijkop:
            uit.append(f"<tr><th scope=\"row\">{cellen[0]}</th>" + "".join(f"<td>{c}</td>" for c in cellen[1:]) + "</tr>")
        else:
            uit.append("<tr>" + "".join(f"<td>{c}</td>" for c in cellen) + "</tr>")
    uit.append("</tbody></table></div>")
    return "".join(uit)

def feitenpaneel():
    """Vier harde feiten in panelen met groot cijfertype."""
    feiten = [(esc(MOEDER_SINDS), "Twents familiebedrijf, deuren en sloten sinds dat jaar"),
              ("EVVA", "officieel partner, net als van ASSA ABLOY en ABUS"),
              ("4 tot 12 uur", "storingsdienst, dag en nacht, 365 dagen per jaar"),
              ("PKVW", "gecertificeerde monteurs, gespecialiseerd in oudere panden")]
    return '<dl class="feitenpaneel">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in feiten) + "</dl>"

def feiten_groen():
    """Groene accentpanelen voor het duurzaamheidsblok."""
    return '<dl class="feitenpaneel feitenpaneel--groen">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in [
        ("46 %", "minder CO₂-equivalenten dan een conventionele ABUS-cilinder"), ("0", "lood in de productie"),
        ("SKG***", "hoogste veiligheidsniveau, onafhankelijk getest"), ("Voorraad", "eigen profiel, direct leverbaar")]) + "</dl>"

def label(tekst):
    return f'<span class="label">{esc(tekst)}</span>'

def hero(h1, intro, foto_html="", cta=True, extra="", illustratie=None, kicker=None):
    """Kop van elke pagina: label, H1, answer-first alinea, CTA; rechts een foto of een illustratie."""
    rechts_inhoud = foto_html or (f'<div class="hero__illustratie">{illustratie}</div>' if illustratie else "")
    rechts = f'<div class="k6 hero__rechts">{rechts_inhoud}</div>' if rechts_inhoud else ""
    kol = "k6" if rechts_inhoud else "k8"
    return (f'<section class="hero"><div class="wrap"><div class="rooster"><div class="{kol}">{label(kicker) if kicker else ""}<h1>{h1}</h1>'
            f'<p class="intro">{intro}</p>{extra}{acties() if cta else ""}</div>{rechts}</div></div></section>')

ISO_CSS = """<style>
.led{animation:led 1.8s ease-in-out infinite}@keyframes led{0%,100%{opacity:1}50%{opacity:.15}}
.anim-auto{animation:rijden 7s linear infinite}@keyframes rijden{0%{transform:translate(-62px,-36px);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translate(62px,36px);opacity:0}}
.anim-auto-2{animation:rijden 11s linear infinite 4s}
.anim-auto-y{animation:rijden-y 9s linear infinite 2s}@keyframes rijden-y{0%{transform:translate(58px,-34px);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translate(-58px,34px);opacity:0}}
.anim-vlag{animation:wapperen 1.4s ease-in-out infinite alternate}@keyframes wapperen{from{transform:scaleX(1)}to{transform:scaleX(.72)}}
.anim-gloed{animation:gloed 2.4s ease-in-out infinite}@keyframes gloed{0%,100%{opacity:1}50%{opacity:.45}}
.anim-water{animation:water 3s ease-in-out infinite}@keyframes water{0%,100%{opacity:1;transform:translate(0,0)}50%{opacity:.55;transform:translate(2px,1px)}}
.anim-rook{animation:rook 3s ease-out infinite}@keyframes rook{0%{opacity:.8;transform:translate(0,0)}100%{opacity:0;transform:translate(6px,-18px)}}
.anim-bal{animation:bal 2.2s ease-in-out infinite alternate}@keyframes bal{from{transform:translate(0,0)}to{transform:translate(18px,10px)}}
.anim-heftruck{animation:heftruck 5s ease-in-out infinite alternate}@keyframes heftruck{from{transform:translate(0,0)}to{transform:translate(-26px,15px)}}
.anim-licht{animation:licht 9s ease-in-out infinite}.anim-licht-1{animation-delay:2s}.anim-licht-2{animation-delay:4.5s}.anim-licht-3{animation-delay:6.5s}
@keyframes licht{0%,35%{fill:#BFE6FF}45%,85%{fill:#FFE49A}95%,100%{fill:#BFE6FF}}
.anim-kraan{animation:kraan 14s ease-in-out infinite alternate}@keyframes kraan{from{transform:rotate(-25deg)}to{transform:rotate(30deg)}}
.anim-loper{animation:loper 9s linear infinite}@keyframes loper{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""

def iso_bestand(sleutel):
    """Schrijft de sectorscène als los SVG-bestand (met de animaties erin) en geeft een <img> terug; scheelt ~110 KB per pagina."""
    uit = DIST / "static" / "img" / "iso"; uit.mkdir(parents=True, exist_ok=True)
    svg = isometrie.SECTOREN[sleutel]()
    svg = svg.replace('class="iso">', 'class="iso">' + ISO_CSS, 1)
    (uit / f"{sleutel}.svg").write_text(svg, encoding="utf-8")
    alt = re.search(r'aria-label="([^"]+)"', svg).group(1)
    return f'<img src="/static/img/iso/{sleutel}.svg" alt="{alt}" width="444" height="350" loading="lazy" class="iso">'

def sectorrij(items, kop, intro=None, kicker="Sectoren"):
    """Horizontaal scrollende rij met illustratie, kop, tekst en link, zoals de sectorrij van Salto."""
    kaarten = "".join(
        f'<article class="kaart"><div class="kaart__beeld">{iso_bestand(sleutel)}</div>'
        f'<div class="kaart__tekst"><h3>{esc(k)}</h3><p>{t}</p><a class="meer" href="{u}">{esc(linktekst)}</a></div></article>'
        for sleutel, k, t, u, linktekst in items)
    return (f'<section class="reveal"><div class="wrap"><div class="rij-kop"><div>{label(kicker)}<h2>{kop}</h2>{f"<p class=intro>{intro}</p>" if intro else ""}</div>'
            f'<div class="rij-knoppen"><button type="button" data-rij="-1" aria-label="Vorige">&#8249;</button><button type="button" data-rij="1" aria-label="Volgende">&#8250;</button></div></div>'
            f'<div class="rij" data-rij-scroll>{kaarten}</div></div></section>')

def video(bestand, poster, alt, kop="Bekijk de video", onderschrift=None):
    """Video op klik, nooit autoplay, eigen bestand uit static/img/bron/. Poster is een eigen foto (3:2) die door de
    beeldpipeline gaat. Ontbreekt de video of de poster, dan wordt het blok weggelaten en gemeld."""
    bronpad = BRON / bestand
    if not bronpad.exists() or not (BRON / poster).exists():
        _ONTBREKEND.append(bestand if not bronpad.exists() else poster)
        return ""
    uit = DIST / "static" / "video"; uit.mkdir(parents=True, exist_ok=True)
    shutil.copy(bronpad, uit / bestand)
    mime = "video/webm" if bestand.endswith(".webm") else "video/mp4"
    poster_html = beeld(poster, alt, sizes="(min-width: 900px) 66vw, 100vw")
    bijschrift = f"<figcaption>{esc(onderschrift)}</figcaption>" if onderschrift else ""
    return (f'<figure class="video" data-video>'
            f'<button type="button" class="video__start" aria-label="{esc(kop)}">{poster_html}<span class="video__knop">{esc(kop)}</span></button>'
            f'<video controls preload="none" playsinline hidden width="1600" height="1067"><source src="/static/video/{bestand}" type="{mime}"></video>'
            f'{bijschrift}</figure>')

def kaart_svg():
    """Schematische kaart van het werkgebied: Enschede in het midden, een cirkel voor 60 minuten rijden, de plaatsen
    als punten op hun ligging (lengte- en breedtegraad, benaderd). Geen kaartdienst, geen externe request."""
    ligging = {"Enschede": (6.89, 52.22), "Hengelo": (6.79, 52.27), "Almelo": (6.66, 52.36), "Oldenzaal": (6.93, 52.31),
               "Haaksbergen": (6.74, 52.16), "Borne": (6.75, 52.30), "Deventer": (6.16, 52.25), "Zwolle": (6.09, 52.51),
               "Zutphen": (6.20, 52.14), "Doetinchem": (6.29, 51.96), "Apeldoorn": (5.97, 52.21)}
    cx, cy, schaal = 6.89, 52.22, 230          # px per graad lengte; breedtegraad gecorrigeerd met cos(52 graden), 0,62
    def xy(lon, lat): return 300 + (lon - cx) * schaal, 220 - (lat - cy) * schaal / 0.62
    punten = []
    for naam, _, _, _ in WERKGEBIED:
        if naam not in ligging: continue
        x, y = xy(*ligging[naam])
        anker = "end" if x < 300 else "start"; dx = -10 if x < 300 else 10
        kleur = "#1B68C0" if naam == PLAATS else "#14232E"
        punten.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{6 if naam == PLAATS else 4}" fill="{kleur}"/>'
                      f'<text x="{x + dx:.0f}" y="{y + 4:.0f}" text-anchor="{anker}" font-size="13" fill="#14232E">{esc(naam)}</text>')
    return (f'<svg viewBox="0 0 600 440" width="600" height="440" role="img" aria-label="Schematische kaart van het werkgebied rond {esc(PLAATS)}" '
            f'xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;font-family:inherit">'
            f'<circle cx="300" cy="220" r="205" fill="#F2F4F6" stroke="#C9CED0"/>{"".join(punten)}'
            f'<text x="300" y="425" text-anchor="middle" font-size="12" fill="#4A5760">Schematisch: plaatsen op hun ligging, de cirkel is ongeveer 60 minuten rijden</text></svg>')

def sectie(kop, inhoud, wit=False, lijn=False, kop_id=None, extra="", kicker=None, groen=False):
    kl = " ".join(k for k in ["reveal", "sectie--wit" if wit else "", "sectie--lijn" if lijn else "", "sectie--groen" if groen else ""] if k)
    kl = f' class="{kl}"' if kl else ""
    hid = f' id="{kop_id}"' if kop_id else ""
    kop_html = (label(kicker) if kicker else "") + (f"<h2{hid}>{kop}</h2>" if kop else "")
    return f'<section{kl}><div class="wrap">{kop_html}{inhoud}{extra}</div></section>'

def stappen(items):
    """Genummerde stappen (het is een volgorde): [(kop, tekst), ...]"""
    return '<ol class="stappen">' + "".join(f"<li><h3>{k}</h3><p>{t}</p></li>" for k, t in items) + "</ol>"

def faqblok(items, kop="Veelgestelde vragen"):
    binnen = "".join(f'<details><summary>{esc(v)}</summary><div class="antwoord">{a if a.startswith("<") else "<p>"+a+"</p>"}</div></details>' for v, a in items)
    return sectie(kop, f'<div class="faq rooster"><div class="k8">{binnen}</div></div>') if False else \
        f'<section class="reveal"><div class="wrap"><div class="rooster"><div class="k8">{label("Veelgestelde vragen")}<h2>{kop}</h2><div class="faq">{binnen}</div></div></div></div></section>'

def kruimels(items):
    """items = [(naam, pad), ...]; laatste zonder link."""
    delen = []
    for i, (n, pad) in enumerate(items):
        delen.append(f'<li><a href="{pad}">{esc(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{esc(n)}</li>')
    return f'<nav class="wrap kruimels" aria-label="Kruimelpad"><ol>{"".join(delen)}</ol></nav>'

# ---------- Beeld: eigen foto's uit static/img/bron, alleen schalen en comprimeren ----------
_ONTBREKEND = []
_MATEN = (800, 1200, 1600)

def _verwerk(bronpad):
    """Schrijft WebP (en AVIF als dat >20% kleiner is) in drie breedtes naar dist. Geeft (breedte, hoogte, avif_ok)."""
    from PIL import Image, ImageOps
    uit = DIST / "static" / "img"
    uit.mkdir(parents=True, exist_ok=True)
    with Image.open(bronpad) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        b0, h0 = im.size
        avif_ok = True
        for w in _MATEN:
            if w > b0 and w != _MATEN[0]:
                continue
            w2 = min(w, b0); h2 = round(h0 * w2 / b0)
            kopie = im.resize((w2, h2), Image.LANCZOS)
            wp = uit / f"{beeldnaam(bronpad.stem)}-{w}.webp"
            kopie.save(wp, "WEBP", quality=80, method=6)
            av = uit / f"{beeldnaam(bronpad.stem)}-{w}.avif"
            try:
                kopie.save(av, "AVIF", quality=60)
                if av.stat().st_size > wp.stat().st_size * 0.8:
                    av.unlink(); avif_ok = False
            except Exception:
                avif_ok = False
        return b0, h0, avif_ok

_BEELDCACHE = {}
_BEELDEN_PAGINA = []   # (url, alt, onderschrift, breedte, hoogte) van de pagina die nu gebouwd wordt; schrijf() leest en leegt dit

def beeldnaam(stem):
    """Bestandsnaam voor Google: kleine letters, koppeltekens, geen spaties, cijfers of camera-namen (IMG_1234)."""
    import unicodedata
    n = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode().lower()
    n = re.sub(r"[^a-z0-9]+", "-", n).strip("-")
    return n or "foto"

def beeld(bestand, alt, onderschrift=None, lazy=True, sizes="(min-width: 900px) 40vw, 100vw", klas="", bron=None):
    """bron: maker van het beeld voor het schema (standaard Westendorp; fabrikantbeeld: bijv. 'ABUS')."""
    """Eigen foto uit static/img/bron/<bestand>. Ontbreekt de foto: blok weglaten en melden."""
    bronpad = BRON / bestand
    if not bronpad.exists():
        _ONTBREKEND.append(bestand)
        return ""
    if bestand not in _BEELDCACHE:
        _BEELDCACHE[bestand] = _verwerk(bronpad)
    b0, h0, avif_ok = _BEELDCACHE[bestand]
    stem = beeldnaam(bronpad.stem)
    maten = [w for w in _MATEN if w <= b0 or w == _MATEN[0]]
    w1 = maten[0]; h1 = round(h0 * min(w1, b0) / b0)
    srcset = lambda ext: ", ".join(f"/static/img/{stem}-{w}.{ext} {min(w, b0)}w" for w in maten)
    laad = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    img = (f'<img src="/static/img/{stem}-{w1}.webp" srcset="{srcset("webp")}" sizes="{sizes}" '
           f'width="{min(w1, b0)}" height="{h1}" alt="{esc(alt)}"{laad}>')
    if avif_ok:
        img = f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">{img}</picture>'
    kl = f' class="{klas}"' if klas else ""
    wg = maten[-1]; _BEELDEN_PAGINA.append((f"/static/img/{stem}-{wg}.webp", alt, onderschrift, min(wg, b0), round(h0 * min(wg, b0) / b0), bron or NAAM))
    if onderschrift:
        return f"<figure{kl}>{img}<figcaption>{esc(onderschrift)}</figcaption></figure>"
    return f"<figure{kl}>{img}</figure>"

# ---------- JSON-LD ----------
ORG_ID = SITE + "/#organisatie"
WEBSITE_ID = SITE + "/#website"

def bedrijf_ld():
    same_as = [u for u in [LINKEDIN, GOOGLE_PROFIEL] + ANDERE_PROFIELEN if u and not placeholder(u)]
    org = {
        "@type": "LocalBusiness", "@id": ORG_ID, "name": NAAM, "legalName": RECHTSPERSOON,
        "url": SITE + "/", "logo": SITE + "/static/img/logo/logo.svg", "image": SITE + "/static/img/og-standaard.png",
        "telephone": TEL_LINK, "email": MAIL,
        "address": {"@type": "PostalAddress", "streetAddress": STRAAT, "postalCode": POSTCODE,
                    "addressLocality": PLAATS, "addressRegion": REGIO, "addressCountry": "NL"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in OPENING_SCHEMA],
        "areaServed": [{"@type": "City", "name": naam} for naam, _, _, _ in WERKGEBIED],
        "identifier": [{"@type": "PropertyValue", "propertyID": "KvK", "value": KVK}],
        "parentOrganization": {"@type": "Organization", "@id": SITE + "/#groep", "name": RECHTSPERSOON, "identifier": {"@type": "PropertyValue", "propertyID": "KvK", "value": KVK}},
        "knowsAbout": ["Toegangscontrole", "EVVA Xesar", "EVVA EMZY", "Mechanische sluitsystemen", "Sluitplannen", "Elektronische sloten", "ASSA ABLOY", "ABUS", "Salto onderhoud", "Deurdrangers GU", "Politiekeurmerk Veilig Wonen"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Diensten", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": SITE + u}} for n, u in DIENSTEN_NAV]},
    }
    if same_as: org["sameAs"] = same_as
    if LAT and LON: org["geo"] = {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON}
    if not placeholder(TOEGANG_SINDS): org["foundingDate"] = str(TOEGANG_SINDS)
    if not placeholder(VESTIGINGSNR): org["identifier"].append({"@type": "PropertyValue", "propertyID": "Vestigingsnummer", "value": VESTIGINGSNR})
    return org

def website_ld():
    return {"@type": "WebSite", "@id": WEBSITE_ID, "url": SITE + "/", "name": NAAM, "inLanguage": "nl-NL", "publisher": {"@id": ORG_ID}}

def webpage_ld(pad, titel, omschrijving, typ="WebPage", datum=None, beelden=()):
    d = {"@type": typ, "@id": SITE + pad + "#webpage", "url": SITE + pad, "name": titel, "description": omschrijving,
         "inLanguage": "nl-NL", "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": ORG_ID}}
    if datum: d["dateModified"] = datum
    if beelden:
        url, alt, onderschrift, b, h, maker = beelden[0]
        d["primaryImageOfPage"] = {"@type": "ImageObject", "contentUrl": SITE + url, "url": SITE + url, "width": b, "height": h,
                                   "description": alt, **({"caption": onderschrift} if onderschrift else {}), "creditText": maker,
                                   **({"creator": {"@id": ORG_ID}, "copyrightNotice": RECHTSPERSOON} if maker == NAAM else {"copyrightNotice": maker})}
        d["image"] = [SITE + u for u, *_ in beelden[:5]]
    return d

def kruimels_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + pad} for i, (n, pad) in enumerate(items)]}

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for v, a in items]}

def service_ld(pad, naam, omschrijving, merk=None):
    d = {"@type": "Service", "@id": SITE + pad + "#dienst", "name": naam, "description": omschrijving, "serviceType": naam,
         "provider": {"@id": ORG_ID}, "areaServed": [{"@type": "City", "name": n} for n, _, _, _ in WERKGEBIED], "url": SITE + pad}
    if merk: d["brand"] = {"@type": "Brand", "name": merk}
    return d

def ld_script(graph):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")) + "</script>"

# ============================================================
# Gedeelde blokken: header, footer, formulier, adviseur, consent
# ============================================================
DIENSTEN_NAV = [("Toegangscontrole", "/toegangscontrole/"), ("Elektronische sloten", "/elektronische-sloten/"),
                ("EVVA Xesar", "/evva-xesar/"), ("Motorcilinder", "/motorcilinder/"), ("Sluitplan", "/sluitplan/"),
                ("Service en beheer", "/service-en-beheer/"), ("Salto onderhoud", "/salto/")]
NAV = [("Toegangscontrole", "/toegangscontrole/"), ("Elektronische sloten", "/elektronische-sloten/"),
       ("Sluitplan", "/sluitplan/"), ("Kosten", "/kosten/"), ("Service", "/service-en-beheer/"),
       ("Over ons", "/over-ons/"), ("Contact", "/contact/")]

_ICOON_BEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
_ICOON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

def header(pad):
    items = "".join(f'<li><a href="{u}"{" aria-current=\"page\"" if u == pad else ""}>{esc(n)}</a></li>' for n, u in NAV)
    return f'''<header class="kop"><div class="wrap">
<a class="logo" href="/" aria-label="{esc(NAAM)}, naar de homepage"><img src="/static/img/logo/logo.svg" alt="{esc(NAAM)}" width="2053" height="647"></a>
<nav class="nav" id="nav" aria-label="Hoofdmenu"><ul>{items}</ul></nav>
<div class="kop__acties"><a class="bel" href="tel:{esc(TEL_LINK)}" aria-label="Bel {esc(NAAM)}, {esc(TEL_TONEN)}">{_ICOON_BEL}<span>{esc(TEL_TONEN)}</span></a>
<button class="menu-knop" id="menu-knop" type="button" aria-expanded="false" aria-controls="nav">{_ICOON_MENU}<span>Menu</span></button></div>
</div></header>'''

# Keurmerk- en partnerlogo's in de footer (Lars, 21-09-2026: PKVW mag erbij). Alleen getoond als het bestand bestaat.
FOOTER_LOGOS = [("pkvw", "Politiekeurmerk Veilig Wonen, gecertificeerde monteurs"), ("evva", "EVVA Partner"),
                ("assa-abloy", "ASSA ABLOY partner"), ("abus", "ABUS partner"), ("gu", "GU deurdrangers en deurautomaten")]

def footer_logos():
    map_ = STATIC / "img" / "logo" / "partners"
    items = []
    for naam, alt in FOOTER_LOGOS:
        bron = next((map_ / f"{naam}.{ext}" for ext in ("svg", "png", "webp") if (map_ / f"{naam}.{ext}").exists()), None)
        if not bron: continue
        uit = DIST / "static" / "img" / "logo" / "partners"; uit.mkdir(parents=True, exist_ok=True)
        shutil.copy(bron, uit / bron.name)
        b, h = (0, 0)
        if bron.suffix != ".svg":
            from PIL import Image
            with Image.open(bron) as im: b, h = im.size
        else:
            b, h = 160, 60
        items.append(f'<li><img src="/static/img/logo/partners/{bron.name}" alt="{esc(alt)}" width="{b}" height="{h}" loading="lazy"></li>')
    return f'<ul class="voet__logos" aria-label="Keurmerken en partners">{"".join(items)}</ul>' if items else ""

def footer():
    diensten = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in DIENSTEN_NAV + [("Kosten", "/kosten/")])
    over = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in [("Over ons", "/over-ons/"), ("Duurzaamheid", "/duurzaamheid/"), ("Werkgebied", "/werkgebied/"), ("Contact", "/contact/"), ("Privacy", "/privacy/")])
    btw = f"<p>Btw-nummer {esc(BTW)}.</p>" if BTW else ""
    profiel = f'<li><a href="{esc(GOOGLE_PROFIEL)}" rel="noopener">Google Bedrijfsprofiel</a></li>' if not placeholder(GOOGLE_PROFIEL) else ""
    linkedin = f'<li><a href="{esc(LINKEDIN)}" rel="noopener">LinkedIn</a></li>' if not placeholder(LINKEDIN) else ""
    cookies = '<li><button type="button" data-consent-open>Cookie-instellingen</button></li>' if TAG_ACTIEF else ""
    return f'''<footer class="voet"><div class="wrap">
<div class="rooster">
<div class="k3"><p class="voet__naam">{esc(NAAM)}</p><p>Elektronische toegangscontrole, mechanische sluitsystemen en sluitplannen voor bedrijven en instellingen in Twente en Oost-Nederland.</p><p>{cta_knop(cta_id="footer")}</p></div>
<div class="k3"><h2>Diensten</h2><ul>{diensten}</ul></div>
<div class="k3"><h2>Contact</h2><address><p>{esc(STRAAT)}<br>{esc(POSTCODE)} {esc(PLAATS)}</p>
<p><a href="tel:{esc(TEL_LINK)}">{esc(TEL_TONEN)}</a><br><a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a></p>
<p>Bereikbaar {esc(OPENING_TEKST)}.</p></address></div>
<div class="k3"><h2>Over</h2><ul>{over}{profiel}{linkedin}{cookies}</ul></div>
</div>
{footer_logos()}<div class="onderdeel"><p>{esc(NAAM)} is onderdeel van {esc(RECHTSPERSOON)}, KvK {esc(KVK)}, {esc(PLAATS)}.</p>{btw}</div>
</div></footer>'''

def consent_html():
    if not TAG_ACTIEF: return ""
    return f'''<div class="consent" id="consent" hidden role="region" aria-label="Cookies"><div class="wrap">
<p>Wij gebruiken cookies van Google om te zien hoe de site wordt gebruikt en of onze advertenties werken. Pas na uw toestemming. Meer in de <a href="/privacy/">privacyverklaring</a>.</p>
<div class="knoppen"><button type="button" class="knop knop--tweede" data-consent="denied">Weigeren</button><button type="button" class="knop" data-consent="granted">Toestaan</button></div>
</div></div>'''

def tag_html():
    if not TAG_ACTIEF: return ""
    return f'''<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500}});</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_TAG_ID}"></script>
<script>gtag('js',new Date());gtag('config','{GOOGLE_TAG_ID}');</script>
'''

def _opties(naam, items, leeg="Maak een keuze"):
    return f'<option value="">{leeg}</option>' + "".join(f'<option value="{esc(i)}">{esc(i)}</option>' for i in items)

def formulier(kort=False, kop="Plan een inventarisatie", intro=None):
    """Het ene formulier van de site (BRIEF §7). kort=True: zelfde velden, als blok onderaan een pagina."""
    intro = intro or ("Vul het formulier in; " + esc(ADVISEUR_NAMEN) + " neemt contact met u op binnen " + esc(REACTIE_AANVRAAG) + ". Alleen naam, plaats en een telefoonnummer of e-mailadres zijn verplicht.")
    velden = f'''<form class="formulier" method="post" action="https://api.web3forms.com/submit" data-aanvraag novalidate>
<div class="veld"><label for="f-naam">Naam</label><input id="f-naam" name="naam" type="text" autocomplete="name" required><span class="melding" aria-live="polite"></span></div>
<div class="veld"><label for="f-bedrijf">Bedrijf of organisatie</label><input id="f-bedrijf" name="bedrijf" type="text" autocomplete="organization"></div>
<div class="veld"><label for="f-email">E-mailadres</label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email"><span class="melding" aria-live="polite"></span></div>
<div class="veld"><label for="f-telefoon">Telefoonnummer</label><input id="f-telefoon" name="telefoon" type="tel" autocomplete="tel" inputmode="tel"><span class="melding" aria-live="polite"></span></div>
<div class="veld"><label for="f-plaats">Plaats van het pand</label><input id="f-plaats" name="plaats" type="text" autocomplete="address-level2" required><span class="melding" aria-live="polite"></span></div>
<div class="veld"><label for="f-pand">Type pand</label><select id="f-pand" name="type_pand">{_opties("type_pand", ["Kantoor", "School", "Zorg", "Appartementencomplex", "Vereniging of kerk", "Recreatiepark", "Bedrijfspand of magazijn", "Overheid", "Anders"])}</select></div>
<div class="veld"><label for="f-deuren">Aantal deuren</label><select id="f-deuren" name="aantal_deuren">{_opties("aantal_deuren", ["1 tot 5", "6 tot 20", "21 tot 50", "Meer dan 50"])}</select></div>
<div class="veld"><label for="f-situatie">Huidige situatie</label><select id="f-situatie" name="huidige_situatie">{_opties("huidige_situatie", ["Mechanisch sluitplan", "Losse sloten", "Elektronisch systeem van een ander merk", "Nieuwbouw"])}</select></div>
<div class="veld breed"><label for="f-toelichting">Toelichting</label><span class="hint" id="f-toelichting-hint">Bijvoorbeeld: welke deuren, wat er nu niet werkt, wanneer u het geregeld wilt hebben.</span><textarea id="f-toelichting" name="toelichting" aria-describedby="f-toelichting-hint"></textarea></div>
<div class="honing" aria-hidden="true"><label for="f-website">Website</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="botcheck" value="">
<div class="breed"><button class="knop" type="submit">{esc(CTA)}</button><p class="form-status" role="status" aria-live="polite"></p>
<p class="zacht">Uw gegevens gebruiken wij alleen om contact met u op te nemen. Zie de <a href="/privacy/">privacyverklaring</a>.</p></div>
</form>'''
    return f'''<section class="reveal" id="aanvraag" data-gedeeld><div class="wrap"><div class="rooster">
<div class="k8">{label("Contact")}<h2>{esc(kop)}</h2><p class="tekst">{intro}</p>{velden}</div>
<div class="k4">{adviseurblok()}</div>
</div></div></section>'''

def adviseurblok():
    personen = "".join(
        f'<div class="adviseur__persoon">{beeld(a["foto"], f"{a['naam']}, {a['functie']} bij {NAAM}", sizes="120px") if a["foto"] else ""}'
        f'<p class="naam">{esc(a["naam"])}</p><p class="functie">{esc(a["functie"].capitalize())}</p></div>' for a in ADVISEURS)
    a = ADVISEUR
    feiten = [f"Reactie binnen {esc(REACTIE_AANVRAAG)}",
              "Inventarisatie op locatie" + (", zonder kosten" if INVENTARISATIE_GRATIS else ""),
              PARTNER_TEKST.capitalize(),
              f"Twents familiebedrijf sinds {esc(MOEDER_SINDS)}"]
    return f'''<div class="adviseur"><div class="adviseur__personen">{personen}</div>
<p>Direct: <a href="tel:{esc(a["tel_link"])}">{esc(a["tel_tonen"])}</a><br><a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a></p>
<ul class="feiten">{"".join(f"<li>{f}</li>" for f in feiten)}</ul></div>'''

# ============================================================
# Pagina schrijven
# ============================================================
_LASTMOD_PAD = ROOT / "lastmod.json"
_LASTMOD = json.loads(_LASTMOD_PAD.read_text(encoding="utf-8")) if _LASTMOD_PAD.exists() else {}
_PAGINAS = []      # (pad, titel, llms-regel, noindex, datum)
_ASSETS = {}

def _template():
    return (ROOT / "templates" / "basis.html").read_text(encoding="utf-8")

def _vul(sjabloon, waarden):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: waarden.get(m.group(1), ""), sjabloon)

def _lastmod(pad, inhoud):
    """Datum van de laatste inhoudelijke wijziging: verandert alleen als de tekst verandert."""
    h = hashlib.md5(re.sub(r"\s+", " ", inhoud).encode("utf-8")).hexdigest()
    rec = _LASTMOD.get(pad)
    if not rec or rec["hash"] != h:
        _LASTMOD[pad] = {"hash": h, "datum": VANDAAG.isoformat()}
    return _LASTMOD[pad]["datum"]

def schrijf(pad, titel, omschrijving, body, kruimelpad=None, faq=None, extra_ld=(), paginatype="WebPage",
            noindex=False, llms="", og_beeld=None, met_formulier=True, formulier_kop="Plan een inventarisatie"):
    """Schrijft dist/<pad>/index.html. pad begint en eindigt met een slash."""
    kruimelpad = kruimelpad or [("Home", "/")] + ([(titel.split(" | ")[0], pad)] if pad != "/" else [])
    kruimel_html = kruimels(kruimelpad) if pad != "/" else ""
    faq_html = faqblok(faq) if faq else ""
    form_html = formulier(kop=formulier_kop) if met_formulier else ""
    volledige_body = kruimel_html + body + faq_html + form_html
    datum = _lastmod(pad, body)
    beelden = [b for b in _BEELDEN_PAGINA if "adviseur-" not in b[0]]; _BEELDEN_PAGINA.clear()   # adviseurfoto's tellen niet als paginabeeld
    graph = [bedrijf_ld(), website_ld(), webpage_ld(pad, titel, omschrijving, paginatype, datum, beelden), kruimels_ld(kruimelpad)]
    graph += list(extra_ld)
    if faq: graph.append(faq_ld(faq))
    volledige_titel = titel if pad == "/" else f"{titel} | {NAAM}" if len(f"{titel} | {NAAM}") <= 60 else titel
    verificatie = (f'<meta name="google-site-verification" content="{esc(SC_VERIFICATIE)}">\n' if SC_VERIFICATIE else "") + \
                  (f'<meta name="msvalidate.01" content="{esc(BING_VERIFICATIE)}">\n' if BING_VERIFICATIE else "")
    waarden = {
        "titel": esc(volledige_titel), "omschrijving": esc(omschrijving), "canonical": SITE + pad, "sitenaam": esc(NAAM),
        "robots": '<meta name="robots" content="noindex, nofollow">\n' if noindex else "", "verificatie": verificatie,
        "og_beeld": SITE + (og_beeld or (beelden[0][0] if beelden else "/static/img/og-standaard.png")),
        "css": _ASSETS["css"], "js": _ASSETS["js"], "tag": tag_html(), "jsonld": ld_script(graph),
        "header": header(pad), "body": volledige_body, "footer": footer(), "consent": consent_html(),
        "config_js": json.dumps({"tagActief": TAG_ACTIEF, "web3formsKey": WEB3FORMS_KEY, "adsLabelForm": ADS_LABEL_FORM,
                                 "adsLabelTel": ADS_LABEL_TEL, "cta": CTA, "mail": MAIL}, ensure_ascii=False),
    }
    uit = DIST / pad.strip("/") / "index.html" if pad != "/" else DIST / "index.html"
    uit.parent.mkdir(parents=True, exist_ok=True)
    uit.write_text(_vul(_template(), waarden), encoding="utf-8")
    _PAGINAS.append((pad, titel, llms, noindex, datum, beelden))

# ============================================================
# Bouwen
# ============================================================
def assets():
    if DIST.exists(): shutil.rmtree(DIST)
    (DIST / "static" / "css").mkdir(parents=True); (DIST / "static" / "js").mkdir(parents=True)
    css = (STATIC / "css" / "tokens.css").read_text(encoding="utf-8") + "\n" + (STATIC / "css" / "styles.css").read_text(encoding="utf-8")
    css_naam = f"site.{hashlib.md5(css.encode()).hexdigest()[:8]}.css"
    (DIST / "static" / "css" / css_naam).write_text(css, encoding="utf-8")
    js_naam = f"site.{versie(STATIC / 'js' / 'site.js')}.js"
    shutil.copy(STATIC / "js" / "site.js", DIST / "static" / "js" / js_naam)
    _ASSETS["css"], _ASSETS["js"] = f"/static/css/{css_naam}", f"/static/js/{js_naam}"
    shutil.copytree(STATIC / "font", DIST / "static" / "font")
    logo_uit = DIST / "static" / "img" / "logo"; logo_uit.mkdir(parents=True)
    # Alleen de header is zwart (#111111); daar staat het logo, dus de variant voor zwarte achtergrond (LEESMIJ: tot #1E1E1E).
    lb = STATIC / "img" / "logo"
    shutil.copy(lb / "logo-zwarte-achtergrond.svg", logo_uit / "logo.svg")
    shutil.copy(lb / "icoon-zwarte-achtergrond.svg", logo_uit / "icoon.svg")
    for extra in ["favicon.ico", "apple-touch-icon.png", "og-standaard.png"]:
        b = STATIC / "img" / extra
        if b.exists(): shutil.copy(b, DIST / (extra if extra != "og-standaard.png" else "static/img/og-standaard.png"))
    (DIST / "manifest.webmanifest").write_text(json.dumps({"name": NAAM, "short_name": "Westendorp", "start_url": "/", "display": "browser",
        "background_color": "#222427", "theme_color": "#222427", "icons": [{"src": "/static/img/logo/icoon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False), encoding="utf-8")

def vierhonderdvier():
    links = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in [("Toegangscontrole", "/toegangscontrole/"), ("Wat kost toegangscontrole", "/kosten/"), ("EVVA Xesar", "/evva-xesar/"), ("Motorcilinder", "/motorcilinder/"), ("Contact", "/contact/")])
    body = f'<section class="hero"><div class="wrap"><div class="rooster"><div class="k8"><h1>Deze pagina bestaat niet</h1><p>Het adres klopt niet meer of is verkeerd getypt. Dit zijn de pagina\'s waar de meeste bezoekers naar zoeken.</p><ul class="lijst-links">{links}</ul>{acties()}</div></div></div></section>'
    schrijf("/404/", "Pagina niet gevonden", "De pagina die u zocht bestaat niet op westendorptoegang.nl. Ga verder naar toegangscontrole, wat het kost, EVVA Xesar, sluitplannen of neem contact op.", body, noindex=True, met_formulier=False)
    shutil.move(DIST / "404" / "index.html", DIST / "404.html"); (DIST / "404").rmdir()
    _PAGINAS[:] = [p for p in _PAGINAS if p[0] != "/404/"]

def sitemap_robots_llms():
    index = [(pad, datum, beelden) for pad, _, _, noindex, datum, beelden in _PAGINAS if not noindex]
    def beeld_xml(b):
        url, alt, onderschrift, *_ = b
        return f"<image:image><image:loc>{SITE}{url}</image:loc><image:title>{html.escape(alt)}</image:title>" + (f"<image:caption>{html.escape(onderschrift)}</image:caption>" if onderschrift else "") + "</image:image>"
    urls = "".join(f"<url><loc>{SITE}{pad}</loc><lastmod>{datum}</lastmod>{''.join(beeld_xml(b) for b in beelden)}</url>" for pad, datum, beelden in index)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{urls}</urlset>\n', encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "PerplexityBot", "Google-Extended", "Bingbot", "Applebot"]
    robots = "User-agent: *\nAllow: /\nDisallow: /bedankt/\n\n" + "".join(f"User-agent: {b}\nAllow: /\nDisallow: /bedankt/\n\n" for b in bots) + f"Sitemap: {SITE}/sitemap.xml\n"
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    regels = "".join(f"- [{titel}]({SITE}{pad}): {llms}\n" for pad, titel, llms, noindex, _, _ in _PAGINAS if llms and not noindex)
    plaatsen = ", ".join(n for n, _, _, _ in WERKGEBIED)
    llms = f"""# {NAAM}

> {NAAM} levert en installeert elektronische toegangscontrole (EVVA Xesar, EVVA EMZY), mechanische sluitsystemen en sluitplannen voor bedrijven en instellingen in Oost-Nederland, altijd op locatie bij de klant, vanuit {PLAATS}. Bestaande Salto-systemen onderhoudt en breidt het bedrijf uit. Werkgebied: {WERKGEBIED_REGEL}, onder meer {plaatsen}. Onderdeel van {RECHTSPERSOON}, KvK {KVK}; Twents familiebedrijf, actief in deuren, sloten en beslag sinds {MOEDER_SINDS}. Officieel partner van EVVA, ASSA ABLOY en ABUS; monteurs PKVW-gecertificeerd; deurdrangers en deurautomaten van GU.

## Pagina's

{regels}
## Contact

- Telefoon: {TEL_TONEN}
- E-mail: {MAIL}
- Adres: {STRAAT}, {POSTCODE} {PLAATS}
- Bereikbaar: {OPENING_TEKST}
- Bezoek aan de vestiging: {BEZOEKADRES}; inventarisatie altijd op locatie bij de klant
"""
    (DIST / "llms.txt").write_text(llms, encoding="utf-8")
    _LASTMOD_PAD.write_text(json.dumps(_LASTMOD, indent=1, ensure_ascii=False), encoding="utf-8")

CONTENT = ["home", "toegangscontrole", "elektronische_sloten", "evva_xesar", "motorcilinder", "sluitplan", "service_en_beheer",
           "salto", "kosten", "duurzaamheid", "werkgebied", "over_ons", "contact", "bedankt", "privacy"]   # volgorde = volgorde in llms.txt

def main():
    assets()
    sys.path.insert(0, str(ROOT / "content"))
    for naam in CONTENT:
        importlib.import_module(naam).bouw()
    vierhonderdvier()
    sitemap_robots_llms()
    print(f"Gebouwd: {len(_PAGINAS)} pagina's naar dist/ ({VANDAAG.isoformat()})")
    if _ONTBREKEND:
        print("Foto's die INPUT.md nog niet levert (blok weggelaten): " + ", ".join(sorted(set(_ONTBREKEND))))

if __name__ == "__main__":
    main()
