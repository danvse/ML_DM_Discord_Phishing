# 🛡️ Dual-Stream Detection of Discord Phishing Campaigns

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.1%2B-EB5424.svg)](https://xgboost.readthedocs.io/)
[![Angular 18](https://img.shields.io/badge/Angular-18-DD0031.svg)](https://angular.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Machine Learning & Data Mining (Fall 2026) — Final Project (Phase 3)**  
> **Team #18:** Edwin Lin, Tin Chak Lam

---

## 📌 Executive Summary

Modern cybercriminals exploit Discord's semi-private server topology and direct messages (DMs) through lateral account compromises. Once an account is hijacked via session token theft, attackers blast malicious lures (fake Discord Nitro giveaways, indie game beta tests containing infostealers, community tournament voting traps) to mutual servers and friends lists who inherently trust the sender.

Existing defenses—such as Discord AutoMod and community moderation bots (MEE6, Dyno)—rely on static keyword blocklists and regular expressions. These deterministic filters suffer an **empirical 37.2% F1 collapse (0.8598 &rarr; 0.4876)** when challenged by basic evasion tricks like Cyrillic homoglyph substitution (`'о'` U+043E instead of ASCII `'o'`) and Markdown URL cloaking (`[discord.com/nitro](https://phishing.xyz)`).

This project presents a **lightweight, privacy-preserving dual-stream machine learning architecture** combining high-pressure semantic cues with structural payload invariants, achieving **0.9780 F1 under evasion attacks** with a **1.2 ms CPU inference latency**.

```
[Raw Discord Payload]
         │
         ▼
[Snowflake Sanitization & Unicode Normalization]
         ├─────────────────────────────────────────┐
         ▼                                         ▼
   Stream A (Semantic)                       Stream B (Structural)
 3,000 TF-IDF Word N-Grams                 17 Domain & Payload Heuristics
 (Sublinear TF Scaling)                    (Levenshtein, Shannon Entropy,
                                            Homoglyph & Markdown Counters)
         │                                         │
         └────────────────────┬────────────────────┘
                              ▼
           [Horizontal Feature Stacking: X ∈ ℝ³⁰¹⁷]
                              ▼
            [XGBoost Gradient-Boosted Trees]
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
     P < 0.50            0.50 ≤ P < 0.80        P ≥ 0.80
  [PASS / BENIGN]      [MOD REVIEW FLAGGED]  [AUTO-QUARANTINE]
```

---

## 🔬 Key Empirical Results

### 1. Model Robustness Benchmark (Clean vs. Adversarial Evasion)

| Model Architecture | Features / Representation | Clean Recall | Clean F1 | Adversarial Recall | Adversarial F1 | CPU Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **AutoMod Regex** | Static Keywords & URL Regex | 0.7753 | 0.8598 | 0.3258 | 0.4876 | **< 0.1 ms** |
| **Multinomial Naive Bayes** | 3,000 TF-IDF N-Grams | 0.9438 | 0.9600 | 0.4888 | 0.6541 | 0.8 ms |
| **Logistic Regression** | 3,000 TF-IDF N-Grams | 0.9607 | 0.9716 | 0.4494 | 0.6178 | 0.9 ms |
| **Linear SVM** | 3,000 TF-IDF N-Grams | 0.9663 | 0.9745 | 0.4438 | 0.6124 | 0.9 ms |
| **Random Forest** | Dual-Stream Fused ($\mathbb{R}^{3017}$) | 0.9494 | 0.9657 | 0.6517 | 0.7811 | 3.4 ms |
| **XGBoost (Unhardened)** | Dual-Stream Fused ($\mathbb{R}^{3017}$) | 0.9663 | 0.9772 | 0.6854 | 0.8078 | **1.2 ms** |
| **XGBoost (Hardened)** | **Dual-Stream Fused + Minimax Augmentation** | **0.9775** | **0.9780** | **1.0000\*** | **0.9780** | **1.2 ms** |

*\*Note on 100% Recall:* Evaluated and audited with 5-fold cross-validation ($0.9888 \pm 0.0112$ recall, $0.9780 \pm 0.0094$ F1) confirming stability while identifying synthetic generator overlap on closed attack distributions (detailed in Section IV of the final report).

### 2. Feature Stream Ablation Study

| Feature Configuration | Input Dimension | Clean F1 | Adversarial Recall | Adversarial F1 | Resilience Drop ($\Delta$ F1) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Stream A Alone (TF-IDF)** | 3,000 | 0.9589 | 0.4944 | 0.6331 | **-34.0%** |
| **Stream B Alone (Heuristics)** | 17 | 0.9636 | 0.6573 | 0.7748 | **-19.6%** |
| **Dual-Stream Fused (A + B)** | **3,017** | **0.9777** | **0.6854** | **0.8078** | **-17.4%** |
| **Dual-Stream Fused + Hardened**| **3,017** | **0.9780** | **1.0000** | **0.9780** | **0.0%** |

---

## 📁 Repository Structure

```
ML_DM/
├── backend/
│   ├── data/
│   │   ├── processed/              # Stratified splits (train, val, test, adversarial)
│   │   └── raw/                    # Raw HuggingFace spam & 21,908 malicious domains
│   ├── models/
│   │   ├── feature_extractor.joblib
│   │   ├── feature_extractor_hardened.joblib
│   │   ├── xgboost_fused.joblib
│   │   └── xgboost_hardened.joblib
│   ├── src/
│   │   ├── api.py                  # FastAPI microservice for real-time inference & SHAP
│   │   ├── app.py                  # Streamlit reference dashboard
│   │   ├── feature_extractor.py    # 17-feature structural extraction engine
│   │   ├── train_xgboost.py        # Fused XGBoost & Random Forest trainer
│   │   ├── adversarial_trainer.py  # Minimax adversarial hardening pipeline
│   │   ├── train_baselines.py      # Baseline models benchmark runner
│   │   ├── ablation_study.py       # 3-way feature ablation experiment runner
│   │   ├── data_loader.py          # Data ingestion, MD5 deduplication & mutation
│   │   ├── evaluate.py             # Evaluation & metric generation routines
│   │   ├── explainability.py       # SHAP TreeExplainer wrapper
│   │   └── predict.py              # CLI batch inference utility
│   └── requirements.txt            # Pinned Python package dependencies
│
├── frontend/                       # Modern Angular 18 Enterprise UI
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/         # Classifier, Analytics Workbench & Popout Chat
│   │   │   └── services/           # HTTP API client connecting to FastAPI backend
│   │   └── index.html
│   ├── package.json
│   └── angular.json
│
├── docs/                           # Academic papers, presentations & scripts
│   ├── reports/
│   │   ├── Final_Project_Report_Discord_Scam_Detection_IEEE.pdf   # 6-page IEEE Final Report
│   │   ├── Final_Project_Report_Discord_Scam_Detection_IEEE.docx  # Formatted Word Document
│   │   └── Edwin_Lin_Tin_Chak_Lam_Mid.pdf                         # Midterm Report
│   └── slides/
│       ├── DEMO_PRESENTATION_SLIDES.pptx                          # 10-slide PowerPoint Deck
│       ├── DEMO_PRESENTATION_SLIDES.html                          # Interactive HTML5 Deck
│       ├── DEMO_VIDEO_PRESENTATION_SCRIPT.md                      # 20-min Spoken Video Script
│       ├── DEMO_VIDEO_PRESENTATION_SCRIPT.docx                    # Formatted Word Script
│       └── slides_assets/                                         # Embedded visual cards & screenshots
│
├── .gitignore                      # Clean repository ignore rules
└── README.md                       # Project documentation & setup guide
```

---

## 🚀 Quickstart & Setup Guide

### Prerequisites
- **Python:** 3.10, 3.11, 3.12, or 3.14
- **Node.js:** v18.0+ or v20.0+ (with `npm`)

---

### 1. Backend Setup (FastAPI & ML Inference)

1. Open a terminal and navigate into the `backend/` directory:
   ```bash
   cd backend
   ```

2. *(Recommended)* Create and activate a Python virtual environment:
   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the FastAPI backend server:
   ```bash
   uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
   ```
   - **Interactive API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **Health Check:** `GET http://127.0.0.1:8000/api/health`

---

### 2. Frontend Setup (Angular 18 Enterprise Portal)

1. Open a second terminal window and navigate into the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Angular development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to:
   👉 **[http://localhost:4200/](http://localhost:4200/)**

The application will load with:
- **Interactive Classifier:** Test benign chat, classic Nitro lures, Cyrillic homoglyph bypasses, and Markdown disguises with sub-2ms latency counters and SHAP feature attribution.
- **Analytics Workbench:** View model comparisons, ROC curves, and ablation tables.
- **Pop-Out Chat Playground:** Test simulated Discord multi-turn messaging with inline quarantine banners.

---

### 3. Reproducing Experimental Benchmarks

All ML training and ablation experiments can be re-run with reproducible seeds (`random_state=42`):

```bash
cd backend

# 1. Ingest threat feeds, deduplicate with MD5, and build train/val/test splits
python src/data_loader.py

# 2. Train baseline models (AutoMod regex, Naive Bayes, Logistic Regression, SVM)
python src/train_baselines.py

# 3. Train fused XGBoost and Random Forest models
python src/train_xgboost.py

# 4. Run Minimax Adversarial Training & Hardening
python src/adversarial_trainer.py

# 5. Run 3-Way Feature Ablation Study (Stream A vs. Stream B vs. Fused)
python src/ablation_study.py
```

Generated metric tables and CSVs are saved to `backend/data/processed/`.

---

## 📑 Course Deliverables & Documentation

All deliverables for the **Phase 3 Final Submission** are organized in `docs/`:

- **IEEE Technical Report (20% Course Grade):**
  - PDF: [`docs/reports/Final_Project_Report_Discord_Scam_Detection_IEEE.pdf`](docs/reports/Final_Project_Report_Discord_Scam_Detection_IEEE.pdf)
  - Word: [`docs/reports/Final_Project_Report_Discord_Scam_Detection_IEEE.docx`](docs/reports/Final_Project_Report_Discord_Scam_Detection_IEEE.docx)
- **Demo Video Presentation Slides:**
  - PowerPoint (16:9 Widescreen): [`docs/slides/DEMO_PRESENTATION_SLIDES.pptx`](docs/slides/DEMO_PRESENTATION_SLIDES.pptx)
  - Interactive HTML5 Deck: [`docs/slides/DEMO_PRESENTATION_SLIDES.html`](docs/slides/DEMO_PRESENTATION_SLIDES.html)
- **Spoken Demo Script (~20-Minute Target):**
  - Markdown: [`docs/slides/DEMO_VIDEO_PRESENTATION_SCRIPT.md`](docs/slides/DEMO_VIDEO_PRESENTATION_SCRIPT.md)
  - Word: [`docs/slides/DEMO_VIDEO_PRESENTATION_SCRIPT.docx`](docs/slides/DEMO_VIDEO_PRESENTATION_SCRIPT.docx)

---

## 👥 Authors & Contributions

**Team #18 (Machine Learning & Data Mining - Fall 2026):**
- **Edwin Lin** (`50% contribution`): Feature engineering, Levenshtein DP optimization, AutoMod baseline failure simulation, adversarial dataset perturbation pipeline, and full-stack Angular 18 UI integration.
- **Tin Chak Lam** (`50% contribution`): XGBoost hyperparameter tuning, minimax adversarial training implementation, SHAP TreeExplainer integration, statistical evaluation, and benchmark ablation studies.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
