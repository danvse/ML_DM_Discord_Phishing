"""
Formal Feature Ablation Study for Discord Scam Detection.
Conducts a rigorous 3-way ablation experiment:
1. Stream A Only: Pure Text Semantics (TF-IDF word & char n-grams)
2. Stream B Only: Pure Structural Payload & Evasion Heuristics (17 numeric indicators)
3. Full Fused Representation: Stream A + Stream B (Joint Multimodal Feature Vector)

Evaluates each configuration across both:
- Held-out Clean Test Set (356 samples)
- Adversarial Stress-Test Set (356 samples with homoglyphs, leetspeak, markdown masks)
Calculates Precision, Recall, F1, AUROC, Adversarial F1, and Delta F1 Drop.
"""

import os
import joblib
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

import sys
sys.path.append(os.path.dirname(__file__))
from feature_extractor import DiscordFeatureExtractor

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def run_ablation_study():
    print("=" * 80)
    print("FORMAL FEATURE ABLATION STUDY: DISCORD SCAM DETECTION")
    print("Evaluating: Stream A (Text Only) vs. Stream B (Heuristics Only) vs. Fused")
    print("=" * 80)

    # 1. Load Data
    train_df = pd.read_csv(os.path.join(PROCESSED_DIR, "train.csv"))
    val_df = pd.read_csv(os.path.join(PROCESSED_DIR, "val.csv"))
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "test.csv"))
    adv_test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "adversarial_test.csv"))

    X_train_text = train_df["message"].fillna("")
    y_train = train_df["label"].values

    X_val_text = val_df["message"].fillna("")
    y_val = val_df["label"].values

    X_test_text = test_df["message"].fillna("")
    y_test = test_df["label"].values

    X_adv_text = adv_test_df["message"].fillna("")
    y_adv = adv_test_df["label"].values

    # 2. Extract Features
    malicious_path = os.path.join(DATA_DIR, "raw", "malicious_domains.json")
    extractor = DiscordFeatureExtractor(malicious_domains_path=malicious_path)
    extractor.fit(X_train_text)

    # --- Stream A: Pure TF-IDF Text Vectors ---
    X_tr_text = extractor.transform_tfidf(X_train_text)
    X_val_text_mat = extractor.transform_tfidf(X_val_text)
    X_te_text = extractor.transform_tfidf(X_test_text)
    X_adv_text_mat = extractor.transform_tfidf(X_adv_text)

    # --- Stream B: Pure 17 Structural Heuristics ---
    X_tr_heur = csr_matrix(extractor.extract_heuristics(X_train_text))
    X_val_heur = csr_matrix(extractor.extract_heuristics(X_val_text))
    X_te_heur = csr_matrix(extractor.extract_heuristics(X_test_text))
    X_adv_heur = csr_matrix(extractor.extract_heuristics(X_adv_text))

    # --- Full Fused Stream: Text + Heuristics ---
    X_tr_fused = extractor.transform_fused(X_train_text)
    X_val_fused = extractor.transform_fused(X_val_text)
    X_te_fused = extractor.transform_fused(X_test_text)
    X_adv_fused = extractor.transform_fused(X_adv_text)

    configurations = [
        ("Stream A: Text Semantics Only", X_tr_text, X_val_text_mat, X_te_text, X_adv_text_mat, "TF-IDF (3,000 n-grams)"),
        ("Stream B: Structural Heuristics Only", X_tr_heur, X_val_heur, X_te_heur, X_adv_heur, "17 Payload & Evasion Features"),
        ("Dual-Stream Fused (Proposed)", X_tr_fused, X_val_fused, X_te_fused, X_adv_fused, "TF-IDF + 17 Heuristics")
    ]

    results = []

    for name, X_tr, X_va, X_te, X_ad, desc in configurations:
        print(f"\nTraining XGBoost on: {name} ({desc})...")
        model = XGBClassifier(
            n_estimators=250,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        )
        model.fit(X_tr, y_train, eval_set=[(X_va, y_val)], verbose=False)

        # Clean Evaluation
        y_pred = model.predict(X_te)
        y_proba = model.predict_proba(X_te)[:, 1]
        p_clean = precision_score(y_test, y_pred)
        r_clean = recall_score(y_test, y_pred)
        f1_clean = f1_score(y_test, y_pred)
        auc_clean = roc_auc_score(y_test, y_proba)

        # Adversarial Evaluation
        y_adv_pred = model.predict(X_ad)
        y_adv_proba = model.predict_proba(X_ad)[:, 1]
        p_adv = precision_score(y_adv, y_adv_pred)
        r_adv = recall_score(y_adv, y_adv_pred)
        f1_adv = f1_score(y_adv, y_adv_pred)
        auc_adv = roc_auc_score(y_adv, y_adv_proba)

        delta_f1 = f1_clean - f1_adv
        drop_pct = (delta_f1 / f1_clean) * 100

        results.append({
            "Feature Configuration": name,
            "Dimensionality": X_tr.shape[1],
            "Clean Precision": round(p_clean, 4),
            "Clean Recall": round(r_clean, 4),
            "Clean F1": round(f1_clean, 4),
            "Clean AUROC": round(auc_clean, 4),
            "Adversarial Recall": round(r_adv, 4),
            "Adversarial F1": round(f1_adv, 4),
            "Adversarial AUROC": round(auc_adv, 4),
            "Delta F1 Drop": f"-{drop_pct:.1f}%"
        })

    df_res = pd.DataFrame(results)
    out_csv = os.path.join(PROCESSED_DIR, "feature_ablation_results.csv")
    df_res.to_csv(out_csv, index=False)

    print("\n" + "=" * 80)
    print("FEATURE ABLATION STUDY RESULTS TABLE")
    print("=" * 80)
    print(df_res.to_string(index=False))
    print(f"\nAblation table exported to: {out_csv}")

    return df_res


if __name__ == "__main__":
    run_ablation_study()
