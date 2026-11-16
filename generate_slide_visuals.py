"""
Generate rich, high-resolution visual cards for all demo presentation slides:
- pipeline_overview_card.png (Slide 1: Dual-Stream Pipeline Flowchart)
- code_adversarial_perturbation.png (Slide 2: Homoglyph & Evasion Vectors)
- code_automod_regex_bypass.png (Slide 3: AutoMod Regex Failure & Evasion Comparison)
- code_feature_extractor.png (Slide 4: Heuristic Feature Extraction Engine)
- math_formulations_card.png (Slide 5: Mathematical Models & Optimizations)
- code_data_loader_dedup.png (Slide 6: MD5 Deduplication & Threat Feed Integration)
- hardened_validation_analysis.png (Slide 8: Feature Importance Shift & 5-Fold CV Variance)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(r"c:\Users\Dan\Downloads\ML_DM", "slides_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color Palette
BG_COLOR = '#181A1F'
CARD_COLOR = '#23262E'
BORDER_COLOR = '#323742'
HEADER_COLOR = '#1E2127'
CYAN = '#00D2FF'
GREEN = '#2ECC71'
RED = '#E74C3C'
PURPLE = '#9B59B6'
YELLOW = '#F1C40F'
ORANGE = '#E67E22'
TEXT_LIGHT = '#F0F3F6'
TEXT_MUTED = '#9AA2B0'
TEXT_DIM = '#5C6370'

def draw_window_chrome(ax, title, width=1.0, height=1.0):
    # Background card
    card = patches.FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.96,
        boxstyle="round,pad=0.01,rounding_size=0.03",
        facecolor=CARD_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5
    )
    ax.add_patch(card)
    
    # Title bar
    title_bar = patches.FancyBboxPatch(
        (0.02, 0.90), 0.96, 0.08,
        boxstyle="round,pad=0.0,rounding_size=0.02",
        facecolor=HEADER_COLOR, edgecolor=BORDER_COLOR, linewidth=1.0
    )
    ax.add_patch(title_bar)
    
    # Window dots
    ax.add_patch(patches.Circle((0.06, 0.94), 0.012, facecolor='#FF5F56', edgecolor='none'))
    ax.add_patch(patches.Circle((0.09, 0.94), 0.012, facecolor='#FFBD2E', edgecolor='none'))
    ax.add_patch(patches.Circle((0.12, 0.94), 0.012, facecolor='#27C93F', edgecolor='none'))
    
    # File tab title
    ax.text(0.16, 0.935, title, color=TEXT_MUTED, fontsize=11, fontfamily='monospace', va='center')


# ==============================================================================
# 1. SLIDE 1: Pipeline Overview Card
# ==============================================================================
def make_pipeline_overview():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "architecture_pipeline_overview.py [Dual-Stream Architecture]")
    
    # Header Banner inside card
    ax.text(0.5, 0.84, "DUAL-STREAM INFERENCE PIPELINE (1.2 ms CPU)", color=CYAN, fontsize=13, fontweight='bold', ha='center', fontfamily='sans-serif')
    
    # Stage 1: Input
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.68), 0.88, 0.11, boxstyle="round,pad=0.01", facecolor='#1E2127', edgecolor='#4B5263'))
    ax.text(0.09, 0.75, "STAGE 1: INPUT MESSAGE NORMALIZATION", color=TEXT_LIGHT, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.705, 'Raw Discord Payload  ->  Strip Snowflake IDs (<@!123...>)  ->  Preserve URLs & Markdown', color=TEXT_MUTED, fontsize=8.5, fontfamily='monospace')
    
    # Stage 2: Dual Stream Split
    # Stream A
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.44), 0.42, 0.20, boxstyle="round,pad=0.01", facecolor='#1c2333', edgecolor=CYAN))
    ax.text(0.09, 0.59, "STREAM A: SEMANTIC (TF-IDF)", color=CYAN, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.54, "* 3,000 Word N-grams (1, 2)", color=TEXT_LIGHT, fontsize=8.5)
    ax.text(0.09, 0.49, "* High-pressure scam vocabulary", color=TEXT_MUTED, fontsize=8)
    ax.text(0.09, 0.45, "* Sublinear TF scaling (1 + log(tf))", color=TEXT_MUTED, fontsize=8)

    # Stream B
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.44), 0.42, 0.20, boxstyle="round,pad=0.01", facecolor='#1c2925', edgecolor=GREEN))
    ax.text(0.55, 0.59, "STREAM B: STRUCTURAL (17 INVARIANTS)", color=GREEN, fontsize=10, fontweight='bold')
    ax.text(0.55, 0.54, "* Min Levenshtein Distance (Discord/Steam)", color=TEXT_LIGHT, fontsize=8.5)
    ax.text(0.55, 0.49, "* Shannon Domain Entropy H(d)", color=TEXT_MUTED, fontsize=8)
    ax.text(0.55, 0.45, "* Homoglyph & Spoiler Mask Counts", color=TEXT_MUTED, fontsize=8)
    
    # Stage 3: Fusion & XGBoost
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.23), 0.88, 0.16, boxstyle="round,pad=0.01", facecolor='#2a2233', edgecolor=PURPLE))
    ax.text(0.09, 0.33, "STAGE 3: FEATURE FUSION & XGBOOST ENSEMBLE (R^3017)", color='#C678DD', fontsize=10, fontweight='bold')
    ax.text(0.09, 0.28, "Horizontal Stacking: [ Sparse TF-IDF (3,000)  ||  Dense Heuristics (17) ]", color=TEXT_LIGHT, fontsize=8.5, fontfamily='monospace')
    ax.text(0.09, 0.245, "Ensemble: 100 Gradient-Boosted Trees (Depth=6, lr=0.1, sub=0.8) -> 1.2 ms Inference", color=TEXT_MUTED, fontsize=8)
    
    # Stage 4: Decision Policy Badges
    b1 = patches.FancyBboxPatch((0.06, 0.06), 0.26, 0.12, boxstyle="round,pad=0.01", facecolor='#192b1e', edgecolor=GREEN)
    ax.add_patch(b1)
    ax.text(0.19, 0.13, "P < 0.50", color=GREEN, fontsize=10, fontweight='bold', ha='center')
    ax.text(0.19, 0.08, "APPROVED (BENIGN)", color=TEXT_LIGHT, fontsize=8, ha='center')
    
    b2 = patches.FancyBboxPatch((0.37, 0.06), 0.26, 0.12, boxstyle="round,pad=0.01", facecolor='#2b2719', edgecolor=YELLOW)
    ax.add_patch(b2)
    ax.text(0.50, 0.13, "0.50 <= P < 0.80", color=YELLOW, fontsize=10, fontweight='bold', ha='center')
    ax.text(0.50, 0.08, "MOD REVIEW FLAGGED", color=TEXT_LIGHT, fontsize=8, ha='center')
    
    b3 = patches.FancyBboxPatch((0.68, 0.06), 0.26, 0.12, boxstyle="round,pad=0.01", facecolor='#2b1919', edgecolor=RED)
    ax.add_patch(b3)
    ax.text(0.81, 0.13, "P >= 0.80", color=RED, fontsize=10, fontweight='bold', ha='center')
    ax.text(0.81, 0.08, "AUTO-QUARANTINE", color=TEXT_LIGHT, fontsize=8, ha='center')
    
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "pipeline_overview_card.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


# ==============================================================================
# 2. SLIDE 2: Adversarial Evasion Vectors (Code Snippet)
# ==============================================================================
def make_code_adversarial_perturbation():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "src/data_loader.py - build_adversarial_variant()")
    
    code_lines = [
        (TEXT_DIM, " 30 | ", PURPLE, "# Unicode Cyrillic homoglyphs visually identical to Latin letters", None, ""),
        (TEXT_DIM, " 31 | ", CYAN, "HOMOGLYPH_MAP", TEXT_LIGHT, " = {", None, ""),
        (TEXT_DIM, " 32 | ", GREEN, "    'a': '\\u0430',  # Cyrillic small 'а'", None, "", None, ""),
        (TEXT_DIM, " 33 | ", GREEN, "    'e': '\\u0435',  # Cyrillic small 'е'", None, "", None, ""),
        (TEXT_DIM, " 34 | ", GREEN, "    'i': '\\u0456',  # Cyrillic small 'і'", None, "", None, ""),
        (TEXT_DIM, " 35 | ", GREEN, "    'o': '\\u043e',  # Cyrillic small 'о'", None, "", None, ""),
        (TEXT_DIM, " 36 | ", GREEN, "    's': '\\u0455',  # Cyrillic small 'ѕ'", None, "", None, ""),
        (TEXT_DIM, " 37 | ", TEXT_LIGHT, "}", None, "", None, "", None, ""),
        (TEXT_DIM, " 38 | ", None, "", None, "", None, ""),
        (TEXT_DIM, "181 | ", PURPLE, "def ", YELLOW, "build_adversarial_variant", TEXT_LIGHT, "(text):"),
        (TEXT_DIM, "182 | ", TEXT_MUTED, '    """Applies realistic evasion perturbations to payload"""', None, ""),
        (TEXT_DIM, "192 | ", PURPLE, "    # Evasion 1: Markdown link spoofing [fake_url](real_malicious_target)", None, ""),
        (TEXT_DIM, "193 | ", CYAN, "    if ", TEXT_LIGHT, "urls ", CYAN, "and ", TEXT_LIGHT, "random.random() > 0.4:"),
        (TEXT_DIM, "195 | ", TEXT_LIGHT, '        masked = ', GREEN, 'f"[{fake_label}]({target_url})"', None, ""),
        (TEXT_DIM, "196 | ", TEXT_LIGHT, '        result = result.replace(target_url, masked)', None, ""),
        (TEXT_DIM, "198 | ", PURPLE, "    # Evasion 2: Character-level homoglyph substitution", None, ""),
        (TEXT_DIM, "201 | ", CYAN, "    for ", TEXT_LIGHT, "i, ch ", CYAN, "in ", YELLOW, "enumerate", TEXT_LIGHT, "(chars):"),
        (TEXT_DIM, "202 | ", CYAN, "        if ", TEXT_LIGHT, "ch.lower() ", CYAN, "in ", CYAN, "HOMOGLYPH_MAP", None, ":"),
        (TEXT_DIM, "203 | ", TEXT_LIGHT, "            chars[i] = HOMOGLYPH_MAP[ch.lower()]", None, ""),
        (TEXT_DIM, "212 | ", PURPLE, "    return ", TEXT_LIGHT, '"".join(chars)', None, "")
    ]
    
    y = 0.85
    for row in code_lines:
        x = 0.05
        for i in range(0, len(row), 2):
            color = row[i]
            text = row[i+1]
            if text:
                ax.text(x, y, text, color=color, fontsize=8.5, fontfamily='monospace', va='center')
                x += len(text) * 0.0095
        y -= 0.038
        
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "code_adversarial_perturbation.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


# ==============================================================================
# 3. SLIDE 3: AutoMod Regex Failure (Comparison Card)
# ==============================================================================
def make_code_automod_regex_bypass():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "automod_regex_benchmark.py [Failure Mode Simulation]")
    
    # AutoMod Rule box
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.72), 0.88, 0.15, boxstyle="round,pad=0.01", facecolor='#1c2333', edgecolor=CYAN))
    ax.text(0.09, 0.82, "TYPICAL DISCORD AUTOMOD REGEX RULE:", color=CYAN, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.76, r"PATTERN = re.compile(r'(discord\.gift|nitro|steamcommunity)', re.IGNORECASE)", color=TEXT_LIGHT, fontsize=8.5, fontfamily='monospace')
    
    # Case 1: Clean Attack (Caught)
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.44), 0.88, 0.24, boxstyle="round,pad=0.01", facecolor='#192b1e', edgecolor=GREEN))
    ax.text(0.09, 0.62, "CASE 1: UNPERTURBED RAW ATTACK (CAUGHT)", color=GREEN, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.56, 'Payload:  "Free 3 Months of Discord Nitro: https://discord.gift/free928"', color=TEXT_LIGHT, fontsize=8.5, fontfamily='monospace')
    ax.text(0.09, 0.51, 'Regex Match:  True -> MATCH FOUND ("discord.gift")', color=GREEN, fontsize=8.5, fontfamily='monospace')
    ax.text(0.09, 0.46, 'AutoMod Outcome:  FLAGGED & DELETED  [PASS]', color=TEXT_MUTED, fontsize=8.5)

    # Case 2: Evasive Attack (Bypassed)
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.16), 0.88, 0.24, boxstyle="round,pad=0.01", facecolor='#2b1919', edgecolor=RED))
    ax.text(0.09, 0.34, "CASE 2: CYRILLIC HOMOGLYPH EVASION (BYPASSED!)", color=RED, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.28, 'Payload:  "Free 3 Months: https://d\\u0456scord.gift/free928" (Cyrillic \\u0456)', color=TEXT_LIGHT, fontsize=8.5, fontfamily='monospace')
    ax.text(0.09, 0.23, 'Regex Match:  False -> re.search() returns None (ASCII mismatch)', color=RED, fontsize=8.5, fontfamily='monospace')
    ax.text(0.09, 0.18, 'AutoMod Outcome:  PERMITTED INTO SERVER  [CRITICAL BYPASS]', color=TEXT_MUTED, fontsize=8.5)
    
    # Bottom Callout Badge
    ax.add_patch(patches.FancyBboxPatch((0.25, 0.04), 0.50, 0.08, boxstyle="round,pad=0.01", facecolor='#3d1717', edgecolor=RED))
    ax.text(0.50, 0.08, "EMPIRICAL COLLAPSE: AutoMod F1 Drops -37.2% (0.8598 -> 0.4876)", color='#FF6B6B', fontsize=9, fontweight='bold', ha='center')
    
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "code_automod_regex_bypass.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


# ==============================================================================
# 4. SLIDE 4: Feature Extractor Code Snippet
# ==============================================================================
def make_code_feature_extractor():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "src/feature_extractor.py - extract_heuristics_single()")
    
    code_lines = [
        (TEXT_DIM, "115 | ", PURPLE, "def ", YELLOW, "extract_heuristics_single", TEXT_LIGHT, "(self, text):"),
        (TEXT_DIM, "121 | ", TEXT_LIGHT, "    urls = re.findall(", GREEN, r"r'https?://[^\s<>]+'", TEXT_LIGHT, ", text)"),
        (TEXT_DIM, "127 | ", TEXT_LIGHT, "    min_dist_discord = 99;  min_dist_steam = 99"),
        (TEXT_DIM, "134 | ", CYAN, "    for ", TEXT_LIGHT, "u ", CYAN, "in ", TEXT_LIGHT, "urls:"),
        (TEXT_DIM, "135 | ", TEXT_LIGHT, "        ext = tldextract.extract(u)"),
        (TEXT_DIM, "136 | ", TEXT_LIGHT, "        domain = f'{ext.domain}.{ext.suffix}'.lower()"),
        (TEXT_DIM, "142 | ", PURPLE, "        # Levenshtein distance with early length exit", None, ""),
        (TEXT_DIM, "143 | ", TEXT_LIGHT, "        d_disc = levenshtein_distance(ext.domain, ", GREEN, "'discord'", TEXT_LIGHT, ")"),
        (TEXT_DIM, "145 | ", TEXT_LIGHT, "        min_dist_discord = ", YELLOW, "min", TEXT_LIGHT, "(min_dist_discord, d_disc)"),
        (TEXT_DIM, "148 | ", PURPLE, "        # Shannon entropy to catch automated DGAs", None, ""),
        (TEXT_DIM, "149 | ", TEXT_LIGHT, "        ent = shannon_entropy(ext.domain)"),
        (TEXT_DIM, "150 | ", TEXT_LIGHT, "        max_entropy = ", YELLOW, "max", TEXT_LIGHT, "(max_entropy, ent)"),
        (TEXT_DIM, "160 | ", PURPLE, "    # Structural features attacker cannot hide", None, ""),
        (TEXT_DIM, "161 | ", TEXT_LIGHT, "    homoglyphs = ", YELLOW, "sum", TEXT_LIGHT, "(1 ", CYAN, "for ", TEXT_LIGHT, "c ", CYAN, "in ", TEXT_LIGHT, "text ", CYAN, "if ", TEXT_LIGHT, "c ", CYAN, "in ", CYAN, "HOMOGLYPH_SET", TEXT_LIGHT, ")"),
        (TEXT_DIM, "163 | ", TEXT_LIGHT, "    has_md_mask = 1 ", CYAN, "if ", TEXT_LIGHT, "re.search(", GREEN, r"r'\[.*?\]\(.*?\)'", TEXT_LIGHT, ", text) ", CYAN, "else ", TEXT_LIGHT, "0"),
        (TEXT_DIM, "166 | ", TEXT_LIGHT, "    urgency_hits = ", YELLOW, "sum", TEXT_LIGHT, "(1 ", CYAN, "for ", TEXT_LIGHT, "w ", CYAN, "in ", CYAN, "URGENCY_WORDS ", CYAN, "if ", TEXT_LIGHT, "w ", CYAN, "in ", TEXT_LIGHT, "text.lower())"),
        (TEXT_DIM, "175 | ", PURPLE, "    return ", CYAN, "np.array", TEXT_LIGHT, "([has_url, min_dist_discord, max_entropy, homoglyphs, ...])")
    ]
    
    y = 0.85
    for row in code_lines:
        x = 0.05
        for i in range(0, len(row), 2):
            color = row[i]
            text = row[i+1]
            if text:
                ax.text(x, y, text, color=color, fontsize=8.5, fontfamily='monospace', va='center')
                x += len(text) * 0.0095
        y -= 0.042
        
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "code_feature_extractor.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


# ==============================================================================
# 5. SLIDE 5: Mathematical Formulations Card
# ==============================================================================
def make_math_formulations_card():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "formal_mathematical_specifications.tex")
    
    # 1. Levenshtein formulation
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.62), 0.88, 0.24, boxstyle="round,pad=0.01", facecolor='#1c2333', edgecolor=CYAN))
    ax.text(0.09, 0.81, "1. MINIMUM LEVENSHTEIN DISTANCE WITH EARLY EXIT", color=CYAN, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.74, r"$d_{\min}(s, \mathcal{C}) = \min_{c \in \mathcal{C}} \mathrm{Levenshtein}(s, c)$", color=TEXT_LIGHT, fontsize=11)
    ax.text(0.09, 0.68, r"Optimization: Skip $O(|s| \cdot |c|)$ DP matrix if $||s| - |c|| > \tau_{exit}$ (where $\tau = 4$)", color=YELLOW, fontsize=8.5)
    ax.text(0.09, 0.64, "Flags typo-squatting targets ('discoord.com', 'steamcommunlty.com') in microseconds.", color=TEXT_MUTED, fontsize=8)

    # 2. Shannon Entropy
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.35), 0.88, 0.24, boxstyle="round,pad=0.01", facecolor='#1c2925', edgecolor=GREEN))
    ax.text(0.09, 0.54, "2. SHANNON DOMAIN ENTROPY (MEASURING RANDOMNESS)", color=GREEN, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.47, r"$H(d) = -\sum_{i=1}^{k} p(c_i) \log_2 p(c_i)$", color=TEXT_LIGHT, fontsize=11)
    ax.text(0.09, 0.41, "Legitimate domains (e.g. 'discord') yield H(d) in [2.0, 2.8].", color=TEXT_MUTED, fontsize=8.5)
    ax.text(0.09, 0.37, "Algorithmic DGA domains ('x7k9-free-nitro.ru') score H(d) > 3.5, triggering heuristic flags.", color=YELLOW, fontsize=8)

    # 3. Minimax Adversarial Formulation
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.08), 0.88, 0.24, boxstyle="round,pad=0.01", facecolor='#2a2233', edgecolor=PURPLE))
    ax.text(0.09, 0.27, "3. MINIMAX ADVERSARIAL RISK OBJECTIVE", color='#C678DD', fontsize=10, fontweight='bold')
    ax.text(0.09, 0.20, r"$\min_{\theta} \mathbb{E}_{(x, y) \sim \mathcal{D}} \left[ \max_{\delta \in \Delta} \mathcal{L}(f_\theta(x + \delta), y) \right]$", color=TEXT_LIGHT, fontsize=11)
    ax.text(0.09, 0.14, "Enforces worst-case empirical risk minimization against perturbation set Delta (homoglyphs + cloaks).", color=TEXT_MUTED, fontsize=8.5)
    ax.text(0.09, 0.10, "Empirical result: Recovers model performance from 0.8078 F1 to 0.9780 F1 under evasion.", color=GREEN, fontsize=8)
    
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "math_formulations_card.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


# ==============================================================================
# 6. SLIDE 6: Data Loader & MD5 Deduplication
# ==============================================================================
def make_code_data_loader_dedup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "src/data_loader.py - Deduplication & Stratification")
    
    code_lines = [
        (TEXT_DIM, "250 | ", PURPLE, "# Ingest 21,908 verified malicious domains from threat intelligence feeds", None, ""),
        (TEXT_DIM, "251 | ", TEXT_LIGHT, "domains = load_malicious_domains()"),
        (TEXT_DIM, "252 | ", TEXT_LIGHT, "scam_playbooks = generate_modern_scam_samples(domains, n_samples=1500)"),
        (TEXT_DIM, "253 | ", TEXT_LIGHT, "clean_chat = generate_clean_gaming_samples(n_samples=2500)"),
        (TEXT_DIM, "254 | ", TEXT_LIGHT, "df_all = pd.DataFrame(records)"),
        (TEXT_DIM, "255 | ", None, "", None, ""),
        (TEXT_DIM, "258 | ", PURPLE, "# CRITICAL: MD5 hash-based text deduplication to stop leakage", None, ""),
        (TEXT_DIM, "259 | ", TEXT_LIGHT, "initial_count = ", YELLOW, "len", TEXT_LIGHT, "(df_all)"),
        (TEXT_DIM, "260 | ", TEXT_LIGHT, "df_all['clean_key'] = df_all['message'].str.lower().str.replace(r'\\s+', ' ', regex=True)"),
        (TEXT_DIM, "261 | ", TEXT_LIGHT, "df_all = df_all.drop_duplicates(subset=['clean_key']).drop(columns=['clean_key'])"),
        (TEXT_DIM, "262 | ", YELLOW, "print", TEXT_LIGHT, '(f"Filtered {initial_count - len(df_all)} duplicate spam copies")'),
        (TEXT_DIM, "263 | ", None, "", None, ""),
        (TEXT_DIM, "268 | ", PURPLE, "# Stratified Partitioning (80% Train, 10% Validation, 10% Test)", None, ""),
        (TEXT_DIM, "269 | ", TEXT_LIGHT, "train_df, temp_df = train_test_split("),
        (TEXT_DIM, "270 | ", TEXT_LIGHT, "    df_all, test_size=0.20, random_state=42, stratify=df_all['label'])"),
        (TEXT_DIM, "274 | ", TEXT_LIGHT, "val_df, test_df = train_test_split("),
        (TEXT_DIM, "275 | ", TEXT_LIGHT, "    temp_df, test_size=0.50, random_state=42, stratify=temp_df['label'])")
    ]
    
    y = 0.85
    for row in code_lines:
        x = 0.05
        for i in range(0, len(row), 2):
            color = row[i]
            text = row[i+1]
            if text:
                ax.text(x, y, text, color=color, fontsize=8.5, fontfamily='monospace', va='center')
                x += len(text) * 0.0095
        y -= 0.043
        
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "code_data_loader_dedup.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


# ==============================================================================
# 8. SLIDE 8: Hardened Validation & CV Analysis Card
# ==============================================================================
def make_hardened_validation_analysis():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    draw_window_chrome(ax, "validation_analysis.py [Tree Importance & CV Variance]")
    
    # Left Card: Tree Split Gain Shift
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.46), 0.42, 0.40, boxstyle="round,pad=0.01", facecolor='#1c2333', edgecolor=CYAN))
    ax.text(0.09, 0.81, "XGBOOST FEATURE GAIN SHIFT", color=CYAN, fontsize=10, fontweight='bold')
    ax.text(0.09, 0.75, "Unhardened Model:", color=TEXT_MUTED, fontsize=8.5)
    ax.text(0.09, 0.70, "1. min_levenshtein_discord (0.342)", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.09, 0.66, "2. has_url (0.281)", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.09, 0.62, "14. homoglyph_count (0.011) [Low Gain]", color=TEXT_DIM, fontsize=8)
    
    ax.text(0.09, 0.56, "Hardened Model (Post-Augmentation):", color=GREEN, fontsize=8.5, fontweight='bold')
    ax.text(0.09, 0.51, "1. min_levenshtein_discord (0.310)", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.09, 0.47, "5. homoglyph_count (0.098) [Rises 9 spots!]", color=GREEN, fontsize=8, fontweight='bold')

    # Right Card: 5-Fold Cross Validation Variance
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.46), 0.42, 0.40, boxstyle="round,pad=0.01", facecolor='#1c2925', edgecolor=GREEN))
    ax.text(0.55, 0.81, "5-FOLD STRATIFIED CV RESULTS", color=GREEN, fontsize=10, fontweight='bold')
    ax.text(0.55, 0.74, "Clean Test Fold Metrics:", color=TEXT_MUTED, fontsize=8.5)
    ax.text(0.55, 0.69, "* Precision: 0.9678 +/- 0.0085", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.55, 0.65, "* Recall:    0.9888 +/- 0.0112", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.55, 0.61, "* F1-Score:  0.9780 +/- 0.0094", color=GREEN, fontsize=8, fontweight='bold')
    
    ax.text(0.55, 0.54, "Statistical Robustness:", color=YELLOW, fontsize=8.5)
    ax.text(0.55, 0.49, "Variance remains strictly within +/- 1.1%,", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.55, 0.45, "confirming splits are not random seed artifacts.", color=TEXT_MUTED, fontsize=8)

    # Bottom Full-Width Card: Scientific Critique of 100% Recall
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.06), 0.88, 0.36, boxstyle="round,pad=0.01", facecolor='#2a2233', edgecolor=PURPLE))
    ax.text(0.09, 0.37, "SCIENTIFIC AUDIT: WHY DID ADVERSARIAL TEST HIT 100% RECALL?", color='#C678DD', fontsize=10, fontweight='bold')
    ax.text(0.09, 0.30, "1. Closed-Generator Overlap: Both augmentation and evaluation utilized build_adversarial_variant().", color=TEXT_LIGHT, fontsize=8.5)
    ax.text(0.09, 0.25, "2. Dominant Tree Split: 'homoglyph_count >= 1' created a deterministic branch catching 178 of 178 test scams.", color=YELLOW, fontsize=8.5)
    ax.text(0.09, 0.20, "3. Realistic Real-World Zero-Day Limitations:", color=TEXT_MUTED, fontsize=8.5)
    ax.text(0.09, 0.15, "   * Novel Unicode scripts outside Cyrillic plane (e.g., Cherokee, Deseret)", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.09, 0.11, "   * Right-to-Left (RTL) directional override characters (\\u202E)", color=TEXT_LIGHT, fontsize=8)
    ax.text(0.09, 0.07, "   * Multi-turn social engineering openers with zero initial URLs or keywords", color=TEXT_LIGHT, fontsize=8)
    
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "hardened_validation_analysis.png")
    plt.savefig(out, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print("Generated:", out)


if __name__ == "__main__":
    print("Building presentation slide visuals...")
    make_pipeline_overview()
    make_code_adversarial_perturbation()
    make_code_automod_regex_bypass()
    make_code_feature_extractor()
    make_math_formulations_card()
    make_code_data_loader_dedup()
    make_hardened_validation_analysis()
    print("All slide visual cards generated successfully!")
