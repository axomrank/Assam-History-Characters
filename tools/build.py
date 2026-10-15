#!/usr/bin/env python3
"""Build data/site.js (what the website loads) and data/assam_history.json (the same data nested as
periods > dynasties > characters > events and scenes) from the one master file, data/assam_history.csv.

Each CSV row is one record, told apart by the `type` column:
  period  a period of Assam's history (id, name, dates, summary, group_order = the order of groups on the page)
  person  a person (period and group place them; ahom_king_no / koch_no place them in the king lists)
  image   a character sheet or portrait (person = whose it is, kind, file, thumbnail, width, height, added)
  event   a dated event on the timeline page (people = ids of the people involved)
  scene   an illustrated scene (people = everyone in it, main_people = who it is about)
Lists inside a cell are separated by "; ".

Image availability per person is worked out from files that exist on disk:
  3 sheet     a real character sheet (turnaround, face, costume, props, palette)
  2 portrait  a portrait or pose, but no sheet
  1 scenes    appears in scenes only
  0 none      nothing yet
Identical scene files count once. Problems (unknown ids, missing files) are printed and the build fails.
Run: python3 tools/build.py
"""
import csv, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data/assam_history.csv"
COLS = ["type", "id", "name", "name_assamese", "period", "group", "date_label", "start_year", "end_year", "sort_year",
        "role", "summary", "notes", "tai_name", "hindu_name", "also_called", "relation", "fate", "consort", "marital_status",
        "ahom_king_no", "koch_no", "koch_branch", "confidence", "status", "approx_dates", "people", "main_people", "person",
        "collection", "kind", "file", "thumbnail", "width", "height", "added", "group_order", "sources"]
FULL_KINDS = {"sheet", "turnaround", "face", "costume", "props", "palette"}


def read_rows():
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_rows(rows):
    with open(CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)


def lst(v):
    return [x.strip() for x in (v or "").split(";") if x.strip()]


def num(v):
    v = (v or "").strip()
    try: f = float(v)
    except ValueError: return None
    return int(f) if f.is_integer() else f


def main():
    rows = read_rows()
    problems = []
    by_type = defaultdict(list)
    for r in rows:
        if r["type"] not in ("period", "person", "image", "event", "scene"): problems.append(f"unknown type {r['type']!r} on {r['id']}")
        by_type[r["type"]].append(r)
    for t, rs in by_type.items():
        dup = [i for i, n in Counter(r["id"] for r in rs).items() if n > 1]
        if dup: problems.append(f"duplicate {t} ids: {', '.join(dup)}")
    era_ids = [r["id"] for r in by_type["period"]]
    ids = {r["id"] for r in by_type["person"]}
    exists = lambda p: (ROOT / p).is_file()

    src_index = {}
    def src(cell):
        return [src_index.setdefault(u, len(src_index)) for u in lst(cell)]

    # ---- scenes: check files, count identical files once
    scenes, seen = [], set()
    main_of, appear_of = defaultdict(list), defaultdict(list)
    for r in by_type["scene"]:
        chars, main = lst(r["people"]), lst(r["main_people"])
        for i in chars + main:
            if i not in ids: problems.append(f"scene {r['id']}: unknown person {i}")
        if not (exists(r["file"]) and exists(r["thumbnail"])):
            problems.append(f"missing file: {r['file']}"); ok = False
        else:
            h = hashlib.sha256((ROOT / r["file"]).read_bytes()).hexdigest(); ok = h not in seen; seen.add(h)
        scenes.append({"id": r["id"], "event": r["name"], "date_label": r["date_label"], "file": r["file"], "thumbnail": r["thumbnail"],
                       "filename": r["file"].rsplit("/", 1)[-1], "collection": r["collection"], "description": r["summary"], "chars": chars, "main": main})
        if ok:
            for cid in chars: (main_of if cid in main else appear_of)[cid].append(r["id"])

    # ---- images made for a person
    sheets, have = defaultdict(list), defaultdict(Counter)
    for r in by_type["image"]:
        if r["person"] not in ids: problems.append(f"image {r['id']}: unknown person {r['person']}"); continue
        if not (exists(r["file"]) and exists(r["thumbnail"])): problems.append(f"missing file: {r['file']}"); continue
        have[r["person"]]["full" if r["kind"] in FULL_KINDS else "port"] += 1
        sheets[r["person"]].append({"file": r["file"], "thumb": r["thumbnail"], "kind": r["kind"], "caption": r["name"],
                                    "width": num(r["width"]), "height": num(r["height"]), "added": r["added"]})

    # ---- people
    chars, levels = [], Counter()
    for r in by_type["person"]:
        if r["period"] not in era_ids: problems.append(f"{r['id']}: unknown period {r['period']}")
        i = r["id"]; full, port, m, a = have[i]["full"], have[i]["port"], len(main_of[i]), len(appear_of[i])
        av = [3 if full else 2 if port else 1 if m or a else 0, full, port, m, a]; levels[av[0]] += 1
        c = {"id": i, "name": r["name"], "name_as": r["name_assamese"], "era": r["period"], "sort_year": num(r["sort_year"]), "label": r["date_label"],
             "role": r["role"], "summary": r["summary"], "status": r["status"], "group": r["group"], "notes": r["notes"],
             "reign_start": num(r["start_year"]), "reign_end": num(r["end_year"]), "confidence": r["confidence"], "tai_name": r["tai_name"],
             "hindu_name": r["hindu_name"], "nicknames": r["also_called"], "relation": r["relation"], "fate": r["fate"], "consort": r["consort"],
             "marital": r["marital_status"], "ahom_no": [int(x) for x in lst(r["ahom_king_no"])], "koch_no": num(r["koch_no"]),
             "koch_branch": r["koch_branch"], "approx": r["approx_dates"] == "yes", "src": src(r["sources"]), "av": av, "sheets": sheets[i]}
        chars.append({k: v for k, v in c.items() if k in ("id", "name", "era", "sort_year", "label", "role", "summary", "status", "av") or not (v is None or v is False or v == "" or v == [])})

    events = []
    for r in by_type["event"]:
        for i in lst(r["people"]):
            if i not in ids: problems.append(f"event {r['id']}: unknown person {i}")
        events.append({"year": num(r["start_year"]), "end": num(r["end_year"]), "title": r["name"], "body": r["summary"], "ids": lst(r["people"]), "src": src(r["sources"])})

    eras = [{"id": r["id"], "name": r["name"], "name_as": r["name_assamese"], "start": num(r["start_year"]), "end": num(r["end_year"]),
             "label": r["date_label"], **({"blurb": r["summary"]} if r["summary"] else {}), **({"groups": lst(r["group_order"])} if r["group_order"] else {})}
            for r in by_type["period"]]

    site = {"eras": eras, "characters": chars, "scenes": scenes, "events": events, "src": list(src_index)}
    (ROOT / "data/site.js").write_text("window.SITE=" + json.dumps(site, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

    write_tree(by_type, sheets, avail={c["id"]: c["av"][0] for c in chars})

    names = ["none", "scenes", "portrait", "sheet"]
    print(f"site.js: {len(eras)} periods, {len(chars)} people, {sum(map(len, sheets.values()))} images, {len(events)} events, {len(scenes)} scenes")
    print("availability:", ", ".join(f"{names[k]} {levels[k]}" for k in (3, 2, 1, 0)))
    for p in problems: print("ERROR", p)
    sys.exit(1 if problems else 0)


def write_tree(by_type, sheets, avail):
    """data/assam_history.json: the same data nested as periods > dynasties > characters > images, events, scenes.
    A scene appears under every person in it (main = true for the people it is about); scenes linking nobody are
    listed once at the end. Generated from the CSV; edit the CSV, not this file."""
    level = ["none", "scenes", "portrait", "sheet"]
    clean = lambda d: {k: v for k, v in d.items() if not (v is None or v == "" or v == [])}
    events_of, scenes_of = defaultdict(list), defaultdict(list)
    for r in by_type["event"]:
        e = clean({"id": r["id"], "title": r["name"], "date_label": r["date_label"], "start_year": num(r["start_year"]), "end_year": num(r["end_year"]),
                   "summary": r["summary"], "people": lst(r["people"]), "sources": lst(r["sources"])})
        for i in lst(r["people"]): events_of[i].append(e)
    unlinked = []
    for r in by_type["scene"]:
        base = {"id": r["id"], "title": r["name"], "date_label": r["date_label"], "sort_year": num(r["sort_year"]), "era": r["group"],
                "collection": r["collection"], "summary": r["summary"], "people": lst(r["people"]), "file": r["file"], "thumbnail": r["thumbnail"]}
        if not lst(r["people"]): unlinked.append(clean(base))
        for i in lst(r["people"]): scenes_of[i].append(clean({**base, "main": i in lst(r["main_people"])}))
    by_year = lambda x: (x.get("sort_year", x.get("start_year")) is None, x.get("sort_year", x.get("start_year")) or 0)
    periods = []
    for p in by_type["period"]:
        people = sorted((r for r in by_type["person"] if r["period"] == p["id"]), key=lambda r: num(r["sort_year"]) or 0)
        order = lst(p["group_order"]); groups = order + [g for g in dict.fromkeys(r["group"] for r in people) if g not in order]
        dynasties = []
        for g in groups:
            members = [r for r in people if r["group"] == g]
            if not members: continue
            years = [y for r in members for y in (num(r["start_year"]), num(r["end_year"])) if y is not None]
            dynasties.append(clean({"name": g or p["name"], "start_year": min(years) if years else None, "end_year": max(years) if years else None,
                "characters": [clean({
                    "id": r["id"], "name": r["name"], "name_assamese": r["name_assamese"], "date_label": r["date_label"],
                    "start_year": num(r["start_year"]), "end_year": num(r["end_year"]), "sort_year": num(r["sort_year"]), "role": r["role"],
                    "summary": r["summary"], "notes": r["notes"], "tai_name": r["tai_name"], "hindu_name": r["hindu_name"], "also_called": r["also_called"],
                    "relation": r["relation"], "fate": r["fate"], "consort": r["consort"], "marital_status": r["marital_status"],
                    "ahom_king_no": [int(x) for x in lst(r["ahom_king_no"])], "koch_no": num(r["koch_no"]), "koch_branch": r["koch_branch"],
                    "confidence": r["confidence"], "status": r["status"], "approx_dates": r["approx_dates"] == "yes" or None,
                    "image_level": level[avail[r["id"]]], "sources": lst(r["sources"]),
                    "images": [clean({"kind": x["kind"], "caption": x["caption"], "file": x["file"], "thumbnail": x["thumb"], "width": x["width"],
                                      "height": x["height"], "added": x["added"]}) for x in sheets[r["id"]]],
                    "events": sorted(events_of[r["id"]], key=by_year), "scenes": sorted(scenes_of[r["id"]], key=by_year)}) for r in members]}))
        periods.append(clean({"id": p["id"], "name": p["name"], "name_assamese": p["name_assamese"], "date_label": p["date_label"],
                              "start_year": num(p["start_year"]), "end_year": num(p["end_year"]), "summary": p["summary"], "dynasties": dynasties}))
    tree = {"title": "Assam history: periods, dynasties, characters, events and scenes",
            "note": "Generated by tools/build.py from data/assam_history.csv. Edit the CSV, then rebuild.",
            "periods": periods, "scenes_without_characters": sorted(unlinked, key=by_year)}
    (ROOT / "data/assam_history.json").write_text(json.dumps(tree, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
