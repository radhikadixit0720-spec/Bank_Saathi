from fastapi import APIRouter, HTTPException, Query

from backend.data.branches import list_branch_services, list_branches
from backend.schemas.tokens import CreateTokenPayload, TokenRecord
from backend.services import token_service
from backend.utils.errors import bad_request, not_found, server_error

router = APIRouter(prefix="/api/tokens", tags=["Branch Token / Appointment"])


@router.get("/branches")
def get_branches():
    return list_branches()


@router.get("/services")
def get_services(lang: str = Query(default="en")):
    return list_branch_services(lang)


@router.post("", response_model=TokenRecord)
async def create_token(payload: CreateTokenPayload):
    try:
        record = await token_service.create_token(
            payload.customer_id, payload.customer_name, payload.branch_id, payload.service_id, payload.lang
        )
        if not record:
            raise bad_request("Invalid branch_id or service_id.")
        return record
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "tokens/create")


@router.get("/customer/{customer_id}", response_model=list[TokenRecord])
async def get_customer_tokens(customer_id: str):
    try:
        return await token_service.get_customer_tokens(customer_id)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "tokens/customer")


@router.get("/{token_id}", response_model=TokenRecord)
async def get_token(token_id: str):
    try:
        record = await token_service.get_token(token_id)
        if not record:
            raise not_found(f"No token found with id '{token_id}'.")
        return record
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "tokens/get")
