from authentication.fastapi_users_router import fastapi_users
from fastapi import APIRouter
from schemas.user import UserRead, UserUpdate

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


router.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate),
)
