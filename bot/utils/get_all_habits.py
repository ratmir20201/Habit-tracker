from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from helpers.habits import HabitsHelper
from main import tg_bot


def get_all_habits(message: Message):
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    if not habits:
        tg_bot.send_message(message.chat.id, "❌ У вас пока нет привычек.")
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for habit in habits:
        keyboard.add(KeyboardButton(habit["name"]))
