#!/usr/bin/env python3
"""Add character-sheet images.

Drop files in incoming/ using either layout, then run:  python3 tools/add_sheets.py

    incoming/lachit-borphukan/anything.png          (folder per character)
    incoming/lachit-borphukan__turnaround.png       (id__kind.ext)

Kinds: turnaround, face, costume, props, palette, pose, portrait, other (default: sheet).
Per file it writes media/characters/<id>/<name>.webp (long edge 2000px) and a thumbnail, moves the untouched
original to archive/sheet-originals/<id>/, and adds an `image` row under that person in data/assam_history.csv.
Use --dry-run to preview. Files whose id is unknown are left in incoming/.
"""
import argparse, datetime, hashlib, re, shutil, subprocess, sys
from PIL import Image, ImageOps
from build import ROOT, FULL_KINDS, read_rows, write_rows

KINDS = FULL_KINDS | {"portrait", "pose", "other"}
ARCHIVE = ROOT / "archive"
thumb_of = lambda f: "{0}/thumb/{1}".format(*f.rsplit("/", 1))
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
    rows = read_rows(); added = skipped = 0
    ids = {r["id"] for r in rows if r["type"] == "person"}
    for cid, kind, src in discover():
        if cid not in ids:
            print(f"SKIP  {src.name}: no character with id '{cid}' (check the person rows in data/assam_history.csv)"); skipped += 1; continue
        if kind not in KINDS: kind = "other"
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        n = 1
        while (ROOT / f"media/characters/{cid}/{kind}-{n}.webp").exists() or any(r["file"] == f"media/characters/{cid}/{kind}-{n}.webp" for r in rows): n += 1
        out = f"media/characters/{cid}/{kind}-{n}.webp"
        print(f"ADD   {cid}: {src.name} -> {out}")
        if a.dry_run: added += 1; continue
        w, h = make_webp(src, out)
        keep = ARCHIVE / "sheet-originals" / cid; keep.mkdir(parents=True, exist_ok=True)
        dest = keep / src.name
        if dest.exists(): dest = keep / f"{digest[:8]}-{src.name}"
        shutil.move(str(src), dest)
        at = max(i for i, r in enumerate(rows) if r["id"] == cid or (r["type"] == "image" and r["person"] == cid)) + 1
        rows.insert(at, dict(type="image", id=f"{cid}-{kind}-{n}", person=cid, kind=kind, file=out, thumbnail=thumb_of(out),
                             width=w, height=h, added=datetime.date.today().isoformat()))
        added += 1
    if added and not a.dry_run:
        write_rows(rows)
        for d in sorted((ROOT / "incoming").glob("*/")):
            if d.is_dir() and not any(d.iterdir()): d.rmdir()
        subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)
    print(f"{added} added, {skipped} skipped")

if __name__ == "__main__":
    main()
