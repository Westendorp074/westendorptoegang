# Ontwerpplan westendorptoegang.nl

Toets: "zou ik dit voor elke installateur maken?" Nee. Wat het eigen maakt: het echte logo (sleutelgat met W) in het huisstijlblauw, een datasheet-tabel op elke product- en merkpagina, één groen element dat letterlijk het "toegang verleend"-groen van een lezer is, en verder foto's van beslag op echte deuren. Geen kaarten, geen schaduwen, geen iconen als versiering.

## Palet (uit het logopakket, LEESMIJ 20-09-2026)

| Token | Waarde | Gebruik |
|---|---|---|
| `--kop` | `#14232E` bijna-zwart | koppen: dezelfde toon als de donkere header, zodat boven en onder één geheel zijn |
| `--primair` | `#1B68C0` middenblauw (uit het logo) | links, 2px-lijn onder de header, stapcijfers, lijntjes boven kolomkoppen, adviseurblok |
| `--primair-donker` | `#02295B` | hover op links |
| `--inkt` | `#14232E` | lopende tekst |
| `--inkt-zacht` | `#4A5760` | onderschriften, metatekst (AA op `--vlak`) |
| `--donker` | `#1C1C1C` donkergrijs | alleen de header: de ondergrond van `logo-zwarte-achtergrond` (LEESMIJ: tot `#1E1E1E`; donkerblauw zou `logo-donkere-achtergrond` vragen, niet aangeleverd). Lars, 20-09-2026 |
| `--link-donker` | `#49BFFE` | links en accent op zwart, het lichtblauw uit het logo |
| `--vlak` | `#FFFFFF` | pagina-achtergrond van de inhoud |
| `--vlak-2` | `#F3F5F7` | afwisselende secties, tabellen, formulier |
| `--lijn` | `#C9CED0` | scheidingen, tabelranden |
| `--signaal` | `#1E8A4C` | alleen primaire CTA, formuliersucces, bedanktpagina |

Lichtblauw `#49BFFE` alleen op zwart (LEESMIJ: nooit op wit). Zwart `#111111` is alleen de header, precies waar het logo staat. Hero en footer zijn lichtgrijs `#F3F5F7`, de inhoud wit.

## Type

IBM Plex Sans, variabel (één woff2, 45 KB, `font-display: swap`), gewichten 400 / 500 / 600. Body 17 px mobiel, 18 px desktop, regelhoogte 1,55, tekst max 72 tekens. H1 36 / 52 px in 600 met −0,02 em spatiëring; H2 28 / 36 px; H3 20 / 22 px. Archivo (uit het logo) is alleen in het logo, als contour.

## Layout

Links uitgelijnd. Eén kolom mobiel; desktop twaalf kolommen van 1200 px, tekst in acht (rest witruimte of één foto). Secties gescheiden door 64 / 96 px witruimte, hooguit één 1 px lijn. Eén afrondingsstraal van 4 px, alleen knoppen en invoervelden. Tabellen als echte `<table>` met `--lijn`-randen en witte achtergrond. Foto's 3:2, onderschrift eronder in `--inkt-zacht`.

## Wireframe home

```
┌────────────────────────────────────────────────────────────────┐
│ [logo]                 Toegangscontrole Merken Kosten … [☎] [≡]│  header, 1px lijn --primair
├────────────────────────────────────────────────────────────────┤
│ H1 Toegangscontrole voor bedrijven in Oost-Nederland  │ foto   │  hero: 7 kol tekst, 5 kol foto 3:2
│ Twee zinnen.                                          │ 3:2    │
│ [Plan een gratis inventarisatie]  Bel 0xx-xxxxxxx     │ ondersch│
├────────────────────────────────────────────────────────────────┤
│ H2 Voor wie                                                     │  drie korte alinea's naast elkaar
│ Kantoren · Zorg · Onderwijs                                     │  (geen kaarten, geen lijn ertussen)
├─ 1px ──────────────────────────────────────────────────────────┤
│ H2 Wat wij plaatsen                                             │  witte sectie (--vlak-2)
│ EVVA Xesar → | Motorcilinder → | Sluitplan → | Salto onderhoud →│  vier alinea's met tekstlink
├────────────────────────────────────────────────────────────────┤
│ H2 Hoe het werkt                                                │
│ 1 Inventarisatie 2 Advies en offerte 3 Installatie 4 Beheer     │  <ol>, cijfers in --primair
├────────────────────────────────────────────────────────────────┤
│ H2 Waarom Westendorp   drie feiten uit INPUT.md, als tekst      │
├────────────────────────────────────────────────────────────────┤
│ H2 Werkgebied   tekst + plaatsenlijst per regio  │ statische    │
│                                                  │ kaart        │
├────────────────────────────────────────────────────────────────┤
│ H2 Veelgestelde vragen   <details> ×5                           │
├────────────────────────────────────────────────────────────────┤
│ H2 Plan een inventarisatie  │ adviseur: foto, naam, nummer,     │  witte sectie
│ [formulier, 8 kol]          │ reactietijd, drie feiten          │
├────────────────────────────────────────────────────────────────┤
│ footer: NAP, KvK, links, "onderdeel van Westendorp Slotenspec." │
└────────────────────────────────────────────────────────────────┘
```

## Wireframe merkpagina (`/evva-xesar/`)

```
│ kruimelpad                                                      │
│ H1 EVVA Xesar toegangscontrole               │ fabrikantbeeld   │
│ answer-first alinea (≤ 60 woorden)           │ (product)        │
│ [CTA]  Bel …                                 │                  │
├────────────────────────────────────────────────────────────────┤
│ H2 Voor wie is Xesar geschikt                                   │
│ H2 Welke Xesar-lijnen wij leveren            (uit INPUT §B4)    │
│ H2 Sterke en zwakke punten                   (twee lijsten)     │
│ H2 Specificaties                                                │
│ ┌ <table> ────────────────────────────────┐                     │
│ │ Identificatie | pas, tag, telefoon      │                     │
│ │ Beheer        | …                       │  datasheet-strook   │
│ │ Offline/online| …                       │                     │
│ │ …             | …                       │                     │
│ └─────────────────────────────────────────┘                     │
│ H2 Wat kost een Xesar-traject → /kosten/                        │
│ H2 Partnerstatus (uit INPUT §B4)                                │
│ H2 Veelgestelde vragen ×5                                       │
│ formulier + adviseur                                            │
```

## Principes

1. Elke pagina begint met het antwoord, niet met een aanloop.
2. Eén handeling per pagina, altijd dezelfde tekst, altijd groen.
3. Bewijs staat als tekst en foto, nooit als logo-rij of cijferstrook.
4. Geen beweging behalve open/dicht.
5. Wat niet in INPUT.md staat, staat niet op de site; placeholders blijven zichtbaar tot ze zijn ingevuld.
