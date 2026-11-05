#!/usr/bin/env python3
"""Import a visually inspected completion asset; preserve PNG and research records."""
import argparse,json,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import build
from add_sheets import make_webp
ap=argparse.ArgumentParser();ap.add_argument('--id',required=True);ap.add_argument('--source',required=True);ap.add_argument('--prompt',default='');a=ap.parse_args()
rows=build.read_rows();r=next(x for x in rows if x['id']==a.id)
here=Path(__file__).resolve().parent
if r['type']=='person':
 out=f"media/characters/{a.id}/turnaround-1.webp";master=ROOT/f"masters/sheets/{a.id}/turnaround-1.png"
 if r['character_sheets']:raise SystemExit('Already illustrated; refusing replacement')
else:
 dirs={'culture':'bhakti/1468-1700','neighbours':'neighbours/1520-1835','colonial':'colonial/1823-1947','modern':'modern/1947-2011'}
 out=f"media/scenes/{dirs[r['period']]}/{a.id}.webp";master=ROOT/f"masters/scenes/{r['period']}/{a.id}.png"
 if r['scene_image']:raise SystemExit('Already illustrated; refusing replacement')
if (ROOT/out).exists() or master.exists():raise SystemExit('Asset path occupied; refusing overwrite')
master.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a.source,master);make_webp(master,out)
if r['type']=='person':r['character_sheets']=out+' | '+r['name']+', eight-view character sheet, artistic reconstruction, see research/completion-2026-10-29'
else:r['scene_image']=out;r['status']='illustrated'
flag='Generated artistic reconstruction, 2026-10-29; reference roles, historical uncertainties and prompt recorded in research/completion-2026-10-29.'
r['notes']=(r['notes']+' '+flag).strip()
build.write_rows(rows)
if a.prompt:
 (here/'prompts').mkdir(exist_ok=True);(here/'prompts'/f'{a.id}.txt').write_text(a.prompt)
queue=here/'queue.json';items=json.loads(queue.read_text())
for x in items:
 if x['id']==a.id:x.update(state='complete',image=out,master=str(master.relative_to(ROOT)),qa='visually inspected')
queue.write_text(json.dumps(items,indent=2));print(out)
