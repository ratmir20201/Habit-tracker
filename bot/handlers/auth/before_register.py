from handlers.auth.register import register
from message_generators.services.auth import (input_email_message,
                                              input_password_message)
from telebot.types import Message
from utils.register_message_checker import is_command

from main import tg_bot


def get_username(message: Message):
    if is_command(message):
        return
    username = message.text
    tg_bot.send_message(message.chat.id, input_email_message)
    tg_bot.register_next_step_handler(message, get_email, username)


def get_email(message: Message, username: str):
    if is_command(message):
        return
    email = message.text
    tg_bot.send_message(message.chat.id, input_password_message)
    tg_bot.register_next_step_handler(message, get_password, username, email)


def get_password(message: Message, username: str, email: str):
    if is_command(message):
        return
    password = message.text
    register(message, username, email, password)
