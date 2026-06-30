"""Build presentation-ready HTML and PDF incident reports."""

from __future__ import annotations

import webbrowser
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_HTML = PROJECT_ROOT / "report.html"
REPORT_PDF = PROJECT_ROOT / "report.pdf"


def _html_report() -> str:
    generated = datetime.now(timezone.utc).strftime("%B %d, %Y · %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Incident Report — INC-2026-0847 | Northwind Financial</title>
  <style>
    @page {{
      size: letter;
      margin: 0.65in 0.75in;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Segoe UI", Calibri, Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.55;
      color: #1a2332;
      background: #e8ecf1;
    }}
    .document {{
      max-width: 8.5in;
      margin: 24px auto;
      background: #fff;
      box-shadow: 0 4px 24px rgba(0,0,0,.12);
    }}
    .cover {{
      background: linear-gradient(135deg, #0f2744 0%, #1a3a5c 55%, #0d2137 100%);
      color: #fff;
      padding: 48px 56px 40px;
      page-break-after: always;
    }}
    .cover-label {{
      font-size: 9pt;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      opacity: 0.75;
      margin-bottom: 12px;
    }}
    .cover h1 {{
      font-size: 26pt;
      font-weight: 600;
      line-height: 1.2;
      margin-bottom: 8px;
    }}
    .cover-sub {{
      font-size: 13pt;
      font-weight: 300;
      opacity: 0.9;
      margin-bottom: 32px;
    }}
    .badge-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 36px; }}
    .badge {{
      display: inline-block;
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 9pt;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}
    .badge-p1 {{ background: #c0392b; color: #fff; }}
    .badge-status {{ background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.35); }}
    .badge-ai {{ background: #2e86ab; color: #fff; }}
    .cover-meta {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px 32px;
      font-size: 10pt;
      border-top: 1px solid rgba(255,255,255,.2);
      padding-top: 24px;
    }}
    .cover-meta dt {{ opacity: 0.65; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2px; }}
    .cover-meta dd {{ font-weight: 500; }}
    .content {{ padding: 40px 56px 48px; }}
    .page-break {{ page-break-before: always; }}
    h2 {{
      font-size: 14pt;
      color: #0f2744;
      border-bottom: 2px solid #2e86ab;
      padding-bottom: 6px;
      margin: 28px 0 16px;
    }}
    h2:first-child {{ margin-top: 0; }}
    h3 {{
      font-size: 11pt;
      color: #1a3a5c;
      margin: 20px 0 10px;
    }}
    p {{ margin-bottom: 10px; }}
    .lead {{
      font-size: 11pt;
      color: #3d4f63;
      background: #f0f6fa;
      border-left: 4px solid #2e86ab;
      padding: 14px 18px;
      margin-bottom: 24px;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin: 20px 0 28px;
    }}
    .kpi {{
      background: #f7f9fb;
      border: 1px solid #dde4ec;
      border-radius: 6px;
      padding: 14px 12px;
      text-align: center;
    }}
    .kpi-value {{
      font-size: 18pt;
      font-weight: 700;
      color: #0f2744;
      line-height: 1.1;
    }}
    .kpi-value.danger {{ color: #c0392b; }}
    .kpi-label {{
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #6b7c93;
      margin-top: 4px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 20px;
      font-size: 9.5pt;
    }}
    th {{
      background: #0f2744;
      color: #fff;
      text-align: left;
      padding: 8px 10px;
      font-weight: 600;
      font-size: 8.5pt;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    td {{
      padding: 8px 10px;
      border-bottom: 1px solid #e4e9ef;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: #f9fafb; }}
    .takeaways {{
      list-style: none;
      margin: 12px 0;
    }}
    .takeaways li {{
      padding: 12px 14px 12px 16px;
      margin-bottom: 10px;
      background: #fff;
      border: 1px solid #dde4ec;
      border-radius: 6px;
      border-left: 4px solid #2e86ab;
    }}
    .takeaways strong {{ color: #0f2744; }}
    .chain {{
      background: #1e2d3d;
      color: #e8f0f8;
      font-family: Consolas, "Courier New", monospace;
      font-size: 8.5pt;
      line-height: 1.7;
      padding: 16px 18px;
      border-radius: 6px;
      margin: 12px 0 16px;
      white-space: pre-wrap;
    }}
    .logs {{
      background: #f4f6f8;
      border: 1px solid #dde4ec;
      font-family: Consolas, monospace;
      font-size: 8pt;
      padding: 12px 14px;
      border-radius: 4px;
      line-height: 1.65;
      color: #2c3e50;
    }}
    .agent-flow {{
      display: grid;
      grid-template-columns: 48px 1fr;
      gap: 4px 14px;
      margin: 16px 0;
    }}
    .agent-step {{
      width: 32px;
      height: 32px;
      background: #2e86ab;
      color: #fff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 10pt;
    }}
    .agent-name {{ font-weight: 600; color: #0f2744; }}
    .agent-desc {{ font-size: 9.5pt; color: #5a6b7d; grid-column: 2; margin-bottom: 10px; }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .callout {{
      background: #fff8f0;
      border: 1px solid #f0d9b5;
      border-radius: 6px;
      padding: 14px 16px;
      margin: 16px 0;
    }}
    .callout strong {{ color: #b45309; }}
    .footer {{
      margin-top: 32px;
      padding-top: 16px;
      border-top: 1px solid #dde4ec;
      font-size: 8pt;
      color: #8a96a3;
      text-align: center;
    }}
    .confidential {{
      text-align: center;
      font-size: 8pt;
      color: rgba(255,255,255,.5);
      margin-top: 32px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}
    @media print {{
      body {{ background: #fff; }}
      .document {{ box-shadow: none; margin: 0; max-width: none; }}
    }}
  </style>
</head>
<body>
  <div class="document">

    <header class="cover">
      <div class="cover-label">Enterprise Incident Intelligence</div>
      <h1>Incident Investigation Report</h1>
      <p class="cover-sub">Customer Portal Outage — Database Connection Pool Exhaustion</p>
      <div class="badge-row">
        <span class="badge badge-p1">P1 Critical</span>
        <span class="badge badge-status">Status: Mitigating</span>
        <span class="badge badge-ai">AI-Generated Analysis</span>
      </div>
      <dl class="cover-meta">
        <div><dt>Incident ID</dt><dd>INC-2026-0847</dd></div>
        <div><dt>Organization</dt><dd>Northwind Financial</dd></div>
        <div><dt>Report Date</dt><dd>{generated}</dd></div>
        <div><dt>Bridge ID</dt><dd>BR-2026-0847</dd></div>
        <div><dt>Classification</dt><dd>Infrastructure / Database</dd></div>
        <div><dt>Analysis Platform</dt><dd>CrewAI · 6-Agent Pipeline</dd></div>
      </dl>
      <p class="confidential">Confidential — Internal Use Only</p>
    </header>

    <main class="content">

      <h2>Executive Summary</h2>
      <p class="lead">
        On June 29, 2026, Northwind Financial's customer portal experienced a <strong>P1 outage</strong>
        affecting approximately <strong>2.1 million accounts</strong>. Six AI agents autonomously triaged,
        analyzed logs, identified root cause, and produced this remediation plan — compressing hours of
        incident response into a single actionable briefing.
      </p>

      <div class="kpi-grid">
        <div class="kpi"><div class="kpi-value danger">2.1M</div><div class="kpi-label">Customers Affected</div></div>
        <div class="kpi"><div class="kpi-value danger">41%</div><div class="kpi-label">Payment Success Rate</div></div>
        <div class="kpi"><div class="kpi-value">$180K</div><div class="kpi-label">Revenue at Risk / Hour</div></div>
        <div class="kpi"><div class="kpi-value">68%→41%</div><div class="kpi-label">Error Rate (Recovering)</div></div>
      </div>

      <h3>Key Takeaways for Leadership</h3>
      <ol class="takeaways">
        <li><strong>Preventable infrastructure failure, not a cyberattack.</strong> A single inefficient database query consumed the entire connection pool, cascading into customer-facing outages across web and mobile.</li>
        <li><strong>Financial and regulatory exposure is immediate.</strong> Payment SLA is in active breach; degradation past 30 minutes triggers OCC notification for core banking services.</li>
        <li><strong>Fix is known and partially applied.</strong> Immediate mitigations are working. Strategic investments in connection management and query governance will prevent recurrence.</li>
      </ol>

      <div class="page-break"></div>

      <h2>AI Agent Pipeline</h2>
      <p>Each agent performed a specialized function in the incident response workflow:</p>
      <div class="agent-flow">
        <div class="agent-step">1</div><div class="agent-name">Senior IT Incident Triage Specialist</div>
        <div></div><div class="agent-desc">Classified P1 severity, infrastructure category, blast radius, and business impact (confidence: 94%)</div>
        <div class="agent-step">2</div><div class="agent-name">Log Analysis &amp; Anomaly Detection Engineer</div>
        <div></div><div class="agent-desc">Parsed logs and metrics; reconstructed chronological event timeline (confidence: 91%)</div>
        <div class="agent-step">3</div><div class="agent-name">Knowledge Base &amp; Runbook Retrieval Specialist</div>
        <div></div><div class="agent-desc">Matched historical incidents and database pool exhaustion runbooks (confidence: 85%)</div>
        <div class="agent-step">4</div><div class="agent-name">Principal Root Cause Analysis Engineer</div>
        <div></div><div class="agent-desc">Built causal chain and ranked hypotheses with supporting evidence (confidence: 88%)</div>
        <div class="agent-step">5</div><div class="agent-name">Remediation &amp; Resilience Architect</div>
        <div></div><div class="agent-desc">Produced immediate, 24-hour, and long-term action plans with owners (confidence: 90%)</div>
        <div class="agent-step">6</div><div class="agent-name">Communications &amp; Reporting Director</div>
        <div></div><div class="agent-desc">Synthesized all findings into this executive-ready report</div>
      </div>

      <h2>Technical Incident Report</h2>

      <h3>Incident Overview</h3>
      <table>
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td>Incident ID</td><td>INC-2026-0847</td></tr>
        <tr><td>Severity</td><td><strong>P1 — Critical</strong></td></tr>
        <tr><td>Category</td><td>Infrastructure / Database</td></tr>
        <tr><td>Status</td><td>Mitigated — degradation reducing</td></tr>
        <tr><td>Confidence</td><td>Triage 94% · Logs 91% · RCA 88%</td></tr>
      </table>

      <h3>Affected Systems</h3>
      <table>
        <tr><th>System</th><th>Role</th></tr>
        <tr><td>customer-portal-api</td><td>Kubernetes, us-east-1 (24 pods)</td></tr>
        <tr><td>auth-service / account-summary-service</td><td>Application tier — connection pool consumers</td></tr>
        <tr><td>postgres-primary-prod</td><td>RDS PostgreSQL 15 — connection exhaustion source</td></tr>
        <tr><td>pgbouncer-prod</td><td>Connection pooler (398/400 at peak)</td></tr>
        <tr><td>api-gateway-prod</td><td>Kong — 503 responses to clients</td></tr>
      </table>

      <h3>Event Timeline</h3>
      <table>
        <tr><th>Time (UTC)</th><th>Event</th></tr>
        <tr><td>08:02:11</td><td>auth-service — HikariPool connection timeout (30s)</td></tr>
        <tr><td>08:02:14</td><td>PostgreSQL — connection slots reserved for SUPERUSER only</td></tr>
        <tr><td>08:02:19</td><td>PgBouncer — 398/400 connections active</td></tr>
        <tr><td>08:03:02</td><td>API Gateway — upstream 503s on /api/v2/auth/login</td></tr>
        <tr><td>08:08:15</td><td>DBA — active_connections=412 exceeds max=400</td></tr>
        <tr><td>08:14:05</td><td>P1 declared — incident bridge BR-2026-0847 opened</td></tr>
        <tr><td>08:16:18</td><td>DBA terminated PID 1849201 (47-minute query)</td></tr>
        <tr><td>08:22:10</td><td>HTTP 503 rate improved: 68% → 41%</td></tr>
      </table>

      <h3>Root Cause — Causal Chain</h3>
      <div class="chain">Long-running unoptimized SELECT (LIMIT 500, multi-table join)
  → Held PostgreSQL connections for 47+ minutes
    → Connection pool exhausted (412 &gt; 400 max)
      → PgBouncer rejected new connections
        → auth-service / account-summary timeouts
          → API Gateway 503 responses
            → Customer portal login failures (68% error rate)</div>

      <div class="callout">
        <strong>Primary root cause:</strong> Database connection pool exhaustion triggered by a
        long-running read query combined with insufficient connection headroom under peak load.
      </div>

      <h3>Key Log Evidence</h3>
      <div class="logs">ERROR auth-service | HikariPool-1 - Connection is not available, request timed out after 30000ms
ERROR postgres-primary | FATAL: remaining connection slots are reserved for SUPERUSER
WARN  pgbouncer-prod | pool 'northwind_app' - too many connections (398/400 active)
INFO  on-call-dba | terminated PID 1849201 (long-running SELECT, runtime 47m)</div>

      <div class="page-break"></div>

      <h2>Remediation Plan</h2>
      <table>
        <tr><th>Horizon</th><th>Actions</th></tr>
        <tr><td><strong>Immediate (&lt; 1 hr)</strong></td><td>Kill long-running queries; temporarily raise connection limits; enable API Gateway rate limiting</td></tr>
        <tr><td><strong>Short-term (&lt; 24 hr)</strong></td><td>Optimize offending query; add statement timeout; review PgBouncer pool sizing</td></tr>
        <tr><td><strong>Long-term</strong></td><td>Deploy connection auto-scaling; APM/DBPM monitoring; circuit breakers on external APIs</td></tr>
      </table>

      <h2>Lessons Learned</h2>
      <div class="two-col">
        <div>
          <h3>What Failed</h3>
          <ul>
            <li>Connection limits not sized for surges + inefficient queries</li>
            <li>Pool utilization alerts too permissive</li>
            <li>47-minute production query undetected</li>
          </ul>
        </div>
        <div>
          <h3>What Worked</h3>
          <ul>
            <li>Prompt P1 declaration and team mobilization</li>
            <li>Effective DBA / SRE collaboration on bridge</li>
            <li>Rapid application of known workarounds</li>
          </ul>
        </div>
      </div>

      <h3>Recommended Investments</h3>
      <table>
        <tr><th>Investment</th><th>Expected ROI</th></tr>
        <tr><td>Dynamic connection management &amp; auto-scaling</td><td>High — prevents P1 recurrence</td></tr>
        <tr><td>APM / database performance monitoring</td><td>High — proactive query detection</td></tr>
        <tr><td>API Gateway rate-limiting &amp; circuit breaking</td><td>High — buffers traffic spikes</td></tr>
      </table>

      <h2>Business Impact</h2>
      <table>
        <tr><th>Metric</th><th>Impact</th></tr>
        <tr><td>Customers affected</td><td>~2.1 million active accounts</td></tr>
        <tr><td>Revenue at risk</td><td>~$180K/hour in payment processing fees</td></tr>
        <tr><td>Payment success rate</td><td>99.2% → 41% (active SLA breach)</td></tr>
        <tr><td>Support queue</td><td>+340% vs. baseline (~1,200 callers)</td></tr>
        <tr><td>Regulatory</td><td>OCC notification if outage exceeds 30 minutes</td></tr>
      </table>

      <div class="footer">
        Generated by Enterprise Incident Intelligence &amp; Resolution System (CrewAI)<br />
        Northwind Financial · Demo Scenario · {generated}
      </div>
    </main>
  </div>
</body>
</html>"""


def build_reports(*, open_browser: bool = False) -> tuple[Path, Path | None]:
    """Write report.html and attempt report.pdf. Returns (html_path, pdf_path or None)."""
    html = _html_report()
    REPORT_HTML.write_text(html, encoding="utf-8")

    pdf_path: Path | None = None
    try:
        from xhtml2pdf import pisa

        with open(REPORT_PDF, "wb") as pdf_file:
            status = pisa.CreatePDF(html, dest=pdf_file, encoding="utf-8")
        if not status.err:
            pdf_path = REPORT_PDF
    except Exception:
        pdf_path = None

    if open_browser:
        webbrowser.open(REPORT_HTML.resolve().as_uri())

    return REPORT_HTML, pdf_path


if __name__ == "__main__":
    html_path, pdf_path = build_reports(open_browser=True)
    print(f"HTML: {html_path}")
    if pdf_path:
        print(f"PDF:  {pdf_path}")
    else:
        print("PDF:  not generated (open report.html and use Print → Save as PDF)")
