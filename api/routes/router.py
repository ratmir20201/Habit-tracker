from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from routes.habit_tracking import router as habit_tracking_router
from routes.habits import router as habits_router
from routes.users import router as users_router
from routes.telegram.untracked_users import router as telegram_router

http_bearer = HTTPBearer(auto_error=False)

main_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(http_bearer)],
)

main_router.include_router(habits_router)
main_router.include_router(users_router)
main_router.include_router(habit_tracking_router)
main_router.include_router(telegram_router)
