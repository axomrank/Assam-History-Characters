import concurrent.futures, html, json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'images/references/present-day-attire'
NOTES = Path(__file__).parent
QUERIES = {
 'mech': 'Mech people traditional dress', 'hajong': 'Hajong traditional dress',
 'barmans-in-cachar': 'Dimasa Cachar traditional costume', 'hojai-kachari': 'Hojai Kachari dress',
 'thengal-kachari': 'Thengal Kachari traditional', 'singpho': 'Singpho traditional dress',
 'khampti': 'Khampti traditional dress', 'garo': 'Garo traditional dress',
 'hmar': 'Hmar', 'kuki': 'Kuki traditional dress',
 'vaiphei': 'Vaiphei traditional', 'thado': 'Thadou',
 'rangkhol': 'Rangkhawl traditional', 'naga': 'Rengma traditional',
 'khasi': 'Khasi traditional dress', 'jaintia-pnar': 'Pnar traditional dress',
 'synteng': 'Synteng dress', 'war': 'War Khasi traditional dress',
 'bhoi': 'Bhoi traditional dress', 'lyngngam': 'Lyngngam traditional',
 'mizo': 'Mizo traditional dress', 'chakma': 'Chakma traditional dress',
 'khelma': 'Sakachep traditional dress', 'lakher-mara': 'Mara people',
 'pawi-lai': 'Lai traditional', 'man-tai-speaking': 'Tai Phake',
}
HEADERS = {'User-Agent': 'AssamHistoryAttireReferenceResearch/1.0 (local educational reference collection)'}
def get(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=45) as r: return r.read()
  except Exception:
   if attempt == 2: raise
   time.sleep(2+attempt)
def clean(s): return html.unescape(re.sub('<[^>]+>', '', s or ''))
def collect(pair):
 community, query = pair
 params = dict(action='query',format='json',generator='search',gsrsearch=query+' -filetype:pdf -filetype:djvu',gsrnamespace=6,gsrlimit=12,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=1600)
 result = {'community':community,'query':query,'images':[],'errors':[]}
 folder=OUT/community; folder.mkdir(parents=True,exist_ok=True)
 try:
  data=json.loads(get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)))
  pages=sorted(data.get('query',{}).get('pages',{}).values(),key=lambda p:p.get('index',99))
  for page in pages:
   if re.search(r'\.(pdf|djvu|svg|tif|tiff)$',page['title'],re.I): continue
   if re.search(r'alphabet|transliteration|flag|logo|map|statue|2nd century',page['title'],re.I): continue
   info=page.get('imageinfo',[{}])[0]; url=info.get('thumburl', info.get('url',''))
   if not re.search(r'\.(jpg|jpeg|png|webp)(?:$|\?)',url,re.I): continue
   meta=info.get('extmetadata',{}); desc=clean(meta.get('ImageDescription',{}).get('value',''))
   record={'community':community,'title':page['title'],'description':desc,'source_page':info.get('descriptionurl'),'original_url':info.get('url'),'download_url':url,'artist':clean(meta.get('Artist',{}).get('value','')),'license':clean(meta.get('LicenseShortName',{}).get('value','')),'license_url':meta.get('LicenseUrl',{}).get('value',''),'review_status':'candidate-needs-visual-and-community-review','geographic_scope':'Verify source locality; may be comparative reference outside Assam'}
   if community=='barmans-in-cachar': record['identity_note']='Dimasa/Cachar search candidate; must verify specifically Barmans in Cachar, not assume all Dimasa images qualify.'
   if community=='man-tai-speaking': record['identity_note']='Tai Phake comparative candidate; umbrella Man (Tai-speaking) must not be reduced to a single asserted costume.'
   ext='.jpg' if '.jpg' in url.lower() or '.jpeg' in url.lower() else '.png' if '.png' in url.lower() else '.webp'
   path=folder/('%02d-'%(len(result['images'])+1)+str(page['pageid'])+ext)
   try:
    content=get(url)
    from PIL import Image
    import io
    im=Image.open(io.BytesIO(content)); im.verify()
    path.write_bytes(content); record['path']=path.relative_to(ROOT).as_posix()
    result['images'].append(record)
   except Exception as e: result['errors'].append(str(e)[:180])
   if len(result['images'])>=2: break
 except Exception as e: result['errors'].append(str(e)[:180])
 print(community,len(result['images']),flush=True)
 return result
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(collect,QUERIES.items()))
 (NOTES/'commons-manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print('TOTAL',sum(len(r['images']) for r in results),flush=True)
