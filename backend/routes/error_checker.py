from fastapi import APIRouter, HTTPException

from backend.schemas.error_checker import ErrorCheckRequest, ErrorCheckResponse
from backend.services import employee_service, validation_service
from backend.utils.errors import server_error

router = APIRouter(prefix="/api/error-checker", tags=["Error Checker"])


@router.post("/check", response_model=ErrorCheckResponse)
async def check_form(payload: ErrorCheckRequest):
    """Run server-side validation on submitted form values."""
    try:
        errors = validation_service.check_form(
            values=payload.values,
            repeat_values=payload.repeat_values,
            consent_given=payload.consent_given,
            signature_present=payload.signature_present,
            required_fields=payload.required_fields,
            lang=payload.lang,
        )

        if payload.customer_id and payload.request_type:
            await employee_service.record_error_check(payload.customer_id, payload.request_type, errors)

        return {
            "is_valid": len(errors) == 0,
            "error_count": len(errors),
            "errors": errors,
        }
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "error-checker/check")
