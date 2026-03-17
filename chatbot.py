import os
from groq import Groq
from dotenv import load_dotenv
from rag import retrieve
from horoscope import generate_horoscope

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

INTENTS = {
    "horoscope":     ["horoscope", "prediction", "forecast", "today",
                      "this week", "this month", "future", "generate my"],
    "compatibility": ["compatible", "compatibility", "match", "partner",
                      "together", "love match", "relationship with"],
    "dasha":         ["dasha", "mahadasha", "antardasha", "period", "cycle"],
    "dosha":         ["dosha", "mangal", "shani", "kaal sarp", "sade sati",
                      "remedy", "remedies"],
    "meaning":       ["what is", "explain", "meaning", "tell me about", "define"],
}

def detect_intent(message):
    msg = message.lower()
    for intent, keywords in INTENTS.items():
        if any(k in msg for k in keywords):
            return intent
    return "general"

def chat(user_message, sign, name, topic, history):
    intent = detect_intent(user_message)

    if intent == "horoscope":
        return generate_horoscope(name, sign, topic)

    context = retrieve(query=user_message, sign1=sign, topic=topic, top_k=3)

    system_prompt = f"""You are Celeste, a wise Vedic astrologer AI.
User: {name if name else 'Seeker'}, Sign: {sign}, Topic: {topic}
Astrology Knowledge:
{context}
Be mystical, warm, and specific to {sign}. Answer in 4-6 sentences."""

    messages = [{"role": "system", "content": system_prompt}]
    for m in history[-6:]:
        if m["role"] in ["user", "assistant"]:
            messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content
