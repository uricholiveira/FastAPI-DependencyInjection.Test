import logging
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.middleware.util.request_context import RequestContext
from app.util.constants import X_REQUEST_ID_HEADER_NAME


class RequestTraceMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: FastAPI, *, logger: logging.Logger, context: RequestContext
    ) -> None:
        self.context = context
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = await self._get_request_id(request)
        request.state.request_id = request_id
        request.state.context = self.context

        response: Response = await call_next(request)
        response.headers[X_REQUEST_ID_HEADER_NAME] = request_id

        return response

    async def _get_request_id(self, request: Request) -> str:
        request_id = request.headers.get(X_REQUEST_ID_HEADER_NAME)
        if request_id is None:
            request_id = str(uuid.uuid4().hex)

        self.context.request_id.set(request_id)
        return request_id
