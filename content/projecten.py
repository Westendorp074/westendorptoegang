"""/projecten/ — hoofdzoekwoord: toegangscontrole projecten / referenties. Uitgevoerd werk per sector en plaats."""
from build import *

PAD = "/projecten/"

# Elk project is één regel; de kaarten en de sectorkoppeling volgen vanzelf.
# (sector-anker uit SECTOREN_LIJST of "", sectornaam, plaats, kop, tekst, foto in static/img/bron of "", alt-tekst)
# Alleen projecten met toestemming van de klant; geen aantallen of details die niet kloppen.
PROJECTEN = [
    ("zorg", "Zorg en welzijn", "Enschede", "Lumen",
     "Voor Lumen, het hart voor de wijk in Enschede, verzorgen wij de toegang en het hang- en sluitwerk.",
     "westendorp-bedrijfsbus-lumen-enschede.jpg",
     "Bedrijfsbus van Westendorp voor het gebouw van Lumen in Enschede"),
]

def bouw():
    titel = "Projecten: ons werk per sector"
    omschrijving = ("Projecten van Westendorp in Oost-Nederland: toegangscontrole, sluitplannen en hang- en sluitwerk "
                    "voor gemeenten, zorg, winkelcentra en bedrijven.")
    intro = ("Van gemeentehuizen tot wijkcentra en van winkelcentra tot werkplaatsen: hieronder ziet u een selectie van ons werk. "
             "Per project leest u waar het was, om welke sector het ging en wat wij daar hebben geplaatst. "
             "Deze pagina groeit; vraag gerust naar een referentie uit uw eigen sector.")

    kaarten = "".join(
        f'<div class="projectkaart">'
        + (beeld(foto, alt, sizes="(min-width: 700px) 46vw, 100vw") if foto else "")
        + f'<span class="product__label">{esc(sector)} · {esc(plaats)}</span><h3>{esc(kop)}</h3><p>{esc(tekst)}</p>'
        + (f'<p class="projectkaart__meer"><a class="meer" href="/toegangscontrole/#sector-{anker}">Meer voor {esc(sector.lower())}</a></p>' if anker else "")
        + "</div>"
        for anker, sector, plaats, kop, tekst, foto, alt in PROJECTEN)
    blok = sectie("Uitgelichte projecten", f'<div class="kolommen kolommen--2">{kaarten}</div>')

    # organisaties waarvoor wij werken (zelfde namen als de logobalk op de homepagina)
    namen = ["Gemeente Enschede", "Gemeente Hengelo", "Gemeente Almelo", "Politie", "Lumen", "Prismare", "Modern Care",
             "Bruna", "Winkelcentrum Hasselo", "Winkelcentrum Enschede Zuid", "Lastechniek Oost", "Oonk", "Rood Zwart"]
    wie = sectie("Zij gingen u voor", p(
        "Wij werken onder meer voor " + ", ".join(namen[:-1]) + " en " + namen[-1] + ". "
        "Wilt u weten wat wij in uw sector hebben gedaan? Bel of mail ons, dan sturen wij een passende referentie.") , wit=True)

    faq = [
        ("Kan ik een referentie krijgen uit mijn eigen sector?",
         "Ja. Vertel ons om wat voor pand het gaat, dan koppelen wij u aan een vergelijkbaar project en, als de klant dat goed vindt, aan een contactpersoon."),
        ("Plaatsen jullie ook buiten de regio van deze projecten?",
         "Wij werken in heel Oost-Nederland, vanuit Enschede. Alle plaatsen staan op <a href=\"/werkgebied/\">werkgebied</a>."),
        ("Komt mijn project ook op deze pagina?",
         "Alleen met uw toestemming. Veel klanten vinden dat prima; sommige panden, zoals serverruimtes of zorglocaties, laten wij bewust weg."),
    ]

    body = hero("Projecten: zo ziet ons werk eruit", intro) + blok + wie
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Projecten", PAD)],
            llms="Referentieprojecten per sector en plaats: wie wij al hielpen met toegangscontrole, sluitplannen en hang- en sluitwerk.")
