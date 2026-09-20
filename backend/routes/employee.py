from fastapi import APIRouter, HTTPException

from backend.schemas.employee import EmployeeDashboardResponse
from backend.services import employee_service
from backend.utils.errors import server_error

router = APIRouter(prefix="/api/employee", tags=["Employee Dashboard"])


@router.get("/dashboard", response_model=EmployeeDashboardResponse)
async def get_dashboard():
    """Aggregated view for bank staff: requests, missing documents and
    validation alerts, so customers are not asked to repeat information
    or make an extra branch visit."""
    try:
        return await employee_service.get_dashboard()
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise server_error(exc, "employee/dashboard")
