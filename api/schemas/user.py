from __future__ import annotations

from dataclasses import field

from fastapi_users import schemas
from pydantic import BaseModel

from api.schemas.habit import HabitBase


class UserRead(schemas.BaseUser[int]):
    username: str
    habits: list[HabitBase] = field(default_factory=list)


class UserCreate(schemas.BaseUserCreate):
    username: str
    # habits: list[HabitBase] = field(default_factory=list)


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    habits: list[HabitBase] = field(default_factory=list)


class User(BaseModel):
    """Схема пользователя с дополнительными данными."""

    username: str
    habits: list[HabitBase] = field(default_factory=list)

    class Config:
        from_attributes = True
