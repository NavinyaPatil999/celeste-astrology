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
    # FORCE horoscope for button + keyword
    if "horoscope" in user_message.lower():
        return generate_horoscope(name, sign, topic)

    # Compatibility
    if "compatibility" in user_message.lower():
        return generate_horoscope(name, sign, topic)

    # Default RAG
    context = retrieve(
        query=user_message,
        sign1=sign,
        topic=topic,
        top_k=3
    )

    prompt = f"""User: {user_message}
Context: {context}
Answer in a mystical astrology tone."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content
