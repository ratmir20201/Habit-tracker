from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.routes.habits import router as habits_router
from api.routes.users import router as users_router
from api.routes.habit_tracking import router as habit_tracking_router

http_bearer = HTTPBearer(auto_error=False)

main_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(http_bearer)],
)

main_router.include_router(habits_router)
main_router.include_router(users_router)
main_router.include_router(habit_tracking_router)
