# Project Sources & Execution Guide
**Course:** Machine Learning & Data Mining (Fall 2026)  
**Project Title:** Dual-Stream Detection of Discord Phishing Campaigns  
**Author / Presenter:** Edwin Lin (Team #18 — Solo Project)  

---

## 📋 System Requirements & Version Information

This project has been tested and verified across modern operating systems. The software environments and version specifications required to execute the pipeline and full-stack application are detailed below:

| System / Component | Minimum Version | Recommended / Tested Version | Purpose in Project |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11, macOS 12+, or Ubuntu 20.04+ LTS | **Windows 11 (64-bit)** / Ubuntu 22.04 LTS | Host operating system environment |
| **Python** | Python 3.10.x | **Python 3.12.x – 3.14.0** | Machine learning pipeline, feature extraction, FastAPI backend |
| **Node.js** | Node.js v18.13.0 LTS | **Node.js v20.18.0 LTS** | Angular 18 build tools and frontend development runtime |
| **npm (Node Package Mgr)**| npm 9.0.0 | **npm 10.8.2+** | Frontend package resolution and dependency installation |
| **Angular CLI** | `@angular/cli@18.0.0` | **`@angular/cli@18.2.11`** | Angular standalone component development server |
| **Web Browser** | Any modern evergreen browser | **Google Chrome (v120+)**, Microsoft Edge (v120+), Firefox (v120+) | Web application dashboard and simulated chatbox interface |
| **Hardware** | 4 GB RAM, Dual-core x86_64 or ARM64 CPU | 8 GB RAM, Quad-core CPU | Inference runs in **1.2 ms on CPU** (no GPU required) |

---

## 📦 Directory Structure of `Sources/`

```text
Sources/
├── backend/                        # Backend API & Machine Learning Engine
│   ├── data/                       # Datasets & Processed Corpus
│   │   ├── raw/                    # Raw Hugging Face & threat feeds
│   │   └── processed/              # Cleaned, MD5-deduplicated 3,552 messages
│   ├── models/                     # Saved model artifacts (.joblib, .json)
│   │   ├── xgboost_hardened.joblib # Production hardened XGBoost model (0.9780 F1)
│   │   ├── tfidf_vectorizer.joblib # 3,000-dimensional TF-IDF word feature extractor
│   │   └── scaler.joblib           # StandardScaler for 17 structural features
│   ├── src/                        # Core Python Source Code
│   │   ├── api.py                  # FastAPI REST service & CORS middleware
│   │   ├── data_loader.py          # Data ingestion, threat feeds & MD5 deduplication
│   │   ├── feature_extractor.py    # 17 engineered structural link domain invariants
│   │   ├── train_baselines.py      # Table I: AutoMod regex, Naive Bayes, LogReg, SVM
│   │   ├── train_xgboost.py        # Table I: Fused XGBoost & Random Forest training
│   │   ├── ablation_study.py       # Table II: 3-way feature ablation (Words vs. Structure)
│   │   └── adversarial_trainer.py  # Table III: Minimax adversarial hardening & 5-fold CV
│   ├── requirements.txt            # Python pip dependencies
│   └── run_showcase_pipeline.py    # Standalone showcase script within backend
│
├── frontend/                       # Angular 18 Web Application Portal
│   ├── src/
│   │   ├── app/                    # Angular Standalone Components & UI Services
│   │   │   ├── app.ts              # Main controller & Chart.js graph rendering
│   │   │   ├── app.html            # 5-tab dashboard & floating chatbox template
│   │   │   ├── app.css             # Responsive styling & dark theme
│   │   │   └── services/           # HTTP communication with FastAPI backend
│   │   ├── index.html              # Single page entry HTML
│   │   └── main.ts                 # Angular application bootstrap
│   ├── package.json                # Frontend dependencies & npm scripts
│   ├── angular.json                # Angular 18 workspace configuration
│   └── tsconfig.json               # TypeScript compiler configuration
│
├── run_showcase_pipeline.py        # Master 17-second ML showcase script (root launcher)
├── run_showcase.bat                # 1-Click Windows Batch Executable for Showcase Pipeline
├── run_showcase.sh                 # 1-Click Unix/macOS Shell Script for Showcase Pipeline
├── start_backend.bat               # 1-Click Windows Executable to Start FastAPI (Port 8000)
├── start_backend.sh                # 1-Click Unix/macOS Executable to Start FastAPI (Port 8000)
├── start_frontend.bat              # 1-Click Windows Executable to Start Angular 18 (Port 4200)
├── start_frontend.sh               # 1-Click Unix/macOS Executable to Start Angular 18 (Port 4200)
└── README.md                       # This comprehensive execution guide
```

---

## 🚀 Step-by-Step Instructions on How to Run

You can run the project in two ways:
1. **Option A (Fast Track — 17s Showcase Pipeline):** Run the end-to-end machine learning pipeline directly in the terminal to reproduce all paper results, benchmarks, and ablation experiments.
2. **Option B (Full-Stack Web Application):** Start the FastAPI backend and Angular 18 frontend to interact with the live web dashboard and pop-out chatbox.

---

### Option A: Running the Master Showcase Pipeline (Recommended for Grading)

This single command executes the entire machine learning lifecycle from start to finish in approximately **17 seconds**:
1. Data Ingestion & MD5 Deduplication (6,000 raw samples $\rightarrow$ 3,552 unique messages).
2. Baseline Benchmarks (Table I: AutoMod regex, Naive Bayes, Logistic Regression, SVM).
3. Dual-Stream Tree Ensembles (Random Forest vs. XGBoost).
4. 3-Way Feature Ablation Analysis (Table II: Text alone vs. Link Structure alone).
5. Minimax Adversarial Hardening (Table III: 0.9780 F1 recovery and 5-fold cross-validation).
6. Final Executive Summary Scorecard.

#### On Windows:
Double-click `run_showcase.bat`, or run from PowerShell / Command Prompt:
```powershell
# Navigate to Sources folder
cd Sources

# Run with python launcher (or python)
py run_showcase_pipeline.py
# or
python run_showcase_pipeline.py
```

#### On Linux / macOS:
```bash
cd Sources
chmod +x run_showcase.sh
./run_showcase.sh
# or directly:
python3 run_showcase_pipeline.py
```

---

### Option B: Running the Full-Stack Web Application

To run the interactive web interface, launch the **Backend** and **Frontend** in two separate terminal windows.

#### Step 1: Install Python Dependencies & Start FastAPI Backend
1. Open a terminal and navigate to `Sources/backend`:
   ```powershell
   cd Sources/backend
   ```
2. Install the required Python packages:
   ```powershell
   py -m pip install -r requirements.txt
   # or
   pip install -r requirements.txt
   ```
3. Start the FastAPI backend server:
   ```powershell
   py -m uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
   ```
   *(Or on Windows, simply double-click `start_backend.bat`)*
4. Verify the backend is active:
   - Backend API URL: `http://127.0.0.1:8000`
   - Interactive Swagger API Docs: `http://127.0.0.1:8000/docs`
   - Healthcheck: Visiting `http://127.0.0.1:8000/health` should return `{"status":"healthy","model_loaded":true}`.

#### Step 2: Install Node Dependencies & Start Angular 18 Frontend
1. Open a **second terminal** and navigate to `Sources/frontend`:
   ```powershell
   cd Sources/frontend
   ```
2. Install the frontend dependencies:
   ```powershell
   npm install
   ```
3. Start the Angular development server:
   ```powershell
   npx ng serve --host 127.0.0.1 --port 4200
   ```
   *(Or on Windows, simply double-click `start_frontend.bat`)*
4. Access the web application:
   - Open your browser to: **`http://localhost:4200/`**

---

## 🖥️ Using the Angular 18 Web Interface

Once `http://localhost:4200/` loads in your browser, you can explore the following functions:

1. **Inference Playground (Main Tab):**
   - Click the preset button **"Clean Gaming Chat"**: Notice inference takes ~1.1 ms and outputs a green **APPROVED** badge (0.02% risk).
   - Click **"Classic Nitro Scam"**: Notice it turns bright red with an **AUTO-QUARANTINE** verdict (99.85% risk).
   - Click **"Cyrillic Homoglyph Attack"**: Notice that while traditional regex filters miss the Russian lookalike `'і'` in `dіscord.com`, our model catches it at 99.42% risk!
   - View the **SHAP Feature Attribution** chart below the input box to see the exact green/red bars explaining the decision.
2. **Pop-Out Chatbox (Floating Button in Bottom-Right):**
   - Click the floating chat icon in the bottom-right corner to open the simulated Discord chat window.
   - Send normal messages to see clean delivery.
   - Paste a malicious link (e.g. `https://steamcommunity-beta.top/setup.exe`) to observe instant **1.2 ms red auto-quarantine overlay** blocking the link from rendering clickable.
3. **Architecture & Benchmark Tabs:**
   - Explore the **Architecture & SOTA**, **Training Dynamics**, and **Empirical Benchmarks** tabs in the left sidebar to view the interactive radar chart, loss convergence curves, and ablation tables.

---

## 🔬 Running Individual Python Research Scripts

If you wish to run the individual machine learning experiments separately:

| Script | Purpose | Command (from `Sources/backend`) | Output Artifacts |
| :--- | :--- | :--- | :--- |
| `data_loader.py` | Ingests threat feeds & runs MD5 deduplication | `py src/data_loader.py` | `backend/data/processed/` dataset |
| `train_baselines.py` | Evaluates AutoMod, Naive Bayes, LogReg, SVM (Table I) | `py src/train_baselines.py` | Table I performance metrics |
| `train_xgboost.py` | Trains Dual-Stream XGBoost & Random Forest | `py src/train_xgboost.py` | `backend/models/xgboost_baseline.joblib` |
| `ablation_study.py` | 3-way feature ablation: Words vs. Structure (Table II) | `py src/ablation_study.py` | Table II ablation metrics |
| `adversarial_trainer.py`| Minimax hardening & 5-fold cross validation (Table III) | `py src/adversarial_trainer.py`| `backend/models/xgboost_hardened.joblib` |

---

## 🛠️ Troubleshooting & Common Setup Notes

1. **Windows Python App Execution Alias (`python` command not found):**
   - On Windows 10/11, typing `python` may open the Microsoft Store shortcut if Python execution aliases are enabled.
   - **Fix:** Use the official Python launcher command **`py`** (e.g., `py run_showcase_pipeline.py`), or disable the Microsoft Store alias in *Windows Settings > Apps > Advanced app settings > App execution aliases*.
2. **Port Conflicts (Port 8000 or 4200 already in use):**
   - If port 8000 is occupied, you can launch the backend on another port:
     `py -m uvicorn src.api:app --port 8001`
   - If port 4200 is occupied, launch Angular on another port:
     `npx ng serve --port 4201`
3. **Node.js Memory / Permission Errors:**
   - Ensure Node.js is at least v18.13.0 LTS (`node -v`).
   - Run terminal as standard user (administrative privileges are not required).

---

## 👤 Author & Academic Integrity

- **Author / Developer:** Edwin Lin
- **Team:** Team #18 (100% Solo Contribution)
- **Course:** Machine Learning & Data Mining (Fall 2026)
- **Compliance:** Built strictly from public research datasets and threat feeds in full compliance with Discord Developer Policy Section 21. No private user chat logs were collected.
