"""Home — / . Hoofdzoekwoord: toegangscontrole bedrijf. Opbouw in de Salto-richting (Lars, 22-09-2026):
hero met illustratie, sectorrij, wat wij plaatsen, hoe het werkt, video, waarom Westendorp, duurzaamheid (alleen met feiten), werkgebied, FAQ."""
from build import *

def bouw():
    titel = "Toegangscontrole voor bedrijven in Oost-Nederland"
    omschrijving = ("Westendorp Toegangscontrole installeert EVVA Xesar, mechanische sluitsystemen en sluitplannen bij "
                    "bedrijven en instellingen in Twente en Oost-Nederland.")

    # ---- hero: eigen foto als die er is, anders de isometrische scène ----
    foto = beeld("hero-beslag.jpg", "Elektronisch beslag op een kantoordeur, geplaatst door Westendorp Toegangscontrole",
                 onderschrift=INV("onderschrift hero-foto: wat, waar, jaar"), lazy=False)
    hero_html = hero("Toegangscontrole voor bedrijven in Oost-Nederland",
        f"Wij leveren en installeren elektronische toegangscontrole van EVVA, mechanische sluitsystemen en sluitplannen voor bedrijven en instellingen in Twente en de rest van Oost-Nederland. "
        f"Twents familiebedrijf sinds {esc(MOEDER_SINDS)}: deuren, sloten en beslag zijn ons vak, het elektronische deel komt uit dezelfde hand.",
        foto_html=foto, illustratie=isometrie.hero_scene(), kicker="Toegangscontrole, Enschede")

    # ---- sectoren: horizontale rij met illustraties ----
    sectoren = [
        ("kantoren", "Kantoren", "Sleutelbeheer dat niet meer bij te houden is, flexwerken of een verhuizing: één pas per medewerker, rechten zelf beheren."),
        ("zorg", "Zorg", "Personeelswisselingen, medicijnruimtes en cliëntkamers: wie was wanneer waar, zonder sleutelbos."),
        ("onderwijs", "Onderwijs", "Veel gebruikers, verhuur van ruimtes en verloren sleutels: zones en tijdsloten per groep, een kwijtgeraakte pas blokkeert u zelf."),
        ("vve", "VvE en vastgoed", "Gemeenschappelijke entree, bergingen en sleutels die bij een verhuizing niet terugkomen: beheer op afstand, geen sleutelkopieën meer."),
        ("verenigingen", "Verenigingen en kerken", "Vrijwilligers, wisselende gebruikers, avonden en weekenden: tijdsloten en een pas die u intrekt als iemand stopt."),
        ("recreatie", "Recreatieparken", "Gasten die elke week wisselen, huisjes, sanitairgebouwen en een receptie die niet altijd bezet is: toegang per boeking, zonder sleuteloverdracht."),
        ("industrie", "Industrie en logistiek", "Ploegen, zonering en een verzekeraar of auditor die wil weten wie waar was: rapportage en uitbreiding per deur."),
        ("overheid", "Overheid en semi-overheid", "Gemeentelijke gebouwen, werven en buurthuizen: zones per afdeling en per gebruiker, met logging voor controle."),
    ]
    voor_wie = sectorrij([(s, k, t, "#aanvraag", "Plan een inventarisatie") for s, k, t in sectoren],
        "Toegangscontrole voor elk pand",
        "Voor alle bedrijven en instellingen die de toegang tot hun pand willen regelen zonder sleutelbos, van vijf deuren tot enkele honderden.")

    # ---- wat we plaatsen ----
    producten = [
        ("EVVA Xesar", "/evva-xesar/", "Elektronische cilinders, beslag en wandlezers van de Oostenrijkse slotenfabrikant EVVA, ons hoofdmerk. Past op bestaande deuren; rechten beheert u in de software en een kwijtgeraakte pas blokkeert u zelf. " + f"Lijnen: {esc(MERKEN['xesar']['lijnen'])}."),
        ("Motorcilinder", "/motorcilinder/", "De EVVA EMZY draait de nachtschoot zelf: op afstand of via een lezer de deur echt op slot en weer open, ook op een buitendeur of vluchtdeur."),
        ("Sluitplan", "/sluitplan/", "Mechanisch, elektronisch of de overstap. Wie mag waar in, vastgelegd in één plan, met gecertificeerde cilinders waar de verzekeraar dat vraagt."),
        ("Salto onderhoud", "/salto/", "Heeft u al een Salto-systeem? Nieuwe systemen plaatsen wij niet, maar onderhoud, storingen en uitbreiding van bestaande Salto-onderdelen doen wij regelmatig."),
    ]
    wat = sectie("Wat wij plaatsen",
        '<div class="kolommen kolommen--4">' + "".join(f'<div><h3>{k}</h3><p>{t}</p><p><a class="meer" href="{u}">Meer over {k if k[0].isupper() and k.split()[0] in ("EVVA", "Salto") else k.lower()}</a></p></div>' for k, u, t in producten) + "</div>",
        kicker="Oplossingen")

    # ---- hoe het werkt ----
    hoe = sectie("Hoe het werkt", stappen([
        ("Inventarisatie op locatie", f"Wij lopen alle deuren met u langs: deurtype, beslag, wie er doorheen moet en wanneer. {'Zonder kosten' if INVENTARISATIE_GRATIS else ''}, na uw aanvraag binnen {esc(REACTIE_AANVRAAG)} gepland."),
        ("Advies met offerte", f"Eén voorstel met systeem, aantal deuren en prijs per deur, {esc(OFFERTE_BINNEN)}. Geen verrassingen achteraf."),
        ("Installatie", "Eigen monteurs, houten deuren frezen wij zelf in. De planning spreken wij per project met u af."),
        ("Beheer en service", f"U beheert pasjes en rechten zelf, of wij doen het voor u. Bij een storing zijn wij er {esc(REACTIE_STORING)}."),
    ]), kicker="Werkwijze")

    # ---- video op klik (verschijnt zodra static/img/bron/hero-video.mp4 en hero-video-poster.jpg bestaan) ----
    film = video("hero-video.mp4", "hero-video-poster.jpg", "Monteur van Westendorp plaatst elektronisch beslag op een deur",
                 onderschrift=INV("onderschrift video: wat, waar, jaar"))
    video_blok = sectie("Zo werkt het bij ons", '<div class="rooster"><div class="k8">' + film + "</div></div>", kicker="Video") if film else ""

    # ---- bewijs: feiten uit INPUT.md ----
    feiten = [
        f"Twents familiebedrijf sinds {esc(MOEDER_SINDS)}; elektronische toegangscontrole sinds {esc(TOEGANG_SINDS)}.",
        f"Eigen werkplaats in {esc(WERKPLAATS)}: houten deuren frezen wij zelf in voor elektronisch beslag, zonder deurenfabrikant ertussen.",
        f"Storingsdienst {esc(REACTIE_STORING)}.",
        esc(PKVW),
        f"{PARTNER_TEKST.capitalize()}: mechanisch en elektronisch van fabrikanten die wij kennen en die ons kennen.",
    ]
    bewijs = sectie("Waarom Westendorp", '<div class="rooster"><div class="k7">' + lijst(feiten, klas="feiten") + '</div><div class="k5">'
        + feitenpaneel() + "</div></div>", wit=True, kicker="Waarom wij")

    # ---- duurzaamheid: alleen met feiten van Lars (CONFIG DUURZAAM) ----
    duurzaam = sectie("Duurzaam omgaan met deuren en sloten",
        '<div class="kolommen kolommen--3">' + "".join(f"<div><h3>{esc(k)}</h3><p>{esc(t)}</p></div>" for k, t in DUURZAAM) + "</div>",
        kicker="Duurzaamheid") if DUURZAAM else ""

    # ---- werkgebied ----
    regios = {}
    for naam, regio, rijtijd, pad in WERKGEBIED:
        regios.setdefault(regio, []).append((naam, rijtijd, pad))
    def plaats_html(naam, rijtijd, pad):
        return f'<a href="{pad}">{esc(naam)}</a>' if pad else esc(naam)
    plaatsen = '<ul class="plaatsen">' + "".join(
        f'<li><span class="regio">{esc(r)}</span><ul>' + "".join(f"<li>{plaats_html(*pl)}</li>" for pl in pls) + "</ul></li>"
        for r, pls in regios.items()) + "</ul>"
    werkgebied = sectie("Werkgebied", f'''<div class="rooster"><div class="k7">
{p(f"Wij werken vanuit {esc(PLAATS)}, {esc(WERKGEBIED_REGEL)}. Dat is heel Twente en het grootste deel van Salland, de Achterhoek, de Veluwe en het Vechtdal, onder meer:")}
{plaatsen}
{p(f'<a class="meer" href="/werkgebied/">Meer over het werkgebied</a>')}</div><div class="k5"><div class="paneel">{kaart_svg()}</div></div></div>''', kicker="Oost-Nederland")

    # ---- FAQ ----
    faq = [
        ("Wat kost toegangscontrole per deur?",
         f"Dat hangt af van het deurtype, het systeem en de beveiligingseisen. Een elektronisch slot kost geplaatst {prijs('slot')}, {BTW_TEKST}; een EVVA AirKey-startpakket {prijs('airkey_start', False)}. {PRIJS_DISCLAIMER} Meer op <a href=\"/kosten/\">wat kost toegangscontrole</a>."),
        ("Werkt elektronische toegangscontrole op onze bestaande deuren?",
         "Meestal wel. Op de meeste binnendeuren komt elektronisch beslag of een elektronische cilinder in plaats van het huidige slot; de deur blijft. Houten deuren die een uitsparing nodig hebben, frezen wij in onze eigen werkplaats in. Stalen, aluminium en glazen deuren bekijken wij tijdens de inventarisatie."),
        ("Wat gebeurt er als een medewerker zijn pas kwijtraakt?",
         "U blokkeert de pas in de software en geeft een nieuwe uit; de deuren en cilinders blijven zoals ze zijn. Bij een mechanisch sluitplan moet u bij een verloren hoofdsleutel vaak cilinders vervangen. Dat verschil is voor de meeste bedrijven de reden om over te stappen."),
        ("Hoe snel kunnen jullie beginnen?",
         f"Na uw aanvraag reageren wij binnen {esc(REACTIE_AANVRAAG)} en plannen wij de inventarisatie in. De offerte volgt {esc(OFFERTE_BINNEN)}; de installatiedatum spreken wij per project af."),
        ("Werken jullie ook buiten Twente?",
         f"Ja, {esc(WERKGEBIED_REGEL)}: Twente, Salland, de Achterhoek, de Veluwe en het Vechtdal. Zie het <a href=\"/werkgebied/\">werkgebied</a>."),
    ]

    body = hero_html + voor_wie + wat + hoe + video_blok + bewijs + duurzaam + werkgebied
    schrijf("/", titel, omschrijving, body, faq=faq,
            llms="Wie wij zijn, voor welke sectoren wij werken, wat wij plaatsen (EVVA Xesar, motorcilinder, sluitplan; onderhoud van Salto), werkwijze in vier stappen, werkgebied.")
