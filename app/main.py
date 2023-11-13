import logging

from fastapi import FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.middleware import (ErrorHandlerMiddleware, LoggingMiddleware,
                                RequestTraceMiddleware)
from app.api.middleware.util.request_context import RequestContext
from app.api.route import routers
from app.core.container import Container
from app.core.rabbitmq import RabbitMQManager


def create_app() -> FastAPI:
    container = Container()
    request_context = RequestContext()

    fastapi = FastAPI()
    fastapi.container = container
    for router in routers:
        fastapi.include_router(router=router)

    # for middleware in middlewares:
    #     app.add_middleware(middleware.get("middleware"), **middleware.get("args"))

    fastapi.request_context = request_context

    fastapi.add_middleware(ProxyHeadersMiddleware)
    fastapi.add_middleware(
        ErrorHandlerMiddleware,
        logger=logging.getLogger(__name__),
        context=fastapi.request_context,
    )
    fastapi.add_middleware(
        LoggingMiddleware,
        logger=logging.getLogger(__name__),
        context=fastapi.request_context,
    )
    fastapi.add_middleware(
        RequestTraceMiddleware,
        logger=logging.getLogger(__name__),
        context=fastapi.request_context,
    )

    return fastapi


app: FastAPI = create_app()


@app.on_event("startup")
async def startup_event():
    database = app.container.db()
    database.create_database()

    app.state.database = database

    rabbitmq_manager = RabbitMQManager(url="amqp://guest:guest@localhost/")
    await rabbitmq_manager.connect()
    app.state.rabbitmq_manager = rabbitmq_manager


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.rabbitmq_manager.close()
