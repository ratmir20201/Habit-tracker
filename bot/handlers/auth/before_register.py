from handlers.auth.register import register
from main import tg_bot


def get_username(message):
    username = message.text
    tg_bot.send_message(message.chat.id, "Введите ваш email: ")
    tg_bot.register_next_step_handler(message, get_email, username)


def get_email(message, username: str):
    email = message.text
    tg_bot.send_message(message.chat.id, "Введите ваш пароль: ")
    tg_bot.register_next_step_handler(message, get_password, username, email)


def get_password(message, username: str, email: str):
    password = message.text
    register(message, username, email, password)
