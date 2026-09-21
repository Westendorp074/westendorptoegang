"""/motorcilinder/ — hoofdzoekwoord: motorcilinder. Productpagina EVVA EMZY."""
from build import *

PAD = "/motorcilinder/"

def bouw():
    m = MERKEN["emzy"]
    titel = "Motorcilinder EVVA EMZY voor bedrijven"
    omschrijving = ("Een motorcilinder draait de nachtschoot zelf: op slot en open met pas, telefoon of op afstand. EVVA EMZY, specificaties, kosten en installatie.")
    intro = ("Een motorcilinder is een elektronische cilinder met een motor erin, die de nachtschoot van het slot zelf uitdraait en intrekt. "
             "De deur gaat dus echt op slot, niet alleen in de dag, en opent met een pas, een tag, de telefoon of op afstand. "
             "Wij plaatsen de EVVA EMZY, meestal op buitendeuren, vluchtdeuren en deuren met een meerpuntssluiting.")
    foto = beeld("evva-emzy-product.jpg", "EVVA EMZY motorcilinder", onderschrift="Productbeeld EVVA EMZY (fabrikant)")

    waarom = sectie("Waarom een motorcilinder en geen gewone elektronische cilinder", p(
        "Een gewone elektronische cilinder geeft de knop vrij; u moet de deur daarna zelf op slot draaien. In de praktijk gebeurt dat aan het eind van de dag niet altijd, "
        "en een meerpuntssluiting op een buitendeur is zwaar om te draaien. De motorcilinder doet dat zelf: na het sluiten van de deur, op een tijdstip, of op commando.",
        "Daarmee lost hij drie situaties op: de buitendeur die om zes uur automatisch op slot moet, de vluchtdeur die van buiten dicht en van binnen altijd open moet, "
        "en de deur die de receptie of de beheerder op afstand moet openen voor een leverancier."))

    voorwie = sectie("Waar wij de EMZY plaatsen", '<div class="kolommen kolommen--3">' + "".join(f"<div><h3>{k}</h3><p>{t}</p></div>" for k, t in [
        ("Buitendeuren", "Voordeur van kantoor, school of verenigingsgebouw: automatisch op slot buiten openingstijden, open met pas of tijdschema."),
        ("Vluchtdeuren", "Aan de binnenzijde altijd te openen met de kruk of panieksluiting; aan de buitenzijde alleen met pas. De motor volgt de vluchtrichting."),
        ("Deuren met meerpuntssluiting", "Kunststof en aluminium buitendeuren met drie of meer sluitpunten: de motor sluit alle punten, zonder kracht van de gebruiker."),
    ]) + "</div>", wit=True)

    specs = sectie("Specificaties EVVA EMZY", tabel([
        ("Identificatie", "Pas, tag, telefoon; op afstand via de beheersoftware of een koppeling"),
        ("Beheer", "In hetzelfde EVVA-systeem als Xesar-cilinders en -beslag"),
        ("Offline / online", "Beide; online voor bediening op afstand"),
        ("Voeding", "Batterij in de cilinder; netvoeding optioneel bij veel bewegingen"),
        ("Deurtypes", "Hout, staal, aluminium en kunststof; sloten met nachtschoot en meerpuntssluitingen"),
        ("Certificering", INV("EMZY-certificering die Westendorp levert, bijv. SKG-sterren of EN-klasse")),
        ("Uitbreidbaarheid", "Per deur, combineerbaar met Xesar en mechanisch sluitplan van EVVA"),
        ("Koppelingen", "Intercom, alarm, tijdregistratie of lift: in overleg"),
    ], bijschrift="Specificaties EVVA EMZY motorcilinder") + p(f"Partnerstatus: {esc(m['partner'])}."))

    kosten = sectie("Wat kost een motorcilinder", p(
        f"Een EVVA EMZY kost geplaatst {esc(PRIJZEN['emzy'][0])} tot {esc(PRIJZEN['emzy'][1])} per deur, excl. btw; daarin zit {esc(PRIJZEN['emzy'][2])}. "
        f"{PRIJS_DISCLAIMER} Meer op <a href=\"/kosten/\">wat kost toegangscontrole</a>."), wit=True)

    faq = [
        ("Wat gebeurt er bij een lege batterij of stroomuitval?", "De EMZY werkt op batterijen en meldt ruim van tevoren dat ze op raken. Is de batterij toch leeg, dan opent u met een noodvoeding tegen de cilinder of met de mechanische noodsleutel. Aan de binnenzijde blijft de deur altijd met de hand te openen."),
        ("Kan de deur op een vast tijdstip op slot?", "Ja. U stelt in de software een tijdschema in: bijvoorbeeld open van 08:00 tot 17:30 voor iedereen met pas, daarbuiten alleen voor beheerders. De motor sluit op het ingestelde tijdstip zelf af."),
        ("Is een motorcilinder toegestaan op een vluchtdeur?", "Ja, mits de vluchtrichting vrij blijft: aan de binnenzijde opent de deur altijd met de kruk of panieksluiting, ongeacht de stand van de motor. Wij stemmen dit af op de vluchtroute in uw pand."),
        ("Past een motorcilinder in mijn bestaande slot?", "Meestal wel. De EMZY vervangt de cilinder in het bestaande slot; de deur en de meerpuntssluiting blijven. Bij een afwijkende cilindermaat of een oud slot bekijken wij het tijdens de inventarisatie."),
        ("Hoe verhoudt de EMZY zich tot een elektrische sluitplaat?", "Een elektrische sluitplaat geeft de dagschoot vrij en heeft een kabel nodig; de deur is dan alleen in de dag. De motorcilinder sluit de nachtschoot en werkt op batterijen. Voor een buitendeur die echt op slot moet, is de motorcilinder de betere keuze."),
    ]

    body = hero("Motorcilinder: de deur die zichzelf op slot draait", intro, foto) + waarom + voorwie + specs + kosten
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Motorcilinder", PAD)],
            extra_ld=[service_ld(PAD, "Motorcilinder EVVA EMZY", omschrijving, merk="EVVA")],
            llms="Motorcilinder EVVA EMZY: wat het is, waarom een motorcilinder, waar wij hem plaatsen, specificatietabel, kosten.")
