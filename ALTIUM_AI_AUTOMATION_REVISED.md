# ALTIUM AI AUTOMATION SYSTEM

## Practical Implementation Plan v2.0

**Target Platform:** Altium Designer 24.01  
**Document Version:** 2.0 (Revised)  
**Date:** February 2026  
**Development Approach:** Export Real Data → Python Development → AI Translation → Altium Integration

---

## EXECUTIVE SUMMARY

This implementation plan uses a **pragmatic four-phase workflow** for each feature:

1. **Export real data** from existing Altium projects (netlists, BOMs, etc.)
2. **Develop in Python** using the exported data (fast debugging with real data)
3. **AI translates** to DelphiScript (automated, proven logic)
4. **Integrate** with Altium API (focused effort, minimal debugging)

### Why This Approach Works

✅ **Real Data**: Test with actual netlists/BOMs from your designs, not synthetic data  
✅ **Fast Development**: Python debugging tools vs. Altium's ShowMessage  
✅ **Proven Logic**: Only translate working, tested code  
✅ **Simple Translation**: AI does it, you just review  
✅ **Focused Integration**: Only the API layer needs Altium debugging  

### Time Savings

**Traditional Approach (Direct DelphiScript):**

- Development: 40% of time
- Debugging in Altium: 50% of time ⚠️ PAINFUL
- Testing: 10% of time

**This Approach:**

- Python development: 35% of time
- AI translation: 5% of time (mostly automated)
- Altium integration: 25% of time
- Testing: 10% of time
- **Net time savings: ~40%**

---

## TABLE OF CONTENTS

1. [Critical First Steps](#critical-first-steps)
2. [Data Export Guide](#data-export-guide)
3. [Python Development Setup](#python-development-setup)
4. [AI Translation Process](#ai-translation-process)
5. [Altium API Integration](#altium-api-integration)
6. [Feature Implementation - TIER 1](#tier-1-features)
7. [Feature Implementation - TIER 2](#tier-2-features)
8. [Feature Implementation - TIER 3](#tier-3-features)
9. [Development Roadmap](#development-roadmap)
10. [Success Metrics](#success-metrics)

---

## CRITICAL FIRST STEPS

### Phase 0: Data Collection (Day 1)

Before writing ANY code, collect real data from your existing Altium projects:

**Required Exports:**

```
□ Netlist from 2-3 completed projects
□ BOM (Bill of Materials) from same projects
□ Layer stack configurations
□ Current design rules (if any)
□ Component datasheets (for AI analysis)
```

**Why This Matters:**

- Your code will handle REAL edge cases, not imagined ones
- Test data is authentic, not synthetic
- Validation is instant (you know what the correct answer should be)

---

## DATA EXPORT GUIDE

### Export 1: Netlist (Network Connectivity)

**Purpose:** Get all net names, component connections, pin assignments

**Procedure:**

```
1. Open your PCB in Altium Designer 24.01
2. File → Export → Protel Netlist
3. Save as: ProjectName.NET
4. Location: Save to test_data/netlists/ folder
```

**What You Get:**

```
[
NetName=USB3_SSTX_P
Pin=U1-A5
Pin=J1-1

NetName=USB3_SSTX_N
Pin=U1-A6
Pin=J1-2

NetName=VCC_3V3
Pin=U1-3
Pin=U2-5
Pin=C1-1
Pin=C2-1
]
```

**Use Cases:**

- Differential pair detection
- Power net identification
- Net topology analysis
- Length matching groups

---

### Export 2: Bill of Materials (Component List)

**Purpose:** Get all components, values, packages, part numbers

**Procedure:**

```
1. Open your PCB in Altium
2. Reports → Bill of Materials
3. Configure columns:
   ☑ Designator
   ☑ Comment (part number/description)
   ☑ Footprint
   ☑ Value (if applicable)
   ☑ Quantity
4. Export as CSV
5. Save to: test_data/boms/ProjectName_BOM.csv
```

**What You Get:**

```csv
Designator,Comment,Footprint,Value,Quantity
R1,Resistor,0603,10K,1
R2,Resistor,0603,4.7K,1
C1,Capacitor,0805,10uF,1
C2,Capacitor,0603,100nF,1
U1,TPS54340,SOT23-6,,1
U2,AP2112K-3.3,SOT23-5,,1
```

**Use Cases:**

- Passive component rating verification
- Power consumption analysis
- Package size verification
- Part number lookups for datasheets

---

### Export 3: Layer Stack

**Purpose:** Get stackup configuration for impedance calculations

**Procedure:**

```
1. Design → Layer Stack Manager
2. Click "Export" button
3. Choose format: XML or text
4. Save to: test_data/stackups/ProjectName_Stack.xml
```

**What You Get:**

```xml
<LayerStack>
  <Layer Name="Top" Type="Signal" Thickness="0.035" CopperWeight="1"/>
  <Layer Name="Dielectric" Type="Dielectric" Thickness="0.19" Er="4.6" Material="7628"/>
  <Layer Name="GND" Type="Plane" Thickness="0.035" CopperWeight="1"/>
  <Layer Name="Core" Type="Dielectric" Thickness="1.02" Er="4.5" Material="FR4"/>
  <Layer Name="PWR" Type="Plane" Thickness="0.035" CopperWeight="1"/>
  <Layer Name="Dielectric" Type="Dielectric" Thickness="0.19" Er="4.6" Material="7628"/>
  <Layer Name="Bottom" Type="Signal" Thickness="0.035" CopperWeight="1"/>
</LayerStack>
```

**Use Cases:**

- Impedance profile calculation
- Trace width determination
- Via aspect ratio analysis

---

### Export 4: Current Design Rules (Optional)

**Purpose:** Understand existing rules to avoid conflicts

**Procedure:**

```
1. Design → Rules
2. Right-click in rules panel
3. Export Rules
4. Save to: test_data/rules/ProjectName_Rules.xml
```

**Use Cases:**

- Rule conflict detection
- Rule migration from old projects
- Understanding user's current workflow

---

### Data Collection Checklist

Create this folder structure:

```
altium-automation/
├── test_data/
│   ├── netlists/
│   │   ├── usb_board_v1.NET
│   │   ├── hdmi_interface.NET
│   │   └── power_supply.NET
│   ├── boms/
│   │   ├── usb_board_v1_BOM.csv
│   │   ├── hdmi_interface_BOM.csv
│   │   └── power_supply_BOM.csv
│   ├── stackups/
│   │   ├── standard_4L.xml
│   │   └── high_speed_6L.xml
│   └── datasheets/
│       ├── TPS54340.pdf
│       └── AP2112K.pdf
```

**Collect data from:**

- ✅ At least 2 different board types (e.g., one USB board, one HDMI board)
- ✅ Boards you've already completed (so you know the correct answers)
- ✅ Include both simple and complex designs

---

## PYTHON DEVELOPMENT SETUP

### Environment Setup (15 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies, please install them automatically,whatever you need


# Create project structure
mkdir -p src/{parsers,analyzers,calculators}
mkdir -p tests
mkdir -p test_data/{netlists,boms,stackups}
touch src/__init__.py
touch tests/__init__.py
```

### Project Structure

```
base folder
├── venv/                          # Python virtual environment
├── src/
│   ├── __init__.py
│   ├── parsers/                   # Parse Altium export formats
│   │   ├── __init__.py
│   │   ├── netlist_parser.py     # Parse .NET files
│   │   ├── bom_parser.py         # Parse BOM CSV
│   │   └── stackup_parser.py     # Parse stackup XML
│   ├── analyzers/                 # Core analysis logic
│   │   ├── __init__.py
│   │   ├── diff_pair_detector.py
│   │   ├── protocol_identifier.py
│   │   ├── power_net_analyzer.py
│   │   └── dfm_checker.py
│   ├── calculators/               # Engineering calculations
│   │   ├── __init__.py
│   │   ├── trace_width_calc.py   # IPC-2152
│   │   └── impedance_calc.py
│   └── ai_interface/              # AI API wrapper
│       ├── __init__.py
│       └── ai_client.py
├── tests/
│   ├── __init__.py
│   ├── test_diff_pairs.py
│   ├── test_power_calc.py
│   └── test_with_real_data.py    # Tests using exported data
├── test_data/                     # Your exported Altium data
│   ├── netlists/
│   ├── boms/
│   └── stackups/
├── altium_scripts/                # Final DelphiScript output
│   └── (AI-generated .pas files go here)
├── requirements.txt
└── README.md
```

### requirements.txt

```
requests==2.31.0
openai==1.12.0
anthropic==0.18.0
pandas==2.2.0
pytest==8.0.0
python-dotenv==1.0.0
```

---

## AI TRANSLATION PROCESS

### Translation Template

Use this prompt structure for all translations:

```
I have working Python code that [DESCRIPTION OF WHAT IT DOES].

The Python code processes real Altium export data and has been 
thoroughly tested. I need to convert it to DelphiScript for 
Altium Designer 24.01.

PYTHON CODE:
[paste your tested Python code]

TRANSLATION REQUIREMENTS:
1. Convert to DelphiScript syntax
2. Replace file reading with Altium API calls:
   - Instead of parsing .NET file, use: Board.Nets[i]
   - Instead of parsing BOM CSV, use: Component objects
3. Use appropriate Delphi types:
   - Python list → TStringList or dynamic array
   - Python dict → Pascal record
   - Python class → Pascal class
4. Keep the EXACT same logic (it's already proven to work)
5. Add proper error handling (try/except)
6. Add logging to C:\Temp\AltiumDebug.log
7. Include comments explaining conversions

ALTIUM API CONTEXT:
- Board: IPCB_Board (get via PCBServer.GetCurrentPCBBoard)
- Nets: IPCB_Net (access via Board.Nets[i], count via Board.NetCount)
- Components: IPCB_Component (access via Board.Components[i])
- Coordinate system: Internal units (use MilsToCoord/CoordToMils)

Generate only the DelphiScript code with explanatory comments.
```

### Translation Review Checklist

After AI generates DelphiScript:

```
□ Logic matches Python version exactly
□ All error cases handled
□ Logging added for debugging
□ Altium API calls correct
□ Coordinate conversions proper (MilsToCoord)
□ Memory management correct (Free objects)
□ Type safety maintained
□ Comments explain non-obvious conversions
```

### Common Translation Issues

**Issue 1: List Operations**

```python
# Python
nets = [net for net in all_nets if '_P' in net]
```

```pascal
// DelphiScript - AI might generate wrong syntax
// Fix manually if needed
For i := 0 To AllNets.Count - 1 Do
Begin
    If Pos('_P', AllNets[i]) > 0 Then
        Nets.Add(AllNets[i]);
End;
```

**Issue 2: Dictionary Access**

```python
# Python
data = {'voltage': 3.3, 'current': 2.0}
voltage = data['voltage']
```

```pascal
// DelphiScript - use records
Type TData = Record
    Voltage: Real;
    Current: Real;
End;

Var Data: TData;
Data.Voltage := 3.3;
Data.Current := 2.0;
```

**Issue 3: String Operations**

```python
# Python
if net.endswith('_P'):
    base = net[:-2]
```

```pascal
// DelphiScript
If Copy(Net, Length(Net) - 1, 2) = '_P' Then
    Base := Copy(Net, 1, Length(Net) - 2);
```

---

## ALTIUM API INTEGRATION

### Key API Patterns for Altium 24.01

#### Getting the Board

```pascal
Var
    Board: IPCB_Board;
Begin
    Board := PCBServer.GetCurrentPCBBoard;
    If Board = Nil Then
    Begin
        ShowMessage('No PCB document open');
        Exit;
    End;
    
    // Use board...
End;
```

#### Iterating Nets

```pascal
Var
    Board: IPCB_Board;
    Net: IPCB_Net;
    i: Integer;
Begin
    Board := PCBServer.GetCurrentPCBBoard;
    
    For i := 0 To Board.NetCount - 1 Do
    Begin
        Net := Board.Nets[i];
        ShowMessage('Net: ' + Net.Name);
    End;
End;
```

#### Iterating Components

```pascal
Var
    Board: IPCB_Board;
    Component: IPCB_Component;
    i: Integer;
Begin
    Board := PCBServer.GetCurrentPCBBoard;
    
    For i := 0 To Board.ComponentCount - 1 Do
    Begin
        Component := Board.Components[i];
        ShowMessage('Component: ' + Component.Designator.Text);
    End;
End;
```

#### Creating Design Rules

```pascal
Var
    Board: IPCB_Board;
    Rule: IPCB_Rule;
Begin
    Board := PCBServer.GetCurrentPCBBoard;
    
    // Create differential pair rule
    Rule := PCBServer.PCBRuleFactory(eRule_DiffPairsRouting);
    Rule.Name := 'DiffPair_USB3_TX';
    Rule.Scope1Expression := 'InNet(''USB3_TX_P'') Or InNet(''USB3_TX_N'')';
    Rule.TargetImpedance := 90;  // Ohms
    Rule.MaxUncoupledLength := MilsToCoord(100);
    
    // Add to board
    Board.AddPCBObject(Rule);
    Board.Refresh;
End;
```

#### Logging for Debugging

```pascal
Var
    LogFile: TextFile;

Procedure Log(Msg: String);
Begin
    AssignFile(LogFile, 'C:\Temp\AltiumDebug.log');
    
    If FileExists('C:\Temp\AltiumDebug.log') Then
        Append(LogFile)
    Else
        Rewrite(LogFile);
    
    WriteLn(LogFile, FormatDateTime('hh:nn:ss.zzz', Now) + ' - ' + Msg);
    CloseFile(LogFile);
End;

// Use everywhere
Procedure AnalyzeSomething;
Begin
    Log('Starting analysis');
    Log('Board has ' + IntToStr(Board.NetCount) + ' nets');
    // ... rest of code
    Log('Analysis complete');
End;
```

---

## TIER 1 FEATURES

### Feature 1.1: Differential Pair Auto-Detection

**Complexity:** ⭐⭐  
**Impact:** ⭐⭐⭐⭐⭐  
**Priority:** 10/10  
**Timeline:** 1 week

#### Phase 1: Export Data (30 minutes)

```
1. Open project with USB 3.0 / HDMI / PCIe
2. File → Export → Protel Netlist
3. Save to: test_data/netlists/usb_board.NET
4. Verify file contains differential pair nets
```

#### Phase 2: Python Development (2-3 days)

**File: src/parsers/netlist_parser.py**

```python
"""Parse Altium .NET netlist files"""

class NetlistParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.nets = []
        self.parse()
    
    def parse(self):
        """Parse Altium netlist format"""
        current_net = None
        
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                
                if line.startswith('['):
                    # Start of nets section
                    continue
                elif line.startswith('NetName='):
                    # New net
                    net_name = line.split('=', 1)[1].strip()
                    current_net = {
                        'name': net_name,
                        'pins': []
                    }
                    self.nets.append(current_net)
                elif line.startswith('Pin=') and current_net is not None:
                    # Pin belonging to current net
                    pin = line.split('=', 1)[1].strip()
                    current_net['pins'].append(pin)
    
    def get_net_names(self):
        """Return list of all net names"""
        return [net['name'] for net in self.nets]
    
    def get_net_info(self, net_name):
        """Get detailed info for specific net"""
        for net in self.nets:
            if net['name'] == net_name:
                return net
        return None
```

**File: src/analyzers/diff_pair_detector.py**

```python
"""Detect differential pairs from netlist"""

import re
from typing import List, Dict, Tuple

class DiffPairDetector:
    def __init__(self):
        # Define patterns for differential pair naming
        self.patterns = [
            (r'(.+)_P$', r'(.+)_N$'),          # NAME_P / NAME_N
            (r'(.+)_DIFF_P$', r'(.+)_DIFF_N$'), # NAME_DIFF_P / NAME_DIFF_N
            (r'(.+)\+$', r'(.+)-$'),            # NAME+ / NAME-
            (r'(.+)_TX$', r'(.+)_RX$'),         # NAME_TX / NAME_RX (for some protocols)
        ]
    
    def detect_pairs(self, net_names: List[str]) -> List[Dict]:
        """
        Detect differential pairs from list of net names.
        
        Args:
            net_names: List of net names from netlist
            
        Returns:
            List of dictionaries with pair information:
            {
                'base_name': 'USB3_TX',
                'positive': 'USB3_TX_P',
                'negative': 'USB3_TX_N',
                'pattern': '_P/_N'
            }
        """
        pairs = []
        processed = set()
        
        for pattern_pos, pattern_neg in self.patterns:
            for net in net_names:
                if net in processed:
                    continue
                
                # Try to match positive pattern
                match_pos = re.match(pattern_pos, net)
                if match_pos:
                    base_name = match_pos.group(1)
                    
                    # Construct expected negative net name
                    # Extract the suffix from pattern and apply to base
                    neg_suffix = pattern_neg.split('$')[0].replace(r'(.+)', '')
                    expected_neg = base_name + neg_suffix
                    
                    if expected_neg in net_names:
                        pairs.append({
                            'base_name': base_name,
                            'positive': net,
                            'negative': expected_neg,
                            'pattern': self._get_pattern_name(pattern_pos)
                        })
                        
                        processed.add(net)
                        processed.add(expected_neg)
        
        return pairs
    
    def _get_pattern_name(self, pattern: str) -> str:
        """Get human-readable pattern name"""
        if '_P$' in pattern:
            return '_P/_N'
        elif '_DIFF_P$' in pattern:
            return '_DIFF_P/_DIFF_N'
        elif '+$' in pattern:
            return '+/-'
        elif '_TX$' in pattern:
            return '_TX/_RX'
        return 'unknown'


# Test with REAL exported data
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from parsers.netlist_parser import NetlistParser
    
    # Use YOUR actual exported netlist
    parser = NetlistParser('../../test_data/netlists/usb_board.NET')
    net_names = parser.get_net_names()
    
    print(f"Total nets: {len(net_names)}")
    print("Sample nets:", net_names[:10])
    print()
    
    detector = DiffPairDetector()
    pairs = detector.detect_pairs(net_names)
    
    print(f"Found {len(pairs)} differential pairs:")
    for pair in pairs:
        print(f"  {pair['base_name']:20} {pair['pattern']:15} "
              f"{pair['positive']} / {pair['negative']}")
```

**File: tests/test_diff_pairs.py**

```python
"""Test differential pair detection with REAL data"""

import unittest
import sys
sys.path.append('../src')

from parsers.netlist_parser import NetlistParser
from analyzers.diff_pair_detector import DiffPairDetector

class TestDiffPairDetectionRealData(unittest.TestCase):
    """Test with actual exported Altium netlists"""
    
    def test_usb_board(self):
        """Test with real USB board netlist"""
        parser = NetlistParser('../test_data/netlists/usb_board.NET')
        net_names = parser.get_net_names()
        
        detector = DiffPairDetector()
        pairs = detector.detect_pairs(net_names)
        
        # Verify we found pairs
        self.assertGreater(len(pairs), 0, "Should find at least one differential pair")
        
        # Verify specific pairs we know exist in this design
        pair_names = [p['base_name'] for p in pairs]
        self.assertIn('USB3_SSTX', pair_names, "Should find USB3 TX pair")
        self.assertIn('USB3_SSRX', pair_names, "Should find USB3 RX pair")
    
    def test_hdmi_board(self):
        """Test with real HDMI board netlist"""
        parser = NetlistParser('../test_data/netlists/hdmi_interface.NET')
        net_names = parser.get_net_names()
        
        detector = DiffPairDetector()
        pairs = detector.detect_pairs(net_names)
        
        # Verify HDMI pairs
        pair_names = [p['base_name'] for p in pairs]
        self.assertIn('HDMI_D0', pair_names, "Should find HDMI D0 pair")
        self.assertIn('HDMI_CLK', pair_names, "Should find HDMI CLK pair")
    
    def test_no_false_positives(self):
        """Ensure we don't detect pairs that don't exist"""
        # Single-ended nets that should NOT be detected as pairs
        single_nets = [
            'VCC_3V3', 'VCC_5V', 'GND', 
            'RESET', 'CLK_OUT', 'DATA_IN'
        ]
        
        detector = DiffPairDetector()
        pairs = detector.detect_pairs(single_nets)
        
        self.assertEqual(len(pairs), 0, "Should not find pairs in single-ended nets")

if __name__ == '__main__':
    unittest.main()
```

**Run tests:**

```bash
cd tests
python test_diff_pairs.py -v

# Expected output:
# test_hdmi_board (__main__.TestDiffPairDetectionRealData) ... ok
# test_no_false_positives (__main__.TestDiffPairDetectionRealData) ... ok
# test_usb_board (__main__.TestDiffPairDetectionRealData) ... ok
# 
# Ran 3 tests in 0.142s
# OK
```

#### Phase 3: Protocol Identification with AI (1 day)

**File: src/analyzers/protocol_identifier.py**

```python
"""Identify communication protocol for differential pairs"""

import openai
import os
from typing import Dict

class ProtocolIdentifier:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        
        # Heuristic database (fast, free fallback)
        self.keywords = {
            'USB 2.0': ['usb2', 'usb_d', 'dp', 'dm', 'usbd'],
            'USB 3.0': ['usb3', 'ss', 'superspeed', 'sstx', 'ssrx'],
            'PCIe Gen3': ['pcie', 'pci_', 'perst', 'refclk', 'pcie_'],
            'PCIe Gen4': ['pcie4', 'pciegen4'],
            'HDMI 2.0': ['hdmi', 'tmds', 'hdmi_d'],
            'MIPI CSI': ['mipi', 'csi', 'mipi_'],
            'MIPI DSI': ['dsi', 'mipi_dsi'],
            'Ethernet 1000Base-T': ['eth', 'mdi', 'rgmii', 'ethernet'],
            'LVDS': ['lvds'],
            'DisplayPort': ['dp_', 'displayport'],
        }
        
        # Protocol specifications database
        self.protocol_specs = {
            'USB 2.0': {
                'diff_impedance': 90,
                'max_mismatch_mils': 5,
                'min_gap_mils': 6,
                'max_gap_mils': 12
            },
            'USB 3.0': {
                'diff_impedance': 90,
                'max_mismatch_mils': 5,
                'min_gap_mils': 6,
                'max_gap_mils': 10
            },
            'PCIe Gen3': {
                'diff_impedance': 100,
                'max_mismatch_mils': 200,
                'min_gap_mils': 6,
                'max_gap_mils': 15
            },
            'HDMI 2.0': {
                'diff_impedance': 100,
                'max_mismatch_mils': 10,
                'min_gap_mils': 6,
                'max_gap_mils': 12
            },
            'MIPI CSI': {
                'diff_impedance': 100,
                'max_mismatch_mils': 10,
                'min_gap_mils': 5,
                'max_gap_mils': 10
            },
            'Ethernet 1000Base-T': {
                'diff_impedance': 100,
                'max_mismatch_mils': 20,
                'min_gap_mils': 8,
                'max_gap_mils': 15
            },
            'LVDS': {
                'diff_impedance': 100,
                'max_mismatch_mils': 10,
                'min_gap_mils': 6,
                'max_gap_mils': 12
            },
        }
    
    def identify(self, pair_info: Dict) -> Dict:
        """
        Identify protocol for a differential pair.
        
        Args:
            pair_info: Dict from DiffPairDetector with 'base_name', 'positive', 'negative'
            
        Returns:
            Dict with protocol info:
            {
                'protocol': 'USB 3.0',
                'confidence': 'high',  # 'high', 'medium', 'low'
                'specs': {...}  # Protocol specifications
            }
        """
        # Try heuristics first (fast, free)
        protocol = self._identify_by_heuristics(pair_info)
        
        if protocol != 'Unknown':
            return {
                'protocol': protocol,
                'confidence': 'high',
                'method': 'heuristics',
                'specs': self.protocol_specs.get(protocol, {})
            }
        
        # Fall back to AI (slower, costs money, but more accurate)
        protocol = self._identify_by_ai(pair_info)
        
        return {
            'protocol': protocol,
            'confidence': 'medium' if protocol != 'Unknown' else 'low',
            'method': 'ai',
            'specs': self.protocol_specs.get(protocol, {})
        }
    
    def _identify_by_heuristics(self, pair_info: Dict) -> str:
        """Fast keyword-based identification"""
        base_name = pair_info['base_name'].lower()
        
        for protocol, keywords in self.keywords.items():
            if any(kw in base_name for kw in keywords):
                return protocol
        
        return 'Unknown'
    
    def _identify_by_ai(self, pair_info: Dict) -> str:
        """AI-based protocol identification"""
        prompt = f"""
Identify the communication protocol for this differential pair:

Base name: {pair_info['base_name']}
Positive net: {pair_info['positive']}
Negative net: {pair_info['negative']}

Common protocols:
- USB 2.0, USB 3.0
- PCIe Gen3, PCIe Gen4
- HDMI 2.0, HDMI 1.4
- MIPI CSI, MIPI DSI
- Ethernet 1000Base-T
- LVDS
- DisplayPort

Return ONLY the protocol name from the list above, or "Unknown" if uncertain.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a PCB design expert specializing in high-speed interfaces."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            protocol = response.choices[0].message.content.strip()
            
            # Validate response is in our known protocols
            all_protocols = list(self.protocol_specs.keys()) + ['Unknown']
            if protocol in all_protocols:
                return protocol
            else:
                return 'Unknown'
                
        except Exception as e:
            print(f"AI identification failed: {e}")
            return 'Unknown'


# Test with real data
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from parsers.netlist_parser import NetlistParser
    from analyzers.diff_pair_detector import DiffPairDetector
    
    # Load real netlist
    parser = NetlistParser('../../test_data/netlists/usb_board.NET')
    net_names = parser.get_net_names()
    
    # Detect pairs
    detector = DiffPairDetector()
    pairs = detector.detect_pairs(net_names)
    
    # Identify protocols
    identifier = ProtocolIdentifier()
    
    print("Differential Pair Protocol Identification:")
    print("=" * 70)
    
    for pair in pairs:
        result = identifier.identify(pair)
        
        print(f"\n{pair['base_name']}")
        print(f"  Protocol: {result['protocol']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Method: {result['method']}")
        
        if result['specs']:
            print(f"  Specifications:")
            print(f"    - Differential Impedance: {result['specs']['diff_impedance']}Ω")
            print(f"    - Max Mismatch: {result['specs']['max_mismatch_mils']} mils")
            print(f"    - Coupling Gap: {result['specs']['min_gap_mils']}-{result['specs']['max_gap_mils']} mils")
```

#### Phase 4: AI Translation to DelphiScript (2 hours)

**Prompt to AI:**

```
I have working Python code that detects differential pairs from Altium 
netlist exports and identifies their protocols. The code has been tested 
with real data from actual Altium projects.

I need to convert it to DelphiScript for Altium Designer 24.01.

PYTHON CODE (diff_pair_detector.py):
[paste the entire DiffPairDetector class]

PYTHON CODE (protocol_identifier.py):
[paste the ProtocolIdentifier class]

TRANSLATION REQUIREMENTS:
1. Convert to DelphiScript syntax
2. Replace netlist file parsing with Altium API:
   - Use Board.Nets[i].Name instead of parsing .NET file
   - Get net count via Board.NetCount
3. Keep exact same detection logic (proven to work)
4. For protocol identification, keep both heuristics and AI methods
5. Use TStringList for net name lists
6. Use records for pair information and protocol specs
7. Add comprehensive logging to C:\Temp\AltiumDebug.log
8. Add error handling with try/except
9. Include comments explaining the logic

ALTIUM API:
- Board: IPCB_Board (from PCBServer.GetCurrentPCBBoard)
- Nets: Board.Nets[i] returns IPCB_Net
- Net name: Net.Name property

Generate the complete DelphiScript code.
```

**AI will generate DelphiScript. You review and save as:**

- `altium_scripts/DiffPairDetector.pas`
- `altium_scripts/ProtocolIdentifier.pas`

#### Phase 5: Altium Integration & Testing (2 days)

**Test procedure:**

```
1. Copy .pas files to Altium scripts folder:
   C:\Users\[YourName]\Documents\Altium\[Version]\Scripts\

2. Open the SAME PCB you exported the netlist from

3. DXP → Run Script → DiffPairDetector.pas

4. Compare results:
   - Python detected: USB3_SSTX, USB3_SSRX, HDMI_D0, HDMI_CLK
   - DelphiScript should detect: SAME pairs
   
5. Check log file: C:\Temp\AltiumDebug.log
   - Should show each net processed
   - Should show pairs found
   - Should show protocol identifications

6. If results match → Success!
   If not → Check log to see where it differs
```

**Integration checklist:**

```
□ Script runs without errors
□ Detects same pairs as Python version
□ Identifies same protocols as Python version
□ Log file shows detailed execution trace
□ Can create design rules from detected pairs
□ Rules appear in Altium's Design Rules panel
□ DRC enforces the new rules correctly
```

#### Deliverables

✅ Working Python code tested with YOUR real netlists  
✅ Unit tests passing with real data  
✅ AI-translated DelphiScript  
✅ Integrated with Altium API  
✅ Tested on actual PCB projects  
✅ Documentation on usage  

**Total time: ~1 week**

---

### Feature 1.2: Power Net Width Calculator

**Complexity:** ⭐⭐  
**Impact:** ⭐⭐⭐⭐⭐  
**Priority:** 10/10  
**Timeline:** 1 week

#### Phase 1: Export Data (30 minutes)

```
1. Open project with power distribution
2. Export netlist: File → Export → Protel Netlist
3. Export BOM: Reports → Bill of Materials → CSV
4. Save component datasheets to test_data/datasheets/
5. Note: Record actual voltages and currents for validation
```

#### Phase 2: Python Development (2-3 days)

**File: src/parsers/bom_parser.py**

```python
"""Parse Altium BOM CSV files"""

import csv
from typing import List, Dict

class BOMParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.components = []
        self.parse()
    
    def parse(self):
        """Parse BOM CSV"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                self.components.append({
                    'designator': row.get('Designator', ''),
                    'comment': row.get('Comment', ''),
                    'footprint': row.get('Footprint', ''),
                    'value': row.get('Value', ''),
                    'quantity': int(row.get('Quantity', 1))
                })
    
    def get_components(self) -> List[Dict]:
        """Return all components"""
        return self.components
    
    def find_by_type(self, component_type: str) -> List[Dict]:
        """Find components by type (resistor, capacitor, IC, etc.)"""
        results = []
        type_lower = component_type.lower()
        
        for comp in self.components:
            comment = comp['comment'].lower()
            designator = comp['designator'].upper()
            
            # Type detection heuristics
            if component_type == 'resistor' and (designator.startswith('R') or 'resistor' in comment):
                results.append(comp)
            elif component_type == 'capacitor' and (designator.startswith('C') or 'capacitor' in comment):
                results.append(comp)
            elif component_type == 'vrm' and any(kw in comment for kw in ['tps', 'ldo', 'buck', 'boost', 'regulator']):
                results.append(comp)
        
        return results


# Test with real BOM
if __name__ == '__main__':
    parser = BOMParser('../../test_data/boms/usb_board_BOM.csv')
    
    print(f"Total components: {len(parser.components)}")
    print("\nVoltage Regulators:")
    vrms = parser.find_by_type('vrm')
    for vrm in vrms:
        print(f"  {vrm['designator']}: {vrm['comment']}")
    
    print("\nCapacitors:")
    caps = parser.find_by_type('capacitor')
    print(f"  Found {len(caps)} capacitors")
```

**File: src/calculators/trace_width_calc.py**

```python
"""IPC-2152 trace width calculator"""

import math
from typing import Dict

class TraceWidthCalculator:
    """
    Calculate trace width using IPC-2152 standard.
    
    Based on empirical data from IPC-2152 "Standard for Determining 
    Current Carrying Capacity in Printed Board Design"
    """
    
    def __init__(self):
        # IPC-2152 curve fit coefficients
        # These are empirically derived from test data
        pass
    
    def calculate(self, 
                  current_amps: float,
                  temp_rise_celsius: float = 10.0,
                  copper_oz: float = 1.0,
                  is_external_layer: bool = True) -> Dict:
        """
        Calculate minimum trace width for given current.
        
        Args:
            current_amps: Maximum current in amperes
            temp_rise_celsius: Acceptable temperature rise above ambient (default 10°C)
            copper_oz: Copper weight in oz/ft² (default 1 oz = 35 µm)
            is_external_layer: True for outer layers (better cooling), False for internal
            
        Returns:
            Dictionary with calculation results:
            {
                'width_mils': Recommended width in mils (thousandths of inch)
                'width_mm': Recommended width in millimeters
                'current_density': Current density in A/mm²
                'temp_rise': Temperature rise used
                'safety_factor': Safety factor applied (1.25 = 25% margin)
            }
        """
        
        # Validate inputs
        if current_amps <= 0:
            raise ValueError("Current must be positive")
        if temp_rise_celsius <= 0:
            raise ValueError("Temperature rise must be positive")
        if copper_oz <= 0:
            raise ValueError("Copper weight must be positive")
        
        # Copper thickness in mils (1 oz/ft² = 1.37 mils = 0.035 mm)
        thickness_mils = copper_oz * 1.37
        
        # IPC-2152 empirical formula (simplified curve fit)
        # Cross-sectional area in square mils
        # A = (I / (k * ΔT^b))^(1/c)
        
        if is_external_layer:
            # External layers have better heat dissipation
            k = 0.048  # Constant for external layers
            b = 0.44   # Temperature exponent
            c = 0.725  # Current exponent
        else:
            # Internal layers have worse heat dissipation
            k = 0.024  # Constant for internal layers (half of external)
            b = 0.44
            c = 0.725
        
        # Calculate required cross-sectional area
        area_sq_mils = math.pow(
            current_amps / (k * math.pow(temp_rise_celsius, b)),
            1.0 / c
        )
        
        # Calculate width from area and thickness
        # Area = Width × Thickness
        width_mils = area_sq_mils / thickness_mils
        
        # Apply safety factor (25% margin)
        safety_factor = 1.25
        width_mils_safe = width_mils * safety_factor
        
        # Round up to nearest mil
        width_mils_final = math.ceil(width_mils_safe)
        
        # Convert to mm
        width_mm = width_mils_final * 0.0254
        
        # Calculate current density
        thickness_mm = thickness_mils * 0.0254
        area_mm2 = width_mm * thickness_mm
        current_density = current_amps / area_mm2 if area_mm2 > 0 else 0
        
        return {
            'width_mils': width_mils_final,
            'width_mm': round(width_mm, 3),
            'current_density_A_mm2': round(current_density, 2),
            'temp_rise_C': temp_rise_celsius,
            'safety_factor': safety_factor,
            'copper_oz': copper_oz,
            'layer_type': 'external' if is_external_layer else 'internal'
        }
    
    def get_recommendation_text(self, current_amps: float) -> str:
        """Get human-readable recommendation"""
        result_ext = self.calculate(current_amps, is_external_layer=True)
        result_int = self.calculate(current_amps, is_external_layer=False)
        
        return f"""
Power Trace Width Recommendation for {current_amps}A:

External Layers (Top/Bottom):
  - Minimum width: {result_ext['width_mils']} mils ({result_ext['width_mm']} mm)
  - Current density: {result_ext['current_density_A_mm2']} A/mm²
  
Internal Layers:
  - Minimum width: {result_int['width_mils']} mils ({result_int['width_mm']} mm)
  - Current density: {result_int['current_density_A_mm2']} A/mm²

Temperature rise: {result_ext['temp_rise_C']}°C above ambient
Safety factor: {result_ext['safety_factor']}x applied
Copper weight: {result_ext['copper_oz']} oz/ft²

Note: These calculations assume:
- Ambient temperature: 25°C
- No additional heat sources nearby
- Standard FR4 substrate
- Continuous DC current
"""


# Test with various currents
if __name__ == '__main__':
    calc = TraceWidthCalculator()
    
    test_currents = [
        ('LED indicator', 0.020),
        ('Logic power', 0.5),
        ('USB port', 2.0),
        ('Motor drive', 5.0),
        ('High power', 10.0),
    ]
    
    print("IPC-2152 Trace Width Calculations")
    print("=" * 70)
    
    for name, current in test_currents:
        result = calc.calculate(current)
        print(f"\n{name} ({current}A):")
        print(f"  External: {result['width_mils']} mils ({result['width_mm']} mm)")
        
        result_int = calc.calculate(current, is_external_layer=False)
        print(f"  Internal: {result_int['width_mils']} mils ({result_int['width_mm']} mm)")
```

**File: src/analyzers/power_net_analyzer.py**

```python
"""Analyze power distribution networks"""

from typing import List, Dict
import sys
sys.path.append('..')

from parsers.netlist_parser import NetlistParser
from parsers.bom_parser import BOMParser
from calculators.trace_width_calc import TraceWidthCalculator

class PowerNetAnalyzer:
    def __init__(self, netlist_path: str, bom_path: str):
        self.netlist = NetlistParser(netlist_path)
        self.bom = BOMParser(bom_path)
        self.calc = TraceWidthCalculator()
    
    def find_power_nets(self) -> List[Dict]:
        """
        Identify power nets from netlist.
        
        Returns:
            List of dicts with power net info:
            {
                'name': 'VCC_3V3',
                'voltage': 3.3,  # Parsed from name
                'pins': [...],   # Connected pins
            }
        """
        all_nets = self.netlist.get_net_names()
        power_nets = []
        
        # Power net detection keywords
        power_keywords = ['VCC', 'VDD', 'V3V3', 'V5V', 'V12V', '+3V3', '+5V', '+12V', 'VBUS']
        
        for net_name in all_nets:
            net_upper = net_name.upper()
            
            if any(kw in net_upper for kw in power_keywords):
                # Try to extract voltage from name
                voltage = self._extract_voltage_from_name(net_name)
                
                net_info = self.netlist.get_net_info(net_name)
                
                power_nets.append({
                    'name': net_name,
                    'voltage': voltage,
                    'pins': net_info['pins'] if net_info else [],
                    'pin_count': len(net_info['pins']) if net_info else 0
                })
        
        return power_nets
    
    def _extract_voltage_from_name(self, net_name: str) -> float:
        """Extract voltage value from net name"""
        name_upper = net_name.upper()
        
        # Common patterns
        voltage_map = {
            '3V3': 3.3, '3.3V': 3.3, 'V3V3': 3.3, '+3V3': 3.3,
            '5V': 5.0, 'V5V': 5.0, '+5V': 5.0, 'V5': 5.0,
            '12V': 12.0, 'V12V': 12.0, '+12V': 12.0,
            '1V8': 1.8, '1.8V': 1.8,
            '2V5': 2.5, '2.5V': 2.5,
        }
        
        for pattern, voltage in voltage_map.items():
            if pattern in name_upper:
                return voltage
        
        return 0.0  # Unknown
    
    def find_voltage_regulators(self) -> List[Dict]:
        """Find voltage regulator components from BOM"""
        vrms = self.bom.find_by_type('vrm')
        
        results = []
        for vrm in vrms:
            results.append({
                'designator': vrm['designator'],
                'part_number': vrm['comment'],
                'package': vrm['footprint']
            })
        
        return results
    
    def analyze_power_net(self, net_name: str, current_amps: float) -> Dict:
        """
        Analyze a specific power net and calculate trace requirements.
        
        Args:
            net_name: Name of the power net
            current_amps: Expected current draw (from user or datasheet)
            
        Returns:
            Dict with analysis results and recommendations
        """
        # Get net info
        net_info = next((n for n in self.find_power_nets() if n['name'] == net_name), None)
        
        if not net_info:
            raise ValueError(f"Net '{net_name}' not found or not identified as power net")
        
        # Calculate trace widths
        width_ext = self.calc.calculate(current_amps, is_external_layer=True)
        width_int = self.calc.calculate(current_amps, is_external_layer=False)
        
        return {
            'net_name': net_name,
            'voltage': net_info['voltage'],
            'current': current_amps,
            'pin_count': net_info['pin_count'],
            'external_width': width_ext,
            'internal_width': width_int,
            'recommendation': self._generate_recommendation(net_name, current_amps, width_ext, width_int)
        }
    
    def _generate_recommendation(self, net_name: str, current: float, 
                                width_ext: Dict, width_int: Dict) -> str:
        """Generate human-readable recommendation"""
        return f"""
Power Net: {net_name}
Current: {current}A

Trace Width Requirements:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
External Layers (Top/Bottom):
  Minimum: {width_ext['width_mils']} mils ({width_ext['width_mm']} mm)
  Current Density: {width_ext['current_density_A_mm2']} A/mm²
  
Internal Layers:
  Minimum: {width_int['width_mils']} mils ({width_int['width_mm']} mm)
  Current Density: {width_int['current_density_A_mm2']} A/mm²

Design Rules to Create:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Width constraint for {net_name} on top layer: {width_ext['width_mils']} mils
2. Width constraint for {net_name} on bottom layer: {width_ext['width_mils']} mils
3. Width constraint for {net_name} on internal layers: {width_int['width_mils']} mils

Additional Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Use multiple vias for layer transitions (min 2-3 vias)
- Keep traces short and direct
- Add decoupling capacitors near load
- Consider copper pours/planes for high current (>{current}A)
"""


# Test with real data
if __name__ == '__main__':
    # Use YOUR exported data
    analyzer = PowerNetAnalyzer(
        '../../test_data/netlists/usb_board.NET',
        '../../test_data/boms/usb_board_BOM.csv'
    )
    
    print("Power Distribution Network Analysis")
    print("=" * 70)
    
    # Find all power nets
    power_nets = analyzer.find_power_nets()
    print(f"\nFound {len(power_nets)} power nets:")
    for net in power_nets:
        print(f"  {net['name']:15} {net['voltage']}V  ({net['pin_count']} pins)")
    
    # Find voltage regulators
    vrms = analyzer.find_voltage_regulators()
    print(f"\nFound {len(vrms)} voltage regulators:")
    for vrm in vrms:
        print(f"  {vrm['designator']}: {vrm['part_number']}")
    
    # Analyze specific power net
    # (In real usage, current would come from datasheet or user input)
    print("\n" + "=" * 70)
    result = analyzer.analyze_power_net('VCC_3V3', current_amps=2.5)
    print(result['recommendation'])
```

#### Phase 3: AI-Powered Current Extraction (Optional, 1 day)

If you want to extract current specs from datasheets automatically:

**File: src/ai_interface/datasheet_analyzer.py**

```python
"""Extract specifications from component datasheets using AI"""

import openai
import os
from pathlib import Path

class DatasheetAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def extract_current_specs(self, pdf_path: str, voltage: float) -> dict:
        """
        Extract current specifications from voltage regulator datasheet.
        
        Args:
            pdf_path: Path to PDF datasheet
            voltage: Output voltage to look for
            
        Returns:
            {
                'max_current': 3.5,  # Amperes
                'typical_current': 2.8,
                'efficiency': 0.92,
                'confidence': 'high'
            }
        """
        # Note: This requires OpenAI's vision API or document parsing
        # For now, implementing a simplified text-based approach
        
        # TODO: Implement PDF text extraction
        # For MVP, can manually input current specs
        
        return {
            'max_current': 0.0,
            'typical_current': 0.0,
            'efficiency': 0.0,
            'confidence': 'low',
            'note': 'Datasheet parsing not yet implemented - please input manually'
        }
```

#### Phase 4: AI Translation (2 hours)

Translation prompt is similar to Feature 1.1. AI will generate:

- `PowerNetAnalyzer.pas`
- `TraceWidthCalculator.pas`

#### Phase 5: Integration & Testing (2 days)

Test on the SAME board you exported data from. Verify calculated widths match expectations.

**Total time: ~1 week**

---

### Feature 1.3: Stackup Template Manager

**Complexity:** ⭐  
**Impact:** ⭐⭐⭐⭐  
**Priority:** 9/10  
**Timeline:** 2-3 days

This feature is simpler - mostly data loading/management. Can be developed directly in DelphiScript or use the same workflow.

**Key components:**

- JSON/XML library of stackup templates
- Parser for template format
- Altium Layer Stack Manager API integration
- Simple GUI for template selection

**Deliverables:**

- Template library (10+ common stackups)
- Template loader script
- One-click application

---

### Feature 1.4: Passive Component Rating Verification

**Timeline:** 1 week  
**Approach:** Same as Features 1.1 and 1.2

Export BOM → Develop in Python → Translate → Integrate

---

### Feature 1.5: DFM Pre-Flight Checker

**Timeline:** 1 week  
**Approach:** Same workflow

Export design data → Develop checks in Python → Translate → Integrate

---

## TIER 2 FEATURES

Features 2.1-2.5 follow the same workflow:

1. Export relevant data
2. Develop in Python
3. AI translates
4. Integrate & test

---

## TIER 3 FEATURES

Advanced features (SI analysis, EMI, thermal) follow same pattern but may require:

- More complex data exports
- Integration with external tools
- More sophisticated algorithms

---

## DEVELOPMENT ROADMAP

### Phase 0: Setup & Proof of Concept (1 week)

**Week 1:**

- ✅ Export data from 2-3 real projects
- ✅ Setup Python environment
- ✅ Implement Feature 1.1 (Diff Pair Detector) completely
- ✅ Verify entire workflow works

**Success Criteria:**

- Python version works with real netlists
- AI translation successful
- DelphiScript version produces same results
- Proven workflow, ready to scale

---

### Phase 1: Tier 1 Features (3 months)

**Month 1: Features 1.1 & 1.2**

- Week 1-2: Differential pair detection (DONE in Phase 0)
- Week 3-4: Power net width calculator

**Month 2: Features 1.3, 1.4, 1.5**

- Week 5-6: Stackup templates + Passive verification
- Week 7-8: DFM checker

**Month 3: Polish & Documentation**

- Week 9-10: Bug fixes, optimization
- Week 11-12: Documentation, user guides

**Deliverables:**

- All Tier 1 features working
- Tested on multiple real projects
- User documentation
- Video tutorials

---

### Phase 2: Tier 2 Features (3 months)

**Month 4-6:**

- Conversational AI interface
- Impedance profiling
- PDN analysis automation
- Length matching groups
- BOM optimization

---

### Phase 3: Tier 3 Features (4 months)

**Month 7-10:**

- Signal integrity analysis
- EMI/ESD checking
- Thermal analysis
- Advanced optimizations

---

### Phase 4: Deployment (1 month)

**Month 11:**

- Installer creation
- Final testing
- User training materials
- Release

**Total Timeline: ~12 months**

---

## SUCCESS METRICS

### Quantitative

- **Rule Setup Time:** 80% reduction (4 hours → <1 hour)
- **DRC Violations:** 60% fewer in first spin
- **First-Pass Success:** 40% improvement
- **Time Saved:** 20-30 hours per project
- **PDN Issues:** 70% reduction in power-related respins

### Qualitative

- User satisfaction >4.5/5
- Adoption rate >80% within team
- Reduced expert review cycles
- Improved designer confidence

---

## CONCLUSION

This revised implementation plan uses a **pragmatic, proven workflow**:

1. **Export real data** from actual Altium projects
2. **Develop in Python** using that real data (excellent debugging)
3. **AI translates** to DelphiScript (automated)
4. **Integrate** with Altium API (focused effort)

### Key Advantages

✅ **Test with real data** from YOUR designs  
✅ **Fast Python debugging** vs. Altium ShowMessage hell  
✅ **Proven logic** before translation  
✅ **Simple AI translation** - just a prompt  
✅ **Focused integration** - only API connections need Altium debugging  

### Critical Success Factors

1. **Start with real data export** - don't skip Phase 0
2. **Test thoroughly in Python** - save time later
3. **Trust the AI translation** - but always review
4. **Integrate incrementally** - one feature at a time

### Next Steps

**Day 1:**

1. Export netlists from 2-3 completed projects
2. Export BOMs from same projects
3. Setup Python environment
4. Verify exports contain expected data

**Week 1:**

1. Implement diff pair detector in Python
2. Test with real netlists
3. Verify results match manual analysis
4. Prove the workflow

**Week 2:**

1. AI translate to DelphiScript
2. Integrate with Altium
3. Test on real PCB
4. Celebrate working prototype!

Then scale to remaining features with confidence.

---

**Document Version:** 2.0  
**Status:** Ready for Implementation  
**Estimated Effort:** 12 months  
**Risk Level:** Low (proven workflow)

**Start Date:** [Your Start Date]  
**Target Completion:** [Start + 12 months]

---
