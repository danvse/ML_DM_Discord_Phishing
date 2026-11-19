# 10-to-12 Minute Final Project Demo Presentation Script
*(High-Level, Accessible, and Student-Friendly — Course Guideline: 10 to 20 Minutes)*

**Project Title:** Dual-Stream Detection of Discord Phishing Campaigns  
**Course:** Machine Learning & Data Mining (Fall 2026)  
**Presenter:** Edwin Lin (Team #18 — Solo Project)  
**Target Video Duration:** 10 – 12 Minutes (Meets the 10 – 20 Minute Course Guideline)  

---

## 📋 Presenter Quick Checklist Before Hitting Record
- [ ] **Webcam On:** Pinned in corner throughout the entire recording (Course Rubric Requirement #1: presenter's face visible).
- [ ] **Microphone Active:** Clear audio, no background hum.
- [ ] **3 Browser Tabs Ready:**
  1. `http://localhost:4200/` (Live Angular 18 Web Application)
  2. `http://127.0.0.1:8000/docs` (FastAPI Swagger UI)
  3. Presentation Slides (`DEMO_PRESENTATION_SLIDES_UPDATED.pptx` or `DEMO_PRESENTATION_SLIDES.html`)
- [ ] **VS Code Terminal Open:** In workspace `c:\Users\Dan\Downloads\ML_DM`.

---

## ⏱️ Streamlined Video Roadmap (~11 Minutes Total)

| Segment | Timestamp | Slide & Activity | What Edwin Explains to the Teacher |
| :---: | :---: | :--- | :--- |
| **1** | **0:00 – 1:30** | **Slide 1 & Slide 2** (Title & Threat) | Introduction, presentation roadmap, and why Discord scams spread so fast |
| **2** | **1:30 – 3:30** | **Slide 3 & Slide 4** (Filter Fails & Our Solution) | Why lookalike letters fool basic filters, and how our dual-stream model works |
| **3** | **3:30 – 5:30** | **Slide 5 & Slide 6** (Smart Clues & Clean Data) | High-level math made simple (brand similarity, randomness) and duplicate removal |
| **4** | **5:30 – 8:00** | **Slide 7 & Slide 8** + Terminal (`run_showcase_pipeline.py`) | Running the 17-second ML pipeline, model comparisons, and honest critique of 100% recall |
| **5** | **8:00 – 10:00** | **Slide 9** + Live Browser Demo (`localhost:4200`) | Live tests (clean message, fake Nitro, tricky Cyrillic attack) and visual SHAP bars |
| **6** | **10:00 – 11:30** | **Slide 10** + Pop-Out Chat & Wrap-Up | Live chatbox interception, post-mortem pivot (why we dropped user metadata), and conclusion |

---

# Spoken Presentation Script

---

### Segment 1: Introduction & Threat Context (0:00 – 1:30)

#### Slide 1: Introduction & Project Overview (0:00 – 0:45)
**[ON SCREEN: Presenter webcam visible in corner. Show Slide 1 with the Architecture Overview Card.]**

> **Spoken Dialogue:**  
> "Hello Professor! Welcome to my final project demonstration for Machine Learning and Data Mining. My name is Edwin Lin, presenting Team 18 as a solo project.  
>  
> Today, I'm presenting **Dual-Stream Detection of Discord Phishing Campaigns**.  
>  
> To give you a quick roadmap of what I'll cover over the next eleven to twelve minutes:  
> First, I'll explain why Discord scams trick so many people and why normal keyword filters fail.  
> Second, I'll explain my dual-stream machine learning approach that catches sneaky scam links without lagging the server.  
> Third, we'll see a quick 17-second live run in the terminal comparing different models.  
> And finally, I'll jump into my live web application to test real messages and show you our interactive pop-out chatbox."

---

#### Slide 2: Why Discord Scams are So Dangerous (0:45 – 1:30)
**[ON SCREEN: Advance to Slide 2 showing the 4 common scam tricks.]**

> **Spoken Dialogue:**  
> "On Slide 2, let's look at why Discord scams are so dangerous compared to normal spam emails.  
>  
> Unlike Twitter or public forums, Discord is built on personal friendships and private gaming servers. When an attacker compromises an account—often through a fake QR code login or malware—automated bots take over and immediately blast scam links to that user's friends list.  
>  
> Because the message comes from a close friend you've known for months, your guard is down, and people click without thinking.  
>  
> As you can see on the slide, scammers usually use four pretexts: fake Discord Nitro giveaways, asking you to test a new indie game demo that installs malware, fake tournament voting links that steal your login token, or fake crypto giveaways. Once someone clicks, their account gets compromised too, spreading the infection across the whole server."

---

### Segment 2: Filter Failures & Our Solution (1:30 – 3:30)

#### Slide 3: Why Traditional Filters Fail (1:30 – 2:30)
**[ON SCREEN: Advance to Slide 3 showing the AutoMod Regex Bypass comparison card.]**

> **Spoken Dialogue:**  
> "Slide 3 shows why basic rules and keyword blocklists fail.  
>  
> Most Discord servers rely on Discord AutoMod or community bots that search for specific banned words or exact website links. But scammers easily get around them using three simple tricks:  
>  
> 1. **Lookalike Letters (Homoglyphs):** Attackers swap English letters for visually identical Russian Cyrillic letters—like using Cyrillic `'о'` (Unicode U+043E) instead of English `'o'`. To a human eye, `discord.com` looks 100% normal. But to a computer filter looking for English letters, they don't match, so AutoMod lets the scam slip right past!  
> 2. **Disguised Links:** Scammers use Markdown formatting like `[discord.com/nitro](evil.com)`. The chat displays a blue, trusted link, but clicking it takes the victim to a credential stealer.  
> 3. **Friendly Openers:** Opening with *'Hey, are you free right now?'* with no link at all, waiting for a reply first.  
>  
> When I benchmarked traditional regex filters against these evasion tricks, their accuracy plummeted by **37.2%**, dropping from 0.86 down to 0.48. That failure is why we need smart machine learning."

---

#### Slide 4: Our Dual-Stream Solution (2:30 – 3:30)
**[ON SCREEN: Advance to Slide 4 showing the Dual-Stream Flowchart and code snippet.]**

> **Spoken Dialogue:**  
> "On Slide 4 is the solution I designed: a **Dual-Stream Detection Pipeline**.  
>  
> The core insight is simple: *Scammers can rewrite their message words in five seconds, but to steal your account, they MUST send you to a website they control.*  
>  
> So I split detection into two streams:  
> - **Stream A (The Words):** Looks at the message text and pulls out word patterns to catch pushy scam language like *'free'*, *'nitro'*, and *'claim'*.  
> - **Stream B (The Link Clues):** Extracts 17 structural hints that don't depend on specific words: it checks for foreign lookalike letters, disguised links, how close the link is to real brands like Discord or Steam, and whether the domain looks like random gibberish.  
>  
> We combine both streams and pass them to an **XGBoost decision tree model**.  
>  
> I chose XGBoost over a heavy neural network like BERT for one big reason: **speed**. A big model like BERT takes 300 milliseconds on a CPU, which would cause server chat queues to back up. XGBoost runs in just **1.2 milliseconds**, so chat stays completely real-time."

---

### Segment 3: High-Level Math & Clean Data (3:30 – 5:30)

#### Slide 5: Smart Clues: How the Model Catches Fakes (3:30 – 4:30)
**[ON SCREEN: Advance to Slide 5 showing the detection clues card.]**

> **Spoken Dialogue:**  
> "On Slide 5, let me explain the three main ideas that make Stream B so effective, without getting bogged down in math:  
>  
> 1. **Brand Lookalike Score (Edit Distance):**  
> We calculate how many letter changes it takes to turn the link into an official platform like `discord.com` or `steamcommunity.com`. If a scammer sends `discoord.com`, that's just a single letter difference, which immediately triggers suspicion. To keep it fast, if the word length is completely different, we skip checking.  
>  
> 2. **Gibberish Score (Domain Randomness):**  
> Real websites have readable, pronounceable names like `discord` or `steam`. Automated scam bots generate random, messy letters like `x7k9-free-nitro.ru`. By measuring letter randomness, the model catches bot-generated scam domains immediately.  
>  
> 3. **Practicing Against Sneaky Tricks:**  
> Rather than only training on clean data, we intentionally attacked our model during training with lookalike letters and disguised links, forcing the decision trees to learn rules that survive sneaky tricks."

---

#### Slide 6: Clean Data & Preventing Cheating (4:30 – 5:30)
**[ON SCREEN: Advance to Slide 6 showing the data pipeline and deduplication card.]**

> **Spoken Dialogue:**  
> "Looking at Slide 6, let's discuss the dataset.  
>  
> To protect user privacy and follow Discord's developer rules, I did not scrape private server chats. Instead, I gathered public research datasets: verified phishing messages, malicious domain threat feeds, and clean everyday gaming conversations.  
>  
> The most critical data engineering step was **duplicate removal**.  
> Raw scam datasets contained hundreds of exact copies of the same Nitro gift message. If you don't remove them, the model will just memorize those messages and get an artificially inflated score on the test set.  
>  
> Using an MD5 hash filter, I eliminated all duplicate copies, creating a clean, balanced dataset of **3,552 unique messages**, split into 80% training, 10% validation, and 10% testing."

---

### Segment 4: Showcase Pipeline & Model Comparison (5:30 – 8:00)

#### Slide 7: Running the Pipeline & Model Comparisons (5:30 – 7:00)
**[ON SCREEN: Switch screen to Terminal in VS Code. Run the showcase script live.]**

```powershell
# Command run live on screen:
py run_showcase_pipeline.py
```

> **Spoken Dialogue:**  
> "Now let's see the experiments in action. In my terminal, I'm running my master script: `py run_showcase_pipeline.py`.  
>  
> In just seventeen seconds, it runs the entire machine learning pipeline: data loading, baseline comparisons, model training, ablation analysis, and attack hardening.  
>  
> Here is what we learned from comparing the models:  
>  
> 1. **Traditional Text Baselines:**  
> Basic regex filters and traditional text models like Naive Bayes and SVM score high on clean text, but they completely fall apart when attackers swap letters—dropping down to under 50% accuracy because those altered letters fall outside their dictionary!  
>  
> 2. **Why XGBoost Won:**  
> Decision trees naturally handle both words and link clues. Between our tree models, Random Forest scored 0.73 but took 3.4 ms. XGBoost scored higher—**0.81 F1** before hardening—and runs in just **1.2 milliseconds**.  
>  
> 3. **The Link Clues Advantage:**  
> When we ran our feature ablation study, text-only models lost 34% of their accuracy under attack. But our link clues alone beat text models by **14%**, proving that link structure is much harder for scammers to disguise!"

---

#### Slide 8: Tough Training & Honest Model Review (7:00 – 8:00)
**[ON SCREEN: Advance to Slide 8 showing the model hardening and cross-validation card.]**

> **Spoken Dialogue:**  
> "On Slide 8, let's look at what happened when we hardened the model against attacks.  
>  
> By exposing the model to synthetic lookalike tricks during training, its detection rate rebounded to **97.8%**, catching all 178 test scams—a 100% recall rate.  
>  
> Now Professor, I want to discuss that 100% result with complete scientific honesty:  
> Whenever you see 100% in machine learning, you have to be skeptical. In my experiment, the model caught all 178 scams because the generator used for testing was similar to the one used in training. The decision trees learned that any message with a lookalike letter was almost certainly a scam.  
>  
> In the open wild against brand-new zero-day attacks, recall will naturally be lower.  
> That is why I ran **5-fold cross-validation with randomized seeds**: across all 5 folds, the model achieved a very steady **98.8% recall (±1.1%)**, proving that our structural link clues are genuinely reliable."

---

### Segment 5: Live Interactive Application Demonstration (8:00 – 10:00)

#### Slide 9 & Live Web Demo (8:00 – 10:00)
**[ON SCREEN: Switch screen to Google Chrome showing Angular 18 at `http://localhost:4200/`. Presenter webcam in corner.]**

> **Spoken Dialogue:**  
> "Now let's switch to my live web application at `localhost:4200`.  
>  
> I built this full-stack tool using **Angular 18** for the frontend, communicating with a **FastAPI backend** running on port 8000.  
> At the top, you can see our live status banner showing our latency counter running at around **1.2 milliseconds**.  
>  
> Let's test three real-world messages right now:  
>  
> **1. Normal Benign Chat:**  
> *'Hey man, are we still hopping on Valorant tonight?'*  
> I click Analyze: it takes just 1.1 milliseconds. The risk gauge stays completely green at **0.02% risk**, verdict is **APPROVED**, and the explanation bars show that ordinary words and the absence of links convinced the model it is safe.  
>  
> **2. Classic Nitro Scam:**  
> *'@everyone Steam free 3 months Discord Nitro: https://discord-nitro-gift.ru/claim'*  
> I click Analyze: the gauge turns bright red at **99.85% risk** and triggers **AUTO-QUARANTINE**. The explanation chart clearly shows that the suspicious `.ru` domain and urgency words pushed the score up.  
>  
> **3. The Sneaky Russian Lookalike Attack:**  
> Look at this link: `https://dіscord.com/gifts`.  
> To our eyes, that looks like official Discord. But the second letter—the `'і'`—is a Russian lookalike letter. Regular expression filters miss this completely.  
> But when I click Analyze with my model: it catches it instantly—flagging it at **99.42% scam probability in 1.2 milliseconds** because it detected the lookalike character and brand imitation!"

---

### Segment 6: Pop-Out Chatbox, Lessons & Wrap-Up (10:00 – 11:30)

#### Slide 10: Live Chatbox Demo & Lessons Learned (10:00 – 11:30)
**[ACTION: Click the floating 'Chat Playground' button in the bottom-right corner. The inline chatbox dialog pops open.]**

> **Spoken Dialogue:**  
> "To see how this works inside a real server, I click the floating button in the bottom-right corner to open the **Pop-Out Chatbox**.  
>  
> If I type a normal message: *'Hey, did you finish the homework?'*, it sends and gets an approved green badge.  
>  
> Now let's simulate the compromised account replying with a fake game test:  
> *'Yeah! My buddy released a game demo on Steam, can you test it? https://steamcommunity-beta.top/setup.exe'*  
>  
> I hit Enter:  
> Instantly—in 1.2 milliseconds—the system flags the message with a bright red **AUTO-QUARANTINED** warning, blocking the dangerous link from rendering clickable in chat.  
>  
> **Architectural Post-Mortem & Lessons Learned:**  
> Finally, I want to share my biggest engineering takeaway.  
> When I originally started in September, I planned to build a bot that inspected user profile data—account age, mutual servers, and avatars. But I quickly hit two brick walls: Discord bots cannot inspect private direct messages, and Discord's developer terms strictly prohibit saving user chat data for machine learning.  
>  
> Pivoting to inspect **only the message text and links** was the best decision of the project. It requires zero access to private user databases, protects user privacy completely, and makes the model fast and self-contained.  
>  
> To wrap up: on 3,552 messages, this detector achieves **97.8% accuracy** under attack, runs in **1.2 milliseconds** on CPU, and is fully deployed across FastAPI and Angular 18.  
>  
> Thank you so much for your time and guidance, Professor! I'm happy to answer any questions."

---

## 🎯 Quick Reminders for Edwin
- **Timing:** Paced for **~11 minutes**. You are comfortably within the **10 to 20 minute** course window!
- **Tone:** Friendly, confident, and explanatory. No need to memorize complicated math formulas—the concepts speak for themselves.
- **Show Your Face:** Pinned webcam in the corner throughout the video.
- **Demonstration:** Move the mouse over the 1.2 ms latency counter and the red quarantine banner to highlight your hard work.
