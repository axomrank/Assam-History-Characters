"""Scenes demanded by the storyline but missing from the site (2026-10-28): the bhakti movement, the Dimasa, Manipur and
Jaintia kingdoms, colonial Assam (1823-1947) and Assam since independence. See storyline.md beside this file.
Run from the project root:  python3 research/storyline-gaps-1468-2011/scenes.py
Writes planned-scenes.csv here and adds missing rows to data/assam_history.csv (status planned, no image)."""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); import build

W = "https://en.wikipedia.org/wiki/"
SD, MD, BD, AN = W + "Sankardev", W + "Madhavdev", W + "Bhattadeva", W + "Aniruddhadeva"
DK, BC, MK = W + "Dimasa_Kingdom", W + "Bhagyachandra", W + "Manipur_(princely_state)"
BR = W + "British_rule_in_Assam"
MRD, ORU, PG = W + "Maniram_Dewan", W + "Orunodoi", W + "Phulaguri_Dhewa"
JON, JOY, KB = W + "Jonaki", W + "Joymoti_(1935_film)", W + "Kanaklata_Barua"
BP, KK, GB, SR = W + "Bhogeswari_Phukanani", W + "Kushal_Konwar", W + "Gopinath_Bordoloi", W + "1947_Sylhet_referendum"
EQ, LM, SW = W + "1950_Assam%E2%80%93Tibet_earthquake", W + "Assam_Official_Language_Act,_1960", W + "Sino-Indian_War"
FA, AM, AA, BH = W + "Fakhruddin_Ali_Ahmed", W + "Assam_Movement", W + "Assam_Accord", W + "Bhupen_Hazarika"
CS, TEA, AC = W + "Chandraprabha_Saikiani", W + "Assam_tea", W + "Assam_Company"
EBA, JM = W + "Eastern_Bengal_and_Assam", W + "Jaintia_Kingdom"

G = {
 "b": ("Bhakti movement (1468–1700)", "culture", "Bhakti chronology"),
 "n": ("Neighbouring kingdoms (1520–1835)", "neighbours", "Neighbouring kingdoms chronology"),
 "c": ("Colonial Assam (1823–1947)", "colonial", "Colonial chronology"),
 "m": ("Assam since independence (1947–2011)", "modern", "Modern chronology"),
}
# id, group key, date_label, sort_year, title, people, main, places, confidence, summary, notes, sources
S = [
 ("BHAKTI-01", "b", "late 15th century (traditional)", 1468, "Sankardev Stages the Chihna Yatra", "sankardev", "sankardev", "bordowa", "low",
  "Young Sankardev stages a dance-drama, the Chihna Yatra, the first of the plays and performances that grow into Ankiya Naat and the satra theatre tradition.",
  "Tradition places it around 1468 at Bordowa; no date was found in the sources checked.", [SD]),
 ("BHAKTI-02", "b", "1522 (traditional) or early 1530s", 1522, "Madhavdev Meets Sankardev", "sankardev; madhavdev", "madhavdev", "", "low",
  "At Dhuwahat, after a long debate, Madhavdev accepts Sankardev as his guru and becomes his chief disciple.",
  "1522 is traditional; revised chronologies place the meeting in the early 1530s.", [MD, SD]),
 ("BHAKTI-03", "b", "after c. 1546", 1550, "The Prayer House at Patbausi", "sankardev; madhavdev", "sankardev", "barpeta", "medium",
  "Settled at Patbausi near Barpeta in Koch territory, Sankardev gathers disciples around a prayer house, the pattern of the namghar and the satra.",
  "Sankardev’s flight from the Ahom kingdom is AHOM-243; his years at the Koch court are KOCH-09, 11 and 20.", [SD]),
 ("BHAKTI-04", "b", "late 16th century", 1569, "Madhavdev Leads the Order", "madhavdev; damodardev", "madhavdev", "barpeta", "low",
  "After Sankardev’s death Madhavdev leads the Ekasarana order, while Damodardev’s followers form a separate branch, the start of the divisions (sanghati) of the movement.",
  "The branches and their dates were not checked in detail; treat as a broad outline.", [MD]),
 ("BHAKTI-05", "b", "late 16th – early 17th century", 1595, "Bhattadev Writes Assamese Prose", "bhattadev", "bhattadev", "", "medium",
  "Bhattadev renders the Bhagavata and the Gita into Assamese prose, among the earliest literary prose in a modern Indian language.", "", [BD]),
 ("BHAKTI-06", "b", "c. 1600", 1600, "Aniruddhadeva Founds the Moamara Satra", "aniruddhadeva", "aniruddhadeva", "", "low",
  "Aniruddhadeva founds the Moamara satra, whose disciples, many of them Morans, later rise against the Ahom state in the Moamoria rebellion.",
  "Founding date approximate. The rebellion itself is in the Ahom scenes (AHOM-203 onward).", [AN]),
 ("DIMASA-01", "n", "Saka 1442 (c. 1520)", 1520, "A Coin at Dimapur", "khorapha", "khorapha", "dimapur", "medium",
  "A coin of Viravijay Narayan, probably Khorapha, struck at Dimapur, is the earliest direct evidence of the Dimasa kingdom.",
  "The Ahom attack on Dimapur in 1536 is AHOM-239 and AHOM-241.", [DK]),
 ("DIMASA-02", "n", "1558 or 1559", 1558, "A New Capital at Maibong", "", "", "maibong", "medium",
  "After a 22-year interregnum following the loss of Dimapur, Nirbhaya Narayana sets up the Dimasa capital at Maibong in the hills.", "", [DK]),
 ("DIMASA-03", "n", "1564", 1564, "The Dimasa Kingdom Bows to the Koch", "chilarai", "", "maibong", "medium",
  "After Chilarai’s victories, the Dimasa kingdom becomes a tributary of the Koch kingdom.", "", [DK]),
 ("DIMASA-04", "n", "c. 1583–1601", 1590, "Yasho Narayan Defeats the Jaintias at Dimarua", "yasho-narayan", "yasho-narayan", "", "low",
  "Yasho Narayan (Satrudaman), the strongest of the Dimasa kings, defeats the Jaintias at Dimarua.", "The year is not given in the sources checked.", [DK]),
 ("DIMASA-05", "n", "c. 1745", 1745, "The Court Moves to Khaspur", "", "", "silchar", "low",
  "Koch rule at Khaspur in the Barak valley ends, the state merges with the Dimasa kingdom, and Khaspur becomes the Dimasa capital.",
  "Sources differ on when the capital moved.", [DK]),
 ("DIMASA-06", "n", "1826", 1826, "Govindachandra Restored by the British", "govindachandra", "govindachandra", "silchar", "medium",
  "After the Treaty of Yandabo the British restore Govindachandra to the Dimasa throne in Cachar.", "", [DK]),
 ("DIMASA-07", "n", "1832–1833", 1832, "Cachar Annexed", "govindachandra", "", "silchar", "medium",
  "After Govindachandra’s death (1830) the British pension off Senapati Tularam and annex his hill region (1832), then Govindachandra’s plains as Cachar district (1833).",
  "The Wikipedia article gives 1832–34 in different places.", [DK]),
 ("MANIPUR-01", "n", "1777", 1777, "The First Maha Ras Lila", "bhagyachandra", "bhagyachandra", "imphal", "medium",
  "At Bhagyachandra’s court the first Manipuri Maha Ras Lila is performed, the beginning of the classical Manipuri dance tradition.",
  "Bhagyachandra’s flight to the Ahom court and Rajeswar Singha’s expeditions are AHOM-201 and AHOM-202.", [BC]),
 ("MANIPUR-02", "n", "1819–1825", 1819, "Manipur under Burmese Occupation", "", "", "imphal", "medium",
  "Burmese armies occupy Manipur, and many Manipuris flee to Cachar and Sylhet.", "", [MK, BC]),
 ("MANIPUR-03", "n", "1825", 1825, "Gambhir Singha Retakes Manipur", "gambhir-singha", "gambhir-singha", "imphal", "medium",
  "With British support in the first Anglo-Burmese war, Gambhir Singha drives the Burmese out and is restored as king of Manipur.", "", [MK, BC]),
 ("JAINTIA-01", "n", "1835", 1835, "The Jaintia Kingdom Annexed", "", "", "jaintiapur", "medium",
  "The British annex the Jaintia kingdom, ending its rule over the plains around Jaintiapur and the Jaintia hills.", "", [JM]),
 ("COL-01", "c", "1823", 1823, "The Assam Tea Plant Shown to Robert Bruce", "maniram-dewan", "maniram-dewan", "", "medium",
  "Guided by Maniram Dewan, the Scottish trader Robert Bruce is shown the tea plant growing wild, used by the Singpho, in upper Assam.", "", [MRD, TEA]),
 ("COL-02", "c", "1839", 1839, "The Assam Company", "maniram-dewan", "maniram-dewan", "", "medium",
  "The Assam Company is formed to grow tea commercially; Maniram Dewan serves it before starting his own gardens.", "", [AC, MRD]),
 ("COL-03", "c", "January 1846", 1846, "Orunodoi, the First Assamese Magazine", "nathan-brown; miles-bronson", "nathan-brown", "sivasagar", "high",
  "American Baptist missionaries at Sivasagar begin Orunodoi, the first Assamese magazine.", "", [ORU]),
 ("COL-04", "c", "26 February 1858", 1858, "Maniram Dewan and Piyali Baruah Hanged", "maniram-dewan", "maniram-dewan", "jorhat", "high",
  "For plotting a rising in 1857 to restore Ahom rule, Maniram Dewan and Piyali Baruah are hanged at Jorhat jail.", "", [MRD]),
 ("COL-05", "c", "1861", 1861, "Phulaguri Dhewa", "", "", "nagaon", "medium",
  "Peasants at Phulaguri in Nagaon rise against new taxes; police fire on the gathering, and leaders are hanged or deported.",
  "Often called the first peasant rising in Assam. Casualty figures vary by source and are not painted as fact.", [PG, BR]),
 ("COL-06", "c", "1873", 1873, "Assamese Restored in Schools and Courts", "", "", "", "medium",
  "After decades of Bengali as the official language, Assamese is restored in the schools and courts of Assam, a campaign begun by Anandaram Dhekial Phukan and the missionaries.", "", [BR]),
 ("COL-07", "c", "1874", 1874, "Assam Becomes a Province", "", "", "", "medium",
  "Assam is separated from Bengal as a Chief Commissioner’s province, with Sylhet and the hill districts.", "", [BR]),
 ("COL-08", "c", "1889", 1889, "Jonaki", "lakshminath-bezbaroa; hemchandra-goswami", "lakshminath-bezbaroa", "", "medium",
  "Assamese students in Calcutta start the magazine Jonaki, opening the romantic age of modern Assamese literature.", "", [JON]),
 ("COL-09", "c", "28 January 1894", 1894, "Patharughat", "", "", "", "medium",
  "At Patharughat in Darrang, troops fire on peasants gathered to protest a steep rise in land revenue.",
  "The exact day is from a single source checked; casualty figures vary.", [W + "Darrang_district", BR]),
 ("COL-10", "c", "1905–1912", 1905, "Eastern Bengal and Assam", "", "", "", "medium",
  "The partition of Bengal joins Assam with eastern Bengal in a new province, undone in 1912.", "", [EBA]),
 ("COL-11", "c", "August 1921", 1921, "Gandhi in Assam", "", "", "guwahati", "medium",
  "Gandhi tours Assam during the Non-Cooperation movement; foreign cloth is burnt and Assamese join the national movement in numbers.", "", [BR]),
 ("COL-12", "c", "1926", 1926, "The Assam Women’s Association", "chandraprabha-saikiani", "chandraprabha-saikiani", "", "medium",
  "Chandraprabha Saikiani founds the Assam Pradeshik Mahila Samiti, the province’s women’s organisation.", "", [CS]),
 ("COL-13", "c", "1935", 1935, "Joymoti, the First Assamese Film", "jyotiprasad-agarwala", "jyotiprasad-agarwala", "", "high",
  "Jyotiprasad Agarwala makes Joymoti, the first Assamese feature film, telling the story of the Ahom princess (AHOM-174, 177, 281).", "", [JOY]),
 ("COL-14", "c", "20 September 1942", 1942, "Kanaklata at Gohpur", "kanaklata-barua", "kanaklata-barua", "", "high",
  "In the Quit India movement, seventeen-year-old Kanaklata Barua leads a procession to raise the national flag at the Gohpur police station and is shot dead.", "", [KB]),
 ("COL-15", "c", "20 September 1942", 1942, "Bhogeswari Phukanani at Barhampur", "bhogeswari-phukanani", "bhogeswari-phukanani", "nagaon", "medium",
  "On the same day Bhogeswari Phukanani, a mother of eight, is shot while trying to raise the flag at Barhampur in Nagaon.", "", [BP]),
 ("COL-16", "c", "15 June 1943", 1943, "Kushal Konwar Hanged", "kushal-konwar", "kushal-konwar", "jorhat", "high",
  "Blamed for the derailment of a military train at Sarupathar, the Gandhian Kushal Konwar is hanged at Jorhat jail.",
  "Sources differ on the date of the derailment (1942).", [KK]),
 ("COL-17", "c", "1946", 1946, "Bordoloi Refuses the Grouping", "gopinath-bordoloi", "gopinath-bordoloi", "", "medium",
  "Gopinath Bordoloi leads Assam’s resistance to the Cabinet Mission plan, which would have grouped Assam with Bengal.", "", [GB]),
 ("COL-18", "c", "July 1947", 1947, "The Sylhet Referendum", "", "", "sylhet", "medium",
  "Sylhet votes to join East Pakistan, and Assam enters independence without it.", "", [SR]),
 ("MOD-01", "m", "15 August 1950", 1950, "The Great Earthquake", "", "", "", "high",
  "One of the strongest earthquakes on record strikes Assam and Tibet, changing rivers and burying land under sand.", "", [EQ]),
 ("MOD-02", "m", "1960", 1960, "The Language Movement", "bimala-prasad-chaliha", "", "", "medium",
  "Assamese is made the official language of the state by the Official Language Act, after a year of agitation.", "", [LM]),
 ("MOD-03", "m", "November 1962", 1962, "War Reaches Bomdila", "", "", "", "medium",
  "In the Sino-Indian war, Chinese forces take Bomdila; Tezpur is evacuated before the ceasefire.", "", [SW]),
 ("MOD-04", "m", "24 August 1974", 1974, "Fakhruddin Ali Ahmed Becomes President", "fakhruddin-ali-ahmed", "fakhruddin-ali-ahmed", "", "high",
  "Fakhruddin Ali Ahmed of Assam is sworn in as the fifth President of India.", "", [FA]),
 ("MOD-05", "m", "1979–1985", 1979, "The Assam Movement", "prafulla-kumar-mahanta", "", "guwahati", "medium",
  "Students of AASU and others lead a six-year mass movement over immigration and the electoral rolls.",
  "Paint the mass protest; the violence of the period is not to be staged as spectacle.", [AM]),
 ("MOD-06", "m", "15 August 1985", 1985, "The Assam Accord", "prafulla-kumar-mahanta", "prafulla-kumar-mahanta", "", "high",
  "The Assam Accord is signed with the central government, ending the movement; Prafulla Kumar Mahanta becomes Chief Minister that December.", "", [AA]),
 ("MOD-07", "m", "November 2011", 2011, "Farewell to Bhupen Hazarika", "bhupen-hazarika", "bhupen-hazarika", "guwahati", "medium",
  "Vast crowds in Guwahati bid farewell to the singer and filmmaker Bhupen Hazarika.", "", [BH]),
]

def rows():
    out = []
    for (i, g, dl, sy, name, people, main, places, conf, summ, notes, src) in S:
        grp, per, col = G[g]
        r = dict.fromkeys(build.COLS, "")
        r.update(type="scene", id=i, name=name, period=per, group=grp, date_label=dl, sort_year=str(sy), people=people,
                 main_people=main, places=places, confidence=conf, status="planned", collection=col, summary=summ,
                 notes=notes, sources="; ".join(src))
        out.append(r)
    return out

if __name__ == "__main__":
    new = rows(); here = Path(__file__).parent
    with open(here / "planned-scenes.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, build.COLS); w.writeheader(); w.writerows(new)
    data = build.read_rows(); have = {(r["type"], r["id"]) for r in data}
    added = [r for r in new if ("scene", r["id"]) not in have]
    data += added
    scenes = build.scene_order([r for r in data if r["type"] == "scene"])
    build.write_rows([r for r in data if r["type"] != "scene"] + scenes)
    print(f"{len(new)} scenes in planned-scenes.csv, {len(added)} added to the CSV")
