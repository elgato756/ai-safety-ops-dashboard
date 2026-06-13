# AI Compliance Risk Intelligence Dashboard

A human-in-the-loop compliance risk intelligence dashboard for monitoring external AI risk signals, tracking regulatory developments, supporting issue triage, documenting review activity, and preserving audit-ready evidence.

This project does **not** make automated legal, regulatory, enforcement, account-level, or compliance decisions. It is an analyst-assist prototype intended to help compliance, risk, audit, legal, policy, and security teams identify, organize, prioritize, and route potential compliance signals for human review.

---

## Why This Project Matters

AI compliance teams need to monitor fast-moving regulatory expectations, policy developments, public risk signals, and operational issues that may create compliance exposure. These signals are often messy, fragmented across public channels, dependent on unreliable APIs, and difficult to convert into structured review work.

This project demonstrates a practical compliance risk-intelligence workflow for AI platforms. It combines external signal monitoring, regulatory source tracking, AI-assisted classification, issue triage, escalation routing, analyst notes, and audit logging into one operational dashboard.

The goal is not automated decision-making. The goal is to help compliance teams reduce detection latency, structure unorganized signals, preserve review evidence, and support defensible escalation decisions while keeping humans in control.

---

## Role Alignment

This project is designed to map to compliance, risk management, audit readiness, regulatory operations, issue management, and AI governance workflows.

It demonstrates experience with:

- regulatory and policy source monitoring
- AI governance and emerging regulatory risk tracking
- external signal ingestion and compliance issue triage
- risk categorization, severity scoring, and confidence scoring
- human-in-the-loop review workflows
- control-oriented escalation pathways
- analyst notes, issue history, and audit trails
- remediation and review status tracking
- graceful degradation when external systems fail
- cross-functional handoff patterns for Compliance, Legal, Policy, Security, Product, Engineering, and Audit teams

---

## Core Features

- Reddit signal ingestion with demo fallback behavior
- X / Twitter public signal monitoring with demo fallback behavior
- Regulatory and policy source monitoring
- AI-assisted compliance risk classification using the OpenAI API
- Safe fallback classification when model access is unavailable
- Severity and confidence scoring
- Recommended review team selection
- Analyst notes and issue lifecycle updates
- Escalation workflow with optional Slack webhook support
- Persistent local issue database using SQLite
- Audit trails for analyst actions and escalations
- Next.js dashboard frontend
- FastAPI backend

---

## Screenshots

### Main Dashboard

![Main dashboard](docs/screenshots/dashboard.png)

### Issue Detail Panel

![Issue detail panel](docs/screenshots/incident-detail.png)

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
2. Seed demo compliance issues.
3. Scan Reddit, X, or regulatory sources.
4. Open an issue detail panel.
5. Review AI summary, severity, confidence, and recommended review path.
6. Add analyst notes.
7. Escalate the issue.
8. Show the audit trail.

---

## Architecture

```text
ai-compliance-risk-dashboard/
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

Note: some backend model and service names still use `incident` because the prototype tracks compliance-relevant issues as incident records in the local database.

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

Seed demo issues:

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

The goal is to demonstrate the operational compliance workflow: signal ingestion, risk classification, analyst review, escalation, issue documentation, and auditability. External APIs improve realism, but the demo does not depend on every external service working perfectly.

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

The OpenAI API powers the AI-assisted compliance analysis layer of the dashboard.

It is used for:

- compliance risk classification
- analyst-facing summaries
- severity scoring
- confidence scoring
- recommended review team selection
- suggested next steps
- structured issue analysis
- control and policy review support

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
review team: compliance_triage
```

This fallback is intentional. In a real compliance environment, analyst workflows should not completely fail just because a model provider, API key, or quota configuration is temporarily unavailable. The system should degrade gracefully, preserve the incoming signal, and route it for human review.

---

### Reddit API

Reddit is used as a public signal source for identifying emerging AI-related discussions that may create compliance, governance, consumer protection, privacy, or platform risk exposure.

It can help monitor:

- AI-related Reddit communities
- emerging misuse or abuse discussions that may indicate control gaps
- jailbreak chatter and prompt injection discussions
- fraud, scam, or phishing enablement discussions
- public user concerns around AI behavior
- early signals that may warrant compliance or policy review

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

- monitoring public AI compliance and governance chatter
- identifying viral misuse signals that may create regulatory or reputational exposure
- tracking public reports of AI-enabled scams, phishing, impersonation, or deepfakes
- surfacing jailbreak and prompt injection discussions
- monitoring public conversation around AI regulation and policy developments
- collecting early warning signals that may require compliance, legal, policy, security, or product review

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
signal type: public_ai_compliance_chatter
status: reviewable_demo_signal
```

This fallback is intentional. Public social APIs can be paid, restricted, unstable, or unavailable depending on account access and API plan. In a real compliance monitoring workflow, one unavailable external source should not prevent the team from reviewing, documenting, and escalating other signals.

X / Twitter is treated as a monitoring lead source, not a source of verified truth. Signals from X should be reviewed by a human analyst and, when necessary, verified against authoritative sources before being used for compliance conclusions or operational action.

---

### Slack Webhook

Slack is used to simulate escalation into an internal compliance response workflow.

It can support:

- high-severity issue alerts
- routing to compliance, legal, policy, security, privacy, or product teams
- operational response workflows
- analyst-to-team handoff
- issue visibility for stakeholders
- remediation coordination

Optional configuration in `backend/.env`:

```text
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

Current behavior:

- If `SLACK_WEBHOOK_URL` is present, escalation actions can send Slack alerts.
- If it is blank, the app still works.
- Escalation status and audit events are still recorded locally even without Slack.

This makes the Slack integration optional while preserving the core workflow. The demo can still show that an issue was escalated, recorded, and added to the audit trail.

---

### Regulatory and Policy Sources

The regulatory scanner monitors official policy-source references and turns them into reviewable compliance signals.

It is intended to help compliance, legal, policy, audit, and AI governance teams track developments from authoritative sources.

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

Regulatory outputs are intended for legal, compliance, and policy review. The system does not provide legal advice, make compliance decisions, or automatically interpret law into operational obligations.

---

### Demo Seed and Reset Endpoints

The backend includes demo endpoints so the dashboard can be populated quickly for presentations.

Useful backend endpoints:

```text
POST /demo/seed
POST /demo/reset
```

`POST /demo/seed` creates realistic test issues across:

- AI governance monitoring
- EU AI Act regulatory tracking
- NIST AI RMF alignment review
- FTC-style consumer protection risk
- AI phishing and impersonation risk
- deepfake fraud risk
- prompt injection and model misuse risk
- privacy and data exposure risk
- regulatory or policy change monitoring

`POST /demo/reset` clears local issues and audit events.

These endpoints are useful for portfolio demos because they let reviewers see the full workflow without depending on live external APIs.

The seed data is not meant to represent real incidents or legal conclusions. It is designed to demonstrate how the system handles different categories of compliance risk, severity, confidence, escalation, analyst notes, and audit logging.

---

### Escalation Threshold

The backend can recommend escalation when an issue reaches a configured severity threshold.

Configure it in `backend/.env`:

```text
ESCALATION_SEVERITY_THRESHOLD=8
```

Default:

```text
8
```

Issues at or above this severity can trigger escalation recommendations and audit events.

This simulates how an internal compliance or risk operations team might define thresholds for legal review, policy review, privacy review, security review, executive visibility, or remediation governance.

---

## Compliance Risk Taxonomy

Current prototype categories include:

- AI governance risk
- regulatory monitoring
- policy compliance risk
- consumer protection risk
- privacy or data exposure
- security or prompt injection risk
- fraud, scam, or impersonation risk
- deepfake or synthetic media risk
- model misuse risk
- third-party or public-signal risk
- reputational risk
- unknown or low relevance

---

## Demo Resilience

The system is intentionally designed to degrade gracefully.

| Dependency | If unavailable |
|---|---|
| OpenAI API | Uses `needs_review` fallback classification |
| Reddit | Uses demo Reddit compliance signals |
| X / Twitter | Uses demo X compliance signals |
| Slack | Records escalation locally without sending a Slack message |
| Regulatory page scraping | Uses curated official-source fallback records |

This keeps the demo reliable while still showing how production integrations would work.

The fallback behavior is part of the product design, not just a workaround. In compliance and operational risk tooling, brittle dependencies can cause missed signals, incomplete documentation, or weak audit trails. This prototype preserves the signal and routes it for human review even when an integration fails.

---

## Human-in-the-Loop Positioning

This project is an analyst-assist compliance prototype.

It does not:

- make automated legal decisions
- make automated compliance determinations
- make account-level moderation decisions
- replace compliance, legal, policy, audit, or risk professionals
- turn regulatory text into binding obligations without review

It does:

- aggregate emerging compliance-relevant signals
- structure messy information
- classify potential risk areas
- recommend human review paths
- support analyst notes
- maintain audit trails
- preserve source metadata
- support escalation and remediation workflows
- help reduce detection latency

The intended value is not automated compliance decision-making. The intended value is helping teams identify, triage, document, and route high-signal issues more efficiently while preserving human judgment and auditability.

---

## Limitations and Future Work

Current limitations:

- SQLite is used for local demo persistence.
- Reddit and X integrations may use fallback demo signals when public API access is blocked, unavailable, or paid.
- AI classification is assistive and requires human review.
- Regulatory outputs are review signals, not legal advice.
- The prototype does not include authentication or role-based access control.
- Demo seed data is synthetic and is not intended to represent real incidents, obligations, or compliance findings.

Future improvements:

- migrate from SQLite to Postgres
- add user authentication and role-based permissions
- add richer source credibility scoring
- add duplicate issue clustering
- add SLA timers and issue ownership
- add exportable issue and audit reports
- add production observability and metrics
- add compliance taxonomy versioning
- add reviewer assignment and queue views
- add control mapping to frameworks such as NIST AI RMF, ISO 27001, SOC 2, SOX, or internal policy standards
- add remediation tracking and management action plan status
- add evidence export for audit or regulator-facing review packages

---

## Reviewer Notes

This project is intended as a portfolio prototype, not a production compliance system.

Key things to evaluate:

- end-to-end workflow completeness
- human-in-the-loop governance design
- fallback behavior when APIs fail
- auditability of analyst actions
- source metadata and verification logic
- clarity of escalation paths
- practical relevance to compliance, audit, and risk operations
- ability to translate unstructured external signals into reviewable issues

---

## Portfolio Positioning

Suggested framing:

> AI-assisted compliance risk intelligence for regulatory monitoring, public signal triage, issue escalation, and audit-ready documentation. The system reduces detection latency and helps compliance teams focus on high-signal issues while preserving human judgment for final review.

Resume bullet:

```text
Built a human-in-the-loop AI compliance risk dashboard that ingests external risk signals, classifies issues with AI assistance, supports analyst notes and escalation workflows, and maintains audit trails for defensible compliance review.
```

Expanded resume bullet:

```text
Designed and built a full-stack AI compliance risk intelligence platform integrating OpenAI-assisted triage, Reddit/X signal monitoring, regulatory source tracking, severity scoring, escalation routing, analyst notes, and audit logging to support compliance monitoring and audit readiness.
```

---

## Suggested GitHub Repo Metadata

Recommended repo description:

```text
Human-in-the-loop AI compliance risk dashboard for regulatory monitoring, external signal triage, escalation workflows, issue documentation, and audit trails.
```

Recommended topics:

```text
compliance
ai-governance
risk-intelligence
regulatory-monitoring
audit-readiness
fastapi
nextjs
openai-api
issue-management
human-in-the-loop
```

---

## Responsible Use Disclaimer

This prototype analyzes public content and official-source references for demonstration purposes only. It should not be used to accuse individuals or groups of wrongdoing, make legal or compliance decisions, conduct surveillance, or produce binding regulatory interpretations. Any production version would require privacy review, legal review, platform Terms of Service review, model governance controls, robust audit logging, access controls, and human oversight.
