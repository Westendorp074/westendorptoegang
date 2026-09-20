# westendorptoegang.nl

Statische B2B-site van Westendorp Toegangscontrole. Regels: `CLAUDE.md`. Wat en waarom: `BRIEF.md`. Feiten: `INPUT.md`.

## Werken

    python build.py        bouwt naar dist/
    python check.py        strikt (livegang): faalt ook op [[INVULLEN]]-placeholders
    python check.py --wip  tijdens de bouw: placeholders rapporteren, niet falen
    python tools/iconen.py <map met logopakket-PNG's>   favicon, apple-touch-icon en OG-beeld

Alle feiten staan in het CONFIG-blok van `build.py`. Pagina's staan in `content/` (één module per pagina, `bouw()`),
opmaak in `static/css/tokens.css` en `styles.css`, gedrag in `static/js/site.js`. `dist/` staat niet in git; Vercel bouwt hem.

## Vercel

Project met framework "Other", build command `python build.py`, output directory `dist`. Domein: apex `westendorptoegang.nl`,
`www` stuurt door via `vercel.json`.
