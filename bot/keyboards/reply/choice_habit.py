from schemas.habit import HabitSchema
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def get_habits_keyboard(habits: list[HabitSchema]) -> ReplyKeyboardMarkup:
    """Создает клавиатуру с названиями привычек."""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for habit in habits:
        keyboard.add(KeyboardButton(habit.name))

    return keyboard
