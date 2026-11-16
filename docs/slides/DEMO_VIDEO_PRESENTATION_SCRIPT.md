# 20-Minute Final Project Demo Video Presentation Script

**Project Title:** Dual-Stream Detection of Discord Phishing Campaigns Using Words and Link Structure  
**Course:** Machine Learning & Data Mining (Fall 2026)  
**Team #18:** Edwin Lin, Tin Chak Lam  
**Target Video Duration:** ~20 Minutes (18:00 – 22:00)  
**Video Setup Checklist:**
- [x] Webcam active in the top-right or bottom-right corner throughout the entire recording.
- [x] Microphone tested for clear audio with no background hum.
- [x] Terminal open in workspace: `c:\Users\Dan\Downloads\ML_DM`.
- [x] FastAPI backend running on `http://127.0.0.1:8000`.
- [x] Angular frontend running on `http://localhost:4200`.
- [x] Browser tabs arranged: (1) Angular App, (2) FastAPI `/docs` Swagger UI, (3) VS Code / Terminal.

---

## Complete Video Timeline & Section Breakdown

| Segment | Video Timestamp | Content & Focus | On-Screen Action |
| :---: | :---: | :--- | :--- |
| **1** | **0:00 – 2:30** | Introduction, Threat Landscape & Motivation | Presenter on camera + Slide / Architecture diagram |
| **2** | **2:30 – 5:30** | System Architecture & Mathematical Models | Slide / Code: Dual-Stream Flow, Levenshtein, Shannon Entropy, Minimax |
| **3** | **5:30 – 8:30** | Data Engineering, Threat Feeds & Feature Extraction | VS Code & Terminal: `data_loader.py`, deduplication, `feature_extractor.py` |
| **4** | **8:30 – 12:00** | Baselines, Ablation Study & Adversarial Hardening | Terminal runs: `train_baselines.py`, `ablation_study.py`, `adversarial_trainer.py` |
| **5** | **12:00 – 17:30** | Full Live Interactive Application Demonstration | Browser: `http://localhost:4200/` (Presets, SHAP, Pop-Out Chat, Latency) |
| **6** | **17:30 – 20:00** | Project Post-Mortem, Lessons Learned & Conclusion | Camera + Summary: Discord Bot API sandboxing pivot, wrap-up |

---

## Detailed Spoken Script & Screen Action Prompts

---

### Segment 1: Introduction, Threat Context & Motivation (0:00 – 2:30)

**[ON SCREEN: Presenter webcam visible in corner. Main screen displays project title card or introductory overview slide showing Discord interface with typical scam messages.]**

> **[0:00 – 0:45] Spoken Dialogue:**  
> "Hello everyone, and welcome to our final project demonstration for Machine Learning and Data Mining. My name is [Your Name], representing Team #18 alongside my project partner [Partner Name]. Today, we're presenting our project: **Dual-Stream Detection of Discord Scam and Phishing Messages Using Semantic and Structural Invariants**.  
>  
> Over the next twenty minutes, I will walk you through the problem we tackled, the engineering architecture we developed, our experimental evaluations across multiple baseline models, and a live demonstration of our production-ready web application and moderation engine."

> **[0:45 – 1:45] Spoken Dialogue:**  
> "To understand why we built this system, let's look at Discord's unique security threat model. Discord has over 200 million monthly active users across gaming, university study groups, and open-source software communities. Unlike public platforms like Twitter or Reddit where spam is broadcast publicly and quickly flagged by the community, Discord is built around closed servers and private Direct Messages (DMs).  
>  
> When an attacker steals an account—typically using an infostealer malware like RedLine or a fake QR code login page—automated scripts immediately weaponize that account. The script scrapes the victim's friends list and active servers, blasting identical lure messages to mutual contacts. Because users naturally trust incoming messages from their friends, click-through rates on Discord scams are notoriously high."

> **[1:45 – 2:30] Spoken Dialogue:**  
> "Server administrators usually try to block these attacks using Discord AutoMod or community bots like MEE6 and Dyno. But almost all of these tools rely on static keyword blocklists and basic regular expressions. Scammers easily bypass them using three tricks:
> 1. **Cyrillic Homoglyphs:** Swapping English letters for visually identical Russian letters, like Cyrillic 'о' for Latin 'o'. A human sees `discord.com`, but a regex sees a completely different byte string.
> 2. **Markdown Masking:** Using syntax like `[https://discord.com/nitro](https://phishing.xyz)` so the client shows a blue, trusted link that redirects to a credential harvester.
> 3. **Casual Pretexts:** Opening with normal greetings like *'Hey, are you free to test my game?'* with zero links, waiting for a reply before dropping the payload.  
>  
> When we benchmarked Discord AutoMod against these evasion tricks, its F1-score dropped by 37.2%. That failure motivated our project: building a fast, machine-learning-based detector that looks past surface text and focuses on invariant link and structural characteristics."

---

### Segment 2: System Architecture & Mathematical Models (2:30 – 5:30)

**[ON SCREEN: Switch screen share to the System Architecture Flowchart / Diagram showing Preprocessing → Stream A (TF-IDF) & Stream B (17 Structural Features) → Concatenation (3,017 dims) → XGBoost → Action Routing.]**

> **[2:30 – 3:30] Spoken Dialogue:**  
> "Let's examine our technical architecture. When designing this system, we asked an essential engineering question: *What can an attacker change easily, and what are they forced to keep?*  
>  
> An attacker can change their words in seconds. But to steal credentials or drop malware, they **must** redirect the victim to an external domain they control. That domain is almost always newly registered, mathematically jumbled, or misspelled compared to real brands.  
>  
> Based on that insight, we designed a **Dual-Stream Feature Fusion Pipeline**:
> - **Stream A (Semantic Representation):** Converts the cleaned message body into 3,000 TF-IDF n-grams (unigrams and bigrams), capturing general social engineering language.
> - **Stream B (Structural Heuristics):** Extracts 17 engineered numerical features directly from raw text strings and embedded URLs.
>  
> We concatenate these into a single 3,017-dimensional vector and pass it to gradient-boosted decision trees using XGBoost."

> **[3:30 – 4:30] Spoken Dialogue:**  
> "A common question from reviewers is: *Why XGBoost instead of fine-tuning a deep transformer like DistilBERT or RoBERTa?*  
> We actually evaluated DistilBERT early on, and we dropped it for three practical reasons:
> 1. **CPU Latency:** DistilBERT took between 150 ms and 300 ms per message on standard CPU hardware. On an active Discord server processing dozens of chat channels, that creates an unacceptable message backlog unless you pay for expensive GPU instances. XGBoost runs in **1.2 ms** on a single CPU core.
> 2. **Subword Tokenization Fragility:** Transformer subword tokenizers (like WordPiece) break homoglyph-substituted words into disjointed, meaningless character fragments, degrading embedding quality.
> 3. **Tabular Decision Logic:** Phishing indicators have non-linear conjunctive relationships: an external URL *paired* with an edit distance $\le 2$ to `discord.com` *paired* with an elevated uppercase ratio. Decision trees partition these discontinuous rules naturally."

> **[4:30 – 5:30] Spoken Dialogue:**  
> "Now let's highlight the mathematical formulations powering Stream B:
> 1. **Minimum Levenshtein Distance ($d_{\min}$):** We calculate the dynamic programming edit distance between extracted domains and canonical platforms—`discord.com`, `discordapp.com`, and `steamcommunity.com`. To keep extraction fast, we added an early-exit optimization: if the absolute difference in string lengths exceeds 4, the edit distance is mathematically guaranteed to exceed our threshold, allowing the $O(NM)$ matrix loop to be skipped.
> 2. **Shannon Domain Entropy ($H(d)$):** Attackers frequently use automated domain generation algorithms (DGAs) or long random subdomains. We compute Shannon entropy over the domain character distribution:
>    $$H(d) = -\sum_{c \in \Sigma_d} p(c) \log_2 p(c)$$
>    Normal brand domains score between 2.0 and 2.8, while random machine-generated phishing strings score above 3.5.
> 3. **Minimax Adversarial Objective:** Instead of standard empirical risk minimization, we train the tree ensemble against worst-case perturbations $\Delta$ (homoglyphs and Markdown cloaking):
>    $$\min_{\theta} \mathbb{E}_{(x, y) \sim D} \left[ \max_{\delta \in \Delta} \mathcal{L}(f_\theta(x + \delta), y) \right]$$
>    This forces tree branches to split on structural invariants rather than brittle words."

---

### Segment 3: Codebase Walkthrough & Data Engineering (5:30 – 8:30)

**[ON SCREEN: Switch screen to VS Code. Show project directory structure, open `src/data_loader.py` and `src/feature_extractor.py`.]**

```
c:\Users\Dan\Downloads\ML_DM\
├── src/
│   ├── feature_extractor.py   <-- Open on screen
│   ├── data_loader.py         <-- Open on screen
│   ├── train_baselines.py
│   ├── train_xgboost.py
│   ├── ablation_study.py
│   ├── adversarial_trainer.py
│   ├── explainability.py
│   └── api.py
├── frontend/                  <-- Angular 18 app
└── generate_final_report.py
```

> **[5:30 – 6:45] Spoken Dialogue:**  
> "Now let's examine the implementation in our codebase. Let's look at `src/data_loader.py`.  
>  
> Gathering Discord data requires strict adherence to privacy rules. Discord Developer Policy Section 21 explicitly forbids saving user private chats for machine learning without consent. Therefore, we compiled our dataset from verified public research sources:
> 1. 2,000 verified phishing messages from the Hugging Face Discord Phishing dataset.
> 2. 21,908 malicious domains from the Nikolaischunk threat feed, mapped into realistic lure templates.
> 3. 1,500 synthetic samples modeling modern 2024–2026 attacks (OAuth token authorizations, fake indie playtests, and crypto drainers), balanced against 2,500 benign messages from open Discord gaming logs.
>  
> Here in `data_loader.py`, you can see a critical engineering step: **data deduplication**. The raw Hugging Face data had hundreds of duplicate copies of the exact same Nitro gift spam. If we had trained on that directly, the model would have memorized those specific strings, causing severe train-test data leakage. We implemented an MD5 hash and fuzzy substring filter that reduced the corpus to **3,552 unique, balanced messages**, split 80% train, 10% validation, and 10% test."

> **[6:45 – 8:00] Spoken Dialogue:**  
> "Next, let's open `src/feature_extractor.py`. This class implements our 17 structural heuristics.  
>  
> Notice this optimization at the top: all regex patterns—URL extraction, spoiler bars (`||link||`), markdown masks, user mentions, and dangerous file extensions like `.exe` and `.scr`—are compiled globally once at module load. In our early prototype, recompiling regexes inside the per-message loop caused a 15-times latency penalty. Pre-compiling brought our feature extraction down to **sub-millisecond speed**.  
>  
> Scrolling down, here is our memoized Levenshtein distance function with the early-exit length filter, followed by our Shannon entropy calculation function using `scipy.stats.entropy` and normalized character frequencies. The `transform_fused()` method takes raw text arrays and uses `scipy.sparse.hstack` to glue the 3,000 sparse TF-IDF features with the dense 17 heuristic features into our final 3,017-dimensional matrix."

> **[8:00 – 8:30] Spoken Dialogue:**  
> "Let's also look at `src/adversarial_trainer.py`. Here is our `build_adversarial_variant()` function. It takes clean scam messages and dynamically injects Cyrillic homoglyph lookalikes (`\u0430`, `\u043E`, `\u0456`), leetspeak substitutions (`fr33`, `n1tr0`), and Markdown URL disguises. This generator creates both our 356-sample adversarial evaluation set and our augmented training partition."

---

### Segment 4: Model Training, Baselines & Adversarial Hardening (8:30 – 12:00)

**[ON SCREEN: Switch to Terminal. Run verification commands and show benchmark results.]**

```powershell
& "C:\Users\Dan\AppData\Local\Python\bin\python3.14.exe" src/train_baselines.py
& "C:\Users\Dan\AppData\Local\Python\bin\python3.14.exe" src/ablation_study.py
```

> **[8:30 – 9:45] Spoken Dialogue:**  
> "Now let's run our baseline training script in the terminal. We benchmarked our system against five representative models:
> 1. **Discord AutoMod (Regex / Blocklists):** Emulating native server moderation rules.
> 2. **Multinomial Naive Bayes (TF-IDF):** Standard lightweight text classifier.
> 3. **Logistic Regression (TF-IDF):** Regularized linear baseline.
> 4. **Linear SVM (TF-IDF):** High-dimensional sparse text classifier.
> 5. **Random Forest (Fused):** Traditional ensemble on both feature streams.
> 6. **XGBoost Fused (Our Baseline):** Gradient-boosted trees on both streams.  
>  
> Look at the terminal output for Table I. On clean test data, all machine learning models score above 0.97 F1. AutoMod regex gets 0.8598 F1.  
>  
> But look what happens when we evaluate against the **adversarial evasion set**:
> - AutoMod regex collapses from 0.8598 to **0.4876 F1**—a 37.2% decrease, because regular expressions fail the moment letters are swapped.
> - Naive Bayes, Logistic Regression, and Linear SVM all drop to between 0.4494 and 0.4944 recall because homoglyph words fall completely outside their TF-IDF vocabularies.
> - Our unhardened XGBoost baseline holds up much better at **0.8078 F1** because its decision trees can still branch on the 17 structural features."

> **[9:45 – 10:45] Spoken Dialogue:**  
> "Now let's run `src/ablation_study.py` to isolate the exact value of our 17 structural heuristics.  
> In Table II, we compare:
> - **Stream A Alone (3,000 TF-IDF features):** Scores 0.9589 on clean data, but collapses to 0.4944 recall and 0.6331 F1 under attack.
> - **Stream B Alone (17 Heuristics Only):** Despite having less than 1% of the feature dimensionality, Stream B achieves 0.9636 clean F1 and **0.7748 adversarial F1**! It outperforms the text-only model by 14.1% under attack because domain edit distance and entropy don't change when message text is scrambled.
> - **Dual-Stream Fused:** Reaches 0.9777 clean F1 and 0.8078 adversarial F1 before any hardening."

> **[10:45 – 12:00] Spoken Dialogue:**  
> "Finally, let's look at **Minimax Adversarial Hardening** in Table III. We augmented 25% of training scam samples with synthetic mutations.  
>  
> After hardening, adversarial F1 rises to **0.9780**, with adversarial test recall reaching **1.0000** (catching 178 of 178 test scams).  
>  
> Now, we want to address this 100% recall with complete scientific honesty, exactly as we did in our report:  
> In machine learning, a 100% test score is usually a red flag for data contamination or closed-distribution evaluation, and that applies here. Our adversarial test set was generated using the same mutation script (`build_adversarial_variant`) used for training augmentation. Because both sets shared the same Cyrillic homoglyph mappings, XGBoost learned that `homoglyph_count >= 1` (which jumped from the #14 feature to the **#5 most important feature** in tree split gain) was a near-guarantee of a scam.  
>  
> In a real-world open deployment with zero-day attacks—like right-to-left override characters or image QR codes—recall would certainly be lower. To estimate true variance, we ran 5-fold cross-validation with randomized mutation seeds: across the 5 folds, hardened adversarial recall averaged **$0.9888 \pm 0.0112$** and F1 averaged **$0.9780 \pm 0.0094$**. This demonstrates that our structural features provide genuine resilience while maintaining realistic variance."

---

### Segment 5: Live Interactive Application Demonstration (12:00 – 17:30)

**[ON SCREEN: Switch screen to Google Chrome showing Angular 18 frontend at `http://localhost:4200/`. Presenter webcam remains in corner.]**

> **[12:00 – 13:00] Spoken Dialogue:**  
> "Now let's transition to the live system demonstration. We packaged our trained models, feature extractor, and SHAP explainability engine into a high-performance **FastAPI backend** on port 8000, connected to this **Angular 18 single-page application** running on port 4200.  
>  
> At the top of the interface, you can see our live status banner: connected to the FastAPI backend, active model `xgboost_hardened.joblib`, and an end-to-end inference latency badge currently reporting **1.2 milliseconds**.  
>  
> Let's test the detector across several real-world test cases using our interactive workbench."

#### Demo Test Case 1: Clean Benign Message
**[ACTION: Click the 'Clean Gaming Chat' preset button or type: *"Hey man, are we still hopping on Valorant tonight? Let me know when you're online."* Click Analyze.]**

> **[13:00 – 13:45] Spoken Dialogue:**  
> "Let's start with a normal, benign Discord message: *'Hey man, are we still hopping on Valorant tonight?'*  
> When I click Analyze, the backend extracts all 3,017 features and runs inference in 1.1 milliseconds.  
>  
> Look at the results card:
> - **Predicted Class:** BENIGN (Green Badge).
> - **Scam Probability:** 0.02% (Essentially zero).
> - **Decision Routing:** Approved for immediate delivery.
> - **Structural Features Card:** `has_url = 0`, `homoglyph_count = 0`, `urgency_token_count = 0`.
> - **SHAP Explanation Bars:** Shows negative attribution—the absence of URLs and standard conversational vocabulary actively push the prediction towards benign."

#### Demo Test Case 2: Classic Unmutated Nitro Scam
**[ACTION: Click the 'Classic Nitro Scam' preset: *"@everyone Steam is giving away 3 months of Discord Nitro for free! Claim your gift here: https://discord-nitro-gift.ru/claim"* Click Analyze.]**

> **[13:45 – 14:30] Spoken Dialogue:**  
> "Now let's test a classic unmutated scam message. This simulates a compromised account blasting a free Nitro gift link.  
>  
> Let's click Analyze:
> - **Predicted Class:** SCAM (Red Badge).
> - **Scam Probability:** 99.85%.
> - **Decision Routing:** AUTO-QUARANTINE (Score $\ge 0.80$).
> - **Extracted Heuristics:**
>   - `min_levenshtein_discord = 1` (Detecting `discord-nitro-gift` vs `discord.com`).
>   - `suspicious_tld = 1` (Flagging `.ru`).
>   - `urgency_token_count = 3` (`free`, `nitro`, `gift`).
>   - `mention_count = 1` (`@everyone`).
>  
> The SHAP waterfall chart clearly shows `min_levenshtein_discord` and `urgency_token_count` providing massive positive attribution towards the scam classification."

#### Demo Test Case 3: Tricky Cyrillic Homoglyph Attack (The AutoMod Evasion)
**[ACTION: Click 'Cyrillic Homoglyph Attack' preset: *"Steam partnership: claim complimentary subscription at https://dіscord.com/gifts (Note: 'і' is Cyrillic U+0456)"* Click Analyze.]**

> **[14:30 – 15:30] Spoken Dialogue:**  
> "Now here is the critical test case that breaks standard filters. Look closely at the domain: to your eyes, it looks identical to `https://discord.com/gifts`. But the letter 'i' is actually Unicode character U+0456 from the Cyrillic alphabet.  
>  
> Standard Discord AutoMod regex looks for ASCII `discord.com` and **completely misses this**.  
>  
> Let's hit Analyze with our model:
> - **Predicted Class:** SCAM!
> - **Scam Probability:** 99.42%!
> - Look at the structural inspection card:
>   - `homoglyph_count = 1` (Highlighted in amber).
>   - `min_levenshtein_discord = 1`.
>   - `urgency_token_count = 2`.  
>  
> Because our model was trained with minimax adversarial augmentation, our decision trees learned that any message combining a lookalike platform domain with a non-zero `homoglyph_count` is an evasion attack. It intercepts the scam effortlessly."

#### Demo Test Case 4: Markdown Link Masking
**[ACTION: Click 'Markdown Link Cloaking' preset: *"[https://discord.com/nitro](https://grabify-token-stealer.xyz/auth)"* Click Analyze.]**

> **[15:30 – 16:15] Spoken Dialogue:**  
> "Next, let's test Markdown link masking. In the Discord chat UI, writing bracketed markdown shows blue trusted text `https://discord.com/nitro`, but clicking it redirects to `grabify-token-stealer.xyz`.  
>  
> Let's analyze it:
> - **Predicted Class:** SCAM (99.78% Probability).
> - **Feature Breakdown:** `spoiler_mask_count = 1`, `suspicious_tld = 1` (`.xyz`), and `domain_entropy = 3.62`.  
> Even though the visible anchor text purports to be official Discord, the parser evaluates the true destination URI, protecting users from deceptive redirects."

#### Demo Test Case 5: Interactive Chatbox Pop-Out Dialog
**[ACTION: Click the floating 'Chat Playground' button in the bottom right corner. The interactive pop-out chatbox dialog opens smoothly.]**

> **[16:15 – 17:30] Spoken Dialogue:**  
> "To test how this operates in a simulated Discord chat environment, we built this interactive **Pop-Out Chat Playground**.  
>  
> As you can see, I can click this floating action button to pop out an inline chat dialog. Let's type a multi-turn conversation:
> 1. *'Hey bro, are you working on the ML project right now?'* -> Model scores 0.04% (Clean chat badge).
> 2. Now let's simulate the compromised bot replying with a fake game test: *'Yeah! By the way, my team just released our beta demo on Steam, can you download and test it? https://steamcommunity-beta-build.top/setup.exe'*
>  
> I hit enter. Instantly—in 1.2 milliseconds—the chatbox flags the message in bright red with an **AUTO-QUARANTINED** overlay, preventing the malicious link from rendering clickable in chat.  
>  
> You can also see the pop-out can be minimized, expanded, or closed, providing server moderators with an intuitive live inspection environment."

---

### Segment 6: Project Post-Mortem, Lessons Learned & Conclusion (17:30 – 20:00)

**[ON SCREEN: Switch screen back to presenter camera and summary slides.]**

> **[17:30 – 18:30] Spoken Dialogue:**  
> "Before concluding, I want to discuss our **Architectural Post-Mortem and Failures**, which is a crucial part of our learning outcomes.  
>  
> When Edwin and I started this project in September, our original proposal was very different: we planned to build a Discord bot that evaluated sender credibility using account-level metadata—account age, mutual server count, avatar presence, and message frequency.  
>  
> That approach hit two brick walls within the first three weeks:
> 1. **Discord Bot Sandboxing:** By platform design, Discord bot accounts **cannot** inspect direct messages between users unless the bot itself is an explicit participant in the DM. Bots also cannot inspect incoming friend requests.
> 2. **Discord Developer Policy Section 21:** Discord strictly bans saving or analyzing user chat data for machine learning without explicit opt-in consent. Running a client-side user proxy to intercept DM traffic would violate Discord's Terms of Service and create serious security risks."

> **[18:30 – 19:30] Spoken Dialogue:**  
> "Pivoting away from user metadata turned out to be the best decision we made. By focusing entirely on what we could parse from the raw message string and URLs, our final detector requires zero access to user profile databases, friends lists, or chat history. It is completely **self-contained and privacy-preserving**.  
>  
> Here are our top three engineering takeaways from this project:
> 1. **Lexical Models Are Brittle:** Bag-of-words and pure NLP models fall apart under basic character evasion. Robust security classifiers must be grounded in structural domain invariants.
> 2. **Latency is a Production Constraint:** A transformer with 99% accuracy is useless if it takes 300 ms on CPU and causes server chat lag. Tree ensembles running in 1.2 ms provide the throughput needed for live platform moderation.
> 3. **Verify API Boundaries Early:** Always confirm platform data access policies before designing features around private user metadata."

> **[19:30 – 20:00] Spoken Dialogue:**  
> "To summarize our results:
> - On a verified dataset of 3,552 messages, our dual-stream XGBoost model achieves **0.9777 F1** on clean messages.
> - Under adversarial evasion, while Discord AutoMod regex collapses by 37.2%, our minimax-hardened model achieves **0.9780 F1** and **$0.9888 \pm 0.0112$ cross-validation recall**.
> - The entire feature extraction and inference pipeline executes in **1.2 milliseconds** per message on a standard laptop CPU.  
>  
> Both the full 6-page IEEE technical report and our complete codebase with frontend and backend services are available in our repository. Thank you very much for your time, and we look forward to your questions!"

---

## Recording Tips for the Presenter

1. **Keep Your Webcam Visible:** Course instruction #1 requires the presenter's face to be in the video. Use OBS Studio or Loom with your webcam pinned in the bottom-right corner.
2. **Pacing:** Speak at a steady, conversational pace (~130–150 words per minute). The script above is calibrated to take approximately 19–20 minutes when demonstrating the interface.
3. **Smooth Transitions:** Practice the transition between Terminal commands and the Chrome browser tab so there are no awkward pauses.
4. **Mouse Clicks:** During Segment 5, clearly highlight and hover over the SHAP bars and feature badges as you explain them so the professor can follow your thought process.
