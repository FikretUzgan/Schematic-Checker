# Software Specification Document
## Automated Component Rating Verification System for Altium Designer

---

**Document Version:** 1.0  
**Date:** February 14, 2026  
**Project:** Auto_Altium  
**Target Platform:** Altium Designer 24.01  
**Development Language:** Python 3.x  

---

## 1. EXECUTIVE SUMMARY

### 1.1 Purpose
The Automated Component Rating Verification System is a Python-based tool designed to automate the verification of passive component derating in PCB designs created with Altium Designer. The system analyzes netlists and Bill of Materials (BOM) to ensure components are not operating beyond their rated specifications, with special consideration for switching paths and transient conditions.

### 1.2 Scope
This system provides:
- Automated voltage/power dissipation analysis
- Component derating verification (capacitors, resistors, inductors)
- Library consistency auditing
- Switching path detection and worst-case analysis
- Multi-format reporting (Excel, HTML, GUI dashboard)
- Interactive voltage confirmation workflow

### 1.3 Key Benefits
- **Time Savings**: Reduces manual component verification from hours to minutes
- **Error Prevention**: Catches over-stressed components before manufacturing
- **Library Quality Control**: Enforces standard library usage and footprint consistency
- **Regulatory Compliance**: Documents derating analysis for certification requirements
- **Worst-Case Analysis**: Identifies switching paths that may experience transient over-stress

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   File       │  │   Voltage    │  │   Results    │  │
│  │  Selection   │  │ Confirmation │  │  Dashboard   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   CORE ANALYSIS ENGINE                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Netlist    │  │   Voltage    │  │   Rating     │  │
│  │    Parser    │  │   Analyzer   │  │   Analyzer   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  REPORT GENERATORS                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Excel     │  │     HTML     │  │     GUI      │  │
│  │   Reporter   │  │   Reporter   │  │   Dashboard  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  COMPONENT DATABASE                      │
│         (Derating Factors, Power Ratings, etc.)         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Module Structure

```
Auto_Altium/
├── run_rating_verification_v2.py    # Main application entry point
├── data/
│   └── component_database.json      # Derating factors & power ratings
├── src/
│   ├── parsers/
│   │   ├── netlist_parser.py        # Protel netlist parser
│   │   └── bom_parser.py            # BOM file parser
│   ├── analyzers/
│   │   ├── net_voltage_analyzer.py  # Voltage detection & inference
│   │   └── passive_rating_analyzer.py # Component rating verification
│   ├── generators/
│   │   ├── excel_generator.py       # Excel report with multiple tabs
│   │   └── html_generator.py        # HTML executive summary
│   └── gui/
│       └── rating_gui.py            # Tkinter-based user interfaces
└── altium_scripts/
    └── [DelphiScript versions]      # Future Altium integration
```

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 Input Processing

#### FR-1.1: Netlist Parsing
**Priority:** Critical  
**Description:** Parse Protel format netlist files (.NET) exported from Altium Designer  
**Inputs:** .NET file path  
**Outputs:** Component dictionary, net connectivity map  
**Validation:**
- Must handle multi-line component definitions
- Must extract component properties (DESCRIPTION, PARTTYPE, FOOTPRINT, Library Name)
- Must build pin-to-net mapping for all components

#### FR-1.2: Component Database Loading
**Priority:** Critical  
**Description:** Load derating factors and power ratings from JSON database  
**Inputs:** component_database.json  
**Outputs:** Configuration dictionary with:
- Marginal threshold (default: 80%)
- Capacitor derating factors by type (MLCC, Tantalum, etc.)
- Resistor power ratings by footprint (0402, 0603, etc.)
- Inductor derating factors

### 3.2 Voltage Analysis

#### FR-2.1: Ground Net Detection
**Priority:** Critical  
**Description:** Automatically identify ground (0V reference) nets  
**Algorithm:**
- Search for keywords: GND, VSS, REF_0V, BAT_NEG, COM
- Case-insensitive matching
- Multiple ground nets supported

#### FR-2.2: Voltage Candidate Detection
**Priority:** High  
**Description:** Identify potential power supply nets using pattern matching  
**Patterns:**
- Direct voltage notation: 3V3, 5V0, 12V
- Prefix notation: VCC, VDD, VBAT, VBUS
- Suffix notation: V_3V3, RAIL_5V
**Output:** List of candidate nets with inferred voltages

#### FR-2.3: Interactive Voltage Confirmation
**Priority:** High  
**Description:** Present detected voltage candidates to user for confirmation  
**GUI Features:**
- List view with net name and detected voltage
- Checkbox for confirmation
- Editable voltage value
- Bulk confirm/reject options
**User Actions:**
- Confirm and use detected voltage
- Edit voltage value before confirming
- Reject (ignore this net)

#### FR-2.4: Switching Path Detection
**Priority:** High  
**Description:** Identify nets that connect to ground through transistor switches  
**Algorithm:**
1. Find all transistor/switch components (Q*, TR* designators)
2. For each switching component:
   - Get all connected nets
   - If any net is ground, mark other nets as "switchable ground"
3. Components on switchable ground nets may see worst-case voltage

### 3.3 Component Analysis

#### FR-3.1: Capacitor Derating Analysis
**Priority:** Critical  
**Description:** Verify capacitor voltage ratings with derating  
**Parameters:**
- Applied voltage (from net analysis)
- Rated voltage (extracted from DESCRIPTION/PARTTYPE)
- Derating factor (from database, default 0.8 for MLCC)
**Calculations:**
```
Derated_Rating = Rated_Voltage × Derating_Factor
Usage_Ratio = Applied_Voltage / Derated_Rating
```
**Verdicts:**
- `OK`: Usage_Ratio < 80%
- `Marginal`: 80% ≤ Usage_Ratio ≤ 100%
- `NOK`: Usage_Ratio > 100%
- `Unknown (Missing Data)`: Rated voltage not found

#### FR-3.2: Resistor Power Dissipation Analysis
**Priority:** Critical  
**Description:** Calculate power dissipation and verify against derating  
**Parameters:**
- Applied voltage (from net analysis)
- Resistance value (extracted from part name)
- Power rating (inferred from footprint or explicit rating)
- Derating factor (default 0.8)
**Calculations:**
```
Applied_Power = V² / R
Derated_Rating = Power_Rating × Derating_Factor
Usage_Ratio = Applied_Power / Derated_Rating
```
**Special Cases:**
- If resistance cannot be parsed: `Unknown (R=?)`
- Missing power rating: `Unknown (Missing Data)`

#### FR-3.3: Inductor Current Analysis
**Priority:** Medium  
**Description:** Verify inductor current ratings with derating  
**Parameters:**
- Applied current (placeholder: 0.0A in current implementation)
- Rated current (extracted from DESCRIPTION/PARTTYPE)
- Derating factor (default 0.7)
**Note:** Current analysis requires PCB layout or simulation data for full implementation

#### FR-3.4: Generic Component Audit
**Priority:** High  
**Description:** Audit library consistency for all component types  
**Applies to:** Connectors (J, CN), ICs (U, IC), Diodes (D), Transistors (Q, TR), etc.  
**Output:** Library audit verdict without electrical analysis

### 3.4 Library Consistency Auditing

#### FR-4.1: Standard Library Enforcement
**Priority:** Critical  
**Description:** Verify components use approved company library  
**Rule:** Library Name field must equal "triomobil.DbLib"  
**Verdict:** FAIL if non-standard library detected  
**Reason:** "Library Error: Non-Standard Library ({library_name})"

#### FR-4.2: Footprint-to-Part Size Matching
**Priority:** Critical  
**Description:** Verify footprint matches part name size code  
**Algorithm:**
1. Extract size code from part name (0402, 0603, 0805, etc.)
2. Extract size code from FOOTPRINT field
3. Compare for exact match
**Examples:**
- ✅ PASS: "RES-SMD-0603 10K" with FOOTPRINT "0603"
- ❌ FAIL: "RES-SMD-0603 10K" with FOOTPRINT "0402"
**Verdict:** FAIL if mismatch detected  
**Reason:** "Library Error: Footprint Mismatch! (Part: 0603, PCB: 0402)"

### 3.5 Switching Path Worst-Case Analysis

#### FR-5.1: Switching Path Verdict Logic
**Priority:** High  
**Description:** Apply special verdict rules for components on switching paths  
**Rules:**
1. If component is on switching path AND voltage detected:
   - If derating verdict is `OK`: Change to `OK (Switching)`
   - If derating verdict is `NOK`: Change to `User Review Required`
   - If derating verdict is `Marginal`: Keep as `Marginal (Switching)`
2. Append `[Switching Path]` to reason field

**Rationale:**
- `OK (Switching)`: Component is safe even during worst-case switching transients
- `User Review Required`: Requires manual analysis of switching waveforms/duty cycle
- System cannot determine if transient overstress is acceptable without detailed analysis

### 3.6 Integrated Audit Verdict

#### FR-6.1: Combined Audit Verdict
**Priority:** Critical  
**Description:** Generate final audit verdict combining library and derating checks  
**Logic:**
```python
if library_audit == "FAIL":
    final_verdict = "FAIL"
elif derating_verdict in ["NOK", "Unknown"]:
    final_verdict = "FAIL"  
elif derating_verdict == "Marginal" and library_audit == "OK":
    final_verdict = "WARNING"
else:
    final_verdict = "OK"
```
**Purpose:** Single field indicates component pass/fail status for quality control

---

## 4. REPORTING REQUIREMENTS

### 4.1 Excel Report Generator

#### FR-7.1: Multi-Tab Excel Workbook
**Priority:** Critical  
**Tabs:**
1. **Summary** - High-level statistics
2. **Verification Details** - Complete component analysis
3. **Library Errors** - Components with library issues
4. **Derating Errors** - Components with NOK/Marginal verdicts

#### FR-7.2: Summary Sheet
**Contents:**
- Total components checked
- Verdict breakdown (OK, Marginal, NOK counts)
- Error summary (Library errors, Derating errors)
- Component type breakdown

#### FR-7.3: Verification Details Sheet
**Columns:**
- Designator, Type, Description, Footprint
- Applied, Rating, Derated (voltage/power/current)
- Verdict, Reason
- AuditVerdict, AuditReason

**Formatting:**
- Header row: Bold, centered
- Color coding by verdict:
  - 🟢 Green (#C6EFCE): OK verdicts
  - 🟡 Yellow (#FFEB9C): Marginal verdicts
  - 🔴 Light Red (#FFC7CE): NOK verdicts
  - 🔴 Bright Red (#FF0000): AuditVerdict = FAIL (overrides other colors)
  - 🔵 Light Blue (#ADD8E6): AuditVerdict = WARNING
  - Gray (#D3D3D3): Unknown verdicts
- Auto-adjusted column widths (Reason/AuditReason: 30 chars, others: 15 chars)
- Sorted: NOK → Marginal → OK

#### FR-7.4: Library Errors Sheet
**Filter:** AuditReason contains "Library Error"  
**Purpose:** Isolate components with non-standard libraries or footprint mismatches  
**Same formatting as Verification Details**

#### FR-7.5: Derating Errors Sheet
**Filter:** Verdict starts with "NOK" or "Marginal"  
**Purpose:** Isolate components with electrical overstress  
**Same formatting as Verification Details**

### 4.2 HTML Executive Summary

#### FR-8.1: HTML Report Generation
**Priority:** High  
**Contents:**
- Project metadata (filename, date, total components)
- Summary statistics with visual indicators
- Critical issues highlighted
- Filterable component table
- Embedded CSS styling for professional appearance

#### FR-8.2: Color-Coded Summary
**Visual Elements:**
- Red badge: Critical failures (library + derating errors)
- Yellow badge: Warnings (marginal components)
- Green badge: Passed components

### 4.3 GUI Dashboard

#### FR-9.1: Interactive Dashboard
**Priority:** High  
**Features:**
- Tree view with all components
- Color-coded rows (same scheme as Excel)
- Summary statistics display
- Sort by verdict (NOK → Marginal → OK)
- Export buttons (Excel, HTML)
- Close button

#### FR-9.2: Color Synchronization
**Requirement:** GUI colors must match Excel report colors  
**Tag Mapping:**
- 'FAIL': Bright red background, white text
- 'NOK': Light red background, dark red text
- 'Marginal': Yellow background, dark yellow text
- 'OK': Light green background, dark green text
- 'WARNING': Light blue background, navy text
- 'UNKNOWN': Gray background, black text

**Priority Logic:**
1. If AuditVerdict == 'FAIL' → 'FAIL' tag (bright red)
2. Else if AuditVerdict == 'WARNING' → 'WARNING' tag (blue)
3. Else if Verdict starts with 'User Review' → 'WARNING' tag
4. Else if Verdict starts with 'OK' → 'OK' tag (includes "OK (Switching)")
5. Else if Verdict starts with 'Marginal' → 'Marginal' tag
6. Else if Verdict starts with 'NOK' → 'NOK' tag
7. Else → 'UNKNOWN' tag

---

## 5. DATA STRUCTURES

### 5.1 Component Dictionary
```python
{
    'designator': str,        # e.g., "R131"
    'type': str,              # e.g., "R", "C", "L"
    'DESCRIPTION': str,       # From netlist
    'PARTTYPE': str,          # From netlist
    'FOOTPRINT': str,         # From netlist
    'Library Name': str,      # From netlist
    'comment': str,           # Optional field
    'value': str              # Optional field
}
```

### 5.2 Analysis Result Dictionary
```python
{
    'Designator': str,
    'Type': str,              # Component prefix
    'Description': str,       # Human-readable part name
    'Footprint': str,         # PCB footprint
    'Applied': str,           # "3.30V" or "12.50mW"
    'Rating': str,            # "16.00V" or "63.00mW"
    'Derated': str,           # "12.80V" or "50.40mW"
    'Verdict': str,           # "OK", "Marginal", "NOK", "OK (Switching)", "User Review Required"
    'Reason': str,            # Detailed explanation
    'AuditVerdict': str,      # "OK", "WARNING", "FAIL"
    'AuditReason': str        # Library audit explanation
}
```

### 5.3 Component Database Schema
```json
{
  "settings": {
    "marginal_threshold_percentage": 80
  },
  "capacitors": {
    "derating_factors": {
      "MLCC": 0.8,
      "Electrolytic": 0.8,
      "Tantalum": 0.8,
      "Film": 0.7,
      "Default": 0.8
    }
  },
  "resistors": {
    "footprint_power_ratings_watts": {
      "0201": 0.05,
      "0402": 0.063,
      "0603": 0.1,
      "0805": 0.125,
      "1206": 0.25,
      "1210": 0.5,
      "2010": 0.75,
      "2512": 1.0
    },
    "default_derating_factor": 0.8
  },
  "inductors": {
    "default_derating_factor": 0.7
  }
}
```

---

## 6. ALGORITHMS

### 6.1 Voltage Extraction Regex
```python
# Pattern: number followed by 'V'
pattern = r'(\d+(?:\.\d+)?)\s*V'
# Examples: "16V", "3.3V", "100 V"
```

### 6.2 Resistance Value Parsing
**Priority Order:**
1. Values with units: `100K`, `4.7R`, `1M`
2. Standalone numbers: `100` (after filtering footprint codes)
3. Fallback: First number found

**Unit Conversion:**
- `K` → × 1,000
- `M` → × 1,000,000
- `R` → × 1 (ohms)

### 6.3 Power Rating Inference
**Priority Order:**
1. Explicit wattage in part name:
   - Fractional: `1/10W`, `1/16W`
   - Decimal: `0.1W`, `100mW`
2. Footprint code in part name: `0603` → 0.1W (from database)
3. FOOTPRINT field: Extract 4-digit code → lookup in database
4. Default: 0.063W (0402 equivalent)

### 6.4 Sorting Algorithm
**Component List Sorting:**
```python
def get_sort_key(verdict_string):
    if verdict_string.startswith('NOK'): return 0      # Highest priority
    if verdict_string.startswith('Marginal'): return 1
    if verdict_string.startswith('OK'): return 2
    return 3                                            # Unknown/other
```
**Purpose:** Show problem components at top of reports

---

## 7. USER INTERFACE SPECIFICATIONS

### 7.1 Netlist Selection Page
**Type:** Modal dialog  
**Elements:**
- Title: "Select Netlist File for Analysis"
- File path display (read-only text field)
- Browse button (opens file dialog, filter: *.NET)
- Confirm button (validates file exists, proceeds to analysis)
- Cancel button (exits application)

**Validation:**
- File must exist
- File must have .NET extension
- Display error message if invalid

### 7.2 Voltage Confirmation GUI
**Type:** Modal dialog  
**Elements:**
- Title: "Confirm Detected Voltage Rails"
- Instructions label
- Scrollable list with checkboxes:
  - Net name (read-only)
  - Detected voltage (editable)
  - Action checkbox (confirm/reject)
- Buttons:
  - "Confirm Selected" (proceeds with checked items)
  - "Skip All" (proceeds with no voltage assumptions)

**Behavior:**
- User can edit voltage values before confirming
- Unchecked items are ignored in analysis
- If all items skipped, analysis proceeds with 0V for all nets

### 7.3 Results Dashboard
**Type:** Modal dialog  
**Elements:**
- Title: "Rating Verification Dashboard - V2.0"
- Summary section:
  - Total components
  - Pass count (green text)
  - Fail count (red text)
  - Warning count (yellow text)
- Tree view table (sortable, scrollable)
- Action buttons:
  - "Export to Excel" (regenerates .xlsx)
  - "Export to HTML" (regenerates .html)
  - "Close"

**Theme:** Dark mode with high contrast (background: #1e1e1e, text: white)

---

## 8. ERROR HANDLING

### 8.1 File Not Found
**Trigger:** Netlist file path invalid  
**Response:** Display error dialog, return to file selection

### 8.2 Parse Errors
**Trigger:** Netlist format incorrect or corrupted  
**Response:** Log warning, skip malformed components, continue analysis

### 8.3 Missing Component Data
**Trigger:** Required fields (DESCRIPTION, PARTTYPE) empty  
**Response:** 
- Set Verdict = "Unknown (Missing Data)"
- Set AuditVerdict = "FAIL"
- Include in Library Errors tab

### 8.4 Database Load Failure
**Trigger:** component_database.json missing or invalid  
**Response:** Display critical error, exit application

### 8.5 Resistance Parsing Failure
**Trigger:** Cannot extract resistance from part name  
**Response:**
- Set Applied = "0.00mW"
- Set Verdict = "Unknown (R=?)"
- Set Reason = "Could not parse resistance value"

---

## 9. PERFORMANCE REQUIREMENTS

### 9.1 Processing Speed
- **Target:** Process 500 components in < 5 seconds (on typical desktop)
- **Maximum:** 2000 components in < 30 seconds

### 9.2 Memory Usage
- **Maximum:** 200 MB RAM for typical project (500 components)

### 9.3 File Size Limits
- **Netlist:** No hard limit (tested up to 50,000 lines)
- **Excel Output:** Excel 2007+ format (handles 1M+ rows)

---

## 10. QUALITY ATTRIBUTES

### 10.1 Reliability
- **Zero Crashes:** Application must handle all invalid inputs gracefully
- **Data Integrity:** No data loss during export operations
- **Reproducibility:** Same inputs always produce identical outputs

### 10.2 Usability
- **Learning Curve:** New users can complete analysis in < 10 minutes
- **Error Messages:** Clear, actionable guidance (no technical jargon)
- **Visual Feedback:** Progress indicators for long operations

### 10.3 Maintainability
- **Code Documentation:** All functions have docstrings
- **Modularity:** Clear separation of parsers, analyzers, generators
- **Configuration:** Derating factors externalized to JSON file

### 10.4 Extensibility
- **New Component Types:** Add to analysis_prefixes list
- **New Derating Rules:** Update component_database.json
- **New Report Formats:** Implement new generator class

---

## 11. COMPLIANCE & STANDARDS

### 11.1 Design Standards Referenced
- **IPC-2221B:** Generic Standard on Printed Board Design
- **IPC-9592B:** Requirements for Power Conversion Devices for the Computer and Telecommunications Industries
- Industry standard derating: 80% for resistors/capacitors (configurable)

### 11.2 Derating Policy
**Capacitors:**
- Voltage derating: 80% (0.8× rated voltage)
- Temperature considerations: Not implemented (assumes 25°C nominal)

**Resistors:**
- Power derating: 80% (0.8× rated power)
- Assumes steady-state DC operation

**Inductors:**
- Current derating: 70% (0.7× rated current)
- Assumes continuous current rating, not saturation current

---

## 12. FUTURE ENHANCEMENTS

### 12.1 Approved for V2.0 Development
**Status:** Approved - Implementation pending

#### Enhancement 1: Save/Load Voltage Configuration
**Priority:** High  
**Description:** Persist confirmed voltage rails to JSON file per project  
**Benefit:** 90% time savings for repeat analyses - users don't need to re-confirm voltages  
**Implementation:**
```python
# After voltage confirmation:
save_voltage_config(netlist_path, confirmed_voltages)
# Next run:
cached_voltages = load_voltage_config(netlist_path)
# Offer "Use saved voltages?" dialog
```

#### Enhancement 6: PDF Report Generation
**Priority:** High  
**Description:** Generate professional PDF reports for archival and customer delivery  
**Benefit:** Better suited for audits and certifications than Excel/HTML  
**Implementation:** Use `weasyprint` or `reportlab` library

#### Enhancement 7: Interactive Voltage Map Visualization
**Priority:** Medium  
**Description:** HTML network graph showing voltage propagation through design  
**Benefit:** Visual debugging of voltage distribution  
**Technology:** `vis.js` or `D3.js` for interactive network diagrams

#### Enhancement 8: Comparison Mode (Design Revisions)
**Priority:** High  
**Description:** Compare two netlist versions and show differences  
**Output:**
- New components added
- Removed components  
- Changed verdicts (OK→NOK, etc.)
- Delta in failure counts  
**CLI:** `python run_v2.py --compare RevA.NET RevB.NET`

#### Enhancement 9: Progress Bar for Large Designs
**Priority:** Low  
**Description:** Add `tqdm` progress bar for 1000+ component designs  
**Benefit:** User feedback during long-running analyses

#### Enhancement 11: Statistics Dashboard Banner
**Priority:** Low  
**Description:** Add summary banner to Excel Verification Details sheet  
**Format:**
```
┌─────────────────────────────────────────────┐
│ 🔴 FAILED: 12  🟡 WARNING: 5  🟢 PASSED: 483 │
└─────────────────────────────────────────────┘
```

#### Enhancement 18: GUI Tooltips
**Priority:** Medium  
**Description:** Hover tooltips explaining technical terms  
**Examples:**
- "Derated" → "Rating after applying 80% derating factor for safety margin"
- "Switching Path" → "Circuit controlled by transistor; may see transient overstress"

#### Enhancement 20: Recent Files List
**Priority:** Medium  
**Description:** "Recently Analyzed" dropdown with last 5 netlist files  
**Benefit:** Faster workflow for engineers working on multiple projects

#### Enhancement 23: Custom Report Templates
**Priority:** Low  
**Description:** Jinja2 templates for company-specific HTML formatting  
**Use Case:** Company logos, custom headers, certification compliance

### 12.2 Under Review
**Status:** Pending team discussion

#### Enhancement 5: Component Exemption List
**Description:** Allow users to mark specific components as exempt from failures  
**Use Case:** TVS diodes, pulse-rated components, intentional overstress  
**Concerns:** May mask real issues if misused  
**Decision:** Pending collaboration with colleagues

### 12.3 Future Phases (V3.0+)

#### Phase 2: Command-Line Interface (CLI)
**Priority:** Medium  
**Description:** Enable automation and batch processing  
**Examples:**
```bash
python run_rating_verification_v2.py --netlist path.NET --auto-confirm --output results/
python run_rating_verification_v2.py --batch folder/*.NET --config voltages.json
```
**Benefit:** CI/CD integration, automated regression testing in build pipelines

#### Phase 3: Current Analysis (Real Implementation)
- Parse PCB layout to extract trace widths
- Calculate trace resistance and voltage drop
- Determine actual current through inductors
- Verify connector current ratings
- Import simulation results (LTspice, PSPICE)

#### Phase 4: Thermal Analysis
- Import thermal simulation results
- Adjust derating based on ambient temperature
- Flag components in hot zones

#### Phase 5: Altium Integration
- Translate Python code to DelphiScript
- Integrate with Altium API for direct netlist access
- In-PCB annotations for failed components
- One-click verification from Altium menu

#### Phase 6: Advanced Features
- Database lookup for actual component datasheets (Octopart API)
- AI-powered component recommendation (suggest higher-rated alternatives)
- Email notifications for automated builds
- Trend analysis over time (failures dashboard)

---

## 13. TESTING REQUIREMENTS

### 13.1 Unit Testing
**Modules to Test:**
- `netlist_parser.py`: Parse component definitions, net extraction
- `passive_rating_analyzer.py`: Verdict logic, derating calculations
- `net_voltage_analyzer.py`: Voltage detection patterns

**Test Cases:**
- Valid netlist parsing: 10+ test netlists
- Edge cases: Empty nets, missing fields, special characters
- Calculation accuracy: Known component scenarios

### 13.2 Integration Testing
**Scenarios:**
- End-to-end: Netlist → Analysis → Excel/HTML generation
- GUI workflow: File selection → Voltage confirmation → Results display
- Error recovery: Invalid file, corrupted netlist, missing database

### 13.3 Acceptance Testing
**Criteria:**
- User can complete analysis of real project in < 5 minutes
- All library errors correctly identified
- All overstressed components flagged (0 false negatives)
- Acceptable false positive rate (< 5% for marginal threshold)

---

## 14. DEPLOYMENT

### 14.1 System Requirements
**Operating System:** Windows 10/11 (primary), Linux/macOS (untested)  
**Python:** 3.8 or higher  
**Dependencies:**
```
pandas >= 1.3.0
openpyxl >= 3.0.0
tkinter (included with Python on Windows)
```

### 14.2 Installation
```bash
# Clone repository
git clone <repository_url>

# Install dependencies
pip install pandas openpyxl

# Run application
python run_rating_verification_v2.py
```

### 14.3 Configuration
**Edit `data/component_database.json` to customize:**
- Marginal threshold percentage (default: 80%)
- Derating factors by component type
- Power ratings by footprint size

---

## 15. GLOSSARY

| Term | Definition |
|------|------------|
| **Derating** | Operating a component below its maximum rated specifications to improve reliability |
| **Verdict** | Analysis result for electrical stress (OK, Marginal, NOK, Unknown) |
| **AuditVerdict** | Combined result for library compliance and electrical stress (OK, WARNING, FAIL) |
| **Switching Path** | Circuit path where voltage is controlled by a transistor, potentially causing transient overstress |
| **Marginal** | Component operating between 80-100% of derated rating (caution zone) |
| **NOK** | Not OK - Component exceeds derated rating (failure) |
| **MLCC** | Multi-Layer Ceramic Capacitor |
| **Netlist** | File describing electrical connections between components in a PCB design |
| **Footprint** | Physical PCB land pattern for a component |

---

## 16. REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | Auto_Altium Team | Initial specification document - V1.0 stable release |
| 1.1 | 2026-02-14 | Auto_Altium Team | Updated Future Enhancements with approved V2.0 features (1, 6, 7, 8, 9, 11, 18, 20, 23), CLI planned for future, Enhancement 5 under review |

---

## 17. APPENDICES

### Appendix A: Sample Netlist Format
```
[
R131
(
DESCRIPTION=RES-SMD-0402 324R %5
FOOTPRINT=0402
LIBREFERENCE=RES0402
Library Name=triomobil.DbLib
)
]
```

### Appendix B: Configuration File Example
See Section 5.3 for full JSON schema.

### Appendix C: Color Codes Reference
- Green (#C6EFCE): OK - Component passes all checks
- Yellow (#FFEB9C): Marginal/WARNING - Component in caution zone
- Light Red (#FFC7CE): NOK - Component fails derating
- Bright Red (#FF0000): FAIL - Component fails audit (library or derating)
- Light Blue (#ADD8E6): WARNING - Requires user review
- Gray (#D3D3D3): UNKNOWN - Missing data

---

**END OF SPECIFICATION DOCUMENT**
