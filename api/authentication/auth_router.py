from fastapi import APIRouter

from api.dependencies.backend import authentication_backend
from api.dependencies.fastapi_users_router import fastapi_users
from api.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)


# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)

# /forgot-password
# /reset-password
router.include_router(
    fastapi_users.get_reset_password_router(),
)
