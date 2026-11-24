"""Regenerate plots only from persisted independent test manifests."""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve,auc,confusion_matrix
from draft_model import LolDraftPredictionSystem,load_pivoted_draft_data,POSITIONS
from snowball_model import LolSnowballPredictionSystem,load_integrated_10min_dataset
from validation import fingerprint,metrics,calibrate,calibration_bins

ROOT=Path(__file__).resolve().parents[2]
FIGURES_DIR=ROOT/'reports/figures'


def verified_test(system,df,target):
    report=system.evaluation
    if fingerprint(df)!=report['data_fingerprint']:raise ValueError('Dataset changed: retrain before evaluating; test must not be reconstructed from current row counts')
    test=df[df.gameid.astype(str).isin(report['partitions']['test']['gameids'])].copy()
    if len(test)!=report['partitions']['test']['rows']:raise ValueError('Test manifest mismatch')
    prob=calibrate(system.best_model.predict_proba(system.fe.transform(test))[:,1],system.calibration)
    current=metrics(test[target],prob)
    if any(abs(current[k]-report['test'][k])>1e-6 for k in current if current[k] is not None):raise ValueError('Saved evaluation mismatch')
    return test,test[target].to_numpy(),prob


def evaluate_and_plot_all():
    systems=[LolDraftPredictionSystem.load_model(),LolSnowballPredictionSystem.load_model()]
    frames=[load_pivoted_draft_data(),load_integrated_10min_dataset()]
    targets=['blue_win','result'];names=['Draft','Snowball']
    tests=[verified_test(s,d,t) for s,d,t in zip(systems,frames,targets)]
    FIGURES_DIR.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(8,6))
    for name,(_,y,p) in zip(names,tests):
        f,t,_=roc_curve(y,p);ax.plot(f,t,label=f'{name}: AUC={auc(f,t):.4f}')
    ax.plot([0,1],[0,1],'k--');ax.set(xlabel='False positive rate',ylabel='True positive rate',title='Independent test ROC (different source/time scopes)');ax.legend()
    fig.savefig(FIGURES_DIR/'fig6_roc_auc_comparison.png',dpi=200,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,name,(_,y,p) in zip(axes,names,tests):
        cm=confusion_matrix(y,p>=.5,labels=[0,1]);ax.imshow(cm,cmap='Blues')
        for (i,j),v in np.ndenumerate(cm):ax.text(j,i,str(v),ha='center',va='center')
        ax.set(title=f'{name} (N={len(y)})',xlabel='Predicted',ylabel='Actual',xticks=[0,1],yticks=[0,1])
    fig.savefig(FIGURES_DIR/'fig7_confusion_matrices.png',dpi=200,bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,6));ax.plot([0,1],[0,1],'k--')
    for name,(_,y,p) in zip(names,tests):
        bins=calibration_bins(y,p);ax.plot([x['predicted'] for x in bins],[x['observed'] for x in bins],'o-',label=name)
    ax.set(xlabel='Mean estimated probability',ylabel='Observed win fraction',title='Test reliability (bin counts in JSON report)');ax.legend()
    fig.savefig(FIGURES_DIR/'fig8_calibration_curve.png',dpi=200,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,5))
    for ax,name,system in zip(axes,names,systems):
        imp=system.best_model.feature_importances_
        if name=='Draft':
            n=system.fe.vocab_size
            groups={f'One-hot {pos}':float(imp[i*n:(i+1)*n].sum()) for i,pos in enumerate(POSITIONS)}
            groups['Historical aggregate features']=float(imp[5*n:].sum())
        else:groups=dict(zip(system.fe.feature_names,imp.tolist()))
        series=pd.Series(groups).sort_values();ax.barh(series.index,series.values)
        ax.set(title=f'{name}: raw booster gain',xlabel='Normalized gain (not causal contribution)')
    fig.tight_layout();fig.savefig(FIGURES_DIR/'fig9_draft_vs_snowball_feature_importance.png',dpi=200,bbox_inches='tight');plt.close(fig)
    lines=['# Evaluation v2 — generated from saved test manifests','',
           'Historical scores in older documents are superseded by this report.',
           'Selection: validation log loss. Calibration: separate shrinkage set. Test untouched during selection.',
           'Pro is chronological; rank is grouped random (event timestamps unavailable).',
           '95% intervals: 300 bootstrap resamples of whole games; repeated teams/players remain a limitation.','',
           '| Model | Test rows / games | Accuracy | AUC | Log loss | Brier |','|---|---:|---:|---:|---:|---:|']
    for name,s in zip(names,systems):
        r=s.evaluation;m=r['test'];part=r['partitions']['test']
        lines.append(f"| {name} | {part['rows']} / {part['games']} | {m['accuracy']:.4f} | {m['roc_auc']:.4f} | {m['log_loss']:.4f} | {m['brier']:.4f} |")
    for name,s in zip(names,systems):
        r=s.evaluation
        lines.extend(['',f'## {name}',f'Model: {s.best_model_name}',f'Calibration: {r["calibration"]}',
                      'CI95: '+json.dumps(r['test_ci95_group_bootstrap']),
                      'Baselines (fit on train only): '+json.dumps(r['baselines']),
                      'Source-specific test: '+json.dumps(r['test_by_source']),''])
    lines+=['AUC is discrimination, not winrate uplift. Calibration does not prove individual probabilities are correct.',
            'Feature importance is computed from the actual selected booster; no fixed fallback values are used.',
            'Prior/majority baselines describe constant predictions. Gold-sign is a documented rule: .75/.25/.5, not calibrated probabilities.']
    (Path(__file__).parent/'evaluation_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines[:12]))


if __name__=='__main__':evaluate_and_plot_all()
