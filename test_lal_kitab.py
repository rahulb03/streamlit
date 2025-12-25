"""
Quick test script for Lal Kitab Predictor
Run this to verify the integration is working correctly
"""

from lal_kitab_predictor import LalKitabPredictor

# Sample chart data for testing (mimics the structure from allchart.py)
sample_rasi_chart = {
    "name": "Test User",
    "ascendant": {
        "sign": "Aries",
        "degree": 15.5
    },
    "planets": {
        "Sun": {
            "degree": 285.5,
            "sign": "Capricorn",
            "house": 10
        },
        "Moon": {
            "degree": 45.2,
            "sign": "Taurus",
            "house": 2
        },
        "Mars": {
            "degree": 15.8,
            "sign": "Aries",
            "house": 1
        },
        "Mercury": {
            "degree": 290.3,
            "sign": "Capricorn",
            "house": 10
        },
        "Jupiter": {
            "degree": 125.7,
            "sign": "Leo",
            "house": 5
        },
        "Venus": {
            "degree": 185.4,
            "sign": "Libra",
            "house": 7
        },
        "Saturn": {
            "degree": 15.2,
            "sign": "Aries",
            "house": 1
        },
        "Rahu": {
            "degree": 95.6,
            "sign": "Cancer",
            "house": 4
        },
        "Ketu": {
            "degree": 275.6,
            "sign": "Capricorn",
            "house": 10
        }
    }
}

def test_lal_kitab_predictor():
    print("=" * 80)
    print("Testing Lal Kitab Predictor Integration")
    print("=" * 80)
    
    # Initialize predictor
    print("\n1. Initializing Lal Kitab Predictor...")
    try:
        lk_predictor = LalKitabPredictor("lal_kitab_data.txt")
        print("✓ Successfully initialized predictor")
    except Exception as e:
        print(f"✗ Error initializing: {e}")
        return
    
    # Test individual prediction lookup
    print("\n2. Testing individual prediction lookup...")
    try:
        sun_prediction = lk_predictor.get_prediction("Sun", 1)
        if sun_prediction:
            print("✓ Found prediction for Sun in House 1")
            print(f"   Preview: {sun_prediction['prediction'][:80]}...")
        else:
            print("⚠ No prediction found for Sun in House 1")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test chart predictions generation
    print("\n3. Testing chart predictions generation...")
    try:
        predictions = lk_predictor.generate_chart_predictions(sample_rasi_chart)
        print(f"✓ Generated predictions for {len(predictions)} planets")
        
        # Show summary
        print("\n   Planets with predictions:")
        for planet, data in predictions.items():
            has_data = "Lal Kitab data" in data['prediction']
            status = "⚠ Missing" if has_data else "✓ Found"
            print(f"   {status} {planet} in House {data['house']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test formatted output
    print("\n4. Testing formatted prediction output...")
    try:
        lk_predictor.print_predictions(sample_rasi_chart)
        print("\n✓ Successfully displayed formatted predictions")
    except Exception as e:
        print(f"✗ Error displaying predictions: {e}")
    
    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)
    
    # Recommendations
    print("\n📋 NEXT STEPS:")
    print("1. Review the predictions above")
    print("2. Add more planet-house combinations to lal_kitab_data.txt")
    print("3. Run allchart.py to test with real birth data")
    print("4. Replace sample data with actual Lal Kitab content")

if __name__ == "__main__":
    test_lal_kitab_predictor()
