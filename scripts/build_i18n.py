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
{hreflangs}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/style.css">
  <link rel="icon" type="image/svg+xml" href="{root}assets/img/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
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
   "p":{"en":"The classic \"world\" list has 197 countries; the UN recognizes 193 members; ISO lists 249 countries and territories. Voymark supports all three definitions, and every number in the app — passport, stats, continents, share cards — follows the one you choose.",
        "fr":"La liste « monde » classique compte 197 pays ; l'ONU reconnaît 193 membres ; l'ISO recense 249 pays et territoires. Voymark prend en charge les trois définitions, et chaque nombre de l'app — passeport, stats, continents, cartes — suit celle que vous choisissez.",
        "es":"La lista clásica del \"mundo\" tiene 197 países; la ONU reconoce 193 miembros; la ISO lista 249 países y territorios. Voymark admite las tres definiciones, y cada número de la app — pasaporte, estadísticas, continentes, tarjetas — sigue la que elijas.",
        "it":"La classica lista \"mondo\" ha 197 paesi; l'ONU riconosce 193 membri; l'ISO elenca 249 paesi e territori. Voymark supporta tutte e tre le definizioni, e ogni numero dell'app — passaporto, statistiche, continenti, card — segue quella che scegli.",
        "de":"Die klassische \"Welt\"-Liste hat 197 Länder; die UN erkennt 193 Mitglieder an; die ISO führt 249 Länder und Territorien. Voymark unterstützt alle drei Definitionen — und jede Zahl in der App folgt der, die du wählst.",
        "ro":"Lista clasică a \"lumii\" are 197 de țări; ONU recunoaște 193 de membri; ISO listează 249 de țări și teritorii. Voymark suportă toate cele trei definiții, iar fiecare număr din aplicație — pașaport, statistici, continente, carduri — o urmează pe cea aleasă de tine."}},
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
 ],
},

}

EXPLORE_SLUGS = ["visited-countries-map", "travel-map", "travel-tracker-app", "country-counter", "travel-photos-to-trips"]
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
{hreflangs}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/style.css">
  <link rel="icon" type="image/svg+xml" href="{root}assets/img/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
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
    <section class="band band-alt">
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

def footnav_block(lang):
    links = [f'      <a href="{page_url(s, lang)}">{PAGES[s]["nav"][lang]}</a>' for s in EXPLORE_SLUGS]
    links.append(f'      <a href="{page_url("privacy", lang)}">{T["nav_privacy"][lang]}</a>')
    links.append(f'      <a href="{page_url("terms", lang)}">{T["nav_terms"][lang]}</a>')
    return "\n".join(links)


def build_index(lang):
    root = "" if lang == "en" else "../"
    values = {key: T[key][lang] for key in T}
    html = TEMPLATE.format(
        lang=lang, root=root,
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
    sections = "\n".join(
        f'      <article class="prose"><h2>{s["h"][lang]}</h2><p>{s["p"][lang]}</p></article>'
        for s in page["sections"]
    )
    html = SUBPAGE_TEMPLATE.format(
        lang=lang, root=root,
        title=page["title"][lang], meta=page["meta"][lang],
        h1=page["h1"][lang], lede=page["lede"][lang],
        sections_html=sections,
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


def build_sitemap():
    urls = []
    for lang in LANGS:
        urls.append(url_for(lang))
        for slug in ALL_SLUGS:
            urls.append(page_url(slug, lang))
    body = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
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
