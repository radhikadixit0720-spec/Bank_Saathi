from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from backend.config.settings import settings
from backend.data.i18n import FORM_SCANNER_MESSAGES, pick
from backend.data.templates import get_template, list_templates
from backend.schemas.form_scanner import ManualScanRequest, ScanResult, TemplateSummary
from backend.services import form_scanner_service
from backend.utils.errors import bad_request, not_found, server_error
from backend.utils.ids import new_uuid

router = APIRouter(prefix="/api/form-scanner", tags=["Form Scanner"])


@router.get("/templates", response_model=list[TemplateSummary])
def get_templates(lang: str = Query(default="en")):
    """List available bank form templates the scanner can compare against."""
    return list_templates(lang)


@router.post("/scan", response_model=ScanResult)
async def scan_uploaded_form(
    template_id: str = Form(...),
    file: UploadFile = File(...),
    lang: str = Form(default="en"),
):
    """Upload a form (PDF/text/image) and compare its detected fields
    against the chosen bank form template."""
    try:
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        raw_bytes = await file.read()
        if len(raw_bytes) > max_bytes:
            raise bad_request(f"File is larger than the {settings.MAX_UPLOAD_SIZE_MB}MB limit.")
        if not raw_bytes:
            raise bad_request("Uploaded file is empty.")

        text, ocr_used, fallback_reason = form_scanner_service._extract_text_from_upload(
            file.filename, file.content_type, raw_bytes
        )

        if text is None:
            # No text could be extracted (e.g. an image with no OCR configured).
            # Return an honest, empty-ish result rather than fabricating matches.
            template = get_template(template_id, lang)
            if not template:
                raise not_found(f"Unknown template_id '{template_id}'.")

            fields = [{
                "field_id": f["field_id"],
                "label": f["label"],
                "required": f["required"],
                "status": "needs_attention",
                "detected_value": None,
                "message": pick(FORM_SCANNER_MESSAGES["could_not_check"], lang),
            } for f in template["fields"]]

            return {
                "scan_id": new_uuid(),
                "template_id": template["template_id"],
                "template_name": template["name"],
                "source": "uploaded_file",
                "ocr_used": False,
                "fallback_reason": fallback_reason,
                "fields": fields,
                "matched_count": 0,
                "missing_count": len([f for f in template["fields"] if f["required"]]),
                "needs_attention_count": len([f for f in template["fields"] if not f["required"]]),
                "extra_fields": [],
                "overall_status": "incomplete",
            }

        result = form_scanner_service.scan_from_text(template_id, text, lang)
        if result is None:
            raise not_found(f"Unknown template_id '{template_id}'.")
        result["source"] = "uploaded_file"
        result["ocr_used"] = ocr_used
        result["fallback_reason"] = fallback_reason
        return result
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "form-scanner/scan")


@router.post("/scan-manual", response_model=ScanResult)
def scan_manual_values(payload: ManualScanRequest):
    """Compare typed/manual field values against a bank form template -
    the most reliable comparison path (no OCR involved at all)."""
    result = form_scanner_service.scan_from_values(payload.template_id, payload.values, payload.lang)
    if result is None:
        raise not_found(f"Unknown template_id '{payload.template_id}'.")
    result["source"] = "typed_values"
    result["ocr_used"] = False
    result["fallback_reason"] = None
    return result
