from typing import Any


async def generate_reminder_message(habits: list[dict[str, Any]]):
    message_text = "🔔 Напоминание! "
    if len(habits) == 1:
        message_text += "Не забудьте отметить свою привычку:\n*{}*.".format(
            habits[0]["name"]
        )
        return message_text

    message_text += " Не забудьте отметить свои привычки:\n"
    message_text += ", ".join("*{}*".format(habit["name"]) for habit in habits)

    return message_text
