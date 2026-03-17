🌿 Celeste — Vedic AI Astrologer


> *"The stars incline, they do not bind."*

Hey! I'm Navinya, a third-year AI/ML student from SVKM's NMIMS. I built Celeste as a passion project combining my love for astrology with everything I've been learning about AI. It's not perfect, but I'm really proud of it. 🌙

#🌐 Try it live → celeste-astrology-uyyegkybbr7isweeyqthjf.streamlit.app


---
🔮 What is Celeste?

Celeste is an AI astrologer that actually knows astrology. Not just "you're a Scorpio so you're mysterious"  but real Vedic concepts like Dasha cycles, Dosha remedies, Nakshatra positions, and actual planetary transits happening right now.

You can ask her things like:

"What does Mars Mahadasha mean for my career?"
"Am I compatible with a Virgo?"
"Give me my love horoscope for this month"
"What is Kaal Sarp Dosha and how do I remedy it?"
And she'll give you a real, personalized answer — not a generic one.

---


✨ What makes it special

Real planetary data — I have minute-by-minute planetary positions from 1990 to 2029 (yes, really). When Celeste generates your horoscope, she actually looks up where the Sun, Moon, Mars, Jupiter and every other planet is today and uses that in her answer.
14,400+ compatibility examples: The RAG system pulls from a real Vedic astrology dataset with detailed compatibility analysis including Dasha and Dosha influences. Not made up. Real data.
Reddit astrology discussions: I also indexed 2,838 high-quality posts from r/astrology, so Celeste has a sense of how real people talk about and experience astrology.
Beautiful zodiac wheel: An interactive wheel that shows all 9 Vedic planets in their current positions, color-coded by element. Built from scratch in SVG.

---


🛠️ How I built it

Honestly? With a lot of trial and error and way too many terminal errors 😅

The stack is pretty simple:
Streamlit for the UI
Groq for the AI:- running llama-3.3-70b-versatile
ChromaDB as the vector database
sentence-transformers for embeddings
Pandas for loading the planet CSV files
The hardest part was getting ChromaDB to work correctly and figuring out that `llama-3.3-70b-versatile` was decommissioned mid-build 💀

---
Run it yourself
```bash
# Clone it
git clone https://github.com/NavinyaPatil999/celeste-astrology.git
cd celeste-astrology

# Install stuff
pip install -r requirements.txt

# Get a FREE Groq API key at console.groq.com
# Create a .env file:
echo 'GROQ_API_KEY="your_key_here"' > .env

# Build the knowledge base (takes ~3 mins first time)
python run_rag.py

# Run!
streamlit run app.py
```
---
📁 What's inside
```
celeste-astrology/
├── app.py              # The whole UI lives here
├── chatbot.py          # Intent detection + chat logic
├── horoscope.py        # Horoscope generator
├── rag.py              # RAG retrieval system
├── data_loader.py      # Loads the datasets
├── planet_loader.py    # Reads the planet CSVs
├── zodiac_wheel.py     # Draws the zodiac wheel in SVG
└── data/
    ├── train.jsonl     # 11,520 compatibility examples
    ├── val.jsonl       # 1,440 more
    ├── astrology.json  # 930 Q&A pairs
    └── planets/        # 2025-2026 planetary positions
```
---

Datasets & credits
Vedic compatibility dataset — 14,400 zodiac pair examples with Dasha/Dosha analysis
Astrology Q&A — 930 pairs from a Spanish astrology knowledge base
Reddit r/astrology — top community discussions (2021)
Planetary positions — Vedic ephemeris data, minute-by-minute, 1990–2029
https://huggingface.co/vedastro-org

---
A note from me:
This was genuinely one of the most fun things I've ever built.🌱
Feel free to fork it, break it, improve it. And if you find a bug... that's probably because I was debugging at 2am 🌙
— Navinya ✨
