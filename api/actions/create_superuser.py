import contextlib
from typing import Optional

from authentication.user_manager import UserManager
from database.db import get_async_context_session
from dependencies.user_manager import get_user_manager
from dependencies.users import get_user_db
from models import User
from schemas.user import UserCreate
from sqlalchemy import select

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    """Создает пользователя."""
    user = await user_manager.create(
        user_create=user_create,
    )
    return user


async def create_superuser(
    email: str,
    username: str,
    password: str,
    telegram_id: Optional[int] = None,
    is_active: bool = True,
    is_superuser: bool = True,
    is_verified: bool = True,
) -> User:
    """
    Создает суперпользователя.

    Если суперпользователь существует, не создаем нового.
    """

    async with get_async_context_session() as session:
        superuser_query = await session.execute(
            select(User).where(User.is_superuser.is_(True)),
        )
        superuser = superuser_query.scalar_one_or_none()

    if superuser:
        return superuser

    user_create = UserCreate(
        email=email,
        username=username,
        password=password,
        telegram_id=telegram_id,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    return await add_superuser_to_db(user_create=user_create)


async def add_superuser_to_db(user_create: UserCreate) -> User:
    """Добавляет суперпользователя в бд."""
    async with get_async_context_session() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )
