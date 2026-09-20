"""/contact/ — formulier, adviseur, NAP, openingstijden. Geen route: wij komen op locatie."""
from build import *

PAD = "/contact/"

def bouw():
    titel = "Contact en inventarisatie aanvragen"
    omschrijving = ("Plan een inventarisatie op locatie of stel uw vraag over toegangscontrole. Telefoon, e-mail, bereikbaarheid en het aanvraagformulier.")
    intro = (f"Bel {tel()}, mail naar <a href=\"mailto:{esc(MAIL)}\">{esc(MAIL)}</a> of vul het formulier in; {esc(ADVISEUR['naam'])} neemt binnen {esc(REACTIE_AANVRAAG)} contact met u op. "
             "De inventarisatie doen wij bij u op locatie; u hoeft nergens heen.")
    profiel = f'<p><a href="{esc(GOOGLE_PROFIEL)}" rel="noopener">Bekijk ons Google Bedrijfsprofiel</a></p>' if not placeholder(GOOGLE_PROFIEL) else f"<p>{esc(GOOGLE_PROFIEL)}</p>"
    nap = sectie("Gegevens", '<div class="rooster"><div class="k4"><h3>Adres</h3>' + f'<address><p>{esc(NAAM)}<br>{esc(STRAAT)}<br>{esc(POSTCODE)} {esc(PLAATS)}</p></address>' +
        f'<p>{esc(RECHTSPERSOON)}, KvK {esc(KVK)}</p><p>Bezoek aan de vestiging {esc(BEZOEKADRES)}; de inventarisatie doen wij bij u.</p></div><div class="k4"><h3>Bereikbaar</h3><p>Kantoor {esc(KANTOORTIJD)}.</p><p>Storingen: {esc(STORING_BUITEN_KANTOORTIJD)}.</p></div>' +
        f'<div class="k4"><h3>Direct</h3><p><a href="tel:{esc(TEL_LINK)}">{esc(TEL_TONEN)}</a><br><a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a></p>{profiel}</div></div>')
    faq = [
        ("Wat gebeurt er na mijn aanvraag?", f"U krijgt een bevestiging per e-mail. {esc(ADVISEUR['naam'])} belt u binnen {esc(REACTIE_AANVRAAG)} om de inventarisatie in te plannen, meestal binnen {esc(INVENTARISATIE_BINNEN)}."),
        ("Moet ik iets voorbereiden voor de inventarisatie?", "Handig zijn een plattegrond of deurenlijst, het huidige sluitplan of de sleutelkaart, en een idee van wie welke deuren moet kunnen openen. Heeft u dat niet, dan maken wij het samen ter plekke."),
        ("Kan ik een storing melden via dit formulier?", f"Voor storingen belt u liever direct: {tel()}. Het formulier is bedoeld voor nieuwe aanvragen en vragen zonder haast."),
    ]
    body = hero("Contact", intro, cta=False) + nap
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Contact", PAD)], paginatype="ContactPage",
            formulier_kop="Plan een inventarisatie op locatie",
            llms="Contactgegevens, bereikbaarheid en het aanvraagformulier voor een inventarisatie op locatie.")
