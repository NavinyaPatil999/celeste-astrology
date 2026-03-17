# zodiac_wheel.py — Beautiful improved zodiac wheel
import math

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SYMBOLS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]

ELEMENTS = {
    "Fire":  ["Aries","Leo","Sagittarius"],
    "Earth": ["Taurus","Virgo","Capricorn"],
    "Air":   ["Gemini","Libra","Aquarius"],
    "Water": ["Cancer","Scorpio","Pisces"]
}

ELEMENT_COLORS = {
    "Fire":  "#E8593C",
    "Earth": "#639922",
    "Air":   "#378ADD",
    "Water": "#1D9E75"
}

PLANET_COLORS = {
    "Sun":     "#EF9F27",
    "Moon":    "#B5D4F4",
    "Mars":    "#E24B4A",
    "Mercury": "#5DCAA5",
    "Jupiter": "#FAC775",
    "Venus":   "#ED93B1",
    "Saturn":  "#888780",
    "Rahu":    "#7F77DD",
    "Ketu":    "#D85A30"
}

PLANET_SYMBOLS = {
    "Sun": "☉", "Moon": "☽", "Mars": "♂", "Mercury": "☿",
    "Jupiter": "♃", "Venus": "♀", "Saturn": "♄",
    "Rahu": "☊", "Ketu": "☋"
}

def get_element(sign):
    for elem, signs in ELEMENTS.items():
        if sign in signs:
            return elem
    return "Fire"

def generate_zodiac_wheel(user_sign: str, planet_positions: dict = None) -> str:
    cx, cy   = 310, 310
    r_outer  = 240   # outer ring
    r_inner  = 170   # inner ring
    r_symbol = 210   # zodiac symbols
    r_label  = 256   # sign name labels

    # Group planets by sign to spread them out
    sign_planets = {}
    if planet_positions:
        for planet, data in planet_positions.items():
            if planet in ['date','tithi','paksha','hora']:
                continue
            rashi = data.get('rashi','') if isinstance(data, dict) else ''
            if rashi in SIGNS:
                sign_planets.setdefault(rashi, []).append(planet)

    svg = []
    svg.append(f'''<svg width="620" height="660" viewBox="0 0 620 660" xmlns="http://www.w3.org/2000/svg">
<rect width="620" height="660" fill="#020f07" rx="16"/>

<!-- Outer decorative rings -->
<circle cx="{cx}" cy="{cy}" r="{r_outer+22}" fill="none" stroke="#52c97a" stroke-width="0.4" opacity="0.2"/>
<circle cx="{cx}" cy="{cy}" r="{r_outer+10}" fill="none" stroke="#52c97a" stroke-width="0.6" opacity="0.3"/>
<circle cx="{cx}" cy="{cy}" r="{r_outer}"    fill="none" stroke="#52c97a" stroke-width="1.2" opacity="0.7"/>
<circle cx="{cx}" cy="{cy}" r="{r_inner}"    fill="none" stroke="#52c97a" stroke-width="0.8" opacity="0.5"/>
<circle cx="{cx}" cy="{cy}" r="72"           fill="#020f07" stroke="#52c97a" stroke-width="1.5" opacity="0.9"/>

<!-- Center -->
<text x="{cx}" y="{cy-12}" text-anchor="middle" fill="#52c97a" font-size="28" font-family="serif">☽</text>
<text x="{cx}" y="{cy+14}" text-anchor="middle" fill="#52c97a" font-size="11" font-family="sans-serif" letter-spacing="3" opacity="0.9">CELESTE</text>
<text x="{cx}" y="{cy+30}" text-anchor="middle" fill="#52c97a" font-size="8" font-family="sans-serif" opacity="0.5">✦ ✦ ✦</text>
''')

    # Draw segments
    for i, (sign, symbol) in enumerate(zip(SIGNS, SYMBOLS)):
        a_start = math.radians(i * 30 - 90)
        a_mid   = math.radians(i * 30 + 15 - 90)
        a_end   = math.radians((i+1) * 30 - 90)

        # Outer segment corners
        ox1 = cx + r_outer * math.cos(a_start)
        oy1 = cy + r_outer * math.sin(a_start)
        ox2 = cx + r_outer * math.cos(a_end)
        oy2 = cy + r_outer * math.sin(a_end)

        # Inner segment corners
        ix1 = cx + r_inner * math.cos(a_start)
        iy1 = cy + r_inner * math.sin(a_start)
        ix2 = cx + r_inner * math.cos(a_end)
        iy2 = cy + r_inner * math.sin(a_end)

        elem    = get_element(sign)
        color   = ELEMENT_COLORS[elem]
        is_user = (sign == user_sign)
        fill_op = "0.45" if is_user else "0.15"
        stk_w   = "2.5" if is_user else "0.5"
        stk_op  = "0.9" if is_user else "0.35"

        # Segment fill
        svg.append(f'<path d="M {ix1:.1f} {iy1:.1f} L {ox1:.1f} {oy1:.1f} A {r_outer} {r_outer} 0 0 1 {ox2:.1f} {oy2:.1f} L {ix2:.1f} {iy2:.1f} A {r_inner} {r_inner} 0 0 0 {ix1:.1f} {iy1:.1f} Z" fill="{color}" opacity="{fill_op}" stroke="{color}" stroke-width="{stk_w}" stroke-opacity="{stk_op}"/>')

        # Gold highlight arc for user sign
        if is_user:
            svg.append(f'<path d="M {ox1:.1f} {oy1:.1f} A {r_outer} {r_outer} 0 0 1 {ox2:.1f} {oy2:.1f}" fill="none" stroke="#7fffa0" stroke-width="4" opacity="0.95"/>')
            svg.append(f'<path d="M {ix1:.1f} {iy1:.1f} A {r_inner} {r_inner} 0 0 1 {ix2:.1f} {iy2:.1f}" fill="none" stroke="#7fffa0" stroke-width="2" opacity="0.6"/>')

        # Divider lines
        svg.append(f'<line x1="{ix1:.1f}" y1="{iy1:.1f}" x2="{ox1:.1f}" y2="{oy1:.1f}" stroke="#52c97a" stroke-width="0.6" opacity="0.4"/>')

        # Zodiac symbol (inside ring)
        sx = cx + r_symbol * math.cos(a_mid)
        sy = cy + r_symbol * math.sin(a_mid)
        s_color = "#7fffa0" if is_user else color
        s_size  = "22" if is_user else "18"
        svg.append(f'<text x="{sx:.1f}" y="{sy:.1f}" text-anchor="middle" dominant-baseline="central" fill="{s_color}" font-size="{s_size}" opacity="0.95">{symbol}</text>')

        # Sign name (outside ring)
        lx = cx + r_label * math.cos(a_mid)
        ly = cy + r_label * math.sin(a_mid)
        l_color = "#7fffa0" if is_user else "#d4b896"
        l_size  = "11" if is_user else "9"
        l_weight = "bold" if is_user else "normal"
        svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" fill="{l_color}" font-size="{l_size}" font-weight="{l_weight}" font-family="sans-serif">{sign[:3]}</text>')

    # Draw planets — spread them in an arc within their sign
    for sign, planets in sign_planets.items():
        idx   = SIGNS.index(sign)
        count = len(planets)
        for j, planet in enumerate(planets):
            # Spread planets evenly within the 30-degree slice
            spread = 24 / max(count, 1)
            angle_deg = idx * 30 + 3 + j * spread - 90
            angle_rad = math.radians(angle_deg)

            # Alternate radii so they don't overlap
            radii = [r_inner - 18, r_inner - 36, r_inner - 54]
            pr = radii[j % 3]

            px = cx + pr * math.cos(angle_rad)
            py = cy + pr * math.sin(angle_rad)

            color  = PLANET_COLORS.get(planet, "#ffffff")
            symbol = PLANET_SYMBOLS.get(planet, planet[:2])

            # Planet circle
            svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="13" fill="{color}" opacity="0.92" stroke="#0d0b1e" stroke-width="1.5"/>')
            # Planet symbol
            svg.append(f'<text x="{px:.1f}" y="{py:.1f}" text-anchor="middle" dominant-baseline="central" fill="#020f07" font-size="11" font-weight="bold">{symbol}</text>')

    # Legend
    legend = [("Fire","#E8593C"), ("Earth","#639922"), ("Air","#378ADD"), ("Water","#1D9E75")]
    svg.append(f'<rect x="0" y="630" width="620" height="30" fill="#020f07"/>')
    for i, (name, color) in enumerate(legend):
        lx = 60 + i * 130
        svg.append(f'<circle cx="{lx}" cy="645" r="7" fill="{color}" opacity="0.85"/>')
        svg.append(f'<text x="{lx+12}" y="649" fill="{color}" font-size="11" font-family="sans-serif">{name}</text>')

    # Today's info
    if planet_positions:
        tithi = planet_positions.get('tithi','')
        paksha = planet_positions.get('paksha','')
        hora = planet_positions.get('hora','')
        svg.append(f'<text x="{cx}" y="598" text-anchor="middle" fill="#52c97a" font-size="10" font-family="sans-serif" opacity="0.8">Tithi {tithi} · {paksha} · Hora: {hora}</text>')

    svg.append('</svg>')
    return "\n".join(svg)
