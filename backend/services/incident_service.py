import json
from datetime import datetime

from sqlmodel import Session, select

from models.incident import Incident


def incident_exists(session: Session, source: str, source_id: str) -> bool:
    statement = select(Incident).where(
        Incident.source == source,
        Incident.source_id == source_id,
    )
    return session.exec(statement).first() is not None


def _parse_analysis(analysis: str | dict):
    if isinstance(analysis, dict):
        return analysis

    try:
        return json.loads(analysis)
    except Exception:
        return {}


def create_incident_from_signal(session: Session, signal: dict, analysis: str | dict):
    parsed = _parse_analysis(analysis)

    source = signal.get("source", "reddit")
    source_id = signal.get("id")

    if not source_id:
        return None

    if incident_exists(session, source, source_id):
        return None

    incident = Incident(
        source=source,
        source_id=source_id,
        source_url=signal.get("url"),
        source_community=signal.get("subreddit") or signal.get("source_community"),

        source_type=signal.get("source_type"),
        verification_status=signal.get("verification_status"),
        jurisdiction=signal.get("jurisdiction"),
        authority=signal.get("authority"),
        compliance_area=signal.get("compliance_area"),
        effective_date=signal.get("effective_date"),

        title=signal.get("title", "Untitled signal"),
        raw_content=signal.get("body", ""),
        category=parsed.get("category", "unknown"),
        severity=int(parsed.get("severity", 1)),
        confidence=float(parsed.get("confidence", 0.5)),
        summary=parsed.get("analyst_summary") or parsed.get("summary", ""),
        escalation_team=(
            parsed.get("recommended_review_team")
            or parsed.get("escalation_team")
            or "trust_and_safety_triage"
        ),
        should_escalate=bool(
            parsed.get("human_review_recommended", parsed.get("should_escalate", True))
        ),
    )

    session.add(incident)
    session.commit()
    session.refresh(incident)

    return incident


def create_incident_from_reddit_post(session: Session, post: dict, analysis: str | dict):
    post = {**post, "source": "reddit"}
    return create_incident_from_signal(session, post, analysis)


def list_incidents(session: Session):
    statement = select(Incident).order_by(Incident.created_at.desc())
    return session.exec(statement).all()


def update_incident_status(
    session: Session,
    incident_id: int,
    status: str,
    analyst_notes: str | None = None,
):
    incident = session.get(Incident, incident_id)

    if not incident:
        return None

    incident.status = status
    incident.updated_at = datetime.utcnow()

    if analyst_notes is not None:
        incident.analyst_notes = analyst_notes

    session.add(incident)
    session.commit()
    session.refresh(incident)

    return incident
