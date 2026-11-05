# data/

| File | What | Edit? |
|---|---|---|
| `assam_history.csv` | **The one source of truth**: periods, people, events, places, realms and scenes, one row each | yes |
| `site.js` | What the website loads (generated) | no |
| `assam_history.json` | Same data nested period > dynasty > person > scenes (generated) | no |

After any edit: `python3 tools/build.py` (rebuilds the two generated files, `c/`, `sitemap.xml`, `sw.js` stamps), then `python3 tools/check.py`.
The Map tab has its own separate data in `map/data/` (see `map/README.md`); it does not read this CSV.

## Rules for the CSV
- Open with a spreadsheet or edit as text. UTF-8 with BOM, comma separated, keep the header row and column order (`build.py` `COLS`).
- `type` says what a row is. `id` is unique **within a type**, kebab-case (`lachit-borphukan`); scene ids look like `VARMAN-01`.
- Lists inside a cell are separated by `; `. Years are plain numbers (negative not used). Leave a cell empty rather than writing "unknown".
- Never add an image as its own row: it belongs to a person (`character_sheets`) or a scene (`scene_image`).
- Keep `sources` (URLs, `; `-separated), `confidence` (high / medium / low) and `notes` honest. Say so when something is uncertain.

## Columns by row type (✓ = used, * = required)
| Column | period | person | event | place | realm | scene | Meaning |
|---|---|---|---|---|---|---|---|
| `id` | ✓* | ✓* | ✓* | ✓* | ✓* | ✓* | unique id within the type |
| `name`, `name_assamese` | ✓ | ✓* | ✓* | ✓* | ✓* | ✓* | display names |
| `period` | | ✓ | | | ✓ | ✓ | id of a `period` row (kamarupa, western, ahom...) |
| `group` | | ✓ | | ✓ | ✓ | ✓ | person/scene: dynasty or house heading; place: kind (River, Capital, Fort...); realm: the kingdom's **place id** |
| `date_label`, `start_year`, `end_year`, `sort_year` | ✓ | ✓ | ✓ | | ✓ | ✓ | text date, numeric span, and the year used to order things |
| `role`, `summary`, `notes` | | ✓ | ✓ | ✓ | ✓ | ✓ | what they are / short text / caveats and disagreements |
| `tai_name`, `hindu_name`, `also_called` | | ✓ | | ✓ | | | alternative names (searched by the site) |
| `relation`, `fate`, `consort`, `marital_status` | | ✓ | | | | | family and end of reign |
| `ahom_king_no`, `koch_no`, `koch_branch` | | ✓ | | | | | position in the king lists |
| `confidence`, `approx_dates`, `status` | | ✓ | | ✓ | ✓ | ✓ | `status` of a scene: illustrated or planned |
| `people`, `main_people` | | | ✓ | | | ✓ | person ids involved / who it is about |
| `places` | | | ✓ | | ✓ | ✓ | place ids (appear on the place pages and in search) |
| `collection`, `group_order` | ✓ | | | | | ✓ | scene collection name; period: order of groups on the page |
| `character_sheets` | | ✓ | | | | | `path | caption; path | caption` for images in `media/characters/<id>/` |
| `scene_image` | | | ✓ | | | ✓ | `media/scenes/<group>/<era>/<ID>.webp` |
| `sheet_brief` | | ✓ | | | | | brief for generating the sheet |
| `present_name`, `location`, `lat`, `lon` | | | | ✓ | | | today's name, where, and a rough point for the map |
| `boundary`, `limit_west/east/north/south` | | | | | ✓ | | kingdom extent described by rivers and landmarks (`river:<id>`, `place:<id>`, `lon:<deg>`, `>` chains) |
| `sources` | | | ✓ | ✓ | ✓ | ✓ | URLs |

`tools/build.py` documents the same rows in its header and fails the build on unknown ids or missing files.

## Common tasks
See `../docs/adding-things.md`.
