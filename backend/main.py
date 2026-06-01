import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session

from ai.classifier import classify_content
from db.database import create_db_and_tables, get_session
from ingestion.reddit_ingest import fetch_reddit_posts
from ingestion.regulatory_ingest import fetch_regulatory_signals
from ingestion.x_ingest import fetch_x_signals
from models.audit_log import AuditLog
from models.incident import Incident
from services.demo_seed_service import seed_demo_incidents
from services.audit_service import (
    create_audit_event,
    list_audit_events,
    list_incident_audit_events,
)
from services.incident_service import (
    create_incident_from_reddit_post,
    create_incident_from_signal,
    list_incidents,
    update_incident_status,
)
from services.slack_service import send_slack_alert

load_dotenv()

app = FastAPI(title="AI Safety Ops Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentUpdate(BaseModel):
    status: str
    analyst_notes: str | None = None


def escalation_threshold() -> int:
    try:
        return int(os.getenv("ESCALATION_SEVERITY_THRESHOLD", "8"))
    except Exception:
        return 8


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "ai-safety-ops-dashboard",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-safety-ops-dashboard",
        "escalation_severity_threshold": escalation_threshold(),
    }


@app.post("/scan/reddit")
def scan_reddit(session: Session = Depends(get_session)):
    posts = fetch_reddit_posts(limit=5)
    created_incidents = []
    threshold = escalation_threshold()

    for post in posts:
        analysis = classify_content(
            title=post["title"],
            body=post.get("body", ""),
        )

        incident = create_incident_from_reddit_post(
            session=session,
            post=post,
            analysis=analysis,
        )

        if incident:
            created_incidents.append(incident)

            create_audit_event(
                session=session,
                incident_id=incident.id,
                action="incident_created",
                details="Created from Reddit scan.",
            )

            if incident.should_escalate or incident.severity >= threshold:
                send_slack_alert(incident)
                create_audit_event(
                    session=session,
                    incident_id=incident.id,
                    action="auto_escalation_recommended",
                    details=(
                        f"Incident met escalation criteria. "
                        f"Severity={incident.severity}, threshold={threshold}."
                    ),
                )

    return {
        "source": "reddit",
        "created": len(created_incidents),
        "incidents": created_incidents,
    }


@app.post("/scan/regulatory")
def scan_regulatory(session: Session = Depends(get_session)):
    signals = fetch_regulatory_signals(limit=10)
    created_incidents = []
    threshold = escalation_threshold()

    for signal in signals:
        analysis = classify_content(
            title=signal["title"],
            body=signal.get("body", ""),
        )

        incident = create_incident_from_signal(
            session=session,
            signal=signal,
            analysis=analysis,
        )

        if incident:
            created_incidents.append(incident)

            create_audit_event(
                session=session,
                incident_id=incident.id,
                action="incident_created",
                details="Created from regulatory scan.",
            )

            if incident.should_escalate or incident.severity >= threshold:
                send_slack_alert(incident)
                create_audit_event(
                    session=session,
                    incident_id=incident.id,
                    action="auto_escalation_recommended",
                    details=(
                        f"Regulatory signal met escalation criteria. "
                        f"Severity={incident.severity}, threshold={threshold}."
                    ),
                )

    return {
        "source": "regulatory_monitor",
        "created": len(created_incidents),
        "incidents": created_incidents,
    }


@app.post("/scan/x")
def scan_x(session: Session = Depends(get_session)):
    signals = fetch_x_signals(limit=10)
    created_incidents = []
    threshold = escalation_threshold()

    for signal in signals:
        analysis = classify_content(
            title=signal["title"],
            body=signal.get("body", ""),
        )

        incident = create_incident_from_signal(
            session=session,
            signal=signal,
            analysis=analysis,
        )

        if incident:
            created_incidents.append(incident)

            create_audit_event(
                session=session,
                incident_id=incident.id,
                action="incident_created",
                details="Created from X scan.",
            )

            if incident.should_escalate or incident.severity >= threshold:
                send_slack_alert(incident)
                create_audit_event(
                    session=session,
                    incident_id=incident.id,
                    action="auto_escalation_recommended",
                    details=(
                        f"X signal met escalation criteria. "
                        f"Severity={incident.severity}, threshold={threshold}."
                    ),
                )

    return {
        "source": "x",
        "created": len(created_incidents),
        "incidents": created_incidents,
    }


@app.get("/incidents", response_model=list[Incident])
def get_incidents(session: Session = Depends(get_session)):
    return list_incidents(session)


@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: int, session: Session = Depends(get_session)):
    incident = session.get(Incident, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@app.patch("/incidents/{incident_id}", response_model=Incident)
def patch_incident(
    incident_id: int,
    payload: IncidentUpdate,
    session: Session = Depends(get_session),
):
    existing = session.get(Incident, incident_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Incident not found")

    previous_status = existing.status

    incident = update_incident_status(
        session=session,
        incident_id=incident_id,
        status=payload.status,
        analyst_notes=payload.analyst_notes,
    )

    if previous_status != payload.status:
        create_audit_event(
            session=session,
            incident_id=incident_id,
            action="status_updated",
            details=f"Status changed from {previous_status} to {payload.status}.",
        )

    if payload.analyst_notes is not None:
        create_audit_event(
            session=session,
            incident_id=incident_id,
            action="analyst_notes_saved",
            details="Analyst notes were updated.",
        )

    return incident


@app.post("/incidents/{incident_id}/escalate")
def escalate_incident(
    incident_id: int,
    session: Session = Depends(get_session),
):
    incident = session.get(Incident, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    result = send_slack_alert(incident)

    previous_status = incident.status
    incident.status = "escalated"
    session.add(incident)
    session.commit()
    session.refresh(incident)

    create_audit_event(
        session=session,
        incident_id=incident_id,
        action="manual_escalation",
        details=f"Status changed from {previous_status} to escalated.",
    )

    return {
        "incident": incident,
        "slack": result,
    }



@app.post("/demo/seed")
def seed_demo_data(session: Session = Depends(get_session)):
    created = seed_demo_incidents(session)

    return {
        "created": len(created),
        "incidents": created,
    }


@app.post("/demo/reset")
def reset_demo_data(session: Session = Depends(get_session)):
    # Delete child audit rows first, then incidents.
    from sqlmodel import delete
    from models.audit_log import AuditLog

    session.exec(delete(AuditLog))
    session.exec(delete(Incident))
    session.commit()

    return {
        "status": "reset_complete",
        "message": "All local incidents and audit events were deleted.",
    }


@app.get("/audit", response_model=list[AuditLog])
def get_audit_events(session: Session = Depends(get_session)):
    return list_audit_events(session)


@app.get("/incidents/{incident_id}/audit", response_model=list[AuditLog])
def get_incident_audit_events(
    incident_id: int,
    session: Session = Depends(get_session),
):
    incident = session.get(Incident, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return list_incident_audit_events(session, incident_id)
