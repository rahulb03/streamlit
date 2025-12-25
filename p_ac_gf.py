# # # import swisseph as swe
# # # from datetime import datetime, timedelta
# # # import tkinter as tk
# # # from geopy.geocoders import Nominatim
# # # from timezonefinder import TimezoneFinder
# # # import pytz
# # # import math

# # # # --- Setup and Constants ---
# # # try:
# # #     # Ensure this path is correct for your system.
# # #     # If you don't have Swiss Ephemeris files, this script may not be fully accurate.
# # #     # You can download them from https://www.astro.com/ftp/swisseph/ephe/
# # #     swe.set_ephe_path('C:/swiss/epeh')
# # # except swe.Error:
# # #     print("Warning: Swiss Ephemeris path not found. Calculations will use built-in ephemeris which is less accurate for older dates.")

# # # ZODIAC_SIGNS = [
# # #     "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
# # #     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
# # # ]

# # # PLANET_NAMES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]

# # # traditional_planet_ids = {
# # #     "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
# # #     "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN
# # # }
# # # outer_planet_ids = {
# # #     "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
# # # }

# # # # Panchanga Data
# # # TITHIS = [
# # #     "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", "Shukla Panchami",
# # #     "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami", "Shukla Navami", "Shukla Dashami",
# # #     "Shukla Ekadashi", "Shukla Dwadashi", "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
# # #     "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", "Krishna Panchami",
# # #     "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami", "Krishna Navami", "Krishna Dashami",
# # #     "Krishna Ekadashi", "Krishna Dwadashi", "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
# # # ]
# # # NAKSHATRAS = [
# # #     "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
# # #     "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
# # #     "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada",
# # #     "Uttara Bhadrapada", "Revati"
# # # ]
# # # YOGAS = [
# # #     "Vishkambha", "Priti", "Aayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarman", "Dhriti", "Shula",
# # #     "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
# # #     "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
# # # ]
# # # KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kintughna"]
# # # WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# # # # Planetary Data for Avakahada Chakra
# # # PLANET_RULERSHIPS = {
# # #     "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
# # #     "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
# # # }

# # # # --- Helper Functions ---
# # # def get_coords(location_name):
# # #     try:
# # #         geolocator = Nominatim(user_agent="kundali_app_v15")
# # #         location = geolocator.geocode(location_name)
# # #         if location:
# # #             return location.latitude, location.longitude
# # #     except Exception as e:
# # #         print(f"Geocoding error: {e}")
# # #     return None, None

# # # def get_timezone_info(lat, lon, date_str, time_str):
# # #     tf = TimezoneFinder()
# # #     timezone_name = tf.timezone_at(lat=lat, lng=lon)
# # #     if not timezone_name:
# # #         print("Could not detect timezone. Defaulting to UTC.")
# # #         return 0.0, "UTC"
    
# # #     local_tz = pytz.timezone(timezone_name)
# # #     try:
# # #         time_format = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
# # #         naive_dt = datetime.strptime(f"{date_str} {time_str}", time_format)
# # #     except ValueError:
# # #         naive_dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")

# # #     local_dt = local_tz.localize(naive_dt)
# # #     return local_dt.utcoffset().total_seconds() / 3600.0, timezone_name

# # # def get_sign(degree):
# # #     return ZODIAC_SIGNS[int(degree // 30)]

# # # def format_dms(degree):
# # #     d = int(degree)
# # #     m = int((degree - d) * 60)
# # #     s = int(((degree - d) * 60 - m) * 60)
# # #     return f"{d:02d}° {m:02d}' {s:02d}\""

# # # # --- Core Calculation Functions ---

# # # def calculate_planets_and_ascendant(date_str, time_str, latitude, longitude, timezone_offset):
# # #     time_format_str = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
# # #     try:
# # #         dt = datetime.strptime(f"{date_str} {time_str}", time_format_str)
# # #     except ValueError:
# # #         dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")

# # #     utc_dt = dt - timedelta(hours=timezone_offset)
# # #     jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

# # #     swe.set_sid_mode(swe.SIDM_LAHIRI)
# # #     ayanamsa = swe.get_ayanamsa_ut(jd_ut)

# # #     _, ascmc = swe.houses(jd_ut, latitude, longitude, b'P')
# # #     ascendant_degree = (ascmc[0] - ayanamsa) % 360

# # #     planets = {}
# # #     tropical_sun_sign = ""
# # #     all_planet_ids = {**traditional_planet_ids, **outer_planet_ids}
# # #     for planet_name, planet_id in all_planet_ids.items():
# # #         xx, _ = swe.calc_ut(jd_ut, planet_id)
# # #         if planet_name == "Sun":
# # #             tropical_sun_sign = get_sign(xx[0])
# # #         sidereal_lon = (xx[0] - ayanamsa) % 360
# # #         planets[planet_name] = {"degree": sidereal_lon, "sign": get_sign(sidereal_lon)}

# # #     rahu_xx, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
# # #     rahu_lon = (rahu_xx[0] - ayanamsa) % 360
# # #     planets["Rahu"] = {"degree": rahu_lon, "sign": get_sign(rahu_lon)}
# # #     planets["Ketu"] = {"degree": (rahu_lon + 180) % 360, "sign": get_sign((rahu_lon + 180) % 360)}

# # #     return planets, {"degree": ascendant_degree, "sign": get_sign(ascendant_degree)}, jd_ut, ayanamsa, tropical_sun_sign


# # # def calculate_panchanga(jd_ut, birth_date_str):
# # #     swe.set_sid_mode(swe.SIDM_LAHIRI)
# # #     ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    
# # #     sun_data, _ = swe.calc_ut(jd_ut, swe.SUN)
# # #     moon_data, _ = swe.calc_ut(jd_ut, swe.MOON)

# # #     sun_lon = (sun_data[0] - ayanamsa) % 360
# # #     moon_lon = (moon_data[0] - ayanamsa) % 360

# # #     tithi_lon = (moon_lon - sun_lon + 360) % 360
# # #     tithi_index = int(tithi_lon / 12)
# # #     paksha = "Shukla Paksha" if tithi_index < 15 else "Krishna Paksha"
    
# # #     karana_num = int(tithi_lon / 6)
# # #     if karana_num == 0: karana_index = 10 
# # #     elif karana_num < 8: karana_index = karana_num - 1
# # #     elif karana_num > 56: karana_index = karana_num - 50
# # #     else: karana_index = ((karana_num - 1) % 7)

# # #     nakshatra_span = 13 + 1/3
# # #     nakshatra_index = int(moon_lon / nakshatra_span)
    
# # #     yoga_lon = (sun_lon + moon_lon) % 360
# # #     yoga_index = int(yoga_lon / (13 + 1/3))
    
# # #     birth_dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
# # #     weekday = WEEKDAYS[birth_dt.weekday()]
# # #     weekday_index_for_paya = (birth_dt.weekday() + 1) % 7
    
# # #     return {
# # #         "moon_lon": moon_lon, # Pass moon longitude for debugging
# # #         "tithi": TITHIS[tithi_index], "paksha": paksha, "karana": KARANAS[karana_index],
# # #         "nakshatra": NAKSHATRAS[nakshatra_index], "nakshatra_index": nakshatra_index,
# # #         "yoga": YOGAS[yoga_index], "weekday": weekday, "weekday_index_for_paya": weekday_index_for_paya
# # #     }

# # # def calculate_avakahada_chakra(rasi_chart, panchanga, ayanamsa_val, tropical_sun_sign):
# # #     details = {}
# # #     moon_sign = rasi_chart['planets']['Moon']['sign']
# # #     moon_lon = rasi_chart['planets']['Moon']['degree']
# # #     moon_nakshatra = panchanga['nakshatra']
    
# # #     # Mappings
# # #     VARNA_MAP = {"Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin", "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya", "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya", "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra"}
# # #     VASYA_MAP = {"Aries": "Chatushpada", "Taurus": "Chatushpada", "Leo": "Chatushpada", "Gemini": "Manava", "Virgo": "Manava", "Libra": "Manava", "Sagittarius": "Manava", "Aquarius": "Manava", "Cancer": "Jalachara", "Pisces": "Jalachara", "Scorpio": "Keeta"}
# # #     GANA_MAP = {"Ashwini": "Deva", "Mrigashira": "Deva", "Punarvasu": "Deva", "Pushya": "Deva", "Hasta": "Deva", "Swati": "Deva", "Anuradha": "Deva", "Shravana": "Deva", "Revati": "Deva", "Bharani": "Manushya", "Rohini": "Manushya", "Ardra": "Manushya", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya", "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Krittika": "Rakshasa", "Ashlesha": "Rakshasa", "Magha": "Rakshasa", "Chitra": "Rakshasa", "Vishakha": "Rakshasa", "Jyeshtha": "Rakshasa", "Mula": "Rakshasa", "Dhanishtha": "Rakshasa", "Shatabhisha": "Rakshasa"}
# # #     NADI_MAP = {"Ashwini": "Adi", "Ardra": "Adi", "Punarvasu": "Adi", "Uttara Phalguni": "Adi", "Hasta": "Adi", "Jyeshtha": "Adi", "Mula": "Adi", "Shatabhisha": "Adi", "Purva Bhadrapada": "Adi", "Bharani": "Madhya", "Mrigashira": "Madhya", "Pushya": "Madhya", "Purva Phalguni": "Madhya", "Chitra": "Madhya", "Anuradha": "Madhya", "Purva Ashadha": "Madhya", "Dhanishtha": "Madhya", "Uttara Bhadrapada": "Madhya", "Krittika": "Antya", "Rohini": "Antya", "Ashlesha": "Antya", "Magha": "Antya", "Swati": "Antya", "Vishakha": "Antya", "Uttara Ashadha": "Antya", "Shravana": "Antya", "Revati": "Antya"}
# # #     YONI_MAP = {"Ashwini": "Ashwa (Horse)", "Bharani": "Gaja (Elephant)", "Krittika": "Mesha (Sheep)", "Rohini": "Sarpa (Serpent)", "Mrigashira": "Sarpa (Serpent)", "Ardra": "Shwana (Dog)", "Punarvasu": "Marjara (Cat)", "Pushya": "Mesha (Sheep)", "Ashlesha": "Marjara (Cat)", "Magha": "Mushaka (Rat)", "Purva Phalguni": "Mushaka (Rat)", "Uttara Phalguni": "Go (Cow)", "Hasta": "Mahisha (Buffalo)", "Chitra": "Vyaghra (Tiger)", "Swati": "Mahisha (Buffalo)", "Vishakha": "Vyaghra (Tiger)", "Anuradha": "Mriga (Deer)", "Jyeshtha": "Mriga (Deer)", "Mula": "Shwana (Dog)", "Purva Ashadha": "Vanara (Monkey)", "Uttara Ashadha": "Nakula (Mongoose)", "Shravana": "Vanara (Monkey)", "Dhanishtha": "Simha (Lion)", "Shatabhisha": "Ashwa (Horse)", "Purva Bhadrapada": "Simha (Lion)", "Uttara Bhadrapada": "Go (Cow)", "Revati": "Gaja (Elephant)"}
# # #     NAKSHATRA_LORD_MAP = {"Ashwini": "Ketu", "Magha": "Ketu", "Mula": "Ketu", "Bharani": "Venus", "Purva Phalguni": "Venus", "Purva Ashadha": "Venus", "Krittika": "Sun", "Uttara Phalguni": "Sun", "Uttara Ashadha": "Sun", "Rohini": "Moon", "Hasta": "Moon", "Shravana": "Moon", "Mrigashira": "Mars", "Chitra": "Mars", "Dhanishtha": "Mars", "Ardra": "Rahu", "Swati": "Rahu", "Shatabhisha": "Rahu", "Punarvasu": "Jupiter", "Vishakha": "Jupiter", "Purva Bhadrapada": "Jupiter", "Pushya": "Saturn", "Anuradha": "Saturn", "Uttara Bhadrapada": "Saturn", "Ashlesha": "Mercury", "Jyeshtha": "Mercury", "Revati": "Mercury"}
# # #     VIMSOTTARI_DURATIONS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

# # #     # Basic Details
# # #     details['ayanamsa_name'] = "Lahiri"
# # #     details['ayanamsa_value'] = format_dms(ayanamsa_val)
# # #     details['sun_sign_indian'] = rasi_chart['planets']['Sun']['sign']
# # #     details['sun_sign_western'] = tropical_sun_sign
# # #     details['lagna'] = rasi_chart['ascendant']['sign']
# # #     details['rasi'] = moon_sign
# # #     details['varna'] = VARNA_MAP.get(moon_sign, "N/A")
# # #     details['gana'] = GANA_MAP.get(moon_nakshatra, "N/A")
# # #     details['nadi'] = NADI_MAP.get(moon_nakshatra, "N/A")
# # #     details['yoni'] = YONI_MAP.get(moon_nakshatra, "N/A")
# # #     details['lagna_lord'] = PLANET_RULERSHIPS.get(details['lagna'], "N/A")
# # #     details['rasi_lord'] = PLANET_RULERSHIPS.get(details['rasi'], "N/A")
    
# # #     if moon_sign == "Capricorn":
# # #         moon_deg_in_sign = rasi_chart['planets']['Moon']['degree'] % 30
# # #         details['vasya'] = "Jalachara (Water)" if moon_deg_in_sign < 15 else "Chatushpada (Quadruped)"
# # #     else:
# # #         details['vasya'] = VASYA_MAP.get(moon_sign, "N/A")

# # #     # Nakshatra Details
# # #     nakshatra_span = 13 + 1/3
# # #     moon_lon_in_nakshatra = moon_lon - (panchanga['nakshatra_index'] * nakshatra_span)
# # #     details['nakshatra_pada'] = math.floor(moon_lon_in_nakshatra / (nakshatra_span / 4)) + 1
# # #     details['nakshatra_lord'] = NAKSHATRA_LORD_MAP.get(moon_nakshatra, "N/A")

# # #     # PAYA CALCULATION
# # #     PAYA_TABLE = [
# # #         ["Gold", "Iron", "Copper", "Silver", "Gold", "Copper", "Iron"],
# # #         ["Iron", "Silver", "Gold", "Iron", "Silver", "Gold", "Copper"],
# # #         ["Silver", "Copper", "Iron", "Gold", "Copper", "Iron", "Gold"],
# # #         ["Copper", "Gold", "Silver", "Copper", "Iron", "Silver", "Gold"]
# # #     ]
# # #     nakshatra_mod = panchanga['nakshatra_index'] % 4
# # #     weekday_index = panchanga['weekday_index_for_paya']
# # #     details['paya'] = PAYA_TABLE[nakshatra_mod][weekday_index]
            
# # #     # Balance of Dasha
# # #     dasha_lord = details['nakshatra_lord']
# # #     total_dasha_period = VIMSOTTARI_DURATIONS.get(dasha_lord, 0)
# # #     moon_remaining_in_nakshatra = nakshatra_span - moon_lon_in_nakshatra
# # #     balance_decimal = (moon_remaining_in_nakshatra / nakshatra_span) * total_dasha_period
    
# # #     years = int(balance_decimal)
# # #     months = int((balance_decimal - years) * 12)
# # #     days = int((((balance_decimal - years) * 12) - months) * 30.4375)
# # #     details['balance_of_dasha'] = f"{dasha_lord}: {years}Y, {months}M, {days}D"
    
# # #     return details

# # # # --- Main Chart Calculation Wrapper ---
# # # def get_rasi_chart(name, birth_date, birth_time, location_str, timezone_offset):
# # #     lat, lon = get_coords(location_str)
# # #     if lat is None: return None, None, None, None, None
# # #     planets, ascendant, jd_ut, ayanamsa, tropical_sun_sign = calculate_planets_and_ascendant(birth_date, birth_time, lat, lon, timezone_offset)
# # #     if planets is None: return None, None, None, None, None
# # #     return {"name": name, "ascendant": ascendant, "planets": planets}, jd_ut, ayanamsa, tropical_sun_sign

# # # # --- Main Execution Block ---
# # # if __name__ == "__main__":
# # #     print("--- Vedic Astrology Chart Generator ---")
# # #     name = input("Enter Full Name: ")
# # #     birth_date = input("Enter Birth Date (YYYY-MM-DD): ")
# # #     birth_time = input("Enter Birth Time (HH:MM or HH:MM:SS in 24-hr format): ")
# # #     birth_location = input("Enter Birth Location (e.g., 'Delhi, India'): ")

# # #     lat_birth, lon_birth = get_coords(birth_location)
# # #     if lat_birth is None: exit()
# # #     print(f"\nGeocoded Birth Location: Latitude = {lat_birth:.4f}, Longitude = {lon_birth:.4f}")

# # #     utc_offset_birth, tz_name_birth = get_timezone_info(lat_birth, lon_birth, birth_date, birth_time)

# # #     rasi_chart, natal_jd_ut, ayanamsa_val, tropical_sun_sign = get_rasi_chart(name, birth_date, birth_time, birth_location, utc_offset_birth)
# # #     if rasi_chart is None: exit()
    
# # #     panchanga = calculate_panchanga(natal_jd_ut, birth_date)
# # #     avakahada = calculate_avakahada_chakra(rasi_chart, panchanga, ayanamsa_val, tropical_sun_sign)
    
# # #     # --- DEBUG SECTION FOR PAYA ---
# # #     print("\n" + "!"*15 + " PAYA CALCULATION DEBUG " + "!"*15)
# # #     print(f"--> Moon Sidereal Longitude : {panchanga['moon_lon']:.4f} degrees")
# # #     print(f"--> Nakshatra Index (0-26)  : {panchanga['nakshatra_index']} ({panchanga['nakshatra']})")
# # #     print(f"--> Weekday                 : {panchanga['weekday']}")
# # #     print(f"--> Weekday Index (Sun=0)   : {panchanga['weekday_index_for_paya']}")
# # #     print(f"--> Nakshatra Index % 4     : {panchanga['nakshatra_index'] % 4}  (This is the ROW in the table)")
# # #     print(f"--> Paya Table[ROW][COLUMN] : PAYA_TABLE[{panchanga['nakshatra_index'] % 4}][{panchanga['weekday_index_for_paya']}]")
# # #     print(f"--> Final Paya Result       : {avakahada['paya']}")
# # #     print("!" * 52)
    
# # #     print("\n" + "=" * 60)
# # #     print(f"🌟 Astrological Details for {name} 🌟")
# # #     print("=" * 60)

# # #     print("\n--- Planetary Positions (Lahiri Ayanamsa) ---")
# # #     ascendant = rasi_chart['ascendant']
# # #     print(f"Ascendant : {ascendant['sign']:<12} {format_dms(ascendant['degree'])}")
# # #     display_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
# # #     for planet_name in display_order:
# # #         if planet_name in rasi_chart['planets']:
# # #             planet_info = rasi_chart['planets'][planet_name]
# # #             print(f"{planet_name:<9} : {planet_info['sign']:<12} {format_dms(planet_info['degree'])}")

# # #     print("\n--- Birth Panchanga ---")
# # #     print(f"Weekday     : {panchanga['weekday']}")
# # #     print(f"Tithi       : {panchanga['tithi']}")
# # #     print(f"Paksha      : {panchanga['paksha']}")
# # #     print(f"Karana      : {panchanga['karana']}")
# # #     print(f"Nakshatra   : {panchanga['nakshatra']}")
# # #     print(f"Yoga        : {panchanga['yoga']}")

# # #     print("\n--- Avakahada Chakra ---")
# # #     print(f"Ayanamsa        : {avakahada['ayanamsa_name']} ({avakahada['ayanamsa_value']})")
# # #     print(f"Sun Sign(Indian): {avakahada['sun_sign_indian']}")
# # #     print(f"Sun Sign(Western): {avakahada['sun_sign_western']}")
# # #     print(f"Lagna           : {avakahada['lagna']}")
# # #     print(f"Lagna Lord      : {avakahada['lagna_lord']}")
# # #     print(f"Rasi (Moon Sign): {avakahada['rasi']}")
# # #     print(f"Rasi Lord       : {avakahada['rasi_lord']}")
# # #     print(f"Nakshatra Lord  : {avakahada['nakshatra_lord']}")
# # #     print(f"Nakshatra Pada  : {avakahada['nakshatra_pada']}")
# # #     print(f"Dasha Balance   : {avakahada['balance_of_dasha']} remaining at birth")
# # #     print(f"Paya (Leg)      : {avakahada['paya']}")
# # #     print(f"Varna           : {avakahada['varna']} (Temperament)")
# # #     print(f"Vasya           : {avakahada['vasya']} (Influence)")
# # #     print(f"Yoni            : {avakahada['yoni']} (Animal Symbol)")
# # #     print(f"Gana            : {avakahada['gana']} (Clan)")
# # #     print(f"Nadi            : {avakahada['nadi']} (Constitution)")
# # #     print("-" * 60)


# # import swisseph as swe
# # from datetime import datetime, timedelta
# # import tkinter as tk
# # from geopy.geocoders import Nominatim
# # from timezonefinder import TimezoneFinder
# # import pytz
# # import math

# # # --- Setup and Constants ---
# # try:
# #     # Ensure this path is correct for your system.
# #     # If you don't have Swiss Ephemeris files, this script may not be fully accurate.
# #     # You can download them from https://www.astro.com/ftp/swisseph/ephe/
# #     swe.set_ephe_path('C:/swiss/epeh')
# # except swe.Error:
# #     print("Warning: Swiss Ephemeris path not found. Calculations will use built-in ephemeris which is less accurate for older dates.")

# # ZODIAC_SIGNS = [
# #     "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
# #     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
# # ]

# # PLANET_NAMES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]

# # traditional_planet_ids = {
# #     "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
# #     "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN
# # }
# # outer_planet_ids = {
# #     "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
# # }

# # # Panchanga Data
# # TITHIS = [
# #     "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", "Shukla Panchami",
# #     "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami", "Shukla Navami", "Shukla Dashami",
# #     "Shukla Ekadashi", "Shukla Dwadashi", "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
# #     "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", "Krishna Panchami",
# #     "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami", "Krishna Navami", "Krishna Dashami",
# #     "Krishna Ekadashi", "Krishna Dwadashi", "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
# # ]
# # NAKSHATRAS = [
# #     "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
# #     "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
# #     "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada",
# #     "Uttara Bhadrapada", "Revati"
# # ]
# # YOGAS = [
# #     "Vishkambha", "Priti", "Aayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarman", "Dhriti", "Shula",
# #     "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
# #     "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
# # ]
# # KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kintughna"]
# # WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# # # Planetary Data for Avakahada Chakra
# # PLANET_RULERSHIPS = {
# #     "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
# #     "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
# # }

# # # --- Yogini Dasha Data ---
# # YOGINI_DASHAS = [
# #     {"yogini": "Mangala", "lord": "Moon", "duration": 1},
# #     {"yogini": "Pingala", "lord": "Sun", "duration": 2},
# #     {"yogini": "Dhanya", "lord": "Jupiter", "duration": 3},
# #     {"yogini": "Bhramari", "lord": "Mars", "duration": 4},
# #     {"yogini": "Bhadrika", "lord": "Mercury", "duration": 5},
# #     {"yogini": "Ulka", "lord": "Saturn", "duration": 6},
# #     {"yogini": "Siddha", "lord": "Venus", "duration": 7},
# #     {"yogini": "Sankata", "lord": "Rahu", "duration": 8}
# # ]


# # # --- Helper Functions ---
# # def get_coords(location_name):
# #     try:
# #         geolocator = Nominatim(user_agent="kundali_app_v15")
# #         location = geolocator.geocode(location_name)
# #         if location:
# #             return location.latitude, location.longitude
# #     except Exception as e:
# #         print(f"Geocoding error: {e}")
# #     return None, None

# # def get_timezone_info(lat, lon, date_str, time_str):
# #     tf = TimezoneFinder()
# #     timezone_name = tf.timezone_at(lat=lat, lng=lon)
# #     if not timezone_name:
# #         print("Could not detect timezone. Defaulting to UTC.")
# #         return 0.0, "UTC"
    
# #     local_tz = pytz.timezone(timezone_name)
# #     try:
# #         time_format = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
# #         naive_dt = datetime.strptime(f"{date_str} {time_str}", time_format)
# #     except ValueError:
# #         naive_dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")

# #     local_dt = local_tz.localize(naive_dt)
# #     return local_dt.utcoffset().total_seconds() / 3600.0, timezone_name

# # def get_sign(degree):
# #     return ZODIAC_SIGNS[int(degree // 30)]

# # def format_dms(degree):
# #     d = int(degree)
# #     m = int((degree - d) * 60)
# #     s = int(((degree - d) * 60 - m) * 60)
# #     return f"{d:02d}° {m:02d}' {s:02d}\""

# # # --- Core Calculation Functions ---

# # def calculate_planets_and_ascendant(date_str, time_str, latitude, longitude, timezone_offset):
# #     time_format_str = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
# #     try:
# #         dt = datetime.strptime(f"{date_str} {time_str}", time_format_str)
# #     except ValueError:
# #         dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")

# #     utc_dt = dt - timedelta(hours=timezone_offset)
# #     jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

# #     swe.set_sid_mode(swe.SIDM_LAHIRI)
# #     ayanamsa = swe.get_ayanamsa_ut(jd_ut)

# #     _, ascmc = swe.houses(jd_ut, latitude, longitude, b'P')
# #     ascendant_degree = (ascmc[0] - ayanamsa) % 360

# #     planets = {}
# #     tropical_sun_sign = ""
# #     all_planet_ids = {**traditional_planet_ids, **outer_planet_ids}
# #     for planet_name, planet_id in all_planet_ids.items():
# #         xx, _ = swe.calc_ut(jd_ut, planet_id)
# #         if planet_name == "Sun":
# #             tropical_sun_sign = get_sign(xx[0])
# #         sidereal_lon = (xx[0] - ayanamsa) % 360
# #         planets[planet_name] = {"degree": sidereal_lon, "sign": get_sign(sidereal_lon)}

# #     rahu_xx, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
# #     rahu_lon = (rahu_xx[0] - ayanamsa) % 360
# #     planets["Rahu"] = {"degree": rahu_lon, "sign": get_sign(rahu_lon)}
# #     planets["Ketu"] = {"degree": (rahu_lon + 180) % 360, "sign": get_sign((rahu_lon + 180) % 360)}

# #     return planets, {"degree": ascendant_degree, "sign": get_sign(ascendant_degree)}, jd_ut, ayanamsa, tropical_sun_sign


# # def calculate_panchanga(jd_ut, birth_date_str):
# #     swe.set_sid_mode(swe.SIDM_LAHIRI)
# #     ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    
# #     sun_data, _ = swe.calc_ut(jd_ut, swe.SUN)
# #     moon_data, _ = swe.calc_ut(jd_ut, swe.MOON)

# #     sun_lon = (sun_data[0] - ayanamsa) % 360
# #     moon_lon = (moon_data[0] - ayanamsa) % 360

# #     tithi_lon = (moon_lon - sun_lon + 360) % 360
# #     tithi_index = int(tithi_lon / 12)
# #     paksha = "Shukla Paksha" if tithi_index < 15 else "Krishna Paksha"
    
# #     karana_num = int(tithi_lon / 6)
# #     if karana_num == 0: karana_index = 10 
# #     elif karana_num < 8: karana_index = karana_num - 1
# #     elif karana_num > 56: karana_index = karana_num - 50
# #     else: karana_index = ((karana_num - 1) % 7)

# #     nakshatra_span = 13 + 1/3
# #     nakshatra_index = int(moon_lon / nakshatra_span)
    
# #     yoga_lon = (sun_lon + moon_lon) % 360
# #     yoga_index = int(yoga_lon / (13 + 1/3))
    
# #     birth_dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
# #     weekday = WEEKDAYS[birth_dt.weekday()]
# #     weekday_index_for_paya = (birth_dt.weekday() + 1) % 7
    
# #     return {
# #         "moon_lon": moon_lon, # Pass moon longitude for debugging
# #         "tithi": TITHIS[tithi_index], "paksha": paksha, "karana": KARANAS[karana_index],
# #         "nakshatra": NAKSHATRAS[nakshatra_index], "nakshatra_index": nakshatra_index,
# #         "yoga": YOGAS[yoga_index], "weekday": weekday, "weekday_index_for_paya": weekday_index_for_paya
# #     }

# # def calculate_avakahada_chakra(rasi_chart, panchanga, ayanamsa_val, tropical_sun_sign):
# #     details = {}
# #     moon_sign = rasi_chart['planets']['Moon']['sign']
# #     moon_lon = rasi_chart['planets']['Moon']['degree']
# #     moon_nakshatra = panchanga['nakshatra']
    
# #     # Mappings
# #     VARNA_MAP = {"Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin", "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya", "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya", "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra"}
# #     VASYA_MAP = {"Aries": "Chatushpada", "Taurus": "Chatushpada", "Leo": "Chatushpada", "Gemini": "Manava", "Virgo": "Manava", "Libra": "Manava", "Sagittarius": "Manava", "Aquarius": "Manava", "Cancer": "Jalachara", "Pisces": "Jalachara", "Scorpio": "Keeta"}
# #     GANA_MAP = {"Ashwini": "Deva", "Mrigashira": "Deva", "Punarvasu": "Deva", "Pushya": "Deva", "Hasta": "Deva", "Swati": "Deva", "Anuradha": "Deva", "Shravana": "Deva", "Revati": "Deva", "Bharani": "Manushya", "Rohini": "Manushya", "Ardra": "Manushya", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya", "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Krittika": "Rakshasa", "Ashlesha": "Rakshasa", "Magha": "Rakshasa", "Chitra": "Rakshasa", "Vishakha": "Rakshasa", "Jyeshtha": "Rakshasa", "Mula": "Rakshasa", "Dhanishtha": "Rakshasa", "Shatabhisha": "Rakshasa"}
# #     NADI_MAP = {"Ashwini": "Adi", "Ardra": "Adi", "Punarvasu": "Adi", "Uttara Phalguni": "Adi", "Hasta": "Adi", "Jyeshtha": "Adi", "Mula": "Adi", "Shatabhisha": "Adi", "Purva Bhadrapada": "Adi", "Bharani": "Madhya", "Mrigashira": "Madhya", "Pushya": "Madhya", "Purva Phalguni": "Madhya", "Chitra": "Madhya", "Anuradha": "Madhya", "Purva Ashadha": "Madhya", "Dhanishtha": "Madhya", "Uttara Bhadrapada": "Madhya", "Krittika": "Antya", "Rohini": "Antya", "Ashlesha": "Antya", "Magha": "Antya", "Swati": "Antya", "Vishakha": "Antya", "Uttara Ashadha": "Antya", "Shravana": "Antya", "Revati": "Antya"}
# #     YONI_MAP = {"Ashwini": "Ashwa (Horse)", "Bharani": "Gaja (Elephant)", "Krittika": "Mesha (Sheep)", "Rohini": "Sarpa (Serpent)", "Mrigashira": "Sarpa (Serpent)", "Ardra": "Shwana (Dog)", "Punarvasu": "Marjara (Cat)", "Pushya": "Mesha (Sheep)", "Ashlesha": "Marjara (Cat)", "Magha": "Mushaka (Rat)", "Purva Phalguni": "Mushaka (Rat)", "Uttara Phalguni": "Go (Cow)", "Hasta": "Mahisha (Buffalo)", "Chitra": "Vyaghra (Tiger)", "Swati": "Mahisha (Buffalo)", "Vishakha": "Vyaghra (Tiger)", "Anuradha": "Mriga (Deer)", "Jyeshtha": "Mriga (Deer)", "Mula": "Shwana (Dog)", "Purva Ashadha": "Vanara (Monkey)", "Uttara Ashadha": "Nakula (Mongoose)", "Shravana": "Vanara (Monkey)", "Dhanishtha": "Simha (Lion)", "Shatabhisha": "Ashwa (Horse)", "Purva Bhadrapada": "Simha (Lion)", "Uttara Bhadrapada": "Go (Cow)", "Revati": "Gaja (Elephant)"}
# #     NAKSHATRA_LORD_MAP = {"Ashwini": "Ketu", "Magha": "Ketu", "Mula": "Ketu", "Bharani": "Venus", "Purva Phalguni": "Venus", "Purva Ashadha": "Venus", "Krittika": "Sun", "Uttara Phalguni": "Sun", "Uttara Ashadha": "Sun", "Rohini": "Moon", "Hasta": "Moon", "Shravana": "Moon", "Mrigashira": "Mars", "Chitra": "Mars", "Dhanishtha": "Mars", "Ardra": "Rahu", "Swati": "Rahu", "Shatabhisha": "Rahu", "Punarvasu": "Jupiter", "Vishakha": "Jupiter", "Purva Bhadrapada": "Jupiter", "Pushya": "Saturn", "Anuradha": "Saturn", "Uttara Bhadrapada": "Saturn", "Ashlesha": "Mercury", "Jyeshtha": "Mercury", "Revati": "Mercury"}
# #     VIMSOTTARI_DURATIONS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

# #     # Basic Details
# #     details['ayanamsa_name'] = "Lahiri"
# #     details['ayanamsa_value'] = format_dms(ayanamsa_val)
# #     details['sun_sign_indian'] = rasi_chart['planets']['Sun']['sign']
# #     details['sun_sign_western'] = tropical_sun_sign
# #     details['lagna'] = rasi_chart['ascendant']['sign']
# #     details['rasi'] = moon_sign
# #     details['varna'] = VARNA_MAP.get(moon_sign, "N/A")
# #     details['gana'] = GANA_MAP.get(moon_nakshatra, "N/A")
# #     details['nadi'] = NADI_MAP.get(moon_nakshatra, "N/A")
# #     details['yoni'] = YONI_MAP.get(moon_nakshatra, "N/A")
# #     details['lagna_lord'] = PLANET_RULERSHIPS.get(details['lagna'], "N/A")
# #     details['rasi_lord'] = PLANET_RULERSHIPS.get(details['rasi'], "N/A")
    
# #     if moon_sign == "Capricorn":
# #         moon_deg_in_sign = rasi_chart['planets']['Moon']['degree'] % 30
# #         details['vasya'] = "Jalachara (Water)" if moon_deg_in_sign < 15 else "Chatushpada (Quadruped)"
# #     else:
# #         details['vasya'] = VASYA_MAP.get(moon_sign, "N/A")

# #     # Nakshatra Details
# #     nakshatra_span = 13 + 1/3
# #     moon_lon_in_nakshatra = moon_lon - (panchanga['nakshatra_index'] * nakshatra_span)
# #     details['nakshatra_pada'] = math.floor(moon_lon_in_nakshatra / (nakshatra_span / 4)) + 1
# #     details['nakshatra_lord'] = NAKSHATRA_LORD_MAP.get(moon_nakshatra, "N/A")

# #     # PAYA CALCULATION
# #     PAYA_TABLE = [
# #         ["Gold", "Iron", "Copper", "Silver", "Gold", "Copper", "Iron"],
# #         ["Iron", "Silver", "Gold", "Iron", "Silver", "Gold", "Copper"],
# #         ["Silver", "Copper", "Iron", "Gold", "Copper", "Iron", "Gold"],
# #         ["Copper", "Gold", "Silver", "Copper", "Iron", "Silver", "Gold"]
# #     ]
# #     nakshatra_mod = panchanga['nakshatra_index'] % 4
# #     weekday_index = panchanga['weekday_index_for_paya']
# #     details['paya'] = PAYA_TABLE[nakshatra_mod][weekday_index]
            
# #     # Balance of Dasha
# #     dasha_lord = details['nakshatra_lord']
# #     total_dasha_period = VIMSOTTARI_DURATIONS.get(dasha_lord, 0)
# #     moon_remaining_in_nakshatra = nakshatra_span - moon_lon_in_nakshatra
# #     balance_decimal = (moon_remaining_in_nakshatra / nakshatra_span) * total_dasha_period
    
# #     years = int(balance_decimal)
# #     months = int((balance_decimal - years) * 12)
# #     days = int((((balance_decimal - years) * 12) - months) * 30.4375)
# #     details['balance_of_dasha'] = f"{dasha_lord}: {years}Y, {months}M, {days}D"
    
# #     return details

# # # --- Yogini Dasha Calculation Function ---
# # def calculate_yogini_dasha(birth_date_str, birth_time_str, nakshatra_index, moon_lon):
# #     # Determine the starting Yogini
# #     yogini_number = (nakshatra_index + 1 + 3) % 8
# #     if yogini_number == 0:
# #         yogini_number = 8
    
# #     start_yogini_index = yogini_number - 1
    
# #     # Calculate the balance of the first Dasha
# #     nakshatra_span = 13 + 1/3
# #     start_of_current_nakshatra = nakshatra_index * nakshatra_span
# #     moon_traversed_in_nakshatra = moon_lon - start_of_current_nakshatra
# #     moon_remaining_in_nakshatra = nakshatra_span - moon_traversed_in_nakshatra
    
# #     current_dasha_info = YOGINI_DASHAS[start_yogini_index]
# #     total_dasha_period_years = current_dasha_info["duration"]
    
# #     balance_decimal_years = (moon_remaining_in_nakshatra / nakshatra_span) * total_dasha_period_years
    
# #     years = int(balance_decimal_years)
# #     months = int((balance_decimal_years - years) * 12)
# #     days = int((((balance_decimal_years - years) * 12) - months) * 30.4375)
    
# #     balance_string = f"{current_dasha_info['yogini']} ({current_dasha_info['lord']}): {years}Y, {months}M, {days}D remaining"
    
# #     # Calculate the full Dasha sequence
# #     dasha_sequence = []
    
# #     time_format_str = "%Y-%m-%d %H:%M:%S" if len(birth_time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
# #     try:
# #         birth_dt = datetime.strptime(f"{birth_date_str} {birth_time_str}", time_format_str)
# #     except ValueError:
# #         birth_dt = datetime.strptime(f"{birth_date_str} {birth_time_str}:00", "%Y-%m-%d %H:%M:%S")

# #     # Calculate the end date of the first (balance) dasha
# #     end_date = birth_dt + timedelta(days=balance_decimal_years * 365.25)
# #     dasha_sequence.append({
# #         "yogini": current_dasha_info['yogini'],
# #         "lord": current_dasha_info['lord'],
# #         "start_date": birth_dt.strftime("%Y-%m-%d"),
# #         "end_date": end_date.strftime("%Y-%m-%d")
# #     })
    
# #     # Calculate subsequent dashas for one full cycle
# #     current_date = end_date
# #     for i in range(1, len(YOGINI_DASHAS)):
# #         yogini_index = (start_yogini_index + i) % 8
# #         dasha_info = YOGINI_DASHAS[yogini_index]
# #         start_date = current_date
# #         end_date = start_date + timedelta(days=dasha_info["duration"] * 365.25)
        
# #         dasha_sequence.append({
# #             "yogini": dasha_info['yogini'],
# #             "lord": dasha_info['lord'],
# #             "start_date": start_date.strftime("%Y-%m-%d"),
# #             "end_date": end_date.strftime("%Y-%m-%d")
# #         })
# #         current_date = end_date
        
# #     return balance_string, dasha_sequence


# # # --- Main Chart Calculation Wrapper ---
# # def get_rasi_chart(name, birth_date, birth_time, location_str, timezone_offset):
# #     lat, lon = get_coords(location_str)
# #     if lat is None: return None, None, None, None, None
# #     planets, ascendant, jd_ut, ayanamsa, tropical_sun_sign = calculate_planets_and_ascendant(birth_date, birth_time, lat, lon, timezone_offset)
# #     if planets is None: return None, None, None, None, None
# #     return {"name": name, "ascendant": ascendant, "planets": planets}, jd_ut, ayanamsa, tropical_sun_sign

# # # --- Main Execution Block ---
# # if __name__ == "__main__":
# #     print("--- Vedic Astrology Chart Generator ---")
# #     name = input("Enter Full Name: ")
# #     birth_date = input("Enter Birth Date (YYYY-MM-DD): ")
# #     birth_time = input("Enter Birth Time (HH:MM or HH:MM:SS in 24-hr format): ")
# #     birth_location = input("Enter Birth Location (e.g., 'Delhi, India'): ")

# #     lat_birth, lon_birth = get_coords(birth_location)
# #     if lat_birth is None: exit()
# #     print(f"\nGeocoded Birth Location: Latitude = {lat_birth:.4f}, Longitude = {lon_birth:.4f}")

# #     utc_offset_birth, tz_name_birth = get_timezone_info(lat_birth, lon_birth, birth_date, birth_time)

# #     rasi_chart, natal_jd_ut, ayanamsa_val, tropical_sun_sign = get_rasi_chart(name, birth_date, birth_time, birth_location, utc_offset_birth)
# #     if rasi_chart is None: exit()
    
# #     panchanga = calculate_panchanga(natal_jd_ut, birth_date)
# #     avakahada = calculate_avakahada_chakra(rasi_chart, panchanga, ayanamsa_val, tropical_sun_sign)
    
# #     # Calculate Yogini Dasha
# #     yogini_balance_str, yogini_dasha_sequence = calculate_yogini_dasha(
# #         birth_date, birth_time, panchanga['nakshatra_index'], panchanga['moon_lon']
# #     )

# #     # --- DEBUG SECTION FOR PAYA ---
# #     print("\n" + "!"*15 + " PAYA CALCULATION DEBUG " + "!"*15)
# #     print(f"--> Moon Sidereal Longitude : {panchanga['moon_lon']:.4f} degrees")
# #     print(f"--> Nakshatra Index (0-26)  : {panchanga['nakshatra_index']} ({panchanga['nakshatra']})")
# #     print(f"--> Weekday                   : {panchanga['weekday']}")
# #     print(f"--> Weekday Index (Sun=0)     : {panchanga['weekday_index_for_paya']}")
# #     print(f"--> Nakshatra Index % 4       : {panchanga['nakshatra_index'] % 4}  (This is the ROW in the table)")
# #     print(f"--> Paya Table[ROW][COLUMN]   : PAYA_TABLE[{panchanga['nakshatra_index'] % 4}][{panchanga['weekday_index_for_paya']}]")
# #     print(f"--> Final Paya Result         : {avakahada['paya']}")
# #     print("!" * 52)
    
# #     print("\n" + "=" * 60)
# #     print(f"🌟 Astrological Details for {name} 🌟")
# #     print("=" * 60)

# #     print("\n--- Planetary Positions (Lahiri Ayanamsa) ---")
# #     ascendant = rasi_chart['ascendant']
# #     print(f"Ascendant : {ascendant['sign']:<12} {format_dms(ascendant['degree'])}")
# #     display_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
# #     for planet_name in display_order:
# #         if planet_name in rasi_chart['planets']:
# #             planet_info = rasi_chart['planets'][planet_name]
# #             print(f"{planet_name:<9} : {planet_info['sign']:<12} {format_dms(planet_info['degree'])}")

# #     print("\n--- Birth Panchanga ---")
# #     print(f"Weekday     : {panchanga['weekday']}")
# #     print(f"Tithi       : {panchanga['tithi']}")
# #     print(f"Paksha      : {panchanga['paksha']}")
# #     print(f"Karana      : {panchanga['karana']}")
# #     print(f"Nakshatra   : {panchanga['nakshatra']}")
# #     print(f"Yoga        : {panchanga['yoga']}")

# #     print("\n--- Avakahada Chakra ---")
# #     print(f"Ayanamsa        : {avakahada['ayanamsa_name']} ({avakahada['ayanamsa_value']})")
# #     print(f"Sun Sign(Indian): {avakahada['sun_sign_indian']}")
# #     print(f"Sun Sign(Western):{avakahada['sun_sign_western']}")
# #     print(f"Lagna           : {avakahada['lagna']}")
# #     print(f"Lagna Lord      : {avakahada['lagna_lord']}")
# #     print(f"Rasi (Moon Sign): {avakahada['rasi']}")
# #     print(f"Rasi Lord       : {avakahada['rasi_lord']}")
# #     print(f"Nakshatra Lord  : {avakahada['nakshatra_lord']}")
# #     print(f"Nakshatra Pada  : {avakahada['nakshatra_pada']}")
# #     print(f"Dasha Balance   : {avakahada['balance_of_dasha']} remaining at birth")
# #     print(f"Paya (Leg)      : {avakahada['paya']}")
# #     print(f"Varna           : {avakahada['varna']} (Temperament)")
# #     print(f"Vasya           : {avakahada['vasya']} (Influence)")
# #     print(f"Yoni            : {avakahada['yoni']} (Animal Symbol)")
# #     print(f"Gana            : {avakahada['gana']} (Clan)")
# #     print(f"Nadi            : {avakahada['nadi']} (Constitution)")
    
# #     print("\n--- Yogini Dasha ---")
# #     print(f"Balance of Dasha at Birth: {yogini_balance_str}")
# #     print("\nYogini Dasha Periods:")
# #     for dasha in yogini_dasha_sequence:
# #         print(f"{dasha['yogini']:<10} ({dasha['lord']:<8}) : {dasha['start_date']} to {dasha['end_date']}")

# #     print("-" * 60)


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
#     # If you don't have Swiss Ephemeris files, this script may not be fully accurate.
#     # You can download them from https://www.astro.com/ftp/swisseph/ephe/
#     swe.set_ephe_path('C:/swiss/epeh')
# except swe.Error:
#     print("Warning: Swiss Ephemeris path not found. Calculations will use built-in ephemeris which is less accurate for older dates.")

# ZODIAC_SIGNS = [
#     "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
#     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
# ]

# PLANET_NAMES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]

# traditional_planet_ids = {
#     "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
#     "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN
# }
# outer_planet_ids = {
#     "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
# }

# # Panchanga Data
# TITHIS = [
#     "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", "Shukla Panchami",
#     "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami", "Shukla Navami", "Shukla Dashami",
#     "Shukla Ekadashi", "Shukla Dwadashi", "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
#     "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", "Krishna Panchami",
#     "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami", "Krishna Navami", "Krishna Dashami",
#     "Krishna Ekadashi", "Krishna Dwadashi", "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
# ]
# NAKSHATRAS = [
#     "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
#     "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
#     "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada",
#     "Uttara Bhadrapada", "Revati"
# ]
# YOGAS = [
#     "Vishkambha", "Priti", "Aayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarman", "Dhriti", "Shula",
#     "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
#     "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
# ]
# KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kintughna"]
# WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# # Planetary Data for Avakahada Chakra
# PLANET_RULERSHIPS = {
#     "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
#     "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
# }

# # --- Yogini Dasha Data ---
# YOGINI_DASHAS = [
#     {"yogini": "Mangala", "lord": "Moon", "duration": 1},
#     {"yogini": "Pingala", "lord": "Sun", "duration": 2},
#     {"yogini": "Dhanya", "lord": "Jupiter", "duration": 3},
#     {"yogini": "Bhramari", "lord": "Mars", "duration": 4},
#     {"yogini": "Bhadrika", "lord": "Mercury", "duration": 5},
#     {"yogini": "Ulka", "lord": "Saturn", "duration": 6},
#     {"yogini": "Siddha", "lord": "Venus", "duration": 7},
#     {"yogini": "Sankata", "lord": "Rahu", "duration": 8}
# ]


# # --- Helper Functions ---
# def get_coords(location_name):
#     try:
#         geolocator = Nominatim(user_agent="kundali_app_v15")
#         location = geolocator.geocode(location_name)
#         if location:
#             return location.latitude, location.longitude
#     except Exception as e:
#         print(f"Geocoding error: {e}")
#     return None, None

# def get_timezone_info(lat, lon, date_str, time_str):
#     tf = TimezoneFinder()
#     timezone_name = tf.timezone_at(lat=lat, lng=lon)
#     if not timezone_name:
#         print("Could not detect timezone. Defaulting to UTC.")
#         return 0.0, "UTC"
    
#     local_tz = pytz.timezone(timezone_name)
#     try:
#         time_format = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
#         naive_dt = datetime.strptime(f"{date_str} {time_str}", time_format)
#     except ValueError:
#         naive_dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")

#     local_dt = local_tz.localize(naive_dt)
#     return local_dt.utcoffset().total_seconds() / 3600.0, timezone_name

# def get_sign(degree):
#     return ZODIAC_SIGNS[int(degree // 30)]

# # --- NEW HELPER FUNCTION FOR CHARA DASHA ---
# def get_sign_index(sign_name):
#     """Gets the index of a sign from the ZODIAC_SIGNS list."""
#     try:
#         return ZODIAC_SIGNS.index(sign_name)
#     except ValueError:
#         return -1
# # ---------------------------------------------

# def format_dms(degree):
#     d = int(degree)
#     m = int((degree - d) * 60)
#     s = int(((degree - d) * 60 - m) * 60)
#     return f"{d:02d}° {m:02d}' {s:02d}\""

# # --- Core Calculation Functions ---

# def calculate_planets_and_ascendant(date_str, time_str, latitude, longitude, timezone_offset):
#     time_format_str = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
#     try:
#         dt = datetime.strptime(f"{date_str} {time_str}", time_format_str)
#     except ValueError:
#         dt = datetime.strptime(f"{date_str} {time_str}:00", "%Y-%m-%d %H:%M:%S")

#     utc_dt = dt - timedelta(hours=timezone_offset)
#     jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

#     swe.set_sid_mode(swe.SIDM_LAHIRI)
#     ayanamsa = swe.get_ayanamsa_ut(jd_ut)

#     _, ascmc = swe.houses(jd_ut, latitude, longitude, b'P')
#     ascendant_degree = (ascmc[0] - ayanamsa) % 360

#     planets = {}
#     tropical_sun_sign = ""
#     all_planet_ids = {**traditional_planet_ids, **outer_planet_ids}
#     for planet_name, planet_id in all_planet_ids.items():
#         xx, _ = swe.calc_ut(jd_ut, planet_id)
#         if planet_name == "Sun":
#             tropical_sun_sign = get_sign(xx[0])
#         sidereal_lon = (xx[0] - ayanamsa) % 360
#         planets[planet_name] = {"degree": sidereal_lon, "sign": get_sign(sidereal_lon)}

#     rahu_xx, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
#     rahu_lon = (rahu_xx[0] - ayanamsa) % 360
#     planets["Rahu"] = {"degree": rahu_lon, "sign": get_sign(rahu_lon)}
#     planets["Ketu"] = {"degree": (rahu_lon + 180) % 360, "sign": get_sign((rahu_lon + 180) % 360)}

#     return planets, {"degree": ascendant_degree, "sign": get_sign(ascendant_degree)}, jd_ut, ayanamsa, tropical_sun_sign


# def calculate_panchanga(jd_ut, birth_date_str):
#     swe.set_sid_mode(swe.SIDM_LAHIRI)
#     ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    
#     sun_data, _ = swe.calc_ut(jd_ut, swe.SUN)
#     moon_data, _ = swe.calc_ut(jd_ut, swe.MOON)

#     sun_lon = (sun_data[0] - ayanamsa) % 360
#     moon_lon = (moon_data[0] - ayanamsa) % 360

#     tithi_lon = (moon_lon - sun_lon + 360) % 360
#     tithi_index = int(tithi_lon / 12)
#     paksha = "Shukla Paksha" if tithi_index < 15 else "Krishna Paksha"
    
#     karana_num = int(tithi_lon / 6)
#     if karana_num == 0: karana_index = 10 
#     elif karana_num < 8: karana_index = karana_num - 1
#     elif karana_num > 56: karana_index = karana_num - 50
#     else: karana_index = ((karana_num - 1) % 7)

#     nakshatra_span = 13 + 1/3
#     nakshatra_index = int(moon_lon / nakshatra_span)
    
#     yoga_lon = (sun_lon + moon_lon) % 360
#     yoga_index = int(yoga_lon / (13 + 1/3))
    
#     birth_dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
#     weekday = WEEKDAYS[birth_dt.weekday()]
#     weekday_index_for_paya = (birth_dt.weekday() + 1) % 7
    
#     return {
#         "moon_lon": moon_lon, # Pass moon longitude for debugging
#         "tithi": TITHIS[tithi_index], "paksha": paksha, "karana": KARANAS[karana_index],
#         "nakshatra": NAKSHATRAS[nakshatra_index], "nakshatra_index": nakshatra_index,
#         "yoga": YOGAS[yoga_index], "weekday": weekday, "weekday_index_for_paya": weekday_index_for_paya
#     }

# def calculate_avakahada_chakra(rasi_chart, panchanga, ayanamsa_val, tropical_sun_sign):
#     details = {}
#     moon_sign = rasi_chart['planets']['Moon']['sign']
#     moon_lon = rasi_chart['planets']['Moon']['degree']
#     moon_nakshatra = panchanga['nakshatra']
    
#     # Mappings
#     VARNA_MAP = {"Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin", "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya", "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya", "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra"}
#     VASYA_MAP = {"Aries": "Chatushpada", "Taurus": "Chatushpada", "Leo": "Chatushpada", "Gemini": "Manava", "Virgo": "Manava", "Libra": "Manava", "Sagittarius": "Manava", "Aquarius": "Manava", "Cancer": "Jalachara", "Pisces": "Jalachara", "Scorpio": "Keeta"}
#     GANA_MAP = {"Ashwini": "Deva", "Mrigashira": "Deva", "Punarvasu": "Deva", "Pushya": "Deva", "Hasta": "Deva", "Swati": "Deva", "Anuradha": "Deva", "Shravana": "Deva", "Revati": "Deva", "Bharani": "Manushya", "Rohini": "Manushya", "Ardra": "Manushya", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya", "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Krittika": "Rakshasa", "Ashlesha": "Rakshasa", "Magha": "Rakshasa", "Chitra": "Rakshasa", "Vishakha": "Rakshasa", "Jyeshtha": "Rakshasa", "Mula": "Rakshasa", "Dhanishtha": "Rakshasa", "Shatabhisha": "Rakshasa"}
#     NADI_MAP = {"Ashwini": "Adi", "Ardra": "Adi", "Punarvasu": "Adi", "Uttara Phalguni": "Adi", "Hasta": "Adi", "Jyeshtha": "Adi", "Mula": "Adi", "Shatabhisha": "Adi", "Purva Bhadrapada": "Adi", "Bharani": "Madhya", "Mrigashira": "Madhya", "Pushya": "Madhya", "Purva Phalguni": "Madhya", "Chitra": "Madhya", "Anuradha": "Madhya", "Purva Ashadha": "Madhya", "Dhanishtha": "Madhya", "Uttara Bhadrapada": "Madhya", "Krittika": "Antya", "Rohini": "Antya", "Ashlesha": "Antya", "Magha": "Antya", "Swati": "Antya", "Vishakha": "Antya", "Uttara Ashadha": "Antya", "Shravana": "Antya", "Revati": "Antya"}
#     YONI_MAP = {"Ashwini": "Ashwa (Horse)", "Bharani": "Gaja (Elephant)", "Krittika": "Mesha (Sheep)", "Rohini": "Sarpa (Serpent)", "Mrigashira": "Sarpa (Serpent)", "Ardra": "Shwana (Dog)", "Punarvasu": "Marjara (Cat)", "Pushya": "Mesha (Sheep)", "Ashlesha": "Marjara (Cat)", "Magha": "Mushaka (Rat)", "Purva Phalguni": "Mushaka (Rat)", "Uttara Phalguni": "Go (Cow)", "Hasta": "Mahisha (Buffalo)", "Chitra": "Vyaghra (Tiger)", "Swati": "Mahisha (Buffalo)", "Vishakha": "Vyaghra (Tiger)", "Anuradha": "Mriga (Deer)", "Jyeshtha": "Mriga (Deer)", "Mula": "Shwana (Dog)", "Purva Ashadha": "Vanara (Monkey)", "Uttara Ashadha": "Nakula (Mongoose)", "Shravana": "Vanara (Monkey)", "Dhanishtha": "Simha (Lion)", "Shatabhisha": "Ashwa (Horse)", "Purva Bhadrapada": "Simha (Lion)", "Uttara Bhadrapada": "Go (Cow)", "Revati": "Gaja (Elephant)"}
#     NAKSHATRA_LORD_MAP = {"Ashwini": "Ketu", "Magha": "Ketu", "Mula": "Ketu", "Bharani": "Venus", "Purva Phalguni": "Venus", "Purva Ashadha": "Venus", "Krittika": "Sun", "Uttara Phalguni": "Sun", "Uttara Ashadha": "Sun", "Rohini": "Moon", "Hasta": "Moon", "Shravana": "Moon", "Mrigashira": "Mars", "Chitra": "Mars", "Dhanishtha": "Mars", "Ardra": "Rahu", "Swati": "Rahu", "Shatabhisha": "Rahu", "Punarvasu": "Jupiter", "Vishakha": "Jupiter", "Purva Bhadrapada": "Jupiter", "Pushya": "Saturn", "Anuradha": "Saturn", "Uttara Bhadrapada": "Saturn", "Ashlesha": "Mercury", "Jyeshtha": "Mercury", "Revati": "Mercury"}
#     VIMSOTTARI_DURATIONS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

#     # Basic Details
#     details['ayanamsa_name'] = "Lahiri"
#     details['ayanamsa_value'] = format_dms(ayanamsa_val)
#     details['sun_sign_indian'] = rasi_chart['planets']['Sun']['sign']
#     details['sun_sign_western'] = tropical_sun_sign
#     details['lagna'] = rasi_chart['ascendant']['sign']
#     details['rasi'] = moon_sign
#     details['varna'] = VARNA_MAP.get(moon_sign, "N/A")
#     details['gana'] = GANA_MAP.get(moon_nakshatra, "N/A")
#     details['nadi'] = NADI_MAP.get(moon_nakshatra, "N/A")
#     details['yoni'] = YONI_MAP.get(moon_nakshatra, "N/A")
#     details['lagna_lord'] = PLANET_RULERSHIPS.get(details['lagna'], "N/A")
#     details['rasi_lord'] = PLANET_RULERSHIPS.get(details['rasi'], "N/A")
    
#     if moon_sign == "Capricorn":
#         moon_deg_in_sign = rasi_chart['planets']['Moon']['degree'] % 30
#         details['vasya'] = "Jalachara (Water)" if moon_deg_in_sign < 15 else "Chatushpada (Quadruped)"
#     else:
#         details['vasya'] = VASYA_MAP.get(moon_sign, "N/A")

#     # Nakshatra Details
#     nakshatra_span = 13 + 1/3
#     moon_lon_in_nakshatra = moon_lon - (panchanga['nakshatra_index'] * nakshatra_span)
#     details['nakshatra_pada'] = math.floor(moon_lon_in_nakshatra / (nakshatra_span / 4)) + 1
#     details['nakshatra_lord'] = NAKSHATRA_LORD_MAP.get(moon_nakshatra, "N/A")

#     # PAYA CALCULATION
#     PAYA_TABLE = [
#         ["Gold", "Iron", "Copper", "Silver", "Gold", "Copper", "Iron"],
#         ["Iron", "Silver", "Gold", "Iron", "Silver", "Gold", "Copper"],
#         ["Silver", "Copper", "Iron", "Gold", "Copper", "Iron", "Gold"],
#         ["Copper", "Gold", "Silver", "Copper", "Iron", "Silver", "Gold"]
#     ]
#     nakshatra_mod = panchanga['nakshatra_index'] % 4
#     weekday_index = panchanga['weekday_index_for_paya']
#     details['paya'] = PAYA_TABLE[nakshatra_mod][weekday_index]
            
#     # Balance of Dasha
#     dasha_lord = details['nakshatra_lord']
#     total_dasha_period = VIMSOTTARI_DURATIONS.get(dasha_lord, 0)
#     moon_remaining_in_nakshatra = nakshatra_span - moon_lon_in_nakshatra
#     balance_decimal = (moon_remaining_in_nakshatra / nakshatra_span) * total_dasha_period
    
#     years = int(balance_decimal)
#     months = int((balance_decimal - years) * 12)
#     days = int((((balance_decimal - years) * 12) - months) * 30.4375)
#     details['balance_of_dasha'] = f"{dasha_lord}: {years}Y, {months}M, {days}D"
    
#     return details

# # --- Yogini Dasha Calculation Function ---
# def calculate_yogini_dasha(birth_date_str, birth_time_str, nakshatra_index, moon_lon):
#     # Determine the starting Yogini
#     yogini_number = (nakshatra_index + 1 + 3) % 8
#     if yogini_number == 0:
#         yogini_number = 8
    
#     start_yogini_index = yogini_number - 1
    
#     # Calculate the balance of the first Dasha
#     nakshatra_span = 13 + 1/3
#     start_of_current_nakshatra = nakshatra_index * nakshatra_span
#     moon_traversed_in_nakshatra = moon_lon - start_of_current_nakshatra
#     moon_remaining_in_nakshatra = nakshatra_span - moon_traversed_in_nakshatra
    
#     current_dasha_info = YOGINI_DASHAS[start_yogini_index]
#     total_dasha_period_years = current_dasha_info["duration"]
    
#     balance_decimal_years = (moon_remaining_in_nakshatra / nakshatra_span) * total_dasha_period_years
    
#     years = int(balance_decimal_years)
#     months = int((balance_decimal_years - years) * 12)
#     days = int((((balance_decimal_years - years) * 12) - months) * 30.4375)
    
#     balance_string = f"{current_dasha_info['yogini']} ({current_dasha_info['lord']}): {years}Y, {months}M, {days}D remaining"
    
#     # Calculate the full Dasha sequence
#     dasha_sequence = []
    
#     time_format_str = "%Y-%m-%d %H:%M:%S" if len(birth_time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
#     try:
#         birth_dt = datetime.strptime(f"{birth_date_str} {birth_time_str}", time_format_str)
#     except ValueError:
#         birth_dt = datetime.strptime(f"{birth_date_str} {birth_time_str}:00", "%Y-%m-%d %H:%M:%S")

#     # Calculate the end date of the first (balance) dasha
#     end_date = birth_dt + timedelta(days=balance_decimal_years * 365.25)
#     dasha_sequence.append({
#         "yogini": current_dasha_info['yogini'],
#         "lord": current_dasha_info['lord'],
#         "start_date": birth_dt.strftime("%Y-%m-%d"),
#         "end_date": end_date.strftime("%Y-%m-%d")
#     })
    
#     # Calculate subsequent dashas for one full cycle
#     current_date = end_date
#     for i in range(1, len(YOGINI_DASHAS)):
#         yogini_index = (start_yogini_index + i) % 8
#         dasha_info = YOGINI_DASHAS[yogini_index]
#         start_date = current_date
#         end_date = start_date + timedelta(days=dasha_info["duration"] * 365.25)
        
#         dasha_sequence.append({
#             "yogini": dasha_info['yogini'],
#             "lord": dasha_info['lord'],
#             "start_date": start_date.strftime("%Y-%m-%d"),
#             "end_date": end_date.strftime("%Y-%m-%d")
#         })
#         current_date = end_date
        
#     return balance_string, dasha_sequence

# # --- NEW CHARA DASHA CALCULATION FUNCTION ---
# def calculate_chara_dasha(rasi_chart, birth_date_str, birth_time_str):
#     """
#     Calculates the Jaimini Chara Dasha (Mahadasha and Antardasha).

#     Args:
#         rasi_chart: The dictionary containing the planetary and ascendant details.
#         birth_date_str: The birth date string in 'YYYY-MM-DD' format.
#         birth_time_str: The birth time string.

#     Returns:
#         A list of dictionaries, where each dictionary represents a Mahadasha
#         period and contains its Antardasha sequence.
#     """
#     # Jaimini Sutras rule for Dasha sequence direction
#     lagna_sign_index = get_sign_index(rasi_chart['ascendant']['sign'])
#     ninth_house_sign_index = (lagna_sign_index + 8) % 12
#     ninth_house_sign = ZODIAC_SIGNS[ninth_house_sign_index]

#     # Odd-footed signs (Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius) lead to forward counting.
#     # Even-footed signs (Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces) lead to backward counting.
#     forward_signs = ["Aries", "Taurus", "Gemini", "Libra", "Scorpio", "Sagittarius"]
#     dasha_sequence_is_forward = ninth_house_sign in forward_signs

#     # Determine the sequence of Mahadasha signs
#     dasha_signs = []
#     if dasha_sequence_is_forward:
#         for i in range(12):
#             dasha_signs.append(ZODIAC_SIGNS[(lagna_sign_index + i) % 12])
#     else:
#         for i in range(12):
#             dasha_signs.append(ZODIAC_SIGNS[(lagna_sign_index - i + 12) % 12])

#     chara_dasha_periods = []
#     planets = rasi_chart['planets']

#     for sign in dasha_signs:
#         sign_index = get_sign_index(sign)
#         lord = PLANET_RULERSHIPS[sign]
        
#         # Special considerations for Scorpio and Aquarius lords
#         if sign == "Scorpio":
#             mars_pos = get_sign_index(planets['Mars']['sign'])
#             ketu_pos = get_sign_index(planets['Ketu']['sign'])
#             # A more complex rule exists for choosing between Mars and Ketu, 
#             # but for simplicity, we'll prefer Mars. A more advanced implementation
#             # would compare their strengths.
#             lord_pos = mars_pos
#         elif sign == "Aquarius":
#             saturn_pos = get_sign_index(planets['Saturn']['sign'])
#             rahu_pos = get_sign_index(planets['Rahu']['sign'])
#             # Similar to Scorpio, we'll prefer Saturn for simplicity.
#             lord_pos = saturn_pos
#         else:
#             lord_pos = get_sign_index(planets[lord]['sign'])

#         # Calculate Dasha duration
#         if lord_pos == sign_index: # Lord in its own sign
#             dasha_years = 12
#         else:
#             # Counting is always forward from the sign to its lord
#             if lord_pos >= sign_index:
#                 dasha_years = lord_pos - sign_index
#             else:
#                 dasha_years = lord_pos - sign_index + 12
        
#         chara_dasha_periods.append({'sign': sign, 'duration': dasha_years})

#     # Calculate Mahadasha and Antardasha start and end dates
#     time_format_str = "%Y-%m-%d %H:%M:%S" if len(birth_time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
#     try:
#         current_date = datetime.strptime(f"{birth_date_str} {birth_time_str}", time_format_str)
#     except ValueError:
#         current_date = datetime.strptime(f"{birth_date_str} {birth_time_str}:00", "%Y-%m-%d %H:%M:%S")

#     full_dasha_sequence = []
#     for i in range(len(chara_dasha_periods)):
#         mahadasha = chara_dasha_periods[i]
#         start_date = current_date
#         end_date = start_date + timedelta(days=mahadasha['duration'] * 365.25)
#         mahadasha_period = {
#             "mahadasha_sign": mahadasha['sign'],
#             "start_date": start_date.strftime("%Y-%m-%d"),
#             "end_date": end_date.strftime("%Y-%m-%d"),
#             "antardashas": []
#         }

#         # Calculate Antardashas
#         antardasha_start_date = start_date
#         antardasha_signs = []
#         mahadasha_sign_index = get_sign_index(mahadasha['sign'])

#         # The Antardasha sequence follows the same direction as the Mahadasha sequence
#         if dasha_sequence_is_forward:
#             for j in range(12):
#                 antardasha_signs.append(ZODIAC_SIGNS[(mahadasha_sign_index + j) % 12])
#         else:
#             for j in range(12):
#                 antardasha_signs.append(ZODIAC_SIGNS[(mahadasha_sign_index - j + 12) % 12])
        
#         for ad_sign in antardasha_signs:
#             # The duration of the Antardasha is proportional to its own Mahadasha length
#             antardasha_duration_years = next((item for item in chara_dasha_periods if item["sign"] == ad_sign), None)['duration']
            
#             if mahadasha['duration'] == 0:
#                 ad_duration_days = 0
#             else:
#                 ad_duration_days = (antardasha_duration_years / 12) * (mahadasha['duration'] * 365.25 / 12) * 12 # Simplified calculation
            
#             # A more precise calculation for Antardasha period
#             total_days_in_mahadasha = (end_date - start_date).days
#             antardasha_duration_days = (antardasha_duration_years / 12) * total_days_in_mahadasha / (sum(p['duration'] for p in chara_dasha_periods)/12) # This is a common interpretation

#             # A simpler, more common approach: Duration of AD = (MD years * AD years) / 12 months -> converting to days
#             # This is complex. Let's use a proportional approach based on years.
#             total_mahadasha_days = mahadasha['duration'] * 365.25
#             antardasha_days = (total_mahadasha_days / 12) * (antardasha_duration_years / 12) * 12 # This simplifies to MD_days * AD_years / 12
#             antardasha_days_final = (mahadasha['duration'] * 365.25 / 12) * antardasha_duration_years

#             antardasha_end_date = antardasha_start_date + timedelta(days=antardasha_days_final)

#             mahadasha_period["antardashas"].append({
#                 "antardasha_sign": ad_sign,
#                 "start_date": antardasha_start_date.strftime("%Y-%m-%d"),
#                 "end_date": antardasha_end_date.strftime("%Y-%m-%d")
#             })
#             antardasha_start_date = antardasha_end_date

#         # Correct the end date of the last antardasha to match the mahadasha's end date
#         if mahadasha_period["antardashas"]:
#             mahadasha_period["antardashas"][-1]["end_date"] = mahadasha_period["end_date"]

#         full_dasha_sequence.append(mahadasha_period)
#         current_date = end_date
    
#     return full_dasha_sequence
# # ---------------------------------------------


# # --- Main Chart Calculation Wrapper ---
# def get_rasi_chart(name, birth_date, birth_time, location_str, timezone_offset):
#     lat, lon = get_coords(location_str)
#     if lat is None: return None, None, None, None, None
#     planets, ascendant, jd_ut, ayanamsa, tropical_sun_sign = calculate_planets_and_ascendant(birth_date, birth_time, lat, lon, timezone_offset)
#     if planets is None: return None, None, None, None, None
#     return {"name": name, "ascendant": ascendant, "planets": planets}, jd_ut, ayanamsa, tropical_sun_sign

# # --- Main Execution Block ---
# if __name__ == "__main__":
#     print("--- Vedic Astrology Chart Generator ---")
#     name = input("Enter Full Name: ")
#     birth_date = input("Enter Birth Date (YYYY-MM-DD): ")
#     birth_time = input("Enter Birth Time (HH:MM or HH:MM:SS in 24-hr format): ")
#     birth_location = input("Enter Birth Location (e.g., 'Delhi, India'): ")

#     lat_birth, lon_birth = get_coords(birth_location)
#     if lat_birth is None: exit()
#     print(f"\nGeocoded Birth Location: Latitude = {lat_birth:.4f}, Longitude = {lon_birth:.4f}")

#     utc_offset_birth, tz_name_birth = get_timezone_info(lat_birth, lon_birth, birth_date, birth_time)

#     rasi_chart, natal_jd_ut, ayanamsa_val, tropical_sun_sign = get_rasi_chart(name, birth_date, birth_time, birth_location, utc_offset_birth)
#     if rasi_chart is None: exit()
    
#     panchanga = calculate_panchanga(natal_jd_ut, birth_date)
#     avakahada = calculate_avakahada_chakra(rasi_chart, panchanga, ayanamsa_val, tropical_sun_sign)
    
#     # Calculate Yogini Dasha
#     yogini_balance_str, yogini_dasha_sequence = calculate_yogini_dasha(
#         birth_date, birth_time, panchanga['nakshatra_index'], panchanga['moon_lon']
#     )
    
#     # --- MODIFICATION: CALCULATE CHARA DASHA ---
#     chara_dasha_sequence = calculate_chara_dasha(rasi_chart, birth_date, birth_time)
#     # -------------------------------------------

#     # --- DEBUG SECTION FOR PAYA ---
#     print("\n" + "!"*15 + " PAYA CALCULATION DEBUG " + "!"*15)
#     print(f"--> Moon Sidereal Longitude : {panchanga['moon_lon']:.4f} degrees")
#     print(f"--> Nakshatra Index (0-26)  : {panchanga['nakshatra_index']} ({panchanga['nakshatra']})")
#     print(f"--> Weekday                 : {panchanga['weekday']}")
#     print(f"--> Weekday Index (Sun=0)   : {panchanga['weekday_index_for_paya']}")
#     print(f"--> Nakshatra Index % 4     : {panchanga['nakshatra_index'] % 4}  (This is the ROW in the table)")
#     print(f"--> Paya Table[ROW][COLUMN] : PAYA_TABLE[{panchanga['nakshatra_index'] % 4}][{panchanga['weekday_index_for_paya']}]")
#     print(f"--> Final Paya Result       : {avakahada['paya']}")
#     print("!" * 52)
    
#     print("\n" + "=" * 60)
#     print(f"🌟 Astrological Details for {name} 🌟")
#     print("=" * 60)

#     print("\n--- Planetary Positions (Lahiri Ayanamsa) ---")
#     ascendant = rasi_chart['ascendant']
#     print(f"Ascendant : {ascendant['sign']:<12} {format_dms(ascendant['degree'])}")
#     display_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
#     for planet_name in display_order:
#         if planet_name in rasi_chart['planets']:
#             planet_info = rasi_chart['planets'][planet_name]
#             print(f"{planet_name:<9} : {planet_info['sign']:<12} {format_dms(planet_info['degree'])}")

#     print("\n--- Birth Panchanga ---")
#     print(f"Weekday     : {panchanga['weekday']}")
#     print(f"Tithi       : {panchanga['tithi']}")
#     print(f"Paksha      : {panchanga['paksha']}")
#     print(f"Karana      : {panchanga['karana']}")
#     print(f"Nakshatra   : {panchanga['nakshatra']}")
#     print(f"Yoga        : {panchanga['yoga']}")

#     print("\n--- Avakahada Chakra ---")
#     print(f"Ayanamsa        : {avakahada['ayanamsa_name']} ({avakahada['ayanamsa_value']})")
#     print(f"Sun Sign(Indian): {avakahada['sun_sign_indian']}")
#     print(f"Sun Sign(Western):{avakahada['sun_sign_western']}")
#     print(f"Lagna           : {avakahada['lagna']}")
#     print(f"Lagna Lord      : {avakahada['lagna_lord']}")
#     print(f"Rasi (Moon Sign): {avakahada['rasi']}")
#     print(f"Rasi Lord       : {avakahada['rasi_lord']}")
#     print(f"Nakshatra Lord  : {avakahada['nakshatra_lord']}")
#     print(f"Nakshatra Pada  : {avakahada['nakshatra_pada']}")
#     print(f"Dasha Balance   : {avakahada['balance_of_dasha']} remaining at birth")
#     print(f"Paya (Leg)      : {avakahada['paya']}")
#     print(f"Varna           : {avakahada['varna']} (Temperament)")
#     print(f"Vasya           : {avakahada['vasya']} (Influence)")
#     print(f"Yoni            : {avakahada['yoni']} (Animal Symbol)")
#     print(f"Gana            : {avakahada['gana']} (Clan)")
#     print(f"Nadi            : {avakahada['nadi']} (Constitution)")
    
#     print("\n--- Yogini Dasha ---")
#     print(f"Balance of Dasha at Birth: {yogini_balance_str}")
#     print("\nYogini Dasha Periods:")
#     for dasha in yogini_dasha_sequence:
#         print(f"{dasha['yogini']:<10} ({dasha['lord']:<8}) : {dasha['start_date']} to {dasha['end_date']}")
    
#     # --- MODIFICATION: DISPLAY CHARA DASHA RESULTS ---
#     print("\n--- Chara Dasha (Jaimini) ---")
#     # Displaying the first cycle (12 Mahadashas)
#     for mahadasha in chara_dasha_sequence[:12]: 
#         print(f"\n**Mahadasha of {mahadasha['mahadasha_sign']} ({mahadasha['start_date']} to {mahadasha['end_date']})**")
#         for antardasha in mahadasha['antardashas']:
#             print(f"  - Antardasha of {antardasha['antardasha_sign']:<12}: {antardasha['start_date']} to {antardasha['end_date']}")
#     # ------------------------------------------------

#     print("-" * 60)

oo