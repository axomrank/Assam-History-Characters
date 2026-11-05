# Chutia character sheets: research and design briefs

Completed 28 October 2026: all eight sheets below now exist and are linked in the catalogue. Final prompts, revisions, master paths and published paths are recorded in [eight-generation-final-2026-10-28.json](chutia-sheets/eight-generation-final-2026-10-28.json). Each was generated individually with built-in imagegen and visually inspected.

> Superseded costume direction: use [the eight-character design plan](chutia-sheets/eight-character-design-plan-2026-10-28.md) and its structured designs/prompts. The older briefs below are retained as a research record; their long tunics, dark headwraps, shoulder cloths, quilted vests, footwear and automatic Vaishnava progression are not current generation instructions.

2026-10-28. For the eight Chutia people with no sheet yet. Three sheets already exist and set the look:
`media/characters/nandi-chutia/`, `satyanarayana-chutia/`, `dhirnarayan/` (briefs in `research/ahom/people/<id>/`).
Read `research/ahom/agent-guidance.md` before generating.

## Shared direction (creative, not evidence)
- Layout: the project's eight-view sheet (front, left profile, back, three-quarter; face close-up, right profile, low angle, high
  angle), neutral grey background, straight frontal face, realistic photographic rendering.
- Court dress continuity with Dhirnarayan's sheet: knee-length woven tunic in madder red or indigo with narrow cream geometric
  borders, wrapped lower garment, sash, dark cloth headwrap with a low bronze brow band, flat dark shoes. Kings: finer weave, one or
  two gold ornaments. Ministers and princes: plainer.
- Dates run 1392 → 1524: show **gradual** Vaishnava court influence (a small tilak, a Vaishnava bead necklace) on later kings, as a
  styling choice; it is not a claim about any king's faith.
- Distinct faces, ages and builds for every person. No crowns copied from Ahom or Mughal art, no 18th-century Ahom palace motifs.
- Modern Sutiya and Deori dress may be used only as colour and weave reference, labelled as such in the notes.
- What the sources say about each person is all there is: **no portrait of any Chutia king survives.**

## The briefs

### Lakshminarayana (`lakshminarayana-chutia`), early 15th century
Research: issued the Ghilamara grant (1401); a brick with his name at Bhismaknagar suggests that fortified brick city was his capital
(CHUTIA-03, 04). Also called Dharmanarayana in one reading.
Design: man of about 45, broad face, calm authority; indigo tunic with cream borders, deep-red sash, gold ear-studs, headwrap with a
bronze band. A builder king: one hand holding a folded grant-cloth or a fired brick is acceptable on a side pose, not on the front view.

### Durlabhnarayana (`durlabhnarayana-chutia`), grant of 1428
Research: issued the Sadiya-Chepakhowa grant (1428) (CHUTIA-05). Not the Kamata king of the same name.
Design: man of about 50, long face, heavier build, grey at the temples; madder-red tunic, ochre wrapped garment, simple gold necklace.

### Mukta Dharmanarayana (`muktadharmanarayana`), 1442
Research: as a prince (son of an unnamed king) built the brick wall of the Kechaikhati shrine, recorded in its inscription of 1442
(CHUTIA-06).
Design: young man of about 25, lean, alert; lighter cream tunic with red geometric border, red sash, small headwrap without the
bronze band (a prince, not yet king).

### Pratyaksanarayana (`pratyaksanarayana`), mid-15th century
Research: known without dates; possibly the Yasanarayana named on the Dhenukhana plate. Low confidence.
Design: man of about 40, round face, short beard; indigo tunic, plain borders. Keep restrained; note the uncertain identity.

### Yasamanarayana (`yasamanarayana`), late 15th century
Research: a late-15th-century king, perhaps the same Yasanarayana. Low confidence.
Design: man of about 55, thin, stooped slightly; dark-red tunic, cream shoulder cloth, a Vaishnava bead necklace.

### Purandarnarayana (`purandarnarayana`), late 15th century
Research: listed before Dhirnarayan; no events known.
Design: man of about 45, strong jaw, clean-shaven; madder-red tunic, quilted brown vest (the military look that Dhirnarayan's sheet
develops), headwrap with bronze band.

### Kasitora (`kasitora`), minister, 1522–23
Research: a minister said to have fought and been defeated alongside Dhirnarayan.
Design: man of about 50, weathered; plain dark tunic, quilted vest, short sword, no gold. A soldier-minister, not royalty.

### Sadhaknarayan (`sadhaknarayan`), prince, 1523–24
Research: a prince after the fall; some sources say he was deported to Darrang, others that he was killed (CHUTIA-13).
Design: youth of about 18; cream tunic with faded red border, no ornaments except a thread on the wrist; dignified, not humiliated.

## When the images exist
Put each sheet in `incoming/<id>__turnaround.png` and run `python3 tools/add_sheets.py`; keep the generation prompt and notes in
`research/koch-chutia-1350-1616/chutia-sheets/<id>.md`.
