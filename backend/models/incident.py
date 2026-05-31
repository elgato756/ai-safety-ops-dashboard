from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Incident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    source: str
    source_id: str
    source_url: Optional[str] = None
    source_community: Optional[str] = None

    source_type: Optional[str] = None
    verification_status: Optional[str] = None
    jurisdiction: Optional[str] = None
    authority: Optional[str] = None
    compliance_area: Optional[str] = None
    effective_date: Optional[str] = None

    title: str
    raw_content: Optional[str] = None

    is_relevant: bool = True
    category: str = "unknown"
    severity: int = 0
    confidence: float = 0.0
    evidence: Optional[str] = None
    missing_context: Optional[str] = None
    analyst_summary: str = ""
    suggested_next_steps: Optional[str] = None
    recommended_review_team: str = "triage"
    human_review_recommended: bool = False

    status: str = "open"
    analyst_notes: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
