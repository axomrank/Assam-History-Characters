"""Apply the user-requested Chihna Yatra replacement after visual review."""
from pathlib import Path
import sys,shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import build
from add_sheets import make_webp
source=Path(sys.argv[1]);here=Path(__file__).resolve().parent
out='media/scenes/bhakti/1468-1700/BHAKTI-01.webp'
master=ROOT/'masters/scenes/culture/BHAKTI-01.png'
archive=ROOT/'drafts/completion-2026-10-31/chihna-yatra-evening';archive.mkdir(parents=True,exist_ok=True)
for path in [master,ROOT/out,ROOT/build.thumb_of(out)]:
 dest=archive/(('thumb-' if path.parent.name=='thumb' else '')+path.name)
 if dest.exists():raise SystemExit('Archive exists; inspect before applying replacement')
 if path.exists():shutil.copy2(path,dest)
old_prompt=here/'prompts/BHAKTI-01.txt';backup=here/'prompts/BHAKTI-01-evening-v1.txt'
if not backup.exists():shutil.copy2(old_prompt,backup)
shutil.copy2(source,master);make_webp(master,out)
shutil.copy2(here/'prompts/BHAKTI-01-daylight-v2.txt',old_prompt)
rows=build.read_rows();row=next(x for x in rows if x['id']=='BHAKTI-01')
row['notes']+=' Revised 2026-10-31: user-directed daylight village-road mobile narrative-cloth display, using the project Sankardev sheet and Vrindavani Vastra textile as visual references. The LACMA textile is dated circa 1570 and is not evidence of the actual earlier Chihna Yatra prop; processional staging is interpretive. See research/completion-2026-10-29/chihna-yatra-daylight-revision.md.'
u='https://collections.lacma.org/object/69745'
if u not in row['sources']:row['sources']+='; '+u
build.write_rows(rows)
qpath=here/'queue.json';q=json.loads(qpath.read_text())
for item in q:
 if item['id']=='BHAKTI-01':item.update(qa='visually inspected, daylight textile procession revision 2026-10-31',revision='daylight-v2')
qpath.write_text(json.dumps(q,indent=2))
(here/'BHAKTI-01-daylight-result.json').write_text(json.dumps({'source':str(source),'master':str(master.relative_to(ROOT)),'published':out,'sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'tool':'built-in image_gen','reviewed':'2026-10-31'},indent=2))
with (here/'chihna-yatra-daylight-revision.md').open('a') as f:f.write('\n## Successful retry — 31 October 2026\n\nGenerated with the built-in image_gen tool using all four references. Visually reviewed for Sankardev identity, daylight village-road composition, portable woven-cloth display, clothing and anatomy. Published as the replacement BHAKTI-01 WebP and thumbnail, with PNG master retained. Previous evening images preserved under drafts/completion-2026-10-31/chihna-yatra-evening/. Exact prompt is also copied to the gallery’s canonical BHAKTI-01.txt link.\n')
print(out)
