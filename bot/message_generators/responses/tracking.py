def generate_is_tracked(habit_name: str) -> str:
    return "✅ Привычка *{habit_name}* успешно помечена как выполненная!".format(
        habit_name=habit_name
    )


habit_already_pointed_message = "Привычка уже отмечена как выполненная сегодня!"
