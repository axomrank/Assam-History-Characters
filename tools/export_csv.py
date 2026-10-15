#!/usr/bin/env python3
"""Export the researched characters to a CSV you can open in a spreadsheet.

Writes data/Assam_Characters_350-1826.csv (Kamarupa CSV rulers + researched entries up to 1826).
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "data/characters.json").read_text(encoding="utf-8"))
eras = {e["id"]: e["name"] for e in d["eras"]}
av = json.loads((ROOT / "data/availability.json").read_text(encoding="utf-8"))
LEVEL = {k: v for k, v in av["chars"].items()}
rows = [c for c in d["characters"] if c.get("status") in ("csv", "researched") or c["id"] == "xuanzang"]
rows.sort(key=lambda c: (c["sort_year"], c["name"]))
cols = ["id", "name", "name_assamese", "also_known_as", "era", "group", "start_year", "end_year", "birth", "death", "dates_label",
        "ahom_reign_no", "tai_name", "hindu_name", "also_called", "relation", "how_reign_ended", "koch_branch", "koch_no",
        "role", "summary", "events_and_notes", "consort_or_marital", "confidence", "status", "image_level", "full_sheets", "portraits", "scenes_main", "scenes_appear", "sources"]
out = ROOT / "data/Assam_Characters_350-1826.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(cols)
    for c in rows:
        w.writerow([c["id"], c["name"], c.get("name_as", ""), c.get("alt_names", ""), eras[c["era"]], c.get("group") or c.get("dynasty", ""),
                    c.get("reign_start", ""), c.get("reign_end", ""), c.get("birth") or "", c.get("death") or "", c["label"], "; ".join(str(n) for n in c.get("ahom_no", [])), c.get("tai_name", ""), c.get("hindu_name", ""), c.get("nicknames", ""), c.get("relation", ""), c.get("fate", ""), c.get("koch_branch", ""), c.get("koch_no", ""), c["role"],
                    c["summary"], c.get("notes", ""), c.get("consort") or c.get("marital", ""), c.get("confidence", "from your CSV"),
                    c.get("status"), av["levels"][LEVEL[c["id"]][0]], *LEVEL[c["id"]][1:], " | ".join(c.get("sources", [])) or c.get("source", "")])
print(f"{len(rows)} rows -> {out.relative_to(ROOT)}")

# focused lists
GAPS = {5: "Interregnum 1364-1369", 6: "Interregnum 1376-1380", 7: "Interregnum 1389-1397", 40: "No Ahom king 1822-1833 (Burmese, then East India Company)"}
REIGN = {37: "1811-1818", 38: "1818-1819", 39: "1819-1821", 41: "1833-1838"}
ahom = sorted(((n, c) for c in d["characters"] for n in c.get("ahom_no", [])), key=lambda x: x[0])
with open(ROOT / "data/Ahom_kings_41_reigns.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["reign_no", "tai_name", "hindu_name", "name_used_here", "also_called", "reign", "relation_to_predecessor", "how_reign_ended", "note", "id"])
    for n, c in ahom:
        w.writerow([n, c.get("tai_name", ""), c.get("hindu_name", ""), c["name"], c.get("nicknames", ""), REIGN.get(n, c["label"].replace(" CE", "")), c.get("relation", ""), c.get("fate", ""), GAPS.get(n, ""), c["id"]])
BRANCHES = ["Koch kingdom (undivided)", "Koch Bihar kings", "Koch Hajo kings", "Darrang kings", "Bijni kings", "Beltola kings", "Khaspur kings"]
koch = sorted((c for c in d["characters"] if c.get("koch_branch") in BRANCHES), key=lambda c: (BRANCHES.index(c["koch_branch"]), c.get("koch_no", 0), c["sort_year"]))
with open(ROOT / "data/Koch_kings.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["branch", "no_in_branch", "name", "reign", "relation", "role", "summary", "notes", "confidence", "sources", "id"])
    for c in koch:
        w.writerow([c["koch_branch"], c.get("koch_no", ""), c["name"], c["label"], c.get("relation", ""), c["role"], c["summary"], c.get("notes", ""), c.get("confidence", ""), " | ".join(c.get("sources", [])), c["id"]])
print(f"{len(ahom)} Ahom reigns, {len(koch)} Koch rows")
