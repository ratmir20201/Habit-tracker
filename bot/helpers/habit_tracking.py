from typing import Optional

from config import settings
from helpers.api import ApiHelper
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from telebot.types import Message

from schemas.habit import HabitSchema

HABIT_POINTED = "habit_pointed"
HABIT_COMPLETED = "habit_totally_complete"
HABIT_ALREADY_POINTED = "habit_already_pointed"


class HabitTrackingHelper(ApiHelper):
    """Класс для взаимодействия с моделью HabitTracking."""

    def __init__(self, message: Message):
        super().__init__(message)

    def add_tracking(
        self,
        habit_id: int,
    ) -> tuple[Optional[str], Optional[HabitSchema]]:
        """Отправляет запрос на отслеживание привычки и возвращает статус."""

        tracking_data = {"habit_id": habit_id}

        response = self._send_request(
            method="post",
            endpoint="/api/track_habit",
            data=tracking_data,
        )

        if response.status_code == HTTP_201_CREATED:
            habit_object = response.json().get("habit")
            if not habit_object:
                return None, None

            habit_streak = habit_object.get("streak", 0)
            if habit_streak >= settings.tg_bot.carry_over_complete_habits_days:
                return HABIT_COMPLETED, habit_object
            return HABIT_POINTED, habit_object
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return HABIT_ALREADY_POINTED, None

        return None, None
