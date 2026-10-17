#!/usr/bin/env python3
"""Build data/site.js (what the website loads) and data/assam_history.json (the same data nested as
periods > dynasties > characters > events and scenes) from the one master file, data/assam_history.csv.

Each CSV row is one record, told apart by the `type` column:
  period  a period of Assam's history (id, name, dates, summary, group_order = the order of groups on the page)
  person  a person (period and group place them; ahom_king_no / koch_no place them in the king lists).
          character_sheets lists their images as "path | caption"; the kind (portrait, pose, turnaround...)
          is the start of the file name, and the size is read from the file.
  event   a dated event on the timeline page (people = ids of the people involved; scene_image optional)
  scene   an illustrated scene (scene_image; people = everyone in it, main_people = who it is about)
Lists inside a cell are separated by "; ". Every image's thumbnail is the same file name in a thumb/ folder beside it.

Image availability per person is worked out from files that exist on disk:
  3 sheet     a real character sheet (turnaround, face, costume, props, palette)
  2 portrait  a portrait or pose, but no sheet
  1 scenes    appears in scenes only
  0 none      nothing yet
Scenes are written in date order (see scene_order). index.html gets ?v= stamps so browsers reload new data.
Identical scene files count once. Problems (unknown ids, missing files) are printed and the build fails.
Run: python3 tools/build.py
"""
import csv, datetime, hashlib, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data/assam_history.csv"
COLS = ["type", "id", "name", "name_assamese", "period", "group", "date_label", "start_year", "end_year", "sort_year",
        "role", "summary", "notes", "tai_name", "hindu_name", "also_called", "relation", "fate", "consort", "marital_status",
        "ahom_king_no", "koch_no", "koch_branch", "confidence", "status", "approx_dates", "people", "main_people",
        "collection", "character_sheets", "scene_image", "group_order", "sources"]
FULL_KINDS = {"sheet", "turnaround", "face", "costume", "props", "palette"}


def read_rows():
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_rows(rows):
    with open(CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)


def lst(v):
    return [x.strip() for x in (v or "").split(";") if x.strip()]


def thumb_of(file):
    d, n = file.rsplit("/", 1)
    return f"{d}/thumb/{n}"


def sheet_list(cell):
    """'path | caption; path | caption' -> [(path, caption)]"""
    return [(x.split("|", 1)[0].strip(), x.split("|", 1)[1].strip() if "|" in x else "") for x in lst(cell)]


def kind_of(file):
    return file.rsplit("/", 1)[-1].rsplit(".", 1)[0].rstrip("0123456789").rstrip("-_") or "other"


def num(v):
    v = (v or "").strip()
    try: f = float(v)
    except ValueError: return None
    return int(f) if f.is_integer() else f


def scene_year(r):
    """sort_year, else the first year written in the date label ('c. 1532', '1815–1816'), else None"""
    y = num(r["sort_year"])
    if y is None:
        m = re.search(r"\b(\d{3,4})\b", r["date_label"] or "")
        y = int(m.group(1)) if m else None
    return y


def scene_order(scenes):
    """Scenes in date order: the dated collections (eras, by the years in their group name) first, then the
    undated gallery. An undated scene takes the year of the scene before it, so it stays where it was put."""
    def era_start(g):
        m = re.search(r"\((\d{3,4})", g or "")
        return int(m.group(1)) if m else None
    keyed, last = [], {}
    for n, r in enumerate(scenes):
        start, y = era_start(r["group"]), scene_year(r)
        if y is None: y = last.get(r["group"])
        last[r["group"]] = y
        keyed.append(((start is None, start or 0, y is None, y or 0, n), r))
    return [r for _, r in sorted(keyed, key=lambda k: k[0])]


def stamp_index():
    """Add ?v=<content hash> to the data, script and style links in index.html so browsers fetch new versions."""
    page = ROOT / "index.html"
    html = page.read_text(encoding="utf-8")
    for f in ("data/site.js", "assets/app.js", "assets/app.css"):
        v = hashlib.sha256((ROOT / f).read_bytes()).hexdigest()[:10]
        html = re.sub(rf'(["\']){re.escape(f)}(\?v=[0-9a-f]*)?(["\'])', rf"\g<1>{f}?v={v}\g<3>", html)
    page.write_text(html, encoding="utf-8")


def main():
    rows = read_rows()
    problems = []
    by_type = defaultdict(list)
    for r in rows:
        if r["type"] not in ("period", "person", "event", "scene"): problems.append(f"unknown type {r['type']!r} on {r['id']}")
        by_type[r["type"]].append(r)
    for t, rs in by_type.items():
        dup = [i for i, n in Counter(r["id"] for r in rs).items() if n > 1]
        if dup: problems.append(f"duplicate {t} ids: {', '.join(dup)}")
    by_type["scene"] = scene_order(by_type["scene"])
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
        img = r["scene_image"]
        if not (exists(img) and exists(thumb_of(img))):
            problems.append(f"missing file: {img}"); ok = False
        else:
            h = hashlib.sha256((ROOT / img).read_bytes()).hexdigest(); ok = h not in seen; seen.add(h)
        scenes.append({"id": r["id"], "event": r["name"], "date_label": r["date_label"], "file": img, "thumbnail": thumb_of(img),
                       "filename": img.rsplit("/", 1)[-1], "collection": r["collection"], "description": r["summary"], "chars": chars, "main": main})
        if ok:
            for cid in chars: (main_of if cid in main else appear_of)[cid].append(r["id"])

    # ---- character sheets, listed on each person's row
    sheets, have = defaultdict(list), defaultdict(Counter)
    for r in by_type["person"]:
        for f, cap in sheet_list(r["character_sheets"]):
            if not (exists(f) and exists(thumb_of(f))): problems.append(f"{r['id']}: missing file {f}"); continue
            kind = kind_of(f); have[r["id"]]["full" if kind in FULL_KINDS else "port"] += 1
            w, h = Image.open(ROOT / f).size
            sheets[r["id"]].append({"file": f, "thumb": thumb_of(f), "kind": kind, "caption": cap, "width": w, "height": h,
                                    "added": datetime.date.fromtimestamp((ROOT / f).stat().st_mtime).isoformat()})

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
        if r["scene_image"] and not (exists(r["scene_image"]) and exists(thumb_of(r["scene_image"]))): problems.append(f"event {r['id']}: missing file {r['scene_image']}")
        events.append({"year": num(r["start_year"]), "end": num(r["end_year"]), "title": r["name"], "body": r["summary"], "ids": lst(r["people"]), "src": src(r["sources"]),
                       **({"image": r["scene_image"], "thumb": thumb_of(r["scene_image"])} if r["scene_image"] else {})})

    eras = [{"id": r["id"], "name": r["name"], "name_as": r["name_assamese"], "start": num(r["start_year"]), "end": num(r["end_year"]),
             "label": r["date_label"], **({"blurb": r["summary"]} if r["summary"] else {}), **({"groups": lst(r["group_order"])} if r["group_order"] else {})}
            for r in by_type["period"]]

    site = {"eras": eras, "characters": chars, "scenes": scenes, "events": events, "src": list(src_index)}
    (ROOT / "data/site.js").write_text("window.SITE=" + json.dumps(site, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

    write_tree(by_type, sheets, avail={c["id"]: c["av"][0] for c in chars})
    stamp_index()

    names = ["none", "scenes", "portrait", "sheet"]
    print(f"site.js: {len(eras)} periods, {len(chars)} people, {sum(map(len, sheets.values()))} character sheets, {len(events)} events, {len(scenes)} scenes")
    print("availability:", ", ".join(f"{names[k]} {levels[k]}" for k in (3, 2, 1, 0)))
    for p in problems: print("ERROR", p)
    sys.exit(1 if problems else 0)


def write_tree(by_type, sheets, avail):
    """data/assam_history.json: the same data nested as periods > dynasties > characters > events, scenes.
    A character holds its own images (character_sheets); a scene or event holds its scene_image.
    A scene appears under every person in it (main = true for the people it is about); scenes linking nobody are
    listed once at the end. Generated from the CSV; edit the CSV, not this file."""
    level = ["none", "scenes", "portrait", "sheet"]
    clean = lambda d: {k: v for k, v in d.items() if not (v is None or v == "" or v == [])}
    events_of, scenes_of = defaultdict(list), defaultdict(list)
    for r in by_type["event"]:
        e = clean({"id": r["id"], "title": r["name"], "date_label": r["date_label"], "start_year": num(r["start_year"]), "end_year": num(r["end_year"]),
                   "summary": r["summary"], "people": lst(r["people"]), "sources": lst(r["sources"]),
                   "scene_image": r["scene_image"], "scene_thumbnail": thumb_of(r["scene_image"]) if r["scene_image"] else ""})
        for i in lst(r["people"]): events_of[i].append(e)
    unlinked = []
    for r in by_type["scene"]:
        base = {"id": r["id"], "title": r["name"], "date_label": r["date_label"], "sort_year": num(r["sort_year"]), "era": r["group"],
                "collection": r["collection"], "summary": r["summary"], "people": lst(r["people"]),
                "scene_image": r["scene_image"], "scene_thumbnail": thumb_of(r["scene_image"])}
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
                    "sheet_status": level[avail[r["id"]]], "sources": lst(r["sources"]),
                    "character_sheets": [clean({"kind": x["kind"], "caption": x["caption"], "image": x["file"], "thumbnail": x["thumb"],
                                                "width": x["width"], "height": x["height"]}) for x in sheets[r["id"]]],
                    "events": sorted(events_of[r["id"]], key=by_year), "scenes": sorted(scenes_of[r["id"]], key=by_year)}) for r in members]}))
        periods.append(clean({"id": p["id"], "name": p["name"], "name_assamese": p["name_assamese"], "date_label": p["date_label"],
                              "start_year": num(p["start_year"]), "end_year": num(p["end_year"]), "summary": p["summary"], "dynasties": dynasties}))
    tree = {"title": "Assam history: periods, dynasties, characters, events and scenes",
            "note": "Generated by tools/build.py from data/assam_history.csv. Edit the CSV, then rebuild.",
            "periods": periods, "scenes_without_characters": sorted(unlinked, key=by_year)}
    (ROOT / "data/assam_history.json").write_text(json.dumps(tree, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
