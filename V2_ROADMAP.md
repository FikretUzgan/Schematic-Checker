# V2.0 Development Roadmap

## Overview
This document tracks the implementation progress of approved V2.0 enhancements.

**Target Release:** Q2 2026 (tentative)  
**Status:** Planning phase - implementation starting after V1.0 release

---

## Feature Implementation Checklist

### 🟢 HIGH PRIORITY (Target: Week 1-2)

#### ✅ Feature #1: Save/Load Voltage Configuration
**Status:** ⬜ Not Started  
**Estimated Effort:** 4-6 hours  
**Dependencies:** None  

**Implementation Tasks:**
- [ ] Create voltage config file format (JSON)
- [ ] Implement save function after voltage confirmation
- [ ] Implement load function at startup
- [ ] Add "Use saved voltages?" dialog
- [ ] Add "Clear cached voltages" button in GUI
- [ ] Handle missing/corrupted config files
- [ ] Test with multiple projects

**Files to Modify:**
- `src/analyzers/net_voltage_analyzer.py` - Add save/load methods
- `src/gui/rating_gui.py` - Add load dialog before voltage confirmation
- `run_rating_verification_v2.py` - Integration logic

**Acceptance Criteria:**
- Voltages persist between runs for same netlist
- User can override cached voltages
- Invalid cache files don't crash the application

---

#### ✅ Feature #8: Comparison Mode (Design Revisions)
**Status:** ⬜ Not Started  
**Estimated Effort:** 8-10 hours  
**Dependencies:** None  

**Implementation Tasks:**
- [ ] Create comparison analyzer module
- [ ] Parse two netlists and generate diff
- [ ] Identify added/removed/changed components
- [ ] Compare verdicts (OK→NOK, etc.)
- [ ] Create comparison report (Excel tab or separate file)
- [ ] Add GUI for file selection (RevA vs RevB)
- [ ] Test with real revision pairs

**New Files to Create:**
- `src/analyzers/revision_comparator.py`

**Files to Modify:**
- `run_rating_verification_v2.py` - Add comparison mode
- `src/generators/excel_generator.py` - Add comparison report tab

**Acceptance Criteria:**
- Correctly identifies all component changes
- Shows verdict changes with color coding
- Summary shows delta in failure counts

---

#### ✅ Feature #6: PDF Report Generation
**Status:** ⬜ Not Started  
**Estimated Effort:** 6-8 hours  
**Dependencies:** New library (`weasyprint` or `reportlab`)  

**Implementation Tasks:**
- [ ] Research library choice (weasyprint vs reportlab)
- [ ] Install and test chosen library
- [ ] Create PDF template design
- [ ] Implement PDF generator class
- [ ] Add company logo placeholder
- [ ] Add "Export to PDF" button in GUI
- [ ] Test PDF generation with various designs
- [ ] Handle large datasets (1000+ components)

**New Files to Create:**
- `src/generators/pdf_generator.py`
- `templates/pdf_template.html` (if using weasyprint)

**Files to Modify:**
- `run_rating_verification_v2.py` - Add PDF output option
- `src/gui/rating_gui.py` - Add export button

**Dependencies to Add:**
```bash
pip install weasyprint
# OR
pip install reportlab
```

**Acceptance Criteria:**
- Professional-looking PDF report
- All data from Excel included
- File size < 5MB for typical projects
- Renders correctly in all PDF readers

---

#### ✅ Feature #20: Recent Files List
**Status:** ⬜ Not Started  
**Estimated Effort:** 2-3 hours  
**Dependencies:** None  

**Implementation Tasks:**
- [ ] Create recent files config (JSON)
- [ ] Track last 5 analyzed netlist paths
- [ ] Add recent files dropdown in file selection dialog
- [ ] Update list after each successful analysis
- [ ] Handle deleted/moved files gracefully
- [ ] Add "Clear recent files" option

**Files to Modify:**
- `src/gui/rating_gui.py` - NetlistSelectionPage enhancement
- Create: `data/recent_files.json`

**Acceptance Criteria:**
- Shows last 5 successfully analyzed netlists
- Clicking entry loads that file
- List persists between application runs
- Gracefully handles missing files

---

### 🟡 MEDIUM PRIORITY (Target: Week 3-4)

#### ✅ Feature #7: Interactive Voltage Map Visualization
**Status:** ⬜ Not Started  
**Estimated Effort:** 12-16 hours  
**Dependencies:** None (pure HTML/JavaScript)  

**Implementation Tasks:**
- [ ] Choose visualization library (vis.js or D3.js)
- [ ] Generate network graph data structure
- [ ] Create HTML template with embedded JavaScript
- [ ] Map components as nodes (colored by verdict)
- [ ] Map nets as edges (labeled with voltage)
- [ ] Add interactive features (zoom, pan, hover)
- [ ] Add filter controls (show only failures, etc.)
- [ ] Test with complex designs (500+ components)

**New Files to Create:**
- `src/generators/network_visualizer.py`
- `templates/network_graph.html`

**Files to Modify:**
- `run_rating_verification_v2.py` - Add visualization output
- `src/gui/rating_gui.py` - Add "View Network Graph" button

**Acceptance Criteria:**
- Interactive graph loads in web browser
- Clear visualization of voltage distribution
- Performance acceptable for 500+ components
- Mobile-friendly (responsive design)

---

#### ✅ Feature #18: GUI Tooltips
**Status:** ⬜ Not Started  
**Estimated Effort:** 3-4 hours  
**Dependencies:** None (tkinter built-in)  

**Implementation Tasks:**
- [ ] Create tooltip class (or use tkinter.ttk.Tooltip if available)
- [ ] Add tooltips to all GUI elements
- [ ] Write clear, concise explanations
- [ ] Test tooltip positioning (doesn't go off-screen)
- [ ] Ensure tooltips don't interfere with workflow

**Tooltip Definitions Needed:**
- "Derated" → "Rating after applying safety derating factor"
- "Switching Path" → "May see transient overstress from switching"
- "AuditVerdict" → "Combined library + derating check result"
- "Marginal" → "Component in caution zone (80-100% of limit)"
- etc. (full list in specification)

**Files to Modify:**
- `src/gui/rating_gui.py` - Add tooltip support
- Create: `data/tooltip_text.json` (optional - externalize text)

**Acceptance Criteria:**
- Tooltips appear on hover (500ms delay)
- Clear, jargon-free explanations
- Tooltips disappear when mouse moves away

---

#### ✅ Feature #23: Custom Report Templates
**Status:** ⬜ Not Started  
**Estimated Effort:** 6-8 hours  
**Dependencies:** `jinja2` library  

**Implementation Tasks:**
- [ ] Install jinja2
- [ ] Convert existing HTML generator to use templates
- [ ] Create default template
- [ ] Add template configuration in database JSON
- [ ] Support custom logo images
- [ ] Support custom CSS styling
- [ ] Document template format for users
- [ ] Provide example custom template

**New Files to Create:**
- `templates/html_report_default.html` (Jinja2 template)
- `templates/html_report_custom_example.html`
- `docs/TEMPLATE_GUIDE.md`

**Files to Modify:**
- `src/generators/html_generator.py` - Convert to Jinja2
- `data/component_database.json` - Add template config

**Dependencies to Add:**
```bash
pip install jinja2
```

**Acceptance Criteria:**
- Users can provide custom HTML templates
- Templates have access to all analysis data
- Sample custom template provided
- Documentation explains template variables

---

### 🔵 LOW PRIORITY (Target: Week 5-6)

#### ✅ Feature #9: Progress Bar for Large Designs
**Status:** ⬜ Not Started  
**Estimated Effort:** 2 hours  
**Dependencies:** `tqdm` library  

**Implementation Tasks:**
- [ ] Install tqdm
- [ ] Add progress bar to main analysis loop
- [ ] Test with large designs (1000+ components)
- [ ] Ensure progress bar doesn't interfere with GUI

**Files to Modify:**
- `run_rating_verification_v2.py` - Add tqdm wrapper

**Dependencies to Add:**
```bash
pip install tqdm
```

**Acceptance Criteria:**
- Shows analysis progress for designs > 100 components
- Updates smoothly without flickering
- Doesn't break GUI workflow

---

#### ✅ Feature #11: Statistics Dashboard Banner in Excel
**Status:** ⬜ Not Started  
**Estimated Effort:** 2-3 hours  
**Dependencies:** None  

**Implementation Tasks:**
- [ ] Design banner format
- [ ] Insert banner at top of Verification Details sheet
- [ ] Use Excel merged cells for formatting
- [ ] Add color coding (red/yellow/green badges)
- [ ] Test with various failure counts

**Files to Modify:**
- `src/generators/excel_generator.py` - Add banner generation

**Acceptance Criteria:**
- Banner appears at top of Details sheet
- Shows counts for FAILED, WARNING, PASSED
- Professional appearance with color coding

---

## Additional Tasks

### Documentation Updates
- [ ] Update SOFTWARE_SPECIFICATION.md with V2.0 implementation details
- [ ] Update RELEASE_NOTES.md with V2.0 changes
- [ ] Create user guide with examples for new features
- [ ] Record demo video showing new features

### Testing
- [ ] Unit tests for all new modules
- [ ] Integration tests for new workflows
- [ ] Performance testing with large designs
- [ ] User acceptance testing with real engineers

### Deployment
- [ ] Update requirements.txt with new dependencies
- [ ] Test installation on clean system
- [ ] Update README with V2.0 features
- [ ] Create migration guide (V1.0 → V2.0)

---

## Under Review (Pending Decision)

### Feature #5: Component Exemption List
**Status:** 🟡 Pending team discussion  
**Concerns:** May mask real issues if misused  

**If Approved, Implementation Tasks:**
- [ ] Create exemptions.json format
- [ ] Add "Exempt this component" option in GUI (right-click)
- [ ] Store exemption reason
- [ ] Mark exempted components differently in reports
- [ ] Add "Review exemptions" dialog
- [ ] Document exemption workflow

**Decision Required By:** Week 2 of V2.0 development

---

## Timeline Estimate

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | High Priority #1, #20 | Save/Load Voltages, Recent Files |
| 2 | High Priority #8, #6 | Comparison Mode, PDF Reports |
| 3 | Medium Priority #7 | Network Visualization |
| 4 | Medium Priority #18, #23 | Tooltips, Templates |
| 5 | Low Priority #9, #11 | Progress Bar, Excel Banner |
| 6 | Testing & Documentation | Final QA, Release prep |

**Total Estimated Effort:** 47-61 hours (1-1.5 months of part-time development)

---

## Future Phases (Post-V2.0)

### V3.0 Candidates
- CLI Mode (command-line interface)
- Real current analysis (PCB trace parsing)
- Component database API integration (Octopart)
- Email notifications

### V4.0 Candidates
- Thermal analysis
- Altium DelphiScript integration
- Multi-board batch analysis
- AI-powered component recommendations

---

## Progress Tracking

**Last Updated:** February 14, 2026  
**Overall Progress:** 0% (Planning phase)  
**Target V2.0 Release:** Q2 2026

**Next Steps:**
1. Finalize team discussion on Feature #5 (exemptions)
2. Begin implementation of Feature #1 (Save/Load Voltages)
3. Set up development branch for V2.0

---

**Note:** This roadmap is subject to change based on user feedback and technical discoveries during implementation.
