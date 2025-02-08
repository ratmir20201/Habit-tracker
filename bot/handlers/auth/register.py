from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from telebot.types import Message

from helpers.auth import AuthenticationHelper
from main import tg_bot


@tg_bot.message_handler(commands=["register"])
def register_new_user(message: Message):
    from handlers import get_username

    tg_bot.send_message(message.chat.id, "Введите ваше имя:")
    tg_bot.register_next_step_handler(message, get_username)


def register(message: Message, username: str, email: str, password: str):
    user_data = {
        "telegram_id": message.from_user.id,
        "username": username,
        "email": email,
        "password": password,
    }

    auth_helper = AuthenticationHelper(message)
    status_code = auth_helper.register_user(user_data=user_data)

    if status_code == HTTP_201_CREATED:
        tg_bot.send_message(
            message.chat.id,
            "✅ Регистрация успешна! Теперь отправьте команду /start для входа.",
        )
    elif status_code == HTTP_400_BAD_REQUEST:
        from handlers import get_username

        tg_bot.send_message(
            message.chat.id,
            "Пользователь с таким именем или email уже существует.",
        )
        tg_bot.send_message(
            message.chat.id, "🔁 Попробуйте еще раз.\n\nВведите ваше имя:"
        )
        tg_bot.register_next_step_handler(message, get_username)
