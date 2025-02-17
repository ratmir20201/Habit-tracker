import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Функция переопределенная из BaseHTTPMiddleware."""

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info("{method} {url} - {status_code} | Time: {process_time:.2f}s".format(
            method=request.method,
            url=request.url,
            status_code=response.status_code,
            process_time=process_time,
        ))

        return response