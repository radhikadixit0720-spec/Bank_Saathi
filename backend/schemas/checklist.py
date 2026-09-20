from typing import Dict, List, Optional

from pydantic import BaseModel


class ChecklistDocument(BaseModel):
    doc_id: str
    label: str
    required: bool
    status: str = "missing"  # "available" | "missing" | "not_applicable"


class ChecklistResponse(BaseModel):
    service_id: str
    service_name: str
    documents: List[ChecklistDocument]
    remaining_required: int
    summary: str


class ChecklistStatusUpdate(BaseModel):
    statuses: Dict[str, str]  # doc_id -> "available" | "missing" | "not_applicable"
    customer_id: Optional[str] = "guest"
