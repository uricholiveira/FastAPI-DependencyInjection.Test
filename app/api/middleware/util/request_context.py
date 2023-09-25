from contextvars import ContextVar


class RequestContext:
    def __init__(self):
        self.request_id = ContextVar("request_id")
        self.request_id.set(None)

        self.access_token = ContextVar("access_token")
        self.access_token.set(None)
