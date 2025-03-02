import functools
from typing import Any, Callable

from logger import logger
from schemas.exceptions import InvalidUserDataError


def invalid_user_data_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для обработки некорректных данных пользователя."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except InvalidUserDataError:
            logger.warning("Произошла ошибка при валидации данных пользователя.")
            return None

    return wrapper
