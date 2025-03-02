from datetime import date
from typing import List

from pydantic import BaseModel


class TrackingSchema(BaseModel):
    """Схема дат отметки привычки."""

    date: date


class HabitSchema(BaseModel):
    """Схема привычки."""

    id: int
    name: str
    tracking: List[TrackingSchema]


class UntrackResponseSchema(BaseModel):
    """Схема отправки пользователей забывших отметить привычки."""

    telegram_id: int
    habits: List[HabitSchema]
