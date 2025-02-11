from database.base import Base
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase, SQLAlchemyBaseAccessTokenTable)
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyAccessTokenDatabase(session, AccessToken)
