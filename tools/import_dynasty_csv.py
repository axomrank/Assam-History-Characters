#!/usr/bin/env python3
"""Import rulers from a dynasty timeline CSV into data/characters.json.

Columns: Dynasty, Start Year (CE), End Year (CE), Ruler, Wife / Marital Status, Events / Notes, Source Note
Usage:   python3 tools/import_dynasty_csv.py data/sources/<file>.csv --era kamarupa [--drop id,id] [--dry-run]

- Rows whose Ruler is "Unknown" are skipped (nothing to draw).
- Rows with no years are placed between the previous and next dated ruler, in file order.
- Existing characters with the same id are updated (brief and Assamese names are kept).
- Run tools/build.py afterwards (this script does it unless --dry-run).
"""
import argparse, csv, re, subprocess, sys
from pathlib import Path
from common import ROOT, load_characters, save_characters
DYNASTY = {"Barman": "Barman dynasty", "Pal": "Pala dynasty", "Salastambha": "Salastambha dynasty"}

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def tidy(name): return re.sub(r"\s+alias\s+(.+)$", r" (alias \1)", name.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--era", required=True)
    ap.add_argument("--drop", default=""); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    data = load_characters()
    if a.era not in {e["id"] for e in data["eras"]}: sys.exit(f"unknown era {a.era}")
    drop = {x for x in a.drop.split(",") if x}
    data["characters"] = [c for c in data["characters"] if c["id"] not in drop]
    by_id = {c["id"]: c for c in data["characters"]}

    rows = [r for r in csv.DictReader(open(ROOT / a.csv if not Path(a.csv).is_absolute() else a.csv, encoding="utf-8-sig"))
            if r["Ruler"].strip() and r["Ruler"].strip().lower() != "unknown"]
    skipped = [r for r in csv.DictReader(open(a.csv if Path(a.csv).is_absolute() else ROOT / a.csv, encoding="utf-8-sig")) if r["Ruler"].strip().lower() == "unknown"]
    # interpolate years for undated rows
    for i, r in enumerate(rows):
        r["_s"] = int(r["Start Year (CE)"]) if r["Start Year (CE)"].strip() else None
        r["_e"] = int(r["End Year (CE)"]) if r["End Year (CE)"].strip() else None
    i = 0
    while i < len(rows):
        if rows[i]["_s"] is None:
            j = i
            while j < len(rows) and rows[j]["_s"] is None: j += 1
            lo = next((rows[k]["_e"] or rows[k]["_s"] for k in range(i - 1, -1, -1) if rows[k]["_s"] is not None), 0)
            hi = rows[j]["_s"] if j < len(rows) else lo + 10 * (j - i + 1)
            n = j - i
            for k in range(n): rows[i + k]["_sort"] = round(lo + (hi - lo) * (k + 1) / (n + 1), 1)
            i = j
        else: rows[i]["_sort"] = rows[i]["_s"]; i += 1

    new = upd = 0
    for r in rows:
        name = tidy(r["Ruler"]); cid = slug(r["Ruler"])
        dyn = DYNASTY.get(r["Dynasty"].strip(), r["Dynasty"].strip() + " dynasty")
        dated = r["_s"] is not None
        label = f"{r['_s']}–{r['_e']} CE" if dated else "Reign dates not given in the source"
        wife = r["Wife / Marital Status"].strip()
        fields = dict(
            name=name, era=a.era, dynasty=dyn, sort_year=r["_sort"], label=label,
            reign_start=r["_s"], reign_end=r["_e"], undated=not dated,
            role=f"{dyn[:-8] if dyn.endswith(' dynasty') else dyn} dynasty ruler",
            summary=f"Ruler of the {dyn}" + (f", {r['_s']}–{r['_e']} CE." if dated else ", reign dates not given in the source."),
            consort=wife if wife.lower() not in ("", "unknown") else "", marital=wife,
            notes=r["Events / Notes"].strip(), source_note=r["Source Note"].strip(),
            source=Path(a.csv).name, approx=True, status="csv")
        if cid in by_id:
            by_id[cid].update(fields); upd += 1
        else:
            c = dict(id=cid, name_as="", match=[], **fields)
            data["characters"].append(c); by_id[cid] = c; new += 1
    print(f"{new} new, {upd} updated, {len(skipped)} 'Unknown' rows skipped, dropped {len(drop)}")
    if a.dry_run: return
    save_characters(data)
    subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)

if __name__ == "__main__":
    main()
