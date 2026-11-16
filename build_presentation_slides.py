"""
Generates both:
1. DEMO_PRESENTATION_SLIDES.pptx (16:9 Widescreen Microsoft PowerPoint Presentation)
2. DEMO_PRESENTATION_SLIDES.html (Interactive HTML5 Slide Deck with Speaker Notes & Keyboard Controls)

Coordinates directly with DEMO_VIDEO_PRESENTATION_SCRIPT.md (20-minute target).
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = r"c:\Users\Dan\Downloads\ML_DM"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "slides_assets")

# Palette
DARK_BG = RGBColor(24, 26, 31)
CARD_BG = RGBColor(35, 38, 46)
TEXT_WHITE = RGBColor(240, 243, 246)
TEXT_MUTED = RGBColor(160, 168, 180)
ACCENT_CYAN = RGBColor(0, 210, 255)
ACCENT_GREEN = RGBColor(46, 204, 113)
ACCENT_RED = RGBColor(231, 76, 60)
ACCENT_PURPLE = RGBColor(155, 89, 182)

SLIDES_DATA = [
    {
        "slide_num": 1,
        "title": "Dual-Stream Detection of Discord Phishing Campaigns",
        "subtitle": "Machine Learning & Data Mining (Fall 2026) | Final Project Demo\nTeam #18: Edwin Lin, Tin Chak Lam",
        "time": "0:00 - 1:00",
        "action": "[ON CAMERA: Presenter intro with pinned webcam in corner]",
        "bullets": [
            "Project Goal: Fast, machine-learning-based phishing detection built for Discord's unique chat invariants.",
            "Novel Dual-Stream Pipeline: 3,000 TF-IDF word n-grams + 17 engineered structural features.",
            "Target Operational Latency: Sub-2ms CPU inference to prevent server message queuing backlogs.",
            "Demonstration Overview: Architecture -> Code & Data -> Model Benchmarks -> Live Angular 18 Demo."
        ],
        "image": None,
        "script_cue": "Introduce yourself and project partner. State the core goal of the project and set up the 20-minute agenda."
    },
    {
        "slide_num": 2,
        "title": "Threat Context: Why Discord Phishing is Dangerous",
        "subtitle": "Localized Trust Networks & Lateral Account Exploitation",
        "time": "1:00 - 2:30",
        "action": "[SLIDE: Explain the 4 common attack pretexts]",
        "bullets": [
            "Platform Topology: Discord is organized into semi-private servers and direct messages (DMs), not an open public feed.",
            "Trust Exploitation: Compromised accounts blast malicious links to mutual servers and friends lists who inherently trust the sender.",
            "Attack Vector 1: Fake Discord Nitro promotions (supposedly sponsored by Steam or Epic Games).",
            "Attack Vector 2: Fake indie game beta playtest invites (.exe / .scr infostealers like RedLine).",
            "Attack Vector 3: Community tournament voting links requiring third-party OAuth token grants.",
            "Attack Vector 4: Fake cryptocurrency / wallet-drainer distribution portals."
        ],
        "image": None,
        "script_cue": "Explain the psychological trust network in Discord. Explain how session token grabbers steal accounts and automate propagation."
    },
    {
        "slide_num": 3,
        "title": "Failure Modes of Deterministic Filters (AutoMod)",
        "subtitle": "Why Keyword Lists & Regular Expressions Break Down",
        "time": "2:30 - 3:30",
        "action": "[SLIDE: Contrast regex matching vs. modern evasion tricks]",
        "bullets": [
            "Discord AutoMod & Community Bots (MEE6, Dyno) rely almost entirely on static regexes and keyword blocklists.",
            "Evasion Trick 1 - Cyrillic Homoglyphs: Replacing Latin 'o' (U+006F) with Cyrillic 'о' (U+043E). Visually identical, but completely bypasses ASCII regex.",
            "Evasion Trick 2 - Markdown Link Masking: '[https://discord.com/nitro](https://phishing.xyz)' renders a blue trusted URL, but clicks route to a credential harvester.",
            "Evasion Trick 3 - Casual Pretexts: Multi-turn conversational openers ('Hey are you free right now?') contain no URLs, evading initial filters.",
            "Empirical Benchmark Result: AutoMod regex F1 drops by 37.2% (0.8598 -> 0.4876) under basic evasion."
        ],
        "image": None,
        "script_cue": "Highlight the 37.2% F1 collapse in AutoMod regex. Explain the difference between human rendering and regex byte matching."
    },
    {
        "slide_num": 4,
        "title": "System Architecture: Dual-Stream Feature Fusion",
        "subtitle": "Pairing Semantic Context with Structural Domain Invariants",
        "time": "3:30 - 5:30",
        "action": "[SLIDE / ARCHITECTURE DIAGRAM: Walk through the 5-stage pipeline]",
        "bullets": [
            "Stage 1 - Normalization: Strips snowflake IDs (<@!123...>) while preserving raw URLs, Markdown, and Unicode for heuristic checks.",
            "Stage 2 - Stream A (Semantics): 3,000 TF-IDF word n-grams (unigrams & bigrams) capture high-pressure scam language.",
            "Stage 3 - Stream B (Structure): 17 engineered scalar features capture platform invariants attackers cannot easily hide.",
            "Stage 4 - Horizontal Stacking: Concatenates sparse TF-IDF with dense heuristics into X in R^3017.",
            "Stage 5 - XGBoost Ensemble: Evaluates vector in 1.2 ms on CPU. Scores >= 0.80 auto-quarantine; 0.50-0.80 human mod review.",
            "Why XGBoost over DistilBERT? 1.2 ms vs 150-300 ms CPU latency, no subword tokenizer fragmentation, natural tabular tree splits."
        ],
        "image": None,
        "script_cue": "Explain the 5 stages. Justify XGBoost over BERT based on latency and tokenization stability. Explain the 0.80 quarantine threshold."
    },
    {
        "slide_num": 5,
        "title": "Mathematical Formulations & Algorithmic Optimizations",
        "subtitle": "Levenshtein Distance, Shannon Entropy, and Minimax Hardening",
        "time": "5:30 - 6:30",
        "action": "[SLIDE / FORMULAS: Highlight mathematical models]",
        "bullets": [
            "1. Minimum Levenshtein Distance (d_min): Dynamic programming edit distance to canonical platforms (discord.com, steamcommunity.com).",
            "   -> Optimization: Early-exit check skips O(NM) matrix if absolute string length difference > 4.",
            "2. Shannon Domain Entropy (H(d)): Quantifies character distribution randomness to catch automated DGAs.",
            "   -> H(d) = - sum p(c) * log2(p(c)). Clean platforms score 2.0-2.8; machine-generated scam strings score > 3.5.",
            "3. Minimax Adversarial Formulation: Trains trees against worst-case synthetic perturbations (homoglyphs + Markdown cloaking):",
            "   -> min_theta E [ max_{delta in Delta} L(f_theta(x + delta), y) ]."
        ],
        "image": None,
        "script_cue": "Walk through the math: d_min early-exit, Shannon entropy formula, and minimax objective. Keep it practical and code-oriented."
    },
    {
        "slide_num": 6,
        "title": "Data Engineering & Threat Feed Integration",
        "subtitle": "3,552 Balanced Messages with MD5 Hash Deduplication",
        "time": "6:30 - 8:30",
        "action": "[SWITCH TO VS CODE: Open data_loader.py & feature_extractor.py]",
        "bullets": [
            "Provenance: 2,000 Hugging Face phishing messages + 21,908 Nikolaischunk threat feed domains + 1,500 modern playbooks + 2,500 clean chat logs.",
            "Platform Privacy Compliance: Built strictly from public research data to respect Discord Developer Policy Section 21.",
            "Critical Deduplication Step: Raw Hugging Face data had hundreds of duplicate Nitro spam copies. Filtered via MD5 hashes to prevent train-test leakage.",
            "Splits: Stratified 80% train (2,841), 10% validation (355), 10% clean test (356) + separate 356-sample adversarial evaluation set.",
            "Feature Extractor Implementation: Globally precompiled regexes to avoid 15x per-message compilation bottleneck."
        ],
        "image": None,
        "script_cue": "Switch to VS Code. Show data_loader.py deduplication logic and feature_extractor.py globally compiled regexes."
    },
    {
        "slide_num": 7,
        "title": "Experimental Benchmarks & 3-Way Feature Ablation",
        "subtitle": "Tables I & II: Validating the Invariant Signal of Stream B",
        "time": "8:30 - 10:30",
        "action": "[SWITCH TO TERMINAL: Run train_baselines.py & ablation_study.py]",
        "bullets": [
            "Table I (Baselines): AutoMod regex collapses to 0.4876 F1 under attack. Naive Bayes, Logistic Regression, SVM drop to 0.44-0.49 recall.",
            "Unhardened XGBoost Baseline: Maintains 0.8078 F1 under attack because structural features remain invariant.",
            "Table II (Ablation Analysis):",
            "  - Stream A Alone (3,000 TF-IDF): 0.9589 clean F1 -> 0.4944 recall (0.6331 F1) under attack (-34.0% drop).",
            "  - Stream B Alone (17 Heuristics): 0.9636 clean F1 -> 0.6573 recall (0.7748 F1) under attack (+14.1% over text alone).",
            "  - Dual-Stream Fused: 0.9777 clean F1 and 0.8078 adversarial F1 before hardening."
        ],
        "image": "workbench_analytics.png",
        "script_cue": "Switch to Terminal. Run the scripts, show Table I and Table II output. Explain why Stream B outperforms Stream A under attack."
    },
    {
        "slide_num": 8,
        "title": "Adversarial Hardening & Honest Review of 100% Recall",
        "subtitle": "Table III: Minimax Training, Generator Overlap, and 5-Fold CV Variance",
        "time": "10:30 - 12:00",
        "action": "[SLIDE / TERMINAL: Discuss Table III results & threats to validity]",
        "bullets": [
            "Minimax Hardening: Augmenting 25% of training scam samples with homoglyphs and Markdown disguises recovers adversarial F1 to 0.9780.",
            "The 100% Recall Artifact: The model caught 178 of 178 test scams (1.0000 recall).",
            "  -> Honest Critique: Both training augmentation and test evaluation used 'build_adversarial_variant'. In this closed distribution, homoglyph_count >= 1 became a near-perfect split rule (jumping from #14 to #5 in tree importance).",
            "Cross-Validation Variance: 5-fold CV with randomized mutation seeds yields 0.9888 +/- 0.0112 recall and 0.9780 +/- 0.0094 F1.",
            "Real-World Zero-Day Limitations: Unseen Unicode scripts, RTL override characters, and image QR codes will inevitably lower open-world recall."
        ],
        "image": None,
        "script_cue": "Discuss the 100% recall result with scientific honesty. Explain the closed-generator overlap and present the 5-fold CV variance."
    },
    {
        "slide_num": 9,
        "title": "Live Demonstration: Classifier & SHAP Explainability",
        "subtitle": "Real-Time 1.2ms Inference on Angular 18 & FastAPI",
        "time": "12:00 - 15:30",
        "action": "[SWITCH TO BROWSER: http://localhost:4200/ - Test Presets Live]",
        "bullets": [
            "Test 1 - Benign Chat: 'Hey man, hopping on Valorant tonight?' -> 0.02% scam probability (Green Approved Badge).",
            "Test 2 - Classic Nitro: '@everyone Steam free nitro https://discord-nitro-gift.ru/claim' -> 99.85% (AUTO-QUARANTINE).",
            "Test 3 - Cyrillic Homoglyphs: 'https://dіscord.com/gifts' (with Cyrillic 'і' U+0456) -> AutoMod misses, our model flags at 99.42%!",
            "Test 4 - Markdown Masking: '[https://discord.com/nitro](https://grabify-stealer.xyz)' -> Flags destination domain at 99.78%.",
            "Explainability: Local SHAP waterfall charts clearly explain why each heuristic contributed to the final score."
        ],
        "image": "classifier_shap_demo.png",
        "script_cue": "Switch to Chrome. Click the preset buttons, show the 1.2ms latency badge, explain the SHAP attribution bars."
    },
    {
        "slide_num": 10,
        "title": "Live Demonstration: Interactive Pop-Out Chatbox",
        "subtitle": "Simulated Discord Chat & Post-Mortem Engineering Takeaways",
        "time": "15:30 - 20:00",
        "action": "[BROWSER: Open floating Chat Playground dialog. Then CAMERA for conclusion]",
        "bullets": [
            "Pop-Out Chat Playground: Floating action button opens inline chat dialog simulating live server conversation.",
            "Instant Interception: Simulated multi-turn dialogue auto-quarantines payload with red warning banner in 1.2 ms.",
            "Architectural Post-Mortem: Why we abandoned user metadata (Discord bot DM sandboxing returning 403 Forbidden & Developer Policy Section 21 privacy bans).",
            "Why the Pivot Succeeded: Pure payload string invariants made the detector completely self-contained, fast, and privacy-preserving.",
            "Final Scorecard: 0.9777 clean F1, 0.9780 hardened F1, 1.2 ms latency, production-ready full-stack architecture."
        ],
        "image": "popout_chat_demo.png",
        "script_cue": "Click the floating Chat Playground button. Send benign then malicious messages. Transition to post-mortem and wrap up video."
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
        badge_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.3), Inches(2.3), Inches(0.5))
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
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.8), Inches(1.0))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = data["title"]
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Subtitle
        p_sub = tf_t.add_paragraph()
        p_sub.text = data["subtitle"]
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = TEXT_MUTED

        # Action Cue Banner
        action_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.45))
        action_box.fill.solid()
        action_box.fill.fore_color.rgb = CARD_BG
        action_box.line.color.rgb = ACCENT_CYAN
        tf_a = action_box.text_frame
        p_a = tf_a.paragraphs[0]
        p_a.alignment = PP_ALIGN.LEFT
        r_a = p_a.add_run()
        r_a.text = f"  PRESENTER ACTION: {data['action']}"
        r_a.font.size = Pt(11)
        r_a.font.bold = True
        r_a.font.color.rgb = ACCENT_CYAN

        # Layout: If image exists, split columns; otherwise full-width bullets
        has_image = data["image"] and os.path.exists(os.path.join(ASSETS_DIR, data["image"]))
        content_w = Inches(6.0) if has_image else Inches(11.733)

        # Bullets Container
        tb_body = slide.shapes.add_textbox(Inches(0.8), Inches(2.1), content_w, Inches(4.8))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True

        for i, b in enumerate(data["bullets"]):
            p = tf_body.add_paragraph() if i > 0 else tf_body.paragraphs[0]
            p.space_after = Pt(8)
            p.level = 1 if b.strip().startswith("->") or b.strip().startswith("- ") else 0
            clean_b = b.replace("->", "•").replace("- ", "• ")
            r = p.add_run()
            r.text = clean_b
            r.font.size = Pt(12.5 if p.level == 0 else 11.5)
            r.font.color.rgb = TEXT_WHITE if p.level == 0 else TEXT_MUTED

        # Add Image if present
        if has_image:
            img_path = os.path.join(ASSETS_DIR, data["image"])
            img_box = slide.shapes.add_picture(img_path, Inches(7.1), Inches(2.2), width=Inches(5.4))

        # Presenter Notes in PPTX
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = f"TIMESTAMP: {data['time']}\nACTION: {data['action']}\n\nTALKING POINTS / SCRIPT CUE:\n{data['script_cue']}"

    prs.save(output_path)
    print(f"PowerPoint slide deck saved successfully to: {output_path}")


# ==============================================================================
# 2. BUILD INTERACTIVE HTML5 SLIDE DECK
# ==============================================================================

def build_html(output_path):
    slides_html_blocks = []

    for d in SLIDES_DATA:
        bullets_li = ""
        for b in d["bullets"]:
            is_sub = b.strip().startswith("->") or b.strip().startswith("- ")
            clean_b = b.replace("->", "↳ ").replace("- ", "↳ ")
            cls = "sub-bullet" if is_sub else "main-bullet"
            bullets_li += f'<li class="{cls}">{clean_b}</li>\n'

        image_html = ""
        if d["image"]:
            img_rel = f"slides_assets/{d['image']}"
            image_html = f'''
            <div class="slide-image-col">
                <div class="image-wrapper">
                    <img src="{img_rel}" alt="Demonstration Screenshot" />
                    <div class="image-caption">Live Interface Screenshot</div>
                </div>
            </div>
            '''

        grid_class = "two-col" if d["image"] else "single-col"

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

            <div class="slide-content {grid_class}">
                <div class="slide-text-col">
                    <ul class="bullet-list">
                        {bullets_li}
                    </ul>
                </div>
                {image_html}
            </div>

            <div class="speaker-notes-box">
                <div class="notes-header">
                    <strong>🎙 Presenter Speaking Cue ({d['time']})</strong>
                    <button class="toggle-notes-btn" onclick="toggleNotes(this)">Show Full Dialogue</button>
                </div>
                <div class="notes-body">
                    <p><em>Focus:</em> {d['script_cue']}</p>
                    <p class="hint">Consult <code>DEMO_VIDEO_PRESENTATION_SCRIPT.md</code> for full word-for-word spoken dialogue.</p>
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
    <title>Discord Scam Detection - 20-Min Demo Presentation Slides</title>
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
            max-width: 1200px;
            min-height: 700px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }}
        .slide {{
            display: none;
            padding: 36px 44px;
            animation: fadeIn 0.3s ease;
        }}
        .slide.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        /* Slide Components */
        .slide-header {{ margin-bottom: 20px; }}
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
        h2 {{ font-size: 26px; font-weight: 800; color: var(--text-main); margin-top: 10px; }}
        .subtitle {{ font-size: 14px; color: var(--text-muted); margin-top: 4px; }}

        .action-banner {{
            background: rgba(0, 210, 255, 0.08);
            border-left: 4px solid var(--accent-cyan);
            padding: 10px 16px;
            border-radius: 4px;
            margin-bottom: 24px;
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
        .action-text {{ font-size: 13px; font-weight: 600; color: #d0f0ff; }}

        /* Grid */
        .slide-content.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: start; }}
        .slide-content.single-col {{ display: block; }}

        .bullet-list {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
        .bullet-list li.main-bullet {{
            position: relative;
            padding-left: 24px;
            font-size: 15px;
            line-height: 1.5;
            color: var(--text-main);
        }}
        .bullet-list li.main-bullet::before {{
            content: "•";
            position: absolute;
            left: 6px;
            color: var(--accent-cyan);
            font-size: 20px;
            top: -2px;
        }}
        .bullet-list li.sub-bullet {{
            padding-left: 44px;
            font-size: 14px;
            line-height: 1.5;
            color: var(--text-muted);
        }}

        /* Image Display */
        .image-wrapper {{
            background: #121418;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px;
            text-align: center;
        }}
        .image-wrapper img {{
            width: 100%;
            height: auto;
            max-height: 340px;
            object-fit: contain;
            border-radius: 4px;
        }}
        .image-caption {{ font-size: 11px; color: var(--text-muted); margin-top: 6px; font-style: italic; }}

        /* Speaker Notes Drawer */
        .speaker-notes-box {{
            margin-top: 28px;
            background: #15181e;
            border: 1px dashed #3a4252;
            border-radius: 8px;
            padding: 12px 18px;
        }}
        .notes-header {{ display: flex; justify-content: space-between; align-items: center; }}
        .notes-header strong {{ font-size: 13px; color: #ffd166; }}
        .toggle-notes-btn {{
            background: transparent;
            border: none;
            color: var(--accent-cyan);
            font-size: 12px;
            cursor: pointer;
            text-decoration: underline;
        }}
        .notes-body {{ margin-top: 8px; font-size: 13px; color: var(--text-muted); line-height: 1.5; display: none; }}
        .notes-body.open {{ display: block; }}
        .notes-body p {{ margin-bottom: 6px; }}
        .notes-body code {{ background: #222630; padding: 2px 6px; border-radius: 4px; color: #00d2ff; }}

        /* Keyboard Legend */
        .footer-legend {{
            background: #14171d;
            border-top: 1px solid var(--border-color);
            padding: 10px 24px;
            display: flex;
            justify-content: center;
            gap: 24px;
            font-size: 12px;
            color: var(--text-muted);
        }}
        .kbd-key {{
            background: #252a36;
            color: var(--text-main);
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #3d4558;
            font-weight: 600;
        }}
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

    <footer class="footer-legend">
        <span><span class="kbd-key">←</span> or <span class="kbd-key">→</span> Navigate Slides</span>
        <span><span class="kbd-key">Space</span> Next Slide</span>
        <span><span class="kbd-key">N</span> Toggle Speaker Notes</span>
        <span><span class="kbd-key">F</span> Fullscreen Mode</span>
    </footer>

    <script>
        let currentSlide = 1;
        const totalSlides = 10;

        function showSlide(n) {{
            document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
            const target = document.querySelector(`.slide[data-slide="${{n}}"]`);
            if (target) {{
                target.classList.add('active');
                document.getElementById('slideIndicator').innerText = `${{n}} / ${{totalSlides}}`;
                currentSlide = n;
            }}
        }}

        function nextSlide() {{
            if (currentSlide < totalSlides) showSlide(currentSlide + 1);
        }}

        function prevSlide() {{
            if (currentSlide > 1) showSlide(currentSlide - 1);
        }}

        function toggleNotes(btn) {{
            const body = btn.closest('.speaker-notes-box').querySelector('.notes-body');
            body.classList.toggle('open');
            btn.innerText = body.classList.contains('open') ? 'Hide Dialogue' : 'Show Full Dialogue';
        }}

        function toggleAllNotes() {{
            const bodies = document.querySelectorAll('.notes-body');
            const anyOpen = Array.from(bodies).some(b => b.classList.contains('open'));
            bodies.forEach(b => {{
                if (anyOpen) b.classList.remove('open');
                else b.classList.add('open');
            }});
        }}

        function toggleFullScreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
                e.preventDefault();
                nextSlide();
            }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
                e.preventDefault();
                prevSlide();
            }} else if (e.key.toLowerCase() === 'n') {{
                toggleAllNotes();
            }} else if (e.key.toLowerCase() === 'f') {{
                toggleFullScreen();
            }}
        }});

        // Initialize slide 1
        showSlide(1);
    </script>
</body>
</html>
'''
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Interactive HTML slide deck saved successfully to: {output_path}")


if __name__ == "__main__":
    pptx_path = os.path.join(OUTPUT_DIR, "DEMO_PRESENTATION_SLIDES.pptx")
    html_path = os.path.join(OUTPUT_DIR, "DEMO_PRESENTATION_SLIDES.html")
    build_pptx(pptx_path)
    build_html(html_path)
    print("\nAll presentation slides successfully built!")
