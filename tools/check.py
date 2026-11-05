#!/usr/bin/env python3
"""Check data/assam_history.csv and media/ for the mistakes people make when adding things.
Run: python3 tools/check.py        (exit code 1 if any ERROR; WARN lines are advice)

ERROR: duplicate id within a type | id not kebab-case (scene ids may be ABC-01) | unknown type | unknown period/place/person id |
       image path listed but file missing | required field empty
WARN:  image file in media/ not listed in the CSV | person or scene with no sources | place without lat/lon
tools/build.py does the heavy checks while building; this one is quick and needs no Pillow.
"""
import csv, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "data/assam_history.csv", encoding="utf-8-sig")))
TYPES = {"period", "person", "event", "place", "realm", "scene"}
REQUIRED = {"period": ["name", "date_label"], "person": ["name"], "event": ["name", "start_year"],
            "place": ["name"], "realm": ["name", "group"], "scene": ["name"]}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors, warns = [], []
err = lambda r, m: errors.append(f"{r['type']}:{r['id']}  {m}")
warn = lambda r, m: warns.append(f"{r['type']}:{r['id']}  {m}")
split = lambda s: [x.strip() for x in (s or "").split(";") if x.strip()]

ids = Counter((r["type"], r["id"]) for r in rows)
for (t, i), n in ids.items():
    if n > 1: errors.append(f"{t} id '{i}' used {n} times")
by = {t: {r["id"] for r in rows if r["type"] == t} for t in TYPES}
listed = set()
for r in rows:
    t = r["type"]
    if t not in TYPES: err(r, f"unknown type '{t}'"); continue
    if not (KEBAB.match(r["id"]) or (t == "scene" and re.match(r"^[A-Z0-9]+(-[A-Z0-9]+)*$", r["id"]))):
        err(r, "id should be kebab-case (scenes may be like VARMAN-01)")
    for f in REQUIRED[t]:
        if not r[f]: err(r, f"'{f}' is empty")
    if r["period"] and t != "period" and r["period"] not in by["period"]: err(r, f"unknown period '{r['period']}'")
    for col, kind in (("places", "place"), ("people", "person"), ("main_people", "person")):
        for x in split(r[col]):
            if x not in by[kind]: err(r, f"{col}: unknown {kind} '{x}'")
    paths = [p.split("|")[0].strip() for p in split(r["character_sheets"])] + ([r["scene_image"]] if r["scene_image"] else [])
    for p in paths:
        listed.add(p)
        if not (ROOT / p).exists(): err(r, f"missing file {p}")
    if t in ("person", "scene") and not r["sources"] and r.get("status") != "planned": warn(r, "no sources")
    if t == "place" and not r["lat"]: warn(r, "no lat/lon (not on the map)")
for f in sorted((ROOT / "media").rglob("*.webp")):
    rel = f.relative_to(ROOT).as_posix()
    if "/thumb/" not in rel and rel not in listed: warn({"type": "file", "id": rel}, "not listed in the CSV")
for m in errors: print("ERROR", m)
for m in warns[:60]: print("WARN ", m)
if len(warns) > 60: print(f"WARN  ... and {len(warns) - 60} more")
print(f"{len(rows)} rows, {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
