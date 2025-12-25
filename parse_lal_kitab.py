"""
Parse Lal Kitab data from data.md and convert it to the format needed by lal_kitab_predictor.py
"""

import re
import json

def parse_lal_kitab_data():
    """Parse the data.md file and extract planet-house combinations"""
    
    with open('data.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Planet names mapping
    planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    
    # Dictionary to store parsed data
    predictions = []
    
    # Parse each planet's section
    for planet in planets:
        print(f"\nProcessing {planet}...")
        
        # Find sections for each house (1-12)
        for house in range(1, 13):
            # Try different pattern variations
            patterns = [
                f'{planet.lower()}_in_{house}(?:st|nd|rd|th)?_house',
                f'{planet.lower()}_{house}(?:st|nd|rd|th)?_house',
                f'{planet.lower()}_in_{house}',
            ]
            
            prediction_text = []
            remedy_text = []
            
            # Search for the planet-house combination
            for pattern in patterns:
                # Find all matches for benefic/effects/descriptions
                benefic_pattern = f'"{pattern}_(?:benefic|benefit|effect|description)[^"]*":"([^"]+)"'
                matches = re.findall(benefic_pattern, content, re.IGNORECASE)
                
                if matches:
                    prediction_text.extend(matches)
                
                # Find remedies
                remedy_pattern = f'"{pattern}_(?:remedy|remedial_measure)[^"]*":"([^"]+)"'
                remedy_matches = re.findall(remedy_pattern, content, re.IGNORECASE)
                
                if remedy_matches:
                    remedy_text.extend(remedy_matches)
            
            # Also look for malefic effects
            for pattern in patterns:
                malefic_pattern = f'"{pattern}_malefic[^"]*":"([^"]+)"'
                mal_matches = re.findall(malefic_pattern, content, re.IGNORECASE)
                if mal_matches:
                    prediction_text.extend([f"(Malefic) {m}" for m in mal_matches])
            
            # If we found data for this combination, add it
            if prediction_text or remedy_text:
                combined_prediction = " ".join(prediction_text)
                combined_remedy = " ".join(remedy_text)
                
                # Clean up the text
                combined_prediction = combined_prediction.replace('\\n', ' ').replace('\\r', '').strip()
                combined_remedy = combined_remedy.replace('\\n', ' ').replace('\\r', '').strip()
                
                if combined_prediction:
                    predictions.append({
                        'planet': planet,
                        'house': str(house),
                        'prediction': combined_prediction,
                        'remedy': combined_remedy if combined_remedy else "Follow general Lal Kitab remedies for this planet."
                    })
                    print(f"  ✓ Found data for {planet} in House {house}")
    
    return predictions

def write_to_lal_kitab_format(predictions, output_file='lal_kitab_data_parsed.txt'):
    """Write the parsed data to the format needed by lal_kitab_predictor.py"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for pred in predictions:
            f.write(f"Planet: {pred['planet']}\n")
            f.write(f"House: {pred['house']}\n")
            f.write(f"Prediction: {pred['prediction']}\n")
            f.write(f"Remedy: {pred['remedy']}\n")
            f.write("---\n")
    
    print(f"\n✓ Successfully wrote {len(predictions)} entries to {output_file}")
    
def main():
    print("=" * 80)
    print("Lal Kitab Data Parser")
    print("=" * 80)
    
    print("\nParsing data.md...")
    predictions = parse_lal_kitab_data()
    
    print(f"\n{'=' * 80}")
    print(f"Total entries found: {len(predictions)}")
    print(f"{'=' * 80}")
    
    # Show summary
    planet_counts = {}
    for pred in predictions:
        planet = pred['planet']
        planet_counts[planet] = planet_counts.get(planet, 0) + 1
    
    print("\nEntries per planet:")
    for planet, count in sorted(planet_counts.items()):
        print(f"  {planet}: {count} houses")
    
    # Write to file
    write_to_lal_kitab_format(predictions)
    
    print(f"\n{'=' * 80}")
    print("✓ Parsing complete!")
    print("✓ Data written to: lal_kitab_data_parsed.txt")
    print("\nNext steps:")
    print("1. Review lal_kitab_data_parsed.txt")
    print("2. Replace lal_kitab_data.txt with the parsed file if satisfied")
    print("3. Run test_lal_kitab.py to verify")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    main()
