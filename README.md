# Enterprise Incident Intelligence & Resolution System

Multi-agent [CrewAI](https://crewai.com) pipeline that autonomously triages IT incidents, analyzes logs, retrieves runbooks, performs root-cause analysis, and generates executive-ready PDF reports.

**Demo scenario:** [INC-2026-0847](report.pdf) — Northwind Financial customer portal P1 outage (database connection pool exhaustion, ~2.1M customers affected).

## What it does

Six AI agents run in a coordinated incident-response workflow:

| Step | Agent | Output |
|------|-------|--------|
| 1 | Senior IT Incident Triage Specialist | Severity, category, blast radius, business impact |
| 2 | Log Analysis & Anomaly Detection Engineer | Event timeline, error patterns, anomalies |
| 3 | Knowledge Base & Runbook Retrieval Specialist | Historical incidents, runbooks, advisories |
| 4 | Principal Root Cause Analysis Engineer | Causal chain, ranked hypotheses, evidence |
| 5 | Remediation & Resilience Architect | Immediate, 24h, and long-term action plans |
| 6 | Communications & Reporting Director | Executive report (Markdown, HTML, PDF) |

## Sample output

Open **[report.pdf](report.pdf)** for a presentation-ready incident briefing (cover page, KPIs, timeline, RCA, remediation plan).

| File | Description |
|------|-------------|
| `report.pdf` | PDF for leadership / portfolio demos |
| `report.html` | Styled web document |
| `report.md` | Markdown source report |

## Quick start

### Prerequisites

- Python 3.10–3.13
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-incident-intelligence-crewai.git
cd enterprise-incident-intelligence-crewai

cp .env.example .env
# Edit .env and set GEMINI_API_KEY

uv sync
```

### Run the full pipeline

```bash
crewai run
```

This runs all six agents against the Northwind Financial demo scenario and writes:

- `report.md`
- `report.html`
- `report.pdf`

### Regenerate PDF only (no LLM calls)

```bash
uv run python -m enterprise_incident_intelligence_resolution_system.report_builder
```

## Project structure

```
├── data/                    # Demo incident data (JSON, logs, metrics)
├── src/
│   └── enterprise_incident_intelligence_resolution_system/
│       ├── config/
│       │   ├── agents.yaml  # Agent roles & backstories
│       │   └── tasks.yaml   # Task pipeline definition
│       ├── crew.py          # Crew orchestration
│       ├── demo_inputs.py   # Realistic demo scenario
│       ├── main.py          # Entry point
│       └── report_builder.py # HTML/PDF report generator
├── report.pdf               # Sample output
├── .env.example
└── pyproject.toml
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `MODEL` | No | Default: `google/gemini-2.5-flash` |
| `EMBEDDINGS_GOOGLE_GENERATIVE_AI_MODEL_NAME` | No | Default: `gemini-embedding-001` |
| `EXA_API_KEY` | No | Enables Exa web search tool |
| `CONTEXTUAL_AI_API_KEY` | No | Enables Contextual AI RAG tool |

## Stack

- CrewAI 1.15 with Google Gemini (`crewai[google-genai]`)
- RAG search tools: JSON, TXT, CSV, PDF, website
- PDF generation via xhtml2pdf

## License

MIT

## Publish to GitHub

```powershell
cd enterprise_incident_intelligence_resolution_system_v1_crewai-project

git init
git add .
git status                    # confirm .env is NOT listed
git commit -m "Initial commit: CrewAI enterprise incident intelligence system"

# Create repo on github.com/new, then:
git remote add origin https://github.com/YOUR_USERNAME/enterprise-incident-intelligence-crewai.git
git branch -M main
git push -u origin main
```

**GitHub repo description (paste in repo settings):**

> Multi-agent CrewAI system that autonomously triages IT incidents, analyzes logs, retrieves runbooks, performs root-cause analysis, and generates executive PDF reports.

**Topics:** `crewai` `multi-agent` `incident-response` `root-cause-analysis` `gemini` `ai-agents` `devops` `sre`

> **Security:** Never commit `.env`. Rotate any API keys that were shared or exposed before publishing.
