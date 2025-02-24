from pydantic_core import ErrorDetails

user_not_authorized_message = "❌ Вы не авторизованы! Введите /start"
user_already_exist_message = "Пользователь с таким именем или email уже существует."

unexpected_login_error_message = "❌ Неизвестная ошибка при авторизации."
unexpected_register_error_message = "❌ Неизвестная ошибка при регистрации."


def generate_register_error_message(errors: list[ErrorDetails]) -> str:
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

    return unexpected_register_error_message
