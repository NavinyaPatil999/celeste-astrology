# planet_loader.py
import pandas as pd
import os
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANET_FOLDER = os.path.join(BASE_DIR, "data", "planets")

PLANETS = ['Moon', 'Sun', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

def get_planet_data(year: int, month: int) -> pd.DataFrame:
    """Load planet CSV for a specific year/month."""
    key_formats = [f"{year}_{month:02d}", f"{year}_{month}"]
    for key in key_formats:
        path = os.path.join(PLANET_FOLDER, f"{key}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    return None

def get_current_positions() -> dict:
    """Get today's planetary positions (daily snapshot)."""
    now = datetime.now()
    df = get_planet_data(now.year, now.month)
    if df is None:
        return {}
    
    # Get today's date string and find matching row
    today_str = now.strftime("%d-%m-%Y")
    day_data = df[df['Date'] == today_str]
    if day_data.empty:
        day_data = df.head(1)
    row = day_data.iloc[0]

    positions = {
        'date': str(row['Date']),
        'tithi': str(row['Tithi']),
        'paksha': str(row['Paksha']),
        'hora': str(row['Hora Planet']),
    }
    for planet in PLANETS:
        positions[planet] = {
            'rashi': str(row.get(f'{planet} Rashi', '')),
            'nakshatra': str(row.get(f'{planet} Nakshatra', '')),
            'pada': str(row.get(f'{planet} Pada', ''))
        }
    return positions

def format_positions_for_prompt(positions: dict) -> str:
    """Format planet positions as readable text for AI prompt."""
    if not positions:
        return "Planetary data unavailable."
    
    lines = [
        f"Date: {positions.get('date', 'Today')}",
        f"Tithi: {positions.get('tithi')} | Paksha: {positions.get('paksha')} | Hora: {positions.get('hora')}",
        "",
        "Current Planetary Positions (Vedic):"
    ]
    for planet in PLANETS:
        p = positions.get(planet, {})
        rashi = p.get('rashi', '')
        nakshatra = p.get('nakshatra', '')
        pada = p.get('pada', '')
        if rashi:
            lines.append(f"  {planet}: {rashi} | Nakshatra: {nakshatra} | Pada: {pada}")
    
    return "\n".join(lines)

def get_sign_current_transits(sign: str) -> str:
    """Get which planets are currently in or aspecting a sign."""
    positions = get_current_positions()
    if not positions:
        return ""
    
    sign_lower = sign.lower()
    transits = []
    for planet in PLANETS:
        p = positions.get(planet, {})
        rashi = p.get('rashi', '').lower()
        if sign_lower in rashi:
            transits.append(f"{planet} is currently in {sign} ({p.get('nakshatra')} nakshatra)")
    
    if transits:
        return "Active transits for " + sign + ":\n" + "\n".join(transits)
    return f"No major planets currently transiting {sign}."
