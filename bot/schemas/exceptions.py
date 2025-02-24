class APIRequestError(Exception):
    """Кастомное исключение для API ошибок."""


class InvalidUserDataError(Exception):
    """Ошибка валидации данных пользователя."""


class UnexpectedServerError(Exception):
    """Неожиданная ошибка сервера."""
