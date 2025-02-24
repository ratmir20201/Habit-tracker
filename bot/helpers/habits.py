from helpers.api import ApiHelper
from message_generators.errors.habits import (
    delete_habit_error_message,
    habit_already_exist_message,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from telebot.types import Message

from bot import tg_bot
from schemas.habit import HabitSchema


class HabitsHelper(ApiHelper):
    """Класс для взаимодействия с моделью Habit."""

    def __init__(self, message: Message):
        super().__init__(message)

    def get_user_habits(self) -> list[HabitSchema] | None:
        response = self._send_request(method="get", endpoint="/api/habits/me")

        if response.status_code == HTTP_200_OK:
            habits: list[HabitSchema] = response.json()
            return habits
        return None

    def add_habit(self) -> HabitSchema | None:
        habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": habit_name}

        response = self._send_request(
            method="post",
            endpoint="/api/habits",
            data=habit_data,
        )

        if response.status_code == HTTP_201_CREATED:
            habit: HabitSchema = response.json()
            return habit
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return None
        return None

    def update_habit(self, habit_id: int) -> HabitSchema | None:
        new_habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": new_habit_name}

        response = self._send_request(
            method="patch",
            endpoint="/api/habits/{habit_id}".format(habit_id=habit_id),
            data=habit_data,
        )

        if response.status_code == HTTP_200_OK:
            habit: HabitSchema = response.json()
            return habit
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return None
        return None

    def delete_habit(self, habit_id: int) -> None:
        response = self._send_request(
            method="delete",
            endpoint="/api/habits/{habit_id}".format(habit_id=habit_id),
        )

        if response.status_code != HTTP_204_NO_CONTENT:
            tg_bot.send_message(
                self.message.chat.id,
                delete_habit_error_message,
            )
        return None
