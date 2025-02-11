from test_config import settings


def generate_congratulations_message(habit_name: str) -> str:
    return (
        "🎉 Поздравляем! Вы успешно закрепили привычку {habit_name}, выполнив её {habit_streak} дней подряд. "
        "Теперь она стала частью вашей жизни!"
    ).format(
        habit_name=habit_name,
        habit_streak=settings.tg_bot.carry_over_complete_habits_days,
    )
