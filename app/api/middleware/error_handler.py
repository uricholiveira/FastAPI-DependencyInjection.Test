import logging
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.middleware.util.request_context import RequestContext


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
            self, app: FastAPI, *, logger: logging.Logger, context: RequestContext
    ) -> None:
        self.context = context
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            raise HTTPException(status_code=500, detail={'message': 'Error handler', 'exception': str(exc)}) from exc
            # return JSONResponse(status_code=500, content={'reason': str(exc)})
