import json
import os
import re
from typing import List, Dict, Any

class PassiveRatingAnalyzer:
    """Analyzes component ratings against applied circuit conditions using a rating database."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        with open(db_path, 'r') as f:
            self.db = json.load(f)
        
        self.settings = self.db.get('settings', {})
        self.marginal_threshold = self.settings.get('marginal_threshold_percentage', 80) / 100.0

    def get_verdict(self, applied: float, rating: float, derating_factor: float) -> str:
        """Determines the status (OK, NOK, Marginal)."""
        if rating <= 0: return "Unknown"
        
        derated_rating = rating * derating_factor
        ratio = applied / derated_rating if derated_rating > 0 else float('inf')
        
        if applied > rating: # Exceeds raw rating
            return "NOK"
        if ratio > 1.0: # Exceeds derated rating
            return "NOK"
        if ratio >= self.marginal_threshold:
            return "Marginal"
        return "OK"

    def audit_component(self, comp: Dict) -> Dict:
        """
        Audits library usage and footprint consistency.
        Checks: 1. Library Name is triomobil.DbLib 2. Part Name Size matches Footprint Size
        """
        lib_name = str(comp.get('Library Name', '')).strip()
        # Enforce strict company library
        is_standard_lib = lib_name == "triomobil.DbLib"
        
        # Footprint Consistency Check
        fields = [str(comp.get(f, '')) for f in ['DESCRIPTION', 'PARTTYPE', 'comment', 'value', 'Description']]
        text = " ".join(fields).upper()
        # Find size code in part name (e.g. 0603)
        part_size_match = re.search(r'\b(0201|0402|0603|0805|1206|1210|2010|2512)\b', text)
        
        footprint = str(comp.get('FOOTPRINT', '')).upper()
        # Improved footprint regex to extract the 4-digit code even if suffixed (e.g., 0402R)
        fp_size_match = re.search(r'(\d{4})', footprint)
        
        audit_verdict = "OK"
        audit_reasons = []
        
        if not is_standard_lib:
            audit_verdict = "FAIL"
            audit_reasons.append(f"Library Error: Non-Standard Library ({lib_name or 'Empty'})")
            
        if part_size_match and fp_size_match:
            part_size = part_size_match.group(1)
            fp_size = fp_size_match.group(1)
            if part_size != fp_size:
                audit_verdict = "FAIL"
                audit_reasons.append(f"Library Error: Footprint Mismatch! (Part: {part_size}, PCB: {fp_size})")
        elif not fp_size_match:
             audit_verdict = "FAIL"
             audit_reasons.append("Library Error: Missing or Invalid Footprint")
        
        return {
            'AuditVerdict': audit_verdict,
            'AuditReason': "; ".join(audit_reasons) if audit_reasons else "Consistent"
        }

    def analyze_capacitor(self, comp: Dict, voltage: float) -> Dict:
        c_type = comp.get('PARTTYPE', 'Capacitor-MLCC')
        factors = self.db['capacitors']['derating_factors']
        factor = factors.get(c_type, factors['Default'])
        
        raw_rating = self._extract_voltage_rating(comp)
        derated = raw_rating * factor
        status = self.get_verdict(abs(voltage), raw_rating, factor)
        
        # Calculate ratio for clearer reason
        ratio = (abs(voltage) / derated) * 100 if derated > 0 else 0
        if status == 'NOK':
            reason = f"EXCEEDED: {ratio:.1f}% of derated limit ({derated:.2f}V)"
        elif status == 'Marginal':
            reason = f"MARGINAL: {ratio:.1f}% of derated limit ({derated:.2f}V)"
        else:
            reason = "Safe"
            
        if raw_rating == 0: 
            status = "Unknown (Missing Data)"
            reason = "No voltage rating found in params"
        
        audit = self.audit_component(comp)
        
        # Update AuditVerdict to include derating failures
        final_audit_verdict = audit['AuditVerdict']
        if status.startswith('NOK') or status.startswith('Unknown'):
            final_audit_verdict = 'FAIL'
        elif status == 'Marginal' and final_audit_verdict == 'OK':
            final_audit_verdict = 'WARNING'
        
        return {
            'Designator': comp['designator'],
            'Applied': f"{voltage:.2f}V",
            'Rating': f"{raw_rating:.2f}V",
            'Derated': f"{derated:.2f}V",
            'Verdict': status,
            'Reason': reason,
            'AuditVerdict': final_audit_verdict,
            'AuditReason': audit['AuditReason']
        }

    def analyze_resistor(self, comp: Dict, voltage: float) -> Dict:
        """Analyzes power dissipation if resistance can be determined."""
        resistance = self._extract_resistance(comp)
        power_rating = self._get_resistor_power(comp)
        factor = self.db['resistors'].get('default_derating_factor', 1.0)
        
        if resistance is None or resistance == 0:
            res_dict = {
                'Designator': comp['designator'], 
                'Verdict': 'Unknown (R=?)', 
                'Applied': '0.00mW', 
                'Rating': f"{power_rating*1000:.1f}mW",
                'Reason': "Could not parse resistance value"
            }
        else:
            applied_power = (voltage ** 2) / resistance
            derated = power_rating * factor
            status = self.get_verdict(applied_power, power_rating, factor)
            
            # Calculate ratio for clearer reason
            ratio = (applied_power / derated) * 100 if derated > 0 else 0
            if status == 'NOK':
                reason = f"EXCEEDED: {ratio:.1f}% of derated limit ({derated*1000:.1f}mW)"
            elif status == 'Marginal':
                reason = f"MARGINAL: {ratio:.1f}% of derated limit ({derated*1000:.1f}mW)"
            else:
                reason = "Safe"
            
            res_dict = {
                'Designator': comp['designator'],
                'Applied': f"{applied_power*1000:.2f}mW",
                'Rating': f"{power_rating*1000:.2f}mW",
                'Derated': f"{derated*1000:.2f}mW",
                'Verdict': status,
                'Reason': reason
            }
        
        if power_rating == 0 or (resistance is None or resistance == 0):
            res_dict['Verdict'] = "Unknown (Missing Data)"
            
        audit = self.audit_component(comp)
        
        # Update AuditVerdict to include derating failures
        final_audit_verdict = audit['AuditVerdict']
        if res_dict['Verdict'].startswith('NOK') or res_dict['Verdict'].startswith('Unknown'):
            final_audit_verdict = 'FAIL'
        elif res_dict['Verdict'] == 'Marginal' and final_audit_verdict == 'OK':
            final_audit_verdict = 'WARNING'
        
        res_dict['AuditVerdict'] = final_audit_verdict
        res_dict['AuditReason'] = audit['AuditReason']
        return res_dict

    def analyze_inductor(self, comp: Dict, current: float) -> Dict:
        """Analyzes inductor current ratings."""
        i_rating = self._extract_current_rating(comp)
        factor = self.db.get('inductors', {}).get('default_derating_factor', 0.7)
        derated = i_rating * factor
        status = self.get_verdict(abs(current), i_rating, factor)
        
        # Calculate ratio
        ratio = (abs(current) / derated) * 100 if derated > 0 else 0
        if status == 'NOK':
            reason = f"EXCEEDED: {ratio:.1f}% of derated limit ({derated:.2f}A)"
        elif status == 'Marginal':
            reason = f"MARGINAL: {ratio:.1f}% of derated limit ({derated:.2f}A)"
        else:
            reason = "Safe"
            
        if i_rating == 0:
            status = "Unknown (Missing Data)"
            reason = "No current rating found in params"
            
        audit = self.audit_component(comp)
        
        # Update AuditVerdict to include derating failures
        final_audit_verdict = audit['AuditVerdict']
        if status.startswith('NOK') or status.startswith('Unknown'):
            final_audit_verdict = 'FAIL'
        elif status == 'Marginal' and final_audit_verdict == 'OK':
            final_audit_verdict = 'WARNING'
        
        return {
            'Designator': comp['designator'],
            'Applied': f"{current:.2f}A",
            'Rating': f"{i_rating:.2f}A",
            'Derated': f"{derated:.2f}A",
            'Verdict': status,
            'Reason': reason,
            'AuditVerdict': final_audit_verdict,
            'AuditReason': audit['AuditReason']
        }

    def _extract_current_rating(self, comp: Dict) -> float:
        """Extracts current rating (e.g., 2A, 500mA) from component fields."""
        fields = [str(comp.get(f, '')) for f in ['DESCRIPTION', 'PARTTYPE', 'comment', 'value', 'Description']]
        text = " ".join(fields).upper()
        
        # Look for Amps/mA
        ma_match = re.search(r'(\d+(?:\.\d+)?)\s*MA', text)
        if ma_match:
            return float(ma_match.group(1)) / 1000.0
            
        a_match = re.search(r'(\d+(?:\.\d+)?)\s*A\b', text)
        if a_match:
            return float(a_match.group(1))
            
        return 0.0

    def _get_resistor_power(self, comp: Dict) -> float:
        """
        Infers resistor power rating from footprints or part names.
        Priority: 1. Explicit Wattage (1/10W, 100mW, 0.1W) 
                  2. Footprint in Part Name (0603...)
                  3. Library Footprint
        """
        fields = [str(comp.get(f, '')) for f in ['DESCRIPTION', 'PARTTYPE', 'comment', 'value', 'Description']]
        text = " ".join(fields).upper()
        
        # Priority 1a: Fractional Wattage (e.g., 1/10W, 1/16W)
        frac_match = re.search(r'(\d+/\d+)\s*W', text)
        if frac_match:
            try:
                num, den = map(float, frac_match.group(1).split('/'))
                return num / den
            except: pass

        # Priority 1b: Decimal/Metric Wattage (e.g., 100MW, 0.1W, 2W)
        # mW check
        mw_match = re.search(r'(\d+(?:\.\d+)?)\s*MW', text)
        if mw_match:
            return float(mw_match.group(1)) / 1000.0
        
        # W check (careful not to match 1W in 100K 1% or similar)
        # Look for standalone number followed by W
        w_match = re.search(r'\b(\d+(?:\.\d+)?)\s*W\b', text)
        if w_match:
            return float(w_match.group(1))
            
        # Priority 2: Footprint codes in Part Name (e.g., 0603SAJ...)
        fp_match = re.search(r'\b(0201|0402|0603|0805|1206|1210|2010|2512)\b', text)
        if fp_match:
            code = fp_match.group(1)
            return self.db['resistors']['footprint_power_ratings_watts'].get(code, 0.063)

        # Priority 3: Library Footprint tag
        footprint = str(comp.get('FOOTPRINT', '')).upper()
        match = re.search(r'(\d{4})', footprint)
        if match:
            fp_code = match.group(1)
            return self.db['resistors']['footprint_power_ratings_watts'].get(fp_code, 0.063)
            
        return 0.063

    def _extract_voltage_rating(self, comp: Dict) -> float:
        # Altium/Protel netlists use PARTTYPE or DESCRIPTION for the value string
        text = (str(comp.get('PARTTYPE', '')) + " " + 
                str(comp.get('DESCRIPTION', '')) + " " + 
                str(comp.get('comment', '')) + " " + 
                str(comp.get('value', ''))).upper()
        
        match = re.search(r'(\d+(?:\.\d+)?)\s*V', text)
        return float(match.group(1)) if match else 0.0

    def _extract_resistance(self, comp: Dict) -> float:
        # Altium/Protel netlists use PARTTYPE or DESCRIPTION for the value string
        fields = [str(comp.get(f, '')) for f in ['DESCRIPTION', 'PARTTYPE', 'comment', 'value', 'Description']]
        text = " ".join(fields).upper()
        
        # Priority 1: Values with units (e.g., 100K, 4.7R, 1M)
        # Search for these first to avoid picking up 0603 from "0603 100K"
        unit_match = re.search(r'(\d+(?:\.\d+)?)\s*([KRM])(?!\w)', text)
        if unit_match:
            val = float(unit_match.group(1))
            unit = unit_match.group(2)
            if unit == 'K': return val * 1000
            if unit == 'M': return val * 1000000
            return val
            
        # Priority 2: Standalone numbers (e.g., "100" in "RES 100")
        # But ignore common footprint prefixes if they appear at the start of a word
        # We look for numbers that aren't 0402, 0603, 0805, 1206 unless they are standalone
        raw_matches = re.findall(r'\b(\d+(?:\.\d+)?)\b', text)
        for val_str in raw_matches:
            if val_str in ['0402', '0603', '0805', '1206']:
                continue
            return float(val_str)
            
        # Fallback: If only a footprint-like number is found, use it as a last resort
        if raw_matches:
            return float(raw_matches[0])
            
        return None

    def analyze_generic(self, comp: Dict, current: float = 0, voltage: float = 0) -> Dict:
        """Fallback for Coils, Ferrites, Diodes, Transistors."""
        # This would ideally use more complex logic per type
        return {
            'Designator': comp['designator'],
            'Verdict': 'Manual Review Required',
            'Note': f"Type: {comp['type']}"
        }
