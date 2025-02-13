def plural_days(days: int) -> str:
    if 11 <= days % 100 <= 19:
        return "дней"
    elif days % 10 == 1:
        return "день"
    elif 2 <= days % 10 <= 4:
        return "дня"
    else:
        return "дней"
