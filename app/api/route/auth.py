from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.controller.service.auth import AuthService
from app.core.container import Container
from app.domain.schema.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
@inject
async def login(
        data: LoginRequest,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    result = await auth_service.login(data=data)
    return result
