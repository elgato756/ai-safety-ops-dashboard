OFFICIAL_REGULATORY_SIGNALS = [
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
        "id": "official_ftc_ai_claims_001",
        "source": "regulatory_monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "US",
        "authority": "FTC",
        "compliance_area": "consumer_protection_marketing_claims_fraud",
        "effective_date": None,
        "source_community": "Federal Trade Commission",
        "title": "FTC materials indicate AI claims and consumer protection risks require careful review",
        "body": (
            "Official FTC materials are relevant to AI-related consumer protection, misleading claims, fraud, "
            "deceptive practices, privacy, and substantiation of product or safety claims. This signal should be "
            "reviewed by legal/policy teams before interpreting it as a specific compliance obligation."
        ),
        "url": "https://www.ftc.gov/",
        "score": 90,
    },
    {
        "id": "official_uk_aisi_001",
        "source": "regulatory_monitor",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "UK",
        "authority": "UK AI Security Institute",
        "compliance_area": "frontier_ai_safety_evaluation",
        "effective_date": None,
        "source_community": "UK AI Security Institute",
        "title": "UK AI Security Institute publications may inform frontier AI safety evaluation expectations",
        "body": (
            "Official UK AI Security Institute materials may be relevant to frontier AI safety research, evaluations, "
            "capability assessments, safeguards, and mitigations. This should be treated as a policy monitoring signal "
            "and reviewed by policy/safety teams."
        ),
        "url": "https://www.aisi.gov.uk/",
        "score": 85,
    },
]


SECONDARY_MONITORING_LEADS = [
    {
        "id": "secondary_state_ai_legislation_001",
        "source": "regulatory_monitor",
        "source_type": "secondary",
        "verification_status": "monitoring_lead_requires_verification",
        "jurisdiction": "US",
        "authority": "State-level AI policy monitoring",
        "compliance_area": "state_ai_legislation",
        "effective_date": None,
        "source_community": "Policy monitoring lead",
        "title": "State-level AI legislation chatter may indicate emerging compliance fragmentation",
        "body": (
            "Secondary monitoring suggests growing state-level attention to AI transparency, automated decision-making, "
            "privacy, and consumer protection. This is not treated as a confirmed obligation until reviewed against "
            "official state legislative or regulator sources."
        ),
        "url": "https://www.ncsl.org/technology-and-communication/artificial-intelligence-2025-legislation",
        "score": 60,
    }
]


def fetch_regulatory_signals(limit=10, include_secondary=True):
    signals = OFFICIAL_REGULATORY_SIGNALS.copy()

    if include_secondary:
        signals.extend(SECONDARY_MONITORING_LEADS)

    return signals[:limit]
