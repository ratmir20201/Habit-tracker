from __future__ import annotations

import datetime

from pydantic import BaseModel

from api.schemas.habit import HabitResponse


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
    date: datetime.datetime
    habit: HabitResponse

    class Config:
        from_attributes = True
