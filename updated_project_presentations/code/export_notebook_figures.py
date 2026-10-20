"""Extract every PNG from saved executed notebook outputs, without refitting.
Usage: python code/export_notebook_figures.py --notebook-dir /path/to/project
"""
import argparse,base64,hashlib,json
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--notebook-dir',required=True,type=Path);args=p.parse_args()
root=Path(__file__).resolve().parents[1]
coverage=json.loads((root/'plot_coverage.json').read_text())
for name in sorted({x['notebook'] for x in coverage}):
 nb=json.loads((args.notebook_dir/name).read_text());task=name.removesuffix('_tutorial.ipynb');extracted=[]
 for i,cell in enumerate(nb['cells']):
  j=0
  for output in cell.get('outputs',[]):
   png=output.get('data',{}).get('image/png')
   if png:
    j+=1;data=base64.b64decode(''.join(png) if isinstance(png,list) else png)
    dest=root/'figures'/'notebook'/task/f'cell_{i:03d}_figure_{j}.png';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    extracted.append({'cell_id':cell['id'],'cell_index':i,'figure_index':j,'figure':dest.relative_to(root).as_posix(),'sha256':hashlib.sha256(data).hexdigest()})
 (root/'evidence'/f'{task}_figure_index.json').write_text(json.dumps(extracted,indent=2))
 print(task,len(extracted),'complete figures')
