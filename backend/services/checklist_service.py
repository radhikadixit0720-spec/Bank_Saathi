"""Document Checklist service."""
from typing import Dict, Optional

from backend.data.checklists import get_checklist
from backend.data.i18n import MISC, normalize_lang, pick
from backend.database.mongo import get_collection

COLLECTION_NAME = "checklist_status"


def _build_response(service: Dict, statuses: Dict[str, str], lang: str = "en") -> Dict:
    documents = []
    remaining_required = 0
    for doc in service["documents"]:
        status = statuses.get(doc["doc_id"], "missing")
        if doc["required"] and status != "available":
            remaining_required += 1
        documents.append({
            "doc_id": doc["doc_id"],
            "label": doc["label"],
            "required": doc["required"],
            "status": status,
        })

    summary = (
        pick(MISC["checklist_all_ready"], lang)
        if remaining_required == 0
        else pick(MISC["checklist_remaining"], lang).format(count=remaining_required)
    )

    return {
        "service_id": service["service_id"],
        "service_name": service["service_name"],
        "documents": documents,
        "remaining_required": remaining_required,
        "summary": summary,
    }


async def get_checklist_for_customer(service_id: str, customer_id: Optional[str] = "guest", lang: str = "en") -> Optional[Dict]:
    service = get_checklist(service_id, lang)
    if not service:
        return None

    record = await get_collection(COLLECTION_NAME).find_one(
        {"service_id": service_id, "customer_id": customer_id}
    )
    statuses = record["statuses"] if record else {}
    return _build_response(service, statuses, lang)


async def update_checklist_status(service_id: str, customer_id: str, statuses: Dict[str, str], lang: str = "en") -> Optional[Dict]:
    service = get_checklist(service_id, lang)
    if not service:
        return None

    valid_doc_ids = {d["doc_id"] for d in service["documents"]}
    valid_statuses = {"available", "missing", "not_applicable"}
    clean_statuses = {
        k: v for k, v in statuses.items() if k in valid_doc_ids and v in valid_statuses
    }

    collection = get_collection(COLLECTION_NAME)
    existing = await collection.find_one({"service_id": service_id, "customer_id": customer_id})
    if existing:
        merged = {**existing.get("statuses", {}), **clean_statuses}
        await collection.update_one(
            {"service_id": service_id, "customer_id": customer_id},
            {"$set": {"statuses": merged}},
        )
    else:
        merged = clean_statuses
        await collection.insert_one({
            "service_id": service_id,
            "customer_id": customer_id,
            "statuses": merged,
        })

    return _build_response(service, merged, lang)
