from message_generators.keyboards.reply.habits import (add_first_habit_button,
                                                       add_habit_button,
                                                       delete_habit_button,
                                                       edit_habit_button,
                                                       get_habits_button,
                                                       track_all_habit_button,
                                                       track_one_habit_button)
from message_generators.services.keyboards import choose_command_message
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def get_habits_crud_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder=choose_command_message,
    )

    keyboard.row(
        KeyboardButton(get_habits_button),
        KeyboardButton(add_habit_button),
    )
    keyboard.row(
        KeyboardButton(edit_habit_button),
        KeyboardButton(delete_habit_button),
    )
    keyboard.row(
        KeyboardButton(track_one_habit_button),
        KeyboardButton(track_all_habit_button),
    )

    return keyboard


def get_create_habit_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton(add_first_habit_button))

    return keyboard
