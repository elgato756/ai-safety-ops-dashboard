from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session

from ai.classifier import classify_content
from db.database import create_db_and_tables, get_session
from ingestion.reddit_ingest import fetch_reddit_posts
from models.incident import Incident
from services.incident_service import (
    create_incident_from_reddit_post,
    list_incidents,
    update_incident_status,
)
from services.slack_service import send_slack_alert

app = FastAPI(title="AI Risk Intelligence Platform")

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


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "running"}


@app.post("/scan/reddit")
def scan_reddit(session: Session = Depends(get_session)) -> dict[str, object]:
    posts = fetch_reddit_posts(limit=5)
    created_incidents: list[Incident] = []

    for post in posts:
        analysis = classify_content(title=post["title"], body=post.get("body", ""))

        incident = create_incident_from_reddit_post(
            session=session,
            post=post,
            analysis=analysis,
        )

        if incident:
            created_incidents.append(incident)

            if incident.human_review_recommended or incident.severity >= 8:
                send_slack_alert(incident)

    return {"created": len(created_incidents), "incidents": created_incidents}


@app.get("/incidents", response_model=list[Incident])
def get_incidents(session: Session = Depends(get_session)) -> list[Incident]:
    return list_incidents(session)


@app.patch("/incidents/{incident_id}", response_model=Incident)
def patch_incident(
    incident_id: int,
    payload: IncidentUpdate,
    session: Session = Depends(get_session),
) -> Incident:
    incident = update_incident_status(
        session=session,
        incident_id=incident_id,
        status=payload.status,
        analyst_notes=payload.analyst_notes,
    )

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@app.post("/incidents/{incident_id}/escalate")
def escalate_incident(
    incident_id: int,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    incident = session.get(Incident, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    result = send_slack_alert(incident)
    update_incident_status(session=session, incident_id=incident_id, status="escalated")

    return result
