"""/bedankt/ — noindex; conversie-event (site.js); wat gebeurt er nu uit INPUT §E2."""
from build import *

PAD = "/bedankt/"

def bouw():
    titel = "Bedankt voor uw aanvraag"
    omschrijving = ("Uw aanvraag is ontvangen. U krijgt een bevestiging per e-mail en de adviseur belt u om de inventarisatie op locatie in te plannen.")
    body = f'''<section class="hero"><div class="wrap"><div class="rooster"><div class="k8">
<h1>Bedankt, uw aanvraag is ontvangen</h1>
<div class="bevestigd"><p class="intro">{esc(BEDANKT_TEKST)}</p></div>
<p>Heeft u intussen een vraag of haast? Bel {tel()} of mail <a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a>.</p>
<p>Verder lezen: <a href="/kosten/">wat kost toegangscontrole</a>, <a href="/evva-xesar/">EVVA Xesar</a> of <a href="/toegangscontrole/">hoe toegangscontrole werkt</a>.</p>
</div></div></div></section>'''
    schrijf(PAD, titel, omschrijving, body, kruimelpad=[("Home", "/"), ("Bedankt", PAD)], noindex=True, met_formulier=False)
