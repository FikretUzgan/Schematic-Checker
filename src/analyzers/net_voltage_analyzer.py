import re
from typing import List, Dict, Optional, Set

class NetVoltageAnalyzer:
    """Detects and confirms voltages on PCB nets based on naming clues."""
    
    def __init__(self):
        self.confirmed_voltages: Dict[str, float] = {}
        self.excluded_nets: Set[str] = set()
        self.current_session_excluded: Set[str] = set()

    def _parse_voltage_value(self, raw_val: str) -> Optional[float]:
        """Robustly parse voltage strings like 3V3, 12V, +5, 1.8 into floats."""
        # Convert to upper and handle the XvY case (e.g., 3V3 -> 3.3)
        v_upper = raw_val.upper()
        
        # Case 1: XvY format (3V3, 1V8)
        xvy_match = re.search(r'(\d+)[Vv](\d+)', v_upper)
        if xvy_match:
            return float(f"{xvy_match.group(1)}.{xvy_match.group(2)}")
            
        # Case 2: Standard numbers (12V, 5, 3.3, +5, -12)
        # Remove 'V' unit if present at the end
        clean_val = v_upper.rstrip('V').replace('+', '')
        try:
            return float(clean_val)
        except ValueError:
            pass
            
        return None

    def detect_candidates(self, net_names: List[str]) -> Dict[str, float]:
        """Scans net names for potential voltage points and values."""
        candidates = {}
        # Priority 1: Numeric patterns like 3V3, 5V, 1.8V, 12V, or even just _3.3_
        num_pattern = re.compile(r'(\d+[Vv]\d+|\d+\.\d+[Vv]?|\d+[Vv])', re.IGNORECASE)
        # Priority 2: Keywords like VCC, VDD, VBUS, +5V, +12V
        main_pattern = re.compile(r'(VCC|VDD|VBUS|VSAFE|PWR|DCDC|REG|LDO|VOUT|\+\d+V)', re.IGNORECASE)
        
        for name in net_names:
            if name in self.excluded_nets or name in self.current_session_excluded:
                continue

            # CRITICAL: Exclude noise containing % or , (User Request)
            if '%' in name or ',' in name:
                continue

            net_upper = name.upper()
            
            # 1. Identify Ground/Reference
            if any(kw in net_upper for kw in ['GND', 'VSS', 'REF_0V', 'BAT_NEG', 'COM']):
                candidates[name] = 0.0
                continue
            
            # 2. Search for numeric voltage content first
            num_match = num_pattern.search(name)
            if num_match:
                voltage = self._parse_voltage_value(num_match.group(0))
                if voltage is not None:
                    candidates[name] = voltage
                    continue

            # 3. Fallback to keywords
            kw_match = main_pattern.search(name)
            if kw_match:
                # Try to see if there's a number AFTER the keyword like VDD33
                num_after = re.search(r'\d+', name[kw_match.end():])
                if num_after:
                   # Attempt to parse as 3.3 or similar if it looks like a common voltage
                   val = num_after.group(0)
                   if len(val) == 2 and val in ['12', '18', '33', '50']:
                       candidates[name] = float(f"{val[0]}.{val[1]}")
                       continue
                
                # Default keyword mapping
                candidates[name] = 3.3 # Standard assumption for VCC/VDD
        return candidates

    def add_confirmed(self, net_name: str, voltage: float):
        self.confirmed_voltages[net_name] = voltage

    def exclude_net(self, net_name: str):
        self.current_session_excluded.add(net_name)

    def get_analysis_state(self):
        return self.confirmed_voltages
