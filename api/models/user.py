from database.base import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from models.mixins.id_int_pk import IdIntPkMixin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    """Модель пользователя."""

    username: Mapped[str] = mapped_column(unique=True)
    telegram_id: Mapped[int | None] = mapped_column(unique=True)

    habits: Mapped[list["Habit"]] = relationship(back_populates="user", lazy="selectin")

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, User)
