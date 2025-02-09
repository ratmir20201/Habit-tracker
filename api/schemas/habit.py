from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    pass


class HabitBase(BaseModel):
    """Базовая схема привычки."""

    name: str


class HabitCreate(HabitBase):
    """Схема для создания привычки."""


class HabitUpdate(HabitCreate):
    """Схема для обновления привычки."""


class HabitResponse(HabitBase):
    """Схема привычки с дополнительными данными."""

    id: int
    streak: int

    class Config:
        from_attributes = True
