"""
Lal Kitab Predictor Module
Reads Lal Kitab text data and generates predictions based on planetary positions
"""

class LalKitabPredictor:
    def __init__(self, lal_kitab_file_path):
        """
        Initialize the Lal Kitab predictor with the text file containing Lal Kitab data.
        
        Args:
            lal_kitab_file_path: Path to the text file containing Lal Kitab predictions and remedies
        """
        self.lal_kitab_file_path = lal_kitab_file_path
        self.predictions_data = {}
        self.remedies_data = {}
        self.load_lal_kitab_data()
    
    def load_lal_kitab_data(self):
        """
        Load and parse Lal Kitab data from the text file.
        Expected format in text file:
        
        [PLANET_HOUSE]
        Planet: Sun
        House: 1
        Prediction: [prediction text]
        Remedy: [remedy text]
        ---
        """
        try:
            with open(self.lal_kitab_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self._parse_lal_kitab_content(content)
            print(f"✓ Loaded Lal Kitab data from {self.lal_kitab_file_path}")
        except FileNotFoundError:
            print(f"⚠ Warning: Lal Kitab file not found at {self.lal_kitab_file_path}")
            print("  Predictions will not be available until the file is provided.")
        except Exception as e:
            print(f"⚠ Error loading Lal Kitab data: {e}")
    
    def _parse_lal_kitab_content(self, content):
        """
        Parse the Lal Kitab content and organize it by planet-house combinations.
        You can customize this parser based on your text file structure.
        """
        # Split content into sections (separated by ---)
        sections = content.split('---')
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Extract planet, house, prediction, and remedy
            planet = None
            house = None
            prediction = None
            remedy = None
            
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('Planet:'):
                    planet = line.split(':', 1)[1].strip()
                elif line.startswith('House:'):
                    house = line.split(':', 1)[1].strip()
                elif line.startswith('Prediction:'):
                    prediction = line.split(':', 1)[1].strip()
                elif line.startswith('Remedy:'):
                    remedy = line.split(':', 1)[1].strip()
            
            # Store the data if all fields are present
            if planet and house and prediction:
                key = f"{planet}_{house}"
                self.predictions_data[key] = {
                    'planet': planet,
                    'house': house,
                    'prediction': prediction,
                    'remedy': remedy if remedy else "No specific remedy mentioned"
                }
    
    def get_prediction(self, planet_name, house_number):
        """
        Get prediction for a specific planet in a specific house.
        
        Args:
            planet_name: Name of the planet (e.g., "Sun", "Moon")
            house_number: House number (1-12)
            
        Returns:
            Dictionary with prediction and remedy, or None if not found
        """
        key = f"{planet_name}_{house_number}"
        return self.predictions_data.get(key, None)
    
    def generate_chart_predictions(self, rasi_chart):
        """
        Generate complete Lal Kitab predictions for a Rasi (Lagna) chart.
        
        Args:
            rasi_chart: The Rasi chart dictionary from allchart.py
            
        Returns:
            Dictionary containing predictions for all planets
        """
        predictions = {}
        
        # Get predictions for each planet in the chart
        for planet_name, planet_data in rasi_chart['planets'].items():
            house = planet_data.get('house')
            if house:
                prediction_data = self.get_prediction(planet_name, house)
                if prediction_data:
                    predictions[planet_name] = {
                        'house': house,
                        'sign': planet_data['sign'],
                        'degree': planet_data['degree'],
                        'prediction': prediction_data['prediction'],
                        'remedy': prediction_data['remedy']
                    }
                else:
                    predictions[planet_name] = {
                        'house': house,
                        'sign': planet_data['sign'],
                        'degree': planet_data['degree'],
                        'prediction': f"No Lal Kitab data available for {planet_name} in house {house}",
                        'remedy': "No remedy available"
                    }
        
        return predictions
    
    def print_predictions(self, rasi_chart):
        """
        Print formatted Lal Kitab predictions for a chart.
        
        Args:
            rasi_chart: The Rasi chart dictionary from allchart.py
        """
        predictions = self.generate_chart_predictions(rasi_chart)
        
        print("\n" + "=" * 80)
        print(f"🔮 LAL KITAB PREDICTIONS for {rasi_chart['name']} 🔮")
        print("=" * 80)
        print(f"Based on Lagna Chart (Ascendant: {rasi_chart['ascendant']['sign']})")
        print("=" * 80)
        
        for planet_name, pred_data in predictions.items():
            print(f"\n{'─' * 80}")
            print(f"📍 {planet_name.upper()} in House {pred_data['house']} ({pred_data['sign']})")
            print(f"{'─' * 80}")
            print(f"\n🔍 PREDICTION:")
            print(f"   {pred_data['prediction']}")
            print(f"\n💊 REMEDY:")
            print(f"   {pred_data['remedy']}")
        
        print("\n" + "=" * 80)
        print("Note: These predictions are based on Lal Kitab principles.")
        print("=" * 80)
    
    def get_summary(self, rasi_chart):
        """
        Get a brief summary of key predictions.
        
        Args:
            rasi_chart: The Rasi chart dictionary
            
        Returns:
            String with summary
        """
        predictions = self.generate_chart_predictions(rasi_chart)
        
        summary_lines = [
            f"\n{'=' * 60}",
            f"LAL KITAB PREDICTIONS SUMMARY - {rasi_chart['name']}",
            f"{'=' * 60}\n"
        ]
        
        for planet_name, pred_data in predictions.items():
            summary_lines.append(f"• {planet_name} (House {pred_data['house']}): {pred_data['prediction'][:100]}...")
        
        return "\n".join(summary_lines)


# Example usage function
def demo_lal_kitab_predictor():
    """
    Demo function showing how to use the Lal Kitab predictor.
    """
    # This would be called from allchart.py after generating the Rasi chart
    print("Lal Kitab Predictor Module Loaded")
    print("Usage: Create a text file with Lal Kitab data and pass it to LalKitabPredictor")
