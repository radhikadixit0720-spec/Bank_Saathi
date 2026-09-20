"""
Form Scanner + Template Matching service.

Real OCR (e.g. a cloud Document AI / Textract-style service) is NOT wired
up in this prototype, and the code below never pretends otherwise: when a
non-text file (an image or a scan) is uploaded, `ocr_used` is returned as
False along with a clear `fallback_reason`, and the frontend must display
that honestly.

What IS implemented for real:
  - PDFs and plain text files are actually parsed and their text is
    matched against the chosen bank form template's expected fields.
  - Typed/manual field values (e.g. from a web form) are matched exactly,
    which is the most reliable path and always fully "real".

The extraction step is isolated in `_extract_text_from_upload` so it can be
swapped for a production OCR provider (AWS Textract, Google Document AI,
Azure Form Recognizer, etc.) later without touching the matching logic.
"""
import io
import re
from typing import Dict, Optional, Tuple

from backend.data.i18n import FORM_SCANNER_MESSAGES, normalize_lang, pick
from backend.data.templates import get_template
from backend.utils.ids import new_uuid


def _extract_text_from_upload(filename: str, content_type: str, raw_bytes: bytes) -> Tuple[Optional[str], bool, Optional[str]]:
    """Returns (extracted_text, ocr_used, fallback_reason)."""
    filename_lower = (filename or "").lower()

    # Plain text files - genuinely parsed.
    if content_type in ("text/plain",) or filename_lower.endswith(".txt"):
        try:
            return raw_bytes.decode("utf-8", errors="ignore"), False, None
        except Exception:
            return None, False, "Could not decode the uploaded text file."

    # PDFs - real text extraction via pypdf, when the PDF has a text layer.
    if content_type == "application/pdf" or filename_lower.endswith(".pdf"):
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(raw_bytes))
            text = "\n".join((page.extract_text() or "") for page in reader.pages)
            if text.strip():
                return text, False, None
            return None, False, (
                "This PDF appears to be a scanned image with no selectable text, "
                "so field text could not be extracted. OCR is not configured in "
                "this prototype."
            )
        except ImportError:
            return None, False, "PDF parsing library is not installed on the server."
        except Exception:
            return None, False, "Could not read this PDF file."

    # Images and anything else - no OCR configured.
    return None, False, (
        "OCR is not configured in this prototype, so text could not be "
        "automatically read from this image. Configure a document/OCR "
        "provider (e.g. AWS Textract, Google Document AI, Azure Form "
        "Recognizer) in services/form_scanner_service.py to enable real "
        "scanning of photographed/scanned forms."
    )


def _field_status_from_text(text_lower: str, keywords) -> Optional[str]:
    for kw in keywords:
        if kw.lower() in text_lower:
            return "found"
    return None


def scan_from_text(template_id: str, text: str, lang: str = "en") -> Dict:
    """Match extracted free text against a template's expected fields."""
    template = get_template(template_id, lang)
    if not template:
        return None

    text_lower = text.lower()
    field_results = []
    matched = missing = attention = 0

    for field in template["fields"]:
        found = _field_status_from_text(text_lower, field["keywords"])
        if found:
            status = "matched"
            matched += 1
            message = pick(FORM_SCANNER_MESSAGES["detected_in_document"], lang).format(label=field["label"])
        elif field["required"]:
            status = "missing"
            missing += 1
            message = pick(FORM_SCANNER_MESSAGES["required_not_found"], lang).format(label=field["label"])
        else:
            status = "needs_attention"
            attention += 1
            message = pick(FORM_SCANNER_MESSAGES["optional_not_detected"], lang).format(label=field["label"])

        field_results.append({
            "field_id": field["field_id"],
            "label": field["label"],
            "required": field["required"],
            "status": status,
            "detected_value": None,
            "message": message,
        })

    return {
        "scan_id": new_uuid(),
        "template_id": template["template_id"],
        "template_name": template["name"],
        "fields": field_results,
        "matched_count": matched,
        "missing_count": missing,
        "needs_attention_count": attention,
        "extra_fields": [],
        "overall_status": "complete" if missing == 0 else "incomplete",
    }


def scan_from_values(template_id: str, values: Dict[str, str], lang: str = "en") -> Dict:
    """Match typed/manual field values against a template - the most
    reliable comparison path, useful once a user has confirmed/typed the
    fields detected from a scan, or when no file upload is available."""
    template = get_template(template_id, lang)
    if not template:
        return None

    known_ids = {f["field_id"] for f in template["fields"]}
    field_results = []
    matched = missing = attention = 0

    for field in template["fields"]:
        raw_value = (values.get(field["field_id"]) or "").strip()
        if raw_value:
            status = "matched"
            matched += 1
            message = pick(FORM_SCANNER_MESSAGES["looks_filled"], lang).format(label=field["label"])
        elif field["required"]:
            status = "missing"
            missing += 1
            message = pick(FORM_SCANNER_MESSAGES["required_empty"], lang).format(label=field["label"])
        else:
            status = "needs_attention"
            attention += 1
            message = pick(FORM_SCANNER_MESSAGES["optional_empty"], lang).format(label=field["label"])

        field_results.append({
            "field_id": field["field_id"],
            "label": field["label"],
            "required": field["required"],
            "status": status,
            "detected_value": raw_value or None,
            "message": message,
        })

    extra_fields = [k for k in values.keys() if k not in known_ids and values.get(k)]

    return {
        "scan_id": new_uuid(),
        "template_id": template["template_id"],
        "template_name": template["name"],
        "fields": field_results,
        "matched_count": matched,
        "missing_count": missing,
        "needs_attention_count": attention,
        "extra_fields": extra_fields,
        "overall_status": "complete" if missing == 0 else "incomplete",
    }
