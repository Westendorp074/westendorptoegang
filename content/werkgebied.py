"""/werkgebied/ — plaatsen per regio met rijtijd vanaf Enschede; plaatsen met eigen pagina linken (fase 2)."""
from build import *

PAD = "/werkgebied/"

def bouw():
    titel = "Werkgebied: Twente en Oost-Nederland"
    omschrijving = ("Westendorp Toegangscontrole werkt vanuit Enschede tot 60 minuten rijden: Twente, Salland, Achterhoek, Veluwe en Vechtdal. Rijtijd per plaats.")
    intro = (f"Wij werken vanuit {esc(PLAATS)}, {esc(WERKGEBIED_REGEL)}. Dat is heel Twente en het grootste deel van Salland, de Achterhoek, de Veluwe en het Vechtdal. "
             "Inventarisatie, installatie en service gebeuren altijd op locatie bij u; u hoeft nergens heen.")

    regios = {}
    for naam, regio, rijtijd, pad in WERKGEBIED:
        regios.setdefault(regio, []).append((naam, rijtijd, pad))
    rijen = []
    for regio, pls in regios.items():
        for naam, rijtijd, pad in pls:
            n = f'<a href="{pad}">{esc(naam)}</a>' if pad else esc(naam)
            rijen.append((n, esc(regio), f"{rijtijd} minuten" if rijtijd is not None else INV(f"rijtijd {naam} vanaf Enschede")))
    lijst_html = sectie("Plaatsen en rijtijd", '<div class="rooster"><div class="k7">' + tabel(rijen, kop=["Plaats", "Regio", "Rijtijd vanaf Enschede"], bijschrift="Werkgebied per plaats") +
        p("Staat uw plaats er niet bij? Binnen de cirkel van 60 minuten komen wij overal; daarbuiten in overleg.") + '</div><div class="k5">' + kaart_svg() + "</div></div>")

    hoe = sectie("Hoe wij op locatie werken", p(
        "De inventarisatie doen wij bij u in het pand: elke deur bekijken, meten en vastleggen. De installatie gebeurt met eigen monteurs vanuit Enschede; "
        "houten deuren die ingefreesd moeten worden, halen wij op of frezen wij ter plekke, afhankelijk van de deur. "
        f"Storingen: {esc(REACTIE_STORING)}, in het hele werkgebied."), wit=True)

    faq = [
        ("Komen jullie ook buiten de 60 minuten?", "In overleg, bijvoorbeeld voor een tweede vestiging van een bestaande klant. Voor een eerste project houden wij de cirkel aan, omdat wij bij storingen snel ter plaatse willen zijn."),
        ("Rekenen jullie voorrijkosten?", f"{INV('voorrijkosten: ja/nee en hoeveel')}"),
        ("Werken jullie ook in Duitsland?", "Nee. Ons werkgebied is Oost-Nederland."),
    ]

    body = hero("Werkgebied: waar wij toegangscontrole plaatsen", intro) + lijst_html + hoe
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Werkgebied", PAD)],
            llms="Werkgebied: tot 60 minuten rijden vanaf Enschede; plaatsen per regio met rijtijd; altijd op locatie.")
