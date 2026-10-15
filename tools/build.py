#!/usr/bin/env python3
"""Build everything the site and the spreadsheets need from the three sources of truth.

Sources:   data/characters.json (people), data/sheets.json (images made for a character), data/scenes.json (scenes)
Generated: data/site.js (slim, loaded by the site), data/availability.json + data/exports/image_availability.csv

Image availability per character is one of four levels, worked out only from files that exist on disk:
  3 sheet     a real character sheet (turnaround, face, costume, props, palette)
  2 portrait  a portrait or pose, but no sheet
  1 scenes    appears in catalogued scenes only
  0 none
Scenes are split into "main" (the person is named in the scene title) and "appears" (linked by the
catalogue's ruler/figures fields only). Identical image files are counted once.

Run after any change:  python3 tools/build.py
"""
import csv, re, sys
from collections import Counter, defaultdict
from common import ROOT, SCENES, CHAR_MEDIA, FULL_KINDS, PORTRAIT_KINDS, compact_char, load_characters, load_sheets, read, thumb_of, write

LEVELS = ["none", "scenes", "portrait", "sheet"]
NEXT = {3: "complete", 2: "make a full sheet from the portraits", 1: "build a sheet from the scene references", 0: "commission a portrait or sheet"}
GENERIC = {"singha", "narayan", "narayana", "borphukan", "burhagohain", "borgohain", "borbarua", "phukan", "konwar", "roja", "raja", "khan", "shah", "chandra",
           "prince", "princess", "queen", "general", "king", "lord", "captain", "colonel", "chronicler", "mughal", "burmese", "kachari", "jaintia", "manipur",
           "british", "architect", "subedar", "first", "rebel", "infant", "governor", "srimanta", "birangana", "mother", "moran", "borahi", "moamoria", "chaolung", "dihingia"}


def words(name):
    return [w for w in re.findall(r"[A-Za-z]+", name) if len(w) >= 4 and w.lower() not in GENERIC]


def main():
    data = load_characters()
    chars = data["characters"]
    sheets = load_sheets()
    cat = read(SCENES)
    alias = cat["metadata"].get("aliases", {})
    problems = []
    ids = {c["id"] for c in chars}
    if len(ids) != len(chars): problems.append("duplicate character ids")
    era_ids = {e["id"] for e in data["eras"]}
    for c in chars:
        if c["era"] not in era_ids: problems.append(f"{c['id']}: unknown era {c['era']}")

    # ---- names -> characters (for linking catalogue scenes)
    by_name = defaultdict(set)
    for c in chars:
        for n in {c["name"], *c.get("match", [])}: by_name[n].add(c["id"])
    key_words = {}
    for c in chars:
        variants = {c["name"], re.sub(r"\s*\(.*?\)", "", c["name"]), *re.findall(r"\((.*?)\)", c["name"]), *c.get("match", []), c.get("tai_name", ""), c.get("hindu_name", "")}
        variants |= {a for a, target in alias.items() if target in variants}
        key_words[c["id"]] = {w.lower() for v in variants for w in words(v)}

    # ---- scenes: link, split main/appears, check files, count identical files once
    scenes, seen_sha = [], {}
    main_of, appear_of = defaultdict(list), defaultdict(list)
    missing = []
    for r in cat["images"]:
        ok = (ROOT / r["file"]).exists() and (ROOT / r["thumbnail"]).exists()
        if not ok: missing.append(r["file"])
        names = {r["ruler"], *r["figures"]}
        names |= {alias[n] for n in list(names) if n in alias}
        linked = sorted({cid for n in names for cid in by_name.get(n, ())})
        title = {w.lower() for w in re.findall(r"[A-Za-z]+", r["event"])}
        main = [cid for cid in linked if key_words[cid] & title]
        dup = seen_sha.get(r["sha256"])
        seen_sha.setdefault(r["sha256"], r["id"])
        scenes.append({"id": r["id"], "event": r["event"], "date_label": r["date_label"], "file": r["file"], "thumbnail": r["thumbnail"],
                       "filename": r["filename"], "collection": r["collection"], "description": r["description"], "chars": linked, "main": main})
        if ok and not dup:
            for cid in linked: (main_of if cid in main else appear_of)[cid].append(r["id"])

    # ---- sheets: check files and characters
    have = defaultdict(lambda: Counter())
    sheet_rows = defaultdict(list)
    known_files = set()
    for s in sheets:
        known_files |= {s["file"], thumb_of(s["file"])}
        if s["char"] not in ids: problems.append(f"sheets.json: unknown character {s['char']}"); continue
        if not ((ROOT / s["file"]).exists() and (ROOT / thumb_of(s["file"])).exists()):
            missing.append(s["file"]); continue
        have[s["char"]]["full" if s["kind"] in FULL_KINDS else "port"] += 1
        sheet_rows[s["char"]].append({"file": s["file"], "thumb": thumb_of(s["file"]), "kind": s["kind"], "caption": s.get("caption", ""), "width": s.get("w"), "height": s.get("h"), "added": s["added"]})
    orphans = sorted(str(p.relative_to(ROOT)) for p in (ROOT / CHAR_MEDIA).rglob("*.webp") if str(p.relative_to(ROOT)) not in known_files) if (ROOT / CHAR_MEDIA).exists() else []

    # ---- availability
    av = {}
    for c in chars:
        i = c["id"]; full, port = have[i]["full"], have[i]["port"]; m, a = len(main_of[i]), len(appear_of[i])
        av[i] = [3 if full else 2 if port else 1 if m or a else 0, full, port, m, a]

    # ---- sources table (URLs once)
    src_index = {}
    def src_ids(urls):
        return [src_index.setdefault(u, len(src_index)) for u in urls]

    # ---- slim site data
    DROP = {"match", "sources", "birth", "death"}
    out_chars = []
    for c in chars:
        o = {k: v for k, v in compact_char(c).items() if k not in DROP}
        if c.get("sources"): o["src"] = src_ids(c["sources"])
        o["av"] = av[c["id"]]
        if sheet_rows[c["id"]]: o["sheets"] = sheet_rows[c["id"]]
        out_chars.append(o)
    events = []
    ev = ROOT / "data/research/events_1100_1515.json"
    known = ids
    if ev.exists():
        for e in read("data/research/events_1100_1515.json")["events"]:
            for i in e["ids"]:
                if i not in known: problems.append(f"event {e['year']} {e['title']}: unknown character {i}")
            e = dict(e); e["src"] = src_ids(e.pop("sources", [])); events.append(e)
    site = {"eras": data["eras"], "characters": out_chars, "scenes": scenes, "events": events, "src": list(src_index)}
    (ROOT / "data/site.js").write_text("window.SITE=" + __import__("json").dumps(site, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

    # ---- availability outputs
    counts = Counter(v[0] for v in av.values())
    (ROOT / "data/availability.json").write_text(__import__("json").dumps({"schema": "ahom-availability-v1", "levels": LEVELS, "fields": ["level", "full_sheets", "portraits", "scenes_main", "scenes_appear"],
        "counts": {LEVELS[k]: counts.get(k, 0) for k in range(4)}, "chars": av}, separators=(",", ":")) + "\n", encoding="utf-8")
    eras = {e["id"]: e["name"] for e in data["eras"]}
    order = {e["id"]: n for n, e in enumerate(data["eras"])}
    with open(ROOT / "data/exports/image_availability.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "period", "group", "dates", "level", "level_name", "full_sheets", "portraits", "scenes_main", "scenes_appear", "reference_scene_ids", "next_step"])
        for c in sorted(chars, key=lambda c: (order[c["era"]], c.get("group") or c.get("dynasty") or "", c["sort_year"])):
            l, full, port, m, a = av[c["id"]]
            w.writerow([c["id"], c["name"], eras[c["era"]], c.get("group") or c.get("dynasty") or "", c["label"], l, LEVELS[l], full, port, m, a, " ".join(main_of[c["id"]][:6]),
                        NEXT[l] if l != 1 or m else "commission a portrait (appears only in the background of scenes)"])

    # ---- report
    print(f"site.js: {len(chars)} characters, {len(scenes)} scenes, {len(src_index)} source links")
    print("availability:", ", ".join(f"{LEVELS[k]} {counts.get(k, 0)}" for k in (3, 2, 1, 0)))
    unlinked = [s["id"] for s in scenes if not s["chars"]]
    print(f"scenes: {len(scenes)} total, {len(unlinked)} not tied to any character, {sum(1 for s in scenes if s['main'])} with a named main figure, {len(scenes) - len(seen_sha)} duplicate file(s)")
    if missing: problems += [f"missing file: {m}" for m in missing]
    if orphans: print(f"note: {len(orphans)} file(s) in media/characters/ are not listed in data/sheets.json, e.g. {orphans[0]}")
    for p in problems: print("ERROR", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
