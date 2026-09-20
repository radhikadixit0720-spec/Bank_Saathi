"""
Status + Digital Receipt Vault service.

Only the minimum necessary information is stored per request: an id,
customer identifier, request type, status, timestamps, optional notes and
a receipt/reference number. No sensitive banking details (account
numbers, documents, balances, etc.) are persisted here.
"""
from typing import Dict, List, Optional

from backend.database.mongo import get_collection
from backend.schemas.requests import VALID_STATUSES
from backend.utils.ids import new_receipt_number, new_request_id, utc_now_iso

COLLECTION_NAME = "requests"


async def create_request(customer_id: str, customer_name: Optional[str], request_type: str, notes: Optional[str]) -> Dict:
    now = utc_now_iso()
    record = {
        "request_id": new_request_id(),
        "customer_id": customer_id,
        "customer_name": customer_name,
        "request_type": request_type,
        "status": "submitted",
        "submitted_at": now,
        "updated_at": now,
        "notes": notes,
        "receipt_number": new_receipt_number(),
    }
    await get_collection(COLLECTION_NAME).insert_one(record)
    return record


async def get_request(request_id: str) -> Optional[Dict]:
    return await get_collection(COLLECTION_NAME).find_one({"request_id": request_id})


async def get_customer_requests(customer_id: str) -> List[Dict]:
    cursor = get_collection(COLLECTION_NAME).find({"customer_id": customer_id}).sort("submitted_at", -1)
    return await cursor.to_list(length=200)


async def list_all_requests() -> List[Dict]:
    cursor = get_collection(COLLECTION_NAME).find({}).sort("submitted_at", -1)
    return await cursor.to_list(length=500)


async def update_request_status(request_id: str, status: str, notes: Optional[str] = None) -> Optional[Dict]:
    if status not in VALID_STATUSES:
        return None
    existing = await get_request(request_id)
    if not existing:
        return None

    update_fields = {"status": status, "updated_at": utc_now_iso()}
    if notes is not None:
        update_fields["notes"] = notes

    await get_collection(COLLECTION_NAME).update_one(
        {"request_id": request_id}, {"$set": update_fields}
    )
    existing.update(update_fields)
    return existing
