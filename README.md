# AI Risk Intelligence Platform

A human-in-the-loop Trust & Safety risk intelligence prototype designed to aggregate emerging signals, support triage, and recommend review paths.

This project does **not** make automated enforcement, legal, account-level, or policy decisions. It is an analyst-assist system intended to help operations teams identify, organize, prioritize, and escalate risk signals for human review.

## Why this project matters

Trust & Safety teams working on AI products need to identify new and complex safety, policy, and integrity challenges in a rapidly evolving landscape. This prototype demonstrates how OpenAI-powered workflows can help analysts:

- Aggregate public risk signals
- Classify possible safety, integrity, regulatory, and reputational risks
- Estimate severity and confidence
- Preserve analyst judgment through human-in-the-loop review
- Route incidents to appropriate review teams
- Maintain an auditable incident lifecycle

## MVP features

- Reddit signal ingestion
- AI-assisted risk classification
- Severity and confidence scoring
- Persistent incident database using SQLite
- Incident lifecycle statuses
- Analyst notes
- Optional Slack webhook escalation
- Next.js dashboard
- FastAPI backend

## Architecture

```text
ai-risk-intelligence-platform/
├── backend/
│   ├── main.py
│   ├── ai/
│   │   └── classifier.py
│   ├── db/
│   │   └── database.py
│   ├── ingestion/
│   │   └── reddit_ingest.py
│   ├── models/
│   │   └── incident.py
│   ├── services/
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
│   └── product_brief.md
├── .gitignore
└── README.md
```

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your API keys to `.env`:

```text
OPENAI_API_KEY=your_openai_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
SLACK_WEBHOOK_URL=optional_slack_webhook_url
```

Run the backend:

```bash
uvicorn main:app --reload
```

Open the API docs:

```text
http://localhost:8000/docs
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Suggested demo flow

1. Start the backend.
2. Start the frontend.
3. Click **Scan Reddit**.
4. Review generated incidents.
5. Mark one as triaged.
6. Escalate a high-severity incident.
7. Explain that the model assists analysts but does not make final decisions.

## Risk taxonomy

Current prototype categories include:

- jailbreak sharing
- prompt injection
- fraud or scam enablement
- coordinated abuse
- synthetic identity abuse
- malware or social engineering assistance
- regulatory risk
- reputational risk
- unknown or low relevance

## Portfolio positioning

Suggested framing:

> AI-assisted operational risk intelligence for emerging misuse and regulatory exposure. The system reduces detection latency and helps analysts focus on high-signal incidents while preserving human judgment for final review.

## Responsible use disclaimer

This prototype analyzes public content for demonstration purposes only. It should not be used to accuse individuals or groups of wrongdoing, make enforcement decisions, or conduct surveillance. Any production version would require privacy review, legal review, platform ToS review, robust audit logging, and human oversight.

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

### Demo Resilience

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

### Human-in-the-Loop Positioning

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

