from fastapi import APIRouter, HTTPException

from backend.services import request_service, token_service
from backend.utils.errors import server_error

router = APIRouter(prefix="/api/customer", tags=["Customer Dashboard"])


@router.get("/{customer_id}/summary")
async def get_customer_summary(customer_id: str):
    """Summary cards for the customer dashboard: pending/completed
    requests and the next upcoming branch token, if any."""
    try:
        requests = await request_service.get_customer_requests(customer_id)
        tokens = await token_service.get_customer_tokens(customer_id)

        pending = len([r for r in requests if r["status"] in ("submitted", "pending", "action_required")])
        completed = len([r for r in requests if r["status"] == "completed"])
        upcoming_token = next((t for t in tokens if t["status"] == "waiting"), None)

        return {
            "customer_id": customer_id,
            "pending_requests": pending,
            "completed_requests": completed,
            "total_requests": len(requests),
            "upcoming_appointment": upcoming_token,
            "recent_requests": requests[:5],
        }
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "customer/summary")
