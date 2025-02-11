from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)

from api.exceptions.responses import (
    unauthorized_response,
    habit_already_exist_response,
    forbid_response,
    habit_not_found_response,
)

get_all_my_habits_responses = {HTTP_401_UNAUTHORIZED: unauthorized_response}

add_habit_responses = {
    HTTP_400_BAD_REQUEST: habit_already_exist_response,
    HTTP_401_UNAUTHORIZED: unauthorized_response,
}

update_habit_responses = {
    HTTP_400_BAD_REQUEST: habit_already_exist_response,
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
    HTTP_404_NOT_FOUND: habit_not_found_response,
}

delete_habit_responses = {
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
    HTTP_404_NOT_FOUND: habit_not_found_response,
}


get_habit_by_id_responses = {
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
    HTTP_404_NOT_FOUND: habit_not_found_response,
}
