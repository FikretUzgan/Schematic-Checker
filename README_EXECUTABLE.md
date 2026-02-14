# Auto_Altium Rating Verifier

## Windows Executable - Quick Start Guide

**Version:** 1.0  
**Release Date:** February 14, 2026

---

## What is This?

Auto_Altium Rating Verifier is a tool that automatically checks if components in your PCB design are rated correctly and not being operated beyond their specifications. It analyzes:

- ✅ **Capacitor voltage ratings** with derating
- ✅ **Resistor power dissipation**
- ✅ **Inductor current ratings**
- ✅ **Library consistency** (standard parts, footprint matching)
- ✅ **Switching path worst-case analysis**

---

## System Requirements

- **OS:** Windows 10 or Windows 11
- **RAM:** 200 MB minimum
- **Disk Space:** 100 MB
- **Dependencies:** None (fully standalone)

**Note:** No Python installation required!

---

## How to Use

### Step 1: Export Netlist from Altium

1. Open your PCB project in Altium Designer
2. Go to: **File → Export → Protel Netlist**
3. Save as `YourProject.NET`

### Step 2: Run the Verifier

1. Double-click `AutoAltium_RatingVerifier.exe`
2. Click **Browse** to select your `.NET` file
3. Click **Confirm** to proceed

### Step 3: Confirm Voltage Rails

1. Review detected voltage nets (e.g., 3V3, 5V0, 12V)
2. Edit voltages if needed
3. Check boxes to confirm
4. Click **Confirm Selected**

### Step 4: View Results

The dashboard will show:
- 🟢 **Green:** Component passes all checks
- 🟡 **Yellow:** Marginal or needs user review
- 🔴 **Red:** Component fails (library error or over-stressed)

### Step 5: Export Reports

Click one of:
- **Export to Excel** → Detailed 4-tab report
- **Export to HTML** → Executive summary

Reports are saved next to your netlist file.

---

## Understanding the Results

### Excel Report Tabs

1. **Summary** - Overall statistics
   - Total components checked
   - Pass/Fail/Warning counts
   - Breakdown by component type

2. **Verification Details** - Complete analysis
   - All components with verdicts
   - Applied vs. Rated values
   - Color-coded by status

3. **Library Errors** - Components with library issues
   - Non-standard library parts
   - Footprint mismatches

4. **Derating Errors** - Over-stressed components
   - Components exceeding ratings
   - Marginal components (80-100%)

### Color Coding

| Color | Meaning |
|-------|---------|
| 🟢 Green | OK - Component passes |
| 🟡 Yellow | Marginal (80-100% of limit) or User Review Required |
| 🔴 Light Red | NOK - Exceeds rating |
| 🔴 Bright Red | FAIL - Library error or critical issue |

### Verdicts Explained

- **OK** - Component passes all checks
- **OK (Switching)** - Safe even on switching path
- **Marginal** - 80-100% of derated rating (caution zone)
- **NOK** - Exceeds derated rating (failure)
- **User Review Required** - NOK on switching path, needs manual analysis
- **Unknown (Missing Data)** - Rating not found in component name

---

## Troubleshooting

### "Cannot find netlist file"
- Ensure file has `.NET` extension
- Check file path for special characters
- Make sure file is not open in another program

### "No voltage rails detected"
- This is normal for some designs
- You can skip voltage confirmation
- Analysis will proceed with 0V assumption

### Reports not generating
- Check disk space
- Ensure you have write permission in the folder
- Close Excel if report file is already open

### Executable won't start
- Check Windows Defender hasn't quarantined it
- Right-click → Properties → Unblock (if option available)
- Antivirus may need exception added

### First run is slow
- Normal behavior (10-15 seconds)
- Subsequent runs are faster
- Windows Defender may scan on first run

---

## Tips & Best Practices

### Before Analysis
✅ Ensure netlist is from latest PCB version  
✅ Close the netlist file in any text editors  
✅ Have component datasheets ready for manual review  

### During Analysis
✅ Carefully review auto-detected voltage values  
✅ Edit voltages if auto-detection is wrong  
✅ Confirm only the voltages you're certain of  

### After Analysis
✅ Review all RED components first  
✅ Check YELLOW components for actual usage conditions  
✅ Verify library errors are corrected in Altium  
✅ Document any "User Review Required" decisions  

---

## What Gets Checked?

### Capacitors
- Rated voltage vs. applied voltage
- 80% derating factor (MLCC default)
- Switching path worst-case analysis

### Resistors
- Power dissipation (V²/R)
- Power rating inferred from footprint
- 80% derating factor

### Inductors
- Current rating (framework ready)
- 70% derating factor
- Note: Current analysis requires manual input in V1.0

### All Components
- Standard library usage (triomobil.DbLib)
- Footprint size matches part name size

---

## Derating Standards

**Marginal Threshold:** 80%

**Derating Factors:**
- Capacitors: 80% (0.8× rated voltage)
- Resistors: 80% (0.8× rated power)
- Inductors: 70% (0.7× rated current)

**Reference:** Industry standard practice, configurable in `data/component_database.json`

---

## File Locations

### Input
- Netlist: Anywhere you choose (dialog prompt)

### Output (same folder as netlist)
- Excel: `RatingVerification_V2_WorstCase.xlsx`
- HTML: `Executive_Summary_V2.html`

---

## Support & Feedback

### For Help
- Read this README
- Check BUILD_GUIDE.md (in source)
- Review SOFTWARE_SPECIFICATION.md (in source)

### Report Issues
- Note the exact error message
- Describe steps to reproduce
- Include netlist file (if not confidential)

---

## Version Information

**Current Release:** V1.0 (February 14, 2026)

**What's New:**
- First stable release
- Multi-tab Excel reports
- Switching path analysis
- Library consistency auditing
- Interactive GUI dashboard

**Coming in V2.0:**
- Save/load voltage configurations
- PDF report generation
- Design revision comparison
- Interactive voltage map
- GUI tooltips
- And more...

---

## License & Credits

**Project:** Auto_Altium Rating Verification Tool  
**Target Platform:** Altium Designer 24.01  
**Repository:** github.com:FikretUzgan/Schematic-Checker.git

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│    AUTO_ALTIUM RATING VERIFIER          │
├─────────────────────────────────────────┤
│ 1. Export netlist from Altium (.NET)   │
│ 2. Run AutoAltium_RatingVerifier.exe   │
│ 3. Select netlist file                 │
│ 4. Confirm voltage rails               │
│ 5. Review results dashboard            │
│ 6. Export to Excel/HTML                │
├─────────────────────────────────────────┤
│ COLOR CODE:                             │
│   🟢 OK - Passed                        │
│   🟡 Marginal - Caution                 │
│   🔴 NOK/FAIL - Error                   │
├─────────────────────────────────────────┤
│ OUTPUT FILES:                           │
│   • RatingVerification_V2_WorstCase.xlsx│
│   • Executive_Summary_V2.html           │
└─────────────────────────────────────────┘
```

---

**Ready to verify your design? Double-click the executable to get started!**
