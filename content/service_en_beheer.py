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
        ("Storing", f"Deur gaat niet open of niet op slot, lezer reageert niet, software meldt een fout. Reactietijd: {esc(REACTIE_STORING)}. Buiten kantoortijd: {esc(STORING_BUITEN_KANTOORTIJD)}."),
        ("Onderhoud", f"Periodieke controle van beslag, cilinders, batterijen en software-updates. Onderhoud en servicecontracten: {esc(DIENSTEN_ONBEVESTIGD['onderhoud'])}."),
        ("Uitbreiding", "Extra deuren, een tweede vestiging, een wandlezer bij de nieuwe entree of de overstap van offline naar online deuren, binnen het bestaande systeem."),
        ("Beheer", f"Passen uitgeven en blokkeren, rechten en tijdsloten bijhouden, rapportages maken. {esc(DIENSTEN_ONBEVESTIGD['beheer'])}."),
    ]) + "</div>")

    ander = sectie("Systeem van een andere installateur", p(
        f"Is uw systeem geplaatst door een bedrijf dat niet meer bestaat of niet meer reageert? Bestaande Salto-systemen onderhouden en breiden wij regelmatig uit; zie <a href=\"/salto/\">Salto onderhoud</a>. "
        f"Voor andere merken: {esc(DIENSTEN_ONBEVESTIGD['overnemen'])}.",
        "Wij beginnen dan met een inventarisatie: welke onderdelen, welke softwareversie, wie heeft de beheerdersrechten. Daarna weet u wat wij kunnen overnemen en wat vervangen moet worden."), wit=True)

    contract = sectie("Contractvormen en reactietijden", tabel([
        ("Contractvormen", esc(CONTRACTVORMEN)),
        ("Reactietijd bij storing, met contract", esc(REACTIE_STORING)),
        ("Reactietijd bij storing, zonder contract", esc(REACTIE_STORING)),
        ("Storingen buiten kantoortijd", esc(STORING_BUITEN_KANTOORTIJD)),
        ("Servicecontract per jaar", f"{esc(PRIJZEN['servicecontract'][0])} tot {esc(PRIJZEN['servicecontract'][1])}, excl. btw; {esc(PRIJZEN['servicecontract'][2])}"),
        ("Garantie op montage en materiaal", esc(GARANTIE)),
    ], bijschrift="Contractvormen en reactietijden") + p(PRIJS_DISCLAIMER))

    faq = [
        ("Een deur gaat niet open, wat doe ik?", f"Probeer eerst een andere pas en de noodvoeding tegen de lezer; is de batterij leeg, dan opent de deur daarmee. Blijft het probleem, bel {tel()} met het deurnummer. Reactietijd: {esc(REACTIE_STORING)}."),
        ("Hoe vaak moeten batterijen vervangen worden?", "Dat hangt af van het aantal passages per dag en de omgeving; het systeem meldt het weken van tevoren. Bij een servicecontract vervangen wij ze preventief tijdens de jaarlijkse controle."),
        ("Kunnen jullie het beheer volledig overnemen?", f"{esc(DIENSTEN_ONBEVESTIGD['beheer'])}. In de praktijk doen veel klanten het dagelijkse beheer zelf en laten ze rapportages en wijzigingen in de structuur aan ons."),
        ("Heb ik een servicecontract nodig?", f"Niet verplicht. Zonder contract helpen wij u ook, tegen uurtarief en met de reactietijd zonder contract ({esc(REACTIE_STORING)}). Met contract heeft u vaste kosten, voorrang bij storingen en preventief onderhoud."),
        ("Nemen jullie ook een mechanisch sluitplan van een ander bedrijf over?", "Ja, als het systeem nog leverbaar is en u de sleutelkaart heeft. Anders adviseren wij een nieuw plan; zie <a href=\"/sluitplan/\">sluitplan</a>."),
    ]

    body = hero("Service en beheer van uw toegangscontrole", intro) + wat + ander + contract
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Service en beheer", PAD)],
            extra_ld=[service_ld(PAD, "Onderhoud en beheer toegangscontrole", omschrijving)], formulier_kop="Storing melden of onderhoud aanvragen",
            llms="Storing, onderhoud, uitbreiding en beheer van toegangscontrole, ook voor systemen van andere installateurs; contractvormen en reactietijden.")
