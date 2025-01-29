from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from api.schemas.user import UserCreate


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    new_user = User(**user.model_dump())

    session.add(new_user)
    await session.commit()

    return new_user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)
