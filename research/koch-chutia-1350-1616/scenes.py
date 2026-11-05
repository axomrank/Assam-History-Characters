"""Planned scenes for the Koch kingdom (1515-1587), Koch Hajo (1581-1616) and the Chutia kingdom (1350-1524).
Researched 2026-10-28; see storyline.md and sources.md beside this file.
Run from the project root:  python3 research/koch-chutia-1350-1616/scenes.py
It writes planned-scenes.csv here and adds any missing rows to data/assam_history.csv (status planned, no image)."""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); import build

W = "https://en.wikipedia.org/wiki/"
KD, BS, NN, CR = W + "Koch_dynasty", W + "Biswa_Singha", W + "Nara_Narayan", W + "Chilarai"
KA, KT, SD, KH = W + "Koch%E2%80%93Ahom_conflicts", W + "Kamakhya_Temple", W + "Sankardev", W + "Koch_Hajo"
HM, KC, RS, KP = W + "Hayagriva_Madhava_Temple", W + "Koch_coinage", W + "Rama_Saraswati", W + "Kalapahad"
SKB = "https://en.banglapedia.org/index.php/Sulaiman_Karrani"
CK, TT, BN, SS = W + "Chutia_Kingdom", W + "Tamreswari_Temple", W + "Bhismaknagar", W + "Sati_Sadhani"

GK, GH, GC = "Koch kingdom (1515–1587)", "Koch Hajo (1581–1616)", "Chutia kingdom (1350–1524)"
COL = {GK: "Koch chronology", GH: "Koch chronology", GC: "Chutia chronology"}
PER = {GK: "western", GH: "western", GC: "neighbours"}

# id, group, date_label, sort_year, title, people, main_people, places, confidence, summary, notes, sources
S = [
 ("KOCH-01", GK, "c. 1515–1520", 1516, "Biswa Singha Counts His People", "biswa-singha; sisu-koch", "biswa-singha", "koch-kingdom", "medium",
  "After a census, Biswa Singha organises his fighting men in graded units under officers called Thakuria, Saikia, Hazari, Omra and Nawab, appoints twelve Karji ministers from Mech families, makes his brother Sisu yuvaraj and names a senapati.",
  "From later chronicles as summarised on Wikipedia; unit sizes are not given in the sources checked.", [BS]),
 ("KOCH-02", GK, "c. 1515–1530", 1518, "The Court Moves to Hingulabas", "biswa-singha", "biswa-singha", "koch-kingdom", "low",
  "At his mother’s request Biswa Singha moves his seat from the Chikna hills to Hingulabas; Kamatapur later becomes the capital.",
  "The capital sequence comes from much later sources and its dates are uncertain; the early seat is spelt Chikana, Chikanabari or Chiknabari.", [BS, KD]),
 ("KOCH-03", GK, "early 16th century", 1520, "Biswa Singha Revives Worship at Kamakhya", "biswa-singha", "biswa-singha", "kamakhya; nilachal", "low",
  "Biswa Singha is said to have found the ruined shrine on Nilachal hill and restored worship there.",
  "Tradition. The earlier destruction is now usually dated to Husain Shah’s invasion of 1498, not to Kalapahar.", [KT]),
 ("KOCH-04", GK, "early 16th century", 1525, "Learned Brahmins Come to the Koch Court", "biswa-singha; nara-narayan; chilarai", "biswa-singha", "koch-kingdom; kanauj", "medium",
  "Biswa Singha sends his sons Malladev (Nara Narayan) and Sukladhwaj (Chilarai) to study under Brahmananda at Varanasi, and brings priests from Kanauj, Mithila, Benaras and Puri.",
  "", [BS]),
 ("KOCH-05", GK, "c. 1532", 1532, "Biswa Singha Makes Peace with the Ahom Army", "biswa-singha; ton-kham-borgohain", "biswa-singha", "karatoya", "medium",
  "Returning from chasing Turbak’s Bengal army to the Karatoya, the Ahom general Tonkham Borgohain meets Biswa Singha, who makes peace and agrees to send the Ahom court a yearly tribute of horses.",
  "Seen from the Koch side; the pursuit itself is AHOM-101.", [KA, BS]),
 ("KOCH-06", GK, "1537", 1537, "The March to Singari Turns Back", "biswa-singha; suhungmung", "biswa-singha", "", "medium",
  "Biswa Singha advances into Ahom territory as far as Singari but gives up for lack of supplies. That winter he and his brother visit Suhungmung’s court.",
  "Singari is placed in Nagaon district by the source; not linked to a place record.", [KA, BS]),
 ("KOCH-07", GK, "1540", 1540, "The Princes Return from Varanasi", "nara-narayan; chilarai", "nara-narayan", "koch-kingdom", "medium",
  "After Biswa Singha’s death, Nara Narayan and Chilarai come back from Varanasi; Nara Narayan takes the throne, with Chilarai as his commander.",
  "The chronicles disagree on Biswa Singha’s death (sores or smallpox), and one Wikipedia infobox even dates Nara Narayan’s reign from 1554.", [NN, BS]),
 ("KOCH-08", GK, "completed 1547", 1547, "Building the Gohain Kamal Ali", "gosain-kamal; nara-narayan", "gosain-kamal", "narayanpur; cooch-behar", "medium",
  "An embanked road some 350 miles long is raised from Koch Bihar to Narayanpur for the war against the Ahoms; it carries the name of Gohain Kamal, Nara Narayan’s brother, and a fort is built at Narayanpur.",
  "Completion in 1547 from the Koch–Ahom conflicts article; the attribution to Gohain Kamal is traditional.", [KA]),
 ("KOCH-09", GK, "c. 1554", 1554, "Weaving the Vrindavani Vastra", "sankardev; nara-narayan", "sankardev", "barpeta", "medium",
  "For Nara Narayan, master weavers at Tantikuchi near Barpeta, guided by Sankardev, weave a long silk cloth showing Krishna’s life in Vrindavan.",
  "One account gives completion in 1554 after six months’ weaving by twelve masters; surviving fragments in London and Los Angeles are dated c. 1570.", [SD]),
 ("KOCH-10", GK, "Saka 1477 (1555 CE)", 1555, "The First Narayani Coins", "nara-narayan", "nara-narayan", "koch-kingdom", "medium",
  "Nara Narayan strikes silver coins in his own name, the Narayani, dated Saka 1477. The same year he writes to the Ahom king Sukhaamphaa proposing friendship and is rebuffed.",
  "Gait (1895) records a coin of Saka 1477 found in the Garo Hills; some coins bearing this date may be later issues.", [KC, KA]),
 ("KOCH-11", GK, "1550s–1560s", 1558, "Sankardev Answers the Pundits", "sankardev; nara-narayan; chilarai", "sankardev", "cooch-behar", "medium",
  "Accused of spreading a new faith, Sankardev goes into hiding when Nara Narayan orders his arrest. Brought to court through Chilarai, he answers the pundits in debate; the king frees him and seats him near the throne.",
  "Undated in the sources. Two associates, Thakur Ata and Gokulchand, were arrested and tortured in his place.", [SD]),
 ("KOCH-12", GK, "1562", 1562, "Chilarai Takes the Barak Valley", "chilarai", "chilarai", "", "medium",
  "Chilarai wins the Barak valley from Tripura and sets up the outpost of Khaspur, which a step-brother’s line later governs.",
  "Udita Narayan declared Khaspur independent in 1590.", [KD]),
 ("KOCH-13", GK, "1560s", 1563, "Manipur’s King Pays Tribute", "chilarai", "chilarai", "manipur", "medium",
  "Ripu Singha of Manipur submits to Chilarai without a fight, paying silver, gold and elephants; a yearly tribute follows.",
  "Year not given in the sources checked (Choudhary 2024, cited on Wikipedia).", [CR]),
 ("KOCH-14", GK, "1560s", 1564, "The Battle at Langai", "chilarai", "chilarai", "", "medium",
  "In the campaign against Tripura its king is killed in battle at Langai; his brother submits and rules under a yearly tribute.",
  "Nath (1989), cited on Wikipedia; year not given.", [CR]),
 ("KOCH-15", GK, "1560s", 1564, "The Jaintia Prince Submits", "chilarai", "chilarai", "jaintiapur", "medium",
  "The Jaintia king is killed fighting Chilarai’s army; his son submits and pays horses, coins and swords, with a yearly tribute.",
  "Nath (1989), cited on Wikipedia; year not given.", [CR]),
 ("KOCH-16", GK, "1560s", 1565, "Chilarai at Sylhet", "chilarai", "chilarai", "sylhet", "medium",
  "After two days of fighting Chilarai kills the governor of Sylhet, and the governor’s brother pays a heavy tribute. On the way back he defeats the small chiefdom of Dimarua and imprisons its king, later releasing him.",
  "Choudhary (2024), cited on Wikipedia; year not given.", [CR]),
 ("KOCH-17", GK, "1565", 1565, "Meghamukdam’s Brick Dome at Kamakhya", "chilarai; nara-narayan", "chilarai", "kamakhya; nilachal", "high",
  "The Kamakhya temple is rebuilt under Chilarai’s supervision, as its inscription of 1565 records. After two failed attempts at a stone spire, the Koch artisan Meghamukdam raises a brick dome, the start of the ‘Nilachal’ temple type.",
  "Material from the older ruined temples was reused, and some survives in the walls.", [KT]),
 ("KOCH-18", GK, "1565", 1566, "The Koch Fleet Routed", "", "", "brahmaputra", "medium",
  "Rebuilt after the Treaty of Majuli, Ahom forces rout the Koch river fleet under Tepu Barua.",
  "Tepu Barua is not a person record yet.", [KA]),
 ("KOCH-19", GK, "1568", 1568, "Chilarai Captured in Bengal", "chilarai", "chilarai", "gaur", "medium",
  "Chilarai invades the Bengal of Sulaiman Karrani; when its weapons run out his army is beaten and he is taken prisoner, through Kalapahar’s stratagem in some accounts. He is later set free.",
  "Sources differ on how long he was held (a year, or a few years) and on Kalapahar’s part. Sulaiman Karrani and Kalapahar are not person records yet.", [SKB, KP]),
 ("KOCH-20", GK, "1568 or 1569", 1569, "Sankardev’s Last Days at Bheladonga", "sankardev", "sankardev", "cooch-behar", "medium",
  "Sankardev dies at Bheladonga near the Koch capital, having declined Nara Narayan’s request to become his disciple.",
  "1568 on Wikipedia; Neog gives 1569 (Saka 1490).", [SD]),
 ("KOCH-21", GK, "December 1570 – January 1571", 1570, "Turned Back at the Dhansiri", "", "", "dhansiri", "medium",
  "The last Koch expedition against the Ahoms is repulsed at the Dhansiri.", "", [KA]),
 ("KOCH-22", GK, "1571", 1571, "Chilarai Dies on the Ganges", "chilarai", "chilarai", "", "medium",
  "Chilarai, the ‘kite’ general named for the speed of his marches, dies of smallpox on the bank of the Ganges.", "", [CR]),
 ("KOCH-23", GK, "16th century", 1575, "An Edict for the Old Faiths", "nara-narayan", "nara-narayan", "koch-kingdom", "medium",
  "Nara Narayan issues an edict recognising the religious practices of the Koch, Mech and Kachari peoples, alongside the Brahmanical order of his court.",
  "Undated in the sources checked.", [NN, KD]),
 ("KOCH-24", GK, "16th century", 1576, "The Epics in Assamese", "nara-narayan", "nara-narayan", "koch-kingdom", "low",
  "Nara Narayan commissions Assamese versions of the Bhagavad Gita, the Puranas and the Mahabharata. Rama Saraswati, remembered as ‘Axom Byas’, renders the Mahabharata.",
  "The commission is on Wikipedia; that Rama Saraswati worked under it is usual in Assamese literary history but was not stated in the sources checked. Rama Saraswati is not a person record yet.", [NN, RS]),
 ("KOCH-25", GK, "1581", 1581, "The Kingdom Divided", "nara-narayan; raghudev", "raghudev", "koch-hajo; manas", "medium",
  "Nara Narayan makes his nephew Raghudev, Chilarai’s son, king of the eastern part at Barnagar near the Manas, paying tribute. The western part is to go to his own son Lakshmi Narayan.",
  "The site does not cover the Koch Bihar line (user decision, 2026-10-28).", [KH, NN]),
 ("HAJO-01", GH, "1583", 1583, "Raghudev Builds the Hayagriva Madhava Temple", "raghudev", "raghudev", "hajo; hayagriva-madhava", "high",
  "On Manikut hill at Hajo, Raghudev completes the temple of Hayagriva Madhava, recorded in his inscription.",
  "Whether it replaced an older temple is not stated in the sources checked.", [HM]),
 ("HAJO-02", GH, "1587", 1587, "Raghudev Stops the Tribute", "raghudev", "raghudev", "koch-hajo", "medium",
  "When Nara Narayan dies, Raghudev stops paying tribute and declares Koch Hajo independent.", "", [KH]),
 ("HAJO-03", GH, "1596", 1596, "Raghudev and Isa Khan Strike Bahirbandh", "raghudev", "raghudev", "north-guwahati; sonargaon", "medium",
  "Allied with Isa Khan, chief of the Bengal Bhuyans, Raghudev attacks Bahirbandh in Koch Bihar, and moves his capital from Barnagar to North Guwahati.",
  "Isa Khan is not a person record yet.", [KH]),
 ("HAJO-04", GH, "1597", 1597, "Defeat and Recovery", "raghudev", "raghudev", "koch-hajo", "medium",
  "In May a Koch Bihar and Mughal army defeats Raghudev. Later that year Isa Khan helps him win back his ground, routing the Mughals and killing their commander Durjan Singh.",
  "From Nath (1989), the single source behind the Koch Hajo article.", [KH]),
 ("HAJO-05", GH, "1603", 1603, "A Contested Throne", "raghudev; parikshit-narayan; man-singha-koch", "parikshit-narayan", "koch-hajo; namrup", "medium",
  "Raghudev dies and his son Parikshit Narayan takes the throne; another prince, Man Singha, takes refuge with the Ahoms at Namrup.",
  "Raghudev’s offer of his daughter Mangaldoi to the Ahom king is AHOM-244.", [KH]),
 ("HAJO-06", GH, "1603–1608", 1605, "Parikshit Recovers the Royal Insignia", "parikshit-narayan", "parikshit-narayan", "koch-hajo", "medium",
  "Parikshit Narayan occupies Bahirbandh and recovers the royal insignia from Koch Bihar.", "", [KH]),
 ("HAJO-07", GH, "July 1612", 1612, "The Mughal Fleet Sails from Dhaka", "parikshit-narayan", "parikshit-narayan", "koch-hajo", "medium",
  "Allied with Lakshmi Narayan of Koch Bihar, the Mughal governor of Bengal sends an army and a river fleet from near Dhaka against Koch Hajo. By the end of the year the kingdom is occupied.",
  "", [KH, KD]),
 ("HAJO-08", GH, "1613–1614", 1614, "Parikshit Narayan Surrenders at Pandu", "parikshit-narayan; balinarayan", "parikshit-narayan", "pandu", "medium",
  "Driven back to Pandu near Guwahati, Parikshit Narayan surrenders and agrees to serve the Mughals, but dies before he can take up the post. His brother Balinarayan escapes to the Ahoms.",
  "One account says Parikshit was taken to Delhi. Balinarayan’s reception is AHOM-246.", [KH, KD]),
 ("CHUTIA-01", GC, "Saka 1314 (1392 CE)", 1392, "A Land Grant at Sadhayapuri", "nandi-chutia; satyanarayana-chutia", "satyanarayana-chutia", "sadiya", "medium",
  "At Sadhayapuri the Chutia kings Nandi and Satyanarayana issue the Dhenukhana copper plate, a Sanskrit land grant and the earliest dated record of the kingdom.", "", [CK]),
 ("CHUTIA-02", GC, "late 14th century", 1395, "Vaishnava Brahmins at the Chutia Court", "satyanarayana-chutia", "satyanarayana-chutia", "sadiya", "low",
  "Vaishnava Brahmins reach the Chutia court and compose genealogies linking its kings to Krishna’s family, while ranking them below themselves.", "", [CK]),
 ("CHUTIA-03", GC, "1401", 1401, "Lakshminarayana’s Ghilamara Grant", "lakshminarayana-chutia", "lakshminarayana-chutia", "", "medium",
  "Lakshminarayana issues a copper-plate land grant, later found at Ghilamara.", "", [CK]),
 ("CHUTIA-04", GC, "early 15th century", 1405, "The Brick Fort at Bhismaknagar", "lakshminarayana-chutia", "lakshminarayana-chutia", "dibang", "low",
  "At the foot of the Mishmi hills a fortified city of fired brick and stone rises, with walls about 4.5 m high, a palace complex of three halls and several tanks. A brick bearing Lakshminarayana’s name suggests it was his capital.",
  "The name Bhismaknagar is modern (1928 gazetteer), from the Rukmini legend. Excavation has been limited.", [BN]),
 ("CHUTIA-05", GC, "Saka 1350 (1428 CE)", 1428, "Durlabhnarayana’s Grant at Sadiya", "durlabhnarayana-chutia", "durlabhnarayana-chutia", "sadiya", "medium",
  "Durlabhnarayana issues the Sadiya-Chepakhowa copper-plate grant.", "", [CK]),
 ("CHUTIA-06", GC, "Saka 1364 (1442 CE)", 1442, "A Brick Wall for Kechaikhati", "muktadharmanarayana", "muktadharmanarayana", "sadiya", "medium",
  "Mukta Dharmanarayana, a Chutia prince, builds the brick wall of the shrine of the goddess Kechaikhati (Dikkaravasini) on the Paya river, served by Deori priests. A later copper roof gives the temple its name, Tamreswari.",
  "The copper roof is described in a 1711 chronicle; human sacrifice there is reported, mostly from later accounts.", [TT, CK]),
 ("CHUTIA-07", GC, "15th century", 1460, "Smiths and Salt Wells of Sadiya", "", "", "sadiya", "low",
  "Chutia blacksmiths, bell-metal workers and goldsmiths, and the salt springs at Borhat, make the kingdom one of the most productive of the valley.",
  "A general scene; scholars call the Chutias the most advanced tribal polity of the 15th-century valley, but details are disputed.", [CK]),
 ("CHUTIA-08", GC, "1513", 1513, "Dhirnarayan’s Stockade at Dikhowmukh", "dhirnarayan; suhungmung", "dhirnarayan", "dikhowmukh", "medium",
  "In a border dispute Dhirnarayan raises the Posola-garh stockade at Dikhowmukh; an Ahom force led by Suhungmung routs the Chutias.", "", [CK]),
 ("CHUTIA-09", GC, "1520", 1520, "The Chutias Take Mungkhrang", "dhirnarayan", "dhirnarayan", "", "medium",
  "Chutia forces attack the Ahom fort at Mungkhrang twice and take it on the second attempt, before the Ahoms win it back.",
  "The Ahom march of 1520 is AHOM-095.", [CK]),
 ("CHUTIA-10", GC, "1523", 1523, "The Chutia Regalia Carried Away", "dhirnarayan", "dhirnarayan", "sadiya", "medium",
  "After the rout at the Dibru fort and the death of the Chutia king, the Ahoms carry off the royal heirlooms: the gold and silver cat (mekuri), the royal umbrella and the bedstead.",
  "The annexation from the Ahom side is AHOM-096. Some later manuscripts name the king Nitipal or Chandranarayan; the early chronicles do not.", [CK]),
 ("CHUTIA-11", GC, "1524 (tradition)", 1524, "Queen Sadhani", "sati-sadhani", "sati-sadhani", "sadiya", "low",
  "Tradition remembers the Chutia queen Sadhani as refusing to submit to the conquerors. The Ahom chronicles mention only a chief Chutia queen, Nang Lung or Bor Konwari, at the fall of Sadiya.",
  "Her name comes from the 19th-century Chutiyar Rajar Vamsavali; the details of her death were not found in the sources checked. Paint as remembered tradition, not a recorded event.", [SS, CK]),
 ("CHUTIA-12", GC, "1524", 1525, "Artisans Taken to the Ahom Capital", "", "", "sadiya", "medium",
  "Brahmans, Kayasthas and artisans are moved from Sadiya to the Ahom capital; one account says some 3,000 blacksmiths were settled at Bosa and Ujoni. Chutia cannons and hand-guns (hiloi) pass to the Ahoms.",
  "The blacksmith figure is from Maniram Dewan’s much later account.", [CK]),
 ("CHUTIA-13", GC, "1524", 1526, "Sadhaknarayan Sent to Darrang", "sadhaknarayan", "sadhaknarayan", "", "low",
  "Some sources say the Chutia prince Sadhaknarayan was deported to Darrang, where descendants are said to live at Geruwapara.", "", [CK]),
]

def rows():
    out = []
    for (i, g, dl, sy, name, people, main, places, conf, summ, notes, src) in S:
        r = dict.fromkeys(build.COLS, "")
        r.update(type="scene", id=i, name=name, period=PER[g], group=g, date_label=dl, sort_year=str(sy), people=people,
                 main_people=main, places=places, confidence=conf, status="planned", collection=COL[g], summary=summ,
                 notes=notes, sources="; ".join(src))
        out.append(r)
    return out

if __name__ == "__main__":
    new = rows()
    here = Path(__file__).parent
    with open(here / "planned-scenes.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, build.COLS); w.writeheader(); w.writerows(new)
    data = build.read_rows(); have = {(r["type"], r["id"]) for r in data}
    added = [r for r in new if ("scene", r["id"]) not in have]
    data += added
    scenes = build.scene_order([r for r in data if r["type"] == "scene"])
    build.write_rows([r for r in data if r["type"] != "scene"] + scenes)
    print(f"{len(new)} scenes in planned-scenes.csv, {len(added)} added to the CSV")
