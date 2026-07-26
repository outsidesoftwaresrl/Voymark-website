#!/usr/bin/env python3
"""Generates the six language pages from one template.

Usage: python3 scripts/build_i18n.py   (run from the repo root)

English lands at /index.html; the rest at /<lang>/index.html.
Keep translations in tone with the app's Strings*.swift tables.
"""

import os

LANGS = ["en", "fr", "es", "it", "de", "ro"]

T = {
"title": {
 "en": "Voymark — Every journey leaves a mark.",
 "fr": "Voymark — Chaque voyage laisse une trace.",
 "es": "Voymark — Cada viaje deja una huella.",
 "it": "Voymark — Ogni viaggio lascia un segno.",
 "de": "Voymark — Jede Reise hinterlässt eine Spur.",
 "ro": "Voymark — Fiecare călătorie lasă o urmă.",
},
"meta": {
 "en": "Voymark is your world passport: a living map of countries, trips, places and memories — built from the photos already on your iPhone. Offline-first, no account, no tracking.",
 "fr": "Voymark est votre passeport du monde : une carte vivante de pays, voyages, lieux et souvenirs — construite à partir des photos déjà sur votre iPhone. Hors ligne d'abord, sans compte, sans suivi.",
 "es": "Voymark es tu pasaporte del mundo: un mapa vivo de países, viajes, lugares y recuerdos — construido con las fotos que ya están en tu iPhone. Offline primero, sin cuenta, sin rastreo.",
 "it": "Voymark è il tuo passaporto del mondo: una mappa viva di paesi, viaggi, luoghi e ricordi — costruita dalle foto già sul tuo iPhone. Offline-first, senza account, senza tracciamento.",
 "de": "Voymark ist dein Weltpass: eine lebendige Karte aus Ländern, Reisen, Orten und Erinnerungen — gebaut aus den Fotos, die schon auf deinem iPhone sind. Offline-first, ohne Konto, ohne Tracking.",
 "ro": "Voymark este pașaportul tău al lumii: o hartă vie de țări, călătorii, locuri și amintiri — construită din pozele aflate deja pe iPhone-ul tău. Offline mai întâi, fără cont, fără urmărire.",
},
"h1": {
 "en": "Every journey leaves a&nbsp;mark.",
 "fr": "Chaque voyage laisse une&nbsp;trace.",
 "es": "Cada viaje deja una&nbsp;huella.",
 "it": "Ogni viaggio lascia un&nbsp;segno.",
 "de": "Jede Reise hinterlässt eine&nbsp;Spur.",
 "ro": "Fiecare călătorie lasă o&nbsp;urmă.",
},
"lede": {
 "en": "Voymark is your world passport — a living map of countries, trips, places and memories, built by hand or from the photos already on your iPhone.",
 "fr": "Voymark est votre passeport du monde — une carte vivante de pays, voyages, lieux et souvenirs, construite à la main ou à partir des photos déjà sur votre iPhone.",
 "es": "Voymark es tu pasaporte del mundo — un mapa vivo de países, viajes, lugares y recuerdos, construido a mano o con las fotos que ya están en tu iPhone.",
 "it": "Voymark è il tuo passaporto del mondo — una mappa viva di paesi, viaggi, luoghi e ricordi, costruita a mano o dalle foto già sul tuo iPhone.",
 "de": "Voymark ist dein Weltpass — eine lebendige Karte aus Ländern, Reisen, Orten und Erinnerungen, von Hand gebaut oder aus den Fotos, die schon auf deinem iPhone sind.",
 "ro": "Voymark este pașaportul tău al lumii — o hartă vie de țări, călătorii, locuri și amintiri, construită manual sau din pozele aflate deja pe iPhone-ul tău.",
},
"badge_small": {
 "en": "Coming soon to the", "fr": "Bientôt sur l'", "es": "Muy pronto en el",
 "it": "Presto sull'", "de": "Bald im", "ro": "În curând pe",
},
"s1_h": {
 "en": "Four maps. One passport.", "fr": "Quatre cartes. Un passeport.",
 "es": "Cuatro mapas. Un pasaporte.", "it": "Quattro mappe. Un passaporto.",
 "de": "Vier Karten. Ein Pass.", "ro": "Patru hărți. Un pașaport.",
},
"atlas_h": {"en": "🗺️ Atlas", "fr": "🗺️ Atlas", "es": "🗺️ Atlas", "it": "🗺️ Atlante", "de": "🗺️ Atlas", "ro": "🗺️ Atlas"},
"atlas_p": {
 "en": "A clean, flat world map with country names in your language — fully offline, zoom from the whole world down to a single region. Tap any country to stamp it.",
 "fr": "Une carte du monde nette et épurée avec les noms des pays dans votre langue — entièrement hors ligne, du monde entier jusqu'à une seule région. Touchez un pays pour le tamponner.",
 "es": "Un mapa del mundo limpio y plano con los nombres de países en tu idioma — totalmente offline, del mundo entero a una sola región. Toca un país para sellarlo.",
 "it": "Una mappa del mondo pulita e piatta con i nomi dei paesi nella tua lingua — completamente offline, dal mondo intero a una singola regione. Tocca un paese per timbrarlo.",
 "de": "Eine klare, flache Weltkarte mit Ländernamen in deiner Sprache — komplett offline, von der ganzen Welt bis zu einer einzelnen Region. Tippe ein Land an, um es zu stempeln.",
 "ro": "O hartă a lumii curată și plată, cu numele țărilor în limba ta — complet offline, de la întreaga lume până la o singură regiune. Atinge o țară pentru a o ștampila.",
},
"paper_h": {"en": "📜 Paper", "fr": "📜 Papier", "es": "📜 Papel", "it": "📜 Carta", "de": "📜 Papier", "ro": "📜 Hârtie"},
"paper_p": {
 "en": "The same passport, drawn as an aged atlas — burgundy stamps pressed into parchment. Your travel history as it deserves to look.",
 "fr": "Le même passeport, dessiné comme un atlas ancien — tampons bordeaux pressés dans le parchemin. Votre histoire de voyage comme elle mérite d'être vue.",
 "es": "El mismo pasaporte, dibujado como un atlas antiguo — sellos burdeos impresos en pergamino. Tu historia de viajes como merece verse.",
 "it": "Lo stesso passaporto, disegnato come un atlante antico — timbri bordeaux impressi nella pergamena. La tua storia di viaggio come merita di apparire.",
 "de": "Derselbe Pass, gezeichnet wie ein alter Atlas — burgunderrote Stempel im Pergament. Deine Reisegeschichte, wie sie aussehen sollte.",
 "ro": "Același pașaport, desenat ca un atlas vechi — ștampile burgundy presate în pergament. Istoria ta de călătorie așa cum merită să arate.",
},
"modern_h": {
 "en": "🧭 Modern &amp; Satellite", "fr": "🧭 Moderne &amp; Satellite", "es": "🧭 Moderno &amp; Satélite",
 "it": "🧭 Moderna &amp; Satellite", "de": "🧭 Modern &amp; Satellit", "ro": "🧭 Modern &amp; Satelit",
},
"modern_p": {
 "en": "Apple Maps styles with your visited countries inked over them, place pins, trip routes and photo markers — all in sync with the Atlas.",
 "fr": "Les styles Apple Plans avec vos pays visités encrés par-dessus, épingles de lieux, itinéraires et marqueurs photo — tout en synchro avec l'Atlas.",
 "es": "Los estilos de Apple Maps con tus países visitados entintados encima, pines de lugares, rutas de viajes y marcadores de fotos — todo en sincronía con el Atlas.",
 "it": "Gli stili di Mappe Apple con i tuoi paesi visitati inchiostrati sopra, segnaposto, rotte dei viaggi e marcatori foto — tutto in sincronia con l'Atlante.",
 "de": "Apple-Karten-Stile mit deinen besuchten Ländern darüber, Orts-Pins, Reiserouten und Foto-Markern — alles synchron mit dem Atlas.",
 "ro": "Stilurile Apple Maps cu țările tale vizitate colorate deasupra, pinuri de locuri, rute de călătorie și marcaje foto — totul în sincron cu Atlasul.",
},
"cities_h": {"en": "🏙️ Cities", "fr": "🏙️ Villes", "es": "🏙️ Ciudades", "it": "🏙️ Città", "de": "🏙️ Städte", "ro": "🏙️ Orașe"},
"cities_p": {
 "en": "7,000+ notable cities worldwide. Check them off by hand — or let your trips seal them automatically as evidence.",
 "fr": "Plus de 7 000 villes notables dans le monde. Cochez-les à la main — ou laissez vos voyages les sceller automatiquement comme preuves.",
 "es": "Más de 7.000 ciudades notables en el mundo. Márcalas a mano — o deja que tus viajes las sellen automáticamente como evidencia.",
 "it": "Oltre 7.000 città notevoli nel mondo. Spuntale a mano — o lascia che i tuoi viaggi le sigillino automaticamente come prova.",
 "de": "Über 7.000 bedeutende Städte weltweit. Hake sie von Hand ab — oder lass deine Reisen sie automatisch als Beleg versiegeln.",
 "ro": "Peste 7.000 de orașe importante din lume. Bifează-le manual — sau lasă călătoriile tale să le sigileze automat ca dovadă.",
},
"s2_h": {
 "en": "Your history builds itself", "fr": "Votre histoire se construit toute seule",
 "es": "Tu historia se construye sola", "it": "La tua storia si costruisce da sola",
 "de": "Deine Geschichte baut sich von selbst", "ro": "Istoria ta se construiește singură",
},
"photos_h": {
 "en": "📸 From your photos", "fr": "📸 Depuis vos photos", "es": "📸 Desde tus fotos",
 "it": "📸 Dalle tue foto", "de": "📸 Aus deinen Fotos", "ro": "📸 Din pozele tale",
},
"photos_p": {
 "en": "Voymark reads locations and dates from the photos you allow — entirely on your device — and reconstructs trips, places and country stamps. Nothing is ever uploaded.",
 "fr": "Voymark lit les lieux et les dates des photos que vous autorisez — entièrement sur votre appareil — et reconstruit voyages, lieux et tampons de pays. Rien n'est jamais envoyé.",
 "es": "Voymark lee ubicaciones y fechas de las fotos que permites — por completo en tu dispositivo — y reconstruye viajes, lugares y sellos de países. Nunca se sube nada.",
 "it": "Voymark legge luoghi e date dalle foto che autorizzi — interamente sul tuo dispositivo — e ricostruisce viaggi, luoghi e timbri dei paesi. Nulla viene mai caricato.",
 "de": "Voymark liest Orte und Daten aus den freigegebenen Fotos — vollständig auf deinem Gerät — und rekonstruiert Reisen, Orte und Länderstempel. Nichts wird jemals hochgeladen.",
 "ro": "Voymark citește locațiile și datele din pozele permise — în întregime pe dispozitivul tău — și reconstruiește călătorii, locuri și ștampile de țări. Nimic nu este încărcat vreodată.",
},
"hand_h": {
 "en": "✍️ Or by hand", "fr": "✍️ Ou à la main", "es": "✍️ O a mano",
 "it": "✍️ O a mano", "de": "✍️ Oder von Hand", "ro": "✍️ Sau manual",
},
"hand_p": {
 "en": "Add trips and places with a searchable country list and a tap-on-the-map pin. No coordinates, no forms that fight you. Your manual entries are sacred — no rebuild ever touches them.",
 "fr": "Ajoutez voyages et lieux avec une liste de pays et une épingle posée d'un tap sur la carte. Pas de coordonnées, pas de formulaires hostiles. Vos saisies manuelles sont sacrées — aucune reconstruction n'y touche.",
 "es": "Añade viajes y lugares con una lista de países y un pin con un toque en el mapa. Sin coordenadas, sin formularios que pelean contigo. Tus entradas manuales son sagradas — ninguna reconstrucción las toca.",
 "it": "Aggiungi viaggi e luoghi con un elenco di paesi ricercabile e un segnaposto con un tocco sulla mappa. Niente coordinate, niente moduli ostili. Le tue voci manuali sono sacre — nessuna ricostruzione le tocca.",
 "de": "Füge Reisen und Orte mit einer durchsuchbaren Länderliste und einem Pin per Karten-Tipp hinzu. Keine Koordinaten, keine sperrigen Formulare. Deine manuellen Einträge sind heilig — kein Neuaufbau rührt sie an.",
 "ro": "Adaugă călătorii și locuri cu o listă de țări căutabilă și un pin printr-o atingere pe hartă. Fără coordonate, fără formulare care se luptă cu tine. Intrările tale manuale sunt sacre — nicio reconstrucție nu le atinge.",
},
"rules_h": {
 "en": "🛂 Passport rules", "fr": "🛂 Règles du passeport", "es": "🛂 Reglas del pasaporte",
 "it": "🛂 Regole del passaporto", "de": "🛂 Pass-Regeln", "ro": "🛂 Regulile pașaportului",
},
"rules_p": {
 "en": "Count the world your way: 197, 193 UN members, or all 249 countries and territories. Airport dashes ink the map without claiming the country — your call, always.",
 "fr": "Comptez le monde à votre façon : 197, 193 membres de l'ONU, ou les 249 pays et territoires. Une escale encre la carte sans revendiquer le pays — c'est toujours vous qui décidez.",
 "es": "Cuenta el mundo a tu manera: 197, 193 miembros de la ONU o los 249 países y territorios. Una escala entinta el mapa sin reclamar el país — siempre decides tú.",
 "it": "Conta il mondo a modo tuo: 197, 193 membri ONU o tutti i 249 paesi e territori. Uno scalo inchiostra la mappa senza rivendicare il paese — decidi sempre tu.",
 "de": "Zähle die Welt auf deine Art: 197, 193 UN-Mitglieder oder alle 249 Länder und Territorien. Ein Zwischenstopp färbt die Karte, ohne das Land zu beanspruchen — du entscheidest, immer.",
 "ro": "Numără lumea în felul tău: 197, 193 de membri ONU sau toate cele 249 de țări și teritorii. O escală colorează harta fără a revendica țara — tu decizi, întotdeauna.",
},
"story_h": {
 "en": "📚 Storytelling", "fr": "📚 Récits", "es": "📚 Historias",
 "it": "📚 Racconti", "de": "📚 Geschichten", "ro": "📚 Povești",
},
"story_p": {
 "en": "Annual recaps, route replays, transport stats, share cards for any year, and PDF travel books generated from your own history.",
 "fr": "Rétrospectives annuelles, itinéraires rejoués, statistiques de transport, cartes à partager pour chaque année, et livres de voyage PDF générés à partir de votre propre histoire.",
 "es": "Resúmenes anuales, rutas reproducidas, estadísticas de transporte, tarjetas para compartir de cualquier año y libros de viaje en PDF generados de tu propia historia.",
 "it": "Riepiloghi annuali, rotte rigiocate, statistiche di trasporto, card da condividere per ogni anno e libri di viaggio PDF generati dalla tua storia.",
 "de": "Jahresrückblicke, abgespielte Routen, Transport-Statistiken, Share-Karten für jedes Jahr und PDF-Reisebücher aus deiner eigenen Geschichte.",
 "ro": "Retrospective anuale, rute redate, statistici de transport, carduri de partajat pentru orice an și cărți de călătorie PDF generate din propria ta istorie.",
},
"s3_h": {
 "en": "Compare passports", "fr": "Comparez les passeports", "es": "Compara pasaportes",
 "it": "Confronta i passaporti", "de": "Pässe vergleichen", "ro": "Compară pașapoartele",
},
"s3_p": {
 "en": "Show a friend your QR code — or send a tiny passport file — and see both journeys on one three-color map: only you, only them, and everywhere you've both been. No accounts. Nothing leaves the two phones.",
 "fr": "Montrez votre code QR à un ami — ou envoyez un minuscule fichier passeport — et voyez les deux parcours sur une carte à trois couleurs : seulement vous, seulement l'autre, et partout où vous êtes allés tous les deux. Pas de comptes. Rien ne quitte les deux téléphones.",
 "es": "Muéstrale a un amigo tu código QR — o envía un pequeño archivo de pasaporte — y ve ambos recorridos en un mapa de tres colores: solo tú, solo él, y todos los lugares donde ambos han estado. Sin cuentas. Nada sale de los dos teléfonos.",
 "it": "Mostra a un amico il tuo codice QR — o invia un piccolo file passaporto — e guarda entrambi i percorsi su una mappa a tre colori: solo tu, solo l'altro, e ovunque siate stati entrambi. Niente account. Nulla lascia i due telefoni.",
 "de": "Zeig einem Freund deinen QR-Code — oder schick eine winzige Passdatei — und seht beide Reisen auf einer dreifarbigen Karte: nur du, nur er, und überall, wo ihr beide wart. Keine Konten. Nichts verlässt die beiden Telefone.",
 "ro": "Arată-i unui prieten codul tău QR — sau trimite un fișier-pașaport minuscul — și vedeți ambele călătorii pe o hartă în trei culori: doar tu, doar el, și oriunde ați fost amândoi. Fără conturi. Nimic nu părăsește cele două telefoane.",
},
"s4_h": {
 "en": "Private by architecture", "fr": "Privé par architecture", "es": "Privado por arquitectura",
 "it": "Privato per architettura", "de": "Privat per Architektur", "ro": "Privat prin arhitectură",
},
"p1s": {"en": "Offline-first.", "fr": "Hors ligne d'abord.", "es": "Offline primero.", "it": "Offline-first.", "de": "Offline-first.", "ro": "Offline mai întâi."},
"p1": {
 "en": "Maps, cities, collections — everything ships inside the app. No tile servers, no API calls.",
 "fr": "Cartes, villes, collections — tout est livré dans l'app. Pas de serveurs de tuiles, pas d'appels d'API.",
 "es": "Mapas, ciudades, colecciones — todo viene dentro de la app. Sin servidores de mosaicos, sin llamadas a API.",
 "it": "Mappe, città, collezioni — tutto è incluso nell'app. Niente server di tile, niente chiamate API.",
 "de": "Karten, Städte, Sammlungen — alles steckt in der App. Keine Tile-Server, keine API-Aufrufe.",
 "ro": "Hărți, orașe, colecții — totul vine în aplicație. Fără servere de hărți, fără apeluri API.",
},
"p2s": {"en": "On-device only.", "fr": "Sur l'appareil uniquement.", "es": "Solo en el dispositivo.", "it": "Solo sul dispositivo.", "de": "Nur auf dem Gerät.", "ro": "Doar pe dispozitiv."},
"p2": {
 "en": "Photo scanning happens on your iPhone; images are never copied or uploaded.",
 "fr": "L'analyse des photos se fait sur votre iPhone ; les images ne sont jamais copiées ni envoyées.",
 "es": "El escaneo de fotos ocurre en tu iPhone; las imágenes nunca se copian ni se suben.",
 "it": "La scansione delle foto avviene sul tuo iPhone; le immagini non vengono mai copiate né caricate.",
 "de": "Der Foto-Scan läuft auf deinem iPhone; Bilder werden nie kopiert oder hochgeladen.",
 "ro": "Scanarea pozelor are loc pe iPhone-ul tău; imaginile nu sunt niciodată copiate sau încărcate.",
},
"p3s": {
 "en": "No account. No tracking. No ads.", "fr": "Pas de compte. Pas de suivi. Pas de pub.",
 "es": "Sin cuenta. Sin rastreo. Sin anuncios.", "it": "Nessun account. Nessun tracciamento. Nessuna pubblicità.",
 "de": "Kein Konto. Kein Tracking. Keine Werbung.", "ro": "Fără cont. Fără urmărire. Fără reclame.",
},
"p3": {
 "en": "Backups and exports are files you create and keep.",
 "fr": "Les sauvegardes et exports sont des fichiers que vous créez et gardez.",
 "es": "Las copias de seguridad y exportaciones son archivos que tú creas y guardas.",
 "it": "Backup ed esportazioni sono file che crei e conservi tu.",
 "de": "Backups und Exporte sind Dateien, die du erstellst und behältst.",
 "ro": "Copiile de siguranță și exporturile sunt fișiere pe care le creezi și le păstrezi tu.",
},
"p4s": {"en": "Free.", "fr": "Gratuit.", "es": "Gratis.", "it": "Gratis.", "de": "Kostenlos.", "ro": "Gratuit."},
"p4": {
 "en": "Every feature. We'll never take away what you already have.",
 "fr": "Toutes les fonctionnalités. Nous ne retirerons jamais ce que vous avez déjà.",
 "es": "Todas las funciones. Nunca te quitaremos lo que ya tienes.",
 "it": "Ogni funzione. Non ti toglieremo mai ciò che hai già.",
 "de": "Jede Funktion. Wir nehmen dir nie weg, was du schon hast.",
 "ro": "Fiecare funcție. Nu îți vom lua niciodată ce ai deja.",
},
"s5_h": {
 "en": "Six languages", "fr": "Six langues", "es": "Seis idiomas",
 "it": "Sei lingue", "de": "Sechs Sprachen", "ro": "Șase limbi",
},
"tagline": {
 "en": "Every journey leaves a mark.", "fr": "Chaque voyage laisse une trace.",
 "es": "Cada viaje deja una huella.", "it": "Ogni viaggio lascia un segno.",
 "de": "Jede Reise hinterlässt eine Spur.", "ro": "Fiecare călătorie lasă o urmă.",
},
"credits": {
 "en": "Map data: Natural Earth (public domain). UNESCO sites: Wikidata (CC0).",
 "fr": "Données cartographiques : Natural Earth (domaine public). Sites UNESCO : Wikidata (CC0).",
 "es": "Datos de mapas: Natural Earth (dominio público). Sitios UNESCO: Wikidata (CC0).",
 "it": "Dati mappa: Natural Earth (pubblico dominio). Siti UNESCO: Wikidata (CC0).",
 "de": "Kartendaten: Natural Earth (gemeinfrei). UNESCO-Stätten: Wikidata (CC0).",
 "ro": "Date hartă: Natural Earth (domeniu public). Situri UNESCO: Wikidata (CC0).",
},
}

BASE_URL = "https://outsidesoftwaresrl.github.io/Voymark-website/"

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta}">
  <meta property="og:type" content="website">
{hreflangs}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>

  <nav class="langnav" aria-label="Language">
{langlinks}
  </nav>

  <header class="hero">
    <div class="stamp" aria-hidden="true">
      <span>VOYMARK</span><span>WORLD</span><span>PASSPORT</span>
    </div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="cta">
      <a class="badge badge-disabled" href="#" aria-disabled="true">
        <span class="badge-small">{badge_small}</span>
        <span class="badge-large">App&nbsp;Store</span>
      </a>
    </div>
    <p class="mrz" aria-hidden="true">P&lt;VOYM&lt;&lt;EVERY&lt;JOURNEY&lt;LEAVES&lt;A&lt;MARK&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;<br>197COUNTRIES7CONT&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;2026&lt;4</p>
  </header>

  <main>
    <section class="band">
      <h2>{s1_h}</h2>
      <div class="grid">
        <article><h3>{atlas_h}</h3><p>{atlas_p}</p></article>
        <article><h3>{paper_h}</h3><p>{paper_p}</p></article>
        <article><h3>{modern_h}</h3><p>{modern_p}</p></article>
        <article><h3>{cities_h}</h3><p>{cities_p}</p></article>
      </div>
    </section>

    <section class="band band-alt">
      <h2>{s2_h}</h2>
      <div class="grid">
        <article><h3>{photos_h}</h3><p>{photos_p}</p></article>
        <article><h3>{hand_h}</h3><p>{hand_p}</p></article>
        <article><h3>{rules_h}</h3><p>{rules_p}</p></article>
        <article><h3>{story_h}</h3><p>{story_p}</p></article>
      </div>
    </section>

    <section class="band">
      <h2>{s3_h}</h2>
      <p class="wide">{s3_p}</p>
    </section>

    <section class="band band-privacy">
      <h2>{s4_h}</h2>
      <ul class="privacy-list">
        <li><strong>{p1s}</strong> {p1}</li>
        <li><strong>{p2s}</strong> {p2}</li>
        <li><strong>{p3s}</strong> {p3}</li>
        <li><strong>{p4s}</strong> {p4}</li>
      </ul>
    </section>

    <section class="band band-alt">
      <h2>{s5_h}</h2>
      <p class="wide langs">English · Français · Español · Italiano · Deutsch · Română</p>
    </section>
  </main>

  <footer>
    <p class="tagline">{tagline}</p>
    <p>© <span id="year">2026</span> Outside Software SRL. {credits}</p>
  </footer>

  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

LANG_LABELS = {"en": "EN", "fr": "FR", "es": "ES", "it": "IT", "de": "DE", "ro": "RO"}


def url_for(lang):
    return BASE_URL if lang == "en" else f"{BASE_URL}{lang}/"


def build(lang):
    root = "" if lang == "en" else "../"
    hreflangs = "\n".join(
        f'  <link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{BASE_URL}">'
    def link(l):
        cls = ' class="current"' if l == lang else ""
        return f'    <a href="{url_for(l)}"{cls}>{LANG_LABELS[l]}</a>'

    langlinks = "\n".join(link(l) for l in LANGS)

    values = {key: T[key][lang] for key in T}
    html = TEMPLATE.format(lang=lang, root=root, hreflangs=hreflangs, langlinks=langlinks, **values)

    out = "index.html" if lang == "en" else f"{lang}/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True) if "/" in out else None
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out)


if __name__ == "__main__":
    for lang in LANGS:
        build(lang)
