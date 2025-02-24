def generate_response(description: str, detail: str):
    return {
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


habit_already_exist_response = generate_response(
    description="Привычка с таким именем уже существует.",
    detail="У вас уже имеется привычка с таким именем.",
)

forbid_response = generate_response(
    description="Недостаточно прав для данной операции.",
    detail="У вас недостаточно прав для данной операции.",
)


habit_not_found_response = generate_response(
    description="Привычка не была найдена.",
    detail="Привычка с таким id не была найдена.",
)

user_with_telegram_id_not_found_response = generate_response(
    description="Пользователь не был найден.",
    detail="Пользователь с таким telegram_id не был найден.",
)

user_not_found_response = generate_response(
    description="Пользователь не был найден.",
    detail="Пользователь с таким id не был найден.",
)

unauthorized_response = generate_response(
    description="Ошибка авторизации. Требуется вход в систему.",
    detail="Ошибка авторизации. Пожалуйста, войдите в систему.",
)


habit_already_pointed = generate_response(
    description="Привычка уже отмечена.",
    detail="Привычка уже отмечена как выполненная сегодня.",
)
