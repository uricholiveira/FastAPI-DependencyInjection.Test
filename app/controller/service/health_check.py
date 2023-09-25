from app.controller.repository.health_check import HealthCheckRepository
from app.core.settings import settings
from app.domain.schema import health_check as model


class HealthCheckService:
    def __init__(self, health_check_repository: HealthCheckRepository) -> None:
        self._repository: HealthCheckRepository = health_check_repository

    async def get_info(self) -> model.HealthCheckResponse:
        memory = await self._repository.get_memory_info()
        database = await self._repository.get_database_status()
        cpu = await self._repository.get_cpu_percent()
        disk = await self._repository.get_disk_usage()

        return model.HealthCheckResponse(
            service=model.HealthCheckAppResponse(
                name=settings.app.title, status="OK", version=settings.app.version
            ),
            cpu=model.HealthCheckCPUResponse(percent=cpu),
            disk=model.HealthCheckDiskResponse(
                free=disk.free,
                used=disk.used,
                total=disk.total,
                percent=disk.percent,
            ),
            memory=model.HealthCheckMemoryResponse(
                total=memory.total if memory is not None else 0,
                available=memory.available if memory is not None else 0,
                percent=memory.percent if memory is not None else 0,
            ),
            database=model.HealthCheckDatabaseResponse(is_active=database),
        )
