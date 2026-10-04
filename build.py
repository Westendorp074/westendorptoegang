#!/usr/bin/env python3
"""westendorptoegang.nl — statische site-generator.

Werkwijze: feiten uit INPUT.md staan in het CONFIG-blok hieronder; pagina's staan als data in content/;
`python build.py` schrijft alles naar dist/. HTML in dist/ nooit met de hand bewerken.

Regels (CLAUDE.md §1): een veld [[INVULLEN: ...]] blijft letterlijk staan tot Lars het invult.
check.py faalt zolang zo'n veld in dist/ voorkomt; die pagina gaat niet live.
"""
import sys, re, json, html, shutil, hashlib, pathlib, datetime, importlib
import straatbeeld   # vlakke straatscènes in code (richting dormakaba, Lars 28-09-2026); isometrie.py blijft staan als terugvaloptie
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
WERKGEBIED_REGEL = "heel Oost-Nederland, daarbuiten in overleg"   # Lars, 04-10-2026: niet meer op rijtijd formuleren
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
HYBRIDE = True   # Lars, 24-09-2026: sleutel, pas, tag/druppel en telefoon door elkaar in één systeem; mobiel vaker noemen
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
# Sectoren op de home en op /toegangscontrole/: (sleutel, kop zonder 'toegangscontrole', wat wij daar oplossen, wat er past). Volgorde van Lars (23-09-2026).
SECTOREN_LIJST = [
    ("zorg", "Zorg",
     "Ziekenhuizen, verpleeghuizen, huisartsenposten en jeugdzorg: medicijnruimtes, cliëntkamers en personeelsingangen met een toegangspas per medewerker. Bij personeelswisselingen trekt u de pas in; cilinders vervangen is niet meer nodig.",
     "Elektronisch beslag op cliëntkamers en medicijnruimtes, een wandlezer op de personeelsingang en rapportage per deur van wie wanneer binnen was."),
    ("woningcorporatie", "Woningcorporaties",
     "Portiekflats, galerijflats en seniorencomplexen: gemeenschappelijke entrees, bergingen, liftmachinekamers en technische ruimtes in tientallen complexen. Bij een huurderswissel blokkeert u de oude pas; de eigen onderhoudsdienst en aannemers krijgen toegang met een tijdslot.",
     "Wandlezers op de entrees, elektronische cilinders op bergingen en technische ruimtes, tijdelijke rechten voor ketenpartners en centraal beheer over alle complexen."),
    ("overheid", "Overheid",
     "Gemeentehuizen, gemeentewerven, wijkcentra en sporthallen: één toegangscontrolesysteem voor alle gemeentelijke gebouwen, met zones per afdeling en een logboek voor de accountant. Ook voor semi-overheid en gemeenschappelijke regelingen.",
     "Xesar online op de publieksingang zodat de receptie of bode op afstand opent, elektronisch beslag op kantoren en werven, en mechanische cilinders uit hetzelfde sluitplan op techniekruimtes."),
    ("onderwijs", "Onderwijs",
     "Basisscholen, middelbare scholen, mbo en kinderopvang: veel gebruikers, verhuur van lokalen en verloren sleutels. Elektronische sloten met zones en tijdsloten per groep; een kwijtgeraakte pas blokkeert de conciërge zelf.",
     "Zones per bouwdeel, tijdsloten voor verhuur van gymzaal en aula, en een pas per leerkracht, conciërge en huurder."),
    ("vve", "VvE & Vastgoed",
     "Appartementencomplexen, verhuurde woningen en bedrijfsverzamelgebouwen: de eigenaar of beheerder regelt de toegang tot entree, bergingen en fietsenstalling met een pas, druppel of de telefoon per woning of huurder. Bij een verhuizing blokkeert u de oude pas; sleutelbeheer zonder kopieën die niet terugkomen.",
     "Een wandlezer op de gemeenschappelijke entree, elektronische cilinders op bergingen en stalling, en toegangsbeheer door de VvE-beheerder of vastgoedbeheerder in de software."),
    ("kantoren", "Kantoren",
     "Kantoorpanden waar u zelf zit: een pas of de telefoon per medewerker, flexwerken en een verhuizing zonder nieuw sluitplan. Rechten beheert u zelf in het toegangscontrolesysteem, ook voor schoonmaak en leveranciers.",
     "Een wandlezer op de entree, elektronisch beslag op kantoren en vergaderruimtes, en rechten per afdeling die u zelf bijwerkt."),
    ("industrie", "Industrie & Logistiek",
     "Productiehallen, distributiecentra en bedrijventerreinen: ploegendiensten, zonering per afdeling en rapportage van wie waar was, voor verzekeraar en auditor. Elektronische toegangscontrole die u per deur uitbreidt, van kantoor tot laaddock.",
     "Online lezers op de hoofdingang en het laaddock, offline beslag op kantoren en magazijn; een koppeling met tijdregistratie of alarm bekijken wij in overleg."),
    ("retail", "Retail",
     "Winkels, supermarkten, winkelcentra en filiaalbedrijven: wisselend personeel, magazijn en kantoor achter de winkel, en meerdere vestigingen onder één toegangsbeheer. Een toegangspas per medewerker; een verloren pas blokkeert de filiaalmanager zelf.",
     "Elektronisch beslag op magazijn, kantoor en kluisruimte, een lezer op de personeelsingang, beheer per filiaal of centraal vanuit het hoofdkantoor."),
    ("horeca", "Horeca",
     "Restaurants, cafés, lunchzaken en cateraars: veel personeelswissels, een kelder of voorraadruimte met dure inkoop en leveranciers die vóór openingstijd binnen moeten. Een pas per medewerker in plaats van een sleutelbos; wie uit dienst gaat, blokkeert u dezelfde dag.",
     "Elektronisch beslag op kantoor, kelder en voorraadruimte, een lezer op de personeelsingang met een tijdslot voor leveranciers, en beheer door de bedrijfsleider zelf."),
    ("verenigingen", "Sport & Verenigingen",
     "Sportparken, sporthallen, clubhuizen en buurthuizen met vrijwilligers en wisselende gebruikers: tijdsloten voor trainingen, avonden en weekenden, en een toegangspas die u intrekt als iemand stopt. Geen sleutelbos meer bij de kantinevrijwilliger.",
     "Een pas of tag per vrijwilliger met tijdslot, elektronische cilinders op clubhuis, kleedkamers en materiaalhok, beheer door één bestuurslid."),
    ("hotel", "Hotels",
     "Hotels, B&B's en short stay: een kamerpas of digitale sleutel op de telefoon per gast, die bij het uitchecken vanzelf verloopt, passen voor housekeeping en technische dienst, en de personeelsingang, het magazijn en de technische ruimtes alleen voor wie daar moet zijn. Neemt een gast de pas mee of raakt hij hem kwijt, dan blokkeert de receptie hem direct.",
     "Kamerpassen met einddatum, elektronisch beslag op kamers en personeelsruimtes, een lezer op de personeelsingang en beheer vanuit de receptie."),
    ("recreatie", "Recreatieparken",
     "Vakantieparken en campings: huisjes, sanitairgebouwen, zwembad en slagboom met toegang per boeking. Gasten wisselen elke week; de receptie stuurt de digitale sleutel naar de telefoon van de gast of geeft een pas uit, zonder sleuteloverdracht.",
     "Toegang per boeking op huisjes en sanitairgebouwen, de slagboom of poort aan een lezer, beheer vanuit de receptie."),
    ("anders", "Anders",
     "Staat uw sector er niet bij, zoals een kerk, museum, laboratorium, datacenter of een pand dat nergens in past: dan kijken wij per pand wat er nodig is. Elk gebouw heeft deuren, gebruikers en sleutels die kwijtraken.",
     "Dat bepalen wij samen bij de inventarisatie op locatie: van één elektronische cilinder tot een compleet systeem, op de deuren die er al zitten."),
]
CERTIFICATEN = "officieel partner van EVVA, ASSA ABLOY en ABUS; monteurs PKVW-gecertificeerd (Politiekeurmerk Veilig Wonen); getraind door EVVA en door GU voor deurdrangers en deurautomaten"   # INPUT §B9 (Lars, 20/21-09-2026)
PKVW = "Onze monteurs zijn PKVW-gecertificeerd (Politiekeurmerk Veilig Wonen) en gespecialiseerd in het vernieuwen van oudere panden met toegangscontrole, zonder de bestaande deuren te vervangen."
DEURDRANGERS = "GU"                                                  # INPUT §B1: deurdrangers en deurautomaten van GU (Lars, 20-09-2026)

# Feiten in het kort (INPUT §C3)
TOEGANG_SINDS   = "1995"                                             # Lars, 21-09-2026
# Aantal deuren en monteurs: bewust niet op de site (Lars, 21-09-2026).
WERKPLAATS      = "Enschede en Hengelo"                              # Lars, 21-09-2026: werkplaats en uitrijbasis in beide; Hengelo is de servicevestiging met kantoor
VESTIGINGEN_MOEDER = "Enschede (winkel, Wesselernering 32) en Hengelo (Oldenzaalsestraat 553)"

# Adviseur (INPUT §C4): staat op elke pagina naast het formulier.
ADVISEURS = [  # Lars, 21-09-2026: twee adviseurs, zelfde nummer; volledige namen en eigenaarschap (Lars, 04-10-2026)
    {"naam": "Lars Westendorp", "functie": "eigenaar en adviseur toegangscontrole", "foto": "adviseur-lars.jpg", "tel_tonen": "053 478 42 45", "tel_link": "+31534784245"},   # portret v2, staand 4:5 (23-09-2026)
    {"naam": "Nick Westendorp", "functie": "eigenaar en adviseur toegangscontrole", "foto": "adviseur-nick.jpg", "tel_tonen": "053 478 42 45", "tel_link": "+31534784245"},
]
ADVISEUR = ADVISEURS[0]
ADVISEUR_NAMEN = " of ".join(a["naam"].split()[0] for a in ADVISEURS)          # "Lars of Nick", voor lopende zinnen

# Conversie (INPUT §E)
# Duurzaamheid (Lars, 22-09-2026): ABUS Magtec in eigen profiel; cijfers van ABUS/ClimatePartner, met bron op /duurzaamheid/.
DUURZAAM = [
    ("46 procent minder CO₂", "De ABUS Magtec-cilinder veroorzaakt 46 procent minder broeikasgasemissies dan een conventionele profielcilinder, berekend door ClimatePartner over de levenscyclus (gebruiksfase niet meegerekend)."),
    ("Loodvrij geproduceerd", "Bij de productie van Magtec-cilinders wordt geen lood gebruikt; het verschil in uitstoot zit vooral in grondstoffen en productie."),
    ("SKG*** en uit voorraad", "Hoogste niveau op DIN EN 1303 en SKG***-gecertificeerd. Wij voeren Magtec in ons eigen profiel en leveren uit voorraad."),
]
DUURZAAM_ELEKTRONISCH = ("Geen sloten vervangen bij sleutelverlies",
    "Raakt bij een mechanisch sluitplan een sleutel kwijt, dan moeten cilinders worden vervangen en sleutels opnieuw gemaakt. Bij elektronische toegangscontrole blokkeert u de pas in de software; "
    "het slot blijft zitten. Er worden geen extra sleutels bijgemaakt en er wordt geen messing of staal verbruikt voor cilinders en sleutels die alleen nodig zijn omdat er een sleutel zoek is.")   # Lars, 23-09-2026
HEADER_LICHT   = True   # witte header met zwart woordmerk (test, Lars 22-09-2026); False = antraciet met logo-zwarte-achtergrond
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
OG_STANDAARD = "/static/img/og-standaard-1200x630.png"   # deelbeeld uit het logopakket (Lars, 23-09-2026)

def leeg_dist():
    """Maakt dist leeg. OneDrive houdt net aangemaakte mappen soms even vast (WinError 5); daarom een paar keer proberen."""
    import time
    for poging in range(6):
        try:
            shutil.rmtree(DIST); return
        except PermissionError:
            time.sleep(0.5 * (poging + 1))
    shutil.rmtree(DIST, ignore_errors=True)   # laatste poging: mappen die blijven staan zijn leeg en worden overschreven
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
    # bellen is een knop, geen tekstlink (Lars, 23-09-2026)
    return (f'<p class="acties" data-gedeeld>{cta_knop(tekst, href)}'
            f'<a class="knop knop--tweede knop--bel" href="tel:{esc(TEL_LINK)}" data-cta="bel">{_ICOON_BEL}<span>Bel {esc(TEL_TONEN)}</span></a></p>')

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

def chat_widget():
    """Contactwidget rechtsonder (Lars, 28-09-2026, naar Leadinfo-voorbeeld van een concurrent maar dan eigen bouw):
    geen externe chatdienst, geen tracking, geen cookies. Eigen <style> en <script> zodat de budgetten van
    site.css (40 KB) en site.js (15 KB) onaangetast blijven; de foto's laden pas als het paneel opengaat."""
    # strakke gezichtsuitsnede van Nick voor de widgetkop (uit de bronfoto, alleen hoofd en schouders)
    # versiehash in de naam: /static/ wordt lang gecachet, dus een nieuwe uitsnede moet een nieuwe naam krijgen
    if "gezicht" not in _ASSETS:
        import io
        from PIL import Image
        foto = Image.open(BRON / "adviseur-nick.jpg").convert("RGB").crop((100, 0, 820, 720))   # hoofd, schouders en armen
        buf = io.BytesIO(); foto.resize((160, 160), Image.LANCZOS).save(buf, "WEBP", quality=84)
        naam = f"nick-gezicht-{hashlib.md5(buf.getvalue()).hexdigest()[:8]}-160.webp"
        (DIST / "static" / "img" / naam).write_bytes(buf.getvalue())
        _ASSETS["gezicht"] = f"/static/img/{naam}"
    gezicht = _ASSETS["gezicht"]
    stijl = """<style>
.wchat{position:fixed;right:18px;bottom:18px;z-index:60;font-family:var(--font)}
.wchat__knop{position:relative;width:60px;height:60px;border:0;border-radius:50%;background:var(--primair-donker);color:#fff;cursor:pointer;box-shadow:0 10px 28px rgba(2,41,91,.35);display:flex;align-items:center;justify-content:center;transition:transform .15s}
.wchat__knop:hover{transform:scale(1.06)}
.wchat__knop .wchat__led{position:absolute;right:2px;top:2px;width:13px;height:13px;border-radius:50%;border:2.5px solid #fff}
.wchat--open .wchat__pict-chat,.wchat__pict-kruis{display:none}
.wchat--open .wchat__pict-kruis{display:block}
.wchat__hint{position:absolute;right:0;bottom:74px;width:min(290px,calc(100vw - 40px));display:flex;gap:12px;align-items:flex-start;background:#fff;color:var(--inkt);border:var(--lijndikte) solid var(--lijn);border-radius:14px;padding:13px 34px 13px 13px;box-shadow:0 18px 44px rgba(2,41,91,.24),0 3px 9px rgba(2,41,91,.1);opacity:0;pointer-events:none;transform:translateY(8px);transition:opacity .35s,transform .35s;cursor:pointer}
.wchat--hint .wchat__hint{opacity:1;pointer-events:auto;transform:none}
.wchat__hint img{width:46px;height:46px;border-radius:50%;object-fit:cover;flex:none;border:2px solid var(--accent)}
.wchat__hint strong{display:block;font-family:var(--font-kop);font-size:13.5px;margin-bottom:2px}
.wchat__hint p{margin:0;font-size:13.5px;line-height:1.45;color:var(--inkt-zacht)}
.wchat__hint-dicht{position:absolute;right:6px;top:6px;width:22px;height:22px;border:0;border-radius:6px;background:transparent;color:var(--inkt-zacht);font-size:15px;line-height:1;cursor:pointer}
.wchat__hint-dicht:hover{background:#EFEAE2}
.wchat__paneel{position:absolute;right:0;bottom:74px;width:min(340px,calc(100vw - 36px));background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 24px 60px rgba(2,41,91,.30),0 4px 12px rgba(2,41,91,.12);border:var(--lijndikte) solid var(--lijn);transform-origin:bottom right;transition:opacity .25s,transform .25s,display .25s allow-discrete}
.wchat__paneel[hidden]{opacity:0;transform:translateY(8px) scale(.98)}
@starting-style{.wchat__paneel{opacity:0;transform:translateY(8px) scale(.98)}}
.wchat__kop{display:flex;gap:12px;align-items:center;background:var(--primair-donker);color:#fff;padding:14px 16px}
.wchat__fotos{display:flex;flex:none}
.wchat__fotos img{width:74px;height:74px;border-radius:50%;object-fit:cover;border:3px solid #fff;background:#fff}
.wchat__fotos img+img{margin-left:-12px}
.wchat__naam{margin:0;font-family:var(--font-kop);font-size:15px;font-weight:700}
.wchat__statustekst{margin:2px 0 0;display:flex;gap:7px;align-items:center;font-size:12.5px;color:#B9CBE2}
.wchat__led,.wchat__statustekst i{width:8px;height:8px;border-radius:50%;background:#3DBE7A;flex:none}
.wchat--dicht .wchat__led,.wchat--dicht .wchat__statustekst i{background:#8AD6FF}
.wchat__sluit{margin-left:auto;flex:none;width:32px;height:32px;border:0;border-radius:8px;background:rgba(255,255,255,.12);color:#fff;font-size:19px;line-height:1;cursor:pointer}
.wchat__sluit:hover{background:rgba(255,255,255,.22)}
.wchat__welkom{margin:14px 16px 4px;background:var(--papier);border:var(--lijndikte) solid var(--lijn);border-radius:12px 12px 12px 3px;padding:11px 14px;font-size:14.5px;line-height:1.5;color:var(--inkt)}
.wchat__acties{display:grid;gap:8px;padding:12px 16px 4px;margin:0}
.wchat__actie{display:flex;gap:10px;align-items:center;border:var(--lijndikte) solid var(--lijn-2);border-radius:10px;background:#fff;padding:11px 13px;font:600 14px/1.3 var(--font);color:var(--inkt);text-decoration:none;cursor:pointer;text-align:left;transition:border-color .15s,background .15s}
.wchat__actie:hover{border-color:var(--primair);background:#F4F9FE}
.wchat__actie svg{flex:none;color:var(--primair)}
.wchat__actie--bel{background:var(--accent);border-color:var(--accent);color:var(--kop)}
.wchat__actie--bel svg{color:var(--kop)}
.wchat__actie--bel:hover{background:var(--accent-hover);border-color:var(--accent-hover)}
.wchat__form{display:none;padding:4px 16px 0}
.wchat--terugbel .wchat__form{display:block}
.wchat--terugbel .wchat__acties,.wchat--terugbel .wchat__welkom{display:none}
.wchat__form label{display:block;font:600 13px/1.4 var(--font);color:var(--inkt);margin:10px 0 4px}
.wchat__form input{width:100%;box-sizing:border-box;border:var(--lijndikte) solid var(--lijn-2);border-radius:8px;padding:10px 12px;font:400 15px/1.4 var(--font);background:var(--papier)}
.wchat__form input:focus{outline:var(--focus);outline-offset:1px}
.wchat__form .knopregel{display:flex;gap:8px;margin-top:12px}
.wchat__form button{flex:1;border:0;border-radius:8px;padding:11px 12px;font:700 13px/1 var(--font-kop);letter-spacing:.06em;text-transform:uppercase;cursor:pointer}
.wchat__verstuur{background:var(--accent);color:var(--kop)}
.wchat__terug{background:#fff;border:var(--lijndikte) solid var(--lijn-2)!important;color:var(--inkt)}
.wchat__formstatus{margin:10px 0 0;font-size:13.5px;line-height:1.45;color:var(--inkt)}
.wchat__formstatus.goed{color:var(--signaal)}
.wchat__voet{margin:10px 16px 14px;font-size:12px;color:var(--inkt-zacht)}
@media (max-width:480px){.wchat{right:12px;bottom:12px}.wchat__paneel{bottom:70px}}
@media (prefers-reduced-motion:reduce){.wchat *{transition:none!important}}
</style>"""
    telefoon_svg = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5c0 8 7 15 15 15l2-4-4-2-2 2c-3-1-6-4-7-7l2-2-2-4z"/></svg>'
    kalender_svg = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="6" width="16" height="14" rx="2"/><path d="M4 10h16M8 3v4M16 3v4"/></svg>'
    terug_svg = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5c0 8 7 15 15 15l2-4-4-2-2 2c-3-1-6-4-7-7l2-2-2-4z"/><path d="M14 6h7M17.5 2.5v7"/></svg>'
    mail_svg = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'
    chat_svg = '<svg class="wchat__pict-chat" viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-8 8H4l2.2-3.3A8 8 0 1 1 21 12z"/><path d="M8.5 10.5h7M8.5 13.5h4.5"/></svg>'
    kruis_svg = '<svg class="wchat__pict-kruis" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
    script = """<script>(function(){
var w=document.querySelector('[data-wchat]');if(!w)return;
var knop=w.querySelector('.wchat__knop'),paneel=w.querySelector('.wchat__paneel');
var uur=new Date().getHours(),dag=new Date().getDay();
var open=dag>=1&&dag<=5&&uur>=8&&uur<17;
w.classList.toggle('wchat--dicht',!open);
w.querySelector('[data-wchat-status]').textContent=open?'Nu bereikbaar':'Ma t/m vr 08:00–17:00';
w.querySelector('[data-wchat-groet]').textContent=(uur<12?'Goedemorgen!':uur<18?'Goedemiddag!':'Goedenavond!')+' Waarmee kunnen wij u helpen?';
function zet(o){w.classList.toggle('wchat--open',o);paneel.hidden=!o;knop.setAttribute('aria-expanded',o);
  knop.setAttribute('aria-label',o?'Sluit contactvenster':'Contact opnemen');
  if(o){w.classList.remove('wchat--hint');try{localStorage.setItem('wchat-gezien',Date.now())}catch(e){}}}
knop.addEventListener('click',function(){zet(paneel.hidden)});
w.querySelector('.wchat__sluit').addEventListener('click',function(){zet(false);knop.focus()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!paneel.hidden){zet(false);knop.focus()}});
var hint=w.querySelector('[data-wchat-hint]');
w.querySelector('[data-wchat-hintgroet]').textContent=(uur<12?'Goedemorgen!':uur<18?'Goedemiddag!':'Goedenavond!')+' Waarmee kan ik u helpen?';
hint.addEventListener('click',function(e){if(e.target.closest('.wchat__hint-dicht')){w.classList.remove('wchat--hint');try{localStorage.setItem('wchat-gezien',Date.now())}catch(err){};return}zet(true)});
var g=false;try{g=(Date.now()-(+localStorage.getItem('wchat-gezien')||0))<864e5}catch(e){}
if(!g){setTimeout(function(){if(paneel.hidden)w.classList.add('wchat--hint')},4500)}
var vorm=w.querySelector('[data-wchat-form]'),status=w.querySelector('.wchat__formstatus');
w.querySelector('[data-wchat-terugbel]').addEventListener('click',function(){w.classList.add('wchat--terugbel');vorm.querySelector('input').focus()});
w.querySelector('.wchat__terug').addEventListener('click',function(){w.classList.remove('wchat--terugbel')});
vorm.addEventListener('submit',function(e){e.preventDefault();
  var C=window.WT_CONFIG||{},naam=vorm.naam.value.trim(),tel=vorm.telefoon.value.trim();
  if(!naam||!tel){status.textContent='Vul uw naam en telefoonnummer in.';return}
  status.textContent='Versturen…';
  fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},
    body:JSON.stringify({access_key:C.web3formsKey,subject:'Terugbelverzoek via de website',from_name:naam,naam:naam,telefoon:tel,pagina:location.pathname,botcheck:''})})
  .then(function(r){if(!r.ok)throw 0;vorm.querySelector('.knopregel').hidden=true;
    status.className='wchat__formstatus goed';
    status.textContent='Dank u, '+naam+'. '+(dag>=1&&dag<=5&&uur>=8&&uur<16?'Wij bellen u vandaag terug.':'Wij bellen u op de eerstvolgende werkdag terug.')})
  .catch(function(){status.textContent='Versturen lukte niet. Bel ons gerust: TEL_TONEN.'})});
})()</script>"""
    script = script.replace("TEL_TONEN", TEL_TONEN)
    return (f'<div class="wchat" data-wchat>{stijl}'
            f'<div class="wchat__paneel" id="wchat-paneel" role="dialog" aria-label="Contact opnemen" hidden>'
            f'<div class="wchat__kop"><span class="wchat__fotos">'
            f'<img src="{gezicht}" alt="" width="74" height="74" loading="lazy"></span>'
            f'<div><p class="wchat__naam">Nick — {esc(NAAM)}</p>'
            f'<p class="wchat__statustekst"><i></i><span data-wchat-status>Bereikbaar</span></p></div>'
            f'<button type="button" class="wchat__sluit" aria-label="Sluiten">&#215;</button></div>'
            f'<p class="wchat__welkom" data-wchat-groet>Waarmee kunnen wij u helpen?</p>'
            f'<div class="wchat__acties">'
            f'<a class="wchat__actie wchat__actie--bel" href="tel:{esc(TEL_LINK)}">{telefoon_svg}Bel {esc(TEL_TONEN)}</a>'
            f'<a class="wchat__actie" href="/contact/#aanvraag">{kalender_svg}Plan een gratis inventarisatie</a>'
            f'<button type="button" class="wchat__actie" data-wchat-terugbel>{terug_svg}Bel mij terug</button>'
            f'<a class="wchat__actie" href="mailto:{esc(MAIL)}">{mail_svg}Mail {esc(MAIL)}</a></div>'
            f'<form class="wchat__form" data-wchat-form novalidate>'
            f'<label for="wchat-naam">Uw naam</label><input id="wchat-naam" name="naam" type="text" autocomplete="name" required>'
            f'<label for="wchat-tel">Uw telefoonnummer</label><input id="wchat-tel" name="telefoon" type="tel" autocomplete="tel" inputmode="tel" required>'
            f'<div class="knopregel"><button type="button" class="wchat__terug">Terug</button>'
            f'<button type="submit" class="wchat__verstuur">Bel mij terug</button></div>'
            f'<p class="wchat__formstatus" role="status" aria-live="polite"></p></form>'
            f'<p class="wchat__voet">Geen chatbot: u krijgt Nick of een van onze medewerkers.</p></div>'
            f'<div class="wchat__hint" data-wchat-hint role="status"><img src="{gezicht}" alt="" width="46" height="46" loading="lazy">'f'<span><strong>Nick van {esc(NAAM)}</strong><p data-wchat-hintgroet>Waarmee kan ik u helpen?</p></span>'f'<button type="button" class="wchat__hint-dicht" aria-label="Melding sluiten">&#215;</button></div>'
            f'<button type="button" class="wchat__knop" aria-expanded="false" aria-controls="wchat-paneel" aria-label="Contact opnemen">'
            f'{chat_svg}{kruis_svg}<i class="wchat__led" aria-hidden="true"></i></button>'
            f'{script}</div>')

def hero(h1, intro, foto_html="", cta=True, extra="", illustratie=None, kicker=None):
    """Kop van elke pagina: label, H1, answer-first alinea, CTA; rechts een foto of een illustratie."""
    rechts_inhoud = foto_html or (f'<div class="hero__illustratie">{illustratie}</div>' if illustratie else "")
    rechts = f'<div class="k6 hero__rechts{" hero__foto" if foto_html else ""}">{rechts_inhoud}</div>' if rechts_inhoud else ""
    kol = "k6" if rechts_inhoud else "k8"
    return (f'<section class="hero{" hero--foto" if foto_html else ""}"><div class="wrap"><div class="rooster"><div class="{kol}">{label(kicker) if kicker else ""}<h1>{h1}</h1>'
            f'<p class="intro">{intro}</p>{extra}{acties() if cta else ""}</div>{rechts}</div></div></section>')

ISO_CSS = """<style>
.sb-wolk{animation:sbwolk 26s ease-in-out infinite alternate}.sb-wolk-1{animation-duration:34s;animation-delay:-9s}.sb-wolk-2{animation-duration:22s;animation-delay:-16s}@keyframes sbwolk{from{transform:translateX(0)}to{transform:translateX(24px)}}
.sb-boom{transform-box:fill-box;transform-origin:50% 100%;animation:sbwind 3.6s ease-in-out infinite alternate}.sb-boom-1{animation-delay:-1.2s}.sb-boom-2{animation-delay:-2.4s}@keyframes sbwind{from{transform:skewX(-2deg)}to{transform:skewX(2deg)}}
.sb-vlag{transform-box:fill-box;transform-origin:0 50%;animation:sbvlag 1.8s ease-in-out infinite alternate}@keyframes sbvlag{from{transform:scaleX(1) skewY(1.5deg)}to{transform:scaleX(.86) skewY(-1.5deg)}}
.sb-rij{animation:sbrij var(--duur,17s) linear var(--wacht,0s) infinite}@keyframes sbrij{from{transform:translateX(-360px)}to{transform:translateX(1260px)}}
.sb-rij-terug{animation:sbrijterug var(--duur,17s) linear var(--wacht,0s) infinite}@keyframes sbrijterug{from{transform:translateX(1260px)}to{transform:translateX(-360px)}}
.sb-zwaai{animation:sbzwaai .9s steps(2) infinite}@keyframes sbzwaai{0%{opacity:1}50%{opacity:.5}}
.sb-loop{animation:sbloop 10s ease-in-out var(--tempo,0s) infinite}@keyframes sbloop{0%{transform:translateX(var(--ix));opacity:0}4%{opacity:1}26%,56%{transform:translateX(0);opacity:1}58%{opacity:1}72%{transform:translateX(var(--dx));opacity:1}76%,100%{transform:translateX(var(--dx));opacity:0}}
.sb-arm{transform-box:fill-box;transform-origin:92% 30%;animation:sbarm 10s ease-in-out var(--tempo,0s) infinite}@keyframes sbarm{0%,28%{transform:rotate(-52deg)}34%,52%{transform:rotate(0)}60%,100%{transform:rotate(-52deg)}}
.led-deur{fill:#D9362B;animation:sbled 10s var(--tempo,0s) infinite}@keyframes sbled{0%,34%{fill:#D9362B}36%,80%{fill:#3DBE7A}84%,100%{fill:#D9362B}}
.sb-pui-l{animation:sbpuil 10s ease-in-out var(--tempo,0s) infinite}@keyframes sbpuil{0%,42%{transform:translateX(0)}52%,76%{transform:translateX(-26px)}86%,100%{transform:translateX(0)}}
.sb-pui-r{animation:sbpuir 10s ease-in-out var(--tempo,0s) infinite}@keyframes sbpuir{0%,42%{transform:translateX(0)}52%,76%{transform:translateX(26px)}86%,100%{transform:translateX(0)}}
.sb-draai{transform-box:fill-box;transform-origin:0 50%;animation:sbdraai 10s ease-in-out var(--tempo,0s) infinite}@keyframes sbdraai{0%,42%{transform:scaleX(1)}52%,76%{transform:scaleX(.14)}86%,100%{transform:scaleX(1)}}
.sb-rook{animation:sbrook 3.2s ease-out infinite}.sb-rook-1{animation-delay:-1.1s}.sb-rook-2{animation-delay:-2.2s}@keyframes sbrook{0%{opacity:.7;transform:translate(0,0) scale(.7)}100%{opacity:0;transform:translate(10px,-34px) scale(1.25)}}
.sb-roldeur{transform-box:fill-box;transform-origin:50% 0;animation:sbroldeur 12s ease-in-out infinite}@keyframes sbroldeur{0%,26%{transform:scaleY(1)}38%,66%{transform:scaleY(.12)}78%,100%{transform:scaleY(1)}}
.sb-slagboom{transform-box:fill-box;transform-origin:6% 50%;animation:sbslagboom 12s ease-in-out infinite}@keyframes sbslagboom{0%,14%{transform:rotate(0)}24%,58%{transform:rotate(-56deg)}70%,100%{transform:rotate(0)}}
.sb-lamp{animation:sblamp 8s ease-in-out infinite;opacity:.25}@keyframes sblamp{0%,100%{opacity:.25}20%,40%{opacity:1}}
.sb-wijzer{transform-box:fill-box;transform-origin:50% 88%;animation:sbwijzer 60s linear infinite}@keyframes sbwijzer{to{transform:rotate(360deg)}}
.sb-bal{animation:sbbal 1.6s cubic-bezier(.35,0,.65,1) infinite alternate}@keyframes sbbal{from{transform:translateY(0)}to{transform:translateY(-26px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""

def iso_bestand(sleutel):
    """Schrijft de sectorscène als los SVG-bestand (met de animaties erin) en geeft een <img> terug; scheelt ~110 KB per pagina."""
    uit = DIST / "static" / "img" / "iso"; uit.mkdir(parents=True, exist_ok=True)
    svg = straatbeeld.SECTOREN[sleutel]()
    svg = svg.replace('class="iso">', 'class="iso">' + ISO_CSS, 1)
    naam = f"{sleutel}.{hashlib.md5(svg.encode()).hexdigest()[:8]}.svg"   # versiehash: /static/ wordt lang gecachet, een nieuwe scène moet een nieuwe naam krijgen
    (uit / naam).write_text(svg, encoding="utf-8")
    alt = re.search(r'aria-label="([^"]+)"', svg).group(1)
    return f'<img src="/static/img/iso/{naam}" alt="{alt}" width="444" height="284" loading="lazy" class="iso">'

def sectorrij(items, kop, intro=None, kicker="Sectoren"):
    """Horizontaal scrollende rij met illustratie, kop, tekst en twee knoppen (Lars wil knoppen, geen tekstlinks): inventarisatie en meer informatie."""
    kaarten = "".join(
        f'<article class="kaart" id="sector-{sleutel}"><div class="kaart__beeld">{iso_bestand(sleutel)}</div>'
        f'<div class="kaart__tekst"><h3>{esc(k)}</h3><p>{t}</p><p class="acties acties--kaart">{cta_knop("Plan een inventarisatie", "#aanvraag", f"sector-{sleutel}")}'
        f'{cta_knop("Meer info", f"/toegangscontrole/#sector-{sleutel}", f"sector-{sleutel}-info", "knop knop--tweede")}</p></div></article>'
        for sleutel, k, t, _ in items)
    pijl_l = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>'
    pijl_r = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>'
    return (f'<section class="reveal"><div class="wrap"><div class="rij-kop"><div>{label(kicker)}<h2>{kop}</h2>{f"<p class=intro>{intro}</p>" if intro else ""}</div></div>'
            f'<div class="rij" data-rij-scroll>{kaarten}</div>'
            f'<div class="rij-knoppen"><button type="button" data-rij="-1" aria-label="Vorige sectoren">{pijl_l}</button><button type="button" data-rij="1" aria-label="Volgende sectoren">{pijl_r}</button></div></div></section>')

def video(bestand, poster, alt, kop="Bekijk de video", onderschrift=None):
    """Video op klik, nooit autoplay, eigen bestand uit static/img/bron/. Poster is een eigen foto (3:2) die door de
    beeldpipeline gaat. Ontbreekt de video of de poster, dan wordt het blok weggelaten en gemeld."""
    bronpad = BRON / bestand
    if not bronpad.exists() or not (BRON / poster).exists():
        _ONTBREKEND.append(bestand if not bronpad.exists() else poster)
        return ""
    uit = DIST / "static" / "video"; uit.mkdir(parents=True, exist_ok=True)
    videonaam = f"{bronpad.stem}-{hashlib.md5(bronpad.read_bytes()).hexdigest()[:8]}{bronpad.suffix}"   # /static/ wordt lang gecachet
    shutil.copy(bronpad, uit / videonaam)
    mime = "video/webm" if bestand.endswith(".webm") else "video/mp4"
    poster_html = beeld(poster, alt, sizes="(min-width: 900px) 66vw, 100vw")
    bijschrift = f"<figcaption>{esc(onderschrift)}</figcaption>" if onderschrift else ""
    return (f'<figure class="video" data-video>'
            f'<button type="button" class="video__start" aria-label="{esc(kop)}">{poster_html}<span class="video__knop">{esc(kop)}</span></button>'
            f'<video controls preload="none" playsinline hidden width="1600" height="1067"><source src="/static/video/{videonaam}" type="{mime}"></video>'
            f'{bijschrift}</figure>')

XESAR_VIDEO = "rAH27xzXeXI"   # EVVA Xesar, YouTube-kanaal van EVVA (Lars, 27-09-2026; gebruik aangevraagd bij EVVA)

# publieke gegevens van de video (oEmbed en videopagina, opgehaald 27-09-2026)
XESAR_VIDEO_INFO = {"titel": "Xesar - het elektronische sluitsysteem van EVVA in één blik", "maker": "EVVA Sicherheitstechnologie",
                    "datum": "2024-07-04", "duur": "PT1M15S", "duur_tonen": "1:15"}

def hero_badges():
    """Keurbalk over de herofoto: PKVW en EVVA. Staat het echte logo in static/img/logo/partners/ (pkvw of evva, svg of png),
    dan staat dat logo in de balk op een wit tegeltje; anders een dun lijnicoon (Lars, 27-09-2026)."""
    map_ = STATIC / "img" / "logo" / "partners"
    uit = DIST / "static" / "img" / "logo" / "partners"; uit.mkdir(parents=True, exist_ok=True)
    lijn = lambda d: f'<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
    def icoon(naam, alt, reserve):
        echt = next((map_ / f"{n}.{e}" for n in (f"{naam}-wit", naam) for e in ("svg", "png") if (map_ / f"{n}.{e}").exists()), None)   # witte versie voor de donkere balk
        if not echt: return reserve, False
        shutil.copy(echt, uit / echt.name)
        from PIL import Image
        if echt.suffix == ".png": bw, bh = Image.open(echt).size
        else:
            vb = re.search(r'viewBox="[\d.\s-]*?([\d.]+)\s+([\d.]+)"', echt.read_text(encoding="utf-8")); bw, bh = (round(float(vb.group(1))), round(float(vb.group(2)))) if vb else (100, 100)
        return f'<img src="/static/img/logo/partners/{echt.name}" alt="{esc(alt)}" width="{bw}" height="{bh}">', True
    pk, pk_echt = icoon("pkvw", "Politiekeurmerk Veilig Wonen", lijn('<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/>'))
    ev, ev_echt = icoon("evva", "EVVA", lijn('<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'))
    ab, ab_echt = icoon("abus", "ABUS", lijn('<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'))
    items = [(ev, ev_echt, "" if ev_echt else "EVVA Partner"), (ab, ab_echt, "" if ab_echt else "ABUS Partner")]   # partners in de balk
    # PKVW is een keurmerk, geen partner: groot en in de echte kleuren als zegel op de foto (Lars, 28-09-2026)
    zegel_bron = map_ / "pkvw-zegel-wit.png"   # wit erkend-zegel, transparante achtergrond, los op de herofoto (Lars, 02-10-2026)
    zegel = ""
    if zegel_bron.exists():
        zegelnaam = f"{zegel_bron.stem}-{hashlib.md5(zegel_bron.read_bytes()).hexdigest()[:8]}{zegel_bron.suffix}"   # /static/ wordt lang gecachet
        shutil.copy(zegel_bron, uit / zegelnaam)
        from PIL import Image
        zb, zh = Image.open(zegel_bron).size
        zegel = (f'<div class="keurmerk"><img src="/static/img/logo/partners/{zegelnaam}" alt="Politiekeurmerk Veilig Wonen, erkend" width="{zb}" height="{zh}">'
                 '</div>')
    tekst = lambda t: (f'<span class="keurbalk__lang">{esc(t.split("|")[0])} </span>{esc(t.split("|")[1].strip())}' if "|" in t else esc(t))
    return zegel   # partnerlogo's niet meer in de hero (Lars, 28-09-2026); PKVW-zegel blijft

def klantenbalk():
    """Bewegende balk met logo's van organisaties waarvoor wij werken (Lars, 28-09-2026). Leest static/img/logo/klanten/
    (svg of png; bestandsnaam = naam van de organisatie, bijvoorbeeld applus-hengelo.png). Alleen logo's met toestemming
    van de klant plaatsen. Zonder bestanden wordt het blok weggelaten."""
    map_ = STATIC / "img" / "logo" / "klanten"
    bestanden = sorted(p for p in map_.glob("*") if p.suffix.lower() in (".svg", ".png", ".webp")) if map_.exists() else []
    if not bestanden: return ""
    uit = DIST / "static" / "img" / "logo" / "klanten"; uit.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    items = []
    for f in bestanden:
        hnaam = f"{f.stem}-{hashlib.md5(f.read_bytes()).hexdigest()[:8]}{f.suffix}"   # hash tegen de 1-jaarscache
        shutil.copy(f, uit / hnaam)
        if f.suffix.lower() == ".svg":
            vb = re.search(r'viewBox="[\d.\s-]*?([\d.]+)\s+([\d.]+)"', f.read_text(encoding="utf-8")); bw, bh = (round(float(vb.group(1))), round(float(vb.group(2)))) if vb else (160, 60)
        else: bw, bh = Image.open(f).size
        naam = f.stem.replace("-", " ").title()
        items.append(f'<li><img src="/static/img/logo/klanten/{hnaam}" alt="{esc("Logo " + naam)}" width="{bw}" height="{bh}" loading="lazy"></li>')
    rij = "".join(items)
    return (f'<section class="klanten" aria-label="Organisaties waarvoor wij werken"><div class="wrap"><p class="klanten__kop">Zij gingen u voor</p></div>'
            f'<div class="klanten__band"><ul class="klanten__rij">{rij}</ul><ul class="klanten__rij" aria-hidden="true">{rij}</ul></div></section>')

XESAR_BESTAND = "evva-xesar-in-een-blik.mp4"   # eigen videobestand in static/img/bron/; zodra dat er staat, speelt de video van de eigen site in plaats van YouTube

def xesar_lokaal():
    """Pad van het eigen videobestand op de site, of None. Kopieert het bestand naar dist/static/video/."""
    bron = BRON / XESAR_BESTAND
    if not bron.exists(): return None
    uit = DIST / "static" / "video"; uit.mkdir(parents=True, exist_ok=True)
    naam = f"{bron.stem}-{hashlib.md5(bron.read_bytes()).hexdigest()[:8]}{bron.suffix}"
    if not (uit / naam).exists(): shutil.copy(bron, uit / naam)
    return f"/static/video/{naam}"

def youtube(video_id, titel, ondertitel=""):
    """YouTube op klik: tot de klik wordt niets van YouTube geladen (snel, geen cookies vooraf). Poster en eindscherm in de huisstijl,
    met het logo van Westendorp; het eindscherm verschijnt als de video klaar is (postMessage van de speler, zonder extra script)."""
    speel = '<svg viewBox="0 0 24 24" width="34" height="34" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>'
    logo = f'<span class="yt__logo"><img src="{_ASSETS["logo"]}" alt="{esc(NAAM)}" width="2053" height="647" loading="lazy"></span>'
    watermerk = f'<img class="yt__watermerk" src="{_ASSETS["icoon"]}" alt="" aria-hidden="true" width="495" height="647" loading="lazy">'
    eind = (f'<div class="yt__eind" hidden>{watermerk}{logo}<p class="yt__eindtitel">EVVA Xesar in uw pand?</p>'
            f'<p class="yt__eindtekst">Wij plaatsen Xesar op uw bestaande deuren, van inventarisatie tot beheer.</p>'
            f'<p class="yt__eindknoppen">{cta_knop("Plan een inventarisatie", "#aanvraag", "video-eind")}'
            f'<button type="button" class="knop knop--tweede yt__opnieuw">Opnieuw bekijken</button></p></div>')
    lokaal = xesar_lokaal()
    bron_attr = f'data-video-src="{lokaal}"' if lokaal else f'data-yt="{esc(video_id)}"'
    return (f'<figure class="yt" {bron_attr} data-yt-titel="{esc(titel)}">'
            f'<button type="button" class="yt__start" aria-label="Video afspelen: {esc(titel)}, {XESAR_VIDEO_INFO["duur_tonen"]} minuut">'
            f'{watermerk}{logo}<span class="yt__merk">EVVA Xesar</span><span class="yt__titel">{esc(titel)}</span>'
            + (f'<span class="yt__sub">{esc(ondertitel)}</span>' if ondertitel else "") +
            f'<span class="yt__knop">{speel}</span><span class="yt__knoptekst">Bekijk de video · {XESAR_VIDEO_INFO["duur_tonen"]}</span></button>'
            f'{eind}</figure>')

def video_ld(pad, beschrijving):
    """VideoObject voor zoekmachines en AI-assistenten: echte gegevens van de video, thumbnail met het logo van Westendorp."""
    v = XESAR_VIDEO_INFO; lokaal = xesar_lokaal()
    bronnen = ({"contentUrl": SITE + lokaal} if lokaal else
               {"embedUrl": f"https://www.youtube-nocookie.com/embed/{XESAR_VIDEO}", "contentUrl": f"https://www.youtube.com/watch?v={XESAR_VIDEO}"})
    return {"@type": "VideoObject", "@id": SITE + pad + "#xesar-video", "name": v["titel"], "description": beschrijving,
            "thumbnailUrl": [SITE + "/static/img/evva-xesar-video-westendorp.jpg", f"https://i.ytimg.com/vi/{XESAR_VIDEO}/hqdefault.jpg"],
            "uploadDate": v["datum"] + "T09:00:00+02:00", "duration": v["duur"], **bronnen, "inLanguage": "nl",
            "author": {"@type": "Organization", "name": v["maker"], "url": "https://www.evva.com"}, "publisher": {"@id": ORG_ID}, "isPartOf": {"@id": SITE + pad + "#webpage"}}

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
            f'<text x="300" y="425" text-anchor="middle" font-size="12" fill="#4A5760">Schematisch: plaatsen op hun ligging, de cirkel is ons kerngebied rond Enschede</text></svg>')

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
            wp = uit / f"{beeldnaam(bronpad)}-{w}.webp"
            # schema's met kleine tekst verdragen de standaardcompressie slecht: hogere kwaliteit (Lars, 01-10-2026)
            tekstbeeld = bronpad.stem.startswith(("sluitplan-voorbeeld", "virtueel-netwerk"))
            kopie.save(wp, "WEBP", quality=90 if tekstbeeld else 80, method=6)
            av = uit / f"{beeldnaam(bronpad)}-{w}.avif"
            try:
                kopie.save(av, "AVIF", quality=60)
                if av.stat().st_size > wp.stat().st_size * 0.8:
                    av.unlink(); avif_ok = False
            except Exception:
                avif_ok = False
        return b0, h0, avif_ok

_BEELDCACHE = {}
_BEELDEN_PAGINA = []   # (url, alt, onderschrift, breedte, hoogte) van de pagina die nu gebouwd wordt; schrijf() leest en leegt dit

_BEELDHASH = {}
def beeldnaam(bronpad):
    """Bestandsnaam voor Google: kleine letters, koppeltekens, plus een korte inhoudshash. /static/ wordt lang
    gecachet, dus een vervangen foto moet een nieuwe naam krijgen, anders blijven browsers de oude tonen (Lars, 01-10-2026)."""
    import unicodedata
    n = unicodedata.normalize("NFKD", bronpad.stem).encode("ascii", "ignore").decode().lower()
    n = re.sub(r"[^a-z0-9]+", "-", n).strip("-") or "foto"
    if bronpad not in _BEELDHASH:
        _BEELDHASH[bronpad] = hashlib.md5(bronpad.read_bytes()).hexdigest()[:8]
    return f"{n}-{_BEELDHASH[bronpad]}"

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
    stem = beeldnaam(bronpad)
    maten = [w for w in _MATEN if w <= b0 or w == _MATEN[0]]
    w1 = maten[0]; h1 = round(h0 * min(w1, b0) / b0)
    srcset = lambda ext: ", ".join(f"/static/img/{stem}-{w}.{ext} {min(w, b0)}w" for w in maten)
    laad = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    img = (f'<img src="/static/img/{stem}-{w1}.webp" srcset="{srcset("webp")}" sizes="{sizes}" '
           f'width="{min(w1, b0)}" height="{h1}" alt="{esc(alt)}"{laad}>')
    if avif_ok:
        img = f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">{img}</picture>'
    kl = f' class="{klas}"' if klas else ""
    wg = maten[-1]; _BEELDEN_PAGINA.append((f"/static/img/{stem}-{wg}.webp", alt, onderschrift, min(wg, b0), round(h0 * min(wg, b0) / b0), bron or NAAM))
    if onderschrift:
        return f"<figure{kl}>{img}<figcaption>{esc(onderschrift)}</figcaption></figure>"
    return f"<figure{kl}>{img}</figure>"

def schema_beeld(stam, alt, klas=""):
    """Eigen vectorschema (SVG) uit static/img/schema/<stam>-<hash>.svg: haarscherp op elk scherm."""
    bronpad = next((STATIC / "img" / "schema").glob(f"{stam}-*.svg"))
    doel = DIST / "static" / "img" / "schema"
    doel.mkdir(parents=True, exist_ok=True)
    shutil.copy(bronpad, doel / bronpad.name)
    kl = f' class="{klas}"' if klas else ""
    _BEELDEN_PAGINA.append((f"/static/img/schema/{bronpad.name}", alt, None, 1240, 840, NAAM))
    return (f'<figure{kl}><img src="/static/img/schema/{bronpad.name}" alt="{esc(alt)}" '
            f'width="1240" height="840" loading="lazy" decoding="async"></figure>')

# ---------- JSON-LD ----------
ORG_ID = SITE + "/#organisatie"
WEBSITE_ID = SITE + "/#website"

def bedrijf_ld():
    same_as = [u for u in [LINKEDIN, GOOGLE_PROFIEL] + ANDERE_PROFIELEN if u and not placeholder(u)]
    org = {
        "@type": "LocalBusiness", "@id": ORG_ID, "name": NAAM, "legalName": RECHTSPERSOON,
        "url": SITE + "/", "logo": SITE + _ASSETS["logo"], "image": SITE + OG_STANDAARD,
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
NAV = [("Toegangscontrole", "/toegangscontrole/"), ("Sectoren", "/toegangscontrole/#sectoren"), ("Elektronische sloten", "/elektronische-sloten/"),
       ("Sluitplan", "/sluitplan/"), ("Projecten", "/projecten/"), ("Kennisbank", "/kennisbank/"), ("Over ons", "/over-ons/"), ("Contact", "/contact/")]   # Kosten en Service in het uitklapmenu (Lars, 23-09-2026); Projecten vast bovenaan (Lars, 02-10-2026)
SUBNAV = {"/over-ons/": [("Over ons", "/over-ons/"), ("Duurzaamheid", "/duurzaamheid/"), ("Beveiliging en certificaten", "/over-ons/#beveiliging")],
          "/toegangscontrole/": [("Wat is toegangscontrole", "/toegangscontrole/"), ("EVVA Xesar", "/evva-xesar/"), ("Motorcilinder", "/motorcilinder/"),
                                 ("Service en beheer", "/service-en-beheer/"), ("Salto onderhoud", "/salto/"), ("Wat kost het", "/kosten/")],
          "/toegangscontrole/#sectoren": None}   # wordt hieronder gevuld uit SECTOREN_LIJST   # uitklapmenu (Lars, 23-09-2026)

_ICOON_BEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
_ICOON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

SUBNAV["/toegangscontrole/#sectoren"] = [(k, f"/toegangscontrole/#sector-{s}") for s, k, *_ in SECTOREN_LIJST]

def header(pad):
    def item(n, u):
        huidig = " aria-current=\"page\"" if u == pad or (u in SUBNAV and pad in [s for _, s in SUBNAV[u]]) else ""
        if u not in SUBNAV: return f'<li><a href="{u}"{huidig}>{esc(n)}</a></li>'
        sub = "".join(f'<li><a href="{su}">{esc(sn)}</a></li>' for sn, su in SUBNAV[u])
        return f'<li class="heeft-sub"><a href="{u}"{huidig} aria-haspopup="true">{esc(n)}<svg viewBox="0 0 24 24" width="12" height="12" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6"><path d="M6 9l6 6 6-6"/></svg></a><ul class="sub">{sub}</ul></li>'
    items = "".join(item(n, u) for n, u in NAV)
    return f'''<header class="kop{' kop--licht' if HEADER_LICHT else ''}"><div class="wrap">
<a class="logo" href="/" aria-label="{esc(NAAM)}, naar de homepage"><img src="{_ASSETS["logo"]}" alt="{esc(NAAM)}" width="2053" height="647"></a>
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
    over = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in [("Over ons", "/over-ons/"), ("Kennisbank", "/kennisbank/"), ("Duurzaamheid", "/duurzaamheid/"), ("Werkgebied", "/werkgebied/"), ("Contact", "/contact/"), ("Privacy", "/privacy/")])
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
    """Cookie-dialoog midden in beeld, naar het voorbeeld van de Slotenspecialist-site (Lars, 02-10-2026):
    logo + cookie-icoon, tabbladen Toestemming/Details/Over, schuifjes per categorie. Stijl en script inline,
    net als de chatwidget, zodat de CSS- en JS-budgetten vrij blijven."""
    if not TAG_ACTIEF: return ""
    stijl = '''<style>
.cmo{position:fixed;inset:0;z-index:90;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(2,24,48,.55)}
.cmo[hidden],.cmo [hidden]{display:none!important}
.cmo__dialoog{background:#fff;border-radius:14px;box-shadow:0 24px 70px rgba(2,24,48,.35);max-width:620px;width:100%;max-height:min(92vh,660px);display:flex;flex-direction:column;overflow:hidden}
.cmo__kop{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:22px 24px 14px}
.cmo__kop img{height:42px;width:auto}
.cmo__koek{color:var(--primair);flex:none}
.cmo__tabs{display:flex;border-bottom:var(--lijndikte) solid var(--lijn)}
.cmo__tabs button{flex:1;background:none;border:0;border-bottom:3px solid transparent;font:inherit;font-family:var(--font-kop);font-weight:700;font-size:15px;color:var(--inkt-zacht);padding:11px 0;cursor:pointer}
.cmo__tabs button.aan{color:var(--primair);border-bottom-color:var(--primair)}
.cmo__paneel{padding:18px 24px 6px;overflow:auto}
.cmo__paneel h2{font-family:var(--font-kop);font-size:18px;color:var(--kop);margin:0 0 8px}
.cmo__paneel p{margin:0 0 12px;font-size:15px;line-height:1.55;max-width:none}
.cmo__rij{display:flex;gap:16px;align-items:flex-start;justify-content:space-between;padding:12px 0;border-top:var(--lijndikte) solid var(--lijn)}
.cmo__rij:first-child{border-top:0}
.cmo__rij b{display:block;color:var(--kop);font-weight:600}
.cmo__rij span{font-size:13.5px;color:var(--inkt-zacht);display:block;max-width:44ch}
.cmo__schakel{position:relative;width:46px;height:26px;flex:none;appearance:none;-webkit-appearance:none;background:var(--lijn-2);border:0;border-radius:999px;cursor:pointer;transition:background .2s;margin:3px 0 0}
.cmo__schakel::after{content:"";position:absolute;left:3px;top:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgba(2,24,48,.3)}
.cmo__schakel:checked{background:var(--primair)}
.cmo__schakel:checked::after{transform:translateX(20px)}
.cmo__schakel:disabled{background:var(--signaal-licht);cursor:default}
.cmo__voet{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:16px 24px 20px;border-top:var(--lijndikte) solid var(--lijn)}
.cmo__stil{background:none;border:0;padding:0;font:inherit;font-size:13.5px;color:var(--inkt-zacht);text-decoration:underline;cursor:pointer}
.cmo__knoppen{display:flex;gap:10px;flex-wrap:wrap}
@media (max-width:520px){.cmo__kop img{height:32px}.cmo__voet{justify-content:center}.cmo__stil{order:2}}
</style>'''
    koek = ('<svg class="cmo__koek" viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 13.1A9 9 0 1 1 10.9 3.2 4 4 0 0 0 15 8a4 4 0 0 0 5.8 5.1z"/>'
            '<circle cx="9" cy="10" r="1" fill="currentColor"/><circle cx="13" cy="14" r="1" fill="currentColor"/>'
            '<circle cx="8.5" cy="14.8" r="1" fill="currentColor"/></svg>')
    html = f'''<div class="cmo" id="consent" hidden data-gedeeld><div class="cmo__dialoog" role="dialog" aria-modal="true" aria-label="Cookie-instellingen">
<div class="cmo__kop"><img src="{_ASSETS["logo_licht"]}" alt="{esc(NAAM)}" width="2053" height="647">{koek}</div>
<div class="cmo__tabs"><button type="button" class="aan" data-ctab="toestemming">Toestemming</button><button type="button" data-ctab="details">Details</button><button type="button" data-ctab="over">Over</button></div>
<div class="cmo__paneel" data-cpaneel="toestemming"><h2>{esc(NAAM)} maakt gebruik van cookies</h2>
<p>Wij gebruiken cookies en vergelijkbare technieken om te zien hoe de site wordt gebruikt en of onze advertenties werken. Noodzakelijke cookies staan altijd aan; de rest pas na uw keuze. Via Aanpassen kiest u per onderdeel. Meer over cookies en persoonsgegevens leest u in de <a href="/privacy/">privacyverklaring</a>.</p></div>
<div class="cmo__paneel" data-cpaneel="details" hidden>
<div class="cmo__rij"><div><b>Noodzakelijk</b><span>Voor het werken van de site, zoals het onthouden van deze cookie-keuze. Altijd actief.</span></div><input type="checkbox" class="cmo__schakel" checked disabled aria-label="Noodzakelijke cookies, altijd actief"></div>
<div class="cmo__rij"><div><b>Statistiek</b><span>Google Analytics: meten welke pagina's worden bezocht, om de site te verbeteren.</span></div><input type="checkbox" class="cmo__schakel" id="c-stat" aria-label="Statistiekcookies"></div>
<div class="cmo__rij"><div><b>Marketing</b><span>Google Ads: meten of onze advertenties tot een aanvraag of telefoontje leiden.</span></div><input type="checkbox" class="cmo__schakel" id="c-ads" aria-label="Marketingcookies"></div></div>
<div class="cmo__paneel" data-cpaneel="over" hidden>
<p>Deze instellingen horen bij westendorptoegang.nl van {esc(NAAM)}, onderdeel van {esc(RECHTSPERSOON)}. U kunt uw keuze altijd wijzigen via Cookie-instellingen onderaan elke pagina.</p>
<p>Vragen over cookies of persoonsgegevens? Bel <a href="tel:{esc(TEL_LINK)}">{esc(TEL_TONEN)}</a> of mail <a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a>. Zie ook de <a href="/privacy/">privacyverklaring</a>.</p></div>
<div class="cmo__voet"><button type="button" class="cmo__stil" data-cactie="weiger">Alleen noodzakelijke cookies</button>
<div class="cmo__knoppen"><button type="button" class="knop knop--tweede" data-cactie="aanpassen">Aanpassen</button><button type="button" class="knop knop--tweede" data-cactie="opslaan" hidden>Selectie opslaan</button><button type="button" class="knop" data-cactie="alles">Alle cookies toestaan</button></div></div>
</div></div>'''
    script = '''<script>(function(){var w=document.getElementById('consent');if(!w)return;
function lees(){try{return localStorage.getItem('consent')}catch(e){return null}}
function bewaar(v){try{localStorage.setItem('consent',v)}catch(e){}}
function update(st,ad){if(typeof gtag!=='function')return;gtag('consent','update',{analytics_storage:st?'granted':'denied',ad_storage:ad?'granted':'denied',ad_user_data:ad?'granted':'denied',ad_personalization:ad?'granted':'denied'})}
var sStat=w.querySelector('#c-stat'),sAds=w.querySelector('#c-ads');
var k=lees();if(k==='granted')update(1,1);else if(k==='stat')update(1,0);else if(k==='ads')update(0,1);
if(!k)w.hidden=false;
var ts=w.querySelectorAll('[data-ctab]'),ps=w.querySelectorAll('[data-cpaneel]');
ts.forEach(function(t){t.addEventListener('click',function(){
ts.forEach(function(x){x.classList.toggle('aan',x===t)});
ps.forEach(function(p){p.hidden=p.getAttribute('data-cpaneel')!==t.getAttribute('data-ctab')});
var det=t.getAttribute('data-ctab')==='details';
w.querySelector('[data-cactie="aanpassen"]').hidden=det;w.querySelector('[data-cactie="opslaan"]').hidden=!det;})});
function kies(v,st,ad){bewaar(v);update(st,ad);w.hidden=true}
w.querySelector('[data-cactie="alles"]').addEventListener('click',function(){sStat.checked=sAds.checked=true;kies('granted',1,1)});
w.querySelector('[data-cactie="weiger"]').addEventListener('click',function(){sStat.checked=sAds.checked=false;kies('denied',0,0)});
w.querySelector('[data-cactie="aanpassen"]').addEventListener('click',function(){w.querySelector('[data-ctab="details"]').click()});
w.querySelector('[data-cactie="opslaan"]').addEventListener('click',function(){var s=sStat.checked?1:0,a=sAds.checked?1:0;kies(s&&a?'granted':s?'stat':a?'ads':'denied',s,a)});
document.querySelectorAll('[data-consent-open]').forEach(function(b){b.addEventListener('click',function(){var k=lees();sStat.checked=k==='granted'||k==='stat';sAds.checked=k==='granted'||k==='ads';w.querySelector('[data-ctab="toestemming"]').click();w.hidden=false})});
})();</script>'''
    return stijl + html + script

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
<div class="veld"><label for="f-pand">Type pand</label><select id="f-pand" name="type_pand">{_opties("type_pand", ["Kantoor", "School", "Zorg", "Appartementencomplex", "Vereniging of kerk", "Horeca", "Recreatiepark", "Bedrijfspand of magazijn", "Overheid", "Anders"])}</select></div>
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
              PARTNER_TEKST[0].upper() + PARTNER_TEKST[1:],
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

def afwisselen(html_body):
    """Achtergronden om en om (Lars, 23-09-2026): geen twee opeenvolgende blokken met dezelfde kleur. De hero is warm gebroken wit,
    het aanvraagblok onderaan altijd lichtblauw; daartussen wit en lichtblauw om en om, terug gerekend vanaf het aanvraagblok.
    Groene blokken (duurzaamheid) houden hun kleur en tellen mee als eigen kleur."""
    delen = re.split(r'(<section class="reveal[^"]*"(?: id="[^"]*")?)', html_body)
    tags = [i for i in range(1, len(delen), 2)]
    kleuren, volgende = {}, "zacht"                                                     # het aanvraagblok
    for i in reversed(tags):
        t = delen[i]
        if 'id="aanvraag"' in t: kleuren[i] = "zacht"; volgende = "wit"; continue
        if "sectie--groen" in t: kleuren[i] = "groen"; continue
        kleuren[i] = volgende; volgende = "zacht" if volgende == "wit" else "wit"
    for i in tags:
        t = re.sub(r" sectie--(wit|lijn|zacht)", "", delen[i])
        if kleuren[i] != "groen": t = t.replace('class="reveal', f'class="reveal sectie--{kleuren[i]}', 1)
        delen[i] = t
    return "".join(delen)

def schrijf(pad, titel, omschrijving, body, kruimelpad=None, faq=None, extra_ld=(), paginatype="WebPage",
            noindex=False, llms="", og_beeld=None, met_formulier=True, formulier_kop="Plan een inventarisatie"):
    """Schrijft dist/<pad>/index.html. pad begint en eindigt met een slash."""
    kruimelpad = kruimelpad or [("Home", "/")] + ([(titel.split(" | ")[0], pad)] if pad != "/" else [])
    kruimel_html = kruimels(kruimelpad) if pad != "/" else ""
    faq_html = faqblok(faq) if faq else ""
    form_html = formulier(kop=formulier_kop) if met_formulier else ""
    volledige_body = kruimel_html + body + faq_html + form_html
    volledige_body = afwisselen(volledige_body)
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
        "og_beeld": SITE + (og_beeld or (beelden[0][0] if beelden else OG_STANDAARD)),
        "css": _ASSETS["css"], "js": _ASSETS["js"], "icoon": _ASSETS["icoon"], "tag": tag_html(), "jsonld": ld_script(graph),
        "header": header(pad), "body": volledige_body, "footer": footer(), "consent": consent_html(),
        "chat": "" if noindex else chat_widget(),
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
    if DIST.exists(): leeg_dist()
    (DIST / "static" / "css").mkdir(parents=True, exist_ok=True); (DIST / "static" / "js").mkdir(parents=True, exist_ok=True)
    css = (STATIC / "css" / "tokens.css").read_text(encoding="utf-8") + "\n" + (STATIC / "css" / "styles.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)        # commentaar strippen: bron blijft leesbaar, dist blijft onder het budget
    css_naam = f"site.{hashlib.md5(css.encode()).hexdigest()[:8]}.css"
    (DIST / "static" / "css" / css_naam).write_text(css, encoding="utf-8")
    js_naam = f"site.{versie(STATIC / 'js' / 'site.js')}.js"
    shutil.copy(STATIC / "js" / "site.js", DIST / "static" / "js" / js_naam)
    _ASSETS["css"], _ASSETS["js"] = f"/static/css/{css_naam}", f"/static/js/{js_naam}"
    shutil.copytree(STATIC / "font", DIST / "static" / "font", dirs_exist_ok=True)
    logo_uit = DIST / "static" / "img" / "logo"; logo_uit.mkdir(parents=True, exist_ok=True)
    # Alleen de header is zwart (#111111); daar staat het logo, dus de variant voor zwarte achtergrond (LEESMIJ: tot #1E1E1E).
    lb = STATIC / "img" / "logo" / "pakket"   # officieel logopakket van Lars (23-09-2026): logo-standaard is het hoofdlogo
    if HEADER_LICHT:
        logo_bron, icoon_bron = lb / "logo-standaard.svg", lb / "icoon-standaard.svg"
    else:
        logo_bron, icoon_bron = lb / "logo-zwarte-achtergrond.svg", lb / "icoon-zwarte-achtergrond.svg"
    # versiehash in de bestandsnaam: /static/ wordt een jaar gecachet, dus een nieuw logo moet een nieuwe naam krijgen
    _ASSETS["logo"] = f"/static/img/logo/logo.{versie(logo_bron)}.svg"; shutil.copy(logo_bron, DIST / _ASSETS["logo"].lstrip("/"))
    licht_bron = lb / "logo-standaard.svg"   # variant voor lichte achtergrond: cookie-dialoog
    _ASSETS["logo_licht"] = f"/static/img/logo/logo-licht.{versie(licht_bron)}.svg"; shutil.copy(licht_bron, DIST / _ASSETS["logo_licht"].lstrip("/"))
    _ASSETS["icoon"] = f"/static/img/logo/icoon.{versie(icoon_bron)}.svg"; shutil.copy(icoon_bron, DIST / _ASSETS["icoon"].lstrip("/"))
    for extra in ["favicon.ico", "favicon.svg", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png", "android-chrome-192x192.png", "android-chrome-512x512.png"]:
        shutil.copy(STATIC / "img" / "logo" / "favicon" / extra, DIST / extra)          # favicon-set uit het logopakket, in de hoofdmap
    thumb = STATIC / "img" / "evva-xesar-video-westendorp.jpg"
    if thumb.exists(): shutil.copy(thumb, DIST / "static" / "img" / thumb.name)          # thumbnail van de Xesar-video, met logo
    shutil.copy(lb / "og-standaard-1200x630.png", DIST / "static" / "img" / OG_STANDAARD.lstrip("/").replace("static/img/", ""))
    (DIST / "manifest.webmanifest").write_text(json.dumps({"name": NAAM, "short_name": "Westendorp", "start_url": "/", "display": "browser",
        "background_color": "#FFFFFF", "theme_color": "#02295B", "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}, {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False), encoding="utf-8")

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
           "salto", "kosten", "projecten", "kennisbank", "duurzaamheid", "werkgebied", "over_ons", "contact", "bedankt", "privacy"]   # volgorde = volgorde in llms.txt

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
