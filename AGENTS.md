# Project map for AI agents

Static site of character sheets and scenes for Assam's history. Start with `INDEX.csv`: one row per image or document
(`path, area, kind, subject, era, status, width, height, kb`). Filter it instead of walking folders.
Rebuild it after adding files: `python3 tools/index_library.py`.

## Where things are
| Need | Look in |
|---|---|
| The data (people, events, scenes) | `data/assam_history.csv` only; `python3 tools/build.py` regenerates `data/site.js` and `.json` |
| Published character sheets | `media/characters/<person-id>/<kind>-N.webp` (+ `thumb/`) |
| Published scenes | `media/scenes/<group>/<era>/<SCENE-ID>.webp` (+ `thumb/`) |
| Lossless PNG original of a published sheet/scene | `masters/sheets/<id>/`, `masters/scenes/<era>/` |
| Unapproved drafts, older versions | `drafts/<dynasty>/` |
| Research notes, sources, prompts (ALL notes live here) | `research/<varman|salastambha|pala|ahom|image-library>/` (see `research/README.md`; images/ layout guide: `research/image-library/images-guide.md`) |
| Generated scene/object library (c15, c18, 1950s, 1990s, now; textiles, jewellery, plants …) | `images/scenes/`, `images/elements/` |
| Real reference photos with licences | `images/photos/<site>/`, `images/photos/manifest.csv` |
| Face crops of Ahom people (127) | `images/faces/<id>.webp` |
| Ahom reels (video) | `reels/web/NN-name.mp4` + `.webp` poster (49 reels), `reels/web/context/` captions (`.as.vtt`, `.en.vtt`), `reels/studio/reel-NNN-*/` HyperFrames projects (each has its own AGENTS.md) |
| Drop new character images here | `incoming/` then `python3 tools/add_sheets.py` |

## Rules
- Before making images read `research/ahom/agent-guidance.md` (reference-selection and costume rules).
- Notes go in `research/`, never beside images. Only README.md and AGENTS.md stay at the root.
- Published = `index.html`, `assets/`, `data/`, `media/`, `tools/`. `reels/` is local too. Everything else is local and git-ignored (rights of photos/references are not cleared).
- Never put images in the CSV as separate records; they belong to a person (`character_sheets`) or a scene (`scene_image`).
- Ids are kebab-case (`bala-varman`); the person id is the folder name under `media/characters/` and `masters/sheets/`.
- `status` in INDEX.csv: published, master, draft, generated, reference, research.
- Generated images are interpretations, not evidence. Keep Hindu temple photos apart from Ahom royal/civic and funerary ones.
