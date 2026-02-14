import os
import sys
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parsers.bom_parser import BOMParser
from parsers.netlist_parser import NetlistParser
from analyzers.net_voltage_analyzer import NetVoltageAnalyzer
from analyzers.passive_rating_analyzer import PassiveRatingAnalyzer
from generators.excel_generator import ExcelGenerator

def automated_verify(netlist_path, db_path):
    print(f"--- Automated Verification: {os.path.basename(netlist_path)} ---")
    
    # 1. Setup
    netlist = NetlistParser(netlist_path)
    analyzer = PassiveRatingAnalyzer(db_path)
    voltage_detector = NetVoltageAnalyzer()
    
    # 2. Get all Nets and Auto-Confirm Voltages
    net_names = netlist.get_net_names()
    candidates = voltage_detector.detect_candidates(net_names)
    
    print(f"Detected {len(candidates)} potential voltage points. Auto-confirming all logical matches...")
    for net, val in candidates.items():
        voltage_detector.add_confirmed(net, val)
    
    confirmed_voltages = voltage_detector.get_analysis_state()

    # 3. Use all components found in the Netlist to create a virtual BOM
    # This ensures we test against real designators found in your file
    print(f"Extracting components from netlist...")
    results = []
    
    # In Protel 2.0, components are in the DESIGNATOR blocks
    # Our parser already populated self.components
    all_designators = netlist.components.keys()
    print(f"Found {len(all_designators)} components in netlist.")

    for des in all_designators:
        comp_data = netlist.components[des]
        desc = comp_data.get('DESCRIPTION', '').upper()
        part_type = comp_data.get('PARTTYPE', '').upper()
        footprint = comp_data.get('FOOTPRINT', '')
        
        # Categorize
        if des.startswith('C'): 
            c_type = 'Capacitor-MLCC'
            if 'TANT' in desc or 'TANT' in part_type: c_type = 'Capacitor-Tantalum'
            elif 'ELECTRO' in desc: c_type = 'Capacitor-Electrolytic'
            comp_info = {'designator': des, 'type': c_type, 'comment': part_type, 'value': part_type, 'footprint': footprint}
        elif des.startswith('R'):
            comp_info = {'designator': des, 'type': 'Resistor', 'comment': part_type, 'value': part_type, 'footprint': footprint}
        elif des.startswith('L') or 'INDUCTOR' in desc:
            comp_info = {'designator': des, 'type': 'Inductor', 'comment': part_type, 'value': part_type, 'footprint': footprint}
        elif des.startswith('D') or 'DIODE' in desc:
            comp_info = {'designator': des, 'type': 'Diode', 'comment': part_type, 'value': part_type, 'footprint': footprint}
        elif des.startswith('Q') or 'MOSFET' in desc or 'TRANSISTOR' in desc:
            comp_info = {'designator': des, 'type': 'Transistor', 'comment': part_type, 'value': part_type, 'footprint': footprint}
        else:
            comp_info = {'designator': des, 'type': 'Other', 'comment': part_type, 'value': part_type, 'footprint': footprint}

        # Find Max Voltage
        pin_to_net = netlist.get_component_nets(des)
        applied_voltages = [confirmed_voltages.get(net, 0.0) for net in pin_to_net.values()]
        max_v = max(applied_voltages) if applied_voltages else 0.0
        
        # Analyze
        if 'Capacitor' in comp_info['type']:
            res = analyzer.analyze_capacitor(comp_info, max_v)
        elif comp_info['type'] == 'Resistor':
            res = analyzer.analyze_resistor(comp_info, max_v)
        else:
            res = analyzer.analyze_generic(comp_info, voltage=max_v)
            
        res['Type'] = comp_info['type']
        res['Value'] = part_type
        res['Footprint'] = footprint
        res['Net_Voltage'] = f"{max_v}V"
        results.append(res)

    # 4. Generate Styled Excel
    output_xlsx = "Verification_Auto_Results.xlsx"
    excel = ExcelGenerator(output_xlsx)
    excel.generate(results)
    
    print(f"\n[Detected Voltage Points]")
    for net, val in confirmed_voltages.items():
        print(f"  {net}: {val}V")

    # 5. Summary Report
    df = pd.DataFrame(results)
    print("\n--- Summary of Analysis ---")
    print(f"Total Analyzed: {len(df)}")
    if not df.empty :
        print(df['verdict'].value_counts())
    
    noks = df[df['verdict'] == 'NOK']
    if not noks.empty:
        print(f"\nFound {len(noks)} NOK components. First 5:")
        # Corrected column name 'applied' (lowercase as per analyzer output)
        print(noks[['designator', 'Type', 'rating', 'applied', 'verdict']].head())

if __name__ == "__main__":
    base = r"c:\Users\fikre\Documents\PlatformIO\Projects\Auto_Altium"
    automated_verify(
        os.path.join(base, "NX_Orin.NET"),
        os.path.join(base, "data", "component_database.json")
    )
