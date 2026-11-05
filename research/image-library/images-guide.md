# images/ — local image library

Everything here is **local only** (git-ignored): the rights of the real photographs and downloaded references are not cleared for the public repo. Only images referenced by `data/assam_history.csv` are published, via `tools/add_sheets.py`.

| Folder | What | Naming |
|---|---|---|
| `scenes/<era>/` | Generated scene paintings (PNG masters) | `c15-`, `c18-`, `1950s-`, `1990s-`, `now-`, and `life-<theme>-` for `scenes/18th-century/daily-life/` |
| `elements/<type>/` | Transparent prop and object sheets: textiles, jewellery, household, instruments, plants, manuscripts, tools-and-craft, emblems, characters | plain object name |
| `photos/<site>/` | 825 real reference photographs (Rang Ghar, Kareng Ghar, Talatal Ghar, Gola Ghar, temples, maidams, tanks, cannons …) | `<site>-NNN.jpg` |
| `references/<topic>/` | Input references used to generate images (user-supplied, museum, web) plus two source PDFs (`references/documents/`) | original names, kebab-case |

- `photos/manifest.csv` — one row per photo: new file name, title, author, licence, source page, original URL, monument, view type, period note. Always read the licence column before reuse; `suitable_as_direct_15th_century_template` is `False` for almost all (surviving masonry is mostly 18th century).
- Prompts and notes for these images are in `../research/image-library/prompts/`. Project-wide file index: `../INDEX.csv`.
- Hindu temple photos stay apart from Ahom royal/civic and Tai-Ahom funerary photos (the original library convention).
- `photos/unidentified-kareng-or-talatal/` — 23 photos whose building is uncertain; check before use.
- Generated scenes are interpretations, not evidence.
