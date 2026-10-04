"""/over-ons/ — entiteitspagina. De enige pagina die het zusterbedrijf en de particuliere markt mag noemen (één zin)."""
from build import *

PAD = "/over-ons/"

def bouw():
    titel = "Over Westendorp Toegangscontrole"
    omschrijving = ("Westendorp Toegangscontrole uit Enschede installeert EVVA-toegangscontrole en sluitplannen bij bedrijven in Oost-Nederland. Feiten, team en werkplaats.")
    intro = (f"{esc(NAAM)} is de zakelijke toegangscontroletak van {esc(RECHTSPERSOON)} in {esc(PLAATS)}. Wij leveren en installeren elektronische toegangscontrole van EVVA, "
             f"mechanische sluitsystemen en sluitplannen bij bedrijven en instellingen in Oost-Nederland, met eigen monteurs en een eigen werkplaats voor het infrezen van deuren.")

    feiten = sectie("Feiten in het kort", '<div class="rooster"><div class="k8">' + lijst([
        f"Twents familiebedrijf sinds {esc(MOEDER_SINDS)}; elektronische toegangscontrole sinds {esc(TOEGANG_SINDS)}",
        f"Vestiging: {esc(STRAAT)}, {esc(POSTCODE)} {esc(PLAATS)}",
        f"Werkgebied: {esc(WERKGEBIED_REGEL)}",
        "Merken: EVVA (mechanisch en elektronisch), ASSA ABLOY (mechanisch en elektronisch), ABUS (mechanisch); onderhoud van bestaande Salto-systemen",
        f"Eigen sleutelprofiel: {esc(EIGEN_PROFIEL)}, cilinders op naam en op voorraad",
        "Eigenaren: Nick en Lars Westendorp, tweede generatie; eigen monteurs",
        f"Werkplaats en uitrijbasis in {esc(WERKPLAATS)}; Hengelo is de servicevestiging met kantoor",
        f"Partner en opleiding: {esc(CERTIFICATEN)}",
        f"Deurdrangers en deurautomaten: {esc(DEURDRANGERS)}",
        f"{esc(RECHTSPERSOON)}, KvK {esc(KVK)}",
    ], klas="feiten") + "</div></div>")

    # het ontstaansverhaal open op de pagina, naar het voorbeeld van de Slotenspecialist-site (Lars, 04-10-2026)
    duo = beeld("westendorp-winkel-enschede-sleutelbalie.jpg",
                "De balie van de Westendorp-winkel in Enschede, met de sleutelborden aan de wand en Nick Westendorp aan het werk",
                klas="pashoog")
    verhaal = sectie("Begonnen met sloten en sleutels, uitgegroeid tot toegangsspecialist", '<div class="rooster"><div class="k7">' + p(
        f"Westendorp begon in {esc(MOEDER_SINDS)} in Hengelo met sleutels, sloten en beslag — een ambacht, geleerd met vijl en hand, niet met een laptop. "
        "Inmiddels staat de tweede generatie aan het roer en rijden onze monteurs dagelijks door heel Oost-Nederland.",
        "Toen bedrijven vroegen om sloten die met een pas opengaan, bleek ons ambacht het verschil: de elektronica is het makkelijke deel, de deur is het lastige. "
        "Past het beslag, sluit de deur nog goed, blijft de brandwerende deur goedgekeurd? Wie veertig jaar deuren doet, weet dat voordat de eerste cilinder besteld is.",
        f"Daarom is {esc(NAAM)} ontstaan: de eigen zakelijke tak voor bedrijven en instellingen, met EVVA als hoofdmerk omdat die fabrikant mechanisch en elektronisch onder één dak maakt. "
        "Wij zijn officieel partner van EVVA, ASSA ABLOY en ABUS, en EVVA schakelt ons zelf in voor projecten in de regio. " + PKVW,
        f"Wat in al die jaren hetzelfde bleef: een sleutel die past, een slot dat werkt, een toegang die klopt — of het nu om één voordeur gaat of om een sluitplan voor honderd deuren. "
        f"{esc(NAAM)} is onderdeel van {esc(RECHTSPERSOON)}; onder dezelfde VOF valt <a href=\"{MOEDER_URL}\" rel=\"noopener\">{esc(MOEDER)}</a>, met winkels in {esc(VESTIGINGEN_MOEDER)} voor particulieren en autosleutels; die markt bedient deze site niet.")
        + f'</div><div class="k5">{duo}</div></div>', wit=True, kicker="Hoe wij begonnen zijn")

    # vier waarden, genummerd zoals de stappen (eigen taal, B2B)
    waarden = sectie("Vier dingen die niet onderhandelbaar zijn", '<ol class="stappen">' + "".join(
        f"<li><h3>{esc(k)}</h3><p>{esc(t)}</p></li>" for k, t in [
            ("Vakwerk boven alles", "Wij zijn toegangsspecialisten omdat we het vak liefhebben. Ook als een klus snel moet, frezen, stellen en testen wij zorgvuldig; de deur moet het over tien jaar nog doen."),
            ("Eerlijk over kosten", "U vindt bij ons vanaf-prijzen gewoon op de site en u hoort vooraf wat een project ongeveer kost. Verrassingen achteraf passen niet bij hoe wij werken."),
            ("Eén aanspreekpunt", "Wie de inventarisatie doet, kent de deuren die de monteur later aantreft. U belt met Nick of Lars, niet met een servicedesk."),
            ("Twents en dichtbij", "Wij zijn opgegroeid in Twente en werken voor organisaties in Oost-Nederland. Bij een storing zijn wij er binnen 4 tot 12 uur, dag en nacht, 365 dagen per jaar."),
        ]) + "</ol>", kicker="Wat wij belangrijk vinden")

    # cijfers in context, met de werkplaats ernaast
    werkbank = beeld("westendorp-werkplaats-sleutelspecialist-werkbank.jpg",
                     "Werkbank in de werkplaats van Westendorp, met ladekasten vol sleutel- en cilinderonderdelen en een monteur aan het werk",
                     klas="vol")
    cijfers = sectie("Wat ruim veertig jaar vakmanschap oplevert", '<div class="rooster"><div class="k7"><dl class="feitenpaneel feitenpaneel--vul">' + "".join(
        f"<div><dt>{esc(c)}</dt><dd>{esc(t)}</dd></div>" for c, t in [
            ("40+", "jaar ervaring met sloten en toegang in Twente"),
            ("2", "vestigingen: werkplaats Enschede en servicevestiging Hengelo"),
            ("300+", "zakelijke klanten in de regio, van gemeente tot winkelcentrum"),
            ("24/7", "storingsdienst: binnen 4 tot 12 uur ter plaatse, het hele jaar"),
        ]) + f'</dl></div><div class="k5">{werkbank}</div></div>', wit=True, kicker="Cijfers in context")

    beveiliging_tekst = p(
        f"Wij zijn {esc(CERTIFICATEN)}. Dat betekent dat wij de systemen van deze fabrikanten mogen leveren en installeren en hun opleidingen hebben gevolgd.",
        "Voor mechanische sluitplannen voeren wij cilinders met SKG-certificering waar de verzekeraar dat vraagt; ABUS Magtec haalt SKG*** en het hoogste niveau op DIN EN 1303. "
        "Elektronisch beslag en elektronische cilinders van EVVA plaatsen wij ook op brandwerende deuren, met behoud van de certificering van de deur.",
        "Uw gegevens en de logging van het toegangssysteem blijven van u; wij beheren alleen wat u ons vraagt te beheren. Zie ook <a href=\"/privacy/\">privacy</a>.")
    duurzaam_tekst = p(
        "Elektronische toegang scheelt vervangen: een verloren pas blokkeert u in de software, de cilinders blijven zitten en er worden geen extra sleutels gemaakt. Zo gaat er geen messing of staal verloren aan sleutelverlies.",
        "Voor de mechanische deuren voeren wij standaard ABUS Magtec: loodvrij geproduceerd en met 46 procent minder broeikasgasemissies dan een conventionele cilinder, berekend door ClimatePartner. "
        "Alles daarover staat op <a href=\"/duurzaamheid/\">duurzaamheid</a>.")
    uitklap = "".join(f'<details id="{a}"{" open" if i == 0 else ""}><summary>{esc(k)}</summary><div class="antwoord">{t}</div></details>' for i, (a, k, t) in enumerate([
        ("beveiliging", "Beveiliging en certificaten", beveiliging_tekst), ("duurzaamheid", "Duurzaamheid", duurzaam_tekst)]))
    meer = sectie("Meer over ons", f'<div class="rooster"><div class="k8"><div class="faq">{uitklap}</div></div></div>', kicker="Uitklappen")

    # teamkaarten in de stijl van de Slotenspecialist-site: grote foto bovenin, naam, functieregel, tekst met citaat (Lars, 04-10-2026)
    TEAMTEKST = {
        "Lars Westendorp": "Tweede generatie. Gespecialiseerd in elektronische toegang en beveiligingsoplossingen, en betrokken bij de dagelijkse aansturing van Westendorp. “Een slot dat klopt, geeft rust. Dat gun ik elke organisatie.”",
        "Nick Westendorp": "Tweede generatie. Verantwoordelijk voor zakelijke trajecten en sluitplan-ontwerp, en het aanspreekpunt voor onze grotere projecten. “Goede toegang is meestal onzichtbaar. Pas als het niet klopt, voel je het.”",
    }
    personen = "".join('<div class="teamkaart">'
        + (beeld(a["foto"], f"{a['naam']}, {a['functie']}", sizes="(min-width: 700px) 46vw, 100vw") if a["foto"] else "")
        + f'<h3>{esc(a["naam"])}</h3><p class="zacht">Eigenaar &amp; {esc(a["functie"].replace("eigenaar en ", ""))}</p>'
        + f'<p>{TEAMTEKST.get(a["naam"], "")}</p><p><a href="tel:{esc(a["tel_link"])}">{esc(a["tel_tonen"])}</a></p></div>' for a in ADVISEURS)
    bus = beeld("westendorp-servicebus-montageteam.jpg",
                "Monteur pakt gereedschap in een volledig ingerichte servicebus van Westendorp",
                klas="vol")
    breed = ('<div class="kolommen" style="margin-top:22px"><div><div class="rooster"><div class="k6"><h3>Onze monteurs en werkplaats</h3>'
        + p("Eigen, PKVW-gecertificeerde monteurs doen zowel het mechanische als het elektronische deel, met ervaring in oudere panden. "
            "Geen onderaannemers: wie de inventarisatie doet, kent de deuren die de monteur later aantreft.",
            f"Elektronisch beslag heeft in een houten deur vaak een uitsparing nodig die er niet is. Die frezen wij zelf in, in onze werkplaatsen in {esc(WERKPLAATS)}, "
            "zodat de deur niet vervangen hoeft te worden en er geen deurenfabrikant tussen zit. Eén partij voor deur, beslag en elektronica.")
        + f'</div><div class="k6">{bus}</div></div></div></div>')
    team = sectie("Twee vertrouwde gezichten, één vast team", '<div class="kolommen kolommen--2">' + personen + "</div>" + breed, kicker="Het team achter Westendorp")

    faq = [
        ("Zijn jullie een installateur of een leverancier?", "Beide. Wij leveren de onderdelen en installeren ze met eigen monteurs. Wij verkopen geen losse onderdelen zonder installatie."),
        ("Voor welke bedrijven werken jullie?", "Alle bedrijven en instellingen die de toegang tot hun pand willen regelen: kantoren, zorg, onderwijs, VvE's, verenigingen, recreatieparken, industrie en overheid. Zie de <a href=\"/\">homepage</a> voor de situaties die wij het meest tegenkomen."),
        ("Kan ik langskomen om een systeem te bekijken?", "Wij komen naar u toe. Bij de inventarisatie op locatie nemen wij demonstratiemateriaal mee, zodat u beslag en cilinder in handen heeft op de deur waar het om gaat."),
        ("Wat is de relatie met Westendorp Slotenspecialist?", f"Beide zijn onderdeel van {esc(RECHTSPERSOON)}. Westendorp Slotenspecialist bedient particulieren en autosleutels vanuit de winkels; {esc(NAAM)} bedient bedrijven en instellingen, op locatie."),
    ]

    herofoto = beeld("westendorp-bedrijfsbus-enschede.jpg",
                     "Bedrijfsbus van Westendorp geparkeerd in een straat in Enschede", lazy=False)
    body = hero(f"Over {esc(NAAM)}", intro, foto_html=herofoto, kicker=f"Familiebedrijf sinds {esc(MOEDER_SINDS)} · tweede generatie") + verhaal + waarden + team + cijfers + feiten + meer
    personen_ld = [{"@type": "Person", "@id": SITE + PAD + "#" + a["naam"].lower(), "name": a["naam"], "jobTitle": a["functie"], "telephone": a["tel_link"], "worksFor": {"@id": ORG_ID}} for a in ADVISEURS]
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Over ons", PAD)], paginatype="AboutPage", extra_ld=personen_ld,
            llms="Wie Westendorp Toegangscontrole is: ontstaan als slotenmakerij in 1985, tweede generatie, vier kernwaarden, cijfers, team met citaten, werkplaats, onderdeel van Westendorp Groep VOF.")
