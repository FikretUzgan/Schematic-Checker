import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import re

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parsers.netlist_parser import NetlistParser
from analyzers.net_voltage_analyzer import NetVoltageAnalyzer
from analyzers.passive_rating_analyzer import PassiveRatingAnalyzer
from generators.excel_generator import ExcelGenerator
from generators.html_generator import HTMLExecutiveGenerator
from gui.rating_gui import VoltageConfirmationList, RatingsDashboard, NetlistSelectionPage

class RatingVerificationAppV2:
    """Version 2.0 with Switching Path Analysis and Worst-Case Detection."""
    
    def __init__(self, netlist_path=None):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # [Step 1] Landing Page for File Selection
        landing = NetlistSelectionPage(self.root, initial_path=netlist_path)
        self.root.wait_window(landing.top)
        
        if not landing.confirmed:
            sys.exit(0)
            
        self.netlist_path = landing.selected_path
        self.netlist = NetlistParser(self.netlist_path)
        self.voltage_detector = NetVoltageAnalyzer()
        
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'component_database.json')
        self.analyzer = PassiveRatingAnalyzer(db_path)
        
        dir_path = os.path.dirname(self.netlist_path)
        self.excel_output = os.path.join(dir_path, "RatingVerification_V2_WorstCase.xlsx")
        self.html_output = os.path.join(dir_path, "Executive_Summary_V2.html")
        
        self.excel_gen = ExcelGenerator(self.excel_output)
        self.html_gen = HTMLExecutiveGenerator(self.html_output)

    def identify_gnd_nets(self, net_names):
        """Standardizes identification of Ground nets."""
        gnd_keywords = ['GND', 'VSS', 'REF_0V', 'BAT_NEG', 'COM']
        return [n for n in net_names if any(kw in n.upper() for kw in gnd_keywords)]

    def map_transistor_bridges(self, gnd_nets):
        """Identify nets connected to GND via a transistor switch."""
        switchable_gnd_nets = set()
        for des, comp_data in self.netlist.components.items():
            if des.startswith('Q') or des.startswith('TR'):
                pin_mapping = self.netlist.get_component_nets(des)
                comp_nets = [n for n in pin_mapping.values() if n]
                if any(net in gnd_nets for net in comp_nets):
                    for net in comp_nets:
                        if net not in gnd_nets:
                            switchable_gnd_nets.add(net)
        return switchable_gnd_nets

    def run(self):
        try:
            print(f"\n--- Starting V2.0 Worst-Case Analysis ---\nTarget: {os.path.basename(self.netlist_path)}")
            
            # [Step 1] Parsing
            self.netlist.parse()
            net_names = list(self.netlist.nets.keys())
            
            # [Step 2] GND & Transistor Bridge Detection
            gnd_nets = self.identify_gnd_nets(net_names)
            switchable_gnd = self.map_transistor_bridges(gnd_nets)
            print(f"  - Detected {len(gnd_nets)} GND nets.")
            print(f"  - Detected {len(switchable_gnd)} Switchable GND nodes (via Transistors).")

            # [Step 3] Voltage Detection
            candidates = self.voltage_detector.detect_candidates(net_names)
            if candidates:
                print(f"[Step 3] {len(candidates)} potential voltage points detected. Opening confirmation UI...")
                confirm_gui = VoltageConfirmationList(self.root, candidates)
                self.root.wait_window(confirm_gui.top)
                confirmed = confirm_gui.results
                for net, info in confirmed.items():
                    if info['action'] == 'confirm':
                        self.voltage_detector.add_confirmed(net, info['voltage'])

            # [Step 4] Worst-Case Analysis
            print("[Step 4] Running Worst-Case Power Analysis...")
            confirmed_voltages = self.voltage_detector.get_analysis_state()
            results = []
            
            # Prefixes from designator_mapping.md
            analysis_prefixes = ['R', 'C', 'L']
            all_prefixes = ['R', 'C', 'J', 'CN', 'IC', 'U', 'D', 'TR', 'Q', 'L', 'FL', 'X']
            
            for des, comp_data in self.netlist.components.items():
                try:
                    # Extract prefix (handles 1 or 2 letter prefixes like CN, FL)
                    prefix_match = re.match(r'^([A-Z]{1,2})', des)
                    if not prefix_match: continue
                    prefix = prefix_match.group(1)
                    
                    if prefix not in all_prefixes: continue
                    
                    pin_mapping = self.netlist.get_component_nets(des)
                    comp_nets = [n for n in pin_mapping.values() if n]
                    
                    power_v = 0.0
                    is_on_switchable_node = False
                    
                    for net in comp_nets:
                        if net in confirmed_voltages:
                            power_v = max(power_v, confirmed_voltages[net])
                        if net in switchable_gnd:
                            is_on_switchable_node = True
                    
                    applied_v = power_v
                    comp_info = {**comp_data, 'designator': des, 'type': prefix}
                    
                    if prefix == 'C':
                        res = self.analyzer.analyze_capacitor(comp_info, applied_v)
                    elif prefix == 'R':
                        res = self.analyzer.analyze_resistor(comp_info, applied_v)
                    elif prefix == 'L':
                        res = self.analyzer.analyze_inductor(comp_info, 0.0) # Placeholder for current
                    else:
                        # General audit for other components (J, U, D, etc.)
                        audit = self.analyzer.audit_component(comp_info)
                        res = {
                            'Designator': des,
                            'Type': prefix,
                            'Verdict': 'OK' if audit['AuditVerdict'] == 'OK' else audit['AuditVerdict'],
                            'Applied': '-',
                            'Rating': '-',
                            'Derated': '-',
                            'Reason': 'Audit Only',
                            **audit
                        }
                    
                    # Metadata override
                    res['Type'] = prefix
                    res['Description'] = comp_data.get('DESCRIPTION') or comp_data.get('PARTTYPE') or '-'
                    res['Footprint'] = comp_data.get('FOOTPRINT', '-')
                    
                    # ENHANCED V2.0 LOGIC:
                    if is_on_switchable_node and prefix in analysis_prefixes:
                        if applied_v > 0:
                            res['Verdict'] = res['Verdict'] + " (Switching)"
                            res['Reason'] = f"[Switching Path] {res.get('Reason', '')}"
                        elif res['Verdict'] == 'OK':
                            res['Reason'] = "(Switching Node found but NO supply V detected/confirmed)"
                        
                    results.append(res)
                except Exception as e:
                    print(f"  [Warning] Skipping {des}: {e}")

            # [Step 5] Pre-test Summary
            print("\n--- PRE-TEST SUMMARY ---")
            lib_errors = [r for r in results if r.get('AuditVerdict') == 'FAIL']
            derating_errors = [r for r in results if r.get('Verdict', '').startswith('NOK')]
            missing_data = [r for r in results if "Missing Data" in r.get('Verdict', '')]
            
            print(f"  - Library / Footprint Issues: {len(lib_errors)}")
            print(f"  - Derating Violations: {len(derating_errors)}")
            print(f"  - Components Missing Ratings: {len(missing_data)}")
            if lib_errors:
                print("  [Sample Library Errors]:")
                for r in lib_errors[:3]:
                    print(f"    * {r['Designator']}: {r['AuditReason']}")
            print("------------------------\n")

            # [Step 5] Reporting
            if results:
                print(f"[Step 5] Generating Reports...")
                self.excel_gen.generate(results)
                self.html_gen.generate(results)
                
                dashboard = RatingsDashboard(self.root, results)
                self.root.wait_window(dashboard.top)
                
        except Exception as e:
            messagebox.showerror("V2.0 Critical Error", str(e))
            import traceback
            traceback.print_exc()
        finally:
            if self.root.winfo_exists():
                self.root.destroy()

if __name__ == "__main__":
    default_net = r"c:\Users\fikre\Documents\PlatformIO\Projects\Auto_Altium\NX_Orin.NET"
    if not os.path.exists(default_net): default_net = None
    app = RatingVerificationAppV2(default_net)
    app.run()
