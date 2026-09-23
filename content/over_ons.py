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
        f"Werkgebied: {esc(WERKGEBIED_REGEL)}, heel Oost-Nederland",
        "Merken: EVVA (mechanisch en elektronisch), ASSA ABLOY (mechanisch en elektronisch), ABUS (mechanisch); onderhoud van bestaande Salto-systemen",
        f"Eigen sleutelprofiel: {esc(EIGEN_PROFIEL)}, cilinders op naam en op voorraad",
        f"Adviseurs {esc(ADVISEUR_NAMEN.replace(' of ', ' en '))}, eigen monteurs",
        f"Werkplaats en uitrijbasis in {esc(WERKPLAATS)}; Hengelo is de servicevestiging met kantoor",
        f"Partner en opleiding: {esc(CERTIFICATEN)}",
        f"Deurdrangers en deurautomaten: {esc(DEURDRANGERS)}",
        f"{esc(RECHTSPERSOON)}, KvK {esc(KVK)}",
    ], klas="feiten") + "</div></div>")

    verhaal_tekst = p(
        f"Westendorp is een Twents familiebedrijf dat sinds {esc(MOEDER_SINDS)} deuren, sloten en beslag doet in Enschede en Hengelo. Toen bedrijven vroegen om sloten die met een pas opengaan, bleek dat de deur en het beslag "
        "het lastige deel zijn: past het beslag, sluit de deur nog goed, blijft de brandwerende deur goedgekeurd. De elektronica komt daar bovenop.",
        f"Daarom is {esc(NAAM)} ontstaan: een eigen tak voor bedrijven en instellingen, met EVVA als hoofdmerk omdat die fabrikant mechanisch en elektronisch onder één dak maakt. Wij zijn officieel partner van EVVA, ASSA ABLOY en ABUS, en EVVA schakelt ons in voor bepaalde projecten. "
        "Wat wij bieden is één adviseur van inventarisatie tot beheer, eigen monteurs binnen een uur rijden en een werkplaats waar wij houten deuren zelf infrezen. " + PKVW,
        f"{esc(NAAM)} is onderdeel van {esc(RECHTSPERSOON)}. Onder dezelfde VOF valt <a href=\"{MOEDER_URL}\" rel=\"noopener\">{esc(MOEDER)}</a>, met winkels in {esc(VESTIGINGEN_MOEDER)} voor particulieren en autosleutels; die markt bedient deze site niet.")
    beveiliging_tekst = p(
        f"Wij zijn {esc(CERTIFICATEN)}. Dat betekent dat wij de systemen van deze fabrikanten mogen leveren en installeren en hun opleidingen hebben gevolgd.",
        "Voor mechanische sluitplannen voeren wij cilinders met SKG-certificering waar de verzekeraar dat vraagt; ABUS Magtec haalt SKG*** en het hoogste niveau op DIN EN 1303. "
        "Elektronisch beslag en elektronische cilinders van EVVA plaatsen wij ook op brandwerende deuren, met behoud van de certificering van de deur.",
        "Uw gegevens en de logging van het toegangssysteem blijven van u; wij beheren alleen wat u ons vraagt te beheren. Zie ook <a href=\"/privacy/\">privacy</a>.")
    duurzaam_tekst = p(
        "Elektronische toegang scheelt vervangen: een verloren pas blokkeert u in de software, de cilinders blijven zitten en er worden geen extra sleutels gemaakt. Zo gaat er geen messing of staal verloren aan sleutelverlies.",
        "Voor de mechanische deuren voeren wij standaard ABUS Magtec: loodvrij geproduceerd en met 46 procent minder broeikasgasemissies dan een conventionele cilinder, berekend door ClimatePartner. "
        "Alles daarover staat op <a href=\"/duurzaamheid/\">duurzaamheid</a>.")
    uitklap = "".join(f'<details{" open" if i == 0 else ""}><summary>{esc(k)}</summary><div class="antwoord">{t}</div></details>' for i, (k, t) in enumerate([
        ("Wie zijn wij als bedrijf", verhaal_tekst), ("Beveiliging en certificaten", beveiliging_tekst), ("Duurzaamheid", duurzaam_tekst)]))
    verhaal = sectie("Meer over ons", f'<div class="rooster"><div class="k8"><div class="faq">{uitklap}</div></div></div>', wit=True, kicker="Uitklappen")

    personen = "".join('<div class="k4">' + (beeld(a["foto"], f"{a['naam']}, {a['functie']}", sizes="(min-width: 900px) 25vw, 50vw", klas="portret") if a["foto"] else "")
        + f'<h3>{esc(a["naam"])}</h3><p>{esc(a["functie"].capitalize())}. Uw contactpersoon van inventarisatie tot beheer.<br>'
        f'<a href="tel:{esc(a["tel_link"])}">{esc(a["tel_tonen"])}</a></p></div>' for a in ADVISEURS)
    team = sectie("Team", '<div class="rooster">' + personen + '<div class="k4"><h3>Monteurs</h3><p>Eigen, PKVW-gecertificeerde monteurs die zowel het mechanische als het elektronische deel doen, met ervaring in oudere panden. '
        "Geen onderaannemers: wie de inventarisatie doet, kent de deuren die de monteur later aantreft.</p></div></div>")

    werkplaats = beeld("werkplaats-infrezen.jpg", "Houten deur wordt ingefreesd voor elektronisch beslag in de werkplaats van Westendorp", onderschrift=INV("onderschrift werkplaatsfoto"))
    werk = sectie("Werkplaats en infrezen", '<div class="rooster"><div class="k7">' + p(
        f"Elektronisch beslag heeft in een houten deur vaak een uitsparing nodig die er niet is. Die frezen wij zelf in, in onze werkplaatsen in {esc(WERKPLAATS)}, zodat de deur niet vervangen hoeft te worden en er geen deurenfabrikant tussen zit. "
        "Voor de klant betekent dat één partij voor deur, beslag en elektronica.") + f'</div><div class="k5">{werkplaats}</div></div>', wit=True)

    faq = [
        ("Zijn jullie een installateur of een leverancier?", "Beide. Wij leveren de onderdelen en installeren ze met eigen monteurs. Wij verkopen geen losse onderdelen zonder installatie."),
        ("Voor welke bedrijven werken jullie?", "Alle bedrijven en instellingen die de toegang tot hun pand willen regelen: kantoren, zorg, onderwijs, VvE's, verenigingen, recreatieparken, industrie en overheid. Zie de <a href=\"/\">homepage</a> voor de situaties die wij het meest tegenkomen."),
        ("Kan ik langskomen om een systeem te bekijken?", "Wij komen naar u toe. Bij de inventarisatie op locatie nemen wij demonstratiemateriaal mee, zodat u beslag en cilinder in handen heeft op de deur waar het om gaat."),
        ("Wat is de relatie met Westendorp Slotenspecialist?", f"Beide zijn onderdeel van {esc(RECHTSPERSOON)}. Westendorp Slotenspecialist bedient particulieren en autosleutels vanuit de winkels; {esc(NAAM)} bedient bedrijven en instellingen, op locatie."),
    ]

    body = hero(f"Over {esc(NAAM)}", intro) + feiten + verhaal + team + werk
    personen_ld = [{"@type": "Person", "@id": SITE + PAD + "#" + a["naam"].lower(), "name": a["naam"], "jobTitle": a["functie"], "telephone": a["tel_link"], "worksFor": {"@id": ORG_ID}} for a in ADVISEURS]
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Over ons", PAD)], paginatype="AboutPage", extra_ld=personen_ld,
            llms="Wie Westendorp Toegangscontrole is: feiten in het kort, ontstaan, team, werkplaats, onderdeel van Westendorp Groep VOF.")
