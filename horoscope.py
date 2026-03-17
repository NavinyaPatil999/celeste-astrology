# horoscope.py — clean working version

import os
from groq import Groq
from dotenv import load_dotenv
from rag import retrieve
from planet_loader import (
    get_current_positions,
    format_positions_for_prompt,
    get_sign_current_transits
)
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_horoscope(name: str, sign: str, topic: str) -> str:
    name_str = f"for {name}" if name else ""
    now = datetime.now()

    # RAG context
    rag_context = retrieve(
        query=f"{sign} {topic} horoscope dasha dosha",
        sign1=sign,
        topic=topic,
        top_k=3
    )

    # Planet data
    positions = get_current_positions()
    planet_text = format_positions_for_prompt(positions)
    transits = get_sign_current_transits(sign)

    prompt = f"""You are Celeste, a master Vedic astrologer.

REAL PLANETARY POSITIONS:
{planet_text}

TRANSITS:
{transits}

KNOWLEDGE:
{rag_context}

Generate a personalized horoscope {name_str} for {sign} about {topic} for {now.strftime('%B %Y')}.
Include prediction + remedy. Tone: mystical, warm."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating horoscope: {e}"