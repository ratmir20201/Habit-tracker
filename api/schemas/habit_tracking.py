from __future__ import annotations

from datetime import date  # noqa: F401

from pydantic import BaseModel
from schemas.habit import HabitResponse


class HabitTrackingBase(BaseModel):
    """Базовая схема трекера привычки."""


class HabitTrackingCreate(HabitTrackingBase):
    """Схема для создания трекера привычки."""

    habit_id: int


class HabitTrackingUpdate(HabitTrackingCreate):
    """Схема для обновления трекера привычки."""


class HabitTrackingResponse(HabitTrackingBase):
    """Схема трекера привычки с дополнительными данными."""

    id: int
    date: date
    habit: HabitResponse

    class Config:
        from_attributes = True
