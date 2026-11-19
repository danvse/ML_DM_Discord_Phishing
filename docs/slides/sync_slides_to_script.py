"""
Synchronizes both:
1. docs/slides/DEMO_PRESENTATION_SLIDES.pptx (16:9 Widescreen Microsoft PowerPoint Deck)
2. docs/slides/DEMO_PRESENTATION_SLIDES.html (Interactive HTML5 Slide Deck)

Direct 1:1 synchronization with docs/slides/DEMO_VIDEO_PRESENTATION_SCRIPT.md
Target Time: 12-15 Minutes (10-20 Minute Guideline | Paced for ~13 min)
Presenter: Edwin Lin (Team #18 - Solo Project)
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "slides_assets")

# Palette
DARK_BG = RGBColor(24, 26, 31)
CARD_BG = RGBColor(35, 38, 46)
TEXT_WHITE = RGBColor(240, 243, 246)
TEXT_MUTED = RGBColor(160, 168, 180)
ACCENT_CYAN = RGBColor(0, 210, 255)
ACCENT_GREEN = RGBColor(46, 204, 113)
ACCENT_RED = RGBColor(231, 76, 60)
ACCENT_PURPLE = RGBColor(155, 89, 182)
ACCENT_YELLOW = RGBColor(241, 196, 15)

SLIDES_DATA = [
    {
        "slide_num": 1,
        "title": "Dual-Stream Detection of Discord Phishing Campaigns",
        "subtitle": "Machine Learning & Data Mining (Fall 2026) | Final Project Demo\nTeam #18: Edwin Lin (Solo Project)",
        "time": "0:00 - 0:45",
        "action": "[ON CAMERA: Presenter intro with pinned webcam in corner — 13-min Demo Roadmap]",
        "bullets": [
            "Project Goal: Fast, machine-learning-based phishing detection built for Discord's unique chat invariants.",
            "Novel Dual-Stream Pipeline: Combines 3,000 TF-IDF word n-grams (Stream A) with 17 engineered structural features (Stream B).",
            "Target Operational Latency: Sub-2ms CPU inference to prevent server message queuing backlogs (achieves 1.2 ms).",
            "Demonstration Overview: Architecture • Math • Data Engineering • Model Benchmarks • Live Angular 18 Demo."
        ],
        "image": "pipeline_overview_card.png",
        "image_caption": "Architecture: Dual-Stream Pipeline & Decision Policy",
        "script_cue": (
            "Hello Professor, and welcome to my final project demonstration for Machine Learning and Data Mining. "
            "My name is Edwin Lin, representing Team 18 as a solo project.\n\n"
            "Today, I'm presenting Dual-Stream Detection of Discord Phishing Campaigns Using Words and Link Structure.\n\n"
            "To give you a quick roadmap of what I'll cover over the next thirteen to fourteen minutes:\n"
            "First, I'll explain why Discord phishing is so dangerous and why simple keyword filters fail.\n"
            "Second, I'll explain my dual-stream architecture and the mathematical models behind it.\n"
            "Third, I'll walk through my data engineering and how I prevented data leakage using MD5 deduplication.\n"
            "Fourth, we'll look at the experimental benchmarks in the terminal and discuss my 100% recall result with scientific honesty.\n"
            "And fifth, I'll jump into my live Angular 18 and FastAPI web application to show you real-time classification in just 1.2 milliseconds."
        )
    },
    {
        "slide_num": 2,
        "title": "Threat Context: Why Discord Phishing is Dangerous",
        "subtitle": "Localized Trust Networks & Lateral Account Hijacking",
        "time": "0:45 - 1:30",
        "action": "[SLIDE: Explain the 4 common attack pretexts & lateral spreading]",
        "bullets": [
            "Platform Topology: Discord is organized into semi-private servers and direct messages (DMs), not an open public feed.",
            "Trust Exploitation: Compromised accounts blast malicious links to mutual servers and friends lists who inherently trust the sender.",
            "Attack Vector 1 • Nitro Lures: Fake Discord Nitro promotions (supposedly sponsored by Steam or Epic Games).",
            "Attack Vector 2 • Fake Game Tests: Indie game alpha playtest invites (.exe / .scr infostealers like RedLine).",
            "Attack Vector 3 • Community Traps: Tournament voting links requiring third-party OAuth token grants.",
            "Attack Vector 4 • Crypto Drainers: Fake cryptocurrency / wallet-drainer distribution portals."
        ],
        "image": "code_adversarial_perturbation.png",
        "image_caption": "Code: Homoglyph & Markdown Link Masking (data_loader.py)",
        "script_cue": (
            "Starting with Slide 2: why is Discord phishing unique compared to normal email spam?\n\n"
            "Discord isn't an open public feed like Twitter—it's made of semi-private servers and direct messages between friends. "
            "When an attacker compromises an account using malware or a fake QR code login, automated scripts take over and immediately blast scam links to that user's friends list. "
            "Because the message comes from a friend you've known for months, your guard is down, and people click without thinking.\n\n"
            "As you can see on Slide 2, scammers use four main pretexts: fake Discord Nitro giveaways, fake indie game alpha tests that contain malware, "
            "community tournament voting traps, and crypto drainers. Once a user clicks, their account gets hijacked too, and the infection spreads laterally across the server."
        )
    },
    {
        "slide_num": 3,
        "title": "Failure Modes of Deterministic Filters (AutoMod)",
        "subtitle": "Why Keyword Blocklists & Regular Expressions Break Down",
        "time": "1:30 - 2:30",
        "action": "[SLIDE: Contrast regex byte matching vs. modern evasion tricks]",
        "bullets": [
            "Industry Standard: Discord AutoMod and bot filters (MEE6, Dyno) rely almost entirely on static regexes and keyword blocklists.",
            "Evasion Trick 1 • Cyrillic Homoglyphs: Swapping Latin 'o' (U+006F) with Cyrillic 'о' (U+043E) looks identical to humans but breaks ASCII regex.",
            "Evasion Trick 2 • Markdown Link Masking: '[discord.com/nitro](evil.xyz)' renders a blue trusted URL while routing clicks to credential harvesters.",
            "Evasion Trick 3 • Casual Pretexts: Multi-turn openers ('Hey are you free right now?') contain no URLs to slip past entry filters.",
            "Empirical Benchmark: AutoMod regex F1 crashes by 37.2% (0.8598 → 0.4876) under basic evasion."
        ],
        "image": "code_automod_regex_bypass.png",
        "image_caption": "Failure Mode: AutoMod Regex Bypass vs Evasion (-37.2% F1)",
        "script_cue": (
            "To stop these scams, Discord servers usually rely on Discord AutoMod or community bots like MEE6. But almost all of them rely on basic keyword blocklists and regular expressions.\n\n"
            "Scammers easily bypass them using three clever tricks:\n"
            "1. Cyrillic Homoglyphs: Attackers swap English letters for visually identical Russian Cyrillic letters—like using Cyrillic 'о' (Unicode U+043E) instead of English 'o'. "
            "To a human eye, discord.com looks 100% identical. But to a computer's regex matching ASCII bytes, they don't match, so AutoMod lets the scam right through!\n"
            "2. Markdown Masking: Discord chat allows Markdown formatting like [discord.com/nitro](evil.xyz). The chat displays a blue, trusted link, but clicking it sends the victim to a credential stealer.\n"
            "3. Casual Pretexts: Opening with 'Hey, are you free?' with no links at all, waiting for a reply before sending the lure.\n\n"
            "When I benchmarked AutoMod regex against these evasion tricks, its F1-score crashed by 37.2%, dropping from 0.8598 down to 0.4876. That failure motivated my machine learning approach."
        )
    },
    {
        "slide_num": 4,
        "title": "System Architecture: Dual-Stream Feature Fusion",
        "subtitle": "Pairing Semantic Context with Structural Domain Invariants",
        "time": "2:30 - 3:30",
        "action": "[SLIDE: Walk through the two feature streams & explain why XGBoost beats BERT]",
        "bullets": [
            "Core Security Insight: Scammers alter text in seconds, but MUST direct victims to external infrastructure they control.",
            "Stream A (Semantic Meaning): 3,000 TF-IDF word n-grams (unigrams & bigrams) capture high-pressure scam language ('free', 'nitro', 'claim').",
            "Stream B (Structural Invariants): 17 scalar features capture link patterns (homoglyphs, cloaked Markdown, brand edit distance, entropy).",
            "Fused Representation: Concatenates into a 3,017-dimensional vector evaluated by an XGBoost gradient-boosted decision tree ensemble.",
            "Why XGBoost over BERT? Runs in 1.2ms vs 150-300ms on CPU (no chat lag) and avoids subword token fragmentation on Cyrillic letters."
        ],
        "image": "code_feature_extractor.png",
        "image_caption": "Code: 17 Structural Domain Invariants (feature_extractor.py)",
        "script_cue": (
            "On Slide 4 is the solution I designed: a Dual-Stream Feature Fusion Pipeline.\n"
            "The core insight is: Scammers can change their words in five seconds, but to steal credentials, they MUST send you to an external website they control.\n\n"
            "So I split feature extraction into two streams:\n"
            "- Stream A (Semantic Meaning): Takes the message text and extracts 3,000 TF-IDF word features—both unigrams and bigrams—to capture high-pressure scam language like 'free', 'nitro', and 'claim'.\n"
            "- Stream B (Structural Clues): Extracts 17 numerical features that don't depend on specific words: it counts lookalike Russian characters, detects cloaked Markdown links, checks similarity to real brand names, and measures how random the link is.\n\n"
            "I concatenate these into a single 3,017-dimensional vector and pass it to an XGBoost gradient-boosted decision tree ensemble.\n\n"
            "I chose XGBoost over a heavy transformer like BERT for two practical reasons:\n"
            "First, speed: BERT takes 150 to 300 ms on a CPU, which causes chat backlogs on busy servers. XGBoost runs in just 1.2 milliseconds.\n"
            "Second, BERT's subword tokenizer fragments lookalike characters into weird pieces that degrade embeddings, whereas decision trees handle tabular structural rules naturally."
        )
    },
    {
        "slide_num": 5,
        "title": "Mathematical Formulations Demystified",
        "subtitle": "Levenshtein Early Exit, Shannon Entropy, and Minimax Risk",
        "time": "3:30 - 4:30",
        "action": "[SLIDE / FORMULAS: Plain-English explanation of mathematical models]",
        "bullets": [
            "1. Minimum Levenshtein Distance (d_min): Dynamic programming edit distance to canonical platforms (discord.com, steamcommunity.com).",
            "• Optimization: Early-exit check skips O(NM) matrix calculation if absolute string length difference > 4.",
            "2. Shannon Domain Entropy (H(d)): Quantifies character randomness from information theory: H(d) = -Σ p(c) log2(p(c)).",
            "• Natural language domains score 2.0–2.8; automated bot-generated scam strings score > 3.5 (red flag).",
            "3. Minimax Adversarial Formulation: Actively attacks training data with synthetic homoglyphs and disguised links:",
            "• min_θ E [ max_{δ ∈ Δ} L(f_θ(x + δ), y) ] — forces decision trees to learn robust, evasive split boundaries."
        ],
        "image": "math_formulations_card.png",
        "image_caption": "Formulations: Levenshtein, Shannon Entropy & Minimax Risk",
        "script_cue": (
            "On Slide 5, let me explain the three main mathematical formulas powering Stream B in plain terms:\n\n"
            "1. Minimum Levenshtein Distance (d_min):\n"
            "This measures the edit distance—insertions, deletions, or substitutions—between extracted links and real brands like discord.com and steamcommunity.com. "
            "If a scammer sends discoord.com, the distance is only 1. To make this fast, I added an early-exit check: if the length difference between the two words is already greater than 4 characters, "
            "I skip the expensive nested loops entirely because it's impossible for the edit distance to be small.\n\n"
            "2. Shannon Domain Entropy (H(d)):\n"
            "This comes from information theory and measures randomness. Real company names like discord or steam use normal, pronounceable letter combinations, so they have low entropy (between 2.0 and 2.8). "
            "But automated scam bots spit out random, gibberish domains like x7k9-free-nitro.ru. Shannon entropy gives me a single number measuring how scrambled the letters are. Anything above 3.5 is an immediate red flag.\n\n"
            "3. Minimax Adversarial Hardening:\n"
            "Instead of just training on normal scams, I formulated training as a minimax problem: my code actively attacks its own dataset during training with synthetic homoglyphs and disguised links, "
            "forcing the decision trees to learn split rules that survive sneaky tricks."
        )
    },
    {
        "slide_num": 6,
        "title": "Data Engineering & MD5 Deduplication",
        "subtitle": "3,552 Balanced Messages with Leakage Prevention",
        "time": "4:30 - 5:30",
        "action": "[SLIDE / CODE: Explain data provenance, ethics compliance, and deduplication]",
        "bullets": [
            "Data Provenance: 2,000 Hugging Face scams + 21,908 Nikolaischunk malicious domains + 1,500 attack playbooks + 2,500 clean chat logs.",
            "Platform Privacy Compliance: Built strictly from public research data to respect Discord Developer Policy Section 21.",
            "Critical Deduplication Step: Raw Hugging Face data had hundreds of duplicate Nitro spam copies.",
            "MD5 Hash Filtering: Cleaned exact spam duplicates in data_loader.py to prevent train-test memorization leakage.",
            "Final Dataset: 3,552 unique messages split 80% train (2,841), 10% validation (355), 10% clean test (356) + 356 adversarial test samples."
        ],
        "image": "code_data_loader_dedup.png",
        "image_caption": "Code: Threat Feeds & MD5 Hash Deduplication (data_loader.py)",
        "script_cue": (
            "Looking at Slide 6, let's discuss the dataset.\n"
            "To respect Discord's Developer Policy Section 21—which strictly bans saving private user chats for machine learning without consent—I built my dataset entirely from public research data:\n"
            "- 2,000 verified phishing messages from Hugging Face.\n"
            "- 21,908 verified malicious domains from the Nikolaischunk threat feed.\n"
            "- 1,500 modern attack playbooks modeling fake game playtests and OAuth traps.\n"
            "- Balanced against 2,500 clean, everyday gaming messages from open research logs.\n\n"
            "But here was the most critical data engineering step: MD5 deduplication.\n"
            "The raw Hugging Face data had hundreds of duplicate copies of the exact same Nitro gift spam. If I hadn't filtered them out, the model would have memorized those exact messages and cheated on the test set.\n"
            "Using an MD5 hash and text-normalization filter in data_loader.py, I eliminated all duplicate spam copies, producing a clean, balanced corpus of 3,552 unique messages split 80% train, 10% validation, and 10% test."
        )
    },
    {
        "slide_num": 7,
        "title": "Showcase Pipeline: Model Progression & Justifications",
        "subtitle": "Running 'py run_showcase_pipeline.py' & Benchmarking 6 Models (Tables I & II)",
        "time": "5:30 - 7:00",
        "action": "[TERMINAL: Run 'py run_showcase_pipeline.py' in VS Code & explain model choices]",
        "bullets": [
            "Master Showcase Script: 'py run_showcase_pipeline.py' runs all 5 ML steps end-to-end in just 17 seconds.",
            "Step 1 • Ingestion: Deduplicates 6,000 raw samples to 3,552 unique messages via MD5 hashing to prevent test memorization.",
            "Step 2 • Baseline Justifications: AutoMod regex crashes by -37.2% F1. Naive Bayes, LogReg, and SVM drop to 0.44-0.49 recall because Cyrillic letters are OOV.",
            "Step 3 • Fused Tree Ensembles: Random Forest (bagging) scores 0.7273 F1 in 3.4ms; XGBoost (gradient boosting) targets hard edge cases, scoring 0.8078 F1 in 1.2ms.",
            "Step 4 • Feature Ablation (Table II): Stream A (text alone) drops -34% under attack; Stream B (structure alone) achieves 0.7748 F1 (+14.1% over text)!"
        ],
        "image": "workbench_analytics.png",
        "image_caption": "Live Dashboard: Model Analytics, ROC Curves & Ablation",
        "script_cue": (
            "Now let's examine our experimental results. In my terminal, I'm going to run my master pipeline script: py run_showcase_pipeline.py.\n\n"
            "Look at how fast this executes—in just seventeen seconds, it executes the entire machine learning pipeline end-to-end: "
            "data ingestion, baseline evaluations, dual-stream training, ablation analysis, and adversarial hardening.\n\n"
            "Let me explain what is happening on screen and why I tested and chose each specific model:\n\n"
            "1. Step 1 (Data Ingestion & Deduplication): Notice that it loaded 6,000 raw messages and deduplicated them down to 3,552 unique messages. "
            "That eliminated hundreds of duplicate Nitro spam copies so the model wouldn't memorize the training set.\n\n"
            "2. Step 2 (Baseline Models Benchmark — Table I): Why did I evaluate AutoMod, Naive Bayes, Logistic Regression, and SVM? "
            "Because I needed to test whether standard industry defenses and traditional NLP models could handle Discord phishing. "
            "As you can see in Table I: on clean text, they all score above 0.96 F1. But under adversarial evasion, AutoMod regex crashes by 37.2% down to 0.4876 F1 because regex breaks when letters are swapped. "
            "Naive Bayes, Logistic Regression, and SVM all collapse to around 0.44 to 0.49 recall because mutated Russian letters fall completely outside their vocabulary dictionary!\n\n"
            "3. Step 3 (Dual-Stream Fused Models — Random Forest vs. XGBoost): Why did I compare Random Forest against XGBoost on the 3,017 fused features? "
            "Both models use decision trees, which naturally handle tabular data like link counts, edit distance, and entropy. Random Forest uses bagging, which scored 0.7273 F1 under attack, but takes 3.4 milliseconds. "
            "I chose XGBoost as our primary model because gradient boosting builds sequential trees that specifically target previously misclassified edge cases. It achieved 0.8078 F1 before hardening and runs in just 1.2 milliseconds on CPU—which is critical for live Discord server throughput.\n\n"
            "4. Step 4 (3-Way Feature Ablation — Table II): Why run an ablation study? To prove whether Stream B (the 17 structural clues) actually adds value. "
            "Look at the numbers: Stream A (text alone) crashes by -34% under attack. But Stream B alone gets 0.7748 F1—beating text alone by 14.1%! This proves that domain edit distance and entropy stay invariant even when the attacker scrambles the words."
        )
    },
    {
        "slide_num": 8,
        "title": "Adversarial Hardening & Honest Review of 100% Recall",
        "subtitle": "Table III: Minimax Training, Generator Overlap, and 5-Fold CV Variance",
        "time": "7:00 - 8:00",
        "action": "[SLIDE: Discuss Table III results, 100% recall critique, and cross-validation]",
        "bullets": [
            "Minimax Hardening: Augmenting 25% of training scam samples with homoglyphs and Markdown disguises recovers adversarial F1 to 0.9780.",
            "The 100% Recall Artifact: The model caught 178 of 178 test scams (1.0000 recall).",
            "• Candid Scientific Critique: Both training augmentation and test evaluation used 'build_adversarial_variant'. In this closed distribution, homoglyph_count >= 1 became a near-perfect split rule (jumping from #14 to #5 in tree importance).",
            "5-Fold Cross-Validation: With randomized mutation seeds, achieves 0.9888 ± 0.0112 recall and 0.9780 ± 0.0094 F1.",
            "Real-World Zero-Day Limitations: Unseen Unicode scripts, RTL override characters, and image QR codes will inevitably lower open-world recall."
        ],
        "image": "hardened_validation_analysis.png",
        "image_caption": "Audit: XGBoost Gain Shift & 5-Fold CV Variance",
        "script_cue": (
            "Now in Step 5 of the pipeline and on Slide 8, let's look at Minimax Adversarial Hardening:\n\n"
            "Why did I add adversarial hardening?\n"
            "Because a standard model only learns from clean historical data. By actively injecting synthetic lookalike characters and disguised links into 25% of training scams, "
            "the decision trees were forced to learn split rules that survive evasion. After hardening, adversarial F1 recovered to 0.9780, catching 178 out of 178 test scams—a 100% recall.\n\n"
            "Now, Professor, I want to address this 100% recall with complete scientific honesty:\n"
            "Whenever you see 100% in machine learning, that is usually a red flag. In my case, there is a clear reason why it happened: "
            "Because I used the same mutation script (build_adversarial_variant) to create the training mutations as I did to evaluate the test set, the decision trees learned that homoglyph_count >= 1 was an easy shortcut! "
            "That feature jumped from the #14 feature all the way up to the #5 most important feature in tree gain.\n\n"
            "In the open real world against brand-new zero-day attacks, recall will naturally be lower. "
            "That is why I ran 5-fold cross-validation with randomized mutation seeds: across the 5 folds, the model achieved 0.9888 ± 0.0112 recall and 0.9780 ± 0.0094 F1. "
            "That confirms my structural features are genuinely robust within a tight 1% variance."
        )
    },
    {
        "slide_num": 9,
        "title": "Live Demonstration: Classifier & SHAP Explainability",
        "subtitle": "Real-Time 1.2ms Inference on Angular 18 & FastAPI",
        "time": "8:00 - 11:15",
        "action": "[BROWSER: http://localhost:4200/ - Live inference on Presets 1, 2, 3 & SHAP bars]",
        "bullets": [
            "Full-Stack Architecture: Angular 18 (Port 4200) frontend communicating with FastAPI (Port 8000) backend in 1.2 ms.",
            "Live Test 1 • Benign Chat: 'Hey man, hopping on Valorant tonight?' → 0.02% scam probability (Green Approved, SHAP negative push).",
            "Live Test 2 • Classic Nitro: '@everyone Steam free nitro https://discord-nitro-gift.ru/claim' → 99.85% (AUTO-QUARANTINE, urgency + domain flags).",
            "Live Test 3 • Cyrillic Homoglyph: 'https://dіscord.com/gifts' (Cyrillic 'і' U+0456) → AutoMod misses, our model flags at 99.42%!",
            "Local SHAP Attribution: Feature importance bars clearly show the exact structural rules that triggered the quarantine verdict."
        ],
        "image": "classifier_shap_demo.png",
        "image_caption": "Live Dashboard: 1.2ms Classifier & SHAP Explainability",
        "script_cue": (
            "Now let's transition to the live system demonstration. I wanted to build a complete, production-ready tool. "
            "So I wrapped the trained models and feature extractor in a FastAPI backend running on port 8000, and I built this modern dashboard in Angular 18 running on port 4200.\n\n"
            "At the top, you can see our live status banner: connected to FastAPI, using model xgboost_hardened.joblib, and showing an end-to-end latency counter currently at 1.2 milliseconds.\n\n"
            "Let's test the detector across real-world test cases right now:\n\n"
            "1. Clean Everyday Chat: 'Hey man, are we still hopping on Valorant tonight?' -> I click Analyze: Inference takes just 1.1 ms. "
            "Risk gauge is completely green at 0.02% scam probability. Verdict: APPROVED (BENIGN). SHAP green bars pointing left show the absence of URLs and ordinary words actively convinced the model the message is safe.\n\n"
            "2. Classic Unmutated Nitro Scam: '@everyone Steam free 3 months Discord Nitro: https://discord-nitro-gift.ru/claim' -> Gauge turns bright red: 99.85% scam probability! "
            "AUTO-QUARANTINE triggered. Structural clues: min_levenshtein_discord = 1, suspicious .ru domain, 3 urgency tokens. SHAP waterfall shows these pushed the score straight into quarantine.\n\n"
            "3. The Tricky Cyrillic Homoglyph Attack: 'Steam partnership: claim complimentary subscription at https://dіscord.com/gifts' (with Cyrillic 'і' U+0456). "
            "Regex looking for discord.com returns False and misses this scam! Our model catches it instantly: 99.42% scam probability in 1.2 ms! "
            "homoglyph_count = 1 highlighted in amber. The hardened trees intercept the scam effortlessly."
        )
    },
    {
        "slide_num": 10,
        "title": "Live Demonstration: Interactive Pop-Out Chatbox & Wrap-Up",
        "subtitle": "Simulated Discord Chat, Architectural Post-Mortem, and Key Takeaways",
        "time": "11:15 - 14:00",
        "action": "[BROWSER: Pop-Out Chat Playground -> CAMERA: Post-Mortem & Wrap-Up]",
        "bullets": [
            "Live Test 4 • Pop-Out Chatbox: Floating action button simulates real Discord conversation with instant 1.2ms red quarantine banners.",
            "Post-Mortem & Initial Failure: Originally planned to use user account metadata (age, mutual servers, avatar, message frequency).",
            "Why We Abandoned Metadata: Discord bot sandboxing blocks reading private DMs (403 Forbidden) and Policy Section 21 bans storing chat data.",
            "The Pivot: Inspecting only raw message payloads made the detector 100% self-contained, fast, and privacy-preserving.",
            "Final Scorecard: 0.9777 clean F1, 0.9780 hardened F1, 1.2ms CPU latency, production-ready full-stack Angular 18 + FastAPI tool."
        ],
        "image": "popout_chat_demo.png",
        "image_caption": "Live Dashboard: Simulated Discord Pop-Out Chatbox",
        "script_cue": (
            "To see how this works in a real chat environment, let's look at Slide 10 and test my Pop-Out Chatbox.\n\n"
            "Down here in the bottom-right corner, I click this floating button. It opens an inline chat window simulating a live Discord server. "
            "Let's type a normal message: 'Hey, did you finish the homework?' Sent—it appears with a green approved badge. "
            "Now let's simulate the compromised account replying with a fake game test: 'Yeah! My buddy released a game demo on Steam, can you test it? https://steamcommunity-beta.top/setup.exe' "
            "I hit Enter: Instantly—in 1.2 milliseconds—the system flags the message in bright red with an AUTO-QUARANTINED warning overlay! The dangerous link is blocked from rendering clickable in chat, protecting users from accidental clicks.\n\n"
            "Before concluding, I want to share a key learning outcome: my Architectural Post-Mortem and Initial Failure.\n"
            "When I originally started in September, my proposal was very different: I planned to build a Discord bot that checked user account metadata—account age, mutual server counts, avatar presence, and message frequency. "
            "That approach hit two brick walls within the first three weeks: Discord bot sandboxing (cannot inspect private DMs between users) and Discord Developer Policy Section 21 (bans saving user chat data for machine learning). "
            "Ditching user metadata was the best engineering pivot I made. By inspecting only the raw message payload and URLs, the final detector requires zero access to private user databases or chat history. It is completely self-contained, privacy-preserving, and fast.\n\n"
            "To wrap up, my top three engineering takeaways:\n"
            "1. Text Models Are Fragile Under Attack: Security classifiers must be grounded in structural domain invariants that attackers cannot easily hide.\n"
            "2. Latency is a Production Constraint: An XGBoost ensemble running in 1.2 ms provides the throughput needed for live moderation without server chat lag.\n"
            "3. Verify API Boundaries Early: Always verify what data a platform permits you to access before designing machine learning features.\n\n"
            "Final results: On 3,552 messages, my model achieves 0.9777 clean F1, recovers to 0.9780 adversarial F1 under evasion attacks (where AutoMod crashes by 37.2%), runs in 1.2 ms on CPU, and is fully deployed across FastAPI and Angular 18.\n"
            "All code, models, reports, and slide decks are available in my GitHub repository. Thank you so much for your time and guidance, Professor. I'm ready for your questions!"
        )
    }
]


# ==============================================================================
# 1. BUILD POWERPOINT (.PPTX)
# ==============================================================================

def build_pptx(output_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for data in SLIDES_DATA:
        slide = prs.slides.add_slide(blank_layout)

        # Background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()

        # Top Accent Bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = ACCENT_CYAN
        top_bar.line.fill.background()

        # Slide Number Badge & Timestamp
        badge_box = slide.shapes.add_textbox(Inches(10.0), Inches(0.28), Inches(2.8), Inches(0.5))
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.RIGHT
        r_b = p_b.add_run()
        r_b.text = f"Slide {data['slide_num']} of 10  |  {data['time']}"
        r_b.font.size = Pt(11)
        r_b.font.bold = True
        r_b.font.color.rgb = ACCENT_CYAN

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.2), Inches(1.0))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = data["title"]
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Subtitle
        p_sub = tf_t.add_paragraph()
        p_sub.text = data["subtitle"]
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = TEXT_MUTED

        # Action Cue Banner
        action_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.42))
        action_box.fill.solid()
        action_box.fill.fore_color.rgb = CARD_BG
        action_box.line.color.rgb = ACCENT_CYAN
        tf_a = action_box.text_frame
        p_a = tf_a.paragraphs[0]
        p_a.alignment = PP_ALIGN.LEFT
        r_a = p_a.add_run()
        r_a.text = f"  PRESENTER ACTION: {data['action']}"
        r_a.font.size = Pt(10.5)
        r_a.font.bold = True
        r_a.font.color.rgb = ACCENT_CYAN

        # Two-column layout
        has_image = data["image"] and os.path.exists(os.path.join(ASSETS_DIR, data["image"]))
        content_w = Inches(5.9) if has_image else Inches(11.733)

        # Bullets Container
        tb_body = slide.shapes.add_textbox(Inches(0.8), Inches(1.98), content_w, Inches(5.1))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True

        for i, b in enumerate(data["bullets"]):
            p = tf_body.add_paragraph() if i > 0 else tf_body.paragraphs[0]
            p.space_after = Pt(5)
            p.level = 1 if b.strip().startswith("•") or b.strip().startswith("->") or b.strip().startswith("- ") else 0
            clean_b = b.replace("->", "•").replace("- ", "• ")
            r = p.add_run()
            r.text = clean_b
            r.font.size = Pt(11.0 if p.level == 0 else 10.0)
            r.font.color.rgb = TEXT_WHITE if p.level == 0 else TEXT_MUTED

        # Add Image if present
        if has_image:
            img_path = os.path.join(ASSETS_DIR, data["image"])
            # Image card background container
            img_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.98), Inches(5.633), Inches(4.7))
            img_card.fill.solid()
            img_card.fill.fore_color.rgb = CARD_BG
            img_card.line.color.rgb = RGBColor(50, 55, 66)

            # Caption Pill inside card
            cap_box = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.4), Inches(0.35))
            tf_cap = cap_box.text_frame
            tf_cap.word_wrap = True
            p_cap = tf_cap.paragraphs[0]
            p_cap.alignment = PP_ALIGN.LEFT
            r_cap = p_cap.add_run()
            r_cap.text = f"VISUAL: {data['image_caption']}"
            r_cap.font.size = Pt(9.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = ACCENT_CYAN

            # Actual Image placement
            slide.shapes.add_picture(img_path, Inches(7.0), Inches(2.45), width=Inches(5.433))

        # Presenter Notes in PPTX
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = (
            f"SLIDE {data['slide_num']} OF 10  |  TIMESTAMP: {data['time']}\n"
            f"ACTION: {data['action']}\n"
            f"VISUAL: {data.get('image_caption', 'N/A')}\n\n"
            f"SPOKEN SCRIPT / TALKING POINTS FOR PROFESSOR:\n"
            f"{data['script_cue']}"
        )

    try:
        prs.save(output_path)
        print(f"PowerPoint slide deck saved successfully to: {output_path}")
    except PermissionError:
        alt_path = output_path.replace(".pptx", "_UPDATED.pptx")
        prs.save(alt_path)
        print(f"Notice: '{output_path}' is currently open in Microsoft PowerPoint.")
        print(f"Saved updated PowerPoint slide deck to: {alt_path}")


# ==============================================================================
# 2. BUILD INTERACTIVE HTML5 SLIDE DECK
# ==============================================================================

def build_html(output_path):
    slides_html_blocks = []

    for d in SLIDES_DATA:
        bullets_li = ""
        for b in d["bullets"]:
            is_sub = b.strip().startswith("•") or b.strip().startswith("->") or b.strip().startswith("- ")
            clean_b = b.replace("->", "↳ ").replace("- ", "↳ ")
            cls = "sub-bullet" if is_sub else "main-bullet"
            bullets_li += f'<li class="{cls}">{clean_b}</li>\n'

        image_html = ""
        if d["image"]:
            img_rel = f"slides_assets/{d['image']}"
            caption = d.get("image_caption", "Demonstration Visual")
            image_html = f'''
            <div class="slide-image-col">
                <div class="image-wrapper">
                    <div class="image-header">
                        <span class="image-tag">VISUAL</span>
                        <span class="image-title">{caption}</span>
                    </div>
                    <img src="{img_rel}" alt="{caption}" />
                </div>
            </div>
            '''

        script_dialogue_html = "<br><br>".join([f"<p>{para.strip()}</p>" for para in d["script_cue"].split("\n\n") if para.strip()])

        slide_block = f'''
        <section class="slide" data-slide="{d['slide_num']}">
            <div class="slide-header">
                <div class="slide-title-wrap">
                    <span class="slide-num-pill">Slide {d['slide_num']} / 10</span>
                    <span class="slide-time-pill"><i class="clock-icon">⏱</i> {d['time']}</span>
                    <h2>{d['title']}</h2>
                    <p class="subtitle">{d['subtitle']}</p>
                </div>
            </div>

            <div class="action-banner">
                <span class="action-badge">PRESENTER ACTION</span>
                <span class="action-text">{d['action']}</span>
            </div>

            <div class="slide-content two-col">
                <div class="slide-text-col">
                    <ul class="bullet-list">
                        {bullets_li}
                    </ul>
                </div>
                {image_html}
            </div>

            <div class="speaker-notes-box">
                <div class="notes-header">
                    <strong>🎙 Presenter Spoken Dialogue ({d['time']})</strong>
                    <button class="toggle-notes-btn" onclick="toggleNotes(this)">Show Full Dialogue</button>
                </div>
                <div class="notes-body">
                    {script_dialogue_html}
                    <p class="hint">Consult <code>DEMO_VIDEO_PRESENTATION_SCRIPT.md</code> for additional checklist items and transitions.</p>
                </div>
            </div>
        </section>
        '''
        slides_html_blocks.append(slide_block)

    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Scam Detection - 12-to-15 Min Demo Presentation Slides</title>
    <style>
        :root {{
            --bg-dark: #121418;
            --card-bg: #1c1f26;
            --border-color: #2e3440;
            --accent-cyan: #00d2ff;
            --accent-purple: #9b59b6;
            --accent-green: #2ecc71;
            --text-main: #f0f3f6;
            --text-muted: #9aa4b2;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{
            background: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}
        /* Top Navigation Bar */
        .top-navbar {{
            background: #181b22;
            border-bottom: 1px solid var(--border-color);
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .brand-title {{ font-size: 15px; font-weight: 700; color: var(--accent-cyan); display: flex; align-items: center; gap: 8px; }}
        .nav-controls {{ display: flex; gap: 10px; align-items: center; }}
        .nav-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .nav-btn:hover {{ background: var(--border-color); color: var(--accent-cyan); }}
        .nav-btn.primary {{ background: #007acc; border-color: #007acc; }}
        .counter-pill {{ font-size: 13px; color: var(--text-muted); font-weight: 600; padding: 0 8px; }}

        /* Presentation Slide Area */
        .presentation-container {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 24px;
        }}
        .slide-deck {{
            width: 100%;
            max-width: 1300px;
            min-height: 720px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }}
        .slide {{
            display: none;
            padding: 32px 40px;
            animation: fadeIn 0.3s ease;
        }}
        .slide.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        /* Slide Components */
        .slide-header {{ margin-bottom: 16px; }}
        .slide-num-pill {{
            background: rgba(0, 210, 255, 0.12);
            color: var(--accent-cyan);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .slide-time-pill {{
            background: rgba(46, 204, 113, 0.15);
            color: var(--accent-green);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 12px;
            margin-left: 8px;
        }}
        h2 {{ font-size: 25px; font-weight: 800; color: var(--text-main); margin-top: 8px; }}
        .subtitle {{ font-size: 13.5px; color: var(--text-muted); margin-top: 4px; white-space: pre-line; }}

        .action-banner {{
            background: rgba(0, 210, 255, 0.08);
            border-left: 4px solid var(--accent-cyan);
            padding: 8px 14px;
            border-radius: 4px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .action-badge {{
            background: var(--accent-cyan);
            color: #000;
            font-size: 10px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.5px;
        }}
        .action-text {{ font-size: 12.5px; font-weight: 600; color: #d0f0ff; }}

        /* Grid */
        .slide-content.two-col {{ display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 28px; align-items: start; }}

        .bullet-list {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
        .bullet-list li.main-bullet {{
            position: relative;
            padding-left: 20px;
            font-size: 14px;
            line-height: 1.45;
            color: var(--text-main);
        }}
        .bullet-list li.main-bullet::before {{
            content: "•";
            position: absolute;
            left: 4px;
            color: var(--accent-cyan);
            font-size: 18px;
            top: -2px;
        }}
        .bullet-list li.sub-bullet {{
            padding-left: 36px;
            font-size: 13px;
            line-height: 1.4;
            color: var(--text-muted);
            position: relative;
        }}
        .bullet-list li.sub-bullet::before {{
            content: "↳";
            position: absolute;
            left: 20px;
            color: var(--text-muted);
        }}

        /* Image Column */
        .slide-image-col {{ display: flex; justify-content: center; }}
        .image-wrapper {{
            background: #14171d;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            width: 100%;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}
        .image-header {{
            background: #20242d;
            padding: 6px 12px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .image-tag {{
            background: rgba(0, 210, 255, 0.15);
            color: var(--accent-cyan);
            font-size: 9px;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        .image-title {{ font-size: 11px; font-weight: 600; color: var(--text-muted); }}
        .image-wrapper img {{
            width: 100%;
            display: block;
            object-fit: contain;
            max-height: 380px;
        }}

        /* Speaker Notes Box */
        .speaker-notes-box {{
            margin-top: 24px;
            background: #15181f;
            border: 1px solid #282e3b;
            border-radius: 6px;
            padding: 12px 16px;
        }}
        .notes-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--accent-cyan);
        }}
        .toggle-notes-btn {{
            background: none;
            border: 1px solid #333a4a;
            color: var(--text-muted);
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 4px;
            cursor: pointer;
        }}
        .toggle-notes-btn:hover {{ color: var(--text-main); border-color: var(--accent-cyan); }}
        .notes-body {{
            display: none;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #232834;
            font-size: 12.5px;
            line-height: 1.5;
            color: #c0c8d4;
        }}
        .notes-body.open {{ display: block; }}
        .notes-body p {{ margin-bottom: 8px; }}
        .notes-body .hint {{ font-size: 11px; color: var(--text-muted); margin-top: 8px; font-style: italic; }}

        /* Navigation Footer */
        .footer-legend {{
            padding: 12px 24px;
            background: #14171d;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: center;
            gap: 24px;
            font-size: 12px;
            color: var(--text-muted);
        }}
        .kbd-key {{
            background: var(--card-bg);
            border: 1px solid #3a4252;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            color: var(--text-main);
            font-weight: 700;
        }}

        /* Bottom thumbnails bar */
        .thumbs-bar {{
            background: #181b22;
            border-top: 1px solid var(--border-color);
            padding: 8px 16px;
            display: flex;
            gap: 8px;
            overflow-x: auto;
            justify-content: center;
        }}
        .thumb-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11.5px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}
        .thumb-btn:hover {{ background: #262c37; color: var(--text-main); }}
        .thumb-btn.active {{ border-color: var(--accent-cyan); color: var(--accent-cyan); background: rgba(0, 210, 255, 0.08); }}
    </style>
</head>
<body>
    <header class="top-navbar">
        <div class="brand-title">
            <span>🛡 Discord Scam Detection</span>
            <span style="color: var(--text-muted); font-weight: 400;">| Final Demo Slides</span>
        </div>
        <div class="nav-controls">
            <button class="nav-btn" onclick="prevSlide()">◀ Previous</button>
            <span class="counter-pill" id="slideIndicator">1 / 10</span>
            <button class="nav-btn primary" onclick="nextSlide()">Next ▶</button>
            <button class="nav-btn" onclick="toggleAllNotes()">Toggle Script Cues</button>
            <button class="nav-btn" onclick="toggleFullScreen()">⛶ Fullscreen</button>
        </div>
    </header>

    <main class="presentation-container">
        <div class="slide-deck">
            {''.join(slides_html_blocks)}
        </div>
    </main>

    <div class="thumbs-bar">
        {''.join([f'<button class="thumb-btn { "active" if i == 0 else "" }" onclick="goToSlide({i+1})">Slide {i+1}</button>' for i in range(10)])}
    </div>

    <footer class="footer-legend">
        <span><span class="kbd-key">◀</span> / <span class="kbd-key">▶</span> Navigate</span>
        <span><span class="kbd-key">Space</span> Next Slide</span>
        <span><span class="kbd-key">N</span> Toggle Speaking Notes</span>
        <span><span class="kbd-key">F</span> Toggle Fullscreen</span>
    </footer>

    <script>
        let currentSlide = 1;
        const totalSlides = 10;

        function showSlide(n) {{
            if (n < 1) n = 1;
            if (n > totalSlides) n = totalSlides;
            currentSlide = n;

            document.querySelectorAll('.slide').forEach((s, idx) => {{
                s.classList.toggle('active', (idx + 1) === currentSlide);
            }});

            document.querySelectorAll('.thumb-btn').forEach((b, idx) => {{
                b.classList.toggle('active', (idx + 1) === currentSlide);
            }});

            document.getElementById('slideIndicator').textContent = `${{currentSlide}} / ${{totalSlides}}`;
        }}

        function nextSlide() {{ showSlide(currentSlide + 1); }}
        function prevSlide() {{ showSlide(currentSlide - 1); }}
        function goToSlide(n) {{ showSlide(n); }}

        function toggleNotes(btn) {{
            const body = btn.closest('.speaker-notes-box').querySelector('.notes-body');
            body.classList.toggle('open');
            btn.textContent = body.classList.contains('open') ? 'Hide Dialogue' : 'Show Full Dialogue';
        }}

        function toggleAllNotes() {{
            const bodies = document.querySelectorAll('.notes-body');
            const btns = document.querySelectorAll('.toggle-notes-btn');
            const anyOpen = Array.from(bodies).some(b => b.classList.contains('open'));
            bodies.forEach(b => b.classList.toggle('open', !anyOpen));
            btns.forEach(btn => btn.textContent = !anyOpen ? 'Hide Dialogue' : 'Show Full Dialogue');
        }}

        function toggleFullScreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else if (document.exitFullscreen) {{
                document.exitFullscreen();
            }}
        }}

        // Keyboard controls
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                nextSlide();
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                prevSlide();
            }} else if (e.key.toLowerCase() === 'n') {{
                toggleAllNotes();
            }} else if (e.key.toLowerCase() === 'f') {{
                toggleFullScreen();
            }}
        }});
    </script>
</body>
</html>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Interactive HTML slide deck saved successfully to: {output_path}")


if __name__ == "__main__":
    print("Building synchronized presentation slides...")
    pptx_path = os.path.join(SCRIPT_DIR, "DEMO_PRESENTATION_SLIDES.pptx")
    html_path = os.path.join(SCRIPT_DIR, "DEMO_PRESENTATION_SLIDES.html")

    build_pptx(pptx_path)
    build_html(html_path)
    print("\nAll presentation slides successfully synchronized with script!")
