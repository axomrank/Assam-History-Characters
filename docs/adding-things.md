# Adding things (step by step)

Always finish with `python3 tools/build.py && python3 tools/check.py`, then commit. Column meanings: `data/README.md`.
Needs Python 3 and Pillow (`pip install pillow`).

## A new person
1. Add a `person` row to `data/assam_history.csv`: `id` (kebab-case), `name`, `period`, `group` (the dynasty heading it sits under), `date_label`, `start_year`, `end_year`, `sort_year`, `role`, `summary`, `sources`.
2. Kings of the Ahom or Koch lists also need `ahom_king_no` / `koch_no`.
3. Build. The person appears at `#/c/<id>` even without images.

## Character sheet images
1. Put the file in `incoming/` as `incoming/<person-id>/<anything>.png`, or `incoming/<person-id>__turnaround.png` (kinds: turnaround, face, costume, props, palette, pose, portrait).
2. `python3 tools/add_sheets.py` (`--dry-run` first). It writes the WebP and thumbnail to `media/characters/<id>/`, moves the original to `masters/sheets/<id>/` and fills `character_sheets`.
3. Add captions in the CSV if you like, then build.

## A new scene
1. Add a `scene` row: `id` (like `AHOM-120`), `name`, `period`, `group`, `date_label`, `sort_year`, `summary`, `notes`, `confidence`, `people`, `main_people`, `places`, `sources`, `collection`.
2. Not painted yet: `status` = `planned`, empty `scene_image` (the site shows a placeholder). Painted: save the WebP as `media/scenes/<group>/<era>/<ID>.webp` plus `thumb/<ID>.webp`, keep the PNG in `masters/scenes/<era>/`, set `scene_image` and `status` = `illustrated`.
3. Read `research/ahom/agent-guidance.md` first when making images (costume and temple/royal/funerary rules). It is on the `archive` branch (see `MIGRATION.md`).

## A new place
Add a `place` row: `name`, `group` (kind), `also_called` (old names), `present_name`, `location`, `lat`, `lon`, `confidence`, `sources`. Scenes and events link to it through their `places` column. Method and known doubts: `research/places/README.md` (archive branch).

## A kingdom's extent (realm)
A `realm` row whose `group` is the kingdom's place id, with `date_label`, `boundary` text and `limit_*` rules. Disagreements between sources go in `notes`.

## An event
An `event` row: `name`, `start_year`, `sort_year`, `summary`, `people`, `places`, `sources`.

## The Map tab
Not data-driven from the CSV. See `map/README.md`.

## Before you commit
- `python3 tools/build.py` and `python3 tools/check.py` pass.
- Nothing in the published folders implies commercial use; the licence is CC BY-NC-ND (content) and PolyForm NC (code).
- Do not commit `masters/`, `research/`, `reels/`, `incoming/*` (git-ignored on purpose; they live on the `archive` branch).
