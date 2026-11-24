# Evaluation v2 — generated from saved test manifests

Historical scores in older documents are superseded by this report.
Selection: validation log loss. Calibration: separate shrinkage set. Test untouched during selection.
Pro is chronological; rank is grouped random (event timestamps unavailable).
95% intervals: 300 bootstrap resamples of whole games; repeated teams/players remain a limitation.

| Model | Test rows / games | Accuracy | AUC | Log loss | Brier |
|---|---:|---:|---:|---:|---:|
| Draft | 600 / 600 | 0.5517 | 0.5628 | 0.6834 | 0.2452 |
| Snowball | 1374 / 687 | 0.6718 | 0.7413 | 0.6004 | 0.2066 |

## Draft
Model: XGBoost CUDA depth=2
Calibration: {'method': 'shrink_to_training_prior', 'alpha': 0.48, 'prior': 0.5285952248750694}
CI95: {"accuracy": [0.5115833333333333, 0.595], "roc_auc": [0.5148291522313297, 0.6080633565482949], "log_loss": [0.6763573597254371, 0.6900198246838544], "brier": [0.24165079631067857, 0.24844169772017688]}
Baselines (fit on train only): {"training_prior": {"accuracy": 0.565, "roc_auc": 0.5, "log_loss": 0.6873423544733986, "brier": 0.2471003076518968}, "majority_class": {"accuracy": 0.565, "roc_auc": null, "log_loss": null, "brier": null, "prediction_kind": "hard_class_only_no_probability_claim"}}
Source-specific test: {}


## Snowball
Model: XGBoost CUDA depth=2
Calibration: {'method': 'shrink_to_training_prior', 'alpha': 0.97, 'prior': 0.5}
CI95: {"accuracy": [0.6320778748180494, 0.7081877729257642], "roc_auc": [0.7040898872595446, 0.7769042829084113], "log_loss": [0.5671429290797038, 0.6320967693888516], "brier": [0.1927439215951474, 0.22056057588145422]}
Baselines (fit on train only): {"training_prior": {"accuracy": 0.5, "roc_auc": 0.5, "log_loss": 0.6931471805599454, "brier": 0.25}, "majority_class": {"accuracy": 0.5, "roc_auc": null, "log_loss": null, "brier": null, "prediction_kind": "hard_class_only_no_probability_claim"}, "training_side_prior": {"accuracy": 0.5327510917030568, "roc_auc": 0.5327510917030568, "log_loss": 0.6918341943212817, "brier": 0.24934362487375608}, "gold_sign_rule": {"accuracy": 0.653566229985444, "roc_auc": 0.653566229985444, "log_loss": 0.6682784693993938, "brier": 0.23571688500727803}}
Source-specific test: {"1": {"accuracy": 0.661522633744856, "roc_auc": 0.7296800115158598, "log_loss": 0.6105628575258135, "brier": 0.2107540789138706}, "0": {"accuracy": 0.6965174129353234, "roc_auc": 0.7729635405064231, "log_loss": 0.5757586599642247, "brier": 0.1966787741450308}}

AUC is discrimination, not winrate uplift. Calibration does not prove individual probabilities are correct.
Feature importance is computed from the actual selected booster; no fixed fallback values are used.
Prior/majority baselines describe constant predictions. Gold-sign is a documented rule: .75/.25/.5, not calibrated probabilities.
