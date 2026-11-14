"""
Comprehensive Evaluation Report Generator:
Evaluates all trained models across standard metrics:
- Precision, Recall, F1-Score, AUROC
- Adversarial F1-Score and Delta F1 (Drop under evasion)
- Saves a clean markdown and CSV benchmark table.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

from feature_extractor import DiscordFeatureExtractor
from train_baselines import RegexBaselineMatcher

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def generate_evaluation_report():
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "test.csv"))
    adv_test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "adversarial_test.csv"))

    X_test_text = test_df["message"].fillna("")
    y_test = test_df["label"].values

    X_adv_text = adv_test_df["message"].fillna("")
    y_adv = adv_test_df["label"].values

    # Load extractor and models
    extractor = joblib.load(os.path.join(MODELS_DIR, "feature_extractor.joblib"))
    nb = joblib.load(os.path.join(MODELS_DIR, "naive_bayes.joblib"))
    lr = joblib.load(os.path.join(MODELS_DIR, "logistic_regression.joblib"))
    lsvc = joblib.load(os.path.join(MODELS_DIR, "linear_svc.joblib"))
    rf = joblib.load(os.path.join(MODELS_DIR, "random_forest.joblib"))
    xgb_fused = joblib.load(os.path.join(MODELS_DIR, "xgboost_fused.joblib"))

    # Feature transforms
    X_test_tfidf = extractor.transform_tfidf(X_test_text)
    X_adv_tfidf = extractor.transform_tfidf(X_adv_text)

    X_test_fused = extractor.transform_fused(X_test_text)
    X_adv_fused = extractor.transform_fused(X_adv_text)

    benchmarks = []

    # 1. Regex (AutoMod)
    regex = RegexBaselineMatcher()
    y_p_regex = regex.predict(X_test_text)
    y_a_regex = regex.predict(X_adv_text)
    f1_clean = f1_score(y_test, y_p_regex)
    f1_adv = f1_score(y_adv, y_a_regex)
    benchmarks.append({
        "Model Tier": "Tier 1: Baseline",
        "Model Name": "Regex / Keyword (AutoMod)",
        "Input Features": "Keyword/URL Rules",
        "Precision": round(precision_score(y_test, y_p_regex), 4),
        "Recall": round(recall_score(y_test, y_p_regex), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": "-",
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": f"-{(f1_clean - f1_adv) * 100:.1f}%"
    })

    # 2. Naive Bayes
    y_p_nb = nb.predict(X_test_tfidf)
    y_a_nb = nb.predict(X_adv_tfidf)
    y_prob_nb = nb.predict_proba(X_test_tfidf)[:, 1]
    f1_clean = f1_score(y_test, y_p_nb)
    f1_adv = f1_score(y_adv, y_a_nb)
    benchmarks.append({
        "Model Tier": "Tier 1: Baseline",
        "Model Name": "Multinomial Naive Bayes",
        "Input Features": "TF-IDF (Word n-grams)",
        "Precision": round(precision_score(y_test, y_p_nb), 4),
        "Recall": round(recall_score(y_test, y_p_nb), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": round(roc_auc_score(y_test, y_prob_nb), 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": f"-{(f1_clean - f1_adv) * 100:.1f}%"
    })

    # 3. Logistic Regression
    y_p_lr = lr.predict(X_test_tfidf)
    y_a_lr = lr.predict(X_adv_tfidf)
    y_prob_lr = lr.predict_proba(X_test_tfidf)[:, 1]
    f1_clean = f1_score(y_test, y_p_lr)
    f1_adv = f1_score(y_adv, y_a_lr)
    benchmarks.append({
        "Model Tier": "Tier 1: Baseline",
        "Model Name": "Logistic Regression",
        "Input Features": "TF-IDF (Word n-grams)",
        "Precision": round(precision_score(y_test, y_p_lr), 4),
        "Recall": round(recall_score(y_test, y_p_lr), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": round(roc_auc_score(y_test, y_prob_lr), 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": f"-{(f1_clean - f1_adv) * 100:.1f}%"
    })

    # 4. LinearSVC
    y_p_lsvc = lsvc.predict(X_test_tfidf)
    y_a_lsvc = lsvc.predict(X_adv_tfidf)
    f1_clean = f1_score(y_test, y_p_lsvc)
    f1_adv = f1_score(y_adv, y_a_lsvc)
    benchmarks.append({
        "Model Tier": "Tier 1: Baseline",
        "Model Name": "LinearSVC",
        "Input Features": "TF-IDF (Word n-grams)",
        "Precision": round(precision_score(y_test, y_p_lsvc), 4),
        "Recall": round(recall_score(y_test, y_p_lsvc), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": "-",
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": f"-{(f1_clean - f1_adv) * 100:.1f}%"
    })

    # 5. Random Forest
    y_p_rf = rf.predict(X_test_fused)
    y_a_rf = rf.predict(X_adv_fused)
    y_prob_rf = rf.predict_proba(X_test_fused)[:, 1]
    f1_clean = f1_score(y_test, y_p_rf)
    f1_adv = f1_score(y_adv, y_a_rf)
    benchmarks.append({
        "Model Tier": "Tier 2: Classical Fusion",
        "Model Name": "Random Forest",
        "Input Features": "TF-IDF + 17 Heuristics",
        "Precision": round(precision_score(y_test, y_p_rf), 4),
        "Recall": round(recall_score(y_test, y_p_rf), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": round(roc_auc_score(y_test, y_prob_rf), 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": f"-{(f1_clean - f1_adv) * 100:.1f}%"
    })

    # 6. XGBoost Fused (Candidate Model)
    y_p_xgb = xgb_fused.predict(X_test_fused)
    y_a_xgb = xgb_fused.predict(X_adv_fused)
    y_prob_xgb = xgb_fused.predict_proba(X_test_fused)[:, 1]
    f1_clean = f1_score(y_test, y_p_xgb)
    f1_adv = f1_score(y_adv, y_a_xgb)
    benchmarks.append({
        "Model Tier": "Tier 2: Classical Fusion",
        "Model Name": "XGBoost Fused (Proposed)",
        "Input Features": "TF-IDF + 17 Heuristics",
        "Precision": round(precision_score(y_test, y_p_xgb), 4),
        "Recall": round(recall_score(y_test, y_p_xgb), 4),
        "F1-Score": round(f1_clean, 4),
        "AUROC": round(roc_auc_score(y_test, y_prob_xgb), 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": f"-{(f1_clean - f1_adv) * 100:.1f}%"
    })

    df_report = pd.DataFrame(benchmarks)
    report_csv = os.path.join(DATA_DIR, "processed", "model_benchmark_report.csv")
    df_report.to_csv(report_csv, index=False)

    print("=" * 80)
    print("FINAL BENCHMARK EVALUATION TABLE")
    print("=" * 80)
    print(df_report.to_string(index=False))
    print(f"\nReport saved to: {report_csv}")


if __name__ == "__main__":
    generate_evaluation_report()
