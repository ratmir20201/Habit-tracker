from fastapi import APIRouter

from api.dependencies.fastapi_users_router import fastapi_users
from api.schemas.user import UserRead, UserUpdate

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


router.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate),
)
