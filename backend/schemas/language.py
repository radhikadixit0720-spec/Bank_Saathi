from pydantic import BaseModel, Field


class SimplifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    lang: str = "en"


class SimplifyResponse(BaseModel):
    original_text: str
    simple_explanation: str
    method: str  # "ai_provider" | "rule_based_fallback"
    note: str = ""
