# map/ — the Map tab

A self-contained static app ("Assam Through Time", 350 CE to today). The site's `#/map` page shows `map/index.html` in an iframe.
It has **its own data** and does not read `data/assam_history.csv`.

- `index.html`, `sankardeva.html`, `app/` — plain browser scripts, no build step needed to run.
- `data/generated/atlas.js` — what the app loads; **generated, never edit**.
- `data/maps/` — reference geography (districts, rivers, outlines) with sources in `data/maps/README.md`.
- `data/features/sankardeva/` — pilgrimage routes.
- Maintained in its own project (`/home/angsuman/extra_spac/MAP`, with editable sources in `data/source/`, build with `npm run build`, checks with `npm run check`). To update the tab, rebuild there and copy `index.html`, `sankardeva.html`, `favicon.svg`, `app/`, `data/generated/`, `data/maps/` and `data/features/sankardeva/` into this folder.
- A map proxy or campaign route is not proof of territorial control; keep source caveats.
Preview: `python3 -m http.server 8000` in the repo root, then open `#/map`.
