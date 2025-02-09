from typing import Any

from helpers.api import ApiHelper
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from telebot.types import Message

from main import tg_bot


class HabitsHelper(ApiHelper):
    """Класс для взаимодействия с моделью Habit."""

    def __init__(self, message: Message):
        super().__init__(message)

    def get_user_habits(self) -> list[dict[str, Any]] | None:
        response = self._send_request(method="get", endpoint="/api/habits/me")

        if not response:
            return None

        if response.status_code == HTTP_200_OK:
            habits = response.json()
            if not habits:
                tg_bot.send_message(self.message.chat.id, "❌ У вас пока нет привычек.")
                return None
            return habits
        elif response.status_code == HTTP_401_UNAUTHORIZED:
            return

    def add_habit(self) -> dict[str, Any] | None:
        habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": habit_name}

        response = self._send_request(
            method="post",
            endpoint="/api/habits",
            data=habit_data,
        )

        if response.status_code == HTTP_201_CREATED:
            habit = response.json()
            return habit
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return None

    def update_habit(self, habit_id: int) -> dict[str, Any]:
        new_habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": new_habit_name}

        response = self._send_request(
            method="patch",
            endpoint="/api/habits/{habit_id}".format(habit_id=habit_id),
            data=habit_data,
        )

        if response.status_code == HTTP_200_OK:
            habit = response.json()
            return habit

    def delete_habit(self, habit_id: int) -> None:
        response = self._send_request(
            method="delete",
            endpoint="/api/habits/{habit_id}".format(habit_id=habit_id),
        )

        if response.status_code != HTTP_204_NO_CONTENT:
            tg_bot.send_message(
                self.message.chat.id, "❌ Ошибка при удалении привычки."
            )
            return None
