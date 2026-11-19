# 12-to-15 Minute Final Project Demo Video Presentation Script
*(Target Window: 10 – 20 Minutes | Paced for ~13 Minutes)*

**Project Title:** Dual-Stream Detection of Discord Phishing Campaigns Using Words and Link Structure  
**Course:** Machine Learning & Data Mining (Fall 2026)  
**Presenter:** Edwin Lin (Team #18 — Solo Project)  
**Target Video Duration:** 12 – 15 Minutes (Meets the 10 – 20 Minute Course Guideline)  

---

## 📋 Presenter Quick Checklist Before Hitting Record
- [ ] **Webcam On:** Pinned in corner throughout the entire recording (Course Rubric Requirement #1: presenter's face visible).
- [ ] **Microphone Active:** Clear audio, no background hum.
- [ ] **3 Chrome Tabs Ready:**
  1. `http://localhost:4200/` (Live Angular 18 Portal)
  2. `http://127.0.0.1:8000/docs` (FastAPI Swagger UI)
  3. Presentation Slides (`DEMO_PRESENTATION_SLIDES.html` or `.pptx`)
- [ ] **VS Code Terminal Open:** In workspace `c:\Users\Dan\Downloads\ML_DM`.

---

## ⏱️ Streamlined Video Roadmap (~13-14 Minutes Total)

| Segment | Timestamp | Slide & Activity | What Edwin Explains to the Teacher |
| :---: | :---: | :--- | :--- |
| **1** | **0:00 – 1:30** | **Slide 1 & Slide 2** (Title Card & Threat Code) | Who I am, the presentation roadmap, and why Discord phishing is dangerous |
| **2** | **1:30 – 3:30** | **Slide 3 & Slide 4** (AutoMod Bypass & Architecture) | Why regular expressions fail on lookalike letters, and how the two streams work |
| **3** | **3:30 – 5:30** | **Slide 5 & Slide 6** (Math Card & Dedup Code) | Plain math (edit distance early exit, entropy) and deduplicating 3,552 messages |
| **4** | **5:30 – 8:00** | **Slide 7 & Slide 8** + Terminal (`ablation_study.py`) | Model benchmarks, why Stream B beats text alone by 14%, and honest critique of 100% recall |
| **5** | **8:00 – 12:00** | **Slide 9 & Slide 10** + Live Browser Demo (`localhost:4200`) | Testing presets (clean chat, Nitro, Cyrillic evasion), SHAP bars, and Pop-out Chatbox |
| **6** | **12:00 – 14:00** | Summary Slides + Wrap-Up | Post-mortem (dropping user metadata for privacy), 3 engineering lessons, and conclusion |

---

# Spoken Presentation Script

---

### Segment 1: Introduction & Threat Context (0:00 – 1:30)

#### Slide 1: Project Overview & Roadmap (0:00 – 0:45)
**[ON SCREEN: Presenter webcam visible in corner. Show Slide 1 with the Pipeline Overview Card.]**

> **Spoken Dialogue:**  
> "Hello Professor, and welcome to my final project demonstration for Machine Learning and Data Mining. My name is Edwin Lin, representing Team 18 as a solo project.  
>  
> Today, I'm presenting **Dual-Stream Detection of Discord Phishing Campaigns Using Words and Link Structure**.  
>  
> To give you a quick roadmap of what I'll cover over the next thirteen to fourteen minutes:  
> First, I'll explain why Discord phishing is so dangerous and why simple keyword filters fail.  
> Second, I'll explain my dual-stream architecture and the mathematical models behind it.  
> Third, I'll walk through my data engineering and how I prevented data leakage using MD5 deduplication.  
> Fourth, we'll look at the experimental benchmarks in the terminal and discuss my 100% recall result with scientific honesty.  
> And fifth, I'll jump into my live Angular 18 and FastAPI web application to show you real-time classification in just 1.2 milliseconds."

---

#### Slide 2: Why Discord Phishing is Dangerous (0:45 – 1:30)
**[ON SCREEN: Advance to Slide 2 showing the 4 common attack pretexts and evasion code.]**

> **Spoken Dialogue:**  
> "Starting with Slide 2: *why is Discord phishing unique compared to normal email spam?*  
>  
> Discord isn't an open public feed like Twitter—it's made of semi-private servers and direct messages between friends.  
> When an attacker compromises an account using malware or a fake QR code login, automated scripts take over and immediately blast scam links to that user's friends list. Because the message comes from a friend you've known for months, your guard is down, and people click without thinking.  
>  
> As you can see on Slide 2, scammers use four main pretexts: fake Discord Nitro giveaways, fake indie game alpha tests that contain malware, community tournament voting traps, and crypto drainers. Once a user clicks, their account gets hijacked too, and the infection spreads laterally across the server."

---

### Segment 2: Filter Failures & System Architecture (1:30 – 3:30)

#### Slide 3: Failure Modes of Simple Filters (1:30 – 2:30)
**[ON SCREEN: Advance to Slide 3 showing the AutoMod Regex Bypass comparison card.]**

> **Spoken Dialogue:**  
> "To stop these scams, Discord servers usually rely on Discord AutoMod or community bots like MEE6. But almost all of them rely on basic keyword blocklists and regular expressions.  
>  
> Scammers easily bypass them using three clever tricks:
> 1. **Cyrillic Homoglyphs:** Attackers swap English letters for visually identical Russian Cyrillic letters—like using Cyrillic `'о'` (Unicode U+043E) instead of English `'o'`. To a human eye, `discord.com` looks 100% identical. But to a computer's regex matching ASCII bytes, they don't match, so AutoMod lets the scam right through!
> 2. **Markdown Masking:** Discord chat allows Markdown formatting like `[discord.com/nitro](evil.xyz)`. The chat displays a blue, trusted link, but clicking it sends the victim to a credential stealer.
> 3. **Casual Pretexts:** Opening with *'Hey, are you free?'* with no links at all, waiting for a reply before sending the lure.  
>  
> When I benchmarked AutoMod regex against these evasion tricks, its F1-score crashed by **37.2%**, dropping from 0.8598 down to 0.4876. That failure motivated my machine learning approach."

---

#### Slide 4: Dual-Stream Feature Fusion Architecture (2:30 – 3:30)
**[ON SCREEN: Advance to Slide 4 showing the Dual-Stream Flowchart and code snippet.]**

> **Spoken Dialogue:**  
> "On Slide 4 is the solution I designed: a **Dual-Stream Feature Fusion Pipeline**.  
> The core insight is: *Scammers can change their words in five seconds, but to steal credentials, they MUST send you to an external website they control.*  
>  
> So I split feature extraction into two streams:
> - **Stream A (Semantic Meaning):** Takes the message text and extracts 3,000 TF-IDF word features—both unigrams and bigrams—to capture high-pressure scam language like *'free'*, *'nitro'*, and *'claim'*.
> - **Stream B (Structural Clues):** Extracts 17 numerical features that don't depend on specific words: it counts lookalike Russian characters, detects cloaked Markdown links, checks similarity to real brand names, and measures how random the link is.  
>  
> I concatenate these into a single 3,017-dimensional vector and pass it to an **XGBoost gradient-boosted decision tree ensemble**.  
>  
> I chose XGBoost over a heavy transformer like BERT for two practical reasons:  
> First, **speed**: BERT takes 150 to 300 ms on a CPU, which causes chat backlogs on busy servers. XGBoost runs in just **1.2 milliseconds**.  
> Second, BERT's subword tokenizer fragments lookalike characters into weird pieces that degrade embeddings, whereas decision trees handle tabular structural rules naturally."

---

### Segment 3: Plain-English Math & Data Engineering (3:30 – 5:30)

#### Slide 5: Mathematical Formulations Demystified (3:30 – 4:30)
**[ON SCREEN: Advance to Slide 5 showing the mathematical cards for Levenshtein, Entropy, and Minimax Risk.]**

> **Spoken Dialogue:**  
> "On Slide 5, let me explain the three main mathematical formulas powering Stream B in plain terms:  
>  
> 1. **Minimum Levenshtein Distance ($d_{\min}$):**  
> This measures the edit distance—insertions, deletions, or substitutions—between extracted links and real brands like `discord.com` and `steamcommunity.com`. If a scammer sends `discoord.com`, the distance is only 1. To make this fast, I added an **early-exit check**: if the length difference between the two words is already greater than 4 characters, I skip the expensive nested loops entirely because it's impossible for the edit distance to be small.  
>  
> 2. **Shannon Domain Entropy ($H(d)$):**  
> This comes from information theory and measures randomness. Real company names like `discord` or `steam` use normal, pronounceable letter combinations, so they have low entropy (between 2.0 and 2.8). But automated scam bots spit out random, gibberish domains like `x7k9-free-nitro.ru`. Shannon entropy gives me a single number measuring how scrambled the letters are. Anything above 3.5 is an immediate red flag.  
>  
> 3. **Minimax Adversarial Hardening:**  
> Instead of just training on normal scams, I formulated training as a minimax problem: my code actively attacks its own dataset during training with synthetic homoglyphs and disguised links, forcing the decision trees to learn split rules that survive sneaky tricks."

---

#### Slide 6: Data Engineering & MD5 Deduplication (4:30 – 5:30)
**[ON SCREEN: Advance to Slide 6 showing the data loading, threat feeds, and MD5 deduplication code snippet.]**

> **Spoken Dialogue:**  
> "Looking at Slide 6, let's discuss the dataset.  
> To respect Discord's Developer Policy Section 21—which strictly bans saving private user chats for machine learning without consent—I built my dataset entirely from public research data:
> - 2,000 verified phishing messages from Hugging Face.
> - 21,908 verified malicious domains from the Nikolaischunk threat feed.
> - 1,500 modern attack playbooks modeling fake game playtests and OAuth traps.
> - Balanced against 2,500 clean, everyday gaming messages from open research logs.  
>  
> But here was the most critical data engineering step: **MD5 deduplication**.  
> The raw Hugging Face data had hundreds of duplicate copies of the exact same Nitro gift spam. If I hadn't filtered them out, the model would have memorized those exact messages and cheated on the test set.  
> Using an MD5 hash and text-normalization filter in `data_loader.py`, I eliminated all duplicate spam copies, producing a clean, balanced corpus of **3,552 unique messages** split 80% train, 10% validation, and 10% test."

---

### Segment 4: Master Showcase Pipeline & Why We Chose Our Models (5:30 – 8:00)

#### Slide 7: Running the Showcase Pipeline & Model Progression (5:30 – 7:00)
**[ON SCREEN: Switch screen to Terminal in VS Code. Run the master demonstration script live.]**

```powershell
# Command run live on screen:
py run_showcase_pipeline.py
```

> **Spoken Dialogue:**  
> "Now let's examine our experimental results. In my terminal, I'm going to run my master pipeline script: `py run_showcase_pipeline.py`.  
>  
> Look at how fast this executes—in just seventeen seconds, it executes the entire machine learning pipeline end-to-end: data ingestion, baseline evaluations, dual-stream training, ablation analysis, and adversarial hardening.  
>  
> Let me explain what is happening on screen and **why I tested and chose each specific model**:
>  
> 1. **Step 1 (Data Ingestion & Deduplication):**  
> Notice that it loaded 6,000 raw messages and deduplicated them down to **3,552 unique messages**. That eliminated hundreds of duplicate Nitro spam copies so the model wouldn't memorize the training set.  
>  
> 2. **Step 2 (Baseline Models Benchmark — Table I):**  
> *Why did I evaluate AutoMod, Naive Bayes, Logistic Regression, and SVM?*  
> Because I needed to test whether standard industry defenses and traditional NLP models could handle Discord phishing.  
> As you can see in Table I: on clean text, they all score above 0.96 F1. But under adversarial evasion, **AutoMod regex crashes by 37.2%** down to 0.4876 F1 because regex breaks when letters are swapped. Naive Bayes, Logistic Regression, and SVM all collapse to around 0.44 to 0.49 recall because mutated Russian letters fall completely outside their vocabulary dictionary!  
>  
> 3. **Step 3 (Dual-Stream Fused Models — Random Forest vs. XGBoost):**  
> *Why did I compare Random Forest against XGBoost on the 3,017 fused features?*  
> Both models use decision trees, which naturally handle tabular data like link counts, edit distance, and entropy. Random Forest uses bagging, which scored 0.7273 F1 under attack, but takes 3.4 milliseconds.  
> I chose **XGBoost as our primary model** because gradient boosting builds sequential trees that specifically target previously misclassified edge cases. It achieved **0.8078 F1** before hardening and runs in just **1.2 milliseconds on CPU**—which is critical for live Discord server throughput.  
>  
> 4. **Step 4 (3-Way Feature Ablation — Table II):**  
> *Why run an ablation study?* To prove whether Stream B (the 17 structural clues) actually adds value.  
> Look at the numbers: Stream A (text alone) crashes by -34% under attack. But Stream B alone gets **0.7748 F1**—beating text alone by **14.1%**! This proves that domain edit distance and entropy stay invariant even when the attacker scrambles the words."

---

#### Slide 8: Adversarial Hardening & Honest Review of 100% Recall (7:00 – 8:00)
**[ON SCREEN: Advance to Slide 8 showing the Feature Gain Shift, 5-Fold CV Variance, and the Scientific Audit card.]**

> **Spoken Dialogue:**  
> "Now in Step 5 of the pipeline and on Slide 8, let's look at **Minimax Adversarial Hardening**:  
>  
> *Why did I add adversarial hardening?*  
> Because a standard model only learns from clean historical data. By actively injecting synthetic lookalike characters and disguised links into 25% of training scams, the decision trees were forced to learn split rules that survive evasion.  
> After hardening, adversarial F1 recovered to **0.9780**, catching **178 out of 178 test scams—a 100% recall**.  
>  
> Now, Professor, I want to address this 100% recall with complete scientific honesty:  
> Whenever you see 100% in machine learning, that is usually a red flag. In my case, there is a clear reason why it happened:  
> Because I used the same mutation script (`build_adversarial_variant`) to create the training mutations as I did to evaluate the test set, the decision trees learned that `homoglyph_count >= 1` was an easy shortcut! That feature jumped from the #14 feature all the way up to the **#5 most important feature in tree gain**.  
>  
> In the open real world against brand-new zero-day attacks, recall will naturally be lower.  
> That is why I ran **5-fold cross-validation with randomized mutation seeds**: across the 5 folds, the model achieved **$0.9888 \pm 0.0112$ recall** and **$0.9780 \pm 0.0094$ F1**. That confirms my structural features are genuinely robust within a tight 1% variance."

---

### Segment 5: Live Interactive Application Demonstration (8:00 – 12:00)

#### Slide 9 & Live Browser Architecture (8:00 – 9:00)
**[ON SCREEN: Switch screen to Google Chrome showing Angular 18 at `http://localhost:4200/`. Presenter webcam in corner.]**

> **Spoken Dialogue:**  
> "Now let's transition to the live system demonstration.  
> I wanted to build a complete, production-ready tool. So I wrapped the trained models and feature extractor in a **FastAPI backend** running on port 8000, and I built this modern dashboard in **Angular 18** running on port 4200.  
>  
> At the top, you can see our live status banner: connected to FastAPI, using model `xgboost_hardened.joblib`, and showing an end-to-end latency counter currently at **1.2 milliseconds**.  
>  
> Let's test the detector across real-world test cases right now."

---

#### Live Test 1: Clean Everyday Chat (9:00 – 9:45)
**[ACTION: Click the 'Clean Gaming Chat' preset: *"Hey man, are we still hopping on Valorant tonight? Let me know when you're online."* Click Analyze.]**

> **Spoken Dialogue:**  
> "First, a normal benign message: *'Hey man, are we still hopping on Valorant tonight?'*  
> I click Analyze:
> - Inference takes just **1.1 milliseconds**.
> - The risk gauge is completely green at **0.02% scam probability**.
> - Policy verdict: **APPROVED (BENIGN)**.
> - In the structural card: `has_url = 0`, `homoglyphs = 0`.
> - And look at the SHAP explainability bars below: green bars pointing left show negative attribution—the absence of URLs and ordinary words actively convinced the model the message is safe."

---

#### Live Test 2: Classic Unmutated Nitro Scam (9:45 – 10:30)
**[ACTION: Click 'Classic Nitro Scam' preset: *"@everyone Steam free 3 months Discord Nitro: https://discord-nitro-gift.ru/claim"* Click Analyze.]**

> **Spoken Dialogue:**  
> "Second, a classic scam message blasting a fake Nitro gift link.  
> I hit Analyze:
> - The gauge turns bright red: **99.85% scam probability**!
> - The verdict triggers **AUTO-QUARANTINE** because it exceeds our 0.80 threshold.
> - Look at the structural clues: `min_levenshtein_discord = 1` (detecting `discord-nitro-gift` vs `discord.com`), suspicious `.ru` domain, and 3 urgency tokens (`free`, `nitro`, `gift`).
> - The SHAP chart clearly shows those domain and urgency features drove the score straight into quarantine."

---

#### Live Test 3: The Tricky Cyrillic Homoglyph Attack (10:30 – 11:15)
**[ACTION: Click 'Cyrillic Homoglyph Attack' preset: *"Steam partnership: claim complimentary subscription at https://dіscord.com/gifts (Note: 'і' is Cyrillic U+0456)"* Click Analyze.]**

> **Spoken Dialogue:**  
> "Now, Professor, here is the critical test case: the attack that completely breaks regular expressions.  
> Look at the link: `https://dіscord.com/gifts`.  
> To you and me, that looks 100% like official Discord. But the second letter—the `'і'`—is Unicode U+0456 from the Russian alphabet. A regex looking for `discord.com` will return False and miss this scam!  
>  
> Let's hit Analyze with my model:
> - It catches it instantly: **99.42% scam probability** in 1.2 ms!
> - In the structural inspection card: `homoglyph_count = 1` is highlighted in amber.
> - Because my model was hardened against synthetic perturbations during training, the decision trees know that combining a lookalike platform link with a non-zero homoglyph count is an evasion attack. It intercepts the scam effortlessly."

---

#### Slide 10 & Live Test 4: Interactive Pop-Out Chatbox (11:15 – 12:00)
**[ACTION: Click the floating 'Chat Playground' button in the bottom-right corner. The inline chatbox dialog pops open.]**

> **Spoken Dialogue:**  
> "To see how this works in a real chat environment, let's look at Slide 10 and test my **Pop-Out Chatbox**.  
>  
> Down here in the bottom-right corner, I click this floating button. It opens an inline chat window simulating a live Discord server.  
>  
> Let's type a normal message: *'Hey, did you finish the homework?'*  
> Sent—it appears with a green approved badge.  
>  
> Now let's simulate the compromised account replying with a fake game test:  
> *'Yeah! My buddy released a game demo on Steam, can you test it? https://steamcommunity-beta.top/setup.exe'*  
>  
> I hit Enter:  
> Instantly—in 1.2 milliseconds—the system flags the message in bright red with an **AUTO-QUARANTINED** warning overlay! The dangerous link is blocked from rendering clickable in chat, protecting users from accidental clicks."

---

### Segment 6: Post-Mortem, Lessons & Conclusion (12:00 – 14:00)

#### Post-Mortem: Why I Dropped User Metadata (12:00 – 13:00)
**[ON SCREEN: Switch screen back to presenter camera and summary slides.]**

> **Spoken Dialogue:**  
> "Before concluding, I want to share a key learning outcome: my **Architectural Post-Mortem and Initial Failure**.  
>  
> When I originally started in September, my proposal was very different: I planned to build a Discord bot that checked user account metadata—account age, mutual server counts, avatar presence, and message frequency.  
>  
> That approach hit two brick walls within the first three weeks:
> 1. **Discord Bot Sandboxing:** By platform design, Discord bots cannot inspect private DMs between users unless the bot is directly participating.
> 2. **Discord Developer Policy Section 21:** Discord strictly bans saving user chat data for machine learning without consent. Building a proxy to intercept DMs would violate Discord's Terms of Service and create huge privacy risks.  
>  
> Ditching user metadata was the best engineering pivot I made. By inspecting **only the raw message payload and URLs**, the final detector requires zero access to private user databases or chat history. It is completely **self-contained, privacy-preserving, and fast**."

---

#### Key Takeaways & Conclusion (13:00 – 14:00)
> **Spoken Dialogue:**  
> "To wrap up, here are my top three engineering takeaways:
> 1. **Text Models Are Fragile Under Attack:** Bag-of-words models break down the moment scammers swap a few letters. Security classifiers must be grounded in structural domain invariants that attackers cannot easily hide.
> 2. **Latency is a Production Constraint:** A giant neural network that gets 99% accuracy is useless if it takes 300 ms on CPU and causes server chat lag. An XGBoost ensemble running in 1.2 ms provides the throughput needed for live moderation.
> 3. **Verify API Boundaries Early:** Always verify what data a platform permits you to access before designing machine learning features around private user metadata.  
>  
> To summarize my final results:  
> On 3,552 messages, my model achieves **0.9777 clean F1**, recovers to **0.9780 adversarial F1** under evasion attacks (where AutoMod crashes by 37.2%), runs in **1.2 milliseconds** on CPU, and is fully deployed across FastAPI and Angular 18.  
>  
> All code, models, reports, and slide decks are available in my GitHub repository.  
> Thank you so much for your time and guidance, Professor. I'm ready for your questions!"

---

## 🎯 Quick Presentation Reminders for Edwin
- **Timing:** This script is paced for **~13 minutes** at a natural talking speed (~130 words/min). You are comfortably within the **10 to 20 minute** course window!
- **Keep Your Face Visible:** OBS or Loom webcam in the corner throughout.
- **Hover on Key Elements:** When you mention 1.2 ms, homoglyph count, or SHAP bars, hover your mouse over them on screen.
- **Show Confidence in Your Critique:** When explaining the 100% recall result, speak with pride—professors love when a student critically analyzes their own experimental data!
