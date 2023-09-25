from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.controller.service.health_check import HealthCheckService
from app.core.container import Container
from app.domain.schema.health_check import HealthCheckResponse

router = APIRouter(prefix="/health_check", tags=["Health Check"])


@router.get("/", response_model=HealthCheckResponse)
@inject
async def health_check(
    health_check_service: HealthCheckService = Depends(
        Provide[Container.health_check_service]
    ),
):
    result = await health_check_service.get_info()
    return result
