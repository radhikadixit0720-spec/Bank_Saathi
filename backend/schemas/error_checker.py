from typing import Dict, List, Optional

from pydantic import BaseModel


class ValidationError(BaseModel):
    field: str
    error_type: str
    message: str
    suggestion: str


class ErrorCheckRequest(BaseModel):
    values: Dict[str, str] = {}
    repeat_values: Optional[Dict[str, str]] = None  # e.g. {"email": "...", "email_confirm": "..."}
    consent_given: Optional[bool] = None
    signature_present: Optional[bool] = None
    required_fields: Optional[List[str]] = None
    # Optional: when provided, the result is stored so the Employee
    # Dashboard can surface these alerts against the matching request.
    customer_id: Optional[str] = None
    request_type: Optional[str] = None
    lang: str = "en"


class ErrorCheckResponse(BaseModel):
    is_valid: bool
    error_count: int
    errors: List[ValidationError]
