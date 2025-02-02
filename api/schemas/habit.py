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


class Habit(HabitBase):
    """Схема привычки с дополнительными данными."""

    id: int
    # user: "User"

    class Config:
        from_attributes = True


class HabitResponse(BaseModel):
    """Схема для ответа."""

    result: bool
    habit: Habit

    class Config:
        from_attributes = True


class HabitsResponse(BaseModel):
    """Схема для ответа."""

    result: bool
    habits: list[Habit]

    class Config:
        from_attributes = True
