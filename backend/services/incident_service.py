from datetime import datetime
from typing import Any, Optional

from sqlmodel import Session, select

from models.incident import Incident


def incident_exists(session: Session, source: str, source_id: str) -> bool:
    statement = select(Incident).where(
        Incident.source == source,
        Incident.source_id == source_id,
    )
    return session.exec(statement).first() is not None


def _normalize_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "is_relevant": bool(analysis.get("is_relevant", True)),
        "category": str(analysis.get("category", "unknown")),
        "severity": max(0, min(10, int(analysis.get("severity", 0) or 0))),
        "confidence": max(0.0, min(1.0, float(analysis.get("confidence", 0.0) or 0.0))),
        "evidence": str(analysis.get("evidence", "")),
        "missing_context": str(analysis.get("missing_context", "")),
        "human_review_recommended": bool(analysis.get("human_review_recommended", False)),
        "recommended_review_team": str(analysis.get("recommended_review_team", "triage")),
        "analyst_summary": str(analysis.get("analyst_summary", "")),
        "suggested_next_steps": str(analysis.get("suggested_next_steps", "")),
    }


def create_incident_from_reddit_post(
    session: Session,
    post: dict[str, Any],
    analysis: dict[str, Any],
) -> Optional[Incident]:
    if incident_exists(session, "reddit", post["id"]):
        return None

    parsed = _normalize_analysis(analysis)

    incident = Incident(
        source="reddit",
        source_id=post["id"],
        source_url=post.get("url"),
        source_community=post.get("subreddit"),
        title=post["title"],
        raw_content=post.get("body"),
        **parsed,
    )

    session.add(incident)
    session.commit()
    session.refresh(incident)

    return incident


def list_incidents(session: Session) -> list[Incident]:
    statement = select(Incident).order_by(Incident.created_at.desc())
    return list(session.exec(statement).all())


def update_incident_status(
    session: Session,
    incident_id: int,
    status: str,
    analyst_notes: Optional[str] = None,
) -> Optional[Incident]:
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
