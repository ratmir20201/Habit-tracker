from utils.morphology import plural_days


def generate_is_tracked(habit_name: str, habit_streak: int) -> str:
    return (
        "✅ Привычка *{habit_name}* успешно помечена как выполненная!\n"
        "Вы выполняете данную привычку *{habit_streak}* {days} 🔥!"
    ).format(
        habit_name=habit_name,
        habit_streak=habit_streak,
        days=plural_days(habit_streak),
    )


habit_already_pointed_message = "Привычка уже отмечена как выполненная сегодня!"
