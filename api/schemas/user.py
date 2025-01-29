from pydantic import BaseModel, EmailStr

from api.schemas.habit import Habit


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Схема для создания пользователя."""


class User(UserBase):
    """Схема пользователя с дополнительными данными."""

    id: int
    habits: list[Habit] = []

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    result: bool
    data: User
