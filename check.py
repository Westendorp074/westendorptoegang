#!/usr/bin/env python3
"""check.py — controles op dist/ vóór elke commit (CLAUDE.md §3 en §4, BRIEF.md §12).

  python check.py          strikt: faalt ook op [[INVULLEN]]-placeholders (dit is de livegang-check)
  python check.py --wip    tijdens de bouw: placeholders per pagina rapporteren, niet falen

Alle andere controles falen altijd hard. Nooit content herschrijven om een check te laten slagen (CLAUDE.md §7.6).
"""
import sys, re, json, pathlib, html
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
WIP = "--wip" in sys.argv
WHITELIST = ("https://www.googletagmanager.com/", "https://api.web3forms.com/", "https://bat.bing.com/")
VERBODEN = ["dé specialist", "totaaloplossing", "ontzorgen", "state-of-the-art", "innovatief", "toekomstbestendig",
            "naadloos", "uw partner in", "passie", "kwaliteit staat voorop", "wij zijn trots", "cutting-edge", "maatwerk", "24/7",
            "slotenmaker"]   # chat 20-09-2026: dat woord hoort bij de hoofdsite, niet bij deze
MAX_HTML = 150 * 1024
MAX_CSS, MAX_JS = 40 * 1024, 15 * 1024

fouten, waarschuwingen = [], []
def fout(pad, tekst): fouten.append(f"{pad}: {tekst}")
def waarschuw(pad, tekst): waarschuwingen.append(f"{pad}: {tekst}")

class Parser(HTMLParser):
    """Verzamelt wat de checks nodig hebben: tekst buiten script/style, tags met attributen, gedeelde blokken."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tekst, self.imgs, self.links, self.srcs, self.h1, self.canonical, self.title, self.desc, self.jsonld = [], [], [], [], 0, [], None, None, []
        self.paragrafen = []          # (tekst, in_gedeeld)
        self._stapel = []             # open tags
        self._gedeeld = 0             # diepte binnen footer/[data-gedeeld]/.consent
        self._in = None               # script/style/title/ld
        self._buf = []
        self._p = None
        self.faq_vragen = 0
        self.lang = None
        self.noindex = False
        self.bewijs = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag in ("footer",) or "data-gedeeld" in a or "consent" in (a.get("class") or "").split() or "kop" in (a.get("class") or "").split():
            self._stapel.append((tag, True)); self._gedeeld += 1
        else:
            self._stapel.append((tag, False))
        if "data-bewijs" in a: self.bewijs = True
        if tag == "script":
            self._in = "ld" if a.get("type") == "application/ld+json" else "script"
            self._buf = []
            if a.get("src"): self.srcs.append(a["src"])
        elif tag == "style": self._in = "style"
        elif tag == "title": self._in = "title"; self._buf = []
        elif tag == "meta":
            if a.get("name") == "description": self.desc = a.get("content", "")
            if a.get("name") == "robots" and "noindex" in a.get("content", ""): self.noindex = True
        elif tag == "link":
            if a.get("rel") == "canonical": self.canonical.append(a.get("href"))
            if a.get("rel") in ("stylesheet", "preload", "icon", "manifest", "apple-touch-icon") and a.get("href"): self.srcs.append(a["href"])
        elif tag == "img": self.imgs.append(a)
        elif tag == "source" and a.get("srcset"): self.srcs += [s.split()[0] for s in a["srcset"].split(",")]
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
        elif tag == "form" and a.get("action"): self.srcs.append(a["action"])
        elif tag == "h1": self.h1 += 1
        elif tag == "summary": self.faq_vragen += 1
        elif tag == "p": self._p = []
    def handle_endtag(self, tag):
        if tag in ("script", "style", "title"):
            if self._in == "ld": self.jsonld.append("".join(self._buf))
            if self._in == "title": self.title = "".join(self._buf).strip()
            self._in = None
        if tag == "p" and self._p is not None:
            self.paragrafen.append(("".join(self._p).strip(), self._gedeeld > 0)); self._p = None
        while self._stapel:
            t, g = self._stapel.pop()
            if g: self._gedeeld -= 1
            if t == tag: break
    def handle_data(self, data):
        if self._in in ("script", "style"): return
        if self._in in ("ld", "title"): self._buf.append(data); return
        self.tekst.append(data)
        if self._p is not None: self._p.append(data)

def intern_bestaat(href):
    href = href.split("#")[0].split("?")[0]
    if not href: return True
    if href.startswith("/"):
        doel = DIST / href.lstrip("/")
        if href.endswith("/"): return (doel / "index.html").exists()
        return doel.exists() or (doel / "index.html").exists()
    return True

def controleer_pagina(pad, tekst_html):
    rel = "/" + str(pad.relative_to(DIST).as_posix()).replace("index.html", "")
    P = Parser(); P.feed(tekst_html)
    platte = " ".join(P.tekst)
    platte = re.sub(r"\s+", " ", platte)
    # placeholders
    ph = sorted(set(re.findall(r"\[\[(?:INVULLEN|OPTIONEEL)[^\]]*\]\]", tekst_html)))
    if ph:
        (waarschuw if WIP else fout)(rel, f"{len(ph)} placeholder(s): " + "; ".join(ph[:6]) + (" …" if len(ph) > 6 else ""))
    # basis
    if P.lang != "nl": fout(rel, "html lang moet 'nl' zijn")
    if P.h1 != 1: fout(rel, f"{P.h1} h1-koppen, moet er precies één zijn")
    if len(P.canonical) != 1: fout(rel, "geen of meer dan één canonical")
    if not P.title: fout(rel, "geen <title>")
    elif len(P.title) > 60: fout(rel, f"title {len(P.title)} tekens (> 60): {P.title}")
    if not P.desc: fout(rel, "geen meta description")
    elif not 120 <= len(P.desc) <= 155: fout(rel, f"meta description {len(P.desc)} tekens (moet 120–155)")
    if len(tekst_html.encode("utf-8")) > MAX_HTML: fout(rel, f"HTML {len(tekst_html)//1024} KB (> 150 KB)")
    # beeld
    for a in P.imgs:
        if "alt" not in a: fout(rel, f"img zonder alt: {a.get('src')}")
        if not a.get("width") or not a.get("height"): fout(rel, f"img zonder width/height: {a.get('src')}")
    # links en externe requests
    for h in P.links:
        if not intern_bestaat(h): fout(rel, f"kapotte interne link: {h}")
    for s in P.srcs:
        if s.startswith("http") and not any(s.startswith(w) for w in WHITELIST): fout(rel, f"externe request buiten whitelist: {s}")
        if not s.startswith("http") and not intern_bestaat(s): fout(rel, f"ontbrekend bestand: {s}")
    # JSON-LD
    if not P.jsonld: fout(rel, "geen JSON-LD")
    for blok in P.jsonld:
        try:
            data = json.loads(blok)
        except json.JSONDecodeError as e:
            fout(rel, f"ongeldige JSON-LD: {e}"); continue
        graph = data.get("@graph", [])
        typen = [g.get("@type") for g in graph]
        if "aggregateRating" in blok or '"Review"' in blok: fout(rel, "aggregateRating of Review in schema is verboden")
        if rel != "/404.html":
            for t in ("LocalBusiness", "WebSite", "BreadcrumbList"):
                if t not in typen: fout(rel, f"schema mist {t}")
            if not any(t in ("WebPage", "AboutPage", "ContactPage") for t in typen): fout(rel, "schema mist WebPage")
            faq = [g for g in graph if g.get("@type") == "FAQPage"]
            if faq and not 3 <= len(faq[0].get("mainEntity", [])) <= 6: fout(rel, f"FAQPage met {len(faq[0]['mainEntity'])} vragen (moet 3–6)")
    # copy
    laag = platte.lower()
    for w in VERBODEN:
        if w in laag: fout(rel, f"verboden woord: '{w}'")
    if "!" in platte: fout(rel, "uitroepteken in tekst")
    for m in re.finditer(r"gratis", laag):
        omgeving = laag[max(0, m.start() - 80): m.end() + 80]
        if "inventarisatie" not in omgeving: fout(rel, "'gratis' buiten de context van de inventarisatie")
    # noindex alleen op bedankt
    if P.noindex and rel not in ("/bedankt/", "/404.html"): fout(rel, "noindex op een pagina die geïndexeerd moet worden")
    if rel == "/bedankt/" and not P.noindex: fout(rel, "bedankt moet noindex zijn")
    # interne links naar dienst en contact
    if rel not in ("/bedankt/", "/404.html", "/privacy/"):
        if not any(h.startswith("/contact/") or h == "#aanvraag" for h in P.links): fout(rel, "geen link naar contact of het formulier")
        if not any(re.match(r"/(toegangscontrole|elektronische-sloten|salto|evva-xesar|motorcilinder|sluitplan|service-en-beheer|kosten)/", h) for h in P.links): fout(rel, "geen link naar een dienstpagina")
    # stadspagina: bewijsblok verplicht
    if re.match(r"/toegangscontrole-[a-z-]+/$", rel) and not P.bewijs: fout(rel, "stadspagina zonder bewijsblok (data-bewijs)")
    return rel, P, platte

def main():
    if not DIST.exists():
        print("dist/ ontbreekt; draai eerst python build.py"); sys.exit(1)
    paginas = sorted(DIST.rglob("*.html"))
    resultaten = {}
    for pad in paginas:
        rel, P, platte = controleer_pagina(pad, pad.read_text(encoding="utf-8"))
        resultaten[rel] = (P, platte)
    # dubbele title / description
    for veld, idx in (("title", 0), ("description", 1)):
        gezien = {}
        for rel, (P, _) in resultaten.items():
            v = (P.title, P.desc)[idx]
            if v in gezien: fout(rel, f"dubbele {veld} met {gezien[v]}")
            gezien[v] = rel
    # inkomende links
    inkomend = {rel: 0 for rel in resultaten}
    for rel, (P, _) in resultaten.items():
        for h in P.links:
            h = h.split("#")[0]
            if h in inkomend and h != rel: inkomend[h] += 1
    for rel, n in inkomend.items():
        if n == 0 and rel not in ("/404.html", "/bedankt/"): fout(rel, "geen inkomende interne links")
    # boilerplate: dezelfde alinea (≥ 80 tekens) op meer dan één pagina, buiten footer/formulier/adviseur
    alineas = {}
    for rel, (P, _) in resultaten.items():
        for t, gedeeld in P.paragrafen:
            if gedeeld or len(t) < 80: continue
            alineas.setdefault(t, set()).add(rel)
    for t, rels in alineas.items():
        if len(rels) > 1: fout(", ".join(sorted(rels)), f"zelfde alinea op meer dan één pagina: '{t[:60]}…'")
    # stadspagina's: minstens 60% inhoudelijk verschil (woord-shingles van 5)
    steden = {rel: platte for rel, (P, platte) in resultaten.items() if re.match(r"/toegangscontrole-[a-z-]+/$", rel)}
    def shingles(t):
        w = re.findall(r"\w+", t.lower()); return {tuple(w[i:i + 5]) for i in range(len(w) - 4)}
    items = list(steden.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = shingles(items[i][1]), shingles(items[j][1])
            if a and b:
                gelijk = len(a & b) / min(len(a), len(b))
                if gelijk > 0.40: fout(items[i][0], f"lijkt voor {gelijk:.0%} op {items[j][0]} (max 40%)")
    # assets
    css = list((DIST / "static" / "css").glob("*.css")); js = list((DIST / "static" / "js").glob("*.js"))
    for f in css:
        if f.stat().st_size > MAX_CSS: fout(f.name, f"CSS {f.stat().st_size//1024} KB (> 40 KB)")
    for f in js:
        if f.stat().st_size > MAX_JS: fout(f.name, f"JS {f.stat().st_size//1024} KB (> 15 KB)")
    woff = list((DIST / "static" / "font").glob("*.woff2"))
    if len(woff) > 2: fout("static/font", f"{len(woff)} woff2-bestanden (max 2)")
    for css_f in css:
        inhoud = css_f.read_text(encoding="utf-8")
        for url in re.findall(r"url\(([^)]+)\)", inhoud):
            url = url.strip("\"'")
            if url.startswith("http"): fout(css_f.name, f"externe request in CSS: {url}")
            elif url.startswith("/") and not (DIST / url.lstrip("/")).exists(): fout(css_f.name, f"ontbrekend bestand in CSS: {url}")
    # sitemap, robots, llms
    sm = DIST / "sitemap.xml"
    if not sm.exists(): fout("sitemap.xml", "ontbreekt")
    else:
        locs = re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))
        for loc in locs:
            pad = re.sub(r"^https?://[^/]+", "", loc)
            if pad == "/bedankt/": fout("sitemap.xml", "bedankt hoort niet in de sitemap")
            if not intern_bestaat(pad): fout("sitemap.xml", f"URL zonder pagina: {pad}")
            if pad in resultaten and resultaten[pad][0].noindex: fout("sitemap.xml", f"noindex-pagina in sitemap: {pad}")
        for rel, (P, _) in resultaten.items():
            if not P.noindex and rel != "/404.html" and rel not in [re.sub(r"^https?://[^/]+", "", l) for l in locs]: fout("sitemap.xml", f"indexeerbare pagina ontbreekt: {rel}")
    for naam in ("robots.txt", "llms.txt", "404.html", "manifest.webmanifest"):
        if not (DIST / naam).exists(): fout(naam, "ontbreekt")
    llms = (DIST / "llms.txt")
    if llms.exists() and "[[" in llms.read_text(encoding="utf-8"):
        (waarschuw if WIP else fout)("llms.txt", "bevat placeholders")

    print(f"Gecontroleerd: {len(paginas)} pagina's")
    for w in waarschuwingen: print("  WIP  " + w)
    for f in fouten: print("  FOUT " + f)
    if fouten:
        print(f"\n{len(fouten)} fout(en)."); sys.exit(1)
    print("Groen." + (f" ({len(waarschuwingen)} pagina's met placeholders, nog niet live)" if waarschuwingen else ""))

if __name__ == "__main__":
    main()
