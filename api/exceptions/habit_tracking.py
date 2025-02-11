from exceptions.responses import (forbid_response, habit_already_pointed,
                                  habit_not_found_response,
                                  unauthorized_response)
from starlette.status import (HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
                              HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND)

add_habit_tracking_responses = {
    HTTP_400_BAD_REQUEST: habit_already_pointed,
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
    HTTP_404_NOT_FOUND: habit_not_found_response,
}
