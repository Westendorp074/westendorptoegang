"""/kosten/ — hoofdzoekwoord: toegangscontrole kosten. De belangrijkste GEO-pagina. Vanaf-prijzen uit CONFIG; regels zonder prijs vervallen."""
from build import *

PAD = "/kosten/"

def bouw():
    titel = "Wat kost toegangscontrole per deur"
    omschrijving = ("Vanaf-prijzen voor elektronische sloten en EVVA AirKey, wat de prijs bepaalt en wat er niet in zit. "
                    "Excl. btw, bijgewerkt door Westendorp Toegangscontrole.")
    intro = (f"Een elektronisch slot (smart lock) kost geplaatst {prijs('slot')}, {BTW_TEKST}. Welk slot het wordt, hangt af van de deur en van de beveiligingseisen "
             f"van uw pand; voor elk type bedrijf is er een passende uitvoering. Een EVVA AirKey-startpakket kost {prijs('airkey_start', False)}. {PRIJS_DISCLAIMER}")
    datum_html = lambda d: f'<p class="laatst">Laatst bijgewerkt: {esc(d)}</p>'

    rijen = [(esc(oms), f"vanaf € {v}" if v else "op aanvraag", esc(een)) for oms, v, een in PRIJZEN.values()]
    rijen.append(("Inventarisatie op locatie", "zonder kosten" if INVENTARISATIE_GRATIS else INV("prijs inventarisatie"), ""))
    strook = sectie("Vanaf-prijzen", tabel(rijen, kop=["Situatie", "Prijs", "Eenheid"], bijschrift="Vanaf-prijzen toegangscontrole, excl. btw")
        + p(f"Alle bedragen {BTW_TEKST}, geplaatst. Regels met 'op aanvraag' hangen zo sterk af van de deur en het aantal dat wij ze pas na de inventarisatie noemen. {PRIJS_DISCLAIMER}"))

    bepaalt = sectie("Wat de prijs bepaalt", '<div class="kolommen kolommen--3">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in [
        ("Beveiligingseisen", "Een binnendeur naar een kantoor vraagt iets anders dan een medicijnruimte of een buitendeur; de klasse van het slot bepaalt de prijs."),
        ("Aantal deuren", "De software en de inrichting zijn vaste kosten; per deur wordt het goedkoper naarmate er meer deuren zijn."),
        ("Deurtype", "Een binnendeur met beslag is het goedkoopst; een buitendeur met meerpuntssluiting vraagt een motorcilinder, een glazen deur een wandlezer."),
        ("Offline of online", "Offline deuren zijn goedkoper. Online betaalt u alleen waar u live inzicht of bediening op afstand nodig heeft."),
        ("Beheer", "Zelf beheren kost niets extra; beheer door ons of een servicecontract zijn jaarlijkse kosten."),
        ("Infrezen en bestaande situatie", "Houten deuren die een uitsparing nodig hebben: een vast bedrag per deur. Een bestaand EVVA-sluitplan of bruikbaar beslag drukt de prijs."),
    ]) + "</div>", wit=True)

    voorbeelden = sectie("Rekenvoorbeelden uit de praktijk", '<div class="kolommen kolommen--3">' + "".join(
        f"<div><h3>{esc(k)}</h3><p>{esc(t)}</p></div>" for k, t in REKENVOORBEELDEN) + "</div>" + p(PRIJS_DISCLAIMER)) if REKENVOORBEELDEN else ""

    nietin = sectie("Wat niet in de prijs zit", lijst([
        f"Btw (alle bedragen op deze pagina zijn {BTW_TEKST}).",
        "Bouwkundige aanpassingen aan kozijnen of deuren, anders dan het infrezen.",
        "Bekabeling en netvoeding voor online wandlezers, als die er nog niet ligt.",
        "Deurdrangers, deurautomaten en intercoms, tenzij in de offerte opgenomen.",
        "Passen en tags boven het aantal in de offerte.",
    ]), wit=not REKENVOORBEELDEN)

    terugverdien = sectie("Terugverdientijd tegenover een mechanisch sluitplan", p(
        "Raakt in een mechanisch sluitplan een hoofdsleutel kwijt, dan moet u de cilinders vervangen van elke deur waar die sleutel op paste, plus montage. "
        "Bij twintig deuren is dat al snel het verschil met een elektronisch systeem, waar een verloren pas de prijs van één pas kost. "
        "Tel daarbij de uren die het bijhouden van een sleuteladministratie kost, en het omslagpunt ligt bij de meeste bedrijven bij de eerste verloren sleutel.",
        "Meer over dat contrast op <a href=\"/sluitplan/\">sluitplan</a>."))

    faq = [
        ("Waarom staan hier vanaf-prijzen en geen vaste prijzen?", "Omdat de deur en de beveiligingseis bepalen wat erop past. Twee kantoren met tien deuren kunnen verschillen in deurtype, beslag en of de buitendeur online moet. Na de inventarisatie krijgt u een offerte met een vaste prijs per deur."),
        ("Is de inventarisatie echt zonder kosten?", "Ja, de inventarisatie op locatie is gratis en zonder verplichting." if INVENTARISATIE_GRATIS else INV("antwoord over kosten inventarisatie")),
        ("Wat kost EVVA AirKey?", f"Een AirKey-startpakket kost {prijs('airkey_start', False)}, {BTW_TEKST}. Daarmee regelt u een of enkele deuren via de telefoon; uitbreiden kan per cilinder. Zie <a href=\"/evva-xesar/\">EVVA Xesar en AirKey</a>."),
        ("Kan ik in fasen betalen of plaatsen?", "Plaatsen in fasen kan altijd: eerst de buitendeur en de ruimtes met risico, later de rest, in hetzelfde systeem. Betaling per fase spreken wij in de offerte af."),
        ("Zijn er subsidies of fiscale regelingen?", "Voor toegangscontrole bestaat geen aparte subsidie. Als bedrijfsmiddel valt de investering onder de gewone afschrijving; overleg daarover met uw accountant, wij geven daar geen advies over."),
    ]

    body = hero("Wat kost toegangscontrole", intro, extra=datum_html(datum_nl(VANDAAG))) + strook + bepaalt + voorbeelden + nietin + terugverdien
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Kosten", PAD)],
            extra_ld=[service_ld(PAD, "Toegangscontrole kosten", omschrijving)],
            llms="Vanaf-prijzen (elektronisch slot, AirKey-startpakket; overige op aanvraag), wat de prijs bepaalt, wat er niet in zit, terugverdientijd.")
