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
from gui.rating_gui import VoltageConfirmationList, RatingsDashboard

class RatingVerificationApp:
    def __init__(self, netlist_path=None):
        self.netlist_path = netlist_path
        self.root = tk.Tk()
        self.root.withdraw()
        
        if not self.netlist_path:
            self.netlist_path = filedialog.askopenfilename(
                title="Select Altium Netlist (.NET)",
                filetypes=[("Netlist files", "*.NET"), ("All files", "*.*")]
            )
            if not self.netlist_path:
                sys.exit(0)

        self.netlist = NetlistParser(self.netlist_path)
        self.voltage_detector = NetVoltageAnalyzer()
        
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'component_database.json')
        self.analyzer = PassiveRatingAnalyzer(db_path)
        
        dir_path = os.path.dirname(self.netlist_path)
        self.excel_output = os.path.join(dir_path, "RatingVerification_Interactive_Report.xlsx")
        self.html_output = os.path.join(dir_path, "Executive_Summary.html")
        
        self.excel_gen = ExcelGenerator(self.excel_output)
        self.html_gen = HTMLExecutiveGenerator(self.html_output)

    def run(self):
        try:
            print(f"\n--- Starting Analysis ---\nTarget: {os.path.basename(self.netlist_path)}")
            
            # [Step 1] Parsing...
            self.netlist.parse()
            net_names = list(self.netlist.nets.keys())
            
            # [Step 2] Voltage Detection & Confirm
            candidates = self.voltage_detector.detect_candidates(net_names)
            if candidates:
                confirm_gui = VoltageConfirmationList(self.root, candidates)
                self.root.wait_window(confirm_gui.top)
                confirmed = confirm_gui.results
                for net, info in confirmed.items():
                    if info['action'] == 'confirm':
                        self.voltage_detector.add_confirmed(net, info['voltage'])
            
            # [Step 3] Analysis
            confirmed_voltages = self.voltage_detector.get_analysis_state()
            results = []
            
            for des, comp_data in self.netlist.components.items():
                try:
                    prefix = ''.join([c for c in des if c.isalpha()])
                    if prefix not in ['C', 'R']: continue
                    
                    pin_mapping = self.netlist.get_component_nets(des)
                    comp_nets = list(pin_mapping.values())
                    net_vs = [confirmed_voltages.get(net, 0.0) for net in comp_nets]
                    max_v = max(net_vs) if net_vs else 0.0
                    
                    comp_info = {**comp_data, 'designator': des}
                    if prefix == 'C':
                        res = self.analyzer.analyze_capacitor(comp_info, max_v)
                    else:
                        res = self.analyzer.analyze_resistor(comp_info, max_v)
                    
                    res['Type'] = prefix
                    res['Description'] = comp_data.get('DESCRIPTION') or comp_data.get('PARTTYPE') or '-'
                    res['Footprint'] = comp_data.get('FOOTPRINT', '-')
                    results.append(res)
                except Exception as e:
                    print(f"  [Warning] Skipping {des}: {e}")

            if results:
                self.excel_gen.generate(results)
                self.html_gen.generate(results)
                try: os.startfile(self.html_output)
                except: pass
                
                dashboard = RatingsDashboard(self.root, results)
                self.root.wait_window(dashboard.top)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if self.root.winfo_exists(): self.root.destroy()

if __name__ == "__main__":
    default_net = r"c:\Users\fikre\Documents\PlatformIO\Projects\Auto_Altium\NX_Orin.NET"
    if not os.path.exists(default_net): default_net = None
    app = RatingVerificationApp(default_net)
    app.run()
