# Beeldrichtlijn westendorptoegang.nl

Zet foto's in `static/img/bron/`. De build doet de rest: drie maten, WebP en AVIF, `width`/`height`, `srcset`, lazy loading, bijschrift, `ImageObject` in het schema, `og:image`, en de image-sitemap. `check.py` weigert beelden die de regels hieronder breken.

## Bestandsnaam (bepaalt hoe Google het beeld begrijpt)
- Kleine letters, woorden gescheiden door koppeltekens, geen spaties, geen hoofdletters, geen `IMG_1234`, `WhatsApp Image`, `foto1`.
- Zeg wat erop staat, in deze volgorde: **onderwerp-merk-deur-of-pand-plaats-jaar**.
  - `evva-xesar-beslag-houten-deur-kantoor-hengelo-2026.jpg`
  - `evva-emzy-motorcilinder-buitendeur-school-enschede-2026.jpg`
  - `infrezen-houten-deur-werkplaats-enschede-2026.jpg`
  - `wandlezer-entree-zorglocatie-almelo-2026.jpg`
- Het woord "toegangscontrole" hoeft er niet in; dat volgt uit de pagina.

## Alt-tekst (wat de build in `alt=""` zet; geef die per foto door)
- Beschrijf wat je ziet, alsof je het door de telefoon vertelt: 8 tot 15 woorden, met merk en plaats als die kloppen.
  - Goed: `EVVA Xesar-beslag op een houten binnendeur in een kantoorpand in Hengelo`
  - Fout: `foto`, `afbeelding van beslag`, `evva-xesar-beslag-hengelo` (bestandsnaam als alt), sleutelwoordenlijstjes.
- Geen "afbeelding van" of "foto van" vooraan; geen uitroeptekens; geen tekst die niet in beeld staat.

## Bijschrift (figcaption, staat zichtbaar onder de foto en in de image-sitemap)
- Het bewijs in één regel: wat, waar, wanneer. `Salto-beslag, kantoorpand Hengelo, 2026` of `Infrezen van een massief houten deur, werkplaats Enschede`.
- Bij fabrikantbeeld: `(beeld: EVVA)` of `(beeld: ABUS)` erachter; de build zet dan de fabrikant als maker in het schema.

## Het beeld zelf
- Eigen foto's, liggend, verhouding 3:2, minimaal 1600 px breed (2400 is beter), scherp, niet bewerkt. JPG of PNG; de build maakt WebP en AVIF.
- Geen tekst, logo's of pijlen in de foto; geen schermafbeeldingen; geen stockfoto's; geen AI-beeld.
- Geen herkenbare personen zonder toestemming; geen klantlogo's zonder toestemming (INPUT §C1).
- Eén onderwerp per foto: de deur met het beslag, de lezer naast de entree, de frees in de deur.

## Waar de foto's terechtkomen (bestandsnamen die de site verwacht)
| Bestand | Pagina | Wat erop moet staan |
|---|---|---|
| `westendorp-bedrijfsbus-lumen-enschede.jpg` | home, hero | geleverd 23-09-2026: bedrijfsbus voor het gebouw van Lumen, Enschede |
| `adviseur-lars.jpg`, `adviseur-nick.jpg` | over-ons, adviseurblok | portretten Lars en Nick (de v2-portretten en de onderhoudsfoto staan op verzoek van Lars in `backup/fotos/`, niet op de site) |
| `toegangscontrole-lezer.jpg` | /toegangscontrole/ | wandlezer naast een kantoordeur |
| `elektronisch-beslag.jpg` | /elektronische-sloten/ | elektronisch beslag op een houten binnendeur |
| `sluitplan-cilinders.jpg` | /sluitplan/ | cilinders en sleutels van een mechanisch sluitplan |
| `werkplaats-infrezen.jpg` | /over-ons/ | houten deur wordt ingefreesd in de werkplaats |
| `evva-xesar-product.jpg`, `evva-emzy-product.jpg` | merkpagina's | fabrikantbeeld EVVA, herkenbaar als product |
| `hero-video.mp4` + `hero-video-poster.jpg` | home, videoblok | 10–30 s, liggend, 1080p; poster is een stilstaand beeld eruit |

Je mag deze namen aanhouden (kort) óf de lange, beschrijvende naam kiezen; in dat laatste geval geef je de nieuwe naam door en pas ik hem aan in de content.
