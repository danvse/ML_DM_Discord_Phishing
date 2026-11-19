"""
Synchronizes both:
1. docs/slides/DEMO_PRESENTATION_SLIDES.pptx (16:9 Widescreen Microsoft PowerPoint Deck)
2. docs/slides/DEMO_PRESENTATION_SLIDES.html (Interactive HTML5 Slide Deck)

High-level, student-friendly, and streamlined for an accessible 10-12 minute presentation.
Direct 1:1 synchronization with docs/slides/DEMO_VIDEO_PRESENTATION_SCRIPT.md
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
        "title": "Dual-Stream Detection of Discord Phishing",
        "subtitle": "Machine Learning & Data Mining | Final Project Demo\nTeam #18: Edwin Lin (Solo Project)",
        "time": "0:00 - 0:45",
        "action": "[ON CAMERA: Presenter intro with pinned webcam — ~11-min Roadmap]",
        "bullets": [
            "The Problem: Attackers hijack Discord accounts and trick friends into clicking dangerous links.",
            "The Big Idea: Scammers can easily rewrite their words, but their links always leave structural clues.",
            "Our Solution: A dual-stream machine learning model combining message words with link structure.",
            "Real-World Speed: Analyzes incoming messages in just 1.2 milliseconds—zero chat lag for active servers.",
            "Presentation Roadmap: The Threat • Filter Failures • Our Model • Pipeline Run • Live Web Demo."
        ],
        "image": "pipeline_overview_card.png",
        "image_caption": "High-Level Architecture: Dual-Stream Pipeline & Decision Policy",
        "script_cue": (
            "Hello Professor! Welcome to my final project demonstration for Machine Learning and Data Mining. "
            "My name is Edwin Lin, presenting Team 18 as a solo project.\n\n"
            "Today, I'm presenting Dual-Stream Detection of Discord Phishing Campaigns.\n\n"
            "Over the next eleven to twelve minutes, I'll walk you through how this system works:\n"
            "First, why Discord scams trick so many people and why normal keyword filters fail.\n"
            "Second, how my dual-stream machine learning approach catches tricky links without lagging the server.\n"
            "Third, we'll see a quick 17-second live run in the terminal comparing different models.\n"
            "And finally, I'll walk you through my live web application with real-world test cases and our pop-out chatbox."
        )
    },
    {
        "slide_num": 2,
        "title": "Why Discord Scams are So Dangerous",
        "subtitle": "High Trust Between Friends & Rapid Server Spreading",
        "time": "0:45 - 1:30",
        "action": "[SLIDE: Explain the 4 common scam tricks & lateral spreading]",
        "bullets": [
            "Built-in Trust: Discord is made of private servers and friend chats, not public feeds. People naturally trust friends.",
            "Account Hijacking: Once an account is hacked, automated bots blast scam links to all their friends and servers.",
            "Attack Pretext 1 • Fake Nitro: 'Steam is giving away 3 months of Discord Nitro!'",
            "Attack Pretext 2 • Fake Game Tests: 'My friend made an indie game, can you test it?' (installs malware).",
            "Attack Pretext 3 • Tournament Voting: 'Vote for my team' links that steal your account login token.",
            "Attack Pretext 4 • Crypto Drainers: Fake giveaways designed to empty connected digital wallets."
        ],
        "image": "code_adversarial_perturbation.png",
        "image_caption": "Attack Tactics: Lookalike Letters & Disguised Links",
        "script_cue": (
            "On Slide 2, let's look at why Discord scams work so well.\n\n"
            "Unlike Twitter or public forums, Discord is built on personal friendships and private gaming servers. "
            "When an account gets compromised—often through a fake QR code or malware—automated bots hijack it and immediately message the victim's friends list.\n\n"
            "Because the message comes from a close friend you talk to every day, your guard is down.\n\n"
            "Attackers usually use four pretexts: free Discord Nitro, asking you to test a new indie game demo, voting for a gaming team, or fake crypto giveaways. "
            "Once someone clicks, their account gets compromised too, spreading the infection across the whole server."
        )
    },
    {
        "slide_num": 3,
        "title": "Why Traditional Filters Fail",
        "subtitle": "How Attackers Easily Bypass Basic Rules & Regular Expressions",
        "time": "1:30 - 2:30",
        "action": "[SLIDE: Show how scammers trick traditional filters]",
        "bullets": [
            "The Status Quo: Built-in tools like Discord AutoMod search for specific banned words and exact website links.",
            "Bypass 1 • Lookalike Letters: Replacing English 'o' with Russian 'о'. They look 100% identical to our eyes, but fool computer filters!",
            "Bypass 2 • Disguised Links: Using chat formatting like [discord.com](evil.com). The blue text looks official, but clicking opens a scam site.",
            "Bypass 3 • Friendly Openers: Starting with 'Hey, are you free?' with no link at all, waiting for a reply first.",
            "The Result: Traditional filters crash by 37.2% as soon as attackers change a few letters."
        ],
        "image": "code_automod_regex_bypass.png",
        "image_caption": "Filter Breakdown: AutoMod Regex Accuracy Drops by 37.2%",
        "script_cue": (
            "Slide 3 shows why basic rules and keyword blocklists fail.\n\n"
            "Most Discord servers use AutoMod or moderation bots that look for banned words or specific URLs. "
            "But scammers easily get around them using three simple tricks:\n\n"
            "First, lookalike letters—technically called homoglyphs. For example, replacing the English letter 'o' with the Russian Cyrillic letter 'о'. "
            "To a human, discord.com looks completely normal. But to a rule looking for ASCII English letters, it doesn't match at all, so the scam slips right past!\n\n"
            "Second, disguised links: using Markdown to make the link text look like official Discord, while the actual click opens a malicious site.\n\n"
            "And third, friendly conversational messages that don't send the link until you reply.\n\n"
            "When I tested traditional filters against these tricks, their accuracy plummeted by nearly 40%. We need smart machine learning, not just static rules."
        )
    },
    {
        "slide_num": 4,
        "title": "Our Solution: Dual-Stream Machine Learning",
        "subtitle": "Looking at Both the Words and the Structure of the Link",
        "time": "2:30 - 3:30",
        "action": "[SLIDE: Explain the two streams and why XGBoost was chosen]",
        "bullets": [
            "Key Insight: Scammers can rewrite their message in seconds, but to steal your account, they MUST send you to their website!",
            "Stream A (The Words): Checks for pushy scam words ('free', 'gift', 'nitro', 'claim').",
            "Stream B (The Link Clues): Checks 17 structural hints that don't depend on specific words:",
            "  • Does the link use foreign lookalike letters?",
            "  • Is it trying to imitate a famous brand like Discord or Steam?",
            "  • Does the website domain look like random, messy gibberish?",
            "Model Choice: We use XGBoost decision trees. It runs in just 1.2 ms, while heavy neural networks like BERT take 300 ms and cause chat lag."
        ],
        "image": "code_feature_extractor.png",
        "image_caption": "Stream B: 17 Structural Domain Invariants",
        "script_cue": (
            "On Slide 4 is my solution: a Dual-Stream Detection Pipeline.\n\n"
            "The main insight here is simple: scammers can change their message wording in five seconds, but they cannot hide their malicious website link.\n\n"
            "So I built two streams:\n"
            "Stream A looks at the message words: it checks for pushy scam language like 'free', 'claim', and 'nitro'.\n"
            "Stream B looks at the link itself: it extracts 17 structural clues that attackers cannot easily disguise. "
            "It checks for lookalike letters, disguised link targets, how close the link is to real brand names, and whether the domain looks like random gibberish.\n\n"
            "We feed both streams into XGBoost, a fast tree-based machine learning model.\n\n"
            "I chose XGBoost over a heavy deep learning model like BERT for one big reason: speed. "
            "BERT takes around 300 milliseconds on a CPU, which would cause server chat queues to back up. XGBoost runs in just 1.2 milliseconds."
        )
    },
    {
        "slide_num": 5,
        "title": "Smart Clues: How the Model Catches Fakes",
        "subtitle": "Brand Similarity, Gibberish Scores, and Practice Against Tricks",
        "time": "3:30 - 4:30",
        "action": "[SLIDE: High-level explanation of the 3 detection concepts]",
        "bullets": [
            "Clue 1 • Brand Lookalike Score (Edit Distance):",
            "  • Measures how many letter changes it takes to turn the link into 'discord.com' or 'steamcommunity.com'.",
            "  • 'discoord.com' is only 1 letter off—immediate red flag! We use a smart shortcut to keep it super fast.",
            "Clue 2 • Gibberish Score (Domain Randomness):",
            "  • Real company names use smooth, readable words.",
            "  • Automated scam bots generate random strings like 'x7k9-free-nitro.ru'. Our score catches this messy letter randomness.",
            "Clue 3 • Practice Against Sneaky Tricks (Adversarial Training):",
            "  • During training, we intentionally attacked our own model with disguised links so it learned how to catch them."
        ],
        "image": "math_formulations_card.png",
        "image_caption": "Detection Clues: Brand Distance, Randomness & Hardening",
        "script_cue": (
            "Slide 5 shows the three intuitive ideas that give Stream B its power:\n\n"
            "First, a Brand Lookalike Check. We calculate how many letter edits it takes to turn the link into an official brand like discord.com or steamcommunity.com. "
            "If a scammer sends discoord.com, that's just a single letter difference, which immediately triggers suspicion.\n\n"
            "Second, a Gibberish Score. Real websites have readable, pronounceable names like discord or steam. "
            "Automated scam sites often use random scrambled letters, like x7k9-nitro.ru. By measuring how random the letters are, the model spots bot-generated domains right away.\n\n"
            "And third, practicing against sneaky tricks. Rather than only training on clean data, we intentionally created synthetic lookalike links during training so the model practiced catching tricky variations."
        )
    },
    {
        "slide_num": 6,
        "title": "Clean Data & Preventing Cheating",
        "subtitle": "3,552 Balanced Messages with Duplicate Removal",
        "time": "4:30 - 5:30",
        "action": "[SLIDE: Explain dataset sources and why deduplication was crucial]",
        "bullets": [
            "Safe & Ethical Data: To protect user privacy and follow Discord rules, we used only public research datasets—no private user chats.",
            "Diverse Threat Feeds: 2,000 real scam messages, 21,900 verified malicious domains, and 2,500 normal gaming messages.",
            "Crucial Data Cleaning: Raw scam datasets contained hundreds of exact duplicate copies of the same Nitro message.",
            "Duplicate Removal: We filtered out all duplicate copies so the model wouldn't just memorize the test set.",
            "Clean Dataset: 3,552 unique messages, split into 80% training, 10% validation, and 10% testing."
        ],
        "image": "code_data_loader_dedup.png",
        "image_caption": "Data Pipeline: Threat Feeds & Exact Duplicate Filtering",
        "script_cue": (
            "Looking at Slide 6, let's talk about the data.\n\n"
            "To protect user privacy and comply with Discord's developer rules, I did not scrape private server chats. "
            "Instead, I gathered public research datasets: verified phishing messages, malicious domain threat feeds, and clean everyday gaming conversations.\n\n"
            "The most important data cleaning step was deduplication. In raw scam datasets, you often find hundreds of exact copies of the same Nitro spam message. "
            "If you don't remove them, the model will just memorize those messages and score artificially high on the test set.\n\n"
            "By filtering out all duplicate copies, I created a clean, balanced dataset of 3,552 unique messages, split into training, validation, and testing sets."
        )
    },
    {
        "slide_num": 7,
        "title": "Pipeline Showcase: Benchmarking the Models",
        "subtitle": "Running 'py run_showcase_pipeline.py' & Explaining Model Performance",
        "time": "5:30 - 7:00",
        "action": "[TERMINAL: Run 'py run_showcase_pipeline.py' in VS Code — 17-second run]",
        "bullets": [
            "One-Click Pipeline: Running 'py run_showcase_pipeline.py' executes all data loading, model training, and testing in 17 seconds.",
            "Traditional Baselines: AutoMod regex, Naive Bayes, and SVM all do well on clean text (above 95%), but crash below 50% under letter-swapping attacks.",
            "Why XGBoost Won: Random Forest scored well (0.73), but takes 3.4 ms. XGBoost scored higher (0.81 before hardening) and runs in just 1.2 ms.",
            "The Link Clues Advantage:",
            "  • Looking only at words drops accuracy by 34% when letters are changed.",
            "  • Looking at link clues alone beats word models by 14%, proving that link structure is much harder for scammers to fake!"
        ],
        "image": "workbench_analytics.png",
        "image_caption": "Model Benchmarks: Baselines vs. Tree Ensembles & Ablation",
        "script_cue": (
            "Now let's see the experiments in action. In my terminal, I run py run_showcase_pipeline.py.\n\n"
            "In just seventeen seconds, this master script runs the entire machine learning pipeline from start to finish.\n\n"
            "Let's look at what we learned from comparing the models:\n\n"
            "First, traditional text models like Naive Bayes and basic regex filters do fine on normal text, but they completely fall apart when attackers swap letters—dropping down to under 50% accuracy.\n\n"
            "Second, between tree models, XGBoost outperformed Random Forest and runs in just 1.2 milliseconds on a standard CPU.\n\n"
            "And third, my feature ablation proved that link clues are the real hero: when text is scrambled, our link structure features beat text-only models by 14%!"
        )
    },
    {
        "slide_num": 8,
        "title": "Tough Training & Honest Model Review",
        "subtitle": "Minimax Training, 100% Recall Analysis, and 5-Fold Validation",
        "time": "7:00 - 8:00",
        "action": "[SLIDE: Candidly discuss the 100% recall result and cross-validation]",
        "bullets": [
            "Hardening the Model: Adding lookalike letters into training forced the model to learn evasion-proof rules, boosting accuracy to 97.8%.",
            "Catching 100% of Scams: In our test set, the hardened model caught 178 out of 178 attacks.",
            "Honest Scientific Critique:",
            "  • As a student, seeing 100% means we should ask questions!",
            "  • The model caught all of them because it saw similar letter-swapping tricks during training.",
            "  • In the real world, brand-new zero-day tricks will appear, so real-world recall will naturally be slightly lower.",
            "Consistent Cross-Validation: Tested across 5 separate random folds, the model scored a steady 98.8% recall (±1.1%), proving it didn't just get lucky."
        ],
        "image": "hardened_validation_analysis.png",
        "image_caption": "Audit: XGBoost Gain Shift & 5-Fold Cross-Validation",
        "script_cue": (
            "On Slide 8, let's look at what happened when we hardened the model against attacks.\n\n"
            "By exposing the model to synthetic lookalike tricks during training, its detection rate rebounded to 97.8%, catching all 178 test scams—a 100% recall rate.\n\n"
            "Now Professor, I want to discuss that 100% result with complete scientific honesty:\n"
            "Whenever you see 100% in machine learning, you have to be skeptical. In my experiment, the model caught all 178 scams because the mutation generator I used for testing was similar to the one used in training. The decision tree noticed that any message with a lookalike letter was almost certainly a scam.\n\n"
            "In the open wild, attackers will invent new tricks, so real-world performance will naturally be lower.\n\n"
            "To verify that the model wasn't just overfitting, I ran 5-fold cross-validation with randomized seeds. It achieved a very stable 98.8% recall with only a 1% variance, confirming that our link features are genuinely reliable."
        )
    },
    {
        "slide_num": 9,
        "title": "Live Demo: Testing Real Messages in the Web App",
        "subtitle": "1.2ms Real-Time Inference on Angular 18 & FastAPI",
        "time": "8:00 - 10:00",
        "action": "[BROWSER: http://localhost:4200/ - Test Presets 1, 2, 3 & explain decisions]",
        "bullets": [
            "Full-Stack Web App: Modern Angular 18 dashboard connected to a high-speed FastAPI backend.",
            "Test 1 • Normal Chat: 'Hey man, hopping on Valorant tonight?' → 0.02% risk (Approved Safe) in 1.1 ms.",
            "Test 2 • Classic Nitro Scam: Fake Steam gift link → 99.85% risk (Quarantined) due to scam words and suspicious domain.",
            "Test 3 • Cyrillic Lookalike Attack: 'dіscord.com' with a Russian 'і' → 99.42% risk (Quarantined) in 1.2 ms! Traditional filters miss this completely.",
            "Transparent Explanations (SHAP): Visual bars show exactly which clues caused the model to approve or block the message."
        ],
        "image": "classifier_shap_demo.png",
        "image_caption": "Live Dashboard: 1.2ms Classifier & SHAP Explainability",
        "script_cue": (
            "Now let's switch to my live web application at localhost:4200.\n\n"
            "I built this in Angular 18, talking to a FastAPI backend. At the top, you can see our live latency counter running at around 1.2 milliseconds.\n\n"
            "Let's run three real-world tests:\n\n"
            "Test 1 is a normal gaming message: 'Hey man, hopping on Valorant tonight?' I click Analyze: it takes 1.1 ms, the gauge stays green at 0.02% risk, and it is Approved.\n\n"
            "Test 2 is a classic scam: a fake Nitro gift link. The gauge turns bright red at 99.85% risk and automatically triggers quarantine. The explanation bars show that the urgency words and suspicious domain pushed the score up.\n\n"
            "Test 3 is the tricky one: a link that looks like discord.com, but the letter 'i' is replaced with a Russian lookalike letter. Regular expression filters let this right through. But my model catches it instantly—flagging it at 99.42% risk in just 1.2 milliseconds!"
        )
    },
    {
        "slide_num": 10,
        "title": "Live Chatbox Demo & Lessons Learned",
        "subtitle": "Interactive Pop-Out Chat, Post-Mortem Pivot, and Takeaways",
        "time": "10:00 - 11:30",
        "action": "[BROWSER: Pop-Out Chat Playground -> CAMERA: Post-Mortem & Wrap-Up]",
        "bullets": [
            "Test 4 • Pop-Out Chatbox: Floating button opens a simulated Discord chat where dangerous messages get an instant red quarantine banner.",
            "Architectural Pivot (Post-Mortem):",
            "  • Initial Plan: Check user profiles (account age, avatar, mutual servers).",
            "  • The Problem: Discord bot rules block reading private chats, and user privacy rules ban storing chat history.",
            "  • The Fix: Focusing purely on message text and links made the tool 100% self-contained, privacy-preserving, and fast.",
            "Final Takeaways: Link structure is harder to hide than words • 1.2 ms speed prevents chat delay • Respect platform privacy rules early."
        ],
        "image": "popout_chat_demo.png",
        "image_caption": "Live Dashboard: Simulated Discord Pop-Out Chatbox",
        "script_cue": (
            "To see how this works inside a real server, I click the floating button in the corner to open the Pop-Out Chatbox.\n\n"
            "If I send a normal message, it shows up clean. But if I paste a fake Steam game link, it gets intercepted in 1.2 milliseconds with a bright red quarantine warning, preventing anyone from accidentally clicking it.\n\n"
            "Finally, I want to share my biggest engineering lesson: my Architectural Post-Mortem.\n\n"
            "When I started this project, I originally planned to inspect user profile data, like account age and avatars. But I quickly realized that Discord bots cannot read private direct messages, and Discord's developer terms strictly prohibit saving user chat data.\n\n"
            "Pivoting to inspect only the message itself was the best decision of the project. It requires zero access to private user databases, protects user privacy completely, and makes the model fast and self-contained.\n\n"
            "To wrap up: on 3,552 messages, this detector achieves 97.8% accuracy under attack, runs in 1.2 milliseconds, and is fully deployed across FastAPI and Angular.\n\n"
            "Thank you so much for your time and guidance, Professor! I'm happy to answer any questions."
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
            is_sub = b.strip().startswith("•") or b.strip().startswith("->") or b.strip().startswith("- ") or b.startswith("  ")
            p.level = 1 if is_sub else 0
            clean_b = b.replace("->", "•").replace("- ", "• ").strip()
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
            is_sub = b.strip().startswith("•") or b.strip().startswith("->") or b.strip().startswith("- ") or b.startswith("  ")
            clean_b = b.replace("->", "↳ ").replace("- ", "↳ ").strip()
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
    <title>Discord Phishing Detection - Demo Presentation Slides</title>
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
            <span>🛡 Discord Phishing Detection</span>
            <span style="color: var(--text-muted); font-weight: 400;">| High-Level Demo Slides</span>
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
    print("Building high-level synchronized presentation slides...")
    pptx_path = os.path.join(SCRIPT_DIR, "DEMO_PRESENTATION_SLIDES.pptx")
    html_path = os.path.join(SCRIPT_DIR, "DEMO_PRESENTATION_SLIDES.html")

    build_pptx(pptx_path)
    build_html(html_path)
    print("\nAll presentation slides successfully streamlined & synchronized with script!")
