import datetime

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin
from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class HabitTracking(Base, IdIntPkMixin):
    """Модель отслеживания выполнения привычки."""

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    habit: Mapped["Habit"] = relationship(back_populates="tracking", lazy="selectin")

    date: Mapped[datetime.datetime] = mapped_column(Date)

    __table_args__ = (
        UniqueConstraint("habit_id", "date", name="unique_habit_tracking_date"),
    )


from models import Habit
