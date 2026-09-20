from fastapi import APIRouter, HTTPException

from backend.schemas.requests import CreateRequestPayload, RequestRecord, UpdateStatusPayload, VALID_STATUSES
from backend.services import request_service
from backend.utils.errors import bad_request, not_found, server_error

router = APIRouter(prefix="/api/requests", tags=["Status & Receipt Vault"])


@router.post("", response_model=RequestRecord)
async def create_request(payload: CreateRequestPayload):
    try:
        return await request_service.create_request(
            payload.customer_id, payload.customer_name, payload.request_type, payload.notes
        )
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "requests/create")


@router.get("/customer/{customer_id}", response_model=list[RequestRecord])
async def get_customer_requests(customer_id: str):
    try:
        return await request_service.get_customer_requests(customer_id)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "requests/customer")


@router.get("/{request_id}", response_model=RequestRecord)
async def get_request(request_id: str):
    try:
        record = await request_service.get_request(request_id)
        if not record:
            raise not_found(f"No request found with id '{request_id}'.")
        return record
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "requests/get")


@router.patch("/{request_id}/status", response_model=RequestRecord)
async def update_status(request_id: str, payload: UpdateStatusPayload):
    try:
        if payload.status not in VALID_STATUSES:
            raise bad_request(f"status must be one of {VALID_STATUSES}")
        record = await request_service.update_request_status(request_id, payload.status, payload.notes)
        if not record:
            raise not_found(f"No request found with id '{request_id}'.")
        return record
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "requests/update-status")
