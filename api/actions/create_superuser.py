import contextlib

from sqlalchemy import select

from api.authentication.user_manager import UserManager
from api.database.db import get_async_context_session
from api.dependencies.user_manager import get_user_manager
from api.dependencies.users import get_user_db
from api.models import User
from api.schemas.user import UserCreate

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
    )
    return user


async def create_superuser(
    email: str,
    username: str,
    password: str,
    is_active: bool = True,
    is_superuser: bool = True,
    is_verified: bool = True,
):
    async with get_async_context_session() as session:
        result = await session.execute(select(User).filter(User.is_superuser == True))
        superuser = result.scalar_one_or_none()

    # Если суперпользователь существует, не создаем нового
    if superuser:
        return superuser

    user_create = UserCreate(
        email=email,
        username=username,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    async with get_async_context_session() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )
