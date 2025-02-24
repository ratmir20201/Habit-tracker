from message_generators.keyboards.reply.default import (
    help_button,
    info_button,
    login_button,
    logout_button,
    start_button,
)
from message_generators.services.keyboards import choose_command_message
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder=choose_command_message,
    )
    keyboard.add(KeyboardButton(start_button), KeyboardButton(info_button))
    keyboard.add(KeyboardButton(login_button), KeyboardButton(logout_button))
    keyboard.add(KeyboardButton(help_button))

    return keyboard
