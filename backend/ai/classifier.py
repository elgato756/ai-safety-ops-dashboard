import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI-assisted risk intelligence system supporting a Trust & Safety operations team.

Your role is to help analysts review emerging signals more efficiently.

Do not make final enforcement, policy, legal, or account-level decisions.
Do not present unverified claims as facts.
Do not accuse specific users or organizations of wrongdoing.

Analyze the following content as a potential risk signal.

Determine:
1. Whether the content is relevant to AI safety, platform integrity, policy, abuse, or regulatory risk
2. The likely risk category
3. A severity estimate from 1-10
4. A confidence score from 0-1
5. What evidence supports the classification
6. What important context may be missing
7. Whether human review is recommended
8. Which team should review it, if any
9. A concise analyst-facing summary
10. Suggested next steps for investigation or monitoring

Return JSON with exactly these keys:
- is_relevant
- category
- severity
- confidence
- evidence
- missing_context
- human_review_recommended
- recommended_review_team
- analyst_summary
- suggested_next_steps
"""


def _fallback_result(error_message: str) -> dict[str, Any]:
    return {
        "is_relevant": False,
        "category": "classification_error",
        "severity": 0,
        "confidence": 0.0,
        "evidence": "Classifier failed before analysis completed.",
        "missing_context": error_message,
        "human_review_recommended": False,
        "recommended_review_team": "triage",
        "analyst_summary": "Classification could not be completed.",
        "suggested_next_steps": "Check API configuration and retry the scan.",
    }


def classify_content(title: str, body: str) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        return _fallback_result("Missing OPENAI_API_KEY in backend/.env.")

    content = f"TITLE: {title}\n\nBODY:\n{body or '[No body text provided]'}"

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content or "{}"
        return json.loads(raw)
    except Exception as exc:  # Keep MVP resilient during demos.
        return _fallback_result(str(exc))
