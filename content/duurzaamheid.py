"""/duurzaamheid/ — ABUS Magtec: het sluitsysteem met een gemeten lagere CO₂-uitstoot. Feiten en cijfers van ABUS/ClimatePartner
(aangeleverd door Lars, 22-09-2026), altijd met bronvermelding. Fabrikantbeeld van ABUS."""
from build import *

PAD = "/duurzaamheid/"

def bouw():
    titel = "Duurzaam sluitsysteem: ABUS Magtec"
    omschrijving = ("ABUS Magtec: SKG***-cilinders in ons eigen profiel, loodvrij en met 46 procent minder CO₂-uitstoot "
                    "dan een gewone cilinder. Uit voorraad bij Westendorp.")
    intro = ("Een sluitsysteem gaat tientallen jaren mee, dus de keuze van de cilinder telt. Samen met onze partner ABUS kozen wij voor Magtec: "
             "een SKG***-cilinder in ons eigen sleutelprofiel die volgens een onafhankelijke berekening 46 procent minder broeikasgassen veroorzaakt "
             "dan een vergelijkbare conventionele cilinder, en die zonder lood wordt gemaakt.")
    foto_hero = beeld("magtec-cilinder-voorkant.jpg", "ABUS Magtec-profielcilinder, vooraanzicht", onderschrift="ABUS Magtec (beeld: ABUS)", lazy=False, bron="ABUS")

    cijfers = sectie("Wat de cijfers zeggen", '<div class="rooster"><div class="k7">' + p(
        "Magtec is ontworpen met de hele levenscyclus in beeld: grondstoffen, productie, levering aan de vakhandel en afvoer aan het einde van de levensduur. "
        "In vergelijking met een conventionele ABUS Vitess-profielcilinder veroorzaakt de functioneel vergelijkbare Magtec-cilinder <strong>46 procent minder broeikasgasemissies</strong>, "
        "berekend in CO₂-equivalenten op basis van een cradle-to-customer-plus-end-of-life-beoordeling. Het verschil zit vooral in grondstoffen en productie.",
        "Bij de productie van Magtec-cilinders wordt <strong>geen lood</strong> gebruikt.",
        "<small>Berekening van de uitstoot in CO₂-equivalenten door ClimatePartner Deutschland GmbH, november en december 2022, volgens de Greenhouse Gas Protocol Product Life Cycle Accounting and Reporting Standard; referentie-eenheid: 1 stuk. "
        "Meegenomen: winning en voorbewerking van grondstoffen en verpakking, productie, levering aan de fabriekspoort van de ABUS-vakhandel, en afvalverwerking van product en verpakking. De gebruiksfase is niet meegerekend. Bron: ABUS.</small>")
        + '</div><div class="k5">' + feiten_groen() + "</div></div>", kicker="Duurzaamheid")

    galerij = sectie("Van binnen en van buiten", '<div class="kolommen kolommen--3 galerij">'
        + "".join(f"<div>{beeld(b, alt, onderschrift=o, sizes='(min-width: 900px) 30vw, 100vw', bron='ABUS')}</div>" for b, alt, o in [
            ("magtec-cilinder-doorsnede.jpg", "Doorsnede van een ABUS Magtec-cilinder met stiften en magneet", "Doorsnede: stiften en magneetcodering (beeld: ABUS)"),
            ("magtec-sleutel.jpg", "ABUS Magtec-sleutel met ingebouwde magneet", "Magtec-sleutel met ingebouwde magneet (beeld: ABUS)"),
            ("magtec-cilinder-zijkant.jpg", "Zijaanzicht van een ABUS Magtec-cilinder", "Zijaanzicht (beeld: ABUS)")]) + "</div>", wit=True, kicker="ABUS Magtec")

    veilig = sectie("Duurzaam en veilig tegelijk", p(
        "De magneet in de Magtec-sleutel beschermt tegen ongeoorloofd kopiëren, ook met 3D-printers en slimme sleutelkopieermachines. "
        "Magtec haalt het hoogste niveau in elk van de categorieën sluitveiligheid, duurzaamheid, corrosiebestendigheid, brandwerendheid en sabotagebestendigheid van de Europese norm DIN EN 1303, "
        "en is SKG***-gecertificeerd door een onafhankelijk testinstituut.",
        f"Wij voeren Magtec in ons eigen sleutelprofiel ({esc(EIGEN_PROFIEL)}). Cilinders en sleutels liggen bij ons op voorraad en een sleutel wordt alleen bij ons bijgemaakt, op vertoon van de sleutelkaart. "
        "Zie ook <a href=\"/sluitplan/\">sluitplan</a>."))

    specs = sectie("Specificaties", tabel([
        ("Certificering", "SKG*** (hoogste niveau), DIN EN 1303 hoogste niveau op sluitveiligheid, duurzaamheid, corrosiebestendigheid, brandwerendheid en sabotagebestendigheid"),
        ("Kopieerbeveiliging", "Magneet in de sleutel; sleutels alleen bijmaken op sleutelkaart"),
        ("Broeikasgasemissies", "46 procent minder CO₂-equivalenten dan een ABUS Vitess-cilinder (ClimatePartner, 2022; gebruiksfase niet meegerekend)"),
        ("Materiaal", "Loodvrij geproduceerd"),
        ("Toepassing", "Mechanische sluitplannen en de mechanische deuren binnen een elektronisch systeem (techniekruimtes, kasten, hekken)"),
        ("Levering", "Eigen profiel bij Westendorp, uit voorraad"),
    ], bijschrift="Specificaties ABUS Magtec"), wit=True)

    faq = [
        ("Is een duurzame cilinder net zo veilig?", "Ja. Magtec is SKG***-gecertificeerd en haalt op alle vijf de categorieën van DIN EN 1303 het hoogste niveau. De lagere uitstoot komt uit grondstoffen en productie, niet uit een lichtere constructie."),
        ("Waar komt het cijfer van 46 procent vandaan?", "Van een levenscyclusberekening door ClimatePartner Deutschland GmbH in opdracht van ABUS (november en december 2022), volgens het GHG Protocol. Vergeleken is één Magtec-cilinder met één conventionele ABUS Vitess-cilinder; de gebruiksfase is niet meegerekend."),
        ("Kan Magtec in mijn bestaande sluitplan?", "Bij een nieuw sluitplan of een uitbreiding in ons eigen profiel: ja, uit voorraad. Een bestaand plan van een ander systeem kan gefaseerd worden overgezet; dat bekijken wij bij de inventarisatie."),
    ]

    body = hero("Duurzaam sluitsysteem: ABUS Magtec", intro, foto_hero, kicker="Duurzaamheid") + cijfers + galerij + veilig + specs
    schrijf(PAD, titel, omschrijving, body, faq=faq, kruimelpad=[("Home", "/"), ("Duurzaamheid", PAD)],
            extra_ld=[service_ld(PAD, "Duurzaam sluitsysteem ABUS Magtec", omschrijving, merk="ABUS")],
            llms="Duurzaamheid: ABUS Magtec-cilinders in eigen profiel, 46 procent minder CO₂-equivalenten dan een conventionele cilinder (ClimatePartner 2022), loodvrij, SKG***.")
