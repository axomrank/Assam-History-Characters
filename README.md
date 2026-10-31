# Assam history character sheets

A static library of character sheets for the people of Assam's history, from Pushyavarman to Tarun Gogoi,
with the historical scenes they appear in. Live at https://axomrank.github.io/Assam-History-Characters/.
Open `index.html`, or serve the folder with `python3 -m http.server`.

## One file holds all the data

`data/assam_history.csv` is the only source of data. Each row is one record, and the `type` column says which:

| type | rows | what it is | key columns |
|---|---|---|---|
| `period` | 7 | a period of Assam's history | `date_label`, `start_year`, `end_year`, `summary`, `group_order` (order of groups on the page) |
| `person` | 328 | a person | `period`, `group`, dates, `role`, `summary`, `notes`, Tai and Hindu names, `ahom_king_no`, `koch_no`, `confidence`, `sources`, `character_sheets` |
| `event` | 24 | a dated event on the Timeline page | `start_year`, `end_year`, `summary`, `people`, `places`, `scene_image` (optional) |
| `realm` | 20 | a kingdom's extent in one era, bounded by rivers and landmarks | `group` (the kingdom's place id), `boundary` ("West: ... \| East: ..."), `limit_west` / `limit_east` / `limit_north` / `limit_south` (what the map shades between; north and south are used where the Brahmaputra splits a kingdom into north-bank and south-bank parts: `river:<id>` from `data/maps/assam.json`, `place:<id>` with lat/lon, `ridge:patkai` or `lon:<degrees>`; empty = none named), `places` (the rivers and landmarks), `notes` (disputes), `confidence`, `sources` |
| `place` | 186 | a place: historic names, present-day name and location, kind, how sure the identification is | `also_called`, `present_name`, `location`, `group` (kind), `confidence`, `sources` |
| `scene` | 331 | an illustrated scene, or a researched one not painted yet (`status` = `planned`) | `date_label`, `sort_year`, `group` (era), `summary`, `people`, `main_people`, `places` (place ids), `scene_image` |

A person whose sheet is researched but not drawn yet can carry a design brief in `sheet_brief`, written as
`appearance: … | costume: … | props: … | avoid: …`. The site then shows a hatched "Sheet planned" placeholder for them and
puts the brief under Reference notes, where the "Copy reference brief" button copies it for an image tool.

Images live inside the record they belong to. A person's `character_sheets` cell lists their sheets and
portraits as `path | caption`, for example
`media/characters/sukaphaa/pose-1.webp | Chaolung Sukapha on Royal Throne (Profile)`. The kind (portrait, pose,
turnaround, face...) is the start of the file name, and the size is read from the file. A scene or event has
one `scene_image`. Every thumbnail is the same file name in the `thumb/` folder beside the image.

A scene that is researched but not painted yet has `status` set to `planned` and no `scene_image`. The site shows it
as a placeholder card, and its viewer shows the description, notes, confidence and sources as a brief for the
painter. To add the painting later, put the WebP (and its thumbnail) in the scene's era folder, fill in
`scene_image`, set `status` to `illustrated` and rebuild. Scenes are shown in date order: by the era in `group`, then
`sort_year` (or the first year in `date_label`).

Lists inside a cell (people, sources, king numbers, group order) are separated by `; `.
`people` and `main_people` hold person ids, so a scene links to everyone in it and is "about" its main people.
Open the file in any spreadsheet program; save it as CSV in UTF-8 so the Assamese names survive.

After editing, rebuild what the website loads:

```
python3 tools/build.py
```

It writes `data/site.js` (what the website loads) and `data/assam_history.json`, works out which people have
images from the files on disk, and stops with a list of errors if an id is unknown or an image file is missing.
Do not edit either generated file by hand.

`data/assam_history.json` holds the same data nested for reading or for other tools:

```
periods[]                      id, name, Assamese name, dates, summary
  dynasties[]                  name, first and last year
    characters[]               every person field, plus sheet_status (sheet, portrait, scenes or none)
      character_sheets[]       their sheets and portraits: kind, caption, image, thumbnail, size
      events[]                 timeline events they took part in, each with its scene_image if it has one
      scenes[]                 scenes they appear in, each with its scene_image; main = true when the scene is about them
scenes_without_characters[]    the 29 scenes that link nobody
```
A scene with several people appears under each of them. People of the colonial and modern periods have no
dynasty, so they sit in a group named after the period.

## Image availability

| Level | Meaning |
|---|---|
| sheet | a real sheet: turnaround, face, costume, props or palette |
| portrait | a portrait or pose, but no sheet |
| scenes | appears in scenes only |
| none | nothing yet |

## Add character sheets
1. Put images in `incoming/`, as `incoming/<person-id>/<kind>.png` or `incoming/<person-id>__<kind>.png`.
   Kinds: `turnaround`, `face`, `costume`, `props`, `palette`, `pose`, `portrait`, `other`.
   The Coverage page lists every person id.
2. Run `python3 tools/add_sheets.py` (add `--dry-run` to preview). It writes a WebP and a thumbnail to
   `media/characters/<id>/`, keeps your original in `masters/sheets/<id>/`, adds it to that person's
   `character_sheets` cell in the CSV and rebuilds. Add a caption after the path in the spreadsheet if you like.

## Folders
Published (these go to GitHub Pages):
```
index.html, favicon.svg      the site's entry page (must stay at the root)
assets/                      app.css and app.js
data/assam_history.csv       all the data
data/site.js, .json          generated from the CSV by tools/build.py
media/characters/<id>/       published sheets and portraits (WebP), with thumb/
media/scenes/<group>/<era>/  published scenes (WebP), with thumb/
tools/                       build.py (CSV -> site.js), add_sheets.py (add images), index_library.py (rebuild INDEX.csv)
```
Local only (git-ignored; see `AGENTS.md` for the full map):
```
masters/     lossless PNG originals of the published sheets and scenes (sheets/<id>/, scenes/<era>/)
drafts/      anything held back from publishing
research/    all research, sources, prompts and notes, by dynasty (varman, salastambha, pala, ahom, image-library)
images/      generated scene/object library, 825 real photographs with licences, face crops
reels/       the 49 Ahom reels (web/) and their editing projects (studio/)
incoming/    drop folder for new images
INDEX.csv    one row per image or document in the project
```
Site routes: `#/`, `#/characters`, `#/c/<id>`, `#/kings`, `#/timeline`, `#/scenes`, `#/coverage`, `#/about`.

The research files, import scripts and older JSON data this CSV was made from were removed on 2026-10-15;
they remain in the git history.

## Design
Historical minimalism taken from Assamese manuscript painting: sanchi-pat bark paper, lampblack ink,
hengul (vermilion) as the one accent and haital (orpiment yellow) to mark which characters have images.
Type is Tiro Bangla for both Latin and Assamese script, loaded from Google Fonts with local serif fallbacks.
The site follows the system light or dark setting.

Each dynasty or house has one colour, used on cards, headings, the home ribbon, kings tables, the timeline and
scenes: Ahom blue, Koch saffron, Varman lac red, Salastambha umber, Pala olive, Kamata plum, Bhuyan slate,
Chutia green, Dimasa teal, Jaintia and Manipur rose, outside powers ash, saints and poets violet, colonial brown,
modern slate-ink. Groups map to houses in `HOUSES` in `assets/app.js`; the colours are the `.h-<house>` rules in `assets/app.css`.

## Licence

For non-commercial use only. Images and text: CC BY-NC-ND 4.0 (`LICENSE-CONTENT.txt`); code: PolyForm Noncommercial 1.0.0
(`LICENSE-CODE.md`); summary and exclusions (the MOD-06 photograph, map data, fonts) in `LICENSE` and on the site's
`#/licence` page.

## Sharing, search and offline

`python3 tools/build.py` also writes `c/<person-id>/index.html` (one small page per person with Open Graph tags for link previews,
which sends visitors on to `#/c/<id>`), `sitemap.xml` and `robots.txt`, and stamps `sw.js` with a version. `manifest.webmanifest`
and `sw.js` make the site installable and readable offline (the app, data and any images already viewed). `assets/og.jpg` is the
home-page preview image. The `#/map` page draws the places that have `lat`/`lon` on the Assam outline from `data/maps/`.
