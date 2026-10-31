# Map shapes

Copied from the AHOM project (`assets/maps/`) on 2026-10-26. These are **modern reference geography**, not historical borders.
Every coordinate is `[latitude, longitude]`.

| File | What it holds | Source and licence |
|---|---|---|
| `assam.json` | 33 district polygons, 41 river paths (the Sisi and the Teesta/Karatoya was added 2026-10-31 from the user's own "Assam Rivers.kml") (Brahmaputra, Dihing, Dikhow and others), and an approximate Patkai ridge | Local KMZ `Dist + Rivers (simplified).kmz`. The licence of that file is not recorded; check it before wider reuse. |
| `boundaries.json` | Outline rings for Assam (dissolved from the district polygons) and India | India: [DataMeet Community Maps, india-soi.geojson](https://github.com/datameet/maps/blob/master/Country/india-soi.geojson), from Survey of India / Census 2011 geometry, simplified. **CC BY-SA 2.5 / ODbL: keep the attribution.** |
| `world.json` | 258 country and territory outlines | [Natural Earth 1:10m admin-0 countries](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/), public domain, simplified at 0.012 degrees. |

## Spots

The map spots are not a separate file. They are the `lat` and `lon` columns of the `place` rows in `data/assam_history.csv`
(186 places; 127 have a point, from the AHOM map catalogue; its separate "Rangpur" spot is the same town as Sivasagar). Each point is an approximate catalogue reference point, not a surveyed
location: it marks "about here" for a named place, region or river. `data/site.js` carries it as `geo: [lat, lon]` on each place.

Not brought over: the AHOM map renderer (`map.js`) and the event routes (`map-stories.json`).
