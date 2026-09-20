"""
Employee Dashboard service.

Aggregates data that already exists elsewhere (requests, checklist status,
stored error-check results) into a single view that helps bank staff spot
missing documents and validation problems without asking the customer to
repeat themselves or make another branch visit.

Only non-sensitive summary information is surfaced - no full document
images, account balances, or other sensitive banking data are exposed
here.
"""
from typing import Dict, List

from backend.data.checklists import get_checklist
from backend.database.mongo import get_collection
from backend.services import request_service

ERROR_CHECKS_COLLECTION = "error_checks"
CHECKLIST_COLLECTION = "checklist_status"


async def record_error_check(customer_id: str, request_type: str, errors: List[Dict]) -> None:
    collection = get_collection(ERROR_CHECKS_COLLECTION)
    existing = await collection.find_one({"customer_id": customer_id, "request_type": request_type})
    payload = {"messages": [e["message"] for e in errors]}
    if existing:
        await collection.update_one(
            {"customer_id": customer_id, "request_type": request_type},
            {"$set": payload},
        )
    else:
        await collection.insert_one({
            "customer_id": customer_id,
            "request_type": request_type,
            **payload,
        })


async def _missing_documents_for(customer_id: str, request_type: str) -> List[str]:
    checklist = get_checklist(request_type)
    if not checklist:
        return []
    record = await get_collection(CHECKLIST_COLLECTION).find_one(
        {"service_id": request_type, "customer_id": customer_id}
    )
    statuses = record["statuses"] if record else {}
    missing = []
    for doc in checklist["documents"]:
        if doc["required"] and statuses.get(doc["doc_id"], "missing") != "available":
            missing.append(doc["label"])
    return missing


async def _error_alerts_for(customer_id: str, request_type: str) -> List[str]:
    record = await get_collection(ERROR_CHECKS_COLLECTION).find_one(
        {"customer_id": customer_id, "request_type": request_type}
    )
    return record["messages"] if record else []


async def get_dashboard() -> Dict:
    all_requests = await request_service.list_all_requests()

    cards = []
    pending = completed = action_required = 0

    for req in all_requests:
        if req["status"] == "pending":
            pending += 1
        elif req["status"] == "completed":
            completed += 1
        elif req["status"] == "action_required":
            action_required += 1

        missing_docs = await _missing_documents_for(req["customer_id"], req["request_type"])
        error_alerts = await _error_alerts_for(req["customer_id"], req["request_type"])

        cards.append({
            "request_id": req["request_id"],
            "customer_id": req["customer_id"],
            "customer_name": req.get("customer_name"),
            "request_type": req["request_type"],
            "status": req["status"],
            "submitted_at": req["submitted_at"],
            "updated_at": req["updated_at"],
            "missing_documents": missing_docs,
            "error_alerts": error_alerts,
        })

    return {
        "total_requests": len(all_requests),
        "pending_count": pending,
        "completed_count": completed,
        "action_required_count": action_required,
        "requests": cards,
    }
