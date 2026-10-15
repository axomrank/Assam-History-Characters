# Assam history character sheets

A static library of character sheets for the people of Assam's history, from Pushyavarman to Tarun Gogoi,
with the historical scenes they appear in. Live at https://axomrank.github.io/Assam-History-Characters/.
Open `index.html`, or serve the folder with `python3 -m http.server`.

## One file holds all the data

`data/assam_history.csv` is the only source of data. Each row is one record, and the `type` column says which:

| type | rows | what it is | key columns |
|---|---|---|---|
| `period` | 7 | a period of Assam's history | `date_label`, `start_year`, `end_year`, `summary`, `group_order` (order of groups on the page) |
| `person` | 328 | a person | `period`, `group`, dates, `role`, `summary`, `notes`, Tai and Hindu names, `ahom_king_no`, `koch_no`, `confidence`, `sources` |
| `image` | 31 | a character sheet or portrait | `person`, `kind`, `file`, `thumbnail`, `width`, `height`, `added` |
| `event` | 24 | a dated event on the Timeline page | `start_year`, `end_year`, `summary`, `people` |
| `scene` | 265 | an illustrated scene | `date_label`, `sort_year`, `group` (era), `summary`, `people`, `main_people`, `file`, `thumbnail` |

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
    characters[]               every person field, plus image_level
      images[]                 their sheets and portraits
      events[]                 timeline events they took part in
      scenes[]                 scenes they appear in; main = true when the scene is about them
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
   `media/characters/<id>/`, keeps your original in `archive/sheet-originals/<id>/`, adds an `image` row
   under that person in the CSV and rebuilds.

## Folders
```
index.html, favicon.svg      the site's entry page (must stay at the root for GitHub Pages)
assets/                      app.css and app.js
data/assam_history.csv       all the data
data/site.js                 generated from the CSV; the website loads this
data/assam_history.json      generated from the CSV: periods > dynasties > characters > events, scenes
media/characters/<id>/       character sheets and portraits, with thumb/
media/scenes/ahom/<era>/     Ahom chronology scenes, one folder per era, with thumb/
media/scenes/gallery/<topic>/ the Assamese AI gallery by topic, with thumb/
tools/build.py               CSV -> site.js
tools/add_sheets.py          add new character images
incoming/                    drop folder for new images
archive/                     local only, git-ignored: PNG originals and retired files
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
