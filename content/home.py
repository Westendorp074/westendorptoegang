"""Home — / . Hoofdzoekwoord: toegangscontrole bedrijf. Blokken in de volgorde van BRIEF.md §5.1."""
from build import *

def bouw():
    titel = "Toegangscontrole voor bedrijven in Oost-Nederland"
    omschrijving = ("Westendorp Toegangscontrole levert en installeert Salto, EVVA Xesar en motorcilinders voor "
                    "bedrijven en instellingen in Twente en Oost-Nederland.")

    # ---- hero ----
    foto = beeld("hero-beslag.jpg", "Elektronisch beslag op een kantoordeur, geplaatst door Westendorp Toegangscontrole",
                 onderschrift=INV("onderschrift hero-foto: wat, waar, jaar"), lazy=False)
    hero = f'''<section class="hero"><div class="wrap"><div class="rooster">
<div class="k7"><h1>Toegangscontrole voor bedrijven in Oost-Nederland</h1>
<p class="intro">Wij leveren en installeren elektronische toegangscontrole van Salto en EVVA, motorcilinders en sluitplannen voor kantoren, zorg en onderwijs, {esc(WERKGEBIED_REGEL)}. Deuren en sloten zijn ons vak sinds {esc(MOEDER_SINDS)}; het elektronische deel komt uit dezelfde hand.</p>
{acties()}</div>
<div class="k5">{foto}</div>
</div></div></section>'''

    # ---- voor wie ----
    sectoren = [
        ("Kantoren", "Sleutelbeheer dat niet meer bij te houden is, flexwerken of een verhuizing: één pas per medewerker, rechten zelf beheren."),
        ("Zorg", "Personeelswisselingen, medicijnruimtes en cliëntkamers: wie was wanneer waar, zonder sleutelbos."),
        ("Onderwijs", "Veel gebruikers, verhuur van ruimtes en verloren sleutels: zones en tijdsloten per groep, een kwijtgeraakte pas blokkeert u zelf."),
    ]
    voor_wie = sectie("Voor wie wij werken",
        '<div class="kolommen kolommen--3">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in sectoren) + "</div>"
        + p("Ook voor VvE's, verenigingen, kerken en bedrijfspanden met magazijn. Particulieren en autosleutels helpen wij via "
            f'<a href="{MOEDER_URL}" rel="noopener">{esc(MOEDER)}</a>.'))

    # ---- wat we plaatsen ----
    producten = [
        ("Salto", "/salto/", "Elektronisch beslag en cilinders die op bestaande deuren passen. Rechten beheert u in de software; een kwijtgeraakte pas blokkeert u zelf. " + f"Lijnen: {esc(MERKEN['salto']['lijnen'])}."),
        ("EVVA Xesar", "/evva-xesar/", "Elektronische cilinders, beslag en wandlezers van de Oostenrijkse slotenfabrikant EVVA. Sterk op deuren waar een mechanische cilinder al zit. " + f"Lijnen: {esc(MERKEN['xesar']['lijnen'])}."),
        ("Motorcilinder", "/motorcilinder/", "De EVVA EMZY draait de nachtschoot zelf: op afstand of via een lezer de deur echt op slot en weer open, ook op een buitendeur of vluchtdeur."),
        ("Sluitplan", "/sluitplan/", "Mechanisch, elektronisch of de overstap. Wie mag waar in, vastgelegd in één plan, met gecertificeerde cilinders waar de verzekeraar dat vraagt."),
    ]
    wat = sectie("Wat wij plaatsen",
        '<div class="kolommen kolommen--4">' + "".join(f'<div><h3>{k}</h3><p>{t}</p><p><a href="{u}">Meer over {k if k in ("Salto", "EVVA Xesar") else k.lower()}</a></p></div>' for k, u, t in producten) + "</div>",
        wit=True)

    # ---- hoe het werkt ----
    hoe = sectie("Hoe het werkt", stappen([
        ("Inventarisatie op locatie", f"Wij lopen alle deuren met u langs: deurtype, beslag, wie er doorheen moet en wanneer. {'Zonder kosten' if INVENTARISATIE_GRATIS else ''}, ingepland binnen {esc(INVENTARISATIE_BINNEN)}."),
        ("Advies met offerte", f"Eén voorstel met systeem, aantal deuren en prijs per deur, binnen {esc(OFFERTE_BINNEN)}. Geen verrassingen achteraf."),
        ("Installatie", f"Eigen monteurs, houten deuren frezen wij zelf in. Van akkoord tot installatie {esc(DOORLOOPTIJD)}."),
        ("Beheer en service", f"U beheert pasjes en rechten zelf of laat het ons doen ({esc(DIENSTEN_ONBEVESTIGD['beheer'])}). Bij een storing: {esc(REACTIE_STORING)}."),
    ]))

    # ---- bewijs: drie feiten uit INPUT.md ----
    feiten = [
        f"Slotenmaker in Enschede en Hengelo sinds {esc(MOEDER_SINDS)}; elektronische toegangscontrole sinds {esc(TOEGANG_SINDS)}.",
        f"{esc(AANTAL_DEUREN)} deuren geplaatst, met {esc(AANTAL_MONTEURS)} eigen monteurs.",
        f"Eigen werkplaats ({esc(WERKPLAATS)}): houten deuren frezen wij zelf in voor elektronisch beslag, zonder deurenfabrikant ertussen.",
    ]
    bewijs = sectie("Waarom Westendorp", '<div class="rooster"><div class="k8">' + lijst(feiten, klas="feiten") +
        p("Mechanisch en elektronisch uit één hand: de deur, het slot en het beslag kennen wij al dertig jaar, en daar komt de elektronica bovenop. "
          "Eén vaste adviseur van inventarisatie tot beheer.") + "</div></div>", lijn=True)

    # ---- werkgebied ----
    regios = {}
    for naam, regio, rijtijd, pad in WERKGEBIED:
        regios.setdefault(regio, []).append((naam, rijtijd, pad))
    def plaats_html(naam, rijtijd, pad):
        t = f"{rijtijd} min" if rijtijd is not None else INV(f"rijtijd {naam}")
        n = f'<a href="{pad}">{esc(naam)}</a>' if pad else esc(naam)
        return f"{n} <span class=\"zacht\">({t})</span>"
    plaatsen = '<ul class="plaatsen">' + "".join(
        f'<li><span class="regio">{esc(r)}</span><ul>' + "".join(f"<li>{plaats_html(*pl)}</li>" for pl in pls) + "</ul></li>"
        for r, pls in regios.items()) + "</ul>"
    kaart = beeld("kaart-werkgebied.png", "Kaart van het werkgebied: Twente, Salland, Achterhoek, Veluwe en Vechtdal", sizes="(min-width: 900px) 33vw, 100vw")
    werkgebied = sectie("Werkgebied", f'''<div class="rooster"><div class="k8">
{p(f"Wij werken vanuit {esc(PLAATS)}, {esc(WERKGEBIED_REGEL)}. Dat is heel Twente en het grootste deel van Salland, de Achterhoek, de Veluwe en het Vechtdal. Rijtijd vanaf onze vestiging:")}
{plaatsen}
{p('<a href="/werkgebied/">Alle plaatsen en rijtijden</a>')}</div><div class="k4">{kaart}</div></div>''', wit=True)

    # ---- FAQ ----
    faq = [
        ("Wat kost toegangscontrole per deur?",
         f"Dat hangt af van het deurtype, het systeem en of de deur online moet zijn. Elektronisch beslag van Salto kost geplaatst {esc(PRIJZEN['beslag_salto'][0])} tot {esc(PRIJZEN['beslag_salto'][1])} per deur, excl. btw. {PRIJS_DISCLAIMER} Alle bandbreedtes en drie rekenvoorbeelden staan op <a href=\"/kosten/\">wat kost toegangscontrole</a>."),
        ("Werkt elektronische toegangscontrole op onze bestaande deuren?",
         "Meestal wel. Op de meeste binnendeuren komt elektronisch beslag of een elektronische cilinder in plaats van het huidige slot; de deur blijft. Houten deuren die een uitsparing nodig hebben, frezen wij in onze eigen werkplaats in. Stalen, aluminium en glazen deuren bekijken wij tijdens de inventarisatie."),
        ("Wat gebeurt er als een medewerker zijn pas kwijtraakt?",
         "U blokkeert de pas in de software en geeft een nieuwe uit; de deuren en cilinders blijven zoals ze zijn. Bij een mechanisch sluitplan moet u bij een verloren hoofdsleutel vaak cilinders vervangen. Dat verschil is voor de meeste bedrijven de reden om over te stappen."),
        ("Hoe snel kunnen jullie beginnen?",
         f"Na uw aanvraag reageren wij binnen {esc(REACTIE_AANVRAAG)} en plannen wij de inventarisatie binnen {esc(INVENTARISATIE_BINNEN)}. Na akkoord op de offerte duurt het {esc(DOORLOOPTIJD)} tot de installatie."),
        ("Werken jullie ook buiten Twente?",
         f"Ja, {esc(WERKGEBIED_REGEL)}: Twente, Salland, de Achterhoek, de Veluwe en het Vechtdal. Zie het <a href=\"/werkgebied/\">werkgebied</a> met rijtijd per plaats."),
    ]

    body = hero + voor_wie + wat + hoe + bewijs + werkgebied
    schrijf("/", titel, omschrijving, body, faq=faq,
            llms="Wie wij zijn, wat wij plaatsen (Salto, EVVA Xesar, motorcilinder, sluitplan), werkwijze in vier stappen, werkgebied.")
