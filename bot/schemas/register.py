import re

from pydantic import BaseModel, EmailStr, field_validator


class RegisterSchema(BaseModel):
    telegram_id: int
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, password: str) -> str:
        """Валидатор пароля: минимум 8 символов, одна заглавная буква и одна цифра."""

        if len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not re.search(r"\d", password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        return password
