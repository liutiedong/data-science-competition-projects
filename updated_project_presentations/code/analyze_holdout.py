"""Generate supplementary analysis directly from saved test predictions.
Run from the presentation bundle: python code/analyze_holdout.py
No model is refitted. Bootstrap intervals condition on the fitted models.
"""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/presentation_matplotlib')
import json,ast
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,precision_recall_curve
from sklearn.calibration import calibration_curve
ROOT=Path(__file__).resolve().parents[1]
TASKS=['ml_models','wine_quality','sailing_boats','crypto_microstructure','pjm_energy','open_power_systems','give_me_some_credit','home_credit','amex_default']
SUFFIX={'LinearRegression':'lr','Ridge':'ridge','Lasso':'lasso','ElasticNet':'elastic','LogisticRegression':'lr','LogReg (L2)':'l2','LogReg (L1)':'l1','LogReg (ElasticNet)':'elastic','KNN':'knn','MLP':'mlp','RandomForest':'rf','XGBoost':'xgb','CatBoost':'cat','LightGBM':'lgbm','ARIMA':'arima','SARIMA':'sarima','Stacking':'stack'}
def prediction_key(model):
 return SUFFIX[model.replace(' (tuned)','')]+('_tuned' if model.endswith(' (tuned)') else '')
def choose_models(results):
 reg='RMSE' in next(iter(results.values()));metric='RMSE' if reg else 'ROC_AUC'
 ranked=sorted(((n,v) for n,v in results.items() if n not in ['LR','RF']),key=lambda x:x[1][metric],reverse=not reg)
 winner=ranked[0][0];runner=next(n for n,v in ranked[1:] if n.replace(' (tuned)','')!=winner.replace(' (tuned)',''))
 return winner,prediction_key(winner),runner,prediction_key(runner)

UNITS={'ml_models':'$100,000','wine_quality':'quality points','sailing_boats':'ln(1 + kg)','crypto_microstructure':'ln(1 + absolute return)','pjm_energy':'MW','open_power_systems':'GWh/day'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'axes.titlesize':15,'axes.labelsize':13,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
TEAL='#007C78';BLUE='#607C8B';ORANGE='#BA6044';INK='#183C4A'
def blocks(rng,ids,L):
 ids=np.asarray(ids);length=len(ids);k=int(np.ceil(length/L));starts=rng.integers(0,length,k)
 return ids[((starts[:,None]+np.arange(L))%length).ravel()[:length]]
summary={}
for name in TASKS:
 r=json.loads((ROOT/'evidence'/f'{name}_results.json').read_text());pr=r['predictions'];y=np.asarray(pr['actual']);reg='y_pred_lr' in pr;prefix='y_pred_' if reg else 'y_proba_';wn,wk,rn,rk=choose_models(r['results']);best=np.asarray(pr[prefix+wk]);runner=np.asarray(pr[prefix+rk]);ref=np.asarray(pr[prefix+'lr']);refname='OLS' if reg else 'Reference logistic';n=len(y);dest=ROOT/'figures'/name;dest.mkdir(exist_ok=True)
 rng=np.random.default_rng(42019);mode='paired row bootstrap' if reg else 'paired stratified row bootstrap';L=None
 if name=='pjm_energy':L=168;mode='paired circular block bootstrap, 168 hours'
 if name=='open_power_systems':L=7;mode='paired circular block bootstrap, 7 days'
 if name=='crypto_microstructure':L=60;mode='paired circular blocks within each asset–venue series, 60 observations'
 def delta(a,b,idx):
  return float(np.sqrt(np.mean((a[idx]-y[idx])**2))-np.sqrt(np.mean((b[idx]-y[idx])**2))) if reg else float(roc_auc_score(y[idx],b[idx])-roc_auc_score(y[idx],a[idx]))
 bs=[[],[]];allidx=np.arange(n)
 for b in range(1000):
  if name=='crypto_microstructure':idx=np.concatenate([blocks(rng,ids,L) for ids in r['test_groups'].values()])
  elif L:idx=blocks(rng,allidx,L)
  elif reg:idx=rng.integers(0,n,n)
  else:idx=np.concatenate([rng.choice(np.flatnonzero(y==v),np.sum(y==v),replace=True) for v in [0,1]])
  for j,other in enumerate([runner,ref]):bs[j].append(delta(other,best,idx))
 comparisons=[]
 for other,aname,bb in zip([runner,ref],[rn,refname],bs):
  point=delta(other,best,allidx);lo,hi=np.quantile(bb,[.025,.975]);comparisons.append({'comparison':wn+' versus '+aname,'other':aname,'advantage':point,'ci_low':float(lo),'ci_high':float(hi)})
 fig,ax=plt.subplots(figsize=(12,4));
 for i,c in enumerate(comparisons):ax.errorbar(c['advantage'],i,xerr=[[c['advantage']-c['ci_low']],[c['ci_high']-c['advantage']]],fmt='o',color=TEAL if i==0 else BLUE,markersize=10,capsize=7,linewidth=3)
 ax.axvline(0,color=ORANGE,ls='--',lw=1.5);ax.set_yticks([0,1],['vs '+rn,'vs '+refname]);ax.invert_yaxis();ax.set_ylim(1.6,-.6);ax.set_xlabel(('RMSE reduction ('+UNITS[name]+')') if reg else 'ROC-AUC increase');ax.set_title(wn+': paired difference and 95% bootstrap interval');ax.grid(axis='x',alpha=.2);fig.tight_layout();fig.savefig(dest/'ranking_stability.png',dpi=180,bbox_inches='tight');plt.close(fig)
 out={'winner':wn,'runner_up':rn,'n_test':n,'resampling':mode,'n_resamples':1000,'comparisons':comparisons,'interval_scope':'Conditional on fitted models and this test population. Training and model selection are not repeated.'}
 if reg:
  resid=best-y;fig,axs=plt.subplots(1,2,figsize=(13,4.8),layout='constrained');select=np.arange(n) if n<=12000 else np.random.default_rng(42).choice(n,12000,replace=False)
  axs[0].scatter(y[select],best[select],s=10,alpha=.22,color=TEAL,rasterized=True);lo=min(y.min(),best.min());hi=max(y.max(),best.max());axs[0].plot([lo,hi],[lo,hi],color=ORANGE,ls='--');axs[0].set(xlabel='Actual ('+UNITS[name]+')',ylabel='Predicted',title=wn+': prediction accuracy')
  axs[1].scatter(y[select],resid[select],s=10,alpha=.22,color=BLUE,rasterized=True);axs[1].axhline(0,color=ORANGE,ls='--');axs[1].set(xlabel='Actual ('+UNITS[name]+')',ylabel='Prediction minus actual',title='Residual structure')
  fig.savefig(dest/'winner_diagnostics.png',dpi=180,bbox_inches='tight');plt.close(fig)
  bands=pd.qcut(y,4,duplicates='drop');slices=[]
  for band in bands.categories:
   ix=np.asarray(bands==band);slices.append({'group':str(band),'n':int(ix.sum()),'rmse':float(np.sqrt(np.mean(resid[ix]**2))),'mae':float(np.mean(abs(resid[ix]))),'bias':float(np.mean(resid[ix]))})
  out['error_slices']=slices;out['rmse']=float(np.sqrt(np.mean(resid**2)));out['mae']=float(np.mean(abs(resid)))
  if name=='ml_models':
   mask=y>=5.0;out['capped_targets']={'n':int(mask.sum()),'mae_usd':float(np.mean(abs(resid[mask]))*1e5),'bias_usd':float(np.mean(resid[mask])*1e5)}
  if name=='sailing_boats':
   kg=np.expm1(y);pk=np.expm1(best);ape=abs(pk-kg)/kg;out['physical_errors']={'mae_kg':float(np.mean(abs(pk-kg))),'median_ape':float(np.median(ape)),'p90_ape':float(np.quantile(ape,.9))}
   fig,axs=plt.subplots(1,2,figsize=(13,4.8),layout='constrained');axs[0].scatter(kg,pk,s=10,alpha=.3,color=TEAL);axs[0].set_xscale('log');axs[0].set_yscale('log');axs[0].plot([kg.min(),kg.max()],[kg.min(),kg.max()],color=ORANGE,ls='--');axs[0].set(xlabel='Actual displacement (kg)',ylabel='Predicted displacement (kg)',title='Accuracy in physical units')
   axs[1].hist(np.minimum(ape,2),bins=40,color=TEAL);axs[1].set(xlabel='Absolute percentage error (clipped at 200%)',ylabel='Test boats',title='Relative error across vessel sizes');fig.savefig(dest/'physical_errors.png',dpi=180,bbox_inches='tight');plt.close(fig)
  if name in ['pjm_energy','open_power_systems']:
   sp=json.loads((ROOT/'evidence'/f'{name}_supplement.json').read_text());dates=pd.date_range(sp['X_test_dates'][0],periods=n,freq='h' if name=='pjm_energy' else 'D');col=dates.hour if name=='pjm_energy' else dates.dayofweek;levels=sorted(set(col));err=[float(np.sqrt(np.mean(resid[col==v]**2))) for v in levels]
   out['calendar_error']=[{'period':int(v),'rmse':z} for v,z in zip(levels,err)]
   fig,axs=plt.subplots(1,2,figsize=(13,4.8),layout='constrained');axs[0].plot(levels,err,marker='o',color=TEAL);axs[0].set(xlabel='Hour of day' if name=='pjm_energy' else 'Weekday (0 = Monday)',ylabel='RMSE ('+UNITS[name]+')',title='Calendar error profile')
   months=sorted(set(dates.month));me=[np.sqrt(np.mean(resid[dates.month==m]**2)) for m in months];axs[1].bar(months,me,color=BLUE);axs[1].set(xlabel='Month',ylabel='RMSE ('+UNITS[name]+')',title='Seasonal error profile');fig.savefig(dest/'calendar_errors.png',dpi=180,bbox_inches='tight');plt.close(fig)
  if name=='crypto_microstructure':
   vals=[]
   for group,ii in r['test_groups'].items():
    ii=np.asarray(ii);symbol,venue=ast.literal_eval(group);vals.append({'series':symbol+' / '+venue,'rmse':float(np.sqrt(np.mean(resid[ii]**2))),'mae':float(np.mean(abs(resid[ii]))),'n':len(ii)})
   out['series_errors']=vals
   fig,ax=plt.subplots(figsize=(12,4.7));ax.barh([v['series'] for v in vals],[v['rmse'] for v in vals],color=TEAL);ax.invert_yaxis();ax.set(xlabel='RMSE (ln(1 + absolute return))',title='Performance differs across asset–venue series');fig.tight_layout();fig.savefig(dest/'series_errors.png',dpi=180,bbox_inches='tight');plt.close(fig)
 else:
  ap=float(average_precision_score(y,best));prev=float(y.mean());brier=float(brier_score_loss(y,best));precision,recall,_=precision_recall_curve(y,best);obs,prob=calibration_curve(y,best,n_bins=10,strategy='quantile')
  fig,axs=plt.subplots(1,2,figsize=(13,4.8),layout='constrained');axs[0].plot(recall,precision,color=TEAL,lw=2,label=f'Average precision {ap:.3f}');axs[0].axhline(prev,color=ORANGE,ls='--',label=f'Prevalence {prev:.3f}');axs[0].set(xlabel='Recall',ylabel='Precision',xlim=(0,1),ylim=(0,1),title=wn+': precision–recall');axs[0].legend(fontsize=11)
  axs[1].plot([0,1],[0,1],color=ORANGE,ls='--');axs[1].plot(prob,obs,marker='o',color=TEAL);axs[1].set(xlabel='Mean predicted risk',ylabel='Observed positive rate',title='Calibration by risk decile',xlim=(0,1),ylim=(0,1));fig.savefig(dest/'pr_calibration.png',dpi=180,bbox_inches='tight');plt.close(fig)
  order=np.argsort(-best,kind='stable');cy=np.cumsum(y[order]);share=np.arange(1,n+1)/n;gain=cy/y.sum();capacity=[]
  for frac in [.01,.05,.10,.20]:
   k=int(np.ceil(frac*n));hits=int(cy[k-1]);precisionk=hits/k;recallk=hits/int(y.sum());capacity.append({'review_share':k/n,'n_reviewed':k,'positives':hits,'precision':precisionk,'recall':recallk,'lift':precisionk/prev})
  fig,ax=plt.subplots(figsize=(12,4.5));ax.plot(share,gain,color=TEAL,lw=2.5,label=wn);ax.plot([0,1],[0,1],color=ORANGE,ls='--',label='Random ranking');ax.set(xlabel='Share of applicants reviewed (highest scores first)',ylabel='Share of positive cases captured',xlim=(0,1),ylim=(0,1),title='Risk ranking under a review-capacity constraint');ax.legend();ax.grid(alpha=.15);fig.tight_layout();fig.savefig(dest/'review_capacity.png',dpi=180,bbox_inches='tight');plt.close(fig)
  out.update({'average_precision':ap,'prevalence':prev,'brier_score':brier,'review_capacity':capacity,'calibration_deciles':{'predicted':prob.tolist(),'observed':obs.tolist()}})
 summary[name]=out
 (ROOT/'evidence'/f'{name}_additional_analysis.json').write_text(json.dumps(out,indent=2));print(name,'runner interval',comparisons[0],flush=True)
(ROOT/'evidence'/'additional_analysis_summary.json').write_text(json.dumps(summary,indent=2))


