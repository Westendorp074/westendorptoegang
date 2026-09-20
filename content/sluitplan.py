"""/sluitplan/ — hoofdzoekwoord: sluitplan. Mechanisch, elektronisch en de overstap."""
from build import *

PAD = "/sluitplan/"

def bouw():
    titel = "Sluitplan voor uw bedrijf: mechanisch of elektronisch"
    omschrijving = ("Sluitplan mechanisch of elektronisch: wanneer welk, wat er gebeurt bij een verloren sleutel, certificering en beheer. Ontwerp en levering door Westendorp.")
    intro = ("Een sluitplan legt vast welke sleutel op welke deur past: de directeur overal, de schoonmaak alleen de kantoren, de monteur alleen de techniekruimte. "
             "Mechanisch werkt dat met gecertificeerde cilinders en sleutels die niet zomaar zijn na te maken; elektronisch met passen en software. "
             "Wij ontwerpen en leveren beide, en verzorgen de overstap van het een naar het ander.")
    foto = beeld("sluitplan-cilinders.jpg", "Cilinders en sleutels van een mechanisch sluitplan", onderschrift=INV("onderschrift foto sluitplan"))

    mech = sectie("Wanneer is een mechanisch sluitplan nog verstandig", p(
        "Bij weinig deuren, weinig wisselingen en geen behoefte aan logging blijft een mechanisch sluitplan de goedkoopste oplossing. "
        "Ook binnen een elektronisch systeem blijven mechanische cilinders nuttig voor deuren die zelden opengaan: meterkasten, techniekruimtes, "
        "kasten en hekken. Wij werken met " + esc(MERKEN['mechanisch']['naam']) + ".",
        "Een gecertificeerd sluitsysteem heeft een sleutelkaart: alleen wie die kaart toont, kan bij ons sleutels laten bijmaken. Dat is het verschil met losse sloten van de bouwmarkt."))

    elek = sectie("Wanneer elektronisch", p(
        "Zodra er regelmatig iemand bijkomt of weggaat, sleutels zoekraken, of u wilt weten wie wanneer binnen was, wint elektronisch. "
        "De rechten zitten dan niet in de sleutel maar in de software: een pas blokkeren kost een minuut, een nieuwe medewerker toevoegen ook. "
        "Zie <a href=\"/evva-xesar/\">EVVA Xesar</a> voor het systeem dat wij daarvoor plaatsen."), wit=True)

    kwijt = sectie("Sleutel kwijt: het verschil in één tabel", tabel([
        ("Wat gebeurt er", "Onbekend wie de sleutel heeft en welke deuren ermee opengaan", "U blokkeert de pas in de software"),
        ("Wat moet u doen", "Cilinders vervangen van alle deuren waar de sleutel op paste; bij een hoofdsleutel vaak het hele plan", "Nieuwe pas uitgeven"),
        ("Kosten", f"Per cilinder {esc(PRIJZEN['mech_cilinder'][0])} tot {esc(PRIJZEN['mech_cilinder'][1])}, excl. btw, plus montage; bij een hoofdsleutel maal het aantal deuren", "De prijs van één pas"),
        ("Doorlooptijd", "Levertijd van gecertificeerde cilinders plus montage", "Direct"),
        ("Bewijs voor verzekeraar", "Alleen de sleutelkaart en de administratie", "Logboek: wanneer geblokkeerd, wie waar was"),
    ], kop=["", "Mechanisch sluitplan", "Elektronisch sluitplan"], bijschrift="Wat er gebeurt als een sleutel of pas kwijt is")
        + p("Dit contrast is voor de meeste bedrijven de reden om over te stappen: niet de techniek, maar die ene verloren hoofdsleutel."))

    overstap = sectie("De overstap van mechanisch naar elektronisch", stappen([
        ("Inventarisatie", "Wij nemen het bestaande sluitplan door: welke cilinders, welke sleutels in omloop, welke deuren echt elektronisch moeten."),
        ("Ontwerp", "Nieuw plan met elektronische deuren waar de wisselingen zitten en mechanische cilinders waar dat volstaat, in één systeem van EVVA."),
        ("Gefaseerd plaatsen", "Deur voor deur, zodat het pand in gebruik blijft. Oude sleutels worden per zone ingeleverd."),
        ("Beheer overdragen", f"U krijgt de software en de instructie; oude sleutelkaarten worden afgesloten. Beheer door ons: {esc(DIENSTEN_ONBEVESTIGD['beheer'])}."),
    ]), wit=True)

    cert = sectie("Certificering, verzekering en beheer", p(
        "Verzekeraars vragen bij inbraakdekking vaak om gecertificeerd hang- en sluitwerk; welke klasse hangt af van het risico en de polis. "
        "Wij leveren cilinders en beslag met de bijbehorende certificaten en zetten de klasse in het sluitplan, zodat u het bij een controle kunt laten zien. "
        f"Certificaten van Westendorp zelf: {esc(CERTIFICATEN)}.",
        "Het beheer van een mechanisch plan bestaat uit de sleutelkaart, de sleutelregistratie en het bijbestellen via ons. Bij een elektronisch plan doet u dat zelf in de software, of wij doen het voor u."))

    faq = [
        ("Wat kost een mechanisch sluitplan?", f"Per gecertificeerde cilinder {esc(PRIJZEN['mech_cilinder'][0])} tot {esc(PRIJZEN['mech_cilinder'][1])}, excl. btw, inclusief {esc(PRIJZEN['mech_cilinder'][2])}. {PRIJS_DISCLAIMER} Zie <a href=\"/kosten/\">kosten</a>."),
        ("Kan ik mijn bestaande sluitplan uitbreiden?", "Ja, zolang het systeem nog geleverd wordt en u de sleutelkaart heeft. Is het systeem verlopen of de kaart kwijt, dan adviseren wij een nieuw plan, meestal meteen elektronisch voor de deuren waar het om gaat."),
        ("Moet alles in één keer elektronisch?", "Nee. De meeste klanten beginnen met de buitendeur en de ruimtes met risico, en laten de rest mechanisch. Het EVVA-systeem laat beide naast elkaar bestaan."),
        ("Hoe lang duurt het maken van een sluitplan?", f"Het ontwerp maken wij na de inventarisatie, de offerte volgt binnen {esc(OFFERTE_BINNEN)}. Levertijd van gecertificeerde cilinders en de montage: {esc(DOORLOOPTIJD)}."),
        ("Wie mag sleutels bijbestellen?", "Alleen de houder van de sleutelkaart, of iemand die u schriftelijk machtigt. Wij leggen dat bij de oplevering vast; zo weet u zeker dat er geen sleutels buiten u om worden gemaakt."),
    ]

    body = hero("Sluitplan: mechanisch, elektronisch of de overstap", intro, foto) + mech + elek + kwijt + overstap + cert
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Sluitplan", PAD)],
            extra_ld=[service_ld(PAD, "Sluitplan", omschrijving)],
            llms="Sluitplan: mechanisch of elektronisch, wat er gebeurt bij een verloren sleutel (vergelijkingstabel), de overstap in vier stappen, certificering en beheer.")
