import functools
from typing import Any, Callable

from logger import logger
from schemas.exceptions import (
    APIRequestError,
    UnauthorizedUserError,
    UnexpectedServerError,
)


def api_error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для обработки неожиданных исключений с API."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except (APIRequestError, UnexpectedServerError):
            logger.warning(
                "Произошла ошибка при запросе API, продолжаем работу бота..."
            )
            return None

    return wrapper


def unauth_user_error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для обработки не аутентифицированного пользователя."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except UnauthorizedUserError:
            logger.warning("Пользователь не авторизован.")
            return None

    return wrapper
