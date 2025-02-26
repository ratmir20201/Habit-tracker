from typing import Callable, cast

from handlers.auth.before_register import take_username_for_register
from helpers.auth import AuthenticationHelper
from helpers.habits import HabitsHelper
from keyboards.reply.habits import (get_create_habit_keyboard,
                                    get_habits_crud_keyboard)
from message_generators.errors.auth import unexpected_login_error_message
from message_generators.keyboards.reply.default import login_button
from message_generators.responses.auth import auth_success_message
from message_generators.services.auth import register_suggestion_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["login"]))
def login_by_command(message: Message):
    login(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == login_button),
)
def login_by_keyboard(message: Message):
    login(message)


def login(message: Message) -> None:
    auth_helper = AuthenticationHelper(message)
    my_response = auth_helper.login_and_save_token_in_redis()

    if my_response == "success":
        habits_helper = HabitsHelper(message)
        habits = habits_helper.get_user_habits()

        if habits:
            reply_markup = get_habits_crud_keyboard()
        else:
            reply_markup = get_create_habit_keyboard()

        tg_bot.send_message(
            message.chat.id,
            auth_success_message,
            reply_markup=reply_markup,
        )
    elif my_response == "user_not_found":
        tg_bot.send_message(
            message.chat.id,
            register_suggestion_message,
        )
        tg_bot.register_next_step_handler(message, take_username_for_register)
    else:
        tg_bot.send_message(
            message.chat.id,
            unexpected_login_error_message,
        )
