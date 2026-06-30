#!/usr/bin/env python
import sys
from datetime import datetime, timezone
from pathlib import Path

from enterprise_incident_intelligence_resolution_system.crew import (
    EnterpriseIncidentIntelligenceResolutionSystemCrew,
)
from enterprise_incident_intelligence_resolution_system.demo_inputs import DEMO_INPUTS

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = PROJECT_ROOT / "report.md"


def _report_header() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""# Enterprise Incident Intelligence Report

| | |
|---|---|
| **Incident** | INC-2026-0847 — Customer Portal outage (database connection exhaustion) |
| **Organization** | Northwind Financial (demo scenario) |
| **Generated** | {now} |
| **System** | CrewAI Multi-Agent Incident Resolution Platform |
| **Agents deployed** | 6 specialists — Triage, Log Analysis, Knowledge Retrieval, RCA, Remediation, Executive Reporting |

> **Purpose:** This report was produced autonomously by a coordinated team of AI agents that
> triaged the incident, analyzed logs, retrieved runbooks, determined root cause, and
> recommended remediation — mirroring a real enterprise incident response workflow.

---

"""


def run():
    """Run the crew and save an executive-ready report."""
    result = EnterpriseIncidentIntelligenceResolutionSystemCrew().crew().kickoff(
        inputs=DEMO_INPUTS
    )

    body = result.raw if hasattr(result, "raw") and result.raw else str(result)
    REPORT_PATH.write_text(_report_header() + body.strip() + "\n", encoding="utf-8")

    from enterprise_incident_intelligence_resolution_system.report_builder import build_reports

    html_path, pdf_path = build_reports(open_browser=False)

    print(f"\n{'=' * 60}")
    print("  INCIDENT ANALYSIS COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Markdown:  {REPORT_PATH}")
    print(f"  HTML:      {html_path}")
    if pdf_path:
        print(f"  PDF:       {pdf_path}")
    else:
        print(f"  PDF:       Open report.html → Print → Save as PDF")
    print(f"{'=' * 60}\n")

    return result


def train():
    """Train the crew for a given number of iterations."""
    try:
        EnterpriseIncidentIntelligenceResolutionSystemCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=DEMO_INPUTS,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}") from e


def replay():
    """Replay the crew execution from a specific task."""
    try:
        EnterpriseIncidentIntelligenceResolutionSystemCrew().crew().replay(
            task_id=sys.argv[1]
        )
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}") from e


def test():
    """Test the crew execution and returns the results."""
    try:
        EnterpriseIncidentIntelligenceResolutionSystemCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=DEMO_INPUTS,
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}") from e


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
