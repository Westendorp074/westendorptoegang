"""/service-en-beheer/ — hoofdzoekwoord: onderhoud toegangscontrole. Bestaande klanten en vergelijkers."""
from build import *

PAD = "/service-en-beheer/"

def bouw():
    titel = "Onderhoud, storing en beheer van toegangscontrole"
    omschrijving = ("Storing, onderhoud, uitbreiding en beheer van toegangscontrole, ook bij een systeem van een andere installateur. Reactietijden en contracten.")
    intro = ("Toegangscontrole heeft weinig onderhoud nodig, maar als een deur niet opengaat wilt u snel iemand aan de lijn die het systeem kent. "
             "Wij verhelpen storingen, vervangen batterijen, breiden systemen uit en nemen het beheer van passen en rechten over als u dat wilt, "
             "voor onze eigen klanten en voor panden met een systeem van een andere installateur.")

    wat = sectie("Wat wij doen", '<div class="kolommen kolommen--2">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in [
        ("Storing", f"Deur gaat niet open of niet op slot, lezer reageert niet, software meldt een fout. Wij zijn er {esc(REACTIE_STORING)}."),
        ("Onderhoud", "Periodieke controle van beslag, cilinders, batterijen en software-updates, los of in een servicecontract."),
        ("Uitbreiding", "Extra deuren, een tweede vestiging, een wandlezer bij de nieuwe entree of de overstap van offline naar online deuren, binnen het bestaande systeem."),
        ("Beheer", "Passen uitgeven en blokkeren, rechten en tijdsloten bijhouden, rapportages maken. U doet het zelf na onze instructie, of wij doen het voor u."),
    ]) + "</div>")

    ander = sectie("Systeem van een andere installateur", p(
        f"Is uw systeem geplaatst door een bedrijf dat niet meer bestaat of niet meer reageert? Bestaande Salto-systemen onderhouden en breiden wij regelmatig uit; zie <a href=\"/salto/\">Salto onderhoud</a>. "
        "Ook systemen van andere merken nemen wij over en breiden wij uit.",
        "Wij beginnen dan met een inventarisatie: welke onderdelen, welke softwareversie, wie heeft de beheerdersrechten. Daarna weet u wat wij kunnen overnemen en wat vervangen moet worden."), wit=True)

    contract = sectie("Storingsdienst en servicecontract", tabel([
        ("Storingsdienst", esc(REACTIE_STORING)),
        ("Bereikbaar", esc(STORING_BUITEN_KANTOORTIJD)),
        ("Servicecontract per jaar", f"{esc(PRIJZEN['servicecontract'][0])} tot {esc(PRIJZEN['servicecontract'][1])}, excl. btw; {esc(PRIJZEN['servicecontract'][2])}"),
        ("Koppelingen met intercom, alarm, tijdregistratie of lift", "In overleg"),
    ], bijschrift="Storingsdienst en servicecontract") + p(PRIJS_DISCLAIMER + " De inhoud van een servicecontract stemmen wij per pand af."))

    faq = [
        ("Een deur gaat niet open, wat doe ik?", f"Probeer eerst een andere pas en de noodvoeding tegen de lezer; is de batterij leeg, dan opent de deur daarmee. Blijft het probleem, bel {tel()} met het deurnummer; wij zijn er {esc(REACTIE_STORING)}."),
        ("Hoe vaak moeten batterijen vervangen worden?", "Dat hangt af van het aantal passages per dag en de omgeving; het systeem meldt het weken van tevoren. Bij een servicecontract vervangen wij ze preventief tijdens de jaarlijkse controle."),
        ("Kunnen jullie het beheer volledig overnemen?", "Ja. In de praktijk doen veel klanten het dagelijkse beheer zelf en laten ze rapportages en wijzigingen in de structuur aan ons."),
        ("Heb ik een servicecontract nodig?", "Niet verplicht. Zonder contract helpen wij u ook, tegen uurtarief. Met contract heeft u vaste kosten en preventief onderhoud; de storingsdienst is er voor iedereen."),
        ("Nemen jullie ook een mechanisch sluitplan van een ander bedrijf over?", "Ja, als het systeem nog leverbaar is en u de sleutelkaart heeft. Anders adviseren wij een nieuw plan; zie <a href=\"/sluitplan/\">sluitplan</a>."),
    ]

    body = hero("Service en beheer van uw toegangscontrole", intro) + wat + ander + contract
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Service en beheer", PAD)],
            extra_ld=[service_ld(PAD, "Onderhoud en beheer toegangscontrole", omschrijving)], formulier_kop="Storing melden of onderhoud aanvragen",
            llms="Storing, onderhoud, uitbreiding en beheer van toegangscontrole, ook voor systemen van andere installateurs; contractvormen en reactietijden.")
