DEMO_REGULATORY_SIGNALS = [
    {
        "id": "reg_eu_ai_act_001",
        "source": "regulatory_monitor",
        "source_community": "EU AI Act",
        "title": "EU AI Act obligations may require additional transparency and risk documentation",
        "body": "A regulatory update indicates that providers of advanced AI systems may need stronger documentation, transparency, risk management, and post-market monitoring processes.",
        "url": "https://artificialintelligenceact.eu/",
        "score": 100,
    },
    {
        "id": "reg_ftc_ai_claims_001",
        "source": "regulatory_monitor",
        "source_community": "FTC",
        "title": "FTC scrutiny of misleading AI claims creates consumer protection risk",
        "body": "Recent enforcement patterns suggest companies should ensure AI capability claims, safety claims, and automated decision-making claims are accurate and substantiated.",
        "url": "https://www.ftc.gov/",
        "score": 90,
    },
    {
        "id": "reg_nist_ai_rmf_001",
        "source": "regulatory_monitor",
        "source_community": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework highlights governance and measurement expectations",
        "body": "Risk management guidance emphasizes mapping, measuring, managing, and governing AI risks across development and deployment lifecycles.",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "score": 85,
    },
]


def fetch_regulatory_signals(limit=10):
    return DEMO_REGULATORY_SIGNALS[:limit]
