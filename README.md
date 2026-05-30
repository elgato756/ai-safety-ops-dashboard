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
