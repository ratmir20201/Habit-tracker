from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.base import Base
from api.models.mixins.id_int_pk import IdIntPkMixin


class Habit(Base, IdIntPkMixin):
    """Модель привычки."""

    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="habits")
