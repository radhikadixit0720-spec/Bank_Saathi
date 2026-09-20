from typing import List, Optional

from pydantic import BaseModel, Field


class TemplateSummary(BaseModel):
    template_id: str
    name: str
    field_count: int


class FieldResult(BaseModel):
    field_id: str
    label: str
    required: bool
    status: str  # "matched" | "missing" | "needs_attention" | "extra"
    detected_value: Optional[str] = None
    message: str


class ScanResult(BaseModel):
    scan_id: str
    template_id: str
    template_name: str
    source: str  # "uploaded_file" | "typed_values"
    ocr_used: bool
    fallback_reason: Optional[str] = None
    fields: List[FieldResult]
    matched_count: int
    missing_count: int
    needs_attention_count: int
    extra_fields: List[str] = Field(default_factory=list)
    overall_status: str  # "complete" | "incomplete"


class ManualScanRequest(BaseModel):
    template_id: str
    values: dict = Field(default_factory=dict)
    lang: str = "en"
