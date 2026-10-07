# AgencyOS — AI Agency Operating System

**Production-ready Streamlit + LangGraph + Copilot Cloud Agents system for autonomous AI agencies.**

Full codebase intelligence, marketing orchestration, sales pipeline, demand monitoring, idea mining & productization, bot provisioning, and multi-client isolation.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure secrets (.streamlit/secrets.toml or environment)
export GITHUB_TOKEN=ghp_...
export PAYPAL_CLIENT_ID=...
export PAYPAL_CLIENT_SECRET=...

# Run the app
streamlit run webhook_app.py
```

Open http://localhost:8501 and navigate to Client Dashboard.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         STREAMLIT FRONTEND (10 pages)               │
│  Dashboard │ Codebase │ Marketing │ Sales │ Ideas   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│     LANGGRAPH ORCHESTRATOR (8 agents)               │
│  Code │ Mktg │ Sales │ Demand │ Idea │ Bot │ CRM    │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│          MCP SERVERS (shared async loop)            │
│  DemandScope │ Graphify │ Synaptiq │ Chitti ...    │
└─────────────────────────────────────────────────────┘
```

## Key Features

### Codebase Intelligence (Triple-Engine)
- **Synaptiq**: Deep structural queries (impact, dead code, git diffs)
- **Graphify**: Multi-modal ingestion (code + docs + PDFs)
- **Copilot Agent**: Write-capable tasks (PRs, implementations)

### Idea Pipeline
- **Mining**: 4 extractors (dead code, diffs, demand spikes, TODOs)
- **Scoring**: Demand × Feasibility × Relevance (0-40 scale)
- **Cross-Client Signal**: Ideas appearing in 2+ clients get amplification bonus
- **PRD Auto-Draft**: Seed PRD at score ≥24, expand via Copilot Agent
- **Governance**: Licensing gate (require IP clearance) + Section approvals

### Hardening
- **Config**: Typed settings with secrets fallback chain
- **Logging**: Structured JSON + correlation IDs + PII redaction
- **Metrics**: In-process counters/histograms → SQLite spillover
- **Resilience**: Retry with exponential backoff, per-key circuit breakers
- **Jobs**: Thread-pool queue with SQLite persistence + DLQ
- **Isolation**: Per-tenant context checking, webhook dedup
- **Flags**: Per-client feature toggles (no restart needed)

## Database Schema

```
data/
├── audit.log              # Hash-chained audit trail
├── ideas.db               # Idea store + fingerprints + approvals
├── policies.db            # Runtime-tunable gates & scoring knobs
├── notifications.db       # Audit log of every alert sent
├── usage.db               # Per-client metering (cost tracking)
├── features.db            # Per-client feature flags
├── jobs.db                # Job queue + DLQ
├── webhooks.db            # Webhook delivery dedup (replay protection)
├── metrics.db             # Flushed metrics
├── audit.db               # Previous cycle before WAL recovery
└── repos/
    └── <client_id>/       # Cloned codebases
```

## Pages

1. **01_Client_Dashboard.py** — Overview, quick stats, onboarding
2. **02_Codebase_Analyzer.py** — 3-tab UI: Copilot dispatch, Graphify explorer, stats
3. **03_Marketing_Command.py** — Draft, approve, schedule posts; brand voice learning
4. **04_Sales_Billing.py** — Pipeline view, PayPal invoices, CRM sync
5. **05_Demand_Radar.py** — Real-time trends, alert thresholds
6. **06_Idea_Pipeline.py** — Kanban board, cross-client radar, PRD diff view, approvals
7. **07_Bot_Control.py** — Chitti (Eliza) + NanoClaw provisioning
8. **08_Admin.py** — Policies, feature flags, health checks, logs, DLQ, sweeps
9. **09_Onboarding.py** — (Coming) Multi-step client setup wizard
10. **10_Reports.py** — (Coming) Weekly/monthly client-facing reports

## Policies (Runtime-Tunable)

All persist in DB, no restart needed:

- `prd_section_gate_enabled` — Require all PRD sections approved before backlog
- `prd_section_gate_min_approved` — Minimum sections approved (0 = all)
- `licensing_default_ttl_days` — Default clearance expiry in UI (365)
- `idea_min_score_for_prd` — Auto-PRD threshold (24)
- `cross_client_bonus_per_client` — Amplification per extra client (3 pts)
- `cross_client_bonus_cap` — Max cross-client bonus (9 pts)

## Deployment

### Streamlit Cloud (Recommended for MVP)
```bash
git push origin main
# Connect repo in Streamlit Cloud dashboard
# Set secrets in Streamlit Cloud secrets manager
```

### Self-Hosted (Docker)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "webhook_app.py"]
```

### Environment Variables
```bash
GITHUB_TOKEN=ghp_...
GITHUB_WEBHOOK_SECRET=whsec_...
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_MODE=sandbox|live
AYRSHARE_API_KEY=...

# Notifications (optional)
SLACK_WEBHOOK=https://hooks.slack.com/services/...
DISCORD_WEBHOOK=https://discordapp.com/api/webhooks/...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASS=...
ADMIN_EMAIL=...

# Runtime
AGENCYOS_ENVIRONMENT=production
AGENCYOS_RATE_LIMIT_PER_HOUR=2500
AGENCYOS_JOB_WORKERS=4
```

## Testing

```bash
pytest tests/ -v
```

Coverage:
- Idea pipeline (cross-client, scoring, gates, approvals)
- Retry & circuit breaker logic
- Job queue (claim, finish, requeue stale)
- Tenant isolation violations
- Policy enforcement

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes, test locally
3. Push and open a PR
4. All changes logged in audit trail

## License

MIT
