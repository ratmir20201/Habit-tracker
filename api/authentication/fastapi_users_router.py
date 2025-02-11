from authentication.backend import authentication_backend
from dependencies.user_manager import get_user_manager
from fastapi_users import FastAPIUsers
from models.user import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
