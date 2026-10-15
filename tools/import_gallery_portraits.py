#!/usr/bin/env python3
"""Attach existing Assamese AI gallery images to the character they depict.

Matches catalog.json gallery entries to characters by name, then creates web-sized images in
sheets/<id>/ and rows in data/sheets.json. Originals in images/ stay untouched. Safe to re-run.
Usage: python3 tools/import_gallery_portraits.py [--dry-run]
"""
import argparse, datetime, re, subprocess, sys
from common import ROOT, load_characters, load_sheets, save_sheets, read
from add_sheets import make_webp

PORTRAIT = re.compile(r"portrait|study|close-up|formal", re.I)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    cat = read("catalog.json"); alias = cat["metadata"].get("aliases", {})
    by_name = {}
    for c in load_characters()["characters"]:
        for n in {c["name"], *c.get("match", [])}: by_name.setdefault(n, set()).add(c["id"])
    rows = load_sheets(); added = 0
    for r in cat["images"]:
        if r["collection"] != "Assamese AI gallery": continue
        ids = by_name.get(r["ruler"], set()) | by_name.get(alias.get(r["ruler"], ""), set())
        if len(ids) != 1: continue
        cid = next(iter(ids))
        if any(x["char"] == cid and x["sha256"] == r["sha256"] for x in rows): continue
        kind = "portrait" if PORTRAIT.search(r["event"] + " " + r["filename"]) else "pose"
        n = sum(1 for x in rows if x["char"] == cid and x["kind"] == kind) + 1
        out = f"sheets/{cid}/{kind}-{n}.webp"
        print(f"ADD {cid}: {r['filename']} -> {kind}")
        if a.dry_run: added += 1; continue
        w, h = make_webp(ROOT / r["file"], out)
        rows.append(dict(char=cid, kind=kind, file=out, caption=r["event"], w=w, h=h, sha256=r["sha256"], added=datetime.date.today().isoformat(), source=f"gallery:{r['id']}"))
        added += 1
    print(f"{added} images attached")
    if added and not a.dry_run:
        save_sheets(rows); subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)

if __name__ == "__main__":
    main()
