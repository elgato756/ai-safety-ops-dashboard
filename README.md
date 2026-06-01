# AI Safety Ops Dashboard

A human-in-the-loop Trust & Safety risk intelligence dashboard for monitoring external AI risk signals, supporting analyst triage, escalating high-severity incidents, and preserving audit trails.

This project does **not** make automated enforcement, legal, account-level, or policy decisions. It is an analyst-assist prototype intended to help operations teams identify, organize, prioritize, and escalate risk signals for human review.

---

## Why This Project Matters

Trust & Safety teams working on AI products need to identify new and complex safety, policy, abuse, fraud, and integrity risks quickly. External signals are messy, API access can be unreliable, and operational decisions often require careful human judgment.

This project demonstrates a practical risk-intelligence workflow for AI platforms. It combines external signal monitoring, AI-assisted triage, analyst review, escalation, regulatory source tracking, and audit logging into one operational dashboard.

The goal is not automated enforcement. The goal is to help analysts reduce detection latency, structure messy external signals, and make better escalation decisions while preserving human review.

---

## Role Alignment

This project is designed to map to Trust & Safety, Risk Operations, Safety Systems, and abuse-response workflows.

It demonstrates experience with:

- emerging abuse and misuse signal detection
- fraud, scam, phishing, jailbreak, and deepfake risk triage
- regulatory and policy source monitoring
- human-in-the-loop review workflows
- severity and confidence scoring
- escalation pathways
- analyst notes and audit trails
- graceful degradation when external systems fail
- cross-functional handoff patterns for Legal, Policy, Security, Fraud, and Trust & Safety teams

---

## Core Features

- Reddit signal ingestion with demo fallback behavior
- X / Twitter public signal monitoring with demo fallback behavior
- Regulatory and policy source monitoring
- AI-assisted risk classification using the OpenAI API
- Safe fallback classification when model access is unavailable
- Severity and confidence scoring
- Recommended review team selection
- Analyst notes and incident lifecycle updates
- Escalation workflow with optional Slack webhook support
- Persistent local incident database using SQLite
- Audit trails for analyst actions and escalations
- Next.js dashboard frontend
- FastAPI backend

---

## Screenshots

### Main Dashboard

![Main dashboard](docs/screenshots/dashboard.png)

### Incident Detail Panel

![Incident detail panel](docs/screenshots/incident-detail.png)

### Audit Trail

![Audit trail](docs/screenshots/audit-trail.png)

---

## Demo Video

A short demo video can be added here after recording:

```text
Demo video link: add Loom, YouTube, or GitHub video link here
```

Recommended demo flow:

1. Start the backend and frontend.
2. Seed demo incidents.
3. Scan Reddit, X, or regulatory sources.
4. Open an incident detail panel.
5. Review AI summary, severity, confidence, and recommended review path.
6. Add analyst notes.
7. Escalate the incident.
8. Show the audit trail.

---

## Architecture

```text
ai-safety-ops-dashboard/
├── backend/
│   ├── main.py
│   ├── ai/
│   │   └── classifier.py
│   ├── db/
│   │   └── database.py
│   ├── ingestion/
│   │   ├── reddit_ingest.py
│   │   ├── x_ingest.py
│   │   └── regulatory_ingest.py
│   ├── models/
│   │   └── incident.py
│   ├── services/
│   │   ├── demo_seed_service.py
│   │   ├── incident_service.py
│   │   └── slack_service.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.js
│
├── docs/
│   ├── demo_runbook.md
│   ├── portfolio_positioning.md
│   └── screenshots/
├── .gitignore
└── README.md
```

---

## Quick Demo Flow

Start the backend:

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Start the frontend in a second terminal:

```bash
cd frontend
npm run dev
```

Seed demo incidents:

```bash
curl -X POST http://localhost:8000/demo/seed
```

Reset demo data:

```bash
curl -X POST http://localhost:8000/demo/reset
```

Open the dashboard:

```text
http://localhost:3000
```

Open the backend API docs:

```text
http://localhost:8000/docs
```

---

## Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run the backend:

```bash
uvicorn main:app --reload
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

---

## API and Integration Details

This project supports multiple external integrations, but it is intentionally designed to remain demoable even when third-party APIs are unavailable, rate-limited, paid, blocked, or missing credentials.

The goal is to demonstrate the operational workflow: signal ingestion, risk classification, analyst review, escalation, and auditability. External APIs improve realism, but the demo does not depend on every external service working perfectly.

---

### Environment Variables

Create a local backend environment file:

```bash
cd backend
cp .env.example .env
nano .env
```

Example `.env` file:

```text
OPENAI_API_KEY=sk-your-openai-api-key
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
SLACK_WEBHOOK_URL=
X_BEARER_TOKEN=
ESCALATION_SEVERITY_THRESHOLD=8
```

Never commit `.env` to GitHub. The `.env` file should stay local only.

---

### OpenAI API

The OpenAI API powers the AI-assisted analysis layer of the dashboard.

It is used for:

- risk classification
- analyst-facing summaries
- severity scoring
- confidence scoring
- recommended review team selection
- suggested next steps
- structured incident analysis

Configure it in `backend/.env`:

```text
OPENAI_API_KEY=sk-your-openai-api-key
```

If the OpenAI API key is missing, invalid, or out of quota, the backend uses a safe fallback classification so the demo still works.

Fallback behavior:

```text
category: needs_review
severity: 5
confidence: 0.5
review team: trust_and_safety_triage
```

This fallback is intentional. In a real Trust & Safety environment, analyst workflows should not completely fail just because a model provider, API key, or quota configuration is temporarily unavailable. The system should degrade gracefully, preserve the incoming signal, and route it for human review.

---

### Reddit API

Reddit is used as a social signal source for identifying emerging AI-related risk discussions.

It can help monitor:

- AI-related Reddit communities
- emerging misuse discussions
- jailbreak chatter
- fraud or scam enablement discussions
- public user concerns around AI behavior
- early signals that may warrant Trust & Safety review

Current behavior:

- The backend attempts Reddit ingestion.
- If Reddit blocks public access or returns an error, the backend uses demo fallback Reddit signals.
- This keeps the dashboard demoable without requiring Reddit credentials.

Optional configuration in `backend/.env`:

```text
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
```

To create Reddit API credentials:

1. Go to Reddit app preferences.
2. Create a new app.
3. Choose `script`.
4. Copy the client ID and client secret.
5. Add them to `backend/.env`.

The prototype currently works without Reddit credentials because fallback demo data is included. This is useful for demos because Reddit access can be inconsistent, blocked, or dependent on API configuration.

---

### X / Twitter API

The X / Twitter API supports the public signal monitoring layer of the dashboard.

It is used for:

- monitoring public AI risk chatter
- identifying viral misuse signals
- tracking reputational risk
- surfacing jailbreak discussions
- detecting AI scam, phishing, and impersonation reports
- monitoring deepfake fraud discussion
- tracking public conversation around AI regulation and policy developments
- collecting early warning signals that may require Trust & Safety analyst review

Configure it in `backend/.env`:

```text
X_BEARER_TOKEN=your-x-bearer-token
```

If `X_BEARER_TOKEN` is present, the backend attempts to use X recent search.

If the X API token is missing, restricted, unpaid, rate-limited, or unavailable, the backend uses demo fallback X signals so the dashboard still works.

Fallback behavior:

```text
source: x_demo_fallback
category: needs_review
signal type: public_ai_risk_chatter
status: reviewable_demo_signal
```

This fallback is intentional. Public social APIs can be paid, restricted, unstable, or unavailable depending on account access and API plan. In a real Trust & Safety environment, a monitoring workflow should not fail completely because one external signal source is unavailable.

Instead, the system should degrade gracefully, preserve the analyst workflow, and continue supporting triage, escalation, notes, and audit logging.

X / Twitter is treated as a monitoring lead source, not a source of verified truth. Signals from X should be reviewed by a human analyst and, when necessary, verified against additional sources before operational action is taken.

---

### Slack Webhook

Slack is used to simulate escalation into an internal response workflow.

It can support:

- high-severity incident alerts
- routing to policy, legal, security, or fraud teams
- operational response workflows
- analyst-to-team handoff
- incident visibility for stakeholders

Optional configuration in `backend/.env`:

```text
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

Current behavior:

- If `SLACK_WEBHOOK_URL` is present, escalation actions can send Slack alerts.
- If it is blank, the app still works.
- Escalation status and audit events are still recorded locally even without Slack.

This makes the Slack integration optional while preserving the core workflow. The demo can still show that an incident was escalated, recorded, and added to the audit trail.

---

### Regulatory and Policy Sources

The regulatory scanner monitors official policy-source references and turns them into reviewable policy signals.

It is intended to help Trust & Safety, legal, and policy teams track developments from authoritative sources.

Current official-source references include:

- NIST AI Risk Management Framework
- NIST AI RMF Core
- European Commission AI Act implementation timeline
- EUR-Lex official EU Artificial Intelligence Act legal reference

The app stores regulatory metadata such as:

- jurisdiction
- authority
- compliance area
- source type
- verification status
- effective date when available

The regulatory source system is designed around source hierarchy:

1. Official government, regulator, standards-body, or legislative sources are treated as high-confidence references.
2. Secondary sources, social media, blogs, or commentary should be treated only as monitoring leads.
3. The system does not automatically convert regulatory text into binding compliance requirements.

Regulatory outputs are intended for legal and policy review. The system does not provide legal advice, make compliance decisions, or automatically interpret law into operational obligations.

---

### Demo Seed and Reset Endpoints

The backend includes demo endpoints so the dashboard can be populated quickly for presentations.

Useful backend endpoints:

```text
POST /demo/seed
POST /demo/reset
```

`POST /demo/seed` creates realistic test incidents across:

- jailbreak sharing
- AI phishing
- deepfake fraud
- prompt injection
- privacy/data exposure
- EU AI Act regulatory monitoring
- FTC-style consumer protection risk

`POST /demo/reset` clears local incidents and audit events.

These endpoints are useful for portfolio demos because they let reviewers see the full workflow without depending on live external APIs.

The seed data is not meant to represent real incidents. It is designed to demonstrate how the system handles different categories of risk, severity, confidence, escalation, analyst notes, and audit logging.

---

### Escalation Threshold

The backend can recommend escalation when an incident reaches a configured severity threshold.

Configure it in `backend/.env`:

```text
ESCALATION_SEVERITY_THRESHOLD=8
```

Default:

```text
8
```

Incidents at or above this severity can trigger escalation recommendations and audit events.

This simulates how an internal Trust & Safety operations team might define thresholds for human review, policy escalation, security review, legal review, or fraud investigation.

---

## Risk Taxonomy

Current prototype categories include:

- jailbreak sharing
- prompt injection
- fraud or scam enablement
- coordinated abuse
- synthetic identity abuse
- malware or social engineering assistance
- deepfake impersonation
- privacy or data exposure
- regulatory risk
- reputational risk
- unknown or low relevance

---

## Demo Resilience

The system is intentionally designed to degrade gracefully.

| Dependency | If unavailable |
|---|---|
| OpenAI API | Uses `needs_review` fallback classification |
| Reddit | Uses demo Reddit risk signals |
| X / Twitter | Uses demo X risk signals |
| Slack | Records escalation locally without sending a Slack message |
| Regulatory page scraping | Uses curated official-source fallback records |

This keeps the demo reliable while still showing how production integrations would work.

The fallback behavior is part of the product design, not just a workaround. In operational risk tooling, brittle dependencies can cause missed signals. This prototype preserves the signal and routes it for human review even when an integration fails.

---

## Human-in-the-Loop Positioning

This project is an analyst-assist prototype.

It does not:

- make automated enforcement decisions
- make legal decisions
- make account-level moderation decisions
- replace human Trust & Safety analysts

It does:

- aggregate emerging signals
- structure messy information
- classify potential risk areas
- recommend human review paths
- support analyst notes
- maintain audit trails
- preserve source metadata
- help reduce detection latency

The intended value is not automated enforcement. The intended value is helping analysts identify, triage, and route high-signal issues more efficiently.

---

## Limitations and Future Work

Current limitations:

- SQLite is used for local demo persistence.
- Reddit and X integrations may use fallback demo signals when public API access is blocked, unavailable, or paid.
- AI classification is assistive and requires human review.
- Regulatory outputs are review signals, not legal advice.
- The prototype does not include authentication or role-based access control.
- Demo seed data is synthetic and is not intended to represent real incidents.

Future improvements:

- migrate from SQLite to Postgres
- add user authentication and role-based permissions
- add richer source credibility scoring
- add duplicate incident clustering
- add SLA timers and queue ownership
- add exportable incident reports
- add production observability and metrics
- add policy taxonomy versioning
- add reviewer assignment and queue views
- add source deduplication and incident clustering

---

## Reviewer Notes

This project is intended as a portfolio prototype, not a production moderation system.

Key things to evaluate:

- end-to-end workflow completeness
- human-in-the-loop safety design
- fallback behavior when APIs fail
- auditability of analyst actions
- source metadata and verification logic
- clarity of escalation paths
- practical relevance to Trust & Safety operations

---

## Portfolio Positioning

Suggested framing:

> AI-assisted operational risk intelligence for emerging misuse and regulatory exposure. The system reduces detection latency and helps analysts focus on high-signal incidents while preserving human judgment for final review.

Resume bullet:

```text
Built a human-in-the-loop AI Safety Ops dashboard that ingests external risk signals, classifies incidents with AI assistance, supports analyst notes and escalation workflows, and maintains audit trails for defensible Trust & Safety operations.
```

Expanded resume bullet:

```text
Designed and built a full-stack AI risk intelligence platform for Trust & Safety workflows, integrating OpenAI-assisted triage, Reddit/X signal monitoring, regulatory source tracking, severity scoring, escalation routing, analyst notes, and audit logging.
```

---

## Suggested GitHub Repo Metadata

Recommended repo description:

```text
Human-in-the-loop AI Safety Ops dashboard for external risk signal monitoring, AI-assisted triage, escalation workflows, regulatory source tracking, and audit trails.
```

Recommended topics:

```text
trust-safety
ai-safety
risk-intelligence
fastapi
nextjs
openai-api
moderation
incident-response
regulatory-monitoring
human-in-the-loop
```

---

## Responsible Use Disclaimer

This prototype analyzes public content for demonstration purposes only. It should not be used to accuse individuals or groups of wrongdoing, make enforcement decisions, or conduct surveillance. Any production version would require privacy review, legal review, platform Terms of Service review, robust audit logging, and human oversight.
