"""
Feature Extractor for Discord Scam Detection.
Extracts:
1. 17 Payload & Evasion structural features directly from the raw message text.
2. Word & character n-gram TF-IDF vectors for semantic intent.
3. Feature fusion helper for classical & tree-based classifiers.
"""

import os
import re
import math
import json
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import tldextract

# Target brand domains to compute Levenshtein distance against
TARGET_BRANDS = ["discord.com", "discordapp.com", "steamcommunity.com"]

SUSPICIOUS_TLDS = {
    "xyz", "top", "buzz", "click", "ru", "cc", "club", "site", "online",
    "work", "rest", "surf", "monster", "cfd", "cam", "shop", "fun"
}

URGENCY_KEYWORDS = [
    "nitro", "free", "gift", "claim", "airdrop", "tournament", "giveaway",
    "steam", "wallet", "beta", "alpha", "test", "demo", "commission",
    "urgent", "accidentally", "banned", "appeal", "trade", "crypto", "profit"
]

ATTACHMENT_EXTENSIONS = [".exe", ".scr", ".zip", ".rar", ".bat", ".vbs", ".cmd", ".iso"]

# Non-Latin Unicode ranges for homoglyph detection (Cyrillic, Greek, etc.)
HOMOGLYPH_REGEX = re.compile(r'[\u0400-\u04FF\u0370-\u03FF\u0500-\u052F]')


def levenshtein_distance(s1, s2):
    """Compute basic Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def shannon_entropy(string):
    """Calculate Shannon entropy of a string (measures randomness)."""
    if not string:
        return 0.0
    entropy = 0.0
    length = len(string)
    counts = {}
    for ch in string:
        counts[ch] = counts.get(ch, 0) + 1
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return float(entropy)


class DiscordFeatureExtractor:
    def __init__(self, malicious_domains_path=None, max_tfidf_features=3000):
        self.max_tfidf_features = max_tfidf_features
        self.malicious_domains = set()

        if malicious_domains_path and os.path.exists(malicious_domains_path):
            with open(malicious_domains_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "domains" in data:
                    self.malicious_domains = set(data["domains"])
                elif isinstance(data, list):
                    self.malicious_domains = set(data)

        # Word TF-IDF vectorizer
        self.word_tfidf = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=self.max_tfidf_features,
            sublinear_tf=True,
            strip_accents="unicode"
        )

        self.feature_names = [
            "has_url",
            "num_urls",
            "min_levenshtein_discord",
            "min_levenshtein_steam",
            "domain_entropy",
            "is_known_bad_domain",
            "has_suspicious_tld",
            "has_ip_in_url",
            "has_markdown_mask",
            "homoglyph_count",
            "urgency_token_count",
            "uppercase_ratio",
            "mention_count",
            "spoiler_mask_count",
            "has_attachment_ext",
            "message_length",
            "digit_ratio"
        ]

    def extract_heuristics_single(self, text):
        """Extract the numeric heuristic feature vector for a single message string."""
        text = str(text) if text is not None else ""
        length = len(text)

        # Find URLs
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
        has_url = 1 if len(urls) > 0 else 0
        num_urls = len(urls)

        # Domain inspection
        extracted_domains = []
        min_dist_discord = 99
        min_dist_steam = 99
        max_entropy = 0.0
        is_known_bad = 0
        has_susp_tld = 0
        has_ip = 0

        for u in urls:
            ext = tldextract.extract(u)
            reg_domain = f"{ext.domain}.{ext.suffix}".lower() if ext.suffix else ext.domain.lower()
            extracted_domains.append(reg_domain)

            # Check known bad list
            if reg_domain in self.malicious_domains or ext.fqdn.lower() in self.malicious_domains:
                is_known_bad = 1

            # Check suspicious TLDs
            if ext.suffix.lower() in SUSPICIOUS_TLDS:
                has_susp_tld = 1

            # Check raw IP
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ext.domain):
                has_ip = 1

            # Levenshtein distances
            d1 = levenshtein_distance(reg_domain, "discord.com")
            d2 = levenshtein_distance(reg_domain, "discordapp.com")
            d_disc = min(d1, d2)
            if d_disc < min_dist_discord:
                min_dist_discord = d_disc

            d_steam = levenshtein_distance(reg_domain, "steamcommunity.com")
            if d_steam < min_dist_steam:
                min_dist_steam = d_steam

            ent = shannon_entropy(ext.domain)
            if ent > max_entropy:
                max_entropy = ent

        if not urls:
            min_dist_discord = 50
            min_dist_steam = 50

        # Markdown link masking: [label](url)
        markdown_masks = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', text)
        has_markdown_mask = 1 if len(markdown_masks) > 0 else 0

        # Homoglyphs
        homoglyphs = HOMOGLYPH_REGEX.findall(text)
        homoglyph_count = len(homoglyphs)

        # Urgency keywords
        text_lower = text.lower()
        urgency_count = sum(1 for kw in URGENCY_KEYWORDS if kw in text_lower)

        # Uppercase ratio
        upper_count = sum(1 for c in text if c.isupper())
        uppercase_ratio = upper_count / max(1, length)

        # Mentions (@everyone, @here, <@!id>)
        mentions = re.findall(r'@everyone|@here|<@!?[0-9]+>', text)
        mention_count = len(mentions)

        # Spoiler masks (||link||)
        spoilers = re.findall(r'\|\|([^\|]+)\|\|', text)
        spoiler_mask_count = len(spoilers)

        # Attachment references
        has_attach = 1 if any(ext in text_lower for ext in ATTACHMENT_EXTENSIONS) else 0

        # Digit ratio
        digit_count = sum(1 for c in text if c.isdigit())
        digit_ratio = digit_count / max(1, length)

        return [
            has_url,
            num_urls,
            min(min_dist_discord, 50),
            min(min_dist_steam, 50),
            round(max_entropy, 3),
            is_known_bad,
            has_susp_tld,
            has_ip,
            has_markdown_mask,
            homoglyph_count,
            urgency_count,
            round(uppercase_ratio, 3),
            mention_count,
            spoiler_mask_count,
            has_attach,
            min(length, 1000),
            round(digit_ratio, 3)
        ]

    def extract_heuristics(self, texts):
        """Extract matrix of heuristics for an iterable of texts."""
        rows = [self.extract_heuristics_single(t) for t in texts]
        return np.array(rows, dtype=np.float32)

    def fit(self, texts):
        """Fit the TF-IDF vectorizer on training text."""
        self.word_tfidf.fit(texts)
        return self

    def transform_tfidf(self, texts):
        """Transform text into sparse TF-IDF feature matrix."""
        return self.word_tfidf.transform(texts)

    def transform_fused(self, texts):
        """Return combined sparse matrix [TF-IDF + Heuristics]."""
        tfidf_mat = self.transform_tfidf(texts)
        heur_mat = csr_matrix(self.extract_heuristics(texts))
        return hstack([tfidf_mat, heur_mat], format="csr")

    def fit_transform_fused(self, texts):
        """Fit TF-IDF on texts and return combined feature matrix."""
        self.fit(texts)
        return self.transform_fused(texts)


if __name__ == "__main__":
    extractor = DiscordFeatureExtractor(
        malicious_domains_path=os.path.join(os.path.dirname(__file__), "..", "data", "raw", "malicious_domains.json")
    )
    sample_text = "@everyone Free Nitro for everyone! Click [discord.com](https://discorcl-app.com/free)"
    heuristics = extractor.extract_heuristics_single(sample_text)
    for name, val in zip(extractor.feature_names, heuristics):
        print(f"  {name:25s}: {val}")
