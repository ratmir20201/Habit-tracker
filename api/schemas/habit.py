from pydantic import BaseModel, ConfigDict

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
    user: User

    model_config = ConfigDict(from_attributes=True)


class HabitResponse(BaseModel):
    """Схема для ответа."""

    result: bool
    data: Habit | list[Habit]
