"""Replace the notebook PNGs in copies of the PPTX files, preserving their layout.
Run after export_notebook_figures.py:
  python code/replace_pptx_figures.py --output-dir updated_powerpoints
"""
import argparse, collections, hashlib, json, zipfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
bundle=Path(__file__).resolve().parents[1];dest=a.output_dir.resolve();dest.mkdir(parents=True,exist_ok=True)
groups=collections.defaultdict(list)
for m in json.loads((bundle/'slide_image_map.json').read_text()):groups[m['deck']].append(m)
for deck,rows in groups.items():
 source=bundle/'powerpoints'/deck;target=dest/deck
 if target==source.resolve():raise SystemExit('Choose a new output directory to preserve the supplied decks.')
 replacements={}
 for m in rows:
  old=m.get('embedded_image_sha256',m['image_sha256']);data=(bundle/m['figure']).read_bytes()
  if old in replacements and replacements[old]!=data:raise SystemExit('A shared original image now has different replacements. Use PowerPoint Change Picture for the affected slides: '+deck)
  replacements[old]=data
 found=set()
 with zipfile.ZipFile(source) as zin:
  contents=[]
  for item in zin.infolist():
   b=zin.read(item.filename)
   if item.filename.startswith('ppt/media/'):
    sha=hashlib.sha256(b).hexdigest()
    if sha in replacements:b=replacements[sha];found.add(sha)
   contents.append((item,b))
  if found!=set(replacements):raise SystemExit(f'{deck}: could not match all embedded plot images. No output written.')
  if target.exists():raise SystemExit(f'Output already exists: {target}')
  with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as zout:
   for item,b in contents:zout.writestr(item,b)
 print(deck,': replaced',len(found),'plot images')
