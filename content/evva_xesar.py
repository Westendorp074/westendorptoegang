"""/evva-xesar/ — hoofdzoekwoord: evva xesar. Merkpagina van ons hoofdmerk."""
from build import *

PAD = "/evva-xesar/"

def bouw():
    m = MERKEN["xesar"]
    titel = "EVVA Xesar toegangscontrole"
    omschrijving = ("EVVA Xesar: elektronische cilinders, beslag en wandlezers voor bedrijven. Voor wie, specificaties, eerlijke plus- en minpunten en installatie.")
    intro = ("EVVA Xesar is een elektronisch toegangscontrolesysteem van de Oostenrijkse slotenfabrikant EVVA, met cilinders, deurbeslag en wandlezers "
             "die op bestaande deuren passen. Het is het systeem dat wij het meest plaatsen: mechanisch en elektronisch van dezelfde fabrikant, "
             "en offline en online deuren in één beheeromgeving.")
    foto = beeld("evva-xesar-product.jpg", "EVVA Xesar elektronische cilinder en beslag", onderschrift="Productbeeld EVVA Xesar (fabrikant)")

    voorwie = sectie("Voor wie is Xesar geschikt", p(
        "Xesar past bij organisaties van een handvol tot enkele honderden deuren die hun toegang zelf willen beheren: kantoren, scholen, zorglocaties, verenigingen, "
        "recreatieparken en bedrijfspanden. Het sterkst is het waar al een mechanische cilinder zit: die wisselt u voor een Xesar-cilinder zonder aan de deur te komen.",
        "Wilt u sommige deuren live zien en op afstand openen, dan zet u die online; de rest blijft offline en goedkoper. Bij nieuwbouw combineren wij Xesar met een mechanisch sluitplan van EVVA voor techniekruimtes en kasten."))

    lijnen = sectie("Welke Xesar-onderdelen wij leveren", p(f"Lijnen en versie: {esc(m['lijnen'])}.") + lijst([
        "Elektronische cilinders (dubbel, half, knop) voor binnen- en buitendeuren en voor hangsloten",
        "Elektronisch beslag voor binnendeuren en brandwerende deuren",
        "Wandlezers met elektrische sluitplaat voor entrees en deuren met deurautomaat",
        "Beheersoftware met tablet of programmeerstation voor het bijwerken van passen",
        "Passen, tags en telefoon-toegang",
    ]) + p(f"Partnerstatus: {esc(m['partner'])}."), wit=True)

    plusmin = sectie("Sterke en zwakke punten, eerlijk", '<div class="kolommen kolommen--2"><div><h3>Sterk</h3>' + lijst([
        "Cilinder en beslag van dezelfde fabrikant als het mechanische sluitplan; alles uit één systeem.",
        "Offline en online deuren door elkaar in één beheeromgeving.",
        "Batterijen en noodopening goed opgelost: melding vooraf, noodvoeding bij de deur.",
        "Onderdelen zijn per deur uit te breiden; u begint klein en groeit mee.",
    ]) + '</div><div><h3>Houd rekening met</h3>' + lijst([
        "Bij offline deuren moet een pas periodiek langs een updater of het programmeerstation om nieuwe rechten op te halen.",
        "De beheersoftware vraagt een korte instructie; wij nemen die met u door bij de oplevering.",
        "Online deuren kosten meer per deur dan offline; kies ze alleen waar het nodig is.",
    ]) + "</div></div>")

    specs = sectie("Specificaties", tabel([
        ("Identificatie", "Pas, tag, telefoon"),
        ("Beheer", "Beheersoftware op eigen server of pc; passen bijwerken via updater of programmeerstation; online deuren direct"),
        ("Offline / online", "Beide, in één systeem"),
        ("Voeding", "Batterij in cilinder en beslag; wandlezer op netvoeding"),
        ("Deurtypes", "Hout, staal, aluminium en kunststof profiel; brandwerende deuren met gecertificeerde uitvoering"),
        ("Certificering", INV("Xesar-certificering die Westendorp levert, bijv. SKG-sterren of EN-klasse per onderdeel")),
        ("Uitbreidbaarheid", "Per deur, zonder de bestaande deuren aan te passen"),
        ("Rapportage", "Passages per deur en per pas, afhankelijk van offline of online"),
    ], bijschrift="Specificaties EVVA Xesar"), wit=True)

    kosten = sectie("Wat kost een Xesar-traject", p(
        f"Een Xesar-cilinder kost geplaatst {esc(PRIJZEN['cilinder_xesar'][0])} tot {esc(PRIJZEN['cilinder_xesar'][1])} per deur, elektronisch beslag {esc(PRIJZEN['beslag'][0])} tot {esc(PRIJZEN['beslag'][1])}, excl. btw. "
        f"Daar komt de beheersoftware bij. {PRIJS_DISCLAIMER} Rekenvoorbeelden voor een klein kantoor, een school en een zorglocatie staan op <a href=\"/kosten/\">wat kost toegangscontrole</a>."))

    faq = [
        ("Wat is het verschil tussen EVVA Xesar en EVVA AirKey?", f"Xesar is een systeem met eigen beheersoftware en passen, gericht op bedrijven en instellingen. AirKey werkt via de cloud en de telefoon. Of wij AirKey leveren: {esc(AIRKEY)}."),
        ("Moet ik voor Xesar mijn deuren vervangen?", "Nee. De Xesar-cilinder vervangt de bestaande cilinder; beslag vervangt de kruk. Alleen houten deuren die beslag krijgen hebben soms een uitsparing nodig, die frezen wij zelf in."),
        ("Hoe krijgt een pas nieuwe rechten bij een offline deur?", "De pas haalt de rechten op bij een updater, meestal bij de entree, of bij het programmeerstation. Blokkeert u een pas, dan weten offline deuren dat zodra de blokkeerlijst is bijgewerkt; online deuren direct."),
        ("Kunnen wij Xesar combineren met een mechanisch sluitplan?", "Ja. EVVA maakt beide, en dat is een van de redenen waarom wij Xesar plaatsen: techniekruimtes, meterkasten en kasten mechanisch, de rest elektronisch, met één leverancier voor beide."),
        ("Doen jullie ook het beheer van Xesar?", f"Wij leveren het systeem op, richten het in en leren u het beheer. Beheer door ons: {esc(DIENSTEN_ONBEVESTIGD['beheer'])}. Zie <a href=\"/service-en-beheer/\">service en beheer</a>."),
    ]

    body = hero("EVVA Xesar: elektronische toegangscontrole voor uw pand", intro, foto) + voorwie + lijnen + plusmin + specs + kosten
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("EVVA Xesar", PAD)],
            extra_ld=[service_ld(PAD, "EVVA Xesar toegangscontrole", omschrijving, merk="EVVA")],
            llms="EVVA Xesar: wat het is, voor wie, welke onderdelen wij leveren, sterke en zwakke punten, specificatietabel, kosten.")
