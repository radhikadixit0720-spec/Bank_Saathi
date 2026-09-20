from fastapi import APIRouter, HTTPException

from backend.schemas.language import SimplifyRequest, SimplifyResponse
from backend.services import language_service
from backend.utils.errors import server_error

router = APIRouter(prefix="/api/language-assistant", tags=["Simple Language Assistant"])


@router.post("/simplify", response_model=SimplifyResponse)
def simplify(payload: SimplifyRequest):
    """Convert formal banking language into a short, simple explanation."""
    try:
        return language_service.simplify_text(payload.text, payload.lang)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "language-assistant/simplify")
