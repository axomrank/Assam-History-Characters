#!/usr/bin/env python3
"""Add character-sheet images.

Drop files in incoming/ using either layout, then run:  python3 tools/add_sheets.py

    incoming/lachit-borphukan/anything.png          (folder per character)
    incoming/lachit-borphukan__turnaround.png       (id__kind.ext)

Kinds: turnaround, face, costume, props, palette, pose, portrait, other (default: sheet).
Per file it writes sheets/<id>/<name>.webp (long edge 2000px) and a thumbnail, moves the untouched
original to sheets_src/<id>/, and adds a row to data/sheets.json. Use --dry-run to preview.
Files whose id is unknown are left in incoming/.
"""
import argparse, datetime, hashlib, re, shutil, subprocess, sys
from PIL import Image, ImageOps
from common import ROOT, FULL_KINDS, PORTRAIT_KINDS, load_characters, load_sheets, save_sheets, thumb_of

KINDS = FULL_KINDS | PORTRAIT_KINDS | {"other"}
EXT = {".png", ".jpg", ".jpeg", ".webp"}
MAX_EDGE, THUMB_W = 2000, 640

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def discover():
    inc = ROOT / "incoming"
    for p in sorted(inc.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXT: continue
        rel = p.relative_to(inc)
        if len(rel.parts) > 1:
            stem = slug(p.stem.split("__")[-1])
            yield rel.parts[0], (stem if stem in KINDS else "sheet"), p
        elif "__" in p.stem:
            cid, kind = p.stem.split("__", 1); yield cid, slug(kind), p
        else:
            yield p.stem, "sheet", p

def make_webp(im_path, out_file):
    im = ImageOps.exif_transpose(Image.open(im_path))
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    full = im.copy(); full.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    th = im.copy(); th.thumbnail((THUMB_W, THUMB_W), Image.LANCZOS)
    dest = ROOT / out_file; (dest.parent / "thumb").mkdir(parents=True, exist_ok=True)
    full.save(dest, "WEBP", quality=88, method=6)
    th.save(ROOT / thumb_of(out_file), "WEBP", quality=80, method=6)
    return full.size

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    ids = {c["id"] for c in load_characters()["characters"]}
    rows = load_sheets(); added = skipped = 0
    for cid, kind, src in discover():
        if cid not in ids:
            print(f"SKIP  {src.name}: no character with id '{cid}' (check data/characters.json)"); skipped += 1; continue
        if kind not in KINDS: kind = "other"
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if any(r["char"] == cid and r["sha256"] == digest for r in rows):
            print(f"SKIP  {src.name}: already added to {cid}"); skipped += 1; continue
        n = sum(1 for r in rows if r["char"] == cid and r["kind"] == kind) + 1
        out = f"sheets/{cid}/{kind}-{n}.webp"
        print(f"ADD   {cid}: {src.name} -> {out}")
        if a.dry_run: added += 1; continue
        w, h = make_webp(src, out)
        keep = ROOT / "sheets_src" / cid; keep.mkdir(parents=True, exist_ok=True)
        dest = keep / src.name
        if dest.exists(): dest = keep / f"{digest[:8]}-{src.name}"
        shutil.move(str(src), dest)
        rows.append(dict(char=cid, kind=kind, file=out, w=w, h=h, sha256=digest, added=datetime.date.today().isoformat()))
        added += 1
    if added and not a.dry_run:
        save_sheets(rows)
        for d in sorted((ROOT / "incoming").glob("*/")):
            if d.is_dir() and not any(d.iterdir()): d.rmdir()
        subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)
    print(f"{added} added, {skipped} skipped")

if __name__ == "__main__":
    main()
