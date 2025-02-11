from typing import Optional

from helpers.api import ApiHelper
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from telebot.types import Message
from test_config import settings


class HabitTrackingHelper(ApiHelper):
    """Класс для взаимодействия с моделью HabitTracking."""

    def __init__(self, message: Message):
        super().__init__(message)

    def add_tracking(self, habit_id: int) -> tuple[str, Optional[dict[str, str]]]:
        tracking_data = {"habit_id": habit_id}

        response = self._send_request(
            method="post",
            endpoint="/api/track_habit",
            data=tracking_data,
        )

        if response.status_code == HTTP_201_CREATED:
            habit_object = response.json()["habit"]
            habit_name = habit_object["name"]
            habit_streak = habit_object["streak"]
            if habit_streak >= settings.tg_bot.carry_over_complete_habits_days:
                return "habit_totally_complete", habit_name
            return "habit_pointed", habit_name
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return "habit_not_pointed", None
