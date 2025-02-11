from authentication.strategy import get_database_strategy
from authentication.transport import bearer_transport
from fastapi_users.authentication import AuthenticationBackend

authentication_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
