"""/privacy/ — verwerking formulier, Consent Mode, Web3Forms als verwerker, contactgegevens, KvK."""
from build import *

PAD = "/privacy/"

def bouw():
    titel = "Privacyverklaring"
    omschrijving = ("Hoe Westendorp Toegangscontrole omgaat met gegevens uit het aanvraagformulier, welke cookies de site pas na toestemming gebruikt, en uw rechten.")
    meting = (f"<p>Na uw toestemming gebruiken wij Google Analytics en Google Ads om te zien hoe de site wordt gebruikt en of onze advertenties werken (Google-tag {esc(GOOGLE_TAG_ID)}). "
              "Zonder toestemming worden er geen meetcookies geplaatst en gaat er niets naar Google; dat is zo ingesteld met Consent Mode v2, standaard op geweigerd. "
              "Uw keuze kunt u onderaan elke pagina wijzigen via Cookie-instellingen.</p>") if TAG_ACTIEF else \
             "<p>Op dit moment meet deze site niets: er worden geen analytics- of advertentiecookies geplaatst en er gaat geen bezoekersinformatie naar Google. Zodra dat verandert, vragen wij eerst uw toestemming en passen wij deze verklaring aan.</p>"
    body = f'''<section class="hero"><div class="wrap"><div class="rooster"><div class="k8"><h1>Privacyverklaring</h1>
<p class="intro">{esc(NAAM)} ({esc(RECHTSPERSOON)}, KvK {esc(KVK)}) verwerkt alleen de gegevens die u zelf invult in het aanvraagformulier, en gebruikt die uitsluitend om contact met u op te nemen over uw aanvraag. Meetcookies plaatsen wij pas na uw toestemming.</p>
<p class="laatst">Laatst bijgewerkt: {esc(datum_nl(VANDAAG))}</p></div></div></div></section>
<section><div class="wrap"><div class="rooster"><div class="k8">
<h2>Aanvraagformulier</h2>
<p>In het formulier vult u naam, bedrijf, e-mailadres, telefoonnummer, plaats, type pand, aantal deuren, huidige situatie en een toelichting in. Verplicht zijn alleen uw naam, plaats en een telefoonnummer of e-mailadres. Wij gebruiken deze gegevens om uw aanvraag te beantwoorden en een inventarisatie in te plannen. Grondslag: uitvoering van de overeenkomst of de stappen daarvoor op uw verzoek.</p>
<p>Het formulier wordt verstuurd via Web3Forms (Web3Forms, verwerker), dat het bericht doorstuurt naar onze mailbox {esc(FORM_MAILBOX)}. Web3Forms bewaart de inzending kort voor de bezorging. Wij bewaren uw aanvraag zolang nodig voor de afhandeling en daarna maximaal twee jaar voor eventuele vervolgvragen, tenzij er een overeenkomst uit voortkomt; dan gelden de bewaartermijnen van onze administratie.</p>
<h2>Cookies en meting</h2>
{meting}
<p>Noodzakelijke opslag: de site onthoudt in uw browser alleen uw cookiekeuze en, na het versturen van een formulier, dat de bedanktpagina al is geteld. Daar zitten geen persoonsgegevens in.</p>
<h2>Externe verbindingen</h2>
<p>De site laadt lettertypen en beelden van de eigen server. Externe verbindingen zijn er alleen naar Web3Forms (bij het versturen van het formulier) en, na toestemming, naar Google. Er staan geen ingesloten kaarten, video's of chatdiensten van derden op de site.</p>
<h2>Telefoon en e-mail</h2>
<p>Belt of mailt u ons, dan gebruiken wij uw gegevens alleen voor het beantwoorden van uw vraag en, als daar een aanvraag uit volgt, voor de offerte en de uitvoering.</p>
<h2>Uw rechten</h2>
<p>U kunt ons vragen welke gegevens wij van u hebben, ze laten corrigeren of verwijderen, en bezwaar maken tegen de verwerking. Mail daarvoor naar <a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a> of bel {tel()}. Bent u het niet eens met hoe wij met uw gegevens omgaan, dan kunt u een klacht indienen bij de Autoriteit Persoonsgegevens.</p>
<h2>Contact</h2>
<address><p>{esc(NAAM)}<br>{esc(STRAAT)}<br>{esc(POSTCODE)} {esc(PLAATS)}<br>{esc(RECHTSPERSOON)}, KvK {esc(KVK)}, inschrijfadres {esc(KVK_ADRES)}<br><a href="mailto:{esc(MAIL)}">{esc(MAIL)}</a></p></address>
</div></div></div></section>'''
    schrijf(PAD, titel, omschrijving, body, kruimelpad=[("Home", "/"), ("Privacy", PAD)], met_formulier=False,
            llms="Privacyverklaring: verwerking van het aanvraagformulier via Web3Forms, cookies pas na toestemming (Consent Mode v2), rechten en contact.")
