from helpers.api import ApiHelper
from message_generators.errors.habits import delete_habit_error_message
from schemas.habit import HabitCreated, HabitSchema, HabitUpdated
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from bot import tg_bot


class HabitsHelper(ApiHelper):
    """Класс для взаимодействия с моделью Habit."""

    def get_user_habits(self) -> list[HabitSchema] | None:
        """Делает запрос на получение всех привычек пользователя."""

        response = self._send_request(method="get", endpoint="/api/habits/me")

        if response.status_code == HTTP_200_OK:
            habits = response.json()
            return [HabitSchema.model_validate(i_habit) for i_habit in habits]
        return None

    def add_habit(self) -> HabitCreated | None:
        """Делает запрос на создание новой привычки."""

        habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": habit_name}

        response = self._send_request(
            method="post",
            endpoint="/api/habits",
            request_data=habit_data,
        )
        if response.status_code == HTTP_201_CREATED:
            habit = response.json()
            return HabitCreated.model_validate(habit)
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return None
        return None

    def update_habit(self, habit_id: int) -> HabitUpdated | None:
        """Делает запрос на изменение привычки."""

        new_habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": new_habit_name}

        response = self._send_request(
            method="patch",
            endpoint="/api/habits/{habit_id}".format(habit_id=habit_id),
            request_data=habit_data,
        )

        if response.status_code == HTTP_200_OK:
            habit = response.json()
            return HabitUpdated.model_validate(habit)
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return None
        return None

    def delete_habit(self, habit_id: int) -> None:
        """Делает запрос на удаление привычки."""

        response = self._send_request(
            method="delete",
            endpoint="/api/habits/{habit_id}".format(habit_id=habit_id),
        )

        if response.status_code != HTTP_204_NO_CONTENT:
            tg_bot.send_message(
                self.message.chat.id,
                delete_habit_error_message,
            )
