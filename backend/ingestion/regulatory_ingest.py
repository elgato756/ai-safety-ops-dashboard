import re
from datetime import datetime

import requests


OFFICIAL_POLICY_SOURCES = [
    {
        "id": "official_nist_ai_rmf_live",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "source_community": "NIST AI Risk Management Framework",
        "jurisdiction": "US",
        "authority": "NIST",
        "compliance_area": "ai_risk_management_governance",
        "title": "NIST AI Risk Management Framework official source monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
    },
    {
        "id": "official_eu_ai_act_timeline_live",
        "url": "https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act",
        "source_community": "European Commission AI Act Service Desk",
        "jurisdiction": "EU",
        "authority": "European Commission",
        "compliance_area": "governance_transparency_risk_management",
        "title": "EU AI Act implementation timeline official source monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
    },
    {
        "id": "official_eurlex_ai_act_text_live",
        "url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
        "source_community": "EUR-Lex Official Journal",
        "jurisdiction": "EU",
        "authority": "European Union",
        "compliance_area": "ai_act_legal_text",
        "title": "EU Artificial Intelligence Act official legal text monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
    },
]


OFFICIAL_FALLBACK_SIGNALS = [
    {
        "id": "official_eu_ai_act_timeline_001",
        "source": "regulatory_monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "EU",
        "authority": "European Commission",
        "compliance_area": "governance_transparency_risk_management",
        "effective_date": "2025-08-02",
        "source_community": "European Commission AI Act Service Desk",
        "title": "EU AI Act implementation timeline includes obligations for general-purpose AI models",
        "body": (
            "Official European Commission AI Act materials describe a phased implementation timeline. "
            "Relevant Trust & Safety review areas may include transparency, risk management, documentation, "
            "governance, and obligations for general-purpose AI model providers. This signal should be reviewed "
            "by policy/legal teams against the latest official EU AI Act materials before any operational change."
        ),
        "url": "https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act",
        "score": 100,
    },
    {
        "id": "official_nist_ai_rmf_001",
        "source": "regulatory_monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "US",
        "authority": "NIST",
        "compliance_area": "ai_risk_management_governance",
        "effective_date": None,
        "source_community": "NIST AI Risk Management Framework",
        "title": "NIST AI Risk Management Framework highlights governance, measurement, and risk management practices",
        "body": (
            "Official NIST AI RMF materials provide guidance for mapping, measuring, managing, and governing AI risks. "
            "This is not an enforcement action, but it is relevant to internal risk governance, documentation, "
            "evaluation, monitoring, and safety operations practices."
        ),
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "score": 95,
    },
    {
        "id": "official_eurlex_ai_act_001",
        "source": "regulatory_monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "EU",
        "authority": "European Union",
        "compliance_area": "ai_act_legal_text",
        "effective_date": None,
        "source_community": "EUR-Lex Official Journal",
        "title": "Official EU Artificial Intelligence Act legal text should be monitored for policy mapping",
        "body": (
            "EUR-Lex hosts the official text of Regulation (EU) 2024/1689, the Artificial Intelligence Act. "
            "This should be treated as a source-of-truth reference for legal/policy review rather than interpreted "
            "automatically by the system."
        ),
        "url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
        "score": 100,
    },
]


def _clean_html(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_relevant_excerpt(text: str, keywords: list[str], max_chars: int = 1800) -> str:
    lowered = text.lower()

    for keyword in keywords:
        idx = lowered.find(keyword.lower())
        if idx != -1:
            start = max(0, idx - 500)
            end = min(len(text), idx + max_chars)
            return text[start:end]

    return text[:max_chars]


def _fetch_official_source(source: dict) -> dict | None:
    headers = {
        "User-Agent": "ai-safety-ops-dashboard/0.1 official-policy-monitor"
    }

    try:
        response = requests.get(source["url"], headers=headers, timeout=15)
        response.raise_for_status()
        text = _clean_html(response.text)

        excerpt = _extract_relevant_excerpt(
            text,
            keywords=[
                "artificial intelligence",
                "AI Risk Management Framework",
                "general-purpose AI",
                "obligations",
                "timeline",
                "risk management",
                "Regulation",
            ],
        )

        if not excerpt:
            return None

        return {
            "id": f'{source["id"]}_{datetime.utcnow().strftime("%Y%m%d")}',
            "source": "regulatory_monitor",
            "source_type": source["source_type"],
            "verification_status": source["verification_status"],
            "jurisdiction": source["jurisdiction"],
            "authority": source["authority"],
            "compliance_area": source["compliance_area"],
            "effective_date": None,
            "source_community": source["source_community"],
            "title": source["title"],
            "body": (
                "Official policy source fetched for monitoring. "
                "The following excerpt should be summarized for analyst review only; "
                "do not treat the model output as legal advice or a final compliance decision.\n\n"
                f"{excerpt}"
            ),
            "url": source["url"],
            "score": 100,
        }

    except Exception as error:
        print(f"Failed to fetch official policy source {source['url']}: {error}")
        return None


def fetch_regulatory_signals(limit=10, include_secondary=False):
    signals = []

    for source in OFFICIAL_POLICY_SOURCES:
        fetched = _fetch_official_source(source)
        if fetched:
            signals.append(fetched)

    if not signals:
        print("Official policy source fetch failed. Using official fallback regulatory signals.")
        signals = OFFICIAL_FALLBACK_SIGNALS.copy()

    return signals[:limit]
