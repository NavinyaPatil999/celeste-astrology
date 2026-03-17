# horoscope.py — uses FREE Groq API + real planet data
import os
from groq import Groq
from dotenv import load_dotenv
from rag import retrieve
from planet_loader import get_current_positions, format_positions_for_prompt, get_sign_current_transits
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_horoscope(name: str, sign: str, topic: str) -> str:
    name_str = f"for {name}" if name else ""
    now = datetime.now()

    # Get RAG context from dataset
    rag_context = retrieve(
        query=f"{sign} {topic} horoscope dasha dosha",
        sign1=sign, topic=topic, top_k=3
    )

    # Get REAL planet positions from YOUR CSV data
    positions = get_current_positions()
    planet_text = format_positions_for_prompt(positions)
    transits = get_sign_current_transits(sign)

    prompt = f"""You are Celeste, a master Vedic astrologer with access to real-time planetary data.

REAL PLANETARY POSITIONS RIGHT NOW:
{planet_text}

ACTIVE TRANSITS FOR {sign.upper()}:
{transits}

KNOWLEDGE BASE:
{rag_context}

Generate a rich, personalized Vedic horoscope {name_str} for {sign} 
focused on {topic} for {now.strftime('%B %Y')}.

Use the REAL planetary positions above to make this horoscope accurate and specific.
Reference actual planets in their current signs and nakshatras.
Include: current transit effects, Tithi significance, specific prediction for {topic}, remedy or mantra.
Tone: mystical, warm, encouraging. 6-8 sentences."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8
    )
    return response.choices[0].message.content
