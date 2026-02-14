import csv
from typing import List, Dict, Optional

class BOMParser:
    """Parses Altium BOM CSV with enhanced metadata extraction for ratings verification."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.components: List[Dict] = []
        self.parse()

    def parse(self):
        """Reads CSV and extracts key fields."""
        try:
            with open(self.filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Normalize keys (Altium often has trailing spaces or specific casing)
                    comp = {
                        'designator': row.get('Designator', '').strip(),
                        'comment': row.get('Comment', '').strip(),
                        'description': row.get('Description', '').strip(),
                        'footprint': row.get('Footprint', '').strip(),
                        'value': row.get('Value', '').strip(),
                        'quantity': row.get('Quantity', '1').strip()
                    }
                    if comp['designator']:
                        comp['type'] = self._infer_type(comp)
                        self.components.append(comp)
        except Exception as e:
            print(f"Error parsing BOM: {e}")

    def _infer_type(self, comp: Dict) -> str:
        """Categorizes components based on designator and comment."""
        d = comp['designator'].upper()
        c = comp['comment'].upper() + " " + comp['description'].upper()
        
        if d.startswith('C'):
            if 'ELECTRO' in c: return 'Capacitor-Electrolytic'
            if 'TANT' in c: return 'Capacitor-Tantalum'
            if 'MLCC' in c or 'CERAMIC' in c: return 'Capacitor-MLCC'
            if 'FILM' in c: return 'Capacitor-Film'
            if 'ORGANIC' in c or 'POLYMER' in c: return 'Capacitor-Organic'
            return 'Capacitor-MLCC' # Default
        elif d.startswith('R'):
            return 'Resistor'
        elif d.startswith('L') or 'INDUCTOR' in c or 'COIL' in c:
            return 'Inductor'
        elif d.startswith('FB') or 'FERRITE' in c:
            return 'Ferrite'
        elif d.startswith('D') or 'DIODE' in c:
            return 'Diode'
        elif d.startswith('Q') or 'TRANSISTOR' in c or 'MOSFET' in c or 'BJT' in c:
            return 'Transistor'
        return 'Other'

    def get_components(self) -> List[Dict]:
        return self.components
