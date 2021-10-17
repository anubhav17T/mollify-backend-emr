from enum import Enum
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    therapy_plan = "THERAPY_PLAN"


class TherapyPlan(BaseModel):
    consultation_id: int = Field(..., description="UNIQUER IDENTIFIER FOR THE CONSULTATION")
    document_type: DocumentType = Field(..., description="TYPES OF DOCUMENT(QUESTIONS) W.R.T CLIENT")
    therapy_plan_html: str = Field(..., description="HTML STRING FOR THERAPY PLAN")
