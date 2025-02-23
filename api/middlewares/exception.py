from fastapi.responses import JSONResponse
from logger import logger
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class ExceptionHandleMiddleware(BaseHTTPMiddleware):
    """Middleware для обработки базовых исключений."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response | JSONResponse:
        """Функция переопределенная из BaseHTTPMiddleware."""
        try:
            return await call_next(request)
        except SQLAlchemyError as exc:
            logger.error("Exception: {exc}".format(exc=str(exc)))
            return JSONResponse(
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": str(exc)},
                )

        except Exception as exc:
            logger.error("Exception: {exc}".format(exc=str(exc)))
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": str(exc)},
            )
