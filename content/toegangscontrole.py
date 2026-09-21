"""/toegangscontrole/ — hoofdzoekwoord: toegangscontrolesysteem. Uitleg voor een leek plus onze aanpak."""
from build import *

PAD = "/toegangscontrole/"

def bouw():
    titel = "Toegangscontrolesysteem voor uw pand"
    omschrijving = ("Wat een toegangscontrolesysteem is, wanneer het loont, offline of online, en hoe Westendorp het aanpakt van inventarisatie tot beheer.")
    intro = ("Een toegangscontrolesysteem vervangt de sleutel door een pas, tag of telefoon en legt per deur vast wie er "
             "wanneer in mag. Raakt iemand zijn pas kwijt, dan blokkeert u die in de software; de deur en het slot blijven zoals ze zijn.")
    foto = beeld("toegangscontrole-lezer.jpg", "Wandlezer naast een kantoordeur", onderschrift=INV("onderschrift foto toegangscontrole"))

    wanneer = sectie("Wanneer loont toegangscontrole", p(
        "Een mechanisch sluitplan werkt prima zolang niemand een sleutel kwijtraakt en de organisatie niet verandert. "
        "In de praktijk ziet het er anders uit. Dit zijn de momenten waarop bedrijven ons bellen:") + lijst([
        "Een sleutel uit het sluitplan is kwijt en niemand weet meer welke deuren daarmee opengaan.",
        "Nieuwbouw, verbouwing of verhuizing: de deuren worden toch al aangepakt.",
        "Het sluitplan is versleten of uitgebreid met losse sloten waar niemand overzicht over heeft.",
        "Een verzekeraar of auditor eist dat u kunt aantonen wie wanneer waar was.",
        "Groei in medewerkers, flexwerken, vrijwilligers of gasten die maar een dag of een week toegang nodig hebben.",
        "U wilt gewoon van de sleutelbos af.",
    ]))

    soorten = sectie("Offline, online of cloud: welke variant past", p(
        "Elk systeem regelt wie de deur mag openen. Het verschil zit in hoe de rechten bij de deur komen en hoe snel een wijziging doorwerkt.")
        + tabel([
            ("Offline", "De deur leest de rechten van de pas zelf; u werkt de passen bij op een programmeerstation of updater bij de entree.", "Kleine en middelgrote panden, weinig wijzigingen, laagste kosten per deur."),
            ("Online (bekabeld of draadloos)", "Elke deur staat in verbinding met de beheersoftware; een wijziging is direct actief en u ziet live wie waar is.", "Panden met veel wisselingen, hoge beveiligingseisen of een receptie die deuren op afstand moet openen."),
            ("Cloud", "Zoals online, maar de software draait bij de leverancier en u beheert via de browser, ook vanaf een andere locatie.", "Meerdere vestigingen, beheer op afstand, geen eigen server."),
        ], kop=["Variant", "Hoe het werkt", "Past bij"], bijschrift="Vergelijking offline, online en cloud")
        + p("Bij EVVA Xesar zijn offline en online deuren te combineren in één systeem: de buitendeur online, de kantoren offline. Dat houdt de kosten in de hand. "
            "Zie <a href=\"/evva-xesar/\">EVVA Xesar</a>."), wit=True)

    middelen = sectie("Pas, tag, telefoon of code", '<div class="kolommen kolommen--4">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in [
        ("Pas", "Kaartformaat, past in de portemonnee, te bedrukken met naam en foto. Gangbaar bij kantoren en scholen."),
        ("Tag", "Sleutelhanger, robuust, handig voor monteurs en vrijwilligers die hem aan de sleutelbos hangen."),
        ("Telefoon", "Toegang via een app of virtuele pas. Geen uitgifte van passen, wel afhankelijk van een opgeladen telefoon."),
        ("Code", "Toetsenbord bij de deur, zonder pas. Praktisch voor bezoekers, minder veilig omdat codes worden doorgegeven."),
    ]) + "</div>")

    deuren = sectie("Wat gebeurt er met onze bestaande deuren", p(
        "In de meeste gevallen niets ingrijpends. Op een binnendeur komt elektronisch beslag of een elektronische cilinder in plaats van het huidige slot; "
        "de deur, het kozijn en de scharnieren blijven. Op een buitendeur of vluchtdeur plaatsen wij een motorcilinder of een wandlezer met elektrische sluitplaat.",
        "Houten deuren die een uitsparing nodig hebben voor beslag frezen wij zelf in, in eigen beheer. Stalen, aluminium en glazen deuren beoordelen wij tijdens de inventarisatie; "
        "daar hangt de oplossing af van het profiel en het bestaande slot. Meer over de soorten op <a href=\"/elektronische-sloten/\">elektronische sloten</a>."))

    aanpak = sectie("Hoe wij het aanpakken", stappen([
        ("Inventarisatie op locatie", f"Wij lopen alle deuren met u langs en leggen per deur vast: type, beslag, wie erdoor moet en wanneer. {'Zonder kosten' if INVENTARISATIE_GRATIS else 'Tegen een vaste prijs'}; wij reageren binnen {esc(REACTIE_AANVRAAG)} op uw aanvraag."),
        ("Advies met offerte", f"Eén voorstel met systeem, aantal deuren en prijs per deur, {esc(OFFERTE_BINNEN)}. Richtprijzen staan op de pagina <a href=\"/kosten/\">wat kost toegangscontrole</a>."),
        ("Installatie", "Eigen monteurs, mechanisch en elektronisch uit één hand. De planning en doorlooptijd spreken wij per project met u af."),
        ("Beheer en service", f"Wij zetten het systeem in bedrijf en leren u het beheer, of wij beheren het voor u. Daarna: <a href=\"/service-en-beheer/\">service en beheer</a>."),
    ]), wit=True)

    faq = [
        ("Wat is het verschil tussen toegangscontrole en een elektronisch slot?",
         "Een elektronisch slot is één deur die met een pas opengaat. Toegangscontrole is het systeem eromheen: de software waarin u vastlegt wie welke deuren mag openen en wanneer, en de rapportage daarover. Eén elektronisch slot kan het begin zijn van een systeem."),
        ("Hoeveel deuren heb ik minimaal nodig?",
         "Er is geen minimum. Veel bedrijven beginnen met de buitendeur en de ruimtes waar het om gaat: serverruimte, magazijn, medicijnkast, directiekamer. De rest van de deuren kan later, in hetzelfde systeem."),
        ("Werkt het ook als de stroom uitvalt?",
         "Elektronisch beslag en elektronische cilinders werken op batterijen en blijven bij stroomuitval gewoon werken. Een wandlezer met elektrische sluitplaat heeft voeding nodig; daar kiest u vooraf of de deur bij stroomuitval open of dicht valt, afhankelijk van de vluchtroute."),
        ("Kan ik rechten zelf beheren?",
         f"Ja. Na de installatie kunt u zelf passen uitgeven, blokkeren en tijdsloten instellen. Wilt u het liever uit handen geven, dan beheren wij het voor u."),
        ("Wat kost een toegangscontrolesysteem?",
         f"Dat hangt af van het aantal deuren, het deurtype en of de deur offline of online moet zijn. Een elektronisch slot kost geplaatst {prijs('slot')}, {BTW_TEKST}. Alle vanaf-prijzen staan op <a href=\"/kosten/\">wat kost toegangscontrole</a>."),
        ("Kunnen jullie een bestaand systeem van een ander merk uitbreiden?",
         f"Bestaande Salto-systemen onderhouden en breiden wij uit; zie <a href=\"/salto/\">Salto onderhoud</a>. Systemen van andere merken nemen wij ook over en breiden wij uit; koppelingen met intercom, alarm of tijdregistratie bekijken wij in overleg."),
    ]

    body = hero("Wat is een toegangscontrolesysteem en hoe pakken wij het aan", intro, foto) + wanneer + soorten + middelen + deuren + aanpak
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Toegangscontrole", PAD)],
            extra_ld=[service_ld(PAD, "Toegangscontrole", omschrijving)],
            llms="Wat een toegangscontrolesysteem is, wanneer het loont, offline/online/cloud vergeleken, identificatiemiddelen, bestaande deuren, onze aanpak in vier stappen.")
