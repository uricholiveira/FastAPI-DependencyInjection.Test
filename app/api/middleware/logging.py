import json
import logging
import time
from typing import Any, Callable

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import Message

from app.api.middleware.util.async_interator import AsyncIteratorWrapper
from app.api.middleware.util.request_context import RequestContext


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: FastAPI, *, logger: logging.Logger, context: RequestContext
    ) -> None:
        self.context = context
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id: str = request.state.request_id
        logging_dict = {
            # X-Request-Id maps each request-response to a unique ID
            "x-request-id": request_id
        }

        await self.set_body(request)
        response, response_dict = await self._log_response(
            call_next, request, request_id
        )
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict

        print(logging_dict)

        return response

    @staticmethod
    async def set_body(request: Request):
        """Avails the response body to be logged within a middleware as,
        it is generally not a standard practice.

           Arguments:
           - request: Request
           Returns:
           - receive_: Receive
        """
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    @staticmethod
    async def _log_request(request: Request) -> dict[str, str | Any]:
        """Logs request part
         Arguments:
        - request: Request

        """

        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host,
        }

        try:
            body = await request.json()
            request_logging["body"] = body
        except Exception:
            body = None

        return request_logging

    async def _log_response(
        self, call_next: Callable, request: Request, request_id: str
    ) -> tuple[Response, dict[str, str | int | Any]]:
        """Logs response part

        Arguments:
        - call_next: Callable (To execute the actual path function and get response back)
        - request: Request
        - request_id: str (uuid)
        Returns:
        - response: Response
        - response_logging: str
        """

        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request, request_id)
        finish_time = time.perf_counter()

        overall_status = "successful" if response and response.status_code < 400 else "failed"
        execution_time = finish_time - start_time

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s",
        }

        resp_body = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

        try:
            resp_body = json.loads(resp_body[0].decode())
        except Exception:
            resp_body = str(resp_body)

        response_logging["body"] = resp_body

        return response, response_logging

    @staticmethod
    async def _execute_request(
        call_next: Callable, request: Request, request_id: str
    ) -> Response:
        """Executes the actual path function using call_next.
        It also injects "X-Request-Id" header to the response.

        Arguments:
        - call_next: Callable (To execute the actual path function
                     and get response back)
        - request: Request
        - request_id: str (uuid)
        Returns:
        - response: Response
        """
        try:
            response: Response = await call_next(request)

            # Kickback X-Request-ID
            response.headers["X-Request-Id"] = request_id
            return response

        except Exception as e:
            print({"path": request.url.path, "method": request.method, "reason": e})
