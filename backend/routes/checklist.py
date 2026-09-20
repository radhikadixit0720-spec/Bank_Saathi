from fastapi import APIRouter, HTTPException, Query

from backend.data.checklists import list_services
from backend.schemas.checklist import ChecklistResponse, ChecklistStatusUpdate
from backend.services import checklist_service
from backend.utils.errors import not_found, server_error

router = APIRouter(prefix="/api/checklist", tags=["Document Checklist"])


@router.get("/services")
def get_services(lang: str = Query(default="en")):
    """List the banking services a document checklist is available for."""
    return list_services(lang)


@router.get("/{service_id}", response_model=ChecklistResponse)
async def get_checklist(service_id: str, customer_id: str = Query(default="guest"), lang: str = Query(default="en")):
    try:
        result = await checklist_service.get_checklist_for_customer(service_id, customer_id, lang)
        if result is None:
            raise not_found(f"No checklist configured for service '{service_id}'.")
        return result
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "checklist/get")


@router.post("/{service_id}/status", response_model=ChecklistResponse)
async def update_checklist_status(service_id: str, payload: ChecklistStatusUpdate, lang: str = Query(default="en")):
    try:
        result = await checklist_service.update_checklist_status(
            service_id, payload.customer_id or "guest", payload.statuses, lang
        )
        if result is None:
            raise not_found(f"No checklist configured for service '{service_id}'.")
        return result
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "checklist/update-status")
