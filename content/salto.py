"""/salto/ — hoofdzoekwoord: salto toegangscontrole. Onderhoud en uitbreiding van bestaande Salto-systemen; wij plaatsen geen nieuwe."""
from build import *

PAD = "/salto/"

def bouw():
    titel = "Salto onderhoud, storing en uitbreiding"
    omschrijving = ("Heeft u al een Salto-systeem? Westendorp verhelpt storingen, vervangt onderdelen en breidt bestaande Salto-installaties uit in Oost-Nederland.")
    intro = ("Heeft uw pand al een Salto-systeem en zoekt u iemand die het onderhoudt? Wij verhelpen storingen aan Salto-beslag, -cilinders en -wandlezers, "
             "vervangen onderdelen en breiden bestaande installaties uit. Nieuwe systemen plaatsen wij niet in Salto maar in EVVA Xesar; "
             "wat u heeft, houden wij aan de praat.")

    wat = sectie("Wat wij aan Salto doen", lijst([
        "Storingen: beslag dat niet reageert, cilinders die niet meer draaien, lezers zonder verbinding.",
        "Onderdelen vervangen: batterijen, beslag, cilinders en lezers die versleten of beschadigd zijn.",
        "Uitbreiding: extra deuren of een nieuwe entree binnen uw bestaande Salto-systeem.",
        "Beheer: passen uitgeven en blokkeren, rechten aanpassen als u daar zelf geen tijd voor heeft.",
    ]) + p(f"Reactietijd bij storing: {esc(REACTIE_STORING)}. Buiten kantoortijd: {esc(STORING_BUITEN_KANTOORTIJD)}."))

    niet = sectie("Wat wij niet doen: nieuwe Salto-systemen", p(
        "Voor nieuwe installaties kiezen wij voor EVVA Xesar: cilinders, beslag en het mechanische sluitplan van dezelfde fabrikant, en offline en online deuren in één systeem. "
        "Overweegt u een nieuw systeem naast of in plaats van uw Salto-installatie, dan laten wij u zien wat dat betekent voor uw deuren en uw passen. "
        "Zie <a href=\"/evva-xesar/\">EVVA Xesar</a> en <a href=\"/kosten/\">wat kost toegangscontrole</a>."), wit=True)

    specs = sectie("Wat wij van u nodig hebben", tabel([
        ("Welke onderdelen", "Beslag, cilinders, wandlezers, updaters; foto's helpen"),
        ("Software", "Welke Salto-software en versie draait er, en op welke pc of server"),
        ("Beheerdersrechten", "Wie heeft de beheerderstoegang en de programmeerkaarten"),
        ("Documentatie", "Deurenlijst, sluitplan of de opleverdocumenten van de vorige installateur, als die er zijn"),
        ("Storing", "Welke deur, wat gebeurt er precies, sinds wanneer"),
    ], bijschrift="Informatie voor onderhoud aan een Salto-systeem") + p("Ontbreekt er iets? Dan beginnen wij met een inventarisatie op locatie en leggen wij het alsnog vast."))

    faq = [
        ("Kunnen jullie een Salto-storing verhelpen als jullie het systeem niet hebben geplaatst?", "Ja. Wij onderhouden regelmatig Salto-onderdelen die door anderen zijn geplaatst. Wij hebben de beheerderstoegang tot de software nodig, of de programmeerkaarten; heeft u die niet, dan kijken wij wat er zonder mogelijk is."),
        ("Leveren jullie Salto-onderdelen?", "Voor vervanging en uitbreiding van een bestaand systeem: ja. Voor een nieuw systeem adviseren wij EVVA Xesar."),
        ("Kan ik van Salto overstappen naar EVVA?", "Ja, gefaseerd. Deuren waarvan het Salto-beslag aan vervanging toe is, krijgen Xesar; de rest volgt later. Tijdens de overgang hebben gebruikers tijdelijk twee passen. Wij plannen dat per zone."),
        ("Wat kost onderhoud aan een Salto-systeem?", f"Storingen zonder contract tegen uurtarief plus onderdelen; met servicecontract {esc(PRIJZEN['servicecontract'][0])} tot {esc(PRIJZEN['servicecontract'][1])} per jaar, excl. btw. {PRIJS_DISCLAIMER}"),
        ("Werken jullie ook aan Salto-systemen buiten Twente?", "Ja, in heel Oost-Nederland. Zie het <a href=\"/werkgebied/\">werkgebied</a>."),
    ]

    body = hero("Salto onderhoud: storing, onderdelen en uitbreiding", intro) + wat + niet + specs
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Salto onderhoud", PAD)],
            extra_ld=[service_ld(PAD, "Salto onderhoud", omschrijving, merk="Salto")], formulier_kop="Storing melden of uitbreiding aanvragen",
            llms="Onderhoud, storingen, onderdelen en uitbreiding van bestaande Salto-systemen; nieuwe systemen plaatst Westendorp in EVVA.")
