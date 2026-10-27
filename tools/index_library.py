#!/usr/bin/env python3
"""Rebuild INDEX.csv: one row per image or document in the project (published media and local libraries).

Columns: path, area, kind, subject, era, status, width, height, kb
  area     published (media/) or local (masters, drafts, images, research)
  kind     character-sheet, portrait, scene, thumbnail, object, photo, reference, prompt, note, source, other
  subject  person id / scene id / site / object name, taken from the path
Run:  python3 tools/index_library.py
"""
import csv, os, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = {r["id"] for r in csv.DictReader(open(ROOT / "data/assam_history.csv", encoding="utf-8-sig")) if r["type"] == "person"}
IMG = {".png", ".jpg", ".jpeg", ".webp"}
SKIP = {".git", "__pycache__", "assets", "tools"}


def classify(rel):
    p = rel.split("/")
    top = p[0]
    ext = os.path.splitext(rel)[1].lower()
    name = os.path.splitext(p[-1])[0]
    area = "published" if top == "media" else "local"
    kind = subject = era = status = ""
    if top == "media":
        status = "published"
        if p[1] == "characters":
            subject = p[2]
            kind = "thumbnail" if "thumb" in p else "character-sheet"
        else:
            era = "/".join(p[2:-1]).replace("/thumb", "")
            subject = name.split("_v")[0]
            kind = "thumbnail" if "thumb" in p else "scene"
    elif top == "masters":
        status = "master"
        kind = "character-sheet" if p[1] == "sheets" else "scene"
        subject = p[2] if p[1] == "sheets" else name
        era = p[2] if p[1] == "scenes" else ""
    elif top == "drafts":
        status = "draft"
        person = len(p) > 3 and p[2] in PEOPLE   # drafts/<dynasty>/<person-id>/<file>: an older sheet of that person
        kind = "character-sheet" if person or "sheets" in p or "supporting" in p else "scene"
        subject = p[2] if person else re.sub(r"[-_]?(v\d+|character-sheet).*", "", name)
        era = p[1]
    elif top == "images":
        status = "reference" if p[1] in ("references", "photos") else "generated"
        kind = {"scenes": "scene", "elements": "object", "photos": "photo", "references": "reference"}.get(p[1], "other")
        era = p[2] if p[1] in ("scenes", "elements", "references") and len(p) > 3 else (p[2] if p[1] == "photos" else "")
        subject = name
    elif top == "research":
        status = "research"
        era = p[1]
        kind = "prompt" if "prompts" in p or "prompt" in name else "source" if "sources" in p or "references" in p or "nepal-references" in p else "note"
        subject = name
    return area, kind, subject, era, status


rows = []
for base in ("media", "masters", "drafts", "images", "research"):
    for r, ds, fs in os.walk(ROOT / base):
        ds.sort()
        for f in sorted(fs):
            full = Path(r) / f
            rel = full.relative_to(ROOT).as_posix()
            ext = full.suffix.lower()
            if ext not in IMG | {".pdf", ".md", ".txt", ".json", ".csv", ".zip"} or rel in ("images/README.md", "photos/manifest.csv") or rel.endswith("photos/manifest.csv"):
                continue
            w = h = ""
            if ext in IMG:
                try:
                    with Image.open(full) as im: w, h = im.size
                except Exception: pass
            area, kind, subject, era, status = classify(rel)
            rows.append([rel, area, kind, subject, era, status, w, h, full.stat().st_size // 1024])

with open(ROOT / "INDEX.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["path", "area", "kind", "subject", "era", "status", "width", "height", "kb"])
    wr.writerows(rows)
print(f"INDEX.csv: {len(rows)} rows")
