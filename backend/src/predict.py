"""
Inference script for Discord Scam Detection.
Accepts any raw Discord message, extracts all 17 payload & evasion features,
runs the trained XGBoost Fused model, and outputs a risk verdict with feature attribution.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

# Reconfigure stdout for UTF-8 on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def load_model_pipeline():
    extractor_path = os.path.join(MODELS_DIR, "feature_extractor.joblib")
    model_path = os.path.join(MODELS_DIR, "xgboost_fused.joblib")

    if not os.path.exists(extractor_path) or not os.path.exists(model_path):
        raise FileNotFoundError("Trained models not found. Run train_baselines.py and train_xgboost.py first.")

    extractor = joblib.load(extractor_path)
    model = joblib.load(model_path)
    return extractor, model


def predict_message(text, extractor=None, model=None):
    if extractor is None or model is None:
        extractor, model = load_model_pipeline()

    # 1. Extract heuristics
    heuristics = extractor.extract_heuristics_single(text)
    feature_dict = dict(zip(extractor.feature_names, heuristics))

    # 2. Extract fused features
    X_fused = extractor.transform_fused([text])

    # 3. Model inference
    proba = model.predict_proba(X_fused)[0]
    scam_prob = float(proba[1])

    # 4. Determine Verdict
    if scam_prob >= 0.80:
        verdict = "MALICIOUS SCAM"
        action = "AUTO-DELETE & BAN SENDER"
    elif scam_prob >= 0.50:
        verdict = "SUSPICIOUS / ELEVATED RISK"
        action = "FLAG FOR MODERATOR REVIEW"
    else:
        verdict = "SAFE / CLEAN"
        action = "ALLOW MESSAGE"

    return {
        "text": text,
        "scam_probability": round(scam_prob, 4),
        "verdict": verdict,
        "recommended_action": action,
        "extracted_heuristics": feature_dict
    }


def demo_test_cases():
    extractor, model = load_model_pipeline()

    test_messages = [
        # Benign chat
        "hey anyone want to play valorant tonight? we need one more for competitive",
        # Benign with legit link
        "check out this funny cat video on youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        # Classic Nitro blast with typosquat
        "@everyone Steam is giving away free Discord Nitro! Claim here: https://discoord-app.com/free",
        # Modern game tester scam
        "Hey bro, me and my team made an indie game on steam/itch, could you test the demo build and tell me if it launches? https://game-alpha-build.xyz/demo.zip",
        # Adversarial evasive scam with homoglyphs and markdown mask
        "Fr33 N1tr0 gіft fоr еvеryоnе! Сlісk [https://discord.com/nitro](https://dlscord-drop.xyz/claim)",
    ]

    print("=" * 75)
    print("LIVE DISCORD SCAM CLASSIFIER INFERENCE DEMO")
    print("=" * 75)

    for i, msg in enumerate(test_messages, 1):
        res = predict_message(msg, extractor, model)
        print(f"\n[Test Case {i}]")
        print(f"Message:   {res['text']}")
        print(f"Verdict:   {res['verdict']} (Confidence: {res['scam_probability'] * 100:.1f}%)")
        print(f"Action:    {res['recommended_action']}")
        h = res["extracted_heuristics"]
        print("Key Flags: ", end="")
        flags = []
        if h["has_url"]: flags.append(f"has_url={h['num_urls']}")
        if h["min_levenshtein_discord"] < 10: flags.append(f"discord_edit_dist={int(h['min_levenshtein_discord'])}")
        if h["is_known_bad_domain"]: flags.append("KNOWN_THREAT_DOMAIN")
        if h["has_markdown_mask"]: flags.append("MARKDOWN_LINK_MASK")
        if h["homoglyph_count"] > 0: flags.append(f"homoglyphs={int(h['homoglyph_count'])}")
        if h["urgency_token_count"] > 0: flags.append(f"urgency_keywords={int(h['urgency_token_count'])}")
        print(", ".join(flags) if flags else "None (Normal text)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        res = predict_message(msg)
        print(json.dumps(res, indent=2))
    else:
        demo_test_cases()
