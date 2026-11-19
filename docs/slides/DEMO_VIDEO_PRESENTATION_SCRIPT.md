# 20-Minute Final Project Demo Video Presentation Script

**Project Title:** Dual-Stream Detection of Discord Phishing Campaigns Using Words and Link Structure  
**Course:** Machine Learning & Data Mining (Fall 2026)  
**Presenter:** Edwin Lin (Team #18 — Solo Project)  
**Target Video Duration:** ~20 Minutes (18:00 – 22:00)  

---

## 📋 Recording Setup Checklist for Edwin
- [ ] **Webcam Visible:** Pinned in the corner throughout the entire recording (Course requirement: presenter's face must be visible).
- [ ] **Microphone Check:** Clear audio with no background noise or echo.
- [ ] **Open Browser Tabs:**
  1. `http://localhost:4200/` (Live Angular 18 Enterprise UI)
  2. `http://127.0.0.1:8000/docs` (FastAPI Swagger Docs)
  3. Presentation Slides (`DEMO_PRESENTATION_SLIDES.html` or `.pptx`)
- [ ] **Open Terminal:** Visual Studio Code / PowerShell ready in `c:\Users\Dan\Downloads\ML_DM`.

---

## ⏱️ Video Presentation Roadmap (10 Slides + Live Demo)

| Segment | Time | Primary Visual & Activity | Focus / Plain Explanation |
| :---: | :---: | :--- | :--- |
| **1** | **0:00 – 2:30** | **Slide 1 & Slide 2** (Architecture card & Evasion code) | Introduction, what Discord phishing is, and why traditional filters fail |
| **2** | **2:30 – 5:00** | **Slide 3 & Slide 4** (Regex failure card & Dual-stream code) | Why regex breaks down, and how the two-stream pipeline works |
| **3** | **5:00 – 7:30** | **Slide 5 & Slide 6** (Math models card & Data loader dedup code) | Edit distance early exit, Shannon entropy, and deduplicating 3,552 messages |
| **4** | **7:30 – 11:30** | **Slide 7 & Slide 8** + Terminal (`train_baselines.py`, `ablation_study.py`) | Model benchmarks, feature ablation, and an honest critique of 100% recall |
| **5** | **11:30 – 17:00** | **Slide 9 & Slide 10** + Live Browser Demo (`http://localhost:4200/`) | Testing benign chat, Nitro lures, Cyrillic lookalikes, SHAP bars, and Pop-out Chatbox |
| **6** | **17:00 – 20:00** | Summary Slides + Camera Wrap-Up | Post-mortem (why I dropped user metadata), lessons learned, and final conclusion |

---

# Detailed Spoken Presentation Script

---

### Segment 1: Introduction, Threat Context & The Problem (0:00 – 2:30)

#### [0:00 – 1:00] Slide 1: Title & Project Overview
**[ON SCREEN: Presenter webcam pinned in top-right or bottom-right corner. Show Slide 1 with the Dual-Stream Pipeline Overview Card.]**

> **Spoken Dialogue:**  
> "Hello Professor, and welcome to my final project demonstration for Machine Learning and Data Mining. My name is Edwin Lin, representing Team 18 as a solo project.  
>  
> Today, I'm presenting my project: **Dual-Stream Detection of Discord Phishing Campaigns Using Words and Link Structure**.  
>  
> To give you a quick roadmap of what I'll be showing you over the next twenty minutes:  
> First, I'm going to explain the real-world security problem on Discord and why simple keyword filters fail.  
> Second, I'll walk you through my dual-stream system architecture and the mathematical models I implemented.  
> Third, I'll show you my actual code in VS Code—how I engineered the dataset, prevented data leakage with MD5 deduplication, and extracted features.  
> Fourth, we'll run the training and benchmark scripts in the terminal to look at the numbers and do an honest scientific critique of my results.  
> And finally, I will switch over to my browser and give you a live demonstration of the full-stack web application I built with Angular 18 and FastAPI, showing real-time message classification in just 1.2 milliseconds."

---

#### [1:00 – 2:30] Slide 2: Threat Context: Why Discord Phishing is Dangerous
**[ON SCREEN: Advance to Slide 2 showing the 4 common attack pretexts and the code snippet card of evasion perturbations.]**

> **Spoken Dialogue:**  
> "So to start off: *why is Discord phishing such a big deal, and why is it different from normal email spam?*  
>  
> Unlike public social media platforms like Twitter or Reddit where anyone can see a spam post and report it, Discord is built on semi-private servers and direct messages between friends.  
>  
> Here is what typically happens: a user accidentally gets their account compromised—maybe by downloading a malicious file or scanning a fake QR code. The scammer's automated script takes over that account and immediately blasts scam messages to everyone on that person's friends list and every mutual server they share.  
>  
> Because the message comes from a friend you've known for months, your guard is down. People click the link without thinking.  
>  
> As you can see on Slide 2, attackers generally use four main pretexts:
> 1. Fake Discord Nitro giveaways, claiming to be sponsored by Steam or Epic Games.
> 2. Fake indie game playtest invites, asking you to test an executable file that actually contains an infostealer.
> 3. Fake tournament voting links that ask you to authorize third-party OAuth access.
> 4. Fake cryptocurrency drops and wallet drainers.  
>  
> Once someone clicks and falls for it, their account gets hijacked too, and the scam spreads laterally across the network like a chain reaction."

---

### Segment 2: Failure of Simple Filters & System Architecture (2:30 – 5:00)

#### [2:30 – 3:45] Slide 3: Failure Modes of Deterministic Filters (AutoMod)
**[ON SCREEN: Advance to Slide 3 showing the AutoMod Regex Bypass comparison card.]**

> **Spoken Dialogue:**  
> "Now, Discord does have a built-in tool called AutoMod, and server owners often install bots like MEE6 or Dyno. But almost all of these tools rely on simple keyword blocklists and regular expressions.  
>  
> If an attacker sends: *'Free Discord Nitro: https://discord.gift/claim'*, AutoMod catches it easily.  
>  
> But scammers know this, so they use very clever tricks to bypass the filters:
> 1. **Cyrillic Homoglyphs:** Attackers replace standard English letters with visually identical letters from the Russian Cyrillic alphabet. For example, if you replace the English letter `'o'` with the Cyrillic letter `'о'`—which is Unicode character U+043E—to a human eye on screen, it looks 100% identical: `discord.com`. But to a computer's regular expression matching ASCII bytes, it's completely different. AutoMod lets it right through!
> 2. **Markdown Link Masking:** Discord chat supports Markdown formatting. An attacker can write: bracket `https://discord.com/nitro` close bracket, followed by parentheses `https://malicious-stealer.xyz`. In the chat window, the user sees a blue, trusted link that says `discord.com/nitro`, but when they click it, Discord sends them to the phishing website.
> 3. **Casual Pretexts:** Scammers open with casual greetings like *'Hey, are you free right now?'* with no links at all, waiting for you to reply before sending the link.  
>  
> When I benchmarked Discord AutoMod's regular expressions against these evasion tricks, its F1-score crashed by **37.2%**—dropping from 0.8598 down to 0.4876. That failure was the main motivation for my project: I wanted to build a machine learning model that looks deeper than surface-level text."

---

#### [3:45 – 5:00] Slide 4: System Architecture: Dual-Stream Feature Fusion
**[ON SCREEN: Advance to Slide 4 showing the Dual-Stream Pipeline flowchart and feature extraction code snippet.]**

> **Spoken Dialogue:**  
> "Here on Slide 4 is the core architecture I designed. When thinking about this problem, I asked myself: *What can a scammer change easily, and what are they forced to keep?*  
>  
> A scammer can change their words or swap letters in five seconds. But to actually steal your account or money, they **must** send you to an external website they control. That website domain is almost always newly registered, slightly misspelled, or full of random characters.  
>  
> So I built a **Dual-Stream Feature Fusion Pipeline**:
> - **Stream A (Semantic Meaning):** This stream looks at the message vocabulary. It cleans the text and creates 3,000 TF-IDF word features—both single words and word pairs—to capture high-pressure scam language like *'limited time'*, *'claim now'*, and *'anniversary'*.
> - **Stream B (Structural Clues):** This stream extracts 17 numerical features that don't depend on specific words. It counts how many lookalike Russian letters are present, checks if Markdown links are cloaked, measures how similar the link is to real brands, and calculates the randomness of the domain name.  
>  
> Then, I concatenate both streams together into a single feature vector of 3,017 numbers and feed it into an **XGBoost gradient-boosted decision tree ensemble**.  
>  
> A teacher or reviewer might ask: *Why use XGBoost instead of a big deep learning model like BERT?*  
> I actually tested BERT early on, but I chose XGBoost for two big reasons:  
> First, **speed**. A BERT transformer takes 150 to 300 milliseconds on a standard CPU. If a busy Discord server gets hundreds of messages a minute, that causes a huge backlog. XGBoost runs in just **1.2 milliseconds** on a regular laptop CPU.  
> Second, **tokenization stability**. When you feed lookalike Russian letters into BERT, its tokenizer breaks the word into weird, disjointed sub-character fragments that confuse the model. Decision trees on tabular features handle these discontinuous rules much more naturally."

---

### Segment 3: Mathematical Models & Data Engineering (5:00 – 7:30)

#### [5:00 – 6:15] Slide 5: Mathematical Formulations & Algorithmic Optimizations
**[ON SCREEN: Advance to Slide 5 showing the mathematical cards for Levenshtein, Shannon Entropy, and Minimax Risk.]**

> **Spoken Dialogue:**  
> "Now let's look at Slide 5, where I want to explain the mathematical ideas behind Stream B in plain terms:  
>  
> 1. **Minimum Levenshtein Distance ($d_{\min}$):**  
> Levenshtein distance simply measures the minimum number of single-character edits—insertions, deletions, or substitutions—needed to turn one string into another. If a scammer sends a link like `discoord.com` or `steamcommunlty.com`, the distance to the real brand name is only 1 or 2.  
> But calculating that edit matrix for every message can get computationally heavy. So I added an **early-exit optimization**: if the length difference between the two words is already greater than 4 characters, I skip the expensive nested loops entirely because it's mathematically impossible for the edit distance to be small. This shaved precious microseconds off every check.  
>  
> 2. **Shannon Domain Entropy ($H(d)$):**  
> Shannon entropy is a concept from information theory that measures randomness or disorder. Real company names—like `discord` or `steam`—use common, pronounceable combinations of letters, so they have low entropy, usually between 2.0 and 2.8. But scammers often use automated scripts that generate random, gibberish domain names like `x7k9-free-nitro.ru`. Shannon entropy gives me a single number measuring how scrambled those characters are. When the score is above 3.5, it immediately raises a red flag.  
>  
> 3. **Minimax Adversarial Hardening:**  
> Normally in machine learning, you train a model on regular training data. But here, I formulated this as a minimax problem: during training, my code actively attacks its own dataset by injecting synthetic homoglyphs and hidden Markdown links, forcing the decision trees to learn split rules that survive worst-case perturbations."

---

#### [6:15 – 7:30] Slide 6: Data Engineering & Threat Feed Integration
**[ON SCREEN: Advance to Slide 6 showing the data loading, threat feeds, and MD5 deduplication code snippet.]**

> **Spoken Dialogue:**  
> "Moving to Slide 6, let's talk about the dataset and how I built it.  
>  
> Collecting Discord data requires being very careful about privacy. Section 21 of Discord's Developer Policy strictly bans saving or analyzing private user chat for machine learning without explicit consent. So I built my dataset entirely from verified, public research sources:
> - 2,000 verified phishing messages from the Hugging Face Discord Phishing dataset.
> - 21,908 verified malicious domains from the Nikolaischunk threat feed, which I inserted into realistic scam templates.
> - 1,500 modern attack playbooks covering things like fake game alpha tests, Steam tournament votes, and OAuth traps.
> - Balanced against 2,500 clean, everyday gaming conversations from open research logs.  
>  
> But here was the biggest data engineering challenge: **data duplication**.  
> When I first inspected the raw data from Hugging Face, there were hundreds of identical copies of the exact same Nitro gift spam. If I had trained the model on that directly, it would have memorized those exact words, and the test set would have been contaminated.  
>  
> To solve that, I wrote an **MD5 hash and text-normalization filter** in `data_loader.py`. That eliminated all duplicate spam and produced a clean, balanced corpus of **3,552 unique messages**, split into 80% for training, 10% for validation, and 10% for clean testing, plus a separate 356-sample adversarial evaluation set."

---

### Segment 4: Model Training, Baselines & Honest Review of 100% Recall (7:30 – 11:30)

#### [7:30 – 9:00] Slide 7: Experimental Benchmarks & Feature Ablation
**[ON SCREEN: Advance to Slide 7 showing the Studio Workbench Analytics, ROC curves, and Tables I & II.]**

> **Spoken Dialogue:**  
> "Now let's examine the experimental results on Slide 7. I benchmarked my system against five different baseline models:
> 1. Discord AutoMod's regular expression rules.
> 2. Naive Bayes with TF-IDF.
> 3. Logistic Regression with TF-IDF.
> 4. Linear Support Vector Machine (SVM).
> 5. A Random Forest on fused features.
> 6. And my unhardened XGBoost baseline.  
>  
> As you can see in Table I, on **clean, standard messages**, all machine learning models perform well—scoring above 0.96 F1. AutoMod regex gets an 0.8598 F1.  
>  
> But the real story happens when we test them against the **adversarial evasion set**:
> - AutoMod collapses by 37.2% down to **0.4876 F1** because a regex fails the moment a letter is swapped.
> - Naive Bayes, Logistic Regression, and SVM all collapse to around 0.44 to 0.49 recall because those mutated Russian words don't exist in their vocabulary.
> - But my unhardened XGBoost model maintains an **0.8078 F1** because its trees can still rely on the structural clues in Stream B."

---

#### [9:00 – 10:15] Terminal Run: Ablation Study
**[ON SCREEN: Switch screen to Terminal in VS Code. Run `train_baselines.py` and `ablation_study.py`.]**

```powershell
# Command shown on screen:
cd backend
python src/ablation_study.py
```

> **Spoken Dialogue:**  
> "Now let me switch over to my terminal and run `src/ablation_study.py` live so you can see Table II being generated.  
>  
> The purpose of an ablation study is to answer: *How much value does Stream B actually add on its own?*  
> Look at the numbers on screen:
> - **Stream A Alone (3,000 TF-IDF words):** On clean data it gets a 0.9589 F1, but under attack, its recall drops to 0.4944—a 34% drop!
> - **Stream B Alone (Just the 17 Structural Features):** Even though it only has 17 numbers compared to 3,000 words, under attack it achieves an F1 of **0.7748**! It beats the text-only model by 14.1% because domain edit distance and entropy don't care if the text is misspelled.
> - **Dual-Stream Combined:** Fusing them together gives us the best of both worlds—0.9777 F1 on clean chat and 0.8078 under evasion."

---

#### [10:15 – 11:30] Slide 8: Adversarial Hardening & Honest Review of 100% Recall
**[ON SCREEN: Advance to Slide 8 showing the XGBoost Feature Gain Shift, 5-Fold CV Variance, and the Scientific Audit card.]**

> **Spoken Dialogue:**  
> "Now let's look at Slide 8, which covers **Adversarial Hardening** and a very important scientific observation.  
>  
> To protect the model from evasion, I augmented 25% of the training scams with synthetic lookalike characters and Markdown disguises. After retraining, my hardened XGBoost model scored **0.9780 F1** on the attack set, catching **178 out of 178 test scams—a 100% recall**.  
>  
> Now, as a student presenting to my teacher, I want to address this 100% recall with complete scientific honesty:  
> When you see 100% in machine learning, that is usually a red flag that something is too easy or there is closed-distribution evaluation. And that is exactly what happened here.  
>  
> Because I used the same perturbation function (`build_adversarial_variant`) to create the training mutations as I did to evaluate the test set, the decision tree learned that `homoglyph_count >= 1` was a near-perfect split rule! That feature jumped from the #14 feature all the way up to the **#5 most important feature in tree gain**.  
>  
> In the open real world, attackers will eventually invent novel zero-day tricks—like right-to-left override characters or QR code images—so real-world recall won't stay at 100%.  
>  
> To check the true statistical variance, I ran a **5-fold cross-validation with randomized mutation seeds**. Across the 5 folds, the model achieved **$0.9888 \pm 0.0112$ recall** and **$0.9780 \pm 0.0094$ F1**. That confirms the model's structural features are genuinely robust, with a tight variance of about plus-or-minus one percent."

---

### Segment 5: Live Application Demonstration (11:30 – 17:00)

#### [11:30 – 12:30] Slide 9 & Live Browser Architecture
**[ON SCREEN: Switch screen to Google Chrome showing the live Angular 18 frontend at `http://localhost:4200/`. Presenter webcam remains visible in corner.]**

> **Spoken Dialogue:**  
> "Now let's move to the live demonstration of the system.  
>  
> I didn't want this project to just be a script in a Jupyter notebook—I wanted to build a production-ready application. So I wrapped the trained models and feature extractor in a **FastAPI backend** running locally on port 8000, and I built this modern single-page dashboard using **Angular 18** running on port 4200.  
>  
> Notice the top header: it shows we are connected to the FastAPI microservice, using the active model `xgboost_hardened.joblib`, and my name, Edwin Lin, as the author.  
>  
> Let's run through four live test cases right now."

---

#### [12:30 – 13:30] Live Test 1: Benign Everyday Chat
**[ACTION: In the Angular UI, click the 'Clean Gaming Chat' preset button: *"Hey man, are we still hopping on Valorant tonight? Let me know when you're online."* Click the purple 'Analyze Message' button.]**

> **Spoken Dialogue:**  
> "First, let's test a normal, everyday gaming message: *'Hey man, are we still hopping on Valorant tonight?'*  
>  
> I click Analyze. Look at that latency counter: it took just **1.1 milliseconds**!  
>  
> Let's look at the result:
> - The radial risk gauge is completely green: **0.02% scam probability**.
> - The policy badge says **APPROVED (BENIGN)**.
> - In the structural inspection card: `has_url` is 0, `homoglyph_count` is 0, and `urgency_tokens` is 0.
> - And look at the SHAP explainability bars below: the bars are green and point to the left, showing negative attribution. That means the absence of URLs and ordinary words actively convinced the model that this message is safe."

---

#### [13:30 – 14:30] Live Test 2: Classic Unmutated Nitro Scam
**[ACTION: Click the 'Classic Nitro Scam' preset: *"@everyone Steam is giving away 3 months of Discord Nitro for free! Claim your gift here: https://discord-nitro-gift.ru/claim"* Click Analyze.]**

> **Spoken Dialogue:**  
> "Now let's test an unmutated scam message that mimics an account blasting free Nitro gifts.  
>  
> I click Analyze:
> - Instantly, the radial gauge turns bright red: **99.85% scam probability**!
> - The decision routing triggers **AUTO-QUARANTINE** because the score is well above our 0.80 policy threshold.
> - Let's see why:
>   - `min_levenshtein_discord = 1`—the system noticed that `discord-nitro-gift` is an edit distance of only 1 from the real brand domain.
>   - `suspicious_tld = 1`—it flagged the `.ru` top-level domain.
>   - `urgency_token_count = 3`—it found `free`, `nitro`, and `gift`.
>   - `mention_count = 1`—it saw the `@everyone` broadcast tag.
> - The SHAP chart gives us complete transparency: the red bars clearly explain that the domain similarity and urgency words drove the score straight into the quarantine zone."

---

#### [14:30 – 15:45] Live Test 3: The Tricky Cyrillic Homoglyph Attack (The Regex Killer)
**[ACTION: Click the 'Cyrillic Homoglyph Attack' preset: *"Steam partnership: claim complimentary subscription at https://dіscord.com/gifts (Note: 'і' is Cyrillic U+0456)"* Click Analyze.]**

> **Spoken Dialogue:**  
> "Now, Professor, this is the most important test case: the attack that completely breaks Discord AutoMod and regex filters.  
>  
> Look closely at the URL: `https://dіscord.com/gifts`.  
> To you and me, that looks 100% like official Discord. But that second letter—the `'і'`—is actually Unicode character U+0456 from the Russian Cyrillic alphabet.  
> If you run a regular expression looking for `discord.com`, it will return False and let this phishing attack into your server!  
>  
> Now let's hit Analyze with my hardened dual-stream model:
> - Look at that: **99.42% scam probability**! It caught it instantly in 1.2 milliseconds!
> - Look at the structural inspection card: `homoglyph_count` is highlighted in amber with a count of 1.
> - Because my model was hardened against synthetic perturbations during training, the decision trees know that combining a lookalike brand URL with a non-zero homoglyph count is an evasion attack. It intercepts the scam effortlessly where normal filters fail."

---

#### [15:45 – 17:00] Slide 10 & Live Test 4: The Pop-Out Chatbox Playground
**[ACTION: Click the floating 'Chat Playground' button in the bottom-right corner. The inline pop-out chatbox dialog opens smoothly.]**

> **Spoken Dialogue:**  
> "Now, to see how this would feel for real users and moderators inside Discord, let's look at Slide 10 and test my **Pop-Out Chatbox Playground**.  
>  
> Down here in the bottom right corner, I can click this floating chat button. It opens an inline chat window that simulates a live Discord conversation.  
>  
> Let's type a normal message first:  
> *'Hey, did you finish the homework assignment?'*  
> I hit send: the message appears with a green approved indicator in 1.2 ms.  
>  
> Now let's simulate the compromised bot account replying with a fake game test:  
> *'Yeah! By the way, my friend made a game demo on Steam, can you test it? https://steamcommunity-beta.top/setup.exe'*  
>  
> I hit Enter:  
> Instantly—in 1.2 milliseconds—the system flags the message in bright red with an **AUTO-QUARANTINED** warning overlay! The dangerous link is blocked from rendering clickable in chat, protecting the user from accidental clicks.  
>  
> The dialog can also be minimized, maximized, or docked, showing how easily this moderation engine could be integrated into real chat software."

---

### Segment 6: Architectural Post-Mortem, Lessons Learned & Conclusion (17:00 – 20:00)

#### [17:00 – 18:30] Project Post-Mortem: Why I Abandoned User Metadata
**[ON SCREEN: Close the chatbox dialog or switch to summary slides with webcam active.]**

> **Spoken Dialogue:**  
> "Before concluding, I want to discuss a crucial part of my learning outcomes: my **Architectural Post-Mortem and Initial Failure**.  
>  
> When I originally started this project back in September, my proposal was very different: I planned to build a Discord bot that evaluated sender credibility using account metadata—things like account age, mutual server counts, avatar presence, and message frequency.  
>  
> That approach hit two brick walls within the first three weeks:
> 1. **Discord Bot Sandboxing:** By platform design, Discord bot accounts **cannot** inspect direct messages between users unless the bot is directly participating in the conversation. Bots also cannot inspect incoming friend requests.
> 2. **Discord Developer Policy Section 21:** Discord strictly forbids saving or analyzing private user chat data for machine learning without explicit opt-in consent. If I had built a client-side proxy to intercept user DMs, it would have violated Discord's Terms of Service and created massive privacy vulnerabilities.  
>  
> Ditching user metadata was the best engineering decision I made. By pivoting to inspect **only the raw message string and its URLs**, the final detector requires zero access to private user databases, friends lists, or chat histories. It is completely **self-contained, privacy-preserving, and fast**."

---

#### [18:30 – 19:30] Key Engineering Takeaways
> **Spoken Dialogue:**  
> "Here are the top three engineering lessons I learned from this project:
> 1. **Text Models Are Fragile Under Attack:** Bag-of-words and standard NLP models break down the moment scammers swap a few letters. Robust security models must be anchored in structural domain invariants that attackers cannot easily disguise.
> 2. **Latency is a Real Production Constraint:** A giant neural network that gets 99% accuracy is useless if it takes 300 milliseconds on a CPU and creates a chat lag backlog. A gradient-boosted tree ensemble running in 1.2 milliseconds gives you the throughput needed for live platform moderation.
> 3. **Verify API Boundaries First:** Always confirm what data an API actually permits you to access before designing machine learning features around private user metadata."

---

#### [19:30 – 20:00] Conclusion & Wrap-Up
> **Spoken Dialogue:**  
> "To summarize what I accomplished in this project:
> - On a verified dataset of 3,552 messages, my dual-stream XGBoost model achieves **0.9777 F1** on clean messages.
> - Under adversarial evasion attacks, while Discord AutoMod regex collapses by 37.2%, my minimax-hardened model recovers to **0.9780 F1** with **$0.9888 \pm 0.0112$ cross-validation recall**.
> - The entire feature extraction and inference pipeline runs in just **1.2 milliseconds** per message on a standard laptop CPU.  
> - And I packaged the entire system into a full-stack, production-ready web application with Angular 18 and FastAPI.  
>  
> All of my code, trained models, 6-page IEEE report, and slide decks are organized cleanly in my GitHub repository.  
>  
> Thank you so much for your time and guidance throughout the semester, Professor. I'm ready to answer any questions you have!"

---

## 💡 Quick Tips for Edwin During the Recording

1. **Keep Your Webcam On:** Pin your face in the corner (OBS or Loom) so the teacher can see you presenting.
2. **Pacing:** Speak naturally and conversational, like you are walking your teacher through a cool project you built and are proud of. Don't rush!
3. **Point at the Visuals:** When you talk about the 1.2 ms badge, the SHAP bars, or the Cyrillic homoglyph, hover your mouse over them on screen so the professor's eyes follow your explanation.
4. **Be Honest About the 100% Score:** Professors love when students explain *why* a number came out high and criticize their own experiments—it proves you understand the machine learning fundamentals!
