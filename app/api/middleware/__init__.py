from app.api.middleware.logging import LoggingMiddleware
from app.api.middleware.request_trace import RequestTraceMiddleware

middlewares = [
    {"middleware": RequestTraceMiddleware, "args": {}},
    {"middleware": LoggingMiddleware, "args": {}},
]
