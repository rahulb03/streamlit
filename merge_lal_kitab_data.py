"""
Script to merge and complete lal_kitab_data.txt from data.md
Adds missing Sun data and any missing houses for other planets
"""

import json
import re

def parse_data_md(filename="data.md"):
    """Parse the data.md file which contains JSON-like structure"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the JSON part (starts with { and ends with })
    # The data starts around line 1
    json_match = re.search(r'\{.*?\n\}', content, re.DOTALL)
    
    if not json_match:
        print("Could not find JSON structure in data.md")
        return None
    
    json_str = json_match.group(0)
    
    try:
        data = json.loads(json_str)
        print(f"✓ Parsed JSON data from data.md")
        return data
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error: {e}")
        return None

def parse_sun_data_from_md(filename="data.md"):
    """Parse Sun data that appears after the main JSON (lines 355+)"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sun_data = {}
    current_house = None
    current_prediction = ""
    current_remedy = ""
    in_prediction = False
    in_remedy = False
    
    for i, line in enumerate(lines[354:], start=355):  # Start from line 355
        line = line.strip()
        
        # Match house number
        if re.match(r'^\d+:\s*\{', line):
            # Save previous house if exists
            if current_house and (current_prediction or current_remedy):
                sun_data[str(current_house)] = {
                    "prediction": current_prediction.strip(),
                    "remedy": current_remedy.strip()
                }
            
            # Start new house
            current_house = int(line.split(':')[0])
            current_prediction = ""
            current_remedy = ""
            in_prediction = False
            in_remedy = False
            
        elif '"prediction":' in line:
            in_prediction = True
            in_remedy = False
            # Extract prediction text
            pred_match = re.search(r'"prediction":\s*"([^"]*)', line)
            if pred_match:
                current_prediction = pred_match.group(1)
                
        elif '"remedy":' in line:
            in_prediction = False
            in_remedy = True
            # Extract remedy text
            remedy_match = re.search(r'"remedy":\s*"([^"]*)', line)
            if remedy_match:
                current_remedy = remedy_match.group(1)
                
        elif in_prediction and line.startswith('"'):
            # Continue collecting prediction
            current_prediction += " " + line.strip(' ",')
            
        elif in_remedy and line.startswith('"'):
            # Continue collecting remedy
            current_remedy += " " + line.strip(' ",')
            
        elif line == '},' or line == '}':
            # End of house
            if current_house and (current_prediction or current_remedy):
                sun_data[str(current_house)] = {
                    "prediction": current_prediction.strip(),
                    "remedy": current_remedy.strip()
                }
            in_prediction = False
            in_remedy = False
        
        # Stop if we've found the Moon section (which indicates Sun section is over)
        if '"Moon":' in line:
            break
    
    if sun_data:
        print(f"✓ Parsed Sun data: {len(sun_data)} houses")
    
    return {"Sun": sun_data}

def load_existing_data(filename="lal_kitab_data.txt"):
    """Load existing data from lal_kitab_data.txt"""
    existing_data = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by ---
        entries = content.split('---')
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            lines = entry.split('\n')
            planet = None
            house = None
            prediction = None
            remedy = None
            
            for line in lines:
                if line.startswith('Planet:'):
                    planet = line.split(':', 1)[1].strip()
                elif line.startswith('House:'):
                    house = line.split(':', 1)[1].strip()
                elif line.startswith('Prediction:'):
                    prediction = line.split(':', 1)[1].strip()
                elif line.startswith('Remedy:'):
                    remedy = line.split(':', 1)[1].strip()
            
            if planet and house and (prediction or remedy):
                if planet not in existing_data:
                    existing_data[planet] = {}
                existing_data[planet][house] = {
                    "prediction": prediction or "",
                    "remedy": remedy or ""
                }
        
        print(f"✓ Loaded existing data: {sum(len(h) for h in existing_data.values())} entries")
        return existing_data
        
    except FileNotFoundError:
        print("✗ lal_kitab_data.txt not found")
        return {}

def merge_data(existing_data, new_data):
    """Merge new data with existing data, preferring existing where conflicts occur"""
    merged = existing_data.copy()
    
    for planet, houses in new_data.items():
        if planet not in merged:
            merged[planet] = {}
        
        for house, data in houses.items():
            if house not in merged[planet]:
                # Add missing house
                merged[planet][house] = data
                print(f"  + Added {planet} House {house}")
    
    return merged

def save_data(data, filename="lal_kitab_data.txt"):
    """Save merged data to lal_kitab_data.txt"""
    with open(filename, 'w', encoding='utf-8') as f:
        # Sort planets to have Sun first, then alphabetically
        planet_order = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        sorted_planets = sorted(data.keys(), key=lambda x: planet_order.index(x) if x in planet_order else 999)
        
        for planet in sorted_planets:
            houses = data[planet]
            # Sort houses numerically
            for house_num in sorted(houses.keys(), key=lambda x: int(x)):
                house_data = houses[house_num]
                f.write(f"Planet: {planet}\n")
                f.write(f"House: {house_num}\n")
                f.write(f"Prediction: {house_data['prediction']}\n")
                f.write(f"Remedy: {house_data['remedy']}\n")
                f.write("---\n")
    
    total_entries = sum(len(h) for h in data.values())
    print(f"\n✓ Saved {total_entries} entries to {filename}")

def main():
    print("=" * 80)
    print("LAL KITAB DATA MERGER")
    print("=" * 80)
    print("\nThis script will:")
    print("1. Load existing data from lal_kitab_data.txt")
    print("2. Parse complete data from data.md")
    print("3. Add missing Sun data and any missing houses")
    print("4. Save the complete dataset")
    print("=" * 80)
    
    # Load existing data
    print("\n[1/4] Loading existing data...")
    existing_data = load_existing_data()
    
    # Parse data.md JSON
    print("\n[2/4] Parsing data.md...")
    new_data = parse_data_md()
    
    # Parse Sun data separately
    print("\n[3/4] Parsing Sun data...")
    sun_data = parse_sun_data_from_md()
    
    if sun_data:
        # Merge Sun data into new_data
        if new_data is None:
            new_data = sun_data
        else:
            new_data.update(sun_data)
    
    if not new_data:
        print("\n✗ Could not parse data from data.md")
        return
    
    # Merge datasets
    print("\n[4/4] Merging data...")
    merged_data = merge_data(existing_data, new_data)
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    planet_order = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    for planet in planet_order:
        if planet in merged_data:
            count = len(merged_data[planet])
            status = "✓ Complete" if count == 12 else f"⚠ {count}/12 houses"
            print(f"{planet:10s}: {status}")
    
    total = sum(len(h) for h in merged_data.values())
    print("=" * 80)
    print(f"Total entries: {total}")
    print("=" * 80)
    
    # Save
    print("\nSaving merged data...")
    save_data(merged_data)
    
    print("\n" + "=" * 80)
    print("✓ MERGE COMPLETE!")
    print("=" * 80)
    print("\nThe file lal_kitab_data.txt now contains:")
    print("- All complete planet data from data.md")
    print("- Sun data for all 12 houses")
    print("- All existing data from your current file")
    print("\nYou can now use allchart.py to see complete predictions!")
    print("=" * 80)

if __name__ == "__main__":
    main()
