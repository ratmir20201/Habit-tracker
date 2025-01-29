from fastapi import APIRouter

from api.routes.habits import router as habits_router
from api.routes.users import router as users_router

main_router = APIRouter()

main_router.include_router(habits_router)
main_router.include_router(users_router)
