"""/kosten/ — hoofdzoekwoord: toegangscontrole kosten. De belangrijkste GEO-pagina; zonder prijzen uit INPUT §B5 niet live."""
from build import *

PAD = "/kosten/"

def bouw():
    titel = "Wat kost toegangscontrole per deur"
    omschrijving = ("Richtprijzen per deur voor beslag, cilinders, motorcilinders en wandlezers, wat de prijs bepaalt, drie rekenvoorbeelden en wat er niet in zit.")
    P = PRIJZEN
    intro = (f"Elektronische toegangscontrole kost geplaatst {esc(P['beslag'][0])} tot {esc(P['beslag'][1])} per deur voor elektronisch beslag en "
             f"{esc(P['cilinder_xesar'][0])} tot {esc(P['cilinder_xesar'][1])} voor een elektronische cilinder, excl. btw, plus de beheersoftware. "
             f"Een motorcilinder of een online wandlezer kost meer. {PRIJS_DISCLAIMER}")
    datum_html = lambda d: f'<p class="laatst">Laatst bijgewerkt: {esc(d)}</p>'

    strook = sectie("Richtprijzen per deur", tabel([
        ("Elektronisch beslag, geplaatst", esc(P['beslag'][0]), esc(P['beslag'][1]), esc(P['beslag'][2])),
        ("Elektronische cilinder (Xesar), geplaatst", esc(P['cilinder_xesar'][0]), esc(P['cilinder_xesar'][1]), esc(P['cilinder_xesar'][2])),
        ("Motorcilinder (EMZY), geplaatst", esc(P['emzy'][0]), esc(P['emzy'][1]), esc(P['emzy'][2])),
        ("Wandlezer met elektrische sluitplaat", esc(P['wandlezer'][0]), esc(P['wandlezer'][1]), esc(P['wandlezer'][2])),
        ("Beheersoftware, per jaar", esc(P['software'][0]), esc(P['software'][1]), esc(P['software'][2])),
        ("Infrezen houten deur", esc(P['infrezen'][0]), esc(P['infrezen'][1]), esc(P['infrezen'][2])),
        ("Mechanisch sluitplan, per cilinder", esc(P['mech_cilinder'][0]), esc(P['mech_cilinder'][1]), esc(P['mech_cilinder'][2])),
        ("Servicecontract, per jaar", esc(P['servicecontract'][0]), esc(P['servicecontract'][1]), esc(P['servicecontract'][2])),
        ("Inventarisatie op locatie", "zonder kosten" if INVENTARISATIE_GRATIS else INV("prijs inventarisatie"), "", ""),
    ], kop=["Situatie", "Vanaf", "Tot", "Wat zit erin"], bijschrift="Richtprijzen toegangscontrole, excl. btw")
        + p("Alle bedragen excl. btw. " + PRIJS_DISCLAIMER))

    bepaalt = sectie("Wat de prijs bepaalt", '<div class="kolommen kolommen--3">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in [
        ("Aantal deuren", "De software en de inrichting zijn vaste kosten; per deur wordt het goedkoper naarmate er meer deuren zijn."),
        ("Deurtype", "Een binnendeur met beslag is het goedkoopst; een buitendeur met meerpuntssluiting vraagt een motorcilinder, een glazen deur een wandlezer."),
        ("Offline of online", "Offline deuren zijn goedkoper. Online betaalt u alleen waar u live inzicht of bediening op afstand nodig heeft."),
        ("Beheer", "Zelf beheren kost niets extra; beheer door ons of een servicecontract zijn jaarlijkse kosten."),
        ("Infrezen", "Houten deuren die een uitsparing nodig hebben voor beslag: een vast bedrag per deur, in eigen werkplaats."),
        ("Bestaande situatie", "Een bestaand EVVA-sluitplan of bruikbaar beslag drukt de prijs; losse sloten van verschillende merken juist niet."),
    ]) + "</div>", wit=True)

    voorbeelden = sectie("Drie rekenvoorbeelden uit de praktijk", '<div class="kolommen kolommen--3">' + "".join(
        f"<div><h3>{esc(k)}</h3><p>{esc(t)}</p></div>" for k, t in REKENVOORBEELDEN) + "</div>" + p(PRIJS_DISCLAIMER))

    nietin = sectie("Wat niet in de prijs zit", lijst([
        "Btw (alle bedragen op deze pagina zijn excl. btw).",
        "Bouwkundige aanpassingen aan kozijnen of deuren, anders dan het infrezen.",
        "Bekabeling en netvoeding voor online wandlezers, als die er nog niet ligt.",
        "Deurdrangers, deurautomaten en intercoms, tenzij in de offerte opgenomen.",
        "Passen en tags boven het aantal in de offerte.",
    ]), wit=True)

    terugverdien = sectie("Terugverdientijd tegenover een mechanisch sluitplan", p(
        f"Raakt in een mechanisch sluitplan een hoofdsleutel kwijt, dan moet u de cilinders vervangen van elke deur waar die sleutel op paste: "
        f"{esc(P['mech_cilinder'][0])} tot {esc(P['mech_cilinder'][1])} per cilinder plus montage. Bij twintig deuren is dat één keer het verschil met een elektronisch systeem, "
        "waar een verloren pas de prijs van één pas kost. Tel daarbij de uren die het bijhouden van een sleuteladministratie kost, en het omslagpunt ligt bij de meeste bedrijven bij de eerste verloren sleutel.",
        "Meer over dat contrast op <a href=\"/sluitplan/\">sluitplan</a>."))

    faq = [
        ("Waarom staan hier bandbreedtes en geen vaste prijzen?", "Omdat de deur bepaalt wat erop past. Twee kantoren met tien deuren kunnen verschillen in deurtype, beslag en of de buitendeur online moet. Na de inventarisatie krijgt u een offerte met een vaste prijs per deur."),
        ("Is de inventarisatie echt zonder kosten?", "Ja, de inventarisatie op locatie is gratis en zonder verplichting." if INVENTARISATIE_GRATIS else INV("antwoord over kosten inventarisatie")),
        ("Wat kost het beheer per jaar?", f"Beheersoftware: {esc(P['software'][0])} tot {esc(P['software'][1])} per jaar, excl. btw. Een servicecontract met onderhoud en voorrang bij storingen: {esc(P['servicecontract'][0])} tot {esc(P['servicecontract'][1])} per jaar."),
        ("Kan ik in fasen betalen of plaatsen?", "Plaatsen in fasen kan altijd: eerst de buitendeur en de ruimtes met risico, later de rest, in hetzelfde systeem. Betaling per fase spreken wij in de offerte af."),
        ("Zijn er subsidies of fiscale regelingen?", "Voor toegangscontrole bestaat geen aparte subsidie. Als bedrijfsmiddel valt de investering onder de gewone afschrijving; overleg daarover met uw accountant, wij geven daar geen advies over."),
    ]

    body = hero("Wat kost toegangscontrole", intro, extra=datum_html(datum_nl(VANDAAG))) + strook + bepaalt + voorbeelden + nietin + terugverdien
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Kosten", PAD)],
            extra_ld=[service_ld(PAD, "Toegangscontrole kosten", omschrijving)],
            llms="Richtprijzen per deur (beslag, cilinder, motorcilinder, wandlezer, software, infrezen, sluitplan, servicecontract), wat de prijs bepaalt, drie rekenvoorbeelden, wat er niet in zit, terugverdientijd.")
