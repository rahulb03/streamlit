import streamlit as st
import swisseph as swe
from datetime import datetime, timedelta, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Lal Kitab & Vedic Astrology", layout="wide")

# Try to import the user's custom predictor.
try:
    from lal_kitab_predictor import LalKitabPredictor
    LAL_KITAB_AVAILABLE = True
except ImportError:
    LAL_KITAB_AVAILABLE = False

# Setup Swiss Ephemeris Path
# Update this path if you are running locally on Windows or Linux
EPHEMERIS_PATH = '/usr/share/ephe' 
try:
    swe.set_ephe_path(EPHEMERIS_PATH)
except swe.Error:
    pass

# Constants
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mercury": "Me", "Venus": "Ve",
    "Mars": "Ma", "Jupiter": "Ju", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
    "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl"
}

# Separate dictionaries for calculation
TRADITIONAL_PLANET_IDS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN
}

OUTER_PLANET_IDS = {
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
}

# --- 2. HELPER FUNCTIONS ---

def decimal_to_dms(decimal_degree):
    degree_in_sign = decimal_degree % 30
    degrees = int(degree_in_sign)
    minutes_decimal = (degree_in_sign - degrees) * 60
    minutes = int(minutes_decimal)
    return degrees, minutes

def get_sign(degree):
    return ZODIAC_SIGNS[int(degree // 30)]

def find_house(degree, cusps):
    degree = degree % 360
    for i in range(12):
        house_start_cusp = cusps[i]
        house_end_cusp = cusps[(i + 1) % 12]
        if house_start_cusp <= house_end_cusp:
            if house_start_cusp <= degree < house_end_cusp:
                return i + 1
        else:
            if degree >= house_start_cusp or degree < house_end_cusp:
                return i + 1
    return 1

@st.cache_data
def get_geo_data(location_name):
    """Geocodes location (Cached to prevent API spam)"""
    try:
        geolocator = Nominatim(user_agent="streamlit_kundali_app_v2")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception:
        return None, None
    return None, None

def get_timezone_offset(lat, lon, date_obj, time_obj):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=lat, lng=lon)
    if not timezone_name:
        return None
    local_tz = pytz.timezone(timezone_name)
    naive_dt = datetime.combine(date_obj, time_obj)
    local_dt = local_tz.localize(naive_dt)
    return (local_dt.utcoffset().total_seconds()) / 3600.0

def calculate_chart(name, dob, tob, lat, lon, tz_offset):
    # Convert inputs to Julian Day
    utc_dt = datetime.combine(dob, tob) - timedelta(hours=tz_offset)
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    cusps, ascmc = swe.houses(jd_ut, lat, lon, b'P')
    
    sidereal_cusps = [(c - ayanamsa) % 360 for c in cusps]
    ascendant_degree = (ascmc[0] - ayanamsa) % 360
    
    planets = {}
    
    # 1. Traditional Planets
    for p_name, p_id in TRADITIONAL_PLANET_IDS.items():
        xx, _ = swe.calc_ut(jd_ut, p_id)
        sid_lon = (xx[0] - ayanamsa) % 360
        is_retro = xx[3] < 0
        house = find_house(sid_lon, sidereal_cusps)
        planets[p_name] = {
            "degree": sid_lon, "sign": get_sign(sid_lon), 
            "house": house, "is_retrograde": is_retro, "type": "traditional"
        }

    # 2. Outer Planets (Included in chart, excluded from prediction logic later)
    for p_name, p_id in OUTER_PLANET_IDS.items():
        xx, _ = swe.calc_ut(jd_ut, p_id)
        sid_lon = (xx[0] - ayanamsa) % 360
        is_retro = xx[3] < 0
        house = find_house(sid_lon, sidereal_cusps)
        planets[p_name] = {
            "degree": sid_lon, "sign": get_sign(sid_lon), 
            "house": house, "is_retrograde": is_retro, "type": "outer"
        }

    # 3. Nodes (Rahu/Ketu)
    rahu_xx, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
    rahu_lon = (rahu_xx[0] - ayanamsa) % 360
    ketu_lon = (rahu_lon + 180) % 360
    
    planets["Rahu"] = {"degree": rahu_lon, "sign": get_sign(rahu_lon), "house": find_house(rahu_lon, sidereal_cusps), "is_retrograde": True, "type": "traditional"}
    planets["Ketu"] = {"degree": ketu_lon, "sign": get_sign(ketu_lon), "house": find_house(ketu_lon, sidereal_cusps), "is_retrograde": True, "type": "traditional"}

    return {
        "name": name,
        "ascendant": {"degree": ascendant_degree, "sign": get_sign(ascendant_degree)},
        "planets": planets,
        "cusps": sidereal_cusps
    }

# --- 3. SVG VISUALIZATION ---

def generate_north_indian_svg(chart):
    """Generates an SVG string for a North Indian Chart including Ascendant and Outer Planets."""
    planets = chart['planets']
    asc_sign = chart['ascendant']['sign']
    asc_degree = chart['ascendant']['degree']
    asc_sign_index = ZODIAC_SIGNS.index(asc_sign) + 1 

    # House coordinates (unchanged)
    house_text_pos = {
        1: (200, 70), 2: (100, 30), 3: (40, 120), 4: (200, 170), 
        5: (40, 280), 6: (100, 370), 7: (200, 330), 8: (300, 370), 
        9: (360, 280), 10: (200, 230), 11: (360, 120), 12: (300, 30)
    }

    house_content = {i: [] for i in range(1, 13)}
    
    # --- ADD ASCENDANT (LAGNA) TO HOUSE 1 ---
    asc_deg_int, asc_min_int = decimal_to_dms(asc_degree)
    # Adding 'Asc' explicitly to the list for House 1
    house_content[1].append(f"Asc {asc_deg_int}°{asc_min_int}'")

    # --- ADD ALL PLANETS (Traditional + Outer) ---
    for p_name, data in planets.items():
        p_sign_index = ZODIAC_SIGNS.index(data['sign'])
        # Calculate house relative to Ascendant sign
        h_num = (p_sign_index - (asc_sign_index - 1) + 12) % 12 + 1
        
        deg, mins = decimal_to_dms(data['degree'])
        retro = " (R)" if data.get('is_retrograde') else ""
        house_content[h_num].append(f"{PLANET_ABBR.get(p_name, p_name)} {deg}°{retro}")

    # Build SVG
    svg = f"""
    <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" style="background-color: white; border: 1px solid #ccc; max-width: 100%; height: auto;">
        <rect x="0" y="0" width="400" height="400" fill="none" stroke="black" stroke-width="2"/>
        <line x1="0" y1="0" x2="400" y2="400" stroke="black" stroke-width="2"/>
        <line x1="0" y1="400" x2="400" y2="0" stroke="black" stroke-width="2"/>
        <line x1="0" y1="200" x2="200" y2="0" stroke="black" stroke-width="2"/>
        <line x1="200" y1="0" x2="400" y2="200" stroke="black" stroke-width="2"/>
        <line x1="400" y1="200" x2="200" y2="400" stroke="black" stroke-width="2"/>
        <line x1="200" y1="400" x2="0" y2="200" stroke="black" stroke-width="2"/>
    """

    # Add Content (Sign Numbers and Planets)
    for h in range(1, 13):
        sign_num = (asc_sign_index + (h - 1) - 1) % 12 + 1
        x, y = house_text_pos[h]
        
        # Sign Number
        sign_offset_y = -15 if h in [1, 4, 7, 10] else 0
        svg += f'<text x="{x}" y="{y + sign_offset_y}" font-family="Arial" font-size="14" font-weight="bold" fill="#bbb" text-anchor="middle">{sign_num}</text>'
        
        # Planets
        planets_in_house = house_content[h]
        start_y = y + 5
        for i, p_str in enumerate(planets_in_house):
            # Color coding
            if "Asc" in p_str:
                color = "#AA0000" # Dark Red for Ascendant
                weight = "bold"
            elif any(x in p_str for x in ["Su", "Ma"]): 
                color = "#D32F2F" # Red
                weight = "normal"
            elif any(x in p_str for x in ["Ur", "Ne", "Pl"]):
                color = "#555555" # Grey for Outer Planets
                weight = "normal"
            else:
                color = "#1976D2" # Blue
                weight = "normal"
                
            svg += f'<text x="{x}" y="{start_y + (i*14)}" font-family="Arial" font-size="11" font-weight="{weight}" fill="{color}" text-anchor="middle">{p_str}</text>'

    svg += "</svg>"
    return svg

# --- 4. PREDICTION MOCK ---
class MockLalKitabPredictor:
    def __init__(self, filepath): pass
    def generate_chart_predictions(self, chart):
        preds = {}
        # Only predict for traditional planets found in the filtered chart
        for p, data in chart['planets'].items():
            preds[p] = {
                "house": data['house'], "sign": data['sign'],
                "prediction": f"General effects of {p} in House {data['house']} ({data['sign']}).",
                "remedy": f"Remedy for {p}."
            }
        return preds

# --- 5. STREAMLIT UI LOGIC ---

st.sidebar.header("Birth Details")
name = st.sidebar.text_input("Name", "Bharati Rahul Sudharsinh")
birth_date = st.sidebar.date_input("Date of Birth", date(2003, 11, 23))
birth_time = st.sidebar.time_input("Time of Birth", time(14, 30))
location_str = st.sidebar.text_input("Location (City, Country)", "Surat, India")

run_btn = st.sidebar.button("Generate Predictions")

if run_btn:
    with st.spinner("Calculating Planetary Positions..."):
        lat, lon = get_geo_data(location_str)
        
        if lat is None:
            st.error(f"Could not find coordinates for '{location_str}'.")
        else:
            tz_offset = get_timezone_offset(lat, lon, birth_date, birth_time)
            
            if tz_offset is None:
                st.error("Could not determine Timezone.")
            else:
                # 1. Calculate Full Chart (Includes Outer Planets)
                full_chart = calculate_chart(name, birth_date, birth_time, lat, lon, tz_offset)

                st.title(f"🔮 Lal Kitab Predictions for {name}")
                st.markdown(f"**Birth Data:** {birth_date} | {birth_time} | {location_str} (Lat: {lat:.2f}, Lon: {lon:.2f})")
                
                tab1, tab2 = st.tabs(["📜 Predictions & Remedies", "🌌 Chart & Planetary Data"])

                # --- TAB 1: PREDICTIONS ---
                with tab1:
                    st.subheader("Planetary Analysis & Remedies")
                    
                    # 2. FILTER: Create a temporary chart with ONLY traditional planets for prediction
                    prediction_chart = {
                        "name": full_chart["name"],
                        "ascendant": full_chart["ascendant"],
                        "planets": {k: v for k, v in full_chart["planets"].items() if v.get("type") == "traditional"},
                        "cusps": full_chart["cusps"]
                    }

                    if LAL_KITAB_AVAILABLE:
                        predictor = LalKitabPredictor("lal_kitab_data.txt") 
                    else:
                        st.warning("`lal_kitab_predictor.py` not found. Using demo mode.")
                        predictor = MockLalKitabPredictor("dummy")

                    # Pass filtered chart to predictor
                    predictions = predictor.generate_chart_predictions(prediction_chart)

                    for planet, info in predictions.items():
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #ff4b4b;">
                                <h4 style="margin:0; color: #31333F;">{planet} in House {info['house']} ({info['sign']})</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_pred, col_rem = st.columns([2, 1])
                            with col_pred:
                                st.markdown("**Prediction:**")
                                st.write(info['prediction'])
                            with col_rem:
                                st.success(f"**Remedy:**\n\n{info['remedy']}")
                            st.markdown("---")

                # --- TAB 2: VISUALIZATION & DATA ---
                with tab2:
                    c1, c2 = st.columns([1, 1])
                    
                    with c1:
                        st.subheader("Lagna Chart")
                        # Uses full_chart (Includes Outer Planets + Asc Label)
                        svg_chart = generate_north_indian_svg(full_chart)
                        st.markdown(svg_chart, unsafe_allow_html=True)

                    with c2:
                        st.subheader("Planetary Degrees")
                        planet_display_list = []
                        
                        # Ascendant Row
                        asc_d, asc_m = decimal_to_dms(full_chart['ascendant']['degree'])
                        planet_display_list.append({
                            "Planet": "Ascendant", "Sign": full_chart['ascendant']['sign'],
                            "Degree": f"{asc_d}° {asc_m}'", "House": 1, "Retro": "-"
                        })

                        # Planets Row
                        for p, d in full_chart['planets'].items():
                            deg, mn = decimal_to_dms(d['degree'])
                            retro = "Yes" if d.get('is_retrograde') else "No"
                            planet_display_list.append({
                                "Planet": p,
                                "Sign": d['sign'],
                                "Degree": f"{deg}° {mn}'",
                                "House": d['house'],
                                "Retro": retro
                            })
                        st.table(planet_display_list)