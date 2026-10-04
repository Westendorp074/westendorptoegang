"""/projecten/ — hoofdzoekwoord: toegangscontrole projecten / referenties. Uitgevoerd werk per sector en plaats."""
from build import *

PAD = "/projecten/"

# Elk project is één regel; de kaarten en de sectorkoppeling volgen vanzelf.
# (sector-anker uit SECTOREN_LIJST of "", sectornaam, plaats, kop, tekst, foto in static/img/bron of "", alt-tekst)
# Alleen projecten met toestemming van de klant; aantallen komen van de uitgevoerde opdrachten (04-10-2026).
PROJECTEN = [
    ("zorg", "Zorg", "7 locaties", "Modern Care",
     "Zorginstelling met zeven locaties, één toegangsbeheer: wij plaatsten 33 deuren met EVVA Xesar en richtten de rechten per medewerker en per locatie in. "
     "Verandert er iets in het team, dan past de beheerder de pas aan in plaats van de cilinder; het geheel stond binnen twee weken.",
     "project-modern-care.jpg", "Adviesgesprek aan tafel over toegangsbeheer bij een zorgorganisatie"),
    ("retail", "Retail", "2 vestigingen", "Bruna",
     "Twee Bruna-vestigingen stapten over van losse sleutels op EVVA AirKey: drie deuren met elektronische cilinders, geopend met telefoon of digitale sleutel. "
     "De leverancier en het schoonmaakbedrijf krijgen rechten met een tijdslot, en een vertrokken medewerker is met één klik geblokkeerd.",
     "project-bruna.jpg", "Winkelgevel van een Bruna-vestiging waar Westendorp EVVA AirKey plaatste"),
    ("retail", "Retail", "Enschede", "Bakkerij Oonk",
     "Vier vestigingen, zeven deuren en ruim veertig medewerkers die vroeg beginnen: Bakkerij Oonk opent nu met EVVA AirKey op de telefoon. "
     "Bezorgers krijgen tijdelijke toegang, rechten wijzigen kost geen nieuwe cilinders, en de ombouw was binnen een week klaar zonder de deuren aan te passen.",
     "project-bakkerij-oonk.jpg", "Winkel van bakkerij Oonk in Enschede, waar Westendorp EVVA AirKey-toegang plaatste"),
    ("verenigingen", "Sport & Verenigingen", "Delden", "Rood Zwart",
     "Voetbalvereniging Rood Zwart draait op vrijwilligers en ruim honderd pasgebruikers over 22 deuren. Sinds 2023 doen wij het jaarlijkse onderhoud aan hun EVVA Xesar-systeem: "
     "componenten nalopen, software bijwerken en de rechten actualiseren — in één week, zonder dat trainingen of wedstrijden er iets van merken.",
     "project-rood-zwart-delden.jpg", "Clubgebouw van voetbalvereniging Rood Zwart in Delden, waar Westendorp het EVVA Xesar-systeem onderhoudt"),
    ("overheid", "Overheid", "Enschede", "Prismare",
     "Wijkcentrum Prismare in Roombeek huisvest tientallen organisaties achter 66 deuren met EVVA Xesar. Wij voeren er het jaarlijkse preventieve onderhoud uit: "
     "volledige systeemcontrole, updates en het bijwerken van de rechten van ruim honderd gebruikers, binnen een week en zonder de dagelijkse activiteiten te storen.",
     "project-prismare-enschede.jpg", "Entree van wijkcentrum Prismare in Enschede, waar Westendorp het EVVA Xesar-systeem onderhoudt"),
    ("overheid", "Overheid", "Enschede", "Lumen",
     "Lumen, het hart voor de wijk, kent intensief gebruik door meerdere organisaties: 25 deuren met EVVA Xesar en ruim honderd pasgebruikers. "
     "Wij onderhouden het systeem jaarlijks — cilinders en componenten controleren, software bijwerken, rechten beheren — binnen een week, terwijl het gebouw gewoon doordraait.",
     "project-lumen-enschede.jpg", "Gebouw van Lumen in Enschede met de bedrijfsbus van Westendorp voor de entree"),
    ("retail", "Retail", "Enschede", "Winkelcentrum Enschede Zuid",
     "Voor winkelcentrum Enschede Zuid ontwierpen wij een compleet mechanisch sluitplan: winkels, gezamenlijke voorzieningen, leveranciersingangen en technische ruimtes "
     "in één sleutelstructuur, zodat winkeliers, beheer en externe partijen precies de deuren openen die bij hun rol horen.",
     "project-winkelcentrum-enschede-zuid.jpg", "Winkelpassage van winkelcentrum Enschede Zuid, waarvoor Westendorp het sluitplan ontwierp"),
    ("retail", "Retail", "Hengelo", "Winkelcentrum Hasseler Es",
     "Winkelcentrum Hasseler Es kreeg in 2023 een nieuw mechanisch sluitplan van ons: één structuur voor winkels, technische ruimtes en externe diensten. "
     "Het aantal losse sleutels in omloop ging flink omlaag en de beheerder weet weer precies welke sleutel waarop past.",
     "project-winkelcentrum-hasseler-es.jpg", "Entree van winkelcentrum Hasselo in Hengelo, waarvoor Westendorp het sluitplan maakte"),
    ("overheid", "Overheid", "Twente", "Zeven gemeenten",
     "Zeven gemeenten in en rond Twente, waaronder Enschede, Almelo en Oldenzaal, schakelen ons in als vaste partner voor hang- en sluitwerk: "
     "panden openen, cilinders vervangen en alles weer veilig afsluiten — gepland of met spoed, dag en nacht, ook bij bijzondere acties met politie of douane.",
     "project-gemeenten.jpg", "Bedrijfsbus van Westendorp bij een pand tijdens een gemeentelijke actie met politie en douane"),
    ("vve", "VvE & Vastgoed", "Twente", "VvE's en vastgoedbeheerders",
     "Voor Verenigingen van Eigenaren vervangen wij cilinders in entrees en bergingen, verbeteren wij het hang- en sluitwerk en zetten wij sluitplannen op "
     "met sleutelbeheer waar het bestuur overzicht over houdt — in afstemming met de beheerder, zonder gedoe voor de bewoners.",
     "project-vve.jpg", "Monteur van Westendorp reviseert een meerpuntsslot aan de werkbank in de servicebus"),
    ("", "Zakelijke dienstverlening", "Twente", "Deurwaarderskantoren",
     "Deurwaarders werken al jaren met ons bij ontruimingen en beslagleggingen: deuren vakkundig openen zonder schade waar dat kan, cilinders direct vervangen "
     "en het pand veilig afgesloten achterlaten. Discreet, 24/7 beschikbaar en direct inzetbaar.",
     "project-deurwaarders.jpg", "Bedrijfsbus van Westendorp bij een woongebouw tijdens een opdracht voor een deurwaarder"),
]

def bouw():
    titel = "Projecten: ons werk per sector"
    omschrijving = ("Projecten van Westendorp in Oost-Nederland: toegangscontrole, sluitplannen en hang- en sluitwerk "
                    "voor gemeenten, zorg, winkelcentra en bedrijven.")
    intro = ("Van gemeentehuizen tot wijkcentra en van winkelcentra tot werkplaatsen: hieronder ziet u een selectie van ons werk. "
             "Per project leest u waar het was, om welke sector het ging en wat wij daar hebben geplaatst. "
             "Deze pagina groeit; vraag gerust naar een referentie uit uw eigen sector.")

    kaarten = "".join(
        f'<div class="projectkaart">'
        + (beeld(foto, alt, sizes="(min-width: 700px) 46vw, 100vw") if foto else "")
        + f'<span class="product__label">{esc(sector)} · {esc(plaats)}</span><h3>{esc(kop)}</h3><p>{esc(tekst)}</p>'
        + '<p class="projectkaart__meer"><a class="knop knop--tweede" href="#aanvraag">Plan een gratis inventarisatie</a></p>'
        + "</div>"
        for anker, sector, plaats, kop, tekst, foto, alt in PROJECTEN)
    blok = sectie("Uitgelichte projecten", f'<div class="kolommen kolommen--2">{kaarten}</div>')

    # organisaties waarvoor wij werken (zelfde namen als de logobalk op de homepagina)
    namen = ["Gemeente Enschede", "Gemeente Hengelo", "Gemeente Almelo", "Politie", "Lumen", "Prismare", "Modern Care",
             "Bruna", "Winkelcentrum Hasselo", "Winkelcentrum Enschede Zuid", "Lastechniek Oost", "Oonk", "Rood Zwart"]
    wie = sectie("Zij gingen u voor", p(
        "Wij werken onder meer voor " + ", ".join(namen[:-1]) + " en " + namen[-1] + ". "
        "Wilt u weten wat wij in uw sector hebben gedaan? Bel of mail ons, dan sturen wij een passende referentie.") , wit=True)

    faq = [
        ("Kan ik een referentie krijgen uit mijn eigen sector?",
         "Ja. Vertel ons om wat voor pand het gaat, dan koppelen wij u aan een vergelijkbaar project en, als de klant dat goed vindt, aan een contactpersoon."),
        ("Plaatsen jullie ook buiten de regio van deze projecten?",
         "Wij werken in heel Oost-Nederland, vanuit Enschede. Alle plaatsen staan op <a href=\"/werkgebied/\">werkgebied</a>."),
        ("Komt mijn project ook op deze pagina?",
         "Alleen met uw toestemming. Veel klanten vinden dat prima; sommige panden, zoals serverruimtes of zorglocaties, laten wij bewust weg."),
    ]

    herofoto = beeld("monteur-xesar-tablet-onderhoud-deur.jpg",
                     "Monteur van Westendorp sluit de Xesar-tablet aan op het elektronische deurbeslag tijdens onderhoud bij een klant", lazy=False)
    body = hero("Projecten: zo ziet ons werk eruit", intro, foto_html=herofoto) + blok + wie
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Projecten", PAD)],
            llms="Referentieprojecten per sector en plaats: wie wij al hielpen met toegangscontrole, sluitplannen en hang- en sluitwerk.")
