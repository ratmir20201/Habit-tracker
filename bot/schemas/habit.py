from pydantic import BaseModel


class HabitSchema(BaseModel):
    """Схема привычки."""

    id: int
    name: str
    streak: int


class HabitCreated(BaseModel):
    name: str


class HabitUpdated(BaseModel):
    name: str
