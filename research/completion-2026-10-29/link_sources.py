from pathlib import Path
import sys
sys.path.insert(0,'tools');import build
m={}
def add(ids,url):
 for i in ids.split():m.setdefault(i,[]).append(url)
add('BHAKTI-01','https://indiaich-sna.in/sites/default/files/2023-11/report_36.pdf')
add('BHAKTI-02 BHAKTI-03 BHAKTI-04 madhavdev damodardev','https://barpeta.assam.gov.in/about-us-level-two/heritage-%26-culture/culture')
add('BHAKTI-04 madhavdev','https://barpeta.assam.gov.in/tourist-place-detail/218')
add('BHAKTI-05 bhattadev','https://bhattadevuniversity.ac.in/docs/prospectus2024-25.pdf')
add('BHAKTI-06 aniruddhadeva','https://ojs.utlib.ee/index.php/JEF/article/download/18835/13519/21941')
add('ananta-kandali','https://ignca.gov.in/Asi_data/1995.pdf')
add('DIMASA-01 DIMASA-02','https://www.yumpu.com/en/document/view/40925060/download-catalogue-pdf-spink/52')
add('DIMASA-03 DIMASA-04 DIMASA-05','https://repository.tribal.gov.in/bitstream/123456789/73787/1/AIRT_1988_0001_book.pdf')
add('DIMASA-06 DIMASA-07','https://ignca.gov.in/Asi_data/42192.pdf')
add('MANIPUR-01','https://ufdcimages.uflib.ufl.edu/UF/E0/05/39/32/00001/SEBASTIAN_R.pdf')
add('MANIPUR-02 MANIPUR-03','https://tourism.gov.in/sites/default/files/2020-04/Manipur.pdf')
add('JAINTIA-01','https://www.ncert.nic.in/pdf/publication/otherpublications/tinei101.pdf')
add('COL-01','https://www.kkhsou.ac.in/web/teaworld/page-details.php?page=9d34bb5c4a06966fcf6ceb4bf')
add('COL-02','https://atom.aim25.com/index.php/assam-company-tea-producers-and-traders-2')
add('COL-03','https://www.gucdoe.in/sites/default/files/MMC-1025_1.pdf')
add('COL-04 maniram-dewan','https://www.publicationsdivision.nic.in/journals/Journalarchives/Yojana/Yojana-English/2007/December/Yojana_2007_December_659992158.pdf')
add('COL-05','https://www.jetir.org/view?paper=JETIR1905S36')
add('COL-06 COL-07','https://archives.assam.gov.in/sites/default/files/swf_utility_folder/departments/archives_webcomindia_org_oid_3/portlet/level_1/files/general_1874_-_1932.pdf')
add('COL-08','https://serendipityarts.org/writing_initiatives/jonaki-the-birth-of-assamese-nationalism/')
add('COL-09','https://karatoya.nbu.ac.in/doc/Karatoya_2009_Volume_3.pdf')
add('COL-11','https://en.wikisource.org/wiki/Page:Speeches_And_Writings_MKGandhi.djvu/683')
add('COL-12','https://ir.nbu.ac.in/bitstreams/d20cdb44-441b-487a-ab3c-81fe2b037bfd/download')
add('COL-13','https://www.publicationsdivision.nic.in/journals/Journalarchives/Yojana/Yojana-English/1995/August/Yojana_1995_August_1611045932.pdf')
add('COL-14 kanaklata-barua','https://static.pib.gov.in/WriteReadData/userfiles/Unsung%20Heroes%20of%20Freedom%20Movement_o.pdf')
add('COL-15 bhogeswari-phukanani','https://admin.missiongyan.in/admin/ebook/ebook_2541_81763515.pdf')
add('COL-16 kushal-konwar','https://www.culture.gov.in/files/publications_documents/Martyrs_Vol_4_06_03_2019_6.pdf')
add('COL-17','https://nehruarchive.in/documents/to-gopinath-bardoloi-23-september-1946-2ve13k')
add('COL-18','https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/making-and-unmaking-of-assambengal-borders-and-the-sylhet-referendum/A75509398FB7B75CF274CA11A399B581')
add('MOD-01','https://www.asdma.gov.in/download/literature_survey.pdf')
add('MOD-02','https://legislative.assam.gov.in/documents-detail/the-assam-official-language-act-1960')
add('MOD-03','https://www.claudearpi.net/wp-content/uploads/2016/12/WhitePaper8NEW.pdf')
add('MOD-04','https://www.presidentofindia.gov.in/fakhruddin-ali-ahmed-profile')
add('MOD-05 MOD-06','https://assamaccord.assam.gov.in/sites/default/files/swf_utility_folder/departments/assamaccord_medhassu_in_oid_3/portlet/level_1/files/The%20Assam%20Accord%20-%20English.pdf')
add('MOD-07','https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=77048')
rows=build.read_rows()
for r in rows:
 for u in m.get(r['id'],[]):
  if u not in r['sources']:r['sources']+='; '+u
 if r['id']=='DIMASA-04':
  r['notes']+=' Chronology and ruler identification differ between narrative and numismatic accounts; image is a thematic reconstruction of the Dimasa–Jaintia conflict, not evidence of a precise dated deployment or costume.'
build.write_rows(rows)
print('Linked research sources to',len(m),'records')
