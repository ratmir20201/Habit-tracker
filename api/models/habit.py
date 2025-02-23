from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Habit(Base, IdIntPkMixin):
    """Модель привычки."""

    name: Mapped[str]
    tracking: Mapped[list["HabitTracking"]] = relationship(
        back_populates="habit",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="habits")

    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_user_habit"),)

    @property
    def streak(self) -> int:
        """Получает количество дней выполнения привычки."""
        return len(self.tracking)


from models import HabitTracking, User
