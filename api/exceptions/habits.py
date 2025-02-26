from exceptions.responses import (forbid_response,
                                  habit_already_exist_response,
                                  habit_not_found_response,
                                  unauthorized_response,
                                  user_not_found_response)
from starlette.status import (HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
                              HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND)

get_all_my_habits_responses = {HTTP_401_UNAUTHORIZED: unauthorized_response}

get_all_user_habits_responses = {
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
    HTTP_404_NOT_FOUND: user_not_found_response,
}

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
