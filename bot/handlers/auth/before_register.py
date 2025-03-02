from handlers.auth.register import register
from message_generators.services.auth import input_email_message, input_password_message
from telebot.types import Message
from utils.register_message_checker import is_command

from bot import tg_bot


def take_username_for_register(message: Message):
    """Получает username пользователя."""

    if is_command(message):
        return
    username = message.text.strip()
    tg_bot.send_message(message.chat.id, input_email_message)
    tg_bot.register_next_step_handler(message, take_email_for_register, username)


def take_email_for_register(message: Message, username: str):
    """Получает email пользователя."""

    if is_command(message):
        return
    email = message.text.strip()
    tg_bot.send_message(message.chat.id, input_password_message)
    tg_bot.register_next_step_handler(
        message, take_password_for_register, username, email
    )


def take_password_for_register(message: Message, username: str, email: str):
    """Получает пароль пользователя и запускает регистрацию."""

    if is_command(message):
        return
    password = message.text.strip()
    register(message, username, email, password)
