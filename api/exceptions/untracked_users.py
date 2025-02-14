from exceptions.responses import forbid_response, unauthorized_response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

untracked_users_responses = {
    HTTP_401_UNAUTHORIZED: unauthorized_response,
    HTTP_403_FORBIDDEN: forbid_response,
}
