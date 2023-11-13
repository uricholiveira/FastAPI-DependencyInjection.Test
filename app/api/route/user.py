from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.controller.service.user import UserService
from app.core.container import Container
from app.domain.schema.user import UserCreationResponse, UserSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=UserSchema)
@inject
async def get_user(
        user_service: UserService = Depends(
            Provide[Container.user_service]
        ),
):
    result = await user_service.get_one()
    return result


@router.post("/", response_model=UserCreationResponse)
@inject
async def create_user(
        data: UserSchema,
        user_service: UserService = Depends(
            Provide[Container.user_service]
        ),
):
    result = await user_service.create(data=data)
    return result
