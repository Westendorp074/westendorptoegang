"""/elektronische-sloten/ — hoofdzoekwoord: elektronisch slot bedrijf. Productinvalshoek."""
from build import *

PAD = "/elektronische-sloten/"

def bouw():
    titel = "Elektronische sloten voor bedrijven"
    omschrijving = ("Elektronisch beslag, cilinder, motorcilinder of wandlezer: welk elektronisch slot past op welke deur, batterij en levensduur, en wat wij zelf infrezen.")
    intro = ("Een elektronisch slot vervangt de sleutel door een pas, tag of telefoon en past op de meeste bestaande deuren. "
             "Er zijn vier soorten: elektronisch beslag, elektronische cilinder, motorcilinder en wandlezer met elektrische sluitplaat. "
             "Welke past, hangt af van de deur en van wat de deur moet doen.")
    foto = beeld("elektronisch-beslag.jpg", "Elektronisch beslag op een houten binnendeur", onderschrift=INV("onderschrift foto elektronisch beslag"))

    soorten = sectie("De vier soorten elektronische sloten", '<div class="kolommen kolommen--2">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in [
        ("Elektronisch beslag", "De deurkruk met lezer erin. Buiten draait de kruk pas mee na een geldige pas, binnen altijd. Op batterijen, geen kabel. De standaardkeuze voor binnendeuren in kantoren, scholen en zorg."),
        ("Elektronische cilinder", "Vervangt de mechanische cilinder in het bestaande slot; de rest van de deur blijft. Op batterijen. Geschikt als het beslag moet blijven, bij smalle deuren of bij kasten en hekken met een cilinderslot."),
        ("Motorcilinder", "Een cilinder met een motor die de nachtschoot zelf uitdraait en intrekt. De deur gaat dus echt op slot, niet alleen in de dag. Voor buitendeuren, vluchtdeuren en deuren die op afstand moeten openen. Zie <a href=\"/motorcilinder/\">motorcilinder</a>."),
        ("Wandlezer met elektrische sluitplaat", "De lezer zit naast de deur, de sluitplaat in het kozijn. Bekabeld en online: de receptie kan de deur op afstand openen en elke passage is direct zichtbaar. Voor entrees, slagbomen van derden en deuren met deurautomaat."),
    ]) + "</div>" + p("Ons hoofdmerk voor elektronisch is EVVA (<a href=\"/evva-xesar/\">Xesar</a> en <a href=\"/motorcilinder/\">EMZY</a>). Daarnaast plaatsen wij elektronische sloten van ASSA ABLOY, waarvan wij ook officieel partner zijn; welk merk past, hangt af van de deur en het bestaande slot."))

    deurtypes = sectie("Wat past op welke deur", tabel([
        ("Houten binnendeur", "Elektronisch beslag of elektronische cilinder", "Uitsparing voor beslag frezen wij zelf in."),
        ("Houten buitendeur", "Motorcilinder of elektronische cilinder", "Meerpuntssluiting: motorcilinder, zodat alle punten sluiten."),
        ("Stalen deur", "Elektronische cilinder of wandlezer met sluitplaat", "Beslag afhankelijk van het slot in de deur."),
        ("Aluminium of kunststof profieldeur", "Elektronische cilinder, motorcilinder of wandlezer", "Smal profiel: cilinder past vrijwel altijd."),
        ("Glazen deur", "Wandlezer met elektrische sluitplaat of speciaal glasbeslag", "Bepalen wij per deur tijdens de inventarisatie."),
        ("Brandwerende deur", "Gecertificeerd beslag of cilinder", "Alleen onderdelen met een toelating voor die deur; de deurdranger blijft."),
    ], kop=["Deur", "Meestal", "Let op"], bijschrift="Welk elektronisch slot past op welke deur")
        + p("Twijfelt u over een deur? Stuur een foto mee in het formulier onderaan, dan zeggen wij vooraf wat erop past."), wit=True)

    specs = sectie("Specificaties per soort", tabel([
        ("Voeding", "Batterij", "Batterij", "Batterij, optioneel netvoeding", "Netvoeding (bekabeld)"),
        ("Verbinding", "Offline of draadloos online", "Offline of draadloos online", "Offline of online", "Online"),
        ("Vergrendeling", "Kruk buiten vrijloop, dagschoot", "Cilinder blokkeert", "Nachtschoot motorisch", "Sluitplaat geeft deur vrij"),
        ("Op afstand openen", "Alleen online-uitvoering", "Alleen online-uitvoering", "Ja", "Ja"),
        ("Bestaande deur", "Kruk vervangen, soms infrezen", "Cilinder wisselen", "Cilinder wisselen", "Sluitplaat in kozijn, kabel"),
        ("Batterijmelding", "In de software en bij de deur", "In de software en bij de deur", "In de software en bij de deur", "Niet van toepassing"),
    ], kop=["", "Elektronisch beslag", "Elektronische cilinder", "Motorcilinder", "Wandlezer + sluitplaat"], bijschrift="Specificaties van de vier soorten elektronische sloten")
        + p("De merkspecifieke gegevens (identificatie, certificering, uitbreidbaarheid) staan op <a href=\"/evva-xesar/\">EVVA Xesar</a> en <a href=\"/motorcilinder/\">EVVA EMZY</a>."))

    batterij = sectie("Batterij en levensduur", p(
        "Elektronisch beslag en elektronische cilinders werken op gangbare batterijen. Hoe lang die meegaan, hangt af van het aantal passages per dag en van de omgeving; "
        "een buitendeur in de vorst vraagt meer dan een kantoordeur. Het systeem meldt ruim van tevoren, in de software en bij de deur, dat de batterij op raakt. "
        "Is hij toch leeg, dan opent u de deur met een noodvoeding of een mechanische noodsleutel; u staat nooit buiten.",
        "Batterijen vervangen kan onderdeel zijn van een servicecontract. Zie <a href=\"/service-en-beheer/\">service en beheer</a>."), wit=True)

    infrezen = sectie("Wat wij zelf infrezen", p(
        "Elektronisch beslag heeft in een houten deur vaak een uitsparing nodig die er nu niet is. Die frezen wij zelf in, in eigen beheer, zodat er geen deurenfabrikant tussen zit en de deur niet vervangen hoeft te worden. "
        f"Wat dat kost staat bij <a href=\"/kosten/\">kosten</a> (infrezen: {prijs('infrezen')})."))

    drangers = sectie("Deurdrangers en deurautomaten", p(
        f"Een elektronisch slot werkt alleen als de deur ook dichtvalt. Daarom leveren en stellen wij deurdrangers en deurautomaten van {esc(DEURDRANGERS)} af, "
        "en zijn wij door de fabrikant getraind in het afstellen ervan: sluitkracht, sluitsnelheid en eindslag afgestemd op de deur en op de brandwerende eisen. "
        "Bij een deurautomaat combineren wij de lezer met de automaat, zodat de deur na een geldige pas zelf opengaat."))

    faq = [
        ("Kan een elektronisch slot op elke deur?", "Op vrijwel elke deur past een van de vier soorten. De uitzonderingen zijn glazen deuren zonder profiel en monumentale deuren; die bekijken wij per stuk."),
        ("Wat als de batterij leeg is?", "Het systeem waarschuwt weken van tevoren. Is de batterij toch leeg, dan opent u met een noodvoeding tegen de lezer of met de mechanische noodsleutel die bij elk slot hoort."),
        ("Blijft mijn deurdranger of brandwerende deur goedgekeurd?", "Ja, mits wij onderdelen gebruiken met een toelating voor die deur. Bij brandwerende deuren gebruiken wij alleen gecertificeerd beslag en laten wij de dranger zitten."),
        ("Kan ik met één pas alle deuren openen?", "Ja. Eén pas, tag of telefoon werkt op elektronisch beslag, cilinders, motorcilinders en wandlezers binnen hetzelfde systeem; de rechten per deur stelt u in de software in."),
        ("Wat kost een elektronisch slot voor een bedrijf?", f"Een elektronisch slot (smart lock) kost geplaatst {prijs('slot')}, {BTW_TEKST}; welke uitvoering past, hangt af van de deur en de beveiligingseisen. Alle vanaf-prijzen op <a href=\"/kosten/\">wat kost toegangscontrole</a>."),
    ]

    body = hero("Elektronische sloten voor bedrijven: welk slot op welke deur", intro, foto) + soorten + deurtypes + specs + batterij + infrezen + drangers
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Elektronische sloten", PAD)],
            extra_ld=[service_ld(PAD, "Elektronische sloten", omschrijving)],
            llms="De vier soorten elektronische sloten, welk slot op welke deur, specificatietabel, batterij en levensduur, infrezen van houten deuren.")
