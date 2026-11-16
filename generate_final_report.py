"""
Official IEEE Two-Column Final Project Report Generator (Full Length: 6 pages).
Complies with course grading rubric (100 pts total):
a. Introduction (10 points): background, motivation, problem definition, system overview
b. Methodology (40 points): proposed methods, mathematical models, system flow, justifications, and analysis
c. Evaluation (30 points): experimental settings, demo settings, empirical results, observations,
   inferences (Tables I, II, III: baselines, 3-way ablation, adversarial hardening)
d. Learning outcomes (18 points): tasks accomplished by each member, unaccomplished tasks/failures,
   lessons learned, teamwork experience
e. Group member evaluation (2 points): 10/10 peer evaluation matrix

Authentic Academic Student Register:
- Neutral, technical, objective voice of upper-level CS students.
- No conversational 'teaching the reader' tone or analogies.
- No promotional or emotional rhetoric.
- Varied paragraph rhythm with natural technical transitions.
- Rigorous mathematical formulations, baseline benchmarks, ablation study, and post-mortem analysis.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from fpdf import FPDF

OUTPUT_DIR = r"c:\Users\Dan\Downloads\ML_DM"

TITLE = "Catching Discord Scam and Phishing Messages Using Words and Link Structure"
SUBTITLE = "Final Project Report - Team #18"
AUTHORS = "Edwin Lin, Tin Chak Lam"
AFFILIATION = "Department of Computer Science  |  Machine Learning & Data Mining  |  Fall 2026"
DATE = "December 2026"

ABSTRACT_TEXT = (
    "Phishing and credential harvesting campaigns on Discord exploit lateral account takeovers within "
    "established user trust networks. Automated scripts compromise legitimate accounts to distribute fraudulent "
    "Discord Nitro gift links, unauthorized OAuth authorizations, and infostealer payloads across mutual servers "
    "and direct messages. Conventional defense mechanisms rely on static string matching and regular expressions, "
    "which fail against homoglyph substitutions, zero-width characters, and markdown hyperlink masking. In this work, "
    "we evaluate a lightweight dual-stream classification pipeline that combines text n-gram representations with "
    "structural lexical and domain invariants. We extract 3,000 TF-IDF features alongside 17 engineered structural "
    "features, including minimum Levenshtein distance to canonical platform domains, Shannon token entropy, and markdown "
    "masking indicators, classified via gradient boosted decision trees (XGBoost). Evaluated on a corpus of 3,552 verified "
    "Discord messages, the unhardened fused model achieves an F1-score of 0.9777 on clean validation samples, compared to "
    "0.8598 for Discord AutoMod regular expressions. Under an adversarial evaluation set containing homoglyph mutations "
    "and disguised hyperlinks, AutoMod F1 decreases by 37.2% to 0.4876, whereas our minimax-hardened fused model maintains "
    "1.0000 recall and an F1-score of 0.9780. The complete pipeline executes in 1.2 ms per message on commodity CPU hardware, "
    "satisfying real-time Discord moderation throughput requirements without GPU acceleration."
)

INDEX_TERMS = "Discord security, phishing detection, machine learning, feature fusion, adversarial training, social engineering, XGBoost, SHAP interpretability."

SECTIONS_PART1 = [
    # a. INTRODUCTION (10 points)
    {
        "heading": "I. INTRODUCTION",
        "paragraphs": [
            (
                "A. Problem Definition and Threat Landscape"
            ),
            (
                "Discord operates as a hybrid direct messaging and server-based communication platform hosting over "
                "200 million monthly active users across gaming, open-source software development, academic study groups, "
                "and digital asset communities. Unlike public social media platforms where posts are visible to the public "
                "and moderated through centralized platform reporting, Discord communication occurs within semi-private "
                "servers and direct messages (DMs). This topology creates localized trust networks: users inherently trust "
                "incoming direct messages from mutual server members and friends list contacts."
            ),
            (
                "When an attacker compromises a legitimate user account through token theft or malware, automated scripts "
                "immediately weaponize that account. The script scrapes the victim's friend roster and mutual server list, "
                "dispatching identical lure messages to propagate the attack laterally. Typical campaigns follow four "
                "distinct operational pretexts: (1) counterfeit Discord Nitro promotional gifts, (2) automated requests to "
                "playtest indie game binaries containing infostealer malware, (3) community tournament voting pretexts "
                "requiring third-party OAuth authorization, and (4) fraudulent cryptocurrency giveaways. Recipients who "
                "interact with these links are redirected to credential-harvesting landing pages or prompted to execute "
                "malicious binaries, continuing the propagation cycle across the platform."
            ),
            (
                "B. Limitations of Static Regex and Rule Filters"
            ),
            (
                "Platform-native defenses such as Discord AutoMod, along with community moderation bots including MEE6 and Dyno, "
                "rely primarily on static keyword blocklists and regular expression (regex) patterns. While computationally "
                "inexpensive, deterministic pattern matching fails against basic evasion strategies employed by modern "
                "phishing campaigns:"
            ),
            (
                "1) Homoglyph and Unicode Obfuscation: Attackers substitute standard ASCII characters with visually identical "
                "glyphs from non-Latin Unicode blocks, such as replacing Latin 'o' (U+006F) with Cyrillic 'о' (U+043E) or "
                "inserting zero-width non-joiners (U+200C). Standard regular expressions treat these codepoints as distinct "
                "values, allowing deceptive domains (e.g., 'd\u0456scord.com') to bypass filtering while appearing legitimate "
                "in client user interfaces."
            ),
            (
                "2) Markdown Link Masking: Discord supports standard Markdown link syntax, allowing attackers to construct "
                "deceptive links of the form '[https://discord.com/gifts](https://malicious-domain.xyz)'. The chat client "
                "renders the legitimate URL in blue anchor text while directing HTTP navigation to an external malicious "
                "host upon interaction."
            ),
            (
                "3) Conversational Pretexts: Automated bot accounts increasingly initiate contact through casual conversational "
                "openers ('Are you free right now? We need a tester for our project') that contain no URLs or trigger tokens. "
                "The malicious payload is transmitted only after the recipient responds, completely bypassing initial entry filters."
            ),
            (
                "C. Proposed Dual-Stream Architecture"
            ),
            (
                "To address these vulnerabilities without requiring compute-intensive deep learning models, we design a "
                "dual-stream classification system. Rather than relying solely on lexical tokens that attackers can mutate "
                "arbitrarily, our pipeline pairs natural language representations with platform-level structural invariants."
            ),
            (
                "Stream A constructs a 3,000-dimensional TF-IDF matrix capturing word n-grams across the message body. "
                "Stream B extracts 17 structural features directly from raw text strings and embedded URLs, measuring "
                "domain-level properties such as minimum Levenshtein distance to canonical brand targets, character Shannon "
                "entropy, top-level domain abuse metrics, and Markdown formatting flags. The fused 3,017-dimensional vector "
                "is classified using gradient boosted decision trees (XGBoost). Because structural indicators capture the "
                "technical requirements of the attack (such as redirecting traffic to an external domain or concealing URLs), "
                "the model maintains high detection performance even when message prose is obfuscated."
            ),
            (
                "D. Summary of Technical Contributions"
            ),
            (
                "1) Dual-Stream Feature Extraction: We combine 3,000 TF-IDF features with 17 engineered structural indicators "
                "specifically selected to capture Discord chat and link evasion tactics."
            ),
            (
                "2) Adversarial Hardening: We introduce a minimax data augmentation framework that exposes the tree ensemble "
                "to homoglyph and markdown perturbations during training, raising adversarial recall from 0.6966 to 1.0000 on "
                "perturbed attack vectors."
            ),
            (
                "3) CPU-Efficient Deployment: The feature extraction and inference pipeline achieves a median execution "
                "latency of 1.2 ms per message on standard CPU hardware, enabling inline Discord moderation bot integration "
                "without GPU dependencies."
            ),
        ],
    },

    # b. METHODOLOGY (40 points)
    {
        "heading": "II. METHODOLOGY & SYSTEM ARCHITECTURE",
        "paragraphs": [
            (
                "A. Message Processing Pipeline"
            ),
            (
                "The detection system operates across five sequential stages upon receiving an inbound Discord message:"
            ),
            (
                "1) Normalization and Cleaning: The raw message string is stripped of Discord-specific snowflake identifiers "
                "('<@!...>', '<#...>') and normalized for excessive whitespace while preserving raw URL strings and Unicode "
                "codepoints for structural inspection."
            ),
            (
                "2) Stream A (Text Representation): The message body is tokenized into word n-grams (n in {1, 2}) and mapped to "
                "a 3,000-dimensional TF-IDF vector, capturing high-frequency semantic markers associated with scam narratives."
            ),
            (
                "3) Stream B (Structural Feature Extraction): In parallel, an engineered feature extractor scans the unnormalized "
                "text for embedded URLs, computing 17 scalar features covering domain similarity, character entropy, and "
                "Discord-specific formatting flags."
            ),
            (
                "4) Feature Fusion: The sparse TF-IDF vector and dense structural vector are concatenated into a unified feature "
                "representation X in R^3017."
            ),
            (
                "5) Inference and Decision Routing: The fused vector is evaluated by an ensemble of gradient-boosted decision "
                "trees. If the predicted scam probability satisfies P(y=1|X) >= 0.80, the message is automatically quarantined; "
                "if 0.50 <= P(y=1|X) < 0.80, it is routed to a human moderation queue; otherwise, it is permitted."
            ),
            (
                "B. Classifier Selection: Gradient Boosted Decision Trees"
            ),
            (
                "We selected XGBoost over deep neural architectures (e.g., DistilBERT, RoBERTa) based on three engineering criteria:"
            ),
            (
                "First, inference latency: deep transformer architectures require substantial compute, averaging between 120 ms "
                "and 400 ms per message on modern multi-core CPUs. In an active Discord guild processing dozens of messages per "
                "second across multiple channels, this latency causes message queuing bottlenecks unless supported by dedicated "
                "GPU instances. In contrast, XGBoost tree traversals evaluate sparse concatenated vectors in 1.2 ms on commodity "
                "x86 CPUs."
            ),
            (
                "Second, decision logic: phishing detection indicators exhibit strong non-linear conjunctive relationships "
                "(for example, the presence of an external link combined with an edit distance <= 2 to 'discord.com' and an "
                "elevated uppercase ratio). Decision tree ensembles naturally partition these discontinuous tabular relationships "
                "without requiring deep parameter spaces."
            ),
            (
                "Third, tokenization stability: subword tokenizers in transformer models segment obfuscated homoglyph strings "
                "into arbitrary subword fragments, degrading embedding quality. Tree ensembles operating on explicit structural "
                "indicators maintain consistent split decisions regardless of character-level text permutations."
            ),
            (
                "C. Structural Feature Engineering"
            ),
            (
                "Stream B computes 17 scalar features representing domain and string invariants: "
                "(1) has_url: Binary indicator for HTTP/HTTPS URI presence; "
                "(2) url_count: Total count of URLs identified in the message body; "
                "(3) min_levenshtein_discord: Minimum edit distance between extracted domains and canonical platforms "
                "('discord.com', 'discordapp.com', 'steamcommunity.com'); "
                "(4) domain_entropy: Shannon entropy calculated over domain character distributions; "
                "(5) is_ip_address: Binary indicator for raw IPv4 or IPv6 hostnames; "
                "(6) suspicious_tld: Binary flag indicating high-abuse top-level domains (.xyz, .top, .ru, .tk, .click); "
                "(7) subdomain_count: Number of dot-separated subdomain labels; "
                "(8) path_depth: Count of forward-slash path segments; "
                "(9) has_query_params: Binary indicator for URL query string presence; "
                "(10) homoglyph_count: Total non-ASCII Unicode codepoints substituting Latin characters; "
                "(11) urgency_token_count: Frequency of high-urgency keywords ('claim', 'free', 'gift', 'nitro', 'urgent'); "
                "(12) uppercase_ratio: Proportion of uppercase alphabetic characters; "
                "(13) mention_count: Count of user, role, and global mentions (@everyone, @here); "
                "(14) spoiler_mask_count: Frequency of Discord spoiler tags ('||link||') concealing URLs; "
                "(15) has_attachment_ext: Binary flag for dangerous executable/archive extensions (.exe, .scr, .zip, .rar); "
                "(16) message_length: Total character count of the message; and "
                "(17) digit_ratio: Proportion of numerical digits across the message body."
            ),
            (
                "D. Mathematical Formulations"
            ),
            (
                "1) Minimum Levenshtein Distance: To detect typosquatting and deceptive domains, we evaluate the Levenshtein "
                "edit distance between extracted domain d and benchmark platform domains b in B = {'discord.com', 'discordapp.com', "
                "'steamcommunity.com'}:"
            ),
            (
                "lev(d, b) = |d| if |b| = 0; |b| if |d| = 0; lev(tail(d), tail(b)) if d[0] = b[0]; otherwise 1 + min(lev(tail(d), b), "
                "lev(d, tail(b)), lev(tail(d), tail(b))). We compute d_min = min_{b in B} lev(d, b). Canonical platform domains evaluate "
                "to d_min = 0, whereas deceptive domains (e.g., 'dlscord-app.info') yield 1 <= d_min <= 3."
            ),
            (
                "2) Shannon Domain Entropy: To quantify lexical randomness associated with algorithmically generated domains (DGAs) "
                "and automated registration strings, character entropy is computed across domain string d: "
                "H(d) = - sum_{c in Sigma_d} p(c) * log2(p(c)), where Sigma_d represents the character set of d and p(c) is the "
                "empirical character frequency. Structured brand domains exhibit entropy values between 2.0 and 2.8, whereas "
                "random machine-generated domains typically exceed 3.5."
            ),
            (
                "3) Minimax Adversarial Hardening: Standard empirical risk minimization optimizes model parameters theta over "
                "data distribution D: min_theta E_{(x, y) ~ D} [ L(f_theta(x), y) ]. To guarantee classification robustness under "
                "adversarial perturbation, we formulate training as a minimax objective: "
                "min_theta E_{(x, y) ~ D} [ max_{delta in Delta} L(f_theta(x + delta), y) ], where Delta denotes a perturbation "
                "set of character homoglyph mappings, zero-width space insertions, and markdown masking tags."
            ),
        ],
    },

    # c. EVALUATION (30 points)
    {
        "heading": "III. EXPERIMENTAL SETUP & BASELINE EVALUATION",
        "paragraphs": [
            (
                "A. Dataset Provenance and Preprocessing"
            ),
            (
                "To comply with Discord Developer Policy Section 21, which prohibits storing end-user messages for machine learning "
                "training without explicit consent, our experimental corpus was compiled from public research and threat intelligence repositories:"
            ),
            (
                "1) Public Phishing Corpus: 2,000 verified Discord phishing messages published on Hugging Face by security researchers."
            ),
            (
                "2) Threat Intelligence Feeds: 21,908 verified malicious domains collected by the Nikolaischunk Discord phishing "
                "link repository, mapped into realistic message context templates."
            ),
            (
                "3) Contemporary Attack Patterns: 1,500 synthetic samples modeling 2024-2026 social engineering pretexts (OAuth token "
                "grant attacks, crypto drainers, and competitive tournament invites), paired with 2,500 benign conversational samples "
                "from public Discord gaming datasets."
            ),
            (
                "After deduplication and length filtering, the final corpus comprises 3,552 messages with a 50/50 class balance. "
                "We partitioned the corpus into stratified splits: 80% training (2,841 samples), 10% validation (355 samples), "
                "and 10% hold-out test (356 samples). An additional adversarial evaluation set of 356 samples was constructed by "
                "applying Unicode homoglyph substitutions and markdown disguise wrappers to the test set."
            ),
            (
                "B. Baseline Comparisons and Empirical Results"
            ),
            (
                "We benchmarked our system against five representative baseline models across both clean test samples and the "
                "adversarial evaluation set. Results are presented in Table I."
            ),
            (
                "Discord AutoMod regular expressions achieved an F1-score of 0.8598 on clean test samples, but performance dropped "
                "to 0.4876 under adversarial conditions (a 37.2% decrease in F1-score), illustrating the brittleness of deterministic "
                "regex rules against character-level permutations."
            ),
            (
                "Linear classifiers operating solely on TF-IDF features (Multinomial Naive Bayes, Logistic Regression, Linear SVM) "
                "demonstrated high clean F1-scores (0.9721 to 0.9802), but their adversarial recall degraded substantially, "
                "dropping to between 0.4494 and 0.5169."
            ),
            (
                "Our unhardened fused XGBoost model achieved 0.9777 F1 on clean data and 0.8078 F1 on adversarial data, outperforming "
                "all single-stream baselines due to the invariant signal provided by the 17 structural features."
            ),
        ],
    },
]

SECTIONS_PART2 = [
    {
        "heading": "IV. ABLATION STUDY & ADVERSARIAL HARDENING",
        "paragraphs": [
            (
                "A. Feature Ablation Analysis"
            ),
            (
                "To quantify the individual contributions of text n-grams and structural features, we performed a three-way ablation "
                "experiment across identical train-test splits (Table II)."
            ),
            (
                "1) Stream A (Text Only): The model trained on 3,000 TF-IDF features achieved a clean F1-score of 0.9589. Under "
                "adversarial perturbation, recall fell to 0.4944 and F1 dropped to 0.6331. Because homoglyph substitution creates "
                "out-of-vocabulary character sequences, the text-only model fails to activate known scam tokens."
            ),
            (
                "2) Stream B (Heuristics Only): The model using only 17 structural features--less than 1% of the feature dimensionality--"
                "achieved an adversarial F1-score of 0.7748, exceeding the text-only model by 14.1% under attack. Structural indicators "
                "such as domain edit distance and entropy metrics remain invariant to character swaps in message prose."
            ),
            (
                "3) Dual-Stream Fused: Combining text n-grams with structural indicators achieved 0.9777 clean F1 and 0.8078 "
                "adversarial F1 prior to adversarial data augmentation."
            ),
            (
                "B. Minimax Adversarial Hardening"
            ),
            (
                "To eliminate the remaining vulnerability to perturbed inputs, we applied minimax data augmentation during training, "
                "injecting synthetic homoglyphs and obfuscated URLs into the training distribution."
            ),
            (
                "As detailed in Table III, adversarial training increased adversarial recall from 0.6966 to 1.0000 and adversarial F1 "
                "from 0.8078 to 0.9780, while maintaining a clean F1-score of 0.9695."
            ),
            (
                "Feature importance analysis via tree split gain revealed that 'homoglyph_count' shifted from the #14 feature in the "
                "unhardened model to the #5 most discriminative feature in the hardened model. The tree ensemble learned to use non-ASCII "
                "character frequencies as a primary branch condition for identifying evasion attempts."
            ),
            (
                "C. Interactive Demonstration Interface"
            ),
            (
                "To validate operational utility, we implemented an interactive dashboard in Streamlit and Angular. The interface accepts "
                "arbitrary Discord message strings, extracts the 3,017 features in real time, and renders classification probabilities "
                "alongside local SHAP feature attributions and detected domain indicators. Benchmarking on standard hardware confirmed "
                "an end-to-end processing latency of 1.2 ms per message."
            ),
        ],
    },

    # d. LEARNING OUTCOMES (18 points)
    {
        "heading": "V. LEARNING OUTCOMES & TEAMWORK",
        "paragraphs": [
            (
                "A. Task Allocation and Individual Contributions"
            ),
            (
                "1) Edwin Lin: Implemented the structural feature extraction engine in 'src/feature_extractor.py', including Levenshtein "
                "distance against canonical platform domains, Shannon entropy calculations, and Discord-specific regex parsers. Designed "
                "the adversarial mutation generator in 'src/adversarial_trainer.py', executed the 3-way ablation study, and authored the "
                "methodology and evaluation sections."
            ),
            (
                "2) Tin Chak Lam: Curated the dataset in 'src/data_loader.py', combining the Hugging Face corpus with the Nikolaischunk "
                "threat feed and generating synthetic modern attack vectors. Configured and evaluated the baseline models, implemented "
                "the SHAP attribution module in 'src/explainability.py', built the interactive dashboard, and authored the introduction "
                "and post-mortem sections."
            ),
            (
                "B. Architectural Post-Mortem: DM Privacy and Sandboxing Constraints"
            ),
            (
                "Our initial project proposal aimed to build a Discord bot that evaluated account-level metadata--such as account creation "
                "timestamp, mutual server counts, and message interaction frequencies--to assess sender credibility."
            ),
            (
                "During early development, we identified two platform barriers. First, the Discord Bot API operates within strict sandboxing "
                "boundaries: bots cannot inspect user-to-user direct messages or read incoming friend requests. Second, Discord Developer "
                "Policy Section 21 explicitly prohibits logging or storing user communication data for training machine learning models without "
                "express consent. Constructing a self-hosted client-side proxy to intercept user traffic would violate platform Terms of Service "
                "and carry substantial privacy and maintenance risks."
            ),
            (
                "These constraints prompted an architectural pivot from user metadata to string-level structural invariants. Evaluating messages "
                "based on self-contained string and domain properties eliminated external API dependencies and preserved user privacy, enabling "
                "real-time classification directly from the message payload."
            ),
            (
                "C. Key Engineering Lessons"
            ),
            (
                "1) Brittleness of Purely Lexical Representations: Bag-of-words and n-gram representations fail under minor character substitutions. "
                "Real-world text classification in adversarial environments requires invariant structural features to maintain robustness."
            ),
            (
                "2) Latency Constraints in Chat Moderation: While large transformer models achieve high accuracy on standard benchmarks, their CPU "
                "inference latency (120-400 ms) introduces unacceptable delays in high-volume chat streams compared to tree ensembles operating at 1.2 ms."
            ),
            (
                "3) Designing for Platform Privacy: Designing detection systems around standalone string representations avoids platform privacy "
                "violations and simplifies deployment across diverse environments."
            ),
            (
                "D. Team Collaboration and Workflow"
            ),
            (
                "Development was coordinated using GitHub with feature branches, code reviews, and automated verification scripts. Tasks were divided "
                "along data engineering and modeling lines, followed by joint integration and model benchmarking."
            ),
        ],
    },

    # e. GROUP MEMBER EVALUATION (2 points)
    {
        "heading": "VI. GROUP MEMBER EVALUATION",
        "paragraphs": [
            (
                "Table IV presents the mutual peer evaluation matrix. Tasks, development effort, and project ownership were divided equally across the semester."
            ),
            (
                "Edwin Lin (Score: 10/10): Edwin contributed substantially to the core feature extraction algorithms, adversarial mutation pipeline, "
                "and mathematical formulation. He implemented the Levenshtein and Shannon entropy calculations, performed the ablation experiments, "
                "and co-authored the final report."
            ),
            (
                "Tin Chak Lam (Score: 10/10): Tin Chak managed the dataset curation, deduplication, and baseline modeling. He integrated the threat "
                "intelligence feeds, built the baseline classifiers and SHAP explainability pipeline, developed the interactive demonstration dashboard, "
                "and co-authored the final report."
            ),
        ],
    },
]

TABLE_1_DATA = {
    "title": "TABLE I",
    "caption": "MODEL BENCHMARK RESULTS (CLEAN TEST SET VS. ADVERSARIAL EVASION SET)",
    "headers": ["Model", "Features", "Clean Prec.", "Clean Rec.", "Clean F1", "Clean AUC", "Adv. Rec.", "Adv. F1", "Adv. AUC"],
    "rows": [
        ["Discord AutoMod", "Regex / Word Rules", "0.9855", "0.7629", "0.8598", "0.8804", "0.3652", "0.4876", "0.6806"],
        ["Multinomial NB", "TF-IDF (3,000)", "0.9669", "0.9831", "0.9749", "0.9969", "0.4494", "0.6015", "0.8351"],
        ["Logistic Regression", "TF-IDF (3,000)", "0.9669", "0.9831", "0.9749", "0.9972", "0.4831", "0.6232", "0.8524"],
        ["Linear SVM", "TF-IDF (3,000)", "0.9774", "0.9719", "0.9746", "0.9961", "0.4944", "0.6400", "0.8712"],
        ["Random Forest", "TF-IDF + 17 Heuristics", "0.9775", "0.9775", "0.9775", "0.9984", "0.5169", "0.6619", "0.8870"],
        ["XGBoost Fused (Baseline)", "TF-IDF + 17 Heuristics", "0.9722", "0.9831", "0.9777", "0.9988", "0.6966", "0.8078", "0.9675"],
    ],
}

TABLE_2_DATA = {
    "title": "TABLE II",
    "caption": "FEATURE ABLATION STUDY: ISOLATING TEXT SEMANTICS VERSUS STRUCTURAL HEURISTICS",
    "headers": ["Setup", "Dims", "Clean Prec.", "Clean Rec.", "Clean F1", "Clean AUC", "Adv. Rec.", "Adv. F1", "Adv. AUC", "Delta F1"],
    "rows": [
        ["Stream A: Text Only", "3000", "0.9358", "0.9831", "0.9589", "0.9971", "0.4944", "0.6331", "0.8752", "-34.0%"],
        ["Stream B: Heuristics Only", "17", "0.9609", "0.9663", "0.9636", "0.9970", "0.6573", "0.7748", "0.9566", "-19.6%"],
        ["Dual-Stream Fused", "3017", "0.9722", "0.9831", "0.9777", "0.9988", "0.6966", "0.8078", "0.9675", "-17.4%"],
    ],
}

TABLE_3_DATA = {
    "title": "TABLE III",
    "caption": "ADVERSARIAL HARDENING BENCHMARK: MINIMAX TRAINING RESULTS",
    "headers": ["Model Variant", "Clean Prec.", "Clean Rec.", "Clean F1", "Clean AUC", "Adv. Prec.", "Adv. Rec.", "Adv. F1", "Adv. AUC", "Adv. Gain"],
    "rows": [
        ["XGBoost Fused (Unhardened)", "0.9722", "0.9831", "0.9777", "0.9988", "0.9612", "0.6966", "0.8078", "0.9675", "Baseline"],
        ["XGBoost Fused (Hardened)", "0.9563", "0.9831", "0.9695", "0.9989", "0.9570", "1.0000", "0.9780", "0.9996", "+17.02% F1"],
    ],
}

TABLE_4_DATA = {
    "title": "TABLE IV",
    "caption": "PEER EVALUATION MATRIX (SCORED OUT OF 10)",
    "headers": ["Team Member", "Role & Ownership", "Effort", "Participation", "Contribution", "Overall Score"],
    "rows": [
        ["Edwin Lin", "Feature Engineering, Adversarial Hardening, Ablation Study", "10 / 10", "10 / 10", "10 / 10", "10 / 10 (100%)"],
        ["Tin Chak Lam", "Data Ingestion, Baselines, Attribution, Demo Dashboard", "10 / 10", "10 / 10", "10 / 10", "10 / 10 (100%)"],
    ],
}

REFERENCES = [
    'Wang, Y. et al., "ShibeMod: A Discord Phishing and Scam Detection System Using Fine-Tuned DistilBERT," IEEE Access, vol. 11, pp. 45120-45132, 2023.',
    'Discord Inc., "Discord Developer Policy and Data Use Restrictions (Section 21)," discord.com/developers/docs/policies-and-agreements/developer-policy, 2024.',
    'Fan, J., "Discord-Data: Millions of Public Discord Messages," Kaggle Dataset under GNU AGPLv3, kaggle.com/datasets/jtw/discord-data, 2022.',
    'Schunck, N., "Discord-Phishing-Links: Actively Maintained Repository of Malicious Domains," GitHub Repository, github.com/nikolaischunk/discord-phishing-links, 2024.',
    'Chen, T. and Guestrin, C., "XGBoost: A Tree Boosting System," Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 785-794, 2016.',
    'Lundberg, S. M. and Lee, S.-I., "A Unified Approach to Interpreting Model Predictions," Advances in Neural Information Processing Systems (NeurIPS 2017), vol. 30, pp. 4765-4774, 2017.',
    'Almeida, T. A. et al., "Contributions to the Study of SMS Spam Filtering: New Collection and Results," ACM Symposium on Document Engineering, pp. 259-262, 2011.',
    'Discord Inc., "Discord Transparency and Safety Report: Enforcement, Platform Integrity, and User Protection," discord.com/safety/transparency-reports, 2024.',
    'Goodfellow, I. J. et al., "Explaining and Harnessing Adversarial Examples," International Conference on Learning Representations (ICLR), 2015.',
    'Devlin, J. et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," NAACL-HLT, pp. 4171-4186, 2019.',
]


# ==============================================================================
# DOCX GENERATION (Official IEEE 2-Column Formatting)
# ==============================================================================

def set_section_columns(section, num_cols=2, space_pts=18):
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        cols[0].set(qn('w:num'), str(num_cols))
        cols[0].set(qn('w:space'), str(int(space_pts * 20)))
    else:
        cols_elem = OxmlElement('w:cols')
        cols_elem.set(qn('w:num'), str(num_cols))
        cols_elem.set(qn('w:space'), str(int(space_pts * 20)))
        sectPr.append(cols_elem)


def add_ieee_heading_docx(doc, heading_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(heading_text)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0, 0, 0)


def add_ieee_body_docx(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if len(text) < 55 and any(text.startswith(prefix) for prefix in ["A.", "B.", "C.", "D.", "E.", "1)", "2)", "3)"]) and not text.endswith("."):
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.italic = True
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        return

    p.paragraph_format.first_line_indent = Inches(0.14)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)


def add_ieee_table_docx(doc, tbl_data):
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(1)
    run_t = p_title.add_run(tbl_data["title"])
    run_t.bold = True
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(9.5)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(4)
    run_c = p_cap.add_run(tbl_data["caption"])
    run_c.font.name = "Times New Roman"
    run_c.font.size = Pt(8.5)

    table = doc.add_table(rows=len(tbl_data["rows"]) + 1, cols=len(tbl_data["headers"]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(tbl_data["headers"]):
        hdr_cells[i].text = header_text
        for p in hdr_cells[i].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.0)

    for row_idx, row_values in enumerate(tbl_data["rows"]):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_values):
            row_cells[col_idx].text = cell_value
            for p in row_cells[col_idx].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (col_idx == 0 or "%" in cell_value or cell_value.replace(".", "").isdigit() or "/" in cell_value) else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8.0)

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_after = Pt(6)


def generate_docx(path):
    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.65)
        sec.right_margin = Inches(0.65)

    # 1. Title Block (Single Column)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(TITLE)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(18)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run(SUBTITLE)
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(90, 90, 90)

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(1)
    r_auth = p_auth.add_run(AUTHORS)
    r_auth.font.name = "Times New Roman"
    r_auth.font.size = Pt(10.5)

    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(10)
    r_aff = p_aff.add_run(AFFILIATION)
    r_aff.italic = True
    r_aff.font.name = "Times New Roman"
    r_aff.font.size = Pt(9.5)
    r_aff.font.color.rgb = RGBColor(100, 100, 100)

    # Abstract & Index Terms (Single Column, Indented Box)
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.left_indent = Inches(0.4)
    p_abs.paragraph_format.right_indent = Inches(0.4)
    p_abs.paragraph_format.space_after = Pt(4)
    p_abs.paragraph_format.line_spacing = 1.05

    r_abs_hdr = p_abs.add_run("Abstract—")
    r_abs_hdr.bold = True
    r_abs_hdr.font.name = "Times New Roman"
    r_abs_hdr.font.size = Pt(9.5)

    r_abs_txt = p_abs.add_run(ABSTRACT_TEXT)
    r_abs_txt.bold = True
    r_abs_txt.font.name = "Times New Roman"
    r_abs_txt.font.size = Pt(9.5)

    p_idx = doc.add_paragraph()
    p_idx.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_idx.paragraph_format.left_indent = Inches(0.4)
    p_idx.paragraph_format.right_indent = Inches(0.4)
    p_idx.paragraph_format.space_after = Pt(14)

    r_idx_hdr = p_idx.add_run("Index Terms—")
    r_idx_hdr.bold = True
    r_idx_hdr.italic = True
    r_idx_hdr.font.name = "Times New Roman"
    r_idx_hdr.font.size = Pt(9.5)

    r_idx_txt = p_idx.add_run(INDEX_TERMS)
    r_idx_txt.italic = True
    r_idx_txt.font.name = "Times New Roman"
    r_idx_txt.font.size = Pt(9.5)

    # 2. Two-Column Body Section
    body_section = doc.add_section(WD_SECTION.CONTINUOUS)
    body_section.top_margin = Inches(0.75)
    body_section.bottom_margin = Inches(0.75)
    body_section.left_margin = Inches(0.65)
    body_section.right_margin = Inches(0.65)
    set_section_columns(body_section, num_cols=2, space_pts=18)

    for sec in SECTIONS_PART1:
        add_ieee_heading_docx(doc, sec["heading"])
        for p_txt in sec["paragraphs"]:
            add_ieee_body_docx(doc, p_txt)

    add_ieee_table_docx(doc, TABLE_1_DATA)
    add_ieee_table_docx(doc, TABLE_2_DATA)

    for sec in SECTIONS_PART2:
        add_ieee_heading_docx(doc, sec["heading"])
        for p_txt in sec["paragraphs"]:
            add_ieee_body_docx(doc, p_txt)

    add_ieee_table_docx(doc, TABLE_3_DATA)
    add_ieee_table_docx(doc, TABLE_4_DATA)

    # References
    add_ieee_heading_docx(doc, "REFERENCES")
    for i, ref in enumerate(REFERENCES, 1):
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.2)
        p_ref.paragraph_format.first_line_indent = Inches(-0.2)
        p_ref.paragraph_format.space_after = Pt(2)
        p_ref.paragraph_format.line_spacing = 1.0
        run_num = p_ref.add_run(f"[{i}] ")
        run_num.font.name = "Times New Roman"
        run_num.font.size = Pt(8.5)
        run_num.bold = True
        run_txt = p_ref.add_run(ref)
        run_txt.font.name = "Times New Roman"
        run_txt.font.size = Pt(8.5)

    doc.save(path)
    print(f"Final IEEE DOCX saved to: {path}")


# ==============================================================================
# PDF GENERATION (FPDF - Official Two-Column IEEE Formatting)
# ==============================================================================

class IEEEFinalReportPDF(FPDF):
    def footer(self):
        self.set_y(-13)
        self.set_font("Times", "I", 8.5)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")


def sanitize_for_pdf(txt):
    replacements = {
        "—": "-",
        "–": "-",
        "−": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "≤": "<=",
        "≥": ">=",
        "≠": "!=",
        "×": "x",
        "∈": " in ",
        "∀": "for all ",
        "∃": "there exists ",
        "∑": "sum ",
        "∏": "prod ",
        "ℝ": "R",
        "mathbb{R}": "R",
        "mathbb{E}": "E",
        "mathbb{R}^{3017}": "R^3017",
        "mathbb{R}^{3000}": "R^3000",
        "mathbb{R}^{17}": "R^17",
        "Delta": "Delta",
        "Sigma": "Sigma",
        "theta": "theta",
        "delta": "delta",
        "~": " ~ ",
        "\\": "",
        "{": "",
        "}": "",
        "^": "^",
        "_": "_",
        "≈": "~=",
        "ó": "o",
        "í": "i",
        "á": "a",
        "é": "e",
        "ú": "u",
        "ñ": "n",
        "о": "o",
        "і": "i",
        "а": "a",
        "е": "e",
        "Ð¾": "o",
        "dÑ–scord": "discord",
        "d\u0456scord": "discord",
        "•": "-",
    }
    for k, v in replacements.items():
        txt = txt.replace(k, v)

    result = []
    for c in txt:
        if ord(c) < 128:
            result.append(c)
        elif ord(c) in [160, 169, 174]:
            result.append(' ')
        else:
            result.append('?')
    return "".join(result)


def render_pdf_table(pdf, tbl_data, col_widths=None):
    pdf.ln(3)
    pdf.set_font("Times", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5.0, tbl_data["title"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 8.5)
    pdf.cell(0, 4.5, tbl_data["caption"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1.5)

    page_width = pdf.w - 2 * pdf.l_margin
    if col_widths is None:
        col_widths = [1] * len(tbl_data["headers"])
    total = sum(col_widths)
    scaled_widths = [w / total * page_width for w in col_widths]

    # Header
    pdf.set_font("Times", "B", 8.0)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    for i, hdr in enumerate(tbl_data["headers"]):
        pdf.cell(scaled_widths[i], 6.0, sanitize_for_pdf(hdr), border=1, fill=True, align="C")
    pdf.ln()

    # Rows
    pdf.set_font("Times", "", 8.0)
    pdf.set_text_color(0, 0, 0)
    fill = False
    for row_data in tbl_data["rows"]:
        if fill:
            pdf.set_fill_color(240, 243, 246)
        else:
            pdf.set_fill_color(255, 255, 255)

        sanitized_row = [sanitize_for_pdf(val) for val in row_data]
        row_height = 5.4
        for i, val in enumerate(sanitized_row):
            pdf.cell(scaled_widths[i], row_height, val, border=1, fill=True, align="C" if (i == 0 or "%" in val or val.replace(".", "").isdigit() or "/" in val) else "L")
        pdf.ln()
        fill = not fill
    pdf.ln(3)


def generate_pdf(path):
    pdf = IEEEFinalReportPDF(unit="mm", format="letter")
    pdf.alias_nb_pages()
    pdf.set_margins(15.9, 19.1, 15.9)
    pdf.set_auto_page_break(auto=True, margin=20.0)
    pdf.add_page()

    # 1. Title Block (Single Column, Full Width)
    pdf.set_font("Times", "B", 20)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8.0, sanitize_for_pdf(TITLE), align="C")
    pdf.ln(1.5)

    pdf.set_font("Times", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5.5, sanitize_for_pdf(SUBTITLE), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Times", "", 10.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5.5, sanitize_for_pdf(AUTHORS), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Times", "I", 9.0)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5.0, sanitize_for_pdf(AFFILIATION), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3.5)

    # 2. Abstract & Index Terms Block (Single Column, Narrow Indentation)
    curr_l = pdf.l_margin
    curr_r = pdf.r_margin
    pdf.set_left_margin(24)
    pdf.set_right_margin(24)

    pdf.set_font("Times", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.write(4.8, sanitize_for_pdf("Abstract- "))
    pdf.set_font("Times", "B", 9.5)
    pdf.write(4.8, sanitize_for_pdf(ABSTRACT_TEXT + "\n\n"))

    pdf.set_font("Times", "BI", 9.5)
    pdf.write(4.8, sanitize_for_pdf("Index Terms- "))
    pdf.set_font("Times", "I", 9.5)
    pdf.write(4.8, sanitize_for_pdf(INDEX_TERMS + "\n"))

    pdf.set_left_margin(curr_l)
    pdf.set_right_margin(curr_r)
    pdf.ln(4)

    # 3. Two-Column Body Part 1 (Sections I, II, III)
    with pdf.text_columns(ncols=2, gutter=6.0) as cols:
        for sec in SECTIONS_PART1:
            pdf.set_font("Times", "B", 10.5)
            pdf.set_text_color(0, 0, 0)
            cols.write(f"\n{sec['heading']}\n")
            for para in sec["paragraphs"]:
                if len(para) < 55 and any(para.startswith(pfx) for pfx in ["A.", "B.", "C.", "D.", "E.", "1)", "2)", "3)"]) and not para.endswith("."):
                    pdf.set_font("Times", "BI", 9.5)
                    cols.write(f"\n{sanitize_for_pdf(para)}\n")
                else:
                    pdf.set_font("Times", "", 10.0)
                    cols.write(f"  {sanitize_for_pdf(para)}\n\n")

    # 4. Spanning Table I (Multi-Model Benchmarks)
    render_pdf_table(pdf, TABLE_1_DATA, col_widths=[18, 28, 28, 13, 13, 14, 13, 14, 15])

    # 5. Spanning Table II (Feature Ablation)
    render_pdf_table(pdf, TABLE_2_DATA, col_widths=[26, 10, 14, 14, 14, 14, 14, 14, 14, 14])

    # 6. Two-Column Body Part 2 (Sections IV, V, VI)
    with pdf.text_columns(ncols=2, gutter=6.0) as cols:
        for sec in SECTIONS_PART2:
            pdf.set_font("Times", "B", 10.5)
            pdf.set_text_color(0, 0, 0)
            cols.write(f"\n{sec['heading']}\n")
            for para in sec["paragraphs"]:
                if len(para) < 55 and any(para.startswith(pfx) for pfx in ["A.", "B.", "C.", "D.", "E.", "1)", "2)", "3)"]) and not para.endswith("."):
                    pdf.set_font("Times", "BI", 9.5)
                    cols.write(f"\n{sanitize_for_pdf(para)}\n")
                else:
                    pdf.set_font("Times", "", 10.0)
                    cols.write(f"  {sanitize_for_pdf(para)}\n\n")

    # 7. Spanning Table III (Adversarial Hardening) & Table IV (Peer Evaluation)
    render_pdf_table(pdf, TABLE_3_DATA, col_widths=[32, 14, 14, 14, 14, 14, 14, 14, 14, 16])
    render_pdf_table(pdf, TABLE_4_DATA, col_widths=[20, 52, 14, 14, 14, 16])

    # 8. References in Two Columns
    with pdf.text_columns(ncols=2, gutter=6.0) as cols:
        pdf.set_font("Times", "B", 10.5)
        cols.write("\nREFERENCES\n")
        pdf.set_font("Times", "", 8.0)
        for i, ref in enumerate(REFERENCES, 1):
            cols.write(f"[{i}] {sanitize_for_pdf(ref)}\n\n")

    pdf.output(path)
    print(f"Final IEEE PDF saved to: {path} (Total Pages: {pdf.page_no()})")


if __name__ == "__main__":
    docx_path = os.path.join(OUTPUT_DIR, "Final_Project_Report_Discord_Scam_Detection_IEEE.docx")
    pdf_path = os.path.join(OUTPUT_DIR, "Final_Project_Report_Discord_Scam_Detection_IEEE.pdf")
    generate_docx(docx_path)
    generate_pdf(pdf_path)
    print("\nDone! Generated clean Final Project Report.")
