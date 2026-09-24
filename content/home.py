"""Home — / . Hoofdzoekwoord: toegangscontrole bedrijf. Opbouw in de Salto-richting (Lars, 22-09-2026):
hero met illustratie, sectorrij, wat wij plaatsen, hoe het werkt, video, waarom Westendorp, duurzaamheid (alleen met feiten), werkgebied, FAQ."""
from build import *

def bouw():
    titel = "Toegangscontrole voor bedrijven in Oost-Nederland"
    omschrijving = ("Westendorp Toegangscontrole installeert EVVA Xesar, mechanische sluitsystemen en sluitplannen bij "
                    "bedrijven en instellingen in Twente en Oost-Nederland.")

    # ---- hero: eigen foto als die er is, anders de isometrische scène ----
    # foto van Lars (23-09-2026); "Slotenspecialist" op de bus mag volgens check.py alleen op /over-ons/ genoemd worden, dus niet in de alt
    foto = beeld("westendorp-bedrijfsbus-lumen-enschede.jpg", "Bedrijfsbus van Westendorp geparkeerd voor het gebouw van Lumen in Enschede",
                 lazy=False, sizes="(min-width: 900px) 56vw, 100vw")   # zonder bijschrift (Lars, 23-09-2026)
    hero_html = hero("Toegangscontrole voor bedrijven in Oost-Nederland",
        f"Sleutels die kwijtraken, cilinders die telkens vervangen moeten worden en geen overzicht wie waar naar binnen kan? "
        f"Wij regelen de toegang tot uw pand op de deuren die er al zitten: elektronisch van EVVA en mechanisch, uit één hand. "
        f"Sterk in renovatie en bestaande panden, Twents familiebedrijf sinds {esc(MOEDER_SINDS)}, alleen toegangscontrole.",
        foto_html=foto, kicker="Toegangscontrole, Enschede")   # illustratie weg; hier komt een echte foto (Lars, 22-09-2026)

    # ---- sectoren: horizontale rij met illustraties ----
    voor_wie = sectorrij(SECTOREN_LIJST,
        "Toegangscontrole per sector",
        "Elke sector heeft eigen deuren, gebruikers en regels. Kies de uwe en lees wat wij daar oplossen, van vijf deuren tot enkele honderden.")

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
        f"{PARTNER_TEKST[0].upper() + PARTNER_TEKST[1:]}: mechanisch en elektronisch van fabrikanten die wij kennen en die ons kennen.",
    ]
    bewijs = sectie("Waarom Westendorp", '<div class="rooster"><div class="k7">' + lijst(feiten, klas="feiten") + '</div><div class="k5">'
        + feitenpaneel() + "</div></div>", wit=True, kicker="Waarom wij")

    # ---- duurzaamheid: alleen met feiten van Lars (CONFIG DUURZAAM) ----
    # twee losse blokken (Lars, 23-09-2026): elektronisch (geen sloten vervangen) en mechanisch (ABUS Magtec)
    duurzaam = sectie("Duurzaam: minder vervangen, minder metaal",
        '<div class="kolommen kolommen--2 kolommen--groen">'
        f'<div>{label("Elektronisch")}<h3>{esc(DUURZAAM_ELEKTRONISCH[0])}</h3><p>Raakt een sleutel kwijt, dan blokkeert u bij elektronische toegang de pas in de software: het slot blijft zitten, er worden geen sleutels bijgemaakt en er gaat geen messing of staal verloren aan cilinders die alleen nodig zijn omdat een sleutel zoek is.</p>'
        '<p><a class="meer" href="/duurzaamheid/#elektronisch">Meer over elektronisch en duurzaam</a></p></div>'
        f'<div>{label("Mechanisch")}<h3>ABUS Magtec: minder uitstoot, geen lood</h3>' + lijst([f"<strong>{esc(k)}.</strong> {esc(t)}" for k, t in DUURZAAM])
        + '<p><a class="meer" href="/duurzaamheid/#magtec">Meer over ABUS Magtec</a></p></div></div>',
        kicker="Duurzaamheid", groen=True) if DUURZAAM else ""

    # ---- kennisbank: drie artikelen als opstap (Lars, 23-09-2026) ----
    from kennisbank import ARTIKELEN
    kennis = sectie("Uit de kennisbank",
        '<div class="kolommen kolommen--3">' + "".join(f'<div><h3><a href="/kennisbank/{slug}/">{esc(kop)}</a></h3><p>{esc(sam)}</p><p><a class="meer" href="/kennisbank/{slug}/">Lees het artikel</a></p></div>'
                                                      for slug, kop, sam, *_ in ARTIKELEN[:3]) + "</div>"
        + p('<a class="meer" href="/kennisbank/">Alle artikelen</a>'), kicker="Kennisbank", wit=True)

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

    # "Herkent u dit?": zes compacte tegels met icoon, het probleem als kop en in één regel wat er verandert (Lars, 23-09-2026)
    IC = {'sleutel': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>', 'oog': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>', 'regel': '<path d="M4 6h10M4 12h16M4 18h8"/><circle cx="17" cy="6" r="2"/><circle cx="15" cy="18" r="2"/>', 'klok': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', 'euro': '<path d="M17 6.5A7 7 0 1 0 17 17.5M4 10h9M4 14h9"/>', 'blad': '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14zM5 19l7-7"/>'}
    tegels = [("sleutel", "Sleutels raken kwijt", "Verloren pas blokkeren in de software; het slot blijft zitten."),
              ("oog", "Geen overzicht wie waar kan", "Per persoon ziet u welke deuren open mogen en wanneer."),
              ("regel", "Zelf beheren of uitbesteden", "U beheert zelf, of wij doen het voor u. Wisselen kan altijd."),
              ("klok", "Tijd kwijt aan sleutelbeheer", "Een nieuwe pas staat in minuten klaar; bij vertrek trekt u hem in."),
              ("euro", "Steeds weer kosten", "Een pas vervangen in plaats van cilinders en sleutels."),
              ("blad", "Onnodig vervangen", "Het hang- en sluitwerk blijft zitten; alleen de pas wisselt.")]
    herken = sectie("Herkent u dit?",
        '<ul class="herken">' + "".join(f'<li><span class="herken__icoon"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{IC[i]}</svg></span>'
                                        f'<div><h3>{esc(k)}</h3><p>{esc(t)}</p></div></li>' for i, k, t in tegels) + "</ul>"
        + '<p class="acties acties--kaart" style="margin-top:24px"><a class="meer" href="/kosten/">Wat kost toegangscontrole</a><a class="meer" href="/service-en-beheer/">Service en beheer</a></p>', kicker="Waarom toegangscontrole")
    body = hero_html + herken + voor_wie + wat + hoe + video_blok + bewijs + duurzaam + kennis + werkgebied
    schrijf("/", titel, omschrijving, body, faq=faq,
            llms="Wie wij zijn, voor welke sectoren wij werken, wat wij plaatsen (EVVA Xesar, motorcilinder, sluitplan; onderhoud van Salto), werkwijze in vier stappen, werkgebied.")
