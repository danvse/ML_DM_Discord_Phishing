"""
Baseline model training and evaluation:
1. Regex / Keyword rule matcher (mimicking AutoMod)
2. Multinomial Naive Bayes (TF-IDF)
3. Logistic Regression (TF-IDF)
4. LinearSVC (TF-IDF)
"""

import os
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, roc_auc_score

from feature_extractor import DiscordFeatureExtractor

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)


class RegexBaselineMatcher:
    """Simulates native Discord AutoMod keyword and regex filters."""
    def __init__(self):
        self.patterns = [
            re.compile(r'\b(nitro|airdrop|giveaway|steam\s*gift|claim\s*now)\b', re.IGNORECASE),
            re.compile(r'https?://[^\s]*(nitro|gift|drop|trade|steam|discord)[^\s]*', re.IGNORECASE),
            re.compile(r'@everyone\b', re.IGNORECASE),
        ]

    def predict(self, texts):
        preds = []
        for text in texts:
            t = str(text)
            matched = any(p.search(t) for p in self.patterns)
            preds.append(1 if matched else 0)
        return np.array(preds)


def train_and_eval_baselines():
    print("=" * 60)
    print("Training Tier 1 Baseline Models (Pure Text)")
    print("=" * 60)

    # 1. Load data
    train_df = pd.read_csv(os.path.join(PROCESSED_DIR, "train.csv"))
    val_df = pd.read_csv(os.path.join(PROCESSED_DIR, "val.csv"))
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "test.csv"))
    adv_test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "adversarial_test.csv"))

    X_train_text = train_df["message"].fillna("")
    y_train = train_df["label"].values

    X_test_text = test_df["message"].fillna("")
    y_test = test_df["label"].values

    X_adv_text = adv_test_df["message"].fillna("")
    y_adv = adv_test_df["label"].values

    # 2. Fit TF-IDF Feature Extractor
    malicious_path = os.path.join(DATA_DIR, "raw", "malicious_domains.json")
    extractor = DiscordFeatureExtractor(malicious_domains_path=malicious_path)
    extractor.fit(X_train_text)

    X_train_tfidf = extractor.transform_tfidf(X_train_text)
    X_test_tfidf = extractor.transform_tfidf(X_test_text)
    X_adv_tfidf = extractor.transform_tfidf(X_adv_text)

    joblib.dump(extractor, os.path.join(MODELS_DIR, "feature_extractor.joblib"))

    results = []

    # --- Baseline 1: Regex Matcher ---
    regex_matcher = RegexBaselineMatcher()
    y_pred_regex = regex_matcher.predict(X_test_text)
    y_adv_regex = regex_matcher.predict(X_adv_text)

    p = precision_score(y_test, y_pred_regex, zero_division=0)
    r = recall_score(y_test, y_pred_regex, zero_division=0)
    f1 = f1_score(y_test, y_pred_regex, zero_division=0)
    f1_adv = f1_score(y_adv, y_adv_regex, zero_division=0)
    delta_f1 = f1 - f1_adv

    results.append({
        "Model": "1. Regex / Keyword (AutoMod)",
        "Precision": round(p, 4),
        "Recall": round(r, 4),
        "F1-Score": round(f1, 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": round(delta_f1, 4)
    })

    # --- Baseline 2: Multinomial Naive Bayes ---
    nb = MultinomialNB(alpha=0.5)
    nb.fit(X_train_tfidf, y_train)
    y_pred_nb = nb.predict(X_test_tfidf)
    y_adv_nb = nb.predict(X_adv_tfidf)

    p = precision_score(y_test, y_pred_nb, zero_division=0)
    r = recall_score(y_test, y_pred_nb, zero_division=0)
    f1 = f1_score(y_test, y_pred_nb, zero_division=0)
    f1_adv = f1_score(y_adv, y_adv_nb, zero_division=0)

    results.append({
        "Model": "2. Naive Bayes (TF-IDF)",
        "Precision": round(p, 4),
        "Recall": round(r, 4),
        "F1-Score": round(f1, 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": round(f1 - f1_adv, 4)
    })
    joblib.dump(nb, os.path.join(MODELS_DIR, "naive_bayes.joblib"))

    # --- Baseline 3: Logistic Regression ---
    lr = LogisticRegression(max_iter=1000, C=2.0, random_state=42)
    lr.fit(X_train_tfidf, y_train)
    y_pred_lr = lr.predict(X_test_tfidf)
    y_adv_lr = lr.predict(X_adv_tfidf)

    p = precision_score(y_test, y_pred_lr, zero_division=0)
    r = recall_score(y_test, y_pred_lr, zero_division=0)
    f1 = f1_score(y_test, y_pred_lr, zero_division=0)
    f1_adv = f1_score(y_adv, y_adv_lr, zero_division=0)

    results.append({
        "Model": "3. Logistic Regression (TF-IDF)",
        "Precision": round(p, 4),
        "Recall": round(r, 4),
        "F1-Score": round(f1, 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": round(f1 - f1_adv, 4)
    })
    joblib.dump(lr, os.path.join(MODELS_DIR, "logistic_regression.joblib"))

    # --- Baseline 4: LinearSVC ---
    lsvc = LinearSVC(C=1.0, random_state=42, max_iter=2000)
    lsvc.fit(X_train_tfidf, y_train)
    y_pred_lsvc = lsvc.predict(X_test_tfidf)
    y_adv_lsvc = lsvc.predict(X_adv_tfidf)

    p = precision_score(y_test, y_pred_lsvc, zero_division=0)
    r = recall_score(y_test, y_pred_lsvc, zero_division=0)
    f1 = f1_score(y_test, y_pred_lsvc, zero_division=0)
    f1_adv = f1_score(y_adv, y_adv_lsvc, zero_division=0)

    results.append({
        "Model": "4. LinearSVC (TF-IDF)",
        "Precision": round(p, 4),
        "Recall": round(r, 4),
        "F1-Score": round(f1, 4),
        "Adversarial F1": round(f1_adv, 4),
        "Delta F1 (Drop)": round(f1 - f1_adv, 4)
    })
    joblib.dump(lsvc, os.path.join(MODELS_DIR, "linear_svc.joblib"))

    df_res = pd.DataFrame(results)
    print("\nBaseline Results on Clean and Adversarial Test Sets:")
    print(df_res.to_string(index=False))

    return df_res


if __name__ == "__main__":
    train_and_eval_baselines()
