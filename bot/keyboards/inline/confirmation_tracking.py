from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirmation_tracking_keyboard(habit_id: int):
    """Создает inline-клавиатуру с кнопками ✅ и ❌."""
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "✅",
            callback_data="confirm_yes_{}".format(habit_id),
        ),
        InlineKeyboardButton(
            "❌",
            callback_data="confirm_no_{}".format(habit_id),
        ),
    )

    return keyboard
