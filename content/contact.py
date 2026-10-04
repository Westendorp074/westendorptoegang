"""/contact/ — formulier, adviseur, NAP, openingstijden. Geen route: wij komen op locatie."""
from build import *

PAD = "/contact/"

def bouw():
    titel = "Contact en inventarisatie aanvragen"
    omschrijving = ("Plan een inventarisatie op locatie of stel uw vraag over toegangscontrole. Telefoon, e-mail, bereikbaarheid en het aanvraagformulier.")
    intro = (f"Een vraag, een offerte of gewoon even overleggen? Mail naar <a href=\"mailto:{esc(MAIL)}\">{esc(MAIL)}</a>, bel {tel()} of vul het formulier in — "
             f"wat u het makkelijkst vindt. {esc(ADVISEUR_NAMEN)} reageert binnen {esc(REACTIE_AANVRAAG)}. De inventarisatie doen wij bij u op locatie; u hoeft nergens heen.")
    knoppen = (f'<p class="acties"><a class="knop" href="mailto:{esc(MAIL)}">Stuur een e-mail</a>'
               f'<a class="knop knop--tweede knop--bel" href="tel:{esc(TEL_LINK)}">Bel {esc(TEL_TONEN)}</a></p>')
    profiel = f'<p><a href="{esc(GOOGLE_PROFIEL)}" rel="noopener">Bekijk ons Google Bedrijfsprofiel</a></p>' if not placeholder(GOOGLE_PROFIEL) else f"<p>{esc(GOOGLE_PROFIEL)}</p>"
    nap = sectie("Gegevens", '<div class="rooster"><div class="k4"><h3>Adres</h3>' + f'<address><p>{esc(NAAM)}<br>{esc(STRAAT)}<br>{esc(POSTCODE)} {esc(PLAATS)}</p></address>' +
        f'<p>{esc(RECHTSPERSOON)}, KvK {esc(KVK)}</p><p>Bezoek aan de vestiging {esc(BEZOEKADRES)}; de inventarisatie doen wij bij u.</p></div><div class="k4"><h3>Bereikbaar</h3><p>Kantoor {esc(KANTOORTIJD)}.</p><p>Storingen: {esc(STORING_BUITEN_KANTOORTIJD)}.</p></div>' +
        f'<div class="k4"><h3>Direct</h3><p><a href="tel:{esc(TEL_LINK)}">{esc(TEL_TONEN)}</a><br><a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a></p>{profiel}</div></div>')
    faq = [
        ("Kan ik ook gewoon een e-mail sturen?", f"Zeker. Mail uw vraag naar <a href=\"mailto:{esc(MAIL)}\">{esc(MAIL)}</a>, met of zonder bijlagen zoals foto's van deuren of een plattegrond; u krijgt binnen {esc(REACTIE_AANVRAAG)} antwoord van {esc(ADVISEUR_NAMEN)}."),
        ("Wat gebeurt er na mijn aanvraag?", f"U krijgt een bevestiging per e-mail. {esc(ADVISEUR_NAMEN)} belt u binnen {esc(REACTIE_AANVRAAG)} om de inventarisatie in te plannen."),
        ("Moet ik iets voorbereiden voor de inventarisatie?", "Handig zijn een plattegrond of deurenlijst, het huidige sluitplan of de sleutelkaart, en een idee van wie welke deuren moet kunnen openen. Heeft u dat niet, dan maken wij het samen ter plekke."),
        ("Kan ik een storing melden via dit formulier?", f"Voor storingen belt u liever direct: {tel()}. Het formulier is bedoeld voor nieuwe aanvragen en vragen zonder haast."),
    ]
    herofoto = beeld("westendorp-kantoor-hengelo.jpg",
                     "Kantoor van Westendorp in Hengelo waar medewerkers aanvragen en planning verwerken", lazy=False)
    body = hero("Contact", intro, foto_html=herofoto, cta=False, extra=knoppen) + nap
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Contact", PAD)], paginatype="ContactPage",
            formulier_kop="Stuur een bericht of plan een inventarisatie", formulier_standaard="bericht", formulier_boven_faq=True, formulier_keuze=True,
            llms="Contactgegevens, bereikbaarheid en het aanvraagformulier voor een inventarisatie op locatie.")
