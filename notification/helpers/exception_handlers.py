import functools
from typing import Any, Callable

import requests
from logger import logger


def api_request_error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.error("Ошибка запроса: {}".format(e))
            return None

    return wrapper
