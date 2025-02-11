from typing import Any

user_not_authorized_message = "❌ Вы не авторизованы! Введите /start"
user_already_exist_message = "Пользователь с таким именем или email уже существует."


def generate_register_error_message(errors: list[dict[str, Any]]) -> str:
    for error in errors:
        field = error["loc"][0]
        error_message = error["msg"]

        if field == "email":
            error_message = (
                "Некорректный формат email. Пожалуйста, введите правильный email."
            )
        elif field == "password":
            error_message = "Пароль должен содержать минимум 8 символов, одну заглавную букву и цифру."

        return "❌ Ошибка: {}".format(error_message)
