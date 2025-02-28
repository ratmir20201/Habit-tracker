from schemas.habit import HabitSchema


def generate_get_habits_message(habits: list[HabitSchema]) -> str:
    message_text = "✨ *Ваши привычки:*\n\n"

    for habit in habits:
        message_text += "📌 *{habit_name}*\n".format(habit_name=habit.name)
        message_text += "   🔥 Дней подряд: *{habit_streak}*\n\n".format(
            habit_streak=habit.streak,
        )

    return message_text


def generate_edit_habit_message(habit_name: str) -> str:
    return "✅ Привычка успешно обновлена на: *{}*.".format(habit_name)


def generate_delete_habit_message(habit_name: str) -> str:
    return "✅ Привычка *{}* успешно удалена.".format(habit_name)


def generate_add_habit_message(habit_name: str, first_habit: bool = False) -> str:
    if first_habit:
        first_sentence = "✨ *Ваша первая привычка добавлена!* ✨"
    else:
        first_sentence = "✨ *Новая привычка добавлена!* ✨"

    message_text = (
        "{first_sentence}\n\n" "✅ Привычка *{habit_name}* успешно создана!"
    ).format(
        first_sentence=first_sentence,
        habit_name=habit_name,
    )

    return message_text
