"""Small helpers for generating human-friendly, unique identifiers."""
import random
import string
import uuid
from datetime import datetime, timezone


def new_uuid() -> str:
    return str(uuid.uuid4())


def new_request_id() -> str:
    """e.g. REQ-20260919-4F82"""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"REQ-{stamp}-{suffix}"


def new_receipt_number() -> str:
    """e.g. BS-RCPT-839201"""
    suffix = "".join(random.choices(string.digits, k=6))
    return f"BS-RCPT-{suffix}"


def new_token_number(prefix: str, sequence: int) -> str:
    """e.g. B-104 (prefix from the service, sequence padded to 3 digits)"""
    return f"{prefix}-{sequence:03d}"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
