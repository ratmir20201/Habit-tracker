from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from api.exceptions.responses import (
    habit_already_pointed,
    habit_not_found_response,
    unauthorized_response,
    forbid_response,
)

add_habit_tracking_responses = {
    HTTP_400_BAD_REQUEST: habit_already_pointed,
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
    HTTP_404_NOT_FOUND: habit_not_found_response,
}
