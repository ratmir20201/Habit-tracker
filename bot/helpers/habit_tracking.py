from helpers.api import ApiHelper
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from telebot.types import Message


class HabitTrackingHelper(ApiHelper):
    """Класс для взаимодействия с моделью HabitTracking."""

    def __init__(self, message: Message):
        super().__init__(message)

    def add_tracking(self, habit_id: int) -> bool | None:
        tracking_data = {"habit_id": habit_id}

        response = self._send_request(
            method="post",
            endpoint="/api/track_habit",
            data=tracking_data,
        )

        if response.status_code == HTTP_201_CREATED:
            return True
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return False
