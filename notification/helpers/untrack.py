from notification.helpers.api import ApiHelper


class UntrackedUsers(ApiHelper):
    """Класс для получения пользователей не отмечавших свои привычки."""

    async def get_untracked_users(self):
        response = await self._send_request(
            method="get",
            endpoint="/api/telegram/untracked_users",
        )
        return response.json()
