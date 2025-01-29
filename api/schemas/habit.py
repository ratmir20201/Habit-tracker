from __future__ import annotations

from typing import List, Union

from pydantic import BaseModel

from api.schemas.user import User


class HabitBase(BaseModel):
    """Базовая схема привычки."""

    name: str


class HabitCreate(HabitBase):
    """Схема для создания привычки."""

    user_id: int


class HabitUpdate(HabitCreate):
    """Схема для обновления привычки."""


class Habit(HabitBase):
    """Схема привычки с дополнительными данными."""

    id: int
    user: "User"

    class Config:
        from_attributes = True


class HabitResponse(BaseModel):
    """Схема для ответа."""

    result: bool
    data: Union[Habit, List[Habit]]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


Habit.model_rebuild()
HabitResponse.model_rebuild()
