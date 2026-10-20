"""Export presentation model comparisons from measured results JSON files.
No chart values are entered in PowerPoint. Run from the bundle with:
  python code/render_comparisons.py
"""
import json,hashlib,csv,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/presentation_matplotlib')
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
TASKS=['ml_models','wine_quality','sailing_boats','crypto_microstructure','pjm_energy','open_power_systems','give_me_some_credit','home_credit','amex_default']
LABEL={'LinearRegression':'OLS','LogisticRegression':'Logistic','RandomForest':'Random Forest','LR':'OLS','ElasticNet':'Elastic Net','LogReg (L2)':'L2 logistic','LogReg (L1)':'L1 logistic','LogReg (ElasticNet)':'Elastic Net logistic','RandomForest (tuned)':'Forest (tuned)'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':15,'axes.titlesize':17,'axes.labelsize':15,'xtick.labelsize':14,'ytick.labelsize':16,'axes.spines.top':False,'axes.spines.right':False})
rows=json.loads((ROOT/'slide_image_map.json').read_text())
for task in TASKS:
 data=json.loads((ROOT/'evidence'/f'{task}_results.json').read_text())['results'];reg='RMSE' in next(iter(data.values()))
 primary='RMSE' if reg else 'ROC_AUC'
 keys=[]
 for base in ['LinearRegression','Ridge','Lasso','ElasticNet','LogisticRegression','LogReg (L2)','LogReg (L1)','LogReg (ElasticNet)','KNN','MLP','RandomForest','XGBoost','CatBoost','LightGBM','Stacking','ARIMA','SARIMA']:
  options=[k for k in [base,base+' (tuned)'] if k in data]
  if options:keys.append(min(options,key=lambda k:data[k][primary]) if reg else max(options,key=lambda k:data[k][primary]))
 penalties=[k for k in keys if k in ['Ridge','Lasso','ElasticNet','LogReg (L2)','LogReg (L1)','LogReg (ElasticNet)']]
 if penalties:
  best_penalty=min(penalties,key=lambda k:data[k][primary]) if reg else max(penalties,key=lambda k:data[k][primary])
  keys=[k for k in keys if k not in penalties or k==best_penalty]
 primary='RMSE' if reg else 'ROC_AUC';keys.sort(key=lambda k:data[k][primary],reverse=not reg)
 metrics=['RMSE','MAE'] if reg else ['ROC_AUC','LogLoss'];titles=['RMSE (lower is better)','MAE (lower is better)'] if reg else ['ROC-AUC (higher is better)','Log loss (lower is better)']
 fig,axes=plt.subplots(1,2,figsize=(14,5.5),layout='constrained')
 for ax,m,title in zip(axes,metrics,titles):
  vals=[data[k][m] for k in keys];colors=['#007C78' if i==0 else '#A8BCC4' for i in range(len(keys))]
  ax.barh([LABEL.get(k,k) for k in keys],vals,color=colors,height=.62);ax.invert_yaxis();ax.set_title(title,pad=16);ax.set_axisbelow(True);ax.grid(axis='x',alpha=.2);ax.spines['left'].set_visible(False);ax.spines['bottom'].set_color('#CFDADC');ax.tick_params(axis='y',length=0)
  if not reg and m=='ROC_AUC':ax.set_xlim(0,1)
  for i,v in enumerate(vals):ax.text(v+max(vals)*.015,i,f'{v:.6f}' if abs(v)<.01 else f'{v:.4f}' if v<10 else f'{v:,.1f}',va='center',fontsize=13,color='#183C4A')
  ax.set_xlim(0,max(vals)*1.23 if reg or m=='LogLoss' else 1.10)
 dest=ROOT/'figures'/task/'comparison.png';fig.savefig(dest,dpi=180,bbox_inches='tight',facecolor='white');plt.close(fig)
 for row in rows:
  if row['task']==task and row['figure'].endswith('/comparison.png'):
   row['image_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();row.setdefault('embedded_image_sha256',row['image_sha256']);row['generator']='code/render_comparisons.py';row['data_source']=f'evidence/{task}_results.json'
(ROOT/'slide_image_map.json').write_text(json.dumps(rows,indent=2))
with (ROOT/'slide_image_map.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
print('Exported nine comparison PNGs from measured results.')
