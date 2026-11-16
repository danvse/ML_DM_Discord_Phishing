"""
Data loader and preprocessor for Discord Scam Detection.
Handles loading raw datasets, augmenting with realistic conversational threat playbooks,
deduplication, stratified train/val/test splitting, and adversarial test set generation.
"""

import os
import re
import json
import random
import unicodedata
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Homoglyph substitution mapping (Latin to visually identical Cyrillic/Greek characters)
HOMOGLYPH_MAP = {
    'a': 'а',  # Cyrillic small letter a (\u0430)
    'c': 'с',  # Cyrillic small letter es (\u0441)
    'e': 'е',  # Cyrillic small letter ie (\u0435)
    'i': 'і',  # Cyrillic small letter byelorussian-ukrainian i (\u0456)
    'j': 'ј',  # Cyrillic small letter je (\u0458)
    'o': 'о',  # Cyrillic small letter o (\u043e)
    'p': 'р',  # Cyrillic small letter er (\u0440)
    's': 'ѕ',  # Cyrillic small letter dze (\u0455)
    'x': 'х',  # Cyrillic small letter ha (\u0445)
    'y': 'у',  # Cyrillic small letter u (\u0443)
}

LEET_MAP = {
    'e': '3',
    'i': '1',
    'o': '0',
    'a': '4',
    's': '5',
    't': '7'
}


def load_malicious_domains():
    domain_path = os.path.join(RAW_DIR, "malicious_domains.json")
    if os.path.exists(domain_path):
        with open(domain_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "domains" in data:
                return data["domains"]
            elif isinstance(data, list):
                return data
    return []


def generate_modern_scam_samples(domains, n_samples=1500):
    """
    Generate realistic modern Discord scam playbooks reflecting 2024-2026 threat intelligence:
    1. Indie game testing lures
    2. Steam tournament / team voting
    3. Art commission infostealers
    4. Discord Nitro giveaways / airdrops
    5. Accidental report Steam scams
    """
    sample_domains = random.choices(domains, k=n_samples) if domains else ["discoord-app.com", "steamcommunlty.com", "nitro-drop.xyz"]

    templates = [
        # Game tester lures
        "Hey! Are you active? My dev team just released an open alpha for our indie survival game on Steam/itch. Could you test the demo build and tell me if it launches? {url}",
        "yo saw you in the gaming server, me and my buddy made a 2d platformer game for a game jam, would mean a lot if you could test play it and give feedback: {url}",
        "Hey bro can you test play my new unity game demo? tell me if there are any bugs, download is here: {url}",
        "Hi! We are looking for beta testers for our upcoming unreal engine RPG. Testers get free in-game skins and $20 giftcard. Download launcher: {url}",

        # Steam tournament / team voting lures
        "Hey mate, can you do me a quick favor? My CS2 team qualified for the semifinals on Faceit/Challenger, could you vote for our team so we can qualify? {url}",
        "Yo, sorry to bother you! Can you vote for 'Team Phantom' in this Valorant community tournament? It takes 10 seconds: {url}",
        "can you help vote for my brother's team in the rocket league cup? here is the match voting link: {url}",

        # Nitro / Airdrop lures
        "@everyone Free 3 Months of Discord Nitro from Epic Games / Steam partnership! Claim here before it expires today: {url}",
        "Discord 9th Anniversary Celebration! Everyone gets 1 year of Nitro. Claim your gift link: {url}",
        "Hey, I accidentally bought an extra Discord Nitro monthly gift subscription, first one to claim it gets it: {url}",
        "@everyone Steam is giving away $50 wallet codes and free Discord Nitro to celebrate summer sale! Check it out: {url}",

        # Art commission lures
        "Hello! Are your commissions open? I saw your portfolio and loved your style. Here is the reference character sheet and moodboard in a zip file: {url}",
        "Hey, I'd like to hire you for a channel banner and server icon! Budget is $200. Here are the references and specs: {url}",

        # Accidental report lures
        "Hey man, I'm really sorry to message you out of nowhere, but I accidentally reported your Steam account for illegal purchases instead of someone else. The Steam admin told me you need to verify your account here or it will be banned: {url}",
        "urgent! someone impersonated your profile and scammed me, I submitted a report to Discord Trust & Safety with your ID by mistake. You need to appeal it here immediately: {url}",

        # Crypto / investment lures
        "I am teaching 10 people how to trade crypto and make $5,000 this week with automated trading bot. Limited spots join: {url}",
        "Solana airdrop phase 2 is live! Connect your phantom wallet to claim 500 $SOL tokens: {url}"
    ]

    generated = []
    for i in range(n_samples):
        tmpl = random.choice(templates)
        domain = sample_domains[i]
        # Randomize protocol and path
        proto = "https://" if random.random() > 0.3 else "http://"
        path = random.choice(["", "/gift", "/trade", "/demo", "/vote", "/verify", "/nitro", "/airdrop"])
        url = f"{proto}{domain}{path}"
        msg = tmpl.format(url=url)
        generated.append({
            "message": msg,
            "label": 1,
            "source": "threat_playbook"
        })

    return generated


def generate_clean_gaming_samples(n_samples=2500):
    """
    Generate realistic clean Discord gaming, social, and tech conversation lines.
    Includes legitimate URLs (youtube, twitch, github, discord.gg, steamcommunity).
    """
    legit_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://twitch.tv/shroud",
        "https://github.com/torvalds/linux",
        "https://discord.gg/minecraft",
        "https://store.steampowered.com/app/730/CounterStrike_2/",
        "https://reddit.com/r/gaming",
        "https://twitter.com/discord"
    ]

    clean_templates = [
        "anyone down for some valorant comp tonight? need 2 more",
        "what rank are you guys in rocket league?",
        "check out this crazy clip from my stream yesterday {url}",
        "did anyone watch the new update trailer? looks insane {url}",
        "bro that boss fight in elden ring took me like 40 attempts lol",
        "can someone help me with this python homework error?",
        "my ping is so high today, discord voice keeps cutting out",
        "ggs everyone, that was a fun match",
        "what time does the raid start tomorrow?",
        "here is the official documentation if you want to read more {url}",
        "has anyone tried the new nvidia drivers? did it fix the stuttering?",
        "i think the server is lagging again, messages take 5 seconds to send",
        "whats your favorite build for cyberpunk right now?",
        "dont forget we have meeting at 7pm in voice channel",
        "happy birthday man! hope you have a great day",
        "can someone send the invite link to the study server? thanks",
        "look at this cool open source project on github {url}",
        "my gpu temperature is reaching 85C, is that normal for a 3070?",
        "just got my first win in warzone after taking a month break",
        "wait did they nerf the weapon in the latest patch?",
        "check out the steam page for the autumn sale {url}",
        "good morning everyone, how was your weekend?",
        "yeah that makes sense, thanks for explaining it",
        "i will be online in about 30 mins after dinner",
        "does discord screen share support audio on mac now?"
    ]

    generated = []
    for _ in range(n_samples):
        tmpl = random.choice(clean_templates)
        if "{url}" in tmpl:
            url = random.choice(legit_urls)
            msg = tmpl.format(url=url)
        else:
            msg = tmpl
        generated.append({
            "message": msg,
            "label": 0,
            "source": "clean_chat"
        })

    return generated


def build_adversarial_variant(text):
    """
    Apply realistic attacker evasion tricks to a text string:
    1. Homoglyph substitution (Latin -> Cyrillic visually identical)
    2. Leetspeak substitution
    3. Markdown link masking: [discord.com](actual_url)
    """
    result = text

    # Markdown link masking if URL present
    urls = re.findall(r'https?://[^\s]+', result)
    if urls and random.random() > 0.4:
        target_url = urls[0]
        fake_label = random.choice(["https://discord.com/nitro", "https://steamcommunity.com/gift", "https://discord.gg/verify"])
        masked = f"[{fake_label}]({target_url})"
        result = result.replace(target_url, masked)

    # Homoglyph substitution on ~30% of eligible characters
    chars = list(result)
    for i, ch in enumerate(chars):
        if ch.lower() in HOMOGLYPH_MAP and random.random() < 0.35:
            chars[i] = HOMOGLYPH_MAP[ch.lower()]
    result = "".join(chars)

    # Leetspeak substitution on select words
    if random.random() > 0.5:
        for orig, sub in [("free", "fr33"), ("nitro", "n1tr0"), ("steam", "st34m"), ("claim", "cl41m")]:
            if orig in result.lower():
                pattern = re.compile(re.escape(orig), re.IGNORECASE)
                result = pattern.sub(sub, result)

    return result


def prepare_full_dataset():
    """
    Load raw Hugging Face data, augment with threat intelligence playbooks and clean chat,
    deduplicate, and output stratified splits + adversarial test set.
    """
    records = []

    # 1. Load Hugging Face raw dataset
    hf_path = os.path.join(RAW_DIR, "discord_phishing_scam.csv")
    if os.path.exists(hf_path):
        df_hf = pd.read_csv(hf_path)
        for _, row in df_hf.iterrows():
            content = str(row.get("msg_content", "")).strip()
            label = row.get("lable", None)
            if content and pd.notna(label):
                try:
                    lbl = int(label)
                    if lbl in [0, 1]:
                        records.append({
                            "message": content,
                            "label": lbl,
                            "source": "hf_discord"
                        })
                except ValueError:
                    pass
        print(f"Loaded {len(records)} messages from Hugging Face dataset.")

    # 2. Load malicious domains
    domains = load_malicious_domains()
    print(f"Loaded {len(domains)} malicious domains from threat list.")

    # 3. Generate modern threat playbooks (1500 scam examples)
    scam_playbooks = generate_modern_scam_samples(domains, n_samples=1500)
    records.extend(scam_playbooks)
    print(f"Added {len(scam_playbooks)} threat playbook scam samples.")

    # 4. Generate clean gaming chatter (2500 clean examples)
    clean_chat = generate_clean_gaming_samples(n_samples=2500)
    records.extend(clean_chat)
    print(f"Added {len(clean_chat)} clean chat samples.")

    df_all = pd.DataFrame(records)

    # 5. Deduplication
    initial_len = len(df_all)
    df_all["clean_text_key"] = df_all["message"].str.lower().str.replace(r'\s+', ' ', regex=True).str.strip()
    df_all = df_all.drop_duplicates(subset=["clean_text_key"]).drop(columns=["clean_text_key"])
    print(f"Deduplicated dataset: {initial_len} -> {len(df_all)} unique messages.")

    print("\nClass distribution:")
    print(df_all["label"].value_counts())

    # 6. Stratified Train / Val / Test Split (80 / 10 / 10)
    train_df, temp_df = train_test_split(
        df_all,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=df_all["label"]
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=RANDOM_SEED,
        stratify=temp_df["label"]
    )

    print(f"\nSplit counts:")
    print(f"  Train: {len(train_df)} ({train_df['label'].value_counts().to_dict()})")
    print(f"  Val:   {len(val_df)} ({val_df['label'].value_counts().to_dict()})")
    print(f"  Test:  {len(test_df)} ({test_df['label'].value_counts().to_dict()})")

    # 7. Generate Adversarial Test Set
    adv_test_records = []
    for _, row in test_df.iterrows():
        msg = row["message"]
        lbl = row["label"]
        if lbl == 1:
            # Apply adversarial perturbations to scams
            perturbed = build_adversarial_variant(msg)
            adv_test_records.append({
                "message": perturbed,
                "label": 1,
                "original_message": msg,
                "source": "adversarial_perturbed"
            })
        else:
            adv_test_records.append({
                "message": msg,
                "label": 0,
                "original_message": msg,
                "source": "clean_test"
            })

    adv_test_df = pd.DataFrame(adv_test_records)

    # 8. Save all splits
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    train_df.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False, encoding="utf-8")
    val_df.to_csv(os.path.join(PROCESSED_DIR, "val.csv"), index=False, encoding="utf-8")
    test_df.to_csv(os.path.join(PROCESSED_DIR, "test.csv"), index=False, encoding="utf-8")
    adv_test_df.to_csv(os.path.join(PROCESSED_DIR, "adversarial_test.csv"), index=False, encoding="utf-8")

    print(f"\nSaved processed datasets to: {PROCESSED_DIR}")
    return train_df, val_df, test_df, adv_test_df


if __name__ == "__main__":
    prepare_full_dataset()
