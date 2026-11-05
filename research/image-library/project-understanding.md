# Project orientation for future image work

Reviewed 26 October 2026. This is an orientation record, not new historical research or a replacement for per-subject briefs.

## Purpose and current catalogue

The static bilingual English/Assamese site is a reusable visual continuity library for Assam history artwork, video and books. It links people to character sheets and historical scenes, from ancient Kamarupa through modern Assam.

The current `data/assam_history.csv` has 7 periods, 334 people, 24 events and 351 scene rows. All 351 scene rows currently have image paths; 179 person rows have their own sheet or portrait paths. These are row counts, not a count of unique images or an assessment of historical completeness. README totals are older. The separate 27-scene western-Assam proposal is research, not automatically part of the main catalogue.

Use `INDEX.csv` to locate assets, then inspect selected files. Use the master CSV's actual ids: examples include `bhaskar-varman`, `brahma-pala`, `salastamba`, `sukaphaa`, `sankardev`. Do not construct ids from display names.

## Visual continuity

Inspected Sukaphaa, Bhaskaravarman and Brahmapala sheets, the Brahmapala election scene, the c15 royal-settlement concept, and Sankardev's domestic manuscript scene.

Character sheets normally use a neutral grey studio background, realistic skin/anatomy and textiles, two rows of four views. Upper row: front, left profile, back, three-quarter full bodies with visible feet. Lower row: frontal close-up, right profile, low angle and high angle. Preserve the same identity, age, proportions, hairstyle, headgear, garment construction and accessories in every panel. Check the actual view against the label; labels alone do not establish correct angles. Consult selected artwork and subsequent revision notes before an earlier generic brief.

Scenes use realistic people, natural light, weathered materials and legible staging. Reuse named characters' selected sheets as image references. Their presence in an existing scene or a CSV `people` link does not independently establish attendance at the depicted event. Recheck chronology and participants for each new commission.

## Group-specific direction

- Varman: preserve each selected design and distinct face. Wrapped garments, draped cloth and royal jewellery are interpretive. Bhaskaravarman's selected sheet has its own crown and red/ivory costume; earlier low-diadem proposals do not override it. No authenticated ruler likenesses or complete wardrobes are established by these notes.
- Salastambha: modern Tiwa/Rabha/Motok supplied clothing inspired the creative direction; this does not establish ancient community identity. Straight overlapping knee-length wrap/lungi, no dhoti or crotch tuck; vivid woven colours, varied shirts and restrained royal ornaments. Jivaraja and Digleswaravarman remain provisional historical identities.
- Kamarupa Pala: preserve the gold-mukut design and each selected identity. Later selected Harsha Pala, Dharma Pala and Jaya Pala sheets use revised dhotis. Sanskritic influence is a costume direction, not a claim of changing ancestry or skin tone.
- Ahom: consult the individual's selected sheet and design/revision notes. Royal, official, common-village, Kachari and Bhuyan designs have separate reference histories. Do not generalize Sukaphaa's royal costume to all people.
- Bhuyan adult men: current explicit direction is plain white dhoti plus separate white shoulder cloth, minimal ochre edging, left shoulder covered and right shoulder/arm bare, barefoot; no shirt, jacket, trousers or headwear unless revised. Preserve individual faces. Women's supplied white-clothing references are separate.
- Kachari common settlements: use their supplied house/clothing comparisons; do not import Ahom palace forms or guard uniforms.

## Architecture, references and evidence

Read `research/ahom/agent-guidance.md` before generation. Keep Hindu temples, royal/civic buildings and Tai-Ahom funerary architecture distinct. Surviving eighteenth-century masonry is not a direct fifteenth-century template. Early timber/thatch royal settlements are speculative; a common village is not an identified royal town. Royal scale and carpentry may differ substantially from ordinary housing.

Current paths supersede relocated paths in older notes:

- `images/scenes/<era>/`: generated environment concepts.
- `images/elements/<type>/`: reusable object/prop assets.
- `images/references/<topic>/`: supplied/comparative inputs.
- `images/photos/<site>/` and `images/photos/manifest.csv`: real photographs with source, licence, architecture family and period limitations.

The `images/referance/ahom/…` and `images/assam/15th-century/` paths mentioned in older guidance no longer exist. Use the current index, images guide and photo manifest instead. Historical prompt paths may also predate reorganization.

Generated artwork is interpretation, not evidence. Modern community photographs, devotional portraits and statues can guide an explicitly requested design but do not authenticate historical likeness, dress or ancestry. Existing source fields often point to summaries; verify relevant primary/authoritative evidence when making new historical claims. Do not treat a downloaded source as consulted or generated charter marks as authentic text.

`research/ahom/batches/burmese-four/realism-remake-review.md` records unactivated alternatives and participant-continuity issues. It retains the earlier Badan Chandra scene as selected. Do not activate those alternatives by filename or realism alone.

## Adding future work

Save research, prompts, provenance and uncertainty notes under `research/`, never beside image assets. Preserve selected originals and earlier versions. Preview/review new artwork before replacing selected catalogue artwork; a review footer may remain in an image already approved according to later notes.

For character import use `incoming/<person-id>/<kind>.png` or `<person-id>__<kind>.png`, then `python3 tools/add_sheets.py --dry-run` followed by import when appropriate. It writes numbered WebPs and thumbnails, retains originals in `masters/sheets/<id>/`, updates the person row and rebuilds. For scenes keep PNG masters, create published WebP plus matching thumb, and update the existing scene's `scene_image` rather than adding image-only rows.

`data/assam_history.csv` is the sole editable site-data source; `python3 tools/build.py` regenerates site data and checks references. `python3 tools/index_library.py` refreshes the file index after additions. The current index classifies files by location; a file under `media/` labelled published is not by itself proof that it is selected in the CSV.

Public site files are `index.html`, `assets/`, `data/`, `media/` and `tools/`. Masters, drafts, research and reference libraries are local; photograph licensing must be checked for the proposed reuse.
