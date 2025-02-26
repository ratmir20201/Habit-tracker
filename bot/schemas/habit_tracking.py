from datetime import date

from pydantic import BaseModel
from schemas.habit import HabitSchema


class HabitTrackingSchema(BaseModel):
    """Схема трекера привычки."""

    id: int
    date: date
    habit: HabitSchema
