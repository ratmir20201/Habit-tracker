import functools
from typing import Any, Callable

from schemas.exceptions import APIRequestError, UnexpectedServerError

from bot import tg_bot
from logger import logger
from message_generators.errors.server import unexpected_server_error_message


def api_error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except (APIRequestError, UnexpectedServerError):
            logger.warning(
                "Произошла ошибка при запросе API, продолжаем работу бота..."
            )
            tg_bot.send_message(
                args[0].message.chat.id,  # Достаем `message` из `self`
                unexpected_server_error_message,
            )
            return None

    return wrapper
