from helpers.habit_tracking import (HABIT_ALREADY_POINTED, HABIT_COMPLETED,
                                    HABIT_POINTED)
from message_generators.errors.server import unexpected_server_error_message
from message_generators.responses.congratulations import \
    generate_congratulations_message
from message_generators.responses.tracking import (
    generate_is_tracked, habit_already_pointed_message)
from schemas.habit import HabitSchema


def generate_answer_track_message(habit_name: str) -> str:
    return "Выполнили ли вы сегодня привычку  *{}*?".format(habit_name)


answer_point_habit_message = (
    "Выберите привычку, которую хотите пометить как выполненную:"
)


def generate_tracking_message_text(
    my_response: str,
    habit: HabitSchema | None,
) -> str:
    if (my_response == HABIT_POINTED) and (habit is not None):
        message_text = generate_is_tracked(
            habit_name=habit.name,
            habit_streak=habit.streak,
        )
    elif (my_response == HABIT_COMPLETED) and (habit is not None):
        message_text = generate_congratulations_message(habit_name=habit.name)
    elif my_response == HABIT_ALREADY_POINTED:
        message_text = habit_already_pointed_message
    else:
        message_text = unexpected_server_error_message

    return message_text
