# app.py — Celeste — Forest Green Luxury Edition
import streamlit as st
from rag import build_index
from chatbot import chat
from planet_loader import get_current_positions, format_positions_for_prompt
from zodiac_wheel import generate_zodiac_wheel

st.set_page_config(page_title="Celeste — Vedic Astrologer", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background: linear-gradient(160deg, #020f07 0%, #041a0e 40%, #061f10 100%);
    color: #d4e8d0;
}

/* ── Headings use Cormorant ── */
h1, h2, h3, .celeste-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 300 !important;
    letter-spacing: 0.08em !important;
    color: #7fffa0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #020f07 !important;
    border-right: 1px solid #1a4a2a !important;
}
[data-testid="stSidebar"] label {
    color: #52c97a !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

/* ── Inputs & Selects ── */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: #041a0e !important;
    border: 1px solid #1a4a2a !important;
    border-radius: 4px !important;
    color: #d4e8d0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus {
    border-color: #52c97a !important;
    box-shadow: 0 0 0 1px #52c97a22 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #52c97a !important;
    color: #52c97a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #52c97a15 !important;
    border-color: #7fffa0 !important;
    color: #7fffa0 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #041a0e !important;
    border: 1px solid #1a4a2a !important;
    border-radius: 6px !important;
    margin-bottom: 10px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border: 1px solid #1a4a2a !important;
    background: #041a0e !important;
    border-radius: 4px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid #1a4a2a !important;
    border-radius: 6px !important;
    background: #041a0e !important;
}

/* ── Divider ── */
hr { border-color: #1a4a2a !important; }

/* ── Caption / small text ── */
.stCaption, small { color: #52c97a88 !important; font-size: 10px !important; letter-spacing: 0.08em; }

/* ── Planet card ── */
.planet-card {
    background: #041a0e;
    border: 1px solid #1a4a2a;
    border-left: 2px solid #52c97a;
    border-radius: 4px;
    padding: 8px 10px;
    margin: 4px 0;
}
.planet-name { color: #52c97a; font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; }
.planet-rashi { color: #d4e8d0; font-size: 12px; }
.planet-nakshatra { color: #52c97a66; font-size: 10px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #020f07; }
::-webkit-scrollbar-thumb { background: #1a4a2a; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Setup ──────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def setup():
    build_index()
    return True

@st.cache_data(ttl=3600, show_spinner=False)
def load_planets():
    return get_current_positions()

with st.spinner(""):
    setup()

# ── Header ─────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem 0;'>
  <div style='font-family: Cormorant Garamond, serif; font-size: 13px; letter-spacing: 0.4em; color: #52c97a; text-transform: uppercase; margin-bottom: 0.5rem;'>✦ Vedic AI Astrologer ✦</div>
  <div style='font-family: Cormorant Garamond, serif; font-size: 52px; font-weight: 300; color: #7fffa0; letter-spacing: 0.1em; line-height: 1;'>Celeste</div>
  <div style='font-size: 11px; color: #52c97a55; letter-spacing: 0.2em; margin-top: 0.5rem; text-transform: uppercase;'>Real planetary data · 16,700+ examples · Dasha & Dosha aware</div>
</div>
<hr style='border-color: #1a4a2a; margin: 0 0 1.5rem 0;'/>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Cormorant Garamond,serif; font-size:20px; color:#7fffa0; letter-spacing:0.1em; padding: 1rem 0 0.5rem 0;'>Your Profile</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1a4a2a; margin: 0 0 1rem 0;'/>", unsafe_allow_html=True)

    name  = st.text_input("Name", placeholder="e.g. Navinya")
    sign  = st.selectbox("Zodiac Sign", [
        "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
        "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
    ])
    sign2 = st.selectbox("Partner's Sign", [
        "None","Aries","Taurus","Gemini","Cancer","Leo","Virgo",
        "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
    ])
    topic = st.selectbox("Focus Area", [
        "Love & Romance","Career & Success",
        "Finance & Wealth","Health & Wellness","General"
    ])
    st.markdown("<hr style='border-color:#1a4a2a;'/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        horoscope_btn = st.button("Horoscope")
    with col2:
        compat_btn = st.button("Compatibility")

    st.markdown("<hr style='border-color:#1a4a2a;'/>", unsafe_allow_html=True)
    show_wheel   = st.checkbox("Zodiac Wheel", value=True)
    show_planets = st.checkbox("Planet Positions", value=True)
    st.markdown("<hr style='border-color:#1a4a2a;'/>", unsafe_allow_html=True)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<div style='color:#52c97a44; font-size:10px; letter-spacing:0.1em; margin-top:1rem;'>Try asking about Sade Sati, Kaal Sarp Dosha, or your Mahadasha period</div>", unsafe_allow_html=True)

# ── Planet positions ───────────────────────────────────────────────
planets = load_planets()

if show_planets and planets:
    with st.expander("🪐  Today's Planetary Positions", expanded=False):
        tithi_line = f"**Tithi {planets.get('tithi','')}** · {planets.get('paksha','')} · Hora: **{planets.get('hora','')}**"
        st.markdown(f"<div style='color:#52c97a; font-size:12px; letter-spacing:0.08em; margin-bottom:0.8rem;'>{tithi_line}</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        planet_list = ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']
        for i, p in enumerate(planet_list):
            data = planets.get(p, {})
            if isinstance(data, dict) and data.get('rashi'):
                with cols[i % 3]:
                    st.markdown(f"""<div class='planet-card'>
                        <div class='planet-name'>{p}</div>
                        <div class='planet-rashi'>{data.get('rashi','')}</div>
                        <div class='planet-nakshatra'>{data.get('nakshatra','')}</div>
                    </div>""", unsafe_allow_html=True)

# ── Zodiac Wheel ───────────────────────────────────────────────────
if show_wheel:
    with st.expander("🌌  Zodiac Wheel", expanded=True):
        wheel_svg = generate_zodiac_wheel(sign, planets)
        st.components.v1.html(wheel_svg, height=680, scrolling=False)

st.markdown("<hr style='border-color:#1a4a2a;'/>", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_history():
    return [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ["user", "assistant"]
    ]

def add_bot_msg(label, content):
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"**{label}**\n\n{content}"
    })

# ── Buttons ────────────────────────────────────────────────────────
if horoscope_btn:
    with st.spinner("Reading the stars..."):
        try:
            result = chat(f"Generate my {topic} horoscope", sign, name, topic, get_history())
            add_bot_msg(f"✦  {sign} — {topic} Horoscope", result)
        except Exception as e:
            st.error(f"Error: {e}")
    st.rerun()

if compat_btn:
    if sign2 == "None":
        st.sidebar.warning("Select a partner's sign first.")
    else:
        with st.spinner(f"Analysing {sign} × {sign2}..."):
            try:
                result = chat(
                    f"Analyze compatibility between {sign} and {sign2} for {topic} with dasha and dosha influences.",
                    sign, name, topic, get_history()
                )
                add_bot_msg(f"✦  {sign} × {sign2} — {topic}", result)
            except Exception as e:
                st.error(f"Error: {e}")
        st.rerun()

# ── Chat history ───────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "✦" if msg["role"] == "user" else "🌿"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ─────────────────────────────────────────────────────
if prompt := st.chat_input("Ask Celeste anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="✦"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("Consulting the cosmos..."):
            try:
                response = chat(prompt, sign, name, topic, get_history())
            except Exception as e:
                response = f"Error: {e}"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
