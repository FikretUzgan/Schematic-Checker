import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parsers.netlist_parser import NetlistParser
from analyzers.net_voltage_analyzer import NetVoltageAnalyzer

def interactive_verification(netlist_path: str):
    print("--- Power Net Voltage Detection & Confirmation ---")
    parser = NetlistParser(netlist_path)
    analyzer = NetVoltageAnalyzer()
    
    net_names = parser.get_net_names()
    candidates = analyzer.detect_candidates(net_names)
    
    if not candidates:
        print("No voltage candidates detected automatically.")
        return

    print(f"Found {len(candidates)} potential voltage nets. Please confirm each:")
    
    for net, val in candidates.items():
        while True:
            resp = input(f"\nNet: {net} | Detected: {val}V\nConfirm? [y(es) / n(ot a voltage) / e(dit value)]: ").lower().strip()
            if resp == 'y':
                analyzer.add_confirmed(net, val)
                print(f"Confirmed {net} = {val}V")
                break
            elif resp == 'n':
                analyzer.exclude_net(net)
                print(f"Excluded {net}")
                break
            elif resp == 'e':
                new_val = input("Enter correct voltage: ").strip()
                try:
                    analyzer.add_confirmed(net, float(new_val))
                    print(f"Confirmed {net} = {new_val}V")
                    break
                except ValueError:
                    print("Invalid number. Try again.")
            else:
                print("Invalid option. Please use y, n, or e.")

    print("\n--- Summary of Confirmed Voltages ---")
    confirmed = analyzer.get_analysis_state()
    for net, v in confirmed.items():
        print(f"{net}: {v}V")
    
    return confirmed

if __name__ == "__main__":
    # Test with the provided NX_Orin.NET if it exists in expected location
    test_net = r"c:\Users\fikre\Documents\PlatformIO\Projects\Auto_Altium\NX_Orin.NET"
    if os.path.exists(test_net):
        interactive_verification(test_net)
    else:
        print(f"Test netlist not found at {test_net}")
