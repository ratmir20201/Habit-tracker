from typing import List, Union, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    pass


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
    # user: "User"

    class Config:
        from_attributes = True


class HabitResponse(BaseModel):
    """Схема для ответа."""

    result: bool
    data: Union[Habit, List[Habit]]

    class Config:
        from_attributes = True
