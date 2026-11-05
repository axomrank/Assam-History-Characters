from pathlib import Path
import sys,json,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'));import build
here=Path(__file__).resolve().parent
queue=json.loads((here/'queue.json').read_text());rows=build.read_rows();byid={r['id']:r for r in rows}
errors=[];cards=[]
for x in queue:
 if x.get('state')!='complete':errors.append(x['id']+': incomplete');continue
 p=ROOT/x['image'];thumb=p.parent/'thumb'/p.name;master=ROOT/x['master']
 for f in [p,thumb,master]:
  if not f.is_file():errors.append(str(f)+': missing');continue
  with Image.open(f) as im:im.verify()
 r=byid[x['id']]
 if x['type']=='person' and x['image'] not in r['character_sheets']:errors.append(x['id']+': CSV sheet link missing')
 if x['type']=='scene' and x['image']!=r['scene_image']:errors.append(x['id']+': CSV scene mismatch')
 if not (here/'prompts'/f"{x['id']}.txt").exists():errors.append(x['id']+': prompt missing')
 cards.append('<article><a href="../../'+html.escape(x['image'])+'"><img loading="lazy" src="../../'+html.escape(str(thumb.relative_to(ROOT)))+'" alt="'+html.escape(x['name'])+'"></a><div><small>'+html.escape(x['id'])+'</small><h2>'+html.escape(x['name'])+'</h2><a href="prompts/'+x['id']+'.txt">Prompt</a> · <a href="../../'+html.escape(x['master'])+'">PNG master</a></div></article>')
missing_people=[r['id'] for r in rows if r['type']=='person' and not r['character_sheets']]
missing_scenes=[r['id'] for r in rows if r['type']=='scene' and not r['scene_image']]
report={'requested':len(queue),'completed':sum(x.get('state')=='complete' for x in queue),'new_sheets':sum(x['type']=='person' for x in queue),'new_scenes':sum(x['type']=='scene' for x in queue),'catalogue_people':len([r for r in rows if r['type']=='person']),'catalogue_scenes':len([r for r in rows if r['type']=='scene']),'missing_people':missing_people,'missing_scenes':missing_scenes,'errors':errors}
(here/'validation.json').write_text(json.dumps(report,indent=2))
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Assam History — completed illustrations</title><style>body{margin:0;background:#111813;color:#ece8da;font:17px/1.6 system-ui}main{max-width:1440px;margin:auto;padding:36px}h1{font:48px Georgia;margin:10px 0}p{max-width:850px;color:#c4c7bb}a{color:#d2b574}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;margin-top:36px}article{background:#202a23;border:1px solid #3c473d}img{display:block;width:100%;aspect-ratio:16/10;object-fit:contain;background:#101510}article div{padding:18px}h2{font:24px Georgia;margin:5px 0 16px}small{color:#c6bc98}</style><main><small>29 OCTOBER 2026 · LOCAL REVIEW GALLERY</small><h1>Assam History illustrations</h1><p>21 new character sheets and 42 new scenes. Generated artistic reconstructions using researched local and internet references. Faces, clothing and settings are interpretive where evidence is limited. Open a thumbnail for the full WebP image.</p><a href="research-notes.md">Research and uncertainty notes</a> · <a href="validation.json">Validation results</a><section>'''+''.join(cards)+'</section></main></html>'
(here/'review-gallery.html').write_text(page)
print(json.dumps(report,indent=2))
if errors or missing_people or missing_scenes:sys.exit(1)
