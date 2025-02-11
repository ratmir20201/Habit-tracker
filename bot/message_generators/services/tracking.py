def generate_answer_track_message(habit_name: str) -> str:
    return ("Выполнили ли вы сегодня привычку  *{}*?".format(habit_name),)


answer_point_habit_message = (
    "Выберите привычку, которую хотите пометить как выполненную:",
)
