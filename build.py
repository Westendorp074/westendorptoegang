#!/usr/bin/env python3
"""westendorptoegang.nl — statische site-generator.

Werkwijze: feiten uit INPUT.md staan in het CONFIG-blok hieronder; pagina's staan als data in content/;
`python build.py` schrijft alles naar dist/. HTML in dist/ nooit met de hand bewerken.

Regels (CLAUDE.md §1): een veld [[INVULLEN: ...]] blijft letterlijk staan tot Lars het invult.
check.py faalt zolang zo'n veld in dist/ voorkomt; die pagina gaat niet live.
"""
import sys, re, json, html, shutil, hashlib, pathlib, datetime, importlib
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
VESTIGINGSNR  = INV("12-cijferig vestigingsnummer")                 # INPUT §A1, alleen in schema als ingevuld
BTW           = ""                                                  # INPUT §A1 optioneel; leeg = niet tonen
MOEDER        = "Westendorp Slotenspecialist"                       # zusterbedrijf; alleen genoemd op /over-ons/ (Lars, 20-09-2026)
MOEDER_URL    = "https://www.westendorpslotenspecialist.nl/"
MOEDER_SINDS  = INV("jaartal start Westendorp, 1995 of 1985")       # INPUT §C3 (aanname 1995; Almelo-CONFIG zegt 1985 voor het bedrijf)
# Lars, chat 20-09-2026: het woord "slotenmaker" komt op deze site niet voor (check.py bewaakt dat); hoofdmerk is EVVA,
# Salto plaatsen wij niet, maar onderhouden en breiden wij wel uit; klanten komen niet langs, wij komen op locatie.
# Westendorp Toegangscontrole is onderdeel van Westendorp Groep VOF (niet van Slotenspecialist). Particulieren en
# autosleutels worden nergens genoemd, behalve één zin op /over-ons/ over de verhouding tot het zusterbedrijf.

STRAAT        = INV("straat en huisnummer, BAG-spelling")           # INPUT §A2
POSTCODE      = INV("postcode")                                     # INPUT §A2
PLAATS        = "Enschede"
REGIO         = "Overijssel"
LAT, LON      = None, None                                          # INPUT §A2: [[INVULLEN: lat, lon]] — None = geo weglaten
TEL_TONEN     = "053 478 42 45"                                     # INPUT §A2, Lars chat 20-09-2026 (zelfde nummer als de hoofdsite)
TEL_LINK      = "+31534784245"
MAIL          = "info@westendorptoegang.nl"                         # INPUT §A2 (aanname)
OPENING_TEKST = "maandag tot en met vrijdag 08:00–17:00 " + INV("openingstijden bevestigen of corrigeren")
OPENING_SCHEMA = [("Monday", "08:00", "17:00"), ("Tuesday", "08:00", "17:00"), ("Wednesday", "08:00", "17:00"),
                  ("Thursday", "08:00", "17:00"), ("Friday", "08:00", "17:00")]   # aanname INPUT §A2
STORING_BUITEN_KANTOORTIJD = INV("storingen buiten kantoortijd: alleen met servicecontract / altijd / niet")
BEZOEKADRES   = False                                               # chat 20-09-2026: geen bezoekadres, wij komen op locatie

GOOGLE_PROFIEL = INV("Google Maps-URL Bedrijfsprofiel")              # INPUT §A3
LINKEDIN       = INV("LinkedIn-URL")                                 # INPUT §A3
ANDERE_PROFIELEN = []                                                # INPUT §A3 optioneel

# Aanbod (INPUT §B1). Diensten zonder ja/nee staan als placeholder in de tekst waar ze genoemd worden.
DIENSTEN_ONBEVESTIGD = {
    "wandlezers": INV("wandlezers met elektrische sluitplaat: ja/nee"),
    "beheer": INV("beheer en programmering: doen wij / leren wij de klant / beide"),
    "onderhoud": INV("onderhoud en servicecontracten: ja/nee"),
    "storingsdienst": INV("storingsdienst: ja/nee"),
    "overnemen": INV("uitbreiden of overnemen van systemen van andere installateurs: ja/nee"),
    "koppelingen": INV("koppelingen: welke wel (intercom, alarm, tijdregistratie, kluis, lift)"),
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

# Merken (INPUT §B4)
MERKEN = {
    "salto": {"naam": "Salto", "lijnen": "", "partner": "", "logo_ok": ""},   # chat 20-09-2026: niet plaatsen, wel onderhoud en uitbreiding van bestaande Salto-systemen
    "xesar": {"naam": "EVVA Xesar", "lijnen": INV("Xesar-lijnen: cilinders, beslag, wandlezers, versie"), "partner": INV("EVVA-partnerstatus, exacte benaming"), "logo_ok": INV("EVVA-logo mag: ja/nee")},
    "emzy":  {"naam": "EVVA EMZY", "lijnen": "motorcilinder", "partner": INV("EVVA-partnerstatus, exacte benaming"), "logo_ok": INV("EVVA-logo mag: ja/nee")},
    "mechanisch": {"naam": INV("merk en systeem mechanisch sluitsysteem, bijv. EVVA 4KS/ICS"), "lijnen": "", "partner": "", "logo_ok": ""},
}
AIRKEY = INV("EVVA AirKey: ja/nee")

# Richtprijzen (INPUT §B5), excl. btw. Zonder ingevulde waarden gaat /kosten/ niet live.
PRIJZEN = {
    "beslag":         (INV("vanaf"), INV("tot"), INV("wat zit erin")),   # elektronisch beslag per deur, geplaatst
    "cilinder_xesar": (INV("vanaf"), INV("tot"), INV("wat zit erin")),
    "emzy":           (INV("vanaf"), INV("tot"), INV("wat zit erin")),
    "wandlezer":      (INV("vanaf"), INV("tot"), INV("wat zit erin")),
    "software":       (INV("vanaf"), INV("tot"), INV("wat zit erin")),
    "infrezen":       (INV("vanaf"), INV("tot"), INV("wat zit erin")),
    "mech_cilinder":  (INV("vanaf"), INV("tot"), INV("wat zit erin")),
    "servicecontract":(INV("vanaf"), INV("tot"), INV("wat zit erin")),
}
REKENVOORBEELDEN = [("Klein kantoor", INV("rekenvoorbeeld klein kantoor")), ("School", INV("rekenvoorbeeld school")), ("Zorglocatie", INV("rekenvoorbeeld zorglocatie"))]
INVENTARISATIE_GRATIS = True                                         # INPUT §B5 aanname
PRIJS_DISCLAIMER = "Richtprijs, definitieve prijs na inventarisatie."

# Proces en beloftes (INPUT §B6)
REACTIE_AANVRAAG   = INV("reactie op een aanvraag binnen, bijv. 1 werkdag")
INVENTARISATIE_BINNEN = INV("inventarisatie ingepland binnen")
OFFERTE_BINNEN     = INV("offerte binnen")
DOORLOOPTIJD       = INV("doorlooptijd van akkoord tot installatie")
UREN_PER_DEUR      = INV("installatie per deur, gemiddeld aantal uren")
GARANTIE           = INV("garantie op montage en materiaal")
REACTIE_STORING    = INV("reactietijd bij storing, met en zonder contract")
CONTRACTVORMEN     = INV("contractvormen")

SECTOREN = ["kantoren", "zorg", "onderwijs"]                          # INPUT §B7 aanname; pagina's pas in fase 2
CERTIFICATEN = INV("certificaten en keurmerken, exacte namen, of 'geen'")   # INPUT §B9

# Feiten in het kort (INPUT §C3)
TOEGANG_SINDS   = INV("jaartal start elektronische toegangscontrole")
AANTAL_DEUREN   = INV("aantal geplaatste deuren of systemen, ruwweg")
AANTAL_MONTEURS = INV("aantal monteurs")
WERKPLAATS      = INV("eigen werkplaats: ja, waar")
VESTIGINGEN_MOEDER = "Enschede (winkel, Wesselernering 32) en Hengelo (Oldenzaalsestraat 553)"

# Adviseur (INPUT §C4): staat op elke pagina naast het formulier.
ADVISEUR = {"naam": INV("naam adviseur"), "functie": "adviseur toegangscontrole", "foto": None,
            "tel_tonen": INV("direct nummer adviseur"), "tel_link": INV("direct nummer adviseur in +31-notatie"),
            "sinds": INV("adviseur sinds")}

# Conversie (INPUT §E)
CTA            = "Plan een gratis inventarisatie"                     # INPUT §E1 aanname
WHATSAPP       = ""                                                   # INPUT §E1 optioneel; leeg = geen WhatsApp
WEB3FORMS_KEY  = INV("Web3Forms access key")                          # INPUT §E2
FORM_MAILBOX   = INV("mailbox aanvragen")                             # INPUT §E2 (alleen in privacy/README)
BEDANKT_TEKST  = INV("tekst bedanktpagina: wat gebeurt er nu")        # INPUT §E2
GOOGLE_TAG_ID  = INV("Google-tag ID, G-… of AW-…")                    # INPUT §E3
ADS_LABEL_FORM = ""                                                   # INPUT §E3, "AW-xxx/label"; leeg = geen Ads-conversie
ADS_LABEL_TEL  = ""
SC_VERIFICATIE = ""                                                   # INPUT §E3 Search Console meta-tag inhoud
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

def sectie(kop, inhoud, wit=False, lijn=False, kop_id=None, extra=""):
    kl = " ".join(k for k in ["sectie--wit" if wit else "", "sectie--lijn" if lijn else ""] if k)
    kl = f' class="{kl}"' if kl else ""
    hid = f' id="{kop_id}"' if kop_id else ""
    kop_html = f"<h2{hid}>{kop}</h2>" if kop else ""
    return f'<section{kl}><div class="wrap">{kop_html}{inhoud}{extra}</div></section>'

def stappen(items):
    """Genummerde stappen (het is een volgorde): [(kop, tekst), ...]"""
    return '<ol class="stappen">' + "".join(f"<li><h3>{k}</h3><p>{t}</p></li>" for k, t in items) + "</ol>"

def faqblok(items, kop="Veelgestelde vragen"):
    binnen = "".join(f'<details><summary>{esc(v)}</summary><div class="antwoord">{a if a.startswith("<") else "<p>"+a+"</p>"}</div></details>' for v, a in items)
    return sectie(kop, f'<div class="faq rooster"><div class="k8">{binnen}</div></div>') if False else \
        f'<section><div class="wrap"><div class="rooster"><div class="k8"><h2>{kop}</h2><div class="faq">{binnen}</div></div></div></div></section>'

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
            wp = uit / f"{bronpad.stem}-{w}.webp"
            kopie.save(wp, "WEBP", quality=80, method=6)
            av = uit / f"{bronpad.stem}-{w}.avif"
            try:
                kopie.save(av, "AVIF", quality=60)
                if av.stat().st_size > wp.stat().st_size * 0.8:
                    av.unlink(); avif_ok = False
            except Exception:
                avif_ok = False
        return b0, h0, avif_ok

_BEELDCACHE = {}
def beeld(bestand, alt, onderschrift=None, lazy=True, sizes="(min-width: 900px) 40vw, 100vw", klas=""):
    """Eigen foto uit static/img/bron/<bestand>. Ontbreekt de foto: blok weglaten en melden."""
    bronpad = BRON / bestand
    if not bronpad.exists():
        _ONTBREKEND.append(bestand)
        return ""
    if bestand not in _BEELDCACHE:
        _BEELDCACHE[bestand] = _verwerk(bronpad)
    b0, h0, avif_ok = _BEELDCACHE[bestand]
    stem = bronpad.stem
    maten = [w for w in _MATEN if w <= b0 or w == _MATEN[0]]
    w1 = maten[0]; h1 = round(h0 * min(w1, b0) / b0)
    srcset = lambda ext: ", ".join(f"/static/img/{stem}-{w}.{ext} {min(w, b0)}w" for w in maten)
    laad = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    img = (f'<img src="/static/img/{stem}-{w1}.webp" srcset="{srcset("webp")}" sizes="{sizes}" '
           f'width="{min(w1, b0)}" height="{h1}" alt="{esc(alt)}"{laad}>')
    if avif_ok:
        img = f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">{img}</picture>'
    kl = f' class="{klas}"' if klas else ""
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
        "knowsAbout": ["Toegangscontrole", "EVVA Xesar", "EVVA EMZY", "Motorcilinders", "Sluitplannen", "Elektronische sloten", "Salto onderhoud"],
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

def webpage_ld(pad, titel, omschrijving, typ="WebPage", datum=None):
    d = {"@type": typ, "@id": SITE + pad + "#webpage", "url": SITE + pad, "name": titel, "description": omschrijving,
         "inLanguage": "nl-NL", "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": ORG_ID}}
    if datum: d["dateModified"] = datum
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
NAV = [("Toegangscontrole", "/toegangscontrole/"), ("Elektronische sloten", "/elektronische-sloten/"), ("EVVA Xesar", "/evva-xesar/"),
       ("Motorcilinder", "/motorcilinder/"), ("Sluitplan", "/sluitplan/"), ("Kosten", "/kosten/"), ("Service", "/service-en-beheer/"),
       ("Over ons", "/over-ons/"), ("Contact", "/contact/")]

_ICOON_BEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
_ICOON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

def header(pad):
    items = "".join(f'<li><a href="{u}"{" aria-current=\"page\"" if u == pad else ""}>{esc(n)}</a></li>' for n, u in NAV)
    return f'''<header class="kop"><div class="wrap">
<a class="logo" href="/" aria-label="{esc(NAAM)}, naar de homepage"><img src="/static/img/logo/logo.svg" alt="{esc(NAAM)}" width="2053" height="647"></a>
<nav class="nav" id="nav" aria-label="Hoofdmenu"><ul>{items}</ul></nav>
<div class="kop__acties"><a class="bel" href="tel:{esc(TEL_LINK)}">{_ICOON_BEL}<span>{esc(TEL_TONEN)}</span><span class="visueel-verborgen">Bel {esc(NAAM)}</span></a>
<button class="menu-knop" id="menu-knop" type="button" aria-expanded="false" aria-controls="nav">{_ICOON_MENU}<span>Menu</span></button></div>
</div></header>'''

def footer():
    diensten = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in DIENSTEN_NAV + [("Kosten", "/kosten/")])
    over = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in [("Over ons", "/over-ons/"), ("Werkgebied", "/werkgebied/"), ("Contact", "/contact/"), ("Privacy", "/privacy/")])
    btw = f"<p>Btw-nummer {esc(BTW)}.</p>" if BTW else ""
    profiel = f'<li><a href="{esc(GOOGLE_PROFIEL)}" rel="noopener">Google Bedrijfsprofiel</a></li>' if not placeholder(GOOGLE_PROFIEL) else ""
    linkedin = f'<li><a href="{esc(LINKEDIN)}" rel="noopener">LinkedIn</a></li>' if not placeholder(LINKEDIN) else ""
    cookies = '<li><button type="button" data-consent-open>Cookie-instellingen</button></li>' if TAG_ACTIEF else ""
    return f'''<footer class="voet"><div class="wrap">
<div class="rooster">
<div class="k4"><h2>Diensten</h2><ul>{diensten}</ul></div>
<div class="k4"><h2>Contact</h2><address><p>{esc(NAAM)}<br>{esc(STRAAT)}<br>{esc(POSTCODE)} {esc(PLAATS)}</p>
<p><a href="tel:{esc(TEL_LINK)}">{esc(TEL_TONEN)}</a><br><a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a></p>
<p>Bereikbaar {esc(OPENING_TEKST)}.</p></address></div>
<div class="k4"><h2>Over</h2><ul>{over}{profiel}{linkedin}{cookies}</ul></div>
</div>
<div class="onderdeel"><p>{esc(NAAM)} is onderdeel van {esc(RECHTSPERSOON)}, KvK {esc(KVK)}, {esc(PLAATS)}.</p>{btw}</div>
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
    intro = intro or ("Vul het formulier in; " + esc(ADVISEUR["naam"]) + " neemt contact met u op binnen " + esc(REACTIE_AANVRAAG) + ". Alleen naam, plaats en een telefoonnummer of e-mailadres zijn verplicht.")
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
    return f'''<section class="sectie--wit" id="aanvraag" data-gedeeld><div class="wrap"><div class="rooster">
<div class="k8"><h2>{esc(kop)}</h2><p class="tekst">{intro}</p>{velden}</div>
<div class="k4">{adviseurblok()}</div>
</div></div></section>'''

def adviseurblok():
    a = ADVISEUR
    foto = beeld(a["foto"], f"{a['naam']}, {a['functie']} bij {NAAM}", sizes="120px") if a["foto"] else ""
    feiten = [f"Reactie binnen {esc(REACTIE_AANVRAAG)}",
              "Inventarisatie op locatie" + (", zonder kosten" if INVENTARISATIE_GRATIS else ""),
              f"Deuren, sloten en beslag sinds {esc(MOEDER_SINDS)}, elektronische toegangscontrole sinds {esc(TOEGANG_SINDS)}"]
    return f'''<div class="adviseur">{foto}<p class="naam">{esc(a["naam"])}</p><p class="functie">{esc(a["functie"].capitalize())}</p>
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
    graph = [bedrijf_ld(), website_ld(), webpage_ld(pad, titel, omschrijving, paginatype, datum), kruimels_ld(kruimelpad)]
    graph += list(extra_ld)
    if faq: graph.append(faq_ld(faq))
    volledige_titel = titel if pad == "/" else f"{titel} | {NAAM}" if len(f"{titel} | {NAAM}") <= 60 else titel
    verificatie = (f'<meta name="google-site-verification" content="{esc(SC_VERIFICATIE)}">\n' if SC_VERIFICATIE else "") + \
                  (f'<meta name="msvalidate.01" content="{esc(BING_VERIFICATIE)}">\n' if BING_VERIFICATIE else "")
    waarden = {
        "titel": esc(volledige_titel), "omschrijving": esc(omschrijving), "canonical": SITE + pad, "sitenaam": esc(NAAM),
        "robots": '<meta name="robots" content="noindex, nofollow">\n' if noindex else "", "verificatie": verificatie,
        "og_beeld": SITE + (og_beeld or "/static/img/og-standaard.png"),
        "css": _ASSETS["css"], "js": _ASSETS["js"], "tag": tag_html(), "jsonld": ld_script(graph),
        "header": header(pad), "body": volledige_body, "footer": footer(), "consent": consent_html(),
        "config_js": json.dumps({"tagActief": TAG_ACTIEF, "web3formsKey": WEB3FORMS_KEY, "adsLabelForm": ADS_LABEL_FORM,
                                 "adsLabelTel": ADS_LABEL_TEL, "cta": CTA, "mail": MAIL}, ensure_ascii=False),
    }
    uit = DIST / pad.strip("/") / "index.html" if pad != "/" else DIST / "index.html"
    uit.parent.mkdir(parents=True, exist_ok=True)
    uit.write_text(_vul(_template(), waarden), encoding="utf-8")
    _PAGINAS.append((pad, titel, llms, noindex, datum))

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
        "background_color": "#1C1C1C", "theme_color": "#1C1C1C", "icons": [{"src": "/static/img/logo/icoon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False), encoding="utf-8")

def vierhonderdvier():
    links = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in [("Toegangscontrole", "/toegangscontrole/"), ("Wat kost toegangscontrole", "/kosten/"), ("EVVA Xesar", "/evva-xesar/"), ("Motorcilinder", "/motorcilinder/"), ("Contact", "/contact/")])
    body = f'<section class="hero"><div class="wrap"><div class="rooster"><div class="k8"><h1>Deze pagina bestaat niet</h1><p>Het adres klopt niet meer of is verkeerd getypt. Dit zijn de pagina\'s waar de meeste bezoekers naar zoeken.</p><ul class="lijst-links">{links}</ul>{acties()}</div></div></div></section>'
    schrijf("/404/", "Pagina niet gevonden", "De pagina die u zocht bestaat niet op westendorptoegang.nl. Ga verder naar toegangscontrole, wat het kost, EVVA Xesar, motorcilinders of neem contact op.", body, noindex=True, met_formulier=False)
    shutil.move(DIST / "404" / "index.html", DIST / "404.html"); (DIST / "404").rmdir()
    _PAGINAS[:] = [p for p in _PAGINAS if p[0] != "/404/"]

def sitemap_robots_llms():
    index = [(pad, datum) for pad, _, _, noindex, datum in _PAGINAS if not noindex]
    urls = "".join(f"<url><loc>{SITE}{pad}</loc><lastmod>{datum}</lastmod></url>" for pad, datum in index)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "PerplexityBot", "Google-Extended", "Bingbot", "Applebot"]
    robots = "User-agent: *\nAllow: /\nDisallow: /bedankt/\n\n" + "".join(f"User-agent: {b}\nAllow: /\nDisallow: /bedankt/\n\n" for b in bots) + f"Sitemap: {SITE}/sitemap.xml\n"
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    regels = "".join(f"- [{titel}]({SITE}{pad}): {llms}\n" for pad, titel, llms, noindex, _ in _PAGINAS if llms and not noindex)
    plaatsen = ", ".join(n for n, _, _, _ in WERKGEBIED)
    llms = f"""# {NAAM}

> {NAAM} levert en installeert elektronische toegangscontrole (EVVA Xesar, EVVA EMZY-motorcilinders) en sluitplannen voor bedrijven en instellingen in Oost-Nederland, altijd op locatie bij de klant, vanuit {PLAATS}. Bestaande Salto-systemen onderhoudt en breidt het bedrijf uit. Werkgebied: {WERKGEBIED_REGEL}, onder meer {plaatsen}. Onderdeel van {RECHTSPERSOON}, KvK {KVK}; actief in deuren, sloten en beslag sinds {MOEDER_SINDS}.

## Pagina's

{regels}
## Contact

- Telefoon: {TEL_TONEN}
- E-mail: {MAIL}
- Adres: {STRAAT}, {POSTCODE} {PLAATS}
- Bereikbaar: {OPENING_TEKST}
"""
    (DIST / "llms.txt").write_text(llms, encoding="utf-8")
    _LASTMOD_PAD.write_text(json.dumps(_LASTMOD, indent=1, ensure_ascii=False), encoding="utf-8")

CONTENT = ["home"]   # volgorde = volgorde in llms.txt; nieuwe pagina's hier toevoegen

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
