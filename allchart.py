# import swisseph as swe
# from datetime import datetime, timedelta
# import tkinter as tk
# from geopy.geocoders import Nominatim
# from timezonefinder import TimezoneFinder
# import pytz
# import math

# # --- Setup and Constants ---
# try:
#     # Ensure this path is correct for your system.
#     # For Windows, it might look like 'C:/swisseph/ephe'
#     # For Linux/macOS, it's often '/usr/share/ephe'
#     swe.set_ephe_path('/usr/share/ephe')
# except swe.Error:
#     print("Error: Swiss Ephemeris path not found. Please set the correct path in the script.")
#     print("Download ephemeris files from http://www.astro.com/swisseph/swoeph.zip")
#     print("Extract them and point swe.set_ephe_path() to the directory containing 'sepha.se1', etc.")
#     exit()

# ZODIAC_SIGNS = [
#     "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
#     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
# ]

# PLANET_NAMES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]
# PLANET_ABBR = {
#     "Sun": "Su", "Moon": "Mo", "Mercury": "Me", "Venus": "Ve",
#     "Mars": "Ma", "Jupiter": "Ju", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
#     "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl"
# }

# # Define traditional and outer planet IDs globally
# traditional_planet_ids = {
#     "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
#     "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN
# }

# outer_planet_ids = {
#     "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
# }

# # Vedic Astrology Specific Data
# # Exaltation signs and degrees (approximate)
# EXALTATION = {
#     "Sun": ("Aries", 10),
#     "Moon": ("Taurus", 3),
#     "Mars": ("Capricorn", 28),
#     "Mercury": ("Virgo", 15), # Also its Moolatrikona
#     "Jupiter": ("Cancer", 5),
#     "Venus": ("Pisces", 27),
#     "Saturn": ("Libra", 20),
# }

# # Debilitation signs and degrees
# DEBILITATION = {
#     "Sun": ("Libra", 10),
#     "Moon": ("Scorpio", 3),
#     "Mars": ("Cancer", 28),
#     "Mercury": ("Pisces", 15),
#     "Jupiter": ("Capricorn", 5),
#     "Venus": ("Virgo", 27),
#     "Saturn": ("Aries", 20),
# }

# # Combustion Orbs (approximate, degrees from Sun)
# COMBUSTION_ORBS = {
#     "Moon": 12,
#     "Mercury": 14, # 12 if direct, 14 if retrograde
#     "Venus": 10,  # 8 if direct, 10 if retrograde
#     "Mars": 17,
#     "Jupiter": 11,
#     "Saturn": 15,
# }

# # New: Define status symbols based on the image
# STATUS_SYMBOLS = {
#     "retrograde": "✶",
#     "combust": "ˆ",
#     "vargottama": "¤",
#     "exalted": "†",
#     "debilitated": "↓"
# }


# # --- Helper for Degree, Minute, Second (DMS) Conversion ---
# def decimal_to_dms(decimal_degree):
#     """Converts a decimal degree to (degrees, minutes, seconds) tuple within its sign."""
#     degree_in_sign = decimal_degree % 30 # Get degree within the current sign
    
#     degrees = int(degree_in_sign)
#     minutes_decimal = (degree_in_sign - degrees) * 60
#     minutes = int(minutes_decimal)
#     seconds = int((minutes_decimal - minutes) * 60)
#     return degrees, minutes, seconds

# # --- Core Calculation Functions ---

# def get_coords(location_name):
#     """Geocodes a location name to get latitude and longitude."""
#     try:
#         geolocator = Nominatim(user_agent="kundali_app_v3")
#         location = geolocator.geocode(location_name)
#         if location:
#             return location.latitude, location.longitude
#     except Exception as e:
#         print(f"Geocoding error: {e}")
#     return None, None

# def get_timezone_offset(lat, lon, date_str, time_str):
#     tf = TimezoneFinder()
#     timezone_name = tf.timezone_at(lat=lat, lng=lon)
#     if not timezone_name:
#         print("Could not detect timezone. Exiting.")
#         return None
#     local_tz = pytz.timezone(timezone_name)
    
#     try:
#         if len(time_str.split(':')) == 3: # HH:MM:SS format
#             naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
#         else: # HH:MM format, default seconds to 00
#             naive_dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")
#     except ValueError:
#         print(f"Invalid time format for {date_str} {time_str}. Please use HH:MM or HH:MM:SS.")
#         return None

#     local_dt = local_tz.localize(naive_dt)
#     return (local_dt.utcoffset().total_seconds()) / 3600.0

# def get_sign(degree):
#     return ZODIAC_SIGNS[int(degree // 30)]

# def find_house(degree, cusps):
#     """
#     Determines the house number (1-12) for a given degree based on house cusps.
#     Assumes cusps are sorted and represent the start of each house.
#     """
#     degree = degree % 360

#     for i in range(12):
#         house_start_cusp = cusps[i]
#         house_end_cusp = cusps[(i + 1) % 12]

#         if house_start_cusp <= house_end_cusp:
#             if house_start_cusp <= degree < house_end_cusp:
#                 return i + 1
#         else: # House crosses the 0/360 degree point
#             if degree >= house_start_cusp or degree < house_end_cusp:
#                 return i + 1
#     return 1 # Fallback, should always find a house


# def calculate_planets_and_ascendant(date_str, time_str, latitude, longitude, timezone_offset):
#     """
#     Calculates planetary positions, ascendant, and house cusps for a given date/time and location.
#     Used for both natal and transit calculations.
#     """
#     time_format_str = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
#     try:
#         dt = datetime.strptime(f"{date_str} {time_str}", time_format_str)
#     except ValueError as e:
#         print(f"Error parsing date/time: {e}. Please ensure date is (%Y-%m-%d) and time is HH:MM or HH:MM:SS.")
#         return None, None, None, None # Return None for planets, ascendant, jd_ut, cusps

#     utc_dt = dt - timedelta(hours=timezone_offset)
#     jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

#     swe.set_sid_mode(swe.SIDM_LAHIRI)
#     ayanamsa = swe.get_ayanamsa_ut(jd_ut)

#     # Calculate house cusps and ascendant (Lagna)
#     # Using 'P' for Placidus houses as a basis for cusps is common for Chalit.
#     cusps, ascmc = swe.houses(jd_ut, latitude, longitude, b'P') 
    
#     # Adjust cusps for Ayanamsa
#     sidereal_cusps = [(c - ayanamsa) % 360 for c in cusps]
#     ascendant_degree = (ascmc[0] - ayanamsa) % 360

#     planets = {}
#     sun_lon = 0 

#     # Calculate positions for traditional and outer planets
#     for planet_name, planet_id in list(traditional_planet_ids.items()) + list(outer_planet_ids.items()):
#         xx, ret = swe.calc_ut(jd_ut, planet_id)
#         sidereal_lon = (xx[0] - ayanamsa) % 360
#         is_retrograde = xx[3] < 0
        
#         # Determine the house for each planet based on the sidereal cusps
#         planet_house = find_house(sidereal_lon, sidereal_cusps)

#         planets[planet_name] = {
#             "degree": sidereal_lon,
#             "sign": get_sign(sidereal_lon),
#             "is_retrograde": is_retrograde,
#             "house": planet_house # Add house information
#         }
#         if planet_name == "Sun":
#             sun_lon = sidereal_lon

#     # Add Rahu and Ketu
#     rahu_xx, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
#     rahu_lon = (rahu_xx[0] - ayanamsa) % 360
#     ketu_lon = (rahu_lon + 180) % 360

#     # Determine houses for Rahu and Ketu
#     rahu_house = find_house(rahu_lon, sidereal_cusps)
#     ketu_house = find_house(ketu_lon, sidereal_cusps)

#     planets["Rahu"] = {"degree": rahu_lon, "sign": get_sign(rahu_lon), "is_retrograde": True, "is_combust": False, "is_exalted": False, "is_debilitated": False, "house": rahu_house}
#     planets["Ketu"] = {"degree": ketu_lon, "sign": get_sign(ketu_lon), "is_retrograde": True, "is_combust": False, "is_exalted": False, "is_debilitated": False, "house": ketu_house}


#     # Populate combustion, exaltation, debilitation for traditional planets
#     for planet_name, data in planets.items():
#         if planet_name != "Sun" and planet_name in COMBUSTION_ORBS:
#             orb = COMBUSTION_ORBS[planet_name]
#             angular_distance = abs(data["degree"] - sun_lon)
#             if angular_distance > 180:
#                 angular_distance = 360 - angular_distance
            
#             is_combust = angular_distance < orb
#             planets[planet_name]["is_combust"] = is_combust
#         elif planet_name not in ["Sun", "Rahu", "Ketu"]:
#              planets[planet_name]["is_combust"] = False

#         if planet_name in traditional_planet_ids:
#             current_sign = data["sign"]
            
#             is_exalted = False
#             if planet_name in EXALTATION:
#                 ex_sign, ex_deg_approx = EXALTATION[planet_name]
#                 if current_sign == ex_sign:
#                     is_exalted = True
#             planets[planet_name]["is_exalted"] = is_exalted

#             is_debilitated = False
#             if planet_name in DEBILITATION:
#                 deb_sign, deb_deg_approx = DEBILITATION[planet_name]
#                 if current_sign == deb_sign:
#                     is_debilitated = True
#             planets[planet_name]["is_debilitated"] = is_debilitated
#         else:
#             planets[planet_name]["is_exalted"] = False
#             planets[planet_name]["is_debilitated"] = False

#     return planets, {"degree": ascendant_degree, "sign": get_sign(ascendant_degree)}, jd_ut, sidereal_cusps


# def calculate_rasi_chart(name, birth_date, birth_time, location_str, timezone_offset):
#     clean_location = location_str.strip().replace("'", "")
#     latitude, longitude = get_coords(clean_location)

#     if latitude is None or longitude is None:
#         print(f"\nFATAL ERROR: Could not find coordinates for '{clean_location}'.")
#         return None

#     planets, ascendant, _, cusps = calculate_planets_and_ascendant(birth_date, birth_time, latitude, longitude, timezone_offset)
#     if planets is None: return None

#     return {
#         "name": name,
#         "birthDate": birth_date,
#         "birthTime": birth_time,
#         "location": clean_location,
#         "latitude": latitude,
#         "longitude": longitude,
#         "ascendant": ascendant,
#         "planets": planets,
#         "cusps": cusps, # Store cusps in the Rasi chart for Chalit calculations
#         "chart_type_specific": "Rasi (Lagna) Chart"
#     }

# def calculate_moon_chart(rasi_chart):
#     moon_sign = rasi_chart['planets']['Moon']['sign']
#     moon_chart_planets = {}
#     moon_sign_index = ZODIAC_SIGNS.index(moon_sign)

#     for planet, data in rasi_chart['planets'].items():
#         original_sign_index = ZODIAC_SIGNS.index(data['sign'])
#         # Calculate house relative to Moon's sign (which is the new ascendant)
#         house_from_moon_lagna = (original_sign_index - moon_sign_index + 12) % 12 + 1

#         moon_chart_planets[planet] = {
#             "degree": data["degree"],
#             "sign": data["sign"],
#             "is_retrograde": data.get("is_retrograde", False),
#             "is_combust": data.get("is_combust", False),
#             "is_exalted": data.get("is_exalted", False),
#             "is_debilitated": data.get("is_debilitated", False),
#             "house": house_from_moon_lagna # House relative to Moon sign
#         }
#     return {
#         "name": rasi_chart["name"],
#         "ascendant": {"sign": moon_sign, "degree": rasi_chart["planets"]["Moon"]["degree"], "house": 1}, 
#         "planets": moon_chart_planets,
#         "chart_type_specific": "Moon Chart" 
#     }

# def calculate_navamsha_chart(rasi_chart):
#     navamsha_planets = {}

#     def get_navamsha_sign(longitude):
#         sign_index = int(longitude // 30)
#         degree_in_sign = longitude % 30
#         navamsha_number = int(degree_in_sign // (30 / 9))

#         # Rules for Navamsha sign calculation based on Rashi (sign) type
#         if sign_index % 3 == 0: # Movable (Aries, Cancer, Libra, Capricorn)
#             start_navamsha_sign_index = sign_index
#         elif sign_index % 3 == 1: # Fixed (Taurus, Leo, Scorpio, Aquarius)
#             start_navamsha_sign_index = (sign_index + 8) % 12 # 9th from itself
#         else: # Dual (Gemini, Virgo, Sagittarius, Pisces)
#             start_navamsha_sign_index = (sign_index + 4) % 12 # 5th from itself

#         final_navamsha_sign_index = (start_navamsha_sign_index + navamsha_number) % 12
#         return ZODIAC_SIGNS[final_navamsha_sign_index]

#     navamsha_asc_sign = get_navamsha_sign(rasi_chart["ascendant"]["degree"])
#     navamsha_asc_index = ZODIAC_SIGNS.index(navamsha_asc_sign)

#     for planet_name, data in rasi_chart["planets"].items():
#         navamsha_sign = get_navamsha_sign(data["degree"])
#         planet_navamsha_sign_index = ZODIAC_SIGNS.index(navamsha_sign)

#         # Calculate house relative to Navamsha Lagna
#         navamsha_house = (planet_navamsha_sign_index - navamsha_asc_index + 12) % 12 + 1

#         navamsha_planets[planet_name] = {
#             "sign": navamsha_sign,
#             "degree": data["degree"], # Keep Rasi degree, but sign is Navamsha
#             "is_retrograde": data.get("is_retrograde", False),
#             "is_combust": data.get("is_combust", False),
#             "is_exalted": data.get("is_exalted", False),
#             "is_debilitated": data.get("is_debilitated", False),
#             "house": navamsha_house # House relative to D9 Lagna
#         }

#     return {
#         "name": rasi_chart["name"],
#         "ascendant": {"sign": navamsha_asc_sign, "degree": rasi_chart["ascendant"]["degree"], "house": 1},
#         "planets": navamsha_planets,
#         "chart_type_specific": "Navamsha"
#     }

# def calculate_chalit_chart(rasi_chart):
#     """
#     Calculates the Chalit (Bhava) chart based on the Rasi chart and house cusps.
#     A planet is considered to be in the house where its longitude falls between the cusp of that house
#     and the cusp of the next house.
#     """
#     chalit_planets = {}
    
#     if 'cusps' not in rasi_chart or not rasi_chart['cusps']:
#         print("Error: Rasi chart does not contain house cusps for Chalit calculation.")
#         return None

#     # The Chalit Lagna (1st house) is the Rasi Lagna, but its house is based on the cusp.
#     chalit_ascendant_sign = rasi_chart['ascendant']['sign']
#     chalit_ascendant_degree = rasi_chart['ascendant']['degree']
    
#     # The actual house cusps define the "houses" in Chalit
#     cusps = rasi_chart['cusps']

#     for planet_name, rasi_data in rasi_chart['planets'].items():
#         planet_degree = rasi_data['degree']
        
#         # Find the house for the planet in the Chalit chart
#         chalit_house = find_house(planet_degree, cusps)

#         chalit_planets[planet_name] = {
#             "degree": planet_degree,
#             "sign": get_sign(planet_degree), # Sign remains Rasi sign
#             "is_retrograde": rasi_data.get("is_retrograde", False),
#             "is_combust": rasi_data.get("is_combust", False),
#             "is_exalted": rasi_data.get("is_exalted", False),
#             "is_debilitated": rasi_data.get("is_debilitated", False),
#             "house": chalit_house # This is the crucial Chalit house placement
#         }
    
#     # We need to explicitly determine the sign of each Chalit house for drawing.
#     # The Chalit house sign is simply the sign where the house cusp falls.
#     # The Lagna sign in Chalit is the sign of the 1st house cusp.
#     chalit_lagna_sign_for_drawing = get_sign(cusps[0])

#     return {
#         "name": rasi_chart["name"],
#         "ascendant": {"sign": chalit_lagna_sign_for_drawing, "degree": chalit_ascendant_degree, "house": 1},
#         "planets": chalit_planets,
#         "chart_type_specific": "Chalit",
#         "cusps": cusps # Keep cusps if needed for future enhancements
#     }


# def get_atmakaraka_info(rasi_chart):
#     karaka_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
#     max_degree_in_sign = -1
#     atmakaraka = None

#     for planet in karaka_planets:
#         if planet not in rasi_chart["planets"]: continue

#         # Degree in sign for normal planets
#         degree_in_sign = rasi_chart["planets"][planet]["degree"] % 30
        
#         # For Rahu, consider 30 - degree_in_sign
#         if planet == "Rahu":
#             degree_in_sign = (30 - degree_in_sign) if degree_in_sign != 0 else 0 # Avoid 30 if exact start of sign

#         if degree_in_sign > max_degree_in_sign:
#             max_degree_in_sign = degree_in_sign
#             atmakaraka = planet
#     return atmakaraka, max_degree_in_sign

# def create_reoriented_chart(person_name, planets_data_source, new_ascendant_sign, chart_type_label):
#     """
#     Creates a new chart dictionary for display by setting a new ascendant.
#     Crucially, it uses the 'planets_data_source' directly for planet positions.
#     'planets_data_source' should be either rasi_chart['planets'] or navamsha_chart['planets'].
#     """
    
#     reoriented_planets = {}
#     new_ascendant_sign_index = ZODIAC_SIGNS.index(new_ascendant_sign)

#     for planet_name, data in planets_data_source.items():
#         original_sign_index = ZODIAC_SIGNS.index(data['sign'])
        
#         # Calculate the house relative to the new ascendant
#         reoriented_house = (original_sign_index - new_ascendant_sign_index + 12) % 12 + 1
        
#         reoriented_planets[planet_name] = data.copy() # Copy all existing data
#         reoriented_planets[planet_name]["house"] = reoriented_house # Add new house information
#         # The sign remains the original sign for these re-oriented charts
#         # Only the 'house' attribute changes based on the new reference.

#     return {
#         "name": person_name, 
#         "ascendant": {"sign": new_ascendant_sign, "degree": 0.0, "house": 1}, # Degree 0.0 is symbolic for a re-oriented lagna, house is always 1
#         "planets": reoriented_planets, 
#         "chart_type_specific": chart_type_label, # For drawing function to know context
#     }

# def check_vargottama(rasi_chart, navamsha_chart):
#     vargottama_planets = []
#     for planet_name in traditional_planet_ids.keys():
#         if planet_name in rasi_chart["planets"] and planet_name in navamsha_chart["planets"]:
#             rasi_sign = rasi_chart["planets"][planet_name]["sign"]
#             navamsha_sign = navamsha_chart["planets"][planet_name]["sign"]
#             if rasi_sign == navamsha_sign:
#                 vargottama_planets.append(planet_name)
#     return vargottama_planets


# def create_transit_chart(natal_chart, transit_planets, transit_ascendant, chart_type):
#     """
#     Generates a transit chart relative to Natal Lagna or Natal Moon.
#     chart_type should be 'Lagna' or 'Moon'.
#     """
#     transit_ascendant_sign = None
#     natal_reference_sign_index = None

#     if chart_type == 'Lagna':
#         transit_ascendant_sign = natal_chart['ascendant']['sign']
#         natal_reference_sign_index = ZODIAC_SIGNS.index(natal_chart['ascendant']['sign'])
#     elif chart_type == 'Moon':
#         transit_ascendant_sign = natal_chart['planets']['Moon']['sign']
#         natal_reference_sign_index = ZODIAC_SIGNS.index(natal_chart['planets']['Moon']['sign'])
#     else:
#         raise ValueError("chart_type must be 'Lagna' or 'Moon'")

#     transit_chart_planets = {}
#     for planet_name, transit_data in transit_planets.items():
#         transit_sign_index = ZODIAC_SIGNS.index(transit_data["sign"])
        
#         # Calculate the house position relative to the natal reference sign
#         house_from_reference = (transit_sign_index - natal_reference_sign_index + 12) % 12 + 1
        
#         transit_chart_planets[planet_name] = {
#             "degree": transit_data["degree"],
#             "sign": transit_data["sign"], # This is the actual transit sign
#             "is_retrograde": transit_data.get("is_retrograde", False),
#             "is_combust": transit_data.get("is_combust", False),
#             "is_exalted": transit_data.get("is_exalted", False),
#             "is_debilitated": transit_data.get("is_debilitated", False),
#             "house": house_from_reference # Store the house for display
#         }

#     return {
#         "name": natal_chart["name"],
#         "ascendant": {"sign": transit_ascendant_sign, "degree": 0.0, "house": 1}, # The reference sign acts as ascendant
#         "planets": transit_chart_planets,
#         "chart_type_specific": f"Transit from {chart_type}" # To differentiate for display logic
#     }


# def print_chart_details(chart, title):
#     print("\n" + "=" * 60)
#     print(f"📜 {title} for {chart['name']} 📜")
#     print("=" * 60)

#     # Print Lagna (Ascendant) details first
#     lagna_sign = chart['ascendant']['sign']
#     lagna_degree_str = "" 

#     # Only show precise degree for Rasi Lagna, others are re-oriented or transit references
#     if chart.get('chart_type_specific') == "Rasi (Lagna) Chart" and 'degree' in chart['ascendant'] and chart['ascendant']['degree'] != 0.0:
#         lagna_degree = chart['ascendant']['degree']
#         d, m, s = decimal_to_dms(lagna_degree)
#         lagna_degree_str = f"{d:02d},{m:02d},{s:02d}"
#     else: # For re-oriented/transit charts, degree is symbolic (start of house)
#             lagna_degree_str = "00,00,00" # Indicating the beginning of the re-oriented first house
        
#     print(f"{'Lagna (La)':<10} | {lagna_degree_str:<15} | {lagna_sign:<12} | {'House':<6} | {'Status':<15}")
#     print("-" * 60)

#     print(f"{'Planet':<10} | {'Degree (D,M,S)':<15} | {'Sign':<12} | {'House':<6} | {'Status':<15}")
#     print("-" * 60)
    
#     planets_for_display = []
#     for planet_name in PLANET_NAMES:
#         if planet_name in chart["planets"]:
#             planets_for_display.append((planet_name, chart["planets"][planet_name]))
    
#     # Sort by house first, then by degree within the house for better readability
#     # Ensure 'house' exists and is an integer for sorting
#     planets_for_display.sort(key=lambda item: (item[1].get('house', 0) if isinstance(item[1].get('house'), int) else 0, item[1]['degree'] % 30))

#     for planet_name, data in planets_for_display:
#         degree = data.get("degree", 0.0)
#         d, m, s = decimal_to_dms(degree)
#         degree_str = f"{d:02d},{m:02d},{s:02d}"
        
#         sign = data["sign"]
        
#         # Get house, default to '-' if not present or not an integer
#         house_num = data.get("house", "-")
#         if not isinstance(house_num, int):
#             house_num = "-" # Ensure it's a string if not an integer
        
#         status_indicators = []
#         if data.get("is_retrograde"):
#             status_indicators.append(STATUS_SYMBOLS["retrograde"])
#         if data.get("is_combust"):
#             status_indicators.append(STATUS_SYMBOLS["combust"])
#         if data.get("is_exalted"):
#             status_indicators.append(STATUS_SYMBOLS["exalted"])
#         if data.get("is_debilitated"):
#             status_indicators.append(STATUS_SYMBOLS["debilitated"])
#         if data.get("is_vargottama"):
#             status_indicators.append(STATUS_SYMBOLS["vargottama"])
        
#         status_str = " ".join(status_indicators) if status_indicators else ""
        
#         print(f"{PLANET_ABBR.get(planet_name, planet_name):<10} | {degree_str:<15} | {sign:<12} | {str(house_num):<6} | {status_str:<15}") # Explicitly cast house_num to str
#     print("-" * 60)


# def draw_north_indian(chart, title):
#     win = tk.Toplevel()
#     win.title(title)
#     canvas = tk.Canvas(win, width=450, height=450, bg="white")
#     canvas.pack(padx=10, pady=10)

#     center_x, center_y = 225, 225
#     half_side = 200

#     # Draw the main diamond (outer boundary)
#     canvas.create_polygon(
#         center_x, center_y - half_side,
#         center_x + half_side, center_y,
#         center_x, center_y + half_side,
#         center_x - half_side, center_y,
#         outline="black", fill="#f7f7f7", width=2
#     )

#     # Draw internal lines for houses
#     canvas.create_line(center_x - half_side, center_y, center_x + half_side, center_y, width=1) # Horizontal
#     canvas.create_line(center_x, center_y - half_side, center_x, center_y + half_side, width=1) # Vertical
    
#     # Diagonal lines for the inner diamond
#     canvas.create_line(center_x - half_side / 2, center_y - half_side / 2, center_x + half_side / 2, center_y + half_side / 2, width=1)
#     canvas.create_line(center_x + half_side / 2, center_y - half_side / 2, center_x - half_side / 2, center_y + half_side / 2, width=1)
    
#     # Additional lines to form all 12 houses (rectangles and triangles)
#     canvas.create_line(center_x - half_side, center_y, center_x, center_y + half_side, width=1) # Bottom-left diagonal
#     canvas.create_line(center_x + half_side, center_y, center_x, center_y + half_side, width=1) # Bottom-right diagonal
#     canvas.create_line(center_x - half_side, center_y, center_x, center_y - half_side, width=1) # Top-left diagonal
#     canvas.create_line(center_x + half_side, center_y, center_x, center_y - half_side, width=1) # Top-right diagonal


#     # Coordinates for placing text for each house (adjusted for North Indian style)
#     house_display_coords = {
#         1: (center_x, center_y - half_side + 50), # Top diamond (1st House)
#         2: (center_x + half_side - 50, center_y - 70), # Top-right triangle (2nd House)
#         3: (center_x + half_side - 50, center_y + 70), # Bottom-right triangle (3rd House)
#         4: (center_x, center_y + half_side - 50), # Bottom diamond (4th House)
#         5: (center_x - half_side + 50, center_y + 70), # Bottom-left triangle (5th House)
#         6: (center_x - half_side + 50, center_y - 70), # Top-left triangle (6th House)

#         # Inner houses for 7-12 (clockwise)
#         7: (center_x + 70, center_y - 20), # Right-center rectangle (7th house)
#         8: (center_x + 20, center_y - 70), # Top-center rectangle (8th house)
#         9: (center_x - 20, center_y - 70), # Top-left inner rectangle (9th house)
#         10: (center_x - 70, center_y - 20), # Left-center rectangle (10th house)
#         11: (center_x - 20, center_y + 70), # Bottom-left inner rectangle (11th house)
#         12: (center_x + 20, center_y + 70) # Bottom-right inner rectangle (12th house)
#     }

#     # Define offsets for sign number and planet text within each house
#     sign_num_offset_x = -40
#     sign_num_offset_y = -60
#     planet_text_start_y_offset = -30
#     line_height = 15

#     # Determine the "starting sign" for the 1st house in the drawing based on the chart's ascendant
#     visual_lagna_sign_index = ZODIAC_SIGNS.index(chart['ascendant']['sign'])

#     # Map actual zodiac sign indices to visual house numbers (1-12)
#     # The sign at the chart's ascendant will be in visual house 1.
#     # The sign after it will be in visual house 2, and so on, clockwise.
#     sign_index_to_visual_house_map = {}
#     for i in range(12):
#         actual_sign_index = (visual_lagna_sign_index + i) % 12
#         visual_house_number = i + 1 
#         sign_index_to_visual_house_map[actual_sign_index] = visual_house_number

#     houses_content = {i: [] for i in range(1, 13)}

#     # Add Lagna indicator to the first visual house (which holds the Ascendant sign)
#     houses_content[1].append("La") 

#     for planet_name in PLANET_NAMES:
#         if planet_name in chart['planets']:
#             data = chart['planets'][planet_name]
            
#             visual_house_number_for_planet = None
#             if chart.get('chart_type_specific') == 'Chalit':
#                 # For Chalit, the planet is drawn in its *Chalit house*
#                 visual_house_number_for_planet = data.get("house")
#                 if visual_house_number_for_planet is None: # Fallback if house not calculated for some reason
#                     visual_house_number_for_planet = sign_index_to_visual_house_map[ZODIAC_SIGNS.index(data['sign'])]
#             else:
#                 # For Rasi, Moon, Navamsha, Swamsha, Karakamsha, Transit, it's drawn based on its *sign relative to the chart's Lagna*
#                 planet_sign_index = ZODIAC_SIGNS.index(data['sign'])
#                 visual_house_number_for_planet = sign_index_to_visual_house_map[planet_sign_index]

#             if visual_house_number_for_planet is None: continue # Skip if house couldn't be determined

#             d, m, s = decimal_to_dms(data['degree'])
#             planet_degree_formatted = f"{d:02d},{m:02d}"
            
#             planet_display = f"{planet_degree_formatted}{PLANET_ABBR[planet_name]}"
            
#             # Add status indicators using symbols
#             if data.get("is_retrograde"):
#                 planet_display += STATUS_SYMBOLS["retrograde"]
#             if data.get("is_combust"):
#                 planet_display += STATUS_SYMBOLS["combust"]
#             if data.get("is_exalted"):
#                 planet_display += STATUS_SYMBOLS["exalted"]
#             if data.get("is_debilitated"):
#                 planet_display += STATUS_SYMBOLS["debilitated"]
#             if data.get("is_vargottama"):
#                 planet_display += STATUS_SYMBOLS["vargottama"]

#             houses_content[visual_house_number_for_planet].append(planet_display)

#     for visual_house_num in range(1, 13):
#         # Determine the actual sign number (1-12) for the current visual house
#         # This is based on the sequence of signs starting from the chart's Lagna
#         actual_sign_index_for_house = (visual_lagna_sign_index + (visual_house_num - 1)) % 12
#         actual_sign_number_for_house = actual_sign_index_for_house + 1

#         x, y = house_display_coords[visual_house_num]

#         # Draw the sign number for the house
#         canvas.create_text(x + sign_num_offset_x, y + sign_num_offset_y, text=str(actual_sign_number_for_house), font=("Arial", 10, "bold"), fill="black", anchor="nw")
        
#         # REMOVED: The line to draw "H{visual_house_num}"
#         # canvas.create_text(x + sign_num_offset_x + 25, y + sign_num_offset_y, text=f"H{visual_house_num}", font=("Arial", 8), fill="gray", anchor="nw")

#         current_y_offset = y + planet_text_start_y_offset
        
#         # Sorting key to put Lagna first, then planets by degree
#         def sort_key(s):
#             if s == "La": return (0, "")
#             try:
#                 # Extract degree if present (e.g., "05,20Su")
#                 if ',' in s:
#                     deg_str = s.split(',')[0]
#                     if deg_str.isdigit():
#                         return (1, int(deg_str))
#                 return (2, s) # Fallback for malformed or other strings
#             except (ValueError, IndexError):
#                 return (2, s) # If parsing fails, put it at the end

#         sorted_elements_in_house = sorted(houses_content[visual_house_num], key=sort_key)

#         for p_str in sorted_elements_in_house:
#             text_color = "red" if p_str == "La" else "blue"
#             font_style = ("Arial", 10, "bold") if p_str == "La" else ("Arial", 9)
#             canvas.create_text(x + sign_num_offset_x, current_y_offset, text=p_str, font=font_style, fill=text_color, anchor="nw")
#             current_y_offset += line_height

#     win.lift()


# # --- Main Execution Block ---
# if __name__ == "__main__":
#     print("--- Vedic Astrology Chart Generator ---")
#     name = input("Enter Full Name: ")
#     birth_date = input("Enter Birth Date (YYYY-MM-DD): ")
    
#     birth_time = input("Enter Birth Time (HH:MM or HH:MM:SS in 24-hr format): ")
    
#     birth_location = input("Enter Birth Location (e.g., 'Delhi, India'): ")

#     # Get birth coordinates and timezone offset
#     lat_birth, lon_birth = get_coords(birth_location)
#     if lat_birth is None or lon_birth is None:
#         print("Could not determine birth coordinates. Please try a more specific location name.")
#         exit()
#     else:
#         print(f"\nGeocoded Birth Location: Latitude = {lat_birth:.4f}, Longitude = {lon_birth:.4f}")

#     utc_offset_birth = get_timezone_offset(lat_birth, lon_birth, birth_date, birth_time)
#     if utc_offset_birth is None:
#         exit()

#     # Calculate Natal (Rasi) Chart
#     natal_planets, natal_ascendant, natal_jd_ut, natal_cusps = calculate_planets_and_ascendant(birth_date, birth_time, lat_birth, lon_birth, utc_offset_birth)
#     if natal_planets is None:
#         exit()

#     rasi_chart = {
#         "name": name,
#         "birthDate": birth_date,
#         "birthTime": birth_time,
#         "location": birth_location,
#         "latitude": lat_birth,
#         "longitude": lon_birth,
#         "ascendant": natal_ascendant,
#         "planets": natal_planets,
#         "cusps": natal_cusps, # Store cusps in the Rasi chart for Chalit calculations
#         "chart_type_specific": "Rasi (Lagna) Chart"
#     }

#     moon_chart = calculate_moon_chart(rasi_chart)
#     navamsha_chart = calculate_navamsha_chart(rasi_chart)
#     chalit_chart = calculate_chalit_chart(rasi_chart) # Calculate Chalit Chart
    
#     atmakaraka_planet, _ = get_atmakaraka_info(rasi_chart)
#     karakamsha_lagna_sign = None
#     if atmakaraka_planet and atmakaraka_planet in navamsha_chart["planets"]:
#         karakamsha_lagna_sign = navamsha_chart["planets"][atmakaraka_planet]["sign"]

#     # Create Swamsha Chart (Rasi re-oriented with Karakamsha Lagna as Ascendant)
#     swamsha_chart = None
#     if karakamsha_lagna_sign:
#         # Pass rasi_chart['planets'] as the source for planet data
#         swamsha_chart = create_reoriented_chart(name, rasi_chart['planets'], karakamsha_lagna_sign, "Swamsha")
#         if swamsha_chart:
#             swamsha_chart["atmakaraka"] = atmakaraka_planet

#     # Create Karakamsha Chart (Navamsha re-oriented with Karakamsha Lagna as Ascendant)
#     karakamsha_chart = None
#     if karakamsha_lagna_sign:
#         # Pass navamsha_chart['planets'] as the source for planet data
#         karakamsha_chart = create_reoriented_chart(name, navamsha_chart['planets'], karakamsha_lagna_sign, "Karakamsha")
#         if karakamsha_chart:
#             karakamsha_chart["atmakaraka"] = atmakaraka_planet


#     vargottama_planets_list = check_vargottama(rasi_chart, navamsha_chart)
#     for planet_name in vargottama_planets_list:
#         if planet_name in rasi_chart["planets"]:
#             rasi_chart["planets"][planet_name]["is_vargottama"] = True
#         if planet_name in navamsha_chart["planets"]:
#             navamsha_chart["planets"][planet_name]["is_vargottama"] = True

#     # --- Transit Chart Calculations (Automated with options to override) ---
#     print("\n--- Transit Chart Input (Press Enter for default current values) ---")
    
#     # Use current time as default
#     now = datetime.now()
#     default_transit_date = now.strftime("%Y-%m-%d")
#     default_transit_time = now.strftime("%H:%M:%S")

#     transit_date_input = input(f"Enter Transit Date (YYYY-MM-DD) [Default: {default_transit_date}]: ")
#     transit_time_input = input(f"Enter Transit Time (HH:MM or HH:MM:SS) [Default: {default_transit_time}]: ")
#     transit_location_input = input(f"Enter Transit Location (e.g., 'Seoul, South Korea') [Default: {birth_location}]: ")

#     transit_date = transit_date_input if transit_date_input else default_transit_date
#     transit_time = transit_time_input if transit_time_input else default_transit_time
#     transit_location = transit_location_input if transit_location_input else birth_location

#     transit_lat, transit_lon = get_coords(transit_location)
#     if transit_lat is None or transit_lon is None:
#         print(f"Could not determine transit coordinates for '{transit_location}'. Using birth location ({birth_location}) for transit calculations.")
#         transit_lat, transit_lon = lat_birth, lon_birth
#         transit_location = birth_location # Revert to birth location if new location fails
#     else:
#         print(f"Geocoded Transit Location: Latitude = {transit_lat:.4f}, Longitude = {transit_lon:.4f}")

#     utc_offset_transit = get_timezone_offset(transit_lat, transit_lon, transit_date, transit_time)
#     if utc_offset_transit is None:
#         print("Could not determine transit timezone. Skipping transit charts.")
#         transit_planets = None
#         transit_ascendant = None
#     else:
#         transit_planets, transit_ascendant, transit_jd_ut, _ = calculate_planets_and_ascendant( # _ for cusps as we don't need them for the transit chart relative to natal lagna/moon
#             transit_date, transit_time, transit_lat, transit_lon, utc_offset_transit
#         )
    
#     transit_lagna_chart = None
#     transit_moon_chart = None
#     if transit_planets and transit_ascendant:
#         transit_lagna_chart = create_transit_chart(rasi_chart, transit_planets, transit_ascendant, 'Lagna')
#         transit_moon_chart = create_transit_chart(rasi_chart, transit_planets, transit_ascendant, 'Moon')


#     # --- Print All Chart Details ---
#     print_chart_details(rasi_chart, "Rasi (Lagna) Chart - Natal")
#     print_chart_details(moon_chart, "Moon Chart (Chandra Lagna) - Natal")
#     print_chart_details(chalit_chart, "Chalit (Bhava) Chart - Natal") # Print Chalit Chart
#     print_chart_details(navamsha_chart, "Navamsha (D9) Chart - Natal")
    
#     if swamsha_chart:
#         print_chart_details(swamsha_chart, f"Swamsha Chart (AK: {swamsha_chart['atmakaraka']}) - Natal Re-oriented")
#     if karakamsha_chart:
#         print_chart_details(karakamsha_chart, f"Karakamsha Chart (AK in D9: {karakamsha_chart['atmakaraka']}) - Navamsha Re-oriented")

#     # Print Transit Charts
#     if transit_lagna_chart:
#         print_chart_details(transit_lagna_chart, f"Transit Chart from Natal Lagna ({transit_date} {transit_time} at {transit_location})")
#     if transit_moon_chart:
#         print_chart_details(transit_moon_chart, f"Transit Chart from Natal Moon ({transit_date} {transit_time} at {transit_location})")

#     # --- Start GUI for chart visualization ---
#     root = tk.Tk()
#     root.title("Kundali Charts")
#     root.geometry("500x650") # Adjusted height for more buttons

#     label = tk.Label(root, text=f"Charts for {rasi_chart['name']}", font=("Arial", 14, "bold"))
#     label.pack(pady=10)

#     # Natal Charts
#     tk.Label(root, text="--- Natal Charts ---", font=("Arial", 12, "underline")).pack(pady=5)
#     tk.Button(root, text="Show Rasi (Lagna) Chart", 
#               command=lambda: draw_north_indian(rasi_chart, f"Rasi (Lagna) Chart - {name}"), 
#               width=40, height=2).pack(pady=2)
    
#     tk.Button(root, text="Show Moon Chart (Chandra Lagna)", 
#               command=lambda: draw_north_indian(moon_chart, f"Moon Chart - {name}"), 
#               width=40, height=2).pack(pady=2)

#     tk.Button(root, text="Show Chalit (Bhava) Chart", # Chalit Chart Button
#               command=lambda: draw_north_indian(chalit_chart, f"Chalit (Bhava) Chart - {name}"), 
#               width=40, height=2).pack(pady=2)
    
#     tk.Button(root, text="Show Navamsha (D9) Chart", 
#               command=lambda: draw_north_indian(navamsha_chart, f"Navamsha (D9) Chart - {name}"), 
#               width=40, height=2).pack(pady=2)
    
#     if swamsha_chart:
#         tk.Button(root, text=f"Show Swamsha Chart (AK: {swamsha_chart['atmakaraka']})", 
#                   command=lambda: draw_north_indian(swamsha_chart, f"Swamsha Chart - {name}"), 
#                   width=40, height=2).pack(pady=2)

#     if karakamsha_chart:
#         tk.Button(root, text=f"Show Karakamsha Chart (AK in D9: {karakamsha_chart['atmakaraka']})", 
#                   command=lambda: draw_north_indian(karakamsha_chart, f"Karakamsha Chart - {name}"), 
#                   width=40, height=2).pack(pady=2)

#     # Transit Charts
#     if transit_lagna_chart and transit_moon_chart:
#         tk.Label(root, text=f"--- Transit Charts ({transit_date} {transit_time} at {transit_location}) ---", font=("Arial", 12, "underline")).pack(pady=5)
#         tk.Button(root, text=f"Show Transit Chart from Natal Lagna", 
#                   command=lambda: draw_north_indian(transit_lagna_chart, f"Transit from Lagna - {name} ({transit_date})"), 
#                   width=40, height=2).pack(pady=2)
#         tk.Button(root, text=f"Show Transit Chart from Natal Moon", 
#                   command=lambda: draw_north_indian(transit_moon_chart, f"Transit from Moon - {name} ({transit_date})"), 
#                   width=40, height=2).pack(pady=2)
#     else:
#         tk.Label(root, text="Transit charts could not be calculated.", fg="red").pack(pady=5)


#     root.mainloop()



import swisseph as swe
from datetime import datetime, timedelta
import tkinter as tk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import math
from lal_kitab_predictor import LalKitabPredictor

# --- Setup and Constants ---
try:
    # Ensure this path is correct for your system.
    # For Windows, it might look like 'C:/swisseph/ephe'
    # For Linux/macOS, it's often '/usr/share/ephe'
    swe.set_ephe_path('/usr/share/ephe')
except swe.Error:
    print("Error: Swiss Ephemeris path not found. Please set the correct path in the script.")
    print("Download ephemeris files from http://www.astro.com/swisseph/swoeph.zip")
    print("Extract them and point swe.set_ephe_path() to the directory containing 'sepha.se1', etc.")
    exit()

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_NAMES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]
PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mercury": "Me", "Venus": "Ve",
    "Mars": "Ma", "Jupiter": "Ju", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
    "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl"
}

# Define traditional and outer planet IDs globally
traditional_planet_ids = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN
}

outer_planet_ids = {
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
}

# Vedic Astrology Specific Data
# Exaltation signs and degrees (approximate)
EXALTATION = {
    "Sun": ("Aries", 10),
    "Moon": ("Taurus", 3),
    "Mars": ("Capricorn", 28),
    "Mercury": ("Virgo", 15), # Also its Moolatrikona
    "Jupiter": ("Cancer", 5),
    "Venus": ("Pisces", 27),
    "Saturn": ("Libra", 20),
}

# Debilitation signs and degrees
DEBILITATION = {
    "Sun": ("Libra", 10),
    "Moon": ("Scorpio", 3),
    "Mars": ("Cancer", 28),
    "Mercury": ("Pisces", 15),
    "Jupiter": ("Capricorn", 5),
    "Venus": ("Virgo", 27),
    "Saturn": ("Aries", 20),
}

# Combustion Orbs (approximate, degrees from Sun)
COMBUSTION_ORBS = {
    "Moon": 12,
    "Mercury": 14, # 12 if direct, 14 if retrograde
    "Venus": 10,  # 8 if direct, 10 if retrograde
    "Mars": 17,
    "Jupiter": 11,
    "Saturn": 15,
}

# New: Define status symbols based on the image
STATUS_SYMBOLS = {
    "retrograde": "✶",
    "combust": "ˆ",
    "vargottama": "¤",
    "exalted": "†",
    "debilitated": "↓"
}


# --- Helper for Degree, Minute, Second (DMS) Conversion ---
def decimal_to_dms(decimal_degree):
    """Converts a decimal degree to (degrees, minutes, seconds) tuple within its sign."""
    degree_in_sign = decimal_degree % 30 # Get degree within the current sign
    
    degrees = int(degree_in_sign)
    minutes_decimal = (degree_in_sign - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = int((minutes_decimal - minutes) * 60)
    return degrees, minutes, seconds

# --- Core Calculation Functions ---

def get_coords(location_name):
    """Geocodes a location name to get latitude and longitude."""
    try:
        geolocator = Nominatim(user_agent="kundali_app_v3")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None

def get_timezone_offset(lat, lon, date_str, time_str):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=lat, lng=lon)
    if not timezone_name:
        print("Could not detect timezone. Exiting.")
        return None
    local_tz = pytz.timezone(timezone_name)
    
    try:
        if len(time_str.split(':')) == 3: # HH:MM:SS format
            naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        else: # HH:MM format, default seconds to 00
            naive_dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print(f"Invalid time format for {date_str} {time_str}. Please use HH:MM or HH:MM:SS.")
        return None

    local_dt = local_tz.localize(naive_dt)
    return (local_dt.utcoffset().total_seconds()) / 3600.0

def get_sign(degree):
    return ZODIAC_SIGNS[int(degree // 30)]

def find_house(degree, cusps):
    """
    Determines the house number (1-12) for a given degree based on house cusps.
    Assumes cusps are sorted and represent the start of each house.
    """
    degree = degree % 360

    for i in range(12):
        house_start_cusp = cusps[i]
        house_end_cusp = cusps[(i + 1) % 12]

        if house_start_cusp <= house_end_cusp:
            if house_start_cusp <= degree < house_end_cusp:
                return i + 1
        else: # House crosses the 0/360 degree point
            if degree >= house_start_cusp or degree < house_end_cusp:
                return i + 1
    return 1 # Fallback, should always find a house


def calculate_planets_and_ascendant(date_str, time_str, latitude, longitude, timezone_offset, is_natal_chart=False):
    """
    Calculates planetary positions, ascendant, and house cusps for a given date/time and location.
    Used for both natal and transit calculations.
    Status is only calculated if is_natal_chart is True.
    """
    time_format_str = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", time_format_str)
    except ValueError as e:
        print(f"Error parsing date/time: {e}. Please ensure date is (%Y-%m-%d) and time is HH:MM or HH:MM:SS.")
        return None, None, None, None # Return None for planets, ascendant, jd_ut, cusps

    utc_dt = dt - timedelta(hours=timezone_offset)
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)

    # Calculate house cusps and ascendant (Lagna)
    cusps, ascmc = swe.houses(jd_ut, latitude, longitude, b'P') 
    
    # Adjust cusps for Ayanamsa
    sidereal_cusps = [(c - ayanamsa) % 360 for c in cusps]
    ascendant_degree = (ascmc[0] - ayanamsa) % 360

    planets = {}
    sun_lon = 0 

    # Calculate positions for traditional and outer planets
    for planet_name, planet_id in list(traditional_planet_ids.items()) + list(outer_planet_ids.items()):
        xx, ret = swe.calc_ut(jd_ut, planet_id)
        sidereal_lon = (xx[0] - ayanamsa) % 360
        is_retrograde = xx[3] < 0
        
        planet_house = find_house(sidereal_lon, sidereal_cusps)

        planets[planet_name] = {
            "degree": sidereal_lon,
            "sign": get_sign(sidereal_lon),
            "house": planet_house 
        }
        # Only add status for the main Rasi/Lagna chart
        if is_natal_chart:
            planets[planet_name]["is_retrograde"] = is_retrograde
        
        if planet_name == "Sun":
            sun_lon = sidereal_lon

    # Add Rahu and Ketu
    rahu_xx, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
    rahu_lon = (rahu_xx[0] - ayanamsa) % 360
    ketu_lon = (rahu_lon + 180) % 360

    rahu_house = find_house(rahu_lon, sidereal_cusps)
    ketu_house = find_house(ketu_lon, sidereal_cusps)

    planets["Rahu"] = {"degree": rahu_lon, "sign": get_sign(rahu_lon), "house": rahu_house}
    planets["Ketu"] = {"degree": ketu_lon, "sign": get_sign(ketu_lon), "house": ketu_house}
    
    if is_natal_chart:
        planets["Rahu"].update({"is_retrograde": True, "is_combust": False, "is_exalted": False, "is_debilitated": False})
        planets["Ketu"].update({"is_retrograde": True, "is_combust": False, "is_exalted": False, "is_debilitated": False})


    # Populate status ONLY if it's the main natal chart
    if is_natal_chart:
        for planet_name, data in planets.items():
            # Combustion
            if planet_name != "Sun" and planet_name in COMBUSTION_ORBS:
                orb = COMBUSTION_ORBS[planet_name]
                angular_distance = abs(data["degree"] - sun_lon)
                if angular_distance > 180:
                    angular_distance = 360 - angular_distance
                planets[planet_name]["is_combust"] = angular_distance < orb
            elif planet_name not in ["Sun", "Rahu", "Ketu"]:
                planets[planet_name]["is_combust"] = False

            # Exaltation & Debilitation
            if planet_name in traditional_planet_ids:
                current_sign = data["sign"]
                
                is_exalted = False
                if planet_name in EXALTATION and current_sign == EXALTATION[planet_name][0]:
                    is_exalted = True
                planets[planet_name]["is_exalted"] = is_exalted

                is_debilitated = False
                if planet_name in DEBILITATION and current_sign == DEBILITATION[planet_name][0]:
                    is_debilitated = True
                planets[planet_name]["is_debilitated"] = is_debilitated
            else:
                planets[planet_name]["is_exalted"] = False
                planets[planet_name]["is_debilitated"] = False

    return planets, {"degree": ascendant_degree, "sign": get_sign(ascendant_degree)}, jd_ut, sidereal_cusps


def calculate_rasi_chart(name, birth_date, birth_time, location_str, timezone_offset):
    clean_location = location_str.strip().replace("'", "")
    latitude, longitude = get_coords(clean_location)

    if latitude is None or longitude is None:
        print(f"\nFATAL ERROR: Could not find coordinates for '{clean_location}'.")
        return None

    # Pass is_natal_chart=True to calculate status for Rasi chart
    planets, ascendant, _, cusps = calculate_planets_and_ascendant(birth_date, birth_time, latitude, longitude, timezone_offset, is_natal_chart=True)
    if planets is None: return None

    return {
        "name": name,
        "birthDate": birth_date,
        "birthTime": birth_time,
        "location": clean_location,
        "latitude": latitude,
        "longitude": longitude,
        "ascendant": ascendant,
        "planets": planets,
        "cusps": cusps,
        "chart_type_specific": "Rasi (Lagna) Chart"
    }

def calculate_moon_chart(rasi_chart):
    moon_sign = rasi_chart['planets']['Moon']['sign']
    moon_chart_planets = {}
    moon_sign_index = ZODIAC_SIGNS.index(moon_sign)

    for planet, data in rasi_chart['planets'].items():
        original_sign_index = ZODIAC_SIGNS.index(data['sign'])
        house_from_moon_lagna = (original_sign_index - moon_sign_index + 12) % 12 + 1

        # Do NOT copy status indicators
        moon_chart_planets[planet] = {
            "degree": data["degree"],
            "sign": data["sign"],
            "house": house_from_moon_lagna 
        }
    return {
        "name": rasi_chart["name"],
        "ascendant": {"sign": moon_sign, "degree": rasi_chart["planets"]["Moon"]["degree"], "house": 1}, 
        "planets": moon_chart_planets,
        "chart_type_specific": "Moon Chart" 
    }

def calculate_navamsha_chart(rasi_chart):
    navamsha_planets = {}

    def get_navamsha_sign(longitude):
        sign_index = int(longitude // 30)
        degree_in_sign = longitude % 30
        navamsha_number = int(degree_in_sign // (30 / 9))

        if sign_index % 3 == 0: 
            start_navamsha_sign_index = sign_index
        elif sign_index % 3 == 1:
            start_navamsha_sign_index = (sign_index + 8) % 12
        else:
            start_navamsha_sign_index = (sign_index + 4) % 12

        final_navamsha_sign_index = (start_navamsha_sign_index + navamsha_number) % 12
        return ZODIAC_SIGNS[final_navamsha_sign_index]

    navamsha_asc_sign = get_navamsha_sign(rasi_chart["ascendant"]["degree"])
    navamsha_asc_index = ZODIAC_SIGNS.index(navamsha_asc_sign)

    for planet_name, data in rasi_chart["planets"].items():
        navamsha_sign = get_navamsha_sign(data["degree"])
        planet_navamsha_sign_index = ZODIAC_SIGNS.index(navamsha_sign)
        navamsha_house = (planet_navamsha_sign_index - navamsha_asc_index + 12) % 12 + 1

        # Do NOT copy status indicators
        navamsha_planets[planet_name] = {
            "sign": navamsha_sign,
            "degree": data["degree"],
            "house": navamsha_house 
        }

    return {
        "name": rasi_chart["name"],
        "ascendant": {"sign": navamsha_asc_sign, "degree": rasi_chart["ascendant"]["degree"], "house": 1},
        "planets": navamsha_planets,
        "chart_type_specific": "Navamsha"
    }

def calculate_chalit_chart(rasi_chart):
    chalit_planets = {}
    
    if 'cusps' not in rasi_chart or not rasi_chart['cusps']:
        print("Error: Rasi chart does not contain house cusps for Chalit calculation.")
        return None

    chalit_ascendant_degree = rasi_chart['ascendant']['degree']
    cusps = rasi_chart['cusps']

    for planet_name, rasi_data in rasi_chart['planets'].items():
        planet_degree = rasi_data['degree']
        chalit_house = find_house(planet_degree, cusps)

        # Do NOT copy status indicators
        chalit_planets[planet_name] = {
            "degree": planet_degree,
            "sign": get_sign(planet_degree),
            "house": chalit_house 
        }
    
    chalit_lagna_sign_for_drawing = get_sign(cusps[0])

    return {
        "name": rasi_chart["name"],
        "ascendant": {"sign": chalit_lagna_sign_for_drawing, "degree": chalit_ascendant_degree, "house": 1},
        "planets": chalit_planets,
        "chart_type_specific": "Chalit",
        "cusps": cusps
    }


def get_atmakaraka_info(rasi_chart):
    karaka_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
    max_degree_in_sign = -1
    atmakaraka = None

    for planet in karaka_planets:
        if planet not in rasi_chart["planets"]: continue
        degree_in_sign = rasi_chart["planets"][planet]["degree"] % 30
        
        if planet == "Rahu":
            degree_in_sign = (30 - degree_in_sign) if degree_in_sign != 0 else 0

        if degree_in_sign > max_degree_in_sign:
            max_degree_in_sign = degree_in_sign
            atmakaraka = planet
    return atmakaraka, max_degree_in_sign

def create_reoriented_chart(person_name, planets_data_source, new_ascendant_sign, chart_type_label):
    reoriented_planets = {}
    new_ascendant_sign_index = ZODIAC_SIGNS.index(new_ascendant_sign)

    for planet_name, data in planets_data_source.items():
        original_sign_index = ZODIAC_SIGNS.index(data['sign'])
        reoriented_house = (original_sign_index - new_ascendant_sign_index + 12) % 12 + 1
        
        # Do NOT copy status indicators
        reoriented_planets[planet_name] = {
            "degree": data["degree"],
            "sign": data["sign"],
            "house": reoriented_house
        }

    return {
        "name": person_name, 
        "ascendant": {"sign": new_ascendant_sign, "degree": 0.0, "house": 1},
        "planets": reoriented_planets, 
        "chart_type_specific": chart_type_label,
    }

def check_vargottama(rasi_chart, navamsha_chart):
    vargottama_planets = []
    for planet_name in traditional_planet_ids.keys():
        if planet_name in rasi_chart["planets"] and planet_name in navamsha_chart["planets"]:
            rasi_sign = rasi_chart["planets"][planet_name]["sign"]
            navamsha_sign = navamsha_chart["planets"][planet_name]["sign"]
            if rasi_sign == navamsha_sign:
                vargottama_planets.append(planet_name)
    return vargottama_planets


def create_transit_chart(natal_chart, transit_planets, transit_ascendant, chart_type):
    transit_ascendant_sign = None
    natal_reference_sign_index = None

    if chart_type == 'Lagna':
        natal_reference_sign_index = ZODIAC_SIGNS.index(natal_chart['ascendant']['sign'])
    elif chart_type == 'Moon':
        natal_reference_sign_index = ZODIAC_SIGNS.index(natal_chart['planets']['Moon']['sign'])
    else:
        raise ValueError("chart_type must be 'Lagna' or 'Moon'")
        
    transit_ascendant_sign = ZODIAC_SIGNS[natal_reference_sign_index]

    transit_chart_planets = {}
    for planet_name, transit_data in transit_planets.items():
        transit_sign_index = ZODIAC_SIGNS.index(transit_data["sign"])
        house_from_reference = (transit_sign_index - natal_reference_sign_index + 12) % 12 + 1
        
        # Do NOT copy status indicators
        transit_chart_planets[planet_name] = {
            "degree": transit_data["degree"],
            "sign": transit_data["sign"],
            "house": house_from_reference 
        }

    return {
        "name": natal_chart["name"],
        "ascendant": {"sign": transit_ascendant_sign, "degree": 0.0, "house": 1},
        "planets": transit_chart_planets,
        "chart_type_specific": f"Transit from {chart_type}"
    }


def print_chart_details(chart, title):
    print("\n" + "=" * 60)
    print(f"📜 {title} for {chart['name']} 📜")
    print("=" * 60)

    is_rasi_chart = chart.get('chart_type_specific') == "Rasi (Lagna) Chart"

    lagna_sign = chart['ascendant']['sign']
    lagna_degree_str = "" 

    if chart.get('chart_type_specific') == "Rasi (Lagna) Chart" and 'degree' in chart['ascendant'] and chart['ascendant']['degree'] != 0.0:
        lagna_degree = chart['ascendant']['degree']
        d, m, s = decimal_to_dms(lagna_degree)
        lagna_degree_str = f"{d:02d},{m:02d},{s:02d}"
    else:
        lagna_degree_str = "00,00,00"
    
    # Define headers based on whether it's the Rasi chart
    if is_rasi_chart:
        print(f"{'Lagna (La)':<10} | {lagna_degree_str:<15} | {lagna_sign:<12} | {'Status':<15}")
        print("-" * 60)
        print(f"{'Planet':<10} | {'Degree (D,M,S)':<15} | {'Sign':<12} | {'Status':<15}")
    else:
        print(f"{'Lagna (La)':<10} | {lagna_degree_str:<15} | {lagna_sign:<12}")
        print("-" * 45)
        print(f"{'Planet':<10} | {'Degree (D,M,S)':<15} | {'Sign':<12}")
    
    print("-" * 60 if is_rasi_chart else "-" * 45)
    
    planets_for_display = []
    for planet_name in PLANET_NAMES:
        if planet_name in chart["planets"]:
            planets_for_display.append((planet_name, chart["planets"][planet_name]))
    
    # Sort by house first (for logical grouping), then by degree
    planets_for_display.sort(key=lambda item: (item[1].get('house', 0), item[1]['degree'] % 30))

    for planet_name, data in planets_for_display:
        degree = data.get("degree", 0.0)
        d, m, s = decimal_to_dms(degree)
        degree_str = f"{d:02d},{m:02d},{s:02d}"
        sign = data["sign"]
        
        # Only print status for Rasi chart
        if is_rasi_chart:
            status_indicators = []
            if data.get("is_retrograde"): status_indicators.append(STATUS_SYMBOLS["retrograde"])
            if data.get("is_combust"): status_indicators.append(STATUS_SYMBOLS["combust"])
            if data.get("is_exalted"): status_indicators.append(STATUS_SYMBOLS["exalted"])
            if data.get("is_debilitated"): status_indicators.append(STATUS_SYMBOLS["debilitated"])
            if data.get("is_vargottama"): status_indicators.append(STATUS_SYMBOLS["vargottama"])
            status_str = " ".join(status_indicators)
            print(f"{PLANET_ABBR.get(planet_name, planet_name):<10} | {degree_str:<15} | {sign:<12} | {status_str:<15}")
        else:
            print(f"{PLANET_ABBR.get(planet_name, planet_name):<10} | {degree_str:<15} | {sign:<12}")

    print("-" * 60 if is_rasi_chart else "-" * 45)


def draw_north_indian(chart, title):
    win = tk.Toplevel()
    win.title(title)
    canvas = tk.Canvas(win, width=450, height=450, bg="white")
    canvas.pack(padx=10, pady=10)

    center_x, center_y = 225, 225
    half_side = 200

    canvas.create_polygon(
        center_x, center_y - half_side, center_x + half_side, center_y,
        center_x, center_y + half_side, center_x - half_side, center_y,
        outline="black", fill="#f7f7f7", width=2
    )

    canvas.create_line(center_x - half_side, center_y, center_x + half_side, center_y, width=1)
    canvas.create_line(center_x, center_y - half_side, center_x, center_y + half_side, width=1)
    canvas.create_line(center_x - half_side / 2, center_y - half_side / 2, center_x + half_side / 2, center_y + half_side / 2, width=1)
    canvas.create_line(center_x + half_side / 2, center_y - half_side / 2, center_x - half_side / 2, center_y + half_side / 2, width=1)
    canvas.create_line(center_x - half_side, center_y, center_x, center_y + half_side, width=1)
    canvas.create_line(center_x + half_side, center_y, center_x, center_y + half_side, width=1)
    canvas.create_line(center_x - half_side, center_y, center_x, center_y - half_side, width=1)
    canvas.create_line(center_x + half_side, center_y, center_x, center_y - half_side, width=1)

    house_display_coords = {
        1: (center_x, center_y - half_side + 50), 2: (center_x + half_side - 50, center_y - 70),
        3: (center_x + half_side - 50, center_y + 70), 4: (center_x, center_y + half_side - 50),
        5: (center_x - half_side + 50, center_y + 70), 6: (center_x - half_side + 50, center_y - 70),
        7: (center_x + 70, center_y - 20), 8: (center_x + 20, center_y - 70),
        9: (center_x - 20, center_y - 70), 10: (center_x - 70, center_y - 20),
        11: (center_x - 20, center_y + 70), 12: (center_x + 20, center_y + 70)
    }

    sign_num_offset_x = -40
    sign_num_offset_y = -60
    planet_text_start_y_offset = -30
    line_height = 15

    is_rasi_chart = chart.get('chart_type_specific') == "Rasi (Lagna) Chart"
    visual_lagna_sign_index = ZODIAC_SIGNS.index(chart['ascendant']['sign'])
    
    sign_index_to_visual_house_map = {}
    for i in range(12):
        actual_sign_index = (visual_lagna_sign_index + i) % 12
        visual_house_number = i + 1 
        sign_index_to_visual_house_map[actual_sign_index] = visual_house_number

    houses_content = {i: [] for i in range(1, 13)}
    houses_content[1].append("La") 

    for planet_name in PLANET_NAMES:
        if planet_name in chart['planets']:
            data = chart['planets'][planet_name]
            
            visual_house_number_for_planet = None
            if chart.get('chart_type_specific') == 'Chalit':
                visual_house_number_for_planet = data.get("house")
                if visual_house_number_for_planet is None:
                    visual_house_number_for_planet = sign_index_to_visual_house_map[ZODIAC_SIGNS.index(data['sign'])]
            else:
                planet_sign_index = ZODIAC_SIGNS.index(data['sign'])
                visual_house_number_for_planet = sign_index_to_visual_house_map[planet_sign_index]

            if visual_house_number_for_planet is None: continue

            d, m, s = decimal_to_dms(data['degree'])
            planet_degree_formatted = f"{d:02d},{m:02d}"
            planet_display = f"{planet_degree_formatted}{PLANET_ABBR[planet_name]}"
            
            # Only add status symbols for the Rasi chart
            if is_rasi_chart:
                if data.get("is_retrograde"): planet_display += STATUS_SYMBOLS["retrograde"]
                if data.get("is_combust"): planet_display += STATUS_SYMBOLS["combust"]
                if data.get("is_exalted"): planet_display += STATUS_SYMBOLS["exalted"]
                if data.get("is_debilitated"): planet_display += STATUS_SYMBOLS["debilitated"]
                if data.get("is_vargottama"): planet_display += STATUS_SYMBOLS["vargottama"]

            houses_content[visual_house_number_for_planet].append(planet_display)

    for visual_house_num in range(1, 13):
        actual_sign_index_for_house = (visual_lagna_sign_index + (visual_house_num - 1)) % 12
        actual_sign_number_for_house = actual_sign_index_for_house + 1
        x, y = house_display_coords[visual_house_num]
        canvas.create_text(x + sign_num_offset_x, y + sign_num_offset_y, text=str(actual_sign_number_for_house), font=("Arial", 10, "bold"), fill="black", anchor="nw")
        
        current_y_offset = y + planet_text_start_y_offset
        
        def sort_key(s):
            if s == "La": return (0, "")
            try:
                if ',' in s:
                    deg_str = s.split(',')[0]
                    if deg_str.isdigit(): return (1, int(deg_str))
                return (2, s)
            except (ValueError, IndexError): return (2, s)

        sorted_elements_in_house = sorted(houses_content[visual_house_num], key=sort_key)

        for p_str in sorted_elements_in_house:
            text_color = "red" if p_str == "La" else "blue"
            font_style = ("Arial", 10, "bold") if p_str == "La" else ("Arial", 9)
            canvas.create_text(x + sign_num_offset_x, current_y_offset, text=p_str, font=font_style, fill=text_color, anchor="nw")
            current_y_offset += line_height

    win.lift()


# --- Main Execution Block ---
if __name__ == "__main__":
    print("--- Vedic Astrology Chart Generator ---")
    name = input("Enter Full Name: ")
    birth_date = input("Enter Birth Date (YYYY-MM-DD): ")
    birth_time = input("Enter Birth Time (HH:MM or HH:MM:SS in 24-hr format): ")
    birth_location = input("Enter Birth Location (e.g., 'Delhi, India'): ")

    lat_birth, lon_birth = get_coords(birth_location)
    if lat_birth is None or lon_birth is None:
        print("Could not determine birth coordinates. Please try a more specific location name.")
        exit()
    else:
        print(f"\nGeocoded Birth Location: Latitude = {lat_birth:.4f}, Longitude = {lon_birth:.4f}")

    utc_offset_birth = get_timezone_offset(lat_birth, lon_birth, birth_date, birth_time)
    if utc_offset_birth is None:
        exit()

    rasi_chart = calculate_rasi_chart(name, birth_date, birth_time, birth_location, utc_offset_birth)
    if not rasi_chart:
        exit()

    moon_chart = calculate_moon_chart(rasi_chart)
    navamsha_chart = calculate_navamsha_chart(rasi_chart)
    chalit_chart = calculate_chalit_chart(rasi_chart)
    
    atmakaraka_planet, _ = get_atmakaraka_info(rasi_chart)
    karakamsha_lagna_sign = None
    if atmakaraka_planet and atmakaraka_planet in navamsha_chart["planets"]:
        karakamsha_lagna_sign = navamsha_chart["planets"][atmakaraka_planet]["sign"]

    swamsha_chart = None
    if karakamsha_lagna_sign:
        swamsha_chart = create_reoriented_chart(name, rasi_chart['planets'], karakamsha_lagna_sign, "Swamsha")
        if swamsha_chart: swamsha_chart["atmakaraka"] = atmakaraka_planet

    karakamsha_chart = None
    if karakamsha_lagna_sign:
        karakamsha_chart = create_reoriented_chart(name, navamsha_chart['planets'], karakamsha_lagna_sign, "Karakamsha")
        if karakamsha_chart: karakamsha_chart["atmakaraka"] = atmakaraka_planet

    vargottama_planets_list = check_vargottama(rasi_chart, navamsha_chart)
    for planet_name in vargottama_planets_list:
        if planet_name in rasi_chart["planets"]:
            rasi_chart["planets"][planet_name]["is_vargottama"] = True
        # No need to add to navamsha, as status is only on rasi

    # --- Transit Chart Calculations ---
    print("\n--- Transit Chart Input (Press Enter for default current values) ---")
    now = datetime.now()
    default_transit_date = now.strftime("%Y-%m-%d")
    default_transit_time = now.strftime("%H:%M:%S")

    transit_date_input = input(f"Enter Transit Date (YYYY-MM-DD) [Default: {default_transit_date}]: ")
    transit_time_input = input(f"Enter Transit Time (HH:MM or HH:MM:SS) [Default: {default_transit_time}]: ")
    transit_location_input = input(f"Enter Transit Location (e.g., 'Seoul, South Korea') [Default: {birth_location}]: ")

    transit_date = transit_date_input if transit_date_input else default_transit_date
    transit_time = transit_time_input if transit_time_input else default_transit_time
    transit_location = transit_location_input if transit_location_input else birth_location

    transit_lat, transit_lon = get_coords(transit_location)
    if transit_lat is None or transit_lon is None:
        print(f"Could not determine transit coordinates for '{transit_location}'. Using birth location.")
        transit_lat, transit_lon = lat_birth, lon_birth
        transit_location = birth_location
    else:
        print(f"Geocoded Transit Location: Latitude = {transit_lat:.4f}, Longitude = {transit_lon:.4f}")

    utc_offset_transit = get_timezone_offset(transit_lat, transit_lon, transit_date, transit_time)
    
    transit_lagna_chart = None
    transit_moon_chart = None
    if utc_offset_transit is not None:
        # Pass is_natal_chart=False so no status is calculated for transit planets
        transit_planets, transit_ascendant, _, _ = calculate_planets_and_ascendant(
            transit_date, transit_time, transit_lat, transit_lon, utc_offset_transit, is_natal_chart=False
        )
        if transit_planets and transit_ascendant:
            transit_lagna_chart = create_transit_chart(rasi_chart, transit_planets, transit_ascendant, 'Lagna')
            transit_moon_chart = create_transit_chart(rasi_chart, transit_planets, transit_ascendant, 'Moon')
    else:
        print("Could not determine transit timezone. Skipping transit charts.")

    # --- Print All Chart Details ---
    print_chart_details(rasi_chart, "Rasi (Lagna) Chart - Natal")
    print_chart_details(moon_chart, "Moon Chart (Chandra Lagna) - Natal")
    print_chart_details(chalit_chart, "Chalit (Bhava) Chart - Natal")
    print_chart_details(navamsha_chart, "Navamsha (D9) Chart - Natal")
    
    if swamsha_chart: print_chart_details(swamsha_chart, f"Swamsha Chart (AK: {swamsha_chart['atmakaraka']}) - Natal Re-oriented")
    if karakamsha_chart: print_chart_details(karakamsha_chart, f"Karakamsha Chart (AK in D9: {karakamsha_chart['atmakaraka']}) - Navamsha Re-oriented")

    if transit_lagna_chart: print_chart_details(transit_lagna_chart, f"Transit Chart from Natal Lagna ({transit_date} {transit_time} at {transit_location})")
    if transit_moon_chart: print_chart_details(transit_moon_chart, f"Transit Chart from Natal Moon ({transit_date} {transit_time} at {transit_location})")

    # --- Lal Kitab Predictions ---
    print("\n--- Lal Kitab Predictions (Optional) ---")
    show_lal_kitab = input("Do you want to see Lal Kitab predictions? (y/n) [Default: y]: ").strip().lower()
    
    if show_lal_kitab in ['y', 'yes', '']:
        try:
            # Initialize Lal Kitab Predictor
            lal_kitab_file = "lal_kitab_data.txt"  # You can change this path
            lk_predictor = LalKitabPredictor(lal_kitab_file)
            
            # Print Lal Kitab predictions based on Rasi chart
            lk_predictor.print_predictions(rasi_chart)
        except Exception as e:
            print(f"Error generating Lal Kitab predictions: {e}")

    # --- Start GUI for chart visualization ---
    root = tk.Tk()
    root.title("Kundali Charts")
    root.geometry("500x650") 

    label = tk.Label(root, text=f"Charts for {rasi_chart['name']}", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    tk.Label(root, text="--- Natal Charts ---", font=("Arial", 12, "underline")).pack(pady=5)
    tk.Button(root, text="Show Rasi (Lagna) Chart", command=lambda: draw_north_indian(rasi_chart, f"Rasi (Lagna) Chart - {name}"), width=40, height=2).pack(pady=2)
    tk.Button(root, text="Show Moon Chart (Chandra Lagna)", command=lambda: draw_north_indian(moon_chart, f"Moon Chart - {name}"), width=40, height=2).pack(pady=2)
    tk.Button(root, text="Show Chalit (Bhava) Chart", command=lambda: draw_north_indian(chalit_chart, f"Chalit (Bhava) Chart - {name}"), width=40, height=2).pack(pady=2)
    tk.Button(root, text="Show Navamsha (D9) Chart", command=lambda: draw_north_indian(navamsha_chart, f"Navamsha (D9) Chart - {name}"), width=40, height=2).pack(pady=2)
    
    if swamsha_chart: tk.Button(root, text=f"Show Swamsha Chart (AK: {swamsha_chart['atmakaraka']})", command=lambda: draw_north_indian(swamsha_chart, f"Swamsha Chart - {name}"), width=40, height=2).pack(pady=2)
    if karakamsha_chart: tk.Button(root, text=f"Show Karakamsha Chart (AK in D9: {karakamsha_chart['atmakaraka']})", command=lambda: draw_north_indian(karakamsha_chart, f"Karakamsha Chart - {name}"), width=40, height=2).pack(pady=2)
    
    # Lal Kitab Predictions Button
    def show_lal_kitab_predictions():
        try:
            lal_kitab_file = "lal_kitab_data.txt"
            lk_predictor = LalKitabPredictor(lal_kitab_file)
            
            # Create a new window for predictions
            pred_window = tk.Toplevel(root)
            pred_window.title(f"Lal Kitab Predictions - {name}")
            pred_window.geometry("800x600")
            
            # Add scrollbar
            scrollbar = tk.Scrollbar(pred_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Text widget to display predictions
            text_widget = tk.Text(pred_window, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 10))
            text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            scrollbar.config(command=text_widget.yview)
            
            # Generate and display predictions
            predictions = lk_predictor.generate_chart_predictions(rasi_chart)
            
            text_widget.insert(tk.END, f"{'=' * 80}\n", "header")
            text_widget.insert(tk.END, f"🔮 LAL KITAB PREDICTIONS for {name} 🔮\n", "header")
            text_widget.insert(tk.END, f"{'=' * 80}\n", "header")
            text_widget.insert(tk.END, f"Based on Lagna Chart (Ascendant: {rasi_chart['ascendant']['sign']})\n", "subheader")
            text_widget.insert(tk.END, f"{'=' * 80}\n\n", "header")
            
            for planet_name, pred_data in predictions.items():
                text_widget.insert(tk.END, f"{'─' * 80}\n", "separator")
                text_widget.insert(tk.END, f"📍 {planet_name.upper()} in House {pred_data['house']} ({pred_data['sign']})\n", "planet")
                text_widget.insert(tk.END, f"{'─' * 80}\n\n", "separator")
                text_widget.insert(tk.END, "🔍 PREDICTION:\n", "label")
                text_widget.insert(tk.END, f"   {pred_data['prediction']}\n\n", "prediction")
                text_widget.insert(tk.END, "💊 REMEDY:\n", "label")
                text_widget.insert(tk.END, f"   {pred_data['remedy']}\n\n", "remedy")
            
            text_widget.insert(tk.END, f"\n{'=' * 80}\n", "header")
            text_widget.insert(tk.END, "Note: These predictions are based on Lal Kitab principles.\n", "note")
            text_widget.insert(tk.END, f"{'=' * 80}\n", "header")
            
            # Configure text tags for formatting
            text_widget.tag_config("header", font=("Arial", 12, "bold"), foreground="#2E86AB")
            text_widget.tag_config("subheader", font=("Arial", 11), foreground="#555")
            text_widget.tag_config("planet", font=("Arial", 11, "bold"), foreground="#A23B72")
            text_widget.tag_config("label", font=("Arial", 10, "bold"), foreground="#F18F01")
            text_widget.tag_config("prediction", font=("Arial", 10), foreground="#333")
            text_widget.tag_config("remedy", font=("Arial", 10), foreground="#06A77D")
            text_widget.tag_config("separator", foreground="#CCC")
            text_widget.tag_config("note", font=("Arial", 9, "italic"), foreground="#888")
            
            text_widget.config(state=tk.DISABLED)  # Make it read-only
            pred_window.lift()
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not load Lal Kitab predictions:\n{str(e)}")
    
    tk.Label(root, text="--- Lal Kitab Predictions ---", font=("Arial", 12, "underline")).pack(pady=5)
    tk.Button(root, text="Show Lal Kitab Predictions & Remedies", command=show_lal_kitab_predictions, width=40, height=2, bg="#FFD700").pack(pady=2)

    if transit_lagna_chart and transit_moon_chart:
        tk.Label(root, text=f"--- Transit Charts ({transit_date} {transit_time} at {transit_location}) ---", font=("Arial", 12, "underline")).pack(pady=5)
        tk.Button(root, text=f"Show Transit Chart from Natal Lagna", command=lambda: draw_north_indian(transit_lagna_chart, f"Transit from Lagna - {name} ({transit_date})"), width=40, height=2).pack(pady=2)
        tk.Button(root, text=f"Show Transit Chart from Natal Moon", command=lambda: draw_north_indian(transit_moon_chart, f"Transit from Moon - {name} ({transit_date})"), width=40, height=2).pack(pady=2)
    else:
        tk.Label(root, text="Transit charts could not be calculated.", fg="red").pack(pady=5)

    root.mainloop()