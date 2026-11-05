# Places: how the gazetteer was made

Written 2026-10-26. The gazetteer is the `place` rows of `data/assam_history.csv` (91 places). Scenes and events link to them by id in the `places` column.

## Columns on a place row
`name` (the name this project uses), `name_assamese`, `group` (kind: river, capital, battle site...), `also_called` (historic and alternative names, `; `-separated,
searched by the site), `present_name` (what it is called today), `location` (district, state, country), `summary`, `notes` (where the identification is uncertain),
`confidence` (how sure the present-day identification is), `sources`.

## Method
1. Place names were extracted from the text of all 351 scenes and 24 events.
2. Present-day identifications were checked in this session against web summaries (Wikipedia articles on Kamarupa, the Pala dynasty, Kamata, the Muslim invasions
   of Assam, Sukaphaa, the Battle of Alaboi, the Battle of Itakhuli, Sivasagar, Charaideo district, the Umachal inscription and Kamarupa inscriptions).
   Places with a source URL were read there; the rest are standard identifications that were **not** individually checked, and say so in `notes`.
3. Each scene and event was linked to every place its title or summary names (whole-word match on the name or a historic name). Notes were not used for linking.
   A link means "the place is named in the scene", not "the picture is set there".
4. Coordinates (`lat`, `lon`) come only from the AHOM map catalogue (`data/map-sites.json`, 76 points, added 2026-10-26). They are approximate reference points, not surveyed locations, and were not independently checked. 36 places were added from that catalogue with a short description and present-day location from standard references; their notes say where that is approximate.

See also `river-boundaries.md` (the 20 `realm` rows: kingdom extents bounded by rivers, by era, with disputes).

## Identifications to verify first
Low confidence (18):
- **Safrai** (`safrai`): not identified | Upper Assam (exact reach not established). Present-day course not established in the sources read.
- **Pushpabhadra** (`pushpabhadra`): not identified | Brahmaputra valley, Assam (exact river not established). Present-day river not established here.
- **Durjaya** (`durjaya`): North Guwahati or Tezpur (unsettled) | Kamrup or Sonitpur district, Assam. The sources read disagree: one article says North Guwahati; the project's own note on Ratnapala says Hadapyaka (Tezpur) was renamed Durjaya.
- **Khamjang** (`khamjang`): not identified | Patkai foothills, near the border (exact place not established). Present-day place not established in the sources read.
- **Nongnyang** (`nongnyang`): not identified | Patkai foothills, Upper Assam (exact place not established). Present-day place not established in the sources read.
- **Habung** (`habung`): Dhakuakhana / Dhemaji area (sources differ) | North bank of the Brahmaputra, Lakhimpur or Dhemaji district, Assam. The sources read give Dhakuakhana in one place and Dhemaji in another.
- **Tipam** (`tipam`): Tipam area | Tinsukia and Dibrugarh districts, Assam (approximate). Exact setting approximate.
- **Simaluguri** (`simaluguri`): Simaluguri | Sivasagar district, Assam. Sukaphaa's site is placed 'downstream of' present Simaluguri; not re-checked.
- **Mungklang** (`mungklang`): Abhoipur (reported) | Upper Assam (district not confirmed). Sources equate it with Abhoipur; not re-checked.
- **Charagua** (`charagua`): not identified | On the Dihing river, Upper Assam (exact place not established). Present-day place not established in the sources read.
- **Mahgarh** (`mahgarh`): Mahgarh | Near Jorhat, Assam. Location given in the project's scene text.
- **Bengmara** (`bengmara`): Tinsukia area | Tinsukia district, Assam. Identification with the Tinsukia area is approximate.
- **Alaboi** (`alaboi`): not identified | Near Dalbari, Assam (exact present place not established). The sources read give only 'Alaboi plains' and 'Alaboi hills near Dalbari'.
- **Kajali** (`kajali`): Kajalimukh area | Brahmaputra-Kolong confluence, Nagaon/Morigaon, Assam (approximate). Exact site approximate.
- **Samdhara** (`samdhara`): not identified | Lower Assam (exact place not established). Present-day place not established in the sources read.
- **Duimunisila** (`duimunisila`): not identified | Brahmaputra, Assam (exact place not established). Present-day place not established in the sources read.
- **Ghilajharighat** (`ghilajharighat`): not identified | Upper Assam (exact place not established). Present-day place not established in the sources read.
- **Langamaguri** (`langamaguri`): not identified | North of Guwahati, Assam (exact place not established). 

Medium confidence (22): Kamata, Namdang, Pragjyotishpura, North Guwahati, Kamarupanagara, Karnasuvarna, Davaka, Barganga, Barpanara, Mong Mao, Mungdunshunkham, Mungkang, Namrup, Ligirigaon, Garhgaon, Hoolungapara, Itakhuli, Kamatapur, Gachtal, Devkot, Aphsad, Kamauli.

## Known conflicts
- **Durjaya**: one source says North Guwahati, the project's note on Ratnapala says Hadapyaka (Tezpur) was renamed Durjaya.
- **Itakhuli**: scenes date its recapture to 1667; other sources give August 1682.
- **Habung**: Dhakuakhana in one source, Dhemaji in another.
- **Rangpur**: in Ahom scenes it means Sivasagar; in Kamata texts it can mean the city in Bangladesh (`rangpur-bangladesh`, linked by hand only).
- **Mong Mao**: Ruili (Yunnan) in most accounts; some place the Tai homeland in the Hukawng valley.

## Not covered yet
Places that appear only in person notes (the Pala grant villages Bargaon, Subhankarapataka, Khonamukha), many small Ahom frontier sites, and places named in the
27 planned Kamata scenes beyond those already in the gazetteer (Bausi, Karnapur, Khuntaghat). See `research/western-assam-1100-1515/`.
