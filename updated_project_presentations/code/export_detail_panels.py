"""Export enlarged notebook plot panels without fitting models.
Regression panels replay only plot cells using the saved predictions.
Classification panels crop the executed notebook confusion-matrix image.
"""
import argparse,json,os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/presentation_matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np,pandas as pd
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--notebook-dir',type=Path,required=True);args=p.parse_args()
ROOT=Path(__file__).resolve().parents[1];metadata=[]
for task,ids in [('wine_quality',['2d26e3e2','7d76e260']),('sailing_boats',['dca36775'])]:
 nb=json.loads((args.notebook_dir/(task+'_tutorial.ipynb')).read_text())
 cells={c['id']:(i,c) for i,c in enumerate(nb['cells'])}
 r=json.loads((ROOT/'evidence'/(task+'_results.json')).read_text())
 g={'np':np,'pd':pd,'plt':plt,'y_test':pd.Series(r['predictions']['actual'])}
 g.update({k:np.asarray(v) for k,v in r['predictions'].items() if k!='actual'})
 for cid in ids:
  plt.close('all');exec(''.join(cells[cid][1]['source']),g)
 fig=g['fig']
 for ax in fig.axes:
  if task=='wine_quality':
   ax.set_xlabel('Actual quality');ax.set_ylabel('Predicted quality');ax.tick_params(labelbottom=True,labelleft=True)
 fig.canvas.draw()
 for i,model in enumerate(g['preds']):
  bbox=fig.axes[i].get_tightbbox(fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted()).expanded(1.07,1.08)
  dest=ROOT/'figures'/'panels'/task/f'regression_{i+1:02d}.png';dest.parent.mkdir(parents=True,exist_ok=True)
  fig.savefig(dest,dpi=300,bbox_inches=bbox)
  metadata.append({'task':task,'cell_index':cells[ids[-1]][0],'cell_id':ids[-1],'axis_index':i,'model':model,'kind':'regression','figure':dest.relative_to(ROOT).as_posix()})
 plt.close('all')
task='wine_quality';nb=json.loads((args.notebook_dir/(task+'_tutorial.ipynb')).read_text());cell=next(i for i,c in enumerate(nb['cells']) if c['id']=='57faadd1')
src=ROOT/'figures'/'notebook'/task/f'cell_{cell:03d}_figure_1.png';im=Image.open(src);w,h=im.size
models=['LogisticRegression','LogisticLasso','LogisticElasticNet','KNN','MLP','RandomForest','XGBoost','CatBoost','LightGBM']
for i,model in enumerate(models):
 row,col=divmod(i,3);bounds=(round(col*w/3),round(row*h/3),round((col+1)*w/3),round((row+1)*h/3))
 dest=ROOT/'figures'/'panels'/task/f'classification_{i+1:02d}.png';im.crop(bounds).save(dest)
 metadata.append({'task':task,'cell_index':cell,'cell_id':'57faadd1','axis_index':i,'model':model,'kind':'classification','figure':dest.relative_to(ROOT).as_posix(),'source_figure':src.relative_to(ROOT).as_posix(),'crop_pixels':bounds})
(ROOT/'figures'/'wine_quality'/'class_confusion.png').write_bytes((ROOT/'figures'/'panels'/'wine_quality'/'classification_07.png').read_bytes())
(ROOT/'evidence'/'detail_panels.json').write_text(json.dumps(metadata,indent=2));print('Exported',len(metadata),'panels.')
