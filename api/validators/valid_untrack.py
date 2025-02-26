from typing import Any

from schemas.untrack import HabitSchema, TrackingSchema, UntrackResponseSchema


async def valid_untracked_users_habits(
    untracked_users_habits: list[dict[str, Any]]
) -> list[UntrackResponseSchema]:
    """Метод превращающий данные в валидированную схему."""

    untracked_habits_response = []

    for i_user_habits in untracked_users_habits:
        habits = i_user_habits["habits"]
        validate_habits = [
            HabitSchema(
                id=habit.id,
                name=habit.name,
                tracking=[TrackingSchema(date=track.date) for track in habit.tracking],
            )
            for habit in habits
        ]
        untracked_habits_response.append(
            UntrackResponseSchema(
                telegram_id=i_user_habits["telegram_id"],
                habits=validate_habits,
            )
        )

    return untracked_habits_response
