from handlers.auth.before_register import get_username
from helpers.auth import AuthenticationHelper
from helpers.habits import HabitsHelper
from keyboards.reply.habits import (get_create_habit_keyboard,
                                    get_habits_crud_keyboard)
from message_generators.keyboards.reply.default import login_button
from message_generators.responses.auth import auth_success_message
from message_generators.services.auth import register_suggestion_message
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["login"])
def login_by_command(message: Message):
    login(message)


@tg_bot.message_handler(func=lambda message: message.text == login_button)
def login_by_keyboard(message: Message):
    login(message)


def login(message: Message):
    auth_helper = AuthenticationHelper(message)
    status_code = auth_helper.login_and_save_token_in_redis()

    if status_code == HTTP_200_OK:
        habits_helper = HabitsHelper(message)
        habits = habits_helper.get_user_habits()

        if not habits:
            reply_markup = get_create_habit_keyboard()
        else:
            reply_markup = get_habits_crud_keyboard()

        tg_bot.send_message(
            message.chat.id,
            auth_success_message,
            reply_markup=reply_markup,
        )
    elif status_code == HTTP_404_NOT_FOUND:
        tg_bot.send_message(
            message.chat.id,
            register_suggestion_message,
        )
        tg_bot.register_next_step_handler(message, get_username)
