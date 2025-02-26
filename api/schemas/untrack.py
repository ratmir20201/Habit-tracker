from datetime import date
from typing import List

from pydantic import BaseModel


class TrackingSchema(BaseModel):
    date: date


class HabitSchema(BaseModel):
    id: int
    name: str
    tracking: List[TrackingSchema]


class UntrackResponseSchema(BaseModel):
    telegram_id: int
    habits: List[HabitSchema]
