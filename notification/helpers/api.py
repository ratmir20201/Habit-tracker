from abc import ABC

import httpx
import requests
from config import settings
from logger import logger
from starlette.status import HTTP_200_OK

from notification.helpers.exception_handlers import api_request_error_handler


class ApiHelper(ABC):
    """Абстрактный класс для взаимодействия с api."""

    API_URL: str = settings.api.url

    def __init__(self):
        self.headers = None

    async def init(self):
        """Асинхронная инициализация (должна быть вызвана после создания экземпляра)."""
        self.headers = await self.login_as_admin()

    async def login_as_admin(self):
        """Метод для подключения к серверу как админ."""
        response = await self._send_request(
            method="post",
            endpoint="/auth/login",
            data={
                "grant_type": "password",
                "username": settings.api.superuser_email,
                "password": settings.api.superuser_password,
            },
            custom_headers={
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            is_form_data=True,
        )
        if response.status_code == HTTP_200_OK:
            token = response.json()["access_token"]
            return await self.get_auth_headers(token=token)
        logger.error("Данные админа не верны.")
        return

    @staticmethod
    async def get_auth_headers(token: str):
        """Метод для получения заголовков для дальнейших запросов."""
        return {"Authorization": "Bearer {token}".format(token=token)}

    @api_request_error_handler
    async def _send_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        custom_headers: dict = None,
        is_form_data: bool = False,  # Добавляем флаг для x-www-form-urlencoded
    ) -> requests.Response:
        """Метод для создания запросов к API."""

        url = f"{self.API_URL}{endpoint}"

        async with httpx.AsyncClient() as client:
            if is_form_data:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=custom_headers,
                    data=data,
                    params=params,
                )
            else:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    params=params,
                )

        return response
