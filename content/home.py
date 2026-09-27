"""Home — / . Hoofdzoekwoord: toegangscontrole bedrijf. Opbouw in de Salto-richting (Lars, 22-09-2026):
hero met illustratie, sectorrij, wat wij plaatsen, hoe het werkt, video, waarom Westendorp, duurzaamheid (alleen met feiten), werkgebied, FAQ."""
from build import *

def bouw():
    titel = "Toegangscontrole in Twente en Oost-Nederland | Westendorp"   # beide regio's (Lars, 27-09-2026)
    omschrijving = ("EVVA Xesar op bestaande deuren in Twente en Oost-Nederland. "
                    "Familiebedrijf sinds 1985. Gratis inventarisatie, storingsdienst dag en nacht.")

    # ---- hero: eigen foto als die er is, anders de isometrische scène ----
    # foto van Lars (23-09-2026); "Slotenspecialist" op de bus mag volgens check.py alleen op /over-ons/ genoemd worden, dus niet in de alt
    foto = beeld("westendorp-bedrijfsbus-lumen-enschede.jpg", "Bedrijfsbus van Westendorp geparkeerd voor het gebouw van Lumen in Enschede",
                 lazy=False, sizes="(min-width: 900px) 56vw, 100vw")   # zonder bijschrift (Lars, 23-09-2026)
    hero_html = hero("Toegangscontrole voor bedrijven in Twente en Oost-Nederland",
        f"Sleutels die kwijtraken, cilinders die telkens vervangen moeten worden en geen overzicht wie waar naar binnen kan? "
        f"Wij regelen de toegang tot uw pand op de deuren die er al zitten: elektronisch van EVVA en mechanisch, uit één hand. "
        f"Sterk in renovatie en bestaande panden, Twents familiebedrijf sinds {esc(MOEDER_SINDS)}, alleen toegangscontrole.",
        foto_html=foto, kicker="Elektronisch en mechanisch, uit één hand")   # illustratie weg; hier komt een echte foto (Lars, 22-09-2026)

    # ---- sectoren: horizontale rij met illustraties ----
    voor_wie = sectorrij(SECTOREN_LIJST,
        "Toegangscontrole per sector",
        "Elke sector heeft eigen deuren, gebruikers en regels. Kies de uwe en lees wat wij daar oplossen, van vijf deuren tot enkele honderden.")

    # ---- wat we plaatsen: vier producten uitgelicht, Xesar groot met video (Lars, 27-09-2026) ----
    magtec = beeld("magtec-cilinder-voorkant.jpg", "ABUS Magtec-profielcilinder, vooraanzicht", sizes="140px", klas="product__beeld", bron="ABUS")
    rest = [
        ("tedee", "Kleinschalige projecten", "Tedee Smart Lock",
         "Een slim slot voor een paar deuren: u opent met de app op uw telefoon en geeft anderen tijdelijk toegang, zonder sleutels bij te maken. Handig voor kleine kantoren, praktijken en verhuurde ruimtes.",
         "#aanvraag", "Vraag advies over Tedee", ""),
        ("magtec", "Mechanisch en duurzaam", "ABUS Magtec cilindersloten",
         "Mechanische cilinders met magneetcodering, SKG*** en in ons eigen sleutelprofiel. Loodvrij geproduceerd en met 46 procent minder CO₂-uitstoot dan een vergelijkbare cilinder.",
         "/duurzaamheid/#magtec", "Meer over ABUS Magtec", magtec),
        ("gu", "Grote projecten", "GU deurdrangers en deurautomaten",
         "Een elektronisch slot werkt pas als de deur ook goed dichtvalt. Wij leveren en stellen deurdrangers en deurautomaten van GU af, afgestemd op de deur en op de eisen voor brandwerende deuren.",
         "/elektronische-sloten/#deurdrangers", "Meer over deurdrangers", ""),
    ]
    wat = sectie("Wat wij plaatsen",
        '<div class="producten">'
        '<article class="product product--uitgelicht"><span class="product__label">Elektronisch · ons hoofdmerk</span><h3>EVVA Xesar</h3>'
        + p("Elektronische cilinders, beslag en wandlezers die u beheert in één overzichtelijke software. Openen met pas, druppel of telefoon, "
            "en een verloren pas blokkeert u zelf. Past op de deuren die er al zitten.")
        + youtube(XESAR_VIDEO, "Xesar in één blik", "Het elektronische sluitsysteem van EVVA, geplaatst door Westendorp")
        + '<p class="product__knop"><a class="meer" href="/evva-xesar/">Meer over EVVA Xesar</a></p></article>'
        '<div class="producten__rest">' + "".join(
            f'<article class="product product--{c}">{img}<div><span class="product__label">{esc(lab)}</span><h3>{esc(k)}</h3><p>{esc(t)}</p>'
            f'<p class="product__knop"><a class="meer" href="{u}">{esc(kn)}</a></p></div></article>' for c, lab, k, t, u, kn, img in rest)
        + "</div></div>"
        + p('Ook: <a href="/motorcilinder/">motorcilinders</a>, <a href="/sluitplan/">sluitplannen</a> en <a href="/salto/">onderhoud van bestaande Salto-systemen</a>.'),
        kicker="Oplossingen")

    # ---- hoe het werkt ----
    hoe = sectie("Toegangscontrole laten plaatsen in 4 stappen", stappen([
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
    bewijs = sectie("Waarom Westendorp", p(f"{esc(NAAM)} uit Enschede installeert EVVA Xesar, mechanische sluitsystemen en sluitplannen bij bedrijven en instellingen in Twente en Oost-Nederland, met eigen monteurs en een eigen werkplaats.") + '<div class="rooster"><div class="k7">' + lijst(feiten, klas="feiten") + '</div><div class="k5">'
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
    kies = ["sleutel-kwijt-sluitplan", "skg-sterren-en-1303", "wat-is-een-sluitplan"]              # op zoekvraag (advies SEO-specialist, 27-09-2026)
    titels = {slug: kop for slug, kop, *_ in ARTIKELEN}
    kennis = sectie("Uit de kennisbank",
        '<ul class="kennislinks">' + "".join(f'<li><a href="/kennisbank/{k}/">{esc(titels[k])}</a></li>' for k in kies) + "</ul>"
        + p('<a class="meer" href="/kennisbank/">Alle artikelen</a>'), kicker="Kennisbank")

    # ---- FAQ ----
    faq = [
        ("Wat kost toegangscontrole per deur?",
         f"Een elektronisch slot kost geplaatst {prijs('slot')} per deur, {BTW_TEKST}. De uiteindelijke prijs hangt af van het deurtype en of de deur online of offline moet werken. "
         f"De inventarisatie op locatie is gratis. Alle vanaf-prijzen staan op <a href=\"/kosten/\">wat kost toegangscontrole</a>."),
        ("Kan toegangscontrole op bestaande deuren?",
         "Ja. Op de meeste deuren komt elektronisch beslag of een elektronische cilinder in plaats van het huidige slot; de deur en het kozijn blijven. "
         "Houten deuren die een uitsparing nodig hebben, frezen wij in onze eigen werkplaats in. Meer op <a href=\"/elektronische-sloten/\">elektronische sloten</a>."),
        ("Wat gebeurt er als een medewerker zijn pas kwijtraakt?",
         "U blokkeert de pas in de software en geeft een nieuwe uit; deuren en cilinders blijven zitten. Bij een mechanisch sluitplan moet u na een verloren sleutel vaak cilinders vervangen. "
         "Zie ook <a href=\"/kennisbank/sleutel-kwijt-sluitplan/\">sleutel kwijt van het sluitplan</a>."),
        ("Kan ik mijn telefoon als sleutel gebruiken?",
         "Ja. Met EVVA AirKey staat de sleutel in een app op de telefoon, en die werkt samen met passen, druppels en gewone sleutels. "
         "U stuurt een sleutel op afstand toe en trekt hem net zo snel in. Meer over de mogelijkheden op <a href=\"/toegangscontrole/\">toegangscontrole</a>."),
        ("Kan ik de pasjes zelf beheren?",
         "Ja. Na de installatie geeft u zelf passen uit, blokkeert u ze en stelt u tijdsloten in. Wilt u het uit handen geven, dan beheren wij het systeem voor u; "
         "overstappen tussen die twee kan altijd. Zie <a href=\"/service-en-beheer/\">service en beheer</a>."),
        ("Werken jullie in Enschede, Hengelo en Zwolle?",
         f"Ja. Wij werken vanuit Enschede, {esc(WERKGEBIED_REGEL)}: heel Twente met onder meer Hengelo en Almelo, en ook Deventer, Zwolle, Zutphen, Doetinchem en Apeldoorn. "
         "Alle plaatsen staan op <a href=\"/werkgebied/\">werkgebied</a>."),
    ]

    # "Herkent u dit?": zes compacte tegels met icoon, het probleem als kop en in één regel wat er verandert (Lars, 23-09-2026)
    IC = {'sleutel': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>', 'oog': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>', 'regel': '<path d="M4 6h10M4 12h16M4 18h8"/><circle cx="17" cy="6" r="2"/><circle cx="15" cy="18" r="2"/>', 'klok': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', 'euro': '<path d="M17 6.5A7 7 0 1 0 17 17.5M4 10h9M4 14h9"/>', 'blad': '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14zM5 19l7-7"/>'}
    tegels = [("sleutel", "Sleutels raken kwijt", "Verloren pas blokkeren in de software; het slot blijft zitten."),
              ("oog", "Geen overzicht wie waar kan", "Per persoon ziet u welke deuren open mogen en wanneer."),
              ("regel", "Zelf beheren of uitbesteden", "U beheert zelf, of wij doen het voor u. Wisselen kan altijd."),
              ("klok", "Tijd kwijt aan sleutelbeheer", "Een pas of digitale sleutel op de telefoon staat in minuten klaar; bij vertrek trekt u hem in."),
              ("euro", "Steeds weer kosten", "Een pas vervangen in plaats van cilinders en sleutels."),
              ("blad", "Onnodig vervangen", "Het hang- en sluitwerk blijft zitten; alleen de pas wisselt.")]
    herken = sectie("Herkent u dit?",
        '<ul class="herken">' + "".join(f'<li><span class="herken__icoon"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{IC[i]}</svg></span>'
                                        f'<div><h3>{esc(k)}</h3><p>{esc(t)}</p></div></li>' for i, k, t in tegels) + "</ul>"
        + '<p class="acties acties--kaart" style="margin-top:24px"><a class="meer" href="/kosten/">Wat kost toegangscontrole</a><a class="meer" href="/service-en-beheer/">Service en beheer</a></p>', kicker="Waarom toegangscontrole")
    body = hero_html + herken + voor_wie + wat + hoe + video_blok + bewijs + duurzaam + kennis   # hybride en werkgebied staan op /toegangscontrole/ en /werkgebied/ (Lars, 27-09-2026)
    schrijf("/", titel, omschrijving, body, faq=faq, extra_ld=[video_ld("/", 'Korte video van EVVA over Xesar, het elektronische sluitsysteem met cilinders, beslag en wandlezers die u in één software beheert. Westendorp Toegangscontrole plaatst Xesar bij bedrijven en instellingen in Twente en Oost-Nederland.')],
            llms="Wie wij zijn, voor welke sectoren wij werken, wat wij plaatsen (EVVA Xesar, motorcilinder, sluitplan; onderhoud van Salto), werkwijze in vier stappen, werkgebied.")
