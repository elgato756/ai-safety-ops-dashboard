import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RiskAnalysis(BaseModel):
    is_relevant: bool = True
    category: str = "unknown"
    severity: int = Field(default=1, ge=1, le=10)
    confidence: float = Field(default=0.5, ge=0, le=1)
    evidence: list[str] = []
    missing_context: list[str] = []
    human_review_recommended: bool = True
    recommended_review_team: str = "trust_and_safety_triage"
    analyst_summary: str = ""
    suggested_next_steps: list[str] = []


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

Return JSON with:
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


def _safe_int(value: Any, default: int = 1) -> int:
    try:
        parsed = int(value)
        return max(1, min(10, parsed))
    except Exception:
        return default


def _safe_float(value: Any, default: float = 0.5) -> float:
    try:
        parsed = float(value)
        return max(0, min(1, parsed))
    except Exception:
        return default


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def classify_content(title: str, body: str):
    content = f"TITLE: {title}\n\nBODY:\n{body}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        response_format={"type": "json_object"},
    )

    raw_text = response.choices[0].message.content or "{}"

    try:
        raw = json.loads(raw_text)
    except Exception:
        raw = {}

    analysis = RiskAnalysis(
        is_relevant=bool(raw.get("is_relevant", True)),
        category=str(raw.get("category", "unknown")),
        severity=_safe_int(raw.get("severity", 1)),
        confidence=_safe_float(raw.get("confidence", 0.5)),
        evidence=_safe_list(raw.get("evidence", [])),
        missing_context=_safe_list(raw.get("missing_context", [])),
        human_review_recommended=bool(raw.get("human_review_recommended", True)),
        recommended_review_team=str(
            raw.get("recommended_review_team", raw.get("escalation_team", "trust_and_safety_triage"))
        ),
        analyst_summary=str(
            raw.get("analyst_summary", raw.get("summary", "Potential risk signal requiring analyst review."))
        ),
        suggested_next_steps=_safe_list(raw.get("suggested_next_steps", [])),
    )

    # Return a JSON string to preserve compatibility with the existing incident service.
    return json.dumps(analysis.dict())
