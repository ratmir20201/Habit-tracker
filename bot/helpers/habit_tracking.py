from typing import Optional

from config import settings
from helpers.api import ApiHelper
from schemas.habit import HabitSchema
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

HABIT_POINTED = "habit_pointed"
HABIT_COMPLETED = "habit_totally_complete"
HABIT_ALREADY_POINTED = "habit_already_pointed"


class HabitTrackingHelper(ApiHelper):
    """Класс для взаимодействия с моделью HabitTracking."""

    def add_tracking(
        self,
        habit_id: int,
    ) -> tuple[Optional[str], Optional[HabitSchema]]:
        """
        Отправляет запрос на отслеживание привычки и возвращает статус.

        Возможные ответы: HABIT_POINTED(успешно), HABIT_COMPLETED(пользователь выполнил
        план), HABIT_ALREADY_POINTED(привычка уже помечена). При успешных ответах
        также отправляется объект привычки.
        """

        tracking_data = {"habit_id": habit_id}

        response = self._send_request(
            method="post",
            endpoint="/api/track_habit",
            request_data=tracking_data,
        )

        if response.status_code == HTTP_201_CREATED:
            habit = response.json().get("habit")
            if not habit:
                return None, None

            habit_object = HabitSchema.model_validate(habit)

            if habit_object.streak >= settings.tg_bot.carry_over_complete_habits_days:
                return HABIT_COMPLETED, habit_object
            return HABIT_POINTED, habit_object
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return HABIT_ALREADY_POINTED, None

        return None, None
