# Voymark — SEO keyword focus list

Last updated: 2026-07-31. Owned pages are relative to the site root; every
page also exists under /fr /es /it /de /ro.

## How to read this

Each cluster maps to exactly one landing page so we never compete with
ourselves. The home page carries the brand + generic head terms; the eight
explore pages each own one intent; privacy/terms exist for trust queries
and are kept indexed because "voymark privacy" searches should land on our
own words.

## Cluster 1 — brand (index.html)

- voymark
- voymark app
- voymark travel tracker
- voymark passport app

## Cluster 2 — visited countries map (visited-countries-map.html)

Primary: **visited countries map**
- map of countries i have visited
- mark countries visited on world map
- scratch map alternative app
- world map travel tracker
- interactive visited countries map free
- countries been to map

## Cluster 2b — travel map (travel-map.html)

Primary: **travel map**
- travel map app
- personal travel map
- my travel map
- world travel map with routes
- map of my travels
- travel map with photos

## Cluster 3 — travel tracker app (travel-tracker-app.html)

Primary: **travel tracker app**
- travel tracker app no account
- offline travel tracker
- travel diary app private
- trip log app free
- travel journal app without subscription
- app to track countries visited

## Cluster 4 — country counter (country-counter.html)

Primary: **country counter**
- how many countries have i visited
- country counter app
- count countries visited
- does a layover count as visiting a country
- percentage of world visited calculator

## Cluster 5 — photos to trips (travel-photos-to-trips.html)

Primary: **turn travel photos into trips**
- organize travel photos by trip
- travel timeline from photos
- app that finds trips in photos
- travel photo organizer private
- reconstruct past trips from photos

## Cluster 6 — how many countries (how-many-countries-in-the-world.html)

Primary: **how many countries are there in the world**
- 193 vs 197 vs 249 countries
- how many countries are in the un
- is taiwan a country
- difference between a country and a territory
- has anyone visited every country

Informational, not product. It is the highest-volume question this
category owns and the one an answer engine is most likely to quote from,
which is why it carries the fullest FAQ block on the site. It hands off to
Cluster 4 for the "does a layover count" follow-up rather than answering
it twice.

## Cluster 7 — free, no subscription (free-travel-app-no-subscription.html)

Primary: **free travel app no subscription**
- travel tracker without subscription
- travel app no account
- free travel diary app no ads
- does voymark sell my data

Every competitor charges, so price is the conversion argument and deserves
its own page rather than a footnote on someone else's.

## Cluster 8 — alternatives (travel-app-alternatives.html)

Primary: **polarsteps alternative**
- been app alternative
- visited app alternative
- free alternative to polarsteps
- travel app comparison price

## Cross-cutting modifiers (used in copy, not standalone pages)

These qualify Voymark against competitors in body copy and meta
descriptions everywhere: **offline**, **no account**, **no subscription**,
**private / on-device**, **free**, **passport stamp**.

## Per-locale head terms

Translating an English keyword does not produce the phrase a native
speaker types, and the previous version of this file assumed it did
("six-language parity means … are covered for free"). It is not free. A
German looking for a digital scratch map types **Rubbelkarte**, which no
translation of "scratch map" would ever produce; a French traveller
looking for a travel diary types **carnet de voyage**, not "journal de
voyage". The non-English titles and H1s target the columns below, not a
rendering of the English one.

| Intent | FR | ES | IT | DE | RO |
|---|---|---|---|---|---|
| scratch map | carte à gratter | mapa rascable | mappa da grattare | Rubbelkarte | hartă răzuibilă |
| visited countries map | carte des pays visités | mapa de países visitados | mappa dei paesi visitati | besuchte Länder Karte | harta țărilor vizitate |
| travel journal | carnet de voyage | diario de viaje | diario di viaggio | Reisetagebuch | jurnal de călătorie |
| my travel map | carte du monde de mes voyages | mapa de mis viajes | mappa dei miei viaggi | Weltkarte meiner Reisen | harta călătoriilor mele |
| tick off countries | — | — | — | Länder abhaken | — |
| how many countries have I visited | combien de pays ai-je visités | cuántos países he visitado | quanti paesi ho visitato | wie viele Länder habe ich besucht | câte țări am vizitat |
| how many countries in the world | combien de pays dans le monde | cuántos países hay en el mundo | quanti paesi ci sono nel mondo | wie viele Länder gibt es auf der Welt | câte țări sunt în lume |
| sort travel photos | trier ses photos de voyage | organizar fotos de viaje | organizzare le foto di viaggio | Reisefotos sortieren | organizarea pozelor de călătorie |
| free, no subscription | gratuite sans abonnement | gratis sin suscripción | gratis senza abbonamento | kostenlos ohne Abo | gratuit fără abonament |

Three coinages were retired for being a translator's inventions rather
than search terms: German "Länderzähler", Romanian "Numărător de țări"
and German "Reiselog". The first two became the question a person
actually asks; the third became "Reisetagebuch".

## Notes

- Competitor trademarks are referenced generically everywhere except
  `travel-app-alternatives`, where naming them is the point of the page
  and is how the query itself is phrased ("polarsteps alternative"). That
  page states each competitor's strengths and dates its prices; an unfair
  comparison page is worth less than no page at all.
- When the Play Store listing goes live, add "voymark android" to
  Cluster 1 and swap the placeholder badge href (see build_i18n.py).
- Structured data: every page carries Organization + WebSite +
  SoftwareApplication; the six explore pages add FAQPage. No
  aggregateRating until there are real reviews.
