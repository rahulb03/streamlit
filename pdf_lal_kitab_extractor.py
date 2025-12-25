"""
Extract Lal Kitab predictions and remedies from PDF
Parses the lalkitab.pdf file to build a comprehensive database
"""

import re
import json
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed. Install with: pip install PyPDF2")
    PyPDF2 = None

class PDFLalKitabExtractor:
    def __init__(self, pdf_path="lalkitab.pdf"):
        self.pdf_path = Path(pdf_path)
        self.predictions_data = {}
        
    def extract_text_from_pdf(self):
        """Extract all text from the PDF"""
        if not PyPDF2:
            raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")
        
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
        
        return text
    
    def parse_planet_section(self, text, planet_name):
        """Parse a specific planet's section from the PDF text"""
        planet_data = {}
        
        # Find the planet section
        pattern = rf"{planet_name}\s*:\s*Effects\s+[Aa]nd\s+Remedies(.*?)(?=\d+\.\s+[A-Z][a-z]+\s*:\s*Effects|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if not match:
            return planet_data
        
        section_text = match.group(1)
        
        # Extract each house section
        for house_num in range(1, 13):
            house_patterns = [
                rf"{planet_name}\s+in\s+{house_num}(?:st|nd|rd|th)?\s+[Hh]ouse(.*?)(?={planet_name}\s+in\s+\d+|$)",
                rf"{planet_name}\s+in\s+{house_num}[a-z]*\s+[Hh]ouse(.*?)(?={planet_name}\s+in\s+\d+|$)"
            ]
            
            for pattern in house_patterns:
                house_match = re.search(pattern, section_text, re.DOTALL | re.IGNORECASE)
                if house_match:
                    house_text = house_match.group(1)
                    
                    # Extract benefic/malefic effects
                    benefic = self._extract_section(house_text, "Benefic")
                    malefic = self._extract_section(house_text, "Malefic")
                    remedies = self._extract_remedies(house_text)
                    
                    # Combine into prediction
                    prediction = ""
                    if benefic:
                        prediction += f"Benefic Effects: {benefic}\n\n"
                    if malefic:
                        prediction += f"Malefic Effects: {malefic}"
                    
                    if prediction.strip() or remedies:
                        planet_data[house_num] = {
                            'prediction': prediction.strip() or f"{planet_name} in house {house_num}",
                            'remedy': remedies or "Follow general remedies for this planet."
                        }
                    break
        
        return planet_data
    
    def _extract_section(self, text, section_name):
        """Extract content under a specific section (Benefic/Malefic)"""
        pattern = rf"{section_name}\s*:?(.*?)(?=Malefic|Remedies|{section_name}|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            content = match.group(1).strip()
            # Clean up the text
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'^\s*:\s*', '', content)
            return content[:500] if len(content) > 500 else content
        return ""
    
    def _extract_remedies(self, text):
        """Extract remedies section"""
        pattern = r"Remedies\s*:?(.*?)(?=\n\s*[A-Z][a-z]+\s+in\s+\d+|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            remedies_text = match.group(1).strip()
            
            # Extract numbered remedies
            remedy_items = re.findall(r'(?:\d+\.|\•)\s*([^\n]+)', remedies_text)
            
            if remedy_items:
                # Take first 3-4 most important remedies
                return " ".join(remedy_items[:4])
            else:
                # Return cleaned text
                cleaned = re.sub(r'\s+', ' ', remedies_text)
                return cleaned[:400] if len(cleaned) > 400 else cleaned
        
        return ""
    
    def extract_all_planets(self):
        """Extract data for all planets from the PDF"""
        print("Extracting text from PDF...")
        full_text = self.extract_text_from_pdf()
        
        if not full_text:
            print("Failed to extract text from PDF")
            return {}
        
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        all_data = {}
        
        for planet in planets:
            print(f"Parsing {planet}...")
            planet_data = self.parse_planet_section(full_text, planet)
            if planet_data:
                all_data[planet] = planet_data
                print(f"  Found {len(planet_data)} houses for {planet}")
        
        return all_data
    
    def save_to_text_format(self, output_file="lal_kitab_data.txt"):
        """Extract and save in the format expected by LalKitabPredictor"""
        all_data = self.extract_all_planets()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for planet, houses in all_data.items():
                for house, data in houses.items():
                    f.write(f"Planet: {planet}\n")
                    f.write(f"House: {house}\n")
                    f.write(f"Prediction: {data['prediction']}\n")
                    f.write(f"Remedy: {data['remedy']}\n")
                    f.write("---\n")
        
        print(f"\n✓ Saved {sum(len(h) for h in all_data.values())} entries to {output_file}")
        return all_data
    
    def save_to_json(self, output_file="lal_kitab_data.json"):
        """Save extracted data as JSON"""
        all_data = self.extract_all_planets()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved data to {output_file}")
        return all_data


def main():
    """Main execution"""
    print("=" * 80)
    print("Lal Kitab PDF Extractor")
    print("=" * 80)
    
    extractor = PDFLalKitabExtractor("lalkitab.pdf")
    
    # Extract and save in text format
    data = extractor.save_to_text_format()
    
    # Also save as JSON for easier access
    extractor.save_to_json()
    
    # Print summary
    print("\n" + "=" * 80)
    print("Extraction Summary:")
    print("=" * 80)
    for planet, houses in data.items():
        print(f"{planet}: {len(houses)} houses")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review 'lal_kitab_data.txt' to verify the extraction")
    print("2. The file is ready to use with LalKitabPredictor")
    print("3. Run allchart.py to see Lal Kitab predictions")
    print("=" * 80)


if __name__ == "__main__":
    main()
