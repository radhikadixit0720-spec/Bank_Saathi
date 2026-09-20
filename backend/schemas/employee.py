from typing import List, Optional

from pydantic import BaseModel


class EmployeeRequestCard(BaseModel):
    request_id: str
    customer_id: str
    customer_name: Optional[str] = None
    request_type: str
    status: str
    submitted_at: str
    updated_at: str
    missing_documents: List[str] = []
    error_alerts: List[str] = []


class EmployeeDashboardResponse(BaseModel):
    total_requests: int
    pending_count: int
    completed_count: int
    action_required_count: int
    requests: List[EmployeeRequestCard]
