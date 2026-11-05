# Where things went (2026-11)

| Was | Now |
|---|---|
| Old Map tab (SVG code in `assets/app.js`, `data/maps/`, polygon-clipping) | Removed. The Map tab shows `map/` (Assam Through Time). `place`/`realm` rows stay in the CSV for place pages and search |
| `images/` (scene/object library, photos with licences, Ahom face crops) | Moved out to a separate local repo `assam` (present-day Assam). Not in this repo |
| `masters/`, `research/`, `reels/` (local only before) | On the `archive` branch of this repo: `git clone -b archive <repo-url> assam-history-archive` or `git worktree add ../archive archive`. Copy back to the repo root (they are git-ignored on `main`) when you need them |
| `drafts/`, `incoming/` | Were empty. `incoming/` is still the drop folder for `tools/add_sheets.py` |

Rebuild everything: `python3 tools/build.py && python3 tools/check.py` (and `python3 tools/index_library.py` for `INDEX.csv` if you have the local folders).
