"""/kennisbank/ — uitlegartikelen zonder datum (Lars, 23-09-2026: kennisbank voor vindbaarheid, SEO en GEO).
Een kennisbank in plaats van een blog: artikelen die een vraag beantwoorden blijven jaren geldig en worden door Google en
AI-zoekmachines als bron gebruikt; een blog met datums veroudert zichtbaar. Alleen algemene vakkennis, geen cijfers die niet
uit INPUT.md of van de fabrikant komen. Elk artikel: vraag als kop, antwoord in de eerste alinea, daarna uitleg, FAQ, formulier."""
from build import *

PAD = "/kennisbank/"

def _art_sleutel_kwijt():
    return (hero("Sleutel kwijt van het sluitplan: wat nu?",
        "Is een sleutel van een mechanisch sluitplan kwijt, dan weet u niet meer wie de deuren kan openen die bij die sleutel horen. "
        "Bepaal eerst welke deuren dat zijn, beslis dan of u die cilinders vervangt, en gebruik het moment om te bekijken of een elektronisch systeem dit probleem voortaan voorkomt.", kicker="Kennisbank")
    + sectie("Stap 1: welke deuren opent de kwijtgeraakte sleutel", p(
        "In een sluitplan hoort elke sleutel bij een groep deuren. Een gebruikerssleutel opent meestal één of enkele deuren, een groepssleutel een afdeling, een hoofdsleutel alles. "
        "Kijk in het sluitplan (de tabel van sleutels en cilinders) welke cilinders bij het nummer op de sleutel horen. Is er geen sluitplan meer, dan kan de leverancier van het systeem dat aan de hand van de sleutelkaart of het cilindernummer terughalen.",
        "Hoe hoger de sleutel in de hiërarchie, hoe groter het risico. Een verloren hoofdsleutel betekent in de praktijk dat alle cilinders in het plan onbetrouwbaar zijn."))
    + sectie("Stap 2: vervangen of afwachten", p(
        "Bij een gebruikerssleutel van een binnendeur zonder waardevolle inhoud kiezen veel bedrijven ervoor om alleen die cilinder te vervangen en de rest te laten zitten. "
        "Bij een buitendeur, een groeps- of hoofdsleutel, of een ruimte met medicijnen, geld of persoonsgegevens is vervangen de enige zekere keuze. Verzekeraars vragen daar bij een inbraak ook naar.",
        "Vervangen betekent: nieuwe cilinders voor alle deuren die de sleutel opende, nieuwe sleutels voor iedereen die die deuren gebruikt, en een bijgewerkt sluitplan. Bij een gecertificeerd profiel gaat dat op sleutelkaart, zodat niemand buiten u om sleutels kan laten bijmaken."), wit=True)
    + sectie("Stap 3: voorkomen dat het weer gebeurt", p(
        "Een sleutel raakt vroeg of laat opnieuw kwijt. Bij elektronische toegangscontrole blokkeert u een verloren pas in de software en blijft het slot zitten; dat is het grootste praktische verschil met een mechanisch plan. "
        "Veel bedrijven stappen daarom over op het moment dat een sleutel kwijt is, te beginnen met de deuren die het meest tellen: buitendeur, serverruimte, magazijn. De rest van het sluitplan kan mechanisch blijven, in hetzelfde systeem.",
        "Meer over de overstap leest u op <a href=\"/sluitplan/\">sluitplan</a> en <a href=\"/toegangscontrole/\">toegangscontrole</a>.") + acties()))

def _art_slot_cilinder_motor():
    return (hero("Elektronisch slot, elektronische cilinder of motorcilinder?",
        "Een elektronische cilinder vervangt alleen de cilinder, elektronisch beslag vervangt de deurkruk met lezer, en een motorcilinder draait de nachtschoot zelf. "
        "Welke past, hangt af van de deur: binnendeur, buitendeur of vluchtdeur.", kicker="Kennisbank")
    + sectie("Elektronische cilinder", p(
        "De elektronische cilinder heeft dezelfde maat als een gewone profielcilinder en gaat in het bestaande slot. Aan de buitenkant zit een knop met lezer; houdt u een geldige pas of tag voor de knop, dan koppelt de knop aan het mechaniek en kunt u draaien. "
        "Voordeel: geen aanpassing aan de deur, snel te plaatsen, ook op oudere deuren. Nadeel: u moet de knop nog steeds draaien om te ontgrendelen, en op een buitendeur is de vrije draaiknop aan de buitenkant een aandachtspunt voor de weerstandsklasse."))
    + sectie("Elektronisch beslag", p(
        "Elektronisch beslag vervangt het schild met de deurkruk. De lezer zit in het beslag; na een geldige pas koppelt de buitenkruk aan het slot en opent de deur zoals altijd. "
        "Voordeel: de deur voelt voor gebruikers als een gewone deur, en de mechanische cilinder blijft als noodopening. Nadeel: een houten deur heeft soms een uitsparing nodig, en het beslag moet passen bij de doornmaat en de krukhoogte van het bestaande slot."), wit=True)
    + sectie("Motorcilinder", p(
        "Een motorcilinder draait de nachtschoot en de dagschoot zelf, aangestuurd door een lezer, een tijdschema of een knop bij de receptie. De deur gaat dus echt op slot en weer van het slot zonder dat iemand draait. "
        "Dat maakt de motorcilinder de keuze voor buitendeuren, vluchtdeuren en deuren die op afstand moeten openen. Zie <a href=\"/motorcilinder/\">motorcilinder</a>."))
    + sectie("Welke voor welke deur", tabel([
        ("Binnendeur kantoor, vergaderruimte", "Elektronisch beslag; elektronische cilinder als het beslag niet past"),
        ("Serverruimte, medicijnkast, magazijn", "Elektronisch beslag of elektronische cilinder, met logging"),
        ("Buitendeur", "Motorcilinder, of wandlezer met elektrische sluitplaat"),
        ("Vluchtdeur", "Motorcilinder in combinatie met een gecertificeerd paniekslot of anti-paniekbeslag"),
        ("Hek, kast, techniekruimte", "Elektronische cilinder of hangslot met lezer"),
    ], kop=["Deur", "Passende oplossing"], bijschrift="Keuze per deurtype") + p("Alle soorten op een rij: <a href=\"/elektronische-sloten/\">elektronische sloten</a>.") + acties(), wit=True))

def _art_sluitplan():
    return (hero("Wat is een sluitplan en hoe stel je het op?",
        "Een sluitplan is de tabel die vastlegt welke sleutel welke deuren opent. Het is de basis van elk mechanisch sluitsysteem en de bron waaruit later een elektronisch systeem wordt opgezet. "
        "Een goed sluitplan begint bij de organisatie, niet bij de deuren.", kicker="Kennisbank")
    + sectie("Wat erin staat", p(
        "In de rijen staan de cilinders (elke deur één), in de kolommen de sleutels. Een kruisje betekent: deze sleutel opent deze cilinder. Zo ontstaat de hiërarchie: gebruikerssleutels voor één of enkele deuren, groepssleutels per afdeling of verdieping, een hoofdsleutel voor alles. "
        "Daarnaast legt het plan vast hoeveel sleutels per soort zijn uitgegeven en aan wie, en welk sleutelprofiel en welke certificering (bijvoorbeeld SKG) de cilinders hebben."))
    + sectie("Hoe u het opstelt", stappen([
        ("Lijst alle deuren", "Loop het pand rond en noteer per deur: naam, type (hout, staal, aluminium, glas), buiten- of binnendeur, vluchtdeur ja of nee, en het huidige slot."),
        ("Bepaal groepen gebruikers", "Niet per persoon, maar per rol: medewerker afdeling A, schoonmaak, techniek, directie, huurder. Rollen veranderen minder vaak dan mensen."),
        ("Koppel rollen aan deuren", "Per rol: welke deuren moeten open. Wees zuinig met hoofdsleutels; elke extra hoofdsleutel is een risico."),
        ("Kies profiel en certificering", "Een gecertificeerd sleutelprofiel op sleutelkaart voorkomt dat sleutels buiten u om worden bijgemaakt. Kies SKG-certificering waar de verzekeraar of de risicoanalyse dat vraagt."),
        ("Leg het beheer vast", "Wie geeft sleutels uit, wie houdt de lijst bij, wat gebeurt er bij vertrek van een medewerker of bij verlies."),
    ]), wit=True)
    + sectie("Van sluitplan naar elektronisch", p(
        "De stappen hierboven zijn precies de stappen die u ook zet voor elektronische toegangscontrole; alleen worden de sleutels dan passen en de tabel wordt software. "
        "Daarom loont het om het sluitplan op orde te hebben voordat u overstapt: de inventarisatie is dan al gedaan. Meer op <a href=\"/sluitplan/\">sluitplan</a>.") + acties()))

def _art_skg():
    return (hero("SKG-sterren en EN 1303: wat betekenen ze?",
        "SKG-sterren geven aan hoe lang een cilinder of beslag inbraakpogingen weerstaat volgens de Nederlandse keuring: één ster is basis, twee is zwaar, drie is het hoogste niveau. "
        "EN 1303 is de Europese norm die cilinders op meer eigenschappen beoordeelt, zoals duurzaamheid en brandwerendheid.", kicker="Kennisbank")
    + sectie("SKG in het kort", p(
        "SKG-IKOB keurt hang- en sluitwerk voor de Nederlandse markt. Een product krijgt sterren op basis van weerstand tegen inbraakmethoden zoals boren, trekken en slagsleutels, en de tijd die een inbreker nodig heeft. "
        "Verzekeraars en het Politiekeurmerk Veilig Wonen verwijzen naar dit sterrensysteem. Voor bedrijfspanden vraagt een verzekeraar vaak om SKG** of SKG*** op de buitendeuren; de polis of de risicoanalyse is daarin leidend."))
    + sectie("EN 1303 in het kort", p(
        "De Europese norm EN 1303 classificeert profielcilinders op een reeks eigenschappen, waaronder sluitveiligheid, duurzaamheid (aantal cycli), corrosiebestendigheid, brandwerendheid en weerstand tegen sabotage. Per eigenschap krijgt de cilinder een klasse. "
        "Een cilinder kan dus op het ene punt hoog scoren en op het andere laag; kijk daarom naar de eigenschappen die voor uw deur tellen. Voor een buitendeur telt sabotagebestendigheid, voor een deur in een vluchtroute brandwerendheid."), wit=True)
    + sectie("Wat het voor uw keuze betekent", lijst([
        "Buitendeuren en deuren met waardevolle inhoud: kies de klasse die de verzekeraar vraagt, meestal SKG** of hoger.",
        "Binnendeuren zonder verzekeringseis: een lagere klasse volstaat vaak; het sluitplan bepaalt wie erdoor mag, niet de ster.",
        "Elektronisch beslag en elektronische cilinders hebben eigen certificeringen; de mechanische cilinder in de deur blijft daarnaast bepalend voor de inbraakwerendheid.",
        "Een voorbeeld van een cilinder met SKG*** en het hoogste EN 1303-niveau op alle categorieën is <a href=\"/duurzaamheid/#magtec\">ABUS Magtec</a>.",
    ]) + p("Wij adviseren per deur welke klasse nodig is bij de inventarisatie; zie <a href=\"/sluitplan/\">sluitplan</a>.") + acties()))

def _art_batterij():
    return (hero("Batterijen in elektronische sloten: hoe lang gaan ze mee?",
        "Elektronisch beslag en elektronische cilinders werken op batterijen, niet op netstroom. De levensduur hangt af van het aantal openingen per dag en van de instellingen; "
        "het systeem waarschuwt ruim van tevoren, en bij een lege batterij is er altijd een noodopening.", kicker="Kennisbank")
    + sectie("Waarom batterijen en geen kabels", p(
        "Een deur met batterijvoeding heeft geen kabel naar het slot nodig. Dat is de reden dat elektronische toegangscontrole op bestaande deuren kan worden geplaatst zonder frezen in wanden en kozijnen. "
        "Alleen wandlezers met elektrische sluitplaat en motorcilinders die op afstand worden aangestuurd krijgen vaste voeding; die zitten meestal op de buitendeur."))
    + sectie("Wat de levensduur bepaalt", lijst([
        "Het aantal openingen: een deur die honderden keren per dag opent, verbruikt meer dan een kastdeur.",
        "Online of offline: een deur die draadloos in verbinding staat met de software verbruikt meer dan een offline deur die de rechten van de pas leest.",
        "Temperatuur: buitendeuren in de kou verbruiken sneller.",
        "Instellingen: een lange ontgrendeltijd of veel signalen kosten energie.",
    ]) + p("Omdat dit per deur verschilt, noemen wij geen vaste levensduur; de fabrikant geeft per product een indicatie en de software houdt per deur de batterijspanning bij."), wit=True)
    + sectie("Wat er gebeurt als de batterij leeg raakt", p(
        "De software en het beslag zelf melden een lage batterij weken van tevoren, met een signaal bij de deur of een melding in het beheer. Vervangen is een kwestie van minuten en kan door uw eigen beheerder. "
        "Raakt een batterij toch leeg, dan opent de deur met een noodvoeding tegen de lezer of met de mechanische noodcilinder; de deur blijft dus nooit dicht zonder uitweg. In een <a href=\"/service-en-beheer/\">onderhoudsafspraak</a> nemen wij het vervangen op ons.") + acties()))

ARTIKELEN = [
    ("sleutel-kwijt-sluitplan", "Sleutel kwijt van het sluitplan: wat nu?",
     "Bepaal welke deuren de sleutel opent, beslis over vervangen, en voorkom herhaling met een pas die u zelf blokkeert.",
     "Sleutel kwijt van het sluitplan: welke deuren opent hij, wanneer vervangt u cilinders, en hoe voorkomt elektronische toegangscontrole herhaling.", _art_sleutel_kwijt, [
        ("Moet ik na een verloren sleutel alle cilinders vervangen?", "Alleen de cilinders die de verloren sleutel opende. Bij een gebruikerssleutel is dat vaak één deur; bij een hoofdsleutel zijn het alle deuren in het plan."),
        ("Kan iemand een gevonden sleutel laten bijmaken?", "Bij een gecertificeerd sleutelprofiel op sleutelkaart niet: de leverancier maakt alleen sleutels bij op vertoon van de kaart. Bij een vrij profiel kan elke sleutelservice dat wel."),
        ("Is overstappen op elektronisch duurder dan cilinders vervangen?", "Per deur kost een elektronisch slot meer dan een cilinder, maar het is de laatste keer dat u om een verloren sleutel iets vervangt. Richtprijzen staan op de pagina wat kost toegangscontrole."),
    ]),
    ("elektronisch-slot-cilinder-motorcilinder", "Elektronisch slot, cilinder of motorcilinder?",
     "Drie soorten elektronische sloten, en welke bij een binnendeur, buitendeur of vluchtdeur past.",
     "Het verschil tussen een elektronische cilinder, elektronisch beslag en een motorcilinder, en welke past bij binnendeur, buitendeur of vluchtdeur.", _art_slot_cilinder_motor, [
        ("Kan elektronisch beslag op elke deur?", "Op de meeste houten, stalen en aluminium deuren wel, mits het slot een gangbare doornmaat en krukhoogte heeft. Glazen deuren en smalle profielen vragen een specifieke uitvoering; dat beoordelen wij bij de inventarisatie."),
        ("Blijft de mechanische sleutel werken?", "Bij elektronisch beslag blijft de mechanische cilinder als noodopening zitten. Bij een elektronische cilinder vervangt de elektronische knop de sleutel; een noodvoeding tegen de lezer opent de deur bij een lege batterij."),
        ("Is een motorcilinder ook geschikt voor een binnendeur?", "Technisch wel, maar het is zelden nodig. Een motorcilinder is bedoeld voor deuren die echt vergrendeld moeten zijn en op afstand of automatisch moeten openen, zoals buitendeuren en vluchtdeuren."),
    ]),
    ("wat-is-een-sluitplan", "Wat is een sluitplan en hoe stel je het op?",
     "De tabel van sleutels en cilinders, stap voor stap opgezet vanuit rollen in plaats van personen.",
     "Wat een sluitplan is, wat erin staat en hoe u het in vijf stappen opstelt vanuit rollen en deuren, als basis voor mechanisch of elektronisch sluiten.", _art_sluitplan, [
        ("Wat is het verschil tussen een sluitplan en een sleutelplan?", "In de praktijk worden beide woorden voor hetzelfde gebruikt: de tabel die vastlegt welke sleutel welke cilinder opent. Sluitplan is de gangbare vakterm."),
        ("Hoeveel hoofdsleutels zijn verstandig?", "Zo min mogelijk. Elke hoofdsleutel opent alles; verlies ervan betekent dat het hele plan onbetrouwbaar wordt. Geef groepssleutels waar een hoofdsleutel niet echt nodig is."),
        ("Kan een bestaand sluitplan worden uitgebreid?", "Ja, zolang het profiel nog leverbaar is en er in het plan ruimte is gehouden voor nieuwe deuren en sleutels. Een goed plan reserveert die ruimte vooraf."),
    ]),
    ("skg-sterren-en-1303", "SKG-sterren en EN 1303: wat betekenen ze?",
     "Wat de sterren en de Europese klassen zeggen over inbraakwerendheid, en welke klasse u voor welke deur kiest.",
     "Wat SKG-sterren en de Europese norm EN 1303 zeggen over cilinders en beslag, wat verzekeraars vragen, en welke klasse past bij welke deur.", _art_skg, [
        ("Is SKG*** altijd nodig?", "Nee. Verzekeraars vragen de hogere klassen voor buitendeuren en ruimtes met waardevolle inhoud. Voor binnendeuren zonder verzekeringseis bepaalt het sluitplan de veiligheid, niet het aantal sterren."),
        ("Geldt SKG ook voor elektronische sloten?", "Elektronisch beslag en elektronische cilinders hebben eigen certificeringen. De mechanische cilinder die in de deur zit, blijft daarnaast bepalend voor de inbraakwerendheid; kies die dus op de juiste klasse."),
        ("Wie bepaalt welke klasse mijn pand nodig heeft?", "Uw verzekeraar en uw eigen risicoanalyse. Wij vertalen dat bij de inventarisatie naar een klasse per deur."),
    ]),
    ("batterijen-elektronische-sloten", "Batterijen in elektronische sloten",
     "Waarom sloten op batterijen werken, wat de levensduur bepaalt en wat er gebeurt als een batterij leeg raakt.",
     "Hoe lang batterijen in elektronische sloten meegaan, wat het verbruik bepaalt, hoe het systeem waarschuwt en hoe de deur opent bij een lege batterij.", _art_batterij, [
        ("Kan ik batterijen zelf vervangen?", "Ja. Het beslag of de cilinder gaat open met een sleuteltje of schroef, de batterijen worden gewisseld en de rechten blijven bewaard. Uw beheerder kan dat zelf, of wij nemen het op in het onderhoud."),
        ("Gaat de deur dicht als de batterij leeg is?", "Nee, de deur blijft niet zonder uitweg. Van binnen opent de deur altijd mechanisch; van buiten opent u met een noodvoeding tegen de lezer of met de mechanische noodcilinder."),
        ("Verbruikt een online deur meer dan een offline deur?", "Ja. Een deur die draadloos in verbinding staat met de software verbruikt meer dan een offline deur die de rechten van de pas zelf leest. Daarom zetten veel bedrijven alleen de buitendeur online."),
    ]),
]

def bouw():
    # ---- artikelen ----
    for slug, kop, samenvatting, omschrijving, fn, faq in ARTIKELEN:
        pad = f"{PAD}{slug}/"
        artikel_ld = {"@type": "Article", "@id": SITE + pad + "#artikel", "headline": kop, "description": omschrijving, "inLanguage": "nl-NL",
                      "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@id": SITE + pad + "#webpage"}, "isPartOf": {"@id": WEBSITE_ID}}
        schrijf(pad, kop, omschrijving, fn(), faq=faq, kruimelpad=[("Home", "/"), ("Kennisbank", PAD), (kop, pad)], extra_ld=[artikel_ld],
                llms=samenvatting)
    # ---- overzicht ----
    kaarten = "".join(f'<div><h3><a href="{PAD}{slug}/">{esc(kop)}</a></h3><p>{esc(omschrijving)}</p><p><a class="meer" href="{PAD}{slug}/">Lees het artikel</a></p></div>'
                      for slug, kop, _, omschrijving, *_ in ARTIKELEN)
    body = (hero("Kennisbank toegangscontrole en sluitsystemen",
                 "Uitleg over toegangscontrole, elektronische sloten, sluitplannen en certificering, geschreven om een vraag te beantwoorden. "
                 "Geen datums, geen nieuws: wat hier staat blijft geldig. Staat uw vraag er niet bij, stel hem via het formulier of bel ons.", kicker="Kennisbank")
            + sectie("Artikelen", f'<div class="kolommen kolommen--2">{kaarten}</div>')
            + sectie("Liever direct advies", p("De artikelen leggen uit hoe het werkt; wat er in uw pand past, bepalen wij samen bij de inventarisatie op locatie. "
                                                "Zie <a href=\"/toegangscontrole/\">toegangscontrole</a> voor onze aanpak.") + acties(), wit=True))
    schrijf(PAD, "Kennisbank toegangscontrole", "Uitleg over toegangscontrole, elektronische sloten, sluitplannen, SKG en batterijen: artikelen die een vraag beantwoorden en geldig blijven.",
            body, kruimelpad=[("Home", "/"), ("Kennisbank", PAD)], paginatype="WebPage",
            llms="Overzicht van de kennisbank: uitlegartikelen over sleutelverlies, soorten elektronische sloten, sluitplannen, SKG en EN 1303, batterijen.")
