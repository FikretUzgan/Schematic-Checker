#!/usr/bin/env python3
"""
Quick test of the Tkinter net selector GUI.
"""

import tkinter as tk
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.tk_net_selector import show_net_selector

def test_net_selector():
    """Test the net selector with sample nets."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Sample nets that might be in a real netlist
    sample_nets = [
        'VCC', 'VCC_3V3', 'VCC_5V', 'VCORE', 'VDRAM',
        'VDD_1V8', 'VDD_3V3', 'VDD_5V', 'VREF',
        'GND', 'GND_STAR', 'GND_RETURN',
        'VBUS', 'V12', 'V5', 'V3V3',
        'V1V2', 'V1V8_AUX', 'VDDA', 'VDDQ',
        'VSS', 'VSUPPLY', 'VCAP', 'VOUT',
        'SDA', 'SCL', 'MOSI', 'MISO', 'CLK',
        'DATA_BUS_0', 'DATA_BUS_1', 'ADDR_0', 'ADDR_1'
    ]
    
    print("Testing Tkinter Net Selector...")
    print(f"Available nets: {len(sample_nets)}")
    print("\nTry typing 'V' to filter nets starting with V")
    print("Then add 'D' to filter to 'VD'")
    print("Hold CTRL and click to select multiple nets")
    print("Double-click to confirm or press Enter after selecting")
    
    result = show_net_selector(root, sample_nets)
    
    if result:
        # result is now a list of (net_name, voltage) tuples
        print(f"\n✓ Selected {len(result)} net(s):")
        for net_name, voltage in result:
            print(f"  - {net_name}: {voltage}V")
    else:
        print("\n✗ Selection cancelled")
    
    root.destroy()

if __name__ == "__main__":
    test_net_selector()
