from typing import Optional

from pydantic import BaseModel, Field

VALID_STATUSES = ["submitted", "pending", "action_required", "completed", "rejected"]


class CreateRequestPayload(BaseModel):
    customer_id: str = Field(..., min_length=1)
    customer_name: Optional[str] = None
    request_type: str = Field(..., min_length=1)
    notes: Optional[str] = None


class UpdateStatusPayload(BaseModel):
    status: str
    notes: Optional[str] = None


class RequestRecord(BaseModel):
    request_id: str
    customer_id: str
    customer_name: Optional[str] = None
    request_type: str
    status: str
    submitted_at: str
    updated_at: str
    notes: Optional[str] = None
    receipt_number: str
