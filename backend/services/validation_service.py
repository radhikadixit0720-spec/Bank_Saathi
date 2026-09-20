"""
Error Checker service.

All validation happens here on the server - the frontend may mirror some
of these checks for instant feedback, but the backend is the source of
truth and is what actually gets called before a request is accepted.
Every message is available in English, Hindi, and Hinglish (see
backend/data/i18n.py for the shared templates).
"""
import re
from datetime import datetime
from typing import Dict, List, Optional

from backend.data.i18n import VALIDATION_MESSAGES, normalize_lang, pick

ACCOUNT_NUMBER_RE = re.compile(r"^\d{9,18}$")
PHONE_RE = re.compile(r"^[6-9]\d{9}$")  # common Indian mobile number pattern
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PAN_RE = re.compile(r"^[A-Z]{5}\d{4}[A-Z]$")

FIELD_LABELS = {
    "account_number": {"en": "Account Number", "hi": "खाता संख्या", "hinglish": "Account number"},
    "phone": {"en": "Phone Number", "hi": "फ़ोन नंबर", "hinglish": "Phone number"},
    "mobile_number": {"en": "Phone Number", "hi": "फ़ोन नंबर", "hinglish": "Phone number"},
    "email": {"en": "Email Address", "hi": "ईमेल पता", "hinglish": "Email address"},
    "pan_number": {"en": "PAN Number", "hi": "पैन नंबर", "hinglish": "PAN number"},
    "date_of_birth": {"en": "Date of Birth", "hi": "जन्म तिथि", "hinglish": "Date of Birth"},
}


def _label(field: str, lang: str) -> str:
    if field in FIELD_LABELS:
        return pick(FIELD_LABELS[field], lang)
    return field.replace("_", " ").title()


def _msg(key: str, lang: str, **kwargs) -> str:
    return pick(VALIDATION_MESSAGES[key], lang).format(**kwargs)


def _looks_like_date(value: str) -> bool:
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d %b %Y"):
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False


def check_form(
    values: Dict[str, str],
    repeat_values: Optional[Dict[str, str]] = None,
    consent_given: Optional[bool] = None,
    signature_present: Optional[bool] = None,
    required_fields: Optional[List[str]] = None,
    lang: str = "en",
) -> List[Dict]:
    lang = normalize_lang(lang)
    errors: List[Dict] = []
    values = values or {}

    # 1. Required fields left blank
    for field in (required_fields or []):
        if not (values.get(field) or "").strip():
            errors.append({
                "field": field,
                "error_type": "required_field_blank",
                "message": _msg("required_field_blank", lang, field=_label(field, lang)),
                "suggestion": _msg("required_field_blank_suggestion", lang, field=_label(field, lang)),
            })

    # 2. Invalid account number length/format
    account_number = values.get("account_number")
    if account_number and not ACCOUNT_NUMBER_RE.match(account_number.strip()):
        errors.append({
            "field": "account_number",
            "error_type": "invalid_format",
            "message": _msg("account_number_invalid", lang),
            "suggestion": _msg("account_number_invalid_suggestion", lang),
        })

    # 3. Invalid phone number
    for phone_field in ("phone", "mobile_number"):
        phone = values.get(phone_field)
        if phone and not PHONE_RE.match(phone.strip()):
            errors.append({
                "field": phone_field,
                "error_type": "invalid_format",
                "message": _msg("phone_invalid", lang),
                "suggestion": _msg("phone_invalid_suggestion", lang),
            })

    # 4. Invalid email
    email = values.get("email")
    if email and not EMAIL_RE.match(email.strip()):
        errors.append({
            "field": "email",
            "error_type": "invalid_format",
            "message": _msg("email_invalid", lang),
            "suggestion": _msg("email_invalid_suggestion", lang),
        })

    # 5. Invalid PAN-like format
    pan = values.get("pan_number")
    if pan and not PAN_RE.match(pan.strip().upper()):
        errors.append({
            "field": "pan_number",
            "error_type": "invalid_format",
            "message": _msg("pan_invalid", lang),
            "suggestion": _msg("pan_invalid_suggestion", lang),
        })

    # 6. Invalid date
    dob = values.get("date_of_birth")
    if dob and not _looks_like_date(dob.strip()):
        errors.append({
            "field": "date_of_birth",
            "error_type": "invalid_date",
            "message": _msg("date_invalid", lang),
            "suggestion": _msg("date_invalid_suggestion", lang),
        })

    # 7. Mismatch between repeated fields
    for field, confirm_value in (repeat_values or {}).items():
        original = values.get(field)
        if original is not None and confirm_value is not None and original.strip() != confirm_value.strip():
            errors.append({
                "field": field,
                "error_type": "field_mismatch",
                "message": _msg("field_mismatch", lang, field=_label(field, lang)),
                "suggestion": _msg("field_mismatch_suggestion", lang, field=_label(field, lang)),
            })

    # 8. Missing consent
    if consent_given is False:
        errors.append({
            "field": "consent",
            "error_type": "missing_consent",
            "message": _msg("missing_consent", lang),
            "suggestion": _msg("missing_consent_suggestion", lang),
        })

    # 9. Missing signature
    if signature_present is False:
        errors.append({
            "field": "signature",
            "error_type": "missing_signature",
            "message": _msg("missing_signature", lang),
            "suggestion": _msg("missing_signature_suggestion", lang),
        })

    # 10. Generic obvious issues: whitespace-only values submitted as "filled"
    for field, value in values.items():
        if value is not None and value != "" and value.strip() == "":
            errors.append({
                "field": field,
                "error_type": "blank_whitespace",
                "message": _msg("blank_whitespace", lang, field=_label(field, lang)),
                "suggestion": _msg("blank_whitespace_suggestion", lang, field=_label(field, lang)),
            })

    return errors
