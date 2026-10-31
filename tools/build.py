#!/usr/bin/env python3
"""Build data/site.js (what the website loads) and data/assam_history.json (the same data nested as
periods > dynasties > characters > events and scenes) from the one master file, data/assam_history.csv.

Each CSV row is one record, told apart by the `type` column:
  period  a period of Assam's history (id, name, dates, summary, group_order = the order of groups on the page)
  person  a person (period and group place them; ahom_king_no / koch_no place them in the king lists).
          character_sheets lists their images as "path | caption"; the kind (portrait, pose, turnaround...)
          is the start of the file name, and the size is read from the file.
  event   a dated event on the timeline page (people = ids of the people involved; scene_image optional)
  place   a place (name, also_called = historic and alternative names, present_name and location = what it is today and where,
          lat / lon = a map reference point (approximate, from the AHOM map catalogue; empty when none),
          group = kind of place, summary, notes, confidence = how sure the present-day identification is, sources)
  realm   a kingdom's extent in one era (group = the kingdom's place id, boundary = "West: ... | East: ..." marked by rivers and
          landmarks, places = the place ids of those rivers and landmarks, notes = disagreements between sources)
  scene   an illustrated scene (scene_image; people = everyone in it, main_people = who it is about, places = place ids).
          A researched scene not painted yet has status "planned" and no scene_image; the site shows a placeholder.
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
import csv, datetime, hashlib, html, json, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data/assam_history.csv"
COLS = ["type", "id", "name", "name_assamese", "period", "group", "date_label", "start_year", "end_year", "sort_year",
        "role", "summary", "notes", "tai_name", "hindu_name", "also_called", "relation", "fate", "consort", "marital_status",
        "ahom_king_no", "koch_no", "koch_branch", "confidence", "status", "approx_dates", "people", "main_people",
        "collection", "character_sheets", "scene_image", "group_order", "sources", "places", "present_name", "location", "lat", "lon", "boundary", "sheet_brief"]
FULL_KINDS = {"sheet", "turnaround", "face", "costume", "props", "palette"}


def read_rows():
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        return [{c: r.get(c) or "" for c in COLS} for r in csv.DictReader(f)]


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


def brief_of(cell):
    """sheet_brief: 'appearance: ... | costume: ... | props: ... | avoid: ...' -> dict (a design brief for a sheet not made yet)"""
    out = {}
    for part in (cell or "").split("|"):
        k, _, v = part.partition(":")
        if v.strip() and k.strip().lower() in ("appearance", "costume", "props", "avoid"): out[k.strip().lower()] = v.strip()
    return out


def scene_year(r):
    """sort_year, else the first year written in the date label ('c. 1532', '1815–1816'), else None"""
    y = num(r["sort_year"])
    if y is None:
        m = re.search(r"\b(\d{3,4})\b", r["date_label"] or "")
        y = int(m.group(1)) if m else None
    return y


def scene_order(scenes):
    """Scenes in strict date order across all eras and collections (ties keep era order, then file order), then the
    undated gallery. An undated scene takes the year of the scene before it in its era, so it stays where it was put."""
    def era_start(g):
        m = re.search(r"\((\d{3,4})", g or "")
        return int(m.group(1)) if m else None
    keyed, last = [], {}
    for n, r in enumerate(scenes):
        start, y = era_start(r["group"]), scene_year(r)
        if y is None: y = last.get(r["group"])
        last[r["group"]] = y
        keyed.append(((y is None and start is None, y if y is not None else (start or 0), start or 0, n), r))
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
        if r["type"] not in ("period", "person", "event", "scene", "place", "realm"): problems.append(f"unknown type {r['type']!r} on {r['id']}")
        by_type[r["type"]].append(r)
    for t, rs in by_type.items():
        dup = [i for i, n in Counter(r["id"] for r in rs).items() if n > 1]
        if dup: problems.append(f"duplicate {t} ids: {', '.join(dup)}")
    by_type["scene"] = scene_order(by_type["scene"])
    era_ids = [r["id"] for r in by_type["period"]]
    ids = {r["id"] for r in by_type["person"]}
    place_ids = {r["id"] for r in by_type["place"]}
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
        for i in lst(r["places"]):
            if i not in place_ids: problems.append(f"scene {r['id']}: unknown place {i}")
        img = r["scene_image"]
        if not img:   # a researched scene that is not painted yet: the site shows a placeholder
            if r["status"] != "planned": problems.append(f"scene {r['id']}: no scene_image (set status to planned if it is not painted yet)")
            ok = False
        elif not (exists(img) and exists(thumb_of(img))):
            problems.append(f"missing file: {img}"); ok = False
        else:
            h = hashlib.sha256((ROOT / img).read_bytes()).hexdigest(); ok = h not in seen; seen.add(h)
        scenes.append({"id": r["id"], "event": r["name"], "date_label": r["date_label"],
                       **({"file": img, "thumbnail": thumb_of(img), "filename": img.rsplit("/", 1)[-1]} if img else {"planned": 1}),
                       "collection": r["collection"], "description": r["summary"], "chars": chars, "main": main,
                       **({"places": lst(r["places"])} if r["places"] else {}),
                       **({"conf": r["confidence"]} if r["confidence"] else {}), **({"notes": r["notes"]} if r["notes"] and not img else {}),
                       **({"src": src(r["sources"])} if r["sources"] else {})})
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
             "koch_branch": r["koch_branch"], "approx": r["approx_dates"] == "yes", "src": src(r["sources"]), "av": av, "sheets": sheets[i], "brief": brief_of(r["sheet_brief"])}
        chars.append({k: v for k, v in c.items() if k in ("id", "name", "era", "sort_year", "label", "role", "summary", "status", "av") or not (v is None or v is False or v == "" or v == [])})

    events = []
    for r in by_type["event"]:
        for i in lst(r["people"]):
            if i not in ids: problems.append(f"event {r['id']}: unknown person {i}")
        if r["scene_image"] and not (exists(r["scene_image"]) and exists(thumb_of(r["scene_image"]))): problems.append(f"event {r['id']}: missing file {r['scene_image']}")
        for i in lst(r["places"]):
            if i not in place_ids: problems.append(f"event {r['id']}: unknown place {i}")
        events.append({"year": num(r["start_year"]), "end": num(r["end_year"]), "title": r["name"], "body": r["summary"], "ids": lst(r["people"]), "src": src(r["sources"]),
                       **({"places": lst(r["places"])} if r["places"] else {}),
                       **({"image": r["scene_image"], "thumb": thumb_of(r["scene_image"])} if r["scene_image"] else {})})

    eras = [{"id": r["id"], "name": r["name"], "name_as": r["name_assamese"], "start": num(r["start_year"]), "end": num(r["end_year"]),
             "label": r["date_label"], **({"blurb": r["summary"]} if r["summary"] else {}), **({"groups": lst(r["group_order"])} if r["group_order"] else {})}
            for r in by_type["period"]]

    places = [{"id": r["id"], "name": r["name"], "name_as": r["name_assamese"], "cat": r["group"], "alt": r["also_called"], "present": r["present_name"],
               "loc": r["location"], "desc": r["summary"], "note": r["notes"], "conf": r["confidence"], "src": src(r["sources"]),
               "geo": [num(r["lat"]), num(r["lon"])] if num(r["lat"]) is not None and num(r["lon"]) is not None else None} for r in by_type["place"]]
    places = [{k: v for k, v in p.items() if v not in ("", [], None)} for p in places]
    realms = []
    for r in by_type["realm"]:
        if r["group"] not in place_ids: problems.append(f"realm {r['id']}: unknown polity {r['group']}")
        for i in lst(r["places"]):
            if i not in place_ids: problems.append(f"realm {r['id']}: unknown place {i}")
        realms.append({k: v for k, v in {"id": r["id"], "name": r["name"], "polity": r["group"], "era": r["period"], "label": r["date_label"], "start": num(r["start_year"]),
                       "end": num(r["end_year"]), "desc": r["summary"], "bounds": r["boundary"], "note": r["notes"], "conf": r["confidence"], "src": src(r["sources"]),
                       "places": lst(r["places"])}.items() if v not in ("", [], None)})
    site = {"eras": eras, "characters": chars, "scenes": scenes, "events": events, "places": places, "realms": realms, "src": list(src_index)}
    (ROOT / "data/site.js").write_text("window.SITE=" + json.dumps(site, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

    write_tree(by_type, sheets, avail={c["id"]: c["av"][0] for c in chars})
    write_share_pages(chars, sheets)
    stamp_index()
    stamp_service_worker()

    names = ["none", "scenes", "portrait", "sheet"]
    print(f"site.js: {len(eras)} periods, {len(chars)} people, {sum(map(len, sheets.values()))} character sheets, {len(events)} events, {len(scenes)} scenes, {len(places)} places, {len(realms)} realms")
    print("availability:", ", ".join(f"{names[k]} {levels[k]}" for k in (3, 2, 1, 0)))
    for p in problems: print("ERROR", p)
    sys.exit(1 if problems else 0)


BASE = "https://axomrank.github.io/Assam-History-Characters/"

SHARE_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Assam history sheets">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{image}">
<meta http-equiv="refresh" content="0;url=../../#/c/{id}">
<script>location.replace("../../#/c/{id}");</script>
<style>body{{font:18px/1.6 Georgia,serif;max-width:40rem;margin:12vh auto;padding:0 20px;background:#e9e1cc;color:#241c13}}a{{color:#a3301c}}</style>
</head><body><h1>{name}</h1><p>{desc}</p><p><a href="../../#/c/{id}">Open the character page</a></p></body></html>
"""


def write_share_pages(chars, sheets):
    """One small page per person at c/<id>/index.html carrying Open Graph tags (name, summary, sheet image) for link previews and
    search engines; it sends visitors on to the app at #/c/<id>. Also writes sitemap.xml and robots.txt. The folder is rebuilt each run."""
    out = ROOT / "c"
    if out.exists(): shutil.rmtree(out)
    urls = [BASE]
    for c in chars:
        sh = sheets.get(c["id"], [])
        pick = next((s for s in sh if s["kind"] in FULL_KINDS), sh[0] if sh else None)
        image = BASE + pick["file"] if pick else BASE + "assets/og.jpg"
        desc = c.get("summary") or c.get("role", "")
        if c.get("label") and c["label"] not in desc: desc = f"{c['label']}. {desc}"
        desc = html.escape(desc if len(desc) <= 200 else desc[:197].rsplit(" ", 1)[0] + "...", quote=True)
        url = f"{BASE}c/{c['id']}/"
        d = out / c["id"]; d.mkdir(parents=True)
        (d / "index.html").write_text(SHARE_PAGE.format(title=html.escape(f"{c['name']}, Assam history sheets", quote=True), desc=desc, url=url,
                                                        image=html.escape(image, quote=True), id=c["id"], name=html.escape(c["name"])), encoding="utf-8")
        urls.append(url)
    today = datetime.date.today().isoformat()
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")


def stamp_service_worker():
    """Give sw.js a version that changes whenever the site files change, so installed copies refresh."""
    page = ROOT / "sw.js"
    if not page.exists(): return
    v = hashlib.sha256(b"".join((ROOT / f).read_bytes() for f in ("data/site.js", "assets/app.js", "assets/app.css", "index.html"))).hexdigest()[:10]
    page.write_text(re.sub(r"const VERSION = '[^']*';", f"const VERSION = '{v}';", page.read_text(encoding="utf-8")), encoding="utf-8")


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
                "scene_image": r["scene_image"], "scene_thumbnail": thumb_of(r["scene_image"]) if r["scene_image"] else "",
                "status": r["status"], "confidence": r["confidence"], "sources": lst(r["sources"]), "places": lst(r["places"])}
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
            "periods": periods, "scenes_without_characters": sorted(unlinked, key=by_year),
            "realms": [clean({"id": r["id"], "name": r["name"], "kingdom": r["group"], "period": r["period"], "date_label": r["date_label"],
                              "start_year": num(r["start_year"]), "end_year": num(r["end_year"]), "summary": r["summary"], "boundary": r["boundary"],
                              "notes": r["notes"], "confidence": r["confidence"], "places": lst(r["places"]), "sources": lst(r["sources"])}) for r in by_type["realm"]],
            "places": [clean({"id": r["id"], "name": r["name"], "name_assamese": r["name_assamese"], "kind": r["group"], "also_called": lst(r["also_called"]),
                              "present_name": r["present_name"], "location": r["location"], "summary": r["summary"], "notes": r["notes"],
                              "confidence": r["confidence"], "latitude": num(r["lat"]), "longitude": num(r["lon"]), "sources": lst(r["sources"])}) for r in by_type["place"]]}
    (ROOT / "data/assam_history.json").write_text(json.dumps(tree, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
