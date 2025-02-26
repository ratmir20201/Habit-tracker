MIN_TEENS = 11
MAX_TEENS = 19
SINGLE = 1
FEW_MIN = 2
FEW_MAX = 4


def plural_days(days: int) -> str:
    """Определяет правильную форму слова "день" в зависимости от числа."""
    remainder_100 = days % 100
    remainder_10 = days % 10

    if MIN_TEENS <= remainder_100 <= MAX_TEENS:
        return "дней"
    elif remainder_10 == SINGLE:
        return "день"
    elif FEW_MIN <= remainder_10 <= FEW_MAX:
        return "дня"
    else:
        return "дней"
