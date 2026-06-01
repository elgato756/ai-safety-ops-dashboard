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
    category: str = "needs_review"
    severity: int = Field(default=5, ge=1, le=10)
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

For regulatory analysis:
- Treat official government, regulator, standards-body, or legislative sources as the highest-confidence source type.
- Treat news, social media, blogs, commentary, or unclear sources only as monitoring leads.
- Do not invent legal obligations.
- Distinguish confirmed official-source information from items requiring legal or policy verification.
- Recommend human legal/policy review before any operational compliance decision.

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


def _safe_int(value: Any, default: int = 5) -> int:
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


def fallback_analysis(reason: str) -> str:
    fallback = RiskAnalysis(
        is_relevant=True,
        category="needs_review",
        severity=5,
        confidence=0.5,
        evidence=[
            "Signal was ingested successfully.",
            "Classifier fallback was used because AI classification could not complete.",
        ],
        missing_context=[
            reason,
            "Human review is required before any operational decision.",
        ],
        human_review_recommended=True,
        recommended_review_team="trust_and_safety_triage",
        analyst_summary=(
            "This signal was ingested successfully, but AI classification could not be completed. "
            "A human analyst should review the source content and backend configuration."
        ),
        suggested_next_steps=[
            "Review the raw source content manually.",
            "Check OPENAI_API_KEY and available API quota.",
            "Confirm whether this signal should be escalated.",
        ],
    )

    return json.dumps(fallback.dict())


def classify_content(title: str, body: str):
    content = f"TITLE: {title}\n\nBODY:\n{body}"

    if not os.getenv("OPENAI_API_KEY"):
        return fallback_analysis("OPENAI_API_KEY is missing from backend/.env.")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            response_format={"type": "json_object"},
        )

        raw_text = response.choices[0].message.content or "{}"
        raw = json.loads(raw_text)

        analysis = RiskAnalysis(
            is_relevant=bool(raw.get("is_relevant", True)),
            category=str(raw.get("category", "needs_review")),
            severity=_safe_int(raw.get("severity", 5)),
            confidence=_safe_float(raw.get("confidence", 0.5)),
            evidence=_safe_list(raw.get("evidence", [])),
            missing_context=_safe_list(raw.get("missing_context", [])),
            human_review_recommended=bool(raw.get("human_review_recommended", True)),
            recommended_review_team=str(
                raw.get("recommended_review_team", "trust_and_safety_triage")
            ),
            analyst_summary=str(
                raw.get(
                    "analyst_summary",
                    "Potential risk signal requiring analyst review.",
                )
            ),
            suggested_next_steps=_safe_list(raw.get("suggested_next_steps", [])),
        )

        return json.dumps(analysis.dict())

    except Exception as error:
        print(f"OpenAI classification failed. Using fallback analysis: {error}")
        return fallback_analysis(str(error))
