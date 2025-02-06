from pydantic import BaseModel, EmailStr, Field, root_validator, model_validator
import re

from typing_extensions import Self


class RegisterSchema(BaseModel):
    telegram_id: int
    username: str
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if len(self.password) < 8:
            raise ValueError("Passwords do not match")
        if not re.search(r"[A-Z]", self.password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not re.search(r"\d", self.password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")

        return self
