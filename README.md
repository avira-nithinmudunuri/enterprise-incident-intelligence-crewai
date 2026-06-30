# Enterprise Incident Intelligence & Resolution System

Multi-agent [CrewAI](https://crewai.com) pipeline that autonomously triages IT incidents, analyzes logs, retrieves runbooks, performs root-cause analysis, and generates executive-ready PDF reports.

**Demo scenario:** INC-2026-0847 — Northwind Financial customer portal P1 outage (database connection pool exhaustion, ~2.1M customers affected).

**[workflow.html](workflow.html)** — Visual diagram of the six-agent pipeline.

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

## Outputs

Running `crewai run` generates incident reports locally (not committed to the repo):

| File | Description |
|------|-------------|
| `report.pdf` | PDF for leadership briefings |
| `report.html` | Styled web document |
| `report.md` | Markdown source report |

## Quick start

### Prerequisites

- Python 3.10–3.13
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Setup

```bash
git clone https://github.com/avira-nithinmudunuri/enterprise-incident-intelligence-crewai.git
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
├── workflow.html            # Visual agent pipeline diagram
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
