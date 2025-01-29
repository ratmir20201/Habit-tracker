from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.base import Base


class User(Base):
    """Модель пользователя."""

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]

    habits: Mapped[list["Habit"]] = relationship(back_populates="user")
