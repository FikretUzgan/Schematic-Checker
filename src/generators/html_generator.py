import os
from datetime import datetime

class HTMLExecutiveGenerator:
    """Generates a professional HTML Executive Summary Report."""
    
    def __init__(self, output_path: str):
        self.output_path = output_path

    def generate(self, results: list):
        """Creates the HTML report with summary stats and critical findings."""
        total = len(results)
        # Fix: Catch variants like "NOK (Switching)" using startswith
        noks = [r for r in results if str(r.get('Verdict', '')).startswith('NOK')]
        marginals = [r for r in results if str(r.get('Verdict', '')).startswith('Marginal')]
        oks = [r for r in results if str(r.get('Verdict', '')).startswith('OK')]
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Summary - Component Rating Verification</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 40px; line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }}
        h1 {{ color: #3498db; border-bottom: 2px solid #333; padding-bottom: 10px; margin-top: 0; }}
        h2 {{ color: #f39c12; margin-top: 30px; font-size: 1.4em; }}
        .meta {{ font-size: 0.9em; color: #888; margin-bottom: 30px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: #2a2a2a; padding: 20px; border-radius: 6px; text-align: center; border-left: 4px solid #444; }}
        .stat-card.nok {{ border-left-color: #e74c3c; }}
        .stat-card.marginal {{ border-left-color: #f1c40f; }}
        .stat-card.ok {{ border-left-color: #2ecc71; }}
        .stat-value {{ font-size: 2em; font-weight: bold; display: block; }}
        .stat-label {{ color: #aaa; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.95em; }}
        th {{ background-color: #333; color: white; text-align: left; padding: 12px; }}
        td {{ padding: 12px; border-bottom: 1px solid #333; }}
        .v-nok {{ color: #ff9999; font-weight: bold; }}
        .v-marginal {{ color: #ffff99; font-weight: bold; }}
        .audit-fail {{ color: #ff4444; font-weight: bold; text-decoration: underline; }}
        .audit-warn {{ color: #ffbb33; font-style: italic; }}
        .banner {{ background: #2c3e50; padding: 15px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #34495e; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Executive Verification Report</h1>
        <div class="meta">Report Generated: {timestamp}</div>
        
        <div class="banner">
            This report summarizes the electrical rating verification for passive components (Resistors & Capacitors). 
            Analysis used an <strong>80% derating threshold</strong> for categorization.
        </div>

        <div class="summary-grid">
            <div class="stat-card">
                <span class="stat-value">{total}</span>
                <span class="stat-label">Total Components</span>
            </div>
            <div class="stat-card nok">
                <span class="stat-value" style="color: #e74c3c;">{len(noks)}</span>
                <span class="stat-label">NOK (Exceeded)</span>
            </div>
            <div class="stat-card marginal">
                <span class="stat-value" style="color: #f1c40f;">{len(marginals)}</span>
                <span class="stat-label">Marginal (Risk)</span>
            </div>
            <div class="stat-card ok">
                <span class="stat-value" style="color: #2ecc71;">{len(oks)}</span>
                <span class="stat-label">OK (Safe)</span>
            </div>
        </div>

        <h2>Critical Findings</h2>
        {"<p>No critical issues found.</p>" if not noks and not marginals else ""}
        {self._generate_findings_table(noks + marginals)}

        <div style="margin-top: 50px; font-size: 0.8em; color: #555; text-align: center;">
            Auto_Altium Passive Verifier v1.0 | Standalone Executive Report
        </div>
    </div>
</body>
</html>
"""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML Executive Report generated: {os.path.abspath(self.output_path)}")

    def _generate_findings_table(self, findings: list) -> str:
        if not findings: return ""
        
        table_html = """
        <table>
            <thead>
                <tr>
                    <th>Designator</th>
                    <th>Type</th>
                    <th>Applied</th>
                    <th>Rating</th>
                    <th>Verdict</th>
                    <th>Reason</th>
                    <th>Library Audit</th>
                </tr>
            </thead>
            <tbody>
        """
        for item in findings:
            verdict_str = str(item.get('Verdict', ''))
            v_class = "v-nok" if verdict_str.startswith('NOK') else "v-marginal"
            table_html += f"""
                <tr>
                    <td>{item.get('Designator', '-')}</td>
                    <td>{item.get('Type', '-')}</td>
                    <td>{item.get('Applied', '-')}</td>
                    <td>{item.get('Rating', '-')}</td>
                    <td class="{v_class}">{verdict_str}</td>
                    <td>{item.get('Reason', '-')}</td>
                    <td class="{self._get_audit_class(item)}">{item.get('AuditReason', 'Consistent')}</td>
                </tr>
            """
        table_html += "</tbody></table>"
        return table_html

    def _get_audit_class(self, item: dict) -> str:
        verdict = item.get('AuditVerdict', 'OK')
        if verdict == 'FAIL': return "audit-fail"
        if verdict == 'WARNING': return "audit-warn"
        return ""
