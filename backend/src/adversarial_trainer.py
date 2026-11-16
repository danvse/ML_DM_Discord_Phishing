"""
Adversarial Training Augmentation Module for Discord Scam Detection.
Implements minimax adversarial hardening by injecting perturbed variants
(Unicode Cyrillic homoglyphs, markdown URL disguises, and leetspeak) into 20%
of the training partition.

Evaluates the hardened model against the original unhardened baseline across:
- Clean Test Set (Generalization retention)
- Adversarial Stress-Test Set (Adversarial robustness gain)
Exports model checkpoints and the comparative hardening benchmark table.
"""

import os
import random
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

import sys
sys.path.append(os.path.dirname(__file__))
from feature_extractor import DiscordFeatureExtractor
from data_loader import build_adversarial_variant

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def build_hardened_training_set(train_df, augment_ratio=0.20):
    """
    Augment 20% of scam samples in the training set with adversarial perturbations
    (homoglyphs, leetspeak, and markdown cloaking) so the model learns split rules
    on homoglyph_count, markdown_mask, and domain distances during training.
    """
    records = []
    scam_count = 0
    augmented_count = 0

    for _, row in train_df.iterrows():
        msg = str(row["message"])
        lbl = int(row["label"])

        records.append({"message": msg, "label": lbl, "is_augmented": 0})

        if lbl == 1:
            scam_count += 1
            if random.random() < augment_ratio:
                # Create adversarial clone in training set
                adv_msg = build_adversarial_variant(msg)
                records.append({"message": adv_msg, "label": 1, "is_augmented": 1})
                augmented_count += 1

    df_hardened = pd.DataFrame(records)
    print(f"Generated hardened training partition:")
    print(f"  Original samples:   {len(train_df)}")
    print(f"  Augmented variants: {augmented_count} (targeting evasion vectors)")
    print(f"  Total train pool:   {len(df_hardened)}")
    return df_hardened


def run_adversarial_training():
    print("=" * 80)
    print("ADVERSARIAL HARDENING BENCHMARK: DISCORD SCAM DETECTION")
    print("Minimax Formulation: Hardening Tree Splits against Adversarial Evasion")
    print("=" * 80)

    # 1. Load Data
    train_df = pd.read_csv(os.path.join(PROCESSED_DIR, "train.csv"))
    val_df = pd.read_csv(os.path.join(PROCESSED_DIR, "val.csv"))
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "test.csv"))
    adv_test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "adversarial_test.csv"))

    # 2. Build Hardened Training Partition
    hardened_train_df = build_hardened_training_set(train_df, augment_ratio=0.25)

    X_train_clean_text = train_df["message"].fillna("")
    y_train_clean = train_df["label"].values

    X_train_hard_text = hardened_train_df["message"].fillna("")
    y_train_hard = hardened_train_df["label"].values

    X_val_text = val_df["message"].fillna("")
    y_val = val_df["label"].values

    X_test_text = test_df["message"].fillna("")
    y_test = test_df["label"].values

    X_adv_text = adv_test_df["message"].fillna("")
    y_adv = adv_test_df["label"].values

    # 3. Fit Feature Extractor on Hardened Vocabulary
    malicious_path = os.path.join(DATA_DIR, "raw", "malicious_domains.json")
    extractor_hardened = DiscordFeatureExtractor(malicious_domains_path=malicious_path)
    extractor_hardened.fit(X_train_hard_text)

    # Transform Feature Matrices
    X_tr_hard_fused = extractor_hardened.transform_fused(X_train_hard_text)
    X_val_fused = extractor_hardened.transform_fused(X_val_text)
    X_te_fused = extractor_hardened.transform_fused(X_test_text)
    X_adv_fused = extractor_hardened.transform_fused(X_adv_text)

    # Transform Clean Baseline Matrices (using existing clean extractor)
    clean_extractor_path = os.path.join(MODELS_DIR, "feature_extractor.joblib")
    clean_extractor = joblib.load(clean_extractor_path)
    X_tr_clean_fused = clean_extractor.transform_fused(X_train_clean_text)
    X_val_clean_fused = clean_extractor.transform_fused(X_val_text)
    X_te_clean_fused = clean_extractor.transform_fused(X_test_text)
    X_adv_clean_fused = clean_extractor.transform_fused(X_adv_text)

    # 4. Train Clean-Only Baseline XGBoost
    print("\n[1/2] Training Baseline XGBoost (Clean Data Only)...")
    xgb_clean = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
    xgb_clean.fit(X_tr_clean_fused, y_train_clean, eval_set=[(X_val_clean_fused, y_val)], verbose=False)

    # Evaluate Baseline
    y_pred_base = xgb_clean.predict(X_te_clean_fused)
    y_prob_base = xgb_clean.predict_proba(X_te_clean_fused)[:, 1]
    y_adv_base = xgb_clean.predict(X_adv_clean_fused)
    y_adv_prob_base = xgb_clean.predict_proba(X_adv_clean_fused)[:, 1]

    f1_clean_base = f1_score(y_test, y_pred_base)
    f1_adv_base = f1_score(y_adv, y_adv_base)
    drop_base = ((f1_clean_base - f1_adv_base) / f1_clean_base) * 100

    # 5. Train Adversarially Hardened XGBoost
    print("\n[2/2] Training Adversarially Hardened XGBoost (with 25% Augmented Evasion Vectors)...")
    xgb_hardened = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
    xgb_hardened.fit(X_tr_hard_fused, y_train_hard, eval_set=[(X_val_fused, y_val)], verbose=False)

    # Evaluate Hardened Model
    y_pred_hard = xgb_hardened.predict(X_te_fused)
    y_prob_hard = xgb_hardened.predict_proba(X_te_fused)[:, 1]
    y_adv_hard = xgb_hardened.predict(X_adv_fused)
    y_adv_prob_hard = xgb_hardened.predict_proba(X_adv_fused)[:, 1]

    f1_clean_hard = f1_score(y_test, y_pred_hard)
    f1_adv_hard = f1_score(y_adv, y_adv_hard)
    drop_hard = ((f1_clean_hard - f1_adv_hard) / f1_clean_hard) * 100

    # Save Hardened Checkpoint
    joblib.dump(extractor_hardened, os.path.join(MODELS_DIR, "feature_extractor_hardened.joblib"))
    joblib.dump(xgb_hardened, os.path.join(MODELS_DIR, "xgboost_hardened.joblib"))

    # 6. Comparative Benchmark Report
    comparison = [
        {
            "Model Variant": "XGBoost Fused (Clean Baseline)",
            "Clean Precision": round(precision_score(y_test, y_pred_base), 4),
            "Clean Recall": round(recall_score(y_test, y_pred_base), 4),
            "Clean F1": round(f1_clean_base, 4),
            "Clean AUROC": round(roc_auc_score(y_test, y_prob_base), 4),
            "Adv. Precision": round(precision_score(y_adv, y_adv_base), 4),
            "Adv. Recall": round(recall_score(y_adv, y_adv_base), 4),
            "Adv. F1": round(f1_adv_base, 4),
            "Adv. AUROC": round(roc_auc_score(y_adv, y_adv_prob_base), 4),
            "Delta F1 Drop": f"-{drop_base:.1f}%"
        },
        {
            "Model Variant": "XGBoost Fused (Adversarially Hardened)",
            "Clean Precision": round(precision_score(y_test, y_pred_hard), 4),
            "Clean Recall": round(recall_score(y_test, y_pred_hard), 4),
            "Clean F1": round(f1_clean_hard, 4),
            "Clean AUROC": round(roc_auc_score(y_test, y_prob_hard), 4),
            "Adv. Precision": round(precision_score(y_adv, y_adv_hard), 4),
            "Adv. Recall": round(recall_score(y_adv, y_adv_hard), 4),
            "Adv. F1": round(f1_adv_hard, 4),
            "Adv. AUROC": round(roc_auc_score(y_adv, y_adv_prob_hard), 4),
            "Delta F1 Drop": f"-{drop_hard:.1f}%"
        }
    ]

    df_comp = pd.DataFrame(comparison)
    out_csv = os.path.join(PROCESSED_DIR, "adversarial_hardening_benchmark.csv")
    df_comp.to_csv(out_csv, index=False)

    print("\n" + "=" * 80)
    print("ADVERSARIAL HARDENING BENCHMARK RESULTS")
    print("=" * 80)
    print(df_comp.to_string(index=False))
    print(f"\nHardening report exported to: {out_csv}")

    # Inspect Feature Importance shift in Hardened Model
    importances = xgb_hardened.feature_importances_
    n_tfidf = X_tr_hard_fused.shape[1] - len(extractor_hardened.feature_names)
    heur_importances = importances[n_tfidf:]
    heur_df = pd.DataFrame({
        "Heuristic Feature": extractor_hardened.feature_names,
        "Hardened Importance": [round(float(s), 5) for s in heur_importances]
    }).sort_values(by="Hardened Importance", ascending=False)

    print("\nHeuristic Feature Importance Shifts in Hardened Model:")
    print(heur_df.head(10).to_string(index=False))

    return df_comp, heur_df


if __name__ == "__main__":
    run_adversarial_training()
