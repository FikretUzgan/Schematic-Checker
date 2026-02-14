
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from parsers.netlist_parser import NetlistParser
from analyzers.net_voltage_analyzer import NetVoltageAnalyzer
from analyzers.passive_rating_analyzer import PassiveRatingAnalyzer

def verify():
    netlist_path = r"c:\Users\fikre\Documents\PlatformIO\Projects\Auto_Altium\NX_Orin.NET"
    db_path = os.path.join(os.getcwd(), 'data', 'component_database.json')
    
    print(f"--- Verifying R81 and R89 Analysis ---")
    
    # 1. Parse
    parser = NetlistParser(netlist_path)
    parser.parse()
    
    # 2. Voltage Detection (Simulate confirmation)
    voltage_detector = NetVoltageAnalyzer()
    # Confirming the rails we found for R89 and R81
    voltage_detector.add_confirmed("VDD_3V3_SYS", 3.3)
    voltage_detector.add_confirmed("VDD_1V8", 1.8)
    confirmed_voltages = voltage_detector.get_analysis_state()
    
    # 3. Switching Detection
    gnd_keywords = ['GND', 'VSS', 'REF_0V', 'BAT_NEG', 'COM']
    gnd_nets = [n for n in parser.nets.keys() if any(kw in n.upper() for kw in gnd_keywords)]
    
    switchable_gnd = set()
    for des, comp_data in parser.components.items():
        if des.startswith('Q') or des.startswith('TR'):
            pin_mapping = parser.get_component_nets(des)
            comp_nets = [n for n in pin_mapping.values() if n]
            if any(net in gnd_nets for net in comp_nets):
                for net in comp_nets:
                    if net not in gnd_nets:
                        switchable_gnd.add(net)
    
    print(f"Detected {len(switchable_gnd)} switchable GND nodes.")
    
    # 4. Analyze
    analyzer = PassiveRatingAnalyzer(db_path)
    results = []
    
    for target in ['R81', 'R89']:
        comp_data = parser.components.get(target)
        if not comp_data:
            print(f"Error: {target} not found in netlist!")
            continue
            
        pin_mapping = parser.get_component_nets(target)
        comp_nets = [n for n in pin_mapping.values() if n]
        
        power_v = 0.0
        is_on_switchable_node = False
        for net in comp_nets:
            if net in confirmed_voltages:
                power_v = max(power_v, confirmed_voltages[net])
            if net in switchable_gnd:
                is_on_switchable_node = True
        
        res = analyzer.analyze_resistor({**comp_data, 'designator': target, 'type': 'R'}, power_v)
        
        if is_on_switchable_node:
            if power_v > 0:
                res['Verdict'] = res['Verdict'] + " (Switching)"
                res['Reason'] = f"[Switching Path] {res.get('Reason', '')}"
        
        print(f"\nResult for {target}:")
        print(f"  Nets: {comp_nets}")
        print(f"  Voltage detected: {power_v}V")
        print(f"  Switchable Node: {is_on_switchable_node}")
        print(f"  Verdict: {res['Verdict']}")
        print(f"  Reason: {res['Reason']}")
        print(f"  Calc: Applied={res.get('Applied')}, Rating={res.get('Rating')}")

if __name__ == "__main__":
    verify()
