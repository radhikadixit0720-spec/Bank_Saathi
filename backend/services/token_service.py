"""
Branch Token / Appointment prototype service.

Generates a unique digital queue/token number per branch+service. This is
explicitly a prototype digital queue, not a real bank-issued token or a
connection to any core banking / branch system - every response says so,
in whichever of English / Hindi / Hinglish the user has selected.
"""
from typing import Dict, List, Optional

from backend.data.branches import get_branch, get_service
from backend.data.i18n import MISC, normalize_lang, pick
from backend.database.mongo import get_collection
from backend.utils.ids import new_token_number, new_uuid, utc_now_iso

COLLECTION_NAME = "tokens"


async def _next_sequence(branch_id: str, service_id: str) -> int:
    count = await get_collection(COLLECTION_NAME).count_documents(
        {"branch_id": branch_id, "service_id": service_id}
    )
    return count + 1


async def create_token(
    customer_id: str, customer_name: Optional[str], branch_id: str, service_id: str, lang: str = "en"
) -> Optional[Dict]:
    branch = get_branch(branch_id)
    service = get_service(service_id)
    if not branch or not service:
        return None

    sequence = await _next_sequence(branch_id, service_id)
    record = {
        "token_id": new_uuid(),
        "token_number": new_token_number(service["prefix"], sequence),
        "customer_id": customer_id,
        "customer_name": customer_name,
        "branch_id": branch_id,
        "branch_name": branch["name"],
        "service_id": service_id,
        "service_name": service["service_name"],
        "status": "waiting",
        "position_in_queue": sequence,
        "created_at": utc_now_iso(),
        "is_prototype": True,
        "disclaimer": pick(MISC["token_disclaimer"], lang),
    }
    await get_collection(COLLECTION_NAME).insert_one(record)
    return record


async def get_token(token_id: str) -> Optional[Dict]:
    return await get_collection(COLLECTION_NAME).find_one({"token_id": token_id})


async def get_customer_tokens(customer_id: str) -> List[Dict]:
    cursor = get_collection(COLLECTION_NAME).find({"customer_id": customer_id}).sort("created_at", -1)
    return await cursor.to_list(length=100)
