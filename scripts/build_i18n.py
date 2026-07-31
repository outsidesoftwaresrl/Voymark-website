#!/usr/bin/env python3
"""Generates the six language pages from one template.

Usage: python3 scripts/build_i18n.py   (run from the repo root)

English lands at /index.html; the rest at /<lang>/index.html.
Keep translations in tone with the app's Strings*.swift tables.
"""

import html
import json
import os
import re
import subprocess

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
 "en": "Voymark is your world passport: a living map of countries, trips, places and memories — built from the photos already on your phone. Offline-first, no account, no tracking.",
 "fr": "Voymark est votre passeport du monde : une carte vivante de pays, voyages, lieux et souvenirs — construite à partir des photos déjà sur votre téléphone. Hors ligne d'abord, sans compte, sans suivi.",
 "es": "Voymark es tu pasaporte del mundo: un mapa vivo de países, viajes, lugares y recuerdos — construido con las fotos que ya están en tu teléfono. Offline primero, sin cuenta, sin rastreo.",
 "it": "Voymark è il tuo passaporto del mondo: una mappa viva di paesi, viaggi, luoghi e ricordi — costruita dalle foto già sul tuo telefono. Offline-first, senza account, senza tracciamento.",
 "de": "Voymark ist dein Weltpass: eine lebendige Karte aus Ländern, Reisen, Orten und Erinnerungen — gebaut aus den Fotos, die schon auf deinem Handy sind. Offline-first, ohne Konto, ohne Tracking.",
 "ro": "Voymark este pașaportul lumii tale: o hartă vie de țări, călătorii, locuri și amintiri — construită din pozele aflate deja pe telefonul tău. Offline mai întâi, fără cont, fără urmărire.",
},
"regions_h": {
 "en": "🏛️ States &amp; regions",
 "fr": "🏛️ États &amp; régions",
 "es": "🏛️ Estados y regiones",
 "it": "🏛️ Stati e regioni",
 "de": "🏛️ Staaten &amp; Regionen",
 "ro": "🏛️ State și regiuni",
},
"regions_p": {
 "en": "Twelve countries go deeper: US states, German Länder, Japanese prefectures and more — 290 regions on their own tap-to-stamp maps.",
 "fr": "Douze pays vont plus loin : États américains, Länder allemands, préfectures japonaises et plus — 290 régions sur leurs propres cartes à tamponner.",
 "es": "Doce países van más allá: estados de EE.&nbsp;UU., Länder alemanes, prefecturas japonesas y más — 290 regiones en sus propios mapas para sellar.",
 "it": "Dodici paesi vanno più a fondo: stati USA, Länder tedeschi, prefetture giapponesi e altro — 290 regioni su mappe proprie, da timbrare al tocco.",
 "de": "Zwölf Länder gehen tiefer: US-Bundesstaaten, deutsche Bundesländer, japanische Präfekturen und mehr — 290 Regionen auf eigenen Karten zum Stempeln.",
 "ro": "Douăsprezece țări merg mai departe: statele americane, landurile germane, prefecturile japoneze și altele — 290 de regiuni pe propriile hărți de ștampilat.",
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
 "en": "Voymark is your world passport — a living map of countries, trips, places and memories, built by hand or from the photos already on your phone.",
 "fr": "Voymark est votre passeport du monde — une carte vivante de pays, voyages, lieux et souvenirs, construite à la main ou à partir des photos déjà sur votre téléphone.",
 "es": "Voymark es tu pasaporte del mundo — un mapa vivo de países, viajes, lugares y recuerdos, construido a mano o con las fotos que ya están en tu teléfono.",
 "it": "Voymark è il tuo passaporto del mondo — una mappa viva di paesi, viaggi, luoghi e ricordi, costruita a mano o dalle foto già sul tuo telefono.",
 "de": "Voymark ist dein Weltpass — eine lebendige Karte aus Ländern, Reisen, Orten und Erinnerungen, von Hand gebaut oder aus den Fotos, die schon auf deinem Handy sind.",
 "ro": "Voymark este pașaportul lumii tale — o hartă vie de țări, călătorii, locuri și amintiri, construită manual sau din pozele aflate deja pe telefonul tău.",
},
"badge_small": {
 "en": "Coming soon to the", "fr": "Bientôt sur l'", "es": "Muy pronto en el",
 "it": "Presto sull'", "de": "Bald im", "ro": "În curând pe",
},
"badge_small_android": {
 "en": "Coming soon to", "fr": "Bientôt sur", "es": "Muy pronto en",
 "it": "Presto su", "de": "Bald bei", "ro": "În curând pe",
},
"shots_title": {
 "en": "Straight from the app", "fr": "Directement depuis l'app", "es": "Directo desde la app",
 "it": "Direttamente dall'app", "de": "Direkt aus der App", "ro": "Direct din aplicație",
},
"shots_alt_map": {
 "en": "The Voymark map with visited countries stamped in burgundy",
 "fr": "La carte Voymark avec les pays visités tamponnés en bordeaux",
 "es": "El mapa de Voymark con los países visitados sellados en burdeos",
 "it": "La mappa Voymark con i paesi visitati timbrati in bordeaux",
 "de": "Die Voymark-Karte mit burgunderrot gestempelten besuchten Ländern",
 "ro": "Harta Voymark cu țările vizitate ștampilate în burgundy",
},
"shots_alt_passport": {
 "en": "The Voymark passport screen with country stamps",
 "fr": "L'écran passeport de Voymark avec des tampons de pays",
 "es": "La pantalla de pasaporte de Voymark con sellos de países",
 "it": "La schermata passaporto di Voymark con timbri dei paesi",
 "de": "Der Voymark-Pass-Bildschirm mit Länderstempeln",
 "ro": "Ecranul de pașaport Voymark cu ștampile de țări",
},
"shots_alt_timeline": {
 "en": "The Voymark timeline of trips by year",
 "fr": "La chronologie Voymark des voyages par année",
 "es": "La línea de tiempo de Voymark con viajes por año",
 "it": "La cronologia Voymark dei viaggi per anno",
 "de": "Die Voymark-Zeitleiste der Reisen nach Jahr",
 "ro": "Cronologia Voymark a călătoriilor pe ani",
},
"nav_privacy": {
 "en": "Privacy", "fr": "Confidentialité", "es": "Privacidad",
 "it": "Privacy", "de": "Datenschutz", "ro": "Confidențialitate",
},
"nav_terms": {
 "en": "Terms", "fr": "Conditions", "es": "Términos",
 "it": "Termini", "de": "Nutzungsbedingungen", "ro": "Termeni",
},
"nav_explore": {
 "en": "Explore", "fr": "Explorer", "es": "Explorar",
 "it": "Esplora", "de": "Entdecken", "ro": "Explorează",
},
"s1_h": {
 "en": "Your maps. Your passport.", "fr": "Vos cartes. Votre passeport.",
 "es": "Tus mapas. Tu pasaporte.", "it": "Le tue mappe. Il tuo passaporto.",
 "de": "Deine Karten. Dein Pass.", "ro": "Hărțile tale. Pașaportul tău.",
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
 "en": "🧭 Modern &amp; Satellite <small>· iPhone</small>", "fr": "🧭 Moderne &amp; Satellite <small>· iPhone</small>",
 "es": "🧭 Moderno &amp; Satélite <small>· iPhone</small>", "it": "🧭 Moderna &amp; Satellite <small>· iPhone</small>",
 "de": "🧭 Modern &amp; Satellit <small>· iPhone</small>", "ro": "🧭 Modern &amp; Satelit <small>· iPhone</small>",
},
"modern_p": {
 "en": "On iPhone, two extra Apple Maps styles with your visited countries inked over them — pins, routes and photo markers stay in sync with the Atlas.",
 "fr": "Sur iPhone, deux styles Apple Plans supplémentaires avec vos pays visités encrés par-dessus — épingles, itinéraires et marqueurs photo restent en synchro avec l'Atlas.",
 "es": "En iPhone, dos estilos extra de Apple Maps con tus países visitados entintados encima — pines, rutas y marcadores de fotos siguen en sincronía con el Atlas.",
 "it": "Su iPhone, due stili extra di Mappe Apple con i tuoi paesi visitati inchiostrati sopra — segnaposto, rotte e marcatori foto restano in sincronia con l'Atlante.",
 "de": "Auf dem iPhone zwei zusätzliche Apple-Karten-Stile mit deinen besuchten Ländern darüber — Pins, Routen und Foto-Marker bleiben synchron mit dem Atlas.",
 "ro": "Pe iPhone, două stiluri Apple Maps în plus, cu țările tale vizitate colorate deasupra — pinurile, rutele și marcajele foto rămân în sincron cu Atlasul.",
},
"layers_h": {
 "en": "🧷 Layers &amp; routes", "fr": "🧷 Calques &amp; itinéraires", "es": "🧷 Capas &amp; rutas",
 "it": "🧷 Livelli &amp; rotte", "de": "🧷 Ebenen &amp; Routen", "ro": "🧷 Straturi &amp; rute",
},
"layers_p": {
 "en": "Place pins, trip routes, photo markers, cities and wishlist shading — flip each layer on or off, on both the Atlas and the Paper map.",
 "fr": "Épingles de lieux, itinéraires de voyage, marqueurs photo, villes et liste d'envies — activez ou coupez chaque calque, sur l'Atlas comme sur la carte Papier.",
 "es": "Pines de lugares, rutas de viaje, marcadores de fotos, ciudades y lista de deseos — activa o desactiva cada capa, tanto en el Atlas como en el mapa de Papel.",
 "it": "Segnaposto, rotte dei viaggi, marcatori foto, città e lista dei desideri — accendi o spegni ogni livello, sia sull'Atlante sia sulla mappa di Carta.",
 "de": "Orts-Pins, Reiserouten, Foto-Marker, Städte und Wunschliste — jede Ebene einzeln schaltbar, auf dem Atlas wie auf der Papierkarte.",
 "ro": "Pinuri de locuri, rute de călătorie, marcaje foto, orașe și lista de dorințe — aprinzi sau stingi fiecare strat, atât pe Atlas, cât și pe harta de Hârtie.",
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
 "en": "Atlas, Paper map, cities, collections — everything ships inside the app and works in airplane mode. Only the optional Apple Maps styles on iPhone fetch map tiles.",
 "fr": "Atlas, carte Papier, villes, collections — tout est livré dans l'app et fonctionne en mode avion. Seuls les styles Apple Plans optionnels sur iPhone chargent des tuiles.",
 "es": "Atlas, mapa de Papel, ciudades, colecciones — todo viene dentro de la app y funciona en modo avión. Solo los estilos opcionales de Apple Maps en iPhone cargan mosaicos.",
 "it": "Atlante, mappa di Carta, città, collezioni — tutto è incluso nell'app e funziona in modalità aereo. Solo gli stili opzionali di Mappe Apple su iPhone scaricano tile.",
 "de": "Atlas, Papierkarte, Städte, Sammlungen — alles steckt in der App und läuft im Flugmodus. Nur die optionalen Apple-Karten-Stile auf dem iPhone laden Kartenkacheln.",
 "ro": "Atlas, hartă de Hârtie, orașe, colecții — totul vine în aplicație și merge în modul avion. Doar stilurile opționale Apple Maps de pe iPhone încarcă dale de hartă.",
},
"p2s": {"en": "On-device only.", "fr": "Sur l'appareil uniquement.", "es": "Solo en el dispositivo.", "it": "Solo sul dispositivo.", "de": "Nur auf dem Gerät.", "ro": "Doar pe dispozitiv."},
"p2": {
 "en": "Photo scanning happens on your phone; images are never copied or uploaded.",
 "fr": "L'analyse des photos se fait sur votre téléphone ; les images ne sont jamais copiées ni envoyées.",
 "es": "El escaneo de fotos ocurre en tu teléfono; las imágenes nunca se copian ni se suben.",
 "it": "La scansione delle foto avviene sul tuo telefono; le immagini non vengono mai copiate né caricate.",
 "de": "Der Foto-Scan läuft auf deinem Handy; Bilder werden nie kopiert oder hochgeladen.",
 "ro": "Scanarea pozelor are loc pe telefonul tău; imaginile nu sunt niciodată copiate sau încărcate.",
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
"collections_h": {
 "en": "🏛️ Landmark collections", "fr": "🏛️ Collections de sites",
 "es": "🏛️ Colecciones de lugares", "it": "🏛️ Collezioni di luoghi",
 "de": "🏛️ Sehenswürdigkeiten", "ro": "🏛️ Colecții de locuri",
},
"collections_p": {
 "en": "All 197 capitals, 1,351 UNESCO World Heritage sites, the New 7 Wonders and the 7 Natural Wonders. Your trips and geotagged photos claim them for you, dated by the earliest evidence — the rest you tick off by hand.",
 "fr": "Les 197 capitales, 1 351 sites du patrimoine mondial de l'UNESCO, les 7 nouvelles merveilles et les 7 merveilles naturelles. Vos voyages et vos photos géolocalisées les réclament pour vous, datés par la première preuve — le reste se coche à la main.",
 "es": "Las 197 capitales, 1351 sitios del Patrimonio Mundial de la UNESCO, las 7 nuevas maravillas y las 7 maravillas naturales. Tus viajes y tus fotos geolocalizadas los reclaman por ti, fechados por la primera evidencia — el resto lo marcas a mano.",
 "it": "Tutte le 197 capitali, 1.351 siti del Patrimonio Mondiale UNESCO, le 7 nuove meraviglie e le 7 meraviglie naturali. I tuoi viaggi e le tue foto geolocalizzate li reclamano per te, datati dalla prima prova — il resto lo spunti a mano.",
 "de": "Alle 197 Hauptstädte, 1.351 UNESCO-Welterbestätten, die 7 neuen Weltwunder und die 7 Naturwunder. Deine Reisen und deine verorteten Fotos holen sie für dich, datiert auf den frühesten Beleg — den Rest hakst du selbst ab.",
 "ro": "Toate cele 197 de capitale, 1.351 de situri din patrimoniul mondial UNESCO, cele 7 noi minuni și cele 7 minuni naturale. Călătoriile și pozele tale geolocalizate le revendică singure, datate după cea mai veche dovadă — restul le bifezi manual.",
},
"journal_h": {
 "en": "📔 Journal &amp; companions", "fr": "📔 Journal &amp; compagnons",
 "es": "📔 Diario y compañeros", "it": "📔 Diario e compagni",
 "de": "📔 Tagebuch &amp; Begleiter", "ro": "📔 Jurnal și însoțitori",
},
"journal_p": {
 "en": "Write a page for any day of a trip, and record who you were with. The names filter your timeline; the pages are printed into your PDF travel book.",
 "fr": "Écrivez une page pour n'importe quel jour d'un voyage, et notez avec qui vous étiez. Les noms filtrent votre chronologie ; les pages s'impriment dans votre livre de voyage PDF.",
 "es": "Escribe una página para cualquier día de un viaje y anota con quién estabas. Los nombres filtran tu cronología; las páginas se imprimen en tu libro de viaje en PDF.",
 "it": "Scrivi una pagina per ogni giorno di un viaggio e annota con chi eri. I nomi filtrano la tua cronologia; le pagine finiscono stampate nel tuo libro di viaggio PDF.",
 "de": "Schreib eine Seite zu jedem Reisetag und halt fest, mit wem du unterwegs warst. Die Namen filtern deine Zeitleiste; die Seiten werden in dein PDF-Reisebuch gedruckt.",
 "ro": "Scrie o pagină pentru orice zi dintr-o călătorie și notează cu cine ai fost. Numele îți filtrează cronologia; paginile se tipăresc în cartea ta de călătorie PDF.",
},
"s6_h": {
 "en": "The passport keeps score", "fr": "Le passeport tient les comptes",
 "es": "El pasaporte lleva la cuenta", "it": "Il passaporto tiene il conto",
 "de": "Der Pass führt Buch", "ro": "Pașaportul ține socoteala",
},
"seals_h": {
 "en": "🏅 Seals", "fr": "🏅 Sceaux", "es": "🏅 Sellos",
 "it": "🏅 Sigilli", "de": "🏅 Siegel", "ro": "🏅 Sigilii",
},
"seals_p": {
 "en": "Around 29 seals pressed automatically from your own record — country milestones, every continent, the Arctic Circle, the equator, your antipode. Change your counting rule and a borderline seal can honestly lock again.",
 "fr": "Environ 29 sceaux apposés automatiquement d'après votre propre histoire — jalons de pays, chaque continent, le cercle polaire, l'équateur, votre antipode. Changez de règle de comptage et un sceau limite peut honnêtement se reverrouiller.",
 "es": "Unos 29 sellos estampados automáticamente desde tu propio registro — hitos de países, cada continente, el círculo polar, el ecuador, tu antípoda. Cambia tu regla de conteo y un sello límite puede bloquearse de nuevo, con toda honestidad.",
 "it": "Circa 29 sigilli impressi automaticamente dal tuo stesso archivio — traguardi di paesi, ogni continente, il circolo polare, l'equatore, il tuo antipodo. Cambia la regola di conteggio e un sigillo al limite può onestamente richiudersi.",
 "de": "Rund 29 Siegel, automatisch aus deiner eigenen Bilanz gestempelt — Länder-Meilensteine, jeder Kontinent, der Polarkreis, der Äquator, dein Antipode. Änderst du deine Zählregel, darf ein Grenzfall-Siegel ehrlich wieder zufallen.",
 "ro": "Aproximativ 29 de sigilii aplicate automat din propria ta evidență — praguri de țări, fiecare continent, cercul polar, ecuatorul, antipodul tău. Schimbi regula de numărare și un sigiliu la limită se poate încuia din nou, cinstit.",
},
"timemachine_h": {
 "en": "🕰️ Time machine", "fr": "🕰️ Machine à remonter le temps",
 "es": "🕰️ Máquina del tiempo", "it": "🕰️ Macchina del tempo",
 "de": "🕰️ Zeitmaschine", "ro": "🕰️ Mașina timpului",
},
"timemachine_p": {
 "en": "Drag a year and the world recolours to exactly where you had been by then. Export any year as an eight-second vertical video — countries stamping in on their real dates, routes drawing themselves.",
 "fr": "Faites glisser une année et le monde se recolore exactement selon vos voyages d'alors. Exportez n'importe quelle année en vidéo verticale de huit secondes — les pays s'y tamponnent à leurs vraies dates, les itinéraires se tracent seuls.",
 "es": "Arrastra un año y el mundo se recolorea justo hasta donde habías llegado entonces. Exporta cualquier año como un vídeo vertical de ocho segundos — los países se sellan en sus fechas reales y las rutas se dibujan solas.",
 "it": "Trascina un anno e il mondo si ricolora esattamente su dove eri arrivato allora. Esporta qualsiasi anno come video verticale di otto secondi — i paesi si timbrano alle loro date vere, le rotte si disegnano da sole.",
 "de": "Zieh an einem Jahr und die Welt färbt sich genau so ein, wie weit du damals warst. Exportier jedes Jahr als acht Sekunden langes Hochkant-Video — Länder stempeln sich an ihren echten Daten ein, Routen zeichnen sich selbst.",
 "ro": "Trage de un an și lumea se recolorează exact până unde ajunseseși atunci. Exportă orice an ca video vertical de opt secunde — țările se ștampilează la datele lor reale, traseele se desenează singure.",
},
"widgets_h": {
 "en": "📱 Widgets &amp; voice", "fr": "📱 Widgets &amp; voix",
 "es": "📱 Widgets y voz", "it": "📱 Widget e voce",
 "de": "📱 Widgets &amp; Sprache", "ro": "📱 Widgeturi și voce",
},
"widgets_p": {
 "en": "Your count, your best continent and your share of the world, on the home screen. On iPhone you can also just ask Siri how many countries you've visited.",
 "fr": "Votre total, votre meilleur continent et votre part du monde, sur l'écran d'accueil. Sur iPhone, vous pouvez aussi simplement demander à Siri combien de pays vous avez visités.",
 "es": "Tu cuenta, tu mejor continente y tu porcentaje del mundo, en la pantalla de inicio. En iPhone también puedes preguntarle a Siri cuántos países has visitado.",
 "it": "Il tuo conteggio, il tuo continente migliore e la tua fetta di mondo, sulla schermata home. Su iPhone puoi anche chiedere a Siri quanti paesi hai visitato.",
 "de": "Dein Zähler, dein bester Kontinent und dein Anteil an der Welt, auf dem Homescreen. Auf dem iPhone kannst du Siri auch einfach fragen, in wie vielen Ländern du warst.",
 "ro": "Numărul tău, continentul tău cel mai bun și partea ta de lume, direct pe ecranul principal. Pe iPhone poți pur și simplu să o întrebi pe Siri în câte țări ai fost.",
},
"icloud_h": {
 "en": "☁️ Your own iCloud <small>· iPhone</small>", "fr": "☁️ Votre propre iCloud <small>· iPhone</small>",
 "es": "☁️ Tu propio iCloud <small>· iPhone</small>", "it": "☁️ Il tuo iCloud <small>· iPhone</small>",
 "de": "☁️ Deine eigene iCloud <small>· iPhone</small>", "ro": "☁️ Propriul tău iCloud <small>· iPhone</small>",
},
"icloud_p": {
 "en": "Switch on iCloud sync and your passport travels between your own devices — through your iCloud account, not ours. There is no Voymark account to make, and the app keeps working when iCloud doesn't.",
 "fr": "Activez la synchronisation iCloud et votre passeport circule entre vos appareils — via votre compte iCloud, pas le nôtre. Il n'y a aucun compte Voymark à créer, et l'application continue de fonctionner quand iCloud ne répond pas.",
 "es": "Activa la sincronización con iCloud y tu pasaporte viaja entre tus dispositivos — por tu cuenta de iCloud, no la nuestra. No hay ninguna cuenta Voymark que crear, y la app sigue funcionando cuando iCloud no lo hace.",
 "it": "Attiva la sincronizzazione iCloud e il tuo passaporto viaggia tra i tuoi dispositivi — attraverso il tuo account iCloud, non il nostro. Non c'è nessun account Voymark da creare, e l'app continua a funzionare quando iCloud non risponde.",
 "de": "Schalte die iCloud-Synchronisierung ein und dein Pass wandert zwischen deinen Geräten — über deine iCloud, nicht unsere. Es gibt kein Voymark-Konto anzulegen, und die App läuft weiter, wenn iCloud es nicht tut.",
 "ro": "Pornește sincronizarea iCloud și pașaportul tău circulă între dispozitivele tale — prin contul tău de iCloud, nu al nostru. Nu ai niciun cont Voymark de creat, iar aplicația merge mai departe și când iCloud nu merge.",
},
"p5s": {"en": "Readable.", "fr": "Lisible.", "es": "Legible.", "it": "Leggibile.", "de": "Lesbar.", "ro": "Lizibil."},
"p5": {
 "en": "One export writes your whole travel record as plain text — every country, trip, place and note, in a file you can open anywhere, forever, without us.",
 "fr": "Un export écrit toute votre histoire de voyage en texte brut — chaque pays, voyage, lieu et note, dans un fichier lisible partout, pour toujours, sans nous.",
 "es": "Una exportación escribe todo tu registro de viajes en texto plano — cada país, viaje, lugar y nota, en un archivo que puedes abrir en cualquier parte, para siempre, sin nosotros.",
 "it": "Un export scrive tutta la tua storia di viaggio in testo semplice — ogni paese, viaggio, luogo e nota, in un file che puoi aprire ovunque, per sempre, senza di noi.",
 "de": "Ein Export schreibt deine ganze Reisebilanz als reinen Text — jedes Land, jede Reise, jeden Ort und jede Notiz, in einer Datei, die du überall öffnen kannst, für immer, auch ohne uns.",
 "ro": "Un export îți scrie toată istoria de călătorie ca text simplu — fiecare țară, călătorie, loc și notiță, într-un fișier pe care îl deschizi oriunde, oricând, și fără noi.",
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
"trust1": {
 "en": "Free · no subscription", "fr": "Gratuit · sans abonnement",
 "es": "Gratis · sin suscripción", "it": "Gratis · senza abbonamento",
 "de": "Kostenlos · ohne Abo", "ro": "Gratuit · fără abonament",
},
"trust2": {
 "en": "Works offline", "fr": "Fonctionne hors ligne", "es": "Funciona sin conexión",
 "it": "Funziona offline", "de": "Funktioniert offline", "ro": "Funcționează offline",
},
"trust3": {
 "en": "No account · no tracking", "fr": "Sans compte · sans suivi",
 "es": "Sin cuenta · sin rastreo", "it": "Senza account · senza tracciamento",
 "de": "Kein Konto · kein Tracking", "ro": "Fără cont · fără urmărire",
},
"faq_title": {
 "en": "Common questions", "fr": "Questions fréquentes",
 "es": "Preguntas frecuentes", "it": "Domande frequenti",
 "de": "Häufige Fragen", "ro": "Întrebări frecvente",
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

# The site moved to its own apex domain (Florentin, 2026-07-31). Everything
# absolute is built from here — canonical, og:url, hreflang, the visible
# language switcher, the sitemap and robots.txt — so this one line is the
# whole move. The CNAME file next to it keeps GitHub Pages pointed at the
# domain across deploys.
BASE_URL = "https://voymark.app/"

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
{social}
  <link rel="canonical" href="{canonical}">
{hreflangs}
  <link rel="preload" href="{root}assets/fonts/Marcellus-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}assets/fonts/IBMPlexMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}assets/style.css">
  <link rel="icon" type="image/svg+xml" href="{root}assets/img/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
{jsonld}
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
    <p class="trustrow"><span>{trust1}</span><span>{trust2}</span><span>{trust3}</span></p>
    <div class="cta">
      <a class="badge badge-disabled" href="#" aria-disabled="true">
        <span class="badge-small">{badge_small}</span>
        <span class="badge-large">App&nbsp;Store</span>
      </a>
      <!-- Placeholder: swap href for the Play Store listing at launch. -->
      <a class="badge badge-disabled" href="#" aria-disabled="true">
        <span class="badge-small">{badge_small_android}</span>
        <span class="badge-large">Google&nbsp;Play</span>
      </a>
    </div>
    <p class="mrz" aria-hidden="true">P&lt;VOYM&lt;&lt;EVERY&lt;JOURNEY&lt;LEAVES&lt;A&lt;MARK&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;<br>197COUNTRIES7CONT&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;2026&lt;4</p>
  </header>

  <main>
    <section class="band">
      <h2>{s1_h}</h2>
      <div class="grid grid-3">
        <article><h3>{atlas_h}</h3><p>{atlas_p}</p></article>
        <article><h3>{paper_h}</h3><p>{paper_p}</p></article>
        <article><h3>{modern_h}</h3><p>{modern_p}</p></article>
        <article><h3>{layers_h}</h3><p>{layers_p}</p></article>
        <article><h3>{cities_h}</h3><p>{cities_p}</p></article>
              <article><h3>{regions_h}</h3><p>{regions_p}</p></article>
      </div>
    </section>

    <section class="band band-shots">
      <h2>{shots_title}</h2>
      <div class="shots">
{shots_html}
      </div>
    </section>

    <section class="band band-alt">
      <h2>{s2_h}</h2>
      <div class="grid">
        <article><h3>{photos_h}</h3><p>{photos_p}</p></article>
        <article><h3>{hand_h}</h3><p>{hand_p}</p></article>
        <article><h3>{rules_h}</h3><p>{rules_p}</p></article>
        <article><h3>{story_h}</h3><p>{story_p}</p></article>
        <article><h3>{collections_h}</h3><p>{collections_p}</p></article>
        <article><h3>{journal_h}</h3><p>{journal_p}</p></article>
      </div>
    </section>

    <section class="band">
      <h2>{s6_h}</h2>
      <div class="grid">
        <article><h3>{seals_h}</h3><p>{seals_p}</p></article>
        <article><h3>{timemachine_h}</h3><p>{timemachine_p}</p></article>
        <article><h3>{widgets_h}</h3><p>{widgets_p}</p></article>
        <article><h3>{icloud_h}</h3><p>{icloud_p}</p></article>
      </div>
    </section>

    <section class="band band-alt">
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
        <li><strong>{p5s}</strong> {p5}</li>
      </ul>
    </section>

    <section class="band band-alt">
      <h2>{s5_h}</h2>
      <p class="wide langs">English · Français · Español · Italiano · Deutsch · Română</p>
    </section>
  </main>

  <footer>
    <p class="tagline">{tagline}</p>
    <nav class="footnav" aria-label="Site">
{footnav}
    </nav>
    <p>© <span id="year">2026</span> Outside Software SRL. {credits}</p>
  </footer>

  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

LANG_LABELS = {"en": "EN", "fr": "FR", "es": "ES", "it": "IT", "de": "DE", "ro": "RO"}

# Open Graph needs a full locale, not a language code.
OG_LOCALE = {"en": "en_US", "fr": "fr_FR", "es": "es_ES",
             "it": "it_IT", "de": "de_DE", "ro": "ro_RO"}

OG_IMAGE = BASE_URL + "assets/img/voymark-og.png"

OG_ALT = {
 "en": "Voymark — a world passport for your travels. Offline, no account, free.",
 "fr": "Voymark — un passeport du monde pour vos voyages. Hors ligne, sans compte, gratuit.",
 "es": "Voymark — un pasaporte del mundo para tus viajes. Offline, sin cuenta, gratis.",
 "it": "Voymark — un passaporto del mondo per i tuoi viaggi. Offline, senza account, gratis.",
 "de": "Voymark — ein Weltpass für deine Reisen. Offline, ohne Konto, kostenlos.",
 "ro": "Voymark — un pașaport al lumii pentru călătoriile tale. Offline, fără cont, gratuit.",
}


def social_block(lang, url, title, description):
    """og:image and the Twitter card, shared by both templates.

    Without og:image every share of the site — X, Slack, WhatsApp,
    LinkedIn, Discord — rendered as a bare text link (SEO audit,
    2026-07-31). One card serves all 48 pages: the site is small enough
    that a per-page image would be six translations of the same claim.
    """
    others = "\n".join(
        f'  <meta property="og:locale:alternate" content="{OG_LOCALE[l]}">'
        for l in LANGS if l != lang
    )
    return f'''  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Voymark">
  <meta property="og:locale" content="{OG_LOCALE[lang]}">
{others}
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{OG_ALT[lang]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="twitter:image:alt" content="{OG_ALT[lang]}">'''


# ---------------------------------------------------------------------------
# Structured data
#
# Search engines and answer engines read JSON-LD to decide what this site
# *is*; without it Voymark was an unlabelled document to both (SEO/GEO
# audit, 2026-07-31). Three rules hold here:
#
# 1. Only claims the app can back. `price: "0"` is true — there is no
#    subscription and no paid tier. There is no `aggregateRating`, because
#    there are no reviews; inventing one would be a fabricated record.
# 2. `applicationCategory` and `operatingSystem` name both platforms,
#    since both ship.
# 3. The graph is the same on every language; only @id/url/inLanguage move.
#    One Organization and one WebSite node, referenced by @id from the
#    per-page nodes, so the six locales describe one entity rather than six.
# ---------------------------------------------------------------------------

ORG_ID = BASE_URL + "#organization"
SITE_ID = BASE_URL + "#website"
APP_ID = BASE_URL + "#app"

APP_DESCRIPTION = {
 "en": "A world passport for your travels: mark the countries you have visited, turn geotagged photos into trips, and keep the whole record on your device. Free, offline, no account.",
 "fr": "Un passeport du monde pour vos voyages : marquez les pays visités, transformez vos photos géolocalisées en voyages et gardez tout sur votre appareil. Gratuit, hors ligne, sans compte.",
 "es": "Un pasaporte del mundo para tus viajes: marca los países visitados, convierte tus fotos geolocalizadas en viajes y guarda todo en tu dispositivo. Gratis, offline, sin cuenta.",
 "it": "Un passaporto del mondo per i tuoi viaggi: segna i paesi visitati, trasforma le foto geolocalizzate in viaggi e tieni tutto sul tuo dispositivo. Gratis, offline, senza account.",
 "de": "Ein Weltpass für deine Reisen: markiere besuchte Länder, mach aus Fotos mit GPS-Daten fertige Reisen und behalte alles auf deinem Gerät. Kostenlos, offline, ohne Konto.",
 "ro": "Un pașaport al lumii pentru călătoriile tale: marchează țările vizitate, transformă pozele cu locație în călătorii și păstrează totul pe dispozitiv. Gratuit, offline, fără cont.",
}

# Every line here must be a feature both platforms ship. Checked against
# the app repo's docs/FEATURES.md — the site's standing rule.
FEATURE_LIST = {
 "en": ["Visited-countries world map", "Passport with stamps and seals",
        "Geotagged photos turned into trips", "Cities and regions",
        "Travel journal and companions", "Time machine by year",
        "PDF travel book and share cards", "Works offline, no account",
        "Export to GPX, KML, GeoJSON, CSV and plain text"],
 "fr": ["Carte du monde des pays visités", "Passeport avec tampons et sceaux",
        "Photos géolocalisées transformées en voyages", "Villes et régions",
        "Journal de voyage et compagnons", "Machine à remonter le temps par année",
        "Livre de voyage PDF et cartes à partager", "Fonctionne hors ligne, sans compte",
        "Export GPX, KML, GeoJSON, CSV et texte brut"],
 "es": ["Mapa mundial de países visitados", "Pasaporte con sellos y medallas",
        "Fotos geolocalizadas convertidas en viajes", "Ciudades y regiones",
        "Diario de viaje y acompañantes", "Máquina del tiempo por año",
        "Libro de viaje en PDF y tarjetas para compartir", "Funciona offline, sin cuenta",
        "Exportación a GPX, KML, GeoJSON, CSV y texto plano"],
 "it": ["Mappa del mondo dei paesi visitati", "Passaporto con timbri e sigilli",
        "Foto geolocalizzate trasformate in viaggi", "Città e regioni",
        "Diario di viaggio e compagni", "Macchina del tempo per anno",
        "Libro di viaggio PDF e card da condividere", "Funziona offline, senza account",
        "Esportazione in GPX, KML, GeoJSON, CSV e testo semplice"],
 "de": ["Weltkarte der besuchten Länder", "Reisepass mit Stempeln und Siegeln",
        "Fotos mit GPS-Daten werden zu Reisen", "Städte und Regionen",
        "Reisetagebuch und Begleiter", "Zeitmaschine nach Jahr",
        "PDF-Reisebuch und Sharing-Karten", "Funktioniert offline, ohne Konto",
        "Export als GPX, KML, GeoJSON, CSV und Klartext"],
 "ro": ["Harta lumii cu țările vizitate", "Pașaport cu ștampile și sigilii",
        "Poze cu locație transformate în călătorii", "Orașe și regiuni",
        "Jurnal de călătorie și însoțitori", "Mașina timpului, an cu an",
        "Carte de călătorie PDF și cărți de partajat", "Funcționează offline, fără cont",
        "Export în GPX, KML, GeoJSON, CSV și text simplu"],
}


def _shared_nodes(lang):
    """Organization, WebSite and SoftwareApplication — one set, every page."""
    return [
        {
            "@type": "Organization",
            "@id": ORG_ID,
            "name": "Outside Software SRL",
            "url": BASE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": BASE_URL + "assets/img/voymark-avatar-seal-1024.png",
                "width": 1024,
                "height": 1024,
            },
        },
        {
            "@type": "WebSite",
            "@id": SITE_ID,
            "name": "Voymark",
            "url": BASE_URL,
            "inLanguage": LANGS,
            "publisher": {"@id": ORG_ID},
        },
        {
            "@type": "SoftwareApplication",
            "@id": APP_ID,
            "name": "Voymark",
            "alternateName": "Voymark — World Passport",
            "applicationCategory": "TravelApplication",
            "applicationSubCategory": "Travel tracker",
            "operatingSystem": "iOS 17+, Android 8+",
            "description": APP_DESCRIPTION[lang],
            "inLanguage": LANGS,
            "isAccessibleForFree": True,
            "image": OG_IMAGE,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "EUR",
                "availability": "https://schema.org/InStock",
            },
            "featureList": FEATURE_LIST[lang],
            "publisher": {"@id": ORG_ID},
        },
    ]


def plain(markup):
    """Copy written for HTML, as a search engine's Answer field wants it.

    The visible answer carries entities and the odd link; the JSON-LD field
    is plain text, so "&amp;" there would be read literally as those five
    characters. Structured data has to say the same thing the page says.
    """
    return html.unescape(re.sub(r"<[^>]+>", "", markup))


def _script(graph):
    body = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)
    body = "\n".join("  " + line for line in body.splitlines())
    return f'  <script type="application/ld+json">\n{body}\n  </script>'


def jsonld_home(lang):
    url = url_for(lang)
    graph = _shared_nodes(lang) + [{
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": T["title"][lang],
        "description": T["meta"][lang],
        "inLanguage": lang,
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": APP_ID},
    }]
    return _script(graph)


def jsonld_page(slug, lang, faq=None):
    url = page_url(slug, lang)
    home = url_for(lang)
    page = PAGES[slug]
    graph = _shared_nodes(lang) + [
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": page["title"][lang],
            "description": page["meta"][lang],
            "inLanguage": lang,
            "isPartOf": {"@id": SITE_ID},
            "about": {"@id": APP_ID},
        },
        {
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumbs",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Voymark", "item": home},
                {"@type": "ListItem", "position": 2, "name": page["nav"][lang], "item": url},
            ],
        },
    ]
    if faq:
        graph.append({
            "@type": "FAQPage",
            "@id": url + "#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": plain(q["q"][lang]),
                    "acceptedAnswer": {"@type": "Answer", "text": plain(q["a"][lang])},
                }
                for q in faq
            ],
        })
    return _script(graph)


# ---------------------------------------------------------------------------
# Subpages: legal + keyword landing pages. Slugs stay English everywhere
# (stable URLs); every page carries its own title/meta/h1/lede/sections.
# Keyword strategy lives in docs/KEYWORDS.md.
# ---------------------------------------------------------------------------

PAGES = {

"privacy": {
 "nav": {"en":"Privacy","fr":"Confidentialité","es":"Privacidad","it":"Privacy","de":"Datenschutz","ro":"Confidențialitate"},
 "title": {
  "en":"Privacy Policy — Voymark","fr":"Politique de confidentialité — Voymark","es":"Política de privacidad — Voymark",
  "it":"Informativa sulla privacy — Voymark","de":"Datenschutzerklärung — Voymark","ro":"Politica de confidențialitate — Voymark"},
 "meta": {
  "en":"Voymark collects no personal data. Everything you record stays on your device: no accounts, no analytics, no tracking, no ads, no servers.",
  "fr":"Voymark ne collecte aucune donnée personnelle. Tout ce que vous enregistrez reste sur votre appareil : pas de compte, pas d'analytique, pas de suivi, pas de pub, pas de serveurs.",
  "es":"Voymark no recopila datos personales. Todo lo que registras permanece en tu dispositivo: sin cuentas, sin analítica, sin rastreo, sin anuncios, sin servidores.",
  "it":"Voymark non raccoglie dati personali. Tutto ciò che registri resta sul tuo dispositivo: niente account, niente analisi, niente tracciamento, niente pubblicità, niente server.",
  "de":"Voymark sammelt keine personenbezogenen Daten. Alles, was du erfasst, bleibt auf deinem Gerät: keine Konten, keine Analyse, kein Tracking, keine Werbung, keine Server.",
  "ro":"Voymark nu colectează date personale. Tot ce înregistrezi rămâne pe dispozitivul tău: fără conturi, fără analitice, fără urmărire, fără reclame, fără servere."},
 "h1": {
  "en":"Privacy Policy","fr":"Politique de confidentialité","es":"Política de privacidad",
  "it":"Informativa sulla privacy","de":"Datenschutzerklärung","ro":"Politica de confidențialitate"},
 "lede": {
  "en":"Last updated: 27 July 2026. The short version: Voymark collects no personal data, and your travel history never leaves your device unless you export or share it yourself.",
  "fr":"Dernière mise à jour : 27 juillet 2026. En bref : Voymark ne collecte aucune donnée personnelle, et votre historique de voyage ne quitte jamais votre appareil, sauf si vous l'exportez ou le partagez vous-même.",
  "es":"Última actualización: 27 de julio de 2026. En resumen: Voymark no recopila datos personales y tu historial de viajes nunca sale de tu dispositivo salvo que tú mismo lo exportes o compartas.",
  "it":"Ultimo aggiornamento: 27 luglio 2026. In breve: Voymark non raccoglie dati personali e la tua storia di viaggio non lascia mai il tuo dispositivo, a meno che non la esporti o condivida tu stesso.",
  "de":"Zuletzt aktualisiert: 27. Juli 2026. Kurz gesagt: Voymark sammelt keine personenbezogenen Daten, und deine Reisegeschichte verlässt dein Gerät nie — außer du exportierst oder teilst sie selbst.",
  "ro":"Ultima actualizare: 27 iulie 2026. Pe scurt: Voymark nu colectează date personale, iar istoria ta de călătorie nu îți părăsește niciodată dispozitivul decât dacă o exporți sau o partajezi tu însuți."},
 "sections": [
  {"h":{"en":"Who we are","fr":"Qui nous sommes","es":"Quiénes somos","it":"Chi siamo","de":"Wer wir sind","ro":"Cine suntem"},
   "p":{"en":"Voymark is published by Outside Software SRL, a company registered in Romania. For this policy, we are the data controller — though, as you'll see below, we hold no data about you.",
        "fr":"Voymark est édité par Outside Software SRL, société immatriculée en Roumanie. Au sens de cette politique, nous sommes le responsable du traitement — même si, comme vous le verrez, nous ne détenons aucune donnée vous concernant.",
        "es":"Voymark es publicado por Outside Software SRL, sociedad registrada en Rumanía. A efectos de esta política somos el responsable del tratamiento — aunque, como verás, no guardamos ningún dato tuyo.",
        "it":"Voymark è pubblicato da Outside Software SRL, società registrata in Romania. Ai fini di questa informativa siamo il titolare del trattamento — anche se, come vedrai, non deteniamo alcun tuo dato.",
        "de":"Voymark wird von Outside Software SRL herausgegeben, einer in Rumänien eingetragenen Gesellschaft. Im Sinne dieser Erklärung sind wir der Verantwortliche — auch wenn wir, wie du gleich siehst, keine Daten über dich besitzen.",
        "ro":"Voymark este publicat de Outside Software SRL, societate înregistrată în România. În sensul acestei politici suntem operatorul de date — deși, după cum vei vedea, nu deținem nicio dată despre tine."}},
  {"h":{"en":"What we don't do","fr":"Ce que nous ne faisons pas","es":"Lo que no hacemos","it":"Cosa non facciamo","de":"Was wir nicht tun","ro":"Ce nu facem"},
   "p":{"en":"No accounts. No analytics. No tracking. No advertising. No crash reporters. Voymark runs no servers of its own, so there is nowhere for your data to be sent.",
        "fr":"Pas de comptes. Pas d'analytique. Pas de suivi. Pas de publicité. Pas de rapporteurs de plantage. Voymark n'exploite aucun serveur, il n'y a donc nulle part où envoyer vos données.",
        "es":"Sin cuentas. Sin analítica. Sin rastreo. Sin publicidad. Sin informes de fallos. Voymark no opera servidores propios, así que no hay ningún lugar al que enviar tus datos.",
        "it":"Niente account. Niente analisi. Niente tracciamento. Niente pubblicità. Niente crash reporter. Voymark non gestisce server propri, quindi non esiste un posto dove inviare i tuoi dati.",
        "de":"Keine Konten. Keine Analyse. Kein Tracking. Keine Werbung. Keine Crash-Reporter. Voymark betreibt keine eigenen Server — es gibt schlicht keinen Ort, an den deine Daten gesendet werden könnten.",
        "ro":"Fără conturi. Fără analitice. Fără urmărire. Fără reclame. Fără raportoare de erori. Voymark nu operează servere proprii, deci nu există niciun loc unde datele tale să fie trimise."}},
  {"h":{"en":"Your photos","fr":"Vos photos","es":"Tus fotos","it":"Le tue foto","de":"Deine Fotos","ro":"Pozele tale"},
   "p":{"en":"If you grant photo access, Voymark reads locations and dates from your photo library entirely on your device to reconstruct trips. Images are never copied, uploaded or analyzed anywhere else, and you can revoke access at any time in system settings. To name your destinations, place coordinates (never the images themselves) are looked up with the device's built-in geocoding service — operated by Apple on iPhone and by Google on Android.",
        "fr":"Si vous accordez l'accès aux photos, Voymark lit les lieux et les dates de votre photothèque entièrement sur votre appareil pour reconstruire vos voyages. Les images ne sont jamais copiées, envoyées ni analysées ailleurs, et vous pouvez révoquer l'accès à tout moment dans les réglages du système. Pour nommer vos destinations, les coordonnées des lieux (jamais les images elles-mêmes) sont résolues via le service de géocodage intégré de l'appareil — opéré par Apple sur iPhone et par Google sur Android.",
        "es":"Si concedes acceso a las fotos, Voymark lee ubicaciones y fechas de tu biblioteca por completo en tu dispositivo para reconstruir viajes. Las imágenes nunca se copian, se suben ni se analizan en otro lugar, y puedes revocar el acceso cuando quieras en los ajustes del sistema. Para nombrar tus destinos, las coordenadas de los lugares (nunca las imágenes) se consultan con el servicio de geocodificación integrado del dispositivo — operado por Apple en iPhone y por Google en Android.",
        "it":"Se concedi l'accesso alle foto, Voymark legge luoghi e date dalla tua libreria interamente sul tuo dispositivo per ricostruire i viaggi. Le immagini non vengono mai copiate, caricate o analizzate altrove, e puoi revocare l'accesso in qualsiasi momento nelle impostazioni di sistema. Per dare un nome alle tue destinazioni, le coordinate dei luoghi (mai le immagini) vengono risolte con il servizio di geocodifica integrato del dispositivo — gestito da Apple su iPhone e da Google su Android.",
        "de":"Wenn du Fotozugriff gewährst, liest Voymark Orte und Daten aus deiner Fotobibliothek vollständig auf deinem Gerät, um Reisen zu rekonstruieren. Bilder werden nie kopiert, hochgeladen oder anderswo analysiert, und du kannst den Zugriff jederzeit in den Systemeinstellungen widerrufen. Um deine Ziele zu benennen, werden Ortskoordinaten (nie die Bilder selbst) über den eingebauten Geocoding-Dienst des Geräts aufgelöst — betrieben von Apple auf dem iPhone und von Google auf Android.",
        "ro":"Dacă acorzi acces la poze, Voymark citește locațiile și datele din biblioteca ta în întregime pe dispozitivul tău pentru a reconstrui călătoriile. Imaginile nu sunt niciodată copiate, încărcate sau analizate altundeva, iar accesul poate fi revocat oricând din setările sistemului. Pentru a-ți numi destinațiile, coordonatele locurilor (niciodată imaginile în sine) sunt căutate prin serviciul de geocodare încorporat al dispozitivului — operat de Apple pe iPhone și de Google pe Android."}},
  {"h":{"en":"Your data, your files","fr":"Vos données, vos fichiers","es":"Tus datos, tus archivos","it":"I tuoi dati, i tuoi file","de":"Deine Daten, deine Dateien","ro":"Datele tale, fișierele tale"},
   "p":{"en":"Countries, trips, places, notes and settings are stored locally on your device. Backups and exports (CSV, GPX, KML, GeoJSON, PDF, passport files) are files you create, keep and delete yourself. Uninstalling the app deletes its local data.",
        "fr":"Pays, voyages, lieux, notes et réglages sont stockés localement sur votre appareil. Les sauvegardes et exports (CSV, GPX, KML, GeoJSON, PDF, fichiers passeport) sont des fichiers que vous créez, conservez et supprimez vous-même. Désinstaller l'app supprime ses données locales.",
        "es":"Países, viajes, lugares, notas y ajustes se guardan localmente en tu dispositivo. Las copias y exportaciones (CSV, GPX, KML, GeoJSON, PDF, archivos de pasaporte) son archivos que tú creas, guardas y borras. Desinstalar la app elimina sus datos locales.",
        "it":"Paesi, viaggi, luoghi, note e impostazioni sono salvati localmente sul tuo dispositivo. Backup ed esportazioni (CSV, GPX, KML, GeoJSON, PDF, file passaporto) sono file che crei, conservi ed elimini tu. Disinstallare l'app cancella i suoi dati locali.",
        "de":"Länder, Reisen, Orte, Notizen und Einstellungen werden lokal auf deinem Gerät gespeichert. Backups und Exporte (CSV, GPX, KML, GeoJSON, PDF, Passdateien) sind Dateien, die du selbst erstellst, aufbewahrst und löschst. Beim Deinstallieren der App werden ihre lokalen Daten gelöscht.",
        "ro":"Țările, călătoriile, locurile, notițele și setările sunt stocate local pe dispozitivul tău. Copiile de siguranță și exporturile (CSV, GPX, KML, GeoJSON, PDF, fișiere pașaport) sunt fișiere pe care le creezi, păstrezi și ștergi tu. Dezinstalarea aplicației îi șterge datele locale."}},
  {"h":{"en":"Sharing features","fr":"Fonctions de partage","es":"Funciones para compartir","it":"Funzioni di condivisione","de":"Teilen-Funktionen","ro":"Funcțiile de partajare"},
   "p":{"en":"Compare codes, share cards, travel books and exports leave your device only when you choose to share them, through your system's share sheet, to the destination you pick. Passport-compare payloads contain only country stamps and a display name — never trips, places, photos or dates.",
        "fr":"Codes de comparaison, cartes à partager, livres de voyage et exports ne quittent votre appareil que lorsque vous choisissez de les partager, via la feuille de partage du système, vers la destination de votre choix. Les données de comparaison ne contiennent que les tampons de pays et un nom d'affichage — jamais les voyages, lieux, photos ou dates.",
        "es":"Códigos de comparación, tarjetas, libros de viaje y exportaciones solo salen de tu dispositivo cuando decides compartirlos, a través de la hoja de compartir del sistema y hacia el destino que elijas. Los datos de comparación contienen solo sellos de países y un nombre — nunca viajes, lugares, fotos o fechas.",
        "it":"Codici di confronto, card, libri di viaggio ed esportazioni lasciano il tuo dispositivo solo quando scegli di condividerli, tramite il foglio di condivisione del sistema, verso la destinazione che scegli. I dati di confronto contengono solo timbri dei paesi e un nome — mai viaggi, luoghi, foto o date.",
        "de":"Vergleichscodes, Share-Karten, Reisebücher und Exporte verlassen dein Gerät nur, wenn du sie über das System-Share-Sheet an ein Ziel deiner Wahl teilst. Vergleichsdaten enthalten nur Länderstempel und einen Anzeigenamen — nie Reisen, Orte, Fotos oder Daten.",
        "ro":"Codurile de comparare, cardurile, cărțile de călătorie și exporturile îți părăsesc dispozitivul doar când alegi tu să le partajezi, prin foaia de partajare a sistemului, către destinația aleasă de tine. Datele de comparare conțin doar ștampile de țări și un nume — niciodată călătorii, locuri, poze sau date."}},
  {"h":{"en":"App stores and this website","fr":"Boutiques d'applications et ce site","es":"Tiendas de aplicaciones y este sitio","it":"Store delle app e questo sito","de":"App-Stores und diese Website","ro":"Magazinele de aplicații și acest site"},
   "p":{"en":"Downloading Voymark through the App Store or Google Play is governed by Apple's and Google's own privacy policies. This website is a static site hosted on GitHub Pages; GitHub may log standard technical requests. The site sets no cookies and runs no analytics; fonts are loaded from Google Fonts, which involves a standard font request to Google. On iPhone, the optional Modern and Satellite map styles load map tiles through Apple Maps; those requests go to Apple under Apple's privacy policy. The Atlas and Paper maps are fully offline on both platforms. On Android, place search sends the text you type to OpenStreetMap's free Nominatim service, which finds places the built-in city list and the device geocoder don't cover; only that text is sent, governed by the OpenStreetMap Foundation's privacy policy.",
        "fr":"Le téléchargement de Voymark via l'App Store ou Google Play est régi par les politiques de confidentialité d'Apple et de Google. Ce site est un site statique hébergé sur GitHub Pages ; GitHub peut journaliser des requêtes techniques standard. Le site ne pose aucun cookie et n'utilise aucune analytique ; les polices sont chargées depuis Google Fonts, ce qui implique une requête standard vers Google. Sur iPhone, les styles de carte optionnels Moderne et Satellite chargent des tuiles via Apple Plans ; ces requêtes vont à Apple selon la politique de confidentialité d'Apple. Les cartes Atlas et Papier sont entièrement hors ligne sur les deux plateformes. Sur Android, la recherche de lieux envoie le texte saisi au service gratuit Nominatim d'OpenStreetMap, qui trouve les lieux absents de la liste de villes intégrée et du géocodeur de l'appareil ; seul ce texte est envoyé, selon la politique de confidentialité de la Fondation OpenStreetMap.",
        "es":"La descarga de Voymark desde el App Store o Google Play se rige por las políticas de privacidad de Apple y Google. Este sitio es estático y está alojado en GitHub Pages; GitHub puede registrar solicitudes técnicas estándar. El sitio no usa cookies ni analítica; las fuentes se cargan desde Google Fonts, lo que implica una solicitud estándar a Google. En iPhone, los estilos de mapa opcionales Moderno y Satélite cargan mosaicos a través de Apple Maps; esas solicitudes van a Apple según la política de privacidad de Apple. Los mapas Atlas y de Papel son totalmente offline en ambas plataformas. En Android, la búsqueda de lugares envía el texto que escribes al servicio gratuito Nominatim de OpenStreetMap, que encuentra lugares que la lista de ciudades integrada y el geocodificador del dispositivo no cubren; solo se envía ese texto, según la política de privacidad de la Fundación OpenStreetMap.",
        "it":"Il download di Voymark tramite App Store o Google Play è regolato dalle politiche sulla privacy di Apple e Google. Questo sito è statico e ospitato su GitHub Pages; GitHub può registrare richieste tecniche standard. Il sito non imposta cookie e non usa analisi; i caratteri sono caricati da Google Fonts, con una richiesta standard a Google. Su iPhone, gli stili di mappa opzionali Moderna e Satellite caricano tile tramite Mappe Apple; quelle richieste vanno ad Apple secondo la politica sulla privacy di Apple. Le mappe Atlante e di Carta sono completamente offline su entrambe le piattaforme. Su Android, la ricerca dei luoghi invia il testo digitato al servizio gratuito Nominatim di OpenStreetMap, che trova luoghi non coperti dall'elenco città integrato e dal geocodificatore del dispositivo; viene inviato solo quel testo, secondo l'informativa sulla privacy della OpenStreetMap Foundation.",
        "de":"Der Download von Voymark über den App Store oder Google Play unterliegt den Datenschutzrichtlinien von Apple bzw. Google. Diese Website ist statisch und wird auf GitHub Pages gehostet; GitHub kann technische Standard-Anfragen protokollieren. Die Seite setzt keine Cookies und nutzt keine Analyse; Schriften werden von Google Fonts geladen, was eine Standard-Anfrage an Google bedeutet. Auf dem iPhone laden die optionalen Kartenstile Modern und Satellit Kartenkacheln über Apple Karten; diese Anfragen gehen gemäß Apples Datenschutzrichtlinie an Apple. Atlas- und Papierkarte sind auf beiden Plattformen vollständig offline. Unter Android sendet die Ortssuche den eingegebenen Text an den kostenlosen Nominatim-Dienst von OpenStreetMap, der Orte findet, die die integrierte Städteliste und der Geocoder des Geräts nicht abdecken; gesendet wird nur dieser Text, gemäß der Datenschutzerklärung der OpenStreetMap Foundation.",
        "ro":"Descărcarea Voymark prin App Store sau Google Play este guvernată de politicile de confidențialitate ale Apple și Google. Acest site este static și găzduit pe GitHub Pages; GitHub poate înregistra cereri tehnice standard. Site-ul nu setează cookie-uri și nu folosește analitice; fonturile sunt încărcate de la Google Fonts, ceea ce presupune o cerere standard către Google. Pe iPhone, stilurile opționale de hartă Modern și Satelit încarcă dale prin Apple Maps; acele cereri merg la Apple conform politicii de confidențialitate Apple. Hărțile Atlas și de Hârtie sunt complet offline pe ambele platforme. Pe Android, căutarea de locuri trimite textul introdus către serviciul gratuit Nominatim de la OpenStreetMap, care găsește locuri neacoperite de lista de orașe integrată și de geocoderul dispozitivului; se trimite doar acel text, conform politicii de confidențialitate a Fundației OpenStreetMap."}},
  {"h":{"en":"Your rights","fr":"Vos droits","es":"Tus derechos","it":"I tuoi diritti","de":"Deine Rechte","ro":"Drepturile tale"},
   "p":{"en":"Under the GDPR you have rights of access, rectification, erasure and portability. Because Voymark holds no data about you, these rights are exercised directly on your own device: your data is already in your hands, and the export tools give you portability in open formats.",
        "fr":"Au titre du RGPD, vous disposez de droits d'accès, de rectification, d'effacement et de portabilité. Comme Voymark ne détient aucune donnée vous concernant, ces droits s'exercent directement sur votre appareil : vos données sont déjà entre vos mains, et les outils d'export assurent la portabilité en formats ouverts.",
        "es":"Según el RGPD tienes derechos de acceso, rectificación, supresión y portabilidad. Como Voymark no guarda datos sobre ti, estos derechos se ejercen directamente en tu dispositivo: tus datos ya están en tus manos y las herramientas de exportación te dan portabilidad en formatos abiertos.",
        "it":"Ai sensi del GDPR hai diritti di accesso, rettifica, cancellazione e portabilità. Poiché Voymark non detiene dati su di te, questi diritti si esercitano direttamente sul tuo dispositivo: i tuoi dati sono già nelle tue mani e gli strumenti di esportazione garantiscono la portabilità in formati aperti.",
        "de":"Nach der DSGVO hast du Rechte auf Auskunft, Berichtigung, Löschung und Übertragbarkeit. Da Voymark keine Daten über dich besitzt, übst du diese Rechte direkt auf deinem Gerät aus: Deine Daten sind bereits in deiner Hand, und die Export-Werkzeuge geben dir Portabilität in offenen Formaten.",
        "ro":"Conform GDPR ai drepturi de acces, rectificare, ștergere și portabilitate. Pentru că Voymark nu deține date despre tine, aceste drepturi se exercită direct pe dispozitivul tău: datele tale sunt deja în mâinile tale, iar instrumentele de export îți oferă portabilitate în formate deschise."}},
  {"h":{"en":"Changes and contact","fr":"Modifications et contact","es":"Cambios y contacto","it":"Modifiche e contatti","de":"Änderungen und Kontakt","ro":"Modificări și contact"},
   "p":{"en":"If this policy changes in a way that matters, we'll say so here with a new date at the top. Questions: contact Outside Software SRL at hello@voymark.app.",
        "fr":"Si cette politique change de manière significative, nous l'indiquerons ici avec une nouvelle date en haut de page. Questions : contactez Outside Software SRL à hello@voymark.app.",
        "es":"Si esta política cambia de forma relevante, lo indicaremos aquí con una nueva fecha arriba. Preguntas: contacta con Outside Software SRL en hello@voymark.app.",
        "it":"Se questa informativa cambierà in modo rilevante, lo indicheremo qui con una nuova data in alto. Domande: contatta Outside Software SRL a hello@voymark.app.",
        "de":"Ändert sich diese Erklärung wesentlich, steht es hier mit neuem Datum oben. Fragen: Outside Software SRL unter hello@voymark.app.",
        "ro":"Dacă această politică se schimbă în mod semnificativ, vom nota aici cu o dată nouă sus. Întrebări: contactează Outside Software SRL la hello@voymark.app."}},
 ],
},

"terms": {
 "nav": {"en":"Terms","fr":"Conditions","es":"Términos","it":"Termini","de":"Nutzungsbedingungen","ro":"Termeni"},
 "title": {
  "en":"Terms of Use — Voymark","fr":"Conditions d'utilisation — Voymark","es":"Términos de uso — Voymark",
  "it":"Termini di utilizzo — Voymark","de":"Nutzungsbedingungen — Voymark","ro":"Termeni de utilizare — Voymark"},
 "meta": {
  "en":"The terms of use for the Voymark travel passport app, published by Outside Software SRL.",
  "fr":"Les conditions d'utilisation de l'app passeport de voyage Voymark, éditée par Outside Software SRL.",
  "es":"Los términos de uso de la app de pasaporte de viajes Voymark, publicada por Outside Software SRL.",
  "it":"I termini di utilizzo dell'app passaporto di viaggio Voymark, pubblicata da Outside Software SRL.",
  "de":"Die Nutzungsbedingungen der Reisepass-App Voymark, herausgegeben von Outside Software SRL.",
  "ro":"Termenii de utilizare ai aplicației-pașaport de călătorie Voymark, publicată de Outside Software SRL."},
 "h1": {
  "en":"Terms of Use","fr":"Conditions d'utilisation","es":"Términos de uso",
  "it":"Termini di utilizzo","de":"Nutzungsbedingungen","ro":"Termeni de utilizare"},
 "lede": {
  "en":"Last updated: 27 July 2026. By downloading or using Voymark you agree to these terms. If you don't agree, please don't use the app.",
  "fr":"Dernière mise à jour : 27 juillet 2026. En téléchargeant ou en utilisant Voymark, vous acceptez ces conditions. Si vous n'êtes pas d'accord, veuillez ne pas utiliser l'app.",
  "es":"Última actualización: 27 de julio de 2026. Al descargar o usar Voymark aceptas estos términos. Si no estás de acuerdo, por favor no uses la app.",
  "it":"Ultimo aggiornamento: 27 luglio 2026. Scaricando o usando Voymark accetti questi termini. Se non sei d'accordo, ti preghiamo di non usare l'app.",
  "de":"Zuletzt aktualisiert: 27. Juli 2026. Mit dem Herunterladen oder Nutzen von Voymark stimmst du diesen Bedingungen zu. Wenn nicht, nutze die App bitte nicht.",
  "ro":"Ultima actualizare: 27 iulie 2026. Prin descărcarea sau folosirea Voymark accepți acești termeni. Dacă nu ești de acord, te rugăm să nu folosești aplicația."},
 "sections": [
  {"h":{"en":"The publisher","fr":"L'éditeur","es":"El editor","it":"L'editore","de":"Der Herausgeber","ro":"Editorul"},
   "p":{"en":"Voymark is published by Outside Software SRL, a company registered in Romania (\"we\"). These terms are governed by Romanian law; mandatory consumer protections of your country of residence remain unaffected.",
        "fr":"Voymark est édité par Outside Software SRL, société immatriculée en Roumanie (« nous »). Ces conditions sont régies par le droit roumain ; les protections impératives des consommateurs de votre pays de résidence restent applicables.",
        "es":"Voymark es publicado por Outside Software SRL, sociedad registrada en Rumanía (\"nosotros\"). Estos términos se rigen por el derecho rumano; las protecciones imperativas del consumidor de tu país de residencia no se ven afectadas.",
        "it":"Voymark è pubblicato da Outside Software SRL, società registrata in Romania (\"noi\"). Questi termini sono regolati dal diritto rumeno; restano ferme le tutele inderogabili dei consumatori del tuo paese di residenza.",
        "de":"Voymark wird von Outside Software SRL herausgegeben, einer in Rumänien eingetragenen Gesellschaft (\"wir\"). Diese Bedingungen unterliegen rumänischem Recht; zwingender Verbraucherschutz deines Wohnsitzlandes bleibt unberührt.",
        "ro":"Voymark este publicat de Outside Software SRL, societate înregistrată în România (\"noi\"). Acești termeni sunt guvernați de legea română; protecțiile obligatorii ale consumatorului din țara ta de reședință rămân neatinse."}},
  {"h":{"en":"Your license","fr":"Votre licence","es":"Tu licencia","it":"La tua licenza","de":"Deine Lizenz","ro":"Licența ta"},
   "p":{"en":"We grant you a personal, non-exclusive, non-transferable license to use Voymark on devices you own or control, for personal, non-commercial purposes, subject to the terms of the store you downloaded it from (Apple App Store or Google Play).",
        "fr":"Nous vous accordons une licence personnelle, non exclusive et non transférable pour utiliser Voymark sur les appareils que vous possédez ou contrôlez, à des fins personnelles et non commerciales, sous réserve des conditions de la boutique où vous l'avez téléchargée (App Store d'Apple ou Google Play).",
        "es":"Te concedemos una licencia personal, no exclusiva e intransferible para usar Voymark en dispositivos que poseas o controles, con fines personales y no comerciales, sujeta a los términos de la tienda desde la que la descargaste (App Store de Apple o Google Play).",
        "it":"Ti concediamo una licenza personale, non esclusiva e non trasferibile per usare Voymark su dispositivi che possiedi o controlli, per scopi personali e non commerciali, nel rispetto dei termini dello store da cui l'hai scaricata (App Store di Apple o Google Play).",
        "de":"Wir gewähren dir eine persönliche, nicht ausschließliche, nicht übertragbare Lizenz zur Nutzung von Voymark auf Geräten, die du besitzt oder kontrollierst, für persönliche, nicht kommerzielle Zwecke — vorbehaltlich der Bedingungen des Stores, aus dem du sie geladen hast (Apple App Store oder Google Play).",
        "ro":"Îți acordăm o licență personală, neexclusivă și netransferabilă pentru a folosi Voymark pe dispozitive pe care le deții sau controlezi, în scopuri personale, necomerciale, sub rezerva termenilor magazinului din care ai descărcat-o (App Store-ul Apple sau Google Play)."}},
  {"h":{"en":"Your content","fr":"Votre contenu","es":"Tu contenido","it":"I tuoi contenuti","de":"Deine Inhalte","ro":"Conținutul tău"},
   "p":{"en":"Everything you record in Voymark — trips, places, stamps, notes, photo links — is yours and stays on your device. We never receive it and claim no rights over it. You are responsible for keeping your own backups; the app's Import &amp; Export screen exists for exactly that.",
        "fr":"Tout ce que vous enregistrez dans Voymark — voyages, lieux, tampons, notes, liens photo — vous appartient et reste sur votre appareil. Nous ne le recevons jamais et ne revendiquons aucun droit dessus. Vous êtes responsable de vos sauvegardes ; l'écran Import &amp; Export de l'app existe exactement pour cela.",
        "es":"Todo lo que registras en Voymark — viajes, lugares, sellos, notas, enlaces de fotos — es tuyo y permanece en tu dispositivo. Nunca lo recibimos y no reclamamos ningún derecho sobre ello. Eres responsable de tus copias de seguridad; la pantalla Importar y exportar existe exactamente para eso.",
        "it":"Tutto ciò che registri in Voymark — viaggi, luoghi, timbri, note, collegamenti alle foto — è tuo e resta sul tuo dispositivo. Non lo riceviamo mai e non rivendichiamo alcun diritto su di esso. Sei responsabile dei tuoi backup; la schermata Importa ed esporta esiste esattamente per questo.",
        "de":"Alles, was du in Voymark erfasst — Reisen, Orte, Stempel, Notizen, Foto-Verknüpfungen — gehört dir und bleibt auf deinem Gerät. Wir erhalten es nie und beanspruchen keine Rechte daran. Für Backups bist du selbst verantwortlich; genau dafür gibt es den Import-&amp;-Export-Bereich der App.",
        "ro":"Tot ce înregistrezi în Voymark — călătorii, locuri, ștampile, notițe, legături foto — este al tău și rămâne pe dispozitivul tău. Nu îl primim niciodată și nu revendicăm niciun drept asupra lui. Ești responsabil de propriile copii de siguranță; ecranul Import și export există exact pentru asta."}},
  {"h":{"en":"Fair use","fr":"Usage loyal","es":"Uso razonable","it":"Uso corretto","de":"Faire Nutzung","ro":"Utilizare corectă"},
   "p":{"en":"Don't resell, sublicense or redistribute the app, don't try to extract or reuse its bundled datasets outside their licenses (Natural Earth is public domain; UNESCO site data comes from Wikidata, CC0), and don't use the app in ways that break the law.",
        "fr":"Ne revendez pas, ne sous-licenciez pas et ne redistribuez pas l'app, n'essayez pas d'extraire ou de réutiliser ses jeux de données hors de leurs licences (Natural Earth est dans le domaine public ; les sites UNESCO proviennent de Wikidata, CC0), et n'utilisez pas l'app de manière illégale.",
        "es":"No revendas, sublicencies ni redistribuyas la app, no intentes extraer o reutilizar sus conjuntos de datos fuera de sus licencias (Natural Earth es de dominio público; los sitios UNESCO provienen de Wikidata, CC0), y no uses la app de formas contrarias a la ley.",
        "it":"Non rivendere, concedere in sublicenza o ridistribuire l'app, non cercare di estrarre o riutilizzare i suoi dataset al di fuori delle loro licenze (Natural Earth è di pubblico dominio; i siti UNESCO provengono da Wikidata, CC0), e non usare l'app in modi contrari alla legge.",
        "de":"Verkaufe, unterlizenziere oder verbreite die App nicht weiter, versuche nicht, ihre mitgelieferten Datensätze außerhalb ihrer Lizenzen zu extrahieren oder weiterzuverwenden (Natural Earth ist gemeinfrei; UNESCO-Daten stammen von Wikidata, CC0), und nutze die App nicht auf rechtswidrige Weise.",
        "ro":"Nu revinde, sublicenția sau redistribui aplicația, nu încerca să extragi sau să refolosești seturile de date incluse în afara licențelor lor (Natural Earth este domeniu public; siturile UNESCO provin din Wikidata, CC0) și nu folosi aplicația în moduri care încalcă legea."}},
  {"h":{"en":"Free features","fr":"Fonctionnalités gratuites","es":"Funciones gratuitas","it":"Funzioni gratuite","de":"Kostenlose Funktionen","ro":"Funcții gratuite"},
   "p":{"en":"Every Voymark feature is currently free. If paid features ever arrive, they will apply to new capabilities — we won't take away what you already have.",
        "fr":"Toutes les fonctionnalités de Voymark sont actuellement gratuites. Si des fonctions payantes arrivent un jour, elles concerneront de nouvelles capacités — nous ne retirerons pas ce que vous avez déjà.",
        "es":"Todas las funciones de Voymark son actualmente gratuitas. Si algún día llegan funciones de pago, se aplicarán a capacidades nuevas — no te quitaremos lo que ya tienes.",
        "it":"Ogni funzione di Voymark è attualmente gratuita. Se un giorno arriveranno funzioni a pagamento, riguarderanno nuove capacità — non ti toglieremo ciò che hai già.",
        "de":"Jede Voymark-Funktion ist derzeit kostenlos. Sollten je kostenpflichtige Funktionen kommen, betreffen sie neue Fähigkeiten — wir nehmen dir nicht weg, was du schon hast.",
        "ro":"Fiecare funcție Voymark este în prezent gratuită. Dacă vor apărea vreodată funcții plătite, ele vor viza capacități noi — nu îți vom lua ce ai deja."}},
  {"h":{"en":"Honest limits","fr":"Limites honnêtes","es":"Límites honestos","it":"Limiti onesti","de":"Ehrliche Grenzen","ro":"Limite oneste"},
   "p":{"en":"Voymark is provided \"as is\", without warranties of any kind to the extent the law allows. Derived data — detected trips, country attribution, statistics — is a best-effort reconstruction from your own data, not an official record. To the maximum extent permitted by law, our liability is limited to the amount you paid for the app (currently zero); nothing here excludes liability that cannot legally be excluded.",
        "fr":"Voymark est fourni « en l'état », sans garantie d'aucune sorte dans la mesure permise par la loi. Les données dérivées — voyages détectés, attribution des pays, statistiques — sont une reconstruction au mieux à partir de vos propres données, pas un registre officiel. Dans la mesure maximale permise par la loi, notre responsabilité est limitée au montant payé pour l'app (actuellement zéro) ; rien ici n'exclut une responsabilité qui ne peut légalement l'être.",
        "es":"Voymark se ofrece \"tal cual\", sin garantías de ningún tipo en la medida que permita la ley. Los datos derivados — viajes detectados, atribución de países, estadísticas — son una reconstrucción de buena fe a partir de tus propios datos, no un registro oficial. En la máxima medida permitida por la ley, nuestra responsabilidad se limita a lo pagado por la app (actualmente cero); nada aquí excluye responsabilidades que legalmente no puedan excluirse.",
        "it":"Voymark è fornito \"così com'è\", senza garanzie di alcun tipo nei limiti consentiti dalla legge. I dati derivati — viaggi rilevati, attribuzione dei paesi, statistiche — sono una ricostruzione al meglio dai tuoi stessi dati, non un registro ufficiale. Nella misura massima consentita dalla legge, la nostra responsabilità è limitata a quanto pagato per l'app (attualmente zero); nulla esclude responsabilità non escludibili per legge.",
        "de":"Voymark wird \"wie besehen\" bereitgestellt, ohne Gewährleistungen jeglicher Art, soweit gesetzlich zulässig. Abgeleitete Daten — erkannte Reisen, Länderzuordnung, Statistiken — sind eine bestmögliche Rekonstruktion aus deinen eigenen Daten, kein amtliches Register. Soweit gesetzlich zulässig, ist unsere Haftung auf den für die App gezahlten Betrag (derzeit null) begrenzt; gesetzlich nicht ausschließbare Haftung bleibt unberührt.",
        "ro":"Voymark este furnizat \"ca atare\", fără garanții de niciun fel, în măsura permisă de lege. Datele derivate — călătorii detectate, atribuirea țărilor, statistici — sunt o reconstrucție de bună-credință din propriile tale date, nu un registru oficial. În măsura maximă permisă de lege, răspunderea noastră este limitată la suma plătită pentru aplicație (în prezent zero); nimic de aici nu exclude răspunderea care nu poate fi exclusă legal."}},
  {"h":{"en":"Changes and contact","fr":"Modifications et contact","es":"Cambios y contacto","it":"Modifiche e contatti","de":"Änderungen und Kontakt","ro":"Modificări și contact"},
   "p":{"en":"We may update these terms; material changes will be posted here with a new date. Continuing to use the app after a change means you accept the updated terms. Questions: Outside Software SRL, hello@voymark.app.",
        "fr":"Nous pouvons mettre à jour ces conditions ; les changements importants seront publiés ici avec une nouvelle date. Continuer à utiliser l'app après un changement vaut acceptation des conditions mises à jour. Questions : Outside Software SRL, hello@voymark.app.",
        "es":"Podemos actualizar estos términos; los cambios relevantes se publicarán aquí con una nueva fecha. Seguir usando la app tras un cambio implica aceptar los términos actualizados. Preguntas: Outside Software SRL, hello@voymark.app.",
        "it":"Possiamo aggiornare questi termini; le modifiche rilevanti saranno pubblicate qui con una nuova data. Continuare a usare l'app dopo una modifica significa accettare i termini aggiornati. Domande: Outside Software SRL, hello@voymark.app.",
        "de":"Wir können diese Bedingungen aktualisieren; wesentliche Änderungen erscheinen hier mit neuem Datum. Die weitere Nutzung der App nach einer Änderung gilt als Zustimmung. Fragen: Outside Software SRL, hello@voymark.app.",
        "ro":"Putem actualiza acești termeni; modificările importante vor fi publicate aici cu o dată nouă. Continuarea folosirii aplicației după o modificare înseamnă acceptarea termenilor actualizați. Întrebări: Outside Software SRL, hello@voymark.app."}},
 ],
},

"visited-countries-map": {
 "nav": {"en":"Visited countries map","fr":"Carte des pays visités","es":"Mapa de países visitados","it":"Mappa dei paesi visitati","de":"Karte besuchter Länder","ro":"Harta țărilor vizitate"},
 "title": {
  "en":"Visited Countries Map — mark every country you've been to | Voymark",
  "fr":"Carte des pays visités — marquez chaque pays où vous êtes allé | Voymark",
  "es":"Mapa de países visitados — marca cada país donde has estado | Voymark",
  "it":"Mappa dei paesi visitati — segna ogni paese in cui sei stato | Voymark",
  "de":"Karte besuchter Länder — markiere jedes bereiste Land | Voymark",
  "ro":"Harta țărilor vizitate — marchează fiecare țară în care ai fost | Voymark"},
 "meta": {
  "en":"Mark the countries you've visited on a beautiful offline world map. Voymark is a scratch-map alternative that stamps a real travel passport — no account, no tracking, free.",
  "fr":"Marquez les pays visités sur une belle carte du monde hors ligne. Voymark est une alternative à la carte à gratter qui tamponne un vrai passeport de voyage — sans compte, sans suivi, gratuit.",
  "es":"Marca los países que has visitado en un precioso mapa del mundo offline. Voymark es una alternativa al mapa rascable que sella un pasaporte de viajes real — sin cuenta, sin rastreo, gratis.",
  "it":"Segna i paesi visitati su una bellissima mappa del mondo offline. Voymark è un'alternativa alla mappa da grattare che timbra un vero passaporto di viaggio — senza account, senza tracciamento, gratis.",
  "de":"Markiere besuchte Länder auf einer schönen Offline-Weltkarte. Voymark ist die Rubbelkarten-Alternative, die einen echten Reisepass stempelt — ohne Konto, ohne Tracking, kostenlos.",
  "ro":"Marchează țările vizitate pe o hartă a lumii frumoasă și offline. Voymark este alternativa la harta răzuibilă care ștampilează un pașaport de călătorie adevărat — fără cont, fără urmărire, gratuit."},
 "h1": {
  "en":"A map of every country you've visited","fr":"Une carte de tous les pays que vous avez visités",
  "es":"Un mapa de cada país que has visitado","it":"Una mappa di ogni paese che hai visitato",
  "de":"Eine Karte aller Länder, die du besucht hast","ro":"O hartă a tuturor țărilor pe care le-ai vizitat"},
 "lede": {
  "en":"Tap a country to stamp it. Watch your world fill in burgundy, on a clean atlas or an aged-paper map — fully offline, in your language.",
  "fr":"Touchez un pays pour le tamponner. Regardez votre monde se remplir de bordeaux, sur un atlas épuré ou une carte au papier vieilli — entièrement hors ligne, dans votre langue.",
  "es":"Toca un país para sellarlo. Mira cómo tu mundo se llena de burdeos, en un atlas limpio o un mapa de papel envejecido — totalmente offline, en tu idioma.",
  "it":"Tocca un paese per timbrarlo. Guarda il tuo mondo riempirsi di bordeaux, su un atlante pulito o una mappa di carta antica — completamente offline, nella tua lingua.",
  "de":"Tippe ein Land an, um es zu stempeln. Sieh zu, wie sich deine Welt burgunderrot füllt — auf einem klaren Atlas oder einer Karte aus gealtertem Papier, komplett offline, in deiner Sprache.",
  "ro":"Atinge o țară pentru a o ștampila. Privește cum lumea ta se umple de burgundy, pe un atlas curat sau pe o hartă de hârtie veche — complet offline, în limba ta."},
 "sections": [
  {"h":{"en":"Better than a scratch map","fr":"Mieux qu'une carte à gratter","es":"Mejor que un mapa rascable","it":"Meglio di una mappa da grattare","de":"Besser als eine Rubbelkarte","ro":"Mai bună decât o hartă răzuibilă"},
   "p":{"en":"A scratch map hangs on a wall and remembers one thing. Voymark's visited-countries map lives in your pocket, distinguishes visited from wishlist, remembers when you were there, and can even fill itself in from the photos you already have.",
        "fr":"Une carte à gratter reste au mur et ne retient qu'une chose. La carte des pays visités de Voymark vit dans votre poche, distingue visité et liste d'envies, se souvient de quand vous y étiez, et peut même se remplir toute seule à partir de vos photos.",
        "es":"Un mapa rascable cuelga de la pared y recuerda una sola cosa. El mapa de países visitados de Voymark vive en tu bolsillo, distingue visitado de lista de deseos, recuerda cuándo estuviste y hasta puede rellenarse solo con tus fotos.",
        "it":"Una mappa da grattare sta al muro e ricorda una cosa sola. La mappa dei paesi visitati di Voymark vive in tasca, distingue visitato da lista dei desideri, ricorda quando ci sei stato e può persino riempirsi da sola dalle tue foto.",
        "de":"Eine Rubbelkarte hängt an der Wand und merkt sich genau eines. Voymarks Karte besuchter Länder lebt in deiner Tasche, unterscheidet besucht von Wunschliste, weiß noch, wann du dort warst — und füllt sich sogar aus deinen Fotos von selbst.",
        "ro":"O hartă răzuibilă stă pe perete și ține minte un singur lucru. Harta țărilor vizitate din Voymark trăiește în buzunarul tău, deosebește vizitat de lista de dorințe, își amintește când ai fost acolo și se poate completa chiar singură din pozele tale."}},
  {"h":{"en":"Honest stamps","fr":"Des tampons honnêtes","es":"Sellos honestos","it":"Timbri onesti","de":"Ehrliche Stempel","ro":"Ștampile oneste"},
   "p":{"en":"Airport layover? Border dash? Mark it as transit: it inks the map without claiming the country. Six visit kinds keep your count honest — your rules, always.",
        "fr":"Escale à l'aéroport ? Passage éclair de frontière ? Marquez-le comme transit : la carte s'encre sans revendiquer le pays. Six types de visite gardent votre compte honnête — vos règles, toujours.",
        "es":"¿Escala en el aeropuerto? ¿Cruce fugaz de frontera? Márcalo como tránsito: entinta el mapa sin reclamar el país. Seis tipos de visita mantienen tu cuenta honesta — tus reglas, siempre.",
        "it":"Scalo in aeroporto? Toccata di frontiera? Segnalo come transito: inchiostra la mappa senza rivendicare il paese. Sei tipi di visita mantengono onesto il conteggio — le tue regole, sempre.",
        "de":"Zwischenstopp am Flughafen? Kurzer Grenzübertritt? Markiere es als Transit: Die Karte wird gefärbt, ohne das Land zu beanspruchen. Sechs Besuchsarten halten deine Zählung ehrlich — deine Regeln, immer.",
        "ro":"Escală în aeroport? Trecere fulger de graniță? Marcheaz-o ca tranzit: harta se colorează fără a revendica țara. Șase tipuri de vizită îți păstrează numărătoarea onestă — regulile tale, întotdeauna."}},
  {"h":{"en":"Private by architecture","fr":"Privé par architecture","es":"Privado por arquitectura","it":"Privato per architettura","de":"Privat per Architektur","ro":"Privat prin arhitectură"},
   "p":{"en":"The whole map ships inside the app. No accounts, no tracking, nothing uploaded — your travel history belongs to you.",
        "fr":"Toute la carte est livrée dans l'app. Pas de compte, pas de suivi, rien d'envoyé — votre historique de voyage vous appartient.",
        "es":"Todo el mapa viene dentro de la app. Sin cuentas, sin rastreo, nada se sube — tu historial de viajes te pertenece.",
        "it":"Tutta la mappa è inclusa nell'app. Niente account, niente tracciamento, nulla di caricato — la tua storia di viaggio appartiene a te.",
        "de":"Die ganze Karte steckt in der App. Keine Konten, kein Tracking, nichts wird hochgeladen — deine Reisegeschichte gehört dir.",
        "ro":"Întreaga hartă vine în aplicație. Fără conturi, fără urmărire, nimic încărcat — istoria ta de călătorie îți aparține."}},
  {"h": {"en":"Past the border lines","fr":"Au-delà des frontières","es":"Más allá de las fronteras","it":"Oltre i confini","de":"Jenseits der Grenzlinien","ro":"Dincolo de granițe"},
   "p": {
        "en":"A country is a coarse unit. Twelve countries go deeper — US states, German Länder, Japanese prefectures and more, 290 regions on their own tap-to-stamp maps. And four landmark collections fill themselves in from the same evidence: all 197 capitals, 1,351 UNESCO World Heritage sites, the New 7 Wonders and the 7 Natural Wonders.",
        "fr":"Un pays est une unité grossière. Douze pays vont plus loin — États américains, Länder allemands, préfectures japonaises et plus encore, 290 régions sur leurs propres cartes à tamponner. Et quatre collections de sites se remplissent des mêmes preuves : les 197 capitales, 1 351 sites du patrimoine mondial de l'UNESCO, les 7 nouvelles merveilles et les 7 merveilles naturelles.",
        "es":"Un país es una unidad gruesa. Doce países van más a fondo — estados de EE. UU., Länder alemanes, prefecturas japonesas y más, 290 regiones en sus propios mapas para sellar. Y cuatro colecciones de lugares se rellenan con la misma evidencia: las 197 capitales, 1351 sitios del Patrimonio Mundial de la UNESCO, las 7 nuevas maravillas y las 7 maravillas naturales.",
        "it":"Un paese è un'unità grossolana. Dodici paesi vanno più a fondo — stati USA, Länder tedeschi, prefetture giapponesi e altri, 290 regioni sulle loro mappe da timbrare. E quattro collezioni di luoghi si riempiono dalle stesse prove: tutte le 197 capitali, 1.351 siti del Patrimonio Mondiale UNESCO, le 7 nuove meraviglie e le 7 meraviglie naturali.",
        "de":"Ein Land ist eine grobe Einheit. Zwölf Länder gehen tiefer — US-Bundesstaaten, deutsche Länder, japanische Präfekturen und mehr, 290 Regionen auf eigenen Karten zum Stempeln. Und vier Sammlungen füllen sich aus denselben Belegen: alle 197 Hauptstädte, 1.351 UNESCO-Welterbestätten, die 7 neuen Weltwunder und die 7 Naturwunder.",
        "ro":"O țară e o unitate grosieră. Douăsprezece țări merg mai adânc — state americane, landuri germane, prefecturi japoneze și altele, 290 de regiuni pe propriile hărți de ștampilat. Iar patru colecții de locuri se completează din aceleași dovezi: toate cele 197 de capitale, 1.351 de situri UNESCO, cele 7 noi minuni și cele 7 minuni naturale."}},
  {"h":{"en":"Wishlist, in gold","fr":"Liste de souhaits, en or","es":"Lista de deseos, en oro","it":"Lista dei desideri, in oro","de":"Wunschliste, in Gold","ro":"Lista de dorințe, în auriu"},
   "p":{"en":"Not every country on the map is one you have been to. Mark the ones you want next and they fill in gold instead of burgundy, so a single map holds your record and your plan at the same time.",
        "fr":"Tous les pays de la carte ne sont pas des pays visités. Marquez ceux que vous visez et ils se remplissent en or plutôt qu'en bordeaux : une seule carte porte à la fois votre histoire et vos projets.",
        "es":"No todos los países del mapa son países que has pisado. Marca los que quieres visitar y se llenan de oro en lugar de burdeos: un mismo mapa guarda tu historial y tus planes.",
        "it":"Non tutti i paesi sulla mappa sono paesi in cui sei stato. Segna quelli che vuoi visitare e si riempiono d'oro invece che di bordeaux: una sola mappa tiene insieme il tuo archivio e i tuoi piani.",
        "de":"Nicht jedes Land auf der Karte ist eines, in dem du warst. Markiere die, die als Nächstes dran sind, und sie füllen sich golden statt burgunderrot — eine Karte trägt Bilanz und Vorhaben zugleich.",
        "ro":"Nu toate țările de pe hartă sunt țări în care ai fost. Marchează-le pe cele pe care le vrei și se umplu cu auriu în loc de bordo: o singură hartă ține și evidența, și planul."},
   "p2":{"en":"The two never mix in the arithmetic. Wishlist countries stay out of your visited count and out of your percentage of the world. The day you arrive, one tap moves a country from gold to burgundy and the stamp carries the date.",
         "fr":"Les deux ne se mélangent jamais dans les calculs. Les pays souhaités restent hors de votre compte et hors de votre pourcentage du monde. Le jour où vous arrivez, un appui fait passer le pays de l'or au bordeaux et le tampon porte la date.",
         "es":"Las dos cosas nunca se mezclan en las cuentas. Los países deseados quedan fuera de tu recuento y de tu porcentaje del mundo. El día que llegas, un toque pasa el país de oro a burdeos y el sello lleva la fecha.",
         "it":"Le due cose non si mescolano mai nei conti. I paesi desiderati restano fuori dal conteggio e dalla tua percentuale di mondo. Il giorno in cui arrivi, un tocco porta il paese dall'oro al bordeaux e il timbro riporta la data.",
         "de":"In der Rechnung vermischt sich beides nie. Wunschländer bleiben aus deiner Zählung und aus deinem Weltanteil heraus. Am Tag der Ankunft macht ein Tippen aus Gold Burgunderrot — und der Stempel trägt das Datum.",
         "ro":"Cele două nu se amestecă niciodată în socoteli. Țările dorite rămân în afara numărătorii și a procentului tău din lume. În ziua în care ajungi, o atingere mută țara din auriu în bordo, iar ștampila poartă data."}},
  {"h":{"en":"The map leaves the app when you say so","fr":"La carte sort de l'app quand vous le décidez","es":"El mapa sale de la app cuando tú quieres","it":"La mappa esce dall'app quando lo decidi tu","de":"Die Karte verlässt die App, wenn du es willst","ro":"Harta iese din aplicație când vrei tu"},
   "p":{"en":"Export it as a share card sized for stories, print your trips into a PDF travel book with maps, photos and journal pages, or keep a widget on your home screen showing your stamps, your continent progress or a ring of the world you have covered.",
        "fr":"Exportez-la en carte à partager au format stories, imprimez vos voyages dans un livre PDF avec cartes, photos et pages de journal, ou gardez un widget sur votre écran d'accueil avec vos tampons, votre progression par continent ou l'anneau du monde parcouru.",
        "es":"Expórtalo como tarjeta para historias, imprime tus viajes en un libro de viaje PDF con mapas, fotos y páginas de diario, o deja un widget en tu pantalla de inicio con tus sellos, tu progreso por continente o el anillo del mundo recorrido.",
        "it":"Esportala come card per le storie, stampa i tuoi viaggi in un libro PDF con mappe, foto e pagine di diario, oppure tieni un widget sulla schermata home con i timbri, i progressi per continente o l'anello di mondo percorso.",
        "de":"Exportiere sie als Share-Karte im Story-Format, drucke deine Reisen in ein PDF-Reisebuch mit Karten, Fotos und Tagebuchseiten, oder behalte ein Widget auf dem Homescreen mit deinen Stempeln, deinem Kontinent-Fortschritt oder dem Ring der bereisten Welt.",
        "ro":"Exportă harta ca un card de partajat pe format de story, tipărește-ți călătoriile într-o carte PDF cu hărți, poze și pagini de jurnal, sau ține un widget pe ecranul principal cu ștampilele tale, progresul pe continente ori inelul lumii parcurse."},
   "p2":{"en":"Everything underneath exports too — CSV, GPX, KML and GeoJSON for other tools, a full backup for a new phone, and a plain-text file you can read years from now without any app at all.",
         "fr":"Tout ce qu'il y a dessous s'exporte aussi — CSV, GPX, KML et GeoJSON pour d'autres outils, une sauvegarde complète pour un nouveau téléphone, et un fichier texte lisible dans dix ans sans aucune application.",
         "es":"Todo lo que hay debajo también se exporta — CSV, GPX, KML y GeoJSON para otras herramientas, una copia completa para un móvil nuevo y un archivo de texto que podrás leer dentro de años sin ninguna app.",
         "it":"Anche tutto ciò che sta sotto si esporta — CSV, GPX, KML e GeoJSON per altri strumenti, un backup completo per un telefono nuovo e un file di testo leggibile fra anni senza nessuna app.",
         "de":"Auch alles darunter lässt sich exportieren — CSV, GPX, KML und GeoJSON für andere Werkzeuge, ein vollständiges Backup fürs neue Telefon und eine Textdatei, die du in Jahren ganz ohne App noch lesen kannst.",
         "ro":"Se exportă și tot ce e dedesubt — CSV, GPX, KML și GeoJSON pentru alte unelte, un backup complet pentru un telefon nou și un fișier text pe care îl vei putea citi peste ani fără nicio aplicație."}},
 ],
 "faq": [
  {"q":{"en":"Does the visited countries map work offline?","fr":"La carte des pays visités fonctionne-t-elle hors ligne ?","es":"¿El mapa de países visitados funciona sin conexión?","it":"La mappa dei paesi visitati funziona offline?","de":"Funktioniert die Karte der besuchten Länder offline?","ro":"Harta țărilor vizitate funcționează offline?"},
   "a":{"en":"Yes. The world map ships inside the app, so stamping countries, browsing your history and exporting a share card all work in airplane mode. Only two extras need a connection: satellite map tiles and searching for a place by name.",
        "fr":"Oui. La carte du monde est intégrée à l'application : tamponner des pays, parcourir votre histoire et exporter une carte fonctionnent en mode avion. Seuls deux extras demandent une connexion : les tuiles satellite et la recherche d'un lieu par son nom.",
        "es":"Sí. El mapa del mundo viene dentro de la app, así que sellar países, revisar tu historial y exportar una tarjeta funcionan en modo avión. Solo dos extras necesitan conexión: las teselas de satélite y buscar un lugar por su nombre.",
        "it":"Sì. La mappa del mondo è dentro l'app: timbrare paesi, sfogliare la tua storia ed esportare una card funzionano in modalità aereo. Solo due extra richiedono connessione: le tile satellitari e la ricerca di un luogo per nome.",
        "de":"Ja. Die Weltkarte steckt in der App: Länder stempeln, die eigene Historie durchgehen und eine Karte exportieren geht im Flugmodus. Nur zwei Extras brauchen Netz: Satelliten-Kacheln und die Ortssuche nach Namen.",
        "ro":"Da. Harta lumii vine în aplicație, așa că ștampilarea țărilor, răsfoirea istoricului și exportul unui card merg în modul avion. Doar două lucruri au nevoie de conexiune: tile-urile satelit și căutarea unui loc după nume."}},
  {"q":{"en":"How many countries can I mark?","fr":"Combien de pays puis-je marquer ?","es":"¿Cuántos países puedo marcar?","it":"Quanti paesi posso segnare?","de":"Wie viele Länder kann ich markieren?","ro":"Câte țări pot marca?"},
   "a":{"en":"All of them, under whichever definition you choose: 197 world countries, 193 UN members, or the full 249 ISO countries and territories. Twelve countries go further still, with 290 regions on their own tap-to-stamp maps.",
        "fr":"Tous, selon la définition que vous choisissez : 197 pays du monde, 193 membres de l'ONU, ou les 249 pays et territoires ISO. Douze pays vont plus loin encore, avec 290 régions sur leurs propres cartes à tamponner.",
        "es":"Todos, según la definición que elijas: 197 países del mundo, 193 miembros de la ONU o los 249 países y territorios ISO. Doce países van aún más lejos, con 290 regiones en sus propios mapas para sellar.",
        "it":"Tutti, secondo la definizione che scegli: 197 paesi del mondo, 193 membri ONU o tutti i 249 paesi e territori ISO. Dodici paesi vanno anche oltre, con 290 regioni su mappe proprie da timbrare.",
        "de":"Alle — je nach gewählter Definition: 197 Länder der Welt, 193 UN-Mitglieder oder die vollen 249 ISO-Länder und -Territorien. Zwölf Länder gehen noch weiter, mit 290 Regionen auf eigenen Stempelkarten.",
        "ro":"Pe toate, în funcție de definiția aleasă: 197 de țări ale lumii, 193 de membri ONU sau toate cele 249 de țări și teritorii ISO. Douăsprezece țări merg și mai departe, cu 290 de regiuni pe hărți proprii de ștampilat."}},
  {"q":{"en":"Is it free?","fr":"Est-ce gratuit ?","es":"¿Es gratis?","it":"È gratis?","de":"Ist es kostenlos?","ro":"Este gratuit?"},
   "a":{"en":"Every feature is free today, with no subscription, no ads and no account. If paid features ever arrive they will be new capabilities — what you already have stays yours.",
        "fr":"Toutes les fonctionnalités sont gratuites aujourd'hui, sans abonnement, sans publicité et sans compte. Si des fonctions payantes arrivent un jour, ce seront de nouvelles capacités — ce que vous avez déjà reste à vous.",
        "es":"Hoy todas las funciones son gratuitas, sin suscripción, sin anuncios y sin cuenta. Si algún día llegan funciones de pago, serán capacidades nuevas — lo que ya tienes sigue siendo tuyo.",
        "it":"Oggi ogni funzione è gratuita, senza abbonamento, senza pubblicità e senza account. Se un giorno arriveranno funzioni a pagamento, saranno nuove capacità — quello che hai già resta tuo.",
        "de":"Heute ist jede Funktion kostenlos — kein Abo, keine Werbung, kein Konto. Sollten je kostenpflichtige Funktionen kommen, wären es neue Fähigkeiten; was du schon hast, bleibt dir.",
        "ro":"Astăzi fiecare funcție este gratuită, fără abonament, fără reclame și fără cont. Dacă vor apărea vreodată funcții cu plată, vor fi capabilități noi — ce ai deja rămâne al tău."}},
  {"q":{"en":"Can I get my data out again?","fr":"Puis-je récupérer mes données ?","es":"¿Puedo sacar mis datos?","it":"Posso riprendermi i miei dati?","de":"Komme ich wieder an meine Daten?","ro":"Îmi pot scoate datele înapoi?"},
   "a":{"en":"At any time, without asking anyone. CSV, GPX, KML, GeoJSON, a full backup file and a readable plain-text export are all one tap away in More → Import &amp; Export.",
        "fr":"À tout moment, sans rien demander à personne. CSV, GPX, KML, GeoJSON, une sauvegarde complète et un export texte lisible sont à un appui dans Plus → Import et export.",
        "es":"Cuando quieras, sin pedir permiso a nadie. CSV, GPX, KML, GeoJSON, una copia de seguridad completa y una exportación de texto legible están a un toque en Más → Importar y exportar.",
        "it":"Quando vuoi, senza chiedere niente a nessuno. CSV, GPX, KML, GeoJSON, un backup completo e un export di testo leggibile sono a un tocco in Altro → Importa ed esporta.",
        "de":"Jederzeit, ohne jemanden zu fragen. CSV, GPX, KML, GeoJSON, ein vollständiges Backup und ein lesbarer Textexport liegen unter Mehr → Import &amp; Export.",
        "ro":"Oricând, fără să ceri voie nimănui. CSV, GPX, KML, GeoJSON, un backup complet și un export text lizibil sunt la o atingere în Mai multe → Import și export."}},
  {"q":{"en":"How is this different from a scratch map?","fr":"En quoi est-ce différent d'une carte à gratter ?","es":"¿En qué se diferencia de un mapa rascable?","it":"In cosa è diversa da una mappa da grattare?","de":"Was unterscheidet das von einer Rubbelkarte?","ro":"Cu ce diferă de o hartă răzuibilă?"},
   "a":{"en":"A scratch map records one bit per country and cannot be undone. Voymark records when you went, how you got there, which cities and regions you saw, and whether a layover should count at all — and you can change your mind.",
        "fr":"Une carte à gratter retient un seul bit par pays, et sans retour en arrière. Voymark retient quand vous y étiez, comment vous y êtes allé, quelles villes et régions vous avez vues, et si une escale doit compter — et vous pouvez changer d'avis.",
        "es":"Un mapa rascable guarda un solo bit por país y no tiene marcha atrás. Voymark guarda cuándo fuiste, cómo llegaste, qué ciudades y regiones viste y si una escala debe contar — y puedes cambiar de opinión.",
        "it":"Una mappa da grattare registra un solo bit per paese e non torna indietro. Voymark registra quando ci sei stato, come ci sei arrivato, quali città e regioni hai visto e se uno scalo debba contare — e puoi cambiare idea.",
        "de":"Eine Rubbelkarte speichert ein Bit pro Land, unwiderruflich. Voymark hält fest, wann du dort warst, wie du hinkamst, welche Städte und Regionen du gesehen hast und ob ein Zwischenstopp überhaupt zählen soll — und du darfst es dir anders überlegen.",
        "ro":"O hartă răzuibilă reține un singur bit pe țară și nu se mai poate întoarce. Voymark reține când ai fost, cum ai ajuns, ce orașe și regiuni ai văzut și dacă o escală ar trebui să conteze — iar tu te poți răzgândi."}},
 ],
},

"travel-tracker-app": {
 "nav": {"en":"Travel tracker","fr":"Suivi de voyages","es":"Registro de viajes","it":"Registro dei viaggi","de":"Reise-Tracker","ro":"Jurnal de călătorii"},
 "title": {
  "en":"Travel Tracker App — trips, places and stats, offline | Voymark",
  "fr":"App de suivi de voyages — voyages, lieux et stats, hors ligne | Voymark",
  "es":"App para registrar viajes — viajes, lugares y estadísticas, offline | Voymark",
  "it":"App per tracciare i viaggi — viaggi, luoghi e statistiche, offline | Voymark",
  "de":"Reise-Tracker-App — Reisen, Orte und Statistiken, offline | Voymark",
  "ro":"Aplicație jurnal de călătorii — călătorii, locuri și statistici, offline | Voymark"},
 "meta": {
  "en":"Track every trip, place and travel day in one private travel log. Timelines, statistics, annual recaps and PDF travel books — offline, no account, free.",
  "fr":"Suivez chaque voyage, lieu et jour de voyage dans un journal privé. Chronologies, statistiques, rétrospectives annuelles et livres de voyage PDF — hors ligne, sans compte, gratuit.",
  "es":"Registra cada viaje, lugar y día de viaje en un diario privado. Cronologías, estadísticas, resúmenes anuales y libros de viaje en PDF — offline, sin cuenta, gratis.",
  "it":"Registra ogni viaggio, luogo e giorno di viaggio in un diario privato. Cronologie, statistiche, riepiloghi annuali e libri di viaggio PDF — offline, senza account, gratis.",
  "de":"Halte jede Reise, jeden Ort und jeden Reisetag in einem privaten Reiselog fest. Zeitleisten, Statistiken, Jahresrückblicke und PDF-Reisebücher — offline, ohne Konto, kostenlos.",
  "ro":"Ține evidența fiecărei călătorii, loc și zi de călătorie într-un jurnal privat. Cronologii, statistici, retrospective anuale și cărți de călătorie PDF — offline, fără cont, gratuit."},
 "h1": {
  "en":"A travel tracker that respects your travels","fr":"Un suivi de voyages qui respecte vos voyages",
  "es":"Un registro de viajes que respeta tus viajes","it":"Un registro che rispetta i tuoi viaggi",
  "de":"Ein Reise-Tracker, der deine Reisen respektiert","ro":"Un jurnal care îți respectă călătoriile"},
 "lede": {
  "en":"Trips with places, dates, notes and photos. A timeline by year. Statistics that answer the questions you actually ask. All of it offline, in a passport that feels like one.",
  "fr":"Des voyages avec lieux, dates, notes et photos. Une chronologie par année. Des statistiques qui répondent aux questions que vous vous posez vraiment. Le tout hors ligne, dans un passeport digne de ce nom.",
  "es":"Viajes con lugares, fechas, notas y fotos. Una cronología por años. Estadísticas que responden a lo que de verdad te preguntas. Todo offline, en un pasaporte que se siente como tal.",
  "it":"Viaggi con luoghi, date, note e foto. Una cronologia per anno. Statistiche che rispondono alle domande che ti fai davvero. Tutto offline, in un passaporto che sembra vero.",
  "de":"Reisen mit Orten, Daten, Notizen und Fotos. Eine Zeitleiste nach Jahren. Statistiken, die die Fragen beantworten, die du wirklich stellst. Alles offline, in einem Pass, der sich wie einer anfühlt.",
  "ro":"Călătorii cu locuri, date, notițe și poze. O cronologie pe ani. Statistici care răspund la întrebările pe care ți le pui cu adevărat. Totul offline, într-un pașaport care chiar arată ca unul."},
 "sections": [
  {"h":{"en":"Your travel log, three ways","fr":"Votre journal, de trois façons","es":"Tu diario, de tres maneras","it":"Il tuo diario, in tre modi","de":"Dein Reiselog, auf drei Arten","ro":"Jurnalul tău, în trei feluri"},
   "p":{"en":"Build trips from your photos automatically, add them by hand in seconds, or import GPX and KML tracks from other tools. However they arrive, your passport stays consistent.",
        "fr":"Construisez vos voyages automatiquement depuis vos photos, ajoutez-les à la main en quelques secondes, ou importez des traces GPX et KML d'autres outils. Quelle que soit la source, votre passeport reste cohérent.",
        "es":"Crea viajes automáticamente desde tus fotos, añádelos a mano en segundos o importa rutas GPX y KML de otras herramientas. Lleguen como lleguen, tu pasaporte se mantiene coherente.",
        "it":"Costruisci i viaggi automaticamente dalle tue foto, aggiungili a mano in pochi secondi o importa tracce GPX e KML da altri strumenti. Comunque arrivino, il tuo passaporto resta coerente.",
        "de":"Baue Reisen automatisch aus deinen Fotos, füge sie in Sekunden von Hand hinzu oder importiere GPX- und KML-Tracks aus anderen Tools. Egal woher — dein Pass bleibt konsistent.",
        "ro":"Construiește călătorii automat din pozele tale, adaugă-le manual în câteva secunde sau importă trasee GPX și KML din alte instrumente. Oricum ar veni, pașaportul tău rămâne coerent."}},
  {"h":{"en":"Stats that mean something","fr":"Des stats qui veulent dire quelque chose","es":"Estadísticas con sentido","it":"Statistiche che contano","de":"Statistiken mit Bedeutung","ro":"Statistici cu sens"},
   "p":{"en":"Countries, trips, unique places, travel days, kilometers, flights versus overland — plus the furthest place you have ever been from home, your compass extremes, and your longest run of consecutive travelling years. An annual recap replays the year's routes on the map and exports as a share card or PDF travel book.",
        "fr":"Pays, voyages, lieux uniques, jours de voyage, kilomètres, vols contre trajets terrestres — plus le lieu le plus éloigné de chez vous où vous soyez allé, vos extrêmes cardinaux et votre plus longue série d'années de voyage consécutives. Une rétrospective annuelle rejoue les itinéraires de l'année sur la carte et s'exporte en carte à partager ou en livre de voyage PDF.",
        "es":"Países, viajes, lugares únicos, días de viaje, kilómetros, vuelos frente a trayectos por tierra — más el lugar más lejano de casa al que has llegado, tus extremos cardinales y tu racha más larga de años viajando seguidos. Un resumen anual reproduce las rutas del año en el mapa y se exporta como tarjeta o libro de viaje en PDF.",
        "it":"Paesi, viaggi, luoghi unici, giorni di viaggio, chilometri, voli contro tratte via terra — più il luogo più lontano da casa in cui tu sia mai stato, i tuoi estremi cardinali e la serie più lunga di anni di viaggio consecutivi. Un riepilogo annuale rigioca le rotte dell'anno sulla mappa e si esporta come card o libro di viaggio PDF.",
        "de":"Länder, Reisen, einzigartige Orte, Reisetage, Kilometer, Flüge versus Landwege — plus der am weitesten von zu Hause entfernte Ort, an dem du je warst, deine Himmelsrichtungs-Extreme und deine längste Serie aufeinanderfolgender Reisejahre. Ein Jahresrückblick spielt die Routen des Jahres auf der Karte ab und exportiert sich als Share-Karte oder PDF-Reisebuch.",
        "ro":"Țări, călătorii, locuri unice, zile de călătorie, kilometri, zboruri versus trasee terestre — plus cel mai îndepărtat loc de acasă în care ai ajuns vreodată, extremele tale cardinale și cea mai lungă serie de ani consecutivi cu călătorii. O retrospectivă anuală redă rutele anului pe hartă și se exportă drept card sau carte de călătorie PDF."}},
  {"h":{"en":"No account, no lock-in","fr":"Sans compte, sans verrouillage","es":"Sin cuenta, sin ataduras","it":"Senza account, senza vincoli","de":"Kein Konto, kein Lock-in","ro":"Fără cont, fără blocaje"},
   "p":{"en":"Everything exports in open formats — CSV, GPX, KML, GeoJSON, plus a full readable-JSON backup. Your data is never locked in, because it was never ours to lock.",
        "fr":"Tout s'exporte en formats ouverts — CSV, GPX, KML, GeoJSON, plus une sauvegarde complète en JSON lisible. Vos données ne sont jamais verrouillées, car elles n'ont jamais été à nous.",
        "es":"Todo se exporta en formatos abiertos — CSV, GPX, KML, GeoJSON, más una copia completa en JSON legible. Tus datos nunca quedan bloqueados, porque nunca fueron nuestros.",
        "it":"Tutto si esporta in formati aperti — CSV, GPX, KML, GeoJSON, più un backup completo in JSON leggibile. I tuoi dati non restano mai bloccati, perché non sono mai stati nostri.",
        "de":"Alles exportiert in offene Formate — CSV, GPX, KML, GeoJSON, plus ein vollständiges Backup als lesbares JSON. Deine Daten sind nie eingesperrt — sie waren nie unsere.",
        "ro":"Totul se exportă în formate deschise — CSV, GPX, KML, GeoJSON, plus o copie completă în JSON lizibil. Datele tale nu sunt niciodată blocate, pentru că n-au fost niciodată ale noastre."}},
  {"h": {"en":"A diary, not just a log","fr":"Un journal, pas seulement un registre","es":"Un diario, no solo un registro","it":"Un diario, non solo un registro","de":"Ein Tagebuch, nicht nur ein Logbuch","ro":"Un jurnal, nu doar o evidență"},
   "p": {
        "en":"Write a page for any day of a trip and record who you were with — the names filter your timeline, and the pages are printed into your PDF travel book. Meanwhile the passport keeps score on its own: around 29 seals press themselves from your record, for country milestones, every continent, the Arctic Circle, the equator and the point exactly opposite your home.",
        "fr":"Écrivez une page pour n'importe quel jour d'un voyage et notez avec qui vous étiez — les noms filtrent votre chronologie, et les pages s'impriment dans votre livre de voyage PDF. Pendant ce temps le passeport tient les comptes tout seul : environ 29 sceaux s'apposent d'après votre histoire, pour les jalons de pays, chaque continent, le cercle polaire, l'équateur et le point exactement opposé à chez vous.",
        "es":"Escribe una página para cualquier día de un viaje y anota con quién estabas — los nombres filtran tu cronología y las páginas se imprimen en tu libro de viaje en PDF. Mientras tanto el pasaporte lleva la cuenta solo: unos 29 sellos se estampan desde tu registro, por hitos de países, cada continente, el círculo polar, el ecuador y el punto exactamente opuesto a tu casa.",
        "it":"Scrivi una pagina per ogni giorno di un viaggio e annota con chi eri — i nomi filtrano la tua cronologia e le pagine finiscono nel tuo libro di viaggio PDF. Intanto il passaporto tiene il conto da solo: circa 29 sigilli si imprimono dal tuo archivio, per traguardi di paesi, ogni continente, il circolo polare, l'equatore e il punto esattamente opposto a casa tua.",
        "de":"Schreib eine Seite zu jedem Reisetag und halt fest, mit wem du unterwegs warst — die Namen filtern deine Zeitleiste, und die Seiten werden in dein PDF-Reisebuch gedruckt. Derweil führt der Pass von selbst Buch: rund 29 Siegel stempeln sich aus deiner Bilanz, für Länder-Meilensteine, jeden Kontinent, den Polarkreis, den Äquator und den Punkt genau gegenüber deinem Zuhause.",
        "ro":"Scrie o pagină pentru orice zi dintr-o călătorie și notează cu cine ai fost — numele îți filtrează cronologia, iar paginile se tipăresc în cartea ta de călătorie PDF. Între timp pașaportul ține socoteala singur: aproximativ 29 de sigilii se aplică din evidența ta, pentru praguri de țări, fiecare continent, cercul polar, ecuatorul și punctul exact opus casei tale."}},
  {"h":{"en":"A timeline that reads like a life","fr":"Une chronologie qui se lit comme une vie","es":"Una línea de tiempo que se lee como una vida","it":"Una cronologia che si legge come una vita","de":"Eine Zeitleiste, die sich wie ein Leben liest","ro":"O cronologie care se citește ca o viață"},
   "p":{"en":"Trips stack by year, newest first, each with its countries, its dates and its cover photo. Filter by country to see every time you went back, or by the person you travelled with to pull out the years you were never alone.",
        "fr":"Les voyages s'empilent par année, du plus récent au plus ancien, chacun avec ses pays, ses dates et sa photo de couverture. Filtrez par pays pour revoir tous vos retours, ou par compagnon de voyage pour isoler les années où vous n'étiez jamais seul.",
        "es":"Los viajes se apilan por año, del más reciente al más antiguo, cada uno con sus países, sus fechas y su foto de portada. Filtra por país para ver todas las veces que volviste, o por la persona con quien viajaste para sacar los años en que nunca estuviste solo.",
        "it":"I viaggi si impilano per anno, dal più recente, ognuno con i suoi paesi, le sue date e la sua foto di copertina. Filtra per paese per rivedere tutte le volte che ci sei tornato, o per la persona con cui hai viaggiato per estrarre gli anni in cui non sei mai stato solo.",
        "de":"Reisen stapeln sich nach Jahr, die neueste oben, jede mit ihren Ländern, ihren Daten und ihrem Titelbild. Filtere nach Land, um jede Rückkehr zu sehen, oder nach Reisebegleitung, um die Jahre herauszuziehen, in denen du nie allein warst.",
        "ro":"Călătoriile se așază pe ani, cea mai nouă prima, fiecare cu țările, datele și poza ei de copertă. Filtrează după țară ca să vezi de câte ori te-ai întors sau după persoana cu care ai călătorit ca să scoți anii în care nu ai fost niciodată singur."},
   "p2":{"en":"Open a trip and it is all there: the places in order, the route on the map, the photos you linked, the journal pages you wrote and the notes you would otherwise have forgotten. Nothing is spread across three apps.",
         "fr":"Ouvrez un voyage et tout y est : les lieux dans l'ordre, l'itinéraire sur la carte, les photos liées, les pages de journal écrites et les notes que vous auriez sinon oubliées. Rien n'est éparpillé entre trois applications.",
         "es":"Abre un viaje y está todo: los lugares en orden, la ruta en el mapa, las fotos que enlazaste, las páginas de diario que escribiste y las notas que si no habrías olvidado. Nada queda repartido entre tres apps.",
         "it":"Apri un viaggio ed è tutto lì: i luoghi in ordine, il percorso sulla mappa, le foto collegate, le pagine di diario che hai scritto e le note che altrimenti avresti dimenticato. Niente sparso fra tre app.",
         "de":"Öffne eine Reise, und alles ist da: die Orte in Reihenfolge, die Route auf der Karte, die verknüpften Fotos, die geschriebenen Tagebuchseiten und die Notizen, die du sonst vergessen hättest. Nichts liegt in drei Apps verstreut.",
         "ro":"Deschizi o călătorie și e tot acolo: locurile în ordine, traseul pe hartă, pozele legate, paginile de jurnal scrise și notițele pe care altfel le-ai fi uitat. Nimic nu e împrăștiat prin trei aplicații."}},
  {"h":{"en":"Built to outlive the app","fr":"Conçu pour survivre à l'application","es":"Hecho para sobrevivir a la app","it":"Fatto per sopravvivere all'app","de":"Gebaut, um die App zu überleben","ro":"Făcut să supraviețuiască aplicației"},
   "p":{"en":"A travel record is only worth keeping if it survives a new phone, a change of platform and eventually the app itself. Voymark's backup file is readable JSON, its exports are the same formats the rest of the world uses, and one of them is plain text you can open in any editor.",
        "fr":"Un carnet de voyage ne vaut d'être tenu que s'il survit à un nouveau téléphone, à un changement de plateforme et, un jour, à l'application elle-même. La sauvegarde de Voymark est du JSON lisible, ses exports sont les formats que tout le monde utilise, et l'un d'eux est du texte brut ouvrable dans n'importe quel éditeur.",
        "es":"Un registro de viajes solo merece la pena si sobrevive a un móvil nuevo, a un cambio de plataforma y, algún día, a la propia app. La copia de seguridad de Voymark es JSON legible, sus exportaciones son los formatos que usa todo el mundo, y una de ellas es texto plano que abre cualquier editor.",
        "it":"Un archivio di viaggi vale la pena solo se sopravvive a un telefono nuovo, a un cambio di piattaforma e un giorno all'app stessa. Il backup di Voymark è JSON leggibile, le esportazioni usano i formati che usa tutto il mondo, e una di esse è testo semplice apribile in qualsiasi editor.",
        "de":"Eine Reisebilanz lohnt sich nur, wenn sie ein neues Telefon, einen Plattformwechsel und irgendwann die App selbst überlebt. Voymarks Backup ist lesbares JSON, die Exporte nutzen die Formate, die alle nutzen, und einer davon ist reiner Text für jeden Editor.",
        "ro":"O evidență de călătorii merită ținută doar dacă supraviețuiește unui telefon nou, unei schimbări de platformă și, într-o zi, aplicației înseși. Backupul Voymark este JSON lizibil, exporturile folosesc formatele pe care le folosește toată lumea, iar unul dintre ele e text simplu, deschis de orice editor."},
   "p2":{"en":"The same file moves between iPhone and Android in both directions, because both apps read and write one format. There is no server in the middle, so there is nothing to shut down.",
         "fr":"Le même fichier passe de l'iPhone à Android et inversement, parce que les deux applications lisent et écrivent le même format. Aucun serveur au milieu : il n'y a donc rien qui puisse fermer.",
         "es":"El mismo archivo va de iPhone a Android y al revés, porque ambas apps leen y escriben un solo formato. No hay servidor en medio, así que no hay nada que pueda cerrar.",
         "it":"Lo stesso file passa da iPhone ad Android e viceversa, perché entrambe le app leggono e scrivono un unico formato. Non c'è nessun server in mezzo, quindi non c'è niente che possa chiudere.",
         "de":"Dieselbe Datei wandert zwischen iPhone und Android in beide Richtungen, weil beide Apps ein Format lesen und schreiben. Kein Server dazwischen — also nichts, das abgeschaltet werden könnte.",
         "ro":"Același fișier trece între iPhone și Android în ambele sensuri, pentru că ambele aplicații citesc și scriu un singur format. Nu există niciun server la mijloc, deci nu există nimic care să se închidă."}},
 ],
 "faq": [
  {"q":{"en":"What makes this different from a travel app with an account?","fr":"Qu'est-ce qui change par rapport à une app de voyage avec compte ?","es":"¿Qué lo diferencia de una app de viajes con cuenta?","it":"Cosa cambia rispetto a un'app di viaggio con account?","de":"Was unterscheidet das von einer Reise-App mit Konto?","ro":"Cu ce diferă de o aplicație de călătorii cu cont?"},
   "a":{"en":"There is nothing to sign up for and nothing to log in to. Your trips live in the app's own storage on your phone, which means no servers hold them, no analytics watch you use them, and no subscription stands between you and your own history.",
        "fr":"Il n'y a rien à créer et rien à connecter. Vos voyages vivent dans le stockage de l'application sur votre téléphone : aucun serveur ne les détient, aucune analytique ne vous observe, aucun abonnement ne s'interpose entre vous et votre propre histoire.",
        "es":"No hay nada que registrar ni con qué iniciar sesión. Tus viajes viven en el almacenamiento de la app en tu móvil: ningún servidor los guarda, ninguna analítica te observa y ninguna suscripción se interpone entre tú y tu propia historia.",
        "it":"Non c'è nulla a cui iscriversi e nulla in cui accedere. I tuoi viaggi vivono nello spazio dell'app sul tuo telefono: nessun server li conserva, nessuna analitica ti osserva, nessun abbonamento si mette fra te e la tua storia.",
        "de":"Es gibt nichts zu registrieren und nichts einzuloggen. Deine Reisen liegen im Speicher der App auf deinem Telefon: kein Server hält sie, keine Analyse beobachtet dich, kein Abo steht zwischen dir und deiner eigenen Geschichte.",
        "ro":"Nu ai la ce să te înregistrezi și în ce să te autentifici. Călătoriile tale stau în spațiul aplicației, pe telefonul tău: niciun server nu le ține, nicio analitică nu te privește, niciun abonament nu stă între tine și propria ta istorie."}},
  {"q":{"en":"Do I have to type every trip in by hand?","fr":"Dois-je saisir chaque voyage à la main ?","es":"¿Tengo que meter cada viaje a mano?","it":"Devo inserire ogni viaggio a mano?","de":"Muss ich jede Reise von Hand eintragen?","ro":"Trebuie să introduc fiecare călătorie manual?"},
   "a":{"en":"No. Point Voymark at your photo library and it proposes finished trips — dates, places and countries — from the coordinates your photos already carry. You review every candidate before anything is saved, and you can still add a trip by hand in about fifteen seconds.",
        "fr":"Non. Pointez Voymark vers votre photothèque et il propose des voyages déjà constitués — dates, lieux, pays — à partir des coordonnées que vos photos portent déjà. Vous validez chaque proposition avant tout enregistrement, et vous pouvez toujours ajouter un voyage à la main en une quinzaine de secondes.",
        "es":"No. Apunta Voymark a tu fototeca y te propone viajes ya montados — fechas, lugares y países — a partir de las coordenadas que tus fotos ya llevan. Revisas cada candidato antes de guardar nada, y siempre puedes añadir un viaje a mano en unos quince segundos.",
        "it":"No. Punta Voymark alla tua libreria foto e ti propone viaggi già pronti — date, luoghi e paesi — dalle coordinate che le foto portano già. Rivedi ogni proposta prima che venga salvato qualcosa, e puoi comunque aggiungere un viaggio a mano in una quindicina di secondi.",
        "de":"Nein. Richte Voymark auf deine Fotomediathek, und es schlägt fertige Reisen vor — Daten, Orte, Länder — aus den Koordinaten, die deine Fotos ohnehin tragen. Du prüfst jeden Vorschlag, bevor etwas gespeichert wird, und kannst eine Reise weiterhin in rund fünfzehn Sekunden von Hand anlegen.",
        "ro":"Nu. Îndreaptă Voymark spre galeria ta foto și îți propune călătorii gata făcute — date, locuri și țări — din coordonatele pe care pozele le poartă deja. Verifici fiecare propunere înainte să se salveze ceva și poți oricând adăuga o călătorie manual, în vreo cincisprezece secunde."}},
  {"q":{"en":"Can I move my history to a new phone?","fr":"Puis-je transférer mon historique sur un nouveau téléphone ?","es":"¿Puedo pasar mi historial a un móvil nuevo?","it":"Posso spostare la mia storia su un telefono nuovo?","de":"Kann ich meine Historie auf ein neues Telefon holen?","ro":"Îmi pot muta istoricul pe un telefon nou?"},
   "a":{"en":"Export a backup file, move it however you like — AirDrop, a cable, a cloud folder you already trust — and restore it on the new phone. It works from iPhone to Android and back, because both apps use the same format.",
        "fr":"Exportez un fichier de sauvegarde, transférez-le comme vous voulez — AirDrop, câble, dossier cloud de confiance — et restaurez-le sur le nouveau téléphone. Cela marche de l'iPhone vers Android et inversement, les deux apps utilisant le même format.",
        "es":"Exporta un archivo de copia de seguridad, muévelo como prefieras — AirDrop, un cable, una carpeta en la nube de tu confianza — y restáuralo en el móvil nuevo. Funciona de iPhone a Android y al revés, porque ambas apps usan el mismo formato.",
        "it":"Esporta un file di backup, spostalo come preferisci — AirDrop, un cavo, una cartella cloud di cui ti fidi — e ripristinalo sul telefono nuovo. Funziona da iPhone ad Android e viceversa, perché entrambe le app usano lo stesso formato.",
        "de":"Exportiere eine Backup-Datei, bring sie wie du magst hinüber — AirDrop, Kabel, ein Cloud-Ordner, dem du ohnehin traust — und stelle sie auf dem neuen Telefon wieder her. Das klappt vom iPhone zu Android und zurück, denn beide Apps nutzen dasselbe Format.",
        "ro":"Exportă un fișier de backup, mută-l cum vrei — AirDrop, un cablu, un folder în cloud în care ai deja încredere — și restaurează-l pe telefonul nou. Merge de la iPhone la Android și invers, pentru că ambele aplicații folosesc același format."}},
  {"q":{"en":"Does it keep a travel diary as well?","fr":"Tient-il aussi un journal de voyage ?","es":"¿Lleva también un diario de viaje?","it":"Tiene anche un diario di viaggio?","de":"Führt es auch ein Reisetagebuch?","ro":"Ține și un jurnal de călătorie?"},
   "a":{"en":"Each trip has a page per day for what happened, and each trip records who you were with. Both are printed into the PDF travel book alongside the maps and photos, so the diary is not stranded inside the app.",
        "fr":"Chaque voyage dispose d'une page par jour pour ce qui s'est passé, et retient avec qui vous étiez. Les deux s'impriment dans le livre de voyage PDF, à côté des cartes et des photos : le journal n'est pas prisonnier de l'application.",
        "es":"Cada viaje tiene una página por día para lo que pasó, y guarda con quién ibas. Ambas cosas se imprimen en el libro de viaje PDF junto a los mapas y las fotos, así que el diario no se queda atrapado en la app.",
        "it":"Ogni viaggio ha una pagina al giorno per ciò che è successo e registra con chi eri. Entrambe finiscono stampate nel libro di viaggio PDF accanto a mappe e foto, così il diario non resta prigioniero dell'app.",
        "de":"Jede Reise hat eine Seite pro Tag für das, was passiert ist, und hält fest, mit wem du unterwegs warst. Beides wird ins PDF-Reisebuch neben Karten und Fotos gedruckt — das Tagebuch bleibt also nicht in der App gefangen.",
        "ro":"Fiecare călătorie are câte o pagină pe zi pentru ce s-a întâmplat și reține cu cine ai fost. Ambele se tipăresc în cartea de călătorie PDF, lângă hărți și poze, așa că jurnalul nu rămâne prizonier în aplicație."}},
  {"q":{"en":"Which languages does it speak?","fr":"Quelles langues parle-t-elle ?","es":"¿Qué idiomas habla?","it":"Che lingue parla?","de":"Welche Sprachen spricht die App?","ro":"Ce limbi vorbește?"},
   "a":{"en":"English, French, Spanish, Italian, German and Romanian, all fully translated rather than partly. You pick the language inside the app, independently of the phone's own setting.",
        "fr":"Anglais, français, espagnol, italien, allemand et roumain, entièrement traduits et non à moitié. Vous choisissez la langue dans l'application, indépendamment du réglage du téléphone.",
        "es":"Inglés, francés, español, italiano, alemán y rumano, todos traducidos por completo y no a medias. Eliges el idioma dentro de la app, independientemente del ajuste del móvil.",
        "it":"Inglese, francese, spagnolo, italiano, tedesco e rumeno, tradotti per intero e non a metà. Scegli la lingua dentro l'app, indipendentemente dall'impostazione del telefono.",
        "de":"Englisch, Französisch, Spanisch, Italienisch, Deutsch und Rumänisch — vollständig übersetzt, nicht halb. Die Sprache wählst du in der App, unabhängig von der Systemeinstellung.",
        "ro":"Engleză, franceză, spaniolă, italiană, germană și română, traduse complet, nu pe jumătate. Alegi limba din aplicație, independent de setarea telefonului."}},
 ],
},

"country-counter": {
 "nav": {"en":"Country counter","fr":"Compteur de pays","es":"Contador de países","it":"Contatore di paesi","de":"Länderzähler","ro":"Numărător de țări"},
 "title": {
  "en":"Country Counter — how many countries have you visited? | Voymark",
  "fr":"Compteur de pays — combien de pays avez-vous visités ? | Voymark",
  "es":"Contador de países — ¿cuántos países has visitado? | Voymark",
  "it":"Contatore di paesi — quanti paesi hai visitato? | Voymark",
  "de":"Länderzähler — wie viele Länder hast du besucht? | Voymark",
  "ro":"Numărător de țări — câte țări ai vizitat? | Voymark"},
 "meta": {
  "en":"Count your visited countries the honest way: 197 world countries, 193 UN members, or all 249 territories. Transit doesn't count unless you say so. Free, offline, no account.",
  "fr":"Comptez vos pays visités honnêtement : 197 pays du monde, 193 membres de l'ONU, ou les 249 territoires. Le transit ne compte pas, sauf si vous le décidez. Gratuit, hors ligne, sans compte.",
  "es":"Cuenta tus países visitados con honestidad: 197 países del mundo, 193 miembros de la ONU o los 249 territorios. El tránsito no cuenta salvo que tú lo digas. Gratis, offline, sin cuenta.",
  "it":"Conta i paesi visitati in modo onesto: 197 paesi del mondo, 193 membri ONU o tutti i 249 territori. Il transito non conta, a meno che non lo decida tu. Gratis, offline, senza account.",
  "de":"Zähle deine besuchten Länder ehrlich: 197 Länder der Welt, 193 UN-Mitglieder oder alle 249 Territorien. Transit zählt nur, wenn du es sagst. Kostenlos, offline, ohne Konto.",
  "ro":"Numără-ți țările vizitate în mod onest: 197 de țări ale lumii, 193 de membri ONU sau toate cele 249 de teritorii. Tranzitul nu contează decât dacă spui tu. Gratuit, offline, fără cont."},
 "h1": {
  "en":"How many countries have you visited?","fr":"Combien de pays avez-vous visités ?",
  "es":"¿Cuántos países has visitado?","it":"Quanti paesi hai visitato?",
  "de":"Wie viele Länder hast du besucht?","ro":"Câte țări ai vizitat?"},
 "lede": {
  "en":"It depends who's counting. Voymark lets you pick the rules — and keeps the answer honest.",
  "fr":"Cela dépend de qui compte. Voymark vous laisse choisir les règles — et garde la réponse honnête.",
  "es":"Depende de quién cuente. Voymark te deja elegir las reglas — y mantiene la respuesta honesta.",
  "it":"Dipende da chi conta. Voymark ti lascia scegliere le regole — e mantiene onesta la risposta.",
  "de":"Kommt darauf an, wer zählt. Voymark lässt dich die Regeln wählen — und hält die Antwort ehrlich.",
  "ro":"Depinde cine numără. Voymark te lasă să alegi regulile — și păstrează răspunsul onest."},
 "sections": [
  {"h":{"en":"197, 193 or 249?","fr":"197, 193 ou 249 ?","es":"¿197, 193 o 249?","it":"197, 193 o 249?","de":"197, 193 oder 249?","ro":"197, 193 sau 249?"},
   "p":{"en":"The classic \"world\" list has 197 countries; the UN recognizes 193 members; ISO lists 249 countries and territories. Voymark supports all three definitions, and every number in the app — passport, stats, continents, share cards — follows the one you choose. What sits inside each of those numbers is unpacked on <a href=\"how-many-countries-in-the-world.html\">how many countries there are in the world</a>.",
        "fr":"La liste « monde » classique compte 197 pays ; l'ONU reconnaît 193 membres ; l'ISO recense 249 pays et territoires. Voymark prend en charge les trois définitions, et chaque nombre de l'app — passeport, stats, continents, cartes — suit celle que vous choisissez. Ce que contient chacun de ces chiffres est détaillé sur <a href=\"how-many-countries-in-the-world.html\">combien y a-t-il de pays dans le monde</a>.",
        "es":"La lista clásica del \"mundo\" tiene 197 países; la ONU reconoce 193 miembros; la ISO lista 249 países y territorios. Voymark admite las tres definiciones, y cada número de la app — pasaporte, estadísticas, continentes, tarjetas — sigue la que elijas. Lo que hay dentro de cada cifra se desglosa en <a href=\"how-many-countries-in-the-world.html\">cuántos países hay en el mundo</a>.",
        "it":"La classica lista \"mondo\" ha 197 paesi; l'ONU riconosce 193 membri; l'ISO elenca 249 paesi e territori. Voymark supporta tutte e tre le definizioni, e ogni numero dell'app — passaporto, statistiche, continenti, card — segue quella che scegli. Cosa c'è dentro ognuno di questi numeri è spiegato in <a href=\"how-many-countries-in-the-world.html\">quanti paesi ci sono nel mondo</a>.",
        "de":"Die klassische \"Welt\"-Liste hat 197 Länder; die UN erkennt 193 Mitglieder an; die ISO führt 249 Länder und Territorien. Voymark unterstützt alle drei Definitionen — und jede Zahl in der App folgt der, die du wählst. Was in jeder dieser Zahlen steckt, steht unter <a href=\"how-many-countries-in-the-world.html\">wie viele Länder es auf der Welt gibt</a>.",
        "ro":"Lista clasică a \"lumii\" are 197 de țări; ONU recunoaște 193 de membri; ISO listează 249 de țări și teritorii. Voymark suportă toate cele trei definiții, iar fiecare număr din aplicație — pașaport, statistici, continente, carduri — o urmează pe cea aleasă de tine. Ce se află în fiecare dintre aceste numere este desfăcut pe <a href=\"how-many-countries-in-the-world.html\">câte țări sunt în lume</a>."}},
  {"h":{"en":"Does an airport count?","fr":"Une escale compte-t-elle ?","es":"¿Cuenta un aeropuerto?","it":"Conta un aeroporto?","de":"Zählt ein Flughafen?","ro":"Contează un aeroport?"},
   "p":{"en":"Travelers argue about this forever. Voymark's answer: you decide. Mark a country as visited, overnight, lived — or as transit, airport-only or border-dash, which ink the map without adding to your count.",
        "fr":"Les voyageurs en débattent sans fin. La réponse de Voymark : c'est vous qui décidez. Marquez un pays comme visité, nuité, vécu — ou comme transit, aéroport ou passage de frontière, qui encrent la carte sans gonfler votre compte.",
        "es":"Los viajeros discuten esto eternamente. La respuesta de Voymark: decides tú. Marca un país como visitado, con noche, vivido — o como tránsito, solo aeropuerto o cruce fugaz, que entintan el mapa sin sumar a tu cuenta.",
        "it":"I viaggiatori ne discutono da sempre. La risposta di Voymark: decidi tu. Segna un paese come visitato, con pernottamento, vissuto — o come transito, solo aeroporto o toccata di frontiera, che inchiostrano la mappa senza gonfiare il conteggio.",
        "de":"Reisende streiten darüber endlos. Voymarks Antwort: Du entscheidest. Markiere ein Land als besucht, übernachtet, gelebt — oder als Transit, nur Flughafen oder Grenz-Stipp, die die Karte färben, ohne deine Zählung zu erhöhen.",
        "ro":"Călătorii se ceartă pe tema asta la nesfârșit. Răspunsul Voymark: tu decizi. Marchează o țară ca vizitată, cu înnoptare, locuită — sau ca tranzit, doar aeroport ori trecere de graniță, care colorează harta fără să-ți umfle numărătoarea."}},
  {"h":{"en":"Continents and disputed places","fr":"Continents et territoires disputés","es":"Continentes y territorios en disputa","it":"Continenti e territori contesi","de":"Kontinente und umstrittene Gebiete","ro":"Continente și teritorii disputate"},
   "p":{"en":"Turkey in Europe or Asia? Is Taiwan its own count? Voymark lets you set your viewpoint for transcontinental countries and disputed territories, and every statistic follows it consistently.",
        "fr":"La Turquie en Europe ou en Asie ? Taïwan compte-t-il à part ? Voymark vous laisse définir votre point de vue pour les pays transcontinentaux et les territoires disputés, et chaque statistique le suit de manière cohérente.",
        "es":"¿Turquía en Europa o en Asia? ¿Taiwán cuenta aparte? Voymark te deja fijar tu punto de vista para países transcontinentales y territorios en disputa, y todas las estadísticas lo siguen con coherencia.",
        "it":"La Turchia in Europa o in Asia? Taiwan conta a parte? Voymark ti lascia impostare il tuo punto di vista per paesi transcontinentali e territori contesi, e ogni statistica lo segue con coerenza.",
        "de":"Türkei in Europa oder Asien? Zählt Taiwan eigenständig? Voymark lässt dich deinen Standpunkt für transkontinentale Länder und umstrittene Gebiete festlegen — jede Statistik folgt ihm konsistent.",
        "ro":"Turcia în Europa sau în Asia? Taiwanul se numără separat? Voymark te lasă să-ți setezi punctul de vedere pentru țările transcontinentale și teritoriile disputate, iar fiecare statistică îl urmează consecvent."}},
  {"h": {"en":"The rule reaches everything","fr":"La règle s'applique à tout","es":"La regla alcanza a todo","it":"La regola arriva ovunque","de":"Die Regel gilt überall","ro":"Regula ajunge peste tot"},
   "p": {
        "en":"Whichever definition you pick, it governs the whole app — not just the headline. Your percentage of the world, your continent rows, your share cards and even your seals follow it: around 29 seals press themselves from your record, and change the rule and a borderline seal can honestly lock again. The statistics go further than a count, too — total distance travelled, your longest run of consecutive travelling years, and the furthest place from home with the kilometres to prove it.",
        "fr":"Quelle que soit la définition choisie, elle régit toute l'application — pas seulement le titre. Votre pourcentage du monde, vos lignes par continent, vos cartes à partager et même vos sceaux la suivent : environ 29 sceaux s'apposent d'après votre histoire, et si vous changez de règle, un sceau limite peut honnêtement se reverrouiller. Les statistiques vont aussi plus loin qu'un simple compte — distance totale parcourue, plus longue série d'années de voyage consécutives, et le lieu le plus éloigné de chez vous avec les kilomètres à l'appui.",
        "es":"Elijas la definición que elijas, gobierna toda la app — no solo el titular. Tu porcentaje del mundo, tus filas por continente, tus tarjetas para compartir e incluso tus sellos la siguen: unos 29 sellos se estampan desde tu registro, y si cambias la regla un sello límite puede bloquearse de nuevo, con toda honestidad. Las estadísticas también van más allá de una cuenta — distancia total recorrida, tu racha más larga de años viajando seguidos y el lugar más lejano de casa con los kilómetros que lo demuestran.",
        "it":"Qualunque definizione scegli, governa tutta l'app — non solo il titolo. La tua percentuale di mondo, le righe per continente, le card da condividere e persino i tuoi sigilli la seguono: circa 29 sigilli si imprimono dal tuo archivio, e se cambi regola un sigillo al limite può onestamente richiudersi. Anche le statistiche vanno oltre un conteggio — distanza totale percorsa, la serie più lunga di anni di viaggio consecutivi e il luogo più lontano da casa con i chilometri a dimostrarlo.",
        "de":"Welche Definition du auch wählst, sie gilt für die ganze App — nicht nur für die Überschrift. Dein Weltanteil, deine Kontinentzeilen, deine Share-Karten und selbst deine Siegel folgen ihr: rund 29 Siegel stempeln sich aus deiner Bilanz, und änderst du die Regel, darf ein Grenzfall-Siegel ehrlich wieder zufallen. Auch die Statistik geht über das Zählen hinaus — zurückgelegte Gesamtstrecke, deine längste Serie aufeinanderfolgender Reisejahre und der am weitesten von zu Hause entfernte Ort samt Kilometern als Beleg.",
        "ro":"Oricare definiție alegi, ea guvernează toată aplicația — nu doar titlul. Procentul tău din lume, rândurile pe continente, cardurile de share și chiar sigiliile tale o urmează: aproximativ 29 de sigilii se aplică din evidența ta, iar dacă schimbi regula, un sigiliu la limită se poate încuia din nou, cinstit. Și statisticile merg mai departe decât un număr — distanța totală parcursă, cea mai lungă serie de ani consecutivi cu călătorii și cel mai îndepărtat loc de acasă, cu kilometrii care o dovedesc."}},
  {"h":{"en":"Six ways to have been somewhere","fr":"Six façons d'être passé quelque part","es":"Seis formas de haber estado en un sitio","it":"Sei modi di esserci stato","de":"Sechs Arten, dort gewesen zu sein","ro":"Șase feluri de a fi fost undeva"},
   "p":{"en":"Visited, stayed overnight, lived there, in transit, airport only, border crossing. Three of them add to your count and three of them do not, and the app is explicit about which is which rather than quietly deciding for you.",
        "fr":"Visité, nuit sur place, vécu, en transit, aéroport seulement, passage de frontière. Trois comptent, trois ne comptent pas, et l'application le dit clairement au lieu de trancher en douce à votre place.",
        "es":"Visitado, con noche, vivido, en tránsito, solo aeropuerto, cruce de frontera. Tres suman a tu recuento y tres no, y la app lo dice con claridad en vez de decidirlo por ti en silencio.",
        "it":"Visitato, con pernottamento, vissuto, in transito, solo aeroporto, valico di frontiera. Tre contano e tre no, e l'app lo dichiara invece di decidere di nascosto al posto tuo.",
        "de":"Besucht, übernachtet, gelebt, im Transit, nur Flughafen, Grenzübertritt. Drei zählen mit, drei nicht — und die App sagt es offen, statt still für dich zu entscheiden.",
        "ro":"Vizitat, cu înnoptare, locuit, în tranzit, doar aeroport, trecere de graniță. Trei se adaugă la numărătoare și trei nu, iar aplicația spune limpede care sunt, în loc să decidă pe tăcute în locul tău."},
   "p2":{"en":"The non-counting kinds still ink the country on the map, in a lighter shade, so a nine-hour layover in Doha shows up in your history without pretending you saw Qatar. Change a country's kind later and every number recomputes.",
         "fr":"Les catégories qui ne comptent pas encrent quand même le pays sur la carte, dans une teinte plus claire : neuf heures d'escale à Doha apparaissent dans votre histoire sans prétendre que vous avez vu le Qatar. Changez la catégorie plus tard et tous les nombres se recalculent.",
         "es":"Las categorías que no cuentan igualmente entintan el país en el mapa, en un tono más claro: nueve horas de escala en Doha aparecen en tu historial sin fingir que viste Catar. Cambia la categoría luego y todos los números se recalculan.",
         "it":"Le categorie che non contano inchiostrano comunque il paese sulla mappa, in una tinta più chiara: nove ore di scalo a Doha compaiono nella tua storia senza far finta che tu abbia visto il Qatar. Cambia categoria più tardi e ogni numero si ricalcola.",
         "de":"Die nicht zählenden Arten färben das Land trotzdem ein, nur heller: neun Stunden Zwischenstopp in Doha erscheinen in deiner Historie, ohne zu behaupten, du hättest Katar gesehen. Ändere die Art später, und alle Zahlen rechnen sich neu.",
         "ro":"Categoriile care nu contează colorează totuși țara pe hartă, într-o nuanță mai deschisă: nouă ore de escală în Doha apar în istoricul tău fără să pretindă că ai văzut Qatarul. Schimbi categoria mai târziu și fiecare cifră se recalculează."}},
  {"h":{"en":"A percentage you can defend","fr":"Un pourcentage défendable","es":"Un porcentaje que puedes defender","it":"Una percentuale che puoi difendere","de":"Ein Prozentsatz, den du verteidigen kannst","ro":"Un procent pe care îl poți susține"},
   "p":{"en":"\"I've done 12% of the world\" only means something if the denominator is stated. Voymark shows both halves of the fraction — countries counted over countries in your chosen definition — so the claim survives being questioned at a dinner table.",
        "fr":"« J'ai fait 12 % du monde » n'a de sens que si le dénominateur est indiqué. Voymark affiche les deux moitiés de la fraction — pays comptés sur pays de la définition choisie — pour que l'affirmation résiste à une question posée à table.",
        "es":"\"He hecho el 12% del mundo\" solo significa algo si se dice el denominador. Voymark muestra las dos mitades de la fracción — países contados sobre países de la definición elegida — para que la afirmación aguante una pregunta en una cena.",
        "it":"\"Ho fatto il 12% del mondo\" significa qualcosa solo se dichiari il denominatore. Voymark mostra entrambe le metà della frazione — paesi contati su paesi della definizione scelta — così l'affermazione regge a una domanda a tavola.",
        "de":"\"Ich habe 12 % der Welt gesehen\" heißt nur etwas, wenn der Nenner dabeisteht. Voymark zeigt beide Hälften des Bruchs — gezählte Länder über Länder deiner gewählten Definition —, damit die Aussage eine Nachfrage beim Abendessen übersteht.",
        "ro":"„Am făcut 12% din lume\" înseamnă ceva doar dacă spui și numitorul. Voymark arată ambele jumătăți ale fracției — țări numărate din țările definiției alese — ca afirmația să reziste la o întrebare pusă la masă."},
   "p2":{"en":"The same honesty runs through the continents: seven rows, each with its own fraction, and a setting for where you put the countries that sit on two of them. Nothing rounds in your favour without telling you.",
         "fr":"La même honnêteté traverse les continents : sept lignes, chacune avec sa fraction, et un réglage pour placer les pays à cheval sur deux d'entre eux. Rien n'arrondit en votre faveur sans le dire.",
         "es":"La misma honestidad recorre los continentes: siete filas, cada una con su fracción, y un ajuste para colocar los países que están en dos. Nada redondea a tu favor sin decírtelo.",
         "it":"La stessa onestà attraversa i continenti: sette righe, ciascuna con la sua frazione, e un'impostazione per collocare i paesi che stanno su due. Niente arrotonda a tuo favore senza dirtelo.",
         "de":"Dieselbe Ehrlichkeit zieht sich durch die Kontinente: sieben Zeilen, jede mit eigenem Bruch, und eine Einstellung für Länder, die auf zweien liegen. Nichts rundet zu deinen Gunsten, ohne es zu sagen.",
         "ro":"Aceeași onestitate străbate continentele: șapte rânduri, fiecare cu fracția lui, și o setare pentru țările care stau pe două dintre ele. Nimic nu rotunjește în favoarea ta fără să-ți spună."}},
 ],
 "faq": [
  {"q":{"en":"How many countries are there in the world?","fr":"Combien y a-t-il de pays dans le monde ?","es":"¿Cuántos países hay en el mundo?","it":"Quanti paesi ci sono nel mondo?","de":"Wie viele Länder gibt es auf der Welt?","ro":"Câte țări sunt în lume?"},
   "a":{"en":"There is no single answer. The travellers' list is 197 — the 193 UN member states plus the two observers and two widely recognized states. The ISO country code standard lists 249 entries including territories. Voymark supports all three.",
        "fr":"Il n'y a pas de réponse unique. La liste des voyageurs en compte 197 — les 193 États membres de l'ONU, plus deux observateurs et deux États largement reconnus. La norme ISO des codes pays en recense 249, territoires compris. Voymark prend en charge les trois.",
        "es":"No hay una única respuesta. La lista de los viajeros son 197 — los 193 estados miembros de la ONU más dos observadores y dos estados ampliamente reconocidos. La norma ISO de códigos de país recoge 249 entradas, territorios incluidos. Voymark admite las tres.",
        "it":"Non c'è una risposta sola. La lista dei viaggiatori è 197 — i 193 stati membri ONU più due osservatori e due stati ampiamente riconosciuti. Lo standard ISO dei codici paese elenca 249 voci, territori compresi. Voymark supporta tutte e tre.",
        "de":"Es gibt keine einzelne Antwort. Die Reisendenliste hat 197 — die 193 UN-Mitgliedstaaten plus zwei Beobachter und zwei weithin anerkannte Staaten. Der ISO-Ländercode-Standard führt 249 Einträge inklusive Territorien. Voymark unterstützt alle drei.",
        "ro":"Nu există un singur răspuns. Lista călătorilor are 197 — cele 193 de state membre ONU plus doi observatori și două state larg recunoscute. Standardul ISO al codurilor de țară listează 249 de intrări, teritorii incluse. Voymark le suportă pe toate trei."}},
  {"q":{"en":"Does a layover count as visiting a country?","fr":"Une escale compte-t-elle comme une visite ?","es":"¿Una escala cuenta como visitar un país?","it":"Uno scalo conta come visita?","de":"Zählt ein Zwischenstopp als Länderbesuch?","ro":"Contează o escală ca vizitarea unei țări?"},
   "a":{"en":"Most seasoned travellers say no, and Voymark's default agrees: airport-only and transit ink the map without adding to your count. But it is a setting, not a verdict — if leaving the terminal counts for you, mark it as visited and the number follows.",
        "fr":"La plupart des voyageurs aguerris disent non, et le réglage par défaut de Voymark aussi : aéroport seul et transit encrent la carte sans gonfler le compte. Mais c'est un réglage, pas un verdict — si sortir du terminal compte pour vous, marquez visité et le nombre suit.",
        "es":"La mayoría de los viajeros veteranos dice que no, y el ajuste por defecto de Voymark coincide: solo aeropuerto y tránsito entintan el mapa sin sumar. Pero es un ajuste, no un veredicto — si salir de la terminal cuenta para ti, márcalo como visitado y el número te sigue.",
        "it":"La maggior parte dei viaggiatori esperti dice di no, e il default di Voymark è d'accordo: solo aeroporto e transito inchiostrano la mappa senza sommare. Ma è un'impostazione, non una sentenza — se per te uscire dal terminal conta, segnalo come visitato e il numero ti segue.",
        "de":"Die meisten erfahrenen Reisenden sagen nein, und Voymarks Voreinstellung stimmt zu: Nur-Flughafen und Transit färben die Karte, ohne mitzuzählen. Aber das ist eine Einstellung, kein Urteil — wenn für dich zählt, das Terminal verlassen zu haben, markiere besucht, und die Zahl folgt.",
        "ro":"Majoritatea călătorilor experimentați spun nu, iar setarea implicită din Voymark e de acord: doar aeroport și tranzit colorează harta fără să adauge la numărătoare. Dar este o setare, nu o sentință — dacă pentru tine contează ieșirea din terminal, marchează vizitat și cifra te urmează."}},
  {"q":{"en":"Can I change the counting rule later?","fr":"Puis-je changer la règle de comptage plus tard ?","es":"¿Puedo cambiar la regla de recuento después?","it":"Posso cambiare la regola di conteggio dopo?","de":"Kann ich die Zählregel später ändern?","ro":"Pot schimba regula de numărare mai târziu?"},
   "a":{"en":"Yes, at any time, and nothing is lost. The rule is a lens over the same records, so switching from 197 to 193 changes every total, percentage, continent row and seal at once — and switching back restores exactly what you had.",
        "fr":"Oui, à tout moment, sans rien perdre. La règle est une lentille posée sur les mêmes données : passer de 197 à 193 change d'un coup tous les totaux, pourcentages, lignes de continent et sceaux — et revenir en arrière restitue exactement l'état précédent.",
        "es":"Sí, cuando quieras, y no se pierde nada. La regla es una lente sobre los mismos registros: pasar de 197 a 193 cambia de golpe todos los totales, porcentajes, filas de continente y sellos — y volver atrás restaura exactamente lo que tenías.",
        "it":"Sì, quando vuoi, e non si perde nulla. La regola è una lente sugli stessi dati: passare da 197 a 193 cambia in un colpo totali, percentuali, righe dei continenti e sigilli — e tornare indietro ripristina esattamente ciò che avevi.",
        "de":"Ja, jederzeit, und nichts geht verloren. Die Regel ist eine Linse über denselben Daten: von 197 auf 193 zu wechseln ändert auf einen Schlag alle Summen, Prozente, Kontinentzeilen und Siegel — und zurückwechseln stellt genau den alten Stand her.",
        "ro":"Da, oricând, și nu se pierde nimic. Regula este o lentilă peste aceleași date: trecerea de la 197 la 193 schimbă dintr-odată toate totalurile, procentele, rândurile pe continente și sigiliile — iar întoarcerea readuce exact ce aveai."}},
  {"q":{"en":"How does it count countries I have lived in?","fr":"Comment compte-t-il les pays où j'ai vécu ?","es":"¿Cómo cuenta los países donde he vivido?","it":"Come conta i paesi in cui ho vissuto?","de":"Wie zählt es Länder, in denen ich gelebt habe?","ro":"Cum numără țările în care am locuit?"},
   "a":{"en":"\"Lived there\" is its own visit kind and counts like a visit, but stays distinguishable in your history — so a year in Berlin never reads as a weekend. The home area you set is separately excluded from photo scanning, so everyday photos never invent trips.",
        "fr":"« Vécu » est une catégorie à part entière : elle compte comme une visite mais reste distincte dans votre historique — une année à Berlin ne se lit jamais comme un week-end. La zone de domicile que vous définissez est par ailleurs exclue du scan photo, pour que le quotidien n'invente pas de voyages.",
        "es":"\"Vivido\" es una categoría propia: cuenta como visita pero sigue distinguiéndose en tu historial — un año en Berlín nunca se lee como un fin de semana. Además, la zona de casa que definas queda excluida del escaneo de fotos, para que lo cotidiano no invente viajes.",
        "it":"\"Vissuto\" è una categoria a sé: conta come visita ma resta distinguibile nella tua storia — un anno a Berlino non si legge mai come un weekend. L'area di casa che imposti è inoltre esclusa dalla scansione foto, così la quotidianità non inventa viaggi.",
        "de":"\"Gelebt\" ist eine eigene Besuchsart: Sie zählt wie ein Besuch, bleibt in deiner Historie aber unterscheidbar — ein Jahr in Berlin liest sich nie wie ein Wochenende. Der von dir gesetzte Heimatbereich wird zudem vom Foto-Scan ausgenommen, damit Alltag keine Reisen erfindet.",
        "ro":"„Locuit\" este o categorie de sine stătătoare: contează ca vizită, dar rămâne distinctă în istoricul tău — un an la Berlin nu se citește niciodată ca un weekend. În plus, zona de acasă pe care o setezi e exclusă din scanarea pozelor, ca rutina să nu inventeze călătorii."}},
  {"q":{"en":"Is there a leaderboard or a social feed?","fr":"Y a-t-il un classement ou un fil social ?","es":"¿Hay clasificación o feed social?","it":"C'è una classifica o un feed social?","de":"Gibt es eine Rangliste oder einen Social Feed?","ro":"Există un clasament sau un flux social?"},
   "a":{"en":"None. There is no ranking, no follower count and no feed, because there is no server to host one. If you want to compare, you can exchange a passport with a friend directly — by QR code or a file — and see the overlap side by side.",
        "fr":"Aucun. Pas de classement, pas d'abonnés, pas de fil, car aucun serveur ne pourrait l'héberger. Pour comparer, échangez un passeport avec un ami en direct — par QR code ou par fichier — et voyez le recoupement côte à côte.",
        "es":"Ninguno. No hay ranking, ni seguidores, ni feed, porque no hay servidor que lo aloje. Si quieres comparar, intercambia un pasaporte con un amigo directamente — por código QR o por archivo — y ved la coincidencia lado a lado.",
        "it":"Nessuno. Niente classifica, niente follower, niente feed, perché non c'è un server che possa ospitarli. Se vuoi confrontare, scambia un passaporto con un amico direttamente — con un codice QR o un file — e guardate la sovrapposizione affiancata.",
        "de":"Gar keine. Keine Rangliste, keine Follower, kein Feed — es gibt keinen Server, der so etwas hosten könnte. Zum Vergleichen tauschst du direkt einen Reisepass mit Freunden aus — per QR-Code oder Datei — und seht die Schnittmenge nebeneinander.",
        "ro":"Niciunul. Nu există clasament, nu există urmăritori, nu există flux, pentru că nu există server care să le găzduiască. Dacă vrei să compari, schimbă un pașaport cu un prieten direct — prin cod QR sau printr-un fișier — și vedeți suprapunerea una lângă alta."}},
 ],
},

"travel-photos-to-trips": {
 "nav": {"en":"Photos → trips","fr":"Photos → voyages","es":"Fotos → viajes","it":"Foto → viaggi","de":"Fotos → Reisen","ro":"Poze → călătorii"},
 "title": {
  "en":"Turn Travel Photos into Trips — automatic travel history | Voymark",
  "fr":"Transformez vos photos de voyage en voyages — historique automatique | Voymark",
  "es":"Convierte tus fotos de viaje en viajes — historial automático | Voymark",
  "it":"Trasforma le foto di viaggio in viaggi — cronologia automatica | Voymark",
  "de":"Verwandle Reisefotos in Reisen — automatische Reisegeschichte | Voymark",
  "ro":"Transformă pozele de călătorie în călătorii — istoric automat | Voymark"},
 "meta": {
  "en":"Voymark reconstructs your travel history from the photos already on your phone — trips, places and country stamps, detected entirely on-device. Nothing is uploaded, ever.",
  "fr":"Voymark reconstruit votre historique de voyage à partir des photos déjà sur votre téléphone — voyages, lieux et tampons de pays, détectés entièrement sur l'appareil. Rien n'est jamais envoyé.",
  "es":"Voymark reconstruye tu historial de viajes a partir de las fotos que ya están en tu teléfono — viajes, lugares y sellos de países, detectados por completo en el dispositivo. Nunca se sube nada.",
  "it":"Voymark ricostruisce la tua storia di viaggio dalle foto già sul tuo telefono — viaggi, luoghi e timbri dei paesi, rilevati interamente sul dispositivo. Nulla viene mai caricato.",
  "de":"Voymark rekonstruiert deine Reisegeschichte aus den Fotos, die schon auf deinem Handy sind — Reisen, Orte und Länderstempel, vollständig auf dem Gerät erkannt. Nichts wird je hochgeladen.",
  "ro":"Voymark îți reconstruiește istoria de călătorie din pozele aflate deja pe telefon — călătorii, locuri și ștampile de țări, detectate în întregime pe dispozitiv. Nimic nu este încărcat, niciodată."},
 "h1": {
  "en":"Your photos already know where you've been","fr":"Vos photos savent déjà où vous êtes allé",
  "es":"Tus fotos ya saben dónde has estado","it":"Le tue foto sanno già dove sei stato",
  "de":"Deine Fotos wissen längst, wo du warst","ro":"Pozele tale știu deja unde ai fost"},
 "lede": {
  "en":"Years of travel are sitting in your photo library. Voymark reads their places and dates — on your device only — and turns them into trips, places and passport stamps you can review before anything is saved.",
  "fr":"Des années de voyage dorment dans votre photothèque. Voymark lit leurs lieux et leurs dates — uniquement sur votre appareil — et les transforme en voyages, lieux et tampons de passeport que vous validez avant tout enregistrement.",
  "es":"Años de viajes descansan en tu biblioteca de fotos. Voymark lee sus lugares y fechas — solo en tu dispositivo — y los convierte en viajes, lugares y sellos de pasaporte que revisas antes de guardar nada.",
  "it":"Anni di viaggi riposano nella tua libreria fotografica. Voymark ne legge luoghi e date — solo sul tuo dispositivo — e li trasforma in viaggi, luoghi e timbri del passaporto che rivedi prima che qualcosa venga salvato.",
  "de":"Jahre voller Reisen liegen in deiner Fotobibliothek. Voymark liest ihre Orte und Daten — nur auf deinem Gerät — und macht daraus Reisen, Orte und Pass-Stempel, die du prüfst, bevor irgendetwas gespeichert wird.",
  "ro":"Ani întregi de călătorii stau în biblioteca ta foto. Voymark le citește locurile și datele — doar pe dispozitivul tău — și le transformă în călătorii, locuri și ștampile de pașaport pe care le revizuiești înainte ca ceva să fie salvat."},
 "sections": [
  {"h":{"en":"You stay in charge","fr":"Vous gardez la main","es":"Tú mandas","it":"Comandi tu","de":"Du behältst die Kontrolle","ro":"Tu rămâi la comandă"},
   "p":{"en":"Every detected trip appears for review first: rename it, split it, merge candidates, or skip it. Photos join your manually created trips only when you approve it — and a skip is remembered forever.",
        "fr":"Chaque voyage détecté apparaît d'abord pour relecture : renommez-le, scindez-le, fusionnez des candidats, ou ignorez-le. Les photos ne rejoignent vos voyages créés à la main que si vous l'approuvez — et un refus est retenu pour toujours.",
        "es":"Cada viaje detectado aparece primero para revisión: renómbralo, divídelo, fusiona candidatos o descártalo. Las fotos solo se unen a tus viajes manuales si lo apruebas — y un descarte se recuerda para siempre.",
        "it":"Ogni viaggio rilevato appare prima in revisione: rinominalo, dividilo, unisci candidati o saltalo. Le foto si aggiungono ai viaggi creati a mano solo se lo approvi — e uno salto viene ricordato per sempre.",
        "de":"Jede erkannte Reise erscheint zuerst zur Prüfung: umbenennen, teilen, Kandidaten zusammenführen oder überspringen. Fotos kommen nur mit deiner Zustimmung zu handgemachten Reisen — und ein Überspringen wird für immer gemerkt.",
        "ro":"Fiecare călătorie detectată apare mai întâi la revizuire: redenumește-o, împarte-o, unește candidați sau omite-o. Pozele se alătură călătoriilor tale manuale doar cu aprobarea ta — iar o omitere este ținută minte pentru totdeauna."}},
  {"h":{"en":"Scan a year, or everything","fr":"Analysez une année, ou tout","es":"Escanea un año, o todo","it":"Scansiona un anno, o tutto","de":"Scanne ein Jahr — oder alles","ro":"Scanează un an, sau tot"},
   "p":{"en":"Scan your whole library, the past year, everything since last time, or any custom period — one era at a time. Your confirmed home area is excluded, so everyday photos never become \"trips\".",
        "fr":"Analysez toute votre photothèque, l'année écoulée, tout depuis la dernière fois, ou n'importe quelle période — une époque à la fois. Votre zone de domicile confirmée est exclue : les photos du quotidien ne deviennent jamais des « voyages ».",
        "es":"Escanea toda tu biblioteca, el último año, todo desde la última vez o cualquier periodo — una época a la vez. Tu zona de casa confirmada queda excluida: las fotos cotidianas nunca se convierten en \"viajes\".",
        "it":"Scansiona tutta la libreria, l'ultimo anno, tutto dall'ultima volta o qualsiasi periodo — un'epoca alla volta. La tua zona di casa confermata è esclusa: le foto quotidiane non diventano mai \"viaggi\".",
        "de":"Scanne die ganze Bibliothek, das letzte Jahr, alles seit dem letzten Mal oder einen beliebigen Zeitraum — eine Ära nach der anderen. Dein bestätigter Heimatbereich ist ausgenommen: Alltagsfotos werden nie zu \"Reisen\".",
        "ro":"Scanează toată biblioteca, ultimul an, tot ce e nou de data trecută sau orice perioadă — o epocă pe rând. Zona ta de acasă confirmată este exclusă: pozele de zi cu zi nu devin niciodată \"călătorii\"."}},
  {"h":{"en":"On-device, provably","fr":"Sur l'appareil, vérifiable","es":"En el dispositivo, comprobable","it":"Sul dispositivo, dimostrabile","de":"Auf dem Gerät, nachweisbar","ro":"Pe dispozitiv, demonstrabil"},
   "p":{"en":"The scan works in airplane mode — that's the whole point. Locations and dates are read on your phone, images are never copied or uploaded, and revoking photo access takes one switch in system settings.",
        "fr":"L'analyse fonctionne en mode avion — c'est tout l'intérêt. Lieux et dates sont lus sur votre téléphone, les images ne sont jamais copiées ni envoyées, et révoquer l'accès aux photos ne prend qu'un interrupteur dans les réglages.",
        "es":"El escaneo funciona en modo avión — de eso se trata. Ubicaciones y fechas se leen en tu teléfono, las imágenes nunca se copian ni se suben, y revocar el acceso a fotos es un interruptor en los ajustes.",
        "it":"La scansione funziona in modalità aereo — è proprio questo il punto. Luoghi e date si leggono sul telefono, le immagini non vengono mai copiate né caricate, e revocare l'accesso alle foto è un interruttore nelle impostazioni.",
        "de":"Der Scan funktioniert im Flugmodus — genau darum geht es. Orte und Daten werden auf deinem Handy gelesen, Bilder nie kopiert oder hochgeladen, und der Fotozugriff lässt sich mit einem Schalter in den Einstellungen widerrufen.",
        "ro":"Scanarea funcționează în modul avion — exact asta e ideea. Locațiile și datele se citesc pe telefonul tău, imaginile nu sunt niciodată copiate sau încărcate, iar accesul la poze se revocă dintr-un comutator în setări."}},
  {"h": {"en":"Photos that aren't in your library","fr":"Les photos qui ne sont pas dans votre photothèque","es":"Fotos que no están en tu fototeca","it":"Le foto che non sono nella tua libreria","de":"Fotos, die nicht in deiner Mediathek liegen","ro":"Pozele care nu sunt în galeria ta"},
   "p": {
        "en":"Old trips are often on a memory card, an external drive or in a restored backup folder rather than in the phone's photo library. Voymark can scan a folder too, reading the same locations and dates and proposing the same reviewable trips — so the decade before this phone isn't lost to it.",
        "fr":"Les anciens voyages sont souvent sur une carte mémoire, un disque externe ou dans un dossier de sauvegarde restauré plutôt que dans la photothèque du téléphone. Voymark peut aussi analyser un dossier, en lisant les mêmes lieux et dates et en proposant les mêmes voyages à valider — pour que la décennie d'avant ce téléphone ne soit pas perdue.",
        "es":"Los viajes antiguos suelen estar en una tarjeta de memoria, un disco externo o una carpeta de copia restaurada, no en la fototeca del teléfono. Voymark también puede escanear una carpeta, leyendo las mismas ubicaciones y fechas y proponiendo los mismos viajes para revisar — así la década anterior a este teléfono no se pierde.",
        "it":"I viaggi vecchi stanno spesso su una scheda di memoria, un disco esterno o in una cartella di backup ripristinata, non nella libreria foto del telefono. Voymark può analizzare anche una cartella, leggendo le stesse posizioni e date e proponendo gli stessi viaggi da rivedere — così il decennio prima di questo telefono non va perso.",
        "de":"Alte Reisen liegen oft auf einer Speicherkarte, einer externen Platte oder in einem wiederhergestellten Backup-Ordner statt in der Fotomediathek des Handys. Voymark kann auch einen Ordner durchsuchen, liest dieselben Orte und Daten und schlägt dieselben prüfbaren Reisen vor — damit das Jahrzehnt vor diesem Handy nicht verloren geht.",
        "ro":"Călătoriile vechi stau adesea pe un card de memorie, pe un disc extern sau într-un folder de backup restaurat, nu în galeria telefonului. Voymark poate scana și un folder, citind aceleași locații și date și propunând aceleași călătorii de verificat — ca deceniul dinaintea acestui telefon să nu se piardă."}},
  {"h":{"en":"How a pile of photos becomes a trip","fr":"Comment un tas de photos devient un voyage","es":"Cómo un montón de fotos se convierte en un viaje","it":"Come un mucchio di foto diventa un viaggio","de":"Wie aus einem Fotostapel eine Reise wird","ro":"Cum devine un morman de poze o călătorie"},
   "p":{"en":"Photos taken near each other on the same day become a stop. Stops on consecutive days become a trip, and a gap of more than two days ends it — so a summer with three holidays comes back as three trips, not one long blur.",
        "fr":"Les photos prises près les unes des autres le même jour deviennent une étape. Les étapes de jours consécutifs forment un voyage, et un écart de plus de deux jours y met fin : un été à trois vacances revient en trois voyages, pas en une longue bouillie.",
        "es":"Las fotos hechas cerca unas de otras el mismo día forman una parada. Las paradas de días consecutivos forman un viaje, y un hueco de más de dos días lo cierra: un verano con tres vacaciones vuelve como tres viajes, no como una única mancha larga.",
        "it":"Le foto scattate vicine tra loro nello stesso giorno diventano una tappa. Le tappe di giorni consecutivi diventano un viaggio, e un intervallo di più di due giorni lo chiude: un'estate con tre vacanze torna come tre viaggi, non come un unico blocco confuso.",
        "de":"Fotos, die am selben Tag nah beieinander entstanden, werden zu einem Halt. Halte an aufeinanderfolgenden Tagen werden zu einer Reise, und eine Lücke von mehr als zwei Tagen beendet sie — ein Sommer mit drei Urlauben kommt als drei Reisen zurück, nicht als ein langer Brei.",
        "ro":"Pozele făcute aproape una de alta în aceeași zi devin o oprire. Opririle din zile consecutive devin o călătorie, iar o pauză de peste două zile o încheie: o vară cu trei vacanțe se întoarce ca trei călătorii, nu ca o singură pată lungă."},
   "p2":{"en":"Each stop is then named by your phone's own geocoder, preferring the city over the district — so a day in Rome reads \"Rome\", not \"Municipio I\". A trip needs at least three geotagged photos to exist at all, which is what stops a stray airport snapshot from becoming a journey.",
         "fr":"Chaque étape est ensuite nommée par le géocodeur du téléphone, qui préfère la ville au quartier : une journée à Rome se lit « Rome », pas « Municipio I ». Un voyage exige au moins trois photos géolocalisées pour exister, ce qui empêche un cliché d'aéroport isolé de devenir une expédition.",
         "es":"Cada parada la nombra el geocodificador del propio móvil, que prefiere la ciudad al distrito: un día en Roma se lee \"Roma\", no \"Municipio I\". Un viaje necesita al menos tres fotos geolocalizadas para existir, y eso evita que una foto suelta de aeropuerto se convierta en una travesía.",
         "it":"Ogni tappa viene poi nominata dal geocoder del telefono, che preferisce la città al quartiere: una giornata a Roma si legge \"Roma\", non \"Municipio I\". Un viaggio ha bisogno di almeno tre foto geolocalizzate per esistere, ed è questo che impedisce a uno scatto sperduto in aeroporto di diventare una spedizione.",
         "de":"Jeden Halt benennt dann der Geocoder des Telefons, der die Stadt dem Bezirk vorzieht: ein Tag in Rom liest sich \"Rom\", nicht \"Municipio I\". Eine Reise braucht mindestens drei Fotos mit Koordinaten, um überhaupt zu existieren — das verhindert, dass ein verirrter Flughafenschnappschuss zur Expedition wird.",
         "ro":"Fiecare oprire e apoi numită de geocoderul telefonului, care preferă orașul cartierului: o zi la Roma se citește „Roma\", nu „Municipio I\". O călătorie are nevoie de cel puțin trei poze cu locație ca să existe, iar asta oprește o poză răzleață de aeroport să devină o expediție."}},
  {"h":{"en":"What the app never does with your photos","fr":"Ce que l'app ne fait jamais de vos photos","es":"Lo que la app nunca hace con tus fotos","it":"Cosa l'app non fa mai con le tue foto","de":"Was die App mit deinen Fotos nie tut","ro":"Ce nu face niciodată aplicația cu pozele tale"},
   "p":{"en":"It does not copy them, does not upload them and does not send them anywhere for analysis. There is no image recognition, no face detection and no cloud step: the only thing read is the coordinate and the timestamp already written into the file by your camera.",
        "fr":"Elle ne les copie pas, ne les téléverse pas et ne les envoie nulle part pour analyse. Pas de reconnaissance d'image, pas de détection de visages, aucune étape dans le cloud : seules sont lues les coordonnées et la date déjà inscrites dans le fichier par votre appareil.",
        "es":"No las copia, no las sube y no las envía a ningún sitio para analizarlas. No hay reconocimiento de imagen, ni detección de caras, ni paso por la nube: lo único que se lee son las coordenadas y la fecha que tu cámara ya escribió en el archivo.",
        "it":"Non le copia, non le carica e non le manda da nessuna parte per l'analisi. Nessun riconoscimento di immagini, nessun rilevamento dei volti, nessun passaggio nel cloud: si leggono solo le coordinate e la data che la tua fotocamera ha già scritto nel file.",
        "de":"Sie kopiert sie nicht, lädt sie nicht hoch und schickt sie nirgends zur Analyse. Keine Bilderkennung, keine Gesichtserkennung, kein Cloud-Schritt: gelesen werden nur Koordinate und Zeitstempel, die deine Kamera ohnehin in die Datei geschrieben hat.",
        "ro":"Nu le copiază, nu le încarcă și nu le trimite nicăieri pentru analiză. Nu există recunoaștere de imagini, nu există detecție de fețe, nu există pas prin cloud: se citesc doar coordonatele și data pe care camera ta le-a scris deja în fișier."},
   "p2":{"en":"Photos you attach to a trip are stored as references, not duplicates, so nothing doubles your storage. Delete a photo from your library and Voymark notices the reference has gone stale and offers to clean it up.",
         "fr":"Les photos attachées à un voyage sont stockées comme références, pas comme copies : rien ne double votre espace. Supprimez une photo de votre photothèque et Voymark remarque que la référence est morte et propose de faire le ménage.",
         "es":"Las fotos que adjuntas a un viaje se guardan como referencias, no como copias, así que nada duplica tu almacenamiento. Borra una foto de tu galería y Voymark detecta que la referencia quedó huérfana y ofrece limpiarla.",
         "it":"Le foto che alleghi a un viaggio sono salvate come riferimenti, non come copie: nulla raddoppia il tuo spazio. Elimina una foto dalla libreria e Voymark si accorge che il riferimento è morto e propone di ripulirlo.",
         "de":"An eine Reise angehängte Fotos werden als Verweise gespeichert, nicht als Kopien — nichts verdoppelt deinen Speicher. Löschst du ein Foto aus der Mediathek, merkt Voymark, dass der Verweis ins Leere zeigt, und bietet an, ihn aufzuräumen.",
         "ro":"Pozele pe care le atașezi unei călătorii sunt salvate ca referințe, nu ca dubluri, așa că nimic nu-ți dublează spațiul. Șterge o poză din galerie și Voymark observă că referința a rămas fără țintă și îți propune să o curețe."}},
 ],
 "faq": [
  {"q":{"en":"Do my photos get uploaded anywhere?","fr":"Mes photos sont-elles envoyées quelque part ?","es":"¿Mis fotos se suben a algún sitio?","it":"Le mie foto vengono caricate da qualche parte?","de":"Werden meine Fotos irgendwohin hochgeladen?","ro":"Pozele mele se încarcă undeva?"},
   "a":{"en":"No. The scan runs entirely on the phone and works with the network switched off — try it in airplane mode. Images are never copied out of your library, and the app has no server to send them to even if it wanted one.",
        "fr":"Non. L'analyse tourne entièrement sur le téléphone et fonctionne réseau coupé — essayez en mode avion. Les images ne quittent jamais votre photothèque, et l'application n'a aucun serveur où les envoyer, même si elle le voulait.",
        "es":"No. El escaneo funciona íntegramente en el móvil y va con la red apagada — pruébalo en modo avión. Las imágenes nunca salen de tu galería, y la app no tiene ningún servidor al que mandarlas aunque quisiera.",
        "it":"No. La scansione gira interamente sul telefono e funziona con la rete spenta — provala in modalità aereo. Le immagini non escono mai dalla tua libreria, e l'app non ha alcun server a cui mandarle nemmeno volendo.",
        "de":"Nein. Der Scan läuft vollständig auf dem Telefon und funktioniert ohne Netz — probier es im Flugmodus. Bilder verlassen deine Mediathek nie, und die App hätte gar keinen Server, an den sie sie schicken könnte.",
        "ro":"Nu. Scanarea rulează integral pe telefon și merge cu rețeaua oprită — încearcă în modul avion. Imaginile nu ies niciodată din galeria ta, iar aplicația nu are niciun server către care să le trimită, chiar dacă ar vrea."}},
  {"q":{"en":"What if my photos have no location data?","fr":"Et si mes photos n'ont pas de données de localisation ?","es":"¿Y si mis fotos no tienen datos de ubicación?","it":"E se le mie foto non hanno dati di posizione?","de":"Und wenn meine Fotos keine Standortdaten haben?","ro":"Dacă pozele mele nu au date de locație?"},
   "a":{"en":"Then they are simply skipped — nothing is guessed. You can still build those trips by hand and attach the photos afterwards, which takes seconds and keeps the dates and places exactly as you remember them.",
        "fr":"Elles sont simplement ignorées — rien n'est deviné. Vous pouvez toujours créer ces voyages à la main et y attacher les photos ensuite : quelques secondes, et les dates et lieux restent exactement ceux dont vous vous souvenez.",
        "es":"Entonces se omiten sin más — no se adivina nada. Puedes crear esos viajes a mano y adjuntar las fotos después: son segundos, y las fechas y lugares quedan tal y como los recuerdas.",
        "it":"Vengono semplicemente saltate — non si indovina nulla. Puoi comunque creare quei viaggi a mano e allegare le foto dopo: pochi secondi, e date e luoghi restano esattamente come li ricordi.",
        "de":"Dann werden sie schlicht übersprungen — es wird nichts geraten. Du kannst solche Reisen weiterhin von Hand anlegen und die Fotos danach anhängen: Sekundensache, und Daten wie Orte bleiben genau so, wie du sie erinnerst.",
        "ro":"Atunci sunt pur și simplu sărite — nu se ghicește nimic. Poți construi acele călătorii manual și atașa pozele după aceea: durează secunde, iar datele și locurile rămân exact cum ți le amintești."}},
  {"q":{"en":"Will it turn my everyday photos into trips?","fr":"Va-t-il transformer mes photos du quotidien en voyages ?","es":"¿Convertirá mis fotos cotidianas en viajes?","it":"Trasformerà le mie foto di tutti i giorni in viaggi?","de":"Macht es aus Alltagsfotos Reisen?","ro":"Îmi va transforma pozele de zi cu zi în călătorii?"},
   "a":{"en":"Set your home area once and everything within 25 km of it is excluded from detection. Voymark never guesses where you live — if you skip that step, nothing is treated as home rather than something being assumed.",
        "fr":"Définissez une fois votre zone de domicile et tout ce qui se trouve dans un rayon de 25 km en est exclu. Voymark ne devine jamais où vous habitez : si vous sautez cette étape, rien n'est considéré comme domicile plutôt que supposé.",
        "es":"Define tu zona de casa una vez y todo lo que esté a menos de 25 km queda excluido de la detección. Voymark nunca adivina dónde vives: si te saltas ese paso, no se considera nada como casa en vez de suponerlo.",
        "it":"Imposta una volta la tua area di casa e tutto ciò che si trova entro 25 km ne resta escluso. Voymark non indovina mai dove abiti: se salti quel passaggio, niente viene considerato casa invece di essere presunto.",
        "de":"Lege deinen Heimatbereich einmal fest, und alles im Umkreis von 25 km fällt aus der Erkennung heraus. Voymark rät nie, wo du wohnst — überspringst du den Schritt, gilt lieber gar nichts als Zuhause, statt etwas anzunehmen.",
        "ro":"Setează o dată zona de acasă și tot ce se află pe o rază de 25 km este exclus din detecție. Voymark nu ghicește niciodată unde locuiești: dacă sari peste pasul acela, nimic nu e tratat drept acasă, în loc să se presupună ceva."}},
  {"q":{"en":"Can I undo an import?","fr":"Puis-je annuler un import ?","es":"¿Puedo deshacer una importación?","it":"Posso annullare un'importazione?","de":"Kann ich einen Import rückgängig machen?","ro":"Pot anula un import?"},
   "a":{"en":"Nothing is written until you accept it, and anything accepted can be edited or deleted afterwards. A candidate you skip is remembered as skipped, so the next scan does not offer it again.",
        "fr":"Rien n'est écrit avant votre accord, et tout ce qui est accepté peut ensuite être modifié ou supprimé. Une proposition ignorée est mémorisée comme telle : le prochain scan ne la reproposera pas.",
        "es":"No se escribe nada hasta que lo aceptas, y todo lo aceptado se puede editar o borrar después. Un candidato que descartas queda recordado como descartado, así que el siguiente escaneo no vuelve a ofrecerlo.",
        "it":"Non viene scritto nulla finché non accetti, e tutto ciò che accetti può essere modificato o eliminato dopo. Una proposta che salti resta memorizzata come saltata, così la scansione successiva non te la ripropone.",
        "de":"Nichts wird geschrieben, bevor du zustimmst, und alles Zugestimmte lässt sich danach ändern oder löschen. Ein übersprungener Vorschlag wird als übersprungen gemerkt — der nächste Scan bietet ihn nicht erneut an.",
        "ro":"Nu se scrie nimic până nu accepți, iar orice ai acceptat poate fi editat sau șters după aceea. O propunere pe care o sari e ținută minte ca sărită, așa că scanarea următoare nu ți-o mai oferă."}},
  {"q":{"en":"How far back can it go?","fr":"Jusqu'où peut-il remonter ?","es":"¿Hasta cuándo puede llegar hacia atrás?","it":"Fin dove può risalire?","de":"Wie weit zurück kommt es?","ro":"Cât de departe poate merge în urmă?"},
   "a":{"en":"As far as your library does. Scan everything at once, the past year, everything since the last scan, or a period you choose. Photos on a memory card, an external drive or a restored backup can be scanned as a folder, so the years before this phone are not lost.",
        "fr":"Aussi loin que votre photothèque. Analysez tout d'un coup, la dernière année, tout depuis le dernier scan, ou une période choisie. Les photos sur carte mémoire, disque externe ou sauvegarde restaurée s'analysent en tant que dossier : les années d'avant ce téléphone ne sont pas perdues.",
        "es":"Tan atrás como llegue tu galería. Escanea todo de golpe, el último año, todo desde el último escaneo o un periodo que elijas. Las fotos en una tarjeta, un disco externo o una copia restaurada se pueden escanear como carpeta, así que los años anteriores a este móvil no se pierden.",
        "it":"Fin dove arriva la tua libreria. Scansiona tutto in una volta, l'ultimo anno, tutto dall'ultima scansione o un periodo che scegli tu. Le foto su scheda di memoria, disco esterno o backup ripristinato si scansionano come cartella: gli anni precedenti a questo telefono non vanno persi.",
        "de":"So weit wie deine Mediathek. Scanne alles auf einmal, das letzte Jahr, alles seit dem letzten Scan oder einen selbst gewählten Zeitraum. Fotos auf Speicherkarte, externer Platte oder in einem wiederhergestellten Backup lassen sich als Ordner scannen — die Jahre vor diesem Telefon sind nicht verloren.",
        "ro":"Cât de departe merge galeria ta. Scanează tot deodată, ultimul an, tot de la ultima scanare sau o perioadă aleasă de tine. Pozele de pe un card, un disc extern sau un backup restaurat se pot scana ca folder, așa că anii dinaintea acestui telefon nu se pierd."}},
 ],
},

"travel-map": {
 "nav": {"en":"Travel map","fr":"Carte de voyage","es":"Mapa de viajes","it":"Mappa di viaggio","de":"Reisekarte","ro":"Hartă de călătorii"},
 "title": {
  "en":"Travel Map — your trips, routes and photos on one world map | Voymark",
  "fr":"Carte de voyage — vos voyages, itinéraires et photos sur une carte du monde | Voymark",
  "es":"Mapa de viajes — tus viajes, rutas y fotos en un mapa del mundo | Voymark",
  "it":"Mappa di viaggio — i tuoi viaggi, itinerari e foto su una mappa del mondo | Voymark",
  "de":"Reisekarte — deine Reisen, Routen und Fotos auf einer Weltkarte | Voymark",
  "ro":"Hartă de călătorii — călătoriile, rutele și pozele tale pe o hartă a lumii | Voymark"},
 "meta": {
  "en":"A personal travel map that shows everywhere you've been: stamped countries, trip routes, marked cities and photo spots — on a beautiful offline world map. No account, free.",
  "fr":"Une carte de voyage personnelle qui montre partout où vous êtes allé : pays tamponnés, itinéraires, villes marquées et lieux de photos — sur une belle carte du monde hors ligne. Sans compte, gratuit.",
  "es":"Un mapa de viajes personal que muestra todos los lugares donde has estado: países sellados, rutas, ciudades marcadas y puntos de fotos — en un precioso mapa del mundo offline. Sin cuenta, gratis.",
  "it":"Una mappa di viaggio personale che mostra ovunque tu sia stato: paesi timbrati, itinerari, città segnate e luoghi delle foto — su una bellissima mappa del mondo offline. Senza account, gratis.",
  "de":"Eine persönliche Reisekarte, die zeigt, wo du überall warst: gestempelte Länder, Reiserouten, markierte Städte und Foto-Orte — auf einer schönen Offline-Weltkarte. Ohne Konto, kostenlos.",
  "ro":"O hartă de călătorii personală care arată peste tot pe unde ai fost: țări ștampilate, rute, orașe marcate și locuri cu poze — pe o hartă a lumii frumoasă și offline. Fără cont, gratuit."},
 "h1": {
  "en":"Your whole travel story, on one map","fr":"Toute votre histoire de voyage, sur une carte",
  "es":"Toda tu historia viajera, en un mapa","it":"Tutta la tua storia di viaggio, su una mappa",
  "de":"Deine ganze Reisegeschichte auf einer Karte","ro":"Toată povestea ta de călătorie, pe o hartă"},
 "lede": {
  "en":"Countries fill in burgundy, routes trace each trip, gold dots mark where photos were taken. Pinch from the whole world down to a single city — all offline.",
  "fr":"Les pays se remplissent de bordeaux, les itinéraires tracent chaque voyage, des points dorés marquent vos photos. Pincez du monde entier jusqu'à une seule ville — tout hors ligne.",
  "es":"Los países se llenan de burdeos, las rutas trazan cada viaje, puntos dorados marcan tus fotos. Haz zoom del mundo entero a una sola ciudad — todo offline.",
  "it":"I paesi si riempiono di bordeaux, le rotte tracciano ogni viaggio, punti dorati segnano le tue foto. Dal mondo intero a una singola città con un gesto — tutto offline.",
  "de":"Länder füllen sich burgunderrot, Routen zeichnen jede Reise nach, goldene Punkte markieren deine Fotos. Zoome von der ganzen Welt bis zu einer einzelnen Stadt — alles offline.",
  "ro":"Țările se umplu de burgundy, rutele trasează fiecare călătorie, puncte aurii marchează pozele tale. Din întreaga lume până la un singur oraș — totul offline."},
 "sections": [
  {"h":{"en":"More than pins on a map","fr":"Plus que des épingles sur une carte","es":"Más que alfileres en un mapa","it":"Più che puntine su una mappa","de":"Mehr als Nadeln auf einer Karte","ro":"Mai mult decât piuneze pe o hartă"},
   "p":{"en":"A travel map should remember journeys, not just places. Voymark layers your stamped countries, every trip's route, the cities you've marked and the spots where your photos were taken — and lets you toggle each layer on and off.",
        "fr":"Une carte de voyage doit retenir des voyages, pas seulement des lieux. Voymark superpose vos pays tamponnés, l'itinéraire de chaque voyage, les villes marquées et les lieux de vos photos — chaque calque s'active ou se désactive.",
        "es":"Un mapa de viajes debe recordar viajes, no solo lugares. Voymark superpone tus países sellados, la ruta de cada viaje, las ciudades marcadas y los puntos de tus fotos — y cada capa se activa o desactiva.",
        "it":"Una mappa di viaggio deve ricordare viaggi, non solo luoghi. Voymark sovrappone i paesi timbrati, la rotta di ogni viaggio, le città segnate e i luoghi delle tue foto — e ogni livello si attiva o disattiva.",
        "de":"Eine Reisekarte sollte sich Reisen merken, nicht nur Orte. Voymark legt deine gestempelten Länder, die Route jeder Reise, markierte Städte und die Orte deiner Fotos übereinander — jede Ebene einzeln schaltbar.",
        "ro":"O hartă de călătorii ar trebui să țină minte călătorii, nu doar locuri. Voymark suprapune țările ștampilate, ruta fiecărei călătorii, orașele marcate și locurile pozelor tale — fiecare strat se aprinde și se stinge separat."}},
  {"h":{"en":"Two styles, one atlas","fr":"Deux styles, un atlas","es":"Dos estilos, un atlas","it":"Due stili, un atlante","de":"Zwei Stile, ein Atlas","ro":"Două stiluri, un atlas"},
   "p":{"en":"Choose a clean, modern Atlas or an aged Paper map that looks pulled from an old expedition journal. Both ship inside the app, work in airplane mode and animate your routes country by country.",
        "fr":"Choisissez un Atlas épuré et moderne ou une carte Papier vieillie qui semble sortie d'un journal d'expédition. Les deux sont livrés dans l'app, fonctionnent en mode avion et animent vos itinéraires pays par pays.",
        "es":"Elige un Atlas limpio y moderno o un mapa de Papel envejecido que parece sacado de un diario de expedición. Ambos vienen dentro de la app, funcionan en modo avión y animan tus rutas país por país.",
        "it":"Scegli un Atlante pulito e moderno o una mappa di Carta invecchiata che sembra uscita da un diario di spedizione. Entrambi sono inclusi nell'app, funzionano in modalità aereo e animano le tue rotte paese per paese.",
        "de":"Wähle einen klaren, modernen Atlas oder eine gealterte Papierkarte wie aus einem alten Expeditionstagebuch. Beide stecken in der App, funktionieren im Flugmodus und animieren deine Routen Land für Land.",
        "ro":"Alege un Atlas curat și modern sau o hartă de Hârtie veche, parcă ruptă dintr-un jurnal de expediție. Ambele vin în aplicație, funcționează în modul avion și îți animă rutele țară cu țară."}},
  {"h":{"en":"Yours alone","fr":"À vous seul","es":"Solo tuyo","it":"Solo tuo","de":"Nur deins","ro":"Doar a ta"},
   "p":{"en":"This is your map, not a feed. It lives on your phone, needs no account, and leaves your device only when you export or share it yourself — as a share card, a PDF travel book or an open-format file.",
        "fr":"C'est votre carte, pas un fil d'actualité. Elle vit sur votre téléphone, n'exige aucun compte et ne quitte votre appareil que si vous l'exportez ou la partagez vous-même — carte à partager, livre de voyage PDF ou fichier au format ouvert.",
        "es":"Es tu mapa, no un feed. Vive en tu teléfono, no necesita cuenta y solo sale de tu dispositivo cuando tú lo exportas o compartes — como tarjeta para compartir, libro de viajes en PDF o archivo en formato abierto.",
        "it":"È la tua mappa, non un feed. Vive sul tuo telefono, non richiede account e lascia il tuo dispositivo solo quando la esporti o condividi tu — come card da condividere, libro di viaggio PDF o file in formato aperto.",
        "de":"Das ist deine Karte, kein Feed. Sie lebt auf deinem Handy, braucht kein Konto und verlässt dein Gerät nur, wenn du sie selbst exportierst oder teilst — als Share-Karte, PDF-Reisebuch oder offenes Dateiformat.",
        "ro":"E harta ta, nu un feed. Trăiește pe telefonul tău, nu cere cont și îți părăsește dispozitivul doar când o exporți sau o distribui chiar tu — drept card de share, carte de călătorie PDF sau fișier în format deschis."}},
  {"h": {"en":"Watch it fill in","fr":"Regardez-la se remplir","es":"Míralo llenarse","it":"Guardala riempirsi","de":"Sieh zu, wie sie sich füllt","ro":"Privește-o cum se umple"},
   "p": {
        "en":"Drag the year slider and the world recolours to exactly where you had been by then — a map of 2019, of 2015, of the year you first left the country. Any year exports as an eight-second vertical video: countries stamping in on their real dates, routes drawing themselves across the paper.",
        "fr":"Faites glisser le curseur des années et le monde se recolore exactement selon vos voyages d'alors — une carte de 2019, de 2015, de l'année où vous avez quitté le pays pour la première fois. Chaque année s'exporte en vidéo verticale de huit secondes : les pays s'y tamponnent à leurs vraies dates, les itinéraires se tracent seuls sur le papier.",
        "es":"Arrastra el control de años y el mundo se recolorea justo hasta donde habías llegado entonces — un mapa de 2019, de 2015, del año en que saliste del país por primera vez. Cualquier año se exporta como vídeo vertical de ocho segundos: los países se sellan en sus fechas reales y las rutas se dibujan solas sobre el papel.",
        "it":"Trascina il cursore degli anni e il mondo si ricolora esattamente su dove eri arrivato allora — una mappa del 2019, del 2015, dell'anno in cui hai lasciato il paese per la prima volta. Ogni anno si esporta come video verticale di otto secondi: i paesi si timbrano alle loro date vere, le rotte si disegnano da sole sulla carta.",
        "de":"Zieh am Jahresregler und die Welt färbt sich genau so ein, wie weit du damals warst — eine Karte von 2019, von 2015, von dem Jahr, in dem du zum ersten Mal das Land verlassen hast. Jedes Jahr lässt sich als acht Sekunden langes Hochkant-Video exportieren: Länder stempeln sich an ihren echten Daten ein, Routen zeichnen sich selbst über das Papier.",
        "ro":"Trage de cursorul anilor și lumea se recolorează exact până unde ajunseseși atunci — o hartă a lui 2019, a lui 2015, a anului în care ai ieșit prima dată din țară. Orice an se exportă ca video vertical de opt secunde: țările se ștampilează la datele lor reale, traseele se desenează singure peste hârtie."}},
  {"h":{"en":"From the whole world down to one street corner","fr":"Du monde entier à un coin de rue","es":"Del mundo entero a una esquina","it":"Dal mondo intero a un angolo di strada","de":"Von der ganzen Welt bis zur Straßenecke","ro":"De la lumea întreagă la un colț de stradă"},
   "p":{"en":"Zoomed out, the map is a passport: burgundy where you have been, gold where you want to go. Pinch in and it becomes a record of a single afternoon — the cities you marked, the route between them, and a gold dot for every place a photo was taken.",
        "fr":"Dézoomée, la carte est un passeport : bordeaux là où vous êtes allé, or là où vous voulez aller. Zoomez et elle devient le récit d'un seul après-midi — les villes marquées, l'itinéraire entre elles et un point doré à chaque endroit photographié.",
        "es":"Alejado, el mapa es un pasaporte: burdeos donde has estado, oro donde quieres ir. Acércate y se convierte en el registro de una sola tarde — las ciudades que marcaste, la ruta entre ellas y un punto dorado en cada lugar donde hiciste una foto.",
        "it":"Da lontano la mappa è un passaporto: bordeaux dove sei stato, oro dove vuoi andare. Avvicinati e diventa il racconto di un solo pomeriggio — le città che hai segnato, il percorso fra loro e un punto dorato per ogni luogo fotografato.",
        "de":"Herausgezoomt ist die Karte ein Reisepass: burgunderrot, wo du warst, golden, wohin du willst. Zoom hinein, und sie wird zum Protokoll eines einzelnen Nachmittags — die markierten Städte, die Route dazwischen und ein goldener Punkt für jeden fotografierten Ort.",
        "ro":"Depărtată, harta e un pașaport: bordo unde ai fost, auriu unde vrei să ajungi. Apropie-te și devine povestea unei singure după-amiezi — orașele marcate, traseul dintre ele și un punct auriu pentru fiecare loc fotografiat."},
   "p2":{"en":"Tap a gold dot and the photo opens full-screen. Every layer — countries, routes, cities, photos — has its own switch, so the map can be a clean atlas one minute and a dense diary of one week the next.",
         "fr":"Touchez un point doré et la photo s'ouvre en plein écran. Chaque couche — pays, itinéraires, villes, photos — a son interrupteur : la carte peut être un atlas épuré à un instant et le journal dense d'une semaine à l'autre.",
         "es":"Toca un punto dorado y la foto se abre a pantalla completa. Cada capa — países, rutas, ciudades, fotos — tiene su interruptor, así que el mapa puede ser un atlas limpio un momento y el diario denso de una semana al siguiente.",
         "it":"Tocca un punto dorato e la foto si apre a schermo intero. Ogni livello — paesi, percorsi, città, foto — ha il suo interruttore: la mappa può essere un atlante pulito in un momento e il diario fitto di una settimana in quello dopo.",
         "de":"Tippe auf einen goldenen Punkt, und das Foto öffnet sich formatfüllend. Jede Ebene — Länder, Routen, Städte, Fotos — hat einen eigenen Schalter: mal klarer Atlas, mal dichtes Tagebuch einer Woche.",
         "ro":"Atinge un punct auriu și poza se deschide pe tot ecranul. Fiecare strat — țări, trasee, orașe, poze — are propriul comutator, așa că harta poate fi un atlas curat într-o clipă și jurnalul dens al unei săptămâni în următoarea."}},
  {"h":{"en":"It never asks where you are","fr":"Elle ne demande jamais où vous êtes","es":"Nunca pregunta dónde estás","it":"Non chiede mai dove sei","de":"Sie fragt nie, wo du bist","ro":"Nu întreabă niciodată unde ești"},
   "p":{"en":"Voymark requests no location permission at all — not once, not in the background. There is no GPS log, no live tracking, nothing following you between trips. The map knows where you have been because you told it, or because a photo you already had carried the coordinates.",
        "fr":"Voymark ne demande aucune autorisation de localisation — jamais, ni en arrière-plan. Pas de journal GPS, pas de suivi en direct, rien qui vous suive entre deux voyages. La carte sait où vous êtes allé parce que vous le lui avez dit, ou parce qu'une photo que vous aviez déjà portait les coordonnées.",
        "es":"Voymark no pide ningún permiso de ubicación — ni una vez, ni en segundo plano. No hay registro de GPS, ni rastreo en vivo, nada que te siga entre viajes. El mapa sabe dónde has estado porque tú se lo dijiste, o porque una foto que ya tenías llevaba las coordenadas.",
        "it":"Voymark non chiede alcun permesso di localizzazione — mai, nemmeno in background. Nessun log GPS, nessun tracciamento dal vivo, niente che ti segua fra un viaggio e l'altro. La mappa sa dove sei stato perché gliel'hai detto tu, o perché una foto che avevi già portava le coordinate.",
        "de":"Voymark fragt überhaupt nicht nach Standortfreigabe — kein einziges Mal, auch nicht im Hintergrund. Kein GPS-Log, kein Live-Tracking, nichts, das dir zwischen Reisen folgt. Die Karte weiß, wo du warst, weil du es ihr gesagt hast oder weil ein Foto die Koordinaten schon trug.",
        "ro":"Voymark nu cere nicio permisiune de locație — nici măcar o dată, nici în fundal. Nu există jurnal GPS, nu există urmărire în timp real, nimic care să te urmeze între călătorii. Harta știe unde ai fost pentru că i-ai spus tu sau pentru că o poză pe care o aveai deja purta coordonatele."},
   "p2":{"en":"That is why the whole map works in airplane mode: the borders, the labels and the region outlines are files inside the app, not tiles fetched from a server that would learn what you are looking at.",
         "fr":"C'est pourquoi toute la carte fonctionne en mode avion : les frontières, les libellés et les contours de régions sont des fichiers dans l'application, pas des tuiles récupérées sur un serveur qui saurait ce que vous regardez.",
         "es":"Por eso el mapa entero funciona en modo avión: las fronteras, las etiquetas y los contornos de regiones son archivos dentro de la app, no teselas pedidas a un servidor que sabría qué estás mirando.",
         "it":"Per questo l'intera mappa funziona in modalità aereo: confini, etichette e contorni delle regioni sono file dentro l'app, non tile chieste a un server che saprebbe cosa stai guardando.",
         "de":"Darum funktioniert die ganze Karte im Flugmodus: Grenzen, Beschriftungen und Regionsumrisse sind Dateien in der App, keine Kacheln von einem Server, der mitbekäme, was du dir ansiehst.",
         "ro":"De aceea toată harta merge în modul avion: granițele, etichetele și conturul regiunilor sunt fișiere din aplicație, nu tile-uri cerute unui server care ar afla ce anume privești."}},
 ],
 "faq": [
  {"q":{"en":"Which map styles are available?","fr":"Quels styles de carte sont disponibles ?","es":"¿Qué estilos de mapa hay?","it":"Quali stili di mappa ci sono?","de":"Welche Kartenstile gibt es?","ro":"Ce stiluri de hartă există?"},
   "a":{"en":"Atlas and Paper are drawn from data bundled in the app and work offline on both iPhone and Android. On iPhone there are two more, Modern and Satellite, drawn by Apple Maps — those fetch tiles, so they need a connection.",
        "fr":"Atlas et Papier sont dessinés à partir de données intégrées et fonctionnent hors ligne sur iPhone comme sur Android. Sur iPhone, deux styles s'ajoutent, Moderne et Satellite, dessinés par Apple Plans — ils téléchargent des tuiles et demandent donc une connexion.",
        "es":"Atlas y Papel se dibujan con datos incluidos en la app y funcionan sin conexión tanto en iPhone como en Android. En iPhone hay dos más, Moderno y Satélite, dibujados por Apple Maps — esos descargan teselas, así que necesitan conexión.",
        "it":"Atlas e Carta sono disegnati da dati inclusi nell'app e funzionano offline su iPhone e Android. Su iPhone se ne aggiungono due, Moderno e Satellite, disegnati da Apple Mappe — quelli scaricano tile, quindi richiedono connessione.",
        "de":"Atlas und Papier werden aus mitgelieferten Daten gezeichnet und funktionieren offline auf iPhone wie Android. Auf dem iPhone kommen Modern und Satellit hinzu, gezeichnet von Apple Karten — die laden Kacheln und brauchen daher Netz.",
        "ro":"Atlas și Hârtie sunt desenate din date incluse în aplicație și merg offline atât pe iPhone, cât și pe Android. Pe iPhone mai există două, Modern și Satelit, desenate de Apple Maps — acelea descarcă tile-uri, deci au nevoie de conexiune."}},
  {"q":{"en":"Can the map show the route of each trip?","fr":"La carte peut-elle montrer l'itinéraire de chaque voyage ?","es":"¿El mapa puede mostrar la ruta de cada viaje?","it":"La mappa può mostrare il percorso di ogni viaggio?","de":"Kann die Karte die Route jeder Reise zeigen?","ro":"Poate harta să arate traseul fiecărei călătorii?"},
   "a":{"en":"Yes. Places are joined in the order you visited them, and each leg is classified as a flight, an overland journey or a local hop from its distance and speed, so a trip reads as a route rather than a scatter of pins. Press play and it draws itself.",
        "fr":"Oui. Les lieux sont reliés dans l'ordre de visite, et chaque étape est classée en vol, trajet terrestre ou déplacement local selon la distance et la vitesse : un voyage se lit comme un itinéraire, pas comme un nuage d'épingles. Appuyez sur lecture et il se dessine.",
        "es":"Sí. Los lugares se unen en el orden en que los visitaste, y cada tramo se clasifica como vuelo, trayecto terrestre o salto local según distancia y velocidad, así que un viaje se lee como una ruta y no como un puñado de chinchetas. Pulsa reproducir y se dibuja solo.",
        "it":"Sì. I luoghi sono uniti nell'ordine in cui li hai visitati e ogni tratta è classificata come volo, viaggio via terra o spostamento locale in base a distanza e velocità: un viaggio si legge come un percorso, non come uno sparpaglio di spilli. Premi play e si disegna da solo.",
        "de":"Ja. Orte werden in der Reihenfolge deines Besuchs verbunden, und jede Etappe wird nach Distanz und Tempo als Flug, Landreise oder lokaler Sprung eingestuft — eine Reise liest sich als Route, nicht als Nadelhaufen. Auf Play tippen, und sie zeichnet sich selbst.",
        "ro":"Da. Locurile sunt unite în ordinea în care le-ai vizitat, iar fiecare etapă e clasificată drept zbor, drum pe uscat sau deplasare locală după distanță și viteză, așa că o călătorie se citește ca un traseu, nu ca un pumn de bolduri. Apeși play și se desenează singură."}},
  {"q":{"en":"Can I make a map of the year I travelled most?","fr":"Puis-je faire la carte de l'année où j'ai le plus voyagé ?","es":"¿Puedo hacer un mapa del año que más viajé?","it":"Posso fare la mappa dell'anno in cui ho viaggiato di più?","de":"Kann ich eine Karte meines reisereichsten Jahres machen?","ro":"Pot face harta anului în care am călătorit cel mai mult?"},
   "a":{"en":"Drag the year slider and the world recolours to exactly what you had marked by that date. Any single year exports as an eight-second vertical video, and the annual recap adds the numbers: countries, distance, flights and the routes replayed.",
        "fr":"Faites glisser le curseur d'année et le monde se recolore exactement selon ce que vous aviez marqué à cette date. Toute année s'exporte en vidéo verticale de huit secondes, et le bilan annuel ajoute les chiffres : pays, distance, vols et itinéraires rejoués.",
        "es":"Arrastra el control de año y el mundo se recolorea con exactamente lo que tenías marcado en esa fecha. Cualquier año se exporta como vídeo vertical de ocho segundos, y el resumen anual añade las cifras: países, distancia, vuelos y las rutas reproducidas.",
        "it":"Trascina il cursore degli anni e il mondo si ricolora esattamente con ciò che avevi segnato a quella data. Ogni singolo anno si esporta come video verticale di otto secondi, e il riepilogo annuale aggiunge i numeri: paesi, distanza, voli e i percorsi riprodotti.",
        "de":"Zieh den Jahresregler, und die Welt färbt sich genau so, wie sie zu diesem Datum markiert war. Jedes Jahr lässt sich als achtsekündiges Hochformat-Video exportieren, und der Jahresrückblick liefert die Zahlen: Länder, Distanz, Flüge und die abgespielten Routen.",
        "ro":"Trage cursorul anilor și lumea se recolorează exact cu ce aveai marcat la acea dată. Orice an se exportă ca video vertical de opt secunde, iar recapitularea anuală adaugă cifrele: țări, distanță, zboruri și traseele rulate."}},
  {"q":{"en":"Does Voymark track my location?","fr":"Voymark suit-il ma position ?","es":"¿Voymark rastrea mi ubicación?","it":"Voymark traccia la mia posizione?","de":"Verfolgt Voymark meinen Standort?","ro":"Voymark îmi urmărește locația?"},
   "a":{"en":"No. It never requests location permission, in the foreground or the background, so there is no GPS trail to keep. What lands on the map is what you marked yourself or what the coordinates in your own photos already said.",
        "fr":"Non. Il ne demande jamais l'autorisation de localisation, au premier plan comme en arrière-plan : il n'y a donc aucune trace GPS à conserver. Ce qui arrive sur la carte, c'est ce que vous avez marqué ou ce que disaient déjà les coordonnées de vos photos.",
        "es":"No. Nunca pide permiso de ubicación, ni en primer plano ni en segundo, así que no hay rastro de GPS que guardar. Lo que llega al mapa es lo que marcaste tú o lo que ya decían las coordenadas de tus propias fotos.",
        "it":"No. Non chiede mai il permesso di localizzazione, né in primo piano né in background: non c'è alcuna traccia GPS da conservare. Sulla mappa finisce ciò che hai segnato tu o ciò che dicevano già le coordinate delle tue foto.",
        "de":"Nein. Die App fragt nie nach Standortfreigabe, weder im Vorder- noch im Hintergrund — es gibt also keine GPS-Spur. Auf der Karte landet, was du selbst markiert hast oder was die Koordinaten deiner eigenen Fotos ohnehin sagten.",
        "ro":"Nu. Nu cere niciodată permisiunea de locație, nici în prim-plan, nici în fundal, deci nu există nicio urmă GPS de păstrat. Pe hartă ajunge ce ai marcat tu sau ce spuneau deja coordonatele din pozele tale."}},
  {"q":{"en":"Can I import a map or tracks I already have?","fr":"Puis-je importer une carte ou des traces existantes ?","es":"¿Puedo importar un mapa o tracks que ya tengo?","it":"Posso importare una mappa o tracce che ho già?","de":"Kann ich vorhandene Karten oder Tracks importieren?","ro":"Pot importa o hartă sau trasee pe care le am deja?"},
   "a":{"en":"GPX and KML files import directly, including exports from other travel apps. Voymark splits them into separate trips where the dates jump, or follows the folder names inside the file when there are any, so one export does not collapse into a single impossible journey.",
        "fr":"Les fichiers GPX et KML s'importent directement, y compris les exports d'autres applications de voyage. Voymark les découpe en voyages distincts là où les dates sautent, ou suit les noms de dossiers du fichier quand il y en a, pour qu'un export ne s'effondre pas en un seul voyage impossible.",
        "es":"Los archivos GPX y KML se importan directamente, incluidas las exportaciones de otras apps de viaje. Voymark los divide en viajes separados donde saltan las fechas, o sigue los nombres de carpeta del archivo cuando los hay, para que una exportación no acabe siendo un único viaje imposible.",
        "it":"I file GPX e KML si importano direttamente, comprese le esportazioni di altre app di viaggio. Voymark li divide in viaggi separati dove le date saltano, oppure segue i nomi delle cartelle nel file quando ci sono, così un export non collassa in un unico viaggio impossibile.",
        "de":"GPX- und KML-Dateien lassen sich direkt importieren, auch Exporte anderer Reise-Apps. Voymark teilt sie dort in eigene Reisen, wo die Daten springen, oder folgt den Ordnernamen in der Datei, falls vorhanden — damit ein Export nicht zu einer einzigen unmöglichen Reise zusammenfällt.",
        "ro":"Fișierele GPX și KML se importă direct, inclusiv exporturile din alte aplicații de călătorie. Voymark le împarte în călătorii separate acolo unde sar datele sau urmează numele folderelor din fișier, când există, ca un export să nu se prăbușească într-o singură călătorie imposibilă."}},
 ],
},

# The one page here that answers a question instead of describing a
# product. "How many countries are there in the world" is asked constantly
# and answered badly — usually with one number and no denominator — and it
# is the exact question Voymark's counting rule exists to settle. It feeds
# country-counter.html, which is about *your* number rather than the
# world's; the two link to each other so they rank as a pair instead of
# competing (SEO/GEO plan, 2026-07-31).
"how-many-countries-in-the-world": {
 "nav": {"en":"How many countries?","fr":"Combien de pays ?","es":"¿Cuántos países?","it":"Quanti paesi?","de":"Wie viele Länder?","ro":"Câte țări?"},
 "title": {
  "en":"How many countries are there in the world? 193, 197 or 249 | Voymark",
  "fr":"Combien y a-t-il de pays dans le monde ? 193, 197 ou 249 | Voymark",
  "es":"¿Cuántos países hay en el mundo? 193, 197 o 249 | Voymark",
  "it":"Quanti paesi ci sono nel mondo? 193, 197 o 249 | Voymark",
  "de":"Wie viele Länder gibt es auf der Welt? 193, 197 oder 249 | Voymark",
  "ro":"Câte țări sunt în lume? 193, 197 sau 249 | Voymark"},
 "meta": {
  "en":"193 UN member states, 197 on the travellers' list, 249 ISO codes — all three are correct answers to different questions. Here is what each number contains and which one to count with.",
  "fr":"193 États membres de l'ONU, 197 sur la liste des voyageurs, 249 codes ISO — les trois réponses sont justes, à des questions différentes. Voici ce que contient chaque nombre et lequel utiliser.",
  "es":"193 estados miembros de la ONU, 197 en la lista de los viajeros, 249 códigos ISO: las tres respuestas son correctas, a preguntas distintas. Esto es lo que contiene cada número y cuál usar.",
  "it":"193 stati membri ONU, 197 nella lista dei viaggiatori, 249 codici ISO: tutte e tre le risposte sono giuste, a domande diverse. Ecco cosa contiene ogni numero e quale usare.",
  "de":"193 UN-Mitgliedstaaten, 197 auf der Reisendenliste, 249 ISO-Codes — alle drei Antworten stimmen, nur auf verschiedene Fragen. Was in jeder Zahl steckt und mit welcher du zählen solltest.",
  "ro":"193 de state membre ONU, 197 pe lista călătorilor, 249 de coduri ISO — toate trei sunt răspunsuri corecte, la întrebări diferite. Iată ce conține fiecare număr și cu care să numeri."},
 "h1": {
  "en":"How many countries are there in the world?",
  "fr":"Combien y a-t-il de pays dans le monde ?",
  "es":"¿Cuántos países hay en el mundo?",
  "it":"Quanti paesi ci sono nel mondo?",
  "de":"Wie viele Länder gibt es auf der Welt?",
  "ro":"Câte țări sunt în lume?"},
 "lede": {
  "en":"193, 197 or 249. All three are right — they answer different questions, and only one of them is a question about travel.",
  "fr":"193, 197 ou 249. Les trois sont justes : elles répondent à des questions différentes, et une seule concerne le voyage.",
  "es":"193, 197 o 249. Las tres son correctas: responden a preguntas distintas, y solo una es una pregunta sobre viajar.",
  "it":"193, 197 o 249. Tutte e tre sono giuste: rispondono a domande diverse, e una sola riguarda il viaggio.",
  "de":"193, 197 oder 249. Alle drei stimmen — sie beantworten verschiedene Fragen, und nur eine davon ist eine Frage übers Reisen.",
  "ro":"193, 197 sau 249. Toate trei sunt corecte: răspund unor întrebări diferite, iar una singură este o întrebare despre călătorii."},
 "sections": [
  {"h":{"en":"The short answer","fr":"La réponse courte","es":"La respuesta corta","it":"La risposta breve","de":"Die kurze Antwort","ro":"Răspunsul scurt"},
   "p":{"en":"There are 193 United Nations member states, 197 countries on the list most travellers use, and 249 entries in the ISO 3166 country-code standard. No number is a mistake; each one draws the line in a different place, and the disagreement is about sovereignty and about territories, not about geography.",
        "fr":"Il y a 193 États membres des Nations unies, 197 pays sur la liste qu'utilisent la plupart des voyageurs, et 249 entrées dans la norme ISO 3166 des codes pays. Aucun chiffre n'est faux ; chacun trace la limite ailleurs, et le désaccord porte sur la souveraineté et les territoires, pas sur la géographie.",
        "es":"Hay 193 estados miembros de las Naciones Unidas, 197 países en la lista que usa la mayoría de los viajeros y 249 entradas en la norma ISO 3166 de códigos de país. Ningún número es un error; cada uno traza la línea en otro sitio, y la discrepancia va de soberanía y de territorios, no de geografía.",
        "it":"Ci sono 193 stati membri delle Nazioni Unite, 197 paesi nella lista che usa la maggior parte dei viaggiatori e 249 voci nello standard ISO 3166 dei codici paese. Nessun numero è sbagliato; ognuno traccia la linea altrove, e il disaccordo riguarda la sovranità e i territori, non la geografia.",
        "de":"Es gibt 193 Mitgliedstaaten der Vereinten Nationen, 197 Länder auf der Liste, die die meisten Reisenden benutzen, und 249 Einträge im ISO-3166-Ländercode-Standard. Keine Zahl ist falsch; jede zieht die Grenze woanders, und der Streit dreht sich um Souveränität und Territorien, nicht um Geografie.",
        "ro":"Există 193 de state membre ale Organizației Națiunilor Unite, 197 de țări pe lista folosită de majoritatea călătorilor și 249 de intrări în standardul ISO 3166 al codurilor de țară. Niciun număr nu este o greșeală; fiecare trage linia în altă parte, iar dezacordul e despre suveranitate și teritorii, nu despre geografie."},
   "p2":{"en":"Which one you should use depends on what you are counting. For a geopolitics essay, 193. For a travel record, 197 is the convention. For collecting territories the way the long-haul clubs do, 249.",
         "fr":"Le bon choix dépend de ce que vous comptez. Pour un devoir de géopolitique, 193. Pour un carnet de voyage, la convention est 197. Pour collectionner les territoires comme le font les clubs de grands voyageurs, 249.",
         "es":"Cuál usar depende de qué estés contando. Para un ensayo de geopolítica, 193. Para un registro de viajes, la convención es 197. Para coleccionar territorios como hacen los clubes de grandes viajeros, 249.",
         "it":"Quale usare dipende da cosa stai contando. Per un saggio di geopolitica, 193. Per un archivio di viaggi la convenzione è 197. Per collezionare territori come fanno i club dei grandi viaggiatori, 249.",
         "de":"Welche du nehmen solltest, hängt davon ab, was du zählst. Für einen geopolitischen Aufsatz 193. Für eine Reisebilanz ist 197 die Konvention. Fürs Sammeln von Territorien, wie es die Vielreisenden-Clubs tun, 249.",
         "ro":"Care dintre ele să o folosești depinde de ce numeri. Pentru un eseu de geopolitică, 193. Pentru o evidență de călătorii, convenția este 197. Pentru colecționat teritorii, așa cum fac cluburile marilor călători, 249."}},
  {"h":{"en":"Why the UN says 193","fr":"Pourquoi l'ONU dit 193","es":"Por qué la ONU dice 193","it":"Perché l'ONU dice 193","de":"Warum die UN 193 sagt","ro":"De ce ONU spune 193"},
   "p":{"en":"193 is a membership figure, not a census of the world. It counts the states that have been admitted to the United Nations — the strictest, cleanest and least arguable definition, which is exactly why institutions use it.",
        "fr":"193 est un chiffre d'adhésion, pas un recensement du monde. Il compte les États admis aux Nations unies — la définition la plus stricte, la plus nette et la moins contestable, et c'est précisément pour cela que les institutions l'emploient.",
        "es":"193 es una cifra de membresía, no un censo del mundo. Cuenta los estados admitidos en las Naciones Unidas: la definición más estricta, más limpia y menos discutible, que es justo por lo que la usan las instituciones.",
        "it":"193 è un dato di adesione, non un censimento del mondo. Conta gli stati ammessi alle Nazioni Unite: la definizione più stretta, più pulita e meno discutibile, ed è esattamente per questo che le istituzioni la usano.",
        "de":"193 ist eine Mitgliederzahl, keine Volkszählung der Welt. Sie zählt die Staaten, die in die Vereinten Nationen aufgenommen wurden — die strengste, sauberste und am wenigsten strittige Definition, und genau darum nutzen Institutionen sie.",
        "ro":"193 este o cifră de membri, nu un recensământ al lumii. Numără statele admise în Organizația Națiunilor Unite — definiția cea mai strictă, cea mai curată și cea mai greu de contestat, exact motivul pentru care instituțiile o folosesc."},
   "p2":{"en":"It leaves out places you can very much fly to, sleep in and get a stamp from. Vatican City and Palestine hold permanent observer status rather than membership; Taiwan is not a member; Kosovo is recognized by many states but not seated. None of that changes whether you have been there.",
         "fr":"Il laisse de côté des lieux où l'on peut parfaitement atterrir, dormir et recevoir un tampon. Le Vatican et la Palestine ont un statut d'observateur permanent et non de membre ; Taïwan n'est pas membre ; le Kosovo est reconnu par de nombreux États mais n'y siège pas. Rien de tout cela ne change le fait que vous y êtes allé.",
         "es":"Deja fuera lugares a los que perfectamente puedes volar, dormir y recibir un sello. El Vaticano y Palestina tienen estatus de observador permanente, no de miembro; Taiwán no es miembro; Kosovo está reconocido por muchos estados pero no tiene asiento. Nada de eso cambia si has estado allí.",
         "it":"Lascia fuori posti in cui si può benissimo atterrare, dormire e farsi timbrare il passaporto. Vaticano e Palestina hanno lo status di osservatore permanente, non di membro; Taiwan non è membro; il Kosovo è riconosciuto da molti stati ma non siede. Niente di tutto ciò cambia il fatto che tu ci sia stato.",
         "de":"Sie lässt Orte aus, zu denen man sehr wohl fliegen, in denen man schlafen und einen Stempel bekommen kann. Vatikanstadt und Palästina haben ständigen Beobachterstatus statt Mitgliedschaft; Taiwan ist kein Mitglied; das Kosovo wird von vielen Staaten anerkannt, sitzt aber nicht am Tisch. Nichts davon ändert, ob du dort warst.",
         "ro":"Lasă pe dinafară locuri în care se poate foarte bine ateriza, dormi și lua o ștampilă. Vaticanul și Palestina au statut de observator permanent, nu de membru; Taiwanul nu este membru; Kosovo este recunoscut de multe state, dar nu are loc la masă. Nimic din toate acestea nu schimbă faptul că ai fost acolo."}},
  {"h":{"en":"Why travellers say 197","fr":"Pourquoi les voyageurs disent 197","es":"Por qué los viajeros dicen 197","it":"Perché i viaggiatori dicono 197","de":"Warum Reisende 197 sagen","ro":"De ce călătorii spun 197"},
   "p":{"en":"197 is the travel community's working answer: the UN's 193 plus the observer states and the de-facto states that function as countries when you actually go — their own border, their own stamp, their own capital.",
        "fr":"197 est la réponse de travail du monde du voyage : les 193 de l'ONU, plus les États observateurs et les États de facto qui se comportent en pays quand on s'y rend vraiment — leur frontière, leur tampon, leur capitale.",
        "es":"197 es la respuesta práctica de la comunidad viajera: los 193 de la ONU más los estados observadores y los estados de facto que funcionan como países cuando de verdad vas — su frontera, su sello, su capital.",
        "it":"197 è la risposta operativa del mondo dei viaggi: i 193 dell'ONU più gli stati osservatori e gli stati de facto che si comportano da paesi quando ci vai davvero — un confine loro, un timbro loro, una capitale loro.",
        "de":"197 ist die Arbeitsantwort der Reise-Community: die 193 der UN plus die Beobachterstaaten und die De-facto-Staaten, die sich wie Länder verhalten, wenn man tatsächlich hinfährt — eigene Grenze, eigener Stempel, eigene Hauptstadt.",
        "ro":"197 este răspunsul practic al comunității de călători: cele 193 ale ONU plus statele observatoare și statele de facto care funcționează ca țări atunci când chiar ajungi acolo — graniță proprie, ștampilă proprie, capitală proprie."},
   "p2":{"en":"It is a convention rather than a law, which is why you will occasionally see 195 or 196 instead, depending on whose list you read and which disputed cases it admits. What matters for a personal record is that the number is stated alongside what it contains.",
         "fr":"C'est une convention et non une loi : d'où les 195 ou 196 qu'on croise parfois, selon la liste consultée et les cas contestés qu'elle accepte. Pour un carnet personnel, l'essentiel est que le nombre soit donné avec ce qu'il contient.",
         "es":"Es una convención, no una ley: por eso a veces verás 195 o 196, según qué lista leas y qué casos disputados admita. Para un registro personal lo que importa es que el número venga con lo que contiene.",
         "it":"È una convenzione, non una legge: per questo a volte trovi 195 o 196, a seconda della lista che leggi e dei casi contesi che ammette. Per un archivio personale conta che il numero sia dichiarato insieme a cosa contiene.",
         "de":"Es ist eine Konvention, kein Gesetz — darum liest man gelegentlich 195 oder 196, je nach Liste und den darin zugelassenen Streitfällen. Für eine persönliche Bilanz zählt, dass die Zahl zusammen mit ihrem Inhalt genannt wird.",
         "ro":"Este o convenție, nu o lege — de aceea vei vedea uneori 195 sau 196, în funcție de lista citită și de cazurile disputate pe care le acceptă. Pentru o evidență personală contează ca numărul să fie spus împreună cu ce conține."}},
  {"h":{"en":"Why a computer says 249","fr":"Pourquoi un ordinateur dit 249","es":"Por qué un ordenador dice 249","it":"Perché un computer dice 249","de":"Warum ein Computer 249 sagt","ro":"De ce un calculator spune 249"},
   "p":{"en":"249 is the count of two-letter codes in ISO 3166-1 — the standard behind country dropdowns, domain suffixes and shipping forms. It includes dependencies and overseas territories: Greenland, Guam, Réunion, the Falklands, Aruba and dozens more.",
        "fr":"249 est le nombre de codes à deux lettres de la norme ISO 3166-1 — celle qui alimente les menus déroulants de pays, les suffixes de domaine et les formulaires d'expédition. Elle inclut les dépendances et territoires d'outre-mer : Groenland, Guam, La Réunion, Malouines, Aruba et des dizaines d'autres.",
        "es":"249 es el número de códigos de dos letras de la ISO 3166-1, la norma que hay detrás de los desplegables de países, los sufijos de dominio y los formularios de envío. Incluye dependencias y territorios de ultramar: Groenlandia, Guam, Reunión, las Malvinas, Aruba y decenas más.",
        "it":"249 è il numero di codici a due lettere della ISO 3166-1 — lo standard dietro i menù a tendina dei paesi, i suffissi di dominio e i moduli di spedizione. Include dipendenze e territori d'oltremare: Groenlandia, Guam, Riunione, Falkland, Aruba e decine di altri.",
        "de":"249 ist die Zahl der Zwei-Buchstaben-Codes in ISO 3166-1 — dem Standard hinter Länder-Dropdowns, Domain-Endungen und Versandformularen. Sie enthält Außengebiete und Überseeterritorien: Grönland, Guam, Réunion, die Falklandinseln, Aruba und Dutzende mehr.",
        "ro":"249 este numărul codurilor din două litere din ISO 3166-1 — standardul din spatele listelor derulante de țări, al sufixelor de domeniu și al formularelor de expediere. Include dependențe și teritorii de peste mări: Groenlanda, Guam, Réunion, Falkland, Aruba și încă zeci."},
   "p2":{"en":"For a traveller this is not padding. Getting to Svalbard or French Guiana is a real journey, and counting them is a legitimate way to keep score — it is simply a different sport from counting sovereign states.",
         "fr":"Pour un voyageur, ce n'est pas du remplissage. Aller au Svalbard ou en Guyane est un vrai voyage, et les compter est une manière légitime de tenir les comptes — c'est simplement un autre sport que compter des États souverains.",
         "es":"Para un viajero esto no es relleno. Llegar a Svalbard o a la Guayana Francesa es un viaje de verdad, y contarlos es una forma legítima de llevar la cuenta — simplemente es otro deporte que contar estados soberanos.",
         "it":"Per un viaggiatore non è riempitivo. Arrivare alle Svalbard o in Guyana francese è un viaggio vero, e contarli è un modo legittimo di tenere il punteggio — è solo uno sport diverso dal contare stati sovrani.",
         "de":"Für Reisende ist das kein Füllmaterial. Nach Spitzbergen oder Französisch-Guayana zu kommen ist eine echte Reise, und sie mitzuzählen ist eine legitime Art zu zählen — nur eben eine andere Disziplin als das Zählen souveräner Staaten.",
         "ro":"Pentru un călător, asta nu e umplutură. Să ajungi în Svalbard sau în Guyana Franceză este o călătorie adevărată, iar numărarea lor e un mod legitim de a ține scorul — pur și simplu e alt sport decât numărarea statelor suverane."}},
  {"h":{"en":"So how many have you visited?","fr":"Alors, combien en avez-vous visités ?","es":"Entonces, ¿cuántos has visitado?","it":"E allora, quanti ne hai visitati?","de":"Und wie viele hast du besucht?","ro":"Deci câte ai vizitat?"},
   "p":{"en":"Your own number needs the same treatment: state the denominator. \"Forty-one out of 197\" is a fact; \"forty-one countries\" is a claim waiting to be argued with. Voymark carries the denominator everywhere the numerator goes, and lets you switch between all three definitions whenever you like.",
        "fr":"Votre propre chiffre mérite le même traitement : donnez le dénominateur. « Quarante et un sur 197 » est un fait ; « quarante et un pays » est une affirmation qui appelle la contradiction. Voymark porte le dénominateur partout où va le numérateur, et vous laisse passer d'une définition à l'autre quand vous voulez.",
        "es":"Tu propio número merece lo mismo: di el denominador. \"Cuarenta y uno de 197\" es un hecho; \"cuarenta y un países\" es una afirmación esperando discusión. Voymark lleva el denominador allí donde va el numerador, y te deja cambiar entre las tres definiciones cuando quieras.",
        "it":"Anche il tuo numero merita lo stesso trattamento: dichiara il denominatore. \"Quarantuno su 197\" è un fatto; \"quarantuno paesi\" è un'affermazione che invita a discutere. Voymark porta il denominatore ovunque vada il numeratore, e ti lascia passare fra le tre definizioni quando vuoi.",
        "de":"Deine eigene Zahl verdient dasselbe: Nenne den Nenner. \"Einundvierzig von 197\" ist eine Tatsache; \"einundvierzig Länder\" ist eine Behauptung, die nach Widerspruch ruft. Voymark trägt den Nenner überall dorthin, wo der Zähler steht, und lässt dich jederzeit zwischen allen drei Definitionen wechseln.",
        "ro":"Și numărul tău merită același tratament: spune numitorul. „Patruzeci și una din 197\" este un fapt; „patruzeci și una de țări\" este o afirmație care așteaptă o ceartă. Voymark duce numitorul oriunde merge numărătorul și te lasă să comuți între toate cele trei definiții oricând vrei."},
   "p2":{"en":"There is a second question underneath, and it is the one that actually changes people's totals: does a layover count? That one is answered on the <a href=\"country-counter.html\">country counter page</a>, where the six visit kinds live.",
         "fr":"Une deuxième question se cache dessous, et c'est elle qui change vraiment les totaux : une escale compte-t-elle ? La réponse est sur la <a href=\"country-counter.html\">page du compteur de pays</a>, là où vivent les six catégories de visite.",
         "es":"Debajo hay una segunda pregunta, y es la que de verdad cambia los totales: ¿cuenta una escala? Eso se responde en la <a href=\"country-counter.html\">página del contador de países</a>, donde viven las seis categorías de visita.",
         "it":"Sotto c'è una seconda domanda, ed è quella che cambia davvero i totali: uno scalo conta? A quella si risponde nella <a href=\"country-counter.html\">pagina del contatore di paesi</a>, dove vivono le sei categorie di visita.",
         "de":"Darunter liegt eine zweite Frage, und sie ist die, die Summen wirklich verändert: Zählt ein Zwischenstopp? Das beantwortet die <a href=\"country-counter.html\">Länderzähler-Seite</a>, auf der die sechs Besuchsarten wohnen.",
         "ro":"Dedesubt stă o a doua întrebare, și tocmai ea schimbă cu adevărat totalurile: contează o escală? La aceea se răspunde pe <a href=\"country-counter.html\">pagina numărătorului de țări</a>, unde stau cele șase feluri de vizită."}},
 ],
 "faq": [
  {"q":{"en":"How many countries are in the United Nations?","fr":"Combien de pays comptent les Nations unies ?","es":"¿Cuántos países hay en las Naciones Unidas?","it":"Quanti paesi ci sono nelle Nazioni Unite?","de":"Wie viele Länder sind in den Vereinten Nationen?","ro":"Câte țări sunt în Organizația Națiunilor Unite?"},
   "a":{"en":"193 member states, plus two permanent observer states — the Holy See and Palestine — which are not counted as members. That is where the gap between 193 and the travellers' 197 starts.",
        "fr":"193 États membres, plus deux États observateurs permanents — le Saint-Siège et la Palestine — qui ne sont pas comptés comme membres. C'est là que commence l'écart entre 193 et les 197 des voyageurs.",
        "es":"193 estados miembros, más dos estados observadores permanentes — la Santa Sede y Palestina — que no cuentan como miembros. Ahí empieza la diferencia entre 193 y los 197 de los viajeros.",
        "it":"193 stati membri, più due stati osservatori permanenti — la Santa Sede e la Palestina — che non contano come membri. È lì che comincia lo scarto fra 193 e i 197 dei viaggiatori.",
        "de":"193 Mitgliedstaaten, dazu zwei ständige Beobachterstaaten — der Heilige Stuhl und Palästina —, die nicht als Mitglieder zählen. Dort beginnt die Lücke zwischen 193 und den 197 der Reisenden.",
        "ro":"193 de state membre, plus două state observatoare permanente — Sfântul Scaun și Palestina — care nu se numără ca membri. De acolo începe diferența dintre 193 și cei 197 ai călătorilor."}},
  {"q":{"en":"Is Taiwan a country?","fr":"Taïwan est-il un pays ?","es":"¿Taiwán es un país?","it":"Taiwan è un paese?","de":"Ist Taiwan ein Land?","ro":"Este Taiwanul o țară?"},
   "a":{"en":"It governs itself, issues its own passports and stamps yours on arrival, but it is not a UN member and its status is disputed. Travellers' lists generally include it; the UN's 193 does not. Voymark counts it under the 197 and the 249 rules and excludes it under 193 — the setting is yours.",
        "fr":"Il se gouverne lui-même, délivre ses propres passeports et tamponne le vôtre à l'arrivée, mais il n'est pas membre de l'ONU et son statut est contesté. Les listes de voyageurs l'incluent généralement ; les 193 de l'ONU non. Voymark le compte sous les règles 197 et 249 et l'exclut sous 193 — le réglage vous appartient.",
        "es":"Se gobierna a sí mismo, emite sus propios pasaportes y sella el tuyo al llegar, pero no es miembro de la ONU y su estatus está en disputa. Las listas de viajeros suelen incluirlo; los 193 de la ONU no. Voymark lo cuenta con las reglas 197 y 249 y lo excluye con 193 — el ajuste es tuyo.",
        "it":"Si governa da sé, rilascia i propri passaporti e timbra il tuo all'arrivo, ma non è membro dell'ONU e il suo status è conteso. Le liste dei viaggiatori di solito lo includono; i 193 dell'ONU no. Voymark lo conta con le regole 197 e 249 e lo esclude con 193 — l'impostazione è tua.",
        "de":"Es regiert sich selbst, gibt eigene Pässe aus und stempelt deinen bei der Ankunft, ist aber kein UN-Mitglied und sein Status ist umstritten. Reisendenlisten führen es meist mit; die 193 der UN nicht. Voymark zählt es unter den Regeln 197 und 249 und lässt es unter 193 weg — die Einstellung gehört dir.",
        "ro":"Se guvernează singur, emite propriile pașapoarte și îl ștampilează pe al tău la sosire, dar nu este membru ONU, iar statutul îi este disputat. Listele călătorilor îl includ de obicei; cei 193 ai ONU, nu. Voymark îl numără sub regulile 197 și 249 și îl exclude sub 193 — setarea îți aparține."}},
  {"q":{"en":"What is the difference between a country and a territory?","fr":"Quelle différence entre un pays et un territoire ?","es":"¿Qué diferencia hay entre un país y un territorio?","it":"Che differenza c'è fra un paese e un territorio?","de":"Was ist der Unterschied zwischen Land und Territorium?","ro":"Care e diferența dintre o țară și un teritoriu?"},
   "a":{"en":"A territory has its own borders, often its own currency and stamps, but its foreign affairs belong to another state — Greenland to Denmark, Guam to the United States. That is why they carry ISO codes without being sovereign countries.",
        "fr":"Un territoire a ses propres frontières, souvent sa monnaie et ses tampons, mais ses affaires étrangères relèvent d'un autre État — le Groenland du Danemark, Guam des États-Unis. D'où des codes ISO sans souveraineté.",
        "es":"Un territorio tiene sus propias fronteras, a menudo su moneda y sus sellos, pero sus asuntos exteriores dependen de otro estado — Groenlandia de Dinamarca, Guam de Estados Unidos. Por eso llevan código ISO sin ser países soberanos.",
        "it":"Un territorio ha confini propri, spesso valuta e timbri propri, ma i suoi affari esteri appartengono a un altro stato — la Groenlandia alla Danimarca, Guam agli Stati Uniti. Per questo hanno un codice ISO senza essere paesi sovrani.",
        "de":"Ein Territorium hat eigene Grenzen, oft eigene Währung und eigene Stempel, aber seine Außenpolitik gehört einem anderen Staat — Grönland zu Dänemark, Guam zu den USA. Deshalb tragen sie ISO-Codes, ohne souveräne Länder zu sein.",
        "ro":"Un teritoriu are granițe proprii, adesea monedă și ștampile proprii, dar afacerile externe îi aparțin altui stat — Groenlanda Danemarcei, Guam Statelor Unite. De aceea poartă coduri ISO fără să fie țări suverane."}},
  {"q":{"en":"Which number should I use for my own travel count?","fr":"Quel nombre utiliser pour mon propre compteur de voyages ?","es":"¿Qué número debo usar para mi propio recuento?","it":"Quale numero devo usare per il mio conteggio?","de":"Welche Zahl nehme ich für meine eigene Zählung?","ro":"Ce număr să folosesc pentru propria numărătoare?"},
   "a":{"en":"197 is the safe default: it is what other travellers assume when you say a number out loud. Switch to 193 if you want the strictest possible reading, or to 249 if territories are part of the game for you. Whatever you pick, say it alongside the count.",
        "fr":"197 est le choix par défaut le plus sûr : c'est ce que les autres voyageurs supposent quand vous annoncez un chiffre. Passez à 193 pour la lecture la plus stricte, ou à 249 si les territoires font partie du jeu. Quel que soit votre choix, énoncez-le avec le compte.",
        "es":"197 es el valor por defecto seguro: es lo que los demás viajeros dan por hecho cuando dices un número en voz alta. Cambia a 193 si quieres la lectura más estricta, o a 249 si los territorios forman parte del juego. Elijas lo que elijas, dilo junto a la cifra.",
        "it":"197 è il default sicuro: è ciò che gli altri viaggiatori danno per scontato quando dici un numero ad alta voce. Passa a 193 per la lettura più severa, o a 249 se i territori fanno parte del gioco. Qualunque cosa scegli, dichiarala insieme al conteggio.",
        "de":"197 ist die sichere Voreinstellung: Genau das nehmen andere Reisende an, wenn du eine Zahl nennst. Wechsle auf 193 für die strengste Lesart oder auf 249, wenn Territorien für dich dazugehören. Was auch immer du wählst — nenne es zusammen mit der Zahl.",
        "ro":"197 este alegerea implicită sigură: exact asta presupun ceilalți călători când spui un număr cu voce tare. Treci la 193 dacă vrei citirea cea mai strictă sau la 249 dacă teritoriile fac parte din joc. Orice alegi, spune-o odată cu cifra."}},
  {"q":{"en":"Has anyone visited every country?","fr":"Quelqu'un a-t-il visité tous les pays ?","es":"¿Alguien ha visitado todos los países?","it":"Qualcuno ha visitato tutti i paesi?","de":"Hat jemand jedes Land besucht?","ro":"A vizitat cineva toate țările?"},
   "a":{"en":"Several people have reached every one of the 197, and a smaller group has gone after the full territory list as well. The reason those claims are always argued over is the one this page is about: without a stated definition, \"every country\" is not a checkable sentence.",
        "fr":"Plusieurs personnes ont atteint chacun des 197, et un groupe plus restreint s'est attaqué aussi à la liste complète des territoires. Si ces revendications sont toujours discutées, c'est pour la raison même de cette page : sans définition annoncée, « tous les pays » n'est pas une phrase vérifiable.",
        "es":"Varias personas han llegado a los 197, y un grupo más reducido ha ido también a por la lista completa de territorios. Esas afirmaciones siempre se discuten por lo mismo que trata esta página: sin una definición declarada, \"todos los países\" no es una frase comprobable.",
        "it":"Diverse persone hanno raggiunto tutti e 197, e un gruppo più ristretto ha puntato anche alla lista completa dei territori. Quelle rivendicazioni fanno sempre discutere per il motivo di cui parla questa pagina: senza una definizione dichiarata, \"tutti i paesi\" non è una frase verificabile.",
        "de":"Mehrere Menschen haben alle 197 erreicht, und eine kleinere Gruppe hat sich auch die vollständige Territorienliste vorgenommen. Dass über solche Behauptungen immer gestritten wird, liegt genau am Thema dieser Seite: Ohne genannte Definition ist \"jedes Land\" kein überprüfbarer Satz.",
        "ro":"Mai multe persoane au ajuns în fiecare dintre cele 197, iar un grup mai mic a mers și după lista completă de teritorii. Motivul pentru care astfel de afirmații sunt mereu contestate este chiar subiectul acestei pagini: fără o definiție declarată, „toate țările\" nu este o propoziție verificabilă."}},
 ],
},

# Positioning page. Every alternative in this category charges — most by
# subscription — so "free, no account" is the whole argument and it had no
# page of its own. The claims here are pinned to what Terms already
# promises, not to a nicer-sounding "free forever" (SEO/GEO plan,
# 2026-07-31).
"free-travel-app-no-subscription": {
 "nav": {"en":"Free, no subscription","fr":"Gratuit, sans abonnement","es":"Gratis, sin suscripción","it":"Gratis, senza abbonamento","de":"Kostenlos, ohne Abo","ro":"Gratuit, fără abonament"},
 "title": {
  "en":"A free travel app with no subscription and no account | Voymark",
  "fr":"Une app de voyage gratuite, sans abonnement ni compte | Voymark",
  "es":"Una app de viajes gratis, sin suscripción ni cuenta | Voymark",
  "it":"Un'app di viaggio gratis, senza abbonamento né account | Voymark",
  "de":"Eine kostenlose Reise-App ohne Abo und ohne Konto | Voymark",
  "ro":"O aplicație de călătorii gratuită, fără abonament și fără cont | Voymark"},
 "meta": {
  "en":"No subscription, no ads, no account, no trial that expires. Every Voymark feature is free, your data stays on your device, and you can export all of it at any time.",
  "fr":"Pas d'abonnement, pas de publicité, pas de compte, pas d'essai qui expire. Toutes les fonctions de Voymark sont gratuites, vos données restent sur votre appareil et vous pouvez tout exporter à tout moment.",
  "es":"Sin suscripción, sin anuncios, sin cuenta, sin prueba que caduca. Todas las funciones de Voymark son gratis, tus datos se quedan en tu dispositivo y puedes exportarlo todo cuando quieras.",
  "it":"Nessun abbonamento, nessuna pubblicità, nessun account, nessuna prova che scade. Ogni funzione di Voymark è gratuita, i tuoi dati restano sul tuo dispositivo e puoi esportare tutto quando vuoi.",
  "de":"Kein Abo, keine Werbung, kein Konto, keine ablaufende Testphase. Jede Voymark-Funktion ist kostenlos, deine Daten bleiben auf deinem Gerät, und du kannst alles jederzeit exportieren.",
  "ro":"Fără abonament, fără reclame, fără cont, fără perioadă de probă care expiră. Fiecare funcție Voymark este gratuită, datele tale rămân pe dispozitiv și poți exporta totul oricând."},
 "h1": {
  "en":"Free. No subscription, no account, no ads.",
  "fr":"Gratuit. Sans abonnement, sans compte, sans publicité.",
  "es":"Gratis. Sin suscripción, sin cuenta, sin anuncios.",
  "it":"Gratis. Senza abbonamento, senza account, senza pubblicità.",
  "de":"Kostenlos. Kein Abo, kein Konto, keine Werbung.",
  "ro":"Gratuit. Fără abonament, fără cont, fără reclame."},
 "lede": {
  "en":"Not a trial, not a limited tier, not free-because-you-are-the-product. Here is exactly what that means and what it does not promise.",
  "fr":"Pas un essai, pas une version limitée, pas un gratuit-parce-que-vous-êtes-le-produit. Voici précisément ce que cela signifie — et ce que cela ne promet pas.",
  "es":"No es una prueba, ni un plan limitado, ni un gratis-porque-tú-eres-el-producto. Esto es exactamente lo que significa y lo que no promete.",
  "it":"Non è una prova, non è un piano limitato, non è un gratis-perché-il-prodotto-sei-tu. Ecco esattamente cosa significa e cosa non promette.",
  "de":"Keine Testphase, keine beschnittene Stufe, kein Kostenlos-weil-du-das-Produkt-bist. Hier steht genau, was das heißt — und was es nicht verspricht.",
  "ro":"Nu e o perioadă de probă, nu e un nivel limitat, nu e un gratuit-pentru-că-produsul-ești-tu. Iată exact ce înseamnă și ce nu promite."},
 "sections": [
  {"h":{"en":"What is free","fr":"Ce qui est gratuit","es":"Qué es gratis","it":"Cosa è gratis","de":"Was kostenlos ist","ro":"Ce este gratuit"},
   "p":{"en":"All of it. Every feature described anywhere on this site is available without paying: the offline maps, the photo scan, the regions, the collections, the seals, the time machine, the PDF travel books, the share cards and every export format.",
        "fr":"Tout. Chaque fonction décrite sur ce site est accessible sans payer : les cartes hors ligne, l'analyse des photos, les régions, les collections, les sceaux, la machine à remonter le temps, les livres de voyage PDF, les cartes à partager et tous les formats d'export.",
        "es":"Todo. Cada función descrita en este sitio está disponible sin pagar: los mapas sin conexión, el escaneo de fotos, las regiones, las colecciones, los sellos, la máquina del tiempo, los libros de viaje en PDF, las tarjetas y todos los formatos de exportación.",
        "it":"Tutto. Ogni funzione descritta su questo sito è disponibile senza pagare: le mappe offline, la scansione delle foto, le regioni, le collezioni, i sigilli, la macchina del tempo, i libri di viaggio PDF, le card e ogni formato di esportazione.",
        "de":"Alles. Jede Funktion, die auf dieser Website beschrieben ist, gibt es ohne Bezahlung: die Offline-Karten, den Foto-Scan, die Regionen, die Sammlungen, die Siegel, die Zeitmaschine, die PDF-Reisebücher, die Share-Karten und jedes Exportformat.",
        "ro":"Tot. Fiecare funcție descrisă oriunde pe acest site este disponibilă fără plată: hărțile offline, scanarea pozelor, regiunile, colecțiile, sigiliile, mașina timpului, cărțile de călătorie PDF, cardurile de partajat și fiecare format de export."},
   "p2":{"en":"There is no counter that stops you at ten trips, no watermark on an export, no feature behind a crown icon and no trial that quietly ends. Nothing on the list above is a paid upgrade.",
         "fr":"Aucun compteur ne vous arrête à dix voyages, aucun filigrane sur un export, aucune fonction derrière une couronne, aucun essai qui s'arrête en douce. Rien de ce qui précède n'est une option payante.",
         "es":"No hay contador que te frene a los diez viajes, ni marca de agua en una exportación, ni función tras un icono de corona, ni prueba que se acabe en silencio. Nada de lo anterior es una mejora de pago.",
         "it":"Non c'è un contatore che ti ferma a dieci viaggi, nessuna filigrana su un export, nessuna funzione dietro una corona, nessuna prova che finisce di nascosto. Niente di quanto sopra è un upgrade a pagamento.",
         "de":"Kein Zähler stoppt dich bei zehn Reisen, kein Wasserzeichen auf einem Export, keine Funktion hinter einem Kronen-Symbol, keine Testphase, die leise endet. Nichts davon ist ein kostenpflichtiges Upgrade.",
         "ro":"Nu există un contor care te oprește la zece călătorii, nicio filigranare pe un export, nicio funcție în spatele unei coroane și nicio probă care se termină pe tăcute. Nimic din lista de mai sus nu este un upgrade cu plată."}},
  {"h":{"en":"Why there is no subscription","fr":"Pourquoi il n'y a pas d'abonnement","es":"Por qué no hay suscripción","it":"Perché non c'è abbonamento","de":"Warum es kein Abo gibt","ro":"De ce nu există abonament"},
   "p":{"en":"A subscription pays for something that costs money every month, and in most travel apps that something is a server holding your trips. Voymark has no server. Your record lives in the app's own storage on your phone, so there is no monthly bill to pass on to you.",
        "fr":"Un abonnement paie ce qui coûte chaque mois, et dans la plupart des apps de voyage c'est un serveur qui détient vos voyages. Voymark n'a pas de serveur. Votre historique vit dans le stockage de l'application sur votre téléphone : aucune facture mensuelle à vous répercuter.",
        "es":"Una suscripción paga algo que cuesta dinero cada mes, y en la mayoría de las apps de viaje ese algo es un servidor que guarda tus viajes. Voymark no tiene servidor. Tu registro vive en el almacenamiento de la app en tu móvil, así que no hay factura mensual que trasladarte.",
        "it":"Un abbonamento paga qualcosa che costa ogni mese, e nella maggior parte delle app di viaggio quel qualcosa è un server che tiene i tuoi viaggi. Voymark non ha server. Il tuo archivio vive nello spazio dell'app sul telefono, quindi non c'è nessuna bolletta mensile da girarti.",
        "de":"Ein Abo bezahlt etwas, das monatlich Geld kostet, und in den meisten Reise-Apps ist das ein Server, der deine Reisen hält. Voymark hat keinen Server. Deine Bilanz liegt im Speicher der App auf deinem Telefon — es gibt also keine monatliche Rechnung, die man an dich weiterreichen müsste.",
        "ro":"Un abonament plătește ceva care costă bani în fiecare lună, iar în majoritatea aplicațiilor de călătorie acel ceva este un server care îți ține călătoriile. Voymark nu are server. Evidența ta stă în spațiul aplicației de pe telefon, deci nu există nicio factură lunară de trecut mai departe."},
   "p2":{"en":"The maps are the same story: borders, labels and region outlines are files shipped inside the app rather than tiles rented from a provider by the request. That is what makes offline the default rather than a premium feature.",
         "fr":"Idem pour les cartes : frontières, libellés et contours de régions sont des fichiers livrés dans l'application, pas des tuiles louées à la requête. C'est ce qui fait du hors ligne la norme et non une option premium.",
         "es":"Con los mapas pasa lo mismo: fronteras, etiquetas y contornos de regiones son archivos que vienen dentro de la app, no teselas alquiladas por petición. Eso es lo que hace que sin conexión sea lo normal y no una función premium.",
         "it":"Con le mappe è lo stesso: confini, etichette e contorni delle regioni sono file spediti dentro l'app, non tile affittate a richiesta. È questo che rende l'offline la normalità e non una funzione premium.",
         "de":"Bei den Karten dasselbe: Grenzen, Beschriftungen und Regionsumrisse sind mitgelieferte Dateien, keine pro Anfrage gemieteten Kacheln. Genau darum ist Offline der Normalfall und kein Premium-Feature.",
         "ro":"Cu hărțile e aceeași poveste: granițele, etichetele și conturul regiunilor sunt fișiere livrate în aplicație, nu tile-uri închiriate la cerere. Asta face ca offline să fie normalitatea, nu o funcție premium."}},
  {"h":{"en":"How it is not paid for","fr":"Comment ce n'est pas financé","es":"Cómo no se paga","it":"Come non viene ripagata","de":"Womit es nicht bezahlt wird","ro":"Cum nu se plătește"},
   "p":{"en":"There are no ads in the app, no analytics measuring what you tap, no crash reporter shipping your session somewhere, and no data broker on the other end of anything. The apps have no advertising identifier and never ask for your location.",
        "fr":"Aucune publicité dans l'application, aucune analytique mesurant vos gestes, aucun rapport de plantage expédiant votre session ailleurs, aucun courtier en données au bout du fil. Les apps n'ont pas d'identifiant publicitaire et ne demandent jamais votre position.",
        "es":"No hay anuncios en la app, ni analítica midiendo lo que tocas, ni informe de fallos enviando tu sesión a ningún sitio, ni un corredor de datos al otro extremo. Las apps no tienen identificador publicitario y nunca piden tu ubicación.",
        "it":"Nessuna pubblicità nell'app, nessuna analitica che misura cosa tocchi, nessun crash reporter che spedisce la tua sessione altrove, nessun broker di dati dall'altra parte. Le app non hanno identificatore pubblicitario e non chiedono mai la tua posizione.",
        "de":"Keine Werbung in der App, keine Analyse, die misst, worauf du tippst, kein Crash-Reporter, der deine Sitzung irgendwohin schickt, und kein Datenhändler am anderen Ende. Die Apps haben keine Werbe-ID und fragen nie nach deinem Standort.",
        "ro":"Nu există reclame în aplicație, nu există analitice care măsoară pe ce apeși, nu există raportor de erori care îți trimite sesiunea undeva și nu există broker de date la celălalt capăt. Aplicațiile nu au identificator publicitar și nu îți cer niciodată locația."},
   "p2":{"en":"That is checkable rather than a promise: put the phone in airplane mode and everything except satellite tiles and name search keeps working, because there is nothing on the other side to talk to.",
         "fr":"C'est vérifiable, pas seulement promis : mettez le téléphone en mode avion et tout continue de fonctionner sauf les tuiles satellite et la recherche par nom — il n'y a personne à l'autre bout.",
         "es":"Eso es comprobable, no solo prometido: pon el móvil en modo avión y todo sigue funcionando salvo las teselas de satélite y la búsqueda por nombre, porque no hay nadie al otro lado con quien hablar.",
         "it":"È verificabile, non solo promesso: metti il telefono in modalità aereo e tutto continua a funzionare tranne le tile satellitari e la ricerca per nome, perché dall'altra parte non c'è nessuno con cui parlare.",
         "de":"Das ist überprüfbar, nicht bloß versprochen: Stell das Telefon in den Flugmodus, und alles außer Satellitenkacheln und Namenssuche arbeitet weiter — es gibt niemanden auf der Gegenseite.",
         "ro":"Asta se poate verifica, nu doar promite: pune telefonul în modul avion și totul continuă să funcționeze, în afară de tile-urile satelit și căutarea după nume, pentru că nu există nimeni de partea cealaltă cu care să vorbească."}},
  {"h":{"en":"What we will not promise","fr":"Ce que nous ne promettons pas","es":"Lo que no vamos a prometer","it":"Cosa non promettiamo","de":"Was wir nicht versprechen","ro":"Ce nu promitem"},
   "p":{"en":"Not \"free forever\" — nobody can honestly promise that about software that has to be maintained for a decade. What the terms actually say is narrower and worth more: every feature is free today, and if paid features ever arrive they will be new capabilities. Nothing you already have gets taken away and put behind a price.",
        "fr":"Pas « gratuit pour toujours » — personne ne peut honnêtement promettre cela d'un logiciel à maintenir pendant dix ans. Ce que disent les conditions est plus étroit et vaut davantage : toutes les fonctions sont gratuites aujourd'hui, et si des fonctions payantes arrivent, ce seront de nouvelles capacités. Rien de ce que vous avez déjà ne sera repris et mis derrière un prix.",
        "es":"No \"gratis para siempre\": nadie puede prometer eso honestamente de un software que hay que mantener una década. Lo que dicen los términos es más estrecho y vale más: hoy todas las funciones son gratuitas, y si algún día llegan funciones de pago, serán capacidades nuevas. Nada de lo que ya tienes se retira para ponerlo tras un precio.",
        "it":"Non \"gratis per sempre\": nessuno può prometterlo onestamente per un software da mantenere per un decennio. Quello che dicono i termini è più stretto e vale di più: oggi ogni funzione è gratuita, e se un giorno arriveranno funzioni a pagamento saranno nuove capacità. Niente di ciò che hai già viene tolto e messo dietro un prezzo.",
        "de":"Nicht \"für immer kostenlos\" — das kann niemand ehrlich über Software versprechen, die ein Jahrzehnt gepflegt werden muss. Was die Bedingungen sagen, ist enger und mehr wert: Heute ist jede Funktion kostenlos, und sollten je kostenpflichtige Funktionen kommen, wären es neue Fähigkeiten. Nichts, was du schon hast, wird dir weggenommen und hinter einen Preis gestellt.",
        "ro":"Nu „gratuit pentru totdeauna\" — nimeni nu poate promite asta cinstit despre un software care trebuie întreținut un deceniu. Ce spun termenii este mai îngust și valorează mai mult: astăzi fiecare funcție este gratuită, iar dacă vor apărea vreodată funcții cu plată, vor fi capabilități noi. Nimic din ce ai deja nu îți este luat și pus în spatele unui preț."},
   "p2":{"en":"The safeguard is not our good intentions, it is the export button. Everything you record leaves in CSV, GPX, KML, GeoJSON, a full backup or plain readable text, so the worst case is that you take your record and go.",
         "fr":"La garantie n'est pas notre bonne volonté, c'est le bouton d'export. Tout ce que vous enregistrez ressort en CSV, GPX, KML, GeoJSON, sauvegarde complète ou texte lisible : au pire, vous partez avec votre historique.",
         "es":"La garantía no son nuestras buenas intenciones, es el botón de exportar. Todo lo que registras sale en CSV, GPX, KML, GeoJSON, copia completa o texto legible: en el peor caso, te llevas tu historial y te vas.",
         "it":"La garanzia non sono le nostre buone intenzioni, è il pulsante di esportazione. Tutto ciò che registri esce in CSV, GPX, KML, GeoJSON, backup completo o testo leggibile: nel caso peggiore, prendi il tuo archivio e te ne vai.",
         "de":"Die Absicherung sind nicht unsere guten Absichten, sondern der Export-Knopf. Alles, was du erfasst, geht als CSV, GPX, KML, GeoJSON, vollständiges Backup oder lesbarer Text hinaus — im schlimmsten Fall nimmst du deine Bilanz und gehst.",
         "ro":"Garanția nu sunt bunele noastre intenții, ci butonul de export. Tot ce înregistrezi iese în CSV, GPX, KML, GeoJSON, backup complet sau text lizibil: în cel mai rău caz, îți iei evidența și pleci."}},
 ],
 "faq": [
  {"q":{"en":"Is Voymark really free?","fr":"Voymark est-il vraiment gratuit ?","es":"¿Voymark es realmente gratis?","it":"Voymark è davvero gratis?","de":"Ist Voymark wirklich kostenlos?","ro":"Voymark chiar este gratuit?"},
   "a":{"en":"Yes, and not in the limited-tier sense — every feature is available, with no trial period and no locked sections. There is no account to create, so there is not even a sign-up standing between you and the app.",
        "fr":"Oui, et pas au sens « version limitée » : toutes les fonctions sont disponibles, sans période d'essai ni sections verrouillées. Il n'y a aucun compte à créer, donc même pas d'inscription entre vous et l'application.",
        "es":"Sí, y no en el sentido de plan limitado: todas las funciones están disponibles, sin periodo de prueba ni secciones bloqueadas. No hay cuenta que crear, así que ni siquiera hay un registro entre tú y la app.",
        "it":"Sì, e non nel senso del piano limitato: tutte le funzioni sono disponibili, senza periodo di prova né sezioni bloccate. Non c'è nessun account da creare, quindi non c'è nemmeno una registrazione fra te e l'app.",
        "de":"Ja, und nicht im Sinne einer beschnittenen Stufe: Alle Funktionen sind verfügbar, ohne Testzeitraum und ohne gesperrte Bereiche. Es gibt kein Konto anzulegen — also nicht einmal eine Anmeldung zwischen dir und der App.",
        "ro":"Da, și nu în sensul de nivel limitat: toate funcțiile sunt disponibile, fără perioadă de probă și fără secțiuni blocate. Nu există niciun cont de creat, deci nu stă nici măcar o înregistrare între tine și aplicație."}},
  {"q":{"en":"Are there ads?","fr":"Y a-t-il de la publicité ?","es":"¿Hay anuncios?","it":"Ci sono pubblicità?","de":"Gibt es Werbung?","ro":"Există reclame?"},
   "a":{"en":"None, and no advertising identifier is read either — so nothing about you is available to sell to an advertiser even in principle.",
        "fr":"Aucune, et aucun identifiant publicitaire n'est lu non plus : rien vous concernant n'est disponible pour un annonceur, même en principe.",
        "es":"Ninguno, y tampoco se lee ningún identificador publicitario: nada sobre ti está disponible para vender a un anunciante, ni siquiera en principio.",
        "it":"Nessuna, e non viene letto nemmeno un identificatore pubblicitario: niente su di te è disponibile da vendere a un inserzionista, nemmeno in linea di principio.",
        "de":"Keine, und es wird auch keine Werbe-ID ausgelesen — es gibt also gar nichts über dich, das man einem Werbetreibenden verkaufen könnte.",
        "ro":"Niciuna, și nu se citește nici vreun identificator publicitar — deci nimic despre tine nu e disponibil de vândut unui agent de publicitate, nici măcar în principiu."}},
  {"q":{"en":"Do you sell my travel data?","fr":"Vendez-vous mes données de voyage ?","es":"¿Vendéis mis datos de viaje?","it":"Vendete i miei dati di viaggio?","de":"Verkauft ihr meine Reisedaten?","ro":"Îmi vindeți datele de călătorie?"},
   "a":{"en":"We never receive them. Your trips, photos links and stamps are written to your device and nowhere else, so there is no copy on our side to sell, lose or hand over.",
        "fr":"Nous ne les recevons jamais. Vos voyages, liens de photos et tampons sont écrits sur votre appareil et nulle part ailleurs : aucune copie chez nous à vendre, à perdre ou à remettre.",
        "es":"Nunca las recibimos. Tus viajes, enlaces de fotos y sellos se escriben en tu dispositivo y en ningún otro sitio, así que no hay copia de nuestro lado que vender, perder o entregar.",
        "it":"Non li riceviamo mai. I tuoi viaggi, i collegamenti alle foto e i timbri vengono scritti sul tuo dispositivo e da nessun'altra parte: non esiste una copia dalla nostra parte da vendere, perdere o consegnare.",
        "de":"Wir bekommen sie nie. Deine Reisen, Fotoverweise und Stempel werden auf dein Gerät geschrieben und nirgends sonst — es gibt bei uns keine Kopie zum Verkaufen, Verlieren oder Herausgeben.",
        "ro":"Nu le primim niciodată. Călătoriile, legăturile către poze și ștampilele tale sunt scrise pe dispozitivul tău și nicăieri altundeva, deci nu există nicio copie la noi de vândut, de pierdut sau de predat."}},
  {"q":{"en":"Will it start charging later?","fr":"Deviendra-t-il payant plus tard ?","es":"¿Empezará a cobrar más adelante?","it":"Inizierà a farsi pagare più avanti?","de":"Wird später Geld verlangt?","ro":"Va începe să coste mai târziu?"},
   "a":{"en":"Possibly, for capabilities that do not exist yet — that is what the terms commit to. What will not happen is a feature you use today moving behind a price. And if it ever did, your whole record exports in open formats, so nothing is held hostage.",
        "fr":"Peut-être, pour des capacités qui n'existent pas encore : c'est ce à quoi les conditions s'engagent. Ce qui n'arrivera pas, c'est qu'une fonction que vous utilisez aujourd'hui passe derrière un prix. Et si cela arrivait, tout votre historique s'exporte en formats ouverts : rien n'est pris en otage.",
        "es":"Posiblemente, para capacidades que aún no existen: eso es a lo que se comprometen los términos. Lo que no va a pasar es que una función que usas hoy se ponga tras un precio. Y si pasara, todo tu registro se exporta en formatos abiertos, así que nada queda secuestrado.",
        "it":"Forse, per capacità che ancora non esistono: è ciò a cui i termini si impegnano. Quello che non succederà è che una funzione che usi oggi finisca dietro un prezzo. E se anche accadesse, tutto il tuo archivio si esporta in formati aperti: niente resta in ostaggio.",
        "de":"Möglicherweise — für Fähigkeiten, die es noch nicht gibt; darauf legen sich die Bedingungen fest. Was nicht passieren wird: dass eine Funktion, die du heute nutzt, hinter einen Preis wandert. Und selbst dann exportiert sich deine ganze Bilanz in offenen Formaten, es wird also nichts als Geisel gehalten.",
        "ro":"Posibil, pentru capabilități care încă nu există — la asta se angajează termenii. Ce nu se va întâmpla este ca o funcție pe care o folosești astăzi să treacă în spatele unui preț. Iar dacă s-ar întâmpla, toată evidența ta se exportă în formate deschise, deci nimic nu e ținut ostatic."}},
  {"q":{"en":"What happens to my trips if the app disappears?","fr":"Qu'advient-il de mes voyages si l'app disparaît ?","es":"¿Qué pasa con mis viajes si la app desaparece?","it":"Cosa succede ai miei viaggi se l'app sparisce?","de":"Was passiert mit meinen Reisen, wenn die App verschwindet?","ro":"Ce se întâmplă cu călătoriile mele dacă aplicația dispare?"},
   "a":{"en":"They stay on your phone, because that is where they always were — nothing switches off when a server does. Export a backup and a plain-text copy now and you hold a readable record that needs no app at all.",
        "fr":"Ils restent sur votre téléphone, puisque c'est là qu'ils ont toujours été : rien ne s'éteint quand un serveur s'éteint. Exportez dès maintenant une sauvegarde et une copie en texte brut, et vous détenez un historique lisible sans aucune application.",
        "es":"Se quedan en tu móvil, porque es donde estuvieron siempre: nada se apaga cuando se apaga un servidor. Exporta ahora una copia de seguridad y una copia en texto plano y tendrás un registro legible que no necesita ninguna app.",
        "it":"Restano sul tuo telefono, perché è lì che sono sempre stati: non si spegne nulla quando si spegne un server. Esporta ora un backup e una copia in testo semplice e avrai un archivio leggibile che non ha bisogno di nessuna app.",
        "de":"Sie bleiben auf deinem Telefon, denn dort waren sie immer — es schaltet sich nichts ab, wenn ein Server abschaltet. Exportiere jetzt ein Backup und eine Textkopie, dann hältst du eine lesbare Bilanz, die ganz ohne App auskommt.",
        "ro":"Rămân pe telefonul tău, pentru că acolo au fost dintotdeauna — nu se stinge nimic când se stinge un server. Exportă acum un backup și o copie în text simplu și ai o evidență lizibilă care nu are nevoie de nicio aplicație."}},
 ],
},

# The comparison page. It names competitors and their prices, which only
# works if it is fair: each entry says what that app is genuinely better
# at, and the prices carry the date they were checked because they move.
# An unfair comparison page is worth less than none — a reader who catches
# one wrong claim discounts the rest (SEO/GEO plan, 2026-07-31).
"travel-app-alternatives": {
 "nav": {"en":"Alternatives","fr":"Alternatives","es":"Alternativas","it":"Alternative","de":"Alternativen","ro":"Alternative"},
 "title": {
  "en":"Travel tracker app alternatives, and what they cost | Voymark",
  "fr":"Alternatives aux apps de suivi de voyage, et leur prix | Voymark",
  "es":"Alternativas a las apps de seguimiento de viajes y su precio | Voymark",
  "it":"Alternative alle app per tracciare i viaggi, e quanto costano | Voymark",
  "de":"Alternativen zu Reise-Tracker-Apps und was sie kosten | Voymark",
  "ro":"Alternative la aplicațiile de urmărit călătorii și cât costă | Voymark"},
 "meta": {
  "en":"Been, Visited, Polarsteps, Journi, Pin Traveler, Skratch, Stampie — what each one is good at, what it charges, and where Voymark differs. Prices checked July 2026.",
  "fr":"Been, Visited, Polarsteps, Journi, Pin Traveler, Skratch, Stampie — les points forts de chacune, leur tarif, et en quoi Voymark diffère. Prix vérifiés en juillet 2026.",
  "es":"Been, Visited, Polarsteps, Journi, Pin Traveler, Skratch, Stampie: en qué es buena cada una, cuánto cobra y en qué se diferencia Voymark. Precios comprobados en julio de 2026.",
  "it":"Been, Visited, Polarsteps, Journi, Pin Traveler, Skratch, Stampie: in cosa è brava ciascuna, quanto costa e in cosa Voymark è diversa. Prezzi verificati a luglio 2026.",
  "de":"Been, Visited, Polarsteps, Journi, Pin Traveler, Skratch, Stampie — worin jede gut ist, was sie kostet und wo Voymark anders ist. Preise geprüft im Juli 2026.",
  "ro":"Been, Visited, Polarsteps, Journi, Pin Traveler, Skratch, Stampie — la ce e bună fiecare, cât costă și prin ce diferă Voymark. Prețuri verificate în iulie 2026."},
 "h1": {
  "en":"Travel tracker apps, compared honestly",
  "fr":"Les apps de suivi de voyage, comparées honnêtement",
  "es":"Apps de seguimiento de viajes, comparadas con honestidad",
  "it":"App per tracciare i viaggi, confrontate onestamente",
  "de":"Reise-Tracker-Apps, ehrlich verglichen",
  "ro":"Aplicații de urmărit călătorii, comparate cinstit"},
 "lede": {
  "en":"Several of these are good apps. Here is what each is best at, what it costs, and the one thing that actually separates them.",
  "fr":"Plusieurs de ces applications sont bonnes. Voici ce que chacune fait de mieux, ce qu'elle coûte, et la seule chose qui les sépare vraiment.",
  "es":"Varias de estas apps son buenas. Esto es en qué destaca cada una, cuánto cuesta y lo único que de verdad las separa.",
  "it":"Diverse di queste sono buone app. Ecco in cosa ciascuna è migliore, quanto costa e l'unica cosa che davvero le separa.",
  "de":"Mehrere davon sind gute Apps. Hier steht, worin jede am besten ist, was sie kostet und was sie tatsächlich unterscheidet.",
  "ro":"Câteva dintre acestea sunt aplicații bune. Iată la ce e fiecare cea mai bună, cât costă și singurul lucru care chiar le desparte."},
 "sections": [
  {"h":{"en":"What the others charge","fr":"Ce que demandent les autres","es":"Lo que cobran las demás","it":"Quanto chiedono le altre","de":"Was die anderen verlangen","ro":"Cât cer celelalte"},
   "p":{"en":"Prices as listed in the app stores in July 2026, for the paid tier that unlocks the app properly. They change, and regional pricing differs — check the store before you decide anything on this.",
        "fr":"Tarifs relevés sur les stores en juillet 2026, pour l'offre payante qui débloque réellement l'application. Ils évoluent et varient selon les régions — vérifiez sur le store avant de décider quoi que ce soit.",
        "es":"Precios tal como figuraban en las tiendas en julio de 2026, para el plan de pago que desbloquea la app de verdad. Cambian y varían por región: comprueba la tienda antes de decidir nada con esto.",
        "it":"Prezzi come indicati negli store a luglio 2026, per il piano a pagamento che sblocca davvero l'app. Cambiano e variano per regione: controlla lo store prima di decidere qualcosa su questa base.",
        "de":"Preise wie im Juli 2026 in den App-Stores gelistet, für die Bezahlstufe, die die App wirklich freischaltet. Sie ändern sich und unterscheiden sich je nach Region — prüfe den Store, bevor du etwas darauf stützt.",
        "ro":"Prețuri așa cum apăreau în magazine în iulie 2026, pentru nivelul plătit care deblochează cu adevărat aplicația. Se schimbă și diferă pe regiuni — verifică magazinul înainte să decizi ceva pe baza lor."},
   "list":{
    "en":["<strong>Been</strong> — about $19.99 a year. The simplest of the group: countries and a percentage, done well.",
          "<strong>Visited</strong> — about $34.99 a year or $59.99 once. Strong on regions and territory lists.",
          "<strong>Polarsteps</strong> — about $34.99 a year. Live GPS tracking while you travel and beautifully printed books; nothing here matches its automatic route recording.",
          "<strong>Journi</strong> — about $53.99 a year. Built around photo books and a shareable travel blog.",
          "<strong>Pin Traveler</strong> — about $34.99 a year or $44.99 once. Detailed pins and trip logs.",
          "<strong>Skratch</strong> — about $9.99 once. A scratch-map feel, cheap and focused.",
          "<strong>Stampie</strong> — about $14.99 once. Passport stamps as the central idea.",
          "<strong>Voymark</strong> — free, no subscription, no account."],
    "fr":["<strong>Been</strong> — environ 19,99 $ par an. La plus simple du lot : les pays et un pourcentage, bien faits.",
          "<strong>Visited</strong> — environ 34,99 $ par an ou 59,99 $ une fois. Solide sur les régions et les listes de territoires.",
          "<strong>Polarsteps</strong> — environ 34,99 $ par an. Suivi GPS en direct pendant le voyage et livres imprimés superbes ; rien ici n'égale son enregistrement automatique d'itinéraire.",
          "<strong>Journi</strong> — environ 53,99 $ par an. Construite autour des livres photo et d'un blog de voyage partageable.",
          "<strong>Pin Traveler</strong> — environ 34,99 $ par an ou 44,99 $ une fois. Épingles détaillées et carnets de voyage.",
          "<strong>Skratch</strong> — environ 9,99 $ une fois. L'esprit carte à gratter, bon marché et concentré.",
          "<strong>Stampie</strong> — environ 14,99 $ une fois. Les tampons de passeport comme idée centrale.",
          "<strong>Voymark</strong> — gratuit, sans abonnement, sans compte."],
    "es":["<strong>Been</strong> — unos 19,99 $ al año. La más simple del grupo: países y un porcentaje, bien hechos.",
          "<strong>Visited</strong> — unos 34,99 $ al año o 59,99 $ una vez. Fuerte en regiones y listas de territorios.",
          "<strong>Polarsteps</strong> — unos 34,99 $ al año. Seguimiento GPS en directo mientras viajas y libros impresos preciosos; nada aquí iguala su registro automático de rutas.",
          "<strong>Journi</strong> — unos 53,99 $ al año. Construida en torno a los fotolibros y a un blog de viaje compartible.",
          "<strong>Pin Traveler</strong> — unos 34,99 $ al año o 44,99 $ una vez. Chinchetas detalladas y registros de viaje.",
          "<strong>Skratch</strong> — unos 9,99 $ una vez. Aire de mapa rascable, barata y centrada.",
          "<strong>Stampie</strong> — unos 14,99 $ una vez. Los sellos de pasaporte como idea central.",
          "<strong>Voymark</strong> — gratis, sin suscripción, sin cuenta."],
    "it":["<strong>Been</strong> — circa 19,99 $ l'anno. La più semplice del gruppo: paesi e una percentuale, fatti bene.",
          "<strong>Visited</strong> — circa 34,99 $ l'anno o 59,99 $ una volta. Forte su regioni ed elenchi di territori.",
          "<strong>Polarsteps</strong> — circa 34,99 $ l'anno. Tracciamento GPS dal vivo mentre viaggi e libri stampati bellissimi; qui niente eguaglia la sua registrazione automatica dei percorsi.",
          "<strong>Journi</strong> — circa 53,99 $ l'anno. Costruita attorno ai fotolibri e a un blog di viaggio condivisibile.",
          "<strong>Pin Traveler</strong> — circa 34,99 $ l'anno o 44,99 $ una volta. Spilli dettagliati e diari di viaggio.",
          "<strong>Skratch</strong> — circa 9,99 $ una volta. Il gusto della mappa da grattare, economica e focalizzata.",
          "<strong>Stampie</strong> — circa 14,99 $ una volta. I timbri del passaporto come idea centrale.",
          "<strong>Voymark</strong> — gratis, senza abbonamento, senza account."],
    "de":["<strong>Been</strong> — rund 19,99 $ im Jahr. Die einfachste der Gruppe: Länder und ein Prozentsatz, sauber gemacht.",
          "<strong>Visited</strong> — rund 34,99 $ im Jahr oder 59,99 $ einmalig. Stark bei Regionen und Territorienlisten.",
          "<strong>Polarsteps</strong> — rund 34,99 $ im Jahr. Live-GPS-Aufzeichnung unterwegs und wunderschön gedruckte Bücher; sein automatisches Routen-Mitschreiben erreicht hier nichts.",
          "<strong>Journi</strong> — rund 53,99 $ im Jahr. Rund um Fotobücher und einen teilbaren Reiseblog gebaut.",
          "<strong>Pin Traveler</strong> — rund 34,99 $ im Jahr oder 44,99 $ einmalig. Detaillierte Pins und Reiseprotokolle.",
          "<strong>Skratch</strong> — rund 9,99 $ einmalig. Rubbelkarten-Gefühl, günstig und fokussiert.",
          "<strong>Stampie</strong> — rund 14,99 $ einmalig. Passstempel als zentrale Idee.",
          "<strong>Voymark</strong> — kostenlos, kein Abo, kein Konto."],
    "ro":["<strong>Been</strong> — cam 19,99 $ pe an. Cea mai simplă din grup: țări și un procent, făcute bine.",
          "<strong>Visited</strong> — cam 34,99 $ pe an sau 59,99 $ o dată. Puternică pe regiuni și liste de teritorii.",
          "<strong>Polarsteps</strong> — cam 34,99 $ pe an. Urmărire GPS în timp real în călătorie și cărți tipărite superbe; nimic de aici nu se compară cu înregistrarea ei automată a traseului.",
          "<strong>Journi</strong> — cam 53,99 $ pe an. Construită în jurul albumelor foto și al unui blog de călătorie de partajat.",
          "<strong>Pin Traveler</strong> — cam 34,99 $ pe an sau 44,99 $ o dată. Bolduri detaliate și jurnale de călătorie.",
          "<strong>Skratch</strong> — cam 9,99 $ o dată. Senzația de hartă răzuibilă, ieftină și concentrată.",
          "<strong>Stampie</strong> — cam 14,99 $ o dată. Ștampilele de pașaport ca idee centrală.",
          "<strong>Voymark</strong> — gratuit, fără abonament, fără cont."]}},
  {"h":{"en":"Where the others win","fr":"Là où les autres gagnent","es":"Dónde ganan las demás","it":"Dove vincono le altre","de":"Wo die anderen gewinnen","ro":"Unde câștigă celelalte"},
   "p":{"en":"If you want your route recorded automatically while you are moving, Polarsteps is built for that and Voymark is not — it never asks for location permission, which is precisely why it cannot follow you down a road. If you want a hardbound book printed and posted to you, Polarsteps and Journi do that; Voymark makes a PDF and stops there.",
        "fr":"Si vous voulez que votre itinéraire s'enregistre automatiquement en route, Polarsteps est fait pour cela et Voymark non — il ne demande jamais l'autorisation de localisation, et c'est précisément pourquoi il ne peut pas vous suivre sur une route. Si vous voulez un livre relié imprimé et expédié, Polarsteps et Journi le font ; Voymark produit un PDF et s'arrête là.",
        "es":"Si quieres que tu ruta se registre automáticamente mientras te mueves, Polarsteps está hecha para eso y Voymark no: nunca pide permiso de ubicación, y justo por eso no puede seguirte por una carretera. Si quieres un libro encuadernado impreso y enviado a casa, Polarsteps y Journi lo hacen; Voymark genera un PDF y ahí se detiene.",
        "it":"Se vuoi che il percorso si registri da solo mentre ti muovi, Polarsteps è fatta per questo e Voymark no — non chiede mai il permesso di localizzazione, ed è esattamente per questo che non può seguirti lungo una strada. Se vuoi un libro rilegato stampato e spedito, lo fanno Polarsteps e Journi; Voymark produce un PDF e si ferma lì.",
        "de":"Wenn deine Route automatisch mitgeschrieben werden soll, während du unterwegs bist, ist Polarsteps dafür gebaut und Voymark nicht — es fragt nie nach Standortfreigabe, und genau deshalb kann es dir nicht die Straße entlang folgen. Willst du ein gebundenes, gedrucktes und zugeschicktes Buch, machen das Polarsteps und Journi; Voymark erzeugt ein PDF und hört dort auf.",
        "ro":"Dacă vrei ca traseul să se înregistreze automat în timp ce te miști, Polarsteps e făcută pentru asta, iar Voymark nu — nu cere niciodată permisiunea de locație, exact motivul pentru care nu te poate urma pe un drum. Dacă vrei o carte legată, tipărită și trimisă acasă, o fac Polarsteps și Journi; Voymark produce un PDF și se oprește acolo."},
   "p2":{"en":"There is also a real argument for a paid app: money from users is a business model that does not need your data, and a company with revenue can keep the lights on. Being free is not automatically the more ethical choice — it is only better if nothing else is being sold instead.",
         "fr":"Il existe aussi un vrai argument pour une app payante : l'argent des utilisateurs est un modèle qui n'a pas besoin de vos données, et une société qui a des revenus peut durer. La gratuité n'est pas automatiquement le choix le plus éthique — elle ne l'est que si rien d'autre n'est vendu à la place.",
         "es":"También hay un argumento real a favor de una app de pago: el dinero de los usuarios es un modelo que no necesita tus datos, y una empresa con ingresos puede mantenerse. Ser gratis no es automáticamente lo más ético: solo lo es si no se está vendiendo otra cosa en su lugar.",
         "it":"C'è anche un argomento vero a favore di un'app a pagamento: i soldi degli utenti sono un modello che non ha bisogno dei tuoi dati, e un'azienda con ricavi può reggere nel tempo. Essere gratis non è automaticamente la scelta più etica — lo è solo se al suo posto non si sta vendendo altro.",
         "de":"Es gibt auch ein echtes Argument für eine Bezahl-App: Geld von Nutzern ist ein Modell, das deine Daten nicht braucht, und eine Firma mit Einnahmen kann durchhalten. Kostenlos ist nicht automatisch die ethischere Wahl — sie ist es nur, wenn stattdessen nichts anderes verkauft wird.",
         "ro":"Există și un argument real pentru o aplicație cu plată: banii de la utilizatori sunt un model care nu are nevoie de datele tale, iar o firmă cu venituri poate rezista. A fi gratuit nu e automat alegerea mai etică — este mai bună doar dacă în locul banilor nu se vinde altceva."}},
  {"h":{"en":"Where Voymark is different","fr":"En quoi Voymark diffère","es":"En qué se diferencia Voymark","it":"In cosa Voymark è diversa","de":"Worin Voymark anders ist","ro":"Prin ce diferă Voymark"},
   "p":{"en":"No account and no server, so nothing to sign into and nothing to be locked out of. The maps ship inside the app, so the whole thing works with the network off. Photos become trips on the phone itself, with no upload step. And the counting rule is yours to set — 197, 193 or 249 — with six visit kinds deciding what a layover is worth.",
        "fr":"Aucun compte et aucun serveur : rien où se connecter, rien dont être exclu. Les cartes sont livrées dans l'application, donc tout fonctionne réseau coupé. Les photos deviennent des voyages sur le téléphone lui-même, sans étape de téléversement. Et la règle de comptage vous appartient — 197, 193 ou 249 — avec six catégories de visite qui décident de la valeur d'une escale.",
        "es":"Sin cuenta y sin servidor: nada donde iniciar sesión y nada de lo que quedarte fuera. Los mapas vienen dentro de la app, así que todo funciona con la red apagada. Las fotos se convierten en viajes en el propio móvil, sin paso de subida. Y la regla de recuento la pones tú — 197, 193 o 249 — con seis categorías de visita que deciden cuánto vale una escala.",
        "it":"Nessun account e nessun server: niente in cui accedere e niente da cui restare fuori. Le mappe sono dentro l'app, quindi tutto funziona con la rete spenta. Le foto diventano viaggi sul telefono stesso, senza passaggio di upload. E la regola di conteggio la scegli tu — 197, 193 o 249 — con sei categorie di visita che decidono quanto vale uno scalo.",
        "de":"Kein Konto und kein Server: nichts zum Einloggen und nichts, wovon man ausgesperrt werden kann. Die Karten stecken in der App, also funktioniert alles mit ausgeschaltetem Netz. Fotos werden auf dem Telefon selbst zu Reisen, ohne Upload-Schritt. Und die Zählregel setzt du — 197, 193 oder 249 — mit sechs Besuchsarten, die entscheiden, was ein Zwischenstopp wert ist.",
        "ro":"Fără cont și fără server: nimic în care să te autentifici și nimic din care să fii dat afară. Hărțile vin în aplicație, deci totul funcționează cu rețeaua oprită. Pozele devin călătorii chiar pe telefon, fără pas de încărcare. Iar regula de numărare ți-o setezi tu — 197, 193 sau 249 — cu șase feluri de vizită care decid cât valorează o escală."},
   "p2":{"en":"It also runs on both platforms with the same feature set and the same file format, which matters more than it sounds: a backup written on an iPhone restores on an Android phone and back again.",
         "fr":"Elle tourne aussi sur les deux plateformes avec le même ensemble de fonctions et le même format de fichier, ce qui compte plus qu'il n'y paraît : une sauvegarde écrite sur iPhone se restaure sur Android, et inversement.",
         "es":"Además funciona en las dos plataformas con el mismo conjunto de funciones y el mismo formato de archivo, algo que importa más de lo que parece: una copia escrita en un iPhone se restaura en un Android, y al revés.",
         "it":"Gira anche su entrambe le piattaforme con lo stesso insieme di funzioni e lo stesso formato di file, cosa che conta più di quanto sembri: un backup scritto su iPhone si ripristina su Android, e viceversa.",
         "de":"Sie läuft außerdem auf beiden Plattformen mit demselben Funktionsumfang und demselben Dateiformat, was mehr zählt, als es klingt: Ein auf dem iPhone geschriebenes Backup lässt sich auf einem Android-Telefon wiederherstellen — und umgekehrt.",
         "ro":"Rulează și pe ambele platforme, cu același set de funcții și același format de fișier, ceea ce contează mai mult decât pare: un backup scris pe iPhone se restaurează pe Android, și invers."}},
  {"h":{"en":"Moving from another app","fr":"Migrer depuis une autre app","es":"Migrar desde otra app","it":"Migrare da un'altra app","de":"Von einer anderen App wechseln","ro":"Mutarea de la altă aplicație"},
   "p":{"en":"If your current app exports GPX or KML — most do, somewhere in their settings — Voymark imports the file directly. It splits the result into separate trips where the dates jump, or follows the folder names inside the file, so a five-year export does not arrive as one impossible journey.",
        "fr":"Si votre application actuelle exporte du GPX ou du KML — la plupart le font, quelque part dans les réglages — Voymark importe le fichier directement. Il découpe le résultat en voyages distincts là où les dates sautent, ou suit les noms de dossiers du fichier : un export de cinq ans n'arrive pas comme un seul voyage impossible.",
        "es":"Si tu app actual exporta GPX o KML — casi todas lo hacen, en algún rincón de los ajustes — Voymark importa el archivo directamente. Divide el resultado en viajes separados donde saltan las fechas, o sigue los nombres de carpeta del archivo, así que una exportación de cinco años no llega como un único viaje imposible.",
        "it":"Se la tua app attuale esporta GPX o KML — quasi tutte lo fanno, da qualche parte nelle impostazioni — Voymark importa il file direttamente. Divide il risultato in viaggi separati dove le date saltano, oppure segue i nomi delle cartelle nel file, così un export di cinque anni non arriva come un unico viaggio impossibile.",
        "de":"Wenn deine bisherige App GPX oder KML exportiert — die meisten tun das irgendwo in den Einstellungen —, importiert Voymark die Datei direkt. Es teilt das Ergebnis dort in eigene Reisen, wo die Daten springen, oder folgt den Ordnernamen in der Datei, damit ein Fünf-Jahres-Export nicht als eine einzige unmögliche Reise ankommt.",
        "ro":"Dacă aplicația ta actuală exportă GPX sau KML — mai toate o fac, undeva prin setări — Voymark importă fișierul direct. Împarte rezultatul în călătorii separate acolo unde sar datele sau urmează numele folderelor din fișier, ca un export de cinci ani să nu ajungă drept o singură călătorie imposibilă."},
   "p2":{"en":"If it exports nothing at all, that is the more useful thing this page can tell you — and a reason to check before your next renewal, whichever app you end up with.",
         "fr":"Si elle n'exporte rien du tout, c'est l'information la plus utile de cette page — et une raison de vérifier avant votre prochain renouvellement, quelle que soit l'app que vous garderez.",
         "es":"Si no exporta nada en absoluto, eso es lo más útil que esta página puede decirte — y una razón para comprobarlo antes de tu próxima renovación, sea cual sea la app con la que te quedes.",
         "it":"Se non esporta proprio nulla, quella è la cosa più utile che questa pagina possa dirti — e un motivo per verificarlo prima del prossimo rinnovo, qualunque app tu scelga.",
         "de":"Exportiert sie gar nichts, ist das die nützlichste Auskunft dieser Seite — und ein Grund, das vor der nächsten Verlängerung zu prüfen, für welche App du dich auch entscheidest.",
         "ro":"Dacă nu exportă absolut nimic, acesta e cel mai util lucru pe care ți-l poate spune pagina asta — și un motiv să verifici înainte de următoarea reînnoire, indiferent cu ce aplicație rămâi."}},
 ],
 "faq": [
  {"q":{"en":"What is the best free alternative to Been or Visited?","fr":"Quelle est la meilleure alternative gratuite à Been ou Visited ?","es":"¿Cuál es la mejor alternativa gratuita a Been o Visited?","it":"Qual è la migliore alternativa gratuita a Been o Visited?","de":"Was ist die beste kostenlose Alternative zu Been oder Visited?","ro":"Care e cea mai bună alternativă gratuită la Been sau Visited?"},
   "a":{"en":"We are not a neutral party, so take this as what Voymark does rather than a verdict: the same country map and percentage, plus trips, regions, photo import and every export format, with no subscription. If all you want is a country count and a percentage, Been does that very simply and it is worth the small price to some people.",
        "fr":"Nous ne sommes pas neutres, alors prenez ceci comme ce que fait Voymark plutôt qu'un verdict : la même carte des pays et le même pourcentage, plus les voyages, les régions, l'import photo et tous les formats d'export, sans abonnement. Si vous ne voulez qu'un compteur de pays et un pourcentage, Been le fait très simplement et son petit prix vaut le coup pour certains.",
        "es":"No somos parte neutral, así que tómalo como lo que hace Voymark y no como un veredicto: el mismo mapa de países y porcentaje, más viajes, regiones, importación de fotos y todos los formatos de exportación, sin suscripción. Si solo quieres una cuenta de países y un porcentaje, Been lo hace muy simple y a algunas personas les compensa el precio.",
        "it":"Non siamo una parte neutrale, quindi prendilo come ciò che fa Voymark e non come un verdetto: la stessa mappa dei paesi e la stessa percentuale, più viaggi, regioni, importazione foto e ogni formato di esportazione, senza abbonamento. Se ti basta un conteggio di paesi e una percentuale, Been lo fa molto semplicemente e per alcuni il piccolo prezzo vale.",
        "de":"Wir sind keine neutrale Partei, nimm das also als das, was Voymark tut, nicht als Urteil: dieselbe Länderkarte und derselbe Prozentsatz, dazu Reisen, Regionen, Fotoimport und jedes Exportformat, ohne Abo. Willst du nur eine Länderzahl und einen Prozentsatz, macht Been das sehr schlicht — manchen ist der kleine Preis das wert.",
        "ro":"Nu suntem o parte neutră, așa că ia asta drept ce face Voymark, nu drept verdict: aceeași hartă a țărilor și același procent, plus călătorii, regiuni, import din poze și fiecare format de export, fără abonament. Dacă vrei doar o numărătoare de țări și un procent, Been face asta foarte simplu, iar pentru unii prețul mic merită."}},
  {"q":{"en":"Is there a free alternative to Polarsteps?","fr":"Existe-t-il une alternative gratuite à Polarsteps ?","es":"¿Hay una alternativa gratuita a Polarsteps?","it":"Esiste un'alternativa gratuita a Polarsteps?","de":"Gibt es eine kostenlose Alternative zu Polarsteps?","ro":"Există o alternativă gratuită la Polarsteps?"},
   "a":{"en":"Partly, and it is worth being clear about which part. Voymark reconstructs trips from the photos you took rather than recording your position as you move, so you get the route, the places and the dates after the fact — but not a live GPS track, and not a printed book in the post.",
        "fr":"En partie, et autant être clair sur laquelle. Voymark reconstruit les voyages à partir des photos prises plutôt qu'en enregistrant votre position en chemin : vous obtenez l'itinéraire, les lieux et les dates après coup — mais pas de trace GPS en direct, ni de livre imprimé par la poste.",
        "es":"En parte, y conviene aclarar en qué parte. Voymark reconstruye los viajes a partir de las fotos que hiciste en vez de registrar tu posición mientras te mueves: obtienes la ruta, los lugares y las fechas a posteriori, pero no un track GPS en vivo ni un libro impreso por correo.",
        "it":"In parte, e conviene essere chiari su quale parte. Voymark ricostruisce i viaggi dalle foto che hai scattato invece di registrare la tua posizione mentre ti muovi: ottieni percorso, luoghi e date a posteriori, ma non una traccia GPS dal vivo né un libro stampato per posta.",
        "de":"Teilweise, und man sollte sagen, in welchem Teil. Voymark rekonstruiert Reisen aus den Fotos, die du gemacht hast, statt deine Position unterwegs aufzuzeichnen: Route, Orte und Daten bekommst du im Nachhinein — aber keinen Live-GPS-Track und kein gedrucktes Buch per Post.",
        "ro":"Parțial, și merită spus limpede în ce parte. Voymark reconstruiește călătoriile din pozele pe care le-ai făcut, în loc să-ți înregistreze poziția în timp ce te miști: primești traseul, locurile și datele după aceea — dar nu o urmă GPS în timp real și nici o carte tipărită prin poștă."}},
  {"q":{"en":"Why compare against competitors at all?","fr":"Pourquoi se comparer aux concurrents ?","es":"¿Por qué compararse con la competencia?","it":"Perché confrontarsi con i concorrenti?","de":"Warum überhaupt mit Konkurrenten vergleichen?","ro":"De ce să te compari cu concurenții?"},
   "a":{"en":"Because the honest answer to \"which one should I use\" is sometimes not this one, and a page that pretends otherwise is not worth reading. Naming what the others do better is also the only way the rest of the page earns any trust.",
        "fr":"Parce que la réponse honnête à « laquelle choisir » n'est parfois pas celle-ci, et qu'une page prétendant le contraire ne mérite pas d'être lue. Nommer ce que les autres font mieux est aussi le seul moyen pour le reste de la page d'inspirer confiance.",
        "es":"Porque la respuesta honesta a \"cuál debería usar\" a veces no es esta, y una página que finja lo contrario no merece leerse. Nombrar lo que las demás hacen mejor es además la única forma de que el resto de la página se gane algo de confianza.",
        "it":"Perché la risposta onesta a \"quale dovrei usare\" a volte non è questa, e una pagina che finge il contrario non merita di essere letta. Dire cosa fanno meglio le altre è anche l'unico modo perché il resto della pagina si guadagni fiducia.",
        "de":"Weil die ehrliche Antwort auf \"welche soll ich nehmen\" manchmal nicht diese ist — und eine Seite, die etwas anderes vorgibt, das Lesen nicht wert ist. Zu benennen, was die anderen besser machen, ist außerdem die einzige Art, wie der Rest der Seite Vertrauen verdient.",
        "ro":"Pentru că răspunsul cinstit la „pe care s-o folosesc\" uneori nu este aceasta, iar o pagină care se preface altfel nu merită citită. Să spui ce fac celelalte mai bine este, de altfel, singurul mod în care restul paginii câștigă vreo încredere."}},
  {"q":{"en":"Can I use two of them at once?","fr":"Puis-je en utiliser deux à la fois ?","es":"¿Puedo usar dos a la vez?","it":"Posso usarne due insieme?","de":"Kann ich zwei gleichzeitig nutzen?","ro":"Pot folosi două deodată?"},
   "a":{"en":"Nothing stops you, and GPX or KML is the bridge. Record with whichever app suits the trip, export at the end, import into the other. That is also the cheapest way to test one without committing to a year of it.",
        "fr":"Rien ne l'empêche, et le GPX ou le KML sert de pont. Enregistrez avec l'app qui convient au voyage, exportez à la fin, importez dans l'autre. C'est aussi le moyen le moins cher d'en tester une sans s'engager pour un an.",
        "es":"Nada te lo impide, y GPX o KML es el puente. Registra con la app que le vaya bien al viaje, exporta al final e importa en la otra. Es además la forma más barata de probar una sin comprometerte a un año.",
        "it":"Niente te lo impedisce, e GPX o KML fa da ponte. Registra con l'app che si adatta al viaggio, esporta alla fine, importa nell'altra. È anche il modo più economico di provarne una senza impegnarsi per un anno.",
        "de":"Nichts hindert dich, und GPX oder KML ist die Brücke. Zeichne mit der App auf, die zur Reise passt, exportiere am Ende, importiere in die andere. Das ist auch der billigste Weg, eine auszuprobieren, ohne sich ein Jahr zu binden.",
        "ro":"Nimic nu te oprește, iar GPX sau KML e puntea. Înregistrează cu aplicația potrivită călătoriei, exportă la final, importă în cealaltă. E și cel mai ieftin mod de a testa una fără să te legi pe un an."}},
  {"q":{"en":"Are these prices current?","fr":"Ces prix sont-ils à jour ?","es":"¿Estos precios están actualizados?","it":"Questi prezzi sono aggiornati?","de":"Sind diese Preise aktuell?","ro":"Prețurile acestea sunt actuale?"},
   "a":{"en":"They were checked in July 2026 and are quoted in US dollars; app store prices move and differ by country. Treat them as an order of magnitude, not a quote, and confirm in the store before you buy anything.",
        "fr":"Ils ont été vérifiés en juillet 2026 et sont indiqués en dollars américains ; les prix des stores évoluent et varient selon les pays. Prenez-les comme un ordre de grandeur, pas comme un devis, et confirmez sur le store avant tout achat.",
        "es":"Se comprobaron en julio de 2026 y están en dólares estadounidenses; los precios de las tiendas cambian y varían por país. Tómalos como un orden de magnitud, no como un presupuesto, y confírmalos en la tienda antes de comprar nada.",
        "it":"Sono stati verificati a luglio 2026 e sono indicati in dollari statunitensi; i prezzi degli store cambiano e variano da paese a paese. Prendili come un ordine di grandezza, non come un preventivo, e conferma nello store prima di comprare.",
        "de":"Sie wurden im Juli 2026 geprüft und sind in US-Dollar angegeben; Store-Preise ändern sich und unterscheiden sich je nach Land. Nimm sie als Größenordnung, nicht als Angebot, und prüfe im Store, bevor du etwas kaufst.",
        "ro":"Au fost verificate în iulie 2026 și sunt exprimate în dolari americani; prețurile din magazine se schimbă și diferă de la o țară la alta. Ia-le ca ordin de mărime, nu ca ofertă, și confirmă în magazin înainte să cumperi ceva."}},
 ],
},

}

EXPLORE_SLUGS = ["visited-countries-map", "travel-map", "travel-tracker-app", "country-counter", "travel-photos-to-trips",
                 "how-many-countries-in-the-world", "free-travel-app-no-subscription", "travel-app-alternatives"]
LEGAL_SLUGS = ["privacy", "terms"]
ALL_SLUGS = EXPLORE_SLUGS + LEGAL_SLUGS

SUBPAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta}">
  <meta property="og:type" content="website">
{social}
  <link rel="canonical" href="{canonical}">
{hreflangs}
  <link rel="preload" href="{root}assets/fonts/Marcellus-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}assets/fonts/IBMPlexMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}assets/style.css">
  <link rel="icon" type="image/svg+xml" href="{root}assets/img/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
{jsonld}
</head>
<body>

  <nav class="langnav" aria-label="Language">
{langlinks}
  </nav>

  <header class="hero hero-sub">
    <a class="homelink" href="{home_url}"><span class="stamp stamp-small" aria-hidden="true"><span>VOYMARK</span></span></a>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </header>

  <main>
{shots_band}    <section class="band">
{sections_html}
    </section>
{faq_html}    <section class="band band-alt">
      <div class="cta">
        <a class="badge badge-disabled" href="#" aria-disabled="true">
          <span class="badge-small">{badge_small}</span>
          <span class="badge-large">App&nbsp;Store</span>
        </a>
        <!-- Placeholder: swap href for the Play Store listing at launch. -->
        <a class="badge badge-disabled" href="#" aria-disabled="true">
          <span class="badge-small">{badge_small_android}</span>
          <span class="badge-large">Google&nbsp;Play</span>
        </a>
      </div>
    </section>
  </main>

  <footer>
    <p class="tagline">{tagline}</p>
    <nav class="footnav" aria-label="Site">
{footnav}
    </nav>
    <p>© <span id="year">2026</span> Outside Software SRL. {credits}</p>
  </footer>

  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def url_for(lang):
    return BASE_URL if lang == "en" else f"{BASE_URL}{lang}/"


def page_url(slug, lang):
    return f"{url_for(lang)}{slug}.html"


def hreflang_block(lang_url):
    lines = [f'  <link rel="alternate" hreflang="{l}" href="{lang_url(l)}">' for l in LANGS]
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{lang_url("en")}">')
    return "\n".join(lines)


def langlinks_block(lang, lang_url):
    def link(l):
        cls = ' class="current"' if l == lang else ""
        return f'    <a href="{lang_url(l)}"{cls}>{LANG_LABELS[l]}</a>'
    return "\n".join(link(l) for l in LANGS)


# App screenshots (assets/img/screen-*.png, captured from the real app on
# Appetize). Key → alt-text T key. Order matters.
SHOT_FILES = {
    "map": ("screen-map.png", "shots_alt_map"),
    "passport": ("screen-passport.png", "shots_alt_passport"),
    "timeline": ("screen-timeline.png", "shots_alt_timeline"),
}
INDEX_SHOTS = ["map", "passport", "timeline"]
PAGE_SHOTS = {
    "visited-countries-map": ["map", "passport"],
    "travel-map": ["map", "timeline"],
    "travel-tracker-app": ["timeline", "passport"],
    "country-counter": ["passport", "map"],
    "travel-photos-to-trips": ["timeline", "map"],
}

def shots_html_block(lang, root, keys):
    lines = []
    for key in keys:
        fname, alt_key = SHOT_FILES[key]
        lines.append(
            f'        <figure class="shot"><img src="{root}assets/img/{fname}" '
            f'alt="{T[alt_key][lang]}" loading="lazy" width="360" height="800"></figure>'
        )
    return "\n".join(lines)

def shots_band_block(lang, root, slug):
    keys = PAGE_SHOTS.get(slug)
    if not keys:
        return ""
    return (
        '    <section class="band band-shots">\n'
        f'      <h2>{T["shots_title"][lang]}</h2>\n'
        '      <div class="shots">\n'
        f"{shots_html_block(lang, root, keys)}\n"
        "      </div>\n"
        "    </section>\n"
    )

def faq_band_block(lang, slug):
    """The visible FAQ, mirroring this page's FAQPage JSON-LD exactly.

    Both halves come from the one `faq` list in PAGES, so the marked-up
    answer and the rendered answer can never drift — Google treats
    structured data that isn't on the page as a violation, and it would
    also just be a lie to the reader.
    """
    faq = PAGES[slug].get("faq")
    if not faq:
        return ""
    items = "\n".join(
        f'        <div class="faq-item"><h3>{q["q"][lang]}</h3>'
        f'<p>{q["a"][lang]}</p></div>'
        for q in faq
    )
    return (
        '    <section class="band">\n'
        f'      <h2>{T["faq_title"][lang]}</h2>\n'
        '      <div class="faq">\n'
        f"{items}\n"
        "      </div>\n"
        "    </section>\n"
    )


def footnav_block(lang):
    links = [f'      <a href="{page_url(s, lang)}">{PAGES[s]["nav"][lang]}</a>' for s in EXPLORE_SLUGS]
    links.append(f'      <a href="{page_url("privacy", lang)}">{T["nav_privacy"][lang]}</a>')
    links.append(f'      <a href="{page_url("terms", lang)}">{T["nav_terms"][lang]}</a>')
    return "\n".join(links)


def build_index(lang):
    root = "" if lang == "en" else "../"
    values = {key: T[key][lang] for key in T}
    values["social"] = social_block(
        lang, url_for(lang), T["title"][lang], T["meta"][lang])
    html = TEMPLATE.format(
        lang=lang, root=root,
        canonical=url_for(lang),
        jsonld=jsonld_home(lang),
        hreflangs=hreflang_block(url_for),
        langlinks=langlinks_block(lang, url_for),
        footnav=footnav_block(lang),
        shots_html=shots_html_block(lang, root, INDEX_SHOTS),
        **values,
    )
    out = "index.html" if lang == "en" else f"{lang}/index.html"
    if "/" in out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out)


def build_page(slug, lang):
    page = PAGES[slug]
    root = "" if lang == "en" else "../"
    # A section may carry a second paragraph ("p2"): the landing pages were
    # 245-286 words each, thin enough that search had little to rank and an
    # answer engine had little to quote (SEO audit, 2026-07-31). Two
    # paragraphs let a section actually answer its own heading.
    def section_html(s):
        body = f'<p>{s["p"][lang]}</p>'
        # A bulleted list, for the one thing prose is bad at: naming eight
        # competing apps and what each costs.
        if "list" in s:
            items = "".join(f"<li>{item}</li>" for item in s["list"][lang])
            body += f"<ul>{items}</ul>"
        if "p2" in s:
            body += f'<p>{s["p2"][lang]}</p>'
        return f'      <article class="prose"><h2>{s["h"][lang]}</h2>{body}</article>'

    sections = "\n".join(section_html(s) for s in page["sections"])
    html = SUBPAGE_TEMPLATE.format(
        social=social_block(lang, page_url(slug, lang),
                            page["title"][lang], page["meta"][lang]),
        lang=lang, root=root,
        canonical=page_url(slug, lang),
        jsonld=jsonld_page(slug, lang, page.get("faq")),
        title=page["title"][lang], meta=page["meta"][lang],
        h1=page["h1"][lang], lede=page["lede"][lang],
        sections_html=sections,
        faq_html=faq_band_block(lang, slug),
        shots_band=shots_band_block(lang, root, slug),
        hreflangs=hreflang_block(lambda l: page_url(slug, l)),
        langlinks=langlinks_block(lang, lambda l: page_url(slug, l)),
        footnav=footnav_block(lang),
        home_url=url_for(lang),
        badge_small=T["badge_small"][lang],
        badge_small_android=T["badge_small_android"][lang],
        tagline=T["tagline"][lang],
        credits=T["credits"][lang],
    )
    out = f"{slug}.html" if lang == "en" else f"{lang}/{slug}.html"
    if "/" in out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out)


def last_modified():
    """The date of the last commit, as YYYY-MM-DD.

    Crawlers use <lastmod> to decide what to re-fetch, and a sitemap that
    never carries one gets ignored on that signal (SEO audit, 2026-07-31).
    Every page here is regenerated by this script from one source, so they
    genuinely all change together — a single site-wide date is the honest
    answer, not a per-file fiction. Falls back to today outside a
    checkout.
    """
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if len(out) == 10:
            return out
    except Exception:
        pass
    import datetime
    return datetime.date.today().isoformat()


def build_sitemap():
    stamp = last_modified()
    urls = []
    for lang in LANGS:
        urls.append((url_for(lang), "1.0"))
        for slug in ALL_SLUGS:
            # The keyword landing pages are what search should reach for;
            # privacy and terms are required reading, not entry points.
            priority = "0.3" if slug in LEGAL_SLUGS else "0.8"
            urls.append((page_url(slug, lang), priority))
    body = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{stamp}</lastmod>"
        f"<changefreq>monthly</changefreq><priority>{p}</priority></url>"
        for u, p in urls
    )
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f"{body}\n</urlset>\n")
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    for lang in LANGS:
        build_index(lang)
        for slug in ALL_SLUGS:
            build_page(slug, lang)
    build_sitemap()
