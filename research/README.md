# research/ — all research, sources, prompts and notes

Local only (git-ignored). Images live elsewhere: `../masters/` (originals of published items), `../drafts/` (unapproved or older versions), `../images/` (library).

| Folder | Contents |
|---|---|
| `varman/` | Varman dynasty (350–655). `dossier/` = RESEARCH.md, SOURCE_REGISTER.md, ATTIRE_AND_CHARACTER_PLAN.md and source page excerpts; `CHARACTER_SHEET_BRIEF.md`; `SOURCES_AND_RIGHTS.md`; `sources/` = Gait 1906, Epigraphia Indica 12 and 31, Shin paper, reference photos (rights unchecked); `notes/` = per-character design notes and scene reconstruction notes; `prompts/sheets/`, `prompts/scenes/` = image prompts (`VARMAN-NN.prompt.txt`) |
| `salastambha/` | `king-research-and-costume-direction.md`, `nepal-references/`, `notes/` (batch and scene research), `prompts/` (prompts and source lists) |
| `pala/` | `notes/` (research and reconstruction notes), `prompts/`, `references/` (user photos used for PALA-01) |
| `ahom/` | Ahom period (from the AHOM repo, 2026-10-26). `people/<id>/` = generation prompts, reference/design notes, scene references (81 people); `batches/<batch>/` = briefs and per-scene generation prompts; `scenes/`; `reports/` = batch research and completion notes (Moamoria, Burmese, Mughal, officers, missing events); `reels/` = reel notes; `prompts/`; `data/` = AHOM repo's eras (chapter text), explore paths, map sites and stories, life catalogue, reel context; `agent-guidance.md` = the AHOM repo's rules for image creation (temple vs royal vs funerary separation, no 18th-c. masonry in 15th-c. scenes, Bhuyan/Kachari costume directions); `AHOM-repo-README.md` |
| `western-assam-1100-1515/` | The 1100–1515 gap (Kamata, Khen, Bhuyans, Bengal sultanate, Koch rise): `storyline.md` (chapters, chronology, disputes, painter notes), `planned-scenes.csv` (27 proposed scene rows, KAMATA-01 to 27, same columns as the master CSV), `sources.md` |
| `koch-chutia-1350-1616/` | Chutia kingdom (c. 1350–1524), undivided Koch kingdom (1515–1587), Koch Hajo (1581–1616): `storyline.md` (the story in chapters with scene ids, disputes, painter notes), `scenes.py` (single source of the 46 planned scenes; writes `planned-scenes.csv` and adds rows to the master CSV), `chutia-character-sheets.md` (briefs for 8 Chutia sheets), `sources.md` |
| `koch-branches-1590-1956/` | Darrang, Beltola, Bijni and Khaspur (research only; taken off the site 2026-10-28): `storyline.md` (chronology, possible scenes DARR/BELT/BIJN/KHAS, sources), `people.csv` (the 37 removed person records, master-CSV columns) |
| `storyline-gaps-1468-2011/` | Scenes the storyline needed and lacked: bhakti movement, Dimasa, Manipur and Jaintia, colonial Assam, Assam since independence. `storyline.md`, `scenes.py` (single source of 42 planned scenes), `planned-scenes.csv` |
| `places/` | `README.md`: how the gazetteer (the `place` rows of the CSV) was made, which identifications are low confidence, known conflicts |
| `image-library/` | `prompts/<era>/`: prompts and notes for the scenes and objects in `../images/`; `images-guide.md` explains the images/ layout and naming |

Where a finding is used in the site, it is in `data/assam_history.csv` (`sources`, `notes`, `confidence` columns). Notes that cite these files say "research/…".
