"""
Tier 2 Classical ML and Feature Fusion Training:
1. Random Forest on (TF-IDF + Heuristics)
2. XGBoost on (TF-IDF only)
3. XGBoost on (TF-IDF + Heuristics) -- Primary Candidate Model
Calculates Feature Importances and evaluates Adversarial Resilience.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

from feature_extractor import DiscordFeatureExtractor

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def train_and_eval_xgboost():
    print("=" * 60)
    print("Training Tier 2 Feature Fusion Models (XGBoost & Random Forest)")
    print("=" * 60)

    # 1. Load data
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

    # Pure TF-IDF
    X_train_tfidf = extractor.transform_tfidf(X_train_text)
    X_val_tfidf = extractor.transform_tfidf(X_val_text)
    X_test_tfidf = extractor.transform_tfidf(X_test_text)
    X_adv_tfidf = extractor.transform_tfidf(X_adv_text)

    # Fused (TF-IDF + 17 Heuristics)
    X_train_fused = extractor.transform_fused(X_train_text)
    X_val_fused = extractor.transform_fused(X_val_text)
    X_test_fused = extractor.transform_fused(X_test_text)
    X_adv_fused = extractor.transform_fused(X_adv_text)

    results = []

    # --- Model 1: Random Forest on Fused Features ---
    print("\nTraining Random Forest on Fused Features...")
    rf = RandomForestClassifier(n_estimators=150, max_depth=20, random_state=42, n_jobs=-1)
    rf.fit(X_train_fused, y_train)

    y_pred_rf = rf.predict(X_test_fused)
    y_adv_rf = rf.predict(X_adv_fused)
    y_proba_rf = rf.predict_proba(X_test_fused)[:, 1]

    results.append({
        "Model": "Random Forest (TF-IDF + Heuristics)",
        "Precision": round(precision_score(y_test, y_pred_rf), 4),
        "Recall": round(recall_score(y_test, y_pred_rf), 4),
        "F1-Score": round(f1_score(y_test, y_pred_rf), 4),
        "AUROC": round(roc_auc_score(y_test, y_proba_rf), 4),
        "Adversarial F1": round(f1_score(y_adv, y_adv_rf), 4),
        "Delta F1 (Drop)": round(f1_score(y_test, y_pred_rf) - f1_score(y_adv, y_adv_rf), 4)
    })
    joblib.dump(rf, os.path.join(MODELS_DIR, "random_forest.joblib"))

    # --- Model 2: XGBoost on TF-IDF Only ---
    print("Training XGBoost on TF-IDF Only...")
    xgb_text = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42
    )
    xgb_text.fit(X_train_tfidf, y_train)

    y_pred_xgb_t = xgb_text.predict(X_test_tfidf)
    y_adv_xgb_t = xgb_text.predict(X_adv_tfidf)
    y_proba_xgb_t = xgb_text.predict_proba(X_test_tfidf)[:, 1]

    results.append({
        "Model": "XGBoost (TF-IDF Only)",
        "Precision": round(precision_score(y_test, y_pred_xgb_t), 4),
        "Recall": round(recall_score(y_test, y_pred_xgb_t), 4),
        "F1-Score": round(f1_score(y_test, y_pred_xgb_t), 4),
        "AUROC": round(roc_auc_score(y_test, y_proba_xgb_t), 4),
        "Adversarial F1": round(f1_score(y_adv, y_adv_xgb_t), 4),
        "Delta F1 (Drop)": round(f1_score(y_test, y_pred_xgb_t) - f1_score(y_adv, y_adv_xgb_t), 4)
    })

    # --- Model 3: XGBoost on Fused Features (Core Proposed Model) ---
    print("Training XGBoost on Fused Features (TF-IDF + Heuristics)...")
    xgb_fused = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
    xgb_fused.fit(
        X_train_fused, y_train,
        eval_set=[(X_val_fused, y_val)],
        verbose=False
    )

    y_pred_fused = xgb_fused.predict(X_test_fused)
    y_adv_fused = xgb_fused.predict(X_adv_fused)
    y_proba_fused = xgb_fused.predict_proba(X_test_fused)[:, 1]

    f1_clean = f1_score(y_test, y_pred_fused)
    f1_adv = f1_score(y_adv, y_adv_fused)

    results.append({
        "Model": "XGBoost Fused (TF-IDF + Heuristics)",
        "Precision": round(precision_score(y_test, y_pred_fused), 4),
        "Recall": round(recall_score(y_test, y_pred_fused), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": round(roc_auc_score(y_test, y_proba_fused), 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": round(f1_clean - f1_adv, 4)
    })
    joblib.dump(xgb_fused, os.path.join(MODELS_DIR, "xgboost_fused.joblib"))

    # 3. Print Results
    df_res = pd.DataFrame(results)
    print("\nTier 2 Results Comparison:")
    print(df_res.to_string(index=False))

    # 4. Analyze Feature Importances for the 17 Heuristics
    importances = xgb_fused.feature_importances_
    n_tfidf = X_train_tfidf.shape[1]
    heur_importances = importances[n_tfidf:]
    heur_df = pd.DataFrame({
        "Heuristic Feature": extractor.feature_names,
        "Importance Score": [round(float(s), 5) for s in heur_importances]
    }).sort_values(by="Importance Score", ascending=False)

    print("\nTop Heuristic Feature Importances in XGBoost:")
    print(heur_df.to_string(index=False))

    return df_res, heur_df


if __name__ == "__main__":
    train_and_eval_xgboost()
