from pydantic import BaseModel, EmailStr, ConfigDict

from api.models.habit import Habit


# Базовые схемы
class UserBase(BaseModel):
    """Базовая схема пользователя."""

    username: str
    email: EmailStr


# Схемы для создания записей
class UserCreate(UserBase):
    """Схема для создания пользователя."""

    pass


class User(UserBase):
    """Схема пользователя с дополнительными данными."""

    id: int
    habits: list[Habit] = []

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    result: bool
    data: User
