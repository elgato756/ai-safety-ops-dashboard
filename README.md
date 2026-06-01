# AI Safety Ops Dashboard

A human-in-the-loop Trust & Safety operations prototype for identifying, triaging, and escalating emerging AI misuse, platform integrity, and regulatory risk signals.

This project demonstrates how OpenAI technology can support operational risk intelligence workflows without replacing human analysts. The system aggregates signals from source monitors, classifies potential risk areas, recommends review paths, supports analyst notes, and maintains an audit trail of actions.

## Why This Matters

Trust & Safety teams need to identify emerging risks quickly across messy external environments: social platforms, forums, regulatory sources, policy updates, and security research. This prototype shows how AI can reduce detection latency and help analysts prioritize high-signal incidents while preserving human review, auditability, and source verification.

## Core Capabilities

- Multi-source signal ingestion
- Reddit/X-style social risk monitoring with demo fallbacks
- Official regulatory/policy source monitoring
- NIST AI RMF and EU AI Act source references
- AI-assisted risk classification
- Severity and confidence scoring
- Human-in-the-loop analyst review
- Analyst notes
- Incident lifecycle management
- Escalation workflow simulation
- Audit trail logging
- Source verification metadata
- Demo seed/reset endpoints

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

## Human-in-the-Loop Design

This prototype is designed as an analyst-assist tool, not an automated enforcement system.

The dashboard helps Trust & Safety teams:

- aggregate emerging AI misuse and integrity signals
- classify potential risks for review
- prioritize incidents by severity and confidence
- recommend appropriate review teams
- support escalation workflows

The system does not make final enforcement, account-level, policy, or legal decisions. Its purpose is to reduce detection latency and help human analysts focus on the highest-signal incidents.

## Demo Features

- Reddit signal ingestion with demo fallback data
- AI-assisted risk classification
- severity and confidence scoring
- incident lifecycle states
- escalation workflow simulation
- dashboard filtering by risk type and status
- local SQLite persistence


---

## Demo Script

A suggested demo flow:

1. Start the backend and frontend.
2. Open the dashboard at `http://localhost:3000`.
3. Click **Scan Regulatory** to ingest official policy-source monitoring signals.
4. Click **Scan Reddit** or **Scan X** to ingest social risk signals or demo fallbacks.
5. Select an incident card.
6. Review:
   - source
   - category
   - severity
   - confidence
   - analyst summary
   - source content
   - verification status
7. Add analyst notes.
8. Mark the incident as triaged or escalated.
9. Review the audit trail to show traceability.

Key message:

> The system does not make enforcement or legal decisions. It assists human analysts by aggregating signals, structuring evidence, recommending review paths, and preserving an audit trail.


---

## Screenshots

### Main Dashboard

![Main dashboard](docs/screenshots/dashboard.png)

### Incident Detail Panel

![Incident detail panel](docs/screenshots/incident-detail.png)

### Audit Trail

![Audit trail](docs/screenshots/audit-trail.png)

