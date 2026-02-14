import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from analyzers.passive_rating_analyzer import PassiveRatingAnalyzer

def test_audit_logic():
    analyzer = PassiveRatingAnalyzer("data/component_database.json")
    
    print("--- Testing Library Audit Logic ---")
    
    # Test Case 1: R131 Footprint Mismatch
    r131 = {
        'designator': 'R131',
        'Library Name': 'Passives.SchLib',
        'FOOTPRINT': '0402R',
        'PARTTYPE': '0603SAJ0104T5E',
        'DESCRIPTION': 'RES.(1608) 0603 100K Ohms 5% 1/10W-S 100PPM'
    }
    audit1 = analyzer.audit_component(r131)
    print(f"\nR131 Audit: {audit1['AuditVerdict']}")
    print(f"Reasons: {audit1['AuditReason']}")
    
    # Test Case 2: Standard Librarian Part
    std_part = {
        'designator': 'R1',
        'Library Name': 'triomobil.DbLib',
        'FOOTPRINT': '0603R',
        'PARTTYPE': 'RC0603FR-07100KL',
        'DESCRIPTION': 'RES SMD 0603 100K'
    }
    audit2 = analyzer.audit_component(std_part)
    print(f"\nStandard Part Audit: {audit2['AuditVerdict']}")
    print(f"Reasons: {audit2['AuditReason']}")
    
    # Test Case 3: Non-Standard Library
    manual_part = {
        'designator': 'C10',
        'Library Name': 'Miscellaneous.IntLib',
        'FOOTPRINT': '0805C',
        'PARTTYPE': 'Cap 100nF',
        'DESCRIPTION': 'Ceramic Capacitor 100nF'
    }
    audit3 = analyzer.audit_component(manual_part)
    print(f"\nManual Part Audit: {audit3['AuditVerdict']}")
    print(f"Reasons: {audit3['AuditReason']}")

if __name__ == "__main__":
    test_audit_logic()
