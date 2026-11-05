import concurrent.futures, io, json, re, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'images/references/present-day-attire'; NOTES=Path(__file__).parent
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 AssamHistoryReferenceResearch'}),timeout=35) as r: return r.read()
class Images(HTMLParser):
 def __init__(self): super().__init__(); self.rows=[]
 def handle_starttag(self,t,a):
  if t=='img': self.rows.append(dict(a))
SOURCES=[
 ('singpho','https://arunachallivingheritage.com/singpho-textile',r'Singpho_[Tt]extile', 'Costume and textile references; Arunachal locality, compare with Assam.'),
 ('khampti','https://arunachallivingheritage.com/lifestyle-of-khampti',r'Khampti_(Attire|Textile)', 'Khampti attire and textiles; Arunachal comparative reference.'),
 ('barmans-in-cachar','https://www.sahapedia.org/dimasa-costumes',r'(Rigu|Rhijhamphai|Rikhosha|Bathau)', 'Gargee Bhattacharjee costume documentation, tagged Barman/Cachar; verify specific garment use before generation.'),
 ('khelma','https://www.tezu.ernet.in/wmcfel/khelma.php',r'khelma1', 'University fieldwork page heading says Khelma traditional dress, but image alt says Biate traditional dress: identity conflict, review required.'),
 ('rangkhol','https://www.hrangkhol.in/en/traditional-attire-1',r'gallery-Traditional', 'Hrangkhawl community gallery; preserve the individual garment labels.'),
 ('jaintia-pnar','https://www.muezart.com/blogs/muezart-musings/little-known-stories-of-khasi-and-jaintia-traditional-attires',r'(Khyrwang|Thohsaru|Jaintia|khyrwang|thohsaru)', 'Local textile producer documentation; retain Jaintia garment labels, not a generic Khasi substitute.'),
 ('thado','https://en.wikipedia.org/wiki/Thadou_people',r'(dress|Dress|Thadou|Thado)', 'Wikipedia image candidate; check original caption and authorship.'),
 ('mech','https://www.back2roots.life/tribes-2/the-meches-tribe',r'(mech|Mech)', 'Community profile photographs; individual attire and identity require review.'),
]
DIRECT=[
 ('hmar','https://e-pao.net/epGallery.asp?id=9&src=Community_Org%2FHmarDress201903','https://www.e-pao.org/galleries/images/Community/2019/Hmar_0319/Hmar_201903_9.jpg','Hmar women; Lamdamba Oinam, 11 March 2019, Manipur comparative reference.'),
 ('hmar','https://e-pao.net/epGallery.asp?id=1&src=Community_Org%2FHmarDress201903','https://www.e-pao.org/galleries/images/Community/2019/Hmar_0319/Hmar_201903_1.jpg','Hmar women; Lamdamba Oinam, 11 March 2019; compare regional variation.'),
 ('bhoi','https://x.com/deptoftextiles/status/1480176566101430274','https://pbs.twimg.com/media/FIqkvSVVgAIxUCF.jpg','Meghalaya Department of Textiles: Ri-Bhoi youths from Raid Nongtluh, Unden, male and female attire.'),
 ('lyngngam','https://4dancing.ru/blogs/211214/1985/','https://4dancing.ru/files/u5304/5060254382_e818af6c4b_z.jpg','Publisher-labelled Lingngam/Lyngngam dancers; secondary source, locality/identity review required.'),
 ('lyngngam','https://4dancing.ru/blogs/211214/1985/','https://4dancing.ru/files/u5304/53040900.jpg','Publisher-labelled Lingngam/Lyngngam dance; secondary source, identity review required.'),
 ('man-tai-speaking','https://www.taiphakeassam.com/about-namphake','https://www.taiphakeassam.com/about/abt-namphake.jpg','Tai Phake women, Namphake Assam; subgroup-specific, not universal Man Tai-speaking attire.'),
 ('vaiphei','https://x.com/being_chikim/status/1767555405557989481','https://pbs.twimg.com/media/GIeeQ3fbsAAj2wK.jpg','Community-labelled Vaiphei woman; social media attribution, verify before generation.'),
 ('vaiphei','https://x.com/being_chikim/status/1377128063490682890','https://pbs.twimg.com/media/ExyKqLcU4AcMuCz.jpg','Community-labelled Vaiphei group; modern male suit is not traditional male costume evidence.'),
 ('pawi-lai','https://www.indiatodayne.in/visualstories/webstories/mizoram-the-major-tribes-of-mizoram-107378-21-02-2024','https://cf-img-a-in.tosshub.com/sites/visualstory/wp/2024/02/mizo-pawi.jpg?size=%2A%3A900','Publisher-labelled Pawi dance group; Mizoram comparative reference.'),
 ('naga/rengma','https://jkphotosnagaland.blogspot.com/2019/09/naga-tribes-of-nagaland-identify-traditional-attire-dress.html','', 'Rengma subgroup only; do not label a single outfit as all Naga tribes.'),
]
records=[]; errors=[]
def save(group,page,url,note):
 try:
  b=get(url); im=Image.open(io.BytesIO(b)); size=im.size; fmt=im.format; im.verify()
  if min(size)<100: return
  folder=OUT/group; folder.mkdir(parents=True,exist_ok=True)
  import hashlib
  ext={'JPEG':'.jpg','PNG':'.png','WEBP':'.webp','GIF':'.gif'}.get(fmt,'.jpg')
  f=folder/('ref-'+hashlib.sha256(url.encode()).hexdigest()[:10]+ext); f.write_bytes(b)
  records.append(dict(community=group,path=f.relative_to(ROOT).as_posix(),source_page=page,download_url=url,description=note,width=size[0],height=size[1],license='Not established; local reference only',review_status='source-labelled; visual review pending'))
 except Exception as e: errors.append(dict(community=group,url=url,error=str(e)[:160]))
def scrape(source):
 group,page,pattern,note=source
 try:
  p=Images(); p.feed(get(page).decode(errors='replace')); seen=set()
  for row in p.rows:
   u=urllib.parse.urljoin(page,row.get('src',''))
   if not re.search(pattern,u): continue
   u=u.replace('http://www.sahapedia.org','https://www.sahapedia.org')
   if u in seen: continue
   seen.add(u); save(group,page,u,note+' Alt: '+row.get('alt',''))
   if len(seen)>=6: break
 except Exception as e: errors.append(dict(community=group,url=page,error=str(e)[:160]))
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  list(pool.map(scrape,SOURCES))
  list(pool.map(lambda x:save(*x),[x for x in DIRECT if x[2]]))
 (NOTES/'curated-manifest.json').write_text(json.dumps({'images':records,'errors':errors},ensure_ascii=False,indent=2)+'\n')
 print('Downloaded',len(records),'images; errors',len(errors))
 for e in errors: print(e)
