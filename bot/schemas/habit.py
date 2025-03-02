from pydantic import BaseModel


class HabitSchema(BaseModel):
    """Схема привычки."""

    id: int
    name: str
    streak: int


class HabitCreated(BaseModel):
    """Схема для создания привычки."""

    name: str


class HabitUpdated(BaseModel):
    """Схема для изменения привычки."""

    name: str
