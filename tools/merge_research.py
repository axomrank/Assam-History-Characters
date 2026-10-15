#!/usr/bin/env python3
"""Merge data/research/characters_pre1826.json into data/characters.json.

Existing characters (same id) are updated in place: brief and any hand-edited Assamese name are kept.
Era is taken from the entry or worked out from sort_year. Run tools/build.py afterwards (done here).
"""
import json, subprocess, sys
from common import ROOT, load_characters, save_characters

PERIODS = [
 dict(id="kamarupa", name="Kamarupa period", name_as="কামৰূপ যুগ", start=350, end=1100, label="350\u20131100 CE",
      blurb="The Varman, Salastambha and Pala dynasties of ancient Kamarupa, ruling most of the Brahmaputra valley.",
      groups=["Barman dynasty", "Salastambha dynasty", "Pala dynasty", "Contemporaries and visitors"]),
 dict(id="western", name="Western (Namoni) Assam after 1100", name_as="নামনি অসম (১১০০ৰ পিছত)", start=1100, end=1826, label="1100\u20131826, Koch lines to 1949",
      blurb="The kingdoms of Lower (Namoni) Assam and north Bengal after the Palas: the successors of Kamarupa, Kamata, the Khen and Bhuyan rulers, and the Koch kingdom with its branches Koch Hajo, Koch Bihar, Darrang, Beltola, Bijni and Khaspur. Sultans from Bengal and Delhi raided this region from 1206.",
      groups=["Kamarupa after the Palas", "Pala Empire of Bengal", "Kamata and Khen kingdoms", "Baro-Bhuyans", "Bengal and Delhi rulers", "Koch kingdom (undivided)", "Koch Hajo kings", "Koch Bihar kings", "Darrang kings", "Beltola kings", "Bijni kings", "Khaspur kings"]),
 dict(id="ahom", name="Ahom period", name_as="অহম যুগ", start=1228, end=1826, label="1228\u20131826",
      blurb="The Tai-Ahom kingdom of Upper (Ujoni) Assam, founded by Sukaphaa in 1228 and ended by the Burmese invasions and the Treaty of Yandabo in 1826: its kings, queens, nobles and rebels, and the foreign commanders they fought.",
      groups=["Ahom kings", "Ahom queens and royal family", "Ahom officers and generals", "Moamoria rebels", "Mughal and Bengal commanders", "Burmese and British figures"]),
 dict(id="neighbours", name="Neighbouring kingdoms", name_as="চুবুৰীয়া ৰাজ্য", start=1300, end=1830, label="c. 1300\u20131830",
      blurb="The Chutia kingdom of Sadiya, the Dimasa (Kachari) and Barahi kingdoms of the centre and south, and Jaintia and Manipur on the edge of the hills.",
      groups=["Chutia kingdom", "Dimasa (Kachari) kingdom", "Jaintia and Manipur"]),
 dict(id="culture", name="Saints, poets and writers", name_as="সন্ত, কবি আৰু লেখক", start=1250, end=1700, label="13th\u201317th century",
      blurb="Assamese literature and the bhakti movement, which grew across the Kamata, Koch and Ahom lands.",
      groups=["Poets and writers", "Saints of the bhakti movement", "Legends"]),
]
GROUP_PERIOD = {g: p["id"] for p in PERIODS for g in p["groups"]}

LIMITS = [("kamarupa", 1100), ("early-ahom", 1515), ("bhakti", 1603), ("mughal", 1681), ("late-ahom", 1827)]

def era_for(y):
    for e, hi in LIMITS:
        if y < hi: return e
    return "colonial"

def main():
    data = load_characters()
    res = json.loads((ROOT / "data/research/characters_pre1826.json").read_text(encoding="utf-8"))["characters"]
    by_id = {c["id"]: c for c in data["characters"]}
    new = upd = 0
    for r in res:
        era = GROUP_PERIOD.get(r["group"]) or r["era"] or era_for(r["sort_year"])
        if era == "ahom" and r["sort_year"] > 1826: era = "colonial"
        fields = {k: r[k] for k in ("name", "group", "sort_year", "label", "role", "summary", "notes", "reign_start", "reign_end", "birth", "death", "alt_names", "sources", "confidence")}
        for k in ("tai_name", "hindu_name", "nicknames", "ahom_no", "relation", "fate", "koch_branch", "koch_no"):
            if k in r: fields[k] = r[k]
        fields.update(era=era, status="researched", approx=False)
        if r["id"] in by_id:
            c = by_id[r["id"]]
            keep_as = c.get("name_as") or r["name_as"]
            c.update(fields); c["name_as"] = keep_as
            c["match"] = sorted({*c.get("match", []), *r["match"]})
            upd += 1
        else:
            c = dict(id=r["id"], name_as=r["name_as"], match=list(r["match"]), **fields)
            data["characters"].append(c); by_id[r["id"]] = c; new += 1
    for c in data["characters"]:  # Kamarupa entries imported from the CSV: group by dynasty
        if not c.get("group") and c.get("dynasty"): c["group"] = c["dynasty"]
    keep = {e["id"]: e for e in data["eras"]}
    data["eras"] = PERIODS + [keep[i] for i in ("colonial", "modern") if i in keep]
    for c in data["characters"]:  # everything with a known group goes to that group's period
        p = GROUP_PERIOD.get(c.get("group") or c.get("dynasty"))
        if p and not (p == "ahom" and c["sort_year"] > 1826): c["era"] = p
    save_characters(data)
    print(f"{new} new, {upd} updated; {len(data['characters'])} characters total")
    subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)

if __name__ == "__main__":
    main()
