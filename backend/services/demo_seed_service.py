from sqlmodel import Session

from models.incident import Incident
from services.audit_service import create_audit_event
from services.incident_service import incident_exists


DEMO_INCIDENTS = [
    {
        "source": "reddit",
        "source_id": "demo_jailbreak_cluster_001",
        "source_url": "https://www.reddit.com/r/ChatGPT/",
        "source_community": "ChatGPT",
        "source_type": "demo_fallback",
        "verification_status": "demo_signal",
        "title": "Emerging jailbreak prompt pattern spreading across AI forums",
        "raw_content": (
            "Multiple posts describe a reusable prompt chain that allegedly bypasses refusal behavior. "
            "The pattern appears to be spreading through comments and copy-paste templates."
        ),
        "category": "jailbreak_sharing",
        "severity": 8,
        "confidence": 0.82,
        "summary": (
            "Potential emerging jailbreak trend. Human review is recommended to determine whether this "
            "is a novel bypass pattern, reposted content, or harmless discussion."
        ),
        "escalation_team": "policy_and_abuse_operations",
        "should_escalate": True,
    },
    {
        "source": "x",
        "source_id": "demo_ai_phishing_001",
        "source_url": "https://x.com/",
        "source_community": "X / fraud monitoring",
        "source_type": "demo_fallback",
        "verification_status": "demo_signal",
        "title": "Social posts report AI-generated phishing kits targeting support workflows",
        "raw_content": (
            "A cluster of posts claims that attackers are using AI-generated scripts to imitate customer "
            "support agents and create more convincing credential theft flows."
        ),
        "category": "fraud_scam_enablement",
        "severity": 9,
        "confidence": 0.76,
        "summary": (
            "Possible fraud enablement trend involving AI-generated phishing content. Needs analyst review "
            "to validate source credibility and assess abuse pattern."
        ),
        "escalation_team": "fraud_and_abuse_prevention",
        "should_escalate": True,
    },
    {
        "source": "x",
        "source_id": "demo_deepfake_impersonation_001",
        "source_url": "https://x.com/",
        "source_community": "X / reputational monitoring",
        "source_type": "demo_fallback",
        "verification_status": "demo_signal",
        "title": "Reports of deepfake voice impersonation used in payment approval scams",
        "raw_content": (
            "Posts describe scammers using synthetic voice clips to impersonate executives and request "
            "urgent payment approvals from finance teams."
        ),
        "category": "deepfake_abuse",
        "severity": 8,
        "confidence": 0.71,
        "summary": (
            "Potential deepfake-enabled fraud signal. Recommend review by fraud, policy, and communications "
            "stakeholders if corroborated."
        ),
        "escalation_team": "fraud_policy_comms",
        "should_escalate": True,
    },
    {
        "source": "regulatory_monitor",
        "source_id": "demo_eu_ai_act_001",
        "source_url": "https://ai-act-service-desk.ec.europa.eu/",
        "source_community": "European Commission AI Act Service Desk",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "EU",
        "authority": "European Commission",
        "compliance_area": "governance_transparency_risk_management",
        "effective_date": "2025-08-02",
        "title": "EU AI Act timeline requires policy/legal review for GPAI obligations",
        "raw_content": (
            "Official EU AI Act implementation materials indicate phased obligations relevant to governance, "
            "transparency, documentation, and risk management for general-purpose AI model providers."
        ),
        "category": "regulatory_compliance",
        "severity": 7,
        "confidence": 0.93,
        "summary": (
            "Official-source regulatory signal. Recommend legal/policy review to map obligations against "
            "current operational controls and documentation practices."
        ),
        "escalation_team": "legal_policy_governance",
        "should_escalate": True,
    },
    {
        "source": "regulatory_monitor",
        "source_id": "demo_ftc_claims_001",
        "source_url": "https://www.ftc.gov/",
        "source_community": "Federal Trade Commission",
        "source_type": "official",
        "verification_status": "official_source_verified",
        "jurisdiction": "US",
        "authority": "FTC",
        "compliance_area": "consumer_protection_marketing_claims_fraud",
        "title": "FTC AI claims scrutiny creates review need for safety and capability messaging",
        "raw_content": (
            "Official FTC materials are relevant to misleading AI claims, fraud, deceptive practices, privacy, "
            "and substantiation of product or safety claims."
        ),
        "category": "regulatory_consumer_protection",
        "severity": 6,
        "confidence": 0.88,
        "summary": (
            "Official-source policy risk signal. Recommend legal and policy review of AI-related capability, "
            "safety, and reliability claims."
        ),
        "escalation_team": "legal_policy",
        "should_escalate": True,
    },
    {
        "source": "security_blog",
        "source_id": "demo_prompt_injection_001",
        "source_url": "https://example.com/security-research",
        "source_community": "Security research monitoring",
        "source_type": "secondary",
        "verification_status": "monitoring_lead_requires_verification",
        "title": "Researchers describe prompt injection pattern targeting AI agent browsing tools",
        "raw_content": (
            "A security writeup describes malicious webpages embedding hidden instructions intended to override "
            "AI agent behavior during browsing or tool-use workflows."
        ),
        "category": "prompt_injection",
        "severity": 8,
        "confidence": 0.79,
        "summary": (
            "Potential agent/tool-use security risk. Requires validation and possible escalation to security "
            "and product safety teams."
        ),
        "escalation_team": "security_product_safety",
        "should_escalate": True,
    },
    {
        "source": "news_monitor",
        "source_id": "demo_privacy_exposure_001",
        "source_url": "https://example.com/privacy-ai",
        "source_community": "Privacy news monitoring",
        "source_type": "secondary",
        "verification_status": "monitoring_lead_requires_verification",
        "title": "Reports raise concern about sensitive data exposure through AI assistant workflows",
        "raw_content": (
            "A secondary report claims employees may be pasting sensitive customer or business data into AI tools. "
            "Requires verification before treating as confirmed exposure."
        ),
        "category": "privacy_data_exposure",
        "severity": 7,
        "confidence": 0.64,
        "summary": (
            "Potential privacy/data handling risk. Recommend review by privacy, security, and policy teams "
            "before any operational action."
        ),
        "escalation_team": "privacy_security_policy",
        "should_escalate": True,
    },
]


def seed_demo_incidents(session: Session):
    created = []

    for item in DEMO_INCIDENTS:
        if incident_exists(session, item["source"], item["source_id"]):
            continue

        incident = Incident(
            source=item["source"],
            source_id=item["source_id"],
            source_url=item.get("source_url"),
            source_community=item.get("source_community"),
            source_type=item.get("source_type"),
            verification_status=item.get("verification_status"),
            jurisdiction=item.get("jurisdiction"),
            authority=item.get("authority"),
            compliance_area=item.get("compliance_area"),
            effective_date=item.get("effective_date"),
            title=item["title"],
            raw_content=item.get("raw_content"),
            category=item["category"],
            severity=item["severity"],
            confidence=item["confidence"],
            summary=item["summary"],
            escalation_team=item["escalation_team"],
            should_escalate=item["should_escalate"],
        )

        session.add(incident)
        session.commit()
        session.refresh(incident)

        create_audit_event(
            session=session,
            incident_id=incident.id,
            action="demo_incident_seeded",
            details="Created from demo seed data.",
        )

        if incident.should_escalate:
            create_audit_event(
                session=session,
                incident_id=incident.id,
                action="auto_escalation_recommended",
                details=(
                    f"Demo incident marked for review. "
                    f"Severity={incident.severity}, confidence={incident.confidence}."
                ),
            )

        created.append(incident)

    return created
