"""Convert catalogued scene images to web-sized WebP and point data/scenes.json at them.

Originals are moved (never deleted) to archive/original-scenes/<same folders>, so they stay out of the published site.
Run: python3 tools/optimize_scenes.py [--dry-run]   then   python3 tools/build.py
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive"
MAX_SIDE, QUALITY = 1600, 82


def main(dry=False):
    cat = json.loads((ROOT / "data/scenes.json").read_text(encoding="utf-8"))
    done = 0
    for r in cat["images"]:
        src = ROOT / r["file"]
        if src.suffix.lower() == ".webp":
            continue
        dst = src.with_suffix(".webp")
        if not dry:
            if src.exists():
                im = Image.open(src)
                im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
                im.save(dst, "WEBP", quality=QUALITY, method=6)
                keep = ARCHIVE / "original-scenes" / Path(*Path(r["file"]).parts[2:])
                keep.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), keep)
            elif not dst.exists():
                print("missing:", r["file"]); continue
        r["file"] = str(dst.relative_to(ROOT))
        r["filename"] = dst.name
        done += 1
    print(f"{done} scene image(s) {'would be ' if dry else ''}converted")
    if not dry:
        (ROOT / "data/scenes.json").write_text(json.dumps(cat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
