"""Group-safe partitions, probability calibration and reproducible evaluation."""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss, brier_score_loss
from xgboost import XGBClassifier, build_info

SCHEMA_VERSION = 2


def fingerprint(df):
    stable = df.sort_values(['gameid'] + (['side'] if 'side' in df else [])).reset_index(drop=True)
    return hashlib.sha256(pd.util.hash_pandas_object(stable.astype(str), index=False).values.tobytes()).hexdigest()


def split_groups(df, test_size=.20):
    """60/10/10/20 within each source; equal dates never cross a boundary.

    Pro: chronological by event date. Rank has no event timestamp in existing
    schema: seeded grouped holdout, explicitly NOT a future-generalization test.
    """
    if not 0 < test_size < .5: raise ValueError('test_size must be between 0 and .5')
    names = ['train', 'validation', 'calibration', 'test']
    ids = {name: [] for name in names}
    policies = {}
    sources = df.groupby('is_pro_play', sort=True) if 'is_pro_play' in df else [('draft', df)]
    for source, sub in sources:
        groups = sub[['gameid']].drop_duplicates()
        if source == 0:
            groups = groups.sort_values('gameid').sample(frac=1, random_state=42).reset_index(drop=True)
            units = [[g] for g in groups.gameid]
            policies[str(source)] = 'grouped_random_no_event_timestamp'
        else:
            dates = sub.groupby('gameid').date.first()
            parsed = pd.to_datetime(dates, errors='raise', utc=True)
            units = [list(v.index) for _, v in parsed.groupby(parsed, sort=True)]
            policies[str(source)] = 'chronological_event_time'
        if len(units) < 10: raise ValueError('Need at least 10 independent time/group units')
        # Split whole time blocks based on cumulative game counts.
        total = sum(map(len, units))
        boundaries = np.array([1-test_size-.2, 1-test_size-.1, 1-test_size]) * total
        seen = 0
        for unit in units:
            part = int(np.searchsorted(boundaries, seen, side='right'))
            ids[names[part]].extend(unit)
            seen += len(unit)
    result = {name: df[df.gameid.isin(values)].copy() for name, values in ids.items()}
    if any(frame.empty for frame in result.values()): raise ValueError('Empty evaluation partition')
    for i, a in enumerate(names):
        for b in names[i+1:]:
            if set(ids[a]) & set(ids[b]): raise ValueError('gameid crosses partitions')
    return result, policies


def gpu_candidates():
    if not build_info().get('USE_CUDA'): raise RuntimeError('XGBoost lacks CUDA support')
    if sys.platform == 'win32':
        import ctypes
        driver = ctypes.WinDLL('nvcuda.dll')
        if driver.cuInit(0) != 0: raise RuntimeError('CUDA driver initialization failed')
        count, version = ctypes.c_int(), ctypes.c_int()
        if driver.cuDeviceGetCount(ctypes.byref(count)) != 0 or count.value < 1:
            raise RuntimeError('No CUDA device; training aborted before fit')
        driver.cuDriverGetVersion(ctypes.byref(version))
        if version.value // 1000 < build_info()['CUDA_VERSION'][0]:
            raise RuntimeError('XGBoost CUDA major version exceeds driver support')
    models = {}
    for depth in [2, 4]:
        model = XGBClassifier(n_estimators=180, max_depth=depth, learning_rate=.035,
                              min_child_weight=8, reg_lambda=5, subsample=.85,
                              colsample_bytree=.85, random_state=42, n_jobs=-1,
                              tree_method='hist', device='cuda', eval_metric='logloss')
        models[f'XGBoost CUDA depth={depth}'] = model
    return models


def check_gpu(model):
    config = json.loads(model.get_booster().save_config())
    if not config['learner']['generic_param']['device'].startswith('cuda'):
        raise RuntimeError('CUDA training required; refusing silent CPU fallback')


def metrics(y, prob):
    y, prob = np.asarray(y), np.clip(np.asarray(prob, dtype=float), 1e-7, 1-1e-7)
    return {'accuracy': float(accuracy_score(y, prob >= .5)),
            'roc_auc': float(roc_auc_score(y, prob)) if len(np.unique(y)) == 2 else None,
            'log_loss': float(log_loss(y, prob, labels=[0, 1])),
            'brier': float(brier_score_loss(y, prob))}


def calibration_bins(y, p):
    d = pd.DataFrame({'y': np.asarray(y), 'p': np.asarray(p)})
    d['bin'] = pd.cut(d.p, np.linspace(0, 1, 11), include_lowest=True)
    out = d.groupby('bin', observed=True).agg(n=('y', 'size'), predicted=('p', 'mean'), observed=('y', 'mean'))
    return [{'bin': str(i), **row.to_dict()} for i, row in out.iterrows()]


def bootstrap_intervals(df, y, p, repetitions=300):
    groups = df.gameid.astype(str).to_numpy()
    unique = np.unique(groups)
    locations = {g: np.flatnonzero(groups == g) for g in unique}
    rng = np.random.default_rng(42)
    samples = {k: [] for k in metrics(y, p)}
    for _ in range(repetitions):
        idx = np.concatenate([locations[g] for g in rng.choice(unique, len(unique), replace=True)])
        for key, value in metrics(np.asarray(y)[idx], np.asarray(p)[idx]).items():
            if value is not None: samples[key].append(value)
    return {k: [float(x) for x in np.quantile(v, [.025, .975])] if v else None for k, v in samples.items()}


def calibrate(p, calibration):
    return np.clip(calibration['alpha'] * np.asarray(p) + (1-calibration['alpha']) * calibration['prior'], 1e-7, 1-1e-7)


def evaluate_training(system, df, target, model_path, test_size=.2, oof_transform=None):
    parts, policies = split_groups(df, test_size)
    train, val, cal, test = (parts[n] for n in ['train','validation','calibration','test'])
    if oof_transform:
        X_train = oof_transform(system.fe, train)
    else:
        X_train = system.fe.fit_transform(train)
    X_val, X_cal, X_test = (system.fe.transform(f) for f in [val, cal, test])
    candidates = gpu_candidates()
    rows = []
    for name, model in candidates.items():
        weights = system.fe.compute_sample_weights(train.date) if hasattr(system.fe, 'compute_sample_weights') else None
        model.fit(X_train, train[target].to_numpy(), sample_weight=weights)
        check_gpu(model)
        rows.append({'model': name, **metrics(val[target], model.predict_proba(X_val)[:,1])})
    best = min(rows, key=lambda r: r['log_loss'])
    system.best_model_name = best['model']
    system.best_model = candidates[best['model']]
    prior = float(train[target].mean())
    raw_cal = system.best_model.predict_proba(X_cal)[:,1]
    alpha = min(np.linspace(0,1,101), key=lambda a: metrics(cal[target], a*raw_cal+(1-a)*prior)['log_loss'])
    system.calibration = {'method': 'shrink_to_training_prior', 'alpha': float(alpha), 'prior': prior}
    raw_test = system.best_model.predict_proba(X_test)[:,1]
    prob = calibrate(raw_test, system.calibration)
    baselines = {'training_prior': np.full(len(test),prior),
                 'majority_class': np.full(len(test),float(prior >= .5))}
    if 'side' in train:
        side_prior = train.groupby('side')[target].mean().to_dict()
        baselines['training_side_prior'] = test.side.map(side_prior).fillna(prior).to_numpy()
    if 'golddiffat10' in test:
        baselines['gold_sign_rule'] = np.where(test.golddiffat10>0,.75,np.where(test.golddiffat10<0,.25,.5))
    report = {'schema_version': SCHEMA_VERSION, 'data_fingerprint': fingerprint(df),
              'training_device': json.loads(system.best_model.get_booster().save_config())['learner']['generic_param']['device'],
              'split_policy': policies, 'selected_by': 'validation_log_loss',
              'partitions': {n: {'rows':len(f), 'games':int(f.gameid.nunique()), 'gameids':sorted(f.gameid.astype(str).unique().tolist())} for n,f in parts.items()},
              'validation_candidates':rows, 'calibration':system.calibration,
              'test_raw': metrics(test[target],raw_test), 'test':metrics(test[target],prob),
              'test_ci95_group_bootstrap':bootstrap_intervals(test,test[target],prob),
              'reliability_bins':calibration_bins(test[target],prob),
              'baselines':{n:metrics(test[target],p) for n,p in baselines.items()},
              'limitations':['Observational prediction; no causal winrate uplift.',
                            'Intervals resample games; repeated teams/players may still be dependent.',
                            'Rank holdout is grouped random because event timestamps are unavailable.']}
    report['baselines']['majority_class'] = {
        'accuracy': float(np.mean(test[target].to_numpy() == int(prior >= .5))),
        'roc_auc': None, 'log_loss': None, 'brier': None,
        'prediction_kind': 'hard_class_only_no_probability_claim'}
    report['test_by_source'] = {}
    if 'is_pro_play' in test:
        for source in test.is_pro_play.unique():
            mask = test.is_pro_play.to_numpy() == source
            report['test_by_source'][str(source)] = metrics(test[target].to_numpy()[mask],prob[mask])
    system.evaluation = report
    system.schema_version = SCHEMA_VERSION
    system.save_model(model_path)
    path = Path(model_path).with_suffix('.evaluation.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['partitions','reliability_bins']},ensure_ascii=False,indent=2))
    return pd.DataFrame(rows)
