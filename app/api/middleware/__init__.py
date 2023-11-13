from app.api.middleware.error_handler import ErrorHandlerMiddleware
from app.api.middleware.logging import LoggingMiddleware
from app.api.middleware.request_trace import RequestTraceMiddleware

middlewares = [
    {"middleware": ErrorHandlerMiddleware, "args": {}},
    {"middleware": RequestTraceMiddleware, "args": {}},
    {"middleware": LoggingMiddleware, "args": {}},
]
