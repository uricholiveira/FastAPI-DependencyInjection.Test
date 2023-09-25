import logging

from fastapi import FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.middleware import LoggingMiddleware, RequestTraceMiddleware
from app.api.middleware.util.request_context import RequestContext
from app.api.route import routers
from app.core.container import Container


def create_app() -> FastAPI:
    container = Container()
    request_context = RequestContext()

    # TODO: Run this on startup method
    try:
        database = container.db()
        database.create_database()
    except Exception as ex:
        print(ex)

    app = FastAPI()
    app.container = container
    for router in routers:
        app.include_router(router=router)

    # for middleware in middlewares:
    #     app.add_middleware(middleware.get("middleware"), **middleware.get("args"))

    app.request_context = request_context

    app.add_middleware(ProxyHeadersMiddleware)
    app.add_middleware(
        LoggingMiddleware,
        logger=logging.getLogger(__name__),
        context=app.request_context,
    )
    app.add_middleware(
        RequestTraceMiddleware,
        logger=logging.getLogger(__name__),
        context=app.request_context,
    )

    return app


app = create_app()
