<div align="center">

<img src="britcore_logo.png" alt="Britcore.AI" width="300"/>

<br/>
<br/>

# Multi-Agent Data Pipeline

### 6 specialised AI agents that autonomously process any data source

<br/>

[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen?style=flat-square)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange?style=flat-square)](https://anthropic.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/harshitboots/multi-agent-data-pipeline?style=flat-square&color=yellow)](https://github.com/harshitboots/multi-agent-data-pipeline/stargazers)
[![Forks](https://img.shields.io/github/forks/harshitboots/multi-agent-data-pipeline?style=flat-square&color=blue)](https://github.com/harshitboots/multi-agent-data-pipeline/network)

<br/>

**[🚀 Quick Start](#quick-start) · [⚡ What's New in v2.0](#whats-new-in-v20) · [🔀 Router Engine](#router-engine) · [📡 Observability](#observability-dashboard) · [🔌 Connectors](#data-sources) · [🤝 Contributing](#contributing)**

<br/>

> *Upload a messy CSV, a complex PDF, or connect your database —*
> *watch 6 AI agents autonomously clean, anonymise, validate, transform,*
> *detect anomalies and summarise your data in real time.*

<br/>

<!-- SCREENSHOT: Full browser screenshot of the app homepage (dark theme, all 6 agent cards visible). Save as docs/images/hero.png -->
<img src="docs/images/hero.png" alt="Multi-Agent Data Pipeline UI" width="900"/>

</div>

---

## What's New in v2.0

> **v2.0.0 — June 2026** · [Full changelog](CHANGELOG.md)

| Feature | Detail |
|---------|--------|
| **Router Engine** | Simple agents → Haiku (cheap), Complex agents → Sonnet (quality). Cost drops from ~£0.27 to ~£0.08 per run |
| **Parallel Execution** | 5 Wave 1 agents run concurrently — 63% latency reduction, zero quality impact |
| **Observability Dashboard** | Full OmniGent-style traces: cost, latency, prompts, raw responses, guardrails — all persisted to SQLite |
| **Cost Comparison** | Single toggle to switch modes — side-by-side cost dashboard auto-appears when both modes run |
| **Guardrails Engine** | Configurable thresholds: budget cap, timeout, PII limits, parse-failure limits |
| **BYOK** | 2 free runs per GitHub user · +1 if you ⭐ star the repo · then bring your own Anthropic key |

---

## The Problem

Every data team has the same nightmare.

You get a CSV from a stakeholder. It has:
- Dates in 3 different formats
- Missing customer IDs on 20% of rows
- A price of £999.99 that should be £9.99
- Column names that change every month
- No documentation. No schema. No context.

You spend **3 hours** writing cleaning scripts.
Then the next file arrives and breaks everything.

**There has to be a better way.**

---

## The Solution

Instead of writing rules, deploy agents.

Each agent has a single job, its own reasoning, and structured output.
In v2.0 the first five agents run in **parallel** — then the Summariser
gets full context from all of them.

```
                  Your messy data
                        ↓
               ┌─────────────────┐
               │   Router Engine  │  ← picks cheapest model per agent
               └────────┬────────┘
                        │
          ┌─────────────┼─────────────┐
   ╔══════▼══════╗  ╔══▼════════╗  ╔══▼══════════╗
   ║   Cleaner   ║  ║  PII Anon ║  ║  Validator  ║  ← Wave 1
   ║   (Haiku)   ║  ║  (regex)  ║  ║  (Sonnet)   ║    parallel
   ╚═════════════╝  ╚═══════════╝  ╚═════════════╝
   ╔══════════════╗  ╔════════════════╗
   ║ Transformer  ║  ║ Anomaly Detect ║             ← Wave 1 (cont.)
   ║   (Haiku)    ║  ║   (Sonnet)     ║
   ╚══════════════╝  ╚════════════════╝
                        │
               ┌────────▼────────┐
               │   Summariser    │                  ← Wave 2
               │   (Sonnet)      │                    (after Wave 1)
               └────────┬────────┘
                        │
     Clean data + Full quality report + Cost trace
```

No config files. No rigid schemas. No rules to write and maintain.

---

## Quick Start

### Prerequisites

- Python 3.10+
- An Anthropic API key — get one free at [console.anthropic.com](https://console.anthropic.com)

---

### 1. Clone the repo

```bash
git clone https://github.com/harshitboots/multi-agent-data-pipeline.git
cd multi-agent-data-pipeline
```

### 2. Create virtual environment

```bash
python3 -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

```bash
cp .env.example .env
```

Open `.env` and add your key:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

### 5. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501)

The **Observability Dashboard** is available at [http://localhost:8501/observability](http://localhost:8501/observability)

### 6. Run the CLI

```bash
python main.py demo/sample_data.csv
```

---

## Router Engine

The router is the core new feature in v2.0. It inspects each agent's task complexity and assigns the cheapest model that can handle it — without any drop in output quality.

### Routing table

| Agent | Model | Reason | Cost per 1K tokens |
|-------|-------|--------|---------------------|
| Cleaner | Claude Haiku | Mechanical formatting — no reasoning needed | $0.80 input / $4.00 output per M |
| PII Anonymiser | Regex engine | Pure pattern matching — no LLM call at all | **Free** |
| Transformer | Claude Haiku | Column derivation — structured, deterministic | $0.80 input / $4.00 output per M |
| Validator | Claude Sonnet | Schema reasoning — needs careful judgment | $3.00 input / $15.00 output per M |
| Anomaly Detector | Claude Sonnet | Statistical reasoning + pattern detection | $3.00 input / $15.00 output per M |
| Summariser | Claude Sonnet | Business insights — full quality required | $3.00 input / $15.00 output per M |

### Cost comparison per run (demo CSV, 15 rows)

| Mode | Cost (GBP) | Latency |
|------|-----------|---------|
| Without Router — all Sonnet | ~£0.27 | ~14s sequential |
| **With Router — routed** | **~£0.08** | **~5s parallel** |
| **Saving** | **~70%** | **~63%** |

### Using the toggle

In the CSV Pipeline section, flip the toggle:

```
[ Enable Router — routes agents to Haiku (fast) or Sonnet (quality) ]
```

Run once without router → run once with router → the comparison dashboard auto-appears.

---

## Parallel Execution

In v1.0 agents ran one after another (sequential). In v2.0:

- **Wave 1** — Cleaner, PII Anonymiser, Validator, Transformer, Anomaly all run at the same time via `ThreadPoolExecutor(max_workers=5)`
- **Wave 2** — Summariser runs after Wave 1 completes, receiving the combined output of all five agents as context

Wall-clock time = slowest Wave 1 agent + Summariser (~5.2s total vs ~14.2s sequential).

This is **mathematically safe** — the same input goes to each agent, the same output comes back. The only thing that changes is the order of completion, not the result.

---

## Observability Dashboard

Open [http://localhost:8501/observability](http://localhost:8501/observability) after running the app.

Every pipeline run is logged to `pipeline_runs.db` (SQLite, auto-created, gitignored).

### 6 tabs

| Tab | What you see |
|-----|-------------|
| **Live Monitor** | Last run — agent waterfall with latency bars, cost per agent, Agent Inspector (full prompts + raw responses + parsed output) |
| **Run History** | All runs in a table — click any run to drill into per-agent spans |
| **Cost Analytics** | Spend over time line chart, Haiku vs Sonnet breakdown, cost by mode (baseline vs routed) |
| **Agent Performance** | Reliability %, avg latency (s), avg cost, parse failure rate — per agent, across all runs |
| **Guardrails Log** | Every guardrail event with severity (🔴 critical / 🟡 warning / 🔵 info), value vs threshold, action taken |
| **Settings** | Configure guardrail thresholds — changes apply to the next pipeline run |

### Guardrails

Configure in the Settings tab or pass a `GuardrailEngine` directly:

```python
from src.observability.guardrails import GuardrailEngine

guardrails = GuardrailEngine(
    budget_cap_gbp=0.50,      # stop run if this is exceeded mid-pipeline
    agent_timeout_s=30,        # skip agent and mark timeout if it hangs
    min_completeness=60.0,     # warn if validator score drops below this
    max_pii_rows=0,            # warn if any PII rows found (0 = always warn)
    max_parse_failures=3,      # abort if this many agents fail to parse JSON
    anomaly_score_warn=9.0,    # warn if anomaly score exceeds this
)
```

---

## Free Access & BYOK

The app is free to try — cost is controlled so it stays open to everyone.

| Tier | Runs | How |
|------|------|-----|
| Free | 2 runs | Enter your GitHub username |
| Star bonus | +1 run | Star this repo — verified via GitHub API |
| BYOK | Unlimited | Provide your own `sk-ant-...` key |

Your API key is stored in `st.session_state` only — it is never written to SQLite, files, or logs. It disappears when you close the browser tab.

Each free run uses router mode (~£0.06/run) to keep total cost under control.

---

## How It Works

### Agent Design Philosophy

Each agent is a **specialised Claude AI instance** with:
- A focused system prompt defining its exact role
- A strict JSON output schema enforced by Pydantic
- A `model` parameter so the router can assign the right Claude model
- A `span` parameter that captures tokens in/out, cost, latency, prompts and raw response
- Graceful error handling with typed fallback responses

No LangChain. No bloated frameworks. Just clean Python and direct API calls.

---

### The 6 CSV Pipeline Agents

#### 🧹 Agent 1 — Cleaner (Haiku)
Identifies and fixes data quality issues before anything else runs.

```python
{
    "issues_fixed": [
        "Inconsistent date formats — standardised to YYYY-MM-DD",
        "Missing product names — flagged 1 row",
        "Missing store IDs — flagged 1 row"
    ],
    "rows_affected": 6,
    "cleaned_columns": ["date", "product_name", "store_id"]
}
```

#### 🔒 Agent 2 — PII Anonymiser (Regex — free)
Scans every row for personal data — emails, phone numbers, card numbers and
postcodes — and masks it before any LLM call sees the data.

```python
{
    "pii_found": [
        "Row 4: email: 1 found",
        "Row 9: phone: 1 found",
        "Row 12: card_number: 1 found"
    ],
    "rows_affected": 3,
    "pii_types_detected": ["card_number", "email", "phone"],
    "anonymised_preview": "...,j***@***.com,***** ****56,**** **** **** 1234,..."
}
```

#### 🛡 Agent 3 — Validator (Sonnet)
Checks schema correctness, data types, constraints and completeness.

```python
{
    "schema_ok": true,
    "violations": [
        "Missing customer_id in rows 8",
        "Negative unit_price in row 11"
    ],
    "passed_checks": ["All transaction IDs unique", "Quantity values positive"],
    "completeness_score": 91.1
}
```

#### ⚡ Agent 4 — Transformer (Haiku)
Standardises, normalises and derives new columns from existing data.

```python
{
    "transformations_applied": [
        "Standardised all dates to ISO 8601",
        "Normalised product names to title case"
    ],
    "new_columns": ["year", "month", "day_of_week", "price_band", "is_weekend"],
    "rows_transformed": 15
}
```

#### 📡 Agent 5 — Anomaly Detector (Sonnet)
Finds statistical outliers, impossible values and suspicious patterns.

```python
{
    "anomalies": [
        "TXN007: total £999.99 — expected ~£51.96 for 4 × £12.99",
        "TXN011: negative unit_price -£5.00 — impossible value"
    ],
    "anomaly_count": 7,
    "anomaly_score": 8.5,
    "flagged_rows": [7, 11]
}
```

#### 📊 Agent 6 — Summariser (Sonnet)
Produces a business-readable summary with key stats and recommendations.
Receives the combined output of all 5 Wave 1 agents as context.

```python
{
    "summary": "Dataset contains 15 retail transactions across 5 categories...",
    "key_stats": {
        "Total Revenue": "£413.56",
        "Top Category": "Skincare",
        "Date Range": "15–20 Jan 2024"
    },
    "recommendations": [
        "Investigate TXN007 — possible data entry error",
        "Standardise date format across all upstream systems"
    ]
}
```

---

### The 5 PDF Intelligence Agents

| Agent | Input | Output |
|-------|-------|--------|
| **📄 PDF Parser** | Raw PDF text | Document type, language, quality, key topics |
| **🔍 Entity Extractor** | PDF text | People, orgs, dates, amounts, emails, locations |
| **⚠️ Risk Detector** | PDF text | PII flags, GDPR risks, legal/financial red flags |
| **✅ Action Extractor** | PDF text | Todos, decisions, deadlines, owners |
| **📊 Summariser** | All agent context | Business summary + recommendations |

---

### Architecture

```
multi-agent-data-pipeline/
├── pages/
│   └── observability.py          # Streamlit multipage — 6-tab observability dashboard  [NEW v2.0]
├── src/
│   ├── agents/
│   │   ├── cleaner.py            # CSV cleaning agent — Haiku, emits telemetry span
│   │   ├── pii_anonymiser.py     # PII detection & anonymisation — regex, zero token cost
│   │   ├── validator.py          # CSV validation agent — Sonnet, emits telemetry span
│   │   ├── transformer.py        # CSV transformation agent — Haiku, emits telemetry span
│   │   ├── anomaly.py            # Anomaly detection agent — Sonnet, emits telemetry span
│   │   ├── summariser.py         # Summarisation agent — Sonnet, emits telemetry span
│   │   ├── pdf_parser.py         # PDF parsing agent
│   │   ├── entity_extractor.py   # Entity extraction agent
│   │   ├── risk_detector.py      # Risk detection agent
│   │   └── action_extractor.py   # Action item agent
│   ├── auth/                                                                             [NEW v2.0]
│   │   ├── credits.py            # Free-run credit tracking per GitHub username, BYOK
│   │   └── github_api.py         # GitHub API — repo stats, star/fork verification
│   ├── connectors/
│   │   ├── databricks.py         # Azure Databricks
│   │   ├── snowflake_conn.py     # Snowflake
│   │   ├── postgres.py           # PostgreSQL
│   │   ├── mysql.py              # MySQL
│   │   ├── bigquery.py           # BigQuery
│   │   └── duckdb_conn.py        # DuckDB
│   ├── observability/                                                                    [NEW v2.0]
│   │   ├── tracer.py             # AgentSpan + RunTracer — captures tokens, cost, latency, prompts
│   │   ├── store.py              # SQLite persistence — runs, spans, guardrails, budget
│   │   ├── guardrails.py         # GuardrailEngine — budget cap, timeout, PII, parse-failure limits
│   │   └── metrics.py            # Analytics queries — cost trend, agent perf, model breakdown
│   ├── cost_config.py            # Model names, pricing (GBP), token limits, timeouts  [NEW v2.0]
│   ├── router.py                 # Router engine — assigns cheapest model per agent    [NEW v2.0]
│   ├── models.py                 # Pydantic schemas — extended with AgentTelemetry
│   └── pipeline.py               # Orchestrator — parallel Wave 1, router, telemetry
├── demo/
│   ├── sample_data.csv           # Demo CSV with intentional data quality issues
│   └── sample_report.pdf         # Demo PDF quarterly report
├── contrib/
│   ├── azure/                    # Azure deployment guide
│   ├── databricks/               # Databricks implementation
│   ├── aws/                      # AWS Lambda implementation
│   └── docker/                   # Docker deployment
├── tests/
│   └── test_pipeline.py          # 16 passing tests
├── pipeline_runs.db              # SQLite — auto-created on first run (gitignored)
├── app.py                        # Streamlit UI — router toggle, BYOK, cost dashboard
├── main.py                       # CLI entrypoint
└── requirements.txt
```

---

### Sequence Flow (v2.0 — parallel)

```
User uploads CSV / PDF / connects DB
                ↓
        Pipeline Orchestrator
                ↓
        ┌───────────────┐
        │ Router Engine  │ ← assigns model per agent
        └───────┬───────┘
                │
  ┌─────────────┼─────────────┬─────────────┬─────────────┐
  ▼             ▼             ▼             ▼             ▼
Cleaner      PII Anon     Validator    Transformer    Anomaly     ← Wave 1 (parallel)
(Haiku)      (regex)      (Sonnet)      (Haiku)      (Sonnet)
  │             │             │             │             │
  └─────────────┴─────────────┴──────┬──────┴─────────────┘
                                      ▼
                                 Summariser                      ← Wave 2
                                  (Sonnet)
                                      │
                          ┌───────────▼───────────┐
                          │  RunTracer + SQLite     │ ← persists all spans
                          └───────────────────────┘
                                      │
                       PipelineResult (combined)
                                      │
                    CLI table + JSON export + UI display
                    + Observability dashboard updates
```

---

## Data Sources

### 📄 CSV Upload

Drop any CSV file — no schema required. The agents infer structure, detect issues and process automatically.

```bash
# CLI
python main.py your_data.csv

# With JSON output
python main.py your_data.csv --output results.json
```

Tested with:
- Retail transaction data
- Financial ledgers
- HR records
- IoT sensor readings
- Marketing campaign data
- Any flat file CSV

---

### 📑 PDF Intelligence

Upload any PDF document. Agents extract structured information automatically.

Best results with:
- Quarterly / annual reports
- Contracts and legal documents
- Invoices and purchase orders
- Meeting minutes and notes
- Research papers
- HR documents and policies

---

### 🔌 Database Connectors

Connect directly to your database. Agents fetch any table and run the full pipeline.

#### Azure Databricks

```python
from src.connectors.databricks import fetch_table

df = fetch_table(
    host="adb-xxxxx.azuredatabricks.net",
    token="dapi...",
    http_path="/sql/1.0/warehouses/xxxxx",
    table="catalog.schema.table_name"
)
```

#### Snowflake

```python
from src.connectors.snowflake_conn import fetch_table

df = fetch_table(
    account="xy12345.eu-west-1",
    user="my_user",
    password="my_password",
    database="MY_DATABASE",
    schema="PUBLIC",
    table="MY_TABLE"
)
```

#### PostgreSQL

```python
from src.connectors.postgres import fetch_table

df = fetch_table(
    host="localhost",
    port=5432,
    database="my_database",
    user="postgres",
    password="my_password",
    table="my_table"
)
```

#### MySQL

```python
from src.connectors.mysql import fetch_table

df = fetch_table(
    host="localhost",
    port=3306,
    database="my_database",
    user="root",
    password="my_password",
    table="my_table"
)
```

#### BigQuery

```python
from src.connectors.bigquery import fetch_table

df = fetch_table(
    project_id="my-gcp-project",
    credentials_json=credentials_dict,
    dataset="my_dataset",
    table="my_table"
)
```

#### DuckDB

```python
from src.connectors.duckdb_conn import fetch_table

df = fetch_table(
    database="/path/to/my_database.duckdb",
    table="my_table"
)
```

---

### Connector Status

| Database | Auth Method | Fetch | Pipeline | Status |
|----------|------------|-------|----------|--------|
| Azure Databricks | PAT Token | ✅ | ✅ | Stable |
| Snowflake | User/Pass | ✅ | ✅ | Stable |
| PostgreSQL | User/Pass | ✅ | ✅ | Stable |
| MySQL | User/Pass | ✅ | ✅ | Stable |
| BigQuery | Service Account JSON | ✅ | ✅ | Stable |
| DuckDB | File path | ✅ | ✅ | Stable |
| MongoDB | — | 🔜 | 🔜 | Planned |
| Redshift | — | 🔜 | 🔜 | Planned |
| Microsoft Fabric | — | 🔜 | 🔜 | Planned |

> Want to add a connector? See [Contributing](#contributing)

---

## Deploy to Production

This pipeline runs locally out of the box. For production deployment it's compatible with every major cloud platform.

---

### 🐳 Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t multi-agent-pipeline .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=sk-ant-... multi-agent-pipeline
```

---

### ☁️ Azure

**Option 1 — Azure Container Apps**
```bash
az containerapp create \
  --name multi-agent-pipeline \
  --resource-group my-rg \
  --image my-registry/multi-agent-pipeline:latest \
  --env-vars ANTHROPIC_API_KEY=sk-ant-...
```

**Option 2 — Azure Databricks Job**
```python
# Run as a Databricks notebook job
# Point pipeline at any Unity Catalog table
# Schedule via ADF pipeline trigger
```

**Option 3 — Azure Functions**
```python
# Trigger on Blob Storage upload
# Process CSV and store results to ADLS
# Integrate with ADF for orchestration
```

---

### ☁️ AWS

**Option 1 — AWS Lambda + S3**
```python
import boto3
from src.pipeline import run_pipeline

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # Download CSV from S3, run pipeline, store results back to S3
```

**Option 2 — ECS + Fargate**
```bash
# Deploy as a containerised service
# Auto-scale based on queue depth
# Integrate with SQS for async processing
```

---

### ☁️ GCP

**Cloud Run**
```bash
gcloud run deploy multi-agent-pipeline \
  --image gcr.io/my-project/multi-agent-pipeline \
  --platform managed \
  --set-env-vars ANTHROPIC_API_KEY=sk-ant-...
```

---

### 🚀 Render / Railway (Free Tier)

One-click deploy — zero infrastructure setup.

**Render:**
1. Fork this repo
2. Connect to Render
3. Set `ANTHROPIC_API_KEY` environment variable
4. Deploy — live URL in 2 minutes

**Railway:**
```bash
railway login
railway init
railway up
```

---

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | Your Anthropic API key (or use BYOK in the UI) |
| `DATABRICKS_HOST` | Optional | Databricks workspace URL |
| `DATABRICKS_TOKEN` | Optional | Databricks PAT token |
| `SNOWFLAKE_ACCOUNT` | Optional | Snowflake account identifier |
| `POSTGRES_HOST` | Optional | PostgreSQL host |
| `MYSQL_HOST` | Optional | MySQL host |

> See `.env.example` for the full list

---

## Contributing

This repo is built for the community. Every contribution makes it better for thousands of data engineers.

---

### Ways to Contribute

#### 🔌 Add a Database Connector

| Database | Difficulty | Issue |
|----------|-----------|-------|
| MongoDB | Medium | #1 |
| Redshift | Easy | #2 |
| Microsoft Fabric | Medium | #4 |
| Elasticsearch | Hard | #5 |

#### ☁️ Cloud Implementations

- `contrib/azure/` — ADF pipeline trigger
- `contrib/databricks/` — Full Databricks notebook
- `contrib/aws/` — Lambda + S3 trigger
- `contrib/docker/` — Production Docker setup
- `contrib/gcp/` — Cloud Run deployment

#### 🤖 New Agents

Ideas for new agents:

- **Schema Inferencer** — auto-detect and document schema
- **Data Lineage Tracker** — track where each column came from
- **Duplicate Detector** — find near-duplicate records
- **Language Translator** — translate non-English data fields

#### 🌍 Language Wrappers

- R package
- Node.js SDK
- Julia package

---

### Getting Started

```bash
# 1. Fork the repo on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/multi-agent-data-pipeline.git
cd multi-agent-data-pipeline

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create a branch
git checkout -b feature/mongodb-connector

# 6. Make your changes

# 7. Run tests — all must pass
pytest tests/ -v

# 8. Push and open a PR
git push origin feature/mongodb-connector
```

---

### Contribution Guidelines

- One feature per PR
- All tests must pass
- Add tests for new features
- Follow existing code style — each agent has the same structure
- Update README if adding a connector or agent

---

### Adding a New Connector

```python
# src/connectors/your_db.py

def connect(host: str, port: int, database: str, user: str, password: str):
    pass

def list_tables(host: str, ...) -> list:
    pass

def fetch_table(host: str, ..., table: str, limit: int = 1000) -> pd.DataFrame:
    pass
```

---

### Adding a New Agent

```python
# src/agents/your_agent.py

SYSTEM_PROMPT = """You are a [role] agent.
Respond ONLY with valid JSON. No markdown. No explanation."""

def run(csv_preview: str, total_rows: int,
        model: str = None, span=None) -> YourAgentResult:
    if model is None:
        model = MODELS["quality"]
    response = client.messages.create(model=model, ...)
    if span:
        span.finish(input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    model=model, raw_response=..., parsed_output=..., parse_ok=True)
    return result
```

---

### Contributors

| Avatar | Name | Contribution |
|--------|------|-------------|
| 👤 | [Harshit Tripathi](https://github.com/harshitboots) | Creator & maintainer |
| 👤 | *Your name here* | *Your contribution* |

---

## Running Tests

```bash
pytest tests/ -v
```

```
tests/test_pipeline.py::TestModels::test_cleaner_result_creation PASSED
tests/test_pipeline.py::TestModels::test_validator_result_creation PASSED
tests/test_pipeline.py::TestModels::test_transformer_result_creation PASSED
tests/test_pipeline.py::TestModels::test_anomaly_result_creation PASSED
tests/test_pipeline.py::TestModels::test_summariser_result_creation PASSED
tests/test_pipeline.py::TestModels::test_pii_anonymiser_result_creation PASSED
tests/test_pipeline.py::TestModels::test_pipeline_result_creation PASSED
tests/test_pipeline.py::TestCSVLoading::test_csv_loads_correctly PASSED
tests/test_pipeline.py::TestCSVLoading::test_csv_preview_generation PASSED
tests/test_pipeline.py::TestCSVLoading::test_demo_csv_exists PASSED
tests/test_pipeline.py::TestCSVLoading::test_demo_csv_has_correct_columns PASSED
tests/test_pipeline.py::TestCSVLoading::test_demo_csv_has_rows PASSED
tests/test_pipeline.py::TestPIIAnonymiser::test_anonymise_text_masks_email PASSED
tests/test_pipeline.py::TestPIIAnonymiser::test_anonymise_text_masks_card_number PASSED
tests/test_pipeline.py::TestPIIAnonymiser::test_anonymise_text_no_pii PASSED
tests/test_pipeline.py::TestPIIAnonymiser::test_run_detects_and_masks_pii PASSED
16 passed in 0.6s
```

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| AI — complex agents | Anthropic Claude Sonnet | claude-sonnet-4-6 |
| AI — simple agents | Anthropic Claude Haiku | claude-haiku-4-5-20251001 |
| Router Engine | Custom — `src/router.py` | v2.0 |
| Parallel Execution | `concurrent.futures.ThreadPoolExecutor` | stdlib |
| Observability | Custom SQLite tracer — `src/observability/` | v2.0 |
| Language | Python | 3.10+ |
| Data | Pandas, PyPDF | — |
| Validation | Pydantic v2 | — |
| CLI | Typer + Rich | — |
| UI | Streamlit | — |
| Persistence | SQLite (`pipeline_runs.db`) | — |
| Connectors | Databricks SDK, Snowflake, psycopg2, mysql-connector, BigQuery | — |
| Testing | pytest | — |

---

## Roadmap

- [x] CSV pipeline — 6 agents
- [x] PDF intelligence — 5 agents
- [x] Database connectors — 6 databases
- [x] Streamlit UI — dark theme
- [x] CLI entrypoint
- [x] JSON export
- [x] **Router Engine — Haiku / Sonnet routing** ✅ v2.0
- [x] **Parallel agent execution — 63% latency reduction** ✅ v2.0
- [x] **Observability dashboard — traces, cost, guardrails** ✅ v2.0
- [x] **BYOK — bring your own Anthropic key** ✅ v2.0
- [x] DuckDB connector
- [ ] pip package — `pip install multi-agent-data-pipeline`
- [ ] MongoDB connector
- [ ] Redshift connector
- [ ] Microsoft Fabric connector
- [ ] Agent memory — learn from past runs
- [ ] Webhook support — trigger via HTTP
- [ ] REST API — FastAPI wrapper
- [ ] Docker image on Docker Hub
- [ ] GitHub Actions CI/CD

---

## About

Built by **Harshit Tripathi** — Founder, Britcore AI · Lead Data Engineer

- Creator of **ATLAS Knowledge Graph** — AI-powered data lineage and discovery platform on Azure Databricks
- 10 years of experience across Azure, Databricks, PySpark, Unity Catalog, Microsoft Fabric
- Databricks Certified Professional
- Cross-industry background — retail, aerospace, healthcare

This project is part of the **Britcore.AI open source initiative** — building practical AI tools for data engineers.

| | |
|--|--|
| 🌐 Website | [britcore.ai](https://britcore.ai) |
| 🐙 GitHub | [github.com/harshitboots](https://github.com/harshitboots) |
| 💼 LinkedIn | [linkedin.com/in/harshittripathi](https://linkedin.com/in/harshittripathi) |

---

## License

MIT License — free to use, modify and distribute.

See [LICENSE](LICENSE) for full terms.

---

<div align="center">

<img src="britcore_logo.png" alt="Britcore.AI" width="200"/>

<br/>
<br/>

### If this tool saved you time or taught you something new

# ⭐ Star the repo

*It takes 2 seconds and helps thousands of data engineers find this tool.*
*You also unlock a bonus free run on the app.*

<br/>

[![Star this repo](https://img.shields.io/github/stars/harshitboots/multi-agent-data-pipeline?style=for-the-badge&color=yellow)](https://github.com/harshitboots/multi-agent-data-pipeline/stargazers)

<br/>

**Built with Claude AI · Powered by Britcore.AI · Made with ❤️ for the data engineering community**

</div>
