"""Shared helpers: paths, JSON IO and the compact on-disk shape of characters and sheets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES = "data/scenes.json"            # catalogued scenes
CHAR_MEDIA = "media/characters"        # character sheets and portraits, one folder per id
ARCHIVE = ROOT / "archive"             # originals and retired files, not published
FULL_KINDS = {"sheet", "turnaround", "face", "costume", "props", "palette"}   # a real character sheet
PORTRAIT_KINDS = {"portrait", "pose"}                                       # a likeness, not a sheet
ALWAYS = ("id", "name", "era", "sort_year", "label", "role", "summary")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path, obj, indent=1):
    (ROOT / path).write_text(json.dumps(obj, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")


def compact_char(c):
    """Drop empty values and fields that live elsewhere (sheets) or duplicate others (dynasty = group)."""
    c = dict(c)
    c.pop("sheets", None); c.pop("scenes", None)
    if c.get("dynasty") and not c.get("group"): c["group"] = c["dynasty"]
    if c.get("dynasty") == c.get("group"): c.pop("dynasty", None)
    b = c.get("brief")
    if b is not None and not any(b.values()): c.pop("brief")
    return {k: v for k, v in c.items() if k in ALWAYS or not (v in ("", None, [], {}) or v is False)}


def load_characters():
    return read("data/characters.json")


def save_characters(data):
    data["characters"] = [compact_char(c) for c in data["characters"]]
    write("data/characters.json", data)


def load_sheets():
    p = ROOT / "data/sheets.json"
    return read("data/sheets.json")["sheets"] if p.exists() else []


def save_sheets(rows):
    rows = sorted(rows, key=lambda r: (r["char"], r["kind"], r["file"]))
    write("data/sheets.json", {"schema": "ahom-sheets-v1", "note": "One row per image made for a character. Thumbnails are at <dir>/thumb/<name>.", "sheets": rows})


def thumb_of(file):
    d, n = file.rsplit("/", 1)
    return f"{d}/thumb/{n}"
