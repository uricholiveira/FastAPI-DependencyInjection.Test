import pathlib
from contextlib import AbstractContextManager
from typing import Callable

import psutil
from psutil._common import sdiskusage
from sqlalchemy.orm import Session


class HealthCheckRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    async def get_database_status(self) -> bool:
        with self.session_factory() as session:
            try:
                session.execute("SELECT 1")
                return True
            except Exception:
                return False

    async def get_cpu_percent(self) -> float:
        return psutil.cpu_percent(interval=None)

    async def get_disk_usage(self) -> sdiskusage:
        path = pathlib.Path()
        return psutil.disk_usage(path.absolute().__str__())

    async def get_memory_info(self) -> None:
        return psutil.virtual_memory()
